import re

from classes.Token import Token

class Lexer:
  def __init__(self, text, TOK_EXP):
    self.text = text
    self.token_expressions = TOK_EXP

  def tokenize(self):
    tokens = [] 
    lines = self.text.split("\n")
    line_number = 1
    isMultiComment = False
    for line in lines:
      line = line.strip()
      line = line + "\n"
      while (line != "" and line != "\n"):
        for token_exp in self.token_expressions:
          pattern, tag = token_exp
          match = re.match(pattern, line)
          
          
          if(isMultiComment): 
            name = line[:-1]
            if name == "TLDR":
              isMultiComment = False
              tag = "TLDR_KEYWORD"
              tokens.append(
                  Token(name,tag, line_number)
                )
            else:
              tag ="BTW_KEYWORD"
              tokens.append(
                Token("COMMENT",tag,line_number)
              )
            line = line[-1:] 
            break

          elif (match):
            
            if(tag == 'YARN'):
              name = match.group(0)
              name = name[1:-2]

            elif(tag == 'BTW_KEYWORD'):
              name = match.group(0)[:-1]
              tokens.append(
                Token(name,tag, line_number)
              )
              line = line[-1:] 
              break
            elif(tag == 'OBTW_KEYWORD'):
              isMultiComment = True
              name = match.group(0)[:-1]
            else:
              name = match.group(0)[:-1]
            tokens.append(
                Token(name,tag, line_number)
              )
            line = line[match.end(0):]
            break

          
        else:
          raise Exception(f"Error in line number {line_number}: Invalid token")
      if (not isMultiComment):
        tokens.append(Token("\\n", "LINEBREAK", line_number))
      line_number += 1
    if(isMultiComment):
      raise Exception("Error: TLDR not found")
    return tokens