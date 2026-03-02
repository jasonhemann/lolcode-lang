package SyntaxNodes;

import java.util.ArrayList;

import backend.Token;
import backend.TokenKind;

public class NodeMultiLine extends SyntaxNode {
	Token operation;
	
	Token loopid;
	Token optype;
	SyntaxNode condition;
	
	ArrayList<SyntaxNode> ifConditions;
	ArrayList<SyntaxNode> statements;
	
	public NodeMultiLine(Token operation, Token loopid, Token optype, SyntaxNode condition, ArrayList<SyntaxNode> statements) {
		super(SyntaxType.loop);
		
		this.operation = operation;
		this.loopid = loopid;
		this.optype = optype;
		this.condition = condition;
		this.statements = statements;
		
	}
	
	public NodeMultiLine(SyntaxType type, Token operation, ArrayList<SyntaxNode> ifConditions, ArrayList<SyntaxNode> statements) {
		super(type);
		
		this.operation = operation;
		this.ifConditions = ifConditions;
		this.statements = statements;
		
	}
	
	public void printChildren(int tab) {
		NodeLiteral currentLiteral;
		int i;
		
		printTab(tab);
		System.out.println("{");
		
		if (type == SyntaxType.ifblock) {
			printTab(tab);
			System.out.println(operation.getValue() + ": ");
			
			for (i = 0; i < statements.size(); i++) {
				printTab(tab);
				System.out.println(i + ": ");
				statements.get(i).printChildren(tab + 1);
			}
			
		} else if (type == SyntaxType.switchcase) {
			printTab(tab);
			System.out.println(operation.getValue() + ": ");
			
			for (i = 0; i < ifConditions.size(); i++) {
				currentLiteral = (NodeLiteral) ifConditions.get(i);
				
				printTab(tab);
				if (currentLiteral.getToken().getTokenKind() == TokenKind.yarnToken) {
					System.out.println("\"" + currentLiteral.getToken().getValue() + "\": ");
				} else {
					System.out.println(currentLiteral.getToken().getValue() + ": ");
				}
				
				statements.get(i).printChildren(tab + 1);
			}
			
		} else if (type == SyntaxType.loop) {
			printTab(tab);
			System.out.print(operation.getValue() + ": " + loopid.getValue());
			System.out.println(" (" + optype.getValue() + ")");
			
			printTab(tab);
			System.out.println("Condition: ");
			condition.printChildren(tab + 1);
			
			printTab(tab);
			System.out.println("0: ");
			statements.get(0).printChildren(tab + 1);
		
		} else if (type == SyntaxType.function) {
			printTab(tab);
			System.out.println("HOW IZ I: " + operation.getValue());
			
			printTab(tab);
			System.out.println("Parameters: ");
			
			printTab(tab + 1);
			for (i = 0; i < ifConditions.size(); i++) {
				currentLiteral = (NodeLiteral) ifConditions.get(i);
				
				System.out.print(currentLiteral.getToken().getValue() + " ");
			}
			System.out.println();
			
			printTab(tab);
			System.out.println("0: ");
			statements.get(0).printChildren(tab + 1);
		}
		
		printTab(tab);
		System.out.println("}");
	}
	
	public String getStrChildren(int tab) {
		String str = new String();
		NodeLiteral currentLiteral;
		int i;
		
		str += getStrTab(tab);
		str += "{\n";
		
		if (type == SyntaxType.ifblock) {
			str += getStrTab(tab);
			str += operation.getValue() + ": \n";
			
			for (i = 0; i < statements.size(); i++) {
				str += getStrTab(tab);
				str += i + ": \n";
				str += statements.get(i).getStrChildren(tab + 1);
			}
			
		} else if (type == SyntaxType.switchcase) {
			str += getStrTab(tab);
			str += operation.getValue() + ": \n";
			
			for (i = 0; i < ifConditions.size(); i++) {
				currentLiteral = (NodeLiteral) ifConditions.get(i);
				
				str += getStrTab(tab);
				
				if (currentLiteral.getToken().getTokenKind() == TokenKind.yarnToken) {
					str += "\""+ currentLiteral.getToken().getValue() + "\": \n";
				} else {
					str += currentLiteral.getToken().getValue() + ": \n";
				}
				
				str += statements.get(i).getStrChildren(tab + 1);
			}

			
		} else if (type == SyntaxType.loop) {
			str += getStrTab(tab);
			
			str += operation.getValue() + ": " + loopid.getValue();
			str += " (" + optype.getValue() + ")\n";
			
			str += getStrTab(tab);
			str += "Condition: \n";
			str += condition.getStrChildren(tab + 1);
			
			str += getStrTab(tab);
			str += "0: \n";
			str += statements.get(0).getStrChildren(tab + 1);

		} else if (type == SyntaxType.function) {
			str += getStrTab(tab);
			str += "HOW IZ I: " + operation.getValue() + "\n";
			
			str += getStrTab(tab);
			str += "Parameters: \n";
			
			str += getStrTab(tab + 1);
			for (i = 0; i < ifConditions.size(); i++) {
				currentLiteral = (NodeLiteral) ifConditions.get(i);
				
				str += currentLiteral.getToken().getValue() + " ";
			}
			str += "\n";
			
			str += getStrTab(tab);
			str += "0: \n";
			str += statements.get(0).getStrChildren(tab + 1);
		}
		
		str += getStrTab(tab);
		str += "}\n";
		
		return str;
	}

	public Token getOperation() {
		return operation;
	}

	public Token getOpType() {
		return optype;
	}
	
	public SyntaxNode getCondition() {
		return condition;
	}
	
	public ArrayList<SyntaxNode> getIfConditions() {
		return ifConditions;
	}
	
	public ArrayList<SyntaxNode> getStatements() {
		return statements;
	}
	
	
}
