package SyntaxNodes;

public class NodeFlowControl extends SyntaxNode {
	SyntaxNode node;
	int lineCounter;
	
	public NodeFlowControl (SyntaxNode node, int lineCounter) {
		super(SyntaxType.flowcontrol);
		this.node = node;
		this.lineCounter = lineCounter;
	}
	
	public void printChildren(int tab) {
		printTab(tab);
		System.out.println("{");

		printTab(tab);
		System.out.println("Line "+lineCounter+": (Flow Control)");
		node.printChildren(tab + 1);
		
		printTab(tab);
		System.out.println("}");
	}
	
	public String getStrChildren(int tab) {
		String str = new String();
		
		str += getStrTab(tab);
		str += "{\n";
		
		str += getStrTab(tab);
		str += "Line " + lineCounter + ": (Flow Control)\n";
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
