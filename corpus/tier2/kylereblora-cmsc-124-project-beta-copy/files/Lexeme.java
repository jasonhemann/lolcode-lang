
	/*****************************************************************************************
	*  File Description:                                                                     *
	*  This file creates the lexeme class for the back-end program.                           *
	*****************************************************************************************/

//  --------------------------------------------------  [PACKAGE DECLARATION]
	package src;

//  --------------------------------------------------  [CLASS SPECIFICATION]
public class Lexeme{

	/***************
	*  Attributes  *
	***************/
	private String regex;
	private String lextype;

	/************************
	*  Lexeme Constructors  *
	************************/
	public Lexeme(String regex, String lextype){
		this.regex = regex;
		this.lextype = lextype;
	}

	/****************
	*    Getters    *
	****************/
	public String getRegex(){ return this.regex; }
	public String getLexType(){ return this.lextype; }
	public String lexToString(){ return this.regex.toString();}

	/****************
	*    Setters    *
	****************/
	public void setText(String regex){ this.regex = regex;}
}
