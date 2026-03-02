using System;

namespace LolcodeInterpreter
{
	public class Token
	{
		String lexeme;
		String type;
		Keyword keyword;
		int lineNumber;
		public Token (String lexeme, String type, Keyword keyword,int lineNumber)
		{
			this.lexeme = lexeme;
			this.type = type;
			this.keyword = keyword;
			this.lineNumber = lineNumber;
		}

		public String getLexeme(){
			return this.lexeme;
		}

		public Keyword getKeyword(){
			return this.keyword;
		}
		public String getType(){
			return this.type;
		}

		public int getLineNumber(){
			return this.lineNumber;
		}
	}
}

