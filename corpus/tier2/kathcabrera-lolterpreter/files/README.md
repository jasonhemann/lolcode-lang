# LOLterpreter
### Authors:
- Diana Kathlyn Cabrera
- Armie Casasola

Usage:
In console, run `py ./gui.py`

Notable Changes:
- Used modified version of lol_lexer.py as the lexer
- Parser doesn't look for NEWLINEs anymore
- `eval_expr()` split into two: `eval_expr()` that returns nodes for the resulting AST, and `var_eval_expr()` that does actual computations for use in the `WAZZUP` block

Todo:
- [x] Lexical Analyzer
- [x] GUI  
**Syntax Analyzer**
- [x] User Input
- [x] User Output
- [x] Variables
- [x] Operations
- [x] Typecasting
- [ ] If-Else
- [ ] Switch-Case
- [ ] Loops
- [ ] Functions  
**Semantic Analyzer**
- [x] User Input
- [x] User Output
- [x] Variables
- [x] Operations
- [x] Typecasting
- [ ] If-Else
- [ ] Switch-Case
- [ ] Loops
- [ ] Functions
