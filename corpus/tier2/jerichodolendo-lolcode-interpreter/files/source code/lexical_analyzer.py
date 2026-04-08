import re
from regex import *

# function that checks if a token has any regex matches


def analyze_tokens(lexemeTups, line):
    global comm_lit, BTW_flag, OBTW_flag
    x = line
    j = 0

    while (re.match("^( *)$", x) == None):
        if (re.match("^[ \t]*", x)):
            x = re.sub("^[ \t]*", "", x, 1)

        # comments
        if (BTW_flag == 1):
            c = re.match(comment_lit, x).group()
            x = re.sub(c, "", x, 1)
            print(c, "\t == Comment Literal")
            lexemeTups.append((c, "Comment Literal"))
            BTW_flag = 0
        elif (OBTW_flag == 1):
            if (re.match(multiple_end, x)):
                x = re.sub(multiple_end, "", x, 1)
                print("TLDR\t== Multiple line comment ends")
                lexemeTups.append(("TLDR", "Multiple line comment ends"))
                OBTW_flag = 0
            else:
                c = re.match(comment_lit, x).group()
                x = re.sub(c, "", x, 1)
                print(c, "\t == Part of Comment Block")
                lexemeTups.append((c, "Part of Comment Block"))

        # code
        if (re.match(single_line, x)):
            x = re.sub(single_line, "", x, 1)
            print("BTW\t== Single line comment")
            lexemeTups.append(("BTW", "Single line comment"))
            BTW_flag = 1

        elif (re.match(multiple_start, x)):
            x = re.sub(multiple_start, "", x, 1)
            print("OBTW\t== Multiple line comment starts")
            lexemeTups.append(("OBTW", "Multiple line comment starts"))
            OBTW_flag = 1

        elif (re.match(start, x)):
            x = re.sub(start, "", x, 1)
            print("HAI\t == Program Start Keyword")
            lexemeTups.append(("HAI", "Program Start Keyword"))

        elif (re.match(end, x)):
            x = re.sub(end, "", x, 1)
            print("KTHXBYE\t == Program End Keyword")
            lexemeTups.append(("KTHXBYE", "Program End Keyword"))

        elif (re.match(declaration, x)):
            x = re.sub(declaration, "", x, 1)
            print("I HAS A\t == Variable Declaration")
            lexemeTups.append(("I HAS A", "Variable Declaration"))

        elif (re.match(assignment_var, x)):
            x = re.sub(assignment_var, "", x, 1)
            print("ITZ\t == Assignment Initialize Keyword")
            lexemeTups.append(("ITZ", "Assignment Initialize Keyword"))

        elif (re.match(assignment_op, x)):
            x = re.sub(assignment_op, "", x, 1)
            print("R\t == Assignment Operator Keyword")
            lexemeTups.append(("R", "Assignment Operator Keyword"))

        elif (re.match(and_operator, x)):
            x = re.sub(and_operator, "", x, 1)
            print("BOTH OF\t == AND Operator")
            lexemeTups.append(("BOTH OF", "AND Operator"))

        elif (re.match(or_operator, x)):
            x = re.sub(or_operator, "", x, 1)
            print("EITHER OF\t == OR Operator")
            lexemeTups.append(("EITHER OF", "OR Operator"))

        elif (re.match(xor_operator, x)):
            x = re.sub(xor_operator, "", x, 1)
            print("WON OF\t == XOR Operator")
            lexemeTups.append(("WON OF", "XOR Operator"))

        elif (re.match(not_operator, x)):
            x = re.sub(not_operator, "", x, 1)
            print("NOT\t == Not Operator")
            lexemeTups.append(("NOT", "Not Operator"))

        elif (re.match(arity_and, x)):
            x = re.sub(arity_and, "", x, 1)
            print("ALL OF\t == Infinite Arity AND Keyword")
            lexemeTups.append(("ALL OF", "Infinite Arity AND Keyword"))

        elif (re.match(arity_or, x)):
            x = re.sub(arity_or, "", x, 1)
            print("ANY OF\t == Infinite Arity OR Keyword")
            lexemeTups.append(("ANY OF", "Infinite Arity OR Keyword"))

        elif (re.match(operand_sep, x)):
            x = re.sub(operand_sep, "", x, 1)
            print("AN\t == Operand Separator Keyword")
            lexemeTups.append(("AN", "Operand Separator Keyword"))

        elif (re.match(plus, x)):
            x = re.sub(plus, "", x, 1)
            print("SUM OF\t == Addition Operator")
            lexemeTups.append(("SUM OF", "Addition Operator"))

        elif (re.match(difference, x)):
            x = re.sub(difference, "", x, 1)
            print("DIFF OF\t == Subtraction Operator")
            lexemeTups.append(("DIFF OF", "Subtraction Operator"))

        elif (re.match(multiply, x)):
            x = re.sub(multiply, "", x, 1)
            print("PRODUKT OF\t == Multiplication Operator")
            lexemeTups.append(("PRODUKT OF", "Multiplication Operator"))

        elif (re.match(divide, x)):
            x = re.sub(divide, "", x, 1)
            print("QUOSHUNT OF\t == Division Operator")
            lexemeTups.append(("QUOSHUNT OF", "Division Operator"))

        elif (re.match(modulo, x)):
            x = re.sub(modulo, "", x, 1)
            print("MOD OF\t == Modulo Operator")
            lexemeTups.append(("MOD OF", "Modulo Operator"))

        elif (re.match(greater_than, x)):
            x = re.sub(greater_than, "", x, 1)
            print("BIGGR OF\t == Max Operator")
            lexemeTups.append(("BIGGR OF", "Max Operator"))

        elif (re.match(less_than, x)):
            x = re.sub(less_than, "", x, 1)
            print("SMALLR OF\t == Minimum Operator")
            lexemeTups.append(("SMALLR OF", "Minimum Operator"))

        elif (re.match(equal, x)):
            x = re.sub(equal, "", x, 1)
            print("BOTH SAEM\t == Equal Operator")
            lexemeTups.append(("BOTH SAEM", "Equal Operator"))

        elif (re.match(not_equal, x)):
            x = re.sub(not_equal, "", x, 1)
            print("DIFFRINT\t == Not Equal Operator")
            lexemeTups.append(("DIFFRINT", "Not Equal Operator"))

        elif (re.match(str_concat, x)):
            x = re.sub(str_concat, "", x, 1)
            print("SMOOSH\t == String Concatenator Keyword")
            lexemeTups.append(("SMOOSH", "String Concatenator Keyword"))

        elif (re.match(typecast, x)):
            x = re.sub(typecast, "", x, 1)
            print("MAEK\t == Typecast Keyword")
            lexemeTups.append(("MAEK", "Typecast Keyword"))

        elif (re.match(typecast_assign, x)):
            x = re.sub(typecast_assign, "", x, 1)
            print("A\t == Typecast Assign Keyword")
            lexemeTups.append(("A", "Typecast Assign Keyword"))

        elif (re.match(recast, x)):
            x = re.sub(recast, "", x, 1)
            print("IS NOW A\t == Recast Keyword")
            lexemeTups.append(("IS NOW A", "Recast Keyword"))

        elif (re.match(printing, x)):
            x = re.sub(printing, "", x, 1)
            print("VISIBLE\t == Output/Printing Keyword")
            lexemeTups.append(("VISIBLE", "Output/Printing Keyword"))

        elif (re.match(inputting, x)):
            x = re.sub(inputting, "", x, 1)
            print("GIMMEH\t == Inputting Keyword")
            lexemeTups.append(("GIMMEH", "Inputting Keyword"))

        elif (re.match(if_start, x)):
            x = re.sub(if_start, "", x, 1)
            print("O RLY?\t == If Start Keyword")
            lexemeTups.append(("O RLY?", "If Start Keyword"))

        elif (re.match(if_cond, x)):
            x = re.sub(if_cond, "", x, 1)
            print("YA RLY\t == If Condition Keyword")
            lexemeTups.append(("YA RLY", "If Condition Keyword"))

        elif (re.match(elif_cond, x)):
            x = re.sub(elif_cond, "", x, 1)
            print("MEBBE\t == Elif Condition Keyword")
            lexemeTups.append(("MEBBE", "Elif Condition Keyword"))

        elif (re.match(else_cond, x)):
            x = re.sub(else_cond, "", x, 1)
            print("NO WAI\t == Else Condition Keyword")
            lexemeTups.append(("NO WAI", "Else Condition Keyword"))

        elif (re.match(if_end, x)):
            x = re.sub(if_end, "", x, 1)
            print("OIC\t == If End Keyword")
            lexemeTups.append(("OIC", "If End Keyword"))

        elif (re.match(switch_case, x)):
            x = re.sub(switch_case, "", x, 1)
            print("WTF?\t == Switch Case Start Keyword")
            lexemeTups.append(("WTF?", "Switch Case Start Keyword"))

        elif (re.match(case, x)):
            x = re.sub(case, "", x, 1)
            print("OMG\t == Case Condition Keyword")
            lexemeTups.append(("OMG", "Case Condition Keyword"))

        elif (re.match(default, x)):
            x = re.sub(default, "", x, 1)
            print("OMGWTF\t == Default Condition Keyword")
            lexemeTups.append(("OMGWTF", "Default Condition Keyword"))

        elif (re.match(break_key, x)):
            x = re.sub(break_key, "", x, 1)
            print("GTFO\t == Break Keyword")
            lexemeTups.append(("GTFO", "Break Keyword"))

        elif (re.match(loop_start, x)):
            x = re.sub(loop_start, "", x, 1)
            print("IM IN YR\t == Loop Start Keyword")
            lexemeTups.append(("IM IN YR", "Loop Start Keyword"))

        elif (re.match(increment, x)):
            x = re.sub(increment, "", x, 1)
            print("UPPIN\t == Loop Increment Keyword")
            lexemeTups.append(("UPPIN", "Loop Increment Keyword"))

        elif (re.match(decrement, x)):
            x = re.sub(decrement, "", x, 1)
            print("NERFIN\t == Loop Decrement Keyword")
            lexemeTups.append(("NERFIN", "Loop Decrement Keyword"))

        elif (re.match(loop_cond, x)):
            x = re.sub(loop_cond, "", x, 1)
            print("YR\t == Loop Condition Keyword")
            lexemeTups.append(("YR", "Loop Condition Keyword"))

        elif (re.match(til, x)):
            x = re.sub(til, "", x, 1)
            print("TIL\t == Loop Until Keyword")
            lexemeTups.append(("TIL", "Loop Until Keyword"))

        elif (re.match(wile, x)):
            x = re.sub(wile, "", x, 1)
            print("WILE\t == Loop While Keyword")
            lexemeTups.append(("WILE", "Loop While Keyword"))

        elif (re.match(loop_end, x)):
            x = re.sub(loop_end, "", x, 1)
            print("IM OUTTA YR\t == Loop End Keyword")
            lexemeTups.append(("IM OUTTA YR", "Loop End Keyword"))

        elif (re.match(NUMBAR, x)):
            n = re.match(NUMBAR, x).group()
            x = re.sub(NUMBAR, "", x, 1)
            print(f"{n}\t == NUMBAR")
            lexemeTups.append((f"{n}", "NUMBAR"))

        elif (re.match(NUMBR, x)):
            n = re.match(NUMBR, x).group()
            x = re.sub(NUMBR, "", x, 1)
            print(f"{n}\t == NUMBR")
            lexemeTups.append((f"{n}", "NUMBR"))

        elif (re.match(YARN, x)):
            n = re.match(YARN, x).group()
            x = re.sub(YARN, "", x, 1)
            print(f"{n}\t == YARN literal")
            lexemeTups.append((f"{n}", "YARN literal"))

        elif (re.match(TROOF, x)):
            n = re.match(TROOF, x).group()
            x = re.sub(TROOF, "", x, 1)
            print(f"{n}\t == TROOF")
            lexemeTups.append((f"{n}", "TROOF"))

        elif (re.match(TYPE, x)):
            n = re.match(TYPE, x).group()
            x = re.sub(TYPE, "", x, 1)
            print(f"{n}\t == TYPE literal")
            lexemeTups.append((f"{n}", "TYPE literal"))

        elif (re.match(variable, x)):
            n = re.match(variable, x).group()
            x = re.sub(variable, "", x, 1)
            print(f"{n}\t == Variable Identifier")
            lexemeTups.append((f"{n}", "Variable Identifier"))

        # newline
        if (re.match("^( *\n)$", x)):
            x = re.sub(new_line, "", x, 1)
            print("\\n\t== New Line")
            lexemeTups.append(("\\n", "New Line"))
