#Authors:
    # Gadil, Jea Anne
    # Leyco, Charlize Althea
    # Resuello, Roxanne Ysabel

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
import re
from collections import OrderedDict
    
def readFile(file_name):
    # Get the current working directory
    current_directory = os.getcwd()
    
    # Create the full file path
    file_path = os.path.join(current_directory, file_name)
    
    contents = []
    try:
        # Check if the file exists
        if os.path.isfile(file_path):
            # Open the file in read mode
            with open(file_path, 'r') as file:
                # Read and print the contents
                #file_content = file.read()
                #print(f"File contents:\n{file_content}")
                for lines in file:
                    contents.append(lines.replace("\n", ""))
        else:
            
            print(f"Error: The file {file_name} does not exist in the current directory.")
    except Exception as e:
        print(f"An error occurred: {e}")
    # print("check here", contents)
    return contents

# Milestone 1 - lexical analyzer
#===========================================================

# Keywords dictionary
keywords = {
    "HAI" : "Code Delimiter"
    , "KTHXBYE" : "Code Delimiter"
    , "I HAS A" : "Variable Declaration"
    , "ITZ" : "Variable Assignment"
    , "R" : "Assignment Operator"
    , "SUM OF" : "Arithmetic Operator"
    , "DIFF OF" : "Arithmetic Operator"
    , "PRODUKT OF" : "Arithmetic Operator"
    , "QUOSHUNT OF" : "Arithmetic Operator"
    , "MOD OF" : "Arithmetic Operator"
    , "BIGGR OF" : "Arithmetic Operator"
    , "SMALLR OF" : "Arithmetic Operator"
    , "BOTH OF" : "Boolean Operator"
    , "EITHER OF" : "Boolean Operator"
    , "WON OF" : "Boolean Operator"
    , "NOT" : "Boolean Operator"
    , "ANY OF" : "Infinite Arity Operator"
    , "ALL OF" : "Infinite Arity Operator"
    , "MKAY" : "Infinite Arity Delimiter"
    , "BOTH SAEM" : "Comparison Operator"
    , "DIFFRINT" : "Comparison Operator"
    , "SMOOSH" : "Concatenation Operator"
    , "AN" : "Literal or Identifier Separator"
    , "MAEK" : "Typecast Operator"
    , "R MAEK": "Reassignment Operator"
    , "A" : "Typecast Separator"
    , "IS NOW A" : "Reassignment Operator"
    , "VISIBLE" : "Output Keyword"
    , "GIMMEH" : "Input Keyword"
    , "O RLY?" : "If Delimiter"
    , "YA RLY" : "If Keyword"
    , "MEBBE" : "Else-if Keyword"
    , "NO WAI" : "Else Keyword"
    , "OIC" : "If-Else or Switch-Case Delimiter"
    , "WTF?" : "Switch-Case Delimiter"
    , "OMG" : "Case Keyword"
    , "OMGWTF" : "Default Case Keyword"
    , "IM IN YR" : "Loop Start Delimiter"
    , "GTFO" : "Break Keyword"
    , "UPPIN" : "Increment Operator"
    , "NERFIN" : "Decrement Operator"
    , "YR" : "Loop Separator"
    , "TIL" : "FAIL Loop Repeater"
    , "WILE" : "WIN Loop Repeater"
    , "IM OUTTA YR" : "Loop End Delimiter"
    , "HOW IZ I" : "Function Delimiter"
    , "IF U SAY SO" : "Function Delimiter"
    # ADDED
    , "WAZZUP" : "Variable Keyword"
    , "BUHBYE" : "Variable Keyword"
    , "FOUND YR": "Return Keyword"
    , "I IZ": "Function Call keyword"
    , "+": "Printing Delimiter"
}

# Regex for identifier
identifier = "^[a-zA-Z][a-zA-Z0-9_]*$"

# Regex for NUMBR/NUMBAR (number) literals
literals = ["^-?\d+$", "^-?\d*\.\d+$"]

# Regex for YARN (string) literals
string_literal = "^\"[^”]*\"$"

# Regex for OIC, delimiter for if-else and switch-case
oic_pattern = r'^\s*OIC\s*$'

# Regex for TROOF (bool) literals
bool_literal = "(WIN|FAIL)"

# Regex for TYPE literals
type_literal = "(NOOB|TROOF|NUMBAR|NUMBR|YARN)"
type_literal_syntax = ["NOOB", "TROOF", "NUMBAR", "NUMBR", "YARN"]

# Additional regex for the semantics analyzer 
wazzup_pattern = re.compile(r'^\s*WAZZUP\s*$')
buhbye_pattern = re.compile(r'^\s*BUHBYE\s*$')
kthxbye_pattern = re.compile(r'^\s*KTHXBYE\s*$')
# smoosh_pattern = re.compile(r'SMOOSH\s+"?[\w.]+"?(?:\s+AN\s+"?[\w.]+"?)*\s*$')
# check this
smoosh_pattern = re.compile(r'^SMOOSH\s+(\S+(\s+AN\s+(\S+|"([^"]*)"))*)\s*$')
smoosh_pattern_forfunc = r'SMOOSH\s+(\S+(\s+AN\s+(\S+|"([^"]*)"))*)\s*'
#arithmetic_pattern = r'(SUM OF|DIFF OF|PRODUKT OF|QUOSHUNT OF|MOD OF|BIGGR OF|SMALLR OF|BOTH OF|EITHER OF|WON OF|BOTH SAEM|DIFFRINT) ([a-zA-Z][a-zA-Z0-9_]*|[0-9]*\.?[0-9]+) (AN) ([a-zA-Z][a-zA-Z0-9_]*|[0-9]*\.?[0-9]+)'
#boolean_operation = r'(NOT|BOTH OF|EITHER OF|WON OF) ([a-zA-Z][a-zA-Z0-9_]*|[0-9]*\.?[0-9]+) (AN [a-zA-Z][a-zA-Z0-9_]*|[0-9]*\.?[0-9]+)'
# literal_pattern = r'([0-9]+|[0-9]+\.[0-9]+|".*"|WIN|FAIL)'
literal_pattern = r'(-?[0-9]+|[0-9]+\.[0-9]+|"[^"]*"|WIN|FAIL)'
#comparison_pattern = r'(BOTH SAEM|DIFFRINT) (.+?) AN (.+)'

#====================== FOR EXPRESSIONS ============================
arithmetic_pattern = r'(SUM OF|DIFF OF|PRODUKT OF|QUOSHUNT OF|MOD OF|BIGGR OF|SMALLR OF|BOTH OF|EITHER OF|WON OF|BOTH SAEM|DIFFRINT) ([a-zA-Z][a-zA-Z0-9_]*|-?[0-9]*\.?[0-9]+) (AN) ([a-zA-Z][a-zA-Z0-9_]*|-?[0-9]*\.?[0-9]+)'
boolean_operation = r'(NOT) ([a-zA-Z][a-zA-Z0-9_]*|-?[0-9]*\.?[0-9]+)'
comparison_pattern = r'(ALL OF|ANY OF) (.+?)(?: AN (.+?))* MKAY$'

#printing_pattern = r'^VISIBLE (.+)$'
#printing_pattern = re.compile(r'^VISIBLE (' + arithmetic_pattern + '|' + literal_pattern + '|' + variable_pattern + '|' + comparison_pattern + '|' + boolean_operation + ')')


variable_pattern = r'^[a-zA-Z_][a-zA-Z0-9_]*$'
variable_pattern_forfunc = r'[a-zA-Z_][a-zA-Z0-9_]*'
integer_pattern = r'^[+-]?\d+$'
float_pattern = r'^[+-]?\d+(\.\d+)?$'
boolean_pattern = r'^(WIN|FAIL)$'
yarn_pattern = r'".*"'
#variable_declaration_pattern = re.compile(r'^I HAS A ([a-zA-Z]+[a-zA-Z0-9_]*)( ITZ (' + binary_pattern + '|' + literal_pattern + '|' + variable_pattern + '|' + urinary_pattern + '|' + infinite_pattern + '))?\s*( BTW .*)?$') 
operand_pattern = r'(' + variable_pattern + '|' + literal_pattern + '|' + arithmetic_pattern + '|' + comparison_pattern + '|' + boolean_operation + '|' + yarn_pattern + ')'
printing_pattern = re.compile(r'^VISIBLE (' + operand_pattern + ')(?: (\+) (' + operand_pattern + '))*$')
#printing_pattern = re.compile(r'^VISIBLE (' + arithmetic_pattern + '|' + literal_pattern + '|' + variable_pattern + '|' + comparison_pattern + '|' + boolean_operation + '|' + yarn_pattern + ') (?:(\+) (' + arithmetic_pattern + '|' + literal_pattern + '|' + variable_pattern + '|' + comparison_pattern + '|' + boolean_operation + '|' + yarn_pattern +'))*$')
variable_declaration_pattern = re.compile(r'^I HAS A ([a-zA-Z]+[a-zA-Z0-9_]*)( ITZ (' + arithmetic_pattern + '|' + literal_pattern + '|' + variable_pattern + '|' + comparison_pattern + '|' + boolean_operation + '|' + smoosh_pattern_forfunc + '))?\s*( BTW .*)?$') 
typecast_pattern = re.compile(r'^MAEK ([a-zA-Z]+[a-zA-Z0-9_]*)( A (' + '|'.join(type_literal_syntax[:-1]) + ')| ' + type_literal_syntax[-1] + ')\s*( BTW .*)?\s*$')
typecast_pattern_forfunc = r'^MAEK ([a-zA-Z]+[a-zA-Z0-9_]*)( A (' + '|'.join(type_literal_syntax[:-1]) + ')| ' + type_literal_syntax[-1] + ')\s*( BTW .*)?\s*$'
reassignment_pattern = re.compile(r'^([a-zA-Z]+[a-zA-Z0-9_]*)\s*((IS NOW A)\s*(' + '|'.join(type_literal_syntax) + ')|(R MAEK)\s*([a-zA-Z]+[a-zA-Z0-9_]*)\s*(' + '|'.join(type_literal_syntax) + '))\s*(BTW .*)?$')       
assignment_pattern = re.compile(r'^([a-zA-Z]+[a-zA-Z0-9_]*)( R (' + arithmetic_pattern + '|' + literal_pattern + '|' + variable_pattern + '|' + comparison_pattern + '|' + boolean_operation + '|' + smoosh_pattern_forfunc + '))?\s*( BTW .*)?$')        

#loop_pattern = re.compile(r"IM IN YR ([a-zA-Z][a-zA-Z0-9_]*) (UPPIN|NERFIN) YR ([a-zA-Z][a-zA-Z0-9_]*) ((TIL|WILE) (.+))?")
#function_pattern = re.compile(r'HOW IZ I (\w+)(?: YR (\w+)(?: AN YR (\w+)(?: AN YR (\w+))?)?)? *$')
if_else_pattern = re.compile(r'^(O RLY\?|YA RLY|NO WAI|OIC)$')
# function_pattern = re.compile(r'HOW IZ I (\w+)(?: YR ([a-zA-Z_][a-zA-Z0-9_]*)(?: AN YR ([a-zA-Z_][a-zA-Z0-9_]*)(?: AN YR ([a-zA-Z_][a-zA-Z0-9_]*))?)?)? *$')


# original loop_pattern
# loop_pattern = re.compile(r"IM IN YR ([a-zA-Z][a-zA-Z0-9_]*) (UPPIN|NERFIN) YR ([a-zA-Z][a-zA-Z0-9_]*) ((TIL|WILE) (.+))?")
# new loop_pattern
loop_pattern = re.compile(r"IM IN YR (\b[a-zA-Z][a-zA-Z0-9_]*\b) (UPPIN|NERFIN) YR (\b[a-zA-Z][a-zA-Z0-9_]*\b) ((TIL|WILE) (.+))")


# old function used in the original working code
# function_pattern = re.compile(r'HOW IZ I (\w+)(?: YR (\w+)(?: AN YR (\w+)(?: AN YR (\w+))?)?)? *$')
# new pattern
function_pattern = re.compile(r'HOW IZ I ([a-zA-Z]\w*)(?: YR ([a-zA-Z]\w*)(?: AN YR ([a-zA-Z]\w*)(?: AN YR ([a-zA-Z]\w*))?)?)? *$')

# variable_function_pattern = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]*$')
combined_pattern_str = (
    arithmetic_pattern + '|' +
    comparison_pattern + '|' +
    smoosh_pattern_forfunc + '|' +
    boolean_pattern + '|' +
    literal_pattern + '|' +
    typecast_pattern_forfunc + '|' +
    variable_pattern_forfunc
    )
# Potential keywords array
potential_keyword = ["I", "I HAS", "SUM", "DIFF", "PRODUKT", "QUOSHUNT", "MOD"
                    , "BIGGR", "SMALLR", "BOTH", "EITHER", "WON", "ANY", "ALL"
                    , "IS", "IS NOW", "O", "YA", "NO", "IM", "IM IN", "IM OUTTA"
                    , "HOW", "HOW IZ", "IF", "IF U", "IF U SAY", "FOUND"]

# To remove comment in the line and tuples
to_remove = {'Multi-Line Comment', 'Single Line Comment', 'Single Line Comment Declaration', 'Multi-Line Comment Declaration'}

# flags
obtw = False
wazzup = False
hai = False
multi_line = False
obtw_line = 0
comments = False
comments_next = False
inside_wazzup_buhbye = False
if_delimiter = False
oic_found = False
if_keyword = False
else_keyword = False
wazzup_line = 0
variables = {}
functions = {}
if_else_condition = []
condition_index = []
loop_lines = []
loop_tokens = []
content = None
is_loop = False
is_loop_del = False
is_var_assignment = False
app = None
is_error = False
line_global = None
if_deli_index = 0

#for function
function_lines =  []
function_tokens = []
is_function = False
function_var = {"FUNCTION VARIABLES": {'value': " ====== ", 'data type': " "}}
is_function_del = False

#for switch case
switch_delimiter = False
switch_case_condition = []
temp = 0
default_case_index = 0
case_keyword = False
default_case_keyword = False

datatypes = {
    'int': "NUMBR",
    'float' : "NUMBAR",
    'str' : "YARN",
    'bool' : "TROOF",
    'NoneType' : "NOOB"
}

def is_integer(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def console_dislay(message, self):
    self.console.print_to_console(f"{message}")

def error_prompt(line_number, error_message, self):
    global is_error
    print(f"Error in line {line_number}: {error_message}")
    self.console.print_to_console(f"Error in line {line_number}: {error_message}")
    is_error = True

def arithmetic(line_number, stack, operation, self):
    operations_dict = {
        "SUM OF": "+",
        "DIFF OF": "-",
        "PRODUKT OF": "*",
        "QUOSHUNT OF": "/",
        "MOD OF": "%",
        "BIGGR OF": "max",
        "SMALLR OF": "min",
    }
    if len(stack) < 2:
        error_prompt(line_number, "Arithmetic expression error.", self)
    
    op2 = stack.pop()
    op1 = stack.pop()

    # if op2 is True or False, convert to 1 or 0
    if op2 == True:
        op2 = 1
    elif op2 == False:
        op2 = 0

    # if op1 is True or False, convert to 1 or 0
    if op1 == True:
        op1 = 1
    elif op1 == False:
        op1 = 0
    try:
        if operations_dict[operation] == "max":
            result = max(op2, op1)
        elif operations_dict[operation] == "min":
            result = min(op2, op1)
        else:
            result = eval(f"{op2} {operations_dict[operation]} {op1}")

            # Check if the operation is division
            if operations_dict[operation] == "/":
                # Check if the operands are integers
                if isinstance(op1, int) and isinstance(op2, int):
                    result = int(result)
    except:
        error_prompt(line_number, "Arithmetic expression error.", self)

    stack.append(result)
    return stack

def boolean(line_number, stack, operation, self):
    print(stack)
    operations_dict = {
        "BOTH OF": "and",
        "EITHER OF": "or",
        "WON OF": "^",
        "NOT": "!",
    }

    if len(stack) < 2 and operation != "NOT":
        error_prompt(line_number, "Boolean expression error.", self)

    if operation == "NOT":
        try:
            op1 = stack.pop()
            result = not op1
            stack.append(result)
            return stack
        except:
            error_prompt(line_number, "Boolean expression error.", self)
    else:
        op2 = stack.pop()
        op1 = stack.pop()

        # if op2 is True or False, convert to 1 or 0
        if float(op2) == 1.0:
            op2 = True
        elif op2 == 0:
            op2 = False

        # if op1 is True or False, convert to 1 or 0
        if float(op1) == 1.0:
            op1 = True
        elif op1 == 0:
            op1 = False

        print(f"op1 = {op1} : op2 = {op2}")
        try:
            result = eval(f"{op2} {operations_dict[operation]} {op1}")
        except:
            error_prompt(line_number, "Boolean expression error.", self)
    
    stack.append(result)
    return stack

def comparison(line_number, stack, operation, self):
    operations_dict = {
        "BOTH SAEM": "==",
        "DIFFRINT": "!=",
    }

    try:
        if len(stack) < 2:
            error_prompt(line_number, "Comparison expression error.", self)

        op2 = stack.pop()
        op1 = stack.pop()

        result = eval(f"{op2} {operations_dict[operation]} {op1}")
    except:
        error_prompt(line_number, "Comparison expression error.", self)

    stack.append(result)
    return stack

def arithmetic_analyzer(line, line_number, untokenized_line, self):

    #print(f"line: {line}")
    #print(f"untokenized_line: {untokenized_line}")
    global inside_wazzup_buhbye, wazzup_line, if_keyword, else_keyword, case_keyword, default_case_keyword

    

    if if_keyword == True and if_delimiter == False:
        if_keyword = False
        return

    if else_keyword == True and if_delimiter == False:
        else_keyword = False
        return
    
    if case_keyword == True and switch_delimiter == False:
        case_keyword = False
        return

    if default_case_keyword == True and switch_delimiter == False:
        default_case_keyword = False
        return
    
    # this is to ensure that the wazzup and buhbye block only contains variable declaration 
    # also, this checks whether the wazzup has corresponding buhbye, and vice versa
    if inside_wazzup_buhbye == True:
        match = variable_declaration_pattern.match(untokenized_line)
        match_code_delim = kthxbye_pattern.match(untokenized_line)
        if 'BUHBYE' in untokenized_line:
            if inside_wazzup_buhbye == False:
                error_prompt(line_number, "No matching WAZZUP declaration.", self)
            if not buhbye_pattern.match(untokenized_line):
                error_prompt(line_number, "BUHBYE should be alone on its line.", self)
            else:
                wazzup_line -=1
                inside_wazzup_buhbye = False
        elif match_code_delim:
            if wazzup_line != 0:
                error_prompt(line_number, "No matching BUHBYE declaration.", self)
        elif not match:
            error_prompt(line_number, "Must be variable declaration only.", self)

    prev = ""
    stack = []
    isInfiniteAnd = False
    isInfiniteOr = False

    # Check if infinite arity operator is present
    if line[0][0] == "ALL OF":
        if line[-1][0] == "MKAY":
            #print("============ALL OF")
            isInfiniteAnd = True
        else:
            error_prompt(line_number, "Boolean expression error.", self)
    elif line[0][0] == "ANY OF":
        if line[-1][0] == "MKAY":
            #print("============ANY OF")
            isInfiniteOr = True
        else:   
            error_prompt(line_number, "Boolean expression error.", self)

    revline = line[::-1]

    if isInfiniteAnd == True or isInfiniteOr == True:
        revline = revline[1:]

    counter = 0
    #print(f"REVLINE ====== {revline}")

    # CHECK IF THERE IS NESTED INFINITE ARITY OPERATOR
    anyof = ('ANY OF', 'Infinite Arity Operator')
    allof = ('ALL OF', 'Infinite Arity Operator')

    count = revline.count(anyof) + revline.count(allof)

    if count > 1:
        error_prompt(line_number, "Boolean expression error.", self)


    for word in revline:

        counter += 1
        # ======================== CHECK SYNTAX
        if counter == 1:
            if word[1] == "String Literal" or word[1] == "NUMBR Literal" or word[1] == "NUMBAR Literal" or word[1] == "TROOF Literal" or word[1] == "Identifier" or word[1] == "Boolean":
                prev = "operand"
        else:
            if counter != len(revline) and (isInfiniteAnd == True or isInfiniteOr == True):
                if word[0] == "ALL OF" or word[0] == "ANY OF":
                    error_prompt(line_number, "Expression error.", self)

            if prev == "operand":
                if word[1] == "Arithmetic Operator" or word[1] == "Boolean Operator" or word[1] == "Comparison Operator" or word[1] == "Infinite Arity Operator":
                    prev = "operator"
                elif word[0] == "AN":
                    prev = "AN"
                else:
                    error_prompt(line_number, "Expression error.", self)
            elif prev == "operator":
                if word[1] == "Arithmetic Operator" or word[1] == "Boolean Operator" or word[1] == "Comparison Operator" or word[1] == "Infinite Arity Operator":
                    prev = "operator"
                elif word[0] == "AN":
                    prev = "AN"
                else:
                    error_prompt(line_number, "Arithmetic expression error.", self)
            elif prev == "AN" :
                if word[0] == "AN" or word[1] == "Arithmetic Operator" or word[1] == "Boolean Operator" or word[1] == "Comparison Operator" or word[1] == "Infinite Arity Operator":
                    error_prompt(line_number, "Expression error.", self)
                else:
                    prev = "operand"


        # ======================== EVALUATE SEMANTICS
        # AFTER CHECKING IF THE CURRENT WORD HAS CORRECT TYPE, UPDATE PREV

        # IF OPERATION, PERFORM
        #print(f"{word[0]} : {variables[word[0]]['value']}")
        if word[1] == "Arithmetic Operator":
            #print(stack)
            # print(stack)
            # if current token is an arithmetic operator
            stack = arithmetic(line_number, stack, word[0], self)
            # print(stack)
        elif word[1] == "Boolean Operator":
            stack = boolean(line_number, stack, word[0], self)
        elif word[1] == "Comparison Operator":
            stack = comparison(line_number, stack, word[0], self)
        
        # IF OPERAND, ADD TO STACK
        
        elif word[0] in variables:
            print(word[0])
            #operand = stack.append(variables[word[0]]['value'])
            if variables[word[0]]['data type'] == 'NUMBR' or variables[word[0]]['data type'] == 'NUMBAR' or variables[word[0]]['data type'] == 'TROOF':
                if variables[word[0]]['data type'] == 'TROOF':
                    if variables[word[0]]['value'] == 'WIN':
                        stack.append(True)
                    else:
                        stack.append(False)
                else:
                    stack.append(variables[word[0]]['value'])
            elif variables[word[0]]['data type'] == 'YARN':
                num = variables[word[0]]['value']
                if is_integer(num):
                    stack.append(int(num))
                elif is_float(num):
                    stack.append(float(num))
            
            #print(stack)
                #stack.append(variables[word[0]]['value'])
        else:
            #print(f'num: {word[0]}')
            # Check if the element is a string and if it's a float or int
            if word[1] != "Infinite Arity Operator":

            
                try:
                    # Check if the element is enclosed in quotation marks
                    if word[0].startswith('"') and word[0].endswith('"'):
                        # Attempt to extract the number inside the quotes
                        num = word[0][1:-1]
                        # Check if the num is an integer or float
                        if is_integer(num):
                            stack.append(int(num))
                        elif is_float(num):
                            stack.append(float(num))
                    elif word[0] == "WIN":
                        stack.append(True)
                    elif word[0] == "FAIL":
                        stack.append(False)
                    else:
                        # Check if the element is a string and if it's a float or int
                        # Check if the num is an integer or float
                        num = word[0]
                        if is_integer(num):
                            stack.append(int(num))
                        elif is_float(num):
                            stack.append(float(num))

                except ValueError:
                    error_prompt(line_number, "EExpression error.", self)

        # If last element in revline and len(stack) != 1, print error
        #print(f"{counter} = {revline} : AND = {isInfiniteAnd} : OR = {isInfiniteOr}")
    if counter == len(revline) and len(stack) != 1 and isInfiniteAnd == False and isInfiniteOr == False:
        error_prompt(line_number, "Expressionn error.", self)
        #print(f"Error in line {line_number}: Arithmetic expression error.")
        return
    if isInfiniteAnd == True:
        print(stack)
        try:
            result = all(stack)
        except:
            error_prompt(line_number, "Boolean expression error.", self)
        if result is True:
            return "WIN"
        elif result is False:
            return "FAIL"
    elif isInfiniteOr == True:
        print(stack)
        try:
            result = any(stack)
        except:
            error_prompt(line_number, "Boolean expression error.", self)
        if result is True:
            return "WIN"
        elif result is False:
            return "FAIL"
    
   #print(stack)
    if len(stack) != 1:
        error_prompt(line_number, "Expressionn error.", self)

    global is_var_assignment

    if is_var_assignment == False:
        if stack[0] is not None:
            if stack[0] is True:
                variables['IT'] = {'value': "WIN", 'data type': "TROOF"}
            elif stack[0] is False:
                variables['IT'] = {'value': "FAIL", 'data type': "TROOF"}
            else:
                variables['IT'] = {'value': stack[0], 'data type': datatypes[type(stack[0]).__name__]}
    else:
        is_var_assignment = False
    
    #print(stack)
    
    if stack[0] is True:
        return "WIN"
    elif stack[0] is False:
        return "FAIL"
    else:
        return stack[0]

def print_analyzer(line, line_number, untokenized, self):
        

    global is_var_assignment, is_error
    isStart = True
    hasOperand = True
    global inside_wazzup_buhbye, wazzup_line
    toprint = ""

    if if_keyword == True and if_delimiter == False:
        return

    if else_keyword == True and if_delimiter == False:
        return
    
    # this is to ensure that the wazzup and buhbye block only contains variable declaration 
    # also, this checks whether the wazzup has corresponding buhbye, and vice versa
    if inside_wazzup_buhbye == True:
        match = variable_declaration_pattern.match(untokenized)
        match_code_delim = kthxbye_pattern.match(untokenized)
        if 'BUHBYE' in untokenized:
            if inside_wazzup_buhbye == False:
                error_prompt(line_number, "No matching WAZZUP declaration.", self)
            if not buhbye_pattern.match(untokenized):
                error_prompt(line_number, "BUHBYE should be alone on its line.", self)
            else:
                wazzup_line -=1
                inside_wazzup_buhbye = False
        elif match_code_delim:
            if wazzup_line != 0:
                error_prompt(line_number, "No matching BUHBYE declaration.", self)
        elif not match:
            error_prompt(line_number, "Must be variable declaration only.", self)

    operands = []
    

    operand = []
    #print(line)
    counter = 0
    #print(f"line: {line}")
    for word in line:

        counter += 1
        if word[0] == "VISIBLE" and isStart == True:  # Correct the condition here
            isStart = False
        elif word[1] == "Printing Delimiter" or counter == len(line):
            if counter == len(line):
                operand.append(word)
                operands.append(operand.copy())  # Use copy to avoid modifying the original list
                operand.clear()
            else:
                operands.append(operand.copy())  # Use copy to avoid modifying the original list
                operand.clear()
        else:
            operand.append(word)

    print(operands)
    for op in operands:
        if len(op) == 1:
            #print("INSIDE")
            if op[0][1] == "String Literal":
                toprint += op[0][0][1:-1]
            elif op[0][1] == "NUMBR Literal" or op[0][1] == "NUMBAR Literal" or op[0][1] == "TROOF Literal" or op[0][1] == "YARN Literal" or op[0][1] == "Boolean":
                toprint += op[0][0]
            elif op[0][1] == "Identifier":
                try:
                    toprint += str(variables[op[0][0]]['value'])
                except:
                    error_prompt(line_number, f"Variable {op[0][0]} is not yet declared.", self)
            else:
                error_prompt(line_number, "Print expression error.", self)
        else:
            print(op[0][1])
            if op[0][1] != "Arithmetic Operator" and op[0][1] != "Boolean Operator" and op[0][1] != "Comparison Operator" and op[0][1] != "Concatenation Operator" and op[0][1] != "Infinite Arity Operator":
                error_prompt(line_number, "Missing printing delimeter between operands.", self)
            
            expression = ""
            for word in op:
                expression += word[0]
                expression += " "
            
            if op[0][1] == "Arithmetic Operator" or op[0][1] == "Boolean Operator" or op[0][1] == "Comparison Operator" or op[0][1] == "Infinite Arity Operator":
                #print(f"expression: {expression[:-1]}")
                new_value = arithmetic_analyzer(op, line_number, expression[:-1], self)
                #def analyze(line, classification, line_number, all_tokens, self):
                toprint += str(new_value)
            else:
                try:
                    #print(op)
                    new_value = analyze(expression[:-1], op[0][1], line_number, op, self)
                    toprint += str(variables['IT']['value'])
                except:
                    error_prompt(line_number, "Print expression error.", self)

    if is_error == False:
        console_dislay(toprint, self)
    return toprint

def input_analyzer(line, line_number, untokenized_line, self):
    if len(line) != 2:
        error_prompt(line_number, "Input expression error.", self)
    else:
        if line[1][1] == "Identifier":
            try:
                dialog_input = app.console.get_user_input("")
                #user_input = input()
                variables[line[1][0]]['value'] = str(dialog_input)
                variables[line[1][0]]['data type'] = 'YARN'
                #app.console.print_to_console(dialog_input)
            except:
                error_prompt(line_number, "Input expression error.", self)
        else:
            error_prompt(line_number, "Input expression error.", self)

def remove_comments(line, all_tokens):
    # print("Line", line)
    # print("all tokens", all_tokens)
    line = line.strip()
    global to_remove
    words_to_remove = []
    
    for token in all_tokens[1:]:
        word, classification = token
        if classification in to_remove:
            words_to_remove.append(word)
    
    if len(words_to_remove) == 0:
        return line
    else:
        for remove in words_to_remove:
            line = line.replace(remove, '')
        print("ETO REMOVED NA DAPAT", line)
        return line


#This function checks for single line and multi-line comment errors
#if an error exists, prints the appropriate error message, else returns bool comment_error
def check_comment_errors(line, line_number, self):
    global obtw, obtw_line, comments

    comment_error = False
    
    if re.search(r'OBTW', line):
        # print(line)
        #set flags to true
        obtw = True
        obtw_line = line_number
        if re.compile(r'^(?!OBTW).+').match(line):
            error_prompt(line_number, "Multi-line comment error.", self)
            comment_error = True
            
    if re.search(r'TLDR', line): 
        # no OBTW 
        if not obtw:
            error_prompt(line_number, "No matching multi-line comment declaration.", self)
            comment_error = True
        if line != "TLDR":
            error_prompt(line_number, "Multi-line comment delimiter error.", self)
            comment_error = True
        obtw = False
    
    return comment_error

# original
expression = {"Variable Declaration", "Variable Assignment", "Identifier"}

def get_data_type(variable_to_analyze):
    data_type = ""
    if re.match(r'\d+\.\d+', variable_to_analyze): 
        data_type = "NUMBAR"
    elif variable_to_analyze.isdigit():  
        data_type = "NUMBR"
    elif variable_to_analyze in ('WIN', 'FAIL'):  
        data_type = "TROOF"
    elif variable_to_analyze.startswith('"') and variable_to_analyze.endswith('"'): 
        data_type = "YARN"
    elif variable_to_analyze == "None":
        data_type = "NOOB"
    else:
        data_type = "ELSE"
        
    return data_type

#This function checks the syntax 
def analyze(line, classification, line_number, all_tokens, self):

    global obtw, obtw_line, comments, inside_wazzup_buhbye, wazzup_line, expression, if_keyword, variables
    global else_keyword, case_keyword, default_case_keyword
    
    if if_keyword == True and if_delimiter == False:
        if_keyword = False
        return

    if else_keyword == True and if_delimiter == False:
        else_keyword = False
        return
    
    if case_keyword == True and switch_delimiter == False:
        case_keyword = False
        return

    if default_case_keyword == True and switch_delimiter == False:
        default_case_keyword = False
        return
    
    # this is to ensure that the wazzup and buhbye block only contains variable declaration 
    # also, this checks whether the wazzup has corresponding buhbye, and vice versa
    if inside_wazzup_buhbye == True:
        match = variable_declaration_pattern.match(line)
        match_code_delim = kthxbye_pattern.match(line)
        if 'BUHBYE' in line:
            if inside_wazzup_buhbye == False:
                error_prompt(line_number, "No matching WAZZUP declaration.", self)
            if not buhbye_pattern.match(line):
                error_prompt(line_number, "BUHBYE should be alone on its line.", self)
            else:
                wazzup_line -=1
                inside_wazzup_buhbye = False
        elif match_code_delim:
            if wazzup_line != 0:
                error_prompt(line_number, "No matching BUHBYE declaration.", self)
        elif not match:
            error_prompt(line_number, "Must be variable declaration only.", self)
        
# ======================================INPUT================================
    if re.match(r'^\s*GIMMEH', line):
        # Check if the syntax is correct
        input_match = re.match(r'^\s*GIMMEH\s+([a-zA-Z][a-zA-Z0-9_]*)\s*(?:BTW .*)?$', line)
        if input_match:
            input_analyzer(all_tokens, line_number, line, self)
        else:
            error_prompt(line_number, "Incorrect format for input.", self)
            
# ======================================CONCATENATION======================================
    #check for concatenation
    if re.match(r'^\s*SMOOSH', line):
        # Check if the syntax is correct
        smoosh_match = re.match(smoosh_pattern, line)
        if smoosh_match:            
            #Get all tokens
            tokens = smoosh_match.group(1).split(' AN ')
            
            correct_values = True

            to_concat = []

            for token in tokens:
                token_data_type = get_data_type(token)
                
                if token_data_type in ("NUMBAR", "NUMBR", "TROOF", "YARN"): 
                    to_concat.append(token)
                else: 
                #check if the variables are declared
                    if token in variables:
                        var_value = str(variables[token]['value'])
                        to_concat.append(var_value)
                    else:
                        error_prompt(line_number, f"Variable '{token}' is not yet declared.", self)
                        #print(f"Error in line {line_number}: Variable '{token}' is not yet declared.")
                        correct_values = False
                                    
            if correct_values == True:
                concatenated = ''.join([str(s).strip('"') for s in to_concat])
                concatenated = "\"" + concatenated + "\""
                print("Resulting string after concatenationnnnnn:", concatenated)
                if 'IT' not in variables:
                    variables['IT'] = {'value': concatenated, 'data type': 'YARN'}
                else:
                    variables['IT']['value'] = concatenated
                    variables['IT']['data type'] = 'YARN'
                return concatenated
        else: 
            error_prompt(line_number, "Incorrect format for concatenation.", self)
    
    #check for variable declaration
    if 'WAZZUP' in line:
        
        if not wazzup_pattern.match(line):
            error_prompt(line_number, "WAZZUP should be alone on its line.", self)
        else:
            inside_wazzup_buhbye = True
            wazzup_line += 1

    if classification == "Variable Declaration":
        if inside_wazzup_buhbye == True:
            match = variable_declaration_pattern.match(line)
            if match:
                variable_name = match.group(1)
                initial_value = match.group(3)
                if initial_value in variables:
                    temp_val = variables[initial_value]['value']
                    temp_type = variables[initial_value]['data type']
                    variables[variable_name] = {'value': temp_val, 'data type': temp_type}
                else:
                    if initial_value is not None:
                        if re.match(integer_pattern, initial_value):
                            variables[variable_name] = {'value': int(initial_value.strip()), 'data type': 'NUMBR'}
                        elif re.match(float_pattern, initial_value):
                            variables[variable_name] = {'value': float(initial_value.strip()), 'data type': 'NUMBAR'}
                        elif re.match(boolean_pattern, initial_value):
                            variables[variable_name] = {'value': initial_value.strip(), 'data type': 'TROOF'}
                        elif re.match(smoosh_pattern, initial_value):
                            # print("ff",initial_value)
                            index = all_tokens.index(('ITZ', 'Variable Assignment'))
                            
                                # Slice the list from that index onwards
                            filtered_tokens = all_tokens[index+1:]
                            # print("\n\n\nentered R", filtered_tokens)
                            # print("all tokens", all_tokens,"all tokens" ,initial_value, "all tokens",line_number, "all tokens",filtered_tokens )
                            inside_wazzup_buhbye = False
                            concatenated = analyze(initial_value, "Concatenation Operator", line_number,  filtered_tokens, self)
                            # print("\n\n*",concatenated)
                            # variables[variable_name]['value'] = variables['IT']['value']
                            # variables[variable_name]['data type'] = 'YARN'
                            variables[variable_name] = {'value': concatenated, 'data type': 'YARN'}


                            if 'IT' in variables:
                                del variables['IT']

                            inside_wazzup_buhbye = True

                        elif re.match(arithmetic_pattern, initial_value) or re.match(boolean_operation, initial_value) or re.match(comparison_pattern, initial_value):
                                print("DETECTED")
                                global is_var_assignment
                                is_var_assignment = True

                                # print(all_tokens)
                                # filtered_tokens = [(value, category) for value, category in all_tokens if category not in expression]
                                
                                # print(expression)

                                index = all_tokens.index(('ITZ', 'Variable Assignment'))

                                # Slice the list from that index onwards
                                filtered_tokens = all_tokens[index+1:]

                                #print("(**(*(*)))",filtered_tokens)
                                new_value = arithmetic_analyzer(filtered_tokens, line_number, line, self)
                                # print("new value", new_value)
                                if re.match(integer_pattern, str(new_value)):
                                    variables[variable_name] = {'value': int(new_value), 'data type': 'NUMBR'}
                                elif re.match(float_pattern, str(new_value)):
                                    variables[variable_name] = {'value': float(new_value), 'data type': 'NUMBAR'}
                                elif re.match(boolean_pattern, str(new_value)):
                                    variables[variable_name] = {'value': str(new_value), 'data type': 'TROOF'}
                                
                        elif re.match(yarn_pattern, initial_value):
                                variables[variable_name] = {'value': initial_value.strip(), 'data type': 'YARN'}
                        else:
                            error_prompt(line_number, "Variable declaration error.", self)
                    else:
                        variables[variable_name] = {'value': None, 'data type': 'NOOB'}
                    
                    
            else:
                error_prompt(line_number, "Variable declaration error.", self)
        else:
            error_prompt(line_number, "Variable declaration error. Must be inside WAZZUP BUHBYE block.", self)

    elif classification == "Typecast Operator":
        # MAEK operator only modifies the resulting value
        # thus, the typecasting here is stored in the key 'IT'
        match = typecast_pattern.match(line)
        if match:
            variable_name = match.group(1)
            variable_type = match.group(3) if match.group(3) else match.group(2)
            if variable_name in variables:
                if 'IT' not in variables:
                    variables['IT'] = {'value': None, 'data type': 'NOOB'} 
                else:
                    if variable_type == 'NUMBR':
                        if variables[variable_name]['data type'] == 'NUMBAR':
                            variables['IT']['value'] = int(variables[variable_name]['value'])
                            variables['IT']['data type'] = 'NUMBR'
                        elif variables[variable_name]['data type'] == 'TROOF':
                            if variables[variable_name]['value'] == 'WIN':
                                variables['IT']['value'] = 1
                                variables['IT']['data type'] = 'NUMBR'
                            else:
                                variables['IT']['value'] = 0
                                variables['IT']['data type'] = 'NUMBR'
                        elif variables[variable_name]['data type'] == 'YARN':
                            var_value = variables[variable_name]['value']
                            var_strip = var_value.strip('\"')
                            if var_strip.isnumeric():
                                variables['IT']['value'] = int(var_strip)
                                variables['IT']['data type'] = 'NUMBR'
                            else:
                                error_prompt(line_number, "Cannot cast non-numeric YARN to NUMBR.", self)
                                # print(f"Error in line {line_number}: Cannot cast non-numeric YARN to NUMBR.")
                        elif variables[variable_name]['data type'] == 'NOOB':
                            variables['IT']['value'] = 0
                            variables['IT']['data type'] = 'NUMBR'
                        

                    elif variable_type == 'NUMBAR':
                        if variables[variable_name]['data type'] == 'NUMBR':
                            variables['IT']['value'] = float(variables[variable_name]['value'])
                            variables['IT']['data type'] = 'NUMBAR'
                        elif variables[variable_name]['data type'] == 'TROOF':
                            if variables[variable_name]['value'] == 'WIN':
                                variables['IT']['value'] = 1.0
                                variables['IT']['data type'] = 'NUMBAR'
                            else:
                                variables['IT']['value'] = float(0)
                                variables['IT']['data type'] = 'NUMBAR'
                        elif variables[variable_name]['data type'] == 'YARN':
                            var_value = variables[variable_name]['value']
                            var_strip = var_value.strip('\"')
                            if var_strip.isnumeric():
                                variables['IT']['value'] = int(var_strip)
                                variables['IT']['data type'] = 'NUMBAR'
                            else:
                                error_prompt(line_number, "Cannot cast non-numeric YARN to NUMBAR.", self)
                        elif variables[variable_name]['data type'] == 'NOOB':
                            variables['IT']['value'] = float(0)
                            variables['IT']['data type'] = 'NUMBAR'

                    elif variable_type == 'YARN':
                        if variables[variable_name]['data type'] == 'NUMBAR':
                            formatted_value = "{:.2f}".format(variables[variable_name]['value'])
                            variables['IT']['value'] = formatted_value
                            variables['IT']['data type'] = 'YARN'
                        elif variables[variable_name]['data type'] == 'NUMBR':
                            variables['IT']['value'] = str(variables[variable_name]['value'])
                            variables['IT']['data type'] = 'YARN'
                        elif variables[variable_name]['data type'] == 'NOOB':
                            variables['IT']['value'] = ""
                            variables['IT']['data type'] = 'YARN'
                    
                    elif variable_type == 'TROOF':
                        if variables[variable_name]['data type'] == 'NOOB' or variables[variable_name]['value'] == None or variables[variable_name]['value'] == 0 or variables[variable_name]['value'] == float(0) or variables[variable_name]['value'] == "":
                            variables['IT']['value'] = 'FAIL'
                            variables['IT']['data type'] = 'TROOF'
                        else:
                            variables['IT']['value'] = 'WIN'
                            variables['IT']['data type'] = 'TROOF'
                        
                    else:
                        error_prompt(line_number, "Typecast error.", self)

            else:
                error_prompt(line_number, "Variable does not exist.", self)
                
        else:
            error_prompt(line_number, "Typecast error.", self)
    
    elif classification == "Reassignment Operator":
        #make a regex for reassignment operator for lolcode 
        match = reassignment_pattern.match(line)
        if match:
            variable_name = match.group(1)
            if match.group(3) == 'IS NOW A':
                variable_type = match.group(4)
            else: # 'R MAEK'
                variable_type = match.group(7)
            # print(variable_name, variable_type)
            if variable_name in variables:
                if variable_type == 'NUMBR':
                    if variables[variable_name]['data type'] == 'NUMBAR':
                        variables[variable_name]['value'] = int(variables[variable_name]['value'])
                        variables[variable_name]['data type'] = 'NUMBR'
                    elif variables[variable_name]['data type'] == 'TROOF':
                        if variables[variable_name]['value'] == 'WIN':
                            variables[variable_name]['value'] = 1
                            variables[variable_name]['data type'] = 'NUMBR'
                        else:
                            variables[variable_name]['value'] = 0
                            variables[variable_name]['data type'] = 'NUMBR'
                    elif variables[variable_name]['data type'] == 'YARN':
                        if variables[variable_name]['value'].isnumeric():
                            variables[variable_name]['value'] = int(variables[variable_name]['value'])
                            variables[variable_name]['data type'] = 'NUMBR'
                        else:
                            error_prompt(line_number, "Cannot reassign non-numeric YARN to NUMBR.", self)
                    elif variables[variable_name]['data type'] == 'NOOB':
                        variables[variable_name]['value'] = 0
                        variables[variable_name]['data type'] = 'NUMBR'
                elif variable_type == 'NUMBAR':
                    if variables[variable_name]['data type'] == 'NUMBR':
                        variables[variable_name]['value'] = float(variables[variable_name]['value'])
                        variables[variable_name]['data type'] = 'NUMBAR'
                    elif variables[variable_name]['data type'] == 'TROOF':
                        if variables[variable_name]['value'] == 'WIN':
                            variables[variable_name]['value'] = 1.0
                            variables[variable_name]['data type'] = 'NUMBAR'
                        else:
                            variables[variable_name]['value'] = float(0)
                            variables[variable_name]['data type'] = 'NUMBAR'
                    elif variables[variable_name]['data type'] == 'YARN':
                        if variables[variable_name]['value'].isnumeric():
                            variables[variable_name]['value'] = float(variables[variable_name]['value'])
                            variables[variable_name]['data type'] = 'NUMBAR'
                        else:
                            error_prompt(line_number, "Cannot reassign non-numeric YARN to NUMBAR.", self)
                    elif variables[variable_name]['data type'] == 'NOOB':
                        variables[variable_name]['value'] = float(0)
                        variables[variable_name]['data type'] = 'NUMBAR'
                
                elif variable_type == 'YARN':
                    if variables[variable_name]['data type'] == 'NUMBAR':
                        formatted_value = "{:.2f}".format(variables[variable_name]['value'])
                        variables[variable_name]['value'] = formatted_value
                        variables[variable_name]['data type'] = 'YARN'
                    elif variables[variable_name]['data type'] == 'NUMBR':
                        variables[variable_name]['value'] = str(variables[variable_name]['value'])
                        variables[variable_name]['data type'] = 'YARN'
                    elif variables[variable_name]['data type'] == 'NOOB':
                        variables[variable_name]['value'] = ""
                        variables[variable_name]['data type'] = 'YARN'
                
                elif variable_type == 'TROOF':
                    if variables[variable_name]['data type'] == 'NOOB' or variables[variable_name]['value'] == None or variables[variable_name]['value'] == 0 or variables[variable_name]['value'] == float(0) or variables[variable_name]['value'] == "":
                        variables[variable_name]['value'] = 'FAIL'
                        variables[variable_name]['data type'] = 'TROOF'
                    else:
                        variables[variable_name]['value'] = 'WIN'
                        variables[variable_name]['data type'] = 'TROOF'
                
                else:
                    error_prompt(line_number, "Reassignment error.", self)
        else:
            error_prompt(line_number, "Reassignment error.", self)

    elif classification == "Assignment Operator":
        #make a regex for assignment operator for lolcode 
        match = assignment_pattern.match(line)
        if match:
            variable_name = match.group(1)
            variable_val = match.group(3)
            print("here beh",variable_val)
            if variable_name in variables:
                if variable_val in variables:
                    temp_val = variables[variable_val]['value']
                    temp_type = variables[variable_val]['data type']
                    variables[variable_name]['value'] = temp_val
                    variables[variable_name]['data type'] = temp_type
                else:
                    if re.match(integer_pattern, variable_val):
                        variables[variable_name]['value'] = int(variable_val)
                        variables[variable_name]['data type'] = 'NUMBR'
                    elif re.match(float_pattern, variable_val):
                        variables[variable_name]['value'] = float(variable_val)
                        variables[variable_name]['data type'] = 'NUMBAR'
                    elif re.match(boolean_pattern, variable_val):
                        variables[variable_name]['value'] = variable_val.strip()
                        variables[variable_name]['data type'] = 'TROOF'
                    elif re.match(smoosh_pattern, variable_val):
                        print(variable_val)
                        index = all_tokens.index(('R', 'Assignment Operator'))
                        temp_itvalue = None
                        temp_itdatatype = 'NOOB'
                            # Slice the list from that index onwards
                        filtered_tokens = all_tokens[index+1:]
                        print("\n\n\nentered R",filtered_tokens)
                        if 'IT' in variables:
                            temp_itvalue = variables['IT']['value']
                            temp_itdatatype = variables['IT']['data type']
                        analyze(variable_val, "Concatenation Operator", line_number,  filtered_tokens, self)
                        variables[variable_name]['value'] = variables['IT']['value']
                        variables[variable_name]['data type'] = 'YARN'

                        if temp_itvalue is None:
                            del variables['IT']
                        else:
                            variables['IT']['value'] = temp_itvalue
                            variables['IT']['data type'] = temp_itdatatype
                    else:
                        if re.match(arithmetic_pattern, variable_val) or re.match(boolean_operation, variable_val) or re.match(comparison_pattern, variable_val):
                            #remove tokens using expression
                            is_var_assignment = True
                            # filtered_tokens = [(value, category) for value, category in all_tokens if category not in expression]
                            # new_value = arithmetic_analyzer(filtered_tokens, line_number, line, self)
                            index = all_tokens.index(('R', 'Assignment Operator'))

                            # Slice the list from that index onwards
                            filtered_tokens = all_tokens[index+1:]

                            print("(**(*(*)))",filtered_tokens)
                            new_value = arithmetic_analyzer(filtered_tokens, line_number, line, self)
                            if re.match(integer_pattern, str(new_value)):
                                variables[variable_name] = {'value': int(new_value), 'data type': 'NUMBR'}
                            elif re.match(float_pattern, str(new_value)):
                                variables[variable_name] = {'value': float(new_value), 'data type': 'NUMBAR'}
                            elif re.match(boolean_pattern, str(new_value)):
                                variables[variable_name] = {'value': str(new_value), 'data type': 'TROOF'}
                
                        else:
                            variables[variable_name]['value'] = variable_val.strip()
                            variables[variable_name]['data type'] = 'YARN'
        else:
            error_prompt(line_number, "Assignment error.", self)

def if_else_statement(content, lines, self):
    global condition_index, if_else_condition, is_loop

    # check the existence of if and else keywords and their respective codeblocks
    if_keywords = [i for i, x in enumerate(if_else_condition) if x[1][0][1] == "If Keyword"]
    else_keywords = [i for i, x in enumerate(if_else_condition) if x[1][0][1] == "Else Keyword"]

    # if either the length of if_keywords or else_keywords is 0, then there is no respective keyword found
    if len(if_keywords) == 0:
        error_prompt(if_else_condition[0][0], "No If Keyword found.", self)
    if len(else_keywords) == 0:
        pass

    # check if the if and else keywords have codeblocks
    for i in if_keywords:
        if i+1 >= len(if_else_condition) or if_else_condition[i+1][1][0][1] in ["If-Else or Switch-Case Delimiter", "Else Keyword"]:
            error_prompt(if_else_condition[i][0], "'YA RLY' has no code block.", self)

    for i in else_keywords:
        if i+1 >= len(if_else_condition) or if_else_condition[i+1][1][0][1] in ["If-Else or Switch-Case Delimiter", "Else Keyword"]:
            error_prompt(if_else_condition[i][0], "'NO WAI' has no code block.", self)
    
    # check if the variable 'IT' exists
    if 'IT' not in variables:
        error_prompt(if_else_condition[0][0], "Accessing a null value.", self)

    # check if the value of the key 'IT' in variables is equal to WIN
    # get the index of the first exression after the if or else keyword
    if variables['IT']['value'] == 'WIN':

        # find the tuple with 'If Keyword'
        for i in range(len(if_else_condition)):
            if if_else_condition[i][1][0][1] == "If Keyword":
                condition_index.append(i+1)
                break
    else:

        # find the tuple with 'If Keyword'
        for i in range(len(if_else_condition)):
            if if_else_condition[i][1][0][1] == "Else Keyword":
                condition_index.append(i+1)
                break

    # get the succeeding expressions after the if or else keyword if it is more than one 
    if if_else_condition[condition_index[0]+1][1][0][1] != "If-Else or Switch-Case Delimiter" or if_else_condition[condition_index[0]+1][1][0][1] != "Else Keyword" or if_else_condition[condition_index[0]+1][1][0][1] != "Break Keyword":        # print("======If-Else or Switch-Case Delimiter")
        if variables['IT']['value'] == 'WIN':
            for i in range(condition_index[0]+1, len(if_else_condition)):
                if if_else_condition[i][1][0][1] == "Else Keyword" or if_else_condition[i][1][0][1] == "If-Else or Switch-Case Delimiter":
                    break
                else:
                    condition_index.append(i)
        else:
            for i in range(condition_index[0]+1, len(if_else_condition)):
                if if_else_condition[i][1][0][1] == "If-Else or Switch-Case Delimiter":
                    break
                else:
                    condition_index.append(i)

    # perform the functionalities needed in the codeblock
    for inner_condition_index in condition_index:

        # similar format to lines 
        if_else_condition_newformat = [[item[0]] + item[1] if len(item) > 1 else [item[0]] for item in if_else_condition]
        
        # remove the comments in the line if there are any
        removed_comment_cond = remove_comments(content[if_else_condition[inner_condition_index][0]-1], if_else_condition_newformat[inner_condition_index])
        
        
        # print("ETOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO", if_else_condition)
        # print("removed_comment_cond", removed_comment_cond)
        # print("[if_else_condition[inner_condition_index]",if_else_condition[inner_condition_index] )
        # =============== LOOPS ===============
        if if_else_condition[inner_condition_index][1][0][1] == 'Loop Start Delimiter':
            is_loop = True
        
         #add the loop code to a list
        if is_loop == True:   
            loop_lines.append(removed_comment_cond)
            loop_tokens.append(if_else_condition[inner_condition_index])
        
        #set is_loop to False and call loop analyzer
        if if_else_condition[inner_condition_index][1][0][1] == "Loop End Delimiter":
            is_loop = False
            loop_analyzer(self)    
            
        if not is_loop:
            if if_else_condition[inner_condition_index][1][0][1] == 'Break Keyword':
                break
            elif if_else_condition[inner_condition_index][1][0][1] == 'Arithmetic Operator' or if_else_condition[inner_condition_index][1][0][1] == 'Boolean Operator' or if_else_condition[inner_condition_index][1][0][1] == 'Comparison Operator':
                b = arithmetic_analyzer(if_else_condition_newformat[inner_condition_index][1:], if_else_condition[inner_condition_index][0], lines, self)
                if b is not None:
                    print("line",if_else_condition[inner_condition_index][0],": ", b)
            elif if_else_condition[inner_condition_index][1][0][1] == 'Output Keyword':
                b = print_analyzer(if_else_condition_newformat[inner_condition_index][1:], if_else_condition[inner_condition_index][0], lines, self)
                if b is not None:
                    print("line",if_else_condition[inner_condition_index][0],": ", b)
                    #console_dislay(b, self)
            elif if_else_condition[inner_condition_index][1][0][1] == 'Function Call keyword':
                # print(f'{content[if_else_condition_newformat[inner_condition_index][0]-1]}\n{if_else_condition_newformat[inner_condition_index]}')
                function_analyzer(content[if_else_condition_newformat[inner_condition_index][0]-1], if_else_condition_newformat[inner_condition_index], self)
            else:
                if if_else_condition[inner_condition_index][1][0][1] == 'Identifier':
                    
                    analyze(removed_comment_cond, if_else_condition[inner_condition_index][1][1][1], if_else_condition[inner_condition_index][0], if_else_condition[inner_condition_index][1:][0], self)
                else:
                    analyze(removed_comment_cond,  if_else_condition[inner_condition_index][1][0][1], if_else_condition[inner_condition_index][0], if_else_condition[inner_condition_index][1:][0], self)

def loop_analyzer(self):
    global loop_lines, loop_tokens, if_keyword, oic_found, switch_delimiter
    global switch_case_condition, temp, default_case_index, if_else_condition, condition_index, if_delimiter
    
    # print("HEREEEEEEEEEEEEEEEEEEEEEEEEE", loop_tokens[0][1][1:])
    print("================INSIDE LOOP================")
    # print(loop_lines)
    # print(variables)
    # Check if the syntax is correct
    if re.match(loop_pattern, loop_lines[0]):
        loop_match = re.match(loop_pattern, loop_lines[0])
        
        #Extract values from the matched groups
        loop_label = loop_match.group(1)
        loop_operation = loop_match.group(2)
        loop_variable = loop_match.group(3)
        repeat_keyword = loop_match.group(5) if loop_match.group(5) else None
        loop_expression = loop_match.group(6) if loop_match.group(6) else None
        loop_block = loop_lines[1:-1]
        loop_variable_end = loop_lines[-1].replace("IM OUTTA YR ", "")
        
        #check if there is no code block
        if len(loop_block) == 0:
            error_prompt(loop_tokens[0][0], "Function has no code block.", self)
        
        #check if label is correct for ending loop delimeter
        if loop_variable_end.strip() == loop_label.strip():
            
            #check if variable is declared 
            if loop_variable in variables:
                #check if variable is osf type NUMBR
                if variables[loop_variable]['data type'] == "NUMBR":
                    #no errors, perform the loop operation 
                    loop_tokens_code = loop_tokens[1:-1]
                    
                    loop_variable_value = variables[loop_variable]['value']
                    loop_expression_tokens = []
                    found_til_or_wile = False
                    
                    #get the tokens of the loop expression
                    for item in loop_tokens[0][1][1:]:
                        if found_til_or_wile:
                            loop_expression_tokens.append(item)
                        elif isinstance(item, tuple) and (item[0] == 'TIL' or item[0] == 'WILE'):
                            found_til_or_wile = True

                    #check if the expression is valid
                    if loop_expression_tokens[0][1] == "Comparison Operator":
                        # print("ETOOOO", loop_expression_tokens)
                        # print(variables)
                        evaluate = arithmetic_analyzer(loop_expression_tokens, loop_tokens[0][0], loop_expression, self)
                    else:
                        error_prompt(loop_tokens[0][0], "Invalid expression in loop.", self)
                        
                    loop_block_counter = 0
                    is_GTFO = False
                                
                    #Execute the loop based on the operation and repeat condition
                    while (repeat_keyword == "TIL" and evaluate == "FAIL") or \
                        (repeat_keyword == "WILE" and evaluate == "WIN"):
                        
                        #Execute loop code block 
                        for loop_code_line in loop_tokens_code:

                            classification = loop_code_line[1][0][1]
                            
                            if classification == "Break Keyword":
                                is_GTFO = True

                                break   

                            if re.match(oic_pattern, loop_code_line[1][0][0]):
                                oic_found = True
                            
                            if if_delimiter == True:
                                if loop_code_line[1][0][0] == "KTHXBYE" and oic_found == False:
                                    error_prompt(loop_code_line[0], "If-Else or Switch-Case Delimiter not found.", self)
                                    # print("Error in line ", loop_code_line[0], ": If-Else or Switch-Case Delimiter not found.")
                                    # exit(0)
                                if loop_code_line[1][0][0] == "OIC":
                                    print(loop_code_line)
                                    if_else_condition.append(loop_code_line)
                                    if_else_statement(content, line_global, self)
                                    condition_index = []
                                    if_delimiter = False
                                    oic_found = False
                                    if_else_condition = []
                                if_else_condition.append(loop_code_line)
                            elif switch_delimiter == True:
                                if loop_code_line[1][0][0] == "KTHXBYE" and oic_found == False:
                                    error_prompt(loop_code_line[0], "If-Else or Switch-Case Delimiter not found.", self)
                                    # print("Error in line ", loop_code_line[0], ": If-Else or Switch-Case Delimiter not found.")
                                    # exit(0)
                                if loop_code_line[1][0][0] == "OIC":
                                    switch_case_condition.append(loop_code_line)
                                    switch_case_analyzer(content, line_global, self)
                                    switch_delimiter = False
                                    oic_found = False
                                    switch_case_condition = []
                                    temp = 0
                                    default_case_index = 0
                                switch_case_condition.append(loop_code_line)
                            else:         
                                if classification == "Output Keyword":
                                    b = print_analyzer(loop_code_line[1:][0], loop_code_line[0], loop_block[loop_block_counter], self)
                                    
                                    if b is not None:
                                        # print(loop_code_line[1:])
                                        #console_dislay(b, self)
                                        print("THISSSSS",loop_code_line[0],": ", b)
                                elif classification == "Arithmetic Operator" or classification == "Boolean Operator" or classification == "Comparison Operator":
                                    b = arithmetic_analyzer(loop_code_line[1:][0], loop_code_line[0], loop_block[loop_block_counter], self)
                                    if b is not None:
                                        print("line", loop_code_line[0],": ", b)
                                elif classification == "Function Call keyword":
                                    tokens_loop = [loop_code_line[0]]
                                    
                                    for to_add in loop_code_line[1:][0]:
                                        tokens_loop.append(to_add)
                                    
                                    function_analyzer(loop_block[loop_block_counter], tokens_loop, self)
                                
                                # =============== IF ELSE STATEMENT ===============

                                elif classification == "If Keyword":
                                    if_keyword = True
                                    if if_delimiter == False:
                                        print(f"Error in line {loop_code_line[0]}: Error in If Delimiter found.")
                                        exit(0)
                                elif classification == "Else Keyword":
                                    else_keyword = True
                                    if if_delimiter == False:
                                        error_prompt(loop_code_line[0], "No If Delimiter found.", self)
                                        # print(f"Error in line {loop_code_line[0]}: Error in If Delimiter found .")
                                        # exit(0)
                                elif classification == "If Delimiter":
                                    if_else_condition.append(loop_code_line)
                                    if_delimiter = True

                                # =============== SWITCH CASE STATEMENT ===============
                                elif classification == "Case Keyword":
                                    case_keyword = True
                                    if switch_delimiter == False:
                                        error_prompt(loop_code_line[0], "No Switch-Case Delimiter found.", self)
                                        # print(f"Error in line {loop_code_line[0]}: No Switch-Case Delimiter found.")
                                        # exit(0)
                                elif classification == "Default Case Keyword":
                                    default_case_keyword = True
                                    if switch_delimiter == False:
                                        error_prompt(loop_code_line[0], "No Switch-Case Delimiter found.", self)
                                        # print(f"Error in line {loop_code_line[0]}: No Switch-Case Delimiter found.")
                                        # exit(0)
                                elif classification == "Switch-Case Delimiter":
                                    switch_case_condition.append(loop_code_line)
                                    # print("switchhh",tokens[0], removed_tuple)
                                    switch_delimiter = True
                                
                                else:
                                    # removed_comment = remove_comments(loop_block[loop_block_counter], loop_code_line)       
                                    if classification == 'Identifier':
                                        analyze(loop_block[loop_block_counter], loop_code_line[1][1][1], loop_code_line[0], loop_code_line[1:][0], self)
                                    else:
                                        analyze(loop_block[loop_block_counter], classification, loop_code_line[0], loop_code_line[1:][0], self)

                            #increment loop code block line
                            loop_block_counter += 1
                        
                        #break loop if GTFO is encountered
                        if is_GTFO == True:
                            break
                        
                        loop_block_counter = 0
                        
                        #Perform the loop operation
                        if loop_operation == "UPPIN":
                            variables[loop_variable]['value'] += 1
                        elif loop_operation == "NERFIN":
                            variables[loop_variable]['value'] -= 1
                                                
                        evaluate = arithmetic_analyzer(loop_expression_tokens, loop_tokens[0], loop_expression, self)

                else:
                    error_prompt(loop_tokens[0][0], f"Variable '{loop_variable}' is not of type NUMBR.", self)
                    # print(f"Error in line {loop_tokens[0][0]}: Variable '{loop_variable}' is not of type NUMBR.")
            else:
                error_prompt(loop_tokens[0][0], f"Variable '{loop_variable}' is not yet declared.", self)
                # print(f"Error in lineeeeee {loop_tokens[0][0]}: Variable '{loop_variable}' is not yet declared.")
        else:
            error_prompt(loop_tokens[len(loop_tokens)-1][0], f"Label '{loop_variable_end}' does not match loop label '{loop_label}'.", self)
            # print(f"Error in line {loop_tokens[len(loop_tokens)-1][0]}: Label '{loop_variable_end}' does not match loop label '{loop_label}'.")
    else:
        error_prompt(loop_tokens[0][0], "Incorrect format for loops.", self)
        print(f"Error in line {loop_tokens[0][0]}: Incorrect format for loops.")

    #Reset the necessary variables
    loop_lines = []
    loop_tokens = []

def variable_checker(var):
    if re.match(variable_pattern, var):
        return True
    else:
        return False

#This function checks the syntax of the function declarion.
#If there are no errors, the function is added to the global dictionary of functions        
def function_checker(self):
    global function_lines, function_tokens, functions
    
    function_match = re.match(function_pattern, function_lines[0])

    # Check if the syntax is correct
    if function_match:
        # print("FUCTION MATCHHHHH", function_tokens[0][0])
        #check if function delimeter is correct
        if re.fullmatch(r'IF U SAY SO *', function_lines[len(function_lines)-1]):
            #extract from line
            function_name = function_match.group(1)
            function_parameters = [param for param in function_match.groups()[1:] if param is not None]
            function_tokens_code = function_tokens[1:-1]
            
            check_parameters = []
            
            #check for duplicate parameter names
            for params in function_parameters:
                if params in check_parameters:
                    error_prompt(function_tokens[0][0], f"Parameter '{params}' already used.", self)
                    print(f"Error in line {function_tokens[0][0]}: Parameter '{params}' already used.")
                else:
                    check_parameters.append(params)
            
            # #check if parameters follow correct naming convention
            # for parameter in function_parameters:
            #     if variable_checker(parameter) == False:
            #         print(f"Error in line {function_tokens[0][0]}: Parameter '{parameter}' is not correctly declared.")
            
            #check if the key is already in the dictionary
            #if no errors, add function to dictionary
            if function_name not in functions:
                
                #check if there is no code block
                if len(function_lines[1:-1]) == 0:
                    print()
                    error_prompt(function_tokens[0][0], "Function has no code block.", self)
                    
                functions[function_name] = [function_parameters, function_lines[1:-1], function_tokens_code]
                # print("\n", functions)
            else:
                error_prompt(function_tokens[0][0], f"Function '{function_name}' already exists.", self)
                print(f"Error in line {function_tokens[0][0]}: Function '{function_name}' already exists.")
        else:
            error_prompt(function_tokens[len(function_tokens)-1][0], "Incorrect syntax for function delimeter.", self)
            print(f"Error in line {function_tokens[len(function_tokens)-1][0]}: Incorrect syntax for function delimeter.")
    else:
        error_prompt(function_tokens[0][0], "Incorrect format for functions.", self)
        print(f"Error in line {function_tokens[0][0]}: Incorrect format for functions.")
    
    #reset the the lists
    function_lines = []
    function_tokens = []

def var_in_param(code_block_tuple, function_parameters):
    # print(function_parameters)
    for first, second in code_block_tuple:
        if second == "Identifier":
            if first not in function_parameters:
                return False, first
    return True, None
 
#This functions calls and evaluates the function given that there are no errors   
def function_analyzer(line, tokens, self):
    
    global variables, is_loop, if_delimiter, oic_found, condition_index, if_else_condition, if_deli_index
    global if_keyword, else_keyword, case_keyword, default_case_keyword, switch_delimiter, switch_case_condition, temp, default_case_index


    temp_variables = variables.copy()
    parameter_number = 0
    param_expressions = []
    # print(line, tokens[0])
    # print("==================== FUNCTION ANALYZER ====================")
    function_line_number = tokens[0]
    # print("TOKENNNNNNNN", tokens)
    
    
    function_call_pattern = re.compile(
        r'I IZ ([a-zA-Z_][a-zA-Z_0-9]*)(?: YR ((?:' + combined_pattern_str + '))?(?: AN YR ((?:' + combined_pattern_str + '))?(?: AN YR ((?:' + combined_pattern_str + ')))?)?)? MKAY'
    )
    
    return_value = None
    has_return = False
    function_call_match = function_call_pattern.match(line)

    #check if syntax is correct
    if function_call_match:
        #extract from match
        function_name = function_call_match.group(1)

        #get parameters from line            
        # no parameters
        if len(tokens)-1 > 3:            
            for i in range(1, len(tokens)):
                if tokens[i][0] == 'YR':
                    parameter_number += 1
                if tokens[i][0] == 'AN':
                    if tokens[i][0] == 'YR':
                        parameter_number += 1
            next = 0
            temp = []    
            for i in range(parameter_number):
                if i == 0: 
                    for j in range(4, len(tokens)):
                        if (tokens[j][0] == 'AN' and tokens[j+1][0] == 'YR') or (tokens[j][0] == 'MKAY'):
                            next = j+2
                            param_expressions.append(' '.join(temp))
                            temp = []
                            break
                        else:
                            temp.append(tokens[j][0])
                else:
                    for k in range(next, len(tokens)):
                        if (tokens[k][0] == 'AN' and tokens[k+1][0] == 'YR') or (tokens[k][0] == 'MKAY'):
                            next = k+2
                            param_expressions.append(' '.join(temp))
                            temp = []
                            break
                        else:
                            temp.append(tokens[k][0])
        
        print("\nNDSKJGKJDFGKJDHFGJKHDFGK", param_expressions)
        function_parameters = {}
        
        #check if function exists
        if function_name in functions:
            #access the function from the global function dictionary
            access_function = functions[function_name]
            access_function_params = access_function[0]
            param_counter = 0
            
            #check if the number of parameters match
            if len(param_expressions) == len(access_function[0]):
                #add parameters to a list
                for expression in param_expressions:
                    
                    parameter_name = access_function_params[param_counter]
                    data_type = get_data_type(expression)
                    
                    #add to dictionary if float, int, boolean, or string
                    if data_type in ("NUMBAR", "NUMBR", "TROOF", "YARN"):
                        if data_type == "NUMBAR": 
                            expression = float(expression) 
                        elif data_type == "NUMBR": 
                            expression = int(expression) 
                            
                        #add to dictionary
                        function_parameters[parameter_name] = {"value": expression, "data type": data_type}
                    else: 
                        #if expression or variable
                        
                        #check if variable or expression
                        if len(expression.split(" ")) > 1:
                            #if expression
                            
                            # Split the expression into tokens
                            expression_tokens = expression.split(" ")
                            expression_tokens_final = []
                            new_value = None
                            current_token = ""
                            tokens_dict = dict(tokens[1:])

                            #get the tokens of the expression
                            for expr in expression_tokens:
                                current_token += " " + expr
                                current_token = current_token.strip()

                                if current_token in tokens_dict:
                                    expression_tokens_final.append((current_token, tokens_dict[current_token]))      
                                    current_token = ""
                            
                            new_classification = expression_tokens_final[0][1]
                            
                            #evaluate the expression
                            if new_classification == "Arithmetic Operator" or new_classification == "Boolean Operator" or new_classification == "Comparison Operator" or new_classification == "Infinite Arity Operator":
                                new_value = arithmetic_analyzer(expression_tokens_final, tokens[0], expression, self)
                                new_value = str(new_value)
                            else:
                                if new_classification == 'Identifier':
                                    # IEEDIT TO
                                    print("ETOOOOOOOOOOO", expression_tokens_final)
                                    new_value = analyze(expression, new_classification, tokens[0], expression_tokens_final, self)
                                else:
                                    new_value = analyze(expression, new_classification, tokens[0], expression_tokens_final, self)
                            
                            #get the data type of the evaluated expression
                            new_data_type = get_data_type(new_value)
                            if new_data_type in ("NUMBAR", "NUMBR", "TROOF", "YARN"):
                                if new_data_type == "NUMBAR": 
                                    new_value = float(new_value) 
                                elif new_data_type == "NUMBR": 
                                    new_value = int(new_value) 
                                    
                                #add to dictionary
                                function_parameters[parameter_name] = {"value": new_value, "data type": new_data_type}     
                        else:
                            # if variable
                            # check if variable exists
                            if expression in variables:
                                function_var_value = variables[expression]['value']
                                function_var_datatype = variables[expression]['data type']
                                function_parameters[parameter_name] = {"value": function_var_value, "data type": function_var_datatype}
                            else:
                                error_prompt(tokens[0], "Variable '{expression}' is not yet declared.", self)
                                # print(f"Error in line {tokens[0]}: Variable '{expression}' is not yet declared.") 
                                return
                    param_counter+=1
                
                variables = function_parameters
                line_counter = 0
                
                for code_block in access_function[2]:
                    # print("PUMASOK", code_block)
                    # existing, no_var = var_in_param(code_block[1:][0], function_parameters)
                    
                    code_line = access_function[1][line_counter]
                    code_line_number = code_block[0]
                    code_tuples = code_block[1]
                    keyword = code_tuples[0][1]

                    # =============== RETURN ===============
                    if keyword == "Return Keyword": 
                        if len(code_tuples) > 1:
                        #remove "FOUND YR" from code line
                            code_line = access_function[1][line_counter].replace("FOUND YR ", "")
                            code_tuples = code_tuples[1:]
                            keyword = code_tuples[0][1]
                            has_return = True
                            
                            #if not expression
                            if len(code_tuples) == 1:
                                check_expression = get_data_type(code_line.strip())
                                if check_expression == "ELSE":
                                    # check if variable exist
                                    if code_line.strip() in variables:
                                        return_value = str(variables[code_line.strip()]['value']) 
                                    else:
                                        # print(f"Error in line {code_line_number}: Variable '{code_line.strip()}' is not a function parameter.")
                                        error_prompt(code_line_number, f"Variable '{code_line.strip()}' is not a function parameter.", self)
                                else:
                                    return_value = str(code_line.strip())
                                break
                        else:
                            # FOUND YR has no expression
                            if 'IT' not in temp_variables:
                                temp_variables['IT'] = {'value': None, 'data type': 'NOOB'}
                            else:
                                temp_variables['IT']['value'] = None
                                temp_variables['IT']['data type'] = 'NOOB'
                            break
                    
                    # GTFO is encountered
                    if keyword == "Break Keyword":
                        if 'IT' not in temp_variables:
                            temp_variables['IT'] = {'value': None, 'data type': 'NOOB'}
                        else:
                            temp_variables['IT']['value'] = None
                            temp_variables['IT']['data type'] = 'NOOB'
                        break

                    # =============== LOOPS ===============
                    if keyword == "Loop Start Delimiter":
                        is_loop = True
                    #add the loop code to a list
                    if is_loop == True:    
                        print("codeline", code_line)
                        print("codelineeee", [code_line_number, code_tuples])
                        loop_lines.append(code_line)
                        loop_tokens.append([code_line_number, code_tuples])

                    #set is_loop to False and call loop analyzer
                    if keyword == "Loop End Delimiter":
                        is_loop = False
                        loop_analyzer(self)    

                    if not is_loop:
                        if re.match(oic_pattern, code_tuples[0][0]):
                            oic_found = True
                        if if_delimiter == True:

                            if code_tuples[0][0] == "KTHXBYE" and oic_found == False:
                                error_prompt(code_line_number, "If-Else or Switch-Case Delimiter not found.", self)
                                # print("Error in line ", code_line_number, ": If-Else or Switch-Case Delimiter not found.")
                                # exit(0)

                            if code_tuples[0][0] == "OIC":
                                if_else_condition.append(code_block)

                                if_else_statement(content,line_global, self)

                                # for i in range(len(if_else_condition)):
                                #     print("*",if_else_condition[i])

                                condition_index = []
                                if_delimiter = False
                                oic_found = False
                                if_else_condition = []

                            if_else_condition.append(code_block)
                        elif switch_delimiter == True:
                            if code_tuples[0][0] == "KTHXBYE" and oic_found == False:
                                error_prompt(code_line_number, "If-Else or Switch-Case Delimiter not found.", self)
                                # print("Error in line ", code_line_number, ": If-Else or Switch-Case Delimiter not found.")
                                # exit(0)
                            else:
                                if code_tuples[0][0] == "OIC":
                                    switch_case_condition.append(code_block)
                                    switch_case_analyzer(content, line_global, self)
                                    

                                    switch_delimiter = False
                                    oic_found = False
                                    switch_case_condition = []
                                    temp = 0
                                    default_case_index = 0
                            
                            switch_case_condition.append(code_block)
                        else:
                            # =============== PRINTING ===============
                            if keyword == "Output Keyword":
                                to_print = print_analyzer(code_tuples, code_line_number, line_global, self)
                                if to_print is not None:
                                    print("THISSSSS", code_line_number,": ", to_print)
                                    
                            # =============== ARITHMETIC OPERATIONS ===============
                            elif keyword == "Arithmetic Operator" or keyword == "Boolean Operator" or keyword == "Comparison Operator" or keyword == "Infinite Arity Operator":
                                return_value = arithmetic_analyzer(code_tuples, code_line_number, code_line, self)
                                return_value = str(return_value)

                            # =============== IF ELSE STATEMENT ===============
                            elif keyword == "If Keyword":
                                if_keyword = True
                                if if_delimiter == False:
                                    error_prompt(code_line_number, "No If Delimiter found.", self)
                                    # print(f"Error in line {code_line_number}: Error in If Delimiter found.")
                                    # exit(0)
                            elif keyword == "Else Keyword":
                                else_keyword = True
                                if if_delimiter == False:
                                    error_prompt(code_line_number, "No If Delimiter found.", self)
                                    # print(f"Error in line {code_line_number}: Error in If Delimiter found .")
                                    # exit(0)
                            elif keyword == "If Delimiter":
                                if_deli_index = access_function[2].index(code_block)
                                # print("THIS IS THE FORMAT", [code_line_number, code_tuples])
                                if_else_condition.append(code_block)
                                if_delimiter = True

                            # =============== SWITCH CASE STATEMENT ===============
                            elif keyword == "Case Keyword":
                                case_keyword = True
                                if switch_delimiter == False:
                                    error_prompt(code_line_number, "No Switch-Case Delimiter found.", self)
                                    # print(f"Error in line {code_line_number}: No Switch-Case Delimiter found.")
                                    # exit(0)
                            elif keyword == "Default Case Keyword":
                                default_case_keyword = True
                                if switch_delimiter == False:
                                    error_prompt(code_line_number, "No Switch-Case Delimiter found.", self)
                                    # print(f"Error in line {code_line_number}: No Switch-Case Delimiter found.")
                                    # exit(0)
                            elif keyword == "Switch-Case Delimiter":
                                switch_case_condition.append(code_block)
                                # print("switchhh",tokens[0], removed_tuple)
                                switch_delimiter = True
                            else:
                                # =============== TYPECASTING ===============
                                if keyword == 'Identifier':
                                    return_value = analyze(code_line, code_tuples[1][1], code_line_number, code_tuples, self)
                                else:
                                    # =============== CONCATENATION AND ASSIGNMENT ===============
                                    return_value = analyze(code_line, keyword, code_line_number, code_tuples, self)
                        
                        # TO ADD:
                        # 1. IF ELSE
                        # 2. SWITCH
                        # 3. INPUT
                    
                    if has_return == True:
                        break
                    
                    line_counter+=1        
            else:
                error_prompt(function_line_number, "Number of parameters do not match.", self)
                # print(f"Error in line {function_line_number}: Number of parameters do not match.")
        else:
            error_prompt(function_line_number, f"Function '{function_name}' not yet declared.", self)
            # print(f"Error in line {function_line_number}: Functionnnnnnnnnnn '{function_name}' not yet declared.")
    else:
        error_prompt(function_line_number, "Incorrect format for function call.", self)
    
    if has_return == True:
        #no error
        print("return to dibaaaaaa", return_value)
        if return_value != None:
            
            return_value_type = get_data_type(return_value)
            if return_value_type in ("NUMBAR", "NUMBR", "TROOF", "YARN"):
                if return_value_type == "NUMBAR": 
                    return_value = float(return_value) 
                elif return_value_type == "NUMBR": 
                    return_value = int(return_value)                 
            if 'IT' not in temp_variables:
                temp_variables['IT'] = {'value': return_value, 'data type': return_value_type}
            else:
                temp_variables['IT']['value'] = return_value
                temp_variables['IT']['data type'] = return_value_type
        else:
            if 'IT' not in temp_variables:
                temp_variables['IT'] = {'value': return_value, 'data type': "NOOB"}
            else:
                temp_variables['IT']['value'] = return_value
                temp_variables['IT']['data type'] = "NOOB"
    
    #reset the variables back
    #function_var.update(function_parameters)
    variables = temp_variables
    
    
    return return_value

def switch_case_analyzer(content, lines, self):
    global switch_case_condition, temp, default_case_index, is_loop


    print(switch_case_condition)

    # check the existence of omg and omgwtf keywords and their respective codeblocks
    case_keywords = [i for i, x in enumerate(switch_case_condition) if x[1][0][1] == "Case Keyword"]
    else_keywords = [i for i, x in enumerate(switch_case_condition) if x[1][0][1] == "Default Case Keyword"]

    # if either the length of case_keywords or else_keywords is 0, then there is no respective keyword found
    if len(case_keywords) == 0:
        error_prompt(switch_case_condition[0][0], "No Case Keyword found.", self)
        # print(f"Error in line {switch_case_condition[0][0]}: No Case Keyword found.")
        # exit(0)
    if len(else_keywords) == 0:
        pass

    # check if the case and else keywords have codeblocks
    for i in case_keywords:
        if i+1 >= len(switch_case_condition) or switch_case_condition[i+1][1][0][1] in ["If-Else or Switch-Case Delimiter", "Default Case Keyword"]:
            error_prompt(switch_case_condition[i][0], "'OMG' has no code block.", self)
            # print(f"Error in line {switch_case_condition[i][0]}: 'OMG' has no code block.")
            # exit(0)

    for i in else_keywords:
        if i+1 >= len(switch_case_condition) or switch_case_condition[i+1][1][0][1] in ["If-Else or Switch-Case Delimiter", "Default Case Keyword"]:
            error_prompt(switch_case_condition[i][0], "'OMGWTF' has no code block.", self)
            # print(f"Error in line {switch_case_condition[i][0]}: 'OMGWTF' has no code block.")
            # exit(0)

    if 'IT' not in variables:
        # print(if_else_condition)
        error_prompt(switch_case_condition[0][0], "Accessing a null value.", self)
        # print(f"Error in line {if_else_condition[0][0]}: Accessing a null value.")
        # exit(0)

    # match = re.match(literal_pattern, switch_case_condition[1][1][1][0])
    # print("*&&*",  switch_case_condition[1][1][1][0])
    # this algo is for the OMG keyword where it will check if the value of IT is equal to the value literal
    # if variables['IT']['value'] == 'WIN':
    #     pass
    # match = literal_pattern.match(switch_case_condition[1][1][1][0])
    # if match:

    # else:
    #     # for i in range(len(switch_case_condition)):
    #     #     print("*",switch_case_condition[i])
    #     print(f"Error in line {switch_case_condition[1][0]}: Invalid value format for OMG. Value must only be a yarn, troof, numbr, or numbar.")
    #     exit(0)
        # print("OK VALID FORMAT")
        
        
        # print(type(temp))
    switch_case_condition_newformat = [[item[0]] + item[1] if len(item) > 1 else [item[0]] for item in switch_case_condition]
    print(switch_case_condition_newformat)
    
    # get the code to execute
    for code_block in range(1, len(switch_case_condition)):
        if switch_case_condition[code_block][1][0][1] ==  "Case Keyword":
            match = re.match(literal_pattern, switch_case_condition[code_block][1][1][0])
            # print("OMG**", switch_case_condition[code_block][1][1][0])
            print("&*^%", switch_case_condition[code_block][1][1][0])
            if match:
                print("hre")
                print(switch_case_condition[code_block][1][0][1])
                if switch_case_condition[code_block][1][1][1] == "NUMBR Literal":
                    temp = int(switch_case_condition[code_block][1][1][0])
                elif switch_case_condition[code_block][1][1][1] == "NUMBAR Literal":
                    temp = float(switch_case_condition[code_block][1][1][0])
                else:
                    temp = switch_case_condition[code_block][1][1][0]
                print("temp",temp)
                
                if temp == variables['IT']['value']:
                    print("MATCH", switch_case_condition[code_block][1][1][0])

                    print("ENTERED HERE")
                    # print("check switch here",switch_case_condition[1][1][1][0], variables['IT']['value'])
                    # if switch_case_condition[2][1][0][1] == "Arithmetic Operator" or  switch_case_condition[2][1][0][1] == "Boolean Operator":
                    #     pass
                    for i in range(code_block+1, len(switch_case_condition)):
                        
                        # print(switch_case_condition[i][1][0][1])
                        if switch_case_condition[i][1][0][1] ==  "Case Keyword" or switch_case_condition[i][1][0][1] ==  "If-Else or Switch-Case Delimiter" or switch_case_condition[i][1][0][1] == "Default Case Keyword":
                            return
                        else:


                            removed_comment = remove_comments(content[switch_case_condition[i][0]-1], switch_case_condition[i][1:])
                            # print("REMOVED DAPAT:::::::::::", removed_comment)
                            
                            # =============== LOOPS ===============
                            if switch_case_condition[i][1][0][1] == 'Loop Start Delimiter':
                                is_loop = True
                                # print("CHECKINGGGGGGGGGGG", switch_case_condition[i][1][0][1])
                            
                            #add the loop code to a list
                            if is_loop == True:   
                                loop_lines.append(removed_comment)
                                loop_tokens.append([switch_case_condition_newformat[i][0], switch_case_condition_newformat[i][1:]])
                            
                            #set is_loop to False and call loop analyzer
                            if switch_case_condition[i][1][0][1] == "Loop End Delimiter":
                                is_loop = False
                                loop_analyzer(self)
                            
                            if not is_loop:
                                if switch_case_condition[i][1][0][1] == "Break Keyword":
                                    break
                                elif switch_case_condition[i][1][0][1] == "Arithmetic Operator" or switch_case_condition[i][1][0][1] == "Boolean Operator" or switch_case_condition[i][1][0][1] == "Comparison Operator":
                                    # print(f'yooo {switch_case_condition[i][0]}')
                                    b = arithmetic_analyzer(switch_case_condition[i][1][0:], switch_case_condition[i][0], lines, self)
                                    
                                    # print("check to pls", switch_case_condition[i][1][0:], switch_case_condition[i][0])
                                    if b is not None:
                                        print("line",switch_case_condition[i][0],": ", b)
                                    # print("hereee", b)
                                elif switch_case_condition[i][1][0][1] == "Output Keyword":
                                    # print(f'{content[switch_case_condition[i][0]-1]}\n{switch_case_condition_newformat[i]}')

                                    b = print_analyzer(switch_case_condition[i][1][0:], switch_case_condition[i][0], line_global, self)
                                    if b is not None:
                                        print("line",switch_case_condition[i][0],": ", b)
                                elif switch_case_condition[i][1][0][1] == "Function Call keyword":
                                    # print(f'{content[switch_case_condition[i][0]-1]}\n{switch_case_condition_newformat[i]}')
                                    function_analyzer(content[switch_case_condition[i][0]-1], switch_case_condition_newformat[i], self)

                                else:
                                    
                                    # print("d222",removed_comment, switch_case_condition[i][1][0][1], switch_case_condition[i][0], switch_case_condition[i][1:])
                                    # print(f'{removed_comment}\n{switch_case_condition[i][1][0][1]}\n{switch_case_condition[i][0]}\n{switch_case_condition[i][1][0:]}')
                                    if switch_case_condition[i][1][0][1] == 'Identifier':
                                        analyze(removed_comment, switch_case_condition[i][1][1][1], switch_case_condition[i][0], switch_case_condition[i][1][0:], self)
                                    else:
                                        analyze(removed_comment, switch_case_condition[i][1][0][1], switch_case_condition[i][0], switch_case_condition[i][1][0:], self)
                                    # print(f'{removed_comment}\n{switch_case_condition[i][1][0][1]}\n{switch_case_condition[i][0]}\n{switch_case_condition[i][1][0:]}')
                else:
                    pass      
            else:
                error_prompt(switch_case_condition[1][0], "Invalid value format for OMG. Value must only be a yarn, troof, numbr, or numbar.", self)
                # print(f"Error in line {switch_case_condition[1][0]}: Invalid value format for OMG. Value must only be a yarn, troof, numbr, or numbar.")
                # exit(0)
        else:
            pass

    
        
    default_case_index = None

    for i in range(len(switch_case_condition)):
        if switch_case_condition[i][1][0][1] == "Default Case Keyword":
            default_case_index = i
            break

    # print("heyy",default_case_index)
    # print("do the code block for omgwtf here")
    for i in range(default_case_index+1, len(switch_case_condition)):
        
        # print(switch_case_condition[i][1][0][1])
        if switch_case_condition[i][1][0][1] ==  "If-Else or Switch-Case Delimiter":
            break
        else:
            # print(i)
            if switch_case_condition[i][1][0][1] == "Break Keyword":
                break
            elif switch_case_condition[i][1][0][1] == "Arithmetic Operator" or switch_case_condition[i][1][0][1] == "Boolean Operator" or switch_case_condition[i][1][0][1] == "Comparison Operator":
                # print(f'yooo {switch_case_condition[i][0]}')
                b = arithmetic_analyzer(switch_case_condition[i][1][0:], switch_case_condition[i][0], lines, self)
                
                # print("check to pls", switch_case_condition[i][1][0:], switch_case_condition[i][0])
                if b is not None:
                    print("line",switch_case_condition[i][0],": ", b)
                # print("hereee", b)
            elif switch_case_condition[i][1][0][1] == "Output Keyword":
                # print(f'{content[switch_case_condition[i][0]-1]}\n{switch_case_condition_newformat[i]}')

                b = print_analyzer(switch_case_condition[i][1][0:], switch_case_condition[i][0], line_global, self)
                if b is not None:
                    print("line",switch_case_condition[i][0],": ", b)
            elif switch_case_condition[i][1][0][1] == "Function Call keyword":
                # print(f'{content[switch_case_condition[i][0]-1]}\n{switch_case_condition_newformat[i]}')
                function_analyzer(content[switch_case_condition[i][0]-1], switch_case_condition_newformat[i], self)
            else:

                # print(i)

                removed_comment = remove_comments(content[switch_case_condition[i][0]-1], switch_case_condition[i][1:])
                
                # =============== LOOPS ===============
                if switch_case_condition[i][1][0][1] == 'Loop Start Delimiter':
                    is_loop = True
                    # print("CHECKINGGGGGGGGGGG", switch_case_condition[i][1][0][1])
                
                #add the loop code to a list
                if is_loop == True:   
                    loop_lines.append(removed_comment)
                    loop_tokens.append([switch_case_condition_newformat[i][0], switch_case_condition_newformat[i][1:]])
                
                #set is_loop to False and call loop analyzer
                if switch_case_condition[i][1][0][1] == "Loop End Delimiter":
                    is_loop = False
                    loop_analyzer(self)
                                
                if not is_loop:
                    if switch_case_condition[i][1][0][1] == "Break Keyword":
                        break
                    elif switch_case_condition[i][1][0][1] == "Arithmetic Operator" or switch_case_condition[i][1][0][1] == "Boolean Operator" or switch_case_condition[i][1][0][1] == "Comparison Operator":
                        # print(f'yooo {switch_case_condition[i][0]}')
                        b = arithmetic_analyzer(switch_case_condition[i][1][0:], switch_case_condition[i][0], lines, self)
                        
                        # print("check to pls", switch_case_condition[i][1][0:], switch_case_condition[i][0])
                        if b is not None:
                            print("line",switch_case_condition[i][0],": ", b)
                        # print("hereee", b)
                    elif switch_case_condition[i][1][0][1] == "Output Keyword":
                        # print(f'{content[switch_case_condition[i][0]-1]}\n{switch_case_condition_newformat[i]}')

                        b = print_analyzer(switch_case_condition[i][1][0:], switch_case_condition[i][0], line_global, self)
                        if b is not None:
                            print("line",switch_case_condition[i][0],": ", b)
                    elif switch_case_condition[i][1][0][1] == "Function Call keyword":
                        # print(f'{content[switch_case_condition[i][0]-1]}\n{switch_case_condition_newformat[i]}')
                        function_analyzer(content[switch_case_condition[i][0]-1], switch_case_condition_newformat[i], self)
                    else:
                        # removed_comment = remove_comments(content[switch_case_condition[i][0]-1], switch_case_condition[i][1:])
                        # print("d222",removed_comment, switch_case_condition[i][1][0][1], switch_case_condition[i][0], switch_case_condition[i][1:])
                        # print(f'{removed_comment}\n{switch_case_condition[i][1][0][1]}\n{switch_case_condition[i][0]}\n{switch_case_condition[i][1][0:]}')
                        if switch_case_condition[i][1][0][1] == 'Identifier':
                            analyze(removed_comment, switch_case_condition[i][1][1][1], switch_case_condition[i][0], switch_case_condition[i][1][0:], self)
                        else:
                            analyze(removed_comment, switch_case_condition[i][1][0][1], switch_case_condition[i][0], switch_case_condition[i][1][0:], self)
                        # print(f'{removed_comment}\n{switch_case_condition[i][1][0][1]}\n{switch_case_condition[i][0]}\n{switch_case_condition[i][1][0:]}')
            # default_case_index = None



    

#TOKENIZE INPUTTED CODE
def tokenize(self):
    global to_remove, if_delimiter, oic_found, if_keyword,else_keyword, inside_wazzup_buhbye, if_else_condition, wazzup_line, condition_index 
    global loop_lines, is_loop, is_function, function_lines, loop_tokens, function_tokens
    global switch_delimiter, switch_case_condition, temp, default_case_index, case_keyword, default_case_keyword, is_loop_del, is_function_del
    global line_global, content
    no_num_all_tokens = []
    all_tokens = []
    
    # multiple_index = []

    # Remove empty strings from the list
    filtered_list = [item for item in content if item != ""]
    filtered_list_removed_comments = [item.strip() for item in filtered_list if not item.startswith("BTW")]

    # Create filtered_list_removed_blocks excluding elements between "OBTW" and "TLDR"
    in_block = False
    filtered_list_removed_blocks = []

    for item in filtered_list_removed_comments:
        if item.startswith("OBTW"):
            in_block = True
        elif item.startswith("TLDR"):
            in_block = False
        elif not in_block:
            filtered_list_removed_blocks.append(item)

    
    # print(filtered_list)
    #check if the lol code starts with HAI and ends with KTHXBYE
    # if filtered_list[0] != "HAI":
    if not re.fullmatch(r'HAI *', filtered_list_removed_blocks[0]):
        error_prompt(1, "Code delimiter not existing. Should start with HAI", self)
    # if filtered_list[len(filtered_list)-1] != "KTHXBYE":
    if not re.fullmatch(r'KTHXBYE *', filtered_list_removed_blocks[len(filtered_list_removed_blocks)-1]):
        error_prompt(len(content), "Code delimiter not existing. Should end with KTHXBYE", self)
    
    # Count occurrences of 'HAI' and 'WAZZUP'
    count_hai = filtered_list_removed_blocks.count('HAI')
    count_wazzup = filtered_list_removed_blocks.count('WAZZUP')

    if count_hai != 1:
        error_prompt(1, "HAI should occur once.", self)
    elif count_wazzup != 1:
        error_prompt(len(content), "WAZZUP should occur once at the end.", self)
    
    multi_line = False
    line_number = 1
    initial_multiline = True
    inserted = False
    current_line_r = 0
    
    for lines in content:
        #print("line", line_number,": ", lines)
        lines = lines.lstrip()
        #print("line", line_number,": ", lines)
        #print(f"line {line_number}: {lines}")
        # print("ok",lines)
        tokens = []
        tokens.append(line_number)
        next_line = 0
        lines_split = lines.strip().split(" ")
        # print("===", lines_split)
        potential = False
        last = lines_split[-1]
        line_global = lines
        
        if(multi_line == False):
            to_check = ""

        # print(last)
        if(next_line == 0):
            for word in lines_split:
                #check if last word
                if(word == last):
                    next_line = 1
                    
                if(to_check == ""):
                    to_check = word
                else:
                    to_check = to_check + " " +  word 
                
                for key, value in keywords.items():
                    if to_check == key:
                        # print("======================TOCHECK:", to_check, line_number)
                        
                        #if current to_check is R
                        if to_check == "R":
                            current_line_r = line_number
                        
                        if line_number!=1 and line_number==current_line_r:
                            if to_check == "MAEK": 
                                # print("=============R MAEKK========")
                                tokens.append(("R MAEK", "Reassignment Operator"))
                                
                                # #pop the tuple with R from the tokens 
                                tokens.remove(("R", "Assignment Operator"))
                                to_check = ""
                                break
                                
                        tokens.append((key, value))   
                        to_check = ""
                        potential = False
                        break
                    
                #check if the current string is a potential keyword
                if(to_check in potential_keyword):
                    potential = True
                
                # Check if the string matches any key in the dictionary
                if(potential == True):
                    for key, value in keywords.items():
                        if to_check == key:
                            tokens.append((key, value))
                            to_check = ""
                            potential = False
                            break
                        
                if(potential == False):   
                    #check if single line comment
                    if re.search(r'^\s*BTW\b', to_check):
                        if(next_line == 1):
                            tokens.append(("BTW", "Single Line Comment Declaration"))
                            if to_check.strip() != "BTW":
                                tokens.append((to_check.replace("BTW ", ""), "Single Line Comment"))
                        continue
                    
                    #check if multi-line comment
                    if re.search(r'OBTW\b', to_check):
                        multi_line = True
                        if initial_multiline:
                            tokens.append(("OBTW", "Multi-Line Comment Declaration"))
                            if next_line == 1 and not to_check != r'OBTW\b':
                                tokens.append((to_check.replace("OBTW ", ""), "Multi-Line Comment"))
                                inserted = True
                                # to_check = "OBTW "
                            line_before = to_check
                            initial_multiline = False
                        else:
                            if to_check.find("TLDR") != -1:
                                modified_string = to_check.replace("OBTW", "").replace("TLDR", "")
                                found = False
                                
                                #find if the the comment is included
                                for inner_list in all_tokens:
                                    for element in inner_list[1:]:  # Skip the first element (integer)
                                        if any(isinstance(item, str) and modified_string in item for item in element):
                                            found = True
                                            break
                                        
                                if not found and not inserted:
                                    tokens.append((modified_string.strip(), "Multi-Line Comment"))

                                tokens.append(("TLDR", "Multi-Line Comment Delimiter"))
                                multi_line = False
                                initial_multiline = True
                                inserted = False
                                to_check = ""
                            else:
                                if(next_line == 1):
                                    tokens.append((to_check.replace(line_before, "").strip(), "Multi-Line Comment"))
                                    inserted = True
                                    line_before = to_check
                        continue

                    #check if it is a string literal
                    if re.match(string_literal, to_check):
                        tokens.append((to_check, "String Literal"))
                        to_check = ""
                    
                    #check if it is a bool
                    if re.match(bool_literal, to_check):
                        tokens.append((to_check, "Boolean"))
                        to_check = ""
                    
                    #check if it is a type literal
                    if re.match(type_literal, to_check):
                        tokens.append((to_check, "Type Literal"))
                        to_check = ""
                    
                    if re.match(literals[0], to_check):
                        tokens.append((to_check, "NUMBR Literal"))
                        to_check = ""
                        
                    if re.match(literals[1], to_check):
                        tokens.append((to_check, "NUMBAR Literal"))
                        to_check = ""
                        
                    if re.match(identifier, to_check):
                        tokens.append((to_check, "Identifier"))
                        to_check = ""
            # print("HEREEEEEEEEEEEEEEEEE:")
            # print(tokens)
            # # line_number += 1
            # # all_tokens.append(tokens)
                    
            #check if tokens is not empty and there are no comment errors
            if len(tokens) > 1 and not check_comment_errors(lines, line_number, self):
                
                #remove comments from the tuple of lexemes
                if tokens[1][1] not in to_remove:
                    removed_tuple = [tup for tup in tokens[1:] if tup[1] not in to_remove]
                    """ print(removed_tuple)
                    if removed_tuple[0][0] != "HAI":
                        error_prompt(1, "Code delimiter not existing. Should start with HAI", self)
                    elif removed_tuple[-1][0] != "KTHXBYE":
                        error_prompt(len(filtered_list), "Code delimiter not existing. Should end with KTHXBYE", self)
 """
                else:
                    # EDITED THIS
                    line_number += 1
                    all_tokens.append(tokens)
                    continue
                    # print('TOKENNNSSS', tokens)
                    # continue
                
                # print('removed_tuple', removed_tuple)
                    # print("REMOVEDDDDD!", tokens[1][1])
                # else:
                #     print("")
                #     removed_tuple = tokens[1]
                # print("ETOOOOOO:",removed_tuple)

                # checks if the if else or switch case has delimiter
                if re.match(oic_pattern, removed_tuple[0][0]):
                    oic_found = True

                if if_delimiter == True:
                    if removed_tuple[0][0] == "KTHXBYE" and oic_found == False:
                        error_prompt(line_number, "If-Else or Switch-Case Delimiter not found.", self)
                    if removed_tuple[0][0] == "OIC":
                        if_else_condition.append([tokens[0], removed_tuple])
                        if_else_statement(content, lines, self)

                        # for i in range(len(if_else_condition)):
                        #     print("*",if_else_condition[i])

                        condition_index = []
                        if_delimiter = False
                        oic_found = False
                        if_else_condition = []

                        # print(condition_index, if_delimiter, oic_found)

                    if_else_condition.append([tokens[0], removed_tuple])

                elif switch_delimiter == True:
                    if removed_tuple[0][0] == "KTHXBYE" and oic_found == False:
                        error_prompt(line_number, "If-Else or Switch-Case Delimiter not found.", self)
                    else:
                        if removed_tuple[0][0] == "OIC":
                            switch_case_condition.append([tokens[0], removed_tuple])
                            switch_case_analyzer(content, lines, self)
                            

                            switch_delimiter = False
                            oic_found = False
                            switch_case_condition = []
                            temp = 0
                            default_case_index = 0
                    
                    switch_case_condition.append([tokens[0], removed_tuple])
                else:
                    # print(tokens[1][0])
                    removed_comment = remove_comments(lines, tokens)
                    # print("ETOOOOOOOOOOOOOOOOO NA TALAGAAAA", removed_comment)
                    
                    #=======================LOOPS=======================
                    if tokens[1][0] == "IM IN YR" and is_function == False:
                        is_loop = True
                    
                    #add the loop code to a list
                    if is_loop == True:    
                        loop_lines.append(removed_comment)
                        loop_tokens.append([line_number, removed_tuple])
                        # continue


                    # tabbed this
                        #set is_loop to False and call loop analyzer
                        if tokens[1][0] == "IM OUTTA YR" and is_function == False:
                            # print("Pumasok baaaaaaaaaaaaaa")
                            is_loop = False
                            is_loop_del = True
                            loop_analyzer(self)
                            is_loop_del = False
                        
                        if tokens[1][0] == "KTHXBYE" and is_loop_del == False:
                            error_prompt(loop_tokens[0][0], "Loop has no ending delimeter.", self)
                    
                    #=======================FUNCTION=======================

                    if tokens[1][0] == "HOW IZ I" and is_loop == False:
                        # print('ETO  BAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
                        is_function = True
                    
                    #add the function code to a list
                    if is_function == True:
                        # print('ETO  BAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA', is_function)
                        function_lines.append(removed_comment)
                        function_tokens.append([line_number, removed_tuple])
                        # continue
                    
                        #set is_function to False and call function analyzer
                        if tokens[1][0] == "IF U SAY SO":
                            # print('ETO  BAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA if you say', is_function)
                            is_function = False
                            is_function_del = True 
                            function_checker(self)
                            is_function_del = False
                        
                        if tokens[1][0] == "KTHXBYE" and is_function_del == False:
                            error_prompt(function_tokens[0][0], "Function has no ending delimeter.", self)
                    

                    if tokens[1][0] == "I IZ" and is_loop == False and is_function == False:
                        function_analyzer(removed_comment, tokens, self)
                    
                    if is_function or is_loop == True:
                        line_number += 1
                        all_tokens.append(tokens)
                        continue
                    
                    #=======================ARITHMETIC OPERATIONS=======================    
                    if tokens[1][1] == "Arithmetic Operator" or tokens[1][1] == "Boolean Operator" or tokens[1][1] == "Comparison Operator" or tokens[1][1] == "Infinite Arity Operator":

                        # this is to ensure that the wazzup and buhbye block only contains variable declaration 
                        # also, this checks whether the wazzup has corresponding buhbye, and vice versa
                        
                        
                        b = arithmetic_analyzer(removed_tuple, tokens[0], lines, self)
                        #print("ETOOOOOOOOOOOOOO")
                        #print("removed_tuple", removed_tuple)
                        #print("tokens[0]", tokens[0])
                        #print("lines", lines)
                        if b is not None:
                            print("line",tokens[0],": ", b)
                    elif tokens[1][1] == "Output Keyword":
                        b = print_analyzer(removed_tuple, tokens[0], lines, self)
                        if b is not None:
                            print("line",tokens[0],": ", b)
                            #console_dislay(b, self)
                    # this is a condition when if keyword is found but no if delimiter  
                    elif tokens[1][1] == "If Keyword":
                        if_keyword = True
                        if if_delimiter == False:
                            error_prompt(line_number, "Error in If Delimiter found.", self)
                    elif tokens[1][1] == "Else Keyword":
                        else_keyword = True
                        if if_delimiter == False:
                            error_prompt(line_number, "Error in If Delimiter found", self)
                    # sets the flag to true when if delimiter is found
                    elif tokens[1][1] == "If Delimiter":
                        
                        if_else_condition.append([tokens[0], removed_tuple])
                        if_delimiter = True

                    elif tokens[1][1] == "Case Keyword":
                        case_keyword = True
                        if switch_delimiter == False:
                            error_prompt(line_number, "No Switch-Case Delimiter found.", self)
                    elif tokens[1][1] == "Default Case Keyword":
                        default_case_keyword = True
                        if switch_delimiter == False:
                            error_prompt(line_number, "No Switch-Case Delimiter found.", self)
                    elif tokens[1][1] == "Switch-Case Delimiter":
                        switch_case_condition.append([tokens[0], removed_tuple])
                        # print("switchhh",tokens[0], removed_tuple)
                        switch_delimiter = True
                    else:
                        # removed_comment = remove_comments(lines, tokens)
                        # print("check no comment", removed_comment)
                        if tokens[1][1] == 'Identifier':
                            # print()
                            analyze(removed_comment, tokens[2][1], tokens[0], tokens[1:], self)
                        else:
                            analyze(removed_comment, tokens[1][1], tokens[0], tokens[1:], self)

            if is_error == True:
                break
            
            app.symbol_table.update(variables)
            #print(f"VARIABLES: {variables}")
            #app.symbol_table.add_function_variables(function_var)
            line_number += 1
            all_tokens.append(tokens)
    #app.symbol_table.add_function_variables(function_var)
    return all_tokens

def reset_flags():
    global app, is_error, function_var, obtw, wazzup, hai, multi_line, obtw_line, comments, comments_next, inside_wazzup_buhbye, if_delimiter, oic_found, if_keyword, else_keyword, wazzup_line, variables, functions, if_else_condition, condition_index, loop_lines, loop_tokens, is_loop, is_var_assignment, function_lines, function_tokens, is_function, switch_delimiter, switch_case_condition, temp, default_case_index, case_keyword, default_case_keyword
    global is_loop_del, is_function_del, if_deli_index, content, line_global
    # flags
    obtw = False
    wazzup = False
    hai = False
    multi_line = False
    obtw_line = 0
    comments = False
    comments_next = False
    inside_wazzup_buhbye = False
    if_delimiter = False
    oic_found = False
    if_keyword = False
    else_keyword = False
    wazzup_line = 0
    variables = {}
    functions = {}
    if_else_condition = []
    condition_index = []
    loop_lines = []
    is_loop_del = False
    is_function_del = False
    loop_tokens = []
    content = None
    is_loop = False
    is_var_assignment = False
    app = app
    is_error = False
    if_deli_index = 0
    line_global = None

    #for function
    function_lines =  []
    function_tokens = []
    is_function = False
    function_var = {"FUNCTION VARIABLES": {'value': " ", 'data type': ""}}

    #for switch case
    switch_delimiter = False
    switch_case_condition = []
    temp = 0
    default_case_index = 0
    case_keyword = False
    default_case_keyword = False

def main():
    file_name_lol = False
    file_name = ""

    while not file_name_lol:
        # file_name = input("Enter filename: ")
        file_name = "try.lol"

        if(file_name[-4:] == ".lol"):
            file_name_lol = True
    
    #get the contents of the lol code
    content = readFile(file_name)


    print("\n====================VARIABLES====================")
    for key, value in variables.items():
        print(f"{key}\n\tValue: {value['value']}, Data Type: {value['data type']}")
    print("\n")

    # print("\n====================Tokens====================")
    # for token in tokens:
    #     print(token)
    
    # print('thisssssssssssssssssssssssssssssssssssssssss')
    # print(variables)
    
    # print('functionsssssss')

    # for func in functions.items():
    #     print(func)

    # print("\n====================LEXEME====================")
    # print("LEXEME\t\t\tIDENTIFIER")
    
    # # #get only the tuples from the list
    # only_tuples = [item for sublist in tokens for item in sublist if isinstance(item, tuple)]
    
    # # #get the max width of each column
    # col_wid = [max(map(len, map(str, col))) for col in zip(*only_tuples)]

    # for row in only_tuples:
    #     print("\t\t\t".join(str(value).ljust(width) for value, width in zip(row, col_wid))) 

def show_content(file_path, self):

        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
                
        self.code_editor.text_widget.delete("1.0", tk.END)
        self.code_editor.text_widget.insert(tk.END, content)
        return

class CodeEditor(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid(row=1, column=0, sticky="nsew")
        self.label = tk.Label(self, text="Text Editor")
        self.label.pack()

        self.text_widget = tk.Text(self, wrap="word", undo=True)
        self.text_widget.pack(fill="both", expand=True)

class LexemeTable(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid(row=1, column=1, sticky="nsew")
        self.label = tk.Label(self, text="Lexeme Table")
        self.label.pack()

        self.treeview = ttk.Treeview(self)
        self.treeview["columns"] = ("Lexeme", "Classification")
        self.treeview.heading("Lexeme", text="Lexeme")
        self.treeview.column("Lexeme", anchor="w", width=150)  # Adjusted anchor to "w"
        self.treeview.heading("Classification", text="Classification")
        self.treeview.column("Classification", anchor="w", width=200)  # Adjust width as needed
        self.treeview.pack(fill="both", expand=True)

    def populate(self, lexeme_list):
        #print(lexeme_list)
        #no_num = [token for token in lexeme_list if len(token) > 1]
        #lexemes = [element for sublist in no_num for element in sublist[1] if len(sublist) > 1]
        nested_list = [item[1:] for item in lexeme_list if len(item) > 1]
        new_list = [element for sublist in nested_list for element in sublist]

        for idx, (lexeme, category) in enumerate(new_list, start=1):
            self.treeview.insert("", idx, values=(lexeme, category))

    def clear(self):
        for item in self.treeview.get_children():
            self.treeview.delete(item)

class SymbolTable(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid(row=1, column=2, sticky="nsew")
        self.label = tk.Label(self, text="Symbol Table")
        self.label.pack()
        self.treeview = ttk.Treeview(self)
        self.treeview["columns"] = ("Identifier", "Value")
        self.treeview.heading("Identifier", text="Identifier")
        self.treeview.column("Identifier", anchor="center", width=100)
        self.treeview.heading("Value", text="Value")
        self.treeview.column("Value", anchor="center", width=100)
        self.treeview.pack(fill="both", expand=True)
    
    def populate(self, symbol_dict):
        for idx, (identifier, info_dict) in enumerate(symbol_dict.items(), start=1):
            value = info_dict.get('value', '')  # Get the value from the 'value' key or use an empty string if not present
            self.treeview.insert("", idx, values=(identifier, value))

    def clear(self):
        for item in self.treeview.get_children():
            self.treeview.delete(item)

    def update(self, symbol_dict):
        for item in self.treeview.get_children():
            self.treeview.delete(item)
            
        for idx, (identifier, info_dict) in enumerate(symbol_dict.items(), start=1):
            value = info_dict.get('value', '')  # Get the value from the 'value' key or use an empty string if not present
            self.treeview.insert("", idx, values=(identifier, value))
        
        #self.treeview.insert("", 'end', values=("LOL", "value"))

    def add_function_variables(self, symbol_dict):
        #print(symbol_dict)
        for idx, (identifier, info_dict) in enumerate(symbol_dict.items(), start=1):
            value = info_dict.get('value', '')
            self.treeview.insert("", 'end', values=(identifier, value))
        
        #self.treeview.insert("", idx, values=("LOL", "value"))

class Console(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid(row=2, column=0, columnspan=3, sticky="nsew")
        self.execute_button = tk.Button(self, text="Execute", command=self.execute_code)
        self.execute_button.pack()
        self.label = tk.Label(self, text="Console")
        self.label.pack()
        self.text_widget = tk.Text(self, wrap="word", state="normal")
        self.text_widget.pack(fill="both", expand=True)
        

    def execute_code(self):
        global content
        self.text_widget.delete("1.0", tk.END)
        app.lexeme_table.clear()
        app.symbol_table.clear()
        code = self.master.code_editor.text_widget.get("1.0", tk.END)
        #print(f"Executing code:\n{code}")
        contents = code.splitlines()
        reset_flags()
        #print("code:")
        #print(code)
        """ print("Tokens:")
        print(self.tokens) """
        content = contents
        app.tokens = tokenize(app)

        # Update LexemeTable with the new tokens
        app.lexeme_table.populate(app.tokens)
        app.symbol_table.add_function_variables(function_var)
        #app.symbol_table.add_function_variables(function_var)
        #app.symbol_table.populate(variables)
        #app.symbol_table.populate(variables)
        #self.print_to_console(f"Executing code:\n{code}")

    def print_to_console(self, message):
        self.text_widget.insert(tk.END, f"{message}\n")
        self.text_widget.see(tk.END)

    def get_user_input(self, prompt):
        user_input = tk.simpledialog.askstring("User Input", prompt)
        return user_input

class Application(tk.Tk):

    def __init__(self):
        global app

        super().__init__()
        app = self
        self.tokens = []
        self.title("Code Editor with Lexemes and Symbol Table")

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

        self.select_file_button = tk.Button(self, text="Select File", command=self.load_file)
        self.select_file_button.grid(row=0, column=0, columnspan=3, sticky="nsew")

        self.code_editor = CodeEditor(self)
        self.lexeme_table = LexemeTable(self)
        self.symbol_table = SymbolTable(self)
        self.console = Console(self)

    def load_file(self):
        

        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.lol"), ("All files", "*.*")])
        contents = []
        if file_path:
            with open(file_path, "r") as file:
                for lines in file:
                    contents.append(lines.replace("\n", ""))
        

        self.code_editor.text_widget.delete("1.0", tk.END)
        self.code_editor.text_widget.insert(tk.END, "\n".join(contents))
        #self.tokens = tokenize(contents, self)
        
        # Update LexemeTable with the new tokens
        #self.lexeme_table.populate(self.tokens)
        #self.symbol_table.populate(variables)

if __name__ == "__main__":
    app = Application()
    app.mainloop()