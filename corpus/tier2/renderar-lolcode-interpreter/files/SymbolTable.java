//SymbolTable.java
import java.util.*;
import javax.swing.*;


public class SymbolTable {
	private Stack<Variable> stackOfVariables;

	public SymbolTable(Stack<Token> stackOfTokens){
		this.stackOfVariables = new Stack<Variable>();
		String varname = "";
		String varvalue = "";
		String vartype = "";
		boolean isVariable = false;
		for(Token t : stackOfTokens){
			if(t == null)continue;
			if(t.getType().equals("Variable Identifier")){
				varname = t.getContent();
			}else if(t.getType().contains("Literal")){
				varvalue = t.getContent();
				vartype = t.getType();
				isVariable = true;
			}
			
			if(isVariable == true){
				stackOfVariables.push(new Variable(varname, vartype, varvalue));
				isVariable = false;
			}
		}
	}

	public void showIdentifiers(JTextArea idHolder, JTextArea valHolder){
		for(Variable v : this.stackOfVariables){
			if(v == null)continue;
			v.show(idHolder, valHolder);
		}
	}


}
