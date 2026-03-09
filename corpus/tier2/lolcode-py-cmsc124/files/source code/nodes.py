from token_types import *
from error import *
from tkinter import *
from tkinter import simpledialog

IS_OPERATING = False

IT = "IT"
NOOB = "NOOB"
NUMBAR = "NUMBAR"
NUMBR = "NUMBR"
YARN = "YARN"
TROOF = "TROOF"

def resetSymbolTable():
    global SYMBOL_TABLE
    SYMBOL_TABLE = {}


def toBool(value):
    return True if value == "WIN" else False


def toTroof(value):
    return "WIN" if value else "FAIL"


def toValue(inputValue):
    if isinstance(inputValue,(ArithmeticNode,ComparisonNode,BooleanNode)):
        return inputValue.value
    elif isinstance(inputValue, VariableNode):
        if inputValue.token.val not in SYMBOL_TABLE:
            raise ErrorSemantic(inputValue.token,"Variable not Initialized")

        return SYMBOL_TABLE[inputValue.token.val]["value"]
    elif isinstance(inputValue,TroofNode):
        return inputValue.token.val
    elif isinstance(inputValue,LiteralNode):
        return inputValue.value
    

    return inputValue.token.val


class BasicNode:
    def __init__(self,token):
        self.token = token

    def __repr__(self) -> str:
        return f'({self.token})'

    def run(self):
        pass


class UnaryOpNode:
    def __init__(self,left, right):
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return f'({self.left}, {self.right})'

    def run(self):
        pass


class BinOpNode:
    def __init__(self, OP_TOKEN, EXPR1, AN, EXPR2) -> None:
        self.OP_TOKEN = OP_TOKEN
        self.EXPR1 = EXPR1
        self.AN = AN
        self.EXPR2 = EXPR2

    def __repr__(self) -> str:
        return f'({self.OP_TOKEN}, {self.EXPR1}, {self.AN}, {self.EXPR2})'

    def run(self):
        pass


class DoubleOpNode:
    def __init__(self, left, middle, right) -> None:
        self.left = left
        self.middle = middle
        self.right = right

    def __repr__(self) -> str:
        return f'({self.left}, {self.middle}, {self.right})'

    def run(self):
        pass


class Program(DoubleOpNode):
    def __init__(self, start_node, body_node,end_node, tbl_sym) -> None:
        super().__init__(start_node, body_node, end_node)
        self.tbl_sym = tbl_sym
        self.run()

    def run(self):
        for statement in self.middle:
            statement.run()

        #  printST()

        if self.tbl_sym is not None:
            # clear previous items in the lexemes treeview
            for x in self.tbl_sym.get_children():
                self.tbl_sym.delete(x)

            for index,key in enumerate(SYMBOL_TABLE):
                if SYMBOL_TABLE[key]["type"] == YARN:
                    self.tbl_sym.insert("",'end',iid=index,
                    values=(key,"\""+str(SYMBOL_TABLE[key]["value"])+"\""))
                else:
                    self.tbl_sym.insert("",'end',iid=index,
                    values=(key,SYMBOL_TABLE[key]["value"]))


class LiteralNode:
    def run(self):
        pass


# NULL
class NoobNode(LiteralNode):
    def __init__(self):
        self.value: None = None


# INTEGERS
class NumbrNode(BasicNode,LiteralNode):
    def __init__(self, token):
        super().__init__(token)
        self.value: int = int(token.val)


# FLOATS
class NumbarNode(BasicNode,LiteralNode):
    def __init__(self, token):
        super().__init__(token)
        self.value: float = float(token.val)


#"STRINGBODY"
class YarnNode(BasicNode,LiteralNode):
    def __init__(self, token) -> None:
        super().__init__(token)
        self.value: str = str(token.val)
        #  SYMBOL_TABLE[IT] = {"type": YARN, "value": self.value}


#TRUE OR FALSE
class TroofNode(BasicNode,LiteralNode):
    def __init__(self, token):
        super().__init__(token)
        self.value = True if self.token.val == "WIN" else False


class OperatorNode(BasicNode):
    def __init__(self, token):
        super().__init__(token)


class VariableNode(BasicNode):
    def __init__(self, token):
        super().__init__(token)

    def run(self):
        if not IS_OPERATING:
            if self.token.val not in SYMBOL_TABLE:
                raise ErrorSemantic(self.token,"Variable not Initialized")
            SYMBOL_TABLE[IT] = {"type": SYMBOL_TABLE[self.token.val]['type'], "value": SYMBOL_TABLE[self.token.val]['value']}


class StatementNode(UnaryOpNode):
    def __init__(self, left, right):
        super().__init__(left, right)

    def run(self):
        if self.right != None:
            self.right.run()


#ARITHMETICOP EXPR AN EXPR
class ArithmeticNode(BinOpNode):
    def __init__(self, OP_TOKEN, EXPR1, AN, EXPR2) -> None:
        super().__init__(OP_TOKEN, EXPR1, AN, EXPR2)

    def run(self):
        self.EXPR1.run()
        self.EXPR2.run()

        left = self.check(self.EXPR1)
        right = self.check(self.EXPR2)

        isNumbar = self.isNumbar(left) or self.isNumbar(right)

        if self.OP_TOKEN.type in (TT_SUMMATION):
            self.value = eval(left + "+" + right)
        elif self.OP_TOKEN.type in (TT_SUB):
            self.value = eval(left + "-" + right)
        elif self.OP_TOKEN.type in (TT_MUL_OP):
            self.value = eval(left + "*" + right)
        elif self.OP_TOKEN.type in (TT_DIV_OP):
            if isNumbar:
                self.value = eval(left + "/" + right)
            else:
                if not int(left) < int(right):
                    self.value = eval(left + "//" + right)
                else:
                    self.value = float(left)/float(right)
        elif self.OP_TOKEN.type in (TT_MOD):
            self.value = eval(left + "%" + right)
        elif self.OP_TOKEN.type in (TT_MAX):
            self.value = max((eval(left),eval(right)))
        elif self.OP_TOKEN.type in (TT_MIN):
            self.value = min((eval(left),eval(right)))

        if isNumbar:
            SYMBOL_TABLE[IT] = {"type": NUMBAR, "value": self.value}
        else:
            SYMBOL_TABLE[IT] = {"type": NUMBR, "value": self.value}

    def isNumbar(self, value:str):
        return True if "." in value else False

    def check(self, INPUT):
        if isinstance(INPUT,ArithmeticNode):
            return str(INPUT.value)
        elif isinstance(INPUT, VariableNode):
            if INPUT.token.val not in SYMBOL_TABLE:
                raise ErrorSemantic(INPUT.token,"Variable not Initialized")
            if SYMBOL_TABLE[INPUT.token.val]['type'] in TROOF:
                raise ErrorSemantic(INPUT.token,"Variable contains TROOF. Unable to use Arithmetic operatons on TROOF")
            if SYMBOL_TABLE[INPUT.token.val]['type'] in NOOB:
                raise ErrorSemantic(INPUT.token,"Variable contains NOOB. Unable to use Arithmetic operatons on NOOB")
            try:
                float(SYMBOL_TABLE[INPUT.token.val]["value"])
            except ValueError:
                raise ErrorSemantic(INPUT.token,"Variable contains Yarn. Unable to use Arithmetic operations on Yarn")
            except TypeError:
                raise ErrorSemantic(INPUT.token,"Variable contains Nothing. Unable to use Arithmetic operations on Nothing")

            return str(SYMBOL_TABLE[INPUT.token.val]["value"])
        elif isinstance(INPUT,YarnNode):
            try:
                float(INPUT.token.val)
            except ValueError:
                raise ErrorSemantic(INPUT.token,"Unable to use Arithmetic operations on Yarn")
        elif isinstance(INPUT, TroofNode):
            if INPUT.token.val == "WIN":
                return "1"
            else:
                return "0"

        return str(INPUT.token.val)


#GIMMEH VAR
class GimmehNode(UnaryOpNode):
    def __init__(self, left, right, txt_console):
        super().__init__(left, right)
        self.txt_console = txt_console

    def run(self):
        if self.right.token.val not in SYMBOL_TABLE:
            raise ErrorSemantic(self.right.token,"Variable not Initialized")
        answer = simpledialog.askstring("Input", f"Value for: {self.right.token.val}")

        SYMBOL_TABLE[IT] = {"type": YARN, "value": answer}
        SYMBOL_TABLE[self.right.token.val]["type"] = YARN
        SYMBOL_TABLE[self.right.token.val]["value"] = answer

        self.txt_console.configure(state=NORMAL)
        self.txt_console.insert(INSERT,str(answer)+'\n')
        self.txt_console.configure(state=DISABLED)


#SMOOSH
class SmooshNode(UnaryOpNode):
    def __init__(self, left, right):
        super().__init__(left, right)

    def run(self):
        self.left.run()

        valueList = []
        valueList.append(self.check(self.left))

        for value in self.right:
            value.run()
            valueList.append(self.check(value))

        self.value = ''.join(valueList)

        SYMBOL_TABLE[IT] = {"type": YARN, "value": self.value}

    def check(self,value):
        if isinstance(value, VariableNode):
            if value.token.val not in SYMBOL_TABLE:
                raise ErrorSemantic(value.token,"Variable not Initialized")
            return str(SYMBOL_TABLE[value.token.val]["value"])
        elif isinstance(value,BooleanNode):
            return str(value.value)
        else:
            return str(value.token.val)


#VISIBLE
class VisibleNode(UnaryOpNode):
    def __init__(self, left, right, txt_console, suppress):
        super().__init__(left, right)
        self.txt_console = txt_console
        self.suppress = suppress

    def run(self):
        global IS_OPERATING
        IS_OPERATING = True
        output = []
        for value in self.right:
            value.run()
            if isinstance(value, VariableNode):
                if value.token.val not in SYMBOL_TABLE:
                    raise ErrorSemantic(value.token,"Variable not Initialized")
                output.append(str(SYMBOL_TABLE[value.token.val]["value"]))
            elif isinstance(value,(BooleanNode, SmooshNode, ArithmeticNode, ComparisonNode)):
                output.append(str(value.value))
            else:
                output.append(str(value.token.val))

        if not self.suppress:
            output.append('\n')

        if self.txt_console is None:
            # CLI
            print("".join(output))
        else:
            # GUI
            self.txt_console.configure(state=NORMAL)
            self.txt_console.insert(INSERT,"".join(output))
            self.txt_console.configure(state=DISABLED)

        IS_OPERATING = False


class AssignmentNode():
    def assign(self,VAR,EXPR):
        if EXPR == None or isinstance(EXPR, NoobNode):
            SYMBOL_TABLE[str(VAR.token.val)] = {"type": NOOB, "value": "NOOB"}

        elif isinstance(EXPR, ArithmeticNode):
            SYMBOL_TABLE[str(VAR.token.val)] = {"type": NUMBAR, "value": SYMBOL_TABLE[IT]["value"]}

        elif isinstance(EXPR, BooleanNode):
            SYMBOL_TABLE[str(VAR.token.val)] = {"type": TROOF, "value": SYMBOL_TABLE[IT]["value"]}

        elif isinstance(EXPR, VariableNode):
            if EXPR.token.val not in SYMBOL_TABLE:
                raise ErrorSemantic(EXPR.token,"Variable not Initialized")

            SYMBOL_TABLE[str(VAR.token.val)] = {"type": SYMBOL_TABLE[EXPR.token.val]["type"], "value": SYMBOL_TABLE[EXPR.token.val]["value"]}

        elif isinstance(EXPR, TroofNode):
            SYMBOL_TABLE[str(VAR.token.val)] = {"type": TROOF, "value": EXPR.token.val}

        elif isinstance(EXPR, TypecastNode):
            SYMBOL_TABLE[str(VAR.token.val)] = {"type": TROOF, "value": EXPR.value}

        elif EXPR.token.type in TT_INTEGER:
            SYMBOL_TABLE[str(VAR.token.val)] = {"type": NUMBAR, "value": int(EXPR.token.val)}
        
        elif EXPR.token.type in TT_FLOAT:
            SYMBOL_TABLE[str(VAR.token.val)] = {"type": NUMBR, "value": float(EXPR.token.val)}
        
        elif EXPR.token.type in TT_BOOLEAN:
            SYMBOL_TABLE[str(VAR.token.val)] = {"type": TROOF, "value": EXPR.token.val}

        else:
            if VAR.token.type not in TT_STRING:
                if VAR.token.val.isdigit():
                    SYMBOL_TABLE[str(VAR.token.val)] = {"type": NUMBAR, "value": eval(EXPR.token.val)}

            SYMBOL_TABLE[str(VAR.token.val)] = {"type": YARN, "value": EXPR.token.val}


#I HAS A Variable
class AssignmentShlongNode(UnaryOpNode,AssignmentNode):
    def __init__(self, IHASA, VAR):
        super().__init__(IHASA, VAR)

    def run(self):
        self.assign(self.right, None)


#I HAS A VAR ITZ EPXR
class AssignmentLongNode(BinOpNode,AssignmentNode):
    def __init__(self, IHASA, VAR, ITZ, EXPR) -> None:
        super().__init__(IHASA, VAR, ITZ, EXPR)

    def run(self):
        self.EXPR2.run()
        self.assign(self.EXPR1,self.EXPR2)


#VAR R EXPR
class AssignmentShortNode(DoubleOpNode,AssignmentNode):
    def __init__(self, left, middle, right) -> None:
        super().__init__(left, middle, right)

    def run(self):
        self.right.run()
        self.assign(self.left,self.right)


#OPERATION EXPR AN EXPR
class ComparisonNode(BinOpNode):
    def __init__(self, OP_TOKEN, EXPR1, AN, EXPR2) -> None:
        super().__init__(OP_TOKEN, EXPR1, AN, EXPR2)

    def run(self):
        self.EXPR1.run()
        self.EXPR2.run()

        left = toValue(self.EXPR1)
        right = toValue(self.EXPR2)
        output = None

        if self.OP_TOKEN.type in (TT_EQU_OP):
            output = eval(str(left) + "==" + str(right))
        elif self.OP_TOKEN.type in (TT_NEQU):
            output = eval(str(left) + "!=" + str(right))

        self.value = toTroof(output)
        SYMBOL_TABLE[IT] = {"type": TROOF, "value": self.value}


class BooleanNode():
    def tobool(self,INPUT):
        if isinstance(INPUT, ComparisonNode):
            INPUT.run()
            return True if SYMBOL_TABLE[IT]['value'] == "WIN" else False
        if isinstance(INPUT,NumbrNode):
            return False if INPUT.value == 0 else True
        return True if self.check(INPUT) == "WIN" else False

    def totroof(self,INPUT):
        return "WIN" if INPUT else "FAIL"

    def check(self, INPUT):
        if isinstance(INPUT,TroofNode):
            return str(INPUT.token.val)
        elif isinstance(INPUT, VariableNode):
            if INPUT.token.val not in SYMBOL_TABLE:
                raise ErrorSemantic(INPUT.token,"Variable not Initialized")

            if SYMBOL_TABLE[INPUT.token.val]["value"] not in ("WIN","FAIL"):
                raise ErrorSemantic(INPUT.token,"Variable contain Yarn. Unable to use Boolean operations on Yarn")

            return str(SYMBOL_TABLE[INPUT.token.val])
        elif isinstance(INPUT,YarnNode):
            if SYMBOL_TABLE[INPUT.token.val]["value"] not in ("WIN","FAIL"):
                raise ErrorSemantic(INPUT.token,"Unable to use Boolean operations on Yarn")

        elif isinstance(INPUT, NumbrNode) or isinstance(INPUT, NumbarNode):
            if INPUT.token.val == "0":
                return "FAIL"
            else:
                return "WIN"

        elif isinstance(INPUT, BooleanShortNode) or isinstance(INPUT, BooleanLongNode):
            INPUT.run()
            return SYMBOL_TABLE[IT]['value']


        raise ErrorSemantic(INPUT.token,"Invalid value for boolean operations")


class BooleanInfNode(UnaryOpNode, BooleanNode):
    def __init__(self, op_token, left, right):
        super().__init__(left,right)
        self.op_token = op_token

    def run(self):
        self.left.run()

        output = self.tobool(self.left)
        if self.op_token.type in (TT_AND_INF):
            for value in self.right:
                value.run()
                output = output and self.tobool(value)
        elif self.op_token.type in (TT_OR_INF):
            for value in self.right:
                value.run()
                output = output or self.tobool(value)

        self.value = self.totroof(output)
        SYMBOL_TABLE[IT] = {"type": TROOF, "value": self.value}


#
class BooleanLongNode(BinOpNode,BooleanNode):
    def __init__(self, OP_TOKEN, EXPR1, AN, EXPR2) -> None:
        super().__init__(OP_TOKEN, EXPR1, AN, EXPR2)

    def run(self):
        self.EXPR1.run()
        self.EXPR2.run()

        leftval = self.check(self.EXPR1)
        rightval = self.check(self.EXPR2)
        left = True if leftval == "WIN" else False
        right = True if rightval == "WIN" else False

        output = None

        if self.OP_TOKEN.type in (TT_AND):
            output = left and right
        elif self.OP_TOKEN.type in (TT_OR_OP):
            output = left or right
        elif self.OP_TOKEN.type in (TT_XOR):
            output = not (left or right)

        self.value = "WIN" if output else "FAIL"
        SYMBOL_TABLE[IT] = {"type": TROOF, "value": self.value}


#OPERATION EXPR
class BooleanShortNode(UnaryOpNode,BooleanNode):
    def __init__(self, left, right):
        super().__init__(left, right)

    def run(self):
        self.right.run()

        val = self.check(self.right)
        output = not val

        self.value = "WIN" if output else "FAIL"
        SYMBOL_TABLE[IT] = {"type": TROOF, "value": self.value}


class TypecastNode:
    def run(self,expr,token):
        expr.run()
        """ FIX ME PROPERLY """
        try:
            token.run()
        except:
            pass

        value = self.getValue(expr)
        originalType = self.getType(expr)
        newType = token.val

        self.value = self.getCastedValue(expr,value,originalType,newType)
        SYMBOL_TABLE[IT] = {"type": newType, "value": self.value}

        if isinstance(expr,VariableNode):
            SYMBOL_TABLE[str(expr.token.val)] = {"type": newType, "value": self.value}

    def getType(self,expr):
        if isinstance(expr,VariableNode):
            if expr.token.val not in SYMBOL_TABLE:
                raise ErrorSemantic(expr.token,"Variable not Initialized")
            return SYMBOL_TABLE[expr.token.val]["type"]
        elif isinstance(expr,(BooleanNode,ComparisonNode)):
            return TROOF
        elif isinstance(expr,SmooshNode):
            return YARN

    def getValue(self, expr):
        if isinstance(expr,VariableNode):
            if expr.token.val not in SYMBOL_TABLE:
                raise ErrorSemantic(expr.token,"Variable not Initialized")
            return SYMBOL_TABLE[expr.token.val]["value"]
        elif isinstance(expr,(BooleanNode,ComparisonNode)):
            return expr.val
        elif isinstance(expr,SmooshNode):
            return expr.val

    def getCastedValue(self,expr, value, originalType, newType):
        res = None
        if originalType == NOOB:
            if newType == "TROOF":
                res = False
            elif newType == "NUMBR":
                res = 0
            elif newType == "NUMBAR":
                res = 0
            elif newType == "YARN":
                res = ""
        elif originalType == NUMBR:
            if newType == "NUMBR":
                res = int(value)
            elif newType == "NUMBAR":
                res = float(value)
            elif newType == "YARN":
                res = str(value)
            elif newType == "NOOB":
                raise ErrorSemantic(expr.token,f"Unable to Typecast NUMBR {value} to NOOB")
        elif originalType == NUMBAR:
            if newType == "NUMBR":
                res = int(value)
            elif newType == "NUMBAR":
                res = float(value)
            elif newType == "YARN":
                res = str(value)
            elif newType == "NOOB":
                raise ErrorSemantic(expr.token,f"Unable to Typecast NUMBAR {value} to NOOB")
        elif originalType == YARN:
            if newType == "NUMBR":
                try:
                    int(value)
                except ValueError:
                    raise ErrorSemantic(expr.token,f"Unable to Typecast Yarn {value} to Numbr")
                res = int(value)
            elif newType == "NUMBAR":
                try:
                    float(value)
                except ValueError:
                    raise ErrorSemantic(expr.token,f"Unable to Typecast Yarn {value} to Numbar")
                res = float(value)
            elif newType == "YARN":
                res = str(value)

        return res


#MAEK EXPR AN TYPE
class TypecastLongNode(TypecastNode, BinOpNode):
    def __init__(self, OP_TOKEN, EXPR1, AN, EXPR2) -> None:
        super().__init__(OP_TOKEN, EXPR1, AN, EXPR2)

    def run(self):
        super().run(self.EXPR1,self.EXPR2)


#MAEK EXPR possible
class TypecastShortNode(TypecastNode,DoubleOpNode):
    def __init__(self, left, middle, right) -> None:
        super().__init__(left, middle, right)

    def run(self):
        super().run(self.middle,self.right)


#OPERATION EXPR
class SwitchNode(UnaryOpNode):
    def __init__(self, left, right):
        super().__init__(left, right)

    def run(self):
        didRun = False
        shouldContinue = False
        for statement in self.right:
            didRun, shouldContinue = statement.run(didRun, shouldContinue)
            if shouldContinue:
                continue
            if didRun:
                break


#OMG VALUE STATEMENT
class SwitchCaseNode(DoubleOpNode):
    def __init__(self, left, middle, right) -> None:
        super().__init__(left, middle, right)

    def run(self, didRun, continuee=False):
        if SYMBOL_TABLE[IT]['value'] == self.middle.value or (didRun and continuee):
            for statement in self.right:
                statement.run()
                if isinstance(statement,CaseBreakNode):
                    return True, False
            return True, True
        return False, False


#OMGWTF
class DefaultCaseNode(UnaryOpNode):
    def __init__(self, left, right):
        super().__init__(left, right)

    def run(self, didRun, shouldContinue = False):
        for statement in self.right:
            statement.run()
        return True, False

#
class CaseBreakNode(BasicNode):
    def __init__(self, token):
        super().__init__(token)

#ORLY
class IfElseNode(DoubleOpNode):
    def __init__(self, left, middle, right) -> None:
        super().__init__(left, middle, right)

    def run(self):
        for statement in self.middle:
            if statement.run():
                break

#ORLY
class IfNode(UnaryOpNode):
    def __init__(self, left, right):
        super().__init__(left, right)


    def run(self):
        if SYMBOL_TABLE[IT]['value'] == "WIN":
            for statement in self.right:
                statement.run()
            return True

        return False


#MEBBE VALUE ELSEBODY
class ElseIfNode(DoubleOpNode):
    def __init__(self, left, middle, right) -> None:
        super().__init__(left, middle, right)

    def run(self):
        self.middle.run()

        if SYMBOL_TABLE[IT]['value'] == "WIN":
            for statement in self.right:
                statement.run()

            return True
        return False


#NOWAI
class ElseNode(UnaryOpNode):
    def __init__(self, left, right):
        super().__init__(left, right)

    def run(self):
        for statement in self.right:
            statement.run()
        return False

# IM IN YR <label> <operation> YR <variable> [TIL|WILE <expression>]
# <code block>
# IM OUTTA YR <label>
class LoopNodeLong:
    def __init__(self, del_start, label_start, operation, yr, var, cond, cond_expr, codeblock, del_end, label_end) -> None:
        self.del_start = del_start
        self.label_start = label_start
        self.operation = operation
        self.yr = yr
        self.var = var
        self.cond = cond
        self.cond_expr = cond_expr
        self.codeblock = codeblock
        self.del_end = del_end
        self.label_end = label_end
    
    def run(self):
        value = 1 if self.operation.val == "UPPIN" else -1
        cond = True if self.cond.type == TT_UNTIL else False
        
        while True:
            self.cond_expr.run()

            if cond:
                if toBool(self.cond_expr.value):
                    break
            else:
                if not toBool(self.cond_expr.value):
                    break
            
            for statement in self.codeblock:
                statement.run()
            
            SYMBOL_TABLE[self.var.val]["value"] += value
            
    
    def __repr__(self) -> str:
        return f'({self.del_start}, {self.label_start}, {self.operation}, {self.yr}, {self.var}, {self.cond},{self.cond_expr},{self.codeblock}, {self.del_end})'


def printST():
    for key,value in SYMBOL_TABLE.items():
        print(key,value)


SYMBOL_TABLE = {
    IT: None
}
