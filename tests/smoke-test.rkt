#lang racket/base

(require rackunit
         racket/file
         racket/path
         "../cli.rkt"
         "../src/lolcode/main.rkt"
         "../src/lolcode/internal/reporting.rkt")

(module+ test
  (check-eq? implementation-phase 'core-subset-v2)

  (define parsed
    (parse-program "HAI 1.3\nVISIBLE \"OH HAI\"\nKTHXBYE\n"))
  (check-true (program? parsed))

  (define out (open-output-string))
  (define result
    (parameterize ([current-output-port out])
      (run-program parsed)))
  (check-true (void? result))
  (check-equal? (get-output-string out) "OH HAI\n")

  (define report (run-program/report parsed))
  (check-eq? (hash-ref report 'status) 'ok)
  (check-equal? (hash-ref report 'stdout) "OH HAI\n")

  (check-exn exn:fail:contract?
             (lambda () (parse-program 42)))
  (check-exn exn:fail:contract?
             (lambda () (run-program "not-a-program")))

  (define here
    (or (current-load-relative-directory)
        (current-directory)))
  (define repo-root
    (simplify-path (build-path here "..")))
  (define tmp-dir (make-temporary-file "lolcode-lang-smoke~a" 'directory))
  (define lang-file (build-path tmp-dir "sample.rkt"))
  (call-with-output-file lang-file
    #:exists 'truncate/replace
    (lambda (out)
      (display "#lang lolcode\nHAI 1.3\nVISIBLE \"LANG\"\nKTHXBYE\n" out)))
  (define local-collects-root
    (build-path tmp-dir "collects"))
  (make-directory local-collects-root)
  (make-file-or-directory-link repo-root
                               (build-path local-collects-root "lolcode"))

  (define with-local-collection
    (lambda (thunk)
      (parameterize ([current-library-collection-paths
                      (cons local-collects-root
                            (current-library-collection-paths))])
        (thunk))))

  (define run-proc
    (with-local-collection
     (lambda ()
       (dynamic-require lang-file 'run))))
  (check-true (procedure? run-proc))

  (define run-out (open-output-string))
  (parameterize ([current-output-port run-out])
    (run-proc))
  (check-equal? (get-output-string run-out) "LANG\n")

  (define main-out (open-output-string))
  (parameterize ([current-output-port main-out])
    (with-local-collection
     (lambda ()
       (dynamic-require `(submod ,lang-file main) #f))))
  (check-equal? (get-output-string main-out) "LANG\n")

  (define lol-file
    (build-path tmp-dir "sample.lol"))
  (call-with-output-file lol-file
    #:exists 'truncate/replace
    (lambda (out)
      (display "HAI 1.3\nVISIBLE \"CLI\"\nKTHXBYE\n" out)))
  (define cli-ok-out (open-output-string))
  (check-equal?
   (parameterize ([current-output-port cli-ok-out])
     (main (list (path->string lol-file))))
   0)
  (check-equal? (get-output-string cli-ok-out) "CLI\n")

  (define cli-bad-file
    (build-path tmp-dir "bad-input.rkt"))
  (call-with-output-file cli-bad-file
    #:exists 'truncate/replace
    (lambda (out)
      (display "#lang racket/base\n(displayln \"nope\")\n" out)))
  (define cli-bad-err (open-output-string))
  (check-equal?
   (parameterize ([current-error-port cli-bad-err])
     (main (list (path->string cli-bad-file))))
   1)
  (check-true
   (regexp-match? #px"program must begin with HAI opener"
                  (get-output-string cli-bad-err)))

  (delete-directory/files tmp-dir))
