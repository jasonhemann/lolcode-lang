#lang racket/base

(require "../main.rkt"
         "../runtime.rkt")

(provide run-program/report
         run-source/report)

(define (run-program/report parsed)
  (unless (program? parsed)
    (raise-argument-error 'run-program/report "program?" parsed))
  (execute-program parsed implementation-phase))

(define (run-source/report source)
  (run-program/report (parse-program source)))
