#lang racket/base

(require racket/list
         racket/string
         (only-in parser-tools/lex
                  define-tokens
                  define-empty-tokens
                  make-position
                  make-position-token
                  position-line
                  position-col)
         parser-tools/yacc
         "ast.rkt"
         "lexer.rkt")

(provide parse-source)

(define-tokens value-tokens (ID NUMBER STRING))

(define-empty-tokens op-tokens
  (HAI KTHXBYE NEWLINE EOF
       I HAS A R ITZ O RLY RLYQ YA NO WAI OIC MEBBE
       WTFQ OMG OMGWTF GTFO FOUND YR
       IF U SAY SO HOW IZ
       VISIBLE AN
       SUM OF DIFF PRODUKT QUOSHUNT MOD BIGGR SMALLR BOTH SAEM DIFFRINT
       SMOOSH SRS MKAY
       KTHX IM LIEK
       SLOT))

(define keyword-token-ctors
  (hash "HAI" token-HAI
        "KTHXBYE" token-KTHXBYE
        "I" token-I
        "HAS" token-HAS
        "A" token-A
        "R" token-R
        "ITZ" token-ITZ
        "O" token-O
        "RLY" token-RLY
        "RLY?" token-RLYQ
        "YA" token-YA
        "NO" token-NO
        "WAI" token-WAI
        "OIC" token-OIC
        "MEBBE" token-MEBBE
        "WTF?" token-WTFQ
        "OMG" token-OMG
        "OMGWTF" token-OMGWTF
        "GTFO" token-GTFO
        "FOUND" token-FOUND
        "YR" token-YR
        "IF" token-IF
        "U" token-U
        "SAY" token-SAY
        "SO" token-SO
        "HOW" token-HOW
        "IZ" token-IZ
        "VISIBLE" token-VISIBLE
        "AN" token-AN
        "SUM" token-SUM
        "OF" token-OF
        "DIFF" token-DIFF
        "PRODUKT" token-PRODUKT
        "QUOSHUNT" token-QUOSHUNT
        "MOD" token-MOD
        "BIGGR" token-BIGGR
        "SMALLR" token-SMALLR
        "BOTH" token-BOTH
        "SAEM" token-SAEM
        "DIFFRINT" token-DIFFRINT
        "SMOOSH" token-SMOOSH
        "SRS" token-SRS
        "MKAY" token-MKAY
        "KTHX" token-KTHX
        "IM" token-IM
        "LIEK" token-LIEK
        "'Z" token-SLOT))

(define current-source-lines (make-parameter #()))

(define (token-label tok-name tok-value)
  (cond
    [(eq? tok-name 'EOF) "EOF"]
    [(and tok-name tok-value) (format "~a (~v)" tok-name tok-value)]
    [tok-name (format "~a" tok-name)]
    [else "unknown token"]))

(define (source-line-text line)
  (define lines (current-source-lines))
  (if (and (vector? lines)
           (<= 1 line)
           (<= line (vector-length lines)))
      (vector-ref lines (- line 1))
      #f))

(define (source-caret col line-text)
  (define line-len (string-length line-text))
  (define caret-col (min (max 1 col) (+ line-len 1)))
  (string-append (make-string (max 0 (- caret-col 1)) #\space) "^"))

(define (raise-parse-error tok-name tok-value start-pos)
  (define line (if start-pos (position-line start-pos) 0))
  (define col (if start-pos (position-col start-pos) 0))
  (define unexpected (token-label tok-name tok-value))
  (define raw-line-text (source-line-text line))
  (define line-text
    (cond
      [(and raw-line-text (not (string=? raw-line-text "")))
       raw-line-text]
      [(eq? tok-name 'EOF)
       "<end of input>"]
      [else
       #f]))
  (define context-fragment
    (if line-text
        (format "\n  ~a\n  ~a" line-text (source-caret col line-text))
        ""))
  (define hint-fragment
    (if (eq? tok-name 'EOF)
        "\n  hint: input ended early; check for a missing KTHXBYE or closing clause."
        ""))
  (error 'parse-source
         "syntax error: unexpected ~a at line ~a, col ~a~a~a"
         unexpected
         line
         col
         context-fragment
         hint-fragment))

(define (raw->token raw)
  (define ttype (token-type raw))
  (define lex (token-lexeme raw))
  (cond
    [(eq? ttype 'NEWLINE) (token-NEWLINE)]
    [(eq? ttype 'EOF) (token-EOF)]
    [(eq? ttype 'NUMBER) (token-NUMBER lex)]
    [(eq? ttype 'STRING) (token-STRING lex)]
    [(eq? ttype 'WORD)
     (define ctor (hash-ref keyword-token-ctors (string-upcase lex) #f))
     (if ctor
         (ctor)
         (token-ID lex))]
    [else
     (error 'parse-source "unknown lexer token type: ~a" ttype)]))

(define (raw->position-token raw)
  (define line (token-line raw))
  (define col (token-col raw))
  (define len (max 1 (string-length (token-lexeme raw))))
  (define start (make-position 0 line col))
  (define end (make-position 0 line (+ col len)))
  (make-position-token (raw->token raw) start end))

(define parse/internal
  (parser
   (start program)
   (end EOF)
   (tokens value-tokens op-tokens)
   (src-pos)
   (expected-SR-conflicts 12)
   (expected-RR-conflicts 0)
   (error
    (lambda (tok-ok? tok-name tok-value start-pos end-pos)
      (raise-parse-error tok-name tok-value start-pos)))
   (grammar
    (program
     [(HAI version nlopt statement-list-opt nlopt KTHXBYE nlopt)
      (program $2 $4)])

    (version
     [(NUMBER) $1]
     [(ID) $1])

    (nlopt
     [() (void)]
     [(nls) (void)])

    (nls
     [(NEWLINE) (void)]
     [(NEWLINE nls) (void)])

    (statement-list-opt
     [() '()]
     [(statement-items) $1])

    (statement-items
     [(statement-item) (list $1)]
     [(statement-item statement-items) (cons $1 $2)])

    (statement-item
     [(statement nlopt) $1])

    (statement
     [(if-stmt) $1]
     [(switch-stmt) $1]
     [(function-stmt) $1]
     [(object-stmt) $1]
     [(declare-stmt) $1]
     [(assign-stmt) $1]
     [(slot-set-stmt) $1]
     [(visible-stmt) $1]
     [(return-stmt) $1]
     [(break-stmt) $1])

    (declare-stmt
     [(I HAS A declare-target declare-init-opt) (stmt-declare $4 $5)]
     [(I HAS declare-target declare-init-opt) (stmt-declare $3 $4)])

    (declare-target
     [(ID) (expr-ident $1)]
     [(SRS expr) (expr-srs $2)])

    (declare-init-opt
     [() #f]
     [(ITZ expr) $2]
     [(ITZ A ID) (expr-ident $3)])

    (assign-stmt
     [(expr R expr) (stmt-assign $1 $3)])

    (slot-set-stmt
     [(expr HAS A slot-target ITZ expr) (stmt-slot-set $1 $4 $6)])

    (slot-target
     [(ID) (expr-ident $1)]
     [(SRS expr) (expr-srs $2)])

    (visible-stmt
     [(VISIBLE visible-args) (stmt-visible $2 #f)])

    (visible-args
     [(expr) (list $1)]
     [(expr AN visible-args) (cons $1 $3)])

    (if-stmt
     [(expr nlopt O RLYQ nlopt YA RLY nlopt statement-list-opt mebbe-list else-opt OIC)
      (stmt-if $1 $9 $10 $11)]
     [(O RLYQ nlopt YA RLY nlopt statement-list-opt mebbe-list else-opt OIC)
      (stmt-if (expr-ident "IT") $7 $8 $9)])

    (mebbe-list
     [() '()]
     [(mebbe-list MEBBE expr nlopt statement-list-opt)
      (append $1 (list (mebbe-branch $3 $5)))])

    (else-opt
     [() '()]
     [(NO WAI nlopt statement-list-opt) $4])

    (switch-stmt
     [(expr nlopt WTFQ nlopt case-list default-opt OIC)
      (stmt-switch $1 $5 $6)]
     [(WTFQ nlopt case-list default-opt OIC)
      (stmt-switch (expr-ident "IT") $3 $4)])

    (case-list
     [(case) (list $1)]
     [(case-list case) (append $1 (list $2))])

    (case
     [(OMG expr nlopt statement-list-opt)
      (switch-case $2 $4)])

    (default-opt
     [() '()]
     [(OMGWTF nlopt statement-list-opt) $3])

    (function-stmt
     [(HOW IZ I ID arg-def-opt nlopt statement-list-opt IF U SAY SO)
      (stmt-function-def $4 $5 $7)])

    (arg-def-opt
     [() '()]
     [(YR ID arg-def-more) (cons $2 $3)])

    (arg-def-more
     [() '()]
     [(AN YR ID arg-def-more) (cons $3 $4)])

    (object-stmt
     [(O HAI IM ID object-parent-opt nlopt statement-list-opt KTHX)
      (stmt-object-def $4 $5 $7)])

    (object-parent-opt
     [() #f]
     [(IM LIEK ID) $3])

    (return-stmt
     [(FOUND YR expr) (stmt-return $3)])

    (break-stmt
     [(GTFO) (stmt-break)])

    (expr
     [(simple-expr postfix-tail) ($2 $1)])

    (postfix-tail
     [() (lambda (base) base)]
     [(SLOT slot-ref postfix-tail)
      (lambda (base) ($3 (expr-slot base $2)))]
     [(IZ ID call-args MKAY postfix-tail)
      (lambda (base) ($5 (expr-method-call base $2 $3)))])

    (slot-ref
     [(ID) (expr-ident $1)]
     [(SRS expr) (expr-srs $2)])

    (simple-expr
     [(NUMBER) (expr-number $1)]
     [(STRING) (expr-string $1)]
     [(ID) (expr-ident $1)]
     [(SRS expr) (expr-srs $2)]
     [(I IZ ID call-args MKAY) (expr-call $3 $4)]
     [(bin-expr) $1]
     [(smoosh-expr) $1])

    (call-args
     [() '()]
     [(YR expr call-args-tail) (cons $2 $3)])

    (call-args-tail
     [() '()]
     [(AN YR expr call-args-tail) (cons $3 $4)])

    (an-opt
     [() (void)]
     [(AN) (void)])

    (bin-expr
     [(SUM OF expr an-opt expr) (expr-binary "SUM OF" $3 $5)]
     [(DIFF OF expr an-opt expr) (expr-binary "DIFF OF" $3 $5)]
     [(PRODUKT OF expr an-opt expr) (expr-binary "PRODUKT OF" $3 $5)]
     [(QUOSHUNT OF expr an-opt expr) (expr-binary "QUOSHUNT OF" $3 $5)]
     [(MOD OF expr an-opt expr) (expr-binary "MOD OF" $3 $5)]
     [(BIGGR OF expr an-opt expr) (expr-binary "BIGGR OF" $3 $5)]
     [(SMALLR OF expr an-opt expr) (expr-binary "SMALLR OF" $3 $5)]
     [(BOTH SAEM expr an-opt expr) (expr-binary "BOTH SAEM" $3 $5)]
     [(DIFFRINT expr an-opt expr) (expr-binary "DIFFRINT" $2 $4)])

    (smoosh-expr
     [(SMOOSH expr smoosh-tail maybe-mkay) (expr-variadic "SMOOSH" (cons $2 $3))])

    (smoosh-tail
     [() '()]
     [(AN expr smoosh-tail) (cons $2 $3)])

    (maybe-mkay
     [() (void)]
     [(MKAY) (void)]))))

(define (parse-source source)
  (unless (string? source)
    (raise-argument-error 'parse-source "string?" source))
  (define toks (map raw->position-token (lex-source source)))
  (define idx 0)
  (define n (length toks))
  (define (next-token)
    (define t (list-ref toks idx))
    (when (< idx (- n 1))
      (set! idx (+ idx 1)))
    t)
  (parameterize ([current-source-lines
                  (list->vector (string-split source "\n" #:trim? #f))])
    (parse/internal next-token)))
