class SyntaxAnalyzer:
    # constructor to initialize the syntax analyzer
    def __init__(self, tokens, log_function=None):
        self.lines = self._organize_tokens_by_line(tokens) # organize tokens by line number
        self.current_line_number = min(self.lines.keys()) if self.lines else None # current line number being processed
        self.current_tokens = self.lines[self.current_line_number] if self.lines else [] # list of tokens from the current line
        self.current_position = 0 # current index of the token being processed
        self.current_token = self.current_tokens[0] if self.current_tokens else None # current token being processed
        self.error_messages = [] # list of error messages
        self.log_function = log_function # function to log error messages to the GUI
        self.variables = { "IT": { "value": None, "type": None } } # dictionary to store variables and their values
        self.operations = [] # list to store operations
        self.in_wazzup_block = False # flag to indicate if the program is inside a 'WAZZUP' block
        self.inside_switch_block = False  # Entering the switch block
    
    # function to organize tokens by line number, excluding comments
    def _organize_tokens_by_line(self, tokens):
        lines = {}
        for token in tokens:
            if token.type != "Comment Line": # skip comments
                if token.line_number not in lines:
                    lines[token.line_number] = []
                lines[token.line_number].append(token)
        return lines

    # function to log syntax errors with context
    def log_syntax_error(self, message, expected=None, found=None):
        if expected and found:
            error_message = (
                f"Syntax Error: {message}. Expected '{expected}', but found '{found}' "
                f"(line {self.current_line_number})"
            )
        elif expected:
            error_message = (
                f"Syntax Error: {message}. Expected '{expected}' "
                f"(line {self.current_line_number})"
            )
        else:
            error_message = f"Syntax Error: {message} (line {self.current_line_number})"

        self.error_messages.append(error_message)
        if self.log_function:
            self.log_function(error_message)
        print(f"{error_message}") # for debugging

    # function to print the variables and their values
    def print_variables(self):
        print("\nVariables:")
        for identifier, identifier_info in self.variables.items():
            value = identifier_info.get("value", "undefined")
            type = identifier_info.get("type", "unknown")
            print(f"Identifier: {identifier}, Value: {value}, Type: {type}")

    # function to parse a single line
    def parse_line(self):
        #inside_switch_block = False  # Track whether we're inside a WTF? block
        
        print(f"\nParsing line {self.current_line_number}: {self.current_tokens}")
        
        while self.current_token:  # While there are tokens in the current line
            if self.current_token.value == 'WAZZUP':  
                self.in_wazzup_block = True
                print("Entered 'WAZZUP' block")
            elif self.current_token.value == 'BUHBYE' and self.in_wazzup_block:  
                self.in_wazzup_block = False
                print("Exited 'WAZZUP' block")
            elif self.in_wazzup_block and self.current_token.value == 'I HAS A':  
                self.parse_variable_declaration()
            elif self.current_token.type == 'Output Keyword':  
                self.parse_print()
            elif self.current_token.type == 'Input Keyword':  
                self.parse_input()
            elif self.current_token.value == 'O RLY?':  
                self.parse_conditional()
            elif self.current_token.value == 'IM IN YR':  
                self.parse_loop()
            elif self.current_token.value == 'HOW IZ I':
                self.parse_function()
            elif self.current_token.value == 'I IZ':
                self.parse_functioncall()
            elif self.current_token.value == 'WTF?':  
                self.parse_switch()
                print(f"Entering WTF? block at line {self.current_line_number}")
            
            # # Check for 'OIC' token and mark exiting the switch block
            # elif self.current_token.value == 'OIC':  
            #     inside_switch_block = False  # Exiting the switch block
            #     print(f"Exiting WTF? block at line {self.current_line_number}")
            
            # Check for 'OMG' and 'OMGWTF' outside of a 'WTF?' block
            elif self.current_token.value == 'OMG' or self.current_token.value == 'OMGWTF':
                if not self.inside_switch_block:  # Error if OMG/OMGWTF appears before 'WTF?'
                    self.log_syntax_error(f"Found '{self.current_token.value}' without preceding 'WTF?'", 
                                        found=self.current_token.value)
                    return {"error": f"Invalid token '{self.current_token.value}' at line {self.current_line_number}"}  # Stop processing and return an error
                # else:
                #     continue  # Skip processing OMG/OMGWTF if inside a 'WTF?' block

            elif self.current_token.type == 'Variable Identifier':
                next_token = self.current_tokens[self.current_position + 1] if self.current_position + 1 < len(self.current_tokens) else None
                if next_token and next_token.type == 'Variable Assignment':  
                    self.parse_assignment()
                elif next_token and next_token.type == 'Typecasting Operation':  
                    self.parse_typecasting()
                
            self.advance_to_next_token()  # Move to the next token

    # function to advance to the next line
    def advance_to_next_line(self):
        if self.current_line_number is None:  # Check if already at the end
            self.current_tokens = []
            self.current_token = None
            return   # Don't try to advance further

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
            self.current_line_number = None  # Indicate end of lines

        # print(f"DEBUG: Current token after advancing: {self.current_token.value if self.current_token else 'None'}")

    # function to advance to the next token
    def advance_to_next_token(self):
        #  #Debug: Before advancing
        # print(f"DEBUG: Current token before advancing: {self.current_token.value if self.current_token else 'None'}")

        if self.current_position < len(self.current_tokens) - 1: # if there are more tokens in the current line
            self.current_position += 1 # move to the next token
            self.current_token = self.current_tokens[self.current_position]  # update current token
        else:
            # print("DEBUG: End of line reached, advancing to the next line.")
            self.current_token = None

        # # Debug: After advancing
        # print(f"DEBUG: Current token after advancing: {self.current_token.value if self.current_token else 'None'}")

    # function to parse the code (entry point of the syntax analyzer)
    def parse_program(self):
        print("\nSYNTAX ANALYSIS")
        
        if self.current_token and self.current_token.value == "HAI":
            print("\nProgram starts with 'HAI'")
            self.advance_to_next_line()

            while self.current_line_number is not None and self.current_token:
                if self.current_token.value == "KTHXBYE":
                    break

                self.parse_line()

                # Check for the specific error immediately after parsing the line
                if self.error_messages and self.error_messages[-1].startswith("Syntax Error: Function must end with 'IF U SAY SO'"):
                    print("Found 'Function must end with IF U SAY SO' error. Stopping further parsing.")
                    break  # Exit the loop in parse_program()

                self.advance_to_next_line()

            if self.current_token and self.current_token.value == "KTHXBYE":
                print("\nProgram ends with 'KTHXBYE'")
            elif not self.error_messages:  # Only log this error if there are no other errors
                self.log_syntax_error("Program must end with 'KTHXBYE'")
        else:
            self.log_syntax_error("Program must start with 'HAI'")

        return self.error_messages
    
    # function to parse a variable declaration
    def parse_variable_declaration(self):
        self.advance_to_next_token() # consume 'I HAS A'

        # check for missing variable name
        if not self.current_token or self.current_token.type != 'Variable Identifier':
            self.log_syntax_error("Variable name is missing or invalid after 'I HAS A'")
            return
        
        variable_name = self.current_token.value # store variable name
        self.advance_to_next_token() # consume the variable name

        if self.current_token and self.current_token.value == "ITZ": # if variable is initialized
            self.advance_to_next_token()  # consume 'ITZ'

            # check if there is a valid expression after 'ITZ'
            if not self.current_token:
                self.log_syntax_error(f"Missing expression to initialize variable '{variable_name}' after 'ITZ'")
                return

            # handle different types of initialization
            if self.current_token.type == 'String Delimiter':
                data_type = 'YARN'
            elif self.current_token.type in ['Arithmetic Operation', 'Boolean Operation', 'Comparison Operation', 'String Concatenation', 'Typecasting Operation']:
                data_type = None
            else:
                data_type = self.current_token.type.split()[0]
            
            value = self.parse_expression() # parsing the value expression

            # save the variable in the symbol table
            self.variables[variable_name] = {
                "value": value,
                "type": data_type
            }
            print(f"Declared variable {variable_name} initialized to {value} with type {data_type}")

        else: # if variable is uninitialized   
            if self.current_token and self.current_token.value != 'ITZ':
                self.log_syntax_error("Expected 'ITZ' after variable name for initialization", found=self.current_token.value)
                return
            
            self.variables[variable_name] = {
                "value": "NOOB",
                "type": "NOOB"
            }
            print(f"Declared uninitialized variable {variable_name} (default value: None, type: NOOB)")

    # function to parse an expression
    def parse_expression(self):
        if self.current_token.type in ['NUMBR Literal', 'NUMBAR Literal', 'TROOF Literal']: # literal
            result = self.current_token.value
            self.advance_to_next_token()
            return result
        elif self.current_token.type == 'String Delimiter': # string
            return self.parse_string()
        elif self.current_token.type == 'Variable Identifier': # variable
            if self.current_token.value in self.variables:
                result = self.variables[self.current_token.value]
                self.advance_to_next_token()
                return result
        elif self.current_token.type in ['Arithmetic Operation', 'Boolean Operation', 'Comparison Operation']: # operation
            return self.parse_operation()
        else:
            self.log_syntax_error("Expected literal or operation")
            return None
    
    # function to evaluate an expression
    def parse_operation(self):
        operation = self.current_token.value
        self.advance_to_next_token() # consume the operation keyword

        if operation == 'NOT': # unary operations
            return self.parse_unary_operation(operation)
        elif operation in ['SUM OF', 'DIFF OF', 'PRODUKT OF', 'QUOSHUNT OF', 'MOD OF', 'BIGGR OF', 'SMALLR OF']: # binary arithmetic
            return self.parse_binary_operation(operation)
        elif operation in ['ALL OF', 'ANY OF']: # infinite-arity boolean
            return self.parse_infinite_arity_operation(operation)
        elif operation in ['BOTH OF', 'EITHER OF', 'WON OF', 'BOTH SAEM', 'DIFFRINT']: # binary boolean
            return self.parse_binary_operation(operation)
        elif operation == 'SMOOSH': # string concatenation
            return self.parse_concatenation()
        else: # unknown operation
            self.log_syntax_error("Unknown operation", found=operation)
            return f"Unknown operation '{operation}'"
    
    # function to parse unary operations (NOT)
    def parse_unary_operation(self, operation):
        operands = []
        
        if not self.current_token:
            self.log_syntax_error("Expected operand for 'NOT'")
            return f"{operation} Missing Operand"
        
        if self.current_token.type in ['TROOF Literal', 'Variable Identifier']: # expect one operand
            operands.append(self.current_token.value)
            self.advance_to_next_token() # consume operand
        elif self.current_token.type in ['Arithmetic Operation', 'Boolean Operation', 'Comparison Operation']: # nested operation
            operands.append(self.parse_operation())
        else:
            self.log_syntax_error("Expected TROOF, variable, or operation for 'NOT'", found=self.current_token.type if self.current_token else "None")

        print(f"Will evaluate '{operation} {operands[0]}'")
        return f"{operation} {operands[0]}" if operands else f"{operation} Missing Operand"
    
    # function to parse binary operations (arithmetic, boolean, comparison)
    def parse_binary_operation(self, operation):
        # helper function to parse a single operand
        def parse_single_operand():
            if not self.current_token:
                self.log_syntax_error(f"Missing operand for '{operation}'")
                return None
            
            if self.current_token.type in ['NUMBR Literal', 'NUMBAR Literal', 'TROOF Literal', 'Variable Identifier']:
                operand = self.current_token.value
                self.advance_to_next_token()
                return operand
            elif self.current_token.type == 'String Delimiter':
                return self.parse_string()
            elif self.current_token.type in ['Arithmetic Operation', 'Boolean Operation', 'Comparison Operation']:
                return self.parse_operation()
            else:
                self.log_syntax_error(f"Expected operand for '{operation}'",found=self.current_token.type if self.current_token else "None"
                )
                return None

        # parse the first operand
        first_operand = parse_single_operand()
        if first_operand is None:
            return f"{operation} Missing First Operand"

        # check for 'AN'
        if not self.current_token or self.current_token.value != 'AN':
            self.log_syntax_error(f"Missing 'AN' after first operand in '{operation}'")
            return f"{operation} {first_operand} Missing AN"
        
        # consume 'AN'
        self.advance_to_next_token()

        # parse the second operand
        second_operand = parse_single_operand()
        if second_operand is None:
            return f"{operation} {first_operand} AN Missing Second Operand"

        print(f"Will evaluate '{operation} {first_operand} AN {second_operand}'")
        return f"{operation} {first_operand} AN {second_operand}"

    # function to parse infinite-arity operations (ALL OF/ANY OF)
    def parse_infinite_arity_operation(self, operation):
        operands = []
        
        # check if there are any tokens after the operation
        if not self.current_token:
            self.log_syntax_error(f"Missing operands for '{operation}'")
            return f"{operation} Missing Operands"
        
        # flag to track if we've seen the first operand
        first_operand_parsed = False
        
        while self.current_token and self.current_token.value != 'MKAY':
            # handle 'AN' token
            if self.current_token.value == 'AN':
                # 'AN' should not be the first token after operation
                if not first_operand_parsed:
                    self.log_syntax_error(f"Unexpected 'AN' at the start of {operation}")
                    return f"{operation} Invalid Start with AN"
                
                # consume 'AN'
                self.advance_to_next_token()
                
                # 'AN' should be followed by an operand
                if not self.current_token:
                    self.log_syntax_error(f"Missing operand after 'AN' in {operation}")
                    return f"{operation} {' AN '.join(operands)} AN Missing Operand"
            
            # parse operand
            if self.current_token.type in ['TROOF Literal', 'NUMBR Literal', 'NUMBAR Literal', 'Variable Identifier']:
                operands.append(self.current_token.value)
                first_operand_parsed = True
                self.advance_to_next_token()
            elif self.current_token.type in ['Arithmetic Operation', 'Boolean Operation', 'Comparison Operation']:
                operand = self.parse_operation()
                operands.append(operand)
                first_operand_parsed = True
            elif self.current_token.type == 'String Delimiter':
                operands.append(self.parse_string())
                first_operand_parsed = True
            else:
                # unexpected token type
                self.log_syntax_error(f"Unexpected token in {operation}", found=self.current_token.type if self.current_token else "None")
                return f"{operation} {' AN '.join(operands)} Unexpected Token"
        
            # Check if there are more operands and 'AN' is expected
            if self.current_token and self.current_token.value not in ['AN', 'MKAY']:
                if operands:
                    self.log_syntax_error(f"Missing 'AN' between operands in {operation}")
                    return f"{operation} {' AN '.join(operands)} Missing 'AN'"
        
        # check for 'MKAY'
        if not self.current_token or self.current_token.value != 'MKAY':
            self.log_syntax_error(f"Missing 'MKAY' at the end of {operation}")
            return f"{operation} {' AN '.join(operands)} Missing MKAY"
        
        # consume 'MKAY'
        self.advance_to_next_token()
        
        # check for any tokens after 'MKAY'
        if self.current_token:
            self.log_syntax_error(f"Unexpected tokens after 'MKAY' in {operation}")
            return f"{operation} {' AN '.join(operands)} MKAY Extra Tokens"
        
        # if no operands were parsed
        if not operands:
            self.log_syntax_error(f"No operands provided for {operation}")
            return f"{operation} Missing Operands"
        
        print(f"Will evaluate '{operation} {' AN '.join(operands)} MKAY'")
        return f"{operation} {' AN '.join(operands)} MKAY"

    # function to parse a string
    def parse_string(self):
        self.advance_to_next_token() # consume opening delimiter

        if self.current_token and self.current_token.type == 'Literal': # check if contains string content
            string_content = self.current_token.value
            self.advance_to_next_token() # consume string content

            if self.current_token and self.current_token.type == 'String Delimiter': # check for closing delimiter
                self.advance_to_next_token() # consume closing delimiter
                return string_content
            else:
                self.log_syntax_error("Expected closing string delimiter", found=self.current_token.value if self.current_token else 'None')
                return None
        else:
            self.log_syntax_error("Expected string literal", found=self.current_token.value if self.current_token else 'None')
            return None
    
    # function to parse a print statement
    def parse_print(self):
        output = []
        self.advance_to_next_token() # consume 'VISIBLE'
        
         # check if there are any tokens after VISIBLE
        if not self.current_token:
            self.log_syntax_error("No output specified after VISIBLE")
            return "VISIBLE Missing Output"

        while self.current_token:
            if self.current_token.type in ['NUMBR Literal', 'NUMBAR Literal', 'TROOF Literal', 'Variable Identifier']: # literal or variable
                output.append(str(self.current_token.value))
                self.advance_to_next_token()
            elif self.current_token.type == 'String Delimiter': # string
                output.append(self.parse_string())
            elif self.current_token.type in ['Arithmetic Operation', 'Boolean Operation', 'Comparison Operation']: # operation
                output.append(self.parse_operation())
            elif self.current_token.type == 'String Concatenation': # concatenation
                output.append(self.parse_concatenation())
            elif self.current_token.type in ['Parameter Delimiter', 'Output Separator']: # if there are more operands
                self.advance_to_next_token() # consume 'AN' or '+'
            elif self.current_token.type == 'Suppress Newline': # suppress newline
                self.advance_to_next_token() # consume '!'
            else:
                self.log_syntax_error("Unexpected token in VISIBLE", found=self.current_token.type)
                break

        print('Will print "' + ''.join(output) + '"')

    # function to parse a user input statement
    def parse_input(self):
        self.advance_to_next_token()  # consume 'GIMMEH'

        # check if there's a token after GIMMEH
        if not self.current_token:
            self.log_syntax_error("Missing variable identifier after GIMMEH")
            return "GIMMEH Missing Variable"

        # store variable name
        variable_name = self.current_token.value
        
        # consume variable name
        self.advance_to_next_token()

        # check for unexpected tokens after variable name
        if self.current_token:
            self.log_syntax_error("Unexpected tokens after variable identifier", found=self.current_token.type)

        print(f"Will store user input in variable {variable_name}")
        return variable_name
        
    # function to parse a string concatenation
    def parse_concatenation(self):
        operands = []
        self.advance_to_next_token() # consume 'SMOOSH'

        first_operand_parsed = False
        
        while self.current_token:
            if first_operand_parsed and self.current_token.value != 'AN':
                self.log_syntax_error("Expected 'AN' between operands in SMOOSH", found=self.current_token.value)
                return f"SMOOSH {' + '.join(operands)} Missing AN"
            
            # handle 'AN' token
            if self.current_token.value == 'AN':
                # 'AN' should not be the first token
                if not first_operand_parsed:
                    self.log_syntax_error("Unexpected 'AN' at the start of SMOOSH")
                    return "SMOOSH Invalid Start with AN"
                
                # consume 'AN'
                self.advance_to_next_token()
                
                # 'AN' should be followed by an operand
                if not self.current_token:
                    self.log_syntax_error("Missing operand after 'AN' in SMOOSH")
                    return f"SMOOSH {' + '.join(operands)} AN Missing Operand"

            # parse operand
            if self.current_token.type in ['NUMBR Literal', 'NUMBAR Literal', 'TROOF Literal', 'Variable Identifier']:
                if self.current_token.type == 'Variable Identifier' and self.current_token.value in self.variables:
                    operands.append(str(self.variables[self.current_token.value]['value']))
                else:
                    operands.append(str(self.current_token.value))
                first_operand_parsed = True
                self.advance_to_next_token()
            elif self.current_token.type == 'String Delimiter':
                string_output = self.parse_string()
                if isinstance(string_output, str) and not string_output.startswith("YARN"):
                    operands.append(string_output)
                    first_operand_parsed = True
                else:
                    return string_output
            elif self.current_token.type in ['Arithmetic Operation', 'Boolean Operation', 'Comparison Operation']:
                operation_output = self.parse_operation()
                operands.append(operation_output)
                first_operand_parsed = True
            else:
                # unexpected token type
                self.log_syntax_error("Unexpected token in SMOOSH", found=self.current_token.type)
                return f"SMOOSH {' + '.join(operands)} Unexpected Token"
        
        # if no operands were parsed
        if not operands:
            self.log_syntax_error("No operands specified after SMOOSH")
            return "SMOOSH Missing Operands"
        elif len(operands) == 1:
            self.log_syntax_error("Only one operand specified after SMOOSH, requires at least two")
            return f"SMOOSH {' + '.join(operands)} Missing AN"

        return f"{' + '.join(operands)}"
    
    # function to parse an assignment statement
    def parse_assignment(self):
        # check if there's a variable name
        if not self.current_token or self.current_token.type != 'Variable Identifier':
            self.log_syntax_error("Invalid variable name for assignment", found=self.current_token.type if self.current_token else "None")
            return "Assignment Missing Variable"
        
        variable_name = self.current_token.value 
        self.advance_to_next_token() # consume the variable identifier

        # check for assignment operator
        if not self.current_token or self.current_token.value != "R":
            self.log_syntax_error("Expected assignment operator 'R'", found=self.current_token.value if self.current_token else "None")
            return f"{variable_name} Missing Assignment Operator"
        
        self.advance_to_next_token() # consume 'R'

        # check if there's a value to assign
        if not self.current_token:
            self.log_syntax_error("Missing value after assignment operator", found="None")
            return f"{variable_name} R Missing Value"

        # parse different types of assignment values
        if self.current_token.type in ['NUMBR Literal', 'NUMBAR Literal', 'TROOF Literal']:
            value = self.current_token.value
            self.advance_to_next_token() # consume the literal
            print(f"Assigned literal value '{value}' to variable {variable_name}")
            return f"{variable_name} R {value}"
        
        elif self.current_token.type == 'String Delimiter':
            value = self.parse_string()
            print(f"Assigned string '{value}' to variable {variable_name}")
            return f"{variable_name} R {value}"
        
        elif self.current_token.type == 'Variable Identifier':
            value = self.current_token.value
            self.advance_to_next_token() # consume the variable
            print(f"Assigned value of variable {value} to variable {variable_name}")
            return f"{variable_name} R {value}"
        
        elif self.current_token.type in ['Arithmetic Operation', 'Boolean Operation', 'Comparison Operation']:
            value = self.parse_operation()
            print(f"Assigned result of operation {value} to variable {variable_name}")
            return f"{variable_name} R {value}"
        
        elif self.current_token.type == 'String Concatenation':
            value = self.parse_concatenation()
            print(f"Assigned concatenated string '{value}' to variable {variable_name}")
            return f"{variable_name} R {value}"
        
        elif self.current_token.type == 'Typecasting Operation':
            value = self.parse_typecasting()
            print(f"Assigned typecasted value '{value}' to variable {variable_name}")
            return f"{variable_name} R {value}"
        
        else:
            # unexpected token type for assignment
            self.log_syntax_error("Invalid value for assignment", found=self.current_token.type)
            return f"{variable_name} R Invalid Value: {self.current_token.type}"

    # function to parse a typecasting statement
    def parse_typecasting(self):
        if self.current_token.value == 'MAEK A':
            self.advance_to_next_token() # consume 'MAEK A'

            if self.current_token and self.current_token.type in ['Variable Identifier', 'NUMBR Literal', 'NUMBAR Literal', 'TROOF Literal']:
                cast_value = self.current_token.value
                self.advance_to_next_token() # consume the value to cast
                
                if self.current_token and self.current_token.type == 'Type Literal':
                    target_type = self.current_token.value
                    self.advance_to_next_token() # consume the type literal
                    print(f"Casting value of {cast_value} to type '{target_type}'")

                    return f"MAEK A {cast_value} {target_type}"
                else:
                    self.log_syntax_error("Expected type literal after value in 'MAEK A' operation", found=self.current_token.type if self.current_token else "None")
                    return "MAEK A Missing Type Literal"
            else:
                self.log_syntax_error("Expected value to cast in 'MAEK A' operation", found=self.current_token.type if self.current_token else "None")    
                return "MAEK A Missing Value"
                
        self.advance_to_next_token() # consume variable identifier

        if self.current_token.value == 'IS NOW A':
            cast_value = self.current_tokens[self.current_position - 1].value
            self.advance_to_next_token() # consume 'IS NOW A'

            if self.current_token and self.current_token.type == 'Type Literal':
                target_type = self.current_token.value
                self.advance_to_next_token() # consume the type literal
                print(f"Casting value of {cast_value} to type {target_type}")
            
                return f"IS NOW A {target_type}"
            else:
                self.log_syntax_error("Expected type literal after 'IS NOW A'", found=self.current_token.type if self.current_token else "None")
                return "IS NOW A Missing Type Literal"
        else:
            self.log_syntax_error("Expected 'MAEK' or 'IS NOW A' for typecasting", found=self.current_token.value if self.current_token else "None")
            return "Typecasting Missing Operator"
            
    #conditional ststament
    '''
    works like
    O RLY?
        ya rly start of if clause
            if code
        NO WAI start of else clause
            else code
    OIC
    '''
    
    #function to parse conditional statements (O RLY?)
    def parse_conditional(self):
        # Preliminary check for 'YA RLY' without a preceding 'O RLY?'
        has_o_rly = False
        for line_number, tokens in self.lines.items():
            for token in tokens:
                if token.value == "O RLY?":
                    has_o_rly = True
                elif token.value == "YA RLY" and not has_o_rly:
                    self.log_syntax_error("Found 'YA RLY' without preceding 'O RLY?'", found="YA RLY without O RLY?")

        if self.current_token.value == "O RLY?":
            print("Parsing conditional 'O RLY?'")
            self.advance_to_next_token()  # Consume 'O RLY?'

            # Ensure 'YA RLY' follows, possibly on the next line
            while not self.current_token and self.current_line_number is not None:
                self.advance_to_next_line()  # Move to the next line if no token is found on the current line

            # Debugging: Output current token
            if self.current_token:
                print(f"DEBUG: Token after 'O RLY?': {self.current_token.value}, Type: {self.current_token.type}")
            else:
                print("DEBUG: No token found after 'O RLY?'")

            # Ensure 'YA RLY' follows
            if self.current_token and self.current_token.value == "YA RLY":
                print("Found 'YA RLY', parsing <if code block>")
                self.advance_to_next_line()  # Consume 'YA RLY'

                # Parse <if code block> until 'NO WAI' or 'OIC'
                while self.current_token and self.current_token.value not in ["NO WAI", "OIC"]:
                    self.parse_line()
                    self.advance_to_next_line()

                # Handle the 'NO WAI' block
                if self.current_token and self.current_token.value == "NO WAI":
                    print("Found 'NO WAI', parsing <else code block>")
                    self.advance_to_next_line()  # Consume 'NO WAI'

                    # Parse <else code block> until 'OIC'
                    while self.current_token and self.current_token.value != "OIC":
                        self.parse_line()
                        self.advance_to_next_line()

                # Ensure 'OIC' ends the construct
                if self.current_token and self.current_token.value == "OIC":
                    print("Found 'OIC', end of conditional block")
                    self.advance_to_next_token()  # Consume 'OIC'
                else:
                    self.log_syntax_error("Expected 'OIC' to close 'O RLY?' block", found=self.current_token.value if self.current_token else "None")
            else:
                self.log_syntax_error("Expected 'YA RLY' after 'O RLY?'", found=self.current_token.value if self.current_token else "None")
        else:
            self.log_syntax_error("Expected 'O RLY?' for conditional block", found=self.current_token.value if self.current_token else "None")

    #function to parse Loops
    '''
    IM IN YR loop_name

    IM OUTTA YR loop_name
    
    '''

    def parse_loop(self):
        if self.current_token.value == "IM IN YR": # start of the loop
            print("Parsing loop 'IM IN YR'")
            self.advance_to_next_token()  # Consume 'IM IN YR'

            # Ensure the loop has a valid label
            if not self.current_token or self.current_token.type != "Variable Identifier":
                self.log_syntax_error(
                    "Expected loop label after 'IM IN YR'",
                    found=self.current_token.value if self.current_token else "None"
                )
                return

            loop_label = self.current_token.value  # Save the loop label for later verification
            print(f"Found loop label: {loop_label}")
            self.advance_to_next_token()  # Consume the loop label

            # Ensure loop has a valid operation (UPPIN/NERFIN)
            if not self.current_token or self.current_token.value not in ["UPPIN", "NERFIN"]:
                self.log_syntax_error(
                    "Expected loop operation (UPPIN/NERFIN) after loop label",
                    found=self.current_token.value if self.current_token else "None"
                )
                return

            operation = self.current_token.value
            print(f"Found loop operation: {operation}")
            self.advance_to_next_token()  # Consume the operation

            # Ensure 'YR' keyword is present
            if not self.current_token or self.current_token.value != "YR":
                self.log_syntax_error(
                    "Expected 'YR' after loop operation",
                    found=self.current_token.value if self.current_token else "None"
                )
                return

            print(f"Found 'YR' after loop operation")
            self.advance_to_next_token()  # Consume 'YR'

            # Ensure a valid variable follows 'YR'
            if not self.current_token or self.current_token.type != "Variable Identifier":
                self.log_syntax_error(
                    "Expected variable name after 'YR'",
                    found=self.current_token.value if self.current_token else "None"
                )
                return

            loop_variable = self.current_token.value
            print(f"Found loop variable: {loop_variable}")
            self.advance_to_next_token()  # Consume the variable identifier

            # Check for loop condition (TIL/WILE)
            if self.current_token and self.current_token.value in ["TIL", "WILE"]:
                loop_condition = self.current_token.value
                print(f"Found loop condition: {loop_condition}")
                self.advance_to_next_token()  # Consume TIL/WILE

                # Parse the loop condition expression
                condition_expression = self.parse_expression()
                if condition_expression is None:
                    self.log_syntax_error("Invalid loop condition expression")
                    return
                print(f"Loop condition expression: {condition_expression}")
            else:
                self.log_syntax_error(
                    "Expected loop condition (TIL/WILE) after loop variable",
                    found=self.current_token.value if self.current_token else "None"
                )
                return

            # Parse the loop body
            print(f"Parsing loop body for loop '{loop_label}'")

            while True:
                if not self.current_token:  # If no more tokens, move to the next line
                    self.advance_to_next_line()

                if self.current_token and self.current_token.value == "IM OUTTA YR":
                    break  # Exit loop body when 'IM OUTTA YR' is found bcs nasa end na tayo ng loop

                if self.current_token:  # Parse the current line if tokens exist
                    self.parse_line()
                else:  # If no tokens remain, exit
                    break

            # Debugging: Check if we exited the loop body correctly
            print(f"DEBUG: Exiting loop body for '{loop_label}', current token: {self.current_token.value if self.current_token else 'None'}")

            # Ensure the loop is closed properly
            if self.current_token and self.current_token.value == "IM OUTTA YR":
                self.advance_to_next_token()  # Consume 'IM OUTTA YR'

                # Debugging: Check the next token after 'IM OUTTA YR'
                print(f"DEBUG: Token after 'IM OUTTA YR': {self.current_token.value if self.current_token else 'None'}")

                # Verify the loop label matches
                if self.current_token and self.current_token.value == loop_label:
                    print(f"Loop '{loop_label}' closed correctly")
                    self.advance_to_next_token()  # Consume the loop label
                else:
                    self.log_syntax_error(
                        f"Expected loop label '{loop_label}' after 'IM OUTTA YR'",
                        found=self.current_token.value if self.current_token else "None"
                    )
            else:
                self.log_syntax_error(
                    f"Expected 'IM OUTTA YR {loop_label}' to close loop",
                    found=self.current_token.value if self.current_token else "None"
                )
        else:
            self.log_syntax_error(
                "Expected 'IM IN YR' to define a loop",
                found=self.current_token.value if self.current_token else "None"
            )

    '''
    WTF?                    --> should be present, if not present check if there is OMG in the code if there is but no WTF before it then error   
    OMG <value literal>
    <code block>
    [OMG <value literal>
    <code block>...]
    [OMGWTF --> default case
    <code block>]

    OIC --> LOOP STOP 
    '''
    # function to parse switch statements
    def parse_switch(self):
        self.inside_switch_block = True  # Entering the switch block
        if self.current_token and self.current_token.value == "WTF?": # program must start with 'HAI'
            print("\nSwitch starts with 'WTF?'")
            self.advance_to_next_line() # consume WTF?

            found_cases = False  # Flag to check if any cases (OMG/OMGWTF) are present

            # parse each line until 'OIC' is found
            while self.current_token:
                if self.current_token.value == "OIC":
                    break

                if self.current_token.value == "OMG":  # Case block

                    found_cases = True  # Set flag to True when a case is found
                    
                    print("DEBUG: Found 'OMG'")
                    self.advance_to_next_token()  # Consume 'OMG'
                    if not self.current_token or self.current_token.type not in ["NUMBR Literal", "NUMBAR Literal", "YARN Literal", "TROOF Literal"]:
                        self.log_syntax_error(
                            "Expected literal value after 'OMG'",
                            found=self.current_token.value if self.current_token else "None"
                        )
                        return
                    
                    case_value = self.current_token.value
                    print(f"DEBUG: Found case value: {case_value}")
                    self.advance_to_next_token()  # Consume the case value

                    # Parse the code block for this case
                    while self.current_token and self.current_token.value == "OMG":
                        print(f"DEBUG: Parsing line in case {case_value}: {self.current_token.value}")
                        self.parse_line()
                        if self.current_token is None:
                            self.advance_to_next_line()
                
                elif self.current_token.value == "OMGWTF":
                    found_cases = True
                    print("DEBUG: Found 'OMGWTF'")
                    self.parse_line()
                    if self.current_token is None:
                        self.advance_to_next_line()

                self.parse_line()
                self.advance_to_next_line()

            if self.current_token and self.current_token.value == "OIC":
                print("\nSwitch ends with 'OIC'")
            else:
                self.log_syntax_error("Switch must end with 'OIC'")

            if not found_cases:
                self.log_syntax_error("Switch must have at least one case (OMG/OMGWTF)")
                
        else:
            self.log_syntax_error("Switch must start with 'WTF?'")

        return self.error_messages, self.variables


    '''
    HOW IZ I <function name> [YR <parameter/argument> [AN YR <other _arguments..> …]]
    <code block to execute / Set of statements to execute>
    IF U SAY SO
    HOW IZ I sample_function                     BTW function with 0 arguments
    HOW IZ I sample_function2 YR x AN YR y       BTW function with 2 arguments

    FOUND YR return statment
    '''
    def parse_function(self):
        # Preliminary check for 'IF U SAY SO' without a preceding 'HOW IZ I'
        has_how_iz_i = False
        for line_number, tokens in self.lines.items():
            for token in tokens:
                if token.value == "HOW IZ I":
                    has_how_iz_i = True
                elif token.value == "IF U SAY SO" and not has_how_iz_i:
                    self.log_syntax_error("Found 'IF U SAY SO' without preceding 'HOW IZ I'", found="IF U SAY SO without HOW IZ I")

        if self.current_token and self.current_token.value == "HOW IZ I":  # Function must start with 'HOW IZ I'
            print("\nFunction starts with 'HOW IZ I'")
            self.advance_to_next_token()  # Consume 'HOW IZ I'

            # Ensure function has a valid name
            if not self.current_token or self.current_token.type != "Variable Identifier":
                self.log_syntax_error(
                    "Expected function name after 'HOW IZ I'",
                    found=self.current_token.value if self.current_token else "None"
                )
                return

            function_name = self.current_token.value  # Save the function name for later verification
            print(f"Found function name: {function_name}")
            self.advance_to_next_token()  # Consume the function name

            # List to store parameters for later checks
            parameters = []

            # Parse each line until 'IF U SAY SO' is found
            while self.current_token:
                if self.current_token and self.current_token.value == "IF U SAY SO":
                    break  # End of function

                # Check for YR (argument) before checking for FOUND YR (return statement)
                if self.current_token and self.current_token.value == "YR":
                    self.advance_to_next_token()
                    if not self.current_token or self.current_token.type != "Variable Identifier":
                        self.log_syntax_error(
                            "Expected parameter name after 'YR'",
                            found=self.current_token.value if self.current_token else "None"
                        )
                        return

                    parameter_name = self.current_token.value
                    parameters.append(parameter_name)
                    print(f"Found parameter name: {parameter_name}")
                    self.advance_to_next_token()

                    # Check if there are more parameters
                    if self.current_token and self.current_token.value == "AN":
                        self.advance_to_next_token()  # Consume 'AN'
                    elif self.current_token and self.current_token.value == "YR":
                        self.log_syntax_error(
                            "Expected 'AN' between multiple parameters, but found another 'YR'",
                            found=self.current_token.value
                        )
                        return

                print("Parameter list:", parameters)
                
                if self.current_token and self.current_token.value == "FOUND YR":  # Handle return statements
                    self.advance_to_next_token()  # Consume 'FOUND YR'

                    if self.current_token:
                        return_value = self.current_token.type  # Check the value being returned

                        if return_value in ["NUMBR Literal", "NUMBAR Literal", "TROOF Literal", "YARN Literal"]:
                            print(f"Return statement value: {return_value}")
                            self.advance_to_next_token()  # Consume the value

                        elif return_value == "Variable Identifier":
                            print(f"Return statement variable: {return_value}")
                            self.advance_to_next_token()  # Consume the variable identifier

                        # Check for arithmetic operations (direct check, no separate method)
                        elif self.current_token and self.current_token.type == "Arithmetic Operation":
                            operator = self.current_token.value
                            self.advance_to_next_token()  # Consume the operator

                            if not self.current_token:
                                self.log_syntax_error(
                                    "Missing first operand in arithmetic operation after 'AN'",
                                    found="None"
                                )
                                return

                            # Ensure the first operand is valid
                            if self.current_token and self.current_token.type not in ["NUMBR Literal", "NUMBAR Literal", "Variable Identifier"]:
                                self.log_syntax_error(
                                    "Invalid first operand for arithmetic operation",
                                    found=self.current_token.value if self.current_token else "None"
                                )
                                return

                            operand1 = self.current_token.value
                            print(f"Found first operand: {operand1}")
                            self.advance_to_next_token()  # Consume the first operand

                            # Ensure the 'AN' keyword exists before the second operand
                            if not self.current_token or self.current_token.value != "AN":
                                self.log_syntax_error(
                                    "Expected 'AN' before second operand in arithmetic operation",
                                    found=self.current_token.value if self.current_token else "None"
                                )
                                return
                            self.advance_to_next_token()  # Consume 'AN'

                            if not self.current_token:
                                self.log_syntax_error(
                                    "Missing second operand in arithmetic operation after 'AN'",
                                    found="None"
                                )
                                return

                            # Ensure the second operand is valid
                            if self.current_token and self.current_token.type not in ["NUMBR Literal", "NUMBAR Literal", "Variable Identifier"]:
                                self.log_syntax_error(
                                    "Invalid second operand for arithmetic operation",
                                    found=self.current_token.value if self.current_token else "None"
                                )
                                return

                            operand2 = self.current_token.value
                            print(f"Found second operand: {operand2}")
                            self.advance_to_next_token()  # Consume the second operand

                            print(f"Found valid arithmetic operation: {operand1} {operator} {operand2}")

                        else:
                            self.log_syntax_error(
                                "Invalid return value. Must be a literal, variable, or valid arithmetic operation",
                                found=self.current_token.value if self.current_token else "None"
                            )
                            return

                    else:
                        self.log_syntax_error("Expected return value after 'FOUND YR'", found="None")

                self.parse_line()  # Parse other lines of the function
                self.advance_to_next_line()

            if self.current_token and self.current_token.value == "IF U SAY SO":
                print("\nFunction ends with 'IF U SAY SO'")
            else:
                self.log_syntax_error("Function must end with 'IF U SAY SO'")
        else:
            self.log_syntax_error("Function must start with 'HOW IZ I'")
                
    def parse_functioncall(self):
        if self.current_token and self.current_token.value == "I IZ":  # Function call must start with 'I IZ'
            print("\nFunction call 'I IZ'")
            self.advance_to_next_token()  # Consume 'I IZ'

            # Ensure function call has a valid name
            if not self.current_token or self.current_token.type != "Variable Identifier":
                self.log_syntax_error(
                    "Expected function name after 'I IZ'",
                    found=self.current_token.value if self.current_token else "None"
                )
                return

            function_name = self.current_token.value  # Save the function name 
            print(f"Found function name: {function_name}")
            self.advance_to_next_token()  # Consume the function name

            # Check for arguments (optional)
            while self.current_token and self.current_token.value == "YR":
                self.advance_to_next_token()  # Consume 'YR'

                # Argument can be a literal, variable, or another function call
                if self.current_token.type in ["NUMBR Literal", "NUMBAR Literal", "TROOF Literal", "YARN Literal", "Variable Identifier"]:
                    argument_value = self.current_token.value
                    print(f"Found argument: {argument_value}")
                    self.advance_to_next_token()  # Consume the argument

                # Check for arithmetic operations (direct check, no separate method)
                elif self.current_token and self.current_token.type == "Arithmetic Operation":
                    operator = self.current_token.value
                    self.advance_to_next_token()  # Consume the operator

                    if not self.current_token:
                        self.log_syntax_error(
                            "Missing first operand in arithmetic operation after 'YR'",
                            found="None"
                        )
                        return

                    # Ensure the first operand is valid
                    if self.current_token and self.current_token.type not in ["NUMBR Literal", "NUMBAR Literal", "Variable Identifier"]:
                        self.log_syntax_error(
                            "Invalid first operand for arithmetic operation",
                            found=self.current_token.value if self.current_token else "None"
                        )
                        return

                    operand1 = self.current_token.value
                    print(f"Found first operand: {operand1}")
                    self.advance_to_next_token()  # Consume the first operand

                    # Ensure the 'AN' keyword exists before the second operand
                    if not self.current_token or self.current_token.value != "AN":
                        self.log_syntax_error(
                            "Expected 'AN' before second operand in arithmetic operation",
                            found=self.current_token.value if self.current_token else "None"
                        )
                        return
                    self.advance_to_next_token()  # Consume 'AN'

                    if not self.current_token:
                        self.log_syntax_error(
                            "Missing second operand in arithmetic operation after 'AN'",
                            found="None"
                        )
                        return

                    # Ensure the second operand is valid
                    if self.current_token and self.current_token.type not in ["NUMBR Literal", "NUMBAR Literal", "Variable Identifier"]:
                        self.log_syntax_error(
                            "Invalid second operand for arithmetic operation",
                            found=self.current_token.value if self.current_token else "None"
                        )
                        return

                    operand2 = self.current_token.value
                    print(f"Found second operand: {operand2}")
                    self.advance_to_next_token()  # Consume the second operand

                    print(f"Found valid arithmetic operation: {operand1} {operator} {operand2}")

                elif self.current_token.value == "I IZ":  # Nested function call
                    argument_value = self.parse_functioncall()  # Recursively parse the nested call
                    print(f"Found nested function call as argument: {argument_value}")

                else:
                    self.log_syntax_error(
                        "Expected literal, variable, or function call after 'YR'",
                        found=self.current_token.value if self.current_token else "None"
                    )
                    return

                # Check for more arguments
                if self.current_token and self.current_token.value == "AN":
                    self.advance_to_next_token()  # Consume 'AN'

                    # Check if there is actually another argument after AN
                    if not self.current_token or self.current_token.value != "YR":
                        self.log_syntax_error(
                            "Expected another argument after 'AN'",
                            found=self.current_token.value if self.current_token else "None"
                        )
                        return
                else:
                    break  # No more arguments

            print(f"Function call to '{function_name}' parsed successfully.")

        else:
            self.log_syntax_error("Function call must start with 'I IZ'")