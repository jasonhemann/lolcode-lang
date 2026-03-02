"""
LOLCODE Parser Module
Converts token stream into an Abstract Syntax Tree (AST)
"""

class ASTNode:
    def __init__(self, node_type, children=None, value=None):
        self.type = node_type
        self.children = children if children is not None else []
        self.value = value

    def __repr__(self):
        value_str = f", value={self.value}" if self.value is not None else ""
        children_str = f", children={len(self.children)}" if self.children else ""
        return f"ASTNode({self.type}{value_str}{children_str})"


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        program_node = ASTNode('PROGRAM')

        if not self.tokens or self.tokens[0].type != 'PROGRAM_START':
            raise SyntaxError("Program must start with 'HAI'")

        self.consume('PROGRAM_START')

        while self.current < len(self.tokens) and self.tokens[self.current].type != 'PROGRAM_END':
            if self.tokens[self.current].type in ['COMMENT_LINE', 'COMMENT_BLOCK_START', 'COMMENT_BLOCK_END']:
                self.current += 1
                continue

            statement = self.parse_statement()
            if statement:
                program_node.children.append(statement)

        if self.current >= len(self.tokens) or self.tokens[self.current].type != 'PROGRAM_END':
            raise SyntaxError("Program must end with 'KTHXBYE'")

        self.consume('PROGRAM_END')
        return program_node

    def parse_statement(self):
        if self.current >= len(self.tokens):
            return None

        token = self.tokens[self.current]

        if token.type == 'VAR_DECLARATION':
            return self.parse_variable_declaration()

        elif token.type == 'IDENTIFIER' and self.peek() and self.peek().type == 'ASSIGNMENT_OP':
            return self.parse_variable_assignment()

        elif token.type == 'OUTPUT':
            return self.parse_output()

        elif token.type == 'INPUT':
            return self.parse_input()

        elif token.type == 'IF_START':
            return self.parse_conditional()

        elif token.type in [
            'OP_ADD', 'OP_SUB', 'OP_MUL', 'OP_DIV', 'OP_MOD', 'OP_MAX', 'OP_MIN',
            'OP_EQUAL', 'OP_NOT_EQUAL', 'OP_AND', 'OP_OR', 'OP_XOR', 'OP_NOT',
            'OP_SMOOSH'
        ]:
            expr = self.parse_expression()
            return ASTNode('VAR_ASSIGNMENT', [expr], 'IT')

        self.current += 1
        return None

    def parse_variable_declaration(self):
        self.consume('VAR_DECLARATION')

        if self.current >= len(self.tokens) or self.tokens[self.current].type != 'IDENTIFIER':
            raise self.syntax_error("Expected variable name after 'I HAS A'")

        var_name = self.tokens[self.current].value
        self.current += 1

        if self.current < len(self.tokens) and self.tokens[self.current].type == 'VAR_ASSIGNMENT':
            self.consume('VAR_ASSIGNMENT')
            value_expr = self.parse_expression()
            return ASTNode('VAR_DECLARATION', [value_expr], var_name)

        return ASTNode('VAR_DECLARATION', [], var_name)

    def parse_variable_assignment(self):
        var_name = self.tokens[self.current].value
        self.current += 1

        self.consume('ASSIGNMENT_OP')
        value_expr = self.parse_expression()
        return ASTNode('VAR_ASSIGNMENT', [value_expr], var_name)

    def parse_output(self):
        self.consume('OUTPUT')
        expr = self.parse_expression()
        return ASTNode('OUTPUT', [expr])

    def parse_input(self):
        self.consume('INPUT')

        if self.current >= len(self.tokens) or self.tokens[self.current].type != 'IDENTIFIER':
            raise self.syntax_error("Expected variable name after 'GIMMEH'")

        var_name = self.tokens[self.current].value
        self.current += 1
        return ASTNode('INPUT', [], var_name)

    def parse_conditional(self):
        self.consume('IF_START')
        cond_node = ASTNode('CONDITIONAL')

        if self.current >= len(self.tokens) or self.tokens[self.current].type != 'IF_TRUE':
            raise self.syntax_error("Expected 'YA RLY' after 'O RLY?'")

        self.consume('IF_TRUE')
        true_branch = ASTNode('TRUE_BRANCH')

        while self.current < len(self.tokens) and self.tokens[self.current].type not in ['IF_FALSE', 'IF_END']:
            statement = self.parse_statement()
            if statement:
                true_branch.children.append(statement)

        cond_node.children.append(true_branch)

        if self.current < len(self.tokens) and self.tokens[self.current].type == 'IF_FALSE':
            self.consume('IF_FALSE')
            false_branch = ASTNode('FALSE_BRANCH')

            while self.current < len(self.tokens) and self.tokens[self.current].type != 'IF_END':
                statement = self.parse_statement()
                if statement:
                    false_branch.children.append(statement)

            cond_node.children.append(false_branch)

        if self.current >= len(self.tokens) or self.tokens[self.current].type != 'IF_END':
            raise self.syntax_error("Expected 'OIC' to end conditional")

        self.consume('IF_END')
        return cond_node

    def parse_expression(self):
        if self.current >= len(self.tokens):
            raise self.syntax_error("Unexpected end of input while parsing expression")

        token = self.tokens[self.current]

        if token.type in ['INT_LITERAL', 'FLOAT_LITERAL', 'STRING_LITERAL', 'BOOL_LITERAL']:
            self.current += 1
            return ASTNode('LITERAL', [], token.value)

        elif token.type == 'IDENTIFIER':
            var_name = token.value
            self.current += 1
            return ASTNode('VARIABLE', [], var_name)

        elif token.type in [
            'OP_ADD', 'OP_SUB', 'OP_MUL', 'OP_DIV', 'OP_MOD', 'OP_MAX', 'OP_MIN',
            'OP_EQUAL', 'OP_NOT_EQUAL', 'OP_AND', 'OP_OR', 'OP_XOR']:
            op_type = token.type
            self.current += 1
            left = self.parse_expression()
            self.consume('CONNECTOR')
            right = self.parse_expression()
            return ASTNode(op_type, [left, right])

        elif token.type == 'OP_NOT':
            self.current += 1
            operand = self.parse_expression()
            return ASTNode('OP_NOT', [operand])

        elif token.type == 'OP_SMOOSH':
            self.current += 1
            args = [self.parse_expression()]
            while self.current < len(self.tokens) and self.tokens[self.current].type == 'CONNECTOR':
                self.consume('CONNECTOR')
                args.append(self.parse_expression())
            return ASTNode('OP_SMOOSH', args)

        raise self.syntax_error(f"Unexpected token in expression: {token.type}")

    def consume(self, expected_type):
        if self.current >= len(self.tokens):
            raise self.syntax_error(f"Unexpected end of input, expected {expected_type}")

        if self.tokens[self.current].type != expected_type:
            raise self.syntax_error(f"Expected {expected_type}, got {self.tokens[self.current].type}")

        self.current += 1

    def peek(self):
        if self.current + 1 >= len(self.tokens):
            return None
        return self.tokens[self.current + 1]

    def syntax_error(self, message):
        token = self.tokens[self.current] if self.current < len(self.tokens) else None
        if token:
            return SyntaxError(f"Syntax Error (line {token.line}): {message}")
        return SyntaxError(message)
