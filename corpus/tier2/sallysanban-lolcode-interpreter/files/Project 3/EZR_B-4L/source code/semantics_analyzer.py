import lexical_analyzer
import syntax_analyzer
from tkinter import *
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import tkinter.filedialog
import tkinter.scrolledtext as scrolledtext


import operation_semantics

types = {}
lexemes = {}
newSymbolTable = {}

literals = ["NUMBR literal",
            "NUMBAR literal",
            "YARN literal",
            "TROOF literal",
            "TYPE literal"
            ]

expressionKeywords = {
                        "arithmetic":
                            ["SUM OF",
                            "DIFF OF",
                            "PRODUKT OF",
                            "QUOSHUNT OF",
                            "MOD OF",
                            "BIGGR OF",
                            "SMALLR OF"],
                        "boolean":
                            ["BOTH OF",
                            "EITHER OF",
                            "WON OF",
                            "NOT",
                            "ANY OF",
                            "ALL OF"],
                        "comparison":
                            ["BOTH SAEM",
                            "DIFFRINT"],
                        "concatenation":
                            ["SMOOSH"]
                    }

BACKGROUND_COLOR = "#e0e0de"
filename = ""

def makeTokens():
    global listOfTokens, tokensTree

    tokens = []
    for i in lexemes.keys():
        for j in range(0, len(lexemes[i])):
            tokens.append((lexemes[i][j], types[i][j]))

    x = tokensTree.get_children()
    for item in x:
        tokensTree.delete(item)

    for i in tokens:
        tokensTree.insert('', 'end', text="1", values=i)

def makeSymbolTable(symbolTable):
    global listOfSymbolTable, symbolTableTree
    
    print(f"Symbol table: {symbolTable}")

    refactoredSymbolTable = []
    for i in symbolTable.keys():
        refactoredSymbolTable.append((i, symbolTable[i][0], symbolTable[i][1]))

    for item in symbolTableTree.get_children():
      symbolTableTree.delete(item)

    for i in refactoredSymbolTable:
        symbolTableTree.insert('', 'end', text="1", values=i)

def openFile():
    global filename

    textEditor.delete(1.0, END)

    filename = tkinter.filedialog.askopenfilename()

    if(filename != ""):
        file = open(filename)

        for i in file.readlines():
            textEditor.insert(END, i)

def getInput():
    inputBox.config(state=NORMAL)
    enterButton.config(state=NORMAL)
    enterButton.wait_variable(enterClicked)

    if(inputBox.get() != ""):
        return inputBox.get()
    else:
        return None
    
def saveInput():
    enterClicked.set("button pressed")

def run():
    global filename, lexemes, types, newSymbolTable

    lexemes = {}
    types = {}
    newSymbolTable = {}

    if(textEditor.get(1.0, END) != "\n"):
        console.config(state=NORMAL)
        console.delete(1.0, END)
        console.config(state=DISABLED)

        listOfLines = []
        for i in textEditor.get(1.0, END).splitlines():
            listOfLines.append(i + "\n")

        lines = lexical_analyzer.readFile(listOfLines)
        lexicalError = lexical_analyzer.findLexemes(lines, lexemes, types)

        if(lexicalError != None):
            messagebox.showinfo('Lexical Error', lexicalError)
        else:
            syntaxError = syntax_analyzer.syntax(lexemes, types)

            if(syntaxError != None):
                messagebox.showinfo('Syntax Error', syntaxError)
            else:
                semanticError = semantics()

                if("SemanticError" in semanticError or "SyntaxError" in semanticError):
                    messagebox.showinfo('Semantic Error', semanticError)
                else:
                    makeTokens()
                    makeSymbolTable(semanticError)
    else:
        textEditor.insert(END, "Please open a file or type some code")

def nextLineNumber(lineNumber):
    found = False

    for i in types.keys():
        if(i == lineNumber):
            found = True
            continue
        
        if(found):
            return i

#takes line number, index of the value of variable (which also has the type), and name of variable
def updateSymbolTable(lineNumber, value, variable):
    if(value == "NOOB"):
        newSymbolTable[variable] = ["NOOB", "NOOB"]
    elif(isinstance(value, list)):
        newSymbolTable[variable] = value
    else:
        if(types[lineNumber][value] == "NUMBR literal"):  #value is numbr
            newSymbolTable[variable] = [int(lexemes[lineNumber][value]), "NUMBR literal"]
        elif(types[lineNumber][value] == "NUMBAR literal"):   #value is numbar
            newSymbolTable[variable] = [float(lexemes[lineNumber][value]), "NUMBAR literal"]
        elif(types[lineNumber][value] == "YARN literal"): #value is yarn
            newSymbolTable[variable] = [str(lexemes[lineNumber][value]), "YARN literal"]
        elif(types[lineNumber][value] == "TROOF literal"):    #value is troof
            if(lexemes[lineNumber][value] == "WIN"):
                newSymbolTable[variable] = ["WIN", "TROOF literal"]
            elif(lexemes[lineNumber][value] == "FAIL"):
                newSymbolTable[variable] = ["FAIL", "TROOF literal"]
        else:   #value is type
            return "[Line " + str(lineNumber) + "] SemanticError: cannot store TYPE in identifier"
    
    return "OK"

def arithmeticExpressionSemantics(lineNumber, variable):
    temp = operation_semantics.arithmeticExpSemantics(lineNumber, newSymbolTable, lexemes, types)
    
    # * Semantic Error
    if type(temp) != list:
        return temp

    # * STORES THE FINAL VALUE OF TEMP HERE
    if(variable != "IT"):
        variable = lexemes[lineNumber][1]
    
    updateSymbolTable(lineNumber, [temp[0], temp[1]], variable)

    return "OK"

def booleanExpressionSemantics(lineNumber, variable):
    temp = operation_semantics.booleanExpSemantics(lineNumber, newSymbolTable, lexemes, types)
    
    # * Semantic Error
    if type(temp) != list:
        return temp

    # * STORES THE FINAL VALUE OF TEMP HERE
    if(variable != "IT"):
        variable = lexemes[lineNumber][1]
    
    updateSymbolTable(lineNumber, [temp[0], temp[1]], variable)

    return "OK"

def comparisonExpressionSemantics(lineNumber, variable):
    temp = operation_semantics.booleanExpSemantics(lineNumber, newSymbolTable, lexemes, types)
    
    # * Semantic Error
    if type(temp) != list:
        return temp

    # * STORES THE FINAL VALUE OF TEMP HERE
    if(variable != "IT"):
        variable = lexemes[lineNumber][1]

    updateSymbolTable(lineNumber, [temp[0], temp[1]], variable)

    return "OK"

def concatenationExpressionSemantics(lineNumber, variable):
    temp = operation_semantics.booleanExpSemantics(lineNumber, newSymbolTable, lexemes, types)
    
    # * Semantic Error
    if type(temp) != list:
        return temp
       
    # * STORES THE FINAL VALUE OF TEMP HERE
    if(variable != "IT"):
        variable = lexemes[lineNumber][1]
    
    tempVal = [tempVal, "YARN literal"]

    updateSymbolTable(lineNumber, [temp[0], temp[1]], variable)

    return "OK"
        
def identifierSemantics(lineNumber, variable):
    temp = operation_semantics.identifierExpSemantics(lineNumber, newSymbolTable, lexemes, types)
    
    # * Semantic Error
    if type(temp) != list:
        return temp
    
    print(temp)

    updateSymbolTable(lineNumber, [temp[0], temp[1]], variable)
    print(newSymbolTable)

    return "OK"
        
def switchCaseSemantics(lineNumber, variable):
    # ! FLOW
    # * First line is WTF?
    # * Succeeding lines is OMG, OMGWTF (default case)
    # * Execution stops when there is an GTFO or OIC

    omgLineNumber = []
    gtfoLineNumber = []
    omgWtfLineNumber = -1

    # * Gets the line number of the OMG and OMGWTF
    while lexemes[lineNumber][0] != "OIC":
        if lexemes[lineNumber][0] == "OMG":
            omgLineNumber.append(lineNumber)
        elif(lexemes[lineNumber][0] == "GTFO"):
            gtfoLineNumber.append(lineNumber)
        elif lexemes[lineNumber][0] == "OMGWTF":
            omgWtfLineNumber = lineNumber

        lineNumber = nextLineNumber(lineNumber)
    
    oicLineNumber = lineNumber
    lineNumber = omgLineNumber[0] - 1       # Returns back the line number to where WTF? is
    
    if(len(gtfoLineNumber) != len(omgLineNumber)):
        return "[Line " + str(lineNumber) + "] SyntaxError: Missing GTFO"

    # print(omgLineNumber)            # Checker
    # print(omgWtfLineNumber)
    # print(lineNumber)

    # * Checks if the IT value is equal to the cases in OMG
    checkedLine = -1
    for omg in range(0, len(omgLineNumber)):
        if types[omgLineNumber[omg]][1] in ["identifier", "NUMBR literal", "NUMBAR literal", "TROOF literal", "string delimiter"]:
            if types[omgLineNumber[omg]][1] == "identifier":
                print(lexemes[omgLineNumber[omg]][1])
                if newSymbolTable.get(lexemes[omgLineNumber[omg]][1]):
                    print(newSymbolTable)
                    if str(newSymbolTable[lexemes[omgLineNumber[omg]][1]][0]) == newSymbolTable[variable][0]:
                        checkedLine = omgLineNumber[omg]

                        for i in range(omgLineNumber[omg] + 1, gtfoLineNumber[omg]):
                            if(lexemes[i][0] == "VISIBLE"):
                                SemanticError = visibleSemantics(i)

                                if(SemanticError != "OK"):
                                    return SemanticError
                            elif(lexemes[i][0] == "GIMMEH"):
                                SemanticError = gimmehSemantics(i)

                                if(SemanticError != "OK"):
                                    return SemanticError
                            elif(lexemes[i][0] == "I HAS A"):
                                SemanticError = iHasASemantics(i)

                                if(SemanticError != "OK"):
                                    return SemanticError
                        break
                    else:
                        continue        # If not equal or NOOB type
                else:
                    return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized identifier"
            elif(types[omgLineNumber[omg]][1] in literals or types[omgLineNumber[omg]][1] == "string delimiter"):
                if(types[omgLineNumber[omg]][1] in literals):
                    if lexemes[omgLineNumber[omg]][1] == newSymbolTable[variable][0]:
                        checkedLine = omgLineNumber[omg]

                        for i in range(omgLineNumber[omg] + 1, gtfoLineNumber[omg]):
                            if(lexemes[i][0] == "VISIBLE"):
                                SemanticError = visibleSemantics(i)

                                if(SemanticError != "OK"):
                                    return SemanticError
                            elif(lexemes[i][0] == "GIMMEH"):
                                SemanticError = gimmehSemantics(i)

                                if(SemanticError != "OK"):
                                    return SemanticError
                            elif(lexemes[i][0] == "I HAS A"):
                                SemanticError = iHasASemantics(i)

                                if(SemanticError != "OK"):
                                    return SemanticError
                        break
                elif(types[omgLineNumber[omg]][1] == "string delimiter"):
                    if lexemes[omgLineNumber[omg]][2] == newSymbolTable[variable][0]:
                        checkedLine = omgLineNumber[omg]

                        for i in range(omgLineNumber[omg] + 1, gtfoLineNumber[omg]):
                            if(lexemes[i][0] == "VISIBLE"):
                                SemanticError = visibleSemantics(i)

                                if(SemanticError != "OK"):
                                    return SemanticError
                            elif(lexemes[i][0] == "GIMMEH"):
                                SemanticError = gimmehSemantics(i)

                                if(SemanticError != "OK"):
                                    return SemanticError
                            elif(lexemes[i][0] == "I HAS A"):
                                SemanticError = iHasASemantics(i)

                                if(SemanticError != "OK"):
                                    return SemanticError
                        break
        else:
            return "[Line " + str(lineNumber) + "] SyntaxError: Invalid case"

    if checkedLine == -1:       # GO TO DEFAULT CASE
        if omgWtfLineNumber == -1:      # No default case
            return "[Line " + str(lineNumber) + "] SyntaxError: Missing default case"
        else:       # Go to default case
            for i in range(omgWtfLineNumber, oicLineNumber):
                if(lexemes[i][0] == "VISIBLE"):
                    SemanticError = visibleSemantics(i)

                    if(SemanticError != "OK"):
                        return SemanticError
                elif(lexemes[i][0] == "GIMMEH"):
                    SemanticError = gimmehSemantics(i)

                    if(SemanticError != "OK"):
                        return SemanticError
                elif(lexemes[i][0] == "I HAS A"):
                    SemanticError = iHasASemantics(i)

                    if(SemanticError != "OK"):
                        return SemanticError

    return oicLineNumber

def iHasASemantics(lineNumber):
    if("variable initialization keyword" in types[lineNumber]): #variable has value
        itzLexeme = lexemes[lineNumber].index("ITZ")

        # TODO: doesnt accept if assigns to variable

        if(types[lineNumber][itzLexeme + 1] in literals): #checks if value is literal
            SemanticError = updateSymbolTable(lineNumber, itzLexeme + 1, lexemes[lineNumber][itzLexeme - 1])

            if(SemanticError != "OK"):
                return SemanticError

        elif(types[lineNumber][itzLexeme + 1] == "string delimiter" and types[lineNumber][itzLexeme + 2] == "YARN literal" and types[lineNumber][itzLexeme + 3] == "string delimiter"): #checks if string
            SemanticError = updateSymbolTable(lineNumber, itzLexeme + 2, lexemes[lineNumber][itzLexeme - 1])

            if(SemanticError != "OK"):
                return SemanticError

        elif(lexemes[lineNumber][itzLexeme + 1] in expressionKeywords["arithmetic"] or lexemes[lineNumber][itzLexeme + 1] in expressionKeywords["boolean"] or lexemes[lineNumber][itzLexeme + 1] in expressionKeywords["comparison"] or lexemes[lineNumber][itzLexeme + 1] in expressionKeywords["concatenation"]): #if expression
            SemanticError = arithmeticExpressionSemantics(lineNumber, lexemes[lineNumber][itzLexeme - 1])

            if(SemanticError != "OK"):
                return SemanticError

    else:   #variable has no value
        iHasALexeme = lexemes[lineNumber].index("I HAS A")

        SemanticError = updateSymbolTable(lineNumber, "NOOB", lexemes[lineNumber][iHasALexeme + 1])

        if(SemanticError != "OK"):
            return SemanticError

    return "OK"

def visibleSemantics(lineNumber):
    console.config(state=NORMAL)
    
    temp = operation_semantics.visibleExpSemantics(lineNumber, newSymbolTable, lexemes, types)
    
    # * Semantic Error
    if type(temp) != list:
        return temp
    
    updateSymbolTable(lineNumber, [temp[0], temp[1]], "IT")
    console.insert(END, str(newSymbolTable['IT'][0]) + "\n")
    console.config(state=DISABLED)
    
    return "OK"
    
def gimmehSemantics(lineNumber):
    gimmehLexeme = lexemes[lineNumber].index("GIMMEH")

    userInput = getInput()

    if(userInput != None):
        SemanticError = updateSymbolTable(lineNumber, [userInput, "YARN literal"], lexemes[lineNumber][gimmehLexeme + 1])

        inputBox.delete(0, END)
        inputBox.config(state=DISABLED)
        enterButton.config(state=DISABLED)

        if(SemanticError != "OK"):
            return SemanticError

        return "OK"
    else:
        inputBox.delete(0, END)
        inputBox.config(state=DISABLED)
        enterButton.config(state=DISABLED)

        return "SemanticError: Please enter input"

def semantics():
    lineNumber = list(lexemes.keys())[0]
    lexemeIndex = 0

    while(lineNumber):
        if(lexemes[lineNumber][lexemeIndex] == "I HAS A"):
            SemanticError = iHasASemantics(lineNumber)

            if(SemanticError != "OK"):
                return SemanticError
            
            lineNumber = nextLineNumber(lineNumber)
            continue
        elif(lexemes[lineNumber][lexemeIndex] == "VISIBLE"):
            SemanticError = visibleSemantics(lineNumber)

            if(SemanticError != "OK"):
                return SemanticError

            lineNumber = nextLineNumber(lineNumber)
            continue
        elif(lexemes[lineNumber][lexemeIndex] == "GIMMEH"):
            gimmehSemantics(lineNumber)
            
            lineNumber = nextLineNumber(lineNumber)
            continue
        elif (types[lineNumber][lexemeIndex] == "identifier"):
            if(lexemes[nextLineNumber(lineNumber)][lexemeIndex] == "WTF?"):
                SemanticError = switchCaseSemantics(lineNumber, lexemes[lineNumber][lexemeIndex])      # Returns a line number

                if (type(SemanticError) != int):
                    return SemanticError

                lineNumber = nextLineNumber(SemanticError)
                continue
            else:
                identifier = lexemes[lineNumber][lexemeIndex]
                semanticsError = identifierSemantics(lineNumber, identifier)

                if (semanticsError != "OK"):
                    return semanticsError
                
                lineNumber = nextLineNumber(lineNumber)
                continue
        

        # * GO NEXT LINE
        else:
            lineNumber = nextLineNumber(lineNumber)
            continue
    
    return newSymbolTable

def getLexemes():
    return lexemes

def getTypes():
    return types

# MAIN
#MAIN
screen = Tk()
screen.title('LOLCODE Interpreter')
screen.geometry("1210x750")
screen.configure(bg=BACKGROUND_COLOR)
screen.resizable(False, False)

style = ttk.Style()
# style.theme_use('vista')

# textEditor = scrolledtext.ScrolledText(screen, undo=True, height=20, width=52)
# textEditor.place(x=20, y=40)

textContainer = Frame(screen, borderwidth=1, width=54, height=20)
textEditor = tk.Text(width=54, height=20, wrap="none", borderwidth=0, highlightthickness=0)
scrollBarTextEditorY = tk.Scrollbar(screen, orient="vertical", command=textEditor.yview)
scrollBarTextEditorX = tk.Scrollbar(screen, orient="horizontal", command=textEditor.xview)
scrollBarTextEditorY.pack(side = RIGHT, fill = Y)
scrollBarTextEditorX.pack(side = BOTTOM, fill = X)
textEditor.configure(xscrollcommand=scrollBarTextEditorX.set, yscrollcommand=scrollBarTextEditorY.set)
# scrollBarTextEditorY.grid(row=5, column=3, sticky="nse", padx=20, pady=45)
# scrollBarTextEditorX.grid(row=5, column=2, sticky="ews", padx=20, pady=45)
# textEditor.grid(row=5, column=2, sticky="nsew", padx=20, pady=45)
textEditor.place(x=20, y=43)


fileButton = ttk.Button(
    screen,
    text='Open File',
    command=lambda:openFile()
)
fileButton.place(x=20, y=15)


tokensLabel = ttk.Label(screen, text="Tokens", background=BACKGROUND_COLOR)
tokensLabel.place(x=470, y=20)
listOfTokens = Listbox(screen, height=20, width=53)
listOfTokens.place(x=470, y=40)

symbolTableLabel = ttk.Label(screen, text="Symbol Table", background=BACKGROUND_COLOR)
symbolTableLabel.place(x=855, y=20)
listOfSymbolTable = Listbox(screen, height=20, width=60, state=DISABLED)
listOfSymbolTable.place(x=845, y=40)

console = scrolledtext.ScrolledText(screen, height=18, width=142, state=DISABLED)
console.place(x=21, y=380)

inputBox = Entry(screen, width=180, state=DISABLED)
inputBox.place(x=21, y=670)

enterClicked = StringVar()
enterButton = ttk.Button(
    screen,
    text='Enter',
    state=DISABLED,
    command=lambda:saveInput()
)
enterButton.place(x=1100, y=667)

runButton = ttk.Button(
    screen,
    text='Run',
    command=lambda:run()
)
runButton.place(x=1100, y=700)

tokensTree = ttk.Treeview(listOfTokens, column=("c1", "c2"), show='headings', height=15)

scrollBarTokens = ttk.Scrollbar(listOfTokens, orient ="vertical", command = tokensTree.yview)
scrollBarTokens.pack(side = RIGHT, fill = Y)

tokensTree.pack(side=LEFT)

tokensTree.configure(yscrollcommand = scrollBarTokens.set)
tokensTree.column("# 1", anchor=CENTER, width=170)
tokensTree.heading("# 1", text="Lexeme")
tokensTree.column("# 2", anchor=CENTER, width=170)
tokensTree.heading("# 2", text="Type")

symbolTableTree = ttk.Treeview(listOfSymbolTable, column=("c1", "c2", "c3"), show='headings', height=15)

scrollBarSymbolTable = ttk.Scrollbar(listOfSymbolTable, orient ="vertical", command = symbolTableTree.yview)
scrollBarSymbolTable.pack(side = RIGHT, fill = Y)

symbolTableTree.pack(side=LEFT)

symbolTableTree.configure(yscrollcommand = scrollBarSymbolTable.set)
symbolTableTree.column("# 1", anchor=CENTER, width=102)
symbolTableTree.heading("# 1", text="Identifier")
symbolTableTree.column("# 2", anchor=CENTER, width=102)
symbolTableTree.heading("# 2", text="Value")
symbolTableTree.column("# 3", anchor=CENTER, width=102)
symbolTableTree.heading("# 3", text="Type")

screen.mainloop()
        
        
