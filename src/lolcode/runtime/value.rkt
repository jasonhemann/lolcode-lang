#lang racket/base

(require racket/class
         racket/format
         racket/list
         racket/string
         "env.rkt")

(provide lol-object%
         lol-object?
         lol-string
         lol-truthy?
         lol-equal?
         bool-xor
         coerce-number
         coerce-cast-number
         cast-value
         type-default-value
         identifier-text
         require-arity
         install-runtime-builtins!)

(define lol-object%
  (class object%
    (init-field [slots (make-hash)]
                [methods (make-hash)]
                [parent noob])
    (super-new)

    (define active-omgwtf-slots (make-hash))

    (define (default-omgwtf receiver arg-values _ctx)
      (require-arity "omgwtf" arg-values 1)
      (error 'run-program "unknown slot: ~a" (lol-string (first arg-values))))

    (define/private (ensure-special-slots!)
      (unless (hash-has-key? slots "parent")
        (hash-set! slots "parent" (box parent)))
      (unless (hash-has-key? slots "omgwtf")
        (hash-set! slots "omgwtf" (box default-omgwtf)))
      (unless (hash-has-key? slots "izmakin")
        (hash-set! slots "izmakin" (box noob))))

    (ensure-special-slots!)

    (define/private (parent-object [visited #f])
      (define parent-value
        (unbox (hash-ref slots "parent" (lambda () (box noob)))))
      (cond
        [(not (lol-object? parent-value)) #f]
        [(and visited (hash-ref visited parent-value #f)) #f]
        [else parent-value]))

    (define/public (lookup-slot-box name visited)
      (cond
        [(hash-ref slots name #f)
         => (lambda (maybe-box)
              (and (box? maybe-box) maybe-box))]
        [else
         (hash-set! visited this #t)
         (define p (parent-object visited))
         (and p (send p lookup-slot-box name visited))]))

    (define/public (lookup-method name visited)
      (cond
        [(hash-ref methods name #f)
         => (lambda (maybe-method)
              (and (procedure? maybe-method) maybe-method))]
        [else
         (hash-set! visited this #t)
         (define p (parent-object visited))
         (and p (send p lookup-method name visited))]))

    (define/private (call-omgwtf! name ctx)
      (when (hash-ref active-omgwtf-slots name #f)
        (error 'run-program
               "omgwtf recursion while resolving missing slot: ~a"
               name))
      (dynamic-wind
        (lambda ()
          (hash-set! active-omgwtf-slots name #t))
        (lambda ()
          (define sentinel (gensym 'no-omgwtf))
          (define maybe-method-value
            (send this invoke-method
                  "omgwtf"
                  (list name)
                  ctx
                  (lambda () sentinel)))
          (define value
            (if (eq? maybe-method-value sentinel)
                (let ([maybe-hook (send this lookup-slot "omgwtf" noob)])
                  (if (procedure? maybe-hook)
                      (maybe-hook this (list name) ctx)
                      (error 'run-program "unknown slot: ~a" name)))
                maybe-method-value))
          ;; Memoize the synthesized result into the missing slot.
          ;; If omgwtf mutated the same slot during evaluation, the return value
          ;; remains authoritative for the requested missing name.
          (send this declare-slot! name value)
          value)
        (lambda ()
          (hash-remove! active-omgwtf-slots name))))

    (define/public (clone)
      (define copied-slots (make-hash))
      (for ([(name b) (in-hash slots)])
        (hash-set! copied-slots name (box (unbox b))))
      (new lol-object%
           [slots copied-slots]
           [methods (hash-copy methods)]
           [parent (unbox (hash-ref slots "parent" (lambda () (box noob))))]))

    (define/public (prototype)
      (new lol-object%
           [parent this]))

    (define/public (slot-table)
      slots)

    (define/public (slot-names [visited (make-hasheq)])
      (hash-set! visited this #t)
      (define parent-names
        (let ([p (parent-object visited)])
          (if p
              (send p slot-names visited)
              '())))
      (remove-duplicates
       (append (hash-keys slots) parent-names)))

    (define/public (copy-own-into! target)
      (for ([(name b) (in-hash slots)])
        (send target declare-slot! name (unbox b)))
      (for ([(name fn) (in-hash methods)]
            #:when (procedure? fn))
        (send target define-method! name fn)))

    (define/public (has-slot? name)
      (hash-has-key? slots name))

    (define/public (lookup-slot name [default #f])
      (cond
        [(send this lookup-slot-box name (make-hasheq)) => unbox]
        [else default]))

    (define/public (get-slot name [default noob] [ctx #f])
      (cond
        [(send this lookup-slot-box name (make-hasheq)) => unbox]
        [else
         (call-omgwtf! name ctx)]))

    (define/public (declare-slot! name value)
      (cond
        [(hash-ref slots name #f)
         => (lambda (maybe-box)
              (if (box? maybe-box)
                  (set-box! maybe-box value)
                  (hash-set! slots name (box value))))]
        [else
         (hash-set! slots name (box value))]))

    (define/public (assign-slot! name value)
      (cond
        [(hash-ref slots name #f)
         => (lambda (b)
              (set-box! b value))]
        [(send this lookup-slot-box name (make-hasheq))
         (hash-set! slots name (box value))]
        [else
         (error 'run-program "unknown slot: ~a" name)]))

    (define/public (set-slot! name value)
      (send this declare-slot! name value))

    (define/public (remove-slot! name)
      (hash-remove! slots name))

    (define/public (define-method! name fn)
      (hash-set! methods name fn))

    (define/public (get-method name [default #f])
      (or (send this lookup-method name (make-hasheq))
          default))

    (define/public (invoke-method name arg-values ctx fallback-thunk)
      (define method
        (send this lookup-method name (make-hasheq)))
      (cond
        [(procedure? method) (method this arg-values ctx)]
        [(procedure? fallback-thunk) (fallback-thunk)]
        [else (error 'run-program "unknown method: ~a" name)]))))

(define (lol-object? v)
  (is-a? v lol-object%))

(define (truncate-real-decimals n places)
  (define scale (expt 10 places))
  (define scaled (* n scale))
  (define clipped
    (if (negative? scaled)
        (ceiling scaled)
        (floor scaled)))
  (/ clipped scale))

(define (format-numbar n)
  (~r (truncate-real-decimals n 2)
      #:precision '(= 2)))

(define (lol-string v)
  (cond
    [(eq? v noob) "NOOB"]
    [(boolean? v) (if v "WIN" "FAIL")]
    [(and (number? v)
          (rational? v)
          (inexact? v))
     (format-numbar v)]
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

(define (bool-xor a b)
  (or (and a (not b))
      (and (not a) b)))

(define (lol-equal? lv rv)
  ;; Spec 1.3 comparison: numeric comparison only when both operands are numeric;
  ;; otherwise no implicit casting is performed.
  (if (and (number? lv) (number? rv))
      (= lv rv)
      (equal? lv rv)))

(define (coerce-number who v)
  (cond
    [(eq? v noob)
     (error who "cannot cast NOOB to numeric value")]
    [else
     (coerce-cast-number who v)]))

(define strict-numeric-yarn-rx
  #px"^-?[0-9]+(?:\\.[0-9]+)?$")

(define (parse-strict-yarn-number who text)
  (unless (regexp-match? strict-numeric-yarn-rx text)
    (error who "cannot cast YARN to numeric value: ~e" text))
  (or (string->number text)
      (error who "cannot cast YARN to numeric value: ~e" text)))

(define (coerce-cast-number who v)
  (cond
    [(number? v) v]
    [(boolean? v) (if v 1 0)]
    [(eq? v noob) 0]
    [(string? v)
     (parse-strict-yarn-number who v)]
    [else (error who "cannot cast ~e to numeric value" v)]))

(define (cast-value who v type-name)
  (case type-name
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
    [else
     (error who "unknown cast target type: ~a" type-name)]))

(define (type-default-value type-name)
  (case type-name
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

(define (install-runtime-builtins! _builtins-env)
  (void))
