# NAIVE LOLCODE Specification 1.0.0

FIRST DRAFT &mdash; 3 January 2019

*It is a modified version of the original specification which matches the capabilities of the  presented parser. *

---

## Formatting

### Whitespace

* Indentation, line breaks and spaces are irrelevant.



### File Creation


All LOLCODE programs must be opened with the command `HAI`.  

A LOLCODE file is closed by the keyword `KTHXBYE` which closes the `HAI` code-block.

---

## Variables

### Scope

There is just one global scope.

### Naming

*(from 1.1)*

Variable identifiers may be in all small or lowercase letters (or a mixture of the two). They must begin with a letter and may be followed only by other letters, numbers, and underscores. No spaces, dashes, or other symbols are allowed. Variable identifiers are CASE SENSITIVE – "cheezburger", "CheezBurger" and "CHEEZBURGER" would all be different variables.

### Declaration and Assignment


To declare a variable, the keyword is `I HAVE A` followed by the variable name. To assign the variable a value within the same statement, you can then follow the variable name with `ITZ <value>`.

Assignment of a variable is accomplished with an assignment statement, `<variable> R <expression>`

```
I HAVE A VAR            BTW VAR is null and untyped
VAR R "THREE"          BTW VAR is now a YARN and equals "THREE"
VAR R 3                BTW VAR is now a NUMBR and equals 3
I HAVE A VAR ITZ 3			 BTW it is a redeclaration error.
```

---

## Types


The variable types that LOLCODE currently recognizes are: strings (YARN), integers (NUMBR), floats (NUMBAR), and booleans (TROOF) (Arrays (BUKKIT) are reserved for future expansion.) Typing is handled dynamically. Until a variable is given an initial value, it is untyped (NOOB).


### Booleans

The two boolean (TROOF) values are WIN (true) and FAIL (false). 

### Numerical Types

A NUMBR is an integer as specified in the host implementation/architecture. Any contiguous sequence of digits outside of a quoted YARN and not containing a decimal point (.) is considered a NUMBR. A NUMBR may have a leading hyphen (-) to signify a negative number.

A NUMBAR is a float as specified in the host implementation/architecture. It is represented as a contiguous string of digits containing exactly one decimal point. Casting a NUMBAR to a NUMBR truncates the decimal portion of the floating point number.  NUMBAR may have a leading hyphen (-) to signify a negative number.


### Strings

String literals (YARN) are demarked with double quotation marks ("). Line continuation and soft-command-breaks are ignored inside quoted strings. An unterminated string literal (no closing quote) will cause an error.

Within a string, all characters represent their literal value .


---

## Operators

### Calling Syntax and Precedence



Calling unary operators then has the following syntax:

```
<operator> <expression1>
```

The `AN` keyword shall be used to separate arguments, so a binary operator expression has the following syntax:

```
<operator> <expression1> AN <expression2>
```


### Math

The basic math operators are binary prefix operators.

```
SUM OF <x> AN <y>       BTW +
DIFF OF <x> AN <y>      BTW -
PRODUKT OF <x> AN <y>   BTW *
QUOSHUNT OF <x> AN <y>  BTW /
MOD OF <x> AN <y>       BTW modulo
BIGGR OF <x> AN <y>     BTW max
SMALLR OF <x> AN <y>    BTW min
```

`<x>` and `<y>` may each be expressions in the above, so mathematical operators can be nested and grouped indefinitely.

Math is performed as integer math in the presence of two NUMBRs, but if either of the expressions are NUMBARs, then floating point math takes over.

If one or both arguments are a YARN, they can only be added to each other (concatenation)

### Boolean

Boolean operators working on TROOFs are as follows:

```
BOTH OF <x> [AN] <y>          BTW and: WIN iff x=WIN, y=WIN
EITHER OF <x> [AN] <y>        BTW or: FAIL iff x=FAIL, y=FAIL
WON OF <x> [AN] <y>           BTW xor: FAIL if x=y
NOT <x>                       BTW unary negation: WIN if x=FAIL
```



### Concatenation

String can be concatenated using SUM OF str1 AN str2.


## Output

### Terminal-Based

The print (to STDOUT or the terminal) operator is `VISIBLE`.
```
VISIBLE <expression> 
```

There is currently no defined standard for printing to a file.

To accept input from the user, the keyword is



## Statements

### Assignment Statements

Assignment statements have no side effects with `IT`. They are generally of the form:

```
<variable> <assignment operator> <expression>
```

The variable being assigned may be used in the expression.

### Flow Control Statements

Flow control statements cover multiple lines and are described in the following section.

---

## Flow Control

### Conditionals

#### If-Then

The traditional if/then construct is a very simple construct operating on the implicit `IT` variable. In the base form, there are four keywords: `O RLY?`, `YA RLY`, `NO WAI`, and `OIC`.

`O RLY?` branches to the block begun with `YA RLY` if `IT` can be cast to WIN, and branches to the `NO WAI` block if `IT` is FAIL. The code block introduced with `YA RLY` is implicitly closed when `NO WAI` is reached. The `NO WAI` block is closed with `OIC`. The general form is then as follows:

```
<boolean expression>
O RLY?
  YA RLY
    <code block>
  NO WAI
    <code block>
OIC
```

Sadly, current version of interpreter only supports the syntax of if/else construction. Due to some techical problems the implementaion of if/else logic is delayed. It is to be changed in the future updates.

