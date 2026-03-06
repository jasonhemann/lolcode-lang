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
                "2\n2.5\nWIN\ncat\nNOOB\n3\n")

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

  (define prototype-srs-parent-and-mixins-src
    "HAI 1.3\nI HAS A pname ITZ \"Parent\"\nI HAS A m1name ITZ \"MixA\"\nI HAS A m2name ITZ \"MixB\"\nO HAI IM Parent\n  I HAS A pslot ITZ \"P\"\nKTHX\nO HAI IM MixA\n  I HAS A m1slot ITZ \"M1\"\nKTHX\nO HAI IM MixB\n  I HAS A m2slot ITZ \"M2\"\nKTHX\nI HAS A kid ITZ A SRS pname SMOOSH SRS m1name AN SRS m2name\nVISIBLE kid'Z pslot\nVISIBLE kid'Z m1slot\nVISIBLE kid'Z m2slot\nKTHXBYE\n")
  (define prototype-srs-parent-and-mixins
    (run-source prototype-srs-parent-and-mixins-src))
  (check-eq? (hash-ref prototype-srs-parent-and-mixins 'status) 'ok)
  (check-equal? (hash-ref prototype-srs-parent-and-mixins 'stdout)
                "P\nM1\nM2\n")

  (define method-def-srs-receiver-and-name-src
    "HAI 1.3\nI HAS A recv ITZ \"box\"\nI HAS A mname ITZ \"bump\"\nO HAI IM box\n  I HAS A n ITZ 0\nKTHX\nHOW IZ SRS recv SRS mname\n  n R SUM OF n AN 1\n  FOUND YR n\nIF U SAY SO\nVISIBLE box IZ bump MKAY\nVISIBLE box IZ bump MKAY\nKTHXBYE\n")
  (define method-def-srs-receiver-and-name
    (run-source method-def-srs-receiver-and-name-src))
  (check-eq? (hash-ref method-def-srs-receiver-and-name 'status) 'ok)
  (check-equal? (hash-ref method-def-srs-receiver-and-name 'stdout)
                "1\n2\n")

  (define call-target-srs-slot-name-src
    "HAI 1.3\nI HAS A host ITZ A BUKKIT\nHOW IZ host ping\n  FOUND YR \"pong\"\nIF U SAY SO\nI HAS A dyn ITZ \"ping\"\nVISIBLE I IZ host'Z SRS dyn MKAY\nKTHXBYE\n")
  (define call-target-srs-slot-name
    (run-source call-target-srs-slot-name-src))
  (check-eq? (hash-ref call-target-srs-slot-name 'status) 'ok)
  (check-equal? (hash-ref call-target-srs-slot-name 'stdout)
                "pong\n")

  (define method-def-srs-receiver-slot-tail-src
    "HAI 1.3\nI HAS A rootname ITZ \"root\"\nI HAS A childname ITZ \"child\"\nO HAI IM root\n  I HAS A child ITZ A BUKKIT\nKTHX\nHOW IZ SRS rootname'Z SRS childname ping\n  FOUND YR \"ok\"\nIF U SAY SO\nVISIBLE root'Z child IZ ping MKAY\nKTHXBYE\n")
  (define method-def-srs-receiver-slot-tail
    (run-source method-def-srs-receiver-slot-tail-src))
  (check-eq? (hash-ref method-def-srs-receiver-slot-tail 'status) 'ok)
  (check-equal? (hash-ref method-def-srs-receiver-slot-tail 'stdout)
                "ok\n")

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

  (define switch-matched-fallthrough-skips-default-src
    "HAI 1.3\nI HAS A x ITZ 1\nx, WTF?\n  OMG 1\n    VISIBLE \"A\"\n  OMG 2\n    VISIBLE \"B\"\n  OMGWTF\n    VISIBLE \"D\"\nOIC\nKTHXBYE\n")
  (define switch-matched-fallthrough-skips-default
    (run-source switch-matched-fallthrough-skips-default-src))
  (check-eq? (hash-ref switch-matched-fallthrough-skips-default 'status) 'ok)
  ;; Spec line 486: OMGWTF is taken only when no OMG literal matches.
  (check-equal? (hash-ref switch-matched-fallthrough-skips-default 'stdout)
                "A\nB\n")

  (define switch-numeric-mode-match-src
    "HAI 1.3\nI HAS A x ITZ 1.0\nx, WTF?\n  OMG 1\n    VISIBLE \"NUM\"\n    GTFO\n  OMG \"1\"\n    VISIBLE \"YARN\"\n    GTFO\n  OMGWTF\n    VISIBLE \"MISS\"\nOIC\nKTHXBYE\n")
  (define switch-numeric-mode-match
    (run-source switch-numeric-mode-match-src))
  (check-eq? (hash-ref switch-numeric-mode-match 'status) 'ok)
  ;; Numeric-mode equality: NUMBR and NUMBAR compare numerically in WTF? matching.
  (check-equal? (hash-ref switch-numeric-mode-match 'stdout) "NUM\n")

  (define switch-no-string-coercion-src
    "HAI 1.3\nI HAS A x ITZ \"1\"\nx, WTF?\n  OMG 1\n    VISIBLE \"NUM\"\n    GTFO\n  OMG \"1\"\n    VISIBLE \"YARN\"\n    GTFO\n  OMGWTF\n    VISIBLE \"MISS\"\nOIC\nKTHXBYE\n")
  (define switch-no-string-coercion
    (run-source switch-no-string-coercion-src))
  (check-eq? (hash-ref switch-no-string-coercion 'status) 'ok)
  ;; Non-numeric mixed-type matching does not coerce in WTF? matching.
  (check-equal? (hash-ref switch-no-string-coercion 'stdout) "YARN\n")

  (define function-src
    "HAI 1.3\nHOW IZ I addin YR x AN YR y\n  FOUND YR SUM OF x AN y\nIF U SAY SO\nI HAS A result ITZ I IZ addin YR 2 AN YR 3 MKAY\nVISIBLE result\nKTHXBYE\n")
  (define function-result (run-source function-src))
  (check-eq? (hash-ref function-result 'status) 'ok)
  (check-equal? (hash-ref function-result 'stdout) "5\n")

  (define function-arg-eval-order-src
    "HAI 1.3\nI HAS A seq ITZ \"\"\nHOW IZ I mark YR c\n  seq R SMOOSH seq AN c MKAY\n  FOUND YR c\nIF U SAY SO\nHOW IZ I see YR a AN YR b\n  FOUND YR seq\nIF U SAY SO\nVISIBLE I IZ see YR I IZ mark YR \"A\" MKAY AN YR I IZ mark YR \"B\" MKAY MKAY\nKTHXBYE\n")
  (define function-arg-eval-order
    (run-source function-arg-eval-order-src))
  (check-eq? (hash-ref function-arg-eval-order 'status) 'ok)
  ;; Regression: call arguments are evaluated before body entry, left-to-right.
  (check-equal? (hash-ref function-arg-eval-order 'stdout) "AB\n")

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

  (define function-forward-reference-runtime-error-src
    "HAI 1.3\nVISIBLE I IZ later MKAY\nHOW IZ I later\n  FOUND YR \"ok\"\nIF U SAY SO\nKTHXBYE\n")
  (define function-forward-reference-runtime-error
    (run-source function-forward-reference-runtime-error-src))
  (check-eq? (hash-ref function-forward-reference-runtime-error 'status) 'runtime-error)
  ;; Policy: function bindings become available when definition statements execute.
  (check-true (regexp-match? #px"unknown function: later"
                             (hash-ref function-forward-reference-runtime-error
                                       'error)))

  (define function-duplicate-params-runtime-error-src
    "HAI 1.3\nHOW IZ I dup YR x AN YR x\n  FOUND YR x\nIF U SAY SO\nVISIBLE I IZ dup YR 1 AN YR 2 MKAY\nKTHXBYE\n")
  (define function-duplicate-params-runtime-error
    (run-source function-duplicate-params-runtime-error-src))
  (check-eq? (hash-ref function-duplicate-params-runtime-error 'status) 'runtime-error)
  (check-true (regexp-match? #px"identifier already declared in this scope: x"
                             (hash-ref function-duplicate-params-runtime-error
                                       'error)))

  (define declaration-rhs-does-not-see-binding-being-declared-src
    "HAI 1.3\nI HAS A x ITZ SUM OF x AN 1\nKTHXBYE\n")
  (define declaration-rhs-does-not-see-binding-being-declared
    (run-source declaration-rhs-does-not-see-binding-being-declared-src))
  (check-eq? (hash-ref declaration-rhs-does-not-see-binding-being-declared 'status)
             'runtime-error)
  (check-true (regexp-match? #px"unknown identifier: x"
                             (hash-ref declaration-rhs-does-not-see-binding-being-declared
                                       'error)))

  (define assignment-rhs-sees-prior-binding-value-src
    "HAI 1.3\nI HAS A x ITZ 1\nx R SUM OF x AN 1\nVISIBLE x\nKTHXBYE\n")
  (define assignment-rhs-sees-prior-binding-value
    (run-source assignment-rhs-sees-prior-binding-value-src))
  (check-eq? (hash-ref assignment-rhs-sees-prior-binding-value 'status) 'ok)
  (check-equal? (hash-ref assignment-rhs-sees-prior-binding-value 'stdout)
                "2\n")

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

  (define empty-bukkit-truthy-src
    "HAI 1.3\nI HAS A b ITZ A BUKKIT\nb\nO RLY?\n  YA RLY\n    VISIBLE \"T\"\n  NO WAI\n    VISIBLE \"F\"\nOIC\nKTHXBYE\n")
  (define empty-bukkit-truthy
    (run-source empty-bukkit-truthy-src))
  (check-eq? (hash-ref empty-bukkit-truthy 'status) 'ok)
  ;; Policy: BUKKIT values are truthy (no empty-container false special case).
  (check-equal? (hash-ref empty-bukkit-truthy 'stdout) "T\n")

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

  (define object-self-reference-during-construction-src
    "HAI 1.3\nO HAI IM selfref\n  I HAS A bad ITZ selfref\nKTHX\nKTHXBYE\n")
  (define object-self-reference-during-construction
    (run-source object-self-reference-during-construction-src))
  (check-eq? (hash-ref object-self-reference-during-construction 'status) 'runtime-error)
  ;; N26: object name binding occurs after O HAI body evaluation.
  (check-true (regexp-match? #px"unknown identifier: selfref"
                             (hash-ref object-self-reference-during-construction
                                       'error)))

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

  (define loop-order-matrix-src
    "HAI 1.3\nI HAS A a ITZ \"\"\nI HAS A i ITZ 0\nIM IN YR l1 UPPIN YR i TIL BOTH SAEM i AN 3\n  a R SMOOSH a AN i MKAY\nIM OUTTA YR l1\nVISIBLE a\nI HAS A b ITZ \"\"\nI HAS A j ITZ 0\nIM IN YR l2 UPPIN YR j WILE DIFFRINT j AN 3\n  b R SMOOSH b AN j MKAY\nIM OUTTA YR l2\nVISIBLE b\nI HAS A c ITZ \"\"\nI HAS A k ITZ 3\nIM IN YR l3 NERFIN YR k TIL BOTH SAEM k AN 0\n  c R SMOOSH c AN k MKAY\nIM OUTTA YR l3\nVISIBLE c\nI HAS A d ITZ \"\"\nI HAS A m ITZ 3\nIM IN YR l4 NERFIN YR m WILE DIFFRINT m AN 0\n  d R SMOOSH d AN m MKAY\nIM OUTTA YR l4\nVISIBLE d\nKTHXBYE\n")
  (define loop-order-matrix (run-source loop-order-matrix-src))
  (check-eq? (hash-ref loop-order-matrix 'status) 'ok)
  ;; Regression: loop condition checks happen pre-body; updater runs post-body.
  (check-equal? (hash-ref loop-order-matrix 'stdout)
                "012\n012\n321\n321\n")

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

  (define loop-unary-updater-side-effects-src
    "HAI 1.3\nI HAS A ticks ITZ 0\nHOW IZ I bump YR v\n  ticks R SUM OF ticks AN 1\n  FOUND YR SUM OF v AN 1\nIF U SAY SO\nIM IN YR lp I IZ bump YR i MKAY TIL BOTH SAEM i AN 3\n  VISIBLE i\nIM OUTTA YR lp\nVISIBLE ticks\nKTHXBYE\n")
  (define loop-unary-updater-side-effects
    (run-source loop-unary-updater-side-effects-src))
  (check-eq? (hash-ref loop-unary-updater-side-effects 'status) 'ok)
  ;; N30: updater function runs once per completed iteration (post-body).
  (check-equal? (hash-ref loop-unary-updater-side-effects 'stdout)
                "0\n1\n2\n3\n")

  (define loop-unary-updater-arity-error-src
    "HAI 1.3\nHOW IZ I zerofn\n  FOUND YR 0\nIF U SAY SO\nIM IN YR lp I IZ zerofn YR i MKAY TIL BOTH SAEM i AN 1\n  VISIBLE i\nIM OUTTA YR lp\nKTHXBYE\n")
  (define loop-unary-updater-arity-error
    (run-source loop-unary-updater-arity-error-src))
  (check-eq? (hash-ref loop-unary-updater-arity-error 'status) 'runtime-error)
  (check-true (regexp-match? #px"function zerofn expected 0 args, got 1"
                             (hash-ref loop-unary-updater-arity-error 'error)))

  (define logic-src
    "HAI 1.3\nI HAS A n ITZ 42\nVISIBLE BOTH OF DIFFRINT n AN 0 AN DIFFRINT n AN 42\nVISIBLE EITHER OF BOTH SAEM n AN 0 AN BOTH SAEM n AN 42\nVISIBLE WON OF BOTH SAEM n AN 42 AN BOTH SAEM n AN 0\nVISIBLE ALL OF DIFFRINT n AN 0 AN NOT BOTH SAEM n AN 0 MKAY\nVISIBLE ANY OF BOTH SAEM n AN 0 AN BOTH SAEM n AN 42 MKAY\nKTHXBYE\n")
  (define logic-result (run-source logic-src))
  (check-eq? (hash-ref logic-result 'status) 'ok)
  (check-equal? (hash-ref logic-result 'stdout) "FAIL\nWIN\nWIN\nWIN\nWIN\n")

  (define logic-binary-eager-rhs-src
    "HAI 1.3\nI HAS A obj ITZ A BUKKIT\nVISIBLE BOTH OF FAIL AN obj'Z missing\nKTHXBYE\n")
  (define logic-binary-eager-rhs (run-source logic-binary-eager-rhs-src))
  (check-eq? (hash-ref logic-binary-eager-rhs 'status) 'runtime-error)
  ;; Binary boolean operators are eager; RHS still evaluates.
  (check-true (regexp-match? #px"unknown slot: missing"
                             (hash-ref logic-binary-eager-rhs 'error)))

  (define logic-binary-eager-rhs-numeric-srs-slot-src
    "HAI 1.3\nI HAS A m ITZ A BUKKIT\nm HAS A SRS 1 ITZ 0\nVISIBLE BOTH OF FAIL AN DIFFRINT m'Z SRS 2 AN 0\nKTHXBYE\n")
  (define logic-binary-eager-rhs-numeric-srs-slot
    (run-source logic-binary-eager-rhs-numeric-srs-slot-src))
  (check-eq? (hash-ref logic-binary-eager-rhs-numeric-srs-slot 'status)
             'runtime-error)
  ;; Corpus tie-in (loleuler/014): eager BOTH OF still evaluates RHS numeric
  ;; SRS slot access, so missing-slot errors are not short-circuited.
  (check-true (regexp-match? #px"unknown slot: 2"
                             (hash-ref logic-binary-eager-rhs-numeric-srs-slot
                                       'error)))

  (define logic-binary-left-to-right-src
    "HAI 1.3\nI HAS A log ITZ \"\"\nHOW IZ I mark YR ch\n  log R SMOOSH log AN ch MKAY\n  FOUND YR WIN\nIF U SAY SO\nVISIBLE BOTH OF I IZ mark YR \"L\" MKAY AN I IZ mark YR \"R\" MKAY\nVISIBLE log\nKTHXBYE\n")
  (define logic-binary-left-to-right (run-source logic-binary-left-to-right-src))
  (check-eq? (hash-ref logic-binary-left-to-right 'status) 'ok)
  ;; Operand evaluation order is deterministic left-to-right.
  (check-equal? (hash-ref logic-binary-left-to-right 'stdout)
                "WIN\nLR\n")

  (define binary-ops-optional-an-src
    "HAI 1.3\nVISIBLE SUM OF 1 2\nVISIBLE DIFF OF 5 2\nVISIBLE PRODUKT OF 3 4\nVISIBLE QUOSHUNT OF 6 2\nVISIBLE MOD OF 7 4\nVISIBLE BIGGR OF 5 2\nVISIBLE SMALLR OF 5 2\nVISIBLE BOTH OF WIN FAIL\nVISIBLE EITHER OF FAIL WIN\nVISIBLE WON OF WIN FAIL\nVISIBLE BOTH SAEM 3 3\nVISIBLE DIFFRINT 3 4\nKTHXBYE\n")
  (define binary-ops-optional-an
    (run-source binary-ops-optional-an-src))
  (check-eq? (hash-ref binary-ops-optional-an 'status) 'ok)
  (check-equal? (hash-ref binary-ops-optional-an 'stdout)
                "3\n3\n12\n3\n3\n5\n2\nFAIL\nWIN\nWIN\nWIN\nWIN\n")

  (define quoshunt-numbr-vs-numbar-src
    "HAI 1.3\nVISIBLE QUOSHUNT OF 5 AN 2\nVISIBLE QUOSHUNT OF MAEK 5 A NUMBAR AN 2\nVISIBLE QUOSHUNT OF 1 AN 2\nKTHXBYE\n")
  (define quoshunt-numbr-vs-numbar
    (run-source quoshunt-numbr-vs-numbar-src))
  (check-eq? (hash-ref quoshunt-numbr-vs-numbar 'status) 'ok)
  ;; Spec line 305: NUMBR/NUMBR uses integer math; NUMBAR presence uses float math.
  (check-equal? (hash-ref quoshunt-numbr-vs-numbar 'stdout)
                "2\n2.5\n0\n")

  (define quoshunt-division-by-zero-runtime-error-src
    "HAI 1.3\nVISIBLE QUOSHUNT OF 1 AN 0\nKTHXBYE\n")
  (define quoshunt-division-by-zero-runtime-error
    (run-source quoshunt-division-by-zero-runtime-error-src))
  (check-eq? (hash-ref quoshunt-division-by-zero-runtime-error 'status)
             'runtime-error)
  (check-true (regexp-match? #px"division by zero"
                             (hash-ref quoshunt-division-by-zero-runtime-error
                                       'error)))

  (define numbr-bignum-arithmetic-src
    "HAI 1.3\nVISIBLE PRODUKT OF 1000000000000000000000000000000 AN 1000000000000000000000000000000\nKTHXBYE\n")
  (define numbr-bignum-arithmetic
    (run-source numbr-bignum-arithmetic-src))
  (check-eq? (hash-ref numbr-bignum-arithmetic 'status) 'ok)
  ;; Policy: numeric portability follows host integers; large NUMBR arithmetic remains exact.
  (check-true (regexp-match? #px"^1[0-9]{60}\n$"
                             (hash-ref numbr-bignum-arithmetic 'stdout)))

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

  (define equality-complex-values-identity-src
    "HAI 1.3\nO HAI IM a\n  I HAS A n ITZ 1\nKTHX\nI HAS A same ITZ a\nO HAI IM b\n  I HAS A n ITZ 1\nKTHX\nVISIBLE BOTH SAEM a AN same\nVISIBLE BOTH SAEM a AN b\nHOW IZ I id YR x\n  FOUND YR x\nIF U SAY SO\nI HAS A f1 ITZ id\nI HAS A f2 ITZ id\nHOW IZ I id2 YR x\n  FOUND YR x\nIF U SAY SO\nI HAS A g ITZ id2\nVISIBLE BOTH SAEM f1 AN f2\nVISIBLE BOTH SAEM f1 AN g\nVISIBLE BOTH SAEM NUMBR AN NUMBR\nVISIBLE BOTH SAEM NUMBR AN YARN\nKTHXBYE\n")
  (define equality-complex-values-identity
    (run-source equality-complex-values-identity-src))
  (check-eq? (hash-ref equality-complex-values-identity 'status) 'ok)
  (check-equal? (hash-ref equality-complex-values-identity 'stdout)
                "WIN\nFAIL\nWIN\nFAIL\nWIN\nFAIL\n")

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
                "2.5\n2\n")

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

  (define cast-plus-number-yarn-src
    "HAI 1.3\nVISIBLE MAEK \"+1.25\" A NUMBAR\nKTHXBYE\n")
  (define cast-plus-number-yarn
    (run-source cast-plus-number-yarn-src))
  (check-eq? (hash-ref cast-plus-number-yarn 'status) 'runtime-error)
  (check-true (regexp-match? #px"cannot cast YARN to numeric value"
                             (hash-ref cast-plus-number-yarn 'error)))

  (define maek-without-article-src
    "HAI 1.3\nVISIBLE MAEK 2 NUMBAR\nKTHXBYE\n")
  (define maek-without-article
    (run-source maek-without-article-src))
  (check-eq? (hash-ref maek-without-article 'status) 'ok)
  (check-equal? (hash-ref maek-without-article 'stdout) "2\n")

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

  (define type-noob-distinction-stability-src
    "HAI 1.3\nVISIBLE BOTH SAEM TYPE AN NOOB\nVISIBLE MAEK TYPE A YARN\nVISIBLE MAEK NOOB A YARN\nVISIBLE MAEK TYPE A TROOF\nVISIBLE MAEK NOOB A TROOF\nKTHXBYE\n")
  (define type-noob-distinction-stability
    (run-source type-noob-distinction-stability-src))
  (check-eq? (hash-ref type-noob-distinction-stability 'status) 'ok)
  ;; N37: TYPE literal and NOOB remain distinct value categories.
  (check-equal? (hash-ref type-noob-distinction-stability 'stdout)
                "FAIL\nTYPE\nNOOB\nWIN\nFAIL\n")

  (define numbar-visible-format-src
    "HAI 1.3\nVISIBLE MAEK \"3.14159\" A NUMBAR\nVISIBLE MAEK 2 A NUMBAR\nVISIBLE MAEK \"-1.239\" A NUMBAR\nKTHXBYE\n")
  (define numbar-visible-format-result
    (run-source numbar-visible-format-src))
  (check-eq? (hash-ref numbar-visible-format-result 'status) 'ok)
  ;; Spec: NUMBAR printed as YARN truncates to default two decimal places.
  ;; Policy: this is interpreted as "at most two decimals" (no forced zero pad).
  (check-equal? (hash-ref numbar-visible-format-result 'stdout)
                "3.14\n2\n-1.23\n")

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

  (define method-call-expression-args-src
    "HAI 1.3\nO HAI IM calc\n  HOW IZ I add YR x AN YR y\n    FOUND YR SUM OF x AN y\n  IF U SAY SO\nKTHX\nVISIBLE calc IZ add YR SUM OF 1 AN 2 AN YR PRODUKT OF 2 AN 3 MKAY\nKTHXBYE\n")
  (define method-call-expression-args
    (run-source method-call-expression-args-src))
  (check-eq? (hash-ref method-call-expression-args 'status) 'ok)
  ;; Adjudication: method-call argument positions accept expressions, matching
  ;; ordinary I IZ call argument semantics.
  (check-equal? (hash-ref method-call-expression-args 'stdout) "9\n")

  (define method-call-arg-eval-order-src
    "HAI 1.3\nI HAS A seq ITZ \"\"\nHOW IZ I mark YR c\n  seq R SMOOSH seq AN c MKAY\n  FOUND YR c\nIF U SAY SO\nO HAI IM obj\n  HOW IZ I see YR a AN YR b\n    FOUND YR seq\n  IF U SAY SO\nKTHX\nVISIBLE obj IZ see YR I IZ mark YR \"C\" MKAY AN YR I IZ mark YR \"D\" MKAY MKAY\nKTHXBYE\n")
  (define method-call-arg-eval-order
    (run-source method-call-arg-eval-order-src))
  (check-eq? (hash-ref method-call-arg-eval-order 'status) 'ok)
  ;; Regression: method-call arguments are evaluated before method body entry.
  (check-equal? (hash-ref method-call-arg-eval-order 'stdout) "CD\n")

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

  (define omgwtf-return-value-overrides-intermediate-slot-mutation-src
    "HAI 1.3\nO HAI IM box\n  I HAS A hits ITZ 0\n  HOW IZ I omgwtf YR slotname\n    hits R SUM OF hits AN 1\n    ME HAS A SRS slotname ITZ \"from-body\"\n    FOUND YR SMOOSH \"from-return-\" AN hits MKAY\n  IF U SAY SO\nKTHX\nVISIBLE box'Z nope\nVISIBLE box'Z nope\nVISIBLE box'Z hits\nVISIBLE box'Z nope\nKTHXBYE\n")
  (define omgwtf-return-value-overrides-intermediate-slot-mutation
    (run-source omgwtf-return-value-overrides-intermediate-slot-mutation-src))
  (check-eq? (hash-ref omgwtf-return-value-overrides-intermediate-slot-mutation 'status) 'ok)
  ;; Policy: resolved missing-slot value is the omgwtf return value, then cached.
  (check-equal? (hash-ref omgwtf-return-value-overrides-intermediate-slot-mutation 'stdout)
                "from-return-1\nfrom-return-1\n1\nfrom-return-1\n")

  (define omgwtf-recursive-same-slot-reentry-src
    "HAI 1.3\nO HAI IM box\n  HOW IZ I omgwtf YR slotname\n    FOUND YR ME'Z SRS slotname\n  IF U SAY SO\nKTHX\nVISIBLE box'Z nope\nKTHXBYE\n")
  (define omgwtf-recursive-same-slot-reentry
    (run-source omgwtf-recursive-same-slot-reentry-src))
  (check-eq? (hash-ref omgwtf-recursive-same-slot-reentry 'status) 'runtime-error)
  ;; Policy: direct omgwtf re-entry on the same unresolved slot is trapped as a
  ;; deterministic runtime error rather than unbounded recursion/divergence.
  (check-true (regexp-match? #px"omgwtf recursion while resolving missing slot: nope"
                             (hash-ref omgwtf-recursive-same-slot-reentry 'error)))

  (define method-call-does-not-trigger-omgwtf-src
    "HAI 1.3\nHOW IZ I helper\n  FOUND YR \"OK\"\nIF U SAY SO\nO HAI IM box\n  HOW IZ I omgwtf YR slotname\n    FOUND YR helper\n  IF U SAY SO\nKTHX\nVISIBLE box IZ nope MKAY\nKTHXBYE\n")
  (define method-call-does-not-trigger-omgwtf
    (run-source method-call-does-not-trigger-omgwtf-src))
  (check-eq? (hash-ref method-call-does-not-trigger-omgwtf 'status) 'runtime-error)
  ;; Policy: <object> IZ <slot> call path does not auto-materialize missing slots
  ;; through omgwtf; only slot access (<object>'Z <slot>) does.
  (check-true (regexp-match? #px"unknown method: nope"
                             (hash-ref method-call-does-not-trigger-omgwtf 'error)))

  (define method-call-uses-prewarmed-omgwtf-slot-src
    "HAI 1.3\nHOW IZ I helper\n  FOUND YR \"OK\"\nIF U SAY SO\nO HAI IM box\n  HOW IZ I omgwtf YR slotname\n    FOUND YR helper\n  IF U SAY SO\nKTHX\nI HAS A warm ITZ box'Z nope\nVISIBLE box IZ nope MKAY\nKTHXBYE\n")
  (define method-call-uses-prewarmed-omgwtf-slot
    (run-source method-call-uses-prewarmed-omgwtf-slot-src))
  (check-eq? (hash-ref method-call-uses-prewarmed-omgwtf-slot 'status) 'ok)
  (check-equal? (hash-ref method-call-uses-prewarmed-omgwtf-slot 'stdout)
                "OK\n")

  (define izmakin-special-slot-runs-on-prototype-src
    "HAI 1.3\nO HAI IM Maker\n  I HAS A seed ITZ 1\n  HOW IZ I izmakin\n    seed R SUM OF seed AN 1\n  IF U SAY SO\nKTHX\nI HAS A first ITZ LIEK A Maker\nI HAS A second ITZ LIEK A Maker\nVISIBLE first'Z seed\nVISIBLE second'Z seed\nKTHXBYE\n")
  (define izmakin-special-slot-runs-on-prototype
    (run-source izmakin-special-slot-runs-on-prototype-src))
  (check-eq? (hash-ref izmakin-special-slot-runs-on-prototype 'status) 'ok)
  (check-equal? (hash-ref izmakin-special-slot-runs-on-prototype 'stdout)
                "3\n3\n")

  (define izmakin-ordering-parent-restore-src
    "HAI 1.3\nO HAI IM base\n  I HAS A tag ITZ \"BASE\"\nKTHX\nO HAI IM mix\n  I HAS A tag ITZ \"MIX\"\n  HOW IZ I izmakin\n    DIFFRINT ME'Z parent AN NOOB\n    O RLY?\n      YA RLY\n        ME HAS A seenTag ITZ ME'Z tag\n        ME HAS A seenParentTag ITZ ME'Z parent'Z tag\n    OIC\n  IF U SAY SO\nKTHX\nO HAI IM child IM LIEK base SMOOSH mix\nKTHX\nVISIBLE child'Z seenTag\nVISIBLE child'Z seenParentTag\nKTHXBYE\n")
  (define izmakin-ordering-parent-restore
    (run-source izmakin-ordering-parent-restore-src))
  (check-eq? (hash-ref izmakin-ordering-parent-restore 'status) 'ok)
  ;; Adjudication: izmakin observes a fully prototyped object where mixin copy
  ;; has already happened and declared parent restoration is complete.
  (check-equal? (hash-ref izmakin-ordering-parent-restore 'stdout)
                "MIX\nBASE\n")

  (define izmakin-reentrant-prototype-src
    "HAI 1.3\nI HAS A ticks ITZ 0\nO HAI IM maker\n  HOW IZ I izmakin\n    DIFFRINT ME'Z parent AN NOOB\n    O RLY?\n      YA RLY\n        ticks R SUM OF ticks AN 1\n        BOTH SAEM ticks AN 1\n        O RLY?\n          YA RLY\n            I HAS A spare ITZ LIEK A maker\n        OIC\n    OIC\n  IF U SAY SO\nKTHX\nI HAS A first ITZ LIEK A maker\nVISIBLE ticks\nKTHXBYE\n")
  (define izmakin-reentrant-prototype
    (run-source izmakin-reentrant-prototype-src))
  (check-eq? (hash-ref izmakin-reentrant-prototype 'status) 'ok)
  ;; Adjudication: reentrant prototyping from izmakin is permitted; each
  ;; constructed prototype runs izmakin exactly once.
  (check-equal? (hash-ref izmakin-reentrant-prototype 'stdout)
                "2\n")

  (define izmakin-failure-surfaced-before-binding-src
    "HAI 1.3\nO HAI IM maker\n  HOW IZ I izmakin\n    DIFFRINT ME'Z parent AN NOOB\n    O RLY?\n      YA RLY\n        VISIBLE ghost\n    OIC\n  IF U SAY SO\nKTHX\nI HAS A prior ITZ \"before\"\nprior\nI HAS A made ITZ LIEK A maker\nKTHXBYE\n")
  (define izmakin-failure-surfaced-before-binding
    (run-source izmakin-failure-surfaced-before-binding-src))
  (check-eq? (hash-ref izmakin-failure-surfaced-before-binding 'status) 'runtime-error)
  ;; Regression: constructor failure from izmakin aborts the declaration path.
  (check-true (regexp-match? #px"unknown identifier: ghost"
                             (hash-ref izmakin-failure-surfaced-before-binding 'error)))

  (define method-global-capture-src
    "HAI 1.3\nI HAS A suffix ITZ \"!\"\nO HAI IM speaker\n  HOW IZ I say YR x\n    FOUND YR SMOOSH x AN suffix MKAY\n  IF U SAY SO\nKTHX\nVISIBLE speaker IZ say YR \"A\" MKAY\nsuffix R \"?\"\nVISIBLE speaker IZ say YR \"A\" MKAY\nKTHXBYE\n")
  (define method-global-capture
    (run-source method-global-capture-src))
  (check-eq? (hash-ref method-global-capture 'status) 'ok)
  ;; Regression: method closures should observe shared lexical boxes.
  (check-equal? (hash-ref method-global-capture 'stdout) "A!\nA?\n")

  (define method-calls-global-function-namespace-src
    "HAI 1.3\nI HAS A x ITZ \"GLOBAL\"\nHOW IZ I pick\n  FOUND YR x\nIF U SAY SO\nO HAI IM box\n  HOW IZ I run\n    I HAS A x ITZ \"LOCAL\"\n    FOUND YR I IZ pick MKAY\n  IF U SAY SO\nKTHX\nVISIBLE box IZ run MKAY\nKTHXBYE\n")
  (define method-calls-global-function-namespace
    (run-source method-calls-global-function-namespace-src))
  (check-eq? (hash-ref method-calls-global-function-namespace 'status) 'ok)
  ;; Regression/policy: I IZ in method context resolves through global function scope.
  (check-equal? (hash-ref method-calls-global-function-namespace 'stdout)
                "GLOBAL\n")

  (define method-local-not-captured-by-global-function-src
    "HAI 1.3\nHOW IZ I readlocal\n  FOUND YR local\nIF U SAY SO\nO HAI IM box\n  HOW IZ I run\n    I HAS A local ITZ 9\n    FOUND YR I IZ readlocal MKAY\n  IF U SAY SO\nKTHX\nVISIBLE box IZ run MKAY\nKTHXBYE\n")
  (define method-local-not-captured-by-global-function
    (run-source method-local-not-captured-by-global-function-src))
  (check-eq? (hash-ref method-local-not-captured-by-global-function 'status) 'runtime-error)
  (check-true (regexp-match? #px"unknown identifier: local"
                             (hash-ref method-local-not-captured-by-global-function
                                       'error)))

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

  (define me-has-a-shadows-inherited-slot-src
    "HAI 1.3\nO HAI IM parent\n  I HAS A v ITZ 1\n  HOW IZ I install\n    ME HAS A v ITZ 9\n    FOUND YR ME'Z v\n  IF U SAY SO\nKTHX\nO HAI IM child IM LIEK parent\nKTHX\nVISIBLE child IZ install MKAY\nVISIBLE child'Z v\nVISIBLE parent'Z v\nKTHXBYE\n")
  (define me-has-a-shadows-inherited-slot
    (run-source me-has-a-shadows-inherited-slot-src))
  (check-eq? (hash-ref me-has-a-shadows-inherited-slot 'status) 'ok)
  ;; Policy: ME HAS A creates/overwrites the receiver's own slot and does not
  ;; mutate the inherited ancestor slot in place.
  (check-equal? (hash-ref me-has-a-shadows-inherited-slot 'stdout)
                "9\n9\n1\n")

  (define me-slot-assign-rhs-sees-prior-value-src
    "HAI 1.3\nO HAI IM box\n  I HAS A n ITZ 4\n  HOW IZ I twice\n    ME'Z n R SUM OF ME'Z n AN ME'Z n\n    FOUND YR ME'Z n\n  IF U SAY SO\nKTHX\nVISIBLE box IZ twice MKAY\nVISIBLE box IZ twice MKAY\nKTHXBYE\n")
  (define me-slot-assign-rhs-sees-prior-value
    (run-source me-slot-assign-rhs-sees-prior-value-src))
  (check-eq? (hash-ref me-slot-assign-rhs-sees-prior-value 'status) 'ok)
  ;; Regression: RHS is evaluated before slot write for ME'Z slot assignment.
  (check-equal? (hash-ref me-slot-assign-rhs-sees-prior-value 'stdout)
                "8\n16\n")

  (define me-outside-method-src
    "HAI 1.3\nHOW IZ I bad\n  FOUND YR ME\nIF U SAY SO\nVISIBLE I IZ bad MKAY\nKTHXBYE\n")
  (define me-outside-method
    (run-source me-outside-method-src))
  (check-eq? (hash-ref me-outside-method 'status) 'runtime-error)
  (check-true (regexp-match? #px"unknown identifier: ME"
                             (hash-ref me-outside-method 'error)))

  (define me-does-not-leak-into-nested-function-from-method-src
    "HAI 1.3\nHOW IZ I readme\n  FOUND YR ME\nIF U SAY SO\nO HAI IM box\n  HOW IZ I run\n    FOUND YR I IZ readme MKAY\n  IF U SAY SO\nKTHX\nVISIBLE box IZ run MKAY\nKTHXBYE\n")
  (define me-does-not-leak-into-nested-function-from-method
    (run-source me-does-not-leak-into-nested-function-from-method-src))
  (check-eq? (hash-ref me-does-not-leak-into-nested-function-from-method 'status)
             'runtime-error)
  ;; Regression/policy: global function calls from method context do not inherit ME.
  (check-true (regexp-match? #px"unknown identifier: ME"
                             (hash-ref me-does-not-leak-into-nested-function-from-method
                                       'error)))

  (define me-available-in-nested-method-call-src
    "HAI 1.3\nO HAI IM box\n  I HAS A n ITZ 1\n  HOW IZ I bump\n    n R SUM OF n AN 1\n    FOUND YR n\n  IF U SAY SO\n  HOW IZ I run\n    FOUND YR ME IZ bump MKAY\n  IF U SAY SO\nKTHX\nVISIBLE box IZ run MKAY\nVISIBLE box'Z n\nKTHXBYE\n")
  (define me-available-in-nested-method-call
    (run-source me-available-in-nested-method-call-src))
  (check-eq? (hash-ref me-available-in-nested-method-call 'status) 'ok)
  (check-equal? (hash-ref me-available-in-nested-method-call 'stdout)
                "2\n2\n")

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

  (define object-block-slot-first-over-lexical-local-src
    "HAI 1.3\nHOW IZ I maker YR x\n  O HAI IM obj\n    I HAS A x ITZ \"slot\"\n    I HAS A seen ITZ x\n  KTHX\n  VISIBLE obj'Z seen\n  FOUND YR x\nIF U SAY SO\nVISIBLE I IZ maker YR \"local\" MKAY\nKTHXBYE\n")
  (define object-block-slot-first-over-lexical-local
    (run-source object-block-slot-first-over-lexical-local-src))
  (check-eq? (hash-ref object-block-slot-first-over-lexical-local 'status) 'ok)
  ;; Regression: object-body lookup is slot-first even against lexical function locals.
  (check-equal? (hash-ref object-block-slot-first-over-lexical-local 'stdout)
                "slot\nlocal\n")

  (define top-level-object-scope-contained-src
    "HAI 1.3\nO HAI IM box\n  I HAS A hidden ITZ 7\nKTHX\nVISIBLE box'Z hidden\nKTHXBYE\n")
  (define top-level-object-scope-contained
    (run-source top-level-object-scope-contained-src))
  (check-eq? (hash-ref top-level-object-scope-contained 'status) 'ok)
  (check-equal? (hash-ref top-level-object-scope-contained 'stdout)
                "7\n")

  (define top-level-object-scope-does-not-leak-src
    "HAI 1.3\nO HAI IM box\n  I HAS A hidden ITZ 7\nKTHX\nVISIBLE hidden\nKTHXBYE\n")
  (define top-level-object-scope-does-not-leak
    (run-source top-level-object-scope-does-not-leak-src))
  (check-eq? (hash-ref top-level-object-scope-does-not-leak 'status) 'runtime-error)
  ;; Regression/policy: object-body declarations remain in object scope, not main scope.
  (check-true (regexp-match? #px"unknown identifier: hidden"
                             (hash-ref top-level-object-scope-does-not-leak 'error)))

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

  (define parent-slot-nonobject-terminates-chain-src
    "HAI 1.3\nO HAI IM parent\n  I HAS A val ITZ \"P\"\nKTHX\nO HAI IM child IM LIEK parent\nKTHX\nchild'Z parent R 0\nVISIBLE child'Z val\nKTHXBYE\n")
  (define parent-slot-nonobject-terminates-chain
    (run-source parent-slot-nonobject-terminates-chain-src))
  (check-eq? (hash-ref parent-slot-nonobject-terminates-chain 'status) 'runtime-error)
  ;; Policy: non-BUKKIT parent values terminate inheritance-chain traversal.
  (check-true (regexp-match? #px"unknown slot: val"
                             (hash-ref parent-slot-nonobject-terminates-chain 'error)))

  (define parent-method-nonobject-terminates-chain-src
    "HAI 1.3\nO HAI IM parent\n  HOW IZ I hi\n    FOUND YR \"P\"\n  IF U SAY SO\nKTHX\nO HAI IM child IM LIEK parent\nKTHX\nchild'Z parent R \"NOPE\"\nVISIBLE child IZ hi MKAY\nKTHXBYE\n")
  (define parent-method-nonobject-terminates-chain
    (run-source parent-method-nonobject-terminates-chain-src))
  (check-eq? (hash-ref parent-method-nonobject-terminates-chain 'status) 'runtime-error)
  (check-true (regexp-match? #px"unknown method: hi"
                             (hash-ref parent-method-nonobject-terminates-chain 'error)))

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

  (define parent-cycle-assignment-existing-name-copy-on-write-src
    "HAI 1.3\nO HAI IM a\n  I HAS A keep ITZ 1\nKTHX\nO HAI IM b IM LIEK a\nKTHX\na'Z parent R b\nb'Z keep R 9\nVISIBLE a'Z keep\nVISIBLE b'Z keep\nKTHXBYE\n")
  (define parent-cycle-assignment-existing-name-copy-on-write
    (run-source parent-cycle-assignment-existing-name-copy-on-write-src))
  (check-eq? (hash-ref parent-cycle-assignment-existing-name-copy-on-write 'status) 'ok)
  ;; Regression: cycle-safe assignment still preserves copy-on-write behavior.
  (check-equal? (hash-ref parent-cycle-assignment-existing-name-copy-on-write 'stdout)
                "1\n9\n")

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

  (define extracted-slot-function-direct-call-namespace-src
    "HAI 1.3\nI HAS A prefix ITZ \"G-\"\nHOW IZ I funkin YR x\n  FOUND YR SMOOSH prefix AN x MKAY\nIF U SAY SO\nO HAI IM box\n  I HAS A prefix ITZ \"O-\"\n  I HAS A f ITZ funkin\nKTHX\nVISIBLE I IZ box'Z f YR \"x\" MKAY\nI HAS A extracted ITZ box'Z f\nVISIBLE I IZ extracted YR \"x\" MKAY\nKTHXBYE\n")
  (define extracted-slot-function-direct-call-namespace
    (run-source extracted-slot-function-direct-call-namespace-src))
  (check-eq? (hash-ref extracted-slot-function-direct-call-namespace 'status) 'ok)
  ;; N16: extracted function values lose slot-call receiver projection; direct
  ;; I IZ invocation uses global call namespace.
  (check-equal? (hash-ref extracted-slot-function-direct-call-namespace 'stdout)
                "O-x\nG-x\n")

  (define inherited-function-slot-assignment-copy-on-write-src
    "HAI 1.3\nHOW IZ I f1\n  FOUND YR \"P\"\nIF U SAY SO\nHOW IZ I f2\n  FOUND YR \"C\"\nIF U SAY SO\nO HAI IM parent\n  I HAS A run ITZ f1\nKTHX\nO HAI IM child IM LIEK parent\nKTHX\nchild'Z run R f2\nVISIBLE I IZ parent'Z run MKAY\nVISIBLE I IZ child'Z run MKAY\nKTHXBYE\n")
  (define inherited-function-slot-assignment-copy-on-write
    (run-source inherited-function-slot-assignment-copy-on-write-src))
  (check-eq? (hash-ref inherited-function-slot-assignment-copy-on-write 'status) 'ok)
  ;; Regression: assigning inherited function-valued slot is copy-on-write.
  (check-equal? (hash-ref inherited-function-slot-assignment-copy-on-write 'stdout)
                "P\nC\n")

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

  (define mixin-static-snapshot-mutable-alias-src
    "HAI 1.3\nO HAI IM parent\nKTHX\nO HAI IM mix\n  I HAS A nested ITZ A BUKKIT\n  nested HAS A n ITZ 1\nKTHX\nO HAI IM child IM LIEK parent SMOOSH mix\nKTHX\nmix'Z nested'Z n R 9\nVISIBLE child'Z nested'Z n\nchild'Z nested'Z n R 7\nVISIBLE mix'Z nested'Z n\nKTHXBYE\n")
  (define mixin-static-snapshot-mutable-alias
    (run-source mixin-static-snapshot-mutable-alias-src))
  (check-eq? (hash-ref mixin-static-snapshot-mutable-alias 'status) 'ok)
  ;; Policy: mixin slot copy is static for direct primitive slots, but mutable
  ;; BUKKIT slot values are copied by reference (call-by-sharing).
  (check-equal? (hash-ref mixin-static-snapshot-mutable-alias 'stdout) "9\n7\n")

  (define mixin-parent-child-combo-src
    "HAI 1.3\nO HAI IM parent\n  I HAS A x ITZ \"parent\"\nKTHX\nO HAI IM mix\n  I HAS A x ITZ \"mix\"\nKTHX\nO HAI IM child IM LIEK parent SMOOSH mix\nKTHX\nVISIBLE child'Z x\nparent'Z x R \"parent2\"\nVISIBLE child'Z x\nKTHXBYE\n")
  (define mixin-parent-child-combo
    (run-source mixin-parent-child-combo-src))
  (check-eq? (hash-ref mixin-parent-child-combo 'status) 'ok)
  (check-equal? (hash-ref mixin-parent-child-combo 'stdout) "mix\nmix\n")

  (define mixin-copied-function-receiver-late-binding-src
    "HAI 1.3\nI HAS A prefix ITZ \"G-\"\nHOW IZ I addprefix YR s\n  FOUND YR SMOOSH prefix AN s MKAY\nIF U SAY SO\nO HAI IM parent\n  I HAS A prefix ITZ \"P-\"\nKTHX\nO HAI IM mix\n  I HAS A prefix ITZ \"M-\"\n  I HAS A run ITZ addprefix\nKTHX\nO HAI IM child IM LIEK parent SMOOSH mix\nKTHX\nchild'Z prefix R \"C-\"\nVISIBLE I IZ child'Z run YR \"x\" MKAY\nI HAS A extracted ITZ child'Z run\nVISIBLE I IZ extracted YR \"x\" MKAY\nKTHXBYE\n")
  (define mixin-copied-function-receiver-late-binding
    (run-source mixin-copied-function-receiver-late-binding-src))
  (check-eq? (hash-ref mixin-copied-function-receiver-late-binding 'status) 'ok)
  ;; N69: copied function slot retains receiver-projected lookup when called via
  ;; slot-call syntax; extracted direct call falls back to global namespace.
  (check-equal? (hash-ref mixin-copied-function-receiver-late-binding 'stdout)
                "C-x\nG-x\n")

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

  (define special-slot-parent-child-shadow-src
    "HAI 1.3\nO HAI IM parent\n  HOW IZ I omgwtf YR slotname\n    FOUND YR SMOOSH \"P-\" AN slotname MKAY\n  IF U SAY SO\n  HOW IZ I izmakin\n    ME HAS A made ITZ \"P\"\n  IF U SAY SO\nKTHX\nO HAI IM child IM LIEK parent\n  HOW IZ I omgwtf YR slotname\n    FOUND YR SMOOSH \"C-\" AN slotname MKAY\n  IF U SAY SO\n  HOW IZ I izmakin\n    ME HAS A made ITZ \"C\"\n  IF U SAY SO\nKTHX\nI HAS A p ITZ LIEK A parent\nI HAS A c ITZ LIEK A child\nVISIBLE p'Z ghost\nVISIBLE c'Z ghost\nVISIBLE p'Z made\nVISIBLE c'Z made\nKTHXBYE\n")
  (define special-slot-parent-child-shadow
    (run-source special-slot-parent-child-shadow-src))
  (check-eq? (hash-ref special-slot-parent-child-shadow 'status) 'ok)
  ;; Regression: child special-slot methods shadow inherited parent special-slot behavior.
  (check-equal? (hash-ref special-slot-parent-child-shadow 'stdout)
                "P-ghost\nC-ghost\nP\nC\n")

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

  (define visible-updates-it-src
    "HAI 1.3\nVISIBLE \"A\" AN \"B\"\nVISIBLE IT\nKTHXBYE\n")
  (define visible-updates-it-result (run-source visible-updates-it-src))
  (check-eq? (hash-ref visible-updates-it-result 'status) 'ok)
  ;; Regression: VISIBLE updates IT to its last argument value.
  (check-equal? (hash-ref visible-updates-it-result 'stdout) "AB\nB\n")

  (define preprocess-order-runtime-src
    "HAI 1.3\nOBTW hidden TLDR, VISIBLE \"A\"\nVISIBLE \"A,B\"\nVISIBLE \"...\"\nVISIBLE \"C\"...\n\"D\"\nKTHXBYE\n")
  (define preprocess-order-runtime-result
    (run-source preprocess-order-runtime-src))
  (check-eq? (hash-ref preprocess-order-runtime-result 'status) 'ok)
  ;; Regression: TLDR handoff + string shielding + continuation ordering.
  (check-equal? (hash-ref preprocess-order-runtime-result 'stdout)
                "A\nA,B\n...\nCD\n")

  (define block-comment-inline-comma-example-src
    "HAI 1.3\nI HAS A VAR ITZ 12, OBTW this is a long comment block\n  see, i have more comments here\n  and here\nTLDR, I HAS A FISH ITZ \"BOB\"\nVISIBLE VAR\nVISIBLE FISH\nKTHXBYE\n")
  (define block-comment-inline-comma-example
    (run-source block-comment-inline-comma-example-src))
  (check-eq? (hash-ref block-comment-inline-comma-example 'status) 'ok)
  ;; Spec lines 79-83: comma-inline OBTW/TLDR handoff is valid.
  (check-equal? (hash-ref block-comment-inline-comma-example 'stdout)
                "12\nBOB\n")

  (define it-update-matrix-src
    "HAI 1.3\nSUM OF 1 AN 1\nI HAS A snap1 ITZ IT\nI HAS A x ITZ 9\nx R 10\nI HAS A snap2 ITZ IT\nO RLY?\n  YA RLY\n    I HAS A y ITZ 1\nOIC\nI HAS A snap3 ITZ IT\nWTF?\n  OMG 2\n    I HAS A z ITZ 1\n    GTFO\nOIC\nI HAS A snap4 ITZ IT\nx IS NOW A YARN\nI HAS A snap5 ITZ IT\nGIMMEH in1\nI HAS A snap6 ITZ IT\nI HAS A obj ITZ A BUKKIT\nobj HAS A n ITZ 7\nI HAS A snap7 ITZ IT\nO HAI IM box\nKTHX\nI HAS A snap8 ITZ IT\nSUM OF 2 AN 3\nI HAS A snap9 ITZ IT\nIM IN YR lp\n  GTFO\nIM OUTTA YR lp\nI HAS A snap10 ITZ IT\nVISIBLE snap1\nVISIBLE snap2\nVISIBLE snap3\nVISIBLE snap4\nVISIBLE snap5\nVISIBLE snap6\nVISIBLE snap7\nVISIBLE snap8\nVISIBLE snap9\nVISIBLE snap10\nKTHXBYE\n")
  (define it-update-matrix-result
    (run-source it-update-matrix-src #:input "hi\n"))
  (check-eq? (hash-ref it-update-matrix-result 'status) 'ok)
  ;; Regression: only IT-updating statement forms change IT; others preserve it.
  (check-equal? (hash-ref it-update-matrix-result 'stdout)
                "2\n2\n2\n2\n10\nhi\n7\n<BUKKIT>\n5\n5\n")

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

  (define lowercase-identifiers-not-literals-src
    "HAI 1.3\nI HAS A win ITZ 3\nI HAS A fail ITZ 4\nI HAS A noob ITZ 5\nI HAS A numbr ITZ 6\nVISIBLE win\nVISIBLE fail\nVISIBLE noob\nVISIBLE numbr\nVISIBLE WIN\nVISIBLE FAIL\nVISIBLE NOOB\nVISIBLE NUMBR\nKTHXBYE\n")
  (define lowercase-identifiers-not-literals-result
    (run-source lowercase-identifiers-not-literals-src))
  (check-eq? (hash-ref lowercase-identifiers-not-literals-result 'status) 'ok)
  (check-equal? (hash-ref lowercase-identifiers-not-literals-result 'stdout)
                "3\n4\n5\n6\nWIN\nFAIL\nNOOB\nNUMBR\n")

  (define reserved-literal-name-declaration-runtime-error-src
    "HAI 1.3\nI HAS A WIN ITZ 1\nKTHXBYE\n")
  (define reserved-literal-name-declaration-runtime-error
    (run-source reserved-literal-name-declaration-runtime-error-src))
  (check-eq? (hash-ref reserved-literal-name-declaration-runtime-error 'status)
             'runtime-error)
  (check-true (regexp-match? #px"declaration uses reserved identifier name: WIN"
                             (hash-ref reserved-literal-name-declaration-runtime-error
                                       'error)))

  (define reserved-special-name-declaration-runtime-error-src
    "HAI 1.3\nI HAS A ME ITZ 1\nKTHXBYE\n")
  (define reserved-special-name-declaration-runtime-error
    (run-source reserved-special-name-declaration-runtime-error-src))
  (check-eq? (hash-ref reserved-special-name-declaration-runtime-error 'status)
             'runtime-error)
  (check-true (regexp-match? #px"declaration uses reserved identifier name: ME"
                             (hash-ref reserved-special-name-declaration-runtime-error
                                       'error)))

  (define reserved-function-name-runtime-error-src
    "HAI 1.3\nHOW IZ I FAIL\n  FOUND YR 1\nIF U SAY SO\nKTHXBYE\n")
  (define reserved-function-name-runtime-error
    (run-source reserved-function-name-runtime-error-src))
  (check-eq? (hash-ref reserved-function-name-runtime-error 'status) 'runtime-error)
  (check-true (regexp-match? #px"function name uses reserved identifier name: FAIL"
                             (hash-ref reserved-function-name-runtime-error
                                       'error)))

  (define reserved-parameter-name-runtime-error-src
    "HAI 1.3\nHOW IZ I f YR NOOB\n  FOUND YR 1\nIF U SAY SO\nKTHXBYE\n")
  (define reserved-parameter-name-runtime-error
    (run-source reserved-parameter-name-runtime-error-src))
  (check-eq? (hash-ref reserved-parameter-name-runtime-error 'status) 'runtime-error)
  (check-true (regexp-match? #px"parameter name uses reserved identifier name: NOOB"
                             (hash-ref reserved-parameter-name-runtime-error
                                       'error)))

  (define reserved-object-name-runtime-error-src
    "HAI 1.3\nO HAI IM TROOF\nKTHX\nKTHXBYE\n")
  (define reserved-object-name-runtime-error
    (run-source reserved-object-name-runtime-error-src))
  (check-eq? (hash-ref reserved-object-name-runtime-error 'status) 'runtime-error)
  (check-true (regexp-match? #px"object name uses reserved identifier name: TROOF"
                             (hash-ref reserved-object-name-runtime-error
                                       'error)))

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

  (define btw-comma-does-not-end-comment-src
    "HAI 1.3\nI HAS A x ITZ 1 BTW comment, x R 2\nVISIBLE x\nKTHXBYE\n")
  (define btw-comma-does-not-end-comment
    (run-source btw-comma-does-not-end-comment-src))
  (check-eq? (hash-ref btw-comma-does-not-end-comment 'status) 'ok)
  ;; Spec line 40: comma after BTW is ignored until newline.
  (check-equal? (hash-ref btw-comma-does-not-end-comment 'stdout) "1\n")

  (define btw-inside-yarn-is-literal-src
    "HAI 1.3\nVISIBLE \"A BTW B, C\"\nKTHXBYE\n")
  (define btw-inside-yarn-is-literal
    (run-source btw-inside-yarn-is-literal-src))
  (check-eq? (hash-ref btw-inside-yarn-is-literal 'status) 'ok)
  ;; Spec line 42: comment/soft-break controls are ignored inside quoted strings.
  (check-equal? (hash-ref btw-inside-yarn-is-literal 'stdout) "A BTW B, C\n")

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

  (define pua-placeholder-start (string (integer->char #xE000)))
  (define pua-placeholder-end (string (integer->char #xE001)))
  (define format-string-private-use-literal-src
    (string-append
     "HAI 1.3\n"
     "VISIBLE \"" pua-placeholder-start "\"\n"
     "VISIBLE \"" pua-placeholder-end "\"\n"
     "KTHXBYE\n"))
  (define format-string-private-use-literal
    (run-source format-string-private-use-literal-src))
  (check-eq? (hash-ref format-string-private-use-literal 'status) 'ok)
  (check-equal? (hash-ref format-string-private-use-literal 'stdout)
                (string-append pua-placeholder-start "\n"
                               pua-placeholder-end "\n"))

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

  (define ast-function-vs-method-def-shape-src
    "HAI 1.3\nI HAS A box ITZ A BUKKIT\nHOW IZ I plain\n  FOUND YR 1\nIF U SAY SO\nHOW IZ box meth\n  FOUND YR 2\nIF U SAY SO\nKTHXBYE\n")
  (define ast-function-vs-method-def-shape
    (parse-program ast-function-vs-method-def-shape-src))
  (define ast-function-vs-method-def-stmts
    (program-statements ast-function-vs-method-def-shape))
  (define ast-function-def
    (for/first ([s (in-list ast-function-vs-method-def-stmts)]
                #:when (stmt-function-def? s))
      s))
  (define ast-method-def
    (for/first ([s (in-list ast-function-vs-method-def-stmts)]
                #:when (stmt-method-def? s))
      s))
  (check-not-false ast-function-def)
  (check-not-false ast-method-def)
  ;; N01: HOW IZ I and HOW IZ <receiver> compile to distinct AST nodes.
  (check-true (expr-literal? (stmt-function-def-name ast-function-def)))
  (check-equal? (expr-literal-value (stmt-function-def-name ast-function-def))
                "plain")
  (check-true (expr-ident? (stmt-method-def-receiver ast-method-def)))
  (check-equal? (expr-ident-name (stmt-method-def-receiver ast-method-def))
                "box")
  (check-true (expr-literal? (stmt-method-def-name ast-method-def)))
  (check-equal? (expr-literal-value (stmt-method-def-name ast-method-def))
                "meth")

  (define ast-stmt-node-split-src
    "HAI 1.3\nI HAS A obj ITZ A BUKKIT\nI HAS A x ITZ 1\nx R 2\nx IS NOW A NUMBAR\nobj HAS A y ITZ 3\nKTHXBYE\n")
  (define ast-stmt-node-split
    (parse-program ast-stmt-node-split-src))
  (define ast-stmt-node-split-stmts
    (program-statements ast-stmt-node-split))
  (define n-declare
    (for/sum ([s (in-list ast-stmt-node-split-stmts)])
      (if (stmt-declare? s) 1 0)))
  (define n-assign
    (for/sum ([s (in-list ast-stmt-node-split-stmts)])
      (if (stmt-assign? s) 1 0)))
  (define n-cast
    (for/sum ([s (in-list ast-stmt-node-split-stmts)])
      (if (stmt-cast? s) 1 0)))
  (define n-slot-set
    (for/sum ([s (in-list ast-stmt-node-split-stmts)])
      (if (stmt-slot-set? s) 1 0)))
  ;; N03: declaration/assignment/cast/slot-set remain distinct statement nodes.
  (check-equal? n-declare 2)
  (check-equal? n-assign 1)
  (check-equal? n-cast 1)
  (check-equal? n-slot-set 1)

  (define ast-srs-sites-shape-src
    "HAI 1.3\nI HAS A key ITZ \"name\"\nI HAS A SRS key ITZ 1\nI HAS A obj ITZ A BUKKIT\nobj HAS A SRS key ITZ I IZ id YR 2 MKAY\nVISIBLE obj IZ SRS key MKAY\nHOW IZ I id YR x\n  FOUND YR x\nIF U SAY SO\nKTHXBYE\n")
  (define ast-srs-sites-shape
    (parse-program ast-srs-sites-shape-src))
  (define ast-srs-sites-stmts
    (program-statements ast-srs-sites-shape))
  (define ast-srs-declare
    (for/first ([s (in-list ast-srs-sites-stmts)]
                #:when (and (stmt-declare? s)
                            (expr-srs? (stmt-declare-target s))))
      s))
  (define ast-srs-slot-set
    (for/first ([s (in-list ast-srs-sites-stmts)]
                #:when (and (stmt-slot-set? s)
                            (expr-srs? (stmt-slot-set-slot s))))
      s))
  (define ast-srs-visible-method-call
    (for/first ([s (in-list ast-srs-sites-stmts)]
                #:when (stmt-visible? s))
      s))
  (check-not-false ast-srs-declare)
  (check-not-false ast-srs-slot-set)
  (check-not-false ast-srs-visible-method-call)
  ;; N04: SRS is preserved as an explicit AST node in identifier-sensitive sites.
  (define ast-srs-visible-expr
    (car (stmt-visible-exprs ast-srs-visible-method-call)))
  (check-true (expr-method-call? ast-srs-visible-expr))
  (check-true (expr-srs? (expr-method-call-name ast-srs-visible-expr)))

  (define ast-smoosh-disambiguation-src
    "HAI 1.3\nI HAS A txt ITZ SMOOSH \"A\" AN \"B\" MKAY\nI HAS A Parent ITZ A BUKKIT\nI HAS A Mix ITZ A BUKKIT\nI HAS A child ITZ A Parent SMOOSH Mix\nKTHXBYE\n")
  (define ast-smoosh-disambiguation
    (parse-program ast-smoosh-disambiguation-src))
  (define ast-smoosh-disambiguation-stmts
    (program-statements ast-smoosh-disambiguation))
  (define ast-smoosh-expr-declare
    (for/first ([s (in-list ast-smoosh-disambiguation-stmts)]
                #:when (and (stmt-declare? s)
                            (expr-ident? (stmt-declare-target s))
                            (string=? (expr-ident-name (stmt-declare-target s))
                                      "txt")))
      s))
  (define ast-prototype-declare
    (for/first ([s (in-list ast-smoosh-disambiguation-stmts)]
                #:when (and (stmt-declare? s)
                            (expr-ident? (stmt-declare-target s))
                            (string=? (expr-ident-name (stmt-declare-target s))
                                      "child")))
      s))
  (check-not-false ast-smoosh-expr-declare)
  (check-not-false ast-prototype-declare)
  ;; N05: SMOOSH expression and prototype-mixin SMOOSH parse into distinct AST forms.
  (check-true (expr-variadic? (stmt-declare-init ast-smoosh-expr-declare)))
  (check-equal? (expr-variadic-op (stmt-declare-init ast-smoosh-expr-declare))
                "SMOOSH")
  (check-true (expr-prototype? (stmt-declare-init ast-prototype-declare)))

  (define i-token-role-shape-src
    "HAI 1.3\nHOW IZ I ping\n  FOUND YR 7\nIF U SAY SO\nVISIBLE I IZ ping MKAY\nO HAI IM box\n  I HAS A n ITZ 1\n  HOW IZ I bump\n    n R SUM OF n AN 1\n    FOUND YR n\n  IF U SAY SO\nKTHX\nVISIBLE box IZ bump MKAY\nVISIBLE box'Z n\nKTHXBYE\n")
  (define i-token-role-shape
    (parse-program i-token-role-shape-src))
  (define i-token-role-stmts
    (program-statements i-token-role-shape))
  (define i-token-visible-call
    (for/first ([s (in-list i-token-role-stmts)]
                #:when (and (stmt-visible? s)
                            (pair? (stmt-visible-exprs s))
                            (expr-call? (car (stmt-visible-exprs s)))))
      s))
  (define i-token-object-stmt
    (for/first ([s (in-list i-token-role-stmts)]
                #:when (stmt-object-def? s))
      s))
  (check-not-false i-token-visible-call)
  (check-not-false i-token-object-stmt)
  ;; N07: token I has distinct contextual roles (call marker, declaration marker,
  ;; and object-body function-to-method declaration form).
  (define i-token-call-expr
    (car (stmt-visible-exprs i-token-visible-call)))
  (check-true (expr-literal? (expr-call-name i-token-call-expr)))
  (check-equal? (expr-literal-value (expr-call-name i-token-call-expr))
                "ping")
  (define i-token-object-body
    (stmt-object-def-body i-token-object-stmt))
  (check-true
   (for/or ([s (in-list i-token-object-body)])
     (and (stmt-declare? s)
          (expr-ident? (stmt-declare-target s))
          (string=? (expr-ident-name (stmt-declare-target s))
                    "n"))))
  (check-true
   (for/or ([s (in-list i-token-object-body)])
     (and (stmt-function-def? s)
          (expr-literal? (stmt-function-def-name s))
          (string=? (expr-literal-value (stmt-function-def-name s))
                    "bump"))))
  (define i-token-role-run
    (run-source i-token-role-shape-src))
  (check-eq? (hash-ref i-token-role-run 'status) 'ok)
  (check-equal? (hash-ref i-token-role-run 'stdout) "7\n2\n2\n")

  (define special-names-global-vs-slot-policy-src
    "HAI 1.3\nI HAS A parent ITZ \"GLOBAL-PARENT\"\nI HAS A omgwtf ITZ \"GLOBAL-OMG\"\nI HAS A izmakin ITZ \"GLOBAL-IZ\"\nO HAI IM base\n  I HAS A tag ITZ \"BASE\"\nKTHX\nO HAI IM child IM LIEK base\nKTHX\nVISIBLE parent\nVISIBLE omgwtf\nVISIBLE izmakin\nVISIBLE child'Z parent'Z tag\nKTHXBYE\n")
  (define special-names-global-vs-slot-policy
    (run-source special-names-global-vs-slot-policy-src))
  (check-eq? (hash-ref special-names-global-vs-slot-policy 'status) 'ok)
  ;; N08: parent/omgwtf/izmakin are not globally reserved names; special behavior
  ;; applies in slot context while globals with those names remain ordinary vars.
  (check-equal? (hash-ref special-names-global-vs-slot-policy 'stdout)
                "GLOBAL-PARENT\nGLOBAL-OMG\nGLOBAL-IZ\nBASE\n")

  (define it-redeclare-runtime-error-src
    "HAI 1.3\nI HAS A IT ITZ 1\nKTHXBYE\n")
  (define it-redeclare-runtime-error
    (run-source it-redeclare-runtime-error-src))
  (check-eq? (hash-ref it-redeclare-runtime-error 'status) 'runtime-error)
  (check-true (regexp-match? #px"identifier already declared in this scope: IT"
                             (hash-ref it-redeclare-runtime-error 'error)))

  (define preprocess-confluence-n09-src
    "HAI 1.3\nVISIBLE \"BTW, OBTW, TLDR, ...\"\nVISIBLE \"A\"...\n\"B\", VISIBLE \"C\" BTW ignored tail\nOBTW hidden TLDR, VISIBLE \"D\"\nKTHXBYE\n")
  (define preprocess-confluence-n09
    (run-source preprocess-confluence-n09-src))
  (check-eq? (hash-ref preprocess-confluence-n09 'status) 'ok)
  ;; N09: statement-boundary normalization composes with string shielding,
  ;; continuation, BTW, and inline OBTW/TLDR handoff.
  (check-equal? (hash-ref preprocess-confluence-n09 'stdout)
                "BTW, OBTW, TLDR, ...\nAB\nC\nD\n")

  (define optional-article-scope-n38-src
    "HAI 1.3\nI HAS A t ITZ NUMBR\nI HAS A u ITZ A NUMBR\nVISIBLE t\nVISIBLE u\nKTHXBYE\n")
  (define optional-article-scope-n38
    (run-source optional-article-scope-n38-src))
  (check-eq? (hash-ref optional-article-scope-n38 'status) 'ok)
  ;; N38: article optionality is grammar-site specific:
  ;; ITZ NUMBR is a TYPE literal expression; ITZ A NUMBR is typed default init.
  (check-equal? (hash-ref optional-article-scope-n38 'stdout)
                "NUMBR\n0\n")

  (define continuation-trailing-space-tab-n45-src
    "HAI 1.3\nVISIBLE SMOOSH \"A\" AN ...   \n\"B\" MKAY\nVISIBLE SMOOSH \"C\" AN …\t\n\"D\" MKAY\nKTHXBYE\n")
  (define continuation-trailing-space-tab-n45
    (run-source continuation-trailing-space-tab-n45-src))
  (check-eq? (hash-ref continuation-trailing-space-tab-n45 'status) 'ok)
  (check-equal? (hash-ref continuation-trailing-space-tab-n45 'stdout)
                "AB\nCD\n")

  (define tldr-handoff-space-comma-n46-src
    "HAI 1.3\nOBTW hidden TLDR   , VISIBLE \"OK\"\nKTHXBYE\n")
  (define tldr-handoff-space-comma-n46
    (run-source tldr-handoff-space-comma-n46-src))
  (check-eq? (hash-ref tldr-handoff-space-comma-n46 'status) 'ok)
  (check-equal? (hash-ref tldr-handoff-space-comma-n46 'stdout)
                "OK\n")

  (define cast-invalid-yarn-dotdot-n48-src
    "HAI 1.3\nVISIBLE MAEK \"1..2\" A NUMBR\nKTHXBYE\n")
  (define cast-invalid-yarn-dotdot-n48
    (run-source cast-invalid-yarn-dotdot-n48-src))
  (check-eq? (hash-ref cast-invalid-yarn-dotdot-n48 'status) 'runtime-error)
  (check-true (regexp-match? #px"cannot cast YARN to numeric value"
                             (hash-ref cast-invalid-yarn-dotdot-n48 'error)))

  (define cast-invalid-yarn-double-minus-n48-src
    "HAI 1.3\nVISIBLE MAEK \"--1\" A NUMBAR\nKTHXBYE\n")
  (define cast-invalid-yarn-double-minus-n48
    (run-source cast-invalid-yarn-double-minus-n48-src))
  (check-eq? (hash-ref cast-invalid-yarn-double-minus-n48 'status) 'runtime-error)
  (check-true (regexp-match? #px"cannot cast YARN to numeric value"
                             (hash-ref cast-invalid-yarn-double-minus-n48 'error)))

  (define cast-invalid-yarn-leading-dot-n48-src
    "HAI 1.3\nVISIBLE MAEK \".5\" A NUMBAR\nKTHXBYE\n")
  (define cast-invalid-yarn-leading-dot-n48
    (run-source cast-invalid-yarn-leading-dot-n48-src))
  (check-eq? (hash-ref cast-invalid-yarn-leading-dot-n48 'status) 'runtime-error)
  (check-true (regexp-match? #px"cannot cast YARN to numeric value"
                             (hash-ref cast-invalid-yarn-leading-dot-n48 'error)))

  (define duplicate-loop-labels-n57-src
    "HAI 1.3\nI HAS A out ITZ \"\"\nIM IN YR lp\n  out R SMOOSH out AN \"A\" MKAY\n  IM IN YR lp\n    out R SMOOSH out AN \"B\" MKAY\n    GTFO\n  IM OUTTA YR lp\n  GTFO\nIM OUTTA YR lp\nVISIBLE out\nKTHXBYE\n")
  (define duplicate-loop-labels-n57
    (run-source duplicate-loop-labels-n57-src))
  (check-eq? (hash-ref duplicate-loop-labels-n57 'status) 'ok)
  ;; N57 policy: labels are case-sensitive; duplicate names are permitted and
  ;; matched structurally by each loop's own IM IN/IM OUTTA pair.
  (check-equal? (hash-ref duplicate-loop-labels-n57 'stdout)
                "AB\n")

  (define method-def-receiver-missing-n68-src
    "HAI 1.3\nHOW IZ ghost ping\n  FOUND YR 1\nIF U SAY SO\nKTHXBYE\n")
  (define method-def-receiver-missing-n68
    (run-source method-def-receiver-missing-n68-src))
  (check-eq? (hash-ref method-def-receiver-missing-n68 'status) 'runtime-error)
  (check-true (regexp-match? #px"unknown identifier: ghost"
                             (hash-ref method-def-receiver-missing-n68 'error)))

  (define method-def-receiver-nonbukkit-n68-src
    "HAI 1.3\nI HAS A ghost ITZ 1\nHOW IZ ghost ping\n  FOUND YR 1\nIF U SAY SO\nKTHXBYE\n")
  (define method-def-receiver-nonbukkit-n68
    (run-source method-def-receiver-nonbukkit-n68-src))
  (check-eq? (hash-ref method-def-receiver-nonbukkit-n68 'status) 'runtime-error)
  (check-true (regexp-match? #px"method declaration requires BUKKIT receiver"
                             (hash-ref method-def-receiver-nonbukkit-n68 'error)))

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
