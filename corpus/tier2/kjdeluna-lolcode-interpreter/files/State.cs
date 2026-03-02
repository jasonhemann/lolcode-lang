/* ---------------------------------------------------
 * This class is used for nesting if-else statements.
 * The parser holds the current State and all the 
 * 		previous states are held by the scopeStack.
 * 	Recommendation: 
 * 		Use this when implementing functions.
 * --------------------------------------------------*/

using System;
using System.Linq;
using System.Collections.Generic;
namespace LolcodeInterpreter
{
	public class State
	{
		private Keyword keyword;
		private Dictionary<String, bool> stateDictionary;
		public State (Keyword keyword, Dictionary<String, bool> dict)
		{
			this.keyword = keyword;
			this.stateDictionary = dict;
		}

		public Keyword getKeyword(){
			return this.keyword;
		}

		public bool getValueFromState(String key){
			return this.stateDictionary [key];
		}
	}
}

