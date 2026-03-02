import re
from tkinter import*
import tkinter as tk
from  tkinter import ttk
import tkinter.font as font
from tkinter import scrolledtext
from tkinter import filedialog as fd
import ctypes as ct
import keywords
import syntax
import semantics

global input_checker, input_user

input_checker = 0
input_user = ""

# this will readd the file and store the content in textEditor
def filename():
    filetypes = (
        ('lol files', '*.lol'),
    )


    filename = fd.askopenfilename(filetypes=filetypes)
    file = open(filename, "r")
    textEditor.delete("1.0", "end")
    textEditor.insert("end", file.read(), ("centered",))
   
    file.close()

#this will be responsible for
def analyzetext():
    for row in lexemes.get_children():
        lexemes.delete(row)
    
    console.delete("1.0", "end")

    results = []

    #this part will get all the input in the text editor
    textEditor_Content = textEditor.get("1.0", "end")
    results.append(keywords.lex(textEditor_Content))

    #this part will show the newly added things!!
    for item in results:
        for j in item:
            lexemes.insert("", "end", values=j)
    
    #this part will show the newly added things!!
    
    if syntax.syntax(textEditor_Content) != '>> No syntax errors.':
        console.insert("end", syntax.syntax(textEditor_Content), ("centered",))
    else:
        while True:
            
            newtext = semantics.semantics(textEditor_Content)
            for row in symbolTable.get_children():
                symbolTable.delete(row)
            for item in newtext[2]:
                symbolTable.insert("", "end", values=[item, newtext[2][item]])
            if newtext[0] is None:
                break
            console.insert("end", newtext[0], ("centered",))
            textEditor_Content = newtext[1]
        

root = tk.Tk()
photo = PhotoImage(file = 'logo-TLS.png')
root.iconphoto(False, photo)
root.title("TayLOL Sheesh-terpreter")
root.configure(bg='#0c1818')
root.geometry("1920x1080+-8+0")

top = Toplevel()
top.geometry("180x100")
top.title("toplevel")
top.geometry('400x300+580+300')
top.overrideredirect(True)
top.config(bg='white')
photo1 = PhotoImage(file = 'logo.png').subsample(3,3)
tile = Label(top, image=photo1, highlightthickness=0, borderwidth=0)
tile.place(x=90, y=15)
Label(top, text = 'TayLOL Sheesh', bg='white', fg = 'darkblue', font=font.Font(family='Bahnschrift', size = 20, weight='bold')).place(x=105,y=250)
top.after(2500,lambda:top.destroy())

#this is the opening file button
openButton = tk.Button(root, text='Open File', font=font.Font(size = 10), bd=1, bg='#365963', fg='white', command=lambda:filename())
openButton.grid(row=0, column=0, padx=5, pady=5, sticky="NSEW")

title = Label(root, text = "TayLOL Sheesh-terpreter: A LOL CODE Interpreter", font=font.Font(size = 12, weight='bold'), fg='white',bg='#0c1818')
title.grid(row=0, column=1, padx=5, pady=2.5, columnspan=2, sticky='W')


lexemeHeader = Label(root, text = "Lexemes", font=font.Font(size = 12), fg='white', bg='#0c1818', borderwidth=1, relief="ridge")
lexemeHeader.grid(row=1, column=1, padx=5, sticky='NSEW')


symbolHeader = Label(root, text = "Symbol Table", font=font.Font(size = 12), fg='white', bg='#0c1818', borderwidth=1, relief="ridge")
symbolHeader.grid(row=1, column=2, padx=5, sticky='NSEW')

textEditor = scrolledtext.ScrolledText(root, width = 75, font = ("Courier New", 11), height = 15, bg='#193433', fg='white')
textEditor.grid(row=1, column=0, padx=5, pady=5, rowspan=2, sticky="NSEW")


lexemes = ttk.Treeview(root, selectmode='browse', height=15)
lexemes.grid(row=2, column=1, padx=5, pady=5)
lexemes['columns'] = ('lexeme', 'classification')
lexemes.column("#0", width=0,  stretch=NO)
lexemes.column("lexeme",anchor=CENTER, width=200,stretch=NO)
lexemes.column("classification",anchor=CENTER, width=200,stretch=NO)
lexemes.heading("#0",text="",anchor=CENTER)
lexemes.heading("lexeme",text="Lexeme",anchor=CENTER)
lexemes.heading("classification",text="Classification",anchor=CENTER)


symbolTable = ttk.Treeview(root, selectmode='browse', height=15)
symbolTable.grid(row=2, column=2, padx=5, pady=5)
symbolTable['columns'] = ('identifier', 'value')
symbolTable.column("#0", width=0,  stretch=NO)
symbolTable.column("identifier",anchor=CENTER, width=200,stretch=NO)
symbolTable.column("value",anchor=CENTER, width=200,stretch=NO)
symbolTable.heading("#0",text="",anchor=CENTER)
symbolTable.heading("identifier",text="Identifier",anchor=CENTER)
symbolTable.heading("value",text="Value",anchor=CENTER)


executeButton = tk.Button(root, text='EXECUTE', font=font.Font(size = 10), bd=1, bg='#365963', fg='white',command=lambda:analyzetext())
executeButton.grid(row=3, column=0, padx=5, pady=5, columnspan=3, sticky="NSEW")

console = scrolledtext.ScrolledText(root, wrap = tk.WORD, font = ("Courier New", 12), height = 18, fg='white', bg='#193433')
console.grid(row=4, column=0, padx=5, pady=5, columnspan=3, sticky="NSEW")


# style of tables
style = ttk.Style(root)
style.theme_use("clam")
style.configure("Treeview.Heading", background="#365963", foreground="white", relief="flat")
style.configure("Treeview", background="#193433", fieldbackground="#193433", foreground="white")


root.mainloop()
