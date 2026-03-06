#lang racket/base

(require racket/cmdline
         racket/date
         racket/file
         racket/format
         racket/list
         racket/path
         racket/runtime-path
         racket/string
         json
         "../tests/regression-evidence/external/run-evidence.rkt")

(define-runtime-path default-manifest-path
  "../tests/regression-evidence/external/manifest.rktd")
(define-runtime-path default-json-out-path
  "../corpus/research/external-evidence-report.json")
(define-runtime-path default-md-out-path
  "../corpus/research/EXTERNAL_EVIDENCE_REPORT.md")

(define (hash-inc h k [n 1])
  (hash-set h k (+ n (hash-ref h k 0))))

(define (counts->rows h)
  (sort
   (for/list ([(k v) (in-hash h)])
     (hash 'label (~a k) 'count v))
   (lambda (a b)
     (define ca (hash-ref a 'count))
     (define cb (hash-ref b 'count))
     (if (= ca cb)
         (string<? (hash-ref a 'label) (hash-ref b 'label))
         (> ca cb)))))

(define (normalize-observed-message row)
  (define msg
    (~a (or (hash-ref row 'observed-message #f) "")))
  (if (string=? (string-trim msg) "")
      "(none)"
      (string-trim (car (string-split msg "\n")))))

(define (bucket-for row)
  (define status
    (~a (hash-ref row 'observed-status "unknown")))
  (define msg
    (string-downcase (normalize-observed-message row)))
  (cond
    [(string=? status "ok")
     "ok"]
    [(or (regexp-match? #px"unsupported version: 1\\.[0-9]" msg)
         (regexp-match? #px"unexpected newline at line [12], col 4" msg)
         (regexp-match? #px"unexpected id \\(\"stdio\\?\"\\)" msg)
         (regexp-match? #px"unexpected id \\(\"string\\?\"\\)" msg)
         (regexp-match? #px"unexpected id \\(\"raylib\\?\"\\)" msg))
     "strict-non-1.3-or-extension"]
    [(and (string=? status "parse-error")
          (or (regexp-match? #px"syntax error: unexpected" msg)
              (regexp-match? #px"invalid identifier syntax" msg)
              (regexp-match? #px"unterminated string literal" msg)
              (regexp-match? #px"line continuation marker must be at end of line" msg)))
     "program-bug-or-non-spec-input"]
    [(or (regexp-match? #px"invalid unicode normative name" msg)
         (regexp-match? #px"invalid unicode codepoint" msg)
         (regexp-match? #px"unicode surrogate codepoint" msg))
     "program-bug-or-non-spec-input"]
    [(and (string=? status "runtime-error")
          (regexp-match? #px"unknown slot:" msg))
     "runtime-program-assumption"]
    [(or (string=? status "parse-error")
         (string=? status "runtime-error")
         (string=? status "unsupported"))
     "possible-spec-divergence"]
    [else
     "needs-manual-triage"]))

(define (build-report rows)
  (define enriched
    (for/list ([r (in-list rows)])
      (define bucket (bucket-for r))
      (define msg (normalize-observed-message r))
      (hash-set* r
                 'bucket bucket
                 'normalized-message msg)))

  (define status-counts
    (for/fold ([acc (hash)]) ([r (in-list enriched)])
      (hash-inc acc (hash-ref r 'observed-status "unknown"))))
  (define bucket-counts
    (for/fold ([acc (hash)]) ([r (in-list enriched)])
      (hash-inc acc (hash-ref r 'bucket "unknown"))))
  (define project-counts
    (for/fold ([acc (hash)]) ([r (in-list enriched)])
      (hash-inc acc (hash-ref r 'project "unknown"))))
  (define message-counts
    (for/fold ([acc (hash)]) ([r (in-list enriched)])
      (if (string=? (hash-ref r 'normalized-message) "(none)")
          acc
          (hash-inc acc (hash-ref r 'normalized-message)))))

  (define candidates
    (for/list ([r (in-list enriched)]
               #:when (member (hash-ref r 'bucket)
                              '("possible-spec-divergence" "needs-manual-triage")))
      (hash 'id (hash-ref r 'id)
            'project (hash-ref r 'project)
            'source-kind (hash-ref r 'source-kind)
            'source-id (hash-ref r 'source-id)
            'source-url (hash-ref r 'source-url)
            'source-file (hash-ref r 'source-file)
            'observed-status (hash-ref r 'observed-status)
            'message (hash-ref r 'normalized-message)
            'triage-status (hash-ref r 'triage-status)
            'hypothesis (hash-ref r 'hypothesis))))

  (hash 'generated-at (date->string (current-date) #t)
        'totals (hash 'cases (length enriched))
        'status-counts (counts->rows status-counts)
        'bucket-counts (counts->rows bucket-counts)
        'project-counts (counts->rows project-counts)
        'top-messages (take (counts->rows message-counts)
                            (min 25 (hash-count message-counts)))
        'candidates candidates))

(define (write-json-report path report)
  (make-directory* (or (path-only path) (current-directory)))
  (call-with-output-file path
    (lambda (out)
      (write-json report out))
    #:exists 'truncate/replace))

(define (write-md-report path report json-path)
  (define status-counts (hash-ref report 'status-counts))
  (define bucket-counts (hash-ref report 'bucket-counts))
  (define top-messages (hash-ref report 'top-messages))
  (define candidates (hash-ref report 'candidates))

  (make-directory* (or (path-only path) (current-directory)))
  (call-with-output-file path
    (lambda (out)
      (fprintf out "# External Evidence Report\n\n")
      (fprintf out "Generated: `~a`\n\n" (hash-ref report 'generated-at))
      (fprintf out "- Cases evaluated: `~a`\n" (hash-ref (hash-ref report 'totals) 'cases))
      (fprintf out "- JSON report: `~a`\n\n" (path->string json-path))

      (fprintf out "## Observed Status Counts\n\n")
      (for ([row (in-list status-counts)])
        (fprintf out "- `~a`: `~a`\n"
                 (hash-ref row 'label)
                 (hash-ref row 'count)))

      (fprintf out "\n## Bucket Counts\n\n")
      (for ([row (in-list bucket-counts)])
        (fprintf out "- `~a`: `~a`\n"
                 (hash-ref row 'label)
                 (hash-ref row 'count)))

      (fprintf out "\n## Top Messages\n\n")
      (for ([row (in-list top-messages)])
        (fprintf out "- `~a` (`~a`)\n"
                 (hash-ref row 'label)
                 (hash-ref row 'count)))

      (fprintf out "\n## Possible Divergence Candidates\n\n")
      (if (null? candidates)
          (fprintf out "- None.\n")
          (for ([c (in-list candidates)])
            (fprintf out "- `~a` (`~a` / `~a`): `~a`\n"
                     (hash-ref c 'id)
                     (hash-ref c 'project)
                     (hash-ref c 'observed-status)
                     (hash-ref c 'message)))))
    #:exists 'truncate/replace))

(module+ main
  (define manifest-path default-manifest-path)
  (define json-out-path default-json-out-path)
  (define md-out-path default-md-out-path)

  (command-line
   #:program "analyze_external_evidence.rkt"
   #:once-each
   [("--manifest") path "Path to external evidence manifest"
                    (set! manifest-path (string->path path))]
   [("--json-out") path "JSON output path"
                    (set! json-out-path (string->path path))]
   [("--md-out") path "Markdown output path"
                  (set! md-out-path (string->path path))])

  (define rows
    (evaluate-evidence-cases manifest-path #f #f))
  (define report
    (build-report rows))

  (write-json-report json-out-path report)
  (write-md-report md-out-path report json-out-path)

  (printf "Wrote JSON report: ~a\n" (path->string json-out-path))
  (printf "Wrote Markdown report: ~a\n" (path->string md-out-path))
  (printf "Cases evaluated: ~a\n" (hash-ref (hash-ref report 'totals) 'cases)))
