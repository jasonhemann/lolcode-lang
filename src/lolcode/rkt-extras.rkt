#lang racket/base

(require racket/list)

(provide split-until)

;; Dual of `splitf-at`: split at the first element satisfying `stop?`.
(define (split-until xs stop?)
  (splitf-at xs
             (lambda (x)
               (not (stop? x)))))
