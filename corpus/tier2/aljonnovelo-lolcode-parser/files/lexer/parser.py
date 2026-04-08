import re

# def identify_literals(lines, i):
#     numbr_literal = re.compile('^-?\d+$')
#     number_literal = re.compile('^-?\d+\.\d+$')
#     yarn_literal = re.compile('^\"(.*?)\"$')
#     troof_literal = re.compile('^(WIN|FAIL)$')
#     type_literal = re.compile('^(NUMBR|NUMBAR|YARN|TROOF|NOOB)$')

#     if numbr_literal.match(lines[i].strip()):
#         return "NUMBR LITERAL", i  
#     elif number_literal.match(lines[i].strip()):
#         return "NUMBER LITERAL", i
#     elif yarn_literal.match(lines[i].strip()):
#         return "YARN LITERAL", i 
#     elif troof_literal.match(lines[i].strip()):
#         return "TROOF LITERAL", i
#     elif type_literal.match(lines[i].strip()):
#         return "TYPE LITERAL", i
    

def identify_statement(lines, i):
    #variable_identifier = re.compile('^[A-Za-z][A-Za-z0-9_]*')
    numbr_literal = re.compile('^-?\d+$')
    number_literal = re.compile('^-?\d+\.\d+$')
    yarn_literal = re.compile('^\"(.*?)\"$')
    troof_literal = re.compile('^(WIN|FAIL)$')
    type_literal = re.compile('^(NUMBR|NUMBAR|YARN|TROOF|NOOB)$')    

    # regular expressions for identifying different LOLCODE statements
    hai_pattern = re.compile(r'^HAI\s*$', re.IGNORECASE)
    kthxbye_pattern = re.compile(r'^KTHXBYE\s*$', re.IGNORECASE)
   
    # comments
    btw_pattern = re.compile(r'^BTW\s*(?P<comment>.*)$', re.IGNORECASE)
    obtw_pattern = re.compile(r'^OBTW\s*(?P<block_comment>.*?)\s*$', re.IGNORECASE | re.DOTALL)

    visible_pattern = re.compile(r'^VISIBLE\s+(?P<comment>.+)$', re.IGNORECASE)
    gimme_pattern = re.compile(r'^GIMMEH\s+([A-Za-z_]\w*)$', re.IGNORECASE)

    # variable declaration
    wazzup_pattern = re.compile(r'^WAZZUP\s*(?P<variable>.*?)\s*$', re.IGNORECASE | re.DOTALL)
    

    i_has_a_pattern = re.compile(r'(I HAS A)\s*$', re.IGNORECASE )
    itz_pattern = re.compile(r'^ITZ\s*$', re.IGNORECASE)


    # check for HAI statement
    if hai_pattern.match(lines[i].strip()):
        return "HAI_STATEMENT", i
    
    # check for KTHXBYE statement
    elif kthxbye_pattern.match(lines[i].strip()):
        return "KTHXBYE_STATEMENT", i
    
    # check for BTW statement
    elif btw_pattern.match(lines[i].strip()):
        return "BTW_STATEMENT", i
    
    # check for OBTW statement
    elif obtw_match := obtw_pattern.match(lines[i].strip()):
        # process the multi-line block comment
        block_comment = obtw_match.group('block_comment')
        while not lines[i].strip().strip().endswith("TLDR"):
            i += 1
            block_comment += "\n" + lines[i].strip()
        return f"OBTW_STATEMENT", i

    # check for VISIBLE statement
    elif visible_pattern.match(lines[i].strip()):
        return "VISIBLE_STATEMENT", i

    # check for GIMMEH statement
    elif gimme_pattern.match(lines[i].strip()):
        return "GIMMEH_STATEMENT", i
    
    # check for WAZZUP statement
    elif wazzup_pattern := wazzup_pattern.match(lines[i].strip()):
        # process the multi-line block comment
        # variable = wazzup_pattern.group('variable')
        # while not lines[i].strip().endswith("BUHBYE"):
        #     i += 1
        #     variable += "\n" + lines[i].strip()
        return f"WAZZUP_STATEMENT", i
    
     # check for I HAS A STATEMENT statement
    elif i_has_a_pattern.match(lines[i].strip()):
        return "I_HAS_A_STATEMENT", i
    
    # check for variable
    # elif variable_identifier.match(lines[i].strip()):
    #     return "VARIABLE", i

    elif numbr_literal.match(lines[i].strip()):
        return "NUMBR LITERAL", i  
    elif number_literal.match(lines[i].strip()):
        return "NUMBER LITERAL", i
    elif yarn_literal.match(lines[i].strip()):
        return "YARN LITERAL", i 
    elif troof_literal.match(lines[i].strip()):
        return "TROOF LITERAL", i
    elif type_literal.match(lines[i].strip()):
        return "TYPE LITERAL", i
    
    
    # add more patterns for other LOLCODE statements as needed

    # if no match, return None
    return None, i
