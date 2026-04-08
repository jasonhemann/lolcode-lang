import re
import tkinter as tk
from tkinter import filedialog

# NOTE: i had to modify the code a little in the lexer, had to remove the \b because they remove the special characters and fuck up the keywords with special characters
# i also changed the line.strip to line.lstrip to catch just the leading whitespace since strip removes all leading and trailing white spaces and fuck up the line counting for syntax error detection

# LOLCODE keywords and patterns
KEYWORDS = {
    "HAI": "Code Delimiter",
    "KTHXBYE": "Code Delimiter",
    "WAZZUP": "Variable Declaration Clause Delimiter",
    "BUHBYE": "Variable Declaration Clause Delimiter",
    "BTW": "Comment",
    "OBTW": "Comment Delimiter",
    "TLDR": "Comment Delimiter",
    "I HAS A": "Variable Declaration",
    "ITZ": "Variable Initialization",
    "R": "Variable Assignment",
    "SUM OF": "Addition Operation",
    "DIFF OF": "Subtraction Operation",
    "PRODUKT OF": "Multiplication Operation",
    "QUOSHUNT OF": "Division Operation",
    "MOD OF": "Modulo Operation",
    "BIGGR OF": "Max Operation",
    "SMALLR OF": "Min Operation",
    "BOTH OF": "Boolean AND",
    "EITHER OF": "Boolean OR",
    "WON OF": "Boolean XOR",
    "NOT": "Boolean NOT",
    "ANY OF": "Boolean OR (Infinite Arity)",
    "ALL OF": "Boolean AND (Infinite Arity)",
    "BOTH SAEM": "Comparison Operation ==",
    "DIFFRINT": "Comparison Operation !=",
    "SMOOSH": "String Concatenation",
    "MAEK": "Explicit Typecast",
    "AN": "Partial Keyword",
    "A": "Partial Keyword",
    "IS NOW A": "Explicit Typecast",
    "VISIBLE": "Output Keyword", 
    "GIMMEH": "Input Keyword",
    "O RLY?": "If Block Start",
    "YA RLY": "Condition Met Code Block Delimiter",
    "^MEBBE": "Else If Code Block Delimiter", # not required to implement
    "NO WAI": "Condition Not Met Code Block Delimiter",
    "OIC": "If/Switch Block End",
    "WTF?": "Switch Block Start",
    "OMGWTF": "Default Case Keyword",
    "OMG": "Case Keyword",
    "IM IN YR": "Loop Delimiter",
    "IM OUTTA YR": "Loop Delimiter",
    "FOUND YR": "Return Keyword",
    "YR": "Partial Keyword",
    "UPPIN": "Increment Operation",
    "NERFIN": "Decrement Operation",
    "TIL": "Repeat Loop Until Condition Met",
    "WILE": "Repeat Loop While Condition Met",
    "HOW IZ I": "Function Delimiter",
    "IF U SAY SO": "Function Delimiter",
    "GTFO": "Break Keyword",
    "I IZ": "Function Call Keyword",
    "MKAY": "Boolean Statement End"
}

TOKEN_TYPES = {
    'COMMENT': r'BTW.*',
    # 'KEYWORD': r'\b(?:' + '|'.join(re.escape(keyword) for keyword in KEYWORDS) + r')\b',
    'KEYWORD': r'(?:' + '|'.join(re.escape(keyword) for keyword in KEYWORDS) + r')',
    'NUMBAR':r'\b-?\d+\.\d+\b',
    'NUMBR': r'\b-?\d+\b',
    'CONCATENATE': r'\+', 
    'TROOF': r'WIN|FAIL',
    'YARN': r'"[^"]*"',
    'TYPE': r'(NUMBAR|NUMBR|TROOF|YARN|NOOB)',
    'VARIABLE': r'\b[A-Za-z_]\w*\b',
    'NEWLINE': r'\n',
    'WHITESPACE': r'[ \t]+'
}

# Combine token types into a single regex pattern
TOKEN_REGEX = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_TYPES.items())

class LOLCodeLexer:
    def __init__(self):
        self.file_path = None  # Initialize without a file path

    def set_file_path(self, file_path):
        self.file_path = file_path

    def read_code(self):
        if not self.file_path:
            raise Exception("File path not set")
        with open(self.file_path, 'r') as file:
            return file.read()

    def tokenize(self, code):
        # Tokenize the given code.
        tokens = []
        lines = code.splitlines(True)
        is_multiline_comment = False
        multiline_comment_content = []

        for line in lines:
            line = line.lstrip()
            # print(line)
            if is_multiline_comment:
                if line.startswith("TLDR"):
                    # End of multi-line comment
                    # Join the comment lines with a \n and add "OBTW" at the start and "TLDR" at the end
                    full_comment = "OBTW \\n " + " \\n ".join(multiline_comment_content) + " \\n TLDR"
                    tokens.append(("MULTI-LINE_COMMENT", full_comment))
                    is_multiline_comment = False
                    multiline_comment_content = []
                else:
                    # Append the content of the line to the multi-line comment (without leading whitespace)
                    multiline_comment_content.append(line)
                continue

            if line.startswith("OBTW"):
                # Start of multi-line comment
                is_multiline_comment = True
                continue

            # Tokenize normally for non-comment lines
            for match in re.finditer(TOKEN_REGEX, line, flags=0):
                # print(match)
                token_type = match.lastgroup
                value = match.group(token_type)
                # print(value, match.re)
                if token_type == "WHITESPACE":
                    continue
                if token_type == "YARN":
                    tokens.append(("STRING_DELIMITER", '"'))
                    value = value[1:-1]
                    tokens.append((token_type, value))
                    tokens.append(("STRING_DELIMITER", '"'))
                    continue
                # if token_type == "NEWLINE":
                #     tokens.append(("NEWLINE", "\n"))
                #     continue
                tokens.append((token_type, value))  # Appends the found value and token type in the tokens list

        return tokens

    def analyze_file(self):
        # Analyze the LOLCODE file.
        code = self.read_code()
        tokens = self.tokenize(code)
        return tokens

# Run the lexer and open the file explorer for file selection
# lexer = LOLCodeLexer()
# tokens = lexer.analyze_file()
# print(tokens)
# print(TOKEN_REGEX)

# # Print header for the table
# print(f"{'TYPE':<20} {'LEXEMES':<25} {'CLASSIFICATION':<30}")
# print("=" * 90)

# # Display tokens in three columns: TYPE, LEXEMES, CLASSIFICATION
# for token in tokens:
#     token_type = token[0]
#     lexeme = token[1]
    
#     if token_type == 'NEWLINE':
#         lexeme = '\\n'
#         classification = 'Newline\n'
#     else:
#         # Classification is either from KEYWORDS or based on the token type
#         if token_type == 'KEYWORD':
#             classification = KEYWORDS.get(lexeme, "Unknown")
#         else:
#             classification = {
#                 'COMMENT': 'Comment',
#                 'NUMBAR': 'Literal (Float)',
#                 'NUMBR': 'Literal (Integer)',
#                 'CONCATENATE': 'Concatenate Keyword',
#                 'TROOF': "Boolean Literal",
#                 'YARN': 'String',
#                 'STRING_DELIMITER': 'String Delimiter',
#                 'VARIABLE': 'Variable'
#             }.get(token_type, "Unknown")
    
#     # Print each token in a formatted table row

#     print(f"{token_type:<20} {lexeme:<25} {classification:<30}")