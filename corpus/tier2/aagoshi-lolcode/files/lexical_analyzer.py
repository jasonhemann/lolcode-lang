'''
This program creates the initial GUI and lexical analyzer for lolcode interpreter
'''
from tkinter import *
from tkinter import filedialog

class Interpreter():
	def __init__(self, root):
		self.root = root
		self.root.title("Lolcode interpreter")
		self.init_gui()

	def init_gui(self): #set the GUI
		self.rootwidth = 1120
		self.rootheight = 600
		self.root.geometry("%dx%d" % (self.rootwidth, self.rootheight)) 
		self.root.resizable(False, False)
		#top frame where code, token table, and symbol table will be put, invisible
		self.frametop = Frame(self.root,width = self.rootwidth, height = self.rootheight*0.5) #creates frame in middle of the screen where tiles be put
		self.frametop.grid(row = 0, column = 0)
		self.frametop.grid_propagate(0)
		#bottom frame where execute will be done
		self.framebot = Frame(self.root, bg = "white", width = self.rootwidth-20, height = self.rootheight*0.45) #creates frame in middle of the screen where tiles be put
		self.framebot.grid(row = 1 , column = 0, padx = 10, pady = 10)
		self.framebot.grid_propagate(0)
		self.init_codeframe() #frame for entering code under frametop
		self.init_tokenframe() #frame for showing tokentable under frametop
		self.init_symbolframe() #frame for showing symboltable under frametop
		self.init_execFrame() #frame for executing functions under framebottom

	def init_execFrame(self):
		self.execButton = Button(self.framebot, text = "Execute", width = 140)
		self.execButton.grid(row = 0, column = 0, padx = 5, pady = 5)
		self.execScreen = Text(self.framebot,bg = "light gray", width = 135, height = 30)
		self.execScreen.grid(row = 1, column = 0, padx = 5, pady = 5)

	def init_codeframe(self):
		self.codeFrame = Frame(self.frametop, bg = "white", width = self.rootwidth*(1/3)-10, height = self.frametop.winfo_screenheight()*0.4)
		self.codeFrame.grid(row = 0, column = 0, padx = 10, pady = 5)
		self.codeFrame.grid_propagate(0)
		#button that opens files
		self.fileloaderButton = Button(self.codeFrame, text = "Choose a lolcode file", command = self.open_file)
		self.fileloaderButton.pack(side="top", pady = 5)
		#ReadFile Print container!!!
		self.codeBox = Frame(self.codeFrame, bg = "pink",  width = 400, height = self.codeFrame.winfo_screenheight()*0.4-45)
		self.codeBox.pack(side = "left", pady = 5)
		self.codeBox.pack_propagate(0)
		self.codeScroll = Scrollbar(self.codeFrame, orient = "vertical")
		self.codeScroll.pack(side = "right", fill = "y")

	def init_tokenframe(self):
		self.tokenFrame = Frame(self.frametop, bg = "white", width = 100, height = self.frametop.winfo_screenheight()*0.4)
		self.tokenFrame.grid(row = 0, column = 1, padx= 5, pady = 5)
		self.tokenFrame.pack_propagate(0)
		#Row1 - General Label
		self.lexemeLbl = Label(self.tokenFrame, bg = "white",text = "LEXEMES", width = 40)
		self.lexemeLbl.grid(row = 0, column = 0,padx = 5)
		#Row2 - table headers
		self.lexemeHeader = Frame(self.tokenFrame)
		self.lexemeHeader.grid(row = 1, column = 0)
		self.lexemeCol1name = Label(self.lexemeHeader, text = "Lexeme", bg = "pink", borderwidth = 0.5, relief="raised", width = 21)
		self.lexemeCol1name.pack(side = "left")
		self.lexemeCol2name = Label(self.lexemeHeader, text = "Classification", bg = "pink",  borderwidth = 0.5, relief="raised",width = 21)
		self.lexemeCol2name.pack(side = "left")
		#Row3 - scrollable lexeme table - container of lexemes !!!
		self.lexemeScroll = Scrollbar(self.tokenFrame, orient = "vertical")
		self.lexemeScroll.grid(row = 2, column = 1)
		self.lexemeTable = Canvas(self.tokenFrame, bg = "white", width = 300, height = int(self.frametop.winfo_screenheight()*0.4-45),  borderwidth = 1, relief="sunken", yscrollcommand = self.lexemeScroll.set)
		self.lexemeTable.grid(row = 2, column = 0)
		self.lexemeTable.grid_propagate(0)
		self.lexemeScroll.config(command = self.lexemeTable.yview)


	def init_symbolframe(self):
		self.symbolFrame = Frame(self.frametop, bg = "white", width =100, height = self.frametop.winfo_screenheight()*0.4)
		self.symbolFrame.grid(row = 0, column = 2, padx = 10, pady = 5)
		self.symbolFrame.pack_propagate(0)
		#Row1 - General Label
		self.symbolLbl = Label(self.symbolFrame, bg = "white",text = "SYMBOL TABLE", width = 40)
		self.symbolLbl.grid(row = 0, column = 0,padx = 5)
		#Row2 - table headers
		self.symbolHeader = Frame(self.symbolFrame)
		self.symbolHeader.grid(row = 1, column = 0)
		self.symbolCol1name = Label(self.symbolHeader, text = "Indentifier", bg = "pink", borderwidth = 0.5, relief="raised", width = 21)
		self.symbolCol1name.pack(side = "left")
		self.symbolCol2name = Label(self.symbolHeader, text = "Value", bg = "pink",  borderwidth = 0.5, relief="raised",width = 21)
		self.symbolCol2name.pack(side = "left")
		#Row3 - scrollable symbol table - container of symbols !!!
		self.symbolScroll = Scrollbar(self.symbolFrame, orient = "vertical")
		self.symbolScroll.grid(row = 2, column = 1)
		self.symbolTable = Canvas(self.symbolFrame, bg = "white", width = 300, height = int(self.frametop.winfo_screenheight()*0.4-45),  borderwidth = 1, relief="sunken", yscrollcommand = self.symbolScroll.set)
		self.symbolTable.grid(row = 2, column = 0)
		self.symbolTable.grid_propagate(0) #para hindi gumalaw fixed position lang
		self.symbolScroll.config(command = self.symbolTable.yview)

	#after button is clicked, open file, print text to codeBox, start lexical analysis and populating symbol table
	def open_file(self):
		filename = filedialog.askopenfilename(initialdir = ".", filetypes = (("input files","*.lol"),("all files","*.*"))) #start searching in current directory
		cont = self.read_file(filename) #returns the whole file as a single string
		#TO DO lexical analyzer, identify lexemes in string cont
		samplelex = [["HAI", "Code Delimiter"],["I HAS A", "variable Declaration"], ["12", "Literal"]] #sample lexeme table to test printing
		self.fill_lexTable(samplelex)

	#populate the lexeme table with identified lexemes
	#same concept lang din sa symbol table print
	def fill_lexTable(self, lexemes):
		for i in range(len(lexemes)):
			for j in range(len(lexemes[0])):
				Label(self.lexemeTable,bg = "white", text = lexemes[i][j], width = 20).grid(row = i, column = j)

	def read_file(self, filename):
		#Every new read clear contents of previous widgets
		#Note: di pa nagagawa ito ^^ though di pa naman priority
		fh = open(filename ,"r") #read contents of input file
		cont = fh.read() #read whole file into one string named cont
		self.codeText = Text(self.codeBox, width = 60, height = 30, bg = "pink", yscrollcommand = self.codeScroll.set)
		self.codeText.insert(END,cont) #insert whole string as a text
		self.codeText.pack()
		self.codeScroll.config(command = self.codeText.yview) #configure movement of scrollwheel every main loop
		fh.close()
		return cont

#main function for flexibility in case kailanganin
def main():
	root = Tk() #creates tkinter root object
	Interpreter(root)
	root.mainloop()

main()

'''
USEFUL REFERENCES:
tkinter
https://users.tricity.wsu.edu/~bobl/cpts481/tkinter_nmt.pdf
'''
''''
Note: Halos complete na itong GUI. gumawa na rin ako ng pamprint sa table para focus ka lang sa analyzer. I think pareho lang siya ng ginawa sa Rust 2 exer
Di ko pa inaayos ang fonts and colors if gusto mo iedit g lang
TO DO: Lexical analyzer and updating symbol table.
Huwag mo na problemahin muna ang scrolling, ako na siguro dun baka makakuha lang siya ng time mo
'''
