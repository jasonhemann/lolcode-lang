import re  # Regular expressions
import patterns as p

class Lexeme:
    def __init__(self, keyword, token_type):
        self.keyword = keyword
        self.token_type = token_type

    def __repr__(self):  # For debugging
        return f"Lexeme({self.keyword}, {self.token_type})"

def lexer(input_file):
    # Remove comments BTW, OBTW, TLDR
    with open(input_file, "r") as f:
        f = f.read().splitlines()
        f = [line.strip() for line in f]    # remove traling and leading spaces 

        clean_string = ""
        isComment = False # Flag to check if the line is a comment
        
        # Remove comments
        for line in f:
            # If OBTW is found, remove the rest of the lines until TLDR is found
            if (re.search("OBTW", line)):
                line = re.sub("OBTW", "", line)
                isComment = True
            
            # If TLDR is found, remove the rest of the line
            if (isComment):
                if (re.search("TLDR", line)):
                    line = re.sub("TLDR.*", "", line)
                    isComment = False
                else:
                    line = ""
                
            # If TLDR is found, remove the rest of the line
            if (re.search("TLDR", line)):
                line = re.sub("TLDR.*", "", line)
            
            # If BTW is found, remove the rest of the line
            if (re.search("BTW", line)):
                line = re.sub("BTW.*", "", line)

            # If line is not empty, add it to the clean string
            if (line != ""):
                clean_string += line + "\n"
                
    #print(f"clean string:\n{clean_string}\n")
    
    # tokenize
    tokens = []
    curr_keyword = ""                
    string_flag = False     # to catch strings
    # this loop will tokenize the string into keywords, symbols, and literals
    for letter in clean_string:
        # if not in string, check for keywords
        if not string_flag:
            if letter == '"': # if string is found, set flag to true then append the string
                string_flag = True
                tokens.append(letter)
            elif letter == " " or letter == "\n":
                if curr_keyword != "":
                    tokens.append(curr_keyword)
                    curr_keyword = ""
                if letter == "\n":
                    next
            else:
                curr_keyword += letter
        else: # if in string, append the string until the end of the string
            if letter == '"':
                string_flag = False
                tokens.append(curr_keyword)
                curr_keyword = ""
                tokens.append(letter)
            else:
                curr_keyword += letter

    
    # Helper function to look ahead by one token
    def lookAhead(tokens, i):
        if (i+1 < len(tokens)):
            return tokens[i+1]
        else:
            return None
        
    def lookBehind(tokens, i):
        if (i-1 >= 0):
            return tokens[i-1]
        else:
            return None

    # identify classification of tokens
    lexemes = []

    i = 0

    while i < len(tokens):
        detected = False # If token is detected, skip to next token
        # Symbol Detection for code delimiters 
        continue_flag = False
        for symbol in p.codeDelimiters:
            if tokens[i] == symbol[0]:
                lexemes.append(Lexeme(tokens[i], symbol[1])) # append the symbol and its token type
                detected = True # set flag to true to skip to next token
             
                break # break the loop to skip to next token
        
        # Symbol Detection for variable segment
        for symbol in p.variableSegment:
            if tokens[i] == symbol[0]:
                lexemes.append(Lexeme(tokens[i], symbol[1]))
                detected = True        
                break
        
        # Symbol Detection for variable declaration
        for symbol in p.iKeyword:
            if tokens[i] == symbol[0]:
                if (lookAhead(tokens, i) == p.Iiz[0]): # check if the next token is IZ
                    lexemes.append(Lexeme(tokens[i] + " " + lookAhead(tokens, i), p.Iiz[1]))
                    detected = True
                    i+=2
                    detected = False
                    continue_flag = True
                    break
                # Check if the next two tokens are HAS A
                elif ((lookAhead(tokens, i), lookAhead(tokens, i+1))  == (p.IhasA[0], p.IhasA[1])):
                    lexemes.append(Lexeme(tokens[i] + " " + lookAhead(tokens, i) + " " + lookAhead(tokens, i+1), p.IhasA[2]))
                    detected = True
                    i+=3
                    detected = False
                    continue_flag = True
                    break
        
        # For variable initialization
        for symbol in p.variableInitialization:
            if tokens[i] == symbol[0]:
                lexemes.append(Lexeme(tokens[i], symbol[1]))
                detected = True 
                break
        
        # For input and output
        for symbol in p.ioKeyword:
            if tokens[i] == symbol[0]:
                lexemes.append(Lexeme(tokens[i], symbol[1]))
                detected = True       
                break
        
        # For conjunctions
        for symbol in p.anSymbol:
            if tokens[i] == symbol[0]:
                lexemes.append(Lexeme(tokens[i], symbol[1]))
                detected = True
                break
            
        # For arithmetic operators
        for symbol in p.arithmeticOperators:
            if tokens[i] == symbol[0]:
                if (lookAhead(tokens, i) == p.arithmeticOf):
                    lexemes.append(Lexeme(tokens[i] + " " + lookAhead(tokens, i), symbol[1]))
                    detected = True
                    i+=2
                    detected = False
                    continue_flag = True
                    break

        # For concatenation
        for symbol in p.smooshKeyword:
            if tokens[i] == symbol[0]:
                lexemes.append(Lexeme(tokens[i], symbol[1]))
                detected = True
                break

        # For both operators
        for symbol in p.bothSymbol:
            if tokens[i] == symbol[0]:
                next_token = lookAhead(tokens, i)
                if next_token == p.booleanOperatorsOf:
                    lexemes.append(Lexeme(tokens[i] + " " + next_token, symbol[1]))
                    detected = True
                    i+=2
                    detected = False
                    continue_flag = True
                    break
                elif next_token == p.bothOperators[0]:
                    lexemes.append(Lexeme(tokens[i] + " " + next_token, p.bothOperators[1]))
                    detected = True
                    i+=2
                    detected = False
                    continue_flag = True
                    break

        #  For boolean operators 
        for symbol in p.booleanOperators:
            if tokens[i] == symbol[0]:
                if (tokens[i] == "NOT"):
                    lexemes.append(Lexeme(tokens[i], symbol[1]))
                    detected = True
                    break
                if (lookAhead(tokens, i) == p.booleanOperatorsOf):
                    lexemes.append(Lexeme(tokens[i] + " " + lookAhead(tokens, i), symbol[1]))
                    detected = True
                    i+=2
                    detected = False
                    continue_flag = True
                    break

        # For infinite arity boolean operators    
        for symbol in p.infBooleanOperators:
            if tokens[i] == symbol[0]:
                if (lookAhead(tokens, i) == p.infBooleanOperatorsOf):
                    lexemes.append(Lexeme(tokens[i] + " " + lookAhead(tokens, i), symbol[1]))
                    detected = True
                    i+=2
                    detected = False
                    continue_flag = True
                    break

        # For end of infinite arity boolean operators 
        for symbol in p.endInfBooleanOperators:
            if tokens[i] == symbol[0]:
                lexemes.append(Lexeme(tokens[i], symbol[1]))
                detected = True             
                break
            
        # For not equal
        for symbol in p.differentSymbol:
            if tokens[i] == symbol[0]:
                lexemes.append(Lexeme(tokens[i], symbol[1]))
                detected = True
                break

        # For typecasting
        for symbol in p.castSymbol:
            if tokens[i] == symbol[0]:
                lexemes.append(Lexeme(tokens[i], symbol[1]))
                detected = True
                break

        # For type recasting
        for symbol in p.recastSymbol:
            if tokens[i] == symbol[0]:
                next_tokens = (lookAhead(tokens, i), lookAhead(tokens, i+1))
                if next_tokens == p.IsNowA:
                    lexemes.append(Lexeme(tokens[i] + " " + next_tokens[0] + " " + next_tokens[1], symbol[1]))
                    detected = True
                    i+=3
                    detected = False
                    break

        # For assignment operators
        for symbol in p.assignmentOperator:
            if tokens[i] == symbol[0]:
                lexemes.append(Lexeme(tokens[i], symbol[1]))
                detected = True
                break

        # For if-then operators
        for symbol in p.ifThenOperator:
            if tokens[i] == symbol[0]:
                next_token = lookAhead(tokens, i)
                
                if symbol[0] == "O":
                    if next_token == p.oRly:
                        lexemes.append(Lexeme(tokens[i] + " " + next_token, symbol[1]))
                        detected = True
                        i+=2
                        detected = False
                        continue_flag = True
                    
                elif symbol[0] == "YA":
                    if next_token == p.yaRly:
                        lexemes.append(Lexeme(tokens[i] + " " + next_token, symbol[1]))
                        detected = True
                        i+=2
                        detected = False
                        continue_flag = True
                    
                elif symbol[0] == "NO":
                    if next_token == p.noWai:
                        lexemes.append(Lexeme(tokens[i] + " " + next_token, symbol[1]))
                        detected = True
                        i+=2
                        detected = False
                        continue_flag = True

        # For switch case operators  
        for symbol in p.switchCaseOperators:
            if tokens[i] == symbol[0]:
                lexemes.append(Lexeme(tokens[i], symbol[1]))
                detected = True
                break

        # For end of switch case operators
        for symbol in p.endFlowControl:
            if tokens[i] == symbol[0]:
                lexemes.append(Lexeme(tokens[i], symbol[1]))
                detected = True
                break
            
        # For I'm outta yr loop
        if tokens[i] == p.imKeyWord:
            for symbol in p.loopKeyword:
                second_token = lookAhead(tokens, i)
                if second_token == symbol[0]:
                    third_token = lookAhead(tokens, i+1)
                    if third_token == p.yrKeyWordLoop:
                        lexemes.append(Lexeme(tokens[i] + " " + second_token + " " + third_token, symbol[1]))
                        detected = True
                        i+=3
                        detected = False
                        continue_flag = True
                        break
        
        # For loop operators            
        for symbol in p.loopOperationKeyword:
            if tokens[i] == symbol[0]:
                lexemes.append(Lexeme(tokens[i], symbol[1]))
                detected = True
                break
        # GTFO
        for symbol in p.gtfoKeyWord:
            if tokens[i] == symbol[0]:
                lexemes.append(Lexeme(tokens[i], symbol[1]))
                detected = True
        # Mebbe
        for symbol in p.mebbeOperator:
            if tokens[i] == symbol[0]:
                lexemes.append(Lexeme(tokens[i], symbol[1]))
                detected = True
                break
            
        # For loop condition operators
        for symbol in p.loopConditionKeyWord:
            if tokens[i] == symbol[0]:
                lexemes.append(Lexeme(tokens[i], symbol[1]))
                detected = True
                break

        # For functions
        for symbol in p.functionKeyWord:
            if tokens[i] == symbol[0]:
                next_token1 =lookAhead(tokens, i)
                next_token2= lookAhead(tokens, i+1)
                if next_token1 == p.HowIzI[0] and next_token2 == p.HowIzI[1]:
                    lexemes.append(Lexeme(tokens[i] + " " + next_token1 + " " + next_token2, symbol[1]))
                    detected = True
                    i+=3
                    detected = False
                    continue_flag = True
                    break

        # For returning values 
        for symbol in p.returnKeyWord:
            if tokens[i] == symbol[0]:
                next_token = lookAhead(tokens, i)
                if next_token == p.yrKeyWordLoop:
                    lexemes.append(Lexeme(tokens[i] + " " + next_token, symbol[1]))
                    detected = True
                    i+=2
                    detected = False
                    continue_flag = True
                    break
                
        # For exiting functions
        for symbol in p.exitFunction:
            if tokens[i] == symbol[0]:
                next_tokens = (lookAhead(tokens, i), lookAhead(tokens, i+1), lookAhead(tokens, i+2))
                if next_tokens == p.ifUSaySo:
                    lexemes.append(Lexeme(tokens[i] + " " + next_tokens[0] + " " + next_tokens[1] + " " + next_tokens[2], symbol[1]))
                    detected = True
                    i+=4       
                    detected = False
                    continue_flag = True
                    break
        
        if continue_flag:
            continue
        
    
        # For string delimiter
        if tokens[i] == "\"":
            lexemes.append(Lexeme(tokens[i], "String Delimiter"))
            detected = True

        # For visible concatenation
        if tokens[i] == "+":
            lexemes.append(Lexeme(tokens[i], "Visible Concatenation Symbol"))
            detected = True

        # For newline suppression
        if tokens[i] == "!":
            lexemes.append(Lexeme(tokens[i], "Newline Suppression Symbol"))
            detected = True

        # Literals
        if not detected:
            # Check if numbr
            if re.search(p.numbrLiteral[0], tokens[i]):
                lexemes.append(Lexeme(tokens[i], p.numbrLiteral[1]))
                detected = True
            # Check if numbar
            elif re.search(p.numbarLiteral[0], tokens[i]):
                lexemes.append(Lexeme(tokens[i], p.numbarLiteral[1]))
                detected = True
            # Check if troof
            elif re.search(p.troofLiteral[0], tokens[i]):
                lexemes.append(Lexeme(tokens[i], p.troofLiteral[1]))
                detected = True
            # Check if string
            elif lookBehind(tokens, i) == "\"" and lookAhead(tokens, i) == "\"":
                lexemes.append(Lexeme(tokens[i], p.yarnLiteral[1]))
                detected = True
            # Check if type literal
            elif re.search(p.typeLiteral[0], tokens[i]):
                lexemes.append(Lexeme(tokens[i], p.typeLiteral[1]))
                detected = True
            

        # identifiers
        if not detected:
            search = re.search(p.identifier[0], tokens[i])
            if search != None:
                lexemes.append(Lexeme(tokens[i], p.identifier[1]))
                detected = True
        
        if not detected:
            # Raise an error
            raise Exception(f"Lexical Error: {tokens[i]} is not a valid token")
        
        detected = False      
        i+=1
    
    # print lexemes
    # for lexeme in lexemes:
    #     print("========================================")
    #     print(f"KEYWORD: {lexeme.keyword}\nTOKEN TYPE: {lexeme.token_type}")
    
    return lexemes
            
            
def main():
    pass
    

if __name__ == "__main__":
    main()
