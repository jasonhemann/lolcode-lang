#lang racket/base

(require json
         racket/file
         racket/list
         racket/match
         racket/path
         racket/string
         racket/format)

(define-values (report-json src-root dst-root manifest-out)
  (match (vector->list (current-command-line-arguments))
    [(list report src dst manifest)
     (values (string->path report)
             (string->path src)
             (string->path dst)
             (string->path manifest))]
    [_ (error 'header_salvage_experiment
              "expected arguments: <report-json> <src-root> <dst-root> <manifest-out>")]))

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

(define (find-first-hai-index lines [i 0])
  (cond
    [(>= i (length lines)) #f]
    [(regexp-match? hai-line-rx (list-ref lines i)) i]
    [else (find-first-hai-index lines (add1 i))]))

(define (normalize-header lines)
  (cond
    [(null? lines) (values lines '())]
    [else
     (define line0 (car lines))
     (cond
       [(regexp-match bare-hai-line-rx line0)
        => (lambda (m)
             (define indent (list-ref m 1))
             (if (and (pair? (cdr lines))
                      (regexp-match version-only-rx (cadr lines)))
                 (values (cons (string-append indent "HAI 1.3") (cddr lines))
                         '("merge-hai-line2-version-to-1.3"))
                 (values (cons (string-append indent "HAI 1.3") (cdr lines))
                         '("promote-bare-hai-to-1.3"))))]
       [(regexp-match hai-version-line-rx line0)
        => (lambda (m)
             (define indent (list-ref m 1))
             (define ver (string-downcase (list-ref m 2)))
             (if (string=? ver "1.3")
                 (values lines '())
                 (values (cons (string-append indent "HAI 1.3") (cdr lines))
                         (list (format "rewrite-version-~a-to-1.3" ver)))))]
       [else (values lines '())]))]))

(define-values (modified-count skipped-nohai rows-out)
  (for/fold ([modified-count 0]
             [skipped-nohai 0]
             [rows-out '()])
            ([row (in-list candidates)])
    (define rel (hash-ref row 'path))
    (define src-file (build-path rel))
    (define dest-file
      (build-path dst-root
                  (find-relative-path src-root src-file)))
    (define msg (hash-ref row 'message ""))

    (if (file-exists? dest-file)
        (let* ([source (file->string dest-file)]
               [lines (regexp-split #rx"\r\n|\n|\r" source)]
               [hai-idx (find-first-hai-index lines)])
          (define-values (work-lines prefix-actions)
            (if (and (string-contains? msg "program must begin with HAI opener")
                     hai-idx
                     (> hai-idx 0))
                (values (drop lines hai-idx)
                        (list (format "trim-prefix-before-hai-~a-lines"
                                      hai-idx)))
                (values lines '())))
          (define-values (normalized-lines hdr-actions)
            (normalize-header work-lines))
          (define actions
            (append prefix-actions hdr-actions))
          (cond
            [(or (not hai-idx) (null? actions))
             (values modified-count
                     (if hai-idx
                         skipped-nohai
                         (add1 skipped-nohai))
                     (cons (list rel "no-change" msg (string-join actions ";"))
                           rows-out))]
            [else
             (call-with-output-file dest-file
               (lambda (out)
                 (display (string-join normalized-lines "\n") out))
               #:exists 'replace)
             (values (add1 modified-count)
                     skipped-nohai
                     (cons (list rel "modified" msg (string-join actions ";"))
                           rows-out))]))
        (values modified-count
                skipped-nohai
                (cons (list rel "missing-in-dst" msg "") rows-out)))))

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
