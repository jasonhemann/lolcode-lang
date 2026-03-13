#lang racket/base

(require json
         racket/cmdline
         racket/file
         racket/list
         racket/path
         racket/string
         racket/format)

(define report-json #f)
(define src-root #f)
(define dst-root #f)
(define manifest-out #f)

(command-line
 #:program "header_salvage_experiment.rkt"
 #:args (report src dst manifest)
 (set! report-json (string->path report))
 (set! src-root (string->path src))
 (set! dst-root (string->path dst))
 (set! manifest-out (string->path manifest)))

(define report
  (call-with-input-file report-json read-json))
(define rows (hash-ref report 'rows '()))

(define (target-msg? msg)
  (and (string? msg)
       (or (string-contains? msg "program must begin with HAI opener")
           (string-contains? msg "unexpected NEWLINE at line 1, col 4")
           (string-contains? msg "unexpected NEWLINE at line 1, col 5"))))

(define (candidate? row)
  (and (equal? (hash-ref row 'classification #f) "likely-program")
       (equal? (hash-ref row 'outcome #f) "parse-error")
       (target-msg? (hash-ref row 'message #f))))

(define candidates (filter candidate? rows))

(define hai-line-rx #px"(?i:^\\s*HAI\\b)")
(define bare-hai-line-rx #px"(?i:^([ \t]*)HAI[ \t]*$)")
(define hai-version-line-rx #px"(?i:^([ \t]*)HAI[ \t]+([^ \t]+).*$)")
(define version-only-rx #px"^\\s*([0-9]+(?:\\.[0-9]+)?)\\s*$")

(define (find-first-hai-index lines)
  (let loop ([i 0])
    (cond
      [(>= i (length lines)) #f]
      [(regexp-match? hai-line-rx (list-ref lines i)) i]
      [else (loop (add1 i))])))

(define (normalize-header lines)
  (cond
    [(null? lines) (values lines '())]
    [else
     (define line0 (car lines))
     (define actions '())
     (define new-lines lines)
     (cond
       [(regexp-match bare-hai-line-rx line0)
        => (lambda (m)
             (define indent (list-ref m 1))
             (if (and (pair? (cdr lines))
                      (regexp-match version-only-rx (cadr lines)))
                 (begin
                   (set! new-lines (cons (string-append indent "HAI 1.3") (cddr lines)))
                   (set! actions (cons "merge-hai-line2-version-to-1.3" actions)))
                 (begin
                   (set! new-lines (cons (string-append indent "HAI 1.3") (cdr lines)))
                   (set! actions (cons "promote-bare-hai-to-1.3" actions)))))]
       [(regexp-match hai-version-line-rx line0)
        => (lambda (m)
             (define indent (list-ref m 1))
             (define ver (string-downcase (list-ref m 2)))
             (unless (string=? ver "1.3")
               (set! new-lines (cons (string-append indent "HAI 1.3") (cdr lines)))
               (set! actions (cons (format "rewrite-version-~a-to-1.3" ver) actions))))]
       [else (void)])
     (values new-lines (reverse actions))]))

(define modified-count 0)
(define skipped-nohai 0)
(define rows-out '())

(for ([row (in-list candidates)])
  (define rel (hash-ref row 'path))
  (define src-file (build-path rel))
  (define dest-file
    (build-path dst-root
                (find-relative-path src-root src-file)))
  (define msg (hash-ref row 'message ""))

  (if (not (file-exists? dest-file))
      (set! rows-out
            (cons (list rel "missing-in-dst" msg "") rows-out))
      (let* ([source (file->string dest-file)]
             [lines (regexp-split #rx"\r\n|\n|\r" source)]
             [hai-idx (find-first-hai-index lines)]
             [work-lines lines]
             [actions '()])
        (when (and (string-contains? msg "program must begin with HAI opener")
                   hai-idx
                   (> hai-idx 0))
          (set! work-lines (drop lines hai-idx))
          (set! actions (append actions (list (format "trim-prefix-before-hai-~a-lines" hai-idx)))))

        (define-values (normalized-lines hdr-actions)
          (normalize-header work-lines))
        (set! actions (append actions hdr-actions))

        (cond
          [(or (not hai-idx) (null? actions))
           (when (not hai-idx) (set! skipped-nohai (add1 skipped-nohai)))
           (set! rows-out
                 (cons (list rel "no-change" msg (string-join actions ";")) rows-out))]
          [else
           (set! modified-count (add1 modified-count))
           (call-with-output-file dest-file
             (lambda (out)
               (display (string-join normalized-lines "\n") out))
             #:exists 'replace)
           (set! rows-out
                 (cons (list rel "modified" msg (string-join actions ";")) rows-out))]))))

(make-directory* (path-only manifest-out))
(call-with-output-file manifest-out
  (lambda (out)
    (display "path\tstatus\toriginal_message\tactions\n" out)
    (for ([r (in-list (reverse rows-out))])
      (display (string-join r "\t") out)
      (newline out)))
  #:exists 'replace)

(printf "candidates=~a modified=~a skipped_no_hai=~a manifest=~a\n"
        (length candidates) modified-count skipped-nohai (path->string manifest-out))
