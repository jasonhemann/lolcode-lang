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

def identify_statement(lines, i):
    # regular expressions for identifying different LOLCODE statements
    hai_pattern = re.compile(r'^HAI\s*$', re.IGNORECASE)
    kthxbye_pattern = re.compile(r'^KTHXBYE\s*$', re.IGNORECASE)
   
    # comments
    btw_pattern = re.compile(r'^BTW\s*(?P<comment>.*)$', re.IGNORECASE)
    obtw_pattern = re.compile(r'^OBTW\s*(?P<block_comment>.*?)\s*$', re.IGNORECASE | re.DOTALL)

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
        while not lines[i].strip().endswith("TLDR"):
            i += 1
            block_comment += "\n" + lines[i].strip()
        return f"OBTW_STATEMENT", i
    
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