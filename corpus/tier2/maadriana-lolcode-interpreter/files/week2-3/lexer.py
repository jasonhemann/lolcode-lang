"""
LOLCODE Lexer/Tokenizer Module
Tokenizes LOLCODE source code into a stream of tokens
"""

class Token:
    def __init__(self, token_type, value=None, line=None, position=None):
        self.type = token_type
        self.value = value
        self.line = line
        self.position = position

    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)}, line={self.line}, pos={self.position})"


class Lexer:
    TOKEN_TYPES = {
        # Multi-word keywords first
        "I HAS A": "VAR_DECLARATION",
        "SUM OF": "OP_ADD",
        "DIFF OF": "OP_SUB",
        "PRODUKT OF": "OP_MUL",
        "QUOSHUNT OF": "OP_DIV",
        "MOD OF": "OP_MOD",
        "BIGGR OF": "OP_MAX",
        "SMALLR OF": "OP_MIN",
        "BOTH SAEM": "OP_EQUAL",
        "DIFFRINT": "OP_NOT_EQUAL",
        "BOTH OF": "OP_AND",
        "EITHER OF": "OP_OR",
        "WON OF": "OP_XOR",
        "ALL OF": "OP_ALL",
        "ANY OF": "OP_ANY",
        "O RLY?": "IF_START",
        "YA RLY": "IF_TRUE",
        "NO WAI": "IF_FALSE",
        "OBTW": "COMMENT_BLOCK_START",
        "TLDR": "COMMENT_BLOCK_END",
        "BTW": "COMMENT_LINE",

        # Single-word keywords
        "HAI": "PROGRAM_START",
        "KTHXBYE": "PROGRAM_END",
        "ITZ": "VAR_ASSIGNMENT",
        "R": "ASSIGNMENT_OP",
        "VISIBLE": "OUTPUT",
        "GIMMEH": "INPUT",
        "OIC": "IF_END",
        "AN": "CONNECTOR",
        "NOT": "OP_NOT",
        "SMOOSH": "OP_SMOOSH"
    }

    def __init__(self, source_code):
        self.source_code = source_code
        self.lines = source_code.split('\n')
        self.tokens = []

    def tokenize(self):
        for line_num, line in enumerate(self.lines):
            words = line.strip().split()
            i = 0
            while i < len(words):
                word = words[i]

                # Handle string literals
                if word.startswith('"'):
                    string_token = word
                    while not string_token.endswith('"') and i + 1 < len(words):
                        i += 1
                        string_token += ' ' + words[i]
                    self.tokens.append(Token("STRING_LITERAL", string_token.strip('"'), line_num + 1, i))
                    i += 1
                    continue

                # Try 3-word phrases
                if i + 2 < len(words):
                    phrase = f"{words[i]} {words[i + 1]} {words[i + 2]}"
                    if phrase in self.TOKEN_TYPES:
                        self.tokens.append(Token(self.TOKEN_TYPES[phrase], phrase, line_num + 1, i))
                        i += 3
                        continue

                # Try 2-word phrases
                if i + 1 < len(words):
                    phrase = f"{words[i]} {words[i + 1]}"
                    if phrase in self.TOKEN_TYPES:
                        self.tokens.append(Token(self.TOKEN_TYPES[phrase], phrase, line_num + 1, i))
                        i += 2
                        continue

                # Single-word tokens
                if word in self.TOKEN_TYPES:
                    self.tokens.append(Token(self.TOKEN_TYPES[word], word, line_num + 1, i))
                    i += 1
                    continue

                # Check for literals
                if word.isdigit():
                    self.tokens.append(Token("INT_LITERAL", int(word), line_num + 1, i))
                    i += 1
                    continue

                if word == "WIN":
                    self.tokens.append(Token("BOOL_LITERAL", True, line_num + 1, i))
                    i += 1
                    continue
                elif word == "FAIL":
                    self.tokens.append(Token("BOOL_LITERAL", False, line_num + 1, i))
                    i += 1
                    continue

                # Otherwise treat as identifier or unknown
                if word.isidentifier():
                    self.tokens.append(Token("IDENTIFIER", word, line_num + 1, i))
                else:
                    self.tokens.append(Token("UNKNOWN", word, line_num + 1, i))

                i += 1

        return self.tokens
