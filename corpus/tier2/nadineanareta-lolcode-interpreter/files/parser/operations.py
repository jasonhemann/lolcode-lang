# parse arithmetic operation
# TODO: if YARN is valid number value, cast to number
def parse_arithmetic(self):
    oper = self.current_token()
    if oper.value not in ['SUM OF', 'DIFF OF', 'PRODUKT OF', 'QUOSHUNT OF', 'MOD OF', 'BIGGR OF', 'SMALLR OF']:
        raise SyntaxError(f"{self.numline}: in parse_arithmetic(): Expected a valid arithmetic expression; Got {oper.value}")
    
    self.next_pos()
    operand1 = self.parse_expression()

    token = self.current_token()
    if not token or token.value != 'AN':
        raise SyntaxError(f"{self.numline}: in parse_arithmetic(): Expected a valid keyword or expression; Got {token.value}")

    self.next_pos()
    operand2 = self.parse_expression()

    if operand1 is None or operand2 is None:
        raise TypeError(f"{self.numline}: in parse_arithmetic(): Operands for {oper.value} must not be None (operand1={operand1}, operand2={operand2})")

    # performs the operation
    # -- not in syntax pero in-advance ko na in case
    if oper.value == 'SUM OF':
        return operand1 + operand2
    elif oper.value == 'DIFF OF':
        return operand1 - operand2
    elif oper.value == 'PRODUKT OF':
        return operand1 * operand2
    elif oper.value == 'QUOSHUNT OF':
        if operand2 == 0:
            raise ZeroDivisionError(f"{self.numline}: in parse_arithmetic(): Division by zero in 'QUOSHUNT OF'")
        if isinstance(operand1, int) and isinstance(operand2, int):
            return operand1 // operand2
        return operand1/operand2
    elif oper.value == 'MOD OF':
        if operand2 == 0:
            raise ZeroDivisionError(f"{self.numline}: in parse_arithmetic(): Division by zero in 'MOD OF'")
        return operand1%operand2
    elif oper.value == 'BIGGR OF':
        return max(operand1, operand2)
    elif oper.value == 'SMALLR OF':
        return min(operand1, operand2)

# parses expression in arithmetic operation
def parse_expression(self):
    token = self.current_token()

    if token.type in ['NUMBAR Literal', 'NUMBR Literal']:
        self.next_pos()
        return float(token.value) if token.type == 'NUMBAR Literal' else int(token.value)
    elif token.type == 'Identifier':
        self.next_pos()

        if token.value in self.variables:
            if self.variables[token.value] == 'NOOB':
                return 0
            return self.variables[token.value]
        else:
            raise SyntaxError(f"{self.numline}: in parse_expression(): Undefined variable '{token.value}'")
    elif token.type == 'YARN Delimiter':
        yarn = self.parse_yarn()
        try:
            return int(yarn.value) if yarn.value.isdigit() else float(yarn.value)
        except ValueError:
            raise TypeError(f"{self.numline}: in parse_expression(): Expected a valid numeric value '{yarn.value}' in YARN Literal")
    elif token.type == 'TROOF Literal':
        value = 1 if token.value == 'WIN' else 0
        self.next_pos()
        return value
    elif token.type == 'Arithmetic Operation':
        return self.parse_arithmetic()
    elif token.type == 'Boolean Operation':
        return self.parse_bool()
    elif token.type == 'Comparison Operation':
        return self.parse_comparison()
    else:
        raise SyntaxError(f"{self.numline}: in parse_expression(): Expected a valid expression; Got {token.value}")

# parses bool operation
def parse_bool(self):
    oper = self.current_token()
    if oper.value not in ['BOTH OF', 'EITHER OF', 'WON OF', 'NOT', 'ALL OF', 'ANY OF', 'WIN', 'FAIL']:
        raise SyntaxError(f"{self.numline}: in parse_bool(): Expected a valid boolean expression; Got {oper.value}")
    
    self.next_pos()
    operand1 = self.current_token()

    if operand1.type not in ['Identifier', 'Boolean Operation', 'And Symbol', 'NUMBR Literal', 'NUMBAR Literal']:
        raise SyntaxError(f"{self.numline}: in parse_bool(): Expected a valid boolean operand; Got {oper.value}")
    operand1 = self.parse_expression()
    
    if oper.value == 'NOT':
        if operand1 > 0:
            return 0
        else:
            return 1

    if oper.value == 'ALL OF':
        value = 1
        op = self.current_token()
        while op.type != 'Delimiter' and op.value != 'MKAY':
            if op.type in ['Identifier', 'Boolean Operation', 'NUMBR Literal', 'NUMBAR Literal']:
                op = self.parse_expression()
                if op == 0:
                    value = 0
                op = self.current_token()
            elif op.type == 'And Symbol':
                op = self.get_next_token()
            else:
                raise SyntaxError(f"{self.numline}: in parse_bool(): expected valid operand type inside ALL clause; Got {op.type}")
        self.next_pos()
        return value

    if oper.value == 'ANY OF':
        value = 0
        op = self.current_token()
        while op.type != 'Delimiter' and op.value != 'MKAY':
            if op.type in ['Identifier', 'Boolean Operation', 'NUMBR Literal', 'NUMBAR Literal']:
                op = self.parse_expression()
                if op > 0:
                    value = 1
                op = self.current_token()
            elif op.type == 'And Symbol':
                op = self.get_next_token()
            else:
                raise SyntaxError(f"{self.numline}: in parse_bool(): expected valid operand type inside ANY clause; Got {op.type}")
        self.next_pos()
        return value
    
    token = self.current_token()
    if not token or token.value != 'AN':
        raise SyntaxError(f"{self.numline}: in parse_bool(): Expected a valid keyword or expression; Got {token.value}")

    self.next_pos()
    operand2 = self.current_token()
    if operand2.type not in ['Identifier', 'Boolean Operation', 'And Symbol', 'NUMBR Literal', 'NUMBAR Literal']:
        raise SyntaxError(f"{self.numline}: in parse_bool(): Expected a valid boolean operand; Got {oper.value}")
    operand2 = self.parse_expression()

    if operand1 == 'NOOB':
        operand1 = 0
    if operand2 == 'NOOB':
        operand2 = 0

    if oper.value == 'BOTH OF':
        if operand1 > 0 and operand2 > 0:
            return 1
        else:
            return 0
    elif oper.value == 'EITHER OF':
        if operand1 > 0 or operand2 > 0:
            return 1
        else:
            return 0
    elif oper.value == 'WON OF':
        if (operand1 > 0 and operand2 == 0) or (operand1 == 0 and operand2 > 0):
            return 1
        else:
            return 0
    
# parse comparison
def parse_comparison(self):
    oper = self.current_token()
    if oper.value not in ['BOTH SAEM', 'DIFFRINT']:
        raise SyntaxError(f"{self.numline}: in parse_comparison(): Expected a valid comparison expression; Got {oper.value}")
    
    self.next_pos()
    operand1 = int(self.parse_expression())

    token = self.current_token()
    if not token or token.value != 'AN':
        raise SyntaxError(f"{self.numline}: in parse_comparison(): Expected a valid keyword or expression; Got {token.value}")

    self.next_pos()
    operand2 = int(self.parse_expression())

    if operand1 is None or operand2 is None:
        raise TypeError(f"{self.numline}: in parse_comparison(): Operands for {oper.value} must not be None (operand1={operand1}, operand2={operand2})")
    
    if oper.value == 'BOTH SAEM':
        if operand1 == operand2:
            self.variables['IT'] = 1
            return 1
        else:
            self.variables['IT'] = 0 
            return 0
    elif oper.value == 'DIFFRINT':
        if operand1 != operand2:
            self.variables['IT'] = 1
            return 1
        else:
            self.variables['IT'] = 0
            return 0
    else:
        raise SyntaxError(f"{self.numline}: in parse_comparison(): Expected a valid comparison expression; Got {oper.value}")
