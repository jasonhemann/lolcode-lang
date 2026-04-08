from gui import *

# parses varialbe declaration block
def parse_variable_declaration_block(self):
    token = self.current_token()

    # parses each variable declaration
    while token and not (token.type == 'Variable Declaration Delimiter' and token.value == 'BUHBYE'):
        self.parse_variable_declaration()
        token = self.current_token()

    # checks if it has delimiter
    if token and token.type == 'Variable Declaration Delimiter' and token.value == 'BUHBYE':
        self.next_pos()
    else:
        raise SyntaxError(f"{self.numline}: in parse_variable_declaration_block(): Expected 'BUHBYE' to close variable declarations; Got {token.value}")
 
# parse variable declaration
def parse_variable_declaration(self):
    token = self.current_token()
    if token.type == 'Variable Declaration' and token.value == 'I HAS A':
        var = self.get_next_token()

        if var and var.type == 'Identifier':
            token = self.get_next_token()

            # I HAS A varident ITZ value
            if token.type == 'Variable Initialization' and token.value == 'ITZ':
                val = self.get_next_token()
                if val and val.type in ['NUMBAR Literal', 'NUMBR Literal', 'TROOF Literal', 'TYPE Literal']:
                    if val.type == 'NUMBAR Literal':
                        val.value = float(val.value)
                    if val.type == 'NUMBR Literal':
                        val.value = int(val.value)
                    self.variables[var.value] = val.value
                    self.next_pos()
                elif val and val.type == 'YARN Delimiter':
                    yarn = self.parse_yarn()
                    self.variables[var.value] = yarn.value
                elif val and val.type == 'Arithmetic Operation':
                    self.variables[var.value] = self.parse_arithmetic()
                else:
                    raise SyntaxError(f"{self.numline}: in parse_variable_declaration(): Expected a valid value after 'ITZ'; Got {val.value}")
            # I HAS A varident
            else:
                self.variables[var.value] = 'NOOB'
                return
            
            if self.gui:
                self.gui.update_symbol_table(self.variables, False, False)

        else:
            raise SyntaxError(f"{self.numline}: in parse_variable_declaration(): Expected variable identifier after 'I HAS A'; Got {var.value}")
    else:
        raise SyntaxError(f"{self.numline}: in parse_variable_declaration(): Expected a valid variable declaration; Got {token.value}")

# parses variable assignment
def parse_variable_assignment(self, variable):
    keyword = self.current_token()

    if keyword:
        if keyword.type == 'Assignment Operation Keyword' and keyword.value == 'R':
            token = self.get_next_token()
            if token.type in ['Identifier', 'NUMBAR Literal', 'NUMBR Literal', 'YARN Delimiter', 'TROOF Literal']:
                result = self.parse_expression()
                self.variables[variable.value] = result
            elif token.type == 'Concatenation Keyword' and token.value == 'SMOOSH':
                self.next_pos()
                self.parse_smoosh(variable.value)
            elif token.type == 'Typecasting Keyword' and token.value == 'MAEK A':
                self.parse_typecasting(variable.value)
            else:
                raise SyntaxError(f"{self.numline}: in parse_variable_assignment(): Expected a valid variable or expression; Got {token.value}")
        elif keyword.type == 'Typecasting Keyword':
            self.parse_typecasting(variable.value)
    else:
        raise SyntaxError(f"{self.numline}: in parse_variable_assignment(): Expected a valid keyword; Got {token.value}")
