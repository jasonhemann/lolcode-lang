import re
from token_class import TokenClass

class Lexer:
    regexes = {
        "NUMBAR": r"-?[0-9]+\.[0-9]+",
        "NUMBR": r"-?[0-9]+",
        "YARN": r'"[^"]*"',
        "TROOF": r"(WIN|FAIL)",
        "type": r"(NOOB|NUMBR|NUMBAR|YARN|TROOF)",
        "program delimiter": r"(HAI|KTHXBYE)",
        "variable declaration": r"(WAZZUP|I HAS A|ITZ)",
        "function declaration": r"HOW IZ I",
        "function call": r"I IZ",
        "if-then statement": r"(O RLY\?|YA RLY|MEBBE|NO WAI)",
        "switch-case statement": r"(WTF\?|OMG|OMGWTF)",
        "loop statement": r"(IM IN YR|UPPIN|NERFIN|TIL|WILE)",
        "closing statement": r"(IM OUTTA YR|OIC|MKAY|IF U SAY SO|BUHBYE)",
        "arithmetic operation": r"(SUM OF|DIFF OF|PRODUKT OF|QUOSHUNT OF|MOD OF|BIGGR OF|SMALLR OF|SMOOSH)",
        "logical operation": r"(BOTH OF|EITHER OF|WON OF|ALL OF|ANY OF|NOT|BOTH SAEM|DIFFRINT)",
        "output statement": r"VISIBLE",
        "input statement": r"GIMMEH",
        "return statement": r"(FOUND YR|GTFO)",
        "typecasting statement": r"(MAEK|A|IS NOW A)",
        "reassignment statement": r"R",
        "variable reference": r"YR",
        "conjunction": r"AN",
        "conjunction": r"AN",
        "comment": r"BTW|OBTW|TLDR",
        "variable": r"[A-Za-z][A-Za-z0-9_]*",
        "output concat": r"\+"
    }

    multiword_keywords = [
        "PRODUKT OF", "QUOSHUNT OF", "SMALLR OF", "BIGGR OF", "EITHER OF",
        "SUM OF", "DIFF OF", "MOD OF", "BOTH OF", "WON OF", "ALL OF", "ANY OF",
        "I HAS A", "IS NOW A", "O RLY?", "YA RLY", "NO WAI", "IM IN YR",
        "IM OUTTA YR", "BOTH SAEM", "I IZ", "FOUND YR", "HOW IZ I", "IF U SAY SO"
    ]

    def __init__(self, program):
        # self.program = program.splitlines()     # expecting program to be a string containing the actual program
        self.program = program.readlines()      # for testing purposes, where program is a file (not applicable in GUI)
        self.line_counter = 0
        self.tokens = self._init_tokens()

    # ===========================================================
    #   Tokenization function
    # ===========================================================

    def tokenize(self):
        words_in_line = []
        skip_line = False
        skip_multiline = False

        for line in self.program:
            line = line.strip()
            self.line_counter += 1

            # ===========================================================
            #   Step 1. Split line, keep multiword keywords together.
            # ===========================================================

            # turns multiword keywords into one "word" so that it remains unaffected by split
            for keyword in self.multiword_keywords:
                if "?" in keyword:
                    pattern = re.escape(keyword)
                else:
                    pattern = r'\b' + re.escape(keyword) + r'\b'
                line = re.sub(pattern, keyword.replace(" ", "\uFFF0"), line)
                line = re.sub(pattern, keyword.replace(" ", "\uFFF0"), line)

            # finds all yarns and replaces their spaces to _ so that it remains unaffected by split
            yarn_matches = re.findall(r'"[^"]*"', line)
            for match in yarn_matches:
                line = line.replace(match, match.replace(" ", "\uFFF0"))
                line = line.replace(match, match.replace(" ", "\uFFF0"))

            words_in_line = line.split()

            # switches multiword keywords' underscores to spaces
            for index in range(len(words_in_line)):
                words_in_line[index] = re.sub(r'\uFFF0', " ", words_in_line[index])
                words_in_line[index] = re.sub(r'\uFFF0', " ", words_in_line[index])

            # skip line if it only contains a space or a new line
            if words_in_line == []:
                continue

            # skip line if within OBTW - TLDR block
            if skip_multiline:
                if "TLDR" in words_in_line:
                    skip_multiline = False
                else:
                    continue

            # ===========================================================
            #   Step 2. Assign type per word based on matching regex.
            # ===========================================================

            prev_word = ""
            for word in words_in_line:
                matched = False

                if skip_line:
                    skip_line = False
                    break

                for type, regex in self.regexes.items():
                    if re.fullmatch(regex, word):
                        if type == "comment":   # handles cases for comments, only gets BTW/OBTW/TLDR
                            if word == "BTW":
                                skip_line = True
                            elif word == "OBTW":
                                skip_multiline = True
                        if type == "variable":  # identify if loop label, function label, or variable only
                            if prev_word in ("IM IN YR", "IM OUTTA YR"):
                                type = "loop label"
                            elif prev_word in ("HOW IZ I", "I IZ"):
                                type = "function label"
                            elif prev_word == "YR" and ("HOW IZ I" in words_in_line):
                                type = "parameter"

                        self._store_token(type, word)
                        matched = True
                        break

                if not matched:
                    self._store_token("unknown", word)

                prev_word = word

        # ===========================================================
        #   Step 3. Return the dictionary of tokens.
        # ===========================================================

        return self.tokens

    # ===========================================================
    #   Helper functions for repetitive/tedious tasks.
    # ===========================================================
    
    def _init_tokens(self):
        tokens = {}
        for line_count in range(len(self.program)):
            tokens[line_count + 1] = []
        return tokens

    def _is_existing(self, type, value):
        for tokens in self.tokens.values():
            for token in tokens:
                if token.type == type and token.value == value:
                    return token
        return False
    
    def _store_token(self, type, word):
        is_reference = self._is_existing(type, word)
        token = TokenClass(type, word, is_reference)
        self.tokens[self.line_counter].append(token)
        # print(f"Successfully appended token {word} with type {type}!")

    def _print_tokens(self):
        print("\n================ TOKENS RECORDED ================")
        for tokens in self.tokens.values():
            for token in tokens:
                print(f"{token.value:<20} -> {token.type}")

        print("\n================ TOKENS PER LINE ================")
        for key, value in self.tokens.items():
            print(f"{key:<5} -> ", end="")
            for token in value:
                print(f"{token.value} ({token.type}) | ", end="")
            print()





# ===========================================================
#   MAIN : for testing purposes only.
#   DO NOT UNCOMMENT FOR FINAL OUTPUT
# ===========================================================

# file = open("test_cases/06_comparison.lol")
# lexer = Lexer(file)
# lexer.tokenize()
# lexer._print_tokens()
# file.close()