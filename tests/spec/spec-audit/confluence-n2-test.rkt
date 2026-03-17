#lang racket/base

(require rackunit
         racket/string
         "../../../src/lolcode/main.rkt"
         "../../../src/lolcode/internal/reporting.rkt")

(struct context (id wrap) #:transparent)

(define (indent n text)
  (define prefix (make-string n #\space))
  (string-join
   (for/list ([line (in-list (string-split text "\n" #:trim? #f))])
     (if (string=? line "")
         line
         (string-append prefix line)))
   "\n"))

(define (ensure-trailing-newline text)
  (if (string-suffix? text "\n")
      text
      (string-append text "\n")))

(define contexts
  (list
   (context 'plain
            (lambda (body _tag)
              body))
   (context 'if-true
            (lambda (body _tag)
              (string-append
               "WIN, O RLY?\n"
               "YA RLY\n"
               (indent 2 body) "\n"
               "NO WAI\n"
               "  BTW no-op\n"
               "OIC\n")))
   (context 'if-mebbe
            (lambda (body _tag)
              (string-append
               "FAIL, O RLY?\n"
               "YA RLY\n"
               "  BTW no-op\n"
               "MEBBE WIN\n"
               (indent 2 body) "\n"
               "NO WAI\n"
               "  BTW no-op\n"
               "OIC\n")))
   (context 'loop-break
            (lambda (body tag)
              (string-append
               "IM IN YR lp" tag "\n"
               (indent 2 body) "\n"
               "  GTFO\n"
               "IM OUTTA YR lp" tag "\n")))
   (context 'loop-til
            (lambda (body tag)
              (string-append
               "I HAS A i" tag " ITZ 0\n"
               "IM IN YR lp" tag " UPPIN YR i" tag " TIL BOTH SAEM i" tag " AN 1\n"
               (indent 2 body) "\n"
               "IM OUTTA YR lp" tag "\n")))
   (context 'loop-wile
            (lambda (body tag)
              (string-append
               "I HAS A i" tag " ITZ 0\n"
               "IM IN YR lp" tag " UPPIN YR i" tag " WILE DIFFRINT i" tag " AN 1\n"
               (indent 2 body) "\n"
               "IM OUTTA YR lp" tag "\n")))
   (context 'switch-hit
            (lambda (body _tag)
              (string-append
               "1, WTF?\n"
               "  OMG 1\n"
               (indent 4 body) "\n"
               "    GTFO\n"
               "  OMGWTF\n"
               "    BTW no-op\n"
               "OIC\n")))
   (context 'switch-default
            (lambda (body _tag)
              (string-append
               "2, WTF?\n"
               "  OMG 1\n"
               "    BTW no-op\n"
               "    GTFO\n"
               "  OMGWTF\n"
               (indent 4 body) "\n"
               "OIC\n")))
   (context 'cast-prelude
            (lambda (body tag)
              (string-append
               "I HAS A num" tag " ITZ \"41\"\n"
               "num" tag " IS NOW A NUMBR\n"
               "num" tag " R SUM OF num" tag " AN 1\n"
               body)))
   (context 'slot-prelude
            (lambda (body tag)
              (string-append
               "I HAS A obj" tag " ITZ A BUKKIT\n"
               "obj" tag " HAS A v ITZ 1\n"
               "obj" tag "'Z v R SUM OF obj" tag "'Z v AN 1\n"
               body)))
   (context 'srs-loop-label
            (lambda (body tag)
              (string-append
               "I HAS A lname" tag " ITZ \"lp" tag "\"\n"
               "IM IN YR SRS lname" tag "\n"
               (indent 2 body) "\n"
               "  GTFO\n"
               "IM OUTTA YR SRS lname" tag "\n")))
   (context 'srs-slot-prelude
            (lambda (body tag)
              (string-append
               "I HAS A obj" tag " ITZ A BUKKIT\n"
               "I HAS A key" tag " ITZ \"v\"\n"
               "obj" tag " HAS A SRS key" tag " ITZ 1\n"
               "obj" tag "'Z SRS key" tag " R SUM OF obj" tag "'Z SRS key" tag " AN 1\n"
               body)))))

(module+ test
  ;; Exhaustive ordered pair coverage over this confluence context basis.
  ;; n = 12 contexts => n^2 = 144 generated confluence tests.
  (for* ([oi (in-range (length contexts))]
         [ii (in-range (length contexts))])
    (define outer (list-ref contexts oi))
    (define inner (list-ref contexts ii))
    (define outer-id (symbol->string (context-id outer)))
    (define inner-id (symbol->string (context-id inner)))
    (define outer-tag (format "o~a" oi))
    (define inner-tag (format "i~a" ii))
    (define body0 "VISIBLE \"OK\"\n")
    (define body1 ((context-wrap inner) body0 inner-tag))
    (define body2 ((context-wrap outer) (ensure-trailing-newline body1) outer-tag))
    (define src
      (string-append "HAI 1.3\n"
                     (ensure-trailing-newline body2)
                     "KTHXBYE\n"))
    (test-case
     (format "n2 confluence ~a x ~a" outer-id inner-id)
     (define out (run-source/report src))
     (check-eq? (hash-ref out 'status) 'ok)
     (check-equal? (hash-ref out 'stdout) "OK\n"))))
