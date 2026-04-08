
	/*****************************************************************************************
	*  File Description:                                                                     *
	*  This file creates the window panel for the UI.                                        *
	*****************************************************************************************/

//  --------------------------------------------------  [PACKAGE DECLARATION]
	package gui;
	
//	--------------------------------------------------	[JAVA IMPORTS]
	import gui.*;
	import java.awt.*;
	import java.awt.event.*;
	import javax.swing.*;

//  --------------------------------------------------  [CLASS SPECIFICATION]
public class MyFrame extends JFrame {

	/**************
	*  Constants  *
	**************/
	private static final int MAXIMUM_WINDOW_WIDTH = 1000;
	private static final int MAXIMUM_WINDOW_HEIGHT = 600;


	/*************************
	*  MyFrame Constructors  *
	*************************/
	public MyFrame(){

		super("Ang Ganda ni Maam Kat LOLTERPRETER");										//	TITLE for window
		this.setPreferredSize(new Dimension(MAXIMUM_WINDOW_WIDTH,MAXIMUM_WINDOW_HEIGHT));	//	sets window size
		this.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);								//	close program on X bar
		this.setResizable(false);															//	set window size - constant

		JFrame frame = this;

		frame.addComponentListener(new ComponentAdapter() {
            @Override
            public void componentResized(ComponentEvent e) {
                titleAlign(frame);
            }
        });

		Container container = this.getContentPane();
		container.add(new MainPanel(),BorderLayout.CENTER);

		this.pack();																		// packs the components
		this.setLocationRelativeTo(null);													// centers the window
		this.setVisible(true);																// show window
	}

	/************
	*  Methods  *
	************/

	private void titleAlign(JFrame frame) {
		/****************************************************************************
		*	Method Description                                                      *
		*	The method is used to center the title of the window in the title bar.  *
		****************************************************************************/
        Font font = frame.getFont();
        String currentTitle = frame.getTitle().trim();
        FontMetrics fm = frame.getFontMetrics(font);
        int frameWidth = frame.getWidth();
        int titleWidth = fm.stringWidth(currentTitle);
        int spaceWidth = fm.stringWidth(" ");
        int centerPos = (frameWidth / 2) - (titleWidth / 2);
        int spaceCount = centerPos / spaceWidth;
        String pad = "";
        pad = String.format("%" + (spaceCount - 14) + "s", pad);
        frame.setTitle(pad + currentTitle);
    }

	/************
	*  Getters  *
	************/
	public static int getFrameWidth() {return MyFrame.MAXIMUM_WINDOW_WIDTH;}
	public static int getFrameHeight() {return MyFrame.MAXIMUM_WINDOW_HEIGHT;}
}

