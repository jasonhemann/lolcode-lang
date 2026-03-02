package backend;

import java.io.File;
import java.util.ArrayList;
import java.util.Scanner;

public class Lexer {
	private File file;
	private String strFile;
	private ArrayList<String> lexemes;
	private int position;

	//	Lexer can be  initialized by either a File or a String
	public Lexer(File file) {
		this.file = file;
		this.position = 0;
		this.lexemes = new ArrayList<String>();
		
		parseFile();
		fixLexemes();
	}
	
	public Lexer(String strFile) {
		this.strFile = strFile;
		this.position = 0;
		this.lexemes = new ArrayList<String>();
		
		parseStrFile();
		fixLexemes();
	}

	//	Read the file to popular the ArrayList lexemes
	private void parseFile() {
		try {
			Scanner sc = new Scanner(file);
			//	Read file line by line
			while (sc.hasNextLine()) {
				String curLine = sc.nextLine();
				
				//	Extract words/digits in the current line
				for (String i : curLine.split("")) {
					lexemes.add(i);
				}
				
				//	Append a "\n" lexeme to symbolize that the current line has ended
				if (sc.hasNextLine())
					lexemes.add("\n");
			}
			
			sc.close();

		} catch (Exception e) {
			e.printStackTrace();
		}

	}
	
	//	Read the String to populate the ArrayList lexemes
	private void parseStrFile() {
		int counter = 0;
		
		//	Evaluate the string line by line
		for (String i : strFile.split("\n")) {
			//	Append \n to the end of the every line except the first and last line and empty lines
			if (counter++ > 0) {
				lexemes.add("\n");
			}
			
			//	Split the current line to individual characters
			for (String j : i.split("")) {
				lexemes.add(j);
			}

		}
	}
	
	//	"fix" the ArrayList lexemes because its only characters
	private void fixLexemes() {
		ArrayList<String> fixedList = new ArrayList<String>();
		String newLexeme = new String();
		String currentString;
		boolean insideQuote = false;
		
		for (int i = 0; i < lexemes.size(); i++) {
			currentString = lexemes.get(i);
			
			//	If current chracter isn't whitespace, quote or a colon
			if (currentString.matches("[^\s\t\"\n:,]")) {
				newLexeme += currentString;
				
			} else if (i + 1 < lexemes.size() && (currentString + lexemes.get(i + 1)).matches(":[\\)>o\":]")) {
				if (!newLexeme.isBlank()) {
					fixedList.add(newLexeme);
					newLexeme = new String();
				}
				
				
				fixedList.add(currentString + lexemes.get(i + 1));
				i++;
				
			} else {
				//	Reached whitespace; append the word to the new ArrayList 
				if (!newLexeme.isBlank()) {
					fixedList.add(newLexeme);
					newLexeme = new String();
				} 
				
				if (currentString.matches("\"")) insideQuote = !insideQuote;
				if (currentString == "\n" && insideQuote) insideQuote = false;
				
				//	Add the newline or quotation mark
				if (!currentString.isBlank() || insideQuote) {
					fixedList.add(currentString);
				} else if (currentString == "\n") {
					fixedList.add(currentString);
				}
			}
		}
		
		
		//	Append the last word built 
		if (!newLexeme.isBlank()) fixedList.add(newLexeme);
		lexemes = fixedList;
	}

	private void next() {
		position++;
	}
	
	//	Look at the lexeme given an offset based on current position
	private String peek(int offset) {
		//	return last lexeme if position + offset is beyond the ArrayList of lexemes 
		if (position + offset >= lexemes.size()) return lexemes.get(position);
		
		return lexemes.get(position + offset);
	}

	private String currentLexeme() {
		return peek(0);
	}

	//	Get next token from the list of lexemes
	public Token nextToken() {
		String lexeme = new String();
		
		//	Check if current position of the lexer has exceeded the number of lexemes
		if (position >= lexemes.size()) {
		    return new Token(TokenKind.eofToken, "\0", position);
		}
		
		//	Peek at the next 3 lexemes and check if it matches the only 4 word keyword token, functionEndToken
		lexeme = currentLexeme() + " " + peek(1) + " " + peek(2) + " " + peek(3);
		if (lexeme.matches(TokenKind.functionEndToken.getRegex())) {
			position = position + 4;
			return new Token(TokenKind.functionEndToken, lexeme, position - 4);
		}
		
		for (TokenKind kind : TokenKind.values()) {
			//	Peek at the next 2 lexemes and check if it matches a 3 word keyword
			lexeme = currentLexeme() + " " + peek(1) + " " + peek(2);
			if (kind.getLength() == 3 && lexeme.matches(kind.getRegex())) {
				position = position + 3;
				return new Token(kind, lexeme, position - 3);
			}
			
			//	Peek at the next lexeme and check if it matches a 2 word keyword
			lexeme = currentLexeme() + " " + peek(1);
			if (kind.getLength() == 2 && lexeme.matches(kind.getRegex())) {
				position = position + 2;
				return new Token(kind, lexeme, position - 2);
			}
			
			//	Check if current lexeme matches a 1 word keyword
			lexeme = currentLexeme();
			if (kind.getLength() == 1 && lexeme.matches(kind.getRegex())) {
				return new Token(kind, lexeme, position++);
			} 
		}
		
		//	Lexeme did not match any of the regex of Token types
		return new Token(TokenKind.badToken, currentLexeme(), position++);
	}

	public void viewLexemes() {
		int count = 0;
		for (String i : lexemes)
			System.out.println("Lexeme #" + ++count + ":" + i);
	}

}
