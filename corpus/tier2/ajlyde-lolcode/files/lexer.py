# lexer.py
class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)})"

class Lexer:
    KEYWORDS = {
        'HAI', 'KTHXBYE', 'I', 'HAS', 'A', 'ITZ', 'VISIBLE',
        'O', 'RLY?', 'YA', 'RLY', 'NO', 'WAI', 'OIC',
        'BOTH', 'SAEM', 'AN'
    }

    def __init__(self, source_code):
        self.lines = source_code.splitlines()
        self.tokens = []

    def tokenize(self):
        for line in self.lines:
            line = line.strip()
            if not line:
                continue
            # Remove commas but keep strings intact
            words = []
            current = ""
            in_string = False
            for ch in line:
                if ch == '"':
                    in_string = not in_string
                    current += ch
                elif ch == ',' and not in_string:
                    if current:
                        words.append(current)
                        current = ""
                elif ch.isspace() and not in_string:
                    if current:
                        words.append(current)
                        current = ""
                else:
                    current += ch
            if current:
                words.append(current)

            for word in words:
                if word in self.KEYWORDS:
                    self.tokens.append(Token(word))
                elif word.isdigit():
                    self.tokens.append(Token('NUMBER', int(word)))
                elif word.startswith('"') and word.endswith('"'):
                    self.tokens.append(Token('STRING', word[1:-1]))
                else:
                    self.tokens.append(Token('IDENTIFIER', word))
        return self.tokens
