from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from syntax_analyzer import (
    ASTNode, BreakStatementNode, NodeType, ProgramNode, VariableDeclarationNode,
    LiteralNode, IdentifierNode, PrintNode, AssignmentNode,
    InputNode, IfStatementNode, LoopNode, FunctionDefinitionNode,
    FunctionCallNode, TypecastingNode, SwitchStatementNode, ReturnStatementNode, ArithmeticNode,
    BooleanNode, InfiniteArityBooleanNode, UnaryOperationNode
)
from lexical_analyzer import TokenType

@dataclass
class FunctionInfo:
    parameters: List[str]
    body: List[ASTNode]
    return_type: Optional[TokenType] = None

class SemanticAnalyzer:
    def __init__(self):
        self.variables: Dict[str, TokenType] = {}
        self.functions: Dict[str, FunctionInfo] = {}
        self.current_scope: List[Dict[str, Any]] = [{"IT": None}]
        self.in_loop = False
        self.current_function: Optional[str] = None

    def analyze(self, ast: ProgramNode) -> None:
        """Perform semantic analysis on the AST"""
        # Analyze declarations
        for declaration in ast.declarations:
            self.analyze_node(declaration)
            
        # Analyze statements
        for statement in ast.statements:
            self.analyze_node(statement)

    def analyze_node(self, node: ASTNode) -> Optional[TokenType]:
        """Analyze a single node in the AST"""
        if node is None:
            return None

        handlers = {
            NodeType.VARIABLE_DECLARATION: self.analyze_variable_declaration,
            NodeType.VARIABLE_ASSIGNMENT: self.analyze_assignment,
            NodeType.FUNCTION_DEFINITION: self.analyze_function_definition,
            NodeType.FUNCTION_CALL: self.analyze_function_call,
            NodeType.IF_STATEMENT: self.analyze_if_statement,
            NodeType.SWITCH_STATEMENT: self.analyze_switch_statement,
            NodeType.LOOP: self.analyze_loop,
            NodeType.PRINT: self.analyze_print,
            NodeType.INPUT: self.analyze_input,
            NodeType.RETURN: self.analyze_return,
            NodeType.TYPECASTING: self.analyze_typecasting,
            NodeType.ARITHMETIC: self.analyze_arithmetic,
            NodeType.BOOLEAN: self.analyze_boolean,
            NodeType.LITERAL: self.analyze_literal,
            NodeType.IDENTIFIER: self.analyze_identifier,
            NodeType.COMPARISON: self.analyze_comparison,
            NodeType.EXPRESSION: self.analyze_expression
        }

        handler = handlers.get(node.type)
        if handler:
            return handler(node)
       
        raise SemanticError(f"Unknown node type: {node.type}", node.line)

    def analyze_expression(self, node: ASTNode) -> TokenType:
        """Analyze an expression node based on its type."""
        if isinstance(node, ArithmeticNode):
            return self.analyze_arithmetic(node)
        elif isinstance(node, BooleanNode):
            return self.analyze_boolean(node)
        elif isinstance(node, LiteralNode):
            return self.analyze_literal(node)
        elif isinstance(node, IdentifierNode):
            return self.analyze_identifier(node)
        elif isinstance(node, InfiniteArityBooleanNode):
            return self.analyze_infinite_arity_boolean(node)
        elif isinstance(node, UnaryOperationNode):
            return self.analyze_unary_operation(node)
        else:
            raise SemanticError(f"Unknown expression type: {node.type}", node.line)

    def analyze_variable_declaration(self, node: VariableDeclarationNode) -> None:
        """Analyze variable declaration"""
        if node.name in self.current_scope[-1]:
            raise SemanticError(f"Variable {node.name} already declared", node.line)

        # If there's an initial value, analyze it and use its type
       
        if node.initial_value is not None:
            var_type = self.analyze_node(node.initial_value)
        else:
            var_type = TokenType.NOOB  # Default type for uninitialized variables
        
        self.current_scope[-1][node.name] = var_type
        

    def analyze_assignment(self, node: AssignmentNode) -> TokenType:
        """Analyze variable assignment"""
        if node.target == "IT":
        # Allow assignment to the implicit variable IT without declaration
            value_type = self.analyze_node(node.value)
            return value_type
        
        if node.target not in self.current_scope[-1]:
            raise SemanticError(f"Variable {node.target} not declared", node.line)

        value_type = self.analyze_node(node.value)
        target_type = self.current_scope[-1][node.target]

        # Check if the assignment involves typecasting
        if node.type == TokenType.IS_NOW_A:
            # Check if the value can be converted to the target type
            if target_type == TokenType.NUMBAR and value_type == TokenType.YARN:
                # Attempt to convert the string to a number
                try:
                    float_value = float(node.value.value)  # Assuming node.value is a LiteralNode
                    return TokenType.NUMBAR  # Successfully casted to NUMBAR
                except ValueError:
                    raise SemanticError(f"Cannot convert {node.value.value} to NUMBAR", node.line)

        # Check type compatibility
        if not self.is_compatible_type(value_type, target_type):
            raise SemanticError(
                f"Type mismatch: Cannot assign {value_type} to {target_type}",
                node.line
            )

        return value_type

    def analyze_function_definition(self, node: FunctionDefinitionNode) -> None:
        """Analyze function definition"""
        print('\nNODE: ', node)
        if node.name in self.functions:
            raise SemanticError(f"Function {node.name} already defined", node.line)

        # Create new scope for function
        self.current_scope.append({})
        self.current_function = node.name

        # Add parameters to function scope
        for param in node.parameters:
            self.current_scope[-1][param] = TokenType.NOOB  # Parameters start as NOOB type

        # Add function info before analyzing body
        self.functions[node.name] = FunctionInfo(
            parameters=node.parameters,
            body=node.body,
            return_type=None  # Initially no return type
        )

        # Analyze function body
        return_type = None
        for stmt in node.body:
            print('\nstmt: ', stmt)
            stmt_type = self.analyze_node(stmt)
            if isinstance(stmt, ReturnStatementNode):
                return_type = stmt_type
                # Update return type in function info
                self.functions[node.name] = FunctionInfo(
                    parameters=node.parameters,
                    body=node.body,
                    return_type=return_type
                )

        print('\nEYYY ', self.functions)

        # Restore scope
        self.current_scope.pop()
        self.current_function = None

    def analyze_function_call(self, node: FunctionCallNode) -> Optional[TokenType]:
        """Analyze function call"""
        if node.name not in self.functions:
            raise SemanticError(f"Function {node.name} not defined", node.line)

        func_info = self.functions[node.name]

        # Check argument count
        if len(node.arguments) != len(func_info.parameters):
            raise SemanticError(
                f"Function {node.name} expects {len(func_info.parameters)} arguments, "
                f"got {len(node.arguments)}",
                node.line
            )

        # Analyze arguments
        for arg in node.arguments:
            self.analyze_node(arg)

        return func_info.return_type


    def analyze_if_statement(self, node: IfStatementNode) -> None:
        """Analyze if statement"""
        # Analyze condition - must evaluate to TROOF
        print('\nnode: ', node)
        condition_type = self.analyze_node(node.condition)
        if condition_type not in [TokenType.TROOF, TokenType.NOOB, None]:
            raise SemanticError(
                f"If condition must be TROOF, got {condition_type}",
                node.line
            )

        # Create new scope for each branch
        self.current_scope.append({})
        for stmt in node.true_branch:
            self.analyze_node(stmt)
        self.current_scope.pop()

        if node.false_branch:
            self.current_scope.append({})
            for stmt in node.false_branch:
                self.analyze_node(stmt)
            self.current_scope.pop()

    def analyze_switch_statement(self, node: SwitchStatementNode) -> None:
        """Analyze switch statement"""
        # Create new scope for switch execution
        self.current_scope.append({})

        # Analyze each case
        for case_value, case_statements in node.cases:
            # Analyze case value
            case_type = self.analyze_node(case_value)
            
            # Analyze case statements
            for stmt in case_statements:
                if isinstance(stmt, BreakStatementNode):
                    continue
                self.analyze_node(stmt)

        # Analyze default case if present
        if node.default:
            for stmt in node.default:
                if isinstance(stmt, BreakStatementNode):
                    continue
                self.analyze_node(stmt)

        # Restore scope
        self.current_scope.pop()

    def analyze_loop(self, node: LoopNode) -> None:
        """Analyze loop statement"""
        # Save previous loop state and set current loop state
        prev_in_loop = self.in_loop
        self.in_loop = True

        # Analyze loop condition
        condition_type = self.analyze_node(node.condition)
        if condition_type not in [TokenType.TROOF, TokenType.NOOB]:
            raise SemanticError(
                f"Loop condition must be TROOF, got {condition_type}",
                node.line
            )

        # Analyze increment if present
        if node.increment:
            incr_type = self.analyze_node(node.increment)
            if incr_type not in [TokenType.NUMBR, TokenType.NUMBAR]:
                raise SemanticError(
                    f"Loop increment must be numeric, got {incr_type}",
                    node.line
                )

        # Create new scope for loop body
        self.current_scope.append({})
        for stmt in node.body:
            self.analyze_node(stmt)
        self.current_scope.pop()

        # Restore previous loop state
        self.in_loop = prev_in_loop

    def analyze_print(self, node: PrintNode) -> None:
        """Analyze print statement"""
        for expr in node.expressions:
            self.analyze_node(expr)

    def analyze_input(self, node: InputNode) -> None:
        """Analyze input statement"""
        print(self.current_scope)
        print(node.variable)
        if node.variable not in self.current_scope[0]:
            raise SemanticError(f"Undefined variable {node.variable}", node.line)

    def analyze_return(self, node: ReturnStatementNode) -> TokenType:
        """Analyze return statement"""
        if not self.current_function:
            raise SemanticError("Return statement outside function", node.line)
        print('\nnode: ', node)
        print('\nself.current_function: ', self.current_function)
        print('\nself.functions: ', self.functions)
        return_type = self.analyze_node(node.expression)
        func_info = self.functions[self.current_function]
       
        # If this is the first return in the function, set its return type
        if func_info.return_type is None:
            func_info.return_type = return_type
        # Otherwise check that return types match
        elif not self.is_compatible_type(return_type, func_info.return_type):
            raise SemanticError(
                f"Inconsistent return type: expected {func_info.return_type}, got {return_type}",
                node.line
            )

        return return_type

    def analyze_typecasting(self, node: TypecastingNode) -> TokenType:
        """Analyze typecasting operation"""
        value_type = self.analyze_node(node.value)
        
        # Check if the typecast is valid
        if not self.is_valid_typecast(value_type, node.new_type):
            raise SemanticError(
                f"Invalid typecast from {value_type} to {node.new_type}",
                node.line
            )
            
        return node.new_type

    def analyze_arithmetic(self, node: ArithmeticNode) -> TokenType:
        """Analyze arithmetic operation"""
        left_type = self.analyze_node(node.left)
        right_type = self.analyze_node(node.right)

        # Check if operands are numeric, TROOF, or YARN that can be converted to numeric
        if not (self.is_numeric_type(left_type) or left_type == TokenType.TROOF or left_type == TokenType.YARN) or \
           not (self.is_numeric_type(right_type) or right_type == TokenType.TROOF or right_type == TokenType.YARN):
            raise SemanticError(
                f"Arithmetic operations require numeric types, TROOF (which casts WIN to 1/1.0 and FAIL to 0), or YARN containing numeric values, got {left_type} and {right_type}",
                node.line
            )

        # Return NUMBAR if either operand is NUMBAR, otherwise NUMBR
        # TROOF values will be implicitly cast to NUMBR (0 or 1)
        # YARN values will be converted to NUMBR or NUMBAR based on content
        return TokenType.NUMBAR if TokenType.NUMBAR in (left_type, right_type) else TokenType.NUMBR

    def analyze_boolean(self, node: BooleanNode) -> TokenType:
        """Analyze boolean operation"""
        
        # Handle ALL OF and ANY OF operators which have multiple operands
        if node.operator in [TokenType.ALL_OF, TokenType.ANY_OF]:
            if isinstance(node, InfiniteArityBooleanNode):
                # Analyze each operand
                for operand in node.operands:
                    self.analyze_node(operand)
                return TokenType.TROOF
        
        # Handle binary boolean operators
        left_type = self.analyze_node(node.left)
        right_type = self.analyze_node(node.right)

        # All values can be used in boolean operations in LOLCODE
        return TokenType.TROOF
    
    def analyze_comparison(self, node: BooleanNode) -> TokenType:
        """
        Analyze comparison operation.
        LOLCODE uses combinations of BOTH SAEM, DIFFRINT, BIGGR OF, and SMALLR OF for comparisons
        """
        left_type = self.analyze_node(node.left)
        right_type = self.analyze_node(node.right)

        # For BOTH SAEM and DIFFRINT operations
        if node.operator in [TokenType.BOTH_SAEM, TokenType.DIFFRINT]:
            # Ensure both sides are compatible for equality or inequality
            if not self.is_compatible_type(left_type, right_type):
                raise SemanticError(
                    f"Type mismatch in comparison: {left_type} and {right_type}",
                    node.line
                )

        # Handle BIGGR OF and SMALLR OF for relational operations
        if isinstance(node.right, BooleanNode) and node.right.operator in [TokenType.BIGGR_OF, TokenType.SMALLR_OF]:
            if not (self.is_numeric_type(left_type) and 
                self.is_numeric_type(self.analyze_node(node.right.left)) and 
                self.is_numeric_type(self.analyze_node(node.right.right))):
                raise SemanticError(
                    f"Numeric comparison requires numeric types",
                    node.line
                )

        # All comparison operations return TROOF
        return TokenType.TROOF     

    def analyze_infinite_arity_boolean(self, node: InfiniteArityBooleanNode) -> TokenType:
        """Analyze infinite arity boolean operation (ALL OF, ANY OF)"""
        for operand in node.operands:
            self.analyze_node(operand)
        return TokenType.TROOF

    def analyze_unary_operation(self, node: UnaryOperationNode) -> TokenType:
        """Analyze unary operation"""
        operand_type = self.analyze_node(node.operand)
        
        if node.operator == TokenType.NOT:
            return TokenType.TROOF
        
        raise SemanticError(f"Unknown unary operator: {node.operator}", node.line)

    def analyze_literal(self, node: LiteralNode) -> TokenType:
        """Analyze literal value"""
        return node.value_type

    def analyze_identifier(self, node: IdentifierNode) -> TokenType:
        """Analyze identifier"""
        # Check all scopes from innermost to outermost
        for scope in reversed(self.current_scope):
            if node.name in scope:
                return scope[node.name]
        raise SemanticError(f"Undefined variable {node.name}", node.line)

    def is_numeric_type(self, type: TokenType) -> bool:
        """Check if type is numeric"""
        return type in [TokenType.NUMBR, TokenType.NUMBAR, TokenType.NOOB]

    def is_valid_typecast(self, from_type: TokenType, to_type: TokenType) -> bool:
        """Check if typecast is valid"""
        # NOOB can be cast to any type
        if from_type == TokenType.NOOB:
            return True

        # Define valid typecasts
        valid_casts = {
            TokenType.NUMBR: {TokenType.NUMBAR, TokenType.YARN, TokenType.TROOF},
            TokenType.NUMBAR: {TokenType.NUMBR, TokenType.YARN, TokenType.TROOF},
            TokenType.YARN: {TokenType.NUMBR, TokenType.NUMBAR, TokenType.TROOF},
            TokenType.TROOF: {TokenType.NUMBR, TokenType.NUMBAR, TokenType.YARN}
        }

        return to_type in valid_casts.get(from_type, set())

    def get_literal_value(self, node: ASTNode) -> Any:
        """Get the literal value from a node if possible"""
        if isinstance(node, LiteralNode):
            return node.value
        return None



    def is_compatible_type(self, source_type: TokenType, target_type: TokenType) -> bool:
        """Check if types are compatible for assignment"""
        # NOOB can be assigned to any type
        if source_type == TokenType.NOOB:
            return True

        # Same types are always compatible
        if source_type == target_type:
            return True

        # Define type conversion rules
        conversions = {
            TokenType.NUMBR: {TokenType.NUMBAR, TokenType.YARN, TokenType.NOOB},
            TokenType.NUMBAR: {TokenType.NUMBR, TokenType.YARN, TokenType.NOOB},
            TokenType.TROOF: {TokenType.YARN, TokenType.NOOB},
            TokenType.YARN: {TokenType.NUMBR, TokenType.NUMBAR, TokenType.TROOF, TokenType.NOOB}
        }

        return target_type in conversions.get(source_type, set())
    
    def print_symbol_table(self) -> None:
        """Print the current symbol table in a tabular format"""
        print("\nSymbol Table:")
        print(f"{'Variable':<20} {'Type':<15}")
        print("=" * 35)
        for scope in self.current_scope:
            for var, var_type in scope.items():
                print(f"{var:<20} {var_type.name:<15}")
    

class SemanticError(Exception):
    def __init__(self, message: str, line: int):
        self.message = message
        self.line = line
        super().__init__(f"Semantic Error at line {line}: {message}")