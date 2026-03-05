#lang racket/base

(require racket/cmdline
         racket/file
         racket/format
         racket/list
         racket/path
         racket/port
         racket/string)

(provide load-traceability
         validate-traceability
         summarize-statuses)

(define required-keys
  '(id
    spec-version
    source-file
    source-line
    clause
    status
    code-refs
    test-refs
    notes))

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

(define (entry-error idx fmt . args)
  (format "entry ~a: ~a" idx (apply format fmt args)))

(define (all-strings? xs)
  (and (list? xs)
       (andmap string? xs)))

(define (validate-entry idx entry root)
  (define errs '())
  (define (add! fmt . args)
    (set! errs (cons (apply entry-error idx fmt args) errs)))
  (unless (hash? entry)
    (add! "expected hash entry, got ~e" entry))
  (when (hash? entry)
    (for ([k (in-list required-keys)])
      (unless (hash-has-key? entry k)
        (add! "missing key ~a" k)))
    (when (hash-has-key? entry 'id)
      (define v (hash-ref entry 'id))
      (unless (and (string? v) (positive? (string-length v)))
        (add! "id must be non-empty string, got ~e" v)))
    (when (hash-has-key? entry 'spec-version)
      (define v (hash-ref entry 'spec-version))
      (unless (and (string? v) (positive? (string-length v)))
        (add! "spec-version must be non-empty string, got ~e" v)))
    (when (hash-has-key? entry 'source-file)
      (define v (hash-ref entry 'source-file))
      (unless (string? v)
        (add! "source-file must be string, got ~e" v))
      (when (string? v)
        (define p (path-under-root root v))
        (unless (file-exists? p)
          (add! "source-file does not exist: ~a" v))))
    (when (hash-has-key? entry 'source-line)
      (define v (hash-ref entry 'source-line))
      (unless (exact-positive-integer? v)
        (add! "source-line must be positive integer, got ~e" v)))
    (when (hash-has-key? entry 'clause)
      (define v (hash-ref entry 'clause))
      (unless (and (string? v) (positive? (string-length v)))
        (add! "clause must be non-empty string, got ~e" v)))
    (when (hash-has-key? entry 'status)
      (define v (hash-ref entry 'status))
      (unless (memq v allowed-statuses)
        (add! "status must be one of ~a, got ~e" allowed-statuses v)))
    (for ([field (in-list '(code-refs test-refs))])
      (when (hash-has-key? entry field)
        (define refs (hash-ref entry field))
        (unless (all-strings? refs)
          (add! "~a must be list of strings, got ~e" field refs))
        (when (all-strings? refs)
          (for ([ref (in-list refs)])
            (define p (path-under-root root ref))
            (unless (file-exists? p)
              (add! "~a references missing path: ~a" field ref))))))
    (when (hash-has-key? entry 'notes)
      (define v (hash-ref entry 'notes))
      (unless (string? v)
        (add! "notes must be string, got ~e" v))))
  (reverse errs))

(define (assert-unique-ids entries)
  (define seen (make-hash))
  (define dupes '())
  (for ([entry (in-list entries)])
    (define id (hash-ref entry 'id #f))
    (when (string? id)
      (if (hash-has-key? seen id)
          (set! dupes (cons id dupes))
          (hash-set! seen id #t))))
  (unless (null? dupes)
    (error 'check_spec_traceability
           "duplicate ids in matrix: ~a"
           (string-join (sort (remove-duplicates dupes) string<?) ", "))))

(define (validate-traceability entries)
  (define root (find-repo-root))
  (define errs
    (append*
     (for/list ([entry (in-list entries)]
                [idx (in-naturals 1)])
       (validate-entry idx entry root))))
  (unless (null? errs)
    (error 'check_spec_traceability
           (string-append
            "traceability validation failed:\n"
            (string-join errs "\n"))))
  (assert-unique-ids entries)
  entries)

(define (summarize-statuses entries)
  (define counts (make-hash))
  (for ([entry (in-list entries)])
    (define st (hash-ref entry 'status))
    (hash-set! counts st (+ 1 (hash-ref counts st 0))))
  counts)

(module+ main
  (define strict? #f)
  (define matrix-path #f)
  (command-line
   #:program "check_spec_traceability.rkt"
   #:once-each
   [("--strict")
    "Fail if any entry is partial/known-divergence/deferred."
    (set! strict? #t)]
   [("--matrix") path
    "Path to a matrix .rktd file."
    (set! matrix-path path)])
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
