from helperFuncs import *

## Functions for Boolean Expressions 

def isBoolOperand(x):
	if re.match(troofIdentifier,x):
		return True
	else:
		return False

def manageBoolKeywords(line):
	keywordListTuple = [("BOTH OF","BOTHOF"),("EITHER OF","EITHEROF"),("WON OF","WONOF"),("ANY OF","ANYOF"),("ALL OF","ALLOF")]
	for keyword in keywordListTuple:
		line = line.replace(keyword[0],keyword[1])
	line = line.split()
	return line

def evaluateBoolExpr(operator,operand1,operand2,lineNumber):

	print("Operator: ",operator," Op1: ",operand1," Op2: ",operand2)

	if operand1 == "WIN": operand1 = True				# Cast to Boolean Type to take advantage of pythhon operations
	elif operand1 == "FAIL": operand1 = False

	if operand2 == "WIN": operand2 = True				
	elif operand2 == "FAIL": operand2 = False

	if operator == "BOTHOF":
		answer = operand1 and operand2
	elif operator == "EITHEROF":
		answer = operand1 or operand2
	elif operator == "WONOF":               # XOR is similar to !=
		if operand1 != operand2: answer = True
		else: answer = False
	else:
		printError("Unrecognized boolean operator",lineNumber)
		return False
	
	if answer == True: answer = "WIN"
	elif answer == False: answer = "FAIL"

	return answer

def mainBool(boolExpr,lineNumber):
	flag = True
	stack = []							    # Stack used for computation
	iters = 0 
										
	inputLength = len(boolExpr)

	for i in range(inputLength):									      # Add every element of String to the stack
		new = boolExpr.pop(0)
		stack.append(new)   
	
	#checkExpression(stack,"Boolean")
	while flag == True:

		iters += 1
		
		if iters > 1000:
			printError("Invalid Operand in Arithmetic Expression",lineNumber)
			return False

		if len(stack) == 1:                                               # Only final answer should be left 
			flag = False
			finalAnswer = stack.pop(0)
			return finalAnswer
		
		hasError = checkStackExpr(stack,"Boolean",lineNumber)
		if hasError == True : 									  		# Exit if there is an error detected 
			printError("Error in Boolean Expression",lineNumber)
			return False

		for i in range(len(stack)-1):                                     # Len of Stack Refreshes after every iteration
			char = stack[i] 
			print(stack)
			if char == "NOT" :                                             # Not of is separated because it only has 1 operand 
				valid = True
				try:
					ops = stack[i]
					op1 = stack[i+1]
					op1 = evaluateIfVar(op1)									 # Checks if the Operands are Possible Variables  

					# Evaluate op1 if variable 
					print("Ops: ",ops," Op1: ",op1)

					if isBoolOperand(op1) and op1 == "WIN":	
						answer = "FAIL"
					elif isBoolOperand(op1) and op1 == "FAIL": 
						answer = "WIN"
					else : 
						valid = False
						
					stack.pop(i)                                            # Pop the not of
					stack[i] = answer
					break
				except: 
					pass

				if valid == False: 
					printError("Invalid Not Operand",lineNumber)
					return False

			elif char == "ALLOF":                                           #  Infinite Arity And
				valid = True
				try:
					start = i
					ops = stack[i]
					end = False

					for m in stack: 										# Traverse the stack and find its matching MKAY
						if m == "MKAY": 
							end = stack.index(m)	
							break						
				
					if end != False:
						
						while stack[i+2] != "MKAY":
							operation = "BOTHOF"									# ALL OF is a reeated form of BOTH OF 
							op1 = str(stack[i+1])
							op2 = str(stack[i+3])

							op1 = evaluateIfVar(op1)									 # Checks if the Operands are Possible Variables  
							op2 = evaluateIfVar(op2)									 # then evaluates them to their value in string 

							if (operation in boolOpsList) and isBoolOperand(op1) and isBoolOperand(op2):
								answer = evaluateBoolExpr(operation,op1,op2,lineNumber)
								if answer == False: return False
								print("Answer: ",answer)
								for j in range(2): stack.pop(i+1)
								stack[i+1] = answer
								continue									
							elif op1 in boolOpsList or op2 in boolOpsList:				# Nested operands, exit to allow them to evaluate
								exit(1)
							else: 
								print("Failed to Evaluate Boolean: ",operation,op1,op2)
								pass
						
						stack.pop(i+2)				# pop MKAY
						stack.pop(i)				# pop ALL OF 
						break						# break out of outer loop to refresh count
						
					elif end == False: valid = False
				except:
					pass

				if valid == False: 
					printError("Error in All OF, matching MKAY not found.",lineNumber)
					return False

			elif char == "ANYOF":                                           	 # Infinite Arity Or
				valid = True													
				try:
					start = i
					ops = stack[i]
					end = False

					for m in stack: 										# Traverse the stack and find its matching MKAY
						if m == "MKAY": 
							end = stack.index(m)	
							break						
					
					if end != False:
						
						while stack[i+2] != "MKAY":
							ops = "EITHEROF"									# ANY OF is a reeated form of EITHER OF 
							op1 = str(stack[i+1])
							op2 = str(stack[i+3])

							op1 = evaluateIfVar(op1)									 # Checks if the Operands are Possible Variables  
							op2 = evaluateIfVar(op2)									 # then evaluates them to their value in string 
							
							if (ops in boolOpsList) and isBoolOperand(op1) and isBoolOperand(op2):
								answer = evaluateBoolExpr(ops,op1,op2,lineNumber)
								if answer == False: return False
								for j in range(2): stack.pop(i+1)
								stack[i+1] = answer
								continue									
							else: 
								pass
						
						stack.pop(i+2)				# pop MKAY
						stack.pop(i)				# pop ANY OF 
						print(stack)
						break						# break out of outer loop to refresh count
					
					elif end == False: valid = False
				except:
					pass

				if valid == False: 
					printError("Error in ANY OF, matching MKAY not found.",lineNumber)
					return False

			elif char == "AN":
				valid = True
				anIndex = i

				if stack.index(stack[i]) == 0 or stack.index(stack[i]) == 1: 
					valid = False
		
				try:
					print("AN Index: ",anIndex)
					ops = stack[anIndex-2]                  	                 # Operation, 2 steps behind AN
					op1 = str(stack[anIndex-1])                                  # Operand 1, 1 step behind AN
					op2 = str(stack[anIndex+1])                                  # Operand 2, 1 step ahead AN 

					op1 = str(evaluateIfVar(op1))									 # Checks if the Operands are Possible Variables  
					op2 = str(evaluateIfVar(op2))									 # then evaluates them to their value in string 
			
					if (ops in boolOpsList) and isBoolOperand(op1) and isBoolOperand(op2):
					
						answer = evaluateBoolExpr(ops,op1,op2,lineNumber)
						if answer == False: return False
						print("Answer: ",answer)
						for j in range(3): stack.pop(anIndex-2)                  # Pop the Stack 3 times: Operation, OP1 , AN 
						stack[anIndex-2] = str(answer)                                # Replace OP2 with the answer
						break									        		 # Break Iteration after an operation has completed 
					else:
						pass
				except: 
					pass

				if valid == False: 
					printError("Error incorrectly placed AN",lineNumber)
					return False
