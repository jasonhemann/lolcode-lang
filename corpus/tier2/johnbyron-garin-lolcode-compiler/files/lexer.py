# module for regular expression operations
import re
# file = open("/Users/JETHRO/Desktop/test_tkinter/read.lol")

# Regular expressions for LOLCode Programming Language
token_patterns = [
    (r'HAI', 'HAI'),
    (r'KTHXBYE', 'KTHXBYE'),
    (r'WAZZUP', 'WAZZUP'),
    (r'BUHBYE', 'BUHBYE'),
    (r'OBTW(?:.|\n)*?TLDR', 'MULTI_LINE_COMMENT'),
    (r'BTW.*', 'INLINE_COMMENT'),
    (r'I HAS A', 'I_HAS_A'),
    (r'ITZ', 'ITZ'),
    (r'R', 'R'),
    (r'\+', 'PLUS'),
    (r'SUM OF', 'SUM_OF'),
    (r'DIFF OF', 'DIFF_OF'),
    (r'PRODUKT OF', 'PRODUKT_OF'),
    (r'QUOSHUNT OF', 'QUOSHUNT_OF'),
    (r'MOD OF', 'MOD_OF'),
    (r'BIGGR OF', 'BIGGR_OF'),
    (r'SMALLR OF', 'SMALLR_OF'),
    (r'BOTH OF', 'BOTH_OF'),
    (r'EITHER OF', 'EITHER_OF'),
    (r'WON OF', 'WON_OF'),
    (r'NOT', 'NOT'),
    (r'ANY OF', 'ANY_OF'),
    (r'ALL OF', 'ALL_OF'),
    (r'BOTH SAEM', 'BOTH_SAEM'),
    (r'DIFFRINT', 'DIFFRINT'),
    (r'SMOOSH', 'SMOOSH'),
    (r'MAEK', 'MAEK'),
    (r'AN', 'AN'),
    (r'A', 'A'),
    (r'IS NOW A', 'IS_NOW_A'),
    (r'VISIBLE', 'VISIBLE'),
    (r'GIMMEH', 'GIMMEH'),
    (r'O RLY\?', 'O_RLY'),
    (r'YA RLY', 'YA_RLY'),
    (r'MEBBE', 'MEBBE'),
    (r'NO WAI', 'NO_WAI'),
    (r'OIC', 'OIC'),
    (r'OMGWTF', 'OMGWTF'),
    (r'WTF\?', 'WTF'),
    (r'OMG', 'OMG'),
    (r'IM IN YR', 'IM_IN_YR'),
    (r'UPPIN.', 'UPPIN'),
    (r'NERFIN.', 'NERFIN'),
    (r'YR', 'YR'),
    (r'TIL.', 'TIL'),
    (r'WILE.', 'WILE'),
    (r'IM OUTTA YR', 'IM_OUTTA_YR'),
    (r'HOW IZ I', 'HOW_IZ_I'),
    (r'IF U SAY SO', 'IF_U_SAY_SO'),
    (r'GTFO', 'GTFO'),
    (r'FOUND YR', 'FOUND_YR'),
    (r'I IZ', 'I_IZ'),
    (r'MKAY', 'MKAY'),
    (r'YARN', 'YARN'),
    (r'NUMBR', 'NUMBR'),
    (r'NUMBAR', 'NUMBAR'),
    (r'TROOF', 'TROOF'),
    (r'NOOB', 'NOOB_LITERAL'),
    (r'"[^"]*"', 'YARN_LITERAL'),
    (r'(-?\d+\.\d+)|(-?\.\d+)|(-?\d+\.)', 'NUMBAR_LITERAL'),
    (r'-?\d+', 'NUMBR_LITERAL'),
    (r'WIN|FAIL', 'TROOF_LITERAL'),
    (r'\s+', 'WHITESPACE'),  # Include whitespace as a token
    (r'[A-Za-z][A-Za-z0-9_]*', 'IDENTIFIER'),  # Variable and Function Identifier
]

'''
-> defines a function tokenize that takes a LOLCODE program (code) as input
-> initializes an empty list tokens to store the identified tokens
-> position is set to 0 to keep track of the parsing position in the code

-> initiates a while loop to iterate through the code until the end is reached
-> initializes the variable match to None for later use

-> the for loop iterates through each regular expression and token type in token_patterns list
-> attempts to match the regular expression against the code starting from the current position

-> if no match is found or the end of the code is reached, the while loop is terminated
-> returns the list of tokens identified during the tokenization process
'''
def tokenize(code):
    tokens = []
    position = 0

    while position < len(code):
        match = None
        for pattern, token_type in token_patterns:
            regex = re.compile(pattern)
            match = regex.match(code, position)
            if match:
                value = match.group(0)
                tokens.append((value, token_type))
                position = match.end()
                break

        if not match or position == len(code):
            break

    return tokens
