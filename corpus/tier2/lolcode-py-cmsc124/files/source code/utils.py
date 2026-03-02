def printToConUtil(txt_console, toPrint):
    txt_console.configure(state=NORMAL)
    txt_console.insert(INSERT,str(toPrint))
    txt_console.configure(state=DISABLED)
