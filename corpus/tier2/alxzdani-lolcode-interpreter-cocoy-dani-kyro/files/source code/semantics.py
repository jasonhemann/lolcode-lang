import tkinter.simpledialog as sd
from typecaster import TypeCaster
import tkinter as tk

class SemanticAnalyzer:
    # constructor to initialize the semantic analyzer
    def __init__(self, tokens, log_function, console, gui_symbol_table):
        self.tokens = tokens
        self.symbol_table = {"IT": {"value": 'NOOB', "type": None}} # dictionary to store variables and their values
        self.errors = []
        self.log_function = log_function # function to log errors to the GUI
        self.current_line_number = None # current line number being analyzed
        self.lines = self._organize_tokens_by_line(tokens) # organize tokens by line number
        self.current_line_number = min(self.lines.keys()) if self.lines else None # get the first line number
        self.current_tokens = self.lines.get(self.current_line_number, []) # get the tokens for the first line
        self.current_position = 0  # position of the current token in the current line
        self.current_token = self.current_tokens[0] if self.current_tokens else None # get the first token in the current line
        self.error_messages = [] # list to store error messages
        self.console = console # reference to the console widget
        self.gui_symbol_table = gui_symbol_table # reference to the GUI symbol table widget
        self.in_wazzup_block = False # flag for 'WAZZUP' block

    # function to organize tokens by line number, excluding comments
    def _organize_tokens_by_line(self, tokens):
        lines = {}
        for token in tokens:
            if token.type != "Comment Line": # skip comments
                if token.line_number not in lines:
                    lines[token.line_number] = []
                lines[token.line_number].append(token)
        return lines

    # function to semantically analyze a single line
    def analyze_line(self):
        while self.current_token:
            # enter WAZZUP block
            if self.current_token.value == 'WAZZUP': 
                self.in_wazzup_block = True
                print("Entered 'WAZZUP' block")

            # exit WAZZUP block
            elif self.current_token.value == 'BUHBYE' and self.in_wazzup_block:  
                self.in_wazzup_block = False
                print("Exited 'WAZZUP' block")

            # variable declaration
            elif self.in_wazzup_block and self.current_token.value == 'I HAS A':  
                self.analyze_variable_declaration()

            # print statement
            elif self.current_token.type == 'Output Keyword':  
                self.analyze_visible()

            # input statement
            elif self.current_token.type == 'Input Keyword':  
                self.analyze_input()

            elif self.current_token.type == 'Variable Identifier':
                next_token = self.current_tokens[self.current_position + 1] if self.current_position + 1 < len(self.current_tokens) else None
                
                # variable assignment
                if next_token and next_token.type == 'Variable Assignment':  
                    self.analyze_assignment()

                # explicit typecasting
                elif next_token and next_token.type == 'Typecasting Operation':  
                    self.analyze_explicit_typecasting()

            # switch-case statement
            elif self.current_token.type == "Switch-Case Variable":
                self.analyze_switch(self.current_token.value)

            # operation
            elif self.current_token.type in ['Arithmetic Operation', 'Boolean Operation', 'Comparison Operation']:
                self.analyze_operation(self.current_token.value)

            # if-else statement
            elif self.current_token.value == "O RLY?":
                self.analyze_condition()

            # loop
            elif self.current_token.value == "IM IN YR":
                self.analyze_loop()

            # function declaration
            elif self.current_token.value == "HOW IZ I":
                self.analyze_function_declaration() 

            # function call
            elif self.current_token.value == "I IZ":
                function_call_start = self.current_line_number

                self.print_symbol_table()
                function_name, arguments = self.analyze_function_call()
                
                if hasattr(self, 'functions') and function_name in self.functions:
                    function_info = self.functions[function_name] # contain only the function name
                    
                    for i, param in enumerate(function_info['parameters']):
                        if i < len(arguments):
                            # check if the argument is a literal (meaning its value is stored in 'IT')
                            if TypeCaster.type_check(arguments[i]) in ['NUMBR', 'NUMBAR', 'TROOF', 'YARN']:
                                argument_value = arguments[i]
                                self.symbol_table[param] = argument_value
                            else:
                                argument_value = self.symbol_table[arguments[i]]['value']
                                self.symbol_table[param] = argument_value
                        else:
                            self.log_semantic_error(f"Missing argument for parameter '{param}'")

                    # after makuha value call this function to execute the body
                    self.execute_function_body(function_info, arguments, function_call_start)
                else:
                    self.log_semantic_error(f"Function '{function_name}' not defined.")

            # update the GUI symbol table
            self.update_symbol_table()

            # move to the next token in the current line
            self.advance_to_next_token()
    
    # function to advance to the next line of tokens
    def advance_to_next_line(self):
        if self.current_line_number is None:
            self.current_tokens = []
            self.current_token = None
            return
        
        line_numbers = sorted(self.lines.keys())
        next_line_index = line_numbers.index(self.current_line_number) + 1
        
        if next_line_index < len(line_numbers):
            self.current_line_number = line_numbers[next_line_index]
            self.current_tokens = self.lines[self.current_line_number]
            self.current_position = 0
            self.current_token = self.current_tokens[0] if self.current_tokens else None
        else:
            self.current_tokens = []
            self.current_token = None
            self.current_line_number = None

    # function to move to the next token in the current line
    def advance_to_next_token(self):
        if self.current_position < len(self.current_tokens) - 1:
            self.current_position += 1
            self.current_token = self.current_tokens[self.current_position]
        else:
            self.current_token = None
    
    # function to semantically analyze the code (entry point of the analyzer)
    def analyze_program(self):
        print("\nSEMANTIC ANALYSIS")
        
        while self.current_line_number is not None and self.current_token:
            print(f"\nAnalyzing line {self.current_line_number}: {self.current_tokens}")
            self.analyze_line()
            self.advance_to_next_line()
            
        return self.error_messages
    
    # function to check if a variable is being used before it's declared
    def check_variable_usage(self, token):
        if token.value not in self.symbol_table and token.type != 'Output Keyword':
            self.log_semantic_error(
                f"Variable '{token.value}' used before declaration.",
                context=f"Variable usage at line {token.line_number}"
            )
            return None

        if token.value not in self.symbol_table and token.type == 'Output Keyword': 
            return {'value': token.value, 'type': 'YARN'} 

        return self.symbol_table[token.value] 

    # function to log a semantic error with context
    def log_semantic_error(self, message, context=None):
        error_message = f"Semantic Error: {message}"
        if context:
            error_message += f" Context: {context}."
        
        self.error_messages.append(error_message)
        
        if self.log_function:
            self.log_function(error_message)
        print(f"{error_message}")

    # function to print the symbol table
    def print_symbol_table(self):
        print("\nSymbol Table:")
        for identifier, identifier_info in self.symbol_table.items():
            value = identifier_info.get("value", "undefined")
            type = identifier_info.get("type", "unknown")
            print(f"Identifier: {identifier}, Value: {value}, Type: {type}")
    
    # function to update the GUI symbol table
    def update_symbol_table(self):
        # clear the existing GUI symbol table
        self.gui_symbol_table.delete(*self.gui_symbol_table.get_children())
        
        # populate the GUI symbol table with updated data
        for identifier, details in self.symbol_table.items():
            self.gui_symbol_table.insert("", tk.END, values=(identifier, details["value"]))

    # function to semantically analyze a variable declaration
    def analyze_variable_declaration(self):
        # consume 'I HAS A'
        self.advance_to_next_token()

        variable_name = self.current_token.value

        # check if variable is already declared
        if variable_name in self.symbol_table:
            self.log_semantic_error(f"Variable '{variable_name}' is already declared", context=f"Line {self.current_token.line_number}")
            return

        # consume variable name
        self.advance_to_next_token()

        # check for initialization
        if self.current_token and self.current_token.value == 'ITZ':
            # consume 'ITZ'
            self.advance_to_next_token()

            # determine type and value based on initialization
            if not self.current_token:
                self.log_semantic_error(f"Missing value for initialization of variable '{variable_name}'", context=f"Line {self.current_token.line_number}")
                return

            # get value and type
            current_token = self.current_token

            value = self.analyze_expression(current_token, variable_name)
            data_type = self.get_token_type(current_token)

            if data_type is not None: 
                # simply store the value and type in the symbol table
                self.symbol_table[variable_name] = {
                    'value': value,
                    'type': data_type
                }
            else:
                # update the type following evaluation of the operation
                data_type = self.symbol_table[variable_name]['type']

            # consume initialization value
            self.advance_to_next_token()
            
            print(f"Declared variable {variable_name} initialized to {value} of type {data_type}")
        else:
            # uninitialized variable
            self.symbol_table[variable_name] = {
                'value': 'NOOB',
                'type': 'NOOB'
            }
            
            # consume variable declaration
            self.advance_to_next_token()
            
            print(f"Declared uninitialized variable {variable_name} of type NOOB")
    
    # helper function to get the type of a token
    def get_token_type(self, token):
        if token.type == 'String Delimiter':
            return 'YARN'
        elif token.type == 'NUMBAR Literal':
            return 'NUMBAR'
        elif token.type == 'NUMBR Literal':
            return 'NUMBR'
        elif token.type == 'TROOF Literal':
            return 'TROOF'
        elif token.type in ['Arithmetic Operation', 'Boolean Operation', 'Comparison Operation', 'String Concatenation', 'Typecasting Operation']:
            return None
        else:
            return 'NOOB'
    
    # function to determine or evaluate the value of an expression
    def analyze_expression(self, token, variable_name):
        if token.type in ['NUMBR Literal', 'NUMBAR Literal', 'TROOF Literal']:
            return token.value
        elif token.type == 'String Delimiter':
            return self.analyze_string(token)
        elif token.type == 'Variable Identifier':
            variable_info = self.check_variable_usage(token)
            if variable_info:
                return variable_info['value']
            else:
                return None
        elif token.type in ['Arithmetic Operation', 'Boolean Operation', 'Comparison Operation']: # operation
            return self.analyze_operation(variable_name)
        else:
            return None
    
    # function to semantically analyze a string
    def analyze_string(self, token):
        # first, validate that we're dealing with a string
        if token.type != 'String Delimiter':
            self.log_semantic_error("Invalid string token", context=f"Expected string delimiter at line {token.line_number}")
            return None

        # consume the opening delimiter
        self.advance_to_next_token()

        # check if we have a valid literal
        if not self.current_token or self.current_token.type != 'Literal':
            self.log_semantic_error("Missing string literal", context=f"Expected string content at line {token.line_number}")
            return None

        # extract the string content
        string_content = self.current_token.value

        # consume the string literal
        self.advance_to_next_token()

        # verify closing delimiter
        if not self.current_token or self.current_token.type != 'String Delimiter':
            self.log_semantic_error("Unclosed string", context=f"Missing closing delimiter at line {token.line_number}")
            return None

        # consume the closing delimiter
        self.advance_to_next_token()
        
        return string_content
    
    # function to determine the operation 
    def analyze_operation(self, variable_name):
        operation = self.current_token.value
        
        # consume the operation
        self.advance_to_next_token()

        if operation == 'NOT': # unary operation
            return self.evaluate_unary_operation(variable_name)
        elif operation in ['SUM OF', 'DIFF OF', 'PRODUKT OF', 'QUOSHUNT OF', 'MOD OF', 'BIGGR OF', 'SMALLR OF', 'BOTH OF', 'EITHER OF', 'WON OF', 'BOTH SAEM', 'DIFFRINT']: # binary operations
            return self.evaluate_binary_operation(operation, variable_name)
        elif operation in ['ALL OF', 'ANY OF']: # infinite-arity operations
            return self.evaluate_infinite_arity_operation(operation)
        elif operation == 'SMOOSH': # string concatenation
            return self.analyze_concatenation(operation)
        else: # unknown operation
            self.log_semantic_error(f"Unknown operation '{operation}'", context="Semantic analysis failed")
            return None
    
    # function to assign a value to a variable
    def analyze_assignment(self):
        variable_name = self.current_token.value
        self.advance_to_next_token() # consume the variable identifier

        if self.current_token.value == 'R': # check for the assignment operator 'R'
            self.advance_to_next_token() # consume 'R'

            if self.current_token.type in ['NUMBR Literal', 'NUMBAR Literal', 'TROOF Literal', 'Variable Identifier']: # NUMBR, NUMBAR, TROOF, or variable
                value = self.current_token.value
                result_type = self.get_token_type(self.current_token)
            elif self.current_token.type == 'String Delimiter': # string literal
                value = self.analyze_string(self.current_token)
                result_type = 'YARN'
            elif self.current_token.type in ['Arithmetic Operation', 'Boolean Operation', 'Comparison Operation']: # operation
                value = self.analyze_operation(variable_name)
                result_type = TypeCaster.type_check(value)
            elif self.current_token.type == 'String Concatenation': # string concatenation
                value = self.analyze_concatenation()
                result_type = 'YARN'
            elif self.current_token.type == 'Typecasting Operation': # explicit typecasting
                value, result_type = self.analyze_explicit_typecasting()
            else:
                self.log_semantic_error(f"Invalid assignment value for variable '{variable_name}'", context=f"Line {self.current_token.line_number}")
                return None

            # update the symbol table entry for the variable
            if variable_name in self.symbol_table:
                self.symbol_table[variable_name]['value'] = value
                self.symbol_table[variable_name]['type'] = result_type
                print(f"Updated variable '{variable_name}' to value '{value}' of type {result_type}")
            else:
                self.log_semantic_error(f"Variable '{variable_name}' not declared before assignment", context=f"Line {self.current_token.line_number}")

    # function to analyze explicit typecasting
    def analyze_explicit_typecasting(self):
        if self.current_token.value == 'MAEK A':
            self.advance_to_next_token() # consume 'MAEK A'

            if self.current_token and self.current_token.type in ['Variable Identifier', 'NUMBR Literal', 'NUMBAR Literal', 'TROOF Literal']:
                cast_value = self.current_token.value
                self.advance_to_next_token() # consume the value to cast
                
                if self.current_token and self.current_token.type == 'Type Literal':
                    target_type = self.current_token.value

                    # check if the variable is declared
                    if cast_value not in self.symbol_table:
                        self.log_semantic_error(f"Variable '{cast_value}' not declared before typecasting", context=f"Line {self.current_token.line_number}")
                        return None
                    
                    # perform the explicit typecasting
                    try:
                        # get the original value and cast it to the target type
                        original_value = self.symbol_table[cast_value]['value']
                        original_type = self.symbol_table[cast_value]['type']
                        casted_value = TypeCaster.explicit_cast(original_value, target_type)

                        # change true/false to WIN/FAIL
                        if target_type == 'TROOF':
                            casted_value = 'WIN' if casted_value else 'FAIL'

                        # update the implicit 'IT' variable
                        self.symbol_table['IT']['value'] = casted_value
                        self.symbol_table['IT']['type'] = target_type

                        print(f"Typecasted value of variable 'IT' to type {target_type}")
                        return original_value, original_type
                    
                    except Exception as e:
                        self.log_semantic_error(f"Error during typecasting: {e}", context="Semantic evaluation failed")
                        return None
                
        self.advance_to_next_token() # consume variable identifier

        if self.current_token.value == 'IS NOW A':
            cast_value = self.current_tokens[self.current_position - 1].value
            self.advance_to_next_token() # consume 'IS NOW A'

            if self.current_token and self.current_token.type == 'Type Literal':
                target_type = self.current_token.value
                self.advance_to_next_token() # consume the type literal

                # check if the variable is declared
                if cast_value not in self.symbol_table:
                    self.log_semantic_error(f"Variable '{cast_value}' not declared before typecasting", context=f"Line {self.current_token.line_number}")
                    return None
                
                # perform the explicit typecasting
                try:
                    # get the original value and cast it to the target type
                    original_value = self.symbol_table[cast_value]['value']
                    casted_value = TypeCaster.explicit_cast(original_value, target_type)

                    # change true/false to WIN/FAIL
                    if target_type == 'TROOF':
                        casted_value = 'WIN' if casted_value else 'FAIL'

                    # update the symbol table entry
                    self.symbol_table[cast_value]['value'] = casted_value
                    self.symbol_table[cast_value]['type'] = target_type

                    print(f"Typecasted value of variable '{cast_value}' to type {target_type}")
                    return None
                
                except Exception as e:
                    self.log_semantic_error(f"Error during typecasting: {e}", context="Semantic evaluation failed")
                    return None

    # function to evaluate a unary operation
    def evaluate_unary_operation(self, variable_name):
        # determine the type and value of the operand
        if self.get_token_type(self.current_token) == 'TROOF':
            # direct boolean literal
            operand_value = self.current_token.value
            operand_type = 'TROOF'
        elif self.current_token.type == 'Variable Identifier':
            # variable - check if it's declared and has a valid type
            variable_info = self.check_variable_usage(self.current_token)
            if not variable_info:
                return None
            operand_value = variable_info['value']
            operand_type = variable_info['type']
        elif self.current_token.type in ['Arithmetic Operation', 'Boolean Operation', 'Comparison Operation']:
            # nested operation - recursively analyze
            operand_value = self.analyze_operation(self.current_token)
            operand_type = self.get_token_type(self.current_token)
        else:
            # semantic error for invalid operand type
            self.log_semantic_error(f"Invalid operand type for 'NOT' operation", context=f"Actual operand type: {self.get_token_type(self.current_token)}")
            return None

        # semantic check for 'NOT' operation type compatibility
        if operand_type != 'TROOF':
            self.log_semantic_error(f"Unary 'NOT' operation requires TROOF operand", context=f"Actual operand type: {operand_type}")
            return None

        # perform the 'NOT' operation
        try:
            bool_value = TypeCaster.implicit_cast_to_troof(operand_value)
            result = 'FAIL' if bool_value else 'WIN'

            print(f"NOT {operand_value} = {result}")

            # if the variable is a valid identifier, store the result in the variable
            if variable_name not in ['NOT', 'BOTH OF', 'EITHER OF', 'WON OF', 'BOTH SAEM', 'DIFFRINT']:  
                self.symbol_table[variable_name] = {
                    'value': result,
                    'type': 'TROOF'
                }
                print(f"Stored result '{result}' in variable '{variable_name}'")
            
            else:
                # otherwise, store the result in the 'IT' variable
                self.symbol_table['IT'] = {
                    'value': result,
                    'type': 'TROOF'
                }
                print(f"Stored result '{result}' in implicit variable 'IT'")

            self.advance_to_next_token()
            return result
        except Exception as e:
            self.log_semantic_error(f"Error evaluating 'NOT' operation: {e}", context="Semantic evaluation failed")
            return None

    # function to analyze the 'VISIBLE' statement
    def analyze_visible(self):
        self.advance_to_next_token() # consume 'VISIBLE'
        output = []
        temp_output = [] # temporary list to store output before variable checks
        suppress_newline = False

        while self.current_token:
            if self.current_token.type in ['NUMBR Literal', 'NUMBAR Literal', 'TROOF Literal', 'Variable Identifier']: # handle literals and variables
                temp_output.append(self.current_token.value)
                self.advance_to_next_token()
            elif self.current_token.type == 'String Delimiter': # handle strings
                temp_output.append(self.analyze_string(self.current_token))
            elif self.current_token.type in ['Arithmetic Operation', 'Boolean Operation', 'Comparison Operation']: # handle operations
                temp_output.append(str(self.analyze_operation(self.current_token.value)))
            elif self.current_token.type == 'String Concatenation': # handle string concatenation
                temp_output.append(self.analyze_concatenation())
            elif self.current_token.type == 'Infinite Arity Operation': # handle infinite arity operations
                temp_output.append(str(self.evaluate_infinite_arity_operation(self.current_token.value)))
            elif self.current_token.type in ['Parameter Delimiter', 'Output Separator']: # handle delimiters
                self.advance_to_next_token()
            elif self.current_token.type == 'Suppress Newline': # handle newline suppression
                suppress_newline = True
                self.advance_to_next_token()
            else:
                self.log_semantic_error(f"Unexpected token in VISIBLE: {self.current_token.value}", context=f"Line {self.current_token.line_number}")  # Use correct arguments
                break

        # now that the expression is analyzed, check variable usage
        for item in temp_output:
            if isinstance(item, str) and item in self.symbol_table: # check if it's a variable in the symbol table
                output.append(str(self.symbol_table[item]['value'])) # use the value from the symbol table
            else:
                output.append(str(item)) # append other items as strings

        print(f"Printed '{''.join(output)}' to console")
        
        if suppress_newline:
            self.console.insert(tk.END, ''.join(output))
        else:
            self.console.insert(tk.END, ''.join(output) + "\n")

    # function to recursively evaluate nested binary operations
    def evaluate_binary_operation(self, operation, variable_name):        
        # helper function to analyze the operand
        def analyze_operand():
            # handle NOT operation first
            if self.current_token.value == 'NOT':
                self.advance_to_next_token()
                return self.evaluate_unary_operation(variable_name)
            
            # nested arithmetic operation
            if self.current_token.type == 'Arithmetic Operation':
                nested_op = self.current_token.value
                self.advance_to_next_token()
                return self.evaluate_binary_operation(nested_op, variable_name)
            
            # nested boolean operation
            if self.current_token.type == 'Boolean Operation':
                nested_op = self.current_token.value
                self.advance_to_next_token()
                # Special handling for nested boolean operations
                if nested_op in ['BOTH OF', 'EITHER OF', 'WON OF', 'BOTH SAEM', 'DIFFRINT']:
                    return self.evaluate_binary_operation(nested_op, variable_name)
            
            # variable identifier
            elif self.current_token.type == 'Variable Identifier':
                var_name = self.current_token.value
                if var_name in self.symbol_table:
                    self.advance_to_next_token()
                    return self.symbol_table[var_name]['value']
                else:
                    self.log_semantic_error(f"Variable '{var_name}' used before declaration", context=f"Line {self.current_token.line_number}")
                    self.advance_to_next_token()
                    return None
            
            # literal values with implicit type casting
            elif self.current_token.type in ['NUMBR Literal', 'NUMBAR Literal', 'TROOF Literal']:
                # use type casting for different literal types
                value = self.current_token.value
                if self.current_token.type == 'NUMBR Literal':
                    value = int(value)
                elif self.current_token.type == 'NUMBAR Literal':
                    value = float(value)
                elif self.current_token.type == 'TROOF Literal':
                    value = True if value.lower() == 'win' else False
                
                self.advance_to_next_token()
                return value
            
            # string literal
            if (self.current_token.type == 'String Delimiter'):
                return self.analyze_string(self.current_token)
            
            else:
                self.log_semantic_error(f"Invalid operand for binary operation '{operation}'", context=f"Actual operand type: {self.get_token_type(self.current_token)}")
                return None
        
        # get first operand
        first_operand = analyze_operand()

        # handle 'AN' delimiter
        if self.current_token and self.current_token.value == 'AN':
            self.advance_to_next_token()
        elif operation in ['BOTH SAEM', 'DIFFRINT']:
            # for comparison operations, 'AN' is required
            self.log_semantic_error(f"Expected 'AN' after first operand in '{operation}'", context=f"Line {self.current_token.line_number if self.current_token else 'Unknown'}")
            return None

        # check if the next operation is an additional relational operation
        additional_operation = None
        if operation in ['BOTH SAEM', 'DIFFRINT'] and self.current_token and self.current_token.type == 'Arithmetic Operation':
            if self.current_token.value in ['BIGGR OF', 'SMALLR OF']:
                additional_operation = self.current_token.value
                self.advance_to_next_token()
        
        # get second operand (could be part of a relational operation)
        second_operand = analyze_operand()

        # if there's an additional operation, get the third operand
        if additional_operation:
            # expecting 'AN' delimiter
            if self.current_token and self.current_token.value == 'AN':
                self.advance_to_next_token()
            else:
                self.log_semantic_error(f"Expected 'AN' after first operand of '{additional_operation}'", context=f"Line {self.current_token.line_number if self.current_token else 'Unknown'}")
                return None

            # get third operand
            third_operand = analyze_operand()
            
            # now, evaluate the relational comparison
            result = self.evaluate_comparison_operation(operation, additional_operation, second_operand, third_operand)
        else:
            # no additional operation; perform basic comparison or regular binary operation
            if operation in ['BOTH SAEM', 'DIFFRINT']:
                # basic comparison
                result = self.evaluate_comparison_operation(operation, None, first_operand, second_operand)
            else:
                # regular binary operation
                # perform the operation
                try:
                    # evaluate arithmetic operations
                    if operation in ['SUM OF', 'DIFF OF', 'PRODUKT OF', 'QUOSHUNT OF', 'MOD OF', 'BIGGR OF', 'SMALLR OF']:
                        result = self.evaluate_arithmetic_operation(operation, first_operand, second_operand)
                        
                        print(f"{operation} {first_operand} AN {second_operand} = {result}")
                        
                        # determine result type based on input types
                        result_type = 'NUMBAR' if isinstance(result, float) else 'NUMBR'
                        
                        if variable_name not in ['SUM OF', 'DIFF OF', 'PRODUKT OF', 'QUOSHUNT OF', 'MOD OF', 'BIGGR OF', 'SMALLR OF']:
                            # if the variable is a valid identifier, store the result in the variable
                            self.symbol_table[variable_name] = {
                                'value': result,
                                'type': result_type
                            }
                            print(f"Stored result '{result}' in variable '{variable_name}'")
                        else:
                            # otherwise, store the result in the 'IT' variable
                            self.symbol_table['IT'] = {
                                'value': result,
                                'type': result_type
                            }
                            print(f"Stored result '{result}' in implicit variable 'IT'")
                        
                        return result

                    # evaluate boolean operations
                    elif operation in ['BOTH OF', 'EITHER OF', 'WON OF']:
                        result = self.evaluate_boolean_operation(operation, first_operand, second_operand)
                        result_type = 'TROOF'

                        print(f"{operation} {first_operand} AN {second_operand} = {result}")

                        if variable_name not in ['BOTH OF', 'EITHER OF', 'WON OF']:
                            # if the variable is a valid identifier, store the result in the variable
                            self.symbol_table[variable_name] = {
                                'value': result,
                                'type': result_type
                            }
                            print(f"Stored result '{result}' in variable '{variable_name}'")
                        else:
                            # otherwise, store the result in the 'IT' variable
                            self.symbol_table['IT'] = {
                                'value': result,
                                'type': result_type
                            }
                            print(f"Stored result '{result}' in implicit variable 'IT'")
                            
                        return result

                    else:
                        self.log_semantic_error(f"Unknown binary operation '{operation}'", context="Semantic evaluation failed")
                except Exception as e:
                    self.log_semantic_error(f"Error evaluating binary operation '{operation}': {e}", context="Semantic evaluation failed")
                    return None

        # after evaluating, store the result
        if operation in ['BOTH SAEM', 'DIFFRINT']:
            troof_result = result
            result_type = 'TROOF'

            if variable_name not in ['BOTH SAEM', 'DIFFRINT']:
                # if the variable is a valid identifier, store the result in the variable
                self.symbol_table[variable_name] = {
                    'value': troof_result,
                    'type': result_type
                }
                print(f"Stored result '{troof_result}' in variable '{variable_name}'")
            else:
                # otherwise, store the result in the 'IT' variable
                self.symbol_table['IT'] = {
                    'value': troof_result,
                    'type': result_type
                }
                print(f"Stored result '{troof_result}' in implicit variable 'IT'")

        return result
    
    # function to evaluate arithmetic operations
    def evaluate_arithmetic_operation(self, operation, operand1, operand2):
        # implicit type casting for numeric operands
        operand1 = TypeCaster.implicit_cast_to_numeric(operand1)
        operand2 = TypeCaster.implicit_cast_to_numeric(operand2)

        if operation == 'SUM OF': # addition
            return operand1 + operand2
        elif operation == 'DIFF OF': # subtraction
            return operand1 - operand2
        elif operation == 'PRODUKT OF': # multiplication
            return operand1 * operand2
        elif operation == 'QUOSHUNT OF': # division
            if operand2 == 0:
                self.log_semantic_error("Division by zero", context="Semantic evaluation failed")
                return None
            return operand1 / operand2
        elif operation == 'MOD OF': # modulo
            if operand2 == 0:
                self.log_semantic_error("Division by zero", context="Semantic evaluation failed")
                return None
            return operand1 % operand2
        elif operation == 'BIGGR OF': # maximum
            return max(operand1, operand2)
        elif operation == 'SMALLR OF': # minimum
            return min(operand1, operand2)
        else:
            self.log_semantic_error(f"Unknown arithmetic operation '{operation}'")
            return None

    # function to evaluate boolean operations
    def evaluate_boolean_operation(self, operation, operand1, operand2):
        # implicit type casting for boolean operands
        operand1 = TypeCaster.implicit_cast_to_troof(operand1)
        operand2 = TypeCaster.implicit_cast_to_troof(operand2)

        if operation == 'BOTH OF': # AND
            return 'WIN' if operand1 and operand2 else 'FAIL'
        
        elif operation == 'EITHER OF': # OR
            return 'WIN' if operand1 or operand2 else 'FAIL'
        
        elif operation == 'WON OF': # XOR
            return 'WIN' if operand1 ^ operand2 else 'FAIL'
        
        else:
            self.log_semantic_error(f"Unknown boolean operation '{operation}'")
            return None
    
    # function to evaluate comparison operations
    def evaluate_comparison_operation(self, operation, additional_operation, operand1, operand2):
        # implicit type casting for numeric operands
        operand1 = TypeCaster.implicit_cast_to_numeric(operand1)
        operand2 = TypeCaster.implicit_cast_to_numeric(operand2)
        
        # check if operands can be compared
        if not TypeCaster.can_compare(operand1, operand2):
            self.log_semantic_error("Cannot compare these values. Ensure both operands are numeric (NUMBR or NUMBAR).", context="Comparison Evaluation")
            return None

        # initialize result
        result = False

        # perform comparison based on operation and additional_operation
        if additional_operation is None:
            # basic comparison
            if operation == 'BOTH SAEM': # equality
                result = operand1 == operand2
                print(f"BOTH SAEM {operand1} AN {operand2} = {'WIN' if result else 'FAIL'}")
            elif operation == 'DIFFRINT': # inequality
                result = operand1 != operand2
                print(f"DIFFRINT {operand1} AN {operand2} = {'WIN' if result else 'FAIL'}")
            else:
                self.log_semantic_error(f"Unknown comparison operation '{operation}'",context="Comparison Evaluation")
                return None
        else:
            # relational comparison
            if additional_operation == 'BIGGR OF':
                if operation == 'BOTH SAEM': # greater than or equal to
                    result = operand1 >= operand2
                    print(f"BOTH SAEM {operand1} AN BIGGR OF {operand1} AN {operand2} = {'WIN' if result else 'FAIL'}")
                elif operation == 'DIFFRINT': # less than
                    result = operand1 < operand2
                    print(f"DIFFRINT {operand1} AN BIGGR OF {operand1} AN {operand2} = {'WIN' if result else 'FAIL'}")
                else:
                    self.log_semantic_error(f"Unknown comparison operation '{operation}' with additional operation '{additional_operation}'", context="Comparison Evaluation")
                    return None
            elif additional_operation == 'SMALLR OF':
                if operation == 'BOTH SAEM': # less than or equal to
                    result = operand1 <= operand2
                    print(f"BOTH SAEM {operand1} AN SMALLR OF {operand1} AN {operand2} = {'WIN' if result else 'FAIL'}")
                elif operation == 'DIFFRINT': # greater than
                    result = operand1 > operand2
                    print(f"DIFFRINT {operand1} AN SMALLR OF {operand1} AN {operand2} = {'WIN' if result else 'FAIL'}")
                else:
                    self.log_semantic_error(f"Unknown comparison operation '{operation}' with additional operation '{additional_operation}'", context="Comparison Evaluation")
                    return None
            else:
                self.log_semantic_error(f"Unknown additional operation '{additional_operation}' for comparison", context="Comparison Evaluation")
                return None

        # convert boolean result to TROOF
        troof_result = 'WIN' if result else 'FAIL'

        return troof_result

    # function to evaluate analyze infinite-arity operations
    def evaluate_infinite_arity_operation(self, operation):
        operands = []
        
        # get operands
        while self.current_token and self.current_token.value != 'MKAY':
            # handle 'AN' token
            if self.current_token.value == 'AN':
                self.advance_to_next_token()
                continue
            
            # analyze operand 
            def analyze_operand():
                # nested arithmetic operation
                if self.current_token.type == 'Arithmetic Operation':
                    nested_op = self.current_token.value
                    self.advance_to_next_token()
                    return self.evaluate_binary_operation(nested_op, 'IT')
                
                # variable identifier
                elif self.current_token.type == 'Variable Identifier':
                    var_name = self.current_token.value
                    if var_name in self.symbol_table:
                        self.advance_to_next_token()
                        return self.symbol_table[var_name]['value']
                    else:
                        self.log_semantic_error(f"Variable '{var_name}' used before declaration", context=f"Line {self.current_token.line_number}")
                        self.advance_to_next_token()
                        return False
                
                # literal values with implicit type casting
                elif self.current_token.type in ['NUMBR Literal', 'NUMBAR Literal', 'TROOF Literal']:
                    value = self.current_token.value
                    if self.current_token.type == 'NUMBR Literal':
                        value = int(value)
                    elif self.current_token.type == 'NUMBAR Literal':
                        value = float(value)
                    elif self.current_token.type == 'TROOF Literal':
                        value = True if value.lower() == 'win' else False
                    
                    self.advance_to_next_token()
                    return value
                
                # string literal
                elif self.current_token.type == 'String Delimiter':
                    return self.analyze_string(self.current_token)
                
                # boolean operations
                elif self.current_token.type in ['Boolean Operation', 'Comparison Operation', 'Arithmetic Operation']:
                    operation_value = self.current_token.value
                    self.advance_to_next_token()
                    
                    # detect nested operations based on operation type
                    if operation_value in ['BOTH OF', 'EITHER OF', 'WON OF', 'BOTH SAEM', 'DIFFRINT']:
                        return self.evaluate_boolean_operation(operation_value, None, None)
                    elif operation_value in ['SUM OF', 'DIFF OF', 'PRODUKT OF', 'QUOSHUNT OF', 'MOD OF', 'BIGGR OF', 'SMALLR OF']:
                        return self.evaluate_arithmetic_operation(operation_value, None, None)
                
                else:
                    self.log_semantic_error(f"Invalid operand for infinite-arity operation '{operation}'", context=f"Actual operand type: {self.current_token.type}")
                    return False
            
            # get operand and add to list
            operand = TypeCaster.implicit_cast_to_troof(analyze_operand())
            operands.append(operand)
            
            # break if MKAY reached
            if self.current_token and self.current_token.value == 'MKAY':
                break
        
        # consume 'MKAY'
        if self.current_token and self.current_token.value == 'MKAY':
            self.advance_to_next_token()
        
        # evaluate the operation
        if operation == 'ALL OF':
            # ALL OF is a logical AND across all operands
            result = all(operands)

            # replace all operands from true/false to WIN/FAIL
            operands = ['WIN' if operand else 'FAIL' for operand in operands]
            print(f"ALL OF {' AN '.join(map(str, operands))} = {'WIN' if result else 'FAIL'}")
            
            # store result in symbol table
            self.symbol_table['IT'] = {
                'value': 'WIN' if result else 'FAIL',
                'type': 'TROOF'
            }

            print(f"Stored result '{'WIN' if result else 'FAIL'}' in implicit variable 'IT'")

            return 'WIN' if result else 'FAIL'
        
        elif operation == 'ANY OF':
            # ANY OF is a logical OR across all operands
            result = any(operands)

            # replace all operands from true/false to WIN/FAIL
            operands = ['WIN' if operand else 'FAIL' for operand in operands]
            print(f"ANY OF {' AN '.join(map(str, operands))} = {'WIN' if result else 'FAIL'}")
            
            # store result in symbol table
            self.symbol_table['IT'] = {
                'value': 'WIN' if result else 'FAIL',
                'type': 'TROOF'
            }

            print(f"Stored result '{'WIN' if result else 'FAIL'}' in implicit variable 'IT'")

            return 'WIN' if result else 'FAIL'
        
        else:
            self.log_semantic_error(f"Unknown infinite-arity operation '{operation}'")
            return None

    # function to semantically analyze string concatenation
    def analyze_concatenation(self):
        operands = []
        self.advance_to_next_token() # consume 'SMOOSH'
        while self.current_token:
            if self.current_token.type in ['NUMBR Literal', 'NUMBAR Literal', 'TROOF Literal', 'Variable Identifier']: # literal or variable
                variable_info = self.check_variable_usage(self.current_token)
                if variable_info:
                    operands.append(str(variable_info['value']))
                else:
                    operands.append(str(self.current_token.value))
                self.advance_to_next_token()
            elif self.current_token.type == 'String Delimiter': # string
                operands.append(self.analyze_string(self.current_token))
            elif self.current_token.type in ['Arithmetic Operation', 'Boolean Operation', 'Comparison Operation']: # operation
                operands.append(self.analyze_operation(self.current_token.value))  
            elif self.current_token.value == 'AN': # delimiter
                self.advance_to_next_token()
            else:
                self.log_semantic_error("Unexpected token in SMOOSH", token=self.current_token)
                break
        if not operands:
            self.log_semantic_error("No operands specified after SMOOSH")
        elif len(operands) == 1:
            self.log_semantic_error("Only one operand specified after SMOOSH, requires at least two")
        return ''.join(operands)
    
    # function to handle user input
    def analyze_input(self):
        self.advance_to_next_token() # consume 'GIMMEH'

        # store variable name
        variable_name = self.current_token.value

        # check if variable is already declared
        variable_info = self.check_variable_usage(self.current_token)

        if not variable_info:
            return None
        
        # prompt user for input
        input_value = sd.askstring(
            "Input", 
            f"Please enter a value for '{variable_name}'"
        )
        
        # check if input was provided
        if input_value is not None:
            # store the input value in the symbol table
            self.symbol_table[variable_name] = {
                'value': input_value,
                'type': 'YARN'
            }
            
            print(f"Stored input value '{input_value}' in variable '{variable_name}'")
        
        print(f"Printed '{input_value}' to console")
        self.console.insert(tk.END, input_value + "\n")

        # consume variable name
        self.advance_to_next_token()

        return None

    # function to analyze the 'SWITCH' statement
    def analyze_switch(self, switch_variable):
        print("Switch variable:", switch_variable)

        if switch_variable not in self.symbol_table:
            self.log_semantic_error(
                message=f"Switch variable '{switch_variable}' is not declared.",
                context=f"Line {self.current_line_number}"
            )
            return False

        switch_variable_value = self.symbol_table[switch_variable]['value']
        print("Switch variable value:", switch_variable_value)

        case_values = []
        has_default = False
        duplicate_case = False
        found_matching_case = False

        while self.current_token:
            if self.current_token.value == "OIC":
                break  # End of the switch block

            if self.current_token.value == "OMG":
                print("DEBUG SEMANTICS: Found 'OMG'")
                self.advance_to_next_token()  # Consume 'OMG'

                if not self.current_token or self.current_token.type not in ["NUMBR Literal", "NUMBAR Literal", "YARN Literal", "TROOF Literal"]:
                    self.log_semantic_error(
                        f"Expected literal value after 'OMG'. Found: {self.current_token.value if self.current_token else 'None'}"
                    )
                    return False

                # Handle duplicate case values
                if self.current_token.value in case_values:
                    duplicate_case = True

                case_value = self.current_token.value
                case_values.append(case_value)
                print(f"DEBUG SEMANTICS: Found case value: {case_value}")
                self.advance_to_next_token()  # Consume the case value

                # Check if this case matches the switch variable value
                if switch_variable_value == case_value:
                    found_matching_case = True
                    self.advance_to_next_line()  # Move to the case block's first line
                    if self.analyze_case_block():
                        return True  # Exit the entire switch if 'GTFO' was encountered
                else:
                    # Skip this case block if it doesn't match
                    while self.current_token and self.current_token.value not in ['OMG', 'OMGWTF', 'OIC']:
                        self.advance_to_next_line()

            elif self.current_token.value == "OMGWTF":
                has_default = True
                if not found_matching_case:  # Only execute default if no case matched
                    self.advance_to_next_token()
                    self.advance_to_next_line()
                    if self.analyze_case_block():
                        return True  # Exit the entire switch if 'GTFO' was encountered
                else:
                    # Skip default block if a case has matched
                    while self.current_token and self.current_token.value != 'OIC':
                        self.advance_to_next_line()

            self.advance_to_next_line()

        # Check if no case matched and there's no default
        if switch_variable_value not in case_values and not has_default:
            self.log_semantic_error(
                message="Switch statement has no matching case or default case.",
                context=f"Line {self.current_line_number}"
            )
            return False
        
        if duplicate_case:
            self.log_semantic_error(
                message="Switch statement has duplicate case values."
            )
            return False

        return True
    
    def analyze_case_block(self):
        print("Analyzing case block")
        while self.current_token and self.current_token.value not in ['OMG', 'OMGWTF', 'OIC']:
            print(f"DEBUG: Current token: {self.current_token.value} (Type: {self.current_token.type})")
            if self.current_token.value == 'GTFO':
                print("Found 'GTFO'")
                self.advance_to_next_token()  # Move past 'GTFO'
                
                break

            # Execute the current line and advance to next line
            self.analyze_line()
            self.advance_to_next_line()

        return False  # No 'GTFO' encountered, continue to the next case block

    #if else semantic analysis
    def analyze_condition(self):
        print("Analyzing condition (IF ELSE)")
        self.advance_to_next_token()  # Consume 'O RLY?'
        
        # Ensure 'YA RLY' follows, possibly on the next line
        while not self.current_token and self.current_line_number is not None:
            self.advance_to_next_line()  # Move to the next line if no token is found on the current line

        '''
        uncomment this pag okei na yung bool
        '''
        comparison_value = self.symbol_table['IT']['value']
        print(f"IT value: {comparison_value}")

        # comparison_value = 'WIN' # Temporary value for testing
        found_ya_rly = False  # Flag to track if YA RLY is found
        mebbe_flag = False # Flag to track if MEBBE is found
        
        print("BEFORE WHILE LOOP INSIDE THE CONDITION")
        while self.current_token:
            while not self.current_token and self.current_line_number is not None:
                self.advance_to_next_line()  # Move to the next line if no token is found on the current line
            
            if self.current_token.value == 'OIC':
                break

            if self.current_token.value == 'YA RLY' and comparison_value == 'WIN':
                print("Found 'YA RLY'")
                self.advance_to_next_token()  # Consume 'YA RLY'
                
                print("FOUND YA RLY VALUE: ", found_ya_rly)
                
                while not self.current_token and self.current_line_number is not None:
                    self.advance_to_next_line()  # Move to the next line if no token is found on the current line

                while self.current_token and self.current_token.value not in ['NO WAI', 'OIC', 'MEBBE']:
                    self.analyze_line()
                    self.advance_to_next_line()

                    found_ya_rly = True   

            elif self.current_token.value == 'MEBBE' and (not found_ya_rly and comparison_value == 'FAIL'):
                print("Found MEBBE")
                
                self.advance_to_next_token()  # Consume 'MEBBE'

                # Evaluate MEBBE's condition
                self.analyze_line()

                mebbe_condition_result = self.symbol_table['IT']['value']
                print(f"MEBBE condition result: {mebbe_condition_result}")

                if mebbe_condition_result == 'WIN':
                    print("MEBBE condition is true")

                    while not self.current_token and self.current_line_number is not None:
                        self.advance_to_next_line()  # Move to the next line if no token is found on the current line

                    while self.current_token and self.current_token.value not in ['NO WAI', 'YA RLY', 'MEBBE']:
                        self.analyze_line()
                        self.advance_to_next_line()
                        mebbe_flag = True

                        if self.current_token.value == 'NO WAI':
                            mebbe_flag = False
                            break
                
            elif self.current_token.value == 'NO WAI':
                print(f"Entering NO WAI block. comparison_value: {comparison_value}, found_ya_rly: {found_ya_rly}, mebbe_flag: {mebbe_flag}")
                if comparison_value == 'FAIL' and not found_ya_rly and not mebbe_flag:
                    print("Executing NO WAI block")
                    self.advance_to_next_token()
                    
                    while not self.current_token and self.current_line_number is not None:
                        self.advance_to_next_line()
                    
                    while self.current_token and self.current_token.value not in ['YA RLY', 'OIC', 'MEBBE']:
                        self.analyze_line()
                        # self.advance_to_next_line()

            self.advance_to_next_line()

        return True
    
    # semantic analysis for the LOOP
    def analyze_loop(self):
        print("Analyzing loop")
        self.advance_to_next_token()  # Consume 'IM IN YR'

        # get loop type
        print("current token value: ", self.current_token.value)
        while self.current_token:
            if self.current_token and self.current_token.value == 'NERFIN':
                self.advance_to_next_token()  # consume NERFIN
                self.nerfin_loop()  # No need to pass loop_start here
                break

            elif self.current_token and self.current_token.value == 'UPPIN':
                self.advance_to_next_token()  # consume UPPIN
                self.uppin_loop()  # No need to pass loop_start here
                break

            self.advance_to_next_token()

        return True
    
    #nerfin loop
    # nerfin loop
    def nerfin_loop(self):
        # After getting loop type
        # R used to assign a value to an already created data type

        print("Before consuming nerfin current token value: ", self.current_token.value) # consume NERFIN

        # Right after nerfin is YR
        if self.current_token.value == 'YR':
            self.advance_to_next_token()  # consume YR
    
            # Get the loop variable
            loop_variable = self.current_token.value
            print("Loop condition Variable: ", loop_variable)

            # Ensure the loop variable exists
            if loop_variable not in self.symbol_table:
                self.log_semantic_error(f"Variable '{loop_variable}' used before declaration", context=f"Line {self.current_token.line_number}")
                return False

            # Move to the next token to get the loop type (TIL/WILE)
            self.advance_to_next_token()

            # Check loop type (TIL/WILE)
            if self.current_token.value in ('TIL', 'WILE'):
                loop_type = self.current_token.value
                print("Loop type: ", loop_type)
                self.advance_to_next_token()  # Consume TIL/WILE

                loop_startline = self.current_line_number
                loop_startposition = self.current_position
                print(loop_startposition)
                print("LOOP START: ", loop_startline)
                print("DEBUG TOKEN", self.current_token.value)

                while True:
                    print("DEBUG TOKEN", self.current_token.value)
                    # Evaluate the loop condition expression
                    self.analyze_operation(self.current_token.value)

                    # Get the condition value from IT
                    condition_value = self.symbol_table['IT']['value']
                    print(f"IT value inside the nerfin loop: {condition_value}")

                    self.advance_to_next_line()
                    # Check if the loop should continue based on loop type and condition value
                    if (loop_type == 'TIL' and condition_value != 'FAIL') or (loop_type == 'WILE' and condition_value != 'WIN'):
                        print("HELLO")
                        break  # Exit the loop

                    # Execute the loop body
                    self.analyze_line()
                    print("Condition still met, continuing loop...")

                    # Update the loop variable (decrement for NERFIN)
                    try:
                        current_value = self.symbol_table[loop_variable]['value']
                        print(f"Current value of {loop_variable}: {current_value}")

                        # Decrement the value
                        new_value = int(current_value) - 1
                        print(f"New value of {loop_variable}: {new_value}")

                        # Update the value in the symbol table
                        self.symbol_table[loop_variable]['value'] = new_value

                    except KeyError:
                        print(f"Error: Variable {loop_variable} not found.")
                        return False
                    except ValueError:
                        self.log_semantic_error(f"Cannot decrement non-numeric variable '{loop_variable}'", context=f"Line {self.current_token.line_number}")
                        return False

                    # Go back to the start of the loop
                    self.current_line_number = loop_startline
                    self.current_tokens = self.lines[self.current_line_number]
                    self.current_position = loop_startposition
                    self.current_token = self.current_tokens[self.current_position]

                    if self.current_token.value == 'IM OUTTA YR':
                        self.advance_to_next_token()  # Consume 'IM OUTTA YR'
                        break  # Exit the loop

                    # self.advance_to_next_token()  # Move to the next token
            else:
                self.log_semantic_error(f"Expected 'TIL' or 'WILE' after loop variable '{loop_variable}'", context=f"Line {self.current_token.line_number}")
                return False
 
    def uppin_loop(self):
        # After getting loop type
        # R used to assign a value to an already created data type

        print("Before consuming nerfin current token value: ", self.current_token.value) # consume NERFIN

        # Right after nerfin is YR
        if self.current_token.value == 'YR':
            self.advance_to_next_token()  # consume YR
    
            # Get the loop variable
            loop_variable = self.current_token.value
            print("Loop condition Variable: ", loop_variable)

            # Ensure the loop variable exists
            if loop_variable not in self.symbol_table:
                self.log_semantic_error(f"Variable '{loop_variable}' used before declaration", context=f"Line {self.current_token.line_number}")
                return False

            # Move to the next token to get the loop type (TIL/WILE)
            self.advance_to_next_token()

            # Check loop type (TIL/WILE)
            if self.current_token.value in ('TIL', 'WILE'):
                loop_type = self.current_token.value
                print("Loop type: ", loop_type)
                self.advance_to_next_token()  # Consume TIL/WILE

                loop_startline = self.current_line_number
                loop_startposition = self.current_position
                print(loop_startposition)
                print("LOOP START: ", loop_startline)
                print("DEBUG TOKEN", self.current_token.value)

                while True:
                    print("DEBUG TOKEN", self.current_token.value)
                    # Evaluate the loop condition expression
                    self.analyze_operation(self.current_token.value)
                    

                    # Get the condition value from IT
                    condition_value = self.symbol_table['IT']['value']
                    print(f"IT value inside the nerfin loop: {condition_value}")


                    self.advance_to_next_line()
                    # Check if the loop should continue based on loop type and condition value
                    if (loop_type == 'TIL' and condition_value != 'FAIL') or (loop_type == 'WILE' and condition_value != 'WIN'):
                        print("HELLO")
                        break  # Exit the loop

                    # Execute the loop body
                    self.analyze_line()
                    print("Condition still met, continuing loop...")

                    # Update the loop variable (INCREMENT FOR UPPIN)
                    try:
                        current_value = self.symbol_table[loop_variable]['value']
                        print(f"Current value of {loop_variable}: {current_value}")

                        # Increment the value
                        new_value = int(current_value) + 1
                        print(f"New value of {loop_variable}: {new_value}")

                        # Update the value in the symbol table
                        self.symbol_table[loop_variable]['value'] = new_value

                    except KeyError:
                        print(f"Error: Variable {loop_variable} not found.")
                        return False
                    except ValueError:
                        self.log_semantic_error(f"Cannot decrement non-numeric variable '{loop_variable}'", context=f"Line {self.current_token.line_number}")
                        return False

                    # Go back to the start of the loop
                    self.current_line_number = loop_startline
                    self.current_tokens = self.lines[self.current_line_number]
                    self.current_position = loop_startposition
                    self.current_token = self.current_tokens[self.current_position]

                    if self.current_token.value == 'IM OUTTA YR':
                        self.advance_to_next_token()  # Consume 'IM OUTTA YR'
                        break  # Exit the loop

                    # self.advance_to_next_token()  # Move to the next token
            else:
                self.log_semantic_error(f"Expected 'TIL' or 'WILE' after loop variable '{loop_variable}'", context=f"Line {self.current_token.line_number}")
                return False

    def analyze_function_declaration(self):
        print("Analyzing function declaration")

        if self.current_token and self.current_token.value == "HOW IZ I":  # Function must start with 'HOW IZ I'
            self.advance_to_next_token()  # Consume 'HOW IZ I'

            function_name = self.current_token.value  # Save the function name for later verification
            self.advance_to_next_token()  # Consume the function name

            # List to store parameters for later checks
            parameters = []
            function_body_start = None

            # Consume the first 'YR'
            self.advance_to_next_token()

            # Store the function actual parameters
            while self.current_token:
                # Check if there are more parameters
                if self.current_token.value == "AN":
                    self.advance_to_next_token()  # Consume 'AN

                    if self.current_token.value == "YR":
                        self.advance_to_next_token()  # Consume 'YR'

                # If a variable identifier is found, 
                elif self.current_token.type == "Variable Identifier":
                    # Store the parameter name
                    parameter_name = self.current_token.value
                    parameters.append(parameter_name)

                    # And add it to the symbol table with a default value of 'NOOB'
                    self.symbol_table[parameter_name] = {
                        'value': 'NOOB',
                        'type': 'NOOB'
                    }
                    self.advance_to_next_token()

                else:
                    self.log_semantic_error(
                        "Expected parameter name after 'YR'",
                        # found=self.current_token.value if self.current_token else "None"
                    )
                    return

            self.advance_to_next_line()  # Move to the next line

            # Save the position of the function body for later execution
            function_body_start = self.current_line_number

            # Store function information in a dictionary keyed by function name
            if not hasattr(self, 'functions'):
                self.functions = {}
            
            self.functions[function_name] = {
                "name": function_name,
                "parameters": parameters,
                "function_body_start": function_body_start
            }

            print(f"Stored function '{function_name}' with parameters {parameters} and body starting at line {function_body_start}")

            # keep skipping lines until we find the end of the function (IF U SAY SO)
            while self.current_token and self.current_token.value != "IF U SAY SO":
                self.advance_to_next_line()

            # consume 'IF U SAY SO'
            self.advance_to_next_token()

            return True

    def execute_function_body(self, function_info, arguments, function_call_start):
        # print(arguments) # arguments are the values of the parameters in the call
        # print(function_info) # function name

        # print('Function Info: ', function_info)
        # print("ARGUMENTS: ",arguments) # arguments are the values of the parameters in the call

        # arg_value = []

        # use zip to map the value of the formal parameters to the actual parameters
        for actual_param, formal_param in zip(function_info['parameters'], arguments):
            print("FORMAL PARAM: ", formal_param)
            print("ACTUAL PARAM: ", actual_param)

            # check if the formal parameter is a literal (meaning that its value is stored in 'IT)
            if TypeCaster.type_check(formal_param) in ['NUMBR', 'NUMBAR', 'TROOF']:
                print("FORMAL PARAM IS A LITERAL OF TYPE", TypeCaster.type_check(formal_param))
                self.symbol_table[actual_param] = {
                    'value': formal_param,
                    'type': self.symbol_table['IT']['type']
                }
            else:
                self.symbol_table[actual_param] = {
                    'value': self.symbol_table[formal_param]['value'],
                    'type': self.symbol_table[formal_param]['type']
                }

        print("SYMBOL TABLE AFTER FUNCTION CALL")
        self.print_symbol_table()
        
        # PARA BUMALIK
        # access the token at the start of the function body
        self.current_line_number = function_info['function_body_start']
        self.current_tokens = self.lines[self.current_line_number]
        self.current_position = 0
        self.current_token = self.current_tokens[self.current_position]
        # print("Current token after function call: ", self.current_token.value)
        
        # Execute the function body
        while self.current_token:
            # flag to check if has return or not
            has_return = False

            # if function body has a return value
            if self.current_token.value == "FOUND YR":
                print("Found 'FOUND YR'")
                has_return = True
                self.advance_to_next_token()  # Consume 'FOUND YR'
                print("Current token after consume found yr: ", self.current_token.value)
                if (self.current_token.type == 'Variable Identifier'):
                    self.advance_to_next_token()
                else:
                    self.analyze_line() # Execute the return statement
                    
                print(f"Return statement value: ", self.symbol_table['IT']['value'])

                while self.current_token and self.current_token.value != "IF U SAY SO":
                    self.advance_to_next_line()

                    if self.current_token and self.current_token.value == "IF U SAY SO":
                        break

            # else, function body has no return value
            elif not has_return:
                print("No 'FOUND YR' found (function has no return value)")
                while self.current_token and self.current_token.value != "GTFO":
                    self.analyze_line()
                    self.advance_to_next_line()
                    
                    if self.current_token and self.current_token.value == "GTFO":
                        print("Found 'GTFO'")
                        self.symbol_table['IT'] = {
                        'value': 'NOOB',
                        'type': 'NOOB'
                        }
                        break
            
            self.current_line_number = function_call_start + 1
            self.current_tokens = self.lines[self.current_line_number]
            self.current_position = 0
            self.current_token = self.current_tokens[self.current_position]
            self.analyze_line()

            # print("Current token after function call check: ", self.current_token.value)

            return True
                
        #     # print('DEBUG TOKEN: ', self.current_token.value)
                
    def analyze_function_call(self):
        print("Analyzing function call")
        self.advance_to_next_token()  # Consume 'I IZ'
        print("Current token value: ", self.current_token.value)

        # Ensure function has a valid name
        if not self.current_token or self.current_token.type != "Variable Identifier":
            self.log_semantic_error(
                "Expected function name after 'I IZ'",
                # found=self.current_token.value if self.current_token else "None"
            )
            return None, []

        function_name = self.current_token.value  # Save the function name
        self.advance_to_next_token()  # Consume the function name

        arguments = []

        # Parse arguments if any
        while self.current_token and self.current_token.value == "YR":
            self.advance_to_next_token()  # Consume 'YR'
            if not self.current_token:
                self.log_semantic_error(
                    "Expected argument after 'YR'",
                    # found="None"
                )
                return function_name, arguments

            if self.current_token.type == "Variable Identifier":
                argument_name = self.current_token.value
                arguments.append(argument_name)
                self.advance_to_next_token()  # Consume the argument name
            # handle parameters that are operations
            elif self.current_token.type in ['Arithmetic Operation', 'Boolean Operation', 'Comparison Operation']:
                # Assuming analyze_operation returns a string representation of the result
                result = self.analyze_operation(self.current_token.value)
                if result is not None:
                    arguments.append(result)

                    # Store in implicit variable 'IT'
                    self.symbol_table['IT'] = {
                        'value': result,
                        'type': TypeCaster.type_check(result)
                    }
                else:
                    self.log_semantic_error(
                        "Expected valid operation after 'YR'",
                        # found=self.current_token.value
                    )
                    return function_name, arguments
            else:
                # Handle the case where we need to calculate the parameter
                result = self.analyze_line()
                print(f"Result of operation: {result}")
                if result is not None:
                    arguments.append(result)
                else:
                    self.log_semantic_error(
                        "Expected valid operation after 'YR'",
                        # found=self.current_token.value
                    )
                    return function_name, arguments

            if self.current_token and self.current_token.value == "AN":
                self.advance_to_next_token()  # Consume 'AN'

        return function_name, arguments