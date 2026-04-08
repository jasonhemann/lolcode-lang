using System;
using System.IO;
using System.Collections;
using System.Collections.Generic;
using System.Text.RegularExpressions;
using System.Linq;
using Gtk;

using Pango;

using ACubeLexer;

public partial class MainWindow: Gtk.Window
{

	public Gdk.Color setColor(byte intred, byte intgreen, byte intblue)
	{ // function that will return color values using RGB
		byte red = 0;
		byte green = 0;
		byte blue = 0;
		red = (byte) (red + intred);
		green = (byte) (green + intgreen);
		blue = (byte) (blue + intblue);

		return new Gdk.Color(red,green,blue);
	}

	public MainWindow () : base (Gtk.WindowType.Toplevel)
	{
		Build ();

		// set UI for the whole application
		Gdk.Color textviewColor = setColor (48, 48, 58);
		Gdk.Color headerTextColor = setColor (255, 255, 255);
		Gdk.Color windowColor = setColor (45+25+15, 45+40+15, 48+25+15);
		Gdk.Color statusColor = setColor (37,37,38);

		Gdk.Color whiteColor = setColor (180, 180, 180);
		Gdk.Color blackColor = setColor (000, 000, 000);

		this.AppPaintable = true;
		this.ModifyBg(StateType.Normal, windowColor);
		this.Opacity = 0.99;

		// logo
		Gtk.Image img = new Gtk.Image("sample.jpg");
		var buffer = System.IO.File.ReadAllBytes ("../../acube_logo.png");
		var pixbuf = new Gdk.Pixbuf (buffer);
		img.Pixbuf = pixbuf;
		imageContainer.Add (img);
		imageContainer.ShowAll ();

		inputWindow.WidthRequest = 250;
		inputWindow.HeightRequest = 120;
		lexemeWindow.WidthRequest = 400;
		symbolTableWindow.WidthRequest = 400;
		lexemeWindow.HeightRequest = 120;
		symbolTableWindow.HeightRequest = 120;
		consoleField.HeightRequest = 100;

		inputWindow.ModifyBase (StateType.Normal, textviewColor);
		inputWindow.ModifyFont (FontDescription.FromString("Consolas 10"));
		inputWindow.ModifyText (StateType.Normal, setColor(100,255,100));
		inputWindow.PixelsAboveLines = 2;
		inputWindow.PixelsBelowLines = 2;
		inputWindow.LeftMargin = 5;
		inputWindow.RightMargin = 5;
		inputWindow.ModifyCursor (setColor(255,255,255), setColor(0,0,0));

		FontDescription windowHeader = FontDescription.FromString ("Roboto 20");
		headerLabel.LabelProp = "CMSC124.LOLCode.Interpreter.Initialize( );";
		headerLabel.ModifyFont (windowHeader);
		headerLabel.Selectable = false;
		headerLabel.Justify = Justification.Left;

		FontDescription tableHeader = FontDescription.FromString ("Roboto 12 bold");

		inputLabel.LabelProp = "Input";
		lexemeLabel.LabelProp = "Lexeme Table";
		symbolTableLabel.LabelProp = "Symbol Table";

		inputLabel.ModifyFont(tableHeader);
		lexemeLabel.ModifyFont(tableHeader);
		symbolTableLabel.ModifyFont(tableHeader);

		headerLabel.ModifyFg (StateType.Normal, headerTextColor);
		inputLabel.ModifyFg (StateType.Normal, headerTextColor);
		lexemeLabel.ModifyFg (StateType.Normal, headerTextColor);
		symbolTableLabel.ModifyFg (StateType.Normal, headerTextColor);
		consoleLabel.ModifyFg (StateType.Normal, headerTextColor);

		consoleField.AppPaintable = true;

		consoleField.ModifyBase (StateType.Normal, setColor(30,30,30));
		consoleField.ModifyFont (FontDescription.FromString("Consolas 10"));
		consoleField.ModifyText (StateType.Normal, setColor(220,200,80));
		consoleField.PixelsAboveLines = 2;
		consoleField.PixelsBelowLines = 2;
		consoleField.LeftMargin = 5;
		consoleField.RightMargin = 5;
		consoleField.Editable = false;

		consoleEntry.ModifyBase (StateType.Normal, textviewColor);
		consoleEntry.ModifyText (StateType.Normal, whiteColor);

		consoleField.Buffer.Text += "> " + "Hello user!" + "\n";

		lexemeTree.ModifyBase (StateType.Normal, textviewColor);
		symbolTableTree.ModifyBase (StateType.Normal, textviewColor);

		fileButton.ModifyBg(StateType.Normal, setColor(0,0,255));
		fileButton.ModifyBase(StateType.Normal, setColor(0,0,255));
		fileButton.ModifyFg (StateType.Normal, setColor(0,0,255));

		lexerStatus.ModifyBase (StateType.Normal, statusColor);
		var contextId = this.lexerStatus.GetContextId ("clicked");
		lexerStatus.Push (contextId, "ACube Interpreter Initialized");

		creditsStatus.ModifyBase (StateType.Normal, statusColor);
		contextId = this.lexerStatus.GetContextId ("clicked");
		creditsStatus.Push (contextId, "Interpreter by Mendoza, Montoya and Tomagos");
	}

	protected void OnDeleteEvent (object sender, DeleteEventArgs a)
	{
		Application.Quit ();
		a.RetVal = true;
	}

	protected void OnExecuteButtonClicked (object sender, EventArgs e)
	{
		// for error checking
		var errorFlag = false;
		var errorMessage = "";
		var errorSource = "";
		String express = null;

		Gdk.Color tableColor = setColor (48, 48, 58);
		Gdk.Color tableTextColor = setColor (180, 180, 180);

		// lexeme table view
		lexemeTree.Destroy();
		lexemeTree = new Gtk.TreeView ();
		lexemeTree.ModifyBase (StateType.Normal, tableColor);
		lexemeTree.ModifyText(StateType.Normal, tableTextColor);
		lexemeWindow.Add (lexemeTree);

		Gtk.TreeViewColumn lexemeColumn = new Gtk.TreeViewColumn ();
		lexemeColumn.Title = "Lexeme";

		Gtk.TreeViewColumn classificationColumn = new Gtk.TreeViewColumn ();
		classificationColumn.Title = "Classification";

		lexemeTree.AppendColumn (lexemeColumn);
		lexemeTree.AppendColumn (classificationColumn);

		// lexeme cell!
		Gtk.CellRendererText lexemeNameCell = new Gtk.CellRendererText();
		lexemeColumn.PackStart(lexemeNameCell, true);

		Gtk.CellRendererText classificationNameCell = new Gtk.CellRendererText ();
		classificationColumn.PackStart (classificationNameCell, true);

		lexemeColumn.AddAttribute (lexemeNameCell, "text", 0);
		classificationColumn.AddAttribute (classificationNameCell, "text", 1);
		// end of lexeme cell

		Gtk.ListStore lexemeListStore = new Gtk.ListStore (typeof(string), typeof(string));
		var lexLength = 0;
		bool mulComment = false;
		bool ifelseIndicator = false;
		bool switchIndicator = false;

		var code = inputWindow.Buffer.Text;
		//textview.Buffer.Text = code;
		List<String> lexemes = new List<String>();
		List<String> classi = new List<String>();
		List<String> varList = new List<String>();

		consoleField.Buffer.Text = "";

		// will check the code from top to bottom using the patterns used below
		MatchCollection regex = Regex.Matches(inputWindow.Buffer.Text,  @"\sHAI|KTHXBYE\s|BTW |(?<=BTW ).+|\nOBTW|\nTLDR\n|I HAS A |( ITZ )|( R )|GIMMEH |(?<=(SMOOSH |VISIBLE |ITZ |R |SUM OF |DIFF OF |PRODUKT OF |QUOSHUNT OF |MOD OF |BIGGR OF |SMALLR OF |BOTH OF |EITHER OF |WON OF |NOT |MOD OF |ALL OF |ANY OF |BOTH SAEM |DIFFRINT ))(-?[0-9]\d*(\.\d+)?|SMOOSH |SUM OF |DIFF OF |PRODUKT OF |QUOSHUNT OF |MOD OF |BIGGR OF |SMALLR OF |BOTH OF |EITHER OF |WON OF |NOT |MOD OF |ALL OF |ANY OF |BOTH SAEM |DIFFRINT )|(?<=(SMOOSH |VISIBLE |I HAS A |SUM OF |GIMMEH |DIFF OF |PRODUKT OF |QUOSHUNT OF |MOD OF |BIGGR OF |SMALLR OF |BOTH OF |EITHER OF |WON OF |NOT |MOD OF |ALL OF |ANY OF |BOTH SAEM |DIFFRINT ))(\w[A-Za-z0-9_]*|SMOOSH |SUM OF |DIFF OF |PRODUKT OF |QUOSHUNT OF |MOD OF |BIGGR OF |SMALLR OF |BOTH OF |EITHER OF |WON OF |NOT |MOD OF |ALL OF |ANY OF |BOTH SAEM |DIFFRINT )|""([^""]|"""")*""|SUM OF |DIFF OF |PRODUKT OF |QUOSHUNT OF |MOD OF |BIGGR OF |SMALLR OF | AN |(?<= AN )-?[0-9]\d*(\.\d+)?|(?<= AN )\w[A-Za-z0-9_]*|BOTH OF |EITHER OF |WON OF |NOT |MOD OF |ALL OF |ANY OF |WIN|FAIL|SMOOSH |BOTH SAEM |DIFFRINT |O RLY?|YA RLY|MEBBE |NO WAI|OIC|WTF?|OMG |OMGWTF|GTFO|OIC|IT|VISIBLE |SMOOSH |!|MKAY|::|:o|:>|:""|:\)|-?[0-9]\d*(\.\d+)?|\w[A-Za-z0-9_]*");
		foreach (Match m in regex)
		{
			lexemes.Add (m.ToString ());
			Regex codeDelim = new Regex(@"HAI|KTHXBYE");
			Regex varDec = new Regex("I HAS A ");
			Regex commentSig = new Regex ("BTW ");
			Regex commentSigStart = new Regex ("(?<=\n)OBTW");
			Regex commentSigEnd = new Regex ("TLDR");
			Regex varass = new Regex ("( ITZ )|( R )");
			Regex gim = new Regex ("GIMMEH ");
			Regex numlit = new Regex (@"-?[0-9]\d*(\.\d+)?");
			Regex vari = new Regex (@"\w[A-Za-z0-9_]*");
			Regex strlit = new Regex ("\"([^\"]|\"\")*\"");
			Regex arith = new Regex ("SUM OF |DIFF OF |PRODUKT OF |QUOSHUNT OF |MOD OF |BIGGR OF |SMALLR OF ");
			Regex bool1 = new Regex ("BOTH OF |EITHER OF |WON OF |NOT |MOD OF |ALL OF |ANY OF ");
			Regex vis = new Regex ("VISIBLE ");
			Regex anOp = new Regex (" AN ");
			Regex boolval = new Regex ("WIN|FAIL");
			Regex comp = new Regex ("BOTH SAEM |DIFFRINT ");
			Regex startIf = new Regex ("O RLY?");
			Regex ifClause = new Regex ("YA RLY");
			Regex elseifClause = new Regex ("MEBBE ");
			Regex elseClause = new Regex ("NO WAI");
			Regex endIf = new Regex ("OIC");
			Regex switchKey = new Regex ("WTF?");
			Regex caseKey = new Regex ("OMG");
			Regex defKey = new Regex ("OMGWTF");
			Regex breakKey = new Regex ("GTFO");
			Regex tempVar = new Regex ("IT");
			Regex strConcat = new Regex ("SMOOSH ");
			Regex strConcatEnd = new Regex ("MKAY");
			Regex noLine = new Regex ("!");
			Regex special = new Regex("::|:o|:>|:\"|:\\)");

			if (lexLength > 0) {
				if (commentSigStart.IsMatch (lexemes [lexLength])) {
					mulComment = true;
					classi.Add ("Multiline Comment Start Signifier");
				} else if (commentSigEnd.IsMatch (lexemes [lexLength])) {
					if (mulComment == false) {
						classi.Add ("Error");
					} else {
						mulComment = false;
						classi.Add ("Multiline Comment End Signifier");
					}
				} else if(mulComment==true){
					classi.Add ("Multiline Comment");
				} else if(lexemes[lexLength-1].Equals("BTW ")){
					classi.Add ("Comment");
				} else if (strlit.IsMatch (lexemes [lexLength])) {
					if (lexemes [lexLength - 1].Equals ("I HAS A ") || lexemes [lexLength - 1].Equals ("GIMMEH ")) {
						classi.Add ("Error");
					} else if(caseKey.IsMatch (lexemes [lexLength-1])||varass.IsMatch (lexemes [lexLength-1])||anOp.IsMatch (lexemes [lexLength-1])||vis.IsMatch (lexemes [lexLength-1])||arith.IsMatch (lexemes [lexLength-1])||strConcat.IsMatch (lexemes [lexLength-1])||comp.IsMatch (lexemes [lexLength-1])){
						lexemes.Insert (lexLength, "\"");
						classi.Insert (lexLength, "String Delimiter");
						lexLength = lexLength + 1;
						string replacedString = lexemes [lexLength].Replace ("\"", "");
						lexemes [lexLength] = replacedString;
						classi.Add ("String Literal");
						lexemes.Insert (lexLength + 1, "\"");
						classi.Insert (lexLength + 1, "String Delimiter");
						lexLength = lexLength + 1;
					} else {
						classi.Add ("Error");
					}
				} else if (commentSig.IsMatch (lexemes [lexLength])) {
					classi.Add ("Comment Signifier");
				} else if (codeDelim.IsMatch (lexemes [lexLength])) {
					classi.Add ("Code Delimiter");
				} else if (varDec.IsMatch (lexemes [lexLength])) {
					if (express!=null) {
						classi.Add("Error");
					} else {
						classi.Add ("Variable Declaration");
					}
				} else if (numlit.IsMatch (lexemes [lexLength])) {
					if (lexemes [lexLength - 1].Equals ("I HAS A ") || lexemes [lexLength - 1].Equals ("GIMMEH ")||lexemes [lexLength - 1].Equals ("HAI")) {
						classi.Add ("Error");
					} else if(caseKey.IsMatch (lexemes [lexLength-1])||varass.IsMatch (lexemes [lexLength-1])||anOp.IsMatch (lexemes [lexLength-1])||vis.IsMatch (lexemes [lexLength-1])||boolval.IsMatch (lexemes [lexLength-1])||arith.IsMatch (lexemes [lexLength-1])||strConcat.IsMatch (lexemes [lexLength-1])||bool1.IsMatch (lexemes [lexLength-1])||comp.IsMatch (lexemes [lexLength-1])){
						classi.Add ("Number Literal");
					} else {
						classi.Add ("Error");
					}
				} else if (varass.IsMatch (lexemes [lexLength])) {
					classi.Add ("Variable Assignment");
				} else if (gim.IsMatch (lexemes [lexLength])) {
					classi.Add ("Input Function");
				} else if (vis.IsMatch (lexemes [lexLength])) {
					classi.Add ("Output Function");
				} else if (arith.IsMatch (lexemes [lexLength])) {
					classi.Add ("Arithmetic Operation");
				} else if (bool1.IsMatch (lexemes [lexLength])) {
					classi.Add ("Boolean Operation");
				} else if (boolval.IsMatch (lexemes [lexLength])) {
					classi.Add ("Boolean Values");
				} else if (anOp.IsMatch (lexemes [lexLength])) {
					if(boolval.IsMatch (lexemes [lexLength-1])||arith.IsMatch (lexemes [lexLength-1])||strConcat.IsMatch (lexemes [lexLength-1])||bool1.IsMatch (lexemes [lexLength-1])||comp.IsMatch (lexemes [lexLength-1])){
						classi.Add ("Error");
					}else{
						classi.Add ("Conjunction");
					}
				} else if (startIf.IsMatch (lexemes [lexLength])) {
					if (ifelseIndicator == true) {
						classi.Add("Error");
					} else {
						ifelseIndicator = true;
						express = "ifelse";
						classi.Add("Start Of If-Else Clause");
					}
				} else if (comp.IsMatch (lexemes [lexLength])) {
					classi.Add("Comparison Operation"); //
				} else if (ifClause.IsMatch (lexemes [lexLength])) {
					classi.Add("If Clause");
				} else if (elseifClause.IsMatch (lexemes [lexLength])) {
					classi.Add("Else-If Clause");
				} else if (elseClause.IsMatch (lexemes [lexLength])) {
					classi.Add("Else Clause");
				} else if (endIf.IsMatch (lexemes [lexLength])) {
					if (express==null) {
						classi.Add ("error");
					} else {
						if (classi.Equals ("ifelse")) {
							express = null;
							ifelseIndicator = false;
						} else if(classi.Equals ("switch")){
							express = null;
							switchIndicator = false;
						}
						classi.Add("End of Block");
					}
				} else if (defKey.IsMatch (lexemes [lexLength])) {
					classi.Add("Default Case Keyword");
				} else if (switchKey.IsMatch (lexemes [lexLength])) {
					if (switchIndicator == true) {
						classi.Add("Error");
					} else {
						switchIndicator = true;
						express = "switch";
						classi.Add("Switch Case Keyword");
					}
				} else if (caseKey.IsMatch (lexemes [lexLength])) {
					classi.Add("Case Keyword");
				} else if (breakKey.IsMatch (lexemes [lexLength])) {
					classi.Add("Break Keyword");
				} else if (tempVar.IsMatch (lexemes [lexLength])) {
					classi.Add("Temporary Variable");
				} else if (strConcat.IsMatch (lexemes [lexLength])) {
					classi.Add("String Concatenation Operation");
				} else if (strConcatEnd.IsMatch (lexemes [lexLength])) {
					classi.Add("End of String Concatenation Operation");
				} else if (noLine.IsMatch (lexemes [lexLength])) {
					classi.Add("No New Line");
				} else if (vari.IsMatch (lexemes [lexLength])) {
					if (lexemes [lexLength - 1].Equals ("I HAS A ")&&!(varList.Contains(lexemes [lexLength]))) {
						varList.Add (lexemes [lexLength]);
						classi.Add ("Variable Identifier");
					} else if (lexemes [lexLength - 1].Equals ("I HAS A ")&&(varList.Contains(lexemes [lexLength]))) {
						classi.Add ("Variable Identifier");
					} else if((!lexemes [lexLength - 1].Equals ("I HAS A "))&&varList.Contains(lexemes [lexLength])) {
						classi.Add ("Variable Identifier");
					} else {
						if(mulComment==true){
							classi.Add ("Multiline Comment");
						}else{
							classi.Add ("Error");
							string toConcat = ">" + lexemes [lexLength] + "--> INVALID ARGUMENT" + "\n";
							consoleField.Buffer.Text += toConcat;
						}

					}

				}
				lexLength++;
			} else if (codeDelim.IsMatch (lexemes [lexLength])&&lexemes[lexLength].Equals("HAI")) {
				classi.Add ("Code Delimiter");
				lexLength++;
			}

		}

		//if lexlength is 0, then HAI does not exist in the input
		if (lexLength == 0) {
			errorSource = consoleField.Buffer.Text;
			errorMessage = "INVALID START OF PROGRAM";
			errorFlag = true;
		} else {
			if((!(lexemes[lexLength-1].Equals("KTHXBYE") && (classi [lexLength - 1].Equals ("Code Delimiter"))) )){
				errorSource = lexemes[lexLength - 1];
				errorMessage = "INVALID END OF PROGRAM";
				errorFlag = true;
			}
		}
		//checker if the HAI and KTHXBYE are only in the Beginning and End respectively
		for(int i=0;i<lexLength;i++){
			if(lexemes[i].Equals("HAI") && i != 0 && (classi [i].Equals ("Code Delimiter")) ){
				errorSource = lexemes[i];
				errorMessage = "INVALID USE OF HAI";
				errorFlag = true;
			} 
			if (lexemes [i].Equals ("KTHXBYE") && i != lexLength - 1 && (classi [i].Equals ("Code Delimiter"))) {
				errorSource = lexemes [i];
				errorMessage = "INVALID USE OF KTHXBYE";
				errorFlag = true;
			}
		}

		// loop this model
		for(int i=0;i<lexLength;i++){
			lexemeListStore.AppendValues (lexemes[i],classi[i]);
		} 

		if(errorFlag){
			lexemeListStore.Clear ();
		}

		lexemeTree.Model = lexemeListStore;

		lexemeWindow.ShowAll ();

		// symbol table view
		symbolTableTree.Destroy();
		symbolTableTree = new Gtk.TreeView ();
		symbolTableTree.ModifyBase (StateType.Normal, tableColor);
		symbolTableTree.ModifyText(StateType.Normal, tableTextColor);
		symbolTableWindow.Add (symbolTableTree);

		Gtk.TreeViewColumn identifierColumn = new Gtk.TreeViewColumn ();
		identifierColumn.Title = "Identifier";

		Gtk.TreeViewColumn valueColumn = new Gtk.TreeViewColumn ();
		valueColumn.Title = "Value";

		symbolTableTree.AppendColumn (identifierColumn);
		symbolTableTree.AppendColumn (valueColumn);

		// symbol table cell!
		Gtk.CellRendererText identifierNameCell = new Gtk.CellRendererText();
		identifierColumn.PackStart(identifierNameCell, true);

		Gtk.CellRendererText valueNameCell = new Gtk.CellRendererText ();
		valueColumn.PackStart (valueNameCell, true);

		identifierColumn.AddAttribute (identifierNameCell, "text", 0);
		valueColumn.AddAttribute (valueNameCell, "text", 1);
		// end of symbol table cell

		Gtk.ListStore symbolTableListStore = new Gtk.ListStore (typeof(string), typeof(string));

		// symbol table checker
		if(!errorFlag){
			Dictionary<string, string> dictionary = new Dictionary<string, string> ();
			// accumulator
			string IT = "0";

			foreach (string variable in varList) {
				dictionary.Add (variable, "null");
			}

			for(int i=0;i<lexLength;i++){

				if (classi [i] == "Input Function") {
					string str = lexemes [i+1];

					InputDialogBox cid = new InputDialogBox (str.ToString(), lexerStatus);
					if (cid.Run () == (int)Gtk.ResponseType.Ok) {
						dictionary [str.ToString()] = cid.retEvalVal ();

						var contextId = this.lexerStatus.GetContextId ("clicked");
						lexerStatus.Push (contextId, cid.retEvalVal () + " assigned to " + dictionary [str.ToString()]);
					}
					cid.Destroy ();
					// for variable assignment operation
				} else if (classi [i] == "Variable Assignment") {
					String key = lexemes [i - 1];
					String val;

					List<String> expression = new List<String> ();

					if (classi [i + 1] == "String Delimiter")
						val = lexemes [i + 2];
					else if (classi [i + 1] == "Arithmetic Operation") {
						int j = i + 1;
						while (classi [j] == "Arithmetic Operation" || classi [j] == "Conjunction" || classi [j] == "Variable Identifier" || classi [j] == "Number Literal" || classi [j] == "String Literal" || classi [j] == "String Delimiter") {
							if (classi [j] == "Conjunction" || classi[j] == "String Delimiter") {
								j++;
								continue;
							} else {
								if ((classi [j - 1] == "Variable Identifier" || classi [j - 1] == "Number Literal" || classi [j - 1] == "String Literal")) {
									i = j - 1;
									break;
								}
								if(lexemes[j] != "String Delimiter") expression.Add (lexemes [j]);
								else expression.Add (lexemes [j+1]);
							}
							j++;
							i = j - 1;
						}
						val = mathOperation (expression, dictionary);
						// for boolean operations
					} else if (classi [i + 1] == "Boolean Operation") {
						int j = i + 1;
						while (classi [j] == "Boolean Operation" || classi [j] == "Conjunction" || classi [j] == "Variable Identifier" || classi [j] == "Boolean Values") {
							if (classi [j] == "Conjunction") {
								j++;
								continue;
							} else {
								if ((classi [j - 1] == "Variable Identifier" || classi [j - 1] == "Boolean Values")) {
									i = j - 1;
									break;
								}
								expression.Add (lexemes [j]);
							}
							j++;
							i = j - 1;
						}
						val = booleanOperation (expression, dictionary);
						// for string concat operations
					}else if (classi [i+1] == "String Concatenation Operation") {
						int j = i+2;
						List<String> strings = new List<String> ();
						while (classi [j] == "Conjunction" || classi [j] == "Boolean Values" || classi [j] == "Number Literal"  || classi [j] == "String Delimiter" || classi [j] == "String Literal" || classi [j] == "Variable Identifier" || classi [i] == "End of String Concatenation Operation") {
							if (classi [j] == "Conjunction" || classi[j] == "String Delimiter") {
								j++;
								continue;
							} else {
								if(classi[j-1] == "String Delimiter") strings.Add ('"' + lexemes [j] + '"');
								else strings.Add (lexemes [j]);

								if ((classi [j + 1] != "Conjunction" && classi [j] == "Variable Identifier") || (classi [j + 2] != "Conjunction" && classi [j] == "String Literal")) {
									i=j-1;
									break;
								}
							}
							j++; i = j - 1;
						}
						val = smoosh (strings, dictionary);
					}else
						val = lexemes [i + 1];

					dictionary [key] = val;
					// for visible function
				} else if (classi [i] == "Output Function") {

					List<String> expression = new List<String> ();

					if (classi [i + 1] == "String Delimiter") {
						lexemes [i + 2] = (lexemes [i + 2]).Replace (":)", "\n");
						lexemes [i + 2] = (lexemes [i + 2]).Replace (":>", "\t");
						lexemes [i + 2] = (lexemes [i + 2]).Replace (":\"", "\"");
						lexemes [i + 2] = (lexemes [i + 2]).Replace ("::", ":");

						if (classi [i + 4] != "No New Line")
							consoleField.Buffer.Text = string.Concat (consoleField.Buffer.Text, lexemes [i + 2] + "\n");
						else
							consoleField.Buffer.Text = string.Concat (consoleField.Buffer.Text, lexemes [i + 2]);
					} else if (classi [i + 1] == "Variable Identifier") {
						if (classi [i + 2] != "No New Line")
							consoleField.Buffer.Text = string.Concat (consoleField.Buffer.Text, dictionary [(lexemes [i + 1])] + "\n");
						else
							consoleField.Buffer.Text = string.Concat (consoleField.Buffer.Text, dictionary [(lexemes [i + 1])]);
					} else if (classi [i + 1] == "Number Literal" || classi [i + 1] == "Boolean Values") {
						if (classi [i + 2] != "No New Line")
							consoleField.Buffer.Text = string.Concat (consoleField.Buffer.Text, (lexemes [i + 1]) + "\n");
						else
							consoleField.Buffer.Text = string.Concat (consoleField.Buffer.Text, (lexemes [i + 1]));
					} else if (classi [i + 1] == "Temporary Variable") {
						if (classi [i + 2] != "No New Line")
							consoleField.Buffer.Text = string.Concat (consoleField.Buffer.Text, IT + "\n");
						else
							consoleField.Buffer.Text = string.Concat (consoleField.Buffer.Text, IT);
					}else if (classi [i + 1] == "Arithmetic Operation") {
						int j = i + 1;
						while (classi [j] == "Arithmetic Operation" || classi [j] == "Conjunction" || classi [j] == "Variable Identifier" || classi [j] == "Number Literal" || classi [j] == "String Literal" || classi [j] == "String Delimiter") {
							if (classi [j] == "Conjunction" || classi[j] == "String Delimiter") {
								j++;
								continue;
							} else {
								if ((classi [j - 1] == "Variable Identifier" || classi [j - 1] == "Number Literal" || classi [j - 1] == "String Literal")) {
									i = j - 1;
									break;
								}
								if(lexemes[j] != "String Delimiter") expression.Add (lexemes [j]);
								else expression.Add (lexemes [j+1]);
							}
							j++;
							i = j - 1;
						}
						if (classi [i + 1] != "No New Line")
							consoleField.Buffer.Text = string.Concat (consoleField.Buffer.Text, mathOperation (expression, dictionary) + "\n");
						else
							consoleField.Buffer.Text = string.Concat (consoleField.Buffer.Text, mathOperation (expression, dictionary));
					} else if (classi [i + 1] == "Boolean Operation") {
						int j = i + 1;
						while (classi [j] == "Boolean Operation" || classi [j] == "Conjunction" || classi [j] == "Variable Identifier" || classi [j] == "Boolean Values") {
							if (classi [j] == "Conjunction") {
								j++;
								continue;
							} else {
								if ((classi [j - 1] == "Variable Identifier" || classi [j - 1] == "Boolean Values")) {
									i = j - 1;
									break;
								}
								expression.Add (lexemes [j]);
							}
							j++;
							i = j - 1;
						}
						if (classi [i + 1] != "No New Line")
							consoleField.Buffer.Text = string.Concat (consoleField.Buffer.Text, booleanOperation (expression, dictionary) + "\n");
						else
							consoleField.Buffer.Text = string.Concat (consoleField.Buffer.Text, booleanOperation (expression, dictionary));
					}else if (classi [i+1] == "String Concatenation Operation") {
						int j = i+2;
						List<String> strings = new List<String> ();
						while (classi [j] == "Conjunction" || classi [j] == "Boolean Values" || classi [j] == "Number Literal"  || classi [j] == "String Delimiter" || classi [j] == "String Literal" || classi [j] == "Variable Identifier" || classi [i] == "End of String Concatenation Operation") {
							if (classi [j] == "Conjunction" || classi[j] == "String Delimiter") {
								j++;
								continue;
							} else {
								if(classi[j-1] == "String Delimiter") strings.Add ('"' + lexemes [j] + '"');
								else strings.Add (lexemes [j]);

								if ((classi [j + 1] != "Conjunction" && classi [j] == "Variable Identifier") || (classi [j + 2] != "Conjunction" && classi [j] == "String Literal")) {
									i=j-1;
									break;
								}
							}
							j++; i = j - 1;
						}
						//val = smoosh (strings, dictionary);
						//consoleField.Buffer.Text = string.Concat (consoleField.Buffer.Text, classi[i+2] + "\n");
						if (classi [i + 1] != "No New Line")
							consoleField.Buffer.Text = string.Concat (consoleField.Buffer.Text, smoosh (strings, dictionary) + "\n");
						else
							consoleField.Buffer.Text = string.Concat (consoleField.Buffer.Text, smoosh (strings, dictionary));
					} 
					// for arithmetic operations
				} else if (classi [i] == "Arithmetic Operation") {
					List<String> expression = new List<String> ();

					int j = i;

					while (classi [j] == "Arithmetic Operation" || classi [j] == "Conjunction" || classi [j] == "Variable Identifier" || classi [j] == "Number Literal" || classi [j] == "String Literal" || classi [j] == "String Delimiter") {
						if (classi [j] == "Conjunction" || classi[j] == "String Delimiter") {
							j++;
							continue;
						} else {
							if ((classi [j - 1] == "Variable Identifier" || classi [j - 1] == "Number Literal" || classi [j - 1] == "String Literal")) {
								if (j != i) {
									i = j - 1;
									break;
								}
							}
							if(lexemes[j] != "String Delimiter") expression.Add (lexemes [j]);
							else expression.Add (lexemes [j+1]);
						}
						j++; i = j - 1;
					}

					IT = mathOperation (expression, dictionary);
					if(IT == "FAIL"){
						errorFlag = true;
						errorSource = lexemes [i - 4];
						errorMessage = lexemes[i - 4] + ": INVALID TYPE(S) USED";
						break;
					}
					// for string concat operations
				} else if (classi [i] == "String Concatenation Operation") {
					int j = i+1;
					List<String> strings = new List<String> ();
					while (classi [j] == "Conjunction" || classi [j] == "Boolean Values" || classi [j] == "Number Literal" || classi [j] == "String Delimiter" || classi [j] == "String Literal" || classi [j] == "Variable Identifier" || classi [i] == "End of String Concatenation Operation") {
						if (classi [j] == "Conjunction" || classi[j] == "String Delimiter") {
							j++;
							continue;
						} else {
							if(classi[j-1] == "String Delimiter") strings.Add ('"' + lexemes [j] + '"');
							else strings.Add (lexemes [j]);

							if ((classi [j + 1] != "Conjunction" && classi [j] == "Variable Identifier") || (classi [j + 2] != "Conjunction" && classi [j] == "String Literal")) {
								i=j-1;
								break;
							}
						}
						j++; i = j - 1;
					}

					IT = smoosh (strings, dictionary);
					// for both saem and diffrint
				} else if (classi [i] == "Comparison Operation") {
					List<String> expression = new List<String> ();
					Stack dataType = new Stack ();
					int j = i;

					while (classi [j] == "Arithmetic Operation" || classi[j] == "Comparison Operation" || classi [j] == "Conjunction" || classi [j] == "Variable Identifier" || classi [j] == "Number Literal" || classi [j] == "String Literal" || classi [j] == "String Delimiter") {
						if (classi [j] == "Conjunction" || classi[j] == "String Delimiter") {
							j++;
							continue;
						} else if(classi[j] == "Arithmetic Operation"){
							List<String> expression1 = new List<String> ();

							int k = j;

							while (classi [k] == "Arithmetic Operation" || classi [k] == "Conjunction" || classi [k] == "Variable Identifier" || classi [k] == "Number Literal" || classi [k] == "String Literal" || classi [j] == "String Delimiter") {
								if (classi [k] == "Conjunction" || classi[k] == "String Delimiter") {
									k++;
									continue;
								} else {
									if ((classi [k - 1] == "Variable Identifier" || classi [k - 1] == "Number Literal" || classi [k - 1] == "String Literal")) {
										if (j != k) {
											j = k - 1;
											break;
										}
									}
									if(lexemes[j] != "String Delimiter") expression1.Add (lexemes [k]);
									else expression1.Add (lexemes [k+1]);
								}
								k++; j = k - 1;
							}

							expression.Add(mathOperation (expression1, dictionary)); i = j;
						} else {
							if ((classi [j - 1] == "Variable Identifier" || classi [j - 1] == "Number Literal" || classi [j - 1] == "String Literal")) {
								if (j != i) {
									i = j - 1;
									break;
								}
							}
							double n;
							if (lexemes [j - 1] == "\"")
								dataType.Push ("String");
							else if (dictionary.ContainsKey(lexemes [j]))
								dataType.Push ("Variable");
							else if (double.TryParse(lexemes [j], out n))
								dataType.Push ("Number");
							else
								dataType.Push ("Unknown");
							expression.Add (lexemes [j]);
						}
						j++; i = j - 1;
					}
					IT = compare (expression, dataType, dictionary);
					// O RLY? functionality
				} else if (classi [i] == "Start Of If-Else Clause") {
					int a = i;

					if (IT == "WIN") {
						//perform until else clause
						int start, end;

						while(classi[a]!="Else Clause"){a++;}
						start = a;
						while(classi[a]!="End of Block"){a++;}
						end = a;

						lexemes.RemoveRange (start, end-start+1);
						classi.RemoveRange (start, end-start+1);
						lexLength = classi.Count;
					} else {
						//perform else clause only
						int start, end;

						while(classi[a]!="If Clause"){a++;}
						start = a;
						while(classi[a]!="Else Clause"){a++;}
						end = a;

						lexemes.RemoveRange (start, end-start+1);
						classi.RemoveRange (start, end-start+1);
						lexLength = classi.Count;
					}
				} else if (classi [i] == "Boolean Operation") {
					int j = i;
					List<String> expression = new List<String> ();

					while (classi [j] == "Boolean Operation" || classi [j] == "Conjunction" || classi [j] == "Variable Identifier" || classi [j] == "Boolean Values") {
						if (classi [j] == "Conjunction") {
							j++;
							continue;
						} else {
							if ((classi [j - 1] == "Variable Identifier" || classi [j - 1] == "Boolean Values")) {
								if (j != i) {
									i = j - 1;
									break;
								}
							}
							expression.Add (lexemes [j]);
						}
						j++;
						i = j - 1;
					}
					IT = booleanOperation (expression, dictionary);
					// switch case functionality
				} else if(classi[i] == "Switch Case Keyword"){
					if (dictionary.ContainsKey (lexemes [i - 1])) {
						IT = dictionary [lexemes [i - 1]];
					}
					int a = i;
					int start, end = a;
					string value;

					while (classi [end] != "End of Block") end++;
					while(classi[a]!="End of Block"){
						if (classi [a] == "Case Keyword") {
							if (classi [a + 1] == "String Delimiter") value = lexemes [a + 2];
							else value = lexemes [a + 1];

							if (IT == value) { 
								start = a;
								while (classi [start] != "Break Keyword" && start!= end)
									start++;

								lexemes.RemoveRange (i, a-i);
								classi.RemoveRange (i, a-i);
								if(classi[start-a+i]== "Break Keyword"){
									lexemes.RemoveRange (start-a+i, end-start+1);
									classi.RemoveRange (start-a+i, end-start+1);
								}
								lexLength = classi.Count;

								break;
							}
						}
						if (classi [a] == "Default Case Keyword") {
							start = a;
							a = i;

							lexemes.RemoveRange (a, start-a);
							classi.RemoveRange (a, start-a);
							lexLength = classi.Count;

							break;
						}
						a++;
					}


				}
			}

			foreach (KeyValuePair<string, string> entry in dictionary) {
				symbolTableListStore.AppendValues (entry.Key, entry.Value);
			}

		}

		symbolTableTree.Model = symbolTableListStore;

		symbolTableWindow.ShowAll ();


		var statusContext = this.lexerStatus.GetContextId ("clicked");
		lexerStatus.Push (statusContext, "Executed");

		if (inputWindow.Buffer.Text == ""
			|| inputWindow.Buffer.Text == " "
			|| inputWindow.Buffer.Text == "\n"
			|| inputWindow.Buffer.Text == "\t") {
			consoleField.Buffer.Text = "> No input entered!";

			statusContext = this.lexerStatus.GetContextId ("clicked");
			lexerStatus.Push (statusContext, "ASSURE THAT INPUT FIELD IS NOT EMPTY");
		} else if (errorFlag) {
			if(!errorSource.Contains("\"")) 
				consoleField.Buffer.Text = "> Error near \""+ errorSource +"\"\n";
			else
				consoleField.Buffer.Text = "> Error near "+ errorSource +"\n";
			statusContext = this.lexerStatus.GetContextId ("clicked");
			lexerStatus.Push (statusContext, errorMessage);
		}

		if(errorFlag == true){ // if error is encountered, the interpreter will clear the tables
			// this will ensure that errrors are debugged one at a time; not throwing all errors
			// at the same time
			lexemeListStore.Clear ();
			lexemeTree.Model = lexemeListStore;
			lexemeWindow.ShowAll ();

			symbolTableListStore.Clear ();
			symbolTableTree.Model = symbolTableListStore;
			symbolTableWindow.ShowAll ();
		}

		errorFlag = false;
	}
	public string compare(List<String> expression, Stack dataType, Dictionary<string, string> dictionary){
		Stack stack = new Stack ();
		Stack typeStack = new Stack ();
		expression.Reverse();//we reverse the expression to read in the characters from right to left
		double n;
		string result = "FAIL";
		foreach (string c in expression) {//for each string character in the array
			/*if (Double.TryParse (c, out n)) {//if the character can be converted to a number (operand)
				stack.Push (n);//push the number onto the stack
				consoleField.Buffer.Text += n + " IM A NUMBER\n";
			} else {*/
			if(c != "DIFFRINT " && c != "BOTH SAEM "){
				string temp = dataType.Pop().ToString();
				stack.Push (c);//push the string onto the stack
				typeStack.Push(temp);
			}
			//}
			if (c == "DIFFRINT ") {//handling of operators
				string i = stack.Pop().ToString();
				string j = stack.Pop().ToString();
				string s = typeStack.Pop ().ToString ();
				string t = typeStack.Pop ().ToString ();

				if (!i.Equals (j))
					result = "WIN";
				else
					result = "FAIL";

				if(!s.Equals(t))
					result = "WIN";

				stack.Push (result);//push current result onto the stack
			}
			if (c == "BOTH SAEM ") {
				string i = stack.Pop().ToString();
				string j = stack.Pop().ToString();
				string s = typeStack.Pop ().ToString ();
				string t = typeStack.Pop ().ToString ();

				if (i.Equals (j))
					result = "WIN";
				else
					result = "FAIL";

				if(!s.Equals(t))
					result = "FAIL";

				stack.Push (result);//push current result onto the stack
			}
			if (dictionary.ContainsKey (c)) {
				if (Double.TryParse (dictionary [c], out n)){
					stack.Push (n);
					typeStack.Push ("Number");
				} else {
					stack.Push (dictionary [c]);
					typeStack.Push ("String");
				}
			}
		}
		return stack.Peek ().ToString ();
	}
	public string booleanOperation(List<String> expression, Dictionary<string, string> dictionary){
		Stack stack = new Stack ();
		expression.Reverse();//we reverse the expression to read in the characters from right to left
		string result;
		foreach (string c in expression) {//for each string character in the array
			if (c == "WIN" || c == "FAIL") {//if the character can be converted to a number (operand)
				stack.Push (c);//push the number onto the stack
			}
			if (c == "BOTH OF ") {//handling of operators
				string x = (string)stack.Pop ();
				string y = (string)stack.Pop ();
				if (x == "WIN" && y == "WIN") result = "WIN";
				else result = "FAIL";
				stack.Push (result);//push current result onto the stack
			}
			if (c == "EITHER OF ") {//handling of operators
				string x = (string)stack.Pop ();
				string y = (string)stack.Pop ();
				if (x == "WIN" || y == "WIN") result = "WIN";
				else result = "FAIL";
				stack.Push (result);//push current result onto the stack
			}
			if (c == "WON OF ") {//handling of operators
				string x = (string)stack.Pop ();
				string y = (string)stack.Pop ();
				if ((x == "WIN" && y == "FAIL")|| (y == "WIN" && x == "FAIL")) result = "WIN";
				else result = "FAIL";
				stack.Push (result);//push current result onto the stack
			}
			if (c == "NOT ") {//handling of operators
				string x = (string)stack.Pop ();
				if (x == "FAIL") result = "WIN";
				else result = "FAIL";
				stack.Push (result);//push current result onto the stack
			}
			if (c == "ALL OF ") {//handling of operators
				if (stack.Contains("FAIL")) result = "FAIL";
				else result = "WIN";
				stack.Push (result);//push current result onto the stack
			}
			if (c == "ANY OF ") {//handling of operators
				if (stack.Contains("WIN")) result = "WIN";
				else result = "FAIL";
				stack.Push (result);//push current result onto the stack
			}
			if (dictionary.ContainsKey (c)) {
				stack.Push (dictionary[c]);
			}
		}
		return stack.Peek ().ToString();
	}
	public string smoosh(List<String> strings, Dictionary<string, string> dictionary){
		string finalString="";
		Regex strlit = new Regex ("\"([^\"]|\"\")*\"");
		foreach(string s in strings){
			if (dictionary.ContainsKey (s))
				finalString = string.Concat (finalString, dictionary [s]);
			else if (strlit.IsMatch (s)) {
				/*s = s.Replace (":)", "\n");
				s = s.Replace (":>", "\t");
//				s = s.Replace (":o", "\g");
				s = s.Replace (":\"", "\"");
				s = s.Replace ("::", ":");*/
				finalString = string.Concat (finalString, s.Replace ("\"", ""));
			}
			else finalString = string.Concat (finalString, s);
		}

		return finalString;
	}
	public string mathOperation(List<String> expression, Dictionary<string, string> dictionary){
		Stack stack = new Stack ();
		expression.Reverse();//we reverse the expression to read in the characters from right to left
		Double n, result;
		bool numberFlag = true;
		foreach (string c in expression) {//for each string character in the array
			if(c != "SUM OF " && c != "DIFF OF " && c != "PRODUKT OF " && c != "QUOSHUNT OF " && c != "MOD OF " && c != "BIGGR OF " && c != "SMALLR OF "){
				if (dictionary.ContainsKey (c)) {
					if (Double.TryParse (dictionary [c], out n)){
						stack.Push (n);
					} else {
						numberFlag = false;
					}
				}
				else if (double.TryParse (c, out n))
					stack.Push (n);//push the string onto the stack
				else
					numberFlag = false;
			}
			if (numberFlag) {
				if (c == "SUM OF ") {//handling of operators
					double x = (double)stack.Pop ();
					double y = (double)stack.Pop ();
					result = x + y;//evaluate the values popped from the stack
					stack.Push (result);//push current result onto the stack
				}
				if (c == "DIFF OF ") {
					double x = (double)stack.Pop ();
					double y = (double)stack.Pop ();
					result = x - y;
					stack.Push (result);
				}
				if (c == "PRODUKT OF ") {
					double x = (double)stack.Pop ();
					double y = (double)stack.Pop ();
					result = x * y;
					stack.Push (result);
				}
				if (c == "QUOSHUNT OF ") {
					double x = (double)stack.Pop ();
					double y = (double)stack.Pop ();
					result = x / y;
					stack.Push (result);
				}
				if (c == "MOD OF ") {
					double x = (double)stack.Pop ();
					double y = (double)stack.Pop ();
					result = x % y;
					stack.Push (result);
				}
				if (c == "BIGGR OF ") {
					double x = (double)stack.Pop ();
					double y = (double)stack.Pop ();
					result = Math.Max (x, y);
					stack.Push (result);
				}
				if (c == "SMALLR OF ") {
					double x = (double)stack.Pop ();
					double y = (double)stack.Pop ();
					result = Math.Min (x, y);
					stack.Push (result);
				}
			} else {
				stack.Push ("FAIL");
			}
		}
		return stack.Peek ().ToString ();
	}

	protected void OnFileButtonClicked (object sender, EventArgs e)
	{
		Gtk.FileChooserDialog fc=
			new Gtk.FileChooserDialog("Choose the file to open",
				this,
				FileChooserAction.Open,
				"Cancel",ResponseType.Cancel,
				"Open",ResponseType.Accept);
		fc.Filter = new FileFilter ();
		fc.Filter.AddPattern ("*.lol");

		if (fc.Run() == (int)ResponseType.Accept) 
		{
			System.IO.FileStream file = System.IO.File.OpenRead(fc.Filename);
			try
			{   // Open the text file using a stream reader.
				using (StreamReader sr = new StreamReader(fc.Filename))
				{
					// Read the stream to a string, and write the string to the console.
					String line = sr.ReadToEnd();
					inputWindow.Buffer.Text = line;
				}
			}
			catch (Exception error)
			{
				Console.WriteLine("The file could not be read:");
				Console.WriteLine(error.Message);
			}
			file.Close();
		}
		fc.Destroy();
	}

	protected void OnConsoleSubmitClicked (object sender, EventArgs e)
	{
		consoleField.Buffer.Text += consoleEntry.Text + "\n";
		consoleEntry.Text = "";
	}
}
