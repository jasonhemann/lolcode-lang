"""
# LOLCODE Interpreter written in Python
    
    Authors:
        Diño, John Matthew D.
        Mandap, Clarence P.
        Pore, Richmond Michael B.

    Components/ modules:
        lexer.py - Handles tokenization and lexical analysis
        parser.py - Handles parsing of keyword/variable and semantic analysis
        interpreter.py - Ties all components together and handles program execution

    GUI Framework:
        Kivy (https://kivy.org/)
"""
# Kivy functions used
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label

# Python functions used
from io import StringIO

import sys
from lexer import Lexer
import parser
import re

lexeme_table=[]

class MainWindow(App):
    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)
        self.current_file = None
        self.output_buffer = StringIO()

        self.current_line_index = 0  # track the current line index
        self.lines = []  # store lines from the file
        self.lexer = Lexer()  # create the lexer instance here

        self.tokens_display = TextInput(readonly=True, multiline=True)  # Initialize tokens_display here

    # function to create main interpreter UI
    def build(self):
        layout = FloatLayout()

        # File Explorer
        file_chooser = FileChooserListView(on_submit=self.load_file)  # FileChooser object for the File Explorer
        file_chooser.size_hint = (0.3, 0.5)
        file_chooser.pos_hint = {'x': 0, 'top': 1} 
        layout.add_widget(file_chooser)

        # Text Editor
        self.text_editor = TextInput(multiline=True, background_color=(1, 1, 1, 1), foreground_color=(0, 0, 0, 1))
        self.text_editor.size_hint = (0.3, 0.5)
        self.text_editor.pos_hint = {'x': 0.3, 'top': 1}
        layout.add_widget(self.text_editor)

        # Save Button for Text Editor
        save_button = Button(text='Save', size_hint=(0.3, None), height=50)
        save_button.pos_hint = {'x': 0.3, 'y': 0.5}
        save_button.bind(on_press=self.save_file)
        layout.add_widget(save_button)

        # Lexeme Table
        self.tokens_display.size_hint = (0.25, 0.5)
        self.tokens_display.pos_hint = {'x': 0.6, 'top': 1}
        layout.add_widget(self.tokens_display)

        # Symbol Table
        self.symbol_table_display = TextInput(readonly=True, multiline=True)
        self.symbol_table_display.size_hint = (0.25, 0.5)
        self.symbol_table_display.pos_hint = {'x': 0.85, 'top': 1}
        layout.add_widget(self.symbol_table_display)

        # Console
        console_section = BoxLayout(orientation='vertical', size_hint=(1, 0.5), pos_hint={'x': 0, 'y': 0})
        self.console_output = TextInput(readonly=True, multiline=True, text="")  # Initialize with an empty string
        console_section.add_widget(self.console_output)  # add output area to Console
        
        # Run/Execute Button for Console
        run_button = Button(text='Execute', size_hint_y=None, height=50)
        run_button.bind(on_press=self.run_lolcode)  # Bind the run button to the run_lolcode method
        console_section.add_widget(run_button)  # add a run button to Console
        layout.add_widget(console_section)  # Add the console section to the layout

        return layout
    
    # File Explorer functions
    def load_file(self, instance, selection, touch=None, **kwargs):
        if selection:  # Check if a file is selected
            self.current_file = selection[0]
            with open(self.current_file, 'r') as file:  # Open the selected file
                self.text_editor.text = file.read()  # Load contents to the text editor

    def save_file(self, instance):
        if self.current_file:
            with open(self.current_file, 'w') as file:  # Open in write mode
                file.write(self.text_editor.text)  # Save the contents to the file

    def update_console(self, message):
        """Update the console output area with a new message."""
        if self.console_output.text is None:  # Check if text is None
            self.console_output.text = ""
        self.console_output.text += f"{message}\n"  # Append the new message to the console output

    def update_tokens_display(self, tokens):
        """Update the tokens display widget with the current tokens."""
        tokens_str = "\n".join([f"{token[0]}: {token[1]}" for token in tokens])  # Format tokens for display
        self.tokens_display.text += tokens_str + "\n"  # Append the new tokens to the display

    def update_symbol_table_display(self, parseinfo):
        """Update the symbol table display widget."""
        if parseinfo == None:
            self.symbol_table_display.text += "ERROR: No tokens to parse"
            self.symbol_table_display.text += f"{parseinfo}"
            return
        self.symbol_table_display.text += "Current Symbol Table:\n"
        for key, value in parseinfo.items():
            self.symbol_table_display.text += (f"{key}: {value}\n")

    # Main LOLCODE Interpreter
    def interpreter(self, filename):
        # We first check if the file extension is .lol
        if not filename.endswith('.lol'):
            self.update_console("Error: File must have '.lol' extension")  # Update console instead of print
            return  # Exit the function
        try:
            with open(filename, 'r') as file:
                # Read the first line and check for HAI
                starting = file.readline().strip()
            
                if starting != "HAI":
                    self.update_console("Error: Invalid Starting Keyword")  # Update console instead of print
                    return  # Exit the function
                for line in file:
                    line = line.strip()  # Removes the white spaces around the line
                    if line:  # Skip empty lines
                        tokenize = self.lexer.definer(line)  # Tokenize the line
                        
                        if tokenize!=None:
                            if tokenize!=[]:
                                lexeme_table.append(tokenize)

                        # Update the tokens display with the current line's tokens
                        self.update_tokens_display(tokenize)

                for index in range(len(lexeme_table)):
                    parse = parser.Parser(lexeme_table[index],lexeme_table,index, main_window = self)
                    parse_tree = parse.parse()
                    
                self.update_symbol_table_display(parser.symbol_table)

        except FileNotFoundError:
            self.update_console(f"Error: Could not find file '{filename}'")  # Update console instead of print

    def run_lolcode(self, instance):
        """Method to execute the LOLCODE script."""
        if self.current_file:
            # Call the interpreter with the current file
            self.interpreter(self.current_file)

    def prompt_for_input(self, variable_name):
        input_box = TextInput(hint_text=f"Enter value for {variable_name}", multiline=False)
        submit_button = Button(text="Submit", size_hint_y=None, height=50)
        cancel_button = Button(text="Cancel", size_hint_y=None, height=50)

        def on_submit(instance):
            value = input_box.text.strip()  # Get input from user
            self.console_output.text += f"value is {value}\n"
            if value:  # Check if the input is not empty
                parser.symbol_table["IT"] = str(value)
                popup.dismiss()
            else:
                self.console_output.text += "Error: Input cannot be empty.\n"

        def on_cancel(instance):
            popup.dismiss()  # Close popup

        submit_button.bind(on_press=on_submit)
        cancel_button.bind(on_press=on_cancel)

        popup_content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        popup_content.add_widget(input_box)
        popup_content.add_widget(submit_button)
        popup_content.add_widget(cancel_button)

        popup = Popup(title="Input Required", content=popup_content, size_hint=(0.8, 0.4))
        popup.open() 

if __name__ == '__main__':
    MainWindow().run()