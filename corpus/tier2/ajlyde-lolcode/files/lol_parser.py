class ASTNode:
    def __init__(self, node_type, value=None, children=None):
        self.type = node_type
        self.value = value
        self.children = children or []

    def __repr__(self):
        return f"ASTNode({self.type}, {self.value}, children={self.children})"

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current_token(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def advance(self):
        self.pos += 1

    def parse(self):
        if self.current_token().type != 'HAI':
            raise SyntaxError("Program must start with HAI")
        self.advance()

        program_nodes = []
        while self.current_token() and self.current_token().type != 'KTHXBYE':
            node = self.parse_statement()
            if node:
                program_nodes.append(node)

        if not self.current_token() or self.current_token().type != 'KTHXBYE':
            raise SyntaxError("Program must end with KTHXBYE")

        return ASTNode('PROGRAM', children=program_nodes)

    def parse_statement(self):
        token = self.current_token()
        if token.type == 'I':
            return self.parse_var_declaration()
        elif token.type == 'IDENTIFIER':
            return self.parse_assignment()
        elif token.type == 'VISIBLE':
            return self.parse_visible()
        elif token.type == 'GIMMEH':
            return self.parse_gimmeh()

        raise SyntaxError(f"Unexpected token {token.type} at line {token.line}")

    def parse_var_declaration(self):
        self.advance()
        if self.current_token().type != 'HAS':
            raise SyntaxError("Expected HAS after I")
        self.advance()
        if self.current_token().type != 'A':
            raise SyntaxError("Expected A after HAS")
        self.advance()
        var_token = self.current_token()
        if var_token.type != 'IDENTIFIER':
            raise SyntaxError("Expected variable name")
        var_name = var_token.value
        self.advance()

        init_value = None
        if self.current_token() and self.current_token().type == 'ITZ':
            self.advance()
            init_value = self.parse_expression()

        return ASTNode('VAR_DECL', value=var_name, children=[init_value] if init_value else [])

    def parse_assignment(self):
        var_token = self.current_token()
        var_name = var_token.value
        self.advance()
        if self.current_token().type != 'R':
            raise SyntaxError("Expected R for assignment")
        self.advance()
        expr = self.parse_expression()
        return ASTNode('ASSIGN', value=var_name, children=[expr])

    def parse_visible(self):
        self.advance()
        expr = self.parse_expression()
        return ASTNode('VISIBLE', children=[expr])

    def parse_gimmeh(self):
        self.advance()
        var_token = self.current_token()
        if var_token.type != 'IDENTIFIER':
            raise SyntaxError("Expected variable name after GIMMEH")
        var_name = var_token.value
        self.advance()
        return ASTNode('GIMMEH', value=var_name)

    def parse_expression(self):
        token = self.current_token()
        if token.type in ('NUMBR', 'NUMBAR', 'YARN', 'IDENTIFIER'):
            self.advance()
            return ASTNode('LITERAL', value=token.value)
        raise SyntaxError(f"Unexpected token in expression: {token.type}")

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current_token(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def eat(self, token_type):
        token = self.current_token()
        if token and token.type == token_type:
            self.pos += 1
            return token
        raise Exception(f"Expected token {token_type}, got {token}")

    def parse(self):
        # Simple example: expect first token to be HAI
        token = self.current_token()
        if token is None:
            raise Exception("No tokens to parse")

        if token.type != 'HAI':
            raise Exception(f"Program must start with HAI, found {token.type}")

        self.eat('HAI')

        # Here you would continue parsing rest of program...
        # For demo, just return a dummy AST:
        return {"program": "parsed"}
