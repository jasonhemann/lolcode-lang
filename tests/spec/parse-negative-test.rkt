#lang racket/base

(require rackunit
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
  (check-true (regexp-match? #px"hint: input ended early" missing-kthxbye-msg))

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
                             nonliteral-wtf-case-msg)))
