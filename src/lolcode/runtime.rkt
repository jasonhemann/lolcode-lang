#lang racket/base

(require racket/class
         racket/list
         racket/match
         racket/string
         "ast.rkt"
         "runtime/env.rkt"
         "runtime/value.rkt"
         "runtime/operators.rkt")

(provide compile-program
         execute-program)

(struct exn:fail:unsupported exn:fail (where) #:transparent)

(define (raise-unsupported where)
  (raise
   (exn:fail:unsupported
    (format "unsupported AST form: ~e" where)
    (current-continuation-marks)
    where)))

(define (raise-unsupported-op kind op where)
  (raise
   (exn:fail:unsupported
    (format "unsupported ~a operator: ~a" kind op)
    (current-continuation-marks)
    where)))

(define (compile-slot-name slot)
  (match slot
    [(expr-ident name) (lambda (_e _ctx) name)]
    [(expr-srs inner)
     (define inner-proc (compile-expr inner))
     (lambda (e ctx)
       (identifier-text
        "SRS slot must evaluate to identifier text"
        (inner-proc e ctx)))]
    [_ (raise-unsupported slot)]))

(define (compile-target-name target)
  (match target
    [(expr-ident name) (lambda (_e _ctx) name)]
    [(expr-srs inner)
     (define inner-proc (compile-expr inner))
     (lambda (e ctx)
       (identifier-text
        "SRS target must evaluate to identifier text"
        (inner-proc e ctx)))]
    [_ (raise-unsupported target)]))

(struct lvalue (read write) #:transparent)

(define (compile-name-resolver who name-spec)
  (cond
    [(string? name-spec)
     (lambda (_e _ctx) name-spec)]
    [(expr-srs? name-spec)
     (define inner-proc
       (compile-expr (expr-srs-expr name-spec)))
     (lambda (e ctx)
       (identifier-text
        who
        (inner-proc e ctx)))]
    [else
     (define name-proc (compile-expr name-spec))
     (lambda (e ctx)
       (identifier-text
        who
        (name-proc e ctx)))]))

(define (dynamic-alias-binding name-spec resolved-name)
  (and (expr-srs? name-spec)
       (expr-ident? (expr-srs-expr name-spec))
       (cons (expr-ident-name (expr-srs-expr name-spec))
             resolved-name)))

(define (compile-lvalue target
                        #:define-missing? [define-missing? #f])
  (match target
    [(or (expr-ident _) (expr-srs _))
     (define name-proc (compile-target-name target))
     (define (lv-read e ctx)
       (env-ref e (name-proc e ctx)))
     (define (lv-write e value ctx)
       (define name (name-proc e ctx))
       (cond
         [(env-lookup-box e name)
          => (lambda (b)
               (set-box! b value))]
         [define-missing?
          (env-define! e name value)]
         [else
          (error 'run-program "unknown identifier: ~a" name)]))
     (lvalue lv-read lv-write)]
    [(expr-slot object slot)
     (define object-proc (compile-expr object))
     (define slot-name-proc (compile-slot-name slot))
     (define (lv-read e ctx)
       (define obj (object-proc e ctx))
       (unless (lol-object? obj)
         (error 'run-program "slot lookup requires BUKKIT, got ~e" obj))
       (send obj get-slot (slot-name-proc e ctx) noob))
     (define (lv-write e value ctx)
       (define obj (object-proc e ctx))
       (unless (lol-object? obj)
         (error 'run-program "slot assignment requires BUKKIT, got ~e" obj))
       (send obj set-slot! (slot-name-proc e ctx) value))
     (lvalue lv-read lv-write)]
    [_ (raise-unsupported target)]))

(define (resolve-callable e ctx name who)
  (define maybe-callable
    (or (hash-ref (runtime-functions ctx) name #f)
        (let ([maybe-box (env-lookup-box e name)])
          (and maybe-box (unbox maybe-box)))))
  (if (procedure? maybe-callable)
      maybe-callable
      (error 'run-program "unknown ~a: ~a" who name)))

(define (compile-declare-init init-expr)
  (cond
    [(not init-expr)
     (lambda (_e _ctx) noob)]
    [(expr-type-default? init-expr)
     (compile-expr init-expr)]
    [(expr-ident? init-expr)
     (define type-name (expr-ident-name init-expr))
     (define-values (known? default-value)
       (type-default-value type-name))
     (if known?
         (if (string-ci=? type-name "BUKKIT")
             (lambda (_e _ctx) (new lol-object%))
             (lambda (_e _ctx) default-value))
         (compile-expr init-expr))]
    [else
     (compile-expr init-expr)]))

(define (loop-continue? e cond-kind cond-proc ctx)
  (cond
    [(not cond-kind) #t]
    [else
     (define cond-value (lol-truthy? (cond-proc e ctx)))
     (case (string->symbol cond-kind)
       [(TIL) (not cond-value)]
       [(WILE) cond-value]
       [else
        (error 'run-program "unknown loop condition mode: ~a" cond-kind)])]))

(define (make-loop-env e update-var)
  (define loop-env (extend-env e))
  (when update-var
    (define initial
      (cond
        [(env-lookup-box e update-var) => unbox]
        [else 0]))
    ;; Iteration variable is temporary and local to this loop.
    (env-define! loop-env update-var initial))
  loop-env)

(define (apply-loop-update! e update-var update-op ctx)
  (when (and update-var update-op)
    (define current
      (cond
        [(env-lookup-box e update-var) => unbox]
        [else
         (error 'run-program
                "loop variable missing during update: ~a"
                update-var)]))
    (define updated
      (cond
        [(and (string? update-op)
              (or (string=? update-op "UPPIN")
                  (string=? update-op "NERFIN")))
         (define current-num (coerce-number 'LOOP current))
         (define delta
           (if (string=? update-op "UPPIN") 1 -1))
         (+ current-num delta)]
        [(and (pair? update-op)
              (eq? (car update-op) 'FUNC)
              (pair? (cdr update-op))
              (string? (cadr update-op)))
         (define fn-name (cadr update-op))
         (define fn
           (hash-ref (runtime-functions ctx) fn-name #f))
         (unless (procedure? fn)
           (error 'run-program "unknown function: ~a" fn-name))
         (fn e (list current) ctx)]
        [else
         (error 'run-program "unsupported loop updater: ~e" update-op)]))
    (env-set! e update-var updated)
    (set-it! e updated)))

(define (expand-format-placeholders e text)
  (define out (open-output-string))
  (define pattern #px":\\{([^\\}]*)\\}")
  (define (loop start)
    (match (regexp-match-positions pattern text start)
      [#f
       (display (substring text start) out)
       (get-output-string out)]
      [(list (cons match-start match-end)
             (cons name-start name-end))
       (define raw-name (substring text name-start name-end))
       (define name (string-trim raw-name))
       (when (string=? name "")
         (error 'run-program "empty :{...} placeholder in YARN literal"))
       (display (substring text start match-start) out)
       (display (lol-string (env-ref e name)) out)
       (loop match-end)]))
  (loop 0))

(define (switch-literal-key expr)
  (match expr
    [(expr-number text)
     (list 'NUM (or (string->number text) text))]
    [(expr-string text)
     (list 'YARN text)]
    [(expr-literal value)
     (list 'LIT value)]
    [_ #f]))

(define (validate-switch-cases! cases)
  (define seen (make-hash))
  (for ([c (in-list cases)])
    (match-define (switch-case case-match _case-body) c)
    (define key (switch-literal-key case-match))
    (when key
      (when (hash-has-key? seen key)
        (error 'run-program
               "duplicate OMG literal in WTF?: ~e"
               case-match))
      (hash-set! seen key #t))))

(define (compile-expr expr)
  (match expr
    [(expr-number text)
     (lambda (_e _ctx)
       (or (string->number text)
           (error 'run-program "invalid number literal: ~a" text)))]

    [(expr-string text)
     (lambda (e _ctx) (expand-format-placeholders e text))]

    [(expr-literal value)
     (lambda (_e _ctx)
       (if (eq? value 'NOOB) noob value))]

    [(expr-type-default type-name)
     (define-values (known? default-value)
       (type-default-value type-name))
     (unless known?
       (error 'run-program "unknown type name in ITZ A: ~a" type-name))
     (if (string-ci=? type-name "BUKKIT")
         (lambda (_e _ctx) (new lol-object%))
         (lambda (_e _ctx) default-value))]

    [(expr-ident name)
     (lambda (e _ctx) (env-ref e name))]

    [(expr-srs inner)
     (define inner-proc (compile-expr inner))
     (lambda (e ctx)
       (define resolved-name
         (identifier-text
          "SRS expression must evaluate to identifier text"
          (inner-proc e ctx)))
       (env-ref e resolved-name))]

    [(expr-clone inner)
     (define inner-proc (compile-expr inner))
     (lambda (e ctx)
       (define value (inner-proc e ctx))
       (unless (lol-object? value)
         (error 'run-program "LIEK initializer requires BUKKIT value, got ~e" value))
       (send value clone))]

    [(expr-binary op left right)
     (define left-proc (compile-expr left))
     (define right-proc (compile-expr right))
     (define op-fn
       (or (hash-ref binary-operator-table op #f)
           (raise-unsupported-op 'binary op expr)))
     (lambda (e ctx)
       (op-fn (left-proc e ctx) (right-proc e ctx)))]

    [(expr-unary op arg)
     (define arg-proc (compile-expr arg))
     (define op-fn
       (or (hash-ref unary-operator-table op #f)
           (raise-unsupported-op 'unary op expr)))
     (lambda (e ctx)
       (op-fn (arg-proc e ctx)))]

    [(expr-variadic op args)
     (define arg-procs (map compile-expr args))
     ((or (hash-ref variadic-operator-compiler-table op #f)
          (raise-unsupported-op 'variadic op expr))
      arg-procs)]

    [(expr-call name args)
     (define name-proc
       (compile-name-resolver
        "function name must evaluate to identifier text"
        name))
     (define arg-procs (map compile-expr args))
     (lambda (e ctx)
       (define fn-name
         (name-proc e ctx))
       (define fn (resolve-callable e ctx fn-name "function"))
       (fn e
           (map (lambda (a) (a e ctx)) arg-procs)
           ctx))]

    [(expr-method-call receiver name args)
     (define recv-proc
       (and (not (expr-ident? receiver))
            (compile-expr receiver)))
     (define receiver-ident
       (and (expr-ident? receiver)
            (expr-ident-name receiver)))
     (define arg-procs (map compile-expr args))
     (lambda (e ctx)
       (define arg-values
         (map (lambda (a) (a e ctx)) arg-procs))
       (define (invoke-on-object obj)
         (send obj
               invoke-method
               name
               arg-values
               ctx
               (lambda ()
                 (define maybe-slot-callable
                   (send obj get-slot name #f))
                 (cond
                   [(procedure? maybe-slot-callable)
                    (maybe-slot-callable e arg-values ctx)]
                   [else
                    ((resolve-callable e ctx name "method")
                     e
                     arg-values
                     ctx)]))))
       (cond
         [receiver-ident
          (define maybe-box
            (env-lookup-box e receiver-ident))
             (if maybe-box
              (let ([recv-val (unbox maybe-box)])
                (unless (lol-object? recv-val)
                  (error 'run-program "method call requires BUKKIT receiver, got ~e" recv-val))
                (invoke-on-object recv-val))
              (let* ([ns-fn-name (format "~a'Z ~a" receiver-ident name)]
                     [ns-fn (hash-ref (runtime-functions ctx) ns-fn-name #f)])
                (if (procedure? ns-fn)
                    (ns-fn e arg-values ctx)
                    (error 'run-program "unknown identifier: ~a" receiver-ident))))]
         [else
          (define obj (recv-proc e ctx))
          (unless (lol-object? obj)
            (error 'run-program "method call requires BUKKIT receiver, got ~e" obj))
          (invoke-on-object obj)]))]

    [(expr-cast inner type-name)
     (define inner-proc (compile-expr inner))
     (lambda (e ctx)
       (cast-value 'MAEK (inner-proc e ctx) type-name))]

    [(expr-slot object slot)
     (define lv (compile-lvalue (expr-slot object slot)))
     (lambda (e ctx)
       ((lvalue-read lv) e ctx))]

    [_ (raise-unsupported expr)]))

(define (compile-block statements)
  (define stmt-procs
    (map compile-stmt statements))
  (lambda (e ctx)
    (for ([stmt-proc (in-list stmt-procs)])
      (stmt-proc e ctx))))

(define (compile-stmt-declare target init)
  (define name-proc (compile-target-name target))
  (define init-proc (compile-declare-init init))
  (lambda (e ctx)
    (define value (init-proc e ctx))
    (env-define! e (name-proc e ctx) value)))

(define (compile-stmt-assign target expr)
  (define lv
    (compile-lvalue target #:define-missing? #t))
  (define expr-proc (compile-expr expr))
  (lambda (e ctx)
    (define value (expr-proc e ctx))
    ((lvalue-write lv) e value ctx)))

(define (compile-stmt-cast target type-name)
  (define lv
    (compile-lvalue target #:define-missing? #f))
  (lambda (e ctx)
    (define value
      (cast-value 'IS-NOW-A
                  ((lvalue-read lv) e ctx)
                  type-name))
    ((lvalue-write lv) e value ctx)
    (set-it! e value)))

(define (compile-stmt-input target)
  (define lv
    (compile-lvalue target #:define-missing? #t))
  (lambda (e ctx)
    (define line (read-line (current-input-port) 'any))
    (define value
      (if (eof-object? line) noob line))
    ((lvalue-write lv) e value ctx)
    (set-it! e value)))

(define (compile-stmt-slot-set object slot expr)
  (define object-proc (compile-expr object))
  (define slot-name-proc (compile-slot-name slot))
  (define expr-proc (compile-declare-init expr))
  (lambda (e ctx)
    (define obj (object-proc e ctx))
    (unless (lol-object? obj)
      (error 'run-program "slot assignment requires BUKKIT, got ~e" obj))
    (define value (expr-proc e ctx))
    (send obj set-slot! (slot-name-proc e ctx) value)
    (set-it! e value)))

(define (compile-stmt-visible exprs suppress-newline?)
  (define expr-procs (map compile-expr exprs))
  (lambda (e ctx)
    (define values
      (map (lambda (ep) (ep e ctx)) expr-procs))
    (for ([v (in-list values)])
      (display (lol-string v) (runtime-stdout ctx)))
    (unless suppress-newline?
      (newline (runtime-stdout ctx)))
    (when (pair? values)
      (set-it! e (last values)))))

(define (compile-stmt-if condition then-branch mebbe-branches else-branch)
  (define cond-proc (compile-expr condition))
  (define then-proc (compile-block then-branch))
  (define mebbe-procs
    (for/list ([mb (in-list mebbe-branches)])
      (match-define (mebbe-branch mebbe-condition mebbe-body) mb)
      (cons (compile-expr mebbe-condition)
            (compile-block mebbe-body))))
  (define else-proc (compile-block else-branch))
  (lambda (e ctx)
    (cond
      [(lol-truthy? (cond-proc e ctx))
       (then-proc (extend-env e) ctx)]
      [else
       (define (mebbe-loop remaining)
         (match remaining
           ['()
            (else-proc (extend-env e) ctx)]
           [(cons (cons mb-cond mb-body) rest)
            (if (lol-truthy? (mb-cond e ctx))
                (mb-body (extend-env e) ctx)
                (mebbe-loop rest))]))
       (mebbe-loop mebbe-procs)])))

(define (compile-stmt-switch subject cases default)
  (validate-switch-cases! cases)
  (define subject-proc (compile-expr subject))
  (define case-procs
    (for/list ([c (in-list cases)])
      (match-define (switch-case case-match case-body) c)
      (cons (compile-expr case-match)
            (compile-block case-body))))
  (define default-proc (compile-block default))
  (lambda (e ctx)
    (let/ec break-k
      (define subject-value (subject-proc e ctx))
      (define switch-ctx
        (ctx-derive ctx #:break-k break-k))
      (define (find-first remaining idx)
        (match remaining
          ['() #f]
          [`((,case-match-proc . ,_case-body-proc) . ,rest)
           (if (equal? subject-value (case-match-proc e ctx))
               idx
               (find-first rest (+ idx 1)))]))
      (define (run-cases remaining)
        (match remaining
          ['() (void)]
          [`((,_case-match-proc . ,case-body-proc) . ,rest)
           (case-body-proc (extend-env e) switch-ctx)
           (run-cases rest)]))
      (match (find-first case-procs 0)
        [(? number? idx)
         (run-cases (drop case-procs idx))]
        [_
         (default-proc (extend-env e) switch-ctx)]))))

(define (compile-stmt-loop _label update-var update-op cond-kind cond-expr body)
  (define cond-proc (and cond-expr (compile-expr cond-expr)))
  (define body-proc (compile-block body))
  (lambda (e ctx)
    (define loop-env
      (make-loop-env e update-var))
    (let/ec break-k
      (define loop-ctx
        (ctx-derive ctx #:break-k break-k))
      (define (loop)
        (when (loop-continue? loop-env cond-kind cond-proc loop-ctx)
          (body-proc (extend-env loop-env) loop-ctx)
          (apply-loop-update! loop-env update-var update-op loop-ctx)
          (loop)))
      (loop))))

(define (compile-stmt-function-def name params body)
  (define body-proc (compile-block body))
  (define name-proc
    (compile-name-resolver
     "function name must evaluate to identifier text"
     name))
  (define param-name-procs
    (map (lambda (param)
           (compile-name-resolver
            "parameter name must evaluate to identifier text"
            param))
         params))
  (lambda (e ctx)
    (define resolved-name
      (name-proc e ctx))
    (define resolved-params
      (map (lambda (param-name-proc)
             (param-name-proc e ctx))
           param-name-procs))
    (define dynamic-aliases
      (filter values
              (append
               (list (dynamic-alias-binding name resolved-name))
               (for/list ([param-spec (in-list params)]
                          [resolved-param (in-list resolved-params)])
                 (dynamic-alias-binding param-spec resolved-param)))))
    (define def-env e)
    (define method-lexical-parent
      (if (exec-ctx-def-object ctx)
          (env-parent def-env)
          def-env))
    (define (make-global-fn fn-name param-names aliases)
      (lambda (_caller-env arg-values caller-ctx)
        (unless (= (length param-names) (length arg-values))
          (error 'run-program
                 "function ~a expected ~a args, got ~a"
                 fn-name
                 (length param-names)
                 (length arg-values)))
        ;; LOLCODE functions run in their own variable scope and do not
        ;; capture variables from surrounding blocks.
        (define call-env (make-root-env))
        (for ([param (in-list param-names)]
              [arg (in-list arg-values)])
          (env-define! call-env param arg))
        (for ([alias (in-list aliases)])
          (define alias-name (car alias))
          (define alias-value (cdr alias))
          (unless (env-lookup-box call-env alias-name)
            (env-define! call-env alias-name alias-value)))
        (env-define! call-env "IT" noob)
        (let/ec return-k
          (define fn-ctx
            (ctx-derive caller-ctx
                        #:return-k return-k
                        #:break-k #f
                        #:object-name #f
                        #:def-object #f))
          (body-proc call-env fn-ctx)
          (env-ref call-env "IT"))))
    (define (make-method-fn fn-name param-names)
      (lambda (receiver arg-values caller-ctx)
        (unless (= (length param-names) (length arg-values))
          (error 'run-program
                 "method ~a expected ~a args, got ~a"
                 fn-name
                 (length param-names)
                 (length arg-values)))
        (define receiver-env
          (env-with-table (send receiver slot-table)
                          method-lexical-parent))
        (define call-env (extend-env receiver-env))
        (for ([param (in-list param-names)]
              [arg (in-list arg-values)])
          (env-define! call-env param arg))
        (env-define! call-env "ME" receiver)
        (env-define! call-env "IT" noob)
        (let/ec return-k
          (define fn-ctx
            (ctx-derive caller-ctx
                        #:return-k return-k
                        #:break-k #f
                        #:object-name #f
                        #:def-object #f))
          (body-proc call-env fn-ctx)
          (env-ref call-env "IT"))))
    (define global-fn
      (make-global-fn resolved-name resolved-params dynamic-aliases))
    (cond
      [(exec-ctx-def-object ctx)
       (send (exec-ctx-def-object ctx)
             define-method!
             resolved-name
             (make-method-fn resolved-name resolved-params))]
      [(eq? e (runtime-globals ctx))
       (hash-set! (runtime-functions ctx) resolved-name global-fn)
       (env-set-or-define! e resolved-name global-fn)]
      [else
       (env-set-or-define! e resolved-name global-fn)])))

(define (compile-stmt-method-def receiver name params body)
  (define receiver-proc (compile-expr receiver))
  (define body-proc (compile-block body))
  (define name-proc
    (compile-name-resolver
     "method name must evaluate to identifier text"
     name))
  (define param-name-procs
    (map (lambda (param)
           (compile-name-resolver
            "parameter name must evaluate to identifier text"
            param))
         params))
  (lambda (e ctx)
    (define resolved-name
      (name-proc e ctx))
    (define resolved-params
      (map (lambda (param-name-proc)
             (param-name-proc e ctx))
           param-name-procs))
    (define target (receiver-proc e ctx))
    (unless (lol-object? target)
      (error 'run-program
             "method declaration requires BUKKIT receiver, got ~e"
             target))
    (define lexical-parent e)
    (define (method-fn receiver-value arg-values caller-ctx)
      (unless (= (length resolved-params) (length arg-values))
        (error 'run-program
               "method ~a expected ~a args, got ~a"
               resolved-name
               (length resolved-params)
               (length arg-values)))
      (define receiver-env
        (env-with-table (send receiver-value slot-table)
                        lexical-parent))
      (define call-env (extend-env receiver-env))
      (for ([param (in-list resolved-params)]
            [arg (in-list arg-values)])
        (env-define! call-env param arg))
      (env-define! call-env "ME" receiver-value)
      (env-define! call-env "IT" noob)
      (let/ec return-k
        (define fn-ctx
          (ctx-derive caller-ctx
                      #:return-k return-k
                      #:break-k #f
                      #:object-name #f
                      #:def-object #f))
        (body-proc call-env fn-ctx)
        (env-ref call-env "IT")))
    (send target define-method! resolved-name method-fn)))

(define (compile-stmt-object-def name parent body)
  (define body-proc (compile-block body))
  (lambda (e ctx)
    (define obj
      (if parent
          (let ([p (env-ref e parent)])
            (unless (lol-object? p)
              (error 'run-program "object parent must be BUKKIT, got ~e" p))
            (send p clone))
          (new lol-object%)))
    (send obj set-slot! "IT" noob)
    (define object-ctx
      (ctx-derive ctx
                  #:object-name name
                  #:def-object obj))
    (body-proc (env-with-table (send obj slot-table) e)
               object-ctx)
    (when (send obj has-slot? "IT")
      (send obj remove-slot! "IT"))
    (env-set-or-define! e name obj)
    (set-it! e obj)))

(define (compile-stmt-return expr)
  (define expr-proc (compile-expr expr))
  (lambda (e ctx)
    (define value (expr-proc e ctx))
    (set-it! e value)
    (ctx-return! ctx value)))

(define (compile-stmt-break)
  (lambda (_e ctx)
    (ctx-break! ctx)))

(define (compile-stmt-import _library)
  (lambda (_e _ctx)
    (void)))

(define (compile-stmt-expr expr)
  (define expr-proc (compile-expr expr))
  (lambda (e ctx)
    (define value (expr-proc e ctx))
    (set-it! e value)))

(define (compile-stmt stmt)
  (match stmt
    [(stmt-declare target init)
     (compile-stmt-declare target init)]
    [(stmt-assign target expr)
     (compile-stmt-assign target expr)]
    [(stmt-cast target type-name)
     (compile-stmt-cast target type-name)]
    [(stmt-input target)
     (compile-stmt-input target)]
    [(stmt-slot-set object slot expr)
     (compile-stmt-slot-set object slot expr)]
    [(stmt-visible exprs suppress-newline?)
     (compile-stmt-visible exprs suppress-newline?)]
    [(stmt-if condition then-branch mebbe-branches else-branch)
     (compile-stmt-if condition then-branch mebbe-branches else-branch)]
    [(stmt-switch subject cases default)
     (compile-stmt-switch subject cases default)]
    [(stmt-loop label update-var update-op cond-kind cond-expr body)
     (compile-stmt-loop label update-var update-op cond-kind cond-expr body)]
    [(stmt-function-def name params body)
     (compile-stmt-function-def name params body)]
    [(stmt-method-def receiver name params body)
     (compile-stmt-method-def receiver name params body)]
    [(stmt-object-def name parent body)
     (compile-stmt-object-def name parent body)]
    [(stmt-return expr)
     (compile-stmt-return expr)]
    [(stmt-break)
     (compile-stmt-break)]
    [(stmt-import library)
     (compile-stmt-import library)]
    [(stmt-expr expr)
     (compile-stmt-expr expr)]
    [_ (raise-unsupported stmt)]))

(define (compile-program parsed [phase 'unknown])
  (unless (program? parsed)
    (raise-argument-error 'compile-program "program?" parsed))
  (lambda ()
    (define globals (make-root-env))
    (define functions (make-hash))
    (install-runtime-builtins! functions)
    (define stdout (open-output-string))
    (env-define! globals "IT" noob)
    (define st
      (runstate globals functions stdout phase))
    (define root-ctx
      (exec-ctx st #f #f #f #f))
    (with-handlers ([exn:fail:unsupported?
                     (lambda (e)
                       (hash 'status 'unsupported
                             'phase (runstate-phase st)
                             'stdout (get-output-string stdout)
                             'last-value (env-ref globals "IT")
                             'reason (exn-message e)
                             'where (exn:fail:unsupported-where e)))]
                    [exn:fail?
                     (lambda (e)
                       (hash 'status 'runtime-error
                             'phase (runstate-phase st)
                             'stdout (get-output-string stdout)
                             'last-value (env-ref globals "IT")
                             'error (exn-message e)))])
      (define program-proc
        (compile-block (program-statements parsed)))
      (program-proc globals root-ctx)
      (hash 'status 'ok
            'phase (runstate-phase st)
            'stdout (get-output-string stdout)
            'last-value (env-ref globals "IT")))))

(define (execute-program parsed phase)
  ((compile-program parsed phase)))
