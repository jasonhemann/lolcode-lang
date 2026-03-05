#lang racket/base

(provide placeholder-start-char
         placeholder-end-char
         placeholder-start?
         placeholder-end?
         contains-placeholder-marker?)

;; Private-use markers to preserve real :{...} placeholders through lexing.
;; This lets escaped forms like "::{name}" remain literal text.
(define placeholder-start-char #\uE000)
(define placeholder-end-char #\uE001)

(define (placeholder-start? ch)
  (char=? ch placeholder-start-char))

(define (placeholder-end? ch)
  (char=? ch placeholder-end-char))

(define (contains-placeholder-marker? text)
  (for/or ([ch (in-string text)])
    (or (placeholder-start? ch)
        (placeholder-end? ch))))
