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

(define option-specs
  (list (hasheq 'flag "--index" 'key 'index-path 'mode 'value 'convert string->path)
        (hasheq 'flag "--matrix" 'key 'matrix-path 'mode 'value 'convert string->path)
        (hasheq 'flag "--out" 'key 'out-path 'mode 'value 'convert string->path)))

(define option-defaults
  (hasheq 'index-path default-adjudication-index-path
          'matrix-path #f
          'out-path (build-path (find-repo-root) "spec" "traceability" "traceability-graph.json")))

(define opts
  (parse-cli-options 'export_traceability_graph
                     (vector->list (current-command-line-arguments))
                     option-specs
                     option-defaults))

(define index-path (hash-ref opts 'index-path))
(define matrix-path (hash-ref opts 'matrix-path))
(define out-path (hash-ref opts 'out-path))

(define (id<? a b)
  (< (string->number (substring a 1))
     (string->number (substring b 1))))

(define (sorted-unique xs [cmp string<?])
  (remove-duplicates (sort xs cmp) string=?))

(define (path-sort xs)
  (sort xs string<?))

(define root (find-repo-root))

(define adjudications
  (validate-adjudication-index
   (load-adjudication-index index-path)))

(define clauses
  (validate-traceability
   (load-traceability matrix-path)))

(define (code-ref? p)
  (or (string-prefix? p "src/")
      (string-prefix? p "lang/")
      (string-prefix? p "internal/")))

(define test-files-cache
  (sort
   (for/list ([p (in-directory (build-path root "tests"))]
              #:when (and (file-exists? p)
                          (regexp-match? #px"\\.rkt$" (path->string p))))
     (path->string (find-relative-path root p)))
   string<?))

(define (find-anchor-test-files anchor)
  (for/list ([rel (in-list test-files-cache)]
             #:when (let ([txt (file->string (build-path root rel))])
                      (string-contains? txt anchor)))
    rel))

(define adjudication-nodes
  (for/list ([entry (in-list (sort adjudications id<? #:key (lambda (h) (hash-ref h 'id))))])
    (define impl-refs (hash-ref entry 'implementation-refs))
    (define code-refs (filter code-ref? impl-refs))
    (define other-refs (filter (lambda (p) (not (code-ref? p))) impl-refs))
    (hasheq 'id (hash-ref entry 'id)
            'disposition (~a (hash-ref entry 'disposition))
            'code_refs (path-sort code-refs)
            'other_refs (path-sort other-refs)
            'test_anchors (hash-ref entry 'test-anchors)
            'resolution_map_lines (hash-ref entry 'resolution-map-lines)
            'ledger_lines (hash-ref entry 'ledger-lines)
            'notes (hash-ref entry 'notes))))

(define clause-nodes
  (for/list ([entry (in-list clauses)])
    (hasheq 'id (hash-ref entry 'id)
            'source_file (hash-ref entry 'source-file)
            'source_line (hash-ref entry 'source-line)
            'clause (hash-ref entry 'clause)
            'status (~a (hash-ref entry 'status))
            'code_refs (path-sort (hash-ref entry 'code-refs))
            'test_refs (path-sort (hash-ref entry 'test-refs))
            'notes (hash-ref entry 'notes))))

(define anchor-nodes
  (for*/list ([entry (in-list adjudication-nodes)]
              [anchor (in-list (hash-ref entry 'test_anchors))])
    (hasheq 'name anchor
            'adjudication_id (hash-ref entry 'id)
            'test_files (path-sort (find-anchor-test-files anchor)))))

(define adjudication-code-edges
  (for*/list ([a (in-list adjudication-nodes)]
              [code-ref (in-list (hash-ref a 'code_refs))])
    (hasheq 'type "adjudication_to_code"
            'from (hash-ref a 'id)
            'to code-ref
            'origin "adjudication-index")))

(define adjudication-anchor-edges
  (for*/list ([a (in-list adjudication-nodes)]
              [anchor (in-list (hash-ref a 'test_anchors))])
    (hasheq 'type "adjudication_to_test_anchor"
            'from (hash-ref a 'id)
            'to anchor
            'origin "adjudication-index")))

(define clause-code-edges
  (for*/list ([clause (in-list clause-nodes)]
              [code-ref (in-list (hash-ref clause 'code_refs))])
    (hasheq 'type "clause_to_code"
            'from (hash-ref clause 'id)
            'to code-ref
            'origin "spec-1.3-matrix")))

(define clause-test-edges
  (for*/list ([clause (in-list clause-nodes)]
              [test-ref (in-list (hash-ref clause 'test_refs))])
    (hasheq 'type "clause_to_test_file"
            'from (hash-ref clause 'id)
            'to test-ref
            'origin "spec-1.3-matrix")))

(define anchor-test-file-edges
  (for*/list ([anchor (in-list anchor-nodes)]
              [test-file (in-list (hash-ref anchor 'test_files))])
    (hasheq 'type "test_anchor_to_test_file"
            'from (hash-ref anchor 'name)
            'to test-file
            'origin "anchor-scan")))

(define clause-code-set
  (for/hash ([clause (in-list clause-nodes)])
    (values (hash-ref clause 'id)
            (hash-ref clause 'code_refs))))

(define inferred-overlap-edges
  (for*/fold ([acc '()])
             ([adj (in-list adjudication-nodes)]
              [(cid code-refs) (in-hash clause-code-set)])
    (define aid (hash-ref adj 'id))
    (define overlap
      (filter (lambda (x) (member x code-refs))
              (hash-ref adj 'code_refs)))
    (if (pair? overlap)
        (cons (hasheq 'type "adjudication_to_clause_inferred_by_code_ref"
                      'from aid
                      'to cid
                      'origin (string-append "shared-code-ref:"
                                             (string-join (sorted-unique overlap) ",")))
              acc)
        acc)))

(define edges
  (append adjudication-code-edges
          adjudication-anchor-edges
          clause-code-edges
          clause-test-edges
          anchor-test-file-edges
          (reverse inferred-overlap-edges)))

(define all-code-refs
  (sorted-unique
   (append
    (apply append (map (lambda (a) (hash-ref a 'code_refs)) adjudication-nodes))
    (apply append (map (lambda (c) (hash-ref c 'code_refs)) clause-nodes)))))

(define all-test-files
  (sorted-unique
   (append
    (apply append (map (lambda (c) (hash-ref c 'test_refs)) clause-nodes))
    (apply append (map (lambda (a) (hash-ref a 'test_files)) anchor-nodes)))))

(define graph
  (hasheq 'schema_version 1
          'adjudications adjudication-nodes
          'clauses clause-nodes
          'test_anchors (sort anchor-nodes string<? #:key (lambda (h) (hash-ref h 'name)))
          'code_refs all-code-refs
          'test_files all-test-files
          'edges (sort edges
                       (lambda (a b)
                         (cond
                           [(string<? (hash-ref a 'type) (hash-ref b 'type)) #t]
                           [(string>? (hash-ref a 'type) (hash-ref b 'type)) #f]
                           [(string<? (hash-ref a 'from) (hash-ref b 'from)) #t]
                           [(string>? (hash-ref a 'from) (hash-ref b 'from)) #f]
                           [else (string<? (hash-ref a 'to) (hash-ref b 'to))])))
          'counts
          (hasheq 'adjudications (length adjudication-nodes)
                  'clauses (length clause-nodes)
                  'test_anchors (length anchor-nodes)
                  'code_refs (length all-code-refs)
                  'test_files (length all-test-files)
                  'edges (length edges))))

(make-directory* (path-only out-path))
(call-with-output-file out-path
  (lambda (out)
    (write-json graph out))
  #:exists 'truncate/replace)

(printf "wrote traceability graph to ~a\n" (path->string out-path))
