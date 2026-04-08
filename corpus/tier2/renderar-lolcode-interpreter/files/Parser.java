import java.util.*;
import javax.swing.*;
import java.util.regex.*;

public class Parser {
	private Token token;
	private Stack<Token> stack;
	private static final Pattern KEYWORD = Pattern.compile("^(|SMOOSH|MAEK|A|IS NOW A|IM IN YR|UPPIN|NERFIN|YR|TIL|WILE|IM OUTTA YR)");
    private static final Pattern CODE_START = Pattern.compile("^(HAI)");
    private static final Pattern CODE_END = Pattern.compile("^(KTHXBYE)");
    private static final Pattern COMMENT = Pattern.compile("^(BTW)");
    private static final Pattern COMMENT_SEPARATE = Pattern.compile("^(OBTW|TLDR)");
    private static final Pattern INPUT = Pattern.compile("^(GIMMEH)");
    private static final Pattern OUTPUT = Pattern.compile("^(VISIBLE)");
    private static final Pattern DECLARATION = Pattern.compile("^(I\\sHAS\\sA)");
    private static final Pattern EXPRESSION = Pattern.compile("^(IT)");
    private static final Pattern INITIALIZE = Pattern.compile("^(ITZ)");
    private static final Pattern ASSIGNMENT = Pattern.compile("^(R)");
    private static final Pattern ARITHMETIC = Pattern.compile("^(SUM\\sOF|DIFF\\sOF|PRODUKT\\sOF|QUOSHUNT\\sOF|MOD\\sOF|BIGGR\\sOF|SMALLR\\sOF)");
    private static final Pattern BOOLEAN = Pattern.compile("^(BOTH\\sOF|EITHER\\sOF|WON\\sOF)");
    private static final Pattern BOOLEAN_INFINITE = Pattern.compile("^(ANY\\sOF|ALL\\sOF)");
    private static final Pattern BOOLEAN_UNARY = Pattern.compile("^(NOT)");
    private static final Pattern COMPARISON = Pattern.compile("^(BOTH\\sSAEM|DIFFRINT)");
    private static final Pattern OPERATION_SEPARATOR = Pattern.compile("^(AN)");
    private static final Pattern CONCATENATE = Pattern.compile("^(SMOOSH)");
    private static final Pattern IFELSE_START = Pattern.compile("^(O\\sRLY?)");
    private static final Pattern SWITCH_START = Pattern.compile("^(WTF?)");
    private static final Pattern CONDITION_END = Pattern.compile("^(OIC)");
    private static final Pattern IF = Pattern.compile("^(YA\\sRLY)");
    private static final Pattern ELSEIF = Pattern.compile("^(MEBBE)");
    private static final Pattern ELSE = Pattern.compile("^(NO\\sWAI)");
    private static final Pattern CASE = Pattern.compile("^(OMG)");
    private static final Pattern DEFAULT = Pattern.compile("^(OMGWTF)");
    private static final Pattern BREAK = Pattern.compile("^(GTFO)");
    private static final Pattern INTEGER = Pattern.compile("^-?\\d+$");
    private static final Pattern FLOAT = Pattern.compile("^-?\\d*\\.\\d+$");
    private static final Pattern STRING = Pattern.compile("^\".*\"$");
    private static final Pattern BOOL = Pattern.compile("^(WIN|FAIL)$");
    private static final Pattern VARIABLE = Pattern.compile("^[a-z]+$");

	public Parser(Stack<Token> stack){
		this.stack = stack;
		codeCheck();
	}

	public boolean match(Token token, Pattern pattern){
		return pattern.matcher(token.getContent()).matches();
	}

	public boolean match(Token token, String string){
		return token.getType().contains(string);
	}

	public void codeCheck(){
		Token token;
		while(!this.stack.empty()){
			token = this.stack.pop();
			if(this.match(token, COMMENT)) continue;
			if(this.match(token, CODE_START)){
				while(!this.match(this.stack.pop(), CODE_END)){
					if(this.stack.empty()){
						System.out.println("Error in code");
						break;
					}if(!statementCheck(this.stack.pop())) break;
				}
			}
		}
	}

	public boolean statementCheck(Token token){
		token.show();
		while(!this.stack.empty()){
			if(this.match(token, INPUT)){
				if(!inputValid(this.stack.pop())){
					System.out.println("Error in input");
					return false;
				}
				if(!this.removeComment(this.stack.pop())){
					System.out.println("Error in input2");
					return false;
				}
			}else if(this.match(token, OUTPUT)){
				if(!outputValid()){
					System.out.println("Error in output");
					return false;
				}
				token = this.stack.pop();
				token.show();
				if(!this.removeComment(token)){
					System.out.println("Error in input");
					return false;
				}
			}else if(this.match(token, DECLARATION)){
				if(!declarationValid(this.stack.pop())){
					System.out.println("Error in declaration");
					return false;
				}
				if(!this.removeComment(this.stack.pop())){
					System.out.println("Error in input");
					return false;
				}
			}else if(this.match(token, VARIABLE)){
				if(!assignmentValid(this.stack.pop())){
					System.out.println("Error in assignment");
					return false;
				}
				if(!this.removeComment(this.stack.pop())){
					System.out.println("Error in input");
					return false;
				}
			}return true;
		}return false;
	}

	public boolean removeComment(Token token){
		if(this.match(token, "Newline")) return true;
		else if(this.match(token, COMMENT)){
			while(!this.stack.empty()){	
				if(this.match(token, "Newline")) return true;
			}
			return false;
		}else return false;
	}

	public boolean inputValid(Token token){
		if(this.match(token, VARIABLE)) return true;
		return false;
	}

	public boolean outputValid(){
		if(this.isInfiniteArity(this.stack.pop())) return true;
		return false;
	}

	public boolean isInfiniteArity(Token token){
		if(this.isValue(token)){
			token = this.stack.pop();
			if (this.match(token, OPERATION_SEPARATOR)) return isInfiniteArity(this.stack.pop());
			if (this.match(token, "Newline")) return true;
			return false;
		}return false;
	}

	public boolean declarationValid(Token token){
		Token sub;
		if(this.match(token, VARIABLE)){
			sub = this.stack.pop();
			if(this.match(sub, INITIALIZE)){
				sub = this.stack.pop();
				if(this.match(sub, VARIABLE) || this.match(sub, "Literal")) return true;
				return false;
			}else this.stack.push(sub);
			return true;
		}return false;
	}

	public boolean assignmentValid(Token token){
		Token sub;
		if(this.match(token, ASSIGNMENT)){
			sub = this.stack.pop();
			if(this.match(sub, VARIABLE) || this.match(sub, "Literal")) return true;
			return false;
		}return false;
	}

	public boolean isValue(Token token){
		if(this.match(token, VARIABLE) || this.match(token, "Literal")) return true;
		return false;
	}
}