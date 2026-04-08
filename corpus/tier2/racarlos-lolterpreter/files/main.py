from lexerfuncs import * 
import settings

def clearCodeEditor():               		# Function for clearing outPut and code Editor 
	codeEditor.delete('1.0',END)

def clearOutputBox():
	outPut.configure(state="normal")
	outPut.delete('1.0',END)

def getFile():
	clearCodeEditor()
	fileName = filedialog.askopenfilename(filetypes=[("LOL File", "*.lol")], initialdir="tests/",title = "Select a LOL Code File")     # Get the LOL File 
	print("File Name: ",fileName)
	fileHandle = open(fileName,"r+") 		# Read and write 
	fileContent = fileHandle.read()

	codeEditor.insert(END, fileContent)
	fileHandle.close() 

def executeCode():
	outPut.configure(state="normal")

	settings.hasError = False
	settings.errorLine = 0 
	settings.errorMessage = " "

	varDict.clear()
	varDict['IT'] = [None,None]					# Clear Variable Dictionary when getting a new file

	# Reset Contents of Symbol Table and Lexemes 
	for i in lexView.get_children():
		lexView.delete(i)

	for j in symbolView.get_children():
		symbolView.delete(j)

	# Clear Output
	clearOutputBox()
	
	# Variables
	tokens = []															# List of Tokens, will be appended through line tokenizer 
	sourceLines = []													# List of Lines
	visibleLines = []													# Strings to be printed per line in Visible 
	
	sourceLines = codeEditor.get("1.0","end-1c")							# Get the input from the code Editor 
	sourceLines = re.split("\n",sourceLines)							# split into list per newline
	sourceLines = handleComments(sourceLines)							# Remove Comments here 

	if sourceLines == False:

		errorString = "Line: " + str(settings.errorLine) + " " + str(settings.errorMessage)
		outPut.insert(END,errorString)

	else:
		for i in range(len(sourceLines)):									# Checks if the first non comment line is HAI 
			if re.match(empty,sourceLines[i]):	
				pass
			elif re.match(hai,sourceLines[i]):	
				break
			else: 
				printError("Invalid Start of program",sourceLines.index(sourceLines[i]))
				break

		while not(re.match(kthxbye,sourceLines[-1])):						
			print(sourceLines[-1])
			if re.match(empty,sourceLines[-1]): sourceLines.pop()			# removes whitespaces after the KTHXBYE
			else: break														# breaks out of the loop if it encounters anything else other than KTHXBYE

		if not(re.match(kthxbye,sourceLines[-1])) : 
			printError("Invalid End of program",len(sourceLines))			# Last Line must be KTHXBYE 

		print("Lines: ")
		for i in range(len(sourceLines)):
			print(i,"-",sourceLines[i])
		
		value = tokenizer(sourceLines,tokens,visibleLines)							# Tokenize each line
		print("Value: ",value)

		if value == False:															# An Error Has Occurred
			errorString = "Line: " + str(settings.errorLine) + " " + str(settings.errorMessage)
			outPut.insert(END,errorString)
			hasError = None

		elif value != False:
			
			for row in tokens:
				for element in row:
					lexView.insert("","end",values=(element[1],element[0]))

			for element in varDict:
				symbolView.insert("","end",values=(element,varDict[element][1]))
																	
			for element in visibleLines:										# Display Contents of Visiblelines to the output box 
				final = str(element.pop()) + "\n"
				outPut.insert(END, final)

		outPut.configure(state="disabled")



## GUI Part

root = Tk()                             # root 
root.title("League of LolCode")         # Title
root.iconbitmap("favicon.ico")          # Icon
root.geometry("1700x900")               # Default window size is 1600x900

topMainFrame = LabelFrame(root,bg="gray17") 

codeFrame = LabelFrame(topMainFrame,relief='flat',borderwidth=3,bg="dodgerblue3")                   # Code Editor Frame
codeScroll = Scrollbar(codeFrame,orient ="vertical")
codeEditor = Text(codeFrame,width=60,height=20,font=("Helvetica",10),background="LightSteelBlue4",selectbackground="DodgerBlue2",selectforeground="black",undo=True,yscrollcommand=codeScroll.set)

symbolFrame = LabelFrame(topMainFrame,relief='flat',borderwidth=3,bg="dodgerblue3")                # Lexemes Frame 
symbolView = ttk.Treeview(symbolFrame, selectmode="browse",height=18)
symbolView['show'] = 'headings'                                                                     # Remove empty first column
symbolView["columns"] = ("1", "2") 
symbolView.column("1", width = 250, anchor ='w') 
symbolView.column("2", width = 250, anchor ='w') 
symbolView.heading("1", text="Identifier") 
symbolView.heading("2", text="Value") 
symbolScroll = ttk.Scrollbar(symbolFrame,orient ="vertical",command = symbolView.yview)
symbolView.configure(yscrollcommand = symbolScroll.set)

lexFrame = LabelFrame(topMainFrame,relief='flat',borderwidth=3,bg="dodgerblue3")                        # Symbol Table Frame 
lexView = ttk.Treeview(lexFrame, selectmode="browse",height=18)
lexView['show'] = 'headings'                                                                        # Remove empty first column
lexView["columns"] = ("1", "2") 
lexView.column("1", width = 250, anchor ='w') 
lexView.column("2", width = 250, anchor ='w') 
lexView.heading("1", text="Lexeme") 
lexView.heading("2", text="Classification") 
lexScroll = ttk.Scrollbar(lexFrame,orient ="vertical",command = lexView.yview)
lexView.configure(yscrollcommand = lexScroll.set)

bottomMainFrame = LabelFrame(root,bg="gray17")  

buttonFrame = LabelFrame(bottomMainFrame,bg="dodgerblue3",padx=50,pady=10,height=12) 
fileButton = Button(buttonFrame, text="Select File",bd=3,command=getFile, borderwidth = 2,bg ="SlateGray1",width=20,height=2)            # Button Used for Getting a LOL File
execButton = Button(buttonFrame, text="Execute ",bd=3,command=executeCode, borderwidth = 2,bg ="SlateGray1",width=20,height=2)           # Button for executing code in the code frame
clearEditorButton = Button(buttonFrame, text="Clear Editor",bd=3,command=clearCodeEditor ,borderwidth = 2,bg ="SlateGray1",width=20,height=2)   # Button for Clearing the code frame 
clearOutputButton = Button(buttonFrame, text="Clear Output",bd=3,command=clearOutputBox ,borderwidth = 2,bg ="SlateGray1",width=20,height=2)

outFrame = LabelFrame(bottomMainFrame,bg="dodgerblue3",height=300,borderwidth = 2,) 
outPut = Text(outFrame,width=110,height=16,font=("Helvetica",12,"bold"),background="LightSteelBlue4",selectbackground="dodgerblue3",selectforeground="black",state="disabled")

codeLabel = Label(codeFrame,text="Code Editor",font=("Helvetica",15,"bold"),width=30,height=1,bg ="dodgerblue3")
lexLabel = Label(lexFrame,text="Lexemes",font=("Helvetica",15,"bold"),width=30,height=1,bg ="dodgerblue3")
symbolLabel = Label(symbolFrame,text="Symbol Table",font=("Helvetica",15,"bold"),width=30,height=1,bg ="dodgerblue3")

buttonLabel = Label(buttonFrame,text="Buttons",bg ="dodgerblue3",font=("Helvetica",15,"bold"),width=20,height=2)

## GUI Placement

topMainFrame.pack(fill='both',expand=True)                                 # Top Main Frame Arrangement
codeFrame.grid(row=0,column=0,padx=10,pady=5)
lexFrame.grid(row=0,column=1,padx=10,pady=5)
symbolFrame.grid(row=0,column=2,padx=10,pady=5)

codeLabel.pack()
codeScroll.pack(side="right",fill="y")
codeEditor.pack()

lexLabel.pack()                                     # Lex Frame Arrangement
lexScroll.pack(side="right",fill="y")
lexView.pack()

symbolLabel.pack()                               # Symbol Frame Arrangement
symbolScroll.pack(side="right",fill="y")
symbolView.pack()

bottomMainFrame.pack(fill='both',expand=True)                            # Bottom Main Frame Arrangement
buttonFrame.grid_rowconfigure(0,weight=1)
buttonFrame.grid_rowconfigure(1,weight=1)
buttonFrame.grid_rowconfigure(2,weight=1)
buttonFrame.grid_rowconfigure(3,weight=1)
buttonFrame.grid(row=0,column=0,padx=5,pady=10)
outFrame.grid(row=0,column=1,columnspan=2,padx=5,pady=10)




outPut.pack(side="left",fill="both",padx=5,pady=5)

buttonLabel.grid(row=0,padx=8)                                  # Button Frame Arrangement 
fileButton.grid(row=1,padx=8,pady=10)
execButton.grid(row=2,padx=8,pady=10)
clearEditorButton.grid(row=3,padx=8,pady=10)
clearOutputButton.grid(row=4,padx=8,pady=10)




root.mainloop() 

print(varDict)

