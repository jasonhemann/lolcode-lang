import lexical_analyzer
import syntax_analyzer
import semantic_analyzer
import tkinter as tk
from tkinter import filedialog, scrolledtext, ttk
import re

class LOLCodeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("LOLCODE Interpreter")

        # Set the root background color
        self.root.configure(bg="ivory2")

        # Create a 3-column grid layout
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2, weight=1)

        # HEADER
        header = tk.Label(root, text="LOLCODE INTERPRETER", bg="steel blue", fg="ivory2", font=("Helvetica", 14, "bold"))
        header.grid(row=0, column=0, columnspan=3, sticky="nsew")

        # COLUMN 1: File Explorer and Text Editor
        self.file_explorer_frame = tk.Frame(root, bd=1, relief="solid", bg="ivory2")
        self.file_explorer_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        self.file_label = tk.Label(self.file_explorer_frame, text="Select a file", bg="ivory2", anchor="w", font=("Helvetica", 10, "bold"))
        self.file_label.pack(fill="x", padx=5, pady=5)

        self.browse_button = tk.Button(self.file_explorer_frame, text="📂", bg="steel blue", fg="ivory2", font=("Helvetica", 12, "bold"), command=self.open_file)
        self.browse_button.pack(fill="x", padx=5, pady=5)

        self.text_editor = scrolledtext.ScrolledText(self.file_explorer_frame, wrap="word", bg="ivory2", font=("Helvetica", 8), height=25, width=60)
        self.text_editor.pack(fill="both", expand=True, padx=5, pady=5)

        # COLUMN 2: List of Tokens
        self.tokens_frame = tk.Frame(root, bd=1, bg="ivory2", relief="solid")
        self.tokens_frame.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)

        self.lexemes_header = tk.Label(self.tokens_frame, text="LEXEMES", bg="steel blue", fg="ivory2", font=("Helvetica", 12, "bold"))
        self.lexemes_header.pack(fill="x", padx=5, pady=5)

        # Create a frame to contain both the Treeview and scrollbar
        tokens_tree_container = tk.Frame(self.tokens_frame, bg="ivory2")
        tokens_tree_container.pack(fill="both", expand=True, padx=5, pady=5)

        # Treeview for the lexemes section
        self.tokens_tree = ttk.Treeview(tokens_tree_container, columns=("Type", "Lexeme", "Classification"), show="headings", height=20)
        self.tokens_tree.heading("Type", text="TYPE")
        self.tokens_tree.heading("Lexeme", text="LEXEMES")
        self.tokens_tree.heading("Classification", text="CLASSIFICATION")

        self.tokens_tree.column("Type", width=120, anchor="w")
        self.tokens_tree.column("Lexeme", width=140, anchor="w")
        self.tokens_tree.column("Classification", width=160, anchor="w")

        self.tokens_tree.pack(side="left", fill="both", expand=True)

        # Add vertical scrollbar to the Treeview
        tokens_scrollbar = ttk.Scrollbar(tokens_tree_container, orient="vertical", command=self.tokens_tree.yview)
        tokens_scrollbar.pack(side="right", fill="y")

        # Configure Treeview to use the scrollbar
        self.tokens_tree.configure(yscrollcommand=tokens_scrollbar.set)

        # COLUMN 3: Symbol Table
        self.symbol_table_frame = tk.Frame(root, bd=1, bg="ivory2", relief="solid")
        self.symbol_table_frame.grid(row=1, column=2, sticky="nsew", padx=5, pady=5)

        self.symbol_table_header = tk.Label(self.symbol_table_frame, text="SYMBOL TABLE", bg="steel blue", fg="ivory2", font=("Helvetica", 12, "bold"))
        self.symbol_table_header.pack(fill="x", padx=5, pady=5)

        # Create a frame to contain both the Treeview and scrollbar
        symbol_table_container = tk.Frame(self.symbol_table_frame, bg="ivory2")
        symbol_table_container.pack(fill="both", expand=True, padx=5, pady=5)

        # Treeview for the symbol table
        self.symbol_table = ttk.Treeview(symbol_table_container, columns=("Identifier", "Value"), show="headings")
        self.symbol_table.heading("Identifier", text="IDENTIFIER")
        self.symbol_table.heading("Value", text="VALUE")

        self.symbol_table.column("Identifier", width=100, anchor="w")
        self.symbol_table.column("Value", width=600, anchor="w")

        self.symbol_table.pack(side="left", fill="both", expand=True)

        # Add vertical scrollbar to the symbol table
        symbol_table_scrollbar = ttk.Scrollbar(symbol_table_container, orient="vertical", command=self.symbol_table.yview)
        symbol_table_scrollbar.pack(side="right", fill="y")

        # Configure Treeview to use the scrollbar
        self.symbol_table.configure(yscrollcommand=symbol_table_scrollbar.set)

        # EXECUTE Button
        self.execute_button = tk.Button(root, text="EXECUTE", command=self.execute_code, font=("Helvetica", 12, "bold"), bg="steel blue", fg="ivory2")
        self.execute_button.grid(row=2, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)

        # CONSOLE
        self.console = scrolledtext.ScrolledText(root, wrap="word", bg="ivory2", font=("Helvetica", 10), height=15)
        self.console.grid(row=3, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)



    def open_file(self):
        # Open file dialog to let the user select a LOLCODE file.
        file_path = filedialog.askopenfilename(
            title="Select a LOLCODE file",
            filetypes=[("LOLCODE files", "*.lol"), ("All files", "*.*")]
        )
        if file_path:
            self.file_label.config(text=file_path)
            with open(file_path, 'r') as file:
                self.text_editor.delete(1.0, tk.END)
                self.text_editor.insert(tk.END, file.read())

    def execute_code(self):
        # Retrieve LOLCODE from the text editor
        code = self.text_editor.get(1.0, tk.END).strip()

        if not code:
            self.console.delete(1.0, tk.END)
            self.console.insert(tk.END, "No code provided!\n")
            return

        # Clear previous data
        self.tokens_tree.delete(*self.tokens_tree.get_children())
        for row in self.symbol_table.get_children():
            self.symbol_table.delete(row)

        # Initialize and use LOLCodeLexer
        lexer = lexical_analyzer.LOLCodeLexer()
        tokens = lexer.tokenize(code)

        # Populate the tokens tree
        for token in tokens:
            token_type = token[0]
            lexeme = token[1]
            if token_type == 'NEWLINE':
                lexeme = '\\n'

            classification = (
                lexical_analyzer.KEYWORDS.get(lexeme, "Unknown") if token_type == "KEYWORD"
                else {
                    "NEWLINE": "Newline",
                    "COMMENT": "Comment",
                    "MULTI-LINE_COMMENT": "Multi-line Comment",
                    "NUMBAR": "Literal (Float)",
                    "NUMBR": "Literal (Integer)",
                    "CONCATENATE": "Concatenate Keyword",
                    "TROOF": "Boolean Literal",
                    "YARN": "String",
                    "STRING_DELIMITER": "String Delimiter",
                    "VARIABLE": "Variable",
                    "TYPE": "Variable Type",
                }.get(token_type, "Unknown")
            )

            self.tokens_tree.insert("", "end", values=(token_type, lexeme, classification))

        # Perform syntax analysis using syntax_analyzer
        syntax_analyzer.tokens = tokens[::-1]  # Reverse tokens for stack-based parsing
        try:
            syntax_result = syntax_analyzer.program_parse()
            self.console.delete(1.0, tk.END)
            self.console.insert(tk.END, f"Syntax Analysis Successful\n")
        except Exception as e:
            self.console.delete(1.0, tk.END)
            self.console.insert(tk.END, f"Syntax Analysis Error: {e}\n")
            return

        # Perform semantic analysis using SemanticAnalyzer
        semantics = semantic_analyzer.SemanticAnalyzer()

        def input_callback(variable_name):
            return self.get_user_input(variable_name)  # Call GUI input method

        if semantics.analyze(syntax_result, input_callback=input_callback):
            # Populate the symbol table TreeView
            for identifier, value in semantics.symbol_table.items():
                if identifier == "IT" and not value:  # Skip IT if it is empty
                    continue
                self.symbol_table.insert("", "end", values=(identifier, value))

            # Collect and display all outputs from VISIBLE statements
            visible_outputs = semantics.get_visible_outputs()
            wrapped_output = "\n".join(map(str, visible_outputs))
            self.console.insert(tk.END, wrapped_output + "\n")
        else:
            # Print visible outputs even if errors occur
            visible_outputs = semantics.get_visible_outputs()
            if visible_outputs:
                wrapped_output = "\n".join(map(str, visible_outputs))
                self.console.insert(tk.END, wrapped_output + "\n")

            # Populate the symbol table TreeView
            for identifier, value in semantics.symbol_table.items():
                if identifier == "IT" and not value:  # Skip IT if it is empty
                    continue
                self.symbol_table.insert("", "end", values=(identifier, value))

            # Display errors after visible outputs
            errors = "\n".join(semantics.report_errors())
            self.console.insert(tk.END, f"Semantic Analysis Errors:\n{errors}\n")

    def get_user_input(self, variable_name):
        """Create a popup to get input from the user."""
        input_value = None  # Variable to store user input

        def on_submit():
            nonlocal input_value
            input_value = entry.get()  # Get the value from the Entry widget
            popup.destroy()  # Close the popup window

        # Create the popup window
        popup = tk.Toplevel(self.root, bg="ivory2")
        popup.title("User Input")
        popup.geometry("300x150")  # Set a reasonable size for the popup

        tk.Label(popup, bg="ivory2", text=f"Enter a value for {variable_name}:", font=("Helvetica", 10)).pack(pady=10)
        entry = tk.Entry(popup, font=("Helvetica", 10))
        entry.pack(pady=10)
        tk.Button(popup, text="Submit", bg="steel blue", fg="ivory2", command=on_submit).pack(pady=10)

        popup.grab_set()  # Make the popup modal (prevent interaction with the main window)
        popup.wait_window()  # Wait until the popup is closed
        return input_value  # Return the input value


if __name__ == "__main__":
    root = tk.Tk()
    app = LOLCodeGUI(root)
    root.mainloop()
