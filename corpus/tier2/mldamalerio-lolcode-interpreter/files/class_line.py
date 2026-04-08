from copy import deepcopy  # to copy list without reference
import re


#Constants
IDENTIFIER = "identifier"
YARN = "yarn"
NUMBR = "numbr"
NUMBAR = "numbar"
TROOF = "troof"
TYPE_LITERAL = "type literal"
MATH = "math"
MAEK = "maek"
BOOL1 = "bool1"
BOOL2 = "bool2"
BOOL3 = "bool3"
COMP = "comp"
SMOOSH = "smoosh"

MAEK_ARGS = [IDENTIFIER, YARN, NUMBR, NUMBAR, TROOF, MATH, COMP, BOOL1, BOOL3]

# MATH
MATH_KEYWORDS = ["SUM OF", "DIFF OF", "PRODUKT OF", "QUOSHUNT OF", "MOD OF", "BIGGR OF", "SMALLR OF"]
MATH_ARGS = [IDENTIFIER, YARN, NUMBR, NUMBAR, TROOF, MATH, COMP]

# COMPARISON
COMPARISON_KEYWORDS = ["BOTH SAEM", "DIFFRINT"]
COMPARISON_ARGS = [YARN, NUMBR, NUMBAR, IDENTIFIER, TROOF, MATH, COMP]

# BOOLEAN
BOOL1_KEYWORDS = ["BOTH OF", "EITHER OF", "WON OF"]     # 2 arguments
BOOL2_KEYWORDS = ["ALL OF", "ANY OF"]                   # infinite arguments
BOOL3_KEYWORDS = ["NOT"]                                # 1 argument
BOOL_ARGS = [YARN, NUMBR, NUMBAR, IDENTIFIER, TROOF, MATH, BOOL1, BOOL3, COMP]

EXPRESSIONS_KEYWORDS = ["SUM OF", "DIFF OF", "PRODUKT OF", "QUOSHUNT OF", "MOD OF", "BIGGR OF", "SMALLR OF", "MAEK", "BOTH OF", "EITHER OF", "WON OF", "ALL OF", "ANY OF", "NOT",
    "BOTH OF", "EITHER OF", "WON OF",
    "ALL OF", "ANY OF", "NOT",
    "SMOOSH", "BOTH SAEM", "DIFFRINT"
]

INVALID = ["INVALID", "INVALID"]
ZERO = [0, 0]
TYPECAST_ERROR = ["TYPECAST", "TYPECAST"]

# expr = ""    # regex for expr

# (FOR REFERENCE ONLY)
# valid_lexemes_dictionary = {
#     "keywords": keywords,
#     "yarns": yarns,
#     "numbrs": numbrs,
#     "numbars": numbars,
#     "troofs": troofs,
#     "type_literals": types,
#     "identifiers": identifiers
# }

def check_expr(line):
    for i in line:
        if i in EXPRESSIONS_KEYWORDS:
            return True
    return False

def check_symbol_table(symbol_table, var_name):
    if var_name in symbol_table:
        return symbol_table.get(var_name)
    else:
        return None

def to_boolean(value):
    if value == "" or value == 0 or value == '""' or value == "0" or value == '"0"':
        return False
    elif type(value) == type(True):
        return value
    else:
        return True

def convert_to_type(type, string):
    string = re.sub("\"", "", string)
    if type == NUMBR or type == 'NUMBR':
        return int(string)
    elif type == NUMBAR or type == 'NUMBAR':
        return float(string)
    elif type == TROOF or type == 'TROOF':
        if string == "WIN":
            return True
        else:
            return False
    elif type == YARN or type == 'YARN':
        newstr = '"'
        newstr += string
        newstr += '"'
        return newstr
    else:
        return string

def convert_to_type_smoosh(type, string):
    if isinstance(string, str):
        string = re.sub("\"", "", string)
    if type == NUMBR or type == 'NUMBR':
        return int(string)
    elif type == NUMBAR or type == 'NUMBAR':
        return float(string)
    elif type == TROOF or type == 'TROOF':
        test = to_boolean(string)
        if test:
            return "WIN"
        return "FAIL"
    elif type == YARN or type == 'YARN':
        newstr = '"'
        newstr += string
        newstr += '"'
        return newstr
    else:
        return string

def evaluate_maek(line_array_types, complete_line, symbol_table):
    print(f"LINE ARRAY: {line_array_types}")
    print(f"COMPLETE ARRAY: {complete_line}")
    to_convert = complete_line[1]

    index = 0
    if line_array_types[index] == "MAEK":
        index += 1

        if line_array_types[index] == IDENTIFIER:
            if to_convert in symbol_table.keys():
                to_convert = symbol_table[to_convert]
                index += 1
            else:
                return INVALID
        else:
            to_convert = complete_line[index]
            index += 1
        
        if line_array_types[index] == "A":
            index += 1

        type = complete_line[index]
        return convert_to_type_smoosh(type, to_convert)

        


# Chinecheck yung pinaka-basic na math, hindi pa kasama yung nested
def check_math(line, console):

    # Index 0 is the operation
    index = 0

    # KEYWORD
    if line[index] in MATH_KEYWORDS: 
        index += 1
        # ARGUMENT #1
        if line[index] in MATH_ARGS: 
            index += 1
            # AN KEYWORD
            if line[index] == "AN": 
                index += 1
                # ARGUMENT #2
                if line[index] in MATH_ARGS: 
                    print("Valid MATH!")
                    return True
                else:
                    print("Invalid MATH Argument 2!")
                    console.append_terminal("Invalid MATH Argument 2!\n")
                    return False
            else:
                print("Invalid/no AN keyword!")
                console.append_terminal("Invalid/no AN keyword!\n")
                return False
        else:
            print("Invalid MATH Argument 1!")
            console.append_terminal("Invalid MATH Argument 1!\n")
            return False
    else:
        print("Invalid MATH Operation!")
        console.append_terminal("Invalid MATH Operation!\n")
        return False

# Check variable typecast (MAEK A (optional A), MAEK)
def check_variable_typecast_normalize(line):

    index = 0

    print("len line", len(line))
    print(line)

    if line[index] == "MAEK":
        index += 1
        if line[index] in MAEK_ARGS:
            index += 1
            if len(line) == 4:
                if line[index] == "A":
                    index += 1
                    if line[index] == TYPE_LITERAL:
                        return True
                    else:
                        print("false 6")
                        return False
                else:
                    return False
            elif len(line) == 3:
                if line[index] == TYPE_LITERAL:
                    index += 1
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
    else:
        return False

def check_bool(line, args_flag, console):
    # args_flag guide
    #   >> 1 = BOOL1    2 arguments
    #   >> 2 = BOOL2    infinite arguments
    #   >> 3 = BOOL3    1 argument

    # Index 0 is the operation
    index = 0

    match args_flag:
        case 1:
            if line[index] in BOOL1_KEYWORDS:
                index += 1
                if line[index] in BOOL_ARGS:
                    index += 1
                    if line[index] == "AN":
                        index += 1
                        if line[index] in BOOL_ARGS:
                            print("Valid BOOLEAN!")
                            return True
                        else:
                            print("Invalid BOOL1 argument 2!")
                            console.append_terminal("Invalid BOOL1 argument 2!\n")
                            return False
                    else:
                        print("Invalid/no AN keyword!")
                        console.append_terminal("Invalid/no AN keyword!\n")
                        return False 
                else:
                    print("Invalid BOOL1 argument 1!")
                    console.append_terminal("Invalid BOOL1 argument 1!\n")
                    return False
            else:
                print("Invalid BOOL1 keyword!")
                console.append_terminal("Invalid BOOL1 keyword!\n")
                return False 
            
        case 2:
            if line[index] in BOOL2_KEYWORDS:
                index += 1
                for i in range(index, len(line)):
                    if i % 2 == 0:
                        if line[i] == "AN" and i != (len(line) - 1):
                            continue
                        elif i == (len(line) - 1):
                            return True
                        else:
                            return False
                    else:
                        if line[i] in BOOL_ARGS:
                            continue
                        else:
                            return False
                    
            else:
                print("Invalid BOOL2 keyword!")
                console.append_terminal("Invalid BOOL2 keyword!\n")
                return False
            
        case 3:
            if line[index] in BOOL3_KEYWORDS:
                index += 1
                if line[index] in BOOL_ARGS:
                    print("Valid BOOLEAN!")
                    return True
                else:
                    print("Invalid BOOL3 argument!")
                    console.append_terminal("Invalid BOOL3 argument!\n")
                    return False
            else:
                print("Invalid BOOL3 keyword!")
                console.append_terminal("Invalid BOOL3 keyword!\n")
                return False 
        case _:
            return None

# Check comparison (BOTH SAEM (x == y), DIFFRINT (x != y))
def check_comparison(line, console):

    # Index 0 is the operation
    index = 0

    # KEYWORD
    if line[index] in COMPARISON_KEYWORDS: 
        index += 1
        # ARGUMENT #1
        if line[index] in COMPARISON_ARGS: 
            index += 1
            # AN KEYWORD
            if line[index] == "AN": 
                index += 1
                # ARGUMENT #2
                if line[index] in COMPARISON_ARGS: 
                    print("Valid COMPARISON!")
                    return True
                else:
                    print("Invalid COMPARISON Argument 2!")
                    console.append_terminal("Invalid COMPARISON Argument 2!\n")
                    return False
            else:
                print("Invalid/no AN keyword!")
                console.append_terminal("Invalid/no AN keyword!\n")
                return False
        else:
            print("Invalid COMPARISON Argument 1!")
            console.append_terminal("Invalid COMPARISON Argument 1!\n")
            return False
    else:
        print("Invalid COMPARISON Operation!")
        console.append_terminal("Invalid COMPARISON Operation!\n")
        return False

def check_smoosh(line):
    if line[0] == "SMOOSH" and len(line) > 0:
        return True
    return False

def check_string_if_number(string):
    numbr_regex = fr'(?<!\w|\.)-?[0-9]+(?!\w|\.)'
    numbar_regex = fr'(?<!\w|\.)(-?\d*\.\d+)(?!\w|\.)'
    numbr_pattern = re.compile(numbr_regex)
    numbar_pattern = re.compile(numbar_regex)
    numbr_match = numbr_pattern.search(string)
    numbar_match = numbar_pattern.search(string)

    if numbr_match:
        return True, NUMBR
    elif numbar_match:
        return True, NUMBAR
    else:
        return False, None

def return_math_value(expr, types, symbol_table):
    expr_copy = deepcopy(expr)

    for i in range(len(expr) - 1, -1, -1):

        # Math operation: with implicit typecasting
        if expr[i] in MATH_KEYWORDS:
            operation = expr_copy[i]
            arg1 = expr_copy[i+1]
            arg2 = expr_copy[i+3]

            # Checking if argument was a result of previous math operation
            if type(arg1) == type(""):
                # Checking for YARN types if they can be typecasted to NUMBR/NUMBAR
                if types[i+1] == YARN:
                    result, arg1_type = check_string_if_number(expr_copy[i+1])
                    if result == True:
                        arg1 = convert_to_type(arg1_type, expr_copy[i+1])
                    else:
                        print("YARN argument cannot be typecasted to NUMBR or NUMBAR!")
                        return TYPECAST_ERROR
                elif types[i+1] == TROOF:
                    arg1_troof = convert_to_type(types[i+1], expr_copy[i+1])
                    if arg1_troof == True:
                        arg1 = 1
                    else:
                        arg1 = 0
                elif types[i+1] == IDENTIFIER:
                    arg1_exists = check_symbol_table(symbol_table, arg1)
                    if arg1_exists != None:
                        if type(arg1_exists) == type(""):
                            result, arg1_type = check_string_if_number(re.sub("\"", "", arg1_exists))
                            if result == True:
                                arg1 = convert_to_type(arg1_type, arg1_exists)
                            else:
                                print("YARN argument cannot be typecasted to NUMBR or NUMBAR!")
                                return TYPECAST_ERROR
                        else:
                            arg1 = arg1_exists
                    else:
                        print("Trying to access uninitialized variable!!")
                        return INVALID
                else:
                    arg1 = convert_to_type(types[i+1], expr_copy[i+1])
            # Checking if argument was a result of previous comparison operation
            elif type(arg1) == type(True):
                if arg1 == True:
                    arg1 = 1
                else:
                    arg1 = 0
            else:
                arg1 = expr_copy[i+1]

            if type(arg2) == type(""):
                # Checking for YARN types if they can be typecasted to NUMBR/NUMBAR
                if types[i+3] == YARN:
                    result, arg2_type = check_string_if_number(expr_copy[i+3])
                    if result == True:
                        arg2 = convert_to_type(arg2_type, expr_copy[i+3])
                    else:
                        print("YARN argument cannot be typecasted to NUMBR or NUMBAR!")
                        return TYPECAST_ERROR
                elif types[i+3] == TROOF:
                    arg2_troof = convert_to_type(types[i+3], expr_copy[i+3])
                    if arg2_troof == True:
                        arg2 = 1
                    else:
                        arg2 = 0
                elif types[i+3] == IDENTIFIER:
                    arg2_exists = check_symbol_table(symbol_table, arg2)
                    if arg2_exists != None:
                        if type(arg2_exists) == type(""):
                            result, arg2_type = check_string_if_number(re.sub("\"", "", arg2_exists))
                            if result == True:
                                arg2 = convert_to_type(arg2_type, arg2_exists)
                            else:
                                print("YARN argument cannot be typecasted to NUMBR or NUMBAR!")
                                return TYPECAST_ERROR
                        else:
                            arg2 = arg2_exists
                    else:
                        print("Trying to access uninitialized variable!!")
                        return INVALID
                else:
                    arg2 = convert_to_type(types[i+3], expr_copy[i+3])
            # Checking if argument was a result of previous comparison operation
            elif type(arg2) == type(True):
                if arg2 == True:
                    arg2 = 1
                else:
                    arg2 = 0
            else:
                arg2 = expr_copy[i+3]
            
            match operation:
                case "SUM OF":
                    expr_copy[i] = arg1 + arg2
                case "DIFF OF":
                    expr_copy[i] = arg1 - arg2
                case "PRODUKT OF":
                    expr_copy[i] = arg1 * arg2
                case "QUOSHUNT OF":
                    expr_copy[i] = arg1 / arg2
                case "MOD OF":
                    expr_copy[i] = arg1 % arg2
                case "BIGGR OF":
                    expr_copy[i] = max(arg1, arg2)
                case "SMALLR OF":
                    expr_copy[i] = min(arg1, arg2)
                case _:
                    continue
            # Remove arguments
            for j in range(i + 3, i, -1):
                expr_copy.pop(j)
                types.pop(j)

        # Comparison operation: no implicit typecasting
        elif expr[i] in COMPARISON_KEYWORDS:
            operation = expr_copy[i]
            arg1 = expr_copy[i+1]
            arg2 = expr_copy[i+3]

            # Convert the result of a comparison operation to lolcode troof
            if type(arg1) == type(True):
                if arg1 == True:
                    arg1 = "WIN"
                else:
                    arg1 = "FAIL"
            else:
                if type(arg1) == type(""):
                    if types[i+1] == IDENTIFIER:
                        arg1_exists = check_symbol_table(symbol_table, arg1)
                        if arg1_exists != None:
                            if type(arg1_exists) == type(""):
                                arg1 = re.sub("\"", "", arg1_exists)
                            else:
                                arg1 = arg1_exists
                        else:
                            print("Trying to access uninitialized variable!!")
                            return INVALID
            if type(arg2) == type(True):
                if arg2 == True:
                    arg2 = "WIN"
                else:
                    arg2 = "FAIL"
            else:
                if type(arg2) == type(""):
                    if types[i+3] == IDENTIFIER:
                        arg2_exists = check_symbol_table(symbol_table, arg2)
                        if arg2_exists != None:
                            if type(arg2_exists) == type(""):
                                arg2 = re.sub("\"", "", arg2_exists)
                            else:
                                arg2 = arg2_exists
                        else:
                            print("Trying to access uninitialized variable!!")
                            return INVALID

            
            match operation:
                case "BOTH SAEM":
                    if str(arg1) == str(arg2):
                        expr_copy[i] = True
                    else:
                        expr_copy[i] = False
                case "DIFFRINT":
                    if str(arg1) == str(arg2):
                        expr_copy[i] = False
                    else:
                        expr_copy[i] = True
                case _:
                    continue
            # Remove arguments
            for j in range(i + 3, i, -1):
                expr_copy.pop(j)
                types.pop(j)

        # Bool1 operation: implicit typecasting to troof - 2 args
        elif expr[i] in BOOL1_KEYWORDS:
            operation = expr_copy[i]
            arg1 = expr_copy[i+1]
            arg2 = expr_copy[i+3]

            if types[i+1] == IDENTIFIER:
                arg1_exists = check_symbol_table(symbol_table, arg1)
                if arg1_exists != None:
                    arg1 = arg1_exists
                else:
                    print("Trying to access uninitialized variable!!")
                    return INVALID
            else:
                if type(arg1) == type(""):
                    arg1 = convert_to_type(types[i+1], arg1)
            
            if types[i+3] == IDENTIFIER:
                arg2_exists = check_symbol_table(symbol_table, arg2)
                if arg2_exists != None:
                    arg2 = arg2_exists
                else:
                    print("Trying to access uninitialized variable!!")
                    return INVALID
            else:
                if type(arg2) == type(""):
                    arg2 = convert_to_type(types[i+3], arg2)

            arg1_bool = to_boolean(arg1)
            arg2_bool = to_boolean(arg2)
            match operation:
                case "BOTH OF":
                    if arg1_bool and arg2_bool:
                        expr_copy[i] = True
                    else:
                        expr_copy[i] = False
                case "EITHER OF":
                    if arg1_bool or arg2_bool:
                        expr_copy[i] = True
                    else:
                        expr_copy[i] = False
                case "WON OF":
                    if (arg1_bool and not arg2_bool) or (not arg1_bool and arg2_bool):
                        expr_copy[i] = True
                    else:
                        expr_copy[i] = False

            # Remove arguments
            for j in range(i + 3, i, -1):
                expr_copy.pop(j)
                types.pop(j)

        # Bool2 operation: implicit typecasting to troof - infinite args
        elif expr[i] in BOOL2_KEYWORDS:
            operation = expr_copy[i]

            while len(expr_copy) > 3:
                arg1 = expr_copy[i+1]
                arg2 = expr_copy[i+3]

                if type(arg1) == type(""):
                    if types[i+1] == IDENTIFIER:
                        arg1_exists = check_symbol_table(symbol_table, arg1)
                        if arg1_exists != None:
                            arg1 = arg1_exists
                        else:
                            print("Trying to access uninitialized variable!!")
                            return INVALID
                    else:
                        arg1 = convert_to_type(types[i+1], arg1)
                
                if type(arg2) == type(""):
                    if types[i+3] == IDENTIFIER:
                        arg2_exists = check_symbol_table(symbol_table, arg2)
                        if arg2_exists != None:
                            arg2 = arg2_exists
                        else:
                            print("Trying to access uninitialized variable!!")
                            return INVALID
                    else:
                        arg2 = convert_to_type(types[i+3], arg2)

                arg1_bool = to_boolean(arg1)
                arg2_bool = to_boolean(arg2)

                match operation:
                    case "ALL OF":
                        if arg1_bool and arg2_bool:
                            expr_copy[i+1] = True
                        else:
                            expr_copy[i+1] = False
                    case "ANY OF":
                        if arg1_bool or arg2_bool:
                            expr_copy[i+1] = True
                        else:
                            expr_copy[i+1] = False

                # Remove arguments
                for j in range(i + 3, i + 1, -1):
                    expr_copy.pop(j)
                    types.pop(j)

            expr_copy.pop(0)
            expr_copy.pop(1)

        # Bool3 operation: implicit typecasting to troof - args
        elif expr[i] in BOOL3_KEYWORDS:
            operation = expr_copy[i]
            arg = expr_copy[i+1]

            if type(arg) == type(""):
                if types[i+1] == IDENTIFIER:
                    arg_exists = check_symbol_table(symbol_table, arg)
                    if arg_exists != None:
                        arg = arg_exists
                    else:
                        print("Trying to access uninitialized variable!!")
                        return INVALID
                else:
                    arg = convert_to_type(types[i+1], arg)

            arg_bool = to_boolean(arg)

            expr_copy[i] = not arg_bool

            # Remove arguments
            for j in range(i + 1, i, -1):
                expr_copy.pop(j)
                types.pop(j)
    if type(expr_copy[0]) == type(True):
        if expr_copy[0] == True:
            return "WIN"
        else:
            return "FAIL"

    return(expr_copy[0])

def simplify_visible(expr, types, symbol_table):
    expr_copy = deepcopy(expr)

    for i in range(len(expr) - 1, -1, -1):
        print(expr[i])
        # Check if visible has expressions
        if expr[i] in MATH_KEYWORDS or expr[i] in COMPARISON_KEYWORDS or expr[i] in BOOL1_KEYWORDS:
            expr_copy[i] = return_math_value(expr_copy[i:i+4], types[i:i+4], symbol_table)
            
            if expr_copy[i] == INVALID:
                return INVALID
            elif expr_copy[i] == TYPECAST_ERROR:
                return INVALID

            # Remove arguments
            for j in range(i + 3, i, -1):
                expr_copy.pop(j)
                types.pop(j)
        elif expr[i] in BOOL2_KEYWORDS:
            expr_copy[i] = return_math_value(expr_copy[i:], types[i:], symbol_table)
            
            if expr_copy[i] == INVALID:
                return INVALID
            elif expr_copy[i] == TYPECAST_ERROR:
                return INVALID
            
            # Remove arguments
            for j in range(len(expr_copy) - 1, i, -1):
                expr_copy.pop(j)
                types.pop(j)
        elif expr[i] in BOOL3_KEYWORDS:
            expr_copy[i] = return_math_value(expr_copy[i:i+2], types[i:i+2], symbol_table)
            
            if expr_copy[i] == INVALID:
                return INVALID
            elif expr_copy[i] == TYPECAST_ERROR:
                return INVALID
            
            # Remove arguments
            for j in range(i + 1, i, -1):
                expr_copy.pop(j)
                types.pop(j)
        elif expr[i] == "SMOOSH":
            expr_copy[i] = return_smoosh(expr_copy[i:], types[i:], symbol_table)

            print("EXPR_COPY HERE", expr_copy)
            if expr_copy[i] == INVALID:
                return INVALID
            if expr_copy[i] == TYPECAST_ERROR:
                return TYPECAST_ERROR
            
            # Remove arguments
            for j in range(len(expr_copy) - 1, i, -1):
                expr_copy.pop(j)
                types.pop(j)
        # Array element is not a keyword, skip.
        else:
            continue
    
    for i in range(len(expr_copy)):
        if type(expr_copy[i]) != type(""):
            expr_copy[i] = str(expr_copy[i])
    return(expr_copy)

def return_smoosh(expr, types, symbol_table):
    new_string = ""

    if types[0] == "SMOOSH":
        expr_copy = deepcopy(expr)

        for i in range(len(expr) - 1, 0, -1):
            # Check if visible has expressions
            if expr[i] in MATH_KEYWORDS or expr[i] in COMPARISON_KEYWORDS or expr[i] in BOOL1_KEYWORDS:
                expr_copy[i] = return_math_value(expr_copy[i:i+4], types[i:i+4], symbol_table)
                
                if expr_copy[i] == INVALID:
                    return INVALID
                elif expr_copy[i] == TYPECAST_ERROR:
                    return INVALID

                # Remove arguments
                for j in range(i + 3, i, -1):
                    expr_copy.pop(j)
                    types.pop(j)
            elif expr[i] in BOOL2_KEYWORDS:
                expr_copy[i] = return_math_value(expr_copy[i:], types[i:], symbol_table)
                
                if expr_copy[i] == INVALID:
                    return INVALID
                elif expr_copy[i] == TYPECAST_ERROR:
                    return INVALID
                
                # Remove arguments
                for j in range(len(expr_copy) - 1, i, -1):
                    expr_copy.pop(j)
                    types.pop(j)
            elif expr[i] in BOOL3_KEYWORDS:
                expr_copy[i] = return_math_value(expr_copy[i:i+2], types[i:i+2], symbol_table)
                
                if expr_copy[i] == INVALID:
                    return INVALID
                elif expr_copy[i] == TYPECAST_ERROR:
                    return INVALID
                
                # Remove arguments
                for j in range(i + 1, i, -1):
                    expr_copy.pop(j)
                    types.pop(j)
            
            # Array element is not a keyword, skip.
            else:
                continue
        
        for i in range(len(expr_copy)):
            if type(expr_copy[i]) == type(""):
                if types[i] == IDENTIFIER:
                    exists = check_symbol_table(symbol_table, expr_copy[i])
                    if exists != None:
                        if type(exists) == type(""):
                            expr_copy[i] = re.sub("\"", "", exists)
                        else:
                            expr_copy[i] = exists
                    else:
                        print("Trying to access uninitialized variable!!")
                        return INVALID

        for i in range(len(expr_copy)):
            if type(expr_copy[i]) != type(""):
                expr_copy[i] = str(expr_copy[i])
        
        for i in range(1, len(expr_copy)):
            if i % 2 != 0:
                new_string += expr_copy[i]
                new_string += " "

        return(new_string)
    else:
        return INVALID





#   _      _               _____ _               
#  | |    (_)             / ____| |              
#  | |     _ _ __   ___  | |    | | __ _ ___ ___ 
#  | |    | | '_ \ / _ \ | |    | |/ _` / __/ __|
#  | |____| | | | |  __/ | |____| | (_| \__ \__ \
#  |______|_|_| |_|\___|  \_____|_|\__,_|___/___/
                                               
                                            
#Class for line
class Line():

    #Constructor
    def __init__(self, line_number, line_array):    # ATTRIBUTES
        self.line_number = line_number              # line number  >> 5
        self.line_array = line_array                # line array   >> ["I HAS A", "identifier"]
        self.line_array_types = []                  # ex. ["I HAS A", "identifier", "ITZ", "SUM OF", "numbr", "AN", "numbr"]
        self.valid_lexemes_dictionary = {}          # dictionary of list of lexemes from lexical analysis

    #Initialize the dictionary reference
    def get_dictionary(self, valid_lexemes_dictionary):
        self.valid_lexemes_dictionary = valid_lexemes_dictionary

    #Normalize line (turn literals to constants such as IDENTIFIER, YARN, etc..)
    def normalize_line(self, check_semantics, console):
        orig_line = deepcopy(check_semantics.line_array)

        # from ["I HAS A", "var1"] to ["I HAS A", IDENTIFIER]
        # from ["I HAS A", "var1", "ITZ", 24] to ["I HAS A", IDENTIFIER, "ITZ", NUMBR]
        normalized_line = deepcopy(self.line_array)
        for i in range(len(normalized_line)):
            if normalized_line[i] in self.valid_lexemes_dictionary["yarns"]:
                normalized_line[i] = YARN
            elif normalized_line[i] in self.valid_lexemes_dictionary["numbrs"]:
                normalized_line[i] = NUMBR
            elif normalized_line[i] in self.valid_lexemes_dictionary["numbars"]:
                normalized_line[i] = NUMBAR
            elif normalized_line[i] in self.valid_lexemes_dictionary["troofs"]:
                normalized_line[i] = TROOF
            elif normalized_line[i] in self.valid_lexemes_dictionary["type_literals"]:
                normalized_line[i] = TYPE_LITERAL
            elif normalized_line[i] in self.valid_lexemes_dictionary["identifiers"]:
                normalized_line[i] = IDENTIFIER

        self.line_array_types = deepcopy(normalized_line)
            
        # TODO: replace exprs with "expression"

        invalid = False

        # Check if line has expressions, search for expression keywords in the line
        has_expr = check_expr(normalized_line)

        # Make a copy of normalized_line to replace expressions with corresponding classifier ("math", "comp", etc.)
        line_copy = deepcopy(normalized_line)

        # While the line still has expressions, continue loop. Loop will end once all expressions are replaced with classifiers ("math", "comp", etc.)
        while has_expr == True:

            # Loop from the last index of the normalized_line to support nested operations
            index = len(normalized_line) - 1

            # Start of loop, start from the last index, decrementing index every iteration
            for i in range(len(normalized_line) - 1, -1, -1):

                # Scan for expression keywords
                if normalized_line[i] in EXPRESSIONS_KEYWORDS:

                    # Check first if the operation has enough arguments for MATH
                    if len(normalized_line) > index + 3 and normalized_line[i] in MATH_KEYWORDS:
                        # Check if it is a MATH operation
                        valid_math = check_math(normalized_line[index:index+4], console)

                        # If it is a valid MATH operation, replace the whole expression with "math"
                        if valid_math == True:
                            line_copy[index] = MATH

                            # Remove arguments
                            for j in range(index + 3, index, -1):
                                line_copy.pop(j)

                            break
                        else:
                            print("Invalid MATH!")
                            console.append_terminal("Invalid MATH!\n")
                            invalid = True
                            break

                    # Check first if the operation has enough arguments for MAEK
                    elif len(normalized_line) > index + 2 and normalized_line[i] == "MAEK":
                        valid_maek = ""     # Temporary value
                        # MAEK with A keyword
                        if len(normalized_line) >= index + 3:
                            valid_maek = check_variable_typecast_normalize(self.line_array_types[index:index+4])

                        # MAEK without A keyword
                        else:
                            valid_maek = check_variable_typecast_normalize(self.line_array_types[index:index+3])

                        print("valid maek", valid_maek)
                        print("NORMALIZED LINE", normalized_line)
                        # If it is a valid MAEK operation, replace the whole expression with "maek"
                        if valid_maek == True:
                            line_copy[index] = MAEK

                            # MAEK with A keyword
                            if len(normalized_line) >= index + 4:
                                # Remove arguments
                                for j in range(index + 3, index, -1):
                                    line_copy.pop(j)

                            # MAEK without A keyword
                            else:
                                # Remove arguments
                                for j in range(index + 2, index, -1):
                                    line_copy.pop(j)
                            print("NORMALIZED LINE", normalized_line)
                            break
                        else:
                            print("Invalid MAEK!")
                            console.append_terminal("Invalid MAEK!\n")
                            invalid = True
                            break
                        print("NORMALIZED LINE", normalized_line)
                    # Check first if the operation has enough arguments for BOOL1
                    elif len(normalized_line) > index + 3 and normalized_line[i] in BOOL1_KEYWORDS:
                        valid_bool1 = check_bool(normalized_line[index:index+4], 1, console)

                        if valid_bool1 == True:
                            line_copy[index] = BOOL1

                            # Remove arguments
                            for j in range(index + 3, index, -1):
                                line_copy.pop(j)

                            break
                        else:
                            print("Invalid BOOL1!")
                            console.append_terminal("Invalid BOOL!\n")
                            invalid = True
                            break

                    # BOOL2
                    elif len(normalized_line) > index + 3 and normalized_line[i] in BOOL2_KEYWORDS:
                        valid_bool1 = check_bool(normalized_line[index:], 2, console)

                        if valid_bool1 == True:
                            line_copy[index] = BOOL2

                            # Remove arguments
                            for j in range(len(normalized_line) - 1, index, -1):
                                line_copy.pop(j)

                            break
                        else:
                            print("Invalid BOOL2!")
                            console.append_terminal("Invalid BOOL!\n")
                            invalid = True
                            break

                    # BOOL3
                    elif len(normalized_line) > index + 1 and normalized_line[i] in BOOL3_KEYWORDS:
                        valid_bool3 = check_bool(normalized_line[index:index+2], 3, console)

                        if valid_bool3 == True:
                            line_copy[index] = BOOL3

                            # Remove arguments
                            for j in range(index + 1, index, -1):
                                line_copy.pop(j)

                            break
                        else:
                            print("Invalid BOOL3!")
                            console.append_terminal("Invalid BOOL!\n")
                            invalid = True
                            break

                    # COMPARISON
                    elif len(normalized_line) > index + 3 and normalized_line[i] in COMPARISON_KEYWORDS:
                        valid_comp = check_comparison(normalized_line[index:index+4], console)

                        if valid_comp == True:
                            line_copy[index] = COMP

                            # Remove arguments
                            for j in range(index + 3, index, -1):
                                line_copy.pop(j)
                            break
                        else:
                            print("Invalid COMPARISON!")
                            console.append_terminal("Invalid COMPARISON!\n")
                            invalid = True
                            break

                    # SMOOSH
                    elif len(normalized_line) > index + 3 and normalized_line[i] == "SMOOSH":
                        valid_smoosh = check_smoosh(normalized_line[index:])

                        if valid_smoosh == True:
                            line_copy[index] = SMOOSH

                            # Remove arguments
                            for j in range(len(normalized_line) - 1, index, -1):
                                line_copy.pop(j)
                            break
                        else:
                            print("Invalid SMOOSH!")
                            console.append_terminal("Invalid SMOOSH!\n")
                            invalid = True
                            break
                
                    # Operation doesn't have enough arguments/invalid keyword
                    else:
                        print("Doesn't have enough arguments")
                        console.append_terminal("Doesn't have enough arguments\n")
                        invalid = True

                if invalid == False:
                    # Check if line still has expressions
                    has_expr = check_expr(normalized_line)
                else:
                    # Stop checking, has invalid syntax
                    has_expr = False
                # Decrement to go to the scan for the next expression keyword (IF ANY)
                index -= 1

            # Update normalized_line
            normalized_line = line_copy

        # set the normalized line
        self.line_array = normalized_line


    #    _____ _               _       _____             _             
    #   / ____| |             | |     / ____|           | |            
    #  | |    | |__   ___  ___| | __ | (___  _   _ _ __ | |_ __ ___  __
    #  | |    | '_ \ / _ \/ __| |/ /  \___ \| | | | '_ \| __/ _` \ \/ /
    #  | |____| | | |  __/ (__|   <   ____) | |_| | | | | || (_| |>  < 
    #   \_____|_| |_|\___|\___|_|\_\ |_____/ \__, |_| |_|\__\__,_/_/\_\
    #                                         __/ |                    
    #                                        |___/                     

    # METHODS FOR CHECKING SYNTAX (after normalizing line)

    # Check program start (HAI)
    def check_hai(self):
        if (self.line_array == ['HAI']):
            return True
        else:
            print("Program has no/invalid HAI!")
            return False
    
    # Check program end (KTHXBYE)
    def check_kthxbye(self):
        if (self.line_array == ['KTHXBYE']):
            return True
        else:
            print("Program has no/invalid KTHXBYE!")
            return False

    # TODO: maek, boolean
    # Check variable declaration (I HAS A)  
    def check_variable_declaration(self, complete_line, symbol_table):
        valid_declare = ["I HAS A", IDENTIFIER]
        valid_literal1 = ["I HAS A", IDENTIFIER, "ITZ", YARN]
        valid_literal2 = ["I HAS A", IDENTIFIER, "ITZ", NUMBR]
        valid_literal3 = ["I HAS A", IDENTIFIER, "ITZ", NUMBAR]
        valid_literal4 = ["I HAS A", IDENTIFIER, "ITZ", TROOF]
        valid_literal5 = ["I HAS A", IDENTIFIER, "ITZ", IDENTIFIER]
        valid_literal6 = ["I HAS A", IDENTIFIER, "ITZ", MATH]
        valid_literal7 = ["I HAS A", IDENTIFIER, "ITZ", MAEK]
        valid_literal8 = ["I HAS A", IDENTIFIER, "ITZ", BOOL1]
        valid_literal9 = ["I HAS A", IDENTIFIER, "ITZ", BOOL2]
        valid_literal10 = ["I HAS A", IDENTIFIER, "ITZ", BOOL3]
        valid_literal11 = ["I HAS A", IDENTIFIER, "ITZ", COMP]
        valid_literal12 = ["I HAS A", IDENTIFIER, "ITZ", SMOOSH]
        valid_list = [valid_declare, valid_literal1, valid_literal2, valid_literal3, valid_literal4, valid_literal5, valid_literal6, valid_literal7, valid_literal8, valid_literal9, valid_literal10, valid_literal11, valid_literal12]
        valid = False
        if (self.line_array in valid_list):
            valid = True

        # case of declaration only (I HAS A identifier)
        if valid and self.line_array == valid_declare:
            given_identifier = complete_line.line_array[1]
            # p(f"{given_identifier}, type: {type(given_identifier)}")
            return (0, given_identifier)     # return the name of identifier

        # case of initialization (I HAS A identifier ITZ value)
        elif valid:
            given_identifier = complete_line.line_array[1]
            value_to_assign = complete_line.line_array[3]  # 3rd argument (YARN by default)

            print(f"SELF LINE: {self.line_array}")
            # cast if other type
            if self.line_array[3] == NUMBR:
                value_to_assign = int(value_to_assign)

            elif self.line_array[3] == NUMBAR:
                value_to_assign = float(value_to_assign)

            elif self.line_array[3] == SMOOSH:
                value_to_assign = return_smoosh(complete_line.line_array[3:], self.line_array_types[3:], symbol_table)
                if value_to_assign == INVALID:
                    return INVALID
                if value_to_assign == TYPECAST_ERROR:
                    return TYPECAST_ERROR
            
            elif self.line_array[3] == MAEK:
                value_to_assign = evaluate_maek(self.line_array_types[3:], complete_line.line_array[3:], symbol_table)
                if value_to_assign == INVALID:
                    return INVALID
                return (1, given_identifier, value_to_assign)

            elif complete_line.line_array[3] in EXPRESSIONS_KEYWORDS:
                value_to_assign = return_math_value(complete_line.line_array[3:], self.line_array_types[3:], symbol_table)
                if value_to_assign == INVALID:
                    return INVALID
                if value_to_assign == TYPECAST_ERROR:
                    return TYPECAST_ERROR

            # print(f"{value_to_assign}, type: {type(value_to_assign)}")
            return (1, given_identifier, value_to_assign)
        else:
            return None

    # Check variable recasting (IS NOW A)
    def check_variable_recast(self, complete_line):
        valid = False
        if (self.line_array == [IDENTIFIER, "IS NOW A", TYPE_LITERAL]):
            valid = True
        
        if valid:
            identifier_to_change = complete_line.line_array[0]
            new_type = complete_line.line_array[2]

            # if valid, return the identifier to change and the new value
            return (identifier_to_change, new_type)
        else:
            return None
    
    # Check variable typecasting (MAEK)
    def check_variable_typecast(self, complete_line):
        valid_typecast = [MAEK]
        valid = False
        if (self.line_array == valid_typecast):
            valid = True
        
        if valid:
            identifier_to_change = complete_line.line_array[1]
            new_value = complete_line.line_array[len(complete_line.line_array) - 1]

            # if valid, return the identifier to change and the new value
            return (identifier_to_change, new_value)
        else:
            return None

    # TODO: SEMANTICS of maek
    # Check variable assignment (R)
    def check_variable_assignment(self, complete_line, symbol_table):
        valid1 = [IDENTIFIER, "R", YARN]
        valid2 = [IDENTIFIER, "R", NUMBR]
        valid3 = [IDENTIFIER, "R", NUMBAR]
        valid4 = [IDENTIFIER, "R", TROOF]
        valid5 = [IDENTIFIER, "R", MATH]
        valid6 = [IDENTIFIER, "R", MAEK]
        valid7 = [IDENTIFIER, "R", IDENTIFIER]
        valid8 = [IDENTIFIER, "R", COMP]
        valid9 = [IDENTIFIER, "R", SMOOSH]
        valid10 = [IDENTIFIER, "R", BOOL1]
        valid11 = [IDENTIFIER, "R", BOOL2]
        valid12 = [IDENTIFIER, "R", BOOL3]
        valid_list = [valid1, valid2, valid3, valid4, valid5, valid6, valid7, valid8, valid9, valid10, valid11, valid12]

        valid = False
        if self.line_array in valid_list:
            valid = True

        if valid:
            identifier_to_change = complete_line.line_array[0]
            new_value = complete_line.line_array[2]

            # if the second argument is an identifier, pass a type 0 return
            if (self.line_array[2] == IDENTIFIER):
                return (0, identifier_to_change, new_value)

            # if not an identifier, pass a type 1 return
            elif (self.line_array[2] == NUMBR):
                new_value = int(new_value)
                return (1, identifier_to_change, new_value)
                
            elif (self.line_array[2] == NUMBAR):
                new_value = float(new_value)
                return (1, identifier_to_change, new_value)

            elif (self.line_array[2] == SMOOSH):
                new_value = return_smoosh(complete_line.line_array[2:], self.line_array_types[2:], symbol_table)
                if new_value == INVALID:
                    return INVALID
                if new_value == TYPECAST_ERROR:
                    return TYPECAST_ERROR

            elif (self.line_array[2] == MAEK):
                value_to_assign = evaluate_maek(self.line_array_types[2:], complete_line.line_array[2:], symbol_table)
                if value_to_assign == INVALID:
                    return INVALID
                return (1, identifier_to_change, value_to_assign)

            elif (complete_line.line_array[2] in MATH_KEYWORDS):
                new_value = return_math_value(complete_line.line_array[2:], self.line_array_types[2:], symbol_table)
                if new_value == INVALID:
                    return INVALID
                if new_value == TYPECAST_ERROR:
                    return TYPECAST_ERROR
                return (1, identifier_to_change, new_value)
            elif (self.line_array[2] == COMP):
                new_value = return_math_value(complete_line.line_array[2:], self.line_array_types[2:], symbol_table)
                if new_value == INVALID:
                    return INVALID
                if new_value == TYPECAST_ERROR:
                    return TYPECAST_ERROR
                return (1, identifier_to_change, new_value)
            
            return (1, identifier_to_change, new_value)
        else:
            return None

    # Check input (GIMMEH)
    def check_input(self, complete_line, symbol_table):
        valid_input = ['GIMMEH', IDENTIFIER]
        valid = False
        if (self.line_array == valid_input):
            valid = True
        
        if valid:
            identifier_to_getinput = complete_line.line_array[1]

            if (identifier_to_getinput not in symbol_table.keys()):
                return INVALID

            return identifier_to_getinput
        else:
            return None

    # Check print (VISIBLE)
    def check_print(self, complete_line, symbol_table):
        valid = False
        if (self.line_array[0] == "VISIBLE" and len(self.line_array) > 1):
            valid = True

        if valid:
            check = simplify_visible(complete_line.line_array, self.line_array_types, symbol_table)
            if check == INVALID:
                return INVALID
            elif check == TYPECAST_ERROR:
                return TYPECAST_ERROR

            return valid, check
        else:
            return None, None
    
    # Check if then start (O RLY?)
    def check_ifthen_start(self):
        valid = False
        if (self.line_array == ["O RLY?"]):
            valid = True

        return valid

    # Check if (YA RLY)
    def check_if(self):
        valid = False
        if (self.line_array == ["YA RLY"]):
            valid = True

        return valid

    # Check else (NO WAI)
    def check_else(self):
        valid = False
        if (self.line_array == ["NO WAI"]):
            valid = True

        return valid

    # Check conditional end (OIC)
    def check_conditional_end(self):
        valid = False
        if (self.line_array == ["OIC"]):
            valid = True

        return valid

    # Check the implicit IT variable
    def check_implicit_it(self, complete_line, symbol_table):
        valid_it1 = [IDENTIFIER]
        valid_it2 = [YARN]
        valid_it3 = [NUMBR]
        valid_it4 = [NUMBAR]
        valid_it5 = [TROOF]
        valid_it6 = [MATH]
        valid_it7 = [COMP]

        valid_list = [valid_it1, valid_it2, valid_it3, valid_it4, valid_it5, valid_it6, valid_it7]

        valid = False
        if (self.line_array in valid_list):
            valid = True
        
        if (valid):
            # TODO: add boolean
            # TODO: note, return (True/False, value_of_it)

            if self.line_array[0] == IDENTIFIER:
                print("IDENTIFIER!")
                to_check = complete_line.line_array[0]
                if (to_check in symbol_table.keys()):
                    value_of_it = symbol_table[to_check]
                    return (to_boolean(value_of_it), value_of_it)
                elif (to_check not in symbol_table.keys()):
                    return INVALID  # invalid (Error)

            if self.line_array[0] == NUMBR:
                value_of_it = int(complete_line.line_array[0])
                return (to_boolean(value_of_it), value_of_it)

            if self.line_array[0] == NUMBAR:
                value_of_it = float(complete_line.line_array[0])
                return (to_boolean(value_of_it), value_of_it)

            if self.line_array[0] == YARN:
                value_of_it = complete_line.line_array[0]
                return (to_boolean(value_of_it), value_of_it)

            if self.line_array[0] == COMP:
                value_of_it = return_math_value(complete_line.line_array, self.line_array_types, symbol_table)

                if value_of_it == INVALID:
                    return INVALID
                
                return (convert_to_type(TROOF, value_of_it), value_of_it)

            if complete_line.line_array[0] in MATH_KEYWORDS:
                value_of_it = return_math_value(complete_line.line_array, self.line_array_types, symbol_table)
                if value_of_it == INVALID:
                    return INVALID
                return (to_boolean(value_of_it), value_of_it)
            
            if self.line_array[0] == TROOF:
                value_of_it = complete_line.line_array[0]
                return (convert_to_type(TROOF, value_of_it), value_of_it)

            

        else:
            return None

    # Check case statement (WTF?)
    def check_case_start(self):
        valid = False
        if (self.line_array == ["WTF?"]):
            valid = True

        return valid

    # Check cases (OMG <case>)
    def check_cases(self, complete_line):
        valid_cases = [IDENTIFIER, NUMBR, NUMBAR, YARN, TROOF, MATH, MAEK]

        valid = False
        if (self.line_array[0] == "OMG"):
            if (self.line_array[1] in valid_cases):
                valid = True
                
        if valid:

            if self.line_array_types[1] == YARN:
                return str(complete_line.line_array[1])
            if self.line_array_types[1] == NUMBR:
                if complete_line.line_array[1] == "0":
                    return ZERO
                else:
                    return int(complete_line.line_array[1])
            if self.line_array_types[1] == NUMBAR:
                return float(complete_line.line_array[1])
            if self.line_array_types[1] == TROOF:
                return str(complete_line.line_array[1])
        else:
            return None

    # Check break (GTFO)
    def check_break(self):
        valid = False
        if (self.line_array == ["GTFO"]):
            valid = True

        return valid

    # Check case default (OMGWTF)
    def check_case_default(self):
        valid = False
        if (self.line_array == ["OMGWTF"]):
            valid = True

        return valid
    
    # Check loop start (IM IN YR <label> <operation> YR <variable> [TIL|WILE <expression>])
    def check_loop_start(self, complete_line, symbol_table):

        OPERATIONS = ["UPPIN", "NERFIN"]
        TIL_OR_WILE = ["TIL", "WILE"]
        EXPRESSION_ARGS = [BOOL1, BOOL2, BOOL3, COMP]

        operation_to_do = ""

        index = 0
        if (self.line_array[index] == "IM IN YR"):
            index += 1
            if (self.line_array[index] == IDENTIFIER):
                index += 1
                if (self.line_array[index] in OPERATIONS):
                    operation_to_do = self.line_array[index]
                    index += 1
                    if (self.line_array[index] == "YR"):
                        index += 1
                        if (self.line_array[index] == IDENTIFIER):
                            
                            variable_to_check = complete_line.line_array[index]
                            # if identifier is not defined
                            if (variable_to_check not in symbol_table.keys()):
                                return INVALID

                            index += 1
                            if (self.line_array[index] in TIL_OR_WILE):
                                CHOOSE_TIL_OR_WILE = self.line_array[index]
                                index += 1
                                if (self.line_array[index] in EXPRESSION_ARGS):
                                    
                                    # if expression is COMP (BOTH SAEM, DIFFRINT)
                                    if self.line_array[index] == COMP:

                                        check_math = return_math_value(complete_line.line_array[index:], self.line_array_types[index:], symbol_table)
                                        if check_math == INVALID:
                                            return INVALID
                                        if check_math == TYPECAST_ERROR:
                                            return TYPECAST_ERROR
                                        
                                        continue_loop = False
                                        if (CHOOSE_TIL_OR_WILE == "TIL" and check_math == "FAIL"):
                                            continue_loop = True
                                        elif (CHOOSE_TIL_OR_WILE == "WILE" and check_math == "FAIL"):
                                            continue_loop = True


                                        print(f"EVALUATE: {complete_line.line_array[index:]}")

                                        # BOOLEAN, OPERATION, VARIABLE to check
                                        print(f"\n\nCONTINUE LOOP? {continue_loop}")
                                        print(f"TO BOOLEAN EXPRESSION {check_math}")
                                        print(f"VARIABLE TO CHECK {variable_to_check} = {symbol_table[variable_to_check]}")
                                        return (continue_loop, operation_to_do, variable_to_check)

        return None

    # Check loop end (IM OUTTA YR <label>)
    def check_loop_end(self):
        valid = False
        if (self.line_array == ["IM OUTTA YR", IDENTIFIER]):
            valid = True
        return valid