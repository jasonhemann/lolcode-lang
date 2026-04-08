# regex patterns for different token types
TOKEN_REGEXES = [
    # updated keyword based on sample run on project specification
    ('COMMENT', r'\b(?:BTW[^\n]*|OBTW(?:.|\b|\n)*TLDR\n)'),  # match comments starting with BTW/OBTW
    ('Code Delimiter', r'(?:HAI|KTHXBYE)'),
    ('Variable Declaration Delimiter', r'(?:WAZZUP|BUHBYE)'),
    ('Variable Declaration', r'I HAS A'),
    ('Variable Initialization', r'ITZ'),
    ('NUMBAR Literal', r'(\-)?\d+\.\d+'),
    ('NUMBR Literal', r'\d+'),
    ('YARN Literal', r'"([^"]*)"'),  # match strings inside double quotes
    ('TROOF Literal', r'(?:WIN|FAIL)'),
    ('TYPE Literal', r'(?:NOOB|NUMBR|NUMBAR|YARN|TROOF)'),
    ('Boolean Operation', r'(?:BOTH OF|EITHER OF|WON OF|NOT|ANY OF|ALL OF)'),
    ('And Symbol', r'AN'),
    ('Symbol', r'[+\-*/=<>!]+'),
    ('Output Keyword', r'VISIBLE'),
    ('Input Keyword', r'GIMMEH'),
    ('Arithmetic Operation', r'(?:SUM OF|DIFF OF|PRODUKT OF|QUOSHUNT OF|MOD OF|BIGGR OF|SMALLR OF)'),
    ('Concatenation Keyword', r'SMOOSH'),
    ('Comparison Operation', r'(?:BOTH SAEM|DIFFRINT)'),
    ('Typecasting Keyword', r'(?:MAEK A|IS NOW A)'),
    ('Implicit Variable Keyword', r'IT'),
    ('Assignment Operation Keyword', r'R'),
    ('If-Then Statement Keyword', r'(?:O RLY\?|YA RLY|MEBBE|NO WAI|OIC)'),
    ('Switch Statement Keyword', r'(?:WTF\?|OMGWTF|OMG|OIC)'),
    ('Loop Keyword', r'(?:IM IN YR|UPPIN|NERFIN|TIL|WILE|IM OUTTA YR)'),
    ('Function Keyword', r'(?:HOW IZ I|IF U SAY SO)'),
    ('YR Keyword', r'YR'),
    ('Return Keyword', r'(?:GTFO|FOUND YR)'),
    ('Function Call Keyword', r'I IZ'),
    ('Delimiter', r'MKAY'),
    ('Identifier', r'[A-Za-z_][A-Za-z0-9_]*'),
    ('NEWLINE', r'[\n]+'),  #whitespace
    ('WHITESPACE', r'[ \t\b]+'),  #whitespace
    ('Command Breaks', r', '),
    ('Line Continuation', r'...\n'),
    ('MISC', r'.'),  #match any other single character (for error handling)
]