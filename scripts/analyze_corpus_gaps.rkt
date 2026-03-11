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
         "../src/lolcode/ast.rkt"
         "../src/lolcode/lexer.rkt"
         "../src/lolcode/main.rkt"
         "../src/lolcode/internal/reporting.rkt")

(define-runtime-path script-dir ".")
(define repo-root
  (simplify-path (build-path script-dir "..")))

(define corpus-root
  (build-path repo-root "corpus" "tier2"))
(define fixtures-root
  (build-path repo-root "tests" "spec" "fixtures" "programs"))
(define json-out
  (build-path repo-root "corpus" "research" "language-gaps-report.json"))
(define md-out
  (build-path repo-root "corpus" "research" "LANGUAGE_GAPS_REPORT.md"))
(define promote-missing-version? #f)
(define promoted-out-dir #f)

(define promotion-comment
  "BTW AUTO-PROMOTE: inserted HAI 1.3 header for strict-1.3 triage")

(command-line
 #:program "analyze_corpus_gaps.rkt"
 #:once-each
 [("--corpus-root")
  dir
  "Tier corpus root directory to scan recursively for .lol files."
  (set! corpus-root (string->path dir))]
 [("--fixtures-root")
  dir
  "1.3 fixture root directory to scan recursively for .lol files."
  (set! fixtures-root (string->path dir))]
 [("--json-out")
  p
  "Output JSON path."
  (set! json-out (string->path p))]
 [("--md-out")
  p
  "Output markdown path."
  (set! md-out (string->path p))]
 [("--promote-missing-version-to-1.3")
  "Promote leading `HAI` (without explicit version) to `HAI 1.3` during analysis."
  (set! promote-missing-version? #t)]
 [("--promoted-out-dir")
  dir
  "If set with promotion mode, writes transformed promoted sources under this directory."
  (set! promoted-out-dir (string->path dir))])

(define (path->display p)
  (path->string (find-relative-path repo-root p)))

(define (lol-file? p)
  (and (file-exists? p)
       (regexp-match? #px"(?i:\\.lol)$" (path->string p))))

(define (collect-lol-files root)
  (sort
   (for/list ([p (in-directory root)]
              #:when (lol-file? p))
     p)
   string<?
   #:key path->string))

(define (first-meaningful-line source)
  (define lines (regexp-split #px"\r\n|\n|\r" source))
  (let loop ([ls lines] [in-block-comment? #f])
    (cond
      [(null? ls) #f]
      [else
       (define line (string-trim (car ls)))
       (cond
         [in-block-comment?
          (if (regexp-match? #px"(?i:\\bTLDR\\b)" line)
              (loop (cdr ls) #f)
              (loop (cdr ls) #t))]
         [(string=? line "")
          (loop (cdr ls) #f)]
         [(regexp-match? #px"^#!" line)
          (loop (cdr ls) #f)]
         [(regexp-match? #px"(?i:^OBTW\\b)" line)
          (if (regexp-match? #px"(?i:\\bTLDR\\b)" line)
              (loop (cdr ls) #f)
              (loop (cdr ls) #t))]
         [(regexp-match? #px"(?i:^BTW\\b)" line)
          (loop (cdr ls) #f)]
         [else line])])))

(define (header-class source)
  (define first-line (first-meaningful-line source))
  (cond
    [(not first-line) "non-program-empty-or-comments"]
    [else
     (define m (regexp-match #px"(?i:^HAI(?:\\s+([^\\s]+))?\\b)" first-line))
     (cond
       [(not m) "non-program-no-leading-hai"]
       [(or (= (length m) 1)
            (not (second m)))
        "out-of-scope-hai-without-version"]
       [else
        (define v (string-downcase (second m)))
        (if (string=? v "1.3")
            "in-scope-1.3"
            (format "out-of-scope-version-~a" v))])]))

(define (first-meaningful-line-index lines)
  (let loop ([i 0] [in-block-comment? #f])
    (cond
      [(>= i (length lines)) #f]
      [else
       (define line (string-trim (list-ref lines i)))
       (cond
         [in-block-comment?
          (if (regexp-match? #px"(?i:\\bTLDR\\b)" line)
              (loop (+ i 1) #f)
              (loop (+ i 1) #t))]
         [(string=? line "")
          (loop (+ i 1) #f)]
         [(regexp-match? #px"^#!" line)
          (loop (+ i 1) #f)]
         [(regexp-match? #px"(?i:^OBTW\\b)" line)
          (if (regexp-match? #px"(?i:\\bTLDR\\b)" line)
              (loop (+ i 1) #f)
              (loop (+ i 1) #t))]
         [(regexp-match? #px"(?i:^BTW\\b)" line)
          (loop (+ i 1) #f)]
         [else i])])))

(define (promote-missing-version-source source)
  (define lines (regexp-split #px"\r\n|\n|\r" source))
  (define idx (first-meaningful-line-index lines))
  (cond
    [(not idx) (values source #f)]
    [else
     (define raw (list-ref lines idx))
     (define m (regexp-match #px"^([ \t]*)HAI[ \t]*$" raw))
     (if (not m)
         (values source #f)
         (let* ([indent (second m)]
                [updated-lines
                 (append
                  (list promotion-comment)
                  (for/list ([line (in-list lines)]
                             [i (in-naturals)])
                    (if (= i idx)
                        (string-append indent "HAI 1.3")
                        line)))]
                [promoted (string-join updated-lines "\n")])
           (values promoted #t)))]))

(define (hash-inc h k [n 1])
  (hash-set h k (+ n (hash-ref h k 0))))

(define (normalize-message msg)
  (if (and (string? msg) (not (string=? (string-trim msg) "")))
      (car (string-split (string-trim msg) "\n"))
      #f))

(define (classify-issue stage msg)
  (define m (or msg ""))
  (cond
    [(regexp-match? #px"unsupported version:" m)
     "out-of-scope-version"]
    [(regexp-match? #px"invalid identifier syntax: \".*\\?\"" m)
     "extension-import-like-identifier"]
    [(regexp-match? #px"invalid identifier syntax: \"//\"" m)
     "non-spec-line-comment-style"]
    [(regexp-match? #px"syntax error: unexpected OF" m)
     "likely-operator-spelling-drift"]
    [(regexp-match? #px"unknown slot:" m)
     "program-runtime-slot-miss"]
    [else
     (if (string=? stage "eval")
         "runtime-core-suspect"
         "parse-core-suspect")]))

(define statement-universe
  '(stmt-declare
    stmt-assign
    stmt-cast
    stmt-input
    stmt-visible
    stmt-loop
    stmt-if
    stmt-switch
    stmt-function-def
    stmt-return
    stmt-break
    stmt-object-def
    stmt-slot-set
    stmt-expr))

(define expr-universe
  '(expr-ident
    expr-number
    expr-string
    expr-literal
    expr-binary
    expr-unary
    expr-variadic
    expr-call
    expr-method-call
    expr-slot
    expr-srs
    expr-cast))

(define binary-op-universe
  '("SUM OF"
    "DIFF OF"
    "PRODUKT OF"
    "QUOSHUNT OF"
    "MOD OF"
    "BIGGR OF"
    "SMALLR OF"
    "BOTH OF"
    "EITHER OF"
    "WON OF"
    "BOTH SAEM"
    "DIFFRINT"))

(define unary-op-universe
  '("NOT"))

(define variadic-op-universe
  '("ALL OF" "ANY OF" "SMOOSH"))

(struct coverage (stmt-set
                  expr-set
                  binary-op-set
                  unary-op-set
                  variadic-op-set
                  branch-counts)
  #:transparent)

(define (make-coverage)
  (coverage (mutable-set)
            (mutable-set)
            (mutable-set)
            (mutable-set)
            (mutable-set)
            (make-hash)))

(define (cov-add-stmt! cov s)
  (set-add! (coverage-stmt-set cov) s))

(define (cov-add-expr! cov e)
  (set-add! (coverage-expr-set cov) e))

(define (cov-add-binary-op! cov op)
  (set-add! (coverage-binary-op-set cov) op))

(define (cov-add-unary-op! cov op)
  (set-add! (coverage-unary-op-set cov) op))

(define (cov-add-variadic-op! cov op)
  (set-add! (coverage-variadic-op-set cov) op))

(define (cov-inc-branch! cov key)
  (hash-set! (coverage-branch-counts cov)
             key
             (+ 1 (hash-ref (coverage-branch-counts cov) key 0))))

(define (visit-expr! cov e)
  (cond
    [(expr-ident? e)
     (cov-add-expr! cov 'expr-ident)]
    [(expr-number? e)
     (cov-add-expr! cov 'expr-number)]
    [(expr-string? e)
     (cov-add-expr! cov 'expr-string)]
    [(expr-literal? e)
     (cov-add-expr! cov 'expr-literal)]
    [(expr-binary? e)
     (cov-add-expr! cov 'expr-binary)
     (cov-add-binary-op! cov (expr-binary-op e))
     (visit-expr! cov (expr-binary-left e))
     (visit-expr! cov (expr-binary-right e))]
    [(expr-unary? e)
     (cov-add-expr! cov 'expr-unary)
     (cov-add-unary-op! cov (expr-unary-op e))
     (visit-expr! cov (expr-unary-arg e))]
    [(expr-variadic? e)
     (cov-add-expr! cov 'expr-variadic)
     (cov-add-variadic-op! cov (expr-variadic-op e))
     (for ([a (in-list (expr-variadic-args e))])
       (visit-expr! cov a))]
    [(expr-call? e)
     (cov-add-expr! cov 'expr-call)
     (for ([a (in-list (expr-call-args e))])
       (visit-expr! cov a))]
    [(expr-method-call? e)
     (cov-add-expr! cov 'expr-method-call)
     (cov-inc-branch! cov 'method-call-total)
     (visit-expr! cov (expr-method-call-receiver e))
     (for ([a (in-list (expr-method-call-args e))])
       (visit-expr! cov a))]
    [(expr-slot? e)
     (cov-add-expr! cov 'expr-slot)
     (visit-expr! cov (expr-slot-object e))
     (visit-expr! cov (expr-slot-slot e))]
    [(expr-srs? e)
     (cov-add-expr! cov 'expr-srs)
     (visit-expr! cov (expr-srs-expr e))]
    [(expr-cast? e)
     (cov-add-expr! cov 'expr-cast)
     (visit-expr! cov (expr-cast-expr e))]
    [else
     (void)]))

(define (visit-stmt! cov s)
  (cond
    [(stmt-declare? s)
     (cov-add-stmt! cov 'stmt-declare)
     (visit-expr! cov (stmt-declare-target s))
     (when (stmt-declare-init s)
       (visit-expr! cov (stmt-declare-init s)))]
    [(stmt-assign? s)
     (cov-add-stmt! cov 'stmt-assign)
     (visit-expr! cov (stmt-assign-target s))
     (visit-expr! cov (stmt-assign-expr s))]
    [(stmt-cast? s)
     (cov-add-stmt! cov 'stmt-cast)
     (visit-expr! cov (stmt-cast-target s))]
    [(stmt-input? s)
     (cov-add-stmt! cov 'stmt-input)
     (visit-expr! cov (stmt-input-target s))]
    [(stmt-visible? s)
     (cov-add-stmt! cov 'stmt-visible)
     (for ([e (in-list (stmt-visible-exprs s))])
       (visit-expr! cov e))]
    [(stmt-loop? s)
     (cov-add-stmt! cov 'stmt-loop)
     (cov-inc-branch! cov 'loop-total)
     (when (stmt-loop-update-op s)
       (cov-inc-branch! cov 'loop-with-update))
     (cond
       [(equal? (stmt-loop-cond-kind s) "TIL")
        (cov-inc-branch! cov 'loop-with-cond-til)]
       [(equal? (stmt-loop-cond-kind s) "WILE")
        (cov-inc-branch! cov 'loop-with-cond-wile)])
     (when (stmt-loop-cond-expr s)
       (visit-expr! cov (stmt-loop-cond-expr s)))
     (for ([inner (in-list (stmt-loop-body s))])
       (visit-stmt! cov inner))]
    [(stmt-if? s)
     (cov-add-stmt! cov 'stmt-if)
     (cov-inc-branch! cov 'if-total)
     (when (pair? (stmt-if-mebbe-branches s))
       (cov-inc-branch! cov 'if-with-mebbe))
     (when (pair? (stmt-if-else-branch s))
       (cov-inc-branch! cov 'if-with-else))
     (visit-expr! cov (stmt-if-condition s))
     (for ([inner (in-list (stmt-if-then-branch s))])
       (visit-stmt! cov inner))
     (for ([m (in-list (stmt-if-mebbe-branches s))])
       (visit-expr! cov (mebbe-branch-condition m))
       (for ([inner (in-list (mebbe-branch-body m))])
         (visit-stmt! cov inner)))
     (for ([inner (in-list (stmt-if-else-branch s))])
       (visit-stmt! cov inner))]
    [(stmt-switch? s)
     (cov-add-stmt! cov 'stmt-switch)
     (cov-inc-branch! cov 'switch-total)
     (when (pair? (stmt-switch-default s))
       (cov-inc-branch! cov 'switch-with-default))
     (visit-expr! cov (stmt-switch-subject s))
     (for ([c (in-list (stmt-switch-cases s))])
       (visit-expr! cov (switch-case-match c))
       (for ([inner (in-list (switch-case-body c))])
         (visit-stmt! cov inner)))
     (for ([inner (in-list (stmt-switch-default s))])
       (visit-stmt! cov inner))]
    [(stmt-function-def? s)
     (cov-add-stmt! cov 'stmt-function-def)
     (cov-inc-branch! cov 'function-total)
     (for ([inner (in-list (stmt-function-def-body s))])
       (visit-stmt! cov inner))]
    [(stmt-return? s)
     (cov-add-stmt! cov 'stmt-return)
     (visit-expr! cov (stmt-return-expr s))]
    [(stmt-break? s)
     (cov-add-stmt! cov 'stmt-break)]
    [(stmt-object-def? s)
     (cov-add-stmt! cov 'stmt-object-def)
     (cov-inc-branch! cov 'object-total)
     (for ([inner (in-list (stmt-object-def-body s))])
       (visit-stmt! cov inner))]
    [(stmt-slot-set? s)
     (cov-add-stmt! cov 'stmt-slot-set)
     (visit-expr! cov (stmt-slot-set-object s))
     (visit-expr! cov (stmt-slot-set-slot s))
     (visit-expr! cov (stmt-slot-set-expr s))]
    [(stmt-expr? s)
     (cov-add-stmt! cov 'stmt-expr)
     (visit-expr! cov (stmt-expr-expr s))]
    [else
     (void)]))

(define (visit-program! cov p)
  (for ([s (in-list (program-statements p))])
    (visit-stmt! cov s)))

(define (set->sorted-list s [less? symbol<?])
  (sort (set->list s) less?))

(define (set-of-strings->sorted-list s)
  (sort (set->list s) string<?))

(define (set-missing universe observed)
  (sort
   (filter (lambda (x) (not (set-member? observed x)))
           universe)
   (if (and (pair? universe) (symbol? (car universe)))
       symbol<?
       string<?)))

(define (scan-corpus files)
  (define original-class-counts (hash))
  (define effective-class-counts (hash))
  (define parse-error-counts (hash))
  (define lex-error-counts (hash))
  (define runtime-error-counts (hash))
  (define issue-triage-counts (hash))
  (define status-counts (hash))
  (define in-scope-cov (make-coverage))
  (define in-scope-ok-cov (make-coverage))
  (define in-scope-files '())
  (define in-scope-parse-ok-files '())
  (define in-scope-ok-files '())
  (define promoted-files '())
  (define sample-issues '())

  (for ([p (in-list files)])
    (define rel (path->display p))
    (define source (file->string p))
    (define original-cls (header-class source))
    (set! original-class-counts (hash-inc original-class-counts original-cls))
    (define effective-source source)
    (define effective-cls original-cls)
    (when (and promote-missing-version?
               (string=? original-cls "out-of-scope-hai-without-version"))
      (define-values (promoted-source promoted?)
        (promote-missing-version-source source))
      (when promoted?
        (set! effective-source promoted-source)
        (set! effective-cls "in-scope-1.3-promoted")
        (set! promoted-files (cons rel promoted-files))
        (when promoted-out-dir
          (define rel-under-corpus (find-relative-path corpus-root p))
          (define out-path (build-path promoted-out-dir rel-under-corpus))
          (make-directory* (path-only out-path))
          (call-with-output-file out-path
            (lambda (out) (display promoted-source out))
            #:exists 'replace))))
    (set! effective-class-counts (hash-inc effective-class-counts effective-cls))
    (cond
      [(and (not (string=? effective-cls "in-scope-1.3"))
            (not (string=? effective-cls "in-scope-1.3-promoted")))
       (void)]
      [else
       (set! in-scope-files (cons rel in-scope-files))
       (with-handlers ([exn:fail?
                        (lambda (e)
                         (define msg (normalize-message (exn-message e)))
                         (define triage (classify-issue "lex" msg))
                          (set! lex-error-counts (hash-inc lex-error-counts msg))
                         (set! issue-triage-counts (hash-inc issue-triage-counts triage))
                          (set! status-counts (hash-inc status-counts "lex-error"))
                          (set! sample-issues
                                (cons (hash 'path rel 'stage "lex" 'message msg 'triage triage) sample-issues)))])
         (lex-source effective-source)
         (define parsed
           (with-handlers ([exn:fail?
                            (lambda (e)
                              (define msg (normalize-message (exn-message e)))
                              (define triage (classify-issue "parse" msg))
                              (set! parse-error-counts (hash-inc parse-error-counts msg))
                              (set! issue-triage-counts (hash-inc issue-triage-counts triage))
                              (set! status-counts (hash-inc status-counts "parse-error"))
                              (set! sample-issues
                                    (cons (hash 'path rel 'stage "parse" 'message msg 'triage triage) sample-issues))
                              #f)])
             (parse-program effective-source)))
         (when parsed
           (set! in-scope-parse-ok-files (cons rel in-scope-parse-ok-files))
           (set! status-counts (hash-inc status-counts "parse-ok"))
           (visit-program! in-scope-cov parsed)
           (define result (run-program/report parsed))
           (define st (~a (hash-ref result 'status 'unknown)))
           (cond
             [(string=? st "ok")
              (set! in-scope-ok-files (cons rel in-scope-ok-files))
              (visit-program! in-scope-ok-cov parsed)]
             [(string=? st "runtime-error")
              (define msg
                (normalize-message
                 (hash-ref result 'error
                           (hash-ref result 'reason ""))))
              (define triage (classify-issue "eval" msg))
              (set! runtime-error-counts (hash-inc runtime-error-counts msg))
              (set! issue-triage-counts (hash-inc issue-triage-counts triage))
              (set! sample-issues
                    (cons (hash 'path rel 'stage "eval" 'message msg 'triage triage) sample-issues))]
             [else
              (void)])
           (set! status-counts (hash-inc status-counts st))))]))

  (hash 'original-class-counts original-class-counts
        'effective-class-counts effective-class-counts
        'status-counts status-counts
        'lex-error-counts lex-error-counts
        'parse-error-counts parse-error-counts
        'runtime-error-counts runtime-error-counts
        'issue-triage-counts issue-triage-counts
        'in-scope-files (reverse in-scope-files)
        'in-scope-parse-ok-files (reverse in-scope-parse-ok-files)
        'in-scope-ok-files (reverse in-scope-ok-files)
        'promoted-files (reverse promoted-files)
        'in-scope-cov in-scope-cov
        'in-scope-ok-cov in-scope-ok-cov
        'sample-issues (take (reverse sample-issues)
                             (min 40 (length sample-issues)))))

(define (scan-fixtures files)
  (define fixture-cov (make-coverage))
  (define parse-errors (hash))
  (define parsed-count 0)
  (for ([p (in-list files)])
    (define source (file->string p))
    (with-handlers ([exn:fail?
                     (lambda (e)
                       (define msg (normalize-message (exn-message e)))
                       (set! parse-errors (hash-inc parse-errors msg)))])
      (define parsed (parse-program source))
      (visit-program! fixture-cov parsed)
      (set! parsed-count (+ parsed-count 1))))
  (hash 'parsed-count parsed-count
        'parse-errors parse-errors
        'coverage fixture-cov))

(define (hash->sorted-kv h)
  (sort (hash->list h) > #:key cdr))

(define (counts->rows h)
  (for/list ([kv (in-list (hash->sorted-kv h))])
    (hash 'label (~a (car kv)) 'count (cdr kv))))

(define corpus-files
  (collect-lol-files corpus-root))

(define fixture-files
  (collect-lol-files fixtures-root))

(define corpus-scan
  (scan-corpus corpus-files))

(define fixture-scan
  (scan-fixtures fixture-files))

(define in-scope-cov
  (hash-ref corpus-scan 'in-scope-cov))

(define fixture-cov
  (hash-ref fixture-scan 'coverage))

(define stmt-missing-in-corpus
  (set-missing statement-universe (coverage-stmt-set in-scope-cov)))

(define expr-missing-in-corpus
  (set-missing expr-universe (coverage-expr-set in-scope-cov)))

(define binary-missing-in-corpus
  (set-missing binary-op-universe (coverage-binary-op-set in-scope-cov)))

(define unary-missing-in-corpus
  (set-missing unary-op-universe (coverage-unary-op-set in-scope-cov)))

(define variadic-missing-in-corpus
  (set-missing variadic-op-universe (coverage-variadic-op-set in-scope-cov)))

(define (set-difference-sorted set-a set-b less?)
  (sort (filter (lambda (x) (not (set-member? set-b x)))
                (set->list set-a))
        less?))

(define (symbol-list->string-list xs)
  (map ~a xs))

(define fixture-only-statements
  (set-difference-sorted (coverage-stmt-set fixture-cov)
                         (coverage-stmt-set in-scope-cov)
                         symbol<?))

(define fixture-only-expressions
  (set-difference-sorted (coverage-expr-set fixture-cov)
                         (coverage-expr-set in-scope-cov)
                         symbol<?))

(define report
  (hash
   'generated-at (date->string (current-date) #t)
   'paths (hash 'corpus-root (path->display corpus-root)
                'fixtures-root (path->display fixtures-root)
                'json-out (path->display json-out)
                'md-out (path->display md-out))
   'totals (hash 'corpus-files (length corpus-files)
                 'fixture-files (length fixture-files)
                 'in-scope-1.3-files (length (hash-ref corpus-scan 'in-scope-files))
                 'in-scope-parse-ok-files (length (hash-ref corpus-scan 'in-scope-parse-ok-files))
                 'in-scope-eval-ok-files (length (hash-ref corpus-scan 'in-scope-ok-files))
                 'promoted-missing-version-files (length (hash-ref corpus-scan 'promoted-files))
                 'fixture-parse-ok-files (hash-ref fixture-scan 'parsed-count))
   'original-class-counts (counts->rows (hash-ref corpus-scan 'original-class-counts))
   'effective-class-counts (counts->rows (hash-ref corpus-scan 'effective-class-counts))
   'status-counts (counts->rows (hash-ref corpus-scan 'status-counts))
   'lex-error-counts (counts->rows (hash-ref corpus-scan 'lex-error-counts))
   'parse-error-counts (counts->rows (hash-ref corpus-scan 'parse-error-counts))
   'runtime-error-counts (counts->rows (hash-ref corpus-scan 'runtime-error-counts))
   'issue-triage-counts (counts->rows (hash-ref corpus-scan 'issue-triage-counts))
   'coverage
   (hash
    'in-scope-statements (symbol-list->string-list
                          (set->sorted-list (coverage-stmt-set in-scope-cov)))
    'in-scope-expressions (symbol-list->string-list
                           (set->sorted-list (coverage-expr-set in-scope-cov)))
    'in-scope-binary-ops (set-of-strings->sorted-list (coverage-binary-op-set in-scope-cov))
    'in-scope-unary-ops (set-of-strings->sorted-list (coverage-unary-op-set in-scope-cov))
    'in-scope-variadic-ops (set-of-strings->sorted-list (coverage-variadic-op-set in-scope-cov))
    'missing-statements (symbol-list->string-list
                         (sort stmt-missing-in-corpus symbol<?))
    'missing-expressions (symbol-list->string-list
                          (sort expr-missing-in-corpus symbol<?))
    'missing-binary-ops (sort binary-missing-in-corpus string<?)
    'missing-unary-ops (sort unary-missing-in-corpus string<?)
    'missing-variadic-ops (sort variadic-missing-in-corpus string<?)
    'fixture-only-statements (symbol-list->string-list fixture-only-statements)
    'fixture-only-expressions (symbol-list->string-list fixture-only-expressions)
    'in-scope-branch-counts (counts->rows (coverage-branch-counts in-scope-cov))
    'fixture-branch-counts (counts->rows (coverage-branch-counts fixture-cov)))
   'sample-issues (hash-ref corpus-scan 'sample-issues)))

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

(make-directory* (path-only json-out))
(make-directory* (path-only md-out))

(call-with-output-file json-out
  (lambda (out)
    (write-json report out))
  #:exists 'replace)

(call-with-output-file md-out
  (lambda (out)
    (fprintf out "# Language Gap Report (Strict 1.3)\n\n")
    (fprintf out "Generated: `~a`\n\n" (hash-ref report 'generated-at))
    (fprintf out "- JSON source: `~a`\n\n" (path->display json-out))
    (define totals (hash-ref report 'totals))
    (fprintf out "## Totals\n\n")
    (fprintf out "- Corpus files: `~a`\n" (hash-ref totals 'corpus-files))
    (fprintf out "- In-scope 1.3 files: `~a`\n" (hash-ref totals 'in-scope-1.3-files))
    (fprintf out "- In-scope parse-ok files: `~a`\n" (hash-ref totals 'in-scope-parse-ok-files))
    (fprintf out "- In-scope eval-ok files: `~a`\n" (hash-ref totals 'in-scope-eval-ok-files))
    (fprintf out "- Promoted missing-version files: `~a`\n" (hash-ref totals 'promoted-missing-version-files))
    (fprintf out "- Fixture files: `~a`\n" (hash-ref totals 'fixture-files))
    (fprintf out "- Fixture parse-ok files: `~a`\n\n" (hash-ref totals 'fixture-parse-ok-files))

    (write-count-section out "Corpus Header Classes (Original)" (hash-ref report 'original-class-counts))
    (write-count-section out "Corpus Header Classes (Effective For Analysis)" (hash-ref report 'effective-class-counts))
    (write-count-section out "In-Scope 1.3 Status Counts" (hash-ref report 'status-counts))
    (write-count-section out "In-Scope Lex Errors" (hash-ref report 'lex-error-counts))
    (write-count-section out "In-Scope Parse Errors" (hash-ref report 'parse-error-counts))
    (write-count-section out "In-Scope Runtime Errors" (hash-ref report 'runtime-error-counts))
    (write-count-section out "In-Scope Issue Triage" (hash-ref report 'issue-triage-counts))

    (define cov (hash-ref report 'coverage))
    (write-list-section out "Missing Statement Forms In In-Scope Corpus"
                        (hash-ref cov 'missing-statements))
    (write-list-section out "Missing Expression Forms In In-Scope Corpus"
                        (hash-ref cov 'missing-expressions))
    (write-list-section out "Missing Binary Operators In In-Scope Corpus"
                        (hash-ref cov 'missing-binary-ops))
    (write-list-section out "Missing Unary Operators In In-Scope Corpus"
                        (hash-ref cov 'missing-unary-ops))
    (write-list-section out "Missing Variadic Operators In In-Scope Corpus"
                        (hash-ref cov 'missing-variadic-ops))
    (write-list-section out "Used In Fixtures But Not In In-Scope Corpus (Statements)"
                        (hash-ref cov 'fixture-only-statements))
    (write-list-section out "Used In Fixtures But Not In In-Scope Corpus (Expressions)"
                        (hash-ref cov 'fixture-only-expressions))
    (write-count-section out "In-Scope Branch Shape Counts"
                         (hash-ref cov 'in-scope-branch-counts))
    (write-count-section out "Fixture Branch Shape Counts"
                         (hash-ref cov 'fixture-branch-counts))

    (fprintf out "### Sample Issues\n\n")
    (for ([row (in-list (hash-ref report 'sample-issues))])
      (fprintf out "- `~a` (`~a`, triage=`~a`): `~a`\n"
               (hash-ref row 'path)
               (hash-ref row 'stage)
               (hash-ref row 'triage "n/a")
               (hash-ref row 'message)))
    (newline out))
  #:exists 'replace)

(printf "Wrote JSON report: ~a\n" (path->display json-out))
(printf "Wrote markdown report: ~a\n" (path->display md-out))
