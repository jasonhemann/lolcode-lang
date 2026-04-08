import collections
from . ast_nodes import PrimitiveType


class RedeclarationError(Exception): pass
class UndeclaredError(Exception): pass
class GTFO_Outside_of_Loop_Error(Exception): pass

class SymbolTable:
    def __init__(self):
        self.declared_variables = collections.ChainMap()
        self.var_count = 1
        self.label_count = 1
        self.gtfo_stack = []

    def declare_variable(self, name, declaration_type):
        if name in self.declared_variables.maps[0]:
            raise RedeclarationError(f'{name} has already been declared!')
        entry = self.get_entry(declaration_type)
        self.declared_variables[name] = entry
        return entry

    def get_entry_for_variable(self, name):
        if name not in self.declared_variables:
            raise UndeclaredError(f'{name} has not been declared!')
        return self.declared_variables[name]
    
    def get_entry(self, expr_type):
        address = self.var_count
        self.var_count += 1
        if isinstance(expr_type, PrimitiveType):
            result = MemoryEntry(expr_type=expr_type, address=address)
        else:
            result = MemoryEntry(expr_type=expr_type, address=address, address_type='a')
        return result

    def get_unique_label(self, root=''):
        unique_value = self.label_count
        self.label_count += 1
        return f'{root}_{unique_value}'
    
    def push_GTFO_stack(self, label):
        self.gtfo_stack.append(label)
    
    def read_GTFO_stack(self):
        if not self.gtfo_stack:
            raise GTFO_Outside_of_Loop_Error('Attempting to read empty GTFO stack')
        return self.gtfo_stack[-1]
    
    def pop_GTFO_stack(self):
        return self.gtfo_stack.pop() 

    def increment_scope(self):
        self.declared_variables.maps.insert(0, {})
    
    def decrement_scope(self):
        self.declared_variables.maps.pop(0)
    
    def get_array_index_entry(self, expr_type, array_entry, index_entry):
        result = self.get_entry(expr_type)
        result.array_entry = array_entry
        result.index_entry = index_entry
        return result

class MemoryEntry:
    """
    This class represents objects that have memory positions,
    they may have names.
    """
    def __init__(self, expr_type=None, address=None,
                 address_type="s", array_entry=None, index_entry=None):
        self.address = address
        self.address_type = address_type
        self.expr_type = expr_type
        self.array_entry = array_entry
        self.index_entry = index_entry

    def __repr__(self):
        return f'{self.address_type}{self.address}'