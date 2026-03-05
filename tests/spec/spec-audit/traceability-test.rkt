#lang racket/base

(require rackunit
         racket/file
         racket/path
         racket/string
         "../../../scripts/check_spec_traceability.rkt")

(module+ test
  (define entries
    (validate-traceability
     (load-traceability)))

  (check-true (list? entries))
  (check-true (>= (length entries) 20))

  (define counts
    (summarize-statuses entries))
  (check-true (> (hash-ref counts 'implemented 0) 0))
  (check-true (>= (hash-ref counts 'known-divergence 0) 0))
  (define unresolved
    (+ (hash-ref counts 'partial 0)
       (hash-ref counts 'known-divergence 0)
       (hash-ref counts 'deferred 0)))
  ;; Either we still have unresolved items, or the matrix is fully implemented.
  (check-true (or (> unresolved 0)
                  (= (hash-ref counts 'implemented 0)
                     (length entries))))

  (define here
    (or (current-load-relative-directory)
        (current-directory)))
  (define clause-index-path
    (build-path here ".." ".." ".." "spec" "traceability" "spec-1.3-clause-index.tsv"))
  (check-true (file-exists? clause-index-path))
  (define clause-index-text
    (file->string clause-index-path))
  (check-true (string-contains? clause-index-text
                                "277\tnormative\tThe `AN` keyword can optionally be used")))
