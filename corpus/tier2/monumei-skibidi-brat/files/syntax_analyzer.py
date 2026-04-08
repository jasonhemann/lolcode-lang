from enum import Enum, auto
from typing import List, Dict, Optional, Any
from lexical_analyzer import Token, TokenType
from dataclasses import dataclass, field

# Node types for AST
class NodeType(Enum):
    PROGRAM = auto()
    VARIABLE_DECLARATION = auto()
    VARIABLE_ASSIGNMENT = auto()
    TYPECASTING = auto()  # Added for typecasting
    EXPRESSION = auto()
    ARITHMETIC = auto()
    BOOLEAN = auto()
    COMPARISON = auto()
    FUNCTION_DEFINITION = auto()
    FUNCTION_CALL = auto()
    IF_STATEMENT = auto()
    SWITCH_STATEMENT = auto()  # Added for switch statement
    CASE_STATEMENT = auto()     # Added for case statement
    LOOP = auto()
    PRINT = auto()
    INPUT = auto()
    RETURN = auto()
    BREAK = auto()
    LITERAL = auto()
    IDENTIFIER = auto()

# AST Node base class
@dataclass
class ASTNode:
    type: NodeType
    line: int
    position: int

@dataclass
class ProgramNode(ASTNode):
    declarations: List[ASTNode] = field(default_factory=list)
    statements: List[ASTNode] = field(default_factory=list)

@dataclass
class VariableDeclarationNode(ASTNode):
    name: str
    initial_value: Optional[ASTNode] = None

@dataclass
class UnaryOperationNode(ASTNode):
    operator: TokenType
    operand: ASTNode

@dataclass
class ArithmeticNode(ASTNode):
    operator: TokenType
    left: ASTNode
    right: ASTNode

@dataclass
class BooleanNode(ASTNode):
    operator: TokenType
    left: ASTNode
    right: ASTNode

@dataclass
class InfiniteArityBooleanNode(ASTNode):
    operator: TokenType
    operands: List[ASTNode]

@dataclass
class LiteralNode(ASTNode):
    value_type: TokenType
    value: Any

@dataclass
class IdentifierNode(ASTNode):
    name: str

@dataclass
class PrintNode(ASTNode):
    expressions: List[ASTNode]  # Changed to support multiple expressions

@dataclass
class InputNode(ASTNode):
    variable: str

@dataclass
class AssignmentNode(ASTNode):
    target: str
    value: ASTNode

@dataclass
class TypecastingNode(ASTNode):  # New node for typecasting
    target: str
    new_type: TokenType
    value: ASTNode

@dataclass
class IfStatementNode(ASTNode):
    condition: ASTNode
    true_branch: List[ASTNode]
    false_branch: List[ASTNode]

@dataclass
class SwitchStatementNode(ASTNode):  # New node for switch statement
    condition: ASTNode
    cases: List['CaseStatementNode']
    default: Optional[List[ASTNode]] = None

@dataclass
class CaseStatementNode(ASTNode):  # New node for case statement
    value: ASTNode
    statements: List[ASTNode]

@dataclass
class FunctionDefinitionNode(ASTNode):
    name: str
    parameters: List[str]
    body: List[ASTNode]

@dataclass
class FunctionCallNode(ASTNode):
    name: str
    arguments: List[ASTNode]

@dataclass
class LoopNode(ASTNode):
    identifier: str
    condition_type: TokenType  # TIL or WILE
    condition: ASTNode
    target: ASTNode
    increment: Optional[ASTNode]
    body: List[ASTNode]

@dataclass
class ReturnStatementNode(ASTNode):
    expression: ASTNode

@dataclass
class BreakStatementNode(ASTNode):
    expression: None

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current = 0
        self.scope_stack = [{}]
    
    def parse(self) -> ProgramNode:
        """Parse the entire program"""
        self.skip_whitespace_and_comments()
        if not self.match(TokenType.HAI):
            raise SyntaxError(f"Program must start with HAI at line {self.peek().line}")
            
        program_node = self.parse_program()
        self.skip_whitespace_and_comments()
        
        if not self.is_at_end():
            raise SyntaxError(f"Unexpected tokens after program end at line {self.peek().line}")
                
        return program_node
    
    def parse_program(self) -> ProgramNode:
        """Parse main program structure"""
        declarations = []
        statements = []
        
        while not self.check(TokenType.KTHXBYE):    
            
            self.skip_whitespace_and_comments()

            if self.match(TokenType.KTHXBYE):
                break

            if self.is_at_end():
                raise SyntaxError("Declaration section not properly closed with KTHXBYE")

           
            if self.match(TokenType.WAZZUP):
                declarations.extend(self.parse_declaration_section())
            
            if self.match(TokenType.I_HAS_A):
                raise SyntaxError(f"Expected WAZZUP at line {self.peek().line}")
            
            
            stmt = self.parse_statement()

            if stmt is not None:
                statements.append(stmt)
            
            

       
        self.skip_whitespace_and_comments()
     

                
        return ProgramNode(NodeType.PROGRAM, self.peek().line, self.peek().position, declarations, statements)

    def parse_declaration_section(self) -> List[ASTNode]:
        """Parse the WAZZUP declaration section"""
        self.skip_whitespace_and_comments()
        declarations = []

        while not self.match(TokenType.BUHBYE):
            self.skip_whitespace_and_comments()
         
            if self.check(TokenType.BUHBYE):
                continue

            if self.is_at_end():
                raise SyntaxError("Declaration section not properly closed with BUHBYE")
                
            if self.match(TokenType.I_HAS_A):
                dec = self.parse_declaration()
                if dec is not None:
                    declarations.append(dec)
                else:
                    raise SyntaxError(f"Error declaration at line {self.peek().line}")
                    
        return declarations

    def parse_declaration(self) -> Optional[VariableDeclarationNode]:
        """Parse variable declarations"""

        if not self.check(TokenType.VARIABLE_IDENTIFIER):
            raise SyntaxError(f"Expected variable identifier at line {self.peek().line}")
        
        var_name = self.advance().value
        initial_value = None
        token = self.peek()

        if token.type in [TokenType.NUMBR, TokenType.NUMBAR, TokenType.YARN, TokenType.TROOF]:
            raise SyntaxError(f"Expected ITZ keyword at line {self.peek().line}")
        
        if self.match(TokenType.ITZ):
            initial_value = self.parse_expression()
            if initial_value == None:
                raise SyntaxError(f"Expected a value at line {self.peek().line} after ITZ")

            
        return VariableDeclarationNode(
            NodeType.VARIABLE_DECLARATION,
            self.peek().line,
            self.peek().position,
            var_name,
            initial_value
        )

    def parse_statement(self) -> Optional[ASTNode]:
        """Parse different types of statements"""
        
        if self.match(TokenType.VISIBLE):
            return self.parse_print_statement()
        elif self.match(TokenType.GIMMEH):
            return self.parse_input_statement()
        elif self.match(TokenType.VARIABLE_IDENTIFIER):
            identifier = self.previous()
            self.skip_whitespace_and_comments()
            if self.check(TokenType.IS_NOW_A):
                return self.parse_is_now_a()
            elif self.check(TokenType.R):
                return self.parse_assignment()
            elif self.check(TokenType.WTF) or self.check(TokenType.O_RLY):
                return self.assign_implicit_variable_it(identifier)
            else:
                raise SyntaxError(f"Invalid statement at line {self.peek().line}")
        elif self.peek().type in [TokenType.YARN, TokenType.NUMBR, TokenType.NUMBAR]:
            raise SyntaxError(f"Invalid statement at line {self.peek().line}")
        elif self.match(TokenType.O_RLY):
            return self.parse_if_statement()
        elif self.match(TokenType.YA_RLY):
            raise SyntaxError(f"Expected O RLY? at line {self.peek().line-1}")
        elif self.match(TokenType.WTF):  # Handle switch statement
            return self.parse_switch_statement()
        elif self.match(TokenType.IM_IN_YR):
            return self.parse_loop()
        elif self.match(TokenType.HOW_IZ_I):
            return self.parse_function_definition()
        elif self.match(TokenType.I_IZ):
            return self.parse_function_call()
        elif self.check_expression_start():
            return self.parse_expression()
        elif self.match(TokenType.FOUND_YR):
            return self.parse_return_statement()
        elif self.match(TokenType.MAEK):  # Handle typecasting
            return self.parse_maek()
        elif self.match(TokenType.AN):
            raise SyntaxError(f"Invalid expression after at line {self.peek().line}")
        else:
            return None
        
    def assign_implicit_variable_it(self, identifier) -> IdentifierNode:
        # Store the result of the comparison in the implicit variable 'IT'
        return AssignmentNode(NodeType.VARIABLE_ASSIGNMENT, self.peek().line, self.peek().position, "IT", 
                                IdentifierNode(NodeType.IDENTIFIER, self.peek().line, self.peek().position, identifier.value))
                                
        
    def parse_return_statement(self) -> ReturnStatementNode:
        """Parse return statement"""
        expr = self.parse_expression()
        return ReturnStatementNode(NodeType.RETURN, self.peek().line, self.peek().position, expr)

    def parse_print_statement(self) -> PrintNode:
        """Parse print statement with proper concatenation
        Handles both explicit '+' concatenation and default concatenation between operands"""
        expressions = []
       
        while not self.check(TokenType.LINEBREAK) and not self.check(TokenType.KTHXBYE) and not self.is_at_end():
            self.skip_whitespace_and_comments()

            expr = self.parse_expression()
            
            if expr == None:
                continue
            expressions.append(expr)
            
            if self.check(TokenType.LINEBREAK) or self.is_at_end():
                break
                
            if self.match(TokenType.CONCATENATE):
                continue

    
        return PrintNode(NodeType.PRINT, self.peek().line, self.peek().position, expressions)

    def parse_input_statement(self) -> InputNode:
        """Parse input statement"""
        if not self.check(TokenType.VARIABLE_IDENTIFIER):
            raise SyntaxError(f"Expected variable identifier at line {self.peek().line}")
        
        var_name = self.advance().value
        return InputNode(NodeType.INPUT, self.peek().line, self.peek().position, var_name)

    def parse_assignment(self) -> AssignmentNode:
        """Parse variable assignment"""
        var_name = self.previous().value

        if not self.match(TokenType.R):
            raise SyntaxError(f"Expected R keyword at line {self.peek().line}")
        
        if self.match(TokenType.MAEK):
            return self.parse_maek()  # Handle typecasting if MAEK is followed by a type
            
        value = self.parse_expression()
        if value is None:
            raise SyntaxError(f"Expected a value at line {self.peek().line} after R")
        
        return AssignmentNode(NodeType.VARIABLE_ASSIGNMENT, self.peek().line, self.peek().position, var_name, value)

    def parse_maek(self) -> TypecastingNode:
        """Parse typecasting using MAEK operator"""
       
        target = self.peek()
        if not self.check(TokenType.VARIABLE_IDENTIFIER):
            raise SyntaxError(f"Expected variable identifier at line {self.peek().line}")
        
        target_var = self.advance().value
        
        if not self.check(TokenType.TYPE):
            raise SyntaxError(f"Expected type after MAEK at line {self.peek().line}")
        
        new_type = self.advance().value

        return TypecastingNode(
            NodeType.TYPECASTING,
            self.peek().line,
            self.peek().position,
            target_var,
            TokenType[new_type],
            IdentifierNode(NodeType.IDENTIFIER, target.line, target.position, target.value)
        )

    def parse_is_now_a(self) -> AssignmentNode:
        """Parse IS NOW A typecasting"""
        target = self.previous()
        target_var = self.previous().value  
        self.advance()
        if not self.check(TokenType.TYPE):
            raise SyntaxError(f"Expected variable TYPE at line {self.peek().line}")
                
        new_type = self.advance().value
        
        return TypecastingNode(
            NodeType.TYPECASTING,
            self.peek().line,
            self.peek().position,
            target_var,
            TokenType[new_type],
            IdentifierNode(NodeType.IDENTIFIER, target.line, target.position, target.value)
        )

    def parse_if_statement(self) -> IfStatementNode:
        """Parse if statement"""
        self.skip_whitespace_and_comments()
            
        condition = self.parse_expression()
        
        true_branch = []
        false_branch = []

     
        
        while not self.check(TokenType.NO_WAI) and not self.check(TokenType.OIC):
            self.skip_whitespace_and_comments()

            if self.is_at_end() or self.check(TokenType.KTHXBYE):
                raise SyntaxError(f"Expected OIC at line {self.peek().line}")

            stmt = self.parse_statement()
            if stmt is not None:
                true_branch.append(stmt)
            
            
        if self.match(TokenType.NO_WAI):
            while not self.check(TokenType.OIC):
                stmt = self.parse_statement()
                if stmt is not None:
                    false_branch.append(stmt)
                self.skip_whitespace_and_comments()
                
        if not self.match(TokenType.OIC):
            raise SyntaxError(f"Expected OIC at line {self.peek().line}")
            
        return IfStatementNode(
            NodeType.IF_STATEMENT,
            self.peek().line,
            self.peek().position,
            condition,
            true_branch,
            false_branch
        )

    def parse_switch_statement(self) -> SwitchStatementNode:
        """Parse switch-case statement"""
        self.skip_whitespace_and_comments()
        
        # The value to compare against IT
        cases = []
        default_case = []

        while not self.match(TokenType.OIC):
            self.skip_whitespace_and_comments()
        
            if self.match(TokenType.OMG):
                # Parse the case value
                case_value = self.parse_expression()  # Assuming this method parses the literal value
                code_block = []
                
                # Collect statements for this case
                while not self.check(TokenType.GTFO) and not self.check(TokenType.OMG) and not self.check(TokenType.OMGWTF):
                    stmt = self.parse_statement()
                    if stmt is not None:
                        code_block.append(stmt)
                    self.skip_whitespace_and_comments()
                
                
                if self.check(TokenType.GTFO):
                    stmt = self.parse_statement()
                    if stmt is not None:
                        code_block.append(stmt)
                    self.skip_whitespace_and_comments()
                
                cases.append((case_value, code_block))
  
            
            elif self.match(TokenType.OMGWTF):
                # Collect statements for the default case
                while not self.check(TokenType.OIC):
                    stmt = self.parse_statement()
                    if stmt is not None:
                        default_case.append(stmt)
                    self.skip_whitespace_and_comments()
            
            else:
                raise SyntaxError(f"Unexpected token at line {self.peek().line}")

     

        return SwitchStatementNode(
            NodeType.SWITCH_STATEMENT,
            self.peek().line,
            self.peek().position,
            None,
            cases,
            default_case
        )

    def parse_loop(self) -> LoopNode:
        """Parse loop statement"""
        if not self.check(TokenType.LOOP_IDENTIFIER):
            raise SyntaxError(f"Expected loop identifier at line {self.peek().line}")
            
        loop_id = self.advance().value
        condition_type = None
        increment = None
        target = None
        
        if self.match(TokenType.UPPIN):
            increment = LiteralNode(NodeType.LITERAL, self.peek().line, self.peek().position, TokenType.NUMBR, 1)
        elif self.match(TokenType.NERFIN):
            increment = LiteralNode(NodeType.LITERAL, self.peek().line, self.peek().position, TokenType.NUMBR, -1)
            
        if self.match(TokenType.YR):
            target = IdentifierNode(NodeType.IDENTIFIER, self.peek().line, self.peek().position, self.peek().value)
            self.advance()
        else:
            raise SyntaxError(f"Expected YR at line {self.peek().line}")
            
        if self.match(TokenType.TIL):
            condition_type = TokenType.TIL
        elif self.match(TokenType.WILE):
            condition_type = TokenType.WILE
        else:
            raise SyntaxError(f"Expected TIL or WILE at line {self.peek().line}")
            
        condition = self.parse_expression()
        body = []
        
        while not self.check(TokenType.IM_OUTTA_YR):
            stmt = self.parse_statement()
            if stmt is not None:
                body.append(stmt)
            self.skip_whitespace_and_comments()
            
        if not self.match(TokenType.IM_OUTTA_YR):
            raise SyntaxError(f"Expected IM OUTTA YR at line {self.peek().line}")
            
        if not self.check(TokenType.LOOP_IDENTIFIER) or self.peek().value != loop_id:
            raise SyntaxError(f"Loop identifier mismatch at line {self.peek().line}")
            
        self.advance()  # Consume loop identifier
        
        return LoopNode(
            NodeType.LOOP,
            self.peek().line,
            self.peek().position,
            loop_id,
            condition_type,
            condition,
            target,
            increment,
            body
        )

    def parse_expression(self) -> ASTNode:
        """Parse expressions including string concatenation"""
        if self.match(TokenType.SMOOSH):
            return self.parse_concatenation()
        elif self.match(TokenType.AN):
            raise SyntaxError(f"Invalid expression at line {self.peek().line}")
        elif self.match(TokenType.NOT):
            return UnaryOperationNode(
                NodeType.EXPRESSION,
                self.peek().line,
                self.peek().position,
                TokenType.NOT,
                self.parse_expression()
            )
        elif self.check_arithmetic_operator():
            return self.parse_arithmetic_expression()
        elif self.check_boolean_operator():
            return self.parse_boolean_expression()
        elif self.check_comparison_operator():
            return self.parse_comparison_expression()
        else:
            return self.parse_primary()

    def parse_concatenation(self) -> ASTNode:
        """Parse string concatenation (SMOOSH)"""
        expressions = []
        
        while not self.check(TokenType.LINEBREAK):
            if self.match(TokenType.AN):
                continue
            expr = self.parse_expression()
            if expr is None:
                if len(expressions) == 0:
                    raise SyntaxError(f"Expected expression at line {self.peek().line} after SMOOSH")
                elif self.previous().type == TokenType.AN:
                    raise SyntaxError(f"Expected expression at line {self.peek().line} after AN")
           
            expressions.append(expr)

        return InfiniteArityBooleanNode(
            NodeType.EXPRESSION,
            self.peek().line,
            self.peek().position,
            TokenType.SMOOSH,
            expressions
        )

    def parse_arithmetic_expression(self) -> ArithmeticNode:
        """Parse arithmetic expressions"""
        operator = self.advance().type
        left = self.parse_expression()
       
        if not self.match(TokenType.AN):
            raise SyntaxError(f"Expected AN at line {self.peek().line}")
        
        right = self.parse_expression()
        return ArithmeticNode(NodeType.ARITHMETIC, self.peek().line, self.peek().position, operator, left, right)

    def parse_boolean_expression(self) -> ASTNode:
        """Parse boolean expressions"""
        operator = self.advance().type
        
        if operator in [TokenType.ALL_OF, TokenType.ANY_OF]:
            operands = []
            while not self.match(TokenType.MKAY):
                operands.append(self.parse_expression())
                if not self.check(TokenType.MKAY):
                    if not self.match(TokenType.AN):
                        raise SyntaxError(f"Expected AN or MKAY at line {self.peek().line}")
                        
            return InfiniteArityBooleanNode(NodeType.BOOLEAN, self.peek().line, self.peek().position, operator, operands)
        else:
            left = self.parse_expression()
            if not self.match(TokenType.AN):
                raise SyntaxError(f"Expected AN at line {self.peek().line}")
            right = self.parse_expression()
            return BooleanNode(NodeType.BOOLEAN, self.peek().line, self.peek().position, operator, left, right)

    def parse_comparison_expression(self) -> BooleanNode:
        """Parse comparison expressions"""
        prev_node = self.previous()
        operator = self.advance().type
        left = self.parse_expression()

        if not self.match(TokenType.AN):
            raise SyntaxError(f"Expected AN at line {self.peek().line}")
            
        right = self.parse_expression()
        
        # Check if the previous token was a LINEBREAK
        if prev_node.type == TokenType.LINEBREAK:
            # Store the result of the comparison in the implicit variable 'IT'
            return AssignmentNode(NodeType.VARIABLE_ASSIGNMENT, self.peek().line, self.peek().position, "IT", 
                                  BooleanNode(NodeType.COMPARISON, self.peek().line, self.peek().position, operator, left, right))

        return BooleanNode(NodeType.COMPARISON, self.peek().line, self.peek().position, operator, left, right)

    def parse_primary(self) -> Optional[ASTNode]:
        """Parse primary expressions (literals, identifiers)"""
        token = self.peek()
        self.advance()
        if token.type in [TokenType.NUMBR, TokenType.NUMBAR, TokenType.YARN, TokenType.TROOF]:
            if token.type == TokenType.NUMBR:
                return LiteralNode(NodeType.LITERAL, token.line, token.position, token.type, int(token.value))
            elif token.type == TokenType.NUMBAR:
                return LiteralNode(NodeType.LITERAL, token.line, token.position, token.type, float(token.value))     
            return LiteralNode(NodeType.LITERAL, token.line, token.position, token.type, token.value)
        elif token.type == TokenType.VARIABLE_IDENTIFIER:
            return IdentifierNode(NodeType.IDENTIFIER, token.line, token.position, token.value)
        elif token.type == TokenType.GTFO:
            return BreakStatementNode(NodeType.BREAK, token.line, token.position, token.value)
        return None

    def check_expression_start(self) -> bool:
        """Check if current token can start an expression"""
        return (self.check(TokenType.NOT) or
                self.check_arithmetic_operator() or
                self.check_boolean_operator() or
                self.check_comparison_operator() or
                self.check(TokenType.NUMBR) or
                self.check(TokenType.NUMBAR) or
                self.check(TokenType.YARN) or
                self.check(TokenType.TROOF) or
                self.check(TokenType.VARIABLE_IDENTIFIER) or
                self.check(TokenType.GTFO))

    def check_arithmetic_operator(self) -> bool:
        """Check if current token is an arithmetic operator"""
        return self.check(TokenType.SUM_OF) or \
               self.check(TokenType.DIFF_OF) or \
               self.check(TokenType.PRODUKT_OF) or \
               self.check(TokenType.QUOSHUNT_OF) or \
               self.check(TokenType.MOD_OF) or \
               self.check(TokenType.BIGGR_OF) or \
               self.check(TokenType.SMALLR_OF)

    def check_boolean_operator(self) -> bool:
        """Check if current token is a boolean operator"""
        return self.check(TokenType.BOTH_OF) or \
               self.check(TokenType.EITHER_OF) or \
               self.check(TokenType.WON_OF) or \
               self.check(TokenType.ALL_OF) or \
               self.check(TokenType.ANY_OF)

    def check_comparison_operator(self) -> bool:
        """Check if current token is a comparison operator"""
        return self.check(TokenType.BOTH_SAEM) or \
               self.check(TokenType.DIFFRINT) or \
               self.check(TokenType.BIGGR_OF) or \
               self.check(TokenType.SMALLR_OF)

    def match(self, *token_types: TokenType) -> bool:
        """Check if the current token matches any of the given types and advance if it does"""
        for token_type in token_types:
            if self.check(token_type):
                self.advance()
                return True
        return False

    def check(self, token_type: TokenType) -> bool:
        """Check if the current token is of the given type"""
        if self.is_at_end():
            return False
        return self.peek().type == token_type

    def advance(self) -> Token:
        """Advance to next token and return the previous one"""
        previous = self.peek()
        self.current += 1
        return previous

    def peek(self) -> Token:
        """Return current token without consuming it"""
        return self.tokens[self.current]

    def previous(self) -> Token:
        """Return the previous token"""
        return self.tokens[self.current - 1]

    def is_at_end(self) -> bool:
        """Check if we've reached the end of the token stream"""
        return self.peek().type == TokenType.EOF

    def skip_whitespace_and_comments(self) -> None:
        """Skip over whitespace and comments"""
        while not self.is_at_end():
            if self.check(TokenType.LINEBREAK):
                self.advance()
            elif self.check(TokenType.BTW):  # Single line comment
                while not self.is_at_end() and not self.check(TokenType.LINEBREAK):
                    self.advance()
            elif self.check(TokenType.OBTW):  # Multi-line comment
                while not self.is_at_end() and not self.check(TokenType.TLDR):
                    self.advance()
                if self.check(TokenType.OBTW) and self.previous() != TokenType.LINEBREAK:
                    raise SyntaxError(f"Unexpected multi-line comment at line {self.peek().line}")
                if not self.match(TokenType.TLDR):
                    raise SyntaxError(f"Unclosed multi-line comment at line {self.peek().line}")
            else:
                break

    def parse_function_definition(self) -> FunctionDefinitionNode:
        """Parse function definition"""
        if not self.check(TokenType.FUNCTION_IDENTIFIER):
            raise SyntaxError(f"Expected function identifier at line {self.peek().line}")
            
        func_name = self.advance().value
        parameters = []
        body = []
        
        while not self.check(TokenType.IF_U_SAY_SO):
            self.skip_whitespace_and_comments()
            if self.check(TokenType.YR):
                self.advance()  # Skip YR
                if not self.check(TokenType.VARIABLE_IDENTIFIER):
                    raise SyntaxError(f"Expected parameter name at line {self.peek().line}")
                parameters.append(self.advance().value)
            elif self.check(TokenType.AN):
                self.advance()  # Skip AN
                if not self.check(TokenType.YR):
                    raise SyntaxError(f"Expected YR after AN at line {self.peek().line}")
                continue
            elif self.match(TokenType.GTFO):
                break
            else:
                stmt = self.parse_statement()
                if stmt is not None:
                    body.append(stmt)
                    continue
   
        self.skip_whitespace_and_comments()
        if not self.match(TokenType.IF_U_SAY_SO):
            raise SyntaxError(f"Expected IF U SAY SO at line {self.peek().line}")
        
        return FunctionDefinitionNode(
            NodeType.FUNCTION_DEFINITION,
            self.peek().line,
            self.peek().position,
            func_name,
            parameters,
            body
        )

    def parse_function_call(self) -> FunctionCallNode:
        """Parse function call"""
        if not self.check(TokenType.FUNCTION_IDENTIFIER):
            raise SyntaxError(f"Expected function identifier at line {self.peek().line}")
            
        func_name = self.advance().value
        arguments = []
        
        while not self.check(TokenType.MKAY):
            if self.check(TokenType.YR):
                self.advance()  # Skip YR
                arguments.append(self.parse_expression())
            elif self.check(TokenType.AN):
                self.advance()  # Skip AN
                if not self.check(TokenType.YR):
                    raise SyntaxError(f"Expected YR after AN at line {self.peek().line}")
                continue
            else:
                break
             
        if not self.match(TokenType.MKAY):
            raise SyntaxError(f"Expected MKAY at line {self.peek().line}")
            
        return FunctionCallNode(
            NodeType.FUNCTION_CALL,
            self.peek().line,
            self.peek().position,
            func_name,
            arguments
        )