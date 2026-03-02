using System;
using Gtk;
using System.Text.RegularExpressions;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using LolcodeInterpreter;
public partial class MainWindow: Gtk.Window
{
	/*------------------------------------
	 * 
	 * Suggestion: switchColorTheme()
	 * 		-> time constraint
	 * 
	 * ---------------------------------*/
	ListStore lexemeList = new ListStore (typeof(string), typeof(string));
	ListStore symbolList = new ListStore (typeof(string), typeof(string), typeof(string));
	//String colorTheme = "Light";
	public MainWindow () : base (Gtk.WindowType.Toplevel)
	{
		Build ();
		tokenTreeViewInit ();
		symbolTableTreeViewInit ();
		consoleTextViewInit ();
	}


	private void tokenTreeViewInit(){
		tokenTreeView.Model = lexemeList;
		tokenTreeView.AppendColumn ("Lexeme", new CellRendererText (), "text", 0);
		tokenTreeView.AppendColumn ("Description", new CellRendererText (), "text", 1);
	}

	private void symbolTableTreeViewInit(){
		symbolTableTreeView.Model = symbolList;
		symbolTableTreeView.AppendColumn ("Lexeme", new CellRendererText (), "text", 0);
		symbolTableTreeView.AppendColumn ("Type", new CellRendererText (), "text", 1);
		symbolTableTreeView.AppendColumn ("Value", new CellRendererText (), "text", 2);
		//symbolTableTreeView.showAlternatingRowBackgrounds = true;
	}

	private void consoleTextViewInit(){
		consoleTextView.ModifyBase (StateType.Normal, new Gdk.Color(52,57,60));
		consoleTextView.ModifyText (StateType.Normal, new Gdk.Color (141,233,113));
		consoleTextView.Buffer.Text += "lolterpreter@CMSC124:~$ \n";
	}

	public void updateChangesOnSymbolTable(Dictionary<String, Variable> variablesDictionary){
		symbolList.Clear ();
		foreach (KeyValuePair<String, Variable> entry in variablesDictionary) {
			symbolList.AppendValues (entry.Value.getVariableName (), entry.Value.getVariableType(), entry.Value.getVariableValue());
		}
	}

	public void clearTokens(){
		lexemeList.Clear ();
	}

	public void appendTokens(String lex, String desc){
		lexemeList.AppendValues (lex, desc);
	}

	public void updateMessagesOnConsole(String message){
		consoleTextView.Buffer.Text += $"{message}\n";
	}

	public void printOnConsole(String text){
		consoleTextView.Buffer.Text += text;
	}
	protected void OnDeleteEvent (object sender, DeleteEventArgs a)
	{
		Application.Quit ();
		a.RetVal = true;
	}

	private void transferSourceCodeToEditor (object sender, EventArgs e)
	{
		lexemeList.Clear ();
		System.IO.StreamReader fileContents = System.IO.File.OpenText (fileChooser.Filename);
		editorTextView.Buffer.Text = fileContents.ReadToEnd ();
		fileContents.Close ();
	}

	protected void onExecuteButtonClick(object sender, EventArgs e){
		consoleTextView.Buffer.Text = "";
		MainClass.runInterpreter ();
	}
	public void clearConsole(){
		consoleTextView.Buffer.Text = "";
	}

	public String getEditorText(){
		return editorTextView.Buffer.Text;
	}

	// Alpha Version Color Theme - Imp. 1.0
	/*
	protected void switchColorMode (object sender, EventArgs e)
	{
		if (this.colorTheme == "Light") {
			tokenTreeView.ModifyBase (StateType.Normal, new Gdk.Color (52,57,60));
			tokenTreeView.ModifyText (StateType.Normal, new Gdk.Color (255, 255, 255));
			symbolTableTreeView.ModifyBase (StateType.Normal, new Gdk.Color (52, 57, 60));
			symbolTableTreeView.ModifyText (StateType.Normal, new Gdk.Color (255, 255, 255));
			this.colorTheme = "Dark";
		}
	}
	*/
}
