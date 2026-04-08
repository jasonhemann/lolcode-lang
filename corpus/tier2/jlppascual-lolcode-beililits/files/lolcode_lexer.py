
import sys, getopt, re

literals = ['VARIDENT', 'NUMBR', 'NUMBAR', 'YARN', 'TROOF', 'NOOB', 'LOOPIDENT', 'FUNCIDENT']
statement = ['VISIBLE','LOOPIDENT','FUNCIDENT','MAEK','SMOOSH']
expression = ['SUMOF', 'DIFFOF', 'PRODOF','QUOOF', 'MODOF', 'BIGGROF', 'SMALLROF','BOTHOF','EITHEROF','WONOF','NOT','ANYOF','ALLOF']
rel_expr = ['BOTHSAEM', 'DIFFRINT']
variables = {}


class Token:
    def __init__(self, type_, value=None, desc=None):
        self.type = type_
        self.value = value
        self.desc = desc

    def __repr__(self):
        if self.value:
            return f'{self.type}|{self.value}|{self.desc}'
        else:
            return f'{self.type}'

class Lexer:
    def __init__(self, string_list, regex_dict):
        self.string_list = string_list
        self.regex_dict = regex_dict

    # bubble sort algorithm to sort the list based on their span (or index)
    def sorted_list(self, line_list):
        n = len(line_list)
        for i in range(n-1):
            for j in range(0, n-i-1):
                if line_list[j].span()[0] > line_list[j+1].span()[0]:
                    line_list[j], line_list[j+1] = line_list[j+1], line_list[j]
        
        for i in range(n):
            line_list[i] = line_list[i].group(0)
        return line_list

    def create_tokens(self):
        regex_list, count_list = self.find_tokens()

        index = 0
        sorted_regex_list = []
        string_list_copy = self.string_list
        while index < len(regex_list):
            temp_list = []
            
            strings = string_list_copy[int(count_list[index])-1]
            for regex in regex_list[index]:
                lexeme = re.search(re.escape(regex), strings)
                if lexeme != None:
                    # print("LEXEME: ",lexeme.group(0))
                    strings = strings.replace(lexeme.group(0), "."*len(lexeme.group(0)), 1)
                    # print(strings)

                    temp_list.append(lexeme)
            sorted_regex_list.append(self.sorted_list(temp_list))
            index += 1
        return sorted_regex_list

    def find_tokens(self):
        count = 0
        is_obtw = False
        var_temp = ""
        regex_list = []
        count_list = []
        comment_list = []
        for strings in self.string_list:
            if 'OBTW' in strings:
                count+=1
                comment_list.append('OBTW')
                count_list.append(count)
                regex_list.append(comment_list)
                comment_list = []
                is_obtw = True
                continue
            elif is_obtw and 'TLDR' not in strings:
                count+=1
                comment_list.append(strings)
                count_list.append(count)
                regex_list.append(comment_list)
                comment_list = []
                continue
            elif 'TLDR' in strings:
                count+=1
                comment_list.append('TLDR')
                count_list.append(count)
                regex_list.append(comment_list)
                comment_list = []
                is_obtw = False
                continue
            count += 1
            temp_list = []   
           
            if 'BTW' in strings and 'OBTW' not in strings:
                btw_index = strings.index("BTW")
                temp_list.append('BTW')
                comment = strings[btw_index:]
                temp_list.append(comment[3:])
                strings = strings[:btw_index]

            for regex in self.regex_dict:
                lexeme = re.findall(self.regex_dict[regex], strings)
                if lexeme != []:
                    if regex in literals: 
                        if len(lexeme) > 0:
                            for sub in lexeme:
                            # store all of the variables detected into a list
                                if regex == 'VARIDENT' and regex not in variables:
                                    var_temp = sub
                                    variables[sub] = None 
                                temp_list.append(sub)
                    else:                       
                        if regex == 'VALIDENT':
                            for sub in lexeme:
                                variables.update({var_temp:sub})
                                var_temp = ""
                        elif regex == 'LITERAL':
                            for sub in lexeme:
                                temp_list.append(sub)
                        elif regex == "VAR CATCH" or regex == "NON KEY": #for variables beside Conditional statements
                            for sub in lexeme:
                                if sub in variables:
                                    temp_list.append(sub)
                                else:
                                    temp_list.append(sub)
                        else:
                            if len(lexeme)>0:
                                for sub in lexeme:
                                    temp_list.append(regex)
                        
            if len(variables) != 0 :
                for word in variables:
                    if word in strings and word not in temp_list:
                        temp_list.append(word)

            if len(temp_list) != 0:
                regex_list.append(temp_list)
                count_list.append(count)
        # print(variables)
        # print(regex_list)
        return regex_list, count_list

def load_variables():
    return variables
    
def load_regex():
    with open('regex.txt', 'r') as f:
        regex_string = f.read()
    f.close()
    regex_string = regex_string.split("\n")

    regex_dict = {}
    
    for regex in regex_string:
        templist = regex.split(" ")
        strings = templist[0].replace("_", " ")
        if len(templist)<2 and templist[0] == '':
            pass
        else:
            regex_dict[strings] = templist[1]
    
    return regex_dict

def load_file():
    try:
        optlist, args = getopt.getopt(sys.argv[1:], 'f:') # reads args included in the terminal
    except getopt.GetoptError:
        sys.exit(1)

    file = None
    # option: -f ; value: <file name> 
    for option, value in optlist:
        if option == '-f':
            with open(value, 'r') as f:
                string1 = f.read()
            f.close()
            
    string_list = string1.split("\n")    
    return string_list
