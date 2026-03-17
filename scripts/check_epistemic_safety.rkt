#lang racket/base

(require json
         racket/file
         racket/format
         racket/list
         racket/path
         racket/string
         "adjudication_index_lib.rkt"
         "check_spec_traceability.rkt"
         "validation_rules_lib.rkt")

(provide build-epistemic-safety-report
         assert-epistemic-safety)

(define default-graph-path
  (build-path (find-repo-root) "spec" "traceability" "traceability-graph.json"))

(define default-defaults-doc-path
  (build-path (find-repo-root) "spec" "traceability" "IMPLEMENTATION_DEPENDENT_DEFAULTS.md"))

(define allowed-edge-types
  '("adjudication_to_clause_inferred_by_code_ref"
    "adjudication_to_code"
    "adjudication_to_test_anchor"
    "clause_to_code"
    "clause_to_test_file"
    "test_anchor_to_test_file"))

(define (id<? a b)
  (< (string->number (substring a 1))
     (string->number (substring b 1))))

(define (as-list v)
  (if (list? v) v '()))

(define (sorted-ids xs)
  (sort xs id<?))

(define (sorted-strings xs)
  (sort xs string<?))

(define (duplicates xs)
  (define counts
    (for/fold ([h (hash)])
              ([x (in-list xs)])
      (hash-update h x add1 0)))
  (sort
   (for/list ([(x count) (in-hash counts)]
              #:when (> count 1))
     x)
   string<?))

(define (json-hash path)
  (unless (file-exists? path)
    (error 'check_epistemic_safety "missing JSON file: ~a" path))
  (define v
    (call-with-input-file path read-json))
  (unless (hash? v)
    (error 'check_epistemic_safety "expected JSON object, got ~e" v))
  v)

(define (build-epistemic-safety-report [index-path default-adjudication-index-path]
                                       [matrix-path #f]
                                       [graph-path default-graph-path]
                                       [defaults-doc-path default-defaults-doc-path])
  (define (failure label data)
    (hasheq 'label label 'data data))
  (define (warning label data)
    (hasheq 'label label 'data data))

  (define index
    (validate-adjudication-index
     (load-adjudication-index index-path)))
  (define clauses
    (validate-traceability
     (load-traceability matrix-path)))
  (define graph
    (json-hash graph-path))
  (void defaults-doc-path)

  (define graph-adjudications
    (as-list (hash-ref graph 'adjudications '())))
  (define graph-clauses
    (as-list (hash-ref graph 'clauses '())))
  (define graph-anchors
    (as-list (hash-ref graph 'test_anchors '())))
  (define graph-edges
    (as-list (hash-ref graph 'edges '())))
  (define graph-counts
    (if (hash? (hash-ref graph 'counts #f))
        (hash-ref graph 'counts)
        #hasheq()))

  (define expected-anchor-count
    (for/sum ([entry (in-list index)])
      (length (hash-ref entry 'test-anchors))))

  (define expected-counts
    (hasheq 'adjudications (length index)
            'clauses (length clauses)
            'test_anchors expected-anchor-count))

  (define count-mismatch-failures
    (for/list ([(k v) (in-hash expected-counts)]
               #:unless (equal? (hash-ref graph-counts k #f) v))
      (failure "count-mismatch"
               (hasheq 'field k
                       'expected v
                       'actual (hash-ref graph-counts k #f)))))

  (define index-ids
    (sorted-ids
     (for/list ([entry (in-list index)])
       (hash-ref entry 'id))))
  (define graph-adj-ids
    (sorted-ids
     (for/list ([entry (in-list graph-adjudications)]
                #:when (hash-has-key? entry 'id))
       (hash-ref entry 'id))))
  (define adjudication-id-mismatch-failures
    (if (equal? index-ids graph-adj-ids)
        '()
        (list
         (failure "adjudication-id-set-mismatch"
                  (hasheq 'index index-ids
                          'graph graph-adj-ids)))))

  (define matrix-ids
    (sorted-strings
     (for/list ([entry (in-list clauses)])
       (hash-ref entry 'id))))
  (define graph-clause-ids
    (sorted-strings
     (for/list ([entry (in-list graph-clauses)]
                #:when (hash-has-key? entry 'id))
       (hash-ref entry 'id))))
  (define clause-id-mismatch-failures
    (if (equal? matrix-ids graph-clause-ids)
        '()
        (list
         (failure "clause-id-set-mismatch"
                  (hasheq 'matrix matrix-ids
                          'graph graph-clause-ids)))))

  (define bad-edge-types
    (remove-duplicates
     (for/list ([edge (in-list graph-edges)]
                #:when (not (member (hash-ref edge 'type #f) allowed-edge-types)))
       (hash-ref edge 'type #f))
     equal?))
  (define bad-edge-type-failures
    (if (null? bad-edge-types)
        '()
        (list (failure "unknown-edge-types" bad-edge-types))))

  (define duplicated-index-ids
    (duplicates index-ids))
  (define duplicate-index-id-failures
    (if (null? duplicated-index-ids)
        '()
        (list (failure "duplicate-index-ids" duplicated-index-ids))))

  (define entries-with-duplicate-test-anchors
    (for/list ([entry (in-list index)]
               #:when (pair? (duplicates (hash-ref entry 'test-anchors))))
      (define dupes
        (duplicates (hash-ref entry 'test-anchors)))
      (hasheq 'id (hash-ref entry 'id)
              'duplicate-anchors (sorted-strings dupes))))
  (define duplicate-anchor-warnings
    (if (null? entries-with-duplicate-test-anchors)
        '()
        (list
         (warning "entries-with-duplicate-test-anchors"
                  entries-with-duplicate-test-anchors))))

  (define no-test-anchor-ids
    (for/list ([entry (in-list index)]
               #:when (null? (hash-ref entry 'test-anchors)))
      (hash-ref entry 'id)))
  (define no-anchor-warnings
    (if (null? no-test-anchor-ids)
        '()
        (list
         (warning "adjudications-without-test-anchors"
                  (sorted-ids no-test-anchor-ids)))))

  (define unresolved-anchor-names
    (for/list ([a (in-list graph-anchors)]
               #:when (null? (as-list (hash-ref a 'test_files '()))))
      (hash-ref a 'name)))
  (define unresolved-anchor-warnings
    (if (null? unresolved-anchor-names)
        '()
        (list
         (warning "anchors-without-test-files"
                  (sorted-strings unresolved-anchor-names)))))

  (define failures
    (append count-mismatch-failures
            adjudication-id-mismatch-failures
            clause-id-mismatch-failures
            bad-edge-type-failures
            duplicate-index-id-failures))
  (define warnings
    (append duplicate-anchor-warnings
            no-anchor-warnings
            unresolved-anchor-warnings))

  (hasheq 'ok? (null? failures)
          'hard-failure-count (length failures)
          'warning-count (length warnings)
          'hard-failures failures
          'warnings warnings
          'counts
          (hasheq 'index-adjudications (length index)
                  'matrix-clauses (length clauses)
                  'graph-adjudications (length graph-adjudications)
                  'graph-clauses (length graph-clauses)
                  'graph-anchors (length graph-anchors)
                  'graph-edges (length graph-edges))))

(define (assert-epistemic-safety report)
  (unless (hash-ref report 'ok?)
    (error 'check_epistemic_safety
           (string-append
            "epistemic safety hard failures:\n"
            (string-join
             (for/list ([f (in-list (hash-ref report 'hard-failures))])
               (format "- ~a: ~e"
                       (hash-ref f 'label)
                       (hash-ref f 'data)))
             "\n"))))
  report)

(module+ main
  (define option-specs
    (list (hasheq 'flag "--index" 'key 'index-path 'mode 'value 'convert string->path)
          (hasheq 'flag "--matrix" 'key 'matrix-path 'mode 'value 'convert string->path)
          (hasheq 'flag "--graph" 'key 'graph-path 'mode 'value 'convert string->path)
          (hasheq 'flag "--defaults-doc" 'key 'defaults-doc-path 'mode 'value 'convert string->path)
          (hasheq 'flag "--json-out" 'key 'json-out 'mode 'value 'convert string->path)))
  (define option-defaults
    (hasheq 'index-path default-adjudication-index-path
            'matrix-path #f
            'graph-path default-graph-path
            'defaults-doc-path default-defaults-doc-path
            'json-out #f))
  (define opts
    (parse-cli-options 'check_epistemic_safety
                       (vector->list (current-command-line-arguments))
                       option-specs
                       option-defaults))
  (define index-path (hash-ref opts 'index-path))
  (define matrix-path (hash-ref opts 'matrix-path))
  (define graph-path (hash-ref opts 'graph-path))
  (define defaults-doc-path (hash-ref opts 'defaults-doc-path))
  (define json-out (hash-ref opts 'json-out))
  (define report
    (build-epistemic-safety-report index-path
                                   matrix-path
                                   graph-path
                                   defaults-doc-path))
  (when json-out
    (make-directory* (path-only json-out))
    (call-with-output-file json-out
      (lambda (out) (write-json report out))
      #:exists 'truncate/replace))
  (printf "Epistemic safety: hard-failures=~a warnings=~a\n"
          (hash-ref report 'hard-failure-count)
          (hash-ref report 'warning-count))
  (for ([w (in-list (hash-ref report 'warnings))])
    (printf "  warning: ~a (~a)\n"
            (hash-ref w 'label)
            (hash-ref w 'data)))
  (void (assert-epistemic-safety report)))
