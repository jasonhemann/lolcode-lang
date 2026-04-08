import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox, simpledialog
import os
import threading

# Import your modules
from lexer import lolcode_lexer
from parser import Parser
from interpreter import Interpreter

class LOLCodeInterpreterGUI:
	def __init__(self, root):
		self.root = root
		self.root.title("LOLCODE Interpreter")
		self.root.geometry("1400x900")
		self.root.minsize(1200, 700)
		self.root.protocol("WM_DELETE_WINDOW", self.on_close)
		
		self.current_file_path = None
		self.unsaved_changes = False
		self.file_path_var = tk.StringVar(value="(None)")
		
		# Real-time update variables
		self.token_update_job = None  # For debouncing token updates
		self.is_executing = False  # Track if code is executing
		
		self.setup_styles()
		self.create_widgets()

	def setup_styles(self):
		style = ttk.Style()
		style.theme_use('clam')
		
		style.configure('Execute.TButton', font=('Arial', 11, 'bold'))
		
		# Treeview headings
		style.configure("Treeview.Heading", font=('Arial', 10, 'bold'))
		style.configure("Treeview", font=('Arial', 10))

	def create_widgets(self):
		# Configure Main Grid
		# Row 0: Code & Data (High weight)
		# Row 1: Button (Low weight)
		# Row 2: Console (Medium weight)
		self.root.columnconfigure(0, weight=1)
		self.root.rowconfigure(0, weight=3) 
		self.root.rowconfigure(1, weight=0)
		self.root.rowconfigure(2, weight=1)

		# ============================================
		# ROW 0: WORKSPACE (Left: Editor, Right: Tables)
		# ============================================
		workspace_frame = ttk.Frame(self.root, padding="5")
		workspace_frame.grid(row=0, column=0, sticky="nsew")
		workspace_frame.columnconfigure(0, weight=2) # Editor gets 2/3 width
		workspace_frame.columnconfigure(1, weight=1) # Tables get 1/3 width
		workspace_frame.rowconfigure(0, weight=1)

		# --- LEFT PANEL: File Explorer (1) + Editor (2) ---
		left_panel = ttk.Frame(workspace_frame)
		left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
		left_panel.columnconfigure(0, weight=1)
		left_panel.rowconfigure(1, weight=1)

		# (1) File Explorer Bar (Top of Left Panel)
		file_frame = ttk.Frame(left_panel)
		file_frame.grid(row=0, column=0, sticky="ew", pady=(0, 5))
		
		ttk.Label(file_frame, text="File:").pack(side=tk.LEFT)
		self.file_entry = ttk.Entry(file_frame, textvariable=self.file_path_var, state='readonly')
		self.file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
		
		browse_btn = ttk.Button(file_frame, text="Browse", command=self.browse_file)
		browse_btn.pack(side=tk.LEFT)

		# (2) Text Editor (Main Body of Left Panel)
		self.code_editor = scrolledtext.ScrolledText(
			left_panel, wrap=tk.NONE, font=('Consolas', 11), undo=True
		)
		self.code_editor.grid(row=1, column=0, sticky="nsew")
		self.code_editor.bind("<<Modified>>", self.on_text_modified)
		# Bind key release for real-time token updates
		self.code_editor.bind("<KeyRelease>", self.on_text_changed)

		# --- RIGHT PANEL: Tokens (3) + Symbols (4) ---
		right_panel = ttk.Frame(workspace_frame)
		right_panel.grid(row=0, column=1, sticky="nsew")
		right_panel.columnconfigure(0, weight=1)
		right_panel.rowconfigure(0, weight=1) # Tokens get 50% height
		right_panel.rowconfigure(1, weight=1) # Symbols get 50% height

		# (3) Tokens Table (Top Half of Right Panel)
		tokens_frame = ttk.LabelFrame(right_panel, text="Lexemes / Tokens", padding=5)
		tokens_frame.grid(row=0, column=0, sticky="nsew", pady=(0, 5))
		
		self.lexemes_tree = ttk.Treeview(tokens_frame, columns=('Lexeme', 'Classification'), show='headings')
		self.lexemes_tree.heading('Lexeme', text='Lexeme')
		self.lexemes_tree.heading('Classification', text='Classification')
		self.lexemes_tree.column('Lexeme', width=80)
		self.lexemes_tree.column('Classification', width=120)
		
		lex_scroll = ttk.Scrollbar(tokens_frame, orient="vertical", command=self.lexemes_tree.yview)
		self.lexemes_tree.configure(yscrollcommand=lex_scroll.set)
		
		self.lexemes_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
		lex_scroll.pack(side=tk.RIGHT, fill=tk.Y)

		# (4) Symbol Table (Bottom Half of Right Panel)
		symbols_frame = ttk.LabelFrame(right_panel, text="Symbol Table", padding=5)
		symbols_frame.grid(row=1, column=0, sticky="nsew")

		self.symbol_tree = ttk.Treeview(symbols_frame, columns=('Identifier', 'Value'), show='headings')
		self.symbol_tree.heading('Identifier', text='Identifier')
		self.symbol_tree.heading('Value', text='Value')
		self.symbol_tree.column('Identifier', width=80)
		self.symbol_tree.column('Value', width=120)

		sym_scroll = ttk.Scrollbar(symbols_frame, orient="vertical", command=self.symbol_tree.yview)
		self.symbol_tree.configure(yscrollcommand=sym_scroll.set)

		self.symbol_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
		sym_scroll.pack(side=tk.RIGHT, fill=tk.Y)

		# ============================================
		# ROW 1: EXECUTE BUTTON (5)
		# ============================================
		# A large, distinct button separating Input from Output
		self.exec_btn = ttk.Button(
			self.root, 
			text="EXECUTE CODE", 
			style='Execute.TButton', 
			command=self.run_code
		)
		self.exec_btn.grid(row=1, column=0, sticky="ew", padx=10, pady=5)

		# ============================================
		# ROW 2: CONSOLE (6)
		# ============================================
		console_frame = ttk.LabelFrame(self.root, text="Console Output", padding=5)
		console_frame.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
		
		self.console_output = scrolledtext.ScrolledText(
			console_frame, 
			wrap=tk.WORD, 
			font=('Consolas', 10), 
			state='disabled',
			height=8,
			bg='#f0f0f0'
		)
		self.console_output.pack(fill=tk.BOTH, expand=True)

	# --- FILE HANDLING ---
	def browse_file(self):
		file_path = filedialog.askopenfilename(filetypes=[("LOLCODE", "*.lol"), ("All files", "*.*")])
		if file_path:
			# Clear tables when opening a new file
			self.clear_tables()
			
			self.current_file_path = file_path
			self.file_path_var.set(file_path)
			try:
				with open(file_path, 'r') as f:
					self.code_editor.delete(1.0, tk.END)
					self.code_editor.insert(tk.END, f.read())
				# Update tokens immediately after loading
				self.update_tokens_realtime()
			except Exception as e:
				messagebox.showerror("Error", f"Failed to open file: {e}")
		
		self.unsaved_changes = False
		self.code_editor.edit_modified(False)
		if file_path:
			self.root.title(f"LOLCODE INTERPRETER - {os.path.basename(file_path)}")
	
	def save_changes(self):
		target_path = self.current_file_path

		if not target_path:
			target_path = filedialog.asksaveasfilename(
				title="Save LOLCODE file",
				defaultextension=".lol",
				filetypes=[("LOLCODE files", "*.lol"), ("All files", "*.*")]
			)

			if not target_path:
				return False
			
			self.current_file_path = target_path
			self.file_path_var.set(target_path)
		
		try:
			content = self.code_editor.get(1.0, tk.END)
			with open(target_path, "w", encoding="utf-8") as file:
				file.write(content.rstrip() + "\n")
		except OSError as exc:
			messagebox.showerror("Save Error", f"Unable to save file.\n\n{exc}")
			return False
		
		self.unsaved_changes = False
		self.root.title(f"LOLCODE Interpreter - {os.path.basename(target_path)}")
		return True
	
	def on_close(self):
		if self.unsaved_changes:
			reply = messagebox.askyesnocancel(
				"Unsaved Changes",
				"You have unsaved changes. Do you want to save before quitting?"
			)

			if reply is True:
				if self.save_changes():
					self.root.destroy()
			
			elif reply is False:
				self.root.destroy()
			
			else:
				return
		else:
			self.root.destroy()
	
	def on_text_modified(self, event=None):
		if self.code_editor.edit_modified():
			self.unsaved_changes = True

			current_title = self.root.title()
			if not current_title.endswith("*"):
				self.root.title(current_title + " *")
			
			self.code_editor.edit_modified(False)
	
	def on_text_changed(self, event=None):
		"""Handle real-time token updates as user types (with debouncing)"""
		# Cancel any pending token update
		if self.token_update_job:
			self.root.after_cancel(self.token_update_job)
		
		# Schedule token update after 500ms of inactivity (debouncing)
		self.token_update_job = self.root.after(500, self.update_tokens_realtime)

	# --- EXECUTION LOGIC ---
	def run_code(self):
		if not self.save_changes():
			return
		code = self.code_editor.get(1.0, tk.END)
		
		# Clear previous run data
		self.console_output.config(state='normal')
		self.console_output.delete(1.0, tk.END)
		self.console_output.config(state='disabled')
		
		# Clear tables
		self.clear_tables()

		# Run in thread
		execution_thread = threading.Thread(target=self.execute_interpreter, args=(code,))
		execution_thread.daemon = True
		execution_thread.start()

	def execute_interpreter(self, code):
		self.is_executing = True
		try:
			# 1. Lexer
			tokens = list(lolcode_lexer(code))
			self.root.after(0, lambda: self.update_lexemes_table(tokens))

			# 2. Parser
			parser = Parser(tokens)
			ast_tree = parser.parse_program()

			# 3. Interpreter with real-time symbol table updates
			interpreter = Interpreter(
				output_func=self.gui_write, 
				input_func=self.gui_input,
				var_update_callback=self.on_variable_updated
			)
			interpreter.visit(ast_tree)

			# 4. Final Symbol Table Update
			self.root.after(0, lambda: self.update_symbol_table(interpreter.variables))

		except Exception as e:
			error_message = str(e)
			self.root.after(0, lambda: self.gui_write(f"\nERROR: {error_message}\n"))
		finally:
			self.is_executing = False
	
	def on_variable_updated(self, variables):
		"""Callback for real-time symbol table updates during execution"""
		self.root.after(0, lambda: self.update_symbol_table(variables))

	# --- I/O METHODS ---
	def gui_write(self, text):
		def _update():
			self.console_output.config(state='normal')
			self.console_output.insert(tk.END, text)
			self.console_output.see(tk.END)
			self.console_output.config(state='disabled')
		self.root.after(0, _update)

	def gui_input(self):
		"""Uses a popup dialog for input to keep the UI clean like the screenshot"""
		# We need to use a threading event or invoke explicitly because simpledialog is blocking
		# but needs to run on the main thread.
		
		result_container = {}
		input_event = threading.Event()

		def _ask():
			# This runs on Main Thread
			# Bring window to front and make sure dialog appears on top
			self.root.lift()
			self.root.attributes('-topmost', True)
			val = simpledialog.askstring("GIMMEH", "Enter value:", parent=self.root)
			self.root.attributes('-topmost', False)
			result_container['value'] = val if val is not None else ""
			input_event.set()

		self.root.after(0, _ask)
		input_event.wait() # Block Interpreter thread until UI responds
		
		val = result_container['value']
		# Echo input to console to match typical terminal behavior
		self.gui_write(f"{val}\n")
		return val

	# --- TABLE UPDATES ---
	def clear_tables(self):
		for i in self.lexemes_tree.get_children():
			self.lexemes_tree.delete(i)
		for i in self.symbol_tree.get_children():
			self.symbol_tree.delete(i)

	def update_lexemes_table(self, tokens):
		"""Matches (Lexeme, Classification) format"""
		# Clear existing tokens
		for item in self.lexemes_tree.get_children():
			self.lexemes_tree.delete(item)
		
		# Insert new tokens
		for t_type, t_val in tokens:
			if t_type != 'EOF' and t_type != 'NEWLINE':
				# Map technical token names to readable "Classifications" if desired
				# For now, we just use the raw token type
				self.lexemes_tree.insert('', 'end', values=(t_val, t_type))
	
	def update_tokens_realtime(self):
		"""Update token list in real-time as user types"""
		if self.is_executing:
			return  # Don't update tokens during execution
		
		try:
			code = self.code_editor.get(1.0, tk.END)
			tokens = list(lolcode_lexer(code))
			self.update_lexemes_table(tokens)
		except Exception:
			# Silently ignore lexer errors during typing
			pass

	def update_symbol_table(self, variables):
		"""Matches (Identifier, Value) format - updates symbol table in real-time"""
		# Clear existing symbols
		for item in self.symbol_tree.get_children():
			self.symbol_tree.delete(item)
		
		# Insert updated symbols
		for name, val in variables.items():
			# Format value for display
			if val is None:
				display_val = "NOOB"
			else:
				display_val = str(val)
			self.symbol_tree.insert('', 'end', values=(name, display_val))

def main():
	root = tk.Tk()
	app = LOLCodeInterpreterGUI(root)
	root.mainloop()

if __name__ == "__main__":
	main()