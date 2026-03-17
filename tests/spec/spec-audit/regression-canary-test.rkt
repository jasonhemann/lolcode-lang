#lang racket/base

(require rackunit
         "../../../src/lolcode/main.rkt"
         "../../../src/lolcode/internal/reporting.rkt")

(module+ test
  ;; Spec ref: spec/upstream/lolcode-spec-v1.3.md:269
  ;; Variadics may omit MKAY when EOL closes open variadic operators.
  (test-case
   "REGRESSION: ALL OF / ANY OF accept EOL closure without MKAY (v1.3 line 269)"
   (define src
     "HAI 1.3\nVISIBLE ALL OF WIN AN FAIL\nVISIBLE ANY OF FAIL AN WIN\nKTHXBYE\n")
   (check-not-exn (lambda () (parse-program src)))
   (define out (run-source/report src))
   (check-eq? (hash-ref out 'status) 'ok)
   (check-equal? (hash-ref out 'stdout) "FAIL\nWIN\n"))

  ;; Spec ref: spec/upstream/lolcode-spec-v1.3.md:486
  ;; OMG literal excludes YARN values with interpolation forms :{var}.
  (test-case
   "REGRESSION: WTF? OMG rejects interpolated YARN literals (v1.3 line 486)"
   (check-exn exn:fail?
              (lambda ()
                (parse-program
                 "HAI 1.3\nI HAS A n ITZ \"x\"\nn, WTF?\n  OMG \":{n}\"\n    VISIBLE \"hit\"\nOIC\nKTHXBYE\n"))))

  ;; Spec ref: spec/upstream/lolcode-spec-v1.3.md:760-770, 790, 796-798
  ;; parent/omgwtf/izmakin slots and parent-chain lookup behavior are required.
  (test-case
   "REGRESSION: child observes parent-chain slot updates"
   (define src
     "HAI 1.3\nO HAI IM parent\n  I HAS A x ITZ 1\nKTHX\nO HAI IM child IM LIEK parent\nKTHX\nparent'Z x R 2\nVISIBLE child'Z x\nKTHXBYE\n")
   (define out (run-source/report src))
   (check-eq? (hash-ref out 'status) 'ok)
   (check-equal? (hash-ref out 'stdout) "2\n"))

  (test-case
   "REGRESSION: child exposes a non-NOOB parent slot"
   (define src
     "HAI 1.3\nO HAI IM parent\n  I HAS A x ITZ 1\nKTHX\nO HAI IM child IM LIEK parent\nKTHX\nVISIBLE child'Z parent\nKTHXBYE\n")
   (define out (run-source/report src))
   (check-eq? (hash-ref out 'status) 'ok)
   (check-equal? (hash-ref out 'stdout) "<BUKKIT>\n"))

  (test-case
   "REGRESSION: omgwtf slot fallback runs on missing slot access"
   (define src
     "HAI 1.3\nO HAI IM obj\n  HOW IZ I omgwtf\n    FOUND YR 42\n  IF U SAY SO\nKTHX\nVISIBLE obj'Z missing\nKTHXBYE\n")
   (define out (run-source/report src))
   (check-eq? (hash-ref out 'status) 'ok)
   (check-equal? (hash-ref out 'stdout) "42\n"))

  (test-case
   "REGRESSION: izmakin hook runs after object construction"
   (define src
     "HAI 1.3\nO HAI IM obj\n  I HAS A n ITZ 1\n  HOW IZ I izmakin\n    n R 9\n  IF U SAY SO\nKTHX\nVISIBLE obj'Z n\nKTHXBYE\n")
   (define out (run-source/report src))
   (check-eq? (hash-ref out 'status) 'ok)
   (check-equal? (hash-ref out 'stdout) "9\n"))

  ;; C1/C2/C3 adjudication policy:
  ;; method IT is activation-local and bypasses receiver slot lookup.
  (test-case
   "REGRESSION: object method IT is activation-local (not global/receiver)"
   (define src
     "HAI 1.3\nO HAI IM obj\n  HOW IZ I show\n    VISIBLE IT\n  IF U SAY SO\nKTHX\n7\nobj IZ show MKAY\nKTHXBYE\n")
   (define out (run-source/report src))
   (check-eq? (hash-ref out 'status) 'ok)
   (check-equal? (hash-ref out 'stdout) "NOOB\n"))

  ;; Spec ref: spec/upstream/lolcode-spec-v1.3.md:259
  ;; TYPE values should include bare words (NUMBR, NUMBAR, ...).
  (test-case
   "REGRESSION: bare TYPE values are valid expressions"
   (define src
     "HAI 1.3\nVISIBLE MAEK NUMBR A YARN\nVISIBLE MAEK TYPE A TROOF\nKTHXBYE\n")
   (define out (run-source/report src))
   (check-eq? (hash-ref out 'status) 'ok)
   (check-equal? (hash-ref out 'stdout) "NUMBR\nWIN\n"))

  )
