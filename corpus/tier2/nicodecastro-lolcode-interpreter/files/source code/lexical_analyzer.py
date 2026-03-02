# LOLCODE Interpreter
# AUTHOR: John Nico T. De Castro
# CREATION DATE: 11/12/2024
# DESCRIPTION: An interpreter for the LOLCODE language. A project for CMSC 124.

'''
TODO Future
- Extra chars showing up as separate word, e.g. NUMBARR => NUMBAR and R
'''

import re

LITERAL_VAR_IDENTIFIER_PATTERN = [
    # ("YARN Literal", '\"[^"]+\"'),        # Added as separate check
    ("NUMBAR Literal",r"^-?[0-9]+\.[0-9]+"),
    ("NUMBR Literal", "^-?[0-9]+"),
    ("TROOF Literal", "(WIN|FAIL)"),
    ("TYPE Literal", "(NOOB|NUMBR|NUMBAR|YARN|TROOF)"),
    ("Identifier", "^[a-zA-Z][a-zA-Z0-9_]*")
]

KEYWORDS_PATTERN = [
    ("HAI","^HAI"),
    ("KTHXBYE","^KTHXBYE"),
    ("WAZZUP","^WAZZUP"),
    ("BUHBYE","^BUHBYE"),
    ("I HAS A","^I HAS A"),
    ("ITZ","ITZ "),
    ("R","R "),
    ("VISIBLE","^VISIBLE"),
    ("FOUND YR","^FOUND YR"),
    ("SUM OF","SUM OF"),
    ("DIFF OF","DIFF OF"),
    ("PRODUKT OF","PRODUKT OF"),
    ("QUOSHUNT OF","QUOSHUNT OF"),
    ("MOD OF","MOD OF"),
    ("BIGGR OF","BIGGR OF"),
    ("SMALLR OF","SMALLR OF"),
    ("BOTH OF","BOTH OF"),
    ("EITHER OF","EITHER OF"),
    ("WON OF","WON OF"),
    ("NOT","NOT"),
    ("ANY OF","ANY OF"),
    ("ALL OF","ALL OF"),
    ("BOTH SAEM","BOTH SAEM"),
    ("DIFFRINT","^DIFFRINT"),
    ("SMOOSH","^SMOOSH"),
    ("MAEK","^MAEK"),
    ("A","^A "),
    ("AN","^AN "),
    ("IS NOW A","IS NOW A"),
    ("GIMMEH","^GIMMEH"),
    ("O RLY?",r"^O RLY\?"),
    ("YA RLY","^YA RLY"),
    ("MEBBE","^MEBBE"),
    ("NO WAI","^NO WAI"),
    ("OIC","^OIC"),
    ("WTF?",r"^WTF\?"),
    ("OMGWTF","^OMGWTF"),
    ("OMG","^OMG"),
    ("IM IN YR","^IM IN YR"),
    ("UPPIN","UPPIN"),
    ("NERFIN","NERFIN"),
    ("YR","YR"),
    ("TIL","TIL"),
    ("WILE","WILE"),
    ("IM OUTTA YR","^IM OUTTA YR"),
    ("HOW IZ I","^HOW IZ I"),
    ("IF U SAY SO","^IF U SAY SO"),
    ("GTFO","^GTFO"),
    ("I IZ","^I IZ"),
    ("MKAY","MKAY")
    ]

LEXEME = 0
CLASSIFICATION = 1

def lexical_analysis(lexeme_table_values: list, lolcode_source: str) -> None:
    print("\n==================== PERFORMING LEXICAL ANALYSIS ====================\n")
    lolcode_lines = lolcode_source.split("\n")
    is_OBTW = [False]
    tokens = []

    for i, line in enumerate(lolcode_lines):
        print(f"Line {i}: {line}")
        line = line.strip()
        if line:
            tokens.extend(tokenize_classify(line, is_OBTW))

            if not is_OBTW[0]:
                for token in tokens:
                    lexeme_table_values.append(token)
                print(f"Tokens: {tokens}\n")
                tokens = []
            if is_OBTW[0] and i == len(lolcode_lines)-1:
                lexeme_table_values.append([None, "No closing TLDR"])
    print("==================== COMPLETED LEXICAL ANALYSIS ====================")
    return

def tokenize_classify(line: str, is_OBTW: list) -> list:
    tokens = []

    # prev line/s are part of OBTW and TLDR not yet found
    if is_OBTW[0]:
        tldr_match = re.search("^TLDR(.*)", line)
        if tldr_match:
            tokens.append(("TLDR", "Keyword"))
            invalid = tldr_match.group(1).strip()
            if invalid:
                tokens.append((invalid, "Invalid statements after TLDR"))
            is_OBTW[0] = False      # next lines are not part of OBTW anymore since TLDR was found
        else:
            tokens.append((line, "Comment"))
        tokens.append(("<linebreak>", "Linebreak"))
        return tokens

    # standalone comments
    btw_match = re.search("^BTW(.*)", line)
    obtw_match = re.search("^OBTW(.*)", line)
    if btw_match:
        tokens.append(("BTW", "Keyword"))
        comment = btw_match.group(1).strip()
        if comment:
            tokens.append((comment, "Comment"))
        tokens.append(("<linebreak>", "Linebreak"))
        return tokens
    elif obtw_match:
        tokens.append(("OBTW", "Keyword"))
        comment = obtw_match.group(1).strip()
        if comment:
            tokens.append((comment, "Comment"))
        is_OBTW[0] = True
        tokens.append(("<linebreak>", "Linebreak"))
        return tokens

    # check for in-line comments, remove them, we will append them later as the last step
    inline_btw_match = re.search(r"\s+BTW(.*)", line)
    inline_btw_tokens = []
    if inline_btw_match:
        inline_btw_tokens.append(("BTW", "Keyword"))
        comment = inline_btw_match.group(1).strip()
        inline_btw_tokens.append((comment, "Comment"))
        line = re.sub(r"\s+BTW(.*)", " ", line)

    # test for keywords
    while True:
        found_tokens = []

        found_keyword_token = True      # set initial true
        while found_keyword_token:          # if a keyword found previously, repeat searching
            for keyword, pattern in KEYWORDS_PATTERN:
                keyword_token_match = re.match(pattern, line)
                if keyword_token_match:
                    found_keyword_token = True
                    found_tokens.append((keyword, "Keyword"))
                    line = re.sub(pattern, "", line, count=1).strip()       # remove found keyword
                    break
                else:           # no more keywords found, try yarn then literal
                    found_keyword_token = False

        # try concatenation separator
        separator_match = re.match(r'\+ ', line)
        if separator_match:
            found_tokens.append((line[separator_match.start():separator_match.end()], "Concatenation Separator"))
            line = re.sub(r'\+ ', " ", line, count=1).strip()
            tokens.extend(found_tokens)
            continue       # start searching for keyword again

        # try for yarn literal
        yarn_token_match = re.match('(\"[^"]+\")', line)
        if yarn_token_match:
            found_tokens.append((yarn_token_match.group(1), "YARN Literal"))
            line = re.sub('\"[^"]+\"', " ", line, count=1).strip()
            tokens.extend(found_tokens)
            continue    # start searching for keyword again

        # try for other literals
        for literal, pattern in LITERAL_VAR_IDENTIFIER_PATTERN:
            literal_match = re.match(pattern, line)
            if literal_match:
                found_tokens.append((line[literal_match.start():literal_match.end()], literal))
                line = re.sub(pattern, "", line, count=1).strip()
                break       # start searching for keyword again

        tokens.extend(found_tokens)
        if not found_tokens:
            break
      
    if inline_btw_tokens:
        tokens.extend(inline_btw_tokens)

    tokens.append(("<linebreak>", "Linebreak"))

    if line.strip():
        tokens.append((f"{line}", "Invalid Token"))

    return tokens