#lang racket/base

(require rackunit
         "../../../src/lolcode/main.rkt")

(define (run-source source)
  (run-program (parse-program source)))

(module+ test
  (define optional-an-binary
    "HAI 1.3\nVISIBLE SUM OF 1 2\nKTHXBYE\n")
  (define optional-an-binary-result
    (run-source optional-an-binary))
  (check-eq? (hash-ref optional-an-binary-result 'status) 'ok)
  (check-equal? (hash-ref optional-an-binary-result 'stdout) "3\n")

  (define optional-an-variadic
    "HAI 1.3\nVISIBLE ALL OF WIN FAIL MKAY\nVISIBLE ANY OF FAIL WIN MKAY\nKTHXBYE\n")
  (define optional-an-variadic-result
    (run-source optional-an-variadic))
  (check-eq? (hash-ref optional-an-variadic-result 'status) 'ok)
  (check-equal? (hash-ref optional-an-variadic-result 'stdout) "FAIL\nWIN\n")

  (define optional-an-smoosh
    "HAI 1.3\nVISIBLE SMOOSH \"A\" \"B\" MKAY\nKTHXBYE\n")
  (define optional-an-smoosh-result
    (run-source optional-an-smoosh))
  (check-eq? (hash-ref optional-an-smoosh-result 'status) 'ok)
  (check-equal? (hash-ref optional-an-smoosh-result 'stdout) "AB\n")

  (define bad-difference
    "HAI 1.3\nVISIBLE DIFFERENCE OF 5 AN 2\nKTHXBYE\n")
  (check-exn #px"syntax error:"
             (lambda () (parse-program bad-difference)))

  (define bad-qoushunt
    "HAI 1.3\nVISIBLE QOUSHUNT OF 6 AN 2\nKTHXBYE\n")
  (check-exn #px"syntax error:"
             (lambda () (parse-program bad-qoushunt)))

  (define and-unbound-runtime
    "HAI 1.3\nVISIBLE SUM OF 1 AND 2\nKTHXBYE\n")
  (define and-unbound-runtime-result
    (run-source and-unbound-runtime))
  (check-eq? (hash-ref and-unbound-runtime-result 'status) 'runtime-error)
  (check-true (regexp-match? #px"unknown identifier: AND"
                             (hash-ref and-unbound-runtime-result 'error)))

  (define and-bound-runtime
    "HAI 1.3\nI HAS A AND ITZ 2\nVISIBLE SUM OF 1 AND 2\nKTHXBYE\n")
  (define and-bound-runtime-result
    (run-source and-bound-runtime))
  (check-eq? (hash-ref and-bound-runtime-result 'status) 'ok)
  (check-equal? (hash-ref and-bound-runtime-result 'stdout) "3\n"))
