using System;
using System.Collections;
using System.Collections.Generic;
using Gtk;
using Gdk;
using Pango;

namespace ACubeLexer
{
	public partial class InputDialogBox : Gtk.Dialog
	{

		public Gdk.Color setColor(byte intred, byte intgreen, byte intblue)
		{
			byte red = 0;
			byte green = 0;
			byte blue = 0;
			red = (byte) (red + intred);
			green = (byte) (green + intgreen);
			blue = (byte) (blue + intblue);

			return new Gdk.Color(red,green,blue);
		}

		public InputDialogBox (string gimmehVariable, Gtk.Statusbar lexerStatus)
		{
			Build ();

			Gdk.Color textviewColor = setColor (48, 48, 58);
			Gdk.Color headerTextColor = setColor (255, 255, 255);
			Gdk.Color windowColor = setColor (45+25+15, 45+40+15, 48+25+15);
			Gdk.Color statusColor = setColor (37,37,38);

			Gdk.Color whiteColor = setColor (180, 180, 180);
			Gdk.Color blackColor = setColor (000, 000, 000);

			this.ModifyBg (StateType.Normal, windowColor);
			this.HeightRequest = 80;

			label1.ModifyFg (StateType.Normal, headerTextColor);
			variableLabel.ModifyFg (StateType.Normal, headerTextColor);
			inputField.ModifyBase (StateType.Normal, textviewColor);
			inputField.ModifyText (StateType.Normal, whiteColor);

			variableLabel.Text = gimmehVariable;
		}

		protected void OnButtonOkClicked (object sender, EventArgs e)
		{
			Respond (Gtk.ResponseType.Ok);
		}

		protected void OnButtonCancelClicked (object sender, EventArgs e)
		{
			inputField.Text = "";
			Respond (Gtk.ResponseType.Cancel);
		}

		public string retEvalVal (){
			return inputField.Text;
		}
	}
}

