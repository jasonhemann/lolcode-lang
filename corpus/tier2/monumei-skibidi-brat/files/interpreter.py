from typing import Dict, Any, Optional, List
from tkinter import simpledialog
import tkinter as tk

from syntax_analyzer import (
    ASTNode, NodeType, ProgramNode, TokenType
)
from semantics_analyzer import SemanticAnalyzer, FunctionInfo
from syntax_analyzer import (
    ASTNode, NodeType, ProgramNode, VariableDeclarationNode,
    LiteralNode, IdentifierNode, PrintNode, AssignmentNode,
    InputNode, IfStatementNode, LoopNode, FunctionDefinitionNode,
    FunctionCallNode, TypecastingNode, SwitchStatementNode,
    CaseStatementNode, ReturnStatementNode, ArithmeticNode,
    BooleanNode, InfiniteArityBooleanNode, UnaryOperationNode, BreakStatementNode
)

class Interpreter:
    def __init__(self):
        self.variables: Dict[str, Any] = {}
        self.functions: Dict[str, FunctionInfo] = {}
        self.current_scope: List[Dict[str, Any]] = [{"IT": None}]
        self.return_value: Optional[Any] = None
        self.console_output_function = None  # Added to hold reference to console output function

    def interpret(self, ast: ProgramNode, semantic_analyzer: SemanticAnalyzer) -> None:
        """Interpret the AST after semantic analysis"""
        # Initialize interpreter with analyzed functions
        self.functions = semantic_analyzer.functions

        # Execute declarations
        for declaration in ast.declarations:
            self.execute_node(declaration)

        # Execute statements
        for statement in ast.statements:
            self.execute_node(statement)

    def execute_node(self, node: ASTNode) -> Any:
        """Execute a single node in the AST"""
    
        if node is None:
            return None

        handlers = {
            NodeType.VARIABLE_DECLARATION: self.execute_variable_declaration,
            NodeType.VARIABLE_ASSIGNMENT: self.execute_assignment,
            NodeType.FUNCTION_DEFINITION: self.execute_function_definition,
            NodeType.FUNCTION_CALL: self.execute_function_call,
            NodeType.IF_STATEMENT: self.execute_if_statement,
            NodeType.SWITCH_STATEMENT: self.execute_switch_statement,
            NodeType.LOOP: self.execute_loop,
            NodeType.PRINT: self.execute_print,
            NodeType.INPUT: self.execute_input,
            NodeType.RETURN: self.execute_return,
            NodeType.ARITHMETIC: self.execute_arithmetic,
            NodeType.BOOLEAN: self.execute_boolean,
            NodeType.LITERAL: self.execute_literal,
            NodeType.IDENTIFIER: self.execute_identifier,
            NodeType.COMPARISON: self.execute_comparison,
            NodeType.EXPRESSION: self.execute_expression,
            NodeType.TYPECASTING: self.execute_typecasting,
            
        }

        handler = handlers.get(node.type)
        if handler:
            return handler(node)
        print(node)
        raise RuntimeError(f"Unknown node type: {node.type}")
    
    def execute_expression(self, node: ASTNode) -> Any:
        """Execute an expression node based on its type."""
        if isinstance(node, ArithmeticNode):
            return self.execute_arithmetic(node)
        elif isinstance(node, BooleanNode):
            return self.execute_boolean(node)
        elif isinstance(node, LiteralNode):
            return self.execute_literal(node)
        elif isinstance(node, IdentifierNode):
            return self.execute_identifier(node)
        elif isinstance(node, InfiniteArityBooleanNode):
            return self.execute_infinite_arity_boolean(node)
        elif isinstance(node, UnaryOperationNode):
            return self.execute_unary_operation(node)
        else:
            raise RuntimeError(f"Unknown expression type: {node.type}")

    def execute_variable_declaration(self, node: VariableDeclarationNode) -> None:
        """Execute variable declaration"""
        value = None
        if node.initial_value:
            value = self.execute_node(node.initial_value)
        self.current_scope[-1][node.name] = value

        # Update the symbol table in the GUI
        if hasattr(self, 'symbol_table_update_function') and self.symbol_table_update_function:
            self.symbol_table_update_function(self.get_symbol_table())

    def execute_assignment(self, node: AssignmentNode) -> Any:
        """Execute variable assignment"""
        value = self.execute_node(node.value)
        if node.target == "IT":
            # Assign the value to the implicit variable IT
            self.current_scope[-1]['IT'] = value
        else:
            self.current_scope[-1][node.target] = value

        # Update the symbol table in the GUI
        if hasattr(self, 'symbol_table_update_function') and self.symbol_table_update_function:
            self.symbol_table_update_function(self.get_symbol_table())

        return value

    def execute_function_definition(self, node: FunctionDefinitionNode) -> None:
        """Execute function definition
        In the interpreter, we just store the function info as it will be executed later when called"""
        self.functions[node.name] = {
            'parameters': node.parameters,
            'body': node.body,
            'scope': dict(self.current_scope[-1])  # Capture current scope for closure
        }

    def execute_function_call(self, node: FunctionCallNode) -> Any:
        """Execute function call"""
        if node.name not in self.functions:
            raise RuntimeError(f"Undefined function: {node.name}")

        func_info = self.functions[node.name]
        
        # Evaluate arguments in current scope
        args = [self.execute_node(arg) for arg in node.arguments]
        
        if len(args) != len(func_info['parameters']):
            raise RuntimeError(
                f"Function {node.name} expects {len(func_info['parameters'])} arguments, "
                f"got {len(args)}"
            )

        # Create new scope with captured function scope
        new_scope = dict(func_info['scope'])
        
        # Add arguments to function scope
        for param, arg in zip(func_info['parameters'], args):
            new_scope[param] = arg
            
        # Push new scope
        self.current_scope.append(new_scope)
        
        # Reset return value
        self.return_value = None
        
        # Execute function body
        result = None
        for stmt in func_info['body']:
            result = self.execute_node(stmt)
            if self.return_value is not None:
                result = self.return_value
                break
                
        # Restore scope
        self.current_scope.pop()
        
        # Reset return value
        self.return_value = None
        
        # Store result in IT variable in global scope
        self.current_scope[0]['IT'] = result
        
        return result

    def execute_return(self, node: ReturnStatementNode) -> Any:
        """Execute return statement"""
        value = self.execute_node(node.expression)
        self.return_value = value
        return value

    def execute_if_statement(self, node: IfStatementNode) -> Any:
        """Execute if statement"""
        condition = self.execute_node(node.condition)
        if condition == None:
            condition = self.current_scope[-1]['IT']
        # Create new scope for branch execution
        self.current_scope.append({})
        result = None
        if self.to_boolean(condition):
            for stmt in node.true_branch:
                result = self.execute_node(stmt)
                if self.return_value is not None:
                    break
        elif node.false_branch:
            for stmt in node.false_branch:
                result = self.execute_node(stmt)
                if self.return_value is not None:
                    break
                    
        # Restore scope
        self.current_scope.pop()
        return result

    def execute_switch_statement(self, node: SwitchStatementNode) -> Any:
        """Execute switch statement"""
        # Get the value of IT for comparison
        it_value = self.current_scope[-1].get('IT') 

        # Create new scope for switch execution
        self.current_scope.append({})

        result = None
        matched = False
        cont = False

        # Check each case
        for case_value, case_statements in node.cases:
            if self.values_equal(it_value, case_value.value) or cont:
                matched = True
                cont = True
                for stmt in case_statements:
                    if isinstance(stmt, BreakStatementNode):
                        cont = False
                        break  # Exit case execution on break
                    result = self.execute_node(stmt)
                    
                

        # Execute default case if no match found
        if not matched and node.default or cont:
            for stmt in node.default:
                if isinstance(stmt, BreakStatementNode):
                    break  # Exit default execution on break
                result = self.execute_node(stmt)
                if self.return_value is not None:  # Check for GTFO
                    break

        # Restore scope
        self.current_scope.pop()
        return result

    def execute_loop(self, node: LoopNode) -> Any:
        """Execute loop statement"""
        # Create new scope for loop execution
        # self.current_scope.append({})
        
        result = None
        cont = True
        
        # Get initial target value if it exists
        target_value = self.execute_identifier(node.target)
            
        if node.condition_type == TokenType.TIL:
            # Execute until condition becomes true
            while cont:
                condition = self.execute_node(node.condition)
                if self.to_boolean(condition):
                    break
                    
                for stmt in node.body:
                    if isinstance(stmt, BreakStatementNode):
                        cont = False
                        break
                    result = self.execute_node(stmt)
                    
                if node.increment and node.target:
                    # Update target value
                    target_value = target_value + node.increment.value
                    self.current_scope[-1][node.target.name] = target_value
                    
        elif node.condition_type == TokenType.WILE:
            # Execute while condition is true
            while cont:
                condition = self.execute_node(node.condition)
                if not self.to_boolean(condition):
                    break
                    
                for stmt in node.body:
                    if isinstance(stmt, BreakStatementNode):
                        cont = False
                        break
                    result = self.execute_node(stmt)
                    
                if node.increment and node.target:
                    # Update target value
                    target_value = target_value + node.increment.value
                    self.current_scope[-1][node.target.name] = target_value
        
        # Restore scope
        # self.current_scope.pop()
        return result

    def execute_print(self, node: PrintNode) -> None:
        """Execute print statement and redirect output to GUI console."""
        values = []
        for expr in node.expressions:
            value = self.execute_node(expr)
            values.append(str(value))
        if self.console_output_function:
            self.console_output_function(" ".join(values))  # Use the output function
        else:
            print(" ".join(values))  # Fallback to print if not set

    def execute_input(self, node: InputNode) -> str:
        """Execute input statement using a dialog without minimizing the main window."""
        root = tk.Tk()
        root.withdraw()  # Hide the root window but keep it active

        # Ensure the focus is set on the input dialog
        root.focus_force()

        # Create the dialog for input
        value = simpledialog.askstring("Input", f"Enter value for {node.variable}:", parent=root)

        if value is not None:  # Check if the user didn't cancel the dialog
            self.current_scope[-1][node.variable] = value

            # Update the symbol table in the GUI
            if hasattr(self, 'symbol_table_update_function') and self.symbol_table_update_function:
                self.symbol_table_update_function(self.get_symbol_table())  # Call the update function

        root.destroy()  # Destroy the root window after dialog is closed
        return value
    
    def execute_return(self, node: ReturnStatementNode) -> Any:
        """Execute return statement"""
        value = self.execute_node(node.expression)
        self.return_value = value
        return value

    def execute_boolean(self, node: BooleanNode) -> bool:
        """Execute boolean operation"""
        if isinstance(node, InfiniteArityBooleanNode):
            return self.execute_infinite_arity_boolean(node)

        left = self.execute_node(node.left)
        right = self.execute_node(node.right)

        operations = {
            TokenType.BOTH_OF: lambda x, y: self.to_boolean(x) and self.to_boolean(y),
            TokenType.EITHER_OF: lambda x, y: self.to_boolean(x) or self.to_boolean(y),
            TokenType.WON_OF: lambda x, y: self.to_boolean(x) != self.to_boolean(y),
            TokenType.BOTH_SAEM: lambda x, y: self.values_equal(x, y),
            TokenType.DIFFRINT: lambda x, y: not self.values_equal(x, y)
        }

        if node.operator not in operations:
            raise RuntimeError(f"Unknown boolean operator: {node.operator}")

        return operations[node.operator](left, right)

    def execute_infinite_arity_boolean(self, node: InfiniteArityBooleanNode) -> bool:
        """Execute infinite arity boolean operation (ALL OF, ANY OF)"""
        
        values = [self.execute_node(operand) for operand in node.operands]
       
        if node.operator == TokenType.ALL_OF:
            return all(self.to_boolean(value) for value in values)
        elif node.operator == TokenType.ANY_OF:
            return any(self.to_boolean(value) for value in values)
        elif node.operator == TokenType.SMOOSH:
        # Concatenate all string operands
            return ''.join(str(value) for value in values)  # Convert each value to string and concatenate
            
        raise RuntimeError(f"Unknown infinite arity operator: {node.operator}")

    def execute_unary_operation(self, node: UnaryOperationNode) -> Any:
        """Execute unary operation"""
        value = self.execute_node(node.operand)
        
        if node.operator == TokenType.NOT:
            return not self.to_boolean(value)
            
        raise RuntimeError(f"Unknown unary operator: {node.operator}")

    def execute_literal(self, node: LiteralNode) -> Any:
        """Execute literal node"""
        return node.value

    def execute_identifier(self, node: IdentifierNode) -> Any:
        """Execute identifier node"""
        # Check all scopes from innermost to outermost
        for scope in reversed(self.current_scope):
            if node.name in scope:
                return scope[node.name]
        raise RuntimeError(f"Undefined variable: {node.name}")

    def execute_typecasting(self, node: TypecastingNode) -> Any:
        """Execute typecasting operation"""
        value = self.execute_node(node.value)
        new_value = self.convert_value(value, node.new_type)
        self.current_scope[-1][node.target] = new_value
       
        return new_value

    # Helper methods
    def to_boolean(self, value: Any) -> bool:
        """Convert any value to boolean according to LOLCODE rules"""
        if isinstance(value, bool):
            return value
        elif isinstance(value, (int, float)):
            return value != 0
        elif isinstance(value, str):
            return len(value) > 0
        return bool(value)

    def values_equal(self, a: Any, b: Any) -> bool:
        """Compare values for equality according to LOLCODE rules"""
        # Handle numeric comparisons
        if isinstance(a, (int, float)) and isinstance(b, (int, float)):
            return abs(float(a) - float(b)) < 1e-10
        
        # Handle string comparisons
        if isinstance(a, str) or isinstance(b, str):
            return str(a) == str(b)
        
        # Handle boolean comparisons
        if isinstance(a, bool) or isinstance(b, bool):
            return self.to_boolean(a) == self.to_boolean(b)
        
        # Default comparison
        return a == b

    def convert_value(self, value: Any, target_type: TokenType) -> Any:
        """Convert value to target type according to LOLCODE rules."""
        if target_type == TokenType.TROOF:
            # Handle casting to TROOF (boolean)
            if value == "" or value == 0 or value is None:
                return False  # Cast to FAIL
            return True  # All other values cast to WIN

        if target_type in [TokenType.NUMBR, TokenType.NUMBAR]:
            # Handle casting to numeric types
            if value == "" or value is None:
                return 0  # FAIL casts to numerical zero
            elif value == "WIN" or value is True:
                return 1.0  # WIN casts to 1.0
            elif value == "FAIL" or value is False:
                return 0  # FAIL casts to numerical zero
            try:
                if isinstance(value, str):
                    # Remove quotes for string conversion
                    value = value.strip('"')
                if target_type == TokenType.NUMBR:
                    return int(float(value))  # Convert to integer
                elif target_type == TokenType.NUMBAR:
                    return float(value)  # Convert to float
            except (ValueError, TypeError):
                raise RuntimeError(f"Cannot convert {value} to {target_type}")

        if target_type == TokenType.YARN:
            # Handle casting to string
            return str(value)
        return value  # Default case, return the value as is

    def execute_arithmetic(self, node: ArithmeticNode) -> Any:
        """Execute arithmetic operation"""
        left = self.execute_node(node.left)
        right = self.execute_node(node.right)
        
        # Handle special values first
        if left == "WIN" or left is True:
            left = 1.0
        elif left == "FAIL" or left is False:
            left = 0.0
            
        if right == "WIN" or right is True:
            right = 1.0
        elif right == "FAIL" or right is False:
            right = 0.0
            
        # Handle string values that could be numeric
        if isinstance(left, str):
            left = left.strip('"')  # Remove quotes
        if isinstance(right, str):
            right = right.strip('"')  # Remove quotes
            
        # Convert to numeric values
        try:
            left = float(left)
            right = float(right)
        except (ValueError, TypeError):
            raise RuntimeError(f"Invalid operands for arithmetic operation: {left}, {right}")
        
        operations = {
            TokenType.SUM_OF: lambda x, y: x + y,
            TokenType.DIFF_OF: lambda x, y: x - y,
            TokenType.PRODUKT_OF: lambda x, y: x * y,
            TokenType.QUOSHUNT_OF: lambda x, y: x / y if y != 0 else float('inf'),
            TokenType.MOD_OF: lambda x, y: x % y if y != 0 else float('inf'),
            TokenType.BIGGR_OF: lambda x, y: max(x, y),
            TokenType.SMALLR_OF: lambda x, y: min(x, y)
        }
        
        if node.operator not in operations:
            raise RuntimeError(f"Unknown arithmetic operator: {node.operator}")
            
        result = operations[node.operator](left, right)
        
        # Convert to integer if result is a whole number
        if result.is_integer():
            return int(result)
        return result


    def execute_comparison(self, node: BooleanNode) -> bool:
        """
        Execute comparison operation based on LOLCODE's comparison patterns:
        BOTH SAEM x AN y  -> x == y
        DIFFRINT x AN y   -> x != y
        Relational operations:
        BOTH SAEM x AN BIGGR OF x AN y  -> x >= y
        BOTH SAEM x AN SMALLR OF x AN y -> x <= y
        DIFFRINT x AN SMALLR OF x AN y  -> x > y
        DIFFRINT x AN BIGGR OF x AN y   -> x < y
        """

        # Evaluate left and right nodes
        left_value = self.execute_node(node.left)
        right_value = self.execute_node(node.right)

        # Handle BIGGR OF and SMALLR OF for relational operations
        if isinstance(node.right, BooleanNode) and node.right.operator in [TokenType.BIGGR_OF, TokenType.SMALLR_OF]:
            # Get the values for comparison
            right_value = self.execute_node(node.right.right)  # Get the second operand

            # Convert to numeric values
            try:
                left_value = float(left_value)
                right_value = float(right_value)
            except (ValueError, TypeError):
                raise RuntimeError(f"Invalid operands for comparison: {left_value}, {right_value}")

            # Handle relational operations
            if node.operator == TokenType.BOTH_SAEM:
                if node.right.operator == TokenType.BIGGR_OF:
                    return left_value >= right_value  # x >= y
                elif node.right.operator == TokenType.SMALLR_OF:
                    return left_value <= right_value  # x <= y
            elif node.operator == TokenType.DIFFRINT:
                if node.right.operator == TokenType.SMALLR_OF:
                    return left_value > right_value   # x > y
                elif node.right.operator == TokenType.BIGGR_OF:
                    return left_value < right_value   # x < y

        # Convert to numeric values for simple comparisons
        try:
            left_value = float(left_value)
            right_value = float(right_value)
        except (ValueError, TypeError):
            raise RuntimeError(f"Invalid operands for comparison: {left_value}, {right_value}")

        # Handle simple equality comparisons
        if node.operator == TokenType.BOTH_SAEM:
            return self.values_equal(left_value, right_value)  # x == y
        elif node.operator == TokenType.DIFFRINT:
            return not self.values_equal(left_value, right_value)  # x != y

        raise RuntimeError(f"Invalid comparison operation: {node.operator}")
    
    def set_console_output(self, output_function):
        """Set the console output function to redirect print statements."""
        self.console_output_function = output_function

    def get_symbol_table(self) -> Dict[str, TokenType]:
        """Return the current symbol table as a dictionary."""
        symbol_table = {}
        for scope in self.current_scope:
            symbol_table.update(scope)
        return symbol_table

    def set_symbol_table_update(self, update_function):
        """Set the function to update the symbol table in the GUI."""
        self.symbol_table_update_function = update_function
