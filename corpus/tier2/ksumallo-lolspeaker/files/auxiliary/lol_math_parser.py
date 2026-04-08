''' Grammar

E ::= T | E + T | E - T
T ::= F | T * F | T / F
F ::= <number> | (E)

'''
import re
from utils import Log

Log.show(True)

class Node:
    def __init__(self, symbol=None, parent=None, children=[]):
        self.symbol = symbol
        self.parent = parent
        self.children = children
        
    def add_child(self, node):
        self.children.append(node)

class Token:
    NUMBR = "NUMBR"
    NUMBAR = "NUMBAR"
    OPERATOR = "OPERATOR"
    KEYWORD = "KEYWORD"

    def __init__(self, lexeme, type=None):
        self.lexeme = lexeme
        self.type = type

    def __str__(self):
        return f"{self.type}: {self.lexeme}"

class Lexer:
    def __init__(self, expression):
        self.expression = expression
        self.cursor = 0

    def tokenize(self):
        tokens = []
        while self.expression:
            match = re.match(r"AN", self.expression)
            if match:
                match_str = self.expression[:match.end()]
                tokens.append(Token(match_str, Token.KEYWORD))
                self.expression = self.expression[match.end():]
                continue

            match = re.match(r"\-?+\d\.\d+", self.expression)
            if match:
                match_str = self.expression[:match.end()]
                tokens.append(Token(match_str, Token.NUMBAR))
                self.expression = self.expression[match.end():]
                continue

            match = re.match(r"\-?\d+", self.expression)
            if match:
                match_str = self.expression[:match.end()]
                tokens.append(Token(match_str, Token.NUMBR))
                self.expression = self.expression[match.end():]
                continue

            match = re.match(r"\b(SUM OF|DIFF OF|PRODUKT OF|QUOSHUNT OF|MOD OF|BIGGR OF|SMALLR OF)\b", self.expression)
            if match:
                match_str = self.expression[:match.end()]
                tokens.append(Token(match_str, Token.OPERATOR))
                self.expression = self.expression[match.end():]
                continue

            match = re.match(r"\s", self.expression)
            if match:
                # Matched whitespace
                self.expression = self.expression[match.end():]
                continue

            raise Exception(f"Unexpected character: {self.expression[0]}")

        return tokens

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.cursor = 0
        self.root = Node()

    def next(self):
        if self.cursor < len(self.tokens) - 1:
            self.cursor += 1

    def current(self):
        return self.tokens[self.cursor]
    
    def curr_node(self):
        return self.tokens[self.cursor]
    
    def accept(self, *token_types):
        return self.current().type in token_types

    def expect(self, *token_types, lexeme=None):
        self.next()
        if self.current().type not in token_types:
            expected = lexeme if lexeme is not None else token_types
            raise Exception(f"Expected {expected}, got {self.current().type}")
        
        return lexeme is None or self.current().lexeme == lexeme

    def expr(self):
        if self.accept(Token.OPERATOR):
            Log.i(f"Start operation: {self.current().lexeme}")
            operation = self.current().lexeme

            self.next()
            accept = self.expr()
            if not accept:
                raise Exception("Expected: <expression>")
                        
            result = accept
            
            self.expect(Token.KEYWORD, "AN")

            self.next()
            accept = self.expr()
            if not accept:
                raise Exception("Expected: <expression>")
            
            match operation:
                case "SUM OF":
                    result += accept
                case "DIFF OF":
                    result -= accept
                case "PRODUKT OF":
                    result *= accept
                case "QUOSHUNT OF":
                    result /= accept
                case "BIGGR OF":
                    result = max(result, accept)
                case "SMALLR OF":
                    result = min(result, accept)
                case _:
                    raise Exception(f"Operation {operation} not recognized")
                
            return result

        if self.current().type == Token.NUMBAR:
            Log.i(f"Got float: {self.current().lexeme}")
            
            return float(self.current().lexeme)
        
        if self.current().type == Token.NUMBR:
            Log.i(f"Got integer: {self.current().lexeme}")
            
            return int(self.current().lexeme)
        
        raise Exception("Invalid syntax in expression")

# MAIN
expression = "PRODUKT OF SUM OF 8 AN 8 AN 100"
expression = input("Enter expression:")
lexer = Lexer(expression)
tokens = lexer.tokenize()

print("Tokens:")
for token in tokens:
    print(token)

parser = Parser(tokens)
result = parser.expr()

print("Result:", result)
Log.d("Parsing completed successfully!")