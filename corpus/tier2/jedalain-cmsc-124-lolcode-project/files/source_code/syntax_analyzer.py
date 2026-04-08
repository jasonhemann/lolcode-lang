import re

class Node:
    def __init__(self, node_type, value=None):
        self.type = node_type       # type of lexeme
        self.value = value          # value of lexeme
        self.children = []          # nested code inside the lexeme

    def add_child(self, child_node):
        self.children.append(child_node)
        
    def print_tree(self, level=0):
        indent = " " * (4 * level)
        node_value = f": {self.value}" if self.value else ""
        print(f"{indent}{self.type}{node_value}")
        for child in self.children:
            child.print_tree(level + 1)
 
# global variable
kthxbye_found = False
           
# -----------------------------------------------------------------------------------------
#  FUNCTION: Checks the correctness of the syntax of the code using the lexemes
#            from the lexical analyzer
# -----------------------------------------------------------------------------------------
def analyze_syntax(lexemes):
    operators = ["String Concatenation", "Arithmetic Operator", "Comparison Operator", "Boolean Operator", "Type Casting", "Type Conversion"]
    
    root = Node("Source Code")          # create the parse tree
    program_body = Node("Program Body") # node to contain all block of codes inside HAI and KTHXBYE
    functions = Node("Functions")       # node to contain all functions
    root.add_child(program_body)        # append node to root
    root.add_child(functions)        # append node to root
    
    in_program_body = False # flag to track if we are parsing block of codes inside HAI and KTHXBYE
    has_body_statements = False
    global kthxbye_found 
    
    while lexemes:
        lexeme, type_lxm, line_no = lexemes.pop(0)  # pop the first lexeme
        
        # parse codes inside the program body
        if in_program_body:
            # variable declaration
            if type_lxm == "Start Variable Declaration Environment":                                                  # variable declaration 
                # check if variable declaration is found at right place
                if has_body_statements: raise Exception(f"LINE {line_no + 1}: Variables should be declared first after \"HAI\"")
                
                variables_node = Node("Variable Declaration")   # create the node
                program_body.add_child(variables_node)          # append to tree
                parse_variables(lexemes, variables_node)        # parse declared variables

            # function
            elif type_lxm == "Function Start":
                has_body_statements = True
                lexemes.insert(0, (lexeme, type_lxm, line_no))
                parse_function(lexemes, functions)
            
            # end of program body
            elif type_lxm == "Code Delimiter End": 
                in_program_body = False                          # update flag
                bye_node = Node("Code Delimiter End", lexeme)    # create node for HAI
                program_body.add_child(bye_node)                 # append to program_body subtree
                kthxbye_found = True                             # update global flag for kthxbye
            # other expressions / statements
            else:
                has_body_statements = True
                parse_body(lexemes, program_body, lexeme, type_lxm, line_no)    # parse the body
                
        # we are still parsing outside of the program body (functions and comments are accepted)
        else:
            if lexeme == "HOW IZ I":  # function defined outside
                lexemes.insert(0, (lexeme, type_lxm, line_no))  # push back the keyword
                parse_function(lexemes, functions)

            elif lexeme == "HAI":       # start of program body
                in_program_body = True  # update flag
                
            else:
                raise Exception(f"LINE {line_no + 1}: Only function definition and comments can be found outside the program body")

    root.print_tree()
    return root

# -----------------------------------------------------------------------------------------
#  FUNCTION: Checks the correctness of the syntax of the code inside the body
# -----------------------------------------------------------------------------------------
def parse_body(lexemes, root, lexeme, type_lxm, line_no):
    operators = ["String Concatenation", "Arithmetic Operator", "Comparison Operator", "Boolean Operator"]
    
    # operations
    if type_lxm in operators:
        operator_node = Node("Operation")
        root.add_child(operator_node)
        lexemes.insert(0, (lexeme, type_lxm, line_no))  # push back operator
        parse_operation(lexemes, operator_node)
    
    # print statement
    elif type_lxm == "Output":
        output_node = Node("Output")
        root.add_child(output_node)
        lexemes.insert(0, (lexeme, type_lxm, line_no))  # push back "VISIBLE"
        parse_output(lexemes, output_node)              # parse print statement
        
    # output statement
    elif type_lxm == "Input":
        input_node = Node("Input")
        root.add_child(input_node)
        lexemes.insert(0, (lexeme, type_lxm, line_no))  # push back "GIMMEH"
        parse_input(lexemes, input_node)
    
    # type casting with MAEK
    elif lexeme == "MAEK" or any("MAEK" == lxm[0] for lxm in lexemes if lxm[2] == line_no):
        lexemes.insert(0, (lexeme, type_lxm, line_no))  # push back "MAEK" or the variable
        typecast_node = Node("Typecasting")
        root.add_child(typecast_node)
        parse_typecast(lexemes, typecast_node)                   # parse typecast
        
    # type casting with IS NOW A
    elif any("IS NOW A" in lxm[0] for lxm in lexemes if lxm[2] == line_no):
        lexemes.insert(0, (lexeme, type_lxm, line_no))  # push back the variable
        typecast_node = Node("Typecasting")
        root.add_child(typecast_node)
        parse_typecast(lexemes, typecast_node)                   # parse typecast
    
    # variable assignment
    elif type_lxm == "VARIABLE|FUNCTION|LOOP" and any("R" in lxm[0] for lxm in lexemes if lxm[2] == line_no):
        lexemes.insert(0, (lexeme, type_lxm, line_no))  # push back the variable
        assignment_node = Node("Assignment")
        root.add_child(assignment_node)
        parse_assignment(lexemes, assignment_node)
    
    # if-then statement
    elif type_lxm == "If Statement Start":
        lexemes.insert(0, (lexeme, type_lxm, line_no))  # push back the keyword
        if_then_node = Node("If-Then")
        root.add_child(if_then_node)
        parse_if_then(lexemes, if_then_node)
    
    # switch-case statement
    elif type_lxm == "Switch Statement Start":
        lexemes.insert(0, (lexeme, type_lxm, line_no))  # push back the keyword
        switch_case_node = Node("Switch-Case")
        root.add_child(switch_case_node)
        parse_switch_case(lexemes, switch_case_node)
    
    # loop statement
    elif type_lxm == "Loop Start":
        lexemes.insert(0, (lexeme, type_lxm, line_no))  # push back the keyword
        loop_node = Node("Loop")
        root.add_child(loop_node)
        parse_loop(lexemes, loop_node)
    
    # function definition
    elif type_lxm == "Function Start":
        lexemes.insert(0, (lexeme, type_lxm, line_no))  # push back the keyword
        function_node = Node(lexeme)
        root.add_child(function_node)
        parse_function(lexemes, function_node)
    
    # function call
    elif type_lxm == "Function Call":
        lexemes.insert(0, (lexeme, type_lxm, line_no))  # push back the keyword
        fxn_call_node = Node("Function Call")
        root.add_child(fxn_call_node)
        parse_function_call(lexemes, fxn_call_node)
        
    else:
        raise Exception(f"LINE {line_no + 1}: Invalid statement")
        
# -----------------------------------------------------------------------------------------
#  FUNCTION: Checks the correctness of the variable declaration block
# -----------------------------------------------------------------------------------------
def parse_variables(lexemes, root):
    while lexemes:
        lexeme, type_lxm, line_no = lexemes.pop(0)  # pop the first lexeme

        if lexeme == "BUHBYE":   # delimeter for variable declaration block
            buhbye_node = Node("End Variable Declaration Environment", lexeme)
            root.add_child(buhbye_node)  # append node to tree
            break

        elif lexeme == "I HAS A":  # declaring variable
            lexemes.insert(0, (lexeme, type_lxm, line_no))      # push I HAS A back to the list
            parse_variables_helper(lexemes, root)              # parse individual declarations
        
        else:
            raise Exception(f"LINE {line_no + 1}: Invalid variable declaration")
            
# -----------------------------------------------------------------------------------------
#  FUNCTION: Checks the correctness of individual variable declaration
# -----------------------------------------------------------------------------------------
def parse_variables_helper(lexemes, root):
    literals = ["NUMBR", "NUMBAR", "YARN", "TROOF", "NOOB"]
    nestable = ["Arithmetic Operator", "Comparison Operator", "Boolean Operator", "Type Casting", "Type Conversion"]
    nonnestable = ["String Concatenation", "Boolean Operator"]
    
    valid_args = literals + nestable + nonnestable
    
    prev_lexeme = None
    prev_type = None
    
    # flags
    has_value = False
    is_assigning_value = False
    is_done = False
    has_var_name = False
    
    while lexemes:
        lexeme, type_lxm, line_no = lexemes.pop(0)  # pop the first lexeme

        # end of declaration
        if is_done:
            # check if variable was initialized with value, if not, initialize it to None
            if not has_value:
                value_node = Node("Value", "None")                    # node to hold the value
                variable_node.add_child(value_node)                   # append to var_dec_node
                type_node = Node("Type", "None")                      # node to hold the type of the value
                variable_node.add_child(type_node)                    # append to var_dec_node
            
            if lexeme == "I HAS A" or lexeme == "BUHBYE": 
                lexemes.insert(0, (lexeme, type_lxm, line_no))
                break
            
            else: raise Exception(f"LINE {line_no + 1}: Invalid variable declaration")
        
        # assigning a value to variable
        elif is_assigning_value:                                  # ITZ was found previously, we will handle assigning the value
            value_node = Node("Value")                            # node to hold the value
            variable_node.add_child(value_node)                   # append to var_dec_node
            type_node = Node("Type")                              # node to hold the type of the value
            variable_node.add_child(type_node)                    # append to var_dec_node
            
             # assigning a literal value
            if prev_lexeme == "ITZ" and type_lxm in literals:  
                value_node.value = lexeme
                type_node.value = type_lxm
            
            # assigning a result from an operation  
            elif prev_lexeme == "ITZ" and type_lxm in valid_args:
                lexemes.insert(0, (lexeme, type_lxm, line_no))   # push the lexeme back
                parse_operation(lexemes, value_node)             # parse the operation
            
            # value is from a function call
            elif prev_lexeme == "ITZ" and type_lxm == "Function Call":
                lexemes.insert(0, (lexeme, type_lxm, line_no))
                parse_function_call(lexemes, value_node)
            
            else: raise Exception(f"LINE {line_no + 1}: Invalid variable assignment using {lexeme}")

            # update flags
            has_value = True
            is_assigning_value = False                      
            is_done = True  
            
        # create node for variable declaration
        else:
            # start of variable declaration aka 'I HAS A'
            if prev_lexeme == None and lexeme == "I HAS A":
                pass
            
            # variable name
            elif prev_lexeme == "I HAS A" and type_lxm == "VARIABLE|FUNCTION|LOOP":  
                variable_node = Node("Variable", lexeme)    # create node for variable
                root.add_child(variable_node)               # append to subtree
                has_var_name = True
            
            # variable with assigned value (ITZ)
            elif has_var_name and prev_type == "VARIABLE|FUNCTION|LOOP" and type_lxm == "Variable Assignment":
                is_assigning_value = True   # update flag
                
            # found new variable declaration or end of declaration
            elif prev_type == "VARIABLE|FUNCTION|LOOP" and lexeme == "I HAS A" or lexeme == "BUHBYE": 
                is_done = True  # update flag
                lexemes.insert(0, (lexeme, type_lxm, line_no))
                
            else: raise Exception(f"LINE {line_no + 1}: Invalid variable declaration")
        
        # save previous values  
        prev_lexeme = lexeme
        prev_type = type_lxm

# -----------------------------------------------------------------------------------------
#  FUNCTION: Checks the correctness of the syntax of operations
# -----------------------------------------------------------------------------------------
def parse_operation(lexemes, root):
    literals = ["NUMBR", "NUMBAR", "YARN", "TROOF", "NOOB"]
    non_nestable = ["String Concatenation", "Boolean Operator"]
    nestable = ["Arithmetic Operator", "Comparison Operator", "Boolean Operator", "Type Casting", "Type Conversion"]
    valid_args = ["VARIABLE|FUNCTION|LOOP"] + literals + nestable
    
    prev_lexeme = None
    prev_line_no = lexemes[0][2]
    arity = 0
              
    # flag
    is_unary = None
    is_binary = None
    is_inf = None
    
    while lexemes:
        lexeme, type_lxm, line_no = lexemes.pop(0)  # get current lexeme
        
        # break case - max arity reached OR line break
        if (is_binary and arity == 2) or (is_unary and arity == 1) or prev_line_no != line_no: 
            lexemes.insert(0, (lexeme, type_lxm, line_no))
            return 
        
         # break case - statement separator
        if (is_inf and arity > 0 and lexeme == "MKAY" or lexeme == "SMOOSHED"):
            return

        # parsing nestable operations
        if type_lxm in nestable and lexeme not in ["ANY OF", "ALL OF"]:
            if is_binary == None and is_unary == None and is_inf == None: # set flags
                if lexeme == "NOT": is_unary = True                       # unary
                else: is_binary = True                                    # binary
            
            lexemes.insert(0, (lexeme, type_lxm, line_no))
            
            if type_lxm == "Arithmetic Operator":
                root.value = "Arithmetic Operation"
                arity = parse_arithmetic_operation(lexemes, root)     # parse arithmetic
            
            elif type_lxm == "Comparison Operator":
                root.value = "Comparison Operation"
                arity = parse_comparison_operation(lexemes, root)     # parse comparison
            
            elif type_lxm == "Boolean Operator":
                root.value = "Boolean Operation"
                arity = parse_boolean_operations(lexemes, root)       # parse boolean
            
            else:
                raise Exception(f"LINE {line_no + 1}: Invalid nestable operation")
                
        # parsing nonnestable operations
        elif type_lxm in non_nestable or lexeme in ["ANY OF", "ALL OF"]:
            if is_binary == None and is_unary == None and is_inf == None: # set flag
                is_inf = True
            
            arity += 1
            
            # concatenation
            if lexeme == "SMOOSH":   
                root.value = "String Concatenation"
                lexemes.insert(0, (lexeme, type_lxm, line_no))        # push back the keyword
                arity = parse_concat(lexemes, root)
            
            # boolean - non-nestable
            elif lexeme in ["ANY OF", "ALL OF"]:                      
                root.value = "Boolean Operation"
                lexemes.insert(0, (lexeme, type_lxm, line_no))        # push back the keyword
                arity = parse_boolean_operations(lexemes, root)
            
            else:
                raise Exception(f"LINE {line_no + 1}: Invalid non-nestable operation")
        
        else:
            raise Exception(f"LINE {line_no + 1}: Invalid operation")
        
        # store old values
        prev_lexeme = lexeme
        prev_line_no = line_no
        
# -----------------------------------------------------------------------------------------
#  FUNCTION: Checks the correctness of the syntax of arithmetic operations
#
#  THINGS TO CONSIDER: Use softbreaks (,) as delimiter
# -----------------------------------------------------------------------------------------
def parse_arithmetic_operation(lexemes, root):
    literals = ["NUMBR", "NUMBAR", "YARN", "TROOF", "NOOB"]
    nestable = ["Arithmetic Operator", "Comparison Operator", "Boolean Operator", "Type Casting", "Type Conversion"]
    valid_args = ["VARIABLE|FUNCTION|LOOP", "Function Call"] + literals + nestable
    
    lexeme = None
    prev_lexeme = None
    prev_type = None
    prev_line_no = lexemes[0][2]
    arity = 0 # keeps track of the arity (MAX. 2)
    
    while lexemes:
        lexeme, type_lxm, line_no = lexemes.pop(0)  # get new lexeme
        
        # break case - arithmetic operations have a max of 2 arity
        if arity == 2:  
            lexemes.insert(0, (lexeme, type_lxm, line_no))
            return arity
        
        # start of arithmetic operation
        if prev_lexeme == None and prev_type == None:
            operation_node = Node("Operator", lexeme)  # holds the operator
            root.add_child(operation_node)             # append to arithmetic_node
            operand_node = Node("Operand")             # holds the operand/s
            root.add_child(operand_node)               # append to arithmetic_node
           
        # operand is a variable 
        elif (prev_type == "Arithmetic Operator" or prev_lexeme == "AN") and type_lxm == "VARIABLE|FUNCTION|LOOP":
            arity += 1
            arg_node = Node("Variable", lexeme)    # new node for the argument
            operand_node.add_child(arg_node)       # append to arithmetic_node
        
        # operand is a literal
        elif (prev_type == "Arithmetic Operator" or prev_lexeme == "AN") and type_lxm in literals:
            arity += 1
            
            if type_lxm == "NOOB":
                arg_node = Node(type_lxm, lexeme)      # new node
            
            elif type_lxm == "TROOF":
                if lexeme == "WIN":
                    arg_node = Node("NUMBR", "1")      # new node
                else:
                    arg_node = Node("NUMBR", "0")      # new node
                    
            elif lexeme == "" or lexeme == "0":    
                arg_node = Node("NUMBR", "0")      # new node 
            
            elif type_lxm == "YARN":
                lexeme = lexeme[1:len(lexeme)-1]
                
                if re.match(r"^-?[0-9]+(\.[0-9]+)?$", lexeme):  # check if yarn can be casted to NUMBR or NUMBAR
                    # create a node for valid YARN
                    if "." in lexeme: arg_node("NUMBAR", lexeme)
                    else: arg_node = Node("NUMBR", lexeme)  
                
                else: raise Exception(f"Invalid YARN for casting: {lexeme}")
            
            elif type_lxm == "NUMBR" or type_lxm == "NUMBAR":
                arg_node = Node(type_lxm, lexeme)      # NUMBR or NUMBAR
            
            else: 
                arg_node = Node("NUMBR", "1")      # other castable types are casted to 1
                
            operand_node.add_child(arg_node) # append the new node
            
        # operand is a nestable operation
        elif (prev_type == "Arithmetic Operator" or prev_lexeme == "AN") and type_lxm in nestable:
            arity += 1
            lexemes.insert(0, (lexeme, type_lxm, line_no))  # push the lexeme back
            nested_operation_node = Node("Operation")       # create node for nested operation
            operand_node.add_child(nested_operation_node)   # append nested operation to the operands
            parse_operation(lexemes, nested_operation_node) # parse the operation
        
        # operand is a function call
        elif (prev_type == "Arithmetic Operator" or prev_lexeme == "AN") and type_lxm == "Function Call":
            arity += 1
            lexemes.insert(0, (lexeme, type_lxm, line_no))  # push the lexeme back
            fxn_call_node = Node("Function Call")       # create node for nested operation
            operand_node.add_child(fxn_call_node)   # append nested operation to the operands
            parse_function_call(lexemes, fxn_call_node) # parse the operation
        
        # separator
        elif prev_type in valid_args and lexeme == "AN" :
            pass
        
        else:
            raise Exception(f"LINE {line_no + 1}: Invalid argument for arithmetic operation")
            
        prev_lexeme = lexeme
        prev_type = type_lxm
        prev_line_no = line_no

# -----------------------------------------------------------------------------------------
#  FUNCTION: Checks the correctness of the syntax of comparison operations
# -----------------------------------------------------------------------------------------
def parse_comparison_operation(lexemes, root):
    literals = ["NUMBR", "NUMBAR", "YARN", "TROOF", "NOOB"]
    nestable = ["Arithmetic Operator", "Comparison Operator", "Boolean Operator", "Type Casting", "Type Conversion"]
    valid_args = ["VARIABLE|FUNCTION|LOOP", "Function Call"] + literals + nestable
    
    prev_lexeme = None
    prev_type = None
    prev_line_no = lexemes[0][2]
    arity = 0                       # flag to keep track of the arity (MAX. 2)
    
    while lexemes:
        lexeme, type_lxm, line_no = lexemes.pop(0)  # get new lexeme
        
        if arity == 2: # comparison operations have arity of 2
            lexemes.insert(0, (lexeme, type_lxm, line_no))  # push back the popped declaration
            return arity           
    
        # start of comparison operation
        if prev_lexeme == None and prev_type == None:   
            operation_node = Node("Operator", lexeme)   # node for operation 
            root.add_child(operation_node)              # append to comparison_node
            operand_node = Node("Operand")              # node for operand/s
            root.add_child(operand_node)                # append to comparison_node
        
        # operand is a variable   
        elif (prev_type == "Comparison Operator" or prev_lexeme == "AN") and type_lxm == "VARIABLE|FUNCTION|LOOP": 
            arity += 1
            arg_node = Node("Variable", lexeme)    # new node for the argument
            operand_node.add_child(arg_node)       # append to comparison_node
        
        # operand is a literal (no implicit typecasting)
        elif (prev_type == "Comparison Operator" or prev_lexeme == "AN") and type_lxm in literals:
            arity += 1
            arg_node = Node(type_lxm, lexeme)    # new node
            operand_node.add_child(arg_node)     # append the new node
        
        # operand is a nestable operation
        elif (prev_type == "Comparison Operator" or prev_lexeme == "AN") and type_lxm in nestable:
            arity += 1
            lexemes.insert(0, (lexeme, type_lxm, line_no))  # push the lexeme back
            nested_operation_node = Node("Operation")       # create node for operation
            operand_node.add_child(nested_operation_node)   # append the new node
            parse_operation(lexemes, nested_operation_node) # parse the operation
        
        # operand is a function call
        elif (prev_type == "Comparison Operator" or prev_lexeme == "AN") and type_lxm == "Function Call":
            arity += 1
            lexemes.insert(0, (lexeme, type_lxm, line_no))  # push the lexeme back
            fxn_call_node = Node("Function Call")       # create node for nested operation
            operand_node.add_child(fxn_call_node)   # append nested operation to the operands
            parse_function_call(lexemes, fxn_call_node) # parse the operation
        
        # separator
        elif prev_type in valid_args and lexeme == "AN" :
            pass
        
        else:
            raise Exception(f"LINE {line_no + 1}: Invalid argument for comparison operation")
        
        prev_lexeme = lexeme
        prev_type = type_lxm
        prev_line_no = line_no

# -----------------------------------------------------------------------------------------
#  FUNCTION: Checks the correctness of the syntax of boolean operations
# -----------------------------------------------------------------------------------------
def parse_boolean_operations(lexemes, root):
    literals = ["NUMBR", "NUMBAR", "YARN", "TROOF", "NOOB"]
    nestable = ["Arithmetic Operator", "Comparison Operator", "Boolean Operator", "Type Casting", "Type Conversion"]
    valid_args = ["VARIABLE|FUNCTION|LOOP", "Function Call"] + literals + nestable
    
    prev_lexeme = None
    prev_type = None
    prev_line_no = lexemes[0][2]
    
    arity = 0                     
    operation_node = None                
    
    # flags
    is_binary = None
    is_unary = None
    is_inf = None
    mkay_found = False
    
    while lexemes: 
        lexeme, type_lxm, line_no = lexemes.pop(0)  # get lexeme to process
        
        # break case - max arity is reached
        if (is_binary and arity == 2) or (is_unary and arity == 1) or prev_line_no != line_no:
            lexemes.insert(0, (lexeme, type_lxm, line_no))  # push back the popped lexeme
            return arity  
        
        # MKAY keyword found for SMOOSH
        if is_inf and mkay_found:
            # lexemes.insert(0, (lexeme, type_lxm, line_no)) # push back the popped lexeme
            
            if not mkay_found: 
                lexemes.insert(0, ("SMOOSHED", type_lxm, line_no))  # push "SMOOSHED" to signal end of SMOOSH without MKAY
            
            return arity
            
        if lexeme in ["ANY OF", "ALL OF"]:  
            # check if nested
            if operation_node != None: # node was initialized by a different boolean operator that can be nested
                raise Exception(f"LINE {line_no + 1}: {lexeme} cannot be nested.")
            
            else: # it is the main operator
                operation_node = Node("Operator", lexeme) # create operation node
                root.add_child(operation_node)            # append node
                operand_node = Node("Operand")            # create operand node
                root.add_child(operand_node)              # append node
                
                is_inf = True # update flag
        
        else:       
            # start of boolean operation
            if prev_lexeme == None and prev_type == None and operation_node == None:
                operation_node = Node("Operator", lexeme) # create operation node
                root.add_child(operation_node)            # append node
                operand_node = Node("Operand")            # create operand node
                root.add_child(operand_node)              # append node
                
                # set flags for proper operation
                if lexeme == "NOT": is_unary = True
                else: is_binary = True
            
            # operand is a variable   
            elif (prev_type == "Boolean Operator" or prev_lexeme == "AN") and type_lxm == "VARIABLE|FUNCTION|LOOP":
                arity += 1
                arg_node = Node("Variable", lexeme)    # new node for the argument
                operand_node.add_child(arg_node)       # append to bool_node

            # operand is a literal
            elif (prev_type == "Boolean Operator" or prev_lexeme == "AN") and type_lxm in literals:  
                arity += 1
                
                if type_lxm == "NOOB":
                    arg_node = Node(type_lxm, lexeme)      # new node
                
                elif type_lxm == "TROOF":
                    if lexeme == "WIN":
                        arg_node = Node("NUMBR", "1")      # new node
                    else:
                        arg_node = Node("NUMBR", "0")      # new node
                        
                elif lexeme == "" or lexeme == "0":    
                    arg_node = Node("NUMBR", "0")      # new node 
                
                elif type_lxm == "YARN":
                    lexeme = lexeme[1:len(lexeme)-1]
                    
                    if re.match(r"^-?[0-9]+(\.[0-9]+)?$", lexeme):  # check if yarn can be casted to NUMBR or NUMBAR
                        # create a node for valid YARN
                        if "." in lexeme: arg_node("NUMBAR", lexeme)
                        else: arg_node = Node("NUMBR", lexeme)  
                    
                    else: raise Exception(f"Invalid YARN for casting: {lexeme}")
                
                elif type_lxm == "NUMBR" or type_lxm == "NUMBAR":
                    arg_node = Node(type_lxm, lexeme)      # NUMBR or NUMBAR
                
                else: 
                    arg_node = Node("NUMBR", "1")      # other castable types are casted to 1
                    
                operand_node.add_child(arg_node)   # append the new node
            
            # operand is a nestable operation
            elif (prev_type == "Boolean Operator" or prev_lexeme == "AN") and type_lxm in nestable:
                arity += 1
                lexemes.insert(0, (lexeme, type_lxm, line_no))  # push the lexeme back
                nested_operation_node = Node("Operation")       # create node for operation
                operand_node.add_child(nested_operation_node)   # append the new node
                parse_operation(lexemes, nested_operation_node) # parse the operation
            
            # operand is a function call
            elif (prev_type == "Boolean Operator" or prev_lexeme == "AN") and type_lxm == "Function Call":
                arity += 1
                lexemes.insert(0, (lexeme, type_lxm, line_no))  # push the lexeme back
                fxn_call_node = Node("Function Call")       # create node for nested operation
                operand_node.add_child(fxn_call_node)   # append nested operation to the operands
                parse_function_call(lexemes, fxn_call_node) # parse the operation
        
            # argument separator
            elif prev_type in valid_args and lexeme == "AN" :
                pass
            
            # statement separator
            elif prev_type in valid_args and lexeme == "MKAY" :
                mkay_found = True   # update flag
                lexemes.insert(0, (lexeme, type_lxm, line_no))  # push the lexeme back
                
            else:
                print(f"lexeme: {lexeme} - {type_lxm}\n")
                raise Exception(f"LINE {line_no + 1}: Invalid argument for Boolean operation")
        
        prev_lexeme = lexeme
        prev_type = type_lxm
        prev_line_no = line_no

# -----------------------------------------------------------------------------------------
#  FUNCTION: Checks the correctness of the syntax for type casting
#   
#  FIX
# -----------------------------------------------------------------------------------------
def parse_typecast(lexemes, root):
    literals = ["NUMBR", "NUMBAR", "YARN", "TROOF", "NOOB"]
    
    prev_lexeme = None
    prev_type = None
    prev_line_no = None
    
    while lexemes:
        lexeme, type_lxm, line_no = lexemes.pop(0)  # get new lexeme
        
        # start of typecasting
        if prev_lexeme == None and prev_type == None:
            # typecasting with assignment
            if type_lxm == "VARIABLE|FUNCTION|LOOP":
                start_node = Node("Destination Variable", lexeme)   
                root.add_child(start_node)
        
        # casting with "IS NOW A" or "R"
        elif prev_type == "VARIABLE|FUNCTION|LOOP" and (lexeme == "IS NOW A" or type_lxm == "Assignment Operator"):
            pass
        
        # casting with "R MAEK"
        elif prev_type == "Assignment Operator" and lexeme == "MAEK":
            pass
        
        # variable to be casted using the "MAEK" / "R MAEK"
        elif prev_lexeme == "MAEK" and type_lxm == "VARIABLE|FUNCTION|LOOP":
            variable_node = Node("Variable", lexeme)
            root.add_child(variable_node)
        
        # type to cast using "IS NOW A"
        elif prev_lexeme == "IS NOW A" and lexeme in literals:
            type_node = Node("Type", lexeme)
            root.add_child(type_node)
            break # end of casting
        
        # "A" keyword or not for "MAEK"
        elif prev_type == "VARIABLE|FUNCTION|LOOP" and (type_lxm == "Type Cast Separator" or lexeme in literals):
            # "A" is not present
            if lexeme in literals:
                type_node = Node(type_lxm, lexeme)
                root.add_child(type_node)
                break # end of casting
            
            # "A" keyword is present
            else:
                # get new lexeme, it must be a literal
                lexeme, type_lxm, line_no = lexemes.pop(0) 
                if lexeme in literals:
                    type_node = Node(type_lxm, lexeme)
                    root.add_child(type_node)
                    break # end of casting
            
                else:
                    raise Exception(f"LINE {line_no + 1}: Invalid type for type casting")
                
        else:
            raise Exception(f"LINE {line_no + 1}: Invalid syntax for type casting")
            
        # store old values
        prev_lexeme = lexeme
        prev_type = type_lxm
        prev_line_no = line_no
        
# -----------------------------------------------------------------------------------------
#  FUNCTION: Checks the correctness of the syntax of SMOOSH operation
# -----------------------------------------------------------------------------------------
def parse_concat(lexemes, root):
    # non_nestable = ["String Concatenation", "Boolean Operator"]
    literals = ["NUMBR", "NUMBAR", "YARN", "TROOF", "NOOB"]
    nestable = ["Arithmetic Operator", "Comparison Operator", "Boolean Operator", "Type Casting", "Type Conversion"]
    valid_args = ["VARIABLE|FUNCTION|LOOP", "Function Call"] + nestable + literals
    
    arity = 0
    
    prev_lexeme = None
    prev_type = None
    prev_line_no = lexemes[0][2]
    
    # flag for MKAY keyword
    mkay_found = False
    
    while lexemes:
        lexeme, type_lxm, line_no = lexemes.pop(0)  # get new lexeme
        
        # MKAY break
        if mkay_found: 
            lexemes.insert(0, (lexeme, type_lxm, line_no))      # push back the popped declaration
            return arity
        
        # new line break
        if line_no != prev_line_no:
            lexemes.insert(0, (lexeme, type_lxm, line_no))      # push back the popped declaration
            return arity
        
        # start of concatenation
        if prev_lexeme == None and prev_type == None:
            operator_node = Node("Operator", lexeme)  # create node for operator
            root.add_child(operator_node)             # append
            operand_node = Node("Operand")           # create node for operands
            root.add_child(operand_node)             # append 
        
        # operand is variable
        elif (prev_lexeme == "SMOOSH" or prev_lexeme == "AN") and type_lxm == "VARIABLE|FUNCTION|LOOP":
            arity += 1
            arg_node = Node("Variable", lexeme) # create node
            operand_node.add_child(arg_node)            # append to subtree
        
        # operand is a literal
        elif (prev_lexeme == "SMOOSH" or prev_lexeme == "AN") and type_lxm in literals:
            arity += 1
            arg_node = Node("YARN", lexeme)     # create node
            operand_node.add_child(arg_node)            # append to subtree
        
        # operand is a nestable operation
        elif (prev_lexeme == "SMOOSH" or prev_lexeme == "AN") and type_lxm in nestable and lexeme not in ["ALL OF", "ANY OF"]:
            arity += 1
            lexemes.insert(0, (lexeme, type_lxm, line_no))  # push the lexeme back
            nested_operation_node = Node("Operation")       # create node for operation
            operand_node.add_child(nested_operation_node)  # append the new node
            parse_operation(lexemes, nested_operation_node) # parse the operation
        
        # operand is a function call
        elif (prev_lexeme == "SMOOSH" or prev_lexeme == "AN") and type_lxm == "Function Call":
            arity += 1
            lexemes.insert(0, (lexeme, type_lxm, line_no))  # push the lexeme back
            fxn_call_node = Node("Function Call")       # create node for nested operation
            operand_node.add_child(fxn_call_node)   # append nested operation to the operands
            parse_function_call(lexemes, fxn_call_node) # parse the operation
        
        # argument separator
        elif prev_type in valid_args and lexeme == "AN":
            pass                     # append to tree
        
        # statement separator
        elif prev_type in valid_args and lexeme == "MKAY":
            mkay_found = True                               # update flag
            lexemes.insert(0, (lexeme, type_lxm, line_no))  # push back MKAY
        
        else: 
            raise Exception(f"LINE {line_no + 1}: Invalid argument for SMOOSH operation")

        prev_line_no = line_no
        prev_lexeme = lexeme
        prev_type = type_lxm

# -----------------------------------------------------------------------------------------
#  FUNCTION: Checks the correctness of print statements
# -----------------------------------------------------------------------------------------
def parse_output(lexemes, root):
    literals = ["NUMBR", "NUMBAR", "YARN", "TROOF", "NOOB"]
    operators = ["String Concatenation", "Arithmetic Operator", "Comparison Operator", "Boolean Operator", "Type Casting", "Type Conversion"]
    valid_args = ["VARIABLE|FUNCTION|LOOP", "VISIBLE Operand Separator", "MKAY", "Function Call"] + literals + operators
    
    prev_lexeme = None
    prev_type = None
    prev_line_no = lexemes[0][2]
    
    while lexemes:
        lexeme, type_lxm, line_no = lexemes.pop(0)  # get lexeme
        
        # break case
        if (prev_lexeme != None and type_lxm not in valid_args) or (prev_line_no != line_no):
            newline_node = Node("Newline", "\\n")           # adds new line for outputs
            operand_node.add_child(newline_node)
            lexemes.insert(0, (lexeme, type_lxm, line_no))  # push back the popped declaration
            break
        
        # start of print statement
        if prev_lexeme == None and prev_type == None:
            operation_node = Node("Operation", lexeme)  # node for Visible
            root.add_child(operation_node)              # append the node
            operand_node = Node("Operand")              # node for the operands
            root.add_child(operand_node)                # append the node
        
        # operand is a literal
        elif (prev_type == "Output" or prev_lexeme.strip() == "+") and type_lxm in literals:  
            # literal_node = Node("YARN", lexeme)           # create node, args are implicitly casted to YARN
            literal_node = Node("YARN", lexeme)             # create node, args are implicitly casted to YARN
            operand_node.add_child(literal_node)            # append
        
        # operand is a variable
        elif (prev_type == "Output" or prev_lexeme.strip() == "+") and type_lxm == "VARIABLE|FUNCTION|LOOP":
            variable_node = Node("Variable", lexeme)        # create node, args are implicitly casted to YARN
            operand_node.add_child(variable_node)                   # append node to var_dec_node
        
        # operand is an operator
        elif (prev_type == "Output" or prev_lexeme.strip() == "+") and type_lxm in operators:
            lexemes.insert(0, (lexeme, type_lxm, line_no))  # push the lexeme back
            operation_node = Node("Operation")              
            operand_node.add_child(operation_node)          # append node 
            parse_operation(lexemes, operation_node)        # parse operation
        
        # operand is a function call
        elif (prev_type == "Outpu" or prev_lexeme.strip() == "+") and type_lxm == "Function Call":
            lexemes.insert(0, (lexeme, type_lxm, line_no))  # push the lexeme back
            fxn_call_node = Node("Function Call")           # create node for nested operation
            operand_node.add_child(fxn_call_node)           # append nested operation to the operands
            parse_function_call(lexemes, fxn_call_node)     # parse the operation
    
        # separator
        elif prev_type in valid_args and lexeme.strip() == "+" :
            pass
        
        else:
            raise Exception(f"LINE {line_no + 1}: Invalid argument for VISIBLE statement.")
        
        prev_lexeme = lexeme
        prev_type = type_lxm
        prev_line_no = line_no
     
# -----------------------------------------------------------------------------------------
#  FUNCTION: Checks the correctness of input statements
# -----------------------------------------------------------------------------------------
def parse_input(lexemes, root):
    prev_lexeme = None
    prev_type = None

    while lexemes:
        lexeme, type_lxm, line_no = lexemes.pop(0)
        
        if prev_lexeme == None and prev_type == None:
            pass
        
        elif prev_type == "Input" and type_lxm == "VARIABLE|FUNCTION|LOOP":
            variable_node = Node("Variable", lexeme)
            root.add_child(variable_node)
            break   # we only need one variable for the input
        
        else:
            raise Exception(f"LINE {line_no + 1}: Invalid argument for input. It must be a variable")
        
        prev_lexeme = lexeme
        prev_type = type_lxm
    
# -----------------------------------------------------------------------------------------
#  FUNCTION: Checks the correctness of assignment statements
#
#  TO DO: Add new type node
# -----------------------------------------------------------------------------------------
def parse_assignment(lexemes, root):
    literals = ["NUMBR", "NUMBAR", "YARN", "TROOF", "NOOB"]
    operators = ["Arithmetic Operator", "Comparison Operator", "Boolean Operator", "String Concatenation", "Type Casting", "Type Conversion"]
    valid_rhs = ["VARIABLE|FUNCTION|LOOP", "Function Call"] + operators + literals
    
    prev_lexeme = None
    prev_type = None

    while lexemes:
        lexeme, type_lxm, line_no = lexemes.pop(0)
        
        # start of assignment
        if prev_lexeme == None and prev_type == None and type_lxm == "VARIABLE|FUNCTION|LOOP":
            variable_node = Node("Variable", lexeme)
            root.add_child(variable_node)
            new_value_node = Node("New Value")
            root.add_child(new_value_node)
        
        # assignment operator
        elif prev_type == "VARIABLE|FUNCTION|LOOP" and type_lxm == "Assignment Operator":
            pass
        
        # assigning a value
        elif prev_type == "Assignment Operator" and type_lxm in valid_rhs:
            # assigning result from operation
            if type_lxm in operators:
                operation_node = Node("Operation")
                new_value_node.add_child(operation_node)
                lexemes.insert(0, (lexeme, type_lxm, line_no))      # push back the operation
                parse_operation(lexemes, operation_node)
            
            # assigning value from a variable
            elif type_lxm == "VARIABLE|FUNCTION|LOOP":
                value_node = Node("Variable", lexeme)
                new_value_node.add_child(value_node)
            
            # operand is a function call
            elif type_lxm == "Function Call":
                lexemes.insert(0, (lexeme, type_lxm, line_no))  # push the lexeme back
                fxn_call_node = Node("Function Call")           # create node for nested operation
                new_value_node.add_child(fxn_call_node)         # append nested operation to the operands
                parse_function_call(lexemes, fxn_call_node)     # parse the operation
        
            # assigning a literal
            else:
                value_node = Node(type_lxm, lexeme)
                new_value_node.add_child(value_node)
            break
        
        else:
            raise Exception(f"LINE {line_no + 1}: Invalid syntax for assignment statement")

        prev_lexeme = lexeme
        prev_type = type_lxm

# -----------------------------------------------------------------------------------------
#  FUNCTION: Checks the correctness of if-else statements
# -----------------------------------------------------------------------------------------
def parse_if_then(lexemes, root):
    delimiters = ["If Statement Else-If Case", "If Statement False Case", "If Statement End"]
    
    prev_lexeme = None
    prev_type = None
    pre_line_no = None
    
    # flags
    ya_rly_found = False
    nested_loop = -1
    
    if_then_lexemes = []
    
    # get all lexemes for the if-then statement
    while lexemes:
        lexeme, type_lxm, line_no = lexemes.pop(0)
        if_then_lexemes.append((lexeme, type_lxm, line_no))
        
        # check for nested if-then / switch-case statement
        if type_lxm == "If Statement Start" or type_lxm == "Switch Statement Start":
            nested_loop += 1
            
        if lexeme == "OIC": 
            if nested_loop == 0:
                break   # break if OIC for current loop is found
            else:
                nested_loop -= 1
                
    # check if OIC does not exist
    if len(lexemes) < 1: raise Exception(f"LINE {line_no + 1}: If-then statement lacks 'OIC'")
    
    # iterate over the code block for if-then statement
    while if_then_lexemes:
        lexeme, type_lxm, line_no = if_then_lexemes.pop(0) # get lexeme
        
        # start
        if prev_lexeme == None and prev_type == None:
            pass
        
        # YA RLY
        elif prev_type == "If Statement Start" and type_lxm == "If Statement True Case":
            ya_rly_found = True # update flag
            ya_rly_node = Node(lexeme)    # create node for the if statement
            root.add_child(ya_rly_node)     # append
            if_then_lexemes.insert(0, (lexeme, type_lxm, line_no)) # push the delimiter back
            parse_if_then_helper(if_then_lexemes, ya_rly_node) # parse the body
             
        # MEBBE
        elif ya_rly_found == True and type_lxm == "If Statement Else-If Case":
            mebbe_node = Node(lexeme)
            root.add_child(mebbe_node)     # append
            if_then_lexemes.insert(0, (lexeme, type_lxm, line_no)) # push the delimiter back
            parse_if_then_helper(if_then_lexemes, mebbe_node) # parse the body
        
        # NO WAI
        elif ya_rly_found == True and type_lxm == "If Statement False Case":
            nowai_node = Node(lexeme)
            root.add_child(nowai_node)     # append
            if_then_lexemes.insert(0, (lexeme, type_lxm, line_no)) # push the delimiter back
            parse_if_then_helper(if_then_lexemes, nowai_node) # parse the body
        
        # OIC
        elif type_lxm == "If Statement End":
            end_node = Node(type_lxm, lexeme)
            root.add_child(end_node)
            
        else:
            raise Exception(f"LINE {line_no + 1}: Invalid expression for if-then statement")
        
        prev_lexeme = lexeme
        prev_type = type_lxm
        prev_line_no = line_no        

# -----------------------------------------------------------------------------------------
#  FUNCTION: Checks the correctness of if, else if, and else clause
# -----------------------------------------------------------------------------------------
def parse_if_then_helper(lexemes, root):
    delimiters = ["If Statement Else-If Case", "If Statement False Case", "If Statement End"]
    operators = ["Arithmetic Operator", "Comparison Operator", "Boolean Operator", "String Concatenation", "Type Casting", "Type Conversion"]
    
    prev_lexeme = None
    prev_type = None
    
    # flags
    else_if_block = False
    
    while lexemes:
        lexeme, type_lxm, line_no = lexemes.pop(0) # get lexeme
        
        if prev_lexeme != None and prev_type != None and type_lxm in delimiters:
            lexemes.insert(0, (lexeme, type_lxm, line_no))
            break  
    
        # start of if-then block
        if prev_lexeme == None and prev_type == None:   
            # check if there is a condition after the keyword
            if type_lxm == "If Statement Else-If Case":
                else_if_block = True
                condition_node = Node("Condition")
                root.add_child(condition_node)
        
        # parse the condition for the else if block
        elif else_if_block:
            # parse the expression
            if type_lxm in operators:
                lexemes.insert(0, (lexeme, type_lxm, line_no))
                operator_node = Node("Operation")
                condition_node.add_child(operator_node)         
                parse_operation(lexemes, operator_node)
                else_if_block = False   # update flag
            
            # condition is a function call
            elif type_lxm == "Function Call":
                lexemes.insert(0, (lexeme, type_lxm, line_no))  # push the lexeme back
                fxn_call_node = Node("Function Call")           # create node
                condition_node.add_child(fxn_call_node)         # appen
                parse_function_call(lexemes, fxn_call_node)     # parse the function call
                else_if_block = False   # update flag
            
            else:
                raise Exception(f"LINE {line_no + 1}: Invalid condition for MEBBE")
        
        # parse body
        else:
            parse_body(lexemes, root, lexeme, type_lxm, line_no)

        prev_lexeme = lexeme
        prev_type = type_lxm
        
# -----------------------------------------------------------------------------------------
#  FUNCTION: Checks the correctness of switch-case statements
# -----------------------------------------------------------------------------------------
def parse_switch_case(lexemes, root):
    prev_lexeme = None
    prev_type = None
    
    switch_case_lexemes = []
    
    # flag
    omgwtf_found = False
    nest_switch = -1
    
    # get all lexemes for the switch-case statement
    while lexemes:
        lexeme, type_lxm, line_no = lexemes.pop(0)
        switch_case_lexemes.append((lexeme, type_lxm, line_no))
        # check for nested switch-case / if-then statement
        if type_lxm == "Switch Statement Start" or type_lxm == "If Statement Start":
            nest_switch += 1
            
        if lexeme == "OIC": 
            if nest_switch == 0:
                break   # break if OIC for current switch-case is found
            else:
                nest_switch -= 1
        
    # check if OIC does not exist
    if len(lexemes) < 1: raise Exception(f"LINE {line_no + 1}: Switch-case statement lacks 'OIC'")
    
    while switch_case_lexemes:
        lexeme, type_lxm, line_no = switch_case_lexemes.pop(0)
    
        # start
        if prev_lexeme == None and prev_type == None:
            pass
        
        # OMG
        elif not omgwtf_found and type_lxm == "Case Statement":
            omg_node = Node(lexeme)     # omg node
            root.add_child(omg_node)    # append
            switch_case_lexemes.insert(0, (lexeme, type_lxm, line_no))  # push the delimiter back
            parse_switch_case_helper(switch_case_lexemes, omg_node)     # parse the body
        
        # OMGWTF
        elif type_lxm == "Default Case Statement":
            omgwtf_found = True             # update flag
            omgwtf_node = Node(lexeme)      # node for OMGWTF
            root.add_child(omgwtf_node)     # append
            switch_case_lexemes.insert(0, (lexeme, type_lxm, line_no)) # push the delimiter back
            parse_switch_case_helper(switch_case_lexemes, omgwtf_node) # parse the body
        
        # OIC
        elif type_lxm == "If Statement End":
            end_node = Node("Swtich-Case End", lexeme)
            root.add_child(end_node)
        
        else:
            raise Exception(f"LINE {line_no + 1}: Invalid expression for switch-case statement")
        
        prev_lexeme = lexeme
        prev_type = type_lxm

# -----------------------------------------------------------------------------------------
#  FUNCTION: Checks the correctness of omg and omgwtf clause
# -----------------------------------------------------------------------------------------
def parse_switch_case_helper(lexemes, root):
    delimiters = ["Case Statement", "Default Case Statement", "If Statement End", "Function/Loop Exit"]
    literals = ["NUMBR", "NUMBAR", "YARN", "TROOF", "NOOB"]
    operators = ["Arithmetic Operator", "Comparison Operator", "Boolean Operator", "String Concatenation", "Type Casting", "Type Conversion"]
    
    prev_lexeme = None
    prev_type = None
    
    # flags
    omgwtf_found = False
    omg_condition = False
    
    while lexemes:
        lexeme, type_lxm, line_no = lexemes.pop(0)
        
        # break case
        if prev_lexeme != None and prev_type != None and type_lxm in delimiters:
            if type_lxm == "Function/Loop Exit": # GTFO is appended, but not pushed back
                exit_node = Node(type_lxm, lexeme)
                root.add_child(exit_node)
            else: lexemes.insert(0, (lexeme, type_lxm, line_no))
            break
        
        # start of switch-case block
        if prev_lexeme == None and prev_type == None:   
            # check if OMGWTF is found already
            if type_lxm == "Default Case Statement":
                omgwtf_found = True
            else: # OMG <condition>
                condition_node = Node("Condition")
                root.add_child(condition_node)
                omg_condition = True            # update flag
        
        # OMG's condition clause
        elif not omgwtf_found and omg_condition and type_lxm in literals:
            condition_literal_node = Node(type_lxm, lexeme)
            condition_node.add_child(condition_literal_node)
            omg_condition = False   # update flag
        
        # condition is a function call
        elif not omgwtf_found and omg_condition and type_lxm == "Function Call":
            lexemes.insert(0, (lexeme, type_lxm, line_no))  # push the lexeme back
            fxn_call_node = Node("Function Call")           # create node
            condition_node.add_child(fxn_call_node)         # appen
            parse_function_call(lexemes, fxn_call_node)     # parse the function call
            omg_condition = False   # update flag
        
        
        # parse body
        else:
            parse_body(lexemes, root, lexeme, type_lxm, line_no)

        prev_lexeme = lexeme
        prev_type = type_lxm     
        
# -----------------------------------------------------------------------------------------
#  FUNCTION: Checks the correctness of loop statements
# -----------------------------------------------------------------------------------------
def parse_loop(lexemes, root):
    operations = ["Loop Increment", "Loop Decrement"]
    conditions = ["Loop Until Condition", "Loop While Condition"]
    operators = ["Arithmetic Operator", "Comparison Operator", "Boolean Operator", "String Concatenation", "Type Casting", "Type Conversion"]
    
    prev_lexeme = None
    prev_type = None
    
    loop_lexemes = []
    label = None
    
    # flag
    label_found = False
    in_loop_body = False
    
    # get all lexemes for the switch-case statement
    while lexemes:
        lexeme, type_lxm, line_no = lexemes.pop(0)
        loop_lexemes.append((lexeme, type_lxm, line_no))
        
        # check for the label at start
        if type_lxm == "Loop Start": 
            lxm, typ, ln = lexemes.pop(0) # get label
            if line_no == ln and typ == "VARIABLE|FUNCTION|LOOP":
                if label == None:
                    loop_lexemes.append((lxm, typ, ln))
                    label = lxm
                else:
                    lexemes.insert(0, (lxm, typ, ln)) # not the label for current loop
            else:
                raise Exception(f"LINE {line_no + 1}: Missing label at the end of loop")
            
        # check for the label at the end
        if type_lxm == "Loop End":
            lxm, typ, ln = lexemes.pop(0) # get label
            if line_no == ln and typ == "VARIABLE|FUNCTION|LOOP":
                if lxm == label:  # label matched, it's the delimiter for the loop
                    loop_lexemes.append((lxm, typ, ln))
                    break   # break if IM OUTTA YR is found
                else:
                    lexemes.insert(0, (lxm, typ, ln)) # not the delimeter for current loop
            else:
                raise Exception(f"LINE {line_no + 1}: Missing label at the end of loop")
    
    # check if OIC does not exist
    if len(lexemes) < 1: raise Exception(f"LINE {line_no + 1}: Loop should be delimited by \"IM OUTTA YR\"")
    
    while loop_lexemes:
        lexeme, type_lxm, line_no = loop_lexemes.pop(0)

        # start of loop
        if prev_lexeme == None and prev_type == None and type_lxm == "Loop Start":
            pass
        
        # loop label
        elif prev_type == "Loop Start" and type_lxm == "VARIABLE|FUNCTION|LOOP":
            root.value = lexeme
            label_found = True
        
        # operation, either UPPIN or NERFIN
        elif label_found and prev_type == "VARIABLE|FUNCTION|LOOP" and type_lxm in operations:
            operation_node = Node("Step", lexeme)
            root.add_child(operation_node)
        
        # YR
        elif label_found and prev_type in operations and type_lxm == "Function/Loop Separator":
            pass
        
        # variable to store the value from UPPIN or NERFIN
        elif label_found and prev_type == "Function/Loop Separator" and type_lxm == "VARIABLE|FUNCTION|LOOP":
            variable_node = Node("Variable", lexeme)
            root.add_child(variable_node)
        
        # condition to terminate the loop
        elif label_found and prev_type == "VARIABLE|FUNCTION|LOOP" and type_lxm in conditions:
            condition_node = Node("Condition", lexeme)
            root.add_child(condition_node)
        
        # operation in condition to terminate the loop
        elif label_found and prev_type in conditions and type_lxm in operators:
            operation_node = Node("Operation")
            condition_node.add_child(operation_node)
            loop_lexemes.insert(0, (lexeme, type_lxm, line_no))    # push the operator back
            parse_operation(loop_lexemes, operation_node)
            in_loop_body = True
        
        # function call in condition to terminate the loop
        elif label_found and prev_type in conditions and type_lxm == "Function Call":
            loop_lexemes.insert(0, (lexeme, type_lxm, line_no))  # push the lexeme back
            fxn_call_node = Node("Function Call")           # create node
            condition_node.add_child(fxn_call_node)         # appen
            parse_function_call(loop_lexemes, fxn_call_node)     # parse the function call
            in_loop_body = True   # update flag
        
        # loop body
        elif in_loop_body:
            loop_lexemes.insert(0, (lexeme, type_lxm, line_no))    # push the operator back
            parse_loop_helper(loop_lexemes, root)
            
            in_loop_body = False
        
        # end of loop
        elif not in_loop_body and type_lxm == "Loop End":
            lxm, typ, ln = loop_lexemes.pop(0) # get label
            
            # check if there is a label at the end of the loop
            if line_no == ln and typ == "VARIABLE|FUNCTION|LOOP" and label_found:
                # check if label name from start is the same with the one at the end
                if root.value == lxm:
                    loop_label_node = Node(type_lxm, lxm)
                    root.add_child(loop_label_node)
                    break   # end loop
                else:
                    raise Exception(f"LINE {ln}: Mismatched label used for loop statement")
            
            else:
                raise Exception(f"LINE {ln}: Missing label for loop statement")

        else:
            raise Exception(f"LINE {ln}: Invalid loop statement")
        
        prev_lexeme = lexeme
        prev_type = type_lxm

# -----------------------------------------------------------------------------------------
#  FUNCTION: Checks the correctness of the statements in the loop body
# -----------------------------------------------------------------------------------------        
def parse_loop_helper(lexemes, root):
    while lexemes:
        lexeme, type_lxm, line_no = lexemes.pop(0)
        
        # break case
        if type_lxm == "Loop End":
            lexemes.insert(0, (lexeme, type_lxm, line_no))
            break
        
        # parse body
        else:
            parse_body(lexemes, root, lexeme, type_lxm, line_no)

# -----------------------------------------------------------------------------------------
#  FUNCTION: Checks the correctness of the syntax of functions
# -----------------------------------------------------------------------------------------        
def parse_function(lexemes, root):
    literals = ["NUMBR", "NUMBAR", "YARN", "TROOF", "NOOB"]
    operators = ["String Concatenation", "Arithmetic Operator", "Comparison Operator", "Boolean Operator", "Type Casting", "Type Conversion"]
    
    prev_lexeme = None
    prev_type = None
    
    fxn_lexemes = []
    
    # flags
    found_yr_found = False
    gtfo_found = False
    global kthxbye_found
    
    # get all lexemes for the function
    while lexemes:
        lexeme, type_lxm, line_no = lexemes.pop(0)
        fxn_lexemes.append((lexeme, type_lxm, line_no))
        if type_lxm == "Function End": break
    
    # check if IF U SAY SO does not exist
    if len(lexemes) < 1 and not kthxbye_found: raise Exception(f"LINE {line_no + 1}: Function lacks 'IF U SAY SO'")
    
    while fxn_lexemes:
        lexeme, type_lxm, line_no = fxn_lexemes.pop(0) # get lexeme
        
        if type_lxm == "Function End":
            if not found_yr_found and (gtfo_found or not gtfo_found): 
                val_ret_node = Node("Literal", "NOOB")  # GTFO or no return will return a NOOB value
                return_node.add_child(val_ret_node)
            fxn_node.add_child(return_node)
            break
        
        # start of function
        if prev_lexeme == None and prev_type == None and type_lxm == "Function Start":
            return_node = Node("Return")
            
        # function name
        elif prev_type == "Function Start" and type_lxm == "VARIABLE|FUNCTION|LOOP":
            fxn_node = Node(lexeme)
            root.add_child(fxn_node)
            
        # check if there are parameters
        elif (prev_type == "Parameter Separator" or prev_lexeme == fxn_node.type)and type_lxm == "Function/Loop Separator":
            lxm, typ, ln = fxn_lexemes.pop(0) # get parameter
            
            # check if there is a parameter after the keyword "YR"
            if ln == line_no and typ == "VARIABLE|FUNCTION|LOOP":
                var_node = Node("Variable", lxm)
                try:
                    variables_node.add_child(var_node)
                    
                except: # first argument, create the node for variables
                    variables_node = Node("Variables")
                    fxn_node.add_child(variables_node)        
                    variables_node.add_child(var_node)
                
                prev_lexeme = lxm
                prev_type = typ
            
            else:
                raise Exception(f"LINE {line_no + 1}: Invalid formal parameter for function {fxn_node.value}")
        
        # AN
        elif (prev_type == "Function/Loop Separator") and type_lxm == "Parameter Separator":
            pass
          
        # FOUND YR  
        elif type_lxm == "Return Statement":
            found_yr_found = True
            lxm, typ, ln = fxn_lexemes.pop(0) # get return statement
            
            # return expression
            if typ in operators:
                parse_body(fxn_lexemes, return_node, lxm, typ, ln)
            
            # return literal value
            elif lxm in literals:
                ret_value = Node("Literal", lxm)
                return_node.add_child(ret_value)
                
            # return variable value
            elif typ == "VARIABLE|FUNCTION|LOOP":
                ret_value = Node("Variable", lxm)
                return_node.add_child(ret_value)
                
            else:
                raise Exception(f"LINE {line_no + 1}: Invalid return type")
        
        # GTFO 
        elif type_lxm == "Function/Loop Exit":
            gtfo_found = True
        
        else:
            parse_body(fxn_lexemes, fxn_node, lexeme, type_lxm, line_no)
            
        prev_lexeme = lexeme
        prev_type = type_lxm
 
# -----------------------------------------------------------------------------------------
#  FUNCTION: Checks the correctness of the syntax of function call 
#  
#  TO DO: add more delimiter
# -----------------------------------------------------------------------------------------        
def parse_function_call(lexemes, root):
    literals = ["NUMBR", "NUMBAR", "YARN", "TROOF", "NOOB"]
    operators = ["String Concatenation", "Arithmetic Operator", "Comparison Operator", "Boolean Operator", "Type Casting", "Type Conversion"]
    
    lxm = None
    typ = None
    prev_lexeme = None
    prev_type = None
    prev_line_no = None
    
    # flag
    has_params = False
    
    while lexemes:
        lexeme, type_lxm, line_no = lexemes.pop(0)
        
        # break case
        if prev_lexeme != None and prev_line_no != line_no or type_lxm == "Statement Separator":
            lexemes.insert(0, (lexeme, type_lxm, line_no))
            break
        
        # start of function call
        if prev_lexeme == None and prev_type == None:
            root.value = "Function Call"
            fxn_name_node = Node("Function Name")
            root.add_child(fxn_name_node)
            fxn_params_node = Node("Parameter")
            root.add_child(fxn_params_node)
        
        # function name
        elif prev_type == "Function Call" and type_lxm == "VARIABLE|FUNCTION|LOOP":
            fxn_name_node.value = lexeme    # append function name
        
        # actual parameters
        elif type_lxm == "Function/Loop Separator":
            lxm, typ, ln = lexemes.pop(0)
            
            # pass an expression
            if typ in operators:
                parse_body(lexemes, fxn_params_node, lxm, typ, ln)
            
            # pass a literal value
            elif typ in literals:
                actual_param = Node("Literal", lxm)
                fxn_params_node.add_child(actual_param)
                
            # pass a variable value
            elif typ == "VARIABLE|FUNCTION|LOOP":
                actual_param = Node("Variable", lxm)
                fxn_params_node.add_child(actual_param)
            
            # pass a function return value
            elif typ == "Function Call":
                parse_body(lexemes, fxn_params_node, lxm, typ, ln)
               
            else:
                raise Exception(f"LINE {line_no + 1}: Invalid return type")

            has_params = True # update flag
            
        # AN
        elif prev_type == "Function/Loop Separator" and type_lxm == "Parameter Separator":
            pass
        
        # function call is in between other arguments for other operation
        # check until where its actual parameters are, and where the arguments of the argument continue
        elif prev_type == "Parameter Separator" and type_lxm != "Function/Loop Separator":
            lexemes.insert(0, (lexeme, type_lxm, line_no))              # push lexeme
            lexemes.insert(0, (prev_lexeme, prev_type, prev_line_no))   # push back AN
            break
        
        # checks if parameters are for its parent operation
        elif prev_type == "VARIABLE|FUNCTION|LOOP" and type_lxm != "YR":
            lexemes.insert(0, (lexeme, type_lxm, line_no))
            break
        
        else:
            raise Exception(f"LINE {line_no + 1}: Invalid parameter/s passed to function call")
        
        prev_lexeme = lexeme
        prev_type = type_lxm
        prev_line_no = line_no