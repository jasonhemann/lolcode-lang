/*-------------------------------------
 * 	Project Status
 * 		[DONE] Comments (BTW, OBTW, TLDR) 
 * 		[DONE] VISIBLE <literal>
 * 		[DONE] VISIBLE <expression>
 * 		[DONE] VISIBLE <variable>
 * 		[DONE] VISIBLE <smoosh>
 * 		[DONE] N-arity Visible
 * 		[DONE] GIMMEH <variable>
 * 		[DONE] I HAS A <variable>
 * 		[DONE] I HAS A <variable> ITZ <expression>
 * 		[DONE] I HAS A <variable> ITZ <variable>
 * 		[DONE] <variable> R <expression>
 * 		[DONE] <variable> R <variable>
 * 		[DONE] <variable> R <literal>
 * 		[DONE] SUM OF, DIFF OF, PRODUKT OF,
 * 				QUOSHUNT OF, MOD OF, BIGGR OF,
 * 				SMALLR OF
 * 		[DONE] BOTH OF, EITHER OF, ANY OF, ALL OF,
 * 				BOTH SAEM, DIFFRINT, WON OF
 * 		[DONE] YA-RLY - NO-WAI - OIC
 * 		[DONE] WTF? OMG OIC
 * 		[DONE] GTFO
 * 		[DONE] SMOOSH
 * 
 * All Specs Done: 12-03-17
 * 
 * Bonus:
 * 		[DONE] VISIBLE!
 * 		[DONE] Soft command breaks
 * 		[DONE] MEBBE
 * 		[DONE] Nesting if-else
 * 
 * Working as of 12-03-17 9:22 PM
 * 
 * Team KTHXBYE Signing OFF
 * -----------------------------------*/


using System;
using Gtk;
using LolcodeInterpreter;
namespace LolcodeInterpreter
{
	class MainClass
	{
		public static MainWindow win;
		public static void Main (string[] args)
		{
			Application.Init ();
			win = new MainWindow ();
			win.Show ();
			Application.Run ();
		}
		public static void runInterpreter(){
			Interpreter interpreter = new Interpreter();
			interpreter.run ();
		}
	}
}
