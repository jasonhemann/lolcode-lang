from turtle import goto
from lexer import *
from tkinter import simpledialog

output = [""]
error = ""
variables = {"IT": ""}
operations = ['SUM_OF', 'DIFF_OF', 'PRODUKT_OF', 'QUOSHUNT_OF', 'MOD_OF', 'BIGGR_OF', 'SMALLR_OF']
arith_operations = ['SUM_OF', 'DIFF_OF', 'PRODUKT_OF', 'QUOSHUNT_OF', 'MOD_OF', 'BIGGR_OF', 'SMALLR_OF']
bool_operations = ['BOTH_OF', 'EITHER_OF', 'WON_OF', 'NOT', 'ALL_OF', 'ANY_OF']


# Matching tokens to check if it is expected
def match(tokens, expected_type):
    global error
    if tokens and tokens[0][1] == expected_type:
        tokens.pop(0)
    else:
        error = "Expected {expected_type}, got {tokens[0][1]}"

# Printing
def display(tokens):
    match(tokens, 'VISIBLE')
    result = ""
    while tokens:
        if tokens and tokens[0][1] == 'SMOOSH':
            result += str(parse_concat(tokens))
        elif tokens and tokens[0][1] in [
            'SUM_OF',
            'DIFF_OF', 
            'PRODUKT_OF',
            'QUOSHUNT_OF', 
            'MOD_OF', 
            'BIGGR_OF', 
            'SMALLR_OF', 
            'BOTH_SAEM', 
            'DIFFRINT'
        ]:
            result += str(parse_expression(tokens))
        elif tokens and tokens[0][1] in [
            'BOTH_OF', 
            'EITHER_OF', 
            'WON_OF', 
            'ANY_OF', 
            'ALL_OF', 
            'NOT'
        ]:
            result += str(parse_boolean_operation(tokens))

        elif tokens and tokens[0][1] == "IDENTIFIER" and tokens[0][0] in variables:
            result += str(variables[tokens[0][0]])
            tokens.pop(0)
        else:
            if tokens[0][1] == "YARN_LITERAL":
                result += tokens[0][0].replace("\"", "")
            else: result += str(tokens[0][0])
            tokens.pop(0)

        if tokens and tokens[0][1] != 'PLUS':
            break
        else:
            match(tokens, 'PLUS')

    output.append(result)
    return tokens

def parse_program(tokens):
    output.clear()
    variables.clear()
    while tokens[0][1] == "INLINE_COMMENT" or tokens[0][1] == "MULTI_LINE_COMMENT":
        if tokens[0][1] == "INLINE_COMMENT":
            match(tokens, 'INLINE_COMMENT')
        elif tokens[0][1] == "MULTI_LINE_COMMENT":
            match(tokens, 'MULTI_LINE_COMMENT')
    match(tokens, 'HAI')
    parse_statements(tokens)
    if error != "":
        output.append(error)
        return output
    else:
        match(tokens, 'KTHXBYE')
        return output

def parse_statements(tokens):
    global error
    error = ""
    while tokens:
        if tokens[0][1] == "WAZZUP": parse_variable_declaration(tokens)
        # elif tokens[0][1] == 'HOW_IZ_I':
        #     parse_function_definition(tokens)
        elif tokens[0][1] == 'INLINE_COMMENT': match(tokens, 'INLINE_COMMENT')
        elif tokens[0][1] == 'MULTI_LINE_COMMENT': match(tokens, 'MULTI_LINE_COMMENT')
        elif tokens[0][1] in ['SUM_OF', 'DIFF_OF', 'PRODUKT_OF', 'QUOSHUNT_OF', 'MOD_OF', 'BIGGR_OF', 'SMALLR_OF', 'BOTH_SAEM', 'DIFFRINT']:
            variables["IT"] = parse_expression(tokens)
        elif tokens[0][1] == 'IDENTIFIER':
            parse_assignment(tokens)
        elif tokens[0][1] == 'SMOOSH':
            variables["IT"] = parse_concat(tokens)
        elif tokens[0][1] == 'GIMMEH':
            parse_input_statements(tokens)
        elif tokens[0][1] in ['BOTH_OF', 'EITHER_OF', 'WON_OF', 'ANY_OF', 'ALL_OF', 'NOT']:
            variables["IT"] = parse_boolean_operation(tokens)
        elif tokens[0][1] == 'MAEK':
            match(tokens, 'MAEK')
            value = tokenize(variables[tokens[0][0]])
            tokens.pop(0)
            match(tokens, 'A')
            parse_typecasting(tokens, value, False)
        elif tokens[0][1] == 'O_RLY':
            parse_ifelse(tokens)
        elif tokens[0][1] == 'WTF':
            parse_switch(tokens)
        elif tokens[0][1] == 'IM_IN_YR':
            parse_loop(tokens)
        elif tokens[0][1] == 'VISIBLE':
            tokens = display(tokens)
        elif tokens[0][1] == 'KTHXBYE':
            break
        else:
            error = "Unexpected token: " + str({tokens[0][0]})
            break
            # raise SyntaxError(f"Unexpected token: {tokens[0][0]}")

# Variables
def parse_variable_declaration(tokens):
    match(tokens, 'WAZZUP')
    while tokens:
        if tokens[0][1] == 'INLINE_COMMENT':
            match(tokens, 'INLINE_COMMENT')
        elif tokens[0][1] == 'MULTI_LINE_COMMENT':
            match(tokens, 'MULTI_LINE_COMMENT')
        elif tokens[0][1] == 'BUHBYE':
            break
        else:
            match(tokens, 'I_HAS_A')
            variable_name = tokens[0][0]
            match(tokens, 'IDENTIFIER')
            if tokens and tokens[0][1] == 'ITZ':
                match(tokens, 'ITZ')
                if tokens and tokens[0][1] in arith_operations:
                    variables[variable_name] = parse_expression(tokens)
                else:
                    variables[variable_name] = tokens.pop(0)[0]  # TO FIX: SKIPPING INITIALIZATION
            else:
                variables[variable_name] = "NOOB"
    match(tokens, 'BUHBYE')

# GIMMEH

# EXPRESSIONS
def parse_expression(tokens):
    # Arithmetic
    if tokens[0][1] == 'SUM_OF': return parse_binary_operation(tokens, 'SUM_OF', lambda x, y: x + y)
    elif tokens[0][1] == 'DIFF_OF': return parse_binary_operation(tokens, 'DIFF_OF', lambda x, y: x - y)
    elif tokens[0][1] == 'PRODUKT_OF': return parse_binary_operation(tokens, 'PRODUKT_OF', lambda x, y: x * y)
    elif tokens[0][1] == 'QUOSHUNT_OF': return parse_binary_operation(tokens, 'QUOSHUNT_OF', lambda x, y: x / y)
    elif tokens[0][1] == 'MOD_OF': return parse_binary_operation(tokens, 'MOD_OF', lambda x, y: x % y)
    elif tokens[0][1] == 'BIGGR_OF': return parse_binary_operation(tokens, 'BIGGR_OF', max)
    elif tokens[0][1] == 'SMALLR_OF': return parse_binary_operation(tokens, 'SMALLR_OF', min)
    
    # Concatenation
    elif tokens[0][1] == 'SMOOSH': return parse_concat(tokens)

    # Boolean
    elif tokens[0][1] == 'BOTH_OF': return None
    elif tokens[0][1] == 'EITHER_OF': return None
    elif tokens[0][1] == 'WON_OF': return None
    elif tokens[0][1] == 'NOT': return None
    elif tokens[0][1] == 'ALL OF': return None
    elif tokens[0][1] == 'ANY OF': return None

    # Comparison
    elif tokens[0][1] == 'BOTH_SAEM': 
        operation_fn = lambda x, y: x == y
        result = parse_binary_operation(tokens, tokens[0][1], operation_fn)
        if result == True: return 'WIN'
        else: return 'FAIL'
    elif tokens[0][1] == 'DIFFRINT': 
        operation_fn = lambda x, y: x != y
        result = parse_binary_operation(tokens, tokens[0][1], operation_fn)
        if result == True: return 'WIN'
        else: return 'FAIL'

    return parse_binary_operation(tokens, tokens[0][1], operation_fn)

def parse_binary_operation(tokens, operator, operation_fn):
    match(tokens, operator)
    x = parse_operand(tokens)
    match(tokens, 'AN')
    y = parse_operand(tokens)
    result = operation_fn(x, y)
    if isinstance(result, float):
        result = round(result, 2)
    return result

def parse_operand(tokens):
    if tokens and tokens[0][1] == 'NUMBR_LITERAL':
        value = int(tokens[0][0])
        tokens.pop(0)
        return value
    elif tokens and tokens[0][1] == 'NUMBAR_LITERAL':
        value = float(tokens[0][0])
        tokens.pop(0)
        return value
    elif tokens and tokens[0][1] in ['TROOF_LITERAL', 'YARN_LITERAL']:
        value = [tokens[0]]
        tokens.pop(0)
        return parse_typecasting(tokens, value, True)
    elif tokens and tokens[0][1] == 'IDENTIFIER':
        value = tokenize(str(variables[tokens[0][0]]))
        tokens.pop(0)
        typecasted = parse_typecasting(tokens, value, True)
        if (typecasted == 'FAIL'):
            return None
        return parse_typecasting(tokens, value, True)
    elif tokens and tokens[0][1] in ['SUM_OF', 'DIFF_OF', 'PRODUKT_OF', 'QUOSHUNT_OF', 'MOD_OF', 'BIGGR_OF', 'SMALLR_OF', 'BOTH_SAEM', 'DIFFRINT']:
        return parse_expression(tokens)
    else:
        raise SyntaxError("Expected numeric literal, variable, or arithmetic expression, got {}".format(tokens[0][1]))

def parse_concat(tokens):
    match(tokens, 'SMOOSH')
    concatenated_strings = []
    
    while tokens and (tokens[0][1] in ['YARN_LITERAL', 'NUMBR_LITERAL', 'NUMBAR_LITERAL', 'TROOF_LITERAL', 'IDENTIFIER']):
        if tokens[0][1] == 'YARN_LITERAL':
            concatenated_strings.append(tokens[0][0][1:-1])
        elif tokens[0][1] == 'IDENTIFIER':
            variable_name = tokens[0][0]
            concatenated_strings.append(str(variables.get(variable_name, '')))
        else:
            concatenated_strings.append(str(tokens[0][0]))
        tokens.pop(0)
        
        if tokens and tokens[0][1] == 'AN':
            tokens.pop(0)
        else:
            break

    result = ''.join(concatenated_strings)
    return result

def parse_troof(returned):
    if returned == 'WIN':
        return True
    elif returned == 'FAIL':
        return False
    
def parse_troof_back(returned):
    if returned == True:
        return 'WIN'
    elif returned == False:
        return 'FAIL'

def parse_assignment(tokens):
    variable_name = tokens[0][0]
    match(tokens, 'IDENTIFIER')
    if variables[variable_name] != "NOOB":
        if tokens and tokens[0][1] == 'IS_NOW_A':
            match(tokens, 'IS_NOW_A')
            value = tokenize(variables[variable_name])
            parse_typecasting(tokens, value, False)
            variables[variable_name] = variables['IT']
        if tokens and tokens[0][1] == 'R':
            match(tokens, 'R')
            match(tokens, 'MAEK')
            value = tokenize(variables[variable_name])
            tokens.pop(0)
            parse_typecasting(tokens, value, False)
            variables[variable_name] = variables['IT']
    else:
        match(tokens, 'R')
        if tokens and tokens[0][1] in ['SUM_OF', 'DIFF_OF', 'PRODUKT_OF', 'QUOSHUNT_OF', 'MOD_OF', 'BIGGR_OF', 'SMALLR_OF']:
            variables[variable_name] = parse_expression(tokens)
        elif tokens and tokens[0][1] == 'SMOOSH':
            variables[variable_name] = parse_concat(tokens)
        elif tokens and tokens[0][1] == 'IDENTIFIER':
            variables[variable_name] = variables[tokens[0][0]]
            tokens.pop(0)
        elif tokens and tokens[0][1] == 'MAEK':
            parse_typecasting(tokens)
            variables[variable_name] = variables['IT']
        else:
            variables[variable_name] = tokens[0][0]
            tokens.pop(0)

# Arithmetic
        
# Smoosh, Assign
        
# Bool
def parse_boolean_operation(tokens):
    if tokens[0][1] == 'BOTH_OF':
        return parse_troof_back(parse_and(tokens))
    elif tokens[0][1] == 'EITHER_OF':
        return parse_troof_back(parse_or(tokens))
    elif tokens[0][1] == 'WON_OF':
        return parse_troof_back(parse_xor(tokens))
    elif tokens[0][1] == 'ANY_OF':
        return parse_troof_back(parse_any(tokens))
    elif tokens[0][1] == 'ALL_OF':
        return parse_troof_back(parse_all(tokens))
    elif tokens[0][1] == 'NOT':
        return parse_troof_back(parse_not(tokens))

def parse_bool_operand(tokens):
    if tokens and tokens[0][1] == 'TROOF_LITERAL':
        value = tokens[0][0]
        tokens.pop(0)
        return parse_troof(value)
    elif tokens and tokens[0][1] in ['BOTH_OF', 'EITHER_OF', 'WON_OF', 'ANY_OF', 'ALL_OF', 'NOT']:
        return parse_boolean_operation(tokens)
    else:
        raise SyntaxError("Expected boolean literal or boolean expression, got {}".format(tokens[0][1]))
    
def parse_and(tokens):
    match(tokens, 'BOTH_OF')
    x = parse_bool_operand(tokens)
    match(tokens, 'AN')
    y = parse_bool_operand(tokens)
    return x and y

def parse_or(tokens):
    match(tokens, 'EITHER_OF')
    x = parse_bool_operand(tokens)
    match(tokens, 'AN')
    y = parse_bool_operand(tokens)
    return x or y

def parse_xor(tokens):
    match(tokens, 'WON_OF')
    x = parse_bool_operand(tokens)
    match(tokens, 'AN')
    y = parse_bool_operand(tokens)
    return x ^ y

def parse_not(tokens):
    match(tokens, 'NOT')
    x = parse_bool_operand(tokens)
    return not x

def parse_all(tokens):
    match(tokens, 'ALL_OF')
    operands = []
    result = True

    while tokens and tokens[0][1] != 'MKAY':
        if tokens[0][1] in ['ALL_OF', 'ANY_OF']:
            raise SyntaxError("ALL_OF and ANY_OF cannot be operands for ALL_OF")
        operands.append(parse_bool_operand(tokens))
        if tokens and tokens[0][1] == 'AN':
            match(tokens, 'AN')

    if not operands:
        raise SyntaxError("Expected at least one operand for ALL_OF, got none")
    
    for troof in operands:
        if troof in ['FAIL', False]:
            result = False
            break
        else:
            continue
    
    match(tokens, 'MKAY')
    return result

def parse_any(tokens):
    match(tokens, 'ANY_OF')
    operands = []
    result = False

    while tokens and tokens[0][1] != 'MKAY':
        if tokens[0][1] in ['ALL_OF', 'ANY_OF']:
            raise SyntaxError("ALL_OF and ANY_OF cannot be operands for ANY_OF")
        operands.append(parse_bool_operand(tokens))
        if tokens and tokens[0][1] == 'AN':
            match(tokens, 'AN')

    if not operands:
        raise SyntaxError("Expected at least one operand for ANY_OF, got none")

    for troof in operands:
        if troof in ['WIN', True]:
            result = True
            break
        else:
            continue

    match(tokens, 'MKAY')
    return result
       
# Comparison
# Typecasting

def parse_toNoob(tokens):
    return None

def parse_toTroof(tokens):
    return None

def parse_toNumbar(tokens):
    return None

def parse_toNumbr(tokens):
    return None

def parse_toYarn(tokens):
    return None

def parse_toBool(tokens):
    return None

# If Else
def parse_ifelse(tokens):
    considered_expression = typeOfIT(variables['IT'])
    if_statement = []
    else_statement = []
    match(tokens, 'O_RLY')
    match(tokens, 'YA_RLY')
    while (tokens):
        if_statement.append(tokens.pop(0))
        if tokens[0][1] == 'OIC' or tokens[0][1] == 'NO_WAI':
            break
    match(tokens, 'NO_WAI')
    while (tokens[0][1] != 'OIC'):
        else_statement.append(tokens.pop(0))
    match(tokens, 'OIC')
    if considered_expression:
        parse_statements(if_statement)
    else:
        parse_statements(else_statement)

# Switch
def parse_switch(tokens):
    accepted_omg = 0
    value_to_compare = variables['IT']
    match(tokens, 'WTF')
    tokens_to_eval = []
    while tokens[0][1] != 'OMGWTF':
        match(tokens, 'OMG')
        if tokens[0][1] in ['TROOF_LITERAL']:
            condition_value = tokens[0][0]
        elif tokens[0][1] in ['YARN_LITERAL']:
            condition_value = tokens[0][0][1:-1]
        else:
            condition_value = parse_typecasting(tokens, [tokens[0]], True)
        if value_to_compare == condition_value:
            accepted_omg = 1
            match(tokens, tokens[0][1])
            while tokens:
                tokens_to_eval.append(tokens.pop(0))
                if tokens[0][1] == 'OMG' or tokens[0][1] == 'OMGWTF':
                    break
            parse_statements(tokens_to_eval)
            while tokens[0][1] != 'OMGWTF':
                tokens.pop(0)
            break
        else:
            while tokens:
                tokens.pop(0)
                if tokens[0][1] == 'OMG' or tokens[0][1] == 'OMGWTF':
                    break
    if accepted_omg == 0:
        match(tokens, 'OMGWTF')
        while tokens[0][1] != 'OIC':
            tokens_to_eval.append(tokens.pop(0))
        parse_statements(tokens_to_eval)
    else:
        match(tokens, 'OMGWTF')
        while tokens[0][1] != 'OIC':
            tokens.pop(0)
    match(tokens, 'OIC')

# Loops
def parse_loop(tokens):
    loops = []
    increment = 0
    value = 0
    variableName = ""
    match(tokens, 'IM_IN_YR')
    loops.append(tokens[0][0])
    match(tokens, 'IDENTIFIER')
    if tokens[0][1] == 'UPPIN':
        increment = 1
        match(tokens, 'UPPIN')
    elif tokens[0][1] == 'NERFIN':
        increment = -1
        match(tokens, 'NERFIN')
    match(tokens, 'YR')
    variableName = tokens[0][0]
    value = variables[variableName]
    if all((char.isdigit() or char == '-' or char == '.') and (char != '-' or i == 0) for i, char in enumerate(value)):
        if '.' in value:
            value = float(value)
        else :
            value =  int(value)
    else:
        if value == 'WIN':
            value = 1
        elif value == 'FAIL':
            value = 1
    match(tokens, 'IDENTIFIER')
    if tokens[0][1] == 'TIL':
        match(tokens, 'TIL')
        orig_loop_body = []
        loop_body = []
        while tokens and tokens[0][1] != 'IM_OUTTA_YR':
            token_to_add = tokens.pop(0)
            orig_loop_body.append(token_to_add)
            loop_body.append(token_to_add)
        while variables['IT'] != 'WIN':
            parse_statements(loop_body)
            value += increment
            variables[variableName] = value
            loop_body = orig_loop_body
    elif tokens[0][1] == 'WILE':
        match(tokens, 'WILE')
        loop_body = []
        while tokens and tokens[0][1] != 'IM_OUTTA_YR':
            loop_body.append(tokens.pop(0))
        while variables['IT'] == 'WIN':
            parse_statements(loop_body)
            value += increment
            variables[variableName] = value
    match(tokens, 'IM_OUTTA_YR')
       
# Functions    
def typeOfIT(value):
    if value == '' or value == 0 or value == 0.0 or value == 'FAIL':
        result = False
    else:
        result = True
    return result

def parse_typecasting(tokens, value, isImplicit):
    global error
    if isImplicit:
        if value and value[0][1] == 'TROOF_LITERAL':
            if value[0][0] == 'WIN':
                return 1
            else:
                return 0
        if value and value[0][1] == 'NUMBR_LITERAL':
            return int(value[0][0])
        if value and value[0][1] == 'NUMBAR_LITERAL':
            return float(value[0][0])
        if value and value[0][1] == 'YARN_LITERAL':
            raw_value = value[0][0][1:-1]
            if all((char.isdigit() or char == '-' or char == '.') and (char != '-' or i == 0) for i, char in enumerate(raw_value)):
                if '.' in raw_value:
                    return float(raw_value)
                else :
                    return int(raw_value)
            else:
                if raw_value == 'WIN' or raw_value == 'FAIL':
                    return parse_troof(raw_value)
        if value and value[0][1] == 'NOOB_LITERAL':
            return 'FAIL'
    else:
        if value and value[0][1] == 'TROOF_LITERAL':
            if tokens[0][1] == 'NUMBR':
                if value[0][0] == 'WIN':
                    variables['IT'] = 1
                else:
                    variables['IT'] = 0
                match(tokens, 'NUMBR')
            elif tokens[0][1] == 'NUMBAR':
                if value[0][0] == 'WIN':
                    variables['IT'] = 1.0
                else:
                    variables['IT'] = 0.0
                match(tokens, 'NUMBAR')
        elif value and value[0][1] == 'NUMBR_LITERAL':
            if tokens[0][1] == 'NUMBAR':
                variables['IT'] = float(value[0][0])
                match(tokens, 'NUMBAR')
            elif tokens[0][1] == 'TROOF':
                if value[0][0] == 0:
                    variables['IT'] = 'FAIL'
                else:
                    variables['IT'] = 'WIN'
                match(tokens, 'TROOF')
            elif tokens[0][1] == 'YARN':
                variables['IT'] = str('"' + value[0][0] + '"')
                match(tokens, 'YARN')
        elif value and value[0][1] == 'NUMBAR_LITERAL':
            if tokens[0][1] == 'NUMBR':
                variables['IT'] = int(float(value[0][0]))
                match(tokens, 'NUMBR')
            elif tokens[0][1] == 'TROOF':
                if value[0][0] == 0.0:
                    variables['IT'] = 'FAIL'
                else:
                    variables['IT'] = 'WIN'
                match(tokens, 'TROOF')
            elif tokens[0][1] == 'YARN':
                variables['IT'] = str('"' + str(round(float(value[0][0]),2)) + '"')
                match(tokens, 'YARN')
        elif value and value[0][1] == 'YARN_LITERAL':
            raw_value = value[0][0][1:-1]
            if all(char.isdigit() or char == '-' or char == '.' for char in raw_value):
                if tokens[0][1] == 'NUMBR':
                    if '.' in raw_value:
                        raw_value = raw_value.split('.')[0]
                        if raw_value == "":
                            raw_value = "0"
                    variables['IT'] = int(raw_value)
                    match(tokens, 'NUMBR')
                elif tokens[0][1] == 'NUMBAR':
                    variables['IT'] = float(raw_value)
                    match(tokens, 'NUMBAR')
        elif value and value[0][1] == 'NOOB_LITERAL':
            if tokens[0][1] == 'NUMBR':
                variables['IT'] = 0
                match(tokens, 'NUMBR')
            elif tokens[0][1] == 'NUMBAR':
                variables['IT'] = 0.0
                match(tokens, 'NUMBAR')
            elif tokens[0][1] == 'YARN':
                variables['IT'] = ""
                match(tokens, 'YARN')

def parse_input_statements(tokens):
    match(tokens, 'GIMMEH')
    if tokens and tokens[0][1] == 'IDENTIFIER':
        variable_name = tokens[0][0]
        match(tokens, 'IDENTIFIER')
        user_input = simpledialog.askstring("Input", f"Enter value for variable '{variable_name}':")
        variables[variable_name] = user_input
    else:
        raise SyntaxError("Expected variable name, got {}".format(tokens[0][1]))

def parse_parameters(tokens):
    while tokens and tokens[0][1] == 'YR':
        tokens.pop(0)  # Skip "YR"
        match(tokens, 'IDENTIFIER')
