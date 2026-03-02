"""
LOLCODE Interpreter Module
Executes the semantically analyzed AST
"""

class Interpreter:
    def __init__(self, ast):
        self.ast = ast
        self.variables = {}
        self.it_value = None

    def interpret(self):
        if not self.ast or self.ast.type != 'PROGRAM':
            raise ValueError("Invalid AST: Root node must be a PROGRAM")

        self.initialize_variables()

        for statement in self.ast.children:
            self.execute_statement(statement)

    def initialize_variables(self):
        self.variables = {
            'IT': None
        }

    def execute_statement(self, node):
        if not node:
            return

        if node.type == 'VAR_DECLARATION':
            self.execute_variable_declaration(node)
        elif node.type == 'VAR_ASSIGNMENT':
            self.execute_variable_assignment(node)
        elif node.type == 'OUTPUT':
            self.execute_output(node)
        elif node.type == 'INPUT':
            self.execute_input(node)
        elif node.type == 'CONDITIONAL':
            self.execute_conditional(node)

    def execute_variable_declaration(self, node):
        var_name = node.value
        self.variables[var_name] = None

        if node.children:
            value = self.evaluate_expression(node.children[0])
            self.variables[var_name] = value

    def execute_variable_assignment(self, node):
        var_name = node.value
        if var_name not in self.variables:
            raise NameError(f"Variable '{var_name}' not declared")

        value = self.evaluate_expression(node.children[0])
        self.variables[var_name] = value
        self.variables['IT'] = value

    def execute_output(self, node):
        value = self.evaluate_expression(node.children[0])
        print(self.to_string(value))

    def execute_input(self, node):
        var_name = node.value
        if var_name not in self.variables:
            raise NameError(f"Variable '{var_name}' not declared")

        user_input = input()

        try:
            self.variables[var_name] = int(user_input)
        except ValueError:
            try:
                self.variables[var_name] = float(user_input)
            except ValueError:
                self.variables[var_name] = user_input

        self.variables['IT'] = self.variables[var_name]

    def execute_conditional(self, node):
        condition = self.variables['IT']
        condition_result = self.is_truthy(condition)

        for branch in node.children:
            if branch.type == 'TRUE_BRANCH' and condition_result:
                for statement in branch.children:
                    self.execute_statement(statement)
                break
            elif branch.type == 'FALSE_BRANCH' and not condition_result:
                for statement in branch.children:
                    self.execute_statement(statement)
                break

    def evaluate_expression(self, node):
        if not node:
            return None

        if node.type == 'LITERAL':
            return node.value

        elif node.type == 'VARIABLE':
            var_name = node.value
            if var_name not in self.variables:
                raise NameError(f"Variable '{var_name}' not declared")
            return self.variables[var_name]

        elif node.type == 'OP_ADD':
            left = self.evaluate_expression(node.children[0])
            right = self.evaluate_expression(node.children[1])
            try:
                result = float(left) + float(right)
                if result.is_integer():
                    result = int(result)
                self.variables['IT'] = result
                return result
            except (ValueError, TypeError):
                result = str(left) + str(right)
                self.variables['IT'] = result
                return result

        elif node.type == 'OP_SUB':
            left = self.evaluate_expression(node.children[0])
            right = self.evaluate_expression(node.children[1])
            try:
                result = float(left) - float(right)
                if result.is_integer():
                    result = int(result)
                self.variables['IT'] = result
                return result
            except (ValueError, TypeError):
                raise TypeError("Cannot subtract non-numeric values")

        elif node.type == 'OP_MUL':
            left = self.evaluate_expression(node.children[0])
            right = self.evaluate_expression(node.children[1])
            try:
                result = float(left) * float(right)
                if result.is_integer():
                    result = int(result)
                self.variables['IT'] = result
                return result
            except (ValueError, TypeError):
                raise TypeError("Cannot multiply non-numeric values")

        elif node.type == 'OP_DIV':
            left = self.evaluate_expression(node.children[0])
            right = self.evaluate_expression(node.children[1])
            try:
                if float(right) == 0:
                    raise ZeroDivisionError("Division by zero")
                result = float(left) / float(right)
                if result.is_integer():
                    result = int(result)
                self.variables['IT'] = result
                return result
            except (ValueError, TypeError):
                raise TypeError("Cannot divide non-numeric values")

        elif node.type == 'OP_MOD':
            left = self.evaluate_expression(node.children[0])
            right = self.evaluate_expression(node.children[1])
            try:
                left_val = int(float(left))
                right_val = int(float(right))
                if right_val == 0:
                    raise ZeroDivisionError("Modulo by zero")
                result = left_val % right_val
                self.variables['IT'] = result
                return result
            except (ValueError, TypeError):
                raise TypeError("Cannot perform modulo on non-numeric values")

        elif node.type == 'OP_MAX':
            left = self.evaluate_expression(node.children[0])
            right = self.evaluate_expression(node.children[1])
            try:
                left_val = float(left)
                right_val = float(right)
                result = max(left_val, right_val)
                if result.is_integer():
                    result = int(result)
                self.variables['IT'] = result
                return result
            except (ValueError, TypeError):
                raise TypeError("Cannot compare non-numeric values")

        elif node.type == 'OP_MIN':
            left = self.evaluate_expression(node.children[0])
            right = self.evaluate_expression(node.children[1])
            try:
                left_val = float(left)
                right_val = float(right)
                result = min(left_val, right_val)
                if result.is_integer():
                    result = int(result)
                self.variables['IT'] = result
                return result
            except (ValueError, TypeError):
                raise TypeError("Cannot compare non-numeric values")

        elif node.type == 'OP_EQUAL':
            left = self.evaluate_expression(node.children[0])
            right = self.evaluate_expression(node.children[1])
            result = left == right
            self.variables['IT'] = result
            return result

        elif node.type == 'OP_NOT_EQUAL':
            left = self.evaluate_expression(node.children[0])
            right = self.evaluate_expression(node.children[1])
            result = left != right
            self.variables['IT'] = result
            return result

        elif node.type == 'OP_AND':
            left = self.evaluate_expression(node.children[0])
            right = self.evaluate_expression(node.children[1])
            result = self.is_truthy(left) and self.is_truthy(right)
            self.variables['IT'] = result
            return result

        elif node.type == 'OP_OR':
            left = self.evaluate_expression(node.children[0])
            right = self.evaluate_expression(node.children[1])
            result = self.is_truthy(left) or self.is_truthy(right)
            self.variables['IT'] = result
            return result

        elif node.type == 'OP_XOR':
            left = self.evaluate_expression(node.children[0])
            right = self.evaluate_expression(node.children[1])
            result = self.is_truthy(left) != self.is_truthy(right)
            self.variables['IT'] = result
            return result

        elif node.type == 'OP_NOT':
            operand = self.evaluate_expression(node.children[0])
            result = not self.is_truthy(operand)
            self.variables['IT'] = result
            return result

        elif node.type == 'OP_SMOOSH':
            parts = [self.evaluate_expression(child) for child in node.children]
            result = ''.join(map(self.to_string, parts))
            self.variables['IT'] = result
            return result

        return None

    def is_truthy(self, value):
        if value is None:
            return False
        if isinstance(value, bool):
            return value
        if isinstance(value, (int, float)):
            return value != 0
        if isinstance(value, str):
            if value.strip() == '' or value.upper() == 'FAIL':
                return False
            try:
                if float(value) == 0:
                    return False
            except ValueError:
                pass
            return True
        return True

    def to_string(self, value):
        if value is None:
            return "NOOB"
        if isinstance(value, bool):
            return "WIN" if value else "FAIL"
        return str(value)
