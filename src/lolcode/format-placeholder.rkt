#lang racket/base

(require racket/match)

(provide (struct-out yarn-template)
         (struct-out yarn-part-text)
         (struct-out yarn-part-placeholder)
         make-yarn-template
         ensure-yarn-template
         yarn-template-has-placeholders?
         yarn-template-static-text
         yarn-template-source-length)

(struct yarn-template (parts) #:transparent)
(struct yarn-part-text (text) #:transparent)
(struct yarn-part-placeholder (name) #:transparent)

(define (normalize-yarn-part who part)
  (cond
    [(string? part)
     (yarn-part-text part)]
    [(yarn-part-text? part)
     (unless (string? (yarn-part-text-text part))
       (raise-argument-error who "yarn-part-text with string payload" part))
     part]
    [(yarn-part-placeholder? part)
     (unless (string? (yarn-part-placeholder-name part))
       (raise-argument-error who "yarn-part-placeholder with string payload" part))
     part]
    [else
     (raise-argument-error
      who
      "(or/c string? yarn-part-text? yarn-part-placeholder?)"
      part)]))

(define (make-yarn-template parts)
  (unless (list? parts)
    (raise-argument-error 'make-yarn-template "list?" parts))
  (define normalized-rev
    (for/fold ([out '()])
              ([raw (in-list parts)])
      (define part (normalize-yarn-part 'make-yarn-template raw))
      (match part
        [(yarn-part-text txt)
         (cond
           [(string=? txt "") out]
           [(and (pair? out) (yarn-part-text? (car out)))
            (cons (yarn-part-text
                   (string-append
                    (yarn-part-text-text (car out))
                    txt))
                  (cdr out))]
           [else
            (cons part out)])]
        [_ (cons part out)])))
  (yarn-template (reverse normalized-rev)))

(define (ensure-yarn-template value)
  (cond
    [(yarn-template? value)
     value]
    [(string? value)
     (make-yarn-template (list (yarn-part-text value)))]
    [else
     (raise-argument-error
      'ensure-yarn-template
      "(or/c yarn-template? string?)"
      value)]))

(define (yarn-template-has-placeholders? value)
  (define template
    (ensure-yarn-template value))
  (for/or ([part (in-list (yarn-template-parts template))])
    (yarn-part-placeholder? part)))

(define (yarn-template-static-text value)
  (define template
    (ensure-yarn-template value))
  (apply string-append
         (for/list ([part (in-list (yarn-template-parts template))])
           (match part
             [(yarn-part-text text) text]
             [(yarn-part-placeholder name)
              (error 'yarn-template-static-text
                     "template contains placeholder segment: ~a"
                     name)]))))

(define (yarn-template-source-length value)
  (define template
    (ensure-yarn-template value))
  (for/sum ([part (in-list (yarn-template-parts template))])
    (match part
      [(yarn-part-text text) (string-length text)]
      [(yarn-part-placeholder name)
       (+ 3 (string-length name))])))
