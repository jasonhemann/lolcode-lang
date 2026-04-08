from classes.Node import Node

DELIMITERS = ["KTHXBYE_KEYWORD", "NO_WAI_KEYWORD", "OIC_KEYWORD", "OMG_KEYWORD", "OMGWTF_KEYWORD"]

class Parser:
  def __init__(self, tokens):
    self.tokens = tokens
    self.current_token = tokens[0]
  
  def eat(self, token_type):
    if (token_type == self.current_token.type):
      self.tokens.pop(0)
    else:
      raise Exception(f"Syntax Error in line number {self.current_token.line_number}: Expect {token_type} but saw {self.current_token.type}")
    if (len(self.tokens) != 0): 
      self.current_token = self.tokens[0]
    else: 
      print("Finished parsing: Tokens is empty")
  
  def parse(self):
    # <program>
    tree = self.program()
    return tree
      
# ***************************************GRAMMAR****************************************************************
# 1. Every method is equivalent to one production rule
# 2. All non-terminal is expanded using the equivalent method
# 3. Every method returns a Node (pls check the Node class)
# 4. For Node type, the convention is to use the equivalent production rule name in uppercase
# 5. For Node value, only the identifiers and literals will fill this argument
# 6. If the parsing reaches a terminal, self.eat(<terminal>) will be called (pls check the implementation of self.eat())
# 7. All syntax errors are handled by self.eat()
# 8. If the production rule is recursive, use tail recursion to accumulate all the duplicate nodes in a single children array.
      # (check the printop() and statement() for the pattern)
# 9. For the walrus operator ":=", google "Assignment Expression Python"
# 10. Check our grammar in google docs to see the overall structure. All of this is patterned from it.

# +++++++++++++++++++++++++INPUT++++++++++++++++++

  def gimmeh(self):
    children = []
    if(self.current_token.type == "GIMMEH_KEYWORD"):
      children.append(Node("GIMMEH_KEYWORD"))
      self.eat("GIMMEH_KEYWORD")
      children.append(self.variable())
    else:
      return False

    return Node("INPUT",children=children)



# +++++++++++++++++++++++++MULTILINECOMMENT++++++++++++++++++
  def multilinecomment(self):
    if(self.current_token.type == "OBTW_KEYWORD"):
      lineNumber = 2
      self.eat("OBTW_KEYWORD")
      while self.current_token.type == "BTW_KEYWORD":
        self.comment()
        lineNumber = lineNumber + 1
      self.eat("TLDR_KEYWORD")
      return Node("MULTICOMMENT",value = str(lineNumber))
    else:
      return False

  def comment(self):
    if(self.current_token.type == "BTW_KEYWORD"):
      self.eat("BTW_KEYWORD")
      return Node("COMMENT")
    else:
      return False    
      

  
# +++++++++++++++++++++++++CONTROL+++++++++++++++++++++++++++
  def control(self):
    children = []
    # <ifthen>
    if (if_then_node := self.ifthen_statement()):
      children.append(if_then_node)
    # <switch>
    elif (switch_node := self.switch_statement()):
      children.append(switch_node)
    else:
      return False

    return Node("CONTROL", children = children)

  # Nilagyan ko ng _statement / _block kasi yung break ay keyword sa python
  # Nilagyan ko na lahat para uniform
  # If hindi tama yung level ng linebreak sa tree, ililipat lang yung mga location ng pagcall ng self.end() sa functions under ng control

  def ifthen_statement(self):
    children = []
    
    if self.current_token.type == "O_RLY?_KEYWORD":
      children.append(Node("O_RLY?_KEYWORD"))
      self.eat("O_RLY?_KEYWORD")
      self.end()
      children.append(self.if_block())
      children.append(self.else_block())
    else:
        return False

    self.eat("OIC_KEYWORD")
    children.append(Node("OIC_KEYWORD"))
      
    return Node("IFTHEN",children = children)
  
  def switch_statement(self):
    children = []
    if self.current_token.type == "WTF?_KEYWORD":
      children.append(Node("WTF?_KEYWORD"))
      self.eat("WTF?_KEYWORD")
      self.end()
      children.append(self.caseop())
      if self.current_token.type == "OMGWTF_KEYWORD":
        children.append(self.defaultcase_block())
      else:
        self.eat("OMGWTF_KEYWORD")
    else:
      return False
    
    self.eat("OIC_KEYWORD")
    children.append(Node("OIC_KEYWORD"))
      
    return Node("SWITCH",children = children)

  def break_statement(self):
    if self.current_token.type == "GTFO_KEYWORD":
      self.eat("GTFO_KEYWORD")
      
    else:
      return False

    return Node("GTFO_KEYWORD")


  def if_block(self):
    children = []
    
    children.append(Node("YA_RLY_KEYWORD"))
    self.eat("YA_RLY_KEYWORD")
    
    codeblock = self.codeblock([], True)
    children.append(codeblock)

    
    return Node("IF",children=children)
  
  def else_block(self):
    children = []
    children.append(Node("NO_WAI_KEYWORD"))
    self.eat("NO_WAI_KEYWORD")

    codeblock = self.codeblock([], True)
    children.append(codeblock)   

    return Node("ELSE",children=children)
  
  def caseop(self):
    children = []
    children.append(self.case_block())
    
    if self.current_token.type == "OMG_KEYWORD":
      
      while self.current_token.type == "OMG_KEYWORD":
        children.append(self.case_block())  
    
    return Node("CASEOP",children = children)

  def case_block(self):
    children = []
    if self.current_token.type == "OMG_KEYWORD":
      children.append(Node("OMG_KEYWORD"))
      self.eat("OMG_KEYWORD")
      children.append(self.value())
      self.end()
      children.append(self.codeblock([], True))

    else:
      return False

    return Node("CASE",children = children)

  def defaultcase_block(self):
    children = []
    
    if self.current_token.type == "OMGWTF_KEYWORD":
      children.append(Node("OMGWTF_KEYWORD"))
      self.eat("OMGWTF_KEYWORD")
      self.end()
      children.append(self.codeblock([], True))
    else:
      return False


    return Node("DEFAULTCASE",children = children)

# +++++++++++++++++++++++++DECLARATION+++++++++++++++++++++++
  def declaration(self, is_block):
    children = []
    # I HAS A
    if(self.current_token.type == "I_HAS_A_KEYWORD"):
      children.append(Node("I_HAS_A_KEYWORD"))
      self.eat("I_HAS_A_KEYWORD")
    else:
      return False

    if (is_block):
      raise Exception(f"Syntax Error in line number {self.current_token.line_number}: DECLARATION is not allowed inside program blocks")
    
    # varident
    children.append(Node("VAR_IDENTIFIER", self.current_token.name))
    self.eat("VAR_IDENTIFIER")
    
    # I HAS A varident <initialization>
    if (self.current_token.type == "ITZ_KEYWORD"):
      init_node =self.initialization()
      children.append(init_node)
    
    return Node("DECLARATION", children = children)
  
  def initialization(self):
    children = []
    
    children.append(Node("ITZ_KEYWORD"))
    self.eat("ITZ_KEYWORD")

    value_node = self.value()
    children.append(value_node)
    
    return Node("INITIALIZATION", children = children)



# +++++++++++++++++++++++++INPUT+++++++++++++++++++++++++++++
  def input(self):
    return False

# +++++++++++++++++++++++++PRINT+++++++++++++++++++++++++++++
  def print(self):
    children = []
    # VISIBLE
    if(self.current_token.type == "VISIBLE_KEYWORD"):
      children.append(Node("VISIBLE_KEYWORD"))
      self.eat("VISIBLE_KEYWORD")
    else:
      return False
    
    # <printop>
    printop_node = self.printop([])
    children.append(printop_node)
  
    return Node("PRINT", children = children)
  
  # Tail-recursion is used to catch multiple argument in VISIBLE/printing
  def printop(self,children):
    # <value>
    value_node = self.value()
    children.append(value_node)
    
    # <printop><value>
    if (self.current_token.type != "LINEBREAK" and self.current_token.type != "BTW_KEYWORD"):
      self.printop(children)
    
    return Node("PRINTOP", children = children)


# +++++++++++++++++++++++++ASSIGNMENT++++++++++++++++++++++++
  def assign(self):
    children = []
    # <variable>
    variable_node = self.variable()
    if (variable_node):
      children.append(variable_node)
    else:
      return False
    
    # R
    self.eat("R_KEYWORD")
    children.append(Node("R_KEYWORD"))
    
    # <value>
    value_node = self.value()
    children.append(value_node)
  
    return Node("ASSIGN", children = children)
  
  def variable(self):
    children = []
    # varident
    if (self.current_token.type == "VAR_IDENTIFIER"):
      children.append(Node("VAR_IDENTIFIER", value = self.current_token.name))
      self.eat("VAR_IDENTIFIER")
    # IT
    elif (self.current_token.type == "IT_KEYWORD"):
      children.append(Node("IT_KEYWORD", value = self.current_token.name))
      self.eat("IT_KEYWORD")
    else:
      return False
    
    return Node("VARIABLE", children = children)
  
  def value(self):
    children = []
    # <variable>
    if (variable_node := self.variable()):
      children.append(variable_node)
    # <expr>
    elif (expr_node := self.expr()):
      children.append(expr_node)
    elif (literal_node := self.literal()):
      # <literal>
      children.append(literal_node)
    else:
      return False
    
    return Node("VALUE", children = children)
  
  def literal(self):
    children = []
 
    # Catches all the literal
    if(self.current_token.type == "YARN"):
      children.append(Node("YARN", value= self.current_token.name))
      self.eat("YARN")
    elif(self.current_token.type == "NUMBR"):
      children.append(Node("NUMBR",value= self.current_token.name))
      self.eat("NUMBR")
    elif(self.current_token.type == "NUMBAR"):
      children.append(Node("NUMBAR",value= self.current_token.name))
      self.eat("NUMBAR")
    elif(self.current_token.type == "TROOF"):
      children.append(Node("TROOF",value = self.current_token.name))
      self.eat("TROOF")
    
    return Node("LITERAL", children = children)


# ===============CONCATENATION==============
  def concatenation(self):
    children = []
    # SMOOSH
    if (self.current_token.type == "SMOOSH_KEYWORD"):
      self.eat("SMOOSH_KEYWORD")
      children.append(Node("SMOOSH_KEYWORD"))
    else:
      return False
    
    # <strconcat>
    children.append(self.strconcat())
    
    return Node("CONCATENATION", children = children)
  
  def strconcat(self):
    children = []
    
    # Nacacatch na kasi ung error sa def value kaya di na ako nag lagay ng if-else dito
    if (value_node := self.value()):
      children.append(value_node)
    else:
      raise Exception(f"Syntax Error in line number {self.current_token.line_number}: Operand must be a VALUE")

    self.eat("AN_KEYWORD")
    
    if (value_node := self.value()):
      children.append(value_node)
    else:
      raise Exception(f"Syntax Error in line number {self.current_token.line_number}: Operand must be a VALUE")

    
    while self.current_token.type == "AN_KEYWORD":
      self.eat("AN_KEYWORD")
      children.append(self.value())


    return Node("STRCONCAT",children = children)
    

# ===============COMPARISON=================
  def comparison(self):
    children = []
    # <equal>
    if (equal_node := self.equal()):
      children.append(equal_node)
    # <noequal>
    elif (noequal_node := self.noequal()):
      children.append(noequal_node)
    else:
      return False

    return Node("COMPARISON", children = children)
  
  def equal(self):
    children = []

    # BOTH SAEM
    if (self.current_token.type == "BOTH_SAEM_KEYWORD"):
      children.append(Node("BOTH_SAEM_KEYWORD"))
      self.eat("BOTH_SAEM_KEYWORD")
      
    else:
      return False

    if (value_node := self.value()):
      children.append(value_node)
    else:
      raise Exception(f"Syntax Error in line number {self.current_token.line_number}: Operand must be a VALUE")
    
    # AN
    self.eat("AN_KEYWORD")
    
    if (value_node := self.value()):
      children.append(value_node)
    else:
      raise Exception(f"Syntax Error in line number {self.current_token.line_number}: Operand must be a VALUE")

    return Node("EQUAL",children = children)

  def noequal(self):
    children = []

    #NOT EQUAL
    if (self.current_token.type == "DIFFRINT_KEYWORD"):
      children.append(Node("DIFFRINT_KEYWORD"))
      self.eat("DIFFRINT_KEYWORD")
      
    else:
      return False

    if (value_node := self.value()):
      children.append(value_node)
    else:
      raise Exception(f"Syntax Error in line number {self.current_token.line_number}: Operand must be a VALUE")
    
    # AN
    self.eat("AN_KEYWORD")
    
    if (value_node := self.value()):
      children.append(value_node)
    else:
      raise Exception(f"Syntax Error in line number {self.current_token.line_number}: Operand must be a VALUE")
    
    return Node("NOTEQUAL",children = children)
  
# ===============BOOLEAN====================
  def boolean(self):
    children = []
    # <bool1>
    if (bool1_node := self.bool1()):
      children.append(bool1_node)
    # <bool2>
    elif (bool2_node := self.bool2()):
      children.append(bool2_node)
    else:
      return False

    return Node("BOOLEAN", children = children)
  
  def bool1(self):
    children = []
    if(andLol_node := self.andLol()):
      children.append(andLol_node)
    elif(orLol_node := self.orLol()):
      children.append(orLol_node)
    elif(xorLol_node := self.xorLol()):
      children.append(xorLol_node)
    elif(notLol_node := self.notLol()):
      children.append(notLol_node)
    else:
      return False

    return Node("BOOL1",children = children)
    
  def bool2(self):
    children = []
    if(all_code := self.allLol()):
      children.append(all_code)
    elif(any_code := self.anyLol()):
      children.append(any_code)
    else:
      return False

    return Node("BOOL2",children = children)

  def andLol(self):
    children = []
    # BOTH OF
    if (self.current_token.type == "BOTH_OF_KEYWORD"):
      children.append(Node("BOTH_OF_KEYWORD"))
      self.eat("BOTH_OF_KEYWORD")
      
    else:
      return False
    
    if (value_node := self.value()):
      children.append(value_node)
    else:
      raise Exception(f"Syntax Error in line number {self.current_token.line_number}: Operand must be a VALUE")
    
    # AN
    self.eat("AN_KEYWORD")
    
    if (value_node := self.value()):
      children.append(value_node)
    else:
      raise Exception(f"Syntax Error in line number {self.current_token.line_number}: Operand must be a VALUE")
    
    return Node("AND",children = children)
    
  def orLol(self):
    children = []
    # EITHER OF
    if (self.current_token.type == "EITHER_OF_KEYWORD"):
      children.append(Node("EITHER_OF_KEYWORD"))
      self.eat("EITHER_OF_KEYWORD")
      
    else:
      return False
    
    if (value_node := self.value()):
      children.append(value_node)
    else:
      raise Exception(f"Syntax Error in line number {self.current_token.line_number}: Operand must be a VALUE")
    
    # AN
    self.eat("AN_KEYWORD")
    
    
    if (value_node := self.value()):
      children.append(value_node)
    else:
      raise Exception(f"Syntax Error in line number {self.current_token.line_number}: Operand must be a VALUE")
    

    return Node("OR",children = children)
  
  def xorLol(self):
    children = []
    # WON OF
    if (self.current_token.type == "WON_OF_KEYWORD"):
      children.append(Node("WON_OF_KEYWORD"))
      self.eat("WON_OF_KEYWORD")
    else:
      return False
    
    # <bool1> | <troof>
    if (value_node := self.value()):
      children.append(value_node)
    else:
      raise Exception(f"Syntax Error in line number {self.current_token.line_number}: Operand must be a VALUE")

    # AN
    self.eat("AN_KEYWORD")
    
    # <bool1> | <troof>
    if (value_node := self.value()):
      children.append(value_node)
    else:
      raise Exception(f"Syntax Error in line number {self.current_token.line_number}: Operand must be a VALUE")
    
    

    return Node("XOR",children = children)
    
  def notLol(self):
    children = []
    # NOT
    if (self.current_token.type == "NOT_KEYWORD"):
      children.append(Node("NOT_KEYWORD"))
      self.eat("NOT_KEYWORD")
    else:
      return False
    # <bool1> | <troof>
    if (value_node := self.value()):
      children.append(value_node)
    else:
      raise Exception(f"Syntax Error in line number {self.current_token.line_number}: Operand must be a VALUE")
    
    
    return Node("NOT",children = children)
  
  def boolop(self):
    children = []
    if (value_node := self.value()):
      children.append(value_node)
      value_node = value_node.children[0]
      if (value_node.type == "EXPR"):
        while (value_node.children and value_node.type != "BOOL2"):
          value_node = value_node.children[0]
        if (value_node.type == "BOOL2"):
          child = value_node.children[0]
          if (child.type == "ALL" or child.type == "ANY"):
            raise Exception(f"Syntax Error in line number {self.current_token.line_number}: ALL or ANY is not allowed as the operand")
    else:
      raise Exception(f"Syntax Error in line number {self.current_token.line_number}: Operand must be a VALUE")

    while (self.current_token.type != "MKAY_KEYWORD"):
      self.eat("AN_KEYWORD")
      
      if (value_node := self.value()):
        children.append(value_node)
        value_node = value_node.children[0]
        if (value_node.type == "EXPR"):
          while (value_node.children and value_node.type != "BOOL2"):
            value_node = value_node.children[0]
          if (value_node.type == "BOOL2"):
            print("yes")
            child = value_node.children[0]
            if (child.type == "ALL" or child.type == "ANY"):
              raise Exception(f"Syntax Error in line number {self.current_token.line_number}: ALL or ANY is not allowed as the operand")
      else:
        raise Exception(f"Syntax Error in line number {self.current_token.line_number}: Operand must be a VALUE")

      if(self.current_token.type == "LINEBREAK" or self.current_token.type == "BTW_KEYWORD"):
        break
        
    return Node("BOOLOP",children=children)

  def allLol(self):
    children = []
    if(self.current_token.type == "ALL_OF_KEYWORD"):
      children.append(Node("ALL_OF_KEYWORD"))
      self.eat("ALL_OF_KEYWORD")
    else:
      return False
    
    all_node = self.boolop()
    children.append(all_node)
    children.append(Node("MKAY"))
    self.eat("MKAY_KEYWORD")
  

    return Node("ALL",children = children)

  def anyLol(self):
    children = []
    if(self.current_token.type == "ANY_OF_KEYWORD"):
      children.append(Node("ANY_OF_KEYWORD"))
      self.eat("ANY_OF_KEYWORD")
    else:
      return False
    
    if all_node := self.boolop():
      children.append(all_node)
    else:
      return False

    children.append(Node("MKAY"))
    self.eat("MKAY_KEYWORD")

    return Node("ANY",children = children)

  
# ==============ARITHMETIC==================

  def arithmetic(self):
    children = []
    # <addition>
    if (addition_node := self.addition()):
      children.append(addition_node)
    # <subtraction>
    elif (subtraction_node := self.subtraction()):
      children.append(subtraction_node)
    # <multiplication>
    elif (multiplication_node := self.multiplication()):
      children.append(multiplication_node)
    # <division>
    elif (division_node := self.division()):
      children.append(division_node)
    # <modulo>
    elif (modulo_node := self.modulo()):
      children.append(modulo_node)
    # <greater>
    elif (greater_node := self.greater()):
      children.append(greater_node)
    # <lesser>
    elif (lesser_node := self.lesser()):
      children.append(lesser_node)
    else:
      return False
    
    return Node("ARITHMETIC", children = children)
  
  # Temporary
  def number(self):
    children = []
    
    if (self.current_token.type == "NUMBR"):
      children.append(Node("NUMBR",value = self.current_token.name))
      self.eat("NUMBR")
    else:
      children.append(Node("NUMBAR",value = self.current_token.name))
      self.eat("NUMBAR")
      
    
    return Node("NUMBER", children = children)
  
  def addition(self):
   
    children = []
    # SUM OF
    if (self.current_token.type == "SUM_OF_KEYWORD"):
      children.append(Node("SUM_OF_KEYWORD"))
      self.eat("SUM_OF_KEYWORD")
      
    else:
      return False
    
    if (value_node := self.value()):
      children.append(value_node)
    else:
      raise Exception(f"Syntax Error in line number {self.current_token.line_number}: Operand must be a VALUE")
    
    # AN
    self.eat("AN_KEYWORD")
    
    
    if (value_node := self.value()):
      children.append(value_node)
    else:
      raise Exception(f"Syntax Error in line number {self.current_token.line_number}: Operand must be a VALUE")
    
    return Node("ADDITION", children = children)
  
  def subtraction(self):
    children = []
    # DIFF OF
    if (self.current_token.type == "DIFF_OF_KEYWORD"):
      children.append(Node("DIFF_OF_KEYWORD"))
      self.eat("DIFF_OF_KEYWORD")
      
    else:
      return False
    
    if (value_node := self.value()):
      children.append(value_node)
    else:
      raise Exception(f"Syntax Error in line number {self.current_token.line_number}: Operand must be a VALUE")
    
    
    # AN
    self.eat("AN_KEYWORD")
    
    
    if (value_node := self.value()):
      children.append(value_node)
    else:
      raise Exception(f"Syntax Error in line number {self.current_token.line_number}: Operand must be a VALUE")
    
    
    return Node("SUBTRACTION", children = children)
    
  def multiplication(self):
    # PRODUKT OF
    children = []
    if (self.current_token.type == "PRODUKT_OF_KEYWORD"):
      children.append(Node("PRODUKT_OF_KEYWORD"))
      self.eat("PRODUKT_OF_KEYWORD")
      
    else:
      return False
    
    if (value_node := self.value()):
      children.append(value_node)
    else:
      raise Exception(f"Syntax Error in line number {self.current_token.line_number}: Operand must be a VALUE")
    
    
    # AN
    self.eat("AN_KEYWORD")
    
    
    if (value_node := self.value()):
      children.append(value_node)
    else:
      raise Exception(f"Syntax Error in line number {self.current_token.line_number}: Operand must be a VALUE")
    
    
    return Node("MULTIPLICATION", children = children)
    
  def division(self):
    # QUOSHUNT OF
    children = []
    if (self.current_token.type == "QUOSHUNT_OF_KEYWORD"):
      children.append(Node("QUOSHUNT_OF_KEYWORD"))
      self.eat("QUOSHUNT_OF_KEYWORD")
      
    else:
      return False
    
    if (value_node := self.value()):
      children.append(value_node)
    else:
      raise Exception(f"Syntax Error in line number {self.current_token.line_number}: Operand must be a VALUE")
    
    
    # AN
    self.eat("AN_KEYWORD")
    
  
    if (value_node := self.value()):
      children.append(value_node)
    else:
      raise Exception(f"Syntax Error in line number {self.current_token.line_number}: Operand must be a VALUE")
    

    return Node("DIVISION", children = children)
    
  def modulo(self):
    # MOD OF
    children = []
    if (self.current_token.type == "MOD_OF_KEYWORD"):
      children.append(Node("MOD_OF_KEYWORD"))
      self.eat("MOD_OF_KEYWORD")
      
    else:
      return False
    
    if (value_node := self.value()):
      children.append(value_node)
    else:
      raise Exception(f"Syntax Error in line number {self.current_token.line_number}: Operand must be a VALUE")
    
    # AN
    self.eat("AN_KEYWORD")
    
    
    if (value_node := self.value()):
      children.append(value_node)
    else:
      raise Exception(f"Syntax Error in line number {self.current_token.line_number}: Operand must be a VALUE")
    
    
    return Node("MODULO", children = children)
    
  def greater(self):
    # BIGGR OF
    children = []
    if (self.current_token.type == "BIGGR_OF_KEYWORD"):
      children.append(Node("BIGGR_OF_KEYWORD"))
      self.eat("BIGGR_OF_KEYWORD")
      
    else:
      return False
    
    if (value_node := self.value()):
      children.append(value_node)
    else:
      raise Exception(f"Syntax Error in line number {self.current_token.line_number}: Operand must be a VALUE")
    
    
    # AN
    self.eat("AN_KEYWORD")
    
    
    if (value_node := self.value()):
      children.append(value_node)
    else:
      raise Exception(f"Syntax Error in line number {self.current_token.line_number}: Operand must be a VALUE")
    
    
    return Node("GREATER", children = children)
    
  def lesser(self):
    
    # SMALLR OF
    children = []
    if (self.current_token.type == "SMALLR_OF_KEYWORD"):
      children.append(Node("SMALLR_OF_KEYWORD"))
      self.eat("SMALLR_OF_KEYWORD")
    else:
      return False
    
    if (value_node := self.value()):
      children.append(value_node)
    else:
      raise Exception(f"Syntax Error in line number {self.current_token.line_number}: Operand must be a VALUE")
    
    
    # AN
    self.eat("AN_KEYWORD")
    
    
    if (value_node := self.value()):
      children.append(value_node)
    else:
      raise Exception(f"Syntax Error in line number {self.current_token.line_number}: Operand must be a VALUE")
    
    
    return Node("LESSER", children = children)
    

# +++++++++++++++++++++++EXPRESSION+++++++++++++++++++++++++
  def expr(self):
    children = []
    # <arithmetic>
    if (arithmetic_node := self.arithmetic()):
      children.append(arithmetic_node)
    # <boolean>
    elif (boolean_node := self.boolean()):
      children.append(boolean_node)
    # <comparison>
    elif (comparison_node := self.comparison()):
      children.append(comparison_node)
    # <concatenation>
    elif (concatenation_node := self.concatenation()):
      children.append(concatenation_node)
    else:
      return False
    
    return Node("EXPR", children = children)

  
  def end(self):
    self.comment()
    self.eat("LINEBREAK")
  
  def statement(self, is_block):
    children = []
    # <expr>
    if (expr_node := self.expr()):
      children.append(expr_node)
    # <assign>
    elif (assign_node := self.assign()):
      children.append(assign_node)
    # <print>
    elif (print_node := self.print()):
      children.append(print_node)
    # <input>
    elif (input_node := self.input()):
      children.append(input_node)
    # <declaration>
    elif (declaration_node := self.declaration(is_block)):
      children.append(declaration_node)
    # <control>
    elif (control_node := self.control()):
      children.append(control_node)
    # <gimmeh>
    elif (gimmeh_node := self.gimmeh()):
      children.append(gimmeh_node)
    # <comment>
    elif (comment_node := self.comment()):
      children.append(comment_node)
    # <multilinecomment>
    elif (multilinecomment_node := self.multilinecomment()):
      children.append(multilinecomment_node)
    elif (break_statement := self.break_statement()):
      children.append(break_statement)
    # <end>
    self.end()
    children.append(Node("LINEBREAK"))
    if (len(children) == 0):
      return
    return Node("STATEMENT", children = children)
  
  def codeblock(self,children, is_block = False):
    # inalis ko yung children = [] sa argument kasi nagcacause ulit ng multiple loop/repetition ng code, same error na naencounter sa printop
    # <statement> 
    statement = self.statement(is_block)
    if (statement):
      children.append(statement)
    # <statement><codeblock>
    token_type = self.current_token.type
    
    # Pwede gawan ng list yung mga != dito, para token_type not in list yung condition
    if(not(token_type in DELIMITERS)):
      self.codeblock(children, is_block)

    return Node("CODEBLOCK", children = children)
  
  def program(self):
    children = []
    # Comment before HAI
    if self.current_token.type == "OBTW_KEYWORD":
        children.append(self.multilinecomment())
        # children.append(Node("LINEBREAK"))
        self.end()
    if self.current_token.type == "BTW_KEYWORD":
        children.append(self.comment())
        # children.append(Node("LINEBREAK"))
        self.end()
    # HAI
    
    self.eat("HAI_KEYWORD")
    children.append(Node("HAI_KEYWORD"))
    
    # <linebreak>
    self.eat("LINEBREAK")
    children.append(Node("LINEBREAK"))

    # <codeblock>
    if (self.current_token.type != "KTHXBYE_KEYWORD"):
      codeblock = self.codeblock([])
      children.append(codeblock)
    
    # KTHXBYE
    self.eat("KTHXBYE_KEYWORD")
    children.append(Node("KTHXBYE_KEYWORD"))

    # <linebreak>
    self.eat("LINEBREAK")
    children.append(Node("LINEBREAK"))

    # Comment after KTHXBYE
    while (len(self.tokens) != 0):
      self.end()

    return Node("PROGRAM", children = children)

  
