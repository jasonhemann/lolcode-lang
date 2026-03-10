#lang racket/base

(require racket/match
         racket/port
         racket/string
         parser-tools/lex
         (prefix-in : parser-tools/lex-sre)
         "format-placeholder.rkt")

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
   'word->tokens/split-slot-dash
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
   'skip-line-continuation!/blank-line
   'skip-line-continuation!/blank-line-allowed
   'skip-line-continuation!/blank-line-error
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

(define (malformed-number-token? text)
  (and (regexp-match? #px"^-?[0-9][0-9.]*$" text)
       (not (numeric-token? text))))

(define (newline-or-return? ch)
  (and (char? ch)
       (or (char=? ch #\newline)
           (char=? ch #\return))))

(define (horizontal-space? ch)
  (and (char? ch)
       (or (char=? ch #\space)
           (char=? ch #\tab))))

(define (comma-char? ch)
  (and (char? ch) (char=? ch #\,)))

(define (valid-tail-after-tldr-space! in)
  (define next (peek-char in))
  (cond
    [(eof-object? next) #t]
    [(horizontal-space? next)
     (read-char in)
     (valid-tail-after-tldr-space! in)]
    [(newline-or-return? next) #t]
    [(comma-char? next) #t]
    [else #f]))

(define (valid-tldr-delimiter? in ch)
  (cond
    [(newline-or-return? ch) #t]
    [(comma-char? ch) #t]
    [(horizontal-space? ch)
     (valid-tail-after-tldr-space! in)]
    [else #f]))

(define (word->tokens text line col)
  (match text
    ["BTW"
     (lexer-cover! 'word->tokens/comment)
     (values 'comment '())]
    ["OBTW"
     (lexer-cover! 'word->tokens/block-comment)
     (values 'block-comment '())]
    [(or "..." "…")
     (lexer-cover! 'word->tokens/line-continuation)
     (values 'line-continuation '())]
    [_
     (define len (string-length text))
     (cond
       [(and (> len 3) (string-suffix? text "..."))
        (lex-word-with-trailing-line-continuation text line col 3)]
       [(and (> len 1) (string-suffix? text "…"))
        (lex-word-with-trailing-line-continuation text line col 1)]
       [(and (> len 2) (string-suffix? text "'Z"))
        (lexer-cover! 'word->tokens/split-slot-z)
        (define base (substring text 0 (- len 2)))
        (define base-token (word-or-number-token base line col))
        (define slot-token (token 'WORD "'Z" line (+ col (- len 1))))
        (values 'ok (list base-token slot-token))]
       [(regexp-match #px"^([A-Za-z][A-Za-z0-9_]*)-([A-Za-z][A-Za-z0-9_]*)$" text)
        => (lambda (m)
             (lexer-cover! 'word->tokens/split-slot-dash)
             (define base (list-ref m 1))
             (define slot (list-ref m 2))
             (define base-len (string-length base))
             (define base-token (token 'WORD base line col))
             (define dash-token (token 'WORD "-" line (+ col base-len)))
             (define slot-token (token 'WORD slot line (+ col base-len 1)))
             (values 'ok (list base-token dash-token slot-token)))]
       [(numeric-token? text)
        (lexer-cover! 'word->tokens/number)
        (values 'ok (list (token 'NUMBER text line col)))]
       [(malformed-number-token? text)
        (lex-error 'lex-source "invalid numeric literal" line col)]
       [else
        (lexer-cover! 'word->tokens/word)
        (values 'ok (list (token 'WORD text line col)))])]))

(define (word-or-number-token text line col)
  (if (numeric-token? text)
      (token 'NUMBER text line col)
      (token 'WORD text line col)))

(define (promote-line-continuation-status status toks)
  (if (eq? status 'ok)
      (begin
        (lexer-cover! 'word->tokens/ok+line-continuation)
        (values 'ok+line-continuation toks))
      (values status toks)))

(define (lex-word-with-trailing-line-continuation text line col suffix-len)
  (define stem (substring text 0 (- (string-length text) suffix-len)))
  (let-values ([(status toks) (word->tokens stem line col)])
    (promote-line-continuation-status status toks)))

(define (skip-comment-tail! in)
  (define ch (peek-char in))
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
     (skip-comment-tail! in)]))

(define (word-char? ch)
  (and (char? ch)
       (not (or (char-whitespace? ch)
                (comma-char? ch)
                (char=? ch #\")))))

(define (skip-block-comment! in [current-word ""] [ch (read-char in)])
  (cond
    [(eof-object? ch)
     (lexer-cover! 'skip-block-comment!/eof)
     (unless (string=? current-word "TLDR")
       (error 'lex-source "unterminated OBTW block comment"))]
    [(word-char? ch)
     (lexer-cover! 'skip-block-comment!/word-char)
     (skip-block-comment! in (string-append current-word (string ch)) (read-char in))]
    [(string=? current-word "TLDR")
     (lexer-cover! 'skip-block-comment!/found-tldr)
     (define delimiter-valid? (valid-tldr-delimiter? in ch))
     (unless delimiter-valid? (error 'lex-source "TLDR must be followed by newline or comma"))
     (void)]
    [else
     (lexer-cover! 'skip-block-comment!/delimiter)
     (skip-block-comment! in "" (read-char in))]))

(define (skip-line-continuation! in line col allow-empty-line?)
  (define (consume-horizontal-space!)
    (define ch (peek-char in))
    (when (horizontal-space? ch)
      (lexer-cover! 'skip-line-continuation!/space-or-tab)
      (read-char in)
      (consume-horizontal-space!)))
  (define (consume-newline!)
    (define ch (peek-char in))
    (cond
      [(eof-object? ch)
       (lexer-cover! 'skip-line-continuation!/eof)
       'eof]
      [(char=? ch #\return)
       (lexer-cover! 'skip-line-continuation!/cr)
       (read-char in)
       (define next (peek-char in))
       (when (and (char? next) (char=? next #\newline))
         (lexer-cover! 'skip-line-continuation!/crlf)
         (read-char in))
       'newline]
      [(char=? ch #\newline)
       (lexer-cover! 'skip-line-continuation!/lf)
       (read-char in)
       'newline]
      [else
       (lexer-cover! 'skip-line-continuation!/other)
       'other]))
  (consume-horizontal-space!)
  (case (consume-newline!)
    [(eof)
     (lex-error 'lex-source
                "line continuation must be followed by another line"
                line
                col)]
    [(other)
     (lex-error 'lex-source
                "line continuation marker must be at end of line"
                line
                col)]
    [else
     (void)])
  (consume-horizontal-space!)
  (define next (peek-char in))
  (cond
    [(eof-object? next)
     (lex-error 'lex-source
                "line continuation must be followed by another line"
                line
                col)]
    [(newline-or-return? next)
     (lexer-cover! 'skip-line-continuation!/blank-line)
     (if allow-empty-line?
         (begin
           (lexer-cover! 'skip-line-continuation!/blank-line-allowed)
           (consume-newline!)
           (void))
         (begin
           (lexer-cover! 'skip-line-continuation!/blank-line-error)
           (lex-error 'lex-source
                      "line continuation may not be followed by an empty line"
                      line
                      col)))]
    [else
     (void)]))

(define (scan-string-format-placeholder! in
                                         line
                                         col
                                         [placeholder-out (open-output-string)]
                                         [pch (read-char in)])
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
     (scan-string-format-placeholder! in line col placeholder-out (read-char in))]))

(define (scan-string-codepoint-escape! in
                                       line
                                       col
                                       [hex-out (open-output-string)]
                                       [pch (read-char in)])
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
     (unless (and cp (<= 0 cp #x10FFFF) (not (<= #xD800 cp #xDFFF)))
       (lexer-cover! 'scan-string-tail!/codepoint/invalid-range)
       (lex-error 'lex-source "invalid Unicode code point in string literal" line col))
     (integer->char cp)]
    [else
     (lexer-cover! 'scan-string-tail!/codepoint/char)
     (write-char pch hex-out)
     (scan-string-codepoint-escape! in line col hex-out (read-char in))]))

(define unicode-normative-name->codepoint-cache #f)

(define (normative-name-char? ch)
  (or (char-alphabetic? ch)
      (char-numeric? ch)
      (char=? ch #\space)
      (char=? ch #\-)))

(define (valid-normative-name? text)
  (and (not (string=? text ""))
       (for/and ([ch (in-string text)])
         (and (normative-name-char? ch)
              (or (not (char-alphabetic? ch))
                  (char-upper-case? ch))))))

(define (load-unicode-normative-name-table)
  (with-handlers ([exn:fail?
                   (lambda (e)
                     (error 'lex-source
                            (string-append
                             "Unicode normative-name escapes require Racket's codepoint data: "
                             (exn-message e))))])
    (define name-table-path (collection-file-path "generated/name.rkt-src" "codepoint"))
    (define cp->name (call-with-input-file name-table-path read))
    (unless (hash? cp->name)
      (error 'lex-source "invalid codepoint name table format"))
    (define table (make-hash))
    (for ([(cp raw-name) (in-hash cp->name)])
      (when (and (exact-nonnegative-integer? cp)
                 (string? raw-name))
        (when (and (valid-normative-name? raw-name)
                   (not (hash-has-key? table raw-name)))
          (hash-set! table raw-name cp))))
    table))

(define (unicode-normative-name->codepoint normalized-name)
  (unless (hash? unicode-normative-name->codepoint-cache)
    (set! unicode-normative-name->codepoint-cache
          (load-unicode-normative-name-table)))
  (hash-ref unicode-normative-name->codepoint-cache normalized-name #f))

(define (scan-string-normative-name-escape! in
                                            line
                                            col
                                            [name-out (open-output-string)]
                                            [pch (read-char in)])
  (cond
    [(eof-object? pch)
     (lexer-cover! 'scan-string-tail!/normative/eof)
     (lex-error 'lex-source "unterminated :[...] Unicode escape in string literal" line col)]
    [(newline-or-return? pch)
     (lexer-cover! 'scan-string-tail!/normative/newline)
     (lex-error 'lex-source "unterminated :[...] Unicode escape in string literal" line col)]
    [(char=? pch #\])
     (lexer-cover! 'scan-string-tail!/normative/end)
     (define name
       (get-output-string name-out))
     (when (string=? name "")
       (lexer-cover! 'scan-string-tail!/normative/empty)
       (lex-error 'lex-source "invalid Unicode normative name in string literal" line col))
     (unless (valid-normative-name? name)
       (lexer-cover! 'scan-string-tail!/normative/invalid-char)
       (lex-error 'lex-source "invalid Unicode normative name in string literal" line col))
     (define cp (unicode-normative-name->codepoint name))
     (unless cp
       (lexer-cover! 'scan-string-tail!/normative/unknown-name)
       (lex-error 'lex-source "invalid Unicode normative name in string literal" line col))
     (integer->char cp)]
    [else
     (lexer-cover! 'scan-string-tail!/normative/char)
     (write-char pch name-out)
     (scan-string-normative-name-escape! in line col name-out (read-char in))]))

(struct string-scan-state (text-rev parts-rev) #:transparent)

(define empty-string-scan-state
  (string-scan-state '() '()))

(define (string-scan-state-emit-char st ch)
  (string-scan-state (cons ch (string-scan-state-text-rev st))
                     (string-scan-state-parts-rev st)))

(define (string-scan-state-flush-text st)
  (match st
    [(string-scan-state '() _) st]
    [(string-scan-state text-rev parts-rev)
     (string-scan-state '() (cons (yarn-part-text (list->string (reverse text-rev))) parts-rev))]))

(define (string-scan-state-emit-placeholder st raw-name)
  (define flushed (string-scan-state-flush-text st))
  (string-scan-state '() (cons (yarn-part-placeholder raw-name)
                               (string-scan-state-parts-rev flushed))))

(define (string-scan-state-finish-template st)
  (define flushed (string-scan-state-flush-text st))
  (make-yarn-template (reverse (string-scan-state-parts-rev flushed))))

(struct scan-step-continue (escaped? st) #:transparent)
(struct scan-step-final (template) #:transparent)

(define (scan-string-tail/continue in line col escaped? st)
  (scan-string-tail/step! in
                          line
                          col
                          escaped?
                          (read-char in)
                          st))

(define scan-string-simple-escape-handlers
  (hash
   #\:
   (lambda (_in _line _col st)
     (lexer-cover! 'scan-string-tail!/escaped-colon)
     (scan-step-continue #f (string-scan-state-emit-char st #\:)))
   #\)
   (lambda (_in _line _col st)
     (lexer-cover! 'scan-string-tail!/escaped-newline)
     (scan-step-continue #f (string-scan-state-emit-char st #\newline)))
   #\>
   (lambda (_in _line _col st)
     (lexer-cover! 'scan-string-tail!/escaped-tab)
     (scan-step-continue #f (string-scan-state-emit-char st #\tab)))
   #\o
   (lambda (_in _line _col st)
     (lexer-cover! 'scan-string-tail!/escaped-bell)
     (scan-step-continue #f (string-scan-state-emit-char st #\u0007)))
   #\(
   (lambda (in line col st)
     (lexer-cover! 'scan-string-tail!/escaped-codepoint)
     (scan-step-continue #f
                         (string-scan-state-emit-char
                          st
                          (scan-string-codepoint-escape! in line col))))
   #\[
   (lambda (in line col st)
     (lexer-cover! 'scan-string-tail!/escaped-normative)
     (scan-step-continue #f
                         (string-scan-state-emit-char
                          st
                          (scan-string-normative-name-escape! in line col))))
   #\{
   (lambda (in line col st)
     (lexer-cover! 'scan-string-tail!/escaped-placeholder)
     (scan-step-continue #f
                         (string-scan-state-emit-placeholder
                          st
                          (scan-string-format-placeholder! in line col))))))

(define (scan-string-escaped-step in line col ch st)
  (cond
    [(hash-ref scan-string-simple-escape-handlers ch #f)
     => (lambda (handler)
          (handler in line col st))]
    [(char=? ch #\")
     (define next (peek-char in))
     (if (or (eof-object? next) (newline-or-return? next))
         (begin
           (lexer-cover! 'scan-string-tail!/escaped-quote/end-string)
           (scan-step-final
            (string-scan-state-finish-template
             (string-scan-state-emit-char st #\:))))
         (begin
           (lexer-cover! 'scan-string-tail!/escaped-quote/literal)
           (scan-step-continue #f (string-scan-state-emit-char st #\"))))]
    [else
     ;; Unknown escape: keep the colon literally.
     (lexer-cover! 'scan-string-tail!/escaped-unknown)
     (scan-step-continue
      #f
      (string-scan-state-emit-char
       (string-scan-state-emit-char st #\:)
       ch))]))

(define (scan-string-tail/step! in line col escaped? ch st)
  (cond
    [(eof-object? ch)
     (lexer-cover! 'scan-string-tail!/eof)
     (lex-error 'lex-source "unterminated string literal" line col)]
    [(newline-or-return? ch)
     (lexer-cover! 'scan-string-tail!/newline)
     (lex-error 'lex-source "unterminated string literal" line col)]
    [escaped?
     (match (scan-string-escaped-step in line col ch st)
       [(scan-step-final template) template]
       [(scan-step-continue escaped-next st-next)
        (scan-string-tail/continue in line col escaped-next st-next)])]
    [(char=? ch #\:)
     (lexer-cover! 'scan-string-tail!/start-escape)
     (scan-string-tail/continue in line col #t st)]
    [(char=? ch #\")
     (lexer-cover! 'scan-string-tail!/end-string)
     (string-scan-state-finish-template st)]
    [else
     (lexer-cover! 'scan-string-tail!/plain-char)
     (scan-string-tail/continue in line col #f (string-scan-state-emit-char st ch))]))

(define (scan-string-tail! in line col)
  (scan-string-tail/step! in line col #f (read-char in) empty-string-scan-state))

(define-lex-abbrevs
  [ws (:or #\space #\tab)]
  [word (:+ (:~ #\space #\tab #\, #\newline #\return #\"))])

(define (make-token type lexeme start-pos)
  (token type lexeme
         (position-line start-pos)
         (+ 1 (position-col start-pos))))

(struct pending-queue (front back) #:transparent)

(define (pending-queue-empty? q)
  (and (null? (pending-queue-front q))
       (null? (pending-queue-back q))))

(define (pending-queue-enqueue-all q toks)
  (pending-queue (pending-queue-front q)
                 (foldl cons (pending-queue-back q) toks)))

(define (pending-queue-dequeue q)
  (match-define-values (front back)
    (if (null? (pending-queue-front q))
        (values (reverse (pending-queue-back q)) '())
        (values (pending-queue-front q)
                (pending-queue-back q))))
  (match front
    [(cons next rest)
     (values next (pending-queue rest back))]
    ['()
     (error 'pending-queue-dequeue
            "dequeue from empty pending queue")]))

(define (make-next-token in)
  ;; Pending token queue, represented as two lists (front/back) for
  ;; amortized O(1) enqueue/dequeue.
  (define pending (pending-queue '() '()))
  (define line-has-token? #f)
  ;; Tokens returned from an `ok+line-continuation` lexeme were parsed before
  ;; the consumed newline. Do not let them affect the next physical line state.
  (define suppress-line-state-updates 0)
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
           (skip-line-continuation! in
                                    (position-line start-pos)
                                    (+ 1 (position-col start-pos))
                                    (not line-has-token?))
           (set! line-has-token? #f)
           (return-without-pos (scanner in))]
          [(eq? status 'ok+line-continuation)
           (lexer-cover! 'scanner/word/ok+line-continuation)
           (skip-line-continuation! in
                                    (position-line start-pos)
                                    (+ 1 (position-col start-pos))
                                    #f)
           (set! line-has-token? #f)
           (set! suppress-line-state-updates
                 (+ suppress-line-state-updates (length toks)))
           (set! pending
                 (pending-queue-enqueue-all pending (cdr toks)))
           (return-without-pos (car toks))]
          [else
           (lexer-cover! 'scanner/word/ok)
           (set! pending
                 (pending-queue-enqueue-all pending (cdr toks)))
           (return-without-pos (car toks))]))]
     [(eof)
      (begin
        (lexer-cover! 'scanner/eof)
        (return-without-pos (make-token 'EOF "" start-pos)))]))
  (lambda ()
    (define t
      (cond
        [(not (pending-queue-empty? pending))
         (lexer-cover! 'scanner/pending)
         (define-values (next q*)
           (pending-queue-dequeue pending))
         (set! pending q*)
         next]
        [else
         (scanner in)]))
    (if (> suppress-line-state-updates 0)
        (set! suppress-line-state-updates (- suppress-line-state-updates 1))
        (cond
          [(eq? (token-type t) 'NEWLINE)
           (set! line-has-token? #f)]
          [(not (eq? (token-type t) 'EOF))
           (set! line-has-token? #t)]))
    t))

(define (collect-lexed-tokens next-token)
  (define-values (acc _done?)
    (for/fold ([acc '()] [done? #f])
              ([_ (in-naturals)]
               #:break done?)
      (define tok (next-token))
      (define done-now? (eq? (token-type tok) 'EOF))
      (values (cons tok acc) done-now?)))
  (reverse acc))

(define (lex-source source)
  (unless (string? source)
    (raise-argument-error 'lex-source "string?" source))
  (define in (open-input-string source))
  (port-count-lines! in)
  (define next-token (make-next-token in))
  (collect-lexed-tokens next-token))
