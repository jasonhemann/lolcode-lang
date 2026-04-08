import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from lexical_analyzer import lex_analysis as Lexer
from syntactic_analyzer import Parser
# from semantic_analyzer import analyze_semantics   # plug this later


class LolcodeGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("LOLCode Interpreter")
        self.root.geometry("1000x700")

        self.create_menu()
        self.create_editor()
        self.create_middle_panes()
        self.create_execute_button()
        self.create_console()

        self.root.mainloop()

    # ------------------------------------------------------------
    # MENU BAR (Open File)
    # ------------------------------------------------------------
    def create_menu(self):
        menubar = tk.Menu(self.root)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open File", command=self.load_file)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        self.root.config(menu=menubar)

    # ------------------------------------------------------------
    # TEXT EDITOR
    # ------------------------------------------------------------
    def create_editor(self):
        frame = tk.Frame(self.root)
        frame.pack(fill="both", expand=False)

        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")

        self.editor = tk.Text(frame, height=10, font=("Consolas", 14))
        self.editor.pack(fill="both", expand=True)

        self.editor.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.editor.yview)

    # ------------------------------------------------------------
    # PANED WINDOW (TOKEN TABLE + SYMBOL TABLE)
    # ------------------------------------------------------------
    def create_middle_panes(self):
        paned = ttk.Panedwindow(self.root, orient=tk.HORIZONTAL)
        paned.pack(fill="both", expand=True, pady=5)

        # --- LEFT: Tokens Table ---
        token_frame = ttk.Labelframe(paned, text="Lexemes")
        self.token_table = ttk.Treeview(token_frame, columns=("lexeme", "class"), show="headings", height=12)
        self.token_table.heading("lexeme", text="Lexeme")
        self.token_table.heading("class", text="Classification")
        self.token_table.column("lexeme", width=150)
        self.token_table.column("class", width=150)

        scroll1 = ttk.Scrollbar(token_frame, command=self.token_table.yview)
        self.token_table.configure(yscrollcommand=scroll1.set)

        self.token_table.pack(side="left", fill="both", expand=True)
        scroll1.pack(side="right", fill="y")

        # --- RIGHT: Symbol Table ---
        symbol_frame = ttk.Labelframe(paned, text="Symbol Table")
        self.symbol_table = ttk.Treeview(symbol_frame, columns=("identifier", "value"), show="headings", height=12)
        self.symbol_table.heading("identifier", text="Identifier")
        self.symbol_table.heading("value", text="Value")
        self.symbol_table.column("identifier", width=150)
        self.symbol_table.column("value", width=150)

        scroll2 = ttk.Scrollbar(symbol_frame, command=self.symbol_table.yview)
        self.symbol_table.configure(yscrollcommand=scroll2.set)

        self.symbol_table.pack(side="left", fill="both", expand=True)
        scroll2.pack(side="right", fill="y")

        # Add to paned window
        paned.add(token_frame, weight=1)
        paned.add(symbol_frame, weight=1)

    # ------------------------------------------------------------
    # EXECUTE BUTTON
    # ------------------------------------------------------------
    def create_execute_button(self):
        self.exec_button = tk.Button(self.root, text="EXECUTE", font=("Arial", 14), command=self.execute_code)
        self.exec_button.pack(pady=5)

    # ------------------------------------------------------------
    # CONSOLE
    # ------------------------------------------------------------
    def create_console(self):
        frame = tk.Frame(self.root)
        frame.pack(fill="both", expand=True)

        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")

        self.console = tk.Text(frame, height=10, font=("Consolas", 14), state="disabled", bg="#222", fg="#0f0")
        self.console.pack(fill="both", expand=True)

        self.console.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.console.yview)

    # ------------------------------------------------------------
    # FILE LOADING
    # ------------------------------------------------------------
    def load_file(self):
        path = filedialog.askopenfilename(filetypes=[("LOLCode Files", "*.lol"), ("All Files", "*.*")])
        if not path:
            return

        with open(path, "r") as file:
            content = file.read()

        self.editor.delete("1.0", tk.END)
        self.editor.insert("1.0", content)

    # ------------------------------------------------------------
    # EXECUTE: LEXER → PARSER → SEMANTIC (NO INTERPRETER YET)
    # ------------------------------------------------------------
    def execute_code(self):
        source = self.editor.get("1.0", tk.END)

        # Clear all displays
        self.clear_tables()
        self.console_clear()

        # -------------------------------
        # 1. LEXICAL ANALYSIS
        # -------------------------------
        try:
            tokens, lex_errors = Lexer(source)
        except Exception as e:
            self.console_write(f"[LEXER ERROR] {e}")
            return

        if lex_errors:
            self.display_errors("LEXER", lex_errors)
            return

        # Populate token table
        for token_line in tokens:
            for token in token_line:
                self.token_table.insert("", "end", values=(token["value"], token["type"]))

        # -------------------------------
        # 2. PARSING
        # -------------------------------
        try:
            parsed_lines, parse_errors = Parser.parse(tokens)
        except Exception as e:
            self.console_write(f"[PARSER ERROR] {e}")
            return

        if parse_errors:
            self.display_errors("PARSER", parse_errors)
            return

        # -------------------------------
        # 3. SEMANTIC ANALYSIS
        # -------------------------------
        try:
            # instructions, symbol_table, sem_errors = analyze_semantics(parsed_lines)
            # placeholder:
            instructions = []
            symbol_table = {"sampleVar": "123"}  # replace later
            sem_errors = []
        except Exception as e:
            self.console_write(f"[SEMANTIC ERROR] {e}")
            return

        if sem_errors:
            self.display_errors("SEMANTICS", sem_errors)
            return

        # Populate symbol table
        for identifier, value in symbol_table.items():
            self.symbol_table.insert("", "end", values=(identifier, value))

        self.console_write("✔ Analysis completed. No interpreter step yet.\n")

    # ------------------------------------------------------------
    # UTILITY FUNCTIONS
    # ------------------------------------------------------------
    def clear_tables(self):
        for item in self.token_table.get_children():
            self.token_table.delete(item)
        for item in self.symbol_table.get_children():
            self.symbol_table.delete(item)

    def console_write(self, text):
        self.console.config(state="normal")
        self.console.insert(tk.END, text + "\n")
        self.console.config(state="disabled")

    def console_clear(self):
        self.console.config(state="normal")
        self.console.delete("1.0", tk.END)
        self.console.config(state="disabled")

    def display_errors(self, stage, errors):
        self.console_write(f"❌ {stage} ERRORS:")
        for err in errors:
            self.console_write(f"  - {err}")


# Run GUI
LolcodeGUI()
