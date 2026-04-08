
	/*****************************************************************************************
	*  File Description:                                                                     *
	*  This file creates the terminal panel for the UI.                                      *
	*****************************************************************************************/

//  --------------------------------------------------  [PACKAGE DECLARATION]
	package gui;

//	--------------------------------------------------	[JAVA IMPORTS]
	import java.awt.*;
	import java.awt.event.*;
	import javax.swing.*;

//	--------------------------------------------------	[CLASS SPECIFICATION]
public class Terminal extends JPanel {

	/**************
	*  Constants  *
	**************/
	private static final int MAXIMUM_PANEL_WIDTH = MainPanel.getPanelWidth();
	private static final int MAXIMUM_PANEL_HEIGHT = MainPanel.getPanelHeight();

	/***************
	*  Attributes  *
	***************/
		private Editor editor;
		private ExecuteButton executeButton;		
		private Interpreter interpreter;
		private JPanel textPanel;
		private JTextArea textArea;
		private JScrollPane textScroll;
		private String textInput;

	/***************************
	*    Panel Constructors    *
	***************************/
	public Terminal(Editor editor, Interpreter interpreter) {
		this.interpreter = interpreter;
		this.editor = editor;
		this.setLayout(new BorderLayout());
		this.setComponents();
	}

	/****************
	*    Methods    *
	****************/
	private void setComponents() {
		
		this.setPreferredSize(new Dimension(Terminal.MAXIMUM_PANEL_WIDTH, Terminal.MAXIMUM_PANEL_HEIGHT));

		// Execute Button Initialization		
		this.executeButton = new ExecuteButton("EXECUTE", this, this.editor, this.interpreter.getTable(), this.interpreter.getStorage(),"images/executebubble.png");
		this.textPanel = new JPanel();

		// creating text area
		this.textArea = new JTextArea(17,88);
		this.textArea.setBackground(Color.BLACK);
		this.textArea.setForeground(Color.GREEN);		
		this.textArea.setText("\n == LOLCODE Interpreter (c) PING PONG PANG ==\n");
        this.textArea.setEditable(false);
        this.textScroll = new JScrollPane(this.textArea);		
        this.textScroll.setVerticalScrollBarPolicy(ScrollPaneConstants.VERTICAL_SCROLLBAR_ALWAYS);

		// execute button initialization
		this.executeButton.setPreferredSize(new Dimension(Terminal.getPanelWidth(),Terminal.getPanelHeight()-280));

		// setting component position
		this.textPanel.add(this.textScroll);
		this.add(this.executeButton, BorderLayout.NORTH);
		this.add(this.textPanel, BorderLayout.CENTER);
	}

	/****************
	*    Methods    *
	****************/
	public void error(int code, int type) {

		String errorDescription=""; String errorType="";
		if (code>=8000) {
			errorType = "SyntaxError :: ";
			switch(code%8000) {
				case 0: errorDescription = "invalid re-initialization of program :: HAI statement found after KTHXBYE\n"; break;
				case 1: errorDescription = "invalid termination of program :: KTHXBYE statement found after KTHXBYE\n"; break;
				case 3: errorDescription = "invalid statements found :: no statements allowed before HAI statement\n"; break;
				case 4: errorDescription = "invalid statements found :: no statements allowed after KTHXBYE statement\n"; break;
				case 5: errorDescription = "invalid HAI statement found :: found HAI duplicate\n"; break;
				case 6: errorDescription = "invalid declaration of variable :: IT variable cannot be declared\n"; break;
				case 7: errorDescription = "invalid termination of comment :: TLDR statement found :: missing OBTW\n"; break;
				case 8: errorDescription = "invalid expression :: AN statement found :: missing operation\n"; break;
				case 50: errorDescription = "invalid statements found :: multiple statements not allowed\n"; break;
				case 100: errorDescription = "reached end of file while parsing :: missing code delimiter\n"; break;
				case 101: errorDescription = "expected HAI statement :: missing code delimiter\n"; break;
				case 102: errorDescription = "invalid use of variable declaration :: missing variable identifier\n"; break;
				case 103: errorDescription = "invalid use of variable declaration :: expected value after variable declaration ITZ\n"; break;
				case 104: errorDescription = "variable "+ this.executeButton.getAnalyzer().getLexemes().get(this.executeButton.getAnalyzer().getCurrent()).getRegex() +" is not defined\n"; break;
				case 105: errorDescription = "invalid use of assignment operator :: no variable found before operator\n"; break;
				case 106: errorDescription = "invalid use of assignment operator  :: no value found after operator \n"; break;
				case 107: errorDescription = "invalid binary operation :: missing AN statement \n"; break;
				case 108: errorDescription = "invalid binary operation :: missing operand \n"; break;
				case 109: errorDescription = "invalid input operation :: expected operand after GIMMEH\n"; break;
				case 110: errorDescription = "invalid boolean operation :: missing operand\n"; break;
				case 111: errorDescription = "invalid boolean operation :: missing AN statement\n"; break;
				case 200: errorDescription = "invalid use of variable declaration :: invalid value after variable assignment \n"; break;
				case 202: errorDescription = "invalid use of variable declaration :: found statement not ITZ\n"; break;
				case 203: errorDescription = "invalid use of variable declaration :: invalid argument\n"; break;
				case 300: errorDescription = "invalid use of output keyword :: statements found before 'VISIBLE' keyword\n"; break;
				case 600: errorDescription = "invalid use of SMOOSH function :: invalid start\n"; break;
				case 601: errorDescription = "invalid use of SMOOSH function :: expected values after\n"; break;
				case 602: errorDescription = "invalid use of SMOOSH function :: invalid arguments\n"; break;
				case 700: errorDescription = "invalid use of boolean operation :: invalid arguments\n"; break;
				case 701: errorDescription = "invalid use of boolean operation :: missing MKAY statement\n"; break;
				default: break;
			}

		} else if (code >= 6000) {
			errorType = "SemanticError :: ";
			switch(code%6000) {
				case 100: errorDescription = "invalid arithmetic operation :: invalid data types\n"; break;
				default: break;
			}


		} else if (code >= 3000) {
			errorType = "LexicalError :: ";
			switch(code%3000) {
				case 0: errorDescription = "invalid statement :: input does not match with any pattern\n";
				default: break;
			}
		}

		// error printing
		this.textArea.append("\n Traceback (most recent call last)--");
		if (type == 2) {
			this.textArea.append("\n          File '"+ this.editor.getFileName() +"', in line " + this.executeButton.getLineNumber() + ", from <Editor.java> class");
			this.textArea.append("\n\t" + this.executeButton.getLine() + "          < - - check this line (>D<) lol iyaq ka na haha");
		}
		this.textArea.append("\n\n          [ ERROR "+ code +" ] "+ errorType + errorDescription);
	}

	public void print(String value) {
		this.textArea.append(' ' + value);
	}

	/****************
	*    Getters    *
	****************/
	public JTextArea getTextArea() {return this.textArea;}
	public ExecuteButton getButton() {return this.executeButton;}
	public Editor getEditor() {return this.editor;}
	public Interpreter getInterpreter() {return this.interpreter;}
	public ExecuteButton getExecuteButton() {return this.executeButton;}
	public static int getPanelWidth(){return Terminal.MAXIMUM_PANEL_WIDTH;}
	public static int getPanelHeight(){return Terminal.MAXIMUM_PANEL_HEIGHT;}

	/****************
	*    Setters    *
	****************/
	public void setTextArea(String s) {this.textArea.append(s);}
}
