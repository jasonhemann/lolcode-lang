#lang racket/base

(require rackunit
         "../src/lolcode/main.rkt")

(module+ test
  (check-eq? implementation-phase 'bootstrap)

  (define parsed
    (parse-program "HAI 1.2\nVISIBLE \"OH HAI\"\nKTHXBYE\n"))
  (check-true (program? parsed))

  (define result (run-program parsed))
  (check-eq? (hash-ref result 'status) 'not-implemented)
  (check-eq? (hash-ref result 'phase) 'bootstrap)

  (check-exn exn:fail:contract?
             (lambda () (parse-program 42)))
  (check-exn exn:fail:contract?
             (lambda () (run-program "not-a-program")))
  (check-exn exn:fail:contract?
             (lambda () (run-file 99))))

