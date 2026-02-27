#lang racket/base

(require rackunit
         "../../src/lolcode/main.rkt")

(module+ test
  (define missing-kthxbye
    "HAI 1.2\nVISIBLE \"OH HAI\"\n")
  (check-exn exn:fail?
             (lambda () (parse-program missing-kthxbye)))

  (define missing-version
    "HAI\nVISIBLE \"OH HAI\"\nKTHXBYE\n")
  (check-exn exn:fail?
             (lambda () (parse-program missing-version)))

  (define unterminated-string
    "HAI 1.2\nVISIBLE \"oops\nKTHXBYE\n")
  (check-exn exn:fail?
             (lambda () (parse-program unterminated-string))))
