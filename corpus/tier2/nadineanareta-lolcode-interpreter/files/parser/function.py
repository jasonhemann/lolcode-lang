def parse_function(self):
    
    function_name = self.current_token()
    parameters = []
    function_body = []
    return_stmt = None

    if not (function_name and function_name.type == 'Identifier'):
        raise SyntaxError(f"{self.numline}: in parse_function(): Expected valid function name: Got {keyword.type} for {keyword.value}")  

    keyword = self.get_next_token()
    while keyword.type == 'YR Keyword' and keyword.value == 'YR':
        param = self.get_next_token()
        if param and param.type in ['NUMBAR Literal', 'NUMBR Literal', 'TROOF Literal', 'Arithmetic Operation', 'YARN Delimiter']:
            self.next_pos()
        elif param and param.type == 'Identifier':
            print("test3")
        else:
            raise SyntaxError(f"{self.numline}: in parse_function(): Expected valid variable; Got {param.type} for {param.value}")

        and_symbol = self.get_next_token()
        if and_symbol and and_symbol.value == 'AN':
            keyword = self.get_next_token()
        else:
            break
    
    while self.current_token() and self.current_token().value not in ['IF U SAY SO', 'FOUND YR', 'GTFO']:
        self.next_pos()

    if self.current_token() and self.current_token().value == 'GTFO':
        self.next_pos()

    if self.current_token() and self.current_token().value == 'FOUND YR':
        while self.current_token().value != 'IF U SAY SO':
            self.next_pos()
    
    if self.current_token() and self.current_token().value == 'IF U SAY SO':
        self.next_pos()
    else:
        raise SyntaxError(f"{self.numline}: in parse_function(): Missing 'IF U SAY SO' in {function_name.value}")

    self.functions[function_name.value] = {
        'parameters': parameters,
        'body': function_body,
        'return': return_stmt
    }

# parses function call
def parse_function_call(self):
    function_name = self.current_token()
    variables = []

    if function_name and function_name.type == 'Identifier':
        keyword = self.get_next_token()
        while keyword.type == 'YR Keyword' and keyword.value == 'YR':
            param = self.get_next_token()
            if param and param.type in ['NUMBAR Literal', 'NUMBR Literal', 'TROOF Literal', 'Arithmetic Operation', 'YARN Delimiter']:
                variables.append(self.parse_expression())
            elif param and param.type == 'Identifier':
                variables.append(self.variables[param.value])
                self.next_pos()
            else:
                raise SyntaxError(f"{self.numline}: in parse_function(): Expected valid variable; Got {param.type} for {param.value}")
            
            if self.current_token() and self.current_token().value == 'AN':
                keyword = self.get_next_token()
            else:
                break
        function_call_position = self.position
        function_call_line = self.numline
        function_helper(self, function_name.value, variables)
        self.position = function_call_position
        self.numline = function_call_line

        return
    else:
        raise SyntaxError(f"{self.numline}: in parse_function_call(): Expected valid and known function name; Got {function_name.value}")

def function_helper(self, function_name, variables):
    count = 0

    while count != 2:
        self.prev_pos()
        if self.current_token().value == function_name:
            count+= 1
    return

