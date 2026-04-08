import tkinter as Tk
from tkinter import Frame, Button, Label, Text, Entry, filedialog, simpledialog, StringVar, END
from tkinter.ttk import Treeview
import platform

from pathlib import Path
from os.path import abspath
import ctypes   

from lexer import Lexer
from parser import Parser
from utils import Log

# Check if the OS is Windows before calling SetProcessDpiAwareness
if platform.system() == "Windows":
    ctypes.windll.shcore.SetProcessDpiAwareness(1)

class LOLCodeInterpreter:
    def __init__(self):
        pane_pad = 8

        self.root = Tk.Tk()
        self.root.title("LOLSPEAKER")

        self.frame = Frame(self.root)
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        self.frame.columnconfigure(2, weight=1)
        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(2, weight=1)
        self.frame.pack()

        # SOURCE PANE
        self.pane_source = Frame(self.frame)
        self.pane_source.grid(row=0, column=0, padx=pane_pad, pady=pane_pad)

        self.file_picker_row = Frame(self.pane_source)
        self.file_picker_row.pack(side="top", fill="x", expand=True)

        self.file_picker_path = StringVar(value="")
        self.file_picker_text = Entry(self.file_picker_row, textvariable=self.file_picker_path, state="disabled")
        self.file_picker_text.pack(side="left", fill="both", expand=True)

        self.import_btn = Button(self.file_picker_row, text="Import", command=self.import_file)
        self.import_btn.pack(side="right")
        
        self.editor = Text(self.pane_source, wrap="char", font=("Consolas"))
        self.editor.pack(side="bottom")

        # LEXEME TABLE PANE
        self.pane_lexemes = Frame(self.frame)
        self.pane_lexemes.grid(row=0, column=1, sticky="ns", padx=pane_pad, pady=pane_pad)

        self.label_lexemes = Label(self.pane_lexemes, text="Lexemes")
        self.label_lexemes.pack(side="top")

        self.lexeme_table = Treeview(self.pane_lexemes, columns=("frequency"))
        self.lexeme_table.heading("#0", text="Lexeme")
        self.lexeme_table.heading("frequency", text="Classification")
        self.lexeme_table.pack(fill="y", expand=True)

        # SYMBOL TABLE PANE
        self.pane_symbols = Frame(self.frame)
        self.pane_symbols.grid(row=0, column=2, sticky="ns", padx=pane_pad, pady=pane_pad)

        self.label_symbols = Label(self.pane_symbols, text="Symbols")
        self.label_symbols.pack(side="top")

        self.symbol_table = Treeview(self.pane_symbols, columns=("value"))
        self.symbol_table.heading("#0", text="Identifier")
        self.symbol_table.heading("value", text="Value")
        self.symbol_table.pack(fill="both", expand=True)

        # EXECUTE BUTTON
        self.execute_btn = Button(self.frame, text="Execute", command=self.execute)
        self.execute_btn.grid(row=1, column=0, columnspan=3, sticky="ew", pady=pane_pad, padx=pane_pad)

        # CONSOLE
        self.buffer = ""
        self.console = Text(self.frame, wrap="char", bg="#000000", fg="#ffffff", font=("Consolas"))
        self.console.grid(row=2, column=0, columnspan=3, sticky="ews", padx=pane_pad, pady=pane_pad)
        # self.console["state"] = "disabled"
        # self.console.bind("<Key>", self.capture_input)
        
    def start(self):
        self.root.mainloop()

    def add_symbol(self, var, val):
        try:
            self.symbol_table.item(var, values=(val,))
            Log.i(f"Updated {var}!")
        except:
            self.symbol_table.insert('', END, iid=var, text=var, values=(val,))
            Log.i(f"Added {var}!")

    def remove_symbol(self):
        pass

    def import_file(self):
        # Accept only .lol or .lols files
        file = filedialog.askopenfile(filetypes=[("LOLCODE File", "*.lol"), ("LOLCODE File", "*.lols")])

        # Display the absolute file of the selected file
        self.file_picker_path.set(str(abspath(file.name)))

        # Clear editor
        self.editor.delete('1.0', END)

        # Load source code from file
        source_code = file.read()

        # Append source code to editor
        self.editor.insert(END, source_code)

    def cout(self, str):
        ''' Prints to the console '''
        self.console["state"] = "normal"
        self.console.insert(END, str)
        self.console["state"] = "disable"

    def clear_console(self):
        self.console["state"] = "normal"
        self.console.delete('1.0', END)
        self.console["state"] = "disable"

    def cin(self, message="INPUT"):
        '''
        Used by `GIMMEH`; called when user input is needed
        '''
        answer = simpledialog.askstring("GIMMEH", message, 
                                        parent=self.root)
        
        print(f"GOT: {answer}")
        return answer

    def execute(self):
        # Clear lexeme table
        for child in self.lexeme_table.get_children():
            self.lexeme_table.delete(child)
        
        # Clear symbol table
        for child in self.symbol_table.get_children():
            self.symbol_table.delete(child)

        # Clear console
        self.clear_console()

        # Feed source code to lexer
        code = self.editor.get("1.0", 'end-1c')
        tokens = Lexer(code).get_tokens()
        
        for token in tokens:
            self.lexeme_table.insert('', END, text=token.get_lexeme(), values=(token.get_desc(),))

        # print("TOKENS:", tokens)
        self.parser = Parser(self)
        self.parser.set_tokens(tokens)

        self.parser.parse()

interpreter = LOLCodeInterpreter()
interpreter.start()