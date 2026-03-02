import re

#filename = "Project 3/Test Files/project-examples/01_variables.lol"

#reads file and cleans each line in the file
def readFile(listOfLines):
    #file = open(filename)
    lines = []

    #reads the file and places each line in a list
    #for line in file.readlines():
    for line in listOfLines:
        if(line != "\n"):
            if(line[len(line)-1] == "\n"):
                lines.append(line[0:len(line)-1])
            else:
                lines.append(line)
        else:
           lines.append("")

    #gets rid of leading whitespaces in each line
    for i in range(0, len(lines)):
        lines[i] = lines[i].strip()
        
    return lines

#finds lexemes in code and groups them 
def findLexemes(lines, lexemes, types):
    stringFound = False
    singleCommentFound = False
    multiCommentFound = False
    iHasAKeyword = ""
    sumOfKeyword = ""
    diffOfKeyword = ""
    produktOfKeyword = ""
    quoshuntOfKeyword = ""
    modOfKeyword = ""
    biggrOfKeyword = ""
    smallrOfKeyword = ""
    bothKeyword = ""
    eitherOfKeyword = ""
    wonOfKeyword = ""
    anyOfKeyword = ""
    allOfKeyword = ""
    isNowAKeyword = ""
    oRlyKeyword = ""
    yaRlyKeyword = ""
    noWaiKeyword = ""
    yrKeyword = ""
    imYrKeyword = ""
    string = ""
    singleComment = ""
    multiComment = ""

    for i in range(0, len(lines)):
        splitWords = lines[i].split()
        for j in range(0, len(splitWords)):
            #catches SINGLE COMMENTS and BTW
            if(splitWords[j] == "BTW"):
                if(i+1 not in lexemes):
                    lexemes[i+1] = []
                    lexemes[i+1].append(splitWords[j])
                else:
                    lexemes[i+1].append(splitWords[j])

                if(i+1 not in types):
                    types[i+1] = []
                    types[i+1].append("comment delimiter")
                else:
                    types[i+1].append("comment delimiter")

                singleCommentFound = True
                continue
            
            if(singleCommentFound == True):
                singleComment = singleComment + splitWords[j] + " "
                
                if(j == len(splitWords)-1):
                    singleCommentFound = False

                    if(singleComment != ""):
                        if(i+1 not in lexemes):
                            lexemes[i+1] = []
                            lexemes[i+1].append(singleComment.strip())
                        else:
                            lexemes[i+1].append(singleComment.strip())

                        if(i+1 not in types):
                            types[i+1] = []
                            types[i+1].append("comment")
                        else:
                            types[i+1].append("comment")
                    
                    singleComment = ""
                
                continue
            
            #catches MULTI COMMENTS, OBTW, and TLDR
            if(splitWords[j] == "OBTW"):
                if(i+1 not in lexemes):
                    lexemes[i+1] = []
                    lexemes[i+1].append(splitWords[j])
                else:
                    lexemes[i+1].append(splitWords[j])

                if(i+1 not in types):
                    types[i+1] = []
                    types[i+1].append("comment delimiter")
                else:
                    types[i+1].append("comment delimiter")

                multiCommentFound = True
                continue
            
            if(multiCommentFound == True):
                if (splitWords[j] == "TLDR"):
                    if(multiComment != ""):
                        if(i+1 not in lexemes):
                            lexemes[i+1] = []
                            lexemes[i+1].append(multiComment.strip())
                        else:
                            lexemes[i+1].append(multiComment.strip())

                        if(i+1 not in types):
                            types[i+1] = []
                            types[i+1].append("comment")
                        else:
                            types[i+1].append("comment")
                            
                    if(i+1 not in lexemes):
                        lexemes[i+1] = []
                        lexemes[i+1].append(splitWords[j])
                    else:
                        lexemes[i+1].append(splitWords[j])

                    if(i+1 not in types):
                        types[i+1] = []
                        types[i+1].append("comment delimiter")
                    else:
                        types[i+1].append("comment delimiter")

                    multiCommentFound = False
                    multiComment = ""
                    continue
                else:
                    multiComment = multiComment + splitWords[j] + " "

                if(j == len(splitWords)-1):
                    if(multiComment != ""):
                        if(i+1 not in lexemes):
                            lexemes[i+1] = []
                            lexemes[i+1].append(multiComment.strip())
                        else:
                            lexemes[i+1].append(multiComment.strip())

                        if(i+1 not in types):
                            types[i+1] = []
                            types[i+1].append("comment")
                        else:
                            types[i+1].append("comment")
                    
                    multiComment = ""

                    continue
                
                continue

            #catches YARN LITERAL and STRING DELIMITER
            if('\"' == splitWords[j][0] and len(splitWords[j]) > 1):
                if(splitWords[j][1] != "\""):
                    stringFound = True

            if(stringFound == True):
                string = string + splitWords[j] + " "

                if('\"' == splitWords[j][len(splitWords[j])-1]):
                    stringFound = False

                    if(string != ""):
                        if(i+1 not in lexemes):
                            lexemes[i+1] = []
                            lexemes[i+1].append("\"")
                            lexemes[i+1].append(string.strip()[1:len(string.strip())-1])
                            lexemes[i+1].append("\"")
                        else:
                            lexemes[i+1].append("\"")
                            lexemes[i+1].append(string.strip()[1:len(string.strip())-1])
                            lexemes[i+1].append("\"")

                        if(i+1 not in types):
                            types[i+1] = []
                            types[i+1].append("string delimiter")
                            types[i+1].append("YARN literal")
                            types[i+1].append("string delimiter")
                        else:
                            types[i+1].append("string delimiter")
                            types[i+1].append("YARN literal")
                            types[i+1].append("string delimiter")
                    
                    string = ""
                elif(j == len(splitWords)-1):
                    if('\"' != splitWords[j][len(splitWords[j])-1]):
                        return "SyntaxError: " + splitWords[j] + " is an invalid keyword"
                    elif('\"' != splitWords[j][len(splitWords[j])-1]):
                        stringFound = False

                        if(string != ""):
                            if(i+1 not in lexemes):
                                lexemes[i+1] = []
                                lexemes[i+1].append("\"")
                                lexemes[i+1].append(string.strip()[1:len(string.strip())-1])
                                lexemes[i+1].append("\"")
                            else:
                                lexemes[i+1].append("\"")
                                lexemes[i+1].append(string.strip()[1:len(string.strip())-1])
                                lexemes[i+1].append("\"")

                            if(i+1 not in types):
                                types[i+1] = []
                                types[i+1].append("string delimiter")
                                types[i+1].append("YARN literal")
                                types[i+1].append("string delimiter")
                            else:
                                types[i+1].append("string delimiter")
                                types[i+1].append("YARN literal")
                                types[i+1].append("string delimiter")
                        
                        string = ""

                continue

            #catches NUMBR LITERAL
            numbrLiteral = re.search("^[-]?\d+$", splitWords[j])
            if(numbrLiteral):
                if(i+1 not in lexemes):
                    lexemes[i+1] = []
                    lexemes[i+1].append(splitWords[j])
                else:
                    lexemes[i+1].append(splitWords[j])

                if(i+1 not in types):
                    types[i+1] = []
                    types[i+1].append("NUMBR literal")
                else:
                    types[i+1].append("NUMBR literal")

                continue
            
            #catches NUMBAR LITERAL
            numbarLiteral = re.search("^[-]?\d+[.]\d+$", splitWords[j])
            if(numbarLiteral):
                if(i+1 not in lexemes):
                    lexemes[i+1] = []
                    lexemes[i+1].append(splitWords[j])
                else:
                    lexemes[i+1].append(splitWords[j])
                
                if(i+1 not in types):
                    types[i+1] = []
                    types[i+1].append("NUMBAR literal")
                else:
                    types[i+1].append("NUMBAR literal")

                continue
            
            #catches TROOF LITERAL
            troofLiteralWin = re.search("^(WIN)$", splitWords[j])
            if(troofLiteralWin):
                if(i+1 not in lexemes):
                    lexemes[i+1] = []
                    lexemes[i+1].append(splitWords[j])
                else:
                    lexemes[i+1].append(splitWords[j])
                
                if(i+1 not in types):
                    types[i+1] = []
                    types[i+1].append("TROOF literal")
                else:
                    types[i+1].append("TROOF literal")
                
                continue

            troofLiteralFail = re.search("^(FAIL)$", splitWords[j])
            if(troofLiteralFail):
                if(i+1 not in lexemes):
                    lexemes[i+1] = []
                    lexemes[i+1].append(splitWords[j])
                else:
                    lexemes[i+1].append(splitWords[j])

                if(i+1 not in types):
                    types[i+1] = []
                    types[i+1].append("TROOF literal")
                else:
                    types[i+1].append("TROOF literal")

                continue
            
            #catches TYPE LITERAL
            typeLiteralTroof = re.search("^(TROOF)$", splitWords[j])
            if(typeLiteralTroof):
                if(i+1 not in lexemes):
                    lexemes[i+1] = []
                    lexemes[i+1].append(splitWords[j])
                else:
                    lexemes[i+1].append(splitWords[j])
                
                if(i+1 not in types):
                    types[i+1] = []
                    types[i+1].append("TYPE literal")
                else:
                    types[i+1].append("TYPE literal")

                continue
            
            typeLiteralNoob = re.search("^(NOOB)$", splitWords[j])
            if(typeLiteralNoob):
                if(i+1 not in lexemes):
                    lexemes[i+1] = []
                    lexemes[i+1].append(splitWords[j])
                else:
                    lexemes[i+1].append(splitWords[j])
                
                if(i+1 not in types):
                    types[i+1] = []
                    types[i+1].append("TYPE literal")
                else:
                    types[i+1].append("TYPE literal")

                continue

            typeLiteralNumbr = re.search("^(NUMBR)$", splitWords[j])
            if(typeLiteralNumbr):
                if(i+1 not in lexemes):
                    lexemes[i+1] = []
                    lexemes[i+1].append(splitWords[j])
                else:
                    lexemes[i+1].append(splitWords[j])

                if(i+1 not in types):
                    types[i+1] = []
                    types[i+1].append("TYPE literal")
                else:
                    types[i+1].append("TYPE literal")

                continue

            typeLiteralNumbar = re.search("^(NUMBAR)$", splitWords[j])
            if(typeLiteralNumbar):
                if(i+1 not in lexemes):
                    lexemes[i+1] = []
                    lexemes[i+1].append(splitWords[j])
                else:
                    lexemes[i+1].append(splitWords[j])

                if(i+1 not in types):
                    types[i+1] = []
                    types[i+1].append("TYPE literal")
                else:
                    types[i+1].append("TYPE literal")

                continue

            typeLiteralYarn = re.search("^(YARN)$", splitWords[j])
            if(typeLiteralYarn):
                if(i+1 not in lexemes):
                    lexemes[i+1] = []
                    lexemes[i+1].append(splitWords[j])
                else:
                    lexemes[i+1].append(splitWords[j])
                
                if(i+1 not in types):
                    types[i+1] = []
                    types[i+1].append("TYPE literal")
                else:
                    types[i+1].append("TYPE literal")

                continue

            typeLiteralType = re.search("^(TYPE)$", splitWords[j])
            if(typeLiteralType):
                if(i+1 not in lexemes):
                    lexemes[i+1] = []
                    lexemes[i+1].append(splitWords[j])
                else:
                    lexemes[i+1].append(splitWords[j])

                if(i+1 not in types):
                    types[i+1] = []
                    types[i+1].append("TYPE literal")
                else:
                    types[i+1].append("TYPE literal")

                continue
            
            #catches HAI
            haiKeyword = re.search("^(HAI)$", splitWords[j])
            if (haiKeyword):
                if(i+1 not in lexemes):
                    lexemes[i+1] = []
                    lexemes[i+1].append(splitWords[j])
                else:
                    lexemes[i+1].append(splitWords[j])
                
                if(i+1 not in types):
                    types[i+1] = []
                    types[i+1].append("code delimiter")
                else:
                    types[i+1].append("code delimiter")

                continue
            
            #catches KTHXBYE
            kThxByeKeyword = re.search("^(KTHXBYE)$", splitWords[j])
            if (kThxByeKeyword):
                if(i+1 not in lexemes):
                    lexemes[i+1] = []
                    lexemes[i+1].append(splitWords[j])
                else:
                    lexemes[i+1].append(splitWords[j])
                
                if(i+1 not in types):
                    types[i+1] = []
                    types[i+1].append("code delimiter")
                else:
                    types[i+1].append("code delimiter")
                    
                continue
            
            #catches I HAS A
            if (splitWords[j] == "I"):
                iHasAKeyword = iHasAKeyword + splitWords[j] + " "
                continue

            if (iHasAKeyword == "I "):
                if (splitWords[j] == "HAS"):
                    iHasAKeyword = iHasAKeyword + splitWords[j] + " "
                    continue
                else: #case where I is alone (identifier)
                    if(i+1 not in lexemes):
                        lexemes[i+1] = []
                        lexemes[i+1].append("I")
                    else:
                        lexemes[i+1].append("I")

                    if(i+1 not in types):
                        types[i+1] = []
                        types[i+1].append("identifier")
                    else:
                        types[i+1].append("identifier")

                    iHasAKeyword = ""

            if(iHasAKeyword == "I HAS "):
                if (splitWords[j] == "A"):
                    iHasAKeyword = iHasAKeyword + splitWords[j]
                    
                    if(iHasAKeyword == "I HAS A"):
                        if(i+1 not in lexemes):
                            lexemes[i+1] = []
                            lexemes[i+1].append(iHasAKeyword)
                        else:
                            lexemes[i+1].append(iHasAKeyword)
                        
                        if(i+1 not in types):
                            types[i+1] = []
                            types[i+1].append("variable declaration keyword")
                        else:
                            types[i+1].append("variable declaration keyword")
                        
                        iHasAKeyword = ""
                        continue
                else: #case where it's only I HAS (invalid)
                    return "SyntaxError: I HAS is an invalid keyword"
            
            #catches ITZ
            itzKeyword = re.search("^(ITZ)$", splitWords[j])
            if (itzKeyword):
                if(i+1 not in lexemes):
                    lexemes[i+1] = []
                    lexemes[i+1].append(splitWords[j])
                else:
                    lexemes[i+1].append(splitWords[j])
                
                if(i+1 not in types):
                    types[i+1] = []
                    types[i+1].append("variable initialization keyword")
                else:
                    types[i+1].append("variable initialization keyword")

                continue
            
            #catches R
            rKeyword = re.search("^(R)$", splitWords[j])
            if (rKeyword):
                if(i+1 not in lexemes):
                    lexemes[i+1] = []
                    lexemes[i+1].append(splitWords[j])
                else:
                    lexemes[i+1].append(splitWords[j])
                
                if(i+1 not in types):
                    types[i+1] = []
                    types[i+1].append("assignment operator")
                else:
                    types[i+1].append("assignment operator")

                continue
            
            #catches SUM OF
            if (splitWords[j] == "SUM"):
                sumOfKeyword = sumOfKeyword + splitWords[j] + " "
                continue

            if (sumOfKeyword == "SUM "):
                if (splitWords[j] == "OF"):
                    sumOfKeyword = sumOfKeyword + splitWords[j]

                    if(sumOfKeyword == "SUM OF"):
                        if(i+1 not in lexemes):
                            lexemes[i+1] = []
                            lexemes[i+1].append(sumOfKeyword)
                        else:
                            lexemes[i+1].append(sumOfKeyword)
                        
                        if(i+1 not in types):
                            types[i+1] = []
                            types[i+1].append("add operator")
                        else:
                            types[i+1].append("add operator")
                        
                        sumOfKeyword = ""
                        continue
                else: #only SUM (identifier)
                    if(i+1 not in lexemes):
                        lexemes[i+1] = []
                        lexemes[i+1].append("SUM")
                    else:
                        lexemes[i+1].append("SUM")

                    if(i+1 not in types):
                        types[i+1] = []
                        types[i+1].append("identifier")
                    else:
                        types[i+1].append("identifier")

                    sumOfKeyword = ""
            
            #catches DIFF OF
            if (splitWords[j] == "DIFF"):
                diffOfKeyword = diffOfKeyword + splitWords[j] + " "
                continue

            if (diffOfKeyword == "DIFF "):
                if (splitWords[j] == "OF"):
                    diffOfKeyword = diffOfKeyword + splitWords[j]

                    if(diffOfKeyword == "DIFF OF"):
                        if(i+1 not in lexemes):
                            lexemes[i+1] = []
                            lexemes[i+1].append(diffOfKeyword)
                        else:
                            lexemes[i+1].append(diffOfKeyword)
                        
                        if(i+1 not in types):
                            types[i+1] = []
                            types[i+1].append("subtract operator")
                        else:
                            types[i+1].append("subtract operator")
                        
                        diffOfKeyword = ""
                        continue
                else: #only DIFF (identifier)
                    if(i+1 not in lexemes):
                        lexemes[i+1] = []
                        lexemes[i+1].append("DIFF")
                    else:
                        lexemes[i+1].append("DIFF")

                    if(i+1 not in types):
                        types[i+1] = []
                        types[i+1].append("identifier")
                    else:
                        types[i+1].append("identifier")

                    diffOfKeyword = ""
            
            #catches PRODUKT OF
            if (splitWords[j] == "PRODUKT"):
                produktOfKeyword = produktOfKeyword + splitWords[j] + " "
                continue

            if (produktOfKeyword == "PRODUKT "):
                if (splitWords[j] == "OF"):
                    produktOfKeyword = produktOfKeyword + splitWords[j]

                    if(produktOfKeyword == "PRODUKT OF"):
                        if(i+1 not in lexemes):
                            lexemes[i+1] = []
                            lexemes[i+1].append(produktOfKeyword)
                        else:
                            lexemes[i+1].append(produktOfKeyword)
                        
                        if(i+1 not in types):
                            types[i+1] = []
                            types[i+1].append("multiply operator")
                        else:
                            types[i+1].append("multiply operator")
                        
                        produktOfKeyword = ""
                        continue
                else: #only PRODUKT (identifier)
                    if(i+1 not in lexemes):
                        lexemes[i+1] = []
                        lexemes[i+1].append("PRODUKT")
                    else:
                        lexemes[i+1].append("PRODUKT")

                    if(i+1 not in types):
                        types[i+1] = []
                        types[i+1].append("identifier")
                    else:
                        types[i+1].append("identifier")

                    produktOfKeyword = ""

            #catches QUOSHUNT OF
            if (splitWords[j] == "QUOSHUNT"):
                quoshuntOfKeyword = quoshuntOfKeyword + splitWords[j] + " "
                continue

            if (quoshuntOfKeyword == "QUOSHUNT "):
                if (splitWords[j] == "OF"):
                    quoshuntOfKeyword = quoshuntOfKeyword + splitWords[j]

                    if(quoshuntOfKeyword == "QUOSHUNT OF"):
                        if(i+1 not in lexemes):
                            lexemes[i+1] = []
                            lexemes[i+1].append(quoshuntOfKeyword)
                        else:
                            lexemes[i+1].append(quoshuntOfKeyword)
                        
                        if(i+1 not in types):
                            types[i+1] = []
                            types[i+1].append("divide operator")
                        else:
                            types[i+1].append("divide operator")
                        
                        quoshuntOfKeyword = ""
                        continue
                else: #only QUOSHUNT (identifier)
                    if(i+1 not in lexemes):
                        lexemes[i+1] = []
                        lexemes[i+1].append("QUOSHUNT")
                    else:
                        lexemes[i+1].append("QUOSHUNT")

                    if(i+1 not in types):
                        types[i+1] = []
                        types[i+1].append("identifier")
                    else:
                        types[i+1].append("identifier")

                    quoshuntOfKeyword = ""
            
            #catches MOD OF
            if (splitWords[j] == "MOD"):
                modOfKeyword = modOfKeyword + splitWords[j] + " "
                continue

            if (modOfKeyword == "MOD "):
                if (splitWords[j] == "OF"):
                    modOfKeyword = modOfKeyword + splitWords[j]

                    if(modOfKeyword == "MOD OF"):
                        if(i+1 not in lexemes):
                            lexemes[i+1] = []
                            lexemes[i+1].append(modOfKeyword)
                        else:
                            lexemes[i+1].append(modOfKeyword)
                        
                        if(i+1 not in types):
                            types[i+1] = []
                            types[i+1].append("modulo operator")
                        else:
                            types[i+1].append("modulo operator")
                        
                        modOfKeyword = ""
                        continue
                else: #only MOD (identifier)
                    if(i+1 not in lexemes):
                        lexemes[i+1] = []
                        lexemes[i+1].append("MOD")
                    else:
                        lexemes[i+1].append("MOD")

                    if(i+1 not in types):
                        types[i+1] = []
                        types[i+1].append("identifier")
                    else:
                        types[i+1].append("identifier")

                    modOfKeyword = ""
            
            #catches BIGGR OF
            if (splitWords[j] == "BIGGR"):
                biggrOfKeyword = biggrOfKeyword + splitWords[j] + " "
                continue

            if (biggrOfKeyword == "BIGGR "):
                if (splitWords[j] == "OF"):
                    biggrOfKeyword = biggrOfKeyword + splitWords[j]

                    if(biggrOfKeyword == "BIGGR OF"):
                        if(i+1 not in lexemes):
                            lexemes[i+1] = []
                            lexemes[i+1].append(biggrOfKeyword)
                        else:
                            lexemes[i+1].append(biggrOfKeyword)
                        
                        if(i+1 not in types):
                            types[i+1] = []
                            types[i+1].append("max operator")
                        else:
                            types[i+1].append("max operator")
                        
                        biggrOfKeyword = ""
                        continue
                else: #only BIGGR (identifier)
                    if(i+1 not in lexemes):
                        lexemes[i+1] = []
                        lexemes[i+1].append("BIGGR")
                    else:
                        lexemes[i+1].append("BIGGR")

                    if(i+1 not in types):
                        types[i+1] = []
                        types[i+1].append("identifier")
                    else:
                        types[i+1].append("identifier")

                    biggrOfKeyword = ""
            
            #catches SMALLR OF
            if (splitWords[j] == "SMALLR"):
                smallrOfKeyword = smallrOfKeyword + splitWords[j] + " "
                continue

            if (smallrOfKeyword == "SMALLR "):
                if (splitWords[j] == "OF"):
                    smallrOfKeyword = smallrOfKeyword + splitWords[j]

                    if(smallrOfKeyword == "SMALLR OF"):
                        if(i+1 not in lexemes):
                            lexemes[i+1] = []
                            lexemes[i+1].append(smallrOfKeyword)
                        else:
                            lexemes[i+1].append(smallrOfKeyword)
                        
                        if(i+1 not in types):
                            types[i+1] = []
                            types[i+1].append("min operator")
                        else:
                            types[i+1].append("min operator")
                        
                        smallrOfKeyword = ""
                        continue
                else: #only SMALLR (identifier)
                    if(i+1 not in lexemes):
                        lexemes[i+1] = []
                        lexemes[i+1].append("SMALLR")
                    else:
                        lexemes[i+1].append("SMALLR")

                    if(i+1 not in types):
                        types[i+1] = []
                        types[i+1].append("identifier")
                    else:
                        types[i+1].append("identifier")

                    smallrOfKeyword = ""
            
            #catches BOTH OF or BOTH SAEM
            if (splitWords[j] == "BOTH"):
                bothKeyword = bothKeyword + splitWords[j] + " "
                continue

            if (bothKeyword == "BOTH "):
                if (splitWords[j] == "OF"):
                    bothKeyword = bothKeyword + splitWords[j]

                    if(bothKeyword == "BOTH OF"):
                        if(i+1 not in lexemes):
                            lexemes[i+1] = []
                            lexemes[i+1].append(bothKeyword)
                        else:
                            lexemes[i+1].append(bothKeyword)
                        
                        if(i+1 not in types):
                            types[i+1] = []
                            types[i+1].append("and operator")
                        else:
                            types[i+1].append("and operator")
                        
                        bothKeyword = ""
                        continue
                elif (splitWords[j] == "SAEM"):
                    bothKeyword = bothKeyword + splitWords[j]

                    if(bothKeyword == "BOTH SAEM"):
                        if(i+1 not in lexemes):
                            lexemes[i+1] = []
                            lexemes[i+1].append(bothKeyword)
                        else:
                            lexemes[i+1].append(bothKeyword)
                        
                        if(i+1 not in types):
                            types[i+1] = []
                            types[i+1].append("is equal comparison operator")
                        else:
                            types[i+1].append("is equal comparison operator")
                        
                        bothKeyword = ""
                        continue
                else: #only BOTH (identifier)
                    if(i+1 not in lexemes):
                        lexemes[i+1] = []
                        lexemes[i+1].append("BOTH")
                    else:
                        lexemes[i+1].append("BOTH")

                    if(i+1 not in types):
                        types[i+1] = []
                        types[i+1].append("identifier")
                    else:
                        types[i+1].append("identifier")

                    bothKeyword = ""

            #catches EITHER OF
            if (splitWords[j] == "EITHER"):
                eitherOfKeyword = eitherOfKeyword + splitWords[j] + " "
                continue

            if (eitherOfKeyword == "EITHER "):
                if (splitWords[j] == "OF"):
                    eitherOfKeyword = eitherOfKeyword + splitWords[j]

                    if(eitherOfKeyword == "EITHER OF"):
                        if(i+1 not in lexemes):
                            lexemes[i+1] = []
                            lexemes[i+1].append(eitherOfKeyword)
                        else:
                            lexemes[i+1].append(eitherOfKeyword)
                        
                        if(i+1 not in types):
                            types[i+1] = []
                            types[i+1].append("or operator")
                        else:
                            types[i+1].append("or operator")
                        
                        eitherOfKeyword = ""
                        continue
                else: #only EITHER (identifier)
                    if(i+1 not in lexemes):
                        lexemes[i+1] = []
                        lexemes[i+1].append("EITHER")
                    else:
                        lexemes[i+1].append("EITHER")

                    if(i+1 not in types):
                        types[i+1] = []
                        types[i+1].append("identifier")
                    else:
                        types[i+1].append("identifier")

                    eitherOfKeyword = ""
            
            #catches WON OF
            if (splitWords[j] == "WON"):
                wonOfKeyword = wonOfKeyword + splitWords[j] + " "
                continue

            if (wonOfKeyword == "WON "):
                if (splitWords[j] == "OF"):
                    wonOfKeyword = wonOfKeyword + splitWords[j]

                    if(wonOfKeyword == "WON OF"):
                        if(i+1 not in lexemes):
                            lexemes[i+1] = []
                            lexemes[i+1].append(wonOfKeyword)
                        else:
                            lexemes[i+1].append(wonOfKeyword)
                        
                        if(i+1 not in types):
                            types[i+1] = []
                            types[i+1].append("xor operator")
                        else:
                            types[i+1].append("xor operator")
                        
                        wonOfKeyword = ""
                        continue
                else: #only WON (identifier)
                    if(i+1 not in lexemes):
                        lexemes[i+1] = []
                        lexemes[i+1].append("WON")
                    else:
                        lexemes[i+1].append("WON")

                    if(i+1 not in types):
                        types[i+1] = []
                        types[i+1].append("identifier")
                    else:
                        types[i+1].append("identifier")

                    wonOfKeyword = ""

            #catches NOT
            notKeyword = re.findall("^(NOT)$", splitWords[j])
            if (notKeyword):
                if(i+1 not in lexemes):
                    lexemes[i+1] = []
                    lexemes[i+1].append(splitWords[j])
                else:
                    lexemes[i+1].append(splitWords[j])
                
                if(i+1 not in types):
                    types[i+1] = []
                    types[i+1].append("not operator")
                else:
                    types[i+1].append("not operator")

                continue
            
            #catches ANY OF
            if (splitWords[j] == "ANY"):
                anyOfKeyword = anyOfKeyword + splitWords[j] + " "
                continue

            if (anyOfKeyword == "ANY "):
                if (splitWords[j] == "OF"):
                    anyOfKeyword = anyOfKeyword + splitWords[j]

                    if(anyOfKeyword == "ANY OF"):
                        if(i+1 not in lexemes):
                            lexemes[i+1] = []
                            lexemes[i+1].append(anyOfKeyword)
                        else:
                            lexemes[i+1].append(anyOfKeyword)
                        
                        if(i+1 not in types):
                            types[i+1] = []
                            types[i+1].append("infinite arity OR operator")
                        else:
                            types[i+1].append("infinite arity OR operator")
                        
                        anyOfKeyword = ""
                        continue
                else: #only ANY (identifier)
                    if(i+1 not in lexemes):
                        lexemes[i+1] = []
                        lexemes[i+1].append("ANY")
                    else:
                        lexemes[i+1].append("ANY")

                    if(i+1 not in types):
                        types[i+1] = []
                        types[i+1].append("identifier")
                    else:
                        types[i+1].append("identifier")

                    anyOfKeyword = ""

            #catches ALL OF
            if (splitWords[j] == "ALL"):
                allOfKeyword = allOfKeyword + splitWords[j] + " "
                continue

            if (allOfKeyword == "ALL "):
                if (splitWords[j] == "OF"):
                    allOfKeyword = allOfKeyword + splitWords[j]

                    if(allOfKeyword == "ALL OF"):
                        if(i+1 not in lexemes):
                            lexemes[i+1] = []
                            lexemes[i+1].append(allOfKeyword)
                        else:
                            lexemes[i+1].append(allOfKeyword)
                        
                        if(i+1 not in types):
                            types[i+1] = []
                            types[i+1].append("infinite arity AND operator")
                        else:
                            types[i+1].append("infinite arity AND operator")
                        
                        allOfKeyword = ""
                        continue
                else: #only ALL (identifier)
                    if(i+1 not in lexemes):
                        lexemes[i+1] = []
                        lexemes[i+1].append("ALL")
                    else:
                        lexemes[i+1].append("ALL")

                    if(i+1 not in types):
                        types[i+1] = []
                        types[i+1].append("identifier")
                    else:
                        types[i+1].append("identifier")

                    allOfKeyword = ""
            
            #catches DIFFRINT
            diffrintKeyword = re.search("^(DIFFRINT)$", splitWords[j])
            if(diffrintKeyword):
                if(i+1 not in lexemes):
                    lexemes[i+1] = []
                    lexemes[i+1].append(splitWords[j])
                else:
                    lexemes[i+1].append(splitWords[j])
            
                if(i+1 not in types):
                    types[i+1] = []
                    types[i+1].append("not equal comparison operator")
                else:
                    types[i+1].append("not equal comparison operator")

                continue

            #catches SMOOSH
            smooshKeyword = re.search("^(SMOOSH)$", splitWords[j])
            if(smooshKeyword):
                if(i+1 not in lexemes):
                    lexemes[i+1] = []
                    lexemes[i+1].append(splitWords[j])
                else:
                    lexemes[i+1].append(splitWords[j])
            
                if(i+1 not in types):
                    types[i+1] = []
                    types[i+1].append("concatenation keyword")
                else:
                    types[i+1].append("concatenation keyword")

                continue
            
            #catches MAEK
            maekKeyword = re.search("^(MAEK)$", splitWords[j])
            if(maekKeyword):
                if(i+1 not in lexemes):
                    lexemes[i+1] = []
                    lexemes[i+1].append(splitWords[j])
                else:
                    lexemes[i+1].append(splitWords[j])
            
                if(i+1 not in types):
                    types[i+1] = []
                    types[i+1].append("typecasting keyword")
                else:
                    types[i+1].append("typecasting keyword")

                continue
            
            #catches A
            aKeyword = re.search("^(A)$", splitWords[j])
            if(aKeyword and isNowAKeyword == "" and iHasAKeyword == ""):
                if(i+1 not in lexemes):
                    lexemes[i+1] = []
                    lexemes[i+1].append(splitWords[j])
                else:
                    lexemes[i+1].append(splitWords[j])
            
                if(i+1 not in types):
                    types[i+1] = []
                    types[i+1].append("typecasting delimiter")
                else:
                    types[i+1].append("typecasting delimiter")

                continue

            #catches IS NOW A
            if (splitWords[j] == "IS"):
                isNowAKeyword = isNowAKeyword + splitWords[j] + " "
                continue

            if (isNowAKeyword == "IS "):
                if (splitWords[j] == "NOW"):
                    isNowAKeyword = isNowAKeyword + splitWords[j] + " "
                    continue
                else: #case where IS is alone (identifier)
                    if(i+1 not in lexemes):
                        lexemes[i+1] = []
                        lexemes[i+1].append("IS")
                    else:
                        lexemes[i+1].append("IS")

                    if(i+1 not in types):
                        types[i+1] = []
                        types[i+1].append("identifier")
                    else:
                        types[i+1].append("identifier")

                    isNowAKeyword = ""

            if(isNowAKeyword == "IS NOW "):
                if (splitWords[j] == "A"):
                    isNowAKeyword = isNowAKeyword + splitWords[j]
                    
                    if(isNowAKeyword == "IS NOW A"):
                        if(i+1 not in lexemes):
                            lexemes[i+1] = []
                            lexemes[i+1].append(isNowAKeyword)
                        else:
                            lexemes[i+1].append(isNowAKeyword)
                        
                        if(i+1 not in types):
                            types[i+1] = []
                            types[i+1].append("typecasting keyword")
                        else:
                            types[i+1].append("typecasting keyword")
                        
                        isNowAKeyword = ""
                        continue
                else: #case where it's only IS NOW (invalid)
                    return "SyntaxError: IS NOW is an invalid keyword"

            #catches VISIBLE
            visibleKeyword = re.search("^(VISIBLE)$", splitWords[j])
            if(visibleKeyword):
                if(i+1 not in lexemes):
                    lexemes[i+1] = []
                    lexemes[i+1].append(splitWords[j])
                else:
                    lexemes[i+1].append(splitWords[j])
            
                if(i+1 not in types):
                    types[i+1] = []
                    types[i+1].append("print keyword")
                else:
                    types[i+1].append("print keyword")

                continue

            #catches GIMMEH
            gimmehKeyword = re.search("^(GIMMEH)$", splitWords[j])
            if(gimmehKeyword):
                if(i+1 not in lexemes):
                    lexemes[i+1] = []
                    lexemes[i+1].append(splitWords[j])
                else:
                    lexemes[i+1].append(splitWords[j])
            
                if(i+1 not in types):
                    types[i+1] = []
                    types[i+1].append("input keyword")
                else:
                    types[i+1].append("input keyword")

                continue

            #catches O RLY?
            if (splitWords[j] == "O"):
                oRlyKeyword = oRlyKeyword + splitWords[j] + " "
                continue

            if (oRlyKeyword == "O "):
                if (splitWords[j] == "RLY?"):
                    oRlyKeyword = oRlyKeyword + splitWords[j]

                    if(oRlyKeyword == "O RLY?"):
                        if(i+1 not in lexemes):
                            lexemes[i+1] = []
                            lexemes[i+1].append(oRlyKeyword)
                        else:
                            lexemes[i+1].append(oRlyKeyword)
                        
                        if(i+1 not in types):
                            types[i+1] = []
                            types[i+1].append("if delimiter")
                        else:
                            types[i+1].append("if delimiter")
                        
                        oRlyKeyword = ""
                        continue
                else: #only O (identifier)
                    if(i+1 not in lexemes):
                        lexemes[i+1] = []
                        lexemes[i+1].append("O")
                    else:
                        lexemes[i+1].append("O")

                    if(i+1 not in types):
                        types[i+1] = []
                        types[i+1].append("identifier")
                    else:
                        types[i+1].append("identifier")

                    oRlyKeyword = ""

            #catches YA RLY
            if (splitWords[j] == "YA"):
                yaRlyKeyword = yaRlyKeyword + splitWords[j] + " "
                continue

            if (yaRlyKeyword == "YA "):
                if (splitWords[j] == "RLY"):
                    yaRlyKeyword = yaRlyKeyword + splitWords[j]

                    if(yaRlyKeyword == "YA RLY"):
                        if(i+1 not in lexemes):
                            lexemes[i+1] = []
                            lexemes[i+1].append(yaRlyKeyword)
                        else:
                            lexemes[i+1].append(yaRlyKeyword)
                        
                        if(i+1 not in types):
                            types[i+1] = []
                            types[i+1].append("if keyword")
                        else:
                            types[i+1].append("if keyword")
                        
                        yaRlyKeyword = ""
                        continue
                else: #only YA (identifier)
                    if(i+1 not in lexemes):
                        lexemes[i+1] = []
                        lexemes[i+1].append("YA")
                    else:
                        lexemes[i+1].append("YA")

                    if(i+1 not in types):
                        types[i+1] = []
                        types[i+1].append("identifier")
                    else:
                        types[i+1].append("identifier")

                    yaRlyKeyword = ""

            #catches MEBBE
            mebbeKeyword = re.search("^(MEBBE)$", splitWords[j])
            if(mebbeKeyword):
                if(i+1 not in lexemes):
                    lexemes[i+1] = []
                    lexemes[i+1].append(splitWords[j])
                else:
                    lexemes[i+1].append(splitWords[j])
            
                if(i+1 not in types):
                    types[i+1] = []
                    types[i+1].append("else if keyword")
                else:
                    types[i+1].append("else if keyword")

                continue

            #catches NO WAI
            if (splitWords[j] == "NO"):
                noWaiKeyword = noWaiKeyword + splitWords[j] + " "
                continue

            if (noWaiKeyword == "NO "):
                if (splitWords[j] == "WAI"):
                    noWaiKeyword = noWaiKeyword + splitWords[j]

                    if(noWaiKeyword == "NO WAI"):
                        if(i+1 not in lexemes):
                            lexemes[i+1] = []
                            lexemes[i+1].append(noWaiKeyword)
                        else:
                            lexemes[i+1].append(noWaiKeyword)
                        
                        if(i+1 not in types):
                            types[i+1] = []
                            types[i+1].append("else keyword")
                        else:
                            types[i+1].append("else keyword")
                        
                        noWaiKeyword = ""
                        continue
                else: #only NO (identifier)
                    if(i+1 not in lexemes):
                        lexemes[i+1] = []
                        lexemes[i+1].append("NO")
                    else:
                        lexemes[i+1].append("NO")

                    if(i+1 not in types):
                        types[i+1] = []
                        types[i+1].append("identifier")
                    else:
                        types[i+1].append("identifier")

                    noWaiKeyword = ""
            
            #catches OIC
            oicKeyword = re.search("^(OIC)$", splitWords[j])
            if(oicKeyword):
                if(i+1 not in lexemes):
                    lexemes[i+1] = []
                    lexemes[i+1].append(splitWords[j])
                else:
                    lexemes[i+1].append(splitWords[j])
            
                if(i+1 not in types):
                    types[i+1] = []
                    types[i+1].append("if/switch case delimiter")
                else:
                    types[i+1].append("if/switch case delimiter")

                continue

            #catches WTF?
            wtfKeyword = re.search("^(WTF\?)$", splitWords[j])
            if(wtfKeyword):
                if(i+1 not in lexemes):
                    lexemes[i+1] = []
                    lexemes[i+1].append(splitWords[j])
                else:
                    lexemes[i+1].append(splitWords[j])
            
                if(i+1 not in types):
                    types[i+1] = []
                    types[i+1].append("switch case delimiter")
                else:
                    types[i+1].append("switch case delimiter")

                continue
            
            #catches OMG
            omgKeyword = re.search("^(OMG)$", splitWords[j])
            if(omgKeyword):
                if(i+1 not in lexemes):
                    lexemes[i+1] = []
                    lexemes[i+1].append(splitWords[j])
                else:
                    lexemes[i+1].append(splitWords[j])
            
                if(i+1 not in types):
                    types[i+1] = []
                    types[i+1].append("case keyword")
                else:
                    types[i+1].append("case keyword")

                continue

            #catches OMGWTF
            omgwtfKeyword = re.search("^(OMGWTF)$", splitWords[j])
            if(omgwtfKeyword):
                if(i+1 not in lexemes):
                    lexemes[i+1] = []
                    lexemes[i+1].append(splitWords[j])
                else:
                    lexemes[i+1].append(splitWords[j])
            
                if(i+1 not in types):
                    types[i+1] = []
                    types[i+1].append("default case keyword")
                else:
                    types[i+1].append("default case keyword")

                continue

            #catches IM IN YR or IM OUTTA YR
            if(splitWords[j] == "IM"):
                imYrKeyword = imYrKeyword + splitWords[j] + " "
                continue

            if(imYrKeyword == "IM "):
                if(splitWords[j] == "IN" or splitWords[j] == "OUTTA"):
                    imYrKeyword = imYrKeyword + splitWords[j] + " "
                    continue
                else: #case where IM is alone (identifier)
                    if(i+1 not in lexemes):
                        lexemes[i+1] = []
                        lexemes[i+1].append("IM")
                    else:
                        lexemes[i+1].append("IM")

                    if(i+1 not in types):
                        types[i+1] = []
                        types[i+1].append("identifier")
                    else:
                        types[i+1].append("identifier")

                    imYrKeyword = ""
               
            if(imYrKeyword == "IM IN "):
                if(splitWords[j] == "YR"):
                    imYrKeyword = imYrKeyword + splitWords[j]

                    if(imYrKeyword == "IM IN YR"):
                        if(i+1 not in lexemes):
                            lexemes[i+1] = []
                            lexemes[i+1].append(imYrKeyword)
                        else:
                            lexemes[i+1].append(imYrKeyword)
                    
                        if(i+1 not in types):
                            types[i+1] = []
                            types[i+1].append("loop delimiter")
                        else:
                            types[i+1].append("loop delimiter")
                        
                        imYrKeyword = ""
                        continue
                else: #case where it's only IM IN (invalid)
                    return "SyntaxError: IM IN is an invalid keyword"
            elif(imYrKeyword == "IM OUTTA "):
                if(splitWords[j] == "YR"):
                    imYrKeyword = imYrKeyword + splitWords[j]

                    if(imYrKeyword == "IM OUTTA YR"):
                        if(i+1 not in lexemes):
                            lexemes[i+1] = []
                            lexemes[i+1].append(imYrKeyword)
                        else:
                            lexemes[i+1].append(imYrKeyword)
                    
                        if(i+1 not in types):
                            types[i+1] = []
                            types[i+1].append("loop delimiter")
                        else:
                            types[i+1].append("loop delimiter")
                        
                        imYrKeyword = ""
                        continue
                else: #case where it's only IM OUTTA (invalid)
                    return "SyntaxError: IM OUTTA is an invalid keyword"

            #catches UPPIN
            uppinKeyword = re.search("^(UPPIN)$", splitWords[j])
            if(uppinKeyword):
                if(i+1 not in lexemes):
                    lexemes[i+1] = []
                    lexemes[i+1].append(splitWords[j])
                else:
                    lexemes[i+1].append(splitWords[j])
            
                if(i+1 not in types):
                    types[i+1] = []
                    types[i+1].append("increment operator")
                else:
                    types[i+1].append("increment operator")

                continue

            #catches NERFIN
            nerfinKeyword = re.search("^(NERFIN)$", splitWords[j])
            if(nerfinKeyword):
                if(i+1 not in lexemes):
                    lexemes[i+1] = []
                    lexemes[i+1].append(splitWords[j])
                else:
                    lexemes[i+1].append(splitWords[j])
            
                if(i+1 not in types):
                    types[i+1] = []
                    types[i+1].append("decrement operator")
                else:
                    types[i+1].append("decrement operator")

                continue

            #catches YR
            yrKeyword = re.search("^(YR)$", splitWords[j])
            if(yrKeyword and imYrKeyword== ""):
                if(i+1 not in lexemes):
                    lexemes[i+1] = []
                    lexemes[i+1].append(splitWords[j])
                else:
                    lexemes[i+1].append(splitWords[j])
            
                if(i+1 not in types):
                    types[i+1] = []
                    types[i+1].append("loop operator delimiter")
                else:
                    types[i+1].append("loop operator delimiter")

                continue

            #catches TIL
            tilKeyword = re.search("^(TIL)$", splitWords[j])
            if(tilKeyword):
                if(i+1 not in lexemes):
                    lexemes[i+1] = []
                    lexemes[i+1].append(splitWords[j])
                else:
                    lexemes[i+1].append(splitWords[j])
            
                if(i+1 not in types):
                    types[i+1] = []
                    types[i+1].append("for loop keyword")
                else:
                    types[i+1].append("for loop keyword")

                continue
            
            #catches WILE
            wileKeyword = re.search("^(WILE)$", splitWords[j])
            if(wileKeyword):
                if(i+1 not in lexemes):
                    lexemes[i+1] = []
                    lexemes[i+1].append(splitWords[j])
                else:
                    lexemes[i+1].append(splitWords[j])
            
                if(i+1 not in types):
                    types[i+1] = []
                    types[i+1].append("while loop keyword")
                else:
                    types[i+1].append("while loop keyword")

                continue

            #catches GTFO
            gtfoKeyword = re.search("^(GTFO)$", splitWords[j])
            if(gtfoKeyword):
                if(i+1 not in lexemes):
                    lexemes[i+1] = []
                    lexemes[i+1].append(splitWords[j])
                else:
                    lexemes[i+1].append(splitWords[j])
            
                if(i+1 not in types):
                    types[i+1] = []
                    types[i+1].append("break keyword")
                else:
                    types[i+1].append("break keyword")

                continue

            #catches AN
            anKeyword = re.search("^(AN)$", splitWords[j])
            if(anKeyword):
                if(i+1 not in lexemes):
                    lexemes[i+1] = []
                    lexemes[i+1].append(splitWords[j])
                else:
                    lexemes[i+1].append(splitWords[j])
            
                if(i+1 not in types):
                    types[i+1] = []
                    types[i+1].append("argument separator keyword")
                else:
                    types[i+1].append("argument separator keyword")

                continue
            
            #catches MKAY
            mkayKeyword = re.search("^(MKAY)$", splitWords[j])
            if(mkayKeyword):
                if(i+1 not in lexemes):
                    lexemes[i+1] = []
                    lexemes[i+1].append(splitWords[j])
                else:
                    lexemes[i+1].append(splitWords[j])
            
                if(i+1 not in types):
                    types[i+1] = []
                    types[i+1].append("infinite arity operation delimiter")
                else:
                    types[i+1].append("infinite arity operation delimiter")

                continue
            
            #catches IDENTIFIERS
            identifier = re.search("^[a-zA-Z][a-zA-Z0-9_]*$", splitWords[j])
            if(identifier):
                if(i+1 not in lexemes):
                    lexemes[i+1] = []
                    lexemes[i+1].append(splitWords[j])
                else:
                    lexemes[i+1].append(splitWords[j])

                if(i+1 not in types):
                    types[i+1] = []
                    types[i+1].append("identifier")
                else:
                    types[i+1].append("identifier")

                continue

            #every other case
            return "SyntaxError: " + splitWords[j] + " is an invalid keyword"

# def printSymbolTable():
#     space1 = 40
#     space2 = 40

#     for i in lexemes.keys():
#         print("Line " + str(i))
#         for j in range(0, len(lexemes[i])):
#             print("Lexeme: " + lexemes[i][j], end=(" " * (space1 - len(lexemes[i][j]))))
#             print("Type: " + types[i][j], end=(" " * (space2 - len(types[i][j]))))
#             print("")
#         print("")

# def getLexemes():
#     return lexemes

# def getType():
#     return types

# MAIN CODE
# lexemes = {}
# types = {}

# lines = readFile(filename)
# findLexemes(lines, lexemes, types)

#printSymbolTable()
