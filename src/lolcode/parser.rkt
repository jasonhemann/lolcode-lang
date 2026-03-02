#lang racket/base

(require racket/list
         racket/match
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
       IF U SAY SO HOW IZ GIMMEH CAN
       VISIBLE AN BANG
       SUM OF DIFF PRODUKT QUOSHUNT MOD BIGGR SMALLR
       BOTH SAEM EITHER WON DIFFRINT NOT ALL ANY
       SMOOSH SRS MKAY
       MAEK IS NOW
       KTHX IM LIEK IN OUTTA IMIN IMOUTTA UPPIN NERFIN TIL WILE
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
        "GIMMEH" token-GIMMEH
        "CAN" token-CAN
        "VISIBLE" token-VISIBLE
        "AN" token-AN
        "AND" token-AN
        "!" token-BANG
        "SUM" token-SUM
        "OF" token-OF
        "DIFF" token-DIFF
        "DIFFERENCE" token-DIFF
        "DIFFRENCE" token-DIFF
        "PRODUKT" token-PRODUKT
        "QUOSHUNT" token-QUOSHUNT
        "QOUSHUNT" token-QUOSHUNT
        "MOD" token-MOD
        "BIGGR" token-BIGGR
        "SMALLR" token-SMALLR
        "BOTH" token-BOTH
        "SAEM" token-SAEM
        "EITHER" token-EITHER
        "WON" token-WON
        "DIFFRINT" token-DIFFRINT
        "NOT" token-NOT
        "ALL" token-ALL
        "ANY" token-ANY
        "SMOOSH" token-SMOOSH
        "SRS" token-SRS
        "MKAY" token-MKAY
        "MAEK" token-MAEK
        "IS" token-IS
        "NOW" token-NOW
        "KTHX" token-KTHX
        "IM" token-IM
        "LIEK" token-LIEK
        "IN" token-IN
        "OUTTA" token-OUTTA
        "IMIN" token-IMIN
        "IMOUTTA" token-IMOUTTA
        "UPPIN" token-UPPIN
        "NERFIN" token-NERFIN
        "TIL" token-TIL
        "WILE" token-WILE
        "'Z" token-SLOT))

(define current-source-lines (make-parameter #()))

(define supported-language-version "1.3")

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

(define (make-loop-stmt label-open label-close update cond body)
  (unless (string-ci=? label-open label-close)
    (error 'parse-source
           "loop label mismatch: ~a closed by ~a"
           label-open
           label-close))
  (stmt-loop label-open
             (car update)
             (cdr update)
             (car cond)
             (cdr cond)
             body))

(define (id->expr name)
  (cond
    [(string-ci=? name "WIN") (expr-literal #t)]
    [(string-ci=? name "FAIL") (expr-literal #f)]
    [(string-ci=? name "NOOB") (expr-literal 'NOOB)]
    [else (expr-ident name)]))

(define (switch-id->literal name)
  (define v (id->expr name))
  (if (expr-ident? v)
      (error 'parse-source
             "WTF? case literal must be NUMBER, STRING, WIN, FAIL, or NOOB; got ~a"
             name)
      v))

(define (call-target->expr target args)
  (match target
    [(list 'function name)
     (expr-call name args)]
    [(list 'namespace ns-name method-name)
     ;; Namespace/library calls like `I IZ STRING'Z LEN ...` compile to
     ;; function-name dispatch while we keep runtime library support separate.
     (expr-call (format "~a'Z ~a" ns-name method-name) args)]
    [_ (error 'parse-source "invalid call target: ~e" target)]))

(define (normalize-import-name lib)
  (if (and (positive? (string-length lib))
           (char=? (string-ref lib (- (string-length lib) 1)) #\?))
      (substring lib 0 (- (string-length lib) 1))
      lib))

(define (word-token-ci=? t text)
  (and (eq? (token-type t) 'WORD)
       (string-ci=? (token-lexeme t) text)))

(define (collapse-phrase-tokens raws [acc '()])
  (cond
    [(null? raws) (reverse acc)]
    [(and (pair? (cdr raws))
          (word-token-ci=? (car raws) "IM")
          (word-token-ci=? (cadr raws) "IN")
          (= (token-line (car raws))
             (token-line (cadr raws))))
     (define t (car raws))
     (collapse-phrase-tokens
      (cddr raws)
      (cons (token 'WORD "IMIN" (token-line t) (token-col t))
            acc))]
    [(and (pair? (cdr raws))
          (word-token-ci=? (car raws) "IM")
          (word-token-ci=? (cadr raws) "OUTTA")
          (= (token-line (car raws))
             (token-line (cadr raws))))
     (define t (car raws))
     (collapse-phrase-tokens
      (cddr raws)
      (cons (token 'WORD "IMOUTTA" (token-line t) (token-col t))
            acc))]
    [else
     (collapse-phrase-tokens
      (cdr raws)
      (cons (car raws) acc))]))

(define (line-has-legacy-variadic? line-toks)
  (cond
    [(or (null? line-toks) (null? (cdr line-toks))) #f]
    [(and (word-token-ci=? (car line-toks) "ALL")
          (word-token-ci=? (cadr line-toks) "OF"))
     #t]
    [(and (word-token-ci=? (car line-toks) "ANY")
          (word-token-ci=? (cadr line-toks) "OF"))
     #t]
    [else
     (line-has-legacy-variadic? (cdr line-toks))]))

(define (line-has-mkay? line-toks)
  (for/or ([t (in-list line-toks)])
    (word-token-ci=? t "MKAY")))

(define (inject-line-mkay line-toks)
  (if (and (pair? line-toks)
           (line-has-legacy-variadic? line-toks)
           (not (line-has-mkay? line-toks)))
      (let* ([last-tok (last line-toks)]
             [inserted
              (token 'WORD
                     "MKAY"
                     (token-line last-tok)
                     (+ (token-col last-tok)
                        (string-length (token-lexeme last-tok))
                        1))])
        (append line-toks (list inserted)))
      line-toks))

(define (insert-missing-mkay-tokens raws [line '()] [out '()])
  (cond
    [(null? raws)
     (append out (inject-line-mkay line))]
    [else
     (define t (car raws))
     (if (eq? (token-type t) 'NEWLINE)
         (insert-missing-mkay-tokens
          (cdr raws)
          '()
          (append out (inject-line-mkay line) (list t)))
         (insert-missing-mkay-tokens
          (cdr raws)
          (append line (list t))
          out))]))

(define (raw->token raw)
  (define ttype (token-type raw))
  (define lex (token-lexeme raw))
  (case ttype
    [(NEWLINE)
     (token-NEWLINE)]
    [(EOF)
     (token-EOF)]
    [(NUMBER)
     (token-NUMBER lex)]
    [(STRING)
     (token-STRING lex)]
    [(WORD)
     (define lex-upcase (string-upcase lex))
     (define ctor
       (if (or (string=? lex "a")
               (string=? lex "i"))
           #f
           (and (string=? lex lex-upcase)
                (hash-ref keyword-token-ctors lex-upcase #f))))
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
   (expected-SR-conflicts 49)
   (expected-RR-conflicts 51)
   (error
    (lambda (tok-ok? tok-name tok-value start-pos end-pos)
      (raise-parse-error tok-name tok-value start-pos)))
   (grammar
    (program
     [(nlopt HAI version nlopt statement-list-opt nlopt KTHXBYE nlopt)
      (program $3 $5)])

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
     [(loop-stmt) $1]
     [(non-loop-statement) $1])

    (non-loop-statement
     [(if-stmt) $1]
     [(switch-stmt) $1]
     [(function-stmt) $1]
     [(object-stmt) $1]
     [(declare-stmt) $1]
     [(assign-stmt) $1]
     [(cast-stmt) $1]
     [(input-stmt) $1]
     [(slot-set-stmt) $1]
     [(import-stmt) $1]
     [(visible-stmt) $1]
     [(return-stmt) $1]
     [(break-stmt) $1]
     [(expr-stmt) $1])

    (declare-stmt
     [(I HAS A declare-target declare-init-opt) (stmt-declare $4 $5)]
     [(I HAS declare-target declare-init-opt) (stmt-declare $3 $4)])

    (declare-target
     [(ident-token) (expr-ident $1)]
     [(SRS expr) (expr-srs $2)])

    (declare-init-opt
     [() #f]
     [(ITZ expr) $2]
     [(ITZ A ID) (expr-ident $3)])

    (assign-stmt
     [(expr R expr) (stmt-assign $1 $3)])

    (cast-stmt
     [(expr IS NOW A ID) (stmt-cast $1 $5)])

    (input-stmt
     [(GIMMEH expr) (stmt-input $2)])

    (import-stmt
     [(CAN HAS ID) (stmt-import (normalize-import-name $3))])

    (slot-set-stmt
     [(expr HAS A slot-target ITZ expr) (stmt-slot-set $1 $4 $6)]
     [(expr HAS A slot-target ITZ A ID) (stmt-slot-set $1 $4 (expr-ident $7))])

    (slot-target
     [(ident-token) (expr-ident $1)]
     [(SRS expr) (expr-srs $2)])

    (visible-stmt
     [(VISIBLE visible-args) (stmt-visible $2 #f)]
     [(VISIBLE visible-inline-args) (stmt-visible $2 #f)]
     [(VISIBLE visible-inline-args BANG) (stmt-visible $2 #t)]
     [(VISIBLE visible-args BANG) (stmt-visible $2 #t)])

    (visible-inline-args
     [(inline-arg inline-arg visible-inline-tail)
      (cons $1 (cons $2 $3))])

    (visible-inline-tail
     [() '()]
     [(inline-arg visible-inline-tail) (cons $1 $2)])

    (inline-arg
     [(NUMBER) (expr-number $1)]
     [(STRING) (expr-string $1)]
     [(ident-token) (id->expr $1)]
     [(SRS expr) (expr-srs $2)]
     [(I IZ call-target call-args MKAY) (call-target->expr $3 $4)])

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

    (loop-stmt
     [(IMIN YR ID loop-update-opt loop-cond-opt nlopt loop-body-opt IMOUTTA YR ID)
      (make-loop-stmt $3 $10 $4 $5 $7)])

    (loop-body-opt
     [() '()]
     [(loop-body-items) $1])

    (loop-body-items
     [(loop-body-item) (list $1)]
     [(loop-body-item loop-body-items) (cons $1 $2)])

    (loop-body-item
     [(statement nlopt) $1])

    (loop-update-opt
     [() (cons #f #f)]
     [(UPPIN YR ident-token) (cons $3 "UPPIN")]
     [(NERFIN YR ident-token) (cons $3 "NERFIN")])

    (loop-cond-opt
     [() (cons #f #f)]
     [(TIL expr) (cons "TIL" $2)]
     [(WILE expr) (cons "WILE" $2)])

    (case-list
     [(case) (list $1)]
     [(case-list case) (append $1 (list $2))])

    (case
     [(OMG case-literal nlopt statement-list-opt)
      (switch-case $2 $4)])

    (case-literal
     [(NUMBER) (expr-number $1)]
     [(STRING) (expr-string $1)]
     [(ID) (switch-id->literal $1)])

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

    (expr-stmt
     [(I IZ call-target call-args MKAY) (stmt-expr (call-target->expr $3 $4))]
     [(bin-expr) (stmt-expr $1)]
     [(logic-variadic-expr) (stmt-expr $1)]
     [(smoosh-expr) (stmt-expr $1)]
     [(NOT expr) (stmt-expr (expr-unary "NOT" $2))]
     [(MAEK expr A ID) (stmt-expr (expr-cast $2 $4))]
     [(MAEK expr ID) (stmt-expr (expr-cast $2 $3))])

    (expr
     [(simple-expr postfix-tail) ($2 $1)])

    (postfix-tail
     [() (lambda (base) base)]
     [(SLOT slot-ref postfix-tail)
      (lambda (base) ($3 (expr-slot base $2)))]
     [(IZ ID call-args MKAY postfix-tail)
      (lambda (base) ($5 (expr-method-call base $2 $3)))])

    (slot-ref
     [(ident-token) (id->expr $1)]
     [(SRS expr-no-postfix) (expr-srs $2)])

    (simple-expr
     [(NUMBER) (expr-number $1)]
     [(STRING) (expr-string $1)]
     [(ident-token) (id->expr $1)]
     [(SRS expr) (expr-srs $2)]
     [(NOT expr) (expr-unary "NOT" $2)]
     [(MAEK expr A ID) (expr-cast $2 $4)]
     [(MAEK expr ID) (expr-cast $2 $3)]
     [(I IZ call-target call-args MKAY) (call-target->expr $3 $4)]
     [(bin-expr) $1]
     [(logic-variadic-expr) $1]
     [(smoosh-expr) $1])

    (expr-no-postfix
     [(simple-expr) $1])

    (rhs-no-an
     [(ident-token postfix-tail) ($2 (id->expr $1))]
     [(NUMBER) (expr-number $1)]
     [(STRING) (expr-string $1)]
     [(SRS expr-no-postfix) (expr-srs $2)]
     [(NOT expr) (expr-unary "NOT" $2)]
     [(MAEK expr A ID) (expr-cast $2 $4)]
     [(MAEK expr ID) (expr-cast $2 $3)]
     [(I IZ call-target call-args MKAY) (call-target->expr $3 $4)]
     [(bin-expr) $1]
     [(logic-variadic-expr) $1]
     [(smoosh-expr) $1])

    (call-target
     [(ident-token) (list 'function $1)]
     [(ident-token SLOT ident-token) (list 'namespace $1 $3)])

    (ident-token
     [(ID) $1]
     [(SUM) "SUM"])

    (call-args
     [() '()]
     [(YR expr call-args-tail) (cons $2 $3)])

    (call-args-tail
     [() '()]
     [(AN YR expr call-args-tail) (cons $3 $4)])

    (bin-expr
     [(SUM OF expr AN expr) (expr-binary "SUM OF" $3 $5)]
     [(SUM OF expr rhs-no-an) (expr-binary "SUM OF" $3 $4)]
     [(DIFF OF expr AN expr) (expr-binary "DIFF OF" $3 $5)]
     [(DIFF OF expr rhs-no-an) (expr-binary "DIFF OF" $3 $4)]
     [(PRODUKT OF expr AN expr) (expr-binary "PRODUKT OF" $3 $5)]
     [(PRODUKT OF expr rhs-no-an) (expr-binary "PRODUKT OF" $3 $4)]
     [(QUOSHUNT OF expr AN expr) (expr-binary "QUOSHUNT OF" $3 $5)]
     [(QUOSHUNT OF expr rhs-no-an) (expr-binary "QUOSHUNT OF" $3 $4)]
     [(MOD OF expr AN expr) (expr-binary "MOD OF" $3 $5)]
     [(MOD OF expr rhs-no-an) (expr-binary "MOD OF" $3 $4)]
     [(BIGGR OF expr AN expr) (expr-binary "BIGGR OF" $3 $5)]
     [(BIGGR OF expr rhs-no-an) (expr-binary "BIGGR OF" $3 $4)]
     [(SMALLR OF expr AN expr) (expr-binary "SMALLR OF" $3 $5)]
     [(SMALLR OF expr rhs-no-an) (expr-binary "SMALLR OF" $3 $4)]
     [(BOTH OF expr AN expr) (expr-binary "BOTH OF" $3 $5)]
     [(BOTH OF expr rhs-no-an) (expr-binary "BOTH OF" $3 $4)]
     [(EITHER OF expr AN expr) (expr-binary "EITHER OF" $3 $5)]
     [(EITHER OF expr rhs-no-an) (expr-binary "EITHER OF" $3 $4)]
     [(WON OF expr AN expr) (expr-binary "WON OF" $3 $5)]
     [(WON OF expr rhs-no-an) (expr-binary "WON OF" $3 $4)]
     [(BOTH SAEM expr AN expr) (expr-binary "BOTH SAEM" $3 $5)]
     [(BOTH SAEM expr rhs-no-an) (expr-binary "BOTH SAEM" $3 $4)]
     [(DIFFRINT expr AN expr) (expr-binary "DIFFRINT" $2 $4)]
     [(DIFFRINT expr rhs-no-an) (expr-binary "DIFFRINT" $2 $3)])

    (logic-variadic-expr
     [(ALL OF expr logic-tail MKAY) (expr-variadic "ALL OF" (cons $3 $4))]
     [(ANY OF expr logic-tail MKAY) (expr-variadic "ANY OF" (cons $3 $4))])

    (logic-tail
     [() '()]
     [(AN expr logic-tail) (cons $2 $3)]
     [(expr logic-tail) (cons $1 $2)])

    (smoosh-expr
     [(SMOOSH expr smoosh-tail maybe-mkay) (expr-variadic "SMOOSH" (cons $2 $3))]
     [(SMOOSH expr expr smoosh-tail maybe-mkay)
      (expr-variadic "SMOOSH" (cons $2 (cons $3 $4)))])

    (smoosh-tail
     [() '()]
     [(AN expr smoosh-tail) (cons $2 $3)])

    (maybe-mkay
     [() (void)]
     [(MKAY) (void)]))))

(define (parse-source source)
  (unless (string? source)
    (raise-argument-error 'parse-source "string?" source))
  (define normalized-raws
    (insert-missing-mkay-tokens
     (collapse-phrase-tokens (lex-source source))))
  (define toks
    (map raw->position-token normalized-raws))
  (define idx 0)
  (define n (length toks))
  (define (next-token)
    (define t (list-ref toks idx))
    (when (< idx (- n 1))
      (set! idx (+ idx 1)))
    t)
  (define parsed
    (parameterize ([current-source-lines
                    (list->vector (string-split source "\n" #:trim? #f))])
      (parse/internal next-token)))
  (unless (string=? (program-version parsed) supported-language-version)
    (error 'parse-source
           "unsupported version: ~a (this implementation only accepts HAI ~a)"
           (program-version parsed)
           supported-language-version))
  parsed)
