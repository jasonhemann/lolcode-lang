package SyntaxNodes;

public enum SyntaxType {
	root,
	statement,
	expression,
	assignment,
	flowcontrol,
	
	comment,
	literal,
	varid,
	vartype,
	
	newvar,
	varchange,
	vartypechange,
	
	mathop,
	boolop,
	cmpop,
	infarop,
	
	concat,
	print,
	scan,
	
	ifblock,
	switchcase,
	gtfo,
	loop,
	loopcond,
	function,
	functionret,
	functioncall,
	
	invalid
}
