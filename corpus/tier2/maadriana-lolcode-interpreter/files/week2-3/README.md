# Week 2–3 – LOLCODE Interpreter (Python Project)

This folder contains the complete implementation of our LOLCODE interpreter, built and finalized during Weeks 2 and 3.

---

## Implemented Features

- **Lexer** – Tokenizes LOLCODE keywords and literals
- **Parser** – Builds an abstract syntax tree (AST)
- **Interpreter** – Executes logic for:
  - Variables & assignments
  - Input/output
  - Arithmetic & logical expressions
  - Conditionals
- **Semantic Analyzer** – Checks variable declarations and usage
- **Bonus Features**:
  - `SMOOSH` string concatenation
  - `WIN`/`FAIL` (TROOF)
  - Nested expressions
  - Error reporting with line numbers
  - GUI runner (Tkinter)
  - `unittest` test suite

---

## How to Run

### Run manually with specific `.lol` file:

```bash
python main.py test/conditional.lol
python main.py test/hello_world.lol
python main.py test/final_test.lol
```

### Run all test files automatically:

```bash
python test_interpreter.py
```

### Run the GUI version:

```bash
python gui_runner.py
```

---

## Folder Contents

- `main.py` – Entry point (command-line runner)
- `interpreter.py` – Core evaluator logic
- `parser.py` – AST builder
- `lexer.py` – Tokenizer
- `semantic_analyzer.py` – Error checks
- `gui_runner.py` – Optional Tkinter GUI
- `test/` – Folder with working `.lol` test files
- `test_interpreter.py` – Batch test runner
- `test/test_interpreter_unittest.py` – Python `unittest` suite

---

## Notes

- All `.lol` files follow simplified LOLCODE syntax.
- `final_test.lol` demonstrates most major features.
- Compatible with both CLI and GUI interfaces.
