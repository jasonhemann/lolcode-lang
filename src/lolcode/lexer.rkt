#lang racket/base

(require racket/string)
(require racket/port)

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

(define (scan-string line i line-no col)
  (define n (string-length line))
  (define out (open-output-string))
  (let loop ([j (+ i 1)] [escaped? #f])
    (when (>= j n)
      (lex-error 'lex-source "unterminated string literal" line-no col))
    (define ch (string-ref line j))
    (cond
      [escaped?
       (write-char ch out)
       (loop (+ j 1) #f)]
      [(char=? ch #\:)
       (write-char ch out)
       (loop (+ j 1) #t)]
      [(char=? ch #\")
       (values (get-output-string out) (+ j 1))]
      [else
       (write-char ch out)
       (loop (+ j 1) #f)])))

(define (lex-line line line-no)
  (define n (string-length line))
  (let loop ([i 0] [col 1] [acc '()])
    (cond
      [(>= i n) (reverse acc)]
      [else
       (define ch (string-ref line i))
       (cond
         [(or (char=? ch #\space) (char=? ch #\tab))
          (loop (+ i 1) (+ col 1) acc)]
         [(char=? ch #\,)
          (loop (+ i 1) (+ col 1) (cons (token 'NEWLINE "," line-no col) acc))]
         [(char=? ch #\")
          (define-values (text next-i) (scan-string line i line-no col))
          (define consumed (- next-i i))
          (loop next-i (+ col consumed) (cons (token 'STRING text line-no col) acc))]
         [else
          (define j
            (let walk ([k i])
              (cond
                [(>= k n) k]
                [else
                 (define c (string-ref line k))
                 (if (or (char=? c #\space) (char=? c #\tab) (char=? c #\,))
                     k
                     (walk (+ k 1)))])))
          (define text (substring line i j))
          (define-values (status toks) (word->tokens text line-no col))
          (cond
            [(eq? status 'comment)
             (reverse acc)]
            [else
             (loop j (+ col (- j i)) (append (reverse toks) acc))])])])))

(define (lex-source source)
  (unless (string? source)
    (raise-argument-error 'lex-source "string?" source))
  (define tokens '())
  (with-input-from-string source
    (lambda ()
      (let loop ([line-no 1])
        (define line (read-line (current-input-port) 'any))
        (unless (eof-object? line)
          (set! tokens (append tokens (lex-line line line-no)))
          (set! tokens (append tokens (list (token 'NEWLINE "\\n" line-no (+ (string-length line) 1)))))
          (loop (+ line-no 1))))))
  (append tokens (list (token 'EOF "" (+ (length (string-split source "\n" #:trim? #f)) 1) 1))))
