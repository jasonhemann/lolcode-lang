#!/usr/bin/env python3
import sys
import re

# ------------------------------
# Tokenization
# ------------------------------

class Token:
    def __init__(self, type_, value, line, col):
        self.type = type_
        self.value = value
        self.line = line
        self.col = col

    def __repr__(self):
        return f"Token({self.type}, {self.value}, line={self.line}, col={self.col})"

# Define multi-word and reserved tokens.
# Note: The regex patterns are anchored at the current substring start.
# They use case‐insensitive matching.
token_patterns = [
    ("I_HAS_A", r"I\s+HAS\s+A"),
    ("SUM_OF", r"SUM\s+OF"),
    ("DIFF_OF", r"DIFF\s+OF"),
    ("PRODUKT_OF", r"PRODUKT\s+OF"),
    ("QUOSHUNT_OF", r"QUOSHUNT\s+OF"),
    ("MOD_OF", r"MOD\s+OF"),
    ("BIGGR_OF", r"BIGGR\s+OF"),
    ("SMALLR_OF", r"SMALLR\s+OF"),
    ("BOTH_SAEM", r"BOTH\s+SAEM"),
    ("BOTH_OF", r"BOTH\s+OF"),
    ("EITHER_OF", r"EITHER\s+OF"),
    ("O_RLY", r"O\s+RLY\?"),
    ("YA_RLY", r"YA\s+RLY"),
    ("NO_WAI", r"NO\s+WAI"),
    ("OIC", r"OIC"),
    ("HAI", r"HAI"),
    ("KTHXBYE", r"KTHXBYE"),
    ("ITZ", r"ITZ"),
    ("VISIBLE", r"VISIBLE"),
    ("GIMMEH", r"GIMMEH"),
    ("DIFFRINT", r"DIFFRINT"),
    ("NOT", r"NOT"),
    ("AN", r"AN"),
    ("R", r"\bR\b")
]

class Lexer:
    def __init__(self, text):
        self.text = text

    def tokenize(self):
        tokens = []
        lines = self.text.splitlines()
        for lnum, line in enumerate(lines, start=1):
            line_tokens = self.tokenize_line(line, lnum)
            tokens.extend(line_tokens)
        return tokens

    def tokenize_line(self, line, lnum):
        tokens = []
        pos = 0
        line = line.strip()
        while pos < len(line):
            # Skip any whitespace
            if line[pos].isspace():
                pos += 1
                continue

            matched = False
            # Try multi-word/reserved tokens first.
            for token_type, pattern in token_patterns:
                regex = re.compile(pattern, re.IGNORECASE)
                m = regex.match(line, pos)
                if m:
                    value = m.group(0)
                    tokens.append(Token(token_type, value.upper(), lnum, pos + 1))
                    pos += len(value)
                    matched = True
                    break
            if matched:
                continue

            # If a string literal (YARN) is encountered.
            if line[pos] == '"':
                end_pos = pos + 1
                while end_pos < len(line) and line[end_pos] != '"':
                    end_pos += 1
                if end_pos < len(line) and line[end_pos] == '"':
                    value = line[pos + 1 : end_pos]
                    tokens.append(Token("YARN", value, lnum, pos + 1))
                    pos = end_pos + 1
                    continue
                else:
                    raise Exception(f"String literal not closed at line {lnum}, col {pos+1}")

            # Check for numbers: NUMBR (integer) or NUMBAR (float)
            num_match = re.match(r"-?\d+(\.\d+)?", line[pos:])
            if num_match:
                value = num_match.group(0)
                if '.' in value:
                    tokens.append(Token("NUMBAR", value, lnum, pos + 1))
                else:
                    tokens.append(Token("NUMBR", value, lnum, pos + 1))
                pos += len(value)
                continue

            # Check for identifiers: letters, digits, underscores.
            id_match = re.match(r"[A-Za-z][A-Za-z0-9_]*", line[pos:])
            if id_match:
                value = id_match.group(0)
                # Recognize TROOF literals (WIN/FAIL) in any case.
                if value.upper() in ["WIN", "FAIL"]:
                    tokens.append(Token("TROOF", value.upper(), lnum, pos + 1))
                else:
                    tokens.append(Token("IDENTIFIER", value, lnum, pos + 1))
                pos += len(value)
                continue

            # If nothing matches, signal an error.
            raise Exception(f"Unrecognized token at line {lnum}, col {pos+1}")
        return tokens

# ------------------------------
# Parsing (AST Construction)
# ------------------------------

# AST Node base class and various concrete AST nodes:

class ASTNode:
    pass

class ProgramNode(ASTNode):
    def __init__(self, statements):
        self.statements = statements

class DeclarationNode(ASTNode):
    def __init__(self, var_name, init_expr=None):
        self.var_name = var_name
        self.init_expr = init_expr

class AssignmentNode(ASTNode):
    def __init__(self, var_name, expr):
        self.var_name = var_name
        self.expr = expr

class VisibleNode(ASTNode):
    def __init__(self, expr):
        self.expr = expr

class GimmehNode(ASTNode):
    def __init__(self, var_name):
        self.var_name = var_name

class IfNode(ASTNode):
    def __init__(self, then_branch, else_branch=None):
        self.then_branch = then_branch
        self.else_branch = else_branch

class BinaryOpNode(ASTNode):
    def __init__(self, op, left, right):
        self.op = op  # e.g., SUM_OF, DIFF_OF, etc.
        self.left = left
        self.right = right

class UnaryOpNode(ASTNode):
    def __init__(self, op, operand):
        self.op = op  # e.g., NOT
        self.operand = operand

class LiteralNode(ASTNode):
    def __init__(self, value):
        self.value = value

class VariableNode(ASTNode):
    def __init__(self, name):
        self.name = name

# The Parser uses recursive descent to convert tokens into an AST.
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current_token(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def eat(self, token_type):
        token = self.current_token()
        if token is not None and token.type == token_type:
            self.pos += 1
            return token
        expected = token_type
        found = token.type if token else "EOF"
        raise Exception(f"Expected {expected} but found {found} at line {token.line if token else 'EOF'}.")

    def parse(self):
        # Require program to start with HAI and end with KTHXBYE.
        if self.current_token().type != "HAI":
            raise Exception("Program must begin with HAI")
        self.eat("HAI")
        statements = []
        while self.current_token() and self.current_token().type != "KTHXBYE":
            stmt = self.parse_statement()
            if stmt is not None:
                statements.append(stmt)
        if not self.current_token() or self.current_token().type != "KTHXBYE":
            raise Exception("Program must end with KTHXBYE")
        self.eat("KTHXBYE")
        return ProgramNode(statements)

    def parse_statement(self):
        token = self.current_token()
        if token is None:
            return None
        if token.type == "I_HAS_A":
            return self.parse_declaration()
        elif token.type == "VISIBLE":
            return self.parse_visible()
        elif token.type == "GIMMEH":
            return self.parse_gimmeh()
        elif token.type == "O_RLY":
            return self.parse_if()
        elif token.type == "IDENTIFIER":
            # Assume an assignment when starting with an identifier.
            return self.parse_assignment()
        else:
            # For any expression statement, we simply return the expression.
            return self.parse_expression()

    def parse_declaration(self):
        self.eat("I_HAS_A")  # "I HAS A"
        var_token = self.eat("IDENTIFIER")
        init_expr = None
        if self.current_token() and self.current_token().type == "ITZ":
            self.eat("ITZ")
            init_expr = self.parse_expression()
        return DeclarationNode(var_token.value, init_expr)

    def parse_assignment(self):
        var_token = self.eat("IDENTIFIER")
        self.eat("R")  # assignment operator
        expr = self.parse_expression()
        return AssignmentNode(var_token.value, expr)

    def parse_visible(self):
        self.eat("VISIBLE")
        expr = self.parse_expression()
        return VisibleNode(expr)

    def parse_gimmeh(self):
        self.eat("GIMMEH")
        var_token = self.eat("IDENTIFIER")
        return GimmehNode(var_token.value)

    def parse_if(self):
        # The condition (a TROOF value) is assumed to have been computed
        # immediately before the "O RLY?" statement and is stored in a special variable.
        self.eat("O_RLY")
        self.eat("YA_RLY")
        then_branch = []
        while self.current_token() and self.current_token().type not in ("NO_WAI", "OIC"):
            stmt = self.parse_statement()
            then_branch.append(stmt)
        else_branch = []
        if self.current_token() and self.current_token().type == "NO_WAI":
            self.eat("NO_WAI")
            while self.current_token() and self.current_token().type != "OIC":
                stmt = self.parse_statement()
                else_branch.append(stmt)
        self.eat("OIC")
        return IfNode(then_branch, else_branch if else_branch else None)

    def parse_expression(self):
        token = self.current_token()
        if token is None:
            raise Exception("Unexpected end of expression")
        if token.type in (
            "SUM_OF",
            "DIFF_OF",
            "PRODUKT_OF",
            "QUOSHUNT_OF",
            "MOD_OF",
            "BIGGR_OF",
            "SMALLR_OF",
            "BOTH_SAEM",
            "BOTH_OF",
            "EITHER_OF",
            "DIFFRINT"
        ):
            op = token.type
            self.eat(token.type)
            left = self.parse_expression()
            # Expect and consume AN between operands
            if self.current_token() and self.current_token().type == "AN":
                self.eat("AN")
            right = self.parse_expression()
            return BinaryOpNode(op, left, right)
        elif token.type == "NOT":
            self.eat("NOT")
            operand = self.parse_expression()
            return UnaryOpNode("NOT", operand)
        elif token.type in ("NUMBR", "NUMBAR"):
            self.eat(token.type)
            if token.type == "NUMBR":
                return LiteralNode(int(token.value))
            else:
                return LiteralNode(float(token.value))
        elif token.type == "YARN":
            self.eat("YARN")
            return LiteralNode(token.value)
        elif token.type == "TROOF":
            self.eat("TROOF")
            return LiteralNode(True if token.value == "WIN" else False)
        elif token.type == "IDENTIFIER":
            self.eat("IDENTIFIER")
            return VariableNode(token.value)
        else:
            raise Exception(f"Unexpected token {token.type} in expression at line {token.line}")

# ------------------------------
# Evaluation
# ------------------------------

# The evaluator runs the AST, maintaining an environment of variables. It also uses a special key "_it"
# to hold the result of the last evaluated expression (useful for conditionals).

def evaluate(node, env):
    if isinstance(node, ProgramNode):
        for stmt in node.statements:
            result = evaluate(stmt, env)
            if result is not None:
                env["_it"] = result
    elif isinstance(node, DeclarationNode):
        if node.var_name in env:
            raise Exception(f"Variable '{node.var_name}' already declared.")
        value = evaluate(node.init_expr, env) if node.init_expr is not None else None
        env[node.var_name] = value
    elif isinstance(node, AssignmentNode):
        if node.var_name not in env:
            raise Exception(f"Variable '{node.var_name}' not declared.")
        value = evaluate(node.expr, env)
        env[node.var_name] = value
        return value
    elif isinstance(node, VisibleNode):
        value = evaluate(node.expr, env)
        print(format_value(value))
        return value
    elif isinstance(node, GimmehNode):
        user_input = input("GIMMEH input: ")
        # Here, we treat the input as a YARN (string).
        env[node.var_name] = user_input
        return user_input
    elif isinstance(node, IfNode):
        # For conditionals, the condition is taken from the special _it value.
        condition = env.get("_it", False)
        if condition:
            for stmt in node.then_branch:
                result = evaluate(stmt, env)
                if result is not None:
                    env["_it"] = result
        elif node.else_branch is not None:
            for stmt in node.else_branch:
                result = evaluate(stmt, env)
                if result is not None:
                    env["_it"] = result
    elif isinstance(node, BinaryOpNode):
        left = evaluate(node.left, env)
        right = evaluate(node.right, env)
        if node.op == "SUM_OF":
            return left + right
        elif node.op == "DIFF_OF":
            return left - right
        elif node.op == "PRODUKT_OF":
            return left * right
        elif node.op == "QUOSHUNT_OF":
            if right == 0:
                raise Exception("Division by zero error.")
            return left / right
        elif node.op == "MOD_OF":
            return left % right
        elif node.op == "BIGGR_OF":
            return left if left > right else right
        elif node.op == "SMALLR_OF":
            return left if left < right else right
        elif node.op == "BOTH_SAEM":
            return True if left == right else False
        elif node.op == "DIFFRINT":
            return True if left != right else False
        elif node.op == "BOTH_OF":
            return True if (left and right) else False
        elif node.op == "EITHER_OF":
            return True if (left or right) else False
        else:
            raise Exception(f"Unknown binary operator '{node.op}'")
    elif isinstance(node, UnaryOpNode):
        operand = evaluate(node.operand, env)
        if node.op == "NOT":
            return not operand
        else:
            raise Exception(f"Unknown unary operator '{node.op}'")
    elif isinstance(node, LiteralNode):
        return node.value
    elif isinstance(node, VariableNode):
        if node.name in env:
            return env[node.name]
        else:
            raise Exception(f"Undefined variable '{node.name}'")
    else:
        raise Exception("Unknown AST node encountered.")

def format_value(val):
    # Convert boolean values back to LOLCODE TROOF representations.
    if isinstance(val, bool):
        return "WIN" if val else "FAIL"
    return str(val)

# ------------------------------
# Main entry point
# ------------------------------

def main():
    if len(sys.argv) < 2:
        print("Usage: python lolcode_interpreter.py <filename.lol>")
        sys.exit(1)
    filename = sys.argv[1]
    try:
        with open(filename, "r") as f:
            code = f.read()
    except Exception as err:
        print("Error reading file:", err)
        sys.exit(1)
    
    try:
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        # Uncomment the following line to see all tokens during debugging.
        # for tok in tokens:
        #     print(tok)
    except Exception as err:
        print("Lexing Error:", err)
        sys.exit(1)

    try:
        parser = Parser(tokens)
        ast = parser.parse()
    except Exception as err:
        print("Parsing Error:", err)
        sys.exit(1)

    # The environment holds declared variables and the special _it value.
    env = {}
    try:
        evaluate(ast, env)
    except Exception as err:
        print("Runtime Error:", err)
        sys.exit(1)

if __name__ == "__main__":
    main()
