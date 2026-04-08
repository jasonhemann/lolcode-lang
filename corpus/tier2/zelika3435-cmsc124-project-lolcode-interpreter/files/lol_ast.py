# Base node class
class ASTNode:
	pass

class Program(ASTNode):
	def __init__(self, declarations, statements):
		self.declarations = declarations # List of variable declaration nodes
		self.statements = statements # List of statement nodes

class VarDecl(ASTNode):
	def __init__(self, var_name, expr=None):
		self.var_name = var_name
		self.expr = expr  # Initial value (optional)

class Assignment(ASTNode):
	def __init__(self, var_name, expr):
		self.var_name = var_name
		self.expr = expr

class Visible(ASTNode):
	def __init__(self, exprs):
		self.exprs = exprs

class BinOp(ASTNode):
	def __init__(self, op, left, right):
		self.op = op      # e.g., 'SUM OF'
		self.left = left  # Left operand (expression node)
		self.right = right # Right operand (expression node)

class Literal(ASTNode):
	def __init__(self, value, type):
		self.value = value
		self.type = type
		
class Variable(ASTNode):
	def __init__(self, name):
		self.name = name

class Smoosh(ASTNode):
	def __init__(self, exprs):
		self.exprs = exprs

class Gimmeh(ASTNode):
	def __init__(self, var_name):
		self.var_name = var_name

class Maek(ASTNode):
	def __init__(self, expr, target_type):
		self.expr = expr
		self.target_type = target_type

class IsNowA(ASTNode):
	def __init__(self, var_name, target_type):
		self.var_name = var_name
		self.target_type = target_type

class UnaryOp(ASTNode):
	def __init__(self, op, expr):
		self.op = op
		self.expr = expr

class AllOf(ASTNode):
	def __init__(self, exprs):
		self.exprs = exprs

class AnyOf(ASTNode):
	def __init__(self, exprs):
		self.exprs = exprs

class IfStatement(ASTNode):
	def __init__(self, true_statements, elif_blocks, false_statements):
		self.true_statements = true_statements
		self.elif_blocks = elif_blocks
		self.false_statements = false_statements

class SwitchStatement(ASTNode):
	def __init__(self, cases, default_statements):
		self.cases = cases
		self.default_statements = default_statements

class Case(ASTNode):
	def __init__(self, value, statements):
		self.value = value
		self.statements = statements
		
class GTFO(ASTNode):
	pass

class Loop(ASTNode):
	def __init__(self, label, op, var, cond_type, cond_expr, statements):
		self.label = label
		self.op = op
		self.var = var
		self.cond_type = cond_type
		self.cond_expr = cond_expr
		self.statements = statements

class FunctionDef(ASTNode):
	def __init__(self, name, params, body):
		self.name = name
		self.params = params
		self.body = body

class FunctionCall(ASTNode):
	def __init__(self, name, args):
		self.name = name
		self.args = args

class Return(ASTNode):
	def __init__(self, expr):
		self.expr = expr