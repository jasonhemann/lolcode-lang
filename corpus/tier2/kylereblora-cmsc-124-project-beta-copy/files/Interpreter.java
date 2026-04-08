
	/*****************************************************************************************
	*  File Description:                                                                     *
	*  This file creates the interpreter panel for the UI.                                   *
	*****************************************************************************************/

//  --------------------------------------------------  [PACKAGE DECLARATION]
	package gui;

//	--------------------------------------------------	[JAVA IMPORTS]
	import java.awt.*;
	import javax.swing.border.*;
	import javax.swing.*;
	import gui.*;

//	--------------------------------------------------	[CLASS SPECIFICATION]
public class Interpreter extends JPanel {

	/**************
	*  Constants  *
	**************/
	private static final int MAXIMUM_PANEL_WIDTH = 600;
	private static final int MAXIMUM_PANEL_HEIGHT = MainPanel.getPanelHeight();

	/***************
	*  Attributes  *
	***************/
	
	// Main Panels
		private JLabel titlebar;
		private LexemeTable lexeme;
		private SymbolTable symboltable;

	// Panel - Dividers
		private JPanel topPanel;
		private JPanel bottomPanel;
		private JPanel titlePanel;

	/***************************
	*    Panel Constructors    *
	***************************/
	public Interpreter() {
		this.setComponents();
	}

	/****************
	*    Methods    *
	****************/
	private void setComponents() {

		this.setLayout(new BorderLayout());

		// creating components
		this.topPanel = new JPanel(); this.bottomPanel = new JPanel();	
		this.topPanel.setLayout(new BorderLayout()); this.bottomPanel.setLayout(new BorderLayout());

		this.titlebar = new JLabel("LOL CODE Interpreter");
		this.lexeme = new LexemeTable();
		this.symboltable = new SymbolTable();
		
		// interpreter title bar - setup		
		this.titlebar.setPreferredSize(new Dimension(Interpreter.MAXIMUM_PANEL_WIDTH, Interpreter.MAXIMUM_PANEL_HEIGHT-280));
		this.titlebar.setForeground(Color.WHITE);
		this.titlebar.setFont(new Font("Serif", Font.BOLD, 12));
		this.titlebar.setBorder(new EmptyBorder(0, 15, 10, 0));

		// interpreter title bar container (panel)
		this.titlePanel = new JPanel(); this.titlePanel.setBackground(Color.BLACK);
		this.titlePanel.setPreferredSize(new Dimension(Interpreter.MAXIMUM_PANEL_WIDTH, Interpreter.MAXIMUM_PANEL_HEIGHT-280));
		this.titlePanel.add(this.titlebar);	
		
		// set component position
		this.topPanel.add(this.titlePanel, BorderLayout.CENTER);
		this.bottomPanel.add(this.lexeme, BorderLayout.WEST);
		this.bottomPanel.add(this.symboltable, BorderLayout.EAST);

		this.add(topPanel, BorderLayout.NORTH);
		this.add(bottomPanel, BorderLayout.CENTER);
	}

	/****************
	*    Getters    *
	****************/
	public LexemeTable getTable(){return this.lexeme;}
	public SymbolTable getStorage(){return this.symboltable;}
	public static int getPanelWidth(){return Interpreter.MAXIMUM_PANEL_WIDTH;}
	public static int getPanelHeight(){return Interpreter.MAXIMUM_PANEL_HEIGHT;}

}
