'''
This program interprets the lolcode from the source code
'''
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import copy
import re

insideswitch = False
insideomg = False
default = False

class Token():
	def __init__(self, token, ttype, row, col, index):
		self.tok = token              #string of token
		self.type = ttype      		  #type of token
		self.row = row                #row/line where it is located
		self.col = col 
		self.index = index
		self.statementId = None
		self.block = []			  
		self.value = None             #no value yet

class Statement():
	def __init__(self, tokens, ttype, statementId):
		self.tokens = tokens              #list of Tokens in that statement
		self.type = ttype                 #type of the statement
		self.id = statementId 			  #index of the statement
		self.valTab = []			  	  #temporary storage of updated symbol Table of the statement
		self.passed = False 			  #toggles true pag nadaanan na

	def appendTok(self, tok):
		self.tokens.append(tok) 		  #appends to Statement's tokens list

class Semantic_Analyzer():
	def __init__(self, symbolTable, parseTree, interpreter):
		self.symbolTable = symbolTable			#symbol table constantly updated
		self.symbolTable[0] = Token("IT", "Identifier", None, None, None)		#make a identifier IT for temporary storage of values
		self.symbolTable[0].statementId = -1		#special statement id
		self.statements = parseTree 				#parse tree from syntax analyzer static
		self.output= []
		self.hold = False
		self.interpreter = interpreter
		self.currentSymbIndex = 0
		self.interpret()

	#removes current statement after meaning is derived
	def removeValues(self,stmnt):
		statementIndex = -1
		i = 0
		while (True):
			if self.symbolTable[i].tok == "KTHXBYE":
				break
			elif self.symbolTable[i].statementId == stmnt.id:
				if statementIndex == -1: statementIndex = i  #get the index of the first matched item in the symbolTable
				self.symbolTable.pop(i)						 #remove the Token in the list
			elif statementIndex != -1: break
			else: i += 1
		return statementIndex

	#get the value of the identifier
	def getIdentValue(self,stmnt, token): #variable is the variable to search
		for item in self.symbolTable:
			if item.tok == token.tok and item.type == "Identifier" : #and item.statementId <= stmnt.id:
				return item.value
		self.callError("ERROR: Uninitialized variable at line " + str(token.row))

	#first step loops all the statements from the parsetree
	def interpret(self):
		for statement in self.statements:
			if self.hold: break 			#don't iterate anymore if hold
			elif statement.passed == False and self.hold == False:
				statement.passed = True
				self.currentStatement = statement.id
				self.solve(statement)
				self.interpreter.update_symbolTable(self.symbolTable) #updates symbol table
		if self.symbolTable[-1].tok == "KTHXBYE" and self.hold == False: self.symbolTable.pop(-1)
		self.interpreter.update_symbolTable(self.symbolTable)

	#redirects to respective statements
	def solve(self, stmnt):
		if stmnt.type == "<PRINT>":
			self.print(stmnt)			
		elif stmnt.type == "<DECLARATION>":
			self.declaration(stmnt)
		elif stmnt.type == "<ASSIGNMENT>":
			self.assignment(stmnt)
		elif stmnt.type == "<BOOLEAN>":
			self.symbolTable[0].value = self.boolean(stmnt)
		elif stmnt.type == "<COMPARISON>":
			self.symbolTable[0].value = self.comparison(stmnt)
		elif stmnt.type == "<ARITHMETIC>":
			self.symbolTable[0].value = self.arithmetic(stmnt)
		elif stmnt.type == "<INPUT>":
			self.input(stmnt)
		elif stmnt.type == "<START IF-ELSE>":
			self.ifelse(stmnt)
		elif stmnt.type == "<START SWITCH>":
			self.switch(stmnt)

	def ifelse(self, stmnt):
		#determine which block will the statement go
		if self.symbolTable[0].value == True:				#if IT is true <YA RLY>
			ifindex = stmnt.tokens[0].block[0]				#get the statement id of if block
			self.statements[ifindex].passed = True
			for i in self.statements[ifindex].tokens[0].block:   #for each statementid referenced in the if block
				self.statements[i].passed = True    			 #statement has been passed
				self.solve(self.statements[i])
		elif self.symbolTable[0].value == False:				#if IT is false <NO WAI>
			ifindex = stmnt.tokens[0].block[1]				    #get the statement id of else block
			self.statements[ifindex].passed = True
			for i in self.statements[ifindex].tokens[0].block:   #for each statementid referenced in the if block
				self.statements[i].passed = True    			 #statement has been passed
				self.solve(self.statements[i])
			
		for i in range(stmnt.id,stmnt.tokens[0].block[2]+1): #removes all statements in <IF-ELSE>
			self.statements[i].passed = True 
			self.removeValues(self.statements[i])

	def switch(self, stmnt):
		for i in stmnt.tokens[0].block:				#for each statement id in WTF?.block
			if self.statements[i].tokens[0].tok == "OMG":
				if self.statements[i].tokens[1].type == "Integer_Constant" or self.statements[i].tokens[1].type == "Float_Constant" or self.statements[i].tokens[1].type == "TROOF":
					if str(self.symbolTable[0].value) == self.statements[i].tokens[1].tok or (str(self.symbolTable[0].value) == "True" and self.statements[i].tokens[1].tok == "WIN") or (str(self.symbolTable[0].value) == "False" and self.statements[i].tokens[1].tok == "FAIL"):
						for i in self.statements[i].tokens[0].block:   #for each statementid referenced in the if block
							self.statements[i].passed = True    			 #statement has been passed
							self.solve(self.statements[i])
						break
				elif self.statements[i].tokens[1].type == "String_Delimiter":
					if self.symbolTable[0].type == "String_Literal" and self.symbolTable[0].value == self.statements[i].tokens[2].tok: #if the string literal matches the value
						for i in self.statements[i].tokens[0].block:   #for each statementid referenced in the if block
							self.statements[i].passed = True    			 #statement has been passed
							self.solve(self.statements[i])
						break
				else: self.callError("Invalid case literal on line "+ self.statements[i].tokens[1].row)
			elif self.statements[i].tokens[0].tok == "OMGWTF": #Default case
				for i in self.statements[i].tokens[0].block:  		
					self.statements[i].passed = True    			 
					self.solve(self.statements[i])
				break
		
		#removes all statements in <SWITCH CASE>
		for i in range(stmnt.id,stmnt.tokens[0].block[-1]+1):
			self.statements[i].passed = True 
			self.removeValues(self.statements[i])

	def print(self, stmnt):
		stok = stmnt.tokens
		printvalue = ""
		for i in range(1, len(stmnt.tokens)):
			if stok[i].type == "String_Literal":	#expected combination ["VISIBLE",'"', StringLiteralToken, '"']
				printvalue += stok[i].tok     		#concatenate if string literal
			elif stok[i].type == "Integer_Constant":		
				printvalue += stok[i].tok
			elif stok[i].type == "Float_Constant":  	
				printvalue += stok[i].tok
			elif stok[i].tok == "WIN" or stok[i].tok == "FAIL": #WIN FAIL literal
				printvalue += stok[i].tok
			elif stok[i].type == "Identifier":
				varval = self.getIdentValue(stmnt, stok[i])
				if str(varval) == "True": printvalue += "WIN"
				elif str(varval) == "False" : printvalue += "FAIL"
				elif varval == None and self.hold == False: self.callError("ERROR: Unbounded variable at line " + str(stok[i].row))
				else: printvalue += str(varval)
			elif stok[i].type == "Arithmetic_Op":		#Arithmetic expression case
				stmnt.tokens = self.clearTokExp(stok,1)
				printvalue += str(self.arithmetic(stmnt))
				break
			elif stok[i].type == "Boolean_Op":
				stmnt.tokens = self.clearTokExp(stok,1)
				value = self.boolean(stmnt)
				if value == True: printvalue += "WIN"
				elif value == False: printvalue += "FAIL"
				else: self.callError("ERROR: Invalid boolean expression at line " + str(stok[i].row))
				break
			elif stok[i].type == "Comparison_Op":
				stmnt.tokens = self.clearTokExp(stok,1)
				value = self.comparison(stmnt)
				if value == True: printvalue += "WIN"
				elif value == False: printvalue += "FAIL"
				else: self.callError("ERROR: Invalid comparison expression at line " + str(stok[i].row))
				break
			elif stok[i].type == "Output_Keyword" or stok[i].type == "String_Delimiter":
				continue
			else: callError("ERROR: Invalid printing on line "+ str(stok[0].row))
		if self.hold == False:
			self.output.append(printvalue)
			self.interpreter.update_exec(self.output, "<PRINT>")
			self.removeValues(stmnt)

	def declaration(self,stmnt):
		stok = stmnt.tokens 				#only to shorten name
		for i in range(1, len(stok)):
			if stok[i-1].type == "Variable_Assignment": 	#if previous token is assignment / ITZ
				if stok[i].type == "Integer_Constant":		#typecasting to integer then put to value Table  
					stmnt.valTab[0].value = int(stok[i].tok)
				elif stok[i].type == "Float_Constant":  	#typecasting to integer then put to value Table
					stmnt.valTab[0].value = float(stok[i].tok)
				elif stok[i].type == "String_Delimiter":    #puts the string literal to value table
					stmnt.valTab[0].value = stok[i+1].tok
				elif stok[i].tok == "WIN":
					stmnt.valTab[0].value = True
				elif stok[i].tok == "FAIL":
					stmnt.valTab[0].value = False
				elif stok[i].type == "Identifier":			#if ITZ variable
					stmnt.valTab[0].value = self.getIdentValue(stmnt, stok[i])
				elif stok[i].type == "Arithmetic_Op":		#Arithmetic expression case
					stmnt.tokens = self.clearTokExp(stok,3)
					stmnt.valTab[0].value = self.arithmetic(stmnt)
				elif stok[i].type == "Boolean_Op":
					stmnt.tokens = self.clearTokExp(stok,3)
					stmnt.valTab[0].value = self.boolean(stmnt)
				elif stok[i].type == "Comparison_Op":
					stmnt.tokens = self.clearTokExp(stok,3)
					stmnt.valTab[0].value = self.comparison(stmnt)
				else: self.callError("ERROR: Invalid assignment to variable")
				break
			elif stok[i].type == "Identifier":
				stmnt.valTab.append(stok[i])			    #append identifier to valueTable
		statementIndex = self.removeValues(stmnt) #remove the items in with the same statement id
		#insert values from value table starting with the index of the first removed
		self.currentSymbIndex += 1
		if statementIndex == -1: statementIndex = self.currentSymbIndex
		for token in stmnt.valTab:
			self.symbolTable.insert(statementIndex, token)
			statementIndex += 1

	def assignment(self, stmnt):
		stok = stmnt.tokens 				#only to shorten name
		k = -1
		if stok[0].type == "Identifier":
			for item in self.symbolTable:
				if item.tok == stok[0].tok and item.type == "Identifier" and item.statementId <= stmnt.id:	#if the token is an identifier that has been passed
					k =1
					if stok[2].type == "Integer_Constant":		#integer literal case
						item.value = int(stok[2].tok)
					elif stok[2].type == "Float_Constant":  	    #float literal case
						item.value = float(stok[2].tok)
					elif stok[2].type == "String_Delimiter":      #string literal case
						item.value = stok[3].tok
					elif stok[2].tok == "WIN":
						item.value = True
					elif stok[2].tok == "FAIL":
						item.value = False
					elif stok[2].type == "Identifier":			#if variable R variable
						item.value = self.getIdentValue(stmnt, stok[2])
					elif stok[2].type == "Arithmetic_Op":		
						stmnt.tokens = self.clearTokExp(stok,2)
						item.value = self.arithmetic(stmnt)
					elif stok[2].type == "Boolean_Op":
						stmnt.tokens = self.clearTokExp(stok,2)
						item.value = self.boolean(stmnt)
					elif stok[2].type == "Comparison_Op":
						stmnt.tokens = self.clearTokExp(stok,2)
						item.value = self.comparison(stmnt)
					else: self.callError("ERROR: Invalid assignment to variable on line " + str(stok[0].row))
					break
			if k == -1: self.callError("ERROR: Identifier not yet assigned on line " + str(stok[0].row))
		else: self.callError("ERROR: Missing identifier for assignment operation on line " + str(stok[0].row))
		self.removeValues(stmnt)

	def clearTokExp(self,stok, n): #clears previous tokens to identify expressions for Declaration, Assignment and Print
		return stok[n:]

	def input(self, stmnt):
		stok = stmnt.tokens
		if len(stok) == 2 and stok[0].type == "Accept_Keyword" and stok[1].type == "Identifier":
			self.interpreter.update_exec(self.output, "<INPUT>")
			for item in self.symbolTable:
				if item.tok == stok[1].tok and item.type == "Identifier" and item.statementId <= stmnt.id:
					item.value = "<HOLD>" 	#item value is on hold until GIMMEH gives input
					self.hold = True        #further interpretation of statements are on hold
			self.removeValues(stmnt)
		else: self.callError("ERROR: Invalid input statement on line " + str(stok[0].row))

	def continueInput(self):		#continues the GIMMEH when input is received no longer on hold
		for item in self.symbolTable:
			if item.value == "<HOLD>":
				item.value = self.output[-1]
				self.hold = False 					#statements no longer on hold
				break
		self.interpret()

	def boolean(self,stmnt):
		stok = stmnt.tokens
		val = -1
		#store to identifier IT (always in index 0)
		if stok[0].tok == "BOTH OF" and len(stok) == 4: #AND
			val = self.getBool(stmnt,stok[1]) and self.getBool(stmnt,stok[3])		
		elif stok[0].tok == "EITHER OF" and len(stok) == 4: #OR
			val = self.getBool(stmnt,stok[1]) or self.getBool(stmnt,stok[3])	
		elif stok[0].tok == "WON OF" and len(stok) == 4: #XOR
			val = self.getBool(stmnt,stok[1]) ^ self.getBool(stmnt,stok[3])	
		if stok[0].tok == "NOT" and len(stok) == 2: #NOT
			val = not self.getBool(stmnt,stok[1])
		elif stok[0].tok == "ALL OF": 
			i = 1
			k = -1				#flag to determine if first bool block
			while (i < len(stok)):
				if stok[i].tok == "BOTH OF": #AND
					boolblock = self.getBool(stmnt,stok[i+1]) and self.getBool(stmnt,stok[i+3])
					i += 4
				elif stok[i].tok == "EITHER OF": #OR
					boolblock = self.getBool(stmnt,stok[i+1]) or self.getBool(stmnt,stok[i+3]) 	
					i += 4
				elif stok[i].tok == "WON OF": #XOR
					boolblock = self.getBool(stmnt,stok[i+1]) ^ self.getBool(stmnt,stok[i+3]) 	
					i += 4
				elif stok[i].tok == "NOT": #NOT
					boolblock = not self.getBool(stmnt,stok[i+1])
					i += 2
				elif stok[i].tok == "WIN": #NOT
					boolblock = True
					i += 1
				elif stok[i].tok == "FAIL": #NOT
					boolblock = False
					i += 1
				elif stok[i].tok == "AN":
					if k == -1: 
						self.symbolTable[0].value = boolblock
						k = 1
					else: self.symbolTable[0].value = self.symbolTable[0].value and boolblock
					i +=1
				elif stok[i].tok == "MKAY":
					if k == -1: 
						val = boolblock
						k = 1
					else: val = self.symbolTable[0].value and boolblock
					break
				else: self.callError("ERROR: INVALID BOOLEAN STATEMENT on line " + str(stok[0].row))
		elif stok[0].tok == "ANY OF":
			i = 1
			k = -1				#flag to determine if first bool block
			while (i < len(stok)):
				if stok[i].tok == "BOTH OF": #AND
					boolblock = self.getBool(stmnt,stok[i+1]) and self.getBool(stmnt,stok[i+3])
					i += 4
				elif stok[i].tok == "EITHER OF": #OR
					boolblock = self.getBool(stmnt,stok[i+1]) or self.getBool(stmnt,stok[i+3]) 	
					i += 4
				elif stok[i].tok == "WON OF": #XOR
					boolblock = self.getBool(stmnt,stok[i+1]) ^ self.getBool(stmnt,stok[i+3]) 	
					i += 4
				elif stok[i].tok == "NOT": #NOT
					boolblock = not self.getBool(stmnt,stok[i+1])
					i += 2
				elif stok[i].tok == "WIN": #NOT
					boolblock = True
					i += 1
				elif stok[i].tok == "FAIL": #NOT
					boolblock = False
					i += 1
				elif stok[i].tok == "AN":
					if k == -1: 
						self.symbolTable[0].value = boolblock
						k = 1
					else: self.symbolTable[0].value = self.symbolTable[0].value or boolblock
					i +=1
				elif stok[i].tok == "MKAY":
					if k == -1: 
						val = boolblock
						k = 1
					else: val = self.symbolTable[0].value or boolblock
					break
				else: self.callError("ERROR: INVALID BOOLEAN STATEMENT on line " + str(stok[0].row))
		elif len(stok) > 4: 
			val = self.compoundBool(stmnt, stok)
		#else: self.callError("ERROR: INVALID BOOLEAN STATEMENT on line " + str(stok[0].row))
		self.removeValues(stmnt)
		if val == True or val == False: return val  #return a value only if True or False and value
		else: self.callError("ERROR: INVALID BOOLEAN STATEMENT on line " + str(stok[0].row))

	def getBool(self,stmnt, token):
		if token.tok == "WIN": return True
		elif token.tok == "FAIL": return False
		elif token.type == "Identifier":
			val = self.getIdentValue(stmnt, token)
			if val == True or val == False: return val
			else: self.callError("ERROR: variable value not a TROOF on line " + str(token.row)) 
		else: self.callError("ERROR: not a TROOF on line " + str(token.row)) 

	def compoundBool(self,stmnt,stok):
		opstack = []
		for i in range(len(stok)-1,-1,-1):
			if stok[i].tok == "NOT" and len(opstack) != 0: #NOT
				x = opstack.pop()
				val = not x
				opstack.append(val)
			elif stok[i].type == "Boolean_Op" and len(opstack) != 0: #if token is Boolean operation and stack is not empty
				x = opstack.pop()
				y = opstack.pop()
				if stok[i].tok == "BOTH OF": #AND
					val = x and y
				elif stok[i].tok == "EITHER OF": #OR
					val = x or y 	
				elif stok[i].tok == "WON OF": #XOR
					val = x ^ y 	
				else: callError("ERROR: INVALID BOOLEAN OP on line " + str(stok[i].row))
				opstack.append(val)
			elif  stok[i].type == "TROOF":
				opstack.append(self.getBool(stmnt, stok[i])) #add integer operands
			elif stok[i].type == "Op_Sep" or stok[i].type == "END_Op": #if AN, ignore
				continue				   
			else:
				self.callError("Error: Invalid arithmetic expression on line" + str(stok[0].row))
				break
		return opstack.pop()

	def comparison(self, stmnt):
		stok = stmnt.tokens
		val = None
		if stok[0].tok == "BOTH SAEM" and len(stok) == 4: 				#if == 
			a, b = self.compare(stmnt, stok[1], stok[3])
			if a == False: val = False
			else: val = (a == b) #returns true or false
		elif stok[0].tok == "DIFFRINT" and len(stok) == 4:				#if != 
			a, b = self.compare(stmnt, stok[1], stok[3])
			if a == False: val = False
			else: val = (a != b)
		elif stok[0].tok == "BOTH SAEM" and stok[3].tok == "BIGGR OF":  # if >=
			if stok[1].tok == stok[4].tok:
				a, b = self.compare(stmnt, stok[4], stok[6])
				if a == False: val = False
				else: val = (a >= b)
			else: self.callError("ERROR: expected same value operand on line " + str(stok[4].row))
		elif stok[0].tok == "BOTH SAEM" and stok[3].tok == "SMALLR OF": # if <=
			if stok[1].tok == stok[4].tok:
				a, b = self.compare(stmnt, stok[4], stok[6])
				if a == False: val = False
				else: val = (a <= b)
			else: self.callError("ERROR: expected same value operand on line " + str(stok[4].row))
		elif stok[0].tok == "DIFFRINT" and stok[3].tok == "BIGGR OF":   # if >
			if stok[1].tok == stok[4].tok:
				a, b = self.compare(stmnt, stok[4], stok[6])
				if a == False: val = False
				else: val = (a > b)
			else: self.callError("ERROR: expected same value operand on line " + str(stok[4].row))
		elif stok[0].tok == "DIFFRINT" and stok[3].tok == "SMALLR OF":  # if <
			if stok[1].tok == stok[4].tok:
				a, b = self.compare(stmnt, stok[4], stok[6])
				if a == False: val = False
				else: val = (a < b)
			else: self.callError("ERROR: expected same value operand on line " + str(stok[4].row))
		else:
			val = self.compoundComparison(stmnt)

		#else:self.callError("ERROR: Invalid comparison operator at line " + str(stok[0].row)) #mangyayari lang to if may mali sa syntax
		self.removeValues(stmnt)
		return val

	def compoundComparison(self,stmnt):
		stok = stmnt.tokens
		opstack = []
		for i in range(len(stok)-1,-1,-1):
			if stok[i].type == "Comparison_Op" and len(opstack) != 0: #if token is Arithmetic operation and stack is not empty
				x = opstack.pop()
				y = opstack.pop()
				if stok[i].tok == "BOTH SAEM": val = (x == y)
				elif stok[i].tok == "DIFFRINT": val = (x != y)
				opstack.append(val)
			elif stok[i].type == "Arithmetic_Op" and len(opstack) != 0: #if token is Arithmetic operation and stack is not empty
				x = opstack.pop()
				y = opstack.pop()
				opstack.append(self.basicExp(x,y,stok[i].tok))
			elif  stok[i].type == "Identifier":
				opstack.append(self.getIdentValue(stmnt, stok[i])) 
			elif  stok[i].type == "Integer_Constant":
				opstack.append(int(stok[i].tok)) #add integer operands
			elif stok[i].type == "Float_Constant":
				opstack.append(float(stok[i].tok)) #add float operands
			elif stok[i].type == "Op_Sep" or stok[i].type == "END_Op": #if AN, ignore
				continue				   
			else:
				self.callError("Error: Invalid comparison expression on line" + str(stok[0].row))
				break
		return opstack.pop()

	def compare(self,stmnt, x,y):
		#Numbr typecast to Numbar
		if x.type == "Identifier" and y.type == "Identifier":
			a = self.getIdentValue(stmnt, x)
			b = self.getIdentValue(stmnt, y)
			print(" " + str(a) + " " + str(y.tok))
		elif x.type == "Identifier" and (y.type == "Integer_Constant" or y.type == "Integer_Constant"): 
			a = self.getIdentValue(stmnt, x) 
			b = float(y.tok)
		elif (x.type == "Integer_Constant" or x.type == "Float_Constant") and y.type == "Identifier": 
			a = float(x.tok)
			b = self.getIdentValue(stmnt, y)
		elif (x.type == "Integer_Constant" or x.type == "Float_Constant") and (y.type == "Integer_Constant" or y.type == "Float_Constant"):
			a = float(x.tok)
			b = float(y.tok)
		else: self.callError("ERROR: Invalid operand on line " + str(x.row))

		 #check if a and b are NUMBARs #if one is NUMBR typecaset to float
		if isinstance(a, float) and isinstance(b,float): return a, b
		elif isinstance(a, int) and isinstance(b,float): return float(a), b
		elif isinstance(a, float) and isinstance(b,int): return a, float(b)
		elif isinstance(a, int) and isinstance(b,int): return float(a), float(b)
		else: return False, False #no typecasting direct to FAIL #returns left and right value (a,b) of comparison depending on type of compared token

	def arithmetic(self, stmnt):
		stok = stmnt.tokens
		if len(stok) == 4: #if basic expression
			a, b = self.checktype(stmnt, stok[1],stok[3]) 
			val = self.basicExp(a,b,stok[0].tok)
		elif len(stok) == 6 and (stok[1].type == "Integer_Constant" or stok[1].type == "Float_Constant") and stok[4].type == "String_Literal":
			a, b = self.checktype(stmnt, stok[1],stok[4])
			val = self.basicExp(a,b,stok[0].tok)
		elif len(stok) == 6 and stok[2].type == "String_Literal" and (stok[5].type == "Integer_Constant" or stok[5].type == "Float_Constant"):
			a, b = self.checktype(stmnt, stok[2],stok[5])
			val = self.basicExp(a,b,stok[0].tok)
		elif len(stok) == 8 and stok[2].type == "String_Literal" and stok[6].type == "String_Literal":
			a, b = self.checktype(stmnt, stok[2],stok[6])
			val = self.basicExp(a,b,stok[0].tok)
		else: #compound expressions
			val = self.compoundArithmetic(stmnt, stok)
		self.removeValues(stmnt)
		return val

	def checktype(self, stmnt, x,y):
		if x.type == "Identifier" and y.type == "Identifier": 
			a = self.getIdentValue(stmnt, x)
			b = self.getIdentValue(stmnt, y)
		elif x.type == "Identifier" and y.type == "Integer_Constant": 
			a = self.getIdentValue(stmnt, x) 
			b = int(y.tok)
		elif x.type == "Identifier" and y.type == "Float_Constant": 
			a = self.getIdentValue(stmnt, x) 
			b = float(y.tok)
		elif x.type == "Integer_Constant" and y.type == "Identifier": 
			a = int(x.tok)
			b = self.getIdentValue(stmnt, y)
		elif x.type == "Float_Constant" and y.type == "Identifier": 
			a = float(x.tok)
			b = self.getIdentValue(stmnt, y)
		elif x.type == "String_Literal" or y.type == "String_Literal":
				#cases where there are at least one string literal to typecast
				if x.type == "String_Literal" and y.type == "String_Literal":
					if self.isFloat(x.tok):
						a = float(x.tok)
						if self.isFloat(y.tok):
							b = float(y.tok)
						elif self.isInt(y.tok):
							b = int(y.tok)
						else: self.callError("ERROR: STRING LITERAL CANNOT BE TYPECASTED ON LINE " + str(y.row))
					elif self.isInt(x.tok):
						a = int(x.tok)
						if self.isFloat(y.tok):
							b = float(y.tok)
						elif self.isInt(y.tok):
							b = int(y.tok)
						else: self.callError("ERROR: STRING LITERAL CANNOT BE TYPECASTED ON LINE " + str(y.row))
					else: self.callError("ERROR: STRING LITERAL CANNOT BE TYPECASTED ON LINE " + str(x.row))
				elif x.type == "String_Literal" and self.isInt(x.tok):
					a = int(x.tok)
					if y.type == "Integer_Constant": b = int(y.tok)
					elif y.type == "Float_Constant": b = float(y.tok)
					elif y.type == "Identifier": b = self.getIdentValue(stmnt, y)
					else: self.callError("ERROR: Invalid operand on line " + str(y.row))
				elif x.type == "String_Literal" and self.isFloat(x.tok):
					a = float(x.tok)
					if y.type == "Integer_Constant": b = int(y.tok)
					elif y.type == "Float_Constant": b = float(y.tok)
					elif y.type == "Identifier": b = self.getIdentValue(stmnt, y)
					else: self.callError("ERROR: Invalid operand on line " + str(y.row))
				elif y.type == "String_Literal" and self.isInt(y.tok):
					b = int(y.tok)
					if x.type == "Integer_Constant": a = int(x.tok)
					elif x.type == "Float_Constant": a = float(x.tok)
					elif x.type == "Identifier": a = self.getIdentValue(stmnt, x)
					else: self.callError("ERROR: Invalid operand on line " + str(x.row))
				elif y.type == "String_Literal" and self.isFloat(y.tok): 
					b = float(y.tok)
					if x.type == "Integer_Constant": a = int(x.tok)
					elif x.type == "Float_Constant": a = float(x.tok)
					elif x.type == "Identifier": a = self.getIdentValue(stmnt, x)
					else: self.callError("ERROR: Invalid operand on line " + str(x.row))
				else: self.callError("ERROR: Invalid operand on line " + str(x.row))
		else:
			if x.type == "Integer_Constant": a = int(x.tok)
			elif x.type == "Float_Constant": a = float(x.tok)
			else: self.callError("ERROR: Invalid operand on line " + str(x.row))
			if y.type == "Integer_Constant": b = int(y.tok)
			elif y.type == "Float_Constant": b = float(y.tok)
			else: self.callError("ERROR: Invalid operand on line " + str(y.row))
		return a,b
				
	def basicExp(self, a, b, operator):
		if operator == "SUM OF": val = a + b
		elif operator == "DIFF OF": val = a - b
		elif operator == "PRODUKT OF": val = a * b
		elif operator == "QUOSHUNT OF": val = a/b
		elif operator == "MOD OF": val = a%b
		elif operator == "BIGGR OF": val = max(a,b)
		elif operator == "SMALLR OF": val = min(a,b)
		else: self.callError("ERROR: Invalid arithmetic operator on line " + str(x.row))
		return val

	def compoundArithmetic(self,stmnt,stok): # prefix evaluation using stack
		opstack = []
		for i in range(len(stok)-1,-1,-1):
			if stok[i].type == "Arithmetic_Op" and len(opstack) != 0: #if token is Arithmetic operation and stack is not empty
				x = opstack.pop()
				y = opstack.pop()
				opstack.append(self.basicExp(x,y,stok[i].tok))
			elif  stok[i].type == "Integer_Constant" or (stok[i].type == "String_Literal" and self.isInt(stok[i].tok)):
				opstack.append(int(stok[i].tok)) #add integer operands
			elif stok[i].type == "Float_Constant" or (stok[i].type == "String_Literal" and self.isFloat(stok[i].tok)):
				opstack.append(float(stok[i].tok)) #add float operands
			elif  stok[i].type == "Identifier":
				opstack.append(self.getIdentValue(stmnt, stok[i])) 
			elif stok[i].type == "Op_Sep" or stok[i].type == "END_Op": #if AN, ignore
				continue				   
			else:
				self.callError("Error: Invalid arithmetic expression on line" + str(stok[0].row))
				break
		return opstack.pop()
			
	def isFloat(self, a): #check if string is float
		try:
			float(a)
			return True
		except ValueError: return False

	def isInt(self, a): #check if string is int
		try:
			int(a)
			return True
		except ValueError: return False

	#Error calls
	def callError(self, text):
		self.output.append(text)
		self.interpreter.update_exec(self.output, "<PRINT>")
		self.hold = True
		self.interpret()			#end interpretation

class Syntax_Analyzer():
	def __init__(self, tokens, interpreter):
		self.tokens = tokens         	#tokens list
		self.tokindex = 0 	            #current token index
		self.parsetree = None			#[STATEMENT1, STATEMENT2, STATEMENT3] will look like this
		self.statementId = -1			#index of statement currently added - this value will be updated to self.tokens. start to -1 because it will immediately be incremented to 1 under statement thus will actually start at value 0
		self.interpreter = interpreter
		self.error = False 				#toggles if there is an error
		self.program()

	#forward to next index in self.tokens 
	def next(self):
		if self.parsetree != None : 				 	#if parse tree has been initialize the succeeding tokens will have a statement id that will match the parse tree
			self.tokens[self.tokindex].statementId = self.statementId #check if tamang index ang inuupdate
		self.tokindex = self.tokindex + 1

	#update current statementid
	def nextstmnt(self):
		self.statementId = self.statementId + 1 

	#checking contents of parse tree
	def viewparse(self):
		for statement in self.parsetree:
			print("Statement: " + str(statement.type) + " " + str(statement.id))
			for token in statement.tokens:  #print token in tokens
				print("\t " + str(token.tok) + " " + str(token.statementId))

	#root
	def program(self): # <program>	::=	HAI <linebreak> <statement> <linebreak> KTHXBYE
		if self.tokens[0].tok == "HAI":
			if self.tokens[1].type == "Float_Constant":
				self.next()						 #move to next token
			if self.tokens[-1].tok == "KTHXBYE": #something like this though di ko sure kung tama na pagsabayin o line per line dapat
				self.next() 					 #move to next token
				self.parsetree = []				 #initialize parse tree tells that a program has started
				self.statement()
			else: self.callError("SYNTAX ERROR: KTHXBYE expected on line " + str(self.tokens[-1].row)) #di ko sure kunt tama icheck agad kthxbye baka skip muna ito
		else: self.callError("SYNTAX ERROR: HAI expected on line " + str(self.tokens[0].row))

	def statement(self): 
		global insideswitch
		if self.tokens[self.tokindex].type == "Output_Keyword": #for VISIBLE/ <print> case
			self.nextstmnt()
			self.parsetree.append(Statement([self.tokens[self.tokindex]], "<PRINT>", self.statementId))
			self.next()						#all self.next() starting this statement fxn will have a statement id value
			self.print()
		elif self.tokens[self.tokindex].type == "Accept_Keyword": #for GIMMEH/ <input> case
			self.nextstmnt()
			self.parsetree.append(Statement([self.tokens[self.tokindex]], "<INPUT>", self.statementId))
			self.next()
			self.input()
		elif self.tokens[self.tokindex].type == "Variable_Declaration": #for I HAS A/ <DECLARATION> case
			self.nextstmnt()
			self.parsetree.append(Statement([self.tokens[self.tokindex]], "<DECLARATION>", self.statementId))
			self.next()
			self.variable()
		elif self.tokens[self.tokindex].type == "Boolean_Op": #for <boolean> case
			self.nextstmnt()
			self.parsetree.append(Statement([self.tokens[self.tokindex]], "<BOOLEAN>", self.statementId))
			self.bool()
		elif self.tokens[self.tokindex].type == "Arithmetic_Op": #for <arithmetic> case
			self.nextstmnt()
			self.parsetree.append(Statement([self.tokens[self.tokindex]], "<ARITHMETIC>", self.statementId))
			self.next()
			self.arithmetic()
		elif self.tokens[self.tokindex].type == "Comparison_Op": #for <comparison> case
			self.nextstmnt()
			self.parsetree.append(Statement([self.tokens[self.tokindex]], "<COMPARISON>", self.statementId))
			self.next()
			self.comparison()
		elif self.tokens[self.tokindex].type == "Identifier": #for <assignment> case
			self.nextstmnt()
			self.next()
			if self.tokens[self.tokindex].type == "Assignment": #for <assignment> case
				self.parsetree.append(Statement([self.tokens[self.tokindex-1]], "<ASSIGNMENT>", self.statementId))
				self.next()
				self.assignment()
			else: self.callError("SYNTAX ERROR: Assignment operator expected on line " + str(self.tokens[self.tokindex].row))
		elif self.tokens[self.tokindex].type == "Cond_Begin": #for <if-else> case
			codeblock = 0
			orly_row = self.tokens[self.tokindex].row
			orly_block = self.tokens[self.tokindex].block
			self.nextstmnt()
			self.parsetree.append(Statement([self.tokens[self.tokindex]], "<START IF-ELSE>", self.statementId))
			self.next()
			if self.tokens[self.tokindex].row != orly_row:
				if self.tokens[self.tokindex].type == "Win_Cond": #for <if-else> case YA RLY BLOCK
					yarly_row = self.tokens[self.tokindex].row
					yarly_block = self.tokens[self.tokindex].block
					self.nextstmnt()
					orly_block.append(self.statementId)    #adds the statement id of yarly to orly for reference
					self.parsetree.append(Statement([self.tokens[self.tokindex]], "<IF>", self.statementId))
					yarly_stmnt = self.statementId
					self.next()
					if self.tokens[self.tokindex].row != yarly_row:
						while self.tokens[self.tokindex].type != "Fail_Cond": #while not equal to NO WAI
							self.statement()
						#appends if block for tracking which statements under this block
						for i in range(self.parsetree[-1].id,yarly_stmnt,-1):
							yarly_block.append(i)
						yarly_block.reverse()
						if self.tokens[self.tokindex].type == "Fail_Cond":
							self.nextstmnt()
							orly_block.append(self.statementId)
							nowai_row = self.tokens[self.tokindex].row
							nowai_block = self.tokens[self.tokindex].block
							self.parsetree.append(Statement([self.tokens[self.tokindex]], "<ELSE>", self.statementId))
							nowai_stmnt = self.statementId
							self.next()
							if self.tokens[self.tokindex].row != nowai_row:
								while self.tokens[self.tokindex].type != "Cond_End":
									self.statement()
								#appends or block for tracking which statements under this block
								for i in range(self.parsetree[-1].id,nowai_stmnt,-1):
									nowai_block.append(i)
								nowai_block.reverse()
								if self.tokens[self.tokindex].type == "Cond_End":
									oic_row = self.tokens[self.tokindex].row
									self.nextstmnt()
									orly_block.append(self.statementId)
									self.parsetree.append(Statement([self.tokens[self.tokindex]], "<END IF-ELSE>", self.statementId))
									self.next()
									if self.tokens[self.tokindex].row != oic_row:
										self.statement()
									else: self.callError("SYNTAX ERROR: OIC must be alone on line " + str(self.tokens[self.tokindex].row))		
								else: self.callError("SYNTAX ERROR: OIC expected on line " + str(self.tokens[self.tokindex].row))
							else: self.callError("SYNTAX ERROR: NO WAI must be alone on line " + str(self.tokens[self.tokindex].row))		
						else: self.callError("SYNTAX ERROR: NO WAI expected on line " + str(self.tokens[self.tokindex].row))
					else: self.callError("SYNTAX ERROR: YA RLY must be alone on line " + str(self.tokens[self.tokindex].row))
				else: self.callError("SYNTAX ERROR: YA RLY expected on line " + str(self.tokens[self.tokindex].row))
			else: self.callError("SYNTAX ERROR: O RLY? must be alone on line " + str(self.tokens[self.tokindex].row))
		elif self.tokens[self.tokindex].type == "Start_Switch": #for <switch> case
			insideswitch = True
			insideomg = False
			default = False
			nobreak = 0
			wtf_row = self.tokens[self.tokindex].row
			wtf_block = self.tokens[self.tokindex].block
			self.nextstmnt()
			self.parsetree.append(Statement([self.tokens[self.tokindex]], "<START SWITCH>", self.statementId))
			self.next()
			if self.tokens[self.tokindex].row != wtf_row:
				nobreakcase = []
				nobreakcase1 = []
				nobreakcase2 = []
				numofomg = 0
				default = False
				while self.tokens[self.tokindex].type != "Cond_End":
					
					if self.tokens[self.tokindex].type == "Default_Case":
						default = False
						if self.tokens[self.tokindex-1].type != "Break":
							if nobreak <= 0:
								nobreak = 0
								nobreakcase = omg_block

							omg_block.append(self.statementId)

							if nobreak == 1:
								nobreakcase.append(self.statementId)
								nobreakcase1 = nobreakcase
							elif nobreak == 2:
								nobreakcase.append(self.statementId)
								nobreakcase1.append(self.statementId)
								nobreakcase2 = nobreakcase1
								nobreakcase1 = nobreakcase
							nobreakcase = omg_block	
							# nobreakcase.append(self.statementId)
							# nobreakcase1.append(self.statementId)		
							nobreak += 1
						if self.tokens[self.tokindex-1].type == "Break":
							
							if nobreak > 0:
								nobreakcase.append(self.statementId-1)
								nobreakcase1.append(self.statementId-1)
								nobreakcase2.append(self.statementId-1)
							# else:
							omg_block.append(self.statementId-1)
							nobreak -= 1
							if nobreak <= 0:
								nobreakcase = omg_block
								nobreak = 0
							if nobreak == 1:
								nobreakcase1 = nobreakcase
							elif nobreak == 2:
								nobreakcase2 = nobreakcase1
								nobreakcase1 = nobreakcase
							
						omg_row = self.tokens[self.tokindex].row
						omg_block = self.tokens[self.tokindex].block
						default = False
						self.nextstmnt()
						self.next()
						self.parsetree.append(Statement([self.tokens[self.tokindex-1]], "<DEFAULT CASE>", self.statementId))
						wtf_block.append(self.statementId)
						if self.tokens[self.tokindex].row != omg_row:
							self.statement()
						else: print("SYNTAX ERROR: Expression must be on a separate line on line " + str(self.tokens[self.tokindex].row))	
						# else: print("SYNTAX ERROR: Literal expected on line " + str(self.tokens[self.tokindex].row))	
					else:
						if numofomg > 0:
							if self.tokens[self.tokindex-1].type != "Break" and self.tokens[self.tokindex].type == "Switch_Case":
								if nobreak <= 0:
									nobreak = 0
									nobreakcase = omg_block

								omg_block.append(self.statementId)
								if nobreak == 1:
									nobreakcase.append(self.statementId)
									nobreakcase1 = nobreakcase
								elif nobreak == 2:
									nobreakcase.append(self.statementId)
									nobreakcase1.append(self.statementId)
									nobreakcase2 = nobreakcase1
									nobreakcase1 = nobreakcase
								# nobreakcase = omg_block			
								nobreak += 1

							if self.tokens[self.tokindex-1].type == "Break" and self.tokens[self.tokindex].type == "Switch_Case":
								if nobreak > 0:
									nobreakcase.append(self.statementId-1)
									nobreakcase1.append(self.statementId-1)
									nobreakcase2.append(self.statementId-1)
								# else:
								omg_block.append(self.statementId-1)
								nobreak -= 1
								if nobreak <= 0:
									nobreak = 0
									nobreakcase = omg_block

								if nobreak == 1:
									nobreakcase1 = nobreakcase
								elif nobreak == 2:
									nobreakcase2 = nobreakcase1
									nobreakcase1 = nobreakcase
								# nobreakcase = omg_block


							

						if self.tokens[self.tokindex].type == "Break":
							self.nextstmnt()
							self.next()
							self.parsetree.append(Statement([self.tokens[self.tokindex-1]], "<BREAK>", self.statementId))
						elif self.tokens[self.tokindex].type == "Switch_Case":

							omg_row = self.tokens[self.tokindex].row
							omg_block = self.tokens[self.tokindex].block
							numofomg +=1							
							self.nextstmnt()
							self.next()
							
							if self.tokens[self.tokindex].row != omg_row:
								print("SYNTAX ERROR: Literal expected on line " + str(self.tokens[self.tokindex].row))	
							elif self.tokens[self.tokindex].type == "Identifier" or self.tokens[self.tokindex].type == "Float_Constant" or self.tokens[self.tokindex].type == "Integer_Constant" or self.tokens[self.tokindex].type == "TROOF":
								self.parsetree.append(Statement([self.tokens[self.tokindex-1]], "<SWITCH CASE>", self.statementId))
								wtf_block.append(self.statementId)
								self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
								print(str(self.tokindex) + " ")
								self.next()
								if self.tokens[self.tokindex].row != omg_row:
									self.statement()
									
								else: print("SYNTAX ERROR: Expression must be on a separate line on line " + str(self.tokens[self.tokindex].row))	
							else: print("SYNTAX ERROR: Literal expected on line " + str(self.tokens[self.tokindex].row))		
						elif self.tokens[self.tokindex-1].type != "Break" and self.tokens[self.tokindex-1].type != "Start_Switch":
							if nobreak > 0 and default == False:
								nobreakcase.append(self.statementId)
								nobreakcase1.append(self.statementId)
								nobreakcase2.append(self.statementId)
							
							omg_block.append(self.statementId)
							self.statement()
							# else: print("SYNTAX ERROR: GTFO expected on line " + str(self.tokens[self.tokindex].row))	
						else: print("SYNTAX ERROR: OMG expected on line " + str(self.tokens[self.tokindex].row))
				if default ==  True:
					omg_block.append(self.statementId)
				# if nobreak <= 0:
				# 			nobreak = 0
				# 			nobreakcase = omg_block

				# if nobreak == 1:
				# 	# nobreakcase.append(self.statementId)
				# 	nobreakcase1 = nobreakcase
				# elif nobreak == 2:
				# 	# nobreakcase.append(self.statementId)
				# 	# nobreakcase1.append(self.statementId)
				# 	nobreakcase2 = nobreakcase1
				# 	nobreakcase1 = nobreakcase
				else:
					if self.tokens[self.tokindex-1].type == "Break":
						omg_block.append(self.statementId-1)
						nobreakcase.append(self.statementId)
						nobreakcase1.append(self.statementId)
						nobreakcase2.append(self.statementId)
					else:
						omg_block.append(self.statementId)
						nobreakcase.append(self.statementId)
						nobreakcase1.append(self.statementId)
						nobreakcase2.append(self.statementId)
				self.nextstmnt()
				self.parsetree.append(Statement([self.tokens[self.tokindex]], "<END SWITCH>", self.statementId))
				wtf_block.append(self.statementId)
				self.next()
				insideswitch = False
				self.statement()
			else: print("SYNTAX ERROR: WTF? must be alone on line " + str(self.tokens[self.tokindex].row))
		
	def print(self):
		insideifelse = False
		if self.tokens[self.tokindex-1].type == "Win_Cond" or self.tokens[self.tokindex-1].type == "Fail_Cond" or insideswitch == True:
			insideifelse = True
		line_num = self.tokens[self.tokindex].row
		while self.tokens[self.tokindex].row == line_num:	
			if self.tokens[self.tokindex].type == "String_Delimiter": #for string literal case #Statement.tokens will look like this: ["VISIBLE",'"', StringLiteralToken, '"'] 
				self.parsetree[-1].appendTok(self.tokens[self.tokindex]) 		#calls the statement method appendTok and adds tokens to the Tokens list of the most recent statement
				self.next()
				self.next() #move 2 indeces
				if self.tokens[self.tokindex].type == "String_Delimiter":
					self.parsetree[-1].appendTok(self.tokens[self.tokindex-1])    #adds the end string delimiter
					self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds string literal
					self.next()							   #back to self.statement to check if there are more statements /recursively call it again
				else: self.callError("SYNTAX ERROR: String Delimiter expected on line " + str(self.tokens[self.tokindex].row))
			elif self.tokens[self.tokindex].type == "Integer_Constant" or self.tokens[self.tokindex].type == "Float_Constant" or self.tokens[self.tokindex].type == "Identifier":
					self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
					self.next()
			elif self.tokens[self.tokindex].type == "TROOF":		
				self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
				self.next()
				if insideifelse == False:
					self.statement()
			elif self.tokens[self.tokindex].type == "Arithmetic_Op":
				self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
				self.next()
				self.arithmetic()
			elif self.tokens[self.tokindex].type == "Boolean_Op":
				self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
				self.bool()
			elif self.tokens[self.tokindex].type == "Comparison_Op":
				self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
				self.next()
				self.comparison()	

		if insideifelse == False:
			self.statement()

	def input(self):
		insideifelse = False
		if self.tokens[self.tokindex-1].type == "Win_Cond" or self.tokens[self.tokindex-1].type == "Fail_Cond" or insideswitch == True:
			insideifelse = True
		if self.tokens[self.tokindex].type == "Identifier":		#if type is an identifier
			self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
			self.next()
			if insideifelse == False:
				self.statement()
		else: self.callError("SYNTAX ERROR: Identifier expected on line: " + str(self.tokens[self.tokindex].row))

	def variable(self):
		insideifelse = False
		if self.tokens[self.tokindex-1].type == "Win_Cond" or self.tokens[self.tokindex-1].type == "Fail_Cond" or insideswitch == True:
			insideifelse = True
		if self.tokens[self.tokindex].type == "Identifier":		#if type is an identifier
			self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
			self.next()
			if self.tokens[self.tokindex].type == "Variable_Assignment":		#if type is a variable assignment
				self.parsetree[-1].appendTok(self.tokens[self.tokindex])
				self.next()
				if self.tokens[self.tokindex].type == "Identifier" or self.tokens[self.tokindex].type == "Integer_Constant" or self.tokens[self.tokindex].type == "Float_Constant":		#if type is an identifier
					self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
					self.next()
					if insideifelse == False:
							self.statement()
				elif self.tokens[self.tokindex].type == "String_Delimiter": #for string literal case #Statement.tokens will look like this: ["VISIBLE",'"', StringLiteralToken, '"'] 
					self.parsetree[-1].appendTok(self.tokens[self.tokindex]) 		#calls the statement method appendTok and adds tokens to the Tokens list of the most recent statement
					self.next()
					self.next() #move 2 indeces
					if self.tokens[self.tokindex].type == "String_Delimiter":
						self.parsetree[-1].appendTok(self.tokens[self.tokindex-1])    #adds the end string delimiter
						self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds string literal
						self.next()
						if insideifelse == False:
							self.statement()							   #back to self.statement to check if there are more statements /recursively call it again
					else: self.callError("SYNTAX ERROR: String Delimiter expected on line " + str(self.tokens[self.tokindex].row))
				elif self.tokens[self.tokindex].type == "TROOF":		
					self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
					self.next()
					if insideifelse == False:
						self.statement()
				elif self.tokens[self.tokindex].type == "Arithmetic_Op":
					self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
					self.next()
					self.arithmetic()
				elif self.tokens[self.tokindex].type == "Boolean_Op":
					self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
					self.bool()
				elif self.tokens[self.tokindex].type == "Comparison_Op":
					self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
					self.next()
					self.comparison()	
				else: self.callError("SYNTAX ERROR: Identifier expected on line: " + str(self.tokens[self.tokindex].row))
			else:
				self.statement()
		else: self.callError("SYNTAX ERROR: Identifier expected on line: " + str(self.tokens[self.tokindex].row))

	def bool(self):
		comp_expr = False
		insideifelse = False
		if self.tokens[self.tokindex-1].type == "Comparison_Op" or self.tokens[self.tokindex-1].type == "Win_Cond" or self.tokens[self.tokindex-1].type == "Fail_Cond" or insideswitch == True:
			insideifelse = True
		if self.tokens[self.tokindex].tok == "NOT":
			self.next()
			if self.tokens[self.tokindex].type == "Identifier" or self.tokens[self.tokindex].type == "TROOF":		#if type is an identifier
				self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
				self.next()
				if insideifelse == False:
					self.statement()
			else: self.callError("SYNTAX ERROR: Identifier or TROOF literal expected on line: " + str(self.tokens[self.tokindex].row))		
		elif self.tokens[self.tokindex].tok == "ALL OF" or self.tokens[self.tokindex].tok == "ANY OF":
			num_id = 0
			line_num = self.tokens[self.tokindex].row
			while self.tokens[self.tokindex].type != "End_Op" and self.tokens[self.tokindex].row == line_num:		
				self.next()
				if self.tokens[self.tokindex].type == "Identifier" or self.tokens[self.tokindex].type == "TROOF":
					self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
					self.next()
					num_id += 1
				elif self.tokens[self.tokindex].tok == "NOT":
					self.parsetree[-1].appendTok(self.tokens[self.tokindex])
					self.next()
					if self.tokens[self.tokindex].type == "Identifier" or self.tokens[self.tokindex].type == "TROOF":		#if type is an identifier
						self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
						self.next()
						num_id += 1
					else: self.callError("SYNTAX ERROR: Identifier or TROOF literal expected on line: " + str(self.tokens[self.tokindex].row))		
				elif self.tokens[self.tokindex].tok == "BOTH OF" or self.tokens[self.tokindex].tok == "EITHER OF" or self.tokens[self.tokindex].tok == "WON OF":
					self.parsetree[-1].appendTok(self.tokens[self.tokindex])
					self.next()
					if self.tokens[self.tokindex].type == "Identifier" or self.tokens[self.tokindex].type == "TROOF":		#if type is an identifier
						self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
						self.next()
						if self.tokens[self.tokindex].type == "Op_Sep":	
							self.parsetree[-1].appendTok(self.tokens[self.tokindex])	
							self.next()
							if self.tokens[self.tokindex].type == "Identifier" or self.tokens[self.tokindex].type == "TROOF":		#if type is an identifier
								self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
								self.next()
								num_id += 1
							else: self.callError("SYNTAX ERROR: Identifier or TROOF literal expected on line: " + str(self.tokens[self.tokindex].row))		
						else: self.callError("SYNTAX ERROR: Operand Separator expected on line: " + str(self.tokens[self.tokindex].row))		
					else: self.callError("SYNTAX ERROR: Identifier or TROOF literal expected on line: " + str(self.tokens[self.tokindex].row))		
				elif self.tokens[self.tokindex].type == "Comparison_Op":
					self.parsetree[-1].appendTok(self.tokens[self.tokindex])
					self.next()
					self.comparison()
				else: self.callError("SYNTAX ERROR: Invalid token in comparison expression on line: " + str(self.tokens[self.tokindex].row))		

				if num_id >= 1:
					if self.tokens[self.tokindex].type == "End_Op":	
						break

				if self.tokens[self.tokindex].type == "Op_Sep":	
					self.parsetree[-1].appendTok(self.tokens[self.tokindex])	
					# self.next()
					# if self.tokens[self.tokindex].type == "Identifier" or self.tokens[self.tokindex].type == "Boolean_Op":		#if type is an identifier
					# 	pass
					# else: print("SYNTAX ERROR: Identifier expected on line: " + str(self.tokens[self.tokindex].row))		
				else: self.callError("SYNTAX ERROR: Operand Separator expected on line: " + str(self.tokens[self.tokindex].row))
								
			if self.tokens[self.tokindex].type == "End_Op":	
				self.parsetree[-1].appendTok(self.tokens[self.tokindex])
				self.next()
				if insideifelse == False:
					self.statement()
			else: self.callError("SYNTAX ERROR: Expected MKAY on line: " + str(self.tokens[self.tokindex-1].row))
				# if insideifelse == False:
				# 	self.statement()

		else:
			self.next()
			if self.tokens[self.tokindex].type == "Identifier" or self.tokens[self.tokindex].type == "TROOF":		#if type is an identifier
				self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
				self.next()
				if self.tokens[self.tokindex].type == "Op_Sep":	
					self.parsetree[-1].appendTok(self.tokens[self.tokindex])	
					self.next()
					if self.tokens[self.tokindex].type == "Identifier" or self.tokens[self.tokindex].type == "TROOF":		#if type is an identifier
						self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
						self.next()
						if insideifelse == False:
							self.statement()
					else: self.callError("SYNTAX ERROR: Identifier or TROOF literal expected on line: " + str(self.tokens[self.tokindex].row))		
				else: self.callError("SYNTAX ERROR: Operand Separator expected on line: " + str(self.tokens[self.tokindex].row))		
			elif self.tokens[self.tokindex].type == "Boolean_Op":
				bool_row = self.tokens[self.tokindex].row
				while (self.tokens[self.tokindex].row == bool_row):
					if self.tokens[self.tokindex].type == "Identifier" or self.tokens[self.tokindex].type == "TROOF" or  self.tokens[self.tokindex].type == "Boolean_Op" or  self.tokens[self.tokindex].type == "Op_Sep":
						self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
						self.next()
					else: self.callError("SYNTAX ERROR: Invalid token on line: " + str(self.tokens[self.tokindex].row))
				self.statement()
			else: self.callError("SYNTAX ERROR: Identifier or TROOF literal expected on line: " + str(self.tokens[self.tokindex].row))		

	def arithmetic(self):
		insideifelse = False
		if self.tokens[self.tokindex-1].type == "Win_Cond" or self.tokens[self.tokindex-1].type == "Fail_Cond" or insideswitch == True:
			insideifelse = True
		no_of_operands = 2
		i = self.tokindex
		op_row = self.tokens[self.tokindex].row
		#while self.tokens[i].type != "Integer_Constant" and self.tokens[i].type != "Float_Constant" and self.tokens[i].type != "String_Delimiter" and self.tokens[i].type != "Identifier":
		while self.tokens[i].row == op_row:
			if self.tokens[i].type == "Arithmetic_Op":
				no_of_operands += 1
			i += 1
			#else:  self.callError("SYNTAX ERROR: Identifier expected on line: " + str(self.tokens[self.tokindex].row))
		

		if no_of_operands > 2:
			self.parsetree[-1].appendTok(self.tokens[self.tokindex])	
			self.next()
			arith_row = self.tokens[self.tokindex].row
			while (self.tokens[self.tokindex].row == arith_row):
				if self.tokens[self.tokindex].type == "Identifier" or self.tokens[self.tokindex].type == "Integer_Constant" or self.tokens[self.tokindex].type == "Float_Constant"or self.tokens[i].type != "String_Delimiter"or self.tokens[i].type != "String_Literal" or self.tokens[self.tokindex].type == "Arithmetic_Op" or  self.tokens[self.tokindex].type == "Op_Sep":
					self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
					self.next()
				else: self.callError("SYNTAX ERROR: Invalid token on line: " + str(self.tokens[self.tokindex].row))
			self.statement()
		else: 
			while no_of_operands != 0:
				if self.tokens[self.tokindex].type == "String_Delimiter":
					self.parsetree[-1].appendTok(self.tokens[self.tokindex]) 		
					self.next()
					self.next() #move 2 indeces
					if self.tokens[self.tokindex].type == "String_Delimiter":
						self.parsetree[-1].appendTok(self.tokens[self.tokindex-1])    #adds the end string delimiter
						self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds string literal
						self.next()
						no_of_operands -=1							   #back to self.statement to check if there are more statements /recursively call it again
					else: self.callError("SYNTAX ERROR: String Delimiter expected on line " + str(self.tokens[self.tokindex].row))
					
					if no_of_operands != 0:
						if self.tokens[self.tokindex].type == "Op_Sep":	
							self.parsetree[-1].appendTok(self.tokens[self.tokindex])	
							self.next()
						else: self.callError("SYNTAX ERROR: Operand Separator expected on line: " + str(self.tokens[self.tokindex].row))		
					else: break
				elif self.tokens[self.tokindex].type != "Integer_Constant" or self.tokens[self.tokindex].type != "Float_Constant" or self.tokens[self.tokindex].type != "Identifier":
					self.parsetree[-1].appendTok(self.tokens[self.tokindex])	
					self.next()
					no_of_operands -= 1
					if no_of_operands != 0:
						if self.tokens[self.tokindex].type == "Op_Sep":	
							self.parsetree[-1].appendTok(self.tokens[self.tokindex])	
							self.next()
						else: self.callError("SYNTAX ERROR: Operand Separator expected on line: " + str(self.tokens[self.tokindex].row))		
					else: break
				else: self.callError("SYNTAX ERROR: Identifier expected on line: " + str(self.tokens[self.tokindex].row))		

		if insideifelse == False:
			self.statement()
	
	def comparison(self):
		insideifelse = False
		if self.tokens[self.tokindex-1].type == "Win_Cond" or self.tokens[self.tokindex-1].type == "Fail_Cond" or insideswitch == True:
			insideifelse = True
		ifinbool = False
		first_op = self.tokens[self.tokindex].tok
		if self.tokens[self.tokindex-1].type == "Boolean_Op": 
			ifinbool = True
		if self.tokens[self.tokindex].type == "Integer_Constant" or self.tokens[self.tokindex].type == "Float_Constant" or self.tokens[self.tokindex].type == "Identifier":		#if type is an identifier
			self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
			self.next()
			if self.tokens[self.tokindex].type == "Op_Sep":	
				self.parsetree[-1].appendTok(self.tokens[self.tokindex])	
				self.next()
				if self.tokens[self.tokindex].type == "Integer_Constant" or self.tokens[self.tokindex].type == "Float_Constant" or self.tokens[self.tokindex].type == "Identifier":		#if type is an identifier
					self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
					self.next()
					if insideifelse == False:
						self.statement()
				elif self.tokens[self.tokindex].type == "Comparison_Op":
					self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
					self.next()
					self.comparison()
				elif self.tokens[self.tokindex].type == "Arithmetic_Op":
					self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
					self.next()
					self.arithmetic()
				elif self.tokens[self.tokindex].tok == "BIGGR OF" or self.tokens[self.tokindex].tok == "SMALLR OF":
					self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
					self.next()
					if self.tokens[self.tokindex].tok == first_op:
						if self.tokens[self.tokindex].type == "Integer_Constant" or self.tokens[self.tokindex].type == "Float_Constant" or self.tokens[self.tokindex].type == "Identifier":
							self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
							self.next()
							if self.tokens[self.tokindex].type == "Op_Sep":	
								self.parsetree[-1].appendTok(self.tokens[self.tokindex])	
								self.next()
								if self.tokens[self.tokindex].type == "Integer_Constant" or self.tokens[self.tokindex].type == "Float_Constant" or self.tokens[self.tokindex].type == "Identifier":
									self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
									self.next()
									if ifinbool == False:
										if insideifelse == False:
											self.statement()
								else: self.callError("SYNTAX ERROR: Identifier expected on line: " + str(self.tokens[self.tokindex].row))		
							else: self.callError("SYNTAX ERROR: Operand Separator expected on line: " + str(self.tokens[self.tokindex].row))		
						else: self.callError("SYNTAX ERROR: Identifier expected on line: " + str(self.tokens[self.tokindex].row))	
					else: self.callError("SYNTAX ERROR: 1st operand must be equal on line: " + str(self.tokens[self.tokindex].row))	
				else: self.callError("SYNTAX ERROR: Identifier expected on line: " + str(self.tokens[self.tokindex].row))		
			else: self.callError("SYNTAX ERROR: Operand Separator expected on line: " + str(self.tokens[self.tokindex].row))		
		
		elif self.tokens[self.tokindex].type == "Arithmetic_Op":
			self.parsetree[-1].appendTok(self.tokens[self.tokindex])
			self.next()
			self.arithmetic()
			if self.tokens[self.tokindex].type == "Op_Sep":	
				self.parsetree[-1].appendTok(self.tokens[self.tokindex])	
				self.next()
				if self.tokens[self.tokindex].type == "Integer_Constant" or self.tokens[self.tokindex].type == "Float_Constant" or self.tokens[self.tokindex].type == "Identifier":		#if type is an identifier
					self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
					self.next()
					if insideifelse == False:
						self.statement()
				elif self.tokens[self.tokindex].type == "Comparison_Op":
					self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
					self.next()
					self.comparison()
				elif self.tokens[self.tokindex].type == "Arithmetic_Op":
					self.parsetree[-1].appendTok(self.tokens[self.tokindex])
					self.next()
					self.arithmetic()
				elif self.tokens[self.tokindex].tok == "BIGGR OF" or self.tokens[self.tokindex].tok == "SMALLR OF":
					self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
					self.next()
					if self.tokens[self.tokindex].tok == first_op:
						if self.tokens[self.tokindex].type == "Integer_Constant" or self.tokens[self.tokindex].type == "Float_Constant" or self.tokens[self.tokindex].type == "Identifier":
							self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
							self.next()
							if self.tokens[self.tokindex].type == "Op_Sep":	
								self.parsetree[-1].appendTok(self.tokens[self.tokindex])	
								self.next()
								if self.tokens[self.tokindex].type == "Integer_Constant" or self.tokens[self.tokindex].type == "Float_Constant" or self.tokens[self.tokindex].type == "Identifier":
									self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
									self.next()
									if ifinbool == False:
										if insideifelse == False:
											self.statement()
								else: self.callError("SYNTAX ERROR: Identifier expected on line: " + str(self.tokens[self.tokindex].row))		
							else: self.callError("SYNTAX ERROR: Operand Separator expected on line: " + str(self.tokens[self.tokindex].row))		
						else: self.callError("SYNTAX ERROR: Identifier expected on line: " + str(self.tokens[self.tokindex].row))	
					else: self.callError("SYNTAX ERROR: 1st operand must be equal on line: " + str(self.tokens[self.tokindex].row))	
				else: self.callError("SYNTAX ERROR: Identifier expected on line: " + str(self.tokens[self.tokindex].row))		
			else: self.callError("SYNTAX ERROR: Operand Separator expected on line: " + str(self.tokens[self.tokindex].row))		
		
		elif self.tokens[self.tokindex].type == "Comparison_Op":
			self.parsetree[-1].appendTok(self.tokens[self.tokindex])
			self.next()
			self.comparison()
			if self.tokens[self.tokindex].type == "Op_Sep":	
				self.parsetree[-1].appendTok(self.tokens[self.tokindex])	
				self.next()
				if self.tokens[self.tokindex].type == "Integer_Constant" or self.tokens[self.tokindex].type == "Float_Constant" or self.tokens[self.tokindex].type == "Identifier":		#if type is an identifier
					self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
					self.next()
					if insideifelse == False:
						self.statement()
				elif self.tokens[self.tokindex].type == "Comparison_Op":
					self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
					self.next()
					self.comparison()
				elif self.tokens[self.tokindex].type == "Arithmetic_Op":
					self.parsetree[-1].appendTok(self.tokens[self.tokindex])
					self.next()
					self.arithmetic()
				elif self.tokens[self.tokindex].tok == "BIGGR OF" or self.tokens[self.tokindex].tok == "SMALLR OF":
					self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
					self.next()
					if self.tokens[self.tokindex].tok == first_op:
						if self.tokens[self.tokindex].type == "Integer_Constant" or self.tokens[self.tokindex].type == "Float_Constant" or self.tokens[self.tokindex].type == "Identifier":
							self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
							self.next()
							if self.tokens[self.tokindex].type == "Op_Sep":	
								self.parsetree[-1].appendTok(self.tokens[self.tokindex])	
								self.next()
								if self.tokens[self.tokindex].type == "Integer_Constant" or self.tokens[self.tokindex].type == "Float_Constant" or self.tokens[self.tokindex].type == "Identifier":
									self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
									self.next()
									if ifinbool == False:
										if insideifelse == False:
											self.statement()
								else: self.callError("SYNTAX ERROR: Identifier expected on line: " + str(self.tokens[self.tokindex].row))		
							else: self.callError("SYNTAX ERROR: Operand Separator expected on line: " + str(self.tokens[self.tokindex].row))		
						else: self.callError("SYNTAX ERROR: Identifier expected on line: " + str(self.tokens[self.tokindex].row))	
					else: self.callError("SYNTAX ERROR: 1st operand must be equal on line: " + str(self.tokens[self.tokindex].row))	
				else: self.callError("SYNTAX ERROR: Identifier expected on line: " + str(self.tokens[self.tokindex].row))		
			else: self.callError("SYNTAX ERROR: Operand Separator expected on line: " + str(self.tokens[self.tokindex].row))		
		

		else: self.callError("SYNTAX ERROR: Identifier expected on line: " + str(self.tokens[self.tokindex].row))		

	def assignment(self):
		insideifelse = False
		if self.tokens[self.tokindex-1].type == "Win_Cond" or self.tokens[self.tokindex-1].type == "Fail_Cond" or insideswitch == True:
			insideifelse = True
		self.parsetree[-1].appendTok(self.tokens[self.tokindex-1])
		if self.tokens[self.tokindex].type == "Identifier" or self.tokens[self.tokindex].type == "Integer_Constant" or self.tokens[self.tokindex].type == "Float_Constant":		#if type is an identifier
			self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
			self.next()
			if insideifelse == False:
				self.statement()
		elif self.tokens[self.tokindex].type == "String_Delimiter": #for string literal case #Statement.tokens will look like this: ["VISIBLE",'"', StringLiteralToken, '"'] 
			self.parsetree[-1].appendTok(self.tokens[self.tokindex]) 		#calls the statement method appendTok and adds tokens to the Tokens list of the most recent statement
			self.next()
			self.next() #move 2 indeces
			if self.tokens[self.tokindex].type == "String_Delimiter":
				self.parsetree[-1].appendTok(self.tokens[self.tokindex-1])    #adds the end string delimiter
				self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds string literal
				self.next()
				if insideifelse == False:
					self.statement()							   #back to self.statement to check if there are more statements /recursively call it again
			else: self.callError("SYNTAX ERROR: String Delimiter expected on line " + str(self.tokens[self.tokindex].row))
		elif self.tokens[self.tokindex].type == "TROOF":		
			self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
			self.next()
			if insideifelse == False:
				self.statement()
		elif self.tokens[self.tokindex].type == "Arithmetic_Op":
			self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
			self.next()
			self.arithmetic()
		elif self.tokens[self.tokindex].type == "Boolean_Op":
			self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
			self.bool()
		elif self.tokens[self.tokindex].type == "Comparison_Op":
			self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
			self.next()
			self.comparison()	
		else: self.callError("SYNTAX ERROR: Identifier expected on line: " + str(self.tokens[self.tokindex].row))

	#Error calls
	def callError(self, text):
		output = []
		output.append(text)
		self.interpreter.update_exec(output, "<PRINT>")
		self.error = True

class Interpreter():
	def __init__(self, root):
		self.root = root
		self.line_num = 1
		self.error = False
		self.root.title("Lolcode interpreter")
		self.init_gui()

	def init_gui(self): #set the GUI
		self.rootwidth = 1120
		self.rootheight = 700
		self.root.geometry("%dx%d" % (self.rootwidth, self.rootheight)) 
		#self.root.resizable(False, False)
		#top frame where code, token table, and symbol table will be put, invisible
		self.frametop = Frame(self.root,width = self.rootwidth, height = self.rootheight*0.45) #creates frame in middle of the screen where tiles be put
		self.frametop.grid(row = 0, column = 0)
		self.frametop.grid_propagate(0)
		#bottom frame where execute will be done
		self.framebot = Frame(self.root, bg = "light gray", width = self.rootwidth-20, height = self.rootheight*0.6) #creates frame in middle of the screen where tiles be put
		self.framebot.grid(row = 1 , column = 0, padx = 10, pady = 10)
		self.framebot.grid_propagate(0)
		self.init_codeframe() #frame for entering code under frametop
		self.init_tokenframe() #frame for showing tokentable under frametop
		self.init_symbolframe() #frame for showing symboltable under frametop
		self.init_execFrame() #frame for executing functions under framebottom

	def init_execFrame(self):
		self.execButton = Button(self.framebot, text = "Execute", width = 140)
		self.execButton.grid(row = 0, column = 0, padx = 5, pady = 5)
		self.execButton.grid_propagate(0)
		self.execScreen = Frame(self.framebot,bg = "light gray", width = self.rootwidth-20, height = self.rootheight*0.6)
		self.execScreen.grid(row = 1, column = 0, padx = 5, pady = 5, sticky= "w")

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
		self.execButton.configure(command = lambda: self.run(content))

	############## MAIN PROGRAM FOR THE INTERPRETER###############
	def run(self, content):
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
		self.symbolTable = copy.deepcopy(tokens)
		self.update_symbolTable(self.symbolTable)

		if self.error == False: #if lexical analysis does not have an error
			#SYNTAX ANALYSIS
			self.syntax = Syntax_Analyzer(self.symbolTable, self) #dynamically updates statement id of Tokens in symbolTable 
			self.syntax.viewparse() #prints parse tree to console for viewing

			'''
			# FOR CHECKING IF ELSE AND SWITCH CASE BLOCKS 
			#checks if symbolTable is updated with the correct block info
			for token in self.symbolTable :
				print( str(token.statementId) + " " + str(token.tok) + " " + str(token.block))
			'''

			if self.syntax.error == False: #if syntax analysis has no error continue semantic analysis
				#SEMANTIC ANALYSIS
				self.sem = Semantic_Analyzer(self.symbolTable,self.syntax.parsetree,self)

				#UPDATES SYMBOL TABLE GUI
				self.update_symbolTable(self.symbolTable)


	###################################################

	#populate the lexeme table with identified lexemes
	def fill_lexTable(self, lexemes):
		for i in range(len(lexemes)):
			self.lexemeTableGUI.insert(parent='', index='end', iid=i, text="", values=(lexemes[i][0], lexemes[i][1]))

	def update_symbolTable(self, symbols):
		self.symbolTable = copy.deepcopy(symbols)
		for i in self.symbolTableGUI.get_children():
			self.symbolTableGUI.delete(i)
		for i in range(len(self.symbolTable)):
			self.symbolTableGUI.insert(parent='', index='end', iid=i, text="", values=(self.symbolTable[i].tok, self.symbolTable[i].value))

	#Prints the values , errors and shows gimmeh when called to the GUI console
	def update_exec(self, outputlist, operation ):
		if operation == "<PRINT>":
			for cont in self.execScreen.winfo_children():
				cont.destroy()
			for i in range(len(outputlist)):
				Label(self.execScreen,bg = "light gray", text = outputlist[i]).grid(row = i, column = 0, sticky = "w")
		elif operation == "<INPUT>":
			for cont in self.execScreen.winfo_children():
				cont.destroy()
			for i in range(len(outputlist)):
				Label(self.execScreen,bg = "light gray", text = outputlist[i]).grid(row = i, column = 0, sticky = "w")
			gimmehInput = -1
			self.inString = StringVar() 
			self.gimmehEntry = Entry(self.execScreen, textvariable =self.inString).grid(row = len(outputlist), column = 0, sticky = "w" )
			self.gimmehButton = Button(self.execScreen, text = "Enter input", command = lambda: self.get_input(outputlist)).grid(row = len(outputlist), column = 1, sticky = "w" )

	#when gimmeh input button is clicked, semantic analysis is resumed
	def get_input(self, outputlist):
		self.gimmehInput = self.inString.get()
		outputlist.append(self.gimmehInput)
		for cont in self.execScreen.winfo_children():
			cont.destroy()
		for i in range(len(outputlist)):
			Label(self.execScreen,bg = "light gray", text = outputlist[i]).grid(row = i, column = 0, sticky = "w")
		self.sem.continueInput()				#continue where left of in semantic analysis

	def read_file(self, filename):
		#Every new read clear contents of previous widgets
		for cont in self.codeBox.winfo_children():
			cont.destroy()
		for i in self.lexemeTableGUI.get_children():
			self.lexemeTableGUI.delete(i)
		for i in self.symbolTableGUI.get_children():
			self.symbolTableGUI.delete(i)
		for cont in self.execScreen.winfo_children():
			cont.destroy()
		self.line_num = 1
		self.error = False
		#STARTS reading content of file
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
            ('Variable_Assignment', r'ITZ'),
            ('Output_Keyword', r'VISIBLE'),
            ('String', r'".*?"'),
            ('TROOF', r'(WIN|FAIL)'),
            ('Arithmetic_Op', r'(SUM OF|DIFF OF|PRODUKT OF|QUOSHUNT OF|MOD OF|BIGGR OF|SMALLR OF)'),
            ('Boolean_Op', r'(BOTH OF|EITHER OF|WON OF|NOT|ALL OF|ANY OF)'),
            ('End_Op', r'MKAY'),
            ('Comparison_Op', r'(BOTH SAEM|DIFFRINT)'),
            ('Accept_Keyword', r'GIMMEH'),
            ('Cond_Begin', r'O RLY\?,?'),
            ('Cond_End', r'OIC'),
            ('Win_Cond', r'YA RLY,?'),
            ('Else_Cond', r'MEBBE'),
            ('Fail_Cond', r'NO WAI'),
            ('Default_Case', r'OMGWTF'),
            ('Start_Switch', r'WTF\?'),
            ('Switch_Case', r'OMG'),
            ('Break', r'GTFO'),
            ('Loop_Begin', r'IM IN YR'),
            ('Loop_End', r'IM OUTTA YR'),
            ('Increment_Keyword', r'UPPIN'),
            ('Decrement_Keyword', r'NERFIN'),
            ('Stop_Win', r'TIL'),
            ('Stop_Fail', r'WILE'),
            ('Function_Begin', r'HOW IZ I'),
            ('Function_End', r'IF U SAY SO'),
            ('Return_Value', r'FOUND YR'),
            ('Assignment', r'R'),
            ('Op_Sep', r'AN'),
            ('Identifier', r'[a-zA-Z]\w*'),     # IDENTIFIERS
            ('Float_Constant', r'-?\d(\d)*\.\d(\d)*'),   # FLOAT
            ('Integer_Constant', r'-?\d(\d)*'),          # INT
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
				tokens.append(Token('"', "String_Delimiter", self.line_num, col, len(tokens) + 1))
				tokens.append(Token(token_lexeme, "String_Literal", self.line_num, col, len(tokens) + 1))
				tokens.append(Token('"', "String_Delimiter", self.line_num, col, len(tokens) + 1))
			elif token_type == 'Skip':			#skips spaces
			    continue
			elif token_type == 'Error':			#shows error
				print("MALIII")
				self.callError('%r unexpected on line %d' % (token_lexeme, self.line_num))
			else:								#when the token is not one of the special cases, add it to actual list of tokens
				col = m.start() - line_start
				tokens.append(Token(token_lexeme, token_type, self.line_num, col, len(tokens) + 1))

		return tokens    #returns list of tokens

	def callError(self, text):
		output = []
		output.append(text)
		self.update_exec(output, "<PRINT>")
		self.error = True

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