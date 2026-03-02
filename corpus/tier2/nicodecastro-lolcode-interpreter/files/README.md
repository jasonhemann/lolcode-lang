# lolcode-interpreter

[![Python](https://img.shields.io/badge/python-3.12.4-blue)]()
[![CustomTkinter](https://img.shields.io/badge/customtkinter-5.2.2-blue)](https://github.com/tomschimansky/customtkinter)
[![License MIT](https://img.shields.io/badge/license-MIT-blue)](https://github.com/nicodecastro/lolcode-interpreter/blob/main/LICENSE.txt)

A LOLCODE interpreter built using Python 3 and customtkinter, featuring a GUI for editing and executing LOLCODE programs. Developed as a coursework for CMSC 124 Design and Implementation of Programming Languages, it includes support for lexical analysis, syntax parsing, semantic analysis, and error handling.

## Table of Contents

- [lolcode-interpreter](#lolcode-interpreter)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Screenshots](#screenshots)
  - [License](#license)

## Installation

1. Install [Python 3](https://www.python.org/downloads/) (Preferably Python 3.12.4) and pip
  - To check if they are already installed type the following commands:
    - `python --version`
    - `pip -V`
2. Install the dependencies in requirements.txt
   1. In your terminal, navigate to the project directory
   2. Install all the packages using the command: `pip install -r requirements.txt`

## Usage

To run the application through the terminal:

- If you have make installed, run the command: `make`
- Otherwise, run either of the following commands: `py ./source\ code/main.py` or `python ./source\ code/main.py`

## Screenshots

![Image of the Interpreter with No File Selected](image-1.png)  

![Image of the Interpreter with a Sample File Executed](image.png)  

## License

Copyright (c) Nico De Castro. All rights reserved.

Licensed under the [MIT](LICENSE.txt) license.
