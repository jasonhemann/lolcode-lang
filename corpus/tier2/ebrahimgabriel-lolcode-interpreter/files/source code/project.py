'''
CMSC 124 Project
Hello World Group
Cid Jezreel Ceradoy, Ebrahim Gabriel, Reynaldo Isaac Jr.
'''

import re
import os as os
import tkinter as tk
from tkinter import filedialog, ttk

import semantic

class LOLCODE_Interpreter(tk.Tk):
    def __init__(self):
        # ui stuff
        tk.Tk.__init__(self)
        self.title("LOLCODE Lexer")

        window_width = 1280
        window_height = 600

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x_position = int((screen_width - window_width) / 2)
        y_position = int((screen_height - window_height) / 2)

        self.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
        self.resizable(False, False)

        # Calculate frame heights based on the specified ratios
        height_top = (window_height) // 10
        height_middle = (4 * window_height) // 10
        height_execute = (window_height) // 10
        height_bottom = (5 * window_height) // 10

        # Calculate frame widths based on the specified ratios
        width_top_left = (window_width - 20) // 3
        width_top_right = 2 * (window_width - 20) // 3

        # Calculate frame widths for frame_middle components
        width_middle_1 = (window_width - 20) // 3
        width_middle_2 = (window_width - 20) // 3
        width_middle_3 = (window_width - 20) // 3

        # Create a frame for the top area (1/10 height)
        frame_top = tk.Frame(self, width=window_width - 20, height=height_top, bd=2)
        frame_top.place(x=10, y=10)
        frame_top.pack_propagate(False)

        # Create a frame for the top left area (1/3 width) with a margin
        frame_top_left = tk.Frame(frame_top, width=width_top_left - 10, height=height_top - 10, bd=2, bg="lightgray")
        frame_top_left.place(x=5, y=5)
        frame_top_left.pack_propagate(False)

        # Create a button for file selection
        input_button = tk.Button(frame_top_left, text="Open File", font=("Helvetica", 12), command=lambda: self.select_input(),
                                 width=width_top_left - 10, height=height_top - 10)
        input_button.pack()

        # Create a frame for the top right area (2/3 width) with a margin
        frame_top_right = tk.Frame(frame_top, width=width_top_right - 10, height=height_top - 10, bd=2, bg="lightgray")
        frame_top_right.place(x=width_top_left + 5, y=5)
        frame_top_right.pack_propagate(False)

        # Create a frame for widget 1.5
        widget1 = tk.Label(frame_top_right, text="\"HELLO WORLD\" - LOL CODE Interpreter", font=("Helvetica", 20, "bold"), bg="lightgray")
        widget1.pack(expand=True, fill=tk.BOTH)

        # Create a frame for the middle area (4/10 height)
        frame_middle = tk.Frame(self, width=window_width - 20, height=height_middle, bd=2)
        frame_middle.place(x=10, y=height_top + 20)
        frame_middle.pack_propagate(False)

        # Create a frame for middle component 1 (1/3 width) with a margin
        frame_middle_1 = tk.Frame(frame_middle, width=width_middle_1 - 10, height=height_middle - 10, bd=2,
                                  bg="lightgray")
        frame_middle_1.place(x=5, y=5)
        frame_middle_1.pack_propagate(False)

        # Create a text box inside frame_middle_1
        self.code_textbox = tk.Text(frame_middle_1, wrap=tk.WORD, font=("Helvetica", 12))
        self.code_textbox.pack(fill=tk.BOTH, expand=True)

        # Create a frame for middle component 2 (1/3 width) with a margin
        frame_middle_2 = tk.Frame(frame_middle, width=width_middle_2 - 10, height=height_middle - 10, bd=2,
                                  bg="lightgray")
        frame_middle_2.place(x=width_middle_1 + 5, y=5)
        frame_middle_2.pack_propagate(False)

        # # Create a frame for widget 4
        # widget4 = tk.Label(frame_middle_2, text="Widget 4", font=("Helvetica", 12))
        # widget4.pack(expand=True, fill=tk.BOTH)

        # Create a label below the Listbox and Scrollbar
        self.label_listbox = tk.Label(frame_middle_2, text="Lexemes", font=("Helvetica", 12), bg="lightgray")
        self.label_listbox.pack()

        # Create a Treeview widget inside frame_middle_2
        self.lextree = ttk.Treeview(frame_middle_2, columns=("Column1", "Column2"), show="headings")
        self.lextree.heading("Column1", text="Lexeme")
        self.lextree.heading("Column2", text="Classification")
        self.lextree.column("Column1", width=100)
        self.lextree.column("Column2", width=100)
        self.lextree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create a Scrollbar for the Treeview
        self.scrollbar_middle_2 = tk.Scrollbar(frame_middle_2, command=self.lextree.yview)
        self.scrollbar_middle_2.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure the Treeview to use the Scrollbar
        self.lextree.config(yscrollcommand=self.scrollbar_middle_2.set)

        # Create a frame for middle component 3 (1/3 width) with a margin
        self.frame_middle_3 = tk.Frame(frame_middle, width=width_middle_3 - 10, height=height_middle - 10, bd=2,
                                  bg="lightgray")
        self.frame_middle_3.place(x=width_middle_1 + width_middle_2 + 5, y=5)
        self.frame_middle_3.pack_propagate(False)

        # Create a frame for widget 5
        widget5 = tk.Label(self.frame_middle_3, text="Symbol Table", font=("Helvetica", 12), bg="lightgray")
        widget5.pack(expand=True, fill=tk.BOTH)
        
        # Create a Treeview widget inside frame_middle_3
        self.symtree = ttk.Treeview(self.frame_middle_3, columns=("Column1", "Column2", "Column3"), show="headings")
        self.symtree.heading("Column1", text="Identifier")
        self.symtree.heading("Column2", text="Datatype")
        self.symtree.heading("Column3", text="Value")
        self.symtree.column("Column1", width=100)
        self.symtree.column("Column2", width=100)
        self.symtree.column("Column3", width=100)
        self.symtree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Create a Scrollbar for the Treeview
        self.scrollbar_middle_3 = tk.Scrollbar(self.frame_middle_3, command=self.symtree.yview)
        self.scrollbar_middle_3.pack(side=tk.RIGHT, fill=tk.Y)

        # Create a frame for the execute area (1/10 height)
        self.frame_execute = tk.Frame(self, width=window_width - 20, height=height_execute, bd=2, bg="lightgray")
        self.frame_execute.place(x=10, y=height_top + height_middle + 30)
        self.frame_execute.pack_propagate(False)

        # Create a button for file selection
        read_button = tk.Button(self.frame_execute, text="Execute", font=("Helvetica", 12), command=lambda: self.read_textbox(),
                                width=window_width - 10,
                                height=height_execute)
        read_button.pack()

        # Create a frame for the bottom area (5/10 height) with a 10-pixel bottom margin
        frame_bottom = tk.Frame(self, width=window_width - 20, height=height_bottom / 1.6, bd=2, bg="lightgray")
        frame_bottom.place(x=10, y=height_top + height_middle + 40 + height_execute)
        frame_bottom.pack_propagate(False)

        # Create a frame for widget 3
        # widget3 = tk.Label(frame_bottom, text="Widget 3", font=("Helvetica", 12))
        # widget3.pack(expand=True, fill=tk.BOTH)
        self.terminal = tk.Text(frame_bottom, wrap=tk.WORD, font=("Helvetica", 12))
        self.terminal.pack(fill=tk.BOTH, expand=True)
        
        # Create a Scrollbar for the Text widget
        scrollbar = tk.Scrollbar(frame_bottom, command=self.terminal.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure Text widget to use the scrollbar
        self.terminal.configure(yscrollcommand=scrollbar.set)

        # contains identified lexemes and their tokens
        self.lexemes = []

        # contains the lolcode script for reading
        self.code = []
        self.lines = []
        # -=================LEXER=====================-

        # regexes to consider
        # categorized
        self.identifiers = r'^([a-zA-Z][a-zA-Z0-9_]*)$'
        self.numbr = r'^(-?[1-9][0-9]*|0)$'
        self.numbar = r'^(-?[1-9][0-9]*\.[0.9]+|-?[0\.[0-9]+)$'
        self.yarn = r'^"[^"]*"$'
        self.troof = r'^(WIN|FAIL)$'
        self.datatype = r'^(NOOB|NUMBA?R|YARN|TROOF)$'
        self.progstart = r'^HAI$'
        self.progend = r'^KTHXBYE$'
        self.vardecstart = r'^WAZZUP$'
        self.vardecend = r'^BUHBYE$'
        self.vardec = r'^I HAS A$'
        self.varinit = r'^ITZ$'
        self.input = r'^GIMMEH$'
        self.output = r'^VISIBLE$'
        self.concatoperator = r'^\+$'
        self.addition = r'^SUM OF$'
        self.difference = r'^DIFF OF$'
        self.multiplication = r'^PRODUKT OF$'
        self.division = r'^QUOSHUNT OF$'
        self.modulo = r'^MOD OF$'
        self.max = r'^BIGGR OF$'
        self.min = r'^SMALLR OF$'
        self.opsep = r'^AN$'
        self.concat = r'^SMOOSH$'
        self.booland = r'^BOTH OF$'
        self.boolor = r'^EITHER OF$'
        self.boolxor = r'^WON OF$'
        self.boolnot = r'^NOT$'
        self.boolalland = r'^ALL OF$'
        self.boolallor = r'^ANY OF$'
        self.endlist = r'^MKAY$'
        self.compareequal = r'^BOTH SAEM$'
        self.comparediff = r'^DIFFRINT$'
        self.typecast = r'^MAEK$'
        self.recast = r'^IS NOW A$'
        self.assign = r'^R$'
        self.ifstart = r'^O RLY\?$'
        self.ifif = r'^YA RLY$'
        self.elseif = r'^MEBBE$'
        self.elsekey = r'^NO WAI$'
        self.flowend = r'^OIC$'
        self.switchstart = r'^WTF\?'
        self.switchcase = r'^OMG$'
        self.switchdef = r'^OMGWTF$'
        self.loopstart = r'^IM IN YR$'
        self.loopend = r'^IM OUTTA YR$'
        self.increment = r'^UPPIN$'
        self.decrement = r'^NERFIN$'
        self.loopcondfor = r'^TIL$'
        self.loopcondwhile = r'^WILE$'
        self.breakkey = r'^GTFO$'
        self.funcstart = r'^HOW IZ I$'
        self.funcend = r'^IF U SAY SO$'
        self.params = r'^YR$'
        self.returnkey = r'^FOUND YR$'
        self.funccall = r'^I IZ$'
        self.linebreak = r'^\n$'

        self.singlecomments = r'BTW.*'
        self.multicommentstart = r'OBTW.*'
        self.multicommentend = r'TLDR'

        # used in tokenizing
        self.spacedkeywords = [r'I HAS A ', r'SUM OF ', r'DIFF OF ', r'PRODUKT OF ', r'QUOSHUNT OF ', r'MOD OF '
            , r'BIGGR OF ', r'SMALLR OF ', r'BOTH OF ', r'EITHER OF ', r'WON OF ', r'ANY OF ', r'ALL OF ', r'BOTH SAEM '
            , r'IS NOW A ', r'O RLY\? ', r'YA RLY ', r'NO WAI ', r'IM IN YR ', r'IM OUTTA YR ', r'HOW IZ I ', r'IF U SAY SO '
            , r'FOUND YR ', r'I IZ ', r'BTW .*', r'OBTW .*', r'TLDR']
        ##
        ## FIX THE COMMENT THING IN TOKENS
        ##
        self.spacedyarn = r'"[^"]*"'

        # -===========================================-

        '''
        notes:
        + is the concat operator for VISIBLE
        NUMBAR, NUMBR, YARN regex literals were changed to remove leading zeroes from NUMBR/NUMBARS and disallow " chars inside the YARN 
        '''

    # open a lolcode file
    def select_input(self):
        input_filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select a File",
                                                    filetypes=(("LOLCODE files", "*.lol"), ("all files", "*.*")))
        input_file = open(input_filename, "r")
        self.code_textbox.delete("1.0", tk.END)
        for line in input_file.readlines():
            self.code_textbox.insert(tk.END, line)
        input_file.close()

    # reads the code in the textbox
    def read_textbox(self):
        # Reset variables
        self.code = []
        self.lexemes = []
        self.lines = []
        # Assures blank slate to all widgets
        # Clear existing content in the textbox
        self.terminal.delete(1.0, tk.END)
        # Clear existing items in the Treeview
        for item in self.lextree.get_children():
            self.lextree.delete(item)
        # Clear existing items in the Treeview
        for item in self.symtree.get_children():
            self.symtree.delete(item)
        
        
        # get text and split
        self.code = self.code_textbox.get("1.0", tk.END)
        delimiter = '\n'
        self.code = [s+delimiter for s in re.split('\n', self.code) if s]

        # magic list comprehension to remove instances of a value
        self.code = [line for line in self.code if line != '']
        # tokenize each line then identify lexemes
        self.lexemes = []

        multicomment = False
        for line in self.code:
            line2 = line.lstrip()
            if line2 == '':
                continue
            
            if multicomment:
                if re.search(self.multicommentend, line2):
                    multicomment = False
                continue

            if re.search(self.multicommentstart, line2):
                multicomment = True
                continue

            tokens = self.tokenize_line(line2)
            temp = []
            for token in tokens:
                lexeme = self.identify_token(token)
                self.lexemes.append(lexeme)
                temp.append(lexeme)
            self.lines.append(temp)

        self.display_lexemes()
        

        #-----------------
        #move this somewhere as long as it does these things properly
        s = semantic.Semantic(self.lines)
        s.read_code()
        # s.symbol_table <- contains symbol table (list of lists)
        # print(s.symbol_table)
        self.display_symboltable(s.symbol_table)
        # s.toprint <- contains lines to be printed

        # print('toprint', s.toprint)
        self.display_terminal(s.toprint)
        #-----------------

        # print(self.lines)
        # Print lexeme array containing sub-arrays of token and category
        # self.lexemes = ['token', 'category'],...
        # for lexeme in self.lexemes:
            # print(lexeme)      

    def display_lexemes(self):
        # Clear existing items in the Treeview
        for item in self.lextree.get_children():
            self.lextree.delete(item)

        # Insert lexemes into the Treeview
        for lexeme in self.lexemes:
            self.lextree.insert("", tk.END, values=(lexeme[0], lexeme[1]))
            
    def display_symboltable(self, symbol_table):
        # Clear existing items in the Treeview
        for item in self.symtree.get_children():
            self.symtree.delete(item)

        # Insert lexemes into the Treeview
        for item in symbol_table:
            col1_value = item[0]  # First item in the sub-array
            col2_value = item[1]
            col3_value = item[2] if len(item) > 2 else ''  # Third item if available, otherwise an empty string
            self.symtree.insert('', 'end', values=(col1_value, col2_value, col3_value))

    def display_terminal(self, toprint):
        # Clear existing content in the textbox
        self.terminal.delete(1.0, tk.END)
        
        for item in toprint:
            self.terminal.insert(tk.END, item + '\n')
    
    # tokenizes one line and returns its tokens
    def tokenize_line(self, line):
        
        ##REMOVE LATER ON
        # remove comments
        temp = re.sub(self.singlecomments, '', line)
        ##

        temp = line.lstrip()
        temp = re.sub('\n', ' \n', temp)

        count = 0
        substrings = []

        # get spaced keywords ####COMMENTS ARENT READ PROPERLY SO I REMOVED THEM FORNOW
        for regex in self.spacedkeywords:
            # extract the spaced keywords and place them in list to return them later
            if re.search(regex, temp) != None:
                regexstring = regex[:-1]
                temp = re.sub(regex, "{" + str(count) + "} ", temp)
                count = count + 1
                substrings.append(regexstring)

        # get YARNs with spaces between
        yarn = re.findall(self.spacedyarn, temp)
        if yarn:
            for match in yarn:
                temp = re.sub(self.spacedyarn, "{" + str(count) + "}", temp, 1)
                count = count + 1
                substrings.append(match)

        # split the line into its tokens, then return the spaced keywords to their original place
        tokens = re.split(' ', temp)
        for i in range(len(substrings)):
            tempstr = "{" + str(i) + "}"
            tempstr2 = "{" + str(i) + "} \n"
            for j in range(len(tokens)):
                if tokens[j] == tempstr:
                    tokens[j] = substrings[i]
                if tokens[j] == tempstr2:
                    tokens[j] = substrings[i]
        return tokens

    # identifies a token
    def identify_token(self, token):
        if re.search(self.identifiers, token) != None:
            category = 'identifier'
        if re.search(self.numbar, token) != None:
            category = 'numbar'
        if re.search(self.numbr, token) != None:
            category = 'numbr'
        if re.search(self.yarn, token) != None:
            category = 'yarn'
        if re.search(self.troof, token) != None:
            category = 'troof'
        if re.search(self.datatype, token) != None:
            category = 'datatype'
        if re.search(self.progstart, token) != None:
            category = 'program start'
        if re.search(self.progend, token) != None:
            category = 'program end'
        if re.search(self.vardecstart, token) != None:
            category = 'variable declaration area start'
        if re.search(self.vardecend, token) != None:
            category = 'variable declaration area end'
        if re.search(self.vardec, token) != None:
            category = 'variable declaration'
        if re.search(self.varinit, token) != None:
            category = 'variable initialization'
        if re.search(self.input, token) != None:
            category = 'input'
        if re.search(self.output, token) != None:
            category = 'output'
        if re.search(self.concatoperator, token) != None:
            category = 'concatenation operator (VISIBLE)'
        if re.search(self.addition, token) != None:
            category = 'addition'
        if re.search(self.difference, token) != None:
            category = 'difference'
        if re.search(self.multiplication, token) != None:
            category = 'multiplication'
        if re.search(self.division, token) != None:
            category = 'division'
        if re.search(self.modulo, token) != None:
            category = 'modulo'
        if re.search(self.max, token) != None:
            category = 'max'
        if re.search(self.min, token) != None:
            category = 'min'
        if re.search(self.opsep, token) != None:
            category = 'operand separator'
        if re.search(self.concat, token) != None:
            category = 'concatenation'
        if re.search(self.booland, token) != None:
            category = 'booland'
        if re.search(self.boolor, token) != None:
            category = 'boolor'
        if re.search(self.boolxor, token) != None:
            category = 'boolxor'
        if re.search(self.boolnot, token) != None:
            category = 'boolnot'
        if re.search(self.boolalland, token) != None:
            category = 'boolalland'
        if re.search(self.boolallor, token) != None:
            category = 'boolallor'
        if re.search(self.endlist, token) != None:
            category = 'end of operands'
        if re.search(self.compareequal, token) != None:
            category = 'compare equal'
        if re.search(self.comparediff, token) != None:
            category = 'compare diff'
        if re.search(self.typecast, token) != None:
            category = 'typecast'
        if re.search(self.recast, token) != None:
            category = 'recast'
        if re.search(self.assign, token) != None:
            category = 'assignment'
        if re.search(self.ifstart, token) != None:
            category = 'if then start'
        if re.search(self.ifif, token) != None:
            category = 'if'
        if re.search(self.elseif, token) != None:
            category = 'else if'
        if re.search(self.elsekey, token) != None:
            category = 'else'
        if re.search(self.flowend, token) != None:
            category = 'flow control end'
        if re.search(self.switchstart, token) != None:
            category = 'switch start'
        if re.search(self.switchcase, token) != None:
            category = 'switch case'
        if re.search(self.switchdef, token) != None:
            category = 'switch default'
        if re.search(self.loopstart, token) != None:
            category = 'loop start'
        if re.search(self.loopend, token) != None:
            category = 'loop end'
        if re.search(self.increment, token) != None:
            category = 'increment'
        if re.search(self.decrement, token) != None:
            category = 'decrement'
        if re.search(self.loopcondfor, token) != None:
            category = 'for condition'
        if re.search(self.loopcondwhile, token) != None:
            category = 'while condition'
        if re.search(self.breakkey, token) != None:
            category = 'break'
        if re.search(self.funcstart, token) != None:
            category = 'function start'
        if re.search(self.funcend, token) != None:
            category = 'function end'
        if re.search(self.params, token) != None:
            category = 'parameter'
        if re.search(self.returnkey, token) != None:
            category = 'function return'
        if re.search(self.funccall, token) != None:
            category = 'function call'
        if re.search(self.linebreak, token) != None:
            category = 'linebreak'
        if re.search(self.singlecomments, token) != None:
            category = 'comment'
        if re.search(self.multicommentstart, token) != None:
            category = 'start multi comment'
        if re.search(self.multicommentend, token) != None:
            category = 'end multi comment'

        return [token, category]


# testing
# tokens = LOLCODE_Interpreter().tokenize_line('SUM OF 5 AN 7 BTW MEOWMEOW MEOW\n') #SUM OF, 5, AN, 7\n
# LOLCODE_Interpreter().tokenize_line('ALL OF x AN y AN z MKAY\n') #ALL OF, x, AN, y, AN, z, MKAY\n
# LOLCODE_Interpreter().tokenize_line('BOTH SAEM x AN BIGGR OF x AN y\n') #BOTH SAEM, x, AN, BIGGR OF, x, AN, y\n
# LOLCODE_Interpreter().tokenize_line('VISIBLE "HELLO WORLD" + "MEOW MEOW"\n') #VISIBLE, "HELLO WORLD", +, "MEOW MEOW"\n

'''
SUM OF 5 AN 7 BTW MEOWMEOW MEOW
ALL OF x AN y AN z MKAY
BOTH SAEM x AN BIGGR OF x AN y
VISIBLE "HELLO WORLD" + "MEOW MEOW"
'''

# starts the ui
LOLCODE_Interpreter().mainloop()
