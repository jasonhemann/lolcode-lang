#lang racket/base

(require "value.rkt")

(provide binary-operator-table
         unary-operator-table
         variadic-operator-compiler-table)

(define ((binop/coerce who op) lv rv)
  (op (coerce-number who lv)
      (coerce-number who rv)))

(define binary-operator-table
  (hash
   "SUM OF" (binop/coerce 'SUM +)
   "DIFF OF" (binop/coerce 'DIFF -)
   "PRODUKT OF" (binop/coerce 'PRODUKT *)
   "QUOSHUNT OF"
   (lambda (lv rv)
     (define lnum (coerce-number 'QUOSHUNT lv))
     (define rnum (coerce-number 'QUOSHUNT rv))
     (if (and (exact-integer? lnum)
              (exact-integer? rnum))
         (quotient lnum rnum)
         (/ lnum rnum)))
   "MOD OF"
   (lambda (lv rv)
     (remainder (inexact->exact (truncate (coerce-number 'MOD lv)))
                (inexact->exact (truncate (coerce-number 'MOD rv)))))
   "BIGGR OF" (binop/coerce 'BIGGR max)
   "SMALLR OF" (binop/coerce 'SMALLR min)
   "BOTH OF" (lambda (lv rv) (and (lol-truthy? lv) (lol-truthy? rv)))
   "EITHER OF" (lambda (lv rv) (or (lol-truthy? lv) (lol-truthy? rv)))
   "WON OF" (lambda (lv rv) (bool-xor (lol-truthy? lv)
                                       (lol-truthy? rv)))
   "BOTH SAEM" (lambda (lv rv) (lol-equal? lv rv))
   "DIFFRINT" (lambda (lv rv) (not (lol-equal? lv rv)))))

(define unary-operator-table
  (hash
   "NOT" (lambda (v) (not (lol-truthy? v)))))

(define variadic-operator-compiler-table
  (hash
   "SMOOSH"
   (lambda (arg-procs)
     (lambda (e ctx)
       (apply string-append
              (for/list ([a (in-list arg-procs)])
                (lol-string (a e ctx))))))
   "ALL OF"
   (lambda (arg-procs)
     (lambda (e ctx)
       (for/fold ([out #t])
                 ([a (in-list arg-procs)])
         (if (lol-truthy? (a e ctx))
             out
             #f))))
   "ANY OF"
   (lambda (arg-procs)
     (lambda (e ctx)
       (for/fold ([out #f])
                 ([a (in-list arg-procs)])
         (if (lol-truthy? (a e ctx))
             #t
             out))))))
