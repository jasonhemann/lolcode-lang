import grab_lexeme

lexemeArr = []


def check_syntax(lexemeArr):
    testing_list = []

    for i in lexemeArr:
        # print(i)
        testing_list.append(i)

    # for i in testing_list:
    #     print(i)

    while (True):
        change = False
        index = 0

        # print("-----------------------------------------")
        # for i in testing_list:
        #     print(i)

        # ---------------------------------------
        for i in testing_list:
            # Literals
            if (i[1] in ["NUMBR Literal", "NUMBAR Literal", "YARN Literal", "TROOF Literal"]):
                del testing_list[index]
                testing_list.insert(index, "literal")
                change = True
            if (i[1] == "String Delimiter" and (index+2) < len(testing_list)):
                if (testing_list[index+1] == "literal" and testing_list[index+2][1] == "String Delimiter"):
                    del testing_list[index:(index+3)]
                    testing_list.insert(index, "literal")
                    change = True

            # Variable Identifier
            if (i[1] == "Variable Identifier"):
                del testing_list[index]
                testing_list.insert(index, "varident")
                change = True

            # Input statement
            if (i[0] == "GIMMEH" and (index+1) < len(testing_list)):
                if (testing_list[index+1] == "varident"):
                    del testing_list[index:(index+2)]
                    testing_list.insert(index, "input")
                    change = True

            # Variable initialization
            if (i[0] == "I HAS A" and (index+2) < len(testing_list)):  # ***
                if (testing_list[index+1] == "varident" and testing_list[index+2][0] != "ITZ"):
                    del testing_list[index:(index+2)]
                    testing_list.insert(index, "varinit")
                    change = True

            # Variable assignment
            if (i == "varident" and (index+1) < len(testing_list)):
                if (testing_list[(index+1)][0] == "R"):
                    del testing_list[index:(index+2)]
                    testing_list.insert(index, "varassignstart")
                    change = True

            # String concatenation (Expression)
            if (i[0] == "SMOOSH" and (index+3) < len(testing_list)):
                if (testing_list[index+1] in ["literal", "varident", "concats"] and testing_list[index+2][0] == "AN" and testing_list[index+3] in ["literal", "varident"]):
                    del testing_list[(index+1):(index+4)]
                    testing_list.insert((index+1), "concats")
                    change = True

            # Typecasting
            if (i[0] == "MAEK" and (index+3) < len(testing_list)):
                if (testing_list[index+1] == "varident" and testing_list[index+2][0] == "A" and testing_list[index+3][1] == "TYPE Literal"):
                    del testing_list[index:(index+4)]
                    testing_list.insert(index, "typecast")
                    change = True
            if (i[0] == "MAEK" and (index+2) < len(testing_list)):
                if (testing_list[index+1] == "varident" and testing_list[index+2][1] == "TYPE Literal"):
                    del testing_list[index:(index+3)]
                    testing_list.insert(index, "typecast")
                    change = True
            if (i == "varident" and (index+2) < len(testing_list)):
                if (testing_list[index+1][0] == "IS NOW A" and testing_list[index+2][1] == "TYPE Literal"):
                    del testing_list[index:(index+3)]
                    testing_list.insert(index, "typecast")
                    change = True

            # break
            if (i[0] == "GTFO"):
                del testing_list[index]
                testing_list.insert(index, "break")
                change = True

            # Comment
            if (i[0] == "OBTW" or i[1] == "comment" or i[0] == "TLDR" or i[0] == "BTW"):
                del testing_list[index]
                change = True

            # Linebreak
            if (i[1] == "linebreak"):
                del testing_list[index]
                testing_list.insert(index, "linebreak")
                change = True
            if (i == "linebreak" and (index+1) < len(testing_list)):
                if (testing_list[index+1] == "linebreak"):
                    del testing_list[index:(index+2)]
                    testing_list.insert(index, "linebreak")
                    change = True

            # Invalid
            if (i[1] == "Invalid"):
                print("Invalid Syntax")
                return (False)
            index += 1

        if (change == False):
            # print("Phase 1")
            break

    # for i in testing_list:
    #     print(i)

    # ---------------------------------------
    while (True):
        change = False
        index = 0

        for i in testing_list:
            # More String concatenation
            if (i[0] == "SMOOSH" and (index+1) < len(testing_list)):
                if (testing_list[index+1] == "concats"):
                    del testing_list[index:(index+2)]
                    testing_list.insert(index, "expr")
                    change = True
            # Print statement
            if (i[0] == "VISIBLE" and (index+2) < len(testing_list)):
                if (testing_list[index+1] in ["printblock", "expr", "literal", "varident"] and testing_list[index+2] in ["expr", "literal", "varident"]):
                    del testing_list[(index+1):(index+3)]
                    testing_list.insert((index+1), "printblock")
                    change = True
                if (testing_list[index+1] in ["expr", "literal", "varident"] and testing_list[index+2][0] not in ["expr", "literal", "varident"]):
                    del testing_list[(index+1)]
                    testing_list.insert((index+1), "printblock")
                    change = True

            if (i[0] == "VISIBLE" and (index+3) < len(testing_list)):
                if (testing_list[index+1] in ["printblock", "expr", "literal", "varident"] and testing_list[index+2][0] == "AN" and testing_list[index+3] in ["expr", "literal", "varident"]):
                    del testing_list[(index+1):(index+4)]
                    testing_list.insert((index+1), "printblock")
                    change = True

            # Variable assignment
            if (i == "varassignstart" and (index+1) < len(testing_list)):
                if (testing_list[index+1] in ["literal", "varident", "expr", "typecast"]):
                    del testing_list[index:(index+2)]
                    testing_list.insert(index, "varassign")
                    change = True

            # Variable initialization 2
            if (i[0] == "I HAS A" and (index+3) < len(testing_list)):
                if (testing_list[index+1] == "varident" and testing_list[index+2][0] == "ITZ" and testing_list[index+3] in ["literal", "expr"]):
                    del testing_list[index:(index+4)]
                    testing_list.insert(index, "varinit")
                    change = True

            #Operations (Expression)
            if (i[0] in ["SUM OF", "DIFF OF", "PRODUKT OF", "QUOSHUNT OF", "MOD OF", "BIGGR OF", "SMALLR OF", "BOTH SAEM", "DIFFRINT"] and (index+3) < len(testing_list)):
                if (testing_list[index+1] in ["literal", "varident", "expr"] and testing_list[index+2][0] == "AN" and testing_list[index+3] in ["literal", "varident", "expr"]):
                    del testing_list[index:(index+4)]
                    testing_list.insert(index, "expr")
                    change = True

            # Boolean operations (expression)
            if (i[0] == "NOT" and (index+1) < len(testing_list)):
                if (testing_list[index+1] in ["literal", "varident", "expr", "boolop"]):
                    del testing_list[index:(index+2)]
                    testing_list.insert(index, "boolop")
                    change = True
            if (i[0] in ["BOTH OF", "EITHER OF", "WON OF"] and (index+3) < len(testing_list)):
                if (testing_list[index+1] in ["literal", "varident", "expr", "boolop"] and testing_list[index+2][0] == "AN" and testing_list[index+3] in ["literal", "varident", "expr", "boolop"]):
                    del testing_list[index:(index+4)]
                    testing_list.insert(index, "boolop")
                    change = True
            if (i in ["boolop", "varident", "literal"] and (index+3) < len(testing_list)):
                if (testing_list[index+1][0] == "AN" and testing_list[index+2] in ["boolop", "infstatement", "varident", "literal"] and testing_list[index+3][0] == "MKAY"):
                    del testing_list[index:(index+3)]
                    testing_list.insert(index, "infstatement")
                    change = True
            if (i[0] in ["ANY OF", "ALL OF"] and (index+2) < len(testing_list)):
                if (testing_list[index+1] == "infstatement" and testing_list[index+2][0] == "MKAY"):
                    del testing_list[index:(index+3)]
                    testing_list.insert(index, "expr")
                    change = True
            # print("------------------------------------")

            index += 1

        if (change == False):
            # print("Phase 2")
            # for i in testing_list:
            #     print(i)
            break

    # ---------------------------------------
    while (True):
        change = False
        index = 0

        for i in testing_list:
            if (i == "boolop"):
                del testing_list[index]
                testing_list.insert(index, "expr")
                change = True
            if (i[0] == "VISIBLE" and (index+1) < len(testing_list)):
                if (testing_list[index+1] == "printblock"):
                    del testing_list[index:(index+2)]
                    testing_list.insert(index, "print")
                    change = True

            if (i[0] == "VISIBLE" and (index+2) < len(testing_list)):
                if (testing_list[index+1] in ["printblock", "expr", "literal", "varident"] and testing_list[index+2] in ["expr", "literal", "varident"]):
                    del testing_list[(index+1):(index+3)]
                    testing_list.insert((index+1), "printblock")
                    change = True
                if (testing_list[index+1] in ["expr", "literal", "varident"] and testing_list[index+2][0] not in ["expr", "literal", "varident"]):
                    del testing_list[(index+1)]
                    testing_list.insert((index+1), "printblock")
                    change = True
            # if-else
            if (i[0] in ["YA RLY", "NO WAI"] and (index+4) < len(testing_list)):
                if (testing_list[index+1] == "linebreak" and testing_list[index+2] in ["expr", "ifelseStatement", "print", "input", "typecast", "varassign", "varident"] and testing_list[index+3] == "linebreak" and testing_list[index+4] in ["expr", "print", "input", "typecast", "varassign", "varident"]):
                    del testing_list[(index+1):(index+5)]
                    testing_list.insert((index+1), "linebreak")
                    testing_list.insert((index+2), "ifelseStatement")
                    change = True
            if (i[0] == "YA RLY" and (index+4) < len(testing_list)):
                if (testing_list[index+1] == "linebreak" and testing_list[index+2] in ["expr", "print", "input", "typecast", "varassign", "varident"] and testing_list[index+3] == "linebreak" and testing_list[index+4][0] in ["OIC", "NO WAI"]):
                    del testing_list[index+2]
                    testing_list.insert((index+2), "ifelseStatement")
                    change = True
            if (i[0] == "NO WAI" and (index+4) < len(testing_list)):
                if (testing_list[index+1] == "linebreak" and testing_list[index+2] in ["expr", "print", "input", "typecast", "varassign", "varident"] and testing_list[index+3] == "linebreak" and testing_list[index+4][0] in ["OIC", "NO WAI"]):
                    del testing_list[index+2]
                    testing_list.insert((index+2), "ifelseStatement")
                    change = True
            if (i[0] == "O RLY?" and (index+6) < len(testing_list)):
                if (testing_list[index+1] == "linebreak" and testing_list[index+2][0] == "YA RLY" and testing_list[index+3] == "linebreak" and testing_list[index+4] == "ifelseStatement" and testing_list[index+5] == "linebreak" and testing_list[index+6][0] == "OIC"):
                    del testing_list[index:(index+7)]
                    testing_list.insert(index, "ifelse")
                    change = True
            if (i[0] == "O RLY?" and (index+5) < len(testing_list)):
                if (testing_list[index+1] == "linebreak" and testing_list[index+2][0] == "YA RLY" and testing_list[index+3] == "linebreak" and testing_list[index+4] == "ifelseStatement" and testing_list[index+5] == "linebreak" and testing_list[index+6][0] == "NO WAI" and testing_list[index+7] == "linebreak" and testing_list[index+8] == "ifelseStatement" and testing_list[index+9] == "linebreak" and testing_list[index+10][0] == "OIC"):
                    del testing_list[index:(index+11)]
                    testing_list.insert(index, "ifelse")
                    change = True

            # Switch-case statements
            if (i[0] == "OMG" and (index+1) < len(testing_list)):
                if (testing_list[index+1] == "literal"):
                    del testing_list[index:(index+2)]
                    testing_list.insert(index, "case")
                    change = True
            if (i[0] == "OMGWTF"):
                del testing_list[index]
                testing_list.insert(index, "case")
                change = True

            if (i == "case" and (index+4) < len(testing_list)):
                if (testing_list[index+1] == "linebreak" and testing_list[index+2] in ["expr", "caseblock", "input", "print", "typecast", "print", "break", "varassign", "varident"] and testing_list[index+3] == "linebreak" and testing_list[index+4] in ["expr", "input", "print", "typecast", "print", "break", "varassign", "varident"]):
                    del testing_list[(index+2):(index+5)]
                    testing_list.insert((index+2), "caseblock")
                    change = True
                if (testing_list[index+1] == "linebreak" and testing_list[index+2] in ["input", "print", "typecast", "print", "break", "varident"] and testing_list[index+3] == "linebreak" and (testing_list[index+4][0] == "OIC" or testing_list[index+4] == "case")):
                    del testing_list[index+2]
                    testing_list.insert((index+2), "caseblock")
                    change = True

            index += 1

        if (change == False):
            # print("Phase 3")
            # for i in testing_list:
            #     print(i)
            break

    # ---------------------------------------
    while (True):
        change = False
        index = 0

        for i in testing_list:
            # Switch case 2
            if (i == "case" and (index+2) < len(testing_list)):
                if (testing_list[index+1] == "linebreak" and testing_list[index+2] == "caseblock"):
                    del testing_list[index:(index+3)]
                    testing_list.insert(index, "casestatement")
                    change = True
            if (i[0] == "WTF?" and (index+4) < len(testing_list)):
                if (testing_list[index+1] == "linebreak" and testing_list[index+2] == "casestatement" and testing_list[index+3] == "linebreak" and testing_list[index+4] == "casestatement"):
                    del testing_list[(index+2):(index+5)]
                    testing_list.insert((index+2), "casestatement")
                    change = True
                if (testing_list[index+1] == "linebreak" and testing_list[index+2] == "casestatement" and testing_list[index+3] == "linebreak" and testing_list[index+4][0] == "OIC"):
                    del testing_list[index:(index+5)]
                    testing_list.insert(index, "switchcase")
                    change = True
            # loops
            if (i[0] in ["TIL", "WILE"] and (index+1) < len(testing_list)):
                if (testing_list[index+1] == "expr"):
                    del testing_list[index:(index+2)]
                    testing_list.insert(index, "tilwhile")
                    change = True
            if (i[0] == "IM IN YR" and (index+5) < len(testing_list)):
                if (testing_list[index+1] == "varident" and testing_list[index+2][0] in ["UPPIN", "NERFIN"] and testing_list[index+3][0] == "YR" and testing_list[index+4] == "varident" and testing_list[index+5] == "tilwhile"):
                    del testing_list[index:(index+6)]
                    testing_list.insert(index, "loopstart")
                    change = True
            if (i[0] == "IM OUTTA YR" and (index+1) < len(testing_list)):
                if (testing_list[index+1] == "varident"):
                    del testing_list[index:(index+2)]
                    testing_list.insert(index, "loopend")
                    change = True

            if (i == "loopstart" and (index+4) < len(testing_list)):
                if (testing_list[index+1] == "linebreak" and testing_list[index+2] in ["loopblock", "expr", "print", "input", "typecast", "varassign", "ifelse", "switchcase", "varident"] and testing_list[index+3] == "linebreak" and testing_list[index+4] in ["loopblock", "expr", "print", "input", "typecast", "varassign", "ifelse", "switchcase", "varident"]):
                    del testing_list[(index+2):(index+5)]
                    testing_list.insert((index+2), "loopblock")
                    change = True
                if (testing_list[index+1] == "linebreak" and testing_list[index+2] in ["expr", "print", "input", "typecast", "varassign", "ifelse", "switchcase", "varident"] and testing_list[index+3] == "linebreak" and testing_list[index+4] == "loopend"):
                    del testing_list[(index+2)]
                    testing_list.insert((index+2), "loopblock")
                    change = True
                if (testing_list[index+1] == "linebreak" and testing_list[index+2] == "loopblock" and testing_list[index+3] == "linebreak" and testing_list[index+4] == "loopend"):
                    del testing_list[index:(index+5)]
                    testing_list.insert(index, "loop")
                    change = True
            index += 1

        if (change == False):
            # print("Phase 4")
            # for i in testing_list:
            #     print(i)
            break

    # ---------------------------------------

    while (True):
        change = False
        index = 0

        # print("-----------------------------------------")
        # for i in testing_list:
        #     print(i)

        for i in testing_list:
            # Chunky parts
            if (i == "linebreak" and (index+1) < len(testing_list)):
                if (testing_list[index+1][0] == "HAI"):
                    del testing_list[index]
                    change = True
            if (i == "statement" and (index+2) < len(testing_list)):
                if (testing_list[index+1] == "linebreak" and testing_list[index+2] == "statement"):
                    del testing_list[index:(index+3)]
                    testing_list.insert(index, "statement")
                    change = True
            if (i in ["varinit", "statement2"]):
                del testing_list[index]
                testing_list.insert(index, "statement")
                change = True
            if (i in ["print", "input", "varassign", "ifelse", "expr", "switchcase", "loop", "typecast", "varident"]):
                del testing_list[index]
                testing_list.insert(index, "statement2")
                change = True

            if (i[0] == "HAI" and len(testing_list) == 6):
                if (testing_list[index+1] == "linebreak" and testing_list[index+2] == "statement" and testing_list[index+3] == "linebreak" and testing_list[index+4][0] == "KTHXBYE" and testing_list[index+5] == "linebreak"):
                    del testing_list[index:(index+7)]
                    testing_list.insert(index, "program")
                    change = True
                    print(True)

                    # for i in testing_list:
                    #     print(i)
                    return (True)
            index += 1

        if (change == False):

            print("Phase 5")
            for i in testing_list:
                print(i)

            print(False)
            return (False)
            break


def fix_obtw(lexemeArr):
    while (True):
        change = False
        index = 0

        for i in lexemeArr:
            # Chunky parts
            if (i[1] == "comment" and (index+2) < len(lexemeArr)):
                if (lexemeArr[index+1][1] == "linebreak" and lexemeArr[index+2][1] == "linebreak"):
                    del lexemeArr[(index+1):(index+3)]
                    lexemeArr.insert((index+1), ["<linebreak>", "linebreak"])
            index += 1

        break


def lex_analyze(lexemeArr, the_long_string):
    lexemeArr.clear()

    lines = the_long_string.split("\n")

    lines2 = []
    for line in lines:
        if (line != ""):
            lines2.append(line.strip())

    for i in range(0, len(lines2)):
        alreadyBlank = False
        if (lines2[i] == ""):
            alreadyBlank = True

        while (lines2[i] != ''):
            grab_lexeme.get_lexemes(lexemeArr, lines2, lines2[i], i)
        if (alreadyBlank == False):
            lexemeArr.append(["<linebreak>", "linebreak"])

    fix_obtw(lexemeArr)
    # for i in lexemeArr:
    #     print(i)

    check_syntax(lexemeArr)


h = '''HAI
    I HAS A x ITZ 1
    I HAS A y ITZ 2
    
    VISIBLE ALL OF x AN x
    VISIBLE ANY OF y AN y

KTHXBYE'''
g = """IM IN YR asc UPPIN YR num2 WILE BOTH SAEM num2 AN SMALLR OF num2 AN num1
		choice
        WTF?
		OMG 1
			choice
            VISIBLE "Enter birth year: "
			GIMMEH input
			VISIBLE DIFF OF 2022 AN input
			GTFO
		OMG 2
			VISIBLE "Enter bill cost: "
			GIMMEH input
			VISIBLE "Tip: " PRODUCKT OF input AN 0.1
			GTFO
		OMG 3
			VISIBLE "Enter width: "
			GIMMEH input
			VISIBLE "Square Area: " PRODUCKT OF input AN input
			GTFO
		OMG 0
			VISIBLE "Goodbye"
		OMGWTF
			VISIBLE "Invalid Input!"
	    OIC

        O RLY?
            YA RLY
                choice
                VISIBLE "Invalid input is > 3."
        OIC
        
	IM OUTTA YR asc"""

lex_analyze(lexemeArr, h)
