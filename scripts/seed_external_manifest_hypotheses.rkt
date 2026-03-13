#lang racket/base

(require racket/cmdline
         racket/date
         racket/file
         racket/format
         racket/list
         racket/path
         racket/runtime-path
         racket/string
         "./external_evidence_common.rkt"
         "../tests/regression-evidence/external/run-evidence.rkt")

(define-runtime-path default-manifest-path
  "../tests/regression-evidence/external/manifest.rktd")
(define-runtime-path default-json-out-path
  "../corpus/research/external-evidence-hypothesis-seed.json")
(define-runtime-path default-md-out-path
  "../corpus/research/EXTERNAL_EVIDENCE_HYPOTHESIS_SEED.md")

(define (inferred-hypothesis observed-status)
  (cond
    [(string=? observed-status "ok") "expects-pass"]
    [(string=? observed-status "parse-error") "expects-parse-error"]
    [(string=? observed-status "runtime-error") "expects-runtime-error"]
    [else #f]))

(define (build-suggestion-index rows)
  (for/hash ([r (in-list rows)]
             #:when (inferred-hypothesis (~a (hash-ref r 'observed-status ""))))
    (values (hash-ref r 'id)
            (inferred-hypothesis (~a (hash-ref r 'observed-status ""))))))

(define (line-hypothesis line)
  (define m
    (regexp-match #px"^(\\s*\\(hypothesis \\. )\"([^\"]+)\"(\\).*)$" line))
  (and m
       (hash 'prefix (list-ref m 1)
             'value (list-ref m 2)
             'suffix (list-ref m 3))))

(define (update-manifest-lines lines suggestions overwrite?)
  (define current-id #f)
  (define changed '())
  (define updated-lines
    (for/list ([line (in-list lines)])
      (define maybe-id (manifest-line-id line))
      (when maybe-id
        (set! current-id maybe-id))
      (define maybe-h (line-hypothesis line))
      (if (and maybe-h
               current-id
               (hash-has-key? suggestions current-id))
          (let* ([existing (hash-ref maybe-h 'value)]
                 [replacement (hash-ref suggestions current-id)])
            (cond
              [(and (not overwrite?)
                    (not (string=? existing "unknown")))
               line]
              [(string=? existing replacement)
               line]
              [else
               (set! changed
                     (cons (hash 'id current-id
                                 'old existing
                                 'new replacement)
                           changed))
               (string-append
                (hash-ref maybe-h 'prefix)
                "\""
                replacement
                "\""
                (hash-ref maybe-h 'suffix))]))
          line)))
  (values updated-lines (reverse changed)))

(define (write-md-report path report json-path)
  (make-directory* (or (path-only path) (current-directory)))
  (call-with-output-file path
    (lambda (out)
      (fprintf out "# External Evidence Hypothesis Seeding\n\n")
      (fprintf out "Generated: `~a`\n\n" (hash-ref report 'generated-at))
      (fprintf out "- JSON report: `~a`\n\n" (path->string json-path))
      (fprintf out "## Summary\n\n")
      (fprintf out "- Cases evaluated: `~a`\n"
               (hash-ref (hash-ref report 'totals) 'cases-evaluated))
      (fprintf out "- Suggestions generated: `~a`\n"
               (hash-ref (hash-ref report 'totals) 'suggestions-generated))
      (fprintf out "- Manifest entries updated: `~a`\n"
               (hash-ref (hash-ref report 'totals) 'entries-updated))
      (fprintf out "- Apply mode: `~a`\n\n"
               (if (hash-ref report 'applied?) "true" "false"))

      (fprintf out "## Suggested Hypothesis Counts\n\n")
      (for ([row (in-list (hash-ref report 'suggestion-counts))])
        (fprintf out "- `~a`: `~a`\n"
                 (hash-ref row 'label)
                 (hash-ref row 'count)))

      (fprintf out "\n## Updated Entries (sample)\n\n")
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
   #:program "seed_external_manifest_hypotheses.rkt"
   #:once-each
   [("--manifest") path "Manifest path"
                    (set! manifest-path (string->path path))]
   [("--json-out") path "JSON report path"
                    (set! json-out-path (string->path path))]
   [("--md-out") path "Markdown report path"
                  (set! md-out-path (string->path path))]
   [("--apply") "Write updates into manifest file"
                (set! apply? #t)]
   [("--overwrite-existing") "Also replace non-unknown hypotheses"
                             (set! overwrite? #t)])

  (define rows
    (evaluate-evidence-cases manifest-path #f #f))
  (define suggestions
    (build-suggestion-index rows))
  (define manifest-lines
    (file->lines manifest-path))
  (define-values (updated-lines changes)
    (update-manifest-lines manifest-lines suggestions overwrite?))

  (when apply?
    (call-with-output-file manifest-path
      (lambda (out)
        (for ([line (in-list updated-lines)])
          (displayln line out)))
      #:exists 'truncate/replace))

  (define suggestion-counts-h
    (for/fold ([acc (hash)]) ([v (in-hash-values suggestions)])
      (hash-inc acc v)))

  (define report
    (hash 'generated-at (date->string (current-date) #t)
          'manifest-path (path->string manifest-path)
          'applied? apply?
          'overwrite-existing? overwrite?
          'totals (hash 'cases-evaluated (length rows)
                       'suggestions-generated (hash-count suggestions)
                       'entries-updated (length changes))
          'suggestion-counts (counts->rows suggestion-counts-h)
          'changes changes))

  (write-json-report json-out-path report)
  (write-md-report md-out-path report json-out-path)

  (printf "Wrote JSON report: ~a\n" (path->string json-out-path))
  (printf "Wrote Markdown report: ~a\n" (path->string md-out-path))
  (printf "Cases evaluated: ~a\n" (length rows))
  (printf "Suggestions generated: ~a\n" (hash-count suggestions))
  (printf "Manifest entries updated: ~a\n" (length changes))
  (printf "Applied: ~a\n" (if apply? "yes" "no")))
