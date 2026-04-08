from lexer.lolcode_lexer import *

# ═════════════════════════════════════════════════════════════════════════════════════════════════
# NODES
# ═════════════════════════════════════════════════════════════════════════════════════════════════
class IntegerNode:
  def __init__(self, token):
    self.token = token

  def __repr__(self):
    return f'{self.token[TOKEN_VALUE]}'

class FloatNode:
  def __init__(self, token):
    self.token = token

  def __repr__(self):
    return f'{self.token[TOKEN_VALUE]}'
  
class BooleanNode:
  def __init__(self, token):
    self.token = token

  def __repr__(self):
    return f'{self.token[TOKEN_VALUE]}'
  
class StringNode:
  def __init__(self, token):
    self.token = (str(token[TOKEN_VALUE][1:-1]), token[TOKEN_TAG], token[TOKEN_LINE_NUMBER])

  def __repr__(self):
    return f'"{self.token[TOKEN_VALUE]}"'

class NoobNode:
  def __init__(self, line_number=None):
    self.line_number = line_number

  def __repr__(self):
    return f"NOOB"

class StringConcatNode:
  def __init__(self, operands):
    self.operands = operands

  def __repr__(self):
    return f"StringConcatenation({self.operands})"
  
class ArithmeticBinaryOpNode:
  def __init__(self, left_node, operation, right_node):
    self.operation = operation
    self.left_node = left_node
    self.right_node = right_node

  def __repr__(self):
    return f'{self.operation[TOKEN_VALUE]}({self.left_node}, {self.right_node})'

class BooleanBinaryOpNode:
  def __init__(self, left_node, operation, right_node):
    self.operation = operation
    self.left_node = left_node
    self.right_node = right_node

  def __repr__(self):
    return f'{self.operation[TOKEN_VALUE]}({self.left_node}, {self.right_node})' 

class BooleanUnaryOpNode:
  def __init__(self, operation, operand):
    self.operation = operation
    self.operand = operand

  def __repr__(self):
    return f'{self.operation[TOKEN_VALUE]}({self.operand})'
  
class BooleanTernaryOpNode:
  def __init__(self, operation, boolean_statements):
    self.operation = operation
    self.boolean_statements = boolean_statements

  def __repr__(self):
    return f"{self.operation}({self.boolean_statements})"

class ComparisonOpNode:
  def __init__(self, left_node, operation, right_node):
    self.operation = operation
    self.left_node = left_node
    self.right_node = right_node

  def __repr__(self):
    return f'{self.operation[TOKEN_VALUE]}({self.left_node}, {self.right_node})' 

class VarAccessNode:
  def __init__(self, var_name_token):
    self.var_name_token = var_name_token

  def __repr__(self):
    return f"VarAccess({self.var_name_token[TOKEN_VALUE]})"

class VarDeclarationNode:
  def __init__(self, var_name_token, value_node):
    self.var_name_token = var_name_token
    self.value_node = value_node

  def __repr__(self):
    return f"VarDeclare({self.var_name_token[TOKEN_VALUE]}, {self.value_node})"

class VarAssignmentNode:
  def __init__(self, var_to_access, value_to_assign):
    self.var_to_access = var_to_access
    self.value_to_assign = value_to_assign

  def __repr__(self):
    return f"VarAssign({self.var_to_access[TOKEN_VALUE]}, {self.value_to_assign})"

class StatementListNode:
  def __init__(self, statements):
    self.statements = statements

  def __repr__(self):
    return f"StatementList({self.statements})"

class VarDecListNode:
  def __init__(self, variable_declarations):
    self.variable_declarations = variable_declarations

  def __repr__(self):
    return f"VarDecListNode({self.variable_declarations})"

class PrintNode:
  def __init__(self, operands):
    self.operands = operands
  
  def __repr__(self):
    return f"PrintNode({self.operands})"

class TypecastNode:
  def __init__(self, source_value, desired_type):
    self.source_value = source_value
    self.desired_type = desired_type

  def __repr__(self):
    return f"{self.desired_type}({self.source_value})"

class SwitchCaseNode:
  def __init__(self, cases, cases_statements, default_case_statements):
    self.cases = cases
    self.cases_statements = cases_statements
    self.default_case_statements = default_case_statements

  def __repr__(self):
    return f"SwitchCases({self.cases_statements})"

class IfNode:
  def __init__(self, if_block_statements, else_block_statements):
    self.if_block_statements = if_block_statements
    self.else_block_statements = else_block_statements

  def __repr__(self):
    return f"IfElse({self.if_block_statements}, {self.else_block_statements})"

class LoopNode:
  def __init__(self, label, operation, variable, clause_type, til_wile_expression, body_statements):
    self.label = label
    self.operation = operation
    self.variable = variable
    self.clause_type = clause_type
    self.til_wile_expression = til_wile_expression
    self.body_statements = body_statements

  def __repr__(self):
    return f"Loop({self.label}, {self.operation[TOKEN_VALUE]}, {self.variable}, {self.clause_type}, {self.til_wile_expression}, {self.body_statements})"

class FuncDefNode:
  def __init__(self, function_name, parameters, body_statements):
    self.function_name = function_name
    self.parameters = parameters
    self.body_statements = body_statements

  def __repr__(self):
    return f"FuncDef({self.function_name}, {self.parameters})"

class FuncCallNode:
  def __init__(self, function_name, parameters):
    self.function_name = function_name
    self.parameters = parameters

  def __repr__(self):
    return f"FuncCall({self.function_name}, {self.parameters})"

class InputNode:
  def __init__(self, variable):
    self.variable = variable

  def __repr__(self):
    return f"StoreTo({self.variable})"

class BreakNode:
  def __init__(self, break_token):
    self.break_token = break_token

  def __repr__(self):
    return f"BREAK"

class ProgramNode:
  def __init__(self, sections):
    self.sections = sections

  def __repr__(self):
    return f"ProgramNode({self.sections})"
  