#lang racket/base

(require racket/cmdline
         racket/date
         racket/file
         racket/format
         racket/list
         racket/path
         racket/runtime-path
         racket/string
         "./external_evidence_common.rkt")

(define-runtime-path default-manifest-path
  "../tests/regression-evidence/external/manifest.rktd")
(define-runtime-path default-json-out-path
  "../corpus/research/external-evidence-spec-scope-seed.json")
(define-runtime-path default-md-out-path
  "../corpus/research/EXTERNAL_EVIDENCE_SPEC_SCOPE_SEED.md")

(define (line-id line)
  (define m
    (regexp-match #px"^\\s*\\(id \\. \"([^\"]+)\"\\)" line))
  (and m (list-ref m 1)))

(define (line-spec-scope line)
  (define m
    (regexp-match #px"^(\\s*\\(spec-scope \\. )\\(([^)]*)\\)(\\).*)$" line))
  (and m
       (hash 'prefix (list-ref m 1)
             'body (list-ref m 2)
             'suffix (list-ref m 3))))

(define (format-scope-body scope-list)
  (string-join (map (lambda (s) (format "\"~a\"" s)) scope-list) " "))

(define (meaningful-lines path)
  (for/list ([line (in-list (file->lines path))]
             #:unless (string=? (string-trim line) ""))
    line))

(define (infer-scope-from-source source-path)
  (define lines
    (meaningful-lines source-path))
  (define first-line
    (for/first ([line (in-list lines)]
                #:unless (regexp-match? #px"^\\s*BTW\\b" line))
      line))
  (cond
    [(not first-line) '("unknown")]
    [else
     (define m
       (regexp-match #px"^(?i:\\s*HAI\\s+([0-9]+\\.[0-9]+)\\b)" first-line))
     (cond
       [(not m) '("unknown")]
       [(string=? (list-ref m 1) "1.2") '("1.2")]
       [(string=? (list-ref m 1) "1.3") '("1.3")]
       [else '("unknown")])]))

(define (build-scope-index manifest-path)
  (define manifest-dir
    (or (path-only (simplify-path manifest-path))
        (current-directory)))
  (define manifest
    (call-with-input-file manifest-path read))
  (for/hash ([entry (in-list manifest)])
    (define id (hash-ref entry 'id))
    (define source-file (hash-ref entry 'source-file))
    (define source-path (build-path manifest-dir source-file))
    (values id (infer-scope-from-source source-path))))

(define (update-manifest-lines lines scopes overwrite?)
  (define current-id #f)
  (define changed '())
  (define updated-lines
    (for/list ([line (in-list lines)])
      (define maybe-id (line-id line))
      (when maybe-id
        (set! current-id maybe-id))
      (define maybe-s (line-spec-scope line))
      (if (and maybe-s
               current-id
               (hash-has-key? scopes current-id))
          (let* ([new-scope (hash-ref scopes current-id)]
                 [existing-body (hash-ref maybe-s 'body)]
                 [new-body (format-scope-body new-scope)]
                 [existing-unknown? (string=? (string-trim existing-body) "\"unknown\"")]
                 [new-unknown? (equal? new-scope '("unknown"))])
            (cond
              [(and (not overwrite?) (not existing-unknown?))
               line]
              [(and (not overwrite?) new-unknown?)
               line]
              [(string=? (string-trim existing-body) new-body)
               line]
              [else
               (set! changed
                     (cons (hash 'id current-id
                                 'old (string-append "(" existing-body ")")
                                 'new (string-append "(" new-body ")"))
                           changed))
               (string-append
                (hash-ref maybe-s 'prefix)
                "("
                new-body
                ")"
                (hash-ref maybe-s 'suffix))]))
          line)))
  (values updated-lines (reverse changed)))

(define (write-md-report path report json-path)
  (make-directory* (or (path-only path) (current-directory)))
  (call-with-output-file path
    (lambda (out)
      (fprintf out "# External Evidence Spec-Scope Seeding\n\n")
      (fprintf out "Generated: `~a`\n\n" (hash-ref report 'generated-at))
      (fprintf out "- JSON report: `~a`\n\n" (path->string json-path))
      (fprintf out "## Summary\n\n")
      (fprintf out "- Scope suggestions: `~a`\n"
               (hash-ref (hash-ref report 'totals) 'scope-suggestions))
      (fprintf out "- Manifest entries updated: `~a`\n"
               (hash-ref (hash-ref report 'totals) 'entries-updated))
      (fprintf out "- Apply mode: `~a`\n\n"
               (if (hash-ref report 'applied?) "true" "false"))

      (fprintf out "## Suggested Scope Counts\n\n")
      (for ([row (in-list (hash-ref report 'scope-counts))])
        (fprintf out "- `~a`: `~a`\n"
                 (hash-ref row 'label)
                 (hash-ref row 'count)))

      (fprintf out "\n## Scope Updates (sample)\n\n")
      (define changes (hash-ref report 'changes))
      (if (null? changes)
          (fprintf out "- None.\n")
          (for ([c (in-list (take changes (min 25 (length changes))))])
            (fprintf out "- `~a`: `~a` -> `~a`\n"
                     (hash-ref c 'id)
                     (hash-ref c 'old)
                     (hash-ref c 'new)))))
    #:exists 'truncate/replace))

(module+ main
  (define manifest-path default-manifest-path)
  (define json-out-path default-json-out-path)
  (define md-out-path default-md-out-path)
  (define apply? #f)
  (define overwrite? #f)

  (command-line
   #:program "seed_external_manifest_spec_scope.rkt"
   #:once-each
   [("--manifest") path "Manifest path"
                    (set! manifest-path (string->path path))]
   [("--json-out") path "JSON output path"
                    (set! json-out-path (string->path path))]
   [("--md-out") path "Markdown output path"
                  (set! md-out-path (string->path path))]
   [("--apply") "Write inferred scope updates into manifest"
                (set! apply? #t)]
   [("--overwrite-existing") "Overwrite existing non-unknown scope values"
                             (set! overwrite? #t)])

  (define scopes
    (build-scope-index manifest-path))
  (define scope-counts-h
    (for/fold ([acc (hash)]) ([v (in-hash-values scopes)])
      (hash-inc acc v)))

  (define manifest-lines
    (file->lines manifest-path))
  (define-values (updated-lines changes)
    (update-manifest-lines manifest-lines scopes overwrite?))

  (when apply?
    (call-with-output-file manifest-path
      (lambda (out)
        (for ([line (in-list updated-lines)])
          (displayln line out)))
      #:exists 'truncate/replace))

  (define report
    (hash 'generated-at (date->string (current-date) #t)
          'manifest-path (path->string manifest-path)
          'applied? apply?
          'overwrite-existing? overwrite?
          'totals (hash 'scope-suggestions (hash-count scopes)
                       'entries-updated (length changes))
          'scope-counts (counts->rows scope-counts-h)
          'changes changes))

  (write-json-report json-out-path report)
  (write-md-report md-out-path report json-out-path)

  (printf "Wrote JSON report: ~a\n" (path->string json-out-path))
  (printf "Wrote Markdown report: ~a\n" (path->string md-out-path))
  (printf "Scope suggestions: ~a\n" (hash-count scopes))
  (printf "Manifest entries updated: ~a\n" (length changes))
  (printf "Applied: ~a\n" (if apply? "yes" "no")))
