import re


def identify_literals(lines, i):
    numbr_literal = re.compile('^-?\d+$')
    number_literal = re.compile('^-?\d+\.\d+$')
    yarn_literal = re.compile('^\"(.*?)\"$')
    troof_literal = re.compile('^(WIN|FAIL)$')
    type_literal = re.compile('^(NUMBR|NUMBAR|YARN|TROOF|NOOB)$')

    if numbr_literal.match(lines[i].strip()):
        return "NUMBR LITERAL", i  
    elif number_literal.match(lines[i].strip()):
        return "NUMBER LITERAL", i
    elif yarn_literal.match(lines[i].strip()):
        return "YARN LITERAL", i 
    elif troof_literal.match(lines[i].strip()):
        return "TROOF LITERAL", i
    elif type_literal.match(lines[i].strip()):
        return "TYPE LITERAL", i 

def identify_keywords(lines, i):
    keywords = ['EITHER OF', 'WON OF', 'NOT', 'ANY OF', 'ALL OF', 'BOTH SAEM', 'DIFFRINT', 'SMOOSH', 'MAEK',
    'A', 'O RLY\?', 'YA RLY', 'MEBBE']
    keyword_pattern = re.compile(r'^(%s)\b' % '|'.join(map(re.escape, keywords)))
    match = keyword_pattern.match(lines[i].strip())
    if match:
        return True
    else:
        return False

def identify_statement(lines, i):
    # regular expressions for identifying different LOLCODE statements
    hai_pattern = re.compile(r'^HAI\s*$', re.IGNORECASE)
    kthxbye_pattern = re.compile(r'^KTHXBYE\s*$', re.IGNORECASE)

    # variable declaration
    wazzup_pattern = re.compile(r'^WAZZUP\s*$', re.IGNORECASE)
    buhbye_pattern = re.compile(r'^BUHBYE\s*$', re.IGNORECASE)

    # comments
    btw_pattern = re.compile(r'^BTW\s*$', re.IGNORECASE)
    obtw_pattern = re.compile(r'^OBTW\s*$', re.IGNORECASE | re.DOTALL)
    tldr_pattern = re.compile(r'^TLDR\s*$', re.IGNORECASE)

    i_has_a_pattern = re.compile(r'^(I HAS A)\s*$', re.IGNORECASE)
    itz_pattern = re.compile(r'^ITZ\s*$', re.IGNORECASE)
    
    r_pattern = re.compile(r'^R\s*$', re.IGNORECASE)
    sum_of_pattern = re.compile(r'^(SUM OF)\s*$', re.IGNORECASE)
    diff_of_pattern = re.compile(r'^(DIFF 0F)\s*$', re.IGNORECASE)
    produKt_of_pattern = re.compile(r'^(PRODUKT OF)\s*$', re.IGNORECASE)
    quoshhunt_of_pattern = re.compile(r'^(QUOSHUNT OF)\s*$', re.IGNORECASE)
    mod_of_pattern = re.compile(r'^(MOD OF)\s*$', re.IGNORECASE)
    
    biggr_of_pattern = re.compile(r'^(BIGGR OF)\s*$', re.IGNORECASE)
    smallr_of_pattern = re.compile(r'^(SMALLER 0F)\s*$', re.IGNORECASE)
    
    both_of_pattern = re.compile(r'^(BOTH OF)\s*$', re.IGNORECASE)

    visible_pattern = re.compile(r'^VISIBLE\s+(?P<comment>.+)$', re.IGNORECASE)
    gimme_pattern = re.compile(r'^GIMMEH\s+([A-Za-z_]\w*)$', re.IGNORECASE)

    # conditional
    conditional_keywords = ["BOTH SAEM", "EITHER OF", "WON OF"]
    condkey_join = "|".join(conditional_keywords)
    expression_pattern = re.compile(r'^({})'.format(condkey_join))
    orly_pattern = re.compile(r'^O RLY/?\s*(?P<code_block>.*?)\s*$', re.IGNORECASE)
    
    # switch-case
    wtf_pattern = re.compile(r'^WTF/?\s*(?P<code_block>.*?)\s*$', re.IGNORECASE)

    # check for HAI statement
    if hai_pattern.match(lines[i].strip()):
        return "HAI: Marks the beginning of the program.", i
    
    # check for KTHXBYE statement
    elif kthxbye_pattern.match(lines[i].strip()):
        return "KTHXBYE: Marks the end of the program.", i

    elif wazzup_pattern.match(lines[i].strip()):
        return "WAZZUP: Used to declare a variable or ask for user input.", i

    elif buhbye_pattern.match(lines[i].strip()):
        return "BUHBYE: Used to exit a program early.", i
    
    # check for BTW statement
    elif btw_pattern.match(lines[i].strip()):
        return "BTW: Begins a comment (inline comment).", i
    
    # check for OBTW statement
    elif obtw_pattern.match(lines[i].strip()):
        return "OBTW: Begins a block comment.", i
    # elif obtw_match := obtw_pattern.match(lines[i].strip()):
    #     # process the multi-line block comment
    #     block_comment = obtw_match.group('block_comment')
    #     while not lines[i].strip().endswith("TLDR"):
    #         i += 1
    #         block_comment += "\n" + lines[i].strip()
    #     return f"OBTW_STATEMENT", i
    
    elif tldr_pattern.match(lines[i].strip()):
        return "TLDR: Ends a block comment.", i
    elif i_has_a_pattern.match(lines[i].strip()):
        return "I HAS A: Used to declare a variable.", i
    elif itz_pattern.match(lines[i].strip()):
        return "ITZ: Used for variable initialization or assignment.", i
    elif r_pattern.match(lines[i].strip()):
        return "R: Acts as a placeholder for values.", i
    elif sum_of_pattern.match(lines[i].strip()):
        return "SUM OF: Addition operator.", i
    elif diff_of_pattern.match(lines[i].strip()):
        return "DIFF OF: Subtraction operator.", i
    elif produKt_of_pattern.match(lines[i].strip()):
        return "PRODUKT OF: Multiplication operator.", i
    elif quoshhunt_of_pattern.match(lines[i].strip()):
        return "QUOSHUNT OF: Division operator.", i
    elif mod_of_pattern.match(lines[i].strip()):
        return "MOD OF: Modulo (remainder) operator.", i
    elif biggr_of_pattern.match(lines[i].strip()):
        return "BIGGR OF: Returns the larger of two values.", i
    elif smallr_of_pattern.match(lines[i].strip()):
        return "SMALLR OF: Returns the smaller of two values.", i
    elif both_of_pattern.match(lines[i].strip()):
        return "BOTH OF: Logical AND operator.", i

    # check for expression
    elif expression_pattern.match(lines[i].strip()):
        return "EXPRESSION_STATEMENT", i
    
    # check for conditional statement
    elif orly_match := orly_pattern.match(lines[i].strip()):
        code_block = orly_match.group('code_block')
        while not lines[i].strip().endswith("OIC"):
            i += 1
            code_block += "\n" + lines[i].strip()
        return "CONDITIONAL_STATEMENT", i
    
    # check for switch-case statement
    elif wtf_match := wtf_pattern.match(lines[i].strip()):
        code_block = wtf_match.group('code_block')
        while not lines[i].strip().endswith("OIC"):
            i += 1
            code_block += "\n" + lines[i].strip()
        return "SWITCH_STATEMENT", i

    # check for VISIBLE statement
    elif visible_pattern.match(lines[i].strip()):
        return "VISIBLE_STATEMENT", i

    # check for GIMMEH statement
    elif gimme_pattern.match(lines[i].strip()):
        return "GIMMEH_STATEMENT", i

    # add more patterns for other LOLCODE statements as needed
    identify_keywords(lines, i)
    # if no match, return None
    return None, i

def identify_condition(lines, i):
    yarly_pattern = re.compile(r'^YA RLY\s*(?P<code_block>.*?)\s*$', re.IGNORECASE)
    
    # check for if conditional
    if yarly_match := yarly_pattern.match(lines[i].strip()):
        code_block = yarly_match.group('code_block')
        while not lines[i].strip().endswith("OIC"):
            i += 1
            code_block += "\n" + lines[i].strip()
        return "IF_STATEMENT", i
    return None, i

def identify_switch(lines, i):
    omg_pattern = re.compile(r'^OMG\s*(?P<value_literal>.*?)\s*$', re.IGNORECASE)

    # check for if conditional
    if omg_pattern.match(lines[i].strip()):
        return "SWITCH_TRUE_STATEMENT", i
    return None, i