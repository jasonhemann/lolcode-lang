import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from lexer import LOLCodeLexer
from syntax import LOLCodeParser

# GUI
class LOLCodeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("carLOLcode")

        self.create_widgets()

    def create_widgets(self):
        # open button
        open_button = tk.Button(self.root, text="Open File", command=self.import_configuration, width=20)
        open_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # lol file
        self.code_text = tk.Text(self.root, width=50, height=10)
        self.code_text.grid(row=1, column=0, rowspan=4, padx=10, pady=10, sticky="nsew")

        # label
        tk.Label(self.root, text="LOLCode Interpreter", font=("Helvetica", 16, "bold")).grid(
            row=0, column=1, columnspan=2, sticky="w", padx=10, pady=5)
        
        run_lexer = tk.Button(self.root, text="LEXEMES", command=self.run_lexer, width=40)
        run_lexer.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        run_semantic = tk.Button(self.root, text="SYMBOL TABLE", command=self.run_syntax, width=40)
        run_semantic.grid(row=1, column=2, padx=10, pady=5, sticky="w")

        # lexeme and symbol table table
        table_frame = tk.Frame(self.root)
        table_frame.grid(row=2, column=1, columnspan=2, padx=5, pady=5, sticky="nsew")

        # lexeme
        self.lexemes_tree = ttk.Treeview(table_frame, columns=("Lexeme", "Classification"), show="headings")
        self.lexemes_tree.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        self.lexemes_scrollbar = tk.Scrollbar(table_frame, orient="vertical", command=self.lexemes_tree.yview)
        self.lexemes_scrollbar.grid(row=0, column=1, sticky="ns")
        self.lexemes_tree.config(yscrollcommand=self.lexemes_scrollbar.set)

        self.lexemes_tree.heading("Lexeme", text="Lexeme")
        self.lexemes_tree.heading("Classification", text="Classification")
        self.lexemes_tree.column("Lexeme", width=150, anchor="w")
        self.lexemes_tree.column("Classification", width=250, anchor="w")

        # symbol table
        self.symbol_tree = ttk.Treeview(table_frame, columns=("Identifier", "Value"), show="headings")
        self.symbol_tree.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")

        self.symbol_scrollbar = tk.Scrollbar(table_frame, orient="vertical", command=self.symbol_tree.yview)
        self.symbol_scrollbar.grid(row=0, column=3, sticky="ns")
        self.symbol_tree.config(yscrollcommand=self.symbol_scrollbar.set)

        self.symbol_tree.heading("Identifier", text="Identifier")
        self.symbol_tree.heading("Value", text="Value")
        self.symbol_tree.column("Identifier", width=250, anchor="w")
        self.symbol_tree.column("Value", width=150, anchor="w")

        # output / terminal
        execute = tk.Button(self.root, text="EXECUTE", anchor='center', font=("Helvetica", 16, "bold"), command=self.run_syntax)
        execute.grid(row=3, column=1, columnspan=2, padx=10, pady=5, sticky="nsew")

        self.result_text = tk.Text(self.root, height=20)
        self.result_text.grid(row=4, column=1, columnspan=2, padx=10, pady=10, sticky="nsew")

    # open/import lolcode file
    def import_configuration(self):
        file_path = filedialog.askopenfilename(title="Open LOLCODE file", filetypes=[("LOLCODE Files", "*.lol"), ("All Files", "*.*")])
        try: 
            with open(file_path, "r") as file:
                code = file.read()
                self.code_text.delete("1.0", tk.END)
                self.code_text.insert(tk.END, code)
            
            for row in self.lexemes_tree.get_children():
                self.lexemes_tree.delete(row)
            
            for row in self.symbol_tree.get_children():
                self.symbol_tree.delete(row)

            self.result_text.delete("1.0", tk.END)

        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
            sys.exit(1)

    # get tokens from lexeme analyzer
    def get_tokens(self):
        code = self.code_text.get("1.0", tk.END)
        lexer = LOLCodeLexer(code)
        try:
            tokens = lexer.tokenize()
            return tokens
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    # runs the lexeme analyzer
    def run_lexer(self):
        # Get code from text widget and tokenize it
        tokens = self.get_tokens()
        for row in self.lexemes_tree.get_children():
            self.lexemes_tree.delete(row)
        
        for row in self.symbol_tree.get_children():
            self.symbol_tree.delete(row)

        self.result_text.delete("1.0", tk.END)
        
        for token in tokens:
            if token.type != 'NEWLINE':
                self.lexemes_tree.insert("", "end", values=(token.value, token.type))
        
    def update_symbol_table(self, variables, print, suppress):
        for row in self.symbol_tree.get_children():
            self.symbol_tree.delete(row)
        
        for identifier, value in variables.items():
            self.symbol_tree.insert("", 0, values=(identifier, value))
        
        if 'IT' in variables.keys() and print == True:
            value = variables['IT']
            if suppress:
                self.result_text.insert(tk.END, f"{value}")
            else: self.result_text.insert(tk.END, f"{value}\n")

    # runs syntax analyzer
    def run_syntax(self):
        tokens = self.get_tokens()
        if not tokens:
            return 

        self.result_text.delete("1.0", tk.END)
        
        try:
            parser = LOLCodeParser(tokens, gui=self)
            parser.parse()
        except SyntaxError as e:
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, f"Syntax Error: {str(e)}")
    
    def get_user_input(self):
        user_input = self.result_text.get("1.0", tk.END).strip().split('\n')[0]
        return user_input

    def write(self, value):
        self.result_text.insert(tk.END, f"{value}\n")