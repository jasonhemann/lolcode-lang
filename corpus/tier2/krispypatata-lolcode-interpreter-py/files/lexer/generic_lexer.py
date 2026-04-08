import sys
import re

# ═════════════════════════════════════════════════════════════════════════════════════════════════
# LEXER
# ═════════════════════════════════════════════════════════════════════════════════════════════════
# Function for tokenizing a string of characters based on a set of token patterns.
def lex(characters, token_exprs):
    pos = 0             # Current position in the input string
    tokens = []         # List to hold the tokenized output
    line_number = 1     # Start with line number 1

    # Traverse through the contents of the input
    while pos < len(characters):
        match = None # Flag to track whether a match is found for the current position

        # traverse through the list of regex patterns for tokens
        for token_expr in token_exprs:
            pattern, tag = token_expr               # Extract regex pattern and tag from token_expr; ex. ('HAI', 'Reserved')
            regex = re.compile(pattern)             # Compile the regex
            match = regex.match(characters, pos)    # Try to match the pattern at the current position
            
            # If there's a match, get the matched text
            if match:
                text = match.group(0)

                # But only add token to the list if it has a valid tag 
                if tag:
                    token = (text, tag, line_number)
                    tokens.append(token)

                # Update line count if a newline is encountered in the matched text
                line_number += text.count('\n')

                 # Exit the loop once a match is found
                break

        # If there's no match found, then there's an error
        if not match:
            sys.stderr.write("Illegal character: '%s' at %d\n" % (characters[pos], line_number))
            sys.exit(1)
        
        # If match found, move the position pointer to the end of the matched text
        else:
            pos = match.end(0)
    
    # Return the list of tokens
    return tokens
