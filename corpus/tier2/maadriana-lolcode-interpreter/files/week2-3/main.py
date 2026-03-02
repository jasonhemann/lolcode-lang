#!/usr/bin/env python3
"""
LOLCODE Interpreter
Main module that orchestrates the interpretation process
"""

import sys
from lexer import Lexer
from parser import Parser
from semantic_analyzer import SemanticAnalyzer
from interpreter import Interpreter

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <filename.lol>")
        return

    file_path = sys.argv[1]

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            source_code = file.read()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return

    # Lexical Analysis
    lexer = Lexer(source_code)
    token_stream = lexer.tokenize()

    # Parsing
    try:
        parser = Parser(token_stream)
        ast = parser.parse()
    except SyntaxError as e:
        print(f"Syntax Error: {e}")
        return

    # Semantic Analysis
    analyzer = SemanticAnalyzer(ast)
    checked_ast = analyzer.analyze()
    if checked_ast is None:
        return  

    # Interpretation
    try:
        interpreter = Interpreter(checked_ast)
        interpreter.interpret()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()
