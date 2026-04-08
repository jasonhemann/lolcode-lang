import sys, re, copy
from operator import xor
from tkinter import *

comment = ['OBTW', 'BTW']
# binary operators
expression = ['SUM OF', 'DIFF OF', 'PRODUKT OF','QUOSHUNT OF', 'MOD OF', 'BIGGR OF', 'SMALLR OF','BOTH OF','EITHER OF','WON OF']
expression2 = ['ALL OF', 'ANY OF']
types = ['NUMBAR','NUMBR','YARN','TROOF']
statement = ['VISIBLE', 'GIMMEH', 'SMOOSH', 'MAEK']
comparison = ["BOTH SAEM", "DIFFRINT"]
troof = ['WIN', 'FAIL']
assignment = ['I HAS A']
digit = '\-?[1-9]+[0-9]*'
float_num = '\-?[0-9]+\.[0-9]+'
is_orly = False

yarn = '\"(.+?)\"'
var_type = [troof,digit,float_num,yarn]

class Interpreter:
    def __init__(self, tokens, gui):
        self.tokens = tokens
        self.variable_dict={}
        self.variable_dict["IT"] = None
        self.HAI_exist =  False
        self.recent_line = None     # holds what line was read in switch case 
        self.enabled_wtf = False    # if a switch-case statement is encountered
        self.omg_value = ""         # Holds the value of the latest OMG checked
        self.omgvar_equal = False   #checks if IT and OMG value is equal
        self.omg_performed = False  #checks if an OMG is executed
        self.recent_token =  None
        self.enabled_orly =  False
        self.action_performed = None
        self.exist_yarly = False    # if YA RLY is read
        self.exist_nowai = False    # if NO WAI is read
        self.in_loop = False        # if IM IN YR is read
        self.loop_name = None       # Loop name
        self.loop_op = None         # UPPIN OR NERFIN
        self.loop_counter = None    # SECOND VARIABLE IN LOOP STATEMENT
        self.loop_func = None       # TIL OR WILE
        self.loop_list = []         # statements enclosed by loop
        self.loop_cond = []         # conditions after TIL or WILE
        self.gui = gui
        self.no_error = True
        self.error_found = False
    def __repr__(self):
        return f'{self.type}:{self.value}'

    def parse_tokens(self):
        while len(self.tokens) > 0:
            if 'HAI' in self.tokens[0]:
                self.HAI_exist = True
                break
            else:
                del self.tokens[0]

        if len(self.tokens) == 0 and self.HAI_exist == False:
            self.no_error = False
            self.print_to_terminal("ERROR: Expected 'HAI' at the beginning of the code")
            self.stop_program()

        elif 'KTHXBYE' not in self.tokens[len(self.tokens)-1]:
            self.no_error = False
            self.print_to_terminal("ERROR: Expected 'KTHXBYE' at the end of the code")
            self.stop_program()
        for i in range(1, len(self.tokens)):
            if self.error_found == False:
                self.check_syntax(self.tokens[i])
            else:
                return

    def check_syntax(self, token_line):
        if token_line != []:

            if token_line[0] == 'GTFO':
                token_line.pop(0)
                self.omgvar_equal = False

            elif token_line[0] == 'OIC':
                if self.enabled_wtf == True:
                    if self.recent_line == "OMGWTF":
                        self.enabled_wtf = False
                        self.recent_line = 'OIC'
                    else:
                        self.no_error = False
                        self.print_to_terminal("ERROR: Missing OMGWTF before this line")
                        self.stop_program()
                elif self.enabled_orly == True:
                    if self.exist_nowai == True:
                        self.enabled_orly = False
                        self.exist_nowai = False
                        self.exist_yarly = False
                        token_line.pop(0)
                    else:
                        self.no_error = False
                        self.print_to_terminal("ERROR: Missing NO WAI before this line")
                        self.stop_program()
                    
                else:
                    self.no_error = False
                    self.print_to_terminal("WARNING: Expected O RLY? | WTF? before this line")

        # SWITCH CASES START
                
            elif token_line[0] == 'OMGWTF' and self.omg_performed == False:
                if self.recent_line == "OMG":
                    self.recent_line = 'OMGWTF'
                    token_line.pop(0)
                    self.omgvar_equal = True
                    self.check_syntax(token_line)
                else:
                    self.no_error = False
                    self.print_to_terminal("Expected: OMG before this line")

            elif token_line[0] == 'OMGWTF' and self.recent_line == 'OMG' and self.omg_performed == True:
                self.recent_line = 'OMGWTF'
                token_line.pop(0)
            
            elif self.enabled_wtf == True and self.omgvar_equal == False and token_line[0]!= 'OMG':
                token_line.pop(0)
            
            elif token_line[0] == 'WTF':
                self.recent_token =  'SWITCH CASE'
                token_line.pop(0)
                self.recent_line = 'WTF'
                self.enabled_wtf = True

            #if OMG found
            elif token_line[0] == "OMG" and self.omgvar_equal == False:
                if self.enabled_wtf == True: 
                    self.recent_line = 'OMG'
                    if self.recent_line == 'WTF' or self.recent_line == 'OMG':
                        try:
                            token_line.pop(0)
                            self.omg_value = token_line.pop(0)

                            if len(token_line) > 0:
                                self.no_error = False
                                self.print_to_terminal("ERROR: Invalid OMG Value, only Literals/Variable are allowed")
                                self.stop_program()

                            if self.variable_dict["IT"] == self.omg_value:
                                self.omgvar_equal = True
                                self.omg_performed = True
                                self.check_syntax(token_line) 
                        except:
                            self.no_error = False
                            self.print_to_terminal("ERROR: Expected Literal/Variable after OMG")
                            self.stop_program()

                else:
                    self.no_error = False
                    self.print_to_terminal("WARNING: Expected WTF | OMG before this line")
          
        #SWITCH CASES END
        # IF ELSE START

            elif token_line[0] == 'O RLY':
                if self.recent_token == 'EXPRESSION':
                    token_line.pop(0)
                    self.enabled_orly = True
                else:
                    self.no_error = False
                    self.print_to_terminal("WARNING: Expected Expression before this line")

            elif token_line[0] == 'YA RLY':
                if self.enabled_orly == True:       
                    token_line.pop(0)
                    self.exist_yarly = True
                    if self.variable_dict["IT"] == True or self.variable_dict["IT"] == 'WIN' :
                        self.action_performed = 'YA RLY'
                        self.recent_token = 'YA RLY'
                        self.check_syntax(token_line)
                else:
                    self.no_error = False
                    self.print_to_terminal("ERROR: O RLY is not initialized")
                    self.stop_program()

            elif token_line[0] == 'NO WAI' and self.action_performed == None:
                if self.enabled_orly == True:
                    if self.exist_yarly == True:
                        if self.variable_dict["IT"] != True or self.variable_dict["IT"] != 'WIN':
                            self.recent_token = 'NO WAI'
                            self.exist_nowai = True
                            self.action_performed = 'NO WAI'
                            token_line.pop(0)
                            self.check_syntax(token_line)
                    else:
                        self.no_error = False
                        self.print_to_terminal("ERROR: YA RLY is not initialized")
                        self.stop_program()
                else:
                    self.no_error = False
                    self.print_to_terminal("ERROR: O RLY is not initialized")
                    self.stop_program()



            elif token_line[0] == 'NO WAI' and self.enabled_orly == True and self.action_performed != None and self.exist_yarly == True:
                self.recent_token = 'NO WAI'
                self.exist_nowai = True
                token_line.pop(0)
            
            elif self.enabled_orly == True and self.recent_token!= self.action_performed:
                token_line.pop(0)

        #IF ELSE END
        #LOOP
            elif token_line[0] == "IM OUTTA YR":
                if self.in_loop == True:
                    self.in_loop = False
                    # print("TOKTOK:",token_line)
                    token_line.pop(0)
                    if token_line.pop(0)==self.loop_name:

                        if self.loop_func == 'TIL': #TIL
                            temp_cond = copy.deepcopy(self.loop_cond)
                            ans = self.convert_from_string(self.comparison_expression(temp_cond[0]))

                            while ans == False:
                                temp_list = copy.deepcopy(self.loop_list)
                                for i in range(len(temp_list)):
                                    self.check_syntax(temp_list[i])
                                temp_cond = copy.deepcopy(self.loop_cond)
                                if self.loop_op == 'UPPIN':
                                    if self.loop_counter in self.variable_dict:
                                        self.variable_dict[self.loop_counter] = int(self.variable_dict[self.loop_counter])+1
                                    else:
                                        self.variable_dict[self.loop_counter] = None
                                elif self.loop_op == 'NERFIN':
                                    if self.loop_counter in self.variable_dict:
                                        self.variable_dict[self.loop_counter] = int(self.variable_dict[self.loop_counter])-1
                                    else:
                                        self.variable_dict[self.loop_counter] = None
                                ans = self.convert_from_string(self.comparison_expression(temp_cond[0]))

                        elif self.loop_func == 'WILE': #WILE
                            temp_cond = copy.deepcopy(self.loop_cond)
                            ans = self.convert_from_string(self.comparison_expression(temp_cond[0]))
                            while ans == True:
                                temp_list = copy.deepcopy(self.loop_list)
                                for i in range(len(temp_list)):
                                    self.check_syntax(temp_list[i])
                                temp_cond = copy.deepcopy(self.loop_cond)
                                if self.loop_op == 'UPPIN':
                                    if self.loop_counter in self.variable_dict:
                                        self.variable_dict[self.loop_counter] = int(self.variable_dict[self.loop_counter])+1
                                    else:
                                        self.no_error = False
                                        self.print_to_terminal("ERROR: variable {self.loop_counter} is not initialized")
                                        self.stop_program()
                                elif self.loop_op == 'NERFIN':
                                    if self.loop_counter in self.variable_dict:
                                        self.variable_dict[self.loop_counter] = int(self.variable_dict[self.loop_counter])-1
                                    else:
                                        self.no_error = False
                                        self.print_to_terminal("ERROR: variable {self.loop_counter} is not initialized")
                                        self.stop_program()
                                else:
                                    self.no_error = False
                                    self.print_to_terminal("ERROR: Missing UPPIN | NERFIN")
                                    self.stop_program()

                                ans = self.convert_from_string(self.comparison_expression(temp_cond[0]))

                    else:
                        self.no_error = False
                        self.print_to_terminal("ERROR: Loop identifier do not match!")
                        self.stop_program()
                else:
                    self.no_error = False
                    self.print_to_terminal("ERROR: IM IN YR is not initialized")
                    self.stop_program()
                self.loop_name = None
                self.loop_cond = []
                self.loop_list = []
                self.loop_counter = None
                self.loop_func = None
                self.loop_op = None

            elif self.in_loop == True:
                self.loop_list.append(token_line)

            elif token_line[0] == "IM IN YR":
                self.in_loop = True
                token_line.pop(0)
                if token_line == []:
                    self.no_error = False
                    self.print_to_terminal("ERROR: Wrong loop function implementation!")
                    self.stop_program()

                else:
                    try:
                        self.loop_name = token_line.pop(0)
                        if self.loop_name == 'UPPIN' or self.loop_name == 'NERFIN' or self.loop_name == 'YR':
                            self.no_error = False
                            self.print_to_terminal("ERROR: No function name initialized")
                            self.stop_program()
                    except:
                        self.no_error = False
                        self.print_to_terminal("WARNING: Expected loop function name")
                        self.stop_program()
                    try:
                        self.loop_op = token_line.pop(0)
                        if self.loop_op != 'UPPIN' and self.loop_op != 'NERFIN':
                            self.no_error == False
                            self.print_to_terminal("WARNING: Expected UPPIN|NERFIN")
                            self.stop_program()
                    except:
                        self.no_error = False
                        self.print_to_terminal("WARNING: Expected UPPIN|NERFIN")
                        self.stop_program()

                    if token_line[0] == "YR":
                        token_line.pop(0)
                        try:
                            self.loop_counter = token_line.pop(0)
                            if self.loop_counter == 'TIL' or self.loop_counter == 'WILE':
                                self.no_error = False
                                self.print_to_terminal("ERROR: No variable initialized")
                                self.stop_program()
                        except:
                            self.no_error = False
                            self.print_to_terminal("WARNING: Expected Variable")
                            self.stop_program()

                        if token_line[0] == 'TIL' or token_line[0] == 'WILE':
                            self.loop_func = token_line[0]
                            temp_index = token_line.index(token_line[0])
                            self.loop_cond.append(token_line[temp_index+1:])
                        else:
                            self.no_error = False
                            self.print_to_terminal("WARNING: Expected TIL|WILE")
                            self.stop_program()

                    else:
                        self.no_error = False
                        self.print_to_terminal("WARNING: Expected YR")
                        self.stop_program()
            #END LOOP

            elif token_line[0] in statement: 
                value = self.statement(token_line)
                self.recent_token =  'STATEMENT'

            elif token_line[0] in expression: #Operations
                value = self.binary_expression(token_line)
                self.recent_token =  'EXPRESSION'
                self.variable_dict["IT"] = value

            elif token_line[0] in expression2:
                value = self.arity_expression(token_line)
                self.recent_token =  'EXPRESSION'
                self.variable_dict["IT"] = value

            elif token_line[0] == 'NOT':
                print(token_line)
                value = not self.convert_from_string(token_line[1])
                self.recent_token =  'EXPRESSION'
                self.variable_dict["IT"] = value

            elif token_line[0] in assignment: #I HAS A
                print(token_line)
                self.recent_token =  'ASSIGNMENT'
                self.assign_variable(token_line)
                
            elif token_line[0] in comparison: #Conditional
                print(token_line)
                value = self.comparison_expression(token_line)
                self.recent_token =  'EXPRESSION'
                self.variable_dict["IT"] = value

            elif 'R' in token_line:
                print(token_line)
                r_index = token_line.index('R')
                token_line.pop(r_index)
                variable = token_line[r_index-1]

                if variable in self.variable_dict:
                    line = token_line[r_index:]
                    if len(line) < 1:
                        self.no_error = False
                        self.print_to_terminal("ERROR: Expected Literal/Expression")
                        self.stop_program()
                    value = line[0]
                    if value in expression:
                        value = self.binary_expression(line)
                    elif value in expression2:
                        print(line)
                        value = self.arity_expression(line)
                        self.variable_dict["IT"] = value
                    elif value == 'MAEK':
                        line.pop(0)
                        x = line.pop(0)
                        if x in self.variable_dict:
                            y = self.variable_dict[x]

                            try:
                                temp_type = line.pop(0)
                                if temp_type == "A":
                                    temp_type = line.pop(0)
                            
                                if temp_type in types:
                                    if temp_type == 'NUMBR':
                                        try:
                                            y = int(y)
                                        except:
                                            self.no_error = False
                                            self.print_to_terminal("ERROR: {x} cannot be casted to a NUMBR")
                                            self.stop_program()
                                    elif temp_type == 'NUMBAR':
                                        try:
                                            y = float(y)
                                        except:
                                            self.no_error = False
                                            self.print_to_terminal("ERROR: {x} cannot be casted to a NUMBR")
                                            self.stop_program()
                                    elif temp_type == 'YARN':
                                        try:
                                            y = str(y)
                                        except:
                                            self.no_error = False
                                            self.print_to_terminal("ERROR: {x} cannot be casted to a YARN")
                                            self.stop_program()
                                    elif temp_type == 'TROOF':
                                        try:
                                            y = bool(y)
                                        except:
                                            self.no_error = False
                                            self.print_to_terminal("ERROR: {x} cannot be casted to a TROOF")
                                            self.stop_program()
                                    self.variable_dict[x] = y
                                
                                    return self.variable_dict[x]
                                else:
                                    self.no_error = False
                                    self.print_to_terminal("ERROR: Invalid variable type!")
                                    self.stop_program()
                            except:
                                self.no_error = False
                                self.print_to_terminal("ERROR: Expected Variable Type")
                                self.stop_program()
                        else:
                            self.no_error = False
                            self.print_to_terminal("ERROR: cannot perform MAEK")
                            self.stop_program()

                    elif value == "" or len(line)<1:
                        self.no_error = False
                        self.print_to_terminal("WARNING: Expected Literal/Expression/Variable")
                        self.stop_program()
                    else:
                        value = self.get_string(line)
                    self.variable_dict[variable] = value
                else:
                    self.no_error = False
                    self.print_to_terminal('ERROR: {variable} not initialized')
                    self.stop_program()

            elif token_line[0] in self.variable_dict:
                print(token_line)
                token = token_line.pop(0)
                self.recent_token =  'VARIABLE'

                if token_line == []:
                    pass
            else:
                token_line.pop(0)

    def comparison_expression(self, token_line):
        token = token_line.pop(0)
        x,y = self.compare(token_line)
        if token == 'DIFFRINT':
            self.variable_dict["IT"] = 'WIN' if x!=y else 'FAIL'
        elif token == 'BOTH SAEM':
            self.variable_dict["IT"] = 'WIN' if x==y else 'FAIL'
        return self.variable_dict["IT"]

    # CONDITIONAL 
    def compare(self,expr):
        x = expr[0]
        if x in expression:
            x = self.binary_expression(expr)
        elif x == 'NOT':
            expr.pop(0)
            x = 'WIN' if x == 'FAIL' else 'FAIL'
            expr.pop(0)
        else:
            x = expr.pop(0)
        
        if expr.pop(0) == 'AN':
            y = expr[0]
            if y in expression:
                y = self.binary_expression(expr)
            elif y == 'NOT':
                expr.pop(0)
                y = "WIN" if y == 'FAIL' else 'FAIL'
                expr.pop(0)
            else:
                y = expr.pop(0)
        else:
            self.no_error = False
            self.print_to_terminal("ERROR: Missing AN keyword")
            self.stop_program()
 
        return self.convert_from_string(x), self.convert_from_string(y)
    
    # I HAS A
    def assign_variable(self, assign_line):
        assign_line.pop(0)
        x = assign_line.pop(0)

        try:
            temp = int(x)
            self.print_to_terminal(f'ERROR: "{x}" is a NUMBR')
            self.stop_program()
        except:
            try:
                temp = float(x)
                self.print_to_terminal(f'ERROR: "{x}" is a NUMBAR')
                self.stop_program()
            except:
                if len(assign_line) > 1 and assign_line.pop(0) == 'ITZ':
                    value = ""

                    if 'BTW' in assign_line:
                        index = assign_line.index('BTW')
                        del assign_line[index:]

                    if assign_line[0] == "SMOOSH":
                        assign_line.pop(0)
                        value = self.smoosh_func(assign_line)

                    elif len(assign_line) > 1:
                        if assign_line[0] in expression:
                            value = self.binary_expression(assign_line)
                        elif assign_line[0] in expression2:
                            value = self.arity_expression(assign_line)
                        elif assign_line[0] in comparison:
                            value = self.comparison_expression(assign_line)
                        print("VAL:",value)
                        self.variable_dict[x] = value

                    else:
                        value = assign_line.pop(0)
                        value = self.convert_from_string(value)
                    self.variable_dict[x] = value

                elif len(assign_line) == 0:
                    self.variable_dict[x] = None

                elif assign_line.pop(0)== 'ITZ' and len(assign_line) == 0:
                    self.no_error = False
                    self.print_to_terminal("ERROR: Expected Expression|Variable|Literal")
                    self.stop_program()


    def get_variables(self):
        return self.variable_dict

    # NON-OPERATORS   
    def statement(self, token_line):
        string = ""
        token = token_line.pop(0)
        if len(token_line) == 0 and token == 'VISIBLE':
            self.no_error = False
            self.print_to_terminal("ERROR: 'VISIBLE' contains invalid argument")
            self.stop_program()
        if token == 'VISIBLE':
            string = ""
            while len(token_line) > 0:
                token = token_line[0]
                if token in expression:
                    value = self.binary_expression(token_line)
                    value = self.convert_from_string(value)
                    del token_line[:4]

                elif token in comparison:
                    value =  self.comparison_expression(token_line)
                    value = self.convert_from_string(value)

                elif token == "NOT":
                    token_line.pop(0)
                    value = not self.convert_from_string(token_line.pop(0))
                
                elif token == "BTW":
                    index = token.index("BTW")
                    token_line.pop(0)
                    del token_line[index:]
                    continue

                elif token == "SMOOSH":
                    x = self.smoosh_func(token_line)
                    return x
                    
                elif len(token_line) == 0:
                    break
                
                else:
                    token = token_line.pop(0) 
                    value = self.convert_from_string(token)
                
                if value == True or value == 1:
                    value = "WIN"
                elif value == False or value == 0:
                    value = "FAIL"

                string = string + str(value)    
            self.print_to_terminal(string)
       
        elif token == 'GIMMEH':
            try:
                token = token_line.pop(0)
                self.gui.terminal_text.config(state="normal")
                user_input = self.gui.input_variables.pop(0)
                self.gui.terminal_text.config(state="disabled")
                if token in list(self.variable_dict.keys()):
                    user_input = self.convert_from_string(user_input)
                    self.variable_dict[token] = user_input
                    self.variable_dict["IT"] = user_input
                else:
                    self.no_error = False
                    self.print_to_terminal(f'WARNING: "{token}" is not a variable')
            except:
                self.no_error = False
                self.print_to_terminal("ERROR: Uninitialized variable")
                self.stop_program()

        elif token_line[0] == 'MAEK':
            token_line.pop(0)
            x = token_line.pop(0)
            if x in self.variable_dict.items():
                pass
            else:
                self.no_error = False
                # print("Error: cannot perform MAEK")
                self.print_to_terminal("ERROR: cannot perform MAEK")
                self.stop_program()

        else:
            pass

    def smoosh_func(self, expr):
        x = expr[0]
        # print("EXPR:",expr)
        if len(expr) > 0:
            if x in expression:
                x = self.binary_expression(expr)
            elif x in comparison:
                x = self.comparison_expression(expr)
            elif x == 'NOT':
                expr.pop(0)
                x = expr.pop(0)
                x = not self.convert_from_string(x)
            else:
                expr.pop(0)
                x = self.convert_from_string(x)
            x = str(x)
            temp = x

            if expr.pop(0) == 'AN' and len(expr) > 0: 
                while len(expr) > 0:
                    x = expr[0]
                    if x in expression:
                        x = self.binary_expression(expr)
                    elif x in comparison:
                        x = self.comparison_expression(expr)
                    elif x == 'NOT':
                        expr.pop(0)
                        x = expr.pop(0)
                        x = not self.convert_from_string(x)
                    else:
                        expr.pop(0)
                        x = self.convert_from_string(x)
                    x = str(x)

                    if len(expr) > 1 and expr.pop(0) != 'AN':
                        break
                    elif len(expr) == 1 and x != 'AN':
                        x = expr.pop(0)
                        x = str(self.convert_from_string(x))
                        
                    temp = temp + x
            else:
                self.no_error = False
                self.print_to_terminal("ERROR: wrong smoosh implementation!")
                self.stop_program()

        else:
            self.no_error = False
            self.print_to_terminal("ERROR: wrong smoosh implementation!") 
            self.stop_program()
        return temp 
    
    def arity_expression(self, token_line):
        token = token_line.pop(0)
        x = self.get_op(token, token_line)
        return x

    def get_op(self, token, expr):
        temp = ""
        isFirst = True
        if len(expr) < 1:
            self.no_error = False
            self.print_to_terminal("ERROR: Expected Expression/Literal")
            self.stop_program
        while len(expr) > 0:
            x = expr[0]
            if x in expression:
                x = self.binary_expression(expr)
            elif x in comparison:
                x = self.comparison_expression(expr)
            elif x == 'NOT':
                expr.pop(0)
                x = expr.pop(0)
                x = not self.convert_from_string(x)
            else:
                expr.pop(0)
            x = self.convert_from_string(x)

            if len(expr) > 0 and expr.pop(0) != 'AN':
                self.no_error = False
                self.print_to_terminal("ERROR: Missing AN")
                self.stop_program()

            elif len(expr) == 1 and x != 'AN':
                x = expr.pop(0)
                x = self.convert_from_string(x)

            elif len(expr) == 1 and x == 'AN':
                self.no_error = False
                self.print_to_terminal("ERROR: Invalid expression")
                self.stop_program

            if isFirst:
                isFirst = False
                temp = x
            else:
                temp = self.convert_from_string(temp)
                if token == 'ANY OF':
                    temp = temp or x 
                elif token == 'ALL OF':
                    temp = temp and x 
        return temp          

    # OPERATORS
    def binary_expression(self, token_line):
        token = token_line.pop(0)
        x, y = self.get_num(token_line)
        try:
            if token == 'SUM OF':
                # print(x + y)
                return x+y
            elif token == 'DIFF OF':
                # print("x-y:",x-y)
                return x-y
            elif token == 'PRODUKT OF':
                # print(x*y)
                return x*y
            elif token == 'QUOSHUNT OF':
                # print(x/y)
                return x/y
            elif token == 'MOD OF':
                # print(x%y)
                return x%y
            elif token == 'BIGGR OF':
                # print(x if x > y else y)
                return x if x > y else y
            elif token == 'SMALLR OF':
                # print(x if x < y else y)
                return x if x < y else y
            elif token == 'BOTH OF':
                # print(x and y)
                IT = x and y
                print("IT: ",IT)
                return 'WIN' if IT == 1 else 'FAIL'
                # return x and y
            elif token == 'EITHER OF':
                # print(x or y)
                IT = x or y
                return 'WIN' if IT == 1 else 'FAIL'
                # return x or y
            elif token == 'WON OF':
                # print(xor(x,y))
                IT = xor(x,y)
                return 'WIN' if IT == 1 else 'FAIL'
                # return xor(x,y)
            elif token == 'NOT':
                x = token_line.pop(0)
                return not self.convert_from_string(x)
        except:
            self.no_error = False
            self.print_to_terminal("ERROR: Invalid literal operation")
            self.stop_program()

    # get variables of binary expr
    def get_num(self, expr):
        try:
            x = expr[0]
            if x in expression:
                x = self.binary_expression(expr[:4])
                del expr[:4]
            elif x == 'NOT':
                expr.pop(0)
                x = "WIN" if x == 'FAIL' else 'FAIL'
                expr.pop(0)
            elif x in self.variable_dict:
                expr.pop(0)
                x = self.variable_dict[x]
            elif x == 'NOT':
                x= not self.convert_from_string(x)
            elif x in comparison:
                x = self.comparison_expression(expr[:4])
            else:
                x = expr.pop(0)
            
            if expr.pop(0) == 'AN':
                y = expr[0]
                if y in expression:
                    y = self.binary_expression(expr)
                elif y == 'NOT':
                    expr.pop(0)
                    y = "WIN" if y == 'FAIL' else 'FAIL'
                    expr.pop(0)
                elif y in self.variable_dict:
                    expr.pop(0)
                    y = self.variable_dict[y]   
                elif y == 'NOT':
                    y= not self.convert_from_string(y) 
                elif y in comparison:
                    y = self.comparison_expression(expr)
                else:
                    y = expr.pop(0)
        except:
            self.no_error = False
            self.print_to_terminal("ERROR: Invalid binary expression")
            self.stop_program()
            # sys.exit(1)
        
        return self.convert_from_string(x), self.convert_from_string(y)
   
    #getting strings for visible
    def get_string(self, expr):
        if expr == []:
            x = "ERROR: Expected expression at end of line"
            self.no_error = False
            self.print_to_terminal(x)
            return str(x)
            
        else:
            x = expr[0]
            if x in expression:
                x = self.binary_expression(expr)
            elif x in comparison:
                x = self.check_syntax(expr)
            elif x in self.variable_dict:
                x = self.variable_dict[expr.pop(0)]
            else:
                x = self.convert_from_string(expr.pop(0))
            x = str(x)

            while expr != []:
                y = expr[0]
                if y == "AN":
                    expr.pop(0)
                    y = self.get_string(expr)
                    if y != "ERROR: expected expression at end of":
                        x = x + str(y)
                    else:
                        x = "ERROR: expected expression at end of"
                        self.no_error = False
                        self.print_to_terminal(x)
                elif re.match(yarn,y):
                    y = self.convert_from_string(y)
                    expr.pop(0)
                    x = x + str(y)
                elif y in self.variable_dict:
                    x = x + str(self.variable_dict[y])
                    expr.pop(0)
                elif y in statement:
                    y = self.binary_expression(expr)
                    x = x + str(y)
                elif y in comparison:
                    y = self.check_syntax(expr)
                    x = x + str(y)
                else:
                    expr.pop(0)                
                
        return str(x)

    def print_to_terminal(self, message):
        self.gui.terminal_text.config(state="normal")
        self.gui.terminal_text.insert(END, message + "\n")  
        self.gui.terminal_text.config(state="disabled")
        if self.no_error == False:
            self.error_found = True

    def stop_program(self):
        self.tokens = ""
        

    def convert_from_string(self, token):
        # print("TOK:",token)
        if isinstance(token,int) == True:
            token = int(token)
        elif isinstance(token,float) == True:
            token = float(token)
        elif token == None:
            token = 'NOOB'
        else:
            try:
                token = int(token)
            except ValueError:
                try:
                    token = float(token)
                except ValueError:
                    if token in troof:
                        # return token
                        if token == 'WIN':
                            return True
                        elif token == 'FAIL':
                            return False
                    # elif: kapag variable'
                    elif token == 'NOOB':
                        return None
                    elif token in list(self.variable_dict.keys()):
                        token_index = list(self.variable_dict.keys()).index(token)
                        values = list(self.variable_dict.values())
                        token = self.convert_from_string(values[token_index])
                    elif "\"" in token or type(token) == str:
                        # token = self.convert_from_string(token.replace("\"", ""))
                        token = token.replace("\"", "")
                        if token.isdigit():
                            token = self.convert_from_string(token.replace("\"", ""))
                    else:
                        self.no_error = False
                        self.print_to_terminal("ERROR: Invalid input!")
                        self.stop_program()
                        # sys.exit(1)
        return token
