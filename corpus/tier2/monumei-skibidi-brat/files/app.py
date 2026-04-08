import tkinter as tk 
from tkinter import ttk 
from tkinter import filedialog, scrolledtext 
from PIL import Image, ImageTk
from lexical_analyzer import LexicalAnalyzer, LexicalError 
from semantics_analyzer import SemanticAnalyzer 
from syntax_analyzer import Parser 
from interpreter import Interpreter 

class LOLInterpreterGUI: 
    def __init__(self, root): 
        self.root = root 
        self.root.title("Skibidi Brat: A LOLCODE Interpreter") 
        self.root.config(background="#8ACE00") 
        self.root.resizable(False, False)
        
        ico = Image.open("assets/logo.png")
        photo = ImageTk.PhotoImage(ico)
        self.root.iconphoto(False, photo)

        # Custom Style 
        style = ttk.Style() 
        style.configure("Treeview", background="#8ACE00", foreground="black", rowheight=20, fieldbackground="#8ACE00", font=("Arial Narrow", 12)) 
        style.configure("Treeview.Heading", background="#8ACE00", foreground="black", font=("Arial Narrow", 12, "bold")) 
        style.configure("TreeView.Column", background="#8ACE00", foreground="black", font=("Arial Narrow", 12, "bold")) 
        style.map("Treeview.Heading", background=[('active', '#3a3d42')]) 

        # Part 1: File Explorer 
        self.file_button = tk.Button(root, text="Open File", command=self.open_file, font=("Arial Narrow", 10, "bold"), 
                                      background="#1c1e22", foreground="white", activebackground="#3a3d42", 
                                      activeforeground="white", relief=tk.FLAT) 
        self.file_button.grid(row=0, column=0, sticky="w", padx=5, pady=5) 

        # Part 2: Text Editor 
        self.text_editor = scrolledtext.ScrolledText(root, wrap=tk.WORD) 
        self.text_editor.config(background="#8ACE00", foreground="black", insertbackground="black", width=75, font=("Arial Narrow", 12, "bold")) 
        self.text_editor.grid(row=1, column=0, columnspan=1, padx=5, pady=5, sticky="nsew") 

        # Part 3: Lexemes List (Tokens) 
        self.lexeme_label = tk.Label(root, text="Lexemes", font=("Arial Narrow", 12, "bold"), background="#8ACE00", foreground="black") 
        self.lexeme_label.grid(row=0, column=1) 

        self.lexeme_table = ttk.Treeview(root, columns=("Lexeme", "Classification"), show="headings", style="Treeview") 
        self.lexeme_table.heading("Lexeme", text="Lexeme") 
        self.lexeme_table.heading("Classification", text="Classification") 
        self.lexeme_table.column("Lexeme", width=128, anchor="center") 
        self.lexeme_table.column("Classification", width=200, anchor="center") 
        self.lexeme_table.grid(row=1, column=1, padx=5, pady=5, sticky="nsew") 

        # Part 4: Symbol Table 
        self.symbol_table_label = tk.Label(root, text="Symbol Table", font=("Arial Narrow", 12, "bold"), background="#8ACE00", foreground="black") 
        self.symbol_table_label.grid(row=0, column=2) 

        self.symbol_table = ttk.Treeview(root, columns=("Variable", "Value"), show="headings", style="Treeview") 
        self.symbol_table.heading("Variable", text="Variable") 
        self.symbol_table.heading("Value", text="Value") 
        self.symbol_table.column("Variable", width=128, anchor="center") 
        self.symbol_table.column("Value", width=128, anchor="center") 
        self.symbol_table.grid(row=1, column=2, padx=5, pady=5, sticky="nsew") 

        # Part 5: Execute/Run Button 
        self.run_button = tk.Button(root, text="Execute", command=self.execute_code, font=("Arial Narrow", 12, "bold"), 
                                     background="#1c1e22", foreground="white", activebackground="#3a3d42", 
                                     activeforeground="white", relief=tk.FLAT) 
        self.run_button.grid(row=4, column=0, columnspan=3, pady=10 , padx=5, sticky="we") 

        # Part 6: Console 
        self.console = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=10) 
        self.console.config(background="#8ACE00", foreground="black", insertbackground="black", font=("Arial Narrow", 10)) 
        self.console.grid(row=5, column=0, columnspan=3, padx=5 , pady=5, sticky="we") 
        self.console.bind("<Return>", self.handle_console_input)

        # Grid weight configuration for resizing 
        self.root.grid_columnconfigure(0, weight=1) 
        self.root.grid_columnconfigure(1, weight=1) 
        self.root.grid_columnconfigure(2, weight=1) 
        self.root.grid_rowconfigure(1, weight=1) 

        # Initialize interpreter 
        self.interpreter = Interpreter() 
        self.interpreter.set_console_output(self.update_console) 
        self.interpreter.set_symbol_table_update(self.update_symbol_table)

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("LOL Code Files", "*.lol")])
        if file_path:
            with open(file_path, 'r') as file:
                code = file.read()
                self.text_editor.delete('1.0', tk.END)
                self.text_editor.insert(tk.END, code)
            
            # Reset the symbol table and lexical analyzer
            self.lexeme_table.delete(*self.lexeme_table.get_children())  # Clear the lexeme table
            self.symbol_table.delete(*self.symbol_table.get_children())  # Clear the symbol table
            self.interpreter = Interpreter()  # Reset the interpreter to clear its state
            self.interpreter.set_console_output(self.update_console)
            self.console.delete('1.0', tk.END)  # Clear the console output

    def execute_code(self): 
        code = self.text_editor.get("1.0", tk.END).strip() 
        # Lexical analysis 
        try: 
            analyzer = LexicalAnalyzer() 
            tokens = analyzer.tokenize(code) 
            self.update_lexemes(tokens) 
        except LexicalError as e: 
            self.update_console(f"Lexical Error: {e}") 
            return 

        # Syntax analysis 
        try: 
            parser = Parser(tokens) 
            ast = parser.parse()  # Parse the tokens into AST 
        except Exception as e:  # Catching any parsing errors 
            self.update_console(f"Syntax Error: {e}") 
            return 

        # Semantic analysis 
        try: 
            semantic_analyzer = SemanticAnalyzer() 
            semantic_analyzer.analyze(ast)  # Perform semantic analysis 
        except Exception as e: 
            self.update_console(f"Semantic Error: {e}") 
            return 

        # Interpretation 
        try: 
            self.interpreter.interpret(ast, semantic_analyzer)  # Execute the AST 
            self.update_symbol_table(self.interpreter.get_symbol_table()) 
        except Exception as e: 
            self.update_console(f"Runtime Error: {e}") 

    def update_lexemes(self, tokens): 
        # Clear previous lexemes 
        for item in self.lexeme_table.get_children(): 
            self.lexeme_table.delete(item) 

        # Insert new lexemes 
        for token in tokens: 
            self.lexeme_table.insert("", tk.END, values=(token.value, token.type.name)) 

    def update_symbol_table(self, symbol_table): 
        # Clear previous symbols 
        for item in self.symbol_table.get_children(): 
            self.symbol_table.delete(item) 

        # Insert symbols from the symbol table 
        for var_name, value in symbol_table.items(): 
            self.symbol_table.insert("", tk.END, values=(var_name, value)) 

    def update_console(self, output): 
        self.console.insert(tk.END, output + "\n")  # Append new output with a newline 
        self.console.see(tk.END)  # Scroll to the end to show the latest output 
        
    def handle_console_input(self, event):
        """Handle input from the console."""
        input_value = self.console.get("1.0", tk.END).strip()  # Get the input from the console
        self.console.delete("1.0", tk.END)  # Clear the console after reading input
        self.interpreter.set_input(input_value)  # Set the input in the interpreter
        
    def update_symbol_table_display(symbol_table):
        # Code to update the GUI with the new symbol table
        pass

if __name__ == "__main__": 
    root = tk.Tk() 
    app = LOLInterpreterGUI(root) 
    root.mainloop() 