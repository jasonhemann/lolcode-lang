#lang info

(define collection "lolcode")

(define pkg-desc
  "Strict LOLCODE 1.3 parser/runtime with CLI and #lang integration.")

(define version "0.1")
(define pkg-authors '("jhemann"))

(define deps
  '("base"
    "codepoint"))

(define build-deps
  '("rackunit-lib"))

(define raco-commands
  '(("lolcode" "raco.rkt" "run LOLCODE 1.3 source files" #f)))

(define racket-launcher-names
  '("lolcode"))

(define racket-launcher-libraries
  '("cmd.rkt"))
