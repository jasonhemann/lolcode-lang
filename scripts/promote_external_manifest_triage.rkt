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
  "../corpus/research/external-evidence-triage-promotion.json")
(define-runtime-path default-md-out-path
  "../corpus/research/EXTERNAL_EVIDENCE_TRIAGE_PROMOTION.md")

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

(define (line-id line)
  (define m
    (regexp-match #px"^\\s*\\(id \\. \"([^\"]+)\"\\)" line))
  (and m (list-ref m 1)))

(define (line-triage line)
  (define m
    (regexp-match #px"^(\\s*\\(triage-status \\. )\"([^\"]+)\"(\\).*)$" line))
  (and m
       (hash 'prefix (list-ref m 1)
             'value (list-ref m 2)
             'suffix (list-ref m 3))))

(define (promotion-target row)
  (define triage (~a (hash-ref row 'triage-status "")))
  (define assessment (~a (hash-ref row 'assessment "")))
  (cond
    [(and (string=? triage "candidate")
          (string=? assessment "supports"))
     "reproducer-ready"]
    [else #f]))

(define (build-promotion-index rows)
  (for/hash ([r (in-list rows)]
             #:when (promotion-target r))
    (values (hash-ref r 'id)
            (promotion-target r))))

(define (update-manifest-lines lines promotions overwrite?)
  (define current-id #f)
  (define changed '())
  (define updated-lines
    (for/list ([line (in-list lines)])
      (define maybe-id (line-id line))
      (when maybe-id
        (set! current-id maybe-id))
      (define maybe-t (line-triage line))
      (if (and maybe-t
               current-id
               (hash-has-key? promotions current-id))
          (let* ([existing (hash-ref maybe-t 'value)]
                 [replacement (hash-ref promotions current-id)])
            (cond
              [(and (not overwrite?)
                    (not (string=? existing "candidate")))
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
                (hash-ref maybe-t 'prefix)
                "\""
                replacement
                "\""
                (hash-ref maybe-t 'suffix))]))
          line)))
  (values updated-lines (reverse changed)))

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
      (fprintf out "# External Evidence Triage Promotion\n\n")
      (fprintf out "Generated: `~a`\n\n" (hash-ref report 'generated-at))
      (fprintf out "- JSON report: `~a`\n\n" (path->string json-path))

      (fprintf out "## Summary\n\n")
      (fprintf out "- Cases evaluated: `~a`\n"
               (hash-ref (hash-ref report 'totals) 'cases-evaluated))
      (fprintf out "- Promotions suggested: `~a`\n"
               (hash-ref (hash-ref report 'totals) 'promotions-suggested))
      (fprintf out "- Manifest entries updated: `~a`\n"
               (hash-ref (hash-ref report 'totals) 'entries-updated))
      (fprintf out "- Apply mode: `~a`\n\n"
               (if (hash-ref report 'applied?) "true" "false"))

      (fprintf out "## Assessment Counts\n\n")
      (for ([row (in-list (hash-ref report 'assessment-counts))])
        (fprintf out "- `~a`: `~a`\n"
                 (hash-ref row 'label)
                 (hash-ref row 'count)))

      (fprintf out "\n## Promotion Changes (sample)\n\n")
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
   #:program "promote_external_manifest_triage.rkt"
   #:once-each
   [("--manifest") path "Manifest path"
                    (set! manifest-path (string->path path))]
   [("--json-out") path "JSON report path"
                    (set! json-out-path (string->path path))]
   [("--md-out") path "Markdown report path"
                  (set! md-out-path (string->path path))]
   [("--apply") "Write triage updates into manifest file"
                (set! apply? #t)]
   [("--overwrite-existing") "Also replace non-candidate triage-status values"
                             (set! overwrite? #t)])

  (define rows
    (evaluate-evidence-cases manifest-path #f #f))
  (define promotions
    (build-promotion-index rows))

  (define assessment-counts-h
    (for/fold ([acc (hash)]) ([r (in-list rows)])
      (hash-inc acc (hash-ref r 'assessment "unknown"))))

  (define manifest-lines
    (file->lines manifest-path))
  (define-values (updated-lines changes)
    (update-manifest-lines manifest-lines promotions overwrite?))

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
          'totals (hash 'cases-evaluated (length rows)
                       'promotions-suggested (hash-count promotions)
                       'entries-updated (length changes))
          'assessment-counts (counts->rows assessment-counts-h)
          'changes changes))

  (write-json-report json-out-path report)
  (write-md-report md-out-path report json-out-path)

  (printf "Wrote JSON report: ~a\n" (path->string json-out-path))
  (printf "Wrote Markdown report: ~a\n" (path->string md-out-path))
  (printf "Cases evaluated: ~a\n" (length rows))
  (printf "Promotions suggested: ~a\n" (hash-count promotions))
  (printf "Manifest entries updated: ~a\n" (length changes))
  (printf "Applied: ~a\n" (if apply? "yes" "no")))

