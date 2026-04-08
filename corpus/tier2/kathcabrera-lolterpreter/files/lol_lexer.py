import sys
import re
from dataclasses import dataclass

#one instance per lexeme
@dataclass
class Token:
    type: str #KEYWORD, IDENT, NUMBR, NUMBAR, YARN, TROOF, TYPE
    lexeme: str #exact text
    line: int #line number of token first char
    col: int #col number of token first char

#Regex building blocks

# Literals
YARN_RE   = r'"(?:[^"\\]|\\.)*"'                       
NUMBAR_RE = r'-?(?:\d+\.\d*|\.\d+)(?:[eE][+-]?\d+)?' #floats
NUMBR_RE  = r'-?\d+' #integers
TROOF_RE  = r'\b(?:WIN|FAIL)\b' #boolean
TYPE_RE   = r'\b(?:NOOB|NUMBR|NUMBAR|YARN|TROOF)\b' #type

#Keywords
KEYWORDS = [
    r'HOW\s+IZ\s+I', r'IF\s+U\s+SAY\s+SO', r'IM\s+IN\s+YR', r'IM\s+OUTTA\s+YR', 
    r'FOUND\s+YR', r'I\s+IZ', r'I\s+HAS\s+A', r'IS\s+NOW\s+A',
    r'SUM\s+OF', r'DIFF\s+OF', r'PRODUKT\s+OF', r'QUOSHUNT\s+OF', r'MOD\s+OF',
    r'BIGGR\s+OF', r'SMALLR\s+OF', r'BOTH\s+OF', r'EITHER\s+OF', r'WON\s+OF', r'NOT',
    r'ANY\s+OF', r'ALL\s+OF', r'BOTH\s+SAEM',
    r'O\s+RLY\?', r'YA\s+RLY', r'NO\s+WAI', r'WTF\?',r'AN',
    r'GIMMEH', r'VISIBLE', r'SMOOSH', r'MAEK\s+A', r'DIFFRINT', r'NOT',
    r'BTW', r'OBTW', r'TLDR', r'HAI', r'KTHXBYE', r'WAZZUP', r'BUHBYE',
    r'ITZ', r'R', r'OIC', r'MEBBE', r'A', r'MKAY', r'\+', r'OMG', r'OMGWTF', r'GTFO', r'UPPIN', r'NERFIN', r'TIL', r'WILE', r'YR'
]
#Long words are checked first
KEYWORDS.sort(key=lambda s: len(s), reverse=True)

KEYWORD_ALT = r'(?<!\w)(?:' + r'|'.join(KEYWORDS) + r')(?!\w)'

#for comments and whitespace
LINE_COMMENT_RE  = r'BTW[^\n]*' #after BTW to end of line
BLOCK_COMMENT_RE = r'OBTW(?:.|\n)*?TLDR'#non-greedy across lines
SKIP_WS_RE       = r'[ \t\r]+'#skip space and tabs

# Identifier 
#determines the role
IDENT_RE = r'[A-Za-z_][A-Za-z0-9_]*'

#Master token
TOKEN_SPEC = [
    ('BLOCK_COMMENT', BLOCK_COMMENT_RE),
    ('LINE_COMMENT',  LINE_COMMENT_RE),
    ('NEWLINE',        r'\n'),
    ('SKIP',           SKIP_WS_RE),

    #Literals
    ('YARN_LIT',           YARN_RE),
    ('NUMBAR_LIT',         NUMBAR_RE),
    ('NUMBR_LIT',          NUMBR_RE),
    ('TROOF_LIT',          TROOF_RE),
    ('TYPE_LIT',           TYPE_RE),

    #Keywords
    ('KEYWORD',        KEYWORD_ALT),

    #Identifier
    ('IDENT',          IDENT_RE),

    #Others
    ('MISMATCH',       r'.'),
]
#Compile a single master regex with named groups
MASTER_RE = re.compile('|'.join(f'(?P<{name}>{pat})' for name, pat in TOKEN_SPEC),
                       re.MULTILINE)

#iterates through the text left to right
def lex(text: str):
    line = 1
    col_start_of_line = 0
    
    #iterates over every match of MATCH_RE
    for m in MASTER_RE.finditer(text):
        type = m.lastgroup #checks named group
        lexeme = m.group() #checks the exact text that matched

        if type == 'NEWLINE':
            line += 1
            col_start_of_line = m.end()
            continue
        #Whitespace and comments are ignored 
        if type in ('SKIP', 'LINE_COMMENT', 'BLOCK_COMMENT'):
            continue
        #if no match then error on token
        if type == 'MISMATCH':
            # You can raise here; for milestone we’ll just report it
            c = m.start() - col_start_of_line + 1
            yield Token('ERROR', lexeme, line, c)
            continue

        col = m.start() - col_start_of_line + 1

        #Normalize KEYWORD lexeme
        if type == 'KEYWORD':
            lexeme = re.sub(r'\s+', ' ', lexeme)
        
        if type == 'YARN':
            inner = lexeme[1:-1]
            yield Token('STRING_QUOTE', '"', line, col)
            # Unescape display? The spec example shows raw inner; keep raw inner text
            yield Token('YARN_LIT', inner, line, col + 1)
            yield Token('STRING_QUOTE', '"', line, col + len(lexeme) - 1)
            continue

        yield Token(type, lexeme, line, col)
    

#Category mapping for keywords to required labels
# CODE_DELIMS = {'HAI', 'KTHXBYE'}
# VARLIST_DELIMS = {'WAZZUP', 'BUHBYE'}
# VAR_DECL = {'I HAS A'}
# ASSIGN_FOLLOWING_IHAS = {'ITZ'}
# OUTPUT_KEYWORDS = {'VISIBLE'}
# MULTI_PARAM_SEP = {'AN'}
ARITH_OPS = {
    'SUM OF': "SUM_OF", 
    'DIFF OF': "DIFF_OF", 
    'PRODUKT OF': "PRODUKT_OF", 
    'QUOSHUNT OF': "QUOSHUNT_OF", 
    'MOD OF': "MOD_OF"
    }
COMPARE_OPS  = {
    'BIGGR OF': "BIGGR_OF",
    'SMALLR OF': "SMALLR_OF",
    'BOTH SAEM': "BOTH_SAEM",
    'DIFFRINT': "DIFFRINT",
    'EITHER OF': "EITHER_OF",
    'BOTH OF': "BOTH_OF",
    'WON OF': "WON_OF",
    'NOT': "NOT",
    'ALL OF': "ALL_OF",
    'ANY OF': "ANY_OF"

   }
TYPECAST_OPS = {
    "IS NOW A": "IS_NOW_A",
    "MAEK A": "MAEK_A"
    }


def clean_lex(src):
    tokens = list(lex(src))
    index = 0

    for t in tokens:
        k = t.lexeme
        if t.type == 'KEYWORD':
            if k == "HAI":
                t.type = "CODE_START"
            elif k == "KTHXBYE":
                t.type = "CODE_END"
            elif k == "WAZZUP":
                t.type = "VARLIST_START"
            elif k == "BUHBYE":
                t.type = "VARLIST_END"
            elif k == "I HAS A":
                t.type = "VAR_DECL"
            elif k == "ITZ":
                t.type = "VAR_ASSIGN_ITZ"
            elif k == "GIMMEH":
                t.type = "GIMMEH"
            elif k == "VISIBLE":
                t.type = "VISIBLE"
            elif k == "AN":
                t.type = "AN"
            elif k in ARITH_OPS:
                t.type = ARITH_OPS[k]
            elif k in COMPARE_OPS:
                t.type = COMPARE_OPS[k]
            elif k == "+":
                t.type = "+"
            elif k == "SMOOSH":
                t.type = "SMOOSH"
            elif k == "R":
                t.type = "R"
            elif k in TYPECAST_OPS:
                t.type = TYPECAST_OPS[k]
            elif k == "MKAY":
                t.type = "MKAY"
            elif k == "O RLY?":
                t.type = "O_RLY?"
            elif k == "OIC":
                t.type = "OIC"
            elif k == "YA RLY":
                t.type = "YA_RLY"
            elif k == "NO WAI":
                t.type = "NO_WAI"
            elif k == "WTF?":
                t.type = "WTF?"
            elif k == "OMG":
                t.type = "OMG"
            elif k == "OMGWTF":
                t.type = "OMGWTF"
            elif k == "HOW IZ I":
                t.type = "HOW_IZ_I"
            elif k == "IF U SAY SO":
                t.type = "IF_U_SAY_SO"
            elif k == "FOUND YR":
                t.type = "FOUND_YR"
            elif k == "GTFO":
                t.type = "GTFO"
            elif k == "I IZ":
                t.type = "I_IZ"
            elif k == "IM IN YR":
                t.type = "IM_IN_YR"
            elif k == "IM OUTTA YR":
                t.type = "IM_OUTTA_YR"
            elif k == "TIL":
                t.type = "TIL"
            elif k == "WILE":
                t.type = "WILE"
            elif k == "YR":
                t.type = "YR"
            elif k == "UPPIN":
                t.type = "UPPIN"
            elif k == "NERFIN":
                t.type = "NERFIN"
   
    return tokens;            



def main():
    #reads the file input
    if len(sys.argv) != 2:
        print("Usage: python lol_lexer.py <source.lol>")
        sys.exit(1)

    #Read the file as UTF-8 text
    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        code = f.read()

    tokens = clean_lex(code)
    
    for token in tokens:
        print(f"Token\n\ttype:{token.type}\n\tlexeme:{token.lexeme}\n")

if __name__ == '__main__':
    main()
