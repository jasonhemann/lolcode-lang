#lang racket/base

(require racket/list
         racket/match
         racket/string
         "ast.rkt")

(provide execute-program)

(define noob 'NOOB)

(struct exn:fail:unsupported exn:fail (where) #:transparent)
(struct ctrl-normal () #:transparent)
(struct ctrl-return (value) #:transparent)
(struct ctrl-break () #:transparent)
(struct runtime-function (name args body) #:transparent)

(define normal-control (ctrl-normal))

(define (raise-unsupported where)
  (raise
   (exn:fail:unsupported
    (format "unsupported AST form: ~e" where)
    (current-continuation-marks)
    where)))

(define (lol-string v)
  (cond
    [(eq? v noob) "NOOB"]
    [(boolean? v) (if v "WIN" "FAIL")]
    [(number? v) (number->string v)]
    [(string? v) v]
    [(hash? v) "<BUKKIT>"]
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

(define (type-default type-name)
  (case (string-upcase type-name)
    [("NUMBR" "NUMBAR") (values #t 0)]
    [("YARN") (values #t "")]
    [("TROOF") (values #t #f)]
    [("BUKKIT") (values #t (make-hash))]
    [("NOOB") (values #t noob)]
    [else (values #f #f)]))

(define (resolve-ident-name env globals name)
  (cond
    [(hash-has-key? env name) (hash-ref env name)]
    [(hash-has-key? globals name) (hash-ref globals name)]
    [else (error 'run-program "unknown identifier: ~a" name)]))

(define (target-name env target eval-expr)
  (match target
    [(expr-ident name) name]
    [(expr-srs inner)
     (define dynamic (eval-expr env inner))
     (cond
       [(string? dynamic) dynamic]
       [(symbol? dynamic) (symbol->string dynamic)]
       [else
        (error 'run-program
               "SRS target must evaluate to identifier text, got ~e"
               dynamic)])]
    [_ (raise-unsupported target)]))

(define (slot-name env slot eval-expr)
  (match slot
    [(expr-ident name) name]
    [(expr-srs inner)
     (define dynamic (eval-expr env inner))
     (cond
       [(string? dynamic) dynamic]
       [(symbol? dynamic) (symbol->string dynamic)]
       [else
        (error 'run-program
               "SRS slot must evaluate to identifier text, got ~e"
               dynamic)])]
    [_ (raise-unsupported slot)]))

(define (execute-program parsed phase)
  (define globals (make-hash))
  (define functions (make-hash))
  (define stdout (open-output-string))
  (hash-set! globals "IT" noob)

  (define (set-it! env v)
    (hash-set! env "IT" v))

  (define (call-function caller-env fn arg-values)
    (define name (runtime-function-name fn))
    (define params (runtime-function-args fn))
    (unless (= (length params) (length arg-values))
      (error 'run-program
             "function ~a expected ~a args, got ~a"
             name
             (length params)
             (length arg-values)))
    (define local-env (hash-copy caller-env))
    (for ([param (in-list params)]
          [arg (in-list arg-values)])
      (hash-set! local-env param arg))
    (hash-set! local-env "IT" noob)
    (define control (execute-statements local-env (runtime-function-body fn)))
    (cond
      [(ctrl-return? control) (ctrl-return-value control)]
      [(ctrl-break? control)
       (error 'run-program "GTFO used outside switch/loop in function ~a" name)]
      [else noob]))

  (define (eval-expr env expr)
    (match expr
      [(expr-number text)
       (define parsed-number (string->number text))
       (if parsed-number
           parsed-number
           (error 'run-program "invalid number literal: ~a" text))]
      [(expr-string text) text]
      [(expr-ident name) (resolve-ident-name env globals name)]
      [(expr-srs inner) (eval-expr env inner)]
      [(expr-binary op left right)
       (define lv (eval-expr env left))
       (define rv (eval-expr env right))
       (case op
         [("SUM OF") (+ (coerce-number 'SUM lv) (coerce-number 'SUM rv))]
         [("DIFF OF") (- (coerce-number 'DIFF lv) (coerce-number 'DIFF rv))]
         [("PRODUKT OF") (* (coerce-number 'PRODUKT lv) (coerce-number 'PRODUKT rv))]
         [("QUOSHUNT OF") (/ (coerce-number 'QUOSHUNT lv) (coerce-number 'QUOSHUNT rv))]
         [("MOD OF") (remainder (coerce-number 'MOD lv) (coerce-number 'MOD rv))]
         [("BIGGR OF") (max (coerce-number 'BIGGR lv) (coerce-number 'BIGGR rv))]
         [("SMALLR OF") (min (coerce-number 'SMALLR lv) (coerce-number 'SMALLR rv))]
         [("BOTH SAEM") (equal? lv rv)]
         [("DIFFRINT") (not (equal? lv rv))]
         [else (raise-unsupported expr)])]
      [(expr-variadic op args)
       (case op
         [("SMOOSH")
          (apply string-append (map (lambda (a) (lol-string (eval-expr env a))) args))]
         [else (raise-unsupported expr)])]
      [(expr-call name args)
       (define fn
         (hash-ref functions name #f))
       (unless fn
         (error 'run-program "unknown function: ~a" name))
       (call-function env fn (map (lambda (a) (eval-expr env a)) args))]
      [(expr-slot object slot)
       (define obj (eval-expr env object))
       (unless (hash? obj)
         (error 'run-program "slot lookup requires BUKKIT, got ~e" obj))
       (hash-ref obj (slot-name env slot eval-expr) noob)]
      [_ (raise-unsupported expr)]))

  (define (eval-declare-init env init)
    (cond
      [(not init) noob]
      [(expr-ident? init)
       (define-values (known? default-value)
         (type-default (expr-ident-name init)))
       (if known?
           default-value
           (eval-expr env init))]
      [else (eval-expr env init)]))

  (define (execute-statements env statements)
    (let loop ([remaining statements])
      (cond
        [(null? remaining) normal-control]
        [else
         (define control (execute-statement env (car remaining)))
         (if (ctrl-normal? control)
             (loop (cdr remaining))
             control)])))

  (define (find-first-matching-case env subject-value cases)
    (let loop ([remaining cases] [idx 0])
      (cond
        [(null? remaining) #f]
        [else
         (define c (car remaining))
         (if (equal? subject-value (eval-expr env (switch-case-match c)))
             idx
             (loop (cdr remaining) (+ idx 1)))])))

  (define (execute-case-sequence env cases)
    (let loop ([remaining cases])
      (cond
        [(null? remaining) normal-control]
        [else
         (define control (execute-statements env (switch-case-body (car remaining))))
         (cond
           [(ctrl-normal? control) (loop (cdr remaining))]
           [(ctrl-break? control) normal-control]
           [else control])])))

  (define (execute-statement env stmt)
    (match stmt
      [(stmt-declare target init)
       (define name (target-name env target eval-expr))
       (define value (eval-declare-init env init))
       (hash-set! env name value)
       (set-it! env value)
       normal-control]
      [(stmt-assign target expr)
       (define name (target-name env target eval-expr))
       (define value (eval-expr env expr))
       (hash-set! env name value)
       (set-it! env value)
       normal-control]
      [(stmt-slot-set object slot expr)
       (define obj (eval-expr env object))
       (unless (hash? obj)
         (error 'run-program "slot assignment requires BUKKIT, got ~e" obj))
       (define value (eval-expr env expr))
       (hash-set! obj (slot-name env slot eval-expr) value)
       (set-it! env value)
       normal-control]
      [(stmt-visible exprs suppress-newline?)
       (define values (map (lambda (e) (eval-expr env e)) exprs))
       (for ([v (in-list values)])
         (display (lol-string v) stdout))
       (unless suppress-newline?
         (newline stdout))
       (when (pair? values)
         (set-it! env (last values)))
       normal-control]
      [(stmt-if condition then-branch mebbe-branches else-branch)
       (if (lol-truthy? (eval-expr env condition))
           (execute-statements env then-branch)
           (let mebbe-loop ([remaining mebbe-branches])
             (cond
               [(null? remaining) (execute-statements env else-branch)]
               [else
                (define mb (car remaining))
                (if (lol-truthy? (eval-expr env (mebbe-branch-condition mb)))
                    (execute-statements env (mebbe-branch-body mb))
                    (mebbe-loop (cdr remaining)))])))]
      [(stmt-switch subject cases default)
       (define subject-value (eval-expr env subject))
       (define first-match (find-first-matching-case env subject-value cases))
       (if first-match
           (execute-case-sequence env (drop cases first-match))
           (let ([control (execute-statements env default)])
             (if (ctrl-break? control)
                 normal-control
                 control)))]
      [(stmt-function-def name args body)
       (hash-set! functions name (runtime-function name args body))
       normal-control]
      [(stmt-object-def name parent body)
       (define obj
         (if parent
             (let ([p (resolve-ident-name env globals parent)])
               (unless (hash? p)
                 (error 'run-program "object parent must be BUKKIT, got ~e" p))
               (hash-copy p))
             (make-hash)))
       (hash-set! obj "IT" noob)
       (define body-control (execute-statements obj body))
       (when (hash-has-key? obj "IT")
         (hash-remove! obj "IT"))
       (cond
         [(ctrl-normal? body-control) (void)]
         [(ctrl-return? body-control)
          (error 'run-program "FOUND YR used inside object definition ~a" name)]
         [(ctrl-break? body-control)
          (error 'run-program "GTFO used inside object definition ~a" name)]
         [else
          (error 'run-program
                 "invalid object body control transfer: ~e"
                 body-control)])
       (hash-set! env name obj)
       (set-it! env obj)
       normal-control]
      [(stmt-return expr)
       (define value (eval-expr env expr))
       (set-it! env value)
       (ctrl-return value)]
      [(stmt-break)
       (ctrl-break)]
      [(stmt-expr expr)
       (define value (eval-expr env expr))
       (set-it! env value)
       normal-control]
      [_ (raise-unsupported stmt)]))

  (with-handlers ([exn:fail:unsupported?
                   (lambda (e)
                     (hash 'status 'unsupported
                           'phase phase
                           'stdout (get-output-string stdout)
                           'last-value (hash-ref globals "IT")
                           'reason (exn-message e)
                           'where (exn:fail:unsupported-where e)))]
                  [exn:fail?
                   (lambda (e)
                     (hash 'status 'runtime-error
                           'phase phase
                           'stdout (get-output-string stdout)
                           'last-value (hash-ref globals "IT")
                           'error (exn-message e)))])
    (define terminal-control
      (execute-statements globals (program-statements parsed)))
    (cond
      [(ctrl-normal? terminal-control)
       (hash 'status 'ok
             'phase phase
             'stdout (get-output-string stdout)
             'last-value (hash-ref globals "IT"))]
      [(ctrl-return? terminal-control)
       (error 'run-program "FOUND YR used outside function")]
      [(ctrl-break? terminal-control)
       (error 'run-program "GTFO used outside switch/loop")]
      [else
       (error 'run-program "invalid control transfer state: ~e" terminal-control)])))
