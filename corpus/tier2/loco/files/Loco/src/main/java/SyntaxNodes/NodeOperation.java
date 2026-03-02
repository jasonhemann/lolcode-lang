package SyntaxNodes;

import backend.Token;

public class NodeOperation extends SyntaxNode{
	Token operation;
	SyntaxNode operand1, operand2;
	
	public NodeOperation (SyntaxType type, Token operation, SyntaxNode op1, SyntaxNode op2) {
		super(type);
		this.operation = operation;
		this.operand1 = op1;
		this.operand2 = op2;
		
	}
	
	public NodeOperation (SyntaxType type, Token operation, SyntaxNode op1) {
		super(type);
		this.operation = operation;
		this.operand1 = op1;
	}
	
	public void printChildren(int tab) {
		printTab(tab);
		System.out.println("{");
		
		printTab(tab);
		System.out.println(operation.getValue() + ": ");
		printTab(tab);
		System.out.println("0: ");
		operand1.printChildren(tab + 1);
		
		if (operand2 != null) {
			printTab(tab);
			System.out.println("1: ");
			operand2.printChildren(tab + 1);
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
		str += "0: \n";
		str += operand1.getStrChildren(tab + 1);
		
		if (operand2 != null) {
			str += getStrTab(tab);
			str += "1: \n";
			str += operand2.getStrChildren(tab + 1);
		}
		
		str += getStrTab(tab);
		str += "}\n";
		
		return str;
	}
	
	public Token getOperation() {
		return operation;
	}
	
	public SyntaxNode getOp1() {
		return operand1;
	}
	
	public SyntaxNode getOp2() {
		return operand2;
	}
}
