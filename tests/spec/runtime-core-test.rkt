#lang racket/base

(require rackunit
         "../../src/lolcode/ast.rkt"
         "../../src/lolcode/main.rkt")

(define (run-source source #:input [input ""])
  (parameterize ([current-input-port (open-input-string input)])
    (run-program (parse-program source))))

(module+ test
  (define declare-assign-src
    "HAI 1.3\nI HAS A var\nvar R 3\nVISIBLE var\nKTHXBYE\n")
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

  (define srs-numeric-target-src
    "HAI 1.3\nI HAS A idx ITZ 0\nI HAS A SRS idx ITZ 9\nKTHXBYE\n")
  (define srs-numeric-target (run-source srs-numeric-target-src))
  (check-eq? (hash-ref srs-numeric-target 'status) 'ok)
  (check-equal? (hash-ref srs-numeric-target 'last-value) 'NOOB)

  (define bukkit-slot-src
    "HAI 1.3\nI HAS A obj ITZ A BUKKIT\nobj HAS A answer ITZ 42\nVISIBLE obj'Z answer\nKTHXBYE\n")
  (define bukkit-slot (run-source bukkit-slot-src))
  (check-eq? (hash-ref bukkit-slot 'status) 'ok)
  (check-equal? (hash-ref bukkit-slot 'stdout) "42\n")

  (define bukkit-srs-numeric-slot-src
    "HAI 1.3\nI HAS A obj ITZ A BUKKIT\nobj HAS A SRS 0 ITZ 41\nobj'Z SRS 0 R SUM OF obj'Z SRS 0 AN 1\nVISIBLE obj'Z SRS 0\nKTHXBYE\n")
  (define bukkit-srs-numeric-slot (run-source bukkit-srs-numeric-slot-src))
  (check-eq? (hash-ref bukkit-srs-numeric-slot 'status) 'ok)
  (check-equal? (hash-ref bukkit-srs-numeric-slot 'stdout) "42\n")

  (define switch-src
    "HAI 1.3\nI HAS A color ITZ \"G\"\ncolor, WTF?\n  OMG \"R\"\n    VISIBLE \"RED FISH\"\n    GTFO\n  OMG \"Y\"\n    VISIBLE \"YELLOW FISH\"\n  OMG \"G\"\n  OMG \"B\"\n    VISIBLE \"FISH HAS A FLAVOR\"\n    GTFO\n  OMGWTF\n    VISIBLE \"FISH IS TRANSPARENT\"\nOIC\nKTHXBYE\n")
  (define switch-result (run-source switch-src))
  (check-eq? (hash-ref switch-result 'status) 'ok)
  (check-equal? (hash-ref switch-result 'stdout) "FISH HAS A FLAVOR\n")

  (define switch-duplicate-src
    "HAI 1.3\nI HAS A x ITZ 1\nx, WTF?\n  OMG 1\n    VISIBLE \"A\"\n  OMG 1\n    VISIBLE \"B\"\nOIC\nKTHXBYE\n")
  (define switch-duplicate-result (run-source switch-duplicate-src))
  (check-eq? (hash-ref switch-duplicate-result 'status) 'runtime-error)
  (check-true (regexp-match? #px"duplicate OMG literal in WTF\\?"
                             (hash-ref switch-duplicate-result 'error "")))

  (define function-src
    "HAI 1.3\nHOW IZ I addin YR x AN YR y\n  FOUND YR SUM OF x AN y\nIF U SAY SO\nI HAS A result ITZ I IZ addin YR 2 AN YR 3 MKAY\nVISIBLE result\nKTHXBYE\n")
  (define function-result (run-source function-src))
  (check-eq? (hash-ref function-result 'status) 'ok)
  (check-equal? (hash-ref function-result 'stdout) "5\n")

  (define function-implicit-it-return-src
    "HAI 1.3\nHOW IZ I calc\n  SUM OF 2 AN 3\nIF U SAY SO\nVISIBLE I IZ calc MKAY\nKTHXBYE\n")
  (define function-implicit-it-return (run-source function-implicit-it-return-src))
  (check-eq? (hash-ref function-implicit-it-return 'status) 'ok)
  (check-equal? (hash-ref function-implicit-it-return 'stdout) "5\n")

  (define function-gtfo-return-src
    "HAI 1.3\nHOW IZ I quitfast\n  GTFO\nIF U SAY SO\nVISIBLE I IZ quitfast MKAY\nKTHXBYE\n")
  (define function-gtfo-return (run-source function-gtfo-return-src))
  (check-eq? (hash-ref function-gtfo-return 'status) 'ok)
  (check-equal? (hash-ref function-gtfo-return 'stdout) "NOOB\n")

  (define function-outer-scope-src
    "HAI 1.3\nI HAS A outside ITZ 9\nHOW IZ I reach\n  FOUND YR outside\nIF U SAY SO\nVISIBLE I IZ reach MKAY\nKTHXBYE\n")
  (define function-outer-scope (run-source function-outer-scope-src))
  (check-eq? (hash-ref function-outer-scope 'status) 'runtime-error)
  (check-true (regexp-match? #px"unknown identifier: outside"
                             (hash-ref function-outer-scope 'error)))

  (define expr-stmt-src
    "HAI 1.3\nHOW IZ I ping\n  VISIBLE \"P\"\nIF U SAY SO\nI IZ ping MKAY\nKTHXBYE\n")
  (define expr-stmt-result (run-source expr-stmt-src))
  (check-eq? (hash-ref expr-stmt-result 'status) 'ok)
  (check-equal? (hash-ref expr-stmt-result 'stdout) "P\n")

  (define bad-return-src
    "HAI 1.3\nFOUND YR 3\nKTHXBYE\n")
  (define bad-return (run-source bad-return-src))
  (check-eq? (hash-ref bad-return 'status) 'runtime-error)
  (check-true (regexp-match? #px"FOUND YR used outside function"
                             (hash-ref bad-return 'error)))

  (define bad-break-src
    "HAI 1.3\nGTFO\nKTHXBYE\n")
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
  (check-eq? (hash-ref unsupported 'status) 'runtime-error)
  (check-true (regexp-match? #px"unknown method"
                             (hash-ref unsupported 'error)))

  (define inherited-object-src
    "HAI 1.3\nO HAI IM parent\n  I HAS A name ITZ \"pikachu\"\nKTHX\nO HAI IM child IM LIEK parent\nKTHX\nVISIBLE child'Z name\nKTHXBYE\n")
  (define inherited-object (run-source inherited-object-src))
  (check-eq? (hash-ref inherited-object 'status) 'ok)
  (check-equal? (hash-ref inherited-object 'stdout) "pikachu\n")

  (define loop-src
    "HAI 1.3\nI HAS A idx ITZ 0\nI HAS A acc ITZ 0\nIM IN YR count UPPIN YR idx TIL BOTH SAEM idx AN 5\n  acc R SUM OF acc AN idx\nIM OUTTA YR count\nVISIBLE acc\nKTHXBYE\n")
  (define loop-result (run-source loop-src))
  (check-eq? (hash-ref loop-result 'status) 'ok)
  (check-equal? (hash-ref loop-result 'stdout) "10\n")

  (define loop-counter-scope-src
    "HAI 1.3\nI HAS A ctr ITZ 5\nIM IN YR lp UPPIN YR ctr WILE DIFFRINT ctr AN 10\n  VISIBLE ctr\nIM OUTTA YR lp\nVISIBLE ctr\nKTHXBYE\n")
  (define loop-counter-scope-result (run-source loop-counter-scope-src))
  (check-eq? (hash-ref loop-counter-scope-result 'status) 'ok)
  (check-equal? (hash-ref loop-counter-scope-result 'stdout) "5\n6\n7\n8\n9\n5\n")

  (define loop-counter-no-leak-src
    "HAI 1.3\nIM IN YR lp UPPIN YR idx TIL BOTH SAEM idx AN 3\n  VISIBLE idx\nIM OUTTA YR lp\nVISIBLE idx\nKTHXBYE\n")
  (define loop-counter-no-leak-result (run-source loop-counter-no-leak-src))
  (check-eq? (hash-ref loop-counter-no-leak-result 'status) 'runtime-error)
  (check-equal? (hash-ref loop-counter-no-leak-result 'stdout) "0\n1\n2\n")
  (check-true (regexp-match? #px"unknown identifier: idx"
                             (hash-ref loop-counter-no-leak-result 'error "")))

  (define nested-loop-src
    "HAI 1.3\nI HAS A outer ITZ 0\nI HAS A total ITZ 0\nIM IN YR out UPPIN YR outer TIL BOTH SAEM outer AN 3\n  I HAS A inner ITZ 0\n  IM IN YR innerloop UPPIN YR inner TIL BOTH SAEM inner AN 2\n    total R SUM OF total AN 1\n  IM OUTTA YR innerloop\nIM OUTTA YR out\nVISIBLE total\nKTHXBYE\n")
  (define nested-loop-result (run-source nested-loop-src))
  (check-eq? (hash-ref nested-loop-result 'status) 'ok)
  (check-equal? (hash-ref nested-loop-result 'stdout) "6\n")

  (define logic-src
    "HAI 1.3\nI HAS A n ITZ 42\nVISIBLE BOTH OF DIFFRINT n AN 0 AN DIFFRINT n AN 42\nVISIBLE EITHER OF BOTH SAEM n AN 0 AN BOTH SAEM n AN 42\nVISIBLE WON OF BOTH SAEM n AN 42 AN BOTH SAEM n AN 0\nVISIBLE ALL OF DIFFRINT n AN 0 AN NOT BOTH SAEM n AN 0 MKAY\nVISIBLE ANY OF BOTH SAEM n AN 0 AN BOTH SAEM n AN 42 MKAY\nKTHXBYE\n")
  (define logic-result (run-source logic-src))
  (check-eq? (hash-ref logic-result 'status) 'ok)
  (check-equal? (hash-ref logic-result 'stdout) "FAIL\nWIN\nWIN\nWIN\nWIN\n")

  (define logic-no-mkay-src
    "HAI 1.3\nI HAS A flag ITZ WIN\nI HAS A anotherflag ITZ FAIL\nI HAS A flag3 ITZ WIN\nI HAS A flag4 ITZ WIN\nI HAS A flag5\nflag5 R ALL OF flag AN anotherflag AN flag3 AN flag4\nVISIBLE flag5\nKTHXBYE\n")
  (define logic-no-mkay-result (run-source logic-no-mkay-src))
  (check-eq? (hash-ref logic-no-mkay-result 'status) 'ok)
  (check-equal? (hash-ref logic-no-mkay-result 'stdout) "FAIL\n")

  (define cast-src
    "HAI 1.3\nI HAS A obj ITZ A BUKKIT\nobj HAS A answer ITZ \"41\"\nobj'Z answer IS NOW A NUMBR\nobj'Z answer R SUM OF obj'Z answer AN 1\nVISIBLE obj'Z answer\nKTHXBYE\n")
  (define cast-result (run-source cast-src))
  (check-eq? (hash-ref cast-result 'status) 'ok)
  (check-equal? (hash-ref cast-result 'stdout) "42\n")

  (define method-src
    "HAI 1.3\nO HAI IM counter\n  I HAS A val ITZ 1\n  HOW IZ I bump YR delta\n    val R SUM OF val AN delta\n    FOUND YR val\n  IF U SAY SO\nKTHX\nVISIBLE counter IZ bump YR 2 MKAY\nVISIBLE counter IZ bump YR 3 MKAY\nVISIBLE counter'Z val\nKTHXBYE\n")
  (define method-result (run-source method-src))
  (check-eq? (hash-ref method-result 'status) 'ok)
  (check-equal? (hash-ref method-result 'stdout) "3\n6\n6\n")

  (define gimmeh-src
    "HAI 1.3\nI HAS A name\nGIMMEH name\nVISIBLE name\nKTHXBYE\n")
  (define gimmeh-result (run-source gimmeh-src #:input "Ada\n"))
  (check-eq? (hash-ref gimmeh-result 'status) 'ok)
  (check-equal? (hash-ref gimmeh-result 'stdout) "Ada\n")

  (define gimmeh-eof-src
    "HAI 1.3\nI HAS A name\nGIMMEH name\nVISIBLE name\nKTHXBYE\n")
  (define gimmeh-eof-result (run-source gimmeh-eof-src #:input ""))
  (check-eq? (hash-ref gimmeh-eof-result 'status) 'ok)
  (check-equal? (hash-ref gimmeh-eof-result 'stdout) "NOOB\n")

  (define visible-bang-src
    "HAI 1.3\nVISIBLE \"A\"!\nVISIBLE \"B\"\nKTHXBYE\n")
  (define visible-bang-result (run-source visible-bang-src))
  (check-eq? (hash-ref visible-bang-result 'status) 'ok)
  (check-equal? (hash-ref visible-bang-result 'stdout) "AB\n")

  (define can-has-src
    "HAI 1.3\nCAN HAS STRING?\nVISIBLE \"OK\"\nKTHXBYE\n")
  (define can-has-result (run-source can-has-src))
  (check-eq? (hash-ref can-has-result 'status) 'ok)
  (check-equal? (hash-ref can-has-result 'stdout) "OK\n")

  (define visible-inline-src
    "HAI 1.3\nVISIBLE \"A\" \"B\" 3\nKTHXBYE\n")
  (define visible-inline-result (run-source visible-inline-src))
  (check-eq? (hash-ref visible-inline-result 'status) 'ok)
  (check-equal? (hash-ref visible-inline-result 'stdout) "AB3\n")

  (define string-namespace-src
    "HAI 1.3\nCAN HAS STRING?\nVISIBLE I IZ STRING'Z LEN YR \"cats\" MKAY\nVISIBLE I IZ STRING'Z AT YR \"cats\" AN YR 2 MKAY\nKTHXBYE\n")
  (define string-namespace-result (run-source string-namespace-src))
  (check-eq? (hash-ref string-namespace-result 'status) 'ok)
  (check-equal? (hash-ref string-namespace-result 'stdout) "4\nt\n")

  (define leading-btw-src
    "BTW top preamble comment\nHAI 1.3\nVISIBLE \"OK\"\nKTHXBYE\n")
  (define leading-btw-result (run-source leading-btw-src))
  (check-eq? (hash-ref leading-btw-result 'status) 'ok)
  (check-equal? (hash-ref leading-btw-result 'stdout) "OK\n")

  (define literals-src
    "HAI 1.3\nVISIBLE WIN\nVISIBLE FAIL\nVISIBLE NOOB\nKTHXBYE\n")
  (define literals-result (run-source literals-src))
  (check-eq? (hash-ref literals-result 'status) 'ok)
  (check-equal? (hash-ref literals-result 'stdout) "WIN\nFAIL\nNOOB\n")

  (define line-cont-src
    "HAI 1.3\nVISIBLE SMOOSH \"A\" AN ...\n\"B\" MKAY\nKTHXBYE\n")
  (define line-cont-result (run-source line-cont-src))
  (check-eq? (hash-ref line-cont-result 'status) 'ok)
  (check-equal? (hash-ref line-cont-result 'stdout) "AB\n")

  (define block-comment-src
    "HAI 1.3\nVISIBLE \"A\"\nOBTW\nVISIBLE \"B\"\nTLDR\nVISIBLE \"C\"\nKTHXBYE\n")
  (define block-comment-result (run-source block-comment-src))
  (check-eq? (hash-ref block-comment-result 'status) 'ok)
  (check-equal? (hash-ref block-comment-result 'stdout) "A\nC\n")

  (define string-escape-src
    "HAI 1.3\nVISIBLE \"A::B\"\nVISIBLE \"X:>Y\"\nKTHXBYE\n")
  (define string-escape-result (run-source string-escape-src))
  (check-eq? (hash-ref string-escape-result 'status) 'ok)
  (check-equal? (hash-ref string-escape-result 'stdout) "A:B\nX\tY\n")

  (define string-codepoint-escape-src
    "HAI 1.3\nVISIBLE \"A:(263A)Z\"\nKTHXBYE\n")
  (define string-codepoint-escape-result (run-source string-codepoint-escape-src))
  (check-eq? (hash-ref string-codepoint-escape-result 'status) 'ok)
  (check-equal? (hash-ref string-codepoint-escape-result 'stdout)
                (string-append "A" (string (integer->char #x263A)) "Z\n"))

  (define string-literal-colon-src
    "HAI 1.3\nVISIBLE \"GIMME RADIUS:\"\nVISIBLE \":3:)\"\nKTHXBYE\n")
  (define string-literal-colon-result (run-source string-literal-colon-src))
  (check-eq? (hash-ref string-literal-colon-result 'status) 'ok)
  (check-equal? (hash-ref string-literal-colon-result 'stdout) "GIMME RADIUS:\n:3\n\n")

  (define format-string-src
    "HAI 1.3\nI HAS A name ITZ \"Ada\"\nI HAS A n ITZ 42\nVISIBLE \"HI :{name}! #:{ n }\"\nKTHXBYE\n")
  (define format-string-result (run-source format-string-src))
  (check-eq? (hash-ref format-string-result 'status) 'ok)
  (check-equal? (hash-ref format-string-result 'stdout) "HI Ada! #42\n")

  (define format-string-missing-src
    "HAI 1.3\nVISIBLE \"HI :{missing}\"\nKTHXBYE\n")
  (define format-string-missing-result (run-source format-string-missing-src))
  (check-eq? (hash-ref format-string-missing-result 'status) 'runtime-error)
  (check-true (regexp-match? #px"unknown identifier: missing"
                             (hash-ref format-string-missing-result 'error)))

  (define no-it-side-effect-src
    "HAI 1.3\nI HAS A x ITZ 3\nx R 4\nKTHXBYE\n")
  (define no-it-side-effect (run-source no-it-side-effect-src))
  (check-eq? (hash-ref no-it-side-effect 'status) 'ok)
  (check-equal? (hash-ref no-it-side-effect 'last-value) 'NOOB)

  (define loop-scope-src
    "HAI 1.3\nI HAS A msg ITZ \"outer\"\nIM IN YR loop\n  I HAS A msg ITZ \"inner\"\n  GTFO\nIM OUTTA YR loop\nVISIBLE msg\nKTHXBYE\n")
  (define loop-scope-result (run-source loop-scope-src))
  (check-eq? (hash-ref loop-scope-result 'status) 'ok)
  (check-equal? (hash-ref loop-scope-result 'stdout) "outer\n")

  (define return-scope-src
    "HAI 1.3\nI HAS A x ITZ \"outer\"\nHOW IZ I pick\n  I HAS A x ITZ \"inner\"\n  FOUND YR x\nIF U SAY SO\nVISIBLE I IZ pick MKAY\nVISIBLE x\nKTHXBYE\n")
  (define return-scope-result (run-source return-scope-src))
  (check-eq? (hash-ref return-scope-result 'status) 'ok)
  (check-equal? (hash-ref return-scope-result 'stdout) "inner\nouter\n")

  (define method-shadow-src
    "HAI 1.3\nO HAI IM sample\n  I HAS A val ITZ 10\n  HOW IZ I adjust YR val\n    val R SUM OF val AN 1\n    FOUND YR val\n  IF U SAY SO\nKTHX\nVISIBLE sample IZ adjust YR 5 MKAY\nVISIBLE sample'Z val\nKTHXBYE\n")
  (define method-shadow-result (run-source method-shadow-src))
  (check-eq? (hash-ref method-shadow-result 'status) 'ok)
  (check-equal? (hash-ref method-shadow-result 'stdout) "6\n10\n")

  (define bad-object-break-src
    "HAI 1.3\nO HAI IM badobj\n  GTFO\nKTHX\nKTHXBYE\n")
  (define bad-object-break (run-source bad-object-break-src))
  (check-eq? (hash-ref bad-object-break 'status) 'runtime-error)
  (check-true (regexp-match? #px"GTFO used inside object definition badobj"
                             (hash-ref bad-object-break 'error)))

  ;; Unsupported operators should be rejected at compile step and surfaced.
  (define unsupported-op-program
    (program "1.3"
             (list
              (stmt-expr
               (expr-binary "NOPE OF"
                            (expr-number "1")
                            (expr-number "2"))))))
  (define unsupported-op-result
    (run-program unsupported-op-program))
  (check-eq? (hash-ref unsupported-op-result 'status) 'unsupported)
  (check-true (regexp-match? #px"unsupported binary operator"
                             (hash-ref unsupported-op-result 'reason))))
