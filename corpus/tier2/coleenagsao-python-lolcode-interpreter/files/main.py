

# LOL Code Interpreter
# Author: Agsao, Coleen Therese & Tuazon, Andre (CMSC 124 - T1L)

import re
import grab_lexeme
import check_semantics
import check_syntax
from tkinter import *
from tkinter import filedialog
from tkinter import font
from tkinter import ttk
from tkinter import simpledialog
from check_semantics import get_input

import os
desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')


def get_output():
    return output


def fix_obtw(lexemeArr):
    while (True):
        change = False
        index = 0

        for i in lexemeArr:
            # Chunky parts
            if (i[1] == "comment" and (index+2) < len(lexemeArr)):
                if (lexemeArr[index+1][1] == "linebreak" and lexemeArr[index+2][1] == "linebreak"):
                    del lexemeArr[(index+1):(index+3)]
                    lexemeArr.insert((index+1), ["<linebreak>", "linebreak"])
            index += 1

        break


def lex_analyze(lexemeArr):
    lexemeArr.clear()

    the_long_string = text_editor.get("1.0", 'end-1c')
    lines = the_long_string.split("\n")

    lines2 = []
    for line in lines:
        if (line != ""):
            lines2.append(line.strip())

    for i in range(0, len(lines2)):
        alreadyBlank = False
        if (lines2[i] == ""):
            alreadyBlank = True

        while (lines2[i] != ''):
            grab_lexeme.get_lexemes(lexemeArr, lines2, lines2[i], i)

        if (alreadyBlank == False):
            lexemeArr.append(["<linebreak>", "linebreak"])

    fix_obtw(lexemeArr)

    # for i in lexemeArr:
    #     print(i)

    for item in lexeme_table.get_children():
        lexeme_table.delete(item)

    for i in lexemeArr:
        lexeme_table.insert("", 'end', text="1", values=i)
    #-------------------------------------------------------------------------

    # grab_symbol_table returns [True, symbolTable] if no semantic errors
    # returns [False, symbolTable] if a semantic error is encountered. The symbol table generated before the semantic error is encountered will be displayed.
    # display prompt if there are syntax errors
    output.delete(1.0, END)
    if (check_syntax.check_syntax(lexemeArr)):
        output.insert("end", "[SYNTAX] No errors.\n")
    else:
        output.insert("end", "[SYNTAX] An error is encountered.\n")
        return



    symbolTable = []
    symbolTableResults = check_semantics.grab_symbol_table(
        lexemeArr, symbolTable)
    isSemanticallyCorrect = symbolTableResults[0]
    error = symbolTableResults[1]
    symbolTable = symbolTableResults[2]
    outputArr = []
    outputArr = symbolTableResults[3]

    for item in symbol_table.get_children():
        symbol_table.delete(item)

    for i in symbolTable:
        symbol_table.insert("", 'end', text="1", values=i)

    # output.delete(1.0, END)

    # display print outs
    if len(outputArr) != 0:
        for i in outputArr:
            output.insert("end", str(i) + "\n")

    

    # display prompt if there are semantics errors
    if isSemanticallyCorrect:
        output.insert("end", "[SEMANTICS] No errors.\n")
    else:
        output.insert("end", error)


def browseFiles():
    filename = filedialog.askopenfilename(initialdir=desktop,
                                          title="Select a File",
                                          filetypes=(("LOL files",
                                                      "*.lol*"),
                                                     ("all files",
                                                      "*.*")))

    # Change label contents
    label_fileExplorer.configure(text="File Opened: " + filename)

    # Delete contents of the text_editor
    text_editor.delete(1.0, END)

    # add reading here
    r_file = open(filename, "r")
    content = r_file.read()
    text_editor.insert(END, content)
    r_file.close()


# GUI part
lexemeArr = []
# Root Widget

root = Tk()
root.title("LOLCode Interpreter")
root.state("zoomed")

# file explorer
label_fileExplorer = Label(root, text="None", font=(
    "Cascade Mono", 12), width=90, bg="white")
label_fileExplorer.grid(row=0, column=0, pady=5)

text_editor = Text(root, width=90, height="27", font=(
    "Cascade Mono", 12), selectbackground="gray", selectforeground="black", undo=True)
text_editor.grid(row=2, column=0, pady=10)

label_fileExplorer_icon = Button(
    root, text="Open File", bg="white", width=115, command=browseFiles)
label_fileExplorer_icon.grid(row=1, column=0)

# Lexeme Table
lexeme_table_name = Label(root, text="Lexemes",
                          font=("Cascade Mono", 12), pady=10)
lexeme_table_name.grid(row=1, column=1)

lexeme_table_frame = Frame(root)
lexeme_table_frame.grid(row=2, column=1)

lexeme_table = ttk.Treeview(lexeme_table_frame, columns=(
    "Lexemes", "Classification"), show="headings", height="23")
lexeme_table.grid(row=1, column=1)
lexeme_table.column("# 1", anchor=CENTER)
lexeme_table.heading("# 1", text="Lexemes")
lexeme_table.column("# 2", anchor=CENTER)
lexeme_table.heading("# 2", text="Classification")

lexeme_table_scrollbar = ttk.Scrollbar(
    lexeme_table_frame, orient="vertical", command=lexeme_table.yview)
lexeme_table.configure(yscroll=lexeme_table_scrollbar.set)
lexeme_table_scrollbar.grid(row=1, column=2, sticky="ns")


# Symbol Table
symbol_table_name = Label(root, text="Symbol Table", font=(
    "Cascade Mono", 12), pady=10, anchor=CENTER)
symbol_table_name.grid(row=1, column=2)

symbol_table_frame = Frame(root)
symbol_table_frame.grid(row=2, column=2)

symbol_table = ttk.Treeview(symbol_table_frame, columns=(
    "1", "2", "3"), show="headings", height="23")
symbol_table.grid(row=1, column=1)
symbol_table.column("# 1", anchor=CENTER)
symbol_table.heading("# 1", text="Identifier")
symbol_table.column("# 2", anchor=CENTER)
symbol_table.heading("# 2", text="Value")
symbol_table.column("# 3", anchor=CENTER)
symbol_table.heading("# 3", text="Type")

symbol_table_scrollbar = ttk.Scrollbar(
    symbol_table_frame, orient="vertical", command=symbol_table.yview)
symbol_table.configure(yscroll=symbol_table_scrollbar.set)
symbol_table_scrollbar.grid(row=1, column=2, sticky="ns")

# Execute Button
execute_button = Button(root, text="execute",
                        command=lambda: lex_analyze(lexemeArr))
execute_button.grid(row=3, column=0, columnspan=3)

# Output Box
output = Text(root, width="210", height="20", font=("Cascade Mono", 12),
              selectbackground="gray", selectforeground="black", undo=True)
output.grid(row=4, column=0, columnspan=3, padx=10, pady=5)


root.mainloop()
