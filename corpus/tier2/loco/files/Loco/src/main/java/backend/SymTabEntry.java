package backend;

public class SymTabEntry {
	private String identifier;
	private TokenKind kind;
	private String value;
	
	SymTabEntry (String identifier, TokenKind kind, String value) {
		this.identifier = identifier;
		this.kind = kind;
		this.value = value;
	}
	
	public String getIdentifier() {
		return identifier;
	}
	
	public TokenKind getKind() {
		return kind;
	}
	
	public String getValue() {
		return value;
	}
	
	public Token getToken() {
		return new Token(kind, value, -1);
	}
	
	public void setKind (TokenKind kind) {
		this.kind = kind;
	}
	
	public void setValue(String value) {
		this.value = value;
	}
	
	public void setKindValue(Token token) {
		this.kind = token.getTokenKind();
		this.value = token.getValue();
	}
}
