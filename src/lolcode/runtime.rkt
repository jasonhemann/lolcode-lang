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
  (match name-spec
    [(expr-literal value)
     (lambda (_e _ctx)
       (identifier-text who value))]
    [(expr-srs inner)
     (define inner-proc
       (compile-expr inner))
     (lambda (e ctx)
       (identifier-text
        who
        (inner-proc e ctx)))]
    [_ (error 'run-program "invalid name spec: ~e" name-spec)]))

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
       (send obj get-slot (slot-name-proc e ctx) noob ctx))
     (define (lv-write e value ctx)
       (define obj (object-proc e ctx))
       (unless (lol-object? obj)
         (error 'run-program "slot assignment requires BUKKIT, got ~e" obj))
       (send obj assign-slot! (slot-name-proc e ctx) value))
     (lvalue lv-read lv-write)]
    [_ (raise-unsupported target)]))

(define (resolve-callable e ctx name who)
  (define maybe-callable
    (let ([maybe-box (env-lookup-box e name)])
      (and maybe-box (unbox maybe-box))))
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
      (update-op e ctx current))
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

(define (resolve-bukkit who value)
  (unless (lol-object? value)
    (error 'run-program "~a requires BUKKIT, got ~e" who value))
  value)

(define (apply-mixins! target mixins)
  ;; Spec says mixins are applied in reverse declaration order.
  (for ([mix (in-list (reverse mixins))])
    (send mix copy-own-into! target)))

(define (run-izmakin-hook! obj e ctx)
  (send obj
        invoke-method
        "izmakin"
        '()
        ctx
        (lambda ()
          (define maybe-slot-hook
            (send obj lookup-slot "izmakin" noob))
          (when (procedure? maybe-slot-hook)
            (maybe-slot-hook e '() ctx))
          (void))))

(define (project-receiver-slot-frame receiver)
  (define own-table
    (send receiver slot-table))
  (define projected-table
    (make-hash))
  (define own-slot-names
    (make-hash))
  (for ([(name b) (in-hash own-table)])
    (hash-set! projected-table name b)
    (hash-set! own-slot-names name #t))
  (define inherited-before
    (make-hash))
  (for ([name (in-list (send receiver slot-names))])
    (unless (hash-has-key? projected-table name)
      (define v
        (send receiver lookup-slot name noob))
      (hash-set! projected-table name (box v))
      (hash-set! inherited-before name v)))
  (values projected-table own-slot-names inherited-before))

(define (sync-receiver-slot-frame! receiver projected-table own-slot-names inherited-before)
  (for ([(name b) (in-hash projected-table)])
    (define value
      (unbox b))
    (cond
      [(hash-has-key? own-slot-names name)
       (send receiver declare-slot! name value)]
      [(hash-has-key? inherited-before name)
       (define prior
         (hash-ref inherited-before name))
       (unless (equal? value prior)
         (send receiver assign-slot! name value))]
      [else
       (void)])))

(define (make-prototype-object parent-obj mixin-objs)
  (define child (send parent-obj prototype))
  (apply-mixins! child mixin-objs)
  ;; Mixins may overwrite parent; restore inheritance parent per spec.
  (send child declare-slot! "parent" parent-obj)
  child)

(define (construct-prototype parent-obj mixin-objs e ctx)
  (define child
    (make-prototype-object parent-obj mixin-objs))
  (run-izmakin-hook! child e ctx)
  child)

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
       (construct-prototype
        (resolve-bukkit "LIEK initializer" (inner-proc e ctx))
        '()
        e
        ctx))]

    [(expr-prototype parent-spec mixins)
     (define parent-name-proc
       (compile-name-resolver
        "prototype parent name must evaluate to identifier text"
        parent-spec))
     (define mixin-name-procs
       (map (lambda (m)
              (compile-name-resolver
               "mixin name must evaluate to identifier text"
               m))
            mixins))
     (lambda (e ctx)
       (define parent-name
         (parent-name-proc e ctx))
       (define parent-obj
         (resolve-bukkit
          "prototype parent"
          (env-ref e parent-name)))
       (define mixin-objs
         (for/list ([mix-proc (in-list mixin-name-procs)])
           (define mix-name (mix-proc e ctx))
           (resolve-bukkit
            "mixin"
            (env-ref e mix-name))))
       (construct-prototype parent-obj mixin-objs e ctx))]

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

    [(expr-method-call receiver name-spec args)
     (define recv-proc
       (and (not (expr-ident? receiver))
            (compile-expr receiver)))
     (define receiver-ident
       (and (expr-ident? receiver)
            (expr-ident-name receiver)))
     (define name-proc
       (compile-name-resolver
        "method name must evaluate to identifier text"
        name-spec))
     (define arg-procs (map compile-expr args))
     (lambda (e ctx)
       (define method-name
         (name-proc e ctx))
       (define arg-values
         (map (lambda (a) (a e ctx)) arg-procs))
       (define (invoke-on-object obj)
         (send obj
               invoke-method
               method-name
               arg-values
               ctx
               (lambda ()
                 (define maybe-slot-callable
                  (send obj lookup-slot method-name #f))
                 (cond
                   [(procedure? maybe-slot-callable)
                    (maybe-slot-callable e arg-values ctx)]
                   [else
                    ((resolve-callable e ctx method-name "method")
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
              (let* ([ns-fn-name (format "~a'Z ~a" receiver-ident method-name)]
                     [ns-fn-box (env-lookup-box e ns-fn-name)]
                     [ns-fn (and ns-fn-box (unbox ns-fn-box))])
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
    (send obj declare-slot! (slot-name-proc e ctx) value)
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

(define (compile-stmt-loop label-open label-close update-var-spec update-op cond-kind cond-expr body)
  (define open-label-proc
    (compile-name-resolver
     "loop label must evaluate to identifier text"
     label-open))
  (define close-label-proc
    (compile-name-resolver
     "loop label must evaluate to identifier text"
     label-close))
  (define update-var-proc
    (and update-var-spec
         (compile-name-resolver
          "loop variable name must evaluate to identifier text"
          update-var-spec)))
  (define update-op-proc
    (cond
      [(not update-op)
       (lambda (_e _ctx) #f)]
      [(and (list? update-op)
            (= (length update-op) 2)
            (eq? (first update-op) 'delta)
            (number? (second update-op)))
       (define delta (second update-op))
       (lambda (_e _ctx)
         (lambda (_loop-env _loop-ctx current)
           (+ (coerce-number 'LOOP current) delta)))]
      [(and (list? update-op)
            (= (length update-op) 2)
            (eq? (first update-op) 'call))
       (define updater-name-proc
         (compile-name-resolver
          "loop updater function name must evaluate to identifier text"
          (second update-op)))
       (lambda (e ctx)
         (define fn-name (updater-name-proc e ctx))
         (lambda (loop-env loop-ctx current)
           (define fn (resolve-callable loop-env loop-ctx fn-name "function"))
           (fn loop-env (list current) loop-ctx)))]
      [else
       (error 'run-program "unsupported loop updater specification: ~e" update-op)]))
  (define cond-proc (and cond-expr (compile-expr cond-expr)))
  (define body-proc (compile-block body))
  (lambda (e ctx)
    (define resolved-open
      (open-label-proc e ctx))
    (define resolved-close
      (close-label-proc e ctx))
    (unless (string-ci=? resolved-open resolved-close)
      (error 'run-program
             "loop label mismatch: ~a closed by ~a"
             resolved-open
             resolved-close))
    (define resolved-update-var
      (and update-var-proc
           (update-var-proc e ctx)))
    (define resolved-update-op
      (update-op-proc e ctx))
    (define loop-env
      (make-loop-env e resolved-update-var))
    (let/ec break-k
      (define loop-ctx
        (ctx-derive ctx #:break-k break-k))
      (define (loop)
        (when (loop-continue? loop-env cond-kind cond-proc loop-ctx)
          (body-proc (extend-env loop-env) loop-ctx)
          (apply-loop-update! loop-env resolved-update-var resolved-update-op loop-ctx)
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
    (define def-env e)
    (define method-lexical-parent
      (if (exec-ctx-def-object ctx)
          (env-parent def-env)
          def-env))
    (define (make-global-fn fn-name param-names)
      (lambda (_caller-env arg-values caller-ctx)
        (unless (= (length param-names) (length arg-values))
          (error 'run-program
                 "function ~a expected ~a args, got ~a"
                 fn-name
                 (length param-names)
                 (length arg-values)))
        ;; LOLCODE functions use a fresh local frame over globals.
        ;; This prevents capture of surrounding local scopes while
        ;; keeping global callables and declarations visible.
        (define call-env (extend-env (runtime-globals caller-ctx)))
        (for ([param (in-list param-names)]
              [arg (in-list arg-values)])
          (env-define! call-env param arg))
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
        (define-values (projected-table own-slot-names inherited-before)
          (project-receiver-slot-frame receiver))
        (define receiver-env
          (env-with-table projected-table
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
          (dynamic-wind
            void
            (lambda ()
              (body-proc call-env fn-ctx)
              (env-ref call-env "IT"))
            (lambda ()
              (sync-receiver-slot-frame!
               receiver
               projected-table
               own-slot-names
               inherited-before))))))
    (define global-fn
      (make-global-fn resolved-name resolved-params))
    (cond
      [(exec-ctx-def-object ctx)
       (send (exec-ctx-def-object ctx)
             define-method!
             resolved-name
             (make-method-fn resolved-name resolved-params))]
      [(eq? e (runtime-globals ctx))
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
      (define-values (projected-table own-slot-names inherited-before)
        (project-receiver-slot-frame receiver-value))
      (define receiver-env
        (env-with-table projected-table
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
        (dynamic-wind
          void
          (lambda ()
            (body-proc call-env fn-ctx)
            (env-ref call-env "IT"))
          (lambda ()
            (sync-receiver-slot-frame!
             receiver-value
             projected-table
             own-slot-names
             inherited-before)))))
    (send target define-method! resolved-name method-fn)))

(define (compile-stmt-object-def name-spec parent-spec mixins body)
  (define name-proc
    (compile-name-resolver
     "object name must evaluate to identifier text"
     name-spec))
  (define parent-proc
    (and parent-spec
         (compile-name-resolver
          "object parent name must evaluate to identifier text"
          parent-spec)))
  (define mixin-name-procs
    (map (lambda (m)
           (compile-name-resolver
            "mixin name must evaluate to identifier text"
            m))
         mixins))
  (define body-proc (compile-block body))
  (lambda (e ctx)
    (define resolved-name
      (name-proc e ctx))
    (define obj
      (if parent-proc
          (let* ([resolved-parent-name
                  (parent-proc e ctx)]
                 [resolved-parent
                  (resolve-bukkit
                   "object parent"
                   (env-ref e resolved-parent-name))]
                 [resolved-mixins
                  (for/list ([mixin-name-proc (in-list mixin-name-procs)])
                    (resolve-bukkit
                     "mixin"
                     (env-ref e (mixin-name-proc e ctx))))])
            (make-prototype-object resolved-parent resolved-mixins))
          (new lol-object%)))
    (send obj set-slot! "IT" noob)
    (define object-ctx
      (ctx-derive ctx
                  #:object-name resolved-name
                  #:def-object obj))
    (body-proc (env-with-table (send obj slot-table) e)
               object-ctx)
    (when (send obj has-slot? "IT")
      (send obj remove-slot! "IT"))
    (run-izmakin-hook! obj e object-ctx)
    (env-set-or-define! e resolved-name obj)
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
    [(stmt-loop label-open label-close update-var update-op cond-kind cond-expr body)
     (compile-stmt-loop label-open label-close update-var update-op cond-kind cond-expr body)]
    [(stmt-function-def name params body)
     (compile-stmt-function-def name params body)]
    [(stmt-method-def receiver name params body)
     (compile-stmt-method-def receiver name params body)]
    [(stmt-object-def name parent mixins body)
     (compile-stmt-object-def name parent mixins body)]
    [(stmt-return expr)
     (compile-stmt-return expr)]
    [(stmt-break)
     (compile-stmt-break)]
    [(stmt-expr expr)
     (compile-stmt-expr expr)]
    [_ (raise-unsupported stmt)]))

(define (compile-program parsed [phase 'unknown])
  (unless (program? parsed)
    (raise-argument-error 'compile-program "program?" parsed))
  (lambda ()
    (define globals (make-root-env))
    (install-runtime-builtins! globals)
    (define stdout (open-output-string))
    (env-define! globals "IT" noob)
    (define st
      (runstate globals stdout phase))
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
