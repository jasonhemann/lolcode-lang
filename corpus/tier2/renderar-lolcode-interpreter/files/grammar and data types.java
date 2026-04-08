/* List of DataTypes 

		Source Code Delimiter
		Visible Keyword
		Gimmeh Keyword
		Increment
		Decrement
		Hard Typecast
		Variable Expression
		Variable Initialization
		Variable Assignment
		Boolean Unary
		Boolean End
		Different
		Operation Separator
		String Concatenate
		Switch Start
		Condition End
		If-else Keyword
		Case Keyword
		Default Keyword
		Break Keyword
		Integer Literal
		Float Literal
		String Literal
		Boolean Liteal
		Variable Identifier
		Newline
	*/

	/*
		<codeChecker> ::= <Source Code Delimiter>
		<Source Code Delimiter> ::= <Visible Keyword> | <Gimmeh Keyword> | <Declaration> | <Newline>
		<Newline> ::= <Visible Keyword> | <Gimmeh Keyword> | <Declaration> | <Newline>
		<Visible Keyword> ::= <ends with Literal> | <Variable Identifier> |  <Newline>
		<Variable Identifier1> ::= <an> <Variable Identifier> | <Variable Identifier>
		<Declaration> ::= <Variable Identifier2>
		<Variable Identifier2> ::= <Variable Initialization> | <Newline>
		<Variable Initialization> ::= <ends with Literal>
		<ends with Literal> ::= <Newline>
	*/