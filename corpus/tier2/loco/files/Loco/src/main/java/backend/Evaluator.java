package backend;

import java.io.File;
import java.util.ArrayList;

import SyntaxNodes.*;

import frontend.WindowController;

public class Evaluator {
	private Parser parser;
	private WindowController window;
	
	private ArrayList<Token> tokens;
	private ArrayList<SymTabEntry> symbolTable;
	private ArrayList<NodeMultiLine> functionTable;
	private String errorMsg;
	
	private NodeRoot root;
	private SyntaxNode programCounter;
	private SyntaxNode currentInstruction;
	private boolean switchBreak;
	private int lineCounter;
	private int loopLimit;
	private int position;
	
	public Evaluator(File file) {
		this.errorMsg = new String();
		this.symbolTable = new ArrayList<SymTabEntry>();
		this.functionTable = new ArrayList<NodeMultiLine>();
		this.lineCounter = 1;
		this.loopLimit = 999;
		this.switchBreak = false;
		this.position = 0;
		
		parser = new Parser(file);
		this.root = parser.parse();
		
		this.tokens = parser.getTokens();
		this.symbolTable.add(new SymTabEntry("IT", TokenKind.noobToken, ""));
		
		if (parser.getDiagnostics().size() > 0) {
			programCounter = null;
		} else {
			updateLineCounter();
			
			this.programCounter = root.getStatements();
		}
	}
	
	public Evaluator(String strFile, WindowController window) {
		this.window = window;
		
		this.errorMsg = new String();
		this.symbolTable = new ArrayList<SymTabEntry>();
		this.functionTable = new ArrayList<NodeMultiLine>();
		this.lineCounter = 1;
		this.loopLimit = 999;
		this.switchBreak = false;
		this.position = 0;
		
		parser = new Parser(strFile);
		this.root = parser.parse();
		
		this.tokens = parser.getTokens();
		this.symbolTable.add(new SymTabEntry("IT", TokenKind.noobToken, ""));
		
		if (parser.getDiagnostics().size() > 0) {
			programCounter = null;
		} else {
			updateLineCounter();
			
			this.programCounter = root.getStatements();
		}
		
		
	}
	
	public void nextInstruction() {
		// check if PC holds only 1 line of code 
		if (programCounter.getType() == SyntaxType.expression ||
			programCounter.getType() == SyntaxType.assignment ||
			programCounter.getType() == SyntaxType.flowcontrol) {
			
			currentInstruction = programCounter;
			programCounter = null;
			
		} else {
			//	Type cast from generic SyntaxNode to NodeStatement
			
			NodeStatement ns = (NodeStatement) programCounter;
			
			currentInstruction = ns.getOp1();
			programCounter = ns.getOp2();
		}
		
		
		if (currentInstruction.getType() == SyntaxType.expression) {
			lineCounter = ((NodeExpression) currentInstruction).getLineCounter();
			evalExpression((NodeExpression) currentInstruction);
			
		} else if (currentInstruction.getType() == SyntaxType.assignment) {
			lineCounter = ((NodeAssignment) currentInstruction).getLineCounter();
			evalAssignment((NodeAssignment) currentInstruction);
			
		} else {
			lineCounter = ((NodeFlowControl) currentInstruction).getLineCounter();
			evalFlowControl((NodeFlowControl) currentInstruction);
		}
		
		//updateLineCounter();
		
		//	prevents next lines from executing if Evaluator encounters an error
		if (!errorMsg.isBlank()) programCounter = null;
	}
	
	//	Evaluate a statement node
	private void evaluate(SyntaxNode statements) {
		SyntaxNode currentLine;
		
		if (!errorMsg.isBlank()) {
			programCounter = null;
			return;
		}
		
		while (statements instanceof NodeStatement) {
			currentLine = ((NodeStatement) statements).getOp1();
			statements = ((NodeStatement) statements).getOp2();
			
			//	stop evaluating if break is encountered
			if (currentLine.getType() == SyntaxType.gtfo) {
				switchBreak = true;
				return;
				
			} else if (currentLine.getType() == SyntaxType.expression) {
				evalExpression((NodeExpression) currentLine);
				
			} else if (currentLine.getType() == SyntaxType.assignment) {
				evalAssignment((NodeAssignment) currentLine);
				
			} else {
				evalFlowControl((NodeFlowControl) currentLine);
			}
			
			if (!errorMsg.isBlank()) {
				programCounter = null;
				return;
			}
		}
		
		if (statements.getType() == SyntaxType.gtfo) {
			switchBreak = true;
			return;
		}
	
		if (statements.getType() == SyntaxType.expression) {
			evalExpression((NodeExpression) statements);
			
		} else if (statements.getType() == SyntaxType.assignment) {
			evalAssignment((NodeAssignment) statements);
			
		} else {
			evalFlowControl((NodeFlowControl) statements);
		}
		
		//	stop evaluation if there is an error
		if (!errorMsg.isBlank()) {
			programCounter = null;
			return;
		}
	}
	
	private void evalExpression(NodeExpression currentInstruction) {
		SyntaxNode node = currentInstruction.getNode();
		Token token = new Token(TokenKind.noobToken, "", -1);
		
		if (node.getType() == SyntaxType.comment) {
			return;
		} else if (node.getType() == SyntaxType.mathop) {
			token = evalMathOp((NodeOperation) node);
		
		} else if (node.getType() == SyntaxType.boolop) {
			token = evalBoolOp((NodeOperation) node);
		
		} else if (node.getType() == SyntaxType.cmpop) {
			token = evalCmpOp((NodeOperation) node);
		
		} else if (node.getType() == SyntaxType.infarop) {
			token = evalInfArOp((NodeOperation) node);
			
		} else if (node.getType() == SyntaxType.vartypechange) {	
			token = evalExpTypecast(node);
		
		} else if (node.getType() == SyntaxType.concat) {
			token = evalConcat((NodeOperation) node);
			
		} else if (node.getType() == SyntaxType.print) {
			token = evalPrint((NodeOperation) node);
			
			//	prints to the GUI the result of the print operation
			if (window != null && errorMsg.isEmpty()) window.updateConsole(token.getValue());
		
		} else if (node.getType() == SyntaxType.functioncall) {
			token = evalFunctionCall((NodeFunctionCall) node);
			
		} else if (node.getType() == SyntaxType.functionret) {
			token = evalFunctionRet((NodeOperation) node);
			
		}
		
		
		//	Assign IT the result of the expression
		symbolTable.get(0).setKindValue(token);
		if (window == null) token.viewToken();
	}
	
	private void evalAssignment(NodeAssignment currentInstruction) {
		SyntaxNode node = currentInstruction.getNode();
		
		if (node.getType() == SyntaxType.newvar) {
			evalNewVar((NodeDeclaration) node);
		
		} else if (node.getType() == SyntaxType.varchange) {
			evalVarChange((NodeDeclaration) node);
		
		} else if (node.getType() == SyntaxType.vartypechange) {
			evalAsnTypecast((NodeDeclaration) node);
			
		} else if (node.getType() == SyntaxType.scan) {
			evalScan((NodeDeclaration) node);
			
		}
	}
	
	private void evalFlowControl(NodeFlowControl currentInstruction) {
		SyntaxNode node = currentInstruction.getNode();
		
		if (node.getType() == SyntaxType.ifblock) {
			evalIfBlock((NodeMultiLine) node);
			
		} else if (node.getType() == SyntaxType.switchcase) {
			evalSwitchCase((NodeMultiLine) node);
			
		} else if (node.getType() == SyntaxType.loop) {
			evalLoop((NodeMultiLine) node);
			
		} else if (node.getType() == SyntaxType.function) {
			//	add current node to the function table to be executed if called
			functionTable.add((NodeMultiLine) node);
			
		}
		
		if (window != null) window.updateSymbolTable();
	}
	
	
	
	
	private Token evalMathOp(NodeOperation node) {
		double op1, op2, result;
		boolean isFloat = false;
		
		Token operation = node.getOperation();
		Token operand1 = evalTerminal(node.getOp1());
		Token operand2 = evalTerminal(node.getOp2());
		
		//	check if any operand contains a decimal point 
		if (operand1.getValue().contains(".") || operand2.getValue().contains(".")) isFloat = true;
		
		//	cast operands to double
		op1 = Double.parseDouble(typecastToken(operand1, TokenKind.numbarToken).getValue());
		op2 = Double.parseDouble(typecastToken(operand2, TokenKind.numbarToken).getValue());
		
		
		//	perform float math operation
		if (operation.getTokenKind() == TokenKind.sumOpToken) {
			result = op1 + op2;
		} else if (operation.getTokenKind() == TokenKind.diffOpToken) {
			result = op1 - op2;
		} else if (operation.getTokenKind() == TokenKind.mulOpToken) {
			result = op1 * op2;
		} else if (operation.getTokenKind() == TokenKind.divOpToken) {
			result = op1 / op2;
		} else if (operation.getTokenKind() == TokenKind.maxOpToken) {
			result = Math.max(op1, op2);
		} else if (operation.getTokenKind() == TokenKind.minOpToken) {
			result = Math.min(op1, op2);
		} else {
			result = op1 % op2;
		}
		
		//	Check if result of math operation is valid
		if (Double.isInfinite(result) || Double.isNaN(result)) {
			if (op2 == 0 && errorMsg.isEmpty()) errorMsg = "Line " + lineCounter + ": Math Error; Attempt to divide by zero";
			result = -1;
		}
		
		if (operand1.getTokenKind() == TokenKind.numbarToken || operand2.getTokenKind() == TokenKind.numbarToken || isFloat) {
			return new Token(TokenKind.numbarToken, Double.toString(result), -1);
		}
		
		//	cast to long if both operands are numbr 
		return new Token(TokenKind.numbrToken, Long.toString((long) result), -1);
	}
	
	private Token evalBoolOp(NodeOperation node) {
		boolean op1, op2, result;
		
		op1 = op2 = true;
		
		Token operation = node.getOperation();
		Token operand1 = evalTerminal(node.getOp1());
		
		//	cast operands to boolean datatypes
		operand1 = typecastToken(operand1, TokenKind.troofToken);
		if (operand1.getValue().equals("WIN")) op1 = true;
		else op1 = false;
		
		
		if (operation.getTokenKind() != TokenKind.notOpToken) {
			Token operand2 = evalTerminal(node.getOp2());
			
			operand2 = typecastToken(operand2, TokenKind.troofToken);
			if (operand2.getValue().equals("WIN")) op2 = true;
			else op2 = false;
		}
		
		
		if (operation.getTokenKind() == TokenKind.bothOpToken) {
			result = op1 && op2;
		} else if (operation.getTokenKind() == TokenKind.eitherOpToken) {
			result = op1 || op2;
		} else if (operation.getTokenKind() == TokenKind.wonOpToken) {
			result = (op1 || op2) && (!op1 || !op2);
		} else {
			result = !op1;
		} 
		
		
		if (result) {
			return new Token(TokenKind.troofToken, "WIN", -1);
		}
		
		return new Token(TokenKind.troofToken, "FAIL", -1);
		
	}
	
	private Token evalCmpOp(NodeOperation node) {
		boolean result = false;
		
		Token operation = node.getOperation();
		Token operand1 = evalTerminal(node.getOp1());
		Token operand2 = evalTerminal(node.getOp2());
		
		//	only checks values if both operand has the same datatype
		if (operand1.getTokenKind() == operand2.getTokenKind()) {
			
			if (operation.getTokenKind() == TokenKind.bothSameOpToken) {
				
				if (operand1.getValue().equals(operand2.getValue())) result = true;
				else result = false;
				
			} else {
				
				if (operand1.getValue().equals(operand2.getValue())) result = false;
				else result = true;
			}
			
		}
		
		
		if (result) {
			return new Token(TokenKind.troofToken, "WIN", -1);
		}
		
		return new Token(TokenKind.troofToken, "FAIL", -1);
	}
	
	private Token evalInfArOp(NodeOperation node) {
		boolean result = true;
		Token operation = node.getOperation();
		Token operand1;
		NodeOperation currentNode = node;
		
		if (operation.getTokenKind() == TokenKind.anyOpToken) result = false;
		
		//	iterates through the operands of the node to get the result
		while (true) {
			operand1 = evalTerminal(currentNode.getOp1());
			operand1 = typecastToken(operand1, TokenKind.troofToken);
			
			if (operation.getTokenKind() == TokenKind.anyOpToken) {
				
				if (operand1.getValue().equals("WIN")) result = result || true;
				else result = result || false;
				
				
			} else {
				
				if (operand1.getValue().equals("WIN")) result = result && true;
				else result = result && false;
				
			}			
			
			if (currentNode.getOp2() == null) break;
			else currentNode = (NodeOperation) currentNode.getOp2();
		}
		
		
		if (result) {
			return new Token(TokenKind.troofToken, "WIN", -1);
		}
		
		return new Token(TokenKind.troofToken, "FAIL", -1);
	}
	
	private Token evalExpTypecast(SyntaxNode node) {
		String varid;
		Token varType;
		Token value;
		int symbolTableIdx;
		
		if (node instanceof NodeDeclaration) {
			varid = ((NodeDeclaration) node).getVarID().getValue();
			varType = ((NodeLiteral) ((NodeDeclaration) node).getValue()).getToken();
			symbolTableIdx = findVarValue(varid);
			
			if (symbolTableIdx >= symbolTable.size()) {
				errorMsg = "Line " + lineCounter + ": ID Error; Given variable id is not instantiated ";
				return new Token (TokenKind.badToken, "", -1);
			}
			
			value = symbolTable.get(symbolTableIdx).getToken();
			
		} else {
			value = evalTerminal(((NodeOperation) node).getOp1());
			
			//	make sure value to type cast is a valid literal/expression
			if (value.getTokenKind() == TokenKind.typeToken) {
				errorMsg = "Line " + lineCounter + ": Type Error; Expected valid Literal/Expression";
			}
			
			varType = ((NodeLiteral) ((NodeOperation) node).getOp2()).getToken();
			
		}
		
		//	get a new token according to what the cast is asking
		if (varType.getValue().matches("YARN")) {
			value = typecastToken(value, TokenKind.yarnToken);
		} else if (varType.getValue().matches("NUMBR")) {
			value = typecastToken(value, TokenKind.numbrToken);
		} else if (varType.getValue().matches("NUMBAR")) {
			value = typecastToken(value, TokenKind.numbarToken);
		} else if (varType.getValue().matches("TROOF")) {
			value = typecastToken(value, TokenKind.troofToken);
		} else {
			value = typecastToken(value, TokenKind.noobToken);
		}
		
		return value;
		
	}
	
	private Token evalConcat(NodeOperation node) {
		String str = new String();
		Token operand1;
		NodeOperation currentNode = node;

		//	goes through the node until operand 2 is empty 
		while (true) {
			operand1 = evalTerminal(currentNode.getOp1());
			operand1 = typecastToken(operand1, TokenKind.yarnToken);
			
			str += operand1.getValue();
			
			if (currentNode.getOp2() == null) break;
			else currentNode = (NodeOperation) currentNode.getOp2();
		}
		
		//	replace \n and \t with the proper newline and tab
		str = str.replaceAll("\\\\n", "\n");
		str = str.replaceAll("\\\\t", "\t");
		
		return new Token(TokenKind.yarnToken, str, -1);
	}
	
	private Token evalPrint(NodeOperation node) {
		String str = new String();
		Token operand1;
		NodeOperation currentNode = node;
		boolean suppressNL = false;

		while (true) {
			operand1 = evalTerminal(currentNode.getOp1());
			
			//	cast operand to yarn unless exclamation is spotted
			if (operand1.getTokenKind() != TokenKind.exclamationToken) {
				operand1 = typecastToken(operand1, TokenKind.yarnToken);
				
				str += operand1.getValue();
				
			} else suppressNL = true;
			
			if (currentNode.getOp2() == null) break;
			else currentNode = (NodeOperation) currentNode.getOp2();
		}
		
		//	replace special string escape characters with their intended values
		str = str.replaceAll(":>", "\t");
		str = str.replaceAll(":\\)", "\n");
		str = str.replaceAll(":o", "\\\\g");
		str = str.replaceAll("::", ":");
		
		if (!suppressNL) str += "\n";
		
		return new Token(TokenKind.yarnToken, str, -1);
	}
	
	
	
	
	private Token evalFunctionRet(NodeOperation node) {
		return evalTerminal(node.getOp1());
	}
	
	private Token evalFunctionCall(NodeFunctionCall node) {
		ArrayList<SyntaxNode> parameters = node.getParameters();
		String functionid = node.getFunctionid().getValue();
		NodeMultiLine function;
		SymTabEntry entry;
		Token newVar = new Token(TokenKind.noobToken, "", -1), parameterToken;
		int functionIdx = 0, symbolTableIdx = 0, i;
		
		ArrayList<SymTabEntry> symbolTableBackup = new ArrayList<SymTabEntry>();
		
		//	store a backup of the symboltable before execution of function
		for (i = 0; i < symbolTable.size(); i++) {
			entry = symbolTable.get(i);
			symbolTableBackup.add(new SymTabEntry(entry.getIdentifier(), entry.getKind(), entry.getValue()));
		}
		
		//	check if function called actually exists
		for (NodeMultiLine j : functionTable) {
			if (j.getOperation().getValue().equals(functionid)) {
				break;
			}	
			functionIdx++;
		}
		
		if (functionIdx >= functionTable.size()) {
			errorMsg = "Line " + lineCounter + ": ID Error; " + functionid + " is not defined";
			
		} else if (parameters.size() != functionTable.get(functionIdx).getIfConditions().size()) {
			errorMsg = "Line " + lineCounter + ": Syntax Error; number of parameters does not match function descriptor";

		} else {
			function = functionTable.get(functionIdx);
			
			//	assign the function variables to the given values from the function call
			for (i = 0; i < parameters.size(); i++) {
				newVar = evalTerminal(parameters.get(i));
				parameterToken = (((NodeLiteral) function.getIfConditions().get(i)).getToken());
				
				symbolTableIdx = findVarValue(parameterToken.getValue());
				
				//	add or change the value of the variable in the symboltable
				if (symbolTableIdx >= symbolTable.size()) {
					symbolTable.add(new SymTabEntry(parameterToken.getValue(), newVar.getTokenKind(), newVar.getValue()));
				} else {
					symbolTable.get(symbolTableIdx).setKindValue(newVar);
				}
			}
			
			//	execute instructions inside function
			evaluate(function.getStatements().get(0));
			newVar = symbolTable.get(0).getToken();
			
			//	return noob token if GTFO is encountered
			if (switchBreak) {
				switchBreak = false;
				newVar = new Token(TokenKind.noobToken, "", -1);
			}
			else newVar = symbolTable.get(0).getToken();
		}
		
		//	restore the symboltable to its state before the function call
		symbolTable.clear();
		for (i = 0; i < symbolTableBackup.size(); i++) {
			symbolTable.add(symbolTableBackup.get(i));
		}

		return newVar;
	}
	
	
	
	
	
	
	private void evalNewVar(NodeDeclaration node) {		
		SymTabEntry newVar;
		String varid = node.getVarID().getValue();
		
		if (findVarValue(varid) < symbolTable.size()) {
			errorMsg = "Line " + lineCounter + ": ID Error; Duplicate instantiation of new variable";
			return;
		}

		//	create a new symbol table entry to add to the table
		if (node.getValue() != null) {
			Token value = evalTerminal(node.getValue());
			newVar = new SymTabEntry(varid, value.getTokenKind(), value.getValue());
		} else {
			newVar = new SymTabEntry(varid, TokenKind.noobToken, "");
		}
		
		symbolTable.add(newVar);
	}
	
	private void evalVarChange(NodeDeclaration node) {
		String varid = node.getVarID().getValue();
		Token value = evalTerminal(node.getValue());
		int symbolTableIdx = findVarValue(varid);
		
		if (symbolTableIdx >= symbolTable.size()) {
			errorMsg = "Line " + lineCounter + ": ID Error; Given variable id is not instantiated ";
			return;
		}
		
		//	update variable in the symboltable with the value given
		symbolTable.get(symbolTableIdx).setKindValue(value);
		
	}
	
	private void evalAsnTypecast(NodeDeclaration node) {
		String varid = node.getVarID().getValue();
		Token varType = ((NodeLiteral) node.getValue()).getToken();
		Token value;
		int symbolTableIdx = findVarValue(varid);
		
		if (symbolTableIdx >= symbolTable.size()) {
			errorMsg = "Line " + lineCounter + ": ID Error; Given variable id is not instantiated ";
			return;
		}
		
		value = symbolTable.get(symbolTableIdx).getToken();
		
		//	typecast value to the given type
		if (varType.getValue().matches("YARN")) {
			value = typecastToken(value, TokenKind.yarnToken);
		} else if (varType.getValue().matches("NUMBR")) {
			value = typecastToken(value, TokenKind.numbrToken);
		} else if (varType.getValue().matches("NUMBAR")) {
			value = typecastToken(value, TokenKind.numbarToken);
		} else if (varType.getValue().matches("TROOF")) {
			value = typecastToken(value, TokenKind.troofToken);
		} else {
			value = typecastToken(value, TokenKind.noobToken);
		}
		
		symbolTable.get(symbolTableIdx).setKindValue(value);
	}
	
	private void evalScan(NodeDeclaration node) {
		Token token;
		String value;
		String varid = node.getVarID().getValue();
		
		int symbolTableIdx = findVarValue(varid);
		
		if (symbolTableIdx >= symbolTable.size()) {
			errorMsg = "Line " + lineCounter + ": ID Error; Given variable id is not instantiated ";
			return;
		}
		
		if (window != null) {
			//	ask user for value
			value = window.getYarnInput(varid);
			
			//	replace special characters if used
			value = value.replaceAll(":>", "\t");
			value = value.replaceAll(":\\)", "\n");
			value = value.replaceAll(":o", "\\\\g");
			value = value.replaceAll("::", ":");
			value = value.replaceAll(":\"", "\"");
			
			token = new Token (TokenKind.yarnToken, value, -1);
		} else {
			token = new Token (TokenKind.yarnToken, "", -1);
		}
		
		symbolTable.get(symbolTableIdx).setKindValue(token);	
	}
	
	
	
	
	
	
	private void evalIfBlock(NodeMultiLine node) {
		ArrayList<SyntaxNode> statements = node.getStatements();
		ArrayList<SyntaxNode> ifConditions = node.getIfConditions();
		Token boolCondition = symbolTable.get(0).getToken();
		boolCondition = typecastToken(boolCondition, TokenKind.troofToken);
		int counter = 1;
		
		//	execute the first statement node if true
		if (boolCondition.getValue().equals("WIN")) {
			evaluate(statements.get(0));
			
			return;
		} else if (ifConditions.size() > 0) {
			//	checks MEBBE block if its true
			for (SyntaxNode i : ifConditions) {
				boolCondition = typecastToken(evalTerminal(i), TokenKind.troofToken);
				
				if (boolCondition.getValue().equals("WIN")) {
					evaluate(statements.get(counter));
					return;
				}
				
				counter++;
			}
			
			//	execute else block if it exists
			if (ifConditions.get(ifConditions.size() - 1) instanceof NodeLiteral) {
				evaluate(statements.get(statements.size() - 1));
			}
		}
		
	}
	
	private void evalSwitchCase(NodeMultiLine node) {
		ArrayList<SyntaxNode> statements = node.getStatements();
		ArrayList<SyntaxNode> switchLiterals = node.getIfConditions();
		NodeLiteral switchCondition = new NodeLiteral(symbolTable.get(0).getToken());
		NodeOperation comparison;
		int counter = 0;
		
		for (SyntaxNode i : switchLiterals) {
			comparison = new NodeOperation(SyntaxType.cmpop, new Token(TokenKind.bothSameOpToken, "BOTH SAEM", -1), switchCondition, i);
			
			//	execute statement if IT value matches one of the literals in the cases or it has a default block
			if (evalCmpOp(comparison).getValue().equals("WIN") ||
				((NodeLiteral) i).getToken().getTokenKind() == TokenKind.defaultToken) {
				
				do {
					switchBreak = false;
					evaluate(statements.get(counter++));
				} while (!switchBreak && counter < statements.size());
				
				break;
			}
			
			counter++;
		}
		
		switchBreak = false;
		
	}
	
	private void evalLoop(NodeMultiLine node) {
		NodeDeclaration condition = (NodeDeclaration) node.getCondition();
		Token varid = ((NodeDeclaration) condition).getVarID();
		Token boolCondition;
		Token newValue;
		
		int incFactor, counter = 0, symbolTableIdx = findVarValue(varid.getValue());
		
		
		//	checking if given variable is valid
		if (symbolTableIdx >= symbolTable.size()) {
			errorMsg = "Line " + lineCounter + ": ID Error; Given variable id is not instantiated ";
			return;
		} else {
			varid = symbolTable.get(symbolTableIdx).getToken();
			
			if (varid.getTokenKind() != TokenKind.numbarToken &&
				varid.getTokenKind() != TokenKind.numbrToken) {
				errorMsg = "Line " + lineCounter + ": Type Error; Given variable id cannot be incremented/decremented ";
				return;
			}
			
		}
		
		//	decide if variable will be incremented or decremented
		if (node.getOpType().getTokenKind() == TokenKind.incToken) incFactor = 1;
		else incFactor = -1;
		
		
		while (counter++ < loopLimit) {
			if (condition.getOperation().getTokenKind() != TokenKind.troofToken) {
				boolCondition = evalCmpOp((NodeOperation) condition.getValue());
				
				if (condition.getOperation().getTokenKind() == TokenKind.tilToken &&
					boolCondition.getValue().equals("WIN")) break;
				else 
				if (condition.getOperation().getTokenKind() == TokenKind.wileToken &&
					boolCondition.getValue().equals("FAIL")) break; 
			}
			varid = symbolTable.get(symbolTableIdx).getToken();
			
			//	execute code blocks
			evaluate(node.getStatements().get(0));
			if (switchBreak) break;
			
			//	update variable
			if (varid.getTokenKind() == TokenKind.numbrToken) {
				newValue = new Token(TokenKind.numbrToken, Long.toString(Long.parseLong(varid.getValue()) + incFactor), -1);
				
				symbolTable.get(symbolTableIdx).setKindValue(newValue);
			} else {
				newValue = new Token(TokenKind.numbarToken, Double.toString(Double.parseDouble(varid.getValue()) + incFactor), -1);
	
				symbolTable.get(symbolTableIdx).setKindValue(newValue);
				
			}
			
		}

		switchBreak = false;		
		if (counter >= loopLimit && errorMsg.isEmpty()) errorMsg = "Line " + lineCounter + ": InfLoopWarning; Loop has exceeded maximum allowed iterations (" + loopLimit + ")";

	}
	
	
	
	
	
	
	//	return a token which is the value of the given operand
	private Token evalTerminal(SyntaxNode operand) {
		//	check if operand is a varid and if it is in the symboltable
		if (operand.getType() == SyntaxType.varid) {
			Token token = ((NodeLiteral) operand).getToken();
			int idx = findVarValue(token.getValue());
			
			if (idx == symbolTable.size()) {
				this.errorMsg = "Line "+ lineCounter + ": ID Error; Unbound variable <"+token.getValue()+">";
				return new Token(TokenKind.numbrToken, "0", -1);
			} else if (symbolTable.get(idx).getValue().isEmpty()) {
				this.errorMsg = "Line "+ lineCounter + ": ID Error; Uninitialized variable <"+token.getValue()+">";
				return new Token(TokenKind.numbrToken, "0", -1);
			} else {				
				return symbolTable.get(idx).getToken();
			}
			
		} else if (operand.getType() == SyntaxType.mathop) {
			return evalMathOp((NodeOperation) operand);
			
		} else if (operand.getType() == SyntaxType.boolop) {
			return evalBoolOp((NodeOperation) operand);
			
		} else if (operand.getType() == SyntaxType.cmpop) {
			return evalCmpOp((NodeOperation) operand);
					
		} else if (operand.getType() == SyntaxType.infarop) {
			return evalInfArOp((NodeOperation) operand);
			
		} else if (operand.getType() == SyntaxType.vartypechange) {
			return evalExpTypecast(operand);
			
		} else if (operand.getType() == SyntaxType.concat) {
			return evalConcat((NodeOperation) operand);
			
		} else if (operand.getType() == SyntaxType.functioncall) {
			return evalFunctionCall((NodeFunctionCall) operand);
			
		}
		
		return ((NodeLiteral) operand).getToken();
	}
	
	//	typecast the given token to the given kind specified
	private Token typecastToken(Token token, TokenKind kind) {
		double numbar = 0;
		long numbr = 0;
		boolean troof = true, isFloat = true, isInt = true;
		String yarn = new String();
		String noob = new String();
		
		if (token.getTokenKind() == kind) return token;
		
		//	typecasting token to all types
		if (token.getTokenKind() == TokenKind.numbrToken) {
			numbar = Double.parseDouble(token.getValue());
			numbr = (long) Double.parseDouble(token.getValue());
			yarn = token.getValue();
			noob = "0";
			
			if (numbr == 0) troof = false;
			else troof = true;
			
		} else if (token.getTokenKind() == TokenKind.numbarToken) {
			numbar = Double.parseDouble(token.getValue());
			numbr = (long) Double.parseDouble(token.getValue());
			yarn = token.getValue();
			noob = "0";
			
			if (numbar == (double) 0) troof = false;
			else troof = true;
			
		} else if (token.getTokenKind() == TokenKind.yarnToken) {
			//	attempt to convert yarn to long/double
			try {
				numbar = Double.parseDouble(token.getValue());
			} catch (Exception e) {
				isFloat = false;
			}
			
			try {
				numbr = Long.parseLong(token.getValue());
			} catch (Exception e) {
				isInt = false;
			}
			
			yarn = token.getValue();
			
			if (yarn.isBlank() || yarn.isEmpty()) troof = false;
			else troof = true;
			
		} else if (token.getTokenKind() == TokenKind.troofToken) {
			yarn = token.getValue();
			
			if (yarn.equals("WIN")) {
				numbar = (double) 1;
				numbr = 1;
				troof = true;
				
			} else {
				numbar = (double) 0;
				numbr = 0;
				troof = false;
			}
		} else if (token.getTokenKind() == TokenKind.noobToken) {
			isInt = false;
			isFloat = false;
			yarn = new String();
			troof = false;
		}
		
 		
		//	return a new token which is typecasted to the indicated type
		
		if (kind == TokenKind.noobToken) {
			return new Token(token.getTokenKind(), noob, token.getPosition());
		}
		
		if (kind == TokenKind.troofToken) {
			if (troof) return new Token(TokenKind.troofToken, "WIN", token.getPosition());
			else return new Token(TokenKind.troofToken, "FAIL", token.getPosition());
			
		} else if (kind == TokenKind.yarnToken) {
			return new Token(TokenKind.yarnToken, yarn, token.getPosition());
		
		}
		
		if (kind == TokenKind.numbrToken && (isInt || isFloat)) {
			return new Token(TokenKind.numbrToken, Long.toString((long) numbr), token.getPosition());
			
		} else if (kind == TokenKind.numbarToken && isFloat) {
			return new Token(TokenKind.numbarToken, Double.toString(numbar), token.getPosition());
		}
		
		
		errorMsg = "Line "+ lineCounter + ": Type Error; <" + token.getTokenKind() + "> cannot be typecasted to "
				+ "<" + kind + "> ";
		return new Token(TokenKind.badToken, "0", -1);
	}
	
	
	//	go through the symboltable to check if variable exists
	private int findVarValue(String varid) {
		int counter = 0;
		for (SymTabEntry entry : symbolTable) {
			if (entry.getIdentifier().equals(varid)) break;
			counter++;
		}

		return counter;
	}
	
	public void changeLoopLimit(int limit) {
		loopLimit = limit;
	}
	
	private void updateLineCounter() {
		//tokens.get(position).viewToken();

			
		while (tokens.get(position).getTokenKind() != TokenKind.eolToken &&
			   tokens.get(position).getTokenKind() != TokenKind.eofToken) {
			position++;
		}
		position++;
		lineCounter++;
		
		//tokens.get(position).viewToken();
		
	}
	
	public void viewParserErrors() {
		for (String i : parser.getDiagnostics()) System.out.println(i);
	}
	
	public void viewParseTree() {
		root.printChildren(0);
	}
	
	public String getStrParseTree() {
		return root.getStrChildren(0);
	}
	
	public boolean isPCEmpty() {
		if (programCounter == null) return true;
		
		return false;
	}
	
	public ArrayList<Token> getTokens() {
		return tokens;
	}
	
	public ArrayList<SymTabEntry> getSymbolTable() {
		return symbolTable;
	}
	
	public ArrayList<String> getParserDiagnostics() {
		return parser.getDiagnostics();
	}
	
	public String getEvalDiagnostics() {
		return errorMsg;
	}

	public int getCurrentLine() {
		return lineCounter;
	}

	//	gets the line number of the next instruction
	public int getNextLineNum() {
		SyntaxNode nextInstruction;

		//	no next line
		if (programCounter == null) return -1;

		//	get next instruction SyntaxNode
		if (programCounter.getType() == SyntaxType.statement) {
			nextInstruction = ((NodeStatement) programCounter).getOp1();
		} else {
			nextInstruction = programCounter;
		}


		if (nextInstruction.getType() == SyntaxType.expression) {
			return ((NodeExpression) nextInstruction).getLineCounter();
		} else if (nextInstruction.getType() == SyntaxType.assignment) {
			return ((NodeAssignment) nextInstruction).getLineCounter();
		} else {
			return ((NodeFlowControl) nextInstruction).getLineCounter();
		}
	}
}
