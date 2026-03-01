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

(define current-runstate (make-parameter #f))
(define current-return-k (make-parameter #f))
(define current-break-k (make-parameter #f))
(define current-object-name (make-parameter #f))
(define current-def-object (make-parameter #f))
(define current-phase (make-parameter 'unknown))

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
  (let loop ([cur e])
    (and cur
         (cond
           [(hash-ref (env-table cur) name #f)
            => (lambda (maybe-box)
                 (if (box? maybe-box)
                     maybe-box
                     (loop (env-parent cur))))]
           [else
            (loop (env-parent cur))]))))

(define (env-define! e name value)
  (hash-set! (env-table e) name (box value)))

(define (env-ref e name)
  (define b (env-lookup-box e name))
  (if b
      (unbox b)
      (error 'run-program "unknown identifier: ~a" name)))

(define (env-set! e name value)
  (define b (env-lookup-box e name))
  (if b
      (set-box! b value)
      (error 'run-program "unknown identifier: ~a" name)))

(define (env-set-or-define! e name value)
  (define b (env-lookup-box e name))
  (if b
      (set-box! b value)
      (env-define! e name value)))

(define (set-it! e value)
  (define maybe-it (env-lookup-box e "IT"))
  (if maybe-it
      (set-box! maybe-it value)
      (env-define! e "IT" value)))

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
      (define maybe-box
        (hash-ref slots name #f))
      (if (box? maybe-box)
          (unbox maybe-box)
          default))

    (define/public (set-slot! name value)
      (define maybe-box
        (hash-ref slots name #f))
      (if (box? maybe-box)
          (set-box! maybe-box value)
          (hash-set! slots name (box value))))

    (define/public (remove-slot! name)
      (hash-remove! slots name))

    (define/public (define-method! name fn)
      (hash-set! methods name fn))

    (define/public (get-method name [default #f])
      (hash-ref methods name default))

    (define/public (invoke-method name arg-values fallback-thunk)
      (define method
        (hash-ref methods name #f))
      (cond
        [(procedure? method) (method this arg-values)]
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
  (cond
    [(number? v) v]
    [else (error who "expected numeric operand, got ~e" v)]))

(define (coerce-cast-number who v)
  (cond
    [(number? v) v]
    [(boolean? v) (if v 1 0)]
    [(eq? v noob) 0]
    [(string? v)
     (define n (string->number (string-trim v)))
     (if n
         n
         (error who "cannot cast YARN to numeric value: ~e" v))]
    [else
     (error who "cannot cast ~e to numeric value" v)]))

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

(define (runtime-functions)
  (define st (current-runstate))
  (if st
      (runstate-functions st)
      (error 'run-program "runtime unavailable")))

(define (runtime-globals)
  (define st (current-runstate))
  (if st
      (runstate-globals st)
      (error 'run-program "runtime unavailable")))

(define (runtime-stdout)
  (define st (current-runstate))
  (if st
      (runstate-stdout st)
      (error 'run-program "runtime unavailable")))

(define (compile-slot-name slot)
  (match slot
    [(expr-ident name) (lambda (_e) name)]
    [(expr-srs inner)
     (define inner-proc (compile-expr inner))
     (lambda (e)
       (identifier-text
        "SRS slot must evaluate to identifier text"
        (inner-proc e)))]
    [_ (raise-unsupported slot)]))

(define (compile-target-name target)
  (match target
    [(expr-ident name) (lambda (_e) name)]
    [(expr-srs inner)
     (define inner-proc (compile-expr inner))
     (lambda (e)
       (identifier-text
        "SRS target must evaluate to identifier text"
        (inner-proc e)))]
    [_ (raise-unsupported target)]))

(define (compile-target-get target)
  (match target
    [(or (expr-ident _) (expr-srs _))
     (define name-proc (compile-target-name target))
     (lambda (e)
       (env-ref e (name-proc e)))]
    [(expr-slot object slot)
     (define object-proc (compile-expr object))
     (define slot-name-proc (compile-slot-name slot))
     (lambda (e)
       (define obj (object-proc e))
       (unless (lol-object? obj)
         (error 'run-program "slot lookup requires BUKKIT, got ~e" obj))
       (send obj get-slot (slot-name-proc e) noob))]
    [_ (raise-unsupported target)]))

(define (compile-target-set target #:define-missing? [define-missing? #t])
  (match target
    [(or (expr-ident _) (expr-srs _))
     (define name-proc (compile-target-name target))
     (lambda (e value)
       (define name (name-proc e))
       (define maybe-box (env-lookup-box e name))
       (cond
         [maybe-box
          (set-box! maybe-box value)]
         [define-missing?
          (env-define! e name value)]
         [else
          (error 'run-program "unknown identifier: ~a" name)]))]
    [(expr-slot object slot)
     (define object-proc (compile-expr object))
     (define slot-name-proc (compile-slot-name slot))
     (lambda (e value)
       (define obj (object-proc e))
       (unless (lol-object? obj)
         (error 'run-program "slot assignment requires BUKKIT, got ~e" obj))
       (send obj set-slot! (slot-name-proc e) value))]
    [_ (raise-unsupported target)]))

(define (compile-declare-init init-expr)
  (cond
    [(not init-expr)
     (lambda (_e) noob)]
    [(expr-ident? init-expr)
     (define type-name (expr-ident-name init-expr))
     (define-values (known? default-value)
       (type-default-value type-name))
     (if known?
         (if (string-ci=? type-name "BUKKIT")
             (lambda (_e) (new lol-object%))
             (lambda (_e) default-value))
         (compile-expr init-expr))]
    [else
     (compile-expr init-expr)]))

(define (loop-continue? e cond-kind cond-proc)
  (cond
    [(not cond-kind) #t]
    [else
     (define cond-value (lol-truthy? (cond-proc e)))
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
      (if (env-lookup-box e update-var)
          (env-ref e update-var)
          0))
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
     (lambda (_e)
       (define parsed-number (string->number text))
       (if parsed-number
           parsed-number
           (error 'run-program "invalid number literal: ~a" text)))]

    [(expr-string text)
     (lambda (e) (expand-format-placeholders e text))]

    [(expr-literal value)
     (lambda (_e)
       (if (eq? value 'NOOB) noob value))]

    [(expr-ident name)
     (lambda (e) (env-ref e name))]

    [(expr-srs inner)
     (define inner-proc (compile-expr inner))
     (lambda (e) (inner-proc e))]

    [(expr-binary op left right)
     (define left-proc (compile-expr left))
     (define right-proc (compile-expr right))
     (define op-fn
       (case op
         [("SUM OF") (lambda (lv rv) (+ (coerce-number 'SUM lv) (coerce-number 'SUM rv)))]
         [("DIFF OF") (lambda (lv rv) (- (coerce-number 'DIFF lv) (coerce-number 'DIFF rv)))]
         [("PRODUKT OF") (lambda (lv rv) (* (coerce-number 'PRODUKT lv) (coerce-number 'PRODUKT rv)))]
         [("QUOSHUNT OF") (lambda (lv rv) (/ (coerce-number 'QUOSHUNT lv) (coerce-number 'QUOSHUNT rv)))]
         [("MOD OF") (lambda (lv rv) (remainder (coerce-number 'MOD lv) (coerce-number 'MOD rv)))]
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
     (lambda (e)
       (op-fn (left-proc e) (right-proc e)))]

    [(expr-unary op arg)
     (define arg-proc (compile-expr arg))
     (define op-fn
       (case op
         [("NOT") (lambda (v) (not (lol-truthy? v)))]
         [else (raise-unsupported-op 'unary op expr)]))
     (lambda (e)
       (op-fn (arg-proc e)))]

    [(expr-variadic op args)
     (define arg-procs (map compile-expr args))
     (case op
       [("SMOOSH")
        (lambda (e)
          (apply string-append
                 (map (lambda (a) (lol-string (a e))) arg-procs)))]
       [("ALL OF")
        (lambda (e)
          (andmap (lambda (a) (lol-truthy? (a e))) arg-procs))]
       [("ANY OF")
        (lambda (e)
          (ormap (lambda (a) (lol-truthy? (a e))) arg-procs))]
       [else (raise-unsupported-op 'variadic op expr)])]

    [(expr-call name args)
     (define arg-procs (map compile-expr args))
     (lambda (e)
       (define fn
         (hash-ref (runtime-functions) name #f))
       (unless (procedure? fn)
         (error 'run-program "unknown function: ~a" name))
       (fn e (map (lambda (a) (a e)) arg-procs)))]

    [(expr-method-call receiver name args)
     (define recv-proc (compile-expr receiver))
     (define arg-procs (map compile-expr args))
     (lambda (e)
       (define obj (recv-proc e))
       (unless (lol-object? obj)
         (error 'run-program "method call requires BUKKIT receiver, got ~e" obj))
       (define arg-values
         (map (lambda (a) (a e)) arg-procs))
       (send obj
             invoke-method
             name
             arg-values
             (lambda ()
               (define fallback
                 (hash-ref (runtime-functions) name #f))
               (if (procedure? fallback)
                   (fallback e arg-values)
                   (error 'run-program "unknown method: ~a" name)))))]

    [(expr-cast inner type-name)
     (define inner-proc (compile-expr inner))
     (lambda (e)
       (cast-value 'MAEK (inner-proc e) type-name))]

    [(expr-slot object slot)
     (define object-proc (compile-expr object))
     (define slot-name-proc (compile-slot-name slot))
     (lambda (e)
       (define obj (object-proc e))
       (unless (lol-object? obj)
         (error 'run-program "slot lookup requires BUKKIT, got ~e" obj))
       (send obj get-slot (slot-name-proc e) noob))]

    [_ (raise-unsupported expr)]))

(define (compile-block statements)
  (define stmt-procs
    (map compile-stmt statements))
  (lambda (e)
    (for ([stmt-proc (in-list stmt-procs)])
      (stmt-proc e))))

(define (compile-stmt stmt)
  (match stmt
    [(stmt-declare target init)
     (define name-proc (compile-target-name target))
     (define init-proc (compile-declare-init init))
     (lambda (e)
       (define value (init-proc e))
       (env-define! e (name-proc e) value)
       (set-it! e value))]

    [(stmt-assign target expr)
     (define target-set-proc
       (compile-target-set target #:define-missing? #t))
     (define expr-proc (compile-expr expr))
     (lambda (e)
       (define value (expr-proc e))
       (target-set-proc e value)
       (set-it! e value))]

    [(stmt-cast target type-name)
     (define target-get-proc (compile-target-get target))
     (define target-set-proc
       (compile-target-set target #:define-missing? #f))
     (lambda (e)
       (define value
         (cast-value 'IS-NOW-A
                     (target-get-proc e)
                     type-name))
       (target-set-proc e value)
       (set-it! e value))]

    [(stmt-input target)
     (define target-set-proc
       (compile-target-set target #:define-missing? #t))
     (lambda (e)
       (define line (read-line (current-input-port) 'any))
       (define value
         (if (eof-object? line) noob line))
       (target-set-proc e value)
       (set-it! e value))]

    [(stmt-slot-set object slot expr)
     (define object-proc (compile-expr object))
     (define slot-name-proc (compile-slot-name slot))
     (define expr-proc (compile-expr expr))
     (lambda (e)
       (define obj (object-proc e))
       (unless (lol-object? obj)
         (error 'run-program "slot assignment requires BUKKIT, got ~e" obj))
       (define value (expr-proc e))
       (send obj set-slot! (slot-name-proc e) value)
       (set-it! e value))]

    [(stmt-visible exprs suppress-newline?)
     (define expr-procs (map compile-expr exprs))
     (lambda (e)
       (define values
         (map (lambda (ep) (ep e)) expr-procs))
       (for ([v (in-list values)])
         (display (lol-string v) (runtime-stdout)))
       (unless suppress-newline?
         (newline (runtime-stdout)))
       (when (pair? values)
         (set-it! e (last values))))]

    [(stmt-if condition then-branch mebbe-branches else-branch)
     (define cond-proc (compile-expr condition))
     (define then-proc (compile-block then-branch))
     (define mebbe-procs
       (for/list ([mb (in-list mebbe-branches)])
         (cons (compile-expr (mebbe-branch-condition mb))
               (compile-block (mebbe-branch-body mb)))))
     (define else-proc (compile-block else-branch))
     (lambda (e)
       (cond
         [(lol-truthy? (cond-proc e))
          (then-proc (extend-env e))]
         [else
          (let mebbe-loop ([remaining mebbe-procs])
            (cond
              [(null? remaining)
               (else-proc (extend-env e))]
              [else
               (define mb (car remaining))
               (if (lol-truthy? ((car mb) e))
                   ((cdr mb) (extend-env e))
                   (mebbe-loop (cdr remaining)))]))]))]

    [(stmt-switch subject cases default)
     (define subject-proc (compile-expr subject))
     (define case-procs
       (for/list ([c (in-list cases)])
         (cons (compile-expr (switch-case-match c))
               (compile-block (switch-case-body c)))))
     (define default-proc (compile-block default))
     (lambda (e)
       (define subject-value (subject-proc e))
       (define first-match
         (let find-first ([remaining case-procs] [idx 0])
           (cond
             [(null? remaining) #f]
             [else
              (define c (car remaining))
              (if (equal? subject-value ((car c) e))
                  idx
                  (find-first (cdr remaining) (+ idx 1)))])))
       (let/ec break-k
         (parameterize ([current-break-k break-k])
           (if first-match
               (for ([c (in-list (drop case-procs first-match))])
                 ((cdr c) (extend-env e)))
               (default-proc (extend-env e))))))]

    [(stmt-loop _label update-var update-op cond-kind cond-expr body)
     (define cond-proc
       (if cond-expr
           (compile-expr cond-expr)
           #f))
     (define body-proc (compile-block body))
     (lambda (e)
       (maybe-init-loop-counter! e update-var)
       (let/ec break-k
         (parameterize ([current-break-k break-k])
           (let loop ()
             (when (loop-continue? e cond-kind cond-proc)
               (body-proc (extend-env e))
               (apply-loop-update! e update-var update-op)
               (loop))))))]

    [(stmt-function-def name params body)
     (define body-proc (compile-block body))
     (lambda (e)
       (define def-env e)
       (define method-lexical-parent
         (if (current-def-object)
             (env-parent def-env)
             def-env))
       (define (make-global-fn)
         (lambda (_caller-env arg-values)
           (unless (= (length params) (length arg-values))
             (error 'run-program
                    "function ~a expected ~a args, got ~a"
                    name
                    (length params)
                    (length arg-values)))
           (let/ec return-k
             (parameterize ([current-return-k return-k]
                            [current-break-k #f]
                            [current-object-name #f]
                            [current-def-object #f])
               (define call-env (extend-env def-env))
               (for ([param (in-list params)]
                     [arg (in-list arg-values)])
                 (env-define! call-env param arg))
               (env-define! call-env "IT" noob)
               (body-proc call-env)
               noob))))
       (define (make-method-fn)
         (lambda (receiver arg-values)
           (unless (= (length params) (length arg-values))
             (error 'run-program
                    "method ~a expected ~a args, got ~a"
                    name
                    (length params)
                    (length arg-values)))
           (let/ec return-k
             (parameterize ([current-return-k return-k]
                            [current-break-k #f]
                            [current-object-name #f]
                            [current-def-object #f])
               (define receiver-env
                 (env-with-table (send receiver slot-table)
                                 method-lexical-parent))
               (define call-env (extend-env receiver-env))
               (for ([param (in-list params)]
                     [arg (in-list arg-values)])
                 (env-define! call-env param arg))
               (env-define! call-env "IT" noob)
               (body-proc call-env)
               noob))))
       (cond
         [(current-def-object)
          (send (current-def-object) define-method! name (make-method-fn))]
         [(eq? e (runtime-globals))
          (hash-set! (runtime-functions) name (make-global-fn))]
         [else
          (env-set-or-define! e name (make-global-fn))]))]

    [(stmt-object-def name parent body)
     (define body-proc (compile-block body))
     (lambda (e)
       (define obj
         (if parent
             (let ([p (env-ref e parent)])
               (unless (lol-object? p)
                 (error 'run-program "object parent must be BUKKIT, got ~e" p))
               (send p clone))
             (new lol-object%)))
       (send obj set-slot! "IT" noob)
       (dynamic-wind
         void
         (lambda ()
           (parameterize ([current-def-object obj]
                          [current-object-name name])
             (body-proc (env-with-table (send obj slot-table) e))))
         (lambda ()
           (when (send obj has-slot? "IT")
             (send obj remove-slot! "IT"))))
       (env-set-or-define! e name obj)
       (set-it! e obj))]

    [(stmt-return expr)
     (define expr-proc (compile-expr expr))
     (lambda (e)
       (define value (expr-proc e))
       (set-it! e value)
       (define ret-k (current-return-k))
       (cond
         [ret-k
          (ret-k value)]
         [(current-object-name)
          (error 'run-program
                 "FOUND YR used inside object definition ~a"
                 (current-object-name))]
         [else
          (error 'run-program "FOUND YR used outside function")]))]

    [(stmt-break)
     (lambda (_e)
       (define brk-k (current-break-k))
       (cond
         [brk-k
          (brk-k (void))]
         [(current-object-name)
          (error 'run-program
                 "GTFO used inside object definition ~a"
                 (current-object-name))]
         [else
          (error 'run-program "GTFO used outside switch/loop")]))]

    [(stmt-expr expr)
     (define expr-proc (compile-expr expr))
     (lambda (e)
       (define value (expr-proc e))
       (set-it! e value))]

    [_ (raise-unsupported stmt)]))

(define (compile-program parsed)
  (unless (program? parsed)
    (raise-argument-error 'compile-program "program?" parsed))
  (lambda ()
    (define globals (make-root-env))
    (define functions (make-hash))
    (define stdout (open-output-string))
    (env-define! globals "IT" noob)
    (define st
      (runstate globals functions stdout (current-phase)))
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
      (parameterize ([current-runstate st]
                     [current-return-k #f]
                     [current-break-k #f]
                     [current-object-name #f]
                     [current-def-object #f])
        (define program-proc
          (compile-block (program-statements parsed)))
        (program-proc globals)
        (hash 'status 'ok
              'phase (runstate-phase st)
              'stdout (get-output-string stdout)
              'last-value (env-ref globals "IT"))))))

(define (execute-program parsed phase)
  (parameterize ([current-phase phase])
    ((compile-program parsed))))
