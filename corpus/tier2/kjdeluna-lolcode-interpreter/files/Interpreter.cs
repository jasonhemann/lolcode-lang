using System;
using System.Text.RegularExpressions;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using LolcodeInterpreter;

namespace LolcodeInterpreter
{
	public class Interpreter
	{
		public Interpreter ()
		{
		}

		public void run(){
			//MainClass.win.clearConsole ();
			LexicalAnalyzer lexicalAnalyzer = new LexicalAnalyzer();
			if (lexicalAnalyzer.analyze ()) {
				Parser parser = new Parser (lexicalAnalyzer.getTokenArrayList ());
				bool parserSuccess = false;
				if (lexicalAnalyzer.getTokenArrayList ().Count < 3) parserSuccess = false;
				else parserSuccess = parser.parseProgram ();
				Console.WriteLine ($"{parserSuccess}");
				if (parserSuccess) {
					MainClass.win.updateMessagesOnConsole ("lolterpreter@CMSC124:~$ \n");
				} else {
					MainClass.win.updateMessagesOnConsole ("Parsing Failed. Terminating Program . . .\nlolterpreter@CMSC124:~$ \n");
				}
			} else
				MainClass.win.updateMessagesOnConsole ("Lexical Analysis Failed. Terminating Program . . . \nlolterpreter@CMSC124:~$ \n");
		}
	}
}

