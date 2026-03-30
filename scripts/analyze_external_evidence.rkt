#lang racket/base

(require racket/date
         racket/file
         racket/format
         racket/list
         racket/path
         racket/runtime-path
         racket/string
         "./external_evidence_common.rkt"
         "./validation_rules_lib.rkt"
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

(define (parse-positive-wave who raw)
  (define maybe-wave
    (string->number raw))
  (unless (and maybe-wave
               (exact-integer? maybe-wave)
               (> maybe-wave 0))
    (error 'analyze-external-evidence
           "~a must be a positive integer, got ~e"
           who
           raw))
  maybe-wave)

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
  (define option-specs
    (list (hasheq 'flag "--manifest" 'key 'manifest-path
                  'mode 'value 'convert string->path)
          (hasheq 'flag "--json-out" 'key 'json-out-path
                  'mode 'value 'convert string->path)
          (hasheq 'flag "--md-out" 'key 'md-out-path
                  'mode 'value 'convert string->path)
          (hasheq 'flag "--wave" 'key 'selected-wave
                  'mode 'value
                  'convert (lambda (w)
                             (parse-positive-wave "--wave" w)))
          (hasheq 'flag "--id" 'key 'selected-id 'mode 'value)
          (hasheq 'flag "--scope" 'key 'selected-scope
                  'mode 'value 'convert parse-scope-arg)
          (hasheq 'flag "--triage" 'key 'selected-triage
                  'mode 'value
                  'convert (lambda (s)
                             (parse-one-of "--triage" s valid-triage-status)))
          (hasheq 'flag "--hypothesis" 'key 'selected-hypothesis
                  'mode 'value
                  'convert (lambda (s)
                             (parse-one-of "--hypothesis" s valid-hypotheses)))))
  (define option-defaults
    (hasheq 'manifest-path default-manifest-path
            'json-out-path default-json-out-path
            'md-out-path default-md-out-path
            'selected-wave #f
            'selected-id #f
            'selected-scope #f
            'selected-triage #f
            'selected-hypothesis #f))
  (define opts
    (parse-cli-options 'analyze-external-evidence
                       (vector->list (current-command-line-arguments))
                       option-specs
                       option-defaults))

  (define rows
    (evaluate-evidence-cases (hash-ref opts 'manifest-path)
                             (hash-ref opts 'selected-wave)
                             (hash-ref opts 'selected-id)
                             (hash-ref opts 'selected-scope)
                             (hash-ref opts 'selected-triage)
                             (hash-ref opts 'selected-hypothesis)))
  (define report
    (build-report rows
                  (hash-ref opts 'selected-wave)
                  (hash-ref opts 'selected-id)
                  (hash-ref opts 'selected-scope)
                  (hash-ref opts 'selected-triage)
                  (hash-ref opts 'selected-hypothesis)))

  (write-json-report (hash-ref opts 'json-out-path) report)
  (write-md-report (hash-ref opts 'md-out-path)
                   report
                   (hash-ref opts 'json-out-path))

  (printf "Wrote JSON report: ~a\n"
          (path->string (hash-ref opts 'json-out-path)))
  (printf "Wrote Markdown report: ~a\n"
          (path->string (hash-ref opts 'md-out-path)))
  (printf "Cases evaluated: ~a\n" (hash-ref (hash-ref report 'totals) 'cases)))
