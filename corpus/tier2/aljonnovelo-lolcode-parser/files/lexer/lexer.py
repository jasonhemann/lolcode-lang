import re
from lolcode_regex import lolregex

def identify_statement(lines, i):
    line = lines[i].strip()
    # identifiers and literals
    variable_identifier = re.compile(lolregex['variable identifier'])
    numbr_literal = re.compile(lolregex['numbr literal'])
    numbar_literal = re.compile(lolregex['numbar literal'])
    yarn_literal = re.compile(lolregex['yarn literal'])
    troof_literal = re.compile(lolregex['troof literal'])
    type_literal = re.compile(lolregex['type literal'])    

    # start and end of program
    hai_pattern = re.compile(lolregex['hai'])
    kthxbye_pattern = re.compile(lolregex['kthxbye'])

    # variable declaration
    wazzup_pattern = re.compile(lolregex['wazzup'])
    buhbye_pattern = re.compile(lolregex['buhbye'])

    # comments
    btw_pattern = re.compile(lolregex['btw'])
    obtw_pattern = re.compile(lolregex['obtw'])
    tldr_pattern = re.compile(lolregex['tldr'])

    # variable initialization
    i_has_a_pattern = re.compile(lolregex['i has a'])
    itz_pattern = re.compile(lolregex['itz'])
    
    # expressions
    r_pattern = re.compile(lolregex['r'])
    sum_of_pattern = re.compile(lolregex['sum of'])
    diff_of_pattern = re.compile(lolregex['diff of'])
    produkt_of_pattern = re.compile(lolregex['produkt of'])
    quoshunt_of_pattern = re.compile(lolregex['quoshunt of'])
    mod_of_pattern = re.compile(lolregex['mod of'])
    biggr_of_pattern = re.compile(lolregex['biggr of'])
    smallr_of_pattern = re.compile(lolregex['smallr of'])
    both_of_pattern = re.compile(lolregex['both of'])
    either_of_pattern = re.compile(lolregex['either of'])
    won_of_pattern = re.compile(lolregex['won of'])
    not_pattern = re.compile(lolregex['not'])
    any_of_pattern = re.compile(lolregex['any of'])
    all_of_pattern = re.compile(lolregex['all of'])
    both_saem_pattern = re.compile(lolregex['both saem'])

    maek_pattern = re.compile(lolregex['maek'])
    a_pattern = re.compile(lolregex['a'])
    is_now_a_pattern = re.compile(lolregex['is now a'])

    #statements
    visible_pattern = re.compile(lolregex['visible'])
    gimmeh_pattern = re.compile(lolregex['gimmeh'])
    o_rly_pattern = re.compile(lolregex['o rly'])
    ya_rly_pattern = re.compile(lolregex['ya rly'])
    mebbe_pattern = re.compile(lolregex['mebbe'])
    wtf_pattern = re.compile(lolregex['wtf'])

    if numbr_literal.match(line):
        return "NUMBR LITERAL", i  
    elif numbar_literal.match(line):
        return "NUMBER LITERAL", i
    elif yarn_literal.match(line):
        return "YARN LITERAL", i 
    elif troof_literal.match(line):
        return "TROOF LITERAL", i
    elif type_literal.match(line):
        return "TYPE LITERAL", i
    elif hai_pattern.match(line):
        return "HAI: Marks the beginning of the program.", i
    elif kthxbye_pattern.match(line):
        return "KTHXBYE: Marks the end of the program.", i
    elif wazzup_pattern.match(line):
        return "WAZZUP: Used to declare a variable or ask for user input.", i
    elif buhbye_pattern.match(line):
        return "BUHBYE: Used to exit a program early.", i
    elif btw_pattern.match(line):
        return "BTW: Begins a comment (inline comment).", i
    elif obtw_pattern.match(line):
        obtw_match = obtw_pattern.match(line)
        if obtw_match:
            comment_lines = []

            # continue until 'TLDR' is found
            while i < len(lines) and not lines[i].strip().endswith("TLDR"):
                comment_lines.append(lines[i])
                i += 1

            # skip the 'TLDR' line
            i += 1

            comment_content = "\n".join(comment_lines)
            return f"OBTW: Begins a block comment.\n{comment_content}", i
    elif tldr_pattern.match(line):
        return "TLDR: Ends a block comment.", i
    elif i_has_a_pattern.match(line):
        # result = re.search(r'[\t]*(I HAS A)\s+([A-Za-z][A-Za-z0-9_]*)*$', line)
        # print(result.group(2))
        return "I HAS A: Used to declare a variable.", i
    elif itz_pattern.match(line):
        return "ITZ: Used for variable initialization or assignment.", i
    elif r_pattern.match(line):
        return "R: Acts as a placeholder for values.", i
    elif sum_of_pattern.match(line):
        return "SUM OF: Addition operator.", i
    elif diff_of_pattern.match(line):
        return "DIFF OF: Subtraction operator.", i
    elif produkt_of_pattern.match(line):
        return "PRODUKT OF: Multiplication operator.", i
    elif quoshunt_of_pattern.match(line):
        return "QUOSHUNT OF: Division operator.", i
    elif mod_of_pattern.match(line):
        return "MOD OF: Modulo (remainder) operator.", i
    elif biggr_of_pattern.match(line):
        return "BIGGR OF: Returns the larger of two values.", i
    elif smallr_of_pattern.match(line):
        return "SMALLR OF: Returns the smaller of two values.", i
    elif both_of_pattern.match(line):
        return "BOTH OF: Logical AND operator.", i
    elif either_of_pattern.match(line):
        return "EITHER OF: Logical OR operator.", i
    elif won_of_pattern.match(line):
        return "WON OF: Logical XOR operator.", i
    elif not_pattern.match(line):
        return "NOT: Logical NOT operator.", i
    elif any_of_pattern.match(line):
        return "ANY OF: Infinite arity OR.", i
    elif all_of_pattern.match(line):
        return "ALL OF: Infinite arity OR.", i
    elif both_saem_pattern.match(line):
        return "BOTH SAEM: Returns WIN if both expressions have the same value.", i
    elif maek_pattern.match(line):
        return "MAEK: Converts a value to a specific type.", i
    elif a_pattern.match(line):
        return "A: Used for defining constants.", i
    elif is_now_a_pattern.match(line):
        return "IS NOW A: Changes the type of a variable.", i
    elif visible_pattern.match(line):
        return "VISIBLE: Outputs a value to the console.", i
    elif gimmeh_pattern.match(line):
        return "GIMMEH: Reads user input.", i
    elif o_rly_pattern.match(line):
        return "O RLY?: Begins an If-Then-Else block.", i
    elif ya_rly_pattern.match(line):
        return "YA RLY: Indicates the code to execute if the condition is true.", i
    elif mebbe_pattern.match(line):
        return "MEBBE: Used for additional conditions in an If-Then-Else block.", i
    # check for switch-case statement
    elif wtf_pattern.match(line):
        # code_block = wtf_match.group('code_block')
        # while not line.endswith("OIC"):
        #     i += 1
        #     code_block += "\n" + line
        return "SWITCH_STATEMENT", i
    elif variable_identifier.match(line):
        return "VARIABLE IDENTIFIER", i

    # if no match, return None
    return None, i