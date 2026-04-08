import lol_ast as ast

class Parser:
	def __init__(self, tokens):
		self.tokens = list(tokens)
		self.pos = 0
		self.current_token = self.tokens[self.pos] if self.tokens else None

	def advance(self):
		self.pos += 1

		if self.pos < len(self.tokens):
			self.current_token = self.tokens[self.pos]
		else:
			self.current_token = ('EOF', None)
	
	def eat(self, token_type):
		if self.current_token[0] == token_type:
			self.advance()
		else:
			raise SyntaxError(f"Expected {token_type}, got {self.current_token[0]}")
	
	def parse_program(self):
		# consume all newlines
		while self.current_token[0] == 'NEWLINE':
			self.advance()

		# parse main code block
		self.eat('HAI')
		
		while self.current_token[0] == 'NEWLINE':
			self.advance()
		
		# parse the variable declarations (if any)
		declarations = []
		if self.current_token[0] == 'WAZZUP':
			declarations = self.parse_wazzup_block()

		statements = []
		while self.current_token[0] != 'KTHXBYE' and self.current_token[0] != 'EOF':
			stmt = self.parse_statement()
			if stmt:
				statements.append(stmt)
		
		self.eat('KTHXBYE')

		# consume all newlines
		while self.current_token[0] == 'NEWLINE':
			self.advance()
		
		return ast.Program(declarations, statements)
	
	def parse_wazzup_block(self):
		self.eat('WAZZUP')
		decls = []

		while self.current_token[0] != 'BUHBYE':
			if self.current_token[0] == 'I_HAS_A':
				decls.append(self.parse_var_decl())
			elif self.current_token[0] == 'NEWLINE':
				self.advance()
			elif self.current_token[0] == 'EOF':
				raise SyntaxError("Expected BUHBYE, found EOF")
			else:
				raise SyntaxError(f"Only variable declarations in WAZZUP. Found {self.current_token[0]}")

		self.eat('BUHBYE')
		return decls
	
	def parse_statement(self):
		token_type = self.current_token[0]

		if token_type == 'NEWLINE':
			self.advance()
			return None
		elif token_type == 'I_HAS_A':
			raise SyntaxError("Variables must be declared in WAZZUP block")
		elif token_type == 'IDENTIFIER':
			next_pos = self.pos + 1
			next_token_type = self.tokens[next_pos][0] if next_pos < len(self.tokens) else None

			if next_token_type in ('R', 'IS_NOW_A'):
				return self.parse_var_change()
			else:
				return self.parse_expression()
		elif token_type in ('NUMBR_LITERAL', 'NUMBAR_LITERAL', 'YARN_LITERAL', 'TROOF_LITERAL', 'TYPE_LITERAL'):
			return self.parse_expression()
		elif token_type == 'VISIBLE':
			return self.parse_visible()
		elif token_type == 'GIMMEH':
			return self.parse_gimmeh()
		elif token_type == 'MAEK':
			return self.parse_expression()
		elif token_type == 'SMOOSH':
			return self.parse_expression()
		elif token_type in ('SUM_OF', 'DIFF_OF', 'PRODUKT_OF', 'QUOSHUNT_OF', 'MOD_OF', 'BIGGR_OF', 'SMALLR_OF'):
			return self.parse_expression()
		elif token_type in ('BOTH_OF', 'EITHER_OF', 'WON_OF', 'NOT', 'ALL_OF', 'ANY_OF'):
			return self.parse_expression()
		elif token_type in ('BOTH_SAEM', 'DIFFRINT'):
			return self.parse_expression()
		elif token_type == 'O_RLY':
			return self.parse_if_statement()
		elif token_type == 'WTF':
			return self.parse_switch_statement()
		elif token_type == 'GTFO':
			self.eat('GTFO')
			return ast.GTFO()
		elif token_type == 'IM_IN_YR':
			return self.parse_loop()
		elif token_type == 'HOW_IZ_I':
			return self.parse_function_def()
		elif token_type == 'I_IZ':
			return self.parse_function_call()
		elif token_type == 'FOUND_YR':
			return self.parse_return()
		else:
			if token_type != 'EOF':
				self.advance()
			return None
		
	def parse_gimmeh(self):
		"""GIMMEH <var>"""
		self.eat('GIMMEH')

		var_name = self.current_token[1]
		self.eat('IDENTIFIER')

		return ast.Gimmeh(var_name)
	
	def parse_var_change(self):
		"""<var> R <expr> or <var> IS NOW A <type>"""
		var_name = self.current_token[1]
		self.eat('IDENTIFIER')

		if self.current_token[0] == 'R':
			self.eat('R')
			expr = self.parse_expression()
			return ast.Assignment(var_name, expr)
		
		elif self.current_token[0] == 'IS_NOW_A':
			self.eat('IS_NOW_A')
			target_type = self.current_token[1]
			self.eat('TYPE_LITERAL')
			return ast.IsNowA(var_name, target_type)
		
		else:
			raise SyntaxError(f"Expected 'R' or 'IS NOW A' after variable '{var_name}'")
	
	def parse_var_decl(self):
		"""I HAS A <var> [ITZ <expr>]"""
		self.eat('I_HAS_A')
		var_name = self.current_token[1]
		self.eat('IDENTIFIER')

		init_expr = None
		if self.current_token[0] == 'ITZ':
			self.eat('ITZ')
			init_expr = self.parse_expression()
		
		return ast.VarDecl(var_name, init_expr)
	
	def parse_visible(self):
		"""VISIBLE <expr> [+ <expr>]*"""
		self.eat('VISIBLE')
		exprs = [self.parse_expression()]

		while self.current_token[0] == 'PLUS':
			self.eat('PLUS')
			exprs.append(self.parse_expression())

		return ast.Visible(exprs)
	
	def parse_expression(self):
		token_type = self.current_token[0]

		# Binary Ops
		if token_type in ('SUM_OF', 'DIFF_OF', 'PRODUKT_OF', 'QUOSHUNT_OF', 'MOD_OF', 'BIGGR_OF', 'SMALLR_OF', 'BOTH_OF', 'EITHER_OF', 'WON_OF', 'BOTH_SAEM', 'DIFFRINT'):
			op = token_type
			self.eat(token_type)
			left = self.parse_expression()
			self.eat('AN')
			right = self.parse_expression()
			return ast.BinOp(op, left, right)
		
		# Unary Op
		elif token_type == 'NOT':
			self.eat('NOT')
			expr = self.parse_expression()
			return ast.UnaryOp('NOT', expr)
		
		# Infinite Arity
		elif token_type in ('ALL_OF', 'ANY_OF'):
			parent_op = token_type
			is_all = (token_type == 'ALL_OF')
			self.eat(token_type)
			exprs = []

			while self.current_token[0] not in ('MKAY', 'NEWLINE', 'EOF'):
				if self.current_token[0] in ('ALL_OF', 'ANY_OF'):
					raise SyntaxError(f"Syntax Error: Nesting '{self.current_token[0]}' inside '{parent_op}' is not allowed")
				
				exprs.append(self.parse_expression())
				if self.current_token[0] == 'AN':
					self.eat('AN')
				
			if self.current_token[0] == 'MKAY':
				self.eat('MKAY')
			
			return ast.AllOf(exprs) if is_all else ast.AnyOf(exprs)

		elif token_type == 'SMOOSH':
			self.eat('SMOOSH')
			exprs = []

			while self.current_token[0] not in ('MKAY', 'NEWLINE', 'EOF'):
				exprs.append(self.parse_expression())

				if self.current_token[0] == 'AN':
					self.eat('AN')
			
			if self.current_token[0] == 'MKAY':
				self.eat('MKAY')

			return ast.Smoosh(exprs)
		
		elif token_type == 'MAEK':
			self.eat('MAEK')
			expr = self.parse_expression()

			if self.current_token[0] == 'A':
				self.eat('A')
			
			target_type = self.current_token[1]
			self.eat('TYPE_LITERAL')

			return ast.Maek(expr, target_type)
		
		elif token_type == 'I_IZ':
			return self.parse_function_call()
		
		elif token_type == 'TROOF_LITERAL':
			val = (self.current_token[1] == 'WIN')
			self.eat('TROOF_LITERAL')
			return ast.Literal(val, 'TROOF')
		
		elif token_type == 'TYPE_LITERAL':
			val = self.current_token[1]
			self.eat('TYPE_LITERAL')
			return ast.Literal(val, 'TYPE')
		
		elif token_type == 'NUMBR_LITERAL':
			val = int(self.current_token[1])
			self.eat('NUMBR_LITERAL')
			return ast.Literal(val, 'NUMBR') 

		elif token_type == 'NUMBAR_LITERAL':
			val = float(self.current_token[1])
			self.eat('NUMBAR_LITERAL')
			return ast.Literal(val, 'NUMBAR')
		
		elif token_type == 'YARN_LITERAL':
			val = self.current_token[1].strip('"“”')
			self.eat('YARN_LITERAL')
			return ast.Literal(val, 'YARN')
		
		elif token_type == 'IDENTIFIER':
			var_name = self.current_token[1]
			self.eat('IDENTIFIER')
			return ast.Variable(var_name)
		
		else:
			raise SyntaxError(f"Unexpected token in expression: {token_type}")
	
	def parse_if_statement(self):
		"""
		O RLY?
			YA RLY
				<code block>
			MEBBE <expr>
				<code block>
			NO WAI
				<code block>
		OIC
		"""
		self.eat('O_RLY')
		self.eat('NEWLINE')
		self.eat('YA_RLY')
		self.eat('NEWLINE')

		true_statements = []
		while self.current_token[0] not in ('MEBBE', 'NO_WAI', 'OIC', 'EOF'):
			stmt = self.parse_statement()
			if stmt: true_statements.append(stmt)
		
		elif_blocks = []
		while self.current_token[0] == 'MEBBE':
			self.eat('MEBBE')

			condition = self.parse_expression()
			self.eat('NEWLINE')

			mebbe_statements = []
			while self.current_token[0] not in ('MEBBE', 'NO_WAI', 'OIC', 'EOF'):
				stmt = self.parse_statement()
				if stmt: mebbe_statements.append(stmt)

			elif_blocks.append((condition, mebbe_statements))
		
		false_statements = []
		if self.current_token[0] == 'NO_WAI':
			self.eat('NO_WAI')
			self.eat('NEWLINE')

			while self.current_token[0] not in ('OIC', 'EOF'):
				stmt = self.parse_statement()
				if stmt: false_statements.append(stmt)
		
		self.eat('OIC')
		return ast.IfStatement(true_statements, elif_blocks, false_statements)
	
	def parse_switch_statement(self):
		"""
		WTF?
		OMG <literal>
			<statements>
		[OMG <literal>
			<statements>]
		[OMGWTF
			<statements>]
		"""
		self.eat('WTF')
		self.eat('NEWLINE')

		cases = []

		while self.current_token[0] == 'OMG':
			self.eat('OMG')

			value_node = None
			if self.current_token[0] in ('NUMBR_LITERAL', 'NUMBAR_LITERAL', 'YARN_LITERAL', 'TROOF_LITERAL', 'TYPE_LITERAL'):
				value_node = self.parse_expression()
			else:
				raise SyntaxError("Expected literal value after OMG")

			self.eat('NEWLINE')

			case_stmts = []
			while self.current_token[0] not in ('OMG', 'OMGWTF', 'OIC', 'EOF'):
				stmt = self.parse_statement()
				if stmt: case_stmts.append(stmt)
			
			cases.append(ast.Case(value_node, case_stmts))
		
		default_stmts = []
		if self.current_token[0] == 'OMGWTF':
			self.eat('OMGWTF')
			self.eat('NEWLINE')

			while self.current_token[0] not in ('OIC', 'EOF'):
				stmt = self.parse_statement()
				if stmt: default_stmts.append(stmt)
		
		self.eat('OIC')
		return ast.SwitchStatement(cases, default_stmts)
	
	def parse_loop(self):
		"""
		IM IN YR <label> <op> YR <var> [TIL|WILE <expr>]
			<statements>
		IM OUTTA YR <label>
		"""
		self.eat('IM_IN_YR')
		label = self.current_token[1]
		self.eat('IDENTIFIER')

		op = self.current_token[0]
		if op not in ('UPPIN', 'NERFIN'):
			raise SyntaxError(f"Expected UPPIN or NERFIN in loop, got {op}")
		self.eat(op)

		self.eat('YR')
		var_name = self.current_token[1]
		self.eat('IDENTIFIER')

		cond_type = None
		cond_expr = None
		if self.current_token[0] in ('TIL', 'WILE'):
			cond_type = self.current_token[0]
			self.eat(cond_type)
			cond_expr = self.parse_expression()

		self.eat('NEWLINE')

		statements = []
		while self.current_token[0] != 'IM_OUTTA_YR':
			if self.current_token[0] == 'EOF':
				raise SyntaxError("Unexpected EOF inside loop (Did you forget IM OUTTA YR?)")

			stmt = self.parse_statement()
			if stmt: statements.append(stmt)

		self.eat('IM_OUTTA_YR')
		end_label = self.current_token[1]
		self.eat('IDENTIFIER')

		if label != end_label:
			raise SyntaxError(f"Loop Label Mismatch: Started '{label}', Ended '{end_label}'")
		
		return ast.Loop(label, op, var_name, cond_type, cond_expr, statements)
	
	def parse_function_def(self):
		"""
		HOW IZ I <name> [YR <param> [AN YR <param> ...]]
			<body>
		IF YOU SAY SO
		"""
		self.eat('HOW_IZ_I')
		func_name = self.current_token[1]
		self.eat('IDENTIFIER')

		params = []
		if self.current_token[0] == 'YR':
			self.eat('YR')
			params.append(self.current_token[1])
			self.eat('IDENTIFIER')

			while self.current_token[0] == 'AN':
				self.eat('AN')
				self.eat('YR')
				params.append(self.current_token[1])
				self.eat('IDENTIFIER')
		self.eat('NEWLINE')

		body = []
		while self.current_token[0] != 'IF_U_SAY_SO':
			if self.current_token[0] == 'EOF':
				raise SyntaxError("Unexpected EOF inside function. Expected IF YOU SAY SO")
			
			stmt = self.parse_statement()
			if stmt: body.append(stmt)
		
		self.eat('IF_U_SAY_SO')
		return ast.FunctionDef(func_name, params, body)
	
	def parse_function_call(self):
		"""
		I IZ <name> [YR <arg> [AN YR <arg> ...]] MKAY
		"""
		self.eat('I_IZ')
		func_name = self.current_token[1]
		self.eat('IDENTIFIER')

		args = []
		if self.current_token[0] == 'YR':
			self.eat('YR')
			args.append(self.parse_expression())

			while self.current_token[0] == 'AN':
				self.eat('AN')
				self.eat('YR')
				args.append(self.parse_expression())
		self.eat('MKAY')

		return ast.FunctionCall(func_name, args)
	
	def parse_return(self):
		"""FOUND YR <expr>"""
		self.eat('FOUND_YR')
		expr = self.parse_expression()

		return ast.Return(expr)
