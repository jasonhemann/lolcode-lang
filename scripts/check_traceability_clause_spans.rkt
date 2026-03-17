#lang racket/base

(require racket/path
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
        (hasheq 'flag "--spans"
                'key 'spans-path
                'mode 'value
                'convert string->path)))

(define option-defaults
  (hasheq 'graph-path default-traceability-graph-path
          'spec-path default-spec-path
          'spans-path default-clause-spans-path))

(define opts
  (parse-cli-options 'check_traceability_clause_spans
                     (vector->list (current-command-line-arguments))
                     option-specs
                     option-defaults))

(define graph-path (hash-ref opts 'graph-path))
(define spec-path (hash-ref opts 'spec-path))
(define spans-path (hash-ref opts 'spans-path))

(define on-disk
  (validate-traceability-clause-spans
   (load-traceability-clause-spans spans-path)
   graph-path
   spec-path))

(define expected
  (validate-traceability-clause-spans
   (build-traceability-clause-spans graph-path spec-path)
   graph-path
   spec-path))

(unless (equal? on-disk expected)
  (error 'check_traceability_clause_spans
         (string-append
          "traceability-clause-spans drift detected.\n"
          "Regenerate with: racket scripts/build_traceability_clause_spans.rkt")))

(printf "Traceability clause spans OK (~a entries)\n"
        (length (hash-ref on-disk 'clauses)))
