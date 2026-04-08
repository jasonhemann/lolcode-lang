class Evaluator:
    def __init__(self):
        self.variables = {}

    def eval(self, node):
        if node.type == 'PROGRAM':
            for child in node.children:
                self.eval(child)

        elif node.type == 'VAR_DECL':
            var_name = node.value
            value = self.eval(node.children[0]) if node.children else None
            self.variables[var_name] = value

        elif node.type == 'ASSIGN':
            var_name = node.value
            value = self.eval(node.children[0])
            if var_name not in self.variables:
                raise NameError(f"Variable '{var_name}' not declared.")
            self.variables[var_name] = value

        elif node.type == 'VISIBLE':
            value = self.eval(node.children[0])
            print(value)

        elif node.type == 'GIMMEH':
            var_name = node.value
            user_input = input()
            self.variables[var_name] = user_input

        elif node.type == 'LITERAL':
            val = node.value
            if val.isdigit() or (val.startswith('-') and val[1:].isdigit()):
                return int(val)
            try:
                return float(val)
            except ValueError:
                if val.startswith('"') and val.endswith('"'):
                    return val[1:-1]
                return self.variables.get(val, val)

        else:
            raise Exception(f"Unknown AST node type: {node.type}")
