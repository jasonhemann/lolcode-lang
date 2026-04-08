import re
from enum import Enum, auto
from typing import List, Optional

class TokenType(Enum):
    # Identifiers
    VARIABLE_IDENTIFIER = auto()
    FUNCTION_IDENTIFIER = auto()
    LOOP_IDENTIFIER = auto()
    
    # Literals
    NUMBR = auto()
    NUMBAR = auto()
    YARN = auto()
    TROOF = auto()
    TYPE = auto()
    
    # Keywords
    HAI = auto()
    KTHXBYE = auto()
    WAZZUP = auto()
    BUHBYE = auto()
    BTW = auto()
    OBTW = auto()
    TLDR = auto()
    I_HAS_A = auto()
    ITZ = auto()
    R = auto()
    SUM_OF = auto()
    DIFF_OF = auto()
    PRODUKT_OF = auto()
    QUOSHUNT_OF = auto()
    MOD_OF = auto()
    BIGGR_OF = auto()
    SMALLR_OF = auto()
    BOTH_OF = auto()
    EITHER_OF = auto()
    WON_OF = auto()
    NOT = auto()
    ANY_OF = auto()
    ALL_OF = auto()
    BOTH_SAEM = auto()
    DIFFRINT = auto()
    SMOOSH = auto()
    MAEK = auto()
    A = auto()
    IS_NOW_A = auto()
    VISIBLE = auto()
    GIMMEH = auto()
    O_RLY = auto()
    YA_RLY = auto()
    MEBBE = auto()
    NO_WAI = auto()
    OIC = auto()
    WTF = auto()
    OMG = auto()
    OMGWTF = auto()
    IM_IN_YR = auto()
    UPPIN = auto()
    NERFIN = auto()
    YR = auto()
    TIL = auto()
    WILE = auto()
    IM_OUTTA_YR = auto()
    HOW_IZ_I = auto()
    IF_U_SAY_SO = auto()
    GTFO = auto()
    FOUND_YR = auto()
    I_IZ = auto()
    MKAY = auto()
    NOOB = auto()
    
    # Special
    AN = auto()
    LINEBREAK = auto()
    ERROR = auto()
    EOF = auto()
    CONCATENATE = auto()  # New token type for concatenation

class Token:
    def __init__(self, type: TokenType, value: str, line: int, position: int):
        self.type = type
        self.value = value
        self.line = line
        self.position = position
        
    
    def __str__(self):
        return f"Token({self.type}, '{self.value}', line {self.line}, pos {self.position})"

class LexicalAnalyzer:
    def __init__(self):
        self.tokens: List[Token] = []
        self.current_line = 1
        self.current_position = 0
        
        # Define regex patterns
        self.patterns = {
            # Identifiers
            'variable_identifier': r'[A-Za-z][A-Za-z0-9_]*',
            'function_identifier': r'[A-Za-z][A-Za-z0-9_]*',
            'loop_identifier': r'[A-Za-z][A-Za-z0-9_]*',
            
            # Literals
            'numbr': r'-?(0|[1-9][0-9]*)',
            'numbar': r'-?(0|[1-9][0-9]*)\.[0-9]+',
            'yarn': r'"([^"\\]*(\\.[^"\\]*)*)"',  # Updated regex to match YARN correctly
            'troof': r'WIN|FAIL',
            'type': r'NUMBR|NUMBAR|TROOF|YARN|NOOB',
            
            # Keywords (sorted by length to match longest first)
            'keywords': {
                'I HAS A': TokenType.I_HAS_A,
                'HOW IZ I': TokenType.HOW_IZ_I,
                'IF U SAY SO': TokenType.IF_U_SAY_SO,
                'IM OUTTA YR': TokenType.IM_OUTTA_YR,
                'IM IN YR': TokenType.IM_IN_YR,
                'IS NOW A': TokenType.IS_NOW_A,
                'FOUND YR': TokenType.FOUND_YR,
                'BOTH SAEM': TokenType.BOTH_SAEM,
                'DIFFRINT': TokenType.DIFFRINT,
                'KTHXBYE': TokenType.KTHXBYE,
                'PRODUKT OF': TokenType.PRODUKT_OF,
                'QUOSHUNT OF': TokenType.QUOSHUNT_OF,
                'SMALLR OF': TokenType.SMALLR_OF,
                'BIGGR OF': TokenType.BIGGR_OF,
                'EITHER OF': TokenType.EITHER_OF,
                'BOTH OF': TokenType.BOTH_OF,
                'SUM OF': TokenType.SUM_OF,
                'DIFF OF': TokenType.DIFF_OF,
                'MOD OF': TokenType.MOD_OF,
                'WON OF': TokenType.WON_OF,
                'ANY OF': TokenType.ANY_OF,
                'ALL OF': TokenType.ALL_OF,
                'WAZZUP': TokenType.WAZZUP,
                'BUHBYE': TokenType.BUHBYE,
                'VISIBLE': TokenType.VISIBLE,
                'GIMMEH': TokenType.GIMMEH,
                'O RLY?': TokenType.O_RLY,
                'OIC': TokenType.OIC,
                'YA RLY': TokenType.YA_RLY,
                'NO WAI': TokenType.NO_WAI,
                'OMGWTF': TokenType.OMGWTF,
                'UPPIN': TokenType.UPPIN,
                'NERFIN': TokenType.NERFIN,
                'MAEK': TokenType.MAEK,
                'I IZ': TokenType.I_IZ,
                'MKAY': TokenType.MKAY,
                'GTFO': TokenType.GTFO,
                'OBTW': TokenType.OBTW,
                'TLDR': TokenType.TLDR,
                'WTF?': TokenType.WTF,
                'OMG': TokenType.OMG,
                'HAI': TokenType.HAI,
                'BTW': TokenType.BTW,
                'NOT': TokenType.NOT,
                'TIL': TokenType.TIL,
                'WILE': TokenType.WILE,
                'ITZ': TokenType.ITZ,
                'YR': TokenType.YR,
                'AN': TokenType.AN,
                'R': TokenType.R,
                'A': TokenType.A,
                '+': TokenType.CONCATENATE,  # Treat '+' as a concatenation operator
                'SMOOSH': TokenType.SMOOSH,
                'NOON': TokenType.NOOB
            }
        }

    def tokenize(self, code: str) -> List[Token]:
        self.tokens = []
        self.current_line = 1
        self.current_position = 0
        
        # Split code into lines while preserving line breaks
        lines = code.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            self.current_line = line_num
            self.current_position = 0

            self.tokenize_line(line)
            
            # Add linebreak token
            if line_num < len(lines):
                self.tokens.append(Token(TokenType.LINEBREAK, '\\n', line_num, len(line)))

        self.tokens.append(Token(TokenType.EOF, 'EOF', line_num, len(line)))

        return self.tokens

    def tokenize_line(self, line: str) -> None:
        while self.current_position < len(line):
            # Skip whitespace
            if line[self.current_position].isspace():
                self.current_position += 1
                continue

            token = self.match_token(line[self.current_position:])
           
            if token:
                self.tokens.append(token)
                self.current_position += len(token.value)
            else:
                # Handle unrecognized character
                self.tokens.append(Token(
                    TokenType.ERROR,
                    line[self.current_position],
                    self.current_line,
                    self.current_position
                ))
                self.current_position += 1
        

    def match_token(self, text: str) -> Optional[Token]:
        # Try matching keywords first (longest matches first)
        for keyword, token_type in self.patterns['keywords'].items():
            if text.startswith(keyword):
                return Token(token_type, keyword, self.current_line, self.current_position)
        
        # Try matching literals
        for pattern_name in ['numbar', 'numbr', 'yarn', 'troof', 'type']:
            pattern = self.patterns[pattern_name]
            match = re.match(pattern, text)
            if match:
                value = match.group(0)
                token_type = TokenType[pattern_name.upper()]
                return Token(token_type, value, self.current_line, self.current_position)
            

        # Try matching identifiers
        identifier_match = re.match(self.patterns['variable_identifier'], text)
        if identifier_match:
            value = identifier_match.group(0)
            if self.tokens[-1].type == TokenType.IM_IN_YR or self.tokens[-1].type == TokenType.IM_OUTTA_YR:
                return Token(TokenType.LOOP_IDENTIFIER, value, self.current_line, self.current_position)
            elif self.tokens[-1].type == TokenType.HOW_IZ_I or self.tokens[-1].type == TokenType.I_IZ:
                return Token(TokenType.FUNCTION_IDENTIFIER, value, self.current_line, self.current_position)
            return Token(TokenType.VARIABLE_IDENTIFIER, value, self.current_line, self.current_position)
            
        
        return None

class LexicalError(Exception):
    def __init__(self, message: str, line: int, position: int):
        self.message = message
        self.line = line
        self.position = position
        super().__init__(f"Lexical Error at line {line}, position {position}: {message}")