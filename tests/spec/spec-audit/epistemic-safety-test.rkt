#lang racket/base

(require rackunit
         "../../../scripts/check_epistemic_safety.rkt")

(module+ test
  (define report
    (build-epistemic-safety-report))

  ;; Hard-failure invariants are gating.
  (check-true (hash-ref report 'ok?))
  (check-equal? (hash-ref report 'hard-failure-count) 0)

  ;; Warning channel is expected to exist and stay machine-readable.
  (check-true (hash-has-key? report 'warning-count))
  (check-true (hash-has-key? report 'warnings)))
