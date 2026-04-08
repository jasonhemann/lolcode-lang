import re
from data.lexemes import lexemes # Import the lexemes from lexemes.py


# -----------------------------------------------------------------------------------------
#  FUNCTION: Finds lexemes in the current line of code
# ----------------------------------------------------------------------------------------- 
def process_line(line_no, line_of_code):
    line_of_code = line_of_code.strip()
    code = line_of_code
    found_lexemes = []

    if len(line_of_code) == 0:
        return found_lexemes
    # Handle multiline comments
    if "OBTW" in line_of_code:
        found_lexemes.append(('OBTW', 'Multiline Comment Start', line_no))
        return found_lexemes
    elif "TLDR" in line_of_code:
        found_lexemes.append(('TLDR', 'Multiline Comment End', line_no))
        return found_lexemes
    
    # FOR KEYWORDS
    # tokenize the line of code
    keywords = re.findall(
        r'(?<!")(\bHAI\b|\bKTHXBYE\b|\bBTW\b|\bI HAS A\b|\bITZ\b|\bSUM OF\b|'
        r'\bDIFF OF\b|\bPRODUKT OF\b|\bQUOSHUNT OF\b|\bMOD OF\b|\bBIGGR OF\b|'
        r'\bSMALLR OF\b|\bBOTH OF\b|\bEITHER OF\b|\bWON OF\b|\bNOT\b|\bANY OF\b|'
        r'\bALL OF\b|\bBOTH SAEM\b|\bDIFFRINT\b|\bSMOOSH\b|\bMAEK\b|\bIS NOW A\b|'
        r'\bVISIBLE\b|\bGIMMEH\b|O RLY\?|\bYA RLY\b|\bMEBBE\b|\bNO WAI\b|\bOIC\b|'
        r'WTF\?|\bOMG\b|\bOMGWTF\b|\bIM IN YR\b|\bUPPIN\b|\bNERFIN\b|\bYR\b|\bTIL\b|'
        r'\bWILE\b|\bIM OUTTA YR\b|\bHOW IZ I\b|\bIF U SAY SO\b|\bGTFO\b|\bFOUND YR\b|'
        r'\bI IZ\b|\bMKAY\b|\bAN|\bBUHBYE\b|\bWAZZUP\b|\bA\b|\bR\b|\,|\.\.\.)(?!")',
        line_of_code
    )
    keywords.extend(re.findall(r'[\+]\s', line_of_code)) # find visibile operand separator/concatenator
    if keywords:
        for keyword in keywords:
            for pattern, type_lxm in lexemes.items():
                if re.fullmatch(pattern, keyword):
                    idx = re.search(rf'{re.escape(keyword)}', code).start()
                    found_lexemes.append((keyword,type_lxm,line_no,idx))
                    code = re.sub(rf'{re.escape(keyword)}',f'{" " * len(keyword)}',code,1) # replace the first instance of the keyword in the string (will be used to sort the lexemes)
                    line_of_code = re.sub(rf'{re.escape(keyword)}',f'{" " * len(keyword)}',line_of_code,1) # filter line of code
                    break
    
    # FOR LITERALS
    # tokenize the line of code
    literals = re.findall(
        r'-?[0-9]+\.[0-9]+\b|-?[0-9]+\b|\b[0-9]+\b|\bWIN\b'
        r'\bFAIL\b|\bNUMBR\b|\bNUMBAR\b|\bYARN\b|\bTROOF\b|'
        r'\bNOOB\b|\"[^\"]*\"', 
        line_of_code
    )
    
    
    if literals:
        for literal in literals:
            for pattern, type_lxm in lexemes.items():
                if re.fullmatch(pattern, literal):    
                    if literal.startswith('"'): # handles YARN literals only
                        idx = re.search(re.escape(literal), code).start()
                        code = re.sub(re.escape(literal),f'{" " * len(literal)}',code,1) # replace the first instance of the literal in the string (will be used to sort the lexemes)
                        line_of_code = re.sub(re.escape(literal),f'{" " * len(literal)}',line_of_code,1) # filter line of code
                    else:
                        idx = re.search(rf'(?<!\S){re.escape(literal)}(?!\S)', code).start()
                        code = re.sub(rf'\b{literal}',f'{" " * len(literal)}',code,1) # replace the first instance of the literal in the string (will be used to sort the lexemes)
                        line_of_code = re.sub(rf'\b{literal}',f'{" " * len(literal)}',line_of_code,1) # filter line of code
                    found_lexemes.append((literal,type_lxm,line_no,idx))
                    break
    
    # FOR IDENTIFIERS
    identifiers = re.findall(r"\b[A-Za-z][A-Za-z0-9_]*\b", line_of_code)
    if identifiers:
        for identifier in identifiers:
            for pattern, type_lxm in lexemes.items():
                if re.fullmatch(pattern, identifier):
                    idx = re.search(rf'{identifier}', code).start()
                    found_lexemes.append((identifier, type_lxm, line_no,idx))
                    code = re.sub(rf'{identifier}',f'{' '*len(identifier)}',code,1) # replace the first instance of the identifier in the string (will be used to sort the lexemes)
                    break
    
    # return lexemes found in line of code (sorted using their index in the line_of_code)
    final_lexemes = [] # tuple made up of: (lexeme, type_lxm, line no)
    for lexeme in sorted(found_lexemes, key=lambda x: x[3]):
        final_lexemes.append((lexeme[0],lexeme[1],lexeme[2])) 
    return final_lexemes

# -----------------------------------------------------------------------------------------
#  FUNCTION: Main lexical analyzer
# ----------------------------------------------------------------------------------------- 
def find_lexemes_from_string(code_string):
    all_lexemes =[] # array tuples: (lexeme, description, line number)
    lines = code_string.splitlines()
    
    # handling BTW
    i = 0
    while i < len(lines):
        line = lines[i]
        if line == '':
            # print('here1')
            lines[i] = ''
            i+=1
            continue
        if "OBTW" in line:
            # skip OBTW (will be handled in process_line fxn)
            i += 1
            continue
        elif 'BTW' in line:
            x = line.find('BTW')
            if x == 0: 
                # lines.pop(i) # remove BTW statement 
                lines[i] = ''
                continue
            else:  # inline BTW
                line = line[:x]  # only statement portion from the line will be left
                lines[i] = line
        # move to next line
        i += 1
    # handles soft-line breaks
    i = 0
    while i < len(lines):
        line = lines[i]
        # extracts all quoted substrings from the line 
        if line == '':
            # print('here2')
            lines[i] = ''
            i+=1
            continue
        
        quoted_parts = re.findall(r'\"[^\"]*\"', line) # used to prevent splitting within quotes.
        split_needed = False
        for part in line.split(","):
            # check if any part of line outside quotes requires splitting 
            if not any(part in q for q in quoted_parts): 
                split_needed = True
                break
        if split_needed:
            # split the line by commas not inside quotes
            new_line = []
            current = []
            inside_quotes = False
            for char in line:
                if char == '"':
                    # first '"' encountered indicate start of YARN will only change back to False is second '"' is encountered
                    inside_quotes = not inside_quotes 
                
                # if comma encountered and not in YARN
                if char == ',' and not inside_quotes:
                    # append current segment in newline
                    new_line.append(''.join(current).strip()) # strip() whitespaces
                    current = [] # reset for the next segment
                else:
                    # append char to build the statement
                    current.append(char)
            
            if current: # not empty, remaining characters
                # append current to newline
                new_line.append(''.join(current).strip())

            lines[i:i+1] = new_line # replace original 
            # skip over the newly inserted lines
            i += len(new_line)
        else:
            # Move to the next if no split is needed
            i += 1

    # handles line continuation
    j = 0
    while j < len(lines) - 1:
        line = lines[j]
        if line == '':
            # print('here3')
            lines[j] = ''
        else:
            while line.endswith("...") or line.endswith("... ") or line.endswith("...\n") or line.endswith("...\t"):
                lines[j] = line + " " + lines[j + 1] # combine lines
                lines.pop(j + 1)  # remove the next line after merging
                line = lines[j]  # update line to the merged one
        j += 1  # proceed to next line
    
    multi_comment = False
    for line_no, line in enumerate(lines):
        stripped_line = line.strip()
        results = process_line(line_no, line)

        # Check for improper placement of OBTW or TLDR
        if 'OBTW' in stripped_line or 'TLDR' in stripped_line:
            if not stripped_line.startswith('OBTW') and not stripped_line.startswith('TLDR'):
                print(f"Error: Improper placement of OBTW or TLDR on line {line_no + 1}")

        if [(lexeme, description) for lexeme, description, _ in results] == [('OBTW', 'Multiline Comment Start')]:  # Handle multiline comment
            multi_comment = True   # Mark the start of the multi-comment

        elif [(lexeme, description) for lexeme, description, _ in results] == [('TLDR', 'Multiline Comment End')]:
            multi_comment = False   # Mark the end of the multi-comment
        elif multi_comment: # Continue if multi-comment
            continue

        else:
            all_lexemes.extend(results)  # Add lexemes from current line
    
    return all_lexemes