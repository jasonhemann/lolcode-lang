#lang racket/base

(require rackunit
         racket/file
         racket/list
         racket/path
         "../../src/lolcode/main.rkt"
         "../../src/lolcode/internal/reporting.rkt")

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
  (check-not-false (member "1.3" versions))
  (check-equal? versions '("1.3"))

  (for ([c (in-list cases)])
    (define id (hash-ref c 'id))
    (define source-path (case-source-path c))
    (check-true (file-exists? source-path) (format "fixture source exists for ~a" id))

    (define source (file->string source-path))
    (check-true (string? source))
    (check-true (regexp-match? #px"(?m:^HAI\\s+1\\.3)" source)
                (format "fixture starts with HAI 1.3 in ~a" id))
    (check-true (regexp-match? #px"(?m:^KTHXBYE\\s*$)" source)
                (format "fixture ends with KTHXBYE in ~a" id))

    (define parsed (parse-program source))
    (check-true (program? parsed) (format "parse-program accepts fixture ~a" id))
    (check-true (pair? (program-statements parsed))
                (format "parsed program has statements for ~a" id))

    (define result (run-program/report parsed))
    (check-true (hash? result) (format "run-program/report returns hash for fixture ~a" id))
    (check-eq? (hash-ref result 'status)
               'ok
               (format "fixture executes successfully for ~a" id))
    (check-eq? (hash-ref result 'phase)
               implementation-phase
               (format "phase marker propagated for ~a" id))

    (define expected-stdout (hash-ref c 'expected-stdout))
    (when (string? expected-stdout)
      (check-equal? (hash-ref result 'stdout)
                    expected-stdout
                    (format "stdout matches fixture expectation for ~a" id)))))
