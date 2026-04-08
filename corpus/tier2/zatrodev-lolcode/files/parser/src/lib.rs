pub mod ast;

pub extern crate lexer;

use crate::ast::{
    Assignment, BinaryExpression, BlockStatement, Declaration, Expression, FunctionCall,
    FunctionDeclaration, IDENTIFIER, If, Input, Literal, LolType, LoopCondition, LoopStatement,
    MultiExpression, NUMBAR, NUMBR, PrefixExpression, Print, Program, RecastStatement,
    ReturnStatement, Statement, Switch, TROOF, TypecastExpression, UnaryExpression, YARN,
};
use lexer::Lexer;
use lexer::token::{Span, Token, TokenKind};

type ParseError = String;
type ParseErrors = Vec<ParseError>;

pub struct Parser<'a> {
    lexer: Lexer<'a>,
    current_token: Token,
    peek_token: Token,
    errors: ParseErrors,
}


impl<'a> Parser<'a> {
    pub fn new(mut lexer: Lexer<'a>) -> Parser<'a> {
        let cur = lexer.next_token();
        let next = lexer.next_token();
        let errors = Vec::new();

        Parser {
            lexer,
            current_token: cur,
            peek_token: next,
            errors,
        }
    }

    fn next_token(&mut self) {
        self.current_token = self.peek_token.clone();
        self.peek_token = self.lexer.next_token();
    }

    fn current_token_is(&self, token: &TokenKind) -> bool {
        self.current_token.kind == *token
    }

    fn peek_token_is(&self, token: &TokenKind) -> bool {
        self.peek_token.kind == *token
    }

    fn expect_peek(&mut self, token: &TokenKind) -> Result<(), ParseError> {
        self.next_token();
        if self.current_token.kind == *token {
            Ok(())
        } else {
            let e = format!("expected token: {} got: {}", token, self.current_token);
            Err(e)
        }
    }

    pub fn parse_program(&mut self) -> Result<Program, ParseErrors> {
        let mut program = Program::new();

        if !self.current_token_is(&TokenKind::HAI) {
            let err = format!(
                "Program must start with 'HAI', but found '{}' instead.",
                self.current_token
            );
            return Err(vec![err]);
        }
        self.next_token();

        if self.current_token_is(&TokenKind::WAZZUP) {
            self.next_token();

            while !self.current_token_is(&TokenKind::BUHBYE)
                && !self.current_token_is(&TokenKind::EOF)
            {
                if self.current_token_is(&TokenKind::IHasA) {
                    match self.parse_declaration_statement() {
                        Ok(stmt) => program.body.push(stmt),
                        Err(e) => self.errors.push(e),
                    }
                } else {
                    self.errors.push(format!(
                        "Only variable declarations (I HAS A) are allowed in the WAZZUP block, found {}",
                        self.current_token
                    ));
                }
                self.next_token();
            }

            if !self.current_token_is(&TokenKind::BUHBYE) {
                self.errors
                    .push("Expected 'BUHBYE' to end the declaration block.".to_string());
            }
            self.next_token();
        }

        while !self.current_token_is(&TokenKind::KTHXBYE) && !self.current_token_is(&TokenKind::EOF)
        {
            match self.parse_statement() {
                Ok(stmt) => program.body.push(stmt),
                Err(e) => self.errors.push(e),
            }
            self.next_token();
        }

        if !self.current_token_is(&TokenKind::KTHXBYE) {
            self.errors.push(
                "Expected 'KTHXBYE' to end the program, but the file ended instead.".to_string(),
            );
        }

        program.span.end = self.current_token.span.end;

        if self.errors.is_empty() {
            Ok(program)
        } else {
            Err(self.errors.clone())
        }
    }

    fn parse_statement(&mut self) -> Result<Statement, ParseError> {
        match self.current_token.kind {
            TokenKind::IHasA => 
                Err(
                "Variable declaration with 'I HAS A' is only allowed inside a 'WAZZUP' ... 'BUHBYE' block at the top of the program.".to_string()
            ),
            TokenKind::VISIBLE => self.parse_print_statement(),
            TokenKind::GIMMEH => self.parse_input_statement(),
            TokenKind::ImInYr => self.parse_loop_statement(),
            TokenKind::FoundYr => self.parse_return_statement(),
            TokenKind::HowIzI => self.parse_function_statement(),
            TokenKind::GTFO => Ok(Statement::Break(self.current_token.span.clone())),
            _ => {
                if let TokenKind::IDENTIFIER { .. } = self.current_token.kind {
                    if self.peek_token_is(&TokenKind::R) {
                        return self.parse_assignment_statement();
                    }
                    if self.peek_token_is(&TokenKind::IsNowA) {
                        return self.parse_recast_statement();
                    }
                }

                let expr = self.parse_expression()?.0;

                match self.peek_token.kind {
                    TokenKind::ORly => {
                        self.next_token();
                        self.parse_if_statement(expr)
                    }
                    TokenKind::WTF => {
                        self.next_token();
                        self.parse_switch_statement(expr)
                    }
                    _ => Ok(Statement::Expression(expr)),
                }
            }
        }
    }

    fn parse_recast_statement(&mut self) -> Result<Statement, ParseError> {
        let start = self.current_token.span.start;

        let name = self.current_token.clone();

        if !matches!(&self.current_token.kind, TokenKind::IDENTIFIER { .. }) {
            return Err(format!("{} not an identifier", self.current_token));
        }

        self.expect_peek(&TokenKind::IsNowA)?;
        self.next_token();

        let new_type = self.parse_type()?;

        let end = self.current_token.span.end;

        Ok(Statement::Recast(RecastStatement {
            identifier: name,
            new_type,
            span: Span { start, end },
        }))
    }

    fn parse_type(&mut self) -> Result<LolType, ParseError> {
        match self.current_token.kind {
            TokenKind::TYPENUMBR => Ok(LolType::NUMBR),
            TokenKind::TYPENUMBAR => Ok(LolType::NUMBAR),
            TokenKind::TYPEYARN => Ok(LolType::YARN),
            TokenKind::TYPETROOF => Ok(LolType::TROOF),
            TokenKind::NOOB => Err("Cannot explicitly cast a value TO the type NOOB.".to_string()),
            _ => Err(format!(
                "Expected a type name (like NUMBR or YARN), but found {} instead.",
                self.current_token
            )),
        }
    }

    fn parse_function_statement(&mut self) -> Result<Statement, ParseError> {
        let start = self.current_token.span.start;
        self.next_token();

        let identifier_name = match &self.current_token.kind {
            TokenKind::IDENTIFIER { name } => name.to_string(),
            _ => return Err(format!("{} not an identifier", self.current_token)),
        };

        let mut params = vec![];
        if self.peek_token_is(&TokenKind::Yr) {
            self.next_token();
            self.next_token();

            match &self.current_token.kind {
                TokenKind::IDENTIFIER { name } => params.push(IDENTIFIER {
                    name: name.clone(),
                    span: self.current_token.span.clone(),
                }),
                token => {
                    return Err(format!(
                        "expected function params to be an identifier, got {}",
                        token
                    ));
                }
            }

            while self.peek_token_is(&TokenKind::AN) {
                self.next_token();
                self.expect_peek(&TokenKind::Yr)?;
                self.next_token();

                match &self.current_token.kind {
                    TokenKind::IDENTIFIER { name } => params.push(IDENTIFIER {
                        name: name.clone(),
                        span: self.current_token.span.clone(),
                    }),
                    token => {
                        return Err(format!(
                            "expected function params to be an identifier, got {}",
                            token
                        ));
                    }
                }
            }
        }
        self.next_token();

        let function_body = self.parse_block_statement(&[&TokenKind::IfUSaySo])?;

        self.expect_peek(&TokenKind::IfUSaySo)?;

        let end = self.current_token.span.end;

        Ok(Statement::FunctionDeclaration(Box::new(
            FunctionDeclaration {
                params,
                body: function_body,
                span: Span { start, end },
                name: identifier_name,
            },
        )))
    }

    fn parse_return_statement(&mut self) -> Result<Statement, ParseError> {
        let start = self.current_token.span.start;
        self.next_token();

        let value = self.parse_expression()?.0;

        let end = self.current_token.span.end;

        Ok(Statement::Return(ReturnStatement {
            argument: value,
            span: Span { start, end },
        }))
    }

    fn parse_loop_statement(&mut self) -> Result<Statement, ParseError> {
        let start = self.current_token.span.start;
        self.next_token();

        let label = self.current_token.clone();
        let identifier_name = match &self.current_token.kind {
            TokenKind::IDENTIFIER { name } => name.to_string(),
            _ => return Err(format!("{} not an identifier", self.current_token)),
        };

        let operation =
            if self.peek_token_is(&TokenKind::UPPIN) || self.peek_token_is(&TokenKind::NERFIN) {
                self.next_token();
                self.current_token.clone()
            } else {
                return Err("Operation must be specified. Either UPPIN or NERFIN.".to_string());
            };

        self.expect_peek(&TokenKind::Yr)?;
        self.next_token();

        let variable = self.current_token.clone();

        if !matches!(&self.current_token.kind, TokenKind::IDENTIFIER { .. }) {
            return Err(format!("{} not an identifier", self.current_token));
        }

        let mut condition: Option<LoopCondition> = None;
        if self.peek_token_is(&TokenKind::TIL) || self.peek_token_is(&TokenKind::WILE) {
            self.next_token();

            let loop_condition = self.current_token.clone();
            self.next_token();

            let expr = self.parse_expression()?.0;

            condition = Some(LoopCondition {
                condition: loop_condition,
                expr,
            });
        }
        self.next_token();

        let body = self.parse_block_statement(&[&TokenKind::ImOuttaYr])?;

        self.expect_peek(&TokenKind::ImOuttaYr)?;
        self.expect_peek(&TokenKind::IDENTIFIER {
            name: identifier_name,
        })?;

        let end = self.current_token.span.end;

        Ok(Statement::Loop(Box::new(LoopStatement {
            label,
            operation,
            condition,
            variable,
            body,
            span: Span { start, end },
        })))
    }

    fn parse_if_statement(&mut self, expr: Expression) -> Result<Statement, ParseError> {
        let start = self.current_token.span.start;

        let condition = expr;

        self.expect_peek(&TokenKind::YaRly)?;
        self.next_token();
        let consequent =
            self.parse_block_statement(&[&TokenKind::Mebbe, &TokenKind::NoWai, &TokenKind::OIC])?;

        let mut elif_branches = Vec::new();
        while self.peek_token_is(&TokenKind::Mebbe) {
            self.next_token();
            self.next_token();
            let (elif_condition, _) = self.parse_expression()?;
            self.next_token();
            let elif_block = self.parse_block_statement(&[
                &TokenKind::Mebbe,
                &TokenKind::NoWai,
                &TokenKind::OIC,
            ])?;
            elif_branches.push((elif_condition, elif_block));
        }

        let alternate = if self.peek_token_is(&TokenKind::NoWai) {
            self.next_token();
            self.next_token();
            Some(self.parse_block_statement(&[&TokenKind::OIC])?)
        } else {
            None
        };

        self.expect_peek(&TokenKind::OIC)?;

        let end = self.current_token.span.end;

        Ok(Statement::If(Box::new(If {
            condition: Box::new(condition),
            consequent,
            elif_branches,
            alternate,
            span: Span { start, end },
        })))
    }

    fn parse_switch_statement(&mut self, expr: Expression) -> Result<Statement, ParseError> {
        let start = self.current_token.span.start;

        let condition = expr;

        let mut cases = Vec::new();
        while self.peek_token_is(&TokenKind::OMG) {
            self.next_token();
            self.next_token();
            let (case_condition, _) = self.parse_expression()?;
            self.next_token();
            let case_block = self.parse_block_statement(&[&TokenKind::OMG, &TokenKind::OMGWTF])?;
            cases.push((case_condition, case_block));
        }

        if cases.is_empty() {
            return Err("Must have at least one case block".to_string());
        }

        let default = if self.peek_token_is(&TokenKind::OMGWTF) {
            self.next_token();
            self.next_token();
            Some(self.parse_block_statement(&[&TokenKind::OIC])?)
        } else {
            None
        };

        self.expect_peek(&TokenKind::OIC)?;

        let end = self.current_token.span.end;

        Ok(Statement::Switch(Box::new(Switch {
            condition,
            cases,
            default,
            span: Span { start, end },
        })))
    }

    fn parse_print_statement(&mut self) -> Result<Statement, ParseError> {
        let start = self.current_token.span.start;
        self.next_token();

        let mut expressions = Vec::new();

        expressions.push(self.parse_expression()?.0);

      while self.peek_token_is(&TokenKind::PLUS) || self.peek_token_is(&TokenKind::AN) {
        self.next_token(); // consume PLUS or AN
        self.next_token(); // move to next expression
        expressions.push(self.parse_expression()?.0);
    }

        let end = self.current_token.span.end;

        Ok(Statement::Print(Print {
            exprs: expressions,
            span: Span { start, end },
        }))
    }

    fn parse_block_statement(
        &mut self,
        end_tokens: &[&TokenKind],
    ) -> Result<BlockStatement, ParseError> {
        let start = self.current_token.span.start;
        let mut block_statement = Vec::new();

        while !self.current_token_is(&TokenKind::EOF) {
            if end_tokens.iter().any(|tk| self.current_token_is(tk)) {
                break;
            }

            match self.parse_statement() {
                Ok(statement) => block_statement.push(statement),
                Err(e) => self.errors.push(e),
            }

            if end_tokens.iter().any(|tk| self.peek_token_is(tk)) {
                break;
            }

            self.next_token();
        }

        let end = self.current_token.span.end;

        Ok(BlockStatement {
            body: block_statement,
            span: Span { start, end },
        })
    }
    fn parse_input_statement(&mut self) -> Result<Statement, ParseError> {
        let start = self.current_token.span.start;
        self.next_token();

        let name = self.current_token.clone();

        if !matches!(&self.current_token.kind, TokenKind::IDENTIFIER { .. }) {
            return Err(format!("{} not an identifier", self.current_token));
        }

        let end = self.current_token.span.end;

        Ok(Statement::Input(Input {
            identifier: name,
            span: Span { start, end },
        }))
    }

    fn parse_declaration_statement(&mut self) -> Result<Statement, ParseError> {
        let start = self.current_token.span.start;
        self.next_token();

        let name = self.current_token.clone();

        if !matches!(&self.current_token.kind, TokenKind::IDENTIFIER { .. }) {
            return Err(format!("{} not an identifier", self.current_token));
        }

        if !self.peek_token_is(&TokenKind::ITZ) {
            return Ok(Statement::Declaration(Declaration {
                identifier: name,
                expr: None,
                span: Span {
                    start,
                    end: self.current_token.span.end,
                },
            }));
        }
        self.next_token();
        self.next_token();

        let value = self.parse_expression()?.0;

        let end = self.current_token.span.end;

        Ok(Statement::Declaration(Declaration {
            identifier: name,
            expr: Some(value),
            span: Span { start, end },
        }))
    }

    fn parse_assignment_statement(&mut self) -> Result<Statement, ParseError> {
        let start = self.current_token.span.start;

        let name = self.current_token.clone();

        if !matches!(&self.current_token.kind, TokenKind::IDENTIFIER { .. }) {
            return Err(format!("{} not an identifier", self.current_token));
        }

        self.expect_peek(&TokenKind::R)?;
        self.next_token();

        let value = self.parse_expression()?.0;

        let end = self.current_token.span.end;

        Ok(Statement::Assignment(Assignment {
            identifier: name,
            expr: value,
            span: Span { start, end },
        }))
    }

    fn parse_expression(&mut self) -> Result<(Expression, Span), ParseError> {
        let start = self.current_token.span.start;

        let expr = self.parse_prefix_expression()?;

        let end = self.current_token.span.end;

        Ok((expr, Span { start, end }))
    }

    fn parse_prefix_expression(&mut self) -> Result<Expression, ParseError> {
        match &self.current_token.kind {
            TokenKind::IDENTIFIER { name } => Ok(Expression::IDENTIFIER(IDENTIFIER {
                name: name.clone(),
                span: self.current_token.clone().span,
            })),
            TokenKind::NUMBR(integer) => Ok(Expression::LITERAL(Literal::NUMBR(NUMBR {
                raw: *integer,
                span: self.current_token.clone().span,
            }))),
            TokenKind::NUMBAR(float) => Ok(Expression::LITERAL(Literal::NUMBAR(NUMBAR {
                raw: *float,
                span: self.current_token.clone().span,
            }))),
            TokenKind::YARN(string) => Ok(Expression::LITERAL(Literal::YARN(YARN {
                raw: string.to_string(),
                span: self.current_token.clone().span,
            }))),
            TokenKind::TROOF(bool) => Ok(Expression::LITERAL(Literal::TROOF(TROOF {
                raw: *bool,
                span: self.current_token.clone().span,
            }))),
            TokenKind::SUM
            | TokenKind::DIFF
            | TokenKind::PRODUKT
            | TokenKind::QUOSHUNT
            | TokenKind::MOD
            | TokenKind::BIGGR
            | TokenKind::SMALLR
            | TokenKind::BothOf
            | TokenKind::EitherOf
            | TokenKind::WonOf
            | TokenKind::BothSaem
            | TokenKind::DIFFRINT => {
                let op = self.current_token.clone();
                self.parse_binary_op(op)
            }
            TokenKind::AllOf | TokenKind::AnyOf => {
                let op = self.current_token.clone();
                self.parse_multi_op(op)
            }
            TokenKind::SMOOSH => {
                let op = self.current_token.clone();
                self.parse_smoosh_op(op)
            }
            TokenKind::NOT => {
                let op = self.current_token.clone();
                self.parse_unary_op(op)
            }
            TokenKind::IIz => self.parse_fn_call_expression(),
            TokenKind::MAEK => self.parse_typecast_expression(),
            TokenKind::IT => Ok(Expression::IDENTIFIER(IDENTIFIER {
                name: "IT".to_string(), 
                span: self.current_token.clone().span,
            })),

            token => Err(format!(
                "No implementation yet: {} {{start:{} end:{}}}",
                token, self.current_token.span.start, self.current_token.span.end
            )),
        }
    }

    fn parse_typecast_expression(&mut self) -> Result<Expression, ParseError> {
        let start = self.current_token.span.start;
        self.next_token();

        let expr = self.parse_expression()?.0;

        self.next_token();

        if self.current_token_is(&TokenKind::A) {
            self.next_token();
        }

        let target_type = self.parse_type()?;

        let end = self.current_token.span.start;

        Ok(Expression::Typecast(TypecastExpression {
            expression: Box::new(expr),
            target_type,
            span: Span { start, end },
        }))
    }

    fn parse_fn_call_expression(&mut self) -> Result<Expression, ParseError> {
        let start = self.current_token.span.start;
        self.next_token();

        let func_name: IDENTIFIER = match &self.current_token.kind {
            TokenKind::IDENTIFIER { name } => IDENTIFIER {
                name: name.clone(),
                span: self.current_token.span.clone(),
            },
            token => {
                return Err(format!(
                    "expected function params to be an identifier, got {}",
                    token
                ));
            }
        };

        if !matches!(&self.current_token.kind, TokenKind::IDENTIFIER { .. }) {
            return Err(format!("{} not an identifier", self.current_token));
        }

        let mut arguments = vec![];
        if self.peek_token_is(&TokenKind::Yr) {
            self.next_token();
            self.next_token();

            arguments.push(self.parse_expression()?.0);

            while self.peek_token_is(&TokenKind::AN) {
                self.next_token();
                self.expect_peek(&TokenKind::Yr)?;
                self.next_token();

                arguments.push(self.parse_expression()?.0);
            }
        }

        self.expect_peek(&TokenKind::MKAY)?;

        let end = self.current_token.span.end;

        Ok(Expression::FunctionCall(FunctionCall {
            arguments,
            span: Span { start, end },
            name: func_name,
        }))
    }

    fn parse_binary_op(&mut self, token: Token) -> Result<Expression, ParseError> {
        let start = self.current_token.span.start;
        self.next_token();

        let left = self.parse_expression()?.0;

        self.expect_peek(&TokenKind::AN)?;
        self.next_token();

        let right = self.parse_expression()?.0;

        let end = self.current_token.span.end;

        Ok(Expression::PREFIX(PrefixExpression::Binary(
            BinaryExpression {
                op: token,
                left: Box::new(left.clone()),
                right: Box::new(right),
                span: Span { start, end },
            },
        )))
    }

    fn parse_multi_op(&mut self, token: Token) -> Result<Expression, ParseError> {
        let start = self.current_token.span.start;
        self.next_token();

        let mut args = vec![self.parse_expression()?.0];

        while self.peek_token_is(&TokenKind::AN) {
            self.next_token();
            self.next_token();
            args.push(self.parse_expression()?.0);
        }

        self.expect_peek(&TokenKind::MKAY)?;

        let end = self.current_token.span.end;

        Ok(Expression::PREFIX(PrefixExpression::Multi(
            MultiExpression {
                op: token,
                args,
                span: Span { start, end },
            },
        )))
    }

    fn parse_smoosh_op(&mut self, token: Token) -> Result<Expression, ParseError> {
        let start = self.current_token.span.start;
        self.next_token();

        let mut args = vec![self.parse_expression()?.0];

        while self.peek_token_is(&TokenKind::AN) {
            self.next_token();
            self.next_token();
            args.push(self.parse_expression()?.0);
        }

        let end = self.current_token.span.end;

        Ok(Expression::PREFIX(PrefixExpression::Multi(
            MultiExpression {
                op: token,
                args,
                span: Span { start, end },
            },
        )))
    }

    fn parse_unary_op(&mut self, token: Token) -> Result<Expression, ParseError> {
        let start = self.current_token.span.start;
        self.next_token();

        let operand = Box::new(self.parse_expression()?.0);

        let end = self.current_token.span.end;

        Ok(Expression::PREFIX(PrefixExpression::Unary(
            UnaryExpression {
                op: token,
                operand,
                span: Span { start, end },
            },
        )))
    }
}
