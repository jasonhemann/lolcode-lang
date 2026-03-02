# CMSC124 B-1L
# Lexical Analyzer
# CONTRIBUTORS:
#   John Kenneth F. Manalang
#   Nathaniel F. Enciso

from tkinter import ttk
import lexical_analyzer
import syntactic_analyzer
import semantic_analyzer
import tkinter as tk
from tkinter import Frame, Scrollbar
from tkinter import filedialog as fd
from tkinter.font import Font


root = tk.Tk()
root.title("LOL_CODE_INTERPRETER by Enciso & Manalang")
root.configure(background='#303030')

lexemes = None
parse_tree = None
symbol_table = None

filename = "::NO_FILE_CHOSEN::"

class GUI:
    def __init__(self, master):
        master.geometry("1300x700")
        master.resizable(False, False)

        frame1 = Frame(master, background="#303030")#272727

        frame1.columnconfigure(0, weight=1)
        frame1.columnconfigure(1, weight=1)
        frame1.columnconfigure(2, weight=1)

        # ===================== lol code frame ==========================
        # TODO: can edit files. if no file selected, create new file then save.
        # else, save the edited to chosen file
        
        lolcode_frame = Frame(frame1, background="#303030")#272727
        berlin_sans = Font(family='Berlin Sans', size=12, weight='bold')
        btn2 = tk.Button(lolcode_frame, text="Open .lol file", font=berlin_sans, width = 43, command=self.open_file)
        btn2.pack(pady=(10, 5), padx=(9, 15), fill="both")

        # Add a Scrollbar
        h=Scrollbar(lolcode_frame, orient='horizontal')
        h.pack(side=tk.BOTTOM, fill='both', padx=(9,15), pady=(0, 10))
        v=Scrollbar(lolcode_frame, orient='vertical')
        v.pack(side=tk.RIGHT, fill='both', padx=(0,15),)

        consolas_font = Font(family='Calibri', size=10, weight='normal') # TODO: not working
        self.code_textbox = tk.Text(lolcode_frame, height=20, width=60, font=consolas_font, bg="#DADADA", wrap="none", xscrollcommand=h.set, yscrollcommand=v.set)

        # Attach the scrollbar with the text widget
        h.config(command=self.code_textbox.xview)
        v.config(command=self.code_textbox.yview)

        self.code_textbox.pack(padx=(10,0), fill="both")

        lolcode_frame.grid(row=0, column=0, sticky="nsew")

        # ===================== lexemes frame ==========================
        lexemes_frame = Frame(frame1, background="#303030")#272727
        lexemes_frame.grid(row=0, column=1, sticky="nsw")

        # -- using treeview for table --
        lextable_frame = Frame(lexemes_frame, background="#303030")#272727
        columns = ('lexemes', 'classification')

        c=Scrollbar(lexemes_frame, orient='vertical')
        c.pack(side=tk.RIGHT, fill='y', pady=12)

        # define headings
        self.style = ttk.Style()
        self.style.theme_use("clam") # clam, alt, 
        self.style.configure("Treeview",
            background = "silver",
            foreground = "black",
            rowheight = 23,
            fieldbackground = "white",
            )
        self.style.configure("Treeview.Heading", font=berlin_sans)
        self.style.map("Treeview",
            background = [("selected", "black")],
            foreground = [("selected", "white")])

        self.tree = ttk.Treeview(lextable_frame, columns=columns, show='headings', height=14, yscrollcommand=c.set)
        self.tree.heading('lexemes', text='Lexeme')
        self.tree.heading('classification', text='Classification')
        self.tree.grid(row=0, column=0, sticky='nsew', pady=10)
        self.tree.column("#1", stretch="yes", width=150)
        self.tree.pack(pady=(12,0))

        lextable_frame.pack()

        c.config(command=self.tree.yview)
        # -- using treeview for table --

        # ===================== symbol table frame ==========================
        symbol_table_frame = Frame(frame1, background="#303030")#272727
        symbol_table_frame.grid(row=0, column=2, sticky="nsw")


        # # -- using treeview for table --
        #symboltable_frame = Frame(symbol_table_frame, background="#303030")#272727
        columns = ('identifier', 'value', "type")

        c1=Scrollbar(symbol_table_frame, orient='vertical')
        c1.pack(side=tk.RIGHT, fill='both', pady=12)


        # define headings
        self.style = ttk.Style()
        self.style.theme_use("clam") # clam, alt, 
        self.style.configure("Treeview",
            background = "silver",
            foreground = "black",
            rowheight = 23,
            fieldbackground = "white",
            )
        self.style.configure("Treeview.Heading", font=berlin_sans)
        self.style.map("Treeview",
            background = [("selected", "black")],
            foreground = [("selected", "white")])

        self.tree_s = ttk.Treeview(symbol_table_frame, columns=columns, show='headings', height=14, yscrollcommand=c1.set)
        self.tree_s.heading('identifier', text='Identifier')
        self.tree_s.heading('value', text='Value')
        self.tree_s.heading('type', text='Type')
        #self.tree_s.grid(row=0, column=0, sticky='nsew', pady=10)
        self.tree_s.column('identifier', stretch="yes", width=100)
        self.tree_s.column('type', stretch="yes", width=90)
        self.tree_s.pack(pady=(12,0))

        c1.config(command=self.tree_s.yview)

        #symboltable_frame.pack()
        frame1.pack(expand=True, fill="both", padx=10, pady=10)

        # ===================== execute frame ==========================
        frame2 = Frame(master, background="#303030")#272727
        execute_label = tk.Button(frame2, text="Execute/Run", font=('Arial', 10), command=self.execute, width=100)
        execute_label.pack(pady=10)
        self.x_textbox = tk.Text(frame2, height=15, width=115, font=('Arial', 10), background="#000", foreground="#fff")
        self.x_textbox.pack()

        frame2.pack(expand=True, fill="both", padx=10, pady=(0, 10))

        clear_btn = tk.Button(master, text="Clear", font=berlin_sans, width = 10, command=self.clear)
        clear_btn.place(x=17, y=400)


    def clear(self):
        global lexemes, parse_tree, symbol_table
        lexemes = None
        parse_tree = None
        symbol_table = None
        self.x_textbox.config(state=tk.NORMAL)
        self.x_textbox.delete("1.0", tk.END)
        self.code_textbox.delete('1.0', "end")
        for item in self.tree.get_children():
            self.tree.delete(item)
        for item in self.tree_s.get_children():
            self.tree_s.delete(item)
        # self.x_textbox.config(state=tk.DISABLED)

    def execute(self):
        self.x_textbox.config(state=tk.NORMAL)
        self.x_textbox.delete("1.0", tk.END)
        global lexemes, parse_tree, symbol_table
        lexemes = None
        parse_tree = None
        symbol_table = None
        temp_content = self.code_textbox.get("1.0", tk.END)
        temp_content.strip
        if ((filename != "::NO_FILE_CHOSEN::" and len(temp_content) > 1) or len(temp_content) > 1):
            lexemes = lexical_analyzer.lex_main(temp_content)
            #print("LEX"+str(lexemes))
            firstLex = lexemes[0]
            #print(firstLex)
            self.show_lexemes()

            if (isinstance(firstLex,str)):
                self.show_symbol_table()
            else:
                parse_tree = syntactic_analyzer.syntax_main(lexemes)
                #print("SYNTAX"+str(parse_tree.getResult()))

                if (isinstance(parse_tree.getResult(), str)):
                    self.x_textbox.insert("insert", parse_tree.getResult())
                    self.show_symbol_table()
                else:
                    symbol_table = semantic_analyzer.semantic_main(parse_tree, self)
                    #print("SEMANTIC"+str(symbol_table))
                    if (isinstance(symbol_table, str)):
                        self.x_textbox.insert("insert", symbol_table)
                        symbol_table = None
                        self.show_symbol_table()
                    else:
                        self.show_symbol_table()
            self.x_textbox.config(state=tk.DISABLED)

        else:
            self.x_textbox.insert("insert","There is no code")
            for item in self.tree.get_children():
                self.tree.delete(item)
            for item in self.tree_s.get_children():
                self.tree_s.delete(item)

    def open_file(self):
        
        filetypes = (
            ('lol files', '*.lol'),
            #('All files', '*.*')
        )

        global filename
        filename = fd.askopenfilenames(
            title='Open files',
            initialdir=".",
            filetypes=filetypes)

        filename = str(filename)[2:-3] # removing parenthesis and apostrophes

        self.code_textbox.delete('1.0', "end")
        try:
            with open(filename, 'r', encoding='utf-8') as a:
                self.code_textbox.insert("insert", a.read())
        except:
            filename = "::NO_FILE_CHOSEN::"
        
        if (filename != "::NO_FILE_CHOSEN::"):
            root.title("LOL_CODE_INTERPRETER by Enciso & Manalang: " + filename)
        else:
            root.title("LOL_CODE_INTERPRETER by Enciso & Manalang")

    # function for treeview
    def show_lexemes(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        global lexemes
        if (isinstance(lexemes[0], str)):
            error = lexemes.pop(0)
            self.x_textbox.insert("insert", error)
        #print(lexemes)
        for lexeme in lexemes:
            if (lexeme[0] != "NEWLINE"):
                rev_lexeme = []
                if (lexeme[0] == "YARN Literal"):
                    temp = lexeme[1].replace("<<@#QUOTE#$>>",'"')
                    temp = temp.replace("<<@#NEWLINE#$>>",'\\n')
                    temp = temp.replace("\t",'\\t')
                    temp = temp.replace("\a","")
                    rev_lexeme.append(temp)
                else:
                    rev_lexeme.append(lexeme[1])
                rev_lexeme.append(lexeme[0])
                self.tree.insert('', tk.END, values=rev_lexeme)

    def show_symbol_table(self):
        for item in self.tree_s.get_children():
            self.tree_s.delete(item)

        global symbol_table
        try:
            for val in symbol_table:
                if (val[2] == "YARN"):
                    temp = []
                    temp.append(val[0])
                    temp2 = val[1].replace("<<@#QUOTE#$>>",'"')
                    temp2 = temp2.replace("<<@#NEWLINE#$>>",'\\n')
                    temp2 = temp2.replace("\t",'\\t')
                    temp2 = temp2.replace("\a","")
                    temp.append(temp2)
                    temp.append(val[2])
                else:
                    temp = []
                    temp.append(val[0])
                    temp.append(val[1])
                    temp.append(val[2])
                self.tree_s.insert('', tk.END, values=temp)
        except:
            pass
    
    def show_symbol_table2(self, temp_table):
        for item in self.tree_s.get_children():
            self.tree_s.delete(item)

        try:
            for val in temp_table:
                if (val[2] == "YARN"):
                    temp = []
                    temp.append(val[0])
                    temp2 = val[1].replace("<<@#QUOTE#$>>",'"')
                    temp2 = temp2.replace("<<@#NEWLINE#$>>",'\\n')
                    temp2 = temp2.replace("\t",'\\t')
                    temp2 = temp2.replace("\a","")
                    temp.append(temp2)
                    temp.append(val[2])
                else:
                    temp = []
                    temp.append(val[0])
                    temp.append(val[1])
                    temp.append(val[2])
                self.tree_s.insert('', tk.END, values=temp)
        except:
            pass


GUI(root)

root.mainloop()


# references:
#   > open file in tkinter: https://www.pythontutorial.net/tkinter/tkinter-open-file-dialog/
#   > color picker: https://imagecolorpicker.com/color-code
#   > table tkinter: https://www.youtube.com/watch?v=ewxT3ZEGKAA

