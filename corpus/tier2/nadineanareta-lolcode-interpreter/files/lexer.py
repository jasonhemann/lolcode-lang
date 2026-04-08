from regex import *
import re

# token class
class Token:
    def __init__(self, type, value): #type-value pair where type is a string that falls into one of the above types
        self.type = type
        self.value = value

    def __repr__(self):
        return f'{self.type} - {self.value}'

# lexer
class LOLCodeLexer:
    def __init__(self, code):
        self.code = code
        self.tokens = [] #token list to be appended to

    # main function
    # using the match() function (from the re package), matches the next read string at the given position
    # looping through the defined regular expressions in TOKEN_REGEXES and appends the string and its corresponding
    # type to the tokens list, skipping through whitespaces and comments (excluding multiline OBTW-TLDR comments for now)
    # and returns the final tokens list
    def tokenize(self): 
        position = 0
        while position < len(self.code):
            match = None

            for token_type, regex in TOKEN_REGEXES:
                pattern = re.compile(regex) #compile() function returns regex object that can be used with the match() function
                match = pattern.match(self.code, position)

                if match:
                    value = match.group(0) #0 parameter returns entire matched string
                    if token_type not in ['COMMENT', 'WHITESPACE', 'Command Breaks', 'Line Continuation']:  # Skip whitespace and comments
                        if token_type == 'YARN Literal': # magkahiwalay yung " sa misong string (di ko alam kung paano haha)
                            self.tokens.append(Token('YARN Delimiter', '"'))
                            self.tokens.append(Token(token_type, value.replace('"', '')))
                            self.tokens.append(Token('YARN Delimiter', '"'))
                        else:
                            token = Token(token_type, value)
                            self.tokens.append(token)
                    position = match.end()
                    break

            if not match:
                raise ValueError(f'Invalid character at position {position}: {self.code[position]}')

        return self.tokens