import tkinter as tk
from tkinter import *
from tkinter import Scrollbar, ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from error import Error
from lexer import *
from parser import Parser


def open_file():
    """Open a file for editing."""
    filepath = askopenfilename(
        filetypes=[("LOLCode", ".lol")]
    )
    if not filepath:
        return
    txt_edit.delete(1.0, tk.END)
    with open(filepath, "r") as input_file:
        text = input_file.read()
        txt_edit.insert(tk.INSERT, text)
    window.title(f"LOLCODE INTERPRETER - {filepath}")

def save_file():
    """Save the current file as a new file."""
    filepath = asksaveasfilename(
        defaultextension="txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
    )
    if not filepath:
        return
    with open(filepath, "w") as output_file:
        text = txt_edit.get(1.0, tk.END)
        output_file.write(text)
    window.title(f"LOLCODE INTERPRETER - {filepath}")

def getTokens():
    # clear console
    txt_console.configure(state=NORMAL)
    txt_console.delete("1.0",tk.END)
    txt_console.configure(state=DISABLED)

    """Insert tokens in the Lexemes Treeview"""
    lx = Lexer()
    lx.input(txt_edit.get(1.0,END))
    # clear previous items in the lexemes treeview
    for x in tbl_lex.get_children():
        tbl_lex.delete(x)

    # put tokens in a list
    try:
        tokens = list(lx.tokens())
    except LexerError as e:
        txt_console.configure(state=NORMAL)
        txt_console.insert(INSERT,str(e))
        txt_console.configure(state=DISABLED)
        return
        

    # insert the generated token in the lexemes treeview
    for index,token in enumerate(tokens):
        if token.type in (TT_NEWLINE):
            continue
        tbl_lex.insert("",'end',iid=index,
		values=(token.val,token.type))

    # clear contents of symbol table
    for x in tbl_sym.get_children():
        tbl_sym.delete(x)
    
    # parse the tokens
    res = Parser(tokens, txt_console, tbl_sym)

    # put into console the output of the parser
    parse = res.parse()
    if isinstance(parse, Error):
        txt_console.configure(state=NORMAL)
        txt_console.insert(INSERT,str(parse))
        txt_console.configure(state=DISABLED)

def printToCon(toPrint):
    txt_console.configure(state=NORMAL)
    txt_console.insert(INSERT,str(toPrint))
    txt_console.configure(state=DISABLED)

window = tk.Tk()
window.title("LOLCODE INTERPRETER")
window.columnconfigure(0, weight=1)
window.rowconfigure(0, weight=1)
window.rowconfigure(1, weight=1)

#Frame for upper subwindows
fr_upper = tk.Frame(window)
fr_upper.grid(row=0,column=0, sticky=NW)
#Frame for File Explorer and Text Editor
fr_code = tk.Frame(fr_upper)
fr_code.grid(row=0, column=0, padx=5, sticky=N)
#Frame for List of tokens and Symbol Table
fr_tokens = tk.Frame(fr_upper)
fr_tokens.grid(row=0, column=1, sticky=N)
#Frame for Execute button and console/Lower subwindows
fr_run = tk.Frame(window)
fr_run.grid(row=1,column=0)

#Frame for File Explorer
fr_buttons = tk.Frame(fr_code)
fr_buttons.columnconfigure(0, weight=1)
fr_buttons.rowconfigure(0, weight=1)
fr_buttons.pack(expand=True)

#Button to open File Explorer
btn_open = tk.Button(fr_buttons, text="Open", command=open_file)
btn_open.grid(row=0, column=0, sticky='nesw')

#Text Editor
sb_edity = Scrollbar(fr_code)
sb_edity.pack(side=RIGHT,fill=Y)
sb_editx = Scrollbar(fr_code,orient=HORIZONTAL)
sb_editx.pack(side=BOTTOM,fill=X)

txt_edit = tk.Text(fr_code,width=50,height=15, wrap=NONE, yscrollcommand=sb_edity.set, xscrollcommand=sb_editx.set)
txt_edit.pack()

sb_edity.config(command=txt_edit.yview)
sb_editx.config(command=txt_edit.xview)

#Frame for List of tokens
fr_lex = tk.Frame(fr_tokens)
fr_lex.grid(row=0, column=0, sticky=N)

lb_lex = tk.Label(fr_lex,text="Lexemes", pady=5)
lb_lex.pack()

#Table for Lexemes
sb_lex = Scrollbar(fr_lex)
sb_lex.pack(side=RIGHT,fill=Y)

tbl_lex = ttk.Treeview(fr_lex, yscrollcommand=sb_lex.set, height=11)
tbl_lex['columns'] = ('Lexeme', 'Classification')

tbl_lex.column('#0', width=0, stretch=NO)
tbl_lex.column('Lexeme', anchor=CENTER, width=200)
tbl_lex.column('Classification', anchor=CENTER, width=200)

tbl_lex.heading('#0', text="",anchor=CENTER)
tbl_lex.heading('Lexeme', text="Lexeme",anchor=CENTER)
tbl_lex.heading('Classification', text="Classification",anchor=CENTER)

sb_lex.config(command=tbl_lex.yview)

tbl_lex.pack()

#Frame for Symbol table
fr_sym = tk.Frame(fr_tokens)
fr_sym.grid(row=0, column=1, sticky=N)

lb_sym = tk.Label(fr_sym,text="Symbol Table", pady=5)
lb_sym.pack()

#Table for Lexemes
sb_sym = Scrollbar(fr_sym)
sb_sym.pack(side=RIGHT,fill=Y)

tbl_sym = ttk.Treeview(fr_sym, yscrollcommand=sb_sym.set, height=11)
tbl_sym['columns'] = ('Identifier', 'Value')

tbl_sym.column('#0', width=0, stretch=NO)
tbl_sym.column('Identifier', anchor=CENTER, width=200)
tbl_sym.column('Value', anchor=CENTER, width=200)

tbl_sym.heading('#0', text="",anchor=CENTER)
tbl_sym.heading('Identifier', text="Identifier",anchor=CENTER)
tbl_sym.heading('Value', text="Value",anchor=CENTER)

sb_sym.config(command=tbl_sym.yview)

tbl_sym.pack()

#Execute Button
btn_execute = tk.Button(fr_run, text="EXECUTE", command=getTokens)
btn_execute.pack()

#Console
sb_consoley = Scrollbar(fr_run)
sb_consoley.pack(side=RIGHT,fill=Y)
sb_consolex = Scrollbar(fr_run,orient=HORIZONTAL)
sb_consolex.pack(side=BOTTOM,fill=X)

txt_console = tk.Text(fr_run, width=155, state=DISABLED, wrap=NONE, yscrollcommand=sb_consoley.set, xscrollcommand=sb_consolex.set)
txt_console.pack()

sb_consoley.config(command=txt_console.yview)
sb_consolex.config(command=txt_console.xview)


window.mainloop()
