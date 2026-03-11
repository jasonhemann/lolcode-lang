#lang racket/base

(require racket/port
         racket/runtime-path)

(provide read
         read-syntax
         get-info)

(define-runtime-path main-module-path
  "../main.rkt")

(define (read in)
  (syntax->datum (read-syntax #f in)))

(define (read-syntax src in)
  (define source-text (port->string in))
  (datum->syntax
   #f
   `(module lolcode-module racket/base
      (require (file ,(path->string main-module-path)))
      (provide run)
      (define source-text ,source-text)
      (define (run)
        (run-program (parse-program source-text)))
      (module+ main
        (run)))
   #f))

(define (get-info . _args)
  (lambda (_key default)
    default))
