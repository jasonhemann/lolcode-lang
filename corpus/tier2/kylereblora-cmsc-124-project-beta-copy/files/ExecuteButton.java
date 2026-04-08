
	/*****************************************************************************************
	*  File Description:                                                                     *
	*  This file creates the execute button for the UI.                                      *
	*****************************************************************************************/

//  --------------------------------------------------  [PACKAGE DECLARATION]
	package gui;

//	--------------------------------------------------	[JAVA IMPORTS]
	import java.awt.*;
	import java.awt.event.*;
	import java.util.*;
	import javax.swing.*;
	import javax.swing.event.*;
	import javax.imageio.*;
	import src.*;

//	--------------------------------------------------	[CLASS SPECIFICATION]
public class ExecuteButton extends JButton implements ActionListener {
	
	/***************
	*  Attributes  *
	***************/
		private Boolean hasError;
		private String line;
		private Editor myEditor;
		private Interpreter myInterpreter;
		private LexemeTable myTable;
		private Parser parser;
		private String input;
		private SymbolTable myStorage;
		private Analyzer analyzer;
		private Terminal myTerminal;
		private int lineNumber;
	
	/****************************
	*    Button Constructors    *
	****************************/
	public ExecuteButton(String label, Terminal terminal, Editor editor, LexemeTable table, SymbolTable storage, String url) {
		super(label);		
		this.myEditor = editor;
		this.myTable = table;
		this.myStorage = storage;
		this.myTerminal = terminal;
		this.parser = new Parser(terminal);
		this.analyzer = new Analyzer(terminal);
		this.addActionListener(this);
	}

	/****************
	*    Methods    *
	****************/
	@Override

	public void actionPerformed(ActionEvent ae) {
		
		// resets the table UI
		this.myTable.getModel().setRowCount(0);
		this.myStorage.getModel().setRowCount(0);
		this.analyzer.setParser(this.parser);

		// terminal printing reset
		System.out.println("\n== Initializing LOLCODE Interpreter 2017 ==");
		this.myTerminal.getTextArea().setText("\n == LOLCODE Interpreter (c) PING PONG PANG ==\n");
		if (this.myEditor.getFileName().equals("")) this.myEditor.setFileName("<user_input>");

		// table defaults
		this.parser.reset(); this.analyzer.reset();
		Lexeme noob = new Lexeme(null,"NOOB Literal");
		this.analyzer.getStorage().put(this.analyzer.getIt(),noob);

		// reads editor per line and parses it
		this.lineNumber = 1;
		for (String lineRead : this.myEditor.getTextArea().getText().split("\\n")) {
			
			System.out.println("Executing parser...");
			this.line = lineRead;
			this.parser.getLexemes().clear();
			this.hasError = parser.createLexemes(lineRead);
			if (this.hasError) break;

			// -- syntax analysis and semantic analysis call
			if (!this.analyzer.analyze(this.parser.getLexemes())) break;

			// symbol table print
			this.myStorage.getModel().setRowCount(0);
			Set<Lexeme> keys = analyzer.getStorage().keySet();
			for(Lexeme key : keys){
				this.myStorage.getModel().addRow(new Object[]{key.getRegex(), analyzer.getStorage().get(key).getRegex(), analyzer.getStorage().get(key).getLexType()});
			}

			lineNumber++;
		}

		// program was not closed - missing KTHXBYE statement
		if (this.analyzer.getStatus() == false) {
			this.myTerminal.error(8100, 1);
		}
	}

	/****************
	*    Getters    *
	****************/
	public Analyzer getAnalyzer() {return this.analyzer;}
	public Parser getParser() {return this.parser;}
	public String getLine() {return this.line;}
	public int getLineNumber() {return this.lineNumber;}
}
