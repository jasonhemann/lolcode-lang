import regex as re
import sys

lines = [] # contains strings per line of code

class Token:
    """
    Class to represent a token, including its type, value, and optionally its value type.
    The __repr__ method is designed to output a readable string representation for debugging.
    """
    def __init__(self, tokentype, tokenvalue, valuetype_ = None):
        # Initialize the token with its type, value, and an optional value type
        self.tokentype = tokentype
        self.tokenvalue = tokenvalue
        self.valuetype = valuetype_

    def __repr__(self) -> str:
        # Return a string representation for the Token instance
        return f"({self.tokentype}, \"{self.tokenvalue}\")"

def find_tldr(i, line):
    """
    Checks if the line contains the 'TLDR' keyword at the end, ensuring no extra content follows.
    If the line ends with 'TLDR', returns True. If 'TLDR' is present but not at the end, raises an error.
    
    Parameters:
        i (int): The line number, used for error reporting.
        line (str): The line to be checked.
    
    Returns:
        bool: True if the line ends with 'TLDR', False otherwise.
    """
    # Pattern to match the word 'TLDR' at the end of the line
    pattern = r'(\bTLDR\b)\s*$'

    # Search for a match with the pattern, which looks for 'TLDR' at the end
    match = re.search(pattern, line)

    if match:
        # If a match is found, the line ends with 'TLDR'
        return True
    else:
        # If 'TLDR' is not at the end of the line, check for any occurrence of 'TLDR' earlier in the line
        if re.search(r'\bTLDR\b', line):
            # If 'TLDR' is found but not at the end, print an error and terminate the program
            print(f"[CommentError] Wrong OBTW TLDR Comment Format Detected. {line}", i+1)      
        else:
            # If 'TLDR' is not present at all, return False
            return False

# Lexical Analyzer Function  
def lexical_analyzer(contents):
    global lines
    lines = contents.split('\n')  # Split input into lines
    lexeme = ""  # Temporary storage for building lexemes
    temp_word = "" # Storage to store the currently combined characters
    items = []  # List to store tokenized results
    obtwFound = False  # Flag to track the start of a block comment
    after_line_cont = False # checker for line continuation (line after ...)
    invalid_flag = False
    current_line = 1
    error_line = 0

    # Dictionary for multi-word keywords
    valid_keywords = {

        "HAI", "I HAS A", "SUM OF", "DIFF OF", "PRODUKT OF", "QUOSHUNT OF", "MOD OF", 
        "BIGGR OF", "SMALLR OF", "BOTH OF", "EITHER OF", "WON OF", "ANY OF", 
        "ALL OF", "BOTH SAEM", "IS NOW A", "O RLY?", "YA RLY", "NO WAI", 
        "IM IN YR", "HOW IZ I", "IF U SAY SO", "FOUND YR", "I IZ", "YR", "VISIBLE", "R",
        "IM OUTTA YR", "WAZZUP", "GIMMEH", "KTHXBYE", "SMOOSH", "MAEK", "WIN", "FAIL", "MKAY",
        "NOOB", "NUMBR", "NUMBAR", "YARN", "TROOF", "BUHBYE", "MEBBE", "WTF?", "OMG", "OMGWTF",
        "UPPIN", "NERFIN", "TIL", "WILE", "IM OUTTA YR", "GTFO", "OIC"
    }

    for i, line in enumerate(lines):
        # For Multi-Line Comments
        # Check if OBTW is found
       # Handle multi-line comments with OBTW and TLDR markers
        if obtwFound:
            if find_tldr(i, line):  # Check if TLDR (end of block comment) is found
                obtwFound = False  # End block comment
                lines[i] = ""  # Clear the line
                items.append(Token("Empty Line", line))
                current_line += 1
                continue
            else:
                lines[i] = ""   # Clear the line
                items.append(Token("Empty Line", line))
                current_line += 1
                continue
        
        # Detect the start of a multi-line comment (OBTW)
        pattern = r'^\s*(.*?)\bOBTW\b'
        match = re.match(pattern, line)
        if match:
            words_before_obtw = match.group(1).split()  # Split the part before OBTW
            
            if words_before_obtw:   # Error if words exist before OBTW
                print(f"[CommentError] Wrong OBTW TLDR Comment Format Detected. {line}", i+1)
            else:
                obtwFound = True  # Start block comment
                lines[i] = ""  # Clear the line
                items.append(Token("Empty Line", line))
                current_line += 1
                continue
        
        if line.strip() == "": # If the line is empty, add an item of empty space
            items.append(Token("Empty Line", line))
            current_line += 1
            continue
                
        # Tokenization logic
        chars = list(line)  # Split line into characters
        print(f"Debug: Processing line: '{line.strip()}' -> Characters: {chars}")  # Debug print for chars
        tokens = []  # List to store individual tokens
        in_quotes = False  # Flag to track whether we are inside quotes
        
        for char in chars: # Check all of the characters in the line
            if char == '"':
                print(f"Debug: '{lexeme}' is the current lexeme for \"")
                # If there is still a lexeme 
                if lexeme == "AN":
                    tokens.append(lexeme)
                    lexeme = ""
                    
                elif lexeme and lexeme not in valid_keywords:
                    print(f"Debug: Skipping '{lexeme}' as it's part of a multi-word keyword")
                    invalid_flag = True
                    error_line = current_line

                if in_quotes:  # Closing quote for string literals
                    lexeme = temp_word
                    tokens.append(lexeme)
                    temp_word = ""
                    lexeme = ""
                tokens.append(char)  # Add the quote itself as a token
                in_quotes = not in_quotes  # Toggle the in_quotes flag

            elif char == " " and not in_quotes:
                # After encountering a space, check if the lexeme is part of a multi-word keyword
                print(f"Debug: '{temp_word}' is the current temp_word")
                print(f"Debug: '{lexeme}' is the current lexeme")
                if temp_word: # temp_word is not empty
                    if lexeme: # lexeme is not empty
                        print(f"Debug: '{(lexeme + ' ' + temp_word)}' checker if valid")
                        # Check if lexeme is a 1 or 2 letter valid keywords and possible lexeme does not form a valid keyword
                        if (lexeme == "AN" or lexeme == "A" or lexeme == "YR" or lexeme == "R") and not any(kw.startswith(lexeme + " " + temp_word) for kw in valid_keywords):
                            tokens.append(lexeme) # add the 1 or 2 letter valid keyword to the tokens
                            if any(kw.startswith(temp_word) for kw in valid_keywords): # Check if the temp word is the same with some of the starting letters or words of valid keywords 
                                lexeme = temp_word 
                                temp_word = ""
                                continue
                            elif any(temp_word in kw for kw in valid_keywords): # Check if temp word is a substring of a valid keyword
                                # This will tell us to not add that token to the tokens since it's just a part of a valid keyword
                                invalid_flag = True
                                error_line = current_line
                                temp_word = ""
                                lexeme = ""
                                continue
                            else: # No match, add the temp word 
                                tokens.append(temp_word)
                                lexeme = ""
                                temp_word = ""
                                continue
                        # elif any(kw.startswith(lexeme) for kw in valid_keywords) and (not any(temp_word in kw for kw in valid_keywords) or temp_word == "IT"):
                        #     tokens.append(temp_word)
                        #     invalid_flag = True
                        #     error_line = current_line
                        #     lexeme = ""
                        #     temp_word = ""
                        #     continue
                        else: # if no match, build the possible lexeme
                            potential_lexeme = lexeme + " " + temp_word 
                    else: # if lexeme is empty, assign the value of the temp_word to it
                        potential_lexeme = temp_word

                    print(f"Debug: '{potential_lexeme}' is the current potential_lexeme")
                    # Check if the possible lexeme will build a valid keyword
                    if any(kw.startswith(potential_lexeme) for kw in valid_keywords):
                        print(f"Debug: '{potential_lexeme}' is a valid prefix, continue building")
                        if potential_lexeme in valid_keywords: # if the possible lexeme is in the valid keyword,
                            tokens.append(potential_lexeme) # add if to the tokens
                            print(f"Debug: Added final multi-word lexeme '{potential_lexeme}' to tokens")
                            lexeme = ""
                            temp_word = ""
                        else: # Continue building the lexeme
                            lexeme = potential_lexeme 
                            print(f"Debug: '{lexeme}' is the current lexeme")
                            temp_word = ""  # Reset the temp_word after adding it to the lexeme
                            continue  # Move to the next character without adding space to tokens
                    else:
                        # check if lexeme and is not empty and temp word is a substring of a valid keyword
                        # this will tell us that the lexeme is invalid and we should check and build the temp word
                        if lexeme and any(temp_word in kw for kw in valid_keywords):
                            lexeme = temp_word
                            invalid_flag = True
                            error_line = current_line
                            temp_word = ""
                            continue
                        # if lexeme is empty, check if the temp word is just a part of a valid keyword (meaning it will not build up to the valid keyword)
                        elif any(temp_word in kw for kw in valid_keywords):
                            print(f"Debug: Skipping '{temp_word}' as it's part of a multi-word keyword")
                            invalid_flag = True
                            temp_word = "" 
                            error_line = current_line
                            continue  # Skip adding 'OF' or other similar words to the tokens
                            
                        # Finalize the current lexeme as an identifier or non-keyword token
                        lexeme = temp_word  # store the current value of temp word to lexeme
                        if lexeme:
                            tokens.append(lexeme)
                            print(f"Debug: Added '{lexeme}' as a valid token")
                            lexeme = ""
                            
                        temp_word = ""  # Reset temp_word
                
            else:  # Handle all other characters
                temp_word += char  # Append current character to temp_word

        # Finalize the remaining lexeme if any
        print(f"Debug: final tempword {temp_word}")
        if temp_word: # temp_word is not empty
            if lexeme == "AN" or lexeme == "A" or lexeme == "YR" or lexeme == "R": # Explicitly use 1 and 2 letter valid keyword to append it to the tokens
                    tokens.append(lexeme)
                    print(f"Debug: Added valid keyword 'AN' to tokens")
                    lexeme = ""

            if lexeme: # lexeme is not empty
                potential_lexeme = lexeme + " " + temp_word # Build the possible lexeme
                print(f"Debug: '{potential_lexeme}' is the current final potential_lexeme")
                
                # Check if the current lexeme is the same with some of the starting letters or words of valid keywords 
                if any(kw.startswith(potential_lexeme) for kw in valid_keywords):
                    if potential_lexeme in valid_keywords: # If the possible lexeme is in the valid keywords,
                        tokens.append(potential_lexeme) # add the possible lexeme to the tokens
                        print(f"Debug: Added final multi-word lexeme '{potential_lexeme}' to tokens")
                    elif any(potential_lexeme in kw for kw in valid_keywords): # If the possible lexeme is only a substring,
                        invalid_flag = True # Flag the current token as invalid
                        error_line = current_line
                    else: # No match
                        tokens.append(temp_word)
                        error_line = current_line
                        invalid_flag = True

                    # Reset lexeme and temp_word
                    lexeme = ""
                    temp_word = ""

                else:
                    tokens.append(temp_word)
                    error_line = current_line
                    invalid_flag = True
                    lexeme = ""
                    temp_word = ""

            elif any(temp_word in kw for kw in valid_keywords):
                if any(kw.startswith(temp_word) for kw in valid_keywords):
                    if temp_word not in valid_keywords:
                        invalid_flag = True
                        temp_word = ""  
                        error_line = current_line
                    else:
                        tokens.append(temp_word)
                        print(f"Debug: Added final lexeme '{temp_word}' to tokens")
                        temp_word = ""
                elif temp_word == "IT":
                    tokens.append(temp_word)
                    temp_word = ""
                else:
                    invalid_flag = True
                    temp_word = "" 
                    error_line = current_line
            else:
                tokens.append(temp_word)
                print(f"Debug: Added final lexeme '{temp_word}' to tokens")
                temp_word = ""
                
        current_line += 1 # Increment the current_line             
        print(tokens)
        tokens.append("\n")  # Add newline as a token
        
        
        # Process each token in the list and classify it
        num_quote = 0
        line_cont = False # Checker for line continuation
        for j,token in enumerate(tokens):
            if token == '"':  # Handle string delimiters
                num_quote += 1
                if num_quote == 2:
                    num_quote = 0
                items.append(Token("String Delimiter", token))
            elif j > 0 and j < len(tokens)-1 and num_quote == 1 and tokens[j+1] == '"' and tokens[j-1] == '"':
                items.append(Token("String Literal", token))
            
            # Comments
            # If comment are seen, show error because it must already be deleted from the start of the program
            elif re.fullmatch(r"BTW", token):
                # show error message and end program
                print(f"[CommentError] Wrong OBTW TLDR Comment Format Detected. {line}", i+1)

            elif re.fullmatch(r"OBTW", token):
                print(f"[CommentError] Wrong OBTW TLDR Comment Format Detected. {line}", i+1)  
            elif re.fullmatch(r"TLDR", token):
                print(f"[CommentError] Wrong OBTW TLDR Comment Format Detected. {line}", i+1)          

            # Tokenize specific keywords, literals, and operators
            elif re.fullmatch(r"WIN|FAIL", token):
                items.append(Token("Troof Literal", token))
            elif re.fullmatch(r"NOOB|NUMBR|NUMBAR|YARN|TROOF", token):
                items.append(Token("Type Literal", token))
            elif re.fullmatch(r"HAI", token):
                items.append(Token("Start Code Delimiter", token))
            elif re.fullmatch(r"KTHXBYE", token):
                items.append(Token("End Code Delimiter", token))
            
            # Variable declarations and assignments
            elif re.fullmatch(r"WAZZUP", token):
                items.append(Token("Start Var Declaration Delimiter", token))
            elif re.fullmatch(r"BUHBYE", token):
                items.append(Token("End Var Declaration Delimiter", token))
            elif re.fullmatch(r"I HAS A", token):
                items.append(Token("Variable Declaration", token))
            elif re.fullmatch(r"ITZ", token):
                items.append(Token("Variable Assignment", token))
            elif re.fullmatch(r"R", token):
                items.append(Token("Variable Value Reassignment", token))
                        
            # Arithmetic operations and keywords
            elif re.fullmatch(r"AN", token):
                items.append(Token("And Keyword", token))
            elif re.fullmatch(r"SUM OF", token):
                items.append(Token("Add Keyword", token))
            elif re.fullmatch(r"DIFF OF", token):
                items.append(Token("Subtract Keyword", token))
            elif re.fullmatch(r"PRODUKT OF", token):
                items.append(Token("Multiply Keyword", token))
            elif re.fullmatch(r"QUOSHUNT OF", token):
                items.append(Token("Divide Keyword", token))
            elif re.fullmatch(r"MOD OF", token):
                items.append(Token("Modulo Keyword", token))
            elif re.fullmatch(r"BIGGR OF", token):
                items.append(Token("Return Larger Number Keyword",token))
            elif re.fullmatch(r"SMALLR OF", token):
                items.append(Token("Return Smaller Number Keyword",token))

            # Boolean operations
            elif re.fullmatch(r"BOTH OF", token):
                items.append(Token("Both True Check Keyword",token))
            elif re.fullmatch(r"EITHER OF", token):
                items.append(Token("One or Both True Check Keyword",token))
            elif re.fullmatch(r"WON OF", token):
                items.append(Token("Exactly One is True Check Keyword",token))
            elif re.fullmatch(r"NOT", token):
                items.append(Token("Negate Keyword", token))
            elif re.fullmatch(r"ANY OF", token):
                items.append(Token("Atleast One True Check Keyword", token))
            elif re.fullmatch(r"ALL OF", token):
                items.append(Token("All True Check Keyword", token))

            # Comparison operations
            elif re.fullmatch(r"BOTH SAEM", token):
                items.append(Token("Both Argument Equal Check Keyword", token))
            elif re.fullmatch(r"DIFFRINT", token):
                items.append(Token("Both Argument Not Equal Check Keyword", token))
            
            # Miscellaneous operations
            elif re.fullmatch(r"SMOOSH", token):
                items.append(Token("Concatenation Keyword", token))
            elif re.fullmatch(r"MAEK", token):
                items.append(Token("Typecast Keyword", token))
            elif re.fullmatch(r"A", token):
                items.append(Token("Typecast Prefix", token))
            elif re.fullmatch(r"IS NOW A", token): 
                items.append(Token("Full Typecast Keyword", token))

            # Input/Output Keyword
            elif re.fullmatch(r"VISIBLE", token):
                items.append(Token("Print Keyword", token))
            elif re.fullmatch(r"GIMMEH", token):
                items.append(Token("Input Keyword", token))

            # Flow-control Keywords
            elif re.fullmatch(r"O RLY\?", token):
                items.append(Token("if Keyword", token))
            elif re.fullmatch(r"YA RLY", token):
                items.append(Token("if true Keyword", token))
            elif re.fullmatch(r"MEBBE", token):
                items.append(Token("else if Keyword", token))
            elif re.fullmatch(r"NO WAI", token):
                items.append(Token("else Keyword", token))
            elif re.fullmatch(r"OIC", token):
                items.append(Token("End of if Block Keyword", token))    

            # Switch-case keywords 
            elif re.fullmatch(r"WTF\?", token):
                items.append(Token("Switch Keyword", token))     
            elif re.fullmatch(r"OMG", token):
                items.append(Token("Switch Case Keyword", token))   
            elif re.fullmatch(r"OMGWTF", token):
                items.append(Token("Switch Default Keyword", token))

            # Loop Keywords, and Increment and Decrement Keywords
            elif re.fullmatch(r"IM IN YR", token):
                items.append(Token("Explicit Start Loop Keyword", token))
            elif re.fullmatch(r"UPPIN", token):
                items.append(Token("Increment Keyword",token)) 
            elif re.fullmatch(r"NERFIN", token):
                items.append(Token("Decrement Keyword", token))   
            elif re.fullmatch(r"YR", token):
                items.append(Token("Parameter Separator Keyword", token))   
            elif re.fullmatch(r"TIL", token):
                items.append(Token("Until indicated end of loop Keyword", token))
            elif re.fullmatch(r"WILE", token):
                items.append(Token("While indicated end of loop Keyword", token))   
            elif re.fullmatch(r"IM OUTTA YR", token):
                items.append(Token("Break Loop Keyword", token))

            # Function and return statements
            elif re.fullmatch(r"HOW IZ I", token):
                items.append(Token("Define Function Keyword", token))
            elif re.fullmatch(r"IF U SAY SO", token):
                items.append(Token("End of Function Keyword", token))
            elif re.fullmatch(r"GTFO", token):
                items.append(Token("General Purpose Break Keyword", token))
            elif re.fullmatch(r"FOUND YR", token):
                items.append(Token("Return Keyword", token))
            elif re.fullmatch(r"I IZ", token):
                items.append(Token("Function Call", token))
            elif re.fullmatch(r"MKAY", token):
                items.append(Token("End of assignment Keyword", token))

           # Handle variables and literals
            elif re.fullmatch(r"[a-zA-Z][a-zA-Z0-9_]*", token):
                items.append(Token("Variable Identifier", token))
            elif re.fullmatch(r"-?([1-9][0-9]*|0)", token):
                items.append(Token("Numbr Literal", int(token)))
            elif re.fullmatch(r"-?(0|[1-9][0-9]*)(\.[0-9]+)?", token):
                items.append(Token("Numbar Literal", float(token)))
            
            # Handle miscellaneous lexemes (newlines, empty strings, etc.)
            elif re.fullmatch(r"\n", token):
                if line_cont:
                    line_cont = False
                    after_line_cont = True
                    continue
                else:
                    if after_line_cont:
                        after_line_cont = False
                        items.append(Token("Linebreak", "\\n"))
                        # Append the empty line for correct line numbering
                        items.append(Token("Empty Line", ""))
                    else: 
                        items.append(Token("Linebreak", "\\n"))
            elif re.fullmatch(r"", token):
                items.append(Token("Epsilon", token))
            # elif re.fullmatch(r".*", token):
            #     items.append(Token("any", token))
            elif re.fullmatch(r"\+", token):
                items.append(Token("Print Concatenation Keyword", token))
            elif re.fullmatch(r"!", token):
                items.append(Token("Suppress Newline", token))
            elif re.fullmatch(r"\.\.\.", token):
                # If the next token is not linebreak, error, else do not add to items: ... and linebreak
                if tokens[j+1] != "\n":
                    print(f"[SyntaxError] Invalid token ({token}) Token after ... should be linebreak", i+1)
                else:
                    line_cont = True
                    continue
            else:
                print(f"[LexerError] Invalid Token Detected.", i+1)

    if invalid_flag:
        items.insert(0, Token("Invalid", f"line {error_line}"))

    # Print all the tokenized items
    for item in items:
        print(item)        
    return items

# Parse the function for terminal
def parse_terminal(file):
    contents = open(file, 'r').read()
    contents.replace('\t', '    ') # Change the tabs to 4 spaces
    contents = re.sub(r"(?<!O)BTW.*?(?=\n)", "", contents) # Remove the comments by deleting BTW and contents after it before the new line
    tokens = lexical_analyzer(contents)
    return tokens

# Parse the function for the GUI
def parse_tkinter(code):
    print(repr(code)) # Printable representation of contents
    code = re.sub(r"(?<!O)BTW.*?(?=\n)", "", code) # Remove the comments by deleting BTW and contents after it before the new line
    tokens = lexical_analyzer(code)
    return tokens

# if __name__ == '__main__':
#     print(parse(sys.argv[1]))