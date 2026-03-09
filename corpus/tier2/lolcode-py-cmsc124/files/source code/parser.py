from token_types import *
from nodes import *
from error import *

class Parser:
    def __init__(self, tokens,  txt_console=None, tbl_sym=None) -> None:
        self.tokens = tokens
        self.token_idx = -1
        self.txt_console = txt_console
        self.tbl_sym = tbl_sym
        self.insideString = False
        self.insideSmoosh = False


    def advance(self):
        self.token_idx += 1
        if self.token_idx < len(self.tokens):
            self.current_tok = self.tokens[self.token_idx]
        if self.current_tok.type in (TT_COMMENT_STRT, TT_COMMENT_MULTI_STRT, TT_COMMENT_MULTI_END):
            self.advance()
        if not self.insideString and not self.insideSmoosh and self.current_tok.type in (TT_NEWLINE):
            self.advance()
        return self.current_tok
    
    def seekToken(self):
        try:
            return self.tokens[self.token_idx+1]
        except Exception:
            pass


    def parse(self):
        res = self.code()
        return res


    def code(self):
        try:
            resetSymbolTable()
            #Start of code
            start_node = self.advance()
            
            if start_node.type not in (TT_CODE_STRT):
                raise ErrorSyntax(self.current_tok, f"Expected HAI at {self.current_tok.pos}")

            body_node = list(self.body())

            #End of code
            end_node = self.current_tok

            if end_node.type not in (TT_CODE_END):
                raise ErrorSyntax(self.current_tok, f"Expected KTHBYE at pos {self.current_tok.pos}")

            res = Program(start_node, body_node, end_node, self.tbl_sym)

            return res
        except Error as err:
            return err
    
    
    def body(self):
        while(self.token_idx+1 < len(self.tokens)):
            if self.seekToken().type in (TT_CODE_END) or self.current_tok.type in (TT_CODE_END):
                break
            
            self.advance()
            yield self.statement()


    def literal(self):
        if self.current_tok.type in (TT_FLOAT):
            return NumbarNode(self.current_tok)
        elif self.current_tok.type in (TT_INTEGER):
            return NumbrNode(self.current_tok)
        elif self.current_tok.type in (TT_STR_DELIMITER):
            return self.string()
        elif self.current_tok.type in (TT_BOOLEAN):
            return TroofNode(self.current_tok)

        return ErrorSyntax(self.current_tok, "Not a literal")


    def do_print(self):
        if self.current_tok.type in (TT_OUTPUT):
            self.insideString = True
            left = self.current_tok

            right = []
            suppress = False
            while 1:
                an = self.seekToken()
                if an.type in (TT_ARG_SEP):
                    self.advance()
                self.advance()
                temptok = self.current_tok
                exproutput = self.expr(raiseError=False)
                if exproutput == None:
                    if self.current_tok.type in (TT_SUPPRESS_NEWLINE):
                        self.advance()
                        temptok = self.current_tok
                        suppress = True
                    if self.current_tok.type not in (TT_NEWLINE):
                        raise ErrorSyntax(self.current_tok, f"Expected Delimiter at pos {self.current_tok.pos}")
                    self.token_idx -= 1
                    self.current_tok = temptok
                    break
                
                right.append(exproutput)
            self.insideString = False
            res = VisibleNode(left, right, self.txt_console, suppress)
            return res

        raise ErrorSyntax(self.current_tok, f"Expected VISIBLE at pos {self.current_tok.pos}")


    def concatenation(self):
        if self.current_tok.type in (TT_CONCAT):
            self.insideSmoosh = True
            
            op_token = self.current_tok

            self.advance()
            left = self.expr()

            right = []
            while 1:
                an = self.advance()
                if an.type not in (TT_ARG_SEP):
                    raise ErrorSyntax(self.current_tok, f"Expected AN at pos {self.current_tok.pos}")
                self.advance()
                temptok = self.current_tok
                exproutput = self.expr(raiseError=False)
                if exproutput == None:
                    self.token_idx -= 1
                    self.current_tok = temptok
                    break
                
                right.append(exproutput)

                if self.seekToken().type in (TT_NEWLINE):
                    break
                
            self.insideSmoosh = False
            res = SmooshNode(left, right)
            return res

        raise ErrorSyntax(self.current_tok, f"Expected VISIBLE at pos {self.current_tok.pos}")

        pass

    def get_input(self):
        if self.current_tok.type in (TT_READ):
            left = self.current_tok
            right = self.advance()
            if right.type not in (TT_IDENTIFIER):
                raise ErrorSyntax(self.current_tok, f"Expected IDENTIFIER at pos {self.current_tok.pos}")

            res = GimmehNode(left, VariableNode(right), self.txt_console)
            return res
        raise ErrorSyntax(self.current_tok, f"Expected GIMMEH at pos {self.current_tok.pos}")


    def comparison(self):
        if self.current_tok.type in (GP_COMPARISON):
            op_token = self.current_tok
            self.advance()
            expr1 = self.expr()
            an = self.advance()
            if an.type not in (TT_ARG_SEP):
                raise ErrorSyntax(self.current_tok, f"Expected AN at pos {self.current_tok.pos}")
            self.advance()
            expr2 = self.expr()
            res = ComparisonNode(op_token, expr1, an, expr2)
            return res


    def expr(self,raiseError=True):
        if self.current_tok.type in GP_ARITHMETIC:
            op_token = self.current_tok

            self.advance()
            left = self.expr()
            an = self.advance()
            if an.type not in (TT_ARG_SEP):
                raise ErrorSyntax(self.current_tok, f"Expected AN at pos {self.current_tok.pos}")
            self.advance()
            right = self.expr()

            res = ArithmeticNode(op_token, left, an, right)
            return res
        elif self.current_tok.type in (TT_FLOAT, TT_INTEGER):
            tok = self.current_tok
            if tok.type in (TT_FLOAT):
                return NumbarNode(tok)
            elif tok.type in (TT_INTEGER):
                return NumbrNode(tok)
        elif self.current_tok.type in (TT_STR_DELIMITER):
            return self.string()
        elif self.current_tok.type in (TT_BOOLEAN):
            return TroofNode(self.current_tok)
        elif self.current_tok.type in (TT_IDENTIFIER):
            return VariableNode(self.current_tok)
        elif self.current_tok.type in (GP_COMPARISON):
            return self.comparison()
        elif self.current_tok.type in (*GP_BOOLEAN_LONG, GP_BOOLEAN_SHORT, *GP_BOOLEAN_INF):
            return self.boolean()
        elif self.current_tok.type in (TT_CONCAT):
            return self.concatenation()
        elif self.current_tok.type in (TT_TYPECAST_2):
            return self.typecast()


        if raiseError:
            raise ErrorSyntax(self.current_tok, f"Expected SUM OF or DIFF OF or OR PRODUKT OF or QUOSHUNT OF or NERFIN or UPPIN or BIGGR or SMALLR or Float or Integer or \" or Boolean or BOTH SAEM or NOT BOTH SAEM at pos {self.current_tok.pos}")
        else:
            return None

    def variableLong(self):
        if self.current_tok.type in (TT_VAR_DEC):
            ihasa_token = self.current_tok

            variable = self.advance()
            if variable.type not in (TT_IDENTIFIER):
                raise ErrorSyntax(self.current_tok, f"Expected IDENTIFIER at pos {self.current_tok.pos}")
            variable = VariableNode(self.current_tok)
            itz = self.seekToken()
            if itz.type not in (TT_VAR_ASSIGN):
                res = AssignmentShlongNode(ihasa_token, variable)
                return res
            itz = self.advance()
            self.advance()
            expr = self.expr()

            res = AssignmentLongNode(ihasa_token, variable, itz, expr)
            return res


    def variableShort(self):
        if self.current_tok.type in (TT_IDENTIFIER):

            variable = self.current_tok
            if variable.type not in (TT_IDENTIFIER):
                raise ErrorSyntax(self.current_tok, f"Expected IDENTIFIER at pos {self.current_tok.pos}")

            variable = VariableNode(self.current_tok)

            r = self.advance()
            if r.type not in (TT_VAR_VAL_ASSIGN):
                raise ErrorSyntax(self.current_tok, f"Expected R at pos {self.current_tok.pos}")

            self.advance()
            expr = self.expr()

            res = AssignmentShortNode(variable, r, expr)
            return res

    def variable(self):
        if self.current_tok.type in (TT_IDENTIFIER):

            variable = self.current_tok
            if variable.type not in (TT_IDENTIFIER):
                raise ErrorSyntax(self.current_tok, f"Expected IDENTIFIER at pos {self.current_tok.pos}")

            res = VariableNode(self.current_tok)
            return res


    def typecast(self):
        if self.current_tok.type in (TT_TYPECAST_2):

            maek = self.current_tok

            self.advance()
            expr = self.expr()

            possibleA = self.advance()
            if possibleA.type in (TT_A):
                pass
            elif possibleA.type in (TT_TYPE):
                return TypecastShortNode(maek,expr,possibleA)
            else:
                raise ErrorSyntax(self.current_tok, f"Expected TROOF|NOOB|NUMBR|NUMBAR|YARN|TYPE at pos {self.current_tok.pos}")

            ttype = self.advance()
            if ttype.type not in (TT_TYPE):
                raise ErrorSyntax(self.current_tok, f"Expected TROOF|NOOB|NUMBR|NUMBAR|YARN|TYPE at pos {self.current_tok.pos}")

            res = TypecastLongNode(maek,expr,possibleA,ttype)
            return res


    def boolean(self):
        if self.current_tok.type in GP_BOOLEAN_INF:
            op_token = self.current_tok

            self.advance()
            left = self.expr()

            right = []
            while 1:
                an = self.advance()
                if an.type not in (TT_ARG_SEP):
                    raise ErrorSyntax(self.current_tok, f"Expected AN at pos {self.current_tok.pos}")
                self.advance()
                temptok = self.current_tok
                exproutput = self.expr(raiseError=False)
                if exproutput == None:
                    self.token_idx -= 1
                    self.current_tok = temptok
                    break

                right.append(exproutput)

                if self.seekToken().type in (TT_MKAY):
                    self.advance()
                    break
                elif self.seekToken().type in (TT_NEWLINE):
                    break

            res = BooleanInfNode(op_token, left, right)
            return res
        elif self.current_tok.type in GP_BOOLEAN_LONG:
            op_token = self.current_tok
            self.advance()
            expr1 = self.expr()
            an = self.advance()
            if an.type not in (TT_ARG_SEP):
                raise ErrorSyntax(self.current_tok, f"Expected AN at pos {self.current_tok.pos}")
            self.advance()
            expr2 = self.expr()
            res = BooleanLongNode(op_token, expr1, an, expr2)
            return res
        elif self.current_tok.type in (TT_NOT):
            op_token = self.current_tok
            self.advance()
            expr = self.expr()
            res = BooleanShortNode(op_token, expr)
            return res

    """
    START SWITCH STATEMENT
    """
    def casebody(self):
        while(self.token_idx < len(self.tokens)):
            if self.tokens[self.token_idx].type in (TT_BREAK, TT_CONTROL_END, TT_CASE):
                break

            if self.current_tok.type in (TT_CASEBREAK):
                yield CaseBreakNode(self.current_tok)
            else:
                yield self.statement()
            self.advance()


    def switchcase(self):
        while(self.token_idx < len(self.tokens)):
            if self.tokens[self.token_idx].type in (TT_CONTROL_END):
                break

            omg = self.current_tok
            if omg.type in (TT_BREAK):
                self.advance()
                casebody = list(self.casebody())
                yield DefaultCaseNode(omg, casebody)
                break

            self.advance()
            value = self.literal()
            self.advance()
            casebody = list(self.casebody())
            yield SwitchCaseNode(omg, value, casebody)


    def switch(self):
        if self.current_tok.type in (TT_SWITCH):
            op_token = self.current_tok
            self.advance()
            expr = list(self.switchcase())
            oic = self.current_tok
            if oic.type not in (TT_CONTROL_END):
                raise ErrorSyntax(self.current_tok, f"Expected OIC at pos {self.current_tok.pos}")
            res = SwitchNode(op_token, expr)
            return res
        else:
            raise ErrorSyntax(self.current_tok, f"Expected OIC at {self.current_tok.pos}")

    """
    END SWITCH STATEMENT
    """

    def string(self):
        if self.current_tok.type in (TT_STR_DELIMITER):
            qt1 = self.current_tok
            string = self.advance()
            if string.type not in (TT_STRING):
                raise ErrorSyntax(self.current_tok, f"Expected String at pos {self.current_tok.pos}")
            qt2 = self.advance()
            if qt2.type not in (TT_STR_DELIMITER):
                raise ErrorSyntax(self.current_tok, f"Expected \" at pos {self.current_tok.pos}")
            res = YarnNode(string)
            return res
        return ErrorSyntax(self.current_tok, f"Expected \" at pos {self.current_tok.pos}")

    """
    START LOOP STATEMENT
    """
    def loopbody(self):
        while(self.token_idx < len(self.tokens)):
            if self.tokens[self.token_idx].type in (TT_LOOP_END):
                break
            
            yield self.statement()
            self.advance()

    def loop(self):
        if self.current_tok.type in (TT_LOOP_STRT):
            del_start = self.current_tok
            label_start = self.advance()
            if label_start.type not in (TT_IDENTIFIER):
                raise ErrorSyntax(self.current_tok, f"Expected IDENTIFIER at pos {self.current_tok.pos}")
            operation = self.advance()
            if operation.type not in (TT_INC, TT_DEC):
                raise ErrorSyntax(self.current_tok,f"Expected UPPIN OR NERFIN at pos {self.current_tok.pos}")
            yr = self.advance()
            if yr.type not in (TT_YR):
                raise ErrorSyntax(self.current_tok,f"Expected YR at pos {self.current_tok.pos}")
            var = self.advance()
            if var.type not in (TT_IDENTIFIER):
                raise ErrorSyntax(self.current_tok,f"Expected IDENTIFIER at pos {self.current_tok.pos}")
            cond = self.advance()
            if cond.type not in (TT_WHILE, TT_UNTIL):
                raise ErrorSyntax(self.current_tok,f"Expected WILE|TIL at pos {self.current_tok.pos}")
            
            self.advance()
            cond_expr = self.expr()
            self.advance()

            codeblock = list(self.loopbody())
            del_end = self.current_tok

            if del_end.type not in (TT_LOOP_END):
                raise ErrorSyntax(self.current_tok,f"Expected IM OUTTA YR at pos {self.current_tok}")
            label_end = self.advance()
            if label_end.type not in (TT_IDENTIFIER):
                raise ErrorSyntax(self.current_tok,f"Expected IDENTIFIER at pos{self.current_tok}")

            res = LoopNodeLong(del_start, label_start, operation, yr, var, cond, cond_expr, codeblock, del_end, label_end)
            return res

    """
    END LOOP STATEMENT
    """

    
    """
    START IF STATEMENT
    """
    def ifbody(self):
        while(self.token_idx < len(self.tokens)):
            if self.tokens[self.token_idx].type in (TT_ELIF, TT_ELSE, TT_CONTROL_END):
                break

            yield self.statement()
            self.advance()


    def elsecase(self):
        if self.current_tok.type not in (TT_TRUTH):
            raise ErrorSyntax(self.current_tok, f"Expected YA RLY at pos {self.current_tok.pos}")
        yield IfNode(self.current_tok, list(self.ifbody()))
        while(self.token_idx < len(self.tokens)):
            if self.tokens[self.token_idx].type not in (TT_CONTROL_END):
                if self.token_idx < len(self.tokens):
                    omg = self.current_tok
                    if omg.type in (TT_ELIF):
                        self.advance()
                        expr = self.statement()
                        self.advance()
                        ifbody = list(self.ifbody())
                        yield ElseIfNode(omg, expr, ifbody)
                    elif omg.type in (TT_ELSE):
                        self.advance()
                        elsebody = list(self.ifbody())
                        yield ElseNode(omg, elsebody)
                        break
            else:
                break


    def ifelse(self):
        if self.current_tok.type in (TT_IF):
            op_token = self.current_tok
            self.advance()
            expr = list(self.elsecase())
            oic = self.current_tok
            if oic.type not in (TT_CONTROL_END):
                raise ErrorSyntax(self.current_tok,f"Expected OIC at pos {self.current_tok.pos}")
            res = IfElseNode(op_token, expr, oic)
            return res
        else:
            raise ErrorSyntax(self.current_tok,f"Expected IF at pos {self.current_tok.pos}")

    """
    END IF STATEMENT
    """

    def statement(self):
        res = None
        if self.current_tok.type in (GP_ARITHMETIC):
            res = self.expr()
        elif self.current_tok.type in (TT_READ):
            res = self.get_input()
        elif self.current_tok.type in (TT_OUTPUT):
            res = self.do_print()
        elif self.current_tok.type in (TT_VAR_DEC):
            res = self.variableLong()
        elif self.current_tok.type in (TT_IDENTIFIER):
            if self.tokens[self.token_idx+1].type in (TT_VAR_VAL_ASSIGN):
                res = self.variableShort()
            else:
                res = self.variable()
        elif self.current_tok.type in (GP_COMPARISON):
            res = self.comparison()
        elif self.current_tok.type in (*GP_BOOLEAN_LONG, *GP_BOOLEAN_SHORT, *GP_BOOLEAN_INF):
            res = self.boolean()
        elif self.current_tok.type in (TT_TYPECAST_2):
            res = self.typecast()
        elif self.current_tok.type in (TT_SWITCH):
            res = self.switch()
        elif self.current_tok.type in (TT_STR_DELIMITER):
            res = self.string()
        elif self.current_tok.type in (TT_LOOP_STRT):
            res = self.loop()
        elif self.current_tok.type in (TT_IF):
            res = self.ifelse()
        elif self.current_tok.type in (TT_CONCAT):
            res = self.concatenation()

        return StatementNode("",res)