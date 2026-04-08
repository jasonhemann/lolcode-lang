import tkinter as tk
from tkinter import ttk
from tkinter import font
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter import filedialog as fd

from lexer import LexAnalyzer, Token
from parser import SyntaxAnalyzer
from semantics import SemanticAnalyzer

GROUP_NAME = "KOOLAIDS"
INTERPRETER_NAME = "Meme-terpreter: A LOLCODE Interpreter"

THEME = 'clam'
BACKGROUND_COLOR = '#d3d3d3'
EDITOR_BG_COLOR = '#ffffff'
BUTTON_BG_COLOR = '#d3d3d3'
TEXT_COLOR = '#333333'
FONT_SIZE_TITLE = 12
FONT_SIZE_TEXT = 10

# this function will handle the opening of a LOLCODE file
def open_file(): 
    file_path = fd.askopenfilename(
        title = "Open LOLCODE File",
        filetypes=[("LOLCODE files", "*.lol")] # accepts only lol code files
    )

    if file_path:
        try:
            with open(file_path, 'r') as file:
                code = file.read()
                text_editor.delete('1.0', tk.END) # clears any existing content in the editor
                text_editor.insert(tk.END, code) # inserts the LOLCODE content
                lexemes.delete(*lexemes.get_children()) # clears the lexeme table
                symbol_table.delete(*symbol_table.get_children()) # clears the symbol table
                console.delete('1.0', tk.END) # clears the console
        
        except Exception as e:
            messagebox.showerror("Error", f"Could not open file: {e}")

# this function will handle the execution of the code
def execute_code():
    # get the current contents of the text editor
    code = text_editor.get('1.0', tk.END)
    console.tag_config("error", foreground = "red")
    
    if not code.strip():
        messagebox.showerror("Error", "No code to execute")
        return
    
    # this function will handle the logging of errors to the console
    def gui_log_error(message):
        console.insert(tk.END, message + "\n", "error")
        console.tag_config("error", foreground = "red")
    
    try:
        # lexical analyzer
        lexer = LexAnalyzer(code, log_function = gui_log_error)
        tokens = lexer.tokenize()

        if isinstance(tokens, dict) and "error" in tokens:
            return # errors already logged to gui

        # # printing tokens in terminal
        # print("Tokens:")
        # for token in tokens:
        #     if isinstance(token, Token): # ensure token is a token object
        #         print(f"Lexeme: {token.value}, Classification: {token.type}, Line Number: {token.line_number}")
        
        # clear previous content in the lexeme table
        for item in lexemes.get_children():
            lexemes.delete(item)

        # populate lexeme table with new tokens
        for token in tokens:
            if isinstance(token, Token): # ensure token is a token object
                lexemes.insert("", tk.END, values=(token.value, token.type))

        # update console
        console.delete('1.0', tk.END)
        # console.insert(tk.END, "Lexical analysis successful\n")
    
        # syntax analyzer
        parser = SyntaxAnalyzer(tokens, log_function = gui_log_error)
        syntax_errors = parser.parse_program()
        
        # parser.print_variables()

        # update console
        if syntax_errors:
            console.insert(tk.END, "Syntax analysis failed\n", "error")
            return
        # else:
            # console.insert(tk.END, "Syntax analysis successful\n")
        
        # semantic analyzer
        semantic_analyzer = SemanticAnalyzer(tokens, log_function = gui_log_error, console = console, gui_symbol_table = symbol_table)
        semantic_errors = semantic_analyzer.analyze_program()

        semantic_analyzer.print_symbol_table()
        
        # # clear previous content in the symbol table
        # for item in symbol_table.get_children():
        #     symbol_table.delete(item)

        # # populate symbol table with new variables
        # for identifier, value in semantic_analyzer.symbol_table.items():
        #     symbol_table.insert("", tk.END, values=(identifier, value["value"]))

        # update console
        if semantic_errors:
            console.insert(tk.END, "Semantic analysis failed\n", "error")
        # else:
        #     console.insert(tk.END, "Semantic analysis successful\n")

    except Exception as e:
        messagebox.showerror("Error", str(e))
        console.insert(tk.END, f"Error: {str(e)}\n")

# main window setup
root = tk.Tk()
root.title(f"{GROUP_NAME}")
root.configure(bg = BACKGROUND_COLOR)
root.geometry("1400x800")

# grid weights
root.columnconfigure(0, weight = 1)
root.columnconfigure(1, weight = 1)
root.columnconfigure(2, weight = 1)
root.rowconfigure(1, weight = 1)
root.rowconfigure(2, weight = 1)
root.rowconfigure(4, weight = 1)

# open file button
open_button = tk.Button(root, text = 'Open File', font = font.Font(size = FONT_SIZE_TEXT), bd = 1, bg = BUTTON_BG_COLOR, fg = TEXT_COLOR, relief = "ridge", command = open_file)
open_button.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = "NSEW")

# title 
title = tk.Label(root, text = f"{INTERPRETER_NAME}", font = font.Font(size = FONT_SIZE_TITLE, weight = 'bold'), fg = TEXT_COLOR, bg = BACKGROUND_COLOR)
title.grid(row = 0, column = 1, padx = 5, pady = 5, columnspan = 2, sticky = 'W')

# text editor
text_editor = scrolledtext.ScrolledText(root, width = 75, height = 15, font = ("Consolas", FONT_SIZE_TEXT), bg = EDITOR_BG_COLOR, fg = TEXT_COLOR)
text_editor.grid(row = 1, column = 0, padx = 5, pady = 5, rowspan = 2, sticky = "NSEW")

# lexeme table header
lexeme_header = tk.Label(root, text = "Lexemes", font = font.Font(size = FONT_SIZE_TEXT), fg = TEXT_COLOR, bg = BACKGROUND_COLOR, borderwidth = 1, relief = "ridge")
lexeme_header.grid(row = 1, column = 1, padx = 5, sticky = 'NSEW')

# lexeme table
lexemes = ttk.Treeview(root, selectmode = 'browse', height = 15, columns = ('lexeme', 'classification'))
lexemes.grid(row = 2, column = 1, padx = 5, pady = 5, sticky = "NSEW")
lexemes.column("#0", width = 0, stretch = tk.NO)
lexemes.column("lexeme", anchor = tk.W, width = 205, stretch = tk.NO)
lexemes.column("classification", anchor = tk.W, width = 205, stretch = tk.NO)
lexemes.heading("#0", text = "", anchor = tk.CENTER)
lexemes.heading("lexeme", text = "Lexeme", anchor = tk.CENTER)
lexemes.heading("classification", text = "Classification", anchor = tk.CENTER)

# symbol table header
symbol_header = tk.Label(root, text = "Symbol Table", font = font.Font(size = FONT_SIZE_TEXT), fg = TEXT_COLOR, bg = BACKGROUND_COLOR, borderwidth = 1, relief = "ridge")
symbol_header.grid(row = 1, column = 2, padx = 5, sticky = 'NSEW')

# symbol table
symbol_table = ttk.Treeview(root, selectmode = 'browse', height = 15, columns = ('identifier', 'value'))
symbol_table.grid(row = 2, column = 2, padx = 5, pady = 5, sticky = "NSEW")
symbol_table.column("#0", width = 0, stretch = tk.NO)
symbol_table.column("identifier", anchor = tk.W, width = 205, stretch = tk.NO)
symbol_table.column("value", anchor = tk.W, width = 205, stretch = tk.NO)
symbol_table.heading("#0", text = "", anchor = tk.CENTER)
symbol_table.heading("identifier", text = "Identifier", anchor = tk.CENTER)
symbol_table.heading("value", text = "Value", anchor = tk.CENTER)

# execute button
execute_button = tk.Button(root, text = 'Execute', font = font.Font(size = FONT_SIZE_TEXT), bd = 1, bg = BUTTON_BG_COLOR, fg = TEXT_COLOR, relief = "ridge", command = execute_code)
execute_button.grid(row = 3, column = 0, padx = 5, pady = 5, columnspan = 3, sticky = "NSEW")

# console
console = scrolledtext.ScrolledText(root, wrap = tk.WORD, font = ("Consolas", FONT_SIZE_TEXT), height = 18, bg = EDITOR_BG_COLOR, fg = TEXT_COLOR)
console.grid(row = 4, column = 0, padx = 5, pady = 5, columnspan = 3, sticky = "NSEW")

# style for tables
style = ttk.Style(root)
style.theme_use(THEME)
style.configure("Treeview.Heading", background = BUTTON_BG_COLOR, foreground = TEXT_COLOR, relief = "flat")
style.configure("Treeview", font = ("Consolas", FONT_SIZE_TEXT), background = EDITOR_BG_COLOR, fieldbackground = EDITOR_BG_COLOR, foreground = TEXT_COLOR)

root.mainloop()