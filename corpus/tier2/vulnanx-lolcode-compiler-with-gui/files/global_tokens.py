from error import Error

class GlobalTokens:
    def __init__(self, line_num, tokens, operation):
        self.line_num = line_num
        self.tokens = tokens
        self.operation = operation
        self.pos = 0

    def get_tok_at_pos(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos] 
        else:
            None

    def consume(self, expected=None):
        tok = self.get_tok_at_pos()
        if tok is None:
            return Error(self.line_num)._operand_count_mismatch(self.operation)
        if expected and tok.get_type_value() != expected.get_type_value():
            return Error(self.line_num)._word_mismatch(expected, tok)
        self.pos += 1
        return tok

    def done(self):
        return self.pos >= len(self.tokens)