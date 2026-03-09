#lang racket/base

(require json
         racket/cmdline
         racket/file
         racket/format
         racket/list
         racket/match
         racket/path
         racket/runtime-path
         racket/string)

(define-runtime-path script-dir ".")
(define repo-root
  (simplify-path (build-path script-dir "..")))

(define manifest-path
  (build-path repo-root "tests" "regression-evidence" "external" "manifest.rktd"))
(define queue-path
  (build-path repo-root "corpus" "research" "external_issues" "candidate_repros_ranked.json"))
(define evidence-root
  (build-path repo-root "tests" "regression-evidence" "external"))

(define apply? #f)
(define move-fixtures? #t)
(define verbose? #f)

(command-line
 #:program "reconcile_external_manifest_waves.rkt"
 #:once-each
 [("--manifest")
  p
  "Path to evidence manifest.rktd."
  (set! manifest-path (string->path p))]
 [("--queue")
  p
  "Path to candidate_repros_ranked.json."
  (set! queue-path (string->path p))]
 [("--evidence-root")
  p
  "Path to tests/regression-evidence/external root."
  (set! evidence-root (string->path p))]
 [("--apply")
  "Apply updates in-place (otherwise dry-run)."
  (set! apply? #t)]
 [("--no-move-fixtures")
  "Do not move fixture files when source-file wave segment changes."
  (set! move-fixtures? #f)]
 [("--verbose")
  "Print per-entry reconciliation details."
  (set! verbose? #t)])

(define (die fmt . args)
  (error 'reconcile-external-manifest-waves (apply format fmt args)))

(define (wave-dir n)
  (if (< n 10)
      (format "wave_0~a" n)
      (format "wave_~a" n)))

(define (parens-delta line)
  (for/fold ([d 0]) ([ch (in-string line)])
    (+ d (cond
            [(char=? ch #\() 1]
            [(char=? ch #\)) -1]
            [else 0]))))

(define (block-id block-lines)
  (for/first ([line (in-list block-lines)]
              #:when (regexp-match? #px"^\\s*\\(id \\. \"[^\"]+\"\\)" line))
    (cadr (regexp-match #px"\\(id \\. \"([^\"]+)\"\\)" line))))

(define (rewrite-entry-block block-lines updates-by-id)
  (define id (block-id block-lines))
  (define upd (and id (hash-ref updates-by-id id #f)))
  (if (not upd)
      block-lines
      (for/list ([line (in-list block-lines)])
        (cond
          [(regexp-match #px"^(\\s*)\\(wave \\. [0-9]+\\)(.*)$" line)
           =>
           (lambda (m)
             (format "~a(wave . ~a)~a"
                     (list-ref m 1)
                     (hash-ref upd 'new-wave)
                     (list-ref m 2)))]
          [(regexp-match #px"^(\\s*)\\(source-file \\. \"[^\"]+\"\\)(.*)$" line)
           =>
           (lambda (m)
             (format "~a(source-file . \"~a\")~a"
                     (list-ref m 1)
                     (hash-ref upd 'new-source-file)
                     (list-ref m 2)))]
          [else
           line]))))

(define (rewrite-manifest-text text updates-by-id)
  (define lines (string-split text "\n" #:trim? #f))
  (define out-lines '())
  (define in-entry? #f)
  (define entry-lines '())
  (define depth 0)

  (define (flush-entry!)
    (set! out-lines
          (append out-lines
                  (rewrite-entry-block entry-lines updates-by-id)))
    (set! entry-lines '())
    (set! in-entry? #f)
    (set! depth 0))

  (for ([line (in-list lines)])
    (cond
      [in-entry?
       (set! entry-lines (append entry-lines (list line)))
       (set! depth (+ depth (parens-delta line)))
       (when (= depth 0)
         (flush-entry!))]
      [(regexp-match? #px"^\\s*#hasheq\\(" line)
       (set! in-entry? #t)
       (set! entry-lines (list line))
       (set! depth (parens-delta line))
       (when (= depth 0)
         (flush-entry!))]
      [else
       (set! out-lines (append out-lines (list line)))]))

  (when in-entry?
    (die "manifest parse ended while still inside entry block"))

  (string-join out-lines "\n"))

(define (relative-path-string p)
  (path->string (find-relative-path repo-root p)))

(unless (file-exists? manifest-path)
  (die "manifest not found: ~a" (relative-path-string manifest-path)))

(unless (file-exists? queue-path)
  (die "queue not found: ~a" (relative-path-string queue-path)))

(define manifest-cases
  (call-with-input-file manifest-path read))
(unless (list? manifest-cases)
  (die "manifest root must be a list"))

(define queue-items
  (call-with-input-file queue-path read-json))
(unless (list? queue-items)
  (die "queue root must be a JSON list"))

(define queue-wave-by-url
  (for/fold ([h (hash)]) ([it (in-list queue-items)])
    (define url (hash-ref it 'url #f))
    (define wave (hash-ref it 'wave #f))
    (cond
      [(and (string? url) (exact-integer? wave) (positive? wave))
       (if (hash-has-key? h url)
           h
           (hash-set h url wave))]
      [else
       h])))

(define updates '())
(define unchanged 0)
(define unmatched 0)

(for ([c (in-list manifest-cases)])
  (define id (hash-ref c 'id #f))
  (define url (hash-ref c 'source-url #f))
  (define old-wave (hash-ref c 'wave #f))
  (define source-file (hash-ref c 'source-file #f))
  (define maybe-new-wave
    (and (string? url)
         (hash-ref queue-wave-by-url url #f)))
  (cond
    [(and maybe-new-wave
          (exact-integer? old-wave)
          (not (= old-wave maybe-new-wave))
          (string? source-file))
     (define old-wave-dir (wave-dir old-wave))
     (define new-wave-dir (wave-dir maybe-new-wave))
     (define new-source-file
       (regexp-replace
        (pregexp (regexp-quote old-wave-dir))
        source-file
        new-wave-dir))
     (set! updates
           (cons (hash 'id id
                       'url url
                       'old-wave old-wave
                       'new-wave maybe-new-wave
                       'old-source-file source-file
                       'new-source-file new-source-file)
                 updates))]
    [maybe-new-wave
     (set! unchanged (+ unchanged 1))]
    [else
     (set! unmatched (+ unmatched 1))]))

(set! updates
      (sort updates string<? #:key (lambda (u) (hash-ref u 'id ""))))

(define updates-by-id
  (for/fold ([h (hash)]) ([u (in-list updates)])
    (hash-set h (hash-ref u 'id) u)))

(printf "manifest_entries=~a\n" (length manifest-cases))
(printf "queue_items=~a\n" (length queue-items))
(printf "queue_urls=~a\n" (hash-count queue-wave-by-url))
(printf "wave_drift_entries=~a\n" (length updates))
(printf "unmatched_manifest_entries=~a\n" unmatched)

(when (or verbose? (positive? (length updates)))
  (for ([u (in-list updates)])
    (printf "drift id=~a wave ~a -> ~a\n"
            (hash-ref u 'id)
            (hash-ref u 'old-wave)
            (hash-ref u 'new-wave))
    (when verbose?
      (printf "  source-file: ~a -> ~a\n"
              (hash-ref u 'old-source-file)
              (hash-ref u 'new-source-file)))))

(when apply?
  (define manifest-text
    (file->string manifest-path))
  (define rewritten
    (rewrite-manifest-text manifest-text updates-by-id))
  (call-with-output-file manifest-path
    (lambda (out)
      (display rewritten out))
    #:exists 'replace)

  (printf "manifest_updated=~a\n" (relative-path-string manifest-path))

  (when move-fixtures?
    (define moved 0)
    (define skipped-missing 0)
    (define skipped-existing 0)
    (for ([u (in-list updates)])
      (define old-rel (hash-ref u 'old-source-file))
      (define new-rel (hash-ref u 'new-source-file))
      (unless (string=? old-rel new-rel)
        (define old-abs (build-path evidence-root old-rel))
        (define new-abs (build-path evidence-root new-rel))
        (cond
          [(not (file-exists? old-abs))
           (set! skipped-missing (+ skipped-missing 1))
           (when verbose?
             (printf "skip-missing old fixture: ~a\n"
                     (relative-path-string old-abs)))]
          [(file-exists? new-abs)
           (set! skipped-existing (+ skipped-existing 1))
           (when verbose?
             (printf "skip-existing new fixture: ~a\n"
                     (relative-path-string new-abs)))]
          [else
           (make-directory* (path-only new-abs))
           (rename-file-or-directory old-abs new-abs)
           (set! moved (+ moved 1))
           (when verbose?
             (printf "moved fixture: ~a -> ~a\n"
                     (relative-path-string old-abs)
                     (relative-path-string new-abs)))])))
    (printf "fixtures_moved=~a\n" moved)
    (printf "fixtures_skip_missing=~a\n" skipped-missing)
    (printf "fixtures_skip_existing=~a\n" skipped-existing)))
