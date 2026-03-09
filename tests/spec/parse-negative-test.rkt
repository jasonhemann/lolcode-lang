#lang racket/base

(require rackunit
         racket/file
         "../../src/lolcode/lexer.rkt"
         "../../src/lolcode/main.rkt")

(define here
  (or (current-load-relative-directory)
      (current-directory)))

(module+ test
  (define (capture-message thunk)
    (with-handlers ([exn:fail? exn-message])
      (thunk)
      #f))

  (define missing-kthxbye
    "HAI 1.3\nVISIBLE \"OH HAI\"\n")
  (define missing-kthxbye-msg
    (capture-message (lambda () (parse-program missing-kthxbye))))
  (check-true (string? missing-kthxbye-msg))
  (check-true (regexp-match? #px"syntax error: unexpected EOF" missing-kthxbye-msg))
  (check-true (regexp-match? #px"line 3, col 1" missing-kthxbye-msg))
  (check-true (regexp-match? #px"\\^" missing-kthxbye-msg))
  (check-false (regexp-match? #px"hint:" missing-kthxbye-msg))

  (define missing-version
    "HAI\nVISIBLE \"OH HAI\"\nKTHXBYE\n")
  (define missing-version-msg
    (capture-message (lambda () (parse-program missing-version))))
  (check-true (string? missing-version-msg))
  (check-true (regexp-match? #px"syntax error: unexpected NEWLINE" missing-version-msg))

  (define unsupported-v12
    "HAI 1.2\nVISIBLE \"legacy\"\nKTHXBYE\n")
  (define unsupported-v12-msg
    (capture-message (lambda () (parse-program unsupported-v12))))
  (check-true (string? unsupported-v12-msg))
  (check-true (regexp-match? #px"unsupported version: 1\\.2" unsupported-v12-msg))

  (define external-lci-issue-0043-path
    (build-path here
                ".."
                "regression-evidence"
                "external"
                "fixtures"
                "lci"
                "wave_01"
                "issue_0043"
                "repro.lol"))
  (define external-lci-issue-0043
    (file->string external-lci-issue-0043-path))
  (define external-lci-issue-0043-msg
    (capture-message (lambda () (parse-program external-lci-issue-0043))))
  (check-true (string? external-lci-issue-0043-msg))
  (check-true (regexp-match? #px"unsupported version: 1\\.2"
                             external-lci-issue-0043-msg))

  (define unsupported-v14
    "HAI 1.4\nVISIBLE \"future\"\nKTHXBYE\n")
  (define unsupported-v14-msg
    (capture-message (lambda () (parse-program unsupported-v14))))
  (check-true (string? unsupported-v14-msg))
  (check-true (regexp-match? #px"unsupported version: 1\\.4" unsupported-v14-msg))

  (define lowercase-keywords-program
    "hai 1.3\nvisible \"nope\"\nkthxbye\n")
  (check-exn #px"syntax error:"
             (lambda () (parse-program lowercase-keywords-program)))

  (define editorial-how-duz-i-form
    "HAI 1.3\nHOW DUZ I addin YR x\n  FOUND YR x\nIF U SAY SO\nKTHXBYE\n")
  (check-exn #px"syntax error:"
             (lambda () (parse-program editorial-how-duz-i-form)))

  (define can-has-extension
    "HAI 1.3\nCAN HAS STRING?\nKTHXBYE\n")
  (define can-has-extension-msg
    (capture-message (lambda () (parse-program can-has-extension))))
  (check-true (string? can-has-extension-msg))
  (check-true (regexp-match? #px"(syntax error:|invalid identifier syntax:)"
                             can-has-extension-msg))

  (define mixin-inheritance
    "HAI 1.3\nO HAI IM Parent\nKTHX\nO HAI IM Mix\nKTHX\nO HAI IM Child IM LIEK Parent SMOOSH Mix\nKTHX\nKTHXBYE\n")
  (check-not-exn
   (lambda () (parse-program mixin-inheritance)))

  (define mixin-declare
    "HAI 1.3\nI HAS A Parent ITZ A BUKKIT\nI HAS A Mix ITZ A BUKKIT\nI HAS A Child ITZ A Parent SMOOSH Mix\nKTHXBYE\n")
  (check-not-exn
   (lambda () (parse-program mixin-declare)))

  (define invalid-plain-a-parent-declare
    "HAI 1.3\nI HAS A River ITZ A BUKKIT\nI HAS A bad ITZ A River\nKTHXBYE\n")
  (check-exn #px"invalid declaration type in ITZ A"
             (lambda () (parse-program invalid-plain-a-parent-declare)))

  (define unterminated-string
    "HAI 1.3\nVISIBLE \"oops\nKTHXBYE\n")
  (check-exn #px"unterminated string literal at line 2, col 9"
             (lambda () (parse-program unterminated-string)))

  (define unterminated-format-placeholder
    "HAI 1.3\nVISIBLE \"oops :{name\"\nKTHXBYE\n")
  (check-exn #px"unterminated :\\{\\.\\.\\.\\} placeholder in string literal"
             (lambda () (parse-program unterminated-format-placeholder)))

  (define invalid-unicode-codepoint
    "HAI 1.3\nVISIBLE \":(110000)\"\nKTHXBYE\n")
  (check-exn #px"invalid Unicode code point in string literal"
             (lambda () (parse-program invalid-unicode-codepoint)))

  (define invalid-unicode-surrogate-codepoint
    "HAI 1.3\nVISIBLE \":(D800)\"\nKTHXBYE\n")
  (check-exn #px"invalid Unicode code point in string literal"
             (lambda () (parse-program invalid-unicode-surrogate-codepoint)))

  (define invalid-unicode-normative-name
    "HAI 1.3\nVISIBLE \":[:{var}]\"\nKTHXBYE\n")
  (check-exn #px"invalid Unicode normative name in string literal"
             (lambda () (parse-program invalid-unicode-normative-name)))

  (define lowercase-unicode-normative-name
    "HAI 1.3\nVISIBLE \":[dollar sign]\"\nKTHXBYE\n")
  (check-exn #px"invalid Unicode normative name in string literal"
             (lambda () (parse-program lowercase-unicode-normative-name)))

  (define spaced-unicode-normative-name
    "HAI 1.3\nVISIBLE \":[DOLLAR  SIGN]\"\nKTHXBYE\n")
  (check-exn #px"invalid Unicode normative name in string literal"
             (lambda () (parse-program spaced-unicode-normative-name)))

  (define tabbed-unicode-normative-name
    "HAI 1.3\nVISIBLE \":[DOLLAR\tSIGN]\"\nKTHXBYE\n")
  (check-exn #px"invalid Unicode normative name in string literal"
             (lambda () (parse-program tabbed-unicode-normative-name)))

  (define unicode-ellipsis-continuation
    "HAI 1.3\nVISIBLE \"A\"…\n\"B\"\nKTHXBYE\n")
  (check-not-exn
   (lambda () (parse-program unicode-ellipsis-continuation)))

  (define comma-plus-continuation-lex
    "VISIBLE \"A\",...\nVISIBLE \"B\"\n")
  (define comma-plus-continuation-toks
    (lex-source comma-plus-continuation-lex))
  (check-equal? (map token-type comma-plus-continuation-toks)
                '(WORD STRING NEWLINE WORD STRING NEWLINE EOF))
  (check-equal? (token-lexeme (list-ref comma-plus-continuation-toks 2))
                ",")

  (define lowercase-comment-markers-lex
    "btw not-a-comment\nobtw still-not-comment\ntldr\n")
  (define lowercase-comment-markers-toks
    (lex-source lowercase-comment-markers-lex))
  (check-equal? (map token-type lowercase-comment-markers-toks)
                '(WORD WORD NEWLINE WORD WORD NEWLINE WORD NEWLINE EOF))
  (check-equal? (token-lexeme (car lowercase-comment-markers-toks))
                "btw")
  (check-equal? (token-lexeme (list-ref lowercase-comment-markers-toks 3))
                "obtw")

  (define lowercase-slot-operator-lex
    "obj'z\n")
  (define lowercase-slot-operator-toks
    (lex-source lowercase-slot-operator-lex))
  (check-equal? (map token-type lowercase-slot-operator-toks)
                '(WORD NEWLINE EOF))
  (check-equal? (token-lexeme (car lowercase-slot-operator-toks))
                "obj'z")

  (define comma-plus-continuation-program
    "HAI 1.3\nVISIBLE \"A\",...\nVISIBLE \"B\"\nKTHXBYE\n")
  (check-not-exn
   (lambda () (parse-program comma-plus-continuation-program)))

  (define continuation-then-comma
    "HAI 1.3\nVISIBLE \"A\"...,\nVISIBLE \"B\"\nKTHXBYE\n")
  (check-exn #px"line continuation marker must be at end of line"
             (lambda () (parse-program continuation-then-comma)))

  (define continuation-followed-by-empty-line
    "HAI 1.3\nVISIBLE \"A\"...\n\n\"B\"\nKTHXBYE\n")
  (check-exn #px"line continuation may not be followed by an empty line"
             (lambda () (parse-program continuation-followed-by-empty-line)))

  (define continuation-only-line-may-include-empty-line
    "HAI 1.3\nVISIBLE \"A\"...\n...\n\n\"B\"\nKTHXBYE\n")
  (check-not-exn
   (lambda () (parse-program continuation-only-line-may-include-empty-line)))

  (define continuation-with-trailing-comment
    "HAI 1.3\nVISIBLE \"A\"... BTW comment\nVISIBLE \"B\"\nKTHXBYE\n")
  (check-exn #px"line continuation marker must be at end of line"
             (lambda () (parse-program continuation-with-trailing-comment)))

  (define ellipsis-in-comment-is-ignored
    "HAI 1.3\nVISIBLE \"A\" BTW ...\nVISIBLE \"B\"\nKTHXBYE\n")
  (check-not-exn
   (lambda () (parse-program ellipsis-in-comment-is-ignored)))

  (define inline-block-comment-tldr-handoff
    "HAI 1.3\nOBTW hidden TLDR, VISIBLE \"OK\"\nKTHXBYE\n")
  (check-not-exn
   (lambda () (parse-program inline-block-comment-tldr-handoff)))

  (define block-comment-tldr-trailing-statement-without-comma
    "HAI 1.3\nOBTW hidden\nTLDR VISIBLE \"OK\"\nKTHXBYE\n")
  (check-exn #px"TLDR must be followed by newline or comma"
             (lambda ()
               (parse-program block-comment-tldr-trailing-statement-without-comma)))

  (define one-line-minimal-program
    "HAI 1.3, KTHXBYE\n")
  (check-not-exn
   (lambda () (parse-program one-line-minimal-program)))

  (define one-line-missing-close
    "HAI 1.3\n")
  (define one-line-missing-close-msg
    (capture-message (lambda () (parse-program one-line-missing-close))))
  (check-true (string? one-line-missing-close-msg))
  (check-true (regexp-match? #px"syntax error: unexpected EOF"
                             one-line-missing-close-msg))

  (define one-line-extra-after-close
    "HAI 1.3, KTHXBYE, VISIBLE \"x\"\n")
  (check-exn #px"syntax error: unexpected VISIBLE"
             (lambda () (parse-program one-line-extra-after-close)))

  (define malformed-number-spaced-sign
    "HAI 1.3\nI HAS A x ITZ - 123\nKTHXBYE\n")
  (check-exn #px"invalid numeric literal"
             (lambda () (parse-program malformed-number-spaced-sign)))

  (define malformed-number-multi-dot
    "HAI 1.3\nI HAS A x ITZ 1..23\nKTHXBYE\n")
  (check-exn #px"invalid numeric literal"
             (lambda () (parse-program malformed-number-multi-dot)))

  (define malformed-number-trailing-dot
    "HAI 1.3\nI HAS A x ITZ 2.\nKTHXBYE\n")
  (check-exn #px"invalid numeric literal"
             (lambda () (parse-program malformed-number-trailing-dot)))

  (define malformed-number-leading-dot
    "HAI 1.3\nI HAS A x ITZ .5\nKTHXBYE\n")
  (check-exn #px"(invalid numeric literal|invalid identifier syntax)"
             (lambda () (parse-program malformed-number-leading-dot)))

  (define malformed-number-minus-leading-dot
    "HAI 1.3\nI HAS A x ITZ -.5\nKTHXBYE\n")
  (check-exn #px"(invalid numeric literal|invalid identifier syntax)"
             (lambda () (parse-program malformed-number-minus-leading-dot)))

  (define malformed-number-negative-trailing-dot
    "HAI 1.3\nI HAS A x ITZ -0.\nKTHXBYE\n")
  (check-exn #px"(invalid numeric literal|invalid identifier syntax)"
             (lambda () (parse-program malformed-number-negative-trailing-dot)))

  (define malformed-number-leading-plus-int
    "HAI 1.3\nI HAS A x ITZ +123\nKTHXBYE\n")
  (check-exn #px"invalid identifier syntax"
             (lambda () (parse-program malformed-number-leading-plus-int)))

  (define malformed-number-leading-plus-float
    "HAI 1.3\nI HAS A x ITZ +1.23\nKTHXBYE\n")
  (check-exn #px"invalid identifier syntax"
             (lambda () (parse-program malformed-number-leading-plus-float)))

  (define invalid-ident-leading-underscore
    "HAI 1.3\nI HAS A _x ITZ 1\nKTHXBYE\n")
  (check-exn #px"invalid identifier syntax"
             (lambda () (parse-program invalid-ident-leading-underscore)))

  (define invalid-ident-with-dash
    "HAI 1.3\nI HAS A x-y ITZ 1\nKTHXBYE\n")
  (check-exn #px"(invalid identifier syntax|syntax error: unexpected SLOT)"
             (lambda () (parse-program invalid-ident-with-dash)))

  (define invalid-ident-symbol-only
    "HAI 1.3\nI HAS A ++ ITZ 1\nKTHXBYE\n")
  (check-exn #px"invalid identifier syntax"
             (lambda () (parse-program invalid-ident-symbol-only)))

  (define and-as-identifier-when-an-omitted
    "HAI 1.3\nVISIBLE SUM OF 1 AND 2\nKTHXBYE\n")
  (check-exn #px"syntax error: unexpected NUMBER"
             (lambda () (parse-program and-as-identifier-when-an-omitted)))

  (for ([src (in-list
              (list
               "HAI 1.3\nVISIBLE SUM OF 1 AND 2\nKTHXBYE\n"
               "HAI 1.3\nVISIBLE DIFF OF 5 AND 2\nKTHXBYE\n"
               "HAI 1.3\nVISIBLE PRODUKT OF 3 AND 4\nKTHXBYE\n"
               "HAI 1.3\nVISIBLE QUOSHUNT OF 6 AND 2\nKTHXBYE\n"
               "HAI 1.3\nVISIBLE MOD OF 7 AND 4\nKTHXBYE\n"
               "HAI 1.3\nVISIBLE BIGGR OF 5 AND 2\nKTHXBYE\n"
               "HAI 1.3\nVISIBLE SMALLR OF 5 AND 2\nKTHXBYE\n"
               "HAI 1.3\nVISIBLE BOTH OF WIN AND FAIL\nKTHXBYE\n"
               "HAI 1.3\nVISIBLE EITHER OF FAIL AND WIN\nKTHXBYE\n"
               "HAI 1.3\nVISIBLE WON OF WIN AND FAIL\nKTHXBYE\n"
               "HAI 1.3\nVISIBLE BOTH SAEM 3 AND 3\nKTHXBYE\n"
               "HAI 1.3\nVISIBLE DIFFRINT 3 AND 4\nKTHXBYE\n"))])
    (check-exn #px"syntax error:"
               (lambda () (parse-program src))))

  (define and-as-identifier-with-explicit-an
    "HAI 1.3\nI HAS A AND ITZ 2\nVISIBLE SUM OF 1 AN AND\nKTHXBYE\n")
  (check-not-exn
   (lambda () (parse-program and-as-identifier-with-explicit-an)))

  (define misspelled-difference-op
    "HAI 1.3\nVISIBLE DIFFERENCE OF 5 AN 2\nKTHXBYE\n")
  (define misspelled-difference-op-msg
    (capture-message (lambda () (parse-program misspelled-difference-op))))
  (check-true (string? misspelled-difference-op-msg))
  (check-true (regexp-match? #px"syntax error:" misspelled-difference-op-msg))
  (check-false (regexp-match? #px"did you mean" misspelled-difference-op-msg))

  (define misspelled-quoshunt-op
    "HAI 1.3\nVISIBLE QOUSHUNT OF 6 AN 2\nKTHXBYE\n")
  (define misspelled-quoshunt-op-msg
    (capture-message (lambda () (parse-program misspelled-quoshunt-op))))
  (check-true (string? misspelled-quoshunt-op-msg))
  (check-true (regexp-match? #px"syntax error:" misspelled-quoshunt-op-msg))
  (check-false (regexp-match? #px"did you mean" misspelled-quoshunt-op-msg))

  (define corrected-operators
    "HAI 1.3\nVISIBLE SUM OF 1 AN 2\nVISIBLE DIFF OF 5 AN 2\nVISIBLE QUOSHUNT OF 6 AN 2\nKTHXBYE\n")
  (check-not-exn
   (lambda () (parse-program corrected-operators)))

  (define as-cast-typo
    "HAI 1.3\nVISIBLE MAEK 2 AS NUMBR\nKTHXBYE\n")
  (define as-cast-typo-msg
    (capture-message (lambda () (parse-program as-cast-typo))))
  (check-true (string? as-cast-typo-msg))
  (check-true (regexp-match? #px"invalid cast target type: AS"
                             as-cast-typo-msg))

  (define as-as-identifier
    "HAI 1.3\nI HAS A AS ITZ 2\nVISIBLE AS\nKTHXBYE\n")
  (check-not-exn
   (lambda () (parse-program as-as-identifier)))

  (define mkay-as-identifier
    "HAI 1.3\nI HAS A MKAY ITZ 1\nKTHXBYE\n")
  (check-exn #px"syntax error:"
             (lambda () (parse-program mkay-as-identifier)))

  (define declaration-article-optional
    "HAI 1.3\nI HAS x ITZ 1\nVISIBLE x\nKTHXBYE\n")
  (check-not-exn
   (lambda () (parse-program declaration-article-optional)))

  (define maek-article-optional
    "HAI 1.3\nVISIBLE MAEK 2 NUMBAR\nKTHXBYE\n")
  (check-not-exn
   (lambda () (parse-program maek-article-optional)))

  (define maek-invalid-cast-target-bukkit
    "HAI 1.3\nVISIBLE MAEK 1 A BUKKIT\nKTHXBYE\n")
  (check-exn #px"invalid cast target type:"
             (lambda () (parse-program maek-invalid-cast-target-bukkit)))

  (define maek-invalid-cast-target-unknown
    "HAI 1.3\nVISIBLE MAEK 1 A FOO\nKTHXBYE\n")
  (check-exn #px"invalid cast target type:"
             (lambda () (parse-program maek-invalid-cast-target-unknown)))

  (define maek-lowercase-cast-target
    "HAI 1.3\nVISIBLE MAEK 1 A numbr\nKTHXBYE\n")
  (check-exn #px"invalid cast target type:"
             (lambda () (parse-program maek-lowercase-cast-target)))

  (define cast-assignment-missing-a
    "HAI 1.3\nI HAS A x ITZ 1\nx IS NOW NUMBR\nKTHXBYE\n")
  (check-exn #px"syntax error:"
             (lambda () (parse-program cast-assignment-missing-a)))

  (define cast-assignment-invalid-cast-target-bukkit
    "HAI 1.3\nI HAS A x ITZ 1\nx IS NOW A BUKKIT\nKTHXBYE\n")
  (check-exn #px"invalid cast target type:"
             (lambda () (parse-program cast-assignment-invalid-cast-target-bukkit)))

  (define cast-assignment-lowercase-cast-target
    "HAI 1.3\nI HAS A x ITZ 1\nx IS NOW A numbar\nKTHXBYE\n")
  (check-exn #px"invalid cast target type:"
             (lambda () (parse-program cast-assignment-lowercase-cast-target)))

  (define assignment-nonvariable-lhs
    "HAI 1.3\nSUM OF 1 AN 2 R 3\nKTHXBYE\n")
  (check-exn #px"syntax error:"
             (lambda () (parse-program assignment-nonvariable-lhs)))

  (define assignment-call-lhs
    "HAI 1.3\nHOW IZ I f\n  FOUND YR 1\nIF U SAY SO\nI IZ f MKAY R 3\nKTHXBYE\n")
  (check-exn #px"syntax error:"
             (lambda () (parse-program assignment-call-lhs)))

  (define cast-assignment-nonvariable-lhs
    "HAI 1.3\nSUM OF 1 AN 2 IS NOW A NUMBR\nKTHXBYE\n")
  (check-exn #px"syntax error:"
             (lambda () (parse-program cast-assignment-nonvariable-lhs)))

  (define assignment-canonical-variable-lhs
    "HAI 1.3\nI HAS A x ITZ 1\nx R SUM OF x AN 1\nKTHXBYE\n")
  (check-not-exn
   (lambda () (parse-program assignment-canonical-variable-lhs)))

  (define assignment-canonical-slot-lhs
    "HAI 1.3\nI HAS A obj ITZ A BUKKIT\nobj HAS A n ITZ 0\nobj'Z n R SUM OF obj'Z n AN 1\nKTHXBYE\n")
  (check-not-exn
   (lambda () (parse-program assignment-canonical-slot-lhs)))

  (define clone-missing-a
    "HAI 1.3\nI HAS A parent ITZ A BUKKIT\nI HAS A child ITZ LIEK parent\nKTHXBYE\n")
  (check-exn #px"syntax error:"
             (lambda () (parse-program clone-missing-a)))

  (define all-of-missing-mkay
    "HAI 1.3\nVISIBLE ALL OF WIN AN FAIL\nKTHXBYE\n")
  (check-not-exn
   (lambda () (parse-program all-of-missing-mkay)))

  (define any-of-missing-mkay
    "HAI 1.3\nVISIBLE ANY OF WIN AN FAIL\nKTHXBYE\n")
  (check-not-exn
   (lambda () (parse-program any-of-missing-mkay)))

  (define slot-set-without-article
    "HAI 1.3\nI HAS A obj ITZ A BUKKIT\nobj HAS foo ITZ 1\nKTHXBYE\n")
  (check-exn #px"syntax error:"
             (lambda () (parse-program slot-set-without-article)))

  (define slot-set-with-an-article
    "HAI 1.3\nI HAS A obj ITZ A BUKKIT\nobj HAS AN foo ITZ 1\nKTHXBYE\n")
  (check-exn #px"syntax error:"
             (lambda () (parse-program slot-set-with-an-article)))

  (define slot-set-direct-numeric-target
    "HAI 1.3\nI HAS A obj ITZ A BUKKIT\nobj HAS A 0 ITZ 1\nKTHXBYE\n")
  (check-exn #px"syntax error:"
             (lambda () (parse-program slot-set-direct-numeric-target)))

  (define slot-access-dash-operator
    "HAI 1.3\nI HAS A obj ITZ A BUKKIT\nVISIBLE obj - foo\nKTHXBYE\n")
  ;; N06: accept both '-' and "'Z" spellings for slot access.
  (check-not-exn
   (lambda () (parse-program slot-access-dash-operator)))

  (define misspelled-diffrence-operator
    "HAI 1.3\nVISIBLE DIFFRENCE OF 3 AN 1\nKTHXBYE\n")
  (check-exn #px"syntax error: unexpected OF"
             (lambda () (parse-program misspelled-diffrence-operator)))

  (define misspelled-diffrence-in-srs-index
    "HAI 1.3\nI HAS A xs ITZ A BUKKIT\nxs HAS A Length ITZ 1\nxs HAS A SRS 0 ITZ 7\nVISIBLE xs'Z SRS DIFFRENCE OF xs'Z Length AN 1\nKTHXBYE\n")
  (check-exn #px"syntax error: unexpected OF"
             (lambda () (parse-program misspelled-diffrence-in-srs-index)))

  (define slash-slash-comment-style
    "HAI 1.3\n// this is not a BTW comment\nKTHXBYE\n")
  (check-exn #px"invalid identifier syntax: \"//\""
             (lambda () (parse-program slash-slash-comment-style)))

  (define unterminated-block-comment
    "HAI 1.3\nOBTW\nVISIBLE \"oops\"\nKTHXBYE\n")
  (check-exn #px"unterminated OBTW block comment"
             (lambda () (parse-program unterminated-block-comment)))

  (define loop-label-mismatch
    "HAI 1.3\nIM IN YR loop\nVISIBLE \"x\"\nIM OUTTA YR notloop\nKTHXBYE\n")
  (check-exn #px"loop label mismatch"
             (lambda () (parse-program loop-label-mismatch)))

  (define loop-label-case-mismatch
    "HAI 1.3\nIM IN YR Loop\nVISIBLE \"x\"\nIM OUTTA YR loop\nKTHXBYE\n")
  (check-exn #px"loop label mismatch"
             (lambda () (parse-program loop-label-case-mismatch)))

  (define reserved-keyword-name
    "HAI 1.3\nI HAS A SUM ITZ 1\nKTHXBYE\n")
  (check-exn #px"syntax error:"
             (lambda () (parse-program reserved-keyword-name)))

  (define reserved-keyword-i-name
    "HAI 1.3\nI HAS A I ITZ 1\nKTHXBYE\n")
  (check-exn #px"syntax error:"
             (lambda () (parse-program reserved-keyword-i-name)))

  (define reserved-keyword-an-name
    "HAI 1.3\nI HAS A AN ITZ 1\nKTHXBYE\n")
  (check-exn #px"syntax error:"
             (lambda () (parse-program reserved-keyword-an-name)))

  (define reserved-keyword-mkay-name
    "HAI 1.3\nI HAS A MKAY ITZ 1\nKTHXBYE\n")
  (check-exn #px"syntax error:"
             (lambda () (parse-program reserved-keyword-mkay-name)))

  (define reserved-keyword-mkay-arg
    "HAI 1.3\nHOW IZ I echo YR x\n  FOUND YR x\nIF U SAY SO\nVISIBLE I IZ echo YR MKAY MKAY\nKTHXBYE\n")
  (check-exn #px"syntax error:"
             (lambda () (parse-program reserved-keyword-mkay-arg)))

  (define malformed-method-call-args-missing-yr
    "HAI 1.3\nO HAI IM box\n  HOW IZ I pair YR x AN YR y\n    FOUND YR x\n  IF U SAY SO\nKTHX\nVISIBLE box IZ pair YR 1 AN 2 MKAY\nKTHXBYE\n")
  ;; Method-call argument lists follow: YR <expr> (AN YR <expr>)*.
  (check-exn #px"syntax error:"
             (lambda () (parse-program malformed-method-call-args-missing-yr)))

  (define nonliteral-wtf-case
    "HAI 1.3\nI HAS A x ITZ 1\nI HAS A y ITZ 1\nx, WTF?\n  OMG y\n    VISIBLE \"bad\"\nOIC\nKTHXBYE\n")
  (define nonliteral-wtf-case-msg
    (capture-message (lambda () (parse-program nonliteral-wtf-case))))
  (check-true (string? nonliteral-wtf-case-msg))
  (check-true (regexp-match? #px"WTF\\? case literal must be NUMBER, STRING, WIN, FAIL, or NOOB"
                             nonliteral-wtf-case-msg))

  (define duplicate-wtf-case-literal
    "HAI 1.3\nI HAS A x ITZ 1\nx, WTF?\n  OMG 1\n    VISIBLE \"A\"\n  OMG 1\n    VISIBLE \"B\"\nOIC\nKTHXBYE\n")
  (check-exn #px"duplicate OMG literal in WTF\\?"
             (lambda () (parse-program duplicate-wtf-case-literal)))

  (define duplicate-wtf-case-literal-numeric-mode
    "HAI 1.3\nI HAS A x ITZ 1\nx, WTF?\n  OMG 1\n    VISIBLE \"A\"\n  OMG 1.0\n    VISIBLE \"B\"\nOIC\nKTHXBYE\n")
  (check-exn #px"duplicate OMG literal in WTF\\?"
             (lambda () (parse-program duplicate-wtf-case-literal-numeric-mode)))

  (define interpolated-wtf-string-case
    "HAI 1.3\nI HAS A n ITZ \"x\"\nn, WTF?\n  OMG \":{n}\"\n    VISIBLE \"bad\"\nOIC\nKTHXBYE\n")
  (check-exn #px"WTF\\? case literal cannot contain YARN interpolation"
             (lambda () (parse-program interpolated-wtf-string-case)))

  (define escaped-interpolation-wtf-string-case
    "HAI 1.3\nI HAS A n ITZ \"x\"\nn, WTF?\n  OMG \"::{n}\"\n    VISIBLE \"ok\"\nOIC\nKTHXBYE\n")
  (check-not-exn
   (lambda () (parse-program escaped-interpolation-wtf-string-case)))

  (define orly-missing-ya-rly
    "HAI 1.3\nWIN\nO RLY?\n  NO WAI\n    VISIBLE \"N\"\nOIC\nKTHXBYE\n")
  (check-exn #px"syntax error:"
             (lambda () (parse-program orly-missing-ya-rly)))

  (define spaced-orly-question
    "HAI 1.3\nWIN\nO RLY ?\n  YA RLY\n    VISIBLE \"Y\"\nOIC\nKTHXBYE\n")
  (check-exn #px"syntax error:"
             (lambda () (parse-program spaced-orly-question)))

  (define spaced-wtf-question
    "HAI 1.3\n1, WTF ?\n  OMG 1\n    VISIBLE \"Y\"\nOIC\nKTHXBYE\n")
  (check-exn #px"syntax error:"
             (lambda () (parse-program spaced-wtf-question)))

  (define orphan-mebbe-without-ya-rly
    "HAI 1.3\nWIN\nO RLY?\n  MEBBE WIN\n    VISIBLE \"x\"\nOIC\nKTHXBYE\n")
  (check-exn #px"syntax error:"
             (lambda () (parse-program orphan-mebbe-without-ya-rly)))

  (define orphan-no-wai-without-orly
    "HAI 1.3\nNO WAI\n  VISIBLE \"N\"\nOIC\nKTHXBYE\n")
  (check-exn #px"syntax error:"
             (lambda () (parse-program orphan-no-wai-without-orly)))

  (define orly-mebbe-after-no-wai
    "HAI 1.3\nFAIL\nO RLY?\n  YA RLY\n    VISIBLE \"Y\"\n  NO WAI\n    VISIBLE \"N\"\n  MEBBE WIN\n    VISIBLE \"M\"\nOIC\nKTHXBYE\n")
  (check-exn #px"syntax error:"
             (lambda () (parse-program orly-mebbe-after-no-wai)))

  (define split-im-outta-phrase
    "HAI 1.3\nIM IN YR lp\n  GTFO\nIM\nOUTTA YR lp\nKTHXBYE\n")
  (check-exn #px"syntax error:"
             (lambda () (parse-program split-im-outta-phrase)))

  (define nested-function-def
    "HAI 1.3\nHOW IZ I outer\n  HOW IZ I inner\n    FOUND YR 1\n  IF U SAY SO\n  FOUND YR I IZ inner MKAY\nIF U SAY SO\nKTHXBYE\n")
  (check-exn #px"nested HOW IZ I definitions are not allowed in strict 1.3"
             (lambda () (parse-program nested-function-def)))

  (define nested-function-def-in-method
    "HAI 1.3\nO HAI IM obj\n  HOW IZ I outer\n    HOW IZ I inner\n      FOUND YR 1\n    IF U SAY SO\n    FOUND YR I IZ inner MKAY\n  IF U SAY SO\nKTHX\nKTHXBYE\n")
  (check-exn #px"nested HOW IZ I definitions are not allowed in strict 1.3"
             (lambda () (parse-program nested-function-def-in-method)))

  (define function-dynamic-arg-name
    "HAI 1.3\nI HAS A n ITZ \"x\"\nHOW IZ I f YR SRS n\n  FOUND YR x\nIF U SAY SO\nKTHXBYE\n")
  (check-exn #px"syntax error:"
             (lambda () (parse-program function-dynamic-arg-name)))

  (define method-dynamic-arg-name
    "HAI 1.3\nO HAI IM box\n  I HAS A n ITZ \"x\"\n  HOW IZ I f YR SRS n\n    FOUND YR x\n  IF U SAY SO\nKTHX\nKTHXBYE\n")
  (check-exn #px"syntax error:"
             (lambda () (parse-program method-dynamic-arg-name))))
