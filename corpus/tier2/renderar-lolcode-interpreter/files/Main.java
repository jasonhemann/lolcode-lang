//Main.java

/* used for analysis */

public class Main{
	public static void main(String[] args) {
		LexicalAnalyzer l = new LexicalAnalyzer(args[0]);
		l.showStack();
		SyntaxAnalyzer s = new SyntaxAnalyzer(l.getStack());
	}
}
