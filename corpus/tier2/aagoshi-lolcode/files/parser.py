'''
This program creates the initial GUI and lexical analyzer for lolcode interpreter
'''
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import copy
import re

class Token():
	def __init__(self, token, ttype, row, col):
		self.tok = token              #string of token
		self.type = ttype      		  #type of token
		self.row = row                #row/line where it is located
		self.col = col 			  
		self.value = None             #no value yet

class Statement():
	def __init__(self, tokens, ttype):
		self.tokens = tokens              #list of Tokens in that statement
		self.type = ttype                 #type of the statement:
		self.valueTable = []			  #wala pa use pero baka pwede para pagnaguupdate ng symbol Table?

	def appendTok(self, tok):
		self.tokens.append(tok) 		  #appends to Statement's tokens list

	def decode(self):					#parang semantic analyzer ng per statement # di ko sure kung mas tama siya ilagay dito o sa semantic analyzer na lang
		if self.type == "<PRINT>":			
			print("Successfully decoded print")
			if self.tokens[2].type == "String_Literal":	#expected combination ["VISIBLE",'"', StringLiteralToken, '"']
				#do whatever printing is supposed to do #DUMMY OUTPUT
				print("THIS IS A DUMMY OUTPUT IN PRINT STATEMENT WITH VALUE OF :" + self.tokens[2].tok )
		elif self.type == "<OUTPUT>":
			print("THIS IS A DUMMY OUTPUT IN OUTPUT STATEMENT WITH VALUE OF :" + self.tokens[1].tok ) #DUMMY OUTPUT


class Syntax_Analyzer():
	def __init__(self, tokens):
		self.tokens = tokens         	#tokens list
		self.tokindex = 0 	            #current token index
		self.parsetree = None			#[STATEMENT1, STATEMENT2, STATEMENT3] will look like this
		self.program()

	#forward to next index in self.tokens 
	def next(self):
		self.tokindex = self.tokindex + 1

	#where main syntax analysis is done
	def parse(self):
		pass

	#or dapat ba line per line ng token na nakaloop?? instead na per function??
	def program(self): # <program>	::=	HAI <linebreak> <statement> <linebreak> KTHXBYE
		if self.tokens[0].tok == "HAI":
			if self.tokens[-1].tok == "KTHXBYE": #something like this though di ko sure kung tama na pagsabayin o line per line dapat
				print(str(self.tokindex) + " ")	 #checking lang kung nasaang index na
				self.parsetree = []				 #initialize parse tree tells that a program has started
				self.next() #because this is the first statement move to index 1
				self.statement()
			else: print("SYNTAX ERROR: KTHXBYE expected on line " + str(self.tokens[-1].row)) #di ko sure kunt tama icheck agad kthxbye baka skip muna ito
		else: print("SYNTAX ERROR: HAI expected on line " + str(self.tokens[0].row))

	def statement(self): #<statement> ::= <statement><linebreak><statement> | <expression> | <switchcase> | <ifthen> | <varcall> | <print> | <input> 
		print(str(self.tokindex) + " ")
		if self.tokens[self.tokindex].type == "Output_Keyword": #for VISIBLE/ <print> case
			self.parsetree.append(Statement([self.tokens[self.tokindex]], "<PRINT>"))
			self.next()
			self.print()
		elif self.tokens[self.tokindex].type == "Accept_Keyword": #for GIMMEH/ <input> case
			self.parsetree.append(Statement([self.tokens[self.tokindex]], "<INPUT>"))
			self.next()
			self.input()

	def print(self):
		print(str(self.tokindex) + " ")
		if self.tokens[self.tokindex].type == "String_Delimiter": #for string literal case #Statement.tokens will look like this: ["VISIBLE",'"', StringLiteralToken, '"'] 
			self.parsetree[-1].appendTok(self.tokens[self.tokindex]) 		#calls the statement method appendTok and adds tokens to the Tokens list of the most recent statement
			self.next()
			self.next() #move 2 indeces
			if self.tokens[self.tokindex].type == "String_Delimiter":
				self.parsetree[-1].appendTok(self.tokens[self.tokindex-1])    #adds the end string delimiter
				self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds string literal
				print(str(self.tokindex) + " ")
				print(print(self.tokens[self.tokindex-1].tok)) #print the middle item
				self.next()
				self.statement()							   #back to self.statement to check if there are more statements /recursively call it again
			else: print("SYNTAX ERROR: String Delimiter expected on line " + str(self.tokens[self.tokindex].row))

	def input(self):
		print(str(self.tokindex) + " ")
		if self.tokens[self.tokindex].type == "Identifier":		#if type is an identifier
			self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
			print(str(self.tokindex) + " ")
			self.next()
			self.statement()
		else: print("SYNTAX ERROR: Identifier expected on line: " + str(self.tokens[self.tokindex].row))


class Interpreter():
	def __init__(self, root):
		self.root = root
		self.line_num = 1
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
		#Row2 - scrollable lexeme table - uses Treeview
		self.lexemeTableGUI = ttk.Treeview(self.tokenFrame, selectmode ='extend')
		self.lexemeTableGUI.grid(row = 1, column = 0)
		self.lexemeTableGUI["columns"] = ("1", "2") 
		self.lexemeTableGUI["show"] = "headings"
		self.lexemeTableGUI.column("1", width=150)
		self.lexemeTableGUI.column("2",  width=150)
		self.lexemeTableGUI.heading("1", text ="Lexeme") 
		self.lexemeTableGUI.heading("2", text ="Classification") 
		#scroll bar on right of canvas
		self.lexemeScroll = Scrollbar( self.tokenFrame, orient = "vertical", command = self.lexemeTableGUI.yview)
		self.lexemeScroll.grid(row = 1, column = 1, sticky = "NS")
		self.lexemeTableGUI.configure(yscrollcommand = self.lexemeScroll.set)

	def init_symbolframe(self):
		self.symbolFrame = Frame(self.frametop, bg = "white", width =100, height = self.frametop.winfo_screenheight()*0.4)
		self.symbolFrame.grid(row = 0, column = 2, padx = 10, pady = 5)
		self.symbolFrame.pack_propagate(0)
		#Row1 - General Label
		self.symbolLbl = Label(self.symbolFrame, bg = "white",text = "SYMBOL TABLE", width = 40)
		self.symbolLbl.grid(row = 0, column = 0,padx = 5)
		#Row2 - scrollable lexeme table - uses Treeview
		self.symbolTableGUI = ttk.Treeview(self.symbolFrame, selectmode ='extend')
		self.symbolTableGUI.grid(row = 1, column = 0)
		self.symbolTableGUI["columns"] = ("symb1", "symb2") 
		self.symbolTableGUI["show"] = "headings"
		self.symbolTableGUI.column("symb1", width=150)
		self.symbolTableGUI.column("symb2",  width=150)
		self.symbolTableGUI.heading("symb1", text ="Identifier") 
		self.symbolTableGUI.heading("symb2", text ="Value") 
		#scroll bar on right of canvas
		self.symbolScroll = Scrollbar( self.symbolFrame, orient = "vertical", command = self.symbolTableGUI.yview)
		self.symbolScroll.grid(row = 1, column = 1, sticky = "NS")
		self.symbolTableGUI.configure(yscrollcommand = self.symbolScroll.set)

	#after button is clicked, open file, print text to codeBox, start lexical analysis and populating symbol table
	def open_file(self):
		filename = filedialog.askopenfilename(initialdir = ".", filetypes = (("input files","*.lol"),("all files","*.*"))) #start searching in current directory
		content = self.read_file(filename) #returns the whole file as a single string

		#LEXICAL ANALYSIS
		lexemes = [] #formerly samplelex, pinaltan lang para mas malinis
		tokens = self.lexical_analyzer(content) #performs lexical analysis
		#reformats tokens in lexemes list for printing in lexemeTable
		for i in range(0,len(tokens)):
			lexemes.append([tokens[i].tok, tokens[i].type])
			print("  " + str(tokens[i].row) + " " + str(tokens[i].tok) )
		# lexemes = [["HAI", "Code Delimiter"],["I HAS A", "variable Declaration"], ["12", "Literal"]] #sample lexeme table to test printing
		self.fill_lexTable(lexemes)

		#UPDATE SYMBOL TABLE 
		self.update_symbolTable(tokens)

		#SYNTAX ANALYSIS
		syntax = Syntax_Analyzer(tokens) 
		#checking contents of parse tree
		for statement in syntax.parsetree:
			print("Statement: " + str(statement.type) + " ")
			for token in statement.tokens:  #print token in tokens
				print("\t" + str(token.tok))

		#ATTEMPTING DUMMY SEMANTIC ANALYZER
		for statement in syntax.parsetree:
			print("Statement: " + str(statement.type) + " ")
			statement.decode()
			#update symbol table?? 



	#populate the lexeme table with identified lexemes
	def fill_lexTable(self, lexemes):
		for i in range(len(lexemes)):
			self.lexemeTableGUI.insert(parent='', index='end', iid=i, text="", values=(lexemes[i][0], lexemes[i][1]))

	def update_symbolTable(self,symbols):
		self.symbolTable = copy.deepcopy(symbols)
		for i in range(len(self.symbolTable)):
			self.symbolTableGUI.insert(parent='', index='end', iid=i, text="", values=(self.symbolTable[i].tok, self.symbolTable[i].type))


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

	#removes the original lexical analyzer and replaced tokenized as the sole lexical analyzer function 
	#the lexical analyzer functions
	def lexical_analyzer(self, code):
		tokens = [					#list of token types and corresponding patterns
			('OBTWComment', r'OBTW'),
			('TLDRComment', r'TLDR'),
			('Comment', r'BTW.*'),	#single line comment
			('Code_Delimiter', r'(HAI|KTHXBYE)'),
            ('Variable_Declaration', r'I HAS A'),       
            ('Variable_Identifier', r'var'),
            ('Assignment', r'R'),
            ('Variable_Assignment', r'ITZ'),
            ('Output_Keyword', r'VISIBLE'),
            ('String', r'".*?"'),
            ('TROOF', r'(WIN|FAIL)'),
            ('Op_Sep', r'AN'),
            ('Arithmetic_Op', r'(SUM OF|DIFF OF|PRODUKT OF|QUOSHUNT OF|MOD OF|BIGGR OF|SMALLR OF)'),
            ('Boolean_Op', r'(BOTH OF|EITHER OF|WON OF|NOT|ALL OF|ANY OF)'),
            ('Comparison_Op', r'(BOTH SAEM|DIFFRINT)'),
            ('Accept_Keyword', r'GIMMEH'),
            ('Cond_Begin', r'O RLY\?'),
            ('Cond_End', r'OIC'),
            ('Win_Cond', r'YA RLY,?'),
            ('Else_Cond', r'MEBBE'),
            ('Fail_Cond', r'NO WAI'),
            ('Loop_Break', r'GTFO'),
            ('Loop_Begin', r'IM IN YR'),
            ('Loop_End', r'IM OUTTA YR'),
            ('Increment_Keyword', r'UPPIN'),
            ('Decrement_Keyword', r'NERFIN'),
            ('Stop_Win', r'TIL'),
            ('Stop_Fail', r'WILE'),
            ('Function_Begin', r'HOW IZ I'),
            ('Function_End', r'IF U SAY SO'),
            ('Return_Value', r'FOUND YR'),
            ('Identifier', r'[a-zA-Z]\w*'),     # IDENTIFIERS
            ('Float_Constant', r'\d(\d)*\.\d(\d)*'),   # FLOAT
            ('Integer_Constant', r'\d(\d)*,?'),          # INT
            ('Newline', r'\n'),         # NEW LINE
            ('Skip', r'[ \t]+'),        # SPACE and TABS
            ('Error', r'.'),         # ANOTHER CHARACTER
        ]

		possible_tokens = '|'.join('(?P<%s>%s)' % x for x in tokens) 
			
		line_start = 0

		tokens = []

		multilineFlag = False #flag for multiline comments
		for m in re.finditer(possible_tokens, code):
			token_type = m.lastgroup
			token_lexeme = m.group(token_type)

			if token_type == 'Newline':  		#skips newline
				line_start = m.end()
				self.line_num += 1
			elif token_type == 'TLDRComment':	#ends ignored multiline comments
				multilineFlag = False
				continue
			elif token_type == 'OBTWComment':	#starts ignored multiline comments
				multilineFlag = True
				continue
			elif (token_type == 'Comment') or (multilineFlag == True): #skip comments
				if token_type == 'Newline':  	self.line_num += 1	#skips newline
				continue
			elif token_type == 'String': 		#separates string delimiter and literal
				token_lexeme = token_lexeme[1:-1:]
				tokens.append(Token('"', "String_Delimiter", self.line_num, col))
				tokens.append(Token(token_lexeme, "String_Literal", self.line_num, col))
				tokens.append(Token('"', "String_Delimiter", self.line_num, col))
			elif token_type == 'Skip':			#skips spaces
			    continue
			elif token_type == 'Error':			#shows error
				raise RuntimeError('%r unexpected on line %d' % (token_lexeme, self.line_num))
			else:								#when the token is not one of the special cases, add it to actual list of tokens
				col = m.start() - line_start
				tokens.append(Token(token_lexeme, token_type, self.line_num, col))

		return tokens    #returns list of tokens

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
https://www.thegeekstuff.com/2014/07/advanced-python-regex/
'''
''''
TO DO: Syntax Analyzer and updating symbol table.
'''

