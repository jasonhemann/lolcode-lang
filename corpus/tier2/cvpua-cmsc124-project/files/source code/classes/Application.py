from tkinter import *
from classes.Interpreter import Interpreter


class Application:
	
	def __init__(self):
		self.lol = Interpreter()

	def update_lexeme_table(self, lexeme_table):			# update lexeme table
		lexeme_table.delete(*lexeme_table.get_children())	# clear table
		for token in self.lol.tokens:
			lexeme_table.insert(parent='', index='end', text=token.name, values=(token.type))
		
	def update_sym_table(self, sym_table):					# update symbol table
		sym_table.delete(*sym_table.get_children())			# clear table
		for key in self.lol.symbol_table:
			if not self.lol.symbol_table[key].value:		# check if value if empty
				sym_table.insert(parent='', index='end', text=key, values=("None"))
			else:

				# handle spaces in treeview, because it would cut spaces if encountered
				temp1 = ""
				if " " in self.lol.symbol_table[key].value:
					temp = self.lol.symbol_table[key].value.split(" ")
					for i in temp:
						temp1 = temp1 + i + "\ "
				else:
					temp1 = self.lol.symbol_table[key].value
				
				

				sym_table.insert(parent='', index='end', text=key, values=(temp1))

	def update_terminal(self, output_text, string):	# update terminal
		string = str(string)
		output_text.insert(END,string+'\n')			# print string
		output_text.insert(END,"lol-terminal:~$ ")	# print string
		output_text.see("end")

	def execute(self, lexeme_table, sym_table, output_text, text_editor):	# run the program

		try:
			self.lol.text = text_editor.get(1.0, END)	# update based from text_editor contents
			self.lol.run_lexer()
			self.update_lexeme_table(lexeme_table)
			# self.lol.print_tokens()
			self.lol.run_parser()
			# self.lol.print_tree()
			self.lol.run_analyzer(output_text)
			self.update_sym_table(sym_table)
			
		except Exception as err:
			# sym_table.delete(*sym_table.get_children())			# clear table
			# lexeme_table.delete(*lexeme_table.get_children())	# lear table
			# output_text.delete(1.0, END) 						# clear the output text
			print(err)
			self.update_terminal(output_text, err)
		self.design_terminal(output_text)


	def upload(self, text_editor,upload_label):			# upload file to gui text editor
		filename = self.lol.readFile()
		if filename:
			text_editor.delete(1.0, END)
			text_editor.insert(END, self.lol.text)
			upload_label.pack_forget()
			file = ""
			filename = filename.split("/")
			if len(filename[-1]) > 20:
				file = filename[-1][0:19] + "..."
			else:
				file = filename[-1]

			upload_label = Label(text=file, anchor=W, font=('Roboto', 12), width=20)
			upload_label.grid(row=0, column=0)

	def design_terminal(self, output_text):		# design gui terminal
	
		ter = "lol-terminal:~$"
		index = '1.0'
		while 1: 
			index = output_text.search(ter, index, nocase=1,stopindex=END)  
			if not index: break
			lastindex = '%s+%dc' % (index, len(ter))  
			output_text.tag_add('found', index, lastindex)  
			index = lastindex 
		output_text.tag_config('found', foreground='green') 
