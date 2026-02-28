#lang racket/base

(require racket/list
         racket/match
         racket/string
         "ast.rkt")

(provide execute-program)

(define noob 'NOOB)

(struct exn:fail:unsupported exn:fail (where) #:transparent)

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

(define (type-default name)
  (case (string-upcase name)
    [("NUMBR" "NUMBAR") 0]
    [("YARN") ""]
    [("TROOF") #f]
    [("BUKKIT") (make-hash)]
    [("NOOB") noob]
    [else #f]))

(define (resolve-ident-name env name)
  (if (hash-has-key? env name)
      (hash-ref env name)
      (error 'run-program "unknown identifier: ~a" name)))

(define (target-name env target eval-expr)
  (match target
    [(expr-ident name) name]
    [(expr-srs inner)
     (define dynamic (eval-expr inner))
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
     (define dynamic (eval-expr inner))
     (cond
       [(string? dynamic) dynamic]
       [(symbol? dynamic) (symbol->string dynamic)]
       [else
        (error 'run-program
               "SRS slot must evaluate to identifier text, got ~e"
               dynamic)])]
    [_ (raise-unsupported slot)]))

(define (execute-program parsed phase)
  (define env (make-hash))
  (define stdout (open-output-string))
  (hash-set! env "IT" noob)

  (define (set-it! v)
    (hash-set! env "IT" v))

  (define (eval-expr expr)
    (match expr
      [(expr-number text)
       (define parsed-number (string->number text))
       (if parsed-number
           parsed-number
           (error 'run-program "invalid number literal: ~a" text))]
      [(expr-string text) text]
      [(expr-ident name) (resolve-ident-name env name)]
      [(expr-srs inner) (eval-expr inner)]
      [(expr-binary op left right)
       (define lv (eval-expr left))
       (define rv (eval-expr right))
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
          (apply string-append (map (lambda (a) (lol-string (eval-expr a))) args))]
         [else (raise-unsupported expr)])]
      [(expr-slot object slot)
       (define obj (eval-expr object))
       (unless (hash? obj)
         (error 'run-program "slot lookup requires BUKKIT, got ~e" obj))
       (hash-ref obj (slot-name env slot eval-expr) noob)]
      [_ (raise-unsupported expr)]))

  (define (eval-declare-init init)
    (cond
      [(not init) noob]
      [(and (expr-ident? init)
            (type-default (expr-ident-name init)))
       => (lambda (v) v)]
      [else (eval-expr init)]))

  (define (execute-statements statements)
    (let loop ([remaining statements])
      (when (pair? remaining)
        (execute-statement (car remaining))
        (loop (cdr remaining)))))

  (define (execute-statement stmt)
    (match stmt
      [(stmt-declare target init)
       (define name (target-name env target eval-expr))
       (define value (eval-declare-init init))
       (hash-set! env name value)
       (set-it! value)]
      [(stmt-assign target expr)
       (define name (target-name env target eval-expr))
       (define value (eval-expr expr))
       (hash-set! env name value)
       (set-it! value)]
      [(stmt-slot-set object slot expr)
       (define obj (eval-expr object))
       (unless (hash? obj)
         (error 'run-program "slot assignment requires BUKKIT, got ~e" obj))
       (define value (eval-expr expr))
       (hash-set! obj (slot-name env slot eval-expr) value)
       (set-it! value)]
      [(stmt-visible exprs suppress-newline?)
       (define values (map eval-expr exprs))
       (for ([v (in-list values)])
         (display (lol-string v) stdout))
       (unless suppress-newline?
         (newline stdout))
       (when (pair? values)
         (set-it! (last values)))]
      [(stmt-if condition then-branch mebbe-branches else-branch)
       (define cv (eval-expr condition))
       (cond
         [(lol-truthy? cv) (execute-statements then-branch)]
         [else
          (let mebbe-loop ([remaining mebbe-branches])
            (if (null? remaining)
                (execute-statements else-branch)
                (let ([mb (car remaining)])
                  (if (lol-truthy? (eval-expr (mebbe-branch-condition mb)))
                      (execute-statements (mebbe-branch-body mb))
                      (mebbe-loop (cdr remaining))))))])]
      [_ (raise-unsupported stmt)]))

  (with-handlers ([exn:fail:unsupported?
                   (lambda (e)
                     (hash 'status 'unsupported
                           'phase phase
                           'stdout (get-output-string stdout)
                           'last-value (hash-ref env "IT")
                           'reason (exn-message e)
                           'where (exn:fail:unsupported-where e)))]
                  [exn:fail?
                   (lambda (e)
                     (hash 'status 'runtime-error
                           'phase phase
                           'stdout (get-output-string stdout)
                           'last-value (hash-ref env "IT")
                           'error (exn-message e)))])
    (execute-statements (program-statements parsed))
    (hash 'status 'ok
          'phase phase
          'stdout (get-output-string stdout)
          'last-value (hash-ref env "IT"))))
