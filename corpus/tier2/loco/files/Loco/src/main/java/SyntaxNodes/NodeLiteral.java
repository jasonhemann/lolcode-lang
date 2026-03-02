package SyntaxNodes;

import backend.Token;
import backend.TokenKind;

public class NodeLiteral extends SyntaxNode {
	Token literalToken;
	
	public NodeLiteral(Token token) {
		super(SyntaxType.literal);
		this.literalToken = token;
		
	}
	
	public NodeLiteral(SyntaxType type, Token token) {
		super(type);
		this.literalToken = token;
		
	}
	
	public void printChildren(int tab) {
		printTab(tab);
		System.out.println(literalToken.getValue() + 
						  " ("+literalToken.getTokenKind()+")");
	}
	
	public String getStrChildren(int tab) {
		String str = new String();
		
		str += getStrTab(tab);
		str += literalToken.getValue();
		str += " (" + literalToken.getTokenKind() + ")\n";
		
		return str;
	}
	
	public Token getToken() {
		return literalToken;
	}
}
