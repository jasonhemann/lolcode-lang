import re

# LOLCODE token patterns for lexical analysis
# the order of these patterns is important because earlier patterns get matched first
token_patterns = [
    # Valid keywords
    (r'O RLY\?', 'If-then Keyword'), 
    (r'WTF\?', 'Switch-Case Keyword'),
    
    (r'O RLY\b', 'INVALID Keyword'),
    (r'WTF\b', 'INVALID Keyword'),

    (r'\+', 'Output Separator'),
    
    # LITERALS
    (r'\"[^\"]*\"', 'YARN Literal'),
    (r'-?[0-9]+\.[0-9]+', 'NUMBAR Literal'),
    (r'-?[0-9]+', 'NUMBR Literal'),
    (r'(WIN|FAIL)', 'TROOF Literal'),
    (r'(NUMBR|NUMBAR|YARN|TROOF|NOOB)', 'Type Literal'),
    
    # KEYWORDS
    (r'HAI\b', 'Code Delimiter'),
    (r'KTHXBYE\b', 'Code Delimiter'),
    (r'BTW.*', 'Comment Line'),
    (r'OBTW\b', 'Comment Line'),
    (r'TLDR\b', 'Comment Line'),
    (r'I HAS A\b', 'Variable Declaration'),
    (r'ITZ\b', 'Variable Assignment'),
    (r'R\b', 'Variable Assignment'),
    (r'AN\b', 'Parameter Delimiter'),
    (r'SUM OF\b', 'Arithmetic Operation'),
    (r'DIFF OF\b', 'Arithmetic Operation'),
    (r'PRODUKT OF\b', 'Arithmetic Operation'),
    (r'QUOSHUNT OF\b', 'Arithmetic Operation'),
    (r'MOD OF\b', 'Arithmetic Operation'),
    (r'BIGGR OF\b', 'Arithmetic Operation'),
    (r'SMALLR OF\b', 'Arithmetic Operation'),
    (r'BOTH OF\b', 'Boolean Operation'),
    (r'EITHER OF\b', 'Boolean Operation'),
    (r'WON OF\b', 'Boolean Operation'),
    (r'NOT\b', 'Boolean Operation'),
    (r'ANY OF\b', 'Boolean Operation'),
    (r'ALL OF\b', 'Boolean Operation'),
    (r'BOTH SAEM\b', 'Comparison Operation'),
    (r'DIFFRINT\b', 'Comparison Operation'),
    (r'SMOOSH\b', 'String Concatenation'),
    (r'MAEK A\b', 'Typecasting Operation'),
    (r'A\b', 'Typecasting Operation'),
    (r'IS NOW A\b', 'Typecasting Operation'),
    (r'VISIBLE\b', 'Output Keyword'),
    (r'GIMMEH\b', 'Input Keyword'),
    (r'YA RLY\b', 'If-then Keyword'),
    (r'MEBBE\b', 'If-then Keyword'),
    (r'NO WAI\b', 'If-then Keyword'),
    (r'OIC\b', 'Exit Keyword'), 
    (r'OMG\b', 'Switch-Case Keyword'),
    (r'OMGWTF\b', 'Switch-Case Keyword'),
    (r'IM IN YR\b', 'Loop Keyword'),
    (r'UPPIN\b', 'Loop Operation'),
    (r'NERFIN\b', 'Loop Operation'),
    (r'YR\b', 'Loop Variable Assignment'),
    (r'TIL\b', 'Loop Keyword'),
    (r'WILE\b', 'Loop Keyword'),
    (r'IM OUTTA YR\b', 'Loop Keyword'),
    (r'HOW IZ I\b', 'Function Keyword'),
    (r'IF U SAY SO\b', 'Function Keyword'),
    (r'GTFO\b', 'Return Keyword'),
    (r'FOUND YR\b', 'Return Keyword'),
    (r'I IZ\b', 'Function Call'),
    (r'MKAY\b', 'Concatenation Delimiter'),
    (r'NOOB\b', 'Void Literal'),

    # BONUS
    (r'!', 'Suppress Newline'),

    # IDENTIFIERS
    (r'[a-zA-Z][a-zA-Z0-9_]*', 'Variable Identifier'),
]

# object token class 
# contains all the tokens that we found from the source code
class Token:
    def __init__(self, type, value, line_number=None):
        self.type = type
        self.value = value
        self.line_number = line_number

    def __repr__(self):
        return f"\nToken(value='{self.value}', type='{self.type}', line={self.line_number})"

# lexical analyzer class
class LexAnalyzer:
    def __init__(self, source_code, log_function=None):
        self.source_code = source_code # lolcode file content
        self.tokens = [] # empty list to store tokens
        self.current_position = 0 # used to track the current position of analyzer in the source code
        self.current_line = 1 # used to track the current line number for prompting error
        self.comment_block_active = False # flag to check if we are inside a comment block
        self.log_function = log_function # function to log errors to GUI or console

    # function to log error
    def log_error(self, message):
        error_message = f"Lexical Error: {message} at line {self.current_line}."

        if self.log_function:
            self.log_function(error_message) # pass the error to the gui
        else:
            print(error_message) # print the error to the console

    # function to advance the current position and update line number
    def advance_position(self, value):
        # count the number of newline characters in the matched token and update the line counter
        self.current_line += value.count('\n')
        self.current_position += len(value)

    # function to skip whitespace and update line numbers
    def skip_whitespace(self):
        while self.current_position < len(self.source_code) and self.source_code[self.current_position].isspace():
            if self.source_code[self.current_position] == '\n':
                self.current_line += 1
            self.current_position += 1

    # function to tokenize the source code
    def tokenize(self):
        while self.current_position < len(self.source_code):
            self.skip_whitespace() # skip any whitespace
            if self.current_position >= len(self.source_code):
                break # end of source code

            token = self.match_token() # try to match a token at the current position

            if token is not None: # if there is a token matched
                # handle token
                if token.type == 'Comment Line' and 'OBTW' in token.value:
                    self.comment_block_active = True

                elif token.type == 'Comment Line' and 'TLDR' in token.value:
                    self.comment_block_active = False
                    continue

                # lexical analyzer ignores anything inside comment blocks
                if self.comment_block_active:
                    continue

                if token is None:
                    continue # skip to the next iteration if no token is found

                # if the token is of type INVALID, stop processing and return an error
                if token.type == "INVALID":
                    self.log_error(f"Invalid token '{token.value}'")
                    return {"error": f"Invalid token '{token.value}' at line {self.current_line}"}  # Stop processing and return an error
                

                # handle YARN Literal
                elif token.type == 'YARN Literal' and token.value.startswith('"') and token.value.endswith('"'):
                    yarn_result = self.handle_yarn_literal(token)
                    if yarn_result is not None:  # If an error occurs
                        return yarn_result  # return the error message dictionary
                    
                else:
                    # Append non-comment tokens
                    self.tokens.append(token)

            else:
                # if no match, create an INVALID token
                invalid_char = self.source_code[self.current_position]
                if invalid_char == '\n':
                    self.current_line += 1
                self.current_position += 1  # Move forward to avoid infinite loop
                self.log_error(f"Invalid token '{invalid_char}'")
                return {"error": f"Invalid token '{invalid_char}' at line {self.current_line}"}

        self.handle_switch_case_variable()
        return self.tokens

    # aside from comment
    # we need to use regex to make sure to handle all actual keywords, delimiters, varident etc.
    def match_token(self):
        for pattern, type in token_patterns:
            regex = re.compile(pattern)
            match = regex.match(self.source_code, self.current_position)

            # if there is a match
            if match:
                value = match.group(0)

                # update current_position and current_line accordingly
                self.advance_position(value)

                if type == 'INVALID Keyword':  # Explicitly handle invalid keywords
                    self.log_error(f"Invalid use of keyword '{value}'. Did you forget the '?'?")
                    return Token("INVALID", value, self.current_line)

                # return single token if it's not a YARN Literal
                return Token(type, value, self.current_line)  # Return a token object with type and value

        # create an invalid token if no pattern matches
        invalid_value = self.source_code[self.current_position]
        self.current_position += 1  # Move forward to avoid infinite loop
        
        if invalid_value == '\n':
            self.current_line += 1
        return Token("INVALID", invalid_value, self.current_line)

    def handle_yarn_literal(self, token):
        # ensure the token is actually a YARN Literal
        if token.type == 'YARN Literal':
            # extract the string literal's components and add them as tokens
            self.tokens.append(Token("String Delimiter", "\"", self.current_line)) # opening quote
            self.tokens.append(Token("Literal", token.value[1:-1], self.current_line)) # content inside quotes
            self.tokens.append(Token("String Delimiter", "\"", self.current_line)) # closing quote
        else:
            # log an error if the token is not a valid YARN Literal
            self.log_error("Invalid YARN Literal token")
            return {"error": f"Invalid YARN Literal at line {self.current_line}"}
        
    def handle_switch_case_variable(self):
        updated_tokens = []
        i = 0
        while i < len(self.tokens) - 1:
            current_token = self.tokens[i]
            next_token = self.tokens[i + 1]
            if current_token.type == 'Variable Identifier' and next_token.value == 'WTF?':
                updated_tokens.append(Token('Switch-Case Variable', current_token.value, current_token.line_number))
                updated_tokens.append(next_token) # Append 'WTF?' as is
                i += 2  # Skip the next token ('WTF?')
            else:
                updated_tokens.append(current_token)
                i += 1
        if i < len(self.tokens):  # Append the last token if not already added
            updated_tokens.append(self.tokens[i])
        self.tokens = updated_tokens