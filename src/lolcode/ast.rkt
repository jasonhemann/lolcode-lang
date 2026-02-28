#lang racket/base

(provide program
         program?
         program-version
         program-statements

         stmt-declare
         stmt-declare?
         stmt-declare-target
         stmt-declare-init

         stmt-assign
         stmt-assign?
         stmt-assign-target
         stmt-assign-expr

         stmt-cast
         stmt-cast?
         stmt-cast-target
         stmt-cast-type-name

         stmt-input
         stmt-input?
         stmt-input-target

         stmt-visible
         stmt-visible?
         stmt-visible-exprs
         stmt-visible-suppress-newline?

         stmt-loop
         stmt-loop?
         stmt-loop-label
         stmt-loop-update-var
         stmt-loop-update-op
         stmt-loop-cond-kind
         stmt-loop-cond-expr
         stmt-loop-body

         stmt-if
         stmt-if?
         stmt-if-condition
         stmt-if-then-branch
         stmt-if-mebbe-branches
         stmt-if-else-branch

         stmt-switch
         stmt-switch?
         stmt-switch-subject
         stmt-switch-cases
         stmt-switch-default

         switch-case
         switch-case?
         switch-case-match
         switch-case-body

         mebbe-branch
         mebbe-branch?
         mebbe-branch-condition
         mebbe-branch-body

         stmt-function-def
         stmt-function-def?
         stmt-function-def-name
         stmt-function-def-args
         stmt-function-def-body

         stmt-return
         stmt-return?
         stmt-return-expr

         stmt-break
         stmt-break?

         stmt-object-def
         stmt-object-def?
         stmt-object-def-name
         stmt-object-def-parent
         stmt-object-def-body

         stmt-slot-set
         stmt-slot-set?
         stmt-slot-set-object
         stmt-slot-set-slot
         stmt-slot-set-expr

         stmt-expr
         stmt-expr?
         stmt-expr-expr

         expr-ident
         expr-ident?
         expr-ident-name

         expr-number
         expr-number?
         expr-number-text

         expr-string
         expr-string?
         expr-string-text

         expr-literal
         expr-literal?
         expr-literal-value

         expr-binary
         expr-binary?
         expr-binary-op
         expr-binary-left
         expr-binary-right

         expr-unary
         expr-unary?
         expr-unary-op
         expr-unary-arg

         expr-variadic
         expr-variadic?
         expr-variadic-op
         expr-variadic-args

         expr-call
         expr-call?
         expr-call-name
         expr-call-args

         expr-method-call
         expr-method-call?
         expr-method-call-receiver
         expr-method-call-name
         expr-method-call-args

         expr-slot
         expr-slot?
         expr-slot-object
         expr-slot-slot

         expr-srs
         expr-srs?
         expr-srs-expr

         expr-cast
         expr-cast?
         expr-cast-expr
         expr-cast-type-name)

(struct program (version statements) #:transparent)

(struct stmt-declare (target init) #:transparent)
(struct stmt-assign (target expr) #:transparent)
(struct stmt-cast (target type-name) #:transparent)
(struct stmt-input (target) #:transparent)
(struct stmt-visible (exprs suppress-newline?) #:transparent)
(struct stmt-loop (label update-var update-op cond-kind cond-expr body) #:transparent)
(struct stmt-if (condition then-branch mebbe-branches else-branch) #:transparent)
(struct stmt-switch (subject cases default) #:transparent)
(struct switch-case (match body) #:transparent)
(struct mebbe-branch (condition body) #:transparent)
(struct stmt-function-def (name args body) #:transparent)
(struct stmt-return (expr) #:transparent)
(struct stmt-break () #:transparent)
(struct stmt-object-def (name parent body) #:transparent)
(struct stmt-slot-set (object slot expr) #:transparent)
(struct stmt-expr (expr) #:transparent)

(struct expr-ident (name) #:transparent)
(struct expr-number (text) #:transparent)
(struct expr-string (text) #:transparent)
(struct expr-literal (value) #:transparent)
(struct expr-binary (op left right) #:transparent)
(struct expr-unary (op arg) #:transparent)
(struct expr-variadic (op args) #:transparent)
(struct expr-call (name args) #:transparent)
(struct expr-method-call (receiver name args) #:transparent)
(struct expr-slot (object slot) #:transparent)
(struct expr-srs (expr) #:transparent)
(struct expr-cast (expr type-name) #:transparent)
