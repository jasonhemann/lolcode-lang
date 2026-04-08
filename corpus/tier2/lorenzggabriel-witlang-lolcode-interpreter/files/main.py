import regex as re  # for regular expression parsing in lexemes
import sys
import math
import tkinter as tk  # for creating GUI interface
from tkinter import font, ttk, filedialog, simpledialog
# from lexer import lexical_analyzer, parse

import lexer

# -------------------------------------------[  LEXER ]-----------------------------------------------------------
lines = [] # contains strings per line of code

# Lexical Analyzer Function  
def lexical_analyzer(contents):
    tokens = lexer.lexical_analyzer(contents)
    return tokens

# Parse the function for terminal
def parse_terminal(file):
    contents = open(file, 'r').read()
    contents.replace('\t', '    ') # Change the tabs to 4 spaces
    contents = re.sub(r"(?<!O)BTW.*?(?=\n)", "", contents) # Remove the comments by deleting BTW and contents after it before the new line
    tokens = lexical_analyzer(contents)
    return tokens

# Parse the function for the GUI
def parse_tkinter(code):
    print(repr(code)) # Printable representation of contents
    code = re.sub(r"(?<!O)BTW.*?(?=\n)", "", code) # Remove the comments by deleting BTW and contents after it before the new line
    tokens = lexical_analyzer(code)
    return tokens

# -------------------------------------------[  PARSER ]--------------------------------------------------------
expression_tokens = ["Add Keyword", 
                    "Subtract Keyword", 
                    "Multiply Keyword", 
                    "Divide Keyword", 
                    "Modulo Keyword",
                    "Typecast Keyword",
                    "Return Larger Number Keyword", 
                    "Return Smaller Number Keyword", 
                    "Both True Check Keyword", 
                    "One or Both True Check Keyword", 
                    "Exactly One is True Check Keyword", 
                    "Negate Keyword", 
                    "Atleast One True Check Keyword", 
                    "All True Check Keyword",
                    "Both Argument Equal Check Keyword", 
                    "Both Argument Not Equal Check Keyword",
                    "Concatenation Keyword"
                    ]

arith_tokens = ["Add Keyword", 
                "Subtract Keyword", 
                "Multiply Keyword", 
                "Divide Keyword", 
                "Modulo Keyword", 
                "Return Larger Number Keyword", 
                "Return Smaller Number Keyword"]

bool_tokens =  ["Both True Check Keyword", 
                "One or Both True Check Keyword", 
                "Exactly One is True Check Keyword", 
                "Negate Keyword", 
                "Atleast One True Check Keyword", 
                "All True Check Keyword"]

comp_tokens =  ["Both Argument Equal Check Keyword", 
                "Both Argument Not Equal Check Keyword"]

flow_control_tokens = ["Explicit Start Loop Keyword",
                       "if Keyword",
                       "Switch Keyword"]

class Variable:
    def __init__(self, name, value, valuetype_ = None):
        self.name = name
        self.value = value
        self.valuetype = valuetype_

    def __repr__(self) -> str:
        return f"({self.type}, \"{self.value}\", {self.valuetype})"

variables = {'IT': None}
var_assign_ongoing = False # checker for expressions if to be placed in IT

active_loops = {}
tokens = []
token_idx = -1
current_token = None
current_line = 1
errorMessage = ""

    
def advance():
    global token_idx, current_token
    if token_idx < len(tokens): # trying to fix index out of range error (added minus 1)
        token_idx += 1
        if token_idx < len(tokens):
            current_token = tokens[token_idx]
        else:
            insert_output(f"[Syntax Error] End of file reached with incorrect syntax at line {current_line}")

def restore(saved_token_idx, saved_curr_line):
    global token_idx, current_token, current_line
    token_idx = saved_token_idx
    current_token = tokens[token_idx]
    current_line = saved_curr_line

class Error(Exception):
    def __init__(self, message=None):
        self.message = message
        super().__init__(message)
        
def error(msg, line):
    global errorMessage
    # use Error class
    code = get_line(line)
    errorMessage = f"{msg} \n{code}  :  Line {line}"
    insert_output(errorMessage)

    raise SyntaxError(errorMessage)

def skip_empty_lines():
    global current_token, current_line
    while current_token.tokentype == "Empty Line":
        advance() # skip empty lines
        current_line += 1

def if_linebreak():
    global current_token, current_line
    if current_token.tokentype == "Linebreak":
        current_line += 1
        advance()
        skip_empty_lines()
    else:
        insert_output(f"[Syntax Error] Linebreak expected after token: {tokens[token_idx-1].tokenvalue} at {current_line}")
        
def program():
    global current_token, current_line
    nodes = []
    update_symbol_table()
    skip_empty_lines()

    if current_token.tokentype == "Invalid":
        insert_output(f"[Syntax Error] Invalid token encountered at {current_token.tokenvalue}")

    # check for function definitions outside hai
    if current_token.tokentype == "Define Function Keyword":
        while current_token.tokentype == "Define Function Keyword":
            check_function_def()
            if_linebreak()
    if current_token.tokentype == "Start Code Delimiter":
        nodes.append(("START",current_token))
        advance()
        if_linebreak()
        
        if current_token.tokentype =="Define Function Keyword":
            while current_token.tokentype == "Define Function Keyword":
                check_function_def()
                if_linebreak() # pass linebreak
        
        # VARIABLE DECLARATION
        if current_token.tokentype == "Start Var Declaration Delimiter": # WAZZUP
            # can only be at the start of the code
            
            advance() # pass wazzup
            if_linebreak()
            varDeclarationList = var_declaration_list()
            nodes.append(("VAR_DEC_LIST",varDeclarationList))
            if current_token.tokentype == "End Var Declaration Delimiter":
                advance() # pass BUHBYE
                if_linebreak()
            else:
                insert_output(f"[Syntax Error] End variable declaration delimiter (BUHBYE) not found at {current_line}")
        # else: # remove so that it is optional only
            #error("[SyntaxError] Start variable declaration delimiter (WAZZUP) not found", current_line)
        
        # STATEMENTS_LIST
        statementList = statement_list()
        nodes.append(("STAT_LIST", statementList))
        if current_token.tokentype == "End Code Delimiter":
            nodes.append(("END",current_token))
            advance() # pass KTHXBYE
        else:
            insert_output(f"[Syntax Error] End code delimiter (KTHXBYE) not found at {current_line}")
    else: 
        insert_output(f"[Syntax Error] Start code delimiter (HAI) not found at {current_line}")

    return nodes

def var_declaration_list(): 
    global current_token, current_line
    nodes = []
    while current_token.tokentype != "End Var Declaration Delimiter":
        node = var_declaration()
        update_symbol_table() # update symbol table
        if node is not None:
            nodes.append(node)
        if_linebreak()
    return nodes

def var_declaration():
    global current_token, current_line, var_assign_ongoing
    var_assign_ongoing = True # assignment ongoing
    if current_token.tokentype == "Variable Declaration": # I HAS A
        advance() # pass I HAS A
        if current_token.tokentype == "Variable Identifier": # var
            varident = current_token.tokenvalue
            advance() # pass var
            if current_token.tokentype == "Variable Assignment":
                advance() # pass ITZ
                if current_token.tokentype == "Variable Identifier":
                    # if not yet in variables then throw error
                    if current_token.tokenvalue not in variables:
                        insert_output(f"[Syntax Error] Variable {current_token.tokenvalue} not yet declared at line {current_line}")
                    # else, get the value of the variable and assign it to the new variable
                    variables[varident] = variables[current_token.tokenvalue]
                    node = ("VARIABLE", varident, current_token)
                    advance()
                    var_assign_ongoing = False # set back to false
                    return node
                elif current_token.tokentype in expression_tokens:
                    ans = expression()
                    ans = check_if_bool_var(ans)
                    variables[varident] = ans
                    node = ("VARIABLE", varident, ans)
                    var_assign_ongoing = False # set back to false
                    return node
                else: 
                    lit_value = literal() 
                    variables[varident] = lit_value
                    var_assign_ongoing = False # set back to false
                    return ("VARIABLE", varident, lit_value)      
                # [] to add expressions (arith)   
            elif current_token.tokentype == "Linebreak": # I HAS A var (only, no ITZ) - untyped or uninitialized variable
                variables[varident] = None # null value
                var_assign_ongoing = False # set back to false
                return ("VARIABLE", varident, "NOOB") # place untyped or uninitialized variable inside nodes list
            else:
                insert_output(f"[Syntax Error] Invalid variable assignment at line {current_line}")
                
        else:
            insert_output(f"[Syntax Error] Invalid variable identifier at line {current_line}")
    else:
        insert_output(f"[Syntax Error] Invalid variable declaration at line {current_line}")


def varident():
    global current_token
    if current_token.tokentype == "Variable Identifier": # check if variable identifier
        if current_token.tokenvalue not in variables:
            insert_output(f"[Syntax Error] Variable {current_token.tokenvalue} not yet declared at line {current_line}")
        node = current_token
        advance() # pass varident to go to next token
        return node
    else:
        insert_output(f"[Syntax Error] Invalid variable identifier at line {current_line}")

# tkinter pop up gui for user input (GIMMEH)
def popup_input(varident_):
    global variables
    user_input = simpledialog.askstring("Input", f"GIMMEH {varident_.tokenvalue}:")
    if user_input is None:
        variables[varident_.tokenvalue] = ""
        user_input = ""
    else:
        variables[varident_.tokenvalue] = user_input
    insert_output(user_input+"\n")
    update_symbol_table()
    print("User input:", user_input)

class Function: # function class
    def __init__(self, name, body, vars):
        self.name = name # string
        self.body = body # list
        self.vars = vars # dictionary

functions = {} # list of functions

# functions = {"funcname": {funcbody:[], token_start_idx:10, funcvars:{"x": 1, "y": 2, "z": 3}}}
# end marker - if u say so
# saved_main = {tokens: None, token_idx: None, current_line: None}
# save variables: tokens, token_idx, current_token, current_line


# only the syntax --- to edit
def check_function_def():
    global current_token, current_line
    advance() # pass HOW IZ I
    if current_token.tokentype == "Variable Identifier":
        funcname = current_token.tokenvalue
        advance() # pass function name
        
        # initialize function variables
        funcvars = {}
        # FUNCTION PARAMETERS
        # funcname var YR x AN YR y AN YR z
        while current_token.tokentype != "Linebreak":
            if current_token.tokentype == "Parameter Separator Keyword":
                advance() # pass YR (for first parameter)
                if current_token.tokentype != "Variable Identifier":
                    insert_output(f"[Syntax Error] Invalid function parameter (parameter name not found) at line {current_line}")
                else:
                    # place current_token.tokenvalue in funcvars
                    funcvars[current_token.tokenvalue] = None
                    advance() # pass parameter name
            elif current_token.tokentype == "And Keyword":
                advance() # pass AN
                if current_token.tokentype != "Parameter Separator Keyword":
                    insert_output(f"[Syntax Error] Invalid function parameter (YR not found) at line {current_line}")
                else:
                    advance() # pass YR
                    if current_token.tokentype != "Variable Identifier":
                        insert_output(f"[Syntax Error] Invalid function parameter (YR not found) at line {current_line}")
                    else:
                        funcvars[current_token.tokenvalue] = None
                        advance() # pass parameter name
            else:
                insert_output(f"[Syntax Error] Invalid function parameter (YR / AN YR not found) at line {current_line}")
        
        if_linebreak() # pass linebreak ?
        
        # save starting token idx and current line
        tokenidx = token_idx
        currentline = current_line
        # FUNCTION BODY
        funcbody = []
        while current_token.tokentype != "End of Function Keyword": # save the succeeding tokens until IF U SAY SO is found
            # get the token idx and current line
            funcbody.append(current_token)
            
            # NOT CHECKING STATEMENT VALIDITY YET
            # run in another process to check if it will result in an error
            if current_token.tokentype == "Linebreak":
                current_line += 1
                advance() # go to next token
                skip_empty_lines()
            else:
                advance() # go to next token 

        # functions = {"funcname": {funcbody:[], tokenidx:20, currentline:5, funcvars:{"x": 1, "y": 2, "z": 3}}}
        # put in functions list
        functions[funcname] = {
            "funcbody": funcbody, 
            "tokenidx": tokenidx, 
            "currentline":currentline, 
            "funcvars": funcvars
            }
        advance() # pass IF U SAY SO     
        return ("FUNCTION", functions[funcname])
    else:
        insert_output(f"[Syntax Error] Invalid function name at line {current_line}")
    
def place_in_IT(value):
    global variables
    variables["IT"] = value
    update_symbol_table()
    
def semi_typecast_expression():
    new_value = None
    advance() # pass MAEK
    var_token = varident() # var
    # may or may not include A typecast_prefix
    if current_token.tokentype != "Typecast Prefix" and current_token.tokentype != "Type Literal":
        insert_output(f"[SyntaxError: Invalid typecast: Line at line {current_line}")
    else:
        if current_token.tokentype == "Typecast Prefix":
            advance() # pass A
        new_value = handle_semi_typecast(var_token.tokenvalue, current_token.tokenvalue, current_line)
        advance() # pass NUMBAR/NUMBR/TROOF/YARN              
    return new_value  # to not print parse tree in var R MAEK var TYPE

# for FUNCTIONS (reusable)
def get_op_value():
    if current_token.tokentype in expression_tokens:
        ans = expression() # pass expression
    elif current_token.tokentype == "Variable Identifier":
        var_token = varident() # pass variable
        ans = variables[var_token.tokenvalue]
    elif current_token.tokentype in ["Numbr Literal", "Numbar Literal", "Troof Literal", "String Delimiter"]:
        ans = literal() # pass literal
    else:
        insert_output(f"[Syntax Error] Invalid expression at line {current_line}")
    return ans

# show the line based on the current_line
def get_line(line):
    global lines
    return lines[line-1]

# GLOBAL VARIABLES FOR FUNCTIONS    
saved_main = {"tokens": [], "token_idx": -1, "current_line": 1, "variables": {"IT":None}, "var_assign_ongoing": False}
function_on = 0 # checker if function is running (if function is on, the symbol table should print the saved main NOT the function variables)
loop_on = 0
has_return = 0 # checker for found yr

def statement():
    global function_on, has_return, current_token, var_assign_ongoing, tokens, token_idx, current_line, variables, saved_main
    if current_token.tokentype == "Define Function Keyword": # checks for function definitions after var_declaration and before kthxbye
        func_details = check_function_def()
        return ("FUNCTION_DEF", func_details)
    elif current_token.tokentype == "Function Call": # [] no function nesting
        advance() # pass I IZ
        if current_token.tokentype != "Variable Identifier":
            insert_output(f"[Syntax Error] Invalid function name at line {current_line}")
        else:
            # FUNCTION PARAMETERS
            # funcname YR SUM OF 1 AN 2 AN YR <expr/lit/var>
            funcname = current_token.tokenvalue

            if funcname not in functions: # check if funcname is in functions
                insert_output(f"[Syntax Error] Function not yet declared at line {current_line}")
            advance() # pass funcname
            
            args = [] # parameter arguments list
            
            # FUNCTION ARGUMENTS
            while current_token.tokentype != "Linebreak":
                if current_token.tokentype == "Parameter Separator Keyword":
                    advance() # pass YR (for first parameter)
                    param_val = get_op_value()
                    args.append(param_val)
                elif current_token.tokentype == "And Keyword":
                    advance() # pass AN
                    if current_token.tokentype != "Parameter Separator Keyword":
                        insert_output(f"[Syntax Error] Invalid function parameter (YR not found) at line {current_line}")
                    else:
                        advance() # pass YR
                        param_val = get_op_value()
                        args.append(param_val)
                else:
                    insert_output(f"[Syntax Error] Invalid function argument at line {current_line}")
            # check total number of parameters if same with number of arguments 
            numParams = len(functions[funcname]["funcvars"])
            if numParams != len(args):
                insert_output(f"[Function Error] Does not meet required number of arguments ({numParams}) in {funcname} function at line {current_line}")
            
            funcvars = functions[funcname]["funcvars"]
            
            # update function's funcvars with the arguments
            params = list(funcvars.keys())

            for i in range(numParams):
                funcvars[params[i]] = args[i]
            funcvars["IT"] = None # place IT in dictionary
            
            # save main details (PC)
            saved_main = {"token_idx": token_idx, "current_line": current_line, "variables": variables, "var_assign_ongoing": var_assign_ongoing}
        
            # update main details with function details
            # functions = {"funcname": {funcbody:[], token_start_idx:10, funcvars:{"x": 1, "y": 2, "z": 3}}}
            token_idx = functions[funcname]["tokenidx"]
            current_line = functions[funcname]["currentline"]
            variables = functions[funcname]["funcvars"]
            var_assign_ongoing = False # initialize to false first
            current_token = tokens[token_idx]

            if function_on == 1:
                insert_output(f"[Syntax Error] Function nesting is not allowed or implementable at line {current_line}")
            function_on = 1 # run function
            # RUN FUNCTION BODY
            while current_token.tokentype != "End of Function Keyword":
                # check if function is off, break
                if function_on == 0:                  
                    break
                statement()
                if_linebreak()
            
            if has_return == 0: # no return value; IT in main is still NOOB
                saved_main["variables"]["IT"] = None

            # restore main details (PC)
            token_idx = saved_main["token_idx"]
            current_token = tokens[token_idx]
            current_line = saved_main["current_line"]
            variables = saved_main["variables"]
            var_assign_ongoing = saved_main["var_assign_ongoing"]
            
            has_return = 0 # set has_return back to 0
            function_on = 0 # set function off (only one function at a time, no nesting)
            return ("FUNCTION_CALL", funcname, args)
    elif current_token.tokentype == "Print Keyword": 
        advance() # pass VISIBLE
        ans = "" # initialize empty string
        newline = True # checker for ! (suppress newline)
        while current_token.tokentype != "Linebreak":
            operand = print_expression()
            ans = str(ans) + str(operand)
            if current_token.tokentype == "Print Concatenation Keyword":
                advance() # advance +
            elif current_token.tokentype == "Suppress Newline":
                # if next token is linebreak, do not print newline else error
                if tokens[token_idx+1].tokentype == "Linebreak":
                    advance() # pass !
                    newline = False
                else:
                    insert_output(f"[Syntax Error] Suppress newline (!) must be followed by linebreak at line {current_line}") 
            elif current_token.tokentype == "Linebreak":
                break
            else:
                insert_output(f"[Syntax Error] : no + keyword detected at line {current_line}")
        
        # ans = print_expression()
        print(ans)
        place_in_IT(ans) # place in IT variable
        if newline == True:
            insert_output(ans + "\n")
        else:
            insert_output(ans)
        return ("PRINT", ans)  
    elif current_token.tokentype == "Input Keyword":
        advance() # pass GIMMEH
        varident_ = varident()
        # pop up tkinter input box
        popup_input(varident_)
        print("variables is now:", variables)
        return ("INPUT", varident_)
    elif current_token.tokentype == "Variable Identifier": #assignment statement
        var_assign_ongoing = True # variable assignment ongoing
        var_dest_token = varident()
        if current_token.tokentype == "Variable Value Reassignment":
            advance() # pass R
            if current_token.tokentype == "Variable Identifier": # var = var
                var_src_token = varident()
                variables[var_dest_token.tokenvalue] = variables[var_src_token.tokenvalue]
                update_symbol_table()
                var_assign_ongoing = False # set back to false, variable reassignment done
                return ("ASSIGN", var_dest_token, var_src_token)
            elif current_token.tokentype in ["Numbr Literal", "Numbar Literal", "Troof Literal", "String Delimiter"]: # var = literal
                lit_value = literal()
                variables[var_dest_token.tokenvalue] = lit_value
                update_symbol_table()
                var_assign_ongoing = False # set back to false, variable reassignment done
                return ("ASSIGN", var_dest_token, lit_value)
            elif current_token.tokentype in expression_tokens: # var = expression
                expr_val = expression()
                variables[var_dest_token.tokenvalue] = expr_val
                update_symbol_table()
                var_assign_ongoing = False # set back to false, variable reassignment done
                return ("ASSIGN", var_dest_token, expr_val)
            else:
                insert_output(f"[Syntax Error] Invalid variable value reassignment at line {current_line}")
        elif current_token.tokentype == "Full Typecast Keyword": # changing the type of the variable
            advance() # pass IS NOW A
            if current_token.tokentype == "Type Literal":
                type_literal_ = current_token
                handle_full_typecast(var_dest_token.tokenvalue, type_literal_.tokenvalue, current_line)
                advance() # pass NUMBAR/NUMBR/TROOF/YARN
                update_symbol_table()
                var_assign_ongoing = False # set back to false, variable reassignment done
                return("FULL_TYPECAST", var_dest_token, type_literal_)
            else:
                insert_output(f"[Syntax Error] Invalid typecast literal at line {current_line}")
        
        elif current_token.tokentype == "Linebreak": # var only as statement
            # get the value of variable and place in IT
            value = variables[var_dest_token.tokenvalue]
            place_in_IT(value) # place in IT variable
            return ("VARIABLE", var_dest_token, value)
        else:
            insert_output(f"[Syntax Error] Invalid variable value reassignment. R not found. at line {current_line}")
    
    elif current_token.tokentype in flow_control_tokens:  #FLOW CONTROL
        if current_token.tokentype == "Explicit Start Loop Keyword": #IM IN YR
            node = loop()
            loop_on = 0
        elif current_token.tokentype == "if Keyword":
            if_else_statement()
        elif current_token.tokentype == "Switch Keyword":
            switch_statement()
    
    elif current_token.tokentype in ["Numbr Literal", "Numbar Literal", "Troof Literal", "String Delimiter"]:
        ans = literal() # returns literal value
        place_in_IT(ans) # place in IT variable
        return ("LITERAL", ans)
    # to check if conflicting with switch-case
    elif current_token.tokentype == "General Purpose Break Keyword": # GTFO
        if function_on == 0:
            if loop_on == 0:
                insert_output(f"[Syntax Error] GTFO found outside function and loop at line {current_line}")
            else:
                advance()
                return "break"
        else:
            advance() # pass GTFO
            # make NOOB in IT main
            saved_main["variables"]["IT"] = None
            function_on = 0 # set function off
            return ("BREAK", None)
    elif current_token.tokentype == "Return Keyword": #FOUND YR    
        if function_on == 0:
            insert_output(f"[Syntax Error] Return keyword not allowed outside function at line {current_line}")
        else:
            advance() # pass FOUND YR
            ans = get_op_value() # pass var, literal, or expression
            # place in IT variable in saved_main
            saved_main["variables"]["IT"] = ans
            has_return = 1 # set has_return to 1 so IT would not be NOOB when it goes back to the function call running
            print("placed answer in IT: ", ans)
            function_on = 0 # set function off
            return ("RETURN", ans)
    # else check if expression (can also be a statement)
    else:
        if current_token.tokentype in expression_tokens:
            expression_ = expression()
            return expression_
        else:
            insert_output(f"[Syntax Error] Invalid statement at line {current_line}")

# FOR SMOOSH TYPECASTING
def subconvert_to_string(value):
    if isinstance(value, bool):
        if value == True:
            return "WIN"
        else:
            return "FAIL"
    elif value == None:
        insert_output(f"[Concatenation Error] Cannot implicitly typecast null value to string at line {current_line}")
    else:
        return str(value)

def convert_to_string():
    # if variable, get value then typecast
    if current_token.tokentype == "Variable Identifier":
        var_token = varident() # goes to next token after var, get variable token
        value = variables[var_token.tokenvalue]
        value = subconvert_to_string(value)        
    elif current_token.tokentype in ["Numbr Literal", "Numbar Literal", "Troof Literal", "String Delimiter"]:
        lit_value = literal()
        value = subconvert_to_string(lit_value)
    elif current_token.tokentype in expression_tokens:
        ans = expression()
        ans = check_if_bool(ans)
        value = subconvert_to_string(ans)
    else:
        insert_output(f"[Syntax Error] Invalid operand at line {current_line}")
    return value
        
def expression():
    global current_token, current_line, var_assign_ongoing
    ans = None
    if current_token.tokentype in arith_tokens:
        ans = arithmetic_expression() 
    elif current_token.tokentype == "Typecast Keyword":
        ans = semi_typecast_expression()
    elif current_token.tokentype in comp_tokens:
        ans = compare_expression()
    elif current_token.tokentype in bool_tokens:
        ans = boolean_expression()
    elif current_token.tokentype == "Concatenation Keyword": # SMOOSH
        advance() # pass SMOOSH
        ans = "" # initialize empty string
        while current_token.tokentype != "Linebreak":
            operand = convert_to_string() # convert to string
            ans = ans + operand
            if current_token.tokentype == "And Keyword":
                advance() # pass AN
            elif current_token.tokentype == "Linebreak":
                break
            else:
                insert_output(f"[Syntax Error] : no AN keyword detected at line {current_line}")
        print(ans)
    if var_assign_ongoing == False: # place in IT variable if not a variable assignment statement
        place_in_IT(ans)
    return ans

def typecast_string(string):
    numbr_pattern = r"-?([1-9][0-9]*|0)"
    numbar_pattern = r"-?(0|[1-9][0-9]*)(\.[0-9]+)?"
    # typecast string to numbr or numbar
    if string == "WIN":
        return 1
    elif string == "FAIL":
        return 0
    elif re.fullmatch(numbr_pattern, string):
        return int(string)
    elif re.fullmatch(numbar_pattern, string):
        return float(string)
    else:
        insert_output(f"[Arithmetic Error] Invalid String. Cannot convert '{string}' to NUMBR/NUMBAR at line {current_line}")
        # return None # prev

def typecast_troof(troof):
    # typecast troof to numbr or numbar
    if troof == "WIN":
        return 1
    else:
        return 0
    
def arithmetic_expression():
    global current_token, current_line
    if current_token.tokentype in ["Add Keyword","Subtract Keyword","Multiply Keyword","Divide Keyword","Modulo Keyword", "Return Larger Number Keyword", "Return Smaller Number Keyword"]:
        operationType = current_token.tokentype # save operation type
        advance() # pass keyword
        
        # left operand # operand can be a variable, numbar, numbr, string, troof  
        if current_token.tokentype in expression_tokens:
            left = expression()
        elif current_token.tokentype in ["Numbr Literal","Numbar Literal"]:
            left = current_token.tokenvalue
            advance() # pass LEFT OPERAND
        elif current_token.tokentype == "String Delimiter":
            advance() # pass starting "
            if current_token.tokentype == "String Literal":
                left = typecast_string(current_token.tokenvalue)
                advance() # pass string literal
                if current_token.tokentype != "String Delimiter":
                    insert_output(f"[Syntax Error] String delimiter expected at line {current_line}")
                advance() # pass closing "
            else:
                insert_output(f"[Syntax Error] Invalid string literal at line {current_line}")
        elif current_token.tokentype == "Troof Literal":
            left = typecast_troof(current_token.tokenvalue)
            advance() # pass LEFT OPERAND
        elif current_token.tokentype == "Variable Identifier":
            if current_token.tokenvalue in variables.keys() and variables[current_token.tokenvalue] is not None:
                if isinstance(variables[current_token.tokenvalue], str): # check if string
                    left = typecast_string(variables[current_token.tokenvalue])
                else: 
                    left = variables[current_token.tokenvalue]
                advance() # pass LEFT OPERAND
            else:
                insert_output(f"[Logic Error] Variable not found at line {current_line}")
        else:
            insert_output(f"[Syntax Error] Invalid operand at line {current_line}")
        
        if current_token.tokentype == "And Keyword":
            advance() # pass AN
            #right operand
            if current_token.tokentype in expression_tokens:
                right = expression()
            elif current_token.tokentype in ["Numbr Literal","Numbar Literal"]:
                right = current_token.tokenvalue
                advance() # pass numbr/numbar literal
            elif current_token.tokentype == "String Delimiter":
                advance() # pass starting "
                if current_token.tokentype == "String Literal":
                    right = typecast_string(current_token.tokenvalue)
                    advance() # pass string literal
                    if current_token.tokentype != "String Delimiter":
                        insert_output(f"[Syntax Error] String delimiter expected at line {current_line}")
                    advance()
                else:
                    insert_output(f"[Syntax Error] Invalid string literal at line {current_line}")
            elif current_token.tokentype == "Troof Literal":
                right = typecast_troof(current_token.tokenvalue)
                advance()
            elif current_token.tokentype == "Variable Identifier":
                if current_token.tokenvalue in variables.keys() and variables[current_token.tokenvalue] is not None:
                    if isinstance(variables[current_token.tokenvalue], str):
                        right = typecast_string(variables[current_token.tokenvalue])
                    else: right = variables[current_token.tokenvalue]
                    advance()
                else:
                    insert_output(f"[Logic Error] Variable value not found at line {current_line}")
            else:
                insert_output(f"[Syntax Error] Invalid operand at line {current_line}")            
           
            if left is None or right is None: # OPERAND NOT TYPECAST-ABLE
                insert_output(f"[Runtime Error] Cannot perform operation. Invalid operand. at line {current_line}")
            elif operationType == "Add Keyword": # ADD OPERATION
                result = left + right
                print(result)
                # advance() # pass RIGHT OPERAND (?)
                return result
            elif operationType == "Subtract Keyword":
                result = left - right
                print(result)
                # advance() # pass RIGHT OPERAND (?)
                return result
            elif operationType == "Multiply Keyword":
                result = left * right
                print(result)
                # advance() # pass RIGHT OPERAND (?)
                return result
            elif operationType == "Divide Keyword":
                if right != 0:
                    result = left / right
                else:
                    insert_output(f"[Arithmetic Error] Cannot divide by zero at line {current_line}")
                print(result)
                # advance() # pass RIGHT OPERAND (?)
                return result
            elif operationType == "Modulo Keyword":
                result = left % right
                print(result)
                return result
            elif operationType == "Return Larger Number Keyword":
                if left > right:
                    result = left
                elif left < right:
                    result = right
                else:
                    result = left
                print(result)
                return result 
            elif operationType == "Return Smaller Number Keyword":
                if left > right:
                    result = right
                elif left < right:
                    result = left
                else:
                    result = left
                print(result)
                return result 
            else:
                insert_output(f"[Syntax Error] Invalid arithmetic operation at line {current_line}")
        else:
            insert_output(f"[Syntax Error] AN keyword not found at line {current_line}")
    else:
        insert_output(f"[Syntax Error] Incorrect Arithmetic Expression at line {current_line}")
    
def compare_expression():
    global current_token, current_line
    if current_token.tokentype in ["Both Argument Equal Check Keyword", "Both Argument Not Equal Check Keyword"]: 
        comparisonType = current_token.tokentype #save comparison type
        advance() # pass BOTH SAEM/DIFFRINT

        # left operand # operand can be a variable, numbar, numbr, string, troof  
        if current_token.tokentype in expression_tokens:
            left = expression()
        elif current_token.tokentype in ["Numbr Literal","Numbar Literal"]:
            left = current_token.tokenvalue
            advance()
        elif current_token.tokentype == "String Delimiter":
            advance() # pass starting "
            if current_token.tokentype == "String Literal":
                left = current_token.tokenvalue
                advance() # pass string literal
                if current_token.tokentype != "String Delimiter":
                    insert_output(f"[Syntax Error] String delimiter expected at line {current_line}")
                advance() # pass closing "
            else:
                insert_output(f"[Syntax Error] Invalid string literal at line {current_line}")
        elif current_token.tokentype == "Troof Literal":
            left = current_token.tokenvalue
            advance() # pass LEFT OPERAND
        elif current_token.tokentype == "Variable Identifier":
            if current_token.tokenvalue in variables.keys() and variables[current_token.tokenvalue] is not None:
                if isinstance(variables[current_token.tokenvalue], str): # check if string
                    left = typecast_string(variables[current_token.tokenvalue])
                else: 
                    left = variables[current_token.tokenvalue]
                advance() # pass LEFT OPERAND
            else:
                insert_output(f"[Logic Error] Variable not found at line {current_line}")
        else:
            insert_output(f"[Syntax Error] Invalid operand at line {current_line}")

        if current_token.tokentype == "And Keyword":
            advance() # pass AN
            #right operand
            if current_token.tokentype in expression_tokens:
                right = expression()
            elif current_token.tokentype in ["Numbr Literal","Numbar Literal"]:
                right = current_token.tokenvalue
                advance()
            elif current_token.tokentype == "String Delimiter":
                advance() # pass starting "
                if current_token.tokentype == "String Literal":
                    right = current_token.tokenvalue
                    advance() # pass string literal
                    if current_token.tokentype != "String Delimiter":
                        insert_output(f"[Syntax Error] String delimiter expected at line {current_line}")
                    advance()
                else:
                    insert_output(f"[Syntax Error] Invalid string literal at line {current_line}")
            elif current_token.tokentype == "Troof Literal":
                right = current_token.tokenvalue
                advance()
            elif current_token.tokentype == "Variable Identifier":
                if current_token.tokenvalue in variables.keys() and variables[current_token.tokenvalue] is not None:
                    if isinstance(variables[current_token.tokenvalue], str): # check if string
                        right = typecast_string(variables[current_token.tokenvalue])
                    else: 
                        right = variables[current_token.tokenvalue]
                    advance()
                else:
                    insert_output(f"[Logic Error] Variable not found at line {current_line}")
            else:
                insert_output(f"[Syntax Error] Invalid operand at line {current_line}")            
           
            if left is None or right is None: # OPERAND NOT TYPECAST-ABLE
                insert_output(f"[Runtime Error] Cannot perform operation. Invalid operand. at line {current_line}")
              
            elif comparisonType == "Both Argument Equal Check Keyword": # Equal to ==
                print(f"Debug: type(left) = {type(left)}, type(right) = {type(right)}")
                result = "WIN" if left == right and type(left) == type(right) else "FAIL"
                return result
            elif comparisonType == "Both Argument Not Equal Check Keyword": # Equal to !=
                result = "WIN" if left != right else "FAIL"
                return result  
            else:
                insert_output(f"[Syntax Error] Invalid Comparison operation at line {current_line}")  
        else:
            insert_output(f"[Syntax Error] AN keyword not found at line {current_line}")


def boolean_expression():
    global current_token, current_line
    has_allOf_anyOf = 0
    infinite_arr = []

    if current_token.tokentype in ["Both True Check Keyword", "One or Both True Check Keyword", "Exactly One is True Check Keyword", "Negate Keyword", "Atleast One True Check Keyword", "All True Check Keyword"]:
        operationType = current_token.tokentype #save boolean operation
        advance()

        #ALL OF and ANY OF existence check (since can't be nested into each other or themselves)
        if operationType in ["Atleast One True Check Keyword", "All True Check Keyword"]: 
            has_allOf_anyOf += 1

        #NOT
        if operationType in ["Negate Keyword"]: 
            if current_token.tokentype in expression_tokens:
                op = expression()
            elif current_token.tokentype in ["Numbr Literal","Numbar Literal"]:
                op = current_token.tokenvalue
                if op == 0:
                    new_value = "FAIL"
                else:
                    new_value = "WIN"
                op = new_value
                advance()
            elif current_token.tokentype == "String Delimiter":
                advance()
                if current_token.tokentype == "String Literal":
                    op = current_token.tokenvalue
                    if op == "":
                        new_value = "FAIL"
                    else:
                        new_value = "WIN"
                    op = new_value
                    advance() #pass string literal
                    if current_token.tokentype != "String Delimiter":
                        insert_output(f"[Syntax Error] String delimiter expected at line {current_line}")
                    advance()
                else:
                    insert_output(f"[Syntax Error] Invalid string literal at line {current_line}")
            elif current_token.tokentype == "Troof Literal":
                op = current_token.tokenvalue
                advance() # pass LEFT OPERAND
            elif current_token.tokentype == "Variable Identifier":
                if current_token.tokenvalue in variables.keys() and variables[current_token.tokenvalue] is not None:
                    op = variables[current_token.tokenvalue]
                    if op == 0:
                        new_value = "FAIL"
                    elif op == "":
                        new_value = "FAIL"
                    else:
                        new_value = "WIN"
                    op = new_value
                    advance()
                else:
                    insert_output(f"[Logic Error] Variable not found at line {current_line}")
            else:
                insert_output(f"[Syntax Error] Invalid operand at line {current_line}")


            if op is None: # OPERAND NOT TYPECAST-ABLE
                insert_output(f"[Runtime Error] Cannot perform operation. Invalid operand. at line {current_line}")
            elif op == "WIN":
                result = "FAIL"
                return result
            elif op == "FAIL":
                result = "WIN"
                return result
            else:
                insert_output(f"[Syntax Error] Invalid Boolean operation at line {current_line}")  

        #BOTH OF, EITHER OF, WON OF
        elif operationType in ["Both True Check Keyword", "One or Both True Check Keyword", "Exactly One is True Check Keyword"]:
            if current_token.tokentype in expression_tokens:
                left = expression()
            elif current_token.tokentype in ["Numbr Literal","Numbar Literal"]:
                left = current_token.tokenvalue
                if left == 0:
                    new_value = "FAIL"
                else:
                    new_value = "WIN"
                left = new_value
                advance()
            elif current_token.tokentype == "String Delimiter":
                advance()
                if current_token.tokentype == "String Literal":
                    left = current_token.tokenvalue
                    if left == "":
                        new_value = "FAIL"
                    else:
                        new_value = "WIN"
                    left = new_value
                    advance() #pass string literal
                    if current_token.tokentype != "String Delimiter":
                        insert_output(f"[Syntax Error] String delimiter expected at line {current_line}")
                    advance()
                else:
                    insert_output(f"[Syntax Error] Invalid string literal at line {current_line}")
            elif current_token.tokentype == "Troof Literal":
                left = current_token.tokenvalue
                advance() # pass LEFT OPERAND
            elif current_token.tokentype == "Variable Identifier":
                if current_token.tokenvalue in variables.keys() and variables[current_token.tokenvalue] is not None:
                    left = variables[current_token.tokenvalue]
                    if left == 0:
                        new_value = "FAIL"
                    elif left == "":
                        new_value = "FAIL"
                    else:
                        new_value = "WIN"
                    left = new_value
                    advance()
                else:
                    insert_output(f"[Logic Error] Variable not found at line {current_line}")
            else:
                insert_output(f"[Syntax Error] Invalid operand at line {current_line}")
            
            if current_token.tokentype == "And Keyword":
                advance() # pass AN
                #right operand
                if current_token.tokentype in expression_tokens:
                    right = expression()
                elif current_token.tokentype in ["Numbr Literal","Numbar Literal"]:
                    right = current_token.tokenvalue
                    if right == 0:
                        new_value = "FAIL"
                    else:
                        new_value = "WIN"
                    right = new_value
                    advance()
                elif current_token.tokentype == "String Delimiter":
                    advance()
                    if current_token.tokentype == "String Literal":
                        right = current_token.tokenvalue
                        if right == "":
                            new_value = "FAIL"
                        else:
                            new_value = "WIN"
                        right = new_value
                        advance() #pass string literal
                        if current_token.tokentype != "String Delimiter":
                            insert_output(f"[Syntax Error] String delimiter expected at line {current_line}")
                        advance()
                    else:
                        insert_output(f"[Syntax Error] Invalid string literal at line {current_line}")
                elif current_token.tokentype == "Troof Literal":
                    right = current_token.tokenvalue
                    advance() # pass LEFT OPERAND
                elif current_token.tokentype == "Variable Identifier":
                    if current_token.tokenvalue in variables.keys() and variables[current_token.tokenvalue] is not None:
                        right = variables[current_token.tokenvalue]
                        if right == 0:
                            new_value = "FAIL"
                        elif right == "":
                            new_value = "FAIL"
                        else:
                            new_value = "WIN"
                        right = new_value
                        advance()
                    else:
                        insert_output(f"[Logic Error] Variable not found at line {current_line}")
                else:
                    insert_output(f"[Syntax Error] Invalid operand at line {current_line}")


                if right is None: # OPERAND NOT TYPECAST-ABLE
                    insert_output(f"[Runtime Error] Cannot perform operation. Invalid operand. at line {current_line}")
                elif operationType == "Both True Check Keyword": #BOTH OF (AND)
                    if left == right == "WIN":
                        result = "WIN"
                    else:
                        result = "FAIL"
                    return result
                elif operationType == "One or Both True Check Keyword": #EITHER OF (OR)
                    if left == "WIN" or right == "WIN":
                        result = "WIN"
                    else:
                        result = "FAIL"   
                    return result
                elif operationType == "Exactly One is True Check Keyword": #WON OF (XOR)
                    if (left == "WIN" and right == "FAIL") or (left == "FAIL" and right == "WIN"):
                        result = "WIN"
                    else:
                        result = "FAIL"
                    return result
                else:
                    insert_output(f"[Syntax Error] Invalid Boolean operation at line {current_line}")  
            else:
                 insert_output(f"[Syntax Error] Invalid Boolean operation at line {current_line}") 
        

        elif operationType in ["Atleast One True Check Keyword", "All True Check Keyword"]:
            if current_token.tokentype in ["All True Check Keyword", "Atleast One True Check Keyword"]: #checks if more than 1 ALL OF OR ANY OF
                has_allOf_anyOf += 1
                if has_allOf_anyOf > 1:
                    insert_output(f"[Syntax Error] ALL OF or ANY OF cannot be nested into each other and themselves at line {current_line}")

            while current_token.tokentype != "End of assignment Keyword":
                if current_token.tokentype in expression_tokens:
                    infinite_arr.append(expression())
                elif current_token.tokentype in ["Numbr Literal","Numbar Literal"]:
                    if current_token.tokenvalue == 0:
                        new_value = "FAIL"
                    else:
                        new_value = "WIN"
                    infinite_arr.append(new_value)
                    advance() # pass numbr, numbar
                elif current_token.tokentype == "String Delimiter":
                    advance() #pass string delim
                    if current_token.tokentype == "String Literal":
                        if current_token.tokenvalue == "":
                            new_value = "FAIL"
                        else:
                            new_value = "WIN"
                        infinite_arr.append(new_value)
                        advance() #pass string literal
                        if current_token.tokentype != "String Delimiter":
                            insert_output(f"[Syntax Error] String delimiter expected at line {current_line}")
                        advance() #pass string delim
                    else:
                        insert_output(f"[Syntax Error] Invalid string literal at line {current_line}")
                elif current_token.tokentype == "Troof Literal":
                    infinite_arr.append(current_token.tokenvalue)
                    advance() # pass LEFT OPERAND
                elif current_token.tokentype == "Variable Identifier":
                    if current_token.tokenvalue in variables.keys() and variables[current_token.tokenvalue] is not None:
                        output = variables[current_token.tokenvalue]
                        if output == 0:
                            new_value = "FAIL"
                        elif output == "":
                            new_value = "FAIL"
                        else:
                            new_value = "WIN"
                        output = new_value
                        infinite_arr.append(output)
                        print(infinite_arr.append)
                        advance() 
                    else:
                        insert_output(f"[Logic Error] Variable not found at line {current_line}")
                else:
                    insert_output(f"[Syntax Error] Invalid operand at line {current_line}")    

                if current_token.tokentype == "And Keyword":
                    advance() # pass AN
                elif current_token.tokentype == "End of assignment Keyword":
                    break
                else:
                    insert_output(f"[Syntax Error] Missing AN or MKAY at line {current_line}")
            advance()
            if operationType == "All True Check Keyword": #infinite AND (ALL OF)
                if "FAIL" in infinite_arr:
                    result = "FAIL"
                else:
                    result = "WIN"
                return result
            elif operationType == "Atleast One True Check Keyword": #infinite OR (ANY OF)
                if "WIN" in infinite_arr:
                    result = "WIN"
                else:
                    result = "FAIL"
                return result
            else:
                insert_output(f"[Syntax Error] Invalid Boolean operation at line {current_line}")  
        else:
            insert_output(f"[Syntax Error] Invalid Boolean operation at line {current_line}") 
    else: 
        insert_output(f"[Syntax Error] Invalid Boolean operation at line {current_line}") 

def loop():
    global loop_on, current_token, current_line
    loop_on = 1
    if current_token.tokentype == "Explicit Start Loop Keyword":
        advance()
        if current_token.tokentype == "Variable Identifier":
            loop_name = current_token.tokenvalue
            advance()
            if current_token.tokentype == "Increment Keyword": #UPPIN   
                op_type = "increment"
            elif current_token.tokentype == "Decrement Keyword": #NERFIN
                op_type = "decrement"
            else:
                insert_output(f"[Syntax Error] Loop operation not found at line {current_line}")
            advance()
            if current_token.tokentype == "Parameter Separator Keyword":
                advance() # pass YR
                if current_token.tokentype == "Variable Identifier":
                    loop_variable = current_token.tokenvalue
                    # check if value can be incremented or decremented and if it exists
                    numbr_pattern = r"-?([1-9][0-9]*|0)"
                    numbar_pattern = r"-?(0|[1-9][0-9]*)(\.[0-9]+)?"
                    if loop_variable in variables.keys():
                        if re.fullmatch(numbr_pattern, str(variables[loop_variable])):
                            variables[loop_variable] = handle_semi_typecast(loop_variable, "NUMBR", current_line)
                        elif re.fullmatch(numbar_pattern, str(variables[loop_variable])):
                            variables[loop_variable] = handle_semi_typecast(loop_variable, "NUMBAR", current_line)
                        elif str(variables[loop_variable]) == "WIN" or variables[loop_variable] == True: 
                            variables[loop_variable] = 1
                        elif str(variables[loop_variable]) == "FAIL" or variables[loop_variable] == False or variables[loop_variable] == None: 
                            variables[loop_variable] = 0
                        else:
                            insert_output(f"[Logic Error] Variable {loop_variable} cannot be incremented or decremented at line {current_line}")
                    else:
                        insert_output(f"[Logic Error] Variable does not exist at line {current_line}")
                    active_loops[loop_name] = loop_variable #save the loop name and associated variable to active loops
                    advance()
                    # optional TIL and WILE
                    savedpc_expression = 0
                    saved_currline_expr = 0
                    if current_token.tokentype == "Until indicated end of loop Keyword":
                        # end_cond_type = "until"
                        advance()
                        savedpc_expression = token_idx
                        saved_currline_expr = current_line
                        expr = expression()
                        #check if result is troof
                        print(expr)
                        if expr not in ["FAIL","WIN"]:
                            insert_output(f"[Runtime Error] Expression in loop operation did not convert to troof at line {current_line}")
                        # CODE BLOCK FOR LOOP
                        if_linebreak()
                        savedpc_codeblock = token_idx
                        saved_currline_codeblock = current_line
                        code_block = loop_statement_list()
                        #GTFO
                        if code_block == "break":
                            print("break runs")
                            #skip lines
                            while current_token.tokentype != "Break Loop Keyword":
                                    if current_token.tokentype == "Linebreak":
                                        current_line += 1
                                    if current_token.tokentype == "End Code Delimiter":
                                        insert_output(f"[Syntax Error] IM OUTTA YR not found at line {current_line}")
                                    advance()
                            if current_token.tokentype == "Break Loop Keyword": #OUTTA YR
                                advance()
                                if current_token.tokentype == "Variable Identifier":
                                    if current_token.tokenvalue == loop_name:
                                        advance()
                                        return "break"
                                else:
                                    insert_output(f"[Syntax Error] Loop variable identifier not found at line {current_line}")
                            else:
                                insert_output(f"[Syntax Error] IM OUTTA YR not found at line {current_line}")
                        print("Nodes after loop statement list",code_block)
                        if current_token.tokentype == "Break Loop Keyword": #OUTTA YR
                            advance()
                            if current_token.tokentype == "Variable Identifier":
                                if current_token.tokenvalue == loop_name:
                                    advance()
                                    savedpc_end = token_idx
                                    saved_currline_end = current_line
                                    if_linebreak()
                                    loop_complete = False
                                    while loop_complete == False:
                                        #increment or decrement
                                        if op_type == "increment":
                                            variables[loop_variable] = variables[loop_variable] + 1
                                            update_symbol_table()
                                        elif op_type == "decrement":
                                            variables[loop_variable] = variables[loop_variable] - 1
                                            update_symbol_table()
                                        else: 
                                            insert_output(f"[Runtime Error] No operation type given at line {current_line}")
                                        #revaluate expression
                                        restore(savedpc_expression, saved_currline_expr)
                                        expr = expression()
                                        print(expr)
                                        if expr not in ["FAIL","WIN"]:
                                            insert_output(f"[Runtime Error] Expression in loop operation did not convert to troof at line {current_line}")
                                        if expr == "FAIL":
                                            #loop again
                                            restore(savedpc_codeblock, saved_currline_codeblock)
                                            code_block = loop_statement_list()
                                            #GTFO
                                            if code_block == "break":
                                                restore(savedpc_end, saved_currline_end)
                                                active_loops.pop(loop_name)
                                                loop_complete = True
                                                # return "break"
                                        else:
                                            restore(savedpc_end, saved_currline_end)
                                            active_loops.pop(loop_name)
                                            loop_complete = True

                    elif current_token.tokentype == "While indicated end of loop Keyword":
                        advance()
                        savedpc_expression = token_idx
                        saved_currline_expr = current_line
                        expr = expression()
                        #check if result is troof
                        print(expr)
                        if expr not in ["FAIL","WIN"]:
                            insert_output(f"[Runtime Error] Expression in loop operation did not convert to troof at line {current_line}")
                        # CODE BLOCK FOR LOOP
                        if_linebreak()
                        savedpc_codeblock = token_idx
                        saved_currline_codeblock = current_line
                        code_block = loop_statement_list()
                        if code_block == "break":
                            #skip lines
                            while current_token.tokentype != "Break Loop Keyword":
                                    if current_token.tokentype == "Linebreak":
                                        current_line += 1
                                    if current_token.tokentype == "End Code Delimiter":
                                        insert_output(f"[Syntax Error] IM OUTTA YR not found at line {current_line}")
                                    advance()
                            if current_token.tokentype == "Break Loop Keyword": #OUTTA YR
                                advance()
                                if current_token.tokentype == "Variable Identifier":
                                    if current_token.tokenvalue == loop_name:
                                        advance()
                                        return "break"
                                else:
                                    insert_output(f"[Syntax Error] Loop variable identifier not found at line {current_line}")
                            else:
                                insert_output(f"[Syntax Error] IM OUTTA YR not found at line {current_line}")
                        print("Nodes after loop statement list",code_block)
                        if current_token.tokentype == "Break Loop Keyword": #OUTTA YR
                            advance()
                            if current_token.tokentype == "Variable Identifier":
                                if current_token.tokenvalue == loop_name:
                                    advance()
                                    savedpc_end = token_idx
                                    saved_currline_end = current_line
                                    if_linebreak()
                                    loop_complete = False
                                    while loop_complete == False:
                                        #increment or decrement
                                        if op_type == "increment":
                                            variables[loop_variable] = variables[loop_variable] + 1
                                            update_symbol_table()
                                        elif op_type == "decrement":
                                            variables[loop_variable] = variables[loop_variable] - 1
                                            update_symbol_table()
                                        else: 
                                            insert_output(f"[Runtime Error] No operation type given at line {current_line}")
                                        #revaluate expression
                                        restore(savedpc_expression, saved_currline_expr)
                                        expr = expression()
                                        print(expr)
                                        if expr not in ["FAIL","WIN"]:
                                            insert_output(f"[Runtime Error] Expression in loop operation did not convert to troof at line {current_line}")
                                        if expr == "WIN":
                                            #loop again
                                            restore(savedpc_codeblock, saved_currline_codeblock)
                                            code_block = loop_statement_list()
                                            #GTFO
                                            if code_block == "break":
                                                restore(savedpc_end, saved_currline_end)
                                                active_loops.pop(loop_name)
                                                loop_complete = True
                                                # return "break"                        
                                        else:
                                            restore(savedpc_end, saved_currline_end)
                                            active_loops.pop(loop_name)
                                            loop_complete = True

                    # elif current_token.tokentype == "Linebreak": # infinite loop until GTFO
                    #     end_cond_type = None
                    else:
                        insert_output(f"[Syntax Error] Unknown loop condition type at line {current_line}")
                    
                else:
                    insert_output(f"[Syntax Error] Variable identifier not found at line {current_line}")
            else:
                insert_output(f"[Syntax Error] YR not found at line {current_line}")
        else:
            insert_output(f"[Syntax Error] Label for the loop not found at line {current_line}")
    else:
        insert_output(f"[Syntax Error] Invalid Loop operation at line {current_line}")


def if_else_statement():
    global current_token
    has_YA_RLY = False
    has_match = False

    value_tocheck = variables["IT"] #stores result of initial statement for basis of value

    if current_token.tokentype == "if Keyword": #O RLY
        advance() #pass O RLY?
        if current_token.tokentype == "Linebreak":
            if_linebreak() #pass linebreak
            if current_token.tokentype == "if true Keyword":
                has_YA_RLY = True
                advance() #pass YA RLY
                if value_tocheck == "WIN":
                    if current_token.tokentype == "Linebreak":
                        if_linebreak() #pass linebreak
                        while current_token.tokentype != "else Keyword": #multiple statements in code block
                            if current_token.tokentype != "End of if Block Keyword":
                                statement()
                                if current_token.tokentype == "Linebreak":
                                    if_linebreak() #pass linebreak
                            if current_token.tokentype in ["else if Keyword", "else Keyword", "End of if Block Keyword"]:
                                break

                        while current_token.tokentype != "End of if Block Keyword": #pass entire NO WAI and MEBBE block
                            advance()
                            if current_token.tokentype == "Linebreak":
                                if_linebreak()

                        if current_token.tokentype == "End of if Block Keyword":
                            advance() #pass OIC 
                        else:
                            insert_output(f"[Syntax Error] Expected OIC at line {current_line}") 

                            
                    else: 
                        insert_output(f"[Syntax Error] Expected linebreak after YA RLY at line {current_line}")

                else:
                    
                    while current_token.tokentype != "else if Keyword":
                        if current_token.tokentype != "Linebreak":
                            advance() #pass entire YA RLY block
                        if current_token.tokentype == "Linebreak":
                            if_linebreak() #pass linebreak
                        if current_token.tokentype == "else Keyword":
                            break
                        if current_token.tokentype == "End of if Block Keyword":
                            break
                    
                    while current_token.tokentype != "else Keyword":
                        if current_token.tokenvalue == "else Keyword":
                            break
                        if current_token.tokentype == "End of if Block Keyword":
                            break
                        advance() #pass MEBBE
                        
                        statement()
                        if current_token.tokentype == "Linebreak":
                            if_linebreak() #pass linebreak
                        else:
                            insert_output(f"[Syntax Error] Expected linebreak statement in MEBBE at line {current_line}")
                        
                        if variables["IT"] == "WIN" and not has_match:
                            has_match = True
                            while current_token.tokentype != "else if Keyword":
                                statement()
                                if current_token.tokentype == "Linebreak":
                                    if_linebreak() #pass linebreak
                                if current_token.tokentype ==  "else Keyword":
                                    break
                        
                        elif variables["IT"] == "FAIL" or has_match:
                            while current_token.tokentype != "else if Keyword":
                                advance() #pass entire MEBBE block
                                if current_token.tokentype == "Linebreak":
                                    if_linebreak() #pass linebreak
                                if current_token.tokentype ==  "else Keyword":
                                    break

                        elif variables["IT"] == "WIN" and has_match:
                            insert_output(f"[Syntax Error] MEBBE conditions must be unique at line {current_line}")

                    if current_token.tokentype == "else Keyword" and value_tocheck == "FAIL":
                        advance() #pass NO WAI
                        if current_token.tokentype == "Linebreak":
                            if_linebreak() #pass linebreak
                        else: 
                            insert_output(f"[Syntax Error] Expected linebreak after NO WAI at line {current_line}")

                        if not has_match:
                            while current_token.tokentype != "End of if Block Keyword":
                                statement()
                                if current_token.tokentype == "Linebreak":
                                    if_linebreak() #pass linebreak
                                else:
                                    insert_output(f"[Syntax Error] Expected linebreak after statement at line {current_line}")                              
                        elif has_match:
                            while current_token.tokentype != "End of if Block Keyword":
                                advance() # pass statement
                                if current_token.tokentype == "Linebreak":
                                    if_linebreak() #pass linebreak
    

                    if current_token.tokentype == "End of if Block Keyword":
                        advance() #pass OIC 
                    else:
                        insert_output(f"[Syntax Error] Expected OIC at line {current_line}")   
            else:
                insert_output(f"[Syntax Error] Expected YA RLY at line {current_line}") 
        else:
            insert_output(f"[Syntax Error] Expected linebreak after O RLY? at line {current_line}") 
    else:
        insert_output(f"[Syntax Error] Expected O RLY? at line {current_line}") 


###### DO NOT UNCOMMENT (W/O MEBBE) ###################################

# def if_else_statement():
#     global current_token
#     has_YA_RLY = False

#     if current_token.tokentype == "if Keyword": #O RLY
#         advance() #pass O RLY?
#         if current_token.tokentype == "Linebreak":
#             # advance() #pass linebreak
#             if_linebreak()
#             if current_token.tokentype == "if true Keyword":
#                 advance() #pass YA RLY
#                 if variables["IT"] == "WIN":
#                     has_YA_RLY = True           
#                     if current_token.tokentype == "Linebreak":
#                         if_linebreak() #pass linebreak
#                         while current_token.tokentype != "else Keyword": #multiple statements in code block
#                             if current_token.tokentype != "End of if Block Keyword":
#                                 statement()
#                                 if_linebreak() #pass linebreak
#                             else:
#                                 break
#                         while current_token.tokentype != "End of if Block Keyword": #pass entire NO WAI block
#                             advance()
#                             if current_token.tokentype == "Linebreak":
#                                 if_linebreak()
#                     else: 
#                         error("[Syntax Error] Expected linebreak after YA RLY", current_line)

#                 elif variables["IT"] == "FAIL":
#                     if not has_YA_RLY:
#                         while current_token.tokentype != "else Keyword": #to pass entire YA RLY block
#                             if current_token.tokentype != "End of if Block Keyword":
#                                 advance()
#                                 if current_token.tokentype == "Linebreak":
#                                     if_linebreak()
#                             else:
#                                 break
                    
#                     if current_token.tokentype == "else Keyword":
#                         advance() #pass NO WAI
#                         if current_token.tokentype == "Linebreak":
#                             if_linebreak() #pass linebreak
#                             while current_token.tokentype != "End of if Block Keyword": #multiple statements in code block
#                                 statement()
#                                 if current_token.tokentype == "Linebreak":
#                                     if_linebreak()                   
#                         else:
#                             error("[Syntax Error] Expected linebreak after NO WAI", current_line) 

#                 if current_token.tokentype == "End of if Block Keyword":
#                     advance() #pass OIC 
#                 else:
#                     error("[Syntax Error] Expected OIC", current_line)  
#             else:
#                 error("[Syntax Error] Expected YA RLY", current_line) 
#         else:
#             error("[Syntax Error] Expected linebreak after O RLY?", current_line) 
#     else:
#         error("[Syntax Error] Expected O RLY?", current_line) 


def switch_statement():
    global current_token
    has_gtfo = False
    statement_value = variables["IT"]
    has_omg_match = False

    if current_token.tokentype == "Switch Keyword":
        advance() #pass WTF?
        if current_token.tokentype == "Linebreak":
            if_linebreak() #pass linebreak
            while current_token.tokentype != "End of if Block Keyword":
                if current_token.tokentype == "Switch Case Keyword":
                    advance() #pass OMG
                    if current_token.tokentype in ["Numbr Literal", "Numbar Literal", "Troof Literal", "String Literal"]:
                        if isinstance(statement_value, str):
                            statement_value = typecast_string(statement_value)
                        if statement_value == current_token.tokenvalue and not has_omg_match: #when a case is satisfied
            
                            has_omg_match = True
                            advance() #pass value literal
                            if_linebreak() #pass line break
                            if current_token.tokentype == "General Purpose Break Keyword":
                                has_gtfo = True
                                advance() #pass GTFO
                                if_linebreak() #pass linebreak
                            else:
                                if current_token.tokentype != "Switch Case Keyword":
                                    while current_token.tokentype != "General Purpose Break Keyword":
                                        statement()
                                        if current_token.tokentype == "Linebreak":
                                            if_linebreak()
                                        if current_token.tokentype == "General Purpose Break Keyword":
                                            has_gtfo = True
                                            advance() #pass GTFO
                                            if current_token.tokentype == "Linebreak":
                                                if_linebreak()
                                            break
                                        elif current_token.tokentype == "Switch Default Keyword":
                                            break
                                        elif current_token.tokentype == "Switch Case Keyword":
                                            advance() #pass omg
                                            advance() #pass value literal
                                            if_linebreak() #pass linebreak
                                            
                                        elif current_token.tokentype == "End of if Block Keyword":
                                            break
                                else:
                                    insert_output(f"[Logic Error] Missing code block for this case at line {current_line}")
                        elif statement_value == current_token.tokenvalue and has_omg_match:
                            insert_output(f"[Syntax Error] OMG literal must be unique at line {current_line}")
                        else: 
                            while current_token.tokentype != "Switch Case Keyword":
                                advance() #pass entire OMG block
                                if current_token.tokentype == "Linebreak":
                                    if_linebreak()
                                if current_token.tokentype == "Switch Default Keyword":
                                    break

                    else:
                        insert_output(f"[Logic Error] Invalid value literal at line {current_line}") 
                elif current_token.tokentype == "Switch Default Keyword":
                    advance() #pass OMGWTF
                    if_linebreak() # pass linebreak
                    if has_gtfo or has_omg_match:
                        while current_token.tokentype != "End of if Block Keyword":
                            advance()
                            if current_token.tokentype == "Linebreak":
                                if_linebreak() #pass linebreak
                            if current_token.tokentype == "General Purpose Break Keyword":
                                insert_output(f"[Syntax Error] OMGWTF does not need GTFO at line {current_line}")  
                    else:
                        while current_token.tokentype != "End of if Block Keyword":
                            statement()
                            if current_token.tokentype == "Linebreak":
                                if_linebreak() #pass linebreak
                            if current_token.tokentype == "General Purpose Break Keyword":
                                insert_output(f"[Syntax Error] OMGWTF does not need GTFO at line {current_line}")  
                    
                else:
                    insert_output(f"[Syntax Error] Expected OMG at line {current_line}")

        else:
            insert_output(f"[Syntax Error] Expected linebreak at line {current_line}") 
    else:
        insert_output(f"[Syntax Error] Expected WTF? at line {current_line}")

    if current_token.tokentype == "End of if Block Keyword":
        advance() #pass OIC
    else:
        insert_output(f"[Syntax Error] Expected OIC? at line {current_line}") 
        

def handle_full_typecast(var_name, target_type, current_line):
    global current_token
    yarn_pattern = r"^-?(0|[1-9][0-9]*)(\.[0-9]+)?$"
    
    #Get the value associated w/ variable identifier
    var_value = variables.get(var_name, "NOOB")

    #perfrom type conversion based on target type
    if target_type == "NUMBR":
        if var_value == "WIN" or (var_value == True and isinstance(var_value, bool)):   #Note: consider string literals WIN and FAIL, not just troof
            new_value = 1
            variables[var_name] = new_value
        elif var_value == "FAIL" or (var_value == False and isinstance(var_value, bool)):
            new_value = 0
            variables[var_name] = new_value
        elif isinstance(var_value, str):
            # test yarn_pattern
            if re.fullmatch(yarn_pattern, var_value):
                var_value = re.sub(r'\.\d+', '', var_value)
                variables[var_name] = int(var_value)
            else:
                insert_output(f"[Runtime Error] Invalid String. Cannot convert '{var_value}' to NUMBR at line {current_line}")
        elif isinstance(var_value, float):
            variables[var_name] = int(var_value)
        elif isinstance(var_value, int):
            variables[var_name] = var_value
        elif var_value == None: # explicit typecasting of noob to numbr
            variables[var_name] = 0
        else:
            insert_output(f"[Runtime Error] Cannot convert '{var_value}' to NUMBR at line {current_line}")
            
    elif target_type == "NUMBAR":
        if var_value == True or var_value=="WIN":   #Note: consider string literals WIN and FAIL, not just troof
            new_value = 1.0
            variables[var_name] = new_value
        elif var_value == False or var_value=="FAIL":
            new_value = 0.0
            variables[var_name] = new_value
        elif isinstance(var_value, str):
            if re.fullmatch(yarn_pattern, var_value):
                variables[var_name] = float(var_value)
            else:
              insert_output(f"[Runtime Error] Invalid String. Cannot convert '{var_value}' to NUMBAR at line {current_line}")  
        elif isinstance(var_value, float):
            variables[var_name] = var_value
        elif isinstance(var_value, int):
            variables[var_name] = float(var_value)
        elif var_value == None:
            variables[var_name] = 0.0 # explicit typecasting of noob to numbar
        else:
            insert_output(f"[Runtime Error] Cannot convert '{var_value}' to NUMBAR at line {current_line}")
    elif target_type == "TROOF":
            if var_value == "" or var_value == None or var_value==0: # None to False allowed
                new_value = False # will print FAIL in Symbol Table
            elif var_value == "WIN":
                new_value = True # equivalent to WIN Troof Literal
            elif var_value == "FAIL":
                new_value = False # equivalent to FAIL Troof Literal
            else:
                new_value = True # equivalent to WIN
        
            variables[var_name] = new_value
            
    elif target_type == "YARN":
        if variables[var_name] == True and isinstance(variables[var_name], bool):
            variables[var_name] = "WIN"
        elif variables[var_name] == False and isinstance(variables[var_name], bool):
            variables[var_name] = "FAIL"
        elif variables[var_name] == None:
            variables[var_name] = "" # explicit typecasting of noob to yarn (empty string)
        else:
            variables[var_name] = str(variables[var_name])
    elif target_type == "NOOB": # var IS NOW A NOOB # typecase a variable to NOOB
        variables[var_name] = None
    else:
        insert_output(f"[Runtime Error] Failed to convert '{var_value}' at line {current_line}")

def handle_semi_typecast(var_name, target_type, current_line):
    global current_token
    yarn_pattern = r"^-?(0|[1-9][0-9]*)(\.[0-9]+)?$"
    
    #Get the value associated w/ variable identifier
    var_value = variables.get(var_name, "NOOB")
    
    #perfrom type conversion based on target type
    if target_type == "NUMBR":
        if var_value == "WIN" or (var_value == True and isinstance(var_value, bool)):   #Note: consider string literals WIN and FAIL, not just troof
            new_value = 1
        elif var_value == "FAIL" or (var_value == False and isinstance(var_value, bool)):
            new_value = 0
        elif isinstance(var_value, str):
            # test yarn_pattern
            if re.fullmatch(yarn_pattern, var_value): # check if string is a number
                var_value = re.sub(r'\.\d+', '', var_value)
                new_value = int(var_value) # change to integer
            else:
                insert_output(f"[Runtime Error] Invalid String. Cannot convert '{var_value}' to NUMBR at line {current_line}")
        elif isinstance(var_value, float):
            new_value = int(var_value) # change float to integer
        elif isinstance(var_value, int):
            new_value = var_value # integer still same
        else: # for None
            insert_output(f"[Runtime Error] Cannot convert '{var_value}' to NUMBR at line {current_line}")

    elif target_type == "NUMBAR":
        if var_value == True or var_value=="WIN":   #Note: consider string literals WIN and FAIL, not just troof
            new_value = 1.0
        elif var_value == False or var_value=="FAIL":
            new_value = 0.0
        elif isinstance(var_value, str):
            if re.fullmatch(yarn_pattern, var_value):
                new_value = int(var_value)
            else:
              insert_output(f"[Runtime Error] Invalid String. Cannot convert '{var_value}' to NUMBAR at line {current_line}")  
        elif isinstance(var_value, float): # float still the same
            new_value = var_value
        elif isinstance(var_value, int):
            new_value = float(var_value)
        else: # for None
            insert_output(f"[Runtime Error] Cannot convert '{var_value}' to NUMBAR at line {current_line}")
    elif target_type == "TROOF":
        if var_value == "" or var_value == 0 or var_value == None: # implicit typecasting of None to False
            new_value = False # will print FAIL in Symbol Table
        elif var_value == "WIN":
            new_value = True # equivalent to WIN Troof Literal
        elif var_value == "FAIL":
            new_value = False # equivalent to FAIL Troof Literal
        elif var_value == None:
            insert_output(f"[Runtime Error] Cannot convert uninitialized value to TROOF at line {current_line}")            
        elif var_value == False:
            new_value = False # still False
        else:
            new_value = True # equivalent to WIN
                        
    elif target_type == "YARN":
        if isinstance(var_value, bool) and var_value == True:
            new_value = "WIN"
        elif isinstance(var_value, bool) and var_value == False:
            new_value = "FAIL"
        elif var_value == None: # none to string only in explicit typecasting
            insert_output(f"[Runtime Error] Cannot convert uninitialized value to YARN at line {current_line}")
        else:
            new_value = str(var_value)
    elif target_type == "NOOB": # var IS NOW A NOOB # typecase a variable to NOOB
        new_value = None
    else:
        insert_output(f"[Runtime Error] Failed to convert '{var_value}' at line {current_line}")
    
    return new_value
                            
def literal():
    if current_token.tokentype in ["Numbr Literal", "Numbar Literal", "Troof Literal"]:
        type = current_token.tokentype
        value = current_token.tokenvalue
        if type == "Numbr Literal":
            final_value = int(value)
        elif type == "Numbar Literal":
            final_value = float(value)
        elif type == "Troof Literal":
            if value == "WIN":
                final_value = True
            else:
                final_value = False
        advance() # pass literal value
        return final_value
    elif current_token.tokentype == "String Delimiter": # string literal
        advance() # pass "
        if current_token.tokentype == "String Literal":
            final_value = current_token.tokenvalue
            advance() # pass string value
            if current_token.tokentype == "String Delimiter":
                advance() # pass "
                return final_value
            else:
                insert_output(f"[Syntax Error] String delimiter expected at line {current_line}")
        else:
            insert_output(f"[Syntax Error] Invalid string literal at line {current_line}")
    else:
        insert_output(f"[Syntax Error] Invalid literal at line {current_line}")

def statement_list():
    global current_token, current_line
    nodes = []
    while current_token.tokentype != "End Code Delimiter":
        node = statement()
        if node is not None:
            nodes.append(node)
        if_linebreak()
    return nodes

def function_statement_list():
    global current_token, current_line
    nodes = []
    while current_token.tokentype != "End of Function Keyword":
        node = statement()
        if node is not None:
            nodes.append(node)
        if_linebreak()
    return nodes

def loop_statement_list():
    global current_token, current_line
    nodes = []
    while current_token.tokentype != "Break Loop Keyword":
        if current_token.tokentype == "End Code Delimiter":
            insert_output(f"[Syntax Error] OUTTA YR not found at line {current_line}")
        if current_token.tokentype == "General Purpose Break Keyword":
            advance()
            return "break"
        node = statement()
        if node is not None:
            nodes.append(node)
        if_linebreak()
    return nodes

def print_expression():
    global current_token
    if current_token.tokentype in ["Numbr Literal", "Numbar Literal", "Troof Literal"]:
        literal_value = current_token.tokenvalue
        advance() # pass literal
        # print the value of the literal
        return literal_value
    elif current_token.tokentype == "Type Literal":
        if current_token.tokenvalue == "NOOB":
            advance() # pass NOOB
            return "NOOB"
        else:
            insert_output(f"[Print Error] Cannot print a type literal at line {current_line}")
    elif current_token.tokentype == "String Delimiter": # string literal
        advance() # pass opening "
        if current_token.tokentype == "String Literal":
            string_value = current_token.tokenvalue
            advance() #string delimiter
            if current_token.tokentype == "String Delimiter":
                advance()  # pass closing "
                #extract/print value of string literal 
                return string_value
            else:
                insert_output(f"[Syntax Error] String delimiter expected at line {current_line}")
        else:
            insert_output(f"[Syntax Error] Invalid string literal at line {current_line}")
    elif current_token.tokentype == "Variable Identifier": # check if variable identifier
        node = ("VARIDENT", current_token.tokentype, current_token.tokenvalue)
        if current_token.tokenvalue not in variables:
            insert_output(f"[Syntax Error] Variable {current_token.tokenvalue} not yet declared at line {current_line}")
        #extract/print value of var identifier
        variable_value = variables[current_token.tokenvalue]
        # change variable value to WIN or FAIL
        variable_value = check_if_bool(variable_value)
        advance() # pass varident
        # next should be linebreak or AN, else error
        if current_token.tokentype == "Linebreak" or current_token.tokentype == "Print Concatenation Keyword" or current_token.tokentype == "Suppress Newline":
            return variable_value
        else:
            insert_output(f"[Syntax Error] Invalid print arguments at line {current_line}")
    elif current_token.tokentype in expression_tokens:
        node = expression()
        ans = check_if_bool(node)
        return ans
    else:
        insert_output(f"[Syntax Error] Invalid print arguments at line {current_line}")

def check_if_bool(ans):
    if isinstance(ans, bool) and ans == True: # because True is similar to 1 
        return "WIN"
    elif isinstance(ans, bool) and ans == False: # False similar to 0
        return "FAIL"
    elif ans == None:
        return "NOOB"
    else:
        return ans

def check_if_bool_var(ans):
    if isinstance(ans, bool) and ans == True: # because True is similar to 1 
        return "WIN"
    elif isinstance(ans, bool) and ans == False: # False similar to 0
        return "FAIL"
    else:
        return ans
    
def syntax_analyzer():
    global current_token,token_idx
    print("\nSYNTAX ANALYZER:")
    try:
        advance()
        return program()
    except SyntaxError as e:
        print(f"Syntax error detected: {e}")
        return None

def do_parse_tree(tokens_list):
    global tokens
    tokens = tokens_list
    parse_tree = syntax_analyzer()

    if parse_tree:
        print(variables)
        print(("PROGRAM", parse_tree))
    else:
        print("\nParsing failed. No parse tree generated.")

# -------------------------------------------[  GUI ]-----------------------------------------------------------

# Global Variables for File State and Path
fileLoaded = False  # Tracks if a file has been loaded
file_path = ""  # Stores the path of the loaded file

# GUI Color Theme
bgcolor1 = "#E0F7FA"  # Light cyan (close to sky blue)
bgcolor2 = "#B3E5FC"  # Light blue
bgcolor3 = "#E1F5FE"  # Very light blue, almost white
bgcolor4 = "#FFFFFF"  # Pure white
bgcolor5 = "#81D4FA"  # Medium sky blue

# Dark Theme Colors
dark00 = "#1f2124"
dark0 = "#2f3136"
dark1 = "#292b2f"
dark2 = "#40444b"
dark3 = "#565960"
dark4 = "#c8ccd4"
bluishdark = "#6786b5"

# Font Configuration for Various UI Elements
defaultFont = ("Microsoft YaHei UI", 8, "normal")
labelFont = ("Microsoft YaHei UI", 8, "bold")
texteditorFont = ("Consolas", 10, "normal")

# Function to Insert Indentation with Spaces in Text Editor
def insert_spaces(event):
    textEditor.insert(tk.INSERT, " " * 4)
    return 'break'

# Program Functions

# Opens a file dialog to select a file and displays its path
def open_file():
    global fileLoaded, file_path
    file_path = filedialog.askopenfilename(title="Select a file", filetypes=[("Lolcode files", "*.lol"), ("All files", "*.*")])
    file = open(file_path, "r")
    if file_path != "":
        fileLoaded = True
        filepathText.config(state=tk.NORMAL)
        filepathText.delete("1.0", "end")
        filepathText.insert(tk.END, file_path)
        filepathText.config(state=tk.DISABLED)
        # Clears previous contents in textEditor and loads the file content
        textEditor.delete("1.0", tk.END)
        textEditor.insert("1.0", file.read())
        file.close()
        
def execute_lexical():
    """
    Executes the lexical analysis phase: extracts text from the editor, converts tabs to spaces,
    parses the text into tokens, and inserts valid tokens (excluding linebreaks and empty lines)
    into the lexeme table.
    """
    global tokens
    # Get text from the editor, replacing tabs with 4 spaces for consistency
    text = textEditor.get("1.0", tk.END)
    text = text.replace('\t', '    ')
    if text:
        tokens = parse_tkinter(text)  # Parses text into tokens using a custom tokenizer
        print(tokens)
        # Insert tokens into lexeme table, excluding linebreaks and empty lines
        for token in tokens:
            if token.tokentype != "Linebreak" and token.tokentype != "Empty Line" and token.tokentype != "Invalid":
                lexemeTable.insert("", "end", values=(token.tokenvalue, token.tokentype))

def execute_parser():
    """
    Executes the parser on the current tokens list, building a parse tree or performing syntax validation.
    """
    global tokens
    do_parse_tree(tokens)  # Calls the function to create a parse tree or analyze syntax

def update_symbol_table():
    """
    Updates the symbol table in the GUI with the current variables dictionary.
    Converts boolean values to 'WIN' (True) or 'FAIL' (False) before displaying.
    """
    global variables, symbolTable
    # Clear existing entries in the symbol table
    for i in symbolTable.get_children():
        symbolTable.delete(i)
    # Insert updated variables into the table with formatted values
    for key, value in variables.items():
        value = check_if_bool(value)  # Convert boolean to 'WIN'/'FAIL'
        symbolTable.insert("", "end", values=(key, value))

def reset_symbol_table():
    """
    Resets the symbol table and variables dictionary to the initial state, with only 'IT' set to None.
    """
    global variables, symbolTable, tokens, token_idx, current_token, current_line, errorMessage
    # Clear the symbol table
    for i in symbolTable.get_children():
        symbolTable.delete(i)
    # Reinitialize variables dictionary with default 'IT' variable
    variables = {'IT': None}
    for key, value in variables.items():
        symbolTable.insert("", "end", values=(key, value))
    
    # Reset parser-related global variables for a fresh parsing state
    tokens = []
    token_idx = -1
    current_token = None
    current_line = 1
    errorMessage = ""

def reset_lexeme_table():
    """
    Clears all entries in the lexeme table, preparing it for fresh lexical analysis.
    """
    global lexemeTable
    # Clear the lexeme table
    for i in lexemeTable.get_children():
        lexemeTable.delete(i)

def reset_console():
    """
    Resets the output console in the GUI by clearing all existing text.
    """
    # Allow text edits temporarily to clear the console
    outputText.configure(state=tk.NORMAL)
    outputText.delete("1.0", "end")
    outputText.configure(state=tk.DISABLED)

def reset_global_variables():
    """
    Resets all key global variables, including tokens, parsing indices, error messages, and
    other parser states such as function and loop flags, to ensure no residual state affects execution.
    """
    global tokens, token_idx, current_token, current_line, errorMessage, variables, saved_main, function_on, loop_on, has_return
    tokens = []
    token_idx = -1
    current_token = None
    current_line = 1
    errorMessage = ""
    variables = {'IT': None}  # Reset variables dictionary with default IT variable
    # Saved main state for potential function handling
    saved_main = {"tokens": [], "token_idx": -1, "current_line": 1, "variables": {"IT": None}, "var_assign_ongoing": False}
    function_on = 0  # Flag for whether a function is currently executing
    loop_on = 0  # Flag for loop status
    has_return = 0  # Flag to check if a return ('FOUND YR') has been executed

def execute_code():
    """
    Main function to execute LOLCode in the interpreter. Resets all global variables, tables, and
    the console, and then calls lexical and parser execution functions.
    """
    # Reset all global variables and clear tables and console
    reset_global_variables()
    reset_lexeme_table()
    reset_symbol_table()
    reset_console()
    # Execute lexical analysis and parsing
    execute_lexical()
    execute_parser()
    # update_symbol_table()
    pass

# Inserts the output into the outputText area
def insert_output(output):
    color = "white"  # Default color for output text
    should_raise_error = False  # Flag to track if a SyntaxError should be raised
    if "Error]" in output:
        color = "#f59393"  # Error message color
        should_raise_error = True  # Set the flag to raise the error later
        reset_symbol_table()
        reset_global_variables()
        reset_console()
    if output == None:
        output = "NOOB"  # Default output if none provided
    outputText.configure(state=tk.NORMAL)  # Make outputText editable temporarily
    start_index = outputText.index('insert')  # Get the current insertion point
    outputText.insert('insert', str(output)) # Insert the output text at the current insertion point
    end_index = f"{start_index}+{len(output)}c"  # Get the index after inserting text
    outputText.tag_configure(color, foreground=color)  # Configure the color tag
    outputText.tag_add(color, start_index, end_index)  # Apply the color tag
    outputText.configure(state=tk.DISABLED)  # Make outputText uneditable again

    if should_raise_error:
        raise SyntaxError(output)

# Main Tkinter Window Setup
root = tk.Tk()
root.title("WitLang LOLCODE Interpreter")

# Set window dimensions and center it on screen
window_width = 1350
window_height = 700
root.geometry(f"{window_width}x{window_height}")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 3  # Add padding on top
root.geometry(f"+{x}+{y}")

# Configure GUI Appearance and Style
font.nametofont("TkDefaultFont").configure(family=defaultFont[0], size=defaultFont[1])
root.config(bg=dark0)
topFrame = tk.Frame(root, bg=bgcolor1)
bottomFrame = tk.Frame(root, bg=dark0)

# Configure dark mode theme for the treeview component
style = ttk.Style()
style.theme_use('clam')
style.configure("Custom.Treeview", background=dark4, fieldbackground=dark4)

# Top Frame: Text Editor Setup
textEditorFrame = tk.Frame(topFrame, width=400, bg=dark0)
openfileUI = tk.Frame(textEditorFrame, bg=dark0)
filepathText = tk.Text(openfileUI, height=1, width=54, bg=dark1, fg="white", selectbackground=dark2, selectforeground="white", padx=5)
openfileButton = tk.Button(openfileUI, text="Open", command=open_file, bg=dark1, fg="white", font=labelFont, activebackground=dark0, activeforeground="white")
filepathText.configure(state=tk.DISABLED)

textEditFrame = tk.Frame(textEditorFrame, bg=dark0)
textEditor = tk.Text(textEditFrame, padx=20, pady=20, height=10, width=60, wrap='none', font=texteditorFont, selectbackground=dark2, selectforeground="white")

# Vertical Scrollbar for Text Editor
textEditorvsb = ttk.Scrollbar(textEditFrame, orient="vertical", command=textEditor.yview)
textEditor.configure(yscrollcommand=textEditorvsb.set, bg=dark0, fg="white", insertbackground="white")  # Dark mode
textEditorvsb.pack(side=tk.RIGHT, fill=tk.Y)

# Horizontal Scrollbar for Text Editor
textEditorhsb = ttk.Scrollbar(textEditFrame, orient="horizontal", command=textEditor.xview)
textEditor.configure(xscrollcommand=textEditorhsb.set)
textEditorhsb.pack(side=tk.BOTTOM, fill=tk.X)

openfileButton.pack(side=tk.RIGHT, fill=tk.X, expand=False)
filepathText.pack(side=tk.RIGHT, fill=tk.X, expand=True)
openfileUI.pack(side=tk.TOP, fill=tk.X, expand=False)
textEditor.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

textEditFrame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
textEditorFrame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Lexeme Table Configuration
lexemeFrame = tk.Frame(topFrame, width=300, bg=dark0)
lexemeTableLabel = tk.Label(lexemeFrame, text="Lexeme Table", font=labelFont, fg="white", bg=dark0)

lexemeTableFrame = tk.Frame(lexemeFrame, width=300, bg=dark0)

lexemeTable = ttk.Treeview(lexemeTableFrame, columns=("lexeme", "classification"), show='headings', style="Custom.Treeview")
lexemeTable.heading("lexeme", text="Lexeme")
lexemeTable.heading("classification", text="Classification")

# Vertical Scrollbar for Lexeme Table
lexemevsb = ttk.Scrollbar(lexemeTableFrame, orient="vertical", command=lexemeTable.yview)
lexemeTable.configure(yscrollcommand=lexemevsb.set)
lexemevsb.pack(side=tk.RIGHT, fill=tk.Y)

lexemeTableLabel.pack(side=tk.TOP)
lexemeTable.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
lexemeTableFrame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

lexemeFrame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Symbol Table Configuration
symbolFrame = tk.Frame(topFrame, width=300, bg=dark1)
symbolTableLabel = tk.Label(symbolFrame, text="Symbol Table", font=labelFont, fg="white", bg=dark1)
symbolTableFrame = tk.Frame(symbolFrame, width=300, bg=dark1)

symbolTable = ttk.Treeview(symbolTableFrame, columns=("identifier", "value"), show='headings', style="Custom.Treeview")
symbolTable.heading("identifier", text="Identifier")
symbolTable.heading("value", text="Value")

# Vertical Scrollbar for Symbol Table
symbolvsb = ttk.Scrollbar(symbolTableFrame, orient="vertical", command=symbolTable.yview)
symbolTable.configure(yscrollcommand=symbolvsb.set)
symbolvsb.pack(side=tk.RIGHT, fill=tk.Y)

symbolTableLabel.pack(side=tk.TOP)
symbolTable.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
symbolTableFrame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

symbolFrame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Bottom Frame: Execute Button and Output Console
executeButton = tk.Button(bottomFrame, text="EXECUTE", font=labelFont, command=execute_code, bg=dark1, fg="white", activebackground=dark0, activeforeground="white")
executeButton.pack(side=tk.TOP, fill=tk.X)

outputFrame = tk.Frame(bottomFrame)
outputText = tk.Text(outputFrame, bg=dark00, padx=20, pady=20, fg="white", height=10, width=60, wrap='none', font=texteditorFont, selectbackground=dark2, selectforeground="white")

# Scrollbars for Console Output Text
outputTextvsb = ttk.Scrollbar(outputFrame, orient="vertical", command=outputText.yview)
outputText.configure(yscrollcommand=outputTextvsb.set)
outputTextvsb.pack(side=tk.RIGHT, fill=tk.Y)

outputTexthsb = ttk.Scrollbar(outputFrame, orient="horizontal", command=outputText.xview)
outputText.configure(xscrollcommand=outputTexthsb.set)
outputTexthsb.pack(side=tk.BOTTOM, fill=tk.X)

outputText.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
outputFrame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
outputText.configure(state=tk.DISABLED)

# Run the Main GUI Loop
topFrame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
bottomFrame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

# Event Binds
textEditor.bind("<Tab>", insert_spaces)

root.mainloop()

# if __name__ == '__main__':
#     tokens = parse_terminal(sys.argv[1])
#     print(tokens)
#     parse_tree = syntax_analyzer()
#     print(variables)
#     print(("PROGRAM",parse_tree))