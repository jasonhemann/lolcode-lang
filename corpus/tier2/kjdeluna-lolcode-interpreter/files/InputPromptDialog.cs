using System;
using LolcodeInterpreter;
using System.Text.RegularExpressions;
namespace LolcodeInterpreter
{
	public partial class InputPromptDialog : Gtk.Dialog
	{
		private String receivedText;
			public InputPromptDialog ()
		{
			this.Build ();
		}



		protected void okButtonOnClick  (object sender, EventArgs e)
		{
			this.receivedText = inputEntry.Text;
			this.Destroy ();
			//Console.WriteLine ($"{receiver}");
			
		}
		public String getReceivedText(){
			return this.receivedText;
		}

	}
}

/*
 * 
 * 				Token scannedVar = (Token)tokensArrayList [currentPosition - 1];
				this.addVariable (scannedVar.getLexeme (), checkLiteralType (prompt.getReceivedText ()), prompt.getReceivedText ());
				MainClass.win.updateChangesOnSymbolTable(this.variablesDictionary);*/