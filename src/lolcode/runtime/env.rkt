#lang racket/base

(provide noob
         (struct-out env)
         (struct-out runstate)
         (struct-out exec-ctx)
         ctx-derive
         ctx-return!
         ctx-break!
         make-root-env
         extend-env
         env-with-table
         env-lookup-box
         env-define!
         env-ref
         env-set!
         env-set-or-define!
         set-it!
         runtime-globals
         runtime-stdout)

(define noob 'NOOB)

;; Runtime model (informal types):
;;   Val        := any LOLCODE runtime value
;;   BindingBox := (Boxof Val)
;;   EnvTable   := (Mutable-HashTable String BindingBox)
;; Invariant: every binding stored in an `env` table is a box.
(struct env (table parent) #:transparent)
(struct runstate (globals stdout phase) #:transparent)
(struct exec-ctx (state return-k break-k object-name def-object) #:transparent)

(define (ctx-derive ctx
                    #:return-k [return-k (exec-ctx-return-k ctx)]
                    #:break-k [break-k (exec-ctx-break-k ctx)]
                    #:object-name [object-name (exec-ctx-object-name ctx)]
                    #:def-object [def-object (exec-ctx-def-object ctx)])
  (exec-ctx (exec-ctx-state ctx)
            return-k
            break-k
            object-name
            def-object))

(define (ctx-return! ctx value)
  (cond
    [(exec-ctx-return-k ctx)
     => (lambda (k)
          (k value))]
    [(exec-ctx-object-name ctx)
     (error 'run-program
            "FOUND YR used inside object definition ~a"
            (exec-ctx-object-name ctx))]
    [else
     (error 'run-program "FOUND YR used outside function")]))

(define (ctx-break! ctx)
  (cond
    [(exec-ctx-break-k ctx)
     => (lambda (k)
          (k (void)))]
    [(exec-ctx-return-k ctx)
     (ctx-return! ctx noob)]
    [(exec-ctx-object-name ctx)
     (error 'run-program
            "GTFO used inside object definition ~a"
            (exec-ctx-object-name ctx))]
    [else
     (error 'run-program "GTFO used outside switch/loop")]))

(define (make-root-env)
  (env (make-hash) #f))

(define (extend-env parent)
  (env (make-hash) parent))

(define (env-with-table table parent)
  (env table parent))

(define (env-lookup-box e name)
  (let loop ([cur e])
    (cond
      [(not cur) #f]
      [(hash-has-key? (env-table cur) name)
       (define maybe-box
         (hash-ref (env-table cur) name))
       (unless (box? maybe-box)
         (error 'run-program
                "runtime invariant violation: non-box binding in env table for identifier ~a: ~e"
                name
                maybe-box))
       maybe-box]
      [else
       (loop (env-parent cur))])))

(define (env-define! e name value)
  (when (hash-has-key? (env-table e) name)
    (error 'run-program "identifier already declared in this scope: ~a" name))
  (hash-set! (env-table e) name (box value)))

(define (env-ref e name)
  (cond
    [(env-lookup-box e name) => unbox]
    [else
     (error 'run-program "unknown identifier: ~a" name)]))

(define (env-set! e name value)
  (cond
    [(env-lookup-box e name)
     => (lambda (b)
          (set-box! b value))]
    [else
     (error 'run-program "unknown identifier: ~a" name)]))

(define (env-set-or-define! e name value)
  (cond
    [(env-lookup-box e name)
     => (lambda (b)
          (set-box! b value))]
    [else
     (env-define! e name value)]))

(define (set-it! e value)
  (cond
    [(env-lookup-box e "IT")
     => (lambda (maybe-it)
          (set-box! maybe-it value))]
    [else (env-define! e "IT" value)]))

(define (runtime-globals ctx)
  (runstate-globals
   (exec-ctx-state ctx)))

(define (runtime-stdout ctx)
  (runstate-stdout
   (exec-ctx-state ctx)))
