import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QTextEdit, 
                           QVBoxLayout, QHBoxLayout, QWidget, QMenuBar, QMenu, 
                           QFileDialog, QDialog, QTableWidget, QTableWidgetItem,
                           QSplitter, QLabel, QHeaderView, QPushButton, QLineEdit, QInputDialog)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QIcon
from lexical_analyzer import find_lexemes_from_string 
from semantic_analyzer import analyze_code, SemanticAnalyzer, SymbolTable

class CreditsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Credits")
        self.setFixedSize(380, 400)

        # Set up the layout
        layout = QVBoxLayout(self)

        # Add the logo
        logo_label = QLabel(self)
        logo_pixmap = QPixmap("./assets/lolcode_logo.png")

        if not logo_pixmap.isNull():
            logo_label.setPixmap(logo_pixmap.scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(logo_label)
        else:
            logo_label.setText("Logo not found!")
            logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(logo_label)


        # Add title
        title_label = QLabel(self)
        title_label.setText(
            "LOLCode Interpreter\n"
        )
        title_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                color: #FFFFFF;
                font-weight: bold;
            }
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add the credits text
        credits_label = QLabel(self)
        credits_label.setText(
            "Developed by Team JJK\n\n"
            "Kyle Nathaniel P. Vinuya\n"
            "Jed Alain Silva\n"
            "Joseffe Ong\n\n"
        )
        credits_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add copyrights
        copyright_label = QLabel(self)
        copyright_label.setText(
            "For project submission in CMSC 124 First Semester A.Y. 2024-2025\n"
            "© University of the Philippines 2024\n"
        )
        copyright_label.setStyleSheet("""
            QLabel {
                font-size: 9px;
                color: #A4A19F;
            }
        """)
        copyright_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(title_label)
        layout.addWidget(credits_label)
        layout.addWidget(copyright_label)
        

class GUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_file = ""
        self.initUI()
        self.semantic_analyzer = SemanticAnalyzer(self) # Initialize the semantic analyzer to get the symbol table

    def initUI(self):
        # Set up the main window
        self.setWindowTitle("CMSC 124 LOLCODE INTERPRETER")
        self.setGeometry(100,100,1200,600)

        # Create top-level widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create horizontal bar above the splitter
        # Holds the current file selected and execute button
        top_bar = QWidget()
        top_bar.setMaximumHeight(40)
        top_bar_layout = QHBoxLayout(top_bar)
        top_bar_layout.setContentsMargins(5,5,5,5)

        self.file_path_display = QLineEdit()
        self.file_path_display.setReadOnly(True)
        self.file_path_display.setPlaceholderText("No file selected")
        self.file_path_display.setMinimumWidth(200)

        self.analyze_button = QPushButton("Execute ✓")
        self.analyze_button.setFixedWidth(100)
        self.analyze_button.clicked.connect(self.analyze_code)

        top_bar_layout.addWidget(self.file_path_display, stretch=1)  
        top_bar_layout.addWidget(self.analyze_button)

        # Create main splitter to hold the upper splitter and console
        main_splitter = QSplitter(Qt.Orientation.Vertical)

        # Create upper splitter to hold the text editor, lexemes display, and symbol table
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Text editor
        self.code_edit = QTextEdit()
        self.code_edit.setPlaceholderText("Enter your LOLCODE here or open a file...")
        splitter.addWidget(self.code_edit)

        # Lexemes
        self.token_table = QTableWidget()
        self.token_table.setColumnCount(3)
        self.token_table.setHorizontalHeaderLabels(['Lexeme', 'Classification', 'Line'])
        self.token_table.verticalHeader().setVisible(False)
        self.token_table.horizontalHeader().setStretchLastSection(True)
        splitter.addWidget(self.token_table)
        self.token_table.setColumnWidth(1, 175)  # Set Classification column to 175 pixels initially

        # Symbol Table
        self.symbol_table = QTableWidget()
        self.symbol_table.setColumnCount(2)
        self.symbol_table.setHorizontalHeaderLabels(['Identifier', 'Value'])
        self.symbol_table.verticalHeader().setVisible(False)
        self.symbol_table.horizontalHeader().setStretchLastSection(True)
        splitter.addWidget(self.symbol_table)

        # Create the console below the splitter 
        self.console_output = QTextEdit()
        self.console_output.setReadOnly(True)
        self.console_output.setPlaceholderText("Console output will appear here...")
        main_splitter.addWidget(splitter)
        main_splitter.addWidget(self.console_output)

        # Add the widgets to the GUI
        layout.addWidget(top_bar)
        layout.addWidget(main_splitter)

        # Create menu bar
        self.create_menu_bar()

        # Connect text changed signal
        self.code_edit.textChanged.connect(self.perform_lexical_analysis)

    # ========================================================
    # Function for requesting input through a pop up
    # ========================================================
    def request_input(self, title, message):
        input_dialog = QInputDialog(self)
        input_dialog.setWindowTitle(title)
        input_dialog.setLabelText(message)
        input_dialog.setTextValue("")

        # Exeute the dialog and get the input
        ok = input_dialog.exec()
        value = input_dialog.textValue()
        return value, ok

    # ========================================================
    # Function for creating the top menu bar
    # ========================================================
    def create_menu_bar(self):
        menubar = self.menuBar()

        # FILE
        file_menu = menubar.addMenu('File')

        # FILE -> Open
        open_action = file_menu.addAction('Open File')
        open_action.triggered.connect(self.open_file)

        # FILE -> Save
        save_action = file_menu.addAction('Save File')
        save_action.triggered.connect(self.save_file)

        # FILE -> Save As
        save_as_action = file_menu.addAction('Save File As')
        save_as_action.triggered.connect(self.save_file_as)

        # FILE -> Exit
        exit_action = file_menu.addAction('Exit')
        exit_action.triggered.connect(self.close) 

        # ABOUT
        about_menu = menubar.addMenu('About')
        about_action = about_menu.addAction('About the Developers')
        about_action.triggered.connect(self.credits)

    # ========================================================
    # Function for opening the file
    # ========================================================
    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Open File', '', 'LOLCODE (*.lol)')

        if filename:
            with open(filename, 'r') as file:
                self.code_edit.setText(file.read()) 
                self.current_file = filename
                self.file_path_display.setText(filename)

            self.semantic_analyzer.symbol_table = SymbolTable()

    # ========================================================
    # Functions for saving the file
    # ========================================================
    def save_file(self):
    # Check if a file is already opened or previously saved
        if self.current_file:
            try:
                with open(self.current_file, 'w') as file:
                    file.write(self.code_edit.toPlainText())  # Save the current text to the same file
                self.write_to_console(f"File saved successfully: {self.current_file}")
            except Exception as e:
                self.write_to_console(f"Error saving file: {str(e)}")
        else:
            self.save_file_as()  # Redirect to Save As if no current file

    def save_file_as(self):
        filename, _ = QFileDialog.getSaveFileName(self, 'Save File As', '', 'LOLCODE (*.lol)')
        if filename:
            try:
                with open(filename, 'w') as file:
                    file.write(self.code_edit.toPlainText())  # Save the text
                self.current_file = filename  # Update current file path
                self.file_path_display.setText(filename)
                self.write_to_console(f"File saved successfully: {filename}")
            except Exception as e:
                self.write_to_console(f"Error saving file: {str(e)}")

    # ========================================================
    # Functions for analyzing the file
    # ========================================================
    def perform_lexical_analysis(self):
        self.token_table.setRowCount(0)
        code = self.code_edit.toPlainText()
        try:
            lexemes = find_lexemes_from_string(code)
            for row, (value, lexeme_type, line_no) in enumerate(lexemes):
                self.token_table.insertRow(row)
                self.token_table.setItem(row, 0, QTableWidgetItem(value))
                self.token_table.setItem(row, 1, QTableWidgetItem(lexeme_type))
                self.token_table.setItem(row, 2, QTableWidgetItem(str(line_no + 1)))
        except Exception as e:
            self.write_to_console(f"Lexical analysis error: {str(e)}")

    def analyze_code(self):
        self.symbol_table.setRowCount(0)
        self.console_output.clear()
        self.semantic_analyzer.symbol_table = SymbolTable()

        code = self.code_edit.toPlainText()
        try:
            # Fetch lexemes from the token table
            lexemes = [
                (
                    self.token_table.item(row, 0).text(),
                    self.token_table.item(row, 1).text(),
                    int(self.token_table.item(row, 2).text())
                )
                for row in range(self.token_table.rowCount())
            ]

            # SYNTAX AND SEMANTIC ANALYSIS
            self.semantic_analyzer.log_console = self.write_to_console
            analyze_code(lexemes, self.semantic_analyzer)
            self.update_symbol_table()

            self.write_to_console(f"Code analyzed successfully.")
        except Exception as e:
            self.write_to_console(f"Error: {str(e)}")

    
    # ========================================================
    # Function for updating the symbol table
    # ========================================================
    def update_symbol_table(self):
        self.symbol_table.setRowCount(0)  # Clear the table

        # Add Variables Header
        row = self.symbol_table.rowCount()
        self.symbol_table.insertRow(row)
        self.symbol_table.setSpan(row, 0, 1, 3)
        header_item = QTableWidgetItem("Variables")
        header_item.setFlags(Qt.ItemFlag.ItemIsEnabled)
        header_item.setBackground(Qt.GlobalColor.lightGray)
        self.symbol_table.setItem(row, 0, header_item)

        # Add variables from symbol table
        for scope_name, scope in self.semantic_analyzer.symbol_table.scopes.items():
            for identifier, attributes in scope.items():
                if attributes.get("type") != "Function":
                    row = self.symbol_table.rowCount()
                    self.symbol_table.insertRow(row)
                    self.symbol_table.setItem(row, 0, QTableWidgetItem(identifier))
                    self.symbol_table.setItem(row, 1, QTableWidgetItem(str(attributes.get("value", "None"))))
                    self.symbol_table.setItem(row, 2, QTableWidgetItem(scope_name))  # Show scope

        # Add IT Variable
        row = self.symbol_table.rowCount()
        self.symbol_table.insertRow(row)
        self.symbol_table.setItem(row, 0, QTableWidgetItem("IT"))
        self.symbol_table.setItem(row, 1, QTableWidgetItem(str(self.semantic_analyzer.symbol_table.get_IT())))
        self.symbol_table.setItem(row, 2, QTableWidgetItem("Global"))

        # Add Functions Header
        row = self.symbol_table.rowCount()
        self.symbol_table.insertRow(row)
        self.symbol_table.setSpan(row, 0, 1, 3)
        header_item = QTableWidgetItem("Functions")
        header_item.setFlags(Qt.ItemFlag.ItemIsEnabled)
        header_item.setBackground(Qt.GlobalColor.lightGray)
        self.symbol_table.setItem(row, 0, header_item)

        # Add functions
        for scope_name, scope in self.semantic_analyzer.symbol_table.scopes.items():
            for identifier, attributes in scope.items():
                if attributes.get("type") == "Function":
                    row = self.symbol_table.rowCount()
                    self.symbol_table.insertRow(row)

                    function_item = QTableWidgetItem(identifier)
                    font = function_item.font()
                    font.setBold(True)
                    function_item.setFont(font)

                    self.symbol_table.setItem(row, 0, function_item)
                    self.symbol_table.setItem(row, 1, QTableWidgetItem("Function"))
                    self.symbol_table.setItem(row, 2, QTableWidgetItem(scope_name))

    # ========================================================
    # Function for writing output to the console
    # ========================================================
    def write_to_console(self, message):
        self.console_output.append(str(message)) # UNCOMMENT IF WE WANT TO APPEND
        # self.console_output.setPlainText(message) # UNCOMMENT IF WE WANT TO REPLACE

    # ========================================================
    # Function for opening the credits window
    # ========================================================
    def credits(self):
        credits_dialog = CreditsDialog(self)
        credits_dialog.exec()
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = GUI()
    gui.show()
    sys.exit(app.exec())