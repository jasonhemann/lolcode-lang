#lang racket/base

(require racket/file
         "ast.rkt"
         "parser.rkt")

(provide implementation-phase
         program
         program?
         program-version
         program-statements
         parse-program
         run-program
         run-file)

;; Step 1 bootstrap marker so tests can assert the current project phase.
(define implementation-phase 'bootstrap)

(define (parse-program source)
  (unless (string? source)
    (raise-argument-error 'parse-program "string?" source))
  (parse-source source))

(define (run-program parsed)
  (unless (program? parsed)
    (raise-argument-error 'run-program "program?" parsed))
  (hash 'status 'not-implemented
        'phase implementation-phase))

(define (run-file path)
  (unless (path-string? path)
    (raise-argument-error 'run-file "path-string?" path))
  (run-program (parse-program (file->string path))))
