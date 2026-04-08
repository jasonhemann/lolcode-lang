import re

KEYWORDS = {
    "Code Start": r"^HAI\s",
    "Code End": r"^KTHXBYE$",
    "Comment Delimiter": r"^BTW\s",
    "Multiline Comment Start": r"^OBTW\s",
    "Multiline Comment End": r"^TLDR\s",
    "Variable Declaration": r"^I HAS A\s",
    "Variable Assignment": r"^ITZ\s",
    "Assignment": r"^R\s",
    "Addition": r"^SUM OF\s",
    "Subtraction": r"^DIFF OF\s",
    "Multiplication": r"^PRODUKT OF\s",
    "Division": r"^QUOSHUNT OF\s",
    "Modulo": r"^MOD OF\s",
    "Max": r"^BIGGR OF\s",
    "Min": r"^SMALLR OF\s",
    "And": r"^BOTH OF\s",
    "Or": r"^EITHER OF\s",
    "Xor": r"^WON OF\s",
    "Not": r"^NOT\s",
    "Infinite Or": r"^ANY OF\s",
    "Infinite And": r"^ALL OF\s",
    "Operation Delimiter": r"^AN\s",
    "Infinite Bool End": r"^MKAY\s",
    "Equality Check": r"^BOTH SAEM\s",
    "Inequality Check": r"^DIFFRINT\s",
    "Concatenate": r"^SMOOSH\s",
    "Maek Keyword": r"^MAEK\s",
    "A Keyword": r"^A\s",
    "Typecast Keyword": r"^IS NOW A\s",
    "Output Keyword": r"^VISIBLE\s",
    "Input Keyword": r"^GIMMEH\s",
    "If-else Start": r"^O RLY\?\s",
    "If Keyword": r"^YA RLY\s",
    "Else-if Keyword": r"^MEBBE\s",
    "Else Keyword": r"^NO WAI\s",
    "If-else End": r"^OIC\s",
    "Switch-case Start": r"^WTF\?\s",
    "Case Keyword": r"^OMG\s",
    "Case Default Keyword": r"^OMGWTF\s",
    "Loop Start": r"^IM IN YR\s",
    "Loop Operation": r"^(UPPIN|NERFIN)\s",
    "Loop Delimiter": r"^YR\s",
    "Condition Keyword": r"^(TIL|WILE)\s",
    "Loop End": r"^IM OUTTA YR\s",
    "Break": r"^GTFO\s",
    "Implicit Variable": r"^IT\s",
    "Troof Literal": r"^(WIN|FAIL)\s",
    "Numbar Literal": r"^-?\d+\.\d+$",
    "Numbr Literal": r"^-?\d+$",
    "Yarn Literal": r"\"[^\"]*\"\s",
    "Data Type": r"^(NOOB|NUMBR|NUMBAR|YARN|TROOF)\s",
    "Variable Identifier": r"[A-Za-z][A-Za-z0-9_]*"
}

# Token function to create a token
def create_token(type_, value, line_num):
    return {"type": type_, "value": value, "line_num": line_num}

# Lexer function to tokenize the text
def tokenize(text):
    tokens = []
    lines = text.split('\n')
    line_no = 1
    in_comment = False

    for line in lines:
        line = line.strip() + '\n'
        hasToken = False
        tok_line = []

        if line == '\n':
            tok_line.append(create_token('Linebreak', '\\n', line_no))
        else:
            while line != '' and line != '\n':
                hasToken = True

                if in_comment:
                    tldr_check = re.search(r"\sTLDR\s", line)
                    if line[:4] == 'TLDR' or tldr_check:
                        tok_line.append(create_token('Multiline Comment End', 'TLDR', line_no))
                        line = line[4:].lstrip() if line[:4] == 'TLDR' else line[tldr_check.end():]
                        in_comment = False
                    else:
                        tok_line.append(create_token('Comment', line[:-1], line_no))
                        line = line[len(line):]
                    continue

                for type_, pattern in KEYWORDS.items():
                    matched_token = re.match(pattern, line)

                    if matched_token:
                        if type_ == 'Comment Delimiter':
                            token_value = matched_token.group(0)
                            tok_line.append(create_token(type_, token_value.strip(), line_no))
                            line = line[matched_token.end():].lstrip()
                            tok_line.append(create_token('Comment', line[:-1].strip(), line_no))
                            line = line[len(line):]
                            break
                        elif type_ == 'Multiline Comment Start':
                            token_value = matched_token.group(0)
                            tok_line.append(create_token(type_, token_value.strip(), line_no))
                            line = line[-1:].lstrip()
                            in_comment = True
                        else:
                            token_value = matched_token.group(0)
                            tok_line.append(create_token(type_, token_value.strip(), line_no))
                        line = line[matched_token.end():].lstrip()
                        break

                if not matched_token and not in_comment:
                    raise Exception(f"Error:{line_no}:Invalid token {line}")

            if hasToken and not in_comment:
                tok_line.append(create_token('Linebreak', '\\n', line_no))
        tokens.append(tok_line)
        line_no += 1

    tokens.append([create_token('End of File', 'EOF', line_no)])
    return tokens


# Sample LOLCode program
lolcode_program = """
I HAS
HAI 1.2
HAI
I HAS A VAR ITZ
VISIBLE "HELLO, WORLD!"
OBTW
    This is a multiline comment.
    ey
    eyo
    eyooo
KTHXBYE
"""

# Tokenize the LOLCode program
try:
    tokens = tokenize(lolcode_program)
    print(tokens)

    program_start = False
    program_end = False
    obtw_found = False
    tldr_found = False
    not_var = False
    itz_found = False
    hai_line_num = -1

    for line in tokens:
        print(line[0]['line_num'])
        for token in line:
            if token['type'] == 'Linebreak':
                continue

            print(f"Type: {token['type']}, Value: {token['value']}, Line Number: {token['line_num']}")

            # find HAI AND KTHXBYE
            if token['type'] == 'Code Start' and not program_start:
                print("Found HAI")
                program_start = True
                hai_line_num = token['line_num']
            elif token['type'] == 'Code Start' and program_start:
                print(f"Line {line[0]['line_num']}: SyntaxError: Expected statement after start of program")
            elif token['type'] == 'Code End' and not program_end:
                print("Found KTHXBYE")
                program_end = True
                kthxbye_line_num = token['line_num']
            elif token['type'] == 'Code End' and program_end:
                print(f"Line {line[0]['line_num']}: SyntaxError: Expected comment/function after end of program")
            # if same line as HAI / KTHXBYE
            elif (token['line_num'] == hai_line_num) or (token['line_num'] == hai_line_num):
                print(f"Line {line[0]['line_num']}: SyntaxError: Illegal statement right after HAI/before KTHXBYE")
            #if HAI and KTHXBYE became a comment
            elif token['type'] == 'Comment' and token['value'] in ['HAI', 'KTHXBYE']:
                print(f"Line {line[0]['line_num']}: SyntaxError: No HAI/KTHXBYE statement")
            
            #Add functions later for before and after program
            if not program_start and token['value'] not in ["BTW", "OBTW", "TLDR", "Linebreak"]:
                print(f"Line {line[0]['line_num']}: SyntaxError: Illegal statement before start of program")
            elif program_end and token['value'] not in ["BTW", "OBTW", "TLDR", "Linebreak"]:
                print(f"Line {line[0]['line_num']}: SyntaxError: Illegal statement after end of program")
            
            #Check OBTW and TLDR pairs and validity
            #The OBTW and TLDR does not have their own lines
            if token['value'] == 'OBTW':
                if len(line) != 1:
                    print(f"Line {line[0]['line_num']}: SyntaxError: Illegal comment")
                else:
                    obtw_found = True
            elif token['value'] == 'TLDR':
                #print(f"TLDR len line: {len(line)}")
                if len(line) > 2 and line[1]['type'] != 'Linebreak':
                    print(f"Line {line[0]['line_num']}: SyntaxError: Illegal comment")
                else:
                    if not obtw_found:
                        print(f"Line {line[0]['line_num']}: SyntaxError: Expected OBTW before TLDR")
                    tldr_found = True

            if (obtw_found and not tldr_found) and token['value'] == 'EOF':
                print(f"Line {line[0]['line_num']}: SyntaxError: Expected TLDR before end of file")
            
            #Variables
            if token['value'] == "I HAS A":
                # get line number
                ihasa_line_no = token['line_num']
                if (len(line)) < 2:
                    print(f"Line {line[0]['line_num']}: SyntaxError: Expected variable name after I HAS A")
                elif line[1]['type'] != 'Variable Identifier':
                    print(f"Line {line[0]['line_num']}: SyntaxError: Expected variable name after I HAS A")
                elif line[2]['type'] == 'Variable Assignment': 
                    itz_found = True
                
                for i in range(3, len(line)):
                    if line[i]['type'] in ["Addition","Subtraction","Multiplication","Division", "Modulo", "Max", "Min", "And", "Or", "Xor", "Not", "Infinite Or", "Infinite And", "Numbar Literal", "Numbr Literal", "Yarn Literal", "Troof Literal", "Variable Identifier"]:
                        not_var = True
            
            if token['value'] == "ITZ":
                if itz_found and line[3]['type'] == 'Linebreak':
                    print(f"Line {line[0]['line_num']}: SyntaxError: Expected variable assignment after variable name")
                if not_var == False:
                    print(f"Line {line[0]['line_num']}: SyntaxError: Invalid variable initialization")
except Exception as e:
    print(e)