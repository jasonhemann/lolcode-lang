import sys
import logging
from AST import *
from Parser import Parser

# Python is already a dynamically-typed interpreter,
# so this is/should-be a pretty easy implementation,
# assuming we fall back to native Python types for
# values.
class Interpreter():

    class Scope:
        def __init__(self):
            self.vars = {}
            self.funcs = {}

    def __init__(self):
        # A stack of scopes for variable/function resolution
        self.scopes = []

        self.log = logging.getLogger("Interpreter")
        self.log.setLevel(logging.DEBUG)
        handler = logging.StreamHandler(sys.stdout)
        #formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        formatter = logging.Formatter('%(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.log.addHandler(handler)

    def log(self, message, level=logging.INFO):
        """Log a message at the specified level"""
        if level == logging.DEBUG:
            self.log.debug(message)
        elif level == logging.INFO:
            self.log.info(message)
        elif level == logging.WARNING:
            self.log.warning(message)
        elif level == logging.ERROR:
            self.log.error(message)
        elif level == logging.CRITICAL:
            self.log.critical(message)

    def push_scope(self):
        """Push a new scope onto the stack"""
        self.scopes.append(self.Scope())

    def pop_scope(self):
        """Pop the top scope off the stack"""
        if self.scopes:
            self.scopes.pop()
        else:
            raise RuntimeError("No scope to pop")

    def current_scope(self):
        """Get the current scope"""
        if not self.scopes:
            raise RuntimeError("No scope in scope; this is probably a bug!")
        return self.scopes[-1]

    def run(self, program: Program):
        """Run the given program"""
        self.push_scope()
        if program.version:
            print(f"LOLCODE v {program.version}")
        for statement in program.body:
            self.statement(statement)
        self.pop_scope()

    def statement(self, stmt: Statement):
        """Execute a statement"""
        if isinstance(stmt, Expression):
            # Expressions are evaluated in the context of the current scope
            self.evaluate_expression(stmt)
        elif isinstance(stmt, Declaration):
            self.declaration(stmt)
        elif isinstance(stmt, Assignment):
            self.assignment(stmt)
        elif isinstance(stmt, PrintStatement):
            self.print_statement(stmt)
        elif isinstance(stmt, InputStatement):
            self.input_statement(stmt)
        elif isinstance(stmt, IfStatement):
            self.if_statement(stmt)
        elif isinstance(stmt, LoopStatement):
            self.loop_statement(stmt)
        elif isinstance(stmt, FunctionDecl):
            self.function_declaration(stmt)
        else:
            raise RuntimeError(f"Unknown statement type: {type(stmt)}")

    def declaration(self, decl: Declaration):
        """Handle variable declaration"""
        name = decl.name
        if name in self.current_scope().vars:
            raise RuntimeError(f"Variable '{name}' already declared")
        value = None
        if decl.initial_value:
            value = self.evaluate_expression(decl.initial_value)
        self.current_scope().vars[name] = value

    def assignment(self, assign: Assignment):
        """Handle variable assignment"""
        name = assign.name
        if name not in self.current_scope().vars:
            raise RuntimeError(f"Variable '{name}' not declared")
        value = self.evaluate_expression(assign.value)
        self.current_scope().vars[name] = value

    def print_statement(self, print_stmt: PrintStatement):
        """Handle print statement"""
        for expr in print_stmt.expressions:
            value = self.evaluate_expression(expr)
            print(value, end=' ')
        print()

    def input_statement(self, input_stmt: InputStatement):
        """Handle input statement"""
        name = input_stmt.name
        if name not in self.current_scope().vars:
            raise RuntimeError(f"Variable '{name}' not declared")
        value = input(f"Input for {name}: ")
        self.current_scope().vars[name] = value
    
    def if_statement(self, if_stmt: IfStatement):
        """Handle if statement"""
        condition = self.evaluate_expression(if_stmt.condition)
        if condition:
            for stmt in if_stmt.then_branch:
                self.statement(stmt)
        elif if_stmt.else_branch:
            for stmt in if_stmt.else_branch:
                self.statement(stmt)

    def loop_statement(self, loop_stmt: LoopStatement):
        """Handle loop statement"""
        while self.evaluate_expression(loop_stmt.condition):
            for stmt in loop_stmt.body:
                self.statement(stmt)

    def function_declaration(self, func_decl: FunctionDecl):
        """Handle function declaration"""
        name = func_decl.name
        if name in self.current_scope().funcs:
            raise RuntimeError(f"Function '{name}' already declared")
        self.current_scope().funcs[name] = func_decl
        # Register the function in the current scope
        self.current_scope().vars[name] = func_decl 
        # Note: Function bodies are not executed here, they are called later

    def function_call(self, func_name: str, args: List[Expression]):    
        """Call a function with the given name and arguments"""
        if func_name not in self.current_scope().funcs:
            raise RuntimeError(f"Function '{func_name}' not declared")
        func = self.current_scope().funcs[func_name]
        if len(func.parameters) != len(args):
            raise RuntimeError(f"Function '{func_name}' expects {len(func.parameters)} arguments, got {len(args)}")
        
        # Create a new scope for the function call
        self.push_scope()
        for param, arg in zip(func.parameters, args):
            value = self.evaluate_expression(arg)
            self.current_scope().vars[param] = value
        
        # Execute the function body
        for stmt in func.body:
            self.statement(stmt)
        
        # Pop the function scope
        self.pop_scope()

    def evaluate_expression(self, expr: 'Expression'):
        """Evaluate an expression"""
        if isinstance(expr, Variable):
            if expr.name not in self.current_scope().vars:
                raise RuntimeError(f"Variable '{expr.name}' not declared")
            return self.current_scope().vars[expr.name]
        elif isinstance(expr, Literal):
            return expr.value
        elif isinstance(expr, MathExpr):
            left = self.evaluate_expression(expr.left)
            right = self.evaluate_expression(expr.right)
            return self.evaluate_math_op(left, right, expr.op)
        elif isinstance(expr, ComparisonExpr):
            left = self.evaluate_expression(expr.left)
            right = self.evaluate_expression(expr.right)
            if expr.op == ComparisonOp.EQUAL:
                return left == right
            elif expr.op == ComparisonOp.DIFFERENT:
                return left != right
            elif expr.op == ComparisonOp.GREATER:
                return left > right
            elif expr.op == ComparisonOp.SMALLER:
                return left < right
            else:
                raise RuntimeError(f"Unknown comparison operation: {expr.op}")
        elif isinstance(expr, LogicalExpr):
            results = [self.evaluate_expression(op) for op in expr.operands]
            if expr.op == LogicalOp.AND:
                return all(results)
            elif expr.op == LogicalOp.OR:
                return any(results)
            elif expr.op == LogicalOp.NOT:
                return not results[0]
        elif isinstance(expr, UnaryExpr):
            operand = self.evaluate_expression(expr.operand)
            if expr.op == LogicalOp.NOT:
                return not operand
            else:
                raise RuntimeError(f"Unknown unary operation: {expr.op}")
        # Handle function calls
        elif isinstance(expr, FunctionCall):
            # Check if this is actually a variable reference first
            if not expr.arguments and expr.name in self.current_scope().vars:
                return self.current_scope().vars[expr.name]
            # Otherwise treat it as a function call
            if expr.name not in self.current_scope().funcs:
                raise RuntimeError(f"Function '{expr.name}' not declared")
            func = self.current_scope().funcs[expr.name]
            args = [self.evaluate_expression(arg) for arg in expr.arguments]
            return self.call_function(func, args)
        else:
            raise RuntimeError(f"Unknown expression type: {type(expr)}")

    def evaluate_math_op(self, left, right, op):
        """Evaluate a math operation"""
        if op == MathOp.ADD:
            return left + right
        elif op == MathOp.SUB:
            return left - right
        elif op == MathOp.MUL:
            return left * right
        elif op == MathOp.DIV:
            return left / right
        elif op == MathOp.MOD:
            return left / right
        else:
            raise RuntimeError(f"Unknown math operation: {op}")

def main(argv):
    print("Parsing....")
    ast = Parser().parse_file(sys.argv[1])
    print(ast)

    print("Interpreting....")
    interp = Interpreter()
    interp.run(ast)
    print("Exiting....")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Specify an incoming file to interpret!")
        sys.exit(1)

    main(sys.argv)

