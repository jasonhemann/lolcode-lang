using System;
using LolcodeInterpreter;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Text.RegularExpressions;

namespace LolcodeInterpreter
{
	public class Parser
	{
		// Dictionary of Variables declared
		private Dictionary <String, Variable> variablesDictionary;

		// ArrayList of Tokens received from Lexical Analyzer
		private ArrayList tokensArrayList;

		// Current index of tokensArrayList being traversed
		private int currentPosition;


		// Stores prefix representation of the expression
		private String expressionString = "";


		// Flags

		// Universal Flag
		private bool skip = false; // whether the statement will be interpreted or not

		// Visible Flag
		private bool printEntered;
		private bool suppressNewLine;

		// Infinity Arity Flag:
			// will set to true if encountered ALL OF / ANY OF
			// will set to false if encountered MKAY
		private bool allOfFlag = false;
		private bool anyOfFlag = false;

		// WTF? Flag (Switch case)
		private bool switchEntered = false; // entered switch-case statement
		private bool omgBlockEntered = false; // entered case
		private bool gtfoed = false; // if flow is already stopped (encountered GTFO)
		private bool flow = false; // proceed to next case
		private bool matched = false; // if condition is satisfied

		private bool concatenationEntered = false;

		// If else flag
		private bool ifEntered = false; // entered YA RLY
		private bool elseEntered = false; // entered NO WAI (consider possibility of encountering OIC

		// True / False - WIN / FAIL Equivalence
		private readonly Dictionary<String, bool> troofDictionary;

		private Stack scopeStack;

		private Dictionary<String, bool> tempDictionary;
		// Regex for implictly determining the type of a literal
		private readonly Regex NUMBR_REGEX = new Regex (@"^-?\d+$");
		private readonly Regex NUMBAR_REGEX = new Regex(@"^(-?\d*\.\d+)$");
		private readonly Regex TROOF_REGEX = new Regex ("^(WIN)|(FAIL)$");
		private readonly Regex YARN_REGEX = new Regex("^[^\"]*$"); 
					// Yarn's quotation marks are already delimited after performing LexicalAnalyzer


		// Similar to IT; will store all values 
		private Variable immediate;
		// Constructor - requires output from LexicalAnalyzer
		public Parser (ArrayList tokensArrayList)
		{
			// Output from lexical analyzer
			this.tokensArrayList = tokensArrayList;
			// Uncomment me to check output from lexical analyzer
			//enumerateReceivedTokens ();

			// HAI is always at index 1 ; Index 0 contains statement delimiter
			this.currentPosition = 1;

			// Instantiate immediate variable
			this.immediate = new Variable ("immediate", "Noob", "");

			// Instantiate variablesDictionary
			this.variablesDictionary = new Dictionary<String, Variable> ();
			this.variablesDictionary.Add("IT", new Variable("IT", "Noob", ""));

			// Instantiate troofDictionary and its contents
			this.troofDictionary = new Dictionary<String, bool> ();
			this.troofDictionary.Add ("WIN", true);
			this.troofDictionary.Add ("FAIL", false);

			this.tempDictionary = new Dictionary<String, bool>();
			this.scopeStack = new Stack();

			// Reflect to the symbol table
			MainClass.win.updateChangesOnSymbolTable (this.variablesDictionary);
		}
			
		private void enumerateReceivedTokens(){
			/* --------------------------------------------------------------
			 *  .getKeyword() -> returns the type of the lexeme
			 *  .getLexeme() -> returns the lexeme itself
			 *  .getLineNumber() -> returns the lineNumber where it is found
			 * 							// for error checking
			 * -------------------------------------------------------------*/
			foreach (Token token in tokensArrayList){
				Console.WriteLine (token.getKeyword ());
				//Console.WriteLine(token.getLexeme ());
				//Console.WriteLine (token.getLineNumber ());
			}
		}

		private String checkLiteralType(String arg){
			if (NUMBR_REGEX.IsMatch (arg))
				return "Numbr";
			else if (NUMBAR_REGEX.IsMatch (arg))
				return "Numbar";
			else if (TROOF_REGEX.IsMatch (arg))
				return "Troof";
			else if (YARN_REGEX.IsMatch (arg))
				return "Yarn";
			else
				return "Noob";
		}

		public void addVariable(String varName, String varType, String varValue){
			/* --------------------------------------------------------------------
			 *  This function adds a certain variable to the variablesDictionary.
			 * -------------------------------------------------------------------*/
			variablesDictionary.Add(varName, new Variable(varName, varType, varValue));
			// Whenever a variable is added, symbol table is also updated
			MainClass.win.updateChangesOnSymbolTable (variablesDictionary);
		}

		private bool checkType(Keyword keyword){
			/* --------------------------------------------------------------------
			 *  This function checks whether the expected <keyword> is the same as
			 * 		one one currently pointed by currentPosition.
			 * -------------------------------------------------------------------*/
			if (currentPosition == tokensArrayList.Count)
				return false;
			Token a = (Token)tokensArrayList [currentPosition++];
			if (a.getKeyword () == keyword){
			return true;
		}
			else {
				return false;
			}
		}

		private String getVariableValueFromKey(String key){
			/* --------------------------------------------------------------------
			 *  This function returns the value of the variable.
			 * -------------------------------------------------------------------*/
			if (doesVariableExist (key)) return this.variablesDictionary [key].getVariableValue ();
			else Console.WriteLine ("You are accessing a non-existing variable name. Value cannot be derived");
			return "#undefined";
		}

		private string getVariableTypeFromKey(String key){
			/* --------------------------------------------------------------------
			 *  This function returns the type of the variable.
			 * -------------------------------------------------------------------*/
			if (doesVariableExist (key)) return this.variablesDictionary [key].getVariableType ();
			else Console.WriteLine ("You are accessing a non-existing variable name. Type cannot be derived.");
			return "#undefined";
		}
		private bool doesVariableExist(String key){
			/* --------------------------------------------------------------------
			 *  This function checks whether such variable exists or not.
			 * -------------------------------------------------------------------*/
			if (this.variablesDictionary.ContainsKey (key)) return true;
			else return false;
		}
		private void updateVariable(String varName, String varType, String varValue){
			/* --------------------------------------------------------------------
			 *  This function updates the attributes of the variable.
			 * -------------------------------------------------------------------*/
			this.variablesDictionary [varName].setVariableType (varType);
			this.variablesDictionary [varName].setVariableValue (varValue);
			// Whenever a variable is updated, symbol table is also updated
			MainClass.win.updateChangesOnSymbolTable (variablesDictionary);
		}

		private bool literal(){
			/* --------------------------------------------------------------------
			 *  This function is for checking if the token pointed by currentPosition
			 * 		is a literal. (an atom type of expression)
			 * -------------------------------------------------------------------*/
			int save = currentPosition;
			if ((currentPosition = save) == save & checkType (Keyword.NUMBR))
				return true;
			else if ((currentPosition = save) == save & checkType (Keyword.NUMBAR))
				return true;
			else if ((currentPosition = save) == save & checkType (Keyword.TROOF))
				return true;
			else if ((currentPosition = save) == save & checkType (Keyword.YARN))
				return true;
			else return false;
		}
		private bool linebreak(){
			/* --------------------------------------------------------------------
			 *  This function catches the linebreak. Used to denote epsilon of a statement.
			 * -------------------------------------------------------------------*/	
			if (currentPosition == tokensArrayList.Count) return false;
			Token a = (Token)tokensArrayList [currentPosition++];
			if (a.getKeyword () == Keyword.DELIMITER)
				return true;
			else
				return false;
		}
		public bool parseProgram(){
			/* --------------------------------------------------------------------
			 *  This function defines the structure of the program. 
			 * -------------------------------------------------------------------*/
			int save = currentPosition;
			if (((currentPosition = save) == save & checkType (Keyword.HAI) && plus_statement () && checkType (Keyword.KTHXBYE)) == false) {
				return false;
			} else if (currentPosition < tokensArrayList.Count)
				return true;
			else
				return true;
		}
			
		private bool evaluateExpression(int lineNumber){
			/* --------------------------------------------------------------------
			 *  This function evaluates an expression and stores it to the immediate
			 * 		variable.
			 * 		- supports nesting of expressions
			 * -------------------------------------------------------------------*/

			// Stack used to evaluate converted postfix expressions
			Stack arithmeticStack = new Stack ();

			// Variables to be used in parsing to decimal
			Decimal first;
			Decimal second;

			String tempFirst;
			String tempSecond;
			 /*----EQUIVALENCE TABLE----\
			 |  	"+" -> SUM OF       |
			 |  	"-" -> DIFF OF      |
			 |  	"*" -> PRODUKT OF   |
			 |  	"/" -> QUOSHUNT OF  |
			 |  	"%" -> MOD OF       |
			 |  	">" -> BIGGR OF     |
			 |  	"<" -> SMALLR OF    |
			 |  	"==" -> BOTH SAEM   |
			 |  	"!=" -> DIFFRINT    |
			 |		"&&" -> AND			|
			 |		"||" -> OR			|
			 |		"^"  -> XOR			|
			 |  	allOfFlag -> ALL OF |
			 |  	anyOfFlag -> ANY OF |
			 *-------------------------*/

			// Variable to be used in ALL OF and ANY OF operations
			String result = "";

			// Split the generated expression symbols by quotation marks
			String[] words = expressionString.Split (new char[]{ '\"' } );
			if (allOfFlag && anyOfFlag) {
				MainClass.win.updateMessagesOnConsole($"Semantic Error: Cannot use ANY OF and ALL OF in the same line at line {lineNumber}");
				return false;
			}
			for (int symbolCount = words.Length - 1; symbolCount >= 0; symbolCount--) {
				/* ---------------------------Algorithm---------------------------------
				 * 		1. split prefix notation-ed expressionString by quotation marks
				 * 		2. store it to an array of strings
				 * 		3. traverse from right to left -> converting to postfix notation
				 * 		4. use stack evaluation
				 * 			4.1 if operation found, pop two operands from the stack
				 * 					and push the result
				 * 			4.2 if non-operation found, push operand to stack
				 * 		Notes:
				 * 			Stack operations return an 'object' class. (Peek()/ Pop())
				 * 			Stack must be homogeneous (contains only Strings)
				 * 			For consistency, use "undefined" for String name parameter
				 * 		Suggestions:
				 * 			Stack should be composed of 'Variable' instances to check the
				 * 				type.
				 *---------------------------------------------------------------------*/
				if (words [symbolCount] == "+") {
					// The operands must be decimal or else generate a semantic error
					if (Decimal.TryParse (arithmeticStack.Pop ().ToString (), out first) && Decimal.TryParse (arithmeticStack.Pop ().ToString (), out second)) {
						// Push the result to the stack since it will be used again
						arithmeticStack.Push (first + second);
					} else {
						MainClass.win.updateMessagesOnConsole ($"Semantic Error: Invalid Operands at line {lineNumber}");
						return false;
					}
				} else if (words [symbolCount] == "-") {
					if (Decimal.TryParse (arithmeticStack.Pop ().ToString (), out first) && Decimal.TryParse (arithmeticStack.Pop ().ToString (), out second)) {
						arithmeticStack.Push (first - second);
					} else {
						MainClass.win.updateMessagesOnConsole ($"Semantic Error: Invalid Operands at line {lineNumber}");
						return false;
					}
				} else if (words [symbolCount] == "*") {
					if (Decimal.TryParse (arithmeticStack.Pop ().ToString (), out first) && Decimal.TryParse (arithmeticStack.Pop ().ToString (), out second)) {
						arithmeticStack.Push (first * second);
					} else {
						MainClass.win.updateMessagesOnConsole ($"Semantic Error: Invalid Operands at line {lineNumber}");
						return false;
					}
				} else if (words [symbolCount] == "/") {
					if (Decimal.TryParse (arithmeticStack.Pop ().ToString (), out first) && Decimal.TryParse (arithmeticStack.Pop ().ToString (), out second)) {
						arithmeticStack.Push (first / second);
					} else {
						MainClass.win.updateMessagesOnConsole ($"Semantic Error: Invalid Operands at line {lineNumber}");
						return false;
					}
				} else if (words [symbolCount] == "%") {
					if (Decimal.TryParse (arithmeticStack.Pop ().ToString (), out first) && Decimal.TryParse (arithmeticStack.Pop ().ToString (), out second)) {
						arithmeticStack.Push (first % second);
					} else {
						MainClass.win.updateMessagesOnConsole ($"Semantic Error: Invalid Operands at line {lineNumber}");
						return false;
					}
				} else if (words [symbolCount] == ">") {
					if (Decimal.TryParse (arithmeticStack.Pop ().ToString (), out first) && Decimal.TryParse (arithmeticStack.Pop ().ToString (), out second)) {
						arithmeticStack.Push (first > second ? first : second);
					} else {
						MainClass.win.updateMessagesOnConsole ($"Semantic Error: Invalid Operands at line {lineNumber}");
						return false;
					}
				} else if (words [symbolCount] == "<") {
					if (Decimal.TryParse (arithmeticStack.Pop ().ToString (), out first) && Decimal.TryParse (arithmeticStack.Pop ().ToString (), out second)) {
						arithmeticStack.Push (first < second ? first : second);
					} else {
						MainClass.win.updateMessagesOnConsole ($"Semantic Error: Invalid Operands at line {lineNumber}");
						return false;
					}
				} else if (words [symbolCount] == "||") {
					tempFirst = arithmeticStack.Pop ().ToString ();
					tempSecond = arithmeticStack.Pop ().ToString ();
					if (this.troofDictionary.ContainsKey (tempFirst) && this.troofDictionary.ContainsKey (tempSecond)) {
						if ((this.troofDictionary [tempFirst] || this.troofDictionary [tempSecond]) == true) arithmeticStack.Push ("WIN");
						else arithmeticStack.Push ("FAIL");
					} 
					else {
						MainClass.win.updateMessagesOnConsole ($"Semantic Error: Invalid Operands at line {lineNumber}");
						return false;
					}
				} else if (words [symbolCount] == "^") {
					tempFirst = arithmeticStack.Pop ().ToString ();
					tempSecond = arithmeticStack.Pop ().ToString ();
					if (this.troofDictionary.ContainsKey (tempFirst) && this.troofDictionary.ContainsKey (tempSecond)) {
						if ((this.troofDictionary [tempFirst] ^ this.troofDictionary [tempSecond]) == true) arithmeticStack.Push ("WIN");
						else arithmeticStack.Push ("FAIL");
					} 
					else {
						MainClass.win.updateMessagesOnConsole ($"Semantic Error: Invalid Operands at line {lineNumber}");
						return false;
					}
				} else if (words [symbolCount] == "&&") {
					tempFirst = arithmeticStack.Pop ().ToString ();
					tempSecond = arithmeticStack.Pop ().ToString ();
					if (this.troofDictionary.ContainsKey (tempFirst) && this.troofDictionary.ContainsKey (tempSecond)) {
						if ((this.troofDictionary [tempFirst] && this.troofDictionary [tempSecond]) == true) arithmeticStack.Push ("WIN");
						else arithmeticStack.Push ("FAIL");
					} 
					else {
						MainClass.win.updateMessagesOnConsole ($"Semantic Error: Invalid Operands at line {lineNumber}");
						return false;
					}
				} else if (words [symbolCount] == "==") {
					tempFirst = arithmeticStack.Pop ().ToString ();
					tempSecond = arithmeticStack.Pop ().ToString ();
					arithmeticStack.Push((tempFirst == tempSecond) ? "WIN" : "FAIL");
				} else if (words [symbolCount] == "!=") {
					tempFirst = arithmeticStack.Pop ().ToString ();
					tempSecond = arithmeticStack.Pop ().ToString ();
					arithmeticStack.Push((tempFirst != tempSecond) ? "WIN" : "FAIL");
				} else if(words[symbolCount] == "!"){
					tempFirst = arithmeticStack.Pop().ToString();
					if(this.troofDictionary[tempFirst])
						arithmeticStack.Push("FAIL");
					else  if(!this.troofDictionary[tempFirst]){
						arithmeticStack.Push("WIN");
					}
					else{
						MainClass.win.updateMessagesOnConsole($"Semantic Error: Invalid Operands at line {lineNumber}");
						return false;
					}
				}

				else {
					arithmeticStack.Push(words[symbolCount]);			
				}
			}
			if (allOfFlag) {
				while (arithmeticStack.Count > 0) {
					if (!(this.troofDictionary [arithmeticStack.Pop ().ToString ()])) {
						// If encounted FAIL, use short-circuit evaluation
						// ... FAIL ... -> FAIL
						arithmeticStack.Clear ();
						arithmeticStack.Push ("FAIL");
						break;
					}
				}
			} 
			else if (anyOfFlag) {
				while (arithmeticStack.Count > 0) {
					if (this.troofDictionary [arithmeticStack.Pop ().ToString ()]) {
						// If encountered, WIN, use short-circuit evaluation
						// ... WIN ... -> WIN
						arithmeticStack.Clear ();
						arithmeticStack.Push("WIN");
						break;
					}
				}
			}
			else if(concatenationEntered){
				while(arithmeticStack.Count > 0){
					result += arithmeticStack.Pop().ToString();
				}
				arithmeticStack.Push(result);
			}

			// If stack is completely traversed, decide if WIN or FAIL
			if (arithmeticStack.Count == 0 && this.allOfFlag) arithmeticStack.Push ("WIN");
			else if(arithmeticStack.Count == 0 && this.anyOfFlag) arithmeticStack.Push("FAIL");

			if(arithmeticStack.Count == 0){
				// If stack does not contain result, it fails to evaluate the expression
				Console.WriteLine("Evaluation fails to continue. Something went wrong.");
				return false;
			}
			// Put to immediate variable
			saveToImmediate(checkLiteralType(arithmeticStack.Peek().ToString()), arithmeticStack.Pop().ToString());

			// Reset all variables used in evaluating expressions
			this.allOfFlag = false;
			this.anyOfFlag = false;
			expressionString = "";
			result = "";
			return true;
		}

		private void saveToImmediate(String varType, String varValue){
			/* --------------------------------------------------------------------
			 *  This function saves all the result to immediate variable.
			 * -------------------------------------------------------------------*/
			this.immediate.setVariableType(varType);
			this.immediate.setVariableValue(varValue);
		}
			
		private bool plus_statement(){
			/* --------------------------------------------------------------------
			 *  This function allows multiple statements to be interpreted.
			 *	Also implements (*) or (0 or more instances) or statements
			 * -------------------------------------------------------------------*/
			int save = currentPosition;
			if((currentPosition = save) == save & statement()){
				return true;
			}
			else if((currentPosition = save) == save & linebreak() && (this.switchEntered || elseEntered) && checkType(Keyword.OIC)){
				if (!switchEntered) {
					Console.WriteLine ("here");
					if (scopeStack.Count == 0)
						Console.WriteLine ("HEEEEEEELP");
					else {
						State currentState = (State)scopeStack.Pop ();
						this.skip = currentState.getValueFromState ("skip");
						this.elseEntered = currentState.getValueFromState ("elseEntered");
						this.ifEntered = currentState.getValueFromState ("ifEntered");
						this.matched = currentState.getValueFromState ("matched");

					}
				} else {
					this.switchEntered = false;
					this.omgBlockEntered = false;
					this.skip = false;
					this.gtfoed = false;
					this.flow = false;
					this.matched = false;
					this.ifEntered = false;
					this.elseEntered = false;
				}
				return true;
			}	else if((currentPosition = save) == save & linebreak() && this.switchEntered && checkType(Keyword.OMG) && literal()){
					Token a = (Token) tokensArrayList[currentPosition - 1]; 	
					if(!gtfoed && a.getLexeme() == getVariableValueFromKey("IT")){
						this.skip = false;
						this.flow = true;
						this.matched = true;
					}
					else if(this.flow) this.skip = false;
					else{
						this.skip = true;
						this.matched = false;
					}
					if(statement()){
						return true;
					}
				return false;
			} 	else if ((currentPosition = save) == save & linebreak() && this.omgBlockEntered && checkType(Keyword.OMGWTF)){
				if(!gtfoed) this.skip = false;
				if(plus_statement()){
					return true;
				}
				return true;
			} else if ((currentPosition = save) == save & linebreak() && this.ifEntered && checkType(Keyword.MEBBE)) {
				skip = false;
				suppressNewLine = false;
				if (getVariableValueFromKey("IT").ToString() == "WIN") {
					skip = true;
				}
				if (expr() && !skip) {
					if (!evaluateExpression(((Token)tokensArrayList[currentPosition - 1]).getLineNumber())) return false;
					updateVariable("IT", immediate.getVariableType(), immediate.getVariableValue());
					if (getVariableValueFromKey("IT").ToString() == "FAIL") {
						skip = true;
					}
					else {// MEBBE is evaluated true
						this.matched = true;
						skip = false;
					}
				}
				if (statement()) {
					return true;
				}
				else return false;
			}
			else if((currentPosition = save) == save & linebreak() && this.ifEntered && checkType(Keyword.NO_WAI)){
				this.elseEntered = true;
				State previousState = ((State)scopeStack.Peek ());
				if (!this.matched && (previousState.getValueFromState ("matched") || scopeStack.Count == 1)) {
					this.matched = true;
					this.skip = false;
				} else {
					this.skip = true;
					//this.matched = false;
				}
				if(statement()){
					return true;
				}
				else return false;
			}
			else if((currentPosition = save) == save & linebreak()){
				return true;
			}  
			else{
				return false;
			}
		}

		private bool statement(){
			/* --------------------------------------------------------------------
			 *  This function contains all the possible statements that can be
			 * 		interpreted.
			 * 	Also implements (+) or (One or more instances) of statements
			 * 			// Cannot be zero statement
			* -------------------------------------------------------------------*/
			int save = currentPosition;
			if ((currentPosition = save) == save & linebreak () && print () && plus_statement ()) { 
				return true;
			} else if ((currentPosition = save) == save & linebreak () && switchcase () && plus_statement()) {
				return true;
			} else if ((currentPosition = save) == save & linebreak () && arithmetic ()) {
				// Evaluate expression returns a boolean value: if operands are correct: it will be true, else false
				if(!skip){
					if (!evaluateExpression (((Token)tokensArrayList [currentPosition-1]).getLineNumber ()))
						return false; // Halt if operands are incorrect
						updateVariable("IT", immediate.getVariableType(), immediate.getVariableValue());
				}
				if (plus_statement ()) {
					return true;
				} else
					return false;
			} else if ((currentPosition = save) == save & linebreak () && booleanOperations ()){
				if(!skip){
					if (!evaluateExpression (((Token)tokensArrayList [currentPosition-1]).getLineNumber ())) return false;
					updateVariable("IT", immediate.getVariableType(), immediate.getVariableValue());
				}
				if(plus_statement ()) {
					return true;
				}
				else{
					return false;
				}
			} else if ((currentPosition = save) == save & linebreak () && declaration ()){
				if(plus_statement ()) {
					return true;
				}
				else{
					return false;
				}
			} else if ((currentPosition = save) == save & linebreak () && assignment () && plus_statement ()) {
				return true;	
			} else if ((currentPosition = save) == save & linebreak () && kyahpeminput () && plus_statement ()) {
				return true;	
			} else if ((currentPosition = save) == save & linebreak () && if_statement () && plus_statement ()) {
				return true;	
			} else if ((currentPosition = save) == save & linebreak () && concatenation ()) {
				if (!evaluateExpression (((Token)tokensArrayList [currentPosition-1]).getLineNumber ())) return false;
				updateVariable("IT", immediate.getVariableType(), immediate.getVariableValue());
				this.concatenationEntered = false;
				if (plus_statement ())
					return true;
				else
					return false;
			} else if((currentPosition = save) == save & linebreak() && this.omgBlockEntered && checkType(Keyword.GTFO)){
				if(this.matched){
					this.gtfoed = true;
					this.skip = true;
				}
				this.flow = false;
				if(plus_statement()){
					return true;
				}
				return false;
			}
			else{ 
				currentPosition = save;
				Token a = (Token)tokensArrayList [currentPosition];
				return false;

			}
		}
		#region INPUT / OUTPUT 
		private bool print(){
			int save = currentPosition;
			this.printEntered = true;
			if ((currentPosition = save) == save & checkType (Keyword.VISIBLE) && checkType(Keyword.VARIABLE)) {
				if(!skip){
					Token a = (Token)tokensArrayList [currentPosition - 1];
					if (this.variablesDictionary.ContainsKey (a.getLexeme ().ToString ())) {
						MainClass.win.printOnConsole (this.variablesDictionary [a.getLexeme ().ToString ()].getVariableValue ());
					} 
					else {
						MainClass.win.updateMessagesOnConsole ($"Semantic Error: Variable not found at line {a.getLineNumber()}");
						return false;
					}
					if(this.variablesDictionary[a.getLexeme().ToString()].getVariableType() == "Noob"){
						MainClass.win.updateMessagesOnConsole($"Semantic Error: Printing a NOOB type variable at line {a.getLineNumber()}");
						return false;
					}
				}
				if (((Token) (tokensArrayList[save])).getLexeme() == "VISIBLE!") suppressNewLine = true;
				plus_variables ();
				return true;
			}
			else if ((currentPosition = save) == save & checkType (Keyword.VISIBLE) && expr()) {
				if (evaluateExpression (((Token)tokensArrayList [currentPosition-1]).getLineNumber ())) {
					if(!skip){
						if (((Token) (tokensArrayList[save])).getLexeme() == "VISIBLE!") suppressNewLine = true;
						MainClass.win.printOnConsole (immediate.getVariableValue ());
						plus_variables();
						return true;
						}
					else{
						plus_variables();
						return true;
					}
				}
				else{
					return false;
				}
			}
			else if ((currentPosition = save) == save & checkType (Keyword.VISIBLE) && concatenation()) {
				if(evaluateExpression(((Token) tokensArrayList[currentPosition-1]).getLineNumber())){
					if (!skip) {
						if (((Token)(tokensArrayList [save])).getLexeme () == "VISIBLE!") {
							suppressNewLine = true;
							MainClass.win.printOnConsole (immediate.getVariableValue ());
						}
						else MainClass.win.printOnConsole (immediate.getVariableValue () + "\n");
						suppressNewLine = false;
					}
				}
				return true;
			}
			else return false;
		}
		
		private bool plus_variables(){
			/* --------------------------------------------------------------------
			 *  This function implements multiple variables/yarn in a line.
			 * 		Is necessary for VISIBLE and SMOOSH statements.
			 * 	Suggestion: 
			 * 		repl Lolcode Interpreter also allows AN keyword.
			 * -------------------------------------------------------------------*/
			int save = currentPosition;
			Token a = (Token)tokensArrayList [currentPosition];
			if ((currentPosition = save) == save & checkType (Keyword.VARIABLE)) {
				if(!skip){
					if (this.printEntered && this.variablesDictionary.ContainsKey (a.getLexeme ().ToString ())) {
						MainClass.win.printOnConsole (this.variablesDictionary [a.getLexeme ().ToString ()].getVariableValue ());
					} 
					else {
						MainClass.win.updateMessagesOnConsole ("Semantic Error: Variable not found");
						return false;
					}
					if(this.variablesDictionary[a.getLexeme().ToString()].getVariableType() == "Noob"){
						MainClass.win.updateMessagesOnConsole($"Semantic Error: Printing a NOOB type variable at line {a.getLineNumber()}");
						return false;
					}
				}
				plus_variables ();
				return true;
			}
			else if ((currentPosition = save) == save & expr()) {
				if (evaluateExpression (((Token)tokensArrayList [currentPosition-1]).getLineNumber ())) {
					if(!skip){
						MainClass.win.printOnConsole (immediate.getVariableValue ());
						plus_variables();
						return true;
					}
					else{
						plus_variables();
						return true;
					}
				}
				else{
					return false;
				}
			}
			else if ((currentPosition = save) == save & linebreak ()) {
				currentPosition -= 1;
				this.printEntered = false;
				if((this.flow || !this.skip) && !suppressNewLine) MainClass.win.printOnConsole("\n");
				this.suppressNewLine = false;

				return true;
			} 
			else {
				return false;
			}
		}

		private bool kyahpeminput(){
			/* --------------------------------------------------------------------
			 *  This function uses another class, InputPromptDialog.
			 * 		Once "OK" is pressed, it will copy the value entered in the entry
			 * 			to the receivedText attribute.
			 * 	Suggestion: Delete exit button in Dialog since it is required for 
			 * 		the program.
			 * 			- Pardon the name; 
			 * -------------------------------------------------------------------*/
			int save = currentPosition;

			if((currentPosition = save) == save & checkType(Keyword.GIMMEH)){
				if(checkType(Keyword.VARIABLE)){
					Token previousToken = (Token) tokensArrayList [currentPosition - 1];
					if(doesVariableExist(previousToken.getLexeme())){
						InputPromptDialog dialog = new InputPromptDialog();
						dialog.Run();
						updateVariable(previousToken.getLexeme(), checkLiteralType(dialog.getReceivedText()), dialog.getReceivedText());
						return true;
					}
					else{
						MainClass.win.updateMessagesOnConsole($"Semantic Error: At line {previousToken.getLineNumber()}. Undeclared variable found.");
						return false;
					}
				}
				else{
					Token a = (Token)tokensArrayList [currentPosition-1];
					if (a.getLexeme () == "\n") a = (Token)tokensArrayList [currentPosition-2];
					MainClass.win.updateMessagesOnConsole ($"You have an error in your LOLCODE Syntax near {a.getLexeme()} at line {a.getLineNumber()}. Expected variable.");
					return false;
				}
			}
			else return false; 
		}

		#endregion
		private bool expr(){
			/* --------------------------------------------------------------------
			 *  This function allows nesting of expressions.
			 * 		Type of expressions used:
			 * 			1. arithmetic expression (returns numbr/numbar)
			 * 			2. boolean expressions (returns win/fail)
			 * 			3. variable (gets the literal mapped to variable)
			 * 			4. literal (numbr/numbar/yarn/troof lexeme)
			 * 	Also responsible for adding to the expressionString to be evaluated
			 * 		depending on use.
			 * -------------------------------------------------------------------*/
			Token temp;
			int save = currentPosition;
			if ((currentPosition = save) == save & arithmetic ()) {
				return true;
			} else if ((currentPosition = save) == save & booleanOperations ()) {
				return true;
			} else if ((currentPosition = save) == save & literal ()) {
				temp = (Token)tokensArrayList [currentPosition - 1];
				if(!skip){
					expressionString += $"{temp.getLexeme()}\"";
				}
				//Console.WriteLine (expressionString);
				return true;
			} else if ((currentPosition = save) == save & checkType (Keyword.VARIABLE)) {
				temp = (Token)tokensArrayList [currentPosition - 1];
				if (doesVariableExist (temp.getLexeme ())) {
					if(!skip){
						expressionString += $"{getVariableValueFromKey (temp.getLexeme ())}\"";
					}
					return true;
				}
				else {
					MainClass.win.updateMessagesOnConsole($"Semantic Error: Variable does not exist at {temp.getLineNumber()}");
					return false;
				}
			} else if ((currentPosition = save) == save & linebreak ()) {
				return false;
			}
			else return false;
		}
#region ARITHMETIC OPERATIONS
		private bool arithmetic(){
			int save = currentPosition;
			if ((currentPosition = save) == save & add ()) {
				return true;
			} 
			else if ((currentPosition = save) == save & subtract ()) {
				return true;
			}
			else if ((currentPosition = save) == save & multiply ()) {
				return true;
			}
			else if ((currentPosition = save) == save & divide ()) {
				return true;
			}
			else if ((currentPosition = save) == save & modulo ()) {
				return true;
			}
			else if ((currentPosition = save) == save & greaterThan ()) {
				return true;
			}
			else if ((currentPosition = save) == save & lessThan ()) {
				return true;
			}
			else{
				return false;
			}
		}

		private bool add(){
			int save = currentPosition;
			if ((currentPosition = save) == save & checkType (Keyword.SUM_OF)) {
				if(!skip){
					expressionString += "+\"";
				}
				if (expr ()) {
					if (checkType (Keyword.AN)) {
						if (expr ()) {
							return true;
						} 
						else {
							Token a = (Token)tokensArrayList [currentPosition-1];
							if (a.getLexeme () == "\n") a = (Token)tokensArrayList [currentPosition-2];
							MainClass.win.updateMessagesOnConsole ($"You have an error in your LOLCODE Syntax near {a.getLexeme()} at line {a.getLineNumber()}. Expected expression.");
						}
					}
					else { // Missing AN 
						Token a = (Token)tokensArrayList [currentPosition-1];
						if (a.getLexeme () == "\n") a = (Token)tokensArrayList [currentPosition-2];
						MainClass.win.updateMessagesOnConsole ($"You have an error in your LOLCODE Syntax near {a.getLexeme()} at line {a.getLineNumber()}. Expected AN");
					}
				} 
				else { // Missing Expression
					Token a = (Token)tokensArrayList [currentPosition-1];
					if (a.getLexeme () == "\n") a = (Token)tokensArrayList [currentPosition-2];
					MainClass.win.updateMessagesOnConsole ($"You have an error in your LOLCODE Syntax near {a.getLexeme()} at line {a.getLineNumber()}. Expected expression.");
				}
			}
			return false;
		}

		private bool subtract(){
			int save = currentPosition;
			if ((currentPosition = save) == save & checkType (Keyword.DIFF_OF)) {
				if(!skip){
					expressionString += "-\"";
				}
				if (expr ()) {
					if (checkType (Keyword.AN)) {
						if (expr ()) {
							return true;
						} 
						else {
							Token a = (Token)tokensArrayList [currentPosition-1];
							if (a.getLexeme () == "\n") a = (Token)tokensArrayList [currentPosition-2];
							MainClass.win.updateMessagesOnConsole ($"You have an error in your LOLCODE Syntax near {a.getLexeme()} at line {a.getLineNumber()}. Expected expression.");
						}
					}
					else { // Missing AN 
						Token a = (Token)tokensArrayList [currentPosition-1];
						if (a.getLexeme () == "\n") a = (Token)tokensArrayList [currentPosition-2];
						MainClass.win.updateMessagesOnConsole ($"You have an error in your LOLCODE Syntax near {a.getLexeme()} at line {a.getLineNumber()}. Expected AN");
					}
				} 
				else { // Missing Expression
					Token a = (Token)tokensArrayList [currentPosition-1];
					if (a.getLexeme () == "\n") a = (Token)tokensArrayList [currentPosition-2];
					MainClass.win.updateMessagesOnConsole ($"You have an error in your LOLCODE Syntax near {a.getLexeme()} at line {a.getLineNumber()}. Expected expression.");
				}
			}
			return false;
		}


		private bool multiply(){
			int save = currentPosition;
			if ((currentPosition = save) == save & checkType (Keyword.PRODUKT_OF)) {
				if(!skip){
					expressionString += "*\"";
				}
				if (expr ()) {
					if (checkType (Keyword.AN)) {
						if (expr ()) {
							return true;
						} 
						else {
							Token a = (Token)tokensArrayList [currentPosition-1];
							if (a.getLexeme () == "\n") a = (Token)tokensArrayList [currentPosition-2];
							MainClass.win.updateMessagesOnConsole ($"You have an error in your LOLCODE Syntax near {a.getLexeme()} at line {a.getLineNumber()}. Expected expression.");
						}
					}
					else { // Missing AN 
						Token a = (Token)tokensArrayList [currentPosition-1];
						if (a.getLexeme () == "\n") a = (Token)tokensArrayList [currentPosition-2];
						MainClass.win.updateMessagesOnConsole ($"You have an error in your LOLCODE Syntax near {a.getLexeme()} at line {a.getLineNumber()}. Expected AN");
					}
				} 
				else { // Missing Expression
					Token a = (Token)tokensArrayList [currentPosition-1];
					if (a.getLexeme () == "\n") a = (Token)tokensArrayList [currentPosition-2];
					MainClass.win.updateMessagesOnConsole ($"You have an error in your LOLCODE Syntax near {a.getLexeme()} at line {a.getLineNumber()}. Expected expression.");
				}
			}
			return false;
		}

		private bool divide(){
			int save = currentPosition;
			if ((currentPosition = save) == save & checkType (Keyword.QUOSHUNT_OF)) {
				if(!skip){
					expressionString += "/\"";
				}
				if (expr ()) {
					if (checkType (Keyword.AN)) {
						if (expr ()) {
							return true;
						} 
						else {
							Token a = (Token)tokensArrayList [currentPosition-1];
							if (a.getLexeme () == "\n") a = (Token)tokensArrayList [currentPosition-2];
							MainClass.win.updateMessagesOnConsole ($"You have an error in your LOLCODE Syntax near {a.getLexeme()} at line {a.getLineNumber()}. Expected expression.");
							}
					}
					else { // Missing AN 
						Token a = (Token)tokensArrayList [currentPosition-1];
						if (a.getLexeme () == "\n") a = (Token)tokensArrayList [currentPosition-2];
						MainClass.win.updateMessagesOnConsole ($"You have an error in your LOLCODE Syntax near {a.getLexeme()} at line {a.getLineNumber()}. Expected AN");
					}
				} 
				else { // Missing Expression
					Token a = (Token)tokensArrayList [currentPosition-1];
					if (a.getLexeme () == "\n") a = (Token)tokensArrayList [currentPosition-2];
					MainClass.win.updateMessagesOnConsole ($"You have an error in your LOLCODE Syntax near {a.getLexeme()} at line {a.getLineNumber()}. Expected expression.");
				}
			}
			return false;
		}

		private bool modulo(){
			int save = currentPosition;
			if ((currentPosition = save) == save & checkType (Keyword.MOD_OF)) {
				if(!skip){
					expressionString += "%\"";
				}
				if (expr ()) {
					if (checkType (Keyword.AN)) {
						if (expr ()) {
							return true;
						} 
						else {
							Token a = (Token)tokensArrayList [currentPosition-1];
							if (a.getLexeme () == "\n") a = (Token)tokensArrayList [currentPosition-2];
							MainClass.win.updateMessagesOnConsole ($"You have an error in your LOLCODE Syntax near {a.getLexeme()} at line {a.getLineNumber()}. Expected expression.");
						}
					}
					else { // Missing AN 
						Token a = (Token)tokensArrayList [currentPosition-1];
						if (a.getLexeme () == "\n") a = (Token)tokensArrayList [currentPosition-2];
						MainClass.win.updateMessagesOnConsole ($"You have an error in your LOLCODE Syntax near {a.getLexeme()} at line {a.getLineNumber()}. Expected AN");
					}
				} 
				else { // Missing Expression
					Token a = (Token)tokensArrayList [currentPosition-1];
					if (a.getLexeme () == "\n") a = (Token)tokensArrayList [currentPosition-2];
					MainClass.win.updateMessagesOnConsole ($"You have an error in your LOLCODE Syntax near {a.getLexeme()} at line {a.getLineNumber()}. Expected expression.");
				}
			}
			return false;
		}

		private bool greaterThan(){
			int save = currentPosition;
			if ((currentPosition = save) == save & checkType (Keyword.BIGGR_OF)) {
				expressionString += ">\"";
				if (expr ()) {
					if (checkType (Keyword.AN)) {
						if (expr ()) {
							return true;
						} 
						else {
							Token a = (Token)tokensArrayList [currentPosition-1];
							if (a.getLexeme () == "\n") a = (Token)tokensArrayList [currentPosition-2];
							MainClass.win.updateMessagesOnConsole ($"You have an error in your LOLCODE Syntax near {a.getLexeme()} at line {a.getLineNumber()}. Expected expression.");
						}
					}
					else { // Missing AN 
						Token a = (Token)tokensArrayList [currentPosition-1];
						if (a.getLexeme () == "\n") a = (Token)tokensArrayList [currentPosition-2];
						MainClass.win.updateMessagesOnConsole ($"You have an error in your LOLCODE Syntax near {a.getLexeme()} at line {a.getLineNumber()}. Expected AN");
					}
				} 
				else { // Missing Expression
					Token a = (Token)tokensArrayList [currentPosition-1];
					if (a.getLexeme () == "\n") a = (Token)tokensArrayList [currentPosition-2];
					MainClass.win.updateMessagesOnConsole ($"You have an error in your LOLCODE Syntax near {a.getLexeme()} at line {a.getLineNumber()}. Expected expression.");
				}
			}
			return false;
		}
		private bool lessThan(){
			int save = currentPosition;
			if ((currentPosition = save) == save & checkType (Keyword.SMALLR_OF)) {
				if(!skip){
					expressionString += "<\"";
				}
				if (expr ()) {
					if (checkType (Keyword.AN)) {
						if (expr ()) {
							return true;
						} 
						else {
							Token a = (Token)tokensArrayList [currentPosition-1];
							if (a.getLexeme () == "\n") a = (Token)tokensArrayList [currentPosition-2];
							MainClass.win.updateMessagesOnConsole ($"You have an error in your LOLCODE Syntax near {a.getLexeme()} at line {a.getLineNumber()}. Expected expression.");
						}
					}
					else { // Missing AN 
						Token a = (Token)tokensArrayList [currentPosition-1];
						if (a.getLexeme () == "\n") a = (Token)tokensArrayList [currentPosition-2];
						MainClass.win.updateMessagesOnConsole ($"You have an error in your LOLCODE Syntax near {a.getLexeme()} at line {a.getLineNumber()}. Expected AN");
					}
				} 
				else { // Missing Expression
					Token a = (Token)tokensArrayList [currentPosition-1];
					if (a.getLexeme () == "\n") a = (Token)tokensArrayList [currentPosition-2];
					MainClass.win.updateMessagesOnConsole ($"You have an error in your LOLCODE Syntax near {a.getLexeme()} at line {a.getLineNumber()}. Expected expression.");
				}
			}
			return false;
		}
#endregion

#region BOOLEAN OPERATIONS 
		private bool booleanOperations(){
			int save = currentPosition;
			if ((currentPosition = save) == save & or ()) {
				return true;
			} 
			else if ((currentPosition = save) == save & xor ()) {
				return true;
			} 
			else if ((currentPosition = save) == save & and ()) {
				return true;
			} 
			else if ((currentPosition = save) == save & all ()) {
				return true;
			} 
			else if ((currentPosition = save) == save & any ()) {
				return true;
			}
			else if ((currentPosition = save) == save & equal ()) {
				return true;
			}
			else if ((currentPosition = save) == save & not_equal ()) {
				return true;
			}
			else if ((currentPosition = save) == save & not ()) {
				return true;
			}
			else{
				return false;
			}
		}
		private bool or(){
			int save = currentPosition;
			if ((currentPosition = save) == save & checkType (Keyword.EITHER_OF)) {
				if(!skip){
					expressionString += "||\"";
				}
				if (expr ()) {
					if (checkType (Keyword.AN)) {
						if (expr ()) {
							return true;
						} 
						else {
							Token a = (Token)tokensArrayList [currentPosition-1];
							if (a.getLexeme () == "\n") a = (Token)tokensArrayList [currentPosition-2];
							MainClass.win.updateMessagesOnConsole ($"You have an error in your LOLCODE Syntax near {a.getLexeme()} at line {a.getLineNumber()}. Expected expression.");
						}
					}
					else { // Missing AN 
						Token a = (Token)tokensArrayList [currentPosition-1];
						if (a.getLexeme () == "\n") a = (Token)tokensArrayList [currentPosition-2];
						MainClass.win.updateMessagesOnConsole ($"You have an error in your LOLCODE Syntax near {a.getLexeme()} at line {a.getLineNumber()}. Expected AN");
					}
				} 
				else { // Missing Expression
					Token a = (Token)tokensArrayList [currentPosition-1];
					if (a.getLexeme () == "\n") a = (Token)tokensArrayList [currentPosition-2];
					MainClass.win.updateMessagesOnConsole ($"You have an error in your LOLCODE Syntax near {a.getLexeme()} at line {a.getLineNumber()}. Expected expression.");
				}
			}
			return false;
		}


		private bool xor(){
			int save = currentPosition;
			if ((currentPosition = save) == save & checkType (Keyword.WON_OF)) {
				if(!skip){
					expressionString += "^\"";
				}
				if (expr ()) {
					if (checkType (Keyword.AN)) {
						if (expr ()) {
							return true;
						} 
						else {
							Token a = (Token)tokensArrayList [currentPosition-1];
							if (a.getLexeme () == "\n") a = (Token)tokensArrayList [currentPosition-2];
							MainClass.win.updateMessagesOnConsole ($"You have an error in your LOLCODE Syntax near {a.getLexeme()} at line {a.getLineNumber()}. Expected expression.");
						}
					}
					else { // Missing AN 
						Token a = (Token)tokensArrayList [currentPosition-1];
						if (a.getLexeme () == "\n") a = (Token)tokensArrayList [currentPosition-2];
						MainClass.win.updateMessagesOnConsole ($"You have an error in your LOLCODE Syntax near {a.getLexeme()} at line {a.getLineNumber()}. Expected AN");
					}
				} 
				else { // Missing Expression
					Token a = (Token)tokensArrayList [currentPosition-1];
					if (a.getLexeme () == "\n") a = (Token)tokensArrayList [currentPosition-2];
					MainClass.win.updateMessagesOnConsole ($"You have an error in your LOLCODE Syntax near {a.getLexeme()} at line {a.getLineNumber()}. Expected expression.");
				}
			}
			return false;
		}

		private bool and(){
			int save = currentPosition;
			if ((currentPosition = save) == save & checkType (Keyword.BOTH_OF)) {
				if(!skip){
					expressionString += "&&\"";
				}
				if (expr ()) {
					if (checkType (Keyword.AN)) {
						if (expr ()) {
							return true;
						} 
						else {
							Token a = (Token)tokensArrayList [currentPosition-1];
							if (a.getLexeme () == "\n") a = (Token)tokensArrayList [currentPosition-2];
							MainClass.win.updateMessagesOnConsole ($"You have an error in your LOLCODE Syntax near {a.getLexeme()} at line {a.getLineNumber()}. Expected expression.");
						}
					}
					else { // Missing AN 
						Token a = (Token)tokensArrayList [currentPosition-1];
						if (a.getLexeme () == "\n") a = (Token)tokensArrayList [currentPosition-2];
						MainClass.win.updateMessagesOnConsole ($"You have an error in your LOLCODE Syntax near {a.getLexeme()} at line {a.getLineNumber()}. Expected AN");
					}
				} 
				else { // Missing Expression
					Token a = (Token)tokensArrayList [currentPosition-1];
					if (a.getLexeme () == "\n") a = (Token)tokensArrayList [currentPosition-2];
					MainClass.win.updateMessagesOnConsole ($"You have an error in your LOLCODE Syntax near {a.getLexeme()} at line {a.getLineNumber()}. Expected expression.");
				}
			}
			return false;
		}


		private bool all(){
			/* --------------------------------------------------------------------
			 *  This function sets the anyOfFlag -> a substitute for symbol for n-arity.
			 * -------------------------------------------------------------------*/
			int save = currentPosition;
			if ((currentPosition = save) == save & checkType (Keyword.ALL_OF)){ 
				if(expr()){
					this.allOfFlag = true;
					if(plus_expression()){
						return true;
					}
					return false;
				}
				MainClass.win.updateMessagesOnConsole ($"Semantic Error: No operands found.");
				return false;
			} 
			else {
				return false;
			}
		}

		private bool plus_expression(){
			/* --------------------------------------------------------------------
			 *  This function allows n-arity expressions to be used by ALL OF, 
			 * 		ANY OF, SMOOSH
			 * -------------------------------------------------------------------*/
			int save = currentPosition;
			if ((currentPosition = save) == (save) && checkType (Keyword.MKAY)) {
				//evaluateExpression (((Token)
				return true;
			}
			else if ((currentPosition = save) == save & checkType (Keyword.AN)){
				
				if (expr ()) {
					if (plus_expression ()) {
						return true;
					}
					return false;
				} 
				return false;
			} 
			else {
				return false;
			}

		}


		private bool any(){
			/* --------------------------------------------------------------------
			 *  This function sets the anyOfFlag -> a substitute for symbol for n-arity
			 * 		to be used in evaluateExpression()
			 * -------------------------------------------------------------------*/
			int save = currentPosition;
			if ((currentPosition = save) == save & checkType (Keyword.ANY_OF)){ 
				if(expr()){
					this.anyOfFlag = true;
					if(plus_expression()){
						return true;
					}
					return false;
				}
				MainClass.win.updateMessagesOnConsole ($"Syntax Error: No operands found.");
				return false;
			} 
			else {
				return false;
			}
		}

		private bool equal(){
			int save = currentPosition;
			if ((currentPosition = save) == save & checkType (Keyword.BOTH_SAEM)) {
				if(!skip){
					expressionString += "==\"";
				}
				if (expr ()) {
					if (checkType (Keyword.AN)) {
						if (expr ()) {
							return true;
						} 
						else {
							Token a = (Token)tokensArrayList [currentPosition-1];
							if (a.getLexeme () == "\n") a = (Token)tokensArrayList [currentPosition-2];
							MainClass.win.updateMessagesOnConsole ($"You have an error in your LOLCODE Syntax near {a.getLexeme()} at line {a.getLineNumber()}. Expected expression.");
						}
					}
					else { // Missing AN 
						Token a = (Token)tokensArrayList [currentPosition-1];
						if (a.getLexeme () == "\n") a = (Token)tokensArrayList [currentPosition-2];
						MainClass.win.updateMessagesOnConsole ($"You have an error in your LOLCODE Syntax near {a.getLexeme()} at line {a.getLineNumber()}. Expected AN");
					}
				} 
				else { // Missing Expression
					Token a = (Token)tokensArrayList [currentPosition-1];
					if (a.getLexeme () == "\n") a = (Token)tokensArrayList [currentPosition-2];
					MainClass.win.updateMessagesOnConsole ($"You have an error in your LOLCODE Syntax near {a.getLexeme()} at line {a.getLineNumber()}. Expected expression.");
				}
			}
			return false;
		}

		private bool not_equal(){
			int save = currentPosition;
			if ((currentPosition = save) == save & checkType (Keyword.DIFFRINT)) {
				if(!skip){
					expressionString += "!=\"";
				}
				if (expr ()) {
					if (checkType (Keyword.AN)) {
						if (expr ()) {
							return true;
						} 
						else {
							Token a = (Token)tokensArrayList [currentPosition-1];
							if (a.getLexeme () == "\n") a = (Token)tokensArrayList [currentPosition-2];
							MainClass.win.updateMessagesOnConsole ($"You have an error in your LOLCODE Syntax near {a.getLexeme()} at line {a.getLineNumber()}. Expected expression.");
						}
					}
					else { // Missing AN 
						Token a = (Token)tokensArrayList [currentPosition-1];
						if (a.getLexeme () == "\n") a = (Token)tokensArrayList [currentPosition-2];
						MainClass.win.updateMessagesOnConsole ($"You have an error in your LOLCODE Syntax near {a.getLexeme()} at line {a.getLineNumber()}. Expected AN");
					}
				} 
				else { // Missing Expression
					Token a = (Token)tokensArrayList [currentPosition-1];
					if (a.getLexeme () == "\n") a = (Token)tokensArrayList [currentPosition-2];
					MainClass.win.updateMessagesOnConsole ($"You have an error in your LOLCODE Syntax near {a.getLexeme()} at line {a.getLineNumber()}. Expected expression.");
				}
			}
			return false;
		}

		private bool not(){
			int save = currentPosition;
			if ((currentPosition = save) == save & checkType (Keyword.NOT)){
				if(!skip){
					expressionString += "!\"";
				}
				if(expr()) {
					return true;
				}
				else{
					Token a = (Token)tokensArrayList [currentPosition-1];
					if (a.getLexeme () == "\n") a = (Token)tokensArrayList [currentPosition-2];
					MainClass.win.updateMessagesOnConsole ($"You have an error in your LOLCODE Syntax near {a.getLexeme()} at line {a.getLineNumber()}. Expected expression.");
					return false;
				}
			} 
			else {
				return false;
			}
		}
#endregion
		#region SWITCH CASE STATEMENTS
		private bool switchcase(){
			/* --------------------------------------------------------------------
		 	 *  WTF? -> switchEntered
		 	 * 		OMG <literal> -> omgEntered
		 	 * 			<statement> <plus_statement> -> omgEntered must be true
		 	 * 		[OMGWTF] -> omgEntered must be true
		 	 * 	OIC -> reset all flags
			 *  This function implements switch-case block. 
			 * 		Flags used:	
			 * 			flow -> allow proceeding to another case
			 * 			matched -> already matched a case
			 * 			gtfoed -> matched case has GTFO
			 * -------------------------------------------------------------------*/
			int save = currentPosition;
			if ((currentPosition = save) == save & checkType (Keyword.WTF) && linebreak()){ 
				this.switchEntered = true;
				if (omg_statement ()) {
					return true;
				}
				return false;
			}
			else {
				return false;
			}
		}

		private bool omg_statement(){
			/* --------------------------------------------------------------------
			 *  This function implements is for the OMG <literal>
			 * 		-> will proceed to the statement (+)
			 * -------------------------------------------------------------------*/
			int save = currentPosition;
			if ((currentPosition = save) == save & checkType (Keyword.OMG) && literal ()){
				this.omgBlockEntered = true;
				Token a = (Token) tokensArrayList[currentPosition - 1];
				if(!gtfoed && a.getLexeme() == getVariableValueFromKey("IT")){
						
						this.skip = false;
						this.flow = true;
						this.matched = true;
						Console.WriteLine(getVariableValueFromKey("IT"));
				}
				else if(this.flow) this.skip = false;
				else{
					this.skip = true;
					this.matched = false;
				}
				if(statement()){
					return true;
				}
				return false;
			}
			else{
				return false;
			}
		}


		#endregion
		#region VARIABLE DECLARATION AND ASSIGNMENT
		private bool declaration(){
		/* --------------------------------------------------------------------
		 * I HAS A <variable> ITZ <expr> is a subset of I HAS A <variable>
		 * <variable> must not be existing in the dictionary
		 * If existing, provide proper error messages. + error detection
		 * -------------------------------------------------------------------*/
			int save = currentPosition;

			if((currentPosition = save) == save & checkType (Keyword.I_HAS_A)){
				if(checkType(Keyword.VARIABLE)){
					Token temp = (Token) tokensArrayList[currentPosition-1];
					if(doesVariableExist(temp.getLexeme())){
						if(temp.getLexeme() == "IT"){
							MainClass.win.updateMessagesOnConsole($"(Semantic Error: Cannot declare special variable IT at line {temp.getLineNumber()}");
							return false;
						}
						MainClass.win.updateMessagesOnConsole($"Semantic Error: Variable name already exists at line {temp.getLineNumber()}");
						return false;
					}
					else{
						if(!skip){
							this.addVariable(temp.getLexeme(), "Noob", "");
							MainClass.win.updateChangesOnSymbolTable (variablesDictionary);
						}
						if(checkType(Keyword.ITZ)){
							if(expr()){
								// Copy value and type of IT since the result of expr is stored in this var
								if(!skip){
									evaluateExpression(temp.getLineNumber());
									this.variablesDictionary[temp.getLexeme()].setVariableValue(immediate.getVariableValue());
									this.variablesDictionary[temp.getLexeme()].setVariableType(immediate.getVariableType());
									MainClass.win.updateChangesOnSymbolTable (variablesDictionary);
								}
								return true;
							}
							else{
								return false;
							}
						}
						else{
							if((currentPosition = save) == save & checkType(Keyword.I_HAS_A)){
								if(checkType(Keyword.VARIABLE)){
									return true;
								}
								return false;
							}
							return false;
						}
					}
				}
				else{
					Token a = (Token)tokensArrayList [currentPosition-1];
					if (a.getLexeme () == "\n") a = (Token)tokensArrayList [currentPosition-2];
					MainClass.win.updateMessagesOnConsole ($"You have an error in your LOLCODE Syntax near {a.getLexeme()} at line {a.getLineNumber()}. Expected variable.");
					return false;

				}
			}
			else return false;

		}
		private bool assignment(){
			/* --------------------------------------------------------------------
			 * 	<variable> R <value>
			 *  This function assigns a new value to the variable
			 * 		* <variable> must exist in the dictionary
			 * 		* allow expression in <value>
			 * -------------------------------------------------------------------*/
			int save = currentPosition;

			if ((currentPosition = save) == save & checkType (Keyword.VARIABLE)){
				Token temp = (Token) tokensArrayList[currentPosition-1];
				if(doesVariableExist(temp.getLexeme())){
					if(checkType(Keyword.R)){
						if(expr()){
							if(!skip){
								evaluateExpression(temp.getLineNumber());
								updateVariable(temp.getLexeme(), immediate.getVariableType(), immediate.getVariableValue());
							}
							return true;
						}
						return false;
					}
					else{
						Token a = (Token)tokensArrayList [currentPosition-1];
						if (a.getLexeme () == "\n") a = (Token)tokensArrayList [currentPosition-2];
						MainClass.win.updateMessagesOnConsole ($"You have an error in your LOLCODE Syntax near {a.getLexeme()} at line {a.getLineNumber()}. Expected R.");
						return false;
					}
				}
				else{
					Token temp2 = (Token) tokensArrayList[currentPosition-1];
					MainClass.win.updateMessagesOnConsole($"Semantic Error: Variable not declared at line {temp2.getLineNumber()}");
					return false;
				}
			}
			else return false;
		}
		#endregion
		#region IF REGION
		private bool if_statement(){
			int save = currentPosition;

			if ((currentPosition = save) == save & checkType (Keyword.O_RLY) && linebreak ()) {
				Console.WriteLine ("HEEEY");
				tempDictionary.Clear ();
				tempDictionary.Add ("skip", this.skip);
				tempDictionary.Add ("elseEntered", this.elseEntered);
				tempDictionary.Add ("ifEntered", this.ifEntered);
				tempDictionary.Add ("matched", this.matched);
				//Console.WriteLine (skip.ToString() + elseEntered.ToString() + ifEntered.ToString());
				//this.skip = false;
				this.matched = false;
				this.elseEntered = false;
				this.ifEntered = false;
				scopeStack.Push (new State(Keyword.O_RLY,tempDictionary));
				if (conditionalStatementEntered ())
					return true;
				else
					return false;
			}
			else
				return false;
		}

		private bool conditionalStatementEntered(){
			int save = currentPosition;

			if((currentPosition = save) == save & !this.ifEntered && checkType(Keyword.YA_RLY)){
				this.ifEntered = true;
				if(getVariableValueFromKey("IT") == "WIN"){
					this.matched = true;
					this.skip = false;
				}
				else this.skip = true;
				if(statement()){
					return true;
				}
				return false;
			}
			else{
				return false;
			}
		}
		#endregion
		#region CONCATENATION
		private bool concatenation(){
			int save = currentPosition;
			if ((currentPosition = save) == save & checkType (Keyword.SMOOSH)) {
				this.concatenationEntered = true;
				if (expr ()) {
					if (plus_literalAndVariable ())
						return true;
				}
				return false;
			} else
				return false;
		}

		private bool plus_literalAndVariable(){
			int save = currentPosition;
			if ((currentPosition = save) == save & checkType (Keyword.AN) && expr () && plus_literalAndVariable ())
				return true;
			else if ((currentPosition = save) == save & checkType (Keyword.MKAY) && linebreak ()) {
				currentPosition -= 1;
				return true;
			}
			else if ((currentPosition = save) == save & expr() && plus_literalAndVariable ())
				return true;
			else if ((currentPosition = save) == save & linebreak ()) {
				currentPosition -= 1;
				return true;
			} else {
				return false;
			}
		}
		#endregion
	}
}

