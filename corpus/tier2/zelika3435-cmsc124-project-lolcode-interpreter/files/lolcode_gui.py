"""
LOLCODE Interpreter GUI
=======================

Graphical front-end for the CMSC 124 LOLCODE interpreter. Provides the file
explorer, editable source pane, token list, symbol table, console I/O, and
execution controls required by the 2025 CMSC 124 project specification.

This module focuses solely on GUI responsibilities (Tkinter widgets, layout,
and user interactions) while delegating lexical analysis to
`lolcode_interpreter.py`.
"""

import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
import os
import re

from lolcode_interpreter import lolcode_lexer


class LOLCodeInterpreterGUI:
    """Tkinter GUI wrapper that wires together all dashboard components."""
    def __init__(self, root):
        self.root = root
        self.root.title("LOLCODE Interpreter - CMSC 124")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 700)
        self.current_file_path = None
        self.unsaved_changes = False
        self.suppress_modified_event = False
        
        # Configure style
        self.setup_styles()
        
        # Create main container
        self.create_widgets()
        
    def setup_styles(self):
        """Configure ttk styles for a modern look"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure button style
        style.configure('Run.TButton', font=('Arial', 11, 'bold'))
        
    def create_widgets(self):
        """Create all GUI components"""
        
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights for resizing
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)  # For tokens and symbol table
        main_frame.columnconfigure(1, weight=1)  # For tokens and symbol table
        main_frame.rowconfigure(1, weight=1)    # Text editor row
        main_frame.rowconfigure(2, weight=1)     # Tokens/Symbol table row
        main_frame.rowconfigure(4, weight=2)     # Console row (bigger)
        
        # ============================================
        # (1) File Explorer Section
        # ============================================
        file_frame = ttk.LabelFrame(main_frame, text="File Explorer", padding="10")
        file_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        file_frame.columnconfigure(1, weight=1)
        
        ttk.Label(file_frame, text="Select LOLCODE file:").grid(row=0, column=0, padx=(0, 10))
        
        self.file_path_var = tk.StringVar(value="No file selected")
        file_entry = ttk.Entry(file_frame, textvariable=self.file_path_var, state='readonly')
        file_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        browse_btn = ttk.Button(file_frame, text="Browse...", command=self.browse_file)
        browse_btn.grid(row=0, column=2)
        
        # ============================================
        # (2) Text Editor Section (Full Width)
        # ============================================
        editor_frame = ttk.LabelFrame(main_frame, text="Text Editor", padding="10")
        editor_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        editor_frame.columnconfigure(0, weight=1)
        editor_frame.rowconfigure(0, weight=1)
        
        # Create scrolled text widget for code editor
        self.code_editor = scrolledtext.ScrolledText(
            editor_frame,
            wrap=tk.NONE,
            font=('Consolas', 11),
            bg='#1e1e1e',
            fg='#d4d4d4',
            insertbackground='#ffffff',
            selectbackground='#264f78',
            selectforeground='#ffffff'
        )
        self.code_editor.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.code_editor.bind('<<Modified>>', self.on_text_modified)
        
        # Add line numbers (placeholder - will be implemented later)
        line_numbers = tk.Text(
            editor_frame,
            width=4,
            bg='#252526',
            fg='#858585',
            state='disabled',
            font=('Consolas', 11)
        )
        line_numbers.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # ============================================
        # (3) List of Tokens Section (Left Half)
        # ============================================
        tokens_frame = ttk.LabelFrame(main_frame, text="List of Tokens", padding="10")
        tokens_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5), pady=(0, 10))
        tokens_frame.columnconfigure(0, weight=1)
        tokens_frame.rowconfigure(0, weight=1)
        
        # Create treeview for tokens with columns
        tokens_tree = ttk.Treeview(tokens_frame, columns=('Type', 'Value'), show='tree headings', height=15)
        tokens_tree.heading('#0', text='#')
        tokens_tree.heading('Type', text='Token Type')
        tokens_tree.heading('Value', text='Token Value')
        tokens_tree.column('#0', width=50, minwidth=50)
        tokens_tree.column('Type', width=150, minwidth=150)
        tokens_tree.column('Value', width=200, minwidth=150)
        
        # Scrollbar for tokens
        tokens_scrollbar = ttk.Scrollbar(tokens_frame, orient=tk.VERTICAL, command=tokens_tree.yview)
        tokens_tree.configure(yscrollcommand=tokens_scrollbar.set)
        
        tokens_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        tokens_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        self.tokens_tree = tokens_tree
        
        # ============================================
        # (4) Symbol Table Section (Right Half)
        # ============================================
        symbol_frame = ttk.LabelFrame(main_frame, text="Symbol Table", padding="10")
        symbol_frame.grid(row=2, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0), pady=(0, 10))
        symbol_frame.columnconfigure(0, weight=1)
        symbol_frame.rowconfigure(0, weight=1)
        
        # Create treeview for symbol table
        symbol_tree = ttk.Treeview(symbol_frame, columns=('Type', 'Value'), show='tree headings', height=15)
        symbol_tree.heading('#0', text='Variable')
        symbol_tree.heading('Type', text='Data Type')
        symbol_tree.heading('Value', text='Value')
        symbol_tree.column('#0', width=150, minwidth=100)
        symbol_tree.column('Type', width=100, minwidth=80)
        symbol_tree.column('Value', width=200, minwidth=150)
        
        # Scrollbar for symbol table
        symbol_scrollbar = ttk.Scrollbar(symbol_frame, orient=tk.VERTICAL, command=symbol_tree.yview)
        symbol_tree.configure(yscrollcommand=symbol_scrollbar.set)
        
        symbol_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        symbol_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        self.symbol_tree = symbol_tree
        
        # ============================================
        # (5) Execute/Run Button Section
        # ============================================
        control_frame = ttk.Frame(main_frame, padding="10")
        control_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.run_btn = ttk.Button(
            control_frame,
            text="▶ Execute/Run",
            style='Run.TButton',
            command=self.run_code,
            width=20
        )
        self.run_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.save_btn = ttk.Button(
            control_frame,
            text="Save Changes",
            command=self.save_changes,
            width=15
        )
        self.save_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.undo_btn = ttk.Button(
            control_frame,
            text="Undo Changes",
            command=self.undo_changes,
            width=15
        )
        self.undo_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.clear_btn = ttk.Button(
            control_frame,
            text="Clear Console",
            command=self.clear_console,
            width=15
        )
        self.clear_btn.pack(side=tk.LEFT)
        
        # Status label
        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(control_frame, textvariable=self.status_var, foreground='gray')
        status_label.pack(side=tk.LEFT, padx=(20, 0))
        
        # ============================================
        # (6) Console Section (Full Width, Bigger)
        # ============================================
        console_frame = ttk.LabelFrame(main_frame, text="Console (Input/Output)", padding="10")
        console_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        console_frame.columnconfigure(0, weight=1)
        console_frame.rowconfigure(0, weight=1)
        
        # Console output area (bigger)
        self.console_output = scrolledtext.ScrolledText(
            console_frame,
            wrap=tk.WORD,
            font=('Consolas', 11),
            bg='#0d1117',
            fg='#c9d1d9',
            insertbackground='#ffffff',
            state='disabled',
            height=15
        )
        self.console_output.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Input field for user input (for GIMMEH)
        input_frame = ttk.Frame(console_frame)
        input_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        input_frame.columnconfigure(1, weight=1)
        
        ttk.Label(input_frame, text="Input:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        
        self.input_entry = ttk.Entry(input_frame)
        self.input_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        self.input_entry.bind('<Return>', self.submit_input)
        
        submit_input_btn = ttk.Button(input_frame, text="Submit", command=self.submit_input, width=10)
        submit_input_btn.grid(row=0, column=2)
        
    def browse_file(self):
        """Open file dialog and load selected LOLCODE file"""
        if not self.confirm_discard_changes():
            return

        file_path = filedialog.askopenfilename(
            title="Select LOLCODE File",
            filetypes=[("LOLCODE files", "*.lol"), ("All files", "*.*")],
            initialdir=os.path.join(os.path.dirname(__file__), "testfiles")
        )
        
        if file_path:
            self.load_file(file_path)

    def load_file(self, file_path):
        """Load the selected file into the text editor"""
        self.suppress_modified_event = True
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
        except UnicodeDecodeError:
            messagebox.showerror("Encoding Error", "Unable to read file using UTF-8 encoding.")
            self.suppress_modified_event = False
            return
        except OSError as exc:
            messagebox.showerror("File Error", f"Unable to open file.\n\n{exc}")
            self.suppress_modified_event = False
            return

        self.code_editor.delete(1.0, tk.END)
        self.code_editor.insert(tk.END, content)
        self.code_editor.edit_modified(False)
        self.suppress_modified_event = False
        self.file_path_var.set(file_path)
        self.current_file_path = file_path
        self.unsaved_changes = False
        self.status_var.set(f"Loaded: {os.path.basename(file_path)}")
        self.root.title(f"LOLCODE Interpreter - CMSC 124 · {os.path.basename(file_path)}")
        self.code_editor.focus_set()
        self.update_tokens_and_symbols(content)

    def confirm_discard_changes(self):
        """Prompt the user before discarding unsaved edits"""
        if not self.unsaved_changes:
            return True

        return messagebox.askyesno(
            "Discard changes?",
            "You have unsaved changes in the current file.\n"
            "Do you want to discard them and continue?"
        )

    def on_text_modified(self, event=None):
        """Track editor modifications to support spec #2"""
        if self.code_editor.edit_modified():
            if self.suppress_modified_event:
                self.code_editor.edit_modified(False)
                return
            self.unsaved_changes = True
            filename = os.path.basename(self.current_file_path) if self.current_file_path else "Untitled"
            self.status_var.set(f"Editing: {filename} (modified)")
            self.code_editor.edit_modified(False)
    
    def save_changes(self):
        """Save the current editor content to disk"""
        target_path = self.current_file_path
        
        if not target_path:
            target_path = filedialog.asksaveasfilename(
                title="Save LOLCODE File",
                defaultextension=".lol",
                filetypes=[("LOLCODE files", "*.lol"), ("All files", "*.*")]
            )
            if not target_path:
                return
            self.current_file_path = target_path
            self.file_path_var.set(target_path)
        
        try:
            content = self.code_editor.get(1.0, tk.END)
            with open(target_path, 'w', encoding='utf-8') as file:
                file.write(content.rstrip() + '\n')
        except OSError as exc:
            messagebox.showerror("Save Error", f"Unable to save file.\n\n{exc}")
            return
        
        self.unsaved_changes = False
        self.code_editor.edit_modified(False)
        self.status_var.set(f"Saved: {os.path.basename(target_path)}")
        self.root.title(f"LOLCODE Interpreter - CMSC 124 · {os.path.basename(target_path)}")
        self.update_tokens_and_symbols(content)
    
    def undo_changes(self):
        """Revert the editor content to the last saved version"""
        if not self.current_file_path:
            messagebox.showinfo("Undo not available", "No file is currently loaded.")
            return
        
        if not self.confirm_discard_changes():
            return
        
        self.load_file(self.current_file_path)

    def update_tokens_and_symbols(self, code):
        """Refresh the token list and symbol table when a file loads or saves"""
        self.populate_tokens(code)
        self.populate_symbol_table(code)

    def populate_tokens(self, code):
        """Fill the token list via the lexer"""
        for child in self.tokens_tree.get_children():
            self.tokens_tree.delete(child)

        try:
            tokens = list(lolcode_lexer(code))
        except SyntaxError as exc:
            messagebox.showerror("Lexer Error", f"{exc}")
            self.status_var.set(f"Lexer error: {exc}")
            return

        for index, (token_type, token_value) in enumerate(tokens, start=1):
            if token_type == 'EOF':
                continue
            display_value = token_value if token_value is not None else ''
            self.tokens_tree.insert('', 'end', text=str(index), values=(token_type, display_value))

    def populate_symbol_table(self, code):
        """Very simple symbol table builder based on declarations inside WAZZUP"""
        for child in self.symbol_tree.get_children():
            self.symbol_tree.delete(child)

        declarations = self.extract_variable_declarations(code)
        for entry in declarations:
            name = entry['name']
            value = entry.get('value')
            dtype = self.infer_value_type(value)
            display_value = value if value is not None else ''
            self.symbol_tree.insert('', 'end', text=name, values=(dtype, display_value))

    def extract_variable_declarations(self, code):
        """Scan the WAZZUP block for simple variable declarations"""
        in_wazzup = False
        declarations = []
        for raw_line in code.splitlines():
            line = raw_line.split('BTW')[0].strip()
            if not line:
                continue
            if line.startswith('WAZZUP'):
                in_wazzup = True
                continue
            if line.startswith('BUHBYE'):
                in_wazzup = False
                continue
            if not in_wazzup:
                continue

            match = re.match(r'I\s+HAS\s+A\s+([A-Za-z][A-Za-z0-9_]*)\s*(?:ITZ\s+(.*))?$', line)
            if match:
                var_name = match.group(1)
                var_value = match.group(2).strip() if match.group(2) else None
                declarations.append({'name': var_name, 'value': var_value})
        return declarations

    def infer_value_type(self, value):
        """Best-effort literal type detection for the symbol table"""
        if not value:
            return 'NOOB'
        if value.startswith('"') and value.endswith('"'):
            return 'YARN'
        if re.fullmatch(r'-?\d+\.\d+', value):
            return 'NUMBAR'
        if re.fullmatch(r'-?\d+', value):
            return 'NUMBR'
        if value in ('WIN', 'FAIL'):
            return 'TROOF'
        return 'EXPR/VAR'
    
    def run_code(self):
        """Placeholder for code execution functionality"""
        self.status_var.set("Running...")
        # TODO: Implement code execution
        # - Get code from editor
        # - Run lexer
        # - Run parser
        # - Execute interpreter
        # - Update tokens tree
        # - Update symbol table
        # - Display output in console
        self.status_var.set("Execution complete")
    
    def clear_console(self):
        """Clear the console output"""
        self.console_output.config(state='normal')
        self.console_output.delete(1.0, tk.END)
        self.console_output.config(state='disabled')
    
    def submit_input(self, event=None):
        """Placeholder for input submission (for GIMMEH)"""
        user_input = self.input_entry.get()
        if user_input:
            # TODO: Process input for GIMMEH statements
            self.console_output.config(state='normal')
            self.console_output.insert(tk.END, f"Input: {user_input}\n")
            self.console_output.config(state='disabled')
            self.input_entry.delete(0, tk.END)
    
    def write_to_console(self, text):
        """Helper method to write text to console"""
        self.console_output.config(state='normal')
        self.console_output.insert(tk.END, text)
        self.console_output.see(tk.END)
        self.console_output.config(state='disabled')


def main():
    """Main entry point for the GUI application"""
    root = tk.Tk()
    app = LOLCodeInterpreterGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

