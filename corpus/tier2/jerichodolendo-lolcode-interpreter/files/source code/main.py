# Python Regex from https://www.w3schools.com/python/python_regex.asp
# GIMMEH popup window: https://www.tutorialspoint.com/creating-a-popup-message-box-with-an-entry-field-in-tkinter
import re
from regex import *
from decimal import *
from lexical_analyzer import *
from syntax_analyzer import *
from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.scrolledtext import ScrolledText
# from tkinter.messagebox import showinfo

symbolTable = {}

def evaluate(validSyntax):
    global gimmehInput, symbolTable

    symbolTable["IT"] = "NOOB"
    print(validSyntax)
    for x in validSyntax[1]:
        if (x[0] == 'I HAS A'):
            # print("Variable Declaration")
            if (type(x[1]) == tuple):
                # print("Variable Initialization")
                print(type(x[1][2]))
                if (type(x[1][2]) == tuple):
                    symbolTable[x[1][0]] = evaluate2(x[1][2])
                elif (type(x[1][2]) != str):
                    symbolTable[x[1][0]] = x[1][2]
                else:
                    if (re.match(NUMBAR, x[1][2])):
                        symbolTable[x[1][0]] = float(x[1][2])
                    elif (re.match(NUMBR, x[1][2])):
                        symbolTable[x[1][0]] = int(x[1][2])
                    elif (re.match(YARN, x[1][2])):
                        symbolTable[x[1][0]] = str(x[1][2])

                console.insert(END, "SUCCESS\n")
            elif (type(x[1]) == str):
                # print("Variable Uninitialized")
                symbolTable[x[1]] = "NOOB"
                console.insert(END, "SUCCESS\n")
            else:
                console.insert(END, "FAIL\n")
        elif (x[0] == 'GIMMEH'):
            if (x[1] in symbolTable.keys()):
                gimmeh_popup(x[1])
                symbolTable[x[1]] = gimmehInput
                console.insert(END, "SUCCESS\n")
            else:
                print(f"Variable {x[1]} is not yet declared!")
                console.insert(END, "FAIL\n")
        elif (x[0] == 'VISIBLE'):
            if (x[1] in symbolTable.keys()):
                print("VISIBLE <variable>:", symbolTable[x[1]])
                console.insert(END, f"{symbolTable[x[1]]}\n")
            elif (type(x[1]) == tuple):
                print("VISIBLE:", evaluate2(x[1]))
                console.insert(END, evaluate2(x[1]) + "\n")
            else:
                print("VISIBLE:", x[1])
                console.insert(END, f"{x[1]}\n")
        elif (x[0] == 'SUM OF'):
            symbolTable["IT"] = eval_add(x[1])
            console.insert(END, "SUCCESS\n")
        elif (x[0] == 'DIFF OF'):
            symbolTable["IT"] = eval_sub(x[1])
            console.insert(END, "SUCCESS\n")
        elif(x[0] == 'PRODUKT OF'):
            symbolTable["IT"] = eval_mul(x[1])
            console.insert(END, "SUCCESS\n")
        elif(x[0] == 'QUOSHUNT OF'):
            symbolTable["IT"] = eval_div(x[1])
            console.insert(END, "SUCCESS\n")
        elif(x[0] == 'MOD OF'):
            symbolTable["IT"] = eval_mod(x[1])
            console.insert(END, "SUCCESS\n")
        elif(x[0] == 'BIGGR OF'):
            symbolTable["IT"] = eval_biggr(x[1])
            console.insert(END, "SUCCESS\n")
        elif(x[0] == 'SMALLR OF'):
            symbolTable["IT"] = eval_smallr(x[1])
            console.insert(END, "SUCCESS\n")
        elif(x[0] == 'BOTH SAEM'):
            symbolTable["IT"] = eval_both_saem(x[1])
            console.insert(END, "SUCCESS\n")
        elif(x[0] == 'DIFFRINT'):
            symbolTable["IT"] = eval_diffrint(x[1])
            console.insert(END, "SUCCESS\n")
        elif (x[0] == 'R'):
            if (type(x[1]) == tuple):
                if (x[1][0] in symbolTable.keys()):
                    if (type(x[1][1]) == tuple):
                        symbolTable[x[1][0]] = evaluate2(x[1][1])
                    elif (type(x[1][1]) != str):
                        symbolTable[x[1][0]] = x[1][1]
                    else:
                        if (re.match(NUMBAR, x[1][1])):
                            symbolTable[x[1][0]] = float(x[1][1])
                        elif (re.match(NUMBR, x[1][1])):
                            symbolTable[x[1][0]] = int(x[1][1])
                        elif (re.match(YARN, x[1][1])):
                            symbolTable[x[1][0]] = str(x[1][1])
                    console.insert(END, "SUCCESS\n")
                else:
                    print(f"Variable {x[1][0]} is not yet declared!")
                    console.insert(END, "FAIL\n")

    print("SymbolTable (keys = variables; values = value of variable):", symbolTable)
    for symb in symbolTable.items():
        symbTbl.insert("", 'end', values=symb)


def evaluate2(tuple):
    if (tuple[0] == 'SUM OF'):
        return eval_add(tuple[1])
    elif (tuple[0] == 'DIFF OF'):
        return eval_sub(tuple[1])
    elif(tuple[0] == 'PRODUKT OF'):
        return eval_mul(tuple[1])
    elif(tuple[0] == 'QUOSHUNT OF'):
        return eval_div(tuple[1])
    elif(tuple[0] == 'MOD OF'):
        return eval_mod(tuple[1])
    elif(tuple[0] == 'BIGGR OF'):
        return eval_biggr(tuple[1])
    elif(tuple[0] == 'SMALLR OF'):
        return eval_smallr(tuple[1])


def eval_add(values):
    if(values[0] in symbolTable.keys()):
        op1 = symbolTable[values[0]]
    elif(re.match(NUMBAR, values[0])):
        op1 = Decimal(values[0])
    elif(re.match(NUMBR, values[0])):
        op1 = int(values[0])

    if(values[2] in symbolTable.keys()):
        op2 = symbolTable[values[2]]
    elif(re.match(NUMBAR, values[2])):
        op2 = Decimal(values[2])
    elif(re.match(NUMBR, values[2])):
        op2 = int(values[2])

    return op1 + op2


def eval_sub(values):
    if(values[0] in symbolTable.keys()):
        op1 = symbolTable[values[0]]
    elif(re.match(NUMBAR, values[0])):
        op1 = Decimal(values[0])
    elif(re.match(NUMBR, values[0])):
        op1 = int(values[0])

    if(values[2] in symbolTable.keys()):
        op2 = symbolTable[values[2]]
    elif(re.match(NUMBAR, values[2])):
        op2 = Decimal(values[2])
    elif(re.match(NUMBR, values[2])):
        op2 = int(values[2])

    return op1 - op2


def eval_mul(values):
    if(values[0] in symbolTable.keys()):
        op1 = symbolTable[values[0]]
    elif(re.match(NUMBAR, values[0])):
        op1 = Decimal(values[0])
    elif(re.match(NUMBR, values[0])):
        op1 = int(values[0])

    if(values[2] in symbolTable.keys()):
        op2 = symbolTable[values[2]]
    elif(re.match(NUMBAR, values[2])):
        op2 = Decimal(values[2])
    elif(re.match(NUMBR, values[2])):
        op2 = int(values[2])

    return op1 * op2


def eval_div(values):
    if(values[0] in symbolTable.keys()):
        op1 = symbolTable[values[0]]
    elif(re.match(NUMBAR, values[0])):
        op1 = Decimal(values[0])
    elif(re.match(NUMBR, values[0])):
        op1 = int(values[0])

    if(values[2] in symbolTable.keys()):
        op2 = symbolTable[values[2]]
    elif(re.match(NUMBAR, values[2])):
        op2 = Decimal(values[2])
    elif(re.match(NUMBR, values[2])):
        op2 = int(values[2])

    return op1 / op2


def eval_mod(values):
    if(values[0] in symbolTable.keys()):
        op1 = symbolTable[values[0]]
    elif(re.match(NUMBAR, values[0])):
        op1 = Decimal(values[0])
    elif(re.match(NUMBR, values[0])):
        op1 = int(values[0])

    if(values[2] in symbolTable.keys()):
        op2 = symbolTable[values[2]]
    elif(re.match(NUMBAR, values[2])):
        op2 = Decimal(values[2])
    elif(re.match(NUMBR, values[2])):
        op2 = int(values[2])

    return op1 % op2


def eval_biggr(values):
    if(values[0] in symbolTable.keys()):
        op1 = symbolTable[values[0]]
    elif(re.match(NUMBAR, values[0])):
        op1 = Decimal(values[0])
    elif(re.match(NUMBR, values[0])):
        op1 = int(values[0])

    if(values[2] in symbolTable.keys()):
        op2 = symbolTable[values[2]]
    elif(re.match(NUMBAR, values[2])):
        op2 = Decimal(values[2])
    elif(re.match(NUMBR, values[2])):
        op2 = int(values[2])

    return max([op1, op2])


def eval_smallr(values):
    if(values[0] in symbolTable.keys()):
        op1 = symbolTable[values[0]]
    elif(re.match(NUMBAR, values[0])):
        op1 = Decimal(values[0])
    elif(re.match(NUMBR, values[0])):
        op1 = int(values[0])

    if(values[2] in symbolTable.keys()):
        op2 = symbolTable[values[2]]
    elif(re.match(NUMBAR, values[2])):
        op2 = Decimal(values[2])
    elif(re.match(NUMBR, values[2])):
        op2 = int(values[2])

    return min([op1, op2])

def eval_both_saem(values):
    if(values[0] in symbolTable.keys()):
        op1 = symbolTable[values[0]]
    elif(re.match(NUMBAR, values[0])):
        op1 = Decimal(values[0])
    elif(re.match(NUMBR, values[0])):
        op1 = int(values[0])

    if(values[2] in symbolTable.keys()):
        op2 = symbolTable[values[2]]
    elif(re.match(NUMBAR, values[2])):
        op2 = Decimal(values[2])
    elif(re.match(NUMBR, values[2])):
        op2 = int(values[2])

    return 'WIN' if op1 == op2 else 'FAIL'

def eval_diffrint(values):
    if(values[0] in symbolTable.keys()):
        op1 = symbolTable[values[0]]
    elif(re.match(NUMBAR, values[0])):
        op1 = Decimal(values[0])
    elif(re.match(NUMBR, values[0])):
        op1 = int(values[0])

    if(values[2] in symbolTable.keys()):
        op2 = symbolTable[values[2]]
    elif(re.match(NUMBAR, values[2])):
        op2 = Decimal(values[2])
    elif(re.match(NUMBR, values[2])):
        op2 = int(values[2])

    return 'WIN' if op1 != op2 else 'FAIL'


def clear_all():
    global symbolTable
    for item in lexTbl.get_children():
        lexTbl.delete(item)

    for item in symbTbl.get_children():
        symbTbl.delete(item)

    symbolTable = {}
    console.delete("1.0", END)


def execute():
    clear_all()
    tokenList = []  # includes all tokens in input
    lexemeTups = []  # contains tuples of lexemes with their classifications, for inserting to lexeme table
    code = text.get("1.0", "end-1c")    # get input from text box
    lineRgx = r"\"?.+\??\"?\n?"  # regex for getting line
    result = re.findall(lineRgx, code)  # returns list containing lines

    for line in result:
        analyze_tokens(lexemeTups, line)

    # after all analysis, we have lexeme tuples
    # insert them to Treeview
    for item in lexemeTups:
        lexTbl.insert("", "end", values=item)

    for x in range(len(lexemeTups)):
        print(f"lexeme: {lexemeTups[x][0]}\tclass: {lexemeTups[x][1]}")

    validSyntax = program(lexemeTups)

    evaluate(validSyntax)


def openFile():
    file = fd.askopenfilename(
        title='Open files',
        initialdir='/')
    file = open(file, "r")
    data = file.read()

    text.delete('1.0', 'end')
    text.insert('1.0', data)
    file.close()


root = Tk()
root.title('mema peepz interpreter xd')
root.resizable(False, False)
root.geometry('1430x700')


# selecting and reading files: https://pythonguides.com/python-tkinter-read-text-file/
# scrollbars: https://stackoverflow.com/questions/42006805/python-scrolledtext-module

openFileBttn = Button(
    root,
    text='Open Files',
    command=openFile,
    width=70
)

gimmehInput = ''


def gimmehGet_Val(top, e):
    global gimmehInput
    gimmehInput = e.get()
    top.destroy()


def gimmeh_popup(variableName):
    # Create a Toplevel window
    top = Toplevel(root)
    top.geometry("250x100")
    top.title("GIMMEH Input")

    label = Label(top, text=f"Input to be stored in {variableName}:")
    label.pack()

    # Create an Entry Widget in the Toplevel window
    entry = Entry(top, width=25)
    entry.pack()

    # Create a Button to print something in the Entry widget
    Button(top, text="Enter input", command=lambda: gimmehGet_Val(top, entry)).pack(
        pady=5, side=TOP)

    root.wait_window(top)


openFileBttn.grid(column=0, row=0, sticky='w', padx=15, pady=10)

# input box for code
inpContainer = Frame(root, borderwidth=1, relief="sunken")
text = Text(inpContainer, height=18, width=50, wrap=NONE)
scrollX = Scrollbar(inpContainer, orient='horizontal', command=text.xview)
scrollY = Scrollbar(inpContainer, orient='vertical', command=text.yview)
text.configure(xscrollcommand=scrollX.set, yscrollcommand=scrollY.set)

text.grid(row=0, column=0, sticky='nsew')
scrollX.grid(row=1, column=0, sticky='ew')
scrollY.grid(row=0, column=1, sticky='ns')

inpContainer.grid_rowconfigure(0, weight=1)
inpContainer.grid_columnconfigure(0, weight=1)

inpContainer.grid(row=1, column=0, sticky='nsew', padx=15)

# treeview for table: https://www.pythontutorial.net/tkinter/tkinter-treeview/#:~:text=Introduction%20to%20the%20Tkinter%20Treeview,has%20one%20or%20more%20columns.

# tabular view for lexemes
lexVar = StringVar()
lexLbl = Label(root, textvariable=lexVar)

lexVar.set("Lexemes")

lexContainer = Frame(root, borderwidth=1, relief="sunken")
lexCols = ('lexemes', 'class')
lexTbl = ttk.Treeview(lexContainer, columns=lexCols, show="headings")
lexTbl.heading('lexemes', text='Lexemes')
lexTbl.heading('class', text='Classification')
lexScrollX = Scrollbar(lexContainer, orient='horizontal', command=lexTbl.xview)
lexScrollY = Scrollbar(lexContainer, orient='vertical', command=lexTbl.yview)
lexTbl.configure(xscrollcommand=lexScrollX.set, yscrollcommand=lexScrollY.set)

lexTbl.grid(row=0, column=0, sticky='nsew')
lexScrollX.grid(row=1, column=0, sticky='ew')
lexScrollY.grid(row=0, column=1, sticky='ns')

lexContainer.grid_rowconfigure(0, weight=1)
lexContainer.grid_columnconfigure(0, weight=1)

lexLbl.grid(row=0, column=1, padx=15)
lexContainer.grid(row=1, column=1, sticky='nsew', padx=15)

# tabular view for symbols (symbol table)
symbVar = StringVar()
symbLbl = Label(root, textvariable=symbVar)

symbVar.set("Symbol Table")

symbContainer = Frame(root, borderwidth=1, relief="sunken")
symbCols = ('ident', 'val')
symbTbl = ttk.Treeview(symbContainer, columns=symbCols, show="headings")
symbTbl.heading('ident', text='Identifier')
symbTbl.heading('val', text='Value')
symbScrollX = Scrollbar(
    symbContainer, orient='horizontal', command=symbTbl.xview)
symbScrollY = Scrollbar(
    symbContainer, orient='vertical', command=symbTbl.yview)

symbTbl.configure(xscrollcommand=symbScrollX.set,
                  yscrollcommand=symbScrollY.set)
symbTbl.grid(row=0, column=0, sticky='nsew')
symbScrollX.grid(row=1, column=0, sticky='ew')
symbScrollY.grid(row=0, column=1, sticky='ns')

symbContainer.grid_rowconfigure(0, weight=1)
symbContainer.grid_columnconfigure(0, weight=1)

symbLbl.grid(row=0, column=2, padx=15)
symbContainer.grid(row=1, column=2, sticky='nsew', padx=15)

# execute button
outputFrm = Frame(root, borderwidth=1)
execBttn = Button(outputFrm, text='Execute', width=180, command=execute)
execBttn.pack()

outputFrm.grid_rowconfigure(0, weight=1)
outputFrm.grid_columnconfigure(0, weight=1)
outputFrm.grid(row=3, columnspan=3, padx=15, pady=15)

# console
console = Text(outputFrm, height=17, width=170)
console.pack(pady=10)

root.mainloop()
