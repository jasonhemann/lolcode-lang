# LOLCODE-interpreter
- **Lexer/Tokenizer**: Charles Vincent A. Tabuzo
- **Parser**: Christian Gabriel Plazo
- **Evaluator**: Arlene B. Bongalos
- **I/O + Conditionals**: Mark Neil Teves
- **Tester/Docs**: Janice Arcilla

## 1. Overview

The LOLCODE Interpreter is a simplified interpreter for programs written in a selected subset of LOLCODE syntax. The interpreter supports:
- **Program Structure:** Programs must begin with `HAI` and end with `KTHXBYE`.
- **Variable Declarations and Assignments:** Create variables using `I HAS A <var>` (with optional `ITZ <value>`) and update them with `<var> R <value or expression>`.
- **Input/Output Operations:** Use `GIMMEH` for input and `VISIBLE` for output.
- **Data Types:** Supports NUMBR (integers), NUMBAR (floats), YARN (strings), and TROOF (booleans, represented as WIN/FAIL).
- **Arithmetic Operations:** Operators such as `SUM OF`, `DIFF OF`, `PRODUKT OF`, `QUOSHUNT OF`, `MOD OF`, `BIGGR OF`, and `SMALLR OF`.
- **Logical Operations:** Operators like `BOTH SAEM`, `DIFFRINT`, `NOT`, `BOTH OF`, and `EITHER OF`.
- **Conditionals:** Implements simple IF-THEN-ELSE with `O RLY?`, `YA RLY`, `NO WAI`, and `OIC`.

This project was developed as a team exercise to learn about lexical analysis, parsing, evaluation, and team collaboration using Git.

---

## 2. Project Architecture

The interpreter is comprised of three main components:

### a. Lexical Analysis (Tokenizer)
- **Purpose:** Reads `.lol` files and converts lines of LOLCODE into tokens.
- **Highlights:**  
  - Recognizes multi-word tokens such as `I HAS A`, `SUM OF`, `O RLY?`, etc.
  - Detects literals for numbers (NUMBR and NUMBAR), strings (YARN), and booleans (TROOF).
  - Provides line and column numbers in tokens to aid in error reporting.

### b. Parsing (Abstract Syntax Tree Construction)
- **Purpose:** Uses recursive descent parsing to convert the token stream into an Abstract Syntax Tree (AST).
- **Highlights:**  
  - Enforces correct program structure (checking the `HAI` starter and `KTHXBYE` terminator).
  - Builds nodes for variable declarations, assignments, I/O commands, arithmetic expressions, logical expressions, and control flow statements (conditionals).
  - Delivers informative error messages with context.

### c. Evaluation (Execution Engine)
- **Purpose:** Walks the AST and executes the program.
- **Highlights:**  
  - Maintains a symbol table (environment) for declared variables.
  - Evaluates arithmetic and logical expressions recursively.
  - Processes conditionals by evaluating a special stored value (`_it`).
  - Provides user interaction through terminal I/O.

---

## 3. Setup and Installation

### Prerequisites
- **Python 3.x:** Install from [python.org](https://www.python.org/downloads/).
- **Git:** Optional (highly recommended) for version control.
- **Visual Studio Code (VSCode):** Provides an integrated environment for editing, running, and debugging the code.

### Installation Steps

1. **Clone or Download the Repository:**
   - **Using Git:**
     ```bash
     git clone <repository-url>
     cd LolcodeInterpreterProject
     ```
   - **Using ZIP:**  
     Download the project archive, extract it, and open the resulting folder.

2. **Project Structure Check:**  
   Ensure your directory resembles the following:
   LolcodeInterpreterProject/
├── lolcode_interpreter.py   # The main Python source code
├── hello.lol                # Sample test file 1
├── variables.lol            # Sample test file 2
├── arithmetic.lol           # Sample test file 3
├── condition.lol            # Sample test file 4
├── input_output.lol         # Sample test file 5
├── README.md                # Documentation (this guide may be part of it)
└── reflections/             # Team member reflection files (if applicable)


3. **Open the Project in VSCode:**
- Launch VSCode.
- Select **File > Open Folder...** and choose your project folder.

4. **Ensure Python is Accessible:**
- Open the integrated terminal in VSCode (using <kbd>Ctrl</kbd>+<kbd>`</kbd> on Windows/Linux or <kbd>Cmd</kbd>+<kbd>`</kbd> on macOS).
- Verify Python installation:
  ```bash
  python --version
  ```
- If necessary, use `python3` instead of `python`.

---

## 4. Running the Interpreter

### a. Running from the Command Line
1. **Open the Terminal:**  
In your project folder, open the terminal.
2. **Execute the Interpreter:**  
Run the following command to execute a LOLCODE file:
```bash
python lolcode_interpreter.py hello.lol
```

### b. Using the Web Interface
1. **Install Streamlit:**
```bash
pip install streamlit
```

2. **Launch the Web Interface:**
```bash
streamlit run lolcode_web.py
```

The web interface provides a user-friendly way to:
- Upload `.lol` files or write LOLCODE directly in the browser
- View step-by-step execution process:
  - Lexical analysis with token visualization
  - Parsing results
  - Program execution and output
- Examine variable environment and program state
- Access helpful LOLCODE examples and documentation

Your default web browser will automatically open to `http://localhost:8501` where you can interact with the LOLCODE interpreter.

# Locode-interpreter is Already Deployed 
You can run this directly to your browser using your broweser
by copy and pasting this URL
```bash
https://lolcode-interpreter.streamlit.app/
```
