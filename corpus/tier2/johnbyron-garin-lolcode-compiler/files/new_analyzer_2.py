# modules imported
from turtle import goto
from lexer import *
from tkinter import simpledialog

output = [""] # used to store the results of the program
error = "" # used to store error messages if any occur during parsing or execution of the program
variables = {"IT": ""} # initializes a dictionary with an initial key-value pair
literals = ['TROOF_LITERAL', 'NUMBR_LITERAL', 'NUMBAR_LITERAL', 'YARN_LITERAL', 'NOOB_LITERAL'] # a list containing string literals representing different types
# a list containing various operations or keywords that the parser seems to recognize
operations = ['SUM_OF', 'DIFF_OF', 'PRODUKT_OF', 'QUOSHUNT_OF', 'MOD_OF', 'BIGGR_OF', 'SMALLR_OF', 'SMOOSH', 'BOTH_OF', 'EITHER_OF', 'WON_OF', 'NOT', 'ALL_OF', 'ANY_OF', 'BOTH_SAEM', 'DIFFRINT']
# arith_operations = ['SUM_OF', 'DIFF_OF', 'PRODUKT_OF', 'QUOSHUNT_OF', 'MOD_OF', 'BIGGR_OF', 'SMALLR_OF']
# bool_operations = ['BOTH_OF', 'EITHER_OF', 'WON_OF', 'NOT', 'ALL_OF', 'ANY_OF']


# Matching tokens to check if it is expected
def match(tokens, expected_type):
    if tokens and tokens[0][1] == expected_type:
        tokens.pop(0)
    else:
        error = "Expected {expected_type}, got {tokens[0][1]}"

# Printing
def display(tokens):
    match(tokens, 'VISIBLE')
    result = ""
    while tokens:
        if tokens[0][1] in operations:
            value = parse_expression(tokens)
            result += parse_toYarn(value)
        elif tokens[0][1] == "IDENTIFIER" and tokens[0][0] in variables:
            result += str(variables[tokens[0][0]])
            tokens.pop(0)
        else:
            if tokens[0][1] == "YARN_LITERAL":
                result += tokens[0][0].replace("\"", "")
            else: result += str(tokens[0][0])
            tokens.pop(0)

        if len(tokens) == 0: break
        elif tokens and tokens[0][1] != 'PLUS':
            break
        else:
            result += " "
            match(tokens, 'PLUS')

    output.append(result)
    return tokens

'''
this function initializes some global variables, 
handles comments at the beginning of the program, 
parses the statements within the program, 
and returns the result or any encountered errors
'''
def parse_program(tokens):
    output.clear() 
    variables.clear() 
    while tokens[0][1] == "INLINE_COMMENT" or tokens[0][1] == "MULTI_LINE_COMMENT":
        if tokens[0][1] == "INLINE_COMMENT":
            match(tokens, 'INLINE_COMMENT')
        elif tokens[0][1] == "MULTI_LINE_COMMENT":
            match(tokens, 'MULTI_LINE_COMMENT')
    match(tokens, 'HAI') # consumes the 'HAI' token, which marks the beginning of a LOLCODE program
    parse_statements(tokens)
    if error != "":
        output.append(error)
        return output
    else:
        match(tokens, 'KTHXBYE') # consumes the 'KTHXBYE' token, which marks the end of the LOLCODE program
        return output

'''
handle different types of statements based on the type of the first token in the list
depending on the token type, it calls the appropriate functions to parse and execute the statements
'''
def parse_statements(tokens):
    '''
    this function is designed to parse statements from a list of tokens
    it uses a while loop to iterate through the tokens until the list is empty
    '''
    global error
    error = ""
    while tokens:
        if tokens[0][1] == "WAZZUP": parse_variable_declaration(tokens)
        elif tokens[0][1] == 'INLINE_COMMENT': match(tokens, 'INLINE_COMMENT')
        elif tokens[0][1] == 'MULTI_LINE_COMMENT': match(tokens, 'MULTI_LINE_COMMENT')
        elif tokens[0][1] in operations:
            variables["IT"] = parse_expression(tokens)
        elif tokens[0][1] == 'IDENTIFIER':
            if tokens[1][1] == 'R':
                parse_assignment(tokens)
            else:
                variables["IT"] = variables[tokens[0][0]]
                tokens.pop(0)
        elif tokens[0][1] == 'GIMMEH':
            parse_input_statements(tokens)
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
        elif tokens[0][1] == 'HOW_IZ_I':
            parse_func_definition(tokens)
        elif tokens[0][1] == 'I_IZ':
            variables['IT'] = parse_func_return(tokens)
        elif tokens[0][1] == 'VISIBLE':
            tokens = display(tokens)
        elif tokens[0][1] == 'KTHXBYE' or len(tokens) == 0:
            break
        else:
            error = "Unexpected token: " + str({tokens[0][0]})
            break
            # raise SyntaxError(f"Unexpected token: {tokens[0][0]}")

# Variables
def parse_variable_declaration(tokens):
    match(tokens, 'WAZZUP') # ensures that the declaration of variables starts with the keyword 'WAZZUP'
    while tokens:
        '''
        checks if the first token is a comment
        '''
        if tokens[0][1] == 'INLINE_COMMENT':
            match(tokens, 'INLINE_COMMENT')
        elif tokens[0][1] == 'MULTI_LINE_COMMENT':
            match(tokens, 'MULTI_LINE_COMMENT')
        elif tokens[0][1] == 'BUHBYE': # the loop terminates if 'BUHBYE' is detected signaling the end of variable declaration
            break
        else: # else, it means there's an actual variable declaration
            '''
            the I_HAS_A token is matched, and the name of the variable is extracted from the next token, which is expected to be an identifier
            '''
            match(tokens, 'I_HAS_A')
            variable_name = tokens[0][0]
            match(tokens, 'IDENTIFIER')
            if tokens and tokens[0][1] == 'ITZ':
                match(tokens, 'ITZ') # there is an initialization of the variable
                if tokens and tokens[0][1] in operations:
                    variables[variable_name] = parse_expression(tokens) # parses the expression and assigns the result to the variable
                else:
                    variables[variable_name] = tokens.pop(0)[0]  # TO FIX: SKIPPING INITIALIZATION
            else: # if there is no 'ITZ' token after the identifier, it means the variable is not initialized, and the default value "NOOB" is assigned
                variables[variable_name] = "NOOB"
    match(tokens, 'BUHBYE') # the 'BUHBYE' token is matched to ensure the end of the variable declaration section

# GIMMEH

# EXPRESSIONS
'''
responsible for parsing arithmetic, string concatenation, boolean, and comparison expressions
'''
def parse_expression(tokens):

    # Arithmetic
    '''
    these lines handle arithmetic operations
    the lambda functions inside the calls represent the actual operation to be performed on the operands
    '''
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
    elif tokens[0][1] == 'BOTH_OF': return parse_boolean_operation(tokens, 'BOTH_OF', lambda x, y: x and y)
    elif tokens[0][1] == 'EITHER_OF': return parse_boolean_operation(tokens, 'EITHER_OF', lambda x, y: x or y)
    elif tokens[0][1] == 'WON_OF': return parse_boolean_operation(tokens, 'WON_OF', lambda x, y: x ^ y)
    elif tokens[0][1] == 'NOT': return parse_not(tokens)
    elif tokens[0][1] == 'ALL_OF': return parse_toTroof(parse_all(tokens))
    elif tokens[0][1] == 'ANY_OF': return parse_toTroof(parse_any(tokens))

    # Comparison
    elif tokens[0][1] == 'BOTH_SAEM': 
        result = parse_binary_operation(tokens, tokens[0][1], lambda x, y: x == y)
        if result == True: return 'WIN'
        else: return 'FAIL'
    elif tokens[0][1] == 'DIFFRINT': 
        result = parse_binary_operation(tokens, tokens[0][1], lambda x, y: x != y)
        if result == True: return 'WIN'
        else: return 'FAIL'

    return None

'''
responsible for parsing binary operations in LOLCODE
it checks the correctness of the operator, 
extracts the left and right operands, 
applies the specified operation function, 
and returns the result
'''
def parse_binary_operation(tokens, operator, operation_fn):
    match(tokens, operator)
    x = parse_operand(tokens)
    match(tokens, 'AN')
    y = parse_operand(tokens)
    result = operation_fn(x, y)
    return result

'''
responsible for parsing different types of operands in LOLCODE, 
including numeric literals, variables, and expressions
'''
def parse_operand(tokens):
    # extracts the numeric value from the token, converts it to an integer, removes the token from the list, and returns the integer value
    if tokens and tokens[0][1] == 'NUMBR_LITERAL':
        value = int(tokens[0][0])
        tokens.pop(0)
        return value
    # extracts the numeric value from the token, converts it to a float, removes the token from the list, and returns the float value
    elif tokens and tokens[0][1] == 'NUMBAR_LITERAL':
        value = float(tokens[0][0])
        tokens.pop(0)
        return value
    # creates a list containing the current token, removes the token from the list, and then calls parse_typecasting to handle typecasting if needed
    elif tokens and tokens[0][1] in ['TROOF_LITERAL', 'YARN_LITERAL']:
        value = [tokens[0]]
        tokens.pop(0)
        return parse_typecasting(tokens, value, True)
    # gets the value of the identifier from the variables dictionary, tokenizes it, and then calls parse_typecasting to handle typecasting
    elif tokens and tokens[0][1] == 'IDENTIFIER':
        value = tokenize(str(variables[tokens[0][0]]))
        tokens.pop(0)
        typecasted = parse_typecasting(tokens, value, True)
        if (typecasted == 'FAIL'):
            return None
        return parse_typecasting(tokens, value, True)
    elif tokens and tokens[0][1] in operations:
        return parse_expression(tokens)
    # if none are satisfied, it raises a SyntaxError with a message indicating that it expected a diff datatype but got something else
    else:
        raise SyntaxError("Expected numeric literal, variable, or arithmetic expression, got {}".format(tokens[0][1]))

# function that handles boolean operations
def parse_boolean_operation(tokens, operator, operation_fn):
    match(tokens, operator)
    x = parse_bool_operand(tokens)
    match(tokens, 'AN')
    y = parse_bool_operand(tokens)
    result = operation_fn(x, y)
    return parse_toTroof(result)

'''
function designed to parse boolean operands, 
which can be literals (like 'WIN' or 'FAIL'), 
identifiers (variable names), 
numeric literals converted to boolean, 
or complex boolean expressions using boolean operators
'''
def parse_bool_operand(tokens):
    if tokens and tokens[0][1] == 'TROOF_LITERAL':
        value = tokens[0][0]
        tokens.pop(0)
        return parse_toBool(value)
    elif tokens and tokens[0][1] == 'IDENTIFIER':
        value = variables[tokens[0][0]]
        tokens.pop(0)
        return parse_toBool(value)
    elif tokens[0][1] == 'NUMBR_LITERAL':
        value = variables[tokens[0][0]]
        tokens.pop(0)
        return parse_toBool(parse_toTroof(value))
    elif tokens and tokens[0][1] in ['BOTH_OF', 'EITHER_OF', 'WON_OF', 'ANY_OF', 'ALL_OF', 'NOT']:
        return parse_expression(tokens)
    else:
        raise SyntaxError("Expected boolean literal or boolean expression, got {}".format(tokens[0][1]))

# handles the negation operand
def parse_not(tokens):
    match(tokens, 'NOT')
    x = parse_bool_operand(tokens)
    return not x

def parse_all(tokens):
    match(tokens, 'ALL_OF')
    operands = []
    result = True

    # Loop to parse boolean operands until 'MKAY' is encountered
    while tokens and tokens[0][1] != 'MKAY':
        '''
        raises an error if 'ALL_OF' or 'ANY_OF' is encountered as an operand
        '''
        if tokens[0][1] in ['ALL_OF', 'ANY_OF']:
            raise SyntaxError("ALL_OF and ANY_OF cannot be operands for ALL_OF")
        operands.append(parse_bool_operand(tokens)) # parses a boolean operand and add it to the list of operands
        '''
        if there are tokens left in the list and the first token is 'AN', it matches and removes the 'AN' token
        '''
        if tokens and tokens[0][1] == 'AN':
            match(tokens, 'AN')

    '''
    if there are no operands in the operands list, it raises a SyntaxError because 'ALL_OF' requires at least one operand
    '''
    if not operands:
        raise SyntaxError("Expected at least one operand for ALL_OF, got none")
    
    '''
    iterates over each operand in the operands list
    if any operand is either 'FAIL' or False, it sets the result variable to False and breaks out of the loop
    '''
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

    # Loop to parse boolean operands until 'MKAY' is encountered
    while tokens and tokens[0][1] != 'MKAY':
        '''
        raises an error if 'ALL_OF' or 'ANY_OF' is encountered as an operand
        '''
        if tokens[0][1] in ['ALL_OF', 'ANY_OF']:
            raise SyntaxError("ALL_OF and ANY_OF cannot be operands for ANY_OF")
        operands.append(parse_bool_operand(tokens)) # parses a boolean operand and add it to the list of operands
        '''
        if there are tokens left in the list and the first token is 'AN', it matches and removes the 'AN' token
        '''
        if tokens and tokens[0][1] == 'AN':
            match(tokens, 'AN')

    '''
    if there are no operands in the operands list, it raises a SyntaxError because 'ANY_OF' requires at least one operand
    '''
    if not operands:
        raise SyntaxError("Expected at least one operand for ANY_OF, got none")

    '''
    iterates over each operand in the operands list
    if any operand is either 'WIN' or True, it sets the result variable to True and breaks out of the loop
    '''
    for troof in operands:
        if troof in ['WIN', True]:
            result = True
            break
        else:
            continue

    match(tokens, 'MKAY')
    return result

'''
this function essentially processes a sequence of tokens representing a SMOOSH operation and 
constructs a string by concatenating the corresponding values
'''
def parse_concat(tokens):
    match(tokens, 'SMOOSH')
    concatenated_strings = [] # used to store the strings that will be concatenated
    
    '''
    while loop that continues as long as there are tokens in the tokens list, 
    and the first token has a type (second element in the tuple) that is one of the specified literals
    '''
    while tokens and (tokens[0][1] in ['YARN_LITERAL', 'NUMBR_LITERAL', 'NUMBAR_LITERAL', 'TROOF_LITERAL', 'IDENTIFIER']):
        '''
        if the first token is of type 'YARN_LITERAL', 
        this block extracts the string value (excluding the double quotes) and appends it to the concatenated_strings list
        '''
        if tokens[0][1] == 'YARN_LITERAL':
            concatenated_strings.append(tokens[0][0][1:-1])
        elif tokens[0][1] == 'IDENTIFIER':
            '''
            if the first token is of type 'IDENTIFIER', 
            this block gets the variable name, 
            looks up its value in the variables dictionary, 
            and appends the string representation of the value (or an empty string if the variable is not found) to the concatenated_strings list
            '''
            variable_name = tokens[0][0]
            concatenated_strings.append(str(variables.get(variable_name, '')))
        else:
            concatenated_strings.append(str(tokens[0][0]))
        tokens.pop(0)
        
        '''
        if the next token is 'AN', it removes it as well
        this is to handle multiple concatenation operations
        if 'AN' is not found, the loop breaks
        '''
        if tokens and tokens[0][1] == 'AN':
            tokens.pop(0)
        else:
            break
    #uses the join method to concatenate all the strings in the list into a single string, using an empty string as the separator
    result = ''.join(concatenated_strings)
    return result

def parse_assignment(tokens):
    variable_name = tokens[0][0]
    # TO DO: Check if valid variable 

    match(tokens, 'IDENTIFIER')

    # if variables[variable_name] != "NOOB":
    #     if tokens and tokens[0][1] == 'IS_NOW_A':
    #         match(tokens, 'IS_NOW_A')
    #         value = tokenize(variables[variable_name])
    #         parse_typecasting(tokens, value, False)
    #         variables[variable_name] = variables['IT']
    #     if tokens and tokens[0][1] == 'R':
    #         match(tokens, 'R')
    #         match(tokens, 'MAEK')
    #         value = tokenize(variables[variable_name])
    #         tokens.pop(0)
    #         parse_typecasting(tokens, value, False)
    #         variables[variable_name] = variables['IT']
    # else:
    match(tokens, 'R')
    if tokens and tokens[0][1] in operations:
        variables[variable_name] = parse_expression(tokens)
    elif tokens and tokens[0][1] == 'IDENTIFIER'  and tokens[0][0] in variables:
        variables[variable_name] = variables[tokens[0][0]]
        tokens.pop(0)
    elif tokens and tokens[0][1] == 'MAEK':
        parse_typecasting(tokens)
        variables[variable_name] = variables['IT']
    else:
        variables[variable_name] = tokens[0][0]
        tokens.pop(0)

# Typecasting
'''
it doesn't perform any meaningful typecasting but simply returns None
'''
def parse_toNoob(returned):
    return None

'''
it checks the type of the returned value using the check_type function
if the type is 'TROOF_LITERAL', it directly returns the returned value
if the value is False, 0, 0.0, or an empty string, it returns 'FAIL'
otherwise, it returns 'WIN'.
'''
def parse_toTroof(returned):
    if check_type(returned) == 'TROOF_LITERAL': return returned
    elif returned == False or returned == 0 or returned == 0.0 or returned == "": return 'FAIL'
    else: return 'WIN'

'''
it checks various conditions to determine the appropriate typecasting:
    -> if returned is 'WIN', it returns 1.0
    -> if returned is 'FAIL', it returns 0
    -> if the type of returned is 'NUMBR_LITERAL' or it's a numerical yarn (checked using is_yarn_numerical), 
        it converts it to a float using float(returned)
    -> if the type is 'NUMBAR_LITERAL', it directly returns returned
    -> if the type is 'NOOB_LITERAL', it sets an error message in the error variable
    -> it returns None if none of the conditions are met
'''
def parse_toNumbar(returned):
    global error
    if returned == 'WIN': return 1.0
    elif returned == 'FAIL': return 0
    elif check_type(returned) == 'NUMBR_LITERAL' or (check_type(returned) == 'YARN_LITERAL' and is_yarn_numerical(returned) == True): return float(returned)
    elif check_type(returned) == 'NUMBAR_LITERAL': return returned
    elif check_type(returned) == 'NOOB_LITERAL': error = "NOOB cannot be typecasted to NUMBAR."
    return None

'''
this function is similar to parse_toNumbar,
iit performs typecasting to integers instead of floats
'''
def parse_toNumbr(returned):
    global error
    if returned == 'WIN': return 1
    elif returned == 'FAIL': return 0
    elif check_type(returned) == 'NUMBAR_LITERAL' or (check_type(returned) == 'YARN_LITERAL' and is_yarn_numerical(returned) == True): return int(parse_toNumbar(returned))
    elif check_type(returned) == 'NUMBR_LITERAL': return returned
    elif check_type(returned) == 'NOOB_LITERAL': error = "NOOB cannot be typecasted to NUMBR."
    return None

'''
this function is responsible for typecasting the input returned to a YARN (string) representation
'''
def parse_toYarn(returned):
    global error
    if check_type(returned) == 'NUMBAR_LITERAL': return str(round(returned, 2))
    elif check_type(returned) == 'NUMBR_LITERAL': return str(returned)
    elif check_type(returned) == 'YARN_LITERAL' or check_type(returned) == 'TROOF_LITERAL': return str(returned)
    elif check_type(returned) == 'NOOB_LITERAL': 
        error = "NOOB cannot be typecasted to NUMBR."
        return None
    elif returned == True: return 'WIN'
    elif returned == False: return 'FAIL'
    else: 
        return returned

'''
this function converts the string representations 'WIN' and 'FAIL' to boolean values True and False, respectively
'''
def parse_toBool(returned):
    if returned == 'WIN': return True
    elif returned == 'FAIL': return False

'''
this function uses the tokenize function to determine the type of the returned value
'''
def check_type(returned):
    token = tokenize(str(returned))
    return token[0][1]

def is_yarn_numerical(returned):
    '''
    this line checks if the first character of the returned string is a minus sign 
    if it is, it removes the minus sign from the string to handle negative numbers
    '''
    if returned[0] == '-': returned = returned[1:]
    valid = True # used to keep track of whether the string is a valid numerical representation
    one_period = False # used to ensure that there is at most one decimal point in the string
    for char in returned: # a loop that iterates over each character in the returned string
        if char.isdigit() == False: # this condition checks if the character is not a digit
            if one_period == False and char == '.': # checks if a decimal point has been encountered
                one_period = True
            else:  # the string is not a valid numerical representation
                valid = False
                break
    '''
    if the last character of the string is a period, it sets valid to False
    this ensures that the string doesn't end with a decimal point, making it an invalid numerical representation
    '''
    if returned[-1] == '.': valid = False
    return valid
    
# If Else
def parse_ifelse(tokens):
    # calls the parse_toTroof function to convert the value of the variable 'IT' in the variables dictionary to a boolean value 
    considered_expression = parse_toTroof(variables['IT'])
    if_statement = [] # used to store the tokens of the "YA_RLY" block
    else_statement = [] # used to store the tokens of the "NO_WAI" block
    match(tokens, 'O_RLY')
    match(tokens, 'YA_RLY')
    '''
    a while loop that continues as long as there are tokens in the list
        adds the first token in the list to the if_statement list and removes it from the list
        checks if the first token after the 'YA_RLY' token is 'OIC' or 'NO_WAI'
            if either condition is true, the loop breaks
    '''
    while (tokens):
        if_statement.append(tokens.pop(0))
        if tokens[0][1] == 'OIC' or tokens[0][1] == 'NO_WAI':
            break
    match(tokens, 'NO_WAI')
    '''
    another while loop that continues as long as the first token in the list is not 'OIC'
        adds the first token in the list to the else_statement list and removes it from the list
    '''
    while (tokens[0][1] != 'OIC'):
        else_statement.append(tokens.pop(0))
    match(tokens, 'OIC')
    '''
    checks if the considered_expression is true, then it enters the block and executes the statements inside the "YA_RLY" block
    '''
    if considered_expression:
        parse_statements(if_statement)
    else:
        parse_statements(else_statement)

'''
this function essentially implements a switch statement in LOLCODE, 
allowing different code blocks to be executed based on the value of the variable IT
'''
# Switch
def parse_switch(tokens):
    accepted_omg = 0 # used to track if any condition in the switch statement is accepted
    value_to_compare = variables['IT'] # retrieves the value to compare from the variable IT in the variables dictionary
    match(tokens, 'WTF')
    tokens_to_eval = [] # used to store the tokens to be evaluated within each condition block
    '''
    a while loop that continues until it encounters 'OMGWTF'
    within the loop, it checks if the next token is 'OMG' using the match function
    '''
    while tokens[0][1] != 'OMGWTF':
        match(tokens, 'OMG')
        '''
        checks the type of the next token by checking:
            ->if it's a 'TROOF_LITERAL', it sets condition_value to the literal value
            ->if it's a 'YARN_LITERAL', it extracts the string value by removing the double quotes
            ->if it's neither of the above, it calls parse_typecasting to typecast the value
        '''
        if tokens[0][1] in ['TROOF_LITERAL']:
            condition_value = tokens[0][0]
        elif tokens[0][1] in ['YARN_LITERAL']:
            condition_value = tokens[0][0][1:-1]
        else:
            condition_value = parse_typecasting(tokens, [tokens[0]], True)
        '''
        if value_to_compare and condition_value matched, it sets accepted_omg to 1 and consumes the current token using match
        '''
        if value_to_compare == condition_value:
            accepted_omg = 1
            match(tokens, tokens[0][1])
            '''
            enters a while loop to gather the tokens until it encounters another 'OMG' or 'OMGWTF'
                appends each token to tokens_to_eval
            calls parse_statements with the collected tokens, effectively parsing and executing the statements within the condition block
            '''
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
    match(tokens, 'OIC') # matches 'OIC' to conclude the switch statement

# Loops
def parse_loop(tokens):
    match(tokens, 'IM_IN_YR') # ensure that the first token in the tokens list is 'IM_IN_YR'
    loopName = tokens[0][0] # retrieves the identifier following 'IM_IN_YR' and assigns it to the variable loopName
    match(tokens, 'IDENTIFIER')
    increment = 0
    if tokens[0][1] == 'UPPIN':
        '''
        checks if the next token is 'UPPIN'
            if true, sets the increment variable to 1
            matches and removes the 'UPPIN' token
        '''
        increment = 1
        match(tokens, 'UPPIN')
    elif tokens[0][1] == 'NERFIN':
        '''
        checks if the next token is 'NERFIN'
            if true, sets the increment variable to -1
            matches and removes the 'NERFIN' token
        '''
        increment = -1
        match(tokens, 'NERFIN')

    match(tokens, 'YR') # matches and removes the 'YR' token
    variableName = tokens[0][0] # retrieves the identifier following 'YR' and assigns it to the variable variableName
    value = variables[variableName] # retrieves the value associated with the "variableName" from the variables dictionary
    '''
    if the type of the value is 'TROOF_LITERAL',
    typecasts the value to a numeric representation using the parse_toNumbr function
    '''
    if check_type(value) == 'TROOF_LITERAL': value = parse_toNumbr(value)
    match(tokens, 'IDENTIFIER')
    '''
    if the next token is 'TIL', sets repeat_condition to 'FAIL
    if the next token is 'WILE', sets repeat_condition to 'WIN'
    '''
    if tokens[0][1] == 'TIL': 
        repeat_condition = 'FAIL'
    elif tokens[0][1] == 'WILE': 
        repeat_condition = 'WIN'
    match(tokens, tokens[0][1])
    tokens_to_eval = []
    save_token_state = tokens.copy() # a copy of the current state of the tokens list.
    while save_token_state[0][1] != 'IM_OUTTA_YR' and save_token_state[1][0] != loopName:
        tokens_to_eval.append(save_token_state.pop(0))
    consumer = tokens_to_eval.copy()
    while parse_toTroof(parse_expression(consumer)) == repeat_condition:
        parse_statements(consumer)
        updated_value = int(variables[variableName]) + increment
        variables[variableName] = updated_value
        consumer = tokens_to_eval.copy()
    while tokens[0][1] != 'IM_OUTTA_YR' and tokens[1][0] != loopName:
        tokens.pop(0)
    match(tokens, 'IM_OUTTA_YR')
    match(tokens, 'IDENTIFIER')


functions = {} # initializes an empty dictionary to store information about defined functions

'''
responsible for parsing the definition of a function
'''
# Functions    
def parse_func_definition(tokens):
    global functions
    match(tokens, 'HOW_IZ_I') # signifies the beginning of a function definition

    func_name = tokens[0][0] # retrieves the name of the function from the second token in the list
    func_variables = [] # an empty list to store the parameters of the function
    match(tokens, 'IDENTIFIER') # ensures that the next token is an identifier (the name of the function)

    func_variables = []
    '''
    processes the parameters of the function
        iterates through the tokens, appending the parameter names to the func_variables list until there are no more parameters
        the 'AN' keyword is optional between parameters
    '''
    while tokens[0][1] == "YR":
        match(tokens, 'YR')
        func_variables.append(tokens[0][0])
        match(tokens, 'IDENTIFIER')
        if tokens[0][1] == 'AN': match(tokens, 'AN')

    tokens_to_eval = [] # an empty list to store the tokens that make up the body of the function
    '''
    processes the tokens constituting the body of the function
    appends tokens to the tokens_to_eval list until the closing token 'IF_U_SAY_SO' is encountered
    '''
    while tokens[0][1] != 'IF_U_SAY_SO':
        tokens_to_eval.append(tokens.pop(0))

    match(tokens, 'IF_U_SAY_SO') # ensures that the closing token 'IF_U_SAY_SO' is encountered after the function body
 
    func_var_dict = {} # an empty dictionary to store the function variables and their values
    '''
    populates the func_var_dict dictionary with the parameters of the function, 
    setting their initial values to an empty string
    '''
    for elem in func_variables:
        func_var_dict[elem] = ""

    '''
    a dictionary containing information about the function,
    including the:
        -> list of variable names, 
        -> the dictionary of variable names and their values, 
        -> the list of tokens representing the function body, 
        -> and the initial return value set to "NOOB"
    '''
    func_dict = {
        "variables_list": func_variables,
        "variables": func_var_dict.copy(), 
        "tokens_to_eval": tokens_to_eval.copy(),
        "return": "NOOB"
    }

    functions[func_name] = func_dict

def parse_func_return(tokens):
    global functions
    global variables
    match(tokens, 'I_IZ') # check if the first token in the tokens list is 'I_IZ'
    func_name = tokens[0][0]
    match(tokens, 'IDENTIFIER') # checks if the next token is an identifier and removes it from the tokens list
    param_index = 0 # used to keep track of the current parameter being processed
    '''
    a while loop that continues as long as the next token is "YR" (indicating function parameters)
        -> if the next token is an identifier and if it exists in the variables dictionary:
                assigns the value of the variable to the value variable
                removes the processed token from the token list
        -> if the next token is an operation:
                calls the parse_expression function to evaluate the expression and assigns the result to the value variable
        -> if the next token is a literal:
                assigns the literal value to the value variable
                removes the processed token from the token list
        
        -> stores the value of the parameter in the functions dictionary
        -> increments the param_index to move to the next parameter
        -> checks if there is an "AN" token after processing a parameter and removes it from the tokens list if present
    '''
    while tokens[0][1] == "YR":
        match(tokens, 'YR') # checks and removes the "YR" token from the tokens list
        if tokens[0][1] == 'IDENTIFIER' and tokens[0][0] in variables:
            value = variables[tokens[0][0]]
            tokens.pop(0)
        elif tokens[0][1] in operations:
            value = parse_expression(tokens)
        elif tokens[0][1] in literals:
            value = tokens[0][0]
            tokens.pop(0)
        functions[func_name]["variables"][functions[func_name]["variables_list"][param_index]] = value
        param_index += 1
        if tokens[0][1] == 'AN': match(tokens, 'AN')

    save_variables = variables.copy() # creates a copy of the variables dictionary
    variables = functions[func_name]["variables"] # the function will now use its own set of variables
    parse_function_body(functions[func_name]["tokens_to_eval"], func_name, functions[func_name]["variables"]) # processes the body of the function
    variables = save_variables.copy() # restores the original state of the global variables dictionary
    return functions[func_name]["return"]

def parse_function_body(tokens, func_name, variables):
    global functions
    global error
    error = ""
    '''
    loop that will continue iterating as long as there are tokens in the tokens list:
        -> if the first token in the list has type 'INLINE_COMMENT':
                it calls the match function to consume that token and move to the next one
        -> if the first token in the list has type 'MULTI_LINE_COMMENT':
                it calls the match function to consume that token and move to the next one
        -> if the first token is an operation:
                it calls the parse_expression function to parse the expression and 
                assigns the result to the variable with the key "IT" in the local variables dictionary
        -> if the first token is an 'IDENTIFIER' and:
                -> if the second token is 'R':
                    it calls the parse_assignment function to handle the assignment operation
                -> if the second token is not 'R':
                    it  then assigns the value of that variable to the "IT" variable in the local variables dictionary and 
                    removes the first token from the list
        -> if the first token is 'GIMMEH':
                it calls the parse_input_statements function to handle input statements
        -> if the first token is 'MAEK':
                it matches 'MAEK' using the match function
                then it creates a value by tokenizing the variable's value
                it consumes the next token (variable name) and matches 'A'
                it then calls parse_typecasting to handle typecasting
        -> if the first token is 'O_RLY':
                it calls parse_ifelse to handle an if-else block
        -> if the current token is of type 'WTF':
                it calls the parse_switch function
        -> if the current token is of type 'IM_IN_YR':
                it calls the parse_loop function
        -> if the current token is of type 'HOW_IZ_I':
                it calls the parse_func_definition function
        -> if the current token is of type 'I_IZ':
                it sets the 'IT' variable to the result of parse_func_return function
        -> if the current token is of type 'VISIBLE':
                it calls the display function and 
                assigns its result back to the tokens variable
        -> If the current token is of type 'FOUND_YR':
                it proceeds to match the token and then checks the type of the next token

                -> if it's an 'IDENTIFIER' and exists in the variables:
                        it assigns the corresponding value to the function return in the functions dictionary
                -> if it's an operation:
                        it assigns the result of parsing the expression to the function return
                -> if it's a literal:
                        it assigns the literal value to the function return
        -> if the current token is 'GTFO' or there are no more tokens:
                it breaks out of the loop
        -> if none of the above conditions are met:
                it sets an error message indicating an unexpected token and 
                breaks out of the loop
    '''
    while tokens:
        if tokens[0][1] == 'INLINE_COMMENT': match(tokens, 'INLINE_COMMENT')
        elif tokens[0][1] == 'MULTI_LINE_COMMENT': match(tokens, 'MULTI_LINE_COMMENT')
        elif tokens[0][1] in operations:
            variables["IT"] = parse_expression(tokens)
        elif tokens[0][1] == 'IDENTIFIER':
            if tokens[1][1] == 'R':
                parse_assignment(tokens)
            else:
                variables["IT"] = variables[tokens[0][0]]
                tokens.pop(0)
        elif tokens[0][1] == 'GIMMEH':
            parse_input_statements(tokens)
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
        elif tokens[0][1] == 'HOW_IZ_I':
            parse_func_definition(tokens)
        elif tokens[0][1] == 'I_IZ':
            variables['IT'] = parse_func_return(tokens)
        elif tokens[0][1] == 'VISIBLE':
            tokens = display(tokens)
        elif tokens[0][1] == 'FOUND_YR':
            match(tokens, 'FOUND_YR')
            if tokens[0][1] == 'IDENTIFIER' and tokens[0][0] in variables:
                functions[func_name]["return"] = variables[tokens[0][0]]
                tokens.pop(0)
            elif tokens[0][1] in operations:
                functions[func_name]["return"] = parse_expression(tokens)
            elif tokens[0][1] in literals:
                functions[func_name]["return"] = tokens[0][0]
                tokens.pop(0)
            break
        elif tokens[0][1] == 'GTFO' or len(tokens) == 0:
            break
        else:
            error = "Unexpected token: " + str({tokens[0][0]})
            break
            # raise SyntaxError(f"Unexpected token: {tokens[0][0]}")

'''
this function handles different types of literals and 
typecasts them accordingly based on the conditions
the return values are the typecasted values
'''
def parse_typecasting(tokens, value, isImplicit):
    global error
    if isImplicit: # checks if the typecasting is implicit
        if value and value[0][1] == 'TROOF_LITERAL':
            if value[0][0] == 'WIN':
                return 1
            else:
                return 0
        if value and value[0][1] == 'NUMBR_LITERAL':
            return int(value[0][0])
        if value and value[0][1] == 'NUMBAR_LITERAL':
            return float(value[0][0])
        '''
        -> if the value is a YARN_LITERAL:
            it extracts raw_value by removing the quotes from the string
            it checks if the raw_value is a valid integer or float using the all function and a generator expression
            -> if it's a valid numeric string:
                    it returns either the integer or float value based on the presence of a decimal point
            -> if it's not a numeric string but 'WIN' or 'FAIL':
                    it calls parse_toBool for typecasting to boolean
        '''
        if value and value[0][1] == 'YARN_LITERAL':
            raw_value = value[0][0][1:-1]
            if all((char.isdigit() or char == '-' or char == '.') and (char != '-' or i == 0) for i, char in enumerate(raw_value)):
                if '.' in raw_value:
                    return float(raw_value)
                else :
                    return int(raw_value)
            else:
                if raw_value == 'WIN' or raw_value == 'FAIL':
                    return parse_toBool(raw_value)
        if value and value[0][1] == 'NOOB_LITERAL':
            return 'FAIL'
    
    else: # else the typecasting is explicit
        '''
        this code block checks the type of the literal value and performs explicit typecasting accordingly
        it sets the IT variable with the typecasted value and matches the expected token in the tokens list
        '''
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

'''
this function is designed to handle input statements
it checks for the presence of the 'GIMMEH' token, 
expects an 'IDENTIFIER' token next, 
prompts the user for input,
and updates the corresponding variable in the variables dictionary
'''
def parse_input_statements(tokens):
    match(tokens, 'GIMMEH')
    if tokens and tokens[0][1] == 'IDENTIFIER':
        variable_name = tokens[0][0]
        match(tokens, 'IDENTIFIER')
        user_input = simpledialog.askstring("Input", f"Enter value for variable '{variable_name}':")
        variables[variable_name] = user_input
    else:
        raise SyntaxError("Expected variable name, got {}".format(tokens[0][1])) # if the expected token is not an identifier, it raises a SyntaxError

'''
this function is designed to parse a sequence of tokens that represent parameters 
it assumes that parameters are marked with 'YR', and it skips the 'YR' token while ensuring that the next token is an 'IDENTIFIER'
'''
def parse_parameters(tokens):
    while tokens and tokens[0][1] == 'YR':
        tokens.pop(0)  # Skip "YR"
        match(tokens, 'IDENTIFIER')
