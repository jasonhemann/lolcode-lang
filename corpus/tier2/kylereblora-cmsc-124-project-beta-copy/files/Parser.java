
	/*****************************************************************************************
	*  File Description:                                                                     *
	*  This file creates the terminal panel for the UI.                                      *
	*                                                                                        *
	*  Source / Guide:                                                                       *
	*  http://cogitolearning.co.uk/2013/04/writing-a-parser-in-java-the-tokenizer/           *
	*****************************************************************************************/

//  --------------------------------------------------  [PACKAGE DECLARATION]
	package src;

//  --------------------------------------------------  [JAVA IMPORTS]
	import java.util.*;
	import java.util.regex.*;
	import src.*;
	import gui.*;

//  --------------------------------------------------  [CLASS SPECIFICATION]
public class Parser {

	/***************
	*  Attributes  *
	***************/
	private ArrayList<Token> tokens;	//linked list for the tokens in lolcode
	private ArrayList<Lexeme> lexemes;  //linked list for the user input lexeme
	private	Boolean mark;
	private Lexeme tempLex;
	private Matcher matcher;
	private String temp;
	private Terminal myTerminal;

	/****************************
	*    Parser Constructors    *
	****************************/
	public Parser(Terminal terminal){
		this.tokens = new ArrayList<Token>();
		this.lexemes = new ArrayList<Lexeme>();
		this.myTerminal = terminal;
		this.mark = false;
		this.setRegex();
	}


	/****************
	*    Methods    *
	****************/

	public void addRegex(String regex, String tokentype){
		/*-------------------------------------------------------------
			Method Description: saves the regex pattern as a token. 
		-------------------------------------------------------------*/
		tokens.add(new Token(Pattern.compile("^(" + regex + ")"), tokentype));
	}

	public boolean createLexemes(String str) {
		/*-------------------------------------------------------------------------------------------------
			Method Description: This method matches the read lines to the tokens and creates the lexemes.
		-------------------------------------------------------------------------------------------------*/
		String s = str.trim();
		Boolean flag = false;
		String filename = this.myTerminal.getEditor().getFileName();														

		System.out.println("Parsing current line ...");
		while(!s.equals("")){
			for(int i = 0; i < tokens.size(); i++){
				this.matcher = tokens.get(i).getRegex().matcher(s);
				if(this.matcher.find()){

					flag = true;
					this.temp = this.matcher.group().trim();
			    	s = this.matcher.replaceFirst("").trim();
			    	tempLex = new Lexeme(this.temp, tokens.get(i).getType());

					this.lexemes.add(tempLex);
					break;
				}
			}
		} return false;
	}

	public Lexeme parse(String str) {
		/*-------------------------------------------------------------------------------------------------
			Method Description: This method matches the string to the tokens and returns the lexeme.
		-------------------------------------------------------------------------------------------------*/
		str = this.removeQuotes(str);
		for(int i = 0; i < tokens.size(); i++){
			this.matcher = tokens.get(i).getRegex().matcher(str);
			if(this.matcher.find()){
				this.temp = this.matcher.group().trim();
			   	str = this.matcher.replaceFirst("").trim();
			   	return new Lexeme(this.temp, tokens.get(i).getType());
			}
		} return null;
	}

	public String removeQuotes(String str) {
		/*-------------------------------------------------------------------------------------------------
			Method Description: This method removes the strings in a string
		-------------------------------------------------------------------------------------------------*/
		String newString="";
		for (int j=0; j < str.length(); j++) {
			if (str.charAt(j) == '"') continue;
			newString+=str.charAt(j);
		} return newString;
	}


	/****************
	*    Getters    *
	****************/
	public ArrayList<Lexeme> getLexemes(){ return lexemes; }

	/****************
	*    Setters    *
	****************/
	public void reset() {
		this.mark = false;
	}

	public void setRegex() {

		// Code Delimiters
		this.addRegex("HAI", "Code Delimiter");
		this.addRegex("KTHXBYE", "Code Delimiter");

		// Literals
		this.addRegex("-?[0-9]+\\.[0-9]+", "Numbar Literal"); 
		this.addRegex("-?[0-9]+", "Numbr Literal");
		this.addRegex("\"[^\"]+\"", "Yarn Literal");
		this.addRegex("(WIN|FAIL)", "Troof Literal");
		this.addRegex("(TROOF|NUMBR|NUMBAR|YARN|NOOB)", "Type Literal");

		// Comments
		this.addRegex("BTW", "Comments");
		this.addRegex("OBTW", "Multi-line Comment");
		this.addRegex("TLDR", "Multi-line Comment");

		// Variables
		this.addRegex("I\\sHAS\\sA", "Variable Declaration");
		this.addRegex("ITZ", "Variable Assignment");
		this.addRegex("R", "Assignment Operator");

		// Arithmetic Operators
		this.addRegex("SUM\\sOF", "Arithmetic Operator");
		this.addRegex("DIFF\\sOF", "Arithmetic Operator");
		this.addRegex("PRODUKT\\sOF", "Arithmetic Operator");
		this.addRegex("QUOSHUNT\\sOF","Arithmetic Operator");
		this.addRegex("MOD\\sOF", "Arithmetic Operator");
		this.addRegex("BIGGR\\sOF", "Arithmetic Operator");
		this.addRegex("SMALLR\\sOF", "Arithmetic Operator");

		// Boolean Operators
		this.addRegex("NOT", "Boolean Operator");
		this.addRegex("BOTH\\sOF", "Boolean Operator");
		this.addRegex("EITHER\\sOF", "Boolean Operator");
		this.addRegex("WON\\sOF", "Boolean Operator");
		this.addRegex("ANY\\sOF", "Boolean Operator");
		this.addRegex("ALL\\sOF", "Boolean Operator");
		this.addRegex("MKAY", "Boolean Delimiter");

		// Comparison-Boolean Operators
		this.addRegex("BOTH\\sSAEM", "Comparison Operator");
		this.addRegex("DIFFRINT", "Comparison Operator");

		// Other Keywords
		this.addRegex("SMOOSH", "Concatenation");
		this.addRegex("MAEK", "Line Break");
		this.addRegex("AN", "Operation Keyword");
		this.addRegex("IS\\sNOW\\sA", "Type Assignment");  
		this.addRegex("VISIBLE", "Output Keyword"); 
		this.addRegex("GIMMEH", "Input Keyword");

		// If-Then Statements
		this.addRegex("O\\sRLY\\?", "IF-THEN Statement"); 
		this.addRegex("YA\\sRLY", "IF-THEN Statement"); 
		this.addRegex("NO\\sWAI", "IF-THEN Statement"); 
		this.addRegex("OIC", "IF-THEN Statement"); 

		// Switch Case Statements
		this.addRegex("WTF\\?", "SWITCH-CASE Statement"); 
		this.addRegex("OMGWTF", "SWITCH-CASE Statement"); 
		this.addRegex("OMG", "SWITCH-CASE Statement"); 
		this.addRegex("GTFO", "SWITCH-CASE Statement"); 

		// Loop Statements
		this.addRegex("IM\\sIN\\sYR", "Loop");
		this.addRegex("UPPIN", "increment");
		this.addRegex("NERFIN", "decrement");
		this.addRegex("YR", "Loop");
		this.addRegex("TIL", "Loop");
		this.addRegex("WILE", "Loop");
		this.addRegex("IM\\sOUTTA\\sYR", "Loop");

		// Identifiers
		this.addRegex("IT", "Global Variable");
		this.addRegex("[a-zA-Z&&[^AR]][a-zA-Z0-9_]*", "Variable Identifier"); 
		this.addRegex("[a-zA-Z&&[^AR]](\\s?[A_Z])*", "Function Identifier"); 
		this.addRegex("A", "Type Assignment"); 

		// Invalid Statements
		this.addRegex("[^a-zA-Z\\s]+.*", "Invalid Statement");			// ex. 23s
		this.addRegex("[a-zA-Z]+\\W+\\w*?", "Invalid Statement");		// ex. S@turday
	}
	
}
