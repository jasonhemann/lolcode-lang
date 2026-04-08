class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {"IT": []}  # Ensure IT starts as an empty list
        self.errors = []        # Accumulate semantic errors
        self.visible_outputs = []  # Holds outputs of VISIBLE statements
        self.in_variable_block = False  # Track if inside a WAZZUP block
        self.it = None          # Implicit IT variable
        self.operators = {"SUM OF", "DIFF OF", "PRODUKT OF", "QUOSHUNT OF", "MOD OF", "BIGGR OF", "SMALLR OF", "BOTH SAEM", "DIFFRINT", "BOTH OF", "EITHER OF", "WON OF", "ALL OF", "ANY OF"}

    def analyze(self, syntax_output, input_callback=None):
        """Analyze the structured output from the syntax analyzer."""
        if not isinstance(syntax_output, list):
            self.errors.append("Invalid syntax output structure.")
            return False

        for statement in syntax_output:
            self.process_statement(statement, input_callback=input_callback)

        print(f"Final Symbol Table: {self.symbol_table}")
        return len(self.errors) == 0

    def process_statement(self, statement, input_callback=None):

        print(f"Processing statement: {statement}")
        """Process a single statement."""
        
        # Handle standalone variable evaluation
        if isinstance(statement, str):
            if statement in self.symbol_table:  # If it's a valid variable
                self.symbol_table["IT"] = self.evaluate_expression(statement)  # Assign its value to IT
                return
            elif statement == "HAI":
                return  # Ignore program start
            elif statement == "KTHXBYE":
                return  # Ignore program end
            else:
                self.errors.append(f"Invalid statement format: {statement}")
                return

        if isinstance(statement, list) and statement:
            keyword = statement[0]
            if keyword == "WAZZUP":
                self.in_variable_block = True
                for var_decl in statement[1:]:
                    if var_decl == "BUHBYE":
                        self.in_variable_block = False
                        break
                    self.handle_variable_declaration(var_decl)
            elif keyword == "VISIBLE":
                self.handle_visible(statement[1:])
            elif keyword == "GIMMEH":
                self.handle_gimmeh(statement[1], input_callback=input_callback)
            elif keyword == "I HAS A":
                self.handle_variable_declaration(statement)
            elif keyword in {"IS NOW A", "MAEK"}:
                self.handle_type_cast(statement)
            elif keyword == "SMOOSH":
                self.handle_smoosh(statement[1:])
            elif keyword == "O RLY?":
                self.handle_orly(statement)
            elif keyword == "WTF?":
                self.handle_wtf(statement)
            elif keyword in self.symbol_table: # for R keyword
                if statement[1] == "R":
                    self.handle_assignment(statement)
            else:
                self.errors.append(f"Unrecognized statement: {statement}")
        else:
            self.errors.append(f"Invalid statement format: {statement}")

    def evaluate_expression(self, expression):
        """Evaluate expressions recursively."""
        print(f"Evaluating expression: {expression}")

        if isinstance(expression, str):
            return self.handle_literals(expression)

        # Handle nested or structured expressions
        elif isinstance(expression, list):
            # Handle single-element list
            if len(expression) == 1:
                return self.evaluate_expression(expression[0])

            # Handle string literals in list form
            if len(expression) > 1 and expression[0] == '"' and expression[-1] == '"':
                value = expression[1:-1][0]
                # Check for numeric literals
                if value.isdigit():
                    return int(value)
                try:
                    return float(value)
                except ValueError:
                    return value  # Return as YARN if not numeric

            # Concatenation with '+' operator
            if '+' in expression:
                return self.handle_concatenation(expression)

            # Handle SMOOSH operation
            if expression[0] == "SMOOSH":
                return self.handle_smoosh(expression[1:])

            # Handle arithmetic or logical operators
            if isinstance(expression, list) and len(expression) > 0:
                operator = expression[0]

                # Check if the operator is a string and belongs to supported operators
                if isinstance(operator, str) and operator in self.operators:
                    if len(expression) < 4 or expression[2] != "AN":
                        self.errors.append(f"Invalid binary operation: {expression}")
                        return None
                    left = self.evaluate_expression(expression[1])  # Evaluate left operand
                    right = self.evaluate_expression(expression[3])  # Evaluate right operand
                    print(f"{operator}: Left = {left}, Right = {right}")  # Debugging
                    left = 1 if left == "WIN" else (0 if left == "FAIL" else left)
                    right = 1 if right == "WIN" else (0 if right == "FAIL" else right)
                    if left is None or right is None:
                        self.errors.append(f"Cannot evaluate operands for operation: {expression}")
                        return None
                    return self.compute_arithmetic(operator, left, right)

                # Handle BIGGR OF and SMALLR OF operators
                if isinstance(operator, str) and operator in {"BIGGR OF", "SMALLR OF"}:
                    if len(expression) < 4 or expression[2] != "AN":
                        self.errors.append(f"Invalid operation: {expression}")
                        return None
                    left = self.evaluate_expression(expression[1])
                    right = self.evaluate_expression(expression[2])
                    print(f"{operator}: Left = {left}, Right = {right}")  # Debugging
                    # left = 1 if left == "WIN" else (0 if left == "FAIL" else left)
                    # right = 1 if right == "WIN" else (0 if right == "FAIL" else right)
                    return max(left, right) if operator == "BIGGR OF" else min(left, right)

                # Handle BOTH SAEM and DIFFRINT operators
                if isinstance(operator, str) and operator in {"BOTH SAEM", "DIFFRINT"}:
                    if len(expression) < 4 or expression[2] != "AN":
                        self.errors.append(f"Invalid comparison operation: {expression}")
                        return None
                    left = self.evaluate_expression(expression[1])
                    right = self.evaluate_expression(expression[3])
                    if left is None or right is None:
                        self.errors.append(f"Cannot evaluate operands for comparison: {expression}")
                        return None
                    # Evaluate the comparison
                    return left == right if operator == "BOTH SAEM" else left != right
            # Unrecognized operator
            else:
                self.errors.append(f"Unrecognized operator: {operator}")
                return None

        else:
            self.errors.append(f"Invalid expression format: {expression}")
            return None

    def handle_assignment(self, statement):
        """Handle variable assignment."""
        if len(statement) < 3 or statement[1] != "R":
            self.errors.append(f"Invalid assignment statement: {statement}")
            return

        variable, value_expression = statement[0], statement[2]
        value = self.evaluate_expression(value_expression)
        if value is not None:
            self.symbol_table[variable] = value
            print(f"Assigned {variable} = {value}")
        else:
            self.errors.append(f"Failed to assign value to {variable}: {value_expression}")

    def handle_type_cast(self, statement):
        """Process typecasting using IS NOW A or MAEK."""
        if statement[2] == "IS NOW A":  # In-place typecasting
            if len(statement) != 4:
                self.errors.append(f"Invalid typecasting statement: {statement}")
                return
            variable, new_type = statement[0], statement[3]
            if variable not in self.symbol_table:
                self.errors.append(f"Undefined variable: {variable}")
                return

            value = self.symbol_table[variable]
            try:
                self.symbol_table[variable] = self.cast_value(value, new_type)
                print(f"Re-cast {variable} to {new_type} = {self.symbol_table[variable]}")
            except (ValueError, TypeError) as e:
                self.errors.append(f"Error casting {variable} to {new_type}: {str(e)}")
        elif statement[0] == "MAEK":  # MAEK operator returns casted value
            variable, new_type = statement[1], statement[2]
            if new_type == "A":
                print("whoopsie A =================================================================================================================================")
                new_type == statement[3]
            if variable not in self.symbol_table:
                self.errors.append(f"Undefined variable: {variable}")
                return
            value = self.symbol_table[variable]
            try:
                return self.cast_value(value, new_type)
            except (ValueError, TypeError) as e:
                self.errors.append(f"Error casting {variable} to {new_type}: {str(e)}")
                return None

    def cast_value(self, value, new_type):
        """Helper method to cast a value to a specified type."""
        if new_type == "NUMBAR":
            return float(value)
        elif new_type == "NUMBR":
            return int(float(value))
        elif new_type == "TROOF":
            return bool(value)
        elif new_type == "YARN":
            return str(value)
        else:
            raise ValueError(f"Unsupported type for casting: {new_type}")

    def handle_variable_declaration(self, declaration):
        """Process variable declarations in the WAZZUP block."""
        if len(declaration) < 2 or declaration[0] != "I HAS A":
            self.errors.append(f"Invalid variable declaration: {declaration}")
            return

        var_name = declaration[1]
        if var_name in self.symbol_table:
            self.errors.append(f"Variable '{var_name}' already declared.")
            return

        # Handle initialization
        if len(declaration) > 2 and declaration[2] == "ITZ":
            value = self.evaluate_expression(declaration[3])
        else:
            value = "NOOB"  # Default uninitialized value

        self.symbol_table[var_name] = value
        print(f"Declared variable: {var_name} = {value}")

    def handle_visible(self, expressions):
        """Process VISIBLE statements."""
        print(f"Processing VISIBLE: {expressions}")
        
        # Function to check if concatenation ('+') is present
        def contains_plus(exp):
            return isinstance(exp, list) and '+' in exp
        
        def contains_an(exp):
            return isinstance(exp, list) and 'AN' in exp

        result = ''
        # for part in expressions:
            # print(f"{part} SDGSJKGNSKDFNKDFNSKDJF11111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111")
        if contains_an(expressions):  # Skip the `AN` keyword
            # continue
            concatenated_result = ''
            for word in expressions:
                print(word)
                if word == 'AN':
                    continue
                evaluated = self.evaluate_expression(word)
                if evaluated is None:
                    self.errors.append(f"Failed to evaluate part of concatenation in VISIBLE: {word}")
                    return
                print(concatenated_result)
                concatenated_result += str(evaluated)
            result += concatenated_result
            self.visible_outputs.append(result)
        elif contains_plus(expressions):  # Handle concatenation using `+`
            concatenated_result = ''
            for subpart in expressions:
                if subpart == '+':
                    continue
                evaluated = self.evaluate_expression(subpart)
                if evaluated is None:
                    self.errors.append(f"Failed to evaluate part of concatenation in VISIBLE: {subpart}")
                    return
                concatenated_result += str(evaluated)
            result += concatenated_result
            self.visible_outputs.append(result)
        else:
            # Evaluate as a single expression
            result = self.evaluate_expression(expressions)
            if result is not None:
                # Store in 'IT' only for non-identifier results
                if not self.is_expression_tied_to_identifier(expressions):
                    if "IT" not in self.symbol_table or not isinstance(self.symbol_table["IT"], list):
                        self.symbol_table["IT"] = []
                    self.symbol_table["IT"].append(result)
                self.visible_outputs.append(result)  # Store for GUI
            else:
                self.errors.append(f"Failed to evaluate VISIBLE statement: {expressions}")

    def is_expression_tied_to_identifier(self, expression):
        """Check if the given expression corresponds to an explicit identifier."""
        if isinstance(expression, str):
            # If the expression is a direct reference to a variable
            return expression in self.symbol_table
        if isinstance(expression, list) and len(expression) == 1:
            # If the expression is wrapped in a list, check the single element
            return self.is_expression_tied_to_identifier(expression[0])
        # Otherwise, it's not tied to any specific identifier
        return False

    def handle_gimmeh(self, variable_name, input_callback=None):
        """Handle the GIMMEH keyword to prompt user input."""
        if variable_name not in self.symbol_table:
            self.errors.append(f"Undefined variable: {variable_name}")
            return

        if input_callback is not None:
            # Use the input callback to get input from the GUI
            user_input = input_callback(variable_name)
            if user_input is not None:
                # Store the user input as a YARN but allow for numeric inference
                try:
                    # Infer type: NUMBR if integer, NUMBAR if float, else YARN
                    if user_input.isdigit():
                        self.symbol_table[variable_name] = int(user_input)
                    else:
                        self.symbol_table[variable_name] = float(user_input)
                except ValueError:
                    self.symbol_table[variable_name] = user_input  # Store as YARN (string)
            else:
                self.errors.append(f"No input provided for variable: {variable_name}")
        else:
            self.errors.append("No input callback provided for GIMMEH.")

    def handle_literals(self, token):
        """Handle numeric, string, boolean literals, or variables."""
        if token.isdigit():
            return int(token)  # NUMBR
        try:
            return float(token)  # NUMBAR
        except ValueError:
            pass

        # Check for string literals
        if isinstance(token, str) and token.startswith('"') and token.endswith('"'):
            value = token.strip('"')  
            if value.isdigit():
                return int(value)
            try:
                return float(value)
            except ValueError:
                return value  # Return as YARN if not numeric

        # Check for boolean literals
        if token == "WIN":
            return 'WIN'  # TROOF
        if token == "FAIL":
            return 'FAIL'  # TROOF

        # Check for variables in the symbol table
        if token in self.symbol_table:
            value = self.symbol_table[token]
            if value == "NOOB":
                return value  # Allow NOOB for non-arithmetic contexts
            return value

        # Undefined token
        self.errors.append(f"Undefined identifier: {token}")
        return None

    def handle_concatenation(self, expressions):
        """Concatenate parts using the '+' operator."""
        result = ''
        for part in expressions:
            if part == '+' or part == 'AN':
                continue
            evaluated = self.evaluate_expression(part)
            if evaluated is None:
                self.errors.append(f"Failed to evaluate part of concatenation: {part}")
                return None
            result += str(evaluated)
        return result

    def handle_smoosh(self, expressions):
        """Concatenate multiple operands into a single string."""
        result = ''
        for part in expressions:
            if part == 'AN':  # Skip the 'AN' keyword
                continue
            evaluated = self.evaluate_expression(part)
            if evaluated is None:
                self.errors.append(f"Failed to evaluate part of SMOOSH: {part}")
                return None
            result += str(evaluated)  # Convert to YARN if necessary
        return result
    
    def handle_orly(self, statement):
        """Process O RLY? conditional statements."""
        print(f"Processing O RLY?: {statement}")
        if len(statement) < 3:
            self.errors.append(f"Invalid O RLY? structure: {statement}")
            return

        # Extract condition and branches
        condition = statement[1]  # First expression
        branches = statement[2:]

        # Evaluate the condition
        condition_result = self.evaluate_expression(condition)

        # Find YA RLY, NO WAI, and optional MEBBE branches
        ya_rly_block = []
        no_wai_block = []
        mebbe_blocks = []  # Each MEBBE block is (condition, statements)

        for i in range(len(branches)):
            if branches[i] == "YA RLY":
                ya_rly_block = branches[i + 1]
            elif branches[i] == "NO WAI":
                no_wai_block = branches[i + 1]
            elif branches[i] == "MEBBE":
                mebbe_blocks.append((branches[i + 1], branches[i + 2]))

        # Execute the appropriate block
        if condition_result == "WIN":
            self.execute_block(ya_rly_block)
        else:
            executed = False
            for mebbe_condition, mebbe_block in mebbe_blocks:
                if self.evaluate_expression(mebbe_condition) == "WIN":
                    self.execute_block(mebbe_block)
                    executed = True
                    break
            if not executed:  # No MEBBE conditions matched
                self.execute_block(no_wai_block)

    def handle_wtf(self, statement):
        """Process WTF? (switch-case) statements."""
        print(f"Processing WTF?: {statement}")
        if len(statement) < 3 or statement[-1] != "OIC":
            self.errors.append(f"Invalid WTF? structure: {statement}")
            return

        # Get the value of IT for comparison
        switch_value = self.symbol_table.get("IT", None)

        # Extract cases and default
        cases = []
        default_block = None

        for i, part in enumerate(statement[1:]):
            if part == "OMG":
                case_value = self.evaluate_expression(statement[i + 2])
                case_block = statement[i + 3:]
                cases.append((case_value, case_block))
            elif part == "OMGWTF":
                default_block = statement[i + 2:]
                break

        # Match and execute the appropriate case
        executed = False
        for case_value, case_block in cases:
            if switch_value == case_value:
                for stmt in case_block:
                    if stmt == "GTFO":
                        return  # Exit the WTF? structure
                    self.process_statement(stmt)
                executed = True
                break

        # Execute default block if no case matches
        if not executed and default_block:
            for stmt in default_block:
                self.process_statement(stmt)

    def execute_block(self, block):
        """Execute a block of statements."""
        if isinstance(block, list):
            for statement in block:
                self.process_statement(statement)

    def compute_arithmetic(self, operator, left, right):
        """Perform arithmetic operations."""
        try:
            if operator == "SUM OF":
                return left + right
            elif operator == "DIFF OF":
                return left - right
            elif operator == "PRODUKT OF":
                return left * right
            elif operator == "QUOSHUNT OF":
                if right == 0:
                    self.errors.append("Division by zero in QUOSHUNT OF")
                    return None
                return left / right
            elif operator == "MOD OF":
                if right == 0:
                    self.errors.append("Division by zero in MOD OF")
                    return None
                return left % right
            elif operator == 'BIGGR OF':
                return max(left, right)
            elif operator == 'SMALLR OF':
                return min(left, right)
            elif operator == 'BOTH OF':
                return 'WIN' if (left and right) else 'FAIL'
            elif operator == 'EITHER OF':
                return 'WIN' if (left or right) else 'FAIL'
            elif operator == 'WON OF':
                return 'WIN' if (left or right) and not (left and right) else 'FAIL'
            elif operator == 'BOTH SAEM':
                return 'WIN' if (left == right) else 'FAIL'
            elif operator == 'DIFFRINT':
                return 'WIN' if (left != right) else 'FAIL'
            elif operator == 'ALL OF':
                return 'WIN' if (left and right) else 'FAIL'
            else:
                self.errors.append(f"Unknown arithmetic operator: {operator}")
                return None
        except TypeError:
            self.errors.append(f"Type error in operation '{operator}' with operands '{left}' and '{right}'.")
            return None
        except ZeroDivisionError:
            self.errors.append("Division by zero.")
            return None

    def get_visible_outputs(self):
        """Return all visible outputs."""
        return self.visible_outputs

    def report_errors(self):
        """Return all semantic errors."""
        return self.errors

