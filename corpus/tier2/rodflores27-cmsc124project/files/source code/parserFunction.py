import re
from macros import LOLMacros
from decimal import Decimal
import tkinter as tk
from tkinter import simpledialog


class LOLCodeParser:
    def __init__(self, lexer, console):
        self.lexer = lexer
        self.tokens = lexer.get_tokens()
        self.current_token_index = 0
        self.errored = False
        self.macros = LOLMacros()
        # Implicit 'it' variable
        self.it = {'type': 'Untyped', 'value': 'NOOB'}
        self.currentIdentifier = None
        self.variables = dict()
        # Lists of values
        self.literalTypes = [self.macros.NUMBR, self.macros.NUMBAR,
                             self.macros.TROOF, self.macros.YARN]
        self.arithmetic_operators = [self.macros.SUM_OF, self.macros.DIFF_OF, self.macros.PRODUKT_OF,
                                     self.macros.QUOSHUNT_OF, self.macros.MOD_OF, self.macros.BIGGR_OF, self.macros.SMALLR_OF]
        # flag to disable nesting of infinite arity boolean operations
        self.infinite_booling = False
        self.bool_operators = [self.macros.BOTH_OF, self.macros.EITHER_OF,
                               self.macros.WON_OF, self.macros.NOT, self.macros.ANY_OF, self.macros.ALL_OF]
        # flag to disable implicit type-casting of other variable types such as TROOFs
        self.comparing = False
        self.comparison_operators = [
            self.macros.BOTH_SAEM, self.macros.DIFFRINT]

        # for tracing function declarations and calls
        self.functionDeclarations = dict()
        self.functionCalls = dict()

        self.output = ""
        print("Output:", self.output)

        self.console = console

    # start
    def parse(self):
        self.program()

    def match(self, expected_type):
        '''
        Checks if current token matches expected_type, if so, consumes it.
        '''

        if self.current_token().get('type') == expected_type:
            macroNameOfExpectedType = [attr for attr in dir(
                self.macros) if getattr(self.macros, attr) == expected_type][0]
            print(self.current_token().get('type'))
            self.consume_token()
        # find macroName in a list
        elif type(expected_type) == list:
            macroNameOfExpectedType = [attr for attr in dir(
                self.macros) if getattr(self.macros, attr) == expected_type]
            if self.current_token().get('type') in expected_type:
                print(self.current_token().get('value'))
                self.consume_token()
        else:
            print("Current Token: ", self.current_token())
            print(
                f"Syntax Error: Expected {expected_type}: {macroNameOfExpectedType}, but instead found {self.current_token()}")
            self.errored = True

    def current_token(self):
        return self.tokens[self.current_token_index]

    def consume_token(self):
        self.current_token_index += 1

    def program(self):
        # optional function declarations
        while self.current_token().get('type') == self.macros.HOW_IZ_I:
            self.function_declaration()
        
        self.match(self.macros.HAI)

        # Loop over all tokens until KTHXBYE is found
        while not self.current_token().get('type') == 'Program End Delimiter':
            self.statement()  # Parse the next statement

        self.match(self.macros.KTHXBYE)

        if not self.errored:
            print("\nProgram ended cleanly.")
        else:
            print("\nProgram has syntax error.")

    def data_segment(self):
        '''
        Variable Declaration Segment
        '''

        self.match(self.macros.WAZZUP)
        # Optional declaration or initialization of variables
        if self.current_token().get('type') == self.macros.I_HAS_A:
            # Allows multiple declarations
            while self.tokens[self.current_token_index+1].get('type') != self.macros.BUHBYE and self.current_token().get('type') == self.macros.I_HAS_A:
                self.variable_declaration()
        self.match(self.macros.BUHBYE)

    def statement(self):
        print("Statementing... Current token:", self.current_token())
        # printing
        if self.current_token().get('type') == 'Output Operator':
            self.match(self.macros.VISIBLE)
            self.print_statement([], 1)
        # user input
        elif self.current_token().get('type') == "Input Operator":
            self.input_statement()
        # string concatenation
        # elif self.current_token() == "SMOOSH":
        #     self.str_concat()
        # explicit type-casting
        elif self.current_token().get('type') == 'Type Conversion Operator 1':  # MAEK
            self.type_cast()
        # statement starts with identifier
        elif self.current_token().get('type') == "Identifier":
            self.currentIdentifier = self.current_token().get('value')
            # implicitly assign self.it value
            self.it = self.variables[self.currentIdentifier]
            self.match(self.macros.IDENTIFIER)
            # if self.current_token() == 'Type Conversion Operator 3':
            #     self.type_cast()
            if self.current_token().get('type') == "Assignment Operator":
                self.assignment_statement()
        elif self.current_token().get('type') == 'Variable Declaration Start Delimiter':
            self.data_segment()
        # arithmetic operations
        elif self.current_token().get('type') in self.arithmetic_operators:
            self.arithmetic_expr()
            print("arithmetic success")
        # boolean operations
        elif self.current_token().get('type') in self.bool_operators:
            self.bool_expr()
            print("bool success")
        # comparison operations
        elif self.current_token().get('type') in self.comparison_operators:
            self.comparison_expr()
            print("comparison success")
        # if-then statements
        elif self.current_token().get('type') == 'If-Then Statement Start Delimiter':
            self.if_then_statement()
            print("if-then success")
        # switch statements
        elif self.current_token().get('type') == 'Switch Statement Start Delimiter':
            self.switch_statement()
            print("switch statement success")
        # loops
        elif self.current_token().get('type') == 'Loop Statement Start Delimiter':
            self.loop()
            print("loop success")
        # function declaration
        elif self.current_token().get('type') == 'Function Declaration Start Delimiter':
            self.function_declaration()
            print("function declaration success")
        # function call
        elif self.current_token().get('type') == 'Function Call Start Delimiter':
            self.function_call()
            print("function call success")
        else:
            raise ValueError(f"Error: Unrecognized statement found.")

    def variable_declaration(self):
        self.match(self.macros.I_HAS_A)
        if self.current_token().get('type') == self.macros.IDENTIFIER:
            self.currentIdentifier = self.current_token().get('value')
            self.variables[self.currentIdentifier] = {
                'type': 'NOOB', 'value': None}
            self.match(self.macros.IDENTIFIER)
        else:
            raise ValueError(f"Error: variableIdentifier not found.")
        # optional ITZ for initialization
        if self.current_token().get('type') == self.macros.ITZ:
            self.consume_token()
            # add identifier to variables; value is expression
            self.variables[self.currentIdentifier] = self.expression()
        print("Current variables: ", self.variables)

    def print_statement(self, operands, sep):
        separator = sep
        if self.current_token().get('type') == self.macros.SMOOSH:
            self.match(self.macros.SMOOSH)
            separator = 2
        # Operand accumulation for recursion
        operands.append(self.expression())
        print("Print Operands:", operands)

        if separator == 1:
            # infinite arity implementation
            if self.current_token().get('type') == self.macros.PLUS:
                self.match(self.macros.PLUS)
                return self.print_statement(operands, 1)
        else:
            if self.current_token().get('type') == self.macros.AN:
                self.match(self.macros.AN)
                return self.print_statement(operands, 2)

        # setup final string
        string_to_print = ""
        for operand in operands:
            # print NOOB on None values
            if operand.get('value') == None and len(operands) == 1:
                string_to_print += "NOOB"
            else:
                string_to_print += str(operand.get('value'))
        print(string_to_print)  # Don't remove
        self.output += string_to_print + "\n"

    def input_statement(self):
        self.match(self.macros.GIMMEH)
        variable_name = self.current_token().get('value')
        self.match(self.macros.IDENTIFIER)

        # Update the console with the current output
        self.console.config(state="normal")
        self.console.delete('1.0', tk.END)
        self.console.insert(tk.END, self.output)
        self.console.config(state="disabled")

        # Get user input from a dialog box
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        user_input = simpledialog.askstring("Input", "Please enter a value for " + variable_name + ": ")
        root.destroy()
        self.output += user_input + "\n"

        self.variables[variable_name] = {'type': 'YARN', 'value': user_input}
        print("Current variable values:", self.variables)

    def function_declaration(self):
        function_declaration_token_index = self.current_token_index  # to track declaration
        self.match(self.macros.HOW_IZ_I)
        # record indices when functionDeclarations were made
        self.functionDeclarations[self.current_token().get(
            'value')] = function_declaration_token_index
        print("Function Declarations:",
              self.functionDeclarations)
        # skip lines until function_declaration terminator
        while self.current_token().get('type') != self.macros.IF_U_SAY_SO:
            self.consume_token()
        self.match(self.macros.IF_U_SAY_SO)

    def function_call(self):
        '''
            After fetching function_call tokens, current_token_index will jump to functionDeclaration and perform there, then jump back from where the function_call ended
        '''
        self.match(self.macros.I_IZ)
        # setup function call arguments
        function = self.current_token().get('value')  # functionName
        self.match(self.macros.IDENTIFIER)
        # get all arguments
        current_function_arguments = list()
        while self.current_token().get('type') == self.macros.YR:
            self.match(self.macros.YR)
            current_function_arguments.append(self.expression())
            if self.current_token().get('type') == self.macros.AN:
                self.match(self.macros.AN)
        print("Current function name:", function)
        print("Current function arguments:", current_function_arguments)
        self.match(self.macros.MKAY)

        # jump back here after function call
        previous_token_index = self.current_token_index

        # FUNCTION CALL READING DONE
        # Jump to function declaration and perform
        self.current_token_index = self.functionDeclarations[function]
        print("Current index:", self.current_token_index)
        self.match(self.macros.HOW_IZ_I)
        self.match(self.macros.IDENTIFIER)

        argument_index = 0
        local_variables = list()
        while self.current_token().get('type') == self.macros.YR:
            self.match(self.macros.YR)
            # add identifier to variables; identifier value will match the argument
            local_variables.append(self.current_token().get('value'))
            print("Local variables:", local_variables)
            self.variables[self.current_token().get(
                'value')] = current_function_arguments[argument_index]  # e.g. formalX = actualX
            argument_index += 1
            print("Current variables (on function):", self.variables)
            self.match(self.macros.IDENTIFIER)
            if self.current_token().get('type') == self.macros.AN:
                self.match(self.macros.AN)

        # setup it
        self.it['type'] = 'Untyped'
        self.it['value'] = 'NOOB'
        while self.current_token().get('type') not in (self.macros.FOUND_YR, self.macros.GTFO, self.macros.IF_U_SAY_SO):
            self.statement()
        # return statement
        if self.current_token().get('type') == self.macros.FOUND_YR:
            self.match(self.macros.FOUND_YR)
            self.it = self.expression()
        # break statement
        elif self.current_token().get('type') == self.macros.GTFO:
            self.match(self.macros.GTFO)

        self.match(self.macros.IF_U_SAY_SO)
        # remove local variables in self.variables
        for variable in local_variables:
            del self.variables[variable]
        # return to previous program counter
        self.current_token_index = previous_token_index

    def loop(self):
        self.match(self.macros.IM_IN_YR)
        # store current loop Identifier
        self.currentLoop = self.current_token().get('value')  # name of loop identifier
        print("Current loop:", self.currentLoop)
        self.match(self.macros.IDENTIFIER)
        # Set IncrementType
        loopIncrementType = None
        if self.current_token().get('type') == self.macros.NERFIN:
            loopIncrementType = 'NERFIN'
        elif self.current_token().get('type') == self.macros.UPPIN:
            loopIncrementType = 'UPPIN'
        self.match([self.macros.NERFIN, self.macros.UPPIN])
        self.match(self.macros.YR)
        # set loop counter aka the value that will be incremented/decremented
        loopCounter = self.current_token().get(
            'value')  # get the name of the identifier
        # NOTE: remove if needed loopCounter variable to have value from previous loop
        # assign initial value to reset loopCounter variable in global scope after loop
        # loopCounterInitialValue = self.variables[loopCounter]['value']
        self.match(self.macros.IDENTIFIER)
        # set loop delimiter aka loop type
        loopConditionDelimiter = self.current_token().get('value')
        self.match([self.macros.TIL, self.macros.WILE])
        # condition
        indexOnCondition = self.current_token_index
        # TIL
        if loopConditionDelimiter == 'TIL':
            # while FAIL
            while self.expression().get('value') in (False, 'FAIL'):
                # run statements inside loop
                while self.current_token().get('type') not in (self.macros.IM_OUTTA_YR, self.macros.GTFO):
                    self.statement()
                # update loop-related variables
                if self.current_token().get('type') == self.macros.IM_OUTTA_YR:
                    if loopIncrementType == 'UPPIN':
                        self.variables[loopCounter]['value'] += 1
                    elif loopIncrementType == 'NERFIN':
                        self.variables[loopCounter]['value'] -= 1
                    # return token_index to where condition was
                    self.current_token_index = indexOnCondition
                elif self.current_token().get('type') == self.macros.GTFO:
                    self.match(self.macros.GTFO)
                    break
            # once the condition is True or GTFO is met, skip all line until IM_OUTTA_YR
            while self.current_token().get('type') != self.macros.IM_OUTTA_YR:
                self.consume_token()
        # WILE
        if loopConditionDelimiter == 'WILE':
            # while WIN
            while self.expression().get('value') in (True, 'WIN'):
                # run statements inside loop
                while self.current_token().get('type') not in (self.macros.IM_OUTTA_YR, self.macros.GTFO):
                    self.statement()
                # update loop-related variables
                if self.current_token().get('type') == self.macros.IM_OUTTA_YR:
                    if loopIncrementType == 'UPPIN':
                        self.variables[loopCounter]['value'] += 1
                    elif loopIncrementType == 'NERFIN':
                        self.variables[loopCounter]['value'] -= 1
                    # return token_index to where condition was
                    self.current_token_index = indexOnCondition
                elif self.current_token().get('type') == self.macros.GTFO:
                    self.match(self.macros.GTFO)
                    break
            # once the condition is False or GTFO is met, skip all line until IM_OUTTA_YR
            while self.current_token().get('type') != self.macros.IM_OUTTA_YR:
                self.consume_token()
        self.match(self.macros.IM_OUTTA_YR)
        # end of loop
        if self.current_token().get('value') == self.currentLoop:
            self.match(self.macros.IDENTIFIER)
        else:
            raise SyntaxError(
                f"Unexpected token in statement: {self.current_token()}. Expecting current loop identifier.")
        # NOTE: remove if needed loopCounter variable to have value from previous loop
        # reset loopCounter variable
        # self.variables[loopCounter]['value'] = loopCounterInitialValue

    def switch_statement(self):
        self.match(self.macros.WTF)
        print(self.current_token().get('value'))

        # optional switch cases
        # Flag for keeping execution of statements until GTFO or OIC is met
        self.switch_case_skipped_GTFO = False
        while self.current_token().get('type') != self.macros.OIC:
            self.switch_case()

        # end of switch statement
        self.match(self.macros.OIC)

    def switch_case(self):
        case = None
        if self.current_token().get('type') == self.macros.OMG:
            self.match(self.macros.OMG)
            case = self.expression().get('value')
            it_value = self.it.get('value')
            print("Case:", case)
            print("IT:", it_value)
            try:
                # integer cast-able strings
                if it_value.isnumeric():
                    it_value = int(it_value)
                # float cast-able strings
                else:
                    it_value = float(it_value)
            except:
                pass
            # usual case
            if case == it_value and not self.switch_case_skipped_GTFO:
                # keep parsing statements
                while self.current_token().get('type') not in (self.macros.GTFO, self.macros.OMG, self.macros.OMGWTF, self.macros.OIC):
                    self.statement()  # Parse the next statement
                # break statement
                if self.current_token().get('type') == self.macros.GTFO:
                    self.match(self.macros.GTFO)
                    # skip the rest of the cases
                    while self.current_token().get('type') != (self.macros.OIC):
                        self.consume_token()
                # break not found
                if self.current_token().get('type') in (self.macros.OMG, self.macros.OMGWTF):
                    self.switch_case_skipped_GTFO = True
                    return

            # special case where break is not found but there are still succeeding cases
            elif self.switch_case_skipped_GTFO:
                while self.current_token().get('type') not in (self.macros.OMG, self.macros.OMGWTF, self.macros.GTFO):
                    self.statement()
                if self.current_token().get('type') == self.macros.GTFO:
                    self.match(self.macros.GTFO)
                    while self.current_token().get('type') != (self.macros.OIC):
                        self.consume_token()

            # case != IT, skip rest of lines until next case
            else:
                while self.current_token().get('type') not in (self.macros.OMG, self.macros.OMGWTF):
                    self.consume_token()

        # optional OMGWTF aka default case
        elif self.current_token().get('type') == self.macros.OMGWTF:
            self.match(self.macros.OMGWTF)
            while self.current_token().get('type') != self.macros.OIC:
                self.statement()  # Parse the next statement

    def if_then_statement(self):
        self.match(self.macros.O_RLY)

        # IT value should be truthy
        if self.it.get('value'):
            # start if clause
            self.match(self.macros.YA_RLY)
            # keep parsing statements until NO WAI is met
            while not self.current_token().get('type') in (self.macros.NO_WAI, self.macros.OIC):
                self.statement()  # Parse the next statement
            # optional else statement
            if self.current_token().get('type') == self.macros.NO_WAI:
                self.match(self.macros.NO_WAI)
                while not self.current_token().get('type') == self.macros.OIC:
                    self.statement()  # Parse the next statement
            self.match(self.macros.OIC)
        # IT value is not truthy
        else:
            while self.current_token().get('type') != self.macros.OIC:
                self.consume_token()
            self.match(self.macros.OIC)

    def expression(self):
        tokenType = None

        # literal return value
        if (self.current_token().get('type') in self.literalTypes):
            tokenType = self.current_token().get('type')

            if tokenType == 'NUMBR':
                tokenValue = int(self.current_token().get('value'))
            elif tokenType == 'NUMBAR':
                tokenValue = float(self.current_token().get('value'))
            # string
            else:
                tokenValue = self.current_token().get('value')

            self.match(tokenType)

        # identifier return value
        elif (self.current_token().get('type') == 'Identifier'):
            # implicit IT variable
            if self.current_token().get('value') == 'IT':
                tokenType = self.it.get('type')
                tokenValue = self.it.get('value')
            else:
                tokenType = self.variables[self.current_token().get(
                    'value')].get('type')
                tokenValue = self.variables[self.current_token().get(
                    'value')].get('value')
            self.match('Identifier')

        # arithmetic expression return value
        elif (self.current_token().get('type') in self.arithmetic_operators):
            self.arithmetic_expr()
            tokenType = self.it.get('type')
            tokenValue = self.it.get('value')
        # bool expression return value
        elif (self.current_token().get('type') in self.bool_operators):
            self.bool_expr()
            tokenType = self.it.get('type')
            tokenValue = self.it.get('value')
        # comparison expression return value
        elif (self.current_token().get('type') in self.comparison_operators):
            self.comparison_expr()
            tokenType = self.it.get('type')
            tokenValue = self.it.get('value')
        # function call return value
        elif self.current_token().get('type') == self.macros.I_IZ:
            self.function_call()
            tokenType = self.it.get('type')
            tokenValue = self.it.get('value')
        else:
            raise SyntaxError(
                f"Unexpected token in expression: {self.current_token()}. Expecting literal, variable, or expression")
        return {'type': tokenType, 'value': tokenValue}

    def fetchOperand(self):
        '''
        Fetches an operand
        '''
        operand = None

        # int literal
        if self.current_token().get('type') == self.macros.NUMBR:
            operand = int(self.current_token().get('value'))
            self.consume_token()
        # float literal
        elif self.current_token().get('type') == self.macros.NUMBAR:
            operand = float(self.current_token().get('value'))
            self.consume_token()
        # identifier aka variable
        elif self.current_token().get('type') == 'Identifier':
            tokenValue = self.variables[self.current_token().get(
                'value')].get('value')
            # typecast
            if type(tokenValue) == str:
                try:
                    # integer cast-able strings
                    if tokenValue.isnumeric():
                        tokenValue = int(tokenValue)
                    # float cast-able strings
                    else:
                        tokenValue = float(tokenValue)
                except:
                    if self.comparing == True:
                        raise SyntaxError(
                            f"Invalid token for comparison expression: {tokenValue}. Automatic Typecasting is disabled.")
                    # TODO: put appropriate error message here.
                    pass
            operand = tokenValue
            self.match('Identifier')
        # string literal
        elif self.current_token().get('type') == 'YARN':
            token = self.current_token()
            print("YARN token:", token)
            tokenValue = self.current_token().get('value')
            # typecast
            try:
                # integer cast-able strings
                if tokenValue.isnumeric():
                    tokenValue = int(tokenValue)
                # float cast-able strings
                else:
                    tokenValue = float(tokenValue)
            except:
                if self.comparing == True:
                    raise SyntaxError(
                        f"Invalid token for comparison expression: {self.current_token()}. Automatic Typecasting is disabled.")
                # TODO: put appropriate error message here.
                pass
            operand = tokenValue
            self.match('YARN')
        # troof aka boolean
        elif self.current_token().get('type') == 'TROOF':
            if self.comparing == True:
                raise SyntaxError(
                    f"Invalid token for comparison expression: {self.current_token()}. Automatic Typecasting is disabled.")
            # set to 1 or 0 to be used on evaluating expressions
            operand = 1 if self.current_token().get('value') == 'WIN' else 0
            self.match(self.macros.TROOF)
        # arithmetic_expr
        elif self.current_token().get('type') in self.arithmetic_operators:
            operand = self.arithmetic_expr()
        # bool_expr
        elif self.current_token().get('type') in self.bool_operators:
            operand = self.bool_expr()
        else:
            raise SyntaxError(
                f"Unexpected token in expression: {self.current_token()}.")

        return operand

    def arithmetic_expr(self):
        operator = self.arithmetic_operator().get('type')

        operand1 = self.fetchOperand()
        self.match(self.macros.AN)
        operand2 = self.fetchOperand()

        print("Operand 1:", operand1)
        print("Operand 2:", operand2)

        answer = None
        if operator == 'Addition Operator':
            # Perform action for addition operator
            answer = operand1 + operand2
        elif operator == 'Subtraction Operator':
            # Perform action for subtraction operator
            answer = operand1 - operand2
        elif operator == 'Multiplication Operator':
            # Perform action for multiplication operator
            answer = operand1 * operand2
        elif operator == 'Division Operator':
            # Perform action for division operator
            if operand2 != 0:
                answer = operand1 / operand2
            else:
                raise ZeroDivisionError("Division by zero")
        elif operator == 'Modulo Operator':
            # Perform action for modulo operator
            answer = operand1 % operand2
        elif operator == 'Max Operator':
            # Perform action for Max operator
            answer = max(operand1, operand2)
        elif operator == 'Min Operator':
            # Perform action for Min operator
            answer = min(operand1, operand2)

        # assign value for implicit variable self.it
        self.it['value'] = answer

        # assign type of self.it
        if isinstance(answer, (int)):
            self.it['type'] = 'NUMBR'

        elif isinstance(answer, (float)):
            self.it['type'] = 'NUMBAR'

        print("Implicit IT variable: ", self.it)

        return answer

    def arithmetic_operator(self):
        tokenType = None
        tokenValue = None
        if (self.current_token().get('type') in self.arithmetic_operators):
            tokenType = self.current_token().get('type')
            tokenValue = self.current_token().get('value')
            self.match(tokenType)
        else:
            raise SyntaxError(
                f"Unexpected token in expression: {self.current_token()}. Expecting arithmetic operator")
        return {'type': tokenType, 'value': tokenValue}

    def str_concat(self):
        strings_to_concat = []
        final_string = ""
        while True:
            if self.current_token().get('type') == 'YARN':
                strings_to_concat.append(self.current_token().get('value'))
                self.match(self.macros.YARN)
                if self.current_token().get('type') == 'Operand Connector':
                    self.match(self.macros.AN)
                    continue
                else:
                    break
            elif self.current_token().get('type') == 'Identifier':
                strings_to_concat.append(
                    self.variables[self.current_token().get('value')].get('value'))
                self.match(self.macros.IDENTIFIER)
                if self.current_token().get('type') == 'Operand Connector':
                    self.match(self.macros.AN)
                    continue
                else:
                    break
            else:
                print(
                    f"Syntax Error: Expected string or identifier, but instead found {self.current_token()}")
                break
        print('STR_CONCAT - ', strings_to_concat)
        for string in strings_to_concat:
            final_string += str(string)
        print(final_string)
        return final_string

    def assignment_statement(self):
        # R followed by an expression
        self.match(self.macros.R)
        if self.current_token().get('type') == 'String Concatenation Operator':
            self.match(self.macros.SMOOSH)
            value = self.str_concat()
            self.variables[self.currentIdentifier]['value'] = value
            self.variables[self.currentIdentifier]['type'] = 'YARN'
        else:
            self.variables[self.currentIdentifier] = self.expression()
        print("Current variables: ", self.variables)

    def type_cast(self):
        # TODO: typecasting using IS_NOW_A

        # MAEK
        if self.current_token().get('type') == self.macros.MAEK:
            self.match(self.macros.MAEK)
            self.currentIdentifier = self.current_token().get('value')
            self.match(self.macros.IDENTIFIER)
            # optional "A"
            if self.current_token().get('type') == self.macros.A:
                self.match(self.macros.A)
            type_to_cast = self.current_token().get('value')
            # self.match(self.literalTypes)
            # print("here")
            self.match(self.macros.TYPE)

            # TODO: NOOB, int, float, string, bool
            # typecast to string
            if type_to_cast == 'YARN':
                if self.variables[self.currentIdentifier]['value'] == None:
                    raise SyntaxError(
                        f"Cannot typecast NOOB to YARN")
                self.variables[self.currentIdentifier]['type'] = 'YARN'
                self.variables[self.currentIdentifier]['value'] = str(
                    self.variables[self.currentIdentifier]['value'])
            # numbr
            if type_to_cast == 'NUMBR':
                value = self.variables[self.currentIdentifier]['value']
                print("value", value)
                if type(value) == str:
                    try:
                        # integer cast-able strings
                        if value.isnumeric():
                            value = int(value)
                        # float cast-able strings
                        else:
                            value = float(value)
                    except:
                        pass
                    self.variables[self.currentIdentifier]['value'] = value
                else:
                    self.variables[self.currentIdentifier]['value'] = int(
                        self.variables[self.currentIdentifier]['value'])

                self.variables[self.currentIdentifier]['type'] = 'NUMBR'

            # numbar
            if type_to_cast == 'NUMBAR':
                self.variables[self.currentIdentifier]['type'] = 'NUMBAR'
                self.variables[self.currentIdentifier]['value'] = float(
                    self.variables[self.currentIdentifier]['value'])
            # troof
            if type_to_cast == 'TROOF':
                self.variables[self.currentIdentifier]['type'] = 'TROOF'
                value = self.variables[self.currentIdentifier]['value']
                cast = bool(
                    self.variables[self.currentIdentifier]['value'])
                if cast == True and value != 'FAIL':
                    self.variables[self.currentIdentifier]['value'] = 'WIN'
                else:
                    self.variables[self.currentIdentifier]['value'] = 'FAIL'

            print("Current variables: ", self.variables)
        # varident IS_NOW_A
        # elif self.current_token().get('type') == self.macros.IS_NOW_A:
        #     self.match(self.macros.IS_NOW_A)
        #     self.match(self.literalTypes)

    def bool_expr(self):
        operator = self.bool_operator().get('type')

        # Not operator -> single arity
        if operator == self.macros.NOT:
            operand = self.fetchOperand()
            print("Operand for NOT:", operand)
            # Perform action for NOT operator
            if operand == 'FAIL':
                answer = 'WIN'
            else:
                answer = 'FAIL'

        # Binary arity bool operators
        elif operator in [self.macros.BOTH_OF, self.macros.EITHER_OF, self.macros, self.macros.WON_OF]:
            operand1 = self.fetchOperand()
            self.match(self.macros.AN)
            operand2 = self.fetchOperand()

            print("Operand 1:", operand1)
            print("Operand 2:", operand2)

            answer = None
            # booleans can make use of Troofs or 0's and 1's
            if operator == 'Logical AND Operator':
                # Perform action for AND operator
                if operand1 in (1, 'WIN') and operand2 in (1, 'WIN'):
                    answer = 'WIN'
                else:
                    answer = 'FAIL'

            elif operator == 'Logical OR Operator':
                # Perform action for OR operator
                if operand1 in (1, 'WIN') or operand2 in (1, 'WIN'):
                    answer = 'WIN'
                else:
                    answer = 'FAIL'

            elif operator == 'Logical XOR Operator':
                # Perform action for XOR operator
                operand1_bool = operand1 in (1, 'WIN')
                operand2_bool = operand2 in (1, 'WIN')

                if operand1_bool ^ operand2_bool:  # XOR operation
                    answer = 'WIN'
                else:
                    answer = 'FAIL'
        # Infinite arity bool operators
        elif (operator in [self.macros.ANY_OF, self.macros.ALL_OF]) and not self.infinite_booling:
            # To disable having an argument that's an infinite arity bool as well
            self.infinite_booling = True
            first_operand = self.fetchOperand()
            operands = [first_operand]
            # infinite arity implementation
            while self.current_token().get('type') == self.macros.AN:
                self.match(self.macros.AN)
                operands.append(self.fetchOperand())
            print("Operands:", operands)

            # statement terminator
            self.match(self.macros.MKAY)

            if operator == 'Infinite Arity Logical OR Operator':
                # Perform action for OR operator
                answer = any((operand != 'FAIL' and operand != 0)
                             for operand in operands)

            elif operator == 'Infinite Arity Logical AND Operator':
                # Perform action for AND operator
                answer = all((operand != 'FAIL' and operand !=
                             0) for operand in operands)
            self.infinite_booling = False

        # assign values for implicit variable self.it
        self.it['type'] = 'TROOF'
        if answer == True or answer == 'WIN':
            self.it['value'] = 'WIN'
        elif answer == False or answer == 'FAIL':
            self.it['value'] = 'FAIL'

        print("Implicit IT variable:", self.it)
        print("Current variables:", self.variables)
        return answer

    def bool_operator(self):
        '''
            fetch bool_operator
        '''
        tokenType = None
        tokenValue = None
        if (self.current_token().get('type') in self.bool_operators):
            tokenType = self.current_token().get('type')
            tokenValue = self.current_token().get('value')
            self.match(tokenType)
        else:
            raise SyntaxError(
                f"Unexpected token in expression: {self.current_token()}. Expecting bool operator")
        return {'type': tokenType, 'value': tokenValue}

    def comparison_expr(self):
        # flag to enable/disable implicit typecasting on some expressions when comparing
        self.comparing = True
        operator = self.comparison_operator().get('type')
        print("Operation:", operator)

        operand1 = self.fetchOperand()
        self.comparing = False
        self.match(self.macros.AN)
        operand2 = self.fetchOperand()
        self.comparing = False

        print("Operand 1:", operand1)
        print("Operand 2:", operand2)

        answer = None
        if operator == 'Equality Operator':
            # Perform action for equality operator
            answer = operand1 == operand2
        elif operator == 'Inequality Operator':
            # Perform action for inequality operator
            answer = operand1 != operand2

        self.comparing = False

        # assign values for implicit variable self.it
        self.it['type'] = 'TROOF'
        self.it['value'] = answer
        print("Implicit IT variable: ", self.it)

        return answer

    def comparison_operator(self):
        '''
            fetch comparison operator
        '''
        tokenType = None
        tokenValue = None
        if (self.current_token().get('type') in self.comparison_operators):
            tokenType = self.current_token().get('type')
            tokenValue = self.current_token().get('value')
            self.match(tokenType)
        else:
            raise SyntaxError(
                f"Unexpected token in expression: {self.current_token()}. Expecting comparison operator")
        return {'type': tokenType, 'value': tokenValue}
