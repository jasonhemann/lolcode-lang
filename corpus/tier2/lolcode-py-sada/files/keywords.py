import re
import sys
import semantics
import syntax

compiled_lex = []
symbol_table = []


class LOLLexer:
    def __init__(self, source_code_file):
        self.source_code = source_code_file
        self.tokens = []
        self.current_position = 0

    #
    def tokenize(self):
        hasobtw = 0
        while self.current_position < len(self.source_code):
            
            # Print the current value at the position
            current_value = self.source_code[self.current_position:self.current_position + 10]
            
            token = self.match_token()
            if token is not None:
                if hasobtw == 0 and token.value[0:4] == 'OBTW': #check if the value of token is OBTW
                    hasobtw = 1 
                if hasobtw == 1:
                    if token.value == 'TLDR': #toggle the hasobtw if there is TLDR
                        hasobtw = 0
                    # else: continue

                if token.type == 'Special Characters' : #para makuha rin mga may special char sa loob ng obtw
                    if hasobtw != 1:
                        continue
                self.tokens.append(token) #appends the token to the tokens list
            else:
                break
        return self.tokens


    #responsible for the actual checking and matching in regex
    def match_token(self):
        for pattern, token_type in token_patterns.items():
            match = re.match(pattern, self.source_code[self.current_position:]) #checks if it matches any pattern in the token_patters
            if match:
                value = match.group(0)
                self.current_position += len(value)
                return Token(token_type, value)     #returns the Token
        return None

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

# Updated LOLCODE token patterns to allow for indentation
token_patterns = {

    # Keywords [<type>, <classification>]
    r'\s*HAI\s+': 'Code Delimiter',
    r'\s*KTHXBYE\s+': 'Code Delimiter',
    r'\s*WAZZUP\s+': 'Variable Declaration Delimiter',
    r'\s*BUHBYE\s+': 'Variable Declaration Delimiter',
    r'\s*TLDR\s+': 'Comment Delimiter',
    r'((\s*^BTW .*)|( ^BTW .*)|(\s*^OBTW .*)|( ^OBTW .*))': 'Comment Line',
    r'\s*I HAS A\s+': 'Variable Declaration',
    r'\s*ITZ\s+': 'Variable Assignment',
    r'\s*R\s+': 'Variable Assignment',
    r'\s*AN\s+': 'Parameter Delimiter',                                   
    r'\s*SUM OF\s+': 'Arithmetic Operation',
    r'\s*DIFF OF\s+': 'Arithmetic Operation',
    r'\s*PRODUKT OF\s+': 'Arithmetic Operation',
    r'\s*QUOSHUNT OF\s+': 'Arithmetic Operation',
    r'\s*MOD OF\s+': 'Arithmetic Operation',
    r'\s*BIGGR OF\s+': 'Arithmetic Operation',
    r'\s*SMALLR OF\s+': 'Arithmetic Operation',
    r'\s*BOTH OF\s+': 'Boolean Operation',
    r'\s*EITHER OF\s+': 'Boolean Operation',
    r'\s*WON OF\s+': 'Boolean Operation',
    r'\s*NOT\s+': 'Boolean Operation',
    r'\s*ANY OF\s+': 'Boolean Operation',
    r'\s*ALL OF\s+': 'Boolean Operation',
    r'\s*BOTH SAEM\s+': 'Comparison Operation',
    r'\s*DIFFRINT\s+': 'Comparison Operation',
    r'\s*SMOOSH\s+': 'String Contatenation',
    r'\s*MAEK\s+': 'Typecasting Operation',
    r'\s*A\s+': 'Typecasting Operation',                   
    r'\s*IS NOW A\s+': 'Typecasting Operation',
    r'\s*VISIBLE\s+': 'Output Keyword',
    r'\s*\+\s+': 'Output Delimiter',
    r'\s*GIMMEH\s+': 'Input Keyword',
    r'\s*O\sRLY\?\s+': 'If-then Keyword',
    r'\s*YA RLY\s+': 'If-then Keyword',
    r'\s*MEBBE\s+': 'If-then Keyword',
    r'\s*NO WAI\s+': 'If-then Keyword',
    r'\s*OIC\s+': 'If-then Keyword',
    r'\s*WTF\?\s+': 'Switch-Case Keyword',
    r'\s*OMG\s+': 'Switch-Case Keyword',
    r'\s*OMGWTF\s+': 'Switch-Case Keyword',
    r'\s*IM IN YR\s+': 'Loop Keyword',
    r'\s*UPPIN\s+': 'Loop Operation',
    r'\s*NERFIN\s+': 'Loop Operation',
    r'\s*YR\s+': 'Parameter Delimiter',
    r'\s*TIL\s+': 'Loop Keyword',
    r'\s*WILE\s+': 'Loop Keyword',
    r'\s*IM OUTTA YR\s+': 'Loop Keyword',
    r'\s*HOW IZ I\s+': 'Function Keyword',
    r'\s*IF U SAY SO\s+': 'Function Keyword',
    r'\s*GTFO\s+': 'Return Keyword',
    r'\s*FOUND YR\s+': 'Return keyword',
    r'\s*I IZ\s+': 'Function Call',
    r'\s*MKAY\s+': 'Concatenation Delimiter',                              
    r'\s*NOOB\s+': 'Void Literal',

    # Literals and variable identifiers
    r'\s*(NUMBR|NUMBAR|YARN|TROOF|NOOB)\s?' : 'Type Literal',  
    r'\s*(WIN|FAIL)\s*': 'TROOF Literal',                 
    r'\s*[a-zA-Z][a-zA-Z0-9_]*\s*': 'Identifier',           
    r'\s*-?(0|[1-9][0-9]*)?\.[0-9]+\s*': 'NUMBAR Literal',  
    r'\s*0\s*|^-?[1-9][0-9]*\s*': 'NUMBR Literal',     
    r'\s*\"[^\"]*\"\s*': 'YARN Literal',   
    r'\s?.*\s?': 'Special Characters'          
}

def lex(str):
    literals=['YARN Literal', 'NUMBR Literal', 'NUMBAR Literal', 'Identifier', 'TROOF Literal', 'Type Literal']
    compiled_lex.clear()
    varidents = []
    code = str
    toRemove = []
    if code.strip() != "":  # to avoid error when there is no input
        lexer = LOLLexer(code)
        tokens = lexer.tokenize()
        hastldr = -1
        hasobtw = -1
        comment_line = ""
        toRemove = []
        indexToinsert = []
        yarnLiterals = []
        
        
        for i in range(0, len(tokens)):
            if i != len(tokens):
                temp = tokens[i].value.rstrip()  # remove leading and trailing space characters 
                val = temp.lstrip()
                if hasobtw == 0 and val != 'TLDR':
                    comment_line += tokens[i].value
                    toRemove.append(tokens[i]) #remove the words after the OBTW 
                elif tokens[i].type == 'YARN Literal':
                    if val[0] == '"' and val[-1] == '"': #if it is enclosed by quotes then append it to list
                        yarnLiterals.append(tokens[i])
                elif 'BTW' == val[0:3]: #separate lexeme for BTW and for the comment line
                    tokens[i].value = val[3:]
                    comment = Token('Comment Delimiter', 'BTW')
                    tokens.insert(i, comment)
                elif 'OBTW' == val[0:4]: #separate lexeme for OBTW and for the comment line
                    hasobtw = 0
                    tokens[i].value = val[4:]
                    comment = Token('Comment Delimiter', 'OBTW')
                    tokens.insert(i, comment)
                elif 'TLDR' == val:
                    indexToinsert.append(tokens[i]) #get idex to insert the comment line after OBTW
                    hasobtw = 1
                elif tokens[i].type == 'Variable Declaration':
                    if tokens[i+1].type == 'Identifier':
                        varidents.append(tokens[i+1].value.lstrip().rstrip())
                        tokens[i+1].type = 'Variable Identifier'
                elif tokens[i].type == 'Loop Keyword':
                    if tokens[i+1].type == 'Identifier':
                        tokens[i+1].type = 'Loop Identifier'
                elif tokens[i].type == 'Function Keyword' or tokens[i].type == 'Function Call':
                    if tokens[i+1].type == 'Identifier':
                        tokens[i+1].type = 'Function Identifier'
                elif tokens[i].type == 'Identifier' and tokens[i].value.lstrip().rstrip() in varidents:
                        tokens[i].type = 'Variable Identifier'

        
        for k in toRemove: #remove tokens made after OBTW in tokens
            tokens.remove(k)

        if comment_line != '' and hasobtw == 1: #add the comment line to lexeme
            comment_block = comment_line.replace('\n',' ').rstrip().lstrip()
            comment = Token('Comment Line', comment_block)
            index = tokens.index(indexToinsert[0])
            tokens.insert(index, comment)
        
        if len(yarnLiterals) != 0: # add the " " separately and the yarn
                for i in yarnLiterals: #i is tokens[i]
                        temp = i.value.rstrip()  # remove leading and trailing space characters 
                        val = temp.lstrip()
                        new = Token('String Delimiter', '"')
                        index = tokens.index(i)
                        i.value = val[1:-1]
                        tokens.insert(index, new)
                        tokens.insert(index+2, new)

        yarnLiterals.clear()   
        comment_line = ''
        for token in tokens:
                if token.type != "YARN Literal": #if it is not yarn, remove trailing and leading spaces
                    temp = token.value.rstrip() 
                    val = temp.lstrip()
                    compiled_lex.append([val, token.type])
                else: #if it is yarn, append the value as it is to retain spaces
                    compiled_lex.append([token.value, token.type])
        return compiled_lex
    
def connect_UI(str):
    compiled_lex.clear()
    return lex(str)
    
#IT VALUE GETTER
def get_IT():
     return symbol_table[0][1]
