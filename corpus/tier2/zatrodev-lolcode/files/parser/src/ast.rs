use core::fmt;
use core::fmt::Result;
use lexer::token::{Span, Token, TokenKind};
use std::fmt::Formatter;

#[derive(Clone, Debug, PartialEq)]
pub enum Node {
    Program(Program),
    Statement(Box<Statement>),
    Expression(Box<Expression>),
}

impl fmt::Display for Node {
    fn fmt(&self, f: &mut Formatter<'_>) -> Result {
        match self {
            Node::Program(p) => write!(f, "{}", p),
            Node::Statement(stmt) => write!(f, "{}", stmt),
            Node::Expression(expr) => write!(f, "{}", expr),
        }
    }
}

#[derive(Clone, Debug, PartialEq)]
pub struct Program {
    pub body: Vec<Statement>,
    pub span: Span,
}

impl Program {
    pub fn new() -> Self {
        Program {
            body: vec![],
            span: Span { start: 0, end: 0 },
        }
    }
}

impl Default for Program {
    fn default() -> Self {
        Self::new()
    }
}

impl fmt::Display for Program {
    fn fmt(&self, f: &mut Formatter<'_>) -> Result {
        write!(f, "{}", format_statements(&self.body))
    }
}

#[derive(Clone, Debug, PartialEq)]
pub enum Statement {
    Print(Print),
    Input(Input),
    Declaration(Declaration),
    Assignment(Assignment),
    Expr(Expression),
    If(Box<If>),
    Switch(Box<Switch>),
    Loop(Box<LoopStatement>),
    FunctionDeclaration(Box<FunctionDeclaration>),
    Return(ReturnStatement),
    Recast(RecastStatement),
    Break(Span),
    Expression(Expression),
}

#[derive(Clone, Debug, PartialEq)]
pub struct Print {
    pub exprs: Vec<Expression>,
    pub span: Span,
}

#[derive(Clone, Debug, PartialEq)]
pub struct Input {
    pub identifier: Token,
    pub span: Span,
}

#[derive(Clone, Debug, PartialEq)]
pub struct Declaration {
    pub identifier: Token,
    pub expr: Option<Expression>,
    pub span: Span,
}

#[derive(Clone, Debug, PartialEq)]
pub struct Assignment {
    pub identifier: Token,
    pub expr: Expression,
    pub span: Span,
}

#[derive(Clone, Debug, PartialEq)]
pub struct If {
    pub condition: Box<Expression>,
    pub consequent: BlockStatement,
    pub elif_branches: Vec<(Expression, BlockStatement)>,
    pub alternate: Option<BlockStatement>,
    pub span: Span,
}

#[derive(Clone, Debug, PartialEq)]
pub struct Switch {
    pub condition: Expression,
    pub cases: Vec<(Expression, BlockStatement)>,
    pub default: Option<BlockStatement>,
    pub span: Span,
}

#[derive(Clone, Debug, PartialEq)]
pub struct LoopCondition {
    pub condition: Token,
    pub expr: Expression,
}

#[derive(Debug, Clone, PartialEq)]
pub struct RecastStatement {
    pub identifier: Token,
    pub new_type: LolType,
    pub span: Span,
}

impl fmt::Display for LoopCondition {
    fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
        match self.condition.kind {
            TokenKind::TIL | TokenKind::WILE => {
                write!(f, "{} {}", self.condition.kind, self.expr)
            }
            _ => panic!("LoopCondition must be TIL or WILE"),
        }
    }
}

#[derive(Clone, Debug, PartialEq)]
pub struct LoopStatement {
    pub label: Token,
    pub operation: Token,
    pub variable: Token,
    pub condition: Option<LoopCondition>,
    pub body: BlockStatement,
    pub span: Span,
}

#[derive(Clone, Debug, PartialEq)]
pub struct FunctionDeclaration {
    pub params: Vec<IDENTIFIER>,
    pub body: BlockStatement,
    pub span: Span,
    pub name: String,
}

#[derive(Clone, Debug, PartialEq)]
pub struct ReturnStatement {
    pub argument: Expression,
    pub span: Span,
}

fn indent_block(s: &str) -> String {
    s.lines()
        .map(|line| format!("    {}", line))
        .collect::<Vec<_>>()
        .join("\n")
}

impl fmt::Display for Statement {
    fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
        match self {
            Statement::Print(Print { exprs, .. }) => {
                write!(f, "VISIBLE {:#?}", exprs)
            }
            Statement::Input(Input { identifier: id, .. }) => {
                if let TokenKind::IDENTIFIER { name } = &id.kind {
                    write!(f, "GIMMEH {}", name)
                } else {
                    unreachable!()
                }
            }
            Statement::Declaration(Declaration {
                identifier: id,
                expr,
                ..
            }) => {
                if let TokenKind::IDENTIFIER { name } = &id.kind {
                    if let Some(expr) = expr {
                        write!(f, "I HAS A {} ITZ {}", name, expr)
                    } else {
                        write!(f, "I HAS A {}", name)
                    }
                } else {
                    unreachable!()
                }
            }
            Statement::Assignment(Assignment {
                identifier: id,
                expr,
                ..
            }) => {
                if let TokenKind::IDENTIFIER { name } = &id.kind {
                    write!(f, "{} R {}", name, expr)
                } else {
                    unreachable!()
                }
            }
            Statement::Expr(expr) | Statement::Expression(expr) => {
                write!(f, "{}", expr)
            }
            // FIX: Updated matching for boxed variants.
            Statement::If(if_stmt) => {
                writeln!(f, "{}\nO RLY?", if_stmt.condition)?;
                writeln!(f, "YA RLY")?;
                writeln!(f, "{}", indent_block(&if_stmt.consequent.to_string()))?;
                for (cond, block) in &if_stmt.elif_branches {
                    writeln!(f, "MEBBE {}", cond)?;
                    writeln!(f, "{}", indent_block(&block.to_string()))?;
                }
                if let Some(else_block) = &if_stmt.alternate {
                    writeln!(f, "NO WAI")?;
                    writeln!(f, "{}", indent_block(&else_block.to_string()))?;
                }
                write!(f, "OIC")
            }
            Statement::Switch(switch_stmt) => {
                writeln!(f, "{}\nWTF?", switch_stmt.condition)?;
                for (case_cond, block) in &switch_stmt.cases {
                    writeln!(f, "OMG {}", case_cond)?;
                    writeln!(f, "{}", indent_block(&block.to_string()))?;
                }
                if let Some(default_block) = &switch_stmt.default {
                    writeln!(f, "OMGWTF")?;
                    writeln!(f, "{}", indent_block(&default_block.to_string()))?;
                }
                write!(f, "OIC")
            }
            Statement::Loop(loop_stmt) => {
                let label_name = if let TokenKind::IDENTIFIER { name } = &loop_stmt.label.kind {
                    name
                } else {
                    unreachable!()
                };
                let variable_name = if let TokenKind::IDENTIFIER { name } = &loop_stmt.variable.kind
                {
                    name
                } else {
                    unreachable!()
                };
                let op_str = loop_stmt.operation.kind.to_string();

                write!(f, "IM IN YR {} {} YR {}", label_name, op_str, variable_name)?;
                if let Some(cond) = &loop_stmt.condition {
                    write!(f, " {}", cond)?;
                }
                writeln!(f)?;
                writeln!(f, "{}", indent_block(&loop_stmt.body.to_string()))?;
                write!(f, "IM OUTTA YR {}", label_name)
            }
            Statement::FunctionDeclaration(func_decl) => {
                let params_str = func_decl
                    .params
                    .iter()
                    .map(|p| format!("YR {}", p))
                    .collect::<Vec<_>>()
                    .join(" AN ");
                writeln!(f, "HOW IZ I {} {}", func_decl.name, params_str)?;
                writeln!(f, "{}", indent_block(&func_decl.body.to_string()))?;
                write!(f, "IF U SAY SO")
            }
            Statement::Return(ReturnStatement { argument, .. }) => {
                write!(f, "FOUND YR {}", argument)
            }
            Statement::Recast(RecastStatement {
                identifier,
                new_type,
                ..
            }) => {
                if let TokenKind::IDENTIFIER { name } = &identifier.kind {
                    write!(f, "{} IS NOW A {}", name, new_type)
                } else {
                    unreachable!()
                }
            }
            Statement::Break(_) => {
                write!(f, "GTFO")
            }
        }
    }
}
#[derive(Clone, Debug, PartialEq)]
pub struct BlockStatement {
    pub body: Vec<Statement>,
    pub span: Span,
}

impl fmt::Display for BlockStatement {
    fn fmt(&self, f: &mut Formatter<'_>) -> Result {
        write!(f, "{}", format_statements(&self.body))
    }
}

#[derive(Clone, Debug, PartialEq)]
pub enum Expression {
    IDENTIFIER(IDENTIFIER),
    LITERAL(Literal),
    PREFIX(PrefixExpression),
    FunctionCall(FunctionCall),
    Typecast(TypecastExpression),
}

#[derive(Clone, Debug, PartialEq)]
pub enum PrefixExpression {
    Unary(UnaryExpression),
    Binary(BinaryExpression),
    Multi(MultiExpression),
}

#[derive(Clone, Debug, Eq, Hash, PartialEq)]
pub struct IDENTIFIER {
    pub name: String,
    pub span: Span,
}

impl fmt::Display for IDENTIFIER {
    fn fmt(&self, f: &mut Formatter<'_>) -> Result {
        write!(f, "{}", &self.name)
    }
}

#[derive(Clone, Debug, PartialEq)]
pub struct TypecastExpression {
    pub expression: Box<Expression>,
    pub target_type: LolType,
    pub span: Span,
}

#[derive(Clone, Debug, PartialEq)]
pub struct UnaryExpression {
    pub op: Token,
    pub operand: Box<Expression>,
    pub span: Span,
}

#[derive(Clone, Debug, PartialEq)]
pub struct BinaryExpression {
    pub op: Token,
    pub left: Box<Expression>,
    pub right: Box<Expression>,
    pub span: Span,
}

#[derive(Clone, Debug, PartialEq)]
pub struct MultiExpression {
    pub op: Token,
    pub args: Vec<Expression>,
    pub span: Span,
}

#[derive(Clone, Debug, PartialEq)]
pub struct FunctionCall {
    pub name: IDENTIFIER,
    pub arguments: Vec<Expression>,
    pub span: Span,
}

impl fmt::Display for Expression {
    fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
        match self {
            Expression::IDENTIFIER(id) => write!(f, "{id}"),

            Expression::LITERAL(lit) => write!(f, "{lit}"),

            Expression::PREFIX(prefix) => write!(f, "{prefix}"),

            Expression::FunctionCall(function) => write!(f, "{function}"),

            Expression::Typecast(TypecastExpression {
                expression,
                target_type,
                ..
            }) => {
                write!(f, "MAEK {} {}", expression, target_type)
            }
        }
    }
}

impl fmt::Display for FunctionCall {
    fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
        write!(f, "I IZ {}", self.name)?;
        let mut args_iter = self.arguments.iter();
        if let Some(first_arg) = args_iter.next() {
            write!(f, " YR {}", first_arg)?;
        }
        for arg in args_iter {
            write!(f, " AN YR {}", arg)?;
        }

        Ok(())
    }
}
impl fmt::Display for PrefixExpression {
    fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
        match self {
            PrefixExpression::Unary(expr) => write!(f, "{expr}"),
            PrefixExpression::Binary(expr) => write!(f, "{expr}"),
            PrefixExpression::Multi(expr) => write!(f, "{expr}"),
        }
    }
}

impl fmt::Display for UnaryExpression {
    fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
        write!(f, "({} {})", self.op.kind, self.operand)
    }
}

impl fmt::Display for BinaryExpression {
    fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
        write!(f, "({} {} {})", self.op.kind, self.left, self.right)
    }
}

impl fmt::Display for MultiExpression {
    fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
        let args_str = self
            .args
            .iter()
            .map(|e| e.to_string())
            .collect::<Vec<_>>()
            .join(" ");
        write!(f, "({} {})", self.op.kind, args_str)
    }
}
#[derive(Clone, Debug, PartialEq)]
pub enum Literal {
    NUMBR(NUMBR),
    NUMBAR(NUMBAR),
    TROOF(TROOF),
    YARN(YARN),
}
#[derive(Clone, Debug, PartialEq)]
pub struct NUMBR {
    pub raw: i64,
    pub span: Span,
}

#[derive(Clone, Debug, PartialEq)]
pub struct NUMBAR {
    pub raw: f64,
    pub span: Span,
}

#[derive(Clone, Debug, PartialEq)]
pub struct TROOF {
    pub raw: bool,
    pub span: Span,
}

#[derive(Clone, Debug, PartialEq)]
pub struct YARN {
    pub raw: String,
    pub span: Span,
}

impl fmt::Display for Literal {
    fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
        match self {
            Literal::NUMBR(NUMBR { raw: i, .. }) => write!(f, "{}", i),
            Literal::NUMBAR(NUMBAR { raw: fl, .. }) => write!(f, "{}", fl),
            Literal::TROOF(TROOF { raw: b, .. }) => write!(f, "{}", b),
            Literal::YARN(YARN { raw: s, .. }) => write!(f, "\"{}\"", s),
        }
    }
}

#[derive(Debug, Clone, PartialEq)]
pub enum LolType {
    NUMBR,
    NUMBAR,
    YARN,
    TROOF,
}

impl fmt::Display for LolType {
    fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
        match self {
            LolType::NUMBR => write!(f, "NUMBR"),
            LolType::NUMBAR => write!(f, "NUMBAR"),
            LolType::YARN => write!(f, "YARN"),
            LolType::TROOF => write!(f, "TROOF"),
        }
    }
}

// FIX: Changed `&Vec<Statement>` to `&[Statement]` for a more flexible API.
// FIX: Removed the needless `return` keyword.
fn format_statements(statements: &[Statement]) -> String {
    statements
        .iter()
        .map(|stmt| stmt.to_string())
        .collect::<Vec<String>>()
        .join("\n")
}
