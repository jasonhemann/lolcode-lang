import re

def get_lexemes(lexemeArr, lines, line, index):
    
    if(len(re.findall(".+OBTW", line)) != 0):
        lexeme_info = [line, "Invalid"]
        lexemeArr.append(lexeme_info)
        lines.remove(line)
        lines.insert(index, "")
        return
    elif(len(re.findall(".+ TLDR.*", line)) != 0):
        comment = re.sub(" TLDR.*", "", line)
        lexemeArr.append([comment, "comment"])
        lexemeArr.append(["TLDR", "keyword"])
        
        remain = re.sub(".*TLDR", "", line).strip()
        if(remain != ""):
            lexemeArr.append([remain, "Invalid"])
        
        lines.remove(line)
        lines.insert(index, "")
        return
    elif(len(re.findall("^TLDR .*", line)) != 0):
        lexemeArr.append(["TLDR", "keyword"])
        remain = re.sub("TLDR", "", line)
        if(remain != ""):
            lexemeArr.append([remain, "Invalid"])
        lines.remove(line)
        lines.insert(index, "")
        return


    if(len(re.findall("^\"[^\"]*\"", line)) != 0):
        exact = re.findall("\"[^\"]*\"", line)[0]
        exact2 = re.sub("\"", "", exact)

        lexeme_info2 = ["\"", "String Delimiter"]
        lexeme_info = []
        lexeme_info.append(exact2)
        lexeme_info.append("YARN Literal")
        lexemeArr.append(lexeme_info2)
        lexemeArr.append(lexeme_info)
        lexemeArr.append(lexeme_info2)
        
        num_exact = len(exact)
        new = line[num_exact:len(line)]
        lines.remove(line)
        lines.insert(index, new.strip())
        
    elif(len(re.findall("^WIN", line)) != 0):
        lexeme_info = []
        lexeme_info.append("WIN")
        lexeme_info.append("TROOF Literal")
        lexemeArr.append(lexeme_info)
        
        num_exact = len("WIN")
        new = line[num_exact:len(line)]
        lines.remove(line)
        lines.insert(index, new.strip())
    
    elif(len(re.findall("^FAIL", line)) != 0):
        lexeme_info = []
        lexeme_info.append("FAIL")
        lexeme_info.append("TROOF Literal")
        lexemeArr.append(lexeme_info)
        
        num_exact = len("FAIL")
        new = line[num_exact:len(line)]
        lines.remove(line)
        lines.insert(index, new.strip())
    
    elif(len(re.findall("^NUMBR", line)) != 0):
        lexeme_info = []
        lexeme_info.append("NUMBR")
        lexeme_info.append("TYPE Literal")
        lexemeArr.append(lexeme_info)
        
        num_exact = len("NUMBR")
        new = line[num_exact:len(line)]
        lines.remove(line)
        lines.insert(index, new.strip())
    
    elif(len(re.findall("^NUMBAR", line)) != 0):
        lexeme_info = []
        lexeme_info.append("NUMBAR")
        lexeme_info.append("TYPE Literal")
        lexemeArr.append(lexeme_info)
        
        num_exact = len("NUMBAR")
        new = line[num_exact:len(line)]
        lines.remove(line)
        lines.insert(index, new.strip())
    
    elif(len(re.findall("^YARN", line)) != 0):
        lexeme_info = []
        lexeme_info.append("YARN")
        lexeme_info.append("TYPE Literal")
        lexemeArr.append(lexeme_info)
        
        num_exact = len("YARN")
        new = line[num_exact:len(line)]
        lines.remove(line)
        lines.insert(index, new.strip())
    
    elif(len(re.findall("^TROOF", line)) != 0):
        lexeme_info = []
        lexeme_info.append("TROOF")
        lexeme_info.append("TYPE Literal")
        lexemeArr.append(lexeme_info)
        
        num_exact = len("TROOF")
        new = line[num_exact:len(line)]
        lines.remove(line)
        lines.insert(index, new.strip())

    elif(len(re.findall("^HAI", line)) != 0):
        lexeme_info = []
        lexeme_info.append("HAI")
        lexeme_info.append("keyword")
        lexemeArr.append(lexeme_info)
        
        num_exact = len("HAI")
        new = line[num_exact:len(line)]
        lines.remove(line)
        lines.insert(index, new.strip())
    
    elif(len(re.findall("^KTHXBYE", line)) != 0):
        lexeme_info = []
        lexeme_info.append("KTHXBYE")
        lexeme_info.append("keyword")
        lexemeArr.append(lexeme_info)
        
        num_exact = len("KTHXBYE")
        new = line[num_exact:len(line)]
        lines.remove(line)
        lines.insert(index, new.strip())

    elif(len(re.findall("^TLDR$", line)) != 0):
        lexeme_info = []
        lexeme_info.append("TLDR")
        lexeme_info.append("keyword")
        lexemeArr.append(lexeme_info)
        
        num_exact = len("TLDR")
        new = line[num_exact:len(line)]
        lines.remove(line)
        lines.insert(index, "")

    elif(len(re.findall("^OBTW", line)) != 0):
        lexeme_info = []
        lexeme_info.append("OBTW")
        lexeme_info.append("keyword")
        lexemeArr.append(lexeme_info)
        
        num_exact = len("OBTW")
        new = line[num_exact:len(line)].strip()
        if(new != ""):
            lexemeArr.append([new, "comment"])
        lexemeArr.append(["<linebreak>", "linebreak"])
        
        
        index2 = index+1
        while(len(re.findall("(^TLDR )|( TLDR )|(^TLDR$)|(TLDR$)", lines[index2])) == 0):
            lexemeArr.append([lines[index2], "comment"])
            lines.remove(lines[index2])
            lines.insert(index2, "")
            lexemeArr.append(["<linebreak>", "linebreak"])
            index2 += 1
        
        # comment = new.strip() + "\n"

        # print(comment)
        lines.remove(line)
        lines.insert(index, "")

    elif(len(re.findall("^I HAS A", line)) != 0):
        lexeme_info = []
        lexeme_info.append("I HAS A")
        lexeme_info.append("keyword")
        lexemeArr.append(lexeme_info)
        
        num_exact = len("I HAS A")
        new = line[num_exact:len(line)]
        lines.remove(line)
        lines.insert(index, new.strip())
    
    elif(len(re.findall("^ITZ", line)) != 0):
        lexeme_info = []
        lexeme_info.append("ITZ")
        lexeme_info.append("keyword")
        lexemeArr.append(lexeme_info)
        
        num_exact = len("ITZ")
        new = line[num_exact:len(line)]
        lines.remove(line)
        lines.insert(index, new.strip())


    
    elif(len(re.findall("^SUM OF", line)) != 0):
        lexeme_info = []
        lexeme_info.append("SUM OF")
        lexeme_info.append("keyword")
        lexemeArr.append(lexeme_info)
        
        num_exact = len("SUM OF")
        new = line[num_exact:len(line)]
        lines.remove(line)
        lines.insert(index, new.strip())
    
    elif(len(re.findall("^DIFF OF", line)) != 0):
        lexeme_info = []
        lexeme_info.append("DIFF OF")
        lexeme_info.append("keyword")
        lexemeArr.append(lexeme_info)
        
        num_exact = len("DIFF OF")
        new = line[num_exact:len(line)]
        lines.remove(line)
        lines.insert(index, new.strip())
    
    elif(len(re.findall("^PRODUKT OF", line)) != 0):
        lexeme_info = []
        lexeme_info.append("PRODUKT OF")
        lexeme_info.append("keyword")
        lexemeArr.append(lexeme_info)
        
        num_exact = len("PRODUKT OF")
        new = line[num_exact:len(line)]
        lines.remove(line)
        lines.insert(index, new.strip())
    
    elif(len(re.findall("^QUOSHUNT OF", line)) != 0):
        lexeme_info = []
        lexeme_info.append("QUOSHUNT OF")
        lexeme_info.append("keyword")
        lexemeArr.append(lexeme_info)
        
        num_exact = len("QUOSHUNT OF")
        new = line[num_exact:len(line)]
        lines.remove(line)
        lines.insert(index, new.strip())
    
    elif(len(re.findall("^MOD OF", line)) != 0):
        lexeme_info = []
        lexeme_info.append("MOD OF")
        lexeme_info.append("keyword")
        lexemeArr.append(lexeme_info)
        
        num_exact = len("MOD OF")
        new = line[num_exact:len(line)]
        lines.remove(line)
        lines.insert(index, new.strip())
    
    elif(len(re.findall("^BIGGR OF", line)) != 0):
        lexeme_info = []
        lexeme_info.append("BIGGR OF")
        lexeme_info.append("keyword")
        lexemeArr.append(lexeme_info)
        
        num_exact = len("BIGGR OF")
        new = line[num_exact:len(line)]
        lines.remove(line)
        lines.insert(index, new.strip())
    
    elif(len(re.findall("^SMALLR OF", line)) != 0):
        lexeme_info = []
        lexeme_info.append("SMALLR OF")
        lexeme_info.append("keyword")
        lexemeArr.append(lexeme_info)
        
        num_exact = len("SMALLR OF")
        new = line[num_exact:len(line)]
        lines.remove(line)
        lines.insert(index, new.strip())
    
    elif(len(re.findall("^BOTH OF", line)) != 0):
        lexeme_info = []
        lexeme_info.append("BOTH OF")
        lexeme_info.append("keyword")
        lexemeArr.append(lexeme_info)
        
        num_exact = len("BOTH OF")
        new = line[num_exact:len(line)]
        lines.remove(line)
        lines.insert(index, new.strip())
    
    elif(len(re.findall("^EITHER OF", line)) != 0):
        lexeme_info = []
        lexeme_info.append("EITHER OF")
        lexeme_info.append("keyword")
        lexemeArr.append(lexeme_info)
        
        num_exact = len("EITHER OF")
        new = line[num_exact:len(line)]
        lines.remove(line)
        lines.insert(index, new.strip())
    
    elif(len(re.findall("^WON OF", line)) != 0):
        lexeme_info = []
        lexeme_info.append("WON OF")
        lexeme_info.append("keyword")
        lexemeArr.append(lexeme_info)
        
        num_exact = len("WON OF")
        new = line[num_exact:len(line)]
        lines.remove(line)
        lines.insert(index, new.strip())
    
    elif(len(re.findall("^NOT", line)) != 0):
        lexeme_info = []
        lexeme_info.append("NOT")
        lexeme_info.append("keyword")
        lexemeArr.append(lexeme_info)
        
        num_exact = len("NOT")
        new = line[num_exact:len(line)]
        lines.remove(line)
        lines.insert(index, new.strip())
    
    elif(len(re.findall("^ANY OF", line)) != 0):
        lexeme_info = []
        lexeme_info.append("ANY OF")
        lexeme_info.append("keyword")
        lexemeArr.append(lexeme_info)
        
        num_exact = len("ANY OF")
        new = line[num_exact:len(line)]
        lines.remove(line)
        lines.insert(index, new.strip())
    
    elif(len(re.findall("^ALL OF", line)) != 0):
        lexeme_info = []
        lexeme_info.append("ALL OF")
        lexeme_info.append("keyword")
        lexemeArr.append(lexeme_info)
        
        num_exact = len("ALL OF")
        new = line[num_exact:len(line)]
        lines.remove(line)
        lines.insert(index, new.strip())
    
    elif(len(re.findall("^BOTH SAEM", line)) != 0):
        lexeme_info = []
        lexeme_info.append("BOTH SAEM")
        lexeme_info.append("keyword")
        lexemeArr.append(lexeme_info)
        
        num_exact = len("BOTH SAEM")
        new = line[num_exact:len(line)]
        lines.remove(line)
        lines.insert(index, new.strip())
    
    elif(len(re.findall("^DIFFRINT", line)) != 0):
        lexeme_info = []
        lexeme_info.append("DIFFRINT")
        lexeme_info.append("keyword")
        lexemeArr.append(lexeme_info)
        
        num_exact = len("DIFFRINT")
        new = line[num_exact:len(line)]
        lines.remove(line)
        lines.insert(index, new.strip())

    elif(len(re.findall("^SMOOSH", line)) != 0):
        lexeme_info = []
        lexeme_info.append("SMOOSH")
        lexeme_info.append("keyword")
        lexemeArr.append(lexeme_info)
        
        num_exact = len("SMOOSH")
        new = line[num_exact:len(line)]
        lines.remove(line)
        lines.insert(index, new.strip())
    
    elif(len(re.findall("^MAEK", line)) != 0):
        lexeme_info = []
        lexeme_info.append("MAEK")
        lexeme_info.append("keyword")
        lexemeArr.append(lexeme_info)
        
        num_exact = len("MAEK")
        new = line[num_exact:len(line)]
        lines.remove(line)
        lines.insert(index, new.strip())
    
    
    
    elif(len(re.findall("^IS NOW A", line)) != 0):
        lexeme_info = []
        lexeme_info.append("IS NOW A")
        lexeme_info.append("keyword")
        lexemeArr.append(lexeme_info)
        
        num_exact = len("IS NOW A")
        new = line[num_exact:len(line)]
        lines.remove(line)
        lines.insert(index, new.strip())
    
    elif(len(re.findall("^VISIBLE", line)) != 0):
        lexeme_info = []
        lexeme_info.append("VISIBLE")
        lexeme_info.append("keyword")
        lexemeArr.append(lexeme_info)
        
        num_exact = len("VISIBLE")
        new = line[num_exact:len(line)]
        lines.remove(line)
        lines.insert(index, new.strip())
    
    elif(len(re.findall("^GIMMEH", line)) != 0):
        lexeme_info = []
        lexeme_info.append("GIMMEH")
        lexeme_info.append("keyword")
        lexemeArr.append(lexeme_info)
        
        num_exact = len("GIMMEH")
        new = line[num_exact:len(line)]
        lines.remove(line)
        lines.insert(index, new.strip())
    
    elif(len(re.findall("^O RLY\?", line)) != 0):
        lexeme_info = []
        lexeme_info.append("O RLY?")
        lexeme_info.append("keyword")
        lexemeArr.append(lexeme_info)
        
        num_exact = len("O RLY?")
        new = line[num_exact:len(line)]
        lines.remove(line)
        lines.insert(index, new.strip())

    elif(len(re.findall("^MEBBE", line)) != 0):
        lexeme_info = []
        lexeme_info.append("MEBBE")
        lexeme_info.append("keyword")
        lexemeArr.append(lexeme_info)
        
        num_exact = len("MEBBE")
        new = line[num_exact:len(line)]
        lines.remove(line)
        lines.insert(index, new.strip())
    
    elif(len(re.findall("^YA RLY", line)) != 0):
        lexeme_info = []
        lexeme_info.append("YA RLY")
        lexeme_info.append("keyword")
        lexemeArr.append(lexeme_info)
        
        num_exact = len("YA RLY")
        new = line[num_exact:len(line)]
        lines.remove(line)
        lines.insert(index, new.strip())
    

    elif(len(re.findall("^NO WAI", line)) != 0):
        lexeme_info = []
        lexeme_info.append("NO WAI")
        lexeme_info.append("keyword")
        lexemeArr.append(lexeme_info)
        
        num_exact = len("NO WAI")
        new = line[num_exact:len(line)]
        lines.remove(line)
        lines.insert(index, new.strip())

    elif(len(re.findall("^OIC", line)) != 0):
        lexeme_info = []
        lexeme_info.append("OIC")
        lexeme_info.append("keyword")
        lexemeArr.append(lexeme_info)
        
        num_exact = len("OIC")
        new = line[num_exact:len(line)]
        lines.remove(line)
        lines.insert(index, new.strip())

    elif(len(re.findall("^WTF\?", line)) != 0):
        lexeme_info = []
        lexeme_info.append("WTF?")
        lexeme_info.append("keyword")
        lexemeArr.append(lexeme_info)
        
        num_exact = len("WTF?")
        new = line[num_exact:len(line)]
        lines.remove(line)
        lines.insert(index, new.strip())
    
    elif(len(re.findall("^OMGWTF", line)) != 0):
        lexeme_info = []
        lexeme_info.append("OMGWTF")
        lexeme_info.append("keyword")
        lexemeArr.append(lexeme_info)
        
        num_exact = len("OMGWTF")
        new = line[num_exact:len(line)]
        lines.remove(line)
        lines.insert(index, new.strip())
    
    elif(len(re.findall("^OMG", line)) != 0):
        lexeme_info = []
        lexeme_info.append("OMG")
        lexeme_info.append("keyword")
        lexemeArr.append(lexeme_info)
        
        num_exact = len("OMG")
        new = line[num_exact:len(line)]
        lines.remove(line)
        lines.insert(index, new.strip())

    elif(len(re.findall("^IM IN YR", line)) != 0):
        lexeme_info = []
        lexeme_info.append("IM IN YR")
        lexeme_info.append("keyword")
        lexemeArr.append(lexeme_info)
        
        num_exact = len("IM IN YR")
        new = line[num_exact:len(line)]
        lines.remove(line)
        lines.insert(index, new.strip())

    elif(len(re.findall("^UPPIN", line)) != 0):
        lexeme_info = []
        lexeme_info.append("UPPIN")
        lexeme_info.append("keyword")
        lexemeArr.append(lexeme_info)
        
        num_exact = len("UPPIN")
        new = line[num_exact:len(line)]
        lines.remove(line)
        lines.insert(index, new.strip())

    elif(len(re.findall("^NERFIN", line)) != 0):
        lexeme_info = []
        lexeme_info.append("NERFIN")
        lexeme_info.append("keyword")
        lexemeArr.append(lexeme_info)
        
        num_exact = len("NERFIN")
        new = line[num_exact:len(line)]
        lines.remove(line)
        lines.insert(index, new.strip())
    
    elif(len(re.findall("^MKAY", line)) != 0):
        lexeme_info = []
        lexeme_info.append("MKAY")
        lexeme_info.append("keyword")
        lexemeArr.append(lexeme_info)
        
        num_exact = len("MKAY")
        new = line[num_exact:len(line)]
        lines.remove(line)
        lines.insert(index, new.strip())

    elif(len(re.findall("^YR", line)) != 0):
        lexeme_info = []
        lexeme_info.append("YR")
        lexeme_info.append("keyword")
        lexemeArr.append(lexeme_info)
        
        num_exact = len("YR")
        new = line[num_exact:len(line)]
        lines.remove(line)
        lines.insert(index, new.strip())

    elif(len(re.findall("^TIL", line)) != 0):
        lexeme_info = []
        lexeme_info.append("TIL")
        lexeme_info.append("keyword")
        lexemeArr.append(lexeme_info)
        
        num_exact = len("TIL")
        new = line[num_exact:len(line)]
        lines.remove(line)
        lines.insert(index, new.strip())

    elif(len(re.findall("^WILE", line)) != 0):
        lexeme_info = []
        lexeme_info.append("WILE")
        lexeme_info.append("keyword")
        lexemeArr.append(lexeme_info)
        
        num_exact = len("WILE")
        new = line[num_exact:len(line)]
        lines.remove(line)
        lines.insert(index, new.strip())

    elif(len(re.findall("^IM OUTTA YR", line)) != 0):
        lexeme_info = []
        lexeme_info.append("IM OUTTA YR")
        lexeme_info.append("keyword")
        lexemeArr.append(lexeme_info)
        
        num_exact = len("IM OUTTA YR")
        new = line[num_exact:len(line)]
        lines.remove(line)
        lines.insert(index, new.strip())

    elif(len(re.findall("^AN", line)) != 0):
        lexeme_info = []
        lexeme_info.append("AN")
        lexeme_info.append("keyword")
        lexemeArr.append(lexeme_info)
        
        num_exact = len("AN")
        new = line[num_exact:len(line)]
        lines.remove(line)
        lines.insert(index, new.strip())

    elif(len(re.findall("^BTW", line)) != 0):
        lexeme_info = []
        lexeme_info.append("BTW")
        lexeme_info.append("keyword")
    
        comment = re.sub(".*BTW ", "", line)
        lexeme_info2 = [comment, "comment"]
    
        lexemeArr.append(lexeme_info)
        lexemeArr.append(lexeme_info2)
    
        new = re.sub("BTW.*", "", line)
        lines.remove(line)
        lines.insert(index, new.strip())
    
    elif(len(re.findall("^A", line)) != 0):
        lexeme_info = []
        lexeme_info.append("A")
        lexeme_info.append("keyword")
        lexemeArr.append(lexeme_info)
        
        num_exact = len("A")
        new = line[num_exact:len(line)]
        lines.remove(line)
        lines.insert(index, new.strip())

    elif(len(re.findall("^R", line)) != 0):
        lexeme_info = []
        lexeme_info.append("R")
        lexeme_info.append("keyword")
        lexemeArr.append(lexeme_info)
        
        num_exact = len("R")
        new = line[num_exact:len(line)]
        lines.remove(line)
        lines.insert(index, new.strip())


    elif(len(re.findall("^[A-Za-z]+[\w]*", line)) != 0):
        exact = re.findall("[A-Za-z]+[\w]*", line)[0]
        lexeme_info = []
        lexeme_info.append(exact)
        lexeme_info.append("Variable Identifier")
        lexemeArr.append(lexeme_info)
        
        num_exact = len(exact)
        new = line[num_exact:len(line)]
        lines.remove(line)
        lines.insert(index, new.strip())

    elif(len(re.findall("^-?[\d]+\.[\d]+", line)) != 0):
        exact = re.findall("-?[\d]+\.[\d]+", line)[0]
        lexeme_info = []
        lexeme_info.append(exact)
        lexeme_info.append("NUMBAR Literal")
        lexemeArr.append(lexeme_info)
        

        num_exact = len(exact)
        new = line[num_exact:len(line)]
        lines.remove(line)
        lines.insert(index, new.strip())



    elif(len(re.findall("^-?\d+", line)) != 0):
        exact = re.findall("-?\d+", line)[0]
        lexeme_info = []
        lexeme_info.append(exact)
        lexeme_info.append("NUMBR Literal")
        lexemeArr.append(lexeme_info)
        
        num_exact = len(exact)
        new = line[num_exact:len(line)]
        lines.remove(line)
        lines.insert(index, new.strip())


    else:
        lexeme_info = []
        lexeme_info.append(line)
        lexeme_info.append("invalid")

        lexemeArr.append(lexeme_info)

        lines.remove(line)
        lines.insert(index, "")
    
    
    

        



def lex_analyze(the_long_string):
    lexemeArr = [] #empty

    #split every line of the string to an array
    lines = the_long_string.split("\n")

    #new string array for removed trailing lines and tabs
    lines2 = []
    for line in lines:
        if(line != ""):
            lines2.append(line.strip())    


    for i in range(0, len(lines2)):
        while(lines2[i] != ''):
            get_lexemes(lexemeArr, lines2, lines2[i], i)
        
    # index = 0
    # for i in lines2:
    #     while(i != ''):
    #         get_lexemes(lexemeArr, lines2, i, index)
    #     index += 1
    
    # for i in lexemeArr:
    #     print(i)
    # print(lines2)

    







x = """BTW start of the program
O RLY?

HAI
    BTW variable dec
    I HAS A monde
    I HAS A num ITZ 17
    I HAS A name ITZ "seventeen"
    I HAS A fnum ITZ 17.0
    I HAS A flag ITZ WIN

    VISIBLE "declarations"
    VISIBLE MONDE BTW should be NOOB
    VISIBLE num
    VISIBLE name
    VISIBLE fnum
    VISIBLE flag

    I HAS A sum ITZ SUM OF num AN 13
    I HAS A diff ITZ DIFF OF sum AN 17
    I HAS A prod ITZ PRODUKT OF 3 AN 4
    I HAS A quo ITZ QUOSHUNT OF 4 AN 5

    VISIBLE sum
    VISIBLE diff
    VISIBLE prod
    VISIBLE quo
5.5
3.4
KTHXBYE"""

y = """HAI
    BTW variable dec
    I HAS A x
    I HAS A y
    
    GIMMEH x
    GIMMEH y

    VISIBLE x "+" y " = " SUM OF x AN y
    VISIBLE x "-" y " = " DIFF OF x AN y
    VISIBLE x "*" y " = " PRODUKT OF x AN y
    VISIBLE x "/" y " = " QUOSHUNT OF x AN y
    VISIBLE x "%" y " = " MOD OF x AN y

    VISIBLE "max(" x "," y ") = " BIGGR OF x AN y
    VISIBLE "min(" x "," y ") = " SMALLR OF x AN y
    
    BTW x^2 + y^2
    VISIBLE SUM OF PRODUKT OF x AN x AN PRODUKT OF y AN y
    BTW (x+y)^2
    VISIBLE PRODUKT OF SUM OF x AN y AN SUM OF x AN y
    BTW max(x,y) - min(x,y)
    VISIBLE DIFF OF BIGGR OF x AN y AN SMALLR OF x AN y

    BTW x + y/x + 0
    VISIBLE SUM OF x AN SUM OF QUOSHUNT OF y AN x AN FAIL

    VISIBLE SUM OF x AN SUM OF QUOSHUNT OF "17" AN x AN FAIL
KTHXBYE"""
# lex_analyze(y)