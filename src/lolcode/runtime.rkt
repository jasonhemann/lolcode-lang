#lang racket/base

(require racket/class
         racket/list
         racket/match
         racket/string
         "ast.rkt")

(provide compile-program
         execute-program)

(define noob 'NOOB)

(struct exn:fail:unsupported exn:fail (where) #:transparent)
(struct env (table parent) #:transparent)
(struct runstate (globals functions stdout phase) #:transparent)
(struct exec-ctx (state allow-return? allow-break? object-name def-object) #:transparent)
(struct ctrl-return (value) #:transparent)
(struct ctrl-break () #:transparent)

(define ctrl-normal 'normal)

(define (control-normal? value)
  (eq? value ctrl-normal))

(define (ctx-derive ctx
                    #:allow-return? [allow-return? (exec-ctx-allow-return? ctx)]
                    #:allow-break? [allow-break? (exec-ctx-allow-break? ctx)]
                    #:object-name [object-name (exec-ctx-object-name ctx)]
                    #:def-object [def-object (exec-ctx-def-object ctx)])
  (exec-ctx (exec-ctx-state ctx)
            allow-return?
            allow-break?
            object-name
            def-object))

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

(define (make-root-env)
  (env (make-hash) #f))

(define (extend-env parent)
  (env (make-hash) parent))

(define (env-with-table table parent)
  (env table parent))

(define (env-lookup-box e name)
  (cond
    [(not e) #f]
    [(hash-ref (env-table e) name #f)
     => (lambda (maybe-box)
          (if (box? maybe-box)
              maybe-box
              (env-lookup-box (env-parent e) name)))]
    [else
     (env-lookup-box (env-parent e) name)]))

(define (env-define! e name value)
  (hash-set! (env-table e) name (box value)))

(define (env-ref e name)
  (cond
    [(env-lookup-box e name) => unbox]
    [else
     (error 'run-program "unknown identifier: ~a" name)]))

(define (env-set! e name value)
  (cond
    [(env-lookup-box e name)
     => (lambda (b)
          (set-box! b value))]
    [else
     (error 'run-program "unknown identifier: ~a" name)]))

(define (env-set-or-define! e name value)
  (cond
    [(env-lookup-box e name)
     => (lambda (b)
          (set-box! b value))]
    [else
     (env-define! e name value)]))

(define (set-it! e value)
  (cond
    [(env-lookup-box e "IT")
     => (lambda (maybe-it)
          (set-box! maybe-it value))]
    [else (env-define! e "IT" value)]))

(define lol-object%
  (class object%
    (init-field [slots (make-hash)]
                [methods (make-hash)])
    (super-new)

    (define/public (clone)
      (define copied-slots (make-hash))
      (for ([(name b) (in-hash slots)])
        (hash-set! copied-slots name (box (unbox b))))
      (new lol-object%
           [slots copied-slots]
           [methods (hash-copy methods)]))

    (define/public (slot-table)
      slots)

    (define/public (has-slot? name)
      (hash-has-key? slots name))

    (define/public (get-slot name [default noob])
      (cond
        [(hash-ref slots name #f) => unbox]
        [else default]))

    (define/public (set-slot! name value)
      (cond
        [(hash-ref slots name #f)
         => (lambda (maybe-box)
              (if (box? maybe-box)
                  (set-box! maybe-box value)
                  (hash-set! slots name (box value))))]
        [else (hash-set! slots name (box value))]))

    (define/public (remove-slot! name)
      (hash-remove! slots name))

    (define/public (define-method! name fn)
      (hash-set! methods name fn))

    (define/public (get-method name [default #f])
      (hash-ref methods name default))

    (define/public (invoke-method name arg-values ctx fallback-thunk)
      (define method
        (hash-ref methods name #f))
      (cond
        [(procedure? method) (method this arg-values ctx)]
        [(procedure? fallback-thunk) (fallback-thunk)]
        [else (error 'run-program "unknown method: ~a" name)]))))

(define (lol-object? v)
  (is-a? v lol-object%))

(define (lol-string v)
  (cond
    [(eq? v noob) "NOOB"]
    [(boolean? v) (if v "WIN" "FAIL")]
    [(number? v) (number->string v)]
    [(string? v) v]
    [(lol-object? v) "<BUKKIT>"]
    [else (format "~a" v)]))

(define (lol-truthy? v)
  (cond
    [(eq? v noob) #f]
    [(boolean? v) v]
    [(number? v) (not (zero? v))]
    [(string? v) (not (string=? v ""))]
    [else #t]))

(define (coerce-number who v)
  (coerce-cast-number who v))

(define (coerce-cast-number who v)
  (cond
    [(number? v) v]
    [(boolean? v) (if v 1 0)]
    [(eq? v noob) 0]
    [(string? v)
     (or (string->number (string-trim v))
         (error who "cannot cast YARN to numeric value: ~e" v))]
    [else (error who "cannot cast ~e to numeric value" v)]))

(define (cast-value who v type-name)
  (case (string-upcase type-name)
    [("NUMBR")
     (inexact->exact (truncate (coerce-cast-number who v)))]
    [("NUMBAR")
     (exact->inexact (coerce-cast-number who v))]
    [("YARN")
     (lol-string v)]
    [("TROOF")
     (lol-truthy? v)]
    [("NOOB")
     noob]
    [("BUKKIT")
     (if (lol-object? v)
         (send v clone)
         (error who "cannot cast non-BUKKIT value to BUKKIT: ~e" v))]
    [else
     (error who "unknown cast target type: ~a" type-name)]))

(define (type-default-value type-name)
  (case (string-upcase type-name)
    [("NUMBR" "NUMBAR") (values #t 0)]
    [("YARN") (values #t "")]
    [("TROOF") (values #t #f)]
    [("BUKKIT") (values #t (new lol-object%))]
    [("NOOB") (values #t noob)]
    [else (values #f #f)]))

(define (identifier-text who value)
  (cond
    [(string? value) value]
    [(symbol? value) (symbol->string value)]
    [(number? value) (number->string value)]
    [(boolean? value) (if value "WIN" "FAIL")]
    [(eq? value noob) "NOOB"]
    [else (error 'run-program "~a, got ~e" who value)]))

(define (require-arity who arg-values n)
  (unless (= (length arg-values) n)
    (error 'run-program "~a expected ~a args, got ~a" who n (length arg-values))))

(define (install-runtime-builtins! functions)
  (hash-set!
   functions
   "STRING'Z LEN"
   (lambda (_caller-env arg-values _ctx)
     (require-arity "STRING'Z LEN" arg-values 1)
     (string-length
      (lol-string (first arg-values)))))
  (hash-set!
   functions
   "STRING'Z AT"
   (lambda (_caller-env arg-values _ctx)
     (require-arity "STRING'Z AT" arg-values 2)
     (define text
       (lol-string (first arg-values)))
     (define idx
       (inexact->exact
        (truncate
         (coerce-cast-number "STRING'Z AT index" (second arg-values)))))
     (if (or (< idx 0) (>= idx (string-length text)))
         noob
         (string (string-ref text idx))))))

(define (runtime-functions ctx)
  (runstate-functions
   (exec-ctx-state ctx)))

(define (runtime-globals ctx)
  (runstate-globals
   (exec-ctx-state ctx)))

(define (runtime-stdout ctx)
  (runstate-stdout
   (exec-ctx-state ctx)))

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

(define (compile-target-get target)
  (match target
    [(or (expr-ident _) (expr-srs _))
     (define name-proc (compile-target-name target))
     (lambda (e ctx)
       (env-ref e (name-proc e ctx)))]
    [(expr-slot object slot)
     (define object-proc (compile-expr object))
     (define slot-name-proc (compile-slot-name slot))
     (lambda (e ctx)
       (define obj (object-proc e ctx))
       (unless (lol-object? obj)
         (error 'run-program "slot lookup requires BUKKIT, got ~e" obj))
       (send obj get-slot (slot-name-proc e ctx) noob))]
    [_ (raise-unsupported target)]))

(define (compile-target-set target #:define-missing? [define-missing? #t])
  (match target
    [(or (expr-ident _) (expr-srs _))
     (define name-proc (compile-target-name target))
     (lambda (e value ctx)
       (define name (name-proc e ctx))
       (cond
         [(env-lookup-box e name)
          => (lambda (b)
               (set-box! b value))]
         [define-missing?
          (env-define! e name value)]
         [else
          (error 'run-program "unknown identifier: ~a" name)]))]
    [(expr-slot object slot)
     (define object-proc (compile-expr object))
     (define slot-name-proc (compile-slot-name slot))
     (lambda (e value ctx)
       (define obj (object-proc e ctx))
       (unless (lol-object? obj)
         (error 'run-program "slot assignment requires BUKKIT, got ~e" obj))
       (send obj set-slot! (slot-name-proc e ctx) value))]
    [_ (raise-unsupported target)]))

(define (compile-declare-init init-expr)
  (cond
    [(not init-expr)
     (lambda (_e _ctx) noob)]
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

(define (maybe-init-loop-counter! e update-var)
  (when update-var
    (unless (env-lookup-box e update-var)
      (env-define! e update-var 0))))

(define (apply-loop-update! e update-var update-op)
  (when (and update-var update-op)
    (define current
      (cond
        [(env-lookup-box e update-var) => unbox]
        [else 0]))
    (define current-num (coerce-number 'LOOP current))
    (define delta
      (if (string=? update-op "UPPIN") 1 -1))
    (define updated (+ current-num delta))
    (env-set-or-define! e update-var updated)
    (set-it! e updated)))

(define (expand-format-placeholders e text)
  (define out (open-output-string))
  (define pattern #px":\\{([^\\}]*)\\}")
  (let loop ([start 0])
    (define m (regexp-match-positions pattern text start))
    (cond
      [(not m)
       (display (substring text start) out)
       (get-output-string out)]
      [else
       (define whole (car m))
       (define name-pos (cadr m))
       (define match-start (car whole))
       (define match-end (cdr whole))
       (define raw-name (substring text (car name-pos) (cdr name-pos)))
       (define name (string-trim raw-name))
       (when (string=? name "")
         (error 'run-program "empty :{...} placeholder in YARN literal"))
       (display (substring text start match-start) out)
       (display (lol-string (env-ref e name)) out)
       (loop match-end)])))

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

    [(expr-ident name)
     (lambda (e _ctx) (env-ref e name))]

    [(expr-srs inner)
     (define inner-proc (compile-expr inner))
     (lambda (e ctx) (inner-proc e ctx))]

    [(expr-binary op left right)
     (define left-proc (compile-expr left))
     (define right-proc (compile-expr right))
     (define op-fn
       (case op
         [("SUM OF") (lambda (lv rv) (+ (coerce-number 'SUM lv) (coerce-number 'SUM rv)))]
         [("DIFF OF") (lambda (lv rv) (- (coerce-number 'DIFF lv) (coerce-number 'DIFF rv)))]
         [("PRODUKT OF") (lambda (lv rv) (* (coerce-number 'PRODUKT lv) (coerce-number 'PRODUKT rv)))]
         [("QUOSHUNT OF") (lambda (lv rv) (/ (coerce-number 'QUOSHUNT lv) (coerce-number 'QUOSHUNT rv)))]
         [("MOD OF")
          (lambda (lv rv)
            (remainder (inexact->exact (truncate (coerce-number 'MOD lv)))
                       (inexact->exact (truncate (coerce-number 'MOD rv)))))]
         [("BIGGR OF") (lambda (lv rv) (max (coerce-number 'BIGGR lv) (coerce-number 'BIGGR rv)))]
         [("SMALLR OF") (lambda (lv rv) (min (coerce-number 'SMALLR lv) (coerce-number 'SMALLR rv)))]
         [("BOTH OF") (lambda (lv rv) (and (lol-truthy? lv) (lol-truthy? rv)))]
         [("EITHER OF") (lambda (lv rv) (or (lol-truthy? lv) (lol-truthy? rv)))]
         [("WON OF")
          (lambda (lv rv)
            (define lb (lol-truthy? lv))
            (define rb (lol-truthy? rv))
            (or (and lb (not rb))
                (and (not lb) rb)))]
         [("BOTH SAEM") (lambda (lv rv) (equal? lv rv))]
         [("DIFFRINT") (lambda (lv rv) (not (equal? lv rv)))]
         [else (raise-unsupported-op 'binary op expr)]))
     (lambda (e ctx)
       (op-fn (left-proc e ctx) (right-proc e ctx)))]

    [(expr-unary op arg)
     (define arg-proc (compile-expr arg))
     (define op-fn
       (case op
         [("NOT") (lambda (v) (not (lol-truthy? v)))]
         [else (raise-unsupported-op 'unary op expr)]))
     (lambda (e ctx)
       (op-fn (arg-proc e ctx)))]

    [(expr-variadic op args)
     (define arg-procs (map compile-expr args))
     (case op
       [("SMOOSH")
        (lambda (e ctx)
          (apply string-append
                 (map (lambda (a) (lol-string (a e ctx))) arg-procs)))]
       [("ALL OF")
        (lambda (e ctx)
          (andmap (lambda (a) (lol-truthy? (a e ctx))) arg-procs))]
       [("ANY OF")
        (lambda (e ctx)
          (ormap (lambda (a) (lol-truthy? (a e ctx))) arg-procs))]
       [else (raise-unsupported-op 'variadic op expr)])]

    [(expr-call name args)
     (define arg-procs (map compile-expr args))
     (lambda (e ctx)
       (define fn
         (hash-ref (runtime-functions ctx) name #f))
       (unless (procedure? fn)
         (error 'run-program "unknown function: ~a" name))
       (fn e
           (map (lambda (a) (a e ctx)) arg-procs)
           ctx))]

    [(expr-method-call receiver name args)
     (define recv-proc (compile-expr receiver))
     (define arg-procs (map compile-expr args))
     (lambda (e ctx)
       (define obj (recv-proc e ctx))
       (unless (lol-object? obj)
         (error 'run-program "method call requires BUKKIT receiver, got ~e" obj))
       (define arg-values
         (map (lambda (a) (a e ctx)) arg-procs))
       (send obj
             invoke-method
             name
             arg-values
             ctx
             (lambda ()
               (define fallback
                 (hash-ref (runtime-functions ctx) name #f))
               (if (procedure? fallback)
                   (fallback e arg-values ctx)
                   (error 'run-program "unknown method: ~a" name)))))]

    [(expr-cast inner type-name)
     (define inner-proc (compile-expr inner))
     (lambda (e ctx)
       (cast-value 'MAEK (inner-proc e ctx) type-name))]

    [(expr-slot object slot)
     (define object-proc (compile-expr object))
     (define slot-name-proc (compile-slot-name slot))
     (lambda (e ctx)
       (define obj (object-proc e ctx))
       (unless (lol-object? obj)
         (error 'run-program "slot lookup requires BUKKIT, got ~e" obj))
       (send obj get-slot (slot-name-proc e ctx) noob))]

    [_ (raise-unsupported expr)]))

(define (compile-block statements)
  (define stmt-procs
    (map compile-stmt statements))
  (lambda (e ctx)
    (let loop ([remaining stmt-procs])
      (cond
        [(null? remaining) ctrl-normal]
        [else
         (define control ((car remaining) e ctx))
         (if (control-normal? control)
             (loop (cdr remaining))
             control)]))))

(define (compile-stmt stmt)
  (match stmt
    [(stmt-declare target init)
     (define name-proc (compile-target-name target))
     (define init-proc (compile-declare-init init))
     (lambda (e ctx)
       (define value (init-proc e ctx))
       (env-define! e (name-proc e ctx) value)
       (set-it! e value)
       ctrl-normal)]

    [(stmt-assign target expr)
     (define target-set-proc
       (compile-target-set target #:define-missing? #t))
     (define expr-proc (compile-expr expr))
     (lambda (e ctx)
       (define value (expr-proc e ctx))
       (target-set-proc e value ctx)
       (set-it! e value)
       ctrl-normal)]

    [(stmt-cast target type-name)
     (define target-get-proc (compile-target-get target))
     (define target-set-proc
       (compile-target-set target #:define-missing? #f))
     (lambda (e ctx)
       (define value
         (cast-value 'IS-NOW-A
                     (target-get-proc e ctx)
                     type-name))
       (target-set-proc e value ctx)
       (set-it! e value)
       ctrl-normal)]

    [(stmt-input target)
     (define target-set-proc
       (compile-target-set target #:define-missing? #t))
     (lambda (e ctx)
       (define line (read-line (current-input-port) 'any))
       (define value
         (if (eof-object? line) noob line))
       (target-set-proc e value ctx)
       (set-it! e value)
       ctrl-normal)]

    [(stmt-slot-set object slot expr)
     (define object-proc (compile-expr object))
     (define slot-name-proc (compile-slot-name slot))
     (define expr-proc (compile-declare-init expr))
     (lambda (e ctx)
       (define obj (object-proc e ctx))
       (unless (lol-object? obj)
         (error 'run-program "slot assignment requires BUKKIT, got ~e" obj))
       (define value (expr-proc e ctx))
       (send obj set-slot! (slot-name-proc e ctx) value)
       (set-it! e value)
       ctrl-normal)]

    [(stmt-visible exprs suppress-newline?)
     (define expr-procs (map compile-expr exprs))
     (lambda (e ctx)
       (define values
         (map (lambda (ep) (ep e ctx)) expr-procs))
       (for ([v (in-list values)])
         (display (lol-string v) (runtime-stdout ctx)))
       (unless suppress-newline?
         (newline (runtime-stdout ctx)))
       (when (pair? values)
         (set-it! e (last values)))
       ctrl-normal)]

    [(stmt-if condition then-branch mebbe-branches else-branch)
     (define cond-proc (compile-expr condition))
     (define then-proc (compile-block then-branch))
     (define mebbe-procs
       (for/list ([mb (in-list mebbe-branches)])
         (cons (compile-expr (mebbe-branch-condition mb))
               (compile-block (mebbe-branch-body mb)))))
     (define else-proc (compile-block else-branch))
     (lambda (e ctx)
       (cond
         [(lol-truthy? (cond-proc e ctx))
          (then-proc (extend-env e) ctx)]
         [else
          (let mebbe-loop ([remaining mebbe-procs])
            (cond
              [(null? remaining)
               (else-proc (extend-env e) ctx)]
              [else
               (define mb (car remaining))
               (if (lol-truthy? ((car mb) e ctx))
                   ((cdr mb) (extend-env e) ctx)
                   (mebbe-loop (cdr remaining)))]))]))]

    [(stmt-switch subject cases default)
     (define subject-proc (compile-expr subject))
     (define case-procs
       (for/list ([c (in-list cases)])
         (cons (compile-expr (switch-case-match c))
               (compile-block (switch-case-body c)))))
     (define default-proc (compile-block default))
     (lambda (e ctx)
       (define subject-value (subject-proc e ctx))
       (define first-match
         (let find-first ([remaining case-procs] [idx 0])
           (cond
             [(null? remaining) #f]
             [else
              (define c (car remaining))
              (if (equal? subject-value ((car c) e ctx))
                  idx
                  (find-first (cdr remaining) (+ idx 1)))])))
       (define switch-ctx
         (ctx-derive ctx #:allow-break? #t))
       (if (number? first-match)
           (let run-cases ([remaining (drop case-procs first-match)])
             (cond
               [(null? remaining) ctrl-normal]
               [else
                (define control
                  ((cdr (car remaining)) (extend-env e) switch-ctx))
                (cond
                  [(control-normal? control)
                   (run-cases (cdr remaining))]
                  [(ctrl-break? control)
                   ctrl-normal]
                  [else
                   control])]))
           (let ([control (default-proc (extend-env e) switch-ctx)])
             (if (ctrl-break? control)
                 ctrl-normal
                 control))))]

    [(stmt-loop _label update-var update-op cond-kind cond-expr body)
     (define cond-proc
       (if cond-expr
           (compile-expr cond-expr)
           #f))
     (define body-proc (compile-block body))
     (lambda (e ctx)
       (define loop-ctx
         (ctx-derive ctx #:allow-break? #t))
       (maybe-init-loop-counter! e update-var)
       (let loop ()
         (if (loop-continue? e cond-kind cond-proc loop-ctx)
             (let ([control (body-proc (extend-env e) loop-ctx)])
               (cond
                 [(control-normal? control)
                  (apply-loop-update! e update-var update-op)
                  (loop)]
                 [(ctrl-break? control)
                  ctrl-normal]
                 [else
                  control]))
             ctrl-normal)))]

    [(stmt-function-def name params body)
     (define body-proc (compile-block body))
     (lambda (e ctx)
       (define def-env e)
       (define method-lexical-parent
         (if (exec-ctx-def-object ctx)
             (env-parent def-env)
             def-env))
       (define (make-global-fn)
         (lambda (_caller-env arg-values caller-ctx)
           (unless (= (length params) (length arg-values))
             (error 'run-program
                    "function ~a expected ~a args, got ~a"
                    name
                    (length params)
                    (length arg-values)))
           (define call-env (extend-env def-env))
           (for ([param (in-list params)]
                 [arg (in-list arg-values)])
             (env-define! call-env param arg))
           (env-define! call-env "IT" noob)
           (define fn-ctx
             (ctx-derive caller-ctx
                         #:allow-return? #t
                         #:allow-break? #f
                         #:object-name #f
                         #:def-object #f))
           (define control
             (body-proc call-env fn-ctx))
           (cond
             [(ctrl-return? control)
              (ctrl-return-value control)]
             [(control-normal? control)
              noob]
             [else
              (error 'run-program "internal control escape in function ~a" name)])))
       (define (make-method-fn)
         (lambda (receiver arg-values caller-ctx)
           (unless (= (length params) (length arg-values))
             (error 'run-program
                    "method ~a expected ~a args, got ~a"
                    name
                    (length params)
                    (length arg-values)))
           (define receiver-env
             (env-with-table (send receiver slot-table)
                             method-lexical-parent))
           (define call-env (extend-env receiver-env))
           (for ([param (in-list params)]
                 [arg (in-list arg-values)])
             (env-define! call-env param arg))
           (env-define! call-env "IT" noob)
           (define fn-ctx
             (ctx-derive caller-ctx
                         #:allow-return? #t
                         #:allow-break? #f
                         #:object-name #f
                         #:def-object #f))
           (define control
             (body-proc call-env fn-ctx))
           (cond
             [(ctrl-return? control)
              (ctrl-return-value control)]
             [(control-normal? control)
              noob]
             [else
              (error 'run-program "internal control escape in method ~a" name)])))
       (cond
         [(exec-ctx-def-object ctx)
          (send (exec-ctx-def-object ctx) define-method! name (make-method-fn))]
         [(eq? e (runtime-globals ctx))
          (hash-set! (runtime-functions ctx) name (make-global-fn))]
         [else
          (env-set-or-define! e name (make-global-fn))])
       ctrl-normal)]

    [(stmt-object-def name parent body)
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
       (define control
         (body-proc (env-with-table (send obj slot-table) e)
                    object-ctx))
       (when (send obj has-slot? "IT")
         (send obj remove-slot! "IT"))
       (if (control-normal? control)
           (begin
             (env-set-or-define! e name obj)
             (set-it! e obj)
             ctrl-normal)
           control))]

    [(stmt-return expr)
     (define expr-proc (compile-expr expr))
     (lambda (e ctx)
       (define value (expr-proc e ctx))
       (set-it! e value)
       (cond
         [(exec-ctx-allow-return? ctx)
          (ctrl-return value)]
         [(exec-ctx-object-name ctx)
          (error 'run-program
                 "FOUND YR used inside object definition ~a"
                 (exec-ctx-object-name ctx))]
         [else
          (error 'run-program "FOUND YR used outside function")]))]

    [(stmt-break)
     (lambda (_e ctx)
       (cond
         [(exec-ctx-allow-break? ctx)
          (ctrl-break)]
         [(exec-ctx-object-name ctx)
          (error 'run-program
                 "GTFO used inside object definition ~a"
                 (exec-ctx-object-name ctx))]
         [else
          (error 'run-program "GTFO used outside switch/loop")]))]

    [(stmt-import _library)
     (lambda (_e _ctx)
       ctrl-normal)]

    [(stmt-expr expr)
     (define expr-proc (compile-expr expr))
     (lambda (e ctx)
       (define value (expr-proc e ctx))
       (set-it! e value)
       ctrl-normal)]

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
      (define control
        (program-proc globals root-ctx))
      (unless (control-normal? control)
        (error 'run-program "internal control escape at program top-level"))
      (hash 'status 'ok
            'phase (runstate-phase st)
            'stdout (get-output-string stdout)
            'last-value (env-ref globals "IT")))))

(define (execute-program parsed phase)
  ((compile-program parsed phase)))
