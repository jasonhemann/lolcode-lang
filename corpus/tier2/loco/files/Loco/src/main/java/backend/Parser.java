package backend;

import java.io.File;
import java.util.ArrayList;

import SyntaxNodes.*;

public class Parser {
	private ArrayList<Token> tokens;
	private ArrayList<Token> allTokens;
	private ArrayList<String> diagnostics;
	private int position;
	private int lineCounter;
	
	private boolean inInfarop;
	private boolean inSmoosh;
	private boolean inPrint;
	private boolean inFlowControl;
	private boolean inFunction;
	
	public Parser (File file) {
		this.tokens = new ArrayList<Token>();
		this.allTokens = new ArrayList<Token>();
		this.diagnostics = new ArrayList<String>();
		this.position = 0;
		this.lineCounter = 1;
		
		this.inInfarop = false;
		this.inSmoosh = false;
		this.inPrint = false;
		this.inFlowControl = false;
		this.inFunction = false;
		
		Lexer lexer = new Lexer(file);
		Token curToken;
		
		//	Get all the tokens from the lexer
		do {
			curToken = lexer.nextToken();
			
			// ignore single line comment
			if (curToken.getTokenKind() == TokenKind.btwToken) {
				while (curToken.getTokenKind() != TokenKind.eolToken && curToken.getTokenKind() != TokenKind.eofToken) {
					allTokens.add(curToken);
					curToken = lexer.nextToken();
				}
			}
			
			if (curToken.getTokenKind() != TokenKind.badToken) {
				allTokens.add(curToken);
				tokens.add(curToken);
			}
			
		} while (curToken.getTokenKind() != TokenKind.eofToken);
	}
	
	public Parser (String strFile) {
		this.tokens = new ArrayList<Token>();
		this.allTokens = new ArrayList<Token>();
		this.diagnostics = new ArrayList<String>();
		this.position = 0;
		this.lineCounter = 1;
		
		this.inInfarop = false;
		this.inSmoosh = false;
		this.inPrint = false;
		this.inFlowControl = false;
		this.inFunction = false;
		
		Lexer lexer = new Lexer(strFile);
		Token curToken;
		
		do {
			curToken = lexer.nextToken();
			
			if (curToken.getTokenKind() == TokenKind.btwToken) {
				while (curToken.getTokenKind() != TokenKind.eolToken && curToken.getTokenKind() != TokenKind.eofToken) {
					allTokens.add(curToken);
					curToken = lexer.nextToken();
				}
			}
			
			if (curToken.getTokenKind() != TokenKind.badToken) {
				allTokens.add(curToken);
				tokens.add(curToken);
			}
			
		} while (curToken.getTokenKind() != TokenKind.eofToken);
	}
	
	private Token peek(int offset) {
		//	check if peek value is within the bounds
		if (position + offset >= tokens.size()) return tokens.get(tokens.size() - 1);
		else if (tokens.get(position + offset).getTokenKind() == TokenKind.dotsToken) {
			if (offset == 0) position += 2;
			else offset += 2;
		}
		
		return tokens.get(position + offset);
	}
	
	private Token current() {
		return peek(0);
	}
	
	private Token nextToken() {
		Token curToken = current();
		position++;
		return curToken;
	}
	
	//	Optionally matches the given parameter; if no match, no error is thrown
	private Token lazyMatch(TokenKind kind) {
		if (current().getTokenKind() == TokenKind.commaToken && kind == TokenKind.eolToken) {
			nextToken();
			return new Token(kind, "\n", -1);
			
		} else if (current().getTokenKind() == kind && kind == TokenKind.eolToken) {
			lineCounter++;

			return consumeEOL();
			
		} else if (current().getTokenKind() == kind) {

			return nextToken();
		}
		
		return new Token(kind, null, current().getPosition() - 1);
	}
	
	//	Check if current token matches the given parameter; if no match, an error is thrown
	private Token match(TokenKind kind) {		
		if (current().getTokenKind() == TokenKind.commaToken && kind == TokenKind.eolToken) {
			nextToken();
			return new Token(kind, "\n", -1);
			
		} else if (current().getTokenKind() == kind && kind == TokenKind.eolToken) {
			lineCounter++;

			//	Console multiple eol tokens
			return consumeEOL();
			
		} else if (current().getTokenKind() == kind) {
			
			return nextToken();
			
		} 
		
		diagnostics.add("Line "+ lineCounter + ": Type Error; Unexpected <"+ current().getTokenKind() 
				+ "> expected <"+ kind + ">");
			
		if (current().getTokenKind() != TokenKind.eofToken &&
			(current().getTokenKind() == TokenKind.miscToken ||
			current().getTokenKind() == TokenKind.badToken ||
			kind == TokenKind.eolToken) ) {
			nextToken();
		}
		
		//	create a fake token for the parse tree
		return new Token(kind, null, current().getPosition() - 1);
	}


	public NodeRoot parse() {
		NodeRoot root;
		
		//	optionally matches any eol before the HAI keyword
		lazyMatch(TokenKind.eolToken);
		omitPreamble();
		Token start = match(TokenKind.haiToken);
		
		//	matches with version number incase any is provided
		lazyMatch(TokenKind.numbarToken);
		
		match(TokenKind.eolToken);
		
		//	check if file has atleast 1 line of code between hai and kthxbye
		if (current().getTokenKind() != TokenKind.byeToken && current().getTokenKind() != TokenKind.eofToken) {
			SyntaxNode statement = parseStatement();
			Token end = match(TokenKind.byeToken);
			
			root = new NodeRoot (start, statement, end);
		} else {
			Token end = match(TokenKind.byeToken);
			root = new NodeRoot (start, end);
		}
		
		lazyMatch(TokenKind.eolToken);
		omitPreamble();
		match(TokenKind.eofToken);
		
		return root;
	}
	
	private SyntaxNode parseStatement() {
		SyntaxNode expression;
		
		if (isAssignment()) expression = parseAssignment();
		else if (isFlowControl()) expression = parseFlowControl();
		else expression = parseExpression();
		
		match(TokenKind.eolToken);
		
		inFlowControl = false;
		
		//	recursively create statement nodes for the parse tree
		while (current().getTokenKind() != TokenKind.byeToken && 
			   current().getTokenKind() != TokenKind.eofToken &&
			   current().getTokenKind() != TokenKind.loopEndToken &&
			   current().getTokenKind() != TokenKind.functionEndToken &&
			   current().getTokenKind().getType() != "switch" &&
			   current().getTokenKind().getType() != "ifblock") {
			expression = new NodeStatement(expression, parseStatement());
		}
		
		return expression;
	}

	
	
	private SyntaxNode parseExpression() {
		
		if (current().getTokenKind() == TokenKind.obtwToken) {
			return new NodeExpression(parseComment(), lineCounter);
			
		} else if (current().getTokenKind().getType() == "mathop") {
			return new NodeExpression(parseMathOp(), lineCounter);
			
		} else if (current().getTokenKind().getType() == "boolop") {
			return new NodeExpression(parseBoolOp(), lineCounter);
			
		} else if (current().getTokenKind().getType() == "infarop") {
			inInfarop = true;
			SyntaxNode infAr = new NodeExpression(parseInfArOp(nextToken()), lineCounter);
			inInfarop = false;
			
			match(TokenKind.mkayToken);
			return infAr;
			
		} else if (current().getTokenKind().getType() == "cmpop") {
			return new NodeExpression(parseCmpOp(), lineCounter);
			
		}	else if (current().getTokenKind() == TokenKind.maekToken) {
			return new NodeExpression(parseExpTypecast(), lineCounter);
				
		} else if (current().getTokenKind() == TokenKind.smooshToken) {
			inSmoosh = true;
			SyntaxNode concat = new NodeExpression(parseConcat(nextToken()), lineCounter);
			inSmoosh = false;
			
			lazyMatch(TokenKind.mkayToken);
			return concat;
			
		} else if (current().getTokenKind() == TokenKind.printToken) {
			inPrint = true;
			SyntaxNode print = new NodeExpression(parsePrint(nextToken()), lineCounter);
			inPrint = false;
			
			return print;
			
		} else if (current().getTokenKind() == TokenKind.breakToken) {
			return new NodeLiteral(SyntaxType.gtfo, nextToken());
			
		} else if (current().getTokenKind() == TokenKind.functionRetToken && inFunction) {
			return new NodeExpression(parseFunctionRet(), lineCounter);
			
		} else if (current().getTokenKind() == TokenKind.functionCallToken) {
			return new NodeExpression(parseFunctionCall(), lineCounter);
			
		}
		
		diagnostics.add("Line "+ lineCounter + ": Syntax Error; Invalid Keyword ");
		while (!isEOL()) {
			nextToken();
		}
		return new NodeLiteral(new Token(TokenKind.badToken, null, -1));
	}
	
	private SyntaxNode parseAssignment() {
		if (current().getTokenKind() == TokenKind.ihasToken) {
			return new NodeAssignment(parseDeclaration(), lineCounter);
			
		// if a line starts with a varid, it can fall in either R (assignment) or IS NOW A (typecast)
		} else if (current().getTokenKind() == TokenKind.idToken) {
			Token varid = nextToken();
			
			if (current().getTokenKind() == TokenKind.rToken) {
				return new NodeAssignment(parseVarChange(varid), lineCounter);
						
			} else if (current().getTokenKind() == TokenKind.isNowToken) {
				return new NodeAssignment(parseAsnTypecast(varid), lineCounter);
			}
		} else if (current().getTokenKind() == TokenKind.scanToken) {
			return new NodeAssignment(parseScan(), lineCounter);
		}
		
		diagnostics.add("Line "+ lineCounter + ": Syntax Error; Invalid Keyword");
		while (!isEOL()) {
			nextToken();
		}
		return new NodeLiteral(new Token(TokenKind.badToken, null, -1));
	}
	
	private SyntaxNode parseFlowControl() {
		int currentLineNum = lineCounter;
		inFlowControl = true;
		
		if (current().getTokenKind() == TokenKind.ifStartToken) {
			return new NodeFlowControl(parseIfBlock(), currentLineNum);
			
		} else if (current().getTokenKind() == TokenKind.switchToken) {
			return new NodeFlowControl(parseSwitchCase(), currentLineNum);
			
		} else if (current().getTokenKind() == TokenKind.loopStartToken) {
			return new NodeFlowControl(parseLoop(), currentLineNum);
			
		} else if (current().getTokenKind() == TokenKind.functionStartToken) {
			inFunction = true;
			return new NodeFlowControl(parseFunction(), currentLineNum);
			
		}
		
		diagnostics.add("Line "+ lineCounter + ": Syntax Error; Invalid Keyword");
		while (!isEOL()) {
			nextToken();
		}
		return new NodeLiteral(new Token(TokenKind.badToken, null, -1));
	}
	
	private SyntaxNode parseComment() {
		ArrayList<Token> inner = new ArrayList<Token>();
		Token start = nextToken();
		int counter = 0;
		
		while (current().getTokenKind() != TokenKind.tldrToken && current().getTokenKind() != TokenKind.byeToken) {
			if (current().getValue() == "\n") {
				counter++;
				lineCounter++;
			}
			inner.add(nextToken());
		}
		Token end = match(TokenKind.tldrToken);
		
		//	multiline comments need atleast 2 newlines to be considered valid
		if (counter < 2) diagnostics.add("Line "+ lineCounter + ": Syntax Error; Invalid comment structure");
		
		return new NodeComment(start, inner, end);
	}
	
	/*
	 ========================
	 
	 	EXPRESSION
	 
	 ========================
	*/
	
	private SyntaxNode parseMathOp() {
		Token operation = nextToken();
		
		SyntaxNode operand1 = parseTerminal();
		match(TokenKind.anToken);
		SyntaxNode operand2 = parseTerminal();
		
		return new NodeOperation(SyntaxType.mathop, operation, operand1, operand2);
		
	}
	
	private SyntaxNode parseBoolOp() {
		Token operation = nextToken();
		
		if (operation.getTokenKind() != TokenKind.notOpToken) {
			SyntaxNode operand1 = parseTerminal();
			match(TokenKind.anToken);
			SyntaxNode operand2 = parseTerminal();
			
			return new NodeOperation(SyntaxType.boolop, operation, operand1, operand2);
		} else {
			SyntaxNode operand1 = parseTerminal();
			
			return new NodeOperation(SyntaxType.boolop, operation, operand1);
		}
	}
	
	private SyntaxNode parseInfArOp(Token operation) {		
		SyntaxNode operand1 = parseTerminal();
		
		//	Recursive construction of parsetree for infinite arity operations
		if (!isEOL() && current().getTokenKind() != TokenKind.mkayToken) {
			match(TokenKind.anToken);
			operand1 = new NodeOperation(SyntaxType.infarop , operation, operand1, parseInfArOp(operation));
		} else {
			operand1 = new NodeOperation(SyntaxType.infarop, operation, operand1);
		}
		
		return operand1;
	}
	
	private SyntaxNode parseCmpOp() {
		Token operation = nextToken();
		
		SyntaxNode operand1 = parseTerminal();
		match(TokenKind.anToken);
		SyntaxNode operand2 = parseTerminal();
		
		return new NodeOperation(SyntaxType.cmpop, operation, operand1, operand2);
	}
	
	private SyntaxNode parseConcat(Token operation) {
		SyntaxNode operand1 = parseTerminal();
		
		//	Recursive construction of parsetree for concatenation operation
		if (!isEOL() && current().getTokenKind() != TokenKind.mkayToken) {
			match(TokenKind.anToken);
			operand1 = new NodeOperation(SyntaxType.concat, operation, operand1, parseConcat(operation));
		} else {
			operand1 = new NodeOperation(SyntaxType.concat, operation, operand1);
		}
		
		return operand1;
	}
	
	private SyntaxNode parsePrint(Token operation) {
		SyntaxNode operand1 = parseTerminal();
		
		//	Recursive construction of parsetree for print operation
		if (!isEOL() && current().getTokenKind() != TokenKind.exclamationToken) {
			operand1 = new NodeOperation(SyntaxType.print, operation, operand1, parsePrint(operation));
		
		} else if (current().getTokenKind() == TokenKind.exclamationToken) {
			operand1 = new NodeOperation(SyntaxType.print, operation, operand1, new NodeOperation(SyntaxType.print, operation, new NodeLiteral(nextToken())));
			
		} else {
			operand1 = new NodeOperation(SyntaxType.print, operation, operand1);
		}
		
		
		return operand1;
	}
	
	private SyntaxNode parseExpTypecast() {
		Token operation = nextToken();
		
		//	Prevent IT from being used as a varid
		if (current().getTokenKind() == TokenKind.idToken) {
			Token varid = nextToken();
			
			lazyMatch(TokenKind.aToken);
			
			SyntaxNode vartype = new NodeLiteral(SyntaxType.vartype, match(TokenKind.typeToken));
			
			return new NodeDeclaration(SyntaxType.vartypechange, operation, varid, vartype);
		}
		
		//	typecast the result of an expression
		SyntaxNode expression = parseTerminal();
		lazyMatch(TokenKind.aToken);
		SyntaxNode vartype = new NodeLiteral(SyntaxType.vartype, match(TokenKind.typeToken));
		
		return new NodeOperation(SyntaxType.vartypechange, operation, expression, vartype);
	}
	
	private SyntaxNode parseFunctionRet() {
		Token operation = nextToken();
		SyntaxNode operand1 = parseTerminal();
		
		return new NodeOperation(SyntaxType.functionret, operation, operand1);
	}
	
	private SyntaxNode parseFunctionCall() {
		ArrayList<SyntaxNode> parameters = new ArrayList<SyntaxNode>();
		Token operation = nextToken();
		Token functionid = match(TokenKind.idToken);
		
		
		//	check if function call includes parameters
		if (current().getTokenKind() == TokenKind.yrToken) {
			nextToken();
			parameters.add(parseTerminal());
			
			//	add to arraylist all the parameters
			while(current().getTokenKind() == TokenKind.anToken) {
				nextToken();
				match(TokenKind.yrToken);
				parameters.add(parseTerminal());
			}
		}
		
		match(TokenKind.mkayToken);
		
		return new NodeFunctionCall(operation, functionid, parameters);
	}
	
	
	/*
	 ========================
	 
	 	ASSIGNMENT
	 
	 ========================
	*/
	
	private SyntaxNode parseDeclaration() {
		Token operation = nextToken();
		Token varid = match(TokenKind.idToken);
		
		//	prevents variable declaration inside flowcontrol statements
		if (inFlowControl) {
			diagnostics.add("Line "+ lineCounter + ": Syntax Error; Invalid variable instantiation");
		}
		
		
		//	assign an expression if there is an ITZ keyword
		if (current().getTokenKind() == TokenKind.itzToken) {
			nextToken();
			
			return new NodeDeclaration(SyntaxType.newvar, operation, varid, parseTerminal());			
		}
		
		return new NodeDeclaration(SyntaxType.newvar, operation, varid);

	}

	private SyntaxNode parseVarChange(Token varid) {
		Token operation = nextToken();
		
		SyntaxNode terminal = parseTerminal();
		
		return new NodeDeclaration(SyntaxType.varchange, operation, varid, terminal);
	}
	
	private SyntaxNode parseAsnTypecast(Token varid) {
		Token operation = nextToken();
		SyntaxNode vartype = new NodeLiteral(SyntaxType.vartype, match(TokenKind.typeToken));
		
		return new NodeDeclaration(SyntaxType.vartypechange, operation, varid, vartype);
	}
	
	private SyntaxNode parseScan() {
		Token operation = nextToken();
		Token varid = match(TokenKind.idToken);
		
		return new NodeDeclaration(SyntaxType.scan, operation, varid);
	}
	
	/*
	 ========================
	 
	 	FLOW CONTROL
	 
	 ========================
	*/
	
	private SyntaxNode parseIfBlock() {
		ArrayList<SyntaxNode> statements = new ArrayList<SyntaxNode>();
		ArrayList<SyntaxNode> ifConditions = new ArrayList<SyntaxNode>();
		Token operation = nextToken();
		
		match(TokenKind.eolToken);
		match(TokenKind.ifBlockToken);
		match(TokenKind.eolToken);
		
		statements.add(parseStatement());
		
		//	add any number of MEBBE blocks
		while (current().getTokenKind() == TokenKind.elifBlockToken) {
			match(TokenKind.elifBlockToken);
			ifConditions.add(parseTerminal());
			match(TokenKind.eolToken);
			statements.add(parseStatement());
		}

		//	optional else block
		if (current().getTokenKind() == TokenKind.elseBlockToken) {
			
			ifConditions.add(new NodeLiteral(nextToken()));
			match(TokenKind.eolToken);
			
			statements.add(parseStatement());
		}
		
		
		match(TokenKind.ifEndToken);
		
		return new NodeMultiLine(SyntaxType.ifblock, operation, ifConditions, statements);
	}
	
	private SyntaxNode parseSwitchCase() {
		ArrayList<SyntaxNode> statements = new ArrayList<SyntaxNode>();
		ArrayList<SyntaxNode> switchLiterals = new ArrayList<SyntaxNode>();
		Token operation = nextToken();
		match(TokenKind.eolToken);
		
		//	get all literals used as considitions for switch case
		do {
			
			match(TokenKind.caseToken);
			switchLiterals.add(parseLiteral());
			match(TokenKind.eolToken);
			
			statements.add(parseStatement());
			
		} while (current().getTokenKind() != TokenKind.ifEndToken && current().getTokenKind() != TokenKind.defaultToken);
		
		//	optional default case
		if (current().getTokenKind() == TokenKind.defaultToken) {
			switchLiterals.add(new NodeLiteral(nextToken()));
			match(TokenKind.eolToken);
			
			statements.add(parseStatement());
		}
		
		match(TokenKind.ifEndToken);
		
		return new NodeMultiLine(SyntaxType.switchcase, operation, switchLiterals, statements);
	}
	
	private SyntaxNode parseLoop() {
		ArrayList<SyntaxNode> statements = new ArrayList<SyntaxNode>();
		Token operation = nextToken();
		Token loopid = match(TokenKind.idToken);
		Token optype;
		SyntaxNode condition;
		
		if (loopid.getValue() != null && loopid.getValue().equals("IT")) {
			diagnostics.add("Line "+ lineCounter + ": Type Error; expected valid Literal/VarId/Expression");
		}
		
		if (current().getTokenKind() == TokenKind.incToken || current().getTokenKind() == TokenKind.decToken) {
			optype = nextToken();
		} else {
			diagnostics.add("Line "+ lineCounter + ": Type Error; Unexpected <"+ current().getTokenKind() 
					+ "> expected <incToken>/<decToken>");
			optype = new Token(TokenKind.incToken, "UPPIN", -1);
		}
		
		match(TokenKind.yrToken);
		Token varid = match(TokenKind.idToken);
		
		//	check if loop has a condition
		if (current().getTokenKind() == TokenKind.tilToken || current().getTokenKind() == TokenKind.wileToken) {
			if (peek(1).getTokenKind().getType() != "cmpop") {
				diagnostics.add("Line "+ lineCounter + ": Type Error; Unexpected <"+ peek(1).getTokenKind().getType() 
						+ "> expected comparison operator <cmpop>");
			}
			condition = new NodeDeclaration(SyntaxType.loopcond, nextToken(), varid, parseCmpOp());
		} else {
			Token tempToken = new Token(TokenKind.troofToken, "WIN", -1);
			condition = new NodeDeclaration(SyntaxType.loopcond, tempToken, varid);
		}
		
		match(TokenKind.eolToken);
		
		statements.add(parseStatement());
		
		match(TokenKind.loopEndToken);
		
		if (!loopid.getValue().equals(current().getValue())) {
			diagnostics.add("Line "+ lineCounter + ": ID Error; Loop id mismatch");
			
		} 
		
		nextToken();
		
		return new NodeMultiLine(operation, loopid, optype, condition, statements);
	}
	
	private SyntaxNode parseFunction() {
		ArrayList<SyntaxNode> statements = new ArrayList<SyntaxNode>();
		ArrayList<SyntaxNode> parameters = new ArrayList<SyntaxNode>();
		nextToken();
		Token functionid = match(TokenKind.idToken);
		
		//	match with function parameters if any
		if (current().getTokenKind() == TokenKind.yrToken) {
			nextToken();
			parameters.add(new NodeLiteral(SyntaxType.varid, match(TokenKind.idToken)));
			
			while(current().getTokenKind() == TokenKind.anToken) {
				nextToken();
				match(TokenKind.yrToken);
				parameters.add(new NodeLiteral(SyntaxType.varid, match(TokenKind.idToken)));
			}
		}
		
		match(TokenKind.eolToken);
		
		statements.add(parseStatement());
		
		match(TokenKind.functionEndToken);
		inFunction = false;
		
		return new NodeMultiLine(SyntaxType.function, functionid, parameters, statements);
	}
	
	
	
	
	//	checker if operand is a valid expression or literal or varid
	private SyntaxNode parseTerminal() {
		
		if (current().getTokenKind().getType() == "mathop") {
			return parseMathOp();
			
		} else if (current().getTokenKind().getType() == "boolop") {
			return parseBoolOp();
			
		} else if (current().getTokenKind().getType() == "cmpop") {
			return parseCmpOp();
			
		//	check if current is a yarn delimiter
		} else if (current().getTokenKind() == TokenKind.quoteToken) {
			return new NodeLiteral(parseYarn());
			
		} else if (current().getTokenKind().getType() == "literal") {
			return new NodeLiteral(nextToken());
			
		} else if (current().getTokenKind() == TokenKind.idToken) {
			return new NodeLiteral(SyntaxType.varid, nextToken());
			
		} else if (current().getTokenKind() == TokenKind.maekToken) {
			return parseExpTypecast();
			
		} else if (current().getTokenKind() == TokenKind.functionCallToken) {
			return parseFunctionCall();
		
		//	stop infarop and concat from nesting
		} else if (current().getTokenKind().getType() == "infarop" && !inInfarop) {
			inInfarop = true;
			SyntaxNode infAr = parseInfArOp(nextToken());
			inInfarop = false;
		
			match(TokenKind.mkayToken);
			return infAr;
		} else if (current().getTokenKind() == TokenKind.smooshToken && !inSmoosh) {
			inSmoosh = true;
			SyntaxNode concat = parseConcat(nextToken());
			inSmoosh = false;
			
			lazyMatch(TokenKind.mkayToken);
			return concat;
			
		}
		
		if (inInfarop || inSmoosh || inPrint) nextToken();
		diagnostics.add("Line "+ lineCounter + ": Type Error; expected valid Literal/VarId/Expression");
		return new NodeLiteral(SyntaxType.invalid, new Token(TokenKind.badToken, null, -1));
	}
	
	//	Makes sure the operand is a literal
	private NodeLiteral parseLiteral() {
		if (current().getTokenKind() == TokenKind.quoteToken) {
			return new NodeLiteral(parseYarn());
		} else if (current().getTokenKind().getType() == "literal") {
			return new NodeLiteral(nextToken());
		}
		
		diagnostics.add("Line "+ lineCounter + ": Type Error; expected valid NUMBR/NUMBAR/YARN/TROOF");
		return new NodeLiteral(SyntaxType.invalid, new Token(TokenKind.badToken, null, -1));
	}
	
	//	 creates a new yarnToken
	private Token parseYarn() {
		String value = new String();
		nextToken();
		
		//	uses string concatenation to add succeeding tokens until it encounters another quote token
		while (current().getTokenKind() != TokenKind.eolToken && 
			   current().getTokenKind() != TokenKind.eofToken &&
			   current().getTokenKind() != TokenKind.quoteToken) {
			
			if (current().getValue().equals(":")) nextToken();
			else if (current().getValue().equals(":\"")) {
				value += "\"";
				nextToken();
				
			} 
			else value += nextToken().getValue();
		}
		
		match(TokenKind.quoteToken);

		return new Token(TokenKind.yarnToken, value, current().getPosition());
	}
	
	
	//	skips newline tokens until it encounters a different token
	private Token consumeEOL() {
		Token token = nextToken();
		
		while (current().getTokenKind() == TokenKind.eolToken) {
			lineCounter++;
			token = nextToken();
		}
		
		return token;
	}

	//	skips all tokens until unless its haitoken, eoftoken or a multiline token
	private void omitPreamble() {
		boolean insideComment = false;
		
		while (current().getTokenKind() != TokenKind.haiToken && current().getTokenKind() != TokenKind.eofToken) {			
			
			if (current().getTokenKind() != TokenKind.obtwToken &&
				current().getTokenKind() != TokenKind.tldrToken &&
				current().getTokenKind() != TokenKind.eolToken &&
				!insideComment) {
				diagnostics.add("Line "+ lineCounter + ": Syntax Error; Unexpected <"+ current().getTokenKind() 
						+ "> before <haiToken>");
			}
			
			if (current().getTokenKind() == TokenKind.obtwToken) insideComment = true;
			else if (current().getTokenKind() == TokenKind.tldrToken) insideComment = false;
			else if (current().getTokenKind() == TokenKind.eolToken) lineCounter++;
			
			nextToken();
		}	
	}
	
	private boolean isAssignment() {
		if (current().getTokenKind() == TokenKind.ihasToken ||
			current().getTokenKind() == TokenKind.idToken ||
			current().getTokenKind() == TokenKind.scanToken) {
			return true;
		}
		
		return false;
	}
	
	private boolean isFlowControl() {
		if (current().getTokenKind() == TokenKind.ifStartToken ||
			current().getTokenKind() == TokenKind.switchToken ||
			current().getTokenKind() == TokenKind.loopStartToken ||
			current().getTokenKind() == TokenKind.functionStartToken) {
			return true;
		}
		
		return false;
	}
	
	private boolean isEOL() {
		if (current().getTokenKind() == TokenKind.eolToken ||
			current().getTokenKind() == TokenKind.commaToken ||
			current().getTokenKind() == TokenKind.eofToken) {
			return true;
		}
		
		return false;
	}
	
	protected ArrayList<Token> getTokens() {
		return allTokens;
	}
	
	protected ArrayList<Token> getParserTokens() {
		return tokens;
	}
	
	protected ArrayList<String> getDiagnostics() {
		return diagnostics;
	}
	
	public void viewTokens() {
		for (Token i : tokens) i.viewToken();
	}
	
	public void viewErrors() {
		for (String i : diagnostics) System.out.println(i);
	}
}
