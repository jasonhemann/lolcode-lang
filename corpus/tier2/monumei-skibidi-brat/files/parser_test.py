from interpreter import Interpreter
from lexical_analyzer import LexicalAnalyzer, LexicalError, TokenType
from semantics_analyzer import SemanticAnalyzer
from syntax_analyzer import Parser

def print_tokens(description: str, code: str) -> None:
    print(f"\n=== {description} ===")
    print("Code:")
    print(code)
    print("\nTokens:")
    try:
        analyzer = LexicalAnalyzer()
        tokens = analyzer.tokenize(code)
        for token in tokens:
            # Format token output for better readability
            print(f"Line {token.line:2d}, Pos {token.position:2d}: {token.type.name:20s} = '{token.value}'")
    except LexicalError as e:
        print(f"Error: {e}")
    print("=" * 50)

# Test Case 1: Basic Variable Declaration and Assignment
test1 = """HAI
    WAZZUP
        I HAS A name ITZ "miru"
        I HAS A num1 ITZ 2
        I HAS A x ITZ 14
        I HAS A y ITZ 12
        I HAS A num2 ITZ 3
    BUHBYE

    HOW IZ I addNum YR x AN YR y
        FOUND YR SUM OF x AN y
    IF U SAY SO

    HOW IZ I printName YR person
        VISIBLE "Hello, " + person
        GTFO
    IF U SAY SO

    HOW IZ I printNum YR x
        FOUND YR x
    IF U SAY SO

    I IZ addNum YR num1 AN YR num2 MKAY
    VISIBLE IT

    GIMMEH name
    I IZ printName YR name MKAY
    VISIBLE IT

    I IZ printNum YR SUM OF x AN 2 MKAY
    VISIBLE IT

KTHXBYE
"""
print_tokens("Basic Variable Declaration", test1)

# First use the lexical analyzer
lexer = LexicalAnalyzer()
tokens = lexer.tokenize(test1)

syntax = Parser(tokens)
ast = syntax.parse()


# print(ast)
print("Program has no syntax error.")


analyzer = SemanticAnalyzer()
analyzer.analyze(ast)

interpreter = Interpreter()
interpreter.interpret(ast, analyzer)











# # Finally perform semantic analysis
# analyzer = SemanticAnalyzer()
# analyzer.analyze(ast)

# # Test Case 2: Arithmetic Operations
# test2 = """
# HAI
#     I HAS A result
#     result R SUM OF 10 AN 20
#     result R DIFF OF result AN 5
#     result R PRODUKT OF result AN 2
# KTHXBYE
# """
# print_tokens("Arithmetic Operations", test2)

# # Test Case 3: Control Flow
# test3 = """
# HAI
#     I HAS A temp ITZ 37
#     BOTH SAEM temp AN 37
#     O RLY?
#         YA RLY
#             VISIBLE "NORMAL TEMP"
#         NO WAI
#             VISIBLE "NOT NORMAL"
#     OIC
# KTHXBYE
# """
# print_tokens("Control Flow", test3)

# # Test Case 4: Loop Example
# test4 = """
# HAI
#     I HAS A counter ITZ 0
#     IM IN YR loop UPPIN YR counter
#         VISIBLE counter
#         BOTH SAEM counter AN 5
#         O RLY?
#             YA RLY
#                 GTFO
#         OIC
#     IM OUTTA YR loop
# KTHXBYE
# """
# print_tokens("Loop Structure", test4)

# # Test Case 5: Function Definition and Call
# test5 = """
# HAI
#     HOW IZ I add_numbers YR x AN YR y
#         FOUND YR SUM OF x AN y
#     IF U SAY SO

#     I HAS A result
#     result R I IZ add_numbers YR 10 AN YR 20 MKAY
# KTHXBYE
# """
# print_tokens("Function Definition and Call", test5)

# # Test Case 6: Mixed Data Types and Type Casting
# test6 = """
# HAI
#     I HAS A num ITZ 42
#     I HAS A str ITZ "42"
#     I HAS A bool ITZ WIN
#     I HAS A converted
#     converted R MAEK str A NUMBR
# KTHXBYE
# """
# print_tokens("Data Types and Type Casting", test6)

# # Test Case 7: Comments
# test7 = """
# HAI
#     BTW this is a single line comment
#     I HAS A x ITZ 10
#     OBTW
#     this is a
#     multi-line comment
#     TLDR
#     VISIBLE x
# KTHXBYE
# """
# print_tokens("Comments", test7)

# # Test Case 8: Error Cases
# test8 = """
# HAI
#     I HAS A 123invalid ITZ 42  BTW Invalid identifier starting with number
#     I HAS A x ITZ @#$        BTW Invalid characters
# KTHXBYE
# """
# print_tokens("Error Cases", test8)

# # Test Case 9: Boolean Operations
# test9 = """
# HAI
#     I HAS A result
#     result R BOTH OF WIN AN WIN
#     result R EITHER OF WIN AN FAIL
#     result R NOT WIN
#     result R ALL OF WIN AN WIN AN WIN MKAY
# KTHXBYE
# """
# print_tokens("Boolean Operations", test9)

# # Test Case 10: String Concatenation
# test10 = """
# HAI
#     I HAS A str1 ITZ "HELLO "
#     I HAS A str2 ITZ "WORLD!"
#     I HAS A result
#     result R SMOOSH str1 AN str2
# KTHXBYE
# """
# print_tokens("String Concatenation", test10)

# if __name__ == "__main__":
#     print("\nLOLCODE Lexical Analyzer Test Suite")
#     print("================================")