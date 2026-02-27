#lang racket/base

(require rackunit
         racket/file
         racket/list
         racket/path
         "../../src/lolcode/main.rkt")

(define here
  (or (current-load-relative-directory)
      (current-directory)))

(define fixtures-dir
  (build-path here "fixtures"))

(define manifest-path
  (build-path fixtures-dir "manifest.rktd"))

(define (load-cases)
  (call-with-input-file manifest-path read))

(define (case-source-path c)
  (build-path fixtures-dir (hash-ref c 'source-file)))

(module+ test
  (define cases (load-cases))

  (check-true (list? cases))
  (check-true (pair? cases))

  (define versions
    (remove-duplicates (map (lambda (c) (hash-ref c 'spec-version)) cases)))
  (check-not-false (member "1.2" versions))
  (check-not-false (member "1.3" versions))

  (for ([c (in-list cases)])
    (define id (hash-ref c 'id))
    (define source-path (case-source-path c))
    (check-true (file-exists? source-path) (format "fixture source exists for ~a" id))

    (define source (file->string source-path))
    (check-true (string? source))
    (check-true (regexp-match? #px"(?m:^HAI\\s+1\\.[23])" source)
                (format "fixture starts with HAI version in ~a" id))
    (check-true (regexp-match? #px"(?m:^KTHXBYE\\s*$)" source)
                (format "fixture ends with KTHXBYE in ~a" id))

    (define parsed (parse-program source))
    (check-true (program? parsed) (format "parse-program accepts fixture ~a" id))
    (check-true (pair? (program-statements parsed))
                (format "parsed program has statements for ~a" id))

    (define result (run-program parsed))
    (check-true (hash? result) (format "run-program returns hash for fixture ~a" id))

    ;; During bootstrap, conformance fixtures are executable but semantics
    ;; are not yet implemented. Later phases should replace this branch with
    ;; output/value checks derived from each fixture metadata.
    (when (eq? implementation-phase 'bootstrap)
      (check-eq? (hash-ref result 'status) 'not-implemented)
      (check-eq? (hash-ref result 'phase) 'bootstrap))))
