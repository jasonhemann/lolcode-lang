class SymbolTable:
    def __init__(self):
        self.symbols = []

    def add_symbol(self, name, value):
        if self.lookup(name):
            # var is alr declared
            return False
        self.symbols.append({"name":name, "type":value})
        return True
    
    def lookup(self, name):
        # check if alr in the symbol list
        for symbol in self.symbols:
            if symbol["name"] == name:
                return symbol
        return None
    
# var's are declared before use

# arithmetic operands compatible

# number of function args