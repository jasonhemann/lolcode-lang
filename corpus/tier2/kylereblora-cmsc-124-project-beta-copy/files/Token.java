
	/*****************************************************************************************
	*  File Description:                                                                     *
	*  This file creates the token class for the back-end program.                           *
	*****************************************************************************************/

//  --------------------------------------------------  [PACKAGE DECLARATION]
	package src;

//  --------------------------------------------------  [JAVA IMPORTS]
	import java.util.regex.Matcher;
	import java.util.regex.Pattern;

//  --------------------------------------------------  [CLASS SPECIFICATION]
public class Token {

	/***************
	*  Attributes  *
	***************/
	private Pattern regex;
	private String type;

	/***********************
	*  Token Constructors  *
	***********************/
	public Token(Pattern regex, String tokentype) {
		this.regex = regex;
		this.type = tokentype;
	}

	/****************
	*    Getters    *
	****************/
	public Pattern getRegex(){ return this.regex; }
	public String getType(){ return this.type;}
}
