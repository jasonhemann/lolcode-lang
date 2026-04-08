from distutils.log import error
from operator import index
import lexer

def getTokens():
    tokens = lexer.main()
    # print(tokens)
    # tokens = [x for x in tokens if x[0][0] != "newline"]
    # tokens = [x for x in tokens if x[0][0] != "multi_cmnt"]
    for i in tokens:
        print(i)
    return tokens
errorRaised = False
def checkTypeVar(type1):
    if type1 in lexer.TYPE_kw or type1 == "varident":
        return True
    return False
def checkArithBoolKW(type1):
    if type1 in lexer.ARITHMETHIC_kw or type1 in lexer.BOOLEAN_kw:
        return True
    return False
def visiArith(line, index, lineNumber):
    currIndex = index
    # print(line[currIndex][0])
    while currIndex < len(line):
        # print(currIndex, len(line))
        if checkArithBoolKW(line[currIndex][0]):#operator
            # print("checkArithBoolKW TRUE")
            currIndex+=1
            if line[currIndex][0] == "K_NOT":
                currIndex+=1
            if checkTypeVar(line[currIndex][0]): #operand 1
                # print("checkTypeVAr TRUE")
                currIndex+=1
                if line[currIndex][0] == "K_AN": #delim
                    currIndex+=1
                    if line[currIndex][0] == "K_NOT":
                        currIndex+=1
                    if checkTypeVar(line[currIndex][0]):#operand 2
                        currIndex+=1
                    elif checkArithBoolKW(line[currIndex][0]):#operand 2
                        result = visiArith(line, currIndex, lineNumber)
                        currIndex = result
                    elif line[currIndex][0] in ("K_ANY_OF", "K_ALL_OF"):
                        currIndex = mkayArity(line,lineNumber,currIndex)
                    elif checkArithBoolKW(line[currIndex][0]):
                        result = visiArith(line, currIndex, lineNumber)
                        currIndex = result
                    else:
                        printError(lineNumber, "Missing second operand.", line)
                else:
                    printError(lineNumber, "Missing AN.", line)
            elif checkArithBoolKW(line[currIndex][0]):
                #print("OP: "+line[currIndex][0])
                result = visiArith(line, currIndex, lineNumber)
                currIndex = result
                if line[currIndex][0] == "K_AN":
                    #print("AN: " + line[currIndex][0])
                    currIndex+=1
                    if line[currIndex][0] == "K_NOT":
                        currIndex+=1
                    if checkTypeVar(line[currIndex][0]):
                        #print("NEXT NEXT: " + line[currIndex].value)
                        currIndex+=1
                    elif checkArithBoolKW(line[currIndex][0]):
                        result = visiArith(line, currIndex, lineNumber)
                        currIndex = result
                    elif checkArithBoolKW(line[currIndex][0]):
                        result = visiArith(line, currIndex, lineNumber)
                        currIndex = result
                    else:
                        printError(lineNumber, "Missing second operand.", line)
                else:
                    printError(lineNumber, "Missing AN.", line)
            elif line[currIndex][0] in ("K_ANY_OF", "K_ALL_OF"):
                currIndex = mkayArity(line,lineNumber,currIndex)
                if line[currIndex][0] == "K_AN":
                    #print("AN: " + line[currIndex][0])
                    currIndex+=1
                    if line[currIndex][0] == "K_NOT":
                        currIndex+=1
                    if checkTypeVar(line[currIndex][0]):
                        #print("NEXT NEXT: " + line[currIndex].value)
                        currIndex+=1
                    elif checkArithBoolKW(line[currIndex][0]):
                        result = visiArith(line, currIndex, lineNumber)
                        currIndex = result
                    else:
                        printError(lineNumber, "Missing second operand.", line)
                else:
                    printError(lineNumber, "Missing AN.", line)
            else:
                printError(lineNumber, "Missing first operand.", line)
            break
        currIndex+=1
    #print(subSet)
    return currIndex
def mkayArity(line, lineNum, index):
    currIndex = index
    # print(line[currIndex])
    mkayFlag = False
    while not mkayFlag and currIndex < len(line):
        if checkTypeVar(line[currIndex][0]):
            currIndex+=1
        elif checkArithBoolKW(line[currIndex][0]):
            currIndex = visiArith(line,currIndex,lineNum)
        if line[currIndex][0] == "K_AN":
            currIndex+=1
            continue
        elif line[currIndex][0] == "K_NOT":
            currIndex+=1
            continue
        elif line[currIndex][0] == "K_MKAY":
            mkayFlag = True
            currIndex+=1
            return currIndex
        else:
            # print("HII")
            # print(line[currIndex])
            printError(lineNum,"What's this?", line)
    else:
        printError(lineNum,"No MKAY detected.", line)
def visibleAn(line, lineNum, index):
    currIndex = index
    # print(line, index)
    while currIndex < len(line)-1:
        currIndex+=1
        #first operand
        if line[currIndex][0] == "K_SMOOSH":
            currIndex+=1
        if line[currIndex][0] == "K_NOT":
            currIndex+=1
        if checkTypeVar(line[currIndex][0]):
            currIndex+=1
            if line[currIndex][0] == "K_AN": #AN delimiter
                currIndex+=1
                if line[currIndex][0] == "K_NOT":
                    currIndex+=1
                if checkTypeVar(line[currIndex][0]): #second operand
                    currIndex+=1
                elif checkArithBoolKW(line[currIndex][0]):#second operand an expr
                    results = visiArith(line,currIndex, lineNum) 
                    currIndex=results
                elif line[currIndex][0] in ("K_ALL_OF", "K_ANY_OF"):
                    currIndex+=1
                    currIndex = mkayArity(line, lineNum, currIndex)
                else:
                    printError(lineNum,"Not valid operand.",line)
            elif line[currIndex][0] in ("K_BTW", "newline"):
                return True
            else:
                if ("K_AN", "AN") not in line:
                    return True
        elif checkArithBoolKW(line[currIndex][0]): #first operand
            results = visiArith(line,currIndex, lineNum)
            currIndex =results
        elif line[currIndex][0] in ("K_ALL_OF", "K_ANY_OF"):
            currIndex+=1
            currIndex = mkayArity(line, lineNum, currIndex)
        elif line[currIndex][0] == "str_delim" and line[currIndex+1][0] == "str_literal" and line[currIndex+2][0] == "str_delim":
            currIndex+=3
        else:
            printError(lineNum,"Invalid operand 1.",line)
    return True
def printError(lineNumber, reason, line):
    global errorRaised
    errorRaised = "Syntax error on line %d: %s" % (lineNumber,reason)
    print(line)
def main():
    lines = getTokens()
    lineNumber = 0
    haiFlag = False
    kthxbyeFlag = False
    while not haiFlag:
        keyword = lines[lineNumber][0]
        lineNumber += 1
        if keyword[0] == "K_HAI":
            haiFlag = True
            #print("HAI DETECTED")
            break
        elif keyword[0] == "K_BTW":
            continue
        else:
            printError(lineNumber,"not hai.", line)
    orlyCount = 0
    while not kthxbyeFlag and not errorRaised:
        line = lines[lineNumber]
        lineNumber += 1
        firstKW = line[0]
        firstKWType = firstKW[0]
        notCount = 0
        notVal = 0
        if firstKWType == "K_BTW":
            continue
        if firstKWType == "K_KTHXBYE":
            kthxbyeFlag = True
            if line[1][0] not in ["newline", "K_BTW"]:
                printError(lineNumber, "check your KTHXBYE 1", line)
            break
        if firstKWType == "newline":
            continue
        if firstKWType == "K_I_HAS_A":
            # print("I_HAS_A VALID")
            if line[1][0] != "varident":
                printError(lineNumber, "Not a variable identifier.", line)
            if line[2][0] in ["newline", "K_BTW"]:
                continue
            elif line[2][0] == "K_ITZ":
                # print("ITZ VALID")
                if line[3][0] in lexer.TYPE_kw:
                    if line[4][0] not in ["newline", "K_BTW"]:
                        printError(lineNumber, "Only one value can be assigned to a variable.", line)
                elif line[3][0] in lexer.ARITHMETHIC_kw or line[3][0] in lexer.BOOLEAN_kw:
                    visiArith(line, 3, lineNumber)
                else:
                    printError(lineNumber, "Not anything related to ITZ.", line)
            else:
                printError(lineNumber, "Not ITZ.", line)
        if firstKWType == "K_VISIBLE":
            if visibleAn(line, lineNumber, 0):
                continue
        if firstKWType == "K_GIMMEH":
            if line[1][0] == "varident":
                if line[2][0] in ("K_BTW", "newline"):
                    continue
            printError(lineNumber, "GIMMEH only takes a variable.", line)
        if firstKWType == "K_O_RLY":
            orlyCount += 1
            continue
        if firstKWType == "K_OIC":
            orlyCount-=1
            if orlyCount < 0:
                printError(lineNumber,"Misplacced OIC here.",line)
            continue
        if checkArithBoolKW(firstKWType):
            visiArith(line, 0, lineNumber)
        if firstKWType == "varident":
            if line[1][0] == "K_R":
                if line[2][0] in lexer.TYPE_kw:
                    if line[3][0] in ("K_BTW", "newline"):
                        continue
                elif checkArithBoolKW(line[2][0]):
                    visiArith(line, 2, lineNumber)
                elif line[2][0] == "K_SMOOSH":
                    if visibleAn(line, lineNumber, 2):
                        continue
            elif line[1][0] == "K_IS_NOW_A":
                if line[2][0] in lexer.TYPE_kw:
                    continue
                else:
                    printError(lineNumber, "Invalid type to typecast into.", line)
            else:
                printError(lineNumber, "Invalid value for variable.", line)
    if kthxbyeFlag:
        for lineIndex in range(lineNumber, len(lines)):
            lineNumber += 1
            if lines[lineIndex][0][0] in ["K_BTW", "newline"]:
                continue
            else:
                printError(lineNumber, "check your KTHXBYE 2", line)
    if errorRaised:
        return(errorRaised)
    else:
        return (lines)

print(main())