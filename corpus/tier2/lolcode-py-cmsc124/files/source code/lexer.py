#Forked from https://gist.github.com/eliben/5797351
import re
from token_types import *
from error import LexerError

class Token(object):
    def __init__(self, type, val, pos, line):
        self.type = type
        self.val = val
        self.pos = pos
        self.line = line

    def __str__(self):
        return '%s: %s' % (self.type, self.val)


class Lexer(object):
    def __init__(self, skip_whitespace=True):
        rules = [
            # literal
            (r'\"[^\"]*\"',                               TT_STRING),
            (r'\bTROOF|NOOB|NUMBR|NUMBAR|YARN|TYPE\b',    TT_TYPE),
            (r'\bWIN|FAIL\b',                             TT_BOOLEAN),
            (r'\b-?\d+.\d+\b',                            TT_FLOAT),
            (r'\b0|-?[1-9][0-9]*\b',                      TT_INTEGER),

            # keywords
            #START
            (r'\bHOW\sIZ\sI\b',                           TT_FUNC_STRT),
            (r'\bIM\sIN\sYR\b',                           TT_LOOP_STRT),
            (r'\bHAI\b',                                  TT_CODE_STRT),

            #END
            (r'\bIF\sU\sSAY\sSO\b',                       TT_FUNC_END),
            (r'\bIM\sOUTTA\sYR\b',                        TT_LOOP_END),
            (r'\bKTHXBYE\b',                              TT_CODE_END),

            #OPERATOR
            (r'\bI\sHAS\sA\b',                            TT_VAR_DEC),
            (r'\bIS\sNOW\sA\b',                           TT_TYPECAST_1),
            (r'\bMAEK\b',                                 TT_TYPECAST_2),

            #Arithmetic
            (r'\bQUOSHUNT\sOF\b',                         TT_DIV_OP),
            (r'\bPRODUKT\sOF\b',                          TT_MUL_OP),
            (r'\bEITHER\sOF\b',                           TT_OR_OP),
            (r'\bDIFF\sOF\b',                             TT_SUB),
            (r'\bMOD\sOF\b',                              TT_MOD),
            (r'\bSUM\sOF\b',                              TT_SUMMATION),
            (r'\bNERFIN\b',                               TT_DEC),
            (r'\bUPPIN\b',                                TT_INC),

            #RELATIONAL
            (r'\bBOTH\sSAEM\b',                           TT_EQU_OP),
            (r'\bDIFFRINT\b',                             TT_NEQU),
            (r'\bBOTH\sOF\b',                             TT_AND),
            (r'\bALL\sOF\b',                              TT_AND_INF),
            (r'\bANY\sOF\b',                              TT_OR_INF),
            (r'\bNO\sWAI\b',                              TT_ELSE),
            (r'\bWON\sOF\b',                              TT_XOR),
            (r'\bNOT\b',                                  TT_NOT),

            #CONTROL
            (r'\bO\sRLY\?',                               TT_IF),
            (r'\bYA\sRLY\b',                              TT_TRUTH),
            (r'\bOMG\b',                                  TT_CASE),
            (r'\bOMGWTF\b',                               TT_BREAK),
            (r'\bGTFO\b',                                 TT_CASEBREAK),
            (r'\bMEBBE\b',                                TT_ELIF),
            (r'\bWTF\?',                                  TT_SWITCH),
            (r'\bWILE\b',                                 TT_WHILE),
            (r'\bTIL\b',                                  TT_UNTIL),
            (r'\bOIC\b',                                  TT_CONTROL_END),

            (r'\bI\sIZ\b',                                TT_FUNCALL),
            (r'\bFOUND\b',                                TT_RETURN),

            #OPERATION
            (r'\bVISIBLE\b',                              TT_OUTPUT),
            (r'\bGIMMEH\b',                               TT_READ),
            (r'\bSMOOSH\b',                               TT_CONCAT),
            (r'\bITZ\b',                                  TT_VAR_ASSIGN),
            (r'\bSMALLR\sOF\b',                           TT_MIN),
            (r'\bBIGGR\sOF\b',                            TT_MAX),
            (r'\bR\b',                                    TT_VAR_VAL_ASSIGN),

            #OTHERS
            (r'\bOBTW\b',                                 TT_COMMENT_MULTI_STRT),
            (r'\bTLDR\b',                                 TT_COMMENT_MULTI_END),
            (r'\bBTW\b',                                  TT_COMMENT_STRT),
            (r'\bMKAY\b',                                 TT_MKAY),
            (r'\bAN\b',                                   TT_ARG_SEP),
            (r'\bYR\b',                                   TT_YR),
            (r'\bA\b',                                    TT_A),
            (r'\!',                                       TT_SUPPRESS_NEWLINE),
            (r'\n|,',                                     TT_NEWLINE),

            #identifier
            (r'\b[a-zA-Z]\w*\b',                          TT_IDENTIFIER),
        ]

        regex_parts = []
        self.group_type = {}

        for index, (regex, classification) in enumerate(rules):
            #Define the name of the group
            groupname = 'GROUP%s' % index
            #Define Capture Groupname and the corresponding regex
            regex_parts.append('(?P<%s>%s)' % (groupname, regex))
            #Define the type of the groupname
            self.group_type[groupname] = classification

        #This is where all the rules get compiled separated by '|'. This is the only regex that will be used for checking Lexemes
        self.regex = re.compile('|'.join(regex_parts))

        #For white space checking
        self.regex_whitespace = re.compile('[\S\r\n]')

    def input(self, buf):
        self.buf = buf
        self.pos = 0
        self.line = 1

    
    def tokens(self):
        tokens = []
        while self.pos < len(self.buf):
            # check for whitespaces
            m = self.regex_whitespace.search(self.buf, self.pos)
            if m == None:
                #No match means end of file
                break
            
            #Get new starting position for regex searching
            self.pos = m.start()
            
            #Do regex match. check for comments and skip them.
            m = self.regex.match(self.buf, self.pos)
            if m == None:
                raise LexerError(self.pos,self.line)
            
            #Get the group that was matched
            groupname = m.lastgroup
            
            #Get the type of the token using the groupname
            tok_type = self.group_type[groupname]
            
            #increment the current line number if newline is seen
            if str(m.group(groupname)) == "\n":
                self.line += 1
                
            if str(m.group(groupname)) == "BTW":
                #Get the current token using the groupname. The actual token is in m.group(groupname). 
                #The Token class is just a struct to store information about the current token.
                tok = Token(tok_type, m.group(groupname), self.pos, self.line)
                
                #Update the position
                self.pos = m.end()
            
                newline = re.compile(r"\n")
                endtok = newline.search(self.buf, self.pos)

                if endtok:
                    #Get new starting position for regex searching
                    self.pos = endtok.start()
                else:
                    self.pos = len(self.buf)
                
                tokens.append(tok)
            elif str(m.group(groupname)) == "OBTW":
                #Get the current token using the groupname. The actual token is in m.group(groupname). 
                #The Token class is just a struct to store information about the current token.
                tok = Token(tok_type, m.group(groupname), self.pos, self.line)
                
                #Update the position
                self.pos = m.end()
                
                newline = re.compile(r"TLDR")
                endtok = newline.search(self.buf, self.pos)
                
                self.line += len(re.compile(r"\n").findall(self.buf,self.pos,endtok.start()))

                if endtok:
                    #Get new starting position for regex searching
                    self.pos = endtok.start()
                else:
                    self.pos = len(self.buf)

                tokens.append(tok)
            elif tok_type in (TT_STRING):
                #Get the current token using the groupname. The actual token is in m.group(groupname). 
                #The Token class is just a struct to store information about the current token.
                
                #Update the position
                
                delim1 = Token(TT_STR_DELIMITER, "\"", self.pos-1, self.line)
                tok = Token(tok_type, "", self.pos, self.line)
                if len(m.group(groupname)) > 2:
                    tok = Token(tok_type, m.group(groupname)[1:-1], self.pos, self.line)
                self.pos = m.end()
                delim2 = Token(TT_STR_DELIMITER, "\"", self.pos, self.line)
                tokens.append(delim1)
                tokens.append(tok)
                tokens.append(delim2)
            else:
                #Get the current token using the groupname. The actual token is in m.group(groupname). 
                #The Token class is just a struct to store information about the current token.
                tok = Token(tok_type, m.group(groupname), self.pos, self.line)
                #Update the position
                self.pos = m.end()
                
                tokens.append(tok)
        
        return tokens

#  if __name__ == "__main__":
#      lx = Lexer()
#      lx.input("""
#               HAI
#  I HAS A rope ITZ SUM OF SUM OF 1 AN 3 AN SUM OF 1 AN SUM OF 1 AN 1
#  VISIBLE "HELLO!"
#  VISIBLE "THIS PROGRAM WORKS LOL!"
#  VISIBLE rope
#  KTHXBYE
#               """)
#      for x in lx.tokens():
#          pass
#
