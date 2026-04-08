//SyntaxAnalyzer.java
import java.util.*;
import javax.swing.*;
import java.util.regex.*;

public class SyntaxAnalyzer {
	// attributes
	private Stack<Token> tokenStack;

	// constructor
	public SyntaxAnalyzer(Stack<Token> tokenStack){
		Collections.reverse(tokenStack);
		this.tokenStack = tokenStack;
		errorHandler();
	}

	public void errorHandler(){
		try{
			System.out.println(code(this.tokenStack.pop())? "Code will run." : "Code cannot run. Wrong token.");
		} catch(Exception e) {
            System.out.println("Code cannot run. Reached end of stack.");
        }
	}

/*	<code> ::= HAI \n <program>	*/
	private boolean code(Token next){
		
		if(next.getType().equals("Source Code Delimiter")){
			System.out.println("Code Start Successful");
			if(lineBreak(this.tokenStack.pop())) return program(this.tokenStack.pop());
	
		}return false;
	}

/*	<br> ::= \n | ,	*/
	private boolean lineBreak(Token next){
		return (next.getType().equals("Newline") || next.getType().equals("Command Break"));
	}

/* 	<program> ::= <br> <program> | <statement> <br> <program> | KTHXBYE	*/
	private boolean program(Token next){

		if(lineBreak(next)) return program(this.tokenStack.pop());

		else if(next.getType().equals("Gimmeh Keyword") || next.getType().equals("Visible Keyword") || next.getType().equals("Variable Declaration") || next.getType().equals("Variable Identifier") || next.getType().equals("Arithmetic") || next.getType().equals("Division") || next.getType().equals("Boolean Binary") || next.getType().equals("Boolean Unary") || next.getType().equals("Infinite And") || next.getType().equals("Infinite Or") || next.getType().equals("And") || next.getType().equals("Different") || next.getType().equals("String Concatenate") || next.getType().equals("If-else Start") || next.getType().equals("Switch Start")){
			if(statement(next)){
				if(lineBreak(this.tokenStack.pop())) return program(this.tokenStack.pop());
			}return false;

		}else if(next.getType().equals("Source Code Delimiter")) return true;

		return false;
	}

/*	GIMMEH <input> | VISIBLE <output> | I HAS A <declaration> | variable <assignment> | <arithmeticExpression> | 
	<booleanExpression> | <infiniteBooleanExpression> | <comparison> | <concatenation>	*/
	private boolean statement(Token next){

		if(next.getType().equals("Gimmeh Keyword")) return input(this.tokenStack.pop());

		else if(next.getType().equals("Visible Keyword")) return output(this.tokenStack.pop());

		else if(next.getType().equals("Variable Declaration")) return declaration(this.tokenStack.pop());

		else if(next.getType().equals("Variable Identifier")) return assignment(this.tokenStack.pop());

		else if(next.getType().equals("Arithmetic") || next.getType().equals("Division")) return arithmeticExpression(next);

		else if(next.getType().equals("Boolean Binary") || next.getType().equals("Boolean Unary")) return booleanExpression(next);

		else if(next.getType().equals("Infinite And") || next.getType().equals("Infinite Or")) return infiniteBooleanExpression(next);

		else if(next.getType().equals("And") || next.getType().equals("Different")) return comparisonExpression(next);

		else if(next.getType().equals("String Concatenate")) return concatenation(next);

		else if(next.getType().equals("If-else Start")){
			if(lineBreak(this.tokenStack.pop())) return ifelseCondition(this.tokenStack.pop());
		
		}else if(next.getType().equals("Switch Start")){
			if(lineBreak(this.tokenStack.pop())) return switchCondition(this.tokenStack.pop());
		
		}return false;
	}

/*	<input> ::= variable	*/
	private boolean input(Token next){
		
		if(next.getType().equals("Variable Identifier")) return true;
		
		return false;
	}

/*	<output> ::= <value> <output> | <value>	*/
	private boolean output(Token next){

		if(value(next)){
			if (!this.tokenStack.peek().getType().equals("Newline") && !this.tokenStack.peek().getType().equals("Command Break")) return output(this.tokenStack.pop());

			return true;
		
		}return false;
	}

/*	<multiExpression> ::= <value> AN <multiExpression> | <value>	*/
	public boolean multiExpression(Token next){
		
		if(value(next)){
			if (this.tokenStack.peek().getType().equals(("Operation Separator"))){
				this.tokenStack.pop();
				return multiExpression(this.tokenStack.pop());

			}return true;
		
		}return false;
	}

/*	<declaration> ::=	I HAS A variable | I HAS A variable ITZ <value>		*/
	public boolean declaration(Token next){

		if(next.getType().equals("Variable Identifier")){
			if(this.tokenStack.peek().getType().equals("Variable Initialization")){
				this.tokenStack.pop();
				return value(this.tokenStack.pop());

			}return true;

		}return false;
	}

/*	<value> ::= <arithmeticExpression> | <booleanExpression> | <infinitebooleanExpression> | <comparisonExpression> | <concatenation> |variable | IT | Literal	*/
	public boolean value(Token next){

		if(next.getType().equals("Variable Identifier") || next.getType().equals("Variable Expression") || next.getType().contains("Literal")) return true;
		
		else if(next.getType().equals("Arithmetic") || next.getType().equals("Division")) return arithmeticExpression(next);

		else if(next.getType().equals("Boolean Binary") || next.getType().equals("Boolean Unary")) return booleanExpression(next);

		else if(next.getType().equals("Infinite And") || next.getType().equals("Infinite Or")) return infiniteBooleanExpression(next);

		else if(next.getType().equals("And") || next.getType().equals("Different")) return comparisonExpression(next);

		else if(next.getType().equals("String Concatenate")) return concatenation(next);

		return false;
	}

/*	<assignment> ::= R <value>	*/
	public boolean assignment(Token next){

		if(next.getType().equals("Variable Assignment")) return value(this.tokenStack.pop());

		return false;
	}

/*	<arithmetic> ::= SUM OF <arithmeticExpression> AN <arithmeticExpression> | DIFF OF <arithmeticExpression> AN <arithmeticExpression> |
	PRODUKT OF <arithmeticExpression> AN <arithmeticExpression> | QUOSHUNT OF <arithmeticExpression> AN <arithmeticExpression> |
	MOD OF <arithmeticExpression> AN <arithmeticExpression> | BIGGR OF <arithmeticExpression> AN <arithmeticExpression> |
	SMALLR OF <arithmeticExpression> AN <arithmeticExpression> | variable | literal | IT */
	public boolean arithmeticExpression(Token next){

		if(next.getType().equals("Variable Identifier") || next.getType().contains("Literal") || next.getType().equals("Variable Expression")) return true;

		else if(next.getType().equals("Arithmetic") || next.getType().equals("Division")){
			if(arithmeticExpression(this.tokenStack.pop())){
				if(this.tokenStack.pop().getType().equals("Operation Separator")) return arithmeticExpression(this.tokenStack.pop());
			}
		
		}return false;
	}

/* 	<booleanExpression> ::= BOTH OF <booleanExpression> AN <booleanExpression> | EITHER OF <booleanExpression> AN <booleanExpression> |
	WON OF <booleanExpression> AN <booleanExpression> | NOT <booleanExpression> | variable | literal | IT	*/
	public boolean booleanExpression(Token next){

		if(next.getType().equals("Variable Identifier") || next.getType().contains("Literal") || next.getType().equals("Variable Expression")) return true;

		else if(next.getType().equals("Boolean Binary")){
			if(booleanExpression(this.tokenStack.pop())){
				if(this.tokenStack.pop().getType().equals("Operation Separator")) return booleanExpression(this.tokenStack.pop());
			}else return false;

		}else if(next.getType().equals("Boolean Unary")) return booleanExpression(this.tokenStack.pop());
		
		return false;
	}

/*	<comparison> ::= BOTH SAEM <arithmeticExpression> AN <arithmeticExpression>	| DIFFRINT <arithmeticExpression> AN <arithmeticExpression>	*/
	public boolean comparisonExpression(Token next){

		if(next.getType().equals("And") || next.getType().equals("Different")){
			if(arithmeticExpression(this.tokenStack.pop())){
				if(this.tokenStack.pop().getType().equals("Operation Separator")) return arithmeticExpression(this.tokenStack.pop());
			}

		}return false;
	}

/*	<infiniteBooleanExpression> ::= ANY OF <multipleBoolean> MKAY | ALL OF <multipleBoolean> MKAY	*/
	public boolean infiniteBooleanExpression(Token next){

		if(next.getType().equals("Infinite And") || next.getType().equals("Infinite Or")){
			if(multipleBoolean(this.tokenStack.pop())){
		 		return this.tokenStack.pop().getType().equals("Boolean End");
			}		
		
		}return false;
	}

/*	<multipleBoolean> ::= variable AN <multipleBoolean> | literal AN <multipleBoolean> | IT	AN <multipleBoolean> | variable | literal | IT 	*/
	public boolean multipleBoolean(Token next){

		if(next.getType().equals("Variable Identifier") || next.getType().contains("Literal") || next.getType().equals("Variable Expression") || booleanExpression(next)){
			if(this.tokenStack.peek().getType().equals("Operation Separator")){
				this.tokenStack.pop();
				return multipleBoolean(this.tokenStack.pop());	
			
			}return true;
		
		}return false;
	}

/*	<concatenation> = SMOOSH <multiExpression>	*/
	public boolean concatenation(Token next){

		if(next.getType().equals("String Concatenate")){
			return multiExpression(this.tokenStack.pop());

		}return false;
	}

/* 	<subprogram> ::= <br> <subprogram> | <statement> <br> <subprogram>	*/
	private boolean subProgram(Token next){

		if(lineBreak(next)) return subProgram(this.tokenStack.pop());

		else if(next.getType().equals("Gimmeh Keyword") || next.getType().equals("Visible Keyword") || next.getType().equals("Variable Declaration") || next.getType().equals("Variable Identifier") || next.getType().equals("Arithmetic") || next.getType().equals("Division") || next.getType().equals("Boolean Binary") || next.getType().equals("Boolean Unary") || next.getType().equals("Infinite And") || next.getType().equals("Infinite Or") || next.getType().equals("And") || next.getType().equals("Different") || next.getType().equals("String Concatenate")){	
			if(statement(next)){
				if(lineBreak(this.tokenStack.pop())) return subProgram(this.tokenStack.pop());
			}return false;

		}else if(next.getType().equals("Break Keyword")){
			if(lineBreak(this.tokenStack.pop())) return subProgram(this.tokenStack.pop());

		}else if(next.getType().equals("If Keyword") || next.getType().equals("Else-If Keyword") || next.getType().equals("Else Keyword") || next.getType().equals("Case Keyword") || next.getType().equals("Default Keyword") || next.getType().equals("Condition End")){
			this.tokenStack.push(next);
			return true;

		}return false;
	}

/*	<ifelse> ::= <br> <ifelse> | <if> <else> | OIC	*/
	private boolean ifelseCondition(Token next){

		if(lineBreak(next)) return ifelseCondition(this.tokenStack.pop());

		else if(next.getType().equals("Condition End")) return true;

		else if(ifBlock(next)) return elseBlock(this.tokenStack.pop());

		return false;
	}

/*	<if> ::= YA RLY <br> <subprogram>	*/
	private boolean ifBlock(Token next){

		if(next.getType().equals("If Keyword")){
			if(lineBreak(this.tokenStack.pop())) return subProgram(this.tokenStack.pop());

		}return false;
	}

/*	<else> ::= <elseif> <else> | <elseif> OIC | NO WAI <br> <subprogram> OIC | OIC */
	private boolean elseBlock(Token next){

		if(next.getType().equals("Condition End")) return true;
		
		else if(next.getType().equals("Else Keyword")){
			if(lineBreak(this.tokenStack.pop())){
				if(subProgram(this.tokenStack.pop())) return this.tokenStack.pop().getType().equals("Condition End");
			}return false;
		
		}else if(elseifBlock(next)){
			if(this.tokenStack.peek().getType().equals("Condition End")) return this.tokenStack.pop().getType().equals("Condition End");
			return elseBlock(this.tokenStack.pop());
		}

		return false;
	}

/*	<elseif> ::= MEBBE <value> <br> <subprogram>	*/
	private boolean elseifBlock(Token next){

		if(next.getType().equals("Else-If Keyword")){
			if(value(this.tokenStack.pop())){
				if(lineBreak(this.tokenStack.pop())) return subProgram(this.tokenStack.pop());
			}
		
		}return false;
	}

/*	<switch> ::= <br> <switch> | <case> <switch> | <case> <default> OIC | OIC	*/
	private boolean switchCondition(Token next){

		if(lineBreak(next)) return switchCondition(this.tokenStack.pop());

		if(next.getType().equals("Condition End")) return true;

		else if(caseBlock(next)){
			if(this.tokenStack.peek().getType().equals("Default Keyword")){
				if(defaultBlock(this.tokenStack.pop())) return this.tokenStack.pop().getType().equals("Condition End");
			}else return switchCondition(this.tokenStack.pop());
		
		}return false;
	}

/*	<case> ::= OMG <value> <br> <subprogram> */
	private boolean caseBlock(Token next){

		if(next.getType().equals("Case Keyword")){
			if(value(this.tokenStack.pop())){
				if(lineBreak(this.tokenStack.pop())) return subProgram(this.tokenStack.pop());
			}
		}return false;
	}

/*	<default> ::= OMGWTF <br> <subProgram> */
	private boolean defaultBlock(Token next){

		if(next.getType().equals("Default Keyword")){
			if(lineBreak(this.tokenStack.pop())) return subProgram(this.tokenStack.pop());

		}return false;
	}
}