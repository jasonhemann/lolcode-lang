from parser.tokens import *
from parser.variables import *
from parser.operations import *
from parser.input_output import *
from parser.yarn import *
from parser.function import *
from parser.loops import *
from parser.control_flow import *
from parser.typecasting import *

class LOLCodeParser:
    def __init__(self, tokens, gui=None):
        self.tokens = tokens
        self.position = 0
        self.has_hai, self.has_kthxbye, self.has_wazzup, self.o_rly = False, False, False, False
        self.variables = {}
        self.functions = {}
        self.numline = 1
        self.gui = gui
        self.suppress = False

    def current_token(self):
        return current_token(self)
    
    def get_next_token(self):
        return get_next_token(self)
    
    def next_pos(self):
        next_pos(self)

    def count_newline(self):
        count_newline(self)

    def prev_pos(self):
        prev_pos(self)

    def sub_newline(self):
        sub_newline(self)

    def parse_variable_declaration_block(self):
        parse_variable_declaration_block(self)
    
    def parse_variable_declaration(self):
        parse_variable_declaration(self)

    def parse_variable_assignment(self, variable):
        parse_variable_assignment(self, variable)

    def parse_arithmetic(self):
        return parse_arithmetic(self)

    def parse_expression(self):
        return parse_expression(self)
    
    def parse_bool(self):
        return parse_bool(self)
    
    def parse_comparison(self):
        return parse_comparison(self)

    def parse_input_keyword(self):
        parse_input_keyword(self)
    
    def parse_output_keyword(self):
        parse_output_keyword(self)

    def parse_yarn(self):
        return parse_yarn(self)
    
    def parse_smoosh(self, value):
        parse_smoosh(self, value)

    def parse_function(self):
        parse_function(self)
    
    def parse_function_call(self):
        parse_function_call(self)

    def parse_loop(self):
        parse_loop(self)

    def parse_if_else(self):
        parse_if_else(self)

    def parse_mebbe(self):
        parse_mebbe(self)
    
    def parse_switch(self, variable):
        parse_switch(self, variable)

    def parse_typecasting(self, var):
        parse_typecasting(self, var)

    # main parser
    def parse(self):
        # exhausts all tokens in a program
        while self.position < len(self.tokens):
            self.parse_statement()

        return

    # parses each statement
    def parse_statement(self):
        # gets current token
        token = self.current_token()

        # not token
        if not token:
            return False
        
        # checks for new line to increment line number
        # does not work for multiline comments
        if token.type == 'NEWLINE':
            self.count_newline()
            return
        
        # code delimiters
        elif token.type == 'Code Delimiter' and token.value == 'HAI':
            self.next_pos()
            self.has_hai = True
            return
        
        # function
        elif token.type == 'Function Keyword' and token.value == 'HOW IZ I':
            self.next_pos()
            self.parse_function()
            return
        
        # first checks if it has program code delimiter
        elif self.has_hai == False:
            raise SyntaxError("in parse_statement(): Program missing 'HAI' start delimiter")
        
        elif token.type == 'Code Delimiter' and token.value == 'KTHXBYE':
            self.next_pos()
            self.has_kthxbye = True
            return
            
        # variable declaration
        elif token.type == 'Variable Declaration Delimiter' and token.value == 'WAZZUP':
            self.next_pos()
            self.has_wazzup = True
            return self.parse_variable_declaration_block()

        elif self.has_wazzup == False:
            raise SyntaxError("in parse_statement(): Program missing 'WAZZUP' variable declaration delimiter")
            
        # output/print
        elif token.type == 'Output Keyword' and token.value == 'VISIBLE':
            self.next_pos()
            self.parse_output_keyword()
            if self.gui:
                self.gui.update_symbol_table(self.variables, True, self.suppress)
            self.suppress = False
            return
        
        # TODO: input parser from user 
        elif token.type == 'Input Keyword' and token.value == 'GIMMEH':
            self.next_pos()
            self.parse_input_keyword()
            return
        
        # identifier (variable assignment and switch case)
        elif token.type == 'Identifier' and token.value in self.variables:
            self.variables['IT'] = self.current_token()
            variable = self.current_token()
            keyword = self.get_next_token()
            if keyword and (keyword.type == 'Assignment Operation Keyword' or keyword.type == 'Typecasting Keyword'):
                self.parse_variable_assignment(variable) #parse assignment
            elif keyword and keyword.type == 'Switch Statement Keyword' and keyword.value == 'WTF?':
                self.parse_switch(variable)
            else:
                raise SyntaxError(f"{self.numline}: in parse_statement(): Expected valid keyword (R or WTF); Got {keyword.value}")
            return
        
        # function call
        elif token.type == 'Function Call Keyword' and token.value == 'I IZ':
            self.next_pos()
            self.parse_function_call()
            return
        
        # loops
        elif token.type == 'Loop Keyword' and token.value == 'IM IN YR':
            self.next_pos()
            self.parse_loop()
            return
        
        # expression
        elif token.type in ['Arithmetic Operation', 'Bool Operation', 'Comparison Operation']:
            self.parse_expression()
            return
        
        # if-else
        elif token.type == 'If-Then Statement Keyword' and token.value == 'O RLY?':
            self.next_pos()
            self.parse_if_else()
            return
        
        elif not self.has_kthxbye and self.position == len(self.tokens):
            raise SyntaxError("in parse_statement(): Program missing 'KTHXBYE' end delimiter")

        else: raise SyntaxError(f"{self.numline}: in parse_statement(): Unexpected token: {token}")
