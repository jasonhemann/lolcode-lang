#lang racket/base

(require rackunit
         "../../src/lolcode/main.rkt")

(define (run-source source)
  (run-program (parse-program source)))

(module+ test
  (define declare-assign-src
    "HAI 1.2\nI HAS A var\nvar R 3\nVISIBLE var\nKTHXBYE\n")
  (define declare-assign (run-source declare-assign-src))
  (check-eq? (hash-ref declare-assign 'status) 'ok)
  (check-equal? (hash-ref declare-assign 'stdout) "3\n")
  (check-equal? (hash-ref declare-assign 'last-value) 3)

  (define typed-decl-src
    "HAI 1.3\nI HAS A count ITZ A NUMBR\nVISIBLE count\nKTHXBYE\n")
  (define typed-decl (run-source typed-decl-src))
  (check-eq? (hash-ref typed-decl 'status) 'ok)
  (check-equal? (hash-ref typed-decl 'stdout) "0\n")

  (define srs-target-src
    "HAI 1.3\nI HAS A name ITZ \"var\"\nI HAS A SRS name ITZ 0\nVISIBLE var\nKTHXBYE\n")
  (define srs-target (run-source srs-target-src))
  (check-eq? (hash-ref srs-target 'status) 'ok)
  (check-equal? (hash-ref srs-target 'stdout) "0\n")

  (define bukkit-slot-src
    "HAI 1.3\nI HAS A obj ITZ A BUKKIT\nobj HAS A answer ITZ 42\nVISIBLE obj'Z answer\nKTHXBYE\n")
  (define bukkit-slot (run-source bukkit-slot-src))
  (check-eq? (hash-ref bukkit-slot 'status) 'ok)
  (check-equal? (hash-ref bukkit-slot 'stdout) "42\n")

  (define unsupported-src
    "HAI 1.2\nWTF?\n  OMG \"x\"\n    VISIBLE \"x\"\nOIC\nKTHXBYE\n")
  (define unsupported (run-source unsupported-src))
  (check-eq? (hash-ref unsupported 'status) 'unsupported))
