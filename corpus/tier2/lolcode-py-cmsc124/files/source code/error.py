class Error(Exception):
    def __init__(self, token, cause) -> None:
        self.token = token
        self.cause = cause

    def __repr__(self) -> str:
        return f'Error at {self.token}: {self.cause}'

    def __str__(self) -> str:
        return f'Error at {self.token}: {self.cause}'

class LexerError(Exception):
    def __init__(self, pos, line):
        self.pos = pos
        self.line = line
    
    def __repr__(self) -> str:
        return f'LexerError at {self.pos} in line {self.line}'

    def __str__(self) -> str:
        return f'LexerError at {self.pos} in line {self.line}'

class ErrorSyntax(Error):
    def __init__(self,token,cause) -> None:
        super().__init__(token,cause)
    
    def __repr__(self) -> str:
        return f'SyntaxError at {self.token} in line {self.token.line}: {self.cause}'

    def __str__(self) -> str:
        return f'SyntaxError at {self.token} in line {self.token.line}: {self.cause}'

class ErrorSemantic(Error):
    def __init__(self,token,cause) -> None:
        super().__init__(token,cause)
    
    def __repr__(self) -> str:
        return f'SemanticError at {self.token} in line {self.token.line}: {self.cause}'

    def __str__(self) -> str:
        return f'SemanticError at {self.token} in line {self.token.line}: {self.cause}'