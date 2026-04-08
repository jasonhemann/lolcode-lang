# parse yarn
def parse_yarn(self):
    self.next_pos()
    yarn = self.current_token()
    if yarn and yarn.type == 'YARN Literal':
        if ':)' in yarn.value:
            yarn.value = yarn.value.replace(':)', '\n')
        elif ':>' in yarn.value:
            yarn.value = yarn.value.replace(':>', '\t')
        elif ':o' in yarn.value:
            yarn.value = yarn.value.replace(':o', '\a')
        elif ':"' in yarn.value:
            yarn.value = yarn.value.replace(':"', '"')
        elif '::' in yarn.value:
            yarn.value = yarn.value.replace('::', ':')

        self.next_pos()
        token = self.current_token()
        if token and token.type == 'YARN Delimiter':
            self.next_pos()
            return yarn
        else:
            raise SyntaxError(f"{self.numline}: in parse_yarn(): Expected YARN Delimiter")
    elif yarn and yarn.type == 'YARN Delimiter': # empty string
        return ""
    else:
        raise SyntaxError(f"{self.numline}: in parse_yarn(): Expected valid YARN Literal")

# parse string concatenation
def parse_smoosh(self, value):
    token = self.current_token()
    current_output = ""
    must_varident = 1

    while token and token.type != 'NEWLINE':
        if must_varident == 1:
            must_varident = 0
            if token.type == 'Identifier':
                if token.value in self.variables:
                    current_output += str(self.variables[token.value])
                    self.next_pos()
                else:
                    raise SyntaxError(f"{self.numline}: in parse_smoosh(): Undefined variable '{token.value}'")
            elif token.type in ['NUMBAR Literal', 'NUMBR Literal', 'TROOF Literal', 'TYPE Literal']:
                current_output += str(token.value)
                self.next_pos()
            elif token.type == 'YARN Delimiter':
                yarn = self.parse_yarn()
                current_output += str(yarn.value)
            elif token.type == 'Arithmetic Operation':
                result = self.parse_arithmetic()
                current_output += str(result)
            else:
                raise SyntaxError(f"{self.numline}: in parse_smoosh(): Expected a valid variable; Got {token.type} for {token.value}")
        elif must_varident == 0:
            must_varident = 1
            if token.type == 'And Symbol' and token.value == 'AN':
                # concatenation
                self.next_pos()
            elif token.type == 'Boolean Operation':
                result = self.parse_bool()
            else:
                break
        else:
            # raise SyntaxError(f"{self.numline}: Unexpected token '{token.value}' in output statement")
            break

        token = self.current_token()
    
    if self.current_token() and self.current_token().value == '!':
        self.suppress = True
        self.position += 1
    
    if value is None:
        self.variables['IT'] = current_output 
        return
    self.variables[value] = current_output 
    return 