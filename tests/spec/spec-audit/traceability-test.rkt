#lang racket/base

(require rackunit
         json
         racket/file
         racket/list
         racket/path
         racket/string
         "../../../scripts/check_spec_traceability.rkt"
         "../../../scripts/adjudication_index_lib.rkt")

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
                                "277\tnormative\tThe `AN` keyword can optionally be used"))

  (define readme-path
    (build-path here ".." ".." ".." "README.md"))
  (check-true (file-exists? readme-path))
  (define readme-text
    (file->string readme-path))
  (check-true (string-contains? readme-text
                                "Most advanced strict HAI 1.3 implementation we know of (we believe), by adjudication depth and traceability completeness."))
  (check-true (string-contains? readme-text
                                "This is a strict-spec, evidence-scoped claim, not a canonical head-to-head benchmark claim."))
  (check-true (string-contains? readme-text
                                "Adjudicated policy choices and implementation-dependent defaults are documented in spec/traceability/."))

  (define defaults-doc-path
    (build-path here ".." ".." ".." "spec" "traceability" "IMPLEMENTATION_DEPENDENT_DEFAULTS.md"))
  (check-true (file-exists? defaults-doc-path))
  (define defaults-doc-text
    (file->string defaults-doc-path))
  (for ([adjudication-id (in-list (list "N20" "N40" "N73" "N75" "N81" "N82"))])
    (check-true (string-contains? defaults-doc-text adjudication-id)))

  ;; Release-blocking runtime boundary regressions must remain in the always-run
  ;; core suite because they pin the IT/object/omgwtf exegesis decisions.
  (define runtime-core-path
    (build-path here ".." "runtime-core-test.rkt"))
  (check-true (file-exists? runtime-core-path))
  (define runtime-core-text
    (file->string runtime-core-path))
  (for ([name (in-list (list "method-fallthrough-it-vs-slot-it"
                             "method-explicit-me-slot-it"
                             "object-body-it-slot-construction"
                             "method-call-noncallable-after-omgwtf-synthesis"
                             "function-identifier-value-binding"
                             "object-body-redeclare-overwrite-does-not-mutate-outer"))])
    (check-true (string-contains? runtime-core-text name)))

  (define holdings-index-path
    (build-path here ".." "HOLDINGS_1_3_TEST_INDEX.md"))
  (check-true (file-exists? holdings-index-path))
  (define holdings-index-text
    (file->string holdings-index-path))
  (for ([holding-id (in-list (list "H01" "H02" "H03" "H04"
                                   "H05" "H06" "H07" "H08"
                                   "H09" "H10" "H11" "H12"
                                   "H13" "H14" "H15" "H16"))])
    (check-true (string-contains? holdings-index-text holding-id)))
  (for ([name (in-list (list "function-identifier-value-binding"
                             "object-body-redeclare-overwrite-does-not-mutate-outer"
                             "method-call-noncallable-after-omgwtf-synthesis"))])
    (check-true (string-contains? holdings-index-text name)))

  (define parse-negative-path
    (build-path here ".." "parse-negative-test.rkt"))
  (check-true (file-exists? parse-negative-path))
  (define parse-negative-text
    (file->string parse-negative-path))
  (for ([name (in-list (list "mixin-declare"
                             "invalid-plain-a-parent-declare"))])
    (check-true (string-contains? parse-negative-text name))
    (check-true (string-contains? holdings-index-text name)))

  (define adjudication-index-path
    (build-path here ".." ".." ".." "spec" "traceability" "adjudication-index.rktd"))
  (check-true (file-exists? adjudication-index-path))
  (define adjudication-index
    (validate-adjudication-index
     (load-adjudication-index adjudication-index-path)))
  (define regenerated-adjudication-index
    (validate-adjudication-index
     (build-adjudication-index)))
  (check-equal? adjudication-index regenerated-adjudication-index)
  (check-true (> (length adjudication-index) 90))

  (define ids
    (sort (map (lambda (h) (hash-ref h 'id)) adjudication-index) string<?))
  (check-not-false (member "N01" ids))
  (check-not-false (member "N99" ids))

  (define traceability-graph-path
    (build-path here ".." ".." ".." "spec" "traceability" "traceability-graph.json"))
  (check-true (file-exists? traceability-graph-path))
  (define traceability-graph
    (call-with-input-file traceability-graph-path read-json))
  (check-equal? (hash-ref traceability-graph 'schema_version) 1)
  (define graph-counts (hash-ref traceability-graph 'counts))
  (check-true (>= (hash-ref graph-counts 'adjudications) 90))
  (check-true (>= (hash-ref graph-counts 'clauses) 70))
  (check-true (> (hash-ref graph-counts 'edges) 0)))
