from syntax_analyzer import analyze_syntax

analyzed_nodes = set()
IT_variable = 'FAIL'

class SymbolTable:
    def __init__(self):
        self.table = {}
        self.current_scope = "global"
        self.scopes = {"global": {}}
        self.IT = {"value": None, "type": "NOOB"}

    # -----------------------------------------------------------------------------------------
    #  FUNCTION: Add a symbol to the current scope
    # -----------------------------------------------------------------------------------------
    def add_update_symbol(self, name, attributes):
        self.scopes[self.current_scope][name] = attributes

    def reset_symbol_table(self):
        self.table = {}
        self.current_scope = "global"
        self.scopes = {"global": {}}
        self.IT = {"value": None, "type": "NOOB"}

    # -----------------------------------------------------------------------------------------
    #  FUNCTION: Look up a symbol in the current scope or its ancestors
    # -----------------------------------------------------------------------------------------
    def lookup(self, name):
        # Check current scope
        if name in self.scopes[self.current_scope]:
            return self.scopes[self.current_scope][name]
        
        # Check global scope
        if name in self.scopes['global']:
            return self.scopes['global'][name]
        
        # Not found
        return None

    # -----------------------------------------------------------------------------------------
    #  FUNCTION: Enter a scope (Create a new one if it does not yet exist)
    # -----------------------------------------------------------------------------------------
    def enter_scope(self, scope_name):
        if scope_name not in self.scopes:
            self.scopes[scope_name] = {}
        self.current_scope = scope_name

    # -----------------------------------------------------------------------------------------
    # FUNCTION: Exit the current scope
    # -----------------------------------------------------------------------------------------
    def exit_scope(self):
        if self.current_scope == "global":
            raise Exception("Cannot exit the global scope.")
        self.current_scope = "global"
    
    # -----------------------------------------------------------------------------------------
    # FUNCTION: Get variable value
    # -----------------------------------------------------------------------------------------
    def get_value(self, name):

        # Check current scope
        if name in self.scopes[self.current_scope]:
            return self.scopes[self.current_scope][name]["value"]

        # Check global scope
        elif name in self.scopes["global"]:
            return self.scopes["global"][name]["value"]
        
        elif name == 'IT':
            value = self.get_IT()
            if value is None:
                raise Exception("Implicit IT not yet initialized")
                
        else:
            raise Exception(f"Variable {name} not declared")
        
    # -----------------------------------------------------------------------------------------
    # FUNCTION: Updating, getting IT variable and its type
    # -----------------------------------------------------------------------------------------
    def update_IT(self, value, var_type):
        self.IT["value"] = value
        self.IT["type"] = var_type

    def get_IT(self):
        return self.IT["value"]
    
    def get_IT_type(self):
        return self.IT["type"]

class SemanticAnalyzer:
    def __init__(self, gui):
        self.gui = gui
        self.symbol_table = SymbolTable()
        self.log_console = None
        self.latest_visible = ""

    def request_input(self, title, varname):
        return self.gui.request_input(title, f"Please enter input for variable {varname}:")

    def log(self, message, **kwargs):
        if self.log_console:
            end = kwargs.get('end', '') 
            self.log_console(message + end if end else message)
        else:
            print(message, **kwargs)

    # Start the semantic analysis on the parse tree.
    def analyze(self, node):
        if not node:
            return
        if node in analyzed_nodes:
            return
        analyzed_nodes.add(node)

        # self.log(f"Analyzing node: {node.type}") # node.type indicates what construct to analyze it with

        match node.type:
            case "Program Body":
                for child in node.children:
                    self.analyze(child)
            case "Functions":
                for function_node in node.children:
                    self.analyze_function(function_node)
            case "Variable Declaration":
                self.analyze_variable_declaration(node)
            case "Output":
                self.analyze_output(node)
            case "Assignment":
                self.analyze_assignment(node)
            case "Operation":
                if node.value == "Comparison Operation":
                    self.evaluate_comparison_operation(node)
                elif node.value == "Arithmetic Operation":
                    self.evaluate_arithmetic_operation(node)
                elif node.value == "Boolean Operation":
                    self.evaluate_boolean_operation(node)
            case "Function Call":
                self.evaluate_function(node)
            case "If-Then":
                self.analyze_control_flow(node)
            case "Loop":
                self.analyze_control_flow(node)
            case 'Switch-Case':
                self.analyze_control_flow(node)
            case "Typecasting":
                self.check_typecasting(node)
            case 'Input':
                self.analyze_input(node)
        
        # Traverse through the tree
        for child in node.children:
            self.analyze(child)

    # -----------------------------------------------------------------------------------------
    # FUNCTION: Process and validate assignment statements
    # ----------------------------------------------------------------------------------------- 
    def analyze_assignment(self, node):
        variable = next((child for child in node.children if child.type == "Variable"), None)
        new_value_node = next((child for child in node.children if child.type == "New Value"), None)

        if not variable or not new_value_node:
            raise Exception("Invalid assignment statement structure")

        if new_value_node.children:
            for new_value in new_value_node.children:
                if new_value.type in ["NUMBR", "NUMBAR", "TROOF", "YARN"]:
                    # Direct value assignment
                    value = new_value.value
                    if new_value.type == "NUMBR":
                        value = int(value)
                    elif new_value.type == "NUMBAR":
                        value = float(value)
                    self.symbol_table.add_update_symbol(variable.value, {"type": new_value.type, "value": value})
                
                elif new_value.type == "Operation":
                    # Handle arithmetic operations
                    if new_value.value == "Arithmetic Operation":
                        result, result_type = self.evaluate_arithmetic_operation(new_value)
                        self.symbol_table.add_update_symbol(variable.value, {"type": result_type, "value": result})
                    
                    # Handle string concatenation (SMOOSH)
                    elif new_value.value == "String Concatenation":
                        result, result_type = self.evaluate_smoosh(new_value)
                        self.symbol_table.add_update_symbol(variable.value, {"type": result_type, "value": result})
                
                elif new_value.type == "Variable":
                    # Variable to variable assignment
                    value = self.symbol_table.get_value(new_value.value)
                    value_type = self.symbol_table.get_type(new_value.value)
                    if value is None or value == "NOOB":
                        raise Exception(f"Variable '{new_value.value}' not initialized")
                    self.symbol_table.add_update_symbol(variable.value, {"type": value_type, "value": value})
                
                else:
                    raise Exception(f"Unsupported value type in assignment: {new_value.type}")

    # -----------------------------------------------------------------------------------------
    # FUNCTION: Process and validate variable declaration constructs
    # ----------------------------------------------------------------------------------------- 
    def analyze_variable_declaration(self, node):
        for var_node in node.children:
            if var_node.type == "Variable":
                name = var_node.value
                value_node = next((child for child in var_node.children if child.type == "Value"), None)
                type_node = next((child for child in var_node.children if child.type == "Type"), None)

                # Evaluate the variable's value and type
                value, infer_type = self.evaluate_value(value_node, type_node)

                # Add the variable to the symbol table
                self.symbol_table.add_update_symbol(name, {"type": infer_type, "value": value})
                # self.log(f"Declared variable '{name}' with value {value} and type {infer_type}")
    
    # -----------------------------------------------------------------------------------------
    # FUNCTION: Evaluate the value of a variable during declaration
    # ----------------------------------------------------------------------------------------- 
    def evaluate_value(self, value_node, type_node):
        if not value_node:  # Check if the node itself is None
            # self.log("value_node is None")
            return "NOOB", "NOOB"  # Default initialization

        if value_node.value is None or value_node.value == "None" or value_node.value == "NOOB":  # Explicit check for None value
            # self.log("value_node.value is None")
            return "NOOB", "NOOB"  # Default initialization
            
        # Debug
        # self.log(f"value_node: {value_node.type} | {value_node.value}")
        # self.log(f"type_node: {type_node.type} | {type_node.value}\n")

        match type_node.value:
            case "NUMBR":
                return int(value_node.value), "NUMBR"
            case "NUMBAR":
                return float(value_node.value), "NUMBAR"
            case "YARN":
                return value_node.value, "YARN"
            case "TROOF":
                return value_node.value, "TROOF"
            case "Operation":
                if value_node.value == "VISIBLE":
                    raise Exception(f"Unsupported value type {value_node.value} (Error 3)")
                return self.evaluate_arithmetic_operation(value_node)
            case None:
                if value_node.value == "Arithmetic Operation":
                    return self.evaluate_arithmetic_operation(value_node)
                raise Exception(f"Unsupported value type {type_node.value} (Error 1)")
            case "NOOB":
                if value_node.value == "Arithmetic Operation":
                    return self.evaluate_arithmetic_operation(value_node)
                raise Exception(f"Unsupported value type {type_node.value} (Error 2)")
            case _:
                raise Exception(f"Unsupported value type {type_node.value} (Error 3)")
    
    # -----------------------------------------------------------------------------------------
    # FUNCTION: Evaluate comparison operations
    # ----------------------------------------------------------------------------------------- 
    def evaluate_comparison_operation(self, comparison_node):
        operator = next((child.value for child in comparison_node.children if child.type == "Operator"), None)
        operands = next((child.children for child in comparison_node.children if child.type == "Operand"), None)

        if not operator or not operands:
            raise Exception("Incorrect comparision operation structure (Error 4)")
        
        left_operand = operands[0]
        right_operand = operands[1]

        left_value, left_type = self._evaluate_operand(left_operand)
        right_value, right_type = self._evaluate_operand(right_operand)

        # Ensure operands are of the same type
        # if left_type != right_type:
        #     raise Exception(f"Comparison operands must be of the same type: {left_type} vs {right_type}")

        # Perform the comparison
        result = None
        
        match operator:
            case "BOTH SAEM":
                result = left_value == right_value
            case "DIFFRINT":
                result = left_value != right_value
            case "BIGGR OF":
                result = left_value > right_value
            case "SMALLR OF":
                result = left_value < right_value
            case _:
                raise Exception(f"Unsupported comparison operator: {operator}")
        
        # For boolean comparisons, update IT and return TROOF
        result_troof = "WIN" if result else "FAIL"
        self.symbol_table.update_IT(result_troof, "TROOF")
        
        return result_troof, "TROOF"
    
    # Helper functions
    def _evaluate_operand(self, operand_node):
        # print(f"Processing operand: {operand_node}")
        if operand_node.type == "Variable":
            var_name = operand_node.value
            # print(f"Accessing {var_name}")
            var_symbol = self.symbol_table.lookup(var_name)
            if not var_symbol:
                raise Exception(f"Variable '{var_name}' not declared.")

            var_value = var_symbol['value']
            var_type = var_symbol['type']

            # print(f"Variable resolved: {var_value} ({var_type})")

            # Typecast if YARN
            if var_type == "YARN":
                return self._typecast_to_numeric(var_value)
            elif var_type in ["NUMBR", "NUMBAR"]:
                return var_value, var_type
            else:
                raise Exception(f"Unsupported variable type '{var_type}' for comparison operations.")

        elif operand_node.type == "YARN":
            # Typecast YARN explicitly
            raw_value, _ = self.evaluate_value(
                operand_node, type("TypeNode", (), {"value": "YARN"})
            )
            return self._typecast_to_numeric(raw_value)
        
        # Handle other types like NUMBR, NUMBAR, etc.
        elif operand_node.type in ["NUMBR", "NUMBAR", "TROOF"]:
            value, value_type = self.evaluate_value(
                operand_node, type("TypeNode", (), {"value": operand_node.type})
            )
            return value, value_type

        # Handle operations
        elif operand_node.type == "Operation":
            return self.evaluate_arithmetic_operation(operand_node)

        raise Exception(f"Unsupported operand type: {operand_node.type}")


    def _typecast_to_numeric(self, value):
        #print(f"Attempting to typecast value '{value}' to NUMBR or NUMBAR")
        if isinstance(value, str):
            if value.isdigit() or (value.startswith('-') and value[1:].isdigit()):
                #print(f"Returning as {int(value)} and 'NUMBR'")
                return int(value), "NUMBR"
            try:
                #print(f"Returning as {int(value)} and 'NUMBAR'")
                float_value = float(value)
                return float_value, "NUMBAR"
            except ValueError:
                #print("Error!")
                pass
        raise Exception(f"Value '{value}' cannot be typecast into NUMBR or NUMBAR.")

    
    # -----------------------------------------------------------------------------------------
    # FUNCTION: Evaluate boolean operations
    # -----------------------------------------------------------------------------------------
    def evaluate_boolean_operation(self, node):
        operator = next((child.value for child in node.children if child.type == "Operator"))

        operand_node = next((child for child in node.children if child.type == "Operand"))
        operands = [child for child in operand_node.children]

        # Helper typecaster to TROOF
        def typecast_to_troof(value):
            if value in [0, 0.0, 'FAIL', None, 'NOOB', "", '""']:
                return 'FAIL'
            return 'WIN'
        
        def evaluate_operand(operand):
            if operand.type == "Variable":
                value = self.symbol_table.get_value(operand.value)
            elif operand.type == "Operation":
                value, _ = self.evaluate_boolean_operation(operand)
            else: # Assume direct value
                value_node = operand
                type_node = type("TypeNode", (), {"value": operand.type})
                value, _ = self.evaluate_value(value_node, type_node)
            return typecast_to_troof(value)
        
        # Process operands based on the operator
        if operator == "NOT":
            if len(operands) != 1:
                raise Exception(f"NOT operation requires exactly one operand. Found: {len(operands)}")
            operand = evaluate_operand(operands[0])
            result = "FAIL" if operand == "WIN" else "WIN"

        elif operator == "BOTH OF":
            if len(operands) != 2:
                raise Exception(f"BOTH OF operation requires exactly two operands. Found: {len(operands)}")
            operand1 = evaluate_operand(operands[0])
            operand2 = evaluate_operand(operands[1])
            result = "WIN" if operand1 == "WIN" and operand2 == "WIN" else "FAIL"

        elif operator == "EITHER OF":
            if len(operands) != 2:
                raise Exception(f"EITHER OF operation requires exactly two operands. Found: {len(operands)}")
            operand1 = evaluate_operand(operands[0])
            operand2 = evaluate_operand(operands[1])
            result = "WIN" if operand1 == "WIN" or operand2 == "WIN" else "FAIL"

        elif operator == "WON OF":
            if len(operands) != 2:
                raise Exception(f"WON OF operation requires exactly two operands. Found: {len(operands)}")
            operand1 = evaluate_operand(operands[0])
            operand2 = evaluate_operand(operands[1])
            result = "WIN" if (operand1 == "WIN") != (operand2 == "WIN") else "FAIL"

        elif operator == "ALL OF":
            if len(operands) < 2:
                raise Exception(f"ALL OF operation requires at least two operands. Found: {len(operands)}")
            result = "WIN"
            for operand in operands:
                if evaluate_operand(operand) == "FAIL":
                    result = "FAIL"
                    break

        elif operator == "ANY OF":
            if len(operands) < 2:
                raise Exception(f"ANY OF operation requires at least two operands. Found: {len(operands)}")
            result = "FAIL"
            for operand in operands:
                if evaluate_operand(operand) == "WIN":
                    result = "WIN"
                    break

        else:
            raise Exception(f"Unsupported boolean operation: {operator}")

        # Update IT with the result and return it
        self.symbol_table.update_IT(result, "TROOF")
        return result, "TROOF"

    # -----------------------------------------------------------------------------------------
    # FUNCTION: Evaluate arithmetic operations
    # ----------------------------------------------------------------------------------------- 
    def evaluate_arithmetic_operation(self, operation_node):
        operator = next((child for child in operation_node.children if child.type == "Operator"), None)
        main_operand_parent = next((child for child in operation_node.children if child.type == "Operand"), None)
        operand_nodes = [child for child in main_operand_parent.children]

        # self.log(operand_nodes)

        if not operator or not operand_nodes:
            raise Exception("Incorrect arithmetic operation structure (Error 3)")

        operands = []
        for operand_node in operand_nodes:

            # Handle variable lookup
            if operand_node.type == "Variable":
                # self.log("Entering variable..")
                var_value = self.symbol_table.get_value(operand_node.value)
                # self.log(f"Got var_value of {var_value}")
                if var_value is None or var_value == "NOOB":
                    raise Exception(f"Variable '{operand_node.value}' not yet initialized")
                
                if isinstance(var_value, str):
                    # Remove leading minus sign if present for checking digits
                    test_value = var_value.lstrip('-')
                    if test_value.isdigit():  # Check if the string represents an integer
                        var_value = int(var_value)
                    elif test_value.replace('.', '', 1).isdigit() and test_value.count('.') == 1:  # Check if it's a float
                        var_value = float(var_value)
                    else:
                        raise Exception(f"{var_value} cannot be implicitly typecasted to neither NUMBR or NUMBAR")

                operands.append(var_value)
            
            # Recursive evaluation for nested operations
            elif operand_node.type == "Operation" or operand_node.value == "Arithmetic Operation":
                # self.log("Entering arithmetic operation..")
                value, _ = self.evaluate_arithmetic_operation(operand_node)
                operands.append(value)

            # Direct evaluation for literals or other types (base case)
            else:
                type_node = type("TypeNode", (), {"type": "Type" ,"value": operand_node.type})()  # Pass a pseudo-node
                value_node = type("ValueNode", (), {"type": "Value", "value": operand_node.value})()
                value, _ = self.evaluate_value(value_node, type_node)
                operands.append(value)

        # Perform the arithmetic operation
    
        match operator.value:
            case "SUM OF":
                result = sum(operands)
            case "DIFF OF":
                result = operands[0] - operands[1]
            case "PRODUKT OF":
                # TODO: Check if it's okay to do float multiplication
                result = operands[0] * operands[1] 
            case "QUOSHUNT OF":
                if operands[1] == 0:
                    raise Exception("Division by zero")
                result = operands[0]/operands[1]
                
                # since python converts division operands to float implicitly,
                # check if we need to have an integer result
                if isinstance(operands[0], int) and isinstance(operands[1], int):
                    result = int(result)
                    
            case "MOD OF":
                try:
                    result = operands[0] % operands[1]
                except ZeroDivisionError as e:
                    raise Exception("Modulo division by zero")
            case "BIGGR OF":
                result = max(operands)
            case "SMALLR OF":
                result = min(operands)
            case _:
                raise Exception(f"Unsupported operator: {operator.value}")
            
        # Update implicit IT variable with the result
        self.symbol_table.update_IT(result, "NUMBR" if isinstance(result, int) else "NUMBAR")
        analyzed_nodes.add(operation_node)
        return result, self.symbol_table.get_IT_type()

    # -----------------------------------------------------------------------------------------
    # FUNCTION: Process and validate output (print) statements
    # ----------------------------------------------------------------------------------------- 
    def analyze_output(self, node):
        output_str = ""

        for child in node.children[1].children:
            # Evaluate SMOOSH
            if child.value == "String Concatenation":
                try:
                    value, _ = self.evaluate_smoosh(child)
                    output_str += value
                except Exception as e:
                    raise Exception(f"Error in SMOOSH operation: {e}")
            
            # Handle arithmetic operations
            elif child.type == "Operation":
                try:
                    if child.value == "Boolean Operation":
                        value, _ = self.evaluate_boolean_operation(child)
                    elif child.value == "Comparison Operation":
                        value, _ = self.evaluate_comparison_operation(child)
                    else: 
                        value, _ = self.evaluate_arithmetic_operation(child)
                        
                    str_value = str(value)

                    # Remove the quotation marks
                    if isinstance(str_value, str) and len(str_value) >= 2 and str_value[0] == '"' and str_value[-1] == '"':
                        output_str += str_value[1:-1]
                    else:
                        output_str += str_value
                except Exception as e:
                    raise Exception(f"Error in output operation: {e}")
                
            elif child.type == "Variable":  # Handle Variables
                try:
                    if child.value == "IT":
                        value = self.symbol_table.get_IT()
                    else:
                        value = self.symbol_table.get_value(child.value)
                    output_str += str(value)
                except Exception as e:
                    raise Exception(f"Semantic error: {e}")
        
            elif child.type == "YARN":  # Handle String Literals
                # Remove the quotation marks
                if child.value[0] == '"' and child.value[-1] == '"':
                    output_str += child.value[1:-1]
                else:
                    output_str += child.value
            
            elif child.type == "Newline":  # Handle Newlines
                output_str += "\n"
            
            else:
                raise Exception(f"Unsupported output type: {child.type}")
        # handling special characters in strings
        output_str = output_str.replace(r":>", "\n").replace(r":)", "\t").replace(r":o", f"{chr(7)}").replace(r"::", ":")
        self.log(output_str, end="")
        analyzed_nodes.discard(node)
        self.latest_visible = output_str

    # -----------------------------------------------------------------------------------------
    # FUNCTION: Analyze control flow structures (If-Then, Switch Case, Loop)
    # ----------------------------------------------------------------------------------------- 
    def analyze_control_flow(self, node):
        match node.type:
            case "If-Then":
                self.analyze_if_then(node)
            case "Switch-Case":
                self.analyze_switch_cases(node)
            case "Loop":
                self.analyze_loops(node)
            case _:
                raise Exception(f"Invalid control flow instruction")
            
            
    def analyze_if_then(self, node):
        it_value = self.symbol_table.get_IT()
        it_value = self.typecast_IT(it_value)

        # Find the YA RLY, MEBBE, NO WAI blocks
        ya_rly = next((child for child in node.children if child.type == "YA RLY"), None)
        no_wai = next((child for child in node.children if child.type == "NO WAI"), None)
        mebbe_blocks = [child for child in node.children if child.type == "MEBBE"]

        if it_value == "WIN" and ya_rly:
            for child in ya_rly.children:
                self.analyze(child)
            
            # Disable the other nodes in the if-block
            analyzed_nodes.add(ya_rly)
            analyzed_nodes.add(node)
            for mebbe in mebbe_blocks:
                analyzed_nodes.add(mebbe)
            if no_wai:
                analyzed_nodes.add(no_wai)
        elif it_value == "FAIL":
            # Don't let the previous instruction to run
            for child in ya_rly.children:
                analyzed_nodes.add(child)

            iteration = 0

            handled_mebbe = False
            for mebbe in mebbe_blocks:
                # Evaluate MEBBE condition  
                
                condition_node = next((child for child in mebbe.children if child.type == "Condition"), None)
                condition = next((child for child in condition_node.children if child.type == "Operation" and child.value == "Comparison Operation"), None)

                if condition:
                    try:
                        result = "WIN"
                        if (condition.value == "Comparison Operation"):
                            result, _ = self.evaluate_comparison_operation(condition)
                        else:
                            result, _ = self.evaluate_arithmetic_operation(condition)

                        if result == "WIN":
                            for child in mebbe.children:
                                if child.type not in ["Operation", "Operand"]:
                                    self.analyze(child)
                                analyzed_nodes.add(mebbe)
                            handled_mebbe = True
                        else:
                            analyzed_nodes.add(mebbe)
                    except Exception:
                        continue

            # Execute NO WAI block if no MEBBE block was executed and IT is FAIL
            if not handled_mebbe and no_wai:
                for child in no_wai.children:
                    self.analyze(child)
                analyzed_nodes.add(no_wai)
            else:
                if no_wai:
                    for child in no_wai.children:
                        analyzed_nodes.add(child)
                    analyzed_nodes.add(no_wai)

    def analyze_switch_cases(self,node):
        it_value = self.symbol_table.get_IT()
        it_type = self.symbol_table.get_IT_type()

        # Separate OMG cases, default OMGWTF case, and other case blokcs
        omg_cases = [child for child in node.children if child.type == "OMG"]
        default_case = next((child for child in node.children if child.type == "OMGWTF"), None)

        # To track if a matching case was found
        # Still need to put the rest of the nodes to analyzed anyways
        case_matched = False
        
        for case in omg_cases:
            case_value_node = next((child.children for child in case.children if child.type == "Condition"), None)

            case_value = case_value_node[0]
            
            if case_value:
                if str(case_value.value) == str(it_value):
                    case_matched = True

                    # Execute the case block
                    for child in case.children:
                        self.analyze(child)

                        # If we reach the end of the case block, do not let the other cases breathe and see the light of day
                        if child.value == "GTFO":
                            for omg in omg_cases:
                                analyzed_nodes.add(omg)
                            analyzed_nodes.add(default_case)

        # Default case
        if not case_matched and default_case:
            for child in default_case.children:
                self.analyze(child)
            
            for case in omg_cases:
                analyzed_nodes.add(case)
            analyzed_nodes.add(default_case)
                    
    def analyze_loops(self, node):
        # Get the details of the loop
        step = next((child.value for child in node.children if child.type == "Step"), None)
        variable_node = next((child for child in node.children if child.type == "Variable"), None)
        variable_name = variable_node.value

        # (OPTIONAL) TIL/WILE Condition 
        til_wile_node = next((child for child in node.children if child.type == "Condition"), None)

        # Get variable value (initial) and apply typecasting
        initial_value = self.symbol_table.get_value(variable_name)
        if isinstance(initial_value, str):
            try:
                if '.' in initial_value:
                    initial_value = float(initial_value)
                else:
                    initial_value = int(initial_value)
            except ValueError:
                raise Exception(f"Cannot convert '{initial_value}' to numeric type for loop variable")

        # Determine loop direction and condition type
        is_uppin = step == "UPPIN"
        is_til = til_wile_node and til_wile_node.value.strip() == "TIL"  # Fix comparison
        is_wile = til_wile_node and til_wile_node.value.strip() == "WILE"  # Fix comparison

        # Find the condition operation
        condition_operation = next((child for child in til_wile_node.children if child.type == "Operation"), None) if til_wile_node else None

        # BODY
        loop_body = [child for child in node.children if child.type not in ["Step", "Variable", "Condition"]]
        # Execute the loop
        current_value = initial_value
        while True:
            # Evaluate the condition (if it exists)
            if condition_operation:
                # Update IT with current value before condition evaluation
                self.symbol_table.update_IT(current_value, "NUMBR")

                # Evaluate condition
                result, _ = self.evaluate_comparison_operation(condition_operation)

                # Check exit conditions
                if (is_til and result == "WIN") or (is_wile and result == "FAIL"):
                    # add nodes to analyzed
                    analyzed_nodes.add(til_wile_node)
                    for child in node.children:
                        analyzed_nodes.add(child)
                        
                    break
            
            # removes nested loop inside the current loop
            # so that it will still execute in the next iterations
            for body_node in loop_body:
                if body_node in analyzed_nodes:
                    analyzed_nodes.remove(body_node)
                    
            # Execute loop body
            for body_node in loop_body:
                if body_node.value == "GTFO":
                    return
                self.analyze(body_node)

            # Update the loop variable
            if is_uppin:
                current_value += 1
            else:
                current_value -= 1

            self.symbol_table.add_update_symbol(variable_name, {"type": "NUMBR", "value": current_value})
    # -----------------------------------------------------------------------------------------
    # FUNCTION: Evaluate SMOOSH (string concatenation)
    # ----------------------------------------------------------------------------------------- 
    def evaluate_smoosh(self, node):
        operand_node = next((child for child in node.children if child.type == "Operand"))
        
        operands = []

        # Gather all operands in the SMOOSH operation
        for child in operand_node.children:
            if child.type == "Variable":
                value = self.symbol_table.get_value(child.value)
                operands.append(str(value)) # Convert to string
            elif child.type == "Value":
                operands.append(str(child.value))
            elif child.type == "Operation":
                value, _ = self.evaluate_arithmetic_operation(child)
                operands.append(str(value))
            else:
                raise Exception(f"Unsupported type in SMOOSH operation: {child.type}")
            ''
        result = ''.join(operands)
        #printoperands)
        self.symbol_table.update_IT(result, "YARN")
        return result, "YARN"
                         
    # --------------------------------------------------------------------------------------------------------
    # FUNCTION: Typecasting IT variable to TROOF for Control Constructs 
    # --------------------------------------------------------------------------------------------------------
    def typecast_IT(self,value_IT):
        # Convert IT to TROOF
        if value_IT in [0, '""', 'FAIL', None]:
            value_IT = "FAIL"
        else:
            value_IT = "WIN"

        self.symbol_table.update_IT(value_IT, "TROOF")
        return value_IT
    
    # --------------------------------------------------------------------------------------------------------
    # FUNCTION: For typecasting statements - checks if typecasting is possible, if yes: proceed in typecasting 
    # --------------------------------------------------------------------------------------------------------
    def check_typecasting(self,node):
        global IT_variable
        target_type = ''
        z = None # holds child.type
        for child in node.children:
            if (child.type == "Destination Variable" and len(node.children) in [3,2]):# IS NOW A
                z = child.type
                var = child.value
                symbol = self.symbol_table.lookup(var)
                
                if not symbol:
                    raise Exception(f"Variable '{var}' not declared before typecasting")
                # retrieve target conversion type
                target_type = next((child.value for child in node.children if child.type in ['TYPE','Type']), None)  

            elif child.type == 'Variable' and len(node.children) == 2: #MAEK
                z = child.type
                var = child.value
                symbol = self.symbol_table.lookup(var)
                if not symbol:
                    raise Exception(f"Variable '{var}' not declared before typecasting")
                target_type = next((child.value for child in node.children if child.type == 'TYPE'), None)

            
            # Start of typecasting
            # TYPECASTING TO NUMBR
            if target_type == 'NUMBR':
                # From YARN
                if symbol['type'] == 'YARN':
                    clean = symbol['value'].strip('\"')  
                    try:  
                        x = float(clean) # convert to float first to catch errors 
                        if (z == "Destination Variable" and len(node.children) in [3,2]):# IS NOW A
                            symbol['value'] = int(x)
                        else: IT_variable = int(x)  # Convert to integer
                    except Exception as e:
                        raise Exception(f"Cannot convert value '{clean}' to NUMBR")
                # From TROOF
                elif symbol['value'] == 'WIN':
                    if (z == "Destination Variable" and len(node.children) in [3,2]):# IS NOW A
                        symbol['value'] = 1
                    else: IT_variable = 1  
                elif symbol['value'] == 'FAIL':
                    if (z == "Destination Variable" and len(node.children) in [3,2]):# IS NOW A
                        symbol['value'] = 1
                    else: IT_variable = 0
                # From NOOB
                elif symbol['type'] == 'NOOB':
                    if (z == "Destination Variable" and len(node.children) in [3,2]):# IS NOW A
                        symbol['value'] = 0
                    else: IT_variable = 0  
                # From NUMBAR, NUMBR
                else:
                    if (z == "Destination Variable" and len(node.children) in [3,2]):# IS NOW A
                        symbol['value'] = int(symbol['value'])
                    else: IT_variable = int(symbol['value'])  
                
                if (z == "Destination Variable" and len(node.children) in [3,2]):# IS NOW A
                    symbol['type'] = target_type
                            
            # TYPECASTING TO NUMBAR
            elif target_type == 'NUMBAR':
                # from YARN
                if symbol['type'] == 'YARN':
                    clean = symbol['value'].strip('\"')
                    try:
                        # Convert to float if possible
                        if (z == "Destination Variable" and len(node.children) in [3,2]):# IS NOW A
                            symbol['value'] = float(clean)
                        else: IT_variable = float(clean)
                    except Exception as e:
                            raise Exception(f"Cannot convert value '{clean}' to NUMBAR")
                # from TROOF
                elif symbol['value'] == 'WIN':
                    if (z == "Destination Variable" and len(node.children) in [3,2]):# IS NOW A
                        symbol['value'] = 1.0
                    else: IT_variable = 1.0
                elif symbol['value'] == 'FAIL':
                    if (z == "Destination Variable" and len(node.children) in [3,2]):# IS NOW A
                        symbol['value'] = 0.0
                    else: IT_variable = 0.0  
                # from NOOB
                elif symbol['type'] == 'NOOB':
                    if (z == "Destination Variable" and len(node.children) in [3,2]):# IS NOW A
                        symbol['value'] = 0.0
                    else: IT_variable = 0.0   
                # From NUMBAR, NUMBR
                else:
                    if (z == "Destination Variable" and len(node.children) in [3,2]):# IS NOW A
                        symbol['value'] = float(symbol['value'])
                    else: IT_variable = float(symbol['value'])  
                if (z == "Destination Variable" and len(node.children) in [3,2]):# IS NOW A
                    symbol['type'] = target_type
                    
                            
            # TYPECASTING TO YARN
            elif target_type == 'YARN':
                if symbol['type'] == 'NOOB':
                    if (z == "Destination Variable" and len(node.children) in [3,2]):# IS NOW A
                        symbol['value'] = '""'
                    else: IT_variable = '""'  
                else:
                    if (z == "Destination Variable" and len(node.children) in [3,2]):# IS NOW A
                        symbol['value'] = str(symbol['value'])
                        if not symbol['value'].startswith('"') and not symbol['value'].endswith('"'): # avoid doubling the quotation marks
                            symbol['value'] = f'"{symbol["value"]}"'
                    else: 
                        IT_variable = str(symbol['value'])
                    # print(IT_variable,str(symbol['value']))
                        if not IT_variable.startswith('"') and not IT_variable.endswith('"'): # avoid doubling the quotation marks
                            IT_variable = f'"{symbol["value"]}"'
                if (z == "Destination Variable" and len(node.children) in [3,2]):# IS NOW A
                    symbol['type'] = target_type
            # TYPECASTING TO TROOF
            elif target_type == 'TROOF':
                if symbol['type'] in 'NOOB' or symbol['value'] == 0 or symbol['value'] == 0.0 or symbol['value'] == '""' or symbol['value'] == 'FAIL':
                    if (z == "Destination Variable" and len(node.children) in [3,2]):# IS NOW A
                        symbol['value'] = 'FAIL'
                    else: IT_variable = 'FAIL'  
                else:
                    if (z == "Destination Variable" and len(node.children) in [3,2]):# IS NOW A
                        symbol['value'] = 'WIN'
                    else: IT_variable = 'WIN'      
                if z == "Destination Variable": # IS NOW A
                        symbol['type'] = target_type           
        if (z == "Destination Variable" and len(node.children) in [3,2]):# IS NOW A
            print(f"{var} is now a {target_type} with the value of {symbol['value']} ")
        else: print(f"The value of {var} is typecasted to {target_type}. IT variable now holds the results with the value of {IT_variable} ")

    # --------------------------------------------------------------------------------------------------------
    # FUNCTION: Anayzle functions (function creation, definition, scoping and execution logic)
    # --------------------------------------------------------------------------------------------------------
    def analyze_function(self, node):
        function_name = node.type
        param_node = next((child for child in node.children if child.type == "Variables"), None)
        body_node = [child for child in node.children if child.type != "Variables" and child.type != "Return"]
        return_node = next((child for child in node.children if child.type == "Return"), None)

        if not function_name:
            raise Exception("Function name is missing.")
        
        if self.symbol_table.lookup(function_name) is not None:
            raise Exception("A function/variable of the same name has already been declared")
            
        
        # Prepare the details of the function
        parameters = [param.value for param in param_node.children]
        returns = [node for node in return_node.children]

        self.symbol_table.add_update_symbol(
            function_name,
            {"type": "Function", "parameters": parameters, "body": body_node, "return": returns}
        )

        # self.log(f"Defined function '{function_name}' with {parameters} and return values of {returns} ")
     
    # --------------------------------------------------------------------------------------------------------
    # FUNCTION: Evaluate function from function call
    # --------------------------------------------------------------------------------------------------------
    def evaluate_function(self, node):
        function_node = node.children
        
        function_name = next((child.value for child in function_node if child.type == "Function Name"), None)
        if not function_name:
            raise Exception("Function name missing in the function call.")
        
        # Retrive the parameters passed in the call
        parameter_node = next((child for child in function_node if child.type == "Parameter"), None)
        call_parameters = [child for child in parameter_node.children] # Can be Literal: 1 or Variable: varname
        
        # Find the function in the symbol table
        function_details = self.symbol_table.lookup(function_name)
        if function_details is None or function_details["type"] != "Function":
            raise Exception(f"Function '{function_name}' is not defined.")
        
        formal_parameters = function_details["parameters"]
        function_body = function_details["body"]
        return_nodes = function_details["return"]

        # Ensure that the number of parameters match
        if len(call_parameters) != len(formal_parameters):
            raise Exception(f"Function {function_name} expects {len(formal_parameters)}, received {len(call_parameters)}")
        
        # Create a new scope for function
        self.symbol_table.enter_scope(function_name)

        # Bind the parameters
        for formal, actual in zip(formal_parameters, call_parameters):
            if actual.type == "Variable":
                value = self.symbol_table.get_value(actual.value)
                value_type = self.symbol_table.lookup(actual.value)["type"]
            elif actual.type == "Operation":
                value, value_type = self.evaluate_arithmetic_operation(actual)
            elif actual.type == "Value":
                value_node = actual
                type_node = type("TypeNode", (), {"value": actual.type})
                value, value_type = self.evaluate_value(value_node, type_node)
            elif actual.type == "Literal":
                value, value_type = actual.value, actual.type
            else:
                raise Exception(f"Unsupported parameter type: {actual.type}")
            
            self.symbol_table.add_update_symbol(formal, {"type": value_type, "value": value})

        #--------------------
        # Execute the function
        
        # self.log(f"Executing function '{function_name}'")
        
        if function_body:
            for body in function_body:
                self.analyze(body)

        return_values = []
        for return_node in return_nodes:
            return_values.append(self.analyze(return_node))

        self.symbol_table.exit_scope()

        # Return the value itself if single, otherwise return a list
        if len(return_values) == 1:
            return return_values[0]
        return return_values


    # --------------------------------------------------------------------------------------------------------
    # FUNCTION: Evaluate function from function call
    # --------------------------------------------------------------------------------------------------------
    def analyze_input(self, node):
        varname = next((child.value for child in node.children if child.type == "Variable"), None)
        if not self.symbol_table.lookup(varname):
            raise Exception("Asking input for undeclared variable")
        
        value, ok = self.request_input("Input", varname)

        if ok:
            self.symbol_table.add_update_symbol(varname, {"type": "YARN", "value": value})
            self.symbol_table.update_IT(value, "YARN")
        else:
            raise Exception("Input operation canceled by the user.")

def analyze_code(lexemes, semantic_analyzer):
    # Connect with syntax_analyzer.py
    syntax_tree = analyze_syntax(lexemes)
    syntax_tree.print_tree()

    # Do semantic analysis
    analyzed_nodes.clear()
    analyzer = semantic_analyzer

    try:
        program_body = next((child for child in syntax_tree.children if child.type == "Program Body"), None)
        functions_node = next((child for child in syntax_tree.children if child.type == "Functions"), None)
        
        # We process the functions block first
        if functions_node:
            for function_node in functions_node.children:
                if function_node not in analyzed_nodes:
                    analyzer.analyze_function(function_node)
                    analyzed_nodes.add(function_node)

        # Process the program body
        if program_body:
            for node in program_body.children:
                if node not in analyzed_nodes:
                    analyzer.analyze(node)

        analyzer.log("Semantic analysis has ended")
        return 
    except Exception as e:
        analyzer.log(f"Semantic error: {e}")