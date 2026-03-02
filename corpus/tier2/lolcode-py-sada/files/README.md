## TayLOL Sheesh: A LOLCode Interpreter

## Program Description
An interpreter for the LOLCode Programming Language using Python Programming Language. More information regarding LOLCode can be found on the following:
- Specs: https://github.com/justinmeza/lolcode-spec/blob/master/v1.2/lolcode-spec-v1.2.md 
- Website: http://www.lolcode.org/

## Features of Interpreter
1. Lexically analyze the LOLCode
2. Syntactically analyze the LOLCode
3. Semantically analyze the LOLCode

## Installation Guide
1. Install Python Programming Language in your OS.
2. Ensure that TKinter is installed together with Python.

### Installing Python
1. Download the Python installer (https://kinsta.com/knowledgebase/install-python/#windows-1)
2. Run the installer
3. Customize the installation (optional)
4. Install Python
5. Verify the installion
6. Alternate installation via Microsoft Store

source: https://kinsta.com/knowledgebase/install-python/

### Ensuring TKinter is installed
1. The tkinter package (“Tk interface”) is the standard Python interface to the Tk GUI toolkit. 
2. To try if TKinter is really installed you may type this in the command line: python -m tkinter 

source: https://docs.python.org/3.8/library/tkinter.html#:~:text=Running%20python%20%2Dm%20tkinter%20from,documentation%20specific%20to%20that%20version.

## How To Run
1. Open the ui.py file
2. Run ui.py file
3. Use the application

## UI Navigation
![image](https://github.com/RamosQuim/CMSC124_Laboratory_Project/assets/125535569/e27a1358-d893-4726-af4c-539f4b032d4c)
1. **Open File:** Can open a LOL file in the Text Editor
2. **Lexeme Table:** Will provide all tokens collected after the Lexical Analyzer is ran
3. **Symbol Table:** Will provide all variable identifiers and the implicit variable with corresponding values
4. **Text Editor:** A field where LOLCode is inserted
5. **Execute:** This will run activate Lexical, Syntax, and Semantic Analyzer
6. **Console:** This is where syntaxErrors and result of LOLCode (if there is any) will prompt
