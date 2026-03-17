#lang racket/base

(require racket/file
         racket/format
         racket/list
         racket/path
         racket/port
         racket/string
         "validation_rules_lib.rkt")

(provide load-traceability
         validate-traceability
         summarize-statuses)

(define allowed-statuses
  '(implemented partial known-divergence deferred out-of-scope))

(define (find-repo-root [start (current-directory)])
  (define marker (build-path start "AGENTS.md"))
  (cond
    [(file-exists? marker) start]
    [else
     (define parent (simplify-path (build-path start 'up)))
     (if (equal? parent start)
         (error 'check_spec_traceability
                "could not locate repository root from ~a"
                start)
         (find-repo-root parent))]))

(define (path-under-root root p)
  (if (absolute-path? p)
      p
      (build-path root p)))

(define (load-traceability [matrix-path #f])
  (define root (find-repo-root))
  (define path
    (or matrix-path
        (build-path root "spec" "traceability" "spec-1.3-matrix.rktd")))
  (unless (file-exists? path)
    (error 'check_spec_traceability "matrix file missing: ~a" path))
  (define entries
    (call-with-input-file path read))
  (unless (list? entries)
    (error 'check_spec_traceability "matrix must contain a list, got ~e" entries))
  entries)

(define (all-strings? xs)
  (and (list? xs)
       (andmap string? xs)))

(define (non-empty-string? v)
  (and (string? v)
       (positive? (string-length v))))

(define traceability-id-rule
  (make-field-rule 'id
                   #t
                   (list (make-check
                          (lambda (v _ctx) (non-empty-string? v))
                          (lambda (v _ctx) (format "id must be non-empty string, got ~e" v))))))

(define traceability-spec-version-rule
  (make-field-rule 'spec-version
                   #t
                   (list (make-check
                          (lambda (v _ctx) (non-empty-string? v))
                          (lambda (v _ctx) (format "spec-version must be non-empty string, got ~e" v))))))

(define traceability-source-file-rule
  (make-field-rule
   'source-file
   #t
   (list
    (make-check
     (lambda (v _ctx) (string? v))
     (lambda (v _ctx) (format "source-file must be string, got ~e" v)))
    (make-check
     (lambda (v ctx)
       (or (not (string? v))
           (file-exists? (path-under-root (hash-ref ctx 'root) v))))
     (lambda (v _ctx) (format "source-file does not exist: ~a" v))))))

(define traceability-source-line-rule
  (make-field-rule 'source-line
                   #t
                   (list (make-check
                          (lambda (v _ctx) (exact-positive-integer? v))
                          (lambda (v _ctx) (format "source-line must be positive integer, got ~e" v))))))

(define traceability-clause-rule
  (make-field-rule 'clause
                   #t
                   (list (make-check
                          (lambda (v _ctx) (non-empty-string? v))
                          (lambda (v _ctx) (format "clause must be non-empty string, got ~e" v))))))

(define traceability-status-rule
  (make-field-rule
   'status
   #t
   (list (make-check
          (lambda (v _ctx) (memq v allowed-statuses))
          (lambda (v _ctx)
            (format "status must be one of ~a, got ~e" allowed-statuses v))))))

(define traceability-code-refs-rule
  (make-field-rule
   'code-refs
   #t
   (list
    (make-check
     (lambda (v _ctx) (all-strings? v))
     (lambda (v _ctx) (format "code-refs must be list of strings, got ~e" v)))
    (make-check
     (lambda (v ctx)
       (or (not (all-strings? v))
           (null? (missing-relative-paths (hash-ref ctx 'root) v))))
     (lambda (v ctx)
       (format "code-refs references missing path: ~a"
               (string-join (missing-relative-paths (hash-ref ctx 'root) v) ", ")))))))

(define traceability-test-refs-rule
  (make-field-rule
   'test-refs
   #t
   (list
    (make-check
     (lambda (v _ctx) (all-strings? v))
     (lambda (v _ctx) (format "test-refs must be list of strings, got ~e" v)))
    (make-check
     (lambda (v ctx)
       (or (not (all-strings? v))
           (null? (missing-relative-paths (hash-ref ctx 'root) v))))
     (lambda (v ctx)
       (format "test-refs references missing path: ~a"
               (string-join (missing-relative-paths (hash-ref ctx 'root) v) ", ")))))))

(define traceability-notes-rule
  (make-field-rule 'notes
                   #t
                   (list (make-check
                          (lambda (v _ctx) (string? v))
                          (lambda (v _ctx) (format "notes must be string, got ~e" v))))))

(define traceability-entry-rules
  (list traceability-id-rule
        traceability-spec-version-rule
        traceability-source-file-rule
        traceability-source-line-rule
        traceability-clause-rule
        traceability-status-rule
        traceability-code-refs-rule
        traceability-test-refs-rule
        traceability-notes-rule))

(define (collect-traceability-ids entries)
  (for/list ([entry (in-list entries)]
             #:when (and (hash? entry)
                         (hash-has-key? entry 'id)
                         (string? (hash-ref entry 'id))))
    (hash-ref entry 'id)))

(define (assert-unique-ids entries)
  (define dupes-err
    (duplicate-string-id-error (collect-traceability-ids entries)
                               "duplicate ids in matrix"))
  (when dupes-err
    (error 'check_spec_traceability "~a" dupes-err)))

(define (validate-traceability entries)
  (define root (find-repo-root))
  (define errs
    (validate-entry-list entries
                         traceability-entry-rules
                         (lambda (_entry _idx) (hasheq 'root root))))
  (unless (null? errs)
    (error 'check_spec_traceability
           (string-append
            "traceability validation failed:\n"
            (string-join errs "\n"))))
  (assert-unique-ids entries)
  entries)

(define (summarize-statuses entries)
  (for/fold ([counts (hash)])
            ([entry (in-list entries)])
    (define st (hash-ref entry 'status))
    (hash-update counts st add1 0)))

(module+ main
  (define option-specs
    (list (hasheq 'flag "--strict" 'key 'strict? 'mode 'switch 'value #t)
          (hasheq 'flag "--matrix" 'key 'matrix-path 'mode 'value)))
  (define defaults
    (hasheq 'strict? #f
            'matrix-path #f))
  (define opts
    (parse-cli-options 'check_spec_traceability
                       (vector->list (current-command-line-arguments))
                       option-specs
                       defaults))
  (define strict?
    (hash-ref opts 'strict?))
  (define matrix-path
    (hash-ref opts 'matrix-path))
  (define entries
    (validate-traceability (load-traceability matrix-path)))
  (define counts
    (summarize-statuses entries))
  (displayln "Spec traceability summary:")
  (for ([st (in-list allowed-statuses)])
    (displayln
     (~a "  "
         st
         ": "
         (hash-ref counts st 0))))
  (displayln
   (~a "  total: " (length entries)))
  (when strict?
    (define offenders
      (for/list ([entry (in-list entries)]
                 #:when (memq (hash-ref entry 'status)
                              '(partial known-divergence deferred)))
        (hash-ref entry 'id)))
    (unless (null? offenders)
      (error 'check_spec_traceability
             "strict mode failed; unresolved entries: ~a"
             (string-join offenders ", ")))))
