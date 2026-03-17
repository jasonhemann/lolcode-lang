#lang racket/base

(require racket/format
         racket/list
         racket/match
         racket/path
         racket/string)

(provide validate-hash-entry
         validate-entry-list
         make-check
         make-field-rule
         missing-relative-paths
         required-key-errors
         duplicate-string-id-error
         parse-cli-options)

(define (entry-error idx fmt . args)
  (format "entry ~a: ~a" idx (apply format fmt args)))

(define (make-field-rule key required? checks)
  (hasheq 'key key
          'required? required?
          'checks checks))

(define (make-check pred message)
  (hasheq 'pred pred
          'message message))

(define (path-under-root root p)
  (if (absolute-path? p)
      p
      (build-path root p)))

(define (missing-relative-paths root refs)
  (for/list ([ref (in-list refs)]
             #:unless (file-exists? (path-under-root root ref)))
    ref))

(define (required-key-errors entry idx rules)
  (for/list ([rule (in-list rules)]
             #:when (and (hash-ref rule 'required? #f)
                         (not (hash-has-key? entry (hash-ref rule 'key)))))
    (entry-error idx "missing key ~a" (hash-ref rule 'key))))

(define (check-error idx check value ctx)
  (define message-proc (hash-ref check 'message))
  (if (procedure? message-proc)
      (entry-error idx "~a" (message-proc value ctx))
      (entry-error idx "~a" message-proc)))

(define (rule-check-errors entry idx rule ctx)
  (define key (hash-ref rule 'key))
  (if (hash-has-key? entry key)
      (let ([value (hash-ref entry key)]
            [checks (hash-ref rule 'checks '())]
            [check-ctx (hash-set ctx 'key key)])
        (for/list ([check (in-list checks)]
                   #:unless ((hash-ref check 'pred) value check-ctx))
          (check-error idx check value check-ctx)))
      '()))

(define (validate-hash-entry entry idx rules [ctx #hasheq()])
  (if (hash? entry)
      (let ([entry-ctx (hash-set ctx 'entry entry)])
		(append*
		  (required-key-errors entry idx rules)
		  (for/list ([rule (in-list rules)])
			(rule-check-errors entry idx rule entry-ctx))))
      (list (entry-error idx "expected hash entry, got ~e" entry))))

(define (validate-entry-list entries rules [context-builder (lambda (_entry _idx) #hasheq())])
  (append*
   (for/list ([entry (in-list entries)]
              [idx (in-naturals 1)])
     (validate-hash-entry entry idx rules (context-builder entry idx)))))

(define (duplicate-string-id-error ids [prefix "duplicate IDs"])
  (define counts
    (for/fold ([h (hash)])
              ([id (in-list ids)])
      (hash-update h id add1 0)))
  (define dupes
    (sort
     (for/list ([(id count) (in-hash counts)]
                #:when (> count 1))
       id)
     string<?))
  (if (null? dupes)
      #f
      (format "~a: ~a" prefix (string-join dupes ", "))))

(define (find-option-spec specs flag)
  (for/first ([spec (in-list specs)]
              #:when (string=? flag (hash-ref spec 'flag)))
    spec))

(define (apply-option who args spec state)
  (define mode (hash-ref spec 'mode 'value))
  (define key (hash-ref spec 'key))
  (match (cons mode args)
    [(cons 'switch (cons _ rest))
     (values rest
             (hash-set state key (hash-ref spec 'value #t)))]
    [(cons 'value (list _ raw rest ...))
     (define convert (hash-ref spec 'convert values))
     (values rest
             (hash-set state key (convert raw)))]
    [(cons (or 'value 'switch) _)
     (error who "unknown or malformed arguments: ~e" args)]
    [_ (error who "unknown option mode: ~e" mode)]))

(define (parse-cli-options who argv specs defaults)
  (match argv
    ['() defaults]
    [(cons token _)
     (cond
       [(find-option-spec specs token)
        => (lambda (spec)
             (let-values ([(next-args next-state)
                           (apply-option who argv spec defaults)])
               (parse-cli-options who next-args specs next-state)))]
       [else
        (error who "unknown or malformed arguments: ~e" argv)])]))
