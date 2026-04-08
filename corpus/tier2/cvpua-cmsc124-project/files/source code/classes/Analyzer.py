from tkinter import *
from classes.Symbol import Symbol
from tkinter import simpledialog


lineNumber = 0

class Analyzer:
  def __init__(self, tree, output_text):
    self.tree = tree
    self.symbol_table = {"IT": Symbol("NOOB", None)}
    self.output_text = output_text
  
  def start_analyze(self,codeblock,line_number):
    global lineNumber 
    lineNumber = line_number
    self.analyze(codeblock)

  def analyze(self, codeblock):
    global lineNumber
    for child in codeblock.children:
      statement = child.children[0]
      # print(statement.type)
      if (statement.type == "PRINT"):
        self.print(statement)
      elif (statement.type == "DECLARATION"):
        self.declaration(statement)
      elif (statement.type == "ASSIGN"):
        self.assign(statement)
      elif (statement.type == "EXPR"):
        symbol = self.expr(statement)
        self.insert("IT", symbol)
      elif (statement.type == "CONTROL"):
        self.control(statement)
      elif (statement.type == "GTFO_KEYWORD"):
        return True
      elif (statement.type == "INPUT"):
        self.gimmeh(statement)
      elif (statement.type == "MULTICOMMENT"):
        lineNumber = lineNumber + int(statement.value)
        continue
      lineNumber = lineNumber + 1
  
  def gimmeh(self, statement): 
    variable = statement.children[1]
    identifier = variable.children[0]
    sample = simpledialog.askstring(title="INPUT", prompt="Enter input: ")
    self.insert(identifier.value, Symbol("YARN", sample))
  
  def control(self, statement):
    child = statement.children[0]
    global lineNumber
    if (child.type == "IFTHEN"):
      it = self.symbol_table["IT"]
      lineNumber = lineNumber + 1
      it_bool = True if it.value == "WIN" else False
      if_block_len = len(child.children[1].children[1].children)
      else_block_len = len(child.children[2].children[1].children)
      if (it_bool):
        if_block = child.children[1]
        codeblock = if_block.children[1]
      else:
        lineNumber = lineNumber + if_block_len
        else_block = child.children[2]
        codeblock = else_block.children[1]
      self.analyze(codeblock)
      if(it_bool):
        lineNumber = lineNumber + else_block_len

    elif (child.type == "SWITCH"):
      it = self.symbol_table["IT"]
      caseop = child.children[1]
      lineNumber = lineNumber + 1
      isGtfo = None
      done = False
      default = child.children[2]
      default_case_len = len(default.children[1].children)
      for case in caseop.children:
        symbol = self.get_value(case.children[1])
        codeblock = case.children[2]
        case_len = len(codeblock.children)
        if not done:
            if (isGtfo == False):
              lineNumber = lineNumber + 1
              isGtfo = self.analyze(codeblock)
              if(isGtfo):
                done = True
                continue
              else:
                isGtfo = False
            elif (symbol.value == it.value and isGtfo != False):
              lineNumber = lineNumber + 1
              isGtfo = self.analyze(codeblock)
              if (isGtfo):
                done = True
                continue
              else:
                isGtfo = False    
            else:
              lineNumber = lineNumber + 1
              lineNumber = lineNumber + case_len
              
        elif done:
          lineNumber = lineNumber + 1
          lineNumber = lineNumber + case_len

      if done:
        print(default_case_len)
        lineNumber = lineNumber + 2
        lineNumber = lineNumber + default_case_len
      
      else:
        default = child.children[2]
        lineNumber = lineNumber + 1
        codeblock = default.children[1]
        self.analyze(codeblock)
        lineNumber = lineNumber + 1
  
  def assign(self, statement):
    variable = statement.children[0]
    identifier = variable.children[0].value
    self.lookup(identifier)
    value_node = statement.children[2]
    symbol = self.get_value(value_node)
    self.insert(identifier, symbol)
  
  def declaration(self, statement):
    identifier = statement.children[1].value
    self.insert(identifier, Symbol("NOOB", None))
    if (len(statement.children) > 2):
      init_node = statement.children[2]
      value_node = init_node.children[1]
      symbol = self.get_value(value_node)
      self.insert(identifier, symbol)
  
  def print(self, statement):
    global s, e,l
    printop = statement.children[1]
    string = ""
    for value_node in printop.children:
      # literal or variable
      symbol = self.get_value(value_node)
      string += str(symbol.value)
    print(string)
    self.output_text.insert(END,string+'\n')          # print string
    self.output_text.insert(END,"lol-terminal:~$ ")   # print string
    self.output_text.see("end")
    
  
  def arithmetic(self, node):
    operation = node.children[0]
    op1_node = operation.children[1]
    op1_symbol = self.get_value(op1_node)
    self.check(op1_symbol, ["NUMBAR", "NUMBR"])
    op2_node = operation.children[2]
    op2_symbol = self.get_value(op2_node)
    self.check(op2_symbol, ["NUMBAR", "NUMBR"])
    op1_symbol.value = float(op1_symbol.value) if op1_symbol.type == "NUMBAR" else int(op1_symbol.value)
    op2_symbol.value = float(op2_symbol.value) if op2_symbol.type == "NUMBAR" else int(op2_symbol.value)
    
    if (operation.type == "ADDITION"):
      ans = op1_symbol.value + op2_symbol.value
    elif (operation.type == "SUBTRACTION"):
      ans = op1_symbol.value - op2_symbol.value
    elif (operation.type == "MULTIPLICATION"):
      ans = op1_symbol.value * op2_symbol.value
    elif (operation.type == "DIVISION"):
      ans = op1_symbol.value / op2_symbol.value
    elif (operation.type == "MODULO"):
      ans = op1_symbol.value % op2_symbol.value
    elif (operation.type == "GREATER"):
      ans = max(op1_symbol.value, op2_symbol.value)
    elif (operation.type == "LESSER"):
      ans = min(op1_symbol.value, op2_symbol.value)
    val_type = "NUMBAR" if (type(ans) == float) else "NUMBR"
    return Symbol(val_type, str(ans))
  
  def comparison(self, node):
    comp_operation = node.children[0]
    op1_node = comp_operation.children[1]
    op1_symbol = self.get_value(op1_node)
    self.check(op1_symbol, ["NUMBAR", "NUMBR"])
    op2_node = comp_operation.children[2]
    op2_symbol = self.get_value(op2_node)
    self.check(op2_symbol, ["NUMBAR", "NUMBR"])
    op1_symbol.value = float(op1_symbol.value) if op1_symbol.type == "NUMBAR" else int(op1_symbol.value)
    op2_symbol.value = float(op2_symbol.value) if op2_symbol.type == "NUMBAR" else int(op2_symbol.value)
    
    if (comp_operation.type == "EQUAL"):
      if (type(op1_symbol.value) != type(op2_symbol.value)):
        ans = False
      else:
        ans = op1_symbol.value == op2_symbol.value
    elif (comp_operation.type == "NOTEQUAL"):
      if (type(op1_symbol.value) != type(op2_symbol.value)):
        ans = True
      else:
        ans = op1_symbol.value != op2_symbol.value
    ans = "WIN" if ans else "FAIL"
    return Symbol("TROOF", ans)
  
  def concatenation(self, node):
    smoosh_op = node.children[1]
    string = ""
    for value_node in smoosh_op.children:
      symbol = self.get_value(value_node)
      string += str(symbol.value)
    
    return Symbol("YARN", string)
  
  def boolean(self, node):
    booltype = node.children[0]
    bool_operation = booltype.children[0]
    if (bool_operation.type == "NOT"):
      op1_node = bool_operation.children[1]
      op1_symbol = self.get_value(op1_node)
      self.check(op1_symbol, ["TROOF"])
      op1_bool = True if op1_symbol.value == "WIN" else False
      ans = not op1_bool
    elif (bool_operation.type in ["ALL", "ANY"]):
      boolop = bool_operation.children[1]
      current_op_symbol = self.get_value(boolop.children[0])
      self.check(current_op_symbol, ["TROOF"])
      op1_bool = True if current_op_symbol.value == "WIN" else False
      for value in boolop.children[1:]:
        op_symbol = self.get_value(value)
        self.check(op_symbol, ["TROOF"])
        op2_bool = True if op_symbol.value == "WIN" else False
        if (bool_operation.type == "ALL"):
          op1_bool = op1_bool and op2_bool
        else:
          op1_bool = op1_bool or op2_bool
      ans = op1_bool
    else:
      op1_node = bool_operation.children[1]
      op1_symbol = self.get_value(op1_node)
      self.check(op1_symbol, ["TROOF"])
      op2_node = bool_operation.children[2]
      op2_symbol = self.get_value(op2_node)
      self.check(op2_symbol, ["TROOF"])

      op1_bool = True if op1_symbol.value == "WIN" else False
      op2_bool = True if op2_symbol.value == "WIN" else False
      
      if (bool_operation.type == "AND"):
        ans = op1_bool and op2_bool
      elif (bool_operation.type == "OR"):
        ans = op1_bool or op2_bool 
      elif (bool_operation.type == "XOR"):
        ans = op1_bool != op2_bool
    
    ans = "WIN" if ans else "FAIL"
    val_type = "TROOF"
    return Symbol(val_type, ans)
     
       
  def expr(self, node):
    child = node.children[0]
    if (child.type == "ARITHMETIC"):
      return self.arithmetic(child)
    elif (child.type == "COMPARISON"):
      return self.comparison(child)
    elif (child.type == "BOOLEAN"):
      return self.boolean(child)
    else:
      return self.concatenation(child)
    
  def get_value(self, node):
    child = node.children[0]
    if (child.type == "VARIABLE"):
      variable = child.children[0]
      identifier = variable.value
      self.lookup(identifier)
      return self.symbol_table[identifier]
    elif (child.type == "EXPR"):
      return self.expr(child)
    else:
      value = child.children[0].value
      val_type = child.children[0].type
      return Symbol(val_type, value)
    
  def check(self, symbol, data_type):
    global lineNumber
    if (not (symbol.type in data_type)):
      raise Exception(f"Semantic Error: Unexpected data type {symbol.type} on line {lineNumber}")
  
  # Adding a new variable or updating the value of the variable
  def insert(self, name, symbol):
    self.symbol_table.update({
      name: symbol
    })
  
  # This function is for knowing whether the current variable is already declared
  def lookup(self, name):
    global lineNumber
    for key in self.symbol_table:
      if (key == name):
        return
    raise Exception(f"Semantic Error: Variable {name} is not yet declared on line {lineNumber}")