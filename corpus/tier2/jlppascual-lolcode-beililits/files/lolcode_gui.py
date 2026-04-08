import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import font
import os
from lolcode_lexer import *
import os, csv, copy
from lolcode_parser import *
from lolcode_interpreter import *

class LolcodeGUI:
    def __init__(self):
        self.ide_text = None
        self.lexemes_text = None
        self.terminal_text = None
        self.input_text = None
        self.symbols_text = None
        self.input_variables = []

    def load_interpreter(self, root):
        # root = Tk()
        root.title('Lolcode Interpreter')
        root.geometry("1300x800")
        # root.configure(bg='#15202b')
        my_frame = Frame(root)
        my_frame.pack(pady=5)

        text_scroll = Scrollbar(my_frame)
        self.ide_text = Text(my_frame, width=50, height=20, font=("Helvetica", 11), selectbackground="gray", foreground="white",selectforeground="white", undo=True, yscrollcommand=text_scroll.set, bg="#2d2d30")
        text_scroll.config(command=self.ide_text.yview)

        self.lexemes_text = Text(my_frame, width=49, height=20, font=("Helvetica", 11), selectbackground="gray", state="disabled", selectforeground="white", foreground="white", bg="#3e3e42")
        self.symbols_text = Text(my_frame, width=49, height=20, font=("Helvetica", 11), selectbackground="gray", state="disabled", selectforeground="white", foreground="white", bg="#3e3e42")
        self.terminal_text = Text(my_frame, width=50, height=20, font=("Helvetica", 11), selectbackground="gray", selectforeground="white", foreground="white", bg="#1e1e1e")
        self.input_text = Text(my_frame, width=50, height=20, font=("Helvetica", 11), selectbackground="gray", selectforeground="white", foreground="white", bg="#252526")

        title = Label(my_frame, text="Lolcode IDE", width=50, height=1, font=("Helvetica", 10), bg='#007acc', foreground="white") 
        lexemes = Label(my_frame, text="LEXEME TABLE", width=49, height=1, font=("Helvetica", 10), bg='#1e1e1e', foreground="white")
        symbol_table = Label(my_frame, text="SYMBOL TABLE", width=49, height=1, font=("Helvetica", 10), bg='#1e1e1e', foreground="white")
        terminal = Label(my_frame, text="TERMINAL", width=50, height=1, font=("Helvetica", 10), bg='#007acc', foreground="white")
        stdin = Label(my_frame, text="STDIN Inputs", width=50, height=1, font=("Helvetica", 10), bg='#3e3e42', foreground="white")

        execute_button = Button(my_frame, text='Run Code', command=run_code, font=("Helvetica", 11), bg="#cba117")

        title.grid(row=0,column=0)
        lexemes.grid(row=0,column=2)
        symbol_table.grid(row=0,column=3)

        self.ide_text.grid(row=1,column=0)
        text_scroll.grid(row=1, column=1, sticky='ns')
        self.lexemes_text.grid(row=1,column=2)
        self.symbols_text.grid(row=1,column=3)
        self.terminal_text.grid(row=1,column=4)

        execute_button.grid(row=2, column=0, columnspan=4, sticky=tk.W+tk.E)
        self.changeOnHover(execute_button, "white", "#cba117")

        terminal.grid(row=3,column=0, columnspan=3, sticky=tk.W+tk.E)
        stdin.grid(row=3, column=3)

        self.terminal_text.grid(row=4,column=0, columnspan=3, sticky=tk.W+tk.E)
        self.input_text.grid(row=4, column=3)

        my_menu = Menu(root)
        root.config(menu=my_menu)

        file_menu = Menu(my_menu, tearoff=False, font=("Helvetica", 10))
        my_menu.add_cascade(label="File", menu=file_menu)

        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=root.quit)

    def changeOnHover(self, button, colorOnHover, colorOnLeave):
  
        # adjusting backgroung of the widget
        # background on entering widget
        button.bind("<Enter>", func=lambda e: button.config(
            background=colorOnHover))
    
        # background color on leving widget
        button.bind("<Leave>", func=lambda e: button.config(
            background=colorOnLeave))

    def save_file(self):
        path = os.path.realpath(__file__)
        text_file = filedialog.asksaveasfilename(defaultextension=".*", initialdir=path, title="Save File", filetypes=(("lolcode", "*.lol"), ("Any Files", "*.*")))
        if text_file:
            text_file = open(text_file, 'w')
            text_file.write(self.ide_text.get(1.0, END))
            text_file.close()

    def get_text(self):
        return self.ide_text.get(1.0, END)

    def new_file(self):
        self.ide_text.delete("1.0", END)

    def open_file(self):
        self.new_file()
        path = os.path.realpath(__file__)
        text_file = filedialog.askopenfilename(initialdir=path, title="Open File", filetypes=(("lolcode", "*.lol"), ("Any Files", "*.*")))

        text_file = open(text_file, 'r')
        string_text = text_file.read()

        self.ide_text.insert(END, string_text)
        text_file.close()

    def update_lexeme_table(self, parser_list):
        self.lexemes_text.config(state="normal")
        self.lexemes_text.insert(END, "  " + "LEXEME" + "\t\t\t"+ "CLASSIFICATION" + "\n")
        self.lexemes_text.insert(END, "  " + "--------" + "\t\t\t"+ "------------" + "\n")
        for parser_line in parser_list:
            # ADDED THIS
            if parser_line == None:
                pass
            else:
                for parse in parser_line:
                    print(parse,"\n")
                    self.lexemes_text.insert(END, "  " + str(parse[0]) + "\t\t\t"+ str(parse[2]) + "\n")
        self.lexemes_text.config(state="disabled")

    def load_inputs(self):
        temp_string = self.input_text.get("1.0", END)
        self.input_variables = temp_string.split("\n")
        print(self.input_variables)

    def delete_lexeme_text(self):
        self.lexemes_text.config(state="normal")
        self.lexemes_text.delete("1.0", END)
        self.lexemes_text.config(state="disabled")
    
    def delete_terminal_text(self):
        self.terminal_text.config(state="normal")
        self.terminal_text.delete("1.0", END)
        self.terminal_text.insert("1.0", "Beililits/Lolcode Interpreter>\n")
        self.terminal_text.config(state="disabled")

    def delete_symbols_text(self):
        self.symbols_text.config(state="normal")
        self.symbols_text.delete("1.0", END)
        self.symbols_text.config(state="disabled")
    
    def update_symbol_table(self, variable_dict):
        self.symbols_text.config(state="normal")
        self.symbols_text.insert(END, "  " + "IDENTIFIER" + "\t\t\t"+ "VALUE" + "\n")
        self.symbols_text.insert(END, "  " + "--------" + "\t\t\t"+ "------------" + "\n")
        for key in variable_dict:
            if str(variable_dict[key]) == "True" or str(variable_dict[key]) == "1":
                self.symbols_text.insert(END, "  " + str(key) + "\t\t\t"+ "WIN" + "\n")
            elif str(variable_dict[key]) == "False"  or str(variable_dict[key]) == "0":
                self.symbols_text.insert(END, "  " + str(key) + "\t\t\t"+ "FAIL" + "\n")
            else:
                self.symbols_text.insert(END, "  " + str(key) + "\t\t\t"+ str(variable_dict[key]) + "\n")
        self.symbols_text.config(state="disabled")


def run_code():
    gui.delete_lexeme_text()
    gui.delete_terminal_text()
    gui.delete_symbols_text()

    gui.load_inputs()
    string = gui.get_text()
    # print(string.split("\n"))
    lexer = Lexer(string.split("\n"), load_regex())
    lexer_list = lexer.create_tokens()
    
    out = open('lexer.txt','w')
    for regex in lexer_list:
        out.write(str(regex)+"\n")
    out.close()

    copy_lexer_list = copy.deepcopy(lexer_list)

    parser = Parser(copy_lexer_list)
    parser_list, token_list = parser.parse_tokens()
    gui.update_lexeme_table(parser_list)

    interpreter = Interpreter(lexer_list, gui)
    interpreter.parse_tokens()
    variable_dict = interpreter.get_variables()
    gui.update_symbol_table(variable_dict)

    out = open('parser.txt','w')
    for parser in token_list:
        out.write(str(parser)+"\n")
    out.close()

    


root = Tk()

gui = LolcodeGUI()
gui.load_interpreter(root)






root.mainloop()
