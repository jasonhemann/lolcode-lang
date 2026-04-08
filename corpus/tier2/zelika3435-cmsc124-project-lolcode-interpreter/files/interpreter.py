class Noob:
	def __str__(self):
		return "NOOB"
	def __repr__(self):
		return "NOOB"
	def __bool__(self):
		return False

class GTFOError(Exception):
	pass

class ReturnError(Exception):
	def __init__(self, value):
		self.value = value
	
NOOB_VAL = Noob()

class Interpreter:
	def __init__(self, output_func=print, input_func=input, var_update_callback=None):
		self.variables = {} # symbol table
		self.variables['IT'] = NOOB_VAL
		self.functions = {}
		
		self.input_func = input_func
		self.output_func = output_func
		self.var_update_callback = var_update_callback  # Callback for real-time symbol table updates
	
	def visit(self, node):
		if node is None:
			return None
		method_name = 'visit_' + type(node).__name__
		visitor = getattr(self, method_name, self.generic_visit)

		return visitor(node)
	
	def generic_visit(self, node):
		raise Exception(f"No visit_{type(node).__name__} method")
	
	def visit_Program(self, node):
		for decl in node.declarations:
			self.visit(decl)

		for stmt in node.statements:
			val = self.visit(stmt)

			if val is not None:
				self.variables['IT'] = val
				if self.var_update_callback:
					self.var_update_callback(self.variables.copy())
		
	def visit_VarDecl(self, node):
		val = NOOB_VAL
		if node.expr:
			val = self.visit(node.expr)
		
		self.variables[node.var_name] = val
		if self.var_update_callback:
			self.var_update_callback(self.variables.copy())
	
	def visit_Assignment(self, node):
		if node.var_name not in self.variables:
			raise NameError(f"Runtime Error: Variable '{node.var_name}' used but is not declared in WAZZUP")
		
		val = self.visit(node.expr)
		self.variables[node.var_name] = val
		if self.var_update_callback:
			self.var_update_callback(self.variables.copy())
	
	def visit_Visible(self, node):
		output = ""
		for expr in node.exprs:
			val = self.visit(expr)
			
			if val is NOOB_VAL:
				output += "NOOB"
			else:
				output += self.cast_value(val, 'YARN')
		
		self.output_func(output + "\n")
	
	def visit_Literal(self, node):
		return node.value
	
	def visit_Variable(self, node):
		name = node.name

		if name in self.variables:
			return self.variables[name]
		else:
			raise NameError(f"Runtime Error: Variable '{name}' is not defined")
		
	def visit_BinOp(self, node):
		left_raw = self.visit(node.left)
		right_raw = self.visit(node.right)

		if node.op == 'BOTH_SAEM':
			if type(left_raw) != type(right_raw):
				return False
			return left_raw == right_raw
		elif node.op == 'DIFFRINT':
			if type(left_raw) != type(right_raw):
				return True
			return left_raw != right_raw
		
		if node.op == 'BOTH_OF':
			return self.cast_value(left_raw, 'TROOF') and self.cast_value(right_raw, 'TROOF')
		elif node.op == 'EITHER_OF':
			return self.cast_value(left_raw, 'TROOF') or self.cast_value(right_raw, 'TROOF')
		elif node.op == 'WON_OF':
			return self.cast_value(left_raw, 'TROOF') != self.cast_value(right_raw, 'TROOF')

		left = self.to_number(left_raw)
		right = self.to_number(right_raw)
		is_numbar = isinstance(left, float) or isinstance(right, float)
		result = 0

		if node.op == 'SUM_OF': result = left+right
		elif node.op == 'DIFF_OF': result = left-right
		elif node.op == 'PRODUKT_OF': result = left*right
		elif node.op == 'QUOSHUNT_OF':
			if right == 0:
				raise ZeroDivisionError("Runtime Error: Division by Zero")
			if not is_numbar:
				result = left // right
			else:
				result = left/right
		elif node.op == 'MOD_OF':
			if right == 0: raise ZeroDivisionError("Runtime Error: Modulo by Zero")
			result = left%right
		elif node.op == 'BIGGR_OF': result = max(left, right)
		elif node.op == 'SMALLR_OF': result = min(left, right)

		if is_numbar:
			return float(result)
		else:
			return int(result)
	
	def visit_UnaryOp(self, node):
		if node.op == 'NOT':
			val = self.visit(node.expr)

			bool_val = self.cast_value(val, 'TROOF')
			return not bool_val
		
	def visit_AllOf(self, node):
		for expr in node.exprs:
			val = self.visit(expr)
			if not self.cast_value(val, 'TROOF'):
				return False
		return True
	
	def visit_AnyOf(self, node):
		for expr in node.exprs:
			val = self.visit(expr)
			if self.cast_value(val, 'TROOF'):
				return True
		return False
	
	def visit_Smoosh(self, node):
		result = ""
		for expr in node.exprs:
			val = self.visit(expr)
			result += self.cast_value(val, 'YARN')
		
		return result
	
	def visit_Gimmeh(self, node):
		if node.var_name not in self.variables:
			raise NameError(f"Runtime Error: Cannot GIMMEH '{node.var_name}' because it was not declared in WAZZUP")
		
		user_input = self.input_func()
		self.variables[node.var_name] = user_input
		if self.var_update_callback:
			self.var_update_callback(self.variables.copy())
	
	def cast_value(self, val, target_type):
		if val is NOOB_VAL:
			if target_type == 'TROOF': return False
			elif target_type == 'NUMBR': return 0
			elif target_type == 'NUMBAR': return 0.0
			elif target_type == 'YARN': return ""
			return 0
		
		if target_type == 'TROOF':
			if val == "" or val == 0 or val == 0.0 or val == False:
				return False
			return True
		
		if target_type == 'NUMBR':
			if val is True: return 1
			if val is False: return 0
			if isinstance(val, float): return int(val)
			if isinstance(val, str):
				try:
					return int(val)
				except:
					raise ValueError(f"Cannot cast YARN '{val}' to NUMBR")
			return int(val)
		
		if target_type == 'NUMBAR':
			if val is True: return 1.0
			if val is False: return 0.0
			if isinstance(val, str):
				try:
					return float(val)
				except:
					raise ValueError(f"Cannot cast YARN '{val}' to NUMBAR")
			return float(val)
		
		if target_type == 'YARN':
			if val is True: return "WIN"
			if val is False: return "FAIL"
			if isinstance(val, float): return f"{val:.2f}"
			return str(val)
		
		if target_type == 'NOOB':
			return NOOB_VAL
		
		raise TypeError(f"Unknown type: {target_type}")
	
	def to_number(self, val):
		if val is NOOB_VAL:
			raise TypeError("Runtime Error: Cannot implicitly cast NOOB to NUMBR/NUMBAR")
		
		if isinstance(val, int) or isinstance(val, float):
			return val
		
		if isinstance(val, bool):
			return 1 if val else 0
		
		if isinstance(val, str):
			try:
				return int(val)
			except ValueError:
				try:
					return float(val)
				except ValueError:
					raise ValueError(f"Runtime Error: Cannot implicitly cast YARN to NUMBR/NUMBAR")
		
		raise TypeError(f"Runtime Error: Invalid type for math operation: {type(val)}")

	def visit_Maek(self, node):
		val = self.visit(node.expr)

		return self.cast_value(val, node.target_type)
	
	def visit_IsNowA(self, node):
		if node.var_name not in self.variables:
			raise NameError(f"Variable '{node.var_name}' not defined")
		
		current_val = self.variables[node.var_name]

		new_val = self.cast_value(current_val, node.target_type)

		self.variables[node.var_name] = new_val
		if self.var_update_callback:
			self.var_update_callback(self.variables.copy())
	
	def visit_IfStatement(self, node):
		it_val = self.variables.get('IT', NOOB_VAL)
		if self.cast_value(it_val, 'TROOF'):
			for stmt in node.true_statements:
				val = self.visit(stmt)
				if val is not None: self.variables['IT'] = val
			return
		
		for condition_node, statements in node.elif_blocks:
			cond_val = self.visit(condition_node)

			self.variables['IT'] = cond_val

			if self.cast_value(cond_val, 'TROOF'):
				for stmt in statements:
					val = self.visit(stmt)
					if val is not None: self.variables['IT'] = val
				return
		
		for stmt in node.false_statements:
			val = self.visit(stmt)
			if val is not None: self.variables['IT'] = val
	
	def visit_GTFO(self, node):
		raise GTFOError()
	
	def visit_SwitchStatement(self, node):
		it_val = self.variables.get('IT', NOOB_VAL)

		fallthrough = False
		match_found_any = False

		try:
			for case in node.cases:
				case_literal = self.visit(case.value)

				if fallthrough or case_literal == it_val:
					match_found_any = True
					fallthrough = True

					for stmt in case.statements:
						val = self.visit(stmt)
						if val is not None: self.variables['IT'] = val
			
			if fallthrough or not match_found_any:
				for stmt in node.default_statements:
					val = self.visit(stmt)
					if val is not None: self.variables['IT'] = val
		
		except GTFOError:
			pass
	
	def visit_Loop(self, node):
		try:
			while True:
				if node.cond_type:
					cond_val = self.visit(node.cond_expr)
					bool_val = self.cast_value(cond_val, 'TROOF')

					if node.cond_type == 'TIL' and bool_val:
						break
					elif node.cond_type == 'WILE' and not bool_val:
						break
				
				try:
					for stmt in node.statements:
						val = self.visit(stmt)
						if val is not None: self.variables['IT'] = val
				except GTFOError:
					break

				curr_val = self.variables.get(node.var, NOOB_VAL)
				curr_num = self.to_number(curr_val)

				if node.op == 'UPPIN':
					curr_num += 1
				elif node.op == 'NERFIN':
					curr_num -= 1
				
				self.variables[node.var] = curr_num
				if self.var_update_callback:
					self.var_update_callback(self.variables.copy())
		except GTFOError:
			pass	
	
	def visit_FunctionDef(self, node):
		self.functions[node.name] = node
	
	def visit_Return(self, node):
		val = self.visit(node.expr)
		raise ReturnError(val)
	
	def visit_FunctionCall(self, node):
		func_name = node.name

		if func_name not in self.functions:
			raise NameError(f"Runtime Error: Function '{func_name}' is not defined")
		
		func_def = self.functions[func_name]

		if len(node.args) != len(func_def.params):
			raise TypeError(f"Function '{func_name}' expects {len(func_def.params)} arguments, got {len(node.args)} instead")
		
		arg_values = []
		for arg in node.args:
			arg_values.append(self.visit(arg))

		# save current global scope
		previous_variables = self.variables

		# create new fresh scope
		self.variables = {'IT': NOOB_VAL}

		for param, value in zip(func_def.params, arg_values):
			self.variables[param] = value
		
		return_val = NOOB_VAL # default return type
		try:
			for stmt in func_def.body:
				val = self.visit(stmt)
				if val is not None: self.variables['IT'] = val
		except ReturnError as e:
			return_val = e.value
		except GTFOError:
			return_val = NOOB_VAL
		finally:
			# restore scope
			self.variables = previous_variables

		self.variables['IT'] = return_val
		if self.var_update_callback:
			self.var_update_callback(self.variables.copy())
		return return_val
