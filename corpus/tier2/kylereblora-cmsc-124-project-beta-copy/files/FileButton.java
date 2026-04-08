
	/*****************************************************************************************
	*  File Description:                                                                     *
	*  This file creates the file chooser for the UI.                                        *
	*****************************************************************************************/

//  --------------------------------------------------  [PACKAGE DECLARATION]
	package gui;

//  --------------------------------------------------  [JAVA IMPORTS]
	import java.awt.*;
	import java.awt.event.*;
	import java.io.*;
	import javax.swing.*;
	import javax.swing.event.*;
	import javax.swing.filechooser.*;

//	--------------------------------------------------	[CLASS SPECIFICATION]
public class FileButton extends JLabel implements MouseListener {

	/***************
	*  Attributes  *
	***************/

	// Class Instance Attributes
		private Editor myEditor;
		private FileNameExtensionFilter filter;
		private JFileChooser chooser;
		private String label;

	// File Reading Attributes
		private FileReader fr;
		private BufferedReader br;
		private String str;
	
	/***************************
	*    Label Constructors    *
	***************************/
	public FileButton(String label, Editor editor) {
		
		super(label);
		this.myEditor = editor;		
		this.addMouseListener(this);
		
		// set default design
		this.setOpaque(true);		
		this.setBackground(Color.BLACK);
		this.setForeground(Color.WHITE);
		this.setBorder(BorderFactory.createLineBorder(Color.GRAY));

		// file chooser creation
		this.filter = new FileNameExtensionFilter("LOL Files", "lol");
		this.chooser = new JFileChooser(FileSystemView.getFileSystemView().getHomeDirectory());		
		this.chooser.setFileFilter(this.filter);
		this.fr = null;
		this.br = null;
		this.str = null;

	}

	/****************
	*    Methods    *
	****************/
	@Override
	public void mousePressed(MouseEvent e) {
		this.setBackground(Color.WHITE);
		this.setForeground(Color.BLACK);
		this.setBorder(BorderFactory.createLineBorder(Color.BLACK));
	}

    public void mouseReleased(MouseEvent e) {
		this.setBackground(Color.BLACK);
		this.setForeground(Color.WHITE);
		this.setBorder(BorderFactory.createLineBorder(Color.GRAY));
	}

    public void mouseEntered(MouseEvent e) {
		this.setBackground(Color.GRAY);
		this.setForeground(Color.WHITE);
		this.setBorder(BorderFactory.createLineBorder(Color.BLACK));
	}

    public void mouseExited(MouseEvent e) {
		this.setBackground(Color.BLACK);
		this.setForeground(Color.WHITE);
		this.setBorder(BorderFactory.createLineBorder(Color.GRAY));
	}

    public void mouseClicked(MouseEvent e) {
		this.setBackground(Color.GRAY);
		this.setForeground(Color.WHITE);
		this.setBorder(BorderFactory.createLineBorder(Color.BLACK));

		// ------------------------------------- Method: Choosing the file -------------------------------------------------
		int returnValue = this.chooser.showOpenDialog(null);

		if (returnValue == JFileChooser.APPROVE_OPTION) {

			String filename = this.chooser.getSelectedFile().getName();
			String extension = filename.substring(filename.lastIndexOf(".") + 1, filename.length());
			String lolext = "lol";

			if (!lolext.equals(extension)) {
				JOptionPane.showMessageDialog(null, "Choose a lol file! LOL.");
			}

			else {

				JOptionPane.showMessageDialog(null, "Upload Successful!");
				File selectedFile = this.chooser.getSelectedFile();
				this.myEditor.setFileName(selectedFile.getName());

				try{

					this.fr = new FileReader(selectedFile.getAbsolutePath());
					this.br = new BufferedReader(fr);
					String currentline = br.readLine();

					this.myEditor.getTextArea().setText("");

					while(currentline != null){
						this.myEditor.getTextArea().append(currentline);
						this.myEditor.getTextArea().append("\n");
			 			currentline = this.br.readLine();
				 	}

			 		this.fr.close();
				 	this.br.close();

				} catch (IOException f) { f.printStackTrace();}
			}
		// -----------------------------------------------------------------------------------------------------------------
		}
	}

}
