# Author: Christian Olo
# Program Description: A LOLCode interpreter developed using python

# a utility class for valid symbols in syntax analyzer
class ATNode:
    def __init__(self, type, value = None, children_nodes = None):
        self.type = type
        self.value = value
        self.children_nodes = children_nodes     