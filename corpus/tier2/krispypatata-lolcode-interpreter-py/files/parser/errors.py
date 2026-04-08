from lexer.lolcode_lexer import *

# ═════════════════════════════════════════════════════════════════════════════════════════════════
class Error:
  def __init__(self, token, details, error_name):
    self.token = token
    self.details = details
    self.error_name = error_name
  def as_string(self):
    return f"{self.error_name}: '{self.token[TOKEN_VALUE]}' at line {self.token[TOKEN_LINE_NUMBER]}\nDetails: {self.details}\n"

class InvalidSyntaxError(Error):
  def __init__(self, token, details):
    super().__init__(token, details, error_name='Invalid Syntax')

class RuntimeError(Error):
  def __init__(self, token, details):
    super().__init__(token, details, error_name='Runtime Error')
    