# LOLCODE Interpreter in Python 🐱‍💻

## 📊 Project Overview

This LOLCODE interpreter processes code written in the meme-inspired LOLCODE language. It supports variable handling, arithmetic, logical operations, and conditional statements using a multi-phase structure: **Lexical Analysis**, **Parsing**, and **Evaluation**.

## 🔗 How the LOLCODE Interpreter Works

The interpreter reads and executes LOLCODE source files through a series of well-defined steps:

- **Lexical Analysis**: Break source code into tokens.
- **Parsing**: Validate token sequences and construct internal representations.
- **Evaluation**: Execute instructions using variables, expressions, and control flow.

## 🎯 Project Goals

- Design and build a functional LOLCODE interpreter.
- Learn about lexical analysis, parsing, and evaluation.
- Practice team collaboration using version control (Git).
- Create well-structured documentation and test cases.
- Optionally, add bonus features like nested expression parsing, error reporting, and GUI support.

## ✅ Features to Implement

- **Program start/end**: `HAI`, `KTHXBYE`
- **Variable declaration**: `I HAS A var`, optionally with `ITZ <value>`
- **Assignment**: `var R <value or expression>`
- **Input/Output**: `VISIBLE`, `GIMMEH`
- **Data types**: `NUMBR` (integer), `NUMBAR` (float), `YARN` (string), `TROOF` (boolean)
- **Arithmetic operations**: `SUM OF`, `DIFF OF`, `PRODUKT OF`, `QUOSHUNT OF`, `MOD OF`, `BIGGR OF`, `SMALLR OF`
- **Logical operations**: `AN`, `OR`, `BOTH SAEM`, `DIFFRINT`
- **Control flow**: `BTW`, `OMG`, `BTW`, `OMGWTF`
  
## 🎉 Example Code

Here is a basic LOLCODE script that prints a message and performs some arithmetic:

```lolcode
HAI
  I HAS A num
  I HAS A result
  num ITZ 5
  result R SUM OF num AN 3
  VISIBLE "The result is: " AN result
KTHXBYE
