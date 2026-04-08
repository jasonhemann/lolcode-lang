from .generic_lexer import *
from .multi_line_comment_validator import *

# ═════════════════════════════════════════════════════════════════════════════════════════════════
# LOLCODE LEXER
# ═════════════════════════════════════════════════════════════════════════════════════════════════
# Indices
TOKEN_VALUE = 0
TOKEN_TAG = 1
TOKEN_LINE_NUMBER = 2

# Keywords
HAI = 'Program Start Delimeter'
KTHXBYE = 'Program End Delimeter'
WAZZUP = 'Variable Declaration Start Delimeter'
BUHBYE = 'Variable Declaration End Delimeter'
I_HAS_A ='Variable Declaration'
ITZ = 'Variable Initialization'
R = 'Assignment Keyword'

# Arithmetic Operations
SUM_OF = 'Addition Operator'
DIFF_OF = 'Subtraction Operator'
PRODUKT_OF = 'Multiplication Operator'
QUOSHUNT_OF = 'Division Operator'
MOD_OF = 'Modulus Operator'
BIGGR_OF = 'Greater Than Operator'
SMALLR_OF = 'Less Than Operator'
BOTH_OF = 'AND Operator'
EITHER_OF = 'OR Operator'
WON_OF = 'XOR Operator'
NOT = 'NOT Operator'
ANY_OF = 'ANY Operator'
ALL_OF = 'ALL Operator'
BOTH_SAEM = 'Equality Operator'
DIFFRINT = 'Inequality Operator'
SMOOSH = 'String Concatenate Operator'
MAEK_A = 'Typecast Operator'
IS_NOW_A = 'Typecast IS NOW A Operator'

# Part of the expression for operands
AN = 'Operand Connector'
YR = 'Parameter Variable'
AN_YR = 'Additional Parameter Variable'

# Statements
VISIBLE = 'Print Statement'
VISIBLE_OPERATOR = 'Print Statement Delimiter'
GIMMEH = 'Input Statement'
O_RLY = 'Conditional Start Delimeter'
YA_RLY = 'If Clause'
MEBBE = 'Else-If Clause'
NO_WAI = 'Else Clause'
OIC = 'Conditional End Delimeter'
WTF = 'Switch-Case Start Delimeter'
OMG = 'Case Clause'
OMGWTF = 'Switch-Case End Delimeter'
IM_IN_YR = 'Loop Start Delimeter'
UPPIN = 'Increment Operator'
NERFIN = 'Decrement Operator'
TIL = 'Until Loop'
WILE = 'While Loop'
IM_OUTTA_YR = 'Loop End Delimeter'
# Functions
HOW_IZ_I = 'Function Start Delimeter'
IF_U_SAY_SO = 'Function End Delimeter'
GTFO = 'Function Return'
FOUND_YR = 'Function Return Value'
I_IZ = 'Function Call'
MKAY = 'Statement End Delimeter'

# Literals
NUMBR = 'Integer'
NUMBAR = 'Float'
TROOF = 'Boolean'
YARN = 'String'
LITERAL_TYPE = 'Literal Type'

NOOB = "NULL"

# Identifier
IDENTIFIER = 'Identifier'

# End of File
EOF = 'End of File'

# Make sure that the pattern matches as a whole word, excluding it from being part of larger words.
def bound(pattern):
    return rf'(?<!\w){pattern}(?!\w)'

token_exprs = [
    (r'[ \n\t]+',                             None),   # whitespace (ignore)
    (r'BTW[^\n]*',                            None),   # single line comments (ignore)
    (r'OBTW\s*((.|\n)*?)\s*TLDR',             None),   # multi-line comments (ignore)
    (bound('HAI'),                            HAI),
    (bound('KTHXBYE'),                        KTHXBYE),
    (bound('WAZZUP'),                         WAZZUP),
    (bound('BUHBYE'),                         BUHBYE),
    (bound('I HAS A'),                        I_HAS_A),
    (bound('ITZ'),                            ITZ),
    (bound('R'),                              R),
    (bound('SUM OF'),                         SUM_OF),
    (bound('DIFF OF'),                        DIFF_OF),
    (bound('PRODUKT OF'),                     PRODUKT_OF),
    (bound('QUOSHUNT OF'),                    QUOSHUNT_OF),
    (bound('MOD OF'),                         MOD_OF),
    (bound('BIGGR OF'),                       BIGGR_OF),
    (bound('SMALLR OF'),                      SMALLR_OF),
    (bound('BOTH OF'),                        BOTH_OF),
    (bound('EITHER OF'),                      EITHER_OF),
    (bound('WON OF'),                         WON_OF),
    (bound('NOT'),                            NOT),
    (bound('ANY OF'),                         ANY_OF),
    (bound('ALL OF'),                         ALL_OF),
    (bound('AN YR'),                          AN_YR),
    (bound('AN'),                             AN),
    (bound('BOTH SAEM'),                      BOTH_SAEM),
    (bound('DIFFRINT'),                       DIFFRINT),
    (bound('SMOOSH'),                         SMOOSH),
    (bound('MAEK A'),                           MAEK_A),
    (bound('IS NOW A'),                       IS_NOW_A),
    (bound('VISIBLE'),                        VISIBLE),
    (bound('GIMMEH'),                         GIMMEH),
    (bound(r'O RLY\?'),                        O_RLY),
    (bound('YA RLY'),                         YA_RLY),
    (bound('MEBBE'),                          MEBBE),
    (bound('NO WAI'),                         NO_WAI),
    (bound('OIC'),                            OIC),
    (bound(r'WTF\?'),                          WTF),
    (bound('OMG'),                            OMG),
    (bound('OMGWTF'),                         OMGWTF),
    (bound('IM IN YR'),                       IM_IN_YR),
    (bound('UPPIN'),                          UPPIN),
    (bound('NERFIN'),                         NERFIN),
    (bound('YR'),                             YR),
    (bound('TIL'),                            TIL),
    (bound('WILE'),                           WILE),
    (bound('IM OUTTA YR'),                    IM_OUTTA_YR),
    (bound('HOW IZ I'),                       HOW_IZ_I),
    (bound('IF U SAY SO'),                    IF_U_SAY_SO),
    (bound('GTFO'),                           GTFO),
    (bound('FOUND YR'),                       FOUND_YR),
    (bound('I IZ'),                           I_IZ),
    (bound('MKAY'),                           MKAY),
    (r'\+',                                   VISIBLE_OPERATOR),
    (bound(r'-?[0-9]+\.[0-9]+'),               NUMBAR),          # Float
    (bound('-?[0-9]+'),                       NUMBR),           # Integer
    (bound('"[^"]*"'),                        YARN),            # String
    (bound('(WIN|FAIL)'),                     TROOF),           # Boolean
    (bound('NOOB'),                           NOOB),          # NOOB literal type
    (bound('(NUMBR|NUMBAR|YARN|TROOF)'), LITERAL_TYPE),    # Type
    (bound('[a-zA-Z][a-zA-Z0-9_]*'),          IDENTIFIER),      # Identifier
]

def lolcode_lex(characters):
    validate_multiline_comments(characters) # Validate the existence of multi-line comments
    return lex(characters, token_exprs)
