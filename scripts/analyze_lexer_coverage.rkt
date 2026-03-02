#lang racket/base

(require json
         racket/cmdline
         racket/date
         racket/file
         racket/format
         racket/list
         racket/path
         racket/runtime-path
         racket/set
         racket/string
         "../src/lolcode/lexer.rkt")

(define-runtime-path script-dir ".")
(define repo-root
  (simplify-path (build-path script-dir "..")))

(define fixtures-root
  (build-path repo-root "tests" "spec" "fixtures" "programs"))
(define corpus-root
  (build-path repo-root "corpus" "tier2"))
(define promoted-root
  (build-path repo-root "corpus" "research" "promoted-1_3-programs"))
(define include-promoted? #t)
(define json-out
  (build-path repo-root "corpus" "research" "lexer-coverage-report.json"))
(define md-out
  (build-path repo-root "corpus" "research" "LEXER_COVERAGE_REPORT_2026-03-02.md"))

(command-line
 #:program "analyze_lexer_coverage.rkt"
 #:once-each
 [("--fixtures-root")
  dir
  "Fixture root directory to scan recursively for .lol files."
  (set! fixtures-root (string->path dir))]
 [("--corpus-root")
  dir
  "Corpus root directory to scan recursively for .lol files."
  (set! corpus-root (string->path dir))]
 [("--promoted-root")
  dir
  "Promoted corpus root directory to scan recursively for .lol files."
  (set! promoted-root (string->path dir))]
 [("--no-promoted")
  "Do not include promoted corpus files in coverage run."
  (set! include-promoted? #f)]
 [("--json-out")
  p
  "Output JSON path."
  (set! json-out (string->path p))]
 [("--md-out")
  p
  "Output markdown path."
  (set! md-out (string->path p))])

(define (path->display p)
  (path->string (find-relative-path repo-root p)))

(define (lol-file? p)
  (and (file-exists? p)
       (regexp-match? #px"(?i:\\.lol)$" (path->string p))))

(define (collect-lol-files root)
  (cond
    [(directory-exists? root)
     (sort
      (for/list ([p (in-directory root)]
                 #:when (lol-file? p))
        p)
      string<?
      #:key path->string)]
    [else '()]))

(define (hash-inc h k [n 1])
  (hash-set h k (+ n (hash-ref h k 0))))

(define (merge-count-hashes hashes)
  (for/fold ([acc (hash)])
            ([h (in-list hashes)])
    (for/fold ([acc2 acc])
              ([(k v) (in-hash h)])
      (hash-set acc2 k (+ v (hash-ref acc2 k 0))))))

(define (normalize-message msg)
  (if (and (string? msg) (not (string=? (string-trim msg) "")))
      (car (string-split (string-trim msg) "\n"))
      "(no message)"))

(define (rows-from-count-hash h)
  (for/list ([kv (in-list (sort (hash->list h) > #:key cdr))])
    (hash 'label (~a (car kv))
          'count (cdr kv))))

(define (set->sorted-strings s)
  (sort (map ~a (set->list s)) string<?))

(define (run-lex-sources files)
  (define-values (status-counts error-counts error-rows)
    (for/fold ([status-counts (hash)]
               [error-counts (hash)]
               [error-rows '()])
              ([p (in-list files)])
      (define rel (path->display p))
      (define src (file->string p))
      (with-handlers ([exn:fail?
                       (lambda (e)
                         (define msg (normalize-message (exn-message e)))
                         (values (hash-inc status-counts 'lex-error)
                                 (hash-inc error-counts msg)
                                 (cons (hash 'path rel 'message msg) error-rows)))])
        (lex-source src)
        (values (hash-inc status-counts 'ok)
                error-counts
                error-rows))))
  (hash 'status-counts status-counts
        'error-counts (rows-from-count-hash error-counts)
        'error-rows (reverse error-rows)))

(define test-submodules
  (list
   `(submod ,(build-path repo-root "tests" "smoke-test.rkt") test)
   `(submod ,(build-path repo-root "tests" "spec" "parse-negative-test.rkt") test)
   `(submod ,(build-path repo-root "tests" "spec" "runtime-core-test.rkt") test)))

(define (run-tests)
  (define-values (status-counts failures)
    (for/fold ([status-counts (hash)]
               [failures '()])
              ([submod-path (in-list test-submodules)])
      (define label (~a submod-path))
      (with-handlers ([exn:fail?
                       (lambda (e)
                         (define msg (normalize-message (exn-message e)))
                         (values (hash-inc status-counts 'failed)
                                 (cons (hash 'module label 'message msg) failures)))])
        (parameterize ([current-directory repo-root])
          (dynamic-require submod-path #f))
        (values (hash-inc status-counts 'ok)
                failures))))
  (hash 'status-counts status-counts
        'failures (reverse failures)))

(define (run-with-coverage thunk)
  (lexer-coverage-reset!)
  (define run-result
    (parameterize ([lexer-coverage-enabled? #t])
      (thunk)))
  (values run-result
          (lexer-coverage-snapshot)))

(define fixture-files
  (collect-lol-files fixtures-root))

(define corpus-files
  (collect-lol-files corpus-root))

(define promoted-files
  (if include-promoted?
      (collect-lol-files promoted-root)
      '()))

(define-values (tests-run tests-coverage)
  (run-with-coverage run-tests))

(define-values (fixtures-run fixtures-coverage)
  (run-with-coverage
   (lambda ()
     (run-lex-sources fixture-files))))

(define-values (corpus-run corpus-coverage)
  (run-with-coverage
   (lambda ()
     (run-lex-sources corpus-files))))

(define-values (promoted-run promoted-coverage)
  (run-with-coverage
   (lambda ()
     (run-lex-sources promoted-files))))

(define total-coverage
  (merge-count-hashes
   (list tests-coverage
         fixtures-coverage
         corpus-coverage
         promoted-coverage)))

(define (keys-hit coverage)
  (for/set ([kv (in-list (hash->list coverage))]
            #:when (> (cdr kv) 0))
    (car kv)))

(define tests-hit (keys-hit tests-coverage))
(define fixtures-hit (keys-hit fixtures-coverage))
(define corpus-hit (keys-hit corpus-coverage))
(define promoted-hit (keys-hit promoted-coverage))
(define total-hit (keys-hit total-coverage))

(define all-keys
  (list->set lexer-coverage-universe))

(define never-hit
  (sort
   (set->list (set-subtract all-keys total-hit))
   symbol<?))

(define report
  (hash
   'generated-at (date->string (current-date) #t)
   'paths (hash 'fixtures-root (path->display fixtures-root)
                'corpus-root (path->display corpus-root)
                'promoted-root (path->display promoted-root)
                'json-out (path->display json-out)
                'md-out (path->display md-out))
   'inputs (hash 'fixtures-file-count (length fixture-files)
                 'corpus-file-count (length corpus-files)
                 'promoted-file-count (length promoted-files)
                 'include-promoted include-promoted?)
   'tests tests-run
   'fixtures fixtures-run
   'corpus corpus-run
   'promoted promoted-run
   'coverage (hash 'tests (rows-from-count-hash tests-coverage)
                   'fixtures (rows-from-count-hash fixtures-coverage)
                   'corpus (rows-from-count-hash corpus-coverage)
                   'promoted (rows-from-count-hash promoted-coverage)
                   'total (rows-from-count-hash total-coverage))
   'hit-sets (hash 'tests (set->sorted-strings tests-hit)
                   'fixtures (set->sorted-strings fixtures-hit)
                   'corpus (set->sorted-strings corpus-hit)
                   'promoted (set->sorted-strings promoted-hit)
                   'total (set->sorted-strings total-hit))
   'never-hit (map ~a never-hit)))

(define (write-count-section out title rows)
  (fprintf out "### ~a\n\n" title)
  (if (null? rows)
      (fprintf out "- (none)\n\n")
      (begin
        (for ([r (in-list rows)])
          (fprintf out "- `~a`: `~a`\n"
                   (hash-ref r 'label)
                   (hash-ref r 'count)))
        (newline out))))

(define (write-list-section out title xs)
  (fprintf out "### ~a\n\n" title)
  (if (null? xs)
      (fprintf out "- (none)\n\n")
      (begin
        (for ([x (in-list xs)])
          (fprintf out "- `~a`\n" x))
        (newline out))))

(define (sample-errors rows [limit 10])
  (take rows (min limit (length rows))))

(make-directory* (path-only json-out))
(make-directory* (path-only md-out))

(call-with-output-file json-out
  (lambda (out)
    (write-json report out))
  #:exists 'replace)

(call-with-output-file md-out
  (lambda (out)
    (fprintf out "# Lexer Coverage Report\n\n")
    (fprintf out "Generated: `~a`\n\n" (hash-ref report 'generated-at))
    (define inputs (hash-ref report 'inputs))
    (fprintf out "## Inputs\n\n")
    (fprintf out "- Fixture `.lol` files: `~a`\n" (hash-ref inputs 'fixtures-file-count))
    (fprintf out "- Corpus `.lol` files: `~a`\n" (hash-ref inputs 'corpus-file-count))
    (fprintf out "- Promoted `.lol` files included: `~a`\n" (hash-ref inputs 'promoted-file-count))
    (fprintf out "- Include promoted: `~a`\n\n" (hash-ref inputs 'include-promoted))

    (define tests (hash-ref report 'tests))
    (write-count-section out "Test Submodule Status Counts"
                         (rows-from-count-hash (hash-ref tests 'status-counts)))
    (write-count-section out "Fixture Lex Status Counts"
                         (rows-from-count-hash (hash-ref (hash-ref report 'fixtures) 'status-counts)))
    (write-count-section out "Corpus Lex Status Counts"
                         (rows-from-count-hash (hash-ref (hash-ref report 'corpus) 'status-counts)))
    (write-count-section out "Promoted Lex Status Counts"
                         (rows-from-count-hash (hash-ref (hash-ref report 'promoted) 'status-counts)))

    (define cov (hash-ref report 'coverage))
    (write-count-section out "Lexer Branch Hits (Total)" (hash-ref cov 'total))
    (write-list-section out "Lexer Branches Never Hit (Tests + Fixtures + Corpus + Promoted)"
                        (hash-ref report 'never-hit))

    (define fixtures-errors
      (sample-errors (hash-ref (hash-ref report 'fixtures) 'error-rows)))
    (define corpus-errors
      (sample-errors (hash-ref (hash-ref report 'corpus) 'error-rows)))
    (define promoted-errors
      (sample-errors (hash-ref (hash-ref report 'promoted) 'error-rows)))

    (fprintf out "### Sample Fixture Lex Errors\n\n")
    (if (null? fixtures-errors)
        (fprintf out "- (none)\n\n")
        (begin
          (for ([r (in-list fixtures-errors)])
            (fprintf out "- `~a`: `~a`\n"
                     (hash-ref r 'path)
                     (hash-ref r 'message)))
          (newline out)))

    (fprintf out "### Sample Corpus Lex Errors\n\n")
    (if (null? corpus-errors)
        (fprintf out "- (none)\n\n")
        (begin
          (for ([r (in-list corpus-errors)])
            (fprintf out "- `~a`: `~a`\n"
                     (hash-ref r 'path)
                     (hash-ref r 'message)))
          (newline out)))

    (fprintf out "### Sample Promoted Lex Errors\n\n")
    (if (null? promoted-errors)
        (fprintf out "- (none)\n\n")
        (begin
          (for ([r (in-list promoted-errors)])
            (fprintf out "- `~a`: `~a`\n"
                     (hash-ref r 'path)
                     (hash-ref r 'message)))
          (newline out))))
  #:exists 'replace)

(printf "Wrote JSON report: ~a\n" (path->display json-out))
(printf "Wrote markdown report: ~a\n" (path->display md-out))
