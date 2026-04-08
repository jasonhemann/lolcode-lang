import sys
from lexer import lolcode_lexer
from parser import Parser
from interpreter import Interpreter

def run(code):
	try:
		tokens = list(lolcode_lexer(code))
		# print(tokens)
		parser = Parser(list(tokens))
		ast = parser.parse_program()
            
		# print_ast(ast)

		interpreter = Interpreter()
		interpreter.visit(ast)
	except SyntaxError as e:
		print(f"Syntax Error: {e}")
	except Exception as e:
		print(f"Unknown Error: {e}")

if __name__=="__main__":
	if len(sys.argv) > 1:
		filename = sys.argv[1]
		with open(filename, 'r') as f:
			code = f.read()
		run(code)
	else:
		print("Please provide a valid LOLCODE file")
		print("Usage: python main.py <filename>.lol")