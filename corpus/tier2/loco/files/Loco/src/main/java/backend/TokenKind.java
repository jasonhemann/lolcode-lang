package backend;

public enum TokenKind {
	haiToken("HAI", "progStart",1), byeToken("KTHXBYE", "progEnd", 1),

	noobToken("(?!x)x", "", 1),
	numbrToken("-?[0-9]+", "literal", 1), 
	numbarToken("-?[0-9]+\\.[0-9]+", "literal", 1), 
	yarnToken("(\".+?|\"[^\"]+\")", "literal", -1), 
	troofToken("WIN|FAIL", "literal", 1), 
	typeToken("(TROOF|NUMBR|NUMBAR|YARN|NOOB)", "literal", 1),

	btwToken("BTW", "comment", 1), obtwToken("OBTW", "comment",1), tldrToken("TLDR", "comment",1),

	ihasToken("I\sHAS\sA", "newvar", 3), 
	itzToken("ITZ", "", 1), 
	rToken("^R$", "varassign", 1), 

	sumOpToken("SUM\sOF", "mathop", 2), 
	diffOpToken("DIFF\sOF", "mathop", 2), 
	divOpToken("QUOSHUNT\sOF", "mathop", 2), 
	mulOpToken("PRODUKT\sOF", "mathop", 2), 
	modOpToken("MOD\sOF", "mathop", 2), 
	minOpToken("SMALLR\sOF", "mathop", 2), 
	maxOpToken("BIGGR\sOF", "mathop", 2),
	
	bothOpToken("BOTH\sOF", "boolop", 2), 
	eitherOpToken("EITHER\sOF", "boolop", 2), 
	wonOpToken("WON\sOF", "boolop", 2), 
	notOpToken("NOT", "boolop", 1), 
	anyOpToken("ANY\sOF", "infarop", 2), 
	allOpToken("ALL\sOF", "infarop", 2),
	
	bothSameOpToken("BOTH\sSAEM", "cmpop", 2),
	diffrntOpToken("DIFFRINT", "cmpop", 1),
	
	smooshToken("SMOOSH", "concat", 1),
	
	isNowToken("IS\sNOW\sA", "asntypecast", 3),
	maekToken("MAEK", "exptypecast", 1),
	mkayToken("MKAY", "", 1),
	aToken("^A$", "", 1),
	anToken("^AN$", "", 1), 
	
	printToken("VISIBLE", "print", 1),
	scanToken("GIMMEH", "scan", 1),
	
	ifStartToken("O\sRLY\\?", "ifstartblock", 2),
	
	ifBlockToken("YA\sRLY", "ifblock", 2),
	elifBlockToken("MEBBE", "ifblock", 1),
	elseBlockToken("NO\sWAI", "ifblock", 2),
	
	switchToken("WTF\\?", "switchstart", 1),
	caseToken("^OMG$", "switch", 1),
	defaultToken("OMGWTF", "switch", 1),
	breakToken("GTFO", "", 1),
	
	ifEndToken("OIC", "ifblock", 1),
	
	loopStartToken("IM\sIN\sYR", "loop", 3),
	
	incToken("UPPIN", "loop", 1),
	decToken("NERFIN", "loop", 1),
	yrToken("^YR$", "loop", 1),
	tilToken("TIL", "loop", 1),
	wileToken("WILE", "loop", 1),
	
	loopEndToken("IM\sOUTTA\sYR", "loop", 3),
	
	functionStartToken("HOW\sIZ\sI", "function", 3),
	functionRetToken("FOUND\sYR", "function", 2),
	functionEndToken("IF\sU\sSAY\sSO", "function", 4),
	functionCallToken("I\sIZ", "function", 2),
	
	idToken("[a-zA-Z][a-zA-Z0-9_]*", "varident", 1), 

	quoteToken("\"", "", 1), whitespaceToken("\s", "", 1), escapeCharToken(":[\\)>o\":]", "", 1),
	
	exclamationToken("^!$", "", 1), dotsToken("\\.\\.\\.", "", 1), commaToken(",", "", 1),
	
	eolToken("\n", "", 1), eofToken("\0", "", 1), 
	
	miscToken("[^\"\s]+", "", 1), badToken("(?!x)x", "", 1);

	private final String regex;
	private final String type;
	private final int length;

	TokenKind(String regex, String type, int length) {
		this.regex = regex;
		this.type = type;
		this.length = length;
	}

	public String getRegex() {
		return regex;
	}
	
	public String getType() {
		return type;
	}
	
	public int getLength() {
		return length;
	}
}
