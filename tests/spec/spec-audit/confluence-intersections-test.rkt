#lang racket/base

(require rackunit
         "../../../src/lolcode/main.rkt"
         "../../../src/lolcode/internal/reporting.rkt")

(module+ test
  ;; Intersection: function return control + loop control/scope
  ;; Spec refs: 552, 564, 586.
  (test-case
   "confluence: FOUND YR inside loop exits function (not just loop)"
   (define src
     "HAI 1.3\nHOW IZ I firstover YR lim\n  I HAS A i ITZ 0\n  IM IN YR lp UPPIN YR i TIL BOTH SAEM i AN lim\n    BOTH SAEM i AN 3, O RLY?\n      YA RLY\n        FOUND YR i\n    OIC\n  IM OUTTA YR lp\n  FOUND YR -1\nIF U SAY SO\nVISIBLE I IZ firstover YR 8 MKAY\nKTHXBYE\n")
   (define out (run-source/report src))
   (check-eq? (hash-ref out 'status) 'ok)
   (check-equal? (hash-ref out 'stdout) "3\n"))

  (test-case
   "confluence: FOUND YR remains invalid outside function even inside loop"
   (define src
     "HAI 1.3\nI HAS A i ITZ 0\nIM IN YR lp UPPIN YR i TIL BOTH SAEM i AN 2\n  FOUND YR i\nIM OUTTA YR lp\nKTHXBYE\n")
   (define out (run-source/report src))
   (check-eq? (hash-ref out 'status) 'runtime-error)
   (check-true (regexp-match? #px"FOUND YR used outside function"
                              (hash-ref out 'error))))

  ;; Intersection: loop-local updater variable + lexical function closures
  ;; Spec refs: 101, 564, 602.
  (test-case
   "confluence: loop updater shadow does not dynamically capture function lookup"
   (define src
     "HAI 1.3\nI HAS A ctr ITZ 1\nHOW IZ I readctr\n  FOUND YR ctr\nIF U SAY SO\nIM IN YR lp UPPIN YR ctr TIL BOTH SAEM ctr AN 3\n  VISIBLE I IZ readctr MKAY\nIM OUTTA YR lp\nVISIBLE ctr\nKTHXBYE\n")
   (define out (run-source/report src))
   (check-eq? (hash-ref out 'status) 'ok)
   ;; Lexical lookup should read the global ctr binding, not loop-local ctr.
   (check-equal? (hash-ref out 'stdout) "1\n1\n1\n"))

  (test-case
   "confluence: function cannot resolve loop-local updater name by dynamic scope"
   (define src
     "HAI 1.3\nHOW IZ I readidx\n  FOUND YR idx\nIF U SAY SO\nIM IN YR lp UPPIN YR idx TIL BOTH SAEM idx AN 1\n  VISIBLE I IZ readidx MKAY\nIM OUTTA YR lp\nKTHXBYE\n")
   (define out (run-source/report src))
   (check-eq? (hash-ref out 'status) 'runtime-error)
   (check-true (regexp-match? #px"unknown identifier: idx"
                              (hash-ref out 'error))))

  ;; Intersection: method execution + loop GTFO validity
  ;; Spec refs: 552, 564, 594, 612.
  (test-case
   "confluence: GTFO in method loop breaks loop and method continues"
   (define src
     "HAI 1.3\nO HAI IM meter\n  HOW IZ I run\n    I HAS A out ITZ \"none\"\n    I HAS A i ITZ 0\n    IM IN YR lp UPPIN YR i TIL BOTH SAEM i AN 5\n      BOTH SAEM i AN 2, O RLY?\n        YA RLY\n          out R i\n          GTFO\n      OIC\n    IM OUTTA YR lp\n    FOUND YR out\n  IF U SAY SO\nKTHX\nVISIBLE meter IZ run MKAY\nKTHXBYE\n")
   (define out (run-source/report src))
   (check-eq? (hash-ref out 'status) 'ok)
   (check-equal? (hash-ref out 'stdout) "2\n"))

  (test-case
   "confluence: GTFO in method body returns NOOB"
   (define src
     "HAI 1.3\nO HAI IM meter\n  HOW IZ I bad\n    GTFO\n  IF U SAY SO\nKTHX\nVISIBLE meter IZ bad MKAY\nKTHXBYE\n")
   (define out (run-source/report src))
   (check-eq? (hash-ref out 'status) 'ok)
   (check-equal? (hash-ref out 'stdout) "NOOB\n"))

  (test-case
   "confluence: GTFO in object definition body remains invalid"
   (define src
     "HAI 1.3\nO HAI IM bad\n  GTFO\nKTHX\nKTHXBYE\n")
   (define out (run-source/report src))
   (check-eq? (hash-ref out 'status) 'runtime-error)
   (check-true (regexp-match? #px"GTFO used inside object definition bad"
                              (hash-ref out 'error))))

  ;; Intersection: object methods + switch returns + control validity in object defs
  ;; Spec refs: 486, 586, 612.
  (test-case
   "confluence: FOUND YR from method-local WTF? escapes full method"
   (define src
     "HAI 1.3\nO HAI IM chooser\n  HOW IZ I pick YR x\n    x, WTF?\n      OMG 7\n        FOUND YR \"seven\"\n      OMGWTF\n        FOUND YR \"other\"\n    OIC\n  IF U SAY SO\nKTHX\nVISIBLE chooser IZ pick YR 7 MKAY\nVISIBLE chooser IZ pick YR 2 MKAY\nKTHXBYE\n")
   (define out (run-source/report src))
   (check-eq? (hash-ref out 'status) 'ok)
   (check-equal? (hash-ref out 'stdout) "seven\nother\n"))

  (test-case
   "confluence: FOUND YR in object definition body remains invalid"
   (define src
     "HAI 1.3\nO HAI IM bad\n  FOUND YR 1\nKTHX\nKTHXBYE\n")
   (define out (run-source/report src))
   (check-eq? (hash-ref out 'status) 'runtime-error)
   (check-true (regexp-match? #px"FOUND YR used inside object definition bad"
                              (hash-ref out 'error)))))
