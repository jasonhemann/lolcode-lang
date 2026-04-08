from lexer import Lexer, Token
from utils import Log
from time import sleep
from checker import *
# from syntax_tree import AST, Node

Log.show(True)

class Parser:
    def __init__(self, gui):
        self.gui = gui
        self.tokens = []
        self.cursor = 0
        self.current = None # self.tokens[self.cursor]

        self.flags = {
            'JMPOUT': False
        }

        _global_scope = {
            "vars": {},
            "loops": {},
            "funcs": {},
        }

        self.stack = [_global_scope]

        self.operations = {
            "SUM OF":       lambda a, b: a + b,
            "DIFF OF":      lambda a, b: a - b,
            "PRODUKT OF":   lambda a, b: a * b,
            "QUOSHUNT OF":  lambda a, b: a / b,
            "MOD OF":       lambda a, b: a % b,
            "BIGGR OF":     lambda a, b: max(a, b),
            "SMALLR OF":    lambda a, b: min(a, b),
            "NOT":          lambda a: not a
        }

        self.bool_operations = {
            "BOTH OF":      lambda a, b: a & b,
            "EITHER OF":    lambda a, b: a | b,
            "WON OF":       lambda a, b: a ^ b
        }

        Error.set_cout(gui)

    def _push(self, layer):
        self.stack.append(layer)

    def _pop(self):
        if len(self.stack) == 1:
            raise Exception(f"{self.current.pos()} Tried popping an empty stack")
        else: self.stack.pop()

    def _top_of_stack(self):
        return self.stack[-1]

    def set_tokens(self, _tokens):
        self.tokens = _tokens
        self.current = self.tokens[self.cursor]

    def next(self):
        "Moves to the next token by incrementing the cursor by 1"

        self.cursor += 1

        if self.cursor < len(self.tokens):
            self.current = self.tokens[self.cursor]
        else: raise Exception("Token overflow!")

    def seek(self, pos):
        "Moves to the cursor to `pos`, then updates the current token"

        self.cursor = pos

        if self.cursor < len(self.tokens):
            self.current = self.tokens[self.cursor ]
        else: raise Exception("Token overflow!")
    
    def curr_node(self):
        return self.tokens[self.cursor]

    def expect(self, *token_types, lexeme=None, consume=True, required=True):
        """
        Checks whether the token at the cursor:
        1. has the specified lexeme, or
        2. are specific type/s of tokens

        ### Parameters
        - `lexeme: str` specifies a lexeme to match in the current token
        - `token_types: varargs` - specify any number of Token types to accept as valid
        - `consume: bool` determines whether to move to next token if
                    expectation was satisfied
        - `required: bool` determines whether an error should be raised if
                    expectation was satisfied
        ### Usage
            self.expect(Token.KEYWORD, "HAI") # The current token needs to specifically be a "HAI" keyword
            self.expect(Token.NUMBAR) # The current token has to be a NUMBAR literal
        ### Return
            True if expectations were met, otherwise False
        """
        if lexeme != None and self.current.lexeme != lexeme:
            if required:
                raise SyntaxError(self.current, lexeme)
            else: return None

        if self.current.type not in token_types:
            if required:
                raise SyntaxError(current=self.current, expected=token_types)
            else: return None

        got = self.current.lexeme

        if consume: self.next()

        return got
    
    # Used for expecting non-terminals
    def accept(self, abstraction, err_msg=f"Unexpected non-terminal!"):
        _accept = abstraction()

        # Exempt expr() since it is allowed to return 'None' as (NOOB)
        if abstraction != self.expr:
            if _accept == None:
                Log.e(err_msg)
                raise UnknownError(current=self.current)
        else:
            # Implicitly assign to IT the resulting value of an expression
            self._set("IT", _accept)
        
        return _accept
    
    '''-----------------------------------------------------------------------------------# 
    In recursive descent, each function represents a non-terminal symbol in the grammar.
    The expansion/s of each non-terminal symbol is handled inside the functions.

    This implementation of recursive descent could be more intuitive 
    when constructing the Abstract Syntax Tree.
    #-----------------------------------------------------------------------------------'''

    def parse(self):
        "Call this function to begin parsing"
        self._set("IT", 0)
        self.program()

    def program(self):
        while self.expect(Token.NEWLINE, required=False):
            pass

        self.expect(Token.KEYWORD, "HAI")
        self.expect(Token.NUMBAR, required=False)
        self.linebreak()

        # Variable Declarations
        self.expect(Token.KEYWORD, lexeme="WAZZUP")
        self.linebreak()
        while not self.expect(Token.KEYWORD, lexeme="BUHBYE", required=False):
            self.expect(Token.KEYWORD, "I HAS A")
            self.accept(self.declare, err_msg="Expected assignment statement")
            self.linebreak()
        
        # Program Body
        while not self.expect(Token.KEYWORD, lexeme="KTHXBYE", consume=False, required=False):
            self.accept(self.statement, err_msg="Statement not recognized")
        
        self.gui.cout("\n========= [ Execution Finished ] =========")
        Log.yell("End.")
        return True
    
    def linebreak(self):
        br = False
        while has_newline := self.expect(Token.NEWLINE, required=False):
            br |= has_newline != None
        return br
    
    def expr(self):
        '''
        Not calling expr() using accept() by passes the assignment to IT after evaluation
        '''
        if operation := self.expect(Token.OPERATOR, required=False):
            op1 = self.accept(self.expr)
            Log.yell(f"OPERATION: {operation}")
            
            match operation:
                case "NOT":
                    op1 = self._cast(op1, "TROOF")
                    return not bool(op1)
                
                case "MAEK":
                    target = self.expect(Token.TYPE)
                    result = self._cast(op1, target)
                    self._set("IT", result)
                    return result
                
                case "ANY OF" | "ALL OF":
                    operands = []
                    
                    while not self.expect(Token.KEYWORD, lexeme="MKAY", required=False):
                        self.expect(Token.KEYWORD, lexeme="AN")
                        op = self.expr()
                        op = self._cast(op, "TROOF")
                        operands.append(op)

                    if operation == "ALL OF":
                        return all(operands)
                    elif operation == "ANY OF":
                        return any(operands)
                    
                case "SMOOSH":
                    operands = [op1]
                    
                    while self.expect(Token.KEYWORD, lexeme="AN", required=False):
                        op = self.accept(self.expr)
                        op = self._cast(op, "YARN")
                        operands.append(op)
                        
                    return "".join(operands)
            
            self.expect(Token.KEYWORD, lexeme="AN")

            op2 = self.accept(self.expr)

            if operation == "BOTH SAEM":
                Log.d(f"COMPARE: {repr(op1)}{self.typeof(op1)} == {repr(op2)}{self.typeof(op2)} -> {repr(op1) == repr(op2)}")
                return op1 == op2
            elif operation == "DIFFRINT":
                Log.d(f"COMPARE: {repr(op1)}{self.typeof(op1)} != {repr(op2)}{self.typeof(op2)} -> {repr(op1) != repr(op2)}")
                return op1 != op2

            if operation in self.operations:
                if self.typeof(op1) not in ("NUMBR", "NUMBAR"):
                    if op1 == None:
                        raise CastError(self.current, self.typeof(op1), target, op1)
                    op1 = self._cast(op1, "NUMBR")

                if self.typeof(op2) not in ("NUMBR", "NUMBAR"):
                    if op2 == None:
                        raise CastError(self.current, self.typeof(op2), target, op2)
                    op2 = self._cast(op2, "NUMBR")

                return self.operations[operation](op1, op2)
            
            elif operation in self.bool_operations:
                op1, op2 = self._cast(op1, "TROOF"), self._cast(op2, "TROOF")
                return self.bool_operations[operation](op1, op2)

        if got := self.expect(Token.NUMBAR, required=False):
            return float(got) 
        
        if got := self.expect(Token.NUMBR, required=False):
            return int(got) 
        
        if got := self.expect(Token.YARN, required=False):
            # Processing special characters
            got = str(got)
            got.replace(":)", "\n")
            got.replace(":>", "\t")
            got.replace(":\"", "\t")
            got.replace("::", ":")
            return str(got)
        
        if got := self.expect(Token.TROOF, required=False):
            return got == "WIN"
        
        if got := self.expect(Token.IDENTIFIER, required=False):
            _val = self._get(got)
            if _val == None:
                return "NOOB"
            else: 
                return _val
        
        return None

    def statement(self):
        # Create a branch for everyn statement ↓↓↓
        Log.i(f"Got statement: {self.current}")
        if self.expect(Token.KEYWORD, lexeme="KTHXBYE", consume=False, required=False):
            return None

        if self.expect(Token.KEYWORD, lexeme="I HAS A", required=False):
            raise IllegalDeclareError(current=self.current)
        
        # <operator> <x> AN <y> | <operator> <x1> AN <x2> ... <xn> | NOT <x>
        if self.expect(Token.OPERATOR, consume=False, required=False):
            Log.i(f"Got operation: {self.current.lexeme}")
            it = self.accept(self.expr, err_msg=f"Error evaluating expression")
            self._set("IT", it)

        # <varident> R <expr>
        if var := self.expect(Token.IDENTIFIER, required=False):
            self._set("IT", var)
            if self.expect(Token.KEYWORD, consume=False, required=False) in ("R", "IS NOW A"):
                self.accept(self.assign, err_msg=f"Error casting/assigning value to variable")
            else:
                self.accept(self.expr, err_msg=f"Error parsing expression")
        
        if self.expect(Token.KEYWORD, lexeme="VISIBLE", required=False):
            self.accept(self.print, err_msg="Error occurred while in VISIBLE")

        if self.expect(Token.KEYWORD, lexeme="GIMMEH", required=False):
            self.accept(self.input, err_msg="Error occurred while in GIMMEH")

        if self.expect(Token.KEYWORD, lexeme="O RLY?", required=False):
            self.accept(self.cond, err_msg="Error occurred while in O RLY?")

        if self.expect(Token.KEYWORD, lexeme="IM IN YR", required=False):
            self.accept(self.loop, err_msg="Error occurred while in IM IN YR")

        if self.expect(Token.KEYWORD, lexeme="MAEK", required=False):
            self.accept(self._cast, err_msg="Error occurred while in IM IN YR")
            
        if self.expect(Token.KEYWORD, lexeme="GTFO", required=False):
            self.flags["JMPOUT"] = True

        if self.expect(Token.KEYWORD, lexeme="HOW IZ I", required=False):
            self.accept(self.def_func, err_msg="Error occured while in I IZ")

        if self.expect(Token.KEYWORD, lexeme="I IZ", required=False):
            self.accept(self.call, err_msg="Error occured while in declaring function")

        if self.expect(Token.KEYWORD, lexeme="FOUND YR", required=False):
            self.accept(self.ret, err_msg="Error occured while in FOUND YR")

        if self.expect(Token.KEYWORD, lexeme="WTF?", required=False):
            self.accept(self.switch_case, err_msg="Error occured while in WTF?")
            
        return self.linebreak()

    def print(self):
        # first = self.accept(self.expr, f"Expected literal or <expr>, got {self.current.lexeme}")
        operands = [] # self._cast(first, "YARN")

        more, endl = True, True
        while more:
            op = self.accept(self.expr, err_msg="Expected: <expr>")
            converted = self._cast(op, "YARN")
            operands.append(converted)
            
            if self.expect(Token.DELIMITER, required=False):
                self.linebreak()
                more = False
                endl = False
            elif self.linebreak():
                more = False    
            elif self.expect(Token.CONCAT, Token.KEYWORD) not in ("+", "AN"):
                raise SyntaxError(self.current, "'+' or 'AN'")
        
        endl = '\n' if endl else ''
        buffer = "".join(operands) + endl
        self.gui.cout(buffer)
        print(buffer, end=endl)
            
        return True
    
    # Not an abstraction
    def _cast(self, val, target):
        match target:
            case "TROOF":
                if self.typeof(val) == "YARN":
                    if val == "WIN" or val == "FAIL":
                        return bool(val == "WIN")
                return bool(val)
            
            case "NUMBR":
                try:
                    return int(val)
                except ValueError:
                    try:
                        return float(val)
                    except ValueError:
                        raise CastError(self.current, self.typeof(val), target, val)
                
            case "NUMBAR":
                try:
                    return float(val)
                except ValueError:
                    # Try parsing to int()
                    try:
                        return int(val)
                    except ValueError:
                        raise CastError(self.current, self.typeof(val), target, val)
                
            case "YARN":
                match self.typeof(val):
                    case "NOOB":
                        return "NOOB"
                    case "TROOF":
                        return "WIN" if val else "FAIL"
                    case "NUMBR"| "NUMBAR" | "YARN":
                        return str(val)
                    
            case _:
                raise CastToUnknownTypeError(self.current, self.typeof(val), target, val)

    def _set(self, var, val):
        if var == "IT":
            self.stack[0]["vars"][var] = val
            self.gui.add_symbol(var, self._cast(val, "YARN"))
        else:
            self._top_of_stack()["vars"][var] = val
            self.gui.add_symbol(var, self._cast(val, "YARN"))

        Log.i(f"SET: {var} = {val}")

    def _set_loop(self, label, val):
        self._top_of_stack()["loops"][label] = val
        Log.i(f"SET LOOP: {label} = {val}")

    def _get(self, var):
        if var == "IT":
            Log.i(f"GET: {var} => {self.stack[0]["vars"][var]}")
            return self.stack[0]["vars"][var]
        
        if var not in self._top_of_stack()["vars"]:
            raise VariableError(current=self.current, var=var)
        
        Log.i(f"GET: {var} => {self._top_of_stack()["vars"][var]}")
        return self._top_of_stack()["vars"][var]
    
    def _get_loop(self, label):
        if label not in self._top_of_stack()["loops"]:
            raise LoopLabelError(current=self.current, label=label)
        
        # Log.i(f"GET: {var} => {self.loops[var]}")
        return self._top_of_stack()["loops"][label]
    
    def _get_func(self, func):
        if func not in self.stack[0]["funcs"]:
            raise FunctionUndefinedError(current=self.current, identifier=func)
        
        # Log.i(f"GET: {var} => {self.funcs[var]}")
        return self.stack[0]["funcs"][func]
    
    def _del_loop(self, label):
        if label not in self._top_of_stack()["loops"]:
            raise LoopLabelError(current=self.current, label=label)
        
        Log.i(f"DEL LOOP: {label}")
        del self._top_of_stack()["loops"][label]
    
    def assign(self):
        var = self._get("IT")
        operation = self.expect(Token.KEYWORD)
        
        if operation == "R":
            value = self.accept(self.expr, err_msg="Expected: <expr>")
            self._set(var, value)
        elif operation == "IS NOW A":
            target = self.expect(Token.TYPE)
            val = self._get(var)

            casted = self._cast(val, target)
            self._set(var, casted)
        else:
            raise SyntaxError(self.current, "'R' or 'IS NOW A'")
        
        return True
    
    def declare(self):
        var = self.expect(Token.IDENTIFIER)

        value = None
        if self.expect(Token.KEYWORD, lexeme="ITZ", required=False):
            value = self.accept(self.expr)

        self._set(var, value)

        return True
    
    def typeof(self, value):
        if value == None:
            return "NOOB"
        elif isinstance(value, bool):
            return "TROOF"
        elif isinstance(value, int):
            return "NUMBR"
        elif isinstance(value, float):
            return "NUMBAR"
        elif isinstance(value, str):
            return "YARN"
        
    def input(self):
        var = self.expect(Token.IDENTIFIER)
        _input = self.gui.cin()

        # Try parsing NUMBR or NUMBAR from input
        try:
            _input = int(_input)
        except ValueError:
            try:
                _input = float(_input)
            except ValueError:
                pass

        self._set(var, _input)

        return True

    # O RLY?
    def cond(self):
        if_start = int(self.cursor)
        win_branch, fail_branch, end = None, None, None
        mebbe = []

        while not self.expect(Token.KEYWORD, lexeme="OIC", required=False):
            Log.w(f"Current token: {self.current} (pos = {self.cursor})")

            match self.current.lexeme: 
                case "YA RLY": win_branch = int(self.cursor)
                case "NO WAI": fail_branch = int(self.cursor)
                case "MEBBE": mebbe.append(int(self.cursor))
            
            Log.w("Nexting")
            self.next()
        
        end = int(self.cursor)
        self.seek(if_start)
        Log.d(f"LEXEME AT START: {self.tokens[if_start]}")
        Log.d(f"BRANCHES: {list(map(lambda b: self.tokens[b], mebbe))}")

        JMP = None

        if self._get("IT"):
            JMP = win_branch
        
        if not JMP:
            for branch in mebbe:
                self.seek(branch + 1)
                if self.accept(self.expr, err_msg=f"{self.current.pos()} Error evaluating expression"):
                    JMP = branch
                    break
        
        if all([not JMP, fail_branch, not self._get("IT")]):
            JMP = fail_branch

        if not JMP:
            # Skip O RLY? block
            self.seek(end)
            return True
        
        JMP += 1 # So that it jumps straight to the branch body
        self.seek(JMP)

        # LOGIC FOR EACH BRANCH
        while not self.expect(Token.KEYWORD, consume=False, required=False) in ("MEBBE", "NO WAI", "OIC"):
            self.accept(self.statement, err_msg=f"{self.current.pos} Error evaluating statement in O RLY?")

        self.seek(end)
        Log.i(f"Exiting O RLY?... Now at {self.tokens[end]}")

        return True
    
    def loop(self):
        label = self.expect(Token.IDENTIFIER)

        operation = self.expect(Token.KEYWORD)
        if operation not in ("UPPIN", "NERFIN"): 
            raise SyntaxError(current=self.current.lexeme, expected="'UPPIN' or 'NERFIN'")

        self.expect(Token.KEYWORD, "YR")

        var = self.expect(Token.IDENTIFIER)

        cond = self.expect(Token.KEYWORD)
        if cond not in ("TIL", "WILE"):
            raise SyntaxError(current=self.current.lexeme, expected="TIL or WILE")
        
        # Jump to the conditional
        self._set_loop(label, int(self.cursor))
        end = None

        # Find the index of the IM OUTTA YR token
        for i in range(self._get_loop(label), len(self.tokens)):
            if self.tokens[i].lexeme == "IM OUTTA YR":
                if self.tokens[i+1].lexeme == label:
                    end = i + 2 # Skip IM OUTTA YR <label>
                    break

        if end == None: raise LoopUnclosedError(current=self.current, label=label)

        # Execute loop
        while True:
            # CONDITIONAL
            cond_result = self.accept(self.expr)

            if cond == "TIL" and cond_result:
                self.seek(end)
                break
            if cond == "WILE" and not cond_result:
                self.seek(end)
                break

            # LOOP BODY
            while not self.expect(Token.KEYWORD, lexeme="IM OUTTA YR", consume=False, required=False):
                self.accept(self.statement)

                # Handle GTFO
                if self.flags["JMPOUT"]:
                    self.flags["JMPOUT"] = False
                    break
            
            # INCREMENT/DECREMENT
            Log.d(f"{operation} {label}")
            if operation == "UPPIN":
                self._set(var, self._get(var) + 1)
            elif operation == "NERFIN":
                self._set(var, self._get(var) - 1)

            # Reset cursor to loop start
            self.seek(self._get_loop(label))

        Log.yell("Finished looping!")
        self._del_loop(label)

        return True
    
    def call(self):
        funcident = self.expect(Token.IDENTIFIER)
        jmp, params = self._get_func(funcident)

        # Initialize scope for function
        scope = {
            "name": funcident,
            "jmp": -1,
            "vars": {},
            "loop": {},
            "ret": -1
        }

        args = []
        # Put the arguments in a list
        while self.expect(Token.KEYWORD, lexeme="YR", required=False):
            arg = self.accept(self.expr, err_msg="Error in accepting arguments")

            args.append(arg)
            
            if not self.expect(Token.KEYWORD, lexeme="AN", required=False):
                break

        if len(args) != len(params):
            raise ArgumentMismatchError(self.current, len(args), len(params))
        
        # Map each argument to its corresponding parameter
        for param, arg in zip(params, args):
            scope["vars"][param] = arg
        
        # Position where the cursor will jump to after returning from function
        ret = int(self.cursor)

        # Defines the index of the start of the function body in the token list
        scope["jmp"] = jmp  
        scope["ret"] = ret

        # Go back to the position where the function was called
        self._push(scope)
        self.seek(self._top_of_stack()["jmp"])

        # Run function body
        while not self.expect(Token.KEYWORD, lexeme="IF U SAY SO", consume=False, required=False):
            self.accept(self.statement, err_msg=f"Error encountered in {self.current.pos()} {funcident}()")
            if self.flags["JMPOUT"]: 
                self.flags["JMPOUT"] = False
                break
        
        # Go back to the position where the function was called
        # Then pop the function scope from the stack
        self.seek(self._top_of_stack()["ret"])
        self._pop()

        return True
    
    def def_func(self):
        funcident = self.expect(Token.IDENTIFIER)

        params = []
        while self.expect(Token.KEYWORD, lexeme="YR", required=False):
            param = self.expect(Token.IDENTIFIER)
            params.append(param)
            if not self.expect(Token.KEYWORD, lexeme="AN", required=False):
                break
        jmp = int(self.cursor)
        
        self.stack[0]["funcs"][funcident] = (jmp, params)

        while not self.expect(Token.KEYWORD, lexeme="IF U SAY SO", required=False):
            self.next()

        return True

    def ret(self):
        # Assign return value to [IT]
        ret_val = self.accept(self.expr, err_msg=f"{self.current.pos()} Invalid return value")
        self._set("IT", ret_val)

        # Set JMP flag
        self.flags["JMPOUT"] = True
        return True
    
    def switch_case(self):
        case_matched = False  # Flag to track if a case is matched
        # gtfoed = False

        # Get all cases (OMG)
        default = None
        cases = []

        # Scan the entire WTF?...OIC block find jump points (OMG, OMGWTF)
        while not self.expect(Token.KEYWORD, lexeme="OIC", consume=False, required=False):
            Log.w(f"Current token: {self.current} (pos = {self.cursor})")

            match self.current.lexeme: 
                case "OMG": 
                    cases.append(int(self.cursor))
                case "OMGWTF": 
                    default = int(self.cursor)
            self.next()

        end = int(self.cursor) + 1      # Index of OIC
        cond = self._get("IT")          # Store value needed to match

        # If we encounter OMG, we are now in a case block
        for case in cases:
            self.seek(case + 1)
            case_value = self.expr()

            Log.i(f"IT value: {case_value}")
            if cond == case_value:
                Log.i(f"Case matched: {case_value} == {cond}")
                case_matched = True
                while not self.cursor in cases and self.cursor != default:
                    # Execute the statements inside the OMG block
                    self.accept(self.statement)

                    # Handle GTFO
                    if self.flags["JMPOUT"]:
                        break
                self.seek(end)

            if self.flags["JMPOUT"]:
                self.flags["JMPOUT"] = False
                Log.d("GTFO encountered, exiting case...")
                self.seek(end)
                break
        
        if not case_matched and default != None:
            self.seek(default + 1)

            # If we've reached the OIC keyword, exit the loop
            while not self.expect(Token.KEYWORD, lexeme="OIC", required=False):
                # Execute the statements inside the OMGWTF block
                self.accept(self.statement)

                # Handle GTFO
                if self.flags["JMPOUT"]:
                    self.flags["JMPOUT"] = False
                    Log.d("GTFO encountered, exiting case...")
                    Log.w(f"OMGWTFCurrent lexeme at END: {self.current.lexeme}")
                    self.seek(end)
                    break

        self.linebreak()

        return True
    
# --- DEBUG ---
# tokens = Lexer(open("project-testcases/05_bool.lol", "r")).get_tokens()
# success = Parser().parse()
# # Log.yell(f"Parsing completed successfully! ({success})")