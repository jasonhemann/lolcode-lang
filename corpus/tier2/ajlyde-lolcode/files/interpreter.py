# interpreter.py
from lexer import Lexer

class Interpreter:
    def __init__(self, source_code):
        self.source = source_code

    def run(self):
        lexer = Lexer(self.source)
        tokens = lexer.tokenize()
        print("TOKENS:", tokens)

        if not tokens:
            print("No tokens found. Exiting.")
            return

        # Example simple parser check for 'HAI' start token
        if tokens[0].type != 'HAI':
            print("Error: Program must start with HAI")
            return
        
        # ... add parser and interpreter logic here ...
        print("Parsing and interpreting not implemented yet.")

from lexer import Lexer
from lol_parser import Parser

class Interpreter:
    def __init__(self, source_code):
        self.source = source_code

    def run(self):
        lexer = Lexer(self.source)
        tokens = lexer.tokenize()
        print("TOKENS:", tokens)
        if not tokens:
            print("No tokens found. Exiting.")
            return

        parser = Parser(tokens)
        ast = parser.parse()
        print("Parsed AST:", ast)
