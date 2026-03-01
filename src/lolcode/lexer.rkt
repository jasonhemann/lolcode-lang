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
         lex-source)

(struct token (type lexeme line col) #:transparent)

(define (lex-error who message line col)
  (error who "~a at line ~a, col ~a" message line col))

(define (numeric-token? text)
  (regexp-match? #px"^-?[0-9]+(?:\\.[0-9]+)?$" text))

(define (word->tokens text line col)
  (cond
    [(string-ci=? text "BTW")
     (values 'comment '())]
    [(string-ci=? text "OBTW")
     (values 'block-comment '())]
    [(string=? text "...")
     (values 'line-continuation '())]
    [(and (> (string-length text) 3)
          (string-suffix? text "..."))
     (define stem (substring text 0 (- (string-length text) 3)))
     (let-values ([(status toks) (word->tokens stem line col)])
       (if (eq? status 'ok)
           (values 'ok+line-continuation toks)
           (values status toks)))]
    [(and (> (string-length text) 2)
          (regexp-match? #px"(?i:^.+\\'Z$)" text))
     (define base (substring text 0 (- (string-length text) 2)))
     (define base-token
       (if (numeric-token? base)
           (token 'NUMBER base line col)
           (token 'WORD base line col)))
     (define slot-token
       (token 'WORD "'Z" line (+ col (- (string-length text) 1))))
     (values 'ok (list base-token slot-token))]
    [else
     (define t
       (if (numeric-token? text)
           (token 'NUMBER text line col)
           (token 'WORD text line col)))
     (values 'ok (list t))]))

(define (skip-comment-tail! in)
  (let loop ()
    (define ch (peek-char in))
    (cond
      [(eof-object? ch) (void)]
      [(or (char=? ch #\newline) (char=? ch #\return)) (void)]
      [else
       (read-char in)
       (loop)])))

(define (word-char? ch)
  (and (char? ch)
       (not (or (char-whitespace? ch)
                (char=? ch #\,)
                (char=? ch #\")))))

(define (skip-block-comment! in)
  (let loop ([current-word ""])
    (define ch (read-char in))
    (cond
      [(eof-object? ch)
       (unless (string-ci=? current-word "TLDR")
         (error 'lex-source "unterminated OBTW block comment"))]
      [(word-char? ch)
       (loop (string-append current-word (string ch)))]
      [(string-ci=? current-word "TLDR")
       (void)]
      [else
       (loop "")])))

(define (skip-line-continuation! in)
  (let loop ()
    (define ch (peek-char in))
    (cond
      [(eof-object? ch) (void)]
      [(or (char=? ch #\space) (char=? ch #\tab))
       (read-char in)
       (loop)]
      [(char=? ch #\return)
       (read-char in)
       (define next (peek-char in))
       (when (and (char? next) (char=? next #\newline))
         (read-char in))
       (void)]
      [(char=? ch #\newline)
       (read-char in)
       (void)]
      [else (void)])))

(define (scan-string-tail! in line col)
  (define (scan-format-placeholder!)
    (define placeholder-out (open-output-string))
    (let loop ()
      (define pch (read-char in))
      (cond
        [(eof-object? pch)
         (lex-error 'lex-source "unterminated :{...} placeholder in string literal" line col)]
        [(or (char=? pch #\newline) (char=? pch #\return))
         (lex-error 'lex-source "unterminated :{...} placeholder in string literal" line col)]
        [(char=? pch #\})
         (get-output-string placeholder-out)]
        [else
         (write-char pch placeholder-out)
         (loop)])))
  (define out (open-output-string))
  (let loop ([escaped? #f])
    (define ch (read-char in))
    (cond
      [(eof-object? ch)
       (lex-error 'lex-source "unterminated string literal" line col)]
      [(or (char=? ch #\newline) (char=? ch #\return))
       (lex-error 'lex-source "unterminated string literal" line col)]
      [escaped?
       (cond
         [(char=? ch #\:)
          (write-char #\: out)
          (loop #f)]
         [(char=? ch #\")
          (define next (peek-char in))
          (if (or (eof-object? next)
                  (char=? next #\newline)
                  (char=? next #\return))
              (begin
                (write-char #\: out)
                (get-output-string out))
              (begin
                (write-char #\" out)
                (loop #f)))]
         [(char=? ch #\))
          (write-char #\newline out)
          (loop #f)]
         [(char=? ch #\>)
          (write-char #\tab out)
          (loop #f)]
         [(char-ci=? ch #\o)
          (write-char #\u0007 out)
          (loop #f)]
         [(char=? ch #\{)
          (display ":{" out)
          (display (scan-format-placeholder!) out)
          (write-char #\} out)
          (loop #f)]
         [else
          ;; Unknown escape: keep the colon literally.
          (write-char #\: out)
          (write-char ch out)
          (loop #f)])]
      [(char=? ch #\:)
       (loop #t)]
      [(char=? ch #\")
       (get-output-string out)]
      [else
       (write-char ch out)
       (loop #f)])))

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
     [ws (return-without-pos (scanner in))]
     [(:: #\return #\newline)
      (return-without-pos (make-token 'NEWLINE "\n" start-pos))]
     [#\newline
      (return-without-pos (make-token 'NEWLINE "\n" start-pos))]
     [#\return
      (return-without-pos (make-token 'NEWLINE "\n" start-pos))]
     [#\,
      (return-without-pos (make-token 'NEWLINE "," start-pos))]
     [#\"
      (return-without-pos
       (make-token
        'STRING
        (scan-string-tail! in
                           (position-line start-pos)
                           (+ 1 (position-col start-pos)))
        start-pos))]
     [word
      (let-values ([(status toks)
                    (word->tokens lexeme
                                  (position-line start-pos)
                                  (+ 1 (position-col start-pos)))])
        (cond
          [(eq? status 'comment)
           (skip-comment-tail! in)
           (return-without-pos (scanner in))]
          [(eq? status 'block-comment)
           (skip-block-comment! in)
           (return-without-pos (scanner in))]
          [(eq? status 'line-continuation)
           (skip-line-continuation! in)
           (return-without-pos (scanner in))]
          [(eq? status 'ok+line-continuation)
           (skip-line-continuation! in)
           (set! pending (append pending (cdr toks)))
           (return-without-pos (car toks))]
          [else
           (set! pending (append pending (cdr toks)))
           (return-without-pos (car toks))]))]
     [(eof)
      (return-without-pos (make-token 'EOF "" start-pos))]))
  (lambda ()
    (cond
      [(pair? pending)
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
  (let loop ([acc '()])
    (define tok (next-token))
    (if (eq? (token-type tok) 'EOF)
        (reverse (cons tok acc))
        (loop (cons tok acc)))))
