
	/*****************************************************************************************
	*  File Description:                                                                     *
	*  This file creates the division panel for the UI.                                      *
	*****************************************************************************************/

//  --------------------------------------------------  [PACKAGE DECLARATION]
	package gui;

//	--------------------------------------------------	[JAVA IMPORTS]	
	import java.awt.BorderLayout;
	import java.awt.Color;
	import java.awt.Dimension;
	import javax.swing.JPanel;

//	--------------------------------------------------	[CLASS SPECIFICATION]
public class MainPanel extends JPanel {

	/***************
	*   Constants  *
	***************/
	private static final int MAXIMUM_WINDOW_HEIGHT = MyFrame.getFrameHeight()/2;
	private static final int MAXIMUM_WINDOW_WIDTH = MyFrame.getFrameWidth();

	/***************
	*  Attributes  *
	***************/
		
	// Main Panels
		private Editor editor;
		private Interpreter interpreter;
		private Terminal terminal;

	// Panel - Dividers
		private JPanel topPanel;
		private JPanel bottomPanel;

	/***************************
	*    Panel Constructors    *
	***************************/
	public MainPanel() {
		this.setLayout(new BorderLayout());
		this.setComponents();
	}
	
	/****************
	*    Methods    *
	****************/
	private void setComponents() {

		// creating components
		this.editor = new Editor();
		this.interpreter = new Interpreter();
		this.terminal = new Terminal(this.editor, this.interpreter);

		this.topPanel = new JPanel();
		this.bottomPanel = new JPanel();
		
		// set panel size - vertical
		this.topPanel.setLayout(new BorderLayout());
		this.topPanel.setPreferredSize(new Dimension(MainPanel.MAXIMUM_WINDOW_WIDTH, MainPanel.MAXIMUM_WINDOW_HEIGHT));
		this.bottomPanel.setPreferredSize(new Dimension(MainPanel.MAXIMUM_WINDOW_WIDTH, MainPanel.MAXIMUM_WINDOW_HEIGHT));

		// set component position - top
		this.topPanel.add(this.editor, BorderLayout.WEST);
		this.topPanel.add(this.interpreter, BorderLayout.CENTER);


		// set component position - bottom
		this.bottomPanel.add(this.terminal, BorderLayout.CENTER);

		// set component position - window
		this.add(this.topPanel,BorderLayout.NORTH);
		this.add(this.bottomPanel,BorderLayout.CENTER);



	}

	/****************
	*    Getters    *
	****************/
	public Editor getEditor(){return this.editor;}
	public Interpreter getInterpreter(){return this.interpreter;}
	public Terminal getTerminal(){return this.terminal;}
	public JPanel getTopPanel(){return this.topPanel;}
	public JPanel getBotPanel(){return this.bottomPanel;}
	public static int getPanelWidth(){return MainPanel.MAXIMUM_WINDOW_WIDTH;}
	public static int getPanelHeight(){return MainPanel.MAXIMUM_WINDOW_HEIGHT;}

}
