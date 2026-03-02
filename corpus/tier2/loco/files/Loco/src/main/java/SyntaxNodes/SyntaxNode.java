package SyntaxNodes;

public abstract class SyntaxNode {
	protected SyntaxType type;
	
	public SyntaxNode(SyntaxType type) {
		this.type = type;
	}
	
	
	public abstract void printChildren(int tab);
	
	public abstract String getStrChildren(int tab);
	
	public void printTab (int x) {
		while (x-- > 0) {
			System.out.print("\t");
		}
	}
	
	public String getStrTab(int x) {
		String str = new String();
		while (x-- > 0) {
			str += "\t";
		}
		
		return str;
	}
	
	public SyntaxType getType() {
		return type;
	}
}
