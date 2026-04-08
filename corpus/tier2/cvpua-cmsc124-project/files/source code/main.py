from classes.Application import Application
from classes.Interpreter import Interpreter
from tkinter import *
from tkinter import ttk
from tkinter import filedialog

app = Application()	

root = Tk()
root.title("LOLTERPRETER")
root.geometry("1000x620")
root.resizable(0, 0)

# upload label
upload_label = Label(root, text="", anchor=W, font=('Roboto', 12), width=20)	
upload_label.grid(row=0,column=0, sticky=W)

# upload button
upload_button = Button(root, text="Upload File", width=23, height=1, command=lambda:app.upload(text_editor, upload_label))
upload_button.grid(row=0,column=1,sticky=E)

# text editor
text_editor_frame = Frame(root)
text_editor = Text(text_editor_frame, width=51,height=21)
text_editor.pack()

text_editor_frame.grid(row=1, column=0, columnspan=2)

# lexeme table label
lexeme_label = Label(root, text="LEXEMES", font=('Roboto', 15, 'bold'))
lexeme_label.grid(row=0, column=2)

# lexeme table
lexeme_table_frame = Frame(root)
lexeme_scroll = Scrollbar(lexeme_table_frame)
lexeme_scroll.pack(side=RIGHT, fill=Y)
lexeme_table =  ttk.Treeview(lexeme_table_frame, yscrollcommand=lexeme_scroll.set, height=17)
lexeme_table.pack()
lexeme_scroll.config(command=lexeme_table.yview)
lexeme_table['columns'] = ("Classification")
lexeme_table.column("#0",width=140, minwidth=50, stretch=NO)
lexeme_table.column("Classification", anchor=W, width=140, minwidth=50, stretch=NO)
lexeme_table.heading("#0", text="Lexeme", anchor=CENTER)
lexeme_table.heading("Classification", text="Classification", anchor=CENTER)

lexeme_table_frame.grid(row=1, column=2)

# symbol table label
sym_label = Label(root, text="SYMBOL TABLE", font=('Roboto', 15, 'bold'))
sym_label.grid(row=0, column=3)

# symbol table
sym_table_frame = Frame(root)
sym_scroll = Scrollbar(sym_table_frame)
sym_scroll.pack(side=RIGHT, fill=Y)
sym_table =  ttk.Treeview(sym_table_frame, yscrollcommand=sym_scroll.set, height=17)
sym_table.pack()
sym_scroll.config(command=sym_table.yview)
sym_table['columns'] = ("Value")
sym_table.column("#0",width=140, minwidth=50, stretch=NO)
sym_table.column("Value", anchor=W, width=140, minwidth=50, stretch=NO)
sym_table.heading("#0", text="Identifier", anchor=CENTER)
sym_table.heading("Value", text="Value", anchor=CENTER)

sym_table_frame.grid(row=1, column=3)

# output text
output_text_frame = Frame(root)
output_text = Text(output_text_frame, width=124,height=12, backgroun="black")
output_text.configure(insertbackground='white')
output_text.pack()
output_text.insert(END,"lol-terminal:~$ ")
output_text.tag_add("terminal", "1.0", "1.15")
output_text.tag_config("terminal", foreground="green")
output_text.tag_add("text", "1.15", END)
output_text.tag_config("text", foreground="white")
output_text.bind("<Key>", lambda e: "break")
output_text_frame.grid(row=3,column=0,columnspan=4)

# execute button
execute_button = Button(root, text="Execute", width=121, command=lambda:app.execute(lexeme_table, sym_table, output_text, text_editor))
execute_button.grid(row=2, column=0, columnspan=4)

root.mainloop()