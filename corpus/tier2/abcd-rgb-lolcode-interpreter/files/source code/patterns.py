# List of LOLCODE patterns


# === start and end of program ===
codeDelimiters = {
    ("HAI", "Start of Code Keyword"),
    ("KTHXBYE", "End of Code Keyword"),
}

# ================================



#  === comments ===
comments = {
    ("BTW", "Comment Keyword"),
    ("OBTW", "Start of Multiline Comment Keyword"),
    ("TLDR", "End of Multiline Comment Keyword"),
}
# =================


iKeyword = ("I", "I Keyword") 


# === variables ===
variableSegment = {
    ("WAZZUP", "Start of Variable Declaration Keyword"),
    ("BUHBYE", "End of Variable Declaration Keyword"),
}

variableInitialization = {
    ("ITZ", "Variable Initialization Keyword"),
}

IhasA = ("HAS", "A", "Variable Declaration Keyword")

# variableAssignment = {
#     ("R", "Variable Assignment Keyword"),
# }
# ==================


#  TODO
# === data types ===
yarnLiteral = ("\"([^\"]*)\"", "YARN Literal")
numbrLiteral = ("^-?[0-9]+$", "NUMBR Literal")
numbarLiteral = ("^(-)?[0-9]*\.?[0-9]+$", "NUMBAR Literal")
troofLiteral = ("WIN|FAIL", "TROOF Literal")
typeLiteral = ("NOOB|TROOF|NUMBR|NUMBAR|YARN", "TYPE Literal")
# ==================



# === input/output operations ===
ioKeyword = {
    ("GIMMEH", "Input Keyword"),
    ("VISIBLE", "Output Keyword")
}
# ===============================


anSymbol = {("AN", "Conjunction Symbol Keyword")}    # used in many operations


# === arithmetic operations ===
arithmeticOperators = {
    ("SUM", "Addition Operator Keyword"),
    ("DIFF", "Subtraction Operator Keyword"),
    ("PRODUKT", "Multiplication Operator Keyword"),
    ("QUOSHUNT", "Division Operator Keyword"),
    ("MOD", "Modulo Operator Keyword"),
    ("BIGGR", "Greater Symbol Keyword"),
    ("SMALLR", "Lesser Symbol Keyword"),
}

arithmeticOf = ("OF")
# =============================



# === concatenation ===
smooshKeyword = {("SMOOSH", "Concatenation Keyword")}
# =====================


bothSymbol = {("BOTH", "AND Symbol Keyword")}   # used in boolean and comparison operations


# === boolean operations ===
# Boolean Operators - Except Both
booleanOperators = {
    ("EITHER", "OR Symbol Keyword"),
    ("WON", "XOR Symbol Keyword"),
    ("NOT", "NOT Symbol Keyword"),
}

booleanOperatorsOf = ("OF")

# Infinite Boolean Operators
infBooleanOperators = {
    ("ALL", "Infinite Arity AND Symbol Keyword"),
    ("ANY", "infinite Arity OR Symbol Keyword"), 
}

endInfBooleanOperators = {("MKAY", "End Of Infinite Boolean Operators Keyword")}

infBooleanOperatorsOf = ("OF")
# ==========================



# === comparison operations ===
bothOperators = ("SAEM", "Equality Operator Keyword")
differentSymbol = {("DIFFRINT", "Inequality Operator Keyword")}
# =============================



# === typecasting statements ===
castSymbol= {
    ("MAEK", "Explicit Typecasting Keyword"),
    ("A", "Optional Typecasting Keyword"),
}

recastSymbol = {("IS", "Re-casting Keyword")}    

IsNowA = ("NOW", "A")
# ==============================



# === assignment statements ===
assignmentOperator = {
    ("R", "Assignment Operator Keyword")
}
# ==============================



# === flow-control statements ===
# If-then
ifThenOperator = {
    ("O", "If-Then Start Keyword"),
    ("YA", "If Statement Keyword"),
    ("NO", "Else Statement Keyword"),
    
}

mebbeOperator = {("MEBBE", "Else-if Statement Keyword")}

oRly = "RLY?"
yaRly = "RLY"
noWai = "WAI"

# Switch case
switchCaseOperators = {
    ("WTF?", "Switch Case Start Keyword"),
    ("OMG", "Case Operator Keyword"),
    ("OMGWTF", "Default Case Keyword")    
}

endFlowControl = {("OIC", "Control Flow End Keyword")}

# Loops
imKeyWord = ("IM")

loopKeyword = {
    ("IN", "Loop Start Keyword"),
    ("OUTTA", "Loop End Keyword")
}

yrKeyWordLoop = ("YR")    # used in loop and function

loopOperationKeyword = {
    ("UPPIN", "Increment Keyword"),
    ("NERFIN", "Decrement Keyword")
}

gtfoKeyWord = {("GTFO", "GTFO Keyword")}  # used in loop and function

loopConditionKeyWord = {
    ("TIL", "Loop Condition Keyword"),
    ("WILE", "Loop Condition Keyword")
}
# ================================



# === function definitions ===
functionKeyWord = {("HOW", "Function Definition Keyword")}

HowIzI = ("IZ", "I")

yrKeyWord = {("YR", "YR Keyword")}

exitFunction = {("IF", "Exit Function Keyword")}

ifUSaySo = ("U", "SAY", "SO") 
# ============================



# === function return ===
returnKeyWord = {("FOUND", "Return Keyword")}
# ========================



# === function call ===
Iiz = ("IZ", "Function Call Keyword")
# =====================



# === identifiers ===
identifier = ("^[a-zA-Z][a-zA-Z0-9_]*$", "Identifier")
# ===================
