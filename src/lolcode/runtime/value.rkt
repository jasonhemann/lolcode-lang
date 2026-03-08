#lang racket/base

(require racket/class
         racket/format
         racket/list
         racket/set
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
                [parent noob])
    (super-new)

    (define active-omgwtf-slots (mutable-set))

    (define/private (ensure-special-slots!)
      (unless (hash-has-key? slots "parent")
        (hash-set! slots "parent" (box parent)))
      (unless (hash-has-key? slots "omgwtf")
        (hash-set! slots "omgwtf" (box noob)))
      (unless (hash-has-key? slots "izmakin")
        (hash-set! slots "izmakin" (box noob))))

    (ensure-special-slots!)

    (define/private (parent-object [visited #f])
      (define parent-value
        (unbox (hash-ref slots "parent" (lambda () (box noob)))))
      (cond
        [(not (lol-object? parent-value)) #f]
        [(and visited (set-member? visited parent-value)) #f]
        [else parent-value]))

    (define/public (lookup-slot-box name visited)
      (cond
        [(hash-ref slots name #f)
         => (lambda (maybe-box)
              (and (box? maybe-box) maybe-box))]
        [else
         (set-add! visited this)
         (define p (parent-object visited))
         (and p (send p lookup-slot-box name visited))]))

    (define/public (resolve-missing-slot! name resolver)
      (when (set-member? active-omgwtf-slots name)
        (error 'run-program
               "omgwtf recursion while resolving missing slot: ~a"
               name))
      (dynamic-wind
        (lambda ()
          (set-add! active-omgwtf-slots name))
        (lambda ()
          (define value (resolver))
          ;; Memoize the synthesized result into the missing slot.
          ;; If omgwtf mutated the same slot during evaluation, the return value
          ;; remains authoritative for the requested missing name.
          (send this declare-slot! name value)
          value)
        (lambda ()
          (set-remove! active-omgwtf-slots name))))

    (define/public (clone)
      (define copied-slots (make-hash))
      (for ([(name b) (in-hash slots)])
        (hash-set! copied-slots name (box (unbox b))))
      (new lol-object%
           [slots copied-slots]
           [parent (unbox (hash-ref slots "parent" (lambda () (box noob))))]))

    (define/public (prototype)
      (new lol-object%
           [parent this]))

    (define/public (slot-table)
      slots)

    (define/public (slot-names [visited (mutable-seteq)])
      (set-add! visited this)
      (define parent-names
        (let ([p (parent-object visited)])
          (if p
              (send p slot-names visited)
              '())))
      (remove-duplicates
       (append (hash-keys slots) parent-names)))

    (define/public (copy-visible-into! target)
      ;; Copy the donor object's effective visible slot interface:
      ;; own slots first, then inherited-visible slots from its parent chain.
      (for ([name (in-list (send this slot-names (mutable-seteq)))])
        (send target declare-slot! name (send this lookup-slot name noob))))

    (define/public (has-slot? name)
      (hash-has-key? slots name))

    (define/public (lookup-slot name [default #f])
      (cond
        [(send this lookup-slot-box name (mutable-seteq)) => unbox]
        [else default]))

    (define/public (lookup-special-procedure-slot name [visited (mutable-seteq)])
      (define (lookup-parent)
        (set-add! visited this)
        (define p (parent-object visited))
        (and p
             (send p lookup-special-procedure-slot name visited)))
      (cond
        [(hash-ref slots name #f)
         => (lambda (maybe-box)
              (or (and (box? maybe-box)
                       (let ([maybe-proc (unbox maybe-box)])
                         (and (procedure? maybe-proc) maybe-proc)))
                  (lookup-parent)))]
        [else (lookup-parent)]))

    (define/public (get-slot name [default noob])
      (cond
        [(send this lookup-slot-box name (mutable-seteq)) => unbox]
        [else default]))

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
        [(send this lookup-slot-box name (mutable-seteq))
         (hash-set! slots name (box value))]
        [else
         (error 'run-program "unknown slot: ~a" name)]))

    (define/public (set-slot! name value)
      (send this declare-slot! name value))

    (define/public (remove-slot! name)
      (hash-remove! slots name))))

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
  (define fixed
    (~r (truncate-real-decimals n 2)
        #:precision '(= 2)))
  (define trimmed
    (regexp-replace #px"\\.$"
                    (regexp-replace #px"0+$" fixed "")
                    ""))
  (if (string=? trimmed "")
      "0"
      trimmed))

(define (lol-string v)
  (cond
    [(eq? v noob) "NOOB"]
    [(boolean? v) (if v "WIN" "FAIL")]
    [(and (number? v)
          (real? v)
          (rational? v)
          (or (inexact? v)
              (not (integer? v))))
     (format-numbar (if (inexact? v) v (exact->inexact v)))]
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
