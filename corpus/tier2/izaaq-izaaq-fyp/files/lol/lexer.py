"""
LOLCODE lexer - define tokens and their regex so they are recognised on input.
Also handles any special behaviour for certain tokens (ie, must remove quotes from string)
"""

from sly import Lexer

class LexerLOL(Lexer):
    tokens = {
        LOOPERATOR,
        LOOPCONDITION,
        IDENTIFIER,
        STRING,
        INTEGER,
        FLOAT,
        BOOLEAN,
        I_HAS_A,
        ITZ,
        R,
        IS_NOW_A,
        TYPE,
        VISIBLE,
        GIMMEH,
        SUM_OF,
        DIFF_OF,
        PRODUKT_OF,
        QUOSHUNT_OF,
        MOD_OF,
        BIGGR_OF,
        SMALLR_OF,
        BOTH_OF,
        EITHER_OF,
        WON_OF,
        NOT,
        MKAY,
        BOTH_SAEM,
        DIFFRINT,
        O_RLY,
        YA_RLY,
        MEBBE,
        NO_WAI,
        IM_IN_YR,
        IM_OUTTA_YR,
        YR,
        GTFO,
        HAI,
        KTHXBYE,
        HOW_IZ_I,
        I_IZ,
        AN,
        FOUND_YR,
        IF_U_SAY_SO,
        OIC,
        EOL
    }

    ignore = '\t '  # ignore whitespace and indentation
    literals = { '!', '?' }

    # Define regex for tokens to be recognized in input
    I_HAS_A         = r'I\s+HAS\s+A\b'
    ITZ             = r'ITZ\b'
    R               = r'R\b'
    IS_NOW_A        = r'IS\s+NOW\s+A\b'
    TYPE            = r'((?:NUMBA?R)|(?:YARN)|(?:TROOF)|(?:NOOB))\b'
    VISIBLE         = r'VISIBLE\b'
    GIMMEH          = r'GIMMEH\b'
    SUM_OF          = r'SUM\s+OF\b'
    DIFF_OF         = r'DIFF\s+OF\b'
    PRODUKT_OF      = r'PRODUKT\s+OF\b'
    QUOSHUNT_OF     = r'QUOSHUNT\s+OF\b'
    MOD_OF          = r'MOD\s+OF\b'
    BIGGR_OF        = r'BIGGR\s+OF\b'
    SMALLR_OF       = r'SMALLR\s+OF\b'
    BOTH_OF         = r'BOTH\s+OF\b'
    EITHER_OF       = r'EITHER\s+OF\b'
    WON_OF          = r'WON\s+OF\b'
    NOT             = r'NOT\b'
    MKAY            = r'MKAY\b'
    BOTH_SAEM       = r'BOTH\s+SAEM\b'
    DIFFRINT        = r'DIFFRINT\b'
    O_RLY           = r'O\s+RLY\b'
    YA_RLY          = r'YA\s+RLY\b'
    MEBBE           = r'MEBBE\b'
    NO_WAI          = r'NO\s+WAI\b'
    IM_IN_YR        = r'IM\s+IN\s+YR\b'
    IM_OUTTA_YR     = r'IM\s+OUTTA\s+YR\b'
    YR              = r'YR\b'
    GTFO            = r'GTFO\b'
    HAI             = r'HAI\b'
    KTHXBYE         = r'KTHXBYE\b'
    HOW_IZ_I        = r'HOW\s+IZ\s+I\b'
    I_IZ            = r'I\s+IZ\b'
    AN              = r'AN\b'
    FOUND_YR        = r'FOUND\s+YR\b'
    IF_U_SAY_SO     = r'IF\s+U\s+SAY\s+SO\b'
    OIC             = r'OIC\b'


    @_(r'[+-]?\d+\.\d+')
    def FLOAT(self, t):
        # convert into python float
        t.value = float(t.value)
        return t

    @_(r'[+-]?\d+')
    def INTEGER(self, t):
        # convert it into python integer
        t.value = int(t.value)
        return t

    @_(r'\".*?\"')
    def STRING(self, t):
        # convert into python string - remove double quotes
        t.value = t.value.strip('"')
        return t

    @_(r'(?:WIN)|(?:FAIL)')
    def BOOLEAN(self, t):
        if t.value == 'WIN':
            t.value = True
        elif t.value == 'FAIL':
            t.value = False

        return t

    @_(r'BTW\s[^\n]*')
    def COMMENT(self, t):
        pass

    @_(r',|\n')
    def EOL(self, t):
        if t.value == '\n':
            self.lineno += 1
        t.value = 'EOL'
        return t

    @_(r'(?:UPPIN)|(?:NERFIN)')
    def LOOPERATOR(self, t):
        if t.value == 'UPPIN':
            t.value = 'increment'
        elif t.value == 'NERFIN':
            t.value = 'decrement'
        return t

    @_(r'(?:TIL)|(?:WILE)')
    def LOOPCONDITION(self, t):
        return t

    # Newline token
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    IDENTIFIER = r'[a-zA-Z_][a-zA-Z0-9_]*'

    def error(self, t):
        print(f"Line {self.lineno}: Bad character '{t.value[0]}'")
        self.index += 1
