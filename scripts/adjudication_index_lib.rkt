#lang racket/base

(require racket/file
         racket/format
         racket/list
         racket/path
         racket/port
         racket/string
         "validation_rules_lib.rkt")

(provide allowed-dispositions
         default-adjudication-index-path
         default-resolution-map-path
         default-test-anchor-index-path
         default-adjudication-ledger-path
         find-repo-root
         load-adjudication-index
         validate-adjudication-index
         extract-resolution-map-rows
         extract-test-anchor-rows
         extract-ledger-id-lines
         build-adjudication-index)

(define allowed-dispositions
  '(implemented
    policy
    policy+implemented
    provisional-policy
    mooted))

(define (find-repo-root [start (current-directory)])
  (define marker (build-path start "AGENTS.md"))
  (cond
    [(file-exists? marker) start]
    [else
     (define parent (simplify-path (build-path start 'up)))
     (if (equal? parent start)
         (error 'adjudication_index "could not locate repository root from ~a" start)
         (find-repo-root parent))]))

(define (must-read-lines p who)
  (unless (file-exists? p)
    (error who "missing file: ~a" p))
  (file->lines p))

(define default-resolution-map-path
  (build-path (find-repo-root) "spec" "traceability" "RESOLUTION_MAP.md"))

(define default-test-anchor-index-path
  (build-path (find-repo-root) "spec" "traceability" "TEST_ANCHOR_INDEX.md"))

(define default-adjudication-ledger-path
  (build-path (find-repo-root) "spec" "traceability" "ADJUDICATION_LEDGER.md"))

(define default-adjudication-index-path
  (build-path (find-repo-root) "spec" "traceability" "adjudication-index.rktd"))

(define resolution-row-rx
  #px"^\\|\\s*`(N[0-9][0-9])`\\s*\\|\\s*([^|]+?)\\s*\\|\\s*(.*?)\\s*\\|\\s*(.*?)\\s*\\|\\s*$")

(define anchor-row-rx
  #px"^\\|\\s*`(N[0-9][0-9])`\\s*\\|\\s*(.*?)\\s*\\|\\s*\\[ADJUDICATION_LEDGER\\.md:line\\s+([0-9]+)\\].*$")

(define ledger-row-rx
  #px"^\\|\\s*`(N[0-9][0-9])`\\s*\\|\\s*([^|]+?)\\s*\\|\\s*(.*)\\|\\s*$")

(define (extract-backtick-paths txt)
  (remove-duplicates
   (for/list ([m (in-list (regexp-match* #px"`([^`]+)`" txt #:match-select second))]
              #:when (string-contains? m "/"))
     m)
   string=?))

(define (parse-disposition txt)
  (string->symbol (string-trim txt)))

(define (extract-resolution-map-rows lines)
  (for/list ([ln (in-list lines)]
             [line-no (in-naturals 1)]
             #:when (regexp-match? resolution-row-rx ln))
    (define m (regexp-match resolution-row-rx ln))
    (define id (list-ref m 1))
    (define disposition-txt (list-ref m 2))
    (define impl-col (list-ref m 3))
    (hasheq 'id id
            'disposition (parse-disposition disposition-txt)
            'implementation-refs (extract-backtick-paths impl-col)
            'line line-no)))

(define (parse-anchor-list txt)
  (define t (string-trim txt))
  (cond
    [(or (string=? t "")
         (string-prefix? t "(none explicit"))
     '()]
    [else
     (filter (lambda (x) (not (string=? x "")))
             (map string-trim (string-split t ",")))]))

(define (extract-test-anchor-rows lines)
  (for/list ([ln (in-list lines)]
             [line-no (in-naturals 1)]
             #:when (regexp-match? anchor-row-rx ln))
    (define m (regexp-match anchor-row-rx ln))
    (hasheq 'id (list-ref m 1)
            'anchors (parse-anchor-list (list-ref m 2))
            'line line-no
            'ledger-line (string->number (list-ref m 3)))))

(define (extract-ledger-id-lines lines)
  (for/fold ([acc (hash)])
            ([ln (in-list lines)]
             [line-no (in-naturals 1)])
    (if (regexp-match? ledger-row-rx ln)
        (let* ([m (regexp-match ledger-row-rx ln)]
               [id (list-ref m 1)]
               [prev (hash-ref acc id '())])
          (hash-set acc id (append prev (list line-no))))
        acc)))

(define (id<? a b)
  (< (string->number (substring a 1))
     (string->number (substring b 1))))

(define (hash-keys-sorted h)
  (sort (hash-keys h) id<?))

(define (build-adjudication-index [map-path default-resolution-map-path]
                                   [anchor-path default-test-anchor-index-path]
                                   [ledger-path default-adjudication-ledger-path])
  (define map-rows
    (extract-resolution-map-rows (must-read-lines map-path 'build-adjudication-index)))
  (define anchor-rows
    (extract-test-anchor-rows (must-read-lines anchor-path 'build-adjudication-index)))
  (define ledger-lines-by-id
    (extract-ledger-id-lines (must-read-lines ledger-path 'build-adjudication-index)))

  (define map-by-id
    (for/fold ([acc (hash)]) ([row (in-list map-rows)])
      (hash-set acc (hash-ref row 'id) row)))
  (define anchor-by-id
    (for/fold ([acc (hash)]) ([row (in-list anchor-rows)])
      (hash-set acc (hash-ref row 'id) row)))

  (define ids-map (hash-keys-sorted map-by-id))
  (define ids-anchors (hash-keys-sorted anchor-by-id))
  (define ids-ledger (hash-keys-sorted ledger-lines-by-id))

  (unless (equal? ids-map ids-anchors)
    (error 'build-adjudication-index
           "ID mismatch between RESOLUTION_MAP and TEST_ANCHOR_INDEX: map=~a anchors=~a"
           ids-map
           ids-anchors))
  (unless (equal? ids-map ids-ledger)
    (error 'build-adjudication-index
           "ID mismatch between RESOLUTION_MAP and ADJUDICATION_LEDGER rows: map=~a ledger=~a"
           ids-map
           ids-ledger))

  (for/list ([id (in-list ids-map)])
    (define map-row (hash-ref map-by-id id))
    (define anchor-row (hash-ref anchor-by-id id))
    (hasheq 'id id
            'disposition (hash-ref map-row 'disposition)
            'implementation-refs (hash-ref map-row 'implementation-refs)
            'test-anchors (hash-ref anchor-row 'anchors)
            'resolution-map-lines (list (hash-ref map-row 'line))
            'ledger-lines (hash-ref ledger-lines-by-id id)
            'notes "")))

(define (load-adjudication-index [index-path default-adjudication-index-path])
  (unless (file-exists? index-path)
    (error 'adjudication_index "index file missing: ~a" index-path))
  (define entries
    (call-with-input-file index-path read))
  (unless (list? entries)
    (error 'adjudication_index "index must contain a list, got ~e" entries))
  entries)

(define (all-strings? xs)
  (and (list? xs)
       (andmap string? xs)))

(define (all-positive-ints? xs)
  (and (list? xs)
       (andmap exact-positive-integer? xs)))

(define adjudication-id-rule
  (make-field-rule 'id
                   #t
                   (list (make-check
                          (lambda (v _ctx)
                            (and (string? v)
                                 (regexp-match? #px"^N[0-9][0-9]$" v)))
                          (lambda (v _ctx)
                            (format "id must match Nxx, got ~e" v))))))

(define adjudication-disposition-rule
  (make-field-rule
   'disposition
   #t
   (list (make-check
          (lambda (v _ctx) (memq v allowed-dispositions))
          (lambda (v _ctx)
            (format "disposition must be one of ~a, got ~e"
                    allowed-dispositions
                    v))))))

(define adjudication-implementation-refs-rule
  (make-field-rule
   'implementation-refs
   #t
   (list
    (make-check
     (lambda (v _ctx) (all-strings? v))
     (lambda (v _ctx)
       (format "implementation-refs must be list of strings, got ~e" v)))
    (make-check
     (lambda (v ctx)
       (or (not (all-strings? v))
           (null? (missing-relative-paths (hash-ref ctx 'root) v))))
     (lambda (v ctx)
       (format "implementation-refs path missing: ~a"
               (string-join (missing-relative-paths (hash-ref ctx 'root) v) ", ")))))))

(define adjudication-test-anchors-rule
  (make-field-rule
   'test-anchors
   #t
   (list (make-check
          (lambda (v _ctx) (all-strings? v))
          (lambda (v _ctx)
            (format "test-anchors must be list of strings, got ~e" v))))))

(define adjudication-resolution-map-lines-rule
  (make-field-rule
   'resolution-map-lines
   #t
   (list (make-check
          (lambda (v _ctx) (all-positive-ints? v))
          (lambda (v _ctx)
            (format "resolution-map-lines must be list of positive integers, got ~e" v))))))

(define adjudication-ledger-lines-rule
  (make-field-rule
   'ledger-lines
   #t
   (list (make-check
          (lambda (v _ctx) (all-positive-ints? v))
          (lambda (v _ctx)
            (format "ledger-lines must be list of positive integers, got ~e" v))))))

(define adjudication-notes-rule
  (make-field-rule
   'notes
   #t
   (list (make-check
          (lambda (v _ctx) (string? v))
          (lambda (v _ctx)
            (format "notes must be string, got ~e" v))))))

(define adjudication-entry-rules
  (list adjudication-id-rule
        adjudication-disposition-rule
        adjudication-implementation-refs-rule
        adjudication-test-anchors-rule
        adjudication-resolution-map-lines-rule
        adjudication-ledger-lines-rule
        adjudication-notes-rule))

(define (collect-adjudication-ids entries)
  (for/list ([entry (in-list entries)]
             #:when (and (hash? entry)
                         (hash-has-key? entry 'id)
                         (string? (hash-ref entry 'id))))
    (hash-ref entry 'id)))

(define (duplicate-id-error ids)
  (duplicate-string-id-error ids "duplicate IDs in adjudication index"))

(define (validate-adjudication-index entries)
  (define root (find-repo-root))
  (define errs
    (validate-entry-list entries
                         adjudication-entry-rules
                         (lambda (_entry _idx) (hasheq 'root root))))
  (define dupes-err
    (duplicate-id-error (collect-adjudication-ids entries)))
  (define final-errs
    (if dupes-err
        (append errs (list dupes-err))
        errs))

  (unless (null? final-errs)
    (error 'adjudication_index
           (string-append
            "adjudication-index validation failed:\n"
            (string-join final-errs "\n"))))
  entries)
