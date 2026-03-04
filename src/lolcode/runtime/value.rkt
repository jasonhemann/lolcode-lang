#lang racket/base

(require racket/class
         racket/list
         racket/string
         "env.rkt")

(provide lol-object%
         lol-object?
         lol-string
         lol-truthy?
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

(define (bool-xor a b)
  (or (and a (not b))
      (and (not a) b)))

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
