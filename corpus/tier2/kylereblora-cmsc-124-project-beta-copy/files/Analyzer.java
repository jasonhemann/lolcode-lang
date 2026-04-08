
	/*****************************************************************************************
	*  File Description:                                                                     *
	*  This file creates the analyzer for the back-end of the program.                       *
	*  The analyzer class acts analyzes both syntax and semantic analyzer                    *
	*****************************************************************************************/

//  --------------------------------------------------  [PACKAGE DECLARATION]
	package src;

//	--------------------------------------------------	[JAVA IMPORTS]
	import java.util.*;
	import javax.swing.*;
	import gui.*;

//  --------------------------------------------------  [CLASS SPECIFICATION]
public class Analyzer {

	/***************
	*  Attributes  *
	***************/
	private ArrayList<Lexeme> lexlist;
	private Boolean isComplete;
	private Boolean commentFlag;
	private Boolean condition;
	private Boolean flowFlag;
	private Boolean subFlowFlag;
	private Hashtable<Lexeme,Lexeme> storage;
	private Set<Lexeme> keys;
	private Lexeme it;
	private Lexeme lastLexeme;
	private Lexeme noob;
	private Lexeme expression;
	private LexemeTable table;
	private Parser parser;
	private Terminal terminal;
	private static int current = 0;

	/**************************
	*  Analyzer Constructors  *
	**************************/
	public Analyzer(Terminal terminal) {
		this.terminal = terminal;
		this.table = terminal.getInterpreter().getTable();
		this.it = new Lexeme("IT","Global Variable");
		this.noob = new Lexeme(null,"NOOB Literal");
		this.storage = new Hashtable<Lexeme,Lexeme>();
		this.commentFlag = this.flowFlag = this.subFlowFlag = false;
	}

	/****************
	*    Methods    *
	****************/

	public boolean analyze(ArrayList<Lexeme> lexlist) {
		/*-------------------------------------------------------------------------------------------------
			Method Description: This method starts the syntax analysis.
		-------------------------------------------------------------------------------------------------*/
		this.lexlist = lexlist;
		this.keys = this.storage.keySet();

		while (current != this.lexlist.size()) {

			Lexeme errorFree = determineType(this.lexlist.get(current));
			if (errorFree == null) {
				this.isComplete = true;
				return false;
			}
			this.lastLexeme = this.lexlist.get(current);
			this.lexlist.remove(current);
		} 

		return true;
	}

	private Lexeme determineType(Lexeme lexeme) {

		/* Conditional Statements*/

		// Condition 1: Lexemes are in a multi-line comment
		if (this.commentFlag && !lexeme.getLexType().equals("Multi-line Comment")) {
			return lexeme;

		// Condition 2: Lexemes are not inside the program
		} else if (!lexeme.getLexType().equals("Code Delimiter") && !lexeme.getLexType().equals("Comments") &&!lexeme.getLexType().equals("Multi-line Comment") && this.isComplete==null) {
			this.terminal.error(8003, 2);
			return null;

		// Condition 3: Lexemes are not to be executed
		} else if (this.flowFlag && !this.subFlowFlag && !lexeme.getLexType().equals("IF-THEN Statement")) {
			return lexeme;
		}

		System.out.println("Checking ( "+ lexeme.getRegex() +" ) lexeme...");
		switch(lexeme.getLexType()) {
			case "Comments": return comment(lexeme);
			case "Multi-line Comment": return multiLineComment(lexeme);
			case "Code Delimiter": return codeDelimiter(lexeme);
			case "Variable Declaration": return variableDeclaration(lexeme);
			case "Variable Identifier": return variableIdentifier(lexeme);
			case "Assignment Operator": return assignmentOperator(lexeme);
			case "Arithmetic Operator": return arithmeticOperator(lexeme);
			case "Boolean Operator": return booleanOperator(lexeme);
			case "Comparison Operator": return comparisonOperator(lexeme);
			case "Global Variable": return globalVariable(lexeme);
			case "Numbr Literal": return literal(lexeme);
			case "Numbar Literal": return literal(lexeme);
			case "Yarn Literal": return literal(lexeme);
			case "Troof Literal": return literal(lexeme);
			case "Operation Keyword": return operationKeyword(lexeme);
			case "Output Keyword": return visible(lexeme);
			case "Concatenation": return smoosh(lexeme);
			case "Input Keyword": return gimmeh(lexeme);
			case "IF-THEN Statement": return controlFlowIfThen(lexeme);
			default: return null;
		}
	}

	private Lexeme checkStorage(Lexeme lexeme) {
		for (Lexeme i: this.keys) {
			if (lexeme.getRegex().equals(i.getRegex())) return i;
		} return null;
	}

	/****************
	*    Getters    *
	****************/
	public Hashtable<Lexeme,Lexeme> getStorage(){ return this.storage; }
	public ArrayList<Lexeme> getLexemes() {return this.lexlist;}
	public Lexeme getIt() {return this.it;}
	public int getCurrent(){ return this.current;}
	public boolean getCommentFlag() {return this.commentFlag;}
	public boolean getStatus() {
		if (this.isComplete == null) return true;
		return this.isComplete;
	}

	/****************
	*    Setters    *
	****************/
	public void reset(){
		this.isComplete = null;
		this.commentFlag = this.flowFlag = this.subFlowFlag = false;
		this.storage.clear();
	}

	public void setParser(Parser parser) { this.parser = parser; }

/*******************************************************************************************************************
	>> FUNCTIONS NEEDED FOR ANALYSIS
*******************************************************************************************************************/
	
	private Lexeme comment(Lexeme lexeme) {
		
		this.commentFlag = true;
		int index = this.lexlist.indexOf(lexeme);
		
		this.table.getModel().addRow(new Object[]{this.lexlist.get(index).getRegex(),this.lexlist.get(index).getLexType()});
		System.out.println("\nProcessing comment lexeme...\n");

		while (this.lexlist.size() > index+1) {
			this.lexlist.remove(index+1);
		}

		this.commentFlag = false;
		return lexeme;
	}

	private Lexeme multiLineComment(Lexeme lexeme) {

		// Lexeme to Table

		// Condition 1: The program will skip comments.
		 if (this.commentFlag == false) {
			if (lexeme.getRegex().equals("TLDR")) {
				this.terminal.error(8007,1);
				return null;
			} else if (lexeme.getRegex().equals("OBTW")) {
				this.commentFlag = true;
			}

		// Condition 3: The program will finish commenting.
		} else if (this.commentFlag == true) {
			if (lexeme.getRegex().equals("TLDR")) this.commentFlag = false;
		}
		this.table.getModel().addRow(new Object[]{this.lexlist.get(current).getRegex(),this.lexlist.get(current).getLexType()});
		return lexeme;
	}

	private Lexeme codeDelimiter(Lexeme lexeme) {

		// Lexeme to Table
		this.table.getModel().addRow(new Object[]{this.lexlist.get(current).getRegex(),this.lexlist.get(current).getLexType()});

		// Condition 1: The program has not been initialized.
		if (this.isComplete == null) {
			if (lexeme.getRegex().equals("HAI")) {
				this.isComplete = false;
				return lexeme;
			} else if (lexeme.getRegex().equals("KTHXBYE")) {
				this.terminal.error(8101, 1);
				return null;
			}

		// Condition 2: The program has been initialized.
		} else if (this.isComplete == false) {
			if (lexeme.getRegex().equals("HAI")) {
				this.terminal.error(8005, 2);
				return null;
			} else if (lexeme.getRegex().equals("KTHXBYE")) {
				this.isComplete = true;
				return lexeme;
			}

		// Condition 3: The program has finished.
		} else if (this.isComplete == true) {
			if (lexeme.getRegex().equals("HAI")) {
				this.terminal.error(8000, 1);
				return null;
			} else if (lexeme.getRegex().equals("KTHXBYE")) {
				this.terminal.error(8001, 1);
				return null;
			} 

		} return lexeme;
	}

	private Lexeme variableDeclaration(Lexeme lexeme) {

		this.lastLexeme = lexeme;

		int index = this.lexlist.indexOf(lexeme);
		this.keys = this.storage.keySet();
		this.table.getModel().addRow(new Object[]{this.lexlist.get(index).getRegex(),this.lexlist.get(index).getLexType()});
		
		// Condition 1: Variable Declaration Without Arguments
		if (this.lexlist.size() == index+1) {
			this.terminal.error(8102,2);
			return null;
		}

		// Condition 2: Variable Declaration With An Argument
		Lexeme variable = determineType(this.lexlist.get(index+1));
		if (variable==null) return null;

		// Condition 3: No Additional Statement Included
		this.lexlist.remove(index+1); variable = this.storage.get(checkStorage(this.it));
		this.storage.put(variable, this.noob);
		if (this.lexlist.size() == index+1) return lexeme;

		// Condition 4: Variable Assignment -- (Optional)
		if (!this.lexlist.get(index+1).getLexType().equals("Variable Assignment")) {
			this.terminal.error(8202,2);
			return null;
		} this.table.getModel().addRow(new Object[]{this.lexlist.get(index+1).getRegex(),this.lexlist.get(index+1).getLexType()});

		// Condition 5: Variable Assignment Without Arguments
		this.lexlist.remove(index+1);
		if (this.lexlist.size() == index+1) {
			this.terminal.error(8103,2);
			return null;
		}

		// Condition 6: Variable Assignment With An Argument
		Lexeme value = determineType(this.lexlist.get(index+1));
		if (value==null) return null;

		// Condition 7: Variable Value is a variable
		if (value.getLexType().equals("Variable Identifier")) {
			value = checkStorage(value);
			this.storage.put(variable, this.storage.get(value)); return lexeme;
		} this.lexlist.remove(index+1);

		// Condition 8: Variable Value is NOT a variable
		this.storage.put(variable, this.storage.get(it));
		return lexeme;
	}

	private Lexeme variableIdentifier(Lexeme lexeme) {

		Boolean isFound = false; int index = this.lexlist.indexOf(lexeme);
		this.lastLexeme = lexeme;
		this.table.getModel().addRow(new Object[]{this.lexlist.get(index).getRegex(),this.lexlist.get(index).getLexType()});

		// Search: Lexeme in Table
		Lexeme temporaryVariable = checkStorage(lexeme);

		// Condition 1: Variable Not In The Storage
		if(temporaryVariable==null) {

			// Condition 1.1: Variable will be used for declaration
			if (this.lexlist.get(current).getLexType().equals("Variable Declaration")) {
				this.storage.put(this.it,lexeme);
				return lexeme;

			// Condition 1.2: Variable uninitialized
			} else if (this.lastLexeme.getLexType().equals("Output Keyword")) {
				current++;
				this.terminal.error(8104,2);
				current = 0;
				return null;
			} else {
				this.terminal.error(8104,2);
				return null;
			}

		// Condition 2: Variable is in Storage
		} else {
			if (this.lexlist.size() == index+1) {this.storage.put(this.it, temporaryVariable);}
			else {this.storage.put(this.it, this.storage.get(temporaryVariable));}
			return lexeme;
		}
	}

	private Lexeme assignmentOperator(Lexeme lexeme) {

		int index = this.lexlist.indexOf(lexeme);

		// Condition 1: No Preceding Statements Found
		if (!this.lastLexeme.getLexType().equals("Variable Identifier") && !this.lastLexeme.getLexType().equals("Global Variable")) {
			this.terminal.error(8105,2);
			return null;

		} else {

		// Condition 2: No Statements Found After R Operator
			if (this.lexlist.size() == index+1) {
				this.terminal.error(8106,2);
				return null;
			}

		// Condition 3: Invalid Argument for Operator
			Lexeme variable = checkStorage(lastLexeme);

			this.table.getModel().addRow(new Object[]{this.lexlist.get(index).getRegex(),this.lexlist.get(index).getLexType()});

			Lexeme value = determineType(this.lexlist.get(index+1));
			if (value == null) {
				this.terminal.error(8200,2);
				return null;
			}

		// Condition 4: Valid Argument for Operator
			this.lexlist.remove(index+1);
			this.storage.put(variable, this.storage.get(it));
		} return lexeme;	
	}

	private Lexeme arithmeticOperator(Lexeme lexeme) {
		
		Object x=null,y=null;

		Lexeme operation = lexeme; int index = this.lexlist.indexOf(lexeme);
		this.table.getModel().addRow(new Object[]{this.lexlist.get(index).getRegex(),this.lexlist.get(index).getLexType()});

		// Condition 1: No Statements found after operator
		if (this.lexlist.size() == index+1) {
			this.terminal.error(8108,2);
			return null;
		}

		// Condition 2: Argument X is invalid
		Lexeme variableX = determineType(this.lexlist.get(index+1)), tempX = null;
		if (variableX==null) {
			this.terminal.error(8108,2);
			return null;
		}

		// Condition 3: Argument X is valid
		switch(variableX.getLexType()) {
			case "Numbr Literal": x = Integer.parseInt(this.storage.get(it).getRegex()); break;
			case "Numbar Literal": x = Float.valueOf(this.storage.get(it).getRegex().trim()).floatValue(); break;
			case "Yarn Literal":
				tempX = this.parser.parse(variableX.getRegex());
				if (tempX.getLexType().equals("Numbr Literal")) x = Integer.parseInt(tempX.getRegex());
				else if (tempX.getLexType().equals("Numbar Literal")) x = Float.valueOf(tempX.getRegex().trim()).floatValue();
				else {this.terminal.error(6100,2); return null; }
				break;
			case "Variable Identifier":
				tempX = this.checkStorage(variableX);
				if (this.storage.get(tempX).getLexType().equals("Numbr Literal")) x = Integer.parseInt(this.storage.get(tempX).getRegex());
				else if (this.storage.get(tempX).getLexType().equals("Numbar Literal")) x = Float.valueOf(this.storage.get(tempX).getRegex().trim()).floatValue();
				else if (this.storage.get(tempX).getLexType().equals("Yarn Literal")) {
					tempX = this.parser.parse(this.storage.get(tempX).getRegex());
					if (tempX.getLexType().equals("Numbr Literal")) x = Integer.parseInt(tempX.getRegex());
					else if (tempX.getLexType().equals("Numbar Literal")) x = Float.valueOf(tempX.getRegex().trim()).floatValue();
					else {this.terminal.error(6100,2); return null; }
				}
				break;
			default: return null;
		}

		// Condition 4: Uses AN operator
		this.lexlist.remove(index+1);
		if(!this.lexlist.get(index+1).getLexType().equals("Operation Keyword")) {
			this.terminal.error(8107,2);
			return null;
		} this.table.getModel().addRow(new Object[]{this.lexlist.get(index+1).getRegex(),this.lexlist.get(index+1).getLexType()}); this.lexlist.remove(index+1);

		// Condition 5: No statements found after AN Operator
		if (this.lexlist.size() == index+1) {
			this.terminal.error(8108,2);
			return null;
		}

		// Condition 6: Argument Y is invalid
		Lexeme variableY = determineType(this.lexlist.get(index+1)), tempY = null;
		if (variableY==null) {
			return null;
		}

		// Condition 7: Argument Y is valid
		switch(variableY.getLexType()) {
			case "Numbr Literal": y = Integer.parseInt(this.storage.get(it).getRegex()); break;
			case "Numbar Literal": y = Float.valueOf(this.storage.get(it).getRegex().trim()).floatValue(); break;
			case "Yarn Literal":
				tempY = this.parser.parse(variableY.getRegex());
				if (tempY.getLexType().equals("Numbr Literal")) y = Integer.parseInt(tempY.getRegex());
				else if (tempY.getLexType().equals("Numbar Literal")) y = Float.valueOf(tempY.getRegex().trim()).floatValue();
				else {this.terminal.error(6100,2); return null;}
				break;
			case "Variable Identifier":
				tempY = this.checkStorage(variableY);
				if (this.storage.get(tempY).getLexType().equals("Numbr Literal")) y = Integer.parseInt(this.storage.get(tempY).getRegex());
				else if (this.storage.get(tempY).getLexType().equals("Numbar Literal")) y = Float.valueOf(this.storage.get(tempY).getRegex().trim()).floatValue();
				else if (this.storage.get(tempY).getLexType().equals("Yarn Literal")) {
					tempY = this.parser.parse(this.storage.get(tempY).getRegex());
					if (tempY.getLexType().equals("Numbr Literal")) y = Integer.parseInt(tempY.getRegex());
					else if (tempY.getLexType().equals("Numbar Literal")) y = Float.valueOf(tempY.getRegex().trim()).floatValue();
					else {this.terminal.error(6100,2); return null; }
				}
				break;
			default: this.terminal.error(8203,2); return null;
		} this.lexlist.remove(index+1);

		// Condition 8: Both X and Y are valid
		Lexeme result = new Lexeme(null,"NOOB Literal");

			// Condition 8.1: Both X and Y are integers
		if (x instanceof Integer && y instanceof Integer) {
			switch (operation.getRegex()) {
				case "SUM OF": result = integerOperator(x,y,1); break;
				case "DIFF OF": result = integerOperator(x,y,2); break;
				case "PRODUKT OF": result = integerOperator(x,y,3); break;
				case "QUOSHUNT OF": result = integerOperator(x,y,4); break;
				case "MOD OF": result = integerOperator(x,y,5); break;
				case "BIGGR OF": result = integerOperator(x,y,6); break;
				case "SMALLR OF": result = integerOperator(x,y,7); break;
				default: break;
			}
		} else if (!(x instanceof Integer || x instanceof Float) || !(y instanceof Integer || y instanceof Float)) {
			this.terminal.error(6100,2);
			return null;
		} else if (x instanceof Float || y instanceof Float) {
			switch (operation.getRegex()) {
				case "SUM OF": result = floatOperator(x,y,1); break;
				case "DIFF OF": result = floatOperator(x,y,2); break;
				case "PRODUKT OF": result = floatOperator(x,y,3); break;
				case "QUOSHUNT OF": result = floatOperator(x,y,4); break;
				case "MOD OF": result = floatOperator(x,y,5); break;
				case "BIGGR OF": result = floatOperator(x,y,6); break;
				case "SMALLR OF": result = floatOperator(x,y,7); break;
				default: break;
			}
		}
		
		this.storage.put(it,result);
		return result;
	}

	private Lexeme booleanOperator(Lexeme lexeme) {

		Object x=null,y=null;

		Lexeme operation = lexeme; int index = this.lexlist.indexOf(lexeme);
		this.table.getModel().addRow(new Object[]{this.lexlist.get(index).getRegex(),this.lexlist.get(index).getLexType()});

		// Condition 1: No Statements found after operator
		if (this.lexlist.size() == index+1) {
			this.terminal.error(8110,2);
			return null;
		}

		// Condition 2: Argument X is invalid
		Lexeme variableX = determineType(this.lexlist.get(index+1)), tempX = null;
		if (variableX == null) {
			this.terminal.error(8108,2);
			return null;
		}

		if (this.lexlist.size() == index+1) {
			this.terminal.error(8111,2);
			return null;
		}

		// Condition 3: Argument X is valid
		switch(variableX.getLexType()) {
			case "Troof Literal" : 
				if (variableX.getRegex().equals("WIN")) { x = true; }
				else if (variableX.getRegex().equals("FAIL")) { x = false; }
				break;
			case "Variable Identifier" : 
				tempX = this.checkStorage(variableX);
				if (this.storage.get(tempX).getLexType().equals("Troof Literal")){
					if (this.storage.get(tempX).getRegex().equals("WIN")) x = true;
					else if (this.storage.get(tempX).getRegex().equals("FAIL")) x = false;
					break;
				} else {
					this.terminal.error(8700, 2);
					return null;
				}
			default: break;
		} this.lexlist.remove(index+1);

		Lexeme result = new Lexeme(null,"NOOB Literal");
		// Condition 5: Infinite Arity
		do {
			// Condition 4: The operation is a binary operation
			if (!operation.getRegex().equals("NOT")) {

				// Condition 5.0
				if (this.lexlist.size()==index+1 && (operation.getRegex().equals("ALL OF") && operation.getRegex().equals("ANY OF"))) {
					this.terminal.error(8701,1);
					return null;
				} else if (this.lexlist.size()==index+1) {
					this.terminal.error(8111,2);
					return null;
				}

				// Condition 5.1: Uses AN operator
				if(!this.lexlist.get(index+1).getLexType().equals("Operation Keyword")) {
					this.terminal.error(8107,2);
					return null;
				} this.table.getModel().addRow(new Object[]{this.lexlist.get(index+1).getRegex(), this.lexlist.get(index+1).getLexType()});
				this.lexlist.remove(index+1);

				// Condition 5.2: No statements found after AN Operator
				if (this.lexlist.size() == index+1) {
					this.terminal.error(8108,2);
					return null;
				}

				// Condition 5.3: Argument Y is invalid
				Lexeme variableY = determineType(this.lexlist.get(index+1)), tempY = null;
				if (variableY == null) {
					this.terminal.error(8108,2);
					return null;
				}

				// Condition 5.4: Argument Y is valid
				switch(variableY.getLexType()) {
					case "Troof Literal" : 
						if (variableY.getRegex().equals("WIN")) { y = true; }
						else if (variableY.getRegex().equals("FAIL")) { y = false; }
						break;
					case "Variable Identifier" : 
						tempY = this.checkStorage(variableY);
						if (this.storage.get(tempY).getLexType().equals("Troof Literal")){
							if (this.storage.get(tempY).getRegex().equals("WIN")) { y = true; }
							else if (this.storage.get(tempY).getRegex().equals("FAIL")) { y = false; }
							break;
						} else {
							this.terminal.error(8700, 2);
							return null;
						}	
					default: break;
				} this.lexlist.remove(index+1);
			}

			// Condition 8: Both X and Y are valid

				// Condition 8.1: Both are TROOFs
				if (x instanceof Boolean && y instanceof Boolean) {
					switch (operation.getRegex()) {
						case "BOTH OF": result = boolOperation(x,y,1); break;
						case "EITHER OF": result = boolOperation(x,y,2); break;
						case "WON OF": result = boolOperation(x,y,3); break;
						case "ALL OF": result = boolOperation(x,y,1); break;
						case "ANY OF": result = boolOperation(x,y,2); break;
						default: break;
					}
				} else if (x instanceof Boolean) {
					switch (operation.getRegex()) {
						case "NOT": result = boolOperation(x,null,0); break;
						default: break;
					}
				}

			this.storage.put(this.it,result);

			if (!operation.getRegex().equals("ANY OF") && !operation.getRegex().equals("ALL OF")) {
				return result;

			} else if (this.lexlist.size() > index+1) {
				if (this.lexlist.get(index+1).getLexType().equals("Boolean Delimiter")) {
					this.table.getModel().addRow(new Object[]{this.lexlist.get(index+1).getRegex(),this.lexlist.get(index+1).getLexType()});				
					this.lexlist.remove(index+1); return result;
				} 

			}

			if (result.getRegex().equals("WIN")) x = true;
			else x =false;

		}  while (this.lexlist.size() > index+1);

		return result; 
	}

	private Lexeme comparisonOperator(Lexeme lexeme) {

		Object x=null,y=null;

		Lexeme operation = lexeme; int index = this.lexlist.indexOf(lexeme);
		this.table.getModel().addRow(new Object[]{this.lexlist.get(index).getRegex(),this.lexlist.get(index).getLexType()});

		// Condition 1: No Statements found after operator
		if (this.lexlist.size() == index+1) {
			this.terminal.error(8108,2);
			return null;
		}

		// Condition 2: Argument X is invalid
		Lexeme variableX = determineType(this.lexlist.get(index+1)), tempX = null;
		if (variableX==null) {
			this.terminal.error(8108,2);
			return null;
		}

		// Condition 3: Argument X is valid
		switch(variableX.getLexType()) {
			case "Numbr Literal": x = Integer.parseInt(this.storage.get(it).getRegex()); break;
			case "Numbar Literal": x = Float.valueOf(this.storage.get(it).getRegex().trim()).floatValue(); break;
			case "Yarn Literal":
				tempX = this.parser.parse(variableX.getRegex());
				if (tempX.getLexType().equals("Numbr Literal")) x = Integer.parseInt(tempX.getRegex());
				else if (tempX.getLexType().equals("Numbar Literal")) x = Float.valueOf(tempX.getRegex().trim()).floatValue();
				else {this.terminal.error(6100,2); return null; }
				break;
			case "Variable Identifier":
				tempX = this.checkStorage(variableX);
				if (this.storage.get(tempX).getLexType().equals("Numbr Literal")) x = Integer.parseInt(this.storage.get(tempX).getRegex());
				else if (this.storage.get(tempX).getLexType().equals("Numbar Literal")) x = Float.valueOf(this.storage.get(tempX).getRegex().trim()).floatValue();
				else if (this.storage.get(tempX).getLexType().equals("Yarn Literal")) {
					tempX = this.parser.parse(variableX.getRegex());
					if (tempX.getLexType().equals("Numbr Literal")) x = Integer.parseInt(tempX.getRegex());
					else if (tempX.getLexType().equals("Numbar Literal")) x = Float.valueOf(tempX.getRegex().trim()).floatValue();
					else {this.terminal.error(6100,2); return null; }
					break;
				}
				break;
			default: return null;
		}

		// Condition 4: Uses AN operator
		this.lexlist.remove(index+1);
		if(!this.lexlist.get(index+1).getLexType().equals("Operation Keyword")) {
			this.terminal.error(8107,2);
			return null;
		} this.table.getModel().addRow(new Object[]{this.lexlist.get(index+1).getRegex(),this.lexlist.get(index+1).getLexType()}); this.lexlist.remove(index+1);

		// Condition 5: No statements found after AN Operator
		if (this.lexlist.size() == index+1) {
			this.terminal.error(8108,2);
			return null;
		}

		// Condition 6: Argument Y is invalid
		Lexeme variableY = determineType(this.lexlist.get(index+1)), tempY = null;
		if (variableY==null) {
			return null;
		}

		// Condition 7: Argument Y is valid
		switch(variableY.getLexType()) {
			case "Numbr Literal": y = Integer.parseInt(this.storage.get(it).getRegex()); break;
			case "Numbar Literal": y = Float.valueOf(this.storage.get(it).getRegex().trim()).floatValue(); break;
			case "Yarn Literal":
				tempY = this.parser.parse(variableY.getRegex());
				if (tempY.getLexType().equals("Numbr Literal")) y = Integer.parseInt(tempY.getRegex());
				else if (tempY.getLexType().equals("Numbar Literal")) y = Float.valueOf(tempY.getRegex().trim()).floatValue();
				else {this.terminal.error(6100,2); return null;}
				break;
			case "Variable Identifier":
				tempY = this.checkStorage(variableY);
				if (this.storage.get(tempY).getLexType().equals("Numbr Literal")) y = Integer.parseInt(this.storage.get(tempY).getRegex());
				else if (this.storage.get(tempY).getLexType().equals("Numbar Literal")) y = Float.valueOf(this.storage.get(tempY).getRegex().trim()).floatValue();
				else if (this.storage.get(tempY).getLexType().equals("Yarn Literal")) {
					tempY = this.parser.parse(variableY.getRegex());
					if (tempY.getLexType().equals("Numbr Literal")) y = Integer.parseInt(tempY.getRegex());
					else if (tempY.getLexType().equals("Numbar Literal")) y = Float.valueOf(tempY.getRegex().trim()).floatValue();
					else {this.terminal.error(6100,2); return null;}
					break;
				}
				break;
			default: return null;
		} this.lexlist.remove(index+1);

		// Condition 8: Both X and Y are valid
		Lexeme result = new Lexeme(null,"NOOB Literal");

		switch (operation.getRegex()) {
				case "BOTH SAEM": result = comparisonOperation(x,y,1); break;
				case "DIFFRINT": result = comparisonOperation(x,y,2); break;
				default: break;
		}
		
		this.storage.put(checkStorage(it),result);
		return result;
	}

	private Lexeme integerOperator(Object x, Object y, int code) {

		int a = (int) x; int b = (int) y; int answer = 0;

		switch (code) {
			case 1: answer = a+b; break;
			case 2: answer = a-b; break;
			case 3: answer = a*b; break;
			case 4: answer = a/b; break;
			case 5: answer = a%b; break;
			case 6:
				if (a>b) answer = a;
				else answer = b;
				break;
			case 7:
				if (a<b) answer = a;
				else answer = b;
				break;
			default: break;
		}

		return new Lexeme(Integer.toString(answer),"Numbr Literal");
	}

	private Lexeme floatOperator(Object x, Object y, int code) {

		float answer=0;
		float a = ((Number)x).floatValue();
		float b = ((Number)y).floatValue();

		switch (code) {
			case 1: answer = a+b; break;
			case 2: answer = a-b; break;
			case 3: answer = a*b; break;
			case 4: answer = a/b; break;
			case 5: answer = a%b; break;
			case 6:
				if (a>b) answer = a;
				else answer = b;
				break;
			case 7:
				if (a<b) answer = a;
				else answer = b;
				break;
			default: break;
		}

		return new Lexeme(Float.toString(answer),"Numbar Literal");
	}

	private Lexeme boolOperation(Object x, Object y, int code) {

		Boolean a = (Boolean) x; Boolean b = (Boolean) y; boolean answer = true;

		switch (code) {
			case 0:
				if (a == true) answer = false;
				else answer = true;
				break;
			case 1: answer = a && b; break;
			case 2: answer = a || b; break;
			case 3: 
				if (a == b) answer = false;
				else answer = true;
				break;
			default: break;
		}

		String result = "";
		if(answer == true) result = "WIN";
		else result = "FAIL";

		return new Lexeme(result,"Troof Literal");
	}

	private Lexeme comparisonOperation(Object x, Object y, int code) {
		Boolean answer = false; String result = "";
		switch (code) {
			case 1:
				if (x == y) answer = true;
				else answer = false;
				break;
			case 2:
				if (x != y) answer = true;
				else answer = false;
				break;
			default: break;
		} System.out.println(answer);

		if(answer == true) result = "WIN";
		else result = "FAIL";

		return new Lexeme(result,"Troof Literal");
	}

	private Lexeme operationKeyword(Lexeme lexeme) {
	
		int index = this.lexlist.indexOf(lexeme);
		this.table.getModel().addRow(new Object[]{this.lexlist.get(index).getRegex(), this.lexlist.get(index).getLexType()});
		if (this.lexlist.get(current) == lexeme) {
			this.terminal.error(8008,2);
			return null;
		}
		return lexeme;
	}

	private Lexeme gimmeh(Lexeme lexeme) {
		
		this.table.getModel().addRow(new Object[]{this.lexlist.get(current).getRegex(), this.lexlist.get(current).getLexType()});
		this.lexlist.remove(current);
		if(this.lexlist.size() == 0) {
			this.terminal.error(8109, 2);
			return null;
		}
		
		Lexeme variable = this.checkStorage(this.lexlist.get(current));
		this.table.getModel().addRow(new Object[]{this.lexlist.get(current).getRegex(), this.lexlist.get(current).getLexType()});
		if (variable != null) {
			JFrame popUp = new JFrame();
			String input = JOptionPane.showInputDialog(popUp,"KYAH PENGENG INPUT... TEH. (o3o)", null);
			this.storage.put(this.it, new Lexeme(input, "Yarn Literal"));
			this.storage.put(variable, this.storage.get(this.it));
			return lexeme;
		}

		this.terminal.error(8104,2);
		return null;
	}

	private Lexeme visible(Lexeme lexeme) {
		int index = this.lexlist.indexOf(lexeme);
		this.table.getModel().addRow(new Object[]{this.lexlist.get(index).getRegex(),this.lexlist.get(index).getLexType()});

		// Condition 1: Preceding Statements Before Visible
		if (this.lexlist.get(current) != lexeme) {
			this.terminal.error(8300, 2);
			return null;

		} else {

			this.lastLexeme = lexeme;
		// Condition 2: No Statements Found After Visible
			if (this.lexlist.size() == index) {
				this.terminal.print("\n");
				return lexeme;
			}

		// Condition 3: Valid Statements Found
			String message = "";
			while (this.lexlist.size() > index+1) {
				
				Lexeme temporaryLexeme = determineType(this.lexlist.get(index+1));

				// Condition 3.1: The statement to be printed is invalid
				if (temporaryLexeme==null) return null;

				// Condition 3.2: The statement to be printed is a literal
				else if (temporaryLexeme.getLexType().equals("Numbr Literal") || temporaryLexeme.getLexType().equals("Numbar Literal") || temporaryLexeme.getLexType().equals("Yarn Literal") || temporaryLexeme.getLexType().equals("Troof Literal")){
					temporaryLexeme = new Lexeme(this.parser.removeQuotes(temporaryLexeme.getRegex()),temporaryLexeme.getLexType());
					message += temporaryLexeme.getRegex() + " ";

				// Condition 3.3: The statement to be printed is a variable
				} else if (temporaryLexeme.getLexType().equals("Variable Identifier") || temporaryLexeme.getLexType().equals("Global Variable")) {
					message += this.storage.get(this.checkStorage(temporaryLexeme)).getRegex() + " ";

				// Condition 3.4: The statements were not met
				} else if (temporaryLexeme.getLexType().equals("Comments")) {
					break;

				} else return null;


		 		this.lexlist.remove(index+1);
			
			} message+= "\n";

			this.storage.put(this.it, new Lexeme(message, "Yarn Literal"));
			this.terminal.print(message);
		 	
			if(this.lexlist.size() == index){
				if (this.lexlist.get(index+1).getLexType().equals("Comments")){
				 	this.lexlist.remove(index+1);
				}
			}	

		}

		return lexeme;
	}

	private Lexeme smoosh(Lexeme lexeme) {

		String concatenated = "", tailString = "";
		int index = this.lexlist.indexOf(lexeme);
		this.table.getModel().addRow(new Object[]{this.lexlist.get(index).getRegex(), this.lexlist.get(index).getLexType()});

		// Condition 1: Invalid X Argument
		Lexeme variableX = determineType(this.lexlist.get(index+1));
		if (variableX==null) {
			this.terminal.error(8602,2);
			return null;
		} concatenated = this.storage.get(it).getRegex();
		concatenated = this.parser.removeQuotes(concatenated);

		// Condition 2: No values after SMOOSH keyword
		if(this.lexlist.size() == index+1) {
			this.terminal.error(8107,2);
			return null;
		} 

		this.lexlist.remove(index+1);

		// Condition 3: Infinite Arity
		while (this.lexlist.size() > index+1){
			// Condition 3.1: Uses AN keyword
			if(!this.lexlist.get(index+1).getLexType().equals("Operation Keyword")) {
				this.terminal.error(8107,2);
				return null;
			}

			// Condition 4: Invalid Y Argument
			this.table.getModel().addRow(new Object[]{this.lexlist.get(index+1).getRegex(), this.lexlist.get(index+1).getLexType()});			
			this.lexlist.remove(index+1);
			Lexeme variableY = determineType(this.lexlist.get(index+1));
			if (variableY == null) {
				this.terminal.error(8602,2);
				return null;
			} tailString = this.storage.get(it).getRegex();


			this.lexlist.remove(index+1);
			concatenated += this.parser.removeQuotes(tailString);
		} 

		this.storage.put(it, new Lexeme(concatenated, "Yarn Literal"));
		return new Lexeme(concatenated, "Yarn Literal");
	}

	private Lexeme globalVariable (Lexeme lexeme) {
		this.lastLexeme = lexeme;
		if (this.lexlist.get(current).getLexType().equals("Variable Declaration")) {
			this.terminal.error(8006,1);
			return null;
		} else if (this.lexlist.get(current).getLexType().equals("Output Keyword")) {
			return this.storage.get(this.checkStorage(lexeme));
		} return lexeme;
	}

	private Lexeme literal(Lexeme lexeme) {

		int index = this.lexlist.indexOf(lexeme);
		this.table.getModel().addRow(new Object[]{this.lexlist.get(index).getRegex(),this.lexlist.get(index).getLexType()});

		this.storage.put(this.it, lexeme);
		return lexeme;
	}

	private Lexeme controlFlowIfThen(Lexeme lexeme) {

		this.table.getModel().addRow(new Object[]{this.lexlist.get(current).getRegex(),this.lexlist.get(current).getLexType()});
		switch (lexeme.getRegex()) {
			case "O RLY?":
				this.expression = this.storage.get(this.it);
				this.condition = false;
				if (expression.getRegex().equals("WIN")) condition = true;
				else condition = false;
				flowFlag = true;
				break;
			case "YA RLY":
				if (condition==true) subFlowFlag = true;
				break;
			case "NO WAI":
				if (condition==false) subFlowFlag = true;
				else subFlowFlag = false;
				break;
			case "OIC":
				flowFlag = false;
				break;
			default: break;
		}

		return lexeme;
	}

	private Lexeme invalidStatement(Lexeme lexeme) {
		if (this.terminal.getExecuteButton().getAnalyzer().getCommentFlag() == false) {			    		
			this.terminal.error(3000,2);
			return null;
		}
		return lexeme;
	}

}