# Author: Christian Olo
# Program Description: A LOLCode interpreter developed using python

# source code for the parser
# 1. Creates a symbol tree by checking the tokens. Every grammar is a child
# in which the lolProgram is the root node
# 2. Linearly checks the tokens, and if a token did not match the grammar by checking
# it using the nextToken function, an error is raised.
# 3. Uses recursion to append childNodes until non-terminal grammars


from ATNode import ATNode           # uses the ATNode class to see valid syntax symbols
from collections import deque

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_idx = 0
        self.current_token = self.tokens[self.token_idx]
        self.err = ''
    
    # checks if the current token is equal to the token_type
    # this is where errors are raised if invalid syntax
    def nextToken(self, token_type):
        # if valid token, proceed to the next
        if  self.current_token.type == token_type:
            if self.token_idx + 1 < len(self.tokens):
                self.token_idx += 1
                self.current_token = self.tokens[self.token_idx]
            else:
                self.token_idx += 1
        elif(self.current_token.type == 'Comment Delimiter'):        # ignore if comment
            self.nextToken('Comment Delimiter')
            self.nextToken('Comment')
            self.nextToken('Linebreak')
        else:                                                        # invalid current toke
            self.err = f"Syntax Error:{self.current_token.line_num}:Expected {token_type} at {self.current_token.value}"
            raise Exception()

    # ------------------------LITERALS/EXPRESISON/VARIABLE------------------------
    # grammar for expresison, literal, and variables
    # infAr is boolean indicating that curr expression is not any of or all of
    def exprvar(self, infAr):
        childNodes = deque()
        if (literal := self.literal()): 
            childNodes.append(literal)
        elif(self.current_token.type == 'Implicit Variable'):
            childNodes.append(ATNode('Implicit Variable', value = 'IT'))
            self.nextToken('Implicit Variable')
        elif (self.current_token.type == 'Variable Identifier'):
            childNodes.append(ATNode('Variable Identifier', value = self.current_token.value))
            self.nextToken('Variable Identifier')
        elif (expression := self.expression(infAr)):
            childNodes.append(expression)
        else:
            return False
        
        return ATNode('Exprvar', children_nodes = childNodes)
    
    # grammar for literals
    def literal(self):
        childNodes = deque()
        nonStringLit = ['Numbar Literal', 'Numbr Literal', 'Troof Literal']
        if(self.current_token.type in nonStringLit):
            childNodes.append(ATNode(self.current_token.type, value = self.current_token.value))
            self.nextToken(self.current_token.type)
        elif(yarn_literal := self.yarn_literal()):
            childNodes.append(yarn_literal)
        else:
            return False
        
        return ATNode('Literal', children_nodes = childNodes)
    
    # grammar for a yarn literal (string)
    def yarn_literal(self):
        childNodes = deque()
        if (self.current_token.type == 'String Delimiter'):
            self.nextToken('String Delimiter')
            val = self.current_token.value
            self.nextToken('Yarn Literal')
            childNodes.append(ATNode('Yarn Literal', value = val))

            self.nextToken('String Delimiter')
        else:
            return False

        return ATNode('Yarn Literal', children_nodes = childNodes)

    # grammar for expressions
    def expression(self, infAr):
        childNodes = deque()
        if(add := self.binaryOp('Addition')):
            childNodes.append(add)
        elif(subtract := self.binaryOp('Subtraction')):
            childNodes.append(subtract)
        elif(mult := self.binaryOp('Multiplication')):
            childNodes.append(mult)
        elif(div := self.binaryOp('Division')):
            childNodes.append(div)
        elif(mod := self.binaryOp('Modulo')):
            childNodes.append(mod)
        elif(maxim := self.binaryOp('Max')):
            childNodes.append(maxim)
        elif(minim := self.binaryOp('Min')):
            childNodes.append(minim)
        elif(andOp := self.binaryOp('And')):
            childNodes.append(andOp)
        elif(orOp := self.binaryOp('Or')):
            childNodes.append(orOp)
        elif(xorOp := self.binaryOp('Xor')):
            childNodes.append(xorOp) 
        elif(notOp := self.unaryOp('Not')):
            childNodes.append(notOp)
        elif(eqCheck := self.binaryOp('Equality Check')):
            childNodes.append(eqCheck)
        elif(ineqCheck := self.binaryOp('Inequality Check')):
            childNodes.append(ineqCheck)
        elif(concat := self.infOp('Concatenate', False)):
            childNodes.append(concat)
        elif(infAr and (infAnd := self.infOp('Infinite And', True))):
            childNodes.append(infAnd)
        elif(infAr and (infOr := self.infOp('Infinite Or', True))):
            childNodes.append(infOr)
        elif(maek := self.maek()):
            childNodes.append(maek)
        else:
            return False
        
        return ATNode('Expression', children_nodes = childNodes)
    
    # grammar for binary operations, accepts operation
    def binaryOp(self, operation):
        childNodes = deque()
        if(self.current_token.type == operation):
            childNodes.append(ATNode(operation))
            self.nextToken(operation)
        else:
            return False
        
        if(exprvar := self.exprvar(True)):
            childNodes.append(exprvar)
        else:
            self.nextToken('Expression')
        
        self.nextToken('Operation Delimiter')

        if(exprvar := self.exprvar(True)):
            childNodes.append(exprvar)
        else:
            self.nextToken('Expression')
        
        return ATNode(operation, children_nodes = childNodes)
    
    # gramamr for unary operations
    def unaryOp(self, operation):
        childNodes = deque()
        if(self.current_token.type == operation):
            childNodes.append(ATNode(operation))
            self.nextToken(operation)
        else:
            return False
        
        if(exprvar := self.exprvar(True)):
            childNodes.append(exprvar)
        else:
            self.nextToken('Expression')
        
        return ATNode(operation, children_nodes = childNodes)
    
    # grammar for operations with infinite arity (smoosh, all of, any of)
    def infOp(self, operation, boolean):
        childNodes = deque()
        if(self.current_token.type == operation):
            childNodes.append(operation)
            self.nextToken(operation)
        else:
            return False

        if(boolean and (exprvar := self.exprvar(False))):
            childNodes.append(exprvar)
        elif(not boolean and (exprvar := self.exprvar(True))):
            childNodes.append(exprvar)
        else:
            self.nextToken('Expression')
        
        while self.current_token.type == 'Operation Delimiter':
            self.nextToken('Operation Delimiter')
            if(boolean and (exprvar := self.exprvar(False))):
                childNodes.append(exprvar)
            elif(not boolean and (exprvar := self.exprvar(True))):
                childNodes.append(exprvar)
            else:
                self.nextToken('Expression')

        # makes MKAY conditional for smoosh
        if(boolean):
            self.nextToken('Infinite Bool End')
        elif(self.current_token.type == 'Infinite Bool End'):
            self.nextToken('Infinite Bool End')

        return ATNode(operation, children_nodes = childNodes)

    # grammar for maek typecast expression
    def maek(self):
        childNodes = deque()
        if self.current_token.type == 'Maek Keyword':
            self.nextToken('Maek Keyword')
            childNodes.append(ATNode('Maek Keyword'))
        else:
            return False

        if(exprvar := self.exprvar(True)):
            childNodes.append(exprvar)
        else:
            self.nextToken('Expression')

        if self.current_token.type == 'A Keyword':
            self.nextToken('A Keyword')
        
        childNodes.append(ATNode('Data Type', value = self.current_token.value))
        self.nextToken('Data Type')

        return ATNode('Maek', children_nodes = childNodes)
    # ------------------------LITERALS/EXPRESISON/VARIABLE------------------------

    # ------------------------I/O------------------------
    # grammar for VISIBLE (print)
    def visible(self):
        childNodes = deque()
        if(self.current_token.type == 'Output Keyword'):
            self.nextToken('Output Keyword')
            childNodes.append(ATNode('Output Keyword'))
        else:
            return False
        
        childNodes.append(self.printNode())

        while(self.current_token.type != 'Comment Delimiter' and self.current_token.type != 'Linebreak'):
            if(self.current_token.type == 'Operation Delimiter'):
                self.nextToken('Operation Delimiter')
            childNodes.append(self.printNode())
        
        if self.current_token.type == 'Newline Supress':
            self.nextToken('Newline Supress')
            childNodes.append(ATNode('Newline Supress'))
        return ATNode('Output Statement', children_nodes = childNodes)

    # grammar for provided parameter for visible (what to print)
    def printNode(self):
        childNodes = deque()
        exprvar = self.exprvar(True)
        if(not exprvar):
            self.nextToken('Expression')
        childNodes.append(exprvar)
    
        return ATNode('Print Expressions', children_nodes = childNodes)
    
    # grammar for gimmeh
    def gimmeh(self):
        childNodes = deque()
        if(self.current_token.type == 'Input Keyword'):
            self.nextToken('Input Keyword')
            childNodes.append(ATNode('Gimmeh'))
        else:
            return False
        
        if self.current_token.type == 'Variable Identifier' or self.current_token.type == 'Implicit Variable':
            childNodes.append(ATNode(self.current_token.type, value = self.current_token.value))
            self.nextToken(self.current_token.type)
        else:
            self.nextToken('Variable Identifier')

        return ATNode('Input Statement', children_nodes = childNodes)
    # ------------------------I/O------------------------
    
    # ------------------------ASSIGNMENT------------------------
    # grammar for variable declaration
    def declaration(self):
        childNodes = deque()

        if(self.current_token.type == 'Variable Declaration'):
            childNodes.append(ATNode('Variable Declaration'))
            self.nextToken('Variable Declaration')
        else:
            return False
        
        childNodes.append(ATNode('Variable Identifier', value = self.current_token.value))
        self.nextToken('Variable Identifier')

        if self.current_token.type == 'Variable Assignment':
            self.nextToken('Variable Assignment')
            childNodes.append(ATNode('Variable Assignment'))

            if(exprvar := self.exprvar(True)):
                childNodes.append(exprvar)
            else:
                self.nextToken('Expression')
        
        return ATNode('Declaration Statement', children_nodes = childNodes)

    # grammar for variable assignment
    def assignment(self):
        childNodes = deque()
        if(self.current_token.type == 'Implicit Variable'):
            childNodes.append(ATNode('Implicit Variable', value = 'IT'))
            self.nextToken('Implicit Variable')
        elif(self.current_token.type == 'Variable Identifier'):
            childNodes.append(ATNode('Variable Identifier', value = self.current_token.value))
            self.nextToken('Variable Identifier')
        else:
            return False
        
        if self.current_token.type == 'Assignment':
            self.nextToken('Assignment')
            childNodes.append(ATNode('Assignment'))
        else:
            self.token_idx -= 1
            self.current_token = self.tokens[self.token_idx]
            return False

        if(exprvar := self.exprvar(True)):
            childNodes.append(exprvar)
        else:
            self.nextToken('Expression')
        
        return ATNode('Assignment Statement', children_nodes = childNodes)

    # grammar for typecasting (IS NOW A)
    def typecast(self):
        childNodes = deque()

        if(self.current_token.type == 'Variable Identifier'):
            childNodes.append(ATNode('Variable Identifier', value = self.current_token.value))
            self.nextToken('Variable Identifier')
        elif(self.current_token.type == 'Implicit Variable'):
            childNodes.append(ATNode('Implicit Variable', value = 'IT'))
            self.nextToken('Implicit Variable')
        else:
            return False
        
        if self.current_token.type == 'Typecast Keyword':
            self.nextToken('Typecast Keyword')
            childNodes.append(ATNode('Typecast Keyword'))
        else:
            self.token_idx -= 1
            self.current_token = self.tokens[self.token_idx]
            return False

        childNodes.append(ATNode('Data Type', value = self.current_token.value))
        self.nextToken('Data Type')

        return ATNode('Typecast Statement', children_nodes = childNodes)
    # ------------------------ASSIGNMENT------------------------

    # ------------------------CONTROL------------------------
    # grammar for a loop
    def loop(self):
        childNodes = deque()
        if(self.current_token.type == 'Loop Start'):
            childNodes.append(ATNode('Loop Start'))
            self.nextToken('Loop Start')
        else:
            return False
        
        childNodes.append(ATNode('Variable Identifier', value = self.current_token.value))
        temp = self.current_token.value         # for checking if identifier matches closing identifier
        self.nextToken('Variable Identifier')

        childNodes.append(ATNode('Loop Operation', value = self.current_token.value))
        self.nextToken('Loop Operation')

        self.nextToken('Loop Delimiter')
        childNodes.append(ATNode('Loop Delimiter'))
        
        if (self.current_token.type == 'Variable Identifier' or self.current_token.type == 'Implicit Variable'):
            childNodes.append(ATNode(self.current_token.type, value = self.current_token.value))
            self.nextToken(self.current_token.type)
        else:
            self.nextToken('Variable Identifier')

        if(self.current_token.type == 'Condition Keyword'):
            childNodes.append(ATNode('Condition Keyword', value = self.current_token.value))
            self.nextToken('Condition Keyword')
            if (not (expression := self.expression(True))):
                self.nextToken('Expression')
            childNodes.append(expression)
        
        self.nextToken('Linebreak')

        while(statement := self.statement(inProgBlock = True)):
            childNodes.append(statement)

        self.nextToken('Loop End')
        childNodes.append(ATNode('Loop End'))

        childNodes.append(ATNode('Variable Identifier', value = self.current_token.value))
        temp2 = self.current_token.value
        self.nextToken('Variable Identifier')

        if temp != temp2:
            raise Exception(f"Syntax Error:{self.current_token.line_num}:Expected matching loop name at {self.current_token.value}")

        return ATNode('Loop Statement', children_nodes = childNodes)

    # grammar for GTFO (break)
    def gtfo(self):
        childNodes = deque()
        if self.current_token.type == 'Break':
            childNodes.append(ATNode('Break'))
            self.nextToken('Break')
        else:
            return False
        
        return(ATNode('Break Statement', children_nodes = childNodes))
    
    # grammar for switch statements
    def switch(self):
        childNodes = deque()
        if self.current_token.type == 'Switch-case Start':
            childNodes.append(ATNode('Switch-case Start'))
            self.nextToken('Switch-case Start')
        else:
            return False
        
        self.nextToken('Linebreak')

        case = self.case()
        childNodes.append(case)

        while self.current_token.type == 'Case Keyword':
            case = self.case()
            childNodes.append(case)
        
        if self.current_token.type == 'Case Default Keyword':
            case = self.caseDefault()
            childNodes.append(case)
            
        self.nextToken('If-else End')
        childNodes.append(ATNode('If-else End'))

        return ATNode('Switch Statement', children_nodes = childNodes)

    # grammar for cases in switch
    def case(self):
        
        childNodes = deque()

        self.nextToken('Case Keyword')
        childNodes.append(ATNode('Case Keyword'))

        if(literal := self.literal()):
            childNodes.append(literal)
        else:
            self.nextToken('Literal')
        
        self.nextToken('Linebreak')
        
        while(statement := self.statement(inProgBlock = True)):
            childNodes.append(statement)
        
        return ATNode('Case', children_nodes = childNodes)

    # gramamr for the default case (OMGWTF)
    def caseDefault(self):
        childNodes = deque()

        self.nextToken('Case Default Keyword')
        childNodes.append(ATNode('Case Default Keyword'))

        self.nextToken('Linebreak')

        while(statement := self.statement(inProgBlock = True)):
            childNodes.append(statement)
        
        return ATNode('Default Case', children_nodes = childNodes)
    
    # grammar for if-else block
    def ifElse(self):
        childNodes = deque()

        if(self.current_token.type == 'If-else Start'):
            self.nextToken('If-else Start')
            childNodes.append(ATNode('If-else Start'))
        else:
            return False
        
        self.nextToken('Linebreak')
        
        ifBlock = self.ifBlock()
        childNodes.append(ifBlock)

        while self.current_token.type == 'Else-if Keyword':
            mebbe = self.mebbe()
            childNodes.append(mebbe)

        if self.current_token.type == 'Else Keyword':
            elseBlock = self.elseBlock()
            childNodes.append(elseBlock)

        self.nextToken('If-else End')
        childNodes.append(ATNode('If-else End'))
        return(ATNode('If-else Statement', children_nodes = childNodes))

    # grammar for the ya rly block
    def ifBlock(self):
        childNodes = deque()

        self.nextToken('If Keyword')
        childNodes.append(ATNode('If Keyword'))

        self.nextToken('Linebreak')

        while(statement := self.statement(inProgBlock = True)):
            childNodes.append(statement)

        return ATNode('If', children_nodes = childNodes)

    # grammar for no wai block
    def elseBlock(self):
        childNodes = deque()
        self.nextToken('Else Keyword')
        childNodes.append(ATNode('Else Keyword'))

        self.nextToken('Linebreak')

        while(statement := self.statement(inProgBlock = True)):
            childNodes.append(statement)
        
        return ATNode('Else', children_nodes = childNodes)

    # grammar for else-if block
    def mebbe(self):
        childNodes = deque()

        self.nextToken('Else-if Keyword')
        childNodes.append(ATNode('Else-if Keyword'))

        if(exprvar := self.exprvar(True)):
            childNodes.append(exprvar)
        else:
            self.nextToken('Expression')

        self.nextToken('Linebreak')

        while(statement := self.statement(inProgBlock = True)):
            childNodes.append(statement)
        
        return ATNode('Else-if', children_nodes = childNodes)

    # ------------------------CONTROL------------------------

    # ------------------------MAIN------------------------
    # grammar for multiline comments
    def multiComment(self):
        childNodes = deque()

        self.nextToken('Multiline Comment Start')
        childNodes.append(ATNode('Multiline Comment Start'))
        
        while(self.current_token.type == 'Comment' or self.current_token.type == 'Linebreak'):
            if self.token_idx + 1 > len(self.tokens):
                break
            self.nextToken(self.current_token.type)
            childNodes.append(ATNode(self.current_token.type))
        
        self.nextToken('Multiline Comment End')
        childNodes.append(ATNode('Multiline Comment End'))
        return ATNode('Multiline Comment', children_nodes = childNodes)
    
    # grammar for statements
    # inProgBlock checks if the current statement is within a code block - avoide declaring a statement inside
    # a code block (switch, if-else, loops)
    def statement(self, inProgBlock = False):
        childNodes = deque()

        if(visible := self.visible()):
            childNodes.append(visible)
        elif(assignment := self.assignment()):
            childNodes.append(assignment)
        elif(typecast := self.typecast()):
            childNodes.append(typecast)
        elif(exprvar := self.exprvar(True)):
            childNodes.append(exprvar)
        elif(gimmeh := self.gimmeh()):
            childNodes.append(gimmeh)
        elif(loop := self.loop()):
            childNodes.append(loop)
        elif(gtfo := self.gtfo()):
            childNodes.append(gtfo)
        elif(switch := self.switch()):
            childNodes.append(switch)
        elif(not inProgBlock and (declaration := self.declaration())):
            childNodes.append(declaration)
        elif(if_else := self.ifElse()):
            childNodes.append(if_else)
        elif(self.current_token.type == 'Multiline Comment Start'):
            childNodes.append(self.multiComment())
        else:
            if(self.current_token.type == 'Comment Delimiter'):
                self.nextToken('Comment Delimiter')
                childNodes.append(ATNode('Comment Delimiter'))
                self.nextToken('Comment')
                childNodes.append(ATNode('Comment'))
            elif(self.current_token.type == 'Linebreak'):
                self.nextToken('Linebreak')
                childNodes.append(ATNode('Linebreak'))
                return ATNode('Ignore')
            else:
                return False
        if(self.current_token.type == 'Comment Delimiter'):
            self.nextToken('Comment Delimiter')
            self.nextToken('Comment')

        self.nextToken('Linebreak')
        return ATNode('Statement', children_nodes = childNodes)
    
    # grammar for a lol code
    def lolProgram(self):
        treeNode = deque()          # symbol tree

        # checks syntax before HAI
        while(self.current_token.type != 'Code Start' and self.token_idx + 1 < len(self.tokens)):
            if self.current_token.type == 'Comment Delimiter':
                self.nextToken('Comment Delimiter')
                treeNode.append(ATNode('Comment Delimiter'))
                self.nextToken('Comment')
                self.nextToken('Linebreak')
            elif(self.current_token.type == 'Multiline Comment Start'):
                treeNode.append(self.multiComment())
            elif(self.current_token.type == 'Linebreak'):
                self.nextToken('Linebreak')
                treeNode.append(ATNode('Linebreak'))
            else:
                self.nextToken('Code Start')

        # HAI
        self.nextToken('Code Start')
        treeNode.append(ATNode('Code Start'))
        
        # checks if the version exists
        if (self.current_token.type == 'Numbar Literal' or self.current_token.type == 'Numbr Literal'):
            self.nextToken(self.current_token.type)
        
        self.nextToken('Linebreak')

        # Code Body
        while(statement := self.statement()):
            treeNode.append(statement)
        
        # KTHXBYE
        self.nextToken('Code End')
        treeNode.append(ATNode('Code End'))

        # checks syntax after KTHXBYE
        while(self.token_idx < len(self.tokens)):
            if self.current_token.type == 'Comment Delimiter':
                self.nextToken('Comment Delimiter')
                treeNode.append(ATNode('Comment Delimiter'))
                self.nextToken('Comment')
                self.nextToken('Linebreak')
            elif(self.current_token.type == 'Multiline Comment Start'):
                treeNode.append(self.multiComment())
            elif(self.current_token.type == 'Linebreak'):
                self.nextToken('Linebreak')
                treeNode.append(ATNode('Linebreak'))
            else:
                self.nextToken('End of File')

        return ATNode('LOLProgram', children_nodes = treeNode)
    # ------------------------MAIN------------------------