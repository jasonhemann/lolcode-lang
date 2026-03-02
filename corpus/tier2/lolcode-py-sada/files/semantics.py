import keywords
import syntax
import for_input
import math 
# import ui 


undefined_error = 0
noob_error = 0
#this part is for the semantics of the arithmetic operations (SUM OF, DIFF OF, ETC.)
def arithmeticAnalyzer(varidents, arithmetic,lexeme):    
    if lexeme[0][0] in arithmetic:
        remover_index = 0
        is_float = False
        valid_checker = 0
        #this is created to remove the literal naming in lexeme and checking if it's a float or not
        while remover_index < len(lexeme):
            #tanggalin muna yung mga string delimiter para madali
            if lexeme[remover_index][1] == "String Delimiter":
                    lexeme.pop(remover_index)
                    remover_index = remover_index - 1
            elif lexeme[remover_index][1] == 'NUMBAR Literal' or lexeme[remover_index][1] == 'YARN Literal' or lexeme[remover_index][1] == 'Identifier':
                if lexeme[remover_index][1] == 'Identifier':
                    if varidents[lexeme[remover_index][0]] == 'NOOB':
                        valid_checker = 1
                        break
                    #THIS IS CREATED TO ENSURE THAT GIMME WILL NOT BE ACCEPTED HERE! 
                    elif str(varidents[lexeme[remover_index][0]]).isnumeric() == False:
                        try:
                            float_val = float(varidents[lexeme[remover_index][0]])
                            int_value = int(float_val)
                            if float_val != int_value:
                                is_float = True
                        except ValueError:
                            #end na!
                            valid_checker = 1
                            break
                    else:
                        float_value = float(varidents[lexeme[remover_index][0]])
                        int_value = int(float_value)
                        if float_value != int_value:
                            is_float = True
                else:
                    float_value = float(lexeme[remover_index][0])
                    int_value = int(float_value)
                    if float_value != int_value:
                        is_float = True
            remover_index = remover_index + 1
        arithmetic_index = 0
        operation_list = []
        values_list = []
        result = 0
        an_counter = 0
        undefined_checker = 0 

        #if mag 1 ang valid_checker ay di na siya papasok sa while loop!! 
        if valid_checker == 1:
            result = "NOOBERROR"
            return result 

        #magloloop lang siya hanggat di pa nareread yung buong line
        while arithmetic_index < len(lexeme) and valid_checker == 0:
            #THIS IS FOR CHECKING IF MAY KATABI BA SIYA OR WALA NA OPERATION (para mas madali yung pag compute)
            # OPERATOR OPERAND1 OPERAND2
            if lexeme[arithmetic_index][0] in arithmetic:
                #check 1ST OPERAND POSITION
                if lexeme[arithmetic_index+1][0] not in arithmetic:
                    #check THE 2ND OPERAND POSITION
                    if lexeme[arithmetic_index+3][0] not in arithmetic:
                        #if accepted then proceed to performing the operations!
                        if lexeme[arithmetic_index][0] == 'SUM OF':
                            #this is created to cater the variables!!!
                            if (lexeme[arithmetic_index+1][1] == 'Identifier' or lexeme[arithmetic_index+1][1] == 'Variable Identifier') and (lexeme[arithmetic_index+3][1] == 'Identifier' or lexeme[arithmetic_index+3][1] == 'Variable Identifier'):                                        
                                result = float(varidents[lexeme[arithmetic_index+1][0]])+float(varidents[lexeme[arithmetic_index+3][0]])
                            elif lexeme[arithmetic_index+1][1] == 'Identifier' or lexeme[arithmetic_index+1][1] == 'Variable Identifier':
                                result = float(varidents[lexeme[arithmetic_index+1][0]])+float(lexeme[arithmetic_index+3][0])
                            elif lexeme[arithmetic_index+3][1] == 'Identifier' or lexeme[arithmetic_index+3][1] == 'Variable Identifier':
                                result = float(lexeme[arithmetic_index+1][0])+float(varidents[lexeme[arithmetic_index+3][0]])
                            #THIS ONE IS FOR THE TROOFS
                            elif lexeme[arithmetic_index+1][1] == 'TROOF Literal' and lexeme[arithmetic_index+3][1] == 'TROOF Literal':
                                if lexeme[arithmetic_index+1][0] == 'WIN' and lexeme[arithmetic_index+3][0] == 'WIN':
                                    result = float(1)+float(1)
                                elif lexeme[arithmetic_index+1][0] == 'WIN' and lexeme[arithmetic_index+3][0] == 'FAIL':
                                    result = float(1)+float(0)
                                elif lexeme[arithmetic_index+1][0] == 'FAIL' and lexeme[arithmetic_index+3][0] == 'WIN':
                                    result = float(0)+float(1)
                                elif lexeme[arithmetic_index+1][0] == 'FAIL' and lexeme[arithmetic_index+3][0] == 'FAIL':
                                    result = float(0)+float(0)
                            elif lexeme[arithmetic_index+1][1] == 'TROOF Literal':
                                if lexeme[arithmetic_index+1][0] == 'WIN':
                                    result = float(1)+float(lexeme[arithmetic_index+3][0])
                                else:
                                    result = float(0)+float(lexeme[arithmetic_index+3][0])
                            elif lexeme[arithmetic_index+3][1] == 'TROOF Literal':
                                if lexeme[arithmetic_index+3][0] == 'WIN':
                                    result =float(lexeme[arithmetic_index+1][0])+ float(1)
                                else:
                                    result = float(lexeme[arithmetic_index+1][0])+float(0)
                            else:
                                result = float(lexeme[arithmetic_index+1][0])+float(lexeme[arithmetic_index+3][0])
                        elif lexeme[arithmetic_index][0] == 'DIFF OF':
                            #this is created to cater the variables!!!
                            if (lexeme[arithmetic_index+1][1] == 'Identifier' or lexeme[arithmetic_index+1][1] == 'Variable Identifier') and (lexeme[arithmetic_index+3][1] == 'Identifier' or lexeme[arithmetic_index+3][1] == 'Variable Identifier'):                                        
                                result = float(varidents[lexeme[arithmetic_index+1][0]])-float(varidents[lexeme[arithmetic_index+3][0]])
                            elif lexeme[arithmetic_index+1][1] == 'Identifier' or lexeme[arithmetic_index+1][1] == 'Variable Identifier':
                                result = float(varidents[lexeme[arithmetic_index+1][0]])-float(lexeme[arithmetic_index+3][0])
                            elif lexeme[arithmetic_index+3][1] == 'Identifier' or lexeme[arithmetic_index+3][1] == 'Variable Identifier':
                                result = float(lexeme[arithmetic_index+1][0])-float(varidents[lexeme[arithmetic_index+3][0]])
                            #THIS ONE IS FOR THE TROOFS
                            elif lexeme[arithmetic_index+1][1] == 'TROOF Literal' and lexeme[arithmetic_index+3][1] == 'TROOF Literal':
                                if lexeme[arithmetic_index+1][0] == 'WIN' and lexeme[arithmetic_index+3][0] == 'WIN':
                                    result = float(1)-float(1)
                                elif lexeme[arithmetic_index+1][0] == 'WIN' and lexeme[arithmetic_index+3][0] == 'FAIL':
                                    result = float(1)-float(0)
                                elif lexeme[arithmetic_index+1][0] == 'FAIL' and lexeme[arithmetic_index+3][0] == 'WIN':
                                    result = float(0)-float(1)
                                elif lexeme[arithmetic_index+1][0] == 'FAIL' and lexeme[arithmetic_index+3][0] == 'FAIL':
                                    result = float(0)-float(0)
                            elif lexeme[arithmetic_index+1][1] == 'TROOF Literal':
                                if lexeme[arithmetic_index+1][0] == 'WIN':
                                    result = float(1)-float(lexeme[arithmetic_index+3][0])
                                else:
                                    result = float(0)-float(lexeme[arithmetic_index+3][0])
                            elif lexeme[arithmetic_index+3][1] == 'TROOF Literal':
                                if lexeme[arithmetic_index+3][0] == 'WIN':
                                    result =float(lexeme[arithmetic_index+1][0])-float(1)
                                else:
                                    result = float(lexeme[arithmetic_index+1][0])-float(0)
                            else:
                                result = float(lexeme[arithmetic_index+1][0]) - float(lexeme[arithmetic_index+3][0])
                        elif lexeme[arithmetic_index][0] == 'PRODUKT OF':
                            #this is created to cater the variables!!!
                            if (lexeme[arithmetic_index+1][1] == 'Identifier' or lexeme[arithmetic_index+1][1] == 'Variable Identifier') and (lexeme[arithmetic_index+3][1] == 'Identifier' or lexeme[arithmetic_index+3][1] == 'Variable Identifier'):                                        
                                result = float(varidents[lexeme[arithmetic_index+1][0]])*float(varidents[lexeme[arithmetic_index+3][0]])
                            elif lexeme[arithmetic_index+1][1] == 'Identifier' or lexeme[arithmetic_index+1][1] == 'Variable Identifier':
                                result = float(varidents[lexeme[arithmetic_index+1][0]])*float(lexeme[arithmetic_index+3][0])
                            elif lexeme[arithmetic_index+3][1] == 'Identifier' or lexeme[arithmetic_index+3][1] == 'Variable Identifier':
                                result = float(lexeme[arithmetic_index+1][0])*float(varidents[lexeme[arithmetic_index+3][0]])
                            #THIS ONE IS FOR THE TROOFS
                            elif lexeme[arithmetic_index+1][1] == 'TROOF Literal' and lexeme[arithmetic_index+3][1] == 'TROOF Literal':
                                if lexeme[arithmetic_index+1][0] == 'WIN' and lexeme[arithmetic_index+3][0] == 'WIN':
                                    result = float(1)*float(1)
                                elif lexeme[arithmetic_index+1][0] == 'WIN' and lexeme[arithmetic_index+3][0] == 'FAIL':
                                    result = float(1)*float(0)
                                elif lexeme[arithmetic_index+1][0] == 'FAIL' and lexeme[arithmetic_index+3][0] == 'WIN':
                                    result = float(0)*float(1)
                                elif lexeme[arithmetic_index+1][0] == 'FAIL' and lexeme[arithmetic_index+3][0] == 'FAIL':
                                    result = float(0)*float(0)
                            elif lexeme[arithmetic_index+1][1] == 'TROOF Literal':
                                if lexeme[arithmetic_index+1][0] == 'WIN':
                                    result = float(1)*float(lexeme[arithmetic_index+3][0])
                                else:
                                    result = float(0)*float(lexeme[arithmetic_index+3][0])
                            elif lexeme[arithmetic_index+3][1] == 'TROOF Literal':
                                if lexeme[arithmetic_index+3][0] == 'WIN':
                                    result =float(lexeme[arithmetic_index+1][0])*float(1)
                                else:
                                    result = float(lexeme[arithmetic_index+1][0])*float(0)
                            else:
                                result = float(lexeme[arithmetic_index+1][0]) * float(lexeme[arithmetic_index+3][0])
                        elif lexeme[arithmetic_index][0] == 'QUOSHUNT OF':
                            #this is created to cater the variables!!!
                            if (lexeme[arithmetic_index+1][1] == 'Identifier' or lexeme[arithmetic_index+1][1] == 'Variable Identifier') and (lexeme[arithmetic_index+3][1] == 'Identifier' or lexeme[arithmetic_index+3][1] == 'Variable Identifier'):
                                if math.ceil(float(varidents[lexeme[arithmetic_index+3][0]])) == 0 or varidents[lexeme[arithmetic_index+3][0]] == '0':
                                    undefined_checker = 1
                                    break
                                else:                                        
                                    result = float(varidents[lexeme[arithmetic_index+1][0]]) / float(varidents[lexeme[arithmetic_index+3][0]])
                            elif lexeme[arithmetic_index+1][1] == 'Identifier' or lexeme[arithmetic_index+1][1] == 'Variable Identifier':
                                result = float(varidents[lexeme[arithmetic_index+1][0]]) / float(lexeme[arithmetic_index+3][0])
                            elif lexeme[arithmetic_index+3][1] == 'Identifier' or lexeme[arithmetic_index+3][1] == 'Variable Identifier':
                                if math.ceil(float(varidents[lexeme[arithmetic_index+3][0]])) == 0 or varidents[lexeme[arithmetic_index+3][0]] == '0':
                                    undefined_checker = 1
                                    break
                                else:  
                                    result = float(lexeme[arithmetic_index+1][0]) / float(varidents[lexeme[arithmetic_index+3][0]])
                            #THIS ONE IS FOR THE TROOFS
                            elif lexeme[arithmetic_index+1][1] == 'TROOF Literal' and lexeme[arithmetic_index+3][1] == 'TROOF Literal':
                                if lexeme[arithmetic_index+1][0] == 'WIN' and lexeme[arithmetic_index+3][0] == 'WIN':
                                    result = float(1)/float(1)
                                elif lexeme[arithmetic_index+1][0] == 'WIN' and lexeme[arithmetic_index+3][0] == 'FAIL':
                                    undefined_checker = 1
                                    break
                                elif lexeme[arithmetic_index+1][0] == 'FAIL' and lexeme[arithmetic_index+3][0] == 'WIN':
                                    result = float(0)/float(1)
                                elif lexeme[arithmetic_index+1][0] == 'FAIL' and lexeme[arithmetic_index+3][0] == 'FAIL':
                                    undefined_checker = 1
                                    break
                            elif lexeme[arithmetic_index+1][1] == 'TROOF Literal':
                                if lexeme[arithmetic_index+1][0] == 'WIN':
                                    result = float(1)/float(lexeme[arithmetic_index+3][0])
                                else:
                                    result = float(0)/float(lexeme[arithmetic_index+3][0])
                            elif lexeme[arithmetic_index+3][1] == 'TROOF Literal':
                                if lexeme[arithmetic_index+3][0] == 'WIN':
                                    result =float(lexeme[arithmetic_index+1][0])/float(1)
                                else:
                                    undefined_checker = 1
                                    break 
                            else:
                                if math.ceil(float(lexeme[arithmetic_index+3][0])) == 0 or lexeme[arithmetic_index+3][0] == "0":
                                    undefined_checker = 1
                                    break 
                                else:
                                    result = float(lexeme[arithmetic_index+1][0]) / float(lexeme[arithmetic_index+3][0])
                        elif lexeme[arithmetic_index][0] == 'MOD OF':
                            #this is created to cater the variables!!!
                            if (lexeme[arithmetic_index+1][1] == 'Identifier' or lexeme[arithmetic_index+1][1] == 'Variable Identifier') and (lexeme[arithmetic_index+3][1] == 'Identifier' or lexeme[arithmetic_index+3][1] == 'Variable Identifier'):                                        
                                result = float(varidents[lexeme[arithmetic_index+1][0]]) % float(varidents[lexeme[arithmetic_index+3][0]])
                            elif lexeme[arithmetic_index+1][1] == 'Identifier' or lexeme[arithmetic_index+1][1] == 'Variable Identifier':
                                result = float(varidents[lexeme[arithmetic_index+1][0]]) % float(lexeme[arithmetic_index+3][0])
                            elif lexeme[arithmetic_index+3][1] == 'Identifier' or lexeme[arithmetic_index+3][1] == 'Variable Identifier':
                                result = float(lexeme[arithmetic_index+1][0]) % float(varidents[lexeme[arithmetic_index+3][0]])
                            #THIS ONE IS FOR THE TROOFS
                            elif lexeme[arithmetic_index+1][1] == 'TROOF Literal' and lexeme[arithmetic_index+3][1] == 'TROOF Literal':
                                if lexeme[arithmetic_index+1][0] == 'WIN' and lexeme[arithmetic_index+3][0] == 'WIN':
                                    result = float(1)%float(1)
                                elif lexeme[arithmetic_index+1][0] == 'WIN' and lexeme[arithmetic_index+3][0] == 'FAIL':
                                    result = float(1)%float(0)
                                elif lexeme[arithmetic_index+1][0] == 'FAIL' and lexeme[arithmetic_index+3][0] == 'WIN':
                                    result = float(0)%float(1)
                                elif lexeme[arithmetic_index+1][0] == 'FAIL' and lexeme[arithmetic_index+3][0] == 'FAIL':
                                    result = float(0)%float(0)
                            elif lexeme[arithmetic_index+1][1] == 'TROOF Literal':
                                if lexeme[arithmetic_index+1][0] == 'WIN':
                                    result = float(1)%float(lexeme[arithmetic_index+3][0])
                                else:
                                    result = float(0)%float(lexeme[arithmetic_index+3][0])
                            elif lexeme[arithmetic_index+3][1] == 'TROOF Literal':
                                if lexeme[arithmetic_index+3][0] == 'WIN':
                                    result =float(lexeme[arithmetic_index+1][0])%float(1)
                                else:
                                    result = float(lexeme[arithmetic_index+1][0])%float(0)
                            else:
                                result = float(lexeme[arithmetic_index+1][0]) % float(lexeme[arithmetic_index+3][0])
                        elif lexeme[arithmetic_index][0] == 'BIGGR OF':
                            #this is created to cater the variables!!!
                            if (lexeme[arithmetic_index+1][1] == 'Identifier' or lexeme[arithmetic_index+1][1] == 'Variable Identifier') and (lexeme[arithmetic_index+3][1] == 'Identifier' or lexeme[arithmetic_index+3][1] == 'Variable Identifier'):
                                if float(varidents[lexeme[arithmetic_index+1][0]]) > float(varidents[lexeme[arithmetic_index+3][0]]):
                                    result = float(varidents[lexeme[arithmetic_index+1][0]])
                                else:
                                    result = float(varidents[lexeme[arithmetic_index+3][0]])
                            elif lexeme[arithmetic_index+1][1] == 'Identifier' or lexeme[arithmetic_index+1][1] == 'Variable Identifier':
                                if float(varidents[lexeme[arithmetic_index+1][0]]) > float(lexeme[arithmetic_index+3][0]):
                                    result = float(varidents[lexeme[arithmetic_index+1][0]])
                                else:
                                    result = float(lexeme[arithmetic_index+3][0])
                            elif lexeme[arithmetic_index+3][1] == 'Identifier' or lexeme[arithmetic_index+3][1] == 'Variable Identifier':
                                if float(lexeme[arithmetic_index+1][0]) > float(varidents[lexeme[arithmetic_index+3][0]]):
                                    result = float(lexeme[arithmetic_index+1][0]) 
                                else:
                                    result = float(varidents[lexeme[arithmetic_index+3][0]])
                            #THIS ONE IS FOR THE TROOFS
                            elif lexeme[arithmetic_index+1][1] == 'TROOF Literal' and lexeme[arithmetic_index+3][1] == 'TROOF Literal':
                                if lexeme[arithmetic_index+1][0] == 'WIN' and lexeme[arithmetic_index+3][0] == 'WIN':
                                    result = float(1)
                                elif lexeme[arithmetic_index+1][0] == 'WIN' and lexeme[arithmetic_index+3][0] == 'FAIL':
                                    result = float(1)
                                elif lexeme[arithmetic_index+1][0] == 'FAIL' and lexeme[arithmetic_index+3][0] == 'WIN':
                                    result = float(1)
                                elif lexeme[arithmetic_index+1][0] == 'FAIL' and lexeme[arithmetic_index+3][0] == 'FAIL':
                                    result = float(0)
                            elif lexeme[arithmetic_index+1][1] == 'TROOF Literal':
                                if lexeme[arithmetic_index+1][0] == 'WIN':
                                    if  float(1) > float(lexeme[arithmetic_index+3][0]):
                                        result = float(1)
                                    else: 
                                        result = float(lexeme[arithmetic_index+3][0])
                                else:
                                    if  float(0) > float(lexeme[arithmetic_index+3][0]):
                                        result = float(0)
                                    else: 
                                        result = float(lexeme[arithmetic_index+3][0])
                            elif lexeme[arithmetic_index+3][1] == 'TROOF Literal':
                                if lexeme[arithmetic_index+3][0] == 'WIN':
                                    if float(lexeme[arithmetic_index+1][0]) < float(1):
                                        result = float(1)
                                    else:
                                        result = float(lexeme[arithmetic_index+1][0]) 
                                else:
                                    if float(lexeme[arithmetic_index+1][0]) < float(0):
                                        result = float(0)
                                    else:
                                        result = float(lexeme[arithmetic_index+1][0])
                            else:
                                if float(lexeme[arithmetic_index+1][0]) > float(lexeme[arithmetic_index+3][0]):
                                    result = float(lexeme[arithmetic_index+1][0])
                                else:
                                    result = float(lexeme[arithmetic_index+3][0])
                        elif lexeme[arithmetic_index][0] == 'SMALLR OF':
                            #this is created to cater the variables!!!
                            if (lexeme[arithmetic_index+1][1] == 'Identifier' or lexeme[arithmetic_index+1][1] == 'Variable Identifier') and (lexeme[arithmetic_index+3][1] == 'Identifier' or lexeme[arithmetic_index+3][1] == 'Variable Identifier'):
                                if float(varidents[lexeme[arithmetic_index+1][0]]) < float(varidents[lexeme[arithmetic_index+3][0]]):
                                    result = float(varidents[lexeme[arithmetic_index+1][0]])
                                else:
                                    result = float(varidents[lexeme[arithmetic_index+3][0]])
                            elif lexeme[arithmetic_index+1][1] == 'Identifier' or lexeme[arithmetic_index+1][1] == 'Variable Identifier':
                                if float(varidents[lexeme[arithmetic_index+1][0]]) < float(lexeme[arithmetic_index+3][0]):
                                    result = float(varidents[lexeme[arithmetic_index+1][0]])
                                else:
                                    result = float(lexeme[arithmetic_index+3][0])
                            elif lexeme[arithmetic_index+3][1] == 'Identifier' or lexeme[arithmetic_index+3][1] == 'Variable Identifier':
                                if float(lexeme[arithmetic_index+1][0]) < float(varidents[lexeme[arithmetic_index+3][0]]):
                                    result = float(lexeme[arithmetic_index+1][0]) 
                                else:
                                    result = float(varidents[lexeme[arithmetic_index+3][0]])
                            #THIS ONE IS FOR THE TROOFS
                            elif lexeme[arithmetic_index+1][1] == 'TROOF Literal' and lexeme[arithmetic_index+3][1] == 'TROOF Literal':
                                if lexeme[arithmetic_index+1][0] == 'WIN' and lexeme[arithmetic_index+3][0] == 'WIN':
                                    result = float(1)
                                elif lexeme[arithmetic_index+1][0] == 'WIN' and lexeme[arithmetic_index+3][0] == 'FAIL':
                                    result = float(0)
                                elif lexeme[arithmetic_index+1][0] == 'FAIL' and lexeme[arithmetic_index+3][0] == 'WIN':
                                    result = float(0)
                                elif lexeme[arithmetic_index+1][0] == 'FAIL' and lexeme[arithmetic_index+3][0] == 'FAIL':
                                    result = float(0)
                            elif lexeme[arithmetic_index+1][1] == 'TROOF Literal':
                                if lexeme[arithmetic_index+1][0] == 'WIN':
                                    if  float(1) < float(lexeme[arithmetic_index+3][0]):
                                        result = float(1)
                                    else: 
                                        result = float(lexeme[arithmetic_index+3][0])
                                else:
                                    if  float(0) < float(lexeme[arithmetic_index+3][0]):
                                        result = float(0)
                                    else: 
                                        result = float(lexeme[arithmetic_index+3][0])
                            elif lexeme[arithmetic_index+3][1] == 'TROOF Literal':
                                if lexeme[arithmetic_index+3][0] == 'WIN':
                                    if float(lexeme[arithmetic_index+1][0]) > float(1):
                                        result = float(1)
                                    else:
                                        result = float(lexeme[arithmetic_index+1][0]) 
                                else:
                                    if float(lexeme[arithmetic_index+1][0]) > float(0):
                                        result = float(0)
                                    else:
                                        result = float(lexeme[arithmetic_index+1][0])
                            else:
                                if float(lexeme[arithmetic_index+1][0]) < float(lexeme[arithmetic_index+3][0]):
                                    result = float(lexeme[arithmetic_index+1][0]) 
                                else:
                                    result = float(lexeme[arithmetic_index+3][0])
                        arithmetic_index = arithmetic_index + 4
                    else:
                        operation_list.append(lexeme[arithmetic_index][0])
                        if lexeme[arithmetic_index+1][0] in varidents:
                            values_list.append(float(varidents[lexeme[arithmetic_index+1][0]]))
                        else:
                            values_list.append(float(lexeme[arithmetic_index+1][0])) 
                        arithmetic_index = arithmetic_index + 3
                        an_counter = an_counter + 1
                else:
                    operation_list.append(lexeme[arithmetic_index][0])
                    arithmetic_index = arithmetic_index + 1                          
            elif lexeme[arithmetic_index][0] == 'AN':
                if lexeme[arithmetic_index+1][0] not in arithmetic:
                    if operation_list[-1] == 'SUM OF':
                        if lexeme[arithmetic_index+1][1] == "Identifier" or lexeme[arithmetic_index+1][1] == "Variable Identifier":
                            result = result + float(varidents[lexeme[arithmetic_index+1][0]])
                        elif lexeme[arithmetic_index+1][1] == "TROOF Literal":
                            if lexeme[arithmetic_index+1][0] == 'WIN':
                                result = result + 1
                            else:
                                result = result + 0
                        else:
                            result = result + float(lexeme[arithmetic_index+1][0])
                    elif operation_list[-1] == 'DIFF OF':
                        if lexeme[arithmetic_index+1][1] == "Identifier" or lexeme[arithmetic_index+1][1] == "Variable Identifier":
                            result = result - float(varidents[lexeme[arithmetic_index+1][0]])
                        elif lexeme[arithmetic_index+1][1] == "TROOF Literal":
                            if lexeme[arithmetic_index+1][0] == 'WIN':
                                result = result - 1
                            else:
                                result = result - 0                        
                        else:
                            result = result - float(lexeme[arithmetic_index+1][0])
                    elif operation_list[-1] == 'PRODUKT OF':
                        if lexeme[arithmetic_index+1][1] == "Identifier" or lexeme[arithmetic_index+1][1] == "Variable Identifier":
                            result = result * float(varidents[lexeme[arithmetic_index+1][0]])
                        elif lexeme[arithmetic_index+1][1] == "TROOF Literal":
                            if lexeme[arithmetic_index+1][0] == 'WIN':
                                result = result * 1
                            else:
                                result = result * 0                        
                        else:
                            result = result * float(lexeme[arithmetic_index+1][0])
                    elif operation_list[-1] == 'QUOSHUNT OF':
                        if lexeme[arithmetic_index+1][1] == "Identifier" or lexeme[arithmetic_index+1][1] == "Variable Identifier":
                            #check if 0 ba siya 
                            if math.ceil(float(varidents[arithmetic_index+1][0])) == 0 or varidents[arithmetic_index+1][0] == "0":
                                undefined_checker = 1
                                break
                            else:
                                result = result / float(varidents[lexeme[arithmetic_index+1][0]])
                        elif lexeme[arithmetic_index+1][1] == "TROOF Literal":
                            if lexeme[arithmetic_index+1][0] == 'WIN':
                                result = result / 1
                            else:
                                undefined_checker = 1
                                break 
                        else:
                            result = result / float(lexeme[arithmetic_index+1][0])
                    elif operation_list[-1] == 'MOD OF':
                        if lexeme[arithmetic_index+1][1] == "Identifier" or lexeme[arithmetic_index+1][1] == "Variable Identifier":
                            result = result % float(varidents[lexeme[arithmetic_index+1][0]])
                        elif lexeme[arithmetic_index+1][1] == "TROOF Literal":
                            if lexeme[arithmetic_index+1][0] == 'WIN':
                                result = result % 1
                            else:
                                result = result % 0
                        else:
                            result = result % float(lexeme[arithmetic_index+1][0])
                    elif operation_list[-1] == 'BIGGR OF':
                        if lexeme[arithmetic_index+1][1] == "Identifier" or lexeme[arithmetic_index+1][1] == "Variable Identifier":
                            if result < float(varidents[lexeme[arithmetic_index+1][0]]):
                                result = float(varidents[lexeme[arithmetic_index+1][0]])
                        elif lexeme[arithmetic_index+1][1] == "TROOF Literal":
                            if lexeme[arithmetic_index+1][0] == 'WIN':
                                if float(1) > result:
                                    result = float(1)
                            else:
                                if float(0) > result:
                                    result = float(0)
                        else:
                            if result < float(lexeme[arithmetic_index+1][0]):
                                result = float(lexeme[arithmetic_index+1][0])
                    elif operation_list[-1] == 'SMALLR OF':
                        if lexeme[arithmetic_index+1][1] == "Identifier" or lexeme[arithmetic_index+1][1] == "Variable Identifier":
                            if result > float(varidents[lexeme[arithmetic_index+1][0]]):  
                                result = float(varidents[lexeme[arithmetic_index+1][0]])
                        elif lexeme[arithmetic_index+1][1] == "TROOF Literal":
                            if lexeme[arithmetic_index+1][0] == 'WIN':
                                if float(1) < result:
                                    result = float(1)
                            else:
                                if float(0) < result:
                                    result = float(0)
                        else:
                            if result > float(lexeme[arithmetic_index+1][0]):  
                                result = float(lexeme[arithmetic_index+1][0])
                    operation_list.pop(-1)                                        
                    arithmetic_index = arithmetic_index +2
                else:
                    an_counter = an_counter + 1
                    arithmetic_index = arithmetic_index + 1
                    values_list.append(result)
                    result = 0

        #this one is created to cater yung mga nauna  (SUM OF SUM OF 3 AN 4 AN DIFF OF 3 AN 2)
        #parang nag babacktracking kana dito 
        is_onelement = 0
        if an_counter == 1:
            is_onelement = 1
            an_counter = 2

        for i in range (an_counter):
            if operation_list[-(1+i)] == 'SUM OF':
                result = values_list[-(1+i)] + result   
            elif operation_list[-(1+i)] == 'DIFF OF':
                result = values_list[-(1+i)] - result 
            elif operation_list[-(1+i)] == 'PRODUKT OF':
                result = values_list[-(1+i)] * result                           
            elif operation_list[-(1+i)] == 'QUOSHUNT OF':
                if math.ceil(float(values_list[-(1+i)])) == 0:
                    undefined_checker = 1
                    break
                else:
                    result = values_list[-(1+i)] / result                  
            elif operation_list[-(1+i)] == 'MOD OF':
                result = values_list[-(1+i)] % result                      
            elif operation_list[-(1+i)] == 'BIGGR OF':
                if values_list[-(1+i)] > result:
                    result = values_list[-(1+i)]                       
            elif operation_list[-(1+i)] == 'SMALLR OF':
                if values_list[-(1+i)] < result:
                    result = values_list[-(1+i)]
            if is_onelement == 1:
                break

        #check if may undefined result
        if undefined_checker == 1:
            result = "UNDEFINEDERROR"
            return result
        #proceed to checking if float or int
        if is_float == False :
            semanticsResult = f"{int(result)}"
        else:
            semanticsResult = f"{result}"
        return semanticsResult

def booleanAnalyzer(thisLexeme, isInfinite):
    boolean_index = 0
    boolean_list = []
    boolean_operands = []
    while boolean_index < len(thisLexeme):
        if thisLexeme[boolean_index][0] in ['BOTH OF', 'EITHER OF', 'WON OF']:
            boolean_list.append(thisLexeme[boolean_index][0])
            if thisLexeme[boolean_index+1][1] == 'TROOF Literal':
                if thisLexeme[boolean_index+1][0] == 'WIN':
                    boolean_operands.append(f'WIN')
                elif thisLexeme[boolean_index+1][0] == 'FAIL':
                    boolean_operands.append(f'FAIL')
                elif varidents[thisLexeme[boolean_index+1][0]] != 'NOOB' or f'{int(float(thisLexeme[boolean_index+1][0]))}' != '0':
                    boolean_operands.append('WIN')
                else:
                    boolean_operands.append('FAIL')
            elif thisLexeme[boolean_index+1][1] == 'Identifier':
                if varidents[thisLexeme[boolean_index+1][0]] == 'WIN':
                    boolean_operands.append(f'WIN')
                elif varidents[thisLexeme[boolean_index+1][0]] == 'FAIL':
                    boolean_operands.append(f'FAIL')
                elif varidents[thisLexeme[boolean_index+1][0]] != 'NOOB' or f'{int(float(varidents[thisLexeme[boolean_index+1][0]]))}' != '0':
                    boolean_operands.append('WIN')
                else:
                    boolean_operands.append('FAIL')
            elif thisLexeme[boolean_index+1][0] in booleans:
                boolean_index += 1
                continue

            if thisLexeme[boolean_index+3][1] == 'TROOF Literal':
                if thisLexeme[boolean_index+3][0] == 'WIN':
                    boolean_operands.append(f'WIN')
                elif thisLexeme[boolean_index+3][0] == 'FAIL':
                    boolean_operands.append(f'FAIL')
                elif varidents[thisLexeme[boolean_index+3][0]] != 'NOOB' or f'{int(float(thisLexeme[boolean_index+3][0]))}' != '0':
                    boolean_operands.append('WIN')
                else:
                    boolean_operands.append('FAIL')
            elif thisLexeme[boolean_index+3][1] == 'Identifier':
                if varidents[thisLexeme[boolean_index+3][0]] == 'WIN':
                    boolean_operands.append(f'WIN')
                elif varidents[thisLexeme[boolean_index+3][0]] == 'FAIL':
                    boolean_operands.append(f'FAIL')
                elif varidents[thisLexeme[boolean_index+3][0]] != 'NOOB' or f'{int(float(varidents[thisLexeme[boolean_index+3][0]]))}' != '0':
                    boolean_operands.append('WIN')
                else:
                    boolean_operands.append('FAIL')
            elif thisLexeme[boolean_index+3][0] in booleans:
                boolean_index += 3
                continue
            boolean_index += 5
        elif thisLexeme[boolean_index][0] == 'NOT':
            if thisLexeme[boolean_index+1][1] == 'TROOF Literal':
                if thisLexeme[boolean_index+1][0] == 'WIN':
                    boolean_operands.append(f'FAIL')
                elif thisLexeme[boolean_index+1][0] == 'FAIL':
                    boolean_operands.append(f'WIN')
                elif varidents[thisLexeme[boolean_index+1][0]] != 'NOOB' or f'{int(float(thisLexeme[boolean_index+1][0]))}' != '0':
                    boolean_operands.append('FAIL')
                else:
                    boolean_operands.append('WIN')
            elif thisLexeme[boolean_index+1][1] == 'Identifier':
                if varidents[thisLexeme[boolean_index+1][0]] == 'WIN':
                    boolean_operands.append(f'FAIL')
                elif varidents[thisLexeme[boolean_index+1][0]] == 'FAIL':
                    boolean_operands.append(f'WIN')
                elif varidents[thisLexeme[boolean_index+1][0]] != 'NOOB' or f'{int(float(varidents[thisLexeme[boolean_index+1][0]]))}' != '0':
                    boolean_operands.append('FAIL')
                else:
                    boolean_operands.append('WIN')
            elif thisLexeme[boolean_index+1][0] in ['BOTH OF', 'EITHER OF', 'WON OF']:
                boolean_list.append('NOT')
                boolean_index += 1
                continue
            elif thisLexeme[boolean_index+1][0] == 'NOT':
                boolean_index += 2
                continue
            boolean_index += 3
        else:
            if thisLexeme[boolean_index][1] == 'TROOF Literal':
                if thisLexeme[boolean_index][0] == 'WIN':
                    boolean_operands.append(f'WIN')
                elif thisLexeme[boolean_index][0] == 'FAIL':
                    boolean_operands.append(f'FAIL')
                elif f'{int(float(thisLexeme[boolean_index][0]))}' != '0':
                    boolean_operands.append('WIN')
                else:
                    boolean_operands.append('FAIL')
            elif thisLexeme[boolean_index][1] == 'Identifier':
                if varidents[thisLexeme[boolean_index][0]] == 'WIN':
                    boolean_operands.append(f'WIN')
                elif varidents[thisLexeme[boolean_index][0]] == 'FAIL':
                    boolean_operands.append(f'FAIL')
                elif f'{int(float(varidents[thisLexeme[boolean_index][0]]))}' != '0':
                    boolean_operands.append('WIN')
                else:
                    boolean_operands.append('FAIL')
            boolean_index += 2

    answer = ''
    if len(boolean_list) == 0:
        answer = boolean_operands[0]
    else:
        for i in range(len(boolean_list)-1, -1, -1):
            if boolean_list[i] == 'BOTH OF':
                if boolean_operands[-1] == 'WIN' and boolean_operands[-2] == 'WIN':
                    answer = 'WIN'
                elif boolean_operands[-1] == 'FAIL' and boolean_operands[-2] == 'WIN':
                    answer = 'FAIL'
                elif boolean_operands[-1] == 'WIN' and boolean_operands[-2] == 'FAIL':
                    answer = 'FAIL'
                else:
                    answer = 'FAIL'
                boolean_operands.pop()
                boolean_operands.pop()
                boolean_operands.append(answer)
            elif boolean_list[i] == 'EITHER OF':
                if boolean_operands[-1] == 'WIN' and boolean_operands[-2] == 'WIN':
                    answer = 'WIN'
                elif boolean_operands[-1] == 'FAIL' and boolean_operands[-2] == 'WIN':
                    answer = 'WIN'
                elif boolean_operands[-1] == 'WIN' and boolean_operands[-2] == 'FAIL':
                    answer = 'WIN'
                else:
                    answer = 'FAIL'
                boolean_operands.pop()
                boolean_operands.pop()
                boolean_operands.append(answer)
            elif boolean_list[i] == 'WON OF':
                if boolean_operands[-1] == 'WIN' and boolean_operands[-2] == 'WIN':
                    answer = 'FAIL'
                elif boolean_operands[-1] == 'FAIL' and boolean_operands[-2] == 'WIN':
                    answer = 'WIN'
                elif boolean_operands[-1] == 'WIN' and boolean_operands[-2] == 'FAIL':
                    answer = 'WIN'
                else:
                    answer = 'FAIL'
                boolean_operands.pop()
                boolean_operands.pop()
                boolean_operands.append(answer)
            elif boolean_list[i] == 'NOT' and boolean_list[i+1] != 'NOT':
                if boolean_operands[-1] == 'WIN':
                    answer = 'FAIL'
                else:
                    answer = 'WIN'
                boolean_operands.pop()
                boolean_operands.append(answer)

    return answer

def infiniteBooleanAnalyzer(lexeme, keyword):
    operands = []
    parameters = []
    result = []
    standby_index = []
    an_counter = 1
    boolean_index = 1
    while boolean_index <= len(lexeme)-2:
        if lexeme[boolean_index][0] in ['BOTH OF', 'EITHER OF', 'WON OF']:
            if lexeme[boolean_index+1][0] in ['BOTH OF', 'EITHER OF', 'WON OF']:
                standby_index.append(boolean_index)
                an_counter += 1
                boolean_index += 1
                continue
            elif lexeme[boolean_index+1][0] == 'NOT':
                standby_index.append(boolean_index)
                boolean_index += 1
                continue
            if lexeme[boolean_index+3][0] in ['BOTH OF', 'EITHER OF', 'WON OF']:
                an_counter += 1
                boolean_index += 3
                continue
            elif lexeme[boolean_index+1][0] == 'NOT':
                standby_index.append(boolean_index)
                boolean_index += 1
                continue
            if lexeme[boolean_index+4][0] == 'AN' and len(standby_index) != 0:
                standby_index.pop()
                if len(standby_index) == 0:
                    operands.append(an_counter)
                    an_counter = 1
            boolean_index += 5
        elif lexeme[boolean_index][0] == 'NOT':
            if lexeme[boolean_index+1][0] in ['BOTH OF', 'EITHER OF', 'WON OF']:
                boolean_index += 1
                continue
            if lexeme[boolean_index+2][0] == 'AN' and len(standby_index) != 0:
                standby_index.pop()
                if len(standby_index) == 0:
                    operands.append(an_counter)
                    an_counter = 1
            boolean_index += 3
        elif lexeme[boolean_index][0] in varidents or lexeme[boolean_index][1] in literals:
            operands.append(an_counter)
            boolean_index += 2
    lexeme = lexeme[1:]

    isEnd = 0
    for number_of_an in operands:
        an = 0
        boolean_index = 0
        while an != number_of_an:
            if lexeme[boolean_index][0] == 'AN':
                an += 1
            elif lexeme[boolean_index][0] == 'MKAY':
                isEnd = 1
                break
            boolean_index += 1
        if isEnd != 1:
            if lexeme[0][0] in booleans:
                if lexeme[0][0] in ["BOTH OF", "EITHER OF", "WON OF"]:
                    parameters.append(lexeme[0:boolean_index+1])
                    lexeme = lexeme[boolean_index+2:]
                else:
                    parameters.append(lexeme[0:boolean_index])
                    lexeme = lexeme[boolean_index+1:]
            else:
                parameters.append(lexeme[0:boolean_index-1])
                lexeme = lexeme[boolean_index:]
        else:
            parameters.append(lexeme[0:-1])
    for operand in parameters:
        if len(operand) != 1:
            result.append(booleanAnalyzer(operand, 0))
        else:
            if operand[0][0] in varidents:
                if varidents[operand[0][0]] in ['WIN', 'FAIL']:
                    result.append(varidents[operand[0][0]])
                elif f'{int(float(varidents[operand[0][0]]))}' != '0' or varidents[operand[0][0]] != 'NOOB':
                    result.append('WIN')
                else:
                    result.append('FAIL')
            else:
                if operand in ['WIN', 'FAIL']:
                    result.append(operand[0][0])
                elif f'{int(float(operand[0][0]))}' != '0':
                    result.append('WIN')
                else:
                    result.append('FAIL')

    if keyword == 'ANY OF':
        if 'WIN' in result:
            return f'WIN'
        else:
            return f'FAIL'
    else:
        if 'FAIL' in result:
            return f'FAIL'
        else:
            return f'WIN'

def concatenationAnalyzer(lexeme):
    concat = []
    result = ''
    start_index = 1
    while start_index <= len(lexeme)-1:
        if lexeme[start_index][1] in literals or lexeme[start_index][1] == 'String Delimiter':
            if lexeme[start_index][1] in literals:
                concat.append(lexeme[start_index][0])
                start_index += 1
            else:
                concat.append(lexeme[start_index][0])
                start_index += 3
        elif lexeme[start_index][0] in varidents:
            concat.append(varidents[lexeme[start_index][0]])
            start_index += 1
        
        if start_index <= len(lexeme)-1:
            if lexeme[start_index][0] == 'AN':
                start_index += 1
        
    for operand in concat:
        result += str(operand)
    
    return result

isInCondition = -1      # -1 means unused
conditionFlag = -1
omgwtfFlag = -1
gtfoFlag = -1
nowaiFlag = -1
ifElseFlag = -1
isInFunction = -1
isLoops = -1
loopOut = -1
hasObtw = -1
functionBody = ''
currentFunction = ''
functions = {}
modified_varidents = {}
loopDone = -1
loops = {}
loopsLabel = ''
loopsOperation = ''
loopsVar = ''
loopsCondition = ''
loopsExpression = ''
loopsBody = []
loopStatement = ''
imOuttaFlag = -1
# loopsCodeBlock = []

temp_res = []
explicit_typecast = []
booleans = ['BOTH OF', 'EITHER OF', 'WON OF', 'NOT']
literals = ['NUMBR Literal', 'NUMBAR Literal', 'YARN Literal', 'TROOF Literal', 'Type Literal']
varidents = {}

def functionExecute(text, parameters):
    global varidents
    comparison = ['BOTH SAEM', 'DIFFRINT']
    booleans = ['BOTH OF', 'EITHER OF', 'WON OF', 'NOT']
    arithmetic = ['SUM OF','DIFF OF','PRODUKT OF', 'QUOSHUNT OF', 'MOD OF', 'BIGGR OF', 'SMALLR OF']
    infinitebooleans = ['ANY OF', "ALL OF"]
    IT = []
    for h in range(0, len(text.splitlines())):
        lexeme = keywords.lex(text.splitlines()[h].lstrip().rstrip())
        if lexeme is not None:
            for i in range(0, len(lexeme)):    

                #VISIBLE SEMANTICS
                if lexeme[i][0] == 'VISIBLE':
                    visible_index = i + 1
                    temp_result = ""
                    while visible_index < len(lexeme):
                        if lexeme[visible_index][1] == 'String Delimiter':
                            temp_result += str(lexeme[visible_index+1][0])
                            visible_index +=3
                        elif lexeme[visible_index][1] == 'Output Delimiter':
                            visible_index +=1
                        elif lexeme[visible_index][0] in parameters:
                            temp_result += str(parameters[lexeme[visible_index][0]])
                            visible_index +=1
                        #this is for IT
                        elif lexeme[visible_index][0] == 'IT':
                            temp_result += str(keywords.get_IT())
                            visible_index+=1
                        #THIS IS FOR THE TROOF LITERAL
                        elif lexeme[visible_index][1] == 'TROOF Literal':
                            temp_result += str(lexeme[visible_index][0])
                            visible_index+=1
                        #THIS IS FOR GETTING THE NUMBR
                        elif lexeme[visible_index][1] == 'NUMBAR Literal':
                            temp_result += str(lexeme[visible_index][0])
                            visible_index+=1
                        #FOR GETTING THE NUMBAR
                        elif lexeme[visible_index][1] == 'NUMBR Literal':
                            temp_result += str(lexeme[visible_index][0])
                            visible_index+=1
                        elif lexeme[visible_index][0] in arithmetic:
                            #kunin ang lexeme until +
                            temp = []
                            temp_index = visible_index
                            while temp_index < len(lexeme):
                                if lexeme[temp_index][1] == "Output Delimiter":
                                    break
                                else:
                                    temp.append(lexeme[temp_index])
                                    temp_index+=1
                            arithmeticresult = str(arithmeticAnalyzer(parameters,arithmetic,temp)) 
                            temp_result += arithmeticresult
                            visible_index = temp_index
                        #COMPARISON 
                        elif lexeme[visible_index][0] in comparison:
                            #kunin ang lexeme until +
                            temp = []
                            temp_index = visible_index
                            while temp_index < len(lexeme):
                                if lexeme[temp_index][1] == "Output Delimiter":
                                    break
                                else:
                                    temp.append(lexeme[temp_index])
                                    temp_index+=1
                            temp_result += str(comparison_expression(temp))
                            visible_index = temp_index

                        #BOOLEANS
                        elif lexeme[visible_index][0] in booleans:
                            #kunin ang lexeme until +
                            temp = []
                            temp_index = visible_index
                            while temp_index < len(lexeme):
                                if lexeme[temp_index][1] == "Output Delimiter":
                                    break
                                else:
                                    temp.append(lexeme[temp_index])
                                    temp_index+=1
                            temp_result += str(booleanAnalyzer(temp, 0))
                            visible_index = temp_index
                        #INFINITE BOOLEANS
                        elif lexeme[visible_index][0] in infinitebooleans:
                            #kunin ang lexeme until +
                            temp = []
                            temp_index = visible_index
                            while temp_index < len(lexeme):
                                if lexeme[temp_index][1] == "Output Delimiter":
                                    break
                                else:
                                    temp.append(lexeme[temp_index])
                                    temp_index+=1
                            temp_result += str(infiniteBooleanAnalyzer(temp, lexeme[visible_index][0]))
                            visible_index = temp_index
                        elif lexeme[visible_index][0] == 'SMOOSH':
                            #kunin ang lexeme until +
                            temp = []
                            temp_index = visible_index
                            while temp_index < len(lexeme):
                                if lexeme[temp_index][1] == "Output Delimiter":
                                    break
                                else:
                                    temp.append(lexeme[temp_index])
                                    temp_index+=1
                            temp_result += str(concatenationAnalyzer(lexeme[i+1:]))
                            visible_index = temp_index
                    text = text.replace(f'{text.splitlines()[h]}', f'I HAS A IT ITZ "{temp_result}"', 1)
                    varidents['IT'] = temp_result
                    IT.append(temp_result)
                    break
                elif lexeme[i][0] == 'FOUND YR':
                    #-- BOTH SAEM AND DIFFRINT WITH VARIDENTS
                    if lexeme[i+1][0] in parameters:
                        varidents['IT'] = parameters[lexeme[i+1][0]]
                    elif lexeme[i+1][0] == 'BOTH SAEM' or lexeme[i+1][0] == 'DIFFRINT':
                        result = comparison_expression(lexeme[i+1:])
                        varidents['IT'] = result
                    
                    ##INFINITE ARITY BOOLEAN SYNTAX - ANY OF
                    elif lexeme[i+1][0] == 'ANY OF' or lexeme[i+1][0] == 'ALL OF':
                        result = infiniteBooleanAnalyzer(lexeme[i+2:], "ALL OF")
                        varidents['IT'] = result
                        
                    elif lexeme[i+1][0] in booleans:
                        result = infiniteBooleanAnalyzer(lexeme[i+2:], "ANY OF")
                        varidents['IT'] = result

                    #THIS PART IS FOR THE COMPUTATIONS!!
                    elif lexeme[i+1][0] in arithmetic:
                        arithmeticresult = str(arithmeticAnalyzer(parameters,arithmetic,lexeme[i+1:]))
                        varidents['IT'] = arithmeticresult
                    return IT
                elif lexeme[i][0] == 'GTFO':
                    return IT

def semantics(text):
    arithmetic = ['SUM OF','DIFF OF','PRODUKT OF', 'QUOSHUNT OF', 'MOD OF', 'BIGGR OF', 'SMALLR OF']
    semanticsResult = ''
    # global modified_varidents
    global varidents
    global explicit_typecast
    global undefined_error
    global noob_error
    global temp_res
    global isInCondition
    global conditionFlag
    global omgwtfFlag
    global gtfoFlag
    global nowaiFlag
    global ifElseFlag
    global isInFunction
    global isLoops
    global functionBody
    global functions
    global currentFunction
    global loops
    global loopsBody
    global loopsCondition
    global loopsExpression
    global loopsLabel
    global loopsOperation
    global loopsVar
    global loopDone
    global loopStatement
    global imOuttaFlag
    global hasObtw
    ifElseFlag = -1
    nowaiFlag = -1

    varidents = {'IT': 'NOOB'}
    temp_list = []

    temp_varident = syntax.getVaridents(text)
    for key in temp_varident:
        varidents[key] = temp_varident[key]
    literals = ['NUMBR Literal', 'NUMBAR Literal', 'YARN Literal', 'TROOF Literal', 'Type Literal']
    comparison = ['BOTH SAEM', 'DIFFRINT']
    booleans = ['BOTH OF', 'EITHER OF', 'WON OF', 'NOT']
    infinitebooleans = ['ANY OF', "ALL OF"]
    outsideWazzup = 0
    undefined_error_prompt =  "\n>> ZeroDivisionError: Result will have an undefined due to 0.\n"
    noob_error_prompt = "\n>> SyntaxError near arithmetic operation: \n\tVariable Identifier to be used in arithmetic operations should not be empty and should be numeric only!"
    parameter_list = {}

    for h in range(0, len(text.splitlines())):
        lexeme = keywords.lex(text.splitlines()[h].lstrip().rstrip())
        if undefined_error == 1 or noob_error == 1:
            undefined_error = 0
            noob_error = 0
            return [None,'', varidents]
        
        if lexeme is not None:
            if ['BTW', 'Comment Delimiter'] in lexeme:
                lexeme.pop(lexeme.index(['BTW', 'Comment Delimiter'])+1)
                lexeme.pop(lexeme.index(['BTW', 'Comment Delimiter']))
            if conditionFlag == 0 and (lexeme[0][0] != 'OMG' and lexeme[0][0] != 'OMGWTF'):     # para sa mga statements na hindi ieexecute sa if else at switch case
                text = text.replace(f'{text.splitlines()[h]}', f'', 1)
                continue
            elif conditionFlag == 1 and gtfoFlag == 1 and lexeme[0][0] != 'OIC':
                continue
            
            if ifElseFlag == 0 and nowaiFlag == 1:
                if len(lexeme) != 2 or lexeme[0][0] != 'NO' or lexeme[1][0] != 'WAI':                  
                    text = text.replace(f'{text.splitlines()[h]}', f'', 1)
                    continue
            elif ifElseFlag == 1 and nowaiFlag == 0 and lexeme[0][0] != 'OIC':
                ('pasok dito >>>>>>', text.splitlines()[h])
                text = text.replace(f'{text.splitlines()[h]}', f'', 1)
                continue 
            
            if imOuttaFlag == 1 and lexeme[0][0] != 'IM OUTTA YR':
                text = text.replace(f'{text.splitlines()[h]}', f'', 1)
                continue

            if isInFunction == 1:
                if lexeme[0][0] != 'IF' or lexeme[1][0] != 'U' or lexeme[2][0] != 'SAY' or lexeme[3][0] != 'SO':
                    functionBody += f'{text.splitlines()[h]}\n'
                    continue

            for i in range(0, len(lexeme)):    
                if lexeme[i][0] == 'OBTW':
                    hasObtw = 0
                if lexeme[i][0] == 'TLDR':
                    hasObtw = -1     
                if lexeme[i][0] == 'BUHBYE':
                    outsideWazzup = 1
                    break
                if lexeme[i][0] == 'I HAS A' and hasObtw == -1 and lexeme[i-1][0] != 'BTW':
                    if outsideWazzup == 1:
                        if len(lexeme) == 4:
                            varidents[lexeme[i+1][0]] = lexeme[i+3][0]
                        elif len(lexeme) > 4:
                            varidents[lexeme[i+1][0]] = lexeme[i+4][0]
                    break
                #-- BOTH SAEM AND DIFFRINT WITH VARIDENTS
                if lexeme[i][0] == 'BOTH SAEM' and hasObtw == -1 and lexeme[i-1][0] != 'BTW' or lexeme[i][0] == 'DIFFRINT' and hasObtw == -1 and lexeme[i-1][0] != 'BTW':
                    result = comparison_expression(lexeme)
                    text = text.replace(f'{text.splitlines()[h]}', f'I HAS A IT ITZ {result}', 1)
                    return ['', text, varidents]
                
                ##INFINITE ARITY BOOLEAN SYNTAX - ANY OF
                elif lexeme[i][0] == 'ANY OF' and hasObtw == -1 and lexeme[i-1][0] != 'BTW' or lexeme[i][0] == 'ALL OF' and hasObtw == -1 and lexeme[i-1][0] != 'BTW':
                    result = infiniteBooleanAnalyzer(lexeme[i+1:], "ALL OF")
                    text = text.replace(f'{text.splitlines()[h]}', f'I HAS A IT ITZ {result}', 1)
                    return ['', text, varidents]
                    
                elif lexeme[i][0] in booleans and hasObtw == -1 and lexeme[i-1][0] != 'BTW':
                    result = infiniteBooleanAnalyzer(lexeme[i+1:], "ANY OF")
                    text = text.replace(f'{text.splitlines()[h]}', f'I HAS A IT ITZ {result}', 1)
                    return ['', text, varidents]

                #THIS PART IS FOR THE COMPUTATIONS!!
                elif lexeme[i][0] in arithmetic and hasObtw == -1 and lexeme[i-1][0] != 'BTW':
                    arithmeticresult = str(arithmeticAnalyzer(varidents,arithmetic,lexeme))
                    if arithmeticresult == "NOOBERROR":
                        temp_result += noob_error_prompt
                        noob_error = 1
                        break 
                    if arithmeticresult == "UNDEFINEDERROR":
                        temp_result += undefined_error_prompt
                        undefined_error = 1
                        break
                    else:
                        text = text.replace(f'{text.splitlines()[h]}', f'I HAS A IT ITZ {arithmeticresult}', 1)
                        return [arithmeticresult, text, varidents]
                        break
                
                #THIS IS TO CATER GIMMEH - ASKING USER FOR INPUT
                elif lexeme[i][0] == 'GIMMEH' and hasObtw == -1 and lexeme[i-1][0] != 'BTW':
                    # resolved na :>>
                    input_value = for_input.get_user_input()
                    if convertFloat(input_value) == False:
                        input_value = '"' + input_value + '"'
                        varidents[lexeme[i+1][0]] = str(input_value)
                    else:
                        if convertFloat(input_value) == int(input_value):
                            varidents[lexeme[i+1][0]] = int(input_value)
                        else:
                            varidents[lexeme[i+1][0]] = float(input_value)
                    
                    
                    # varidents[lexeme[i+1][0]] = str(input_value)
                    modified_varidents[lexeme[i+1][0]] = str(input_value)
                    text = text.replace(f'{text.splitlines()[h]}', f'I HAS A {lexeme[i+1][0]} ITZ {input_value}', 1)
                    return [f'{input_value}\n', text, varidents]
                    
                #R
                elif lexeme[i][0] == 'R' and hasObtw == -1 and lexeme[i-1][0] != 'BTW':
                    if len(lexeme) == 3:
                        for j in varidents:
                            if lexeme[i-1][0] == j:
                                if lexeme[i+1][0].isnumeric():
                                    varidents[j] = int(lexeme[i+1][0])
                                    modified_varidents[lexeme[i-1][0]] = int(lexeme[i+1][0])
                                else:
                                    if convertFloat(lexeme[i+1][0]):
                                        varidents[j] = float(lexeme[i+1][0])
                                        modified_varidents[lexeme[i-1][0]] = float(lexeme[i+1][0])
                                    elif lexeme[i+1][0] in varidents:
                                        for k in varidents:
                                            if lexeme[i+1][0] == k:
                                                varidents[lexeme[i-1][0]] = varidents[k]
                                                modified_varidents[lexeme[i-1][0]] = varidents[k]  
                                                text = text.replace(f'{text.splitlines()[h]}', f'I HAS A {lexeme[i-1][0]} ITZ {varidents[k]}', 1)
                                                return [f'', text, varidents]     
                                    else:
                                        varidents[j] = lexeme[i+1][0]
                                        modified_varidents[lexeme[i-1][0]] = lexeme[i+1][0]  
                                        text = text.replace(f'{text.splitlines()[h]}', f'I HAS A {lexeme[i-1][0]} ITZ {varidents[j]}', 1)
                                        return [f'', text, varidents]              
                                
                    elif len(lexeme) == 5 and lexeme[i+1][0] != 'MAEK':
                        for j in varidents:
                            if lexeme[i-1][0] == j:
                                if lexeme[i+1][0] == '"' and lexeme[i+3][0] == '"':
                                    varidents[j] = lexeme[i+2][0]
                                    modified_varidents[lexeme[i-1][0]] = str(lexeme[i+2][0])
                                    text = text.replace(f'{text.splitlines()[h]}', f'I HAS A {j} ITZ {lexeme[i+2][0]}', 1)
                                    return [f'', text, varidents]  
                    else:
                        if lexeme[i+1][0] == 'BOTH SAEM' or lexeme[i+1][0] == 'DIFFRINT':
                            for j in varidents:
                                if lexeme[i-1][0] == j:
                                    result = comparison_expression(lexeme[i+1:])
                                    if len(result) != 0:
                                        varidents[j] = result
                                        modified_varidents[lexeme[i-1][0]] = str(result)
                                        text = text.replace(f'{text.splitlines()[h]}', f'I HAS A {j} ITZ {result}', 1)
                                        return [f'', text, varidents] 
                                        
                        elif lexeme[i+1][0] in booleans:
                            for j in varidents:
                                if lexeme[i-1][0] == j:
                                    result = booleanAnalyzer(lexeme[i+1:], "no")
                                    if len(result) != 0:
                                        varidents[j] = result
                                        modified_varidents[lexeme[i-1][0]] = str(result)
                                        text = text.replace(f'{text.splitlines()[h]}', f'I HAS A {j} ITZ {result}', 1)
                                        return [f'', text, varidents] 
                                        
                        elif lexeme[i+1][0] == 'ANY OF':
                            for j in varidents:
                                if lexeme[i-1][0] == j:
                                    result = infiniteBooleanAnalyzer(lexeme[i+1:], "ANY OF")
                                    if len(result) != 0:
                                        varidents[j] = result
                                        modified_varidents[lexeme[i-1][0]] = str(result)
                                        text = text.replace(f'{text.splitlines()[h]}', f'I HAS A {j} ITZ {result}', 1)
                                        return [f'', text, varidents] 
                                        
                        elif lexeme[i+1][0] == 'SMOOSH':
                            for j in varidents:
                                if lexeme[i-1][0] == j:
                                    result = concatenationAnalyzer(lexeme[i+1:])
                                    if len(result) != 0:
                                        varidents[j] = result
                                        modified_varidents[lexeme[i-1][0]] = str(result)
                                        text = text.replace(f'{text.splitlines()[h]}', f'I HAS A {j} ITZ {result}', 1)
                                        return [f'', text, varidents] 
                                        

                        elif lexeme[i+1][0] == 'ALL OF':
                            for j in varidents:
                                if lexeme[i-1][0] == j:
                                    result = infiniteBooleanAnalyzer(lexeme[i+1:], lexeme[i+1][0])
                                    if len(result) != 0:
                                        varidents[j] = result
                                        modified_varidents[lexeme[i-1][0]] = str(result)
                                        text = text.replace(f'{text.splitlines()[h]}', f'I HAS A {j} ITZ {result}', 1)
                                        return [f'', text, varidents] 
                                        
                        elif lexeme[i+1][0] in arithmetic:
                            for j in varidents:
                                if lexeme[i-1][0] == j:
                                    result = arithmeticAnalyzer(varidents, arithmetic,lexeme[i+1:])
                                    if result == "NOOBERROR":
                                        temp_result += noob_error_prompt
                                        noob_error = 1
                                    elif result == 'UNDEFINEDERROR':
                                        temp_result += undefined_error_prompt
                                        undefined_error = 1
                                        
                                    else:
                                        if len(result) != 0:
                                            varidents[j] = result
                                            modified_varidents[lexeme[i-1][0]] = str(result)
                                            text = text.replace(f'{text.splitlines()[h]}', f'I HAS A {j} ITZ {result}', 1)
                                            return [f'', text, varidents] 
                        elif lexeme[i+1][0] == 'MAEK':
                            i += 1
                            if len(lexeme[i:]) == 3 or len(lexeme[i:]) == 4 :
                                for j in varidents:
                                    if j == lexeme[i+1][0]:
                                        if varidents[j] == 'NOOB':
                                            if lexeme[i+2][0] == 'YARN' or (lexeme[i+2][0] == 'A' and lexeme[i+3][0] == 'YARN'):
                                                text = text.replace(f'{text.splitlines()[h]}', f'I HAS A {lexeme[i-2][0]} ITZ {""}', 1)
                                                return [f'', text, varidents] 
                                            elif lexeme[i+2][0] == 'NUMBAR' or (lexeme[i+2][0] == 'A' and lexeme[i+3][0] == 'NUMBAR'):
                                                text = text.replace(f'{text.splitlines()[h]}', f'I HAS A {lexeme[i-2][0]} ITZ {"0.0"}', 1)
                                                return [f'', text, varidents] 
                                            elif lexeme[i+2][0] == 'NUMBR' or (lexeme[i+2][0] == 'A' and lexeme[i+3][0] == 'NUMBR'):
                                                text = text.replace(f'{text.splitlines()[h]}', f'I HAS A {lexeme[i-2][0]} ITZ {"0"}', 1)
                                                return [f'', text, varidents]
                                            elif lexeme[i+2][0] == 'TROOF' or (lexeme[i+2][0] == 'A' and lexeme[i+3][0] == 'TROOF'):
                                                text = text.replace(f'{text.splitlines()[h]}', f'I HAS A {lexeme[i-2][0]} ITZ {"FAIL"}', 1)
                                                return [f'', text, varidents]
                                            elif lexeme[i+2][0] == 'NOOB' or (lexeme[i+2][0] == 'A' and lexeme[i+3][0] == 'NOOB'):
                                                text = text.replace(f'{text.splitlines()[h]}', f'I HAS A {lexeme[i-2][0]} ITZ {"NOOB"}', 1)
                                                return [f'', text, varidents]
                                        else:
                                            if convertFloat(varidents[j]):
                                                if lexeme[i+2][0] == 'YARN' or (lexeme[i+2][0] == 'A' and lexeme[i+3][0] == 'YARN'):
                                                    text = text.replace(f'{text.splitlines()[h]}', f'I HAS A {lexeme[i-2][0]} ITZ {str(varidents[j])}', 1)
                                                    return [f'', text, varidents]
                                                elif lexeme[i+2][0] == 'NUMBAR' or (lexeme[i+2][0] == 'A' and lexeme[i+3][0] == 'NUMBAR'):
                                                    if '.' in str(varidents[j]):
                                                        text = text.replace(f'{text.splitlines()[h]}', f'I HAS A {lexeme[i-2][0]} ITZ {varidents[j]}', 1)
                                                        return [f'', text, varidents]
                                                    else:
                                                        text = text.replace(f'{text.splitlines()[h]}', f'I HAS A {lexeme[i-2][0]} ITZ {varidents[j]}.0', 1)
                                                        return [f'', text, varidents]
                                                elif lexeme[i+2][0] == 'NUMBR' or (lexeme[i+2][0] == 'A' and lexeme[i+3][0] == 'NUMBR'):
                                                    text = text.replace(f'{text.splitlines()[h]}', f'I HAS A {lexeme[i-2][0]} ITZ {int(float(varidents[j]))}', 1)
                                                    return [f'', text, varidents]
                                                elif lexeme[i+2][0] == 'NOOB' or (lexeme[i+2][0] == 'A' and lexeme[i+3][0] == 'NOOB'):
                                                    text = text.replace(f'{text.splitlines()[h]}', f'I HAS A {lexeme[i-2][0]} ITZ {"NOOB"}', 1)
                                                    return [f'', text, varidents]
                                                elif lexeme[i+2][0] == 'TROOF' or (lexeme[i+2][0] == 'A' and lexeme[i+3][0] == 'TROOF'):
                                                    if varidents[j] == 0.0:
                                                        text = text.replace(f'{text.splitlines()[h]}', f'I HAS A {lexeme[i-2][0]} ITZ {"FAIL"}', 1)
                                                        return [f'', text, varidents]
                                                    else:
                                                        text = text.replace(f'{text.splitlines()[h]}', f'I HAS A {lexeme[i-2][0]} ITZ {"WIN"}', 1)
                                                        return [f'', text, varidents]
                                            elif varidents[j] == 'WIN':
                                                if lexeme[i+2][0] == 'YARN' or (lexeme[i+2][0] == 'A' and lexeme[i+3][0] == 'YARN'):
                                                    text = text.replace(f'{text.splitlines()[h]}', f'I HAS A {lexeme[i-2][0]} ITZ {str(varidents[j])}', 1)
                                                    return [f'', text, varidents]
                                                elif lexeme[i+2][0] == 'NUMBAR' or (lexeme[i+2][0] == 'A' and lexeme[i+3][0] == 'NUMBAR'):
                                                    text = text.replace(f'{text.splitlines()[h]}', f'I HAS A {lexeme[i-2][0]} ITZ {"1.0"}', 1)
                                                    return [f'', text, varidents] 
                                                elif lexeme[i+2][0] == 'NUMBR' or (lexeme[i+2][0] == 'A' and lexeme[i+3][0] == 'NUMBR'):
                                                    text = text.replace(f'{text.splitlines()[h]}', f'I HAS A {lexeme[i-2][0]} ITZ {"1"}', 1)
                                                    return [f'', text, varidents] 
                                                elif lexeme[i+2][0] == 'TROOF' or (lexeme[i+2][0] == 'A' and lexeme[i+3][0] == 'TROOF'):
                                                    text = text.replace(f'{text.splitlines()[h]}', f'I HAS A {lexeme[i-2][0]} ITZ {varidents[j]}', 1)
                                                    return [f'', text, varidents]
                                                elif lexeme[i+2][0] == 'NOOB' or (lexeme[i+2][0] == 'A' and lexeme[i+3][0] == 'NOOB'):
                                                    text = text.replace(f'{text.splitlines()[h]}', f'I HAS A {lexeme[i-2][0]} ITZ {"NOOB"}', 1)
                                                    return [f'', text, varidents]
                                            elif varidents[j] == 'FAIL':
                                                if lexeme[i+2][0] == 'YARN' or (lexeme[i+2][0] == 'A' and lexeme[i+3][0] == 'YARN'):
                                                    text = text.replace(f'{text.splitlines()[h]}', f'I HAS A {lexeme[i-2][0]} ITZ {str(varidents[j])}', 1)
                                                    return [f'', text, varidents]
                                                elif lexeme[i+2][0] == 'NUMBAR' or (lexeme[i+2][0] == 'A' and lexeme[i+3][0] == 'NUMBAR'):
                                                    text = text.replace(f'{text.splitlines()[h]}', f'I HAS A {lexeme[i-2][0]} ITZ {"0.0"}', 1)
                                                    return [f'', text, varidents] 
                                                elif lexeme[i+2][0] == 'NUMBR' or (lexeme[i+2][0] == 'A' and lexeme[i+3][0] == 'NUMBR'):
                                                    text = text.replace(f'{text.splitlines()[h]}', f'I HAS A {lexeme[i-2][0]} ITZ {"0"}', 1)
                                                    return [f'', text, varidents] 
                                                elif lexeme[i+2][0] == 'TROOF' or (lexeme[i+2][0] == 'A' and lexeme[i+3][0] == 'TROOF'):
                                                    text = text.replace(f'{text.splitlines()[h]}', f'I HAS A {lexeme[i-2][0]} ITZ {varidents[j]}', 1)
                                                    return [f'', text, varidents]
                                                elif lexeme[i+2][0] == 'NOOB' or (lexeme[i+2][0] == 'A' and lexeme[i+3][0] == 'NOOB'):
                                                    text = text.replace(f'{text.splitlines()[h]}', f'I HAS A {lexeme[i-2][0]} ITZ {"NOOB"}', 1)
                                                    return [f'', text, varidents]                    
                elif lexeme[i][0] == 'IS NOW A' and hasObtw == -1 and lexeme[i-1][0] != 'BTW':
                    for j in varidents:
                        if j == lexeme[i-1][0]:
                            if varidents[j] == 'NOOB':
                                if lexeme[i+1][0] == 'YARN':
                                    text = text.replace(f'{text.splitlines()[h]}', f'I HAS A {lexeme[i-1][0]} ITZ {""}', 1)
                                    return [f'', text, varidents] 
                                elif lexeme[i+1][0] == 'NUMBAR':
                                    text = text.replace(f'{text.splitlines()[h]}', f'I HAS A {lexeme[i-1][0]} ITZ {"0.0"}', 1)
                                    return [f'', text, varidents] 
                                elif lexeme[i+1][0] == 'NUMBR':
                                    text = text.replace(f'{text.splitlines()[h]}', f'I HAS A {lexeme[i-1][0]} ITZ {"0"}', 1)
                                    return [f'', text, varidents]
                                elif lexeme[i+1][0] == 'TROOF':
                                    text = text.replace(f'{text.splitlines()[h]}', f'I HAS A {lexeme[i-1][0]} ITZ {"FAIL"}', 1)
                                    return [f'', text, varidents]
                                elif lexeme[i+1][0] == 'NOOB':
                                    text = text.replace(f'{text.splitlines()[h]}', f'I HAS A {lexeme[i-1][0]} ITZ {"NOOB"}', 1)
                                    return [f'', text, varidents]
                            else:
                                if convertFloat(varidents[j]):
                                    if lexeme[i+1][0] == 'YARN':
                                        text = text.replace(f'{text.splitlines()[h]}', f'I HAS A {lexeme[i-1][0]} ITZ {str(varidents[j])}', 1)
                                        return [f'', text, varidents]
                                    elif lexeme[i+1][0] == 'NUMBAR':
                                        if '.' in str(varidents[j]):
                                            text = text.replace(f'{text.splitlines()[h]}', f'I HAS A {lexeme[i-1][0]} ITZ {varidents[j]}', 1)
                                            return [f'', text, varidents]
                                        else:
                                            text = text.replace(f'{text.splitlines()[h]}', f'I HAS A {lexeme[i-1][0]} ITZ {varidents[j]}.0', 1)
                                            return [f'', text, varidents]
                                    elif lexeme[i+1][0] == 'NUMBR':
                                        text = text.replace(f'{text.splitlines()[h]}', f'I HAS A {lexeme[i-1][0]} ITZ {int(float(varidents[j]))}', 1)
                                        return [f'', text, varidents]
                                    elif lexeme[i+1][0] == 'NOOB':
                                        text = text.replace(f'{text.splitlines()[h]}', f'I HAS A {lexeme[i-1][0]} ITZ {"NOOB"}', 1)
                                        return [f'', text, varidents]
                                    elif lexeme[i+1][0] == 'TROOF':
                                        if varidents[j] == 0.0:
                                            text = text.replace(f'{text.splitlines()[h]}', f'I HAS A {lexeme[i-1][0]} ITZ {"FAIL"}', 1)
                                            return [f'', text, varidents]
                                        else:
                                            text = text.replace(f'{text.splitlines()[h]}', f'I HAS A {lexeme[i-1][0]} ITZ {"WIN"}', 1)
                                            return [f'', text, varidents]
                                elif varidents[j] == 'WIN':
                                    if lexeme[i+1][0] == 'YARN':
                                        text = text.replace(f'{text.splitlines()[h]}', f'I HAS A {lexeme[i-1][0]} ITZ {str(varidents[j])}', 1)
                                        return [f'', text, varidents]
                                    elif lexeme[i+1][0] == 'NUMBAR':
                                        text = text.replace(f'{text.splitlines()[h]}', f'I HAS A {lexeme[i-1][0]} ITZ {"1.0"}', 1)
                                        return [f'', text, varidents] 
                                    elif lexeme[i+1][0] == 'NUMBR':
                                        text = text.replace(f'{text.splitlines()[h]}', f'I HAS A {lexeme[i-1][0]} ITZ {"1"}', 1)
                                        return [f'', text, varidents] 
                                    elif lexeme[i+1][0] == 'TROOF':
                                        text = text.replace(f'{text.splitlines()[h]}', f'I HAS A {lexeme[i-1][0]} ITZ {varidents[j]}', 1)
                                        return [f'', text, varidents]
                                    elif lexeme[i+1][0] == 'NOOB':
                                        text = text.replace(f'{text.splitlines()[h]}', f'I HAS A {lexeme[i-1][0]} ITZ {"NOOB"}', 1)
                                        return [f'', text, varidents]
                                elif varidents[j] == 'FAIL':
                                    if lexeme[i+1][0] == 'YARN':
                                        text = text.replace(f'{text.splitlines()[h]}', f'I HAS A {lexeme[i-1][0]} ITZ {str(varidents[j])}', 1)
                                        return [f'', text, varidents]
                                    elif lexeme[i+1][0] == 'NUMBAR':
                                        text = text.replace(f'{text.splitlines()[h]}', f'I HAS A {lexeme[i-1][0]} ITZ {"0.0"}', 1)
                                        return [f'', text, varidents] 
                                    elif lexeme[i+1][0] == 'NUMBR':
                                        text = text.replace(f'{text.splitlines()[h]}', f'I HAS A {lexeme[i-1][0]} ITZ {"0"}', 1)
                                        return [f'', text, varidents] 
                                    elif lexeme[i+1][0] == 'TROOF':
                                        text = text.replace(f'{text.splitlines()[h]}', f'I HAS A {lexeme[i-1][0]} ITZ {varidents[j]}', 1)
                                        return [f'', text, varidents]
                                    elif lexeme[i+1][0] == 'NOOB':
                                        text = text.replace(f'{text.splitlines()[h]}', f'I HAS A {lexeme[i-1][0]} ITZ {"NOOB"}', 1)
                                        return [f'', text, varidents]
                #MAEK    
                elif lexeme[i][0] == 'MAEK' and hasObtw == -1 and lexeme[i-1][0] != 'BTW':
                    if len(lexeme) == 3 or len(lexeme) == 4 :
                        for j in varidents:
                            if j == lexeme[i+1][0]:
                                if varidents[j] == 'NOOB':
                                    if lexeme[i+2][0] == 'YARN' or (lexeme[i+2][0] == 'A' and lexeme[i+3][0] == 'YARN'):
                                        text = text.replace(f'{text.splitlines()[h]}', f'I HAS A IT ITZ {""}', 1)
                                        return [f'', text, varidents] 
                                    elif lexeme[i+2][0] == 'NUMBAR' or (lexeme[i+2][0] == 'A' and lexeme[i+3][0] == 'NUMBAR'):
                                        text = text.replace(f'{text.splitlines()[h]}', f'I HAS A IT ITZ {"0.0"}', 1)
                                        return [f'', text, varidents] 
                                    elif lexeme[i+2][0] == 'NUMBR' or (lexeme[i+2][0] == 'A' and lexeme[i+3][0] == 'NUMBR'):
                                        text = text.replace(f'{text.splitlines()[h]}', f'I HAS A IT ITZ {"0"}', 1)
                                        return [f'', text, varidents]
                                    elif lexeme[i+2][0] == 'TROOF' or (lexeme[i+2][0] == 'A' and lexeme[i+3][0] == 'TROOF'):
                                        text = text.replace(f'{text.splitlines()[h]}', f'I HAS A IT ITZ {"FAIL"}', 1)
                                        return [f'', text, varidents]
                                    elif lexeme[i+2][0] == 'NOOB' or (lexeme[i+2][0] == 'A' and lexeme[i+3][0] == 'NOOB'):
                                        text = text.replace(f'{text.splitlines()[h]}', f'I HAS A IT ITZ {"NOOB"}', 1)
                                        return [f'', text, varidents]
                                else:
                                    if convertFloat(varidents[j]):
                                        if lexeme[i+2][0] == 'YARN' or (lexeme[i+2][0] == 'A' and lexeme[i+3][0] == 'YARN'):
                                            text = text.replace(f'{text.splitlines()[h]}', f'I HAS A IT ITZ {str(varidents[j])}', 1)
                                            return [f'', text, varidents]
                                        elif lexeme[i+2][0] == 'NUMBAR' or (lexeme[i+2][0] == 'A' and lexeme[i+3][0] == 'NUMBAR'):
                                            if '.' in str(varidents[j]):
                                                text = text.replace(f'{text.splitlines()[h]}', f'I HAS A IT ITZ {varidents[j]}', 1)
                                                return [f'', text, varidents]
                                            else:
                                                text = text.replace(f'{text.splitlines()[h]}', f'I HAS A IT ITZ {varidents[j]}.0', 1)
                                                return [f'', text, varidents]
                                        elif lexeme[i+2][0] == 'NUMBR' or (lexeme[i+2][0] == 'A' and lexeme[i+3][0] == 'NUMBR'):
                                            text = text.replace(f'{text.splitlines()[h]}', f'I HAS A IT ITZ {int(float(varidents[j]))}', 1)
                                            return [f'', text, varidents]
                                        elif lexeme[i+2][0] == 'NOOB' or (lexeme[i+2][0] == 'A' and lexeme[i+3][0] == 'NOOB'):
                                            text = text.replace(f'{text.splitlines()[h]}', f'I HAS A IT ITZ {"NOOB"}', 1)
                                            return [f'', text, varidents]
                                        elif lexeme[i+2][0] == 'TROOF' or (lexeme[i+2][0] == 'A' and lexeme[i+3][0] == 'TROOF'):
                                            if varidents[j] == 0.0:
                                                text = text.replace(f'{text.splitlines()[h]}', f'I HAS A IT ITZ {"FAIL"}', 1)
                                                return [f'', text, varidents]
                                            else:
                                                text = text.replace(f'{text.splitlines()[h]}', f'I HAS A IT ITZ {"WIN"}', 1)
                                                return [f'', text, varidents]
                                    elif varidents[j] == 'WIN':
                                        if lexeme[i+2][0] == 'YARN' or (lexeme[i+2][0] == 'A' and lexeme[i+3][0] == 'YARN'):
                                            text = text.replace(f'{text.splitlines()[h]}', f'I HAS A IT ITZ {str(varidents[j])}', 1)
                                            return [f'', text, varidents]
                                        elif lexeme[i+2][0] == 'NUMBAR' or (lexeme[i+2][0] == 'A' and lexeme[i+3][0] == 'NUMBAR'):
                                            text = text.replace(f'{text.splitlines()[h]}', f'I HAS A IT ITZ {"1.0"}', 1)
                                            return [f'', text, varidents] 
                                        elif lexeme[i+2][0] == 'NUMBR' or (lexeme[i+2][0] == 'A' and lexeme[i+3][0] == 'NUMBR'):
                                            text = text.replace(f'{text.splitlines()[h]}', f'I HAS A IT ITZ {"1"}', 1)
                                            return [f'', text, varidents] 
                                        elif lexeme[i+2][0] == 'TROOF' or (lexeme[i+2][0] == 'A' and lexeme[i+3][0] == 'TROOF'):
                                            text = text.replace(f'{text.splitlines()[h]}', f'I HAS A IT ITZ {varidents[j]}', 1)
                                            return [f'', text, varidents]
                                        elif lexeme[i+2][0] == 'NOOB' or (lexeme[i+2][0] == 'A' and lexeme[i+3][0] == 'NOOB'):
                                            text = text.replace(f'{text.splitlines()[h]}', f'I HAS A IT ITZ {"NOOB"}', 1)
                                            return [f'', text, varidents]
                                    elif varidents[j] == 'FAIL':
                                        if lexeme[i+2][0] == 'YARN' or (lexeme[i+2][0] == 'A' and lexeme[i+3][0] == 'YARN'):
                                            text = text.replace(f'{text.splitlines()[h]}', f'I HAS A IT ITZ {str(varidents[j])}', 1)
                                            return [f'', text, varidents]
                                        elif lexeme[i+2][0] == 'NUMBAR' or (lexeme[i+2][0] == 'A' and lexeme[i+3][0] == 'NUMBAR'):
                                            text = text.replace(f'{text.splitlines()[h]}', f'I HAS A IT ITZ {"0.0"}', 1)
                                            return [f'', text, varidents] 
                                        elif lexeme[i+2][0] == 'NUMBR' or (lexeme[i+2][0] == 'A' and lexeme[i+3][0] == 'NUMBR'):
                                            text = text.replace(f'{text.splitlines()[h]}', f'I HAS A IT ITZ {"0"}', 1)
                                            return [f'', text, varidents] 
                                        elif lexeme[i+2][0] == 'TROOF' or (lexeme[i+2][0] == 'A' and lexeme[i+3][0] == 'TROOF'):
                                            text = text.replace(f'{text.splitlines()[h]}', f'I HAS A IT ITZ {varidents[j]}', 1)
                                            return [f'', text, varidents]
                                        elif lexeme[i+2][0] == 'NOOB' or (lexeme[i+2][0] == 'A' and lexeme[i+3][0] == 'NOOB'):
                                            text = text.replace(f'{text.splitlines()[h]}', f'I HAS A IT ITZ {"NOOB"}', 1)
                                            return [f'', text, varidents]
                
                elif lexeme[i][0] in varidents and len(lexeme) == 1 and hasObtw == -1 and lexeme[i-1][0] != 'BTW':
                    text = text.replace(f'{text.splitlines()[h]}', f'I HAS A IT ITZ {varidents[lexeme[i][0]]}', 1)
                    return [f'', text, varidents]

                elif len(lexeme) == 2 and lexeme[i][0] == 'O' and lexeme[i+1][0] == 'RLY' and hasObtw == -1 and lexeme[i-1][0] != 'BTW':
                    isInCondition = 1

                elif len(lexeme) == 2 and lexeme[i][0] == 'YA' and lexeme[i+1][0] == 'RLY' and hasObtw == -1 and lexeme[i-1][0] != 'BTW':
                    if varidents['IT'] == 'WIN':
                        ifElseFlag = 1
                    elif varidents['IT'] == 'FAIL':
                        ifElseFlag = 0
                        nowaiFlag = 1
                    else:
                        if f'{int(float(varidents["IT"]))}' != '0' or varidents["IT"] != 'NOOB':
                            ifElseFlag = 1
                        else:
                            ifElseFlag = 0
                            nowaiFlag = 1
                
                elif len(lexeme) == 2 and lexeme[i][0] == 'NO' and lexeme[i+1][0] == 'WAI' and hasObtw == -1 and lexeme[i-1][0] != 'BTW':
                    nowaiFlag = 0

                elif lexeme[i][0] == 'WTF' and hasObtw == -1 and lexeme[i-1][0] != 'BTW':
                    isInCondition = 1
                
                elif lexeme[i][0] == 'OMG' and isInCondition == 1 and hasObtw == -1 and lexeme[i-1][0] != 'BTW':
                    if len(lexeme) > 2:     # pag string ang condition
                        if lexeme[i+2][0] == varidents['IT']:
                            conditionFlag = 1
                        else:
                            conditionFlag = 0
                    else:                   # pag other literals
                        if lexeme[i+1][0] == varidents['IT']:
                            conditionFlag = 1
                        else:
                            conditionFlag = 0
                
                elif lexeme[i][0] == 'GTFO' and isInCondition == 1 and hasObtw == -1 and lexeme[i-1][0] != 'BTW':
                    gtfoFlag = 1

                elif lexeme[i][0] == 'OMGWTF' and isInCondition == 1 and hasObtw == -1 and lexeme[i-1][0] != 'BTW':
                    conditionFlag = -1
                    omgwtfFlag = -1

                elif lexeme[i][0] == 'OIC' and isInCondition == 1 and hasObtw == -1 and lexeme[i-1][0] != 'BTW':  # reset all flags
                    if gtfoFlag != -1:
                        gtfoFlag = -1
                    isInCondition == -1
                    conditionFlag = -1
                    ifElseFlag = -1
                    nowaiFlag = -1

                elif lexeme[i][0] == 'HOW IZ I' and hasObtw == -1 and lexeme[i-1][0] != 'BTW':
                    currentFunction = lexeme[i+1][0]
                    if len(lexeme) == 4:
                        parameter_list[lexeme[i+1][0]] = lexeme[i+3][0]
                    else:
                        parameters = []
                        param_index = 3

                        while param_index < len(lexeme):
                            parameters.append(lexeme[param_index][0])
                            param_index += 3
                        
                        parameter_list[lexeme[i+1][0]] = parameters

                    isInFunction = 1
                
                elif lexeme[i][0] == 'I IZ' and hasObtw == -1 and lexeme[i-1][0] != 'BTW':
                    if len(lexeme) != 8 or lexeme[i+3][0] in arithmetic:
                        if lexeme[i+3][0] in varidents:
                            it = functionExecute(functions[lexeme[i+1][0]], {parameter_list[lexeme[i+1][0]]: varidents[lexeme[i+3][0]]})
                            
                            if len(it) != 0:
                                to_print = ''
                                for value in it:
                                    to_print += f'{value}\n'
                                text = text.replace(f'{text.splitlines()[h]}', f'I HAS A IT ITZ "{it[-1]}"', 1)
                                varidents['IT'] = it[-1]
                                return [f"{to_print}", text, varidents]
                            return [f'', text, varidents]
                        elif lexeme[i+3][0] in arithmetic:
                            arithresult = arithmeticAnalyzer(varidents, arithmetic, lexeme[i+3:-1])
                            it = functionExecute(functions[lexeme[i+1][0]], {parameter_list[lexeme[i+1][0]]: arithresult})
                            if len(it) != 0:
                                to_print = ''
                                for value in it:
                                    to_print += f'{value}\n'
                                text = text.replace(f'{text.splitlines()[h]}', f'I HAS A IT ITZ "{it[-1]}"', 1)
                                varidents['IT'] = it[-1]
                                return [f"{to_print}", text, varidents]
                            text = text.replace(f'{text.splitlines()[h]}', f'I HAS A IT ITZ "{varidents["IT"]}"', 1)
                            return [f'', text, varidents]
                    else:
                        parameter_index = 3
                        parameters = []
                        param_counter = 0
                        to_pass = {}
                        while parameter_index < len(lexeme):
                            if lexeme[parameter_index][0] in varidents:
                                parameters.append(varidents[lexeme[parameter_index][0]])
                                parameter_index += 3
                        
                        for value in parameter_list[lexeme[i+1][0]]:
                            to_pass[value] = parameters[param_counter]
                            param_counter += 1
                        it = functionExecute(functions[lexeme[i+1][0]], to_pass)
                            
                        if len(it) != 0:
                            to_print = ''
                            for value in it:
                                to_print += f'{value}\n'
                            text = text.replace(f'{text.splitlines()[h]}', f'I HAS A IT ITZ "{it[-1]}"', 1)
                            varidents['IT'] = it[-1]
                            return [f"{to_print}", text, varidents]
                        text = text.replace(f'{text.splitlines()[h]}', f'I HAS A IT ITZ "{varidents["IT"]}"', 1)
                        return [f'', text, varidents]

                elif lexeme[i][0] == 'IF' and lexeme[i+1][0] == 'U' and lexeme[i+2][0] == 'SAY' and lexeme[i+3][0] == 'SO' and hasObtw == -1 and lexeme[i-1][0] != 'BTW':

                    functions[currentFunction] = functionBody
                    functionBody = ''
                    isInFunction = -1
                
                elif lexeme[i][0] == 'IM IN YR' and hasObtw == -1 and lexeme[i-1][0] != 'BTW':
                    loopStatement = text.splitlines()[h]
                    isLoops = 0
                    loopsLabel = lexeme[i+1][0] #label
                    loopsOperation = lexeme[i+2][0]
                    loopsVar = lexeme[i+4][0]
                    loopsCondition = lexeme[i+5][0]
                    
                    if lexeme[i+6][0] == 'BOTH SAEM' or lexeme[i+6][0] == 'DIFFRINT':
                        if loopsCondition == 'TIL':
                            result = comparison_expression(lexeme[i+6:])
                            if result == 'FAIL':
                                loopDone = 0
                            else:
                                imOuttaFlag = 1
                                loopDone = 1
                                

                        elif loopsCondition == 'WILE':
                            result = comparison_expression(lexeme[i+6:])
                            if result == 'WIN':
                                loopDone = 0
                            else:
                                imOuttaFlag = 1
                                loopDone = 1
                                
                    break

                elif lexeme[i][0] == 'IM OUTTA YR' and hasObtw == -1 and lexeme[i-1][0] != 'BTW':
                    imOuttaFlag = -1
                    text = text.replace(f'{loopStatement}', f'', 1)
                    text = text.replace(f'{text.splitlines()[h]}', f'', 1)
                    return ['', text, varidents]
                    

                elif lexeme[i][0] == 'VISIBLE' and hasObtw == -1 and lexeme[i-1][0] != 'BTW':
                    visible_index = i + 1
                    temp_result = ""
                    while visible_index < len(lexeme):
                        if lexeme[visible_index][1] == 'String Delimiter':
                            if lexeme[visible_index+1][0].isspace():
                                temp_result += " "
                                visible_index +=3
                            else:
                                temp_result += str(lexeme[visible_index+1][0])
                                visible_index +=3
                        elif lexeme[visible_index][1] == 'Output Delimiter':
                            visible_index +=1
                        elif lexeme[visible_index][0] in varidents:
                            temp_result += str(varidents[lexeme[visible_index][0]])
                            visible_index +=1
                        #this is for IT
                        elif lexeme[visible_index][0] == 'IT':
                            temp_result += str(keywords.get_IT())
                            visible_index+=1
                        #THIS IS FOR THE TROOF LITERAL
                        elif lexeme[visible_index][1] == 'TROOF Literal':
                            temp_result += str(lexeme[visible_index][0])
                            visible_index+=1
                        #THIS IS FOR GETTING THE NUMBR
                        elif lexeme[visible_index][1] == 'NUMBAR Literal':
                            temp_result += str(lexeme[visible_index][0])
                            visible_index+=1
                        #FOR GETTING THE NUMBAR
                        elif lexeme[visible_index][1] == 'NUMBR Literal':
                            temp_result += str(lexeme[visible_index][0])
                            visible_index+=1
                        elif lexeme[visible_index][0] in arithmetic:
                            #kunin ang lexeme until +
                            temp = []
                            temp_index = visible_index
                            while temp_index < len(lexeme):
                                if lexeme[temp_index][1] == "Output Delimiter":
                                    break
                                else:
                                    temp.append(lexeme[temp_index])
                                    temp_index+=1
                            arithmeticresult = str(arithmeticAnalyzer(varidents,arithmetic,temp)) 
                            if arithmeticresult == "NOOBERROR":
                                temp_result += noob_error_prompt
                                noob_error = 1
                                break 
                            elif arithmeticresult == "UNDEFINEDERROR":
                                temp_result += undefined_error_prompt
                                undefined_error = 1
                                break
                            else:
                                temp_result += arithmeticresult
                                visible_index = temp_index
                        #COMPARISON 
                        elif lexeme[visible_index][0] in comparison:
                            #kunin ang lexeme until +
                            temp = []
                            temp_index = visible_index
                            while temp_index < len(lexeme):
                                if lexeme[temp_index][1] == "Output Delimiter":
                                    break
                                else:
                                    temp.append(lexeme[temp_index])
                                    temp_index+=1
                            temp_result += str(comparison_expression(temp))
                            visible_index = temp_index

                        #BOOLEANS
                        elif lexeme[visible_index][0] in booleans:
                            #kunin ang lexeme until +
                            temp = []
                            temp_index = visible_index
                            while temp_index < len(lexeme):
                                if lexeme[temp_index][1] == "Output Delimiter":
                                    break
                                else:
                                    temp.append(lexeme[temp_index])
                                    temp_index+=1
                            temp_result += str(booleanAnalyzer(temp, 0))
                            visible_index = temp_index
                        #INFINITE BOOLEANS
                        elif lexeme[visible_index][0] in infinitebooleans:
                            #kunin ang lexeme until +
                            temp = []
                            temp_index = visible_index
                            while temp_index < len(lexeme):
                                if lexeme[temp_index][1] == "Output Delimiter":
                                    break
                                else:
                                    temp.append(lexeme[temp_index])
                                    temp_index+=1
                            temp_result += str(infiniteBooleanAnalyzer(temp, lexeme[visible_index][0]))
                            visible_index = temp_index
                        elif lexeme[visible_index][0] == 'SMOOSH':
                            #kunin ang lexeme until +
                            temp = []
                            temp_index = visible_index
                            while temp_index < len(lexeme):
                                if lexeme[temp_index][1] == "Output Delimiter":
                                    break
                                else:
                                    temp.append(lexeme[temp_index])
                                    temp_index+=1
                            temp_result += str(concatenationAnalyzer(lexeme[i+1:]))
                            visible_index = temp_index
                    if loopDone == 0:
                        if loopsOperation != 'NERFIN':
                            text = text.replace(f'{loopStatement}', f'I HAS A IT ITZ {temp_result}\nI HAS A {loopsVar} ITZ {int(varidents[loopsVar])+1}\n{loopStatement}', 1)
                        else:
                            text = text.replace(f'{loopStatement}', f'I HAS A IT ITZ {temp_result}\nI HAS A {loopsVar} ITZ {int(varidents[loopsVar])-1}\n{loopStatement}', 1)
                        return [f"{temp_result}\n", text, varidents]
                    text = text.replace(f'{text.splitlines()[h]}', f'I HAS A IT ITZ "{temp_result}"', 1)
                    varidents['IT'] = temp_result
                    return [f"{temp_result}\n", text, varidents]
                
            lexeme.clear()
    
    text = text.replace(f'{text.splitlines()[h]}', '', 1)
    temp_res = temp_list
    
    return [None, text, varidents]

def comparison_expression(lexeme):
    arithmetic = ['SUM OF','DIFF OF','PRODUKT OF', 'QUOSHUNT OF', 'MOD OF', 'BIGGR OF', 'SMALLR OF']
    result = []
    for i in range(0, len(lexeme)):
                if lexeme[i][0] == 'BOTH SAEM':
                    if len(lexeme) == 4:
                        one = convertFloat(lexeme[i+1][0])
                        three = convertFloat(lexeme[i+3][0])
                        
                        if one == True and three == True:
                            if float(lexeme[i+1][0]) == float(lexeme[i+3][0]):
                                result = 'WIN'
                                
                            else:
                                result = 'FAIL'
                        elif one == False and three == True:
                            
                            value = ""
                            for j in varidents:
                                if j == lexeme[i+1][0]:
                                    value = varidents[j]
                            if convertFloat(value) == True:
                                if float(value) == float(lexeme[i+3][0]):
                                    result = 'WIN'
                                else:
                                    result = 'FAIL'
                            else:
                                if value == float(lexeme[i+3][0]):
                                    result = 'WIN'
                                else:
                                    result = 'FAIL'
                        elif one == True and three == False:
                            value = ""
                            for j in varidents:
                                if j == lexeme[i+3][0]:
                                    value = varidents[j]
                            if convertFloat(value) == True:
                                if float(lexeme[i+1][0]) == float(value):
                                    result = 'WIN'
                                else:
                                    result = 'FAIL'
                            else:
                                if float(lexeme[i+1][0]) == value:
                                    result = 'WIN'
                                else:
                                    result = 'FAIL'
                        elif one == False and three == False:
                            
                                if convertFloat(varidents[lexeme[i+1][0]]) == True and  convertFloat(varidents[lexeme[i+3][0]]) == True:
                                    if float(varidents[lexeme[i+1][0]]) == float(varidents[lexeme[i+3][0]]):
                                        result = 'WIN'
                                    else:
                                        result = 'FAIL'
                                else:
                                    if varidents[lexeme[i+1][0]] == varidents[lexeme[i+3][0]]:
                                        result = 'WIN'
                                    else:
                                        result = 'FAIL'
                    else: #for SMALLR OF and BIGGR OF
                        #BOTH SAEM/DIFFRINT x AN y

                        #assuming x is in arithmetic
                        
                        if lexeme[i+1][0] in arithmetic:
                            num_operations = 1
            
                            index =i+1
                            for j in range(2, len(lexeme)):
                                if lexeme[j][0] in arithmetic:
                                    num_operations += 1
                                    index = j
                            num_AN = num_operations * 2 + 3


                            temp = arithmeticAnalyzer(varidents, arithmetic,lexeme[i+1:num_AN])
                            if temp == 'NOOBERROR':
                                result =  f'>> ERROR: Cannot be compare using SMALLR or BIGGR because (both input are strings) or (a string and an integer) or (a string and a float)'
                            else:
                                one = convertFloat(temp)
                                three = convertFloat(lexeme[index+4+1][0])
                                last_operand = lexeme[index+4+1][0]
                                if one == True and three == True:
                                    if float(temp) == float(last_operand):
                                        result = 'WIN'
                                    else:
                                        result = 'FAIL'
                           
                                elif one == True and three == False:
                                    value = ""
                                    for j in varidents:
                                        if j == last_operand:
                                            value = varidents[j]
                                    if convertFloat(value) == True:
                                        if float(temp) == float(value):
                                            result = 'WIN'
                                        else:
                                            result = 'FAIL'
                                    else:
                                        if float(temp) == value:
                                            result = 'WIN'
                                        else:
                                            result = 'FAIL'
                            break
                        
                
                        elif lexeme[i+3][0] == 'SMALLR OF':
                            
                            one = convertFloat(lexeme[i+1][0])
                            three = convertFloat(lexeme[i+6][0])
                            if one == True and three == True:
                                if float(lexeme[i+1][0]) <= float(lexeme[i+6][0]):
                                    result = 'WIN'
                                else:
                                    result = 'FAIL'
                            elif one == False and three == True:
                                value = ""
                                for j in varidents:
                                    if j == lexeme[i+1][0]:
                                        value = varidents[j]
                                if convertFloat(value) == True:
                                    if float(value) <= float(lexeme[i+6][0]):
                                        result = 'WIN'
                                    else:
                                       result = 'FAIL'
                                else:
                                    if value <= float(lexeme[i+6][0]):
                                        result = 'WIN'
                                    else:
                                       result = 'FAIL'
                            elif one == True and three == False:
                                value = ""
                                for j in varidents:
                                    if j == lexeme[i+6][0]:
                                        value = varidents[j]
                                if convertFloat(value) == True:
                                    if float(lexeme[i+1][0]) <= float(value):
                                       result = 'WIN'
                                    else:
                                        result = 'FAIL'
                                else:
                                    if float(lexeme[i+1][0]) <= value:
                                       result = 'WIN'
                                    else:
                                        result = 'FAIL'
                            elif one == False and three == False:
                                    if convertFloat(varidents[lexeme[i+1][0]]) == True and  convertFloat(varidents[lexeme[i+6][0]]) == True:
                                        if float(varidents[lexeme[i+1][0]]) <= float(varidents[lexeme[i+6][0]]):
                                            result = 'WIN'
                                        else:
                                            result = 'FAIL'
                                    else:
                                        result =  f'>> ERROR: Cannot be compare using SMALLR or BIGGR because (both input are strings) or (a string and an integer) or (a string and a float)'
                        elif lexeme[i+3][0] == 'BIGGR OF':
                            one = convertFloat(lexeme[i+1][0])
                            three = convertFloat(lexeme[i+6][0])
                            if one == True and three == True:
                                if float(lexeme[i+1][0]) >= float(lexeme[i+6][0]):
                                   result = 'WIN'
                                else:
                                    result = 'FAIL'
                            elif one == False and three == True:
                                value = ""
                                for j in varidents:
                                    if j == lexeme[i+1][0]:
                                        value = varidents[j]
                                if convertFloat(value) == True:
                                    if float(value) >= float(lexeme[i+6][0]):
                                        result = 'WIN'
                                    else:
                                        result = 'FAIL'
                                else:
                                    if value >= float(lexeme[i+6][0]):
                                        result = 'WIN'
                                    else:
                                        result = 'FAIL'
                            elif one == True and three == False:
                                value = ""
                                for j in varidents:
                                    if j == lexeme[i+6][0]:
                                        value = varidents[j]
                                if convertFloat(value) == True:
                                    if float(lexeme[i+1][0]) >= float(value):
                                        result = 'WIN'
                                    else:
                                       result = 'FAIL'
                                else:
                                    if float(lexeme[i+1][0]) >= value:
                                        result = 'WIN'
                                    else:
                                       result = 'FAIL'
                            elif one == False and three == False:
                                if convertFloat(varidents[lexeme[i+1][0]]) == True and  convertFloat(varidents[lexeme[i+6][0]]) == True:
                                        if float(varidents[lexeme[i+1][0]]) >= float(varidents[lexeme[i+6][0]]):
                                            result = 'WIN'
                                        else:
                                            result = 'FAIL'
                                else:
                                    result =  f'>> ERROR: Cannot be compare using SMALLR or BIGGR because (both input are strings) or (a string and an integer) or (a string and a float)'
                                
                        #assuming y is in arithmetic
                        elif lexeme[i+3][0] in arithmetic:
                            num_operations = 1
            
                            index =i+3
                            for j in range(index, len(lexeme)):
                                if lexeme[j][0] in arithmetic:
                                    num_operations += 1
                                    index = j
                            num_AN = num_operations * 2 + 3

                            temp = arithmeticAnalyzer(varidents, arithmetic,lexeme[i+3:num_AN])
                            if temp == 'NOOBERROR':
                                result =  f'>> ERROR: Cannot be compare using SMALLR or BIGGR because (both input are strings) or (a string and an integer) or (a string and a float)'
                            else:
                                one = convertFloat(temp)
                                three = convertFloat(lexeme[index+3][0])
                                if one == True and three == True:
                                    if float(lexeme[i+1][0]) == float(temp):
                                        result = 'WIN'
                                    else:
                                        result = 'FAIL'
                           
                                elif one == False and three == True:
                                    value = ""
                                    for j in varidents:
                                        if j == lexeme[i+1][0]:
                                            value = varidents[j]
                                    if convertFloat(value) == True:
                                        if float(value) == float(temp):
                                            result = 'WIN'
                                        else:
                                            result = 'FAIL'
                                    else:
                                        if value == float(temp):
                                            result = 'WIN'
                                        else:
                                            result = 'FAIL'
                            break
                            
                #for diffrint
                elif lexeme[i][0] == 'DIFFRINT':
                    if len(lexeme) == 4:
                        one = convertFloat(lexeme[i+1][0])
                        three = convertFloat(lexeme[i+3][0])
                        if one == True and three == True:
                            if float(lexeme[i+1][0]) != float(lexeme[i+3][0]):
                               result = 'WIN'
                            else:
                                result = 'FAIL'
                        elif one == False and three == True:
                            value = ""
                            for j in varidents:
                                if j == lexeme[i+1][0]:
                                    value = varidents[j]
                            if convertFloat(value) == True:
                                if float(value) != float(lexeme[i+3][0]):
                                   result = 'WIN'
                                else:
                                   result = 'FAIL'
                            else:
                                if value != float(lexeme[i+3][0]):
                                   result = 'WIN'
                                else:
                                   result = 'FAIL'
                        elif one == True and three == False:
                            value = ""
                            for j in varidents:
                                if j == lexeme[i+3][0]:
                                    value = varidents[j]
                            if convertFloat(value) == True:
                                if float(lexeme[i+1][0]) != float(value):
                                   result = 'WIN'
                                else:
                                    result = 'FAIL'
                            else:
                                if float(lexeme[i+1][0]) != value:
                                   result = 'WIN'
                                else:
                                    result = 'FAIL'
                        elif one == False and three == False:
                            if convertFloat(varidents[lexeme[i+1][0]]) == True and  convertFloat(varidents[lexeme[i+3][0]]) == True:
                                        if float(varidents[lexeme[i+1][0]]) != float(varidents[lexeme[i+3][0]]):
                                            result = 'WIN'
                                        else:
                                            result = 'FAIL'
                            else:
                                    if varidents[lexeme[i+1][0]] != varidents[lexeme[i+3][0]]:
                                        result = 'WIN'
                                    else:
                                        result = 'FAIL'
                           
                    else: #for SMALLR OF and BIGGR OF
                        
                        if lexeme[i+1][0] in arithmetic:
                            num_operations = 1
            
                            index =i+1
                            # num_operations += 1
                            for j in range(index, len(lexeme)):
                                if lexeme[j][0] in arithmetic:
                                    num_operations += 1
                                    index = j
                            num_AN =num_operations * 2 + 3

                            temp = arithmeticAnalyzer(varidents, arithmetic,lexeme[i+1:index+4])
                            print("temp", temp)
                            if temp == 'NOOBERROR':
                               result =  f'>> ERROR: Cannot be compare using SMALLR or BIGGR because (both input are strings) or (a string and an integer) or (a string and a float)'
                            else:
                                one = convertFloat(temp)
                                three = convertFloat(lexeme[index+4+1][0])
                                last_operand = lexeme[index+4+1][0]
                                if one == True and three == True:
                                    if float(temp) != float(last_operand):
                                        result = 'WIN'
                                    else:
                                        result = 'FAIL'
                           
                                elif one == True and three == False:
                                    value = ""
                                    for j in varidents:
                                        if j == last_operand:
                                            value = varidents[j]
                                    if convertFloat(value) == True:
                                        if float(temp) != float(value):
                                            result = 'WIN'
                                        else:
                                            result = 'FAIL'
                                    else:
                                        if float(temp) != value:
                                            result = 'WIN'
                                        else:
                                            result = 'FAIL'
                        
                        if lexeme[i+3][0] == 'SMALLR OF':
                            one = convertFloat(lexeme[i+1][0])
                            three = convertFloat(lexeme[i+6][0])
                            if one == True and three == True:
                                if float(lexeme[i+1][0]) > float(lexeme[i+6][0]):
                                    result = 'WIN'
                                else:
                                    result = 'FAIL'
                            elif one == False and three == True:
                                value = ""
                                for j in varidents:
                                    if j == lexeme[i+1][0]:
                                        value = varidents[j]
                                if convertFloat(value) == True:
                                    if float(value) > float(lexeme[i+6][0]):
                                        result = 'WIN'
                                    else:
                                       result = 'FAIL'
                                else:
                                    if value > float(lexeme[i+6][0]):
                                        result = 'WIN'
                                    else:
                                       result = 'FAIL'
                            elif one == True and three == False:
                                value = ""
                                for j in varidents:
                                    if j == lexeme[i+6][0]:
                                        value = varidents[j]
                                if convertFloat(value) == True:
                                    if float(lexeme[i+1][0]) > float(value):
                                        result = 'WIN'
                                    else:
                                        result = 'FAIL'
                                else:
                                    if float(lexeme[i+1][0]) > value:
                                        result = 'WIN'
                                    else:
                                        result = 'FAIL'
                            elif one == False and three == False:
                                if convertFloat(varidents[lexeme[i+1][0]]) == True and  convertFloat(varidents[lexeme[i+6][0]]) == True:
                                        if float(varidents[lexeme[i+1][0]]) > float(varidents[lexeme[i+6][0]]):
                                            result = 'WIN'
                                        else:
                                            result = 'FAIL'
                                else:
                                    result =  f'>> ERROR: Cannot be compare using SMALLR or BIGGR because (both input are strings) or (a string and an integer) or (a string and a float)'
                                
                        elif lexeme[i+3][0] == 'BIGGR OF':
                            one = convertFloat(lexeme[i+1][0])
                            three = convertFloat(lexeme[i+6][0])
                            if one == True and three == True:
                                if float(lexeme[i+1][0]) < float(lexeme[i+6][0]):
                                    result = 'WIN'
                                else:
                                    result = 'FAIL'
                            elif one == False and three == True:
                                value = ""
                                for j in varidents:
                                    if j == lexeme[i+1][0]:
                                        value = varidents[j]
                                if convertFloat(value) == True:
                                    if float(value) < float(lexeme[i+6][0]):
                                       result = 'WIN'
                                    else:
                                       result = 'FAIL'
                                else:
                                    if value < float(lexeme[i+6][0]):
                                       result = 'WIN'
                                    else:
                                       result = 'FAIL'
                            elif one == True and three == False:
                                value = ""
                                for j in varidents:
                                    if j == lexeme[i+6][0]:
                                        value = varidents[j]
                                if convertFloat(value) == True:
                                    if float(lexeme[i+1][0]) < float(value):
                                        result = 'WIN'
                                    else:
                                        result = 'FAIL'
                                else:
                                    if lexeme[i+1][0] < float(value):
                                        result = 'WIN'
                                    else:
                                        result = 'FAIL'
                            elif one == False and three == False:
                                if convertFloat(varidents[lexeme[i+1][0]]) == True and  convertFloat(varidents[lexeme[i+6][0]]) == True:
                                        if float(varidents[lexeme[i+1][0]]) < float(varidents[lexeme[i+6][0]]):
                                            result = 'WIN'
                                        else:
                                            result = 'FAIL'
                                else:
                                    result =  f'>> ERROR: Cannot be compare using SMALLR or BIGGR because (both input are strings) or (a string and an integer) or (a string and a float)'
                                
                        #assuming y is in arithmetic
                        elif lexeme[i+3][0] in arithmetic:
                            num_operations = 1
            
                            index =i+3
                            for j in range(index, len(lexeme)):
                                if lexeme[j][0] in arithmetic:
                                    num_operations += 1
                                    index = j
                            num_AN = num_operations * 2 + 3

                            temp = arithmeticAnalyzer(varidents, arithmetic,lexeme[i+3:num_AN])
                            if temp == 'NOOBERROR':
                                result =  f'>> ERROR: Cannot be compare using SMALLR or BIGGR because (both input are strings) or (a string and an integer) or (a string and a float)'
                            else:
                                one = convertFloat(temp)
                                three = convertFloat(lexeme[index+3][0])
                                if one == True and three == True:
                                    if float(lexeme[i+1][0]) != float(temp):
                                        result = 'WIN'
                                    else:
                                        result = 'FAIL'
                           
                                elif one == False and three == True:
                                    value = ""
                                    for j in varidents:
                                        if j == lexeme[i+1][0]:
                                            value = varidents[j]
                                    if convertFloat(value) == True:
                                        if float(value) != float(temp):
                                            result = 'WIN'
                                        else:
                                            result = 'FAIL'
                                    else:
                                        if value != float(temp):
                                            result = 'WIN'
                                        else:
                                            result = 'FAIL'
    return result

def convertFloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False