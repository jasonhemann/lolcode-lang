package backend;

public class Token {
	private TokenKind tokenKind;
	private String value;
	private int position;

	Token(TokenKind kind, String value, int position) {
		this.tokenKind = kind;
		this.value = value;
		this.position = position;
		
	}

	public TokenKind getTokenKind() {
		return tokenKind;
	}

	public String getValue() {		
		return value;
	}
	
	public int getPosition() {
		return position;
	}

	public void viewToken() {
		System.out.println(tokenKind + ": " + value);
	}
}
