# Author: Christian Olo
# Program Description: A LOLCode interpreter developed using python

# a utilitily class for storing symbols from semantic analyzer(SemanticAnalyzer)
class Symbol:
    def __init__(self, type, value = None):
        self.type = type
        self.value = value