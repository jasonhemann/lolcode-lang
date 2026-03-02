"""
LOLCODE Semantic Analyzer Module
Performs semantic analysis on the AST
"""

class SemanticAnalyzer:
    def __init__(self, ast):
        self.ast = ast
        self.symbol_table = {}
        self.errors = []
        self.it_value = None

    def analyze(self):
        if not self.ast or self.ast.type != 'PROGRAM':
            self.errors.append("Invalid AST: Root node must be a PROGRAM")
            return None
        self.initialize_scope()
        self.analyze_node(self.ast)
        if self.errors:
            for error in self.errors:
                print(f"Semantic Error: {error}")
            return None
        return self.ast

    def initialize_scope(self):
        self.symbol_table = {'IT': {'type': 'NOOB', 'declared': True}}

    def analyze_node(self, node):
        if not node:
            return
        if node.type == 'PROGRAM':
            for child in node.children:
                self.analyze_node(child)
        elif node.type == 'VAR_DECLARATION':
            self.analyze_variable_declaration(node)
        elif node.type == 'VAR_ASSIGNMENT':
            self.analyze_variable_assignment(node)
        elif node.type == 'OUTPUT':
            self.analyze_output(node)
        elif node.type == 'INPUT':
            self.analyze_input(node)
        elif node.type == 'CONDITIONAL':
            self.analyze_conditional(node)
        elif node.type in ['LITERAL', 'VARIABLE']:
            return self.analyze_expression(node)
        elif node.type in ['OP_ADD', 'OP_SUB', 'OP_MUL', 'OP_DIV', 'OP_MOD', 'OP_MAX', 'OP_MIN']:
            return self.analyze_arithmetic_operation(node)
        elif node.type in ['OP_EQUAL', 'OP_NOT_EQUAL']:
            return self.analyze_comparison_operation(node)
        elif node.type in ['OP_AND', 'OP_OR', 'OP_XOR', 'OP_NOT']:
            return self.analyze_logical_operation(node)
        elif node.type in ['TRUE_BRANCH', 'FALSE_BRANCH']:
            for child in node.children:
                self.analyze_node(child)

    def analyze_variable_declaration(self, node):
        var_name = node.value
        if var_name in self.symbol_table:
            self.errors.append(f"Variable '{var_name}' already declared")
            return
        self.symbol_table[var_name] = {'type': 'NOOB', 'declared': True}
        if node.children:
            expr_type = self.analyze_expression(node.children[0])
            self.symbol_table[var_name]['type'] = expr_type

    def analyze_variable_assignment(self, node):
        var_name = node.value
        if var_name not in self.symbol_table:
            self.errors.append(f"Variable '{var_name}' not declared")
            return
        expr_type = self.analyze_expression(node.children[0])
        self.symbol_table[var_name]['type'] = expr_type
        # Set IT variable type
        self.symbol_table['IT']['type'] = expr_type

    def analyze_output(self, node):
        if node.children:
            self.analyze_expression(node.children[0])

    def analyze_input(self, node):
        var_name = node.value
        if var_name not in self.symbol_table:
            self.errors.append(f"Variable '{var_name}' not declared")
            return
        
        self.symbol_table[var_name]['type'] = 'YARN'
        
        self.symbol_table['IT']['type'] = 'YARN'

    def analyze_conditional(self, node):
        
        if 'IT' not in self.symbol_table:
            self.errors.append("IT variable not set before conditional")
        for child in node.children:
            self.analyze_node(child)

    def analyze_expression(self, node):
        if node.type == 'LITERAL':
            if isinstance(node.value, int):
                return 'NUMBR'
            elif isinstance(node.value, float):
                return 'NUMBAR'
            elif isinstance(node.value, bool):
                return 'TROOF'
            elif isinstance(node.value, str):
                
                try:
                    int(node.value)
                    return 'NUMBR'
                except ValueError:
                    try:
                        float(node.value)
                        return 'NUMBAR'
                    except ValueError:
                        return 'YARN'
            else:
                return 'NOOB'
        elif node.type == 'VARIABLE':
            var_name = node.value
            if var_name not in self.symbol_table:
                self.errors.append(f"Variable '{var_name}' not declared")
                return 'NOOB'
            return self.symbol_table[var_name]['type']
        elif node.type in ['OP_ADD', 'OP_SUB', 'OP_MUL', 'OP_DIV', 'OP_MOD', 'OP_MAX', 'OP_MIN']:
            return self.analyze_arithmetic_operation(node)
        elif node.type in ['OP_EQUAL', 'OP_NOT_EQUAL']:
            return self.analyze_comparison_operation(node)
        elif node.type in ['OP_AND', 'OP_OR', 'OP_XOR', 'OP_NOT']:
            return self.analyze_logical_operation(node)
        return 'NOOB'

    def analyze_arithmetic_operation(self, node):
        if len(node.children) != 2:
            self.errors.append(f"Arithmetic operation requires exactly 2 operands")
            return 'NOOB'
        
        left_type = self.analyze_expression(node.children[0])
        right_type = self.analyze_expression(node.children[1])
        
        
        if node.type == 'OP_ADD' and (left_type == 'YARN' or right_type == 'YARN'):    
            if (left_type in ['NUMBR', 'NUMBAR'] or right_type in ['NUMBR', 'NUMBAR']):                
                return 'NUMBR'  
        
        
        if node.type in ['OP_MAX', 'OP_MIN']:           
            if left_type in ['YARN', 'NUMBR', 'NUMBAR'] and right_type in ['YARN', 'NUMBR', 'NUMBAR']:
                return 'NUMBR'  
        
        
        if left_type in ['NUMBR', 'NUMBAR'] and right_type in ['NUMBR', 'NUMBAR']:
            if node.type == 'OP_DIV' or left_type == 'NUMBAR' or right_type == 'NUMBAR':
                return 'NUMBAR'
            return 'NUMBR'
            
        
        if left_type == 'YARN' or right_type == 'YARN':
            return 'NUMBR'
            
        self.errors.append("Arithmetic operation requires numeric operands")
        return 'NOOB'

    def analyze_comparison_operation(self, node):
        if len(node.children) != 2:
            self.errors.append("Comparison operation requires 2 operands")
            return 'NOOB'
        self.analyze_expression(node.children[0])
        self.analyze_expression(node.children[1])
        self.symbol_table['IT']['type'] = 'TROOF'
        return 'TROOF'

    def analyze_logical_operation(self, node):
        expected = 1 if node.type == 'OP_NOT' else 2
        if len(node.children) != expected:
            self.errors.append(f"{node.type} expects {expected} operands")
            return 'NOOB'
        for child in node.children:
            self.analyze_expression(child)
        self.symbol_table['IT']['type'] = 'TROOF'
        return 'TROOF'