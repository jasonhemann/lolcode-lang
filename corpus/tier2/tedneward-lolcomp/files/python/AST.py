from dataclasses import dataclass
from typing import List, Optional, Union
from enum import Enum, auto

class MathOp(Enum):
    MUL = "PRODUKT OF"
    DIV = "QUOSHUNT OF"
    MOD = "MOD OF"
    ADD = "SUM OF"
    SUB = "DIFF OF"

class ComparisonOp(Enum):
    EQUAL = "BOTH SAEM"
    DIFFERENT = "DIFFRINT"
    GREATER = "BIGGR OF"
    SMALLER = "SMALLR OF"

class LogicalOp(Enum):
    ALL = "ALL OF"
    ANY = "ANY OF"
    BOTH = "BOTH OF"
    EITHER = "EITHER OF"
    NOT = "NOT"

@dataclass
class Node:
    """Base class for all AST nodes"""
    pass

@dataclass
class Program(Node):
    """Root node of the program"""
    version: Optional[str]
    body: List['Statement']

@dataclass
class Statement(Node):
    """Base class for all statements"""
    pass

@dataclass
class Declaration(Statement):
    """Variable declaration: I HAS A &lt;name> [ITZ &lt;expr>]"""
    name: str
    initial_value: Optional['Expression'] = None

@dataclass
class Assignment(Statement):
    """Variable assignment: &lt;name> R &lt;expr>"""
    name: str
    value: 'Expression'

@dataclass
class PrintStatement(Statement):
    """Print statement: VISIBLE &lt;expr>* MKAY?"""
    expressions: List['Expression']

@dataclass
class InputStatement(Statement):
    """Input statement: GIMMEH &lt;name>"""
    name: str

@dataclass
class LoopStatement(Statement):
    """Loop statement: IM IN YR &lt;label> WILE &lt;expr> &lt;code> IM OUTTA YR &lt;label>"""
    label: str
    condition: 'Expression'
    body: List[Statement]

@dataclass
class IfStatement(Statement):
    """If statement: &lt;expr>, O RLY? YA RLY &lt;code> [NO WAI &lt;code>] OIC"""
    condition: 'Expression'
    then_branch: List[Statement]
    else_branch: Optional[List[Statement]] = None

@dataclass
class FunctionDecl(Statement):
    """Function declaration: HOW DUZ I &lt;name> [YR &lt;param> [AN YR &lt;param>]*] &lt;code> IF U SAY SO"""
    name: str
    parameters: List[str]
    body: List[Statement]

@dataclass
class Expression(Node):
    """Base class for all expressions"""
    pass

@dataclass
class Literal(Expression):
    """Literal values (WIN, FAIL, NOOB, numbers, strings)"""
    value: Union[bool, int, float, str, None]

@dataclass
class Variable(Expression):
    """Variable reference"""
    name: str

@dataclass
class MathExpr(Expression):
    """Math operations"""
    op: MathOp
    left: Expression
    right: Expression

@dataclass
class ComparisonExpr(Expression):
    """Comparison operations"""
    op: ComparisonOp
    left: Expression
    right: Expression

@dataclass
class LogicalExpr(Expression):
    """Logical operations"""
    op: LogicalOp
    operands: List[Expression]  # For ALL OF/ANY OF which can take multiple expressions

@dataclass
class UnaryExpr(Expression):
    """Unary operations (NOT)"""
    op: LogicalOp
    operand: Expression

@dataclass
class FunctionCall(Expression):
    """Function call: &lt;name> [YR &lt;expr> [AN YR &lt;expr>]*] MKAY?"""
    name: str
    arguments: List[Expression]

