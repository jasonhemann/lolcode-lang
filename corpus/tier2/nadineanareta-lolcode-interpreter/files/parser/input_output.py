from tkinter import simpledialog

# parse visible
def parse_output_keyword(self):
    token = self.current_token()
    current_output = ""
    must_varident = 1

    if token.type == 'Concatenation Keyword':
        self.next_pos()
        self.parse_smoosh(None)
        return 

    while token and token.type != 'NEWLINE':
        # print(f"DEBUG IN OUTPUT: Processing token: {token.type} - {token.value}")
        if must_varident == 1:
            must_varident = 0
            if token.type == 'Identifier':
                if token.value in self.variables:
                    current_output += str(self.variables[token.value])
                    self.next_pos()
                else:
                    raise SyntaxError(f"{self.numline}: in parse_output_keyword(): Undefined variable '{token.value}'")
            elif token.type in ['NUMBAR Literal', 'NUMBR Literal', 'TROOF Literal', 'TYPE Literal', 'Implicit Variable Keyword']:
                current_output += str(token.value)
                self.next_pos()
            elif token.type == 'YARN Delimiter':
                yarn = self.parse_yarn()
                current_output += str(yarn.value)
            elif token.type == 'Arithmetic Operation':
                result = self.parse_arithmetic()
                current_output += str(result)
            elif token.type == 'Boolean Operation':
                value = self.parse_bool()
                result = 'WIN' if value == 1 else 'FAIL'
                current_output += str(result)
            elif token.type == 'Comparison Operation':
                value = self.parse_comparison()
                result = 'WIN' if value == 1 else 'FAIL'
                current_output += str(result)
            else:
                raise SyntaxError(f"{self.numline}: in parse_output_keyword(): Expected a valid variable/expression; Got {token.type} for {token.value}")
        elif must_varident == 0:
            must_varident = 1
            if (token.type == 'Symbol' and token.value == '+') or (token.type == 'And Symbol' and token.value == 'AN'):
                # concatenation
                self.next_pos()
            else:
                break
        else:
            break

        token = self.current_token()
    if self.current_token() and self.current_token().value == '!':
        self.position += 1
        self.suppress = True
    self.variables['IT'] = current_output 
    return 

# parse gimmeh
def parse_input_keyword(self):
    token = self.current_token()
    if token and token.type == 'Identifier':
        if token.value in self.variables:
            input_value = simpledialog.askstring("User Input", f"GIMMEH {token.value}:")
            if input_value is None:
                input_value = ''
            if input_value.isdigit():
                input_value = int(input_value) 
            self.gui.write(input_value)
            self.variables[token.value] = input_value
            self.next_pos()
            if self.gui:
                self.gui.update_symbol_table(self.variables, False, False)
        else:
            raise SyntaxError(f"{self.numline}: in parse_int_keyword(): Undefined variable '{token.value}'")
    else:
        raise SyntaxError(f"{self.numline}: in parse_int_keyword(): Expected valid input variable; Got {token.value}")
