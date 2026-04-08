# Author: Christian Olo
# Program Description: A LOLCode interpreter developed using python

# source code for the lexer

import re
from collections import deque
from Tokens import Token                    # uses the tokens class to store valid tokens

# accepted tokens
TOKENS = [
    (r"^HAI\s", "Code Start"),
    (r"^KTHXBYE$", "Code End"),
    (r"^BTW\s", "Comment Delimiter"),
    (r"^OBTW\s", "Multiline Comment Start"),
    (r"^TLDR\s", "Multiline Comment End"),
    (r"^I HAS A\s", "Variable Declaration"),
    (r"^ITZ\s", "Variable Assignment"),
    (r"^R\s", "Assignment"),
    (r"^SUM OF\s", "Addition"),
    (r"^DIFF OF\s", "Subtraction"),
    (r"^PRODUKT OF\s", "Multiplication"),
    (r"^QUOSHUNT OF\s", "Division"),
    (r"^MOD OF\s", "Modulo"),
    (r"^BIGGR OF\s", "Max"),
    (r"^SMALLR OF\s", "Min"),
    (r"^BOTH OF\s", "And"),
    (r"^EITHER OF\s", "Or"),
    (r"^WON OF\s", "Xor"),
    (r"^NOT\s", "Not"),
    (r"^ANY OF\s", "Infinite Or"),
    (r"^ALL OF\s", "Infinite And"),
    (r"^AN\s", "Operation Delimiter"),
    (r"^MKAY\s", "Infinite Bool End"),
    (r"^BOTH SAEM\s", "Equality Check"),
    (r"^DIFFRINT\s", "Inequality Check"),
    (r"^SMOOSH\s", "Concatenate"),
    (r"^MAEK\s", "Maek Keyword"),
    (r"^A\s", "A Keyword"),
    (r"^IS NOW A\s", "Typecast Keyword"),
    (r"^VISIBLE\s", "Output Keyword"),
    (r"^GIMMEH\s", "Input Keyword"),
    (r"^O RLY\?\s", "If-else Start"),
    (r"^YA RLY\s", "If Keyword"),
    (r"^MEBBE\s", "Else-if Keyword"),
    (r"^NO WAI\s", "Else Keyword"),
    (r"^OIC\s", "If-else End"),
    (r"^WTF\?\s", "Switch-case Start"),
    (r"^OMG\s", "Case Keyword"),
    (r"^OMGWTF\s", "Case Default Keyword"),
    (r"^IM IN YR\s", "Loop Start"),
    (r"^UPPIN\s", "Loop Operation"),
    (r"^NERFIN\s", "Loop Operation"),
    (r"^YR\s", "Loop Delimiter"),
    (r"^TIL\s", "Condition Keyword"),
    (r"^WILE\s", "Condition Keyword"),
    (r"^IM OUTTA YR\s", "Loop End"),
    (r"^GTFO\s", "Break"),
    (r"^IT\s", "Implicit Variable"),
    (r"^(WIN|FAIL)\s", "Troof Literal"),
    (r"-?[0-9]+\.[0-9]+\s", "Numbar Literal"),
    (r"-?[0-9]+\s", "Numbr Literal"),
    (r"\"[^\"]*\"\s", "Yarn Literal"),
    (r"^(NOOB|NUMBR|NUMBAR|YARN|TROOF)\s", "Data Type"),
    (r"^[a-zA-Z][a-zA-Z0-9_]*\s", "Variable Identifier")
]

class Lexer:
    def __init__(self, text):
        self.text = text
        self.err = ''           # for printing the error if any

    # tokenizes the provided text
    def tokenize(self):
        tokens = deque()                # stores valid token objects
        lines = self.text.split('\n')
        line_no = 1
        in_comment = False

        # iterates through each line of the source code
        for line in lines:
            line = line.strip()+'\n'    # strips leading and trailing spaces
            hasToken = False
            if line == '\n':            # empty line
                tokens.append(Token('Linebreak', '\\n', line_no))
            else:
                while(line !='' and line != '\n'):       # while there are possible tokens
                    hasToken = True
                    # if in multiline comment
                    if(in_comment):
                        tldr_check = re.search(r"\sTLDR\s", line)
                        if(line[:4] == 'TLDR'):
                            token_value = matched_token.group(0)
                            tokens.append(Token('Multiline Comment End', line[:4], line_no))
                            line = line[4:].lstrip()
                            in_comment = False
                        elif(tldr_check):
                            tokens.append(Token('Multiline Comment End', 'TLDR', line_no))
                            line = line[tldr_check.end():]
                            in_comment = False
                        else:
                            tokens.append(Token('Comment', line[:-1], line_no))
                            line = line[len(line):]
                        continue
                    # checks the list of provided valid tokens if one would match the current lin
                    for token in TOKENS:       
                        pattern, type = token
                        matched_token = re.match(pattern, line)         # checks if curr token match the line
                        if(matched_token):      # a token is matched
                            if type == 'Comment Delimiter':
                                token_value = matched_token.group(0)
                                tokens.append(Token(type, token_value.strip(), line_no))
                                line = line[matched_token.end():].lstrip()
                                tokens.append(Token('Comment', line[:-1].strip(), line_no))
                                line = line[len(line):]
                                break
                            elif type == 'Multiline Comment Start':
                                token_value = matched_token.group(0)
                                tokens.append(Token(type, token_value.strip(), line_no))
                                line = line[-1:].lstrip()
                                in_comment = True  
                            elif type == 'Yarn Literal':
                                temp_token = matched_token.group(0)
                                tokens.append(Token('String Delimiter', '"', line_no))
                                tokens.append(Token(type, temp_token[1:-2], line_no))
                                tokens.append(Token('String Delimiter', '"', line_no))
                            else:
                                token_value = matched_token.group(0)
                                tokens.append(Token(type, token_value.strip(), line_no))
                            line = line[matched_token.end():].lstrip()      # removes the matched word from the line
                            break
                    if(not matched_token and not in_comment):               # raises invalid tokens
                        self.err = f"Error:{line_no}:Invalid token {line}"
                        raise Exception()
                if(hasToken and not in_comment):
                    tokens.append(Token('Linebreak', '\\n', line_no))
            line_no += 1
        tokens.append(Token('End of File', 'EOF', line_no))                 # for checking EOF
        return tokens  