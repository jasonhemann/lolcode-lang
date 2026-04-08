''' Grammar

E ::= T | E + T | E - T
T ::= F | T * F | T / F
F ::= <number> | (E)

'''
import re

class Token:
    NUMBER = "NUMBER"
    OPERATOR = "OPERATOR"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"

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
            match = re.match(r"\d+", self.expression)
            if match:
                match_str = self.expression[:match.end()]
                tokens.append(Token(match_str, Token.NUMBER))
                self.expression = self.expression[match.end():]
                continue

            match = re.match(r"[+\-\*\/]", self.expression)
            if match:
                match_str = self.expression[:match.end()]
                tokens.append(Token(match_str, Token.OPERATOR))
                self.expression = self.expression[match.end():]
                continue

            match = re.match(r"\(", self.expression)
            if match:
                match_str = self.expression[:match.end()]
                tokens.append(Token(match_str, Token.LPAREN))
                self.expression = self.expression[match.end():]
                continue

            match = re.match(r"\)", self.expression)
            if match:
                match_str = self.expression[:match.end()]
                tokens.append(Token(match_str, Token.RPAREN))
                self.expression = self.expression[match.end():]
                continue

            raise Exception(f"Unexpected character: {self.expression[0]}")

        return tokens

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.cursor = 0

    def advance(self):
        if self.cursor < len(self.tokens) - 1:
            self.cursor += 1

    def current(self):
        return self.tokens[self.cursor]

    def expect(self, token_type):
        if self.current().type != token_type:
            raise Exception(f"Expected {token_type}, got {self.current().type}")
        self.advance()

    def expr(self):
        if self.current().type == Token.NUMBER:
            print("Got number:", self.current().lexeme)
            result = int(self.current().lexeme)

            self.advance()
            if self.current().type == Token.OPERATOR:
                # Parse the right-hand side of the operation
                print("Got operator:", f"\"{self.current().lexeme}\"")

                if self.current().lexeme == "+":
                    self.advance()
                    result += self.expr() 
                elif self.current().lexeme == "-":
                    self.advance()
                    result -= self.expr() 
                elif self.current().lexeme == "*":
                    self.advance()
                    result *= self.expr() 
                elif self.current().lexeme == "/":
                    self.advance()
                    result /= self.expr() 

            return result

        elif self.current().type == Token.LPAREN:
            print("Got left parenthesis: (")
            self.advance()
            result = self.expr()

            self.expect(Token.RPAREN)  # Ensure the parenthesis is closed
            print("Got right parenthesis: )")

            print(f"Is {self.current().lexeme} an {Token.OPERATOR}? {self.current().type == Token.OPERATOR}")
            if self.current().type == Token.OPERATOR:
                # Parse the right-hand side of the operation
                print("Got operator:", f"\"{self.current().lexeme}\"")

                if self.current().lexeme == "+":
                    self.advance()
                    result += self.expr() 
                elif self.current().lexeme == "-":
                    self.advance()
                    result -= self.expr() 
                elif self.current().lexeme == "*":
                    self.advance()
                    result *= self.expr() 
                elif self.current().lexeme == "/":
                    self.advance()
                    result /= self.expr() 

            return result

        else:
            raise Exception("Invalid syntax in expression")

# MAIN
expression = "((((2+(4*5)))))*(5*8)"
lexer = Lexer(expression)
tokens = lexer.tokenize()

print("Tokens:")
for token in tokens:
    print(token)

parser = Parser(tokens)
result = parser.expr()

print("Result:", result)
print("\nParsing completed successfully!")
