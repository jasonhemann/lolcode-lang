using System;

namespace LolcodeInterpreter
{
	public partial class InputPromptDialog : Gtk.Dialog
	{
		String receiver;
		public InputPromptDialog ()
		{
			this.Build ();
		}

		protected void okButtonOnClick (object sender, EventArgs e)
		{
			receiver = inputEntry.Text;
			this.Destroy ();
			Console.WriteLine ($"{receiver}");
		}
	}
}

