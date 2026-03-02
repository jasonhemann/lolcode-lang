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
			LexicalAnalyzer la = new LexicalAnalyzer();
			la.analyze();
			Parser pa = new Parser (la.getTokenArrayList());
			Console.WriteLine (pa.program ());
		}

	}
}

