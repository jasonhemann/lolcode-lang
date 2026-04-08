from helperFuncs import *

## Functions for Comparison Expressions 

def isCompOperand(x):
	if re.match(troofIdentifier,x): return True
	elif re.match(numIdentifier,x): return True
	elif re.match(floatIdentifier,x): return True
	else: return False 

def manageCompKeywords(line):
	keywordListTuple = [("BIGGR OF","BIGGROF"),("SMALLR OF","SMALLROF"),("BOTH SAEM","BOTHSAEM")]
	for keyword in keywordListTuple:
		line = line.replace(keyword[0],keyword[1])
	line = line.split()
	return line

def evaluateCompExpr(operator,operand1,operand2,lineNumber) :

	print("Ops: ",operator," Op1: ",operand1," Op2: ",operand2)
	answer = None

	if isNumber(operand1): operand1 = int(operand1)				# Cast Operand 1 to Its Type
	elif isFloat(operand1) : operand1 = float(operand1)

	if isNumber(operand2): operand2 = int(operand2)				# Cast Operands 2 to Its Type 
	elif isFloat(operand2) : operand2 = float(operand2)

	if operator == "BOTHSAEM":
		if operand1 == operand2: answer = "WIN"	 # Win if equal, Fail if not
		else: answer = "FAIL"
	elif operator == "DIFFRINT":
		if operand1 != operand2: answer = "WIN"	 # Win if not equal, Fail if not 
		else: answer = "FAIL"

	elif operator == "BIGGROF" and (isinstance(operand1,int) or isinstance(operand1,float)) and  (isinstance(operand2,int) or isinstance(operand2,float)):
		
		answer = max(operand1,operand2)

	elif operator == "SMALLROF" and (isinstance(operand1,int) or isinstance(operand1,float)) and  (isinstance(operand2,int) or isinstance(operand2,float)):

		answer = min(operand1,operand2)
	else:
		printError("Error Unrecognized Comparison Operator or Invalid Pair of Operands",lineNumber)
		return False


	return answer

def mainComp(compExpr,lineNumber):
	flag = True							# Flag if running should still continue
	stack = []							# Stack used for computation
	iters = 0
										
	inputLength = len(compExpr)

	for i in range(inputLength):			# Add every element of String to the stack
		new = compExpr.pop(0)
		stack.append(new)   
	
	errVal = checkExpression(stack,"Comparison",lineNumber)
	if errVal == False: return errVal															# If it's false, moves on to error

	while flag == True:
		
		iters += 1

		if iters > 1000:
			printError("Invalid Operand in Arithmetic Expression",lineNumber)
			return False

		if len(stack) == 1:			 # Only final answer should be left 
			flag = False
			finalAnswer = stack.pop(0)
			return finalAnswer

		hasError = checkStackExpr(stack,"Comparison",lineNumber)

		if hasError == True : return False											  # Exit if there is an error detected 

		for i in range(len(stack)-1):									   # Len of Stack Refreshes after every iteration
			char = stack[i] 

			if char == "AN":
				anIndex = i
				try:
					#print("AN Index: ",anIndex)
					ops = stack[anIndex-2]				  					 # Operation, 2 steps behind AN
					op1 = str(stack[anIndex-1])								  # Operand 1, 1 step behind AN
					op2 = str(stack[anIndex+1])								  # Operand 2, 1 step ahead AN 

					op1 = str(evaluateIfVar(op1))									 # Checks if the Operands are Possible Variables  
					op2 = str(evaluateIfVar(op2))									 # then evaluates them to their value in string 

					
					if (ops in compOpsList) and not(op1 in compOpsList) and not(op2 in compOpsList):
						answer = evaluateCompExpr(ops,op1,op2,lineNumber)
						for j in range(3): stack.pop(anIndex-2)				  		# Pop the Stack 3 times: Operation, OP1 , AN 
						stack[anIndex-2] = str(answer)								# Replace OP2 with the answer
						break													 	# Break Iteration after an operation has completed 
					else:
						pass
				except:
					print(stack)
					printError("Error in Comparison Expression",lineNumber)
			