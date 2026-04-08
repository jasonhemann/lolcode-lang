
	/*****************************************************************************************
	*  File Description:                                                                     *
	*  This file creates the Editor panel for the UI.                                        *
	*****************************************************************************************/

//  --------------------------------------------------  [PACKAGE DECLARATION]
	package gui;

//	--------------------------------------------------	[JAVA IMPORTS]	
	import java.awt.*;
	import java.awt.event.*;
	import javax.swing.*;
	import javax.swing.border.*;

//	--------------------------------------------------	[CLASS SPECIFICATION]
public class Editor extends JPanel {

	/**************
	*  Constants  *
	**************/
	private static final int MAXIMUM_PANEL_WIDTH = 400;
	private static final int MAXIMUM_PANEL_HEIGHT = MainPanel.getPanelHeight();
	private static final int TEXT_AREA_WIDTH = 17;
	private static final int TEXT_AREA_HEIGHT = 33;

	/***************
	*  Attributes  *
	***************/

	// Panel Components
		private FileButton fileButton;
		private JTextArea fileName;
		private JTextArea textArea;
		private JScrollPane textScroll;

	// Panel - Dividers	
		private JPanel topPanel;
		private JPanel bottomPanel;
		private JPanel rightPanel;
		private JPanel leftPanel;

	/***************************
	*    Panel Constructors    *
	***************************/
	public Editor() {
		this.setComponents();
	}

	/****************
	*    Methods    *
	****************/
	private void setComponents() {

		// set panel defaults
		
			// set panel size
			this.setPreferredSize(new Dimension(Editor.MAXIMUM_PANEL_WIDTH, Editor.MAXIMUM_PANEL_HEIGHT));

			// set panel layout
			this.setLayout(new BorderLayout());

		// creating components
		this.topPanel = new JPanel();
		this.bottomPanel = new JPanel();
		this.leftPanel = new JPanel();
		this.rightPanel = new JPanel();
		
		// top panel: creating the file chooser
		this.topPanel.setBorder(BorderFactory.createEmptyBorder(0,5,0,0)); 
		this.fileName = new JTextArea();
		this.fileName.setPreferredSize(new Dimension(280,20));
		this.fileName.setEditable(false);
		this.fileButton = new FileButton("Choose File", this);

		// bottom: creating text area with scrollbar
		this.textArea = new JTextArea(Editor.TEXT_AREA_WIDTH, Editor.TEXT_AREA_HEIGHT);
        this.textArea.setEditable(true);
        this.textScroll = new JScrollPane(this.textArea);
        this.textScroll.setVerticalScrollBarPolicy(ScrollPaneConstants.VERTICAL_SCROLLBAR_ALWAYS);

		// modifying component size & layout
		this.topPanel.setLayout(new BorderLayout());
		this.topPanel.setPreferredSize(new Dimension(Editor.MAXIMUM_PANEL_WIDTH, Editor.MAXIMUM_PANEL_HEIGHT-275));
		this.bottomPanel.setPreferredSize(new Dimension(Editor.MAXIMUM_PANEL_WIDTH, Editor.MAXIMUM_PANEL_HEIGHT-35));
		
		// set components - top panel
		this.leftPanel.add(this.fileName, BorderLayout.CENTER);
		this.rightPanel.add(this.fileButton, BorderLayout.CENTER);
		this.topPanel.add(this.leftPanel, BorderLayout.WEST);
		this.topPanel.add(this.rightPanel, BorderLayout.CENTER);

		// set components position - editor
		this.bottomPanel.add(this.textScroll, BorderLayout.CENTER);
		this.add(this.topPanel, BorderLayout.NORTH);
		this.add(this.bottomPanel, BorderLayout.CENTER);
	}	

	/****************
	*    Getters    *
	****************/
	public FileButton getFileButton(){return this.fileButton;}
	public JTextArea getTextArea(){return this.textArea;}
	public JScrollPane getTextScroll(){return this.textScroll;}
	public JPanel getLeftPanel(){return this.leftPanel;}
	public JPanel getRightPanel(){return this.rightPanel;}
	public JPanel getTopPanel(){return this.topPanel;}
	public JPanel getBottomPanel(){return this.bottomPanel;}
	public String getFileName(){return this.fileName.getText();}
	public static int getPanelWidth(){return Editor.MAXIMUM_PANEL_WIDTH;}
	public static int getPanelHeight(){return Editor.MAXIMUM_PANEL_HEIGHT;}

	/****************
	*    Setters    *
	****************/
	public void setFileName(String input){this.fileName.setText(input);}
}
