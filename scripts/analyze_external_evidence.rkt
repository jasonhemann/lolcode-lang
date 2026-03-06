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

(define valid-triage-status
  '("candidate"
    "reproducer-ready"
    "spec-ambiguous"
    "known-divergence"
    "out-of-spec-1.4"
    "promoted-conformance"))

(define valid-hypotheses
  '("unknown"
    "expects-pass"
    "expects-parse-error"
    "expects-runtime-error"))

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

(define (parse-scope-arg s)
  (cond
    [(string=? s "1.2") '("1.2")]
    [(string=? s "1.3") '("1.3")]
    [(or (string=? s "1.2+1.3")
         (string=? s "1.3+1.2"))
     '("1.2" "1.3")]
    [(string=? s "unknown") '("unknown")]
    [else
     (error 'analyze-external-evidence
            "--scope must be one of 1.2, 1.3, 1.2+1.3, unknown; got ~e"
            s)]))

(define (parse-one-of who arg allowed)
  (unless (member arg allowed)
    (error 'analyze-external-evidence
           "~a must be one of ~a, got ~e"
           who
           (string-join allowed ", ")
           arg))
  arg)

(define (scope-label scope)
  (cond
    [(equal? scope '("1.2")) "1.2"]
    [(equal? scope '("1.3")) "1.3"]
    [(equal? scope '("1.2" "1.3")) "1.2+1.3"]
    [(equal? scope '("unknown")) "unknown"]
    [else (format "~s" scope)]))

(define (filter-value->label v kind)
  (cond
    [(eq? v #f) "all"]
    [(eq? kind 'scope) (scope-label v)]
    [else (~a v)]))

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

(define (build-report rows
                      selected-wave
                      selected-id
                      selected-scope
                      selected-triage
                      selected-hypothesis)
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
  (define scope-counts
    (for/fold ([acc (hash)]) ([r (in-list enriched)])
      (hash-inc acc (scope-label (hash-ref r 'spec-scope '("unknown"))))))

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
  (define unknown-scope
    (for/list ([r (in-list enriched)]
               #:when (equal? (hash-ref r 'spec-scope '("unknown")) '("unknown")))
      (hash 'id (hash-ref r 'id)
            'project (hash-ref r 'project)
            'source-kind (hash-ref r 'source-kind)
            'source-id (hash-ref r 'source-id)
            'source-url (hash-ref r 'source-url)
            'source-file (hash-ref r 'source-file)
            'observed-status (hash-ref r 'observed-status)
            'message (hash-ref r 'normalized-message))))

  (hash 'generated-at (date->string (current-date) #t)
        'filters (hash 'wave (filter-value->label selected-wave 'wave)
                       'id (filter-value->label selected-id 'id)
                       'scope (filter-value->label selected-scope 'scope)
                       'triage-status (filter-value->label selected-triage 'triage-status)
                       'hypothesis (filter-value->label selected-hypothesis 'hypothesis))
        'totals (hash 'cases (length enriched))
        'status-counts (counts->rows status-counts)
        'bucket-counts (counts->rows bucket-counts)
        'spec-scope-counts (counts->rows scope-counts)
        'project-counts (counts->rows project-counts)
        'top-messages (take (counts->rows message-counts)
                            (min 25 (hash-count message-counts)))
        'unknown-spec-scope unknown-scope
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
  (define scope-counts (hash-ref report 'spec-scope-counts))
  (define top-messages (hash-ref report 'top-messages))
  (define unknown-scope (hash-ref report 'unknown-spec-scope))
  (define candidates (hash-ref report 'candidates))
  (define filters (hash-ref report 'filters))

  (make-directory* (or (path-only path) (current-directory)))
  (call-with-output-file path
    (lambda (out)
      (fprintf out "# External Evidence Report\n\n")
      (fprintf out "Generated: `~a`\n\n" (hash-ref report 'generated-at))
      (fprintf out "- Cases evaluated: `~a`\n" (hash-ref (hash-ref report 'totals) 'cases))
      (fprintf out "- Filters: wave=`~a`, id=`~a`, scope=`~a`, triage=`~a`, hypothesis=`~a`\n"
               (hash-ref filters 'wave)
               (hash-ref filters 'id)
               (hash-ref filters 'scope)
               (hash-ref filters 'triage-status)
               (hash-ref filters 'hypothesis))
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

      (fprintf out "\n## Spec Scope Counts\n\n")
      (for ([row (in-list scope-counts)])
        (fprintf out "- `~a`: `~a`\n"
                 (hash-ref row 'label)
                 (hash-ref row 'count)))

      (fprintf out "\n## Unknown Spec Scope Cases\n\n")
      (if (null? unknown-scope)
          (fprintf out "- None.\n")
          (for ([c (in-list unknown-scope)])
            (fprintf out "- `~a` (`~a` / `~a`): `~a`\n"
                     (hash-ref c 'id)
                     (hash-ref c 'project)
                     (hash-ref c 'observed-status)
                     (hash-ref c 'message))))

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
  (define selected-wave #f)
  (define selected-id #f)
  (define selected-scope #f)
  (define selected-triage #f)
  (define selected-hypothesis #f)

  (command-line
   #:program "analyze_external_evidence.rkt"
   #:once-each
   [("--manifest") path "Path to external evidence manifest"
                    (set! manifest-path (string->path path))]
   [("--json-out") path "JSON output path"
                    (set! json-out-path (string->path path))]
   [("--md-out") path "Markdown output path"
                  (set! md-out-path (string->path path))]
   [("--wave") w "Select only wave N"
                (define maybe-wave (string->number w))
                (unless (and maybe-wave
                             (exact-integer? maybe-wave)
                             (> maybe-wave 0))
                  (error 'analyze-external-evidence
                         "--wave must be a positive integer, got ~e"
                         w))
                (set! selected-wave maybe-wave)]
   [("--id") case-id "Select only one case id"
               (set! selected-id case-id)]
   [("--scope") s "Select only one spec scope: 1.2 | 1.3 | 1.2+1.3 | unknown"
                 (set! selected-scope (parse-scope-arg s))]
   [("--triage") s "Select only one triage-status"
                  (set! selected-triage
                        (parse-one-of "--triage" s valid-triage-status))]
   [("--hypothesis") s "Select only one hypothesis"
                      (set! selected-hypothesis
                            (parse-one-of "--hypothesis" s valid-hypotheses))])

  (define rows
    (evaluate-evidence-cases manifest-path
                             selected-wave
                             selected-id
                             selected-scope
                             selected-triage
                             selected-hypothesis))
  (define report
    (build-report rows
                  selected-wave
                  selected-id
                  selected-scope
                  selected-triage
                  selected-hypothesis))

  (write-json-report json-out-path report)
  (write-md-report md-out-path report json-out-path)

  (printf "Wrote JSON report: ~a\n" (path->string json-out-path))
  (printf "Wrote Markdown report: ~a\n" (path->string md-out-path))
  (printf "Cases evaluated: ~a\n" (hash-ref (hash-ref report 'totals) 'cases)))
