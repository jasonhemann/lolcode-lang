from tkinter import ttk
from tkinter import filedialog
from tkinter import *
from arith import *
from booleans import *
from comp import *
from ifelse import *
from helperFuncs import *
import settings
import os
import sys

def evaluateExpression(expr,lineNumber,lineTokens):

	finalAnswer = None						# Final answer is value of the expression to be returned
	# Arithmetic Expressions
	if re.match(sumof,expr) or re.match(diffof,expr) or re.match(produktof,expr) or re.match(quoshuntof,expr) or re.match(modof,expr) or re.match(biggrof,expr) or re.match(smallrof,expr):

		arithExpr = manageArithKeywords(expr)			
		
		for lexeme in arithExpr:

			if lexeme in arithOpsList:								# If the lexeme is an arith operator (SUMOF,DIFFOF)	
				lineTokens.append(('Arithmetic Operator',lexeme))
			elif lexeme == "AN":
				lineTokens.append(('Operand Separator',lexeme))
			elif isArithOperand(lexeme) != False:
				lineTokens.append(('Arithmetic Operand',lexeme))
			elif isVariable(lexeme) and lexeme in varDict:
				lineTokens.append(('Variable Identfier',lexeme))
			else :
				printError("Invalid Lexeme in Arithmetic Expression",lineNumber)
				return False

		value = mainArith(arithExpr,lineNumber)
		if value == False: return False
		else: value = str(value)
		varType = getVarType(value)
		finalAnswer = [varType,value]
	
	# Comparison Expressions
	elif re.match(bothsaem,expr) or re.match(diffrint,expr):

		compExpr = manageCompKeywords(expr)
			
		for lexeme in compExpr:

			if lexeme in compOpsList:
				lineTokens.append(('Comparison Operator',lexeme))
			elif lexeme == "AN":
				lineTokens.append(('Operand Separator',lexeme))
			elif isCompOperand(lexeme) != False:
				lineTokens.append(('Comparison Operand',lexeme))
			elif isVariable(lexeme) and lexeme in varDict:
				lineTokens.append(('Variable Identfier',lexeme))
			else :
				printError("Invalid Lexeme in Comparison Expression",lineNumber)
				return False

		value = mainComp(compExpr,lineNumber)
		if value == False: return False
		else: value = str(value)
		varType = getVarType(value)
		finalAnswer = [varType,value]

	# Boolean Expressions
	elif re.match(notop,expr) or re.match(eitherof,expr) or re.match(wonof,expr) or re.match(bothof,expr) or re.match(allof,expr) or re.match(anyof,expr):	

		boolExpr = manageBoolKeywords(expr)

		for lexeme in boolExpr:

			if lexeme in boolOpsList:
				lineTokens.append(('Boolean Operator',lexeme))
			elif lexeme == "AN":
				lineTokens.append(('Operand Separator',lexeme))
			elif isBoolOperand(lexeme) != False:
				lineTokens.append(('Boolean Operand',lexeme))
			elif isVariable(lexeme) and lexeme in varDict:
				lineTokens.append(('Variable Identfier',lexeme))
			elif lexeme == "MKAY":
				lineTokens.append(('End Keyword',lexeme))
			else :
				printError("Invalid Lexeme in Boolean Expression",lineNumber)
				return False
		
		value = mainBool(boolExpr,lineNumber)
		if value == False: return False
		else: value = str(value)
		varType = getVarType(value)
		finalAnswer = [varType,value]

	# String Concatenation 
	elif re.match(smoosh,expr):
		m = re.match(smoosh,expr)
		kw = m.group('kw')
		ops = m.group('ops')

		ops = smooshHelper(ops)

		lineTokens.append(('Print Keyword','VISIBLE'))
		lineTokens.append(('Concatenate Keyword',kw))
		for lexeme in ops:
			if lexeme == "AN":
				lineTokens.append(('Operand Separator',lexeme))
			else:
				lineTokens.append(('Concatenation Operator',lexeme))
		finalAnswer = smooshExpression(ops,lineNumber)
		if finalAnswer == False: return False
		varType = getVarType(finalAnswer)
		varDict['IT'] = [varType,finalAnswer]

	# If it doesn't match with any expression print an error 
	else:
		printError("Invalid Expression",lineNumber)
		return False

	if finalAnswer != None:
		return finalAnswer
	else:
		printError("Expression has no return value",lineNumber)
		return False


def tokenizer(sourceLines,tokens,visibleLines):

	lineNumber = 0
	disabled = False
	caseFlag = 1
	
	for line in sourceLines:		# tokenize every line in the sourceLines

		lineNumber += 1				# Increment Line Number
		thisLine = line.split()		# List form of the line 
		lineTokens = []
		printLine = []				# List to append with stuff to print

		if settings.hasError == True:		# Return False if an error is detected 
			return False
		
		if re.match(hai,line):											# Start
			lineTokens.append(('Program Start',line))

		elif re.match(kthxbye,line):								    # End
			lineTokens.append(('Program End',line))

		elif re.match(ihasa,line):										# Variable Declaration 

			lineTokens.append(('Declaration Keyword','I HAS A'))
			
			if (len(thisLine) == 4) and isVariable(thisLine[3]):					# Variable Declaration with no initialization
				lineTokens.append(('Variable Identifier',thisLine[3]))
				varName = thisLine[3]
		
				varDict[varName] = [None,None]										# Add to variable dictionary with unknown type and unknown value 
			
			elif re.match(ihasitz,line):											# Variable Declaration with initialization
				
				m = re.match(ihasitz,line).groups()
				lineTokens.append(('Variable Identifier',m[2]))
				lineTokens.append(("Assigment KeyWord",m[3]))

				if getVarType(m[4]) != False:										# m[2] is the variable , m[3] = ITZ, m[4] is the value 
					varType = getVarType(m[4])
					lineTokens.append((varType,m[4]))	
					varDict[m[2]] = [varType,m[4]]

				elif isVariable(m[4]) == True and (m[4] in varDict): 				# Used in I HAS A X ITZ Y 
					value = varDict[m[4]][1]
					varType = varDict[m[4]][0]
					varDict[m[2]] = [varType,value]
					lineTokens.append(("Assign to Variable",m[4]))	

				elif isExpression(m[4]):
					exprValue = evaluateExpression(m[4],sourceLines.index(line)+1,lineTokens)	# exprValue[0] = type | exprValue[0] = value 
					if exprValue == False: return False
					varDict[m[2]] = exprValue
		
				else:
					printError("Invalid LExeme in Variable Declaration",sourceLines.index(line)+1)
					return False
					
			else: 
				printError("Error in Lexer - Variable Declaration",sourceLines.index(line)+1)
				return False
	
		elif re.match(gimmeh,line) and disabled == False:												# If it is an input Statement 
			m = re.match(gimmeh,line)
			kw = m.group('kw')
			var = m.group('var')
			lineTokens.append(('Input KeyWord',kw))								# Gimmeh tokenized as keyword

			if isVariable(var) and (var in varDict):
				lineTokens.append(('Variable Identfier',var))					# IF variable passes, tokenized as variable identifier 
				
				def getInput():
					inputLine = e.get()
					varType = getVarType(inputLine)								# Put to Variable Dictionary 
					varDict[var] = [varType,inputLine]
					strMsg = "Received: " + inputLine
					l.configure(text = strMsg)									# Change label to confirm input reception
					b.configure(state="disabled")								# Disable Submit button
					new.quit()
				
				new = Tk()	
				l = Label(new,width=20,bg="dodgerblue3",text="Enter Input")
				e = Entry(new,width=20,fg="black",borderwidth=5)
				b = Button(new,width=10,text="Submit",bg ="SlateGray1",command=getInput)

				l.pack()
				e.pack()
				b.pack()

				new.mainloop()

			else:
				printError("Error at Gimmeh, Variable Not Found",sourceLines.index(line)+1)
				return False
		
		elif re.match(r,line) and disabled == False:													# If assignment Statement

			m = re.match(r,line)
			var = m.group('var')
			kw = m.group('kw')
			val = m.group('val')

			if var not in varDict: 
				printError("Unbound Variable in Assignment Operation",sourceLines.index(line)+1)
				return False
			if isVariable(var): lineTokens.append(('Variable Identifier',var))

			if kw == "R": lineTokens.append(('Assignment Keyword', kw))

			if isLiteral(val) != False:
				literalType = isLiteral(val)
				lineTokens.append((literalType,val))
				val = str(val)
				varType = getVarType(val)
				varDict[var] = [varType,val]
			elif isVariable(val) and val in varDict:
				varDict[var][0] = varDict[val][0]
				varDict[var][0] = varDict[val][0] 
			elif isExpression(val) :
				exprValue = evaluateExpression(val,sourceLines.index(line)+1,lineTokens)
				if exprValue == False: return False
				varDict[var] = exprValue
			else:
				printError("Invalid lexeme at assignment statement",sourceLines.index(line)+1)
				return False
				
		elif re.match(visible,line) and disabled == False :											# If it is a print statement 
			
			m = re.match(visible, line)
			kw = m.group('kw')
			lineTokens.append(('Print Keyword',kw))	
			expr = m.group('expr')
			
			if re.match(smoosh,expr):											#currently special case
				lineTokens.pop()
				value = evaluateExpression(expr,sourceLines.index(line)+1,lineTokens)
				if value == False: return False
				tokens.append(lineTokens)
				print("-",value,len(value))
				printLine.append(value)
				if len(printLine) > 0:visibleLines.append(printLine)
				continue
			
			strList = re.findall(r"\"[^\"]*\"",expr)	# Get all strings, enclosed in doublq quotes
			expr = expr.split('"')				# Split by double quotes delimiter, original list, changes will be stored here 
			copy = []							# Copy list used for evaluation
		
			for entry in expr: 					# Copy the trimmed strings to copy list 
				new = re.sub(r"^\s+|\s+$", "", entry)
				copy.append(new)

			for string in strList:
				lineTokens.append(("String Literal",string))

			for entry in copy:													# Substitute Variables in the Statement 

				if entry in varDict and isVariable(entry):						# If it is a variable 
					expr[copy.index(entry)] = varDict[entry][1] 				# Get the value in vardict and replace it in the original list 
					lineTokens.append(('Variable Identfier',entry))

				elif isLiteral(entry) !=  False:								# If printing a Literal
					dataType = isLiteral(entry)
					lineTokens.append((dataType,entry))
				
				elif isExpression(entry):										# If printing an expression 
					
					value = evaluateExpression(entry,sourceLines.index(line)+1,lineTokens)
					if value == False: return False
					varDict['IT'] = value
					strVal = str(value[1])
					expr[copy.index(entry)] = strVal

			finalStr = ""
			for element in expr:
				finalStr = finalStr + element
			
			printLine.append(finalStr)

		elif (re.match(sumof,line) or re.match(diffof,line) or re.match(produktof,line) or re.match(quoshuntof,line) or re.match(modof,line) or re.match(biggrof,line) or re.match(smallrof,line)) and disabled == False :	# Arithmetic Statement 
		
			arithExpr = manageArithKeywords(line)			
			
			for lexeme in arithExpr:

				if lexeme in arithOpsList:								# If the lexeme is an arith operator (SUMOF,DIFFOF)	
					lineTokens.append(('Arithmetic Operator',lexeme))
				elif lexeme == "AN":
					lineTokens.append(('Operand Separator',lexeme))
				elif isArithOperand(lexeme) != False:
					lineTokens.append(('Arithmetic Operand',lexeme))
				elif isVariable(lexeme) and evalVar(lexeme):
					lineTokens.append(('Variable Identfier',lexeme))
				else :
					printError("Invalid Lexeme in Arithmetic Expression",sourceLines.index(line)+1)
					return False
			
			# Assign Expression's return value to IT 
			finalAnswer = mainArith(arithExpr,sourceLines.index(line)+1)
			if finalAnswer == False: return False
			else: finalAnswer = str(finalAnswer)
			varType = getVarType(finalAnswer)
			varDict['IT'] = [varType,finalAnswer]
			print("Final Answer to Arithmetic Expression: ",finalAnswer)

		elif (re.match(bothsaem,line) or re.match(diffrint,line))  and disabled == False:		# Comparison Expressions 

			compExpr = manageCompKeywords(line)
			
			for lexeme in compExpr:

				if lexeme in compOpsList:
					lineTokens.append(('Comparison Operator',lexeme))
				elif lexeme == "AN":
					lineTokens.append(('Operand Separator',lexeme))
				elif isCompOperand(lexeme) != False:
					lineTokens.append(('Comparison Operand',lexeme))
				elif isVariable(lexeme) and evalVar(lexeme):
					lineTokens.append(('Variable Identfier',lexeme))
				else :
					printError("Invalid Lexeme in Comparison Expression",sourceLines.index(line)+1)
					return False
						
			# Assign Expression's return value to IT 
			finalAnswer = mainComp(compExpr,sourceLines.index(line)+1)
			if finalAnswer == False: return False
			else: finalAnswer = str(finalAnswer)
			varType = getVarType(finalAnswer)
			varDict['IT'] = [varType,finalAnswer]
			print("Final Answer to Comparison Expression: ",finalAnswer)

		elif (re.match(notop,line) or re.match(eitherof,line) or re.match(bothof,line) or re.match(wonof,line) or re.match(allof,line) or re.match(anyof,line)) and disabled == False :		# Boolean operations

			boolExpr = manageBoolKeywords(line)

			for lexeme in boolExpr:

				if lexeme in boolOpsList:
					lineTokens.append(('Boolean Operator',lexeme))
				elif lexeme == "AN":
					lineTokens.append(('Operand Separator',lexeme))
				elif isBoolOperand(lexeme) != False:
					lineTokens.append(('Boolean Operand',lexeme))
				elif isVariable(lexeme) and evalVar(lexeme):
					lineTokens.append(('Variable Identfier',lexeme))
				elif lexeme == "MKAY":
					lineTokens.append(('Boolean Delimiter',lexeme))
				else :
					printError("Invalid Lexeme in Boolean Expression",sourceLines.index(line)+1)
					return False

			# Assign Expression's return value to IT 
			finalAnswer = mainBool(boolExpr,sourceLines.index(line)+1)
			if finalAnswer == False: return False
			else: finalAnswer = str(finalAnswer)
			varType = getVarType(finalAnswer)
			varDict['IT'] = [varType,finalAnswer]
			print("Final Answer to Boolean Expression: ",finalAnswer)

		elif re.match(smoosh,line) and disabled == False:
			m = re.match(smoosh,line)
			kw = m.group('kw')
			ops = m.group('ops')

			ops = smooshHelper(ops)

			lineTokens.append(('Concatenate Keyword',kw))
			for lexeme in ops:
				if lexeme == "AN":
					lineTokens.append(('Operand Separator',lexeme))
				else:
					lineTokens.append(('Concatenation Operator',lexeme))

			finalAnswer = smooshExpression(ops,lineNumber)
			if finalAnswer == False: return False
			else: finalAnswer = str(finalAnswer)
			varType = getVarType(finalAnswer)
			varDict['IT'] = [varType,finalAnswer]
			print("SMOOSH: "+ finalAnswer)
		
		elif re.match(orly,line):									 # Start of If statement 
			lineTokens.append(('Start of Condtional',lexeme))

			start = sourceLines.index(line)							 # Index of YA RLY, start of loop 

			inds = findIndex(start,sourceLines)						# Finds the Indices of YA RLY, NO WAI, and OIC
			if inds == False: return False							# Error In Finding Index 
			ya = inds[0]
			no = inds[1]
			end = inds[2]

			condValue = varDict['IT'][1]

			if condValue == None: 
				printError("IT has no value thus Condtional Statement, cannot be evaluated",lineNumber)
				return False
			if condValue == 'WIN':		
				print("YA RLY block will execute")
				disabled = False		# Will Disable at NO WAI and Reenable at OIC
			else:					
				print("NO WAI block will execute")	
				disabled = True			# Will Disable here and Reenable at NO WAI 
														
		elif re.match(nowai,line):
			lineTokens.append(('Conditional Else Block',line))
			disabled = not(disabled)

		elif re.match(wtf,line):
			lineTokens.append(('Switch-case Keyword',"WTF?"))
			condValue = varDict['IT'][1]
			if condValue == None: 
				printError("IT has no value thus Switch-case Statement, cannot be evaluated",lineNumber)
				return False
			disabled = not(disabled)

		elif re.match(omg,line):
			m = re.match(omg,line)
			kw = m.group('kw')
			lit = m.group('lit')
			if varDict['IT'][1] == lit:
				lineTokens.append(('Case Keyword',kw))
				lineTokens.append(('Literal',lit))
				disabled = not(disabled)
				caseFlag = True
			else: continue
				
		elif re.match(gtfo,line):
			if disabled == True: continue
			disabled = not(disabled)
			caseFlag = False
			lineTokens.append(('End of Case Keyword','GTFO'))

		elif re.match(omgwtf,line):
			if caseFlag == False: continue
			else:
				lineTokens.append(('Default Keyword',"OMGWTF"))
				disabled = False

		elif re.match(oicswitch,line):
			lineTokens.append(('End of Conditional',"OIC"))
			disabled = False

		elif re.match(yarly,line):
			lineTokens.append(('Conditional IF Block',line))	

		elif re.match(empty,line) or disabled == True:
			pass

		else :
			printError("Unrecognized Pattern of Expression",lineNumber)
			return False

		## End
		if len(printLine) > 0: visibleLines.append(printLine)
		if len(lineTokens) > 0 : tokens.append(lineTokens)







