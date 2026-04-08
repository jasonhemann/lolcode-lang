def check_syntax(console):
# 	#Assumptions
# 	#No version number
# 	#One line has one statement
# 	#One whitespace between keywords

# 	#Variables
# 	line_no = 1
# 	program_start = False
# 	program_end = False
# 	line_start = True
# 	line_end = False
# 	func_start = False
# 	func_end = False
# 	comment_start = False
# 	comment_end = False
# 	string_start = False
# 	string_end = False
# 	# varclause_start = False
# 	# varclause_end = False
# 	prev_keyword = ""

# 	for i in range(len(lex_keys)):
# 		if lex_keys[i] == "<linebreak>":
# 			line_no += 1
# 			continue
# 		elif lex_keys[i] == "HAI" and not program_start:
# 			if i == 0 and lex_keys[i+1] in ["<linebreak>", "BTW"]:
# 				program_start = True
# 				prev_keyword = "HAI"
# 				continue
# 			elif lex_keys[i-1] == "<linebreak>" and lex_keys[i+1] in ["<linebreak>", "BTW"]:
# 				program_start = True
# 				prev_keyword = "HAI"
# 				continue
# 		elif lex_keys[i] == "HAI" and program_start and not string_start:
# 			return console.insert(tk.END, "Line {}: SyntaxError: Expected statement after start of program\n".format(line_no))
# 		elif lex_keys[i] == "KTHXBYE" and not program_end:
# 			if lex_keys[i-1] == "<linebreak>" and lex_keys[i+1] in ["<linebreak>", "BTW"]:
# 				program_end = True
# 				prev_keyword = "KTHXBYE"
# 				continue
# 		elif lex_keys[i] == "KTHXBYE" and program_end and not string_start:
# 			return console.insert(tk.END, "Line {}: SyntaxError: Expected comment/function after end of program\n".format(line_no))
		
# 		#Add functions later for before and after program
# 		if not program_start and lex_keys[i] not in ["BTW", "OBTW", "TLDR", "<linebreak>"]:
# 			# print(lex_keys[i], " ANO YUN")
# 			return console.insert(tk.END, "Line {}: SyntaxError: Illegal statement before start of program\n".format(line_no))
# 		elif program_end and lex_keys[i] not in ["BTW", "OBTW", "TLDR", "<linebreak>"]:
# 			return console.insert(tk.END, "Line {}: SyntaxError: Illegal statement after end of program\n".format(line_no))
		
# 		#Check OBTW and TLDR pairs and validity
# 		if lex_keys[i] == "OBTW":
# 			if i == 0 or lex_keys[i-1] == "<linebreak>":
# 				comment_start = True
# 				comment_end = False
# 				continue
# 			else:
# 				return console.insert(tk.END, "Line {}: SyntaxError: Illegal comment\n".format(line_no))
# 		elif lex_keys[i] == "TLDR":
# 			if not comment_start:
# 				return console.insert(tk.END, "Line {}: SyntaxError: Illegal expression\n".format(line_no))
		
# 			if lex_keys[i+1] == "<linebreak>":
# 				comment_end = True
# 				comment_start = False
# 				continue
# 			else:
# 				return console.insert(tk.END, "Line {}: SyntaxError: Illegal comment\n".format(line_no))

# 		# #Check if WAZZUP-BUHBYE clause comes after HAI
# 		# if lex_keys[i] == "WAZZUP":
# 		# 	if lex_keys[i-1] == "<linebreak>" and prev_keyword == "HAI" :
# 		# 		varclause_start = True
# 		# 		continue
# 		# 	else:
# 		# 		return console.insert(tk.END, "Line {}: SyntaxError: Illegal comment\n".format(line_no))
# 		# elif lex_keys[i] == "BUHBYE":
# 		# 	if not comment_start:
# 		# 		return console.insert(tk.END, "Line {}: SyntaxError: Illegal expression\n".format(line_no))
		
# 		# 	if lex_keys[i+1] == "<linebreak>":
# 		# 		comment_end = True
# 		# 		comment_start = False
# 		# 		continue
# 		# 	else:
# 		# 		return console.insert(tk.END, "Line {}: SyntaxError: Illegal comment\n".format(line_no))

# 		#Variables
# 		if lex_keys[i] == "I HAS A":
# 			prev_keyword = "I HAS A"
# 			if lex_words[lex_keys[i+1]] != "Variable/Loop/Function Identifier":
# 				return console.insert(tk.END, "Line {}: SyntaxError: Invalid variable name\n".format(line_no))
# 		elif lex_keys[i] == "ITZ":
# 			if prev_keyword != "I HAS A":
# 				return console.insert(tk.END, "Line {}: SyntaxError: Illegal use of ITZ\n".format(line_no))
# 			#Add expression after ITZ
# 			elif lex_words[lex_keys[i+1]] not in ["Variable/Loop/Function Identifier", "Literal"] and lex_keys[i+2] not in ["<linebreak>", "BTW"]:
# 				return console.insert(tk.END, "Line {}: SyntaxError: Invalid variable initialization\n".format(line_no))

# 		#Input/Output
# 		if lex_keys[i] == "GIMMEH":
# 			prev_keyword = "GIMMEH"
# 			if lex_words[lex_keys[i+1]] != "Variable/Loop/Function Identifier":
# 				return console.insert(tk.END, "Line {}: SyntaxError: Invalid variable name\n".format(line_no))
# 			elif lex_keys[i+2] not in ["<linebreak>", "BTW"]:
# 				return console.insert(tk.END, "Line {}: SyntaxError: Invalid statement\n".format(line_no))
			
# 		#Add multiple inputs later
# 		elif lex_keys[i] == "VISIBLE":
# 			prev_keyword = "VISIBLE"
# 			if lex_words[lex_keys[i+1]] == "\"" and lex_words[lex_keys[i+3]] == "\"" and lex_keys[i+4] not in ["<linebreak>", "BTW"]:
# 				return console.insert(tk.END, "Line {}: SyntaxError: Invalid statement\n".format(line_no))
# 			elif lex_words[lex_keys[i+1]] not in ["Variable/Loop/Function Identifier", "Literal"]:
# 				return console.insert(tk.END, "Line {}: SyntaxError: Invalid variable name\n".format(line_no))
		

# 	#Check if HAI and KTHXBYE exist
# 	if not program_start:
# 		return console.insert(tk.END, "Line {}: SyntaxError: Expected start of program\n".format(line_no-1))
# 	elif not program_end:
# 		return console.insert(tk.END, "Line {}: SyntaxError: Expected end of program\n".format(line_no-1))
# 	#Check if all comments were closed
# 	if comment_start and not comment_end:
# 		return console.insert(tk.END, "Line {}: SyntaxError: Illegal comment\n".format(line_no-1))

# 	console.config(state = "disabled")