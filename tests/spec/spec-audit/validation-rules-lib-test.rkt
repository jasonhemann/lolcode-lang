#lang racket/base

(require rackunit
         racket/file
         racket/list
         racket/path
         racket/string
         "../../../scripts/validation_rules_lib.rkt")

(module+ test
  (test-case "missing required key emits one error"
    (define rules
      (list (make-field-rule 'id #t '())))
    (define errs
      (validate-hash-entry #hasheq() 1 rules))
    (check-equal? errs (list "entry 1: missing key id")))

  (test-case "invalid type emits rule-specific error"
    (define rules
      (list (make-field-rule
             'id
             #t
             (list (make-check
                    (lambda (v _ctx) (string? v))
                    (lambda (v _ctx) (format "id must be string, got ~e" v)))))))
    (define errs
      (validate-hash-entry (hasheq 'id 42) 2 rules))
    (check-equal? (length errs) 1)
    (check-true (string-contains? (car errs) "id must be string")))

  (test-case "path check fails when referenced path is missing"
    (define tmp
      (make-temporary-file "validation-rules-missing-~a"))
    (delete-file tmp)
    (define root
      (or (path-only tmp) (current-directory)))
    (define rel
      (path->string (file-name-from-path tmp)))
    (define rules
      (list (make-field-rule
             'refs
             #t
             (list
              (make-check
               (lambda (v _ctx) (and (list? v) (andmap string? v)))
               (lambda (v _ctx) (format "refs must be list of strings, got ~e" v)))
              (make-check
               (lambda (v ctx)
                 (or (not (and (list? v) (andmap string? v)))
                     (null? (missing-relative-paths (hash-ref ctx 'root) v))))
               (lambda (_v _ctx) "refs path missing"))))))
    (define errs
      (validate-hash-entry (hasheq 'refs (list rel))
                           3
                           rules
                           (hasheq 'root root)))
    (check-equal? (length errs) 1)
    (check-true (string-contains? (car errs) "refs path missing")))

  (test-case "multiple failures preserve rule/check order"
    (define rules
      (list
       (make-field-rule
        'id
        #t
        (list (make-check
               (lambda (v _ctx) (string? v))
               (lambda (_v _ctx) "id must be string"))))
       (make-field-rule
        'status
        #t
        (list (make-check
               (lambda (v _ctx) (eq? v 'ok))
               (lambda (_v _ctx) "status must be ok"))))))
    (define errs
      (validate-hash-entry (hasheq 'id 1 'status 'bad) 4 rules))
    (check-equal? (length errs) 2)
    (check-true (string-contains? (list-ref errs 0) "id must be string"))
    (check-true (string-contains? (list-ref errs 1) "status must be ok")))

  (test-case "duplicate-string-id-error reports sorted unique duplicates"
    (check-equal?
     (duplicate-string-id-error (list "N02" "N01" "N02" "N03" "N01")
                                "dupes")
     "dupes: N01, N02")
    (check-false
     (duplicate-string-id-error (list "N01" "N02") "dupes")))

  (test-case "parse-cli-options accepts known flags and rejects malformed/unknown"
    (define specs
      (list (hasheq 'flag "--alpha" 'key 'alpha 'mode 'value 'convert string->number)
            (hasheq 'flag "--beta" 'key 'beta 'mode 'switch 'value #t)))
    (define defaults
      (hasheq 'alpha 0
              'beta #f))
    (define parsed
      (parse-cli-options 'validation-rules-lib-test
                         (list "--beta" "--alpha" "7")
                         specs
                         defaults))
    (check-equal? (hash-ref parsed 'alpha) 7)
    (check-equal? (hash-ref parsed 'beta) #t)
    (check-exn exn:fail?
               (lambda ()
                 (parse-cli-options 'validation-rules-lib-test
                                    (list "--alpha")
                                    specs
                                    defaults)))
    (check-exn exn:fail?
               (lambda ()
                 (parse-cli-options 'validation-rules-lib-test
                                    (list "--gamma" "1")
                                    specs
                                    defaults)))
    (check-exn exn:fail?
               (lambda ()
                 (parse-cli-options 'validation-rules-lib-test
                                    (list "--bad" "x")
                                    (list (hasheq 'flag "--bad"
                                                  'key 'bad
                                                  'mode 'invalid))
                                    defaults)))))
