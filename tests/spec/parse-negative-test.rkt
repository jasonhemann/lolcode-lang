#lang racket/base

(require rackunit
         "../../src/lolcode/lexer.rkt"
         "../../src/lolcode/main.rkt")

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

  (define unsupported-v14
    "HAI 1.4\nVISIBLE \"future\"\nKTHXBYE\n")
  (define unsupported-v14-msg
    (capture-message (lambda () (parse-program unsupported-v14))))
  (check-true (string? unsupported-v14-msg))
  (check-true (regexp-match? #px"unsupported version: 1\\.4" unsupported-v14-msg))

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

  (define invalid-unicode-normative-name
    "HAI 1.3\nVISIBLE \":[:{var}]\"\nKTHXBYE\n")
  (check-exn #px"invalid Unicode normative name in string literal"
             (lambda () (parse-program invalid-unicode-normative-name)))

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

  (define invalid-ident-leading-underscore
    "HAI 1.3\nI HAS A _x ITZ 1\nKTHXBYE\n")
  (check-exn #px"invalid identifier syntax"
             (lambda () (parse-program invalid-ident-leading-underscore)))

  (define invalid-ident-with-dash
    "HAI 1.3\nI HAS A x-y ITZ 1\nKTHXBYE\n")
  (check-exn #px"invalid identifier syntax"
             (lambda () (parse-program invalid-ident-with-dash)))

  (define invalid-ident-symbol-only
    "HAI 1.3\nI HAS A ++ ITZ 1\nKTHXBYE\n")
  (check-exn #px"invalid identifier syntax"
             (lambda () (parse-program invalid-ident-symbol-only)))

  (define and-as-identifier-when-an-omitted
    "HAI 1.3\nVISIBLE SUM OF 1 AND 2\nKTHXBYE\n")
  (check-exn #px"syntax error: unexpected NUMBER"
             (lambda () (parse-program and-as-identifier-when-an-omitted)))

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
  (check-true (regexp-match? #px"syntax error: unexpected ID \\(\"NUMBR\"\\)"
                             as-cast-typo-msg))

  (define as-as-identifier
    "HAI 1.3\nI HAS A AS ITZ 2\nVISIBLE AS\nKTHXBYE\n")
  (check-not-exn
   (lambda () (parse-program as-as-identifier)))

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

  (define unterminated-block-comment
    "HAI 1.3\nOBTW\nVISIBLE \"oops\"\nKTHXBYE\n")
  (check-exn #px"unterminated OBTW block comment"
             (lambda () (parse-program unterminated-block-comment)))

  (define loop-label-mismatch
    "HAI 1.3\nIM IN YR loop\nVISIBLE \"x\"\nIM OUTTA YR notloop\nKTHXBYE\n")
  (check-exn #px"loop label mismatch"
             (lambda () (parse-program loop-label-mismatch)))

  (define reserved-keyword-name
    "HAI 1.3\nI HAS A SUM ITZ 1\nKTHXBYE\n")
  (define reserved-keyword-name-msg
    (capture-message (lambda () (parse-program reserved-keyword-name))))
  (check-false reserved-keyword-name-msg)

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

  (define interpolated-wtf-string-case
    "HAI 1.3\nI HAS A n ITZ \"x\"\nn, WTF?\n  OMG \":{n}\"\n    VISIBLE \"bad\"\nOIC\nKTHXBYE\n")
  (check-exn #px"WTF\\? case literal cannot contain YARN interpolation"
             (lambda () (parse-program interpolated-wtf-string-case)))

  (define nested-function-def
    "HAI 1.3\nHOW IZ I outer\n  HOW IZ I inner\n    FOUND YR 1\n  IF U SAY SO\n  FOUND YR I IZ inner MKAY\nIF U SAY SO\nKTHXBYE\n")
  (check-exn #px"nested HOW IZ I definitions are not allowed in strict 1.3"
             (lambda () (parse-program nested-function-def))))
