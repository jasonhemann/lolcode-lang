
# parses typecasting
def parse_typecasting(self, var):
    typecasting = self.current_token()

    if typecasting and typecasting.value == 'MAEK A':
        variable = self.get_next_token()
        if variable.value in self.variables:
            a = self.get_next_token()
            if not (a and a.value == 'A'):
                raise SyntaxError(f"{self.numline}: in parse_typecasting(): Expected an 'A'; Got {a.value}")
            
            literal = self.get_next_token()
            if literal and literal.type == 'TYPE Literal':
                if self.variables[variable.value] == 'NOOB':
                    if literal.type in ['TROOF', 'NUMBAR', 'NUMBR']:
                        self.variables[variable.value] = 0
                    elif literal.type == 'YARN':
                        self.variables[variable.value] = ''
                if literal.value == 'TROOF':
                    if self.variables[variable.value] in [0, '']:
                        self.variables[variable.value] = 'FAIL'
                    else:
                        self.variables[variable.value] = 'WIN'
                elif literal.value == 'NUMBAR':
                    self.variables[variable.value] = float(self.variables[variable.value])
                elif literal.value == 'NUMBR':
                    self.variables[variable.value] = int(self.variables[variable.value])
                self.next_pos()
                return
            else:
                raise SyntaxError(f"{self.numline}: in parse_typecasting(): Expected a TYPE Literal; Got {literal.value}")
        else:
            raise SyntaxError(f"{self.numline}: in parse_typecasting(): Expected known variable; Got {variable.value}")
    elif typecasting and typecasting.value == 'IS NOW A':
        literal = self.get_next_token()
        if literal and literal.type == 'TYPE Literal':
            if self.variables[var] == 'NOOB':
                if literal.type in ['TROOF', 'NUMBAR', 'NUMBR']:
                    self.variables[var] = 0
                elif literal.type == 'YARN':
                    self.variables[var] = ''
            if literal.value == 'TROOF':
                if self.variables[var] in [0, '']:
                    self.variables[var] = 'FAIL'
                else:
                    self.variables[var] = 'WIN'
            elif literal.value == 'NUMBAR':
                self.variables[var] = float(self.variables[var])
            elif literal.value == 'NUMBR':
                self.variables[var] = int(self.variables[var])
            self.next_pos()
            return
        else:
            raise SyntaxError(f"{self.numline}: in parse_typecasting(): Expected a TYPE Literal; Got {literal.value}")
    else:
        raise SyntaxError(f"{self.numline}: in parse_typecasting(): Expected valid typecasting keyword; Got {typecasting.value}")
