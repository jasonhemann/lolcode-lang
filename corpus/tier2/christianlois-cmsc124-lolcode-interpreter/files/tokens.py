# Author: Christian Olo
# Program Description: A LOLCode interpreter developed using python

# utility class for a valid token in lexer
class Token:
    def __init__(self, type_, value, line_num):
        self.type = type_
        self.value = value
        self.line_num = line_num