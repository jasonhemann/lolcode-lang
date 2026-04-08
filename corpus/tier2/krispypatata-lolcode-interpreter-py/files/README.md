# lolcode-interpreter-py
By Keith Ginoel Gabinete, 2025

## OVERVIEW
<p align="justify">
This is a LOLCODE interpreter built using Python and tkinter (for the GUI). It is based on the specifications from http://www.lolcode.org/. While the features may not exactly match the original, this project aims to closely mimic its behavior. The author’s purpose in building this project is to create a simple programming language from scratch and to understand the phases of lexer, parser, and interpreter.
</p>

### Author’s Note:
<p align="justify">
Originally, this was a group project at the author’s university. Although the team submitted a satisfactory version, the author decided to revive this project to improve it by fixing bugs and adding new features. While it started as a group project, it is worth noting that the code retrieved from the original repository includes only the work done by the author. In other words, contributions from other team members were not transferred to this repository. 
<br/><br/>
<b>tl;dr</b>: This is a solo project.
</p>

## Prerequisites
- [Python 3](https://www.python.org/downloads/)
- [tkinter](https://docs.python.org/3/library/tkinter.html)

## How to Run
1. Clone the repository to your local machine:  
   `git clone https://github.com/krispypatata/lolcode-interpreter-py.git`

2. Open a terminal in the project’s root directory.

3. Run the program by typing:  
   `python3 lolcode.py`

4. Alternatively, if you have `make` installed, simply run:  
   `make`

5. To test the program without the GUI:  
   - Open `lolcode.py` in your code editor.  
   - In the `__main__` section, comment out the GUI-related statements and uncomment the call to `test_run_lolcode()`.  
   - You can modify the `test_run_lolcode` function as needed for testing.  
   - Alternatively, you can also use the `handle_run_lolcode()` function.

## Interpreter Features
This section outlines the features that are implemented or not yet implemented in this version of the LOLCODE interpreter.
For detailed information on the original LOLCODE specifications, please refer to the [official LOLCODE spec](https://github.com/justinmeza/lolcode-spec/tree/master).

### 1. File Structure and Formatting

* **File Extension**: `.lol`
* **Program Start**: `HAI`
* **Program End**: `KTHXBYE`
* **Comments**:

  * Single-line: Start with `BTW`
  * Multi-line: Enclosed between `OBTW` and `TLDR`
* **Statement Rules**:

  * One statement per line
  * No support for comma-separated statements
  * Indentation and extra spaces are ignored
* **Function Definitions**: Must be within `HAI` and `KTHXBYE`

### 2. Variables

* **Declaration Block**: Between `WAZZUP` and `BUHBYE`
* **Declaration Syntax**: `I HAS A <variable>`
* **Initialization**: Optional, using `ITZ`
* **Naming Rules**:

  * Start with a letter
  * Can include letters, numbers, and underscores
  * No spaces or special characters
* **Dynamic Typing**: Variables can change types during execution (just like in python)
* **Implicit Variable**: `IT` holds the result of the last evaluated expression
    
*Note*: For VISIBLE (print) statements (for example, `VISIBLE 2 + " - " + 3 + " = " + DIFF OF 2 AN 3`), the result will be stored in `IT` as the full output string (`2 - 3 = -1`).

### 3. Data Types

* **NOOB**: Uninitialized variable
* **NUMBR**: Integer (e.g., `42`)
* **NUMBAR**: Floating-point number (e.g., `3.14`)
* **YARN**: String enclosed in double quotes (e.g., `"hello"`)
* **TROOF**: Boolean values `WIN` (true) or `FAIL` (false)

### 4. Input and Output

* **Output**: `VISIBLE` prints to the console

  * Supports multiple arguments separated by `AN` or `+`
  * Automatically adds a newline after output
* **Input**: `GIMMEH <variable>` reads input as a string and assigns it to the variable

### 5. Operations

#### 5.1 Arithmetic Operations

* **Addition**: `SUM OF <a> AN <b>`
* **Subtraction**: `DIFF OF <a> AN <b>`
* **Multiplication**: `PRODUKT OF <a> AN <b>`
* **Division**: `QUOSHUNT OF <a> AN <b>`
* **Modulo**: `MOD OF <a> AN <b>`
* **Maximum**: `BIGGR OF <a> AN <b>`
* **Minimum**: `SMALLR OF <a> AN <b>`

*Note*: Operands are automatically typecasted to `NUMBR` or `NUMBAR` as needed.

#### 5.2 String Concatenation

* **Concatenation**: `SMOOSH <a> AN <b> AN ...`
  * Can also use `+` as a separator
  * Converts all operands to strings before concatenation

#### 5.3 Boolean Operations

* **AND**: `BOTH OF <a> AN <b>`
* **OR**: `EITHER OF <a> AN <b>`
* **XOR**: `WON OF <a> AN <b>`
* **NOT**: `NOT <a>`
* **ALL OF**: `ALL OF <a> AN <b> AN ... MKAY`
* **ANY OF**: `ANY OF <a> AN <b> AN ... MKAY`

*Note*: Non-boolean operands are implicitly cast to `TROOF`.

#### 5.4 Comparison Operations

* **Equal**: `BOTH SAEM <a> AN <b>`
* **Not Equal**: `DIFFRINT <a> AN <b>`
* **Greater Than or Equal**: `BOTH SAEM <a> AN BIGGR OF <a> AN <b>`
* **Less Than or Equal**: `BOTH SAEM <a> AN SMALLR OF <a> AN <b>`
* **Greater Than**: `DIFFRINT <a> AN SMALLR OF <a> AN <b>`
* **Less Than**: `DIFFRINT <a> AN BIGGR OF <a> AN <b>`

*Note*: No automatic typecasting; operands must be of comparable types.

### 6. Typecasting

* **Implicit Casting**:

  * `NOOB` to `TROOF`: `FAIL`
  * `TROOF` to `NUMBR`: `WIN` → `1`, `FAIL` → `0`
  * `NUMBAR` to `NUMBR`: Truncates decimal
  * `NUMBR` to `NUMBAR`: Converts to float
* **Explicit Casting**:

  * `MAEK <value> A <type>`: Casts value to specified type
  * `IS NOW A`: Changes the type of a variable

### 7. Statements

#### 7.1 Expression Statements

* Evaluating an expression without assignment stores the result in `IT`

#### 7.2 Assignment Statements

* Syntax: `<variable> R <expression>`

#### 7.3 Conditional Statements

* **Structure**:

  ```
  <expression>
  O RLY?
    YA RLY
      <code block>
    NO WAI
      <code block>
  OIC
  ```
* Executes `YA RLY` block if `IT` is `WIN`; otherwise, executes `NO WAI` block
* `MEBBE` (else-if) clauses are **not yet implemented**

#### 7.4 Switch-Case Statements

* **Structure**:

  ```
  WTF?
    OMG <value>
      <code block>
    OMGWTF
      <default code block>
  OIC
  ```
* Compares `IT` to each `OMG` value; executes matching block
* `OMGWTF` is the default case
* Use `GTFO` to exit a case block

#### 7.5 Loops

* **Structure**:

  ```
  IM IN YR <label> <operation> YR <variable> [TIL|WILE <condition>]
    <code block>
  IM OUTTA YR <label>
  ```
* `<operation>`: `UPPIN` (increment) or `NERFIN` (decrement)
* `TIL <condition>`: Loop until condition is `WIN`
* `WILE <condition>`: Loop while condition is `WIN`
* Use `GTFO` to break out of the loop

### 8. Functions

#### 8.1 Definition

* **Structure**:

  ```
  HOW IZ I <function name> [YR <param1> [AN YR <param2> ...]]
    <code block>
  IF U SAY SO
  ```
* Fixed number of parameters
* Parameters are local to the function
* No access to variables outside the function scope

#### 8.2 Returning Values

* `FOUND YR <expression>`: Returns the value of the expression and exits the function
* `GTFO`: Exits the function immediately without returning a value
* If no `FOUND` is executed, the function returns `NOOB` by default
* The returned value is stored in `IT`

#### 8.3 Calling Functions

* Call functions using:

  ```
  I IZ <function name> [YR <expression1> [AN YR <expression2> ...]] MKAY
  ```

* Expressions (or arguments) are evaluated first before the function executes.



## Lexemes & Literals Summary  
### Lexemes Table

| **Lexeme**           | **Tag Description**                    |
|----------------------|----------------------------------------|
| `HAI`                | Program Start Delimiter                |
| `KTHXBYE`            | Program End Delimiter                  |
| `WAZZUP`             | Variable Declaration Start Delimiter   |
| `BUHBYE`             | Variable Declaration End Delimiter     |
| `I HAS A`            | Variable Declaration                   |
| `ITZ`                | Variable Initialization                |
| `R`                  | Assignment Keyword                     |
| `SUM OF`             | Addition Operator                      |
| `DIFF OF`            | Subtraction Operator                   |
| `PRODUKT OF`         | Multiplication Operator                |
| `QUOSHUNT OF`        | Division Operator                      |
| `MOD OF`             | Modulus Operator                       |
| `BIGGR OF`           | Greater Than Operator                  |
| `SMALLR OF`          | Less Than Operator                     |
| `BOTH OF`            | AND Operator                           |
| `EITHER OF`          | OR Operator                            |
| `WON OF`             | XOR Operator                           |
| `NOT`                | NOT Operator                           |
| `ANY OF`             | ANY Operator                           |
| `ALL OF`             | ALL Operator                           |
| `BOTH SAEM`          | Equality Operator                      |
| `DIFFRINT`           | Inequality Operator                    |
| `SMOOSH`             | String Concatenate Operator            |
| `MAEK A`             | Typecast Operator                      |
| `IS NOW A`           | Typecast IS NOW A Operator             |
| `AN`                 | Operand Connector                      |
| `YR`                 | Parameter Variable                     |
| `AN YR`              | Additional Parameter Variable          |
| `VISIBLE`            | Print Statement                        |
| `+`                  | Print Statement Delimiter              |
| `GIMMEH`             | Input Statement                        |
| `O RLY?`             | Conditional Start Delimiter            |
| `YA RLY`             | If Clause                              |
| `MEBBE`              | Else-If Clause                         |
| `NO WAI`             | Else Clause                            |
| `OIC`                | Conditional End Delimiter              |
| `WTF?`               | Switch-Case Start Delimiter            |
| `OMG`                | Case Clause                            |
| `OMGWTF`             | Switch-Case End Delimiter              |
| `IM IN YR`           | Loop Start Delimiter                   |
| `UPPIN`              | Increment Operator                     |
| `NERFIN`             | Decrement Operator                     |
| `TIL`                | Until Loop                             |
| `WILE`               | While Loop                             |
| `IM OUTTA YR`        | Loop End Delimiter                     |
| `HOW IZ I`           | Function Start Delimiter               |
| `IF U SAY SO`        | Function End Delimiter                 |
| `GTFO`               | Function Return                        |
| `FOUND YR`           | Function Return Value                  |
| `I IZ`               | Function Call                          |
| `MKAY`               | Statement End Delimiter                |
| Identifier (e.g. `var1`) | Identifier                        |
| *EOF (implicit)*     | End of File                            |


### Literal Table

| **Literal Example**   | **Tag Description**  |
|-----------------------|----------------------|
| `42`                  | NUMBR (Integer)      |
| `3.14`                | NUMBAR (Float)       |
| `"Hello"`             | YARN (String)        |
| `WIN`, `FAIL`         | TROOF (Boolean)      |
| `NOOB`                | NULL                 |
| `NUMBR`, `NUMBAR`, `YARN`, `TROOF` | LITERAL_TYPE |


## GUI Features
Employs a dark theme for better visual comfort.

### Layout Overview

**Window (1280 × 720, default on launch)**  
![Default Window Screenshot](screenshots/01_window-default.png)

**Window (maximized)**  
![Maximized Window Screenshot](screenshots/01_window-maximized.png)


#### Top Left Panel: Code Editor View

1. **File Chooser Button**

   * Allows users to open a file with a `.lol` extension.
   * The contents of the selected file are immediately displayed in the code editor.

2. **Code Editor**

   * Displays LOLCODE files.
   * Code is editable.
   * Line numbers are displayed and update automatically when new lines are added.
   * Line numbers adjust in real time based on the scrollbar view.
   * Horizontal scrollbars appear if the code line exceeds the editor’s width.
   * Context menu on right-click with the following options:

     * Copy
     * Cut
     * Paste
     * Select All
   * Keyboard shortcuts supported for these actions.

**Screenshots:**  
*![Code Editor Screenshot](screenshots/02_editor.png)*  
*![Code Editor's File Chooser Screenshot](screenshots/02_editor-file-chooser.png)*


#### Top Right Panel: Table Views

1. **Lexeme Table**

   * Displays: Lexeme | Classification | Line #

2. **Symbol Table**

   * Displays: Symbol | Value

> **Note:** If content exceeds the column width, a tooltip appears showing the full content of the cell.

**Screenshot:**  
*![Table Views Screenshot](screenshots/03_table-views.png)*



#### Center: Execute Button

* Executes the LOLCODE displayed in the code editor.

**Screenshot:**  
*![Execute Button Screenshot](screenshots/04_execute.png)*



#### Bottom Panel: Console/Terminal

* Displays output from the interpreter.
* **Extra Feature:** Right-clicking a selected text copies it to the clipboard.

**Screenshot:**  
*![Console Screenshot](screenshots/05_console.png)*



### Modal: User Input

* A pop-up modal (non-resizable) appears when input is required.

**Screenshot:**  
*![Input Modal Screenshot](screenshots/06_get-input.png)*



