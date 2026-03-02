package SyntaxNodes;

import backend.Token;

public class NodeDeclaration extends SyntaxNode {
	Token operation, varid;
	SyntaxNode value;
	
	public NodeDeclaration(SyntaxType type, Token operation, Token varid) {
		super(type);
		this.operation = operation;
		this.varid = varid;
	}
	
	public NodeDeclaration(SyntaxType type, Token operation, Token varid, SyntaxNode value) {
		super(type);
		this.operation = operation;
		this.varid = varid;
		this.value = value;
	}
	
	public void printChildren(int tab) {
		printTab(tab);
		System.out.println("{");
		
		printTab(tab);
		System.out.println(operation.getValue() + ": ");
		printTab(tab);
		System.out.print("varID: ");
		System.out.println(varid.getValue());
		printTab(tab);
		System.out.println("value: ");
		
		
		if (value != null) value.printChildren(tab + 1);
		else {
			printTab(tab + 1);
			System.out.println("<Empty>");
		}
		
		printTab(tab);
		System.out.println("}");
		
	}
	
	public String getStrChildren(int tab) {
		String str = new String();
		
		str += getStrTab(tab);
		str += "{\n";
		
		str += getStrTab(tab);
		str += operation.getValue() + ": \n";
		str += getStrTab(tab);
		str += "varID: ";
		str += varid.getValue() + "\n";
		str += getStrTab(tab);
		str += "value: \n";
		
		if (value != null) str += value.getStrChildren(tab + 1);
		else {
			str += getStrTab(tab + 1);
			str += "<Empty>\n";
		}
		
		str += getStrTab(tab);
		str += "}\n";
		
		return str;
	}
	
	public Token getOperation() {
		return operation;
	}
	
	public Token getVarID() {
		return varid;
	}
	
	public SyntaxNode getValue() {
		return value;
	}

}
