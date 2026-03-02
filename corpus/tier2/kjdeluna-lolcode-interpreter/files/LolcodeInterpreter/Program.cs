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
