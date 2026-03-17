#lang racket/base

(require json
         racket/file
         racket/path
         "traceability_clause_spans_lib.rkt"
         "validation_rules_lib.rkt")

(define option-specs
  (list (hasheq 'flag "--graph"
                'key 'graph-path
                'mode 'value
                'convert string->path)
        (hasheq 'flag "--spec"
                'key 'spec-path
                'mode 'value
                'convert string->path)
        (hasheq 'flag "--out"
                'key 'out-path
                'mode 'value
                'convert string->path)))

(define option-defaults
  (hasheq 'graph-path default-traceability-graph-path
          'spec-path default-spec-path
          'out-path default-clause-spans-path))

(define opts
  (parse-cli-options 'build_traceability_clause_spans
                     (vector->list (current-command-line-arguments))
                     option-specs
                     option-defaults))

(define graph-path (hash-ref opts 'graph-path))
(define spec-path (hash-ref opts 'spec-path))
(define out-path (hash-ref opts 'out-path))

(define spans
  (validate-traceability-clause-spans
   (build-traceability-clause-spans graph-path spec-path)
   graph-path
   spec-path))

(make-directory* (path-only out-path))
(call-with-output-file out-path
  (lambda (out)
    (write-json spans out))
  #:exists 'truncate/replace)

(printf "wrote ~a clause spans to ~a\n"
        (length (hash-ref spans 'clauses))
        (path->string out-path))
