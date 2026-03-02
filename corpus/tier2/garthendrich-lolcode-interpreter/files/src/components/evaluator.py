from copy import deepcopy

import easygui

from .token_enum import TOKEN
from .utils import isEmpty, toNumber


class Evaluator:
    def evaluate(self, sourceCode, tokens):
        self.currentLineNumber = 1
        self.sourceCodeLines = sourceCode.split("\n")
        self.tokens = tokens

        self.memory = {}
        self.memoryStack = []
        self.outputBuffer = ""

        self.canGTFO = False

        return self._Program()

    def _nextTokenIs(self, tokenType):
        if isEmpty(self.tokens):
            return None

        return self.tokens[0].lexemeType == tokenType

    def _popNextToken(self):
        if isEmpty(self.tokens):
            return None

        self._updateCurrentLineNumber()

        return self.tokens.pop(0)

    def _updateCurrentLineNumber(self):
        if self._nextTokenIs(TOKEN.LINEBREAK):
            self.currentLineNumber += 1

    def _expectNextToken(self, tokenType, errorMessage):
        if self._nextTokenIs(tokenType):
            self._popNextToken()
        else:
            self._throwError(SyntaxError, errorMessage)

    def _assign(self, identifier, value):
        self.memory[identifier] = value

    def _getValue(self, identifier):
        if identifier in self.memory:
            return self.memory.get(identifier)

        self._throwError(NameError, f"{identifier} is not defined")

    def _enterNewScope(self):
        self.memoryStack.append(deepcopy(self.memory))

    def _exitCurrentScope(self):
        self.memory = self.memoryStack.pop()

    def _throwError(self, errorType, message):
        errorArgs = (
            None,
            self.currentLineNumber,
            0,  # not yet implemented
            self.sourceCodeLines[self.currentLineNumber - 1],
        )

        raise errorType(message, errorArgs)

    def _Program(self):

        while self._nextTokenIs(TOKEN.LINEBREAK):
            self._popNextToken()

        self._expectNextToken(TOKEN.CODE_DELIMITER, 'Missing starting keyword "HAI"')

        self._expectNextToken(TOKEN.LINEBREAK, "Missing linebreak")
        while self._nextTokenIs(TOKEN.LINEBREAK):
            self._popNextToken()

        self._Statements()

        self._expectNextToken(TOKEN.CODE_DELIMITER, 'Missing ending keyword "KTHXBYE"')

    def _Statements(self):
        statement = (
            self._Declaration()
            or self._Output()
            or self._RecastingStatement()
            or self._AssignmentStatement()
            or self._LoopStatement()
            or self._Input()
            or self._IfStatement()
            or self._CaseStatement()
            or self._BreakStatement()
        )

        if statement is None:
            statement = self._Operand()
            if statement is not None:
                self._assign(TOKEN.IT_VARIABLE, statement)

        if statement is not None:

            self._expectNextToken(TOKEN.LINEBREAK, "Expected linebreak")
            while self._nextTokenIs(TOKEN.LINEBREAK):
                self._popNextToken()

            self._Statements()

    def _Declaration(self):
        if self._nextTokenIs(TOKEN.VARIABLE_DECLARATION):
            self._popNextToken()

            if self._nextTokenIs(TOKEN.VARIABLE_IDENTIFIER):
                variableIdentifierToken = self._popNextToken()
                variableIdentifier = variableIdentifierToken.lexeme
                value = None

                if self._nextTokenIs(TOKEN.VARIABLE_ASSIGNMENT):
                    self._popNextToken()

                    value = self._Operand()
                    if value is None:
                        self._throwError(SyntaxError, "Expected an expression")

                self._assign(variableIdentifier, value)
                return True

            self._throwError(SyntaxError, "Expected a variable identifier")

        return None

    def _Output(self):
        if self._nextTokenIs(TOKEN.OUTPUT_KEYWORD):
            self._popNextToken()

            value = self._Operand()
            if value is None:
                self._throwError(SyntaxError, "Expected an operand")

            self._output(value)

            while not self._nextTokenIs(TOKEN.LINEBREAK):
                if self._nextTokenIs(TOKEN.OPERAND_SEPARATOR):
                    self._popNextToken()

                value = self._Operand()
                if value is None:
                    self._throwError(SyntaxError, "Expected an operand")

                self._output(value)

            self._output("\n")

            return True

        return None

    def _output(self, value):
        self.outputBuffer += self._typeCast("YARN", value)

    def _Input(self):
        children = []

        if self._nextTokenIs(TOKEN.INPUT_KEYWORD):
            self._popNextToken()

            if self._nextTokenIs(TOKEN.VARIABLE_IDENTIFIER):
                variableIdentifierToken = self._popNextToken()
                variableIdentifier = variableIdentifierToken.lexeme

                value = easygui.enterbox(self.outputBuffer)
                self._assign(variableIdentifier, value)

                self._output(value)
                self._output("\n")

                return True

        return None

    def _Operand(self):
        literalValue = self._Literal()
        if literalValue is not None:
            return literalValue

        if self._nextTokenIs(TOKEN.VARIABLE_IDENTIFIER):
            identifierToken = self._popNextToken()
            return self._getValue(identifierToken.lexeme)

        operationValue = self._TwoOperandOperation()
        if operationValue is not None:
            return operationValue

        operationValue = self._NotOperation()
        if operationValue is not None:
            return operationValue

        operationValue = self._MultipleOperandOperation()
        if operationValue is not None:
            return operationValue

        explicitTypecast = self._ExplicitTypecast()
        if explicitTypecast is not None:
            return explicitTypecast

        return None

    def _Literal(self):
        if self._nextTokenIs(TOKEN.BOOL_LITERAL):
            boolToken = self._popNextToken()
            return True if boolToken.lexeme == "WIN" else False

        if self._nextTokenIs(TOKEN.FLOAT_LITERAL):
            integerToken = self._popNextToken()
            return float(integerToken.lexeme)

        if self._nextTokenIs(TOKEN.INTEGER_LITERAL):
            integerToken = self._popNextToken()
            return int(integerToken.lexeme)

        if self._nextTokenIs(TOKEN.STRING_LITERAL):
            stringToken = self._popNextToken()

            return stringToken.lexeme[1:-1]  # remove quotes

        if self._nextTokenIs(TOKEN.TYPE_LITERAL):
            typeToken = self._popNextToken()
            return typeToken.lexeme  # !!! ?????

        return None

    def _operate(self, operationToken, a, b):
        try:
            if operationToken.lexemeType == TOKEN.ADDITION_OPERATION:
                return toNumber(a) + toNumber(b)
            if operationToken.lexemeType == TOKEN.SUBTRACTION_OPERATION:
                return toNumber(a) - toNumber(b)
            if operationToken.lexemeType == TOKEN.MULTIPLICATION_OPERATION:
                return toNumber(a) * toNumber(b)
            if operationToken.lexemeType == TOKEN.QUOTIENT_OPERATION:
                return toNumber(a) / toNumber(b)
            if operationToken.lexemeType == TOKEN.MODULO_OPERATION:
                return toNumber(a) % toNumber(b)
            if operationToken.lexemeType == TOKEN.MAX_OPERATION:
                return max(toNumber(a), toNumber(b))
            if operationToken.lexemeType == TOKEN.MIN_OPERATION:
                return min(toNumber(a), toNumber(b))
            if operationToken.lexemeType == TOKEN.AND_OPERATION:
                return bool(a) and bool(b)
            if operationToken.lexemeType == TOKEN.OR_OPERATION:
                return bool(a) or bool(b)
            if operationToken.lexemeType == TOKEN.XOR_OPERATION:
                return (bool(a) and not bool(b)) or (not bool(a) and bool(b))

            if not (isinstance(a, (int, float)) and isinstance(b, (int, float))):
                self._throwError(SyntaxError, "Invalid Type")

            if operationToken.lexemeType == TOKEN.EQUAL_TO_OPERATION:
                return toNumber(a) == toNumber(b)
            if operationToken.lexemeType == TOKEN.NOT_EQUAL_TO_OPERATION:
                return toNumber(a) != toNumber(b)
        except ValueError as error:
            self._throwError(ValueError, error.args[0])

    def _TwoOperandOperation(self):
        if (
            self._nextTokenIs(TOKEN.ADDITION_OPERATION)
            or self._nextTokenIs(TOKEN.SUBTRACTION_OPERATION)
            or self._nextTokenIs(TOKEN.MULTIPLICATION_OPERATION)
            or self._nextTokenIs(TOKEN.QUOTIENT_OPERATION)
            or self._nextTokenIs(TOKEN.MODULO_OPERATION)
            or self._nextTokenIs(TOKEN.MAX_OPERATION)
            or self._nextTokenIs(TOKEN.MIN_OPERATION)
            or self._nextTokenIs(TOKEN.AND_OPERATION)
            or self._nextTokenIs(TOKEN.OR_OPERATION)
            or self._nextTokenIs(TOKEN.XOR_OPERATION)
            or self._nextTokenIs(TOKEN.EQUAL_TO_OPERATION)
            or self._nextTokenIs(TOKEN.NOT_EQUAL_TO_OPERATION)
        ):
            operationToken = self._popNextToken()

            firstOperandValue = self._Operand()
            if firstOperandValue is not None:
                self._expectNextToken(TOKEN.OPERAND_SEPARATOR, 'Missing keyword "AN"')

                secondOperandValue = self._Operand()
                if secondOperandValue is not None:
                    return self._operate(
                        operationToken, firstOperandValue, secondOperandValue
                    )

                self._throwError(SyntaxError, "Expected an operand")

            self._throwError(SyntaxError, "Expected an operand")

        return None

    def _NotOperation(self):
        if self._nextTokenIs(TOKEN.NOT_OPERATION):
            self._popNextToken()

            value = self._Operand()
            if value is not None:
                return not value

            self._throwError(SyntaxError, "Expected an operand")

        return None

    def _MultipleOperandOperation(self):
        operandValues = []

        if (
            self._nextTokenIs(TOKEN.INFINITE_ARITY_AND_OPERATION)
            or self._nextTokenIs(TOKEN.INFINITE_ARITY_OR_OPERATION)
            or self._nextTokenIs(TOKEN.CONCATENATION_OPERATION)
        ):
            operationToken = self._popNextToken()

            if operationToken.lexemeType == TOKEN.CONCATENATION_OPERATION:
                needsMkay = False
            else:
                needsMkay = True

            firstOperandValue = self._Operand()
            if firstOperandValue is not None:
                operandValues.append(firstOperandValue)

                self._expectNextToken(TOKEN.OPERAND_SEPARATOR, 'Missing keyword "AN"')

                secondOperandValue = self._Operand()
                if secondOperandValue is not None:
                    operandValues.append(secondOperandValue)

                    while self._nextTokenIs(TOKEN.OPERAND_SEPARATOR):
                        self._popNextToken()

                        operandValue = self._Operand()
                        if operandValue is not None:
                            operandValues.append(operandValue)
                        else:
                            self._throwError(SyntaxError, "Expected an operand")

                    if needsMkay:
                        self._expectNextToken(
                            TOKEN.INFINITE_ARITY_DELIMITER, 'Missing keyword "MKAY"'
                        )

                    if operationToken.lexemeType == TOKEN.INFINITE_ARITY_AND_OPERATION:
                        return all(operandValues)
                    if operationToken.lexemeType == TOKEN.INFINITE_ARITY_OR_OPERATION:
                        return any(operandValues)
                    if operationToken.lexemeType == TOKEN.CONCATENATION_OPERATION:
                        return "".join(operandValues)

                self._throwError(SyntaxError, "Expected an operand")

            self._throwError(SyntaxError, "Expected an operand")

        return None

    def _typeCast(self, type, value):
        if isinstance(value, str):
            return value

        if type == "TROOF":
            return bool(value)

        try:
            if type == "NUMBAR":
                return float(value) if value != None else 0.0

            if type == "NUMBR":
                return int(value) if value != None else 0

        except ValueError as error:
            self._throwError(ValueError, error.args[0])

        if type == "YARN":
            if value == None:
                return ""

            if isinstance(value, bool):
                return "WIN" if value else "FAIL"

            if isinstance(value, int) or isinstance(value, float):
                return str(round(value, 2))

    def _ExplicitTypecast(self):
        if self._nextTokenIs(TOKEN.EXPLICIT_TYPECASTING_KEYWORD):
            self._popNextToken()

            if self._nextTokenIs(TOKEN.VARIABLE_IDENTIFIER):
                variableIdentifierToken = self._popNextToken()
                variableIdentifier = variableIdentifierToken.lexeme
                value = self._getValue(variableIdentifier)

                if self._nextTokenIs(TOKEN.TYPE_LITERAL):
                    typeToken = self._popNextToken()

                    return self._typeCast(typeToken.lexeme, value)

                self._throwError(SyntaxError, "Expected a type")

            self._throwError(SyntaxError, "Expected a variable")

        return None

    def _AssignmentStatement(self):

        if self._nextTokenIs(TOKEN.VARIABLE_IDENTIFIER):
            variableIdentifierToken = self._popNextToken()
            variableIdentifier = variableIdentifierToken.lexeme
            value = None

            if variableIdentifier not in self.memory.keys():
                self._throwError(SyntaxError, "Variable not declared")

            if self._nextTokenIs(TOKEN.VARIABLE_ASSIGNMENT):
                print("assigning var")
                self._popNextToken()

                value = self._Operand()
                if value is None:
                    self._throwError(SyntaxError, "Expected operand")

                self._assign(variableIdentifier, value)

                return True

            self.tokens.insert(0, variableIdentifierToken)

            return None

        return None

    def _RecastingStatement(self):

        if self._nextTokenIs(TOKEN.VARIABLE_IDENTIFIER):
            variableIdentifierToken = self._popNextToken()
            variableIdentifier = variableIdentifierToken.lexeme
            value = None

            if variableIdentifier not in self.memory.keys():
                self._throwError(SyntaxError, "Variable not declared")

            if self._nextTokenIs(TOKEN.RECASTING_KEYWORD):
                print("recasting var")
                self._popNextToken()

                value = self._getValue(variableIdentifier)

                if self._nextTokenIs(TOKEN.TYPE_LITERAL):
                    typeToken = self._popNextToken()

                    typedValue = self._typeCast(typeToken.lexeme, value)

                    self._assign(variableIdentifier, typedValue)

                    return True

                self._throwError(SyntaxError, "Expected operand")

            self.tokens.insert(0, variableIdentifierToken)

            return None

        return None

    def _IfStatement(self):

        if self._nextTokenIs(TOKEN.IF_ELSE_DELIMITER):
            self._popNextToken()

            statementBlockDict = {}

            self._expectNextToken(TOKEN.LINEBREAK, "Expected a linebreak")
            self._expectNextToken(TOKEN.IF_STATEMENT_KEYWORD, "Expected 'YA RLY'")
            self._expectNextToken(TOKEN.LINEBREAK, "Expected a linebreak")

            while self._nextTokenIs(TOKEN.LINEBREAK):
                self._popNextToken()

            ifBlockTokens = []
            while not (
                self._nextTokenIs(TOKEN.ELSE_STATEMENT_KEYWORD)
                or self._nextTokenIs(TOKEN.FLOW_CONTROL_STATEMENTS_DELIMITER)
            ):
                ifBlockTokens.append(self._popNextToken())

            statementBlockDict[self._getValue(TOKEN.IT_VARIABLE)] = ifBlockTokens

            if self._nextTokenIs(TOKEN.ELSE_STATEMENT_KEYWORD):
                self._popNextToken()

                self._expectNextToken(TOKEN.LINEBREAK, "Expected a linebreak")

                while self._nextTokenIs(TOKEN.LINEBREAK):
                    self._popNextToken()

                elseBlockTokens = []
                while not self._nextTokenIs(TOKEN.FLOW_CONTROL_STATEMENTS_DELIMITER):
                    elseBlockTokens.append(self._popNextToken())

                if True not in statementBlockDict.keys():
                    statementBlockDict[True] = elseBlockTokens

            self._expectNextToken(
                TOKEN.FLOW_CONTROL_STATEMENTS_DELIMITER, "Expected 'OIC'"
            )

            if True in statementBlockDict.keys():
                remainingTokens = self.tokens

                currentLineNumber = self.currentLineNumber
                self.tokens = statementBlockDict[True]
                self.currentLineNumber = 0

                self._enterNewScope()
                self._Statements()
                self._exitCurrentScope()

                self.tokens = remainingTokens
                self.currentLineNumber = currentLineNumber

            return True

        return None

    def _BreakStatement(self):

        if self.canGTFO:

            if self._nextTokenIs(TOKEN.BREAK_STATEMENT):

                self.tokens = []
                self.canGTFO = False
                return None

        return None

    def _CaseStatement(self):

        if self._nextTokenIs(TOKEN.SWITCH_CASE_STATEMENT_DELIMITER):
            self._popNextToken()

            statementBlockLocation = {}
            caseCodeBlock = []
            it_var = self._getValue(TOKEN.IT_VARIABLE)

            self._expectNextToken(TOKEN.LINEBREAK, "Expected a linebreak")
            self._expectNextToken(TOKEN.CASE_KEYWORD, "Expected keyword 'OMG'")

            operand = self._Operand()
            if operand is not None:

                self._expectNextToken(TOKEN.LINEBREAK, "Expected a linebreak")

                while self._nextTokenIs(TOKEN.LINEBREAK):
                    self._popNextToken()

                statementBlockLocation[str(operand)] = 0

                while not (
                    self._nextTokenIs(TOKEN.CASE_KEYWORD)
                    or self._nextTokenIs(TOKEN.DEFAULT_CASE_KEYWORD)
                    or self._nextTokenIs(TOKEN.FLOW_CONTROL_STATEMENTS_DELIMITER)
                ):
                    caseCodeBlock.append(self._popNextToken())

                while True:
                    if self._nextTokenIs(TOKEN.CASE_KEYWORD):
                        self._popNextToken()

                        operand = self._Operand()
                        if operand is not None:

                            while self._nextTokenIs(TOKEN.LINEBREAK):
                                self._popNextToken()

                            if str(it_var) not in statementBlockLocation.keys():
                                statementBlockLocation[str(operand)] = len(
                                    caseCodeBlock
                                )

                            while not (
                                self._nextTokenIs(TOKEN.CASE_KEYWORD)
                                or self._nextTokenIs(
                                    TOKEN.FLOW_CONTROL_STATEMENTS_DELIMITER
                                )
                                or self._nextTokenIs(TOKEN.DEFAULT_CASE_KEYWORD)
                            ):
                                caseCodeBlock.append(self._popNextToken())

                        else:
                            self._throwError(SyntaxError, "Missing Operand")
                    else:
                        break

                if self._nextTokenIs(TOKEN.DEFAULT_CASE_KEYWORD):
                    self._popNextToken()

                    while self._nextTokenIs(TOKEN.LINEBREAK):
                        self._popNextToken()

                    if str(it_var) not in statementBlockLocation.keys():
                        statementBlockLocation[str(it_var)] = len(caseCodeBlock)

                    while not (
                        self._nextTokenIs(TOKEN.FLOW_CONTROL_STATEMENTS_DELIMITER)
                    ):
                        caseCodeBlock.append(self._popNextToken())

                self._expectNextToken(
                    TOKEN.FLOW_CONTROL_STATEMENTS_DELIMITER, "Expected 'OIC'"
                )

                if str(it_var) in statementBlockLocation.keys():

                    currentLineNumber = self.currentLineNumber
                    remainingTokens = self.tokens
                    self.canGTFO = True

                    self.tokens = caseCodeBlock[
                        statementBlockLocation[it_var] : len(caseCodeBlock)
                    ]

                    self.currentLineNumber = 0

                    self._enterNewScope()
                    self._Statements()
                    self._exitCurrentScope()

                    self.tokens = remainingTokens
                    self.currentLineNumber = currentLineNumber

                return True

            self._throwError(SyntaxError, "Missing Operand")

        return None

    # !!! no nested loops
    # !!! does not verify loop identifier
    def _LoopStatement(self):
        if self._nextTokenIs(TOKEN.LOOP_DECLARATION_AND_DELIMITER):
            self._popNextToken()

            loopHeaderLineNumber = self.currentLineNumber

            if self._nextTokenIs(TOKEN.LOOP_IDENTIFIER):
                loopIdentifierToken = self._popNextToken()
                loopIdentifier = loopIdentifierToken.lexeme

                if self._nextTokenIs(TOKEN.INCREMENT_KEYWORD) or self._nextTokenIs(
                    TOKEN.DECREMENT_KEYWORD
                ):
                    deltaToken = self._popNextToken()
                    if deltaToken.lexeme == "UPPIN":
                        delta = 1
                    elif deltaToken.lexeme == "NERFIN":
                        delta = -1

                    self._expectNextToken(TOKEN.KEYWORD_IN_LOOP, 'Missing keyword "YR"')

                    if self._nextTokenIs(TOKEN.VARIABLE_IDENTIFIER):
                        variableIdentifierToken = self._popNextToken()
                        variableIdentifier = variableIdentifierToken.lexeme

                        conditionExpressionTokens = []
                        hasLoopCondition = False
                        if self._nextTokenIs(TOKEN.LOOP_CONDITION_KEYWORD):
                            loopConditionKeywordToken = self._popNextToken()

                            hasLoopCondition = True

                            while not self._nextTokenIs(TOKEN.LINEBREAK):
                                conditionExpressionTokens.append(self._popNextToken())

                        self._expectNextToken(
                            TOKEN.LINEBREAK, "Missing condition or new line"
                        )

                        while self._nextTokenIs(TOKEN.LINEBREAK):
                            self._popNextToken()

                        loopBlockTokens = []
                        while not self._nextTokenIs(TOKEN.LOOP_DELIMITER):
                            loopBlockTokens.append(self._popNextToken())

                        self._expectNextToken(
                            TOKEN.LOOP_DELIMITER, "Missing loop closing"
                        )

                        self._expectNextToken(
                            TOKEN.LOOP_IDENTIFIER, "Missing loop identifier"
                        )

                        remainingTokens = self.tokens

                        while True:
                            self.tokens = conditionExpressionTokens + loopBlockTokens
                            self.currentLineNumber = loopHeaderLineNumber + 1

                            if hasLoopCondition:
                                if loopConditionKeywordToken.lexeme == "WILE":
                                    loopRunCondition = self._Operand()
                                elif loopConditionKeywordToken.lexeme == "TIL":
                                    loopRunCondition = not self._Operand()

                                if not loopRunCondition:
                                    break

                            self._enterNewScope()
                            self._Statements()
                            self._exitCurrentScope()

                            self._assign(
                                variableIdentifier,
                                self._getValue(variableIdentifier) + delta,
                            )

                        self.tokens = remainingTokens

                        return True

                    self._throwError(SyntaxError, "Missing variable")

                self._throwError(SyntaxError, "Missing UPPIN/NERFIN keyword")

            self._throwError(SyntaxError, "Missing loop name")

        return None
