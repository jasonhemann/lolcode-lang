#lang racket/base

(require racket/list
         racket/match
         racket/set
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
         "format-placeholder.rkt"
         "lexer.rkt")

(provide parse-source)

(define-tokens value-tokens (ID NUMBER STRING))

(define-empty-tokens op-tokens
  (HAI KTHXBYE NEWLINE EOF
       I HAS A R ITZ O RLY RLYQ YA NO WAI OIC MEBBE
       WTFQ OMG OMGWTF GTFO FOUND YR
       IF U SAY SO HOW IZ DUZ GIMMEH
       VISIBLE AN BANG
       SUM OF DIFF PRODUKT QUOSHUNT MOD BIGGR SMALLR
       BOTH SAEM EITHER WON DIFFRINT NOT ALL ANY
       SMOOSH SRS MKAY
       MAEK IS NOW
       KTHX IM LIEK IN OUTTA IMIN IMOUTTA UPPIN NERFIN TIL WILE
       SLOT))

(define keyword-token-ctors
  (hash
        "!" token-BANG
        "-" token-SLOT
        "'Z" token-SLOT
        "A" token-A
        "ALL" token-ALL
        "AN" token-AN
        "ANY" token-ANY
        "BIGGR" token-BIGGR
        "BOTH" token-BOTH
        "DIFF" token-DIFF
        "DIFFRINT" token-DIFFRINT
        "DUZ" token-DUZ
        "EITHER" token-EITHER
        "FOUND" token-FOUND
        "GIMMEH" token-GIMMEH
        "GTFO" token-GTFO
        "HAI" token-HAI
        "HAS" token-HAS
        "HOW" token-HOW
        "I" token-I
        "IF" token-IF
        "IM" token-IM
        "IMIN" token-IMIN
        "IMOUTTA" token-IMOUTTA
        "IN" token-IN
        "IS" token-IS
        "ITZ" token-ITZ
        "IZ" token-IZ
        "KTHX" token-KTHX
        "KTHXBYE" token-KTHXBYE
        "LIEK" token-LIEK
        "MAEK" token-MAEK
        "MEBBE" token-MEBBE
        "MKAY" token-MKAY
        "MOD" token-MOD
        "NERFIN" token-NERFIN
        "NO" token-NO
        "NOT" token-NOT
        "NOW" token-NOW
        "O" token-O
        "OF" token-OF
        "OIC" token-OIC
        "OMG" token-OMG
        "OMGWTF" token-OMGWTF
        "OUTTA" token-OUTTA
        "PRODUKT" token-PRODUKT
        "QUOSHUNT" token-QUOSHUNT
        "R" token-R
        "RLY" token-RLY
        "RLY?" token-RLYQ
        "SAEM" token-SAEM
        "SAY" token-SAY
        "SMALLR" token-SMALLR
        "SMOOSH" token-SMOOSH
        "SO" token-SO
        "SRS" token-SRS
        "SUM" token-SUM
        "TIL" token-TIL
        "U" token-U
        "UPPIN" token-UPPIN
        "VISIBLE" token-VISIBLE
        "WAI" token-WAI
        "WILE" token-WILE
        "WON" token-WON
        "WTF?" token-WTFQ
        "YA" token-YA
        "YR" token-YR
))

(define current-source-lines (make-parameter #()))

(define supported-language-version "1.3")

(define identifier-token-rx #px"^[A-Za-z][A-Za-z0-9_]*$")

(define (valid-identifier-token? text) (regexp-match? identifier-token-rx text))

(define (ensure-identifier-token who text)
  (unless (valid-identifier-token? text)
    (error who "invalid identifier syntax: ~v" text))
  text)

(define cast-target-types (set "TROOF" "YARN" "NUMBR" "NUMBAR" "NOOB"))

(define declaration-default-types (set "TROOF" "YARN" "NUMBR" "NUMBAR" "NOOB" "BUKKIT"))

(define (ensure-cast-target-type who text)
  (unless (set-member? cast-target-types text)
    (error who
           "invalid cast target type: ~a (expected TROOF, YARN, NUMBR, NUMBAR, or NOOB)"
           text))
  text)

(define (ensure-declaration-default-type who text)
  (unless (set-member? declaration-default-types text)
    (error who
           (string-append
            "invalid declaration type in ITZ A: ~a "
            "(expected TROOF, YARN, NUMBR, NUMBAR, NOOB, or BUKKIT)")
           text))
  text)

(define (token-label tok-name tok-value)
  (cond
    [(eq? tok-name 'EOF) "EOF"]
    [(and tok-name tok-value) (format "~a (~v)" tok-name tok-value)]
    [tok-name (format "~a" tok-name)]
    [else "unknown token"]))

(define (source-line-text line)
  (define lines (current-source-lines))
  (and (vector? lines)
       (<= 1 line)
       (<= line (vector-length lines))
       (vector-ref lines (- line 1))))

(define source-line-split-rx #px"\r\n|\n|\r")

(define program-opener-rx #px"^\\s*HAI(?:\\s|$)")
(define kthxbye-inline-tail-rx #px"^\\s*(?:BTW.*)?$")

(define (source->line-vector source)
  (list->vector (string-split source source-line-split-rx #:trim? #f)))

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
      [(and raw-line-text (not (string=? raw-line-text ""))) raw-line-text]
      [(eq? tok-name 'EOF) "<end of input>"]
      [else #f]))
  (define context-fragment
    (if line-text
        (format "\n  ~a\n  ~a" line-text (source-caret col line-text))
        ""))
  (error 'parse-source
         "syntax error: unexpected ~a at line ~a, col ~a~a"
         unexpected
         line
         col
         context-fragment))

(define (make-loop-stmt label-open label-close update condtn body)
  (define open-static
    (match label-open
      [(expr-literal (? string? s)) s]
      [_ #f]))
  (define close-static
    (match label-close
      [(expr-literal (? string? s)) s]
      [_ #f]))
  (when (and open-static close-static (not (string=? open-static close-static)))
    (error 'parse-source
           "loop label mismatch: ~a closed by ~a"
           open-static
           close-static))
  (match-define (cons update-var update-op) update)
  (match-define (cons cond-kind cond-expr) condtn)
  (stmt-loop label-open label-close update-var update-op cond-kind cond-expr body))

(define (id->expr name)
  (cond
    [(string=? name "WIN") (expr-literal #t)]
    [(string=? name "FAIL") (expr-literal #f)]
    [(string=? name "NOOB") (expr-literal 'NOOB)]
    [(or (string=? name "NUMBR")
         (string=? name "NUMBAR")
         (string=? name "YARN")
         (string=? name "TROOF")
         (string=? name "TYPE"))
     (expr-literal name)]
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
    [(list 'function name) (expr-call name args)]
    [(list 'method receiver method-name)
     ;; Method-call syntax remains distinct from ordinary I IZ function calls.
     (expr-method-call receiver method-name args)]
    [_ (error 'parse-source "invalid call target: ~e" target)]))

(define (slot-name-spec->expr spec)
  (match spec
    [(expr-literal (? string? name)) (expr-ident name)]
    [(expr-literal _) (error 'parse-source "invalid slot name spec literal: ~e" spec)]
    [(? string? name) (expr-ident name)]
    [(and s (expr-srs _)) s]
    [else (error 'parse-source "invalid slot name spec: ~e" spec)]))

(define (build-slot-chain base slot-name-specs)
  (for/fold ([obj base]) ([slot-spec (in-list slot-name-specs)])
    (expr-slot obj (slot-name-spec->expr slot-spec))))

(define (call-slot-chain->target base slot-name-specs)
  (unless (pair? slot-name-specs)
    (error 'parse-source "invalid call slot chain"))
  (match-define-values (receiver-slot-specs (list method-name-spec))
    (split-at-right slot-name-specs 1))
  (define receiver (build-slot-chain base receiver-slot-specs))
  (list 'method receiver method-name-spec))

(define (call-target-from-ident name maybe-slots)
  (if maybe-slots
      (call-slot-chain->target (id->expr name) maybe-slots)
      (list 'function (expr-literal name))))

(define (loop-update->spec target var-name)
  (match target
    [(list 'function fn-name) (cons var-name (list 'call fn-name))]
    [_ (error 'parse-source
              "loop updater call must target a function name, got ~e"
              target)]))

(define (make-slot-set-stmt target slot maybe-init)
  (cond
    [maybe-init
     (stmt-slot-set target slot maybe-init)]
    [(and (expr-ident? target)
          (string=? (expr-ident-name target) "ME"))
     (stmt-slot-set target slot (expr-literal 'NOOB))]
    [else
     (error 'parse-source
            "slot declaration without ITZ is only allowed as ME HAS A <slotname>")]))

(define (switch-string->literal text)
  (define template (ensure-yarn-template text))
  (when (yarn-template-has-placeholders? template)
    (error 'parse-source
           "WTF? case literal cannot contain YARN interpolation (:{...})"))
  (expr-string template))

(define (switch-literal-key expr)
  (match expr
    [(expr-number text) (list 'NUM (or (string->number text) text))]
    [(expr-string text) (list 'YARN (yarn-template-static-text text))]
    [(expr-literal value) (list 'LIT value)]
    [_ #f]))

(define (switch-literal-duplicate? a b)
  (match* (a b)
    [((list 'NUM na) (list 'NUM nb)) (= na nb)]
    [(_ _) (equal? a b)]))

(define (validate-switch-case-literals cases)
  (void
    (for/fold ([seen '()])
              ([c (in-list cases)])
      (match-define (switch-case case-match _case-body) c)
      (cond
        [(switch-literal-key case-match) =>
         (lambda (key)
            (when (for/or ([prior (in-list seen)])
                    (switch-literal-duplicate? prior key))
              (error 'parse-source
                     "duplicate OMG literal in WTF?: ~e"
                     case-match))
            (cons key seen))]
        [else seen]))))

(define (word-token=? text t)
  (match t
    [(token 'WORD lexeme _ _) (string=? lexeme text)]
    [_ #f]))

(define (collapse-phrase-tokens raws [acc '()])
  (match raws
    ['() (reverse acc)]

    [(cons (token 'WORD "IM" line col) (cons (token 'WORD "IN" line2 _) rst))
     #:when (= line line2)
     (collapse-phrase-tokens rst (cons (token 'WORD "IMIN" line col) acc))]

    [(cons (token 'WORD "IM" line col) (cons (token 'WORD "OUTTA" line2 _) rst))
     #:when (= line line2)
     (collapse-phrase-tokens rst (cons (token 'WORD "IMOUTTA" line col) acc))]

    [(cons t rst) (collapse-phrase-tokens rst (cons t acc))]))

(define (raw->token raw)
  (match raw
    [(token 'NEWLINE _ _ _) (token-NEWLINE)]
    [(token 'EOF _ _ _) (token-EOF)]
    [(token 'NUMBER lex _ _) (token-NUMBER lex)]
    [(token 'STRING lex _ _) (token-STRING lex)]
    [(token 'WORD lex _ _)
     (cond
       [(hash-ref keyword-token-ctors lex #f)
        => (lambda (ctor) (ctor))]
       [else (token-ID lex)])]
    [(token ttype _ _ _)
     (error 'parse-source "unknown lexer token type: ~a" ttype)]))

(define (raw->position-token raw)
  (match-define (token _ lexeme line col) raw)
  (define len
    (match lexeme
      [(? string? s) (max 1 (string-length s))]
      [(? yarn-template? yt) (max 1 (yarn-template-source-length yt))]
      [_ 1]))
  (define start (make-position 0 line col))
  (define end (make-position 0 line (+ col len)))
  (make-position-token (raw->token raw) start end))

(define parse/internal
  (parser
   (start program)
   (end EOF)
   (tokens value-tokens op-tokens)
   (src-pos)
   (expected-SR-conflicts 131)
   (expected-RR-conflicts 0)
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
     [(NEWLINE nlopt) (void)])

    (statement-list-opt
     [() '()]
     [(statement-items) $1])

    (statement-items
     [(statement-item) (list $1)]
     [(statement-item statement-items) (cons $1 $2)])

    (statement-item
     [(statement NEWLINE nlopt) $1])

    (statement
     [(loop-stmt) $1]
     [(non-loop-statement) $1])

    (non-loop-statement
     [(if-stmt) $1]
     [(switch-stmt) $1]
     [(function-stmt) $1]
     [(method-stmt) $1]
     [(object-stmt) $1]
     [(declare-stmt) $1]
     [(stmt-leading-lvalue) $1]
     [(nonlvalue-expr-stmt) $1]
     [(input-stmt) $1]
     [(slot-set-stmt) $1]
     [(visible-stmt) $1]
     [(return-stmt) $1]
     [(break-stmt) $1])

    (article-opt
     [() (void)]
     [(A) (void)])

    (slot-article
     [(A) (void)])

    (declare-stmt
     [(I HAS article-opt declare-target declare-init-opt) (stmt-declare $4 $5)])

    (declare-target
     [(ident-token) (expr-ident $1)]
     [(SRS expr) (expr-srs $2)])

    (declare-init-opt
     [() #f]
     [(ITZ expr) $2]
     [(ITZ A ID) (expr-type-default (ensure-declaration-default-type 'parse-source $3))]
     [(ITZ A ID SMOOSH name-spec mixin-list-tail)
      (expr-prototype (expr-literal $3) (cons $5 $6))]
     [(ITZ A SRS expr SMOOSH name-spec mixin-list-tail)
      (expr-prototype (expr-srs $4) (cons $6 $7))])

    (stmt-leading-lvalue
     [(lvalue stmt-lvalue-tail) ($2 $1)])

    (stmt-lvalue-tail
     [(R expr) (lambda (target) (stmt-assign target $2))]
     [(IS NOW A ID)
      (lambda (target)
        (stmt-cast target (ensure-cast-target-type 'IS-NOW-A $4)))]
     [() (lambda (target) (stmt-expr target))]
     [(IZ name-spec call-args MKAY postfix-tail)
      (lambda (target) (stmt-expr ($5 (expr-method-call target $2 $3))))])

    (lvalue
     [(ident-token lvalue-slot-tail) ($2 (id->expr $1))]
     [(SRS expr-no-postfix lvalue-slot-tail) ($3 (expr-srs $2))])

    (lvalue-slot-tail
     [() (lambda (base) base)]
     [(SLOT slot-ref lvalue-slot-tail)
      (lambda (base) ($3 (expr-slot base $2)))])

    (nonlvalue-expr-stmt
     [(nonlvalue-expr) (stmt-expr $1)])

    (nonlvalue-expr
     [(simple-expr-nonid postfix-tail) ($2 $1)])

    (input-stmt
     [(GIMMEH declare-target) (stmt-input $2)])

    (slot-set-stmt
     [(lvalue HAS slot-article slot-target slot-init-opt)
      (make-slot-set-stmt $1 $4 $5)])

    (slot-target
     [(ident-token) (expr-ident $1)]
     [(SRS expr) (expr-srs $2)])

    (slot-init-opt
     [() #f]
     [(ITZ expr) $2])

    (visible-stmt
     [(VISIBLE visible-args) (stmt-visible $2 #f)]
     [(VISIBLE visible-args BANG) (stmt-visible $2 #t)])

    (visible-args
     [(expr) (list $1)]
     [(expr visible-args) (cons $1 $2)])

    (if-stmt
     [(O RLYQ nlopt YA RLY nlopt statement-list-opt mebbe-list else-opt OIC)
      (stmt-if (expr-ident "IT") $7 $8 $9)])

    (mebbe-list
     [() '()]
     [(MEBBE expr nlopt statement-list-opt mebbe-list)
      (cons (mebbe-branch $2 $4) $5)])

    (else-opt
     [() '()]
     [(NO WAI nlopt statement-list-opt) $4])

    (switch-stmt
     [(WTFQ nlopt case-list default-opt OIC)
      (begin
        (validate-switch-case-literals $3)
        (stmt-switch (expr-ident "IT") $3 $4))])

    (loop-stmt
     [(IMIN YR loop-label loop-update-opt loop-cond-opt nlopt loop-body-opt IMOUTTA YR loop-label)
      (make-loop-stmt $3 $10 $4 $5 $7)])

    (loop-label
     [(ident-token) (expr-literal $1)]
     [(SRS expr) (expr-srs $2)])

    (loop-body-opt
     [() '()]
     [(loop-body-items) $1])

    (loop-body-items
     [(loop-body-item) (list $1)]
     [(loop-body-item loop-body-items) (cons $1 $2)])

    (loop-body-item
     [(statement NEWLINE nlopt) $1])

    (loop-update-opt
     [() (cons #f #f)]
     [(UPPIN YR name-spec) (cons $3 '(delta 1))]
     [(NERFIN YR name-spec) (cons $3 '(delta -1))]
     [(I IZ call-target YR name-spec MKAY) (loop-update->spec $3 $5)])

    (loop-cond-opt
     [() (cons #f #f)]
     [(TIL expr) (cons "TIL" $2)]
     [(WILE expr) (cons "WILE" $2)])

    (case-list
     [(case case-list-tail) (cons $1 $2)])

    (case-list-tail
     [() '()]
     [(case case-list-tail) (cons $1 $2)])

    (case
     [(OMG case-literal nlopt statement-list-opt)
      (switch-case $2 $4)])

    (case-literal
     [(NUMBER) (expr-number $1)]
     [(STRING) (switch-string->literal $1)]
     [(ID) (switch-id->literal $1)])

    (default-opt
     [() '()]
     [(OMGWTF nlopt statement-list-opt) $3])

    (function-stmt
     [(HOW how-definition-verb I name-spec arg-def-opt nlopt statement-list-opt IF U SAY SO)
      (stmt-function-def $4 $5 $7)])

    (method-stmt
     [(HOW how-definition-verb method-receiver name-spec arg-def-opt nlopt statement-list-opt IF U SAY SO)
      (stmt-method-def $3 $4 $5 $7)])

    (how-definition-verb
     [(IZ) (void)]
     [(DUZ) (void)])

    (arg-def-opt
     [() '()]
     [(YR ident-token arg-def-more) (cons (expr-literal $2) $3)])

    (arg-def-more
     [() '()]
     [(AN YR ident-token arg-def-more)
      (cons (expr-literal $3) $4)])

    (name-spec
     [(ident-token) (expr-literal $1)]
     [(SRS expr) (expr-srs $2)])

    (method-receiver
     [(ident-token receiver-slot-tail) ($2 (id->expr $1))]
     [(SRS expr-no-postfix receiver-slot-tail) ($3 (expr-srs $2))])

    (receiver-slot-tail
     [() (lambda (base) base)]
     [(SLOT slot-ref receiver-slot-tail)
      (lambda (base) ($3 (expr-slot base $2)))])

    (object-stmt
     [(O HAI IM name-spec object-parent-opt nlopt statement-list-opt KTHX)
      (match-let ([(cons parent-spec mixins) $5])
        (stmt-object-def $4 parent-spec mixins $7))])

    (object-parent-opt
     [() (cons #f '())]
     [(IM LIEK name-spec object-mixins-opt)
      (cons $3 $4)])

    (object-mixins-opt
     [() '()]
     [(SMOOSH name-spec mixin-list-tail) (cons $2 $3)])

    (mixin-list-tail
     [() '()]
     [(AN name-spec mixin-list-tail) (cons $2 $3)])

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
     [(IZ name-spec call-args MKAY postfix-tail)
      (lambda (base) ($5 (expr-method-call base $2 $3)))])

    (slot-ref
     [(ident-token) (expr-ident $1)]
     [(SRS expr-no-postfix) (expr-srs $2)])

    (simple-expr
     [(simple-expr-leading-id) $1]
     [(simple-expr-nonid) $1])

    (simple-expr-leading-id
     [(ident-token) (id->expr $1)]
     [(SRS expr) (expr-srs $2)])

    (simple-expr-nonid
     [(NUMBER) (expr-number $1)]
     [(STRING) (expr-string $1)]
     [(LIEK A expr) (expr-clone $3)]
     [(NOT expr) (expr-unary "NOT" $2)]
     [(MAEK expr A ID)
      (expr-cast $2 (ensure-cast-target-type 'MAEK $4))]
     [(MAEK expr ID)
      (expr-cast $2 (ensure-cast-target-type 'MAEK $3))]
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
     [(LIEK A expr) (expr-clone $3)]
     [(NOT expr) (expr-unary "NOT" $2)]
     [(MAEK expr A ID)
      (expr-cast $2 (ensure-cast-target-type 'MAEK $4))]
     [(MAEK expr ID)
      (expr-cast $2 (ensure-cast-target-type 'MAEK $3))]
     [(I IZ call-target call-args MKAY) (call-target->expr $3 $4)]
     [(bin-expr) $1]
     [(logic-variadic-expr) $1]
     [(smoosh-expr) $1])

    (call-target
     [(ident-token call-target-tail)
      (call-target-from-ident $1 $2)]
     [(SRS expr) (list 'function (expr-srs $2))])

    (call-target-tail
     [() #f]
     [(call-slot-chain) $1])

    (call-slot-chain
     [(SLOT call-slot-name-spec) (list $2)]
     [(SLOT call-slot-name-spec call-slot-chain) (cons $2 $3)])

    (call-slot-name-spec
     [(ident-token) (expr-literal $1)]
     [(SRS expr-no-postfix) (expr-srs $2)])

    (ident-token
     [(ID) (ensure-identifier-token 'parse-source $1)])

    (raw-atom-expr
     [(ident-token) (id->expr $1)]
     [(NUMBER) (expr-number $1)]
     [(STRING) (expr-string $1)])

    (raw-atom-expr-list+
     [(raw-atom-expr) (list $1)]
     [(raw-atom-expr raw-atom-expr-list+) (cons $1 $2)])

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
     [(ALL OF expr logic-arg logic-arg-tail maybe-mkay)
      (expr-variadic "ALL OF" (cons $3 (cons $4 $5)))]
     [(ANY OF expr logic-arg logic-arg-tail maybe-mkay)
      (expr-variadic "ANY OF" (cons $3 (cons $4 $5)))])

    (logic-arg
     [(AN expr) $2]
     [(expr) $1])

    (logic-arg-tail
     [() '()]
     [(logic-arg logic-arg-tail) (cons $1 $2)])

    (smoosh-expr
     [(SMOOSH expr smoosh-arg-tail maybe-mkay)
      (expr-variadic "SMOOSH" (cons $2 $3))])

    (smoosh-arg
     [(AN expr) $2]
     [(expr) $1])

    (smoosh-arg-tail
     [() '()]
     [(smoosh-arg smoosh-arg-tail) (cons $1 $2)])

    (maybe-mkay
     [() (void)]
     [(MKAY) (void)]))))

(define (validate-raw-token-stream raws)
  (match raws
    [(cons (token 'WORD "-" line col)
           (cons (and t2 (token 'NUMBER _ line2 _)) rest))
     (when (= line line2)
       (error 'parse-source
              "invalid numeric literal: '-' must be adjacent to digits at line ~a, col ~a"
              line
              col))
     (validate-raw-token-stream (cons t2 rest))]
    [(cons _ rst) (validate-raw-token-stream rst)]
    [_ (void)]))

(define (variadic-context? context-stack)
  (for/or ([ctx (in-list context-stack)])
    (eq? ctx 'variadic)))

(define (push-context-if-opener t prev-word context-stack)
  (match t
    [(token 'WORD "IZ" _ _)
     (if (string=? prev-word "HOW")
         context-stack
         (cons 'call context-stack))]
    [(token 'WORD "OF" _ _)
     (if (or (string=? prev-word "ALL")
             (string=? prev-word "ANY"))
         (cons 'variadic context-stack)
         context-stack)]
    [(token 'WORD "SMOOSH" _ _) (cons 'variadic context-stack)]
    [(token 'WORD "MKAY" _ _)
     (match context-stack
       ['() context-stack]
       [(cons _ rest) rest])]
    [_ context-stack]))

(define (validate-implicit-mkay-boundaries raws [prev-word ""] [context-stack '()])
  (match raws
    ['() (void)]
    [(cons (token 'NEWLINE _ _ _) rst)
     (validate-implicit-mkay-boundaries rst "" '())]
    [(cons (token 'WORD "!" line col) rst)
     (when (variadic-context? context-stack)
       (error 'parse-source
              (string-append
               "implicit MKAY omission is only allowed at statement boundary; "
               "explicit MKAY required before ! at line ~a, col ~a")
              line
              col))
     (validate-implicit-mkay-boundaries rst "!" context-stack)]
    [(cons (token 'WORD "AN" line col)
           (cons (token 'WORD "YR" _ _) _))
     #:when (variadic-context? context-stack)
     (error 'parse-source
            (string-append
             "implicit MKAY omission is only allowed at statement boundary; "
             "explicit MKAY required before AN YR at line ~a, col ~a")
            line
            col)]
    [(cons (and t (token 'WORD word _ _)) rst)
     (validate-implicit-mkay-boundaries
      rst
      word
      (push-context-if-opener t prev-word context-stack))]
    [(cons _ rst)
     (validate-implicit-mkay-boundaries rst prev-word context-stack)]))

(define (validate-kthxbye-postlude source raws)
  (define maybe-kthxbye
    (for/first ([t (in-list raws)]
                #:when (match t
                         [(token 'WORD "KTHXBYE" _ _) #t]
                         [_ #f]))
      t))
  (when maybe-kthxbye
    (match-define (token 'WORD "KTHXBYE" line col) maybe-kthxbye)
    (define lines (source->line-vector source))
    (define line-index (- line 1))
    (define line-text
      (if (and (<= 0 line-index) (< line-index (vector-length lines)))
          (vector-ref lines line-index)
          ""))
    (define suffix-start (+ (- col 1) (string-length "KTHXBYE")))
    (define line-suffix
      (if (<= suffix-start (string-length line-text))
          (substring line-text suffix-start)
          ""))
    (unless (regexp-match? kthxbye-inline-tail-rx line-suffix)
      (error 'parse-source
             "no material allowed after KTHXBYE except optional same-line BTW comment"))
    (for ([idx (in-range line (vector-length lines))])
      (define trailing-line (vector-ref lines idx))
      (unless (regexp-match? #px"^\\s*$" trailing-line)
        (error 'parse-source
               "no material allowed after KTHXBYE except optional same-line BTW comment")))))

(define (validate-function-def-placement parsed)
  (define (walk-block stmts allow-function-def?)
    (for ([stmt (in-list stmts)])
      (walk-stmt stmt allow-function-def?)))
  (define (walk-stmt stmt allow-function-def?)
    (match stmt
      [(stmt-function-def _ _ body)
       (unless allow-function-def?
         (error 'parse-source
                "nested HOW IZ I definitions are not allowed in strict 1.3"))
       (walk-block body #f)]
      [(stmt-method-def _ _ _ body) (walk-block body #f)]
       ;; Object bodies may declare methods with HOW IZ I.
      [(stmt-object-def _ _ _ body) (walk-block body #t)]
      [(stmt-if _ then-branch mebbe-branches else-branch)
       (walk-block then-branch #f)
       (for ([mb (in-list mebbe-branches)])
         (walk-block (mebbe-branch-body mb) #f))
       (walk-block else-branch #f)]
      [(stmt-switch _ cases default)
       (for ([c (in-list cases)])
         (walk-block (switch-case-body c) #f))
       (walk-block default #f)]
      [(stmt-loop _ _ _ _ _ _ body) (walk-block body #f)]
      [_ (void)]))
  (walk-block (program-statements parsed) #t))

(define (parse-source source)
  (unless (string? source)
    (raise-argument-error 'parse-source "string?" source))
  (unless (regexp-match? program-opener-rx source)
    (error 'parse-source
           "program must begin with HAI opener (no leading comments or tokens before HAI)"))
  (define normalized-raws (collapse-phrase-tokens (lex-source source)))
  (validate-raw-token-stream normalized-raws)
  (validate-implicit-mkay-boundaries normalized-raws)
  (define toks (map raw->position-token normalized-raws))
  (unless (pair? toks)
    (error 'parse-source "internal error: lexer produced no tokens"))
  (match-define-values (non-eof-toks (list eof-token)) (split-at-right toks 1))
  (define-values (more-token? advance-token) (sequence-generate (in-list non-eof-toks)))
  (define (next-token)
    (if (more-token?)
        (advance-token)
        eof-token))
  (define parsed
    (parameterize ([current-source-lines
                    (source->line-vector source)])
      (parse/internal next-token)))
  (unless (string=? (program-version parsed) supported-language-version)
    (error 'parse-source
           "unsupported version: ~a (this implementation only accepts HAI ~a)"
           (program-version parsed)
           supported-language-version))
  (validate-kthxbye-postlude source normalized-raws)
  (validate-function-def-placement parsed)
  parsed)
