import lexical_analyzer
import syntactic_analyzer
from tkinter import simpledialog

symbolTable = {
    "IT": None
}

switchCases = []

inLoop = False

def mathSolve(tokens):
    acc = []
    eval = "NO ERRORS"
    curr = 0
    math_operations = ["SUM OF", "DIFF OF", "PRODUKT OF", "QUOSHUNT OF", "MOD OF", "BIGGR OF", "SMALLR OF"]
    sublistTokens = []
    for i in tokens:
        if (i[0] == 'Arithmetic Operation' or i[0] == 'Operand Separator'):
            sublistTokens.append(i[1])
        elif (i[0] == "NUMBR Literal"):
            sublistTokens.append(int(i[1]))
        elif (i[0] == "NUMBAR Literal"):
            sublistTokens.append(float(i[1]))
        elif (i[0] == "YARN Literal"):
            try:
                containsDecimal = '.' in i[1]

                if (containsDecimal):
                    sublistTokens.append(float(i[1]))
                else:
                    sublistTokens.append(int(i[1]))
            except:
                eval = f"ERROR: {i[1]} cannot be converted to number"
                return eval
        elif (i[0] == "TROOF Literal"):
            if (i[1] == "WIN"): sublistTokens.append(1)
            else:               sublistTokens.append(0)
        elif (i[0] == "Variable Identifier"):
            varValue = symbolTable[i[1]]
            try:
                # check if int, float, string (convert to num), bool (convert to num)
                if (varValue == True): sublistTokens.append(1)
                elif (varValue == False): sublistTokens.append(0)
                elif (varValue == None): 
                    eval = f"ERROR: {varValue} cannot be converted to number"
                    return eval
                elif (isinstance(varValue, int) or isinstance(varValue, float)): sublistTokens.append(varValue)
                else: #YARN
                    containsDecimal = '.' in varValue

                    if (containsDecimal):
                        sublistTokens.append(float(varValue))
                    else:
                        sublistTokens.append(int(varValue))
            except:
                eval = f"ERROR: {varValue} cannot be converted to number"
                return eval

    
    while (1):
        if (len(acc) >= 3):
            lastElemIsNum = isinstance(acc[len(acc)-1], int) or isinstance(acc[len(acc)-1], float)
            secondLastElemIsNum = isinstance(acc[len(acc)-2], int) or isinstance(acc[len(acc)-2], float)
            if (lastElemIsNum and secondLastElemIsNum):
                firstOperand = acc[len(acc)-2]
                secondOperand = acc[len(acc)-1]
                operation = acc[len(acc)-3]
                if (operation not in math_operations): break
                if (operation == "SUM OF"):         acc[len(acc)-3] = firstOperand + secondOperand
                elif (operation == "DIFF OF"):      acc[len(acc)-3] = firstOperand - secondOperand
                elif (operation == "PRODUKT OF"):   acc[len(acc)-3] = firstOperand * secondOperand
                elif (operation == "QUOSHUNT OF"):  
                    if (secondOperand == 0): return "ERROR: Cannot divide by zero"
                    temp = firstOperand / secondOperand
                    cnv = int(temp)
                    if (temp-cnv == 0):
                        if ('.' in str(firstOperand) or '.' in str(secondOperand)):
                            acc[len(acc)-3] = temp
                        else:
                            acc[len(acc)-3] = int(temp)
                    else:
                        acc[len(acc)-3] = temp
                elif (operation == "MOD OF"):       acc[len(acc)-3] = firstOperand % secondOperand
                elif (operation == "BIGGR OF"):     acc[len(acc)-3] = max(firstOperand, secondOperand)
                elif (operation == "SMALLR OF"):    acc[len(acc)-3] = min(firstOperand, secondOperand)
                acc.pop()
                acc.pop()

                if (len(acc) == 1 and curr > len(tokens)-1):
                    eval = acc[0]
                    break
                continue

        if (curr == 0):
            if (sublistTokens[curr] not in math_operations): break
            else:
                acc.append(sublistTokens[curr])
                curr += 1
        else:
            toBeInserted = sublistTokens[curr]

            if (toBeInserted == "AN"):
                curr += 1
                #print(sublistTokens)
                toBeInserted = sublistTokens[curr]
            
            acc.append(toBeInserted)
            curr += 1
    
    return eval

def semanticAnalyze(lst, interface):
    temp = ""
    tempList = []
    cnt = 0
    update_symbol_table(interface)
    while (cnt < len(lst)):
        line = lst[cnt]
        if (line[0][0] == "Code Delimiter OPEN"):
            pass
        elif (line[0][0] == "Variable Identifier"):
            if (len(line) == 1):
                symbolTable["IT"] = symbolTable[line[0][1]]
                update_symbol_table(interface)
            else:
                # in ["NUMBR Literal","NUMBAR Literal","TROOF Literal","YARN Literal"]
                if (line[1][0] == "Assignment Keyword"): # R keyword
                    value = line[2]
                    if (isinstance(value, list)): 
                        if (value[0] == "Variable Identifier"): # assigning value from variable
                            symbolTable[line[0][1]] = symbolTable[value[1]]
                        else:                                   # assigning value from a literal            
                            if (value[0] == "NUMBR Literal"): 
                                symbolTable[line[0][1]] = int(value[1])
                            elif (value[0] == "NUMBAR Literal"):
                                symbolTable[line[0][1]] = float(value[1])
                            elif (value[0] ==  "YARN Literal"):
                                symbolTable[line[0][1]] = value[1]
                            else:
                                if (value[1] == "WIN"):
                                    symbolTable[line[0][1]] = True
                                else:
                                    symbolTable[line[0][1]] = False

                    elif (value == "<typecasted_value>"):       # MAEK
                        var = line[0][1]
                        cnt += 1
                        line = lst[cnt]

                        new_value = symbolTable[line[1][1]]

                        if (line[2][0] == "YARN keyword"):      # converting to YARN
                            symbolTable[var] = str(new_value)
                        elif (line[2][0] == "TROOF keyword"):   # to TROOF
                            if (new_value == None): symbolTable[var] = False
                            elif (isinstance(new_value, int) or isinstance(new_value, float)):
                                if (new_value == 0) : symbolTable[var] = False
                                else: symbolTable[var] = True
                            elif (isinstance(new_value, str)):
                                if (len(new_value) == 0) : symbolTable[var] = False
                                else: symbolTable[var] = True
                            else:
                                symbolTable[var] = new_value
                        elif (line[2][0] == "NUMBAR keyword"):  # to float
                            if (new_value == None): 
                                symbolTable[var] = 0.0
                            elif (isinstance(new_value, int)):
                                symbolTable[var] = float(new_value)
                            elif (isinstance(new_value, float)):
                                symbolTable[var] = new_value
                            elif (isinstance(new_value, str)):
                                if (check_string_to_float(new_value)) : symbolTable[var] = float(new_value)
                                else: return f"ERROR: {new_value} can't be typecasted to float"
                            else:
                                if (new_value == True): symbolTable[var] = 1.0
                                else: symbolTable[var] = 0.0
                        elif (line[2][0] == "NUMBR keyword"):  # to integer
                            if (new_value == None): 
                                symbolTable[var] = 0
                            elif (isinstance(new_value, int)): # TROOF are also fall here
                                symbolTable[var] = int(new_value)
                            elif (isinstance(new_value, float)):
                                symbolTable[var] = int(new_value)
                            else:
                                if (check_string_to_int(new_value)) : symbolTable[var] = int(float(new_value))
                                else: return f"ERROR: '{new_value}' can't be typecasted to integer"

                    elif (value == "<comparison_operation>"):
                        var = line[0][1]
                        cnt += 1
                        line = lst[cnt]
                        result = get_comparison_result(line)
                        if (result not in [True, False]): return result

                        symbolTable[var] = result

                    elif (value == "<boolean_operation>"):
                        var = line[0][1]
                        cnt += 1
                        line = lst[cnt]
                        result = get_bool_result(line)

                        symbolTable[var] = result

                    elif (value == "<concat>"):
                        var = line[0][1]
                        cnt += 1
                        line = lst[cnt]

                        numSmooshArgs = line[0][2]
                        tempList = []
                        tempCnt = 0
                        while (tempCnt < numSmooshArgs):
                            cnt += 1
                            tempList.append(lst[cnt])

                            if (lst[cnt][0] == "<math_arguments>"):
                                tempList.pop()
                                cnt += 1
                                tempList.append(lst[cnt])
                                tempCnt += len(lst[cnt])-1
                            # boolean
                            # comparison
                            elif (lst[cnt][0] in ["<boolean_operation>", "<comparison_operation>"]):
                                tempList.pop()
                                cnt += 1
                                tempList.append(lst[cnt])
                                
                                tempCnt += lst[cnt][len(lst[cnt])-1] - 1
                            
                            tempCnt += 1
                        
                        temp = ""
                        for i in tempList:
                            lexType = i[0][0]
                            value = i[0][1]
                            if (isinstance(i[0], list)):
                                if (lexType in ["NUMBR Literal","NUMBAR Literal","TROOF Literal","YARN Literal"]):
                                    if (lexType == "NUMBAR Literal"):
                                        temp += "{:.2f}".format(value)
                                    else:
                                        temp += str(value)
                                elif (lexType == "Variable Identifier"):
                                    if (symbolTable[value] == None):
                                        eval = f"ERROR: Variable {value} of type NOOB cannot be implicitly typecasted to YARN."
                                        return eval
                                    else:
                                        if (isinstance(symbolTable[value], bool) and symbolTable[value] == True):
                                            temp += "WIN"
                                        elif (isinstance(symbolTable[value], bool) and symbolTable[value] == False):
                                            temp += "FAIL"
                                        elif (isinstance(symbolTable[value], float)):
                                            temp += "{:.2f}".format(symbolTable[value])
                                        else:
                                            temp += str(symbolTable[value])
                                elif (lexType == "Arithmetic Operation"):
                                    valueM = mathSolve(i)
                                    if (isinstance(valueM, str)):
                                        return valueM
                                    temp += str(valueM)
                                elif (lexType == "Operand Separator"):
                                    pass
                            else: 
                                if (i[0] in ["BOTH OF", "EITHER OF", "WON OF", "NOT", "ALL OF", "ANY OF"]):
                                    result = get_bool_result(i)

                                    temp += str(result)

                                elif (i[0] in ["BOTH SAEM", "DIFFRINT"]):
                                    result = get_comparison_result(i)
                                    if (result not in [True, False]): return result

                                    temp += str(result)
                                    
                        symbolTable[var] = temp

                    else: # Math operations
                        var = line[0][1]
                        cnt += 1
                        line = lst[cnt]

                        value = mathSolve(lst[cnt])
                        if (isinstance(value, str)):
                            return value

                        symbolTable[var] = value
                else: # IS NOW A -> "Typecast Keyword"
                    val = symbolTable[line[0][1]]
                    new_type = line[2][0]
                    if (new_type == "NUMBAR keyword"):
                        if (val == None): symbolTable[line[0][1]] = 0.0
                        else:
                            if(check_string_to_float(val)): symbolTable[line[0][1]] = float(val)
                            else: return f"ERROR: {val} can't be typecasted to float"
                    elif (new_type == "NUMBR keyword"):
                        if (val == None): symbolTable[line[0][1]] = 0
                        else:
                            if(check_string_to_int(val)): symbolTable[line[0][1]] = int(float(val))
                            else: return f"ERROR: '{val}' can't be typecasted to integer"
                    elif (new_type == "YARN keyword"):
                        if (val == None): symbolTable[line[0][1]] = ""
                        else:
                            if (isinstance(val, float)):
                                symbolTable[line[0][1]] = "{:.2f}".format(val)
                            else:
                                symbolTable[line[0][1]] = str(val)
                    else: # TROOF
                        if(val == None): symbolTable[line[0][1]] = False
                        else:
                            if (val == None): symbolTable[line[0][1]] = False
                            elif (isinstance(val, int) or isinstance(val, float)):
                                if (val == 0) : symbolTable[line[0][1]] = False
                                else: symbolTable[line[0][1]] = True
                            elif (isinstance(val, str)):
                                if (len(val) == 0) : symbolTable[line[0][1]] = False
                                else: symbolTable[line[0][1]] = True
                            else: # True or False
                                symbolTable[line[0][1]] = val
            update_symbol_table(interface)
        elif (line[0] == "<typecasted_value>"):
            cnt += 1
            line = lst[cnt]

            new_value = symbolTable[line[1][1]]

            if (line[2][0] == "YARN keyword"):      # converting to YARN
                if (isinstance(new_value, float)):
                    symbolTable["IT"] = "{:.2f}".format(new_value)
                else:
                    symbolTable["IT"] = str(new_value)
            elif (line[2][0] == "TROOF keyword"):   # to TROOF
                if (new_value == None): symbolTable["IT"] = False
                elif (isinstance(new_value, int) or isinstance(new_value, float)):
                    if (new_value == 0) : symbolTable["IT"] = False
                    else: symbolTable["IT"] = True
                elif (isinstance(new_value, str)):
                    if (len(new_value) == 0) : symbolTable["IT"] = False
                    else: symbolTable["IT"] = True
                else:
                    symbolTable["IT"] = new_value
            elif (line[2][0] == "NUMBAR keyword"):  # to float
                if (new_value == None): 
                    symbolTable["IT"] = 0.0
                elif (isinstance(new_value, int)):
                    symbolTable["IT"] = float(new_value)
                elif (isinstance(new_value, float)):
                    symbolTable["IT"] = new_value
                elif (isinstance(new_value, str)):
                    if (check_string_to_float(new_value)) : symbolTable["IT"] = float(new_value)
                    else: return f"ERROR: {new_value} can't be typecasted to float"
                else:
                    if (new_value == True): symbolTable["IT"] = 1.0
                    else: symbolTable["IT"] = 0.0
            elif (line[2][0] == "NUMBR keyword"):  # to integer
                if (new_value == None): 
                    symbolTable["IT"] = 0
                elif (isinstance(new_value, int)): # TROOF are also fall here
                    symbolTable["IT"] = int(new_value)
                elif (isinstance(new_value, float)):
                    symbolTable["IT"] = int(new_value)
                else:
                    if (check_string_to_int(new_value)) : symbolTable["IT"] = int(float(new_value))
                    else: return f"ERROR: '{new_value}' can't be typecasted to integer"
            update_symbol_table(interface)

        elif (line[0][0] == "Variable Declaration"):
            var = line[1][1]
            if var in symbolTable:
                return f"ERROR: {var} has already been declared"
            else:
                symbolTable[var] = None
                if (len(line) > 2):
                    if (isinstance(line[3], str)):
                        typeChild = line[3]
                        if (typeChild == "<math_arguments>"):
                            cnt += 1
                            value = mathSolve(lst[cnt])
                            if (isinstance(value, str)):
                                return value
                            allInt = True
                            for i in lst[cnt]:
                                if (i[0] == "NUMBAR Literal"):
                                    allInt = False
                                    break
                                elif (i[0] == "YARN Literal"):
                                    temp = float(i[1])
                                    checkTemp = temp - int(float(i[1]))
                                    if (checkTemp != 0):
                                        allInt = False
                                        break
                            if (allInt):
                                symbolTable[var] = int(value)
                            else:
                                symbolTable[var] = value
                        elif(typeChild == "<boolean_operation>"): 
                            var = line[1][1]
                            cnt += 1
                            line = lst[cnt]
                            result = get_bool_result(line)

                            symbolTable[var] = result
                        
                        elif (typeChild == "<comparison_operation>"):
                            var = line[1][1]
                            cnt += 1
                            line = lst[cnt]
                            result = get_comparison_result(line)
                            if (result not in [True, False]): return result

                            symbolTable[var] = result

                    elif (isinstance(line[3], list)):
                        valType = line[3][0]
                        value = line[3][1]

                        if (valType == "NUMBR Literal"): 
                            symbolTable[var] = int(value)
                        elif (valType == "NUMBAR Literal"):
                            symbolTable[var] = float(value)
                        elif (valType == "YARN Literal"):
                            symbolTable[var] = value
                        elif (valType == "TROOF Literal"):
                            if (value == "WIN"):
                                symbolTable[var] = True
                            else:
                                symbolTable[var] = False
            update_symbol_table(interface)
        elif (line[0][0] == "Arithmetic Operation"):
            #print(lst[cnt:])
            #print("###"+str(line))
            value = mathSolve(lst[cnt])
            if (isinstance(value, str)):
                return value
            symbolTable["IT"] = value
            update_symbol_table(interface)
        elif (line[0][0] in ["NUMBR Literal","NUMBAR Literal","TROOF Literal","YARN Literal"]):
            type1 = line[0][0]
            value = line[0][1]
            if (type1 == "NUMBR Literal"):
                symbolTable["IT"] = int(value)
            elif (type1 == "NUMBAR Literal"):
                symbolTable["IT"] = float(value)
            elif (type1 == "YARN Literal"):
                symbolTable["IT"] = value
            elif (type1 == "TROOF Literal"):
                if (value == "WIN"):
                    symbolTable["IT"] = True
                else:
                    symbolTable["IT"] = False
            update_symbol_table(interface)
        elif (line[0][0] == "Input Keyword"):
            
            temp = simpledialog.askstring("","Enter input")
            if (temp == None):
                temp = ""
            interface.x_textbox.insert("end",temp+"\n")
            interface.x_textbox.see("end")
            var = line[1][1]
            symbolTable[var] = temp
            update_symbol_table(interface)
        elif (line[0][0] == "Output Keyword"):
            numVisibleArgs = line[0][2]
            tempList = []
            smooshIndex = -1
            tempCnt = 0
            # print(f"here:   {numVisibleArgs}")
            while (tempCnt < numVisibleArgs):
                cnt += 1
                tempList.append(lst[cnt])

                if (lst[cnt][0] in ["<math_arguments>"]):
                    tempList.pop()
                    cnt += 1
                    tempList.append(lst[cnt])
                    tempCnt += len(lst[cnt])-1

                elif (lst[cnt][0] in ["<boolean_operation>", "<comparison_operation>"]):
                    tempList.pop()
                    cnt += 1
                    tempList.append(lst[cnt])
                    
                    tempCnt += lst[cnt][len(lst[cnt])-1] - 1 

                if (lst[cnt][0][0] == "Concatenation Keyword"):
                    smooshIndex = cnt
                
                tempCnt += 1

            if (smooshIndex != -1):
                numSmooshArgs = lst[smooshIndex][0][2]
                tempCnt = 0
                while (tempCnt < numSmooshArgs):
                    cnt += 1
                    tempList.append(lst[cnt])

                    if (lst[cnt][0] == "<math_arguments>"):
                        tempList.pop()
                        cnt += 1
                        tempList.append(lst[cnt])
                        tempCnt += len(lst[cnt])-1
                    # boolean
                    # comparison
                    
                    tempCnt += 1
            
            temp = ""
            for i in tempList:
                lexType = i[0][0]
                value = i[0][1]

                if (isinstance(i[0], list)):
                    if (lexType in ["NUMBR Literal","NUMBAR Literal","TROOF Literal","YARN Literal"]):
                        if (lexType == "NUMBAR Literal"):
                            temp += "{:.2f}".format(value)
                        else:
                            temp += str(value)
                    elif (lexType == "Variable Identifier"):
                        if (symbolTable[value] == None):
                            eval = f"ERROR: Variable {value} of type NOOB cannot be implicitly typecasted to YARN."
                            return eval
                        else:
                            #print("***")
                            #print(symbolTable)
                            if (isinstance(symbolTable[value], bool) and symbolTable[value] == True):
                                temp += "WIN"
                            elif (isinstance(symbolTable[value], bool) and symbolTable[value] == False):
                                temp += "FAIL"
                            elif (isinstance(symbolTable[value], float)):
                                temp += "{:.2f}".format(symbolTable[value])
                            else:
                                temp += str(symbolTable[value])
                    elif (lexType == "Arithmetic Operation"):
                        valueM = mathSolve(i)
                        if (isinstance(valueM, str)):
                            return valueM
                        temp += str(valueM)
                    elif (lexType == "Operand Separator"):
                        pass
                    elif (lexType == "Suppressor"):
                        pass
                    
                else : # bool and comparison is seperated since i[0][0] is not a lex type
                    if (i[0] in ["BOTH OF", "EITHER OF", "WON OF", "NOT", "ALL OF", "ANY OF"]):
                        result = get_bool_result(i)
                        if (result not in [True, False]): return result

                        temp += "WIN" if(result==True) else "FAIL"

                    elif (i[0] in ["BOTH SAEM", "DIFFRINT"]):
                        result = get_comparison_result(i)
                        if (result not in [True, False]): return result

                        temp += "WIN" if(result==True) else "FAIL"

            # Don't comment out this print statement
            #print(temp)
            playBell = False
            temp = temp.replace("<<@#QUOTE#$>>",'"')
            temp = temp.replace("<<@#NEWLINE#$>>",'\n')
            if ("\a" in temp):
                temp = temp.replace("\a","")
                playBell = True
            if (playBell):
                print('\a')
            try:
                if (tempList[len(tempList)-1][0][0] == "Suppressor"):
                    interface.x_textbox.insert("end",temp)
                else:
                    interface.x_textbox.insert("end",temp+"\n")
            except:
                interface.x_textbox.insert("end",temp+"\n")
            interface.x_textbox.see("end")
            # # # # # # # # # # # # # # # # # # # #
        elif (line[0][0] == "Concatenation Keyword"):
            numSmooshArgs = line[0][2]
            tempList = []
            tempCnt = 0
            while (tempCnt < numSmooshArgs):
                cnt += 1
                tempList.append(lst[cnt])

                if (lst[cnt][0] == "<math_arguments>"):
                    tempList.pop()
                    cnt += 1
                    tempList.append(lst[cnt])
                    tempCnt += len(lst[cnt])-1
                # boolean
                # comparison
                elif (lst[cnt][0] in ["<boolean_operation>", "<comparison_operation>"]):
                    tempList.pop()
                    cnt += 1
                    tempList.append(lst[cnt])
                    
                    tempCnt += lst[cnt][len(lst[cnt])-1] - 1
                
                tempCnt += 1
            
            temp = ""
            for i in tempList:
                lexType = i[0][0]
                value = i[0][1]
                if (isinstance(i[0], list)):
                    if (lexType in ["NUMBR Literal","NUMBAR Literal","TROOF Literal","YARN Literal"]):
                        if (lexType == "NUMBAR Literal"):
                            temp += "{:.2f}".format(value)
                        else:
                            temp += str(value)
                    elif (lexType == "Variable Identifier"):
                        if (symbolTable[value] == None):
                            eval = f"ERROR: Variable {value} of type NOOB cannot be implicitly typecasted to YARN."
                            return eval
                        else:
                            if (isinstance(symbolTable[value], bool) and symbolTable[value] == True):
                                temp += "WIN"
                            elif (isinstance(symbolTable[value], bool) and symbolTable[value] == False):
                                temp += "FAIL"
                            elif (isinstance(symbolTable[value], float)):
                                temp += "{:.2f}".format(symbolTable[value])
                            else:
                                temp += str(symbolTable[value])
                    elif (lexType == "Arithmetic Operation"):
                        valueM = mathSolve(i)
                        if (isinstance(valueM, str)):
                            return valueM
                        temp += str(valueM)
                    elif (lexType == "Operand Separator"):
                        pass
                else: 
                    if (i[0] in ["BOTH OF", "EITHER OF", "WON OF", "NOT", "ALL OF", "ANY OF"]):
                        result = get_bool_result(i)

                        temp += str(result)

                    elif (i[0] in ["BOTH SAEM", "DIFFRINT"]):
                        result = get_comparison_result(i)
                        if (result not in [True, False]): return result

                        temp += str(result)

            symbolTable["IT"] = temp
            update_symbol_table(interface)
        elif (line[0][0] == "<if-then block>"):
            ifList = []
            cnt += 2
            while (1):
                if (lst[cnt][0][0] == "<if-end>"):
                    break
                ifList.append(lst[cnt])
                cnt += 1
            cnt += 1
            elseList = []
            if (cnt >= len(lst)):
                pass
            else:
                if (lst[cnt][0][0] == "<else>"):
                    
                    cnt += 1
                    while (1):
                        if (lst[cnt][0][0] == "<else-end>"):
                            break
                        elseList.append(lst[cnt])
                        cnt += 1
                    cnt += 1
            
            varIT = symbolTable["IT"]
            if (isinstance(varIT, str)):
                if (varIT == ""):   eval = False
                else:               eval = True
            elif (isinstance(varIT, int) or isinstance(varIT, float)):
                if (float(varIT) == 0.0):   eval = False
                else:                       eval = True
            elif (isinstance(varIT, bool)):
                eval = varIT
            else:
                eval = False
            
            #print("EVAL: "+str(eval))
            if (eval):
                tmp = semanticAnalyze(ifList, interface)
                if (tmp == "ENDLOOP"):
                    return "ENDLOOP"
            elif (len(elseList) != 0 and not eval):
                tmp = semanticAnalyze(elseList, interface)
                if (tmp == "ENDLOOP"):
                    return "ENDLOOP"
            
            continue

        elif (line[0][0] == "<switch-case block>"):
            temp = []
            #print("&&&")
            while (1):
                if (lst[cnt][0][0] == "<switch-case end>"):
                    break
                if (lst[cnt][0][0][0:6] == "<case:"):
                    caseList = []
                    endRemoved = lst[cnt][0][0][:-1]
                    frontRemoved = endRemoved[7:]
                    if (frontRemoved[0] == '"'):
                        caseVal = str(frontRemoved[1:-1])
                    elif (frontRemoved == 'WIN'):
                        caseVal = True
                    elif (frontRemoved == 'FAIL'):
                        caseVal = False
                    else:
                        containsDecimal = '.' in frontRemoved

                        if (containsDecimal):
                            caseVal = float(frontRemoved)
                        else:
                            caseVal = int(frontRemoved)

                    breakEncountered = False
                    #print("$"+str(frontRemoved))
                    while (1):
                        if (lst[cnt][0][0] == "<case-end>"):
                            break
                        
                        if (not breakEncountered):
                            caseList.append(lst[cnt])

                        if (not breakEncountered and lst[cnt][0][0] == "Break Keyword"):
                            breakEncountered = True
                        cnt += 1
                    
                    caseList.pop(0)
                    switchCases.append((caseVal, caseList))
                elif (lst[cnt][0][0] == "<default_case>"):
                    breakEncountered = False
                    caseList = []
                    #print("$")
                    while (1):
                        if (lst[cnt][0][0] == "<default-case-end>"):
                            break
                        
                        if (not breakEncountered):
                            caseList.append(lst[cnt])

                        if (not breakEncountered and lst[cnt][0][0] == "Break Keyword"):
                            breakEncountered = True
                        cnt += 1
                    caseList.pop(0)
                    switchCases.append(("$#DEFAULT#$", caseList))

                cnt += 1
            matchedCase = False
            execSucceeding = True
            #for i in switchCases:
            #    print(i)
            for i in switchCases:
                if (i[0] == "$#DEFAULT#$" and not matchedCase):
                    if (i[1][len(i[1])-1][0][0] == "Break Keyword"):
                        i[1].pop()
                        semanticAnalyze(i[1], interface)
                        break
                    else:
                        semanticAnalyze(i[1], interface)
                if (matchedCase and execSucceeding and i[0] != "$#DEFAULT#$"):
                    if (i[1][len(i[1])-1][0][0] == "Break Keyword"):
                        i[1].pop()
                        semanticAnalyze(i[1], interface)
                        break
                    else:
                        semanticAnalyze(i[1], interface)
                    continue
                if (not matchedCase and i[0] == symbolTable["IT"]):
                    matchedCase = True
                    #print("QQQ:"+str(i[1][len(i[1])-1][0]))
                    if (i[1][len(i[1])-1][0][0] == "Break Keyword"):
                        i[1].pop()
                        semanticAnalyze(i[1], interface)
                        break
                    else:
                        semanticAnalyze(i[1], interface)
            switchCases.clear()

        elif (line[0] == "<boolean_operation>"):
            cnt += 1
            line = lst[cnt]
            result = get_bool_result(line)

            symbolTable["IT"] = result
            update_symbol_table(interface)

        elif (line[0] == "<comparison_operation>"):
            cnt += 1
            line = lst[cnt]
            result = get_comparison_result(line)
            if (result not in [True, False]): return result

            symbolTable["IT"] = result
            update_symbol_table(interface)

        elif (line[0][0] == "<loop>"):
            cnt += 1
            loopList = []
            global inLoop
            inLoop = True
            loopIterOperation = lst[cnt][0][0]
            loopVar = lst[cnt][0][1]
            #print(":"+str(loopIterOperation))
            #print(":"+str(loopVar))
            cnt += 1
            while (1):
                if (lst[cnt][0][0] == "<loop-content-end>"):
                    break
                loopList.append(lst[cnt])
                cnt += 1
            loopList.pop(0)
            #print("***")
            #print(loopList)
            while (1):
                iterResult = semanticAnalyze(loopList, interface)
                #print("///"+str(iterResult))
                if (isinstance(iterResult,str)):
                    if ("ERROR" in iterResult):
                        return iterResult
                    if (iterResult == "ENDLOOP"):
                        break
                
                try:
                    temp = int(symbolTable[loopVar])
                    if (loopIterOperation == "UPPIN"):
                        temp += 1
                    else:
                        temp -= 1
                    symbolTable[loopVar] = temp
                except:
                    return f"ERROR: {loopVar} cannot be typecast to a number"
        
        elif (line[0] == "<loop>" and len(line) == 3):
            loopConditionType = line[1]
            #print(loopConditionType)
            cnt += 1
            
            #print(":::"+str(lst[cnt]))
            if (lst[cnt][0][0] == "UPPIN" or lst[cnt][0][0] == "NERFIN"):
                cnt -= 1
                loopCondition = lst[cnt][2]
                cnt += 1
                loopIterOperation = lst[cnt][0][0]
                loopVar = lst[cnt][0][1]
                #print(":"+str(loopCondition))
                #print(":"+str(loopIterOperation))
                #print(":"+str(loopVar))
                cnt += 2
            else:
                #print("^^^"+str(lst[cnt]))
                loopCondition = lst[cnt]
                cnt += 1
                loopIterOperation = lst[cnt][0][0]
                #print("^^^"+str(lst[cnt]))
                loopVar = lst[cnt][0][1]
                #print(":"+str(loopCondition))
                #print(":"+str(loopIterOperation))
                #print(":"+str(loopVar))
                cnt += 2
            
            loopList = []
            inLoop = True
            while (1):
                if (lst[cnt][0][0] == "<loop-content-end>"):
                    break
                loopList.append(lst[cnt])
                cnt += 1
            #print("***")
            #print(loopList)
            #print(loopIterOperation,loopVar)
            #print(loopConditionType,loopCondition)
            while (1):
                if (isinstance(loopCondition, list)):
                    if (loopCondition[0] in ["BOTH OF", "EITHER OF", "WON OF", "ANY OF", "ALL OF","NOT"]):
                        fulfilledExpr = get_bool_result(loopCondition)
                    elif (loopCondition[0][0] == "Arithmetic Operation"):
                        fulfilledExpr = bool(mathSolve(loopCondition))
                    else:
                        fulfilledExpr = get_comparison_result(loopCondition)
                elif (isinstance(loopCondition, str)):
                    #print("*"+loopCondition)
                    if (loopCondition == "WIN"):
                        fulfilledExpr = True
                    elif (loopCondition == "FAIL"):
                        fulfilledExpr = False
                    elif (loopCondition[0] == '"'):
                        #print("\nYARN\n")
                        if (len(loopCondition) > 0):
                            fulfilledExpr = True
                        else:
                            fulfilledExpr = False
                    elif (loopCondition[0] in ["-","0","1","2","3","4","5","6","7","8","9"]):
                        fulfilledExpr = bool(float(loopCondition))
                    else:
                        varVal = symbolTable[loopCondition]
                        if (varVal in [True,False]):
                            fulfilledExpr = varVal
                        elif (isinstance(varVal, str)):
                            if (len(varVal) > 0):
                                fulfilledExpr = True
                            else:
                                fulfilledExpr = False
                        elif (isinstance(varVal,int) or isinstance(varVal,float)):
                            fulfilledExpr = bool(varVal)
                        else:
                            fulfilledExpr = False


                if (loopConditionType == "TIL" and fulfilledExpr):
                    break
                if (loopConditionType == "WILE" and not fulfilledExpr):
                    break

                iterResult = semanticAnalyze(loopList, interface)
                #print("///"+str(iterResult))
                if (iterResult == "ENDLOOP"):
                    break
                
                try:
                    temp = int(symbolTable[loopVar])
                    if (loopIterOperation == "UPPIN"):
                        temp += 1
                    else:
                        temp -= 1
                    symbolTable[loopVar] = temp
                except:
                    return f"ERROR: {loopVar} cannot be typecast to a number"

        elif (line[0][0] == "Break Keyword" and inLoop):
            inLoop = False
            return "ENDLOOP"

        else:
            pass
            
        cnt += 1
    return 1

def check_string_to_int(value):
    try:
        int(float(value)) # weirdly "1.1" (with deci) cant be typecasted to int
        return True       # so typecast first to float, since we can typecast float to int
    except:
        return False

def check_string_to_float(value):
    try:
        float(value)
        return True
    except:
        return False

def get_comparison_value(comp_arguments, comp_type): # BIGGR OF and SMALLR OF
    UNMATCH_TYPE_ERROR = f"ERROR: Possible errors:\n\tValues are not of the same type \n\tOne of the value is of the type NOOB \n\tTried to nest BOTH SAEM or DIFFRINT with non-TROOF value"
    comp_type = comp_type
    to_evaluate = [comp_arguments[0], "", ""]

    # ============= first value ===================
    if (isinstance(comp_arguments[1], str)): # if string, might be a variable or a string
        if(comp_arguments[1][0] == "\""): # sure to be string
            temp_type = "string"
            if (comp_type == ""): comp_type = temp_type
            else:
                if (comp_type != temp_type): return UNMATCH_TYPE_ERROR
            to_evaluate[1] = comp_arguments[1][1:len(comp_arguments[1])-1] # removing double quotes
        else:
            value = symbolTable[comp_arguments[1]]
            if (value == None): # value is a NOOB
                return f"ERROR: (Comparison) Value of '{comp_arguments[1]}' must not be NOOB"
            else:
                if (isinstance(value, int)):
                    temp_type = "integer"
                    if (comp_type == ""): comp_type = temp_type
                    else:
                        if (comp_type != temp_type): return UNMATCH_TYPE_ERROR
                    to_evaluate[1] = value
                elif (isinstance(value, str)):
                    temp_type = "string"
                    if (comp_type == ""): comp_type = temp_type
                    else:
                        if (comp_type != temp_type): return UNMATCH_TYPE_ERROR
                    to_evaluate[1] = value
                elif (isinstance(value, bool)):
                    temp_type = "bool"
                    if (comp_type == ""): comp_type = temp_type
                    else:
                        if (comp_type != temp_type): return UNMATCH_TYPE_ERROR
                    to_evaluate[1] = value
                else:
                    temp_type = "float"
                    if (comp_type == ""): comp_type = temp_type
                    else:
                        if (comp_type != temp_type): return UNMATCH_TYPE_ERROR
                    to_evaluate[1] = value   
    elif (isinstance(comp_arguments[1], list)):       
        if(comp_arguments[1][0] in ["BOTH SAEM", "DIFFRINT"]): # if BOTH SAEM or DIFFRINT
            value = get_comparison_result(comp_arguments[1])
            if (isinstance(value, str)): 
                return value
            temp_type = "bool"
            if (comp_type == ""): comp_type = temp_type
            else:
                if (comp_type != temp_type): return UNMATCH_TYPE_ERROR
            to_evaluate[1] = value
        else: # if BIGGR OF or SMALLR OF
            value = get_comparison_value(comp_arguments[1], comp_type)  
            if (isinstance(value, str)): 
                if (len(value) > 6): 
                    if (value[:5] == "ERROR"):
                        return value
                temp_type = "string"
                if (comp_type == ""): comp_type = temp_type
                else:
                    if (comp_type != temp_type): return UNMATCH_TYPE_ERROR
                to_evaluate[1] = value
            elif (isinstance(value, bool)):
                temp_type = "bool"
                if (comp_type == ""): comp_type = temp_type
                else:
                    if (comp_type != temp_type): return UNMATCH_TYPE_ERROR
                to_evaluate[1] = value
            elif (isinstance(value, int)):
                temp_type = "integer"
                if (comp_type == ""): comp_type = temp_type
                else:
                    if (comp_type != temp_type): return UNMATCH_TYPE_ERROR
                to_evaluate[1] = value
            else:
                temp_type = "float"
                if (comp_type == ""): comp_type = temp_type
                else:
                    if (comp_type != temp_type): return UNMATCH_TYPE_ERROR
                to_evaluate[1] = value  
    elif (isinstance(comp_arguments[1], bool)):             # bool
        temp_type = "bool"
        if (comp_type == ""): comp_type = temp_type
        else:
            if (comp_type != temp_type): return UNMATCH_TYPE_ERROR
        to_evaluate[1] = comp_arguments[1]
    elif (isinstance(comp_arguments[1], int)):             # integer
        temp_type = "integer"
        if (comp_type == ""): comp_type = temp_type
        else:
            if (comp_type != temp_type): 
                return UNMATCH_TYPE_ERROR
        to_evaluate[1] = comp_arguments[1]
    else:                                   # float
        temp_type = "float"
        if (comp_type == ""): comp_type = temp_type
        else:
            if (comp_type != temp_type): return UNMATCH_TYPE_ERROR
        to_evaluate[1] = comp_arguments[1]  

    # ============= second value ===================
    if (isinstance(comp_arguments[2], str)): # if string, might be a variable or a string
        if(comp_arguments[2][0] == "\""): # sure to be string
            temp_type = "string"
            if (comp_type == ""): comp_type = temp_type
            else:
                if (comp_type != temp_type): return UNMATCH_TYPE_ERROR
            to_evaluate[2] = comp_arguments[2][1:len(comp_arguments[2])-1] # removing double quotes
        else:
            value = symbolTable[comp_arguments[2]]
            if (value == None): # value is a NOOB
                return f"ERROR: (Comparison) Value of '{comp_arguments[2]}' must not be NOOB"
            else:
                if (isinstance(value, int)):
                    temp_type = "integer"
                    if (comp_type == ""): comp_type = temp_type
                    else:
                        if (comp_type != temp_type): return UNMATCH_TYPE_ERROR
                    to_evaluate[2] = value
                elif (isinstance(value, str)):
                    temp_type = "string"
                    if (comp_type == ""): comp_type = temp_type
                    else:
                        if (comp_type != temp_type): return UNMATCH_TYPE_ERROR
                    to_evaluate[2] = value
                elif (isinstance(value, bool)):
                    temp_type = "bool"
                    if (comp_type == ""): comp_type = temp_type
                    else:
                        if (comp_type != temp_type): return UNMATCH_TYPE_ERROR
                    to_evaluate[2] = value
                else:
                    temp_type = "float"
                    if (comp_type == ""): comp_type = temp_type
                    else:
                        if (comp_type != temp_type): return UNMATCH_TYPE_ERROR
                    to_evaluate[2] = value   
    elif (isinstance(comp_arguments[2], list)):       
        if(comp_arguments[2][0] in ["BOTH SAEM", "DIFFRINT"]): # if BOTH SAEM or DIFFRINT
            value = get_comparison_result(comp_arguments[2])
            if (isinstance(value, str)): 
                return value
            temp_type = "bool"
            if (comp_type == ""): comp_type = temp_type
            else:
                if (comp_type != temp_type): return UNMATCH_TYPE_ERROR
            to_evaluate[2] = value
        else: # if BIGGR OF or SMALLR OF
            value = get_comparison_value(comp_arguments[2], comp_type)  
            if (isinstance(value, str)): 
                if (len(value) > 6): 
                    if (value[:5] == "ERROR"):
                        return value
                temp_type = "string"
                if (comp_type == ""): comp_type = temp_type
                else:
                    if (comp_type != temp_type): return UNMATCH_TYPE_ERROR
                to_evaluate[2] = value
            elif (isinstance(value, bool)):
                temp_type = "bool"
                if (comp_type == ""): comp_type = temp_type
                else:
                    if (comp_type != temp_type): return UNMATCH_TYPE_ERROR
                to_evaluate[2] = value
            elif (isinstance(value, int)):
                temp_type = "integer"
                if (comp_type == ""): comp_type = temp_type
                else:
                    if (comp_type != temp_type): return UNMATCH_TYPE_ERROR
                to_evaluate[2] = value
            else:
                temp_type = "float"
                if (comp_type == ""): comp_type = temp_type
                else:
                    if (comp_type != temp_type): return UNMATCH_TYPE_ERROR
                to_evaluate[2] = value  
    elif (isinstance(comp_arguments[2], bool)):             # bool
        temp_type = "bool"
        if (comp_type == ""): comp_type = temp_type
        else:
            if (comp_type != temp_type): return UNMATCH_TYPE_ERROR
        to_evaluate[2] = comp_arguments[2]
    elif (isinstance(comp_arguments[2], int)):             # integer
        temp_type = "integer"
        if (comp_type == ""): comp_type = temp_type
        else:
            if (comp_type != temp_type): return UNMATCH_TYPE_ERROR
        to_evaluate[2] = comp_arguments[2]
    else:                                   # float
        temp_type = "float"
        if (comp_type == ""): comp_type = temp_type
        else:
            if (comp_type != temp_type): return UNMATCH_TYPE_ERROR
        to_evaluate[2] = comp_arguments[2]  

    # ====== at this point, we can now compare the value of index 1 and 2 ========
    if (comp_arguments[0] == "BIGGR OF"):
        return max(to_evaluate[1], to_evaluate[2])
    else: # SMALLR OF
        return min(to_evaluate[1], to_evaluate[2])

def get_comparison_result(line): # BOTH SAEM and DIFFRNT
    UNMATCH_TYPE_ERROR = f"ERROR: Possible errors:\n\tValues are not of the same type \n\tOne of the value is of the type NOOB \n\tTried to nest BOTH SAEM or DIFFRINT with non-TROOF value"
    comp_type = ""
    to_evaluate = [line[0], "", ""]

    # ============= first value ===================
    if (isinstance(line[1], str)): # if string, might be a variable or a string
        if(line[1][0] == "\""): # sure to be string
            temp_type = "string"
            if (comp_type == ""): comp_type = temp_type
            else:
                if (comp_type != temp_type): return UNMATCH_TYPE_ERROR
            to_evaluate[1] = line[1][1:len(line[1])-1] # removing double quotes
        else:
            value = symbolTable[line[1]]
            if (value == None): # value is a NOOB
                return f"ERROR: (Comparison) Value of '{line[1]}' must not be NOOB"
            else:
                if (isinstance(value, int)):
                    temp_type = "integer"
                    if (comp_type == ""): comp_type = temp_type
                    else:
                        if (comp_type != temp_type): return UNMATCH_TYPE_ERROR
                    to_evaluate[1] = value
                elif (isinstance(value, str)):
                    temp_type = "string"
                    if (comp_type == ""): comp_type = temp_type
                    else:
                        if (comp_type != temp_type): return UNMATCH_TYPE_ERROR
                    to_evaluate[1] = value
                elif (isinstance(value, bool)):
                    temp_type = "bool"
                    if (comp_type == ""): comp_type = temp_type
                    else:
                        if (comp_type != temp_type): return UNMATCH_TYPE_ERROR
                    to_evaluate[1] = value
                else:
                    temp_type = "float"
                    if (comp_type == ""): comp_type = temp_type
                    else:
                        if (comp_type != temp_type): return UNMATCH_TYPE_ERROR
                    to_evaluate[1] = value   
    elif (isinstance(line[1], list)):       

        if(line[1][0] in ["BOTH SAEM", "DIFFRINT"]): # if BOTH SAEM or DIFFRINT
            value = get_comparison_result(line[1])
            if (isinstance(value, str)): 
                return value
            temp_type = "bool"
            if (comp_type == ""): comp_type = temp_type
            else:
                if (comp_type != temp_type): return UNMATCH_TYPE_ERROR
            to_evaluate[1] = value
        else: # if BIGGR OF or SMALLR OF
            value = get_comparison_value(line[1], comp_type)  
            if (isinstance(value, str)): 
                if (len(value) > 6): 
                    if (value[:5] == "ERROR"):
                        return value
                temp_type = "string"
                if (comp_type == ""): comp_type = temp_type
                else:
                    if (comp_type != temp_type): return UNMATCH_TYPE_ERROR
                to_evaluate[1] = value
            elif (isinstance(value, bool)):
                temp_type = "bool"
                if (comp_type == ""): comp_type = temp_type
                else:
                    if (comp_type != temp_type): return UNMATCH_TYPE_ERROR
                to_evaluate[1] = value
            elif (isinstance(value, int)):
                temp_type = "integer"
                if (comp_type == ""): comp_type = temp_type
                else:
                    if (comp_type != temp_type): return UNMATCH_TYPE_ERROR
                to_evaluate[1] = value
            else:
                temp_type = "float"
                if (comp_type == ""): comp_type = temp_type
                else:
                    if (comp_type != temp_type): return UNMATCH_TYPE_ERROR
                to_evaluate[1] = value  
    elif (isinstance(line[1], bool)):             # bool
        temp_type = "bool"
        if (comp_type == ""): comp_type = temp_type
        else:
            if (comp_type != temp_type): return UNMATCH_TYPE_ERROR
        to_evaluate[1] = line[1]
    elif (isinstance(line[1], int)):             # integer
        temp_type = "integer"
        if (comp_type == ""): comp_type = temp_type
        else:
            if (comp_type != temp_type): return UNMATCH_TYPE_ERROR
        to_evaluate[1] = line[1]
    else:                                   # float
        temp_type = "float"
        if (comp_type == ""): comp_type = temp_type
        else:
            if (comp_type != temp_type): return UNMATCH_TYPE_ERROR
        to_evaluate[1] = line[1]  

    # ============= second value ===================
    if (isinstance(line[2], str)): # if string, might be a variable or a string
        if(line[2][0] == "\""): # sure to be string
            temp_type = "string"
            if (comp_type == ""): comp_type = temp_type
            else:
                if (comp_type != temp_type): return UNMATCH_TYPE_ERROR
            to_evaluate[2] = line[2][1:len(line[2])-1] # removing double quotes
        else:
            value = symbolTable[line[2]]
            if (value == None): # value is a NOOB
                return f"ERROR: (Comparison) Value of '{line[2]}' must not be NOOB"
            else:
                if (isinstance(value, int)):
                    temp_type = "integer"
                    if (comp_type == ""): comp_type = temp_type
                    else:
                        if (comp_type != temp_type): return UNMATCH_TYPE_ERROR
                    to_evaluate[2] = value
                elif (isinstance(value, str)):
                    temp_type = "string"
                    if (comp_type == ""): comp_type = temp_type
                    else:
                        if (comp_type != temp_type): return UNMATCH_TYPE_ERROR
                    to_evaluate[2] = value
                elif (isinstance(value, bool)):
                    temp_type = "bool"
                    if (comp_type == ""): comp_type = temp_type
                    else:
                        if (comp_type != temp_type): return UNMATCH_TYPE_ERROR
                    to_evaluate[2] = value
                else:
                    temp_type = "float"
                    if (comp_type == ""): comp_type = temp_type
                    else:
                        if (comp_type != temp_type): return UNMATCH_TYPE_ERROR
                    to_evaluate[2] = value 
    elif (isinstance(line[2], list)):       

        if(line[2][0] in ["BOTH SAEM", "DIFFRINT"]): # if BOTH SAEM or DIFFRINT
            value = get_comparison_result(line[2])
            if (isinstance(value, str)): 
                return value
            temp_type = "bool"
            if (comp_type == ""): comp_type = temp_type
            else:
                if (comp_type != temp_type): return UNMATCH_TYPE_ERROR
            to_evaluate[2] = value
        else: # if BIGGR OF or SMALLR OF
            value = get_comparison_value(line[2], comp_type)  
            if (isinstance(value, str)): 
                if (len(value) > 6): 
                    if (value[:5] == "ERROR"):
                        return value
                temp_type = "string"
                if (comp_type == ""): comp_type = temp_type
                else:
                    if (comp_type != temp_type): return UNMATCH_TYPE_ERROR
                to_evaluate[2] = value
            elif (isinstance(value, bool)):
                temp_type = "bool"
                if (comp_type == ""): comp_type = temp_type
                else:
                    if (comp_type != temp_type): return UNMATCH_TYPE_ERROR
                to_evaluate[2] = value
            elif (isinstance(value, int)):
                temp_type = "integer"
                if (comp_type == ""): comp_type = temp_type
                else:
                    if (comp_type != temp_type): return UNMATCH_TYPE_ERROR
                to_evaluate[2] = value
            else:
                temp_type = "float"
                if (comp_type == ""): comp_type = temp_type
                else:
                    if (comp_type != temp_type): return UNMATCH_TYPE_ERROR
                to_evaluate[2] = value  
    elif (isinstance(line[2], bool)):             # bool
        temp_type = "bool"
        if (comp_type == ""): comp_type = temp_type
        else:
            if (comp_type != temp_type): return UNMATCH_TYPE_ERROR
        to_evaluate[2] = line[2]
    elif (isinstance(line[2], int)):             # integer
        temp_type = "integer"
        if (comp_type == ""): comp_type = temp_type
        else:
            if (comp_type != temp_type): return UNMATCH_TYPE_ERROR
        to_evaluate[2] = line[2]
    else:                                   # float
        temp_type = "float"
        if (comp_type == ""): comp_type = temp_type
        else:
            if (comp_type != temp_type): return UNMATCH_TYPE_ERROR
        to_evaluate[2] = line[2]  

    # ====== at this point, we can now compare the value of index 1 and 2 ========
    if (line[0] == "BOTH SAEM"):
        if (to_evaluate[1] == to_evaluate[2]): return True
        else: return False
    else: # DIFFRINT
        if (to_evaluate[1] != to_evaluate[2]): return True
        else: return False

def convert_value_to_bool(value):
    if (value in ['WIN', 'FAIL']): # value is already a TROOF
        return value
    elif (isinstance(value, str)): # value is YARN
        if (len(value) > 0): return 'WIN'
        else: return 'FAIL'
    else:                          # value will now fall on either NUMBR or NUMBAR
        if (value > 0): return 'WIN'
        else: return 'FAIL'

# use this to get the value of boolean operation
def get_bool_result(line):
    if (line[0] in ["BOTH OF", "EITHER OF", "WON OF"]):
        bool_arguments = [line[0], line[1], line[2]]
        result = get_bool_result_2(bool_arguments)
    elif (line[0] == "NOT"):
        bool_arguments = [line[0], line[1]]
        result = get_bool_result_not(bool_arguments)
    else:
        result = get_bool_result_all(line)

    result = True if result=="WIN" else False

    return result

def get_bool_result_all(bool_arguments):

    for i in range(1, len(bool_arguments)-1):
        
        temp = ""
        if ((bool_arguments[i][0] == "TROOF Literal")): # if already a TROOF
            temp = bool_arguments[i][1]
        else: 
            if (bool_arguments[i][0] in ["BOTH OF", "EITHER OF", "WON OF"]): 
                temp = get_bool_result_2(bool_arguments[i])
            elif (bool_arguments[i][0] in ["NOT"]): 
                temp = get_bool_result_not(bool_arguments[i])
            elif (bool_arguments[i][0] == "NUMBR Literal"):
                if (int(bool_arguments[i][1]) > 0): temp = 'WIN'
                else: temp = 'FAIL'
            elif (bool_arguments[i][0] == "NUMBAR Literal"):
                if (float(bool_arguments[i][1]) > 0): temp = 'WIN'
                else: temp = 'FAIL'
            elif (bool_arguments[i][0] == "YARN Literal"):
                if (len(bool_arguments[i][1]) > 0): temp = 'WIN'
                else: temp = 'FAIL'
            elif (bool_arguments[i][0] == "Variable Identifier"): # get value from symbol table
                var = bool_arguments[i][1]
                if (symbolTable[var] == None): temp = 'FAIL'
                else: temp = convert_value_to_bool(symbolTable[var])
        # checker if break from loop
        x = True if temp == 'WIN' else False

        if(bool_arguments[0] == "ALL OF"): # infinite and (break if false)
            if (not x): return "FAIL" 
        else:                              # infinite or (break if true)
            if (x): return "WIN"

    if(bool_arguments[0] == "ALL OF"): # infinite and (did not break, so return true)
        return "WIN" 
    else:                              # infinite or (did not break, so return false)
        return "FAIL"

def get_bool_result_not(bool_arguments):
    second_arg = bool_arguments[1]

    # =========== second argument ============ (first operand)
    if ((second_arg[0] == "TROOF Literal")): # if already a TROOF
        bool_arguments[1] = second_arg[1]
    else:
        if (second_arg[0] in ["BOTH OF", "EITHER OF", "WON OF"]): 
            bool_arguments[1] = get_bool_result_2(second_arg)
        elif (second_arg[0] in ["NOT"]): 
            bool_arguments[1] = get_bool_result_not(second_arg)
        elif (second_arg[0] in ["ANY OF", "ALL OF"]):
            bool_arguments[1] = get_bool_result_all(second_arg)
        elif (second_arg[0] == "NUMBR Literal"):
            if (int(second_arg[1]) > 0): bool_arguments[1] = 'WIN'
            else: bool_arguments[1] = 'FAIL'
        elif (second_arg[0] == "NUMBAR Literal"):
            if (float(second_arg[1]) > 0): bool_arguments[1] = 'WIN'
            else: bool_arguments[1] = 'FAIL'
        elif (second_arg[0] == "YARN Literal"):
            if (len(second_arg[1]) > 0): bool_arguments[1] = 'WIN'
            else: bool_arguments[1] = 'FAIL'
        elif (second_arg[0] == "Variable Identifier"): # get value from symbol table
            var = second_arg[1]
            if (symbolTable[var] == None): bool_arguments[1] = 'FAIL'
            else: bool_arguments[1] = convert_value_to_bool(symbolTable[var])

    # ======= at this point, value can now be evaluated using second argument =========
    x = True if bool_arguments[1] == 'WIN' else False
    if (x): return 'FAIL'
    else: return 'WIN'
     
def get_bool_result_2(bool_arguments):
    first_arg = bool_arguments[0]
    second_arg = bool_arguments[1]
    third_arg = bool_arguments[2]

    # =========== second argument ============ (first operand)
    if ((second_arg[0] == "TROOF Literal")): # if already a TROOF
        bool_arguments[1] = second_arg[1]
    else:
        if (second_arg[0] in ["BOTH OF", "EITHER OF", "WON OF"]): # if not, do your thing
            bool_arguments[1] = get_bool_result_2(second_arg)
        elif (second_arg[0] in ["NOT"]): 
            bool_arguments[1] = get_bool_result_not(second_arg)
        elif (second_arg[0] in ["ANY OF", "ALL OF"]):
            bool_arguments[1] = get_bool_result_all(second_arg)
        elif (second_arg[0] == "NUMBR Literal"):
            if (int(second_arg[1]) > 0): bool_arguments[1] = 'WIN'
            else: bool_arguments[1] = 'FAIL'
        elif (second_arg[0] == "NUMBAR Literal"):
            if (float(second_arg[1]) > 0): bool_arguments[1] = 'WIN'
            else: bool_arguments[1] = 'FAIL'
        elif (second_arg[0] == "YARN Literal"):
            if (len(second_arg[1]) > 0): bool_arguments[1] = 'WIN'
            else: bool_arguments[1] = 'FAIL'
        elif (second_arg[0] == "Variable Identifier"): # get value from symbol table
            var = second_arg[1]
            if (symbolTable[var] == None): bool_arguments[1] = 'FAIL'
            else: bool_arguments[1] = convert_value_to_bool(symbolTable[var])

    # =========== third argument ============ (second operand)
    if ((third_arg[0] == "TROOF Literal")): # if already a TROOF
        bool_arguments[2] = third_arg[1]
    else:
        if (third_arg[0] in ["BOTH OF", "EITHER OF", "WON OF"]): # if not, do your thing
            bool_arguments[2] = get_bool_result_2(third_arg)
        elif (third_arg[0] in ["NOT"]): 
            bool_arguments[2] = get_bool_result_not(third_arg)
        elif (second_arg[0] in ["ANY OF", "ALL OF"]):
            bool_arguments[2] = get_bool_result_all(third_arg)
        elif (third_arg[0] == "NUMBR Literal"):
            if (int(third_arg[1]) > 0): bool_arguments[2] = 'WIN'
            else: bool_arguments[2] = 'FAIL'
        elif (third_arg[0] == "NUMBAR Literal"):
            if (float(third_arg[1]) > 0): bool_arguments[2] = 'WIN'
            else: bool_arguments[2] = 'FAIL'
        elif (third_arg[0] == "YARN Literal"):
            if (len(third_arg[1]) > 0): bool_arguments[2] = 'WIN'
            else: bool_arguments[2] = 'FAIL'
        elif (third_arg[0] == "Variable Identifier"): # get value from symbol table
            var = third_arg[1]
            if (symbolTable[var] == None): bool_arguments[2] = 'FAIL'
            else: bool_arguments[2] = convert_value_to_bool(symbolTable[var])

    # ======= at this point, value can now be evaluated using second and third argument =========
    x = True if bool_arguments[1] == 'WIN' else False
    y = True if bool_arguments[2] == 'WIN' else False

    if (first_arg == "BOTH OF"): # and
        if (x and y): return 'WIN'
        else: return 'FAIL'
    elif (first_arg == "EITHER OF"): # or
        if (x or y): return 'WIN'
        else: return 'FAIL'
    else:                         # fall in xor
        if (x ^ y): return 'WIN'
        else: return 'FAIL'      


def update_symbol_table(interface):
    symbolTable_list = []
    for i in symbolTable:
        elem = []
        elem.append(str(i))
        value = symbolTable[i]
        

        v_type = None
        if (value == None):
            v_type = "NOOB"
        elif (isinstance(value, str)):
            v_type = "YARN"
        elif (type(value) == int):
            v_type = "NUMBR"
        elif (type(value) == float):
            v_type = "NUMBAR"
        else:
            v_type = "TROOF"
        
        if (value == True and v_type == "TROOF"):
            elem.append("WIN")
        elif (value == False and v_type == "TROOF"):
            elem.append("FAIL")    
        else:
            elem.append(str(value))

        elem.append(v_type)
        symbolTable_list.append(elem)
    interface.show_symbol_table2(symbolTable_list)

def semantic_main(syntax, interface):
    global symbolTable
    symbolTable = {
        "IT": None
    }

    lst = syntax.getResult().get_list([])
    semanticResult = semanticAnalyze(lst, interface)

    if (semanticResult != 1):
        return semanticResult

    symbolTable_list = []
    for i in symbolTable:
        elem = []
        elem.append(str(i))
        value = symbolTable[i]
        

        v_type = None
        if (value == None):
            v_type = "NOOB"
        elif (isinstance(value, str)):
            v_type = "YARN"
        elif (type(value) == int):
            v_type = "NUMBR"
        elif (type(value) == float):
            v_type = "NUMBAR"
        else:
            v_type = "TROOF"
        
        if (value == True and v_type == "TROOF"):
            elem.append("WIN")
        elif (value == False and v_type == "TROOF"):
            elem.append("FAIL")    
        else:
            elem.append(str(value))

        elem.append(v_type)
        symbolTable_list.append(elem)

    return symbolTable_list