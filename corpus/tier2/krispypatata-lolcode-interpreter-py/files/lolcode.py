import sys
from lexer.lolcode_lexer import *
from parser.lolcode_parser import *
from interpreter.lolcode_interpreter import *
from interpreter.values import *
from common import globals

# Initialize the global symbol table
globals.symbol_table = SymbolTable()
globals.symbol_table.set("IT", Number(0))

# ═══════════════════════════════════════════════════════════════════════════════════════════════
# Function to run the LOLCODE interpreter
def run_lolcode(inputText=None):
    if inputText is None:
        return None, None

    # print('Input Text:')
    # print(inputText)

    # Generate Tokens
    globals.tokens = lolcode_lex(inputText)
    # tokens.append(('EOF', EOF, tokens[-1][TOKEN_LINE_NUMBER])) # Add end of line

    # print('\nTokens:')
    # print(globals.tokens)
    # print()

    # Generate ast
    lolcode_parser = Parser(globals.tokens)
    ast = lolcode_parser.parse()
    if ast.error: return None, ast.error

    # print('\nAST:')
    # print(ast.node)
    # print()

    # Run program
    lolcode_interpreter = Interpreter()
    context = Context('<program>')
    context.symbol_table = globals.symbol_table
    result = lolcode_interpreter.visit(ast.node, context)

    # print("\n─────────────────────────────────────────────────")
    # print("Symbol Table:")
    # print(globals.symbol_table.symbols)
    # print("─────────────────────────────────────────────────\n")

    return result.value, result.error

# ───────────────────────────────────────────────────────────────────────────────────────────────
# Helper function to handle the running of the LOLCODE interpreter
def handle_run_lolcode(inputText=None):
    result, error = run_lolcode(inputText)

    # If program encounters an error
    if error: print(error.as_string())
    # else: print(result)

# ───────────────────────────────────────────────────────────────────────────────────────────────
_tests = {
    "c1": "tests/c1.lol",
    "c2": "tests/c2.lol",
    "c3": "tests/c3.lol",
    "c4": "tests/c4.lol",
    "c5": "tests/c5.lol",
    "c6": "tests/c6.lol",
    "t1": "tests/01_variables.lol",
    "t2": "tests/02_gimmeh.lol",
    "t3": "tests/03_arith.lol",
    "t4": "tests/04_smoosh_assign.lol",
    "t5": "tests/05_bool.lol",
    "t6": "tests/06_comparison.lol",
    "t7": "tests/07_ifelse.lol",
    "t8": "tests/08_switch.lol",
    "t9": "tests/09_loops.lol",
    "t10": "tests/10_functions.lol",
    "a1": "tests_2/01_variables.lol",
    "a2": "tests_2/02_gimmeh.lol",
    "a3": "tests_2/03_arith.lol",
    "a4": "tests_2/04_smoosh_assign.lol",
    "a5": "tests_2/05_bool.lol",
    "a6": "tests_2/06_comparison.lol",
    "a7": "tests_2/07_ifelse.lol",
    "a8": "tests_2/08_switch.lol",
    "a9": "tests_2/09_loops.lol",
    "a10": "tests_2/10_functions.lol",
    "b1": "tests_3/01_variables.lol",
    "b2": "tests_3/02_gimmeh.lol",
    "b3": "tests_3/03_arith.lol",
    "b4": "tests_3/04_smoosh_assign.lol",
    "b5": "tests_3/05_bool.lol",
    "b6": "tests_3/06_comparison.lol",
    "b7": "tests_3/07_ifelse.lol",
    "b8": "tests_3/08_switch.lol",
    "b9": "tests_3/09_loops.lol",
    "b10": "tests_3/10_functions.lol"
}

# Function to test the LOLCODE interpreter with a specific file (terminal-based interpreter)
def test_run_lolcode():
    file = open(_tests['b2']) 
    characters = file.read()
    file.close()
    globals.no_gui = True  # Terminal-based interpreter
    handle_run_lolcode(characters)

# ═══════════════════════════════════════════════════════════════════════════════════════════════
# For testing the implementation of the program
if __name__ == '__main__':
    # test_run_lolcode() # Uncomment to run the tests on the terminal-based interpreter

    # Run the GUI-based interpreter
    from gui.lolcode_gui import run_gui
    run_gui()
