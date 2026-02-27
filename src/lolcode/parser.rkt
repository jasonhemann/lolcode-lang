#lang racket/base

(require racket/list
         racket/string
         "ast.rkt"
         "lexer.rkt")

(provide parse-source)

(define (parse-error where tok fmt . args)
  (define msg (apply format fmt args))
  (error where "~a at line ~a, col ~a" msg (token-line tok) (token-col tok)))

(define (parse-source source)
  (define tv (list->vector (lex-source source)))
  (define len (vector-length tv))
  (define pos 0)

  (define (cur) (vector-ref tv pos))
  (define (cur-type) (token-type (cur)))
  (define (cur-lexeme) (token-lexeme (cur)))
  (define (cur-word-up) (string-upcase (cur-lexeme)))

  (define (advance!)
    (when (< pos (- len 1))
      (set! pos (+ pos 1)))
    (cur))

  (define (at-type? t) (eq? (cur-type) t))
  (define (at-word? w)
    (and (at-type? 'WORD)
         (string=? (cur-word-up) (string-upcase w))))
  (define (at-words? ws)
    (let loop ([i 0] [rest ws])
      (cond
        [(null? rest) #t]
        [else
         (define p (+ pos i))
         (and (< p len)
              (eq? (token-type (vector-ref tv p)) 'WORD)
              (string=? (string-upcase (token-lexeme (vector-ref tv p)))
                        (string-upcase (car rest)))
              (loop (+ i 1) (cdr rest)))])))

  (define (consume-word! w)
    (unless (at-word? w)
      (parse-error 'parse-source (cur) "expected word ~a, got ~a" w (cur-lexeme)))
    (define t (cur))
    (advance!)
    t)

  (define (consume-words! ws)
    (for ([w (in-list ws)])
      (consume-word! w)))

  (define (skip-newlines!)
    (let loop ()
      (when (at-type? 'NEWLINE)
        (advance!)
        (loop))))

  (define (parse-identifier!)
    (unless (at-type? 'WORD)
      (parse-error 'parse-source (cur) "expected identifier, got ~a" (cur-lexeme)))
    (define x (cur-lexeme))
    (advance!)
    x)

  (define (parse-call-args!)
    (define args '())
    (when (at-word? "YR")
      (let loop ()
        (consume-word! "YR")
        (set! args (append args (list (parse-expression!))))
        (when (at-word? "AN")
          (consume-word! "AN")
          (unless (at-word? "YR")
            (parse-error 'parse-source (cur) "expected YR after AN in call arguments"))
          (loop))))
    args)

  (define (parse-expression-core!)
    (cond
      [(at-words? '("I" "IZ"))
       (consume-words! '("I" "IZ"))
       (define name (parse-identifier!))
       (define args (parse-call-args!))
       (consume-word! "MKAY")
       (expr-call name args)]
      [(at-word? "SRS")
       (consume-word! "SRS")
       (expr-srs (parse-expression!))]
      [(at-word? "SMOOSH")
       (consume-word! "SMOOSH")
       (define args (list (parse-expression!)))
       (let loop ()
         (cond
           [(at-word? "AN")
            (consume-word! "AN")
            (set! args (append args (list (parse-expression!))))
            (loop)]
           [(at-word? "MKAY")
            (consume-word! "MKAY")]
           [else (void)]))
       (expr-variadic "SMOOSH" args)]
      [(or (at-words? '("SUM" "OF"))
           (at-words? '("DIFF" "OF"))
           (at-words? '("PRODUKT" "OF"))
           (at-words? '("QUOSHUNT" "OF"))
           (at-words? '("MOD" "OF"))
           (at-words? '("BIGGR" "OF"))
           (at-words? '("SMALLR" "OF"))
           (at-words? '("BOTH" "SAEM"))
           (at-word? "DIFFRINT"))
       (define op
         (cond
           [(at-words? '("SUM" "OF")) (consume-words! '("SUM" "OF")) "SUM OF"]
           [(at-words? '("DIFF" "OF")) (consume-words! '("DIFF" "OF")) "DIFF OF"]
           [(at-words? '("PRODUKT" "OF")) (consume-words! '("PRODUKT" "OF")) "PRODUKT OF"]
           [(at-words? '("QUOSHUNT" "OF")) (consume-words! '("QUOSHUNT" "OF")) "QUOSHUNT OF"]
           [(at-words? '("MOD" "OF")) (consume-words! '("MOD" "OF")) "MOD OF"]
           [(at-words? '("BIGGR" "OF")) (consume-words! '("BIGGR" "OF")) "BIGGR OF"]
           [(at-words? '("SMALLR" "OF")) (consume-words! '("SMALLR" "OF")) "SMALLR OF"]
           [(at-words? '("BOTH" "SAEM")) (consume-words! '("BOTH" "SAEM")) "BOTH SAEM"]
           [else (consume-word! "DIFFRINT") "DIFFRINT"]))
       (define left (parse-expression!))
       (when (at-word? "AN")
         (consume-word! "AN"))
       (define right (parse-expression!))
       (expr-binary op left right)]
      [(at-type? 'STRING)
       (define t (cur-lexeme))
       (advance!)
       (expr-string t)]
      [(at-type? 'NUMBER)
       (define t (cur-lexeme))
       (advance!)
       (expr-number t)]
      [(at-type? 'WORD)
       (define t (cur-lexeme))
       (advance!)
       (expr-ident t)]
      [else
       (parse-error 'parse-source (cur) "unexpected token in expression: ~a" (cur-lexeme))]))

  (define (parse-expression!)
    (define e (parse-expression-core!))
    (let loop ([acc e])
      (cond
        [(at-word? "'Z")
         (consume-word! "'Z")
         (define slot
           (if (at-word? "SRS")
               (begin
                 (consume-word! "SRS")
                 (parse-expression!))
               (expr-ident (parse-identifier!))))
         (loop (expr-slot acc slot))]
        [(at-word? "IZ")
         (consume-word! "IZ")
         (define method-name (parse-identifier!))
         (define args (parse-call-args!))
         (consume-word! "MKAY")
         (loop (expr-method-call acc method-name args))]
        [else acc])))

  (define (parse-statements-until stop?)
    (define stmts '())
    (skip-newlines!)
    (let loop ()
      (unless (stop?)
        (when (at-type? 'EOF)
          (parse-error 'parse-source (cur) "unexpected EOF while parsing block"))
        (set! stmts (append stmts (list (parse-statement!))))
        (skip-newlines!)
        (loop)))
    stmts)

  (define (parse-if-tail! condition)
    (consume-words! '("O" "RLY?"))
    (skip-newlines!)
    (consume-words! '("YA" "RLY"))
    (define then-branch
      (parse-statements-until
       (lambda ()
         (or (at-word? "MEBBE")
             (at-words? '("NO" "WAI"))
             (at-word? "OIC")))))
    (define mebbes '())
    (let mebbe-loop ()
      (when (at-word? "MEBBE")
        (consume-word! "MEBBE")
        (define m-cond (parse-expression!))
        (define m-body
          (parse-statements-until
           (lambda ()
             (or (at-word? "MEBBE")
                 (at-words? '("NO" "WAI"))
                 (at-word? "OIC")))))
        (set! mebbes (append mebbes (list (mebbe-branch m-cond m-body))))
        (mebbe-loop)))
    (define else-branch '())
    (when (at-words? '("NO" "WAI"))
      (consume-words! '("NO" "WAI"))
      (set! else-branch
            (parse-statements-until (lambda () (at-word? "OIC")))))
    (consume-word! "OIC")
    (stmt-if condition then-branch mebbes else-branch))

  (define (parse-switch-tail! subject)
    (consume-word! "WTF?")
    (define cases '())
    (define default '())
    (skip-newlines!)
    (let loop ()
      (cond
        [(at-word? "OMG")
         (consume-word! "OMG")
         (define match-expr (parse-expression!))
         (define case-body
           (parse-statements-until
            (lambda ()
              (or (at-word? "OMG")
                  (at-word? "OMGWTF")
                  (at-word? "OIC")))))
         (set! cases (append cases (list (switch-case match-expr case-body))))
         (loop)]
        [(at-word? "OMGWTF")
         (consume-word! "OMGWTF")
         (set! default
               (parse-statements-until (lambda () (at-word? "OIC"))))
         (loop)]
        [(at-word? "OIC")
         (consume-word! "OIC")
         (stmt-switch subject cases default)]
        [else
         (parse-error 'parse-source (cur) "expected OMG/OMGWTF/OIC in WTF block")]))
    )

  (define (parse-function-def!)
    (consume-words! '("HOW" "IZ" "I"))
    (define name (parse-identifier!))
    (define args '())
    (when (at-word? "YR")
      (consume-word! "YR")
      (set! args (append args (list (parse-identifier!))))
      (let loop ()
        (when (at-word? "AN")
          (consume-word! "AN")
          (consume-word! "YR")
          (set! args (append args (list (parse-identifier!))))
          (loop))))
    (define body
      (parse-statements-until
       (lambda ()
         (at-words? '("IF" "U" "SAY" "SO")))))
    (consume-words! '("IF" "U" "SAY" "SO"))
    (stmt-function-def name args body))

  (define (parse-object-def!)
    (consume-words! '("O" "HAI" "IM"))
    (define name (parse-identifier!))
    (define parent #f)
    (when (at-words? '("IM" "LIEK"))
      (consume-words! '("IM" "LIEK"))
      (set! parent (parse-identifier!)))
    (define body
      (parse-statements-until (lambda () (at-word? "KTHX"))))
    (consume-word! "KTHX")
    (stmt-object-def name parent body))

  (define (parse-visible!)
    (consume-word! "VISIBLE")
    (define exprs '())
    (define suppress-newline? #f)
    (let loop ()
      (cond
        [(or (at-type? 'NEWLINE) (at-type? 'EOF)) (void)]
        [(and (at-type? 'WORD) (string=? (cur-lexeme) "!"))
         (set! suppress-newline? #t)
         (advance!)
         (loop)]
        [else
         (set! exprs (append exprs (list (parse-expression!))))
         (when (at-word? "AN")
           (consume-word! "AN")
           (loop))]))
    (stmt-visible exprs suppress-newline?))

  (define (parse-declare!)
    (consume-words! '("I" "HAS"))
    (when (at-word? "A")
      (consume-word! "A"))
    (define target
      (if (at-word? "SRS")
          (begin
            (consume-word! "SRS")
            (expr-srs (parse-expression!)))
          (expr-ident (parse-identifier!))))
    (define init #f)
    (when (at-word? "ITZ")
      (consume-word! "ITZ")
      (if (at-word? "A")
          (begin
            (consume-word! "A")
            (set! init (expr-ident (parse-identifier!))))
          (set! init (parse-expression!))))
    (stmt-declare target init))

  (define (parse-statement!)
    (skip-newlines!)
    (cond
      [(at-words? '("O" "RLY?")) (parse-if-tail! (expr-ident "IT"))]
      [(at-word? "WTF?") (parse-switch-tail! (expr-ident "IT"))]
      [(at-words? '("HOW" "IZ" "I")) (parse-function-def!)]
      [(at-words? '("O" "HAI" "IM")) (parse-object-def!)]
      [(at-word? "VISIBLE") (parse-visible!)]
      [(at-words? '("I" "HAS")) (parse-declare!)]
      [(at-words? '("FOUND" "YR"))
       (consume-words! '("FOUND" "YR"))
       (stmt-return (parse-expression!))]
      [(at-word? "GTFO")
       (consume-word! "GTFO")
       (stmt-break)]
      [else
       (define first-expr (parse-expression!))
       (cond
         [(at-word? "R")
          (consume-word! "R")
          (stmt-assign first-expr (parse-expression!))]
         [(at-words? '("HAS" "A"))
          (consume-words! '("HAS" "A"))
          (define slot
            (if (at-word? "SRS")
                (begin
                  (consume-word! "SRS")
                  (expr-srs (parse-expression!)))
                (expr-ident (parse-identifier!))))
          (consume-word! "ITZ")
          (stmt-slot-set first-expr slot (parse-expression!))]
         [(at-words? '("O" "RLY?"))
          (parse-if-tail! first-expr)]
         [(at-word? "WTF?")
          (parse-switch-tail! first-expr)]
         [else
          (stmt-expr first-expr)])]))

  (skip-newlines!)
  (consume-word! "HAI")
  (unless (or (at-type? 'NUMBER) (at-type? 'WORD))
    (parse-error 'parse-source (cur) "expected version number after HAI"))
  (define version (cur-lexeme))
  (advance!)

  (define body
    (parse-statements-until (lambda () (at-word? "KTHXBYE"))))

  (consume-word! "KTHXBYE")
  (skip-newlines!)
  (unless (at-type? 'EOF)
    (parse-error 'parse-source (cur) "unexpected trailing tokens after KTHXBYE"))
  (program version body))
