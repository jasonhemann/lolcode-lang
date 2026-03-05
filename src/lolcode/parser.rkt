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
       IF U SAY SO HOW IZ GIMMEH
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
        "'Z" token-SLOT
        "A" token-A
        "ALL" token-ALL
        "AN" token-AN
        "ANY" token-ANY
        "BIGGR" token-BIGGR
        "BOTH" token-BOTH
        "DIFF" token-DIFF
        "DIFFRINT" token-DIFFRINT
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

(define identifier-token-rx
  #px"^[A-Za-z][A-Za-z0-9_]*$")

(define (valid-identifier-token? text)
  (regexp-match? identifier-token-rx text))

(define (ensure-identifier-token who text)
  (unless (valid-identifier-token? text)
    (error who "invalid identifier syntax: ~v" text))
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
  (error 'parse-source
         "syntax error: unexpected ~a at line ~a, col ~a~a"
         unexpected
         line
         col
         context-fragment))

(define (make-loop-stmt label-open label-close update cond body)
  (define open-static
    (match label-open
      [(expr-literal (? string? s)) s]
      [_ #f]))
  (define close-static
    (match label-close
      [(expr-literal (? string? s)) s]
      [_ #f]))
  (when (and open-static
             close-static
             (not (string-ci=? open-static close-static)))
    (error 'parse-source
           "loop label mismatch: ~a closed by ~a"
           open-static
           close-static))
  (stmt-loop label-open
             label-close
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
    [(or (string-ci=? name "NUMBR")
         (string-ci=? name "NUMBAR")
         (string-ci=? name "YARN")
         (string-ci=? name "TROOF")
         (string-ci=? name "TYPE"))
     (expr-literal (string-upcase name))]
    [else (expr-ident name)]))

(define (static-name-spec name)
  (expr-literal name))

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
    [(list 'method receiver method-name)
     ;; Namespace-style calls dispatch as method calls first and fall back to
     ;; runtime namespace functions when receiver binding is absent.
     (expr-method-call receiver method-name args)]
    [_ (error 'parse-source "invalid call target: ~e" target)]))

(define (slot-name-spec->expr spec)
  (cond
    [(expr-literal? spec)
     (define maybe-name
       (expr-literal-value spec))
     (unless (string? maybe-name)
       (error 'parse-source "invalid slot name spec literal: ~e" spec))
     (expr-ident maybe-name)]
    [(string? spec)
     (expr-ident spec)]
    [(expr-srs? spec)
     spec]
    [else
     (error 'parse-source "invalid slot name spec: ~e" spec)]))

(define (build-slot-chain base slot-name-specs)
  (for/fold ([obj base]) ([slot-spec (in-list slot-name-specs)])
    (expr-slot obj (slot-name-spec->expr slot-spec))))

(define (call-slot-chain->target base slot-name-specs)
  (define n (length slot-name-specs))
  (when (< n 1)
    (error 'parse-source "invalid call slot chain"))
  (define receiver
    (build-slot-chain base (take slot-name-specs (sub1 n))))
  (define method-name-spec
    (last slot-name-specs))
  (list 'method receiver method-name-spec))

(define (call-target-from-ident name maybe-slots)
  (if maybe-slots
      (call-slot-chain->target (id->expr name) maybe-slots)
      (list 'function (static-name-spec name))))

(define (loop-update->spec target var-name)
  (match target
    [(list 'function fn-name)
     (cons var-name (list 'call fn-name))]
    [_ (error 'parse-source
              "loop updater call must target a function name, got ~e"
              target)]))

(define switch-interpolation-rx
  #px":\\{[^\\}]*\\}")

(define (switch-string->literal text)
  (when (regexp-match? switch-interpolation-rx text)
    (error 'parse-source
           "WTF? case literal cannot contain YARN interpolation (:{...})"))
  (expr-string text))

(define (switch-literal-key expr)
  (match expr
    [(expr-number text)
     (list 'NUM (or (string->number text) text))]
    [(expr-string text)
     (list 'YARN text)]
    [(expr-literal value)
     (list 'LIT value)]
    [_ #f]))

(define (validate-switch-case-literals! cases)
  (define seen (make-hash))
  (for ([c (in-list cases)])
    (match-define (switch-case case-match _case-body) c)
    (define key (switch-literal-key case-match))
    (when key
      (when (hash-has-key? seen key)
        (error 'parse-source
               "duplicate OMG literal in WTF?: ~e"
               case-match))
      (hash-set! seen key #t))))

(define (word-token-ci=? t text)
  (and (eq? (token-type t) 'WORD)
       (string-ci=? (token-lexeme t) text)))

(define (collapse-phrase-tokens raws [acc '()])
  (match raws
    ['() (reverse acc)]
    [`(,t1 ,t2 ., rest)
     #:when (and (word-token-ci=? t1 "IM")
                 (word-token-ci=? t2 "IN")
                 (= (token-line t1) (token-line t2)))
     (collapse-phrase-tokens
      rest
      (cons (token 'WORD "IMIN" (token-line t1) (token-col t1))
            acc))]
    [`(,t1 ,t2 . ,rest)
     #:when (and (word-token-ci=? t1 "IM")
                 (word-token-ci=? t2 "OUTTA")
                 (= (token-line t1) (token-line t2)))
     (collapse-phrase-tokens
      rest
      (cons (token 'WORD "IMOUTTA" (token-line t1) (token-col t1))
            acc))]
    [`(,t . ,rest)
     (collapse-phrase-tokens rest (cons t acc))]))

(define (raw-atom-token? t)
  (case (token-type t)
    [(NUMBER STRING) #t]
    [(WORD)
     (not (hash-ref keyword-token-ctors
                    (string-upcase (token-lexeme t))
                    #f))]
    [else #f]))

(define (rewrite-smoosh-line line-toks)
  (let loop ([prefix '()] [rest line-toks])
    (cond
      [(null? rest)
       (append (reverse prefix) rest)]
      [(word-token-ci=? (car rest) "SMOOSH")
       (define sm (car rest))
       (define suffix (cdr rest))
       (define-values (args tail)
         (let gather ([remaining suffix] [acc '()])
           (cond
             [(null? remaining)
              (values (reverse acc) '())]
             [(word-token-ci=? (car remaining) "MKAY")
              (values (reverse acc) remaining)]
             [else
              (gather (cdr remaining) (cons (car remaining) acc))])))
       (define rewritten-rest
         (if (and (>= (length args) 2)
                  (not (for/or ([a (in-list args)])
                         (word-token-ci=? a "AN")))
                  (andmap raw-atom-token? args))
             (let build ([remaining args] [idx 0] [out '()])
               (cond
                 [(null? remaining) (reverse out)]
                 [else
                  (define arg (car remaining))
                  (if (>= idx 1)
                      (build (cdr remaining)
                             (+ idx 1)
                             (cons arg
                                   (cons (token 'WORD
                                                "AN"
                                                (token-line arg)
                                                (max 1 (- (token-col arg) 3)))
                                         out)))
                      (build (cdr remaining)
                             (+ idx 1)
                             (cons arg out)))]))
             args))
       (append (reverse prefix) (list sm) rewritten-rest tail)]
      [else
       (loop (cons (car rest) prefix) (cdr rest))])))

(define (rewrite-smoosh-no-an-raws raws [line '()] [out '()])
  (cond
    [(null? raws)
     (append out (rewrite-smoosh-line line))]
    [else
     (define t (car raws))
     (if (eq? (token-type t) 'NEWLINE)
         (rewrite-smoosh-no-an-raws
          (cdr raws)
          '()
          (append out (rewrite-smoosh-line line) (list t)))
         (rewrite-smoosh-no-an-raws
          (cdr raws)
          (append line (list t))
          out))]))

(define (logic-head-token? t)
  (and (eq? (token-type t) 'WORD)
       (or (string-ci=? (token-lexeme t) "ALL")
           (string-ci=? (token-lexeme t) "ANY"))))

(define (rewrite-logic-line line-toks)
  (let loop ([prefix '()] [rest line-toks])
    (cond
      [(null? rest)
       (append (reverse prefix) rest)]
      [(and (pair? (cdr rest))
            (logic-head-token? (car rest))
            (word-token-ci=? (cadr rest) "OF"))
       (define head1 (car rest))
       (define head2 (cadr rest))
       (define suffix (cddr rest))
       (define-values (args tail)
         (let gather ([remaining suffix] [acc '()])
           (cond
             [(null? remaining)
              (values (reverse acc) '())]
             [(word-token-ci=? (car remaining) "MKAY")
              (values (reverse acc) remaining)]
             [else
              (gather (cdr remaining) (cons (car remaining) acc))])))
       (define rewritten-args
         (if (and (>= (length args) 2)
                  (not (for/or ([a (in-list args)])
                         (word-token-ci=? a "AN")))
                  (andmap raw-atom-token? args))
             (insert-optional-an-separators args)
             args))
       (append (reverse prefix) (list head1 head2) rewritten-args tail)]
      [else
       (loop (cons (car rest) prefix) (cdr rest))])))

(define (rewrite-logic-no-an-raws raws [line '()] [out '()])
  (cond
    [(null? raws)
     (append out (rewrite-logic-line line))]
    [else
     (define t (car raws))
     (if (eq? (token-type t) 'NEWLINE)
         (rewrite-logic-no-an-raws
          (cdr raws)
          '()
          (append out (rewrite-logic-line line) (list t)))
         (rewrite-logic-no-an-raws
          (cdr raws)
          (append line (list t))
          out))]))

(define (insert-optional-an-separators args)
  (let loop ([remaining args] [idx 0] [out '()])
    (cond
      [(null? remaining) (reverse out)]
      [else
       (define arg (car remaining))
       (if (zero? idx)
           (loop (cdr remaining)
                 (add1 idx)
                 (cons arg out))
           (loop (cdr remaining)
                 (add1 idx)
                 (cons arg
                       (cons (token 'WORD
                                    "AN"
                                    (token-line arg)
                                    (max 1 (- (token-col arg) 3)))
                             out))))])))

(define (rewrite-visible-line line-toks)
  (cond
    [(or (null? line-toks)
         (not (word-token-ci=? (car line-toks) "VISIBLE")))
     line-toks]
    [else
     (define visible-tok (car line-toks))
     (define body (cdr line-toks))
     (define has-trailing-bang?
       (and (pair? body)
            (word-token-ci=? (last body) "!")))
     (define args
       (if has-trailing-bang?
           (drop-right body 1)
           body))
     (define trailing
       (if has-trailing-bang?
           (list (last body))
           '()))
     (if (and (>= (length args) 2)
              (not (for/or ([a (in-list args)])
                     (word-token-ci=? a "AN")))
              (andmap raw-atom-token? args))
         (append (list visible-tok)
                 (insert-optional-an-separators args)
                 trailing)
         line-toks)]))

(define (rewrite-visible-no-an-raws raws [line '()] [out '()])
  (cond
    [(null? raws)
     (append out (rewrite-visible-line line))]
    [else
     (define t (car raws))
     (if (eq? (token-type t) 'NEWLINE)
         (rewrite-visible-no-an-raws
          (cdr raws)
          '()
          (append out (rewrite-visible-line line) (list t)))
         (rewrite-visible-no-an-raws
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
       (and (not (string=? lex "a"))
			(not (string=? lex "i"))
			(string=? lex lex-upcase)
            (hash-ref keyword-token-ctors lex-upcase #f)))
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
   (expected-SR-conflicts 21)
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
     [(assign-stmt) $1]
     [(cast-stmt) $1]
     [(input-stmt) $1]
     [(slot-set-stmt) $1]
     [(visible-stmt) $1]
     [(return-stmt) $1]
     [(break-stmt) $1]
     [(expr-stmt) $1])

    (article-opt
     [() (void)]
     [(A) (void)]
     [(AN) (void)])

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
     [(ITZ A ID) (expr-ident $3)]
     [(ITZ A ID SMOOSH name-spec mixin-list-tail)
      (expr-prototype (static-name-spec $3) (cons $5 $6))]
     [(ITZ A SRS expr SMOOSH name-spec mixin-list-tail)
      (expr-prototype (expr-srs $4) (cons $6 $7))])

    (assign-stmt
     [(expr R expr) (stmt-assign $1 $3)])

    (cast-stmt
     [(expr IS NOW A ID) (stmt-cast $1 $5)])

    (input-stmt
     [(GIMMEH expr) (stmt-input $2)])

    (slot-set-stmt
     [(expr HAS slot-article slot-target slot-init-opt) (stmt-slot-set $1 $4 $5)])

    (slot-target
     [(ident-token) (expr-ident $1)]
     [(SRS expr) (expr-srs $2)])

    (slot-init-opt
     [() #f]
     [(ITZ expr) $2]
     [(ITZ A ID) (expr-ident $3)])

    (visible-stmt
     [(VISIBLE visible-args) (stmt-visible $2 #f)]
     [(VISIBLE visible-args BANG) (stmt-visible $2 #t)])

    (visible-args
     [(expr) (list $1)]
     [(expr AN visible-args) (cons $1 $3)])

    (if-stmt
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
     [(WTFQ nlopt case-list default-opt OIC)
      (begin
        (validate-switch-case-literals! $3)
        (stmt-switch (expr-ident "IT") $3 $4))])

    (loop-stmt
     [(IMIN YR loop-label loop-update-opt loop-cond-opt nlopt loop-body-opt IMOUTTA YR loop-label)
      (make-loop-stmt $3 $10 $4 $5 $7)])

    (loop-label
     [(ident-token) (static-name-spec $1)]
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
     [(case) (list $1)]
     [(case-list case) (append $1 (list $2))])

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
     [(HOW IZ I name-spec arg-def-opt nlopt statement-list-opt IF U SAY SO)
      (stmt-function-def $4 $5 $7)])

    (method-stmt
     [(HOW IZ method-receiver name-spec arg-def-opt nlopt statement-list-opt IF U SAY SO)
      (stmt-method-def $3 $4 $5 $7)])

    (arg-def-opt
     [() '()]
     [(YR name-spec arg-def-more) (cons $2 $3)])

    (arg-def-more
     [() '()]
     [(AN YR name-spec arg-def-more) (cons $3 $4)])

    (name-spec
     [(ident-token) (static-name-spec $1)]
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
      (stmt-object-def $4 (car $5) (cdr $5) $7)])

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

    (expr-stmt
     [(expr) (stmt-expr $1)])

    (expr
     [(simple-expr postfix-tail) ($2 $1)])

    (postfix-tail
     [() (lambda (base) base)]
     [(SLOT slot-ref postfix-tail)
      (lambda (base) ($3 (expr-slot base $2)))]
     [(IZ name-spec call-args MKAY postfix-tail)
      (lambda (base) ($5 (expr-method-call base $2 $3)))])

    (slot-ref
     [(ident-token) (id->expr $1)]
     [(SRS expr-no-postfix) (expr-srs $2)])

    (simple-expr
     [(NUMBER) (expr-number $1)]
     [(STRING) (expr-string $1)]
     [(ident-token) (id->expr $1)]
     [(SRS expr) (expr-srs $2)]
     [(LIEK A expr) (expr-clone $3)]
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
     [(LIEK A expr) (expr-clone $3)]
     [(NOT expr) (expr-unary "NOT" $2)]
     [(MAEK expr A ID) (expr-cast $2 $4)]
     [(MAEK expr ID) (expr-cast $2 $3)]
     [(I IZ call-target call-args MKAY) (call-target->expr $3 $4)]
     [(bin-expr) $1]
     [(logic-variadic-expr) $1]
     [(smoosh-expr) $1])

    (call-target
     [(ident-token call-target-tail)
      (call-target-from-ident $1 $2)]
     [(SRS expr) (list 'function (expr-srs $2))]
     )

    (call-target-tail
     [() #f]
     [(call-slot-chain) $1])

    (call-slot-chain
     [(SLOT call-slot-name-spec) (list $2)]
     [(SLOT call-slot-name-spec call-slot-chain) (cons $2 $3)])

    (call-slot-name-spec
     [(ident-token) (static-name-spec $1)]
     [(SRS expr-no-postfix) (expr-srs $2)])

    (ident-token
     [(ID) (ensure-identifier-token 'parse-source $1)]
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
     [(ALL OF expr logic-tail maybe-mkay) (expr-variadic "ALL OF" (cons $3 $4))]
     [(ANY OF expr logic-tail maybe-mkay) (expr-variadic "ANY OF" (cons $3 $4))])

    (logic-tail
     [() '()]
     [(AN expr logic-tail) (cons $2 $3)])

    (smoosh-expr
     [(SMOOSH expr smoosh-tail maybe-mkay) (expr-variadic "SMOOSH" (cons $2 $3))])

    (smoosh-tail
     [() '()]
     [(AN expr smoosh-tail) (cons $2 $3)])

    (maybe-mkay
     [() (void)]
     [(MKAY) (void)]))))

(define (validate-raw-token-stream! raws)
  (define (loop remaining)
    (match remaining
      [`(,t1 ,t2 . ,rest)
       (when (and (eq? (token-type t1) 'WORD)
                  (string=? (token-lexeme t1) "-")
                  (eq? (token-type t2) 'NUMBER)
                  (= (token-line t1) (token-line t2)))
         (error 'parse-source
                "invalid numeric literal: '-' must be adjacent to digits at line ~a, col ~a"
                (token-line t1)
                (token-col t1)))
       (loop (cons t2 rest))]
      [_ (void)]))
  (loop raws))

(define (validate-function-def-placement! parsed)
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
      [(stmt-method-def _ _ _ body)
       (walk-block body #f)]
      [(stmt-object-def _ _ _ body)
       ;; Object bodies may declare methods with HOW IZ I.
       (walk-block body #t)]
      [(stmt-if _ then-branch mebbe-branches else-branch)
       (walk-block then-branch #f)
       (for ([mb (in-list mebbe-branches)])
         (walk-block (mebbe-branch-body mb) #f))
       (walk-block else-branch #f)]
      [(stmt-switch _ cases default)
       (for ([c (in-list cases)])
         (walk-block (switch-case-body c) #f))
       (walk-block default #f)]
      [(stmt-loop _ _ _ _ _ _ body)
       (walk-block body #f)]
      [_ (void)]))
  (walk-block (program-statements parsed) #t))

(define (parse-source source)
  (unless (string? source)
    (raise-argument-error 'parse-source "string?" source))
  (define normalized-raws
    (rewrite-visible-no-an-raws
     (rewrite-logic-no-an-raws
      (rewrite-smoosh-no-an-raws
       (collapse-phrase-tokens (lex-source source))))))
  (validate-raw-token-stream! normalized-raws)
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
  (validate-function-def-placement! parsed)
  parsed)
