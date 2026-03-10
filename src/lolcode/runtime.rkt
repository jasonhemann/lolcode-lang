#lang racket/base

(require racket/class
         racket/list
         racket/match
         racket/set
         racket/string
         "ast.rkt"
         "format-placeholder.rkt"
         "runtime/env.rkt"
         "runtime/value.rkt"
         "runtime/operators.rkt")

(provide compile-program
         execute-program)

(struct exn:fail:unsupported exn:fail (where) #:transparent)

(define (raise-unsupported where)
  (raise
   (exn:fail:unsupported
    (format "unsupported AST form: ~e" where)
    (current-continuation-marks)
    where)))

(define (raise-unsupported-op kind op where)
  (raise
   (exn:fail:unsupported
    (format "unsupported ~a operator: ~a" kind op)
    (current-continuation-marks)
    where)))

(define (compile-slot-name slot)
  (match slot
    [(expr-ident name) (lambda (_e _ctx) name)]
    [(expr-srs inner)
     (define inner-proc (compile-expr inner))
     (lambda (e ctx)
       (identifier-text
        "SRS slot must evaluate to identifier text"
        (inner-proc e ctx)))]
    [_ (raise-unsupported slot)]))

(define (compile-target-name target)
  (match target
    [(expr-ident name) (lambda (_e _ctx) name)]
    [(expr-srs inner)
     (define inner-proc (compile-expr inner))
     (lambda (e ctx)
       (identifier-text
        "SRS target must evaluate to identifier text"
        (inner-proc e ctx)))]
    [_ (raise-unsupported target)]))

(struct lvalue (read write) #:transparent)

(define (compile-name-resolver who name-spec)
  (match name-spec
    [(expr-literal value)
     (lambda (_e _ctx)
       (identifier-text who value))]
    [(expr-srs inner)
     (define inner-proc (compile-expr inner))
     (lambda (e ctx)
       (identifier-text who (inner-proc e ctx)))]
    [_ (error 'run-program "invalid name spec: ~e" name-spec)]))

(define (compile-lvalue target #:define-missing? [define-missing? #f])
  (match target
    [(or (expr-ident _) (expr-srs _))
     (define name-proc (compile-target-name target))
     (define (lv-read e ctx)
       (env-ref e (name-proc e ctx)))
     (define (lv-write e value ctx)
       (define name (name-proc e ctx))
       (cond
         [(env-lookup-box e name)
          => (lambda (b) (set-box! b value))]
         [define-missing?
          (env-define! e name value)]
         [else
          (error 'run-program "unknown identifier: ~a" name)]))
     (lvalue lv-read lv-write)]
    [(expr-slot object slot)
     (define object-proc (compile-expr object))
     (define slot-name-proc (compile-slot-name slot))
     (define (lv-read e ctx)
       (read-slot-value
        (resolve-bukkit-from-proc "slot lookup" object-proc e ctx)
        (slot-name-proc e ctx)
        ctx))
     (define (lv-write e value ctx)
       (send (resolve-bukkit-from-proc "slot assignment" object-proc e ctx)
             assign-slot!
             (slot-name-proc e ctx)
             value))
     (lvalue lv-read lv-write)]
    [_ (raise-unsupported target)]))

(define (resolve-callable e ctx name who)
  (define maybe-callable
    (let ([maybe-box (env-lookup-box e name)])
      (and maybe-box (unbox maybe-box))))
  (if (procedure? maybe-callable)
      maybe-callable
      (error 'run-program "unknown ~a: ~a" who name)))

(define reserved-binding-names
  (set "WIN" "FAIL" "NOOB" "NUMBR" "NUMBAR" "YARN" "TROOF" "TYPE" "ME"))

(define (ensure-bindable-name who name)
  (when (set-member? reserved-binding-names name)
    (error 'run-program
           "~a uses reserved identifier name: ~a"
           who
           name))
  name)

(define (compile-declare-init init-expr)
  (cond
    [(not init-expr)
     (lambda (_e _ctx) noob)]
    [(expr-type-default? init-expr)
     (compile-expr init-expr)]
    [(expr-ident? init-expr)
     (define type-name (expr-ident-name init-expr))
     (define-values (known? default-value)
       (type-default-value type-name))
     (if known?
         (if (string=? type-name "BUKKIT")
             (lambda (_e _ctx) (new lol-object%))
             (lambda (_e _ctx) default-value))
         (compile-expr init-expr))]
    [else (compile-expr init-expr)]))

(define (loop-continue? e cond-kind cond-proc ctx)
  (cond
    [(not cond-kind) #t]
    [else
     (define cond-value (lol-truthy? (cond-proc e ctx)))
     (case (string->symbol cond-kind)
       [(TIL) (not cond-value)]
       [(WILE) cond-value]
       [else (error 'run-program "unknown loop condition mode: ~a" cond-kind)])]))

(define (make-loop-env e update-var)
  (define loop-env (extend-env e))
  (when update-var
    (define initial
      (cond
        [(env-lookup-box e update-var) => unbox]
        [else 0]))
    ;; Iteration variable is temporary and local to this loop.
    (env-define! loop-env update-var initial))
  loop-env)

(define (apply-loop-update! e update-var update-op ctx)
  (when (and update-var update-op)
    (define current
      (cond
        [(env-lookup-box e update-var) => unbox]
        [else
         (error 'run-program
                "loop variable missing during update: ~a"
                update-var)]))
    (define updated (update-op e ctx current))
    (env-set! e update-var updated)
    (set-it! e updated)))

(define (run-compiled-loop! loop-env
                            loop-ctx
                            cond-kind
                            cond-proc
                            body-proc
                            resolved-update-var
                            resolved-update-op)
  (when (loop-continue? loop-env cond-kind cond-proc loop-ctx)
    (body-proc (extend-env loop-env) loop-ctx)
    (apply-loop-update! loop-env resolved-update-var resolved-update-op loop-ctx)
    (run-compiled-loop! loop-env
                        loop-ctx
                        cond-kind
                        cond-proc
                        body-proc
                        resolved-update-var
                        resolved-update-op)))

(define (compile-loop-update-op update-op)
  (match update-op
    [#f
     (lambda (_e _ctx) #f)]
    [(list 'delta (? number? delta))
     (lambda (_e _ctx)
       (lambda (_loop-env _loop-ctx current)
         (+ (coerce-number 'LOOP current) delta)))]
    [(list 'call updater-name-spec)
     (define updater-name-proc
       (compile-name-resolver
        "loop updater function name must evaluate to identifier text"
        updater-name-spec))
     (lambda (e ctx)
       (define fn-name
         (updater-name-proc e ctx))
       (lambda (loop-env loop-ctx current)
         (define fn
           (resolve-callable loop-env loop-ctx fn-name "function"))
         (fn loop-env (list current) loop-ctx)))]
    [_ (error 'run-program "unsupported loop updater specification: ~e" update-op)]))

(define (ensure-loop-labels-match open-label-proc close-label-proc e ctx)
  (define resolved-open (open-label-proc e ctx))
  (define resolved-close (close-label-proc e ctx))
  (unless (string=? resolved-open resolved-close)
    (error 'run-program
           "loop label mismatch: ~a closed by ~a"
           resolved-open
           resolved-close)))

(define (run-compiled-loop-stmt! e
                                 ctx
                                 open-label-proc
                                 close-label-proc
                                 update-var-proc
                                 update-op-proc
                                 cond-kind
                                 cond-proc
                                 body-proc)
  (ensure-loop-labels-match open-label-proc close-label-proc e ctx)
  (define resolved-update-var (and update-var-proc (update-var-proc e ctx)))
  (define resolved-update-op (update-op-proc e ctx))
  (define loop-env (make-loop-env e resolved-update-var))
  (let/ec break-k
    (define loop-ctx (ctx-derive ctx #:break-k break-k))
    (run-compiled-loop! loop-env
                        loop-ctx
                        cond-kind
                        cond-proc
                        body-proc
                        resolved-update-var
                        resolved-update-op)))

(define (expand-format-placeholders e text)
  (define template (ensure-yarn-template text))
  (define out (open-output-string))
  (for ([part (in-list (yarn-template-parts template))])
    (match part
      [(yarn-part-text literal) (display literal out)]
      [(yarn-part-placeholder raw-name)
       (define name (string-trim raw-name))
       (when (string=? name "")
         (error 'run-program "empty :{...} placeholder in YARN literal"))
       (display (lol-string (env-ref e name)) out)]))
  (get-output-string out))

(define (resolve-bukkit who value)
  (unless (lol-object? value)
    (error 'run-program "~a requires BUKKIT, got ~e" who value))
  value)

(define (resolve-bukkit-from-proc who object-proc e ctx)
  (resolve-bukkit who (object-proc e ctx)))

(define (for-each-right f xs)
  (match xs
    ['() (void)]
    [(cons x rst)
     (for-each-right f rst)
     (f x)]))

(define (apply-mixins! target mixins)
  ;; Spec says mixins are applied in reverse declaration order.
  (for-each-right
    (lambda (mix) (send mix copy-visible-into! target))
    mixins))

(define (run-izmakin-hook! obj _e ctx)
  (define maybe-slot-hook
    (send obj lookup-special-procedure-slot "izmakin"))
  (when (procedure? maybe-slot-hook)
    (invoke-slot-callable obj maybe-slot-hook '() ctx)))

(define (project-receiver-slot-frame receiver)
  (define own-table (send receiver slot-table))
  ;; Table keys/shape are built immutably; per-slot values remain boxed and
  ;; therefore mutable through lexical env operations.
  (define-values (own-projected own-slot-names)
    (for/fold ([projected-table (hash)]
               [own-slot-names (set)])
              ([(name b) (in-hash own-table)])
      (values (hash-set projected-table name b)
              (set-add own-slot-names name))))
  (define-values (projected-table inherited-before)
    (for/fold ([projected-table own-projected]
               [inherited-before (hash)])
              ([name (in-list (send receiver slot-names))])
      (if (hash-has-key? projected-table name)
          (values projected-table inherited-before)
          (let ([v (send receiver lookup-slot name noob)])
            (values (hash-set projected-table name (box v))
                    ;; Snapshot inherited values in boxes as well, so the
                    ;; projection/sync path has one representation shape.
                    (hash-set inherited-before name (box v)))))))
  (values projected-table own-slot-names inherited-before))

(define (sync-receiver-slot-frame! receiver projected-table own-slot-names inherited-before)
  (define missing-inherited-slot (gensym 'missing-inherited-slot))
  (for ([(name b) (in-hash projected-table)])
    (define value (unbox b))
    (cond
      [(set-member? own-slot-names name)
       (send receiver declare-slot! name value)]
      [else
       (define prior-box (hash-ref inherited-before name missing-inherited-slot))
         (unless (or (eq? prior-box missing-inherited-slot)
                     (equal? value (unbox prior-box)))
           (send receiver assign-slot! name value))])))

(define (invoke-slot-callable obj slot-fn arg-values ctx)
  (define-values (projected-table own-slot-names inherited-before)
    (project-receiver-slot-frame obj))
  (define receiver-slot-env (env-with-table projected-table (runtime-globals ctx)))
  (define receiver-call-root (extend-env receiver-slot-env))
  (env-define! receiver-call-root "ME" obj)
  (dynamic-wind
    void
    (lambda () (slot-fn receiver-call-root arg-values ctx))
    (lambda ()
      (sync-receiver-slot-frame!
       obj
       projected-table
       own-slot-names
       inherited-before))))

(define (read-slot-value obj slot-name ctx)
  (define missing-slot-value (gensym 'missing-slot-value))
  (define maybe-value (send obj lookup-slot slot-name missing-slot-value))
  (if (eq? maybe-value missing-slot-value)
      (send obj resolve-missing-slot!
            slot-name
            (lambda ()
              (define maybe-hook (send obj lookup-special-procedure-slot "omgwtf"))
              (if (procedure? maybe-hook)
                  (invoke-slot-callable
                   obj
                   maybe-hook
                   '()
                   ctx)
                  (error 'run-program "unknown slot: ~a" slot-name))))
      maybe-value))

(define (make-prototype-object parent-obj mixin-objs)
  (define child (send parent-obj prototype))
  (apply-mixins! child mixin-objs)
  ;; Mixins may overwrite parent; restore inheritance parent per spec.
  (send child declare-slot! "parent" parent-obj)
  child)

(define (construct-prototype parent-obj mixin-objs e ctx)
  (define child (make-prototype-object parent-obj mixin-objs))
  (run-izmakin-hook! child e ctx)
  child)

(define (compile-expr-srs inner)
  (define inner-proc (compile-expr inner))
  (lambda (e ctx)
    (define resolved-name
      (identifier-text "SRS expression must evaluate to identifier text" (inner-proc e ctx)))
    (env-ref e resolved-name)))

(define (compile-expr-clone inner)
  (define inner-proc (compile-expr inner))
  (lambda (e ctx)
    (construct-prototype
     (resolve-bukkit "LIEK initializer" (inner-proc e ctx))
     '()
     e
     ctx)))

(define (compile-expr-prototype parent-spec mixins)
  (define parent-name-proc
    (compile-name-resolver "prototype parent name must evaluate to identifier text" parent-spec))
  (define mixin-name-procs
    (map (lambda (m)
           (compile-name-resolver "mixin name must evaluate to identifier text" m))
         mixins))
  (lambda (e ctx)
    (define parent-name (parent-name-proc e ctx))
    (define parent-obj (resolve-bukkit "prototype parent" (env-ref e parent-name)))
    (define mixin-objs
      (for/list ([mix-proc (in-list mixin-name-procs)])
        (define mix-name (mix-proc e ctx))
        (resolve-bukkit "mixin" (env-ref e mix-name))))
    (construct-prototype parent-obj mixin-objs e ctx)))

(define (compile-expr-binary op left right whole-expr)
  (define left-proc (compile-expr left))
  (define right-proc (compile-expr right))
  (define op-fn
    (or (hash-ref binary-operator-table op #f)
        (raise-unsupported-op 'binary op whole-expr)))
  (lambda (e ctx)
    (op-fn (left-proc e ctx) (right-proc e ctx))))

(define (compile-expr-unary op arg whole-expr)
  (define arg-proc (compile-expr arg))
  (define op-fn
    (or (hash-ref unary-operator-table op #f)
        (raise-unsupported-op 'unary op whole-expr)))
  (lambda (e ctx)
    (op-fn (arg-proc e ctx))))

(define (compile-expr-variadic op args whole-expr)
  (define arg-procs (map compile-expr args))
  ((or (hash-ref variadic-operator-compiler-table op #f)
       (raise-unsupported-op 'variadic op whole-expr))
   arg-procs))

(define (compile-expr-call name args)
  (define name-proc
    (compile-name-resolver "function name must evaluate to identifier text" name))
  (define arg-procs (map compile-expr args))
  (lambda (e ctx)
    (define fn-name (name-proc e ctx))
    (define fn (resolve-callable e ctx fn-name "function"))
    ;; Strict 1.3 function calls use global namespace, not caller-local scope.
    (fn (runtime-globals ctx)
        (map (lambda (a) (a e ctx)) arg-procs)
        ctx)))

(define (compile-expr-method-call receiver name-spec args)
  (define recv-proc
    (and (not (expr-ident? receiver))
         (compile-expr receiver)))
  (define receiver-ident
    (and (expr-ident? receiver)
         (expr-ident-name receiver)))
  (define name-proc
    (compile-name-resolver "method name must evaluate to identifier text" name-spec))
  (define arg-procs (map compile-expr args))
  (lambda (e ctx)
    (define method-name (name-proc e ctx))
    (define arg-values (map (lambda (a) (a e ctx)) arg-procs))
    (define (invoke-on-object obj)
        ;; Method calls share slot-access resolution semantics:
        ;; full parent-chain search first, then one omgwtf miss hook on the
        ;; original receiver if and only if the overall lookup fails.
      (define maybe-slot-callable (read-slot-value obj method-name ctx))
      (if (procedure? maybe-slot-callable)
          (invoke-slot-callable obj maybe-slot-callable arg-values ctx)
          (error 'run-program
                 "method slot is not callable: ~a"
                 method-name)))
    (cond
      [receiver-ident
       (define maybe-box (env-lookup-box e receiver-ident))
       (unless maybe-box
         (error 'run-program "unknown identifier: ~a" receiver-ident))
       (define recv-val (unbox maybe-box))
       (unless (lol-object? recv-val)
         (error 'run-program "method call requires BUKKIT receiver, got ~e" recv-val))
       (invoke-on-object recv-val)]
      [else
       (define obj (recv-proc e ctx))
       (unless (lol-object? obj)
         (error 'run-program "method call requires BUKKIT receiver, got ~e" obj))
       (invoke-on-object obj)])))

(define (compile-expr-cast inner type-name)
  (define inner-proc (compile-expr inner))
  (lambda (e ctx)
    (cast-value 'MAEK (inner-proc e ctx) type-name)))

(define (compile-expr-slot object slot)
  (match-define (lvalue lread _) (compile-lvalue (expr-slot object slot)))
  (lambda (e ctx) (lread e ctx)))

(define (compile-expr expr)
  (match expr
    [(expr-number text)
     (lambda (_e _ctx)
       (or (string->number text)
           (error 'run-program "invalid number literal: ~a" text)))]

    [(expr-string text)
     (lambda (e _ctx) (expand-format-placeholders e text))]

    [(expr-literal value)
     (lambda (_e _ctx)
       (if (eq? value 'NOOB) noob value))]

    [(expr-type-default type-name)
     (define-values (known? default-value)
       (type-default-value type-name))
     (unless known?
       (error 'run-program "unknown type name in ITZ A: ~a" type-name))
     (if (string=? type-name "BUKKIT")
         (lambda (_e _ctx) (new lol-object%))
         (lambda (_e _ctx) default-value))]

    [(expr-ident name)
     (lambda (e _ctx) (env-ref e name))]

    [(expr-srs inner)
     (compile-expr-srs inner)]

    [(expr-clone inner)
     (compile-expr-clone inner)]

    [(expr-prototype parent-spec mixins)
     (compile-expr-prototype parent-spec mixins)]

    [(and whole-expr (expr-binary op left right))
     (compile-expr-binary op left right whole-expr)]

    [(and whole-expr (expr-unary op arg))
     (compile-expr-unary op arg whole-expr)]

    [(and whole-expr (expr-variadic op args))
     (compile-expr-variadic op args whole-expr)]

    [(expr-call name args)
     (compile-expr-call name args)]

    [(expr-method-call receiver name-spec args)
     (compile-expr-method-call receiver name-spec args)]

    [(expr-cast inner type-name)
     (compile-expr-cast inner type-name)]

    [(expr-slot object slot)
     (compile-expr-slot object slot)]

    [_ (raise-unsupported expr)]))

(define (compile-block statements)
  (define stmt-procs (map compile-stmt statements))
  (lambda (e ctx)
    (for ([stmt-proc (in-list stmt-procs)])
      (stmt-proc e ctx))))

(define (compile-stmt-declare target init)
  (define name-proc (compile-target-name target))
  (define init-proc (compile-declare-init init))
  (lambda (e ctx)
    (define value (init-proc e ctx))
    (define name (ensure-bindable-name "declaration" (name-proc e ctx)))
    (if (exec-ctx-def-object ctx)
        ;; Object body declarations are slot declarations; special slots such as
        ;; omgwtf/izmakin/parent already exist and must remain assignable via
        ;; `I HAS A ...` within O HAI IM blocks.
        (cond
          [(hash-ref (env-table e) name #f)
           => (lambda (b) (set-box! b value))]
          [else (env-define! e name value)])
        (env-define! e name value))))

(define (compile-stmt-assign target expr)
  (match-define (lvalue lread lwrite) (compile-lvalue target))
  (define expr-proc (compile-expr expr))
  (lambda (e ctx)
    (lwrite e (expr-proc e ctx) ctx)))

(define (compile-stmt-cast target type-name)
  (match-define (lvalue lread lwrite)
    (compile-lvalue target))
  (lambda (e ctx)
    (define value (cast-value 'IS-NOW-A (lread e ctx) type-name))
    (lwrite e value ctx)
    (set-it! e value)))

(define (compile-stmt-input target)
  (match-define (lvalue lread lwrite)
    (compile-lvalue target #:define-missing? #t))
  (lambda (e ctx)
    (define line (read-line (current-input-port) 'any))
    (define value (if (eof-object? line) noob line))
    (lwrite e value ctx)
    (set-it! e value)))

(define (compile-stmt-slot-set object slot expr)
  (define object-proc (compile-expr object))
  (define slot-name-proc (compile-slot-name slot))
  (define expr-proc (compile-declare-init expr))
  (lambda (e ctx)
    (define obj (resolve-bukkit-from-proc "slot assignment" object-proc e ctx))
    (define value (expr-proc e ctx))
    (send obj declare-slot! (slot-name-proc e ctx) value)
    (set-it! e value)))

(define (compile-stmt-visible exprs suppress-newline?)
  (define expr-procs (map compile-expr exprs))
  (lambda (e ctx)
    (define values (map (lambda (ep) (ep e ctx)) expr-procs))
    (for ([v (in-list values)])
      (display (lol-string v) (runtime-stdout ctx)))
    (unless suppress-newline?
      (newline (runtime-stdout ctx)))
    (when (pair? values)
      (set-it! e (last values)))))

(define (compile-stmt-if condition then-branch mebbe-branches else-branch)
  (define cond-proc (compile-expr condition))
  (define then-proc (compile-block then-branch))
  (define mebbe-procs
    (for/list ([mb (in-list mebbe-branches)])
      (match-define (mebbe-branch mebbe-condition mebbe-body) mb)
      (cons (compile-expr mebbe-condition)
            (compile-block mebbe-body))))
  (define else-proc (compile-block else-branch))
  (lambda (e ctx)
    (cond
      [(lol-truthy? (cond-proc e ctx))
       (then-proc (extend-env e) ctx)]
      [(for/or ([mb (in-list mebbe-procs)])
         (match-define (cons mb-cond mb-body) mb)
         (and (lol-truthy? (mb-cond e ctx))
              mb-body))
       => (lambda (mb-body)
            (mb-body (extend-env e) ctx))]
      [else (else-proc (extend-env e) ctx)])))

(define (compile-stmt-switch subject cases default)
  (define subject-proc (compile-expr subject))
  (define case-procs
    (for/list ([c (in-list cases)])
      (match-define (switch-case case-match case-body) c)
      (cons (compile-expr case-match)
            (compile-block case-body))))
  (define default-proc (compile-block default))
  (lambda (e ctx)
    (let/ec break-k
      (define subject-value (subject-proc e ctx))
      (define switch-ctx (ctx-derive ctx #:break-k break-k))
      (define-values (_before matching-and-after)
        (splitf-at case-procs
                   (match-lambda
                     [(cons case-match-proc _case-body-proc)
                      (not (lol-equal? subject-value (case-match-proc e ctx)))])))
      (if (null? matching-and-after)
          (default-proc (extend-env e) switch-ctx)
          (for ([compiled-case (in-list matching-and-after)])
            (match-define (cons _case-match-proc case-body-proc)
              compiled-case)
            (case-body-proc (extend-env e) switch-ctx))))))

(define (compile-stmt-loop label-open label-close update-var-spec
                           update-op cond-kind cond-expr body)
  (define open-label-proc
    (compile-name-resolver "loop label must evaluate to identifier text" label-open))
  (define close-label-proc
    (compile-name-resolver "loop label must evaluate to identifier text" label-close))
  (define update-var-proc
    (and update-var-spec
         (compile-name-resolver
          "loop variable name must evaluate to identifier text"
          update-var-spec)))
  (define update-op-proc (compile-loop-update-op update-op))
  (define cond-proc (and cond-expr (compile-expr cond-expr)))
  (define body-proc (compile-block body))
  (lambda (e ctx)
    (run-compiled-loop-stmt! e ctx
                             open-label-proc close-label-proc
                             update-var-proc update-op-proc
                             cond-kind cond-proc body-proc)))

(define (make-callable-fn kind fn-name param-names body-proc)
  (define expected-arity (length param-names))
  (lambda (caller-env arg-values caller-ctx)
    (define actual-arity (length arg-values))
    (unless (= expected-arity actual-arity)
      (error 'run-program
             "~a ~a expected ~a args, got ~a"
             kind
             fn-name
             expected-arity
             actual-arity))
    (define call-root (or caller-env (runtime-globals caller-ctx)))
    (define call-env (extend-env call-root))
    (for ([param (in-list param-names)]
          [arg (in-list arg-values)])
      (env-define! call-env param arg))
    ;; Each function/method activation gets its own IT cell.
    ;; Method calls still resolve non-IT names through receiver projection via caller-env.
    (env-define! call-env "IT" noob)
    (let/ec return-k
      (define fn-ctx
        (ctx-derive caller-ctx
                    #:return-k return-k
                    #:break-k #f
                    #:object-name #f
                    #:def-object #f))
      (body-proc call-env fn-ctx)
      (env-ref call-env "IT"))))

(define (compile-stmt-function-def name params body)
  (define body-proc (compile-block body))
  (define name-proc
    (compile-name-resolver "function name must evaluate to identifier text" name))
  (define param-name-procs
    (map (lambda (param)
           (compile-name-resolver
            "parameter name must evaluate to identifier text"
            param))
         params))
  (lambda (e ctx)
    (define resolved-name (ensure-bindable-name "function name" (name-proc e ctx)))
    (define resolved-params
      (map (lambda (param-name-proc)
             (ensure-bindable-name "parameter name" (param-name-proc e ctx)))
           param-name-procs))
    (define callable-fn
      (make-callable-fn
       (if (exec-ctx-def-object ctx) "method" "function")
       resolved-name
       resolved-params
       body-proc))
    (cond
      [(exec-ctx-def-object ctx)
       (send (exec-ctx-def-object ctx)
             declare-slot!
             resolved-name
             callable-fn)]
      [else (env-define! e resolved-name callable-fn)])))

(define (compile-stmt-method-def receiver name params body)
  (define receiver-proc (compile-expr receiver))
  (define body-proc (compile-block body))
  (define name-proc
    (compile-name-resolver "method name must evaluate to identifier text" name))
  (define param-name-procs
    (map (lambda (param)
           (compile-name-resolver
            "parameter name must evaluate to identifier text"
            param))
         params))
  (lambda (e ctx)
    (define resolved-name (ensure-bindable-name "method name" (name-proc e ctx)))
    (define resolved-params
      (map (lambda (param-name-proc)
             (ensure-bindable-name "parameter name" (param-name-proc e ctx)))
           param-name-procs))
    (define target (receiver-proc e ctx))
    (unless (lol-object? target)
      (error 'run-program
             "method declaration requires BUKKIT receiver, got ~e"
             target))
    (define method-fn
      (make-callable-fn
       "method"
       resolved-name
       resolved-params
       body-proc))
    (send target declare-slot! resolved-name method-fn)))

(define (compile-stmt-object-def name-spec parent-spec mixins body)
  (define name-proc
    (compile-name-resolver "object name must evaluate to identifier text" name-spec))
  (define parent-proc
    (and parent-spec
         (compile-name-resolver
          "object parent name must evaluate to identifier text"
          parent-spec)))
  (define mixin-name-procs
    (map (lambda (m)
           (compile-name-resolver
            "mixin name must evaluate to identifier text"
            m))
         mixins))
  (define body-proc (compile-block body))
  (lambda (e ctx)
    (define resolved-name
      (ensure-bindable-name "object name" (name-proc e ctx)))
    (define obj
      (if parent-proc
          (let* ([resolved-parent-name (parent-proc e ctx)]
                 [resolved-parent
                  (resolve-bukkit "object parent" (env-ref e resolved-parent-name))]
                 [resolved-mixins
                  (for/list ([mixin-name-proc (in-list mixin-name-procs)])
                    (resolve-bukkit "mixin" (env-ref e (mixin-name-proc e ctx))))])
            (make-prototype-object resolved-parent resolved-mixins))
          (new lol-object%)))
    (define object-ctx
      (ctx-derive ctx
                  #:object-name resolved-name
                  #:def-object obj))
    (body-proc (env-with-table (send obj slot-table) e)
               object-ctx)
    (run-izmakin-hook! obj e object-ctx)
    (env-set-or-define! e resolved-name obj)
    (set-it! e obj)))

(define (compile-stmt-return expr)
  (define expr-proc (compile-expr expr))
  (lambda (e ctx)
    (define value (expr-proc e ctx))
    (set-it! e value)
    (ctx-return! ctx value)))

(define (compile-stmt-break)
  (lambda (_e ctx)
    (ctx-break! ctx)))

(define (compile-stmt-expr expr)
  (define expr-proc (compile-expr expr))
  (lambda (e ctx)
    (define value (expr-proc e ctx))
    (set-it! e value)))

(define (compile-stmt stmt)
  (match stmt
    [(stmt-declare target init)
     (compile-stmt-declare target init)]
    [(stmt-assign target expr)
     (compile-stmt-assign target expr)]
    [(stmt-cast target type-name)
     (compile-stmt-cast target type-name)]
    [(stmt-input target)
     (compile-stmt-input target)]
    [(stmt-slot-set object slot expr)
     (compile-stmt-slot-set object slot expr)]
    [(stmt-visible exprs suppress-newline?)
     (compile-stmt-visible exprs suppress-newline?)]
    [(stmt-if condition then-branch mebbe-branches else-branch)
     (compile-stmt-if condition then-branch mebbe-branches else-branch)]
    [(stmt-switch subject cases default)
     (compile-stmt-switch subject cases default)]
    [(stmt-loop label-open label-close update-var update-op cond-kind cond-expr body)
     (compile-stmt-loop label-open label-close update-var update-op cond-kind cond-expr body)]
    [(stmt-function-def name params body)
     (compile-stmt-function-def name params body)]
    [(stmt-method-def receiver name params body)
     (compile-stmt-method-def receiver name params body)]
    [(stmt-object-def name parent mixins body)
     (compile-stmt-object-def name parent mixins body)]
    [(stmt-return expr)
     (compile-stmt-return expr)]
    [(stmt-break)
     (compile-stmt-break)]
    [(stmt-expr expr)
     (compile-stmt-expr expr)]
    [_ (raise-unsupported stmt)]))

(define (compile-program parsed [phase 'unknown])
  (define program-proc
    (match parsed
      [(program _ statements)
       (with-handlers ([exn:fail?
                        (lambda (e)
                          (lambda (_e _ctx)
                            (raise e)))])
         (compile-block statements))]
      [_ (raise-argument-error 'compile-program "program?" parsed)]))
  (lambda ()
    (define globals (make-root-env))
    (define stdout (open-output-string))
    (define st (runstate globals stdout phase))
    (define root-ctx (exec-ctx st #f #f #f #f))
    (with-handlers ([exn:fail:unsupported?
                     (lambda (e)
                       (hash 'status 'unsupported
                             'phase (runstate-phase st)
                             'stdout (get-output-string stdout)
                             'last-value (env-ref globals "IT")
                             'reason (exn-message e)
                             'where (exn:fail:unsupported-where e)))]
                    [exn:fail?
                     (lambda (e)
                       (hash 'status 'runtime-error
                             'phase (runstate-phase st)
                             'stdout (get-output-string stdout)
                             'last-value (env-ref globals "IT")
                             'error (exn-message e)))])
      (program-proc globals root-ctx)
      (hash 'status 'ok
            'phase (runstate-phase st)
            'stdout (get-output-string stdout)
            'last-value (env-ref globals "IT")))))

(define (execute-program parsed phase)
  ((compile-program parsed phase)))
