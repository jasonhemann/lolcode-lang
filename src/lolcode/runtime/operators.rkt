#lang racket/base

(require "value.rkt")

(provide binary-operator-table
         unary-operator-table
         variadic-operator-compiler-table)

(define binary-operator-table
  (hash
   "SUM OF" (lambda (lv rv) (+ (coerce-number 'SUM lv) (coerce-number 'SUM rv)))
   "DIFF OF" (lambda (lv rv) (- (coerce-number 'DIFF lv) (coerce-number 'DIFF rv)))
   "PRODUKT OF" (lambda (lv rv) (* (coerce-number 'PRODUKT lv) (coerce-number 'PRODUKT rv)))
   "QUOSHUNT OF" (lambda (lv rv) (/ (coerce-number 'QUOSHUNT lv) (coerce-number 'QUOSHUNT rv)))
   "MOD OF"
   (lambda (lv rv)
     (remainder (inexact->exact (truncate (coerce-number 'MOD lv)))
                (inexact->exact (truncate (coerce-number 'MOD rv)))))
   "BIGGR OF" (lambda (lv rv) (max (coerce-number 'BIGGR lv) (coerce-number 'BIGGR rv)))
   "SMALLR OF" (lambda (lv rv) (min (coerce-number 'SMALLR lv) (coerce-number 'SMALLR rv)))
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
              (map (lambda (a) (lol-string (a e ctx))) arg-procs))))
   "ALL OF"
   (lambda (arg-procs)
     (lambda (e ctx)
       (andmap (lambda (a) (lol-truthy? (a e ctx))) arg-procs)))
   "ANY OF"
   (lambda (arg-procs)
     (lambda (e ctx)
       (ormap (lambda (a) (lol-truthy? (a e ctx))) arg-procs)))))
