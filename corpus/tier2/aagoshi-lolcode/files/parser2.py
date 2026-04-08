'''
This program creates the initial GUI and lexical analyzer for lolcode interpreter
'''
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import copy
import re

insideswitch = False

class Token():
	def __init__(self, token, ttype, row, col, index):
		self.tok = token              #string of token
		self.type = ttype      		  #type of token
		self.row = row                #row/line where it is located
		self.col = col 
		self.index = index
		self.statementId = None			  
		self.value = None             #no value yet

class Statement():
	def __init__(self, tokens, ttype, statementId):
		self.tokens = tokens              #list of Tokens in that statement
		self.type = ttype                 #type of the statement
		self.id = statementId 			  #index of the statement
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

class Semantic_Analyzer():
	def __init__(self, symbolTable, parseTree):
		self.tokens = symbolTable			#symbol table constantly updated
		self.statements = parseTree 		#parse tree from syntax analyzer static

	def interpret(self):
		for statement in syntax.parsetree:
			solve(statement.type, statement.tokens)

	def solve(self, stype, stok):
		if stype == "<PRINT>":
			self.print(stype, stok)			
		elif stype == "<DECLARATION>":
			self.declaration(stype, stok)

	def print(self,stype, stok):
		printvalue = ""
		for i in range(1, len(stok)):
			if stok[i].type == "String_Literal":	#expected combination ["VISIBLE",'"', StringLiteralToken, '"']
				printvalue += stok[i].tok     		#concatenate if string literal
			elif stok[i].type == "Identifier":
				stok[i].index

	def declaration(self,stype, stok):
		pass


class Syntax_Analyzer():
	def __init__(self, tokens):
		self.tokens = tokens         	#tokens list
		self.tokindex = 0 	            #current token index
		self.parsetree = None			#[STATEMENT1, STATEMENT2, STATEMENT3] will look like this
		self.statementId = -1			#index of statement currently added - this value will be updated to self.tokens. start to -1 because it will immediately be incremented to 1 under statement thus will actually start at value 0
		self.program()

	#forward to next index in self.tokens 
	def next(self):
		self.tokindex = self.tokindex + 1
		if self.parsetree != None : 				 	#if parse tree has been initialize the succeeding tokens will have a statement id that will match the parse tree
			self.tokens[self.tokindex].statementId = self.statementId #check if tamang index ang inuupdate

	#update current statementid
	def nextstmnt(self):
		self.statementId = self.statementId + 1 

	#where main syntax analysis is done
	def parse(self):
		pass

	#or dapat ba line per line ng token na nakaloop?? instead na per function??
	def program(self): # <program>	::=	HAI <linebreak> <statement> <linebreak> KTHXBYE
		if self.tokens[0].tok == "HAI":
			if self.tokens[1].type == "Float_Constant":
				self.next()						 #move to next token
			if self.tokens[-1].tok == "KTHXBYE": #something like this though di ko sure kung tama na pagsabayin o line per line dapat
				print(str(self.tokindex) + " ")	 #checking lang kung nasaang index na
				self.next() 					 #move to next token
				self.parsetree = []				 #initialize parse tree tells that a program has started
				self.statement()
			else: print("SYNTAX ERROR: KTHXBYE expected on line " + str(self.tokens[-1].row)) #di ko sure kunt tama icheck agad kthxbye baka skip muna ito
		else: print("SYNTAX ERROR: HAI expected on line " + str(self.tokens[0].row))

	def statement(self): #<statement> ::= <statement><linebreak><statement> | <expression> | <switchcase> | <ifthen> | <varcall> | <print> | <input> 
		global insideswitch
		print(str(self.tokindex) + " ")
		if self.tokens[self.tokindex].type == "Output_Keyword": #for VISIBLE/ <print> case
			self.parsetree.append(Statement([self.tokens[self.tokindex]], "<PRINT>", self.statementId))
			self.nextstmnt()
			self.next()						#all self.next() starting this statement fxn will have a statement id value
			self.print()
		elif self.tokens[self.tokindex].type == "Accept_Keyword": #for GIMMEH/ <input> case
			self.parsetree.append(Statement([self.tokens[self.tokindex]], "<INPUT>", self.statementId))
			self.nextstmnt()
			self.next()
			self.input()
		elif self.tokens[self.tokindex].type == "Variable_Declaration": #for I HAS A/ <DECLARATION> case
			self.parsetree.append(Statement([self.tokens[self.tokindex]], "<DECLARATION>", self.statementId))
			self.nextstmnt()
			self.next()
			self.variable()
		elif self.tokens[self.tokindex].type == "Boolean_Op": #for <boolean> case
			self.parsetree.append(Statement([self.tokens[self.tokindex]], "<BOOLEAN>", self.statementId))
			self.nextstmnt()
			self.bool()
		elif self.tokens[self.tokindex].type == "Arithmetic_Op": #for <arithmetic> case
			self.parsetree.append(Statement([self.tokens[self.tokindex]], "<ARITHMETIC>", self.statementId))
			self.nextstmnt()
			self.next()
			self.arithmetic()
		elif self.tokens[self.tokindex].type == "Comparison_Op": #for <comparison> case
			self.parsetree.append(Statement([self.tokens[self.tokindex]], "<COMPARISON>", self.statementId))
			self.nextstmnt()
			self.next()
			self.comparison()
		elif self.tokens[self.tokindex].type == "Identifier": #for <assignment> case
			self.next()
			if self.tokens[self.tokindex].type == "Assignment": #for <assignment> case
				self.parsetree.append(Statement([self.tokens[self.tokindex-1]], "<ASSIGNMENT>", self.statementId))
				self.nextstmnt()
				self.next()
				self.assignment()
			else: print("SYNTAX ERROR: Assignment operator expected on line " + str(self.tokens[self.tokindex].row))
		elif self.tokens[self.tokindex].type == "Cond_Begin": #for <if-else> case
			orly_row = self.tokens[self.tokindex].row
			self.parsetree.append(Statement([self.tokens[self.tokindex]], "<IF-ELSE>", self.statementId))
			self.nextstmnt()
			self.next()
			if self.tokens[self.tokindex].row != orly_row:
				if self.tokens[self.tokindex].type == "Win_Cond": #for <if-else> case
					yarly_row = self.tokens[self.tokindex].row
					self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
					print(str(self.tokindex) + " ")
					self.next()
					if self.tokens[self.tokindex].row != yarly_row:
						self.expression()
						if self.tokens[self.tokindex].type == "Fail_Cond":
							nowai_row = self.tokens[self.tokindex].row
							self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
							print(str(self.tokindex) + " ")
							self.next()
							if self.tokens[self.tokindex].row != nowai_row:
								self.expression()
								if self.tokens[self.tokindex].type == "Cond_End":
									oic_row = self.tokens[self.tokindex].row
									self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
									print(str(self.tokindex) + " ")
									self.next()
									if self.tokens[self.tokindex].row != oic_row:
										self.statement()
									else: print("SYNTAX ERROR: OIC must be alone on line " + str(self.tokens[self.tokindex].row))		
								else: print("SYNTAX ERROR: OIC expected on line " + str(self.tokens[self.tokindex].row))
							else: print("SYNTAX ERROR: NO WAI must be alone on line " + str(self.tokens[self.tokindex].row))		
						else: print("SYNTAX ERROR: NO WAI expected on line " + str(self.tokens[self.tokindex].row))
					else: print("SYNTAX ERROR: YA RLY must be alone on line " + str(self.tokens[self.tokindex].row))
				else: print("SYNTAX ERROR: YA RLY expected on line " + str(self.tokens[self.tokindex].row))
			else: print("SYNTAX ERROR: O RLY? must be alone on line " + str(self.tokens[self.tokindex].row))
		elif self.tokens[self.tokindex].type == "Start_Switch": #for <switch> case
			insideswitch = True
			wtf_row = self.tokens[self.tokindex].row
			self.parsetree.append(Statement([self.tokens[self.tokindex]], "<SWITCH>", self.statementId))
			self.next()
			if self.tokens[self.tokindex].row != wtf_row:
				# while self.tokens[self.tokindex].type != "Default_Case":
				# 	self.cases()
				while self.tokens[self.tokindex].type != "Cond_End":
					if self.tokens[self.tokindex].type == "Default_Case":
						self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
						print(str(self.tokindex) + " ")
						self.next()		
					else:
						self.cases()
				self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
				print(str(self.tokindex) + " ")
				self.next()
				insideswitch = False
				self.statement()

			else: print("SYNTAX ERROR: WTF? must be alone on line " + str(self.tokens[self.tokindex].row))

		

	def print(self):
		insideifelse = False
		if self.tokens[self.tokindex-1].type == "Win_Cond" or self.tokens[self.tokindex-1].type == "Fail_Cond" or insideswitch == True:
			insideifelse = True
		print(str(self.tokindex) + " ")
		line_num = self.tokens[self.tokindex].row
		while self.tokens[self.tokindex].row == line_num:	
			if self.tokens[self.tokindex].type == "String_Delimiter": #for string literal case #Statement.tokens will look like this: ["VISIBLE",'"', StringLiteralToken, '"'] 
				self.parsetree[-1].appendTok(self.tokens[self.tokindex]) 		#calls the statement method appendTok and adds tokens to the Tokens list of the most recent statement
				self.next()
				self.next() #move 2 indeces
				if self.tokens[self.tokindex].type == "String_Delimiter":
					self.parsetree[-1].appendTok(self.tokens[self.tokindex-1])    #adds the end string delimiter
					self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds string literal
					print(str(self.tokindex) + " ")
					print(print(self.tokens[self.tokindex-1].tok)) #print the middle item
					self.next()							   #back to self.statement to check if there are more statements /recursively call it again
				else: print("SYNTAX ERROR: String Delimiter expected on line " + str(self.tokens[self.tokindex].row))
			elif self.tokens[self.tokindex].type == "Integer_Constant" or self.tokens[self.tokindex].type == "Float_Constant" or self.tokens[self.tokindex].type == "Identifier":
					self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
					print(str(self.tokindex) + " ")
					self.next()
			elif self.tokens[self.tokindex].type == "TROOF":		
				self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
				print(str(self.tokindex) + " ")
				self.next()
				if insideifelse == False:
					self.statement()
			elif self.tokens[self.tokindex].type == "Arithmetic_Op":
				self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
				print(str(self.tokindex) + " ")
				self.next()
				self.arithmetic()
			elif self.tokens[self.tokindex].type == "Boolean_Op":
				self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
				print(str(self.tokindex) + " ")
				self.bool()
			elif self.tokens[self.tokindex].type == "Comparison_Op":
				self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
				print(str(self.tokindex) + " ")
				self.next()
				self.comparison()	

		if insideifelse == False:
			self.statement()

	def input(self):
		insideifelse = False
		if self.tokens[self.tokindex-1].type == "Win_Cond" or self.tokens[self.tokindex-1].type == "Fail_Cond" or insideswitch == True:
			insideifelse = True
		print(str(self.tokindex) + " ")
		if self.tokens[self.tokindex].type == "Identifier":		#if type is an identifier
			self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
			print(str(self.tokindex) + " ")
			self.next()
			if insideifelse == False:
				self.statement()
		else: print("SYNTAX ERROR: Identifier expected on line: " + str(self.tokens[self.tokindex].row))

	def variable(self):
		insideifelse = False
		if self.tokens[self.tokindex-1].type == "Win_Cond" or self.tokens[self.tokindex-1].type == "Fail_Cond" or insideswitch == True:
			insideifelse = True
		print(str(self.tokindex) + " ")
		if self.tokens[self.tokindex].type == "Identifier":		#if type is an identifier
			self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
			print(str(self.tokindex) + " ")
			self.next()
			if self.tokens[self.tokindex].type == "Variable_Assignment":		#if type is a variable assignment
				self.parsetree[-1].appendTok(self.tokens[self.tokindex])
				self.next()
				if self.tokens[self.tokindex].type == "Identifier" or self.tokens[self.tokindex].type == "Integer_Constant" or self.tokens[self.tokindex].type == "Float_Constant":		#if type is an identifier
					self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
					print(str(self.tokindex) + " ")
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
						print(str(self.tokindex) + " ")
						print(print(self.tokens[self.tokindex-1].tok)) #print the middle item
						self.next()
						if insideifelse == False:
							self.statement()							   #back to self.statement to check if there are more statements /recursively call it again
					else: print("SYNTAX ERROR: String Delimiter expected on line " + str(self.tokens[self.tokindex].row))
				elif self.tokens[self.tokindex].type == "TROOF":		
					self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
					print(str(self.tokindex) + " ")
					self.next()
					if insideifelse == False:
						self.statement()
				elif self.tokens[self.tokindex].type == "Arithmetic_Op":
					self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
					print(str(self.tokindex) + " ")
					self.next()
					self.arithmetic()
				elif self.tokens[self.tokindex].type == "Boolean_Op":
					self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
					print(str(self.tokindex) + " ")
					self.bool()
				elif self.tokens[self.tokindex].type == "Comparison_Op":
					self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
					print(str(self.tokindex) + " ")
					self.next()
					self.comparison()	
				else: print("SYNTAX ERROR: Identifier expected on line: " + str(self.tokens[self.tokindex].row))
			else:
				self.statement()
		else: print("SYNTAX ERROR: Identifier expected on line: " + str(self.tokens[self.tokindex].row))

	def bool(self):
		comp_expr = False
		insideifelse = False
		if self.tokens[self.tokindex-1].type == "Comparison_Op" or self.tokens[self.tokindex-1].type == "Win_Cond" or self.tokens[self.tokindex-1].type == "Fail_Cond" or insideswitch == True:
			insideifelse = True
		print(str(self.tokindex) + " ")
		if self.tokens[self.tokindex].tok == "NOT":
			self.next()
			if self.tokens[self.tokindex].type == "Identifier" or self.tokens[self.tokindex].type == "TROOF":		#if type is an identifier
				self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
				print(str(self.tokindex) + " ")
				self.next()
				if insideifelse == False:
					self.statement()
			else: print("SYNTAX ERROR: Identifier expected on line: " + str(self.tokens[self.tokindex].row))		
		elif self.tokens[self.tokindex].tok == "ALL OF" or self.tokens[self.tokindex].tok == "ANY OF":
			num_id = 0
			line_num = self.tokens[self.tokindex].row
			while self.tokens[self.tokindex].type != "End_Op" and self.tokens[self.tokindex].row == line_num:		
				self.next()
				if self.tokens[self.tokindex].type == "Identifier" or self.tokens[self.tokindex].type == "TROOF":
					self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
					print(str(self.tokindex) + " ")
					self.next()
					num_id += 1
				elif self.tokens[self.tokindex].tok == "NOT":
					self.parsetree[-1].appendTok(self.tokens[self.tokindex])
					print(str(self.tokindex) + " ")
					self.next()
					if self.tokens[self.tokindex].type == "Identifier" or self.tokens[self.tokindex].type == "TROOF":		#if type is an identifier
						self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
						print(str(self.tokindex) + " ")
						self.next()
						num_id += 1
					else: print("SYNTAX ERROR: Identifier expected on line: " + str(self.tokens[self.tokindex].row))		
				elif self.tokens[self.tokindex].tok == "BOTH OF" or self.tokens[self.tokindex].tok == "EITHER OF" or self.tokens[self.tokindex].tok == "WON OF":
					self.parsetree[-1].appendTok(self.tokens[self.tokindex])
					print(str(self.tokindex) + " ")
					self.next()
					if self.tokens[self.tokindex].type == "Identifier" or self.tokens[self.tokindex].type == "TROOF":		#if type is an identifier
						self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
						print(str(self.tokindex) + " ")
						self.next()
						if self.tokens[self.tokindex].type == "Op_Sep":	
							self.parsetree[-1].appendTok(self.tokens[self.tokindex])	
							print(str(self.tokindex) + " ")
							self.next()
							if self.tokens[self.tokindex].type == "Identifier" or self.tokens[self.tokindex].type == "TROOF":		#if type is an identifier
								self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
								print(str(self.tokindex) + " ")
								self.next()
								num_id += 1
							else: print("SYNTAX ERROR: Identifier expected on line: " + str(self.tokens[self.tokindex].row))		
						else: print("SYNTAX ERROR: Operand Separator expected on line: " + str(self.tokens[self.tokindex].row))		
					else: print("SYNTAX ERROR: Identifier expected on line: " + str(self.tokens[self.tokindex].row))		
				elif self.tokens[self.tokindex].type == "Comparison_Op":
					self.parsetree[-1].appendTok(self.tokens[self.tokindex])
					self.next()
					self.comparison()
				else: print("SYNTAX ERROR: Identifier expected on line: " + str(self.tokens[self.tokindex].row))		

				if num_id >= 1:
					if self.tokens[self.tokindex].type == "End_Op":	
						break

				if self.tokens[self.tokindex].type == "Op_Sep":	
					self.parsetree[-1].appendTok(self.tokens[self.tokindex])	
					print(str(self.tokindex) + " ")
					# self.next()
					# if self.tokens[self.tokindex].type == "Identifier" or self.tokens[self.tokindex].type == "Boolean_Op":		#if type is an identifier
					# 	pass
					# else: print("SYNTAX ERROR: Identifier expected on line: " + str(self.tokens[self.tokindex].row))		
				else: print("SYNTAX ERROR: Operand Separator expected on line: " + str(self.tokens[self.tokindex].row))
								
			if self.tokens[self.tokindex].type == "End_Op":	
				self.parsetree[-1].appendTok(self.tokens[self.tokindex])
				print(str(self.tokindex) + " ")
				self.next()
				if insideifelse == False:
					self.statement()
			else:
				if insideifelse == False:
					self.statement()

		else:
			self.next()
			print(self.tokens[self.tokindex].type)
			if self.tokens[self.tokindex].type == "Identifier" or self.tokens[self.tokindex].type == "TROOF":		#if type is an identifier
				self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
				print(str(self.tokindex) + " ")
				self.next()
				if self.tokens[self.tokindex].type == "Op_Sep":	
					self.parsetree[-1].appendTok(self.tokens[self.tokindex])	
					print(str(self.tokindex) + " ")
					self.next()
					if self.tokens[self.tokindex].type == "Identifier" or self.tokens[self.tokindex].type == "TROOF":		#if type is an identifier
						self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
						print(str(self.tokindex) + " ")
						self.next()
						if insideifelse == False:
							self.statement()
					else: print("SYNTAX ERROR: Identifier expected on line: " + str(self.tokens[self.tokindex].row))		
				else: print("SYNTAX ERROR: Operand Separator expected on line: " + str(self.tokens[self.tokindex].row))		
			else: print("SYNTAX ERROR: Identifier expected on line: " + str(self.tokens[self.tokindex].row))		

	def arithmetic(self):
		insideifelse = False
		if self.tokens[self.tokindex-1].type == "Win_Cond" or self.tokens[self.tokindex-1].type == "Fail_Cond" or insideswitch == True:
			insideifelse = True
		print(str(self.tokindex) + " ")
		no_of_operands = 2
		while self.tokens[self.tokindex].type != "Integer_Constant" and self.tokens[self.tokindex].type != "Float_Constant" and self.tokens[self.tokindex].type != "String_Delimiter" and self.tokens[self.tokindex].type != "Identifier":
			if self.tokens[self.tokindex].type == "Arithmetic_Op":
				self.parsetree[-1].appendTok(self.tokens[self.tokindex])	
				print(str(self.tokindex) + " ")
				self.next()
				no_of_operands += 1
			else:  print("SYNTAX ERROR: Identifier expected on line: " + str(self.tokens[self.tokindex].row))
					
		while no_of_operands != 0:
			if self.tokens[self.tokindex].type == "String_Delimiter":
				self.parsetree[-1].appendTok(self.tokens[self.tokindex]) 		#calls the statement method appendTok and adds tokens to the Tokens list of the most recent statement
				self.next()
				self.next() #move 2 indeces
				if self.tokens[self.tokindex].type == "String_Delimiter":
					self.parsetree[-1].appendTok(self.tokens[self.tokindex-1])    #adds the end string delimiter
					self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds string literal
					print(str(self.tokindex) + " ")
					print(print(self.tokens[self.tokindex-1].tok)) #print the middle item
					self.next()
					no_of_operands -=1							   #back to self.statement to check if there are more statements /recursively call it again
				else: print("SYNTAX ERROR: String Delimiter expected on line " + str(self.tokens[self.tokindex].row))
				
				if no_of_operands != 0:
					if self.tokens[self.tokindex].type == "Op_Sep":	
						self.parsetree[-1].appendTok(self.tokens[self.tokindex])	
						print(str(self.tokindex) + " ")
						self.next()
					else: print("SYNTAX ERROR: Operand Separator expected on line: " + str(self.tokens[self.tokindex].row))		
				else: break
			elif self.tokens[self.tokindex].type != "Integer_Constant" or self.tokens[self.tokindex].type != "Float_Constant" or self.tokens[self.tokindex].type != "Identifier":
				self.parsetree[-1].appendTok(self.tokens[self.tokindex])	
				print(str(self.tokindex) + " ")
				self.next()
				no_of_operands -= 1
				if no_of_operands != 0:
					if self.tokens[self.tokindex].type == "Op_Sep":	
						self.parsetree[-1].appendTok(self.tokens[self.tokindex])	
						print(str(self.tokindex) + " ")
						self.next()
					else: print("SYNTAX ERROR: Operand Separator expected on line: " + str(self.tokens[self.tokindex].row))		
				else: break
			else: print("SYNTAX ERROR: Identifier expected on line: " + str(self.tokens[self.tokindex].row))		

		if insideifelse == False:
			self.statement()
	
	def comparison(self):
		insideifelse = False
		if self.tokens[self.tokindex-1].type == "Win_Cond" or self.tokens[self.tokindex-1].type == "Fail_Cond" or insideswitch == True:
			insideifelse = True
		ifinbool = False
		first_op = self.tokens[self.tokindex].tok
		print(self.tokens[self.tokindex].type)
		if self.tokens[self.tokindex-1].type == "Boolean_Op": 
			ifinbool = True
		if self.tokens[self.tokindex].type == "Integer_Constant" or self.tokens[self.tokindex].type == "Float_Constant" or self.tokens[self.tokindex].type == "Identifier":		#if type is an identifier
			self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
			print(str(self.tokindex) + " ")
			self.next()
			if self.tokens[self.tokindex].type == "Op_Sep":	
				self.parsetree[-1].appendTok(self.tokens[self.tokindex])	
				print(str(self.tokindex) + " ")
				self.next()
				if self.tokens[self.tokindex].type == "Integer_Constant" or self.tokens[self.tokindex].type == "Float_Constant" or self.tokens[self.tokindex].type == "Identifier":		#if type is an identifier
					self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
					print(str(self.tokindex) + " ")
					self.next()
					if insideifelse == False:
						self.statement()
				elif self.tokens[self.tokindex].type == "Comparison_Op":
					self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
					print(str(self.tokindex) + " ")
					self.next()
					self.comparison()
				elif self.tokens[self.tokindex].type == "Arithmetic_Op":
					self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
					print(str(self.tokindex) + " ")
					self.next()
					self.arithmetic()
				elif self.tokens[self.tokindex].tok == "BIGGR OF" or self.tokens[self.tokindex].tok == "SMALLR OF":
					self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
					print(str(self.tokindex) + " ")
					self.next()
					if self.tokens[self.tokindex].tok == first_op:
						if self.tokens[self.tokindex].type == "Integer_Constant" or self.tokens[self.tokindex].type == "Float_Constant" or self.tokens[self.tokindex].type == "Identifier":
							self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
							print(str(self.tokindex) + " ")
							self.next()
							if self.tokens[self.tokindex].type == "Op_Sep":	
								self.parsetree[-1].appendTok(self.tokens[self.tokindex])	
								print(str(self.tokindex) + " ")
								self.next()
								if self.tokens[self.tokindex].type == "Integer_Constant" or self.tokens[self.tokindex].type == "Float_Constant" or self.tokens[self.tokindex].type == "Identifier":
									self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
									print(str(self.tokindex) + " ")
									self.next()
									if ifinbool == False:
										if insideifelse == False:
											self.statement()
								else: print("SYNTAX ERROR: Identifier expected on line: " + str(self.tokens[self.tokindex].row))		
							else: print("SYNTAX ERROR: Operand Separator expected on line: " + str(self.tokens[self.tokindex].row))		
						else: print("SYNTAX ERROR: Identifier expected on line: " + str(self.tokens[self.tokindex].row))	
					else: print("SYNTAX ERROR: 1st operand must be equal on line: " + str(self.tokens[self.tokindex].row))	
				else: print("SYNTAX ERROR: Identifier expected on line: " + str(self.tokens[self.tokindex].row))		
			else: print("SYNTAX ERROR: Operand Separator expected on line: " + str(self.tokens[self.tokindex].row))		
		
		elif self.tokens[self.tokindex].type == "Arithmetic_Op":
			self.parsetree[-1].appendTok(self.tokens[self.tokindex])
			self.next()
			self.arithmetic()
			if self.tokens[self.tokindex].type == "Op_Sep":	
				self.parsetree[-1].appendTok(self.tokens[self.tokindex])	
				print(str(self.tokindex) + " ")
				self.next()
				if self.tokens[self.tokindex].type == "Integer_Constant" or self.tokens[self.tokindex].type == "Float_Constant" or self.tokens[self.tokindex].type == "Identifier":		#if type is an identifier
					self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
					print(str(self.tokindex) + " ")
					self.next()
					if insideifelse == False:
						self.statement()
				elif self.tokens[self.tokindex].type == "Comparison_Op":
					self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
					print(str(self.tokindex) + " ")
					self.next()
					self.comparison()
				elif self.tokens[self.tokindex].type == "Arithmetic_Op":
					self.parsetree[-1].appendTok(self.tokens[self.tokindex])
					self.next()
					self.arithmetic()
				elif self.tokens[self.tokindex].tok == "BIGGR OF" or self.tokens[self.tokindex].tok == "SMALLR OF":
					self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
					print(str(self.tokindex) + " ")
					self.next()
					if self.tokens[self.tokindex].tok == first_op:
						if self.tokens[self.tokindex].type == "Integer_Constant" or self.tokens[self.tokindex].type == "Float_Constant" or self.tokens[self.tokindex].type == "Identifier":
							self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
							print(str(self.tokindex) + " ")
							self.next()
							if self.tokens[self.tokindex].type == "Op_Sep":	
								self.parsetree[-1].appendTok(self.tokens[self.tokindex])	
								print(str(self.tokindex) + " ")
								self.next()
								if self.tokens[self.tokindex].type == "Integer_Constant" or self.tokens[self.tokindex].type == "Float_Constant" or self.tokens[self.tokindex].type == "Identifier":
									self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
									print(str(self.tokindex) + " ")
									self.next()
									if ifinbool == False:
										if insideifelse == False:
											self.statement()
								else: print("SYNTAX ERROR: Identifier expected on line: " + str(self.tokens[self.tokindex].row))		
							else: print("SYNTAX ERROR: Operand Separator expected on line: " + str(self.tokens[self.tokindex].row))		
						else: print("SYNTAX ERROR: Identifier expected on line: " + str(self.tokens[self.tokindex].row))	
					else: print("SYNTAX ERROR: 1st operand must be equal on line: " + str(self.tokens[self.tokindex].row))	
				else: print("SYNTAX ERROR: Identifier expected on line: " + str(self.tokens[self.tokindex].row))		
			else: print("SYNTAX ERROR: Operand Separator expected on line: " + str(self.tokens[self.tokindex].row))		
		
		elif self.tokens[self.tokindex].type == "Comparison_Op":
			self.parsetree[-1].appendTok(self.tokens[self.tokindex])
			self.next()
			self.comparison()
			if self.tokens[self.tokindex].type == "Op_Sep":	
				self.parsetree[-1].appendTok(self.tokens[self.tokindex])	
				print(str(self.tokindex) + " ")
				self.next()
				if self.tokens[self.tokindex].type == "Integer_Constant" or self.tokens[self.tokindex].type == "Float_Constant" or self.tokens[self.tokindex].type == "Identifier":		#if type is an identifier
					self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
					print(str(self.tokindex) + " ")
					self.next()
					if insideifelse == False:
						self.statement()
				elif self.tokens[self.tokindex].type == "Comparison_Op":
					self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
					print(str(self.tokindex) + " ")
					self.next()
					self.comparison()
				elif self.tokens[self.tokindex].type == "Arithmetic_Op":
					self.parsetree[-1].appendTok(self.tokens[self.tokindex])
					self.next()
					self.arithmetic()
				elif self.tokens[self.tokindex].tok == "BIGGR OF" or self.tokens[self.tokindex].tok == "SMALLR OF":
					self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
					print(str(self.tokindex) + " ")
					self.next()
					if self.tokens[self.tokindex].tok == first_op:
						if self.tokens[self.tokindex].type == "Integer_Constant" or self.tokens[self.tokindex].type == "Float_Constant" or self.tokens[self.tokindex].type == "Identifier":
							self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
							print(str(self.tokindex) + " ")
							self.next()
							if self.tokens[self.tokindex].type == "Op_Sep":	
								self.parsetree[-1].appendTok(self.tokens[self.tokindex])	
								print(str(self.tokindex) + " ")
								self.next()
								if self.tokens[self.tokindex].type == "Integer_Constant" or self.tokens[self.tokindex].type == "Float_Constant" or self.tokens[self.tokindex].type == "Identifier":
									self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
									print(str(self.tokindex) + " ")
									self.next()
									if ifinbool == False:
										if insideifelse == False:
											self.statement()
								else: print("SYNTAX ERROR: Identifier expected on line: " + str(self.tokens[self.tokindex].row))		
							else: print("SYNTAX ERROR: Operand Separator expected on line: " + str(self.tokens[self.tokindex].row))		
						else: print("SYNTAX ERROR: Identifier expected on line: " + str(self.tokens[self.tokindex].row))	
					else: print("SYNTAX ERROR: 1st operand must be equal on line: " + str(self.tokens[self.tokindex].row))	
				else: print("SYNTAX ERROR: Identifier expected on line: " + str(self.tokens[self.tokindex].row))		
			else: print("SYNTAX ERROR: Operand Separator expected on line: " + str(self.tokens[self.tokindex].row))		
		

		else: print("SYNTAX ERROR: Identifier expected on line: " + str(self.tokens[self.tokindex].row))		

	def assignment(self):
		insideifelse = False
		if self.tokens[self.tokindex-1].type == "Win_Cond" or self.tokens[self.tokindex-1].type == "Fail_Cond" or insideswitch == True:
			insideifelse = True
		self.parsetree[-1].appendTok(self.tokens[self.tokindex-1])
		if self.tokens[self.tokindex].type == "Identifier" or self.tokens[self.tokindex].type == "Integer_Constant" or self.tokens[self.tokindex].type == "Float_Constant":		#if type is an identifier
			self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
			print(str(self.tokindex) + " ")
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
				print(str(self.tokindex) + " ")
				print(print(self.tokens[self.tokindex-1].tok)) #print the middle item
				self.next()
				if insideifelse == False:
					self.statement()							   #back to self.statement to check if there are more statements /recursively call it again
			else: print("SYNTAX ERROR: String Delimiter expected on line " + str(self.tokens[self.tokindex].row))
		elif self.tokens[self.tokindex].type == "TROOF":		
			self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
			print(str(self.tokindex) + " ")
			self.next()
			if insideifelse == False:
				self.statement()
		elif self.tokens[self.tokindex].type == "Arithmetic_Op":
			self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
			print(str(self.tokindex) + " ")
			self.next()
			self.arithmetic()
		elif self.tokens[self.tokindex].type == "Boolean_Op":
			self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
			print(str(self.tokindex) + " ")
			self.bool()
		elif self.tokens[self.tokindex].type == "Comparison_Op":
			self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
			print(str(self.tokindex) + " ")
			self.next()
			self.comparison()	
		else: print("SYNTAX ERROR: Identifier expected on line: " + str(self.tokens[self.tokindex].row))

	def expression(self):
		if self.tokens[self.tokindex].type == "Output_Keyword":
			self.next()
			self.print()
		elif self.tokens[self.tokindex].type == "Accept_Keyword": #for GIMMEH/ <input> case
			# self.parsetree.append(Statement([self.tokens[self.tokindex]], "<INPUT>"))
			self.next()
			self.input()
		elif self.tokens[self.tokindex].type == "Variable_Declaration": #for I HAS A/ <DECLARATION> case
			# self.parsetree.append(Statement([self.tokens[self.tokindex]], "<DECLARATION>"))
			self.next()
			self.variable()
		elif self.tokens[self.tokindex].type == "Boolean_Op": #for <boolean> case
			# self.parsetree.append(Statement([self.tokens[self.tokindex]], "<BOOLEAN>"))
			self.bool()
		elif self.tokens[self.tokindex].type == "Arithmetic_Op": #for <arithmetic> case
			# self.parsetree.append(Statement([self.tokens[self.tokindex]], "<ARITHMETIC>"))
			self.next()
			self.arithmetic()
		elif self.tokens[self.tokindex].type == "Comparison_Op": #for <comparison> case
			# self.parsetree.append(Statement([self.tokens[self.tokindex]], "<COMPARISON>"))
			self.next()
			self.comparison()
		elif self.tokens[self.tokindex].type == "Identifier": #for <assignment> case
			self.next()
			if self.tokens[self.tokindex].type == "Assignment": #for <assignment> case
				# self.parsetree.append(Statement([self.tokens[self.tokindex-1]], "<ASSIGNMENT>"))
				self.next()
				self.assignment()
			else: print("SYNTAX ERROR: Assignment operator expected on line " + str(self.tokens[self.tokindex].row))
	
	def cases(self):
		if self.tokens[self.tokindex].type == "Break":
			self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
			print(str(self.tokindex) + " ")
			self.next()
		elif self.tokens[self.tokindex].type == "Default_Case":
			self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
			print(str(self.tokindex) + " ")
			self.expression()
		elif self.tokens[self.tokindex-1].type != "Break" and self.tokens[self.tokindex-1].type != "Start_Switch":
			self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
			print(str(self.tokindex) + " ")
			self.expression()
		elif self.tokens[self.tokindex].type == "Switch_Case":
			omg_row = self.tokens[self.tokindex].row
			self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
			print(str(self.tokindex) + " ")
			self.next()
			if self.tokens[self.tokindex].row != omg_row:
				print("SYNTAX ERROR: Literal expected on line " + str(self.tokens[self.tokindex].row))	
			elif self.tokens[self.tokindex].type == "Identifier" or self.tokens[self.tokindex].type == "Float_Constant" or self.tokens[self.tokindex].type == "Integer_Constant" or self.tokens[self.tokindex].type == "TROOF":
				self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
				print(str(self.tokindex) + " ")
				self.next()
				if self.tokens[self.tokindex].row != omg_row:
					expr_row = self.tokens[self.tokindex].row
					self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
					print(str(self.tokindex) + " ")
					self.expression()
					# while self.tokens[self.tokindex].type != "Break":
					# 	if self.tokens[self.tokindex].row != expr_row:
					# 		self.expression()
					# 		expr_row = self.tokens[self.tokindex].row
					# 	else: print("SYNTAX ERROR: Expression must be on a separate line on line " + str(self.tokens[self.tokindex].row))	
					# self.parsetree[-1].appendTok(self.tokens[self.tokindex])	#adds identifier to parse tree
					# print(str(self.tokindex) + " ")
					# self.next()
				else: print("SYNTAX ERROR: Expression must be on a separate line on line " + str(self.tokens[self.tokindex].row))	
			else: print("SYNTAX ERROR: Literal expected on line " + str(self.tokens[self.tokindex].row))	
		else: print("SYNTAX ERROR: OMG expected on line " + str(self.tokens[self.tokindex].row))

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
		syntax = Syntax_Analyzer(self.symbolTable) 
		#checking contents of parse tree
		for statement in syntax.parsetree:
			print("Statement: " + str(statement.type) + " ")
			for token in statement.tokens:  #print token in tokens
				print("\t " + str(token.tok))

		# #ATTEMPTING DUMMY SEMANTIC ANALYZER
		# for statement in syntax.parsetree:
		# 	print("Statement: " + str(statement.type) + " ")
		# 	statement.decode()
		# 	#update symbol table?? 

		# print(tokens[1].type)



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
            ('Variable_Assignment', r'ITZ'),
            ('Output_Keyword', r'VISIBLE'),
            ('String', r'".*?"'),
            ('TROOF', r'(WIN|FAIL)'),
            ('Op_Sep', r'AN'),
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
            ('Assignment', r'R'),
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
				tokens.append(Token('"', "String_Delimiter", self.line_num, col, len(tokens) + 1))
				tokens.append(Token(token_lexeme, "String_Literal", self.line_num, col, len(tokens) + 1))
				tokens.append(Token('"', "String_Delimiter", self.line_num, col, len(tokens) + 1))
			elif token_type == 'Skip':			#skips spaces
			    continue
			elif token_type == 'Error':			#shows error
				raise RuntimeError('%r unexpected on line %d' % (token_lexeme, self.line_num))
			else:								#when the token is not one of the special cases, add it to actual list of tokens
				col = m.start() - line_start
				tokens.append(Token(token_lexeme, token_type, self.line_num, col, len(tokens) + 1))

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