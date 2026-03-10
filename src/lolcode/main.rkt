#lang racket/base

(require racket/file
         racket/path
         "ast.rkt"
         "parser.rkt"
         "runtime.rkt")

(provide implementation-phase
         program
         program?
         program-version
         program-statements
         parse-program
         run-program
         run-file)

;; Phase marker so tests can assert the current implementation slice.
(define implementation-phase 'core-subset-v2)

(define (parse-program source)
  (unless (string? source)
    (raise-argument-error 'parse-program "string?" source))
  (parse-source source))

(define (run-program parsed)
  (unless (program? parsed)
    (raise-argument-error 'run-program "program?" parsed))
  (execute-program parsed implementation-phase))

(define (run-file path)
  (unless (path-string? path)
    (raise-argument-error 'run-file "path-string?" path))
  (define full-path (simplify-path (path->complete-path path)))
  (define base-dir (or (path-only full-path) (current-directory)))
  (parameterize ([current-directory base-dir])
    (run-program (parse-program (file->string full-path)))))
