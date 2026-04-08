# lexical analyzer for the LOLCODE language
from parserFunction import LOLCodeParser
import sys
import re
from macros import LOLMacros
import tkinter as tk
from tkinter import filedialog, Text, messagebox, ttk


class LOLCodeLexer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.tokens = []
        self.variable_names = set()
        self.string_literals = []
        self.macros = LOLMacros()

    def tokenize(self):
        # Define regular expressions for LOLCODE tokens
        token_patterns = [
            # keywords
            (r'^\b(HAI)\b', 'Program Start Delimiter'),
            (r'^\b(KTHXBYE)\b', 'Program End Delimiter'),
            (r'^\b(WAZZUP)\b', 'Variable Declaration Start Delimiter'),
            (r'^\b(BUHBYE)\b', 'Variable Declaration End Delimiter'),
            (r'^\bBTW\b', 'Single Line Comment Delimiter'),
            (r'^\b(OBTW)\b', 'Multi Line Comment Start Delimiter'),
            (r'^\b(TLDR)\b', 'Multi Line Comment End Delimiter'),
            (r'^\b((I HAS A))\b', 'Variable Declaration'),
            (r'^\bITZ\b', 'Variable Assignment'),
            (r'^\bR\b', 'Assignment Operator'),
            (r'^\b(SUM OF)\b', 'Addition Operator'),
            (r'^\b(DIFF OF)\b', 'Subtraction Operator'),
            (r'^\b(PRODUKT OF)\b', 'Multiplication Operator'),
            (r'^\b(QUOSHUNT OF)\b', 'Division Operator'),
            (r'^\b(MOD OF)\b', 'Modulo Operator'),
            (r'^\b(BIGGR OF)\b', 'Max Operator'),
            (r'^\b(SMALLR OF)\b', 'Min Operator'),
            (r'^\b(BOTH OF)\b', 'Logical AND Operator'),
            (r'^\b(EITHER OF)\b', 'Logical OR Operator'),
            (r'^\b(WON OF)\b', 'Logical XOR Operator'),
            (r'^\b(NOT)\b', 'Logical NOT Operator'),
            (r'^\b((ANY OF))\b', 'Infinite Arity Logical OR Operator'),
            (r'^\b((ALL OF))\b', 'Infinite Arity Logical AND Operator'),
            (r'^\b(BOTH SAEM)\b', 'Equality Operator'),
            (r'^\b(DIFFRINT)\b', 'Inequality Operator'),
            (r'^\b(SMOOSH)\b', 'String Concatenation Operator'),
            (r'^\bMAEK\b', 'Type Conversion Operator 1'),
            (r'^\b(AN)\b', 'Operand Connector'),
            (r'^\b(A)\b', 'Type Conversion Operator 2'),
            (r'^\b(IS NOW A)\b', 'Type Conversion Operator 3'),
            (r'^\b(VISIBLE)\b', 'Output Operator'),
            (r'^\b(GIMMEH)\b', 'Input Operator'),
            (r'^\b(O RLY\?)', 'If-Then Statement Start Delimiter'),
            (r'^\b(YA RLY)\b', 'If Statement Delimiter'),
            (r'^\b(MEBBE)\b', 'Else If Statement Delimiter'),
            (r'^\b(NO WAI)\b', 'Else Statement Delimiter'),
            (r'^\b(OIC)\b', 'If-Then Statement End Delimiter'),
            (r'^\b(GTFO)\b', 'Break Statement'),
            (r'^\b(WTF\?)', 'Switch Statement Start Delimiter'),
            (r'^\b(OMG)\b', 'Case Statement Start Delimiter'),
            (r'^\b(OMGWTF)\b', 'Default Case Statement Start Delimiter'),
            (r'^\b((IM IN YR))\b', 'Loop Statement Start Delimiter'),
            (r'^\bUPPIN\b', 'Increment Operator'),
            (r'^\bNERFIN\b', 'Decrement Operator'),
            (r'^\b(YR)\b', 'Loop and Function Argument Declaration'),
            (r'^\bTIL\b', 'Loop Condition Delimiter 1'),
            (r'^\bWILE\b', 'Loop Condition Delimiter 2'),
            (r'^\b(IM OUTTA YR)\b', 'Loop Statement End Delimiter'),
            (r'^\b((HOW IZ I))\b', 'Function Declaration Start Delimiter'),
            (r'^\b(FOUND YR)\b', 'Return Statement Delimiter'),
            (r'^\b((IF U SAY SO))\b', 'Function Declaration End Delimiter'),
            (r'^\b((I IZ))\b', 'Function Call Start Delimiter'),
            (r'^\bMKAY\b', 'Function Call End Delimiter'),
            (r'\+', 'Print Concatenation Operator'),

            # literals
            # Pattern for capturing floating point literals
            (r'^\b-?[0-9]+\.[0-9]+\b', 'NUMBAR'),
            # Pattern for capturing integer literals
            (r'^\b-?[0-9]+\b', 'NUMBR'),
            (r'^\bWIN\b', 'TROOF'),  # Pattern for capturing boolean literals
            (r'^\bFAIL\b', 'TROOF'),  # Pattern for capturing boolean literals
            # Pattern for capturing string literals
            (r'"([^"]*"*(?!""))(?=[^+])*"', 'YARN'),
            # Pattern for capturing type literals
            (r'^\b(NUMBR|NUMBAR|TROOF|YARN)\b', 'Type'),
            # identifiers
            # Pattern for capturing variable identifiers
            (r'^\b[a-zA-Z][a-zA-Z0-9_]*\b', 'Identifier'),
        ]

        # Split the source code into lines
        lines = self.source_code.split('\n')
        # print(f"Lines: {lines}\n\n")

        in_multiline_comment = False

        # Tokenize each line
        for line in lines:
            line = line.strip()
            while line:
                for pattern, token_type in token_patterns:
                    match = re.match(pattern, line)
                    if match:
                        token_value = match.group().strip()  # Remove leading and trailing whitespace

                        if in_multiline_comment:
                            if token_type == self.macros.TLDR:  # 'Multi Line Comment End Delimiter'
                                in_multiline_comment = False
                            line = ''
                            break

                        if token_type == 'YARN':
                            # Remove the start and end quotes
                            token_value = token_value[1:-1]

                        if token_type not in {self.macros.BTW, self.macros.OBTW}:
                            self.tokens.append(
                                {'type': token_type, 'value': token_value})

                        if token_type == 'Identifier':
                            variable_name = match.group().strip()  # Remove leading and trailing whitespace
                            self.variable_names.add(variable_name)
                        elif token_type == 'YARN':
                            string_literal = token_value
                            self.string_literals.append(string_literal)
                        elif token_type == self.macros.BTW:  # 'Single Line Comment Delimiter'
                            line = ''  # Remove the rest of the line
                            break
                        elif token_type == self.macros.OBTW:  # 'Multi Line Comment Start Delimiter'
                            in_multiline_comment = True
                            line = ''  # Remove the rest of the line
                            break

                        # Remove the matched token from the line
                        line = line[match.end():].lstrip()
                        break  # Break the for loop if a match is found
                else:
                    raise ValueError(
                        f"Error: Unrecognized token in line: {line}")
                    break  # Break the while loop if no match is found in the for loop

    def get_tokens(self):
        return self.tokens

    def get_variable_names(self):
        return self.variable_names

    def get_string_literals(self):
        return self.string_literals

    def __str__(self):
        return f"LOLCodeLexer(\ntokens={self.tokens}, \nvariable_names={self.variable_names}, \nstring_literals={self.string_literals})"

# Example usage


# def main():
#     # Check if the correct number of arguments is provided
#     if len(sys.argv) != 2:
#         print("Usage: python main.py <filename>")
#         return

#     # Get the file name from the command-line arguments
#     filename = sys.argv[1]

#     # Now you can use the 'filename' variable in your code
#     print(f"Interpreting LOLCODE file: {filename}")

#     # Add your file processing logic here
#     with open(filename, 'r') as f:
#         file_content = f.read()

#     lexer = LOLCodeLexer(file_content)
#     lexer.tokenize()
#     print(lexer)

#     parser = LOLCodeParser(lexer)
#     parser.parse()
#     for key, value in parser.variables.items():
#         print(f"{key}: {value}")


# if __name__ == "__main__":
#     main()

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        # Upper half
        self.upper_frame = tk.Frame(self)
        self.upper_frame.pack(side="top")

        # First column
        self.first_column = tk.Frame(self.upper_frame)
        self.first_column.pack(side="left", padx=5)

        self.file_location_frame = tk.Frame(self.first_column)
        self.file_location_frame.pack(fill=tk.X)
        self.file_location_frame.grid_columnconfigure(0, weight=1)

        self.file_location = tk.Entry(self.file_location_frame, state="readonly")
        # self.file_location.pack()
        self.file_location.grid(row=0, column=0, sticky="ew", padx=5)

        self.open_file_button = tk.Button(self.file_location_frame, text="Open File", command=self.open_file)
        # self.open_file_button.pack()
        self.open_file_button.grid(row=0, column=1, pady=5)

        self.file_content = tk.Text(self.first_column, height=15)
        self.file_content.pack()

        # Second and third columns frame
        self.columns_frame = tk.Frame(self.upper_frame)
        self.columns_frame.pack(side="left", fill="both", expand=True)

        self.top_label = tk.Label(self.columns_frame, text="LOL CODE Interpreter", pady=5)
        self.top_label.pack()

        # Second column
        self.second_column = tk.Frame(self.columns_frame)
        self.second_column.pack(side="left", fill="both", expand=True, padx=5)

        self.tokens_label = tk.Label(self.second_column, text="Lexemes", pady=5)
        self.tokens_label.pack()

        self.tokens_table = ttk.Treeview(self.second_column, columns=("Lexeme", "Classification"), show="headings")
        self.tokens_table.heading("Lexeme", text="Lexeme")
        self.tokens_table.heading("Classification", text="Classification")
        self.tokens_table.pack()

        # Third column
        self.third_column = tk.Frame(self.columns_frame)
        self.third_column.pack(side="left", fill="both", expand=True, padx=5)

        self.symbol_table_label = tk.Label(self.third_column, text="SYMBOL TABLE", pady=5)
        self.symbol_table_label.pack()

        # self.symbol_table = ttk.Treeview(self.third_column, columns=("Identifier", "Value"), show="headings")
        self.symbol_table = ttk.Treeview(self.third_column, columns=("Identifier", "Value", "Type"), show="headings")
        self.symbol_table.heading("Identifier", text="Identifier")
        self.symbol_table.heading("Value", text="Value")
        self.symbol_table.heading("Type", text="Type")      # Temporary
        self.symbol_table.pack()

        # Execute button
        self.execute_button = tk.Button(self, text="EXECUTE", command=self.execute)
        self.execute_button.pack(fill=tk.X, padx=10, pady=10)

        # Lower half
        self.lower_frame = tk.Frame(self)
        self.lower_frame.pack(side="bottom", fill=tk.X)

        self.console = tk.Text(self.lower_frame, state="disabled")
        self.console.pack(fill=tk.BOTH, expand=True)

    def open_file(self):
        # Open file dialog and update file_location and file_content
        filename = filedialog.askopenfilename()
        with open(filename, 'r') as f:
            file_content = f.read()
        self.file_location.config(state="normal")
        self.file_location.delete(0, tk.END)
        self.file_location.insert(0, filename)
        self.file_location.config(state="readonly")
        self.file_content.delete('1.0', tk.END)
        self.file_content.insert(tk.END, file_content)

    def execute(self):
        # Save file, update tokens_table, symbol_table, and console
        filename = self.file_location.get()
        file_content = self.file_content.get('1.0', tk.END)
        with open(filename, 'w') as f:
            f.write(file_content)
        lexer = LOLCodeLexer(file_content)
        lexer.tokenize()
        self.tokens_table.delete(*self.tokens_table.get_children())
        for token in lexer.get_tokens():
            self.tokens_table.insert('', 'end', values=(token['value'], token['type']))
        # Update symbol_table and console widgets if necessary
        parser = LOLCodeParser(lexer, self.console)
        parser.parse()

        self.symbol_table.delete(*self.symbol_table.get_children())

        # Insert the implicit IT variable at the start of the symbol table
        # self.symbol_table.insert('', 'end', values=('IT', parser.it['value']))
        self.symbol_table.insert('', 'end', values=('IT', parser.it['value'], parser.it['type']))

        for identifier, value in parser.variables.items():
            # if value['value'] == None:
            #     self.symbol_table.insert('', 'end', values=(identifier, value['type']))
            # else:
            #     self.symbol_table.insert('', 'end', values=(identifier, value['value']))
            self.symbol_table.insert('', 'end', values=(identifier, value['value'], value['type']))

        self.console.config(state="normal")
        self.console.delete('1.0', tk.END)
        self.console.insert(tk.END, parser.output)
        self.console.config(state="disabled")

root = tk.Tk()
root.title("FLOWERS MARKET LOLCODE Interpreter")
app = Application(master=root)
app.mainloop()
