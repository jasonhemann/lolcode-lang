import re

def identify_tokens(lines):
    identifier_pattern = re.compile(r'^[A-Za-z][A-Za-z0-9_]', re.IGNORECASE)
    numbr_pattern = re.compile(r'^-?\d+$', re.IGNORECASE)
    numbar_pattern = re.compile(r'^-?\d+\.\d+$', re.IGNORECASE)
    yarn_pattern = re.compile(r'^\"(.*?)\"$', re.IGNORECASE)
    troof_pattern = re.compile(r'^(WIN|FAIL)$', re.IGNORECASE)
    type_pattern = re.compile(r'^(NUMBR|NUMBAR|YARN|TROOF|NOOB)$', re.IGNORECASE)

    keywords = ["HAI", "KTHXBYE", "WAZZUP", "BUHBYE", "BTW", "OBTW", "TLDR", "I HAS A", "ITZ", "R",
                "SUM OF", "DIFF OF", "PRODUKT OF", "QUOSHUNT OF", "MOD OF", "BIGGR OF", "SMALLR OF",
                "BOTH OF", "EITHER OF", "WON OF", "NOT", "ANY OF", "ALL OF", "BOTH SAEM", "DIFFRINT",
                "SMOOSH", "MAEK", "A", "IS NOW A", "VISIBLE", "GIMMEH", "O RLY?", "YA RLY", "MEBBE",
                "NO WAI", "OIC", "WTF?", "OMG", "OMGWTF", "IM IN YR", "UPPIN", "NERFIN", "YR", "TIL",
                "WILE", "IM OUTTA YR", "HOW IZ I", "IF U SAY SO", "GTFO", "FOUND YR", "I IZ", "MKAY",]
    tokens = tokenize(lines)
    
    for token in tokens:
        if token in keywords:
            print(f"{token} is an reserved keyword")
        elif numbr_pattern.match(token) or numbar_pattern.match(token) or yarn_pattern.match(token) or troof_pattern.match(token) or type_pattern.match(token):
            print(f"{token} is a literal")
        elif identifier_pattern.match(token):
            print(f"{token} is an identifier")

def tokenize(lines):
    tokens = []
    for line in lines:
        line_tokens = line.split(" ")
        for tok in line_tokens:
            if tok != "":
                tokens.append(tok)
    return tokens
