from patterns import * 
import settings

# Global Lists
varDict = {'IT':[None,None]} 

def printError(message,lineNumber):
	if lineNumber == "":
		print(message)
	else:
		print("Line:",lineNumber,"",message)

	settings.hasError = True
	settings.errorMessage = message
	settings.errorLine = lineNumber


def isVariable(var):					# Checks if the given parameter fits as a variable identifier 
	if re.match(varIdentifier,var):
		return True
	else: return False

def isString(val):
	if re.match(strIdentifier,val):
		return True
	else:
		return False

def isNumber(val):
	if re.match(numIdentifier,val):
		return True
	else:
		return False

def isFloat(val):
	if re.match(floatIdentifier,val):
		return True
	else : 
		return False

def isTroof(val):
	if re.match(troofIdentifier,val):
		return True
	else: 
		return False

def getVarType(value):	# Returns the type of the Variable, Used for Tokenizing Variables
	if isNumber(value): return "Integer"
	elif isFloat(value): return "Float"
	elif isTroof(value): return "Troof"
	elif isString(value): return "String"
	else : return False	

def isLiteral(value):	# Checks for the type of the value, returns a string of its type, Used for Tokenizing Literals

	if isString(value): return "String Literal"
	elif isNumber(value): return "Integer Literal"
	elif isFloat(value): return "Float Literal"
	elif isTroof(value): return "Troof Literal"
	else : return False

def isExpression(expr):

	if re.match(sumof,expr) or re.match(diffof,expr) or re.match(produktof,expr) or re.match(quoshuntof,expr) or re.match(modof,expr) or re.match(biggrof,expr) or re.match(smallrof,expr):
		print("Matched With Arithmetic Expression",expr)
		return True
	elif re.match(bothsaem,expr) or re.match(diffrint,expr):
		print("Matched With Comparison Expression")
		return True
	elif re.match(notop,expr) or re.match(eitherof,expr) or re.match(bothof,expr) or re.match(wonof,expr) or re.match(allof,expr) or re.match(anyof,expr):
		print("Matched With Boolean Expression",expr)
		return True
	elif re.match(smoosh,expr):
		print("Matched With Concatenation Expression", expr)
		return True
	else:
		#print("Did not match with any expression: ",expr)
		return False

def evaluateIfVar(operand):		# Evaluates a possible variable to its value in string format, Used in Operations

	if operand in varDict:					# If the operand is the list of variables 
		varVal = varDict[operand][1]		# Get the value and the type 
		operand = str(varVal)

	return operand

def evalVar(var):				# Function for Evaluating Variable value
	if var in varDict:
		val = varDict[var]
		return val[1]			# Returns the 2nd element of the list which is the value 
	else : 
		return False			# If the var is not in the list return False 

def checkExpression(stack,listFlag,lineNumber):	#checks the stack if it's balanced
	countArithKey = 0
	countAnKey = 0
	operationsList= None
	if listFlag == "Arithmetic": operationsList = arithOpsList
	elif listFlag == "Boolean": operationsList = boolOpsList
	elif listFlag == "Comparison": operationsList = compOpsList
	
	for key in stack:
		if key in operationsList: countArithKey+=1
		elif key == "NOT": continue
		elif key == "AN": countAnKey+=1

	#break for ALL OF and ANY OF
	if countArithKey != countAnKey:
		printError("Error: Unbalanced pairs of Arithmetic Operands and Operators",lineNumber)
		return False
	return None

#constantly checks within the loop the stack and the series of elements in it
def checkStackExpr(stack,listFlag,lineNumber):
	operationsList= None
	if listFlag == "Arithmetic": operationsList = arithOpsList
	elif listFlag == "Boolean": operationsList = boolOpsList
	elif listFlag == "Comparison": operationsList = compOpsList

	try:
		if stack[-1] == "AN" or stack[0] == "AN" or stack[1] == "AN":
			message = "Syntax Error," + listFlag + ", Incorrectly Placed AN"
			printError(message,lineNumber)
			return True
		elif not (stack[0] in operationsList):
			message = "Syntax Error," + listFlag + ", First Element is not an Operator"
			printError(message,lineNumber)
			return True
		elif stack[-1] in operationsList:
			message = "Syntax Error," + listFlag + ", Last Element is an Operator"
			printError(message,lineNumber)
			return True
	except:
		pass

	return False 


def smooshExpression(stack,lineNumber):															# return the concatenated string
	smooshedWords = ""
	if stack[-1] == "AN": printError("Incomplete number of items to SMOOSH",lineNumber)			# Hanging AN keyword
	print(stack)
	for i in range(len(stack)):
		if i%2 == 1:
			if stack[i] != "AN": 
				printError("Mismatched items in SMOOSH",lineNumber)			# AN delimeter
				return False
		else:
			if stack[i] == "IT": 
				if varDict["IT"][1] != None:
					smooshedWords += str(varDict["IT"][1])
				else:
					printError("Cannot concatenate IT has a None value",lineNumber) 
					return False
			elif isLiteral(stack[i]):
				if isLiteral(stack[i]) == "String Literal":
					smooshedWords += str(stack[i][1:-1])
				else:
					smooshedWords += str(stack[i])								# Literal
			elif isVariable(stack[i]):															# Variable
				temp = evalVar(stack[i])
				if temp != False: 
					if isLiteral(temp) == "String Literal":
						smooshedWords += str(temp[1:-1])
					else:
						smooshedWords += str(temp)
				else: 
					printError(str(stack[i])+ " is not defined",lineNumber)
					return False
			else: 
				printError(str(stack[i])+ ": invalid element in SMOOSH",lineNumber)
				return False
	return smooshedWords

def handleComments(sourceLines):					                        # Replaces the comments with an empty string and returns the edited file
	newSourceLines= []
	notEndComment= True
	errLine = None

	for i in range(len(sourceLines)):
		if re.match(r'[^\s]OBTW',sourceLines[i]):
			printError("Error in multi-line comment: ",sourceLines[i])
			return False
		elif re.match(r'\s*OBTW',sourceLines[i]):
			notEndComment= False
			errLine = i
			sourceLines[i]=""
		elif re.match(r'.*BTW',sourceLines[i]):
			sourceLines[i]= re.sub(r'\s*BTW .*$', "",sourceLines[i])
		elif re.match(r'\s*TLDR',sourceLines[i]) and not notEndComment:
			notEndComment= True
			sourceLines[i]=""
		elif not notEndComment:
			if re.match(kthxbye,sourceLines[i]):
				printError("Error in multi-line comment TLDR not found",errLine)
				return False
			sourceLines[i]=""
		newSourceLines.append(sourceLines[i])

	return newSourceLines
	
def smooshHelper(line):
	string = False

	modifiedLine = []
	wordLetters = ''
	for letter in line:
		if letter == '"' or string:
			wordLetters += letter
			if not string or letter == '"':
				string = not(string)
		elif letter == " ":
			modifiedLine.append(wordLetters)
			wordLetters = ''
		else:
			wordLetters += letter
	if wordLetters != '': modifiedLine.append(wordLetters)
	return modifiedLine

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
				printError("Arithmetic Operation Lexical Error",lineNumber)

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
				print(lexeme)
				printError("Comparison Operation Lexical Error",lineNumber)

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
				print(lexeme)
				printError("Boolean Operation Lexical Error",lineNumber)
		
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
		print("Invalid Expression: ",expr)
		printError("Invalid Expression",lineNumber)
		return False

	if finalAnswer != None:
		return finalAnswer
	else:
		printError("Expression has no return value",lineNumber)
		return False