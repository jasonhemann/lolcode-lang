import re

from .token_enum import TOKEN


class Lexer:
    def __init__(self):
        self.patternTypes = {
            r"^HAI$": TOKEN.CODE_DELIMITER,
            r"^KTHXBYE$": TOKEN.CODE_DELIMITER,
            r"^BTW$": TOKEN.COMMENT_KEYWORD,
            r"^OBTW$": TOKEN.MULTILINE_COMMENT_DELIMITER,
            r"^TLDR$": TOKEN.MULTILINE_COMMENT_DELIMITER,
            r"^I HAS A$": TOKEN.VARIABLE_DECLARATION,
            r"^ITZ$": TOKEN.VARIABLE_ASSIGNMENT,
            r"^R$": TOKEN.VARIABLE_ASSIGNMENT,
            r"^SUM OF$": TOKEN.ADDITION_OPERATION,
            r"^DIFF OF$": TOKEN.SUBTRACTION_OPERATION,
            r"^PRODUKT OF$": TOKEN.MULTIPLICATION_OPERATION,
            r"^QUOSHUNT OF$": TOKEN.QUOTIENT_OPERATION,
            r"^MOD OF$": TOKEN.MODULO_OPERATION,
            r"^BIGGR OF$": TOKEN.MAX_OPERATION,
            r"^SMALLR OF$": TOKEN.MIN_OPERATION,
            r"^BOTH OF$": TOKEN.AND_OPERATION,
            r"^EITHER OF$": TOKEN.OR_OPERATION,
            r"^WON OF$": TOKEN.XOR_OPERATION,
            r"^NOT$": TOKEN.NOT_OPERATION,
            r"^ALL OF$": TOKEN.INFINITE_ARITY_AND_OPERATION,
            r"^ANY OF$": TOKEN.INFINITE_ARITY_OR_OPERATION,
            r"^BOTH SAEM$": TOKEN.EQUAL_TO_OPERATION,
            r"^DIFFRINT$": TOKEN.NOT_EQUAL_TO_OPERATION,
            r"^SMOOSH$": TOKEN.CONCATENATION_OPERATION,
            r"^MAEK$": TOKEN.EXPLICIT_TYPECASTING_KEYWORD,
            r"^A$": TOKEN.OPTIONAL_A_KEYWORD,
            r"^AN$": TOKEN.OPERAND_SEPARATOR,
            r"^MKAY$": TOKEN.INFINITE_ARITY_DELIMITER,
            r"^IS NOW A$": TOKEN.RECASTING_KEYWORD,
            r"^VISIBLE$": TOKEN.OUTPUT_KEYWORD,
            r"^GIMMEH$": TOKEN.INPUT_KEYWORD,
            r"^O RLY\?$": TOKEN.IF_ELSE_DELIMITER,
            r"^YA RLY$": TOKEN.IF_STATEMENT_KEYWORD,
            r"^MEBBE$": TOKEN.ELSE_IF_STATEMENT_KEYWORD,
            r"^GTFO$": TOKEN.BREAK_STATEMENT,
            r"^NO WAI$": TOKEN.ELSE_STATEMENT_KEYWORD,
            r"^OIC$": TOKEN.FLOW_CONTROL_STATEMENTS_DELIMITER,
            r"^WTF\?$": TOKEN.SWITCH_CASE_STATEMENT_DELIMITER,
            r"^OMG$": TOKEN.CASE_KEYWORD,
            r"^OMGWTF$": TOKEN.DEFAULT_CASE_KEYWORD,
            r"^IM IN YR$": TOKEN.LOOP_DECLARATION_AND_DELIMITER,
            r"^UPPIN$": TOKEN.INCREMENT_KEYWORD,
            r"^NERFIN$": TOKEN.DECREMENT_KEYWORD,
            r"^YR$": TOKEN.KEYWORD_IN_LOOP,
            r"^TIL$": TOKEN.LOOP_CONDITION_KEYWORD,
            r"^WILE$": TOKEN.LOOP_CONDITION_KEYWORD,
            r"^IM OUTTA YR$": TOKEN.LOOP_DELIMITER,
            r"^-?\d*\.\d+$": TOKEN.FLOAT_LITERAL,
            r"^-?\d+$": TOKEN.INTEGER_LITERAL,
            r"^\".*\"$": TOKEN.STRING_LITERAL,
            r"^(WIN|FAIL)$": TOKEN.BOOL_LITERAL,
            r"^(NOOB|NUMBR|NUMBAR|YARN|TROOF)$": TOKEN.TYPE_LITERAL,
        }

    def process(self, content):
        self.tokens = []

        content = self._removeIndents(content)
        content = self._removeComments(content)
        self._tokenizeSourceCode(content)
        return self.tokens

    def _removeIndents(self, content):
        return re.sub(r"\t", "", content)

    def _removeComments(self, content):
        noMultilineComments = re.sub(r"(OBTW(?<=OBTW)(.|\n)*?(?=TLDR)TLDR)", "", content)
        noComments = re.sub(r"BTW .*", "", noMultilineComments)
        
        return noComments

    def _tokenizeSourceCode(self, sourceCode):
        for lineIndex, line in enumerate(sourceCode.split("\n")):
            self.currentLineNumber = lineIndex + 1
            self.currentLine = line
            self.currentLineColumnNumber = 0
            self._tokenizeCurrentLine()

    def _tokenizeCurrentLine(self):
        words = self.currentLine.split()

        buffer = ""
        previousLexemeType = None
        isLineTokenized = False

        while not isLineTokenized:
            for word in words:
                if len(buffer) > 0:
                    buffer += " "
                buffer += word

                lexemeType = self._getLexemeType(buffer)
                if lexemeType != None:
                    self.tokens.append(Token(buffer, lexemeType))
                    previousLexemeType = lexemeType

                    buffer = ""
                    self.currentLineColumnNumber += len(buffer)

            if buffer == "":
                break

            possibleIdentifier, *words = buffer.split()

            if not self._isIdentifier(possibleIdentifier):
                self._throwSyntaxError("Unexpected token")

            identifier = possibleIdentifier

            identifierLexemeType = self._getIdentifierTypeBasedOn(previousLexemeType)

            self.tokens.append(Token(identifier, identifierLexemeType))
            self.currentLineColumnNumber += len(identifier) + 1
            previousLexemeType = identifierLexemeType

            buffer = ""

        self.tokens.append(Token("\n", TOKEN.LINEBREAK))

    def _throwSyntaxError(self, message):
        # column number is not accurate due to source code cleaning

        syntaxErrorArgs = (
            None,
            self.currentLineNumber,
            self.currentLineColumnNumber,
            self.currentLine,
        )

        raise SyntaxError(message, syntaxErrorArgs)

    def _getLexemeType(self, lexeme):
        allPatterns = dict.keys(self.patternTypes)
        for pattern in allPatterns:
            if re.match(pattern, lexeme):
                lexemeType = self.patternTypes[pattern]
                return lexemeType
        return None

    def _isIdentifier(self, word):
        return re.match(r"^[a-zA-Z]\w*$", word)

    def _getIdentifierTypeBasedOn(self, previousLexemeType):
        if previousLexemeType in [
            TOKEN.LOOP_DECLARATION_AND_DELIMITER,
            TOKEN.LOOP_DELIMITER,
        ]:
            return TOKEN.LOOP_IDENTIFIER

        return TOKEN.VARIABLE_IDENTIFIER


class Token:
    def __init__(self, lexeme, lexemeType):
        self.lexeme = lexeme
        self.lexemeType = lexemeType
