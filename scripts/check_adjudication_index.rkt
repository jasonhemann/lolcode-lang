#lang racket/base

(require racket/format
         racket/list
         racket/path
         "adjudication_index_lib.rkt"
         "validation_rules_lib.rkt")

(define option-specs
  (list (hasheq 'flag "--index" 'key 'index-path 'mode 'value 'convert string->path)
        (hasheq 'flag "--map" 'key 'map-path 'mode 'value 'convert string->path)
        (hasheq 'flag "--anchors" 'key 'anchor-path 'mode 'value 'convert string->path)
        (hasheq 'flag "--ledger" 'key 'ledger-path 'mode 'value 'convert string->path)))

(define option-defaults
  (hasheq 'index-path default-adjudication-index-path
          'map-path default-resolution-map-path
          'anchor-path default-test-anchor-index-path
          'ledger-path default-adjudication-ledger-path))

(define opts
  (parse-cli-options 'check_adjudication_index
                     (vector->list (current-command-line-arguments))
                     option-specs
                     option-defaults))

(define index-path (hash-ref opts 'index-path))
(define map-path (hash-ref opts 'map-path))
(define anchor-path (hash-ref opts 'anchor-path))
(define ledger-path (hash-ref opts 'ledger-path))

(define on-disk
  (validate-adjudication-index
   (load-adjudication-index index-path)))

(define expected
  (validate-adjudication-index
   (build-adjudication-index map-path anchor-path ledger-path)))

(unless (equal? on-disk expected)
  (error 'check_adjudication_index
         (string-append
          "adjudication-index drift detected.\n"
          (format "on-disk entries: ~a\n" (length on-disk))
          (format "expected entries: ~a\n" (length expected))
          "Regenerate with: racket scripts/build_adjudication_index.rkt")))

(printf "Adjudication index OK (~a entries)\n" (length on-disk))
