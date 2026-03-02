import unittest
from src.components.lexer import Lexer
from components.evaluator import Evaluator


lexer = Lexer()
parser = Evaluator()


class TestDeclarationAbstraction(unittest.TestCase):
    def test_valid_declaration(self):
        lexemes = lexer.process(
            """HAI
            I HAS A var
        KTHXBYE"""
        )

        parser.evaluate(lexemes)
        self.assertIsNone(parser.memory["var"])

    def test_valid_declaration_with_value(self):
        lexemes = lexer.process(
            """HAI
            I HAS A var ITZ 5
        KTHXBYE"""
        )

        parser.evaluate(lexemes)
        self.assertEqual(parser.memory["var"], 5)
