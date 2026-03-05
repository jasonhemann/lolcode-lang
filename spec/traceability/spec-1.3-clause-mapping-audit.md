# Spec 1.3 Clause-to-Matrix Recalculation Audit

Date: 2026-03-05

## Method

- Re-extracted clause index from `spec/upstream/lolcode-spec-v1.3.md` using updated extractor logic in `scripts/extract_spec_clauses.rkt`.
- Clause index now records all non-empty lines outside fenced code (`heading`, `bullet`, `normative`, `prose`) and fenced code lines (`syntax`, `code`).
- Recomputed coverage by matching matrix `source-line` values in `spec/traceability/spec-1.3-matrix.rktd` against extracted clause lines.
- For strict clause gap accounting, used `kind=normative` rows.

## Summary

- Matrix entries: 60
- Unique matrix source lines: 59
- Extracted 1.3 clause rows: 573
- Extracted 1.3 normative rows: 65
- Normative rows mapped by matrix source line: 35
- Normative rows not mapped by matrix source line: 30

## Unmapped 1.3 Normative Clauses (line -> text)

- 50: All of these are valid single line comments:
- 67: These are valid multi-line comments:
- 105: All variable scope, as of this version, is local to the enclosing function or to the main program block. Variables are only accessible after declaration, and there is no global scope.
- 123: This instantiates and initializes a variable. If the value is a literal, the variable is initialized to the appropriate object type (YARN, TROOF, NOOB, NUMBR, NUMBAR). If the value is an identifier or expression, the variable is initialized to the resulting expression.
- 145: Function types are declared/initialized using the HOW DUZ I / IF U SAY SO blocks, however they behave the same as variables. For example:
- 219: The variable types that LOLCODE currently recognizes are: strings (YARN), integers (NUMBR), floats (NUMBAR), and booleans (TROOF) (Arrays (BUKKIT) are reserved for future expansion.) Typing is handled dynamically. Until a variable is given an initial value, it is untyped (NOOB). ~~Casting operations operate on TYPE types, as well.~~
- 241: String literals (YARN) are demarked with double quotation marks ("). Line continuation and soft-command-breaks are ignored inside quoted strings. An unterminated string literal (no closing quote) will cause an error.
- 269: Mathematical operators and functions in general rely on prefix notation. By doing this, it is possible to call and compose operations with a minimum of explicit grouping. When all operators and functions have known arity, no grouping markers are necessary. In cases where operators have variable arity, the operation is closed with `MKAY`. An `MKAY` may be omitted if it coincides with the end of the line/statement, in which case the EOL stands in for as many `MKAYs` as there are open variadic functions.
- 271: Calling unary operators then has the following syntax:
- 283: An expression containing an operator with infinite arity can then be expressed with the following syntax:
- 324: `<x>` and `<y>` in the expression syntaxes above are automatically cast as TROOF values if they are not already so.
- 346: If `<x>` in the above formulations is too verbose or difficult to compute, don't forget the automatically created IT temporary variable. A further idiom could then be:
- 391: To accept input from the user, the keyword is
- 407: A bare expression (e.g. a function call or math operation), without any assignment, is a legal statement in LOLCODE. Aside from any side-effects from the expression when evaluated, the final value is placed in the temporary variable `IT`. `IT`'s value remains in local scope and exists until the next time it is replaced with a bare expression.
- 411: Assignment statements have no side effects with `IT`. They are generally of the form:
- 433: `O RLY?` branches to the block begun with `YA RLY` if `IT` can be cast to WIN, and branches to the `NO WAI` block if `IT` is FAIL. The code block introduced with `YA RLY` is implicitly closed when `NO WAI` is reached. The `NO WAI` block is closed with `OIC`. The general form is then as follows:
- 582: Currently, the number of arguments in a function can only be defined as a fixed number. The `<argument>`s are single-word identifiers that act as variables within the scope of the function's code. The calling parameters' values are then the initial values for the variables within the function's code block when the function is called.
- 588: Return from the function is accomplished in one of the following ways:
- 596: A function of given arity is called with:
- 604: The I parameter is used to distingish a function call on the current namespace vs. a function call on a bukkit (defined below).
- 612: BUKKITs are the container type. They may hold NUMBRs, NUMBARs, TROOFs, YARNs, functions (FUNKSHUN), and other BUKKITS. Each entity within a BUKKIT may be indexed by a NUMBR or a YARN. These indices, whether NUMBRs or YARNs, referring to functions, variables, or other BUKKITS, are generically called “slots”.
- 616: To create an empty object within the current object's scope:
- 678: BTW bar is on function namespace
- 680: BTW bar2 is on the function namespace
- 741: Slot access is very important to function calls. To call a function on an object:
- 770: `izmakin` refers to a method that will be run after a bukkit is fully prototyped but before the prototyping method returns. This allows a bukkit creator to perform some logic every time that bukkit is prototyped, and guarantees a “well-formed” bukkit.
- 774: To create an object based upon an existing object:
- 782: To define inheritance using alternate syntax, do the following.
- 804: No matter where a FUNKSHUN is stored in a slot, during a Slot-Access Function call, the Function obtains variables from the object it was accessed from.
- 810: In this case, the function will pull variables from <object>.

## 1.2 \ 1.3 Normative Delta (text-normalized)

Derived by normalized text set difference over extracted `kind=normative` rows:

- 1.2 line 81: All LOLCODE programs must be opened with the command `HAI`. `HAI` should then be followed with the current LOLCODE language version number (1.2, in this case). There is no current standard behavior for implementations to treat the version number, though.
- 1.2 line 99: Variable identifiers may be in all uppercase or lowercase letters (or a mixture of the two). They must begin with a letter and may be followed only by other letters, numbers, and underscores. No spaces, dashes, or other symbols are allowed. Variable identifiers are CASE SENSITIVE – "cheezburger", "CheezBurger" and "CHEEZBURGER" would all be different variables.

Both 1.2-only normative lines are semantically represented in the current 1.3 matrix via:

- Program envelope/version handling (`program.envelope-hai-kthxbye`, `program.version-handling`)
- Identifier naming constraints (`var.identifier-shape`)

## Notes

- The 30 unmapped 1.3 normative lines include a mixture of:
  - real semantic clauses not yet modeled as distinct traceability rows,
  - syntax-introduction prose that overlaps existing rows,
  - and example/illustrative lines currently tagged `normative` by heuristic extraction.
- This audit is intended to drive matrix refinement; it is stricter and broader than the previous clause-index extraction.
