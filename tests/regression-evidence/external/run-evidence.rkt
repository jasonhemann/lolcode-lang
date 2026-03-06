#lang racket/base

(require racket/cmdline
         racket/file
         racket/format
         racket/list
         racket/path
         racket/runtime-path
         racket/string
         "../../../src/lolcode/main.rkt")

(provide load-and-validate-manifest
         evaluate-evidence-cases
         select-cases
         run-evidence-cases)

(define valid-source-kinds
  '("issue" "pr" "commit"))

(define valid-source-origins
  '("issue-body"
    "issue-comment"
    "pr-description"
    "pr-diff"
    "commit-message"
    "commit-diff"))

(define valid-spec-scopes
  '(("1.2")
    ("1.3")
    ("1.2" "1.3")
    ("unknown")))

(define valid-triage-status
  '("candidate"
    "reproducer-ready"
    "spec-ambiguous"
    "known-divergence"
    "out-of-spec-1.4"
    "promoted-conformance"))

(define valid-hypotheses
  '("unknown"
    "expects-pass"
    "expects-parse-error"
    "expects-runtime-error"))

(define required-fields
  '(id
    wave
    source-file
    source-project
    source-repo
    source-kind
    source-id
    source-url
    source-origin
    spec-scope
    spec-refs
    oracle-class
    triage-status
    hypothesis
    notes))

(define optional-fields
  '(expected-stdout
    expected-error-regex
    added-on))

(define all-known-fields
  (append required-fields optional-fields))

(define (fail fmt . args)
  (error 'run-evidence (apply format fmt args)))

(define (non-empty-string? x)
  (and (string? x)
       (not (string=? (string-trim x) ""))))

(define (hash-require who h key pred pred-desc)
  (unless (hash-has-key? h key)
    (fail "~a missing required field '~a'" who key))
  (define v (hash-ref h key))
  (unless (pred v)
    (fail "~a field '~a' must be ~a, got ~e" who key pred-desc v))
  v)

(define (validate-spec-scope who scope)
  (unless (and (list? scope)
               (andmap string? scope))
    (fail "~a field 'spec-scope' must be a list of strings" who))
  (define sorted
    (sort scope string<?))
  (unless (member sorted valid-spec-scopes)
    (fail "~a field 'spec-scope' must be one of ~e, got ~e"
          who
          valid-spec-scopes
          scope)))

(define (validate-spec-refs who refs)
  (unless (and (list? refs)
               (andmap string? refs))
    (fail "~a field 'spec-refs' must be a list of strings" who)))

(define (validate-field-membership who field value allowed)
  (unless (member value allowed)
    (fail "~a field '~a' must be one of ~e, got ~e"
          who
          field
          allowed
          value)))

(define (validate-optional-date who v)
  (unless (and (string? v)
               (regexp-match? #px"^[0-9]{4}-[0-9]{2}-[0-9]{2}$" v))
    (fail "~a optional field 'added-on' must be YYYY-MM-DD, got ~e" who v)))

(define (validate-source-file who source-file)
  (define p (string->path source-file))
  (when (absolute-path? p)
    (fail "~a field 'source-file' must be a relative path, got ~e" who source-file))
  (define elems (explode-path p))
  (when (member (string->path "..") elems)
    (fail "~a field 'source-file' must not contain '..', got ~e" who source-file)))

(define (validate-case idx c)
  (unless (hash? c)
    (fail "manifest entry ~a must be #hasheq, got ~e" idx c))
  (define who (format "manifest entry ~a (~a)" idx (hash-ref c 'id "<missing-id>")))

  (for ([k (in-list required-fields)])
    (unless (hash-has-key? c k)
      (fail "~a missing required field '~a'" who k)))

  (hash-require who c 'id non-empty-string? "a non-empty string")
  (hash-require who c 'wave exact-positive-integer? "a positive integer")
  (define source-file
    (hash-require who c 'source-file non-empty-string? "a non-empty string"))
  (validate-source-file who source-file)

  (hash-require who c 'source-project non-empty-string? "a non-empty string")
  (hash-require who c 'source-repo non-empty-string? "a non-empty string")
  (define source-kind
    (hash-require who c 'source-kind non-empty-string? "a non-empty string"))
  (validate-field-membership who 'source-kind source-kind valid-source-kinds)

  (hash-require who c 'source-id non-empty-string? "a non-empty string")

  (define source-url
    (hash-require who c 'source-url non-empty-string? "a non-empty string"))
  (unless (regexp-match? #px"^https?://" source-url)
    (fail "~a field 'source-url' must start with http:// or https://, got ~e"
          who
          source-url))

  (define source-origin
    (hash-require who c 'source-origin non-empty-string? "a non-empty string"))
  (validate-field-membership who 'source-origin source-origin valid-source-origins)

  (validate-spec-scope who (hash-ref c 'spec-scope))
  (validate-spec-refs who (hash-ref c 'spec-refs))

  (define oracle-class
    (hash-require who c 'oracle-class non-empty-string? "a non-empty string"))
  (unless (string=? oracle-class "external-evidence")
    (fail "~a field 'oracle-class' must be \"external-evidence\", got ~e" who oracle-class))

  (define triage-status
    (hash-require who c 'triage-status non-empty-string? "a non-empty string"))
  (validate-field-membership who 'triage-status triage-status valid-triage-status)

  (define hypothesis
    (hash-require who c 'hypothesis non-empty-string? "a non-empty string"))
  (validate-field-membership who 'hypothesis hypothesis valid-hypotheses)

  (hash-require who c 'notes string? "a string")

  (when (hash-has-key? c 'expected-stdout)
    (unless (string? (hash-ref c 'expected-stdout))
      (fail "~a optional field 'expected-stdout' must be string" who)))

  (when (hash-has-key? c 'expected-error-regex)
    (unless (string? (hash-ref c 'expected-error-regex))
      (fail "~a optional field 'expected-error-regex' must be string" who)))

  (when (hash-has-key? c 'added-on)
    (validate-optional-date who (hash-ref c 'added-on)))

  (for ([k (in-list (hash-keys c))])
    (unless (member k all-known-fields)
      (fail "~a contains unknown field '~a'" who k))))

(define (load-and-validate-manifest manifest-path)
  (unless (file-exists? manifest-path)
    (fail "manifest does not exist: ~a" manifest-path))
  (define cases
    (call-with-input-file manifest-path read))
  (unless (list? cases)
    (fail "manifest must be a list of #hasheq entries"))

  (for ([c (in-list cases)]
        [idx (in-naturals 1)])
    (validate-case idx c))

  (define ids
    (map (lambda (c) (hash-ref c 'id)) cases))
  (define dedup-ids
    (remove-duplicates ids string=?))
  (unless (= (length ids) (length dedup-ids))
    (fail "manifest contains duplicate ids"))

  cases)

(define (select-cases cases selected-wave selected-id)
  (filter
   (lambda (c)
     (and (or (not selected-wave)
              (= (hash-ref c 'wave) selected-wave))
          (or (not selected-id)
              (string=? (hash-ref c 'id) selected-id))))
   cases))

(define (parse-scope-arg s)
  (cond
    [(string=? s "1.2") '("1.2")]
    [(string=? s "1.3") '("1.3")]
    [(or (string=? s "1.2+1.3")
         (string=? s "1.3+1.2"))
     '("1.2" "1.3")]
    [(string=? s "unknown") '("unknown")]
    [else
     (fail "--scope must be one of 1.2, 1.3, 1.2+1.3, unknown; got ~e" s)]))

(define (scope->arg-label scope)
  (cond
    [(equal? scope '("1.2")) "1.2"]
    [(equal? scope '("1.3")) "1.3"]
    [(equal? scope '("1.2" "1.3")) "1.2+1.3"]
    [(equal? scope '("unknown")) "unknown"]
    [else (format "~s" scope)]))

(define (select-cases/scope cases selected-wave selected-id selected-scope)
  (filter
   (lambda (c)
     (and (or (not selected-wave)
              (= (hash-ref c 'wave) selected-wave))
          (or (not selected-id)
              (string=? (hash-ref c 'id) selected-id))
          (or (not selected-scope)
              (equal? (hash-ref c 'spec-scope) selected-scope))))
   cases))

(define (parse-one-of who arg allowed)
  (unless (member arg allowed)
    (fail "~a must be one of ~a, got ~e"
          who
          (string-join allowed ", ")
          arg))
  arg)

(define (select-cases/filters cases
                              selected-wave
                              selected-id
                              selected-scope
                              selected-triage
                              selected-hypothesis)
  (filter
   (lambda (c)
     (and (or (not selected-wave)
              (= (hash-ref c 'wave) selected-wave))
          (or (not selected-id)
              (string=? (hash-ref c 'id) selected-id))
          (or (not selected-scope)
              (equal? (hash-ref c 'spec-scope) selected-scope))
          (or (not selected-triage)
              (string=? (hash-ref c 'triage-status) selected-triage))
          (or (not selected-hypothesis)
              (string=? (hash-ref c 'hypothesis) selected-hypothesis))))
   cases))

(define (assessment-for c observed-status observed-stdout observed-message)
  (define hypothesis (hash-ref c 'hypothesis))
  (define expected-stdout
    (hash-ref c 'expected-stdout #f))
  (define expected-error-regex
    (hash-ref c 'expected-error-regex #f))

  (define base-assessment
    (case (string->symbol hypothesis)
      [(unknown) "unknown"]
      [(expects-pass) (if (string=? observed-status "ok") "supports" "conflicts")]
      [(expects-parse-error) (if (string=? observed-status "parse-error") "supports" "conflicts")]
      [(expects-runtime-error) (if (string=? observed-status "runtime-error") "supports" "conflicts")]
      [else "unknown"]))

  (define stdout-check
    (cond
      [(not expected-stdout) "n/a"]
      [(string=? observed-stdout expected-stdout) "match"]
      [else "mismatch"]))

  (define regex-check
    (cond
      [(not expected-error-regex) "n/a"]
      [(and observed-message
            (regexp-match? (pregexp expected-error-regex) observed-message))
       "match"]
      [else "mismatch"]))

  (values base-assessment stdout-check regex-check))

(define (run-one-case c manifest-dir)
  (define source-path
    (build-path manifest-dir (hash-ref c 'source-file)))
  (unless (file-exists? source-path)
    (fail "fixture missing for case ~a: ~a"
          (hash-ref c 'id)
          source-path))

  (define source
    (file->string source-path))

  (define observed-status #f)
  (define observed-stdout "")
  (define observed-message #f)

  (define parsed
    (with-handlers ([exn:fail?
                     (lambda (e)
                       (set! observed-status "parse-error")
                       (set! observed-message (exn-message e))
                       #f)])
      (parse-program source)))

  (when parsed
    (with-handlers ([exn:fail?
                     (lambda (e)
                       (set! observed-status "runtime-error")
                       (set! observed-message (exn-message e)))])
      (define result (run-program parsed))
      (define status (hash-ref result 'status))
      (set! observed-status
            (case status
              [(ok) "ok"]
              [(runtime-error) "runtime-error"]
              [(unsupported) "unsupported"]
              [else (format "~a" status)]))
      (set! observed-stdout (hash-ref result 'stdout ""))
      (when (hash-has-key? result 'error)
        (set! observed-message (hash-ref result 'error)))
      (when (hash-has-key? result 'reason)
        (set! observed-message (hash-ref result 'reason)))))

  (define-values (assessment stdout-check regex-check)
    (assessment-for c observed-status observed-stdout observed-message))

  (hash 'id (hash-ref c 'id)
        'wave (hash-ref c 'wave)
        'project (hash-ref c 'source-project)
        'source-kind (hash-ref c 'source-kind)
        'source-id (hash-ref c 'source-id)
        'source-url (hash-ref c 'source-url)
        'spec-scope (hash-ref c 'spec-scope)
        'spec-refs (hash-ref c 'spec-refs)
        'triage-status (hash-ref c 'triage-status)
        'hypothesis (hash-ref c 'hypothesis)
        'observed-status observed-status
        'assessment assessment
        'stdout-check stdout-check
        'regex-check regex-check
        'observed-message observed-message
        'notes (hash-ref c 'notes)
        'source-file (hash-ref c 'source-file)))

(define (status-count rows key)
  (for/fold ([acc (hash)]) ([r (in-list rows)])
    (define value (hash-ref r key))
    (hash-set acc value (+ 1 (hash-ref acc value 0)))))

(define (print-counts label counts)
  (displayln label)
  (for ([k (in-list (sort (hash-keys counts) string<?))])
    (printf "  ~a: ~a\n" k (hash-ref counts k))))

(define (print-report rows)
  (displayln "id\twave\tproject\tkind\tsource-id\tobserved\tassessment\ttriage\thypothesis\tstdout-check\terror-check")
  (for ([r (in-list rows)])
    (printf "~a\t~a\t~a\t~a\t~a\t~a\t~a\t~a\t~a\t~a\t~a\n"
            (hash-ref r 'id)
            (hash-ref r 'wave)
            (hash-ref r 'project)
            (hash-ref r 'source-kind)
            (hash-ref r 'source-id)
            (hash-ref r 'observed-status)
            (hash-ref r 'assessment)
            (hash-ref r 'triage-status)
            (hash-ref r 'hypothesis)
            (hash-ref r 'stdout-check)
            (hash-ref r 'regex-check)))
  (newline)
  (print-counts "Observed status counts:" (status-count rows 'observed-status))
  (print-counts "Assessment counts:" (status-count rows 'assessment))
  (newline)
  (displayln "Note: semantic conflicts are reported as evidence and do not fail this run."))

(define (evaluate-evidence-cases manifest-path
                                 selected-wave
                                 selected-id
                                 [selected-scope #f]
                                 [selected-triage #f]
                                 [selected-hypothesis #f])
  (define cases
    (load-and-validate-manifest manifest-path))

  (define selected
    (select-cases/filters cases
                          selected-wave
                          selected-id
                          selected-scope
                          selected-triage
                          selected-hypothesis))

  (when selected-id
    (unless (ormap (lambda (c) (string=? (hash-ref c 'id) selected-id)) cases)
      (fail "requested --id not found in manifest: ~a" selected-id)))

  (cond
    [(null? selected) '()]
    [else
     (define manifest-dir
       (or (path-only (simplify-path manifest-path))
           (current-directory)))

     (for/list ([c (in-list selected)])
       (run-one-case c manifest-dir))]))

(define (run-evidence-cases manifest-path
                            selected-wave
                            selected-id
                            [selected-scope #f]
                            [selected-triage #f]
                            [selected-hypothesis #f])
  (define rows
    (evaluate-evidence-cases manifest-path
                             selected-wave
                             selected-id
                             selected-scope
                             selected-triage
                             selected-hypothesis))
  (when (null? rows)
    (if selected-scope
        (printf "No evidence cases selected (scope: ~a).\n"
                (scope->arg-label selected-scope))
        (displayln "No evidence cases selected."))
    (void))
  (print-report rows)
  rows)

(define-runtime-path default-manifest-path "manifest.rktd")

(module+ main
  (define manifest-path
    default-manifest-path)
  (define selected-wave #f)
  (define selected-id #f)
  (define selected-scope #f)
  (define selected-triage #f)
  (define selected-hypothesis #f)

  (command-line
   #:program "run-evidence.rkt"
   #:once-each
   [("--manifest") m "Path to manifest.rktd"
                    (set! manifest-path (string->path m))]
   [("--wave") w "Select only wave N"
                 (define maybe-wave (string->number w))
                 (unless (and maybe-wave
                              (exact-integer? maybe-wave)
                              (> maybe-wave 0))
                   (fail "--wave must be a positive integer, got ~e" w))
                 (set! selected-wave maybe-wave)]
   [("--id") case-id "Select only one case id"
               (set! selected-id case-id)]
   [("--scope") s "Select only one spec scope: 1.2 | 1.3 | 1.2+1.3 | unknown"
                 (set! selected-scope (parse-scope-arg s))]
   [("--triage") s "Select only one triage-status"
                  (set! selected-triage
                        (parse-one-of "--triage" s valid-triage-status))]
   [("--hypothesis") s "Select only one hypothesis"
                      (set! selected-hypothesis
                            (parse-one-of "--hypothesis" s valid-hypotheses))])

  (void (run-evidence-cases manifest-path
                            selected-wave
                            selected-id
                            selected-scope
                            selected-triage
                            selected-hypothesis)))
