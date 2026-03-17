#lang racket/base

(require json
         racket/file
         racket/format
         racket/list
         racket/path
         racket/string
         "adjudication_index_lib.rkt")

(provide default-spec-file
         default-traceability-graph-path
         default-spec-path
         default-clause-spans-path
         build-traceability-clause-spans
         load-traceability-clause-spans
         validate-traceability-clause-spans)

(define default-spec-file
  "spec/upstream/lolcode-spec-v1.3.md")

(define default-traceability-graph-path
  (build-path (find-repo-root)
              "spec"
              "traceability"
              "traceability-graph.json"))

(define default-spec-path
  (build-path (find-repo-root)
              "spec"
              "upstream"
              "lolcode-spec-v1.3.md"))

(define default-clause-spans-path
  (build-path (find-repo-root)
              "spec"
              "traceability"
              "traceability-clause-spans.json"))

(define (entry-error idx fmt . args)
  (format "entry ~a: ~a" idx (apply format fmt args)))

(define (json-hash path who)
  (unless (file-exists? path)
    (error who "missing JSON file: ~a" path))
  (define v
    (call-with-input-file path read-json))
  (unless (hash? v)
    (error who "expected JSON object at ~a, got ~e" path v))
  v)

(define (first-non-space-column text)
  (define len (string-length text))
  (define (go idx)
    (cond
      [(= idx len) 0]
      [(char-whitespace? (string-ref text idx))
       (go (add1 idx))]
      [else idx]))
  (go 0))

(define (trimmed-line-span line-text)
  (define len
    (string-length line-text))
  (when (zero? len)
    (error 'build-traceability-clause-spans
           "cannot derive span from empty source line"))
  (define left
    (first-non-space-column line-text))
  (define start-col
    (add1 left))
  (define end-col
    (add1 len))
  (if (< start-col end-col)
      (values start-col end-col)
      (values 1 end-col)))

(define (substring-span line-text clause-text)
  (cond
    [(string-contains? line-text clause-text)
     => (lambda (start-idx)
          (define start-col
            (add1 start-idx))
          (define end-col
            (+ start-col (string-length clause-text)))
          (values start-col end-col))]
    [else
     (trimmed-line-span line-text)]))

(define (line-at spec-lines line-no)
  (if (and (exact-positive-integer? line-no)
           (<= line-no (length spec-lines)))
      (list-ref spec-lines (sub1 line-no))
      (error 'build-traceability-clause-spans
             "source line ~a is out of bounds for spec"
             line-no)))

(define (id<? a b)
  (string<? a b))

(define (clause-id<? a b)
  (id<? (hash-ref a 'id) (hash-ref b 'id)))

(define (build-traceability-clause-spans
         [graph-path default-traceability-graph-path]
         [spec-path default-spec-path])
  (define graph
    (json-hash graph-path 'build-traceability-clause-spans))
  (define clauses
    (hash-ref graph 'clauses))
  (unless (list? clauses)
    (error 'build-traceability-clause-spans
           "graph clauses must be a list, got ~e"
           clauses))
  (unless (file-exists? spec-path)
    (error 'build-traceability-clause-spans
           "spec file missing: ~a"
           spec-path))
  (define spec-lines
    (file->lines spec-path))
  (define span-rows
    (for/list ([clause (in-list (sort clauses clause-id<?))])
      (define clause-id
        (hash-ref clause 'id))
      (define source-line
        (hash-ref clause 'source_line))
      (define clause-text
        (hash-ref clause 'clause))
      (unless (string? clause-id)
        (error 'build-traceability-clause-spans
               "clause id must be string, got ~e"
               clause-id))
      (unless (string? clause-text)
        (error 'build-traceability-clause-spans
               "clause text must be string, got ~e"
               clause-text))
      (define line-text
        (line-at spec-lines source-line))
      (define-values (start-col end-col)
        (substring-span line-text clause-text))
      (hasheq 'clause_id clause-id
              'start (hasheq 'line source-line
                             'column start-col)
              'end (hasheq 'line source-line
                           'column end-col))))
  (hasheq 'schema_version 1
          'spec_file default-spec-file
          'clauses span-rows))

(define (load-traceability-clause-spans
         [spans-path default-clause-spans-path])
  (json-hash spans-path 'load-traceability-clause-spans))

(define (line-column-errors idx which pos spec-lines)
  (define line
    (hash-ref pos 'line #f))
  (define col
    (hash-ref pos 'column #f))
  (define line-valid?
    (and (exact-positive-integer? line)
         (<= line (length spec-lines))))
  (cond
    [(not (hash? pos))
     (list (entry-error idx
                        "~a must be object with line/column"
                        which))]
    [else
     (append
      (if line-valid?
          '()
          (list (entry-error idx
                             "~a.line out of range: ~e"
                             which
                             line)))
      (cond
        [(not (exact-positive-integer? col))
         (list (entry-error idx
                            "~a.column must be positive integer: ~e"
                            which
                            col))]
        [line-valid?
         (define line-len
           (string-length (list-ref spec-lines (sub1 line))))
         (if (<= col (add1 line-len))
             '()
             (list (entry-error idx
                                "~a.column out of range: ~e"
                                which
                                col)))]
        [else '()]))]))

(define (span-order-valid? start-pos end-pos)
  (define sl
    (hash-ref start-pos 'line #f))
  (define sc
    (hash-ref start-pos 'column #f))
  (define el
    (hash-ref end-pos 'line #f))
  (define ec
    (hash-ref end-pos 'column #f))
  (and (exact-positive-integer? sl)
       (exact-positive-integer? sc)
       (exact-positive-integer? el)
       (exact-positive-integer? ec)
       (or (< sl el)
           (and (= sl el)
                (< sc ec)))))

(define (duplicate-ids ids)
  (define counts
    (for/fold ([h (hash)])
              ([id (in-list ids)])
      (hash-update h id add1 0)))
  (sort
   (for/list ([(id count) (in-hash counts)]
              #:when (> count 1))
     id)
   string<?))

(define (validate-traceability-clause-spans
         spans
         [graph-path default-traceability-graph-path]
         [spec-path default-spec-path])
  (define graph
    (json-hash graph-path 'validate-traceability-clause-spans))
  (define graph-clauses
    (hash-ref graph 'clauses))
  (define graph-ids
    (sort
     (for/list ([c (in-list graph-clauses)])
       (hash-ref c 'id))
     string<?))
  (unless (file-exists? spec-path)
    (error 'validate-traceability-clause-spans
           "spec file missing: ~a"
           spec-path))
  (define spec-lines
    (file->lines spec-path))
  (unless (hash? spans)
    (error 'validate-traceability-clause-spans
           "spans artifact must be JSON object"))
  (define schema-version
    (hash-ref spans 'schema_version #f))
  (define spec-file
    (hash-ref spans 'spec_file #f))
  (define clauses
    (hash-ref spans 'clauses #f))
  (define base-errors
    (append
     (if (equal? schema-version 1)
         '()
         (list "schema_version must be 1"))
     (if (equal? spec-file default-spec-file)
         '()
         (list (format "spec_file must be ~a" default-spec-file)))
     (if (list? clauses)
         '()
         (list "clauses must be array/list"))))
  (define clause-errors
    (if (list? clauses)
        (append*
         (for/list ([entry (in-list clauses)]
                    [idx (in-naturals 1)])
           (if (hash? entry)
               (let ([clause-id (hash-ref entry 'clause_id #f)]
                     [start-pos (hash-ref entry 'start #f)]
                     [end-pos (hash-ref entry 'end #f)])
                 (append
                  (if (and (string? clause-id)
                           (not (string=? clause-id "")))
                      '()
                      (list (entry-error idx
                                         "clause_id must be non-empty string")))
                  (line-column-errors idx "start" start-pos spec-lines)
                  (line-column-errors idx "end" end-pos spec-lines)
                  (if (and (hash? start-pos)
                           (hash? end-pos)
                           (span-order-valid? start-pos end-pos))
                      '()
                      (list (entry-error idx
                                         "span must be non-empty with start<end")))))
               (list (entry-error idx "entry must be object")))))
        '()))
  (define span-ids
    (if (list? clauses)
        (for/list ([entry (in-list clauses)]
                   #:when (and (hash? entry)
                               (string? (hash-ref entry 'clause_id #f))))
          (hash-ref entry 'clause_id))
        '()))
  (define dupes
    (duplicate-ids span-ids))
  (define id-errors
    (if (list? clauses)
        (let* ([span-id-set (sort (remove-duplicates span-ids) string<?)]
               [missing (filter (lambda (id)
                                  (not (member id span-id-set)))
                                graph-ids)]
               [extras (filter (lambda (id)
                                 (not (member id graph-ids)))
                               span-id-set)])
          (append
           (if (null? dupes)
               '()
               (list (format "duplicate clause_id values: ~a"
                             (string-join dupes ", "))))
           (if (null? missing)
               '()
               (list (format "missing clause_id values: ~a"
                             (string-join missing ", "))))
           (if (null? extras)
               '()
               (list (format "unknown extra clause_id values: ~a"
                             (string-join extras ", "))))))
        '()))
  (define all-errors
    (append base-errors clause-errors id-errors))
  (unless (null? all-errors)
    (error 'validate-traceability-clause-spans
           (string-append
            "traceability-clause-spans validation failed:\n"
            (string-join all-errors "\n"))))
  spans)
