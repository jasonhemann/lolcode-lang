#lang racket/base

(require "cli.rkt")

(exit (main (vector->list (current-command-line-arguments))))
