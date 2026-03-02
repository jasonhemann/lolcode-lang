import unittest
from src.components.lexer import Lexer
from components.evaluator import Evaluator


lexer = Lexer()
parser = Evaluator()


class TestProgramAbstraction(unittest.TestCase):
    def test_empty_program(self):
        lexemes = lexer.process(
            """HAI
        KTHXBYE"""
        )

        try:
            parser.evaluate(lexemes)
        except SyntaxError:
            self.fail("Unexpected syntax error")

    def test_valid_program(self):
        lexemes = lexer.process(
            """HAI
            VISIBLE 1
        KTHXBYE"""
        )

        try:
            parser.evaluate(lexemes)
        except SyntaxError:
            self.fail("Unexpected syntax error")

    def test_no_hai(self):
        lexemes = lexer.process("KTHXBYE")

        with self.assertRaises(SyntaxError):
            parser.evaluate(lexemes)

    def test_no_kthxbye(self):
        lexemes = lexer.process("HAI")

        with self.assertRaises(SyntaxError):
            parser.evaluate(lexemes)

    def test_no_newlines(self):
        lexemes = lexer.process("HAI KTHXBYE")

        with self.assertRaises(SyntaxError):
            parser.evaluate(lexemes)

        lexemes = lexer.process(
            """HAI VISIBLE 1
        KTHXBYE"""
        )

        with self.assertRaises(SyntaxError):
            parser.evaluate(lexemes)

    def test_extra_newlines(self):
        lexemes = lexer.process(
            """HAI


            VISIBLE 1
        KTHXBYE"""
        )

        try:
            parser.evaluate(lexemes)
        except SyntaxError:
            self.fail("Unexpected syntax error")


class TestStatementsAbstraction(unittest.TestCase):
    def test_valid_multiline_statements(self):
        lexemes = lexer.process(
            """HAI
            VISIBLE 1
            VISIBLE 2
            VISIBLE 3
        KTHXBYE"""
        )

        try:
            parser.evaluate(lexemes)
        except SyntaxError:
            self.fail("Unexpected syntax error")

    def test_no_newlines(self):
        lexemes = lexer.process(
            """HAI
            VISIBLE 1 KTHXBYE"""
        )

        with self.assertRaises(SyntaxError):
            parser.evaluate(lexemes)

    def test_extra_newlines(self):
        lexemes = lexer.process(
            """HAI
            VISIBLE 1


        KTHXBYE"""
        )

        try:
            parser.evaluate(lexemes)
        except SyntaxError:
            self.fail("Unexpected syntax error")


class TestOutputAbstraction(unittest.TestCase):
    def test_valid_multi_operand_output(self):
        lexemes = lexer.process(
            """HAI
            VISIBLE one 2 "three" 4.0 five 6 "7" 8.9 WIN
        KTHXBYE"""
        )

        try:
            parser.evaluate(lexemes)
        except SyntaxError:
            self.fail("Unexpected syntax error")


class TestLoopAbstraction(unittest.TestCase):
    def test_valid_loop(self):
        lexemes = lexer.process(
            """HAI
            IM IN YR asc UPPIN YR num2 WILE BOTH SAEM num2 AN SMALLR OF num2 AN num1
                VISIBLE num2
            IM OUTTA YR asc
        KTHXBYE"""
        )

        try:
            parser.evaluate(lexemes)
        except SyntaxError:
            self.fail("Unexpected syntax error")

    def test_no_name(self):
        lexemes = lexer.process(
            """HAI
            IM IN YR UPPIN YR num2 WILE BOTH SAEM num2 AN SMALLR OF num2 AN num1
                VISIBLE num2
            IM OUTTA YR asc
        KTHXBYE"""
        )

        with self.assertRaises(SyntaxError):
            parser.evaluate(lexemes)

    def test_no_increment_decrement(self):
        lexemes = lexer.process(
            """HAI
            IM IN YR asc YR num2 WILE BOTH SAEM num2 AN SMALLR OF num2 AN num1
                VISIBLE num2
            IM OUTTA YR asc
        KTHXBYE"""
        )

        with self.assertRaises(SyntaxError):
            parser.evaluate(lexemes)

    def test_no_yr(self):
        lexemes = lexer.process(
            """HAI
            IM IN YR asc UPPIN num2 WILE BOTH SAEM num2 AN SMALLR OF num2 AN num1
                VISIBLE num2
            IM OUTTA YR asc
        KTHXBYE"""
        )

        with self.assertRaises(SyntaxError):
            parser.evaluate(lexemes)

    def test_no_variable(self):
        lexemes = lexer.process(
            """HAI
            IM IN YR asc UPPIN YR WILE BOTH SAEM num2 AN SMALLR OF num2 AN num1
                VISIBLE num2
            IM OUTTA YR asc
        KTHXBYE"""
        )

        with self.assertRaises(SyntaxError):
            parser.evaluate(lexemes)

    def test_incomplete_condition(self):
        lexemes = lexer.process(
            """HAI
            IM IN YR asc UPPIN YR num2 BOTH SAEM num2 AN SMALLR OF num2 AN num1
                VISIBLE num2
            IM OUTTA YR asc
        KTHXBYE"""
        )

        with self.assertRaises(SyntaxError):
            parser.evaluate(lexemes)

        lexemes = lexer.process(
            """HAI
            IM IN YR asc UPPIN YR num2 WILE 
                VISIBLE num2
            IM OUTTA YR asc
        KTHXBYE"""
        )

        with self.assertRaises(SyntaxError):
            parser.evaluate(lexemes)

    def test_allow_no_statement(self):
        lexemes = lexer.process(
            """HAI
            IM IN YR asc UPPIN YR num2 WILE BOTH SAEM num2 AN SMALLR OF num2 AN num1
            IM OUTTA YR asc
        KTHXBYE"""
        )

        try:
            parser.evaluate(lexemes)
        except SyntaxError:
            self.fail("Unexpected syntax error")

    def test_no_closing(self):
        lexemes = lexer.process(
            """HAI
            IM IN YR asc UPPIN YR num2 WILE BOTH SAEM num2 AN SMALLR OF num2 AN num1
                VISIBLE num2
            asc
        KTHXBYE"""
        )

        with self.assertRaises(SyntaxError):
            parser.evaluate(lexemes)

    def test_no_closing_name(self):
        lexemes = lexer.process(
            """HAI
            IM IN YR asc UPPIN YR num2 WILE BOTH SAEM num2 AN SMALLR OF num2 AN num1
                VISIBLE num2
            IM OUTTA YR
        KTHXBYE"""
        )

        with self.assertRaises(SyntaxError):
            parser.evaluate(lexemes)


class TestMultipleOperandAbstraction(unittest.TestCase):
    def test_valid_multiple_and(self):
        lexemes = lexer.process(
            """HAI
            ALL OF WIN AN WIN AN WIN AN WIN AN FAIL MKAY
        KTHXBYE"""
        )

        try:
            parser.evaluate(lexemes)
        except SyntaxError:
            self.fail("Unexpected syntax error")

    def test_multiple_and_missing_separator(self):
        lexemes = lexer.process(
            """HAI
            ALL OF WIN AN WIN WIN AN WIN AN FAIL MKAY
        KTHXBYE"""
        )

        with self.assertRaises(SyntaxError):
            parser.evaluate(lexemes)

    def test_multiple_and_missing_closing(self):
        lexemes = lexer.process(
            """HAI
            ALL OF WIN AN WIN AN WIN AN WIN AN FAIL 
        KTHXBYE"""
        )

        with self.assertRaises(SyntaxError):
            parser.evaluate(lexemes)
