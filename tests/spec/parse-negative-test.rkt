#lang racket/base

(require rackunit
         "../../src/lolcode/main.rkt")

(module+ test
  (define (capture-message thunk)
    (with-handlers ([exn:fail? exn-message])
      (thunk)
      #f))

  (define missing-kthxbye
    "HAI 1.2\nVISIBLE \"OH HAI\"\n")
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
  (check-true (regexp-match? #px"line 1, col 4" missing-version-msg))

  (define unterminated-string
    "HAI 1.2\nVISIBLE \"oops\nKTHXBYE\n")
  (check-exn #px"unterminated string literal at line 2, col 9"
             (lambda () (parse-program unterminated-string)))

  (define unterminated-format-placeholder
    "HAI 1.2\nVISIBLE \"oops :{name\"\nKTHXBYE\n")
  (check-exn #px"unterminated :\\{\\.\\.\\.\\} placeholder in string literal"
             (lambda () (parse-program unterminated-format-placeholder)))

  (define unterminated-block-comment
    "HAI 1.2\nOBTW\nVISIBLE \"oops\"\nKTHXBYE\n")
  (check-exn #px"unterminated OBTW block comment"
             (lambda () (parse-program unterminated-block-comment)))

  (define loop-label-mismatch
    "HAI 1.2\nIM IN YR loop\nVISIBLE \"x\"\nIM OUTTA YR notloop\nKTHXBYE\n")
  (check-exn #px"loop label mismatch"
             (lambda () (parse-program loop-label-mismatch)))

  (define reserved-keyword-name
    "HAI 1.2\nI HAS A SUM ITZ 1\nKTHXBYE\n")
  (define reserved-keyword-name-msg
    (capture-message (lambda () (parse-program reserved-keyword-name))))
  (check-false reserved-keyword-name-msg))
