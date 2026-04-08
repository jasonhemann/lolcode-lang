# ===================================================
# LEAF NODES
# ===================================================
# Tokens with type "NUMBAR", "NUMBR", "YARN", "TROOF"
class Literal:
    def __init__(self, value, type):
        self.value = value
        self.type = type

    def __repr__(self):
        return f"{self.value} ({self.type})"

# Variable Tokens (declared)
class Variable:
    def __init__(self, name, type, value):               
        self.name = name  
        self.type = type                  
        self.value = value                

    def __repr__(self):
        return f"{self.name}={self.value} ({self.type})"

# Data Types
class Type: 
    def __init__(self, name):               
        self.name = name                    
        self.value = "noob"                

    def __repr__(self):
        return f"{self.name} ({self.value})"
    
# ===================================================
# CONTROL FLOW CONTROL FLOW STATEMENTS (KEYWORDS)
# ===================================================

class WazzupVariableDeclaration:
    def __init__(self):
        self.code_block = []        # VariableDeclaration Class
    
    def __repr__(self):
        return f"WAZZUP\n{self.code_block}\nBUHBYE"


class VariableDeclaration:
    def __init__(self, var): 
        self.var = var              # Variable Class            

    def __repr__(self):
        if self.var.value:
            return f"I HAS A {self.var.name} ITZ {self.var.value} ({self.var.type})"
        return f"I HAS A {self.var.name}"

class FunctionDeclaration:
    def __init__(self, label, params, var_table):
        self.label = label                
        self.params = params        # List of Token Objects 
        self.var_table = var_table     
        self.code_block = []        # CONTROL FLOW STATEMENTS   
        self.return_block = None    # FunctionReturn Class 

    def __repr__(self):
        if self.return_block:
            return f"HOW IZ I {self.label} YR {' AN YR '.join(self.params) if self.params else ''}\n{self.return_block}"
        return f"HOW IZ I {self.label} YR {' AN YR '.join(self.params) if self.params else ''}" 

class FunctionCall:
    def __init__(self, label, params):
        self.label = label               
        self.params = params               

    def __repr__(self):
        return f"I IZ {self.label} YR {' AN YR '.join([str(param) for param in self.params]) if self.params else ''} MKAY"

class FunctionReturn:
    def __init__(self, value, type):
        self.value = value      # Node
        self.type = type        

    def __repr__(self):
        return f"FOUND YR {self.value}"
    
class IfElse:
    def __init__(self, condition):
        self.condition = condition       # Variable "IT" object
        self.if_block = None        # IfBlock Class
        self.mebbe_blocks = []      # MebbeBlock Class
        self.else_block = None      # ElseBlock Class

    def __repr__(self):
        if self.else_block and self.if_block and self.mebbe_blocks:
            return f"O RLY?\n{self.if_block}\n{self.mebbe_blocks}\n{self.else_block}\nOIC"
        elif self.else_block and self.if_block: 
            return f"O RLY?\n{self.if_block}\n{self.else_block}\nOIC"
        elif self.if_block:
            return f"O RLY?\n{self.if_block}\nOIC"
        return f"O RLY?\n{self.else_block}\nOIC"
    
class IfBlock:
    def __init__(self):
        self.code_block = []        # CONTROL FLOW STATEMENTS
    
    def __repr__(self):
        return f"YA RLY\n{self.code_block}"
    
class ElseBlock:
    def __init__(self):
        self.code_block = []        # CONTROL FLOW STATEMENTS
    
    def __repr__(self):
        return f"NO WAI\n{self.code_block}"
    
class MebbeBlock: 
    def __init__(self, condition):
        self.condition = condition
        self.code_block = []       # CONTROL FLOW STATEMENTS

    def __repr__(self):
        return f"MEBBE {self.condition}\n{self.code_block}"

class SwitchCase:
    def __init__(self, condition):
        self.condition = None
        self.code_block = []                # Case Class
        self.default_case_block = None      # DefaultCase Class

    def __repr__(self):
        if self.default_case_block:
            return f"WTF?\n{self.code_block}\n{self.default_case_block}\nOIC"
        return f"WTF?\n{self.code_block}\nOIC"

class Case:
    def __init__(self, value):
        self.value = value          # Literal Node
        self.code_block = []        # CONTROL FLOW STATEMENTS

    def __repr__(self):
        return f"OMG {self.value}\n{self.code_block}\n"
    
class DefaultCase:
    def __init__(self):
        self.code_block = []        # CONTROL FLOW STATEMENTS

    def __repr__(self):
        return f"OMGWTF\n{self.code_block}"
    
class LoopDeclaration:
    def __init__(self, label, operation, variable, loop_type, expression, var_table):
        self.label = label
        self.operation = operation      
        self.variable = variable        # Variable Node
        self.loop_type = loop_type     
        self.expression = expression    # Node
        self.var_table = var_table   
        self.code_block = []            # CONTROL FLOW STATEMENTS             

    def __repr__(self): 
        if self.loop_type and self.expression: 
            return f"IM IN YR {self.label} {self.operation} YR {self.variable} {self.loop_type} {self.expression}\n{self.code_block}\n{self.exit_block}"
        return f"IM IN YR {self.label} {self.operation} YR {self.variable}\n{self.code_block}\n{self.exit_block}"

class ExitLoop:
    def __init__(self, label):
        self.label = label

    def __repr__(self):
        return f"IM OUTTA YR {self.label}"

class Print:
    def __init__(self, value):
        self.value = value           # Node

    def __repr__(self):
        return f"VISIBLE {self.value}"
    
class Input:
    def __init__(self, storage):
        self.storage = storage

    def __repr__(self):
        return f"GIMMEH {self.storage}"

class Assignment:
    def __init__(self, var, value):
        self.var = var          # variable class   
        self.value = value      # Node         

    def __repr__(self):
        return f"{self.var} R {self.value}"

class Typecast:
    def __init__(self, var, type):
        self.var = var              
        self.type = type  

    def __repr__(self):
        return f"MAEK {self.var.value} A {self.type}"

class Recast:
    def __init__(self, var, type):
        self.var = var        # Variable Class obj        
        self.type = type  

    def __repr__(self):
        return f"{self.var.value} IS NOW A {self.type}"

class Break:
    def __init__(self, label):
        self.label = label          # LoopDeclaration Class, FunctionDeclaration Class

    def __repr__(self):
        return "GTFO"
    


# ===================================================
# EXPRESSIONS
# ===================================================

class BooleanOperation:
    def __init__(self, operation, left, right):
        self.operation = operation
        self.left = left
        self.right = right
        self.value = None       # Node

    def __repr__(self):
        return f"{self.operation} {self.left} AN {self.right}"
    
class ArithOperation:
    def __init__(self, operation, left, right):
        self.operation = operation
        self.left = left
        self.right = right
        self.value = None        # Node

    def __repr__(self):
        return f"{self.operation} {self.left} AN {self.right}"

class UnaryOperation:
    def __init__(self, operation, operand):
        self.operation = operation
        self.operand = operand
        self.value = None           # Node

    def __repr__(self):
        return f"{self.operation} {self.operand}"


class NaryYarnOperation:
    def __init__(self, operation, operands):
        self.operation = operation
        self.operands = operands        # List of Literal/ Variable/ Boolean.. Operations Objects
        self.value = None               # Node    

    def __repr__(self):
        return f"{self.operation} {self.operands} (MKAY)"

class NaryBoolOperation:
    def __init__(self, operation, operands):
        self.operation = operation
        self.operands = operands  
        self.value = None               # Node

    def __repr__(self):
        return f"{self.operation} {self.operands} MKAY"

__all__ = [
    "Literal", "Variable", "Type", "WazzupVariableDeclaration", "VariableDeclaration",
    "FunctionDeclaration", "FunctionCall", "FunctionReturn", "IfElse", "IfBlock",
    "ElseBlock", "MebbeBlock", "SwitchCase", "Case", "DefaultCase",
    "LoopDeclaration", "ExitLoop", "Print", "Input", "Assignment",
    "Typecast", "Recast", "Break", "BooleanOperation", "ArithOperation",
    "UnaryOperation", "NaryYarnOperation", "NaryBoolOperation"
]