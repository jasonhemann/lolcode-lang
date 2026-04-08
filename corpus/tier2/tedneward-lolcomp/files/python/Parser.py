import sys
from antlr4 import *
from lolcode.lolcodeLexer import lolcodeLexer
from lolcode.lolcodeParser import lolcodeParser
from lolcode.lolcodeVisitor import lolcodeVisitor
from AST import *

class Parser(lolcodeVisitor):
    """Parses LOLCODE into our custom AST"""
    
    def visitProgram(self, ctx: lolcodeParser.ProgramContext) -> Program:
        """Convert the program node into our AST Program node"""
        version = None
        if ctx.opening() and ctx.opening().version():
            version = ctx.opening().version().getText()
            
        body = []
        if ctx.code_block():
            statements = self.visit(ctx.code_block())
            if isinstance(statements, list):
                body.extend(statements)
            else:
                body.append(statements)
                
        return Program(version=version, body=body)

    def visitCode_block(self, ctx: lolcodeParser.Code_blockContext) -> List[Statement]:
        """Convert a code block into a list of statements"""
        statements = []
        for stmt in ctx.statement():
            result = self.visit(stmt)
            if result is not None:  # Skip comments and empty statements
                statements.append(result)
        return statements

    def visitDeclaration(self, ctx: lolcodeParser.DeclarationContext) -> Declaration:
        """Convert a variable declaration"""
        name = ctx.LABEL().getText()
        initial_value = None
        if ctx.expression():  # If there is an expression
            initial_value = self.visit(ctx.expression())
        return Declaration(name=name, initial_value=initial_value)

    def visitPrint_block(self, ctx: lolcodeParser.Print_blockContext) -> PrintStatement:
        """Convert a print statement"""
        # In VISIBLE statements, any standalone LABEL is a variable reference
        expressions = []
        for expr in ctx.expression():
            expressions.append(self.visit(expr))
        return PrintStatement(expressions=expressions)

    def visitInput_block(self, ctx: lolcodeParser.Input_blockContext) -> InputStatement:
        """Convert an input statement"""
        return InputStatement(name=ctx.LABEL().getText())

    def visitAssignment(self, ctx: lolcodeParser.AssignmentContext) -> Assignment:
        """Convert an assignment statement"""
        name = ctx.LABEL().getText()
        value = self.visit(ctx.expression())
        return Assignment(name=name, value=value)

    def visitLoop(self, ctx: lolcodeParser.LoopContext) -> LoopStatement:
        """Convert a loop statement"""
        label = ctx.LABEL(0).getText()
        condition = self.visit(ctx.expression())
        body = self.visit(ctx.code_block())
        return LoopStatement(label=label, condition=condition, body=body)

    def visitIf_block(self, ctx: lolcodeParser.If_blockContext) -> IfStatement:
        """Convert an if statement"""
        condition = self.visit(ctx.expression())
        then_branch = self.visit(ctx.code_block(0))
        else_branch = None
        if len(ctx.code_block()) > 1:
            else_branch = self.visit(ctx.code_block(1))
        return IfStatement(condition=condition, then_branch=then_branch, else_branch=else_branch)

    def visitFunc_decl(self, ctx: lolcodeParser.Func_declContext) -> FunctionDecl:
        """Convert a function declaration"""
        name = ctx.name.text
        parameters = []
        # Get all LABEL tokens after the first one (which is the function name)
        for label in ctx.LABEL()[1:]:
            parameters.append(label.getText())
        body = self.visit(ctx.code_block())
        return FunctionDecl(name=name, parameters=parameters, body=body)

    def visitExpression(self, ctx: lolcodeParser.ExpressionContext) -> Expression:
        """Convert an expression"""
        # Handle each type of expression
        if ctx.maths():
            return self.visit(ctx.maths())
        elif ctx.comparison():
            return self.visit(ctx.comparison())
        elif ctx.logical():
            return self.visit(ctx.logical())
        elif ctx.unary_op():
            return self.visit(ctx.unary_op())
        elif ctx.func_call():
            # Only visit func_call if it's actually a function call with MKAY?
            if 'MKAY?' in ctx.getText():
                return self.visit(ctx.func_call())
            else:
                # If it's just a label, treat it as a variable
                return Variable(ctx.func_call().name.text)
        elif ctx.atom:
            # Handle literal values
            value = ctx.ATOM().getText()
            if value == 'WIN':
                return Literal(True)
            elif value == 'FAIL':
                return Literal(False)
            elif value == 'NOOB':
                return Literal(None)
            elif value.startswith('"'):
                return Literal(value.strip('"'))
            elif '.' in value:
                return Literal(float(value))
            else:
                try:
                    return Literal(int(value))
                except ValueError:
                    return Literal(value)
        elif ctx.label:
            # A bare label is always a variable reference
            return Variable(ctx.LABEL().getText())
        else:
            raise ValueError(f"Unhandled expression type: {ctx.getText()}")

    def visitMaths(self, ctx: lolcodeParser.MathsContext) -> MathExpr:
        """Convert a math expression"""
        op_text = ctx.op.text
        op = next(op for op in MathOp if op.value == op_text)
        left = self.visit(ctx.left)
        right = self.visit(ctx.right)
        return MathExpr(op=op, left=left, right=right)

    def visitComparison(self, ctx: lolcodeParser.ComparisonContext) -> ComparisonExpr:
        """Convert a comparison expression"""
        op_text = ctx.op.text
        op = next(op for op in ComparisonOp if op.value == op_text)
        left = self.visit(ctx.left)
        right = self.visit(ctx.right)
        return ComparisonExpr(op=op, left=left, right=right)

    def visitLogical(self, ctx: lolcodeParser.LogicalContext) -> LogicalExpr:
        """Convert a logical expression"""
        op_text = ctx.op.text
        op = next(op for op in LogicalOp if op.value == op_text)
        
        operands = []
        if op in (LogicalOp.ALL, LogicalOp.ANY):
            for expr in ctx.expression():
                operands.append(self.visit(expr))
        else:  # BOTH OF or EITHER OF
            operands = [self.visit(ctx.left), self.visit(ctx.right)]
            
        return LogicalExpr(op=op, operands=operands)

    def visitUnary_op(self, ctx: lolcodeParser.Unary_opContext) -> UnaryExpr:
        """Convert a unary operation"""
        operand = self.visit(ctx.expression())
        return UnaryExpr(op=LogicalOp.NOT, operand=operand)

    def visitFunc_call(self, ctx: lolcodeParser.Func_callContext) -> Expression:
        """Convert a function call"""
        name = ctx.name.text
        arguments = [self.visit(expr) for expr in ctx.expression()]
        return FunctionCall(name=name, arguments=arguments)

    def parse_file(self, file_path: str) -> Program:
        """Compile a LOLCODE file into our AST"""
        input_stream = FileStream(file_path)
        lexer = lolcodeLexer(input_stream)
        tokens = CommonTokenStream(lexer)
        parser = lolcodeParser(tokens)
        tree = parser.program()
        
        return self.visit(tree)

def main():
    if len(sys.argv) < 2:
        print("Usage: python Parser.py <lolcode-file>")
        return

    ast = Parser().parse_file(sys.argv[1])
    print(f"Parsed {sys.argv[1]} into AST:")
    print(ast)

if __name__ == '__main__':
    main()
