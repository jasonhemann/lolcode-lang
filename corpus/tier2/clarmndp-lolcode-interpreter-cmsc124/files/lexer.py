# We define token types for lexical analysis
import re
string_lit =  r'"[^"]*"'
numbr= r"-?\d+"
numbar= r"-?\d*(\.)\d+"
addition= r"SUM OF"
subtraction = r"DIFF OF"
multiplication = r"PRODUKT OF"
division= r"QUOSHUNT OF"
space= r"[\s]"
an= r"AN"
equal= r"R"
visible= r"VISIBLE"
varname =r"[A-Za-z][A-Za-z\d]*"
TOKEN_TYPES = {
    "KEYWORD": "KEYWORD",
    "STRING": "STRING",
    "NUMBER": "NUMBER",
    "LITERAL": "LITERAL",
    "IDENTIFIER": "IDENTIFIER",
    "OPERATOR": "OPERATOR",
    "DELIMITER": "DELIMITER",
    "COMMENT": "COMMENT",
    "WHITESPACE": "WHITESPACE",
    "TROOF": "TROOF",
    "NUMBR": "NUMBR",
    "NUMBAR": "NUMBAR"
}

# LOLCODE keywords
KEYWORDS = {
    # Program structure
    "HAI": "program_start",
    "KTHXBYE": "program_end",
    "WAZZUP": "variable_section_start",
    "BUHBYE": "variable_section_end",
        
    # Comments
    "BTW": "single_line_comment",
    "OBTW": "multi_line_comment_start",
    "TLDR": "multi_line_comment_end",
        
    # Variables and assignments
    "I HAS A": "variable_declaration",
    "ITZ": "assignment",
    "R": "assignment_operator",
        
    # Input/output
    "VISIBLE": "print",
    "GIMMEH": "input",

    # Boolean operators
    "BOTH OF": "and",
    "EITHER OF": "or",
    "WON OF": "xor",
    "NOT": "not",
    "ANY OF": "infinite_or",
    "ALL OF": "infinite_and",

    # Arithmetic operators
    "SUM OF": "addition",
    "DIFF OF": "subtraction",
    "PRODUKT OF": "multiplication",
    "QUOSHUNT OF": "division",
    "MOD OF": "modulus",
    "BIGGR OF": "maximum",
    "SMALLR OF": "minimum",
        
    # Comparison operators
    "BOTH SAEM": "equality",
    "DIFFRINT": "inequality",
        
    # String operation
    "SMOOSH": "string_concatenation",
        
    # Type casting
    "MAEK": "cast_operator",
    "A": "cast_delimiter",
    "IS NOW A": "typecast",
        
    # Condition statements
    "O RLY?": "if_start",
    "YA RLY": "then",
    "MEBBE": "else_if",
    "NO WAI": "else",
    "OIC": "if_end",
        
    # Switch cases
    "WTF?": "switch",
    "OMG": "case",
    "OMGWTF": "default_case",
        
    # Loops
    "IM IN YR": "loop_start",
    "UPPIN": "increment",
    "NERFIN": "decrement",
    "YR": "loop_variable",
    "TIL": "until",
    "WILE": "while",
    "IM OUTTA YR": "loop_end",
        
    # Function declarations
    "HOW IZ I": "function_declaration",
    "IF U SAY SO": "function_end",
    "GTFO": "return",
    "FOUND YR": "return_value",
    "I IZ": "function_call",
        
    # Infinite arity
    "MKAY": "infinite_arity_end"
}
keyword= ["SUM OF", "VISIBLE","+", "DIFF OF","PRODUKT OF", "QUOSHUNT OF",
          "BOTH SAEM", "DIFFRINT", "BIGGR OF", "SMALLR OF","MOD OF",
          "BOTH OF", "EITHER OF", "WON OF", "NOT","WIN","FAIL", "ALL OF","MKAY","ANY OF",
          "I HAS A", "ITZ","WAZZUP","BUHBYE", 
          "SMOOSH",
          "R","MAEK","IS NOW A"
          "GIMMEH"
          ]

class Token:
    """ Parameter 'type' provides the category for TOKEN_TYPES
        Parameter 'value' holds the text/ content
    """
    def __init__(self, type, value):
        self.type = type
        self.value = value

class Lexer:  
    # We convert source code by line into tokens
    def definer(self, line):
        tokens = []
        # Boolean keywords  
        BOOLEAN_VALUES = {
            "WIN": Token(TOKEN_TYPES["TROOF"], True),
            "FAIL": Token(TOKEN_TYPES["TROOF"], False),
            "NOOB": Token(TOKEN_TYPES["LITERAL"], None),
        }
        # token_elem=r'|'.join([re.escape(keyword_elem) for keyword_elem in keyword]) + r'|\S+' # Seperate by space
        token_elem =  r'|'.join([re.escape(keyword_elem) for keyword_elem in keyword]) +r'|'+r'"[^"]*"|\S+'+r'|' +r"-?\d+"+r'|'+r'\S+'
        token_elem=re.findall(token_elem,line)
        # print(token_elem)
        for temp_str in token_elem:
            if temp_str == "KTHXBYE":
                tokens.append(Token("end", temp_str.strip()))
            
            elif re.search(visible, temp_str):
                tokens.append(Token("expression", temp_str.strip()))
                
            elif re.search(string_lit, temp_str):
                tokens.append(Token(TOKEN_TYPES["STRING"], temp_str.strip()))
                
            elif re.search(addition, temp_str):
                tokens.append(Token("arithmetic_operator", temp_str.strip()))
                
            elif re.search(subtraction, temp_str):
                tokens.append(Token("arithmetic_operator", temp_str.strip()))
               
            elif re.search(division, temp_str):
                tokens.append(Token("arithmetic_operator", temp_str.strip()))
                
            elif re.search(multiplication, temp_str):
                tokens.append(Token("arithmetic_operator", temp_str.strip()))
            
            elif re.search(r"MOD OF", temp_str):
                tokens.append(Token("arithmetic_operator", temp_str))
            
            elif re.search(r"BOTH SAEM", temp_str):
                tokens.append(Token("comparison_operator", temp_str))
            
            elif re.search(r"DIFFRINT", temp_str):
                tokens.append(Token("comparison_operator", temp_str))
            
            elif re.search(r"BOTH OF", temp_str):
                tokens.append(Token("boolean_operator", temp_str))
            
            elif re.search(r"EITHER OF", temp_str):
                tokens.append(Token("boolean_operator", temp_str))
            
            elif re.search(r"WON OF", temp_str):
                tokens.append(Token("boolean_operator", temp_str))
            
            elif re.search(r"NOT", temp_str):
                tokens.append(Token("boolean_operator", temp_str))
            
            elif re.search(r"ALL OF", temp_str):
                tokens.append(Token("boolean_operator", temp_str))
            
            elif re.search(r"ANY OF", temp_str):
                tokens.append(Token("boolean_operator", temp_str))
            
            elif re.search(r"MKAY", temp_str):
                tokens.append(Token("inf_arity_delimeter", temp_str))
            
            elif re.search(r"BIGGR OF", temp_str):
                tokens.append(Token("arithmetic_operator", temp_str))
            
            elif re.search(r"SMALLR OF", temp_str):
                tokens.append(Token("arithmetic_operator", temp_str))
            
            elif re.search(an, temp_str):
                tokens.append(Token("delimeter", temp_str))
            
            elif re.search(r"WAZZUP", temp_str):
                tokens.append(Token("declaration_start", temp_str))
            
            elif re.search(r"BUHBYE", temp_str):
                tokens.append(Token("declaration_end", temp_str))
            
            elif re.search(r"I HAS A", temp_str):
                tokens.append(Token("declaration_keyword", temp_str))
            
            elif re.search(r"ITZ", temp_str):
                tokens.append(Token("declaration_delimiter", temp_str))
            
            elif re.search(r"WIN", temp_str):
                tokens.append(Token(TOKEN_TYPES["TROOF"], "WIN"))
            
            elif re.search(r"FAIL", temp_str):
                tokens.append(Token(TOKEN_TYPES["TROOF"], "FAIL"))
            
            elif re.search(r"SMOOSH", temp_str):
                tokens.append(Token("concatenation", temp_str))
            
            elif re.search(r"R", temp_str):
                tokens.append(Token("reassignment_delimeter", temp_str))
            
            elif re.search(r"MAEK A", temp_str):
                tokens.append(Token("typecasting_delimeter", temp_str))
            
            elif re.search(r"IS NOW A", temp_str):
                tokens.append(Token("typecasting_delimeter", temp_str))
            
            elif re.search(r"GIMMEH", temp_str):
                tokens.append(Token("input", temp_str))
            
            elif re.search(r"\+", temp_str):
                tokens.append(Token("visible_concat", temp_str))
            
            elif re.search(varname, temp_str):
                tokens.append(Token("variable", temp_str))
            
            elif re.fullmatch(numbar, temp_str):
                tokens.append(Token(TOKEN_TYPES["NUMBAR"], float(temp_str)))
            
            elif re.fullmatch(numbr, temp_str):
                tokens.append(Token(TOKEN_TYPES["NUMBR"], int(temp_str)))

        print(tokens)
        return tokens