variables = dict
result = list

def findLexemeClass(lexemes,lexemeClass,toFind): #finding and returning the class of specific lemexe
    for i in range(len(lexemes)):
        for j in range(len(lexemes[i])):
            if lexemes[i][j] == toFind:
                return lexemeClass[i][j]

def sum_of(op1,op2):
    return op1+op2

def diff_of(op1, op2):
    return op1-op2

def produkt_of(op1,op2):
    return op1*op2

def quoshunt_of(op1,op2):
    return op1/op2

def mod_of(op1,op2):
    return op1%op2

def biggr_of(op1,op2):
    return max(op1,op2)

def smallr_of(op1,op2):
    return min (op1,op2)

def both_of(op1,op2):
    return op1 and op2

def either_of(op1,op2):
    return op1 or op2

def won_of(op1,op2):
    return (op1 or op2) and (not op1 or not op2)

def not_op(op1):
    return not op1

def both_saem(op1,op2):
    return op1 == op2

def diffrint(op1,op2):
    return op1 != op2

def parser(lexemes, lexemeClass):
    global variables, result
    variables = {'IT':18}
    result = []

    literalList = ['Yarn Literal', 'TROOF Literal', 'NUMBR Literal', 'NUMBAR Literal']
        
    skip = False        #flag for if-else
    switch = False      #flag for switch
    error = False       #flag for error
    gtfo = False        #flag for break
    

    #if the code starts in HAI
    if lexemes[0][0] == 'HAI':
        print(lexemes)
        for x in range(len(lexemes)):
            if skip == False and error == False and gtfo == False:

                #if the code does not end in KTHXBYE
                if lexemes[-1][0] != 'KTHXBYE':
                    result.append("SYNTAX ERROR: Expected KTHXBYE")
                    break

                #gimmeh option                    
                elif lexemes[x][0] == 'GIMMEH':
                    variables[lexemes[x][1]] = input("Enter entry: ")

                #visible/to print
                elif lexemes[x][0] == 'VISIBLE':
                    if len(lexemes[x]) == 2:

                        #if variable or IT print value
                        if lexemeClass[x][1] == 'Variable Identifier' or lexemeClass[x][1] == 'Temporary Variable':
                            if lexemes[x][1] in variables:
                                result.append(variables[lexemes[x][1]])
                        else:
                            result.append(lexemes[x][1])

                    elif len(lexemes[x]) > 2:
                        string = ''
                        for y in range(len(lexemes[x])-1):
                            y=y+1

                            if lexemeClass[x][y] == 'YARN Literal':
                                string = string+str(lexemes[x][y])

                            elif lexemeClass[x][y] == 'NUMBR Literal':
                                string = string+str(int(lexemes[x][y]))

                            elif lexemeClass[x][y] == 'NUMBAR Literal':
                                string = string+str(float(lexemes[x][y]))

                            elif lexemeClass[x][y] == 'Variable Identifier':
                                if lexemes[x][y] in variables:
                                    string = string+str(variables[lexemes[x][y]])

                        result.append(string)

                #i has a statement        
                elif lexemes[x][0] == 'I HAS A':
                    if len(lexemes[x]) == 2:
                        variables[lexemes[x][1]] = None

                    elif len(lexemes[x]) == 4:
                        if lexemes[x][2] == 'ITZ':
                            if lexemeClass[x][3] in literalList:
                                variables[lexemes[x][1]] = lexemes[x][3]

                            elif lexemeClass[x][3] == 'Temporary Variable':
                                variables[lexemes[x][1]] = variables['IT']

                            elif lexemeClass[x][3] == 'Variable Identifier':
                                variables[lexemes[x][1]] = variables[lexemes[x][3]]

                    elif len(lexemes[x]) > 4:
                        if lexemes[x][2] == 'ITZ':
                            if lexemeClass[x][4] == 'YARN Literal':
                                variables[lexemes[x][1]] = lexemes[x][4]

                #R operation
                elif lexemeClass[x][0] == 'Temporary Variable' or lexemeClass[x][0] == 'Variable Identifier': 
                    if lexemes[x][1] == 'R' and lexemeClass[x][2] in literalList:
                        variables[lexemes[x][0]] = lexemes[x][2]

                    elif lexemes[x][1] == 'R' and lexemeClass[x][2] in variables:
                        variables[lexemes[x][0]] = variables[lexemes[x][2]]

                #both saem operation
                elif lexemes[x][0] == 'BOTH SAEM':      
                    if len(lexemes[x]) == 4:
                        if lexemeClass[x][1] == 'NUMBR Literal' and lexemeClass[x][3] == 'NUMBR Literal':
                            if int(lexemes[x][1]) == int(lexemes[x][3]):
                                variables['IT'] = 'WIN'

                            else:
                                variables['IT'] = 'FAIL'

                        elif lexemes[x][1] in variables and lexemeClass[x][3] == 'NUMBR Literal':
                            if findLexemeClass(lexemes,lexemeClass,lexemeClass[x][1]) == 'NUMBR Literal':
                                if int(lexemes[x][1]) == int(lexemes[x][3]):
                                    variables['IT'] = 'WIN'
                                
                                else:
                                    variables['IT'] = 'FAIL'

                        elif lexemeClass[x][1] == 'NUMBR Literal' and lexemes[x][3] in variables:
                            if findLexemeClass(lexemes,lexemeClass,lexemeClass[x][3]) == 'NUMBR Literal':
                                if int(lexemes[x][1]) == int(lexemes[x][3]):
                                    variables['IT'] = 'WIN'
                                
                                else:
                                    variables['IT'] = 'FAIL'

                        elif lexemeClass[x][1] == 'NUMBAR Literal' and lexemeClass[x][3] == 'NUMBAR Literal':
                            if float(lexemes[x][1]) == float(lexemes[x][3]):
                                variables['IT'] = 'WIN'

                            else: 
                                variables['IT'] = 'FAIL'

                        elif lexemes[x][1] in variables and lexemeClass[x][3] == 'NUMBAR Literal':
                            if findLexemeClass(lexemes,lexemeClass,lexemes[x][1]) == 'NUMBAR Literal':
                                if float(lexemes[x][1]) == float(lexemes[x][3]):
                                    variables['IT'] = 'WIN'
                                
                                else:
                                    variables['IT'] = 'FAIL'
                        
                        elif lexemeClass[x][1] == 'NUMBAR Literal' and lexemes[x][3] in variables:
                            if findLexemeClass(lexemes,lexemeClass,lexemes[x][3]) == 'NUMBAR Literal':
                                if float(lexemes[x][1]) == float(lexemes[x][3]):
                                    variables['IT'] = 'WIN'
                        
                                else:
                                    variables['IT'] = 'FAIL'
                        
                        elif lexemes[x][1] in variables and lexemes[x][3] in variables:
                            if findLexemeClass(lexemes,lexemeClass,lexemes[x][1]) == findLexemeClass(lexemes,lexemeClass,lexemes[x][3]):
                                if lexemes[x][1] == lexemes[x][3]:
                                    variables['IT'] = 'WIN'
                                else:
                                    variables['IT'] = 'FAIL'
                        else:
                            result.append("SYNTAX ERROR: Comparison of two different types")
                            error = True
                
                #diffrint operation
                elif lexemes[x][0] == 'DIFFRINT':       
                    if len(lexemes[x]) == 4:
                        if lexemeClass[x][1] == 'NUMBR Literal' and lexemeClass[x][3] == 'NUMBR Literal':
                            if int(lexemes[x][1]) != int(lexemes[x][3]):
                                variables['IT'] = 'WIN'
                        
                            else:
                                variables['IT'] = 'FAIL'
                        
                        elif lexemes[x][1] in variables and lexemeClass[x][3] == 'NUMBR Literal':
                            if findLexemeClass(lexemes,lexemeClass,lexemes[x][1]) == 'NUMBR Literal':
                                if int(lexemes[x][1]) != int(lexemes[x][3]):
                                    variables['IT'] = 'WIN'
                        
                                else:
                                    variables['IT'] = 'FAIL'
                        
                        elif lexemeClass[x][1] == 'NUMBR Literal' and lexemes[x][3] in variables:
                            if findLexemeClass(lexemes,lexemeClass,lexemes[x][3]) == 'NUMBR Literal':
                                if int(lexemes[x][1]) != int(lexemes[x][3]):
                                    variables['IT'] = 'WIN'
                        
                                else:
                                    variables['IT'] = 'FAIL'
                        
                        elif lexemeClass[x][1] == 'NUMBAR Literal' and lexemeClass[x][3] == 'NUMBAR Literal':
                            if float(lexemes[x][1]) != float(lexemes[x][3]):
                                variables['IT'] = 'WIN'
                        
                            else: 
                                variables['IT'] = 'FAIL'
                        
                        elif lexemes[x][1] in variables and lexemeClass[x][3] == 'NUMBAR Literal':
                            if findLexemeClass(lexemes,lexemeClass,lexemes[x][1]) == 'NUMBAR Literal':
                                if float(lexemes[x][1]) != float(lexemes[x][3]):
                                    variables['IT'] = 'WIN'
                        
                                else:
                                    variables['IT'] = 'FAIL'
                        elif lexemeClass[x][1] == 'NUMBAR Literal' and lexemes[x][3] in variables:
                            if findLexemeClass(lexemes,lexemeClass,lexemes[x][3]) == 'NUMBAR Literal':
                                if float(lexemes[x][1]) != float(lexemes[x][3]):
                                    variables['IT'] = 'WIN'
                        
                                else:
                                    variables['IT'] = 'FAIL'
                        
                        elif lexemes[x][1] in variables and lexemes[x][3] in variables:
                            if findLexemeClass(lexemes,lexemeClass,lexemes[x][1]) == findLexemeClass(lexemes,lexemeClass,lexemes[x][3]):
                                if lexemes[x][1] != lexemes[x][3]:
                                    variables['IT'] = 'WIN'
                        
                                else:
                                    variables['IT'] = 'FAIL'
                        
                        else:
                            result.append("SYNTAX ERROR: Comparison of two different types")
                            error = True

                #both of operation
                elif lexemes[x][0] == 'BOTH OF':
                    if len(lexemes[x]) == 4:
                        if lexemeClass[x][1] == 'TROOF Literal' and lexemeClass[x][3] == 'TROOF Literal':
                            op1 = True if lexemes[x][1] == 'WIN' else False
                            op2 = True if lexemes[x][3] == 'WIN' else False
                            answer = both_of(op1,op2)
                            if answer == True:
                                variables['IT'] = 'WIN'
                            else:    
                                variables['IT'] = 'FAIL'

                #either of operation
                elif lexemes[x][0] == 'EITHER OF':
                    if len(lexemes[x]) == 4:
                        if lexemeClass[x][1] == 'TROOF Literal' and lexemeClass[x][3] == 'TROOF Literal':
                            op1 = True if lexemes[x][1] == 'WIN' else False
                            op2 = True if lexemes[x][3] == 'WIN' else False
                            answer = either_of(op1,op2)
                            if answer == True:
                                variables['IT'] = 'WIN'
                            else:    
                                variables['IT'] = 'FAIL'

                #won of operation
                elif lexemes[x][0] == 'WON OF':
                    if len(lexemes[x]) == 4:
                        if lexemeClass[x][1] == 'TROOF Literal' and lexemeClass[x][3] == 'TROOF Literal':
                            op1 = True if lexemes[x][1] == 'WIN' else False
                            op2 = True if lexemes[x][3] == 'WIN' else False
                            answer = won_of(op1,op2)
                            if answer == True:
                                variables['IT'] = 'WIN'
                            else:    
                                variables['IT'] = 'FAIL'

                #not of operation
                elif lexemes[x][0] == 'NOT':
                    if len(lexemes[x]) == 2:
                        if lexemeClass[x][1] == 'TROOF Literal':
                            op1 = True if lexemes[x][1] == 'WIN' else False
                            answer = not_op(op1)
                            if answer == True:
                                variables['IT'] = 'WIN'
                            else:    
                                variables['IT'] = 'FAIL'

                #sum of operation
                elif lexemes[x][0] == 'SUM OF':
                    if len(lexemes[x]) == 4:
                        if lexemeClass[x][1] == 'NUMBR Literal' and lexemeClass[x][3] == 'NUMBR Literal':
                            variables['IT'] = sum_of(int(lexemes[x][1]),int(lexemes[x][3]))
                        
                        elif lexemeClass[x][1] == 'NUMBAR Literal' and lexemeClass[x][3] == 'NUMBAR Literal':
                            variables['IT'] = sum_of(float(lexemes[x][1]),float(lexemes[x][3]))
                        
                        elif lexemeClass[x][1] == 'NUMBR Literal' and lexemeClass[x][3] == 'NUMBAR Literal':
                            variables['IT'] = sum_of(int(lexemes[x][1]),float(lexemes[x][3]))
                        
                        elif lexemeClass[x][1] == 'NUMBAR Literal' and lexemeClass[x][3] == 'NUMBR Literal':
                            variables['IT'] = sum_of(float(lexemes[x][1]),int(lexemes[x][3]))

                #diff of operation
                elif lexemes[x][0] == 'DIFF OF':
                    if len(lexemes[x]) == 4:
                        if lexemeClass[x][1] == 'NUMBR Literal' and lexemeClass[x][3] == 'NUMBR Literal':
                            variables['IT'] = diff_of(int(lexemes[x][1]),int(lexemes[x][3]))
                        
                        elif lexemeClass[x][1] == 'NUMBAR Literal' and lexemeClass[x][3] == 'NUMBAR Literal':
                            variables['IT'] = diff_of(float(lexemes[x][1]),float(lexemes[x][3]))
                        
                        elif lexemeClass[x][1] == 'NUMBR Literal' and lexemeClass[x][3] == 'NUMBAR Literal':
                            variables['IT'] = diff_of(int(lexemes[x][1]),float(lexemes[x][3]))
                        
                        elif lexemeClass[x][1] == 'NUMBAR Literal' and lexemeClass[x][3] == 'NUMBR Literal':
                            variables['IT'] = diff_of(float(lexemes[x][1]),int(lexemes[x][3]))

                #produkt of operation
                elif lexemes[x][0] == 'PRODUKT OF':
                    if len(lexemes[x]) == 4:
                        if lexemeClass[x][1] == 'NUMBR Literal' and lexemeClass[x][3] == 'NUMBR Literal':
                            variables['IT'] = produkt_of(int(lexemes[x][1]),int(lexemes[x][3]))
                        
                        elif lexemeClass[x][1] == 'NUMBAR Literal' and lexemeClass[x][3] == 'NUMBAR Literal':
                            variables['IT'] = produkt_of(float(lexemes[x][1]),float(lexemes[x][3]))
                        
                        elif lexemeClass[x][1] == 'NUMBR Literal' and lexemeClass[x][3] == 'NUMBAR Literal':
                            variables['IT'] = produkt_of(int(lexemes[x][1]),float(lexemes[x][3]))
                        
                        elif lexemeClass[x][1] == 'NUMBAR Literal' and lexemeClass[x][3] == 'NUMBR Literal':
                            variables['IT'] = produkt_of(float(lexemes[x][1]),int(lexemes[x][3]))

                #quoshunt of operation
                elif lexemes[x][0] == 'QUOSHUNT OF':
                    if len(lexemes[x]) == 4:
                        if lexemeClass[x][1] == 'NUMBR Literal' and lexemeClass[x][3] == 'NUMBR Literal':
                            variables['IT'] = quoshunt_of(int(lexemes[x][1]),int(lexemes[x][3]))
                        
                        elif lexemeClass[x][1] == 'NUMBAR Literal' and lexemeClass[x][3] == 'NUMBAR Literal':
                            variables['IT'] = quoshunt_of(float(lexemes[x][1]),float(lexemes[x][3]))
                        
                        elif lexemeClass[x][1] == 'NUMBR Literal' and lexemeClass[x][3] == 'NUMBAR Literal':
                            variables['IT'] = quoshunt_of(int(lexemes[x][1]),float(lexemes[x][3]))
                        
                        elif lexemeClass[x][1] == 'NUMBAR Literal' and lexemeClass[x][3] == 'NUMBR Literal':
                            variables['IT'] = quoshunt_of(float(lexemes[x][1]),int(lexemes[x][3]))

                #mod of operation
                elif lexemes[x][0] == 'MOD OF':
                    if len(lexemes[x]) == 4:
                        if lexemeClass[x][1] == 'NUMBR Literal' and lexemeClass[x][3] == 'NUMBR Literal':
                            variables['IT'] = mod_of(int(lexemes[x][1]),int(lexemes[x][3]))
                        
                        elif lexemeClass[x][1] == 'NUMBAR Literal' and lexemeClass[x][3] == 'NUMBAR Literal':
                            variables['IT'] = mod_of(float(lexemes[x][1]),float(lexemes[x][3]))
                        
                        elif lexemeClass[x][1] == 'NUMBR Literal' and lexemeClass[x][3] == 'NUMBAR Literal':
                            variables['IT'] = mod_of(int(lexemes[x][1]),float(lexemes[x][3]))
                        
                        elif lexemeClass[x][1] == 'NUMBAR Literal' and lexemeClass[x][3] == 'NUMBR Literal':
                            variables['IT'] = mod_of(float(lexemes[x][1]),int(lexemes[x][3]))
                
                #biggr of operation
                elif lexemes[x][0] == 'BIGGR OF':
                    if len(lexemes[x]) == 4:
                        if lexemeClass[x][1] == 'NUMBR Literal' and lexemeClass[x][3] == 'NUMBR Literal':
                            variables['IT'] = biggr_of(int(lexemes[x][1]),int(lexemes[x][3]))
                        
                        elif lexemeClass[x][1] == 'NUMBAR Literal' and lexemeClass[x][3] == 'NUMBAR Literal':
                            variables['IT'] = biggr_of(float(lexemes[x][1]),float(lexemes[x][3]))
                        
                        elif lexemeClass[x][1] == 'NUMBR Literal' and lexemeClass[x][3] == 'NUMBAR Literal':
                            variables['IT'] = biggr_of(int(lexemes[x][1]),float(lexemes[x][3]))
                        
                        elif lexemeClass[x][1] == 'NUMBAR Literal' and lexemeClass[x][3] == 'NUMBR Literal':
                            variables['IT'] = biggr_of(float(lexemes[x][1]),int(lexemes[x][3]))

                #smallr of operation
                elif lexemes[x][0] == 'SMALLR OF':
                    if len(lexemes[x]) == 4:
                        if lexemeClass[x][1] == 'NUMBR Literal' and lexemeClass[x][3] == 'NUMBR Literal':
                            variables['IT'] = smallr_of(int(lexemes[x][1]),int(lexemes[x][3]))
                        
                        elif lexemeClass[x][1] == 'NUMBAR Literal' and lexemeClass[x][3] == 'NUMBAR Literal':
                            variables['IT'] = smallr_of(float(lexemes[x][1]),float(lexemes[x][3]))
                        
                        elif lexemeClass[x][1] == 'NUMBR Literal' and lexemeClass[x][3] == 'NUMBAR Literal':
                            variables['IT'] = smallr_of(int(lexemes[x][1]),float(lexemes[x][3]))
                        
                        elif lexemeClass[x][1] == 'NUMBAR Literal' and lexemeClass[x][3] == 'NUMBR Literal':
                            variables['IT'] = smallr_of(float(lexemes[x][1]),int(lexemes[x][3]))       

                #if-else condition
                elif lexemes[x][0] == 'O RLY?':
                    if lexemes[x+1][0] == 'YA RLY' and variables['IT'] == 'WIN':
                        continue

                    else:
                        skip = True
                        continue

                elif lexemes[x][0] == 'NO WAI':
                    skip =  True
                    continue

                elif lexemes[x][0] == 'WTF?':
                    continue

                elif lexemes[x][0] == 'OMG':
                    if str(variables['IT']) == str(lexemes[x][1]):
                        switch = True
                        continue
                    
                    else:
                        skip = True
                        continue

                elif lexemes[x][0] == 'OIC':
                    continue

            #skip == True        
            else:
                if lexemes[x][0] == 'NO WAI':
                    skip = False

                elif lexemes[x][0] == 'OIC':
                    continue
                
                elif lexemes[x][0] == 'OMG' and str(variables['IT']) == str(lexemes[x][1]):
                    switch = True
                    skip = False
                
                elif lexemes[x][0] == 'OMGWTF' and switch == False:
                    skip = False

    #if the code does not start with HAI
    else:
        result.append("SYNTAX ERROR: Expected HAI")