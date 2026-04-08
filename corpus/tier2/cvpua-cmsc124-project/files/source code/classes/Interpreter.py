import tkinter
from tkinter.filedialog import askopenfilename

from classes.Lexer import Lexer
from classes.Parser import Parser
from classes.Analyzer import Analyzer
from utils.tokexp import TOK_EXP


class Interpreter:
  def __init__(self):
    self.tokens = []
    self.text = ""
    self.tree = None
    self.symbol_table = {}
  
  def readFile(self):
    # To do: 
    # [ ] check if the file type is lol, if not, then print an error
    filename = askopenfilename()
    if filename:
      file = open(filename,'r')
      self.text = file.read()
      return filename
    else:
      return None

  def run_lexer(self):
    if (self.text != ""):
      lexer = Lexer(self.text, TOK_EXP)
    else:
      raise Exception("FAILED TO RUN THE LEXER: Empty file or set the file first")
    self.tokens = lexer.tokenize()
  
  def run_parser(self):
    print("Parsing...")
    if (len(self.tokens) != 0):
      parser = Parser(self.tokens)
    else:
      raise Exception("Parsing Error: The list of tokens is empty")
    self.tree = parser.parse()
    return True
  
  def run_analyzer(self, output_text):
    if (self.tree != None):
      analyzer = Analyzer(self.tree, output_text)
    else:
      print("The tree is still empty")
      return False
    
    codeblock = None
    lineNumber = 0
    for node in self.tree.children:
      if (node.type == "CODEBLOCK"):
        codeblock = node
        break
      elif (node.type == "MULTICOMMENT"):
        lineNumber = lineNumber + int(node.value)
      elif (node.type == "COMMENT"):
        lineNumber = lineNumber + 1
      else:
        lineNumber = lineNumber + 1
    analyzer.start_analyze(codeblock,lineNumber)
    self.symbol_table = analyzer.symbol_table
    return True
  
  # def interpret(self):
  #   is_successful = self.run_lexer()
  #   if (not(is_successful)):
  #     print("Tokenizing is not successful")
  #     return False

  #   is_successful = self.run_parser()
  #   if (not(is_successful)):
  #     print("Parsing is not successful")
  #     return False
    
  #   is_successful = self.run_analyzer()
  #   if (not(is_successful)):
  #     print("Semantic analysis is not successful")
  #     return False
  
  def print_text(self):
    print(self.text)
  
  def print_tokens(self):
    print("\n")
    print("==========TOKENS==========")
    for token in self.tokens:
      print('"' + token.name + '"' + "\n\t" + token.type )
    print("========END TOKENS========")
    print("\n")
  
  def print_tree(self,iteration = 0, node = None):
    if (iteration == 0):
      print("\n")
      print("==========TREE==========")
      children = self.tree.children
    else:
      children = node.children
    for child in children:
      value = "- " + child.value if child.value else ""
      print("    "*iteration + child.type  + value)
      if(child.children):
        self.print_tree(iteration + 1, child)
    if (iteration == 0):
      print("========END TREE========")
      print("\n")
    
  # def print_symbol_table(self):
