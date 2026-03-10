#lang racket/base

(require json
         racket/cmdline
         racket/date
         racket/file
         racket/format
         racket/list
         racket/match
         racket/path
         racket/runtime-path
         racket/string
         "../src/lolcode/lexer.rkt"
         "../src/lolcode/main.rkt")

(define-runtime-path script-dir ".")
(define repo-root
  (simplify-path (build-path script-dir "..")))

(define corpus-root
  (build-path repo-root "corpus" "tier2"))
(define json-out
  (build-path repo-root "corpus" "research" "tier2-eval-classified.json"))
(define md-out
  (build-path repo-root "corpus" "research" "tier2-eval-classified.md"))
(define timeout-seconds 2.0)

(command-line
 #:program "eval_tier2_corpus.rkt"
 #:once-each
 [("--corpus-root")
  dir
  "Tier corpus root directory to scan recursively for .lol files."
  (set! corpus-root (string->path dir))]
 [("--json-out")
  p
  "Output JSON report path."
  (set! json-out (string->path p))]
 [("--md-out")
  p
  "Output Markdown summary path."
  (set! md-out (string->path p))]
 [("--timeout-seconds")
  s
  "Per-program evaluation timeout in seconds (default: 2.0)."
  (set! timeout-seconds (string->number s))])

(unless (and (real? timeout-seconds) (> timeout-seconds 0))
  (error 'eval-tier2-corpus "--timeout-seconds must be a positive real number"))

(define (path->display p)
  (path->string (find-relative-path repo-root p)))

(define (lol-file? p)
  (and (file-exists? p)
       (regexp-match? #px"(?i:\\.lol)$" (path->string p))))

(define (collect-lol-files root)
  (sort
   (for/list ([p (in-directory root)]
              #:when (lol-file? p))
     p)
   string<?
   #:key path->string))

(define (first-meaningful-line source)
  (define lines (regexp-split #px"\r\n|\n|\r" source))
  (let loop ([ls lines] [in-block-comment? #f])
    (cond
      [(null? ls) #f]
      [else
       (define line (string-trim (car ls)))
       (cond
         [in-block-comment?
          (if (regexp-match? #px"(?i:\\bTLDR\\b)" line)
              (loop (cdr ls) #f)
              (loop (cdr ls) #t))]
         [(string=? line "")
          (loop (cdr ls) #f)]
         [(regexp-match? #px"^#!" line)
          (loop (cdr ls) #f)]
         [(regexp-match? #px"(?i:^OBTW\\b)" line)
          (if (regexp-match? #px"(?i:\\bTLDR\\b)" line)
              (loop (cdr ls) #f)
              (loop (cdr ls) #t))]
         [(regexp-match? #px"(?i:^BTW\\b)" line)
          (loop (cdr ls) #f)]
         [else line])])))

(define leading-hai-re
  #px"(?i:^HAI(?:\\s+[0-9]+(?:\\.[0-9]+)?)?\\b)")

(define any-hai-re
  #px"(?mi:^\\s*HAI(?:\\s+[0-9]+(?:\\.[0-9]+)?)?\\b)")

(define (classify-source source)
  (define first-line (first-meaningful-line source))
  (cond
    [(not first-line)
     (values "non-program" "empty-or-comments-only" #f)]
    [(regexp-match? leading-hai-re first-line)
     (values "likely-program" "leading-hai" first-line)]
    [(regexp-match? any-hai-re source)
     (values "likely-program" "hai-found-not-leading" first-line)]
    [else
     (values "non-program" "no-hai-header" first-line)]))

(define (with-timeout timeout thunk)
  (define ch (make-channel))
  (define worker
    (thread
     (lambda ()
       (channel-put
        ch
        (with-handlers ([exn:fail? (lambda (e) (list 'raised (exn-message e)))])
          (list 'ok (thunk)))))))
  (define result (sync/timeout timeout ch))
  (if result
      result
      (begin
        (kill-thread worker)
        '(timeout))))

(define (truncate-text s [n 160])
  (if (and (string? s) (> (string-length s) n))
      (string-append (substring s 0 n) "...")
      s))

(define (normalize-message msg)
  (if (and (string? msg) (not (string=? (string-trim msg) "")))
      (truncate-text (car (string-split (string-trim msg) "\n")))
      #f))

(define (run-one path)
  (define rel (path->display path))
  (define source (file->string path))
  (define-values (classification classification-reason first-line)
    (classify-source source))

  (define base
    (hash 'path rel
          'classification classification
          'classification-reason classification-reason
          'first-meaningful-line (and first-line (truncate-text first-line 120))))

  (if (not (string=? classification "likely-program"))
      (hash-set* base
                 'outcome "non-program"
                 'lex-status "skipped"
                 'parse-status "skipped"
                 'eval-status "skipped")
      (with-handlers ([exn:fail?
                       (lambda (e)
                         (hash-set* base
                                    'outcome "lex-error"
                                    'lex-status "lex-error"
                                    'parse-status "skipped"
                                    'eval-status "skipped"
                                    'message (exn-message e)))])
        (define tokens (lex-source source))
        (define parse-or-error
          (with-handlers ([exn:fail? (lambda (e) (list 'parse-error (exn-message e)))])
            (list 'parse-ok (parse-program source))))
        (match parse-or-error
          [(list 'parse-error msg)
           (hash-set* base
                      'outcome "parse-error"
                      'lex-status "lex-ok"
                      'token-count (length tokens)
                      'parse-status "parse-error"
                      'eval-status "skipped"
                      'message msg)]
          [(list 'parse-ok parsed)
           (define eval-result
             (with-timeout timeout-seconds (lambda () (run-program parsed))))
           (match eval-result
             ['(timeout)
              (hash-set* base
                         'outcome "timeout"
                         'lex-status "lex-ok"
                         'token-count (length tokens)
                         'parse-status "parse-ok"
                         'eval-status "timeout"
                         'message (format "evaluation timed out after ~a seconds" timeout-seconds))]
             [(list 'raised msg)
              (hash-set* base
                         'outcome "runtime-exn"
                         'lex-status "lex-ok"
                         'token-count (length tokens)
                         'parse-status "parse-ok"
                         'eval-status "runtime-exn"
                         'message msg)]
             [(list 'ok result)
              (define status
                (hash-ref result 'status 'unknown))
              (define status-text
                (case status
                  [(ok) "ok"]
                  [(runtime-error) "runtime-error"]
                  [(unsupported) "unsupported"]
                  [else (~a status)]))
              (define stdout-text
                (hash-ref result 'stdout ""))
              (define msg
                (cond
                  [(hash-has-key? result 'error) (hash-ref result 'error)]
                  [(hash-has-key? result 'reason) (hash-ref result 'reason)]
                  [else #f]))
              (hash-set* base
                         'outcome status-text
                         'lex-status "lex-ok"
                         'token-count (length tokens)
                         'parse-status "parse-ok"
                         'eval-status status-text
                         'stdout-bytes (string-length stdout-text)
                         'stdout-preview (truncate-text stdout-text 120)
                         'message msg)])]))))

(define (count-by rows key)
  (for/fold ([acc (hash)]) ([r (in-list rows)])
    (define v (hash-ref r key "unknown"))
    (hash-set acc v (+ 1 (hash-ref acc v 0)))))

(define (message-counts rows)
  (for/fold ([acc (hash)]) ([r (in-list rows)])
    (define msg (normalize-message (hash-ref r 'message #f)))
    (if msg
        (hash-set acc msg (+ 1 (hash-ref acc msg 0)))
        acc)))

(define (hash->sorted-pairs h)
  (sort (hash->list h) > #:key cdr))

(define (counts->rows h)
  (for/list ([kv (in-list (hash->sorted-pairs h))])
    (hash 'label (car kv)
          'count (cdr kv))))

(define (print-count-block out title h)
  (fprintf out "### ~a\n\n" title)
  (if (zero? (hash-count h))
      (fprintf out "- (none)\n\n")
      (begin
        (for ([kv (in-list (hash->sorted-pairs h))])
          (fprintf out "- `~a`: `~a`\n" (car kv) (cdr kv)))
        (newline out))))

(define (top-error-rows rows n)
  (define errs
    (filter (lambda (r)
              (member (hash-ref r 'outcome "")
                      '("lex-error" "parse-error" "runtime-error" "runtime-exn" "timeout" "unsupported")))
            rows))
  (take errs (min n (length errs))))

(define files
  (collect-lol-files corpus-root))

(define rows
  (for/list ([p (in-list files)])
    (run-one p)))

(define likely-program-rows
  (filter (lambda (r)
            (string=? (hash-ref r 'classification) "likely-program"))
          rows))

(define classification-counts-h
  (count-by rows 'classification-reason))

(define outcome-counts-all-h
  (count-by rows 'outcome))

(define outcome-counts-likely-h
  (count-by likely-program-rows 'outcome))

(define message-counts-likely-h
  (message-counts likely-program-rows))

(define summary
  (hash 'generated-at (date->string (current-date) #t)
        'corpus-root (path->display corpus-root)
        'timeout-seconds timeout-seconds
        'totals (hash 'files (length rows)
                      'likely-programs (length likely-program-rows)
                      'non-programs (- (length rows) (length likely-program-rows)))
        'classification-counts (counts->rows classification-counts-h)
        'outcome-counts-all (counts->rows outcome-counts-all-h)
        'outcome-counts-likely-programs (counts->rows outcome-counts-likely-h)
        'message-counts-likely-programs (counts->rows message-counts-likely-h)))

(define report-json
  (hash 'summary summary
        'rows rows))

(make-directory* (path-only json-out))
(make-directory* (path-only md-out))

(call-with-output-file json-out
  (lambda (out)
    (write-json report-json out))
  #:exists 'replace)

(call-with-output-file md-out
  (lambda (out)
    (fprintf out "# Tier2 Classified Eval Snapshot\n\n")
    (fprintf out "Generated: `~a`\n\n" (hash-ref summary 'generated-at))
    (fprintf out "- JSON source: `~a`\n\n" (path->display json-out))
    (fprintf out "- Corpus root: `~a`\n" (hash-ref summary 'corpus-root))
    (fprintf out "- Timeout seconds: `~a`\n\n" timeout-seconds)
    (fprintf out "## Totals\n\n")
    (define totals (hash-ref summary 'totals))
    (fprintf out "- Files: `~a`\n" (hash-ref totals 'files))
    (fprintf out "- Likely programs: `~a`\n" (hash-ref totals 'likely-programs))
    (fprintf out "- Non-programs: `~a`\n\n" (hash-ref totals 'non-programs))
    (print-count-block out "Classification Reasons" classification-counts-h)
    (print-count-block out "Outcome Counts (All Files)" outcome-counts-all-h)
    (print-count-block out "Outcome Counts (Likely Programs)" outcome-counts-likely-h)
    (print-count-block out "Top Messages (Likely Programs)" message-counts-likely-h)
    (fprintf out "## Sample Error Rows\n\n")
    (for ([r (in-list (top-error-rows rows 20))])
      (fprintf out "- `~a` => `~a` (`~a`)\n"
               (hash-ref r 'path)
               (hash-ref r 'outcome)
               (or (normalize-message (hash-ref r 'message #f)) "no message")))
    (newline out))
  #:exists 'replace)

(printf "Wrote JSON report: ~a\n" (path->display json-out))
(printf "Wrote Markdown summary: ~a\n" (path->display md-out))
(printf "Totals: files=~a likely-programs=~a non-programs=~a\n"
        (hash-ref (hash-ref summary 'totals) 'files)
        (hash-ref (hash-ref summary 'totals) 'likely-programs)
        (hash-ref (hash-ref summary 'totals) 'non-programs))
