class TokenClass:
    _counter = 0

    def __init__(self, type, value, is_reference):
        self.type = type
        self.value = value
        self.is_reference = is_reference 

        TokenClass._counter += 1
        self.id = TokenClass._counter

    def get_type_value(self):
        return (self.type, self.value)
