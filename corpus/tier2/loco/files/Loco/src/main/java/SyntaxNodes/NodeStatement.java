package SyntaxNodes;

public class NodeStatement extends SyntaxNode{
	SyntaxType type;
	SyntaxNode operand1, operand2;
	int lineCounter;
	static int counter = 0;
	
	public NodeStatement(SyntaxNode op1, SyntaxNode op2) {
		super(SyntaxType.statement);
		this.operand1 = op1;
		this.operand2 = op2;
		
		this.lineCounter = ++counter;
		
	}
	
	public void printChildren(int tab) {
		
		printTree(tab);
		//operand1.printChildren(tab);
		//operand2.printChildren(tab);
	}
	
	public String getStrChildren(int tab) {
		String str = new String();
		
		str += getStrTree(tab);
		//str += operand1.getStrChildren(tab);
		//str += operand2.getStrChildren(tab);
		
		return str;
	}
	
	public void printTree(int tab) {
		
		printTab(tab);
		System.out.println("{");
		
		printTab(tab);
		System.out.println("Statement Node:");
		
		//printTab(tab);
		//System.out.println("Line " + (Math.abs(lineCounter - counter) + 2) + ":");
		operand1.printChildren(tab + 1);
		
		
		//printTab(tab);
		//System.out.println("Line " + (Math.abs(lineCounter - counter) + 3) + ":");
		operand2.printChildren(tab + 1);
		
		printTab(tab);
		System.out.println("}");
		
	}
	
	public String getStrTree(int tab) {
		String str = new String();
		
		str += getStrTab(tab);
		str += "{\n";
		
		str += getStrTab(tab);
		str += "Statement Node:\n";
		

		str += operand1.getStrChildren(tab + 1);
		str += operand2.getStrChildren(tab + 1);

		
		str += getStrTab(tab);
		str += "}\n";
		
		return str;
	}
	
	public SyntaxNode getOp1() {
		return operand1;
	}
	
	public SyntaxNode getOp2() {
		return operand2;
	}
}
