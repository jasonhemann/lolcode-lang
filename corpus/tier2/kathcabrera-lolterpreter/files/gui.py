import tkinter as tk
from PIL import Image
from tkinter import filedialog
import lol_lexer as lexer
import parser_try as parser
from parser_try import ScanError
from parser_try import ParseError
from tkinter import simpledialog
import re

# Source - https://www.w3resource.com/python-exercises/tkinter/python-tkinter-dialogs-and-file-handling-exercise-3.php

class RuntimeError(Exception): ...
class MultiList:
    def __init__(self, parent, title, name1, name2, side):
        self.parent = parent
        self.title = title
        self.name1 = name1
        self.name2 = name2
        self.list1 = 0
        self.list2 = 0
        self.scrollbar = 0
        self.side = side
    
    def clear(self):
        self.list1.delete(0, tk.END)
        self.list2.delete(0, tk.END)

    def populate(self, iterable):
        if len(iterable) == 0:
            self.list1.insert(tk.END, "None")
            self.list2.insert(tk.END, "None")
            
        
        elif type(iterable) is dict:
            for k, v in iterable.items():
                self.list1.insert(tk.END, k)
                self.list2.insert(tk.END, v)
            
                
        elif isinstance(iterable[0], lexer.Token):
            for i in range(0, len(iterable)):
                self.list1.insert(tk.END, iterable[i].lexeme)
                self.list2.insert(tk.END, iterable[i].type)


    def scroll_all(self, *args):
        self.list1.yview(*args)
        self.list2.yview(*args)
    
    def make(self):
        main_frame = tk.Frame(self.parent)
        sub_frame = tk.Frame(main_frame)
        left_list = tk.Frame(sub_frame)
        right_list = tk.Frame(sub_frame)

        title = tk.Label(main_frame, text=self.title)
        title.pack()

        self.list1 = tk.Listbox(left_list, width=27, height=15)
        name1 = tk.Label(left_list, text=self.name1)
        self.list1.pack(side=tk.BOTTOM)
        name1.pack(side=tk.TOP)


        self.list2 = tk.Listbox(right_list, width=27, height=15)
        name2 = tk.Label(right_list, text=self.name2)
        self.list2.pack(side=tk.BOTTOM)
        name2.pack(side=tk.TOP)

        self.scrollbar = tk.Scrollbar(sub_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.list1.config(yscrollcommand=self.scrollbar.set)
        self.list2.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.scroll_all)

        left_list.pack(side=tk.LEFT)
        right_list.pack(side=tk.LEFT)
        sub_frame.pack()
        main_frame.pack(side=self.side, pady=6)

# taken from www.w3resource.com
def select_file():
    file_path = filedialog.askopenfilename(title="Select a File", filetypes=[("LOL files", "*.lol"), ("All files", "*.*")])
    if file_path:
        file_label.config(text=f"{file_path}")
        process_file(file_path)

# taken from www.w3resource.com
def process_file(file_path):
    # Implement your file processing logic here
    # For demonstration, let's just display the contents of the selected file
    try:
        with open(file_path, 'r') as file:
            file_contents = file.read()
            textEditor.delete('1.0', tk.END)
            textEditor.insert(tk.END, file_contents)
    except Exception as e:
        file_label.config(text=f"Error: {str(e)}")

def update_symboltable(symbols):
    symbols_listbox.clear()
    symbols_listbox.populate(symbols)
    return

def arith(op, a, b):
    to_cast = a if isinstance(b, str) else b
    if a == "WIN":
        a = 1
    elif a in ("FAIL", "NOOB", ""):
        a = 0
    if b == "WIN":
        b = 1
    elif b in ("FAIL", "NOOB", ""):
        b = 0
    
    a = makeDigit(a)
    b = makeDigit(b)

    if isinstance(to_cast, int) or (isinstance(a, str) and isinstance(b, str)):
        a = int(a)
        b = int(b)
    elif isinstance(to_cast, float):
        a = float(a)
        b = float(b)

    if op == "SUM_OF":      return (a or 0) + (b or 0)
    if op == "DIFF_OF":     return (a or 0) - (b or 0)
    if op == "PRODUKT_OF":  return (a or 0) * (b or 0)
    if op == "QUOSHUNT_OF": return (a or 0) / (b or 1)
    if op == "MOD_OF":      return (a or 0) % (b or 1)
    if op == "BIGGR_OF":    return a if a >= b else b
    if op == "SMALLR_OF":   return a if a <= b else b

def bool_op(op, a, b):
    if isinstance(a, str):
        a = 0 if a == "" or a == "NOOB" or a == "FAIL" else 1
    if isinstance(b, str):
        b = 0 if b == "" or b == "NOOB" or b == "FAIL" else 1

    if op == "BOTH_OF":   return bool(a) and bool(b)
    if op == "EITHER_OF": return bool(a) or bool(b)
    if op == "WON_OF":    return bool(a) ^ bool(b)
    if op == "NOT":       return not bool(a)

def compare(op, a, b):
    if op == "BOTH_SAEM":    return a == b
    if op == "DIFFRINT":    return a != b

def cast(v, t):
    if t == "NUMBR": return 0 if v == "NOOB" else int(v)
    if t == "NUMBAR": return 0.0 if v == "NOOB" else float(v)
    if t == "YARN":  return "" if v == "NOOB" else str(v)
    if t == "TROOF": return False if v == "NOOB" else bool(v)
    return v

def makeDigit(value):
    if isinstance(value, int) or isinstance(value, float):
        return value
    NUMBAR_RE = r'-?(?:\d+\.\d*|\.\d+)(?:[eE][+-]?\d+)?' #floats
    NUMBR_RE  = r'-?\d+' #integers

    if re.search(NUMBAR_RE, value):
        return float(value)
    if re.search(NUMBR_RE, value):
        return int(value)
    
    raise RuntimeError(f"Runtime Error: Cannot implicitly cast `{value}` to digit ")

# should be kinda same as in the parser's var_eval_expr()
# untested
def eval_expr(tup, symbols):
    # print(tup)
    if tup[0] == "Identifier":
        return symbols[tup[1]]
    if tup[0] in ("Integer", "Float", "String", "Boolean"):
        return tup[1]
    if tup[0] == "CAST":
        #    [0]       [1][0]       [1][1]       [2][0]         [2][1]
        # ("CAST", (<Current_Type>, <Value>), ("Target Type", <Target_Type))
        return cast(eval_expr(tup[1], symbols), tup[2][1])
    
    if tup[0] in ("SUM_OF","DIFF_OF","PRODUKT_OF","QUOSHUNT_OF","MOD_OF","BIGGR_OF","SMALLR_OF"):
        return arith(tup[0], eval_expr(tup[1], symbols), eval_expr(tup[2], symbols))
    
    if tup[0] in ("BOTH_OF","EITHER_OF","WON_OF","BIGGR_OF","SMALLR_OF"):
        return bool_op(tup[0], eval_expr(tup[1], symbols), eval_expr(tup[2], symbols))
    
    if tup[0] == "NOT":
        return bool_op(tup[0], eval_expr(tup[1], symbols), 1)
    
    if tup[0] in ("ALL_OF", "ANY_OF"):
        vals = []
        for i in range(1, len(tup)):
            result = eval_expr(tup[i], symbols)
            if result in ("", 0, 0.0, "FAIL", "NOOB"):
               vals.append(False)
            else:
               vals.append(True)           
        return all(vals) if tup[0] == "ALL_OF" else any(vals)
    
    if tup[0] in ("DIFFRINT", "BOTH_SAEM"):
        a = eval_expr(tup[1], symbols)
        b = eval_expr(tup[2], symbols)

        # return compare(tup[0], a, b)
        new_a = makeDigit(a)
        new_b = makeDigit(b)

        # if new_a and new_b:
        return compare(tup[0], new_a, new_b)
        # else:
        # #     # replace with yield Error
        #     print(f"Error at instruction {tup[0]}: Operand(s) is not NUMBR or NUMBAR")

    if tup[0] == "CONCATENATE":
        result = ""
        for i in range(1, len(tup)):
            result = result + eval_expr(tup[i], symbols)
        return result

def loop_code(operation, variable, symbols, *code_block):
    # run code block
    for i in range(0, len(code_block)):
        evaluate_ast(code_block[i], symbols)

    #increment or decrement
    if operation == "UPPIN":
        symbols[variable[1]] += 1
    else:
        symbols[variable[1]] -= 1
        
    update_symboltable(symbols)

def evaluate_ast(node, symbols):
    # parser.pp_tuple(node)
    instruction = node[0]
    children = []
    for i in range(1, len(node)):
        children.append(node[i])

    if instruction == "INPUT":
        if children[0] in symbols:  # children[0] is the variable name
            input = simpledialog.askstring(f"GIMMEH {children[0]}", "", parent=root)            
            if input is None:
                input = ""
            symbols[children[0]] = input
            update_symboltable(symbols)
            outputText.insert(tk.END, input+"\n")
        else:
            # replace this with a raise Error() later
            print(f"Variable identifier {children[0]} has not yet been declared")
    
    elif instruction == "LOOP":
        label = children[0][1]
        operation = children[1][0]
        if children[1][1][1] not in symbols:
            raise RuntimeError(f"Runtime Error: The variable '{children[1][1][1]}' has not yet been declared")
        variable = children[1][1]
        loop_type = children[2][0]
        expression = children[2][1]
        code_block = []
        for i in range(1, len(children[3])):
            code_block.append(children[3][i])

        # print(code_block)
        
        if loop_type == "WILE":
            while eval_expr(expression, symbols):
                loop_code(operation, variable, symbols, *code_block)
        else:       # loop_type == "TIL"
            while eval_expr(expression, symbols) == False:
                loop_code(operation, variable, symbols, *code_block)

    elif instruction == "ASSIGN":
        # children looks like 
        #      [0][0]      [0][1]    [1][0]       [1][1]
        # [("Identifier", <Value>), ("Value", <Expression>)]
        if children[0][1] in symbols:
            symbols[children[0][1]] = eval_expr(children[1][1], symbols)
            update_symboltable(symbols)
        else:
            # replace this with a raise Error() later
            print(f"Variable identifier {children[0]} has not yet been declared")

    elif instruction == "PERM_CAST":    # Explicit cast using I HAS A
        ident = children[0][1]
        type = children[1][1]
        if ident in symbols:
            symbols[ident] = cast(symbols[ident], type)
            update_symboltable(symbols)
        else:
            # replace this with a raise Error() later
            print(f"Variable identifier {children[0]} has not yet been declared")
    
    elif instruction in ("ARITH_OPERATION", "BOOL_OPERATION"):
        result = eval_expr(children[0], symbols)
        symbols["IT"] = result
        update_symboltable(symbols)
    
    elif instruction == "PRINT":
        to_print = ""
        for child in children:
            to_print = to_print + str(eval_expr(child, symbols))
        outputText.insert(tk.END, to_print+"\n")

def execute_code():
    # clear GUI
    lexemes.clear()
    symbols_listbox.clear()
    outputText.delete("1.0", tk.END)
    
    # Analyze
    try:
        tokens = lexer.clean_lex(textEditor.get("1.0", "end-1c"))        
    except ScanError as e:
        outputText.insert(tk.END, e)
    except Exception as e:        
        outputText.insert(tk.END, e)
    else:
        lexemes.populate(tokens)

        try:
            p = parser.Parser(tokens)
            ast = p.parse()
        except ParseError as e:
            outputText.insert(tk.END, e)
        except Exception as e:        
            outputText.insert(tk.END, e)
        else:
            if len(p.symbols) == 0:
                print(f"{p.symbols}")
                symbols_listbox.populate({"None": "None"})
            else:
                symbols_listbox.populate(p.symbols)
                parser.pp_tree(ast)
                # parser.pp_tuple(ast)
                print("=======================================")
            
            statement_list = ast[2]
            symbolTable = p.symbols

            try:
                for i in range(1, len(statement_list)):
                    evaluate_ast(statement_list[i], symbolTable)
            except Exception as e:
                outputText.insert(tk.End, e)
            except RuntimeError as e:
                outputText.insert(tk.End, e)

# ================================ GUI Widgets ================================
root = tk.Tk()

# Window properties
root.title("LOLterpreter")
root.geometry("1080x600+300+120")
root.config(bg="skyblue")

# Left frame content
left_frame = tk.Frame(root)

file_frame = tk.Frame(left_frame)

file_label = tk.Label(file_frame, width=48, text='(None selected)')
file_label.grid(row=0, column=0)
fileButton = tk.Button(file_frame, text="File Select", command=select_file)
fileButton.grid(row=0, column=1, padx=5)

file_frame.pack(side=tk.TOP, anchor=tk.NW)

# textEditor_frame =  tk.Frame(left_frame)
textEditor = tk.Text(left_frame, width=50, height=33)
textEditor.pack()
executeButton = tk.Button(left_frame, text="EXECUTE", width=45, command=execute_code)
executeButton.pack(padx=5, pady=5)

left_frame.grid(row=0, column=0, sticky=tk.W+tk.E)


# Middle frame content
middle_frame = tk.Frame(root)

lexemes = MultiList(middle_frame, "LEXEMES", "Lexeme", "Classification", tk.TOP)
lexemes.make()

symbols_listbox = MultiList(middle_frame, "SYMBOL TABLE", "Identifier", "Value", tk.BOTTOM)
symbols_listbox.make()

middle_frame.grid(row=0, column=1, sticky=tk.W+tk.E)

# Right frame content
right_frame = tk.Frame(root)
outputText = tk.Text(right_frame, height=37, width=39)
outputText.pack()

right_frame.grid(row=0, column=2, sticky=tk.W+tk.E)


root.mainloop()
