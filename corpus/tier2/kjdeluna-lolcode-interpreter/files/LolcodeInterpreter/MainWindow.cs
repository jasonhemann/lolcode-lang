using System;
using Gtk;
using System.Text.RegularExpressions;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using LolcodeInterpreter;
public partial class MainWindow: Gtk.Window
{
	ListStore lexemeList = new ListStore (typeof(string), typeof(string));
	ListStore symbolList = new ListStore (typeof(string), typeof(string));

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
	}

	private void consoleTextViewInit(){
		consoleTextView.ModifyBase (StateType.Normal, new Gdk.Color(52,57,60));
		consoleTextView.ModifyText (StateType.Normal, new Gdk.Color (141,233,113));
	}

	public void updateChangesOnSymbolTable(Dictionary<String, String> dict){
		symbolList.Clear ();
	}

	public void clearTokens(){
		lexemeList.Clear ();
	}

	public void appendTokens(String lex, String desc){
		lexemeList.AppendValues (lex, desc);
	}

	public void updateMessagesOnConsole(String message, int lineCount){
		consoleTextView.Buffer.Text = consoleTextView.Buffer.Text +$"Line {lineCount}: {message}\n";
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

	public String getEditorText(){
		return editorTextView.Buffer.Text;
	}

		
}
