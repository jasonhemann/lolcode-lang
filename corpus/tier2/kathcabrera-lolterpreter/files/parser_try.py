import re
from lol_lexer import Token, lex
from dataclasses import dataclass
from typing import Any, List, Tuple

class ScanError(Exception): ...
class ParseError(Exception): ...

# Token types that will be encountered as the first token of the line
INLINE_TYPES = ("VISIBLE", "IDENT", "GIMMEH", "+", "SMOOSH", "IS_NOW_A","SUM_OF","DIFF_OF","PRODUKT_OF","QUOSHUNT_OF","MOD_OF","BIGGR_OF","SMALLR_OF","BOTH_OF","EITHER_OF","WON_OF","NOT","ALL_OF","ANY_OF","BOTH_SAEM", "DIFFRINT", "SMOOSH", "IM_IN_YR", "HOW_IZ_I", "FOUND_YR", "GTFO", "I_IZ")

#ast helpers
def node(tag: str, *children: Any) -> Tuple[str, Any]:
    return (tag, *children)

def pp_tuple(ast):
    import pprint; pprint.pprint(ast, width=100)

def pp_tree(ast, indent=""):
    tag = ast[0]
    print(indent + tag)
    for child in ast[1:]:
        if isinstance(child, tuple):
            pp_tree(child, indent + "│   ")
        else:
            print(indent + "│   " + repr(child))

#parser and evaluator
class Parser:
    def __init__(self, toks: List[Token]):
        self.toks = toks
        self.i = 0
        self.symbols = {}   #symbol table

    #basic stream ops
    def peek(self, k=0): return self.toks[self.i + k]
    def at(self, *types): return self.peek().type in types
    def match(self, *types):
        if self.at(*types):
            t = self.peek(); self.i += 1; return t
        return None
    def need(self, *types):
        t = self.match(*types)
        if not t:
            got = self.peek()
            raise ParseError(f"Expected {'/'.join(types)} at {got.line}:{got.col}, got {got.type} {got.lexeme!r}")
        return t
    def skip_nl(self):
        while self.match("NEWLINE"): pass

    # Since we're using the old lexer, we don't need to parse for new lines
    def parse(self):
        # self.skip_nl()
        self.need("CODE_START")
        # self.need("NEWLINE")
        # self.skip_nl()
        self.symbols["IT"] = "NOOB"

        wazzup_decls = None
        if self.match("VARLIST_START"):
            # self.skip_nl()
            wazzup_decls = self.wazzup_block()             

        # inline_decls = self.variable_declaration_list_opt() 
        stmts        = self.statement_list_opt()            

        # self.skip_nl()
        self.need("CODE_END")
        # self.skip_nl()
        # self.need("EOF")

        # merge decl lists
        decls = None
        if wazzup_decls:
            decls = node("VARIABLE_DECLARATION_LIST", *wazzup_decls[1:])
        else:
            decls = node("VARIABLE_DECLARATION_LIST")
        # if wazzup_decls and inline_decls:
        #     decls = node("VARIABLE_DECLARATION_LIST", *wazzup_decls[1:], *inline_decls[1:])
        # else:
        #     decls = wazzup_decls or inline_decls or node("VARIABLE_DECLARATION_LIST")

        # return node("PROGRAM",
        #             decls,
        #             node("STATEMENT_LIST"))
        return node("PROGRAM",
                    decls,
                    stmts if stmts else node("STATEMENT_LIST"))


    #WAZZUP
    def wazzup_block(self):
        items = []
        while self.match("VAR_DECL"):
            # self.need("I"); self.need("HAS"); self.need("A")
            ident = self.need("IDENT").lexeme
            if self.match("VAR_ASSIGN_ITZ"):
                val = self.var_eval_expr()
                self.symbols[ident] = val
                items.append(node("VARIABLE", ("Identifier", ident), ("Value", val)))
            else:
                self.symbols.setdefault(ident, "NOOB")
                items.append(node("VARIABLE", ("Identifier", ident)))
            self.skip_nl()
        self.need("VARLIST_END")
        # self.skip_nl()
        return node("VARIABLE_DECLARATION_LIST", *items)


    # Optional variable declarations
    def variable_declaration_list_opt(self):
        while self.peek().type == "I":
            self.need("I"); self.need("HAS"); self.need("A")
            ident = self.need("IDENT").lexeme
            if self.match("ITZ"):
                val = self.var_eval_expr()
                self.symbols[ident] = val
            else:
                self.symbols.setdefault(ident, None)
            self.skip_nl()

    # Statement list
    def statement_list_opt(self):
        items = []
        while self.peek().type in INLINE_TYPES:
            if self.at("VISIBLE"):
                items.append(self.print_stmt())
            elif self.at("GIMMEH"):
                items.append(self.input_stmt())
            elif self.at("SMOOSH"):
                items.append(self.concat_stmt())
            elif self.at("SUM_OF","DIFF_OF","PRODUKT_OF","QUOSHUNT_OF","MOD_OF","BIGGR_OF","SMALLR_OF"):
                items.append(node("ARITH_OPERATION", self.eval_expr()))
            elif self.at("BOTH_OF","EITHER_OF","WON_OF", "NOT","ALL_OF","ANY_OF","BOTH_SAEM", "DIFFRINT"):
                items.append(node("BOOL_OPERATION", self.eval_expr()))
            elif self.at("IM_IN_YR"):
                items.append(self.loop_stmt())
            elif self.at("HOW_IZ_I"):
                items.append(self.func_stmt())
            elif self.at("I_IZ"):
                items.append(self.call_stmt())
            else:
                if self.peek(1).type == "R":
                    items.append(self.assign_stmt())
                
                elif self.peek(1).type in ("IS_NOW_A", "MAEK_A"):
                    items.append(self.cast_stmt())
                else:
                    break
            # self.skip_nl()
        return node("STATEMENT_LIST", *items)

    def eval_codeblock(self):
        items = []
        while self.peek().type in INLINE_TYPES:
            if self.at("VISIBLE"):
                items.append(self.print_stmt())
            elif self.at("GIMMEH"):
                items.append(self.input_stmt())
            elif self.at("SMOOSH"):
                items.append(self.concat_stmt())
            elif self.at("SUM_OF","DIFF_OF","PRODUKT_OF","QUOSHUNT_OF","MOD_OF","BIGGR_OF","SMALLR_OF"):
                items.append(node("ARITH_OPERATION", self.eval_expr()))
            elif self.at("BOTH_OF","EITHER_OF","WON_OF", "NOT","ALL_OF","ANY_OF","BOTH_SAEM", "DIFFRINT"):
                items.append(node("BOOL_OPERATION", self.eval_expr()))
            elif self.at("IM_IN_YR"):
                items.append(self.loop_stmt())
            
            # for functions
            elif self.at("FOUND_YR"):
                items.append(self.return_stmt())
            elif self.at("GTFO"):
                items.append(node("BREAK"))
                self.need("GTFO")
            elif self.at("HOW_IZ_I"):
                items.append(self.call_stmt)

            else:
                if self.peek(1).type == "R":
                    items.append(self.assign_stmt())
                
                elif self.peek(1).type in ("IS_NOW_A", "MAEK_A"):
                    items.append(self.cast_stmt())
                else:
                    break
        return items

    def eval_parameter(self, acc: list):
        self.need("YR")
        acc.append(self.eval_expr())
        if self.at("AN"):
            self.need("AN")
            self.eval_parameter(acc)

    def call_stmt(self):
        self.need("I_IZ")
        func_name = self.eval_expr()
        args = []

        if self.at("YR"):
            self.eval_parameter(args)

        return node("CALL", func_name, ("Arguments", *args))      

    def loop_stmt(self):
        self.need("IM_IN_YR")
        name = self.need("IDENT").lexeme

        incr_decr = self.need("UPPIN", "NERFIN").lexeme
        self.need("YR")
        var = self.eval_expr()
        loop_type = self.need("TIL", "WILE").lexeme
        condition = self.eval_expr()

        items = self.eval_codeblock()

        self.need("IM_OUTTA_YR")
        out_name = self.need("IDENT").lexeme
        if name != out_name:
            raise ParseError(f"Expected token {name}, got {out_name}")
        
        return node("LOOP", ("Name", name), (incr_decr, var), (loop_type, condition), ("CODE_BLOCK", *items))
    
    def func_stmt(self):
        self.need("HOW_IZ_I")
        name = self.need("IDENT").lexeme
        
        parameters = []
        if self.at("YR"):
            self.eval_parameter(parameters)
        
        items = self.eval_codeblock()

        self.need("IF_U_SAY_SO")
        return node("FUNCTION", ("Name", name), ("Parameters", *parameters), ("CODE_BLOCK", *items))

    def return_stmt(self):
        self.need("FOUND_YR")
        return node("RETURN", self.eval_expr())

    def cast_stmt(self):
        ident = self.need("IDENT").lexeme
        self.need("IS_NOW_A")
        type = self.need("TYPE_LIT").lexeme
        return node("PERM_CAST", ("Identifier", ident), ("Target Type", type))

    def concat_stmt(self):
        self.need("SMOOSH")
        vals = []
        vals.append(self.eval_expr())
        while self.match("AN"):
            vals.append(self.eval_expr())
        return node("CONCATENATE", *vals)

    def input_stmt(self):
        self.need("GIMMEH")
        val = self.need("IDENT").lexeme

        return node("INPUT", val)

    def print_stmt(self):
        self.need("VISIBLE")

        vals = []
        
        vals.append(self.eval_expr())
        while self.match("+", "AN"):  
            vals.append(self.eval_expr())
        return node("PRINT", *vals)
                # items.append(node("VARIABLE", ("Identifier", ident), ("Value", val)))

    def assign_stmt(self):
        name = self.need("IDENT").lexeme
        self.need("R")
        val = self.eval_expr()
        # self.symbols[name] = val
        return node("ASSIGN", ("Identifier", name), ("Value", val))

    #  returns nodes for the AST, does not do actual computations
    def eval_expr(self):
        # literals
        if self.at("NUMBR_LIT"):
            return node("Integer", int(self.need("NUMBR_LIT").lexeme))
        if self.at("NUMBAR_LIT"):
            return node("Float", float(self.need("NUMBAR_LIT").lexeme))
        if self.at("YARN_LIT"):
            s = self.need("YARN_LIT").lexeme
            return node("String", bytes(s[1:-1], "utf-8").decode("unicode_escape"))
        if self.at("TROOF_LIT"):
            return node("Boolean", self.need("TROOF_LIT").lexeme)

        # identifier reference
        if self.at("IDENT"):
            # name = self.need("IDENT").lexeme
            # return self.symbols.get(name, None)
            return node("Identifier", self.need("IDENT").lexeme)

        # arithmetic binary
        if self.at("SUM_OF","DIFF_OF","PRODUKT_OF","QUOSHUNT_OF","MOD_OF","BIGGR_OF","SMALLR_OF"):
            op = self.peek().type; self.i += 1
            a = self.eval_expr(); self.need("AN"); b = self.eval_expr()
            # return self._arith(op, a, b)
            return node(op, a, b)

        # boolean binary
        if self.at("BOTH_OF","EITHER_OF","WON_OF"):
            op = self.peek().type; self.i += 1
            a = self.eval_expr(); self.need("AN"); b = self.eval_expr()
            # return self._bool(op, a, b)
            return node(op, a, b)
        if self.at("NOT"):
            # self.i += 1; return not self.eval_expr()
            self.i += 1; return node("NOT", self.eval_expr())
        
        if self.at("ALL_OF","ANY_OF"):
            op = self.peek().type; self.i += 1
            vals = [self.eval_expr()]; self.need("AN"); vals.append(self.eval_expr())
            while self.match("AN"): vals.append(self.eval_expr())
            self.need("MKAY")
            # return all(vals) if op == "ALL_OF" else any(vals)
            return node(op, *vals)

        # comparison
        if self.at("BOTH_SAEM"):
            # self.i += 1; a = self.eval_expr(); self.need("AN"); b = self.eval_expr(); return a == b
            self.i += 1; a = self.eval_expr(); self.need("AN"); b = self.eval_expr(); return node("BOTH_SAEM", a, b)
        if self.peek().lexeme == "DIFFRINT":   # tokenized as IDENT
            # self.i += 1; a = self.eval_expr(); self.need("AN"); b = self.eval_expr(); return a != b
            self.i += 1; a = self.eval_expr(); self.need("AN"); b = self.eval_expr(); return node("DIFFRINT", a, b)

        # concatenation
        if self.at("SMOOSH"):
            n = self.concat_stmt()
            return n

        # cast
        if self.at("MAEK_A"):
            # self.i += 1; v = self.eval_expr(); self.need("A"); t = self.need("TYPE").lexeme
            self.i += 1; v = self.eval_expr(); t = self.need("TYPE_LIT").lexeme
            # return self._cast(v, t)
            return node("CAST", v, ("Target Type", t))

        got = self.peek()
        raise ParseError(f"Unsupported expression at {got.line}:{got.col}: {got.lexeme!r}")

    # for evaluating expressions in the WAZZUP block only, does actual computations
    def var_eval_expr(self):
        # literals
        if self.at("NUMBR_LIT"):
            return int(self.need("NUMBR_LIT").lexeme)
        if self.at("NUMBAR_LIT"):
            return float(self.need("NUMBAR_LIT").lexeme)
        if self.at("YARN_LIT"):
            s = self.need("YARN_LIT").lexeme
            return bytes(s[1:-1], "utf-8").decode("unicode_escape")
        if self.at("TROOF_LIT"):
            troof = self.need("TROOF_LIT").lexeme
            return "True" if troof == "WIN" else "False"
        # identifier reference
        if self.at("IDENT"):
            name = self.need("IDENT").lexeme
            return self.symbols.get(name, None)

        # arithmetic binary
        if self.at("SUM_OF","DIFF_OF","PRODUKT_OF","QUOSHUNT_OF","MOD_OF","BIGGR_OF","SMALLR_OF"):
            op = self.peek().type; self.i += 1
            a = self.var_eval_expr(); self.need("AN"); b = self.var_eval_expr()
            return self._arith(op, a, b)
            # return node("ARITHMETIC OP", op, a, b)

        # boolean binary
        if self.at("BOTH_OF","EITHER_OF","WON_OF"):
            op = self.peek().type; self.i += 1
            a = self.var_eval_expr(); self.need("AN"); b = self.var_eval_expr()
            return self._bool(op, a, b)
            # return node("BOOLEAN OP", op, a, b)
        if self.at("NOT"):
            self.i += 1; return not self.var_eval_expr()
            # self.i += 1; return node("NOT", self.var_eval_expr())
        
        if self.at("ALL_OF","ANY_OF"):
            op = self.peek().type; self.i += 1
            vals = [self.var_eval_expr()]; self.need("AN"); vals.append(self.var_eval_expr())
            while self.match("AN"): vals.append(self.var_eval_expr())
            self.need("MKAY")
            return all(vals) if op == "ALL_OF" else any(vals)

        # comparison
        if self.at("BOTH_SAEM"):
            self.i += 1; a = self.var_eval_expr(); self.need("AN"); b = self.var_eval_expr(); return a == b
            # self.i += 1; a = self.var_eval_expr(); self.need("AN"); b = self.var_eval_expr(); return node("BOTH_SAEM", a, b)
        if self.peek().lexeme == "DIFFRINT":   # tokenized as IDENT
            self.i += 1; a = self.var_eval_expr(); self.need("AN"); b = self.var_eval_expr(); return a != b
            # self.i += 1; a = self.var_eval_expr(); self.need("AN"); b = self.var_eval_expr(); return node("DIFFRINT", a, b)

        # concatenation
        if self.at("SMOOSH"):
            self.i += 1
            parts = [str(self.var_eval_expr())]
            while self.match("AN"): parts.append(str(self.var_eval_expr()))
            self.need("MKAY"); return "".join(parts)
            # parts = ()
            # while self.match("AN"): parts.append(self.var_eval_expr())
            # self.need("MKAY")
            # return node("SMOOSH", parts)

        # cast
        if self.at("MAEK_A"):
            # self.i += 1; v = self.var_eval_expr(); self.need("A"); t = self.need("TYPE").lexeme
            self.i += 1; v = self.var_eval_expr(); t = self.need("TYPE_LIT").lexeme
            return self._cast(v, t)
            # return node("CAST", ("VALUE", v), ("TARGET_TYPE", t))

        got = self.peek()
        raise ParseError(f"Unsupported expression at {got.line}:{got.col}: {got.lexeme!r}")

    def _arith(self, op, a, b):
        if op == "SUM_OF":      return (a or 0) + (b or 0)
        if op == "DIFF_OF":     return (a or 0) - (b or 0)
        if op == "PRODUKT_OF":  return (a or 0) * (b or 0)
        if op == "QUOSHUNT_OF": return (a or 0) / (b or 1)
        if op == "MOD_OF":      return (a or 0) % (b or 1)
        if op == "BIGGR_OF":    return a if a >= b else b
        if op == "SMALLR_OF":   return a if a <= b else b

    def _bool(self, op, a, b):
        if op == "BOTH_OF":   return bool(a) and bool(b)
        if op == "EITHER_OF": return bool(a) or bool(b)
        if op == "WON_OF":    return bool(a) ^ bool(b)

    def _cast(self, v, t):
        if t == "NUMBR": return int(v)
        if t == "NUMBAR": return float(v)
        if t == "YARN":  return "" if v is None else str(v)
        if t == "TROOF": return bool(v)
        return v
