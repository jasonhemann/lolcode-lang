literals = ["NUMBR literal",
            "NUMBAR literal",
            "YARN literal",
            "TROOF literal",
            "NOOB"
            ]
expressionKeywords = {
                        "arithmetic":
                            ["SUM OF",
                            "DIFF OF",
                            "PRODUKT OF",
                            "QUOSHUNT OF",
                            "MOD OF",
                            "BIGGR OF",
                            "SMALLR OF"],
                        "boolean":
                            ["BOTH OF",
                            "EITHER OF",
                            "WON OF",
                            "NOT",
                            "ANY OF",
                            "ALL OF"],
                        "comparison":
                            ["BOTH SAEM",
                            "DIFFRINT"],
                        "concatenation":
                            ["SMOOSH"]
                    }

def arithmeticExpSemantics(lineNumber, symbolTable, lexemes, types):
  # * Gets the index of ITZ
  if("variable initialization keyword" in types[lineNumber]):
    expressionIndex = lexemes[lineNumber].index("ITZ")
  #put other cases where the arithmetic expression might be
  elif("print keyword" in types[lineNumber]):
    expressionIndex = lexemes[lineNumber].index("VISIBLE")

    if types[lineNumber][expressionIndex + 1] not in expressionKeywords["arithmetic"]:
      # Find the first operation to appear in string
      operationIndices = []
      for index in range(len(lexemes[lineNumber])):
        if lexemes[lineNumber][index] in expressionKeywords["arithmetic"]:
          operationIndices.append(index)
      
      expressionIndex = operationIndices[0] - 1     
      
  else:
    expressionIndex = -1 

  # * Gets the indices of arithmetic operations
  operationIndices = []
  lexemeExpression = 0
  typeExpression = 0
  for index in range(len(lexemes[lineNumber])):
    if lexemes[lineNumber][index] in expressionKeywords["arithmetic"]:
      operationIndices.append(index)

  # * Gets the indices of AN
  anIndices = []
  for index in range(len(lexemes[lineNumber])):
    if lexemes[lineNumber][index] == "AN":
      try:
        if types[lineNumber][index - 1] not in ["identifier", "string delimiter", "NUMBR literal", "NUMBAR literal", "TROOF literal", "NOOB"]:
          return "[Line " + str(lineNumber) + "] SyntaxError: Expected a valid identifier or literal"
        if types[lineNumber][index + 1] not in ["identifier", "string delimiter", "NUMBR literal", "NUMBAR literal", "TROOF literal", "NOOB", "add operator", "subtract operator", "multiply operator", "divide operator", "max operator", "min operator"]:
          return "[Line " + str(lineNumber) + "] SyntaxError: Expected a valid identifier or literal"
        
        anIndices.append(index)
      except IndexError:
        return "[Line " + str(lineNumber) + "] SyntaxError: Expected an identifier after argument separator keyword"

  for operator in expressionKeywords["arithmetic"]:
    if lexemes[lineNumber][expressionIndex + 1] == operator:
      # parentOperation = operator
      lexemeExpression = lexemes[lineNumber][(expressionIndex + 1):(anIndices[len(anIndices) - 1] + 2)]
      typeExpression = types[lineNumber][(expressionIndex + 1):(anIndices[len(anIndices) - 1] + 2)]

      # * Removes the string delimiters from the list
      while True:
        try:
          lexemeExpression.remove("\"")
          typeExpression.remove("string delimiter")
        except ValueError:
          break
      break

  if len(anIndices) != len(operationIndices):
    print()
    return(f"[Line {lineNumber}] SyntaxError: Invalid expression")
  

  while True:
    print(lexemeExpression)
    # * Breaks the loop if lexemeExpression is equal to 1
    if (len(lexemeExpression) == 1):
      break

    # * Refreshes the operationIndices
    operationIndices.clear()
    for index in range(len(lexemeExpression)):
      if lexemeExpression[index] in expressionKeywords["arithmetic"]:
          operationIndices.append(index)  

    tempVal = 0

    # * Get index of first operation to solve starting from the last
    lastIndexOperator = operationIndices[len(operationIndices) - 1]

    if typeExpression[lastIndexOperator + 1] == "identifier":   # ! identifier (1st operand)
      if symbolTable.get(lexemeExpression[lastIndexOperator + 1]):
        identifier = symbolTable[lexemeExpression[lastIndexOperator + 1]]
        lexemeExpression[lastIndexOperator + 1] = identifier[0]
        typeExpression[lastIndexOperator + 1] = identifier[1]
      else:
        return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized variable"
    elif typeExpression[lastIndexOperator + 1] not in ["NUMBR literal", "NUMBAR literal", "TROOF literal", "string delimiter", "YARN literal", "NOOB"]:
      return "[Line " + str(lineNumber) + "] SyntaxError: Invalid expression"

    
    if typeExpression[lastIndexOperator + 3] == "identifier":   # ! identifier (2nd operand)
      if symbolTable.get(lexemeExpression[lastIndexOperator + 3]):
        identifier = symbolTable[lexemeExpression[lastIndexOperator + 3]]
        lexemeExpression[lastIndexOperator + 3] = identifier[0]
        typeExpression[lastIndexOperator + 3] = identifier[1]
      else:
        return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized variable"
    elif typeExpression[lastIndexOperator + 3] not in ["NUMBR literal", "NUMBAR literal", "TROOF literal", "string delimiter", "YARN literal", "NOOB"]:
      return "[Line " + str(lineNumber) + "] SyntaxError: Invalid expression"
    
    print(lexemeExpression)
    print(typeExpression)

    if lexemeExpression[lastIndexOperator] == "SUM OF":
      if typeExpression[lastIndexOperator + 1] == "NUMBR literal":    # ! NUMBR Literal (1st operand)
        if typeExpression[lastIndexOperator + 3] == "NUMBR literal":
          tempVal = int(int(lexemeExpression[lastIndexOperator + 1]) + int(lexemeExpression[lastIndexOperator + 3]))
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBR literal")
        elif typeExpression[lastIndexOperator + 3] == "NUMBAR literal":
          tempVal = float(float(lexemeExpression[lastIndexOperator + 1]) + float(lexemeExpression[lastIndexOperator + 3]))
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "YARN literal":
          try:
            tempVal = int(lexemeExpression[lastIndexOperator + 1]) + int(lexemeExpression[lastIndexOperator + 3])
          except ValueError:
            try:
              tempVal = float(lexemeExpression[lastIndexOperator + 1]) + float(lexemeExpression[lastIndexOperator + 3])
            except ValueError:
              return "[Line " + str(lineNumber) + "] SemanticError: YARN literal cannot be converted to NUMBR or NUMBAR literal"
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          if(type(tempVal) == int):
            typeExpression.insert(lastIndexOperator, "NUMBR literal")
          if(type(tempVal) == float):
            typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "TROOF literal":
          if lexemeExpression[lastIndexOperator + 3] == "WIN":
            tempVal = int(int(lexemeExpression[lastIndexOperator + 1]) + 1)
          else:
            tempVal = int(int(lexemeExpression[lastIndexOperator + 1]) + 0)
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBR literal")
        else:
          return "[Line " + str(lineNumber) + "] SemanticError: NOOB literal cannot be converted to NUMBR or NUMBAR literal"
      elif typeExpression[lastIndexOperator + 1] == "NUMBAR literal":   # ! NUMBAR Literal (1st operand)
        if typeExpression[lastIndexOperator + 3] == "NUMBR literal":
          tempVal = float(float(lexemeExpression[lastIndexOperator + 1]) + float(lexemeExpression[lastIndexOperator + 3]))
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "NUMBAR literal":
          tempVal = float(float(lexemeExpression[lastIndexOperator + 1]) + float(lexemeExpression[lastIndexOperator + 3]))
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "YARN literal":
          try:
            tempVal = float(lexemeExpression[lastIndexOperator + 1]) + float(lexemeExpression[lastIndexOperator + 3])
          except ValueError:
            try:
              tempVal = float(lexemeExpression[lastIndexOperator + 1]) + float(lexemeExpression[lastIndexOperator + 3])
            except ValueError:
              return "[Line " + str(lineNumber) + "] SemanticError: YARN literal cannot be converted to NUMBR or NUMBAR literal"
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          if(type(tempVal) == int):
            typeExpression.insert(lastIndexOperator, "NUMBR literal")
          if(type(tempVal) == float):
            typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "TROOF literal":
          if lexemeExpression[lastIndexOperator + 3] == "WIN":
            tempVal = float(float(lexemeExpression[lastIndexOperator + 1]) + 1)
          else:
            tempVal = float(float(lexemeExpression[lastIndexOperator + 1]) + 0)
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        else:
          return "[Line " + str(lineNumber) + "] SemanticError: NOOB literal cannot be converted to NUMBR or NUMBAR literal"
      elif typeExpression[lastIndexOperator + 1] == "TROOF literal":         # ! TROOF LITERAL (1st operand)
        temp = 0
        if typeExpression[lastIndexOperator + 1] == "WIN":
          temp = 1

        if typeExpression[lastIndexOperator + 3] == "NUMBR literal":
          tempVal = int(temp + int(lexemeExpression[lastIndexOperator + 3]))
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBR literal")
        elif typeExpression[lastIndexOperator + 3] == "NUMBAR literal":
          tempVal = float(temp + float(lexemeExpression[lastIndexOperator + 3]))
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "YARN literal":
          try:
            tempVal = temp + int(lexemeExpression[lastIndexOperator + 3])
          except ValueError:
            try:
              tempVal = temp + float(lexemeExpression[lastIndexOperator + 3])
            except ValueError:
              return "[Line " + str(lineNumber) + "] SemanticError: YARN literal cannot be converted to NUMBR or NUMBAR literal"
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          if(type(tempVal) == int):
            typeExpression.insert(lastIndexOperator, "NUMBR literal")
          if(type(tempVal) == float):
            typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "TROOF literal":
          if lexemeExpression[lastIndexOperator + 3] == "WIN":
            tempVal = int(temp + 1)
          else:
            tempVal = int(temp + 0)
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        else:
          return "[Line " + str(lineNumber) + "] SemanticError: NOOB literal cannot be converted to NUMBR or NUMBAR literal"
      elif typeExpression[lastIndexOperator + 1] == "YARN literal":         # ! YARN LITERAL (1st operand)
        try:
          temp = int(lexemeExpression[lastIndexOperator + 1])
        except ValueError:
          try:
            temp = float(lexemeExpression[lastIndexOperator + 1])
          except ValueError:
            return "[Line " + str(lineNumber) + "] SemanticError: YARN literal cannot be converted to NUMBR or NUMBAR literal"

        if typeExpression[lastIndexOperator + 3] == "NUMBR literal":
          tempVal = temp + int(lexemeExpression[lastIndexOperator + 3])
          
          # * Popping the elements from the lexeme and type list

          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          if(type(tempVal) == int):
            typeExpression.insert(lastIndexOperator, "NUMBR literal")
          if(type(tempVal) == float):
            typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "NUMBAR literal":
          tempVal = float(temp + float(lexemeExpression[lastIndexOperator + 3]))
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "YARN literal":
          try:
            tempVal = temp + int(lexemeExpression[lastIndexOperator + 3])
          except ValueError:
            try:
              tempVal = temp + float(lexemeExpression[lastIndexOperator + 3])
            except ValueError:
              return "[Line " + str(lineNumber) + "] SemanticError: YARN literal cannot be converted to NUMBR or NUMBAR literal"
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          if(type(tempVal) == int):
            typeExpression.insert(lastIndexOperator, "NUMBR literal")
          if(type(tempVal) == float):
            typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "TROOF literal":
          if lexemeExpression[lastIndexOperator + 3] == "WIN":
            tempVal = temp + 1
          else:
            tempVal = temp + 0
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          if(type(tempVal) == int):
            typeExpression.insert(lastIndexOperator, "NUMBR literal")
          if(type(tempVal) == float):
            typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        else:
          return "[Line " + str(lineNumber) + "] SemanticError: NOOB literal cannot be converted to NUMBR or NUMBAR literal"
      else:     # ! NOOB literal (1st operand)
        return "[Line " + str(lineNumber) + "] SemanticError: NOOB literal cannot be converted to NUMBR or NUMBAR literal"
    elif lexemeExpression[lastIndexOperator] == "DIFF OF":
      if typeExpression[lastIndexOperator + 1] == "NUMBR literal":    # ! NUMBR Literal (1st operand)
        if typeExpression[lastIndexOperator + 3] == "NUMBR literal":
          tempVal = int(int(lexemeExpression[lastIndexOperator + 1]) - int(lexemeExpression[lastIndexOperator + 3]))
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBR literal")
        elif typeExpression[lastIndexOperator + 3] == "NUMBAR literal":
          tempVal = float(float(lexemeExpression[lastIndexOperator + 1]) - float(lexemeExpression[lastIndexOperator + 3]))
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "YARN literal":
          try:
            tempVal = int(lexemeExpression[lastIndexOperator + 1]) - int(lexemeExpression[lastIndexOperator + 3])
          except ValueError:
            try:
              tempVal = float(lexemeExpression[lastIndexOperator + 1]) - float(lexemeExpression[lastIndexOperator + 3])
            except ValueError:
              return "[Line " + str(lineNumber) + "] SemanticError: YARN literal cannot be converted to NUMBR or NUMBAR literal"
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          if(type(tempVal) == int):
            typeExpression.insert(lastIndexOperator, "NUMBR literal")
          if(type(tempVal) == float):
            typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "TROOF literal":
          if lexemeExpression[lastIndexOperator + 3] == "WIN":
            tempVal = int(int(lexemeExpression[lastIndexOperator + 1]) - 1)
          else:
            tempVal = int(int(lexemeExpression[lastIndexOperator + 1]) - 0)
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBR literal")
        else:
          return "[Line " + str(lineNumber) + "] SemanticError: NOOB literal cannot be converted to NUMBR or NUMBAR literal"
      elif typeExpression[lastIndexOperator + 1] == "NUMBAR literal":   # ! NUMBAR Literal (1st operand)
        if typeExpression[lastIndexOperator + 3] == "NUMBR literal":
          tempVal = float(float(lexemeExpression[lastIndexOperator + 1]) - float(lexemeExpression[lastIndexOperator + 3]))
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "NUMBAR literal":
          tempVal = float(float(lexemeExpression[lastIndexOperator + 1]) - float(lexemeExpression[lastIndexOperator + 3]))
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "YARN literal":
          try:
            tempVal = float(lexemeExpression[lastIndexOperator + 1]) - float(lexemeExpression[lastIndexOperator + 3])
          except ValueError:
            try:
              tempVal = float(lexemeExpression[lastIndexOperator + 1]) - float(lexemeExpression[lastIndexOperator + 3])
            except ValueError:
              return "[Line " + str(lineNumber) + "] SemanticError: YARN literal cannot be converted to NUMBR or NUMBAR literal"

          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          if(type(tempVal) == int):
            typeExpression.insert(lastIndexOperator, "NUMBR literal")
          if(type(tempVal) == float):
            typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "TROOF literal":
          if lexemeExpression[lastIndexOperator + 3] == "WIN":
            tempVal = float(float(lexemeExpression[lastIndexOperator + 1]) - 1)
          else:
            tempVal = float(float(lexemeExpression[lastIndexOperator + 1]) - 0)
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        else:
          return "[Line " + str(lineNumber) + "] SemanticError: NOOB literal cannot be converted to NUMBR or NUMBAR literal"
      elif typeExpression[lastIndexOperator + 1] == "TROOF literal":         # ! TROOF LITERAL (1st operand)
        temp = 0
        if typeExpression[lastIndexOperator + 1] == "WIN":
          temp = 1

        if typeExpression[lastIndexOperator + 3] == "NUMBR literal":
          tempVal = int(temp - int(lexemeExpression[lastIndexOperator + 3]))
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBR literal")
        elif typeExpression[lastIndexOperator + 3] == "NUMBAR literal":
          tempVal = float(temp - float(lexemeExpression[lastIndexOperator + 3]))
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "YARN literal":
          try:
            tempVal = temp - int(lexemeExpression[lastIndexOperator + 3])
          except ValueError:
            try:
              tempVal = temp - float(lexemeExpression[lastIndexOperator + 3])
            except ValueError:
              return "[Line " + str(lineNumber) + "] SemanticError: YARN literal cannot be converted to NUMBR or NUMBAR literal"
          
          # * Popping the elements from the lexeme and type list

          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          if(type(tempVal) == int):
            typeExpression.insert(lastIndexOperator, "NUMBR literal")
          if(type(tempVal) == float):
            typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "TROOF literal":
          if lexemeExpression[lastIndexOperator + 3] == "WIN":
            tempVal = int(temp - 1)
          else:
            tempVal = int(temp - 0)
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        else:
          return "[Line " + str(lineNumber) + "] SemanticError: NOOB literal cannot be converted to NUMBR or NUMBAR literal"
      elif typeExpression[lastIndexOperator + 1] == "YARN literal":         # ! YARN LITERAL (1st operand)
        try:
          temp = int(lexemeExpression[lastIndexOperator + 1])
        except ValueError:
          try:
            temp = float(lexemeExpression[lastIndexOperator + 1])
          except ValueError:
            return "[Line " + str(lineNumber) + "] SemanticError: YARN literal cannot be converted to NUMBR or NUMBAR literal"

        if typeExpression[lastIndexOperator + 3] == "NUMBR literal":
          tempVal = temp - int(lexemeExpression[lastIndexOperator + 3])
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          if(type(tempVal) == int):
            typeExpression.insert(lastIndexOperator, "NUMBR literal")
          if(type(tempVal) == float):
            typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "NUMBAR literal":
          tempVal = float(temp - float(lexemeExpression[lastIndexOperator + 3]))
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "YARN literal":
          try:
            tempVal = temp - int(lexemeExpression[lastIndexOperator + 3])
          except ValueError:
            try:
              tempVal = temp - float(lexemeExpression[lastIndexOperator + 3])
            except ValueError:
              return "[Line " + str(lineNumber) + "] SemanticError: YARN literal cannot be converted to NUMBR or NUMBAR literal"
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          if(type(tempVal) == int):
            typeExpression.insert(lastIndexOperator, "NUMBR literal")
          if(type(tempVal) == float):
            typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "TROOF literal":
          if lexemeExpression[lastIndexOperator + 3] == "WIN":
            tempVal = int(temp - 1)
          else:
            tempVal = int(temp - 0)
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        else:
          return "[Line " + str(lineNumber) + "] SemanticError: NOOB literal cannot be converted to NUMBR or NUMBAR literal"
      else:     # ! NOOB literal (1st operand)
        return "[Line " + str(lineNumber) + "] SemanticError: NOOB literal cannot be converted to NUMBR or NUMBAR literal"
    elif lexemeExpression[lastIndexOperator] == "PRODUKT OF":
      if typeExpression[lastIndexOperator + 1] == "NUMBR literal":    # ! NUMBR Literal (1st operand)
        if typeExpression[lastIndexOperator + 3] == "NUMBR literal":
          tempVal = int(int(lexemeExpression[lastIndexOperator + 1]) * int(lexemeExpression[lastIndexOperator + 3]))
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBR literal")
        elif typeExpression[lastIndexOperator + 3] == "NUMBAR literal":
          tempVal = float(float(lexemeExpression[lastIndexOperator + 1]) * float(lexemeExpression[lastIndexOperator + 3]))
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "YARN literal":
          try:
            tempVal = int(lexemeExpression[lastIndexOperator + 1]) * int(lexemeExpression[lastIndexOperator + 3])
          except ValueError:
            try:
              tempVal = float(lexemeExpression[lastIndexOperator + 1]) * float(lexemeExpression[lastIndexOperator + 3])
            except ValueError:
              return "[Line " + str(lineNumber) + "] SemanticError: YARN literal cannot be converted to NUMBR or NUMBAR literal"
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          if(type(tempVal) == int):
            typeExpression.insert(lastIndexOperator, "NUMBR literal")
          if(type(tempVal) == float):
            typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "TROOF literal":
          if lexemeExpression[lastIndexOperator + 3] == "WIN":
            tempVal = int(int(lexemeExpression[lastIndexOperator + 1]) * 1)
          else:
            tempVal = int(int(lexemeExpression[lastIndexOperator + 1]) * 0)
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBR literal")
        else:
          return "[Line " + str(lineNumber) + "] SemanticError: NOOB literal cannot be converted to NUMBR or NUMBAR literal"
      elif typeExpression[lastIndexOperator + 1] == "NUMBAR literal":   # ! NUMBAR Literal (1st operand)
        if typeExpression[lastIndexOperator + 3] == "NUMBR literal":
          tempVal = float(float(lexemeExpression[lastIndexOperator + 1]) * float(lexemeExpression[lastIndexOperator + 3]))
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "NUMBAR literal":
          tempVal = float(float(lexemeExpression[lastIndexOperator + 1]) * float(lexemeExpression[lastIndexOperator + 3]))
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "YARN literal":
          try:
            tempVal = float(lexemeExpression[lastIndexOperator + 1]) * float(lexemeExpression[lastIndexOperator + 3])
          except ValueError:
            try:
              tempVal = float(lexemeExpression[lastIndexOperator + 1]) * float(lexemeExpression[lastIndexOperator + 3])
            except ValueError:
              return "[Line " + str(lineNumber) + "] SemanticError: YARN literal cannot be converted to NUMBR or NUMBAR literal"
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          if(type(tempVal) == int):
            typeExpression.insert(lastIndexOperator, "NUMBR literal")
          if(type(tempVal) == float):
            typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "TROOF literal":
          if lexemeExpression[lastIndexOperator + 3] == "WIN":
            tempVal = float(float(lexemeExpression[lastIndexOperator + 1]) * 1)
          else:
            tempVal = float(float(lexemeExpression[lastIndexOperator + 1]) * 0)
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        else:
          return "[Line " + str(lineNumber) + "] SemanticError: NOOB literal cannot be converted to NUMBR or NUMBAR literal"
      elif typeExpression[lastIndexOperator + 1] == "TROOF literal":         # ! TROOF LITERAL (1st operand)
        temp = 0
        if typeExpression[lastIndexOperator + 1] == "WIN":
          temp = 1

        if typeExpression[lastIndexOperator + 3] == "NUMBR literal":
          tempVal = int(temp * int(lexemeExpression[lastIndexOperator + 3]))
        
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBR literal")
        elif typeExpression[lastIndexOperator + 3] == "NUMBAR literal":
          tempVal = float(temp * float(lexemeExpression[lastIndexOperator + 3]))
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "YARN literal":
          try:
            tempVal = temp * int(lexemeExpression[lastIndexOperator + 3])
          except ValueError:
            try:
              tempVal = temp * float(lexemeExpression[lastIndexOperator + 3])
            except ValueError:
              return "[Line " + str(lineNumber) + "] SemanticError: YARN literal cannot be converted to NUMBR or NUMBAR literal"
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          if(type(tempVal) == int):
            typeExpression.insert(lastIndexOperator, "NUMBR literal")
          if(type(tempVal) == float):
            typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "TROOF literal":
          if lexemeExpression[lastIndexOperator + 3] == "WIN":
            tempVal = int(temp * 1)
          else:
            tempVal = int(temp * 0)
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        else:
          return "[Line " + str(lineNumber) + "] SemanticError: NOOB literal cannot be converted to NUMBR or NUMBAR literal"
      elif typeExpression[lastIndexOperator + 1] == "YARN literal":         # ! YARN LITERAL (1st operand)
        try:
          temp = int(lexemeExpression[lastIndexOperator + 1])
        except ValueError:
          try:
            temp = float(lexemeExpression[lastIndexOperator + 1])
          except ValueError:
            return "[Line " + str(lineNumber) + "] SemanticError: YARN literal cannot be converted to NUMBR or NUMBAR literal"

        if typeExpression[lastIndexOperator + 3] == "NUMBR literal":
          tempVal = temp * int(lexemeExpression[lastIndexOperator + 3])
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          if(type(tempVal) == int):
            typeExpression.insert(lastIndexOperator, "NUMBR literal")
          if(type(tempVal) == float):
            typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "NUMBAR literal":
          tempVal = float(temp * float(lexemeExpression[lastIndexOperator + 3]))
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "YARN literal":
          try:
            tempVal = temp * int(lexemeExpression[lastIndexOperator + 3])
          except ValueError:
            try:
              tempVal = temp * float(lexemeExpression[lastIndexOperator + 3])
            except ValueError:
              return "[Line " + str(lineNumber) + "] SemanticError: YARN literal cannot be converted to NUMBR or NUMBAR literal"
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          if(type(tempVal) == int):
            typeExpression.insert(lastIndexOperator, "NUMBR literal")
          if(type(tempVal) == float):
            typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "TROOF literal":
          if lexemeExpression[lastIndexOperator + 3] == "WIN":
            tempVal = temp * 1
          else:
            tempVal = temp * 0
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          if(type(tempVal) == int):
            typeExpression.insert(lastIndexOperator, "NUMBR literal")
          if(type(tempVal) == float):
            typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        else:
          return "[Line " + str(lineNumber) + "] SemanticError: NOOB literal cannot be converted to NUMBR or NUMBAR literal"
      else:     # ! NOOB literal (2st operand)
        return "[Line " + str(lineNumber) + "] SemanticError: NOOB literal cannot be converted to NUMBR or NUMBAR literal"
    elif lexemeExpression[lastIndexOperator] == "QUOSHUNT OF":
      if typeExpression[lastIndexOperator + 1] == "NUMBR literal":    # ! NUMBR Literal (1st operand)
        if typeExpression[lastIndexOperator + 3] == "NUMBR literal":
          if lexemeExpression[lastIndexOperator + 3] == "0":
            return "[Line " + str(lineNumber) + "] SemanticError: Division by zero" 
          tempVal = int(lexemeExpression[lastIndexOperator + 1]) / int(lexemeExpression[lastIndexOperator + 3])
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          if(type(tempVal) == int):
            typeExpression.insert(lastIndexOperator, "NUMBR literal")
          if(type(tempVal) == float):
            typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "NUMBAR literal":
          if lexemeExpression[lastIndexOperator + 3] == "0.0":
            return "[Line " + str(lineNumber) + "] SemanticError: Division by zero" 
          tempVal = float(float(lexemeExpression[lastIndexOperator + 1]) / float(lexemeExpression[lastIndexOperator + 3]))
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "YARN literal":
          if lexemeExpression[lastIndexOperator + 3] == "0" or lexemeExpression[lastIndexOperator + 3] == "0.0":
            return "[Line " + str(lineNumber) + "] SemanticError: Division by zero" 
          try:
            tempVal = int(lexemeExpression[lastIndexOperator + 1]) / int(lexemeExpression[lastIndexOperator + 3])
          except ValueError:
            try:
              tempVal = float(float(lexemeExpression[lastIndexOperator + 1]) / float(lexemeExpression[lastIndexOperator + 3]))
            except ValueError:
              return "[Line " + str(lineNumber) + "] SemanticError: YARN literal cannot be converted to NUMBR or NUMBAR literal"
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          if(type(tempVal) == int):
            typeExpression.insert(lastIndexOperator, "NUMBR literal")
          if(type(tempVal) == float):
            typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "TROOF literal":
          if lexemeExpression[lastIndexOperator + 3] == "WIN":
            tempVal = int(int(lexemeExpression[lastIndexOperator + 1]) / 1)
          else:
            return "[Line " + str(lineNumber) + "] SemanticError: Division by zero"
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBR literal")
        else:
          return "[Line " + str(lineNumber) + "] SemanticError: NOOB literal cannot be converted to NUMBR or NUMBAR literal"
      elif typeExpression[lastIndexOperator + 1] == "NUMBAR literal":   # ! NUMBAR Literal (1st operand)
        if typeExpression[lastIndexOperator + 3] == "NUMBR literal":
          if lexemeExpression[lastIndexOperator + 3] == "0":
            return "[Line " + str(lineNumber) + "] SemanticError: Division by zero" 
          tempVal = float(float(lexemeExpression[lastIndexOperator + 1]) / float(lexemeExpression[lastIndexOperator + 3]))
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "NUMBAR literal":
          if lexemeExpression[lastIndexOperator + 3] == "0" or lexemeExpression[lastIndexOperator + 3] == "0.0":
            return "[Line " + str(lineNumber) + "] SemanticError: Division by zero" 
          tempVal = float(float(lexemeExpression[lastIndexOperator + 1]) / float(lexemeExpression[lastIndexOperator + 3]))
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "YARN literal":
          if lexemeExpression[lastIndexOperator + 3] == "0" or lexemeExpression[lastIndexOperator + 3] == "0.0":
            return "[Line " + str(lineNumber) + "] SemanticError: Division by zero" 
          try:
            tempVal = float(lexemeExpression[lastIndexOperator + 1]) / float(lexemeExpression[lastIndexOperator + 3])
          except ValueError:
            try:
              tempVal = float(lexemeExpression[lastIndexOperator + 1]) / float(lexemeExpression[lastIndexOperator + 3])
            except ValueError:
              return "[Line " + str(lineNumber) + "] SemanticError: YARN literal cannot be converted to NUMBR or NUMBAR literal"
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          if(type(tempVal) == int):
            typeExpression.insert(lastIndexOperator, "NUMBR literal")
          if(type(tempVal) == float):
            typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "TROOF literal":
          if lexemeExpression[lastIndexOperator + 3] == "WIN":
            tempVal = float(float(lexemeExpression[lastIndexOperator + 1]) / 1)
          else:
            return "[Line " + str(lineNumber) + "] SemanticError: Division by zero" 
        
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        else:
          return "[Line " + str(lineNumber) + "] SemanticError: NOOB literal cannot be converted to NUMBR or NUMBAR literal"
      elif typeExpression[lastIndexOperator + 1] == "TROOF literal":         # ! TROOF LITERAL (1st operand)
        temp = 0
        if typeExpression[lastIndexOperator + 1] == "WIN":
          temp = 1

        if typeExpression[lastIndexOperator + 3] == "NUMBR literal":
          if lexemeExpression[lastIndexOperator + 3] == "0":
            return "[Line " + str(lineNumber) + "] SemanticError: Division by zero" 
          tempVal = temp / int(lexemeExpression[lastIndexOperator + 3])
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          if(type(tempVal) == int):
            typeExpression.insert(lastIndexOperator, "NUMBR literal")
          if(type(tempVal) == float):
            typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "NUMBAR literal":
          if lexemeExpression[lastIndexOperator + 3] == "0" or lexemeExpression[lastIndexOperator + 3] == "0.0":
            return "[Line " + str(lineNumber) + "] SemanticError: Division by zero" 
          tempVal = float(temp * float(lexemeExpression[lastIndexOperator + 3]))
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "YARN literal":
          if lexemeExpression[lastIndexOperator + 3] == "0" or lexemeExpression[lastIndexOperator + 3] == "0.0":
            return "[Line " + str(lineNumber) + "] SemanticError: Division by zero" 
          try:
            tempVal = temp / int(lexemeExpression[lastIndexOperator + 3])
          except ValueError:
            try:
              tempVal = temp / float(lexemeExpression[lastIndexOperator + 3])
            except ValueError:
              return "[Line " + str(lineNumber) + "] SemanticError: YARN literal cannot be converted to NUMBR or NUMBAR literal"
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          if(type(tempVal) == int):
            typeExpression.insert(lastIndexOperator, "NUMBR literal")
          if(type(tempVal) == float):
            typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "TROOF literal":
          if lexemeExpression[lastIndexOperator + 3] == "WIN":
            tempVal = temp / 1
          else:
            return "[Line " + str(lineNumber) + "] SemanticError: Division by zero" 

          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          if(type(tempVal) == int):
            typeExpression.insert(lastIndexOperator, "NUMBR literal")
          if(type(tempVal) == float):
            typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        else:
          return "[Line " + str(lineNumber) + "] SemanticError: NOOB literal cannot be converted to NUMBR or NUMBAR literal"
      elif typeExpression[lastIndexOperator + 1] == "YARN literal":         # ! YARN LITERAL (1st operand)
        try:
          temp = int(lexemeExpression[lastIndexOperator + 1])
        except ValueError:
          try:
            temp = float(lexemeExpression[lastIndexOperator + 1])
          except ValueError:
            return "[Line " + str(lineNumber) + "] SemanticError: YARN literal cannot be converted to NUMBR or NUMBAR literal"

        if typeExpression[lastIndexOperator + 3] == "NUMBR literal":
          tempVal = temp / int(lexemeExpression[lastIndexOperator + 3])
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          if(type(tempVal) == int):
            typeExpression.insert(lastIndexOperator, "NUMBR literal")
          if(type(tempVal) == float):
            typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "NUMBAR literal":
          tempVal = float(temp / float(lexemeExpression[lastIndexOperator + 3]))
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "YARN literal":
          try:
            if int(lexemeExpression[lastIndexOperator + 3]) == 0:
              return "[Line " + str(lineNumber) + "] SemanticError: Division by zero"
            tempVal = temp / int(lexemeExpression[lastIndexOperator + 3])
          except ValueError:
            try:
              tempVal = float(temp / float(lexemeExpression[lastIndexOperator + 3]))
            except ValueError:
              return "[Line " + str(lineNumber) + "] SemanticError: YARN literal cannot be converted to NUMBR or NUMBAR literal"
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          if(type(tempVal) == int):
            typeExpression.insert(lastIndexOperator, "NUMBR literal")
          if(type(tempVal) == float):
            typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "TROOF literal":
          if lexemeExpression[lastIndexOperator + 3] == "WIN":
            tempVal = temp / 1
          else:
            return(f"[Line {lineNumber}] SemanticError: Divison by zero")
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          if(type(tempVal) == int):
            typeExpression.insert(lastIndexOperator, "NUMBR literal")
          if(type(tempVal) == float):
            typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        else:
          return "[Line " + str(lineNumber) + "] SemanticError: NOOB literal cannot be converted to NUMBR or NUMBAR literal"
      else:     # ! NOOB literal (2st operand)
        return "[Line " + str(lineNumber) + "] SemanticError: NOOB literal cannot be converted to NUMBR or NUMBAR literal"
    elif lexemeExpression[lastIndexOperator] == "MOD OF":
      if typeExpression[lastIndexOperator + 1] == "NUMBR literal":    # ! NUMBR Literal (1st operand)
        if typeExpression[lastIndexOperator + 3] == "NUMBR literal":
          if lexemeExpression[lastIndexOperator + 3] == "0" or lexemeExpression[lastIndexOperator + 3] == "0.0":
            return "[Line " + str(lineNumber) + "] SemanticError: Division by zero" 
          tempVal = int(int(lexemeExpression[lastIndexOperator + 1]) % int(lexemeExpression[lastIndexOperator + 3]))
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBR literal")
        elif typeExpression[lastIndexOperator + 3] == "NUMBAR literal":
          if lexemeExpression[lastIndexOperator + 3] == "0" or lexemeExpression[lastIndexOperator + 3] == "0.0":
            return "[Line " + str(lineNumber) + "] SemanticError: Division by zero" 
          tempVal = float(float(lexemeExpression[lastIndexOperator + 1]) % float(lexemeExpression[lastIndexOperator + 3]))

          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "YARN literal":
          if lexemeExpression[lastIndexOperator + 3] == "0" or lexemeExpression[lastIndexOperator + 3] == "0.0":
            return "[Line " + str(lineNumber) + "] SemanticError: Division by zero" 
          try:
            tempVal = int(lexemeExpression[lastIndexOperator + 1]) % int(lexemeExpression[lastIndexOperator + 3])
          except ValueError:
            try:
              tempVal = float(lexemeExpression[lastIndexOperator + 1]) % float(lexemeExpression[lastIndexOperator + 3])
            except ValueError:
              return "[Line " + str(lineNumber) + "] SemanticError: YARN literal cannot be converted to NUMBR or NUMBAR literal"
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          if(type(tempVal) == int):
            typeExpression.insert(lastIndexOperator, "NUMBR literal")
          if(type(tempVal) == float):
            typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "TROOF literal":
          if lexemeExpression[lastIndexOperator + 3] == "WIN":
            tempVal = int(int(lexemeExpression[lastIndexOperator + 1]) % 1)
          else:
            return "[Line " + str(lineNumber) + "] SemanticError: Division by zero" 
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBR literal")
        else:
          return "[Line " + str(lineNumber) + "] SemanticError: NOOB literal cannot be converted to NUMBR or NUMBAR literal"
      elif typeExpression[lastIndexOperator + 1] == "NUMBAR literal":   # ! NUMBAR Literal (1st operand)
        if typeExpression[lastIndexOperator + 3] == "NUMBR literal":
          if lexemeExpression[lastIndexOperator + 3] == "0" or lexemeExpression[lastIndexOperator + 3] == "0.0":
            return "[Line " + str(lineNumber) + "] SemanticError: Division by zero" 
          tempVal = float(float(lexemeExpression[lastIndexOperator + 1]) % float(lexemeExpression[lastIndexOperator + 3]))
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "NUMBAR literal":
          if lexemeExpression[lastIndexOperator + 3] == "0" or lexemeExpression[lastIndexOperator + 3] == "0.0":
            return "[Line " + str(lineNumber) + "] SemanticError: Division by zero" 
          tempVal = float(float(lexemeExpression[lastIndexOperator + 1]) % float(lexemeExpression[lastIndexOperator + 3]))
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "YARN literal":
          if lexemeExpression[lastIndexOperator + 3] == "0" or lexemeExpression[lastIndexOperator + 3] == "0.0":
            return "[Line " + str(lineNumber) + "] SemanticError: Division by zero" 
          try:
            tempVal = float(lexemeExpression[lastIndexOperator + 1]) % float(lexemeExpression[lastIndexOperator + 3])
          except ValueError:
            try:
              tempVal = float(lexemeExpression[lastIndexOperator + 1]) % float(lexemeExpression[lastIndexOperator + 3])
            except ValueError:
              return "[Line " + str(lineNumber) + "] SemanticError: YARN literal cannot be converted to NUMBR or NUMBAR literal"
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          if(type(tempVal) == int):
            typeExpression.insert(lastIndexOperator, "NUMBR literal")
          if(type(tempVal) == float):
            typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "TROOF literal":
          if lexemeExpression[lastIndexOperator + 3] == "WIN":
            tempVal = float(float(lexemeExpression[lastIndexOperator + 1]) % 1)
          else:
            return "[Line " + str(lineNumber) + "] SemanticError: Division by zero" 
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        else:
          return "[Line " + str(lineNumber) + "] SemanticError: NOOB literal cannot be converted to NUMBR or NUMBAR literal"
      elif typeExpression[lastIndexOperator + 1] == "TROOF literal":         # ! TROOF LITERAL (1st operand)
        temp = 0
        if typeExpression[lastIndexOperator + 1] == "WIN":
          temp = 1

        if typeExpression[lastIndexOperator + 3] == "NUMBR literal":
          if lexemeExpression[lastIndexOperator + 3] == "0" or lexemeExpression[lastIndexOperator + 3] == "0.0":
            return "[Line " + str(lineNumber) + "] SemanticError: Division by zero" 
          tempVal = int(temp % int(lexemeExpression[lastIndexOperator + 3]))
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBR literal")
        elif typeExpression[lastIndexOperator + 3] == "NUMBAR literal":
          if lexemeExpression[lastIndexOperator + 3] == "0" or lexemeExpression[lastIndexOperator + 3] == "0.0":
            return "[Line " + str(lineNumber) + "] SemanticError: Division by zero" 
          tempVal = float(temp % float(lexemeExpression[lastIndexOperator + 3]))
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "YARN literal":
          if lexemeExpression[lastIndexOperator + 3] == "0" or lexemeExpression[lastIndexOperator + 3] == "0.0":
            return "[Line " + str(lineNumber) + "] SemanticError: Division by zero" 
          try:
            tempVal = int(temp % int(lexemeExpression[lastIndexOperator + 3]))
          except ValueError:
            try:
              tempVal = float(temp % float(lexemeExpression[lastIndexOperator + 3]))
            except ValueError:
              return "[Line " + str(lineNumber) + "] SemanticError: YARN literal cannot be converted to NUMBR or NUMBAR literal"
          
          # * Popping the elements from the lexeme and type list

          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          if(type(tempVal) == int):
            typeExpression.insert(lastIndexOperator, "NUMBR literal")
          if(type(tempVal) == float):
            typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "TROOF literal":
          if lexemeExpression[lastIndexOperator + 3] == "WIN":
            tempVal = temp % 1
          else:
            return "[Line " + str(lineNumber) + "] SemanticError: Division by zero" 
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          if(type(tempVal) == int):
            typeExpression.insert(lastIndexOperator, "NUMBR literal")
          if(type(tempVal) == float):
            typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        else:
          return "[Line " + str(lineNumber) + "] SemanticError: NOOB literal cannot be converted to NUMBR or NUMBAR literal"
      elif typeExpression[lastIndexOperator + 1] == "YARN literal":         # ! YARN LITERAL (1st operand)
        try:
          temp = int(lexemeExpression[lastIndexOperator + 1])
        except ValueError:
          try:
            temp = float(lexemeExpression[lastIndexOperator + 1])
          except ValueError:
            return "[Line " + str(lineNumber) + "] SemanticError: YARN literal cannot be converted to NUMBR or NUMBAR literal"

        if typeExpression[lastIndexOperator + 3] == "NUMBR literal":
          if lexemeExpression[lastIndexOperator + 3] == "0" or lexemeExpression[lastIndexOperator + 3] == "0.0":
            return "[Line " + str(lineNumber) + "] SemanticError: Division by zero" 
          tempVal = temp % int(lexemeExpression[lastIndexOperator + 3])
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          if(type(tempVal) == int):
            typeExpression.insert(lastIndexOperator, "NUMBR literal")
          if(type(tempVal) == float):
            typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "NUMBAR literal":
          if lexemeExpression[lastIndexOperator + 3] == "0" or lexemeExpression[lastIndexOperator + 3] == "0.0":
            return "[Line " + str(lineNumber) + "] SemanticError: Division by zero" 
          tempVal = temp % float(lexemeExpression[lastIndexOperator + 3])
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          if(type(tempVal) == int):
            typeExpression.insert(lastIndexOperator, "NUMBR literal")
          if(type(tempVal) == float):
            typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "YARN literal":
          if lexemeExpression[lastIndexOperator + 3] == "0" or lexemeExpression[lastIndexOperator + 3] == "0.0":
            return "[Line " + str(lineNumber) + "] SemanticError: Division by zero" 
          try:
            tempVal = temp % int(lexemeExpression[lastIndexOperator + 3])
          except ValueError:
            try:
              tempVal = temp % float(lexemeExpression[lastIndexOperator + 3])
            except ValueError:
              return "[Line " + str(lineNumber) + "] SemanticError: YARN literal cannot be converted to NUMBR or NUMBAR literal"
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          if(type(tempVal) == int):
            typeExpression.insert(lastIndexOperator, "NUMBR literal")
          if(type(tempVal) == float):
            typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "TROOF literal":
          if lexemeExpression[lastIndexOperator + 3] == "WIN":
            tempVal = temp % 1
          else:
            return "[Line " + str(lineNumber) + "] SemanticError: Division by zero" 
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          if(type(tempVal) == int):
            typeExpression.insert(lastIndexOperator, "NUMBR literal")
          if(type(tempVal) == float):
            typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        else:
          return "[Line " + str(lineNumber) + "] SemanticError: NOOB literal cannot be converted to NUMBR or NUMBAR literal"
      else:     # ! NOOB literal (1st operand)
        return "[Line " + str(lineNumber) + "] SemanticError: NOOB literal cannot be converted to NUMBR or NUMBAR literal"
    elif lexemeExpression[lastIndexOperator] == "BIGGR OF":
      if typeExpression[lastIndexOperator + 1] == "NUMBR literal":    # ! NUMBR Literal (1st operand)
        if typeExpression[lastIndexOperator + 3] == "NUMBR literal":
          tempVal = max(int(lexemeExpression[lastIndexOperator + 1]),int(lexemeExpression[lastIndexOperator + 3]))
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          if(type(tempVal) == int):
            typeExpression.insert(lastIndexOperator, "NUMBR literal")
          if(type(tempVal) == float):
            typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "NUMBAR literal":
          tempVal = max(float(lexemeExpression[lastIndexOperator + 1]), float(lexemeExpression[lastIndexOperator + 3]))
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          if(type(tempVal) == int):
            typeExpression.insert(lastIndexOperator, "NUMBR literal")
          if(type(tempVal) == float):
            typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "YARN literal":
          try:
            tempVal = max(int(lexemeExpression[lastIndexOperator + 1]), int(lexemeExpression[lastIndexOperator + 3]))
          except ValueError:
            try:
              tempVal = max(float(lexemeExpression[lastIndexOperator + 1]), float(lexemeExpression[lastIndexOperator + 3]))
            except ValueError:
              return "[Line " + str(lineNumber) + "] SemanticError: YARN literal cannot be converted to NUMBR or NUMBAR literal"
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          if(type(tempVal) == int):
            typeExpression.insert(lastIndexOperator, "NUMBR literal")
          if(type(tempVal) == float):
            typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "TROOF literal":
          if lexemeExpression[lastIndexOperator + 3] == "WIN":
            tempVal = max(lexemeExpression[lastIndexOperator + 1], 1)
          else:
            tempVal = max(lexemeExpression[lastIndexOperator + 1], 0)
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          if(type(tempVal) == int):
            typeExpression.insert(lastIndexOperator, "NUMBR literal")
          if(type(tempVal) == float):
            typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        else:
          return "[Line " + str(lineNumber) + "] SemanticError: NOOB literal cannot be converted to NUMBR or NUMBAR literal"
      elif typeExpression[lastIndexOperator + 1] == "NUMBAR literal":   # ! NUMBAR Literal (1st operand)
        if typeExpression[lastIndexOperator + 3] == "NUMBR literal":
          tempVal = max(float(lexemeExpression[lastIndexOperator + 1]), float(lexemeExpression[lastIndexOperator + 3]))
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          if(type(tempVal) == int):
            typeExpression.insert(lastIndexOperator, "NUMBR literal")
          if(type(tempVal) == float):
            typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "NUMBAR literal":
          tempVal = max(float(lexemeExpression[lastIndexOperator + 1]), float(lexemeExpression[lastIndexOperator + 3]))
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          if(type(tempVal) == int):
            typeExpression.insert(lastIndexOperator, "NUMBR literal")
          if(type(tempVal) == float):
            typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "YARN literal":
          try:
            tempVal = max(float(lexemeExpression[lastIndexOperator + 1]), float(lexemeExpression[lastIndexOperator + 3]))
          except ValueError:
            try:
              tempVal = max(float(lexemeExpression[lastIndexOperator + 1]), float(lexemeExpression[lastIndexOperator + 3]))
            except ValueError:
              return "[Line " + str(lineNumber) + "] SemanticError: YARN literal cannot be converted to NUMBR or NUMBAR literal"

          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          if(type(tempVal) == int):
            typeExpression.insert(lastIndexOperator, "NUMBR literal")
          if(type(tempVal) == float):
            typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "TROOF literal":
          if lexemeExpression[lastIndexOperator + 3] == "WIN":
            tempVal = max(float(lexemeExpression[lastIndexOperator + 1]), 1)
          else:
            tempVal = max(float(lexemeExpression[lastIndexOperator + 1]), 0)
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          if(type(tempVal) == int):
            typeExpression.insert(lastIndexOperator, "NUMBR literal")
          if(type(tempVal) == float):
            typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        else:
          return "[Line " + str(lineNumber) + "] SemanticError: NOOB literal cannot be converted to NUMBR or NUMBAR literal"
      elif typeExpression[lastIndexOperator + 1] == "TROOF literal":         # ! TROOF LITERAL (1st operand)
        temp = 0
        if typeExpression[lastIndexOperator + 1] == "WIN":
          temp = 1

        if typeExpression[lastIndexOperator + 3] == "NUMBR literal":
          tempVal = max(temp, int(lexemeExpression[lastIndexOperator + 3]))
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          if(type(tempVal) == int):
            typeExpression.insert(lastIndexOperator, "NUMBR literal")
          if(type(tempVal) == float):
            typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "NUMBAR literal":
          tempVal = max(temp, float(lexemeExpression[lastIndexOperator + 3]))
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          if(type(tempVal) == int):
            typeExpression.insert(lastIndexOperator, "NUMBR literal")
          if(type(tempVal) == float):
            typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "YARN literal":
          try:
            tempVal = max(temp, int(lexemeExpression[lastIndexOperator + 3]))
          except ValueError:
            try:
              tempVal = max(temp, float(lexemeExpression[lastIndexOperator + 3]))
            except ValueError:
              return "[Line " + str(lineNumber) + "] SemanticError: YARN literal cannot be converted to NUMBR or NUMBAR literal"
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          if(type(tempVal) == int):
            typeExpression.insert(lastIndexOperator, "NUMBR literal")
          if(type(tempVal) == float):
            typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "TROOF literal":
          if lexemeExpression[lastIndexOperator + 3] == "WIN":
            tempVal = max(temp, 1)
          else:
            tempVal = max(temp, 0)

          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          if(type(tempVal) == int):
            typeExpression.insert(lastIndexOperator, "NUMBR literal")
          if(type(tempVal) == float):
            typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        else:
          return "[Line " + str(lineNumber) + "] SemanticError: NOOB literal cannot be converted to NUMBR or NUMBAR literal"
      elif typeExpression[lastIndexOperator + 1] == "YARN literal":         # ! YARN LITERAL (1st operand)
        try:
          temp = int(lexemeExpression[lastIndexOperator + 1])
        except ValueError:
          try:
            temp = float(lexemeExpression[lastIndexOperator + 1])
          except ValueError:
            return "[Line " + str(lineNumber) + "] SemanticError: YARN literal cannot be converted to NUMBR or NUMBAR literal"

        if typeExpression[lastIndexOperator + 3] == "NUMBR literal":
          tempVal = max(temp, int(lexemeExpression[lastIndexOperator + 3]))
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          if(type(tempVal) == int):
            typeExpression.insert(lastIndexOperator, "NUMBR literal")
          if(type(tempVal) == float):
            typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "NUMBAR literal":
          tempVal = max(temp, float(lexemeExpression[lastIndexOperator + 3]))
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          if(type(tempVal) == int):
            typeExpression.insert(lastIndexOperator, "NUMBR literal")
          if(type(tempVal) == float):
            typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "YARN literal":
          try:
            tempVal = max(temp, int(lexemeExpression[lastIndexOperator + 3]))
          except ValueError:
            try:
              tempVal = max(temp, float(lexemeExpression[lastIndexOperator + 3]))
            except ValueError:
              return "[Line " + str(lineNumber) + "] SemanticError: YARN literal cannot be converted to NUMBR or NUMBAR literal"
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          if(type(tempVal) == int):
            typeExpression.insert(lastIndexOperator, "NUMBR literal")
          if(type(tempVal) == float):
            typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "TROOF literal":
          if lexemeExpression[lastIndexOperator + 3] == "WIN":
            tempVal = max(temp, 1)
          else:
            tempVal = max(temp, 0)
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          if(type(tempVal) == int):
            typeExpression.insert(lastIndexOperator, "NUMBR literal")
          if(type(tempVal) == float):
            typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        else:
          return "[Line " + str(lineNumber) + "] SemanticError: NOOB literal cannot be converted to NUMBR or NUMBAR literal"
      else:     # ! NOOB literal (1st operand)
        return "[Line " + str(lineNumber) + "] SemanticError: NOOB literal cannot be converted to NUMBR or NUMBAR literal"
    elif lexemeExpression[lastIndexOperator] == "SMALLR OF":
      if typeExpression[lastIndexOperator + 1] == "NUMBR literal":    # ! NUMBR Literal (1st operand)
        if typeExpression[lastIndexOperator + 3] == "NUMBR literal":
          tempVal = min(int(lexemeExpression[lastIndexOperator + 1]),int(lexemeExpression[lastIndexOperator + 3]))
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          if(type(tempVal) == int):
            typeExpression.insert(lastIndexOperator, "NUMBR literal")
          if(type(tempVal) == float):
            typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "NUMBAR literal":
          tempVal = min(float(lexemeExpression[lastIndexOperator + 1]), float(lexemeExpression[lastIndexOperator + 3]))
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          if(type(tempVal) == int):
            typeExpression.insert(lastIndexOperator, "NUMBR literal")
          if(type(tempVal) == float):
            typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "YARN literal":
          try:
            tempVal = min(int(lexemeExpression[lastIndexOperator + 1]), int(lexemeExpression[lastIndexOperator + 3]))
          except ValueError:
            try:
              tempVal = min(float(lexemeExpression[lastIndexOperator + 1]), float(lexemeExpression[lastIndexOperator + 3]))
            except ValueError:
              return "[Line " + str(lineNumber) + "] SemanticError: YARN literal cannot be converted to NUMBR or NUMBAR literal"
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          if(type(tempVal) == int):
            typeExpression.insert(lastIndexOperator, "NUMBR literal")
          if(type(tempVal) == float):
            typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "TROOF literal":
          if lexemeExpression[lastIndexOperator + 3] == "WIN":
            tempVal = min(lexemeExpression[lastIndexOperator + 1], 1)
          else:
            tempVal = min(lexemeExpression[lastIndexOperator + 1], 0)
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          if(type(tempVal) == int):
            typeExpression.insert(lastIndexOperator, "NUMBR literal")
          if(type(tempVal) == float):
            typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        else:
          return "[Line " + str(lineNumber) + "] SemanticError: NOOB literal cannot be converted to NUMBR or NUMBAR literal"
      elif typeExpression[lastIndexOperator + 1] == "NUMBAR literal":   # ! NUMBAR Literal (1st operand)
        if typeExpression[lastIndexOperator + 3] == "NUMBR literal":
          tempVal = min(float(lexemeExpression[lastIndexOperator + 1]), float(lexemeExpression[lastIndexOperator + 3]))
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          if(type(tempVal) == int):
            typeExpression.insert(lastIndexOperator, "NUMBR literal")
          if(type(tempVal) == float):
            typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "NUMBAR literal":
          tempVal = max(float(lexemeExpression[lastIndexOperator + 1]), float(lexemeExpression[lastIndexOperator + 3]))
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          if(type(tempVal) == int):
            typeExpression.insert(lastIndexOperator, "NUMBR literal")
          if(type(tempVal) == float):
            typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "YARN literal":
          try:
            tempVal = max(float(lexemeExpression[lastIndexOperator + 1]), float(lexemeExpression[lastIndexOperator + 3]))
          except ValueError:
            try:
              tempVal = max(float(lexemeExpression[lastIndexOperator + 1]), float(lexemeExpression[lastIndexOperator + 3]))
            except ValueError:
              return "[Line " + str(lineNumber) + "] SemanticError: YARN literal cannot be converted to NUMBR or NUMBAR literal"
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          if(type(tempVal) == int):
            typeExpression.insert(lastIndexOperator, "NUMBR literal")
          if(type(tempVal) == float):
            typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "TROOF literal":
          if lexemeExpression[lastIndexOperator + 3] == "WIN":
            tempVal = max(float(lexemeExpression[lastIndexOperator + 1]), 1)
          else:
            tempVal = max(float(lexemeExpression[lastIndexOperator + 1]), 0)
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          if(type(tempVal) == int):
            typeExpression.insert(lastIndexOperator, "NUMBR literal")
          if(type(tempVal) == float):
            typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        else:
          return "[Line " + str(lineNumber) + "] SemanticError: NOOB literal cannot be converted to NUMBR or NUMBAR literal"
      elif typeExpression[lastIndexOperator + 1] == "TROOF literal":         # ! TROOF LITERAL (1st operand)
        temp = 0
        if typeExpression[lastIndexOperator + 1] == "WIN":
          temp = 1

        if typeExpression[lastIndexOperator + 3] == "NUMBR literal":
          tempVal = min(temp, int(lexemeExpression[lastIndexOperator + 3]))
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          if(type(tempVal) == int):
            typeExpression.insert(lastIndexOperator, "NUMBR literal")
          if(type(tempVal) == float):
            typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "NUMBAR literal":
          tempVal = min(temp, float(lexemeExpression[lastIndexOperator + 3]))
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          if(type(tempVal) == int):
            typeExpression.insert(lastIndexOperator, "NUMBR literal")
          if(type(tempVal) == float):
            typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "YARN literal":
          try:
            tempVal = min(temp, int(lexemeExpression[lastIndexOperator + 3]))
          except ValueError:
            try:
              tempVal = min(temp, float(lexemeExpression[lastIndexOperator + 3]))
            except ValueError:
              return "[Line " + str(lineNumber) + "] SemanticError: YARN literal cannot be converted to NUMBR or NUMBAR literal"
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          if(type(tempVal) == int):
            typeExpression.insert(lastIndexOperator, "NUMBR literal")
          if(type(tempVal) == float):
            typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "TROOF literal":
          if lexemeExpression[lastIndexOperator + 3] == "WIN":
            tempVal = min(temp, 1)
          else:
            tempVal = min(temp, 0)
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          if(type(tempVal) == int):
            typeExpression.insert(lastIndexOperator, "NUMBR literal")
          if(type(tempVal) == float):
            typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        else:
          return "[Line " + str(lineNumber) + "] SemanticError: NOOB literal cannot be converted to NUMBR or NUMBAR literal"
      elif typeExpression[lastIndexOperator + 1] == "YARN literal":         # ! YARN LITERAL (1st operand)
        try:
          temp = int(lexemeExpression[lastIndexOperator + 1])
        except ValueError:
          try:
            temp = float(lexemeExpression[lastIndexOperator + 1])
          except ValueError:
            return "[Line " + str(lineNumber) + "] SemanticError: YARN literal cannot be converted to NUMBR or NUMBAR literal"

        if typeExpression[lastIndexOperator + 3] == "NUMBR literal":
          tempVal = min(temp, int(lexemeExpression[lastIndexOperator + 3]))
          
          # * Popping the elements from the lexeme and type list

          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          if(type(tempVal) == int):
            typeExpression.insert(lastIndexOperator, "NUMBR literal")
          if(type(tempVal) == float):
            typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "NUMBAR literal":
          tempVal = min(temp, float(lexemeExpression[lastIndexOperator + 3]))
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          if(type(tempVal) == int):
            typeExpression.insert(lastIndexOperator, "NUMBR literal")
          if(type(tempVal) == float):
            typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "YARN literal":
          try:
            tempVal = min(temp, int(lexemeExpression[lastIndexOperator + 3]))
          except ValueError:
            try:
              tempVal = max(temp, float(lexemeExpression[lastIndexOperator + 3]))
            except ValueError:
              return "[Line " + str(lineNumber) + "] SemanticError: YARN literal cannot be converted to NUMBR or NUMBAR literal"
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          if(type(tempVal) == int):
            typeExpression.insert(lastIndexOperator, "NUMBR literal")
          if(type(tempVal) == float):
            typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "TROOF literal":
          if lexemeExpression[lastIndexOperator + 3] == "WIN":
            tempVal = min(temp, 1)
          else:
            tempVal = min(temp, 0)
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          if(type(tempVal) == int):
            typeExpression.insert(lastIndexOperator, "NUMBR literal")
          if(type(tempVal) == float):
            typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        else:
          return "[Line " + str(lineNumber) + "] SemanticError: NOOB literal cannot be converted to NUMBR or NUMBAR literal"
      else:     # ! NOOB literal (1st operand)
        return "[Line " + str(lineNumber) + "] SemanticError: NOOB literal cannot be converted to NUMBR or NUMBAR literal"

  if typeExpression[0] == "NUMBR literal":
    tempVal = [int(lexemeExpression[0]), typeExpression[0]]
  else:
    tempVal = [float(lexemeExpression[0]), typeExpression[0]]
    
  return tempVal

def booleanExpSemantics(lineNumber, symbolTable, lexemes, types):
  # * Gets the index of ITZ
  if("variable initialization keyword" in types[lineNumber]):
    expressionIndex = lexemes[lineNumber].index("ITZ")
  #put other cases where the arithmetic expression might be
  elif("print keyword" in types[lineNumber]):
    expressionIndex = lexemes[lineNumber].index("VISIBLE")
    
    if types[lineNumber][expressionIndex + 1] not in expressionKeywords["boolean"]:
      operationIndices = []
      # Find the first operation to appear in string
      for index in range(len(lexemes[lineNumber])):
        if lexemes[lineNumber][index] in expressionKeywords["boolean"]:
          operationIndices.append(index)
      
      expressionIndex = operationIndices[0] - 1
  else:
    expressionIndex = -1 
  
  if lexemes[lineNumber].count("ANY OF") > 1:
    return "[Line " + str(lineNumber) + "] SyntaxError: ANY OF cannot be nested"
  
  if lexemes[lineNumber].count("ANY OF") == 1:
    if lexemes[lineNumber].count("MKAY") > 1:
      return "[Line " + str(lineNumber) + "] SyntaxError: Have too many ANY OF delimiter MKAY "
    
    try:
      x = lexemes[lineNumber].index("MKAY")
      try:
        if lexemes[lineNumber][x + 1]:
          return "[Line " + str(lineNumber) + "] SyntaxError: No statements allowed after ALL OF or ANY OF delimiter"
      except IndexError:
        print("", end="")
    except ValueError:
        return "[Line " + str(lineNumber) + "] SyntaxError: Missing ANY OF delimiter"
    
  if lexemes[lineNumber].count("ALL OF") > 1:
    return "[Line " + str(lineNumber) + "] SyntaxError: ANY OF cannot be nested"
  if lexemes[lineNumber].count("ALL OF") == 1:
    if lexemes[lineNumber].count("MKAY") > 1:
      return "[Line " + str(lineNumber) + "] SyntaxError: Have too many ANY OF delimiter MKAY "
    
    try:
      x = lexemes[lineNumber].index("MKAY")
      try:
        if lexemes[lineNumber][x + 1]:
          return "[Line " + str(lineNumber) + "] SyntaxError: No statements allowed after ALL OF or ANY OF delimiter"
      except IndexError:
        print("", end="")
    except ValueError:
        return "[Line " + str(lineNumber) + "] SyntaxError: Missing ALL OF delimiter"
         

  # * Gets the indices of boolean operations
  operationIndices = []
  lexemeExpression = 0
  typeExpression = 0
  for index in range(len(lexemes[lineNumber])):
    if lexemes[lineNumber][index] in expressionKeywords["boolean"]:
      operationIndices.append(index)

  # * Gets the indices of AN
  anIndices = []
  for index in range(len(lexemes[lineNumber])):
    if lexemes[lineNumber][index] == "AN":
      anIndices.append(index)


  for operator in expressionKeywords["boolean"]:
    if lexemes[lineNumber][expressionIndex + 1] in ["BOTH OF", "EITHER OF", "WON OF"]:
      lexemeExpression = lexemes[lineNumber][(expressionIndex + 1):(anIndices[len(anIndices) - 1] + 3)]
      typeExpression = types[lineNumber][(expressionIndex + 1):(anIndices[len(anIndices) - 1] + 3)]

      # * Removes the string delimiters from the list
      while True:
        try:
          lexemeExpression.remove("\"")
          typeExpression.remove("string delimiter")
        except ValueError:
          break
      
    elif lexemes[lineNumber][expressionIndex + 1] == "NOT":
      # print(anIndices)
      if len(anIndices) == 0:   # single operand
        lexemeExpression = lexemes[lineNumber][(expressionIndex + 1):(expressionIndex + 3)]
        typeExpression = types[lineNumber][(expressionIndex + 1):(expressionIndex + 3)]
      elif lexemes[lineNumber][anIndices[len(anIndices) - 1] + 1] == "NOT":
        lexemeExpression = lexemes[lineNumber][(expressionIndex + 1):(anIndices[len(anIndices) - 1] + 2)]
        typeExpression = types[lineNumber][(expressionIndex + 1):(anIndices[len(anIndices) - 1] + 2)]
      else:
        lexemeExpression = lexemes[lineNumber][(expressionIndex + 1):(anIndices[len(anIndices) - 1] + 3)]
        typeExpression = types[lineNumber][(expressionIndex + 1):(anIndices[len(anIndices) - 1] + 3)]
    elif lexemes[lineNumber][expressionIndex + 1] in ["ANY OF", "ALL OF"]:
      mkayIndex = lexemes[lineNumber].index("MKAY")
      
      lexemeExpression = lexemes[lineNumber][(expressionIndex + 1):(mkayIndex)]
      typeExpression = types[lineNumber][(expressionIndex + 1):(mkayIndex)]
        
      
      # * Removes the string delimiters from the list
      while True:
        try:
          lexemeExpression.remove("\"")
          typeExpression.remove("string delimiter")
        except ValueError:
          break
    
    # print(lexemeExpression)
  
  identifierIndices = []
  for k in range(len(typeExpression)):
    if typeExpression[k] == "identifier":
      identifierIndices.append(k)
  
  for k in identifierIndices:
    if symbolTable.get(lexemeExpression[k]):
      identifier = symbolTable[lexemeExpression[k]]
      lexemeExpression[k] = identifier[0]
      typeExpression[k] = identifier[1]
    else:
      return(f"[Line {lineNumber}] SemanticError: Uninitialized variable") 
  
  print("=======")
  print(anIndices)
  print(operationIndices)
  print(lexemeExpression)
  print("=======")
  
  
  # # * Check if valid expression
  # notCount = lexemeExpression.count("NOT")
  # anyOfCount = lexemeExpression.count("ANY OF")
  # allOfCount = lexemeExpression.count("ALL OF")
  # if anyOfCount > 0 or allOfCount > 0:
  #   if lexemeExpression[operationIndices[0]] not in ["ALL OF", "ANY OF"]:
  #     if len(anIndices) != (len(operationIndices) - notCount):
  #       return(f"[Line {lineNumber}] SyntaxError: Invalid expression")
  #   else:
  #     return(f"[Line {lineNumber}] SyntaxError: Invalid expression")
  # else:
  #   if len(anIndices) != (len(operationIndices) - notCount):
  #     return(f"[Line {lineNumber}] SyntaxError: Invalid expression")
  
  # CHECKER
  # print(lexemeExpression)
  
  # print(lexemeExpression)
  # print(typeExpression)
  # return
  
  while True:
    print(lexemeExpression)
    # * Breaks the loop if lexemeExpression is equal to 1
    if (len(lexemeExpression) == 1):
      break

    # * Refreshes the operationIndices
    operationIndices.clear()
    for index in range(len(lexemeExpression)):
      if lexemeExpression[index] in expressionKeywords["boolean"]:
          operationIndices.append(index)  

    tempVal = 0

    # * Get index of first operation to solve starting from the last
    lastIndexOperator = operationIndices[len(operationIndices) - 1]   
    
    if lastIndexOperator == 0:
      if lexemeExpression[lastIndexOperator] in ["ALL OF", "ANY OF"]:
        # * Gets the indices of AN
        anIndices = []
        for index in range(len(lexemeExpression)):
          if lexemeExpression[index] == "AN":
            anIndices.append(index)
            
        for index in range(len(anIndices)):
          anIndex = anIndices[index]
          # * Last index of AN
          if anIndex == anIndices[-1]:
            if typeExpression[anIndex - 1] == "identifier":
              if symbolTable.get(lexemeExpression[anIndex - 1]):
                identifier = symbolTable[lexemeExpression[anIndex - 1]]
                lexemeExpression[anIndex - 1] = identifier[0]
                typeExpression[anIndex - 1] = identifier[1]
                
                # * Checks if TROOF or NOOB type
                if typeExpression[anIndex - 1] in ["TROOF literal", "NOOB"]:
                  if lexemeExpression[anIndex - 1] == "NOOB":
                    lexemeExpression[anIndex - 1] == False
                    typeExpression[anIndex - 1] == "TROOF literal"
                  else:
                    return "[Line " + str(lineNumber) + "] SyntaxError: Value can not be typecasted to TROOF literal"
              else:
                return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized variable"
            elif lexemeExpression[lastIndexOperator + 1] not in ["WIN", "FAIL", "NOOB"]:
              # print(f"[Line {lineNumber}] SyntaxError: Invalid statement")
              return "[Line " + str(lineNumber) + "] SyntaxError: Invalid expression"
            
            try:
              if typeExpression[anIndex + 1] == "identifier":
                if symbolTable.get(lexemeExpression[anIndex + 1]):
                  identifier = symbolTable[lexemeExpression[anIndex + 1]]
                  lexemeExpression[anIndex + 1] = identifier[0]
                  typeExpression[anIndex + 1] = identifier[1]
                  
                  # * Checks if TROOF or NOOB type
                  if typeExpression[anIndex + 1] in ["TROOF literal", "NOOB"]:
                    if lexemeExpression[anIndex + 1] == "NOOB":
                      lexemeExpression[anIndex + 1] == False
                      typeExpression[anIndex + 1] == "TROOF literal"
                    else:
                      return "[Line " + str(lineNumber) + "] SyntaxError: Value can not be typecasted to TROOF literal"
                else:
                  return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized variable"
              elif lexemeExpression[lastIndexOperator + 1] not in ["WIN", "FAIL", "NOOB"]:
                # print(f"[Line {lineNumber}] SyntaxError: Invalid statement")
                return "[Line " + str(lineNumber) + "] SyntaxError: Invalid expression"
            except:
              return "[Line " + str(lineNumber) + "] SyntaxError: Invalid expression"
            
          # * Current index of AN
          else:
            if typeExpression[anIndex - 1] == "identifier":
              if symbolTable.get(lexemeExpression[anIndex - 1]):
                identifier = symbolTable[lexemeExpression[anIndex - 1]]
                lexemeExpression[anIndex - 1] = identifier[0]
                typeExpression[anIndex - 1] = identifier[1]
                
                # * Checks if TROOF or NOOB type
                if typeExpression[anIndex - 1] in ["TROOF literal", "NOOB"]:
                  if lexemeExpression[anIndex - 1] == "NOOB":
                    lexemeExpression[anIndex - 1] == False
                    typeExpression[anIndex - 1] == "TROOF literal"
                  else:
                    return "[Line " + str(lineNumber) + "] SyntaxError: Value can not be typecasted to TROOF literal"
              else:
                return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized variable"
            elif lexemeExpression[lastIndexOperator + 1] not in ["WIN", "FAIL", "NOOB"]:
              # print(f"[Line {lineNumber}] SyntaxError: Invalid statement")
              return "[Line " + str(lineNumber) + "] SyntaxError: Invalid expression"
  
      else:
        # * Breaks the lexeme expression and replaces the values
        if lexemeExpression[lastIndexOperator] in ["BOTH OF", "EITHER OF", "WON OF"]:
          if typeExpression[lastIndexOperator + 1] == "identifier":   # ! identifier (1st operand)
            if symbolTable.get(lexemeExpression[lastIndexOperator + 1]):
              identifier = symbolTable[lexemeExpression[lastIndexOperator + 1]]
              lexemeExpression[lastIndexOperator + 1] = identifier[0]
              typeExpression[lastIndexOperator + 1] = identifier[1]
              
              # * Checks if TROOF or NOOB type
              if typeExpression[lastIndexOperator] in ["TROOF literal", "NOOB"]:
                if lexemeExpression[lastIndexOperator + 1] == "NOOB":
                  lexemeExpression[lastIndexOperator + 1] == False
                  typeExpression[lastIndexOperator + 1] == "TROOF literal"
                else:
                  return "[Line " + str(lineNumber) + "] SyntaxError: Value can not be typecasted to TROOF literal"
            else:
              return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized variable"
            
            if symbolTable.get(lexemeExpression[lastIndexOperator + 3]):
              identifier = symbolTable[lexemeExpression[lastIndexOperator + 3]]
              lexemeExpression[lastIndexOperator + 3] = identifier[0]
              typeExpression[lastIndexOperator + 3] = identifier[1]
              
              # * Checks if TROOF or NOOB type
              if typeExpression[lastIndexOperator] in ["TROOF literal", "NOOB"]:
                if lexemeExpression[lastIndexOperator + 3] == "NOOB":
                  lexemeExpression[lastIndexOperator + 3] == False
                  typeExpression[lastIndexOperator + 3] == "TROOF literal"
                else:
                  return "[Line " + str(lineNumber) + "] SyntaxError: Value can not be typecasted to TROOF literal"
            else:
              return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized variable"
          elif lexemeExpression[lastIndexOperator + 1] not in ["WIN", "FAIL", "NOOB"]:
            return "[Line " + str(lineNumber) + "] SyntaxError: Invalid expression"
        elif lexemeExpression[lastIndexOperator] == "NOT":
          if typeExpression[lastIndexOperator + 1] == "identifier":   # ! identifier (1st operand)
            if symbolTable.get(lexemeExpression[lastIndexOperator + 1]):
              identifier = symbolTable[lexemeExpression[lastIndexOperator + 1]]
              lexemeExpression[lastIndexOperator + 1] = identifier[0]
              typeExpression[lastIndexOperator + 1] = identifier[1]
              
              # * Checks if TROOF or NOOB type
              if typeExpression[lastIndexOperator] in ["TROOF literal", "NOOB"]:
                if lexemeExpression[lastIndexOperator + 1] == "NOOB":
                  lexemeExpression[lastIndexOperator + 1] == False
                  typeExpression[lastIndexOperator + 1] == "TROOF literal"
                else:
                  return "[Line " + str(lineNumber) + "] SyntaxError: Value can not be typecasted to TROOF literal"
            else:
              return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized variable"
          elif lexemeExpression[lastIndexOperator + 1] not in ["WIN", "FAIL", "NOOB"]:
            # print(f"[Line {lineNumber}] SyntaxError: Invalid statement")
            return "[Line " + str(lineNumber) + "] SyntaxError: Invalid expression"

    # * Checks the current operator
    if lexemeExpression[lastIndexOperator] == "BOTH OF":    # * AND
      if lexemeExpression[lastIndexOperator + 1] == "WIN":    # ! WIN (1st operand)
        if lexemeExpression[lastIndexOperator + 3] == "WIN":
          tempVal = "WIN"
        else:
          tempVal = "FAIL"
      else:                                                  
        if lexemeExpression[lastIndexOperator + 1] == "FAIL": # ! FAIL (1st operand)
          if lexemeExpression[lastIndexOperator + 3] == "WIN":
            tempVal = "FAIL"
          else:
            tempVal = "FAIL"
      
      # * Popping the elements from the lexeme and type list
      counter = 0
      while counter != 4:
        lexemeExpression.pop(lastIndexOperator)
        typeExpression.pop(lastIndexOperator)
        counter += 1

      # * Appending the new elements from the lexeme and type list
      lexemeExpression.insert(lastIndexOperator, str(tempVal))
      typeExpression.insert(lastIndexOperator, "TROOF literal")
    elif lexemeExpression[lastIndexOperator] == "EITHER OF":  # * OR
      if lexemeExpression[lastIndexOperator + 1] == "WIN":    # ! WIN (1st operand)
        if lexemeExpression[lastIndexOperator + 3] == "WIN":
          tempVal = "WIN"
        else:
          tempVal = "WIN"
      else:                                                  
        if lexemeExpression[lastIndexOperator + 1] == "FAIL": # ! FAIL (1st operand)
          if lexemeExpression[lastIndexOperator + 3] == "WIN":
            tempVal = "WIN"
          else:
            tempVal = "FAIL"
      
      # * Popping the elements from the lexeme and type list
      counter = 0
      while counter != 4:
        lexemeExpression.pop(lastIndexOperator)
        typeExpression.pop(lastIndexOperator)
        counter += 1

      # * Appending the new elements from the lexeme and type list
      lexemeExpression.insert(lastIndexOperator, str(tempVal))
      typeExpression.insert(lastIndexOperator, "TROOF literal")
    elif lexemeExpression[lastIndexOperator] == "WON OF":   # * XOR
      if lexemeExpression[lastIndexOperator + 1] == "WIN":    # ! WIN (1st operand)
        if lexemeExpression[lastIndexOperator + 3] == "WIN":
          tempVal = "FAIL"
        else:
          tempVal = "WIN"
      else:                                                  
        if lexemeExpression[lastIndexOperator + 1] == "FAIL": # ! FAIL (1st operand)
          if lexemeExpression[lastIndexOperator + 3] == "WIN":
            tempVal = "WIN"
          else:
            tempVal = "FAIL"
      
      # * Popping the elements from the lexeme and type list
      counter = 0
      while counter != 4:
        lexemeExpression.pop(lastIndexOperator)
        typeExpression.pop(lastIndexOperator)
        counter += 1

      # * Appending the new elements from the lexeme and type list
      lexemeExpression.insert(lastIndexOperator, str(tempVal))
      typeExpression.insert(lastIndexOperator, "TROOF literal")
    elif lexemeExpression[lastIndexOperator] == "NOT":   # * NOT
      if lexemeExpression[lastIndexOperator + 1] == "WIN":    # ! WIN operand
        tempVal = "FAIL"
      else:                                                  
        tempVal = "WIN"
    
      # * Popping the elements from the lexeme and type list
      counter = 0
      while counter != 2:
        lexemeExpression.pop(lastIndexOperator)
        typeExpression.pop(lastIndexOperator)
        counter += 1

      # * Appending the new elements from the lexeme and type list
      lexemeExpression.insert(lastIndexOperator, str(tempVal))
      typeExpression.insert(lastIndexOperator, "TROOF literal")
    elif lexemeExpression[lastIndexOperator] == "ALL OF":   # * ALL OF (infinite arity)
      literalCount = typeExpression.count("TROOF literal")
      if lexemeExpression.count("WIN") > 0 and lexemeExpression.count("FAIL") > 0:
        lexemeExpression = ["FAIL"]
        typeExpression = ["TROOF literal"]
      elif lexemeExpression.count("WIN") == literalCount:
        lexemeExpression = ["WIN"]
        typeExpression = ["TROOF literal"]
      elif lexemeExpression.count("FAIL") == literalCount:
        lexemeExpression = ["FAIL"]
        typeExpression = ["TROOF literal"]    
      break    
    elif lexemeExpression[lastIndexOperator] == "ANY OF":   # * ANY OF (infinite arity)
      literalCount = typeExpression.count("TROOF literal")
      if lexemeExpression.count("WIN") > 0 and lexemeExpression.count("FAIL") > 0:
        lexemeExpression = ["WIN"]
        typeExpression = ["TROOF literal"]
      elif lexemeExpression.count("WIN") == literalCount:
        lexemeExpression = ["WIN"]
        typeExpression = ["TROOF literal"]
      elif lexemeExpression.count("FAIL") == literalCount:
        lexemeExpression = ["FAIL"]
        typeExpression = ["TROOF literal"]
      break
  
  if lexemeExpression[0] == "WIN":
    tempVal = ["WIN", typeExpression[0]]
  else:
    tempVal = ["FAIL", typeExpression[0]]
    
  # print(lexemeExpression)
  # print(typeExpression)
  # print(tempVal)
  print(tempVal)
  return tempVal

def comparisonExpSemantics(lineNumber, symbolTable, lexemes, types):
    # * Gets the index of ITZ
    if("variable initialization keyword" in types[lineNumber]):
      expressionIndex = lexemes[lineNumber].index("ITZ")
    #put other cases where the arithmetic expression might be
    elif("print keyword" in types[lineNumber]):
      expressionIndex = lexemes[lineNumber].index("VISIBLE")
      
      operationIndices = []
      if types[lineNumber][expressionIndex + 1] not in expressionKeywords["comparison"]:
        # Find the first operation to appear in string
        for index in range(len(lexemes[lineNumber])):
          if lexemes[lineNumber][index] in expressionKeywords["comparison"]:
            operationIndices.append(index)
        
        expressionIndex = operationIndices[0] - 1
    else:
      expressionIndex = -1    

    anIndices = []
    for index in range(len(lexemes[lineNumber])):
      if lexemes[lineNumber][index] == "AN":
        anIndices.append(index)
    

    biggrOfCnt = lexemes[lineNumber].count("BIGGR OF")
    smallrOfCnt = lexemes[lineNumber].count("SMALLR OF")
    
    if (len(anIndices) - biggrOfCnt - smallrOfCnt) != len(operationIndices):
      return(f"[Line {lineNumber}] SyntaxError: Invalid expression")
    
    
    if (len(anIndices) == 1):      # (x == y OR x != y)
        if lexemes[lineNumber][expressionIndex + 1] == "BOTH SAEM": # x == y
            if types[lineNumber][expressionIndex + 2] == "identifier":  # x = identifier
                if symbolTable.get(lexemes[lineNumber][expressionIndex + 2]):
                    if types[lineNumber][expressionIndex + 4] == "identifier":      # y
                        if symbolTable.get(lexemes[lineNumber][expressionIndex + 4]):
                            if (symbolTable[lexemes[lineNumber][expressionIndex + 2]][0] == symbolTable[lexemes[lineNumber][expressionIndex + 4]][0]):
                                tempVal = ["WIN", "TROOF literal"]
                            else:
                                tempVal = ["FAIL", "TROOF literal"]
                        else:
                            return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized identifier"
                    elif types[lineNumber][expressionIndex + 4] == "NUMBR literal":
                        if (symbolTable[lexemes[lineNumber][expressionIndex + 2]][1] == "NUMBR literal"):
                            if (symbolTable[lexemes[lineNumber][expressionIndex + 2]][0] == int(lexemes[lineNumber][expressionIndex + 4])):
                                tempVal = ["WIN", "TROOF literal"]
                            else:
                                tempVal = ["FAIL", "TROOF literal"]
                        else:
                            return "[Line " + str(lineNumber) + "] SemanticError: Cannot implicitly typecast in comparison operation"
                    elif types[lineNumber][expressionIndex + 4] == "NUMBAR literal":
                        if (symbolTable[lexemes[lineNumber][expressionIndex + 2]][1] == "NUMBAR literal"):
                            if (symbolTable[lexemes[lineNumber][expressionIndex + 4]][0] == float(lexemes[lineNumber][expressionIndex + 4])):
                                tempVal = ["WIN", "TROOF literal"]
                            else:
                                tempVal = ["FAIL", "TROOF literal"]
                        else:
                            return "[Line " + str(lineNumber) + "] SemanticError: Cannot implicitly typecast in comparison operation"
                    else:
                        return "[Line " + str(lineNumber) + "] SemanticError: Invalid operands for comparison operation"
                else:
                    return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized identifier"
            elif types[lineNumber][expressionIndex + 2] == "NUMBR literal": # x = NUMBR
                if types[lineNumber][expressionIndex + 4] == "identifier":      # y
                    if symbolTable.get(lexemes[lineNumber][expressionIndex + 4]):
                        if (int(lexemes[lineNumber][expressionIndex + 2]) == symbolTable[lexemes[lineNumber][expressionIndex + 4]][0]):
                            temp = ["WIN", "TROOF literal"]
                        else:
                            temp = ["FAIL", "TROOF literal"]
                    else:
                        return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized identifier"
                elif types[lineNumber][expressionIndex + 4] == "NUMBR literal":
                    if (int(lexemes[lineNumber][expressionIndex + 2]) == int(lexemes[lineNumber][expressionIndex + 4])):
                        temp = ["WIN", "TROOF literal"]
                    else:
                        temp = ["FAIL", "TROOF literal"]
                elif types[lineNumber][expressionIndex + 4] == "NUMBAR literal":
                    if (int(lexemes[lineNumber][expressionIndex + 2]) == float(lexemes[lineNumber][expressionIndex + 4])):
                        temp = ["WIN", "TROOF literal"]
                    else:
                        temp = ["FAIL", "TROOF literal"]
                else:
                    return "[Line " + str(lineNumber) + "] SemanticError: Invalid operands for comparison operation"
            elif types[lineNumber][expressionIndex + 2] == "NUMBAR literal":    # x = NUMBAR
                if types[lineNumber][expressionIndex + 4] == "identifier":      # y
                    if symbolTable.get(lexemes[lineNumber][expressionIndex + 4]):
                        if (float(lexemes[lineNumber][expressionIndex + 2]) == symbolTable[lexemes[lineNumber][expressionIndex + 4]][0]):
                            tempVal = ["WIN", "TROOF literal"]
                        else:
                            tempVal = ["FAIL", "TROOF literal"]
                    else:
                        return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized identifier"
                elif types[lineNumber][expressionIndex + 4] == "NUMBR literal":
                    if (float(lexemes[lineNumber][expressionIndex + 2]) == int(lexemes[lineNumber][expressionIndex + 4])):
                        tempVal = ["WIN", "TROOF literal"]
                    else:
                        tempVal = ["FAIL", "TROOF literal"]
                elif types[lineNumber][expressionIndex + 4] == "NUMBAR literal":
                    if (float(lexemes[lineNumber][expressionIndex + 2]) == float(lexemes[lineNumber][expressionIndex + 4])):
                        tempVal = ["WIN", "TROOF literal"]
                    else:
                        tempVal = ["FAIL", "TROOF literal"]
                else:
                    return "[Line " + str(lineNumber) + "] SemanticError: Invalid operands for comparison operation"
            else:
                return "[Line " + str(lineNumber) + "] SemanticError: Invalid operands for comparison operation"
        else:   # DIFFRINT      x != y
            if types[lineNumber][expressionIndex + 2] == "identifier":  # x = identifier
                if symbolTable.get(lexemes[lineNumber][expressionIndex + 2]):
                    if types[lineNumber][expressionIndex + 4] == "identifier":      # y
                        if symbolTable.get(lexemes[lineNumber][expressionIndex + 4]):
                            if (symbolTable[lexemes[lineNumber][expressionIndex + 2]][0] != symbolTable[lexemes[lineNumber][expressionIndex + 4]][0]):
                                tempVal = ["WIN", "TROOF literal"]
                            else:
                                tempVal = ["FAIL", "TROOF literal"]
                        else:
                            return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized identifier"
                    elif types[lineNumber][expressionIndex + 4] == "NUMBR literal":
                        if (symbolTable[lexemes[lineNumber][expressionIndex + 2]][1] == "NUMBR literal"):
                            if (symbolTable[lexemes[lineNumber][expressionIndex + 2]][0] != int(lexemes[lineNumber][expressionIndex + 4])):
                                tempVal = ["WIN", "TROOF literal"]
                            else:
                                tempVal = ["FAIL", "TROOF literal"]
                        else:
                            return "[Line " + str(lineNumber) + "] SemanticError: Cannot implicitly typecast in comparison operation"
                    elif types[lineNumber][expressionIndex + 4] == "NUMBAR literal":
                        if (symbolTable[lexemes[lineNumber][expressionIndex + 2]][1] == "NUMBAR literal"):
                            if (symbolTable[lexemes[lineNumber][expressionIndex + 4]][0] != float(lexemes[lineNumber][expressionIndex + 4])):
                                tempVal = ["WIN", "TROOF literal"]
                            else:
                                tempVal = ["FAIL", "TROOF literal"]
                        else:
                            return "[Line " + str(lineNumber) + "] SemanticError: Cannot implicitly typecast in comparison operation"
                    else:
                        return "[Line " + str(lineNumber) + "] SemanticError: Invalid operands for comparison operation"
                else:
                    return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized identifier"
            elif types[lineNumber][expressionIndex + 2] == "NUMBR literal": # x = NUMBR
                if types[lineNumber][expressionIndex + 4] == "identifier":      # y
                    if symbolTable.get(lexemes[lineNumber][expressionIndex + 4]):
                        if (int(lexemes[lineNumber][expressionIndex + 2]) != symbolTable[lexemes[lineNumber][expressionIndex + 4]][0]):
                            tempVal = ["WIN", "TROOF literal"]
                        else:
                            tempVal = ["FAIL", "TROOF literal"]
                    else:
                        return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized identifier"
                elif types[lineNumber][expressionIndex + 4] == "NUMBR literal":
                    if (int(lexemes[lineNumber][expressionIndex + 2]) != int(lexemes[lineNumber][expressionIndex + 4])):
                        tempVal = ["WIN", "TROOF literal"]
                    else:
                        tempVal = ["FAIL", "TROOF literal"]
                elif types[lineNumber][expressionIndex + 4] == "NUMBAR literal":
                    if (int(lexemes[lineNumber][expressionIndex + 2]) != float(lexemes[lineNumber][expressionIndex + 4])):
                        tempVal = ["WIN", "TROOF literal"]
                    else:
                        tempVal = ["FAIL", "TROOF literal"]
                else:
                    return "[Line " + str(lineNumber) + "] SemanticError: Invalid operands for comparison operation"
            elif types[lineNumber][expressionIndex + 2] == "NUMBAR literal":    # x = NUMBAR
                if types[lineNumber][expressionIndex + 4] == "identifier":      # y
                    if symbolTable.get(lexemes[lineNumber][expressionIndex + 4]):
                        if (float(lexemes[lineNumber][expressionIndex + 2]) != symbolTable[lexemes[lineNumber][expressionIndex + 4]][0]):
                            tempVal = ["WIN", "TROOF literal"]
                        else:
                            tempVal = ["FAIL", "TROOF literal"]
                    else:
                        return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized identifier"
                elif types[lineNumber][expressionIndex + 4] == "NUMBR literal":
                    if (float(lexemes[lineNumber][expressionIndex + 2]) != int(lexemes[lineNumber][expressionIndex + 4])):
                        tempVal = ["WIN", "TROOF literal"]
                    else:
                        tempVal = ["FAIL", "TROOF literal"]
                elif types[lineNumber][expressionIndex + 4] == "NUMBAR literal":
                    if (float(lexemes[lineNumber][expressionIndex + 2]) != float(lexemes[lineNumber][expressionIndex + 4])):
                        tempVal = ["WIN", "TROOF literal"]
                    else:
                        tempVal = ["FAIL", "TROOF literal"]
                else:
                    return "[Line " + str(lineNumber) + "] SemanticError: Invalid operands for comparison operation"
            else:
                return "[Line " + str(lineNumber) + "] SemanticError: Invalid operands for comparison operation"

    else:       # (x <= y, x >= y, x < y, x > y)
        bigCnt = lexemes[lineNumber].count("BIGGR OF")
        try:
            sizeIndex = lexemes[lineNumber].index("BIGGR OF")
        except ValueError:
            sizeIndex = lexemes[lineNumber].index("SMALLR OF")


        if lexemes[lineNumber][expressionIndex + 1] == "BOTH SAEM": # x <= y, x >= y
            if (bigCnt == 0):       # x <= y
                if types[lineNumber][sizeIndex + 1] == "identifier":  # x = identifier
                    if symbolTable.get(lexemes[lineNumber][sizeIndex + 1]):
                        if types[lineNumber][sizeIndex + 3] == "identifier":      # y
                            if symbolTable.get(lexemes[lineNumber][sizeIndex + 3]):
                                if (symbolTable[lexemes[lineNumber][sizeIndex + 1]][0] <= symbolTable[lexemes[lineNumber][sizeIndex + 3]][0]):
                                    tempVal = ["WIN", "TROOF literal"]
                                else:
                                    tempVal = ["FAIL", "TROOF literal"]
                            else:
                                return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized identifier"
                        elif types[lineNumber][sizeIndex + 3] == "NUMBR literal":
                            if (symbolTable[lexemes[lineNumber][sizeIndex + 1]][1] == "NUMBR literal"):
                                if (symbolTable[lexemes[lineNumber][sizeIndex + 1]][0] <= int(lexemes[lineNumber][sizeIndex + 3])):
                                    tempVal = ["WIN", "TROOF literal"]
                                else:
                                    tempVal = ["FAIL", "TROOF literal"]
                            else:
                                return "[Line " + str(lineNumber) + "] SemanticError: Cannot implicitly typecast in comparison operation"
                        elif types[lineNumber][sizeIndex + 3] == "NUMBAR literal":
                            if (symbolTable[lexemes[lineNumber][sizeIndex + 1]][1] == "NUMBAR literal"):
                                if (symbolTable[lexemes[lineNumber][sizeIndex + 3]][0] <= float(lexemes[lineNumber][sizeIndex + 3])):
                                    tempVal = ["WIN", "TROOF literal"]
                                else:
                                    tempVal = ["FAIL", "TROOF literal"]
                            else:
                                return "[Line " + str(lineNumber) + "] SemanticError: Cannot implicitly typecast in comparison operation"
                        else:
                            return "[Line " + str(lineNumber) + "] SemanticError: Invalid operands for comparison operation"
                    else:
                        return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized identifier"
                elif types[lineNumber][sizeIndex + 1] == "NUMBR literal": # x = NUMBR
                    if types[lineNumber][sizeIndex + 3] == "identifier":      # y
                        if symbolTable.get(lexemes[lineNumber][sizeIndex + 3]):
                            if (int(lexemes[lineNumber][sizeIndex + 1]) <= symbolTable[lexemes[lineNumber][sizeIndex + 3]][0]):
                                temp = ["WIN", "TROOF literal"]
                            else:
                                temp = ["FAIL", "TROOF literal"]
                        else:
                            return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized identifier"
                    elif types[lineNumber][sizeIndex + 3] == "NUMBR literal":
                        if (int(lexemes[lineNumber][sizeIndex + 1]) <= int(lexemes[lineNumber][sizeIndex + 1])):
                            temp = ["WIN", "TROOF literal"]
                        else:
                            temp = ["FAIL", "TROOF literal"]
                    elif types[lineNumber][sizeIndex + 3] == "NUMBAR literal":
                        if (int(lexemes[lineNumber][sizeIndex + 1]) <= float(lexemes[lineNumber][sizeIndex + 3])):
                            temp = ["WIN", "TROOF literal"]
                        else:
                            temp = ["FAIL", "TROOF literal"]
                    else:
                        return "[Line " + str(lineNumber) + "] SemanticError: Invalid operands for comparison operation"
                elif types[lineNumber][sizeIndex + 1] == "NUMBAR literal":    # x = NUMBAR
                    if types[lineNumber][sizeIndex + 3] == "identifier":      # y
                        if symbolTable.get(lexemes[lineNumber][sizeIndex + 3]):
                            if (float(lexemes[lineNumber][sizeIndex + 1]) <= symbolTable[lexemes[lineNumber][sizeIndex + 3]][0]):
                                tempVal = ["WIN", "TROOF literal"]
                            else:
                                tempVal = ["FAIL", "TROOF literal"]
                        else:
                            return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized identifier"
                    elif types[lineNumber][sizeIndex + 3] == "NUMBR literal":
                        if (float(lexemes[lineNumber][sizeIndex + 1]) <= int(lexemes[lineNumber][sizeIndex + 3])):
                            tempVal = ["WIN", "TROOF literal"]
                        else:
                            tempVal = ["FAIL", "TROOF literal"]
                    elif types[lineNumber][sizeIndex + 3] == "NUMBAR literal":
                        if (float(lexemes[lineNumber][sizeIndex + 1]) <= float(lexemes[lineNumber][sizeIndex + 3])):
                            tempVal = ["WIN", "TROOF literal"]
                        else:
                            tempVal = ["FAIL", "TROOF literal"]
                    else:
                        return "[Line " + str(lineNumber) + "] SemanticError: Invalid operands for comparison operation"
                else:
                    return "[Line " + str(lineNumber) + "] SemanticError: Invalid operands for comparison operation"
            else:       # x >= y
                if types[lineNumber][sizeIndex + 1] == "identifier":  # x = identifier
                    if symbolTable.get(lexemes[lineNumber][sizeIndex + 1]):
                        if types[lineNumber][sizeIndex + 3] == "identifier":      # y
                            if symbolTable.get(lexemes[lineNumber][sizeIndex + 3]):
                                if (symbolTable[lexemes[lineNumber][sizeIndex + 1]][0] >= symbolTable[lexemes[lineNumber][sizeIndex + 3]][0]):
                                    tempVal = ["WIN", "TROOF literal"]
                                else:
                                    tempVal = ["FAIL", "TROOF literal"]
                            else:
                                return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized identifier"
                        elif types[lineNumber][sizeIndex + 3] == "NUMBR literal":
                            if (symbolTable[lexemes[lineNumber][sizeIndex + 1]][1] == "NUMBR literal"):
                                if (symbolTable[lexemes[lineNumber][sizeIndex + 1]][0] >= int(lexemes[lineNumber][sizeIndex + 3])):
                                    tempVal = ["WIN", "TROOF literal"]
                                else:
                                    tempVal = ["FAIL", "TROOF literal"]
                            else:
                                return "[Line " + str(lineNumber) + "] SemanticError: Cannot implicitly typecast in comparison operation"
                        elif types[lineNumber][sizeIndex + 3] == "NUMBAR literal":
                            if (symbolTable[lexemes[lineNumber][sizeIndex + 1]][1] == "NUMBAR literal"):
                                if (symbolTable[lexemes[lineNumber][sizeIndex + 3]][0] >= float(lexemes[lineNumber][sizeIndex + 3])):
                                    tempVal = ["WIN", "TROOF literal"]
                                else:
                                    tempVal = ["FAIL", "TROOF literal"]
                            else:
                                return "[Line " + str(lineNumber) + "] SemanticError: Cannot implicitly typecast in comparison operation"
                        else:
                            return "[Line " + str(lineNumber) + "] SemanticError: Invalid operands for comparison operation"
                    else:
                        return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized identifier"
                elif types[lineNumber][sizeIndex + 1] == "NUMBR literal": # x = NUMBR
                    if types[lineNumber][sizeIndex + 3] == "identifier":      # y
                        if symbolTable.get(lexemes[lineNumber][sizeIndex + 3]):
                            if (int(lexemes[lineNumber][sizeIndex + 1]) >= symbolTable[lexemes[lineNumber][sizeIndex + 3]][0]):
                                temp = ["WIN", "TROOF literal"]
                            else:
                                temp = ["FAIL", "TROOF literal"]
                        else:
                            return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized identifier"
                    elif types[lineNumber][sizeIndex + 3] == "NUMBR literal":
                        if (int(lexemes[lineNumber][sizeIndex + 1]) >= int(lexemes[lineNumber][sizeIndex + 1])):
                            temp = ["WIN", "TROOF literal"]
                        else:
                            temp = ["FAIL", "TROOF literal"]
                    elif types[lineNumber][sizeIndex + 3] == "NUMBAR literal":
                        if (int(lexemes[lineNumber][sizeIndex + 1]) >= float(lexemes[lineNumber][sizeIndex + 3])):
                            temp = ["WIN", "TROOF literal"]
                        else:
                            temp = ["FAIL", "TROOF literal"]
                    else:
                        return "[Line " + str(lineNumber) + "] SemanticError: Invalid operands for comparison operation"
                elif types[lineNumber][sizeIndex + 1] == "NUMBAR literal":    # x = NUMBAR
                    if types[lineNumber][sizeIndex + 3] == "identifier":      # y
                        if symbolTable.get(lexemes[lineNumber][sizeIndex + 3]):
                            if (float(lexemes[lineNumber][sizeIndex + 1]) >= symbolTable[lexemes[lineNumber][sizeIndex + 3]][0]):
                                tempVal = ["WIN", "TROOF literal"]
                            else:
                                tempVal = ["FAIL", "TROOF literal"]
                        else:
                            return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized identifier"
                    elif types[lineNumber][sizeIndex + 3] == "NUMBR literal":
                        if (float(lexemes[lineNumber][sizeIndex + 1]) >= int(lexemes[lineNumber][sizeIndex + 3])):
                            tempVal = ["WIN", "TROOF literal"]
                        else:
                            tempVal = ["FAIL", "TROOF literal"]
                    elif types[lineNumber][sizeIndex + 3] == "NUMBAR literal":
                        if (float(lexemes[lineNumber][sizeIndex + 1]) >= float(lexemes[lineNumber][sizeIndex + 3])):
                            tempVal = ["WIN", "TROOF literal"]
                        else:
                            tempVal = ["FAIL", "TROOF literal"]
                    else:
                        return "[Line " + str(lineNumber) + "] SemanticError: Invalid operands for comparison operation"
                else:
                    return "[Line " + str(lineNumber) + "] SemanticError: Invalid operands for comparison operation"
        else: # DIFFRINT (x < y, x > y)
            if (bigCnt == 0):       # x > y
                if types[lineNumber][sizeIndex + 1] == "identifier":  # x = identifier
                    if symbolTable.get(lexemes[lineNumber][sizeIndex + 1]):
                        if types[lineNumber][sizeIndex + 3] == "identifier":      # y
                            if symbolTable.get(lexemes[lineNumber][sizeIndex + 3]):
                                if (symbolTable[lexemes[lineNumber][sizeIndex + 1]][0] > symbolTable[lexemes[lineNumber][sizeIndex + 3]][0]):
                                    tempVal = ["WIN", "TROOF literal"]
                                else:
                                    tempVal = ["FAIL", "TROOF literal"]
                            else:
                                return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized identifier"
                        elif types[lineNumber][sizeIndex + 3] == "NUMBR literal":
                            if (symbolTable[lexemes[lineNumber][sizeIndex + 1]][1] == "NUMBR literal"):
                                if (symbolTable[lexemes[lineNumber][sizeIndex + 1]][0] > int(lexemes[lineNumber][sizeIndex + 3])):
                                    tempVal = ["WIN", "TROOF literal"]
                                else:
                                    tempVal = ["FAIL", "TROOF literal"]
                            else:
                                return "[Line " + str(lineNumber) + "] SemanticError: Cannot implicitly typecast in comparison operation"
                        elif types[lineNumber][sizeIndex + 3] == "NUMBAR literal":
                            if (symbolTable[lexemes[lineNumber][sizeIndex + 1]][1] == "NUMBAR literal"):
                                if (symbolTable[lexemes[lineNumber][sizeIndex + 3]][0] > float(lexemes[lineNumber][sizeIndex + 3])):
                                    tempVal = ["WIN", "TROOF literal"]
                                else:
                                    tempVal = ["FAIL", "TROOF literal"]
                            else:
                                return "[Line " + str(lineNumber) + "] SemanticError: Cannot implicitly typecast in comparison operation"
                        else:
                            return "[Line " + str(lineNumber) + "] SemanticError: Invalid operands for comparison operation"
                    else:
                        return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized identifier"
                elif types[lineNumber][sizeIndex + 1] == "NUMBR literal": # x = NUMBR
                    if types[lineNumber][sizeIndex + 3] == "identifier":      # y
                        if symbolTable.get(lexemes[lineNumber][sizeIndex + 3]):
                            if (int(lexemes[lineNumber][sizeIndex + 1]) > symbolTable[lexemes[lineNumber][sizeIndex + 3]][0]):
                                temp = ["WIN", "TROOF literal"]
                            else:
                                temp = ["FAIL", "TROOF literal"]
                        else:
                            return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized identifier"
                    elif types[lineNumber][sizeIndex + 3] == "NUMBR literal":
                        if (int(lexemes[lineNumber][sizeIndex + 1]) > int(lexemes[lineNumber][sizeIndex + 1])):
                            temp = ["WIN", "TROOF literal"]
                        else:
                            temp = ["FAIL", "TROOF literal"]
                    elif types[lineNumber][sizeIndex + 3] == "NUMBAR literal":
                        if (int(lexemes[lineNumber][sizeIndex + 1]) > float(lexemes[lineNumber][sizeIndex + 3])):
                            temp = ["WIN", "TROOF literal"]
                        else:
                            temp = ["FAIL", "TROOF literal"]
                    else:
                        return "[Line " + str(lineNumber) + "] SemanticError: Invalid operands for comparison operation"
                elif types[lineNumber][sizeIndex + 1] == "NUMBAR literal":    # x = NUMBAR
                    if types[lineNumber][sizeIndex + 3] == "identifier":      # y
                        if symbolTable.get(lexemes[lineNumber][sizeIndex + 3]):
                            if (float(lexemes[lineNumber][sizeIndex + 1]) > symbolTable[lexemes[lineNumber][sizeIndex + 3]][0]):
                                tempVal = ["WIN", "TROOF literal"]
                            else:
                                tempVal = ["FAIL", "TROOF literal"]
                        else:
                            return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized identifier"
                    elif types[lineNumber][sizeIndex + 3] == "NUMBR literal":
                        if (float(lexemes[lineNumber][sizeIndex + 1]) > int(lexemes[lineNumber][sizeIndex + 3])):
                            tempVal = ["WIN", "TROOF literal"]
                        else:
                            tempVal = ["FAIL", "TROOF literal"]
                    elif types[lineNumber][sizeIndex + 3] == "NUMBAR literal":
                        if (float(lexemes[lineNumber][sizeIndex + 1]) > float(lexemes[lineNumber][sizeIndex + 3])):
                            tempVal = ["WIN", "TROOF literal"]
                        else:
                            tempVal = ["FAIL", "TROOF literal"]
                    else:
                        return "[Line " + str(lineNumber) + "] SemanticError: Invalid operands for comparison operation"
                else:
                    return "[Line " + str(lineNumber) + "] SemanticError: Invalid operands for comparison operation"
            else:       # x < y
                if types[lineNumber][sizeIndex + 1] == "identifier":  # x = identifier
                    if symbolTable.get(lexemes[lineNumber][sizeIndex + 1]):
                        if types[lineNumber][sizeIndex + 3] == "identifier":      # y
                            if symbolTable.get(lexemes[lineNumber][sizeIndex + 3]):
                                if (symbolTable[lexemes[lineNumber][sizeIndex + 1]][0] < symbolTable[lexemes[lineNumber][sizeIndex + 3]][0]):
                                    tempVal = ["WIN", "TROOF literal"]
                                else:
                                    tempVal = ["FAIL", "TROOF literal"]
                            else:
                                return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized identifier"
                        elif types[lineNumber][sizeIndex + 3] == "NUMBR literal":
                            if (symbolTable[lexemes[lineNumber][sizeIndex + 1]][1] == "NUMBR literal"):
                                if (symbolTable[lexemes[lineNumber][sizeIndex + 1]][0] < int(lexemes[lineNumber][sizeIndex + 3])):
                                    tempVal = ["WIN", "TROOF literal"]
                                else:
                                    tempVal = ["FAIL", "TROOF literal"]
                            else:
                                return "[Line " + str(lineNumber) + "] SemanticError: Cannot implicitly typecast in comparison operation"
                        elif types[lineNumber][sizeIndex + 3] == "NUMBAR literal":
                            if (symbolTable[lexemes[lineNumber][sizeIndex + 1]][1] == "NUMBAR literal"):
                                if (symbolTable[lexemes[lineNumber][sizeIndex + 3]][0] < float(lexemes[lineNumber][sizeIndex + 3])):
                                    tempVal = ["WIN", "TROOF literal"]
                                else:
                                    tempVal = ["FAIL", "TROOF literal"]
                            else:
                                return "[Line " + str(lineNumber) + "] SemanticError: Cannot implicitly typecast in comparison operation"
                        else:
                            return "[Line " + str(lineNumber) + "] SemanticError: Invalid operands for comparison operation"
                    else:
                        return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized identifier"
                elif types[lineNumber][sizeIndex + 1] == "NUMBR literal": # x = NUMBR
                    if types[lineNumber][sizeIndex + 3] == "identifier":      # y
                        if symbolTable.get(lexemes[lineNumber][sizeIndex + 3]):
                            if (int(lexemes[lineNumber][sizeIndex + 1]) < symbolTable[lexemes[lineNumber][sizeIndex + 3]][0]):
                                temp = ["WIN", "TROOF literal"]
                            else:
                                temp = ["FAIL", "TROOF literal"]
                        else:
                            return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized identifier"
                    elif types[lineNumber][sizeIndex + 3] == "NUMBR literal":
                        if (int(lexemes[lineNumber][sizeIndex + 1]) < int(lexemes[lineNumber][sizeIndex + 1])):
                            temp = ["WIN", "TROOF literal"]
                        else:
                            temp = ["FAIL", "TROOF literal"]
                    elif types[lineNumber][sizeIndex + 3] == "NUMBAR literal":
                        if (int(lexemes[lineNumber][sizeIndex + 1]) < float(lexemes[lineNumber][sizeIndex + 3])):
                            temp = ["WIN", "TROOF literal"]
                        else:
                            temp = ["FAIL", "TROOF literal"]
                    else:
                        return "[Line " + str(lineNumber) + "] SemanticError: Invalid operands for comparison operation"
                elif types[lineNumber][sizeIndex + 1] == "NUMBAR literal":    # x = NUMBAR
                    if types[lineNumber][sizeIndex + 3] == "identifier":      # y
                        if symbolTable.get(lexemes[lineNumber][sizeIndex + 3]):
                            if (float(lexemes[lineNumber][sizeIndex + 1]) < symbolTable[lexemes[lineNumber][sizeIndex + 3]][0]):
                                tempVal = ["WIN", "TROOF literal"]
                            else:
                                tempVal = ["FAIL", "TROOF literal"]
                        else:
                            return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized identifier"
                    elif types[lineNumber][sizeIndex + 3] == "NUMBR literal":
                        if (float(lexemes[lineNumber][sizeIndex + 1]) < int(lexemes[lineNumber][sizeIndex + 3])):
                            tempVal = ["WIN", "TROOF literal"]
                        else:
                            tempVal = ["FAIL", "TROOF literal"]
                    elif types[lineNumber][sizeIndex + 3] == "NUMBAR literal":
                        if (float(lexemes[lineNumber][sizeIndex + 1]) < float(lexemes[lineNumber][sizeIndex + 3])):
                          tempVal = ["WIN", "TROOF literal"]
                        else:
                          tempVal = ["FAIL", "TROOF literal"]
                    else:
                      return "[Line " + str(lineNumber) + "] SemanticError: Invalid operands for comparison operation"
                else:
                    return "[Line " + str(lineNumber) + "] SemanticError: Invalid operands for comparison operation"
    
    return tempVal

def concatenationExpSemantics(lineNumber, symbolTable, lexemes, types):
  # ! NO OPERATIONS AS OPERANDS YET
  # * Gets the index of ITZ
  if("variable initialization keyword" in types[lineNumber]):
    expressionIndex = lexemes[lineNumber].index("ITZ")
  #put other cases where the arithmetic expression might be
  elif("print keyword" in types[lineNumber]):
    expressionIndex = lexemes[lineNumber].index("VISIBLE")
  else:
    expressionIndex = -1    
  
  #print(lexemes[lineNumber][expressionIndex])
  anIndices = []
  for index in range(len(lexemes[lineNumber])):
    if lexemes[lineNumber][index] == "AN":
        anIndices.append(index)
  
  counter = 0
  tempVal = ''
  while True:
    if (counter == len(anIndices) - 1):
      if (types[lineNumber][anIndices[counter] - 1] == "identifier"):
        if (symbolTable.get(lexemes[lineNumber][anIndices[counter] - 1])):
          tempVal += str(symbolTable[lexemes[lineNumber][anIndices[counter] - 1]][0])
        else:
          return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized identifier"
      elif (types[lineNumber][anIndices[counter] - 1] == "string delimiter"):     # YARN literal
        if (types[lineNumber][anIndices[counter] - 3] == "string delimiter"):   # another delimiter
          tempVal += lexemes[lineNumber][anIndices[counter] - 2]
        else:
          return "[Line " + str(lineNumber) + "] SyntaxError: Invalid syntax of YARN literal"     # ! TAKE NOTE
      else:
        tempVal += str(lexemes[lineNumber][anIndices[counter] - 1])
      
      if (types[lineNumber][anIndices[counter] + 1] == "identifier"):
        if (symbolTable.get(lexemes[lineNumber][anIndices[counter] + 1])):
          tempVal += str(symbolTable[lexemes[lineNumber][anIndices[counter] + 1]][0])
        else:
          return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized identifier"
      elif (types[lineNumber][anIndices[counter] + 1] == "string delimiter"):     # YARN literal
        if (types[lineNumber][anIndices[counter] + 3] == "string delimiter"):   # another delimiter
          tempVal += lexemes[lineNumber][anIndices[counter] + 2]
        else:
          return "[Line " + str(lineNumber) + "] SyntaxError: Invalid syntax of YARN literal"     # ! TAKE NOTE
      else:
        tempVal += str(lexemes[lineNumber][anIndices[counter] + 1])

      break
    
    if (types[lineNumber][anIndices[counter] - 1] == "identifier"):
      if (symbolTable.get(lexemes[lineNumber][anIndices[counter] - 1])):
        tempVal += str(symbolTable[lexemes[lineNumber][anIndices[counter] - 1]][0])
      else:
        return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized identifier"
    elif (types[lineNumber][anIndices[counter] - 1] == "string delimiter"):     # YARN literal
      if (types[lineNumber][anIndices[counter] - 3] == "string delimiter"):   # another delimiter
        tempVal += lexemes[lineNumber][anIndices[counter] - 2]
      else:
        return "[Line " + str(lineNumber) + "] SyntaxError: Invalid syntax of YARN literal"     # ! TAKE NOTE
    else:
      tempVal += str(lexemes[lineNumber][anIndices[counter] - 1])


    counter += 1
    
  tempVal = [tempVal, "YARN literal"]
  
  return tempVal

def visibleExpSemantics(lineNumber, symbolTable, lexemes, types):
  # * Gets the index of VISIBLE
  visibleIndex = lexemes[lineNumber].index("VISIBLE")
  
  if visibleIndex != 0:
    return "[Line " + str(lineNumber) + "] SyntaxError: VISIBLE should be the first element in the line"
  
  lexemeExpression = 0
  typeExpression = 0
  
  # * Check if valid syntax of YARN literal
  yarnIndices = []
  for index in range(len(types[lineNumber])):
    if types[lineNumber][index] == "YARN literal":
      yarnIndices.append(index)
      
  for index in yarnIndices:
    if types[lineNumber][index - 1] != "string delimiter" or types[lineNumber][index + 1] != "string delimiter":
      return "[Line " + str(lineNumber) + "] SyntaxError: Invalid format of YARN literal"
  
  # * Check if there are comments
  endIndex = -1
  try:
    btwIndex = lexemes[lineNumber].index("BTW")
    
    endIndex = btwIndex - 1
  except ValueError:
    endIndex = len(lexemes[lineNumber]) - 1
  
  # * Creates the whole expression excluding the comments and VISIBLE keyword
  lexemeExpression = lexemes[lineNumber][(1):(endIndex + 1)]
  typeExpression = types[lineNumber][(1):(endIndex + 1)]

  # * Removes the string delimiters from the list
  while True:
    try:
      lexemeExpression.remove("\"")
      typeExpression.remove("string delimiter")
    except ValueError:
      break
    
  # * Converts the identifiers to their respective values
  
  for index in range(len(lexemeExpression)):
    if lexemeExpression[index] == "AN":
      lexemeExpression[index] = " "
  
  identifierIndices = []
  for index in range(len(typeExpression)):
    if typeExpression[index] == "identifier":
      identifierIndices.append(index)
      
  for index in identifierIndices:
    if symbolTable.get(lexemeExpression[index]):      
      identifier = symbolTable[lexemeExpression[index]]
      lexemeExpression[index] = identifier[0]
      typeExpression[index] = identifier[1]
      
      if lexemeExpression[index] == "NOOB":
        return ["NOOB", "NOOB"]
    else:
      return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized identifier"
  
  # * Gets the indices of operations in the expression
  operationIndices = []
  
  while True:
    # * Refreshes the operationIndices
    operationIndices.clear()
    for index in range(len(lexemeExpression)):
      if lexemeExpression[index] in expressionKeywords["arithmetic"]:
        operationIndices.append(index)
      if lexemeExpression[index] in expressionKeywords["boolean"]:
        operationIndices.append(index)
      if lexemeExpression[index] in expressionKeywords["comparison"]:
        operationIndices.append(index)
      if lexemeExpression[index] in expressionKeywords["concatenation"]:
        operationIndices.append(index)
    
    if len(operationIndices) == 0:
      break
      
        
    # * Get index of first operation to solve starting from the last
    print("*************")
    print(operationIndices)
    print(lexemeExpression)
    print("*************")
    if lexemeExpression[operationIndices[0]] in ["BOTH SAEM", "DIFFRINT", "SMOOSH"]:
      lastIndexOperator = 0
    else:
      lastIndexOperator = operationIndices[len(operationIndices) - 1]
    
    print("*************")
    print(lastIndexOperator)
    print("*************")
         
    
    if lexemeExpression[lastIndexOperator] in expressionKeywords["arithmetic"]:
      tempVal = arithmeticExpSemantics(lineNumber, symbolTable, lexemes, types)
      
      if type(tempVal) != list:
        return tempVal
      
      # * Popping the elements from the lexeme and type list
      if lexemeExpression[lastIndexOperator] not in ["ALL OF", "ANY OF", "SMOOSH", "NOT"]:
        counter = 0
        while counter != 3:
          lexemeExpression.pop(lastIndexOperator)
          typeExpression.pop(lastIndexOperator)
          counter += 1
      elif lexemeExpression[lastIndexOperator] == "NOT":
        counter = 0
        while counter != 1:
          lexemeExpression.pop(lastIndexOperator)
          typeExpression.pop(lastIndexOperator)
          counter += 1
      
      lexemeExpression[lastIndexOperator] = tempVal[0]
      typeExpression[lastIndexOperator] = tempVal[1]
      
    elif lexemeExpression[lastIndexOperator] in expressionKeywords["boolean"]:
      tempVal = booleanExpSemantics(lineNumber, symbolTable, lexemes, types)
      
      if type(tempVal) != list:
        return tempVal
      
      # * Popping the elements from the lexeme and type list
      if lexemeExpression[lastIndexOperator] not in ["ALL OF", "ANY OF", "SMOOSH", "NOT"]:
        counter = 0
        while counter != 3:
          lexemeExpression.pop(lastIndexOperator)
          typeExpression.pop(lastIndexOperator)
          counter += 1
      elif lexemeExpression[lastIndexOperator] == "NOT":
        counter = 0
        while counter != 1:
          lexemeExpression.pop(lastIndexOperator)
          typeExpression.pop(lastIndexOperator)
          counter += 1
      else:
        try:
          while len(lexemeExpression) != 1:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
        except IndexError:
          lexemeExpression[lastIndexOperator] = tempVal[0]
          typeExpression[lastIndexOperator] = tempVal[1]
          
      
      lexemeExpression[lastIndexOperator] = tempVal[0]
      typeExpression[lastIndexOperator] = tempVal[1]
    
    elif lexemeExpression[lastIndexOperator] in expressionKeywords["comparison"]:
      tempVal = comparisonExpSemantics(lineNumber, symbolTable, lexemes, types)
      
      if type(tempVal) != list:
        return tempVal
      
      # * Popping the elements from the lexeme and type list
      if lexemeExpression[lastIndexOperator] not in ["ALL OF", "ANY OF", "SMOOSH", "NOT"]:
        counter = 0
        while counter != 3:
          lexemeExpression.pop(lastIndexOperator)
          typeExpression.pop(lastIndexOperator)
          counter += 1
      elif lexemeExpression[lastIndexOperator] == "NOT":
        counter = 0
        while counter != 1:
          lexemeExpression.pop(lastIndexOperator)
          typeExpression.pop(lastIndexOperator)
          counter += 1
      else:
        try:
          while len(lexemeExpression) != 1:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
        except IndexError:
          lexemeExpression[lastIndexOperator] = tempVal[0]
          typeExpression[lastIndexOperator] = tempVal[1]
      
      lexemeExpression = [0]
      typeExpression = [0]
      
      
      lexemeExpression[lastIndexOperator] = tempVal[0]
      typeExpression[lastIndexOperator] = tempVal[1]
    
    elif lexemeExpression[lastIndexOperator] in expressionKeywords["concatenation"]:
      tempVal = concatenationExpSemantics(lineNumber, symbolTable, lexemes, types)
      
      if type(tempVal) != list:
        return tempVal
      
      # * Popping the elements from the lexeme and type list
      if lexemeExpression[lastIndexOperator] not in ["ALL OF", "ANY OF", "SMOOSH", "NOT"]:
        counter = 0
        while counter != 3:
          lexemeExpression.pop(lastIndexOperator)
          typeExpression.pop(lastIndexOperator)
          counter += 1
      elif lexemeExpression[lastIndexOperator] == "NOT":
        counter = 0
        while counter != 1:
          lexemeExpression.pop(lastIndexOperator)
          typeExpression.pop(lastIndexOperator)
          counter += 1
      else:
        try:
          while len(lexemeExpression) != 1:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
        except IndexError:
          lexemeExpression[lastIndexOperator] = tempVal[0]
          typeExpression[lastIndexOperator] = tempVal[1]
          
      
      lexemeExpression[lastIndexOperator] = tempVal[0]
      typeExpression[lastIndexOperator] = tempVal[1]
  
  print(lexemeExpression)
  print(typeExpression)
  
  
      
  
  # * Converts the list to a whole string
  for index in range(len(lexemeExpression)):
    if typeExpression[index] == "NOOB":
      return "[Line " + str(lineNumber) + "] SemanticError: NOOB literal can not be typecasted to YARN literal"
    else:
      lexemeExpression[index] = str(lexemeExpression[index])
    
  # print(operationIndices)
  tempVal = ''.join(element for element in lexemeExpression)
  
  tempVal = [tempVal, "YARN literal"]
  
  print(operationIndices)
  print(lexemes[lineNumber])
  print(types[lineNumber])
  
  return tempVal
   
def identifierExpSemantics(lineNumber, symbolTable, lexemes, types):
  identifierIndex = types[lineNumber].index("identifier")
  rIndex = -1
  maekIndex = -1
  
  while True:
    try:
      if lexemes[lineNumber][identifierIndex + 1] == "R":
        rIndex = identifierIndex + 1
        
        try:
          if lexemes[lineNumber][identifierIndex + 2] == "MAEK":
            try:
              if types[lineNumber][identifierIndex + 3] == "identifier":
                if symbolTable.get(lexemes[lineNumber][identifierIndex + 3]):
                  identifier = symbolTable[lexemes[lineNumber][identifierIndex + 3]]
                  
                  try:
                    print("-------")
                    print(lexemes[lineNumber][identifierIndex + 4])
                    print(types[lineNumber][identifierIndex + 4])
                    print(identifier[0])
                    print(identifier[1])
                    print("-------")
                    
                    if types[lineNumber][identifierIndex + 4] in ["TYPE literal"]:
                      literal = lexemes[lineNumber][identifierIndex + 4]
                      if identifier[1] == "NUMBR literal":
                        if literal == "NUMBR":
                          tempVal = [int(identifier[0]), "NUMBR literal"]
                          
                          return tempVal
                        elif literal == "NUMBAR":
                          tempVal = [float(identifier[0]), "NUMBAR literal"]
                          
                          return tempVal
                        elif literal == "TROOF":
                          if int(identifier[0]) == 0:
                            tempVal = ["FAIL", "TROOF literal"]
                          else:
                            tempVal = ["WIN", "TROOF literal"]
                            
                          return tempVal
                        elif literal == "YARN":
                          tempVal = [str(identifier[0]), "YARN literal"]
                            
                          return tempVal
                        else:   # NOOB
                          return "[Line " + str(lineNumber) + "] SemanticError: Cannot typecast identifier to NOOB"
                      elif identifier[1] == "NUMBAR literal":
                        if literal == "NUMBR":
                          tempVal = [int(identifier[0]), "NUMBR literal"]
                          
                          return tempVal
                        elif literal == "NUMBAR":
                          tempVal = [float(identifier[0]), "NUMBAR literal"]
                          
                          return tempVal
                        elif literal == "TROOF":
                          if float(identifier[0]) == 0.0:
                            tempVal = ["FAIL", "TROOF literal"]
                          else:
                            tempVal = ["WIN", "TROOF literal"]
                            
                          return tempVal
                        elif literal == "YARN":
                          tempVal = [str(identifier[0]), "YARN literal"]
                            
                          return tempVal
                        else:   # NOOB
                          return "[Line " + str(lineNumber) + "] SemanticError: Cannot typecast identifier to NOOB"
                      elif identifier[1] == "TROOF literal":
                        if literal == "NUMBR":
                          if identifier[0] == "WIN":
                            tempVal = [int(1), "NUMBR literal"]
                          else:
                            tempVal = [int(0), "NUMBR literal"]
                          
                          return tempVal
                        elif literal == "NUMBAR":
                          if identifier[0] == "WIN":
                            tempVal = [float(1), "NUMBAR literal"]
                          else:
                            tempVal = [float(0), "NUMBAR literal"]
                          
                          return tempVal
                        elif literal == "TROOF":
                          tempVal = [identifier[0], identifier[1]]
                            
                          return tempVal
                        elif literal == "YARN":
                          tempVal = [str(identifier[0]), "YARN literal"]
                            
                          return tempVal
                        else:   # NOOB
                          return "[Line " + str(lineNumber) + "] SemanticError: Cannot typecast identifier to NOOB"
                      elif identifier[1] == "YARN literal":
                        if literal == "NUMBR":
                          try:
                            tempVal = [int(identifier[0]), "NUMBR literal"]
                          except ValueError:
                            return "[Line " + str(lineNumber) + "] SemanticError: Cannot typecast identifier to NUMBR literal"
                          
                          return tempVal
                        elif literal == "NUMBAR":
                          try:
                            tempVal = [float(identifier[0]), "NUMBAR literal"]
                          except ValueError:
                            return "[Line " + str(lineNumber) + "] SemanticError: Cannot typecast identifier to NUMBAR literal"
                          
                          return tempVal
                        elif literal == "TROOF":
                          if identifier[0] == "":
                            tempVal = ["FAIL", "TROOF literal"]
                          else:
                            tempVal = ["WIN", "TROOF literal"]
                            
                          return tempVal
                        elif literal == "YARN":
                          tempVal = [str(identifier[0]), "YARN literal"]
                            
                          return tempVal
                        else:   # NOOB
                          return "[Line " + str(lineNumber) + "] SemanticError: Cannot typecast identifier to NOOB"
                      else: # NOOB
                        if literal == "NUMBR literal":
                          tempVal = [int(0), literal]
                          
                          return tempVal
                        elif literal == "NUMBAR literal":
                          tempVal = [float(0), literal]
                          
                          return tempVal
                        elif literal == "TROOF literal":
                          tempVal = ["FAIL", literal]
                            
                          return tempVal
                        elif literal == "YARN literal":
                          tempVal = [str(""), literal]
                            
                          return tempVal
                        else:   # NOOB
                          tempVal = [identifier[0], literal]
                            
                          return tempVal
                    else:
                      return "[Line " + str(lineNumber) + "] SemanticError: Invalid literal for typecasting"
                  except IndexError:
                    return "[Line " + str(lineNumber) + "] SyntaxError: Invalid typecasting format"
                else:
                  return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized variable"
              else:
                return "[Line " + str(lineNumber) + "] SemanticError: Expected an identifier to be typecasted"
            except IndexError:
              return "[Line " + str(lineNumber) + "] SyntaxError: Invalid typecasting format"
          else:
            break
        except IndexError:
          return "[Line " + str(lineNumber) + "] SyntaxError: Invalid typecasting format"
      elif lexemes[lineNumber][identifierIndex + 1] == "IS NOW A":
        if symbolTable.get(lexemes[lineNumber][identifierIndex]):
          identifier = symbolTable[lexemes[lineNumber][identifierIndex]]
          
          try:
            if lexemes[lineNumber][identifierIndex + 3] != "BTW":
                return "[Line " + str(lineNumber) + "] SyntaxError: Cannot have statements after operation"
          except IndexError:
          
            try:
              print("-------")
              print(lexemes[lineNumber][identifierIndex + 2])
              print(types[lineNumber][identifierIndex + 2])
              print(identifier[0])
              print(identifier[1])
              print("-------")
              
              if types[lineNumber][identifierIndex + 2] in ["TYPE literal"]:
                literal = lexemes[lineNumber][identifierIndex + 2]

                if identifier[1] == "NUMBR literal":
                  if literal == "NUMBR":
                    tempVal = [int(identifier[0]), "NUMBR literal"]
                    
                    return tempVal
                  elif literal == "NUMBAR":
                    tempVal = [float(identifier[0]), "NUMBAR literal"]
                    
                    return tempVal
                  elif literal == "TROOF":
                    if int(identifier[0]) == 0:
                      tempVal = ["FAIL", "TROOF literal"]
                    else:
                      tempVal = ["WIN", "TROOF literal"]
                      
                    return tempVal
                  elif literal == "YARN":
                    tempVal = [str(identifier[0]), "YARN literal"]
                      
                    return tempVal
                  else:   # NOOB
                    return "[Line " + str(lineNumber) + "] SemanticError: Cannot typecast identifier to NOOB"
                elif identifier[1] == "NUMBAR literal":
                  if literal == "NUMBR":
                    tempVal = [int(identifier[0]), "NUMBR literal"]
                    
                    return tempVal
                  elif literal == "NUMBAR":
                    tempVal = [float(identifier[0]), "NUMBAR literal"]
                    
                    return tempVal
                  elif literal == "TROOF":
                    if float(identifier[0]) == 0.0:
                      tempVal = ["FAIL", "TROOF literal"]
                    else:
                      tempVal = ["WIN", "TROOF literal"]
                      
                    return tempVal
                  elif literal == "YARN":
                    tempVal = [str(identifier[0]), "YARN literal"]
                      
                    return tempVal
                  else:   # NOOB
                    return "[Line " + str(lineNumber) + "] SemanticError: Cannot typecast identifier to NOOB"
                elif identifier[1] == "TROOF literal":
                  if literal == "NUMBR":
                    if identifier[0] == "WIN":
                      tempVal = [int(1), "NUMBR literal"]
                    else:
                      tempVal = [int(0), "NUMBR literal"]
                    
                    return tempVal
                  elif literal == "NUMBAR":
                    if identifier[0] == "WIN":
                      tempVal = [float(1), "NUMBAR literal"]
                    else:
                      tempVal = [float(0), "NUMBAR literal"]
                    
                    return tempVal
                  elif literal == "TROOF":
                    tempVal = [identifier[0], identifier[1]]
                      
                    return tempVal
                  elif literal == "YARN":
                    tempVal = [str(identifier[0]), "YARN literal"]
                      
                    return tempVal
                  else:   # NOOB
                    return "[Line " + str(lineNumber) + "] SemanticError: Cannot typecast identifier to NOOB"
                elif identifier[1] == "YARN literal":
                  if literal == "NUMBR":
                    try:
                      tempVal = [int(identifier[0]), "NUMBR literal"]
                    except ValueError:
                      return "[Line " + str(lineNumber) + "] SemanticError: Cannot typecast identifier to NUMBR literal"
                    
                    return tempVal
                  elif literal == "NUMBAR":
                    try:
                      tempVal = [float(identifier[0]), "NUMBAR literal"]
                    except ValueError:
                      return "[Line " + str(lineNumber) + "] SemanticError: Cannot typecast identifier to NUMBAR literal"
                    
                    return tempVal
                  elif literal == "TROOF":
                    if identifier[0] == "":
                      tempVal = ["FAIL", "TROOF literal"]
                    else:
                      tempVal = ["WIN", "TROOF literal"]
                      
                    return tempVal
                  elif literal == "YARN":
                    tempVal = [str(identifier[0]), "YARN literal"]
                      
                    return tempVal
                  else:   # NOOB
                    return "[Line " + str(lineNumber) + "] SemanticError: Cannot typecast identifier to NOOB"
                else: # NOOB
                  if literal == "NUMBR literal":
                    tempVal = [int(0), "NUMBR literal"]
                    
                    return tempVal
                  elif literal == "NUMBAR literal":
                    tempVal = [float(0), "NUMBAR literal"]
                    
                    return tempVal
                  elif literal == "TROOF literal":
                    tempVal = ["FAIL", "TROOF literal"]
                      
                    return tempVal
                  elif literal == "YARN literal":
                    tempVal = [str(""), "YARN literal"]
                      
                    return tempVal
                  else:   # NOOB
                    tempVal = [identifier[0], "NOOB"]
                      
                    return tempVal
              else:
                return "[Line " + str(lineNumber) + "] SemanticError: Invalid literal for typecasting"
            except IndexError:
              print("hahhaha")
              return "[Line " + str(lineNumber) + "] SyntaxError: Invalid typecasting format"
        else:
          return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized variable"
      else:
        return "[Line " + str(lineNumber) + "] SyntaxError: Invalid assignment format"
    except IndexError:
      return symbolTable[lexemes[lineNumber][identifierIndex]]

  # * R exists
  if rIndex != -1:
    try:
      if types[lineNumber][rIndex + 1] in ["identifier", "NUMBR literal", "NUMBAR literal", "TROOF literal", "string delimiter"]:
        if types[lineNumber][rIndex + 1] == "identifier":
          if symbolTable.get(lexemes[lineNumber][rIndex + 1]):
            return [symbolTable[lexemes[lineNumber][rIndex + 1]][0], symbolTable[lexemes[lineNumber][rIndex + 1]][1]]
          else:
            return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized identifier"
        elif types[lineNumber][rIndex + 1] in ["NUMBR literal", "NUMBAR literal", "TROOF literal"]:
          print(f"{lexemes[lineNumber][0]} = {lexemes[lineNumber][rIndex + 1]}")
          print([lexemes[lineNumber][rIndex + 1], types[lineNumber][rIndex + 1]])
          print("====")
          return [lexemes[lineNumber][rIndex + 1], types[lineNumber][rIndex + 1]]
        else:   # YARN literal
          yarnIndex = types[lineNumber].index("YARN literal")
          
          try:
            if types[lineNumber][yarnIndex - 1] == "string delimiter" or types[lineNumber][yarnIndex + 1] == "string delimiter":
              return [lexemes[lineNumber][yarnIndex], "YARN literal"]
          except IndexError:
            return "[Line " + str(lineNumber) + "] SyntaxError: Invalid YARN literal format"
            
      
      if lexemes[lineNumber][rIndex + 1] in expressionKeywords["arithmetic"] or lexemes[lineNumber][rIndex + 1] in expressionKeywords["boolean"] or lexemes[lineNumber][rIndex + 1] in expressionKeywords["comparison"] or lexemes[lineNumber][rIndex + 1] in expressionKeywords["concatenation"]:
        operator = lexemes[lineNumber][rIndex + 1]
        
        if operator in expressionKeywords["arithmetic"]:
          temp = arithmeticExpSemantics(lineNumber, symbolTable, lexemes, types)
  
          # * Semantic Error
          if type(temp) != list:
            return temp
          
          tempVal = [temp[0], temp[1]]
          
          return tempVal
        elif operator in expressionKeywords["boolean"]:
          temp = booleanExpSemantics(lineNumber, symbolTable, lexemes, types)
  
          # * Semantic Error
          if type(temp) != list:
            return temp
          
          tempVal = [temp[0], temp[1]]
          
          return tempVal
        elif operator in expressionKeywords["comparison"]:
          temp = comparisonExpSemantics(lineNumber, symbolTable, lexemes, types)
  
          # * Semantic Error
          if type(temp) != list:
            return temp
          
          tempVal = [temp[0], temp[1]]
          
          return tempVal
        elif operator in expressionKeywords["concatenation"]:
          temp = concatenationExpSemantics(lineNumber, symbolTable, lexemes, types)

          print("adsvdfsb")
          print(temp)
          print("adsvdfsb")

          # * Semantic Error
          if type(temp) != list:
            return temp
          
          tempVal = [temp[0], temp[1]]
          
          return tempVal
        
    except IndexError:
      return "[Line " + str(lineNumber) + "] SyntaxError: Invalid assignment format"
      
    
    
    # * MAEK exists
    # if maekIndex != -1:
    # * MAEK does not exist
    # else:

    
  
  