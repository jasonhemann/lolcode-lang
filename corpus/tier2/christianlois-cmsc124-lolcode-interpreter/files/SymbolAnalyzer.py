# Author: Christian Olo
# Program Description: A LOLCode interpreter developed using python

# source code for the semantic analyzer

from Symbol import Symbol                   # uses the symbol class to store valid symbol objects
import math
import re

class SymbolAnalyzer:
    def __init__(self, atnode_tree, stdin = []):
        self.atnode_tree = atnode_tree
        self.symbol_table = {'IT': Symbol('Noob', value = None)}
        self.stdin = stdin                                          # pre-defined user inputs
        self.output = ''                                            # stores the stdout
        self.err = ''                           
        self.line_number = 1

    # main function to start the analyzer
    def analyze(self):
        for node in self.atnode_tree.children_nodes:
            if node.type == 'Statement':
                self.analyzeStatement(node.children_nodes)
                self.line_number += 1
            elif node.type == 'Multiline Comment':
                self.line_number += len(node.children_nodes) - 1
            else:
                self.line_number += 1 
        
        return self.symbol_table, self.output
    
    # analyzes a statement
    def analyzeStatement(self, node):
        statement = node[0]
        if statement.type == 'Output Statement':
            self.visible(statement)
        elif statement.type == 'Assignment Statement':
            self.assignment(statement)
        elif statement.type == 'Typecast Statement':
            self.cast(statement)
        elif statement.type == 'Exprvar':
            self.expression(statement)
        elif statement.type == 'Input Statement':
            self.gimmeh(statement)
        elif statement.type == 'Loop Statement':
            self.loop(statement)
        elif statement.type == 'Switch Statement':
            self.switch(statement)
        elif statement.type == 'Declaration Statement':
            self.declaration(statement)
        elif statement.type == 'If-else Statement':
            return self.ifElse(statement)
        elif statement.type == 'Multiline Comment':
            self.line_number += len(statement.children_nodes)
        elif statement.type == 'Break Statement':
            return 1

        return 0

    # analyzes visible statement
    def visible(self, statement):
        printNodes = list(statement.children_nodes)[1:]
        toPrint = ''
        # iteratively checks the provided to be printed values for visible
        for i in printNodes:
            expression = i.children_nodes[0]
            expValue = self.getValue(expression.children_nodes[0])
            if expValue.type != 'Yarn Literal':
                expValue = self.strTypecast(expValue)
            toPrint += expValue.value
        self.output += toPrint + '\n'           # stores the result to later print to the GUI terminal

    # analyzes declaration statement
    def declaration(self, statement):
        variable = statement.children_nodes[1].value

        if len(statement.children_nodes) > 2:       # value is initialized
            value = self.getValue(statement.children_nodes[3].children_nodes[0])    # gets the value of the expression
            self.symbol_table[variable] = Symbol(value.type, value.value)
        else:
            self.symbol_table[variable] = Symbol('Noob')    # set as None
    
    # analyzes input statements (uses stdin)
    def gimmeh(self, statement):
        variable = statement.children_nodes[1].value
        self.lookup(variable)       # checks if the variable is declared
        # uses the value provided in stdin
        if len(self.stdin) > 0:
            temp = self.stdin[0]
            self.stdin.pop(0)
        else:
            temp = ''
        # typecasts numeric value to float or int
        try:
            self.symbol_table[variable] = self.numTypecast(Symbol('Yarn Literal', temp))
        except:
            self.symbol_table[variable] = Symbol('Yarn Literal', temp)

    # analyzes assignment statement
    def assignment(self, statement):
        variable = statement.children_nodes[0].value
        self.lookup(variable)
        value = self.getValue(statement.children_nodes[2].children_nodes[0])
        self.symbol_table[variable] = value
    
    # analyzes expressions
    def expression(self, statement):
        value = self.getValue(statement.children_nodes[0])
        self.symbol_table['IT'] = value

    # analyzes typecase (IS NOW A) statement
    def cast(self, statement):
        variable = statement.children_nodes[0].value
        self.lookup(variable)
        value = self.symbol_table[variable]
        dataType = statement.children_nodes[2].value
        newValue = self.typecast(value, dataType)

        self.symbol_table[variable] = newValue

    # analyzes loop statement
    def loop(self, statement):
        operation = statement.children_nodes[2].value   # uppin/nerfin
        variable = statement.children_nodes[4].value    # variable to change
        self.lookup(variable)

        # typecasts the value to numerical types if not numbr or numbar
        if self.symbol_table[variable].type != 'Numbr Literal' and self.symbol_table[variable].type != 'Numbar Literal':
            self.symbol_table[variable] = self.numTypecast(self.symbol_table[variable])
        
        condition = False
        expression = None
        
        stIdx = 5

        # checks if there is a provided condition
        if statement.children_nodes[5].type == 'Condition Keyword':
            condition = statement.children_nodes[5].value
            expressionNode = statement.children_nodes[6]
            expression = self.evaluateExpression(expressionNode.children_nodes[0])
            stIdx = 7
        
        self.line_number += 1

        # code block
        statements = list(statement.children_nodes)[stIdx:]

        temp = self.symbol_table[variable].value
        stopExec = False

        tempLine = self.line_number
        init = True
        while True:
            # checks condition, breaks if condition is met
            if condition == 'TIL' or condition == 'WILE':
                expression = self.evaluateExpression(expressionNode.children_nodes[0])
                if expression.type != 'Troof Literal':
                    expression = self.boolTypecast(expression)
                if ((condition == 'TIL' and expression.value == 'WIN') or
                (condition == 'WILE' and expression.value == 'FAIL')):
                    break

            # analyzes statements within the loop
            for statement in statements:
                if statement.type == 'Loop End':
                    break
                if not statement.children_nodes:
                    self.line_number += 1 if init else 0
                    continue
                if self.analyzeStatement(statement.children_nodes):
                    stopExec = True
                    self.line_number += 1 if init else 0
                    break
                self.line_number += 1 if init else 0

            if stopExec:
                break
            if operation == 'UPPIN':
                temp += 1
            elif operation == 'NERFIN':
                temp -= 1
            self.symbol_table[variable] = Symbol(self.symbol_table[variable].type, temp)
            init = False
        self.line_number = tempLine + len(statements) - 2

    # analyzes switch statements
    def switch(self, statement):
        temp = self.symbol_table['IT'].value
        cases = list(statement.children_nodes)[1:]
        self.line_number += 1
        i = 0
        matched = False

        # analyzes the cases
        while cases[i].type == 'Case':
            omg = cases[i]
            value = self.getValue(omg.children_nodes[1])

            if value.value == temp:
                matched = True
                break
            self.line_number += len(omg.children_nodes) - 1
            i += 1
        
        # if a case is matched
        if matched:
            tempLine = self.line_number
            statements = list(cases[i].children_nodes)[2:]
            for statement in statements:
                if not statement.children_nodes:
                    self.line_number += 1
                    continue
                status = self.analyzeStatement(statement.children_nodes)
                self.line_number += 1
                if status == 1:
                    break
            self.line_number = tempLine + len(cases[i].children_nodes) - 1
            i += 1
            while cases[i].type == 'Case' or cases[i].type == 'Default Case':
                self.line_number += len(cases[i].children_nodes) - 1 if cases[i].type == 'Case' else len(cases[i].children_nodes)
                i += 1
        elif cases[-2].type == 'Default Case':              # default case
            tempLine = self.line_number
            statements = list(cases[-2].children_nodes)[1:]
            for statement in statements:
                if not statement.children_nodes:
                    self.line_number += 1
                    continue
                status = self.analyzeStatement(statement.children_nodes)
                self.line_number += 1
                if status == 1:
                    break
            self.line_number = tempLine + len(cases[-2].children_nodes)

    # analyzes ifElse statements
    def ifElse(self, statement):
        temp = self.symbol_table['IT']
        
        if temp.type != 'Troof Literal':
            temp = self.boolTypecast(temp)
        
        self.line_number += 1

        status = 0

        # ya rly
        if temp.value == 'WIN':
            block = statement.children_nodes[1]
            self.line_number += 1

            statements = list(block.children_nodes)[1:]
            for s in statements:
                if not s.children_nodes:
                    self.line_number += 1
                    continue
                status = self.analyzeStatement(s.children_nodes)
                self.line_number += 1
            i = 2
            while statement.children_nodes[i].type == 'Else-if' or statement.children_nodes[i].type == 'Else':
                self.line_number += len(statement.children_nodes[i].children_nodes) - 1 if statement.children_nodes[i].type == 'Else-if' else len(statement.children_nodes[i].children_nodes)
                i += 1
        else:
            self.line_number += len(statement.children_nodes[1].children_nodes)
            i = 2
            matched = False
            # mebbe
            while statement.children_nodes[i].type == 'Else-if':
                conditionNode = statement.children_nodes[i].children_nodes[1]
                condition = self.getValue(conditionNode.children_nodes[0])

                if condition.type != 'Troof Literal':
                    condition = self.boolTypecast(condition)

                if condition.value == 'WIN':
                    self.line_number += 1
                    matched = True
                    block = statement.children_nodes[i]
                    statements = list(block.children_nodes)[2:]
                    for s in statements:
                        if not s.children_nodes:
                            self.line_number += 1
                            continue
                        status = self.analyzeStatement(s.children_nodes)
                        self.line_number += 1
                    j = i+1
                    while statement.children_nodes[j].type == 'Else-if' or statement.children_nodes[j].type == 'Else':
                        self.line_number += len(statement.children_nodes[j].children_nodes) - 1 if statement.children_nodes[j].type == 'Else-if' else len(statement.children_nodes[j].children_nodes)
                        j += 1
                    break
                else:
                    self.line_number += len(statement.children_nodes[i].children_nodes) - 1
                i += 1
            if not matched:
                if statement.children_nodes[i].type == 'Else':  # else
                    block = statement.children_nodes[i]
                    statements = list(block.children_nodes)[1:]
                    for s in statements:
                        if not s.children_nodes:
                            self.line_number += 1
                            continue
                        status = self.analyzeStatement(s.children_nodes)
                        self.line_number += 1
        return status
    # --------------------Getting Values of expresison/literal/variable-------------------
    # gets the value of an expression, literal, or variable, return a symbol
    def getValue(self, expression):
        expType = expression

        if expType.type == 'Literal':
            litType = expType.children_nodes[0]
            if litType.type == 'Yarn Literal':
                return Symbol('Yarn Literal', litType.children_nodes[0].value)
            elif litType.type == 'Numbr Literal':
                return Symbol(litType.type, int(litType.value))
            elif litType.type == 'Numbar Literal':
                return Symbol(litType.type, float(litType.value))
            else:
                return Symbol(litType.type, litType.value)
        elif expType.type == 'Variable Identifier' or expType.type == 'Implicit Variable':
            variable = expType.value
            self.lookup(variable)
            return self.symbol_table[variable]
        else:       # expression
            return self.evaluateExpression(expType.children_nodes[0])
    
    # evaulates an expression
    def evaluateExpression(self, expression):
        if (expression.type == 'Addition' or 
        expression.type == 'Subtraction' or
        expression.type == 'Multiplication' or
        expression.type == 'Division' or
        expression.type == 'Modulo' or
        expression.type == 'Min' or
        expression.type == 'Max'):
            return self.arithmetic(expression)
        elif (expression.type == 'And' or
        expression.type == 'Or' or
        expression.type == 'Xor' or
        expression.type == 'Not'):
            return self.boolean(expression)
        elif (expression.type == 'Infinite And' or
        expression.type == 'Infinite Or'):
            return self.infBoolean(expression)
        elif (expression.type == 'Equality Check' or
        expression.type == 'Inequality Check'):
            return self.comparison(expression)
        elif (expression.type == 'Concatenate'):
            return self.smoosh(expression)
        elif (expression.type == 'Maek'):
            return self.maek(expression)
    
    # evaulates arithmetic operation
    def arithmetic(self, expression):
        operands = expression.children_nodes
        op1Exp = self.getValue(operands[1].children_nodes[0])
        op2Exp = self.getValue(operands[2].children_nodes[0])

        # typcasts operands if not numeric type
        if op1Exp.type != 'Numbr Literal' and op1Exp.type != 'Numbar Literal':
            temp = self.numTypecast(op1Exp)
            op1 = temp.value
        else:
            op1 = op1Exp.value
        if op2Exp.type != 'Numbr Literal' and op2Exp.type != 'Numbar Literal':
            temp = self.numTypecast(op2Exp)
            op2 = temp.value
        else:
            op2 = op2Exp.value

        if expression.type == 'Addition':
            ans = op1 + op2
        elif expression.type == 'Subtraction':
            ans = op1 - op2
        elif expression.type == 'Multiplication':
            ans = op1 * op2
        elif expression.type == 'Division':
            if op1Exp.type == 'Numbr Literal' and op2Exp.type == 'Numbr Literal':
                ans = op1 // op2
            else:
                ans = op1 / op2
        elif expression.type == 'Modulo':
            ans = op1 % op2
        elif expression.type == 'Max':
            ans = max(op1, op2)
        elif expression.type == 'Min':
            ans = min(op1, op2)

        if isinstance(ans, int):
            return Symbol('Numbr Literal', ans)
        else:
            return Symbol('Numbar Literal', ans)

    # evaulates boolean expressions
    def boolean(self, expression):
        operands = expression.children_nodes
        op1Exp = self.getValue(operands[1].children_nodes[0])

        # typecasting if necessary
        if op1Exp.type == 'Troof Literal':
            if op1Exp.value == 'WIN':
                op1 = True
            else:
                op1 = False
        else:
            temp = self.boolTypecast(op1Exp)
            if temp.value == 'WIN':
                op1 = True
            else:
                op1 = False
        if expression.type != 'Not':
            op2Exp = self.getValue(operands[2].children_nodes[0])
            if op2Exp.type == 'Troof Literal':
                if op2Exp.value == 'WIN':
                    op2 = True
                else:
                    op2 = False
            else:
                temp = self.boolTypecast(op2Exp)
                if temp.value == 'WIN':
                    op2 = True
                else:
                    op2 = False
        
        if expression.type == 'And':
            ans = op1 and op2
        elif expression.type == 'Or':
            ans = op1 or op2
        elif expression.type == 'Not':
            ans = not op1
        elif expression.type == 'Xor':
            ans = op1 ^ op2
        
        if ans == True:
            return Symbol('Troof Literal', 'WIN')
        else:
            return Symbol('Troof Literal', 'FAIL')

    # evaluate all of an any of
    def infBoolean(self, expression):
        operations = list(expression.children_nodes)[2:]

        res = self.getValue(expression.children_nodes[1].children_nodes[0])
        if res.type != 'Troof Literal':
            res = self.boolTypecast(res)
        if res.value == 'WIN':
            ans = True
        else:
            ans = False
        for op in operations:
            res = self.getValue(op.children_nodes[0])
            if res.type != 'Troof Literal':
                res = self.boolTypecast(res)
            if res.value == 'WIN':
                temp = True
            else:
                temp = False
            if expression.type == 'Infinite And':
                ans = ans and temp
            else:
                ans = ans or temp
        
        if ans == True:
            return Symbol('Troof Literal', 'WIN')
        else:
            return Symbol('Troof Literal', 'FAIL')

    # evaluates smoosh operation
    def smoosh(self, expression):
        operations = list(expression.children_nodes)[1:]

        toConcat = ''
        for op in operations:
            temp = self.getValue(op.children_nodes[0])
            if temp.type != 'Yarn Literal':
                temp = self.strTypecast(temp)
            toConcat += temp.value
        
        return Symbol('Yarn Literal', value = toConcat)

    # analyze comparison expressions
    def comparison(self, expression):
        operands = expression.children_nodes
        op1Exp = self.getValue(operands[1].children_nodes[0])
        op2Exp = self.getValue(operands[2].children_nodes[0])

        if op1Exp.type == 'Troof Literal':
            op1 = True
        else:
            op1 = op1Exp.value
        
        if op2Exp.type == 'Troof Literal':
            op2 = True
        else:
            op2 = op2Exp.value

        if expression.type == 'Equality Check':
            ans = op1 == op2
        elif expression.type == 'Inequality Check':
            ans = op1 != op2

        if ans == True:
            return Symbol('Troof Literal', 'WIN')
        else:
            return Symbol('Troof Literal', 'FAIL')
    
    # evaluates maek expression (explicit typecasting)
    def maek(self, expression):
        value = self.getValue(expression.children_nodes[1].children_nodes[0])
        dataType = expression.children_nodes[2].value
        return self.typecast(value, dataType)
    # --------------------Getting Values of expresison/literal/variable-------------------

    # --------------------Implicit typecasting-------------------
    # typecast a value to boolean
    def boolTypecast(self, expression):
        if expression.type == 'Yarn Literal':
            if expression.value == '':
                return Symbol('Troof Literal', 'FAIL')
            else:
                return Symbol('Troof Literal', 'WIN')
        elif expression.type == 'Numbr Literal' or expression.type == 'Numbar Literal':
            if float(expression.value) == 0:
                return Symbol('Troof Literal', 'FAIL')
            else:
                return Symbol('Troof Literal', 'WIN')
        elif expression.type == 'Noob':
            return Symbol('Troof Literal', 'FAIL')
        else:
            self.err = f"Semantic Error:{self.line_number}: {expression.value} cannot be typecasted to TROOF"
            raise Exception()
    
    # typecasts a value to numerical type
    def numTypecast(self, expression):
        if expression.type == 'Yarn Literal':
            if re.match(r"-?[0-9]+\.[0-9]+$", expression.value):
                return Symbol('Numbar Literal', float(expression.value))
            elif re.match(r"-?[0-9]+$", expression.value):
                return Symbol('Numbr Literal', int(expression.value))
            else:
                self.err = f"Semantic Error:{self.line_number}: {expression.value} cannot be typecasted to numerical data type"
                raise Exception()
        elif expression.type == 'Troof Literal':
            if expression.value == 'WIN':
                return Symbol('Numbr Literal', 1)
            else:
                return Symbol('Numbr Literal', 0)
        else:
            self.err = f"Semantic Error:{self.line_number}: {expression.value} cannot be typecasted to numerical data type"
            raise Exception()

    # typecasts the value to a string (yarn)
    def strTypecast(self, expression):
        if expression.type == 'Numbr Literal':
            return Symbol('Yarn Literal', str(expression.value))
        elif expression.type == 'Numbar Literal':
            return Symbol('Yarn Literal', str(math.floor(expression.value*100)/100))
        elif expression.type == 'Troof Literal':
            return Symbol('Yarn Literal', expression.value)
        else:
            self.err = f"Semantic Error:{self.line_number}: {expression.value} cannot be typecasted to YARN"
            raise Exception()
    # --------------------Implicit typecasting-------------------

    # --------------------Explicit typecasting-------------------
    # symbol is the to be typecasted and data type is the target data type
    def typecast(self, symbol, dataType):
        if symbol.type == 'Noob':
            if dataType == 'NUMBR':
                return Symbol('Numbr Literal', 0)
            elif dataType == 'NUMBAR':
                return Symbol('Numbar Literal', 0.0)
            elif dataType == 'YARN':
                return Symbol('Yarn Literal', '')
            elif dataType == 'TROOF':
                return Symbol('Troof Literal', 'FAIL')
            elif dataType == 'NOOB':
                return symbol
        elif symbol.type == 'Troof Literal':
            if dataType == 'NUMBR':
                temp = 1 if symbol.value == 'WIN' else 0
                return Symbol('Numbr Literal', temp)
            elif dataType == 'NUMBAR':
                temp = 1.0 if symbol.value == 'WIN' else 0.0
                return Symbol('Numbar Literal', temp)
            elif dataType == 'YARN':
                return Symbol('Yarn Literal', symbol.value)
            elif dataType == 'TROOF':
                return symbol
            else:
                self.err = f"Semantic Error:{self.line_number}: {symbol.value} cannot be typecasted to {dataType}"
                raise Exception()
        elif symbol.type == 'Numbar Literal':
            if dataType == 'NUMBR':
                return Symbol('Numbr Literal', int(symbol.value))
            elif dataType == 'YARN':
                return Symbol('Yarn Literal', str(math.floor(symbol.value*100)/100))
            elif dataType == 'TROOF':
                temp = 'WIN' if symbol.value != 0 else 'FAIL'
                return Symbol('Troof Literal', temp)
            elif dataType == 'NUMBAR':
                return symbol
            else:
                self.err = f"Semantic Error:{self.line_number}: {symbol.value} cannot be typecasted to {dataType}"
                raise Exception()
        elif symbol.type == 'Numbr Literal':
            if dataType == 'NUMBAR':
                return Symbol('Numbar Literal', float(symbol.value))
            elif dataType == 'YARN':
                return Symbol('Yarn Literal', str(symbol.value))
            elif dataType == 'TROOF':
                temp = 'WIN' if symbol.value != 0 else 'FAIL'
                return Symbol('Troof Literal', temp)
            elif dataType == 'NUMBR':
                return symbol
            else:
                self.err = f"Semantic Error:{self.line_number}: {symbol.value} cannot be typecasted to {dataType}"
                raise Exception()
        elif symbol.type == 'Yarn Literal':
            if dataType == 'NUMBAR':
                if re.match(r"-?[0-9]+\.[0-9]+$", symbol.value) or re.match(r"-?[0-9]+$", symbol.value):
                    return Symbol('Numbar Literal', float(symbol.value))
                else:
                    self.err = f"Semantic Error:{self.line_number}: {symbol.value} cannot be typecasted to {dataType}"
                    raise Exception()
            elif dataType == 'NUMBR':
                if re.match(r"-?[0-9]+$", symbol.value):
                    return Symbol('Numbr Literal', int(symbol.value))
                else:
                    self.err = f"Semantic Error:{self.line_number}: {symbol.value} cannot be typecasted to {dataType}"
                    raise Exception()
            elif dataType == 'YARN':
                return symbol
            elif dataType == 'TROOF':
                if symbol.value == '':
                    return Symbol('Troof Literal', 'FAIL')
                else:
                    return Symbol('Troof Literal', 'WIN')
            else:
                self.err = f"Semantic Error:{self.line_number}: {symbol.value} cannot be typecasted to {dataType}"
                raise Exception()
    # --------------------Explicit typecasting-------------------

    # --------------------Utils-------------------
    # checks if a variable is declared
    def lookup(self, key):
        if key in self.symbol_table.keys():
            return
        
        self.err = f"Semantic Error:{self.line_number}: Variable \'{key}\' not declared"
        raise Exception()
    # --------------------Utils-------------------