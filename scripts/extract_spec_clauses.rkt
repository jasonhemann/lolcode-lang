#lang racket/base

(require racket/cmdline
         racket/file
         racket/list
         racket/match
         racket/path
         racket/string)

(define (find-repo-root [start (current-directory)])
  (define marker (build-path start "AGENTS.md"))
  (cond
    [(file-exists? marker) start]
    [else
     (define parent (simplify-path (build-path start 'up)))
     (if (equal? parent start)
         (error 'extract_spec_clauses
                "could not locate repository root from ~a"
                start)
         (find-repo-root parent))]))

(define (path-under-root root p)
  (if (absolute-path? p)
      p
      (build-path root p)))

(define (sanitize text)
  (string-replace (string-trim text) "\t" " "))

(define (normative-line? text)
  (regexp-match?
   #px"(?i:(must|should|may|optional|cannot|can't|error|requires|terminated|opened|closed|valid))"
   text))

(define (extract-rows lines)
  (define rows '())
  (define in-code-block? #f)
  (for ([line (in-list lines)]
        [ln (in-naturals 1)])
    (when (regexp-match? #px"^```" line)
      (set! in-code-block? (not in-code-block?)))
    (unless in-code-block?
      (define heading-match
        (regexp-match #px"^(#{2,6})\\s+(.+)$" line))
      (when heading-match
        (define heading-text
          (sanitize (list-ref heading-match 2)))
        (set! rows
              (cons (list ln "heading" heading-text)
                    rows)))
      (when (and (not heading-match)
                 (normative-line? line))
        (define txt (sanitize line))
        (when (positive? (string-length txt))
          (set! rows
                (cons (list ln "normative" txt)
                      rows))))))
  (reverse rows))

(module+ main
  (define root (find-repo-root))
  (define in-path
    (path-under-root root "spec/upstream/lolcode-spec-v1.3.md"))
  (define out-path
    (path-under-root root "spec/traceability/spec-1.3-clause-index.tsv"))
  (command-line
   #:program "extract_spec_clauses.rkt"
   #:once-each
   [("--in") p "Input spec markdown path." (set! in-path (path-under-root root p))]
   [("--out") p "Output TSV path." (set! out-path (path-under-root root p))])
  (unless (file-exists? in-path)
    (error 'extract_spec_clauses "input file missing: ~a" in-path))
  (define rows
    (extract-rows (file->lines in-path)))
  (call-with-output-file out-path
    (lambda (out)
      (fprintf out "line\tkind\ttext\n")
      (for ([row (in-list rows)])
        (match-define (list ln kind txt) row)
        (fprintf out "~a\t~a\t~a\n" ln kind txt)))
    #:exists 'truncate/replace)
  (printf "wrote ~a rows to ~a\n" (length rows) out-path))
