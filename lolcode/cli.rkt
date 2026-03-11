#lang racket/base

(require racket/cmdline
         racket/file
         racket/path
         "main.rkt")

(provide main)

(define (run-path path)
  (define full-path
    (simplify-path (path->complete-path path)))
  (define base-dir
    (or (path-only full-path)
        (current-directory)))
  (parameterize ([current-directory base-dir])
    (run-program (parse-program (file->string full-path)))))

(define (main [argv (vector->list (current-command-line-arguments))])
  (define trace? #f)
  (define source-path #f)
  (with-handlers ([exn:fail?
                   (lambda (e)
                     (if trace?
                         (raise e)
                         (begin
                           (displayln (exn-message e) (current-error-port))
                           1)))])
    (parameterize ([current-command-line-arguments (list->vector argv)])
      (command-line
       #:program "lolcode"
       #:once-each
       [("--trace")
        "Print full Racket stack trace on failures."
        (set! trace? #t)]
       #:args (file)
       (set! source-path file)))
    (run-path source-path)
    0))

(module+ main
  (exit (main)))
