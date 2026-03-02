package SyntaxNodes;

public class NodeExpression extends SyntaxNode {
	SyntaxNode node;
	int lineCounter;
	
	public NodeExpression(SyntaxNode node, int lineCounter) {
		super(SyntaxType.expression);
		this.node = node;
		this.lineCounter = lineCounter;
		
	}
	
	public void printChildren(int tab) {
		printTab(tab);
		System.out.println("{");
		
		printTab(tab);
		System.out.println("Line "+lineCounter+": (Expression)");
		node.printChildren(tab + 1);
		
		printTab(tab);
		System.out.println("}");
	}
	
	public String getStrChildren(int tab) {
		String str = new String();
		
		str += getStrTab(tab);
		str += "{\n";
		
		str += getStrTab(tab);
		str += "Line " + lineCounter + ": (Expression)\n";
		str += node.getStrChildren(tab+1);
		
		str += getStrTab(tab);
		str += "}\n";
		
		return str;
	}
	
	public SyntaxNode getNode() {
		return node;
	}
	
	public int getLineCounter() {
		return lineCounter;
	}
}
