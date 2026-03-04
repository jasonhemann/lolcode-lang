#lang racket/base

(require racket/port
         racket/string
         parser-tools/lex
         (prefix-in : parser-tools/lex-sre))

(provide token
         token?
         token-type
         token-lexeme
         token-line
         token-col
         lex-source
         lexer-coverage-enabled?
         lexer-coverage-reset!
         lexer-coverage-snapshot
         lexer-coverage-universe)

(struct token (type lexeme line col) #:transparent)

(define lexer-coverage-enabled?
  (make-parameter #f))

(define lexer-coverage-counts
  (make-hash))

(define lexer-coverage-universe
  (list
   'lex-error
   'word->tokens/comment
   'word->tokens/block-comment
   'word->tokens/line-continuation
   'word->tokens/ok+line-continuation
   'word->tokens/split-slot-z
   'word->tokens/number
   'word->tokens/word
   'skip-comment-tail!/eof
   'skip-comment-tail!/newline
   'skip-comment-tail!/char
   'skip-block-comment!/eof
   'skip-block-comment!/word-char
   'skip-block-comment!/found-tldr
   'skip-block-comment!/delimiter
   'skip-line-continuation!/eof
   'skip-line-continuation!/space-or-tab
   'skip-line-continuation!/crlf
   'skip-line-continuation!/cr
   'skip-line-continuation!/lf
   'skip-line-continuation!/other
   'scan-string-tail!/format-placeholder/eof
   'scan-string-tail!/format-placeholder/newline
   'scan-string-tail!/format-placeholder/end
   'scan-string-tail!/format-placeholder/char
   'scan-string-tail!/codepoint/eof
   'scan-string-tail!/codepoint/newline
   'scan-string-tail!/codepoint/end
   'scan-string-tail!/codepoint/invalid-hex
   'scan-string-tail!/codepoint/invalid-range
   'scan-string-tail!/codepoint/char
   'scan-string-tail!/normative/eof
   'scan-string-tail!/normative/newline
   'scan-string-tail!/normative/end
   'scan-string-tail!/normative/char
   'scan-string-tail!/normative/empty
   'scan-string-tail!/normative/invalid-char
   'scan-string-tail!/normative/unknown-name
   'scan-string-tail!/eof
   'scan-string-tail!/newline
   'scan-string-tail!/escaped-colon
   'scan-string-tail!/escaped-quote/end-string
   'scan-string-tail!/escaped-quote/literal
   'scan-string-tail!/escaped-newline
   'scan-string-tail!/escaped-tab
   'scan-string-tail!/escaped-bell
   'scan-string-tail!/escaped-codepoint
   'scan-string-tail!/escaped-normative
   'scan-string-tail!/escaped-placeholder
   'scan-string-tail!/escaped-unknown
   'scan-string-tail!/start-escape
   'scan-string-tail!/end-string
   'scan-string-tail!/plain-char
   'scanner/ws
   'scanner/newline/crlf
   'scanner/newline/lf
   'scanner/newline/cr
   'scanner/newline/comma
   'scanner/string
   'scanner/word/comment
   'scanner/word/block-comment
   'scanner/word/line-continuation
   'scanner/word/ok+line-continuation
   'scanner/word/ok
   'scanner/eof
   'scanner/pending))

(define (lexer-cover! key)
  (when (lexer-coverage-enabled?)
    (hash-set! lexer-coverage-counts
               key
               (+ 1 (hash-ref lexer-coverage-counts key 0)))))

(define (lexer-coverage-reset!)
  (hash-clear! lexer-coverage-counts))

(define (lexer-coverage-snapshot)
  (for/hash ([(k v) (in-hash lexer-coverage-counts)])
    (values k v)))

(define (lex-error who message line col)
  (lexer-cover! 'lex-error)
  (error who "~a at line ~a, col ~a" message line col))

(define (numeric-token? text)
  (regexp-match? #px"^-?[0-9]+(?:\\.[0-9]+)?$" text))

(define (newline-or-return? ch)
  (and (char? ch)
       (or (char=? ch #\newline)
           (char=? ch #\return))))

(define (word->tokens text line col)
  (cond
    [(string-ci=? text "BTW")
     (lexer-cover! 'word->tokens/comment)
     (values 'comment '())]
    [(string-ci=? text "OBTW")
     (lexer-cover! 'word->tokens/block-comment)
     (values 'block-comment '())]
    [(or (string=? text "...")
         (string=? text "…"))
     (lexer-cover! 'word->tokens/line-continuation)
     (values 'line-continuation '())]
    [else
     (define len (string-length text))
     (cond
       [(or (and (> len 3)
                 (string-suffix? text "..."))
            (and (> len 1)
                 (string-suffix? text "…")))
        (define stem
          (if (string-suffix? text "…")
              (substring text 0 (- len 1))
              (substring text 0 (- len 3))))
        (let-values ([(status toks) (word->tokens stem line col)])
          (if (eq? status 'ok)
              (begin
                (lexer-cover! 'word->tokens/ok+line-continuation)
                (values 'ok+line-continuation toks))
              (values status toks)))]
       [(and (> len 2)
             (regexp-match? #px"(?i:^.+\\'Z$)" text))
        (lexer-cover! 'word->tokens/split-slot-z)
        (define base (substring text 0 (- len 2)))
        (define base-token
          (if (numeric-token? base)
              (token 'NUMBER base line col)
              (token 'WORD base line col)))
        (define slot-token
          (token 'WORD "'Z" line (+ col (- len 1))))
        (values 'ok (list base-token slot-token))]
       [(numeric-token? text)
        (lexer-cover! 'word->tokens/number)
        (values 'ok (list (token 'NUMBER text line col)))]
       [else
        (lexer-cover! 'word->tokens/word)
        (values 'ok (list (token 'WORD text line col)))])]))

(define (skip-comment-tail! in)
  (define (loop ch)
    (cond
      [(eof-object? ch)
       (lexer-cover! 'skip-comment-tail!/eof)
       (void)]
      [(newline-or-return? ch)
       (lexer-cover! 'skip-comment-tail!/newline)
       (void)]
      [else
       (lexer-cover! 'skip-comment-tail!/char)
       (read-char in)
       (loop (peek-char in))]))
  (loop (peek-char in)))

(define (word-char? ch)
  (and (char? ch)
       (not (or (char-whitespace? ch)
                (char=? ch #\,)
                (char=? ch #\")))))

(define (skip-block-comment! in)
  (define (loop current-word ch)
    (cond
      [(eof-object? ch)
       (lexer-cover! 'skip-block-comment!/eof)
       (unless (string-ci=? current-word "TLDR")
         (error 'lex-source "unterminated OBTW block comment"))]
      [(word-char? ch)
       (lexer-cover! 'skip-block-comment!/word-char)
       (loop (string-append current-word (string ch))
             (read-char in))]
      [(string-ci=? current-word "TLDR")
       (lexer-cover! 'skip-block-comment!/found-tldr)
       (void)]
      [else
       (lexer-cover! 'skip-block-comment!/delimiter)
       (loop ""
             (read-char in))]))
  (loop "" (read-char in)))

(define (skip-line-continuation! in)
  (define (loop ch)
    (cond
      [(eof-object? ch)
       (lexer-cover! 'skip-line-continuation!/eof)
       (void)]
      [(or (char=? ch #\space) (char=? ch #\tab))
       (lexer-cover! 'skip-line-continuation!/space-or-tab)
       (read-char in)
       (loop (peek-char in))]
      [(char=? ch #\return)
       (lexer-cover! 'skip-line-continuation!/cr)
       (read-char in)
       (define next (peek-char in))
       (when (and (char? next) (char=? next #\newline))
         (lexer-cover! 'skip-line-continuation!/crlf)
         (read-char in))
       (void)]
      [(char=? ch #\newline)
       (lexer-cover! 'skip-line-continuation!/lf)
       (read-char in)
       (void)]
      [else
       (lexer-cover! 'skip-line-continuation!/other)
       (void)]))
  (loop (peek-char in)))

(define (scan-string-format-placeholder! in line col)
  (define placeholder-out (open-output-string))
  (define (loop pch)
    (cond
      [(eof-object? pch)
       (lexer-cover! 'scan-string-tail!/format-placeholder/eof)
       (lex-error 'lex-source "unterminated :{...} placeholder in string literal" line col)]
      [(newline-or-return? pch)
       (lexer-cover! 'scan-string-tail!/format-placeholder/newline)
       (lex-error 'lex-source "unterminated :{...} placeholder in string literal" line col)]
      [(char=? pch #\})
       (lexer-cover! 'scan-string-tail!/format-placeholder/end)
       (get-output-string placeholder-out)]
      [else
       (lexer-cover! 'scan-string-tail!/format-placeholder/char)
       (write-char pch placeholder-out)
       (loop (read-char in))]))
  (loop (read-char in)))

(define (scan-string-codepoint-escape! in line col)
  (define hex-out (open-output-string))
  (define (loop pch)
    (cond
      [(eof-object? pch)
       (lexer-cover! 'scan-string-tail!/codepoint/eof)
       (lex-error 'lex-source "unterminated :(... ) Unicode escape in string literal" line col)]
      [(newline-or-return? pch)
       (lexer-cover! 'scan-string-tail!/codepoint/newline)
       (lex-error 'lex-source "unterminated :(... ) Unicode escape in string literal" line col)]
      [(char=? pch #\))
       (lexer-cover! 'scan-string-tail!/codepoint/end)
       (define hex (get-output-string hex-out))
       (unless (regexp-match? #px"^[0-9A-Fa-f]+$" hex)
         (lexer-cover! 'scan-string-tail!/codepoint/invalid-hex)
         (lex-error 'lex-source "invalid Unicode code point escape in string literal" line col))
       (define cp (string->number hex 16))
       (unless (and cp
                    (<= 0 cp #x10FFFF)
                    (not (<= #xD800 cp #xDFFF)))
         (lexer-cover! 'scan-string-tail!/codepoint/invalid-range)
         (lex-error 'lex-source "invalid Unicode code point in string literal" line col))
       (integer->char cp)]
      [else
       (lexer-cover! 'scan-string-tail!/codepoint/char)
       (write-char pch hex-out)
       (loop (read-char in))]))
  (loop (read-char in)))

(define unicode-normative-name->codepoint
  (hash "DOLLAR SIGN" #x0024
        "CENT SIGN" #x00A2
        "EURO SIGN" #x20AC))

(define (normalize-unicode-normative-name text)
  (regexp-replace* #px"[ \t]+" (string-upcase (string-trim text)) " "))

(define (normative-name-char? ch)
  (or (char-alphabetic? ch)
      (char-numeric? ch)
      (char-whitespace? ch)
      (char=? ch #\-)))

(define (scan-string-normative-name-escape! in line col)
  (define name-out (open-output-string))
  (define (loop pch)
    (cond
      [(eof-object? pch)
       (lexer-cover! 'scan-string-tail!/normative/eof)
       (lex-error 'lex-source "unterminated :[...] Unicode escape in string literal" line col)]
      [(newline-or-return? pch)
       (lexer-cover! 'scan-string-tail!/normative/newline)
       (lex-error 'lex-source "unterminated :[...] Unicode escape in string literal" line col)]
      [(char=? pch #\])
       (lexer-cover! 'scan-string-tail!/normative/end)
       (define normalized
         (normalize-unicode-normative-name (get-output-string name-out)))
       (when (string=? normalized "")
         (lexer-cover! 'scan-string-tail!/normative/empty)
         (lex-error 'lex-source "invalid Unicode normative name in string literal" line col))
       (unless (for/and ([ch (in-string normalized)])
                 (normative-name-char? ch))
         (lexer-cover! 'scan-string-tail!/normative/invalid-char)
         (lex-error 'lex-source "invalid Unicode normative name in string literal" line col))
       (define cp
         (hash-ref unicode-normative-name->codepoint normalized #f))
       (unless cp
         (lexer-cover! 'scan-string-tail!/normative/unknown-name)
         (lex-error 'lex-source "invalid Unicode normative name in string literal" line col))
       (integer->char cp)]
      [else
       (lexer-cover! 'scan-string-tail!/normative/char)
       (write-char pch name-out)
       (loop (read-char in))]))
  (loop (read-char in)))

(define (scan-string-handle-escape! in line col out ch)
  (cond
    [(char=? ch #\:)
     (lexer-cover! 'scan-string-tail!/escaped-colon)
     (write-char #\: out)
     #f]
    [(char=? ch #\")
     (define next (peek-char in))
     (if (or (eof-object? next)
             (newline-or-return? next))
         (begin
           (lexer-cover! 'scan-string-tail!/escaped-quote/end-string)
           (write-char #\: out)
           (get-output-string out))
         (begin
           (lexer-cover! 'scan-string-tail!/escaped-quote/literal)
           (write-char #\" out)
           #f))]
    [(char=? ch #\))
     (lexer-cover! 'scan-string-tail!/escaped-newline)
     (write-char #\newline out)
     #f]
    [(char=? ch #\>)
     (lexer-cover! 'scan-string-tail!/escaped-tab)
     (write-char #\tab out)
     #f]
    [(char-ci=? ch #\o)
     (lexer-cover! 'scan-string-tail!/escaped-bell)
     (write-char #\u0007 out)
     #f]
    [(char=? ch #\()
     (lexer-cover! 'scan-string-tail!/escaped-codepoint)
     (write-char (scan-string-codepoint-escape! in line col) out)
     #f]
    [(char=? ch #\[)
     (lexer-cover! 'scan-string-tail!/escaped-normative)
     (write-char (scan-string-normative-name-escape! in line col) out)
     #f]
    [(char=? ch #\{)
     (lexer-cover! 'scan-string-tail!/escaped-placeholder)
     (display ":{" out)
     (display (scan-string-format-placeholder! in line col) out)
     (write-char #\} out)
     #f]
    [else
     ;; Unknown escape: keep the colon literally.
     (lexer-cover! 'scan-string-tail!/escaped-unknown)
     (write-char #\: out)
     (write-char ch out)
     #f]))

(define (scan-string-tail! in line col)
  (define out (open-output-string))
  (define (loop escaped? ch)
    (cond
      [(eof-object? ch)
       (lexer-cover! 'scan-string-tail!/eof)
       (lex-error 'lex-source "unterminated string literal" line col)]
      [(newline-or-return? ch)
       (lexer-cover! 'scan-string-tail!/newline)
       (lex-error 'lex-source "unterminated string literal" line col)]
      [escaped?
       (define maybe-result
         (scan-string-handle-escape! in line col out ch))
       (if (string? maybe-result)
           maybe-result
           (loop #f (read-char in)))]
      [(char=? ch #\:)
       (lexer-cover! 'scan-string-tail!/start-escape)
       (loop #t (read-char in))]
      [(char=? ch #\")
       (lexer-cover! 'scan-string-tail!/end-string)
       (get-output-string out)]
      [else
       (lexer-cover! 'scan-string-tail!/plain-char)
       (write-char ch out)
       (loop #f (read-char in))]))
  (loop #f (read-char in)))

(define-lex-abbrevs
  [ws (:or #\space #\tab)]
  [word (:+ (:~ #\space #\tab #\, #\newline #\return #\"))])

(define (make-token type lexeme start-pos)
  (token type lexeme
         (position-line start-pos)
         (+ 1 (position-col start-pos))))

(define (make-next-token in)
  (define pending '())
  (define scanner
     (lexer-src-pos
     [ws
      (begin
        (lexer-cover! 'scanner/ws)
        (return-without-pos (scanner in)))]
     [(:: #\return #\newline)
      (begin
        (lexer-cover! 'scanner/newline/crlf)
        (return-without-pos (make-token 'NEWLINE "\n" start-pos)))]
     [#\newline
      (begin
        (lexer-cover! 'scanner/newline/lf)
        (return-without-pos (make-token 'NEWLINE "\n" start-pos)))]
     [#\return
      (begin
        (lexer-cover! 'scanner/newline/cr)
        (return-without-pos (make-token 'NEWLINE "\n" start-pos)))]
     [#\,
      (begin
        (lexer-cover! 'scanner/newline/comma)
        (return-without-pos (make-token 'NEWLINE "," start-pos)))]
     [#\"
      (begin
        (lexer-cover! 'scanner/string)
        (return-without-pos
         (make-token
          'STRING
          (scan-string-tail! in
                             (position-line start-pos)
                             (+ 1 (position-col start-pos)))
          start-pos)))]
     [word
      (let-values ([(status toks)
                    (word->tokens lexeme
                                  (position-line start-pos)
                                  (+ 1 (position-col start-pos)))])
        (cond
          [(eq? status 'comment)
           (lexer-cover! 'scanner/word/comment)
           (skip-comment-tail! in)
           (return-without-pos (scanner in))]
          [(eq? status 'block-comment)
           (lexer-cover! 'scanner/word/block-comment)
           (skip-block-comment! in)
           (return-without-pos (scanner in))]
          [(eq? status 'line-continuation)
           (lexer-cover! 'scanner/word/line-continuation)
           (skip-line-continuation! in)
           (return-without-pos (scanner in))]
          [(eq? status 'ok+line-continuation)
           (lexer-cover! 'scanner/word/ok+line-continuation)
           (skip-line-continuation! in)
           (set! pending (append pending (cdr toks)))
           (return-without-pos (car toks))]
          [else
           (lexer-cover! 'scanner/word/ok)
           (set! pending (append pending (cdr toks)))
           (return-without-pos (car toks))]))]
     [(eof)
      (begin
        (lexer-cover! 'scanner/eof)
        (return-without-pos (make-token 'EOF "" start-pos)))]))
  (lambda ()
    (cond
      [(pair? pending)
       (lexer-cover! 'scanner/pending)
       (define t (car pending))
       (set! pending (cdr pending))
       t]
      [else
       (scanner in)])))

(define (lex-source source)
  (unless (string? source)
    (raise-argument-error 'lex-source "string?" source))
  (define in (open-input-string source))
  (port-count-lines! in)
  (define next-token (make-next-token in))
  (define (loop acc)
    (define tok (next-token))
    (if (eq? (token-type tok) 'EOF)
        (reverse (cons tok acc))
        (loop (cons tok acc))))
  (loop '()))
