# test/test_interpreter_unittest.py

import unittest
import subprocess
import sys
import os

class TestLOLCODE(unittest.TestCase):

    def run_lol(self, filename):
        result = subprocess.run(
            [sys.executable, "main.py", filename],
            capture_output=True,
            text=True
        )
        return result.stdout.strip()

    def test_hello_world(self):
        output = self.run_lol("test/hello_world.lol")
        self.assertIn("HAI WORLD!", output)

    def test_conditional(self):
        # Simulate input "5" for testing
        result = subprocess.run(
            [sys.executable, "main.py", "test/conditional.lol"],
            input="5\n",
            capture_output=True,
            text=True
        )
        self.assertIn("UR NUMBR IZ LESS THAN 10!", result.stdout)
    
    def test_smoosh(self):
        output = self.run_lol("test/smoosh.lol")
        self.assertIn("HAI WORLD!", output)

    def test_nested_expr(self):
        output = self.run_lol("test/nested_expr.lol")
        self.assertIn("7", output)

if __name__ == '__main__':
    unittest.main()
