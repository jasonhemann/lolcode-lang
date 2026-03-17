#lang racket/base

(require racket/file
         racket/path
         racket/pretty
         "adjudication_index_lib.rkt"
         "validation_rules_lib.rkt")

(define option-specs
  (list (hasheq 'flag "--map" 'key 'map-path 'mode 'value 'convert string->path)
        (hasheq 'flag "--anchors" 'key 'anchor-path 'mode 'value 'convert string->path)
        (hasheq 'flag "--ledger" 'key 'ledger-path 'mode 'value 'convert string->path)
        (hasheq 'flag "--out" 'key 'out-path 'mode 'value 'convert string->path)))

(define option-defaults
  (hasheq 'map-path default-resolution-map-path
          'anchor-path default-test-anchor-index-path
          'ledger-path default-adjudication-ledger-path
          'out-path default-adjudication-index-path))

(define opts
  (parse-cli-options 'build_adjudication_index
                     (vector->list (current-command-line-arguments))
                     option-specs
                     option-defaults))

(define map-path (hash-ref opts 'map-path))
(define anchor-path (hash-ref opts 'anchor-path))
(define ledger-path (hash-ref opts 'ledger-path))
(define out-path (hash-ref opts 'out-path))

(define entries
  (validate-adjudication-index
   (build-adjudication-index map-path anchor-path ledger-path)))

(make-directory* (path-only out-path))
(call-with-output-file out-path
  (lambda (out)
    (pretty-write entries out))
  #:exists 'truncate/replace)

(printf "wrote ~a entries to ~a\n"
        (length entries)
        (path->string out-path))
