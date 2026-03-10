#lang racket/base

(require racket/cmdline
         racket/file
         racket/list
         racket/match
         racket/path
         racket/port
         racket/string)

(define (repo-root)
  (simplify-path (current-directory)))

(define default-map
  (build-path (repo-root) "spec" "traceability" "RESOLUTION_MAP.md"))
(define default-ledger
  (build-path (repo-root) "spec" "traceability" "ADJUDICATION_LEDGER.md"))
(define default-out
  (build-path (repo-root) "spec" "traceability" "TEST_ANCHOR_INDEX.md"))

(define map-path default-map)
(define ledger-path default-ledger)
(define out-path default-out)

(command-line
 #:program "generate_nxx_test_anchors.rkt"
 #:once-each
 [("--map") p "Path to RESOLUTION_MAP markdown" (set! map-path (string->path p))]
 [("--ledger") p "Path to adjudication ledger markdown" (set! ledger-path (string->path p))]
 [("--out") p "Output markdown path" (set! out-path (string->path p))])

(define (must-read-lines p who)
  (unless (file-exists? p)
    (error who "missing file: ~a" p))
  (file->lines p))

(define map-lines (must-read-lines map-path 'generate_nxx_test_anchors))
(define ledger-lines (must-read-lines ledger-path 'generate_nxx_test_anchors))

(define (extract-ids lines)
  (for/list ([ln (in-list lines)]
             #:when (regexp-match? #px"^\\| `N[0-9][0-9]` " ln))
    (define m (regexp-match #px"`(N[0-9][0-9])`" ln))
    (if m
        (second m)
        #f)))

(define ids
  (remove-duplicates (filter values (extract-ids map-lines)) string=?))

(define (find-ledger-line id)
  (for/first ([ln (in-list ledger-lines)]
              [idx (in-naturals 1)]
              #:when (regexp-match? (pregexp (format "^\\| `~a` \\|" id)) ln))
    (list idx ln)))

(define (token-allowed? tok id)
  (and (not (string=? tok id))
       (not (string=? tok "-"))
       (regexp-match? #px"^[A-Za-z0-9][A-Za-z0-9-]*$" tok)
       (regexp-match? #px"-" tok)
       (not (regexp-match? #px"\\.md$|\\.rktd$" tok))
       (not (regexp-match? #px"^N[0-9][0-9]$" tok))
       (not (regexp-match? #px"^C[0-9]$" tok))
       (not (regexp-match? #px"^C[0-9]/" tok))
       (not (member tok '("HAI" "BUKKIT" "NOOB" "IT" "SRS" "ME" "WTF?" "O RLY?")))))

(define (extract-anchor-tokens line id)
  (define raw
    (for/list ([m (in-list (regexp-match* #px"`([^`]+)`" line #:match-select second))])
      m))
  (remove-duplicates
   (filter (lambda (tok) (token-allowed? tok id)) raw)
   string=?))

(define (anchors->text anchors)
  (if (null? anchors)
      "(none explicit in ledger row)"
      (string-join anchors ", ")))

(define (emit-row out id)
  (define maybe (find-ledger-line id))
  (match maybe
    [(list line-no line-text)
     (define anchors (extract-anchor-tokens line-text id))
     (fprintf out
              "| `~a` | ~a | [ADJUDICATION_LEDGER.md:line ~a](./ADJUDICATION_LEDGER.md#L~a) |\n"
              id
              (anchors->text anchors)
              line-no
              line-no)]
    [_ (fprintf out "| `~a` | (no ledger row found) | (missing) |\n" id)]))

(make-parent-directory* out-path)
(call-with-output-file out-path
  (lambda (out)
    (fprintf out "# Nxx Test Anchor Ledger\n\n")
    (fprintf out "Source-of-truth extraction: `~a` adjudication rows.\n"
             (path->string (path->complete-path ledger-path)))
    (fprintf out "This file provides direct named regression anchors for each `Nxx` item in the resolution map.\n\n")
    (fprintf out "| ID | Test anchors | Source |\n")
    (fprintf out "|---|---|---|\n")
    (for ([id (in-list ids)])
      (emit-row out id)))
  #:exists 'truncate/replace)

(displayln (format "wrote ~a" (path->string out-path)))
