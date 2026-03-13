#lang racket/base

(require json
         racket/file
         racket/format
         racket/list
         racket/path)

(provide hash-inc
         counts->rows
         write-json-report)

(define (hash-inc h k [n 1])
  (hash-set h k (+ n (hash-ref h k 0))))

(define (counts->rows h)
  (sort
   (for/list ([(k v) (in-hash h)])
     (hash 'label (~a k) 'count v))
   (lambda (a b)
     (define ca (hash-ref a 'count))
     (define cb (hash-ref b 'count))
     (if (= ca cb)
         (string<? (hash-ref a 'label) (hash-ref b 'label))
         (> ca cb)))))

(define (write-json-report path report)
  (make-directory* (or (path-only path) (current-directory)))
  (call-with-output-file path
    (lambda (out) (write-json report out))
    #:exists 'truncate/replace))
