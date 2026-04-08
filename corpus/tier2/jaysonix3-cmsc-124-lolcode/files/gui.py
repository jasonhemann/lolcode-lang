# from win32 import win32api
# from win32api import GetSystemMetrics
import re
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import font
from tkinter import filedialog
from tkinter.ttk import *
import lexer

#Create an instance of tkinter frame
root = Tk() #whole screen
root.title("LOLCODE Interpreter") #program name
root.iconbitmap('lolcodeicon.ico') #icon
root.config(bg="#24262A") #background color
root.geometry("1000x730") #background size
root.resizable(False,False) #not resizeable window
# root.geometry(f"373x395+{int(GetSystemMetrics(0)/2)-300}+40")

def _deleteAllText():
    showtext.delete('1.0', END)

def _deleteAllOutput():
    evaluatetext.configure(state='normal')
    evaluatetext.delete('1.0', END)

def _openFile():
    _deleteAllText()
    filepath = filedialog.askopenfilename(initialdir="C:\\Users\\stephanie\\Documents",
                                            title="Select LOLCODE File",
                                            filetypes=(("lol files", "*.lol"),("all files","*.*"))
                                            )
    print("Selected File's Path: ", filepath) #checker if correct filepath see terminal
    file = open(filepath, 'r+') #read and write lolcode to textbox
    read = file.read()   

    showtext.tag_config('details', foreground="white") #change font color
    showtext.insert(END, read, 'details')

    filename = filepath.split("/")[len(filepath.split("/"))-1] #display filename current selected file
    showfile['text'] = filename
    file.close()

def _evaluate():
    evaluatetext.configure(state='normal')

    for values in lextree.get_children():
        lextree.delete(values)

    for values in symbtree.get_children():
        symbtree.delete(values)

    _deleteAllOutput()

    file = showtext.get("1.0", "end-1c")
    file = re.split("\n", file)
    # lexemes = []
    # file = showtext.get("1.0", "end-1c")
    ret = lexer.detect_tokens(file)
    printtok = lexer.create_tok(ret)
    for element in printtok:
        lextree.insert("","end", values=(element[1], element[0]))
    # return printtok
    evaluatetext.config(state='disabled')

#lagay table here
def _lexerprint():
    _evaluate()

#CONTAINER LEFT
textarea= tk.Frame(height=380, width=430, bg="#24262A", background="#24262A", highlightbackground="white", highlightthickness=0.75)
textarea.grid(row=0, column=0, padx=9, pady=5)

showfile = tk.Label(textarea, text='PLEASE CHOOSE A FILE', anchor=CENTER, font=("Arial", 10), width=40, height=1, padx=15, pady=5, fg="#545657")
showfile.grid(row=0, column=0, padx=5, pady=5)

openIcon = PhotoImage(file = 'fileopen.png')
photoimage = openIcon.subsample(65, 65) 
openfileButton = tk.Button(textarea, image = photoimage, command=_openFile)
openfileButton.grid(row=0, column=1)

showtext= tk.Text(textarea, height=20, width=50, bg="#24262A", highlightbackground="#24262A", highlightthickness=0)
showtext.grid(row=1, column=0, columnspan=2, padx=9, pady=5)

#CONTAINER RIGHT
tablearea= tk.Frame(height=300, width=430, bg="#24262A", background="#24262A", highlightbackground="white", highlightthickness=0.75)
tablearea.grid(row=0, column=1, padx=9, pady=5)

tabletitle = tk.Label(tablearea, text="LOL CODE INTERPRETER", anchor=CENTER, font=("Arial", 13), width=57, height=1, fg="white", bg="#007C8A")
tabletitle.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

lexemestitle = tk.Label(tablearea, text="LEXEMES", anchor=CENTER, font=("Arial", 10), width=19, height=1, padx=15, pady=5, fg = "white", bg = "#24262A")
lexemestitle.grid(row=1, column=0, padx=5, pady=5)

symtabletitle = tk.Label(tablearea, text="SYMBOL TABLE", anchor=CENTER, font=("Arial", 10), width=19, height=1, padx=15, pady=5, fg = "white", bg = "#24262A")
symtabletitle.grid(row=1, column=1, padx=5, pady=5)

showlexemes= tk.Text(tablearea, height=15, width=23, bg="#24262A", highlightbackground="#24262A", highlightthickness=0, padx=5, pady=5)
showlexemes.grid(row=2, column=0, padx=5, pady=2)

showsymtable= tk.Text(tablearea, height=15, width=23, bg="#24262A", highlightbackground="#24262A", highlightthickness=0, padx=5, pady=5)
showsymtable.grid(row=2, column=1, padx=5, pady=2)

evaluateButton = tk.Button(text='E V A L U A T E', anchor=CENTER, font=("Arial", 13), width=108, height=1, fg="white", 
                    bg="#007C8A", command=_evaluate)
evaluateButton.grid(row=1, column=0, columnspan = 2, padx=5, pady=5)

#CONTAINER BOTTOM
evaluatearea= tk.Frame(height=300, width=890, bg="#24262A", background="#24262A", highlightbackground="white", highlightthickness=0.75)
evaluatearea.grid(row=2, column=0, columnspan = 2, padx=9, pady=5)

evaluatetext= tk.Text(evaluatearea, height=17, width=120, bg="#24262A", highlightbackground="#24262A", highlightthickness=0, state='disabled')
evaluatetext.grid(row=0, column=0, columnspan = 2, padx=9, pady=5)

#TREE CONTAINER RIGHT COLUMN 0 LEX TABLE
style = ttk.Style()

style.theme_use("clam")
style.configure("Treeview.Heading", background="#007C8A", foreground="white")

style.configure('Treeview', 
            background = "#24262A", 
            foreground ="white",
            rowheight = 25,
            fieldbackground = "#24262A")

style.map('Treeview', background=[('selected', '#007C8A')])

lextree = ttk.Treeview(showlexemes)

lextree['columns'] = ("Lexeme", "Classification")

lextree.column("#0", width=0, stretch = NO)
lextree.column("Classification", anchor=CENTER, width=120)
lextree.column("Lexeme", anchor=CENTER, width=120)

lextree.heading("#0", text="", anchor=CENTER)
lextree.heading("Classification", text = "Classification", anchor=CENTER)
lextree.heading("Lexeme", text="Lexeme", anchor=CENTER)

lextree.pack()

#TREE CONTAINER RIGHT COLUMN 1 SYMBOL TABLE
symbtree = ttk.Treeview(showsymtable)

symbtree['columns'] = ("Identifier", "Value")

symbtree.column("#0", width=0, stretch = NO)
symbtree.column("Identifier", anchor=CENTER, width=120)
symbtree.column("Value", anchor=CENTER, width=120)

symbtree.heading("#0", text="", anchor=CENTER)
symbtree.heading("Identifier", text = "Identifier", anchor=CENTER)
symbtree.heading("Value", text="Value", anchor=CENTER)

data = []

count= 0
for record in data:
    symbtree.insert(parent='', index='end', iid=count, text='', values=(record[1], record[0]))
    count += 1

symbtree.pack()


root.mainloop()