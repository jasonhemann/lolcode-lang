import re
import lexical_analyzer

# all of this is based on the grammar we submitted with a few modifications
# program parse -> statement parse
# statement parse -> print parse | variable declaration parse | etc other stuff
# print parse -> VISIBLE variable/literal/expression
# variable declaration parse -> I HAS A variable [ITZ variable/literal]

# uses tokens as stack to get the next lexeme
# uses a lot of loops and recursions
# outputs a nested list file we can later turn into a tree if needed

# NOTE: should be all working now, no bonuses except for nested loops and nested if-else i think (need to check that)

class LolcodeException(Exception):
    pass

def var_or_lit_or_expr(classification, lexeme):
    # print("var or lit or expr")

    res = []
    # classification, lexeme = tokens.pop()
    # print(classification, lexeme)
    
    if classification == "VARIABLE" or classification == "NUMBR" or classification == "NUMBAR"or classification == "TROOF":             # if next lexeme is variable or literal (that isn't a YARN) just append it and return the list
        # res = []
        res.append(lexeme)
    elif classification == "STRING_DELIMITER":              # if string delimiter is found, we hit yarn, parse yarn then return list
        tokens.append((classification, lexeme))
        res = yarn_parse()
    elif lexeme == "SMOOSH":
        tokens.append((classification, lexeme))
        res = smoosh_parse()
    elif lexeme == "SUM OF" or lexeme == "DIFF OF" or lexeme == "PRODUKT OF" or lexeme == "QUOSHUNT OF" or lexeme == "MOD OF" or lexeme == "BIGGR OF" or lexeme == "SMALLR OF":
        tokens.append((classification, lexeme))
        res = expr_parse()
    elif lexeme == "NOT" or lexeme == "BOTH OF" or lexeme == "EITHER OF" or lexeme == "WON OF":
        tokens.append((classification, lexeme))
        res = bool_expr_parse()
    else:
        # print(classification, lexeme)
        tokens.append((classification, lexeme))
        return 0
    
    return res

def input_parse():
    # print("input parse")
    input_list = []

    classification, lexeme = tokens.pop()
    input_list.append(lexeme)

    classification, lexeme = tokens.pop()

    if classification == "VARIABLE":
        input_list.append(lexeme)
    else:
        print(classification, lexeme)
        raise LolcodeException("Syntax error in input - incorrect operand: line " + str(lines))
    
    return input_list
    
def yarn_parse():               # yarn literal parse
    # print("string parse")
    yarn_list = []
    classification, lexeme = tokens.pop()
    yarn_list.append(lexeme)
    classification, lexeme = tokens.pop()
    yarn_list.append(lexeme)
    classification, lexeme = tokens.pop()
    yarn_list.append(lexeme)
    return yarn_list

def expr_parse():
    # print("expression parse")
    expr_list = []

    classification, lexeme = tokens.pop()
    expr_list.append(lexeme)
    classification, lexeme = tokens.pop()

    if classification == "VARIABLE" or classification == "NUMBR" or classification == "NUMBAR" or classification == "TROOF":
        expr_list.append(lexeme)
    elif classification == "STRING_DELIMITER":
        tokens.append((classification, lexeme))
        expr_list.append(yarn_parse())
    elif lexeme == "SUM OF" or lexeme == "DIFF OF" or lexeme == "PRODUKT OF" or lexeme == "QUOSHUNT OF" or lexeme == "MOD OF" or lexeme == "BIGGR OF" or lexeme == "SMALLER OF":
        tokens.append((classification, lexeme))
        expr_list.append(expr_parse())
    elif lexeme == "NOT" or lexeme == "BOTH OF" or lexeme == "EITHER OF" or lexeme == "WON OF":
        tokens.append((classification, lexeme))
        expr_list.append(bool_expr_parse())
    else:
        print(classification, lexeme)
        raise LolcodeException("Syntax error in expression - incorrect operand: line " + str(lines))
    
    classification, lexeme = tokens.pop()
    if classification == "KEYWORD" and lexeme == "AN":
        expr_list.append(lexeme)
    else:
        print(classification, lexeme)
        print(tokens[-5:])
        raise LolcodeException("Syntax error in expression - missing 'AN' keyword: line " + str(lines))
    
    classification, lexeme = tokens.pop()
    if classification == "VARIABLE" or classification == "NUMBR" or classification == "NUMBAR" or classification == "TROOF":
        expr_list.append(lexeme)
    elif classification == "STRING_DELIMITER":
        tokens.append((classification, lexeme))
        expr_list.append(yarn_parse())
    elif lexeme == "SUM OF" or lexeme == "DIFF OF" or lexeme == "PRODUKT OF" or lexeme == "QUOSHUNT OF" or lexeme == "MOD OF" or lexeme == "BIGGR OF" or lexeme == "SMALLR OF":
        tokens.append((classification, lexeme))
        expr_list.append(expr_parse())
    elif lexeme == "NOT" or lexeme == "BOTH OF" or lexeme == "EITHER OF" or lexeme == "WON OF":
        tokens.append((classification, lexeme))
        expr_list.append(bool_expr_parse())
    else:
        print(classification, lexeme)
        raise LolcodeException("Syntax error in expression - incorrect operand: line " + str(lines))
    
    return expr_list

def typecast_parse():
    # print("typecast parse")
    typecast_list = []

    classification, lexeme = tokens.pop()
    typecast_list.append(lexeme)


    classification, lexeme = tokens.pop()
    if classification == "VARIABLE":
        typecast_list.append(lexeme)
    else:
        print(classification, lexeme)
        raise LolcodeException("Syntax error in typecast - variable not found: line " + str(lines))

    classification, lexeme = tokens.pop()
    if lexeme == "A":
        typecast_list.append(lexeme)
    else:
        tokens.append((classification, lexeme))
        
    classification, lexeme = tokens.pop()
    if classification == "TYPE":
        typecast_list.append(lexeme)
    else:
        print(classification, lexeme)
        raise LolcodeException("Syntax error in typecast - incorrect syntax in type: line " + str(lines))
    
    return typecast_list

def assign_parse():
    # print("assign parse")
    assign_list = []
    
    classification, lexeme = tokens.pop()
    assign_list.append(lexeme)

    classification, lexeme = tokens.pop()
    if lexeme == "R":
        assign_list.append(lexeme)
        classification, lexeme = tokens.pop()
        if res := var_or_lit_or_expr(classification, lexeme):
            assign_list.append(res)
            return assign_list
        elif lexeme == "ALL OF" or lexeme == "ANY OF":
            assign_list.append(bool_all_any_parse())
        elif lexeme == "MAEK":
            assign_list.append(typecast_parse())
            return assign_list
        else:                               # otherwise, syntax error
            print(classification, lexeme)
            raise LolcodeException("Syntax error in assignment statement - incorrect operand: line " + str(lines))
    elif lexeme == "IS NOW A":
        assign_list.append(lexeme)
        classification, lexeme = tokens.pop()
        if classification == "TYPE":
            assign_list.append(lexeme)
            return assign_list
        else:
            print(classification, lexeme)
            raise LolcodeException("Syntax error in assignment statement - incorrect type: line " + str(lines))
    else:
        tokens.append((classification, lexeme))
        return assign_list

def var_dec_parse():                # variable declaration statement parse
    # print("parsing variable declaration")

    var_dec_list = []                                   # initialize variable declaration statement list

    classification, lexeme = tokens.pop()                       # put "I HAS A" keyword in list then pop next lexeme
    var_dec_list.append(lexeme)
    classification, lexeme = tokens.pop()

    if classification == "VARIABLE":                    # if next lexeme is a variable then append it, otherwise bad syntax
        var_dec_list.append(lexeme)
    else:
        print(classification, lexeme)
        raise LolcodeException("Syntax error in variable declaration - variable not found: line " + str(lines))

    classification, lexeme = tokens.pop()               # pop next lexeme again
    
    if lexeme != "ITZ":                             # if not ITZ keyword (for elaborate variable declaration, push that lexeme back in stack)
        tokens.append((classification, lexeme))
    else:                                              # if ITZ keyword, put "ITZ" keyword in list
        var_dec_list.append(lexeme)
        classification, lexeme = tokens.pop()           # pop next lexeme
        if res := var_or_lit_or_expr(classification, lexeme):
            var_dec_list.append(res)
        elif lexeme == "ALL OF" or lexeme == "ANY OF":
            var_dec_list.append(bool_all_any_parse())
        else:                   # else, bad syntax
            print(classification, lexeme)
            raise LolcodeException("Syntax error in variable declaration - incorrect operand: line " + str(lines))
        
    return var_dec_list

def smoosh_parse():
    # print("smoosh parse")
    smoosh_list = []

    classification, lexeme = tokens.pop()
    smoosh_list.append(lexeme)

    classification, lexeme = tokens.pop()
    if res := var_or_lit_or_expr(classification, lexeme):
        smoosh_list.append(res)
    else:
        print(classification, lexeme)
        raise LolcodeException("Syntax error in concatenation - incorrect operand: line " + str(lines))
    
    while True:
        classification, lexeme = tokens.pop()
        if lexeme == "AN":
            smoosh_list.append(lexeme)
            classification, lexeme = tokens.pop()
            if res := var_or_lit_or_expr(classification, lexeme):
                smoosh_list.append(res)
            else:
                print(classification, lexeme)
                raise LolcodeException("Syntax error in concatenation - incorrect operand: line " + str(lines))
        else:
            tokens.append((classification, lexeme))
            break
    
    return smoosh_list

def print_parse():              # print statement parse
    # print("parsing print")
    print_list = []                 # initialize list for print statement

    classification, lexeme = tokens.pop()           # add "VISIBLE" lexeme to list then pop next lexeme
    print_list.append(lexeme)
    classification, lexeme = tokens.pop()

    
    if res := var_or_lit_or_expr(classification, lexeme):
        print_list.append(res)
    elif lexeme == "ALL OF" or lexeme == "ANY OF":
        print_list.append(bool_all_any_parse())
    elif lexeme == "BOTH SAEM" or lexeme == "DIFFRINT":
        print_list.append(comp_parse())
    elif classification == "TYPE":              # if lexeme is of literal type TYPE, also append it to list and return list
        print_list.append(lexeme)
    else:                               # otherwise, syntax error
        print(classification, lexeme)
        raise LolcodeException("Syntax error in printing - incorrect operand: line " + str(lines))
    
    while True:
        classification, lexeme = tokens.pop()
        if lexeme == "AN" or classification == "CONCATENATE":
            print_list.append(lexeme)
            classification, lexeme = tokens.pop()
            if res := var_or_lit_or_expr(classification, lexeme):
                print_list.append(res)
            elif classification == "TYPE":              # if lexeme is of literal type TYPE, also append it to list and return list
                print_list.append(lexeme)
            else:
                print(classification, lexeme)
                raise LolcodeException("Syntax error in printing - incorrect operand: line " + str(lines))
        else:
            tokens.append((classification, lexeme))
            break
    
    return print_list

def if_parse():
    # print("if statement parse")
    global lines

    if_list = []
    classification, lexeme = tokens.pop()
    if_list.append(lexeme)

    while True:
        classification, lexeme = tokens.pop()

        while classification == "COMMENT" or classification == "MULTI-LINE_COMMENT" or classification == "NEWLINE":
            if classification == "MULTI-LINE_COMMENT":
                for newline in re.findall(r"\n", lexeme):
                    # print(lines)
                    lines += 1
            elif classification == "NEWLINE":
                # print(lines)
                lines += 1
            classification, lexeme = tokens.pop()
        
        if lexeme == "YA RLY":
            if_list.append(lexeme)
            while True:                                     # iterate infinitely through all lexemes
                classification, lexeme = tokens.pop()
                if classification == "NEWLINE":                 # ignore newline and comments
                    # print(lines)
                    lines += 1
                    continue
                elif classification == "COMMENT":
                    continue
                elif classification == "MULTI-LINE_COMMENT":
                    for newline in re.findall(r"\n", lexeme):
                        # print(lines)
                        lines += 1
                    continue
                elif lexeme == "EOF":
                    print(classification, lexeme)
                    raise LolcodeException("Syntax error in if-else - missing 'OIC' terminating keyword: line " + str(lines))
                elif lexeme == "NO WAI":
                    tokens.append((classification, lexeme))
                    break
                elif lexeme == "OIC":
                    tokens.append((classification, lexeme))
                    break
                else:
                    tokens.append((classification, lexeme))         # otherwise, found other keyword, statement starts, go to parse statement and append that statement to list
                    if_list.append(statement_parse())
        elif lexeme == "NO WAI":
            if_list.append(lexeme)
            while True:                                     # iterate infinitely through all lexemes
                classification, lexeme = tokens.pop()
                if classification == "NEWLINE":                 # ignore newline and comments
                    # print(lines)
                    lines += 1
                    continue
                elif classification == "COMMENT":
                    continue
                elif classification == "MULTI-LINE_COMMENT":
                    for newline in re.findall(r"\n", lexeme):
                        # print(lines)
                        lines += 1
                    continue
                elif lexeme == "EOF":
                    print(classification, lexeme)
                    raise LolcodeException("Syntax error in if-else - missing 'OIC' terminating keyword: line " + str(lines))
                elif lexeme == "OIC":
                    tokens.append((classification, lexeme))
                    break
                else:
                    tokens.append((classification, lexeme))         # otherwise, found other keyword, statement starts, go to parse statement and append that statement to list
                    if_list.append(statement_parse())
        elif lexeme == "OIC":
            if_list.append(lexeme)
            break

    return if_list

def switch_parse():
    # print("switch parse")
    global lines

    switch_list = []
    classification, lexeme = tokens.pop()
    switch_list.append(lexeme)

    while True:
        classification, lexeme = tokens.pop()

        while classification == "COMMENT" or classification == "MULTI-LINE_COMMENT" or classification == "NEWLINE":
            if classification == "MULTI-LINE_COMMENT":
                for newline in re.findall(r"\n", lexeme):
                    # print(lines)
                    lines += 1
            elif classification == "NEWLINE":
                # print(lines)
                lines += 1
            classification, lexeme = tokens.pop()

        if lexeme == "OMG":
            switch_list.append(lexeme)

            classification, lexeme = tokens.pop()
            if classification == "NUMBR" or classification == "NUMBAR" or classification == "TROOF":
                switch_list.append(lexeme)
            elif classification == "STRING_DELIMITER":
                tokens.append((classification, lexeme))
                switch_list.append(yarn_parse())
            else:
                raise LolcodeException("Syntax error in switch statement - missing literal in case: line " + str(lines))

            while True:                                     # iterate infinitely through all lexemes
                classification, lexeme = tokens.pop()
                if classification == "NEWLINE":                 # ignore newline and comments
                    # print(lines)
                    lines += 1
                    continue
                elif classification == "COMMENT":
                    continue
                elif classification == "MULTI-LINE_COMMENT":
                    for newline in re.findall(r"\n", lexeme):
                        # print(lines)
                        lines += 1
                    continue
                elif lexeme == "EOF":
                    print(classification, lexeme)
                    raise LolcodeException("Syntax error in switch statement - missing 'OIC' terminating keyword: line " + str(lines))
                elif lexeme == "GTFO":
                    switch_list.append(lexeme)
                    break
                elif lexeme == "OMGWTF":
                    tokens.append((classification, lexeme))
                    break
                elif lexeme == "OMG":
                    tokens.append((classification, lexeme))
                    break
                elif lexeme == "OIC":
                    tokens.append((classification, lexeme))
                    break
                else:
                    tokens.append((classification, lexeme))         # otherwise, found other keyword, statement starts, go to parse statement and append that statement to list
                    switch_list.append(statement_parse())
        elif lexeme == "OMGWTF":
            switch_list.append(lexeme)

            while True:                                     # iterate infinitely through all lexemes
                classification, lexeme = tokens.pop()
                if classification == "NEWLINE":                 # ignore newline and comments
                    # print(lines)
                    lines += 1
                    continue
                elif classification == "COMMENT":
                    continue
                elif classification == "MULTI-LINE_COMMENT":
                    for newline in re.findall(r"\n", lexeme):
                        # print(lines)
                        lines += 1
                    continue
                elif lexeme == "EOF":
                    print(classification, lexeme)
                    raise LolcodeException("Syntax error in switch statement - missing 'OIC' terminating keyword: line " + str(lines))
                elif lexeme == "GTFO":
                    switch_list.append(lexeme)
                    break
                elif lexeme == "OMGWTF":
                    print(classification, lexeme)
                    raise LolcodeException("Syntax error in switch statement - duplicate default case: line " + str(lines))
                elif lexeme == "OMG":
                    print(classification, lexeme)
                    raise LolcodeException("Syntax error in switch statement - case found after default case: line " + str(lines))
                elif lexeme == "OIC":
                    tokens.append((classification, lexeme))
                    break
                else:
                    tokens.append((classification, lexeme))         # otherwise, found other keyword, statement starts, go to parse statement and append that statement to list
                    switch_list.append(statement_parse())
        elif lexeme == "OIC":
            switch_list.append(lexeme)
            break
    
    return switch_list

def loop_parse():
    # print("loop parse")
    global lines

    loop_list = []
    classification, lexeme = tokens.pop()
    loop_list.append(lexeme)
    classification, lexeme = tokens.pop()

    if classification == "VARIABLE":
        loop_list.append(lexeme)
    else:
        raise LolcodeException("Syntax error in loop - incorrect label: line " + str(lines))
    
    classification, lexeme = tokens.pop()

    if lexeme == "UPPIN" or lexeme == "NERFIN":
        loop_list.append(lexeme)
    else:
        raise LolcodeException("Syntax error in loop - incorrect operation: line " + str(lines))
    
    classification, lexeme = tokens.pop()

    if lexeme == "YR":
        loop_list.append(lexeme)
    else:
        raise LolcodeException("Syntax error in loop - missing 'YR' keyword: line " + str(lines))
    
    classification, lexeme = tokens.pop()

    if classification == "VARIABLE":
        loop_list.append(lexeme)
    else:
        raise LolcodeException("Syntax error in loop - incorrect operand: line " + str(lines))
    
    classification, lexeme = tokens.pop()

    if lexeme == "TIL" or lexeme == "WILE":
        loop_list.append(lexeme)
    else:
        raise LolcodeException("Syntax error in loop - incorrect keyword: line " + str(lines))
    
    classification, lexeme = tokens.pop()

    if lexeme == "DIFFRINT" or lexeme == "BOTH SAEM":
        tokens.append((classification, lexeme))
        loop_list.append(comp_parse())
    else:
        raise LolcodeException("Syntax error in loop - incorrect operand: line " + str(lines))
    
    while True:
        classification, lexeme = tokens.pop()
        if classification == "NEWLINE":
            # print(lines)
            lines += 1
            continue
        elif classification == "COMMENT":
            continue
        elif classification == "MULTI-LINE_COMMENT":
            for newline in re.findall(r"\n", lexeme):
                # print(lines)
                lines += 1
            continue
        elif lexeme == "EOF":
            print(classification, lexeme)
            raise LolcodeException("Syntax error in loop - missing closing keyword: line " + str(lines))
        elif lexeme == "IM OUTTA YR":
            loop_list.append(lexeme)

            classification, lexeme = tokens.pop()
            if classification == "VARIABLE":
                loop_list.append(lexeme)
            else:
                raise LolcodeException("Syntax error in loop - missing closing label: line " + str(lines))

            break
        else:
            tokens.append((classification, lexeme))         # otherwise, found other keyword, statement starts, go to parse statement and append that statement to list
            loop_list.append(statement_parse())
    
    return loop_list

def func_dec_parse():
    # print("function declaration parse")
    global lines

    func_dec_list = []
    classification, lexeme = tokens.pop()
    func_dec_list.append(lexeme)
    classification, lexeme = tokens.pop()

    if classification == "VARIABLE":
        func_dec_list.append(lexeme)
    else:
        raise LolcodeException("Syntax error in function declaration - incorrect function name: line " + str(lines))
    
    classification, lexeme = tokens.pop()
    if lexeme == "YR":
        func_dec_list.append(lexeme)

        classification, lexeme = tokens.pop()
        if classification == "VARIABLE":
            func_dec_list.append(lexeme)
        else:
            raise LolcodeException("Syntax error in function declaration - incorrect parameter: line " + str(lines))

        while True:
            classification, lexeme = tokens.pop()
            if lexeme == "AN":
                func_dec_list.append(lexeme)

                classification, lexeme = tokens.pop()
                if lexeme == "YR":
                    func_dec_list.append(lexeme)
                else:
                    raise LolcodeException("Syntax error in function declaration - missing 'YR' keyword in parameter: line " + str(lines))
                
                classification, lexeme = tokens.pop()
                if classification == "VARIABLE":
                    func_dec_list.append(lexeme)
                else:
                    raise LolcodeException("Syntax error in function declaration - incorrect parameter: line " + str(lines))
            else:
                tokens.append((classification, lexeme))
                break
    else:
        tokens.append((classification, lexeme))
    
    while True:                                     # iterate infinitely through all lexemes
        classification, lexeme = tokens.pop()
        # print(classification, lexeme)
        if classification == "NEWLINE":                 # ignore newline and comments
            # print(lines)
            lines += 1
            continue
        elif classification == "COMMENT":
            continue
        elif classification == "MULTI-LINE_COMMENT":
            for newline in re.findall(r"\n", lexeme):
                # print(lines)
                lines += 1
            continue
        elif lexeme == "EOF":
            print(classification, lexeme)
            raise LolcodeException("Syntax error in function declaration - missing closing keyword: line " + str(lines))
        elif lexeme == "FOUND YR":
            func_dec_list.append(lexeme)
            classification, lexeme = tokens.pop()
            if res := var_or_lit_or_expr(classification, lexeme):
                func_dec_list.append(res)
            else:
                raise LolcodeException("Syntax error in function declaration - incorrect operand for return value: line " + str(lines))
        elif lexeme == "GTFO":
            func_dec_list.append(lexeme)
        elif lexeme == "IF U SAY SO":
            func_dec_list.append(lexeme)
            break
        else:
            tokens.append((classification, lexeme))         # otherwise, found other keyword, statement starts, go to parse statement and append that statement to list
            func_dec_list.append(statement_parse())
    
    return func_dec_list

def func_call_parse():
    # print("function call parse")

    func_call_list = []
    classification, lexeme = tokens.pop()
    func_call_list.append(lexeme)
    classification, lexeme = tokens.pop()
    if classification == "VARIABLE":
        func_call_list.append(lexeme)
    else:
        raise LolcodeException("Syntax error in function call - incorrect function name: line " + str(lines))
    
    classification, lexeme = tokens.pop()
    if lexeme == "YR":
        func_call_list.append(lexeme)

        classification, lexeme = tokens.pop()
        if res := var_or_lit_or_expr(classification, lexeme):
            func_call_list.append(res)
        else:
            raise LolcodeException("Syntax error in function call - incorrect parameter: line " + str(lines))

        while True:
            classification, lexeme = tokens.pop()
            if lexeme == "AN":
                func_call_list.append(lexeme)

                classification, lexeme = tokens.pop()
                if lexeme == "YR":
                    func_call_list.append(lexeme)
                else:
                    raise LolcodeException("Syntax error in function call - missing 'YR' keyword in parameter: line " + str(lines))
                
                classification, lexeme = tokens.pop()
                if res := var_or_lit_or_expr(classification, lexeme):
                    func_call_list.append(res)
                else:
                    raise LolcodeException("Syntax error in function call - incorrect parameter: line " + str(lines))
            elif lexeme == "MKAY":
                func_call_list.append(lexeme)
                break
            else:
                raise LolcodeException("Syntax error in function call - incorrect keyword: line " + str(lines))
    elif lexeme == "MKAY":
        func_call_list.append(lexeme)
    else:
        raise LolcodeException("Syntax error in function call - missing 'MKAY' terminating keyword: line " + str(lines))

    return func_call_list

def comp_parse():
    # print("comparison parse")
    comp_list = []

    classification, lexeme = tokens.pop()
    comp_list.append(lexeme)
    classification, lexeme = tokens.pop()

    if res := var_or_lit_or_expr(classification, lexeme):
        comp_list.append(res)
    else:
        print(classification, lexeme)
        raise LolcodeException("Syntax error in comparison - incorrect operand: line " + str(lines))
    
    classification, lexeme = tokens.pop()

    if lexeme == "AN":
        comp_list.append(lexeme)
    else:
        print(classification, lexeme)
        raise LolcodeException("Syntax error in comparison - incorrect keyword: line " + str(lines))
    
    classification, lexeme = tokens.pop()
    
    if lexeme == "BIGGR OF" or lexeme == "SMALLR OF":
        comp_list.append(lexeme)
    elif res:= var_or_lit_or_expr(classification, lexeme):
        comp_list.append(res)
        return comp_list
    else:
        print(classification, lexeme)
        raise LolcodeException("Syntax error in comparison - incorrect operand: line " + str(lines))
    
    classification, lexeme = tokens.pop()

    if res := var_or_lit_or_expr(classification, lexeme):
        comp_list.append(res)
    else:
        print(classification, lexeme)
        raise LolcodeException("Syntax error in comparison - incorrect operand: line " + str(lines))
    
    classification, lexeme = tokens.pop()

    if lexeme == "AN":
        comp_list.append(lexeme)
    else:
        print(classification, lexeme)
        raise LolcodeException("Syntax error in comparison - incorrect keyword: line " + str(lines))
    
    classification, lexeme = tokens.pop()

    if res := var_or_lit_or_expr(classification, lexeme):
        comp_list.append(res)
    else:
        print(classification, lexeme)
        raise LolcodeException("Syntax error in comparison - incorrect operand: line " + str(lines))
    
    return comp_list

def bool_expr_parse():
    # print("boolean expression parse, non-infinite arity")
    bool_expr_list = []
    classification, lexeme = tokens.pop()
    bool_expr_list.append(lexeme)
    
    if lexeme == "NOT":
        classification, lexeme = tokens.pop()  
        if res := var_or_lit_or_expr(classification, lexeme):
            bool_expr_list.append(res)
        else:
            print(classification, lexeme)
            raise LolcodeException("Syntax error in boolean expression - incorrect operand: line + " + str(lines))
    elif lexeme == "BOTH OF" or lexeme == "EITHER OF" or lexeme == "WON OF":
        classification, lexeme = tokens.pop()
        if res := var_or_lit_or_expr(classification, lexeme):
            bool_expr_list.append(res)
        else:
            print(classification, lexeme)
            raise LolcodeException("Syntax error in boolean expression - incorrect operand: line + " + str(lines))
        
        classification, lexeme = tokens.pop()
        if lexeme == "AN":
            bool_expr_list.append(lexeme)
        else:
            print(classification, lexeme)
            raise LolcodeException("Syntax error in boolean expression - incorrect keyword: line + " + str(lines))
        
        classification, lexeme = tokens.pop()
        if res := var_or_lit_or_expr(classification, lexeme):
            bool_expr_list.append(res)
        else:
            print(classification, lexeme)
            raise LolcodeException("Syntax error in boolean expression - incorrect operand: line + " + str(lines))
    
    return bool_expr_list

def bool_all_any_parse():
    # print("boolean expression parse, all of/any of")
    bool_all_any_list = []
    classification, lexeme = tokens.pop()
    bool_all_any_list.append(lexeme)
    classification, lexeme = tokens.pop()

    if res := var_or_lit_or_expr(classification, lexeme):
        bool_all_any_list.append(res)
    else:
        print(classification, lexeme)
        raise LolcodeException("Syntax error in boolean expression - incorrect operand: line " + str(lines))
    
    while True:
        classification, lexeme = tokens.pop()
        if lexeme == "AN":
            bool_all_any_list.append(lexeme)
            classification, lexeme = tokens.pop()
            if res := var_or_lit_or_expr(classification, lexeme):
                bool_all_any_list.append(res)
            else:
                print(classification, lexeme)
                raise LolcodeException("Syntax error in boolean expression - incorrect operand: line " + str(lines))
        elif lexeme == "MKAY":
            bool_all_any_list.append(lexeme)
            break
        else:
            print(classification, lexeme)
            raise LolcodeException("Syntax error in boolean expression - missing 'MKAY' terminating keyword: line " + str(lines))
    
    return bool_all_any_list
        
def statement_parse():                  # statement parse
    # print("parsing statement")
    classification, lexeme = tokens.pop()
    # print(tokens[-5:])
    # print(classification, lexeme)

    if classification == "KEYWORD" or classification == "VARIABLE":         # if keyword or variable, correct syntax
        tokens.append((classification, lexeme))
        if lexeme == "VISIBLE":                     # if VISIBLE keyword found, go to print parse and return its output
            return print_parse()
        elif lexeme == "GIMMEH":
            return input_parse()
        elif lexeme == "BOTH SAEM" or lexeme == "DIFFRINT":
            return comp_parse()
        elif lexeme == "O RLY?":
            return if_parse()
        elif lexeme == "WTF?":
            return switch_parse()
        elif lexeme == "IM IN YR":
            return loop_parse()
        elif lexeme == "HOW IZ I":
            return func_dec_parse()
        elif lexeme == "I IZ":
            return func_call_parse()
        elif classification == "VARIABLE":
            return assign_parse()
        else:
            print(classification, lexeme)
            raise LolcodeException("Syntax error in program - unrecognized code: line " + str(lines))
        
def var_dec_section_parse():
    # print("variable declarations section parse")
    var_dec_sec_list = []
    global lines
    classification, lexeme = tokens.pop()
    var_dec_sec_list.append(lexeme)
    while True:
        classification, lexeme = tokens.pop()
        if classification == "NEWLINE":
            # print(lines)
            lines += 1
            continue
        elif classification == "COMMENT":
            continue
        elif classification == "MULTI-LINE_COMMENT":
            for newline in re.findall(r"\n", lexeme):
                # print(lines)
                lines += 1
            continue
        elif lexeme == "I HAS A":
            tokens.append((classification, lexeme))
            var_dec_sec_list.append(var_dec_parse())
        elif lexeme == "BUHBYE":
            var_dec_sec_list.append(lexeme)
            break
        elif lexeme == "EOF":
            print(classification, lexeme)
            raise LolcodeException("Syntax error in variable declaration section - missing closing keyword: line " + str(lines))
        else:
            print(classification, lexeme)
            raise LolcodeException("Syntax error in variable declaration section - non-variable declaration found: line " + str(lines))
    
    return var_dec_sec_list

def program_parse():                # topmost level, checks hai and kthxbye
    # print("parsing program")
    classification, lexeme = tokens.pop()
    
    global lines

    while classification == "COMMENT" or classification == "NEWLINE":              # ignore comments at start of program
        # global lines
        if classification == "NEWLINE":
            # print(lines)
            lines += 1
        classification, lexeme = tokens.pop()
    
    # print(classification, lexeme)

    if classification == "KEYWORD":
        if lexeme == "HAI":                 # hai found
            program_list = []                       # make list and append hai
            program_list.append(lexeme)
            while True:                                     # iterate infinitely through all lexemes
                classification, lexeme = tokens.pop()
                # print(classification, lexeme)
                if classification == "NEWLINE":                 # ignore newline and comments
                    # print(lines)
                    lines += 1
                    continue
                elif classification == "COMMENT":
                    continue
                elif classification == "MULTI-LINE_COMMENT":
                    for newline in re.findall(r"\n", lexeme):
                        # print(lines)
                        lines += 1
                    continue
                elif lexeme == "WAZZUP":
                    tokens.append((classification, lexeme))
                    program_list.append(var_dec_section_parse())
                elif lexeme == "KTHXBYE":                   # if end of program found, exit and return program list 
                    program_list.append(lexeme)
                    return program_list
                elif lexeme == "EOF":
                    print(classification, lexeme)
                    raise LolcodeException("Syntax error in program - missing closing keyword: line " + str(lines))
                else:
                    tokens.append((classification, lexeme))         # otherwise, found other keyword, statement starts, go to parse statement and append that statement to list
                    program_list.append(statement_parse())
        else:
            print("Parse error!")

lines = 1
# ======= SOME REFERENCES
# https://www.booleanworld.com/building-recursive-descent-parsers-definitive-guide/
# https://cratecode.com/info/python-recursive-descent-parser
# https://stackoverflow.com/questions/19749883/how-to-parse-parenthetical-trees-in-python