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

  (define switch-src
    "HAI 1.2\nI HAS A color ITZ \"G\"\ncolor, WTF?\n  OMG \"R\"\n    VISIBLE \"RED FISH\"\n    GTFO\n  OMG \"Y\"\n    VISIBLE \"YELLOW FISH\"\n  OMG \"G\"\n  OMG \"B\"\n    VISIBLE \"FISH HAS A FLAVOR\"\n    GTFO\n  OMGWTF\n    VISIBLE \"FISH IS TRANSPARENT\"\nOIC\nKTHXBYE\n")
  (define switch-result (run-source switch-src))
  (check-eq? (hash-ref switch-result 'status) 'ok)
  (check-equal? (hash-ref switch-result 'stdout) "FISH HAS A FLAVOR\n")

  (define function-src
    "HAI 1.3\nHOW IZ I addin YR x AN YR y\n  FOUND YR SUM OF x AN y\nIF U SAY SO\nI HAS A result ITZ I IZ addin YR 2 AN YR 3 MKAY\nVISIBLE result\nKTHXBYE\n")
  (define function-result (run-source function-src))
  (check-eq? (hash-ref function-result 'status) 'ok)
  (check-equal? (hash-ref function-result 'stdout) "5\n")

  (define bad-return-src
    "HAI 1.2\nFOUND YR 3\nKTHXBYE\n")
  (define bad-return (run-source bad-return-src))
  (check-eq? (hash-ref bad-return 'status) 'runtime-error)
  (check-true (regexp-match? #px"FOUND YR used outside function"
                             (hash-ref bad-return 'error)))

  (define bad-break-src
    "HAI 1.2\nGTFO\nKTHXBYE\n")
  (define bad-break (run-source bad-break-src))
  (check-eq? (hash-ref bad-break 'status) 'runtime-error)
  (check-true (regexp-match? #px"GTFO used outside switch/loop"
                             (hash-ref bad-break 'error)))

  (define object-alt-src
    "HAI 1.3\nO HAI IM pokeman\n  I HAS A name ITZ \"pikachu\"\nKTHX\nVISIBLE pokeman'Z name\nKTHXBYE\n")
  (define object-alt (run-source object-alt-src))
  (check-eq? (hash-ref object-alt 'status) 'ok)
  (check-equal? (hash-ref object-alt 'stdout) "pikachu\n")

  (define unsupported-src
    "HAI 1.3\nI HAS A obj ITZ A BUKKIT\nI HAS A res ITZ obj IZ call MKAY\nKTHXBYE\n")
  (define unsupported (run-source unsupported-src))
  (check-eq? (hash-ref unsupported 'status) 'unsupported)
  (check-true (regexp-match? #px"unsupported AST form"
                             (hash-ref unsupported 'reason)))

  (define inherited-object-src
    "HAI 1.3\nO HAI IM parent\n  I HAS A name ITZ \"pikachu\"\nKTHX\nO HAI IM child IM LIEK parent\nKTHX\nVISIBLE child'Z name\nKTHXBYE\n")
  (define inherited-object (run-source inherited-object-src))
  (check-eq? (hash-ref inherited-object 'status) 'ok)
  (check-equal? (hash-ref inherited-object 'stdout) "pikachu\n"))
