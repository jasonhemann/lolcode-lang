import sys, re, os, csv
from operator import xor

from lolcode_lexer import Token

comment = ['OBTW', 'BTW']
# binary operators
expression = ['SUM OF', 'DIFF OF', 'PRODUKT OF','QUOSHUNT OF', 'MOD OF', 'BIGGR OF', 'SMALLR OF','BOTH OF', 'BOTH SAEM','EITHER OF','WON OF']
statement = ['VISIBLE', 'GIMMEH', 'SMOOSH', 'MAEK']
troof = ['WIN', 'FAIL']
assignment = ['I HAS A', 'R']
literals = ['NUMBR', 'NUMBAR', 'YARN', 'TROOF', 'NOOB']
digit = '\-?[1-9]+'
float_num = '\-?[0-9]+\.[0-9]+'

yarn = '\"(.+?)\"'
var_type = [troof,digit,float_num,yarn]

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.variable_dict = {}
        self.tokens_list = []
        self.lexemes_dict = load_lex()
        self.hai_exist = False

    def __repr__(self):
        return f'{self.type}:{self.value}'

    def parse_tokens(self):
        while len(self.tokens) > 0:
            if 'HAI' in self.tokens[0]:
                self.hai_exist = True
                self.tokens_list.append([Token(self.tokens[0][0], self.lexemes_dict[self.tokens[0][0]])])
                self.tokens_list.pop(0)
                break
            else:
                del self.tokens[0]

        # if len(self.tokens) == 0 and self.HAI_exist == False:
        #     print("Error: No HAI found!")
            # sys.exit(1)

        # if 'KTHXBYE' not in self.tokens[len(self.tokens)-1]:
        #     print("Error: Code must end with KTHXBYE")
        #     # sys.exit(1)
        # else:
        # self.tokens_list.append([Token(self.tokens[len(self.tokens)-1][0], self.lexemes_dict[self.tokens[len(self.tokens)-1][0]])])
        # self.tokens_list.pop(0)

        for i in range(1, len(self.tokens)):
            if 'WTF' in self.tokens[i]:
                self.case_statement(self.tokens, i)
            elif 'O RLY?' in self.tokens[i]:
                self.if_else_statement(self.tokens, i)
            elif 'OBTW' in self.tokens[i]:
                self.obtw_comment(self.tokens, i)
            else:
                self.check_syntax(self.tokens[i])
    

        lexeme_list = []

        for token_line in self.tokens_list:
            lexeme_list.append(self.lexeme_table(token_line))

        return lexeme_list, self.tokens_list

    def obtw_comment(self, token_line, index):
        obtw_keyword = False
        temp = []
        token = token_line[index].pop(0)
        if token == 'OBTW' and len(token_line[index]) == 0:
            temp.append(self.convert_from_string(token))
            for i in range(index+1, len(token_line)):
                if len(token_line[i]) > 0 and token_line[i][0] == 'TLDR':
                    token = token_line[i].pop(0)
                    temp.append(self.convert_from_string(token))
                    break
                else:
                    token = token_line[i].pop(0)
                    temp.append(Token(token, "LN_CMMNT", "Line Comment"))
        elif len(token_line[index]) > 0:
            print("Invalid Format! OBTW should be followed by a next line!")
        self.tokens_list.append(temp)

    def if_else_statement(self, token_line, index):
        temp = []
        if_statement = False
        for i in range(index, len(token_line)):
            if token_line[i][0] == 'O RLY?':
                token = token_line[i].pop(0)
                temp.append(self.convert_from_string(token))
                if_statement = True
            
            # print("token_line: ",if_statement)
            elif if_statement == True:
                if token_line[i][0] in ['YA RLY', 'NO WAI', 'OIC']:
                    # self.tokens_list.append(temp)
                    temp = []
                    token = token_line[i].pop(0)
                    temp.append(self.convert_from_string(token))
                    self.tokens_list.append(temp)

                    if token == 'OIC':
                        break

                else:
                    self.check_syntax(token_line[i])
        print(self.tokens_list)


    def case_statement(self, token_line, index):
        temp = []
        case_statement = False
        for i in range(index, len(token_line)):
            if token_line[i][0] == 'WTF' and case_statement == False:
                temp = []
                token = token_line[i].pop(0)
                temp.append(self.convert_from_string(token))
                self.tokens_list.append(temp)
                case_statement = True
            elif case_statement:
                if token_line[i][0] == "OMG":
                    temp = []
                    token = token_line[i].pop(0)
                    temp.append(self.convert_from_string(token))
                    self.tokens_list.append(temp)
                    print(token_line[i])
                    if token_line[i] == []:
                        break
                    elif len(token_line[i]) > 0 or token_line[i][0] != "":
                        temp.append(self.convert_from_string(token_line[i].pop(0)))
                    else:
                        print("Error! Expected expression after OMG")
                elif token_line[i][0] in ['GTFO', 'OMGWTF', 'OIC']:
                    temp = []
                    token = token_line[i].pop(0)
                    temp.append(self.convert_from_string(token))
                    self.tokens_list.append(temp)
                    if token == 'OIC':
                        break
                else:
                    self.check_syntax(token_line[i])
                   

    def lexeme_table(self, token_line):
        temp_list = []
 
        if token_line == None:
            return
        else:
            for token in token_line:
                if type(token) == list:
                    temp_list += self.lexeme_table(token)
                else:
                    temp_list.append(str(token).split("|"))

        return temp_list
   
    def check_syntax(self, token_line):
        if len(token_line) > 0:
            if token_line[0] in statement:
                self.tokens_list.append(self.statement(token_line))
            elif token_line[0] in expression:
                self.tokens_list.append(self.binary_expression(token_line))
            elif token_line[0] in assignment or 'R' in token_line:
                self.tokens_list.append(self.assign_variable(token_line))
            
            if 'BTW' in token_line:
                self.tokens_list.append(self.process_comment(token_line))

            temp = []
            while len(token_line) > 0:
                token = token_line.pop(0)
                try:
                    value = list(self.lexemes_dict[token].keys())[0]
                    desc = list(self.lexemes_dict[token].values())[0]
                    print("HELLOO WORD",token, value)
                    temp.append(Token(token, value, desc))

                    if token == "IM IN YR" or "IM OUTTA YR":
                        token = token_line.pop(0)
                        print("SUOPP", token)
                        temp.append(Token(token, "LOOPIDENT", "Loop Identifier"))
                except:
                    None
            self.tokens_list.append(temp)
    
    def process_comment(self, token_line):
        temp = []
        i = token_line.index('BTW')
        token = token_line.pop(i)
        comment = token_line.pop(i)

        temp.append(self.convert_from_string(token))
        temp.append(Token(comment, "COMMENT", "User Comment"))
        print(temp)
        return temp
                

    def assign_variable(self, token_line):

        if token_line[0] == 'I HAS A':
            assign = token_line.pop(0)
            try:
                x = token_line.pop(0)
            except:
                print("'I HAS A' requires a variable but none was given")
            if len(token_line) > 0:
                itz = token_line.pop(0)
                if itz == 'ITZ':
                    try:
                        value = token_line.pop(0)
                    
                        if value in list(self.variable_dict.keys()):
                            print("value: ", value)
                        self.variable_dict[x] = value
                        return [self.convert_from_string(assign), self.convert_from_string(x), self.convert_from_string(itz), self.convert_from_string(value)]
                    except:
                        None
            else:
                try:
                    self.variable_dict[x] = None
                    return [self.convert_from_string(assign), self.convert_from_string(x)]
                except:
                    None
        elif 'R' in token_line:
            var = token_line.pop(0)

            if var in list(self.variable_dict.keys()) and token_line.pop(0) == 'R':
                try:
                    expr = token_line[0]

                    if expr in expression:
                        expr = self.binary_expression(token_line[:4])
                        del token_line[:4]

                    return [self.convert_from_string(var), self.convert_from_string('R'), self.convert_from_string(expr)]
                except:
                    None
    def statement(self, token_line):
        temp = []
        token = token_line.pop(0)
        value = list(self.lexemes_dict[token].keys())[0]
        desc = list(self.lexemes_dict[token].values())[0]

        temp.append(Token(token, value, desc))
        if token == 'VISIBLE':

            if len(token_line) != 0 and token_line[0] == 'SMOOSH':
                value = list(self.lexemes_dict[token_line[0]].keys())[0]
                desc = list(self.lexemes_dict[token_line[0]].values())[0]
                temp.append(Token(token, value, desc))
                # temp.append(self.convert_from_string(token_line.pop(0)))
                while len(token_line) > 1:
                    temp.append(self.convert_from_string(token_line.pop(0)))
                    if token_line[0] == 'AN':
                        temp.append(self.convert_from_string(token_line.pop(0)))
                    else:
                        print("There should be an AN keyword")
                temp.append(self.convert_from_string(token_line.pop(0)))
            


            # iimplement pa lang soon yung kapag may statement sa visible
            while len(token_line) > 0:
                token = token_line.pop(0)
                if token == "BTW":
                    temp.append(self.convert_from_string(token))
                    token = token_line.pop(0)
                    temp.append(Token(token, "Comment", "User Comment"))
                else:
                    temp.append(self.convert_from_string(token))
        
        elif token == 'GIMMEH':

            if len(token_line) > 0:
                temp.append(self.convert_from_string(token_line.pop(0)))

        elif token == 'SMOOSH':
            while len(token_line) > 1:
                temp.append(self.convert_from_string(token_line.pop(0)))
                if token_line[0] == 'AN':
                    temp.append(self.convert_from_string(token_line.pop(0)))
                else:
                    print("There should be an AN keyword")
            temp.append(self.convert_from_string(token_line.pop(0)))
        
        elif token == 'MAEK':
            token = token_line.pop(0)
            print("token: ", token)
            if token in list(self.variable_dict.keys()):
                temp.append(self.convert_from_string(token))
                print(token_line)
                token = token_line.pop(0)
                # print(token_line)
                if token == 'A':
                    temp.append(self.convert_from_string(token))
                    token = token_line.pop(0)
                    if token in ['NUMBR', 'NUMBAR', 'YARN', 'TROOF', 'NOOB']:
                        temp.append(self.convert_from_string(token))
                    else:
                        print("Error: not a literal type")
                else:
                    print("Error: Expected 'A'")
            else:
                print("Error: not a variable")

        
        return temp

    def binary_expression(self, token_line):
        try:
            token = token_line.pop(0)
            x,y = self.get_values(token_line)
            return [self.convert_from_string(token), self.convert_from_string(x), self.convert_from_string('AN'),self.convert_from_string(y)]
        except:
            return


    def get_values(self, expr):
        try:
            x = expr[0]
            if x in expression:
                x = self.binary_expression(expr[:4])
                del expr[:4]
            elif x == 'NOT':
                x = [self.convert_from_string(expr.pop(0)), self.convert_from_string(expr.pop(0))]
            else:
                x = expr.pop(0)
            token = expr.pop(0)

            if token == 'AN':
                y = expr[0]
                if y in expression:
                    y = self.binary_expression(expr)
                elif y == 'NOT':
                    y = [self.convert_from_string(expr.pop(0)), self.convert_from_string(expr.pop(0))]
                else:
                    y = expr.pop(0)

            # print("x: ", self.convert_from_string(x))
            return x,y
        except:
            return

    def convert_from_string(self, token):
        if isinstance(token, list):
            return token
        if token in list(self.lexemes_dict.keys()):
            value = list(self.lexemes_dict[token].keys())[0]
            desc = list(self.lexemes_dict[token].values())[0]
            return Token(token, value, desc)
        try:
            token = int(token)
            type = 'NUMBR'
        except ValueError:
            try:
                token = float(token)
                type = 'NUMBAR'
            except ValueError:
                if token in troof:
                    type = 'TROOF'
                elif token in list(self.variable_dict.keys()):
                    type = 'VARIDENT'
                elif "\"" in token or isinstance(token, str):
                    # token = token.replace("\"", "")
                    if token in comment or token in expression or token in assignment:
                        print("TOKKEEEEEEEEN\n: ", token)
                        value = list(self.lexemes_dict[token].keys())[0]
                        desc = list(self.lexemes_dict[token].values())[0]
                        return Token(token, value, desc)
                    type = 'YARN'
                else:
                    print(f'To be fixed: {token}')
                    return
        value = list(self.lexemes_dict[type].keys())[0]
        desc = list(self.lexemes_dict[type].values())[0]
        return Token(token, value, desc)
                
filename = os.path.basename("/Lexemes.csv")
def load_lex():
    with open(filename,'r') as f:
        lexemes = csv.reader(f)
        lexemes_list = {}

        for row in lexemes:
            string = row[0].replace("_"," ")
            lexemes_list[string] = {row[1]:row[2]}
        file = open('parseeeeer.txt','w')
        key = ""
        for key,value in lexemes_list.items():
            file.write(key + " " + str(value) + '\n')
        file.close()
        f.close()
        return lexemes_list
