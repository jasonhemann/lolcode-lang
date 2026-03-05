#lang racket/base

(require rackunit
         "../../src/lolcode/ast.rkt"
         "../../src/lolcode/main.rkt")

(define (run-source source #:input [input ""])
  (parameterize ([current-input-port (open-input-string input)])
    (run-program (parse-program source))))

(module+ test
  (define one-line-minimal-src
    "HAI 1.3, KTHXBYE\n")
  (define one-line-minimal (run-source one-line-minimal-src))
  (check-eq? (hash-ref one-line-minimal 'status) 'ok)
  (check-equal? (hash-ref one-line-minimal 'stdout) "")

  (define duplicate-variable-declare-src
    "HAI 1.3\nI HAS A var ITZ 1\nI HAS A var ITZ 2\nKTHXBYE\n")
  (define duplicate-variable-declare
    (run-source duplicate-variable-declare-src))
  (check-eq? (hash-ref duplicate-variable-declare 'status) 'runtime-error)
  (check-true
   (regexp-match? #px"identifier already declared in this scope: var"
                  (hash-ref duplicate-variable-declare 'error)))

  (define duplicate-function-def-src
    "HAI 1.3\nHOW IZ I f\n  FOUND YR 1\nIF U SAY SO\nHOW IZ I f\n  FOUND YR 2\nIF U SAY SO\nKTHXBYE\n")
  (define duplicate-function-def
    (run-source duplicate-function-def-src))
  (check-eq? (hash-ref duplicate-function-def 'status) 'runtime-error)
  (check-true
   (regexp-match? #px"identifier already declared in this scope: f"
                  (hash-ref duplicate-function-def 'error)))

  (define function-var-namespace-collision-src
    "HAI 1.3\nHOW IZ I var YR stuff\n  FOUND YR stuff\nIF U SAY SO\nI HAS A var ITZ 0\nKTHXBYE\n")
  (define function-var-namespace-collision
    (run-source function-var-namespace-collision-src))
  (check-eq? (hash-ref function-var-namespace-collision 'status) 'runtime-error)
  (check-true
   (regexp-match? #px"identifier already declared in this scope: var"
                  (hash-ref function-var-namespace-collision 'error)))

  (define function-rebound-as-number-src
    "HAI 1.3\nHOW IZ I var YR stuff\n  FOUND YR stuff\nIF U SAY SO\nvar R 0\nVISIBLE var\nKTHXBYE\n")
  (define function-rebound-as-number
    (run-source function-rebound-as-number-src))
  (check-eq? (hash-ref function-rebound-as-number 'status) 'ok)
  (check-equal? (hash-ref function-rebound-as-number 'stdout) "0\n")

  (define r-noob-retains-binding-src
    "HAI 1.3\nI HAS A x ITZ 7\nx R NOOB\nVISIBLE x\nKTHXBYE\n")
  (define r-noob-retains-binding
    (run-source r-noob-retains-binding-src))
  (check-eq? (hash-ref r-noob-retains-binding 'status) 'ok)
  (check-equal? (hash-ref r-noob-retains-binding 'stdout) "NOOB\n")

  (define r-noob-does-not-invalidate-other-reference-src
    "HAI 1.3\nI HAS A one ITZ A BUKKIT\none HAS A val ITZ 42\nI HAS A two ITZ one\none R NOOB\nVISIBLE two'Z val\nKTHXBYE\n")
  (define r-noob-does-not-invalidate-other-reference
    (run-source r-noob-does-not-invalidate-other-reference-src))
  (check-eq? (hash-ref r-noob-does-not-invalidate-other-reference 'status) 'ok)
  (check-equal? (hash-ref r-noob-does-not-invalidate-other-reference 'stdout) "42\n")

  (define primitive-ops-immutable-src
    "HAI 1.3\nI HAS A n ITZ 5\nI HAS A y ITZ \"A\"\nVISIBLE SUM OF n AN 1\nVISIBLE n\nVISIBLE SMOOSH y AN \"B\" MKAY\nVISIBLE y\nKTHXBYE\n")
  (define primitive-ops-immutable
    (run-source primitive-ops-immutable-src))
  (check-eq? (hash-ref primitive-ops-immutable 'status) 'ok)
  (check-equal? (hash-ref primitive-ops-immutable 'stdout) "6\n5\nAB\nA\n")

  (define declare-assign-src
    "HAI 1.3\nI HAS A var\nvar R 3\nVISIBLE var\nKTHXBYE\n")
  (define declare-assign (run-source declare-assign-src))
  (check-eq? (hash-ref declare-assign 'status) 'ok)
  (check-equal? (hash-ref declare-assign 'stdout) "3\n")
  (check-equal? (hash-ref declare-assign 'last-value) 3)

  (define declare-without-article-src
    "HAI 1.3\nI HAS var ITZ 9\nVISIBLE var\nKTHXBYE\n")
  (define declare-without-article
    (run-source declare-without-article-src))
  (check-eq? (hash-ref declare-without-article 'status) 'ok)
  (check-equal? (hash-ref declare-without-article 'stdout) "9\n")

  (define declaration-literal-infers-type-src
    "HAI 1.3\nI HAS A i ITZ 2\nI HAS A f ITZ 2.5\nI HAS A t ITZ WIN\nI HAS A y ITZ \"cat\"\nI HAS A n ITZ NOOB\nI HAS A from_expr ITZ SUM OF 1 AN 2\nVISIBLE i\nVISIBLE f\nVISIBLE t\nVISIBLE y\nVISIBLE n\nVISIBLE from_expr\nKTHXBYE\n")
  (define declaration-literal-infers-type
    (run-source declaration-literal-infers-type-src))
  (check-eq? (hash-ref declaration-literal-infers-type 'status) 'ok)
  (check-equal? (hash-ref declaration-literal-infers-type 'stdout)
                "2\n2.50\nWIN\ncat\nNOOB\n3\n")

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

  (define srs-keyword-name-in-function-arg-src
    "HAI 1.3\nI HAS A kw ITZ \"MKAY\"\nI HAS A SRS kw ITZ 7\nHOW IZ I echo YR x\n  FOUND YR x\nIF U SAY SO\nVISIBLE I IZ echo YR SRS kw MKAY\nKTHXBYE\n")
  (define srs-keyword-name-in-function-arg
    (run-source srs-keyword-name-in-function-arg-src))
  (check-eq? (hash-ref srs-keyword-name-in-function-arg 'status) 'ok)
  (check-equal? (hash-ref srs-keyword-name-in-function-arg 'stdout)
                "7\n")

  (define bukkit-slot-src
    "HAI 1.3\nI HAS A obj ITZ A BUKKIT\nobj HAS A answer ITZ 42\nVISIBLE obj'Z answer\nKTHXBYE\n")
  (define bukkit-slot (run-source bukkit-slot-src))
  (check-eq? (hash-ref bukkit-slot 'status) 'ok)
  (check-equal? (hash-ref bukkit-slot 'stdout) "42\n")

  (define bukkit-slot-update-src
    "HAI 1.3\nI HAS A obj ITZ A BUKKIT\nobj HAS A answer ITZ 41\nobj'Z answer R SUM OF obj'Z answer AN 1\nVISIBLE obj'Z answer\nKTHXBYE\n")
  (define bukkit-slot-update (run-source bukkit-slot-update-src))
  (check-eq? (hash-ref bukkit-slot-update 'status) 'ok)
  (check-equal? (hash-ref bukkit-slot-update 'stdout) "42\n")

  (define bukkit-srs-numeric-slot-src
    "HAI 1.3\nI HAS A obj ITZ A BUKKIT\nobj HAS A SRS 0 ITZ 41\nobj'Z SRS 0 R SUM OF obj'Z SRS 0 AN 1\nVISIBLE obj'Z SRS 0\nKTHXBYE\n")
  (define bukkit-srs-numeric-slot (run-source bukkit-srs-numeric-slot-src))
  (check-eq? (hash-ref bukkit-srs-numeric-slot 'status) 'ok)
  (check-equal? (hash-ref bukkit-srs-numeric-slot 'stdout) "42\n")

  (define bukkit-slot-redeclare-overwrite-src
    "HAI 1.3\nI HAS A obj ITZ A BUKKIT\nobj HAS A answer ITZ 1\nobj HAS A answer ITZ 2\nVISIBLE obj'Z answer\nKTHXBYE\n")
  (define bukkit-slot-redeclare-overwrite
    (run-source bukkit-slot-redeclare-overwrite-src))
  (check-eq? (hash-ref bukkit-slot-redeclare-overwrite 'status) 'ok)
  (check-equal? (hash-ref bukkit-slot-redeclare-overwrite 'stdout) "2\n")

  (define slot-declare-a-only-src
    "HAI 1.3\nI HAS AN obj ITZ A BUKKIT\nobj HAS A elem ITZ \"catmium\"\nobj HAS A empty\nVISIBLE obj'Z elem\nVISIBLE obj'Z empty\nKTHXBYE\n")
  (define slot-declare-a-only (run-source slot-declare-a-only-src))
  (check-eq? (hash-ref slot-declare-a-only 'status) 'ok)
  (check-equal? (hash-ref slot-declare-a-only 'stdout) "catmium\nNOOB\n")

  (define clone-like-src
    "HAI 1.3\nI HAS A parent ITZ A BUKKIT\nparent HAS A val ITZ 1\nI HAS A child ITZ LIEK A parent\nchild'Z val R 2\nVISIBLE parent'Z val\nVISIBLE child'Z val\nKTHXBYE\n")
  (define clone-like (run-source clone-like-src))
  (check-eq? (hash-ref clone-like 'status) 'ok)
  (check-equal? (hash-ref clone-like 'stdout) "1\n2\n")

  (define switch-src
    "HAI 1.3\nI HAS A color ITZ \"G\"\ncolor, WTF?\n  OMG \"R\"\n    VISIBLE \"RED FISH\"\n    GTFO\n  OMG \"Y\"\n    VISIBLE \"YELLOW FISH\"\n  OMG \"G\"\n  OMG \"B\"\n    VISIBLE \"FISH HAS A FLAVOR\"\n    GTFO\n  OMGWTF\n    VISIBLE \"FISH IS TRANSPARENT\"\nOIC\nKTHXBYE\n")
  (define switch-result (run-source switch-src))
  (check-eq? (hash-ref switch-result 'status) 'ok)
  (check-equal? (hash-ref switch-result 'stdout) "FISH HAS A FLAVOR\n")

  (define switch-duplicate-src
    "HAI 1.3\nI HAS A x ITZ 1\nx, WTF?\n  OMG 1\n    VISIBLE \"A\"\n  OMG 1\n    VISIBLE \"B\"\nOIC\nKTHXBYE\n")
  (check-exn #px"duplicate OMG literal in WTF\\?"
             (lambda () (parse-program switch-duplicate-src)))

  (define switch-literal-escaped-placeholder-src
    "HAI 1.3\nI HAS A n ITZ \"n\"\nI HAS A probe ITZ \"::{n}\"\nprobe, WTF?\n  OMG \"::{n}\"\n    VISIBLE \"LIT\"\n    GTFO\n  OMGWTF\n    VISIBLE \"MISS\"\nOIC\nKTHXBYE\n")
  (define switch-literal-escaped-placeholder
    (run-source switch-literal-escaped-placeholder-src))
  (check-eq? (hash-ref switch-literal-escaped-placeholder 'status) 'ok)
  (check-equal? (hash-ref switch-literal-escaped-placeholder 'stdout) "LIT\n")

  (define switch-runtime-error-propagates-src
    "HAI 1.3\n1, WTF?\n  OMG 1\n    SUM OF NOOB AN 1\n  OMGWTF\n    VISIBLE \"BAD\"\nOIC\nVISIBLE \"AFTER\"\nKTHXBYE\n")
  (define switch-runtime-error-propagates
    (run-source switch-runtime-error-propagates-src))
  (check-eq? (hash-ref switch-runtime-error-propagates 'status) 'runtime-error)
  (check-equal? (hash-ref switch-runtime-error-propagates 'stdout) "")
  (check-true (regexp-match? #px"cannot cast NOOB to numeric value"
                             (hash-ref switch-runtime-error-propagates 'error)))

  (define switch-empty-omg-fallthrough-src
    "HAI 1.3\n1, WTF?\n  OMG 1\n  OMG 2\n    VISIBLE \"FALL\"\n    GTFO\n  OMGWTF\n    VISIBLE \"BAD\"\nOIC\nKTHXBYE\n")
  (define switch-empty-omg-fallthrough
    (run-source switch-empty-omg-fallthrough-src))
  (check-eq? (hash-ref switch-empty-omg-fallthrough 'status) 'ok)
  (check-equal? (hash-ref switch-empty-omg-fallthrough 'stdout) "FALL\n")

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

  (define function-void-return-src
    "HAI 1.3\nHOW IZ I fun1\n  \"a\"\nIF U SAY SO\nHOW IZ I fun2 YR arg\n  arg\nIF U SAY SO\nVISIBLE I IZ fun1 MKAY\nVISIBLE I IZ fun2 YR \"b\" MKAY\nKTHXBYE\n")
  (define function-void-return (run-source function-void-return-src))
  (check-eq? (hash-ref function-void-return 'status) 'ok)
  (check-equal? (hash-ref function-void-return 'stdout) "a\nb\n")

  (define function-gtfo-return-src
    "HAI 1.3\nHOW IZ I quitfast\n  GTFO\nIF U SAY SO\nVISIBLE I IZ quitfast MKAY\nKTHXBYE\n")
  (define function-gtfo-return (run-source function-gtfo-return-src))
  (check-eq? (hash-ref function-gtfo-return 'status) 'ok)
  (check-equal? (hash-ref function-gtfo-return 'stdout) "NOOB\n")

  (define function-switch-gtfo-scope-src
    "HAI 1.3\nHOW IZ I choose\n  I HAS A out ITZ \"ok\"\n  1, WTF?\n    OMG 1\n      GTFO\n    OMGWTF\n      out R \"bad\"\n  OIC\n  FOUND YR out\nIF U SAY SO\nVISIBLE I IZ choose MKAY\nKTHXBYE\n")
  (define function-switch-gtfo-scope
    (run-source function-switch-gtfo-scope-src))
  (check-eq? (hash-ref function-switch-gtfo-scope 'status) 'ok)
  ;; Regression: GTFO in switch must break switch, not return from function.
  (check-equal? (hash-ref function-switch-gtfo-scope 'stdout) "ok\n")

  (define function-switch-found-return-src
    "HAI 1.3\nHOW IZ I classify YR x\n  x, WTF?\n    OMG 2\n      FOUND YR \"two\"\n    OMGWTF\n      FOUND YR \"other\"\n  OIC\n  FOUND YR \"bad\"\nIF U SAY SO\nVISIBLE I IZ classify YR 2 MKAY\nVISIBLE I IZ classify YR 9 MKAY\nKTHXBYE\n")
  (define function-switch-found-return
    (run-source function-switch-found-return-src))
  (check-eq? (hash-ref function-switch-found-return 'status) 'ok)
  ;; Regression: FOUND YR inside nested switch must escape whole function.
  (check-equal? (hash-ref function-switch-found-return 'stdout) "two\nother\n")

  (define function-outer-scope-src
    "HAI 1.3\nI HAS A outside ITZ 9\nHOW IZ I reach\n  FOUND YR outside\nIF U SAY SO\nVISIBLE I IZ reach MKAY\nKTHXBYE\n")
  (define function-outer-scope (run-source function-outer-scope-src))
  (check-eq? (hash-ref function-outer-scope 'status) 'ok)
  (check-equal? (hash-ref function-outer-scope 'stdout) "9\n")

  (define function-it-reset-src
    "HAI 1.3\nHOW IZ I peek\n  FOUND YR IT\nIF U SAY SO\nVISIBLE I IZ peek MKAY\nSUM OF 1 AN 2\nVISIBLE I IZ peek MKAY\nKTHXBYE\n")
  (define function-it-reset (run-source function-it-reset-src))
  (check-eq? (hash-ref function-it-reset 'status) 'ok)
  ;; Regression: function call frames must initialize IT independently.
  (check-equal? (hash-ref function-it-reset 'stdout) "NOOB\nNOOB\n")

  (define it-local-main-and-function-src
    "HAI 1.3\nSUM OF 1 AN 2\nHOW IZ I check\n  VISIBLE IT\n  SUM OF 4 AN 5\n  FOUND YR IT\nIF U SAY SO\nI HAS A r ITZ I IZ check MKAY\nVISIBLE IT\nVISIBLE r\nKTHXBYE\n")
  (define it-local-main-and-function
    (run-source it-local-main-and-function-src))
  (check-eq? (hash-ref it-local-main-and-function 'status) 'ok)
  (check-equal? (hash-ref it-local-main-and-function 'stdout) "NOOB\n3\n9\n")

  (define method-it-global-lookup-src
    "HAI 1.3\nSUM OF 1 AN 2\nO HAI IM obj\n  HOW IZ I bump\n    SUM OF IT AN 1\n    FOUND YR IT\n  IF U SAY SO\nKTHX\nSUM OF 1 AN 2\nI HAS A r ITZ obj IZ bump MKAY\nVISIBLE r\nVISIBLE IT\nKTHXBYE\n")
  (define method-it-global-lookup
    (run-source method-it-global-lookup-src))
  (check-eq? (hash-ref method-it-global-lookup 'status) 'ok)
  (check-equal? (hash-ref method-it-global-lookup 'stdout) "4\n4\n")

  (define expr-stmt-src
    "HAI 1.3\nHOW IZ I ping\n  VISIBLE \"P\"\nIF U SAY SO\nI IZ ping MKAY\nKTHXBYE\n")
  (define expr-stmt-result (run-source expr-stmt-src))
  (check-eq? (hash-ref expr-stmt-result 'status) 'ok)
  (check-equal? (hash-ref expr-stmt-result 'stdout) "P\n")

  (define expr-slot-to-it-orly-src
    "HAI 1.3\nI HAS A obj ITZ A BUKKIT\nobj HAS A alive ITZ WIN\nobj'Z alive\nO RLY?\n  YA RLY\n    VISIBLE \"Y\"\n  NO WAI\n    VISIBLE \"N\"\nOIC\nKTHXBYE\n")
  (define expr-slot-to-it-orly-result
    (run-source expr-slot-to-it-orly-src))
  (check-eq? (hash-ref expr-slot-to-it-orly-result 'status) 'ok)
  (check-equal? (hash-ref expr-slot-to-it-orly-result 'stdout) "Y\n")

  (define expr-slot-to-it-orly-inline-src
    "HAI 1.3\nI HAS A obj ITZ A BUKKIT\nobj HAS A alive ITZ WIN\nobj'Z alive, O RLY?, YA RLY, VISIBLE \"Y\", NO WAI, VISIBLE \"N\", OIC\nKTHXBYE\n")
  (define expr-slot-to-it-orly-inline-result
    (run-source expr-slot-to-it-orly-inline-src))
  (check-eq? (hash-ref expr-slot-to-it-orly-inline-result 'status) 'ok)
  (check-equal? (hash-ref expr-slot-to-it-orly-inline-result 'stdout) "Y\n")

  (define orly-uses-implicit-it-src
    "HAI 1.3\nI HAS A itflag ITZ WIN\nBOTH SAEM 1 AN 2\nO RLY?\n  YA RLY\n    VISIBLE \"Y\"\n  NO WAI\n    VISIBLE \"N\"\nOIC\nKTHXBYE\n")
  (define orly-uses-implicit-it
    (run-source orly-uses-implicit-it-src))
  (check-eq? (hash-ref orly-uses-implicit-it 'status) 'ok)
  (check-equal? (hash-ref orly-uses-implicit-it 'stdout) "N\n")

  (define orly-assignment-does-not-reset-it-src
    "HAI 1.3\nWIN\nI HAS A x ITZ 0\nx R 1\nO RLY?\n  YA RLY\n    VISIBLE \"Y\"\n  NO WAI\n    VISIBLE \"N\"\nOIC\nKTHXBYE\n")
  (define orly-assignment-does-not-reset-it
    (run-source orly-assignment-does-not-reset-it-src))
  (check-eq? (hash-ref orly-assignment-does-not-reset-it 'status) 'ok)
  (check-equal? (hash-ref orly-assignment-does-not-reset-it 'stdout) "Y\n")

  (define orly-mebbe-first-match-wins-src
    "HAI 1.3\nFAIL\nO RLY?\n  YA RLY\n    VISIBLE \"Y\"\n  MEBBE WIN\n    VISIBLE \"A\"\n  MEBBE WIN\n    VISIBLE \"B\"\n  NO WAI\n    VISIBLE \"C\"\nOIC\nKTHXBYE\n")
  (define orly-mebbe-first-match-wins
    (run-source orly-mebbe-first-match-wins-src))
  (check-eq? (hash-ref orly-mebbe-first-match-wins 'status) 'ok)
  (check-equal? (hash-ref orly-mebbe-first-match-wins 'stdout) "A\n")

  (define orly-mebbe-truthy-cast-src
    "HAI 1.3\nFAIL\nO RLY?\n  YA RLY\n    VISIBLE \"Y\"\n  MEBBE 3\n    VISIBLE \"M\"\n  NO WAI\n    VISIBLE \"N\"\nOIC\nKTHXBYE\n")
  (define orly-mebbe-truthy-cast
    (run-source orly-mebbe-truthy-cast-src))
  (check-eq? (hash-ref orly-mebbe-truthy-cast 'status) 'ok)
  ;; Regression/policy: MEBBE condition is evaluated with TROOF truthiness semantics.
  (check-equal? (hash-ref orly-mebbe-truthy-cast 'stdout) "M\n")

  (define orly-no-wai-optional-src
    "HAI 1.3\nFAIL\nO RLY?\n  YA RLY\n    VISIBLE \"Y\"\nOIC\nVISIBLE \"Z\"\nKTHXBYE\n")
  (define orly-no-wai-optional
    (run-source orly-no-wai-optional-src))
  (check-eq? (hash-ref orly-no-wai-optional 'status) 'ok)
  (check-equal? (hash-ref orly-no-wai-optional 'stdout) "Z\n")

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

  (define object-alt-dynamic-name-src
    "HAI 1.3\nI HAS A objname ITZ \"pokeman\"\nO HAI IM SRS objname\n  I HAS A name ITZ \"pikachu\"\nKTHX\nVISIBLE pokeman'Z name\nKTHXBYE\n")
  (define object-alt-dynamic-name (run-source object-alt-dynamic-name-src))
  (check-eq? (hash-ref object-alt-dynamic-name 'status) 'ok)
  (check-equal? (hash-ref object-alt-dynamic-name 'stdout) "pikachu\n")

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

  (define inherited-object-dynamic-parent-src
    "HAI 1.3\nI HAS A pname ITZ \"parent\"\nI HAS A cname ITZ \"child\"\nO HAI IM SRS pname\n  I HAS A name ITZ \"pikachu\"\nKTHX\nO HAI IM SRS cname IM LIEK SRS pname\nKTHX\nVISIBLE child'Z name\nKTHXBYE\n")
  (define inherited-object-dynamic-parent
    (run-source inherited-object-dynamic-parent-src))
  (check-eq? (hash-ref inherited-object-dynamic-parent 'status) 'ok)
  (check-equal? (hash-ref inherited-object-dynamic-parent 'stdout) "pikachu\n")

  (define loop-src
    "HAI 1.3\nI HAS A idx ITZ 0\nI HAS A acc ITZ 0\nIM IN YR count UPPIN YR idx TIL BOTH SAEM idx AN 5\n  acc R SUM OF acc AN idx\nIM OUTTA YR count\nVISIBLE acc\nKTHXBYE\n")
  (define loop-result (run-source loop-src))
  (check-eq? (hash-ref loop-result 'status) 'ok)
  (check-equal? (hash-ref loop-result 'stdout) "10\n")

  (define loop-dynamic-label-src
    "HAI 1.3\nI HAS A loopname ITZ \"lp\"\nI HAS A i ITZ 0\nIM IN YR SRS loopname UPPIN YR i TIL BOTH SAEM i AN 3\n  VISIBLE i\nIM OUTTA YR SRS loopname\nKTHXBYE\n")
  (define loop-dynamic-label (run-source loop-dynamic-label-src))
  (check-eq? (hash-ref loop-dynamic-label 'status) 'ok)
  (check-equal? (hash-ref loop-dynamic-label 'stdout) "0\n1\n2\n")

  (define loop-dynamic-label-mismatch-src
    "HAI 1.3\nI HAS A open ITZ \"lp\"\nI HAS A close ITZ \"oops\"\nIM IN YR SRS open\n  GTFO\nIM OUTTA YR SRS close\nKTHXBYE\n")
  (define loop-dynamic-label-mismatch
    (run-source loop-dynamic-label-mismatch-src))
  (check-eq? (hash-ref loop-dynamic-label-mismatch 'status) 'runtime-error)
  (check-true (regexp-match? #px"loop label mismatch"
                             (hash-ref loop-dynamic-label-mismatch 'error)))

  (define loop-counter-scope-src
    "HAI 1.3\nI HAS A ctr ITZ 5\nIM IN YR lp UPPIN YR ctr WILE DIFFRINT ctr AN 10\n  VISIBLE ctr\nIM OUTTA YR lp\nVISIBLE ctr\nKTHXBYE\n")
  (define loop-counter-scope-result (run-source loop-counter-scope-src))
  (check-eq? (hash-ref loop-counter-scope-result 'status) 'ok)
  (check-equal? (hash-ref loop-counter-scope-result 'stdout) "5\n6\n7\n8\n9\n5\n")

  (define loop-counter-dynamic-name-src
    "HAI 1.3\nI HAS A vname ITZ \"ctr\"\nI HAS A ctr ITZ 5\nIM IN YR lp UPPIN YR SRS vname WILE DIFFRINT ctr AN 10\n  VISIBLE ctr\nIM OUTTA YR lp\nVISIBLE ctr\nKTHXBYE\n")
  (define loop-counter-dynamic-name-result
    (run-source loop-counter-dynamic-name-src))
  (check-eq? (hash-ref loop-counter-dynamic-name-result 'status) 'ok)
  (check-equal? (hash-ref loop-counter-dynamic-name-result 'stdout) "5\n6\n7\n8\n9\n5\n")

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

  (define switch-break-inside-loop-src
    "HAI 1.3\nI HAS A i ITZ 0\nI HAS A out ITZ \"\"\nIM IN YR lp UPPIN YR i TIL BOTH SAEM i AN 3\n  i, WTF?\n    OMG 1\n      out R SMOOSH out AN \"A\" MKAY\n      GTFO\n    OMGWTF\n      out R SMOOSH out AN \"B\" MKAY\n  OIC\nIM OUTTA YR lp\nVISIBLE out\nKTHXBYE\n")
  (define switch-break-inside-loop
    (run-source switch-break-inside-loop-src))
  (check-eq? (hash-ref switch-break-inside-loop 'status) 'ok)
  ;; Regression: GTFO from switch must not break enclosing loop.
  (check-equal? (hash-ref switch-break-inside-loop 'stdout) "BAB\n")

  (define loop-unary-updater-src
    "HAI 1.3\nHOW IZ I plustwoin YR var\n  FOUND YR SUM OF var AN 2\nIF U SAY SO\nIM IN YR loop I IZ plustwoin YR var MKAY\n  VISIBLE var\n  BOTH SAEM var AN 10\n  O RLY?\n    YA RLY\n      GTFO\n  OIC\nIM OUTTA YR loop\nKTHXBYE\n")
  (define loop-unary-updater (run-source loop-unary-updater-src))
  (check-eq? (hash-ref loop-unary-updater 'status) 'ok)
  (check-equal? (hash-ref loop-unary-updater 'stdout) "0\n2\n4\n6\n8\n10\n")

  (define logic-src
    "HAI 1.3\nI HAS A n ITZ 42\nVISIBLE BOTH OF DIFFRINT n AN 0 AN DIFFRINT n AN 42\nVISIBLE EITHER OF BOTH SAEM n AN 0 AN BOTH SAEM n AN 42\nVISIBLE WON OF BOTH SAEM n AN 42 AN BOTH SAEM n AN 0\nVISIBLE ALL OF DIFFRINT n AN 0 AN NOT BOTH SAEM n AN 0 MKAY\nVISIBLE ANY OF BOTH SAEM n AN 0 AN BOTH SAEM n AN 42 MKAY\nKTHXBYE\n")
  (define logic-result (run-source logic-src))
  (check-eq? (hash-ref logic-result 'status) 'ok)
  (check-equal? (hash-ref logic-result 'stdout) "FAIL\nWIN\nWIN\nWIN\nWIN\n")

  (define binary-ops-optional-an-src
    "HAI 1.3\nVISIBLE SUM OF 1 2\nVISIBLE DIFF OF 5 2\nVISIBLE PRODUKT OF 3 4\nVISIBLE QUOSHUNT OF 6 2\nVISIBLE MOD OF 7 4\nVISIBLE BIGGR OF 5 2\nVISIBLE SMALLR OF 5 2\nVISIBLE BOTH OF WIN FAIL\nVISIBLE EITHER OF FAIL WIN\nVISIBLE WON OF WIN FAIL\nVISIBLE BOTH SAEM 3 3\nVISIBLE DIFFRINT 3 4\nKTHXBYE\n")
  (define binary-ops-optional-an
    (run-source binary-ops-optional-an-src))
  (check-eq? (hash-ref binary-ops-optional-an 'status) 'ok)
  (check-equal? (hash-ref binary-ops-optional-an 'stdout)
                "3\n3\n12\n3\n3\n5\n2\nFAIL\nWIN\nWIN\nWIN\nWIN\n")

  (define equality-no-implicit-cast-src
    "HAI 1.3\nVISIBLE BOTH SAEM \"3\" AN 3\nVISIBLE DIFFRINT \"3\" AN 3\nVISIBLE BOTH SAEM MAEK \"3\" A NUMBR AN 3\nKTHXBYE\n")
  (define equality-no-implicit-cast
    (run-source equality-no-implicit-cast-src))
  (check-eq? (hash-ref equality-no-implicit-cast 'status) 'ok)
  (check-equal? (hash-ref equality-no-implicit-cast 'stdout)
                "FAIL\nWIN\nWIN\n")

  (define equality-numbr-numbar-numeric-mode-src
    "HAI 1.3\nI HAS A i ITZ 3\nI HAS A f ITZ MAEK 3 A NUMBAR\nVISIBLE BOTH SAEM i AN f\nVISIBLE DIFFRINT i AN MAEK \"3.1\" A NUMBAR\nKTHXBYE\n")
  (define equality-numbr-numbar-numeric-mode
    (run-source equality-numbr-numbar-numeric-mode-src))
  (check-eq? (hash-ref equality-numbr-numbar-numeric-mode 'status) 'ok)
  (check-equal? (hash-ref equality-numbr-numbar-numeric-mode 'stdout)
                "WIN\nWIN\n")

  (define logic-all-of-src
    "HAI 1.3\nI HAS A flag ITZ WIN\nI HAS A anotherflag ITZ FAIL\nI HAS A flag3 ITZ WIN\nI HAS A flag4 ITZ WIN\nI HAS A flag5\nflag5 R ALL OF flag AN anotherflag AN flag3 AN flag4 MKAY\nVISIBLE flag5\nKTHXBYE\n")
  (define logic-all-of-result (run-source logic-all-of-src))
  (check-eq? (hash-ref logic-all-of-result 'status) 'ok)
  (check-equal? (hash-ref logic-all-of-result 'stdout) "FAIL\n")

  (define nested-variadic-closure-src
    "HAI 1.3\nVISIBLE ALL OF WIN AN ANY OF FAIL AN WIN\nVISIBLE ALL OF WIN AN ANY OF FAIL AN WIN MKAY\nVISIBLE ALL OF WIN AN ...\nANY OF FAIL AN WIN MKAY\nVISIBLE ALL OF WIN AN ANY OF FAIL AN WIN MKAY, VISIBLE \"X\"\nKTHXBYE\n")
  (define nested-variadic-closure-result
    (run-source nested-variadic-closure-src))
  (check-eq? (hash-ref nested-variadic-closure-result 'status) 'ok)
  ;; EOL/comma must close any remaining open variadics (stack order).
  (check-equal? (hash-ref nested-variadic-closure-result 'stdout)
                "WIN\nWIN\nWIN\nWIN\nX\n")

  (define cast-src
    "HAI 1.3\nI HAS A obj ITZ A BUKKIT\nobj HAS A answer ITZ \"41\"\nobj'Z answer IS NOW A NUMBR\nobj'Z answer R SUM OF obj'Z answer AN 1\nVISIBLE obj'Z answer\nKTHXBYE\n")
  (define cast-result (run-source cast-src))
  (check-eq? (hash-ref cast-result 'status) 'ok)
  (check-equal? (hash-ref cast-result 'stdout) "42\n")

  (define maek-local-cast-does-not-mutate-var-src
    "HAI 1.3\nI HAS A foo ITZ MAEK \"2.5\" A NUMBAR\nI HAS A bar ITZ MAEK foo A NUMBR\nVISIBLE foo\nVISIBLE bar\nKTHXBYE\n")
  (define maek-local-cast-does-not-mutate-var
    (run-source maek-local-cast-does-not-mutate-var-src))
  (check-eq? (hash-ref maek-local-cast-does-not-mutate-var 'status) 'ok)
  (check-equal? (hash-ref maek-local-cast-does-not-mutate-var 'stdout)
                "2.50\n2\n")

  (define maek-local-cast-does-not-mutate-slot-src
    "HAI 1.3\nI HAS A obj ITZ A BUKKIT\nobj HAS A raw ITZ \"41\"\nI HAS A casted ITZ MAEK obj'Z raw A NUMBR\nVISIBLE obj'Z raw\nVISIBLE casted\nKTHXBYE\n")
  (define maek-local-cast-does-not-mutate-slot
    (run-source maek-local-cast-does-not-mutate-slot-src))
  (check-eq? (hash-ref maek-local-cast-does-not-mutate-slot 'status) 'ok)
  (check-equal? (hash-ref maek-local-cast-does-not-mutate-slot 'stdout)
                "41\n41\n")

  (define cast-relaxed-number-yarn-src
    "HAI 1.3\nVISIBLE MAEK \" 123\" A NUMBR\nKTHXBYE\n")
  (define cast-relaxed-number-yarn
    (run-source cast-relaxed-number-yarn-src))
  (check-eq? (hash-ref cast-relaxed-number-yarn 'status) 'runtime-error)
  (check-true (regexp-match? #px"cannot cast YARN to numeric value"
                             (hash-ref cast-relaxed-number-yarn 'error)))

  (define cast-scientific-number-yarn-src
    "HAI 1.3\nVISIBLE MAEK \"1e2\" A NUMBAR\nKTHXBYE\n")
  (define cast-scientific-number-yarn
    (run-source cast-scientific-number-yarn-src))
  (check-eq? (hash-ref cast-scientific-number-yarn 'status) 'runtime-error)
  (check-true (regexp-match? #px"cannot cast YARN to numeric value"
                             (hash-ref cast-scientific-number-yarn 'error)))

  (define maek-without-article-src
    "HAI 1.3\nVISIBLE MAEK 2 NUMBAR\nKTHXBYE\n")
  (define maek-without-article
    (run-source maek-without-article-src))
  (check-eq? (hash-ref maek-without-article 'status) 'ok)
  (check-equal? (hash-ref maek-without-article 'stdout) "2.00\n")

  (define noob-arithmetic-src
    "HAI 1.3\nVISIBLE SUM OF NOOB AN 1\nKTHXBYE\n")
  (define noob-arithmetic-result
    (run-source noob-arithmetic-src))
  (check-eq? (hash-ref noob-arithmetic-result 'status) 'runtime-error)
  (check-true (regexp-match? #px"cannot cast NOOB to numeric value"
                             (hash-ref noob-arithmetic-result 'error)))

  (define type-literals-cast-to-troof-src
    "HAI 1.3\nVISIBLE MAEK TYPE A TROOF\nVISIBLE MAEK NOOB A TROOF\nKTHXBYE\n")
  (define type-literals-cast-to-troof
    (run-source type-literals-cast-to-troof-src))
  (check-eq? (hash-ref type-literals-cast-to-troof 'status) 'ok)
  (check-equal? (hash-ref type-literals-cast-to-troof 'stdout) "WIN\nFAIL\n")

  (define type-literal-domain-casts-src
    "HAI 1.3\nVISIBLE MAEK TROOF A YARN\nVISIBLE MAEK NOOB A YARN\nVISIBLE MAEK NUMBR A YARN\nVISIBLE MAEK NUMBAR A YARN\nVISIBLE MAEK YARN A YARN\nVISIBLE MAEK TYPE A YARN\nVISIBLE MAEK TROOF A TROOF\nVISIBLE MAEK NOOB A TROOF\nVISIBLE MAEK NUMBR A TROOF\nVISIBLE MAEK NUMBAR A TROOF\nVISIBLE MAEK YARN A TROOF\nVISIBLE MAEK TYPE A TROOF\nKTHXBYE\n")
  (define type-literal-domain-casts
    (run-source type-literal-domain-casts-src))
  (check-eq? (hash-ref type-literal-domain-casts 'status) 'ok)
  (check-equal? (hash-ref type-literal-domain-casts 'stdout)
                "TROOF\nNOOB\nNUMBR\nNUMBAR\nYARN\nTYPE\nWIN\nFAIL\nWIN\nWIN\nWIN\nWIN\n")

  (define numbar-visible-format-src
    "HAI 1.3\nVISIBLE MAEK \"3.14159\" A NUMBAR\nVISIBLE MAEK 2 A NUMBAR\nVISIBLE MAEK \"-1.239\" A NUMBAR\nKTHXBYE\n")
  (define numbar-visible-format-result
    (run-source numbar-visible-format-src))
  (check-eq? (hash-ref numbar-visible-format-result 'status) 'ok)
  ;; Spec: NUMBAR printed as YARN defaults to two decimal places (truncated).
  (check-equal? (hash-ref numbar-visible-format-result 'stdout)
                "3.14\n2.00\n-1.23\n")

  (define numbar-to-numbr-truncate-src
    "HAI 1.3\nVISIBLE MAEK \"-0.567\" A NUMBR\nVISIBLE MAEK \"-1.239\" A NUMBR\nVISIBLE MAEK \"1.999\" A NUMBR\nKTHXBYE\n")
  (define numbar-to-numbr-truncate-result
    (run-source numbar-to-numbr-truncate-src))
  (check-eq? (hash-ref numbar-to-numbr-truncate-result 'status) 'ok)
  ;; Spec truncation is toward zero for both positive and negative values.
  (check-equal? (hash-ref numbar-to-numbr-truncate-result 'stdout)
                "0\n-1\n1\n")

  (define method-src
    "HAI 1.3\nO HAI IM counter\n  I HAS A val ITZ 1\n  HOW IZ I bump YR delta\n    val R SUM OF val AN delta\n    FOUND YR val\n  IF U SAY SO\nKTHX\nVISIBLE counter IZ bump YR 2 MKAY\nVISIBLE counter IZ bump YR 3 MKAY\nVISIBLE counter'Z val\nKTHXBYE\n")
  (define method-result (run-source method-src))
  (check-eq? (hash-ref method-result 'status) 'ok)
  (check-equal? (hash-ref method-result 'stdout) "3\n6\n6\n")

  (define method-alt-def-src
    "HAI 1.3\nI HAS A foo ITZ A BUKKIT\nfoo HAS A bar ITZ 123\nHOW IZ foo fun1\n  FOUND YR ME'Z bar\nIF U SAY SO\nVISIBLE I IZ foo'Z fun1 MKAY\nKTHXBYE\n")
  (define method-alt-def (run-source method-alt-def-src))
  (check-eq? (hash-ref method-alt-def 'status) 'ok)
  (check-equal? (hash-ref method-alt-def 'stdout) "123\n")

  (define method-nested-receiver-def-src
    "HAI 1.3\nI HAS A foo ITZ A BUKKIT\nfoo HAS A var1 ITZ A BUKKIT\nHOW IZ foo'Z var1 fun1\n  VISIBLE \"i\"\nIF U SAY SO\nI IZ foo'Z var1'Z fun1 MKAY\nKTHXBYE\n")
  (define method-nested-receiver-def
    (run-source method-nested-receiver-def-src))
  (check-eq? (hash-ref method-nested-receiver-def 'status) 'ok)
  (check-equal? (hash-ref method-nested-receiver-def 'stdout) "i\n")

  (define method-alt-call-syntax-src
    "HAI 1.3\nI HAS A foo ITZ A BUKKIT\nfoo HAS A bar ITZ 10\nHOW IZ foo inc\n  ME'Z bar R SUM OF ME'Z bar AN 1\nIF U SAY SO\nfoo IZ inc MKAY\nVISIBLE foo'Z bar\nKTHXBYE\n")
  (define method-alt-call-syntax (run-source method-alt-call-syntax-src))
  (check-eq? (hash-ref method-alt-call-syntax 'status) 'ok)
  (check-equal? (hash-ref method-alt-call-syntax 'stdout) "11\n")

  (define method-alt-call-dynamic-name-src
    "HAI 1.3\nI HAS A foo ITZ A BUKKIT\nfoo HAS A bar ITZ 10\nHOW IZ foo inc\n  ME'Z bar R SUM OF ME'Z bar AN 1\nIF U SAY SO\nI HAS A m ITZ \"inc\"\nfoo IZ SRS m MKAY\nVISIBLE foo'Z bar\nKTHXBYE\n")
  (define method-alt-call-dynamic-name
    (run-source method-alt-call-dynamic-name-src))
  (check-eq? (hash-ref method-alt-call-dynamic-name 'status) 'ok)
  (check-equal? (hash-ref method-alt-call-dynamic-name 'stdout) "11\n")

  (define method-call-missing-slot-src
    "HAI 1.3\nI HAS A foo ITZ A BUKKIT\nfoo IZ nope MKAY\nKTHXBYE\n")
  (define method-call-missing-slot
    (run-source method-call-missing-slot-src))
  (check-eq? (hash-ref method-call-missing-slot 'status) 'runtime-error)
  (check-true (regexp-match? #px"unknown method: nope"
                             (hash-ref method-call-missing-slot 'error)))

  (define method-call-noncallable-slot-src
    "HAI 1.3\nI HAS A foo ITZ A BUKKIT\nfoo HAS A nope ITZ 42\nfoo IZ nope MKAY\nKTHXBYE\n")
  (define method-call-noncallable-slot
    (run-source method-call-noncallable-slot-src))
  (check-eq? (hash-ref method-call-noncallable-slot 'status) 'runtime-error)
  (check-true (regexp-match? #px"unknown method: nope"
                             (hash-ref method-call-noncallable-slot 'error)))

  (define missing-slot-default-omgwtf-src
    "HAI 1.3\nI HAS A foo ITZ A BUKKIT\nVISIBLE foo'Z nope\nKTHXBYE\n")
  (define missing-slot-default-omgwtf
    (run-source missing-slot-default-omgwtf-src))
  (check-eq? (hash-ref missing-slot-default-omgwtf 'status) 'runtime-error)
  (check-true (regexp-match? #px"unknown slot: nope"
                             (hash-ref missing-slot-default-omgwtf 'error)))

  (define custom-omgwtf-on-missing-slot-src
    "HAI 1.3\nO HAI IM box\n  HOW IZ I omgwtf YR slotname\n    FOUND YR SMOOSH \"made-\" AN slotname MKAY\n  IF U SAY SO\nKTHX\nVISIBLE box'Z nope\nVISIBLE box'Z nope\nKTHXBYE\n")
  (define custom-omgwtf-on-missing-slot
    (run-source custom-omgwtf-on-missing-slot-src))
  (check-eq? (hash-ref custom-omgwtf-on-missing-slot 'status) 'ok)
  (check-equal? (hash-ref custom-omgwtf-on-missing-slot 'stdout)
                "made-nope\nmade-nope\n")

  (define omgwtf-memoizes-missing-slot-src
    "HAI 1.3\nO HAI IM box\n  I HAS A hits ITZ 0\n  HOW IZ I omgwtf YR slotname\n    hits R SUM OF hits AN 1\n    FOUND YR hits\n  IF U SAY SO\nKTHX\nVISIBLE box'Z nope\nVISIBLE box'Z nope\nVISIBLE box'Z hits\nKTHXBYE\n")
  (define omgwtf-memoizes-missing-slot
    (run-source omgwtf-memoizes-missing-slot-src))
  (check-eq? (hash-ref omgwtf-memoizes-missing-slot 'status) 'ok)
  ;; Regression: missing slot is cached after omgwtf synthesizes a value.
  (check-equal? (hash-ref omgwtf-memoizes-missing-slot 'stdout)
                "1\n1\n1\n")

  (define izmakin-special-slot-runs-on-prototype-src
    "HAI 1.3\nO HAI IM Maker\n  I HAS A seed ITZ 1\n  HOW IZ I izmakin\n    seed R SUM OF seed AN 1\n  IF U SAY SO\nKTHX\nI HAS A first ITZ LIEK A Maker\nI HAS A second ITZ LIEK A Maker\nVISIBLE first'Z seed\nVISIBLE second'Z seed\nKTHXBYE\n")
  (define izmakin-special-slot-runs-on-prototype
    (run-source izmakin-special-slot-runs-on-prototype-src))
  (check-eq? (hash-ref izmakin-special-slot-runs-on-prototype 'status) 'ok)
  (check-equal? (hash-ref izmakin-special-slot-runs-on-prototype 'stdout)
                "3\n3\n")

  (define method-global-capture-src
    "HAI 1.3\nI HAS A suffix ITZ \"!\"\nO HAI IM speaker\n  HOW IZ I say YR x\n    FOUND YR SMOOSH x AN suffix MKAY\n  IF U SAY SO\nKTHX\nVISIBLE speaker IZ say YR \"A\" MKAY\nsuffix R \"?\"\nVISIBLE speaker IZ say YR \"A\" MKAY\nKTHXBYE\n")
  (define method-global-capture
    (run-source method-global-capture-src))
  (check-eq? (hash-ref method-global-capture 'status) 'ok)
  ;; Regression: method closures should observe shared lexical boxes.
  (check-equal? (hash-ref method-global-capture 'stdout) "A!\nA?\n")

  (define method-dynamic-slot-srs-src
    "HAI 1.3\nO HAI IM box\n  I HAS A key ITZ \"n\"\n  I HAS A n ITZ 4\n  HOW IZ I bump\n    I HAS A name ITZ key\n    ME'Z SRS name R SUM OF ME'Z SRS name AN 1\n    FOUND YR ME'Z n\n  IF U SAY SO\nKTHX\nVISIBLE box IZ bump MKAY\nVISIBLE box IZ bump MKAY\nKTHXBYE\n")
  (define method-dynamic-slot-srs
    (run-source method-dynamic-slot-srs-src))
  (check-eq? (hash-ref method-dynamic-slot-srs 'status) 'ok)
  ;; Regression: dynamic slot names must compose with ME receiver writes.
  (check-equal? (hash-ref method-dynamic-slot-srs 'stdout) "5\n6\n")

  (define method-me-has-a-slot-src
    "HAI 1.3\nO HAI IM box\n  HOW IZ I addslot\n    ME HAS A made ITZ 9\n    FOUND YR ME'Z made\n  IF U SAY SO\nKTHX\nVISIBLE box IZ addslot MKAY\nVISIBLE box'Z made\nKTHXBYE\n")
  (define method-me-has-a-slot
    (run-source method-me-has-a-slot-src))
  (check-eq? (hash-ref method-me-has-a-slot 'status) 'ok)
  (check-equal? (hash-ref method-me-has-a-slot 'stdout) "9\n9\n")

  (define me-outside-method-src
    "HAI 1.3\nHOW IZ I bad\n  FOUND YR ME\nIF U SAY SO\nVISIBLE I IZ bad MKAY\nKTHXBYE\n")
  (define me-outside-method
    (run-source me-outside-method-src))
  (check-eq? (hash-ref me-outside-method 'status) 'runtime-error)
  (check-true (regexp-match? #px"unknown identifier: ME"
                             (hash-ref me-outside-method 'error)))

  (define method-lookup-order-src
    "HAI 1.3\nI HAS A g ITZ \"GLOBAL\"\nI HAS A h ITZ \"GLOBAL-H\"\nO HAI IM obj\n  I HAS A g ITZ \"SLOT\"\n  HOW IZ I pick YR g\n    FOUND YR g\n  IF U SAY SO\n  HOW IZ I pickslot\n    FOUND YR g\n  IF U SAY SO\n  HOW IZ I pickglobal\n    FOUND YR h\n  IF U SAY SO\nKTHX\nVISIBLE obj IZ pick YR \"ARG\" MKAY\nVISIBLE obj IZ pickslot MKAY\nVISIBLE obj IZ pickglobal MKAY\nKTHXBYE\n")
  (define method-lookup-order
    (run-source method-lookup-order-src))
  (check-eq? (hash-ref method-lookup-order 'status) 'ok)
  (check-equal? (hash-ref method-lookup-order 'stdout)
                "ARG\nSLOT\nGLOBAL-H\n")

  (define object-block-slot-first-over-global-src
    "HAI 1.3\nI HAS A x ITZ \"global\"\nO HAI IM obj\n  I HAS A x ITZ \"slot\"\n  VISIBLE x\nKTHX\nVISIBLE x\nKTHXBYE\n")
  (define object-block-slot-first-over-global
    (run-source object-block-slot-first-over-global-src))
  (check-eq? (hash-ref object-block-slot-first-over-global 'status) 'ok)
  ;; Regression: inside O HAI IM block, lookup is slot-first before global.
  (check-equal? (hash-ref object-block-slot-first-over-global 'stdout)
                "slot\nglobal\n")

  (define slot-function-receiver-namespace-src
    "HAI 1.3\nHOW IZ I funkin YR shun\n  FOUND YR SMOOSH prefix AN shun MKAY\nIF U SAY SO\nO HAI IM parentClass\n  I HAS A prefix ITZ \"parentClass-\"\n  I HAS A runin ITZ funkin\nKTHX\nO HAI IM childClass IM LIEK parentClass\n  I HAS A prefix ITZ \"childClass-\"\nKTHX\nVISIBLE parentClass IZ runin YR \"A\" MKAY\nVISIBLE childClass IZ runin YR \"B\" MKAY\nKTHXBYE\n")
  (define slot-function-receiver-namespace
    (run-source slot-function-receiver-namespace-src))
  (check-eq? (hash-ref slot-function-receiver-namespace 'status) 'ok)
  (check-equal? (hash-ref slot-function-receiver-namespace 'stdout)
                "parentClass-A\nchildClass-B\n")

  (define slot-function-receiver-assignment-src
    "HAI 1.3\nHOW IZ I setprefix YR p\n  prefix R p\n  FOUND YR prefix\nIF U SAY SO\nO HAI IM parentClass\n  I HAS A prefix ITZ \"parentClass-\"\n  I HAS A runin ITZ setprefix\nKTHX\nO HAI IM childClass IM LIEK parentClass\n  I HAS A prefix ITZ \"childClass-\"\nKTHX\nVISIBLE childClass IZ runin YR \"childClass+\" MKAY\nVISIBLE childClass'Z prefix\nVISIBLE parentClass'Z prefix\nKTHXBYE\n")
  (define slot-function-receiver-assignment
    (run-source slot-function-receiver-assignment-src))
  (check-eq? (hash-ref slot-function-receiver-assignment 'status) 'ok)
  (check-equal? (hash-ref slot-function-receiver-assignment 'stdout)
                "childClass+\nchildClass+\nparentClass-\n")

  (define inherited-method-slot-independence-src
    "HAI 1.3\nO HAI IM parent\n  I HAS A val ITZ 1\n  HOW IZ I bump\n    val R SUM OF val AN 1\n    FOUND YR val\n  IF U SAY SO\nKTHX\nO HAI IM child IM LIEK parent\nKTHX\nVISIBLE parent IZ bump MKAY\nVISIBLE child IZ bump MKAY\nVISIBLE parent'Z val\nVISIBLE child'Z val\nKTHXBYE\n")
  (define inherited-method-slot-independence
    (run-source inherited-method-slot-independence-src))
  (check-eq? (hash-ref inherited-method-slot-independence 'status) 'ok)
  ;; Parent-chain lookup plus copy-on-write assignment should not alias parent slots.
  (check-equal? (hash-ref inherited-method-slot-independence 'stdout)
                "2\n3\n2\n3\n")

  (define inherited-parent-mutation-visibility-src
    "HAI 1.3\nO HAI IM parent\n  I HAS A val ITZ 1\nKTHX\nO HAI IM child IM LIEK parent\nKTHX\nparent'Z val R 5\nVISIBLE child'Z val\nchild'Z val R 7\nVISIBLE parent'Z val\nVISIBLE child'Z val\nKTHXBYE\n")
  (define inherited-parent-mutation-visibility
    (run-source inherited-parent-mutation-visibility-src))
  (check-eq? (hash-ref inherited-parent-mutation-visibility 'status) 'ok)
  (check-equal? (hash-ref inherited-parent-mutation-visibility 'stdout)
                "5\n5\n7\n")

  (define parent-slot-reparenting-src
    "HAI 1.3\nO HAI IM a\n  I HAS A val ITZ \"A\"\nKTHX\nO HAI IM b\n  I HAS A val ITZ \"B\"\nKTHX\nO HAI IM c IM LIEK a\nKTHX\nVISIBLE c'Z val\nc'Z parent R b\nVISIBLE c'Z val\nKTHXBYE\n")
  (define parent-slot-reparenting
    (run-source parent-slot-reparenting-src))
  (check-eq? (hash-ref parent-slot-reparenting 'status) 'ok)
  (check-equal? (hash-ref parent-slot-reparenting 'stdout)
                "A\nB\n")

  (define parent-cycle-lookup-terminates-src
    "HAI 1.3\nO HAI IM a\n  I HAS A keep ITZ 1\nKTHX\nO HAI IM b IM LIEK a\nKTHX\na'Z parent R b\nVISIBLE b'Z keep\nVISIBLE b'Z missing\nKTHXBYE\n")
  (define parent-cycle-lookup-terminates
    (run-source parent-cycle-lookup-terminates-src))
  (check-eq? (hash-ref parent-cycle-lookup-terminates 'status) 'runtime-error)
  (check-equal? (hash-ref parent-cycle-lookup-terminates 'stdout) "1\n")
  (check-true (regexp-match? #px"unknown slot: missing"
                             (hash-ref parent-cycle-lookup-terminates 'error)))

  (define parent-cycle-assignment-terminates-src
    "HAI 1.3\nO HAI IM a\n  I HAS A keep ITZ 1\nKTHX\nO HAI IM b IM LIEK a\nKTHX\na'Z parent R b\nb'Z ghost R 3\nKTHXBYE\n")
  (define parent-cycle-assignment-terminates
    (run-source parent-cycle-assignment-terminates-src))
  (check-eq? (hash-ref parent-cycle-assignment-terminates 'status) 'runtime-error)
  ;; Regression: assignment traversal over parent chain must remain cycle-safe.
  (check-true (regexp-match? #px"unknown slot: ghost"
                             (hash-ref parent-cycle-assignment-terminates 'error)))

  (define parent-cycle-method-call-terminates-src
    "HAI 1.3\nO HAI IM a\n  I HAS A keep ITZ 1\nKTHX\nO HAI IM b IM LIEK a\nKTHX\na'Z parent R b\nb IZ nope MKAY\nKTHXBYE\n")
  (define parent-cycle-method-call-terminates
    (run-source parent-cycle-method-call-terminates-src))
  (check-eq? (hash-ref parent-cycle-method-call-terminates 'status) 'runtime-error)
  ;; Regression: method lookup traversal over parent chain must remain cycle-safe.
  (check-true (regexp-match? #px"unknown method: nope"
                             (hash-ref parent-cycle-method-call-terminates 'error)))

  (define inherited-assignment-unknown-name-src
    "HAI 1.3\nO HAI IM parent\nKTHX\nO HAI IM child IM LIEK parent\nKTHX\nchild'Z ghost R 5\nKTHXBYE\n")
  (define inherited-assignment-unknown-name
    (run-source inherited-assignment-unknown-name-src))
  (check-eq? (hash-ref inherited-assignment-unknown-name 'status) 'runtime-error)
  (check-true (regexp-match? #px"unknown slot: ghost"
                             (hash-ref inherited-assignment-unknown-name 'error)))

  (define function-storage-src
    "HAI 1.3\nHOW IZ I fun1\n  FOUND YR \"a\"\nIF U SAY SO\nI HAS A foo ITZ A BUKKIT\nfoo HAS A var1 ITZ fun1\nVISIBLE I IZ foo'Z var1 MKAY\nKTHXBYE\n")
  (define function-storage (run-source function-storage-src))
  (check-eq? (hash-ref function-storage 'status) 'ok)
  (check-equal? (hash-ref function-storage 'stdout) "a\n")

  (define dynamic-function-name-src
    "HAI 1.3\nI HAS A name1 ITZ \"fun\"\nHOW IZ I SRS SMOOSH name1 AN 1 MKAY\n  VISIBLE \"a\"\nIF U SAY SO\nHOW IZ I SRS SMOOSH name1 AN 2 MKAY YR arg\n  VISIBLE arg\nIF U SAY SO\nI IZ SRS SMOOSH name1 AN 1 MKAY MKAY\nI IZ SRS SMOOSH name1 AN 2 MKAY YR \"b\" MKAY\nKTHXBYE\n")
  (define dynamic-function-name (run-source dynamic-function-name-src))
  (check-eq? (hash-ref dynamic-function-name 'status) 'ok)
  (check-equal? (hash-ref dynamic-function-name 'stdout) "a\nb\n")

  (define mixin-object-src
    "HAI 1.3\nO HAI IM parent\n  I HAS A p ITZ 1\nKTHX\nO HAI IM mix1\n  I HAS A a ITZ 10\nKTHX\nO HAI IM mix2\n  I HAS A a ITZ 20\n  I HAS A b ITZ 30\nKTHX\nO HAI IM child IM LIEK parent SMOOSH mix1 AN mix2\nKTHX\nVISIBLE child'Z p\nVISIBLE child'Z a\nVISIBLE child'Z b\nKTHXBYE\n")
  (define mixin-object (run-source mixin-object-src))
  (check-eq? (hash-ref mixin-object 'status) 'ok)
  ;; Reverse-order copy means mix1 overrides mix2 for duplicate slots.
  (check-equal? (hash-ref mixin-object 'stdout) "1\n10\n30\n")

  (define mixin-static-snapshot-src
    "HAI 1.3\nO HAI IM parent\nKTHX\nO HAI IM mix\n  I HAS A v ITZ 1\nKTHX\nO HAI IM child IM LIEK parent SMOOSH mix\nKTHX\nmix'Z v R 9\nVISIBLE child'Z v\nKTHXBYE\n")
  (define mixin-static-snapshot
    (run-source mixin-static-snapshot-src))
  (check-eq? (hash-ref mixin-static-snapshot 'status) 'ok)
  (check-equal? (hash-ref mixin-static-snapshot 'stdout) "1\n")

  (define mixin-parent-child-combo-src
    "HAI 1.3\nO HAI IM parent\n  I HAS A x ITZ \"parent\"\nKTHX\nO HAI IM mix\n  I HAS A x ITZ \"mix\"\nKTHX\nO HAI IM child IM LIEK parent SMOOSH mix\nKTHX\nVISIBLE child'Z x\nparent'Z x R \"parent2\"\nVISIBLE child'Z x\nKTHXBYE\n")
  (define mixin-parent-child-combo
    (run-source mixin-parent-child-combo-src))
  (check-eq? (hash-ref mixin-parent-child-combo 'status) 'ok)
  (check-equal? (hash-ref mixin-parent-child-combo 'stdout) "mix\nmix\n")

  (define mixin-special-parent-restored-src
    "HAI 1.3\nO HAI IM base1\n  I HAS A tag ITZ \"BASE1\"\nKTHX\nO HAI IM base2\n  I HAS A tag ITZ \"BASE2\"\nKTHX\nO HAI IM mix IM LIEK base1\nKTHX\nO HAI IM child IM LIEK base2 SMOOSH mix\nKTHX\nVISIBLE child'Z tag\nKTHXBYE\n")
  (define mixin-special-parent-restored
    (run-source mixin-special-parent-restored-src))
  (check-eq? (hash-ref mixin-special-parent-restored 'status) 'ok)
  ;; Regression: mixin parent slot copy must not replace declared IM LIEK parent.
  (check-equal? (hash-ref mixin-special-parent-restored 'stdout) "BASE2\n")

  (define mixin-special-omgwtf-copied-src
    "HAI 1.3\nO HAI IM parent\nKTHX\nO HAI IM mix\n  HOW IZ I omgwtf YR slotname\n    FOUND YR SMOOSH \"mix-\" AN slotname MKAY\n  IF U SAY SO\nKTHX\nO HAI IM child IM LIEK parent SMOOSH mix\nKTHX\nVISIBLE child'Z ghost\nKTHXBYE\n")
  (define mixin-special-omgwtf-copied
    (run-source mixin-special-omgwtf-copied-src))
  (check-eq? (hash-ref mixin-special-omgwtf-copied 'status) 'ok)
  ;; Regression: mixin-provided omgwtf special slot behavior is copied to child.
  (check-equal? (hash-ref mixin-special-omgwtf-copied 'stdout) "mix-ghost\n")

  (define mixin-special-izmakin-copied-src
    "HAI 1.3\nO HAI IM parent\nKTHX\nO HAI IM mix\n  HOW IZ I izmakin\n    ME HAS A built ITZ \"YES\"\n  IF U SAY SO\nKTHX\nO HAI IM child IM LIEK parent SMOOSH mix\nKTHX\nVISIBLE child'Z built\nKTHXBYE\n")
  (define mixin-special-izmakin-copied
    (run-source mixin-special-izmakin-copied-src))
  (check-eq? (hash-ref mixin-special-izmakin-copied 'status) 'ok)
  ;; Regression: mixin-provided izmakin runs during child construction.
  (check-equal? (hash-ref mixin-special-izmakin-copied 'stdout) "YES\n")

  (define mixin-source-own-only-slots-src
    "HAI 1.3\nO HAI IM mixbase\n  I HAS A inherited ITZ \"INHERITED\"\nKTHX\nO HAI IM mix IM LIEK mixbase\n  I HAS A own ITZ \"OWN\"\nKTHX\nO HAI IM parent\nKTHX\nO HAI IM child IM LIEK parent SMOOSH mix\nKTHX\nVISIBLE child'Z own\nVISIBLE child'Z inherited\nKTHXBYE\n")
  (define mixin-source-own-only-slots
    (run-source mixin-source-own-only-slots-src))
  (check-eq? (hash-ref mixin-source-own-only-slots 'status) 'runtime-error)
  ;; Regression: mixin copy source set is own slots/methods, not inherited ones.
  (check-equal? (hash-ref mixin-source-own-only-slots 'stdout) "OWN\n")
  (check-true (regexp-match? #px"unknown slot: inherited"
                             (hash-ref mixin-source-own-only-slots 'error)))

  (define mixin-source-own-only-methods-src
    "HAI 1.3\nO HAI IM mixbase\n  HOW IZ I inheritedmeth\n    FOUND YR \"INHERITED\"\n  IF U SAY SO\nKTHX\nO HAI IM mix IM LIEK mixbase\nKTHX\nO HAI IM parent\nKTHX\nO HAI IM child IM LIEK parent SMOOSH mix\nKTHX\nchild IZ inheritedmeth MKAY\nKTHXBYE\n")
  (define mixin-source-own-only-methods
    (run-source mixin-source-own-only-methods-src))
  (check-eq? (hash-ref mixin-source-own-only-methods 'status) 'runtime-error)
  (check-true (regexp-match? #px"unknown method: inheritedmeth"
                             (hash-ref mixin-source-own-only-methods 'error)))

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

  (define gimmeh-implicit-target-declare-src
    "HAI 1.3\nGIMMEH fresh\nVISIBLE fresh\nKTHXBYE\n")
  (define gimmeh-implicit-target-declare
    (run-source gimmeh-implicit-target-declare-src #:input "Zed\n"))
  (check-eq? (hash-ref gimmeh-implicit-target-declare 'status) 'ok)
  ;; Regression/policy: GIMMEH creates missing target binding when undeclared.
  (check-equal? (hash-ref gimmeh-implicit-target-declare 'stdout) "Zed\n")

  (define visible-bang-src
    "HAI 1.3\nVISIBLE \"A\"!\nVISIBLE \"B\"\nKTHXBYE\n")
  (define visible-bang-result (run-source visible-bang-src))
  (check-eq? (hash-ref visible-bang-result 'status) 'ok)
  (check-equal? (hash-ref visible-bang-result 'stdout) "AB\n")

  (define visible-inline-src
    "HAI 1.3\nVISIBLE \"A\" \"B\" 3\nKTHXBYE\n")
  (define visible-inline-result (run-source visible-inline-src))
  (check-eq? (hash-ref visible-inline-result 'status) 'ok)
  (check-equal? (hash-ref visible-inline-result 'stdout) "AB3\n")

  (define string-namespace-src
    "HAI 1.3\nVISIBLE I IZ STRING'Z LEN YR \"cats\" MKAY\nKTHXBYE\n")
  (define string-namespace-result (run-source string-namespace-src))
  (check-eq? (hash-ref string-namespace-result 'status) 'runtime-error)
  (check-true (regexp-match? #px"unknown identifier: STRING"
                             (hash-ref string-namespace-result 'error)))

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

  (define unicode-line-cont-src
    "HAI 1.3\nVISIBLE SMOOSH \"A\" AN …\n\"B\" MKAY\nKTHXBYE\n")
  (define unicode-line-cont-result (run-source unicode-line-cont-src))
  (check-eq? (hash-ref unicode-line-cont-result 'status) 'ok)
  (check-equal? (hash-ref unicode-line-cont-result 'stdout) "AB\n")

  (define line-cont-comma-soft-break-src
    "HAI 1.3\nVISIBLE \"A\",...\nVISIBLE \"B\"\nKTHXBYE\n")
  (define line-cont-comma-soft-break-result
    (run-source line-cont-comma-soft-break-src))
  (check-eq? (hash-ref line-cont-comma-soft-break-result 'status) 'ok)
  (check-equal? (hash-ref line-cont-comma-soft-break-result 'stdout) "A\nB\n")

  (define line-cont-chain-ending-comma-src
    "HAI 1.3\nVISIBLE SMOOSH \"A\" AN ...\n\"B\" MKAY, VISIBLE \"C\"\nKTHXBYE\n")
  (define line-cont-chain-ending-comma-result
    (run-source line-cont-chain-ending-comma-src))
  (check-eq? (hash-ref line-cont-chain-ending-comma-result 'status) 'ok)
  (check-equal? (hash-ref line-cont-chain-ending-comma-result 'stdout) "AB\nC\n")

  (define visible-continuation-comma-boundary-src
    "HAI 1.3\nVISIBLE \"A\" ...\n\"B\", VISIBLE \"C\" ...\n\"D\"\nKTHXBYE\n")
  (define visible-continuation-comma-boundary
    (run-source visible-continuation-comma-boundary-src))
  (check-eq? (hash-ref visible-continuation-comma-boundary 'status) 'ok)
  (check-equal? (hash-ref visible-continuation-comma-boundary 'stdout) "AB\nCD\n")

  (define visible-continuation-bang-src
    "HAI 1.3\nVISIBLE \"A\" ...\n\"B\" !\nVISIBLE \"C\"\nKTHXBYE\n")
  (define visible-continuation-bang
    (run-source visible-continuation-bang-src))
  (check-eq? (hash-ref visible-continuation-bang 'status) 'ok)
  (check-equal? (hash-ref visible-continuation-bang 'stdout) "ABC\n")

  (define line-cont-standalone-ellipsis-src
    "HAI 1.3\nVISIBLE \"A\"...\n...\n\n\"B\"\nKTHXBYE\n")
  (define line-cont-standalone-ellipsis-result
    (run-source line-cont-standalone-ellipsis-src))
  (check-eq? (hash-ref line-cont-standalone-ellipsis-result 'status) 'ok)
  (check-equal? (hash-ref line-cont-standalone-ellipsis-result 'stdout) "AB\n")

  (define line-cont-ellipsis-in-comment-src
    "HAI 1.3\nVISIBLE \"A\" BTW ...\nVISIBLE \"B\"\nKTHXBYE\n")
  (define line-cont-ellipsis-in-comment-result
    (run-source line-cont-ellipsis-in-comment-src))
  (check-eq? (hash-ref line-cont-ellipsis-in-comment-result 'status) 'ok)
  (check-equal? (hash-ref line-cont-ellipsis-in-comment-result 'stdout) "A\nB\n")

  (define smoosh-optional-an-src
    "HAI 1.3\nVISIBLE SMOOSH \"a\" \"b\" \"c\" MKAY\nKTHXBYE\n")
  (define smoosh-optional-an (run-source smoosh-optional-an-src))
  (check-eq? (hash-ref smoosh-optional-an 'status) 'ok)
  (check-equal? (hash-ref smoosh-optional-an 'stdout) "abc\n")

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

  (define string-normative-escape-src
    "HAI 1.3\nVISIBLE \"A:[DOLLAR SIGN]B:[CENT SIGN]C:[EURO SIGN]D:[SNOWMAN]E:[GREEK SMALL LETTER PI]\"\nKTHXBYE\n")
  (define string-normative-escape-result (run-source string-normative-escape-src))
  (check-eq? (hash-ref string-normative-escape-result 'status) 'ok)
  (check-equal? (hash-ref string-normative-escape-result 'stdout)
                (string-append "A"
                               (string (integer->char #x0024))
                               "B"
                               (string (integer->char #x00A2))
                               "C"
                               (string (integer->char #x20AC))
                               "D"
                               (string (integer->char #x2603))
                               "E"
                               (string (integer->char #x03C0))
                               "\n"))

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

  (define format-string-escaped-placeholder-src
    "HAI 1.3\nI HAS A name ITZ \"Ada\"\nVISIBLE \"::{name}\"\nKTHXBYE\n")
  (define format-string-escaped-placeholder
    (run-source format-string-escaped-placeholder-src))
  (check-eq? (hash-ref format-string-escaped-placeholder 'status) 'ok)
  (check-equal? (hash-ref format-string-escaped-placeholder 'stdout)
                ":{name}\n")

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

  (define assign-undeclared-runtime-error-src
    "HAI 1.3\nx R 4\nKTHXBYE\n")
  (define assign-undeclared-runtime-error
    (run-source assign-undeclared-runtime-error-src))
  (check-eq? (hash-ref assign-undeclared-runtime-error 'status) 'runtime-error)
  (check-true (regexp-match? #px"unknown identifier: x"
                             (hash-ref assign-undeclared-runtime-error 'error)))

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
