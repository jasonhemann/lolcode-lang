from io import TextIOWrapper
import re

class Pattern:
    KEYWORD = r"\b(HAI|KTHXBYE|WAZZUP|BUHBYE|I HAS A|ITZ\b|R|AN|MAEK|A|IS NOW A|VISIBLE|GIMMEH|O RLY\?|YA RLY|NO WAI|MEBBE|NO WAI|OIC|WTF\?|OMGWTF|OMG|IM IN YR|UPPIN|NERFIN|YR|TIL|WILE|IM OUTTA YR|HOW IZ I|IF U SAY SO|GTFO|FOUND YR|I IZ|MKAY|NUMBR|NUMBAR|YARN|TROOF|NOOB)"
    OPERATOR = r"\b(SUM OF|DIFF OF|PRODUKT OF|QUOSHUNT OF|MOD OF|BIGGR OF|SMALLR OF|BOTH OF|EITHER OF|WON OF|NOT|ANY OF|ALL OF|BOTH SAEM|DIFFRINT|SMOOSH|MAEK)"
    TYPE = r"\b(NUMBR|NUMBAR|TROOF|YARN|NOOB)"
    
    CONCAT = r"\+"
    DELIMITER = r"\!"
    IDENTIFIER = r"\b[a-zA-Z]\w*\b"
    NUMBAR = r"\-?\d+\.\d+"
    NUMBR = r"\-?\d+"
    YARN = r"\"[^\n\"]*\""
    TROOF = r"\b(WIN|FAIL)\b"
    NEWLINE = r"(\s*\n\s*|\,)"
    WHITESPACE = r" |\t"
    COMMENT_SINGLE = r"BTW [^\n]*"
    COMMENT_MULTI = r"OBTW\s(.|\n)*\sTLDR"

class Token:
    KEYWORD = "KEYWORD"
    OPERATOR = "OPERATOR"
    TYPE = "TYPE"

    CONCAT = "CONCAT"
    DELIMITER = "DELIMITER"
    IDENTIFIER = "IDENTIFIER"
    NUMBAR = "NUMBAR"
    NUMBR = "NUMBR"
    YARN = "YARN"
    TROOF = "TROOF"
    NEWLINE = "NEWLINE"
    WHITESPACE = "WHITESPACE"
    COMMENT_SINGLE = "COMMENT_SINGLE"
    COMMENT_MULTI = "COMMENT_MULTI"

    # Higher to lower order of precedence
    precedence = (
        (Pattern.COMMENT_MULTI, COMMENT_MULTI),
        (Pattern.COMMENT_SINGLE, COMMENT_SINGLE),
        (Pattern.WHITESPACE, WHITESPACE),
        (Pattern.NEWLINE, NEWLINE),
        (Pattern.CONCAT, CONCAT),
        (Pattern.DELIMITER, DELIMITER),
        (Pattern.TYPE, TYPE),
        (Pattern.OPERATOR, OPERATOR),
        (Pattern.KEYWORD, KEYWORD),
        (Pattern.TROOF, TROOF),
        (Pattern.IDENTIFIER, IDENTIFIER),
        (Pattern.NUMBAR, NUMBAR),
        (Pattern.NUMBR, NUMBR),
        (Pattern.YARN, YARN),
    )

    ignore = (WHITESPACE, COMMENT_SINGLE, COMMENT_MULTI)

    def __init__(self, lexeme, type=None, description="None", line=-1, col=-1):
        self.lexeme = lexeme
        self.type = type
        self.description = description
        self.line = line
        self.col = col

    def get_lexeme(self):
        return self.lexeme
    
    def get_type(self):
        return self.type

    def get_desc(self):
        return self.description
    
    def pos(self):
        return f"[line: {self.line}, col: {self.col}]"
    
    def __repr__(self):
        return f"[{self.line}:{self.col}] {self.type}: {self.lexeme}"

# Dictionary for LOLCODE keyword descriptions
descriptions = {
    Token.NUMBR: "Integer literal",
    Token.NUMBAR: "Floating-point literal",
    Token.YARN: "String literal",
    Token.TROOF: "Boolean literal",
    Token.IDENTIFIER: "Identifier",
    Token.COMMENT_SINGLE: "Single-line comment",
    Token.COMMENT_MULTI: "Multiline comment",
    Token.NEWLINE: "Line break",
    Token.TYPE: "Type identifier",
    "<identifier>": "Variable, function, or loop name",
    "HAI": "Start of program",
    "KTHXBYE": "End of program",
    "WAZZUP": "Alternative start of program",
    "BUHBYE": "Alternative end of program",
    "BTW": "Single-line comment",
    "OBTW": "Start of multi-line comment",
    "TLDR": "End of multi-line comment",
    "I HAS A": "Variable declaration",
    "ITZ": "Initial value assignment",
    "R": "Assignment operator",
    "AN": "Argument separator",
    "SUM OF": "Addition operator",
    "DIFF OF": "Subtraction operator",
    "PRODUKT OF": "Multiplication operator",
    "QUOSHUNT OF": "Division operator",
    "MOD OF": "Modulus operator",
    "BIGGR OF": "Maximum of two values",
    "SMALLR OF": "Minimum of two values",
    "BOTH OF": "Logical AND",
    "EITHER OF": "Logical OR",  
    "WON OF": "Logical XOR",
    "NOT": "Logical NOT",
    "ANY OF": "Any operand is true",
    "ALL OF": "All operands are true",
    "BOTH SAEM": "Equality check",
    "DIFFRINT": "Inequality check",
    "SMOOSH": "String concatenation",
    "MAEK": "Type casting",
    "A": "Type specifier in casting",
    "IS NOW A": "Dynamic type change",
    "VISIBLE": "Output statement",
    "+": "Concatenation Operator",
    "GIMMEH": "Input statement",
    "O RLY?": "Start of conditional block",
    "YA RLY": "True branch of conditional",
    "MEBBE": "Else-if branch",
    "NO WAI": "False branch of conditional",
    "OIC": "End of conditional block",
    "WTF?": "Start of switch-case block",
    "OMG": "Case in switch block",
    "OMGWTF": "Default case in switch block",
    "IM IN YR": "Start of loop block",
    "UPPIN": "Increment loop variable",
    "NERFIN": "Decrement loop variable",
    "YR": "Loop variable specifier",
    "TIL": "Loop until condition",
    "WILE": "Loop while condition",
    "IM OUTTA YR": "End of loop block",
    "HOW IZ I": "Function definition",
    "IF U SAY SO": "End of function definition",
    "GTFO": "Exit loop or function",
    "FOUND YR": "Return value from function",
    "I IZ": "Function call",
    "MKAY": "End of function call arguments",
    " ": "Whitespace",
    "\t": "Whitespace",
    "\n": "Newline",
}

class Lexer:
    def __init__(self, input):
        # Check if it is an opened file
        # Otherwise, [input] is a plain string
        if isinstance(input, TextIOWrapper):
            self.source_code = input.read()
        elif isinstance(input, str):
            self.source_code = input
        else: raise TypeError(f"Cannot accept {type(input)}. Input a string or a File.")

        self.curr_line = 1
        self.curr_col = 0
        self.tokens = self.tokenize() # Tokenize becomes part of __init__

    def get_tokens(self):  # Use get_item to return value
        return self.tokens

    def tokenize(self):
        tokens = []

        # While there are strings to be read
        while self.source_code:
            for pattern, token_type in Token.precedence:
                # Check if the current pattern has match
                match = re.match(pattern, self.source_code)
                if match:
                    match_str = self.source_code[:match.end()]

                    # Given a lexeme, find the appropriate description
                    description = descriptions.get(match_str, None) or descriptions.get(token_type, "?") 

                    # Trim single- and double-quotes
                    if token_type == Token.YARN:
                        match_str = match_str[1:-1]

                    if token_type in (Token.COMMENT_MULTI, Token.NEWLINE):
                        self.curr_line += match_str.count('\n')
                        i_last_newline = match_str.rfind('\n')
                        self.curr_col = len(match_str[i_last_newline:match.end()])
                        
                    if token_type not in Token.ignore:
                        token = Token(match_str, token_type, description, self.curr_line, self.curr_col)
                        tokens.append(token)  

                    # Advance the cursor by the length of the lexeme
                    self.source_code = self.source_code[match.end():]
                    self.curr_col += match.end()
                    break
            else: raise ValueError(f"Unexpected character: \"{self.source_code[0]}\"")

        print("(✓) Tokenization finished.") # Relocated at the bottom for console readability
        print("Tokens:", len(tokens))
        # print(tokens)

        # Print all tokens
        # for token in tokens:
        #     print(token) 

        return tokens