#lang racket/base

(require racket/cmdline
         racket/date
         racket/file
         racket/format
         racket/list
         racket/path
         racket/runtime-path
         racket/string
         json)

(define-runtime-path default-manifest-path
  "../tests/regression-evidence/external/manifest.rktd")
(define-runtime-path default-json-out-path
  "../corpus/research/external-evidence-spec-scope-unknowns.json")
(define-runtime-path default-md-out-path
  "../corpus/research/EXTERNAL_EVIDENCE_SPEC_SCOPE_UNKNOWNS.md")

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

(define (truncate-line s [max-len 120])
  (if (> (string-length s) max-len)
      (string-append (substring s 0 max-len) "...")
      s))

(define (safe-first-meaningful-line source-path)
  (with-handlers ([exn:fail? (lambda (_) #f)])
    (define lines (file->lines source-path))
    (for/first ([line (in-list lines)]
                #:unless (string=? (string-trim line) ""))
      line)))

(define (classify-unknown-source first-line)
  (cond
    [(not first-line)
     (values "empty-or-unreadable" "keep-unknown")]
    [(regexp-match? #px"(?i:^\\s*HAI\\s+[0-9]+\\.[0-9]+\\b)" first-line)
     (values "has-versioned-hai-header" "re-check-seeding-logic")]
    [(regexp-match? #px"(?i:^\\s*HAI\\b)" first-line)
     (values "hai-missing-version" "keep-unknown")]
    [(regexp-match? #px"(?i:^\\s*(echo|dd|cat|printf|#!/|bash\\b))" first-line)
     (values "non-lolcode-shell-snippet" "keep-unknown")]
    [(regexp-match? #px"^\\s*R[A-Z]{2,3}\\s+0x[0-9a-fA-F]+" first-line)
     (values "non-program-crash-dump" "keep-unknown")]
    [else
     (values "no-detectable-hai-header" "keep-unknown")]))

(define (build-report manifest-path)
  (define manifest-dir
    (or (path-only (simplify-path manifest-path))
        (current-directory)))
  (define manifest
    (call-with-input-file manifest-path read))
  (define unknowns
    (for/list ([entry (in-list manifest)]
               #:when (equal? (hash-ref entry 'spec-scope '()) '("unknown")))
      entry))

  (define entries
    (for/list ([entry (in-list unknowns)])
      (define source-file (hash-ref entry 'source-file))
      (define source-path (build-path manifest-dir source-file))
      (define first-line (safe-first-meaningful-line source-path))
      (define-values (reason action)
        (classify-unknown-source first-line))
      (hash 'id (hash-ref entry 'id)
            'source-project (hash-ref entry 'source-project)
            'source-kind (hash-ref entry 'source-kind)
            'source-id (hash-ref entry 'source-id)
            'source-url (hash-ref entry 'source-url)
            'source-file source-file
            'reason reason
            'suggested-action action
            'first-line (or first-line "(none)"))))

  (define reason-counts
    (for/fold ([acc (hash)]) ([e (in-list entries)])
      (hash-inc acc (hash-ref e 'reason))))

  (hash 'generated-at (date->string (current-date) #t)
        'manifest-path (path->string manifest-path)
        'totals (hash 'unknown-entries (length unknowns))
        'reason-counts (counts->rows reason-counts)
        'entries entries))

(define (write-json-report path report)
  (make-directory* (or (path-only path) (current-directory)))
  (call-with-output-file path
    (lambda (out)
      (write-json report out))
    #:exists 'truncate/replace))

(define (write-md-report path report json-path)
  (make-directory* (or (path-only path) (current-directory)))
  (call-with-output-file path
    (lambda (out)
      (fprintf out "# External Evidence Spec-Scope Unknowns\n\n")
      (fprintf out "Generated: `~a`\n\n" (hash-ref report 'generated-at))
      (fprintf out "- Unknown entries: `~a`\n"
               (hash-ref (hash-ref report 'totals) 'unknown-entries))
      (fprintf out "- JSON report: `~a`\n\n" (path->string json-path))

      (fprintf out "## Reason Counts\n\n")
      (for ([row (in-list (hash-ref report 'reason-counts))])
        (fprintf out "- `~a`: `~a`\n"
                 (hash-ref row 'label)
                 (hash-ref row 'count)))

      (fprintf out "\n## Entries\n\n")
      (define entries (hash-ref report 'entries))
      (if (null? entries)
          (fprintf out "- None.\n")
          (for ([e (in-list entries)])
            (fprintf out "- `~a` (`~a` / `~a`): `~a` | action=`~a`\n"
                     (hash-ref e 'id)
                     (hash-ref e 'source-project)
                     (hash-ref e 'source-kind)
                     (hash-ref e 'reason)
                     (hash-ref e 'suggested-action))
            (fprintf out "  - file: `~a`\n" (hash-ref e 'source-file))
            (fprintf out "  - first-line: `~a`\n"
                     (truncate-line (hash-ref e 'first-line))))))
    #:exists 'truncate/replace))

(module+ main
  (define manifest-path default-manifest-path)
  (define json-out-path default-json-out-path)
  (define md-out-path default-md-out-path)

  (command-line
   #:program "report_external_spec_scope_unknowns.rkt"
   #:once-each
   [("--manifest") path "Manifest path"
                    (set! manifest-path (string->path path))]
   [("--json-out") path "JSON output path"
                    (set! json-out-path (string->path path))]
   [("--md-out") path "Markdown output path"
                  (set! md-out-path (string->path path))])

  (define report
    (build-report manifest-path))
  (write-json-report json-out-path report)
  (write-md-report md-out-path report json-out-path)

  (printf "Wrote JSON report: ~a\n" (path->string json-out-path))
  (printf "Wrote Markdown report: ~a\n" (path->string md-out-path))
  (printf "Unknown entries: ~a\n"
          (hash-ref (hash-ref report 'totals) 'unknown-entries)))
