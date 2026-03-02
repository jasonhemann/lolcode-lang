package SyntaxNodes;

import backend.Token;

public class NodeRoot extends SyntaxNode {
	SyntaxType type;
	Token start, end;
	SyntaxNode statement;
	
	public NodeRoot (Token start, Token end) {
		super(SyntaxType.root);
		this.start = start;
		this.end = end;
	}
	
	public NodeRoot (Token start, SyntaxNode statement, Token end) {
		super(SyntaxType.root);
		this.start = start;
		this.statement = statement;
		this.end = end;
		
	}
	
	public void printChildren(int tab) {
		printTab(tab);
		System.out.println("{");
		
		printTab(tab);
		System.out.println("PARSE TREE");
		System.out.print("0: ");
		printTab(tab);
		System.out.println(start.getValue());
		
		System.out.println("1: ");
		printTab(tab);
		if (statement == null) System.out.println("<No Statements>");
		else statement.printChildren(tab + 1);
		
		System.out.print("2: ");
		printTab(tab);
		System.out.println(end.getValue());
		
		printTab(tab);
		System.out.println("}");
	}
	
	public String getStrChildren(int tab) {
		String str = new String();
		
		str += getStrTab(tab);
		str += "{\n";
		
		str += getStrTab(tab);
		str += "PARSE TREE\n";
		str += "0: ";
		str += getStrTab(tab);
		str += start.getValue() + "\n";
		
		str += "1: \n";
		str += getStrTab(tab);
		if (statement == null) str += "<Not Statements>\n";
		else str += statement.getStrChildren(tab + 1);
		
		str += "2: ";
		str += getStrTab(tab);
		str += end.getValue() + "\n";
		
		str += getStrTab(tab);
		str += "}\n";
		
		return str;
	}
	
	public SyntaxNode getStatements() {
		return statement;
	}
}
