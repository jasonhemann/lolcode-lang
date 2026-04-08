'''
This python GUI program is used to support windows operating systems 
'''

# modules imported
import os
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from lexer import *
from new_analyzer_2 import *

# will be used to store the path of the selected file later
f_path = ""

root = Tk() # creates the main Tkinter window.
root.title("LOLTERPRETER") # sets the title of the window
root.geometry("1325x925") # sets the initial dimensions of the window to 1325 pixels width and 925 pixels height
root.resizable(False, False) # disables resizing of the window
root.config(background="white") # sets the background color of the window to white

# function for parsing LOLCODE programs
def parser():
    parsed = []
    global f_path
    file_to_read = open(f_path)
    read_file = file_to_read.read()
    tokens = tokenize(read_file)

    for token in tokens:
        if token[1] == 'WHITESPACE':
            tokens.remove(token)

    parsed = parse_program(tokens)

    if type(parsed) is list:
        lexemes()
        for item in parsed:
            console.insert(END, str(item)+"\n")
    else:
        messagebox.showerror('Parser Error', parsed)

# function for opening a file dialog to select a LOLCODE file
def browse():
    global f_path 
    f_path = askopenfilename(initialdir="/", title="Select File", filetypes=(("LOLCODE files",".lol"),("All Files",".")))
    filename = os.path.basename(f_path)
    files.configure(text=" " + filename)
    file = open(f_path, 'r')
    editor.delete('1.0', END)
    editor.insert(END,file.read())
    file.close()

# function for saving the edited code, parsing it, updating symbols, and displaying results
def execute_save():
    console.config(state=NORMAL)
    global f_path, tokens
    file = open(f_path, 'w')
    file.write(editor.get('1.0',END))
    file.close()
    console.delete('1.0', END)
    lexemes_clear()
    parser()
    # lexemes()
    symbols_clear()
    symbols()
    console.config(state=DISABLED)

'''
the following are the defined widgets along with their specified attributes that will be used in the UI 
'''
folder_photo = PhotoImage(
    file=r"folder.png"
)

title = Label(
    root, 
    text="LOL CODE Interpreter", 
    width=74, 
    anchor="w", 
    font=("Arial",14), 
    pady=3
)

files = Button(
    root, 
    text=" (None)", 
    font=("Arial",12), 
    width=490, 
    command=browse, 
    image = folder_photo, 
    compound=LEFT, 
    anchor="w"
)

editor = Text(
    root, 
    width=55, 
    height=25, 
    bg="white", 
    fg="black", 
    font=("Arial",12)
)
editor.insert(END,"Edit your code here")

lexemes_title = Label(
    root, 
    text="LEXEMES", 
    width=20, 
    bg="white", 
    fg="black", 
    font=("Arial",12,'bold')
)

lexemes_style = ttk.Style()
lexemes_style.theme_use("clam")
lexemes_style.configure("lexemes.Treeview.Heading", font=("Arial", 12), background="black", foreground="white")
lexemes_style.configure("lexemes.Treeview", fieldbackground="white", background="white", padding=2)

lexemes_columns = ("Lexeme", "Classification")

lexemes_list = ttk.Treeview(
    root,
    columns=lexemes_columns,
    show="headings",
    height=19,
    style="lexemes.Treeview"
)

lexemes_list.heading("Lexeme", text="Lexeme")
lexemes_list.heading("Classification", text="Classification")

# function used to populate the lexemes treeview based on the LOLCODE program
def lexemes():
    global f_path
    file_to_read = open(f_path)
    read_file = file_to_read.read()
    tokens = tokenize(read_file)

    for token in tokens:
        if token[1] != 'WHITESPACE':
            lexemes_list.insert('', END, values=token)

# function used to clear the lexemes treeview
def lexemes_clear():
    for token in lexemes_list.get_children():
        lexemes_list.delete(token)

'''
the following are the defined widgets along with their specified attributes that will be used in the UI 
'''
symbols_title = Label(
    root, 
    text="SYMBOL TABLE", 
    width=20, 
    bg="white", 
    fg="black", 
    font=("Arial",12)
)

symbols_style = ttk.Style()
symbols_style.configure("Treeview.Heading", font=("Arial", 12))
symbols_style.configure("Treeview", padding=2)

symbols_columns = ("Identifier", "Value")

symbols_list = ttk.Treeview(
    root,
    columns=symbols_columns,
    show="headings",
    height=19
)

symbols_list.heading("Identifier", text="Identifier")
symbols_list.heading("Value", text="Value")

# function used to populate the symbols treeview with identifier-value pairs
def symbols():
    content_variables = []

    for var in variables:
        content_variables.append((f'{var}', f'{variables[var]}'))

    for content in content_variables:
        symbols_list.insert('', END, values=content)

# function used to clear the symbols treeview
def symbols_clear():
    for var in symbols_list.get_children():
        symbols_list.delete(var)

# button for executing code
execute = Button(
    root, 
    text="EXECUTE", 
    command=execute_save, 
    width=146, 
    font=("Arial",12), 
    pady=2
)

# console for output
console = Text(
    root,
    width=146,
    height=21.5,
    bg="white", 
    fg="black", 
    font=("Arial",12),
    state=DISABLED
)
console.insert(END, "")

# grid layout for organizing widgets
files.grid(row=0,column=0)
title.grid(row=0,column=1,columnspan=2)
editor.grid(row=1,column=0,rowspan=2)
lexemes_title.grid(row=1,column=1)
lexemes_list.grid(row=2, column=1)
symbols_title.grid(row=1,column=2)
symbols_list.grid(row=2, column=2)
execute.grid(row=3,column=0,columnspan=3)
console.grid(row=4,column=0,columnspan=3)

root.mainloop()