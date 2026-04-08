# from syntax_checker import SyntaxChecker
from ast_objects import * 
from itertools import groupby
import re

# =====================================================
# TODO: REMOVE IMPORTS BELOW WHEN SYNTAX CHECKER COMPLETE
# =====================================================
from token_class import TokenClass
from lexer import Lexer
from syntax_checker import SyntaxChecker

'''
This class assumes that the syntax is already checked (from Lexer and Syntax Checker).
The symbol/variable table is already built
'''

class Parser:
    literals = ["NUMBAR", "NUMBR", "YARN", "TROOF", "TYPE"]
    binary_arith_ops = ["SUM OF", "DIFF OF", "PRODUKT OF", "QUOSHUNT OF", "MOD OF", "BIGGR OF", "SMALLR OF"] # returns NUMBR/NUMBAR
    binary_bool_ops = ["BOTH SAEM", "DIFFRINT", "BOTH OF", "EITHER OF", "WON OF"] # returns TROOF
    binary_ops = binary_arith_ops + binary_bool_ops
    nary_bool_ops = ["ALL OF", "ANY OF"] # returns TROOF
    nary_yarn_ops = ["SMOOSH"] # returns YARN
    nary_ops = nary_bool_ops + nary_yarn_ops
    unary_ops = ["NOT"] # return TROOF
    closing_tags = ["BUHBYE", "GTFO", "IM OUTTA YR", "IF U SAY SO", "OIC"] 
    
    functions_label = [] # list of FuncDecl Class
    loops_label = []     # list of LoopDecl Class
    var_table = []       # list of Variable Class   
    
    var_table_dict = {} # THIS IS FROM SYNTAX ANALYZER == SHOULD NOT BE USED ONCE PARSER IS INITIALIZED
    ast = []
    stack = []

    def __init__(self, program):
        # ============================================================
        # TODO: UNCOMMENT WHEN SYNTAX CHECKER IS COMPLETE
        # ============================================================
        # ----- attributes from syntax checker -----
        self.syntax_checker = SyntaxChecker(program)
        self.syntax_errors = self.syntax_checker.check_syntax()
        self.tokens = self.syntax_checker.cleaned_tokens
        self.var_table_dict = self.syntax_checker.var_table
        self.regexes = self.syntax_checker.lexer.regexes

        # ----- attributes of Parser -----
        self.var_table = []         # serves as var_table of Variable Class objects
        self.ast = []               # full AST
        self.stack = []             # for nested nodes
        
       
        # ======================================================
        # TODO: DUMMY DATA (REMOVE WHEN SYNTAX CHECKER IS COMPLETE)
        # ======================================================
        self.regexes = Lexer.regexes
        self.tokens = {
            1: [TokenClass("program delimiter", "HAI", False)],

            # WAZZUP variable declarations
            3: [TokenClass("variable declaration", "WAZZUP", False)],
            4: [TokenClass("variable declaration", "I HAS A", False),
                TokenClass("variable", "name", True)],
            5: [TokenClass("variable declaration", "I HAS A", False),
                TokenClass("variable", "num1", True)],
            6: [TokenClass("variable declaration", "I HAS A", False),
                TokenClass("variable", "num2", True)],
            7: [TokenClass("closing statement", "BUHBYE", False)],

            # HOW IZ I addNum
            9: [TokenClass("function declaration", "HOW IZ I", False),
                TokenClass("variable", "addNum", True),
                TokenClass("variable reference", "YR", False), TokenClass("variable", "x", True),
                TokenClass("conjunction", "AN", False),
                TokenClass("variable reference", "YR", False), TokenClass("variable", "y", True)],
            10: [TokenClass("return statement", "FOUND YR", False),
                TokenClass("arithmetic operation", "SUM OF", False),
                TokenClass("variable", "x", True),
                TokenClass("conjunction", "AN", False),
                TokenClass("variable", "y", True)],
            11: [TokenClass("closing statement", "IF U SAY SO", False)],

            # HOW IZ I printName
            13: [TokenClass("function declaration", "HOW IZ I", False),
                TokenClass("variable", "printName", True),
                TokenClass("variable reference", "YR", False), TokenClass("variable", "person", True)],
            14: [TokenClass("output statement", "VISIBLE", False),
                TokenClass("YARN", '"Hello, "', False),
                TokenClass("output concat", "+", False),
                TokenClass("variable", "person", True)],
            15: [TokenClass("return statement", "GTFO", False)],
            16: [TokenClass("closing statement", "IF U SAY SO", False)],

            # HOW IZ I printNum
            18: [TokenClass("function declaration", "HOW IZ I", False),
                TokenClass("variable", "printNum", True),
                TokenClass("variable reference", "YR", False), TokenClass("variable", "x", True)],
            19: [TokenClass("return statement", "FOUND YR", False),
                TokenClass("variable", "x", True)],
            20: [TokenClass("closing statement", "IF U SAY SO", False)],

            # MAIN PROGRAM
            22: [TokenClass("input statement", "GIMMEH", False),
                TokenClass("variable", "num1", True)],
            23: [TokenClass("input statement", "GIMMEH", False),
                TokenClass("variable", "num2", True)],

            25: [TokenClass("function call", "I IZ", False),
                TokenClass("variable", "addNum", True),
                TokenClass("variable reference", "YR", False),
                TokenClass("variable", "num1", True),
                TokenClass("conjunction", "AN", False),
                TokenClass("variable reference", "YR", False),
                TokenClass("variable", "num2", True)],
            26: [TokenClass("output statement", "VISIBLE", False),
                TokenClass("variable", "IT", True)],

            28: [TokenClass("input statement", "GIMMEH", False),
                TokenClass("variable", "name", True)],
            29: [TokenClass("function call", "I IZ", False),
                TokenClass("variable", "printName", True),
                TokenClass("variable reference", "YR", False),
                TokenClass("variable", "name", True)],
            30: [TokenClass("output statement", "VISIBLE", False),
                TokenClass("variable", "IT", True)],

            32: [TokenClass("function call", "I IZ", False),
                TokenClass("variable", "printNum", True),
                TokenClass("variable reference", "YR", False),
                TokenClass("arithmetic operation", "SUM OF", False),
                TokenClass("variable", "x", True),
                TokenClass("conjunction", "AN", False),
                TokenClass("NUMBR", "2", False)],
            33: [TokenClass("output statement", "VISIBLE", False),
                TokenClass("variable", "IT", True)],

            35: [TokenClass("program delimiter", "KTHXBYE", False)]
        }
        self.var_table_dict = {
            "name": ["NOOB", None],
            "num1": ["NOOB", None],
            "num2": ["NOOB", None],
        }


        # ----- init self.global_var_table -----
        self.global_var_table_init(self.var_table_dict)
    
    # ===========================================================
    #  Variable Table with Variable Class Objects 
    # ===========================================================
    def global_var_table_init(self, var_table_dict):
        for name, type_val in var_table_dict.items():
            type = type_val[0]
            value = type_val[1]

            if type == "expression" and isinstance(value, list):
                node_value = self.parse_expression(value)
                determined_type = self._determine_expression_type(node_value)
                if determined_type:
                    type = determined_type 
                value = node_value
                
            node = Variable(name, type, value)
            self.var_table.append(node)

    # ===========================================================
    #   AST builder function
    # ===========================================================
    
    def build_ast(self):
        if self.syntax_errors:
            print("FATAL: Please resolve errors first.")
            self.syntax_checker._print_err()
            return

        for line_num, tokens_in_line in self.tokens.items():
            if not tokens_in_line:
                continue
            token = tokens_in_line[0].value
            second_token = None
            if len(tokens_in_line) > 1:
                second_token = tokens_in_line[1].value

            if token == "HAI" or token == "KTHXBYE":
                continue

            # ----------- SECOND TOKEN KEYWORD ------------------
            
            # check agad for keyword not in first token
            if second_token and second_token == "R":
                self._parse_assignment(tokens_in_line)
                continue

            if second_token and second_token == "IS NOW A":
                self._parse_recast(tokens_in_line)
                continue

            # ------------------- OPENING -----------------------
            if token == "WAZZUP":
                self._parse_wazzup()
                continue

            if token == "HOW IZ I":
                self._parse_func_dec(tokens_in_line)
                continue

            if token == "IM IN YR":
                self._parse_loops_dec(tokens_in_line)
                continue

            if token == "WTF?":
                var = self.get_var("IT" , self.get_nearest_scope_var_table())
                self._parse_switch(var)
                continue

            if token == "OMG":
                self._parse_switch_case(tokens_in_line)
                continue

            if token == "OMGWTF":
                self._parse_default_case(tokens_in_line)
                continue

            if token == "O RLY?":
                var = self.get_var("IT" , self.get_nearest_scope_var_table())
                self._parse_ifelse(var)
                continue

            if token == "YA RLY":
                self._parse_if_block()
                continue

            if token == "MEBBE":
                condition = tokens_in_line[1:]
                self._parse_mebbe_block(condition)
                continue
            
            if token == "NO WAI":
                self._parse_else_block()
                continue

            # ------------------- CLOSING -----------------------
            if token in self.closing_tags:
                if token == "OIC":
                    if self.stack and isinstance(self.stack[-1], (ElseBlock, IfBlock, MebbeBlock)):
                        node = self.stack.pop()
                    if self.stack and isinstance(self.stack[-1], IfElse):
                        node = self.stack.pop()
                        self._add_node(node)
                        continue
                    if self.stack and isinstance(self.stack[-1], DefaultCase):
                        self.stack.pop()
                    if self.stack and isinstance(self.stack[-1], SwitchCase):
                        node = self.stack.pop()
                        self._add_node(node)
                        continue
                if token == "GTFO" and self.stack and isinstance(self.stack[-1], FunctionDeclaration):
                    self._parse_return_func(tokens_in_line)
                    continue

                node = self._parse_closing() # these blocks have code_block attr
                if token == "IM OUTTA YR": 
                    self.loops_label.append(node.label)
                elif token == "IF U SAY SO":
                    self.functions_label.append(node.label)
                    # return noob
                if token == "GTFO": 
                    if isinstance(node, VariableDeclaration):
                        self.loops_label.append(node.label)
                        # return noob
                    elif isinstance(node, FunctionDeclaration):
                        self.functions_label.append(node.label)
                        # return noob
                continue
            
            # ------------------- CONTROL FLOW STATEMENTS -----------------------
            if token == "I HAS A":
                self._parse_var_dec(tokens_in_line)
                continue

            if token == "I IZ":
                self._parse_function_call(tokens_in_line)
                continue
            
            if token == "MAEK A":
                self._parse_typecast(tokens_in_line)
                continue

            if token == "GIMMEH":
                self._parse_input(tokens_in_line)
                continue

            if token == "VISIBLE":
                self._parse_print(tokens_in_line)
                continue
            
            if token == "FOUND YR":
                self._parse_return_func(tokens_in_line)
                continue
            # ------------------- "IT" UPDATER -----------------------
                
            if token == "SMOOSH":
                node = self._parse_nary(tokens_in_line)
                self._add_node(node)
                continue    
            
            # else, this is an expression/variable/functioncall that is meant to change the value of IT
            declared_vars = [var.name for var in self.get_nearest_scope_var_table()]
            ops = self.binary_ops + self.unary_ops + self.nary_ops
            if token in ops: 
                node = self.parse_expression(tokens_in_line)
            elif token in declared_vars:
                node = self.get_var(token, self.get_nearest_scope_var_table())
            else:
                node = self._parse_atom(token)
            
            # to update IT value
            self._add_node(node)
            continue        

    # ===========================================================
    #   PARSER FUNCTIONS
    # ===========================================================

    # ----------------------- CLOSING TAGS (POP STACK) ----------------------
    def _parse_closing(self):
       
        node = self.stack.pop()
        self._add_node(node)
        return node

    # --------------------- OPENING TAGS (PUSH TO STACK) -----------------------
    def _parse_wazzup(self):
        node = WazzupVariableDeclaration()
        self.stack.append(node)        

    def _parse_func_dec(self, tokens_in_line):
        label = tokens_in_line[1].value
        params_tok = [token for token in tokens_in_line[2:] if token.value != "AN" and token.value != "YR"]
        params_var_obj = [Variable(tok.value, "NOOB", None) for tok in params_tok]
            # duplicate var_table from nearest scope
        dup_var_table = self.get_nearest_scope_var_table()
        
        for tok in params_tok: 
            name = tok.value
            node = Variable(name, "NOOB", None)
            dup_var_table.append(node)

        node = FunctionDeclaration(label, params_var_obj, dup_var_table)
        self.stack.append(node)     
    
    def _parse_return_func(self, tokens_in_line):
        keyword = tokens_in_line[0].value
        if keyword == "FOUND YR":
            # default to return is the it value of the var_table of the function
            if self.stack and isinstance(self.stack[-1], FunctionDeclaration):
                return_node = self.get_var("IT", self.get_nearest_scope_var_table())
                if tokens_in_line[1]:
                    return_node = self.parse_expression(tokens_in_line[1:])
                
                node = FunctionReturn(return_node, self._determine_expression_type(return_node))
                self.stack[-1].return_block = node
        elif keyword == "GTFO":
            return_node = Literal(None,"NOOB")
            node = FunctionReturn(return_node, self._determine_expression_type(return_node))
            self.stack[-1].return_block = node

    def _parse_loops_dec(self, tokens_in_line):
        label = tokens_in_line[1].value         # Loop label
        operation = tokens_in_line[2].value     # UPPIN YR/ NERFIN YR
        var_name = tokens_in_line[3].value      # the loop variable
        loop_type = None
        expression_tokens = []
        expression_node = None

        # find the variable in the table
        variable = self.get_var(var_name, self.get_nearest_scope_var_table())

        # if the loop has a condition like "TIL" or "WILE"
        if len(tokens_in_line) > 4:
            loop_type = tokens_in_line[4].value
            # everything after the loop_type is the expression
            expression_tokens = tokens_in_line[5:]
        if expression_tokens:
            expression_node = self.parse_expression(expression_tokens)
        # duplicate var_table from nearest scope
        dup_var_table = self.get_nearest_scope_var_table()
    
        node = LoopDeclaration(label, operation, variable, loop_type, expression_node, dup_var_table)
        self.stack.append(node)  

    # -------------- SWITCH CASES ---------------

    def _parse_switch(self, condition):
        node = SwitchCase(condition)
        self.stack.append(node)
 
    def _parse_switch_case(self, tokens_in_line):
        value_literal = tokens_in_line[1].value # OMG n
        node = Case(value_literal)

        if self.stack and isinstance(self.stack[-1], SwitchCase):
            self.stack.append(node)

    def _parse_default_case(self, tokens_in_line):
        node = DefaultCase()
    
        if self.stack and isinstance(self.stack[-1], SwitchCase):
            self.stack[-1].default_case_block = node
            self.stack.append(node)

    # -------------- IF ELSE ---------------
    
    def _parse_ifelse(self, condition):
        node = IfElse(condition)
        self.stack.append(node)

    def _parse_if_block(self):
        node = IfBlock()
        if self.stack and isinstance(self.stack[-1], IfElse):
            self.stack[-1].if_block = node
            self.stack.append(node)

    def _parse_else_block(self):
        node = ElseBlock()
        if self.stack and isinstance(self.stack[-1], (IfBlock)) and isinstance(self.stack[-2], (IfElse)): # NO WAI is also a closing tag (indicates MEBBE or YA RLY code_block is finished)
            pop_node = self.stack.pop()
            self.stack[-1].if_block = pop_node
        if self.stack and isinstance(self.stack[-1], MebbeBlock) and isinstance(self.stack[-2], IfElse):
            pop_node = self.stack.pop()
        if self.stack and self.stack[-1].if_block and isinstance(self.stack[-1], IfElse):
            self.stack[-1].else_block = node

        self.stack.append(node)
        return

    def _parse_mebbe_block(self, condition):
        
        if condition:
            condition = self.parse_expression(condition)
            node = MebbeBlock(condition)
        
        if self.stack and isinstance(self.stack[-1], IfBlock) and isinstance(self.stack[-2], IfElse): # MEBBE is also a closing tag (indicates YA RLY or MEBBE code_block is finished)
            pop_node = self.stack.pop()
            self.stack[-1].if_block = pop_node
        if self.stack and isinstance(self.stack[-1], MebbeBlock) and isinstance(self.stack[-2], IfElse):
            pop_node = self.stack.pop()
        if self.stack and isinstance(self.stack[-1], IfElse):
            self.stack[-1].mebbe_blocks.append(node)
        
        self.stack.append(node)

    # --------------------- CONTROL FLOW STATEMENTS -----------------------
    def _parse_var_dec(self, tokens_in_line):
        var_name = tokens_in_line[1].value
        var =  self.get_var(var_name, self.get_nearest_scope_var_table())
        node = VariableDeclaration(var)
        self._add_node(node)
    
    def _parse_function_call(self, tokens_in_line):
        label = tokens_in_line[1].value
        params_tok = [token for token in tokens_in_line[2:] if token.value != "AN" and token.value != "YR"]
        params_name = [tok.value for tok in params_tok]
            # get var_table from nearest scope
        curr_var_table = self.get_nearest_scope_var_table()
        var_params = [self.get_var(param, curr_var_table) for param in params_name]
            
        node = FunctionCall(label, var_params)
        self._add_node(node)

    def _parse_assignment(self, tokens_in_line):
        var_name = tokens_in_line[0].value
        val = tokens_in_line[2:]
        val = self.parse_expression(val)
        var =  self.get_var(var_name , self.get_nearest_scope_var_table())
        
        node = Assignment(var, val)
        self._add_node(node)

    def _parse_typecast(self, tokens_in_line):
        var_name = tokens_in_line[1].value
        type = tokens_in_line[2].value
        var =  self.get_var(var_name , self.get_nearest_scope_var_table())
        
        node = Typecast(var, type)
        self._add_node(node)
        return node

    def _parse_recast(self, tokens_in_line):
        var_name = tokens_in_line[0].value
        type = tokens_in_line[2].value
        var =  self.get_var(var_name , self.get_nearest_scope_var_table())
        
        node = Recast(var, type)
        self._add_node(node)

    def _parse_input(self, tokens_in_line):
        var_name = tokens_in_line[1].value
        var =  self.get_var(var_name , self.get_nearest_scope_var_table())
        node = Input(var)
        self._add_node(node)
    
    # TODO
    def _parse_print(self, tokens_in_line):
        # convert the operands into yarns (+)
        op = tokens_in_line[0].value # "VISIBLE"
        statements = tokens_in_line[1:]

        # either a literal, variable 
        if len(statements) == 1: 
            statement_node = self._parse_atom(tokens_in_line[1])  

        # to be concatenated
        elif "+" in [tok.value for tok in statements]:
            statement_node = self._parse_concat(statements)
        else: 
            statement_node = self.parse_expression(statements)
            
        node = Print(statement_node)
        self._add_node(node)

    # ===========================================================
    #   PARSING EXPRESSIONS 
    # ===========================================================
    # NOTE: input list of TokenClass, returns Node
    def parse_expression(self, tokens):
        
        if not tokens:
            return None

        tok_val = [tok.value for tok in tokens]

        # 1. Check unary
        if tok_val[0] in self.unary_ops:
            return self._parse_unary(tokens)
        # 2. Check binary
        if tok_val[0] in self.binary_ops:
            return self._parse_binary(tokens)
        # 3. Check n-ary
        if tok_val[0] in self.nary_ops:
            return self._parse_nary(tokens)
        if tok_val[0] == "MAEK A":
            return self._parse_typecast(tokens)
        else:
        # 4. Literal or variable (single atom)
            return self._parse_atom(tokens[0])

    # NOTE: input TokenClass, returns Node
    def _parse_atom(self, tok):

        if isinstance(tok, TokenClass):
            value = tok.value
            raw_s = str(value)
            
            if re.match(self.regexes["YARN"], raw_s):
                return Literal(raw_s.strip('"'), "YARN")
            if re.match(self.regexes["NUMBAR"], raw_s):
                return Literal(float(raw_s), "NUMBAR")
            if re.match(self.regexes["NUMBR"], raw_s):
                return Literal(int(raw_s), "NUMBR")
            if raw_s in ["WIN", "FAIL"]:
                return Literal(raw_s, "TROOF")

            # variable fallback: only attempt if raw appears in var_table
            var =  self.get_var(raw_s, self.get_nearest_scope_var_table())
            if var:
                return Variable(var.name, var.type, var.value)
            return "NOOB"

    def _parse_binary(self, tokens):
        op = tokens[0].value
        token_vals = [tok.value for tok in tokens]

        # Find LAST occurrence of "AN"
        try:
            an_index = len(token_vals) - 1 - token_vals[::-1].index("AN")
        except ValueError:
            raise Exception(f"Binary operator '{op}' missing 'AN' separator.")

        # LEFT = everything between operator and last AN
        left_tokens = tokens[1:an_index]
        if not left_tokens:
            raise Exception(f"Binary operator '{op}' missing left operand.")

        left = self.parse_expression(left_tokens)

        # RIGHT = everything after last AN (not just 1 token!)
        right_tokens = tokens[an_index + 1:]
        if not right_tokens:
            raise Exception(f"Binary operator '{op}' missing right operand.")

        # RIGHT is also a full expression, not atom
        right = self.parse_expression(right_tokens)

        # Decide type
        if op in self.binary_arith_ops:
            return ArithOperation(op, left, right)
        elif op in self.binary_bool_ops:
            return BooleanOperation(op, left, right)
        
    def _parse_unary(self, tokens):
        op = tokens[0].value
        operand = self._parse_atom(tokens[1])
        return UnaryOperation(op, operand)
            
    def _parse_nary(self, tokens):
        op = tokens[0].value

        # remove operator itself
        statements = tokens[1:]
        if statements and statements[-1].value == "MKAY":
            statements = statements[:-1]

        # split by "AN"
        operands_groups = [list(g) for k, g in groupby(statements, lambda x: x.value == "AN") if not k]

        # parse each operand group recursively
        parsed_operands = []
        for group in operands_groups:
            if len(group) == 1:
                # single token: atom or variable
                parsed_operands.append(self.parse_expression(group))
            else:
                # multiple tokens: full expression
                parsed_operands.append(self.parse_expression(group))

        # Wrap in the correct N-ary node
        if op in self.nary_yarn_ops:
            return NaryYarnOperation(op, parsed_operands)
        elif op in self.nary_bool_ops:
            return NaryBoolOperation(op, parsed_operands)

    # ===========================================================
    #   Helper functions
    # ===========================================================
    
    # ----------- print stack -----------------------------
    # debug only
    def _debug_stack(self):
        print("STACK:", [type(n).__name__ for n in self.stack])


    # ------------- separated by "+" in visible ------------------------
    def _parse_concat(self, tokens_in_line):
        # Group tokens by "+" separator
        elements = [list(g) for k, g in groupby(tokens_in_line, lambda x: x.value == "+") if not k]
        
        nodes = []
        for element in elements:
            # always pass a list to parse_expression
            nodes.append(self.parse_expression(element))
        
        # If only one node, return it directly
        if len(nodes) == 1:
            return nodes[0]
        else:
            return NaryYarnOperation("+", nodes)

    # ---------- leaf node value identifying ------------
    def _determine_expression_type(self, node):
        """
        Recursively checks an expression AST node for its resulting type.
        Precedence: NUMBAR > NUMBR (for arithmetic), YARN/TROOF determined by operator.
        """
        if isinstance(node, Literal):
            return node.type

        if isinstance(node, Variable):
            var = self.get_var(node.name, self.get_nearest_scope_var_table())
            if var:
                return var.type
            return "NOOB" 

        # Handle operation nodes
        if isinstance(node, ArithOperation):
            # Arithmetic operations always result in NUMBR or NUMBAR
            left_type = self._determine_expression_type(node.left)
            right_type = self._determine_expression_type(node.right)
            
            # NUMBAR precedence rule: if either is NUMBAR, the result is NUMBAR
            if left_type == "NUMBAR" or right_type == "NUMBAR":
                return "NUMBAR"
            # Otherwise, if they are both numeric (NUMBR), the result is NUMBR
            if left_type == "NUMBR" and right_type == "NUMBR":
                return "NUMBR"
            
            # Fallback for unexpected operand types, usually results in a runtime error/NOOB in LOlCODE
            # For parsing, we'll assume the result type aligns with the expected numeric output.
            return "NUMBR" 

        if isinstance(node, BooleanOperation):
            # Boolean operations always result in TROOF
            return "TROOF" 

        if isinstance(node, UnaryOperation):
            # NOT operation always results in TROOF
            return "TROOF"

        if isinstance(node, NaryYarnOperation):
            # SMOOSH operation always results in YARN
            return "YARN"

        if isinstance(node, NaryBoolOperation):
            # ALL OF / ANY OF operations always result in TROOF
            return "TROOF"
            
        return "NOOB" # Default for uninitialized or complex cases
    
    # ----------- get latest scope of var_table ------------
    def get_nearest_scope_var_table(self):
        """
        Returns the var_table of the nearest (topmost) object in the stack that has
        a 'var_table' attribute. If none exists, returns the global var_table.
        """

        # Look from top of stack downward
        for obj in reversed(self.stack):
            if hasattr(obj, "var_table"):
                return obj.var_table

        # If nothing found, return global scope
        return self.var_table


    # ----------- stack appending ------------
    def _add_node(self, node):                      
        if self.stack:                              # currently in a nested structure
            self.stack[-1].code_block.append(node)
        else:                                       # finished the nested structure
            self.ast.append(node)                   
    
    # ------------- AST printing -------------
    def _print_ast(self):
        for node in self.ast:
            self._print_ast_node(node)

    def _print_ast_node(self, node, indent=""):
        if node is None:
            print(f"{indent}None")
            return

        print(f"{indent}**{node.__class__.__name__}**")
        
        for attr, value in vars(node).items():
            if attr.startswith('_') or attr in ["var_table"]:
                continue
            
            # TokenClass (This should not appear but catcher na lang)
            if isinstance(value, TokenClass):
                print(f"{indent}  {attr}: TokenValue: '{value.value}', TokenType: {value.type}")
                continue

            # List/tuple of children nodes
            if isinstance(value, (list, tuple)):
                print(f"{indent}  {attr}: [")
                for child in value:
                    self._print_ast_node(child, indent + "    ")
                print(f"{indent}  ]")
            
            # Single child AST node
            elif hasattr(value, '__dict__'):
                print(f"{indent}  {attr}:")
                self._print_ast_node(value, indent + "    ")
            
            # Primitives
            else:
                print(f"{indent}  {attr}: {value}")

    # -------------- Lexemes printing -----------
    def print_tokens_dict(self):
        print("=== TOKENS DICTIONARY ===")
        for line_num, tokens_in_line in self.tokens.items():
            print(f"Line {line_num}:")
            if not tokens_in_line:
                print("  <empty>")
                continue
            for token in tokens_in_line:
                print(f"\t{token.value} ({token.type}) -> variable? {token.is_reference}")
        print("=========================")

    # --------------- variable finding -------------- (specify which var_table cause it can vary under diff scopes)
    def get_var(self, name, var_table):
        for var in var_table:
            if var.name == name:
                return var
            
# ===========================================================
#   MAIN : for testing purposes only.
#   DO NOT UNCOMMENT FOR FINAL OUTPUT
# ===========================================================

file = open("test_cases/01_variables.lol")
parser = Parser(file)
# parser.print_tokens_dict()
print("Building AST...")
parser.build_ast()
print("Printing AST...")
parser._print_ast()