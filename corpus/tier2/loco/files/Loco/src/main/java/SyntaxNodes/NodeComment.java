package SyntaxNodes;

import java.util.ArrayList;

import backend.Token;

public class NodeComment extends SyntaxNode{
	Token start, end;	
	ArrayList<Token> inner;
	
	public NodeComment(Token start, ArrayList<Token> inner, Token end) {
		super(SyntaxType.comment);
		this.start = start;
		this.inner = inner;
		this.end = end;
	}
	
	
	public void printChildren(int tab) {
		printTab(tab);
		System.out.println("{");
		
		printTab(tab);
		System.out.println("Comment: ");
		
		for (Token i : inner) {
			printTab(tab + 1);
			System.out.print(i.getValue());
		}
		
		printTab(tab);
		System.out.println("}");
	}
	
	public String getStrChildren(int tab) {
		String str = new String();
		
		str += getStrTab(tab);
		str += "{\n";
		
		str += getStrTab(tab);
		str += "Comment: \n";
		
		for (Token i : inner) {
			str += getStrTab(tab + 1);
			str += i.getValue();
		}
		
		str += getStrTab(tab);
		str += "}\n";
		
		return str;
	}
	
}
