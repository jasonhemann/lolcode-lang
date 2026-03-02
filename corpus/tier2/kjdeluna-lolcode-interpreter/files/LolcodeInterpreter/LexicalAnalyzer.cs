using System;
using System.Text.RegularExpressions;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using LolcodeInterpreter;

namespace LolcodeInterpreter
{
	public class LexicalAnalyzer
	{
		ArrayList tokensArrayList;
		// PAIRED KEYWORDS
		public readonly Regex HAI_REGEX = new Regex(@"^\s*HAI\s*");
		public readonly Regex KTHXBYE_REGEX = new Regex(@"^\s*KTHXBYE\s*");
		public readonly Regex OBTW_REGEX = new Regex(@"^\s*OBTW");
		public readonly Regex TLDR_REGEX = new Regex(@"^\s*TLDR");
		public readonly Regex AN_REGEX = new Regex (@"^\s*AN");

		// COMMENT
		public readonly Regex BTW_REGEX = new Regex(@"^\s*BTW");

		// ARITHMETIC OPERATORS
		public readonly Regex SUM_OF_REGEX = new Regex(@"^\s*SUM OF");
		public readonly Regex DIFF_OF_REGEX = new Regex(@"^\s*DIFF OF");
		public readonly Regex PRODUKT_OF_REGEX = new Regex(@"^\s*PRODUKT OF");
		public readonly Regex QUOSHUNT_OF_REGEX = new Regex (@"^\s*QUOSHUNT OF");
		public readonly Regex MOD_OF_REGEX = new Regex(@"^\s*MOD OF");
		public readonly Regex BIGGR_OF_REGEX = new Regex (@"^\s*BIGGR OF");
		public readonly Regex SMALLR_OF_REGEX = new Regex (@"^\s*SMALLR OF");

		// LOGICAL OPERATORS
		public readonly Regex BOTH_OF_REGEX = new Regex (@"^\s*BOTH OF");
		public readonly Regex EITHER_OF_REGEX = new Regex (@"^\s*EITHER OF");
		public readonly Regex WON_OF_REGEX = new Regex (@"^\s*WON OF");
		public readonly Regex NOT_REGEX = new Regex (@"^\s*NOT");
		public readonly Regex ALL_OF_REGEX = new Regex (@"^\s*ALL OF");
		public readonly Regex ANY_OF_REGEX = new Regex (@"^\s*ANY OF");
		public readonly Regex BOTH_SAEM_REGEX = new Regex (@"^\s*BOTH SAEM");
		public readonly Regex DIFFRINT_REGEX = new Regex (@"^\s*DIFFRINT");

		// INPUT AND OUTPUT
		public readonly Regex VISIBLE_REGEX = new Regex(@"^\s*VISIBLE");
		public readonly Regex GIMMEH_REGEX = new Regex(@"^\s*GIMMEH");

		// VARIABLE DECLARATION, ASSIGNMENT, INITIALIZATION
		public readonly Regex VARIABLE_REGEX = new Regex(@"^\s*[A-Za-z0-9][A-Za-z0-9_]*");
		public readonly Regex I_HAS_A_REGEX = new Regex(@"^\s*I HAS A");
		public readonly Regex ITZ_REGEX = new Regex(@"^\s*ITZ");
		public readonly Regex R_REGEX = new Regex(@"^\s*R$");

		// PRIMITIVE DATA TYPES
		public readonly Regex NUMBR_REGEX = new Regex (@"^-?\d+$");
		public readonly Regex NUMBAR_REGEX = new Regex(@"^(-?\d*\.\d+)$");
		public readonly Regex YARN_REGEX = new Regex("^(?m)(?<OpeningQuotes>\")(?<StringLiteral>[^\"]*)(?<ClosingQuotes>\")$");
		public readonly Regex TROOF_REGEX = new Regex ("^(WIN)|(FAIL)$");
		private readonly Regex TYPE_REGEX = new Regex ("^NUMBR|NUMBAR|YARN|TROOF|NOOB|TYPE");

		// CONDITIONAL STATEMENTS
		public readonly Regex O_RLY_REGEX = new Regex(@"^\s*O RLY");
		public readonly Regex YA_RLY_REGEX = new Regex(@"^\s*YA RLY");
		public readonly Regex NO_WAI_REGEX = new Regex(@"^\s*NO WAI");
		public readonly Regex OIC_REGEX = new Regex(@"^\s*OIC");

		// SWITCH CASE STATEMENTS
		public readonly Regex WTF_REGEX = new Regex(@"^\s*WTF");
		public readonly Regex OMG_REGEX = new Regex(@"^\s*OMG");
		public readonly Regex OMGWTF_REGEX = new Regex(@"^\s*OMGWTF");
		public readonly Regex MKAY_REGEX = new Regex(@"^\s*MKAY");

		// CONCATENATION OPERATOR
		public readonly Regex SMOOSH_REGEX = new Regex(@"^SMOOSH");

		// CONSTRUCTOR
		public LexicalAnalyzer ()
		{
			this.tokensArrayList = new ArrayList ();
		}

		public ArrayList getTokenArrayList(){
			return tokensArrayList;
		}
		private void addToken(String lexeme, String type, Keyword keyword, int lineNumber){
			this.tokensArrayList.Add(new Token(lexeme, type, keyword, lineNumber));
		}
			
		protected Dictionary<String, String> createLexemeDictionary()
		{
			Dictionary<String, String> lexemesDictionary = new Dictionary<String, String>();
			lexemesDictionary.Add ("HAI", "Start of the Program Delimiter");
			lexemesDictionary.Add ("KTHXBYE", "End of the Program Delimiter");
			lexemesDictionary.Add ("I HAS A", "Variable Declaration");
			lexemesDictionary.Add ("BTW", "Line Comment Declaration");
			lexemesDictionary.Add ("OBTW", "Start of Multiline Comment");
			lexemesDictionary.Add ("TLDR", "End of Multiline Comment");
			lexemesDictionary.Add ("VISIBLE", "Printing Keyword");
			lexemesDictionary.Add ("GIMMEH", "Input Keyword");
			lexemesDictionary.Add ("SUM OF", "Arithmetic Operator");
			lexemesDictionary.Add ("DIFF OF", "Arithmetic Operator");
			lexemesDictionary.Add ("PRODUKT OF", "Arithmetic Operator");
			lexemesDictionary.Add ("QUOSHUNT OF", "Arithmetic Operator");
			lexemesDictionary.Add ("MOD OF", "Arithmetic Operator");
			lexemesDictionary.Add ("BIGGR OF", "Arithmetic Operator");
			lexemesDictionary.Add ("SMALLR OF", "Arithmetic Operator");
			lexemesDictionary.Add ("BOTH OF", "Logical Operator");
			lexemesDictionary.Add ("EITHER OF", "Logical Operator");
			lexemesDictionary.Add ("WON OF", "Logical Operator");
			lexemesDictionary.Add ("NOT", "Logical Operator");
			lexemesDictionary.Add ("ALL OF", "Logical Operator");
			lexemesDictionary.Add ("ANY OF", "Logical Operator");
			lexemesDictionary.Add ("BOTH SAEM", "Comparison Operator");
			lexemesDictionary.Add ("DIFFRINT", "Comparison Operator Operator");
			lexemesDictionary.Add ("O RLY", "Start of Condition Delimiter");
			lexemesDictionary.Add ("YA RLY", "If Construct");
			lexemesDictionary.Add ("NO WAI", "Else Construct");
			lexemesDictionary.Add ("OIC", "End Delimiter");
			lexemesDictionary.Add ("WTF", "Start of Switch-Case Delimiter");
			lexemesDictionary.Add ("OMG", "Case Declaration");
			lexemesDictionary.Add ("OMGWTF", "Default Declaration");
			lexemesDictionary.Add ("ITZ", "Initialization Assignment Operator");
			lexemesDictionary.Add ("AN", "Conjunction Operator");
			lexemesDictionary.Add ("SMOOSH", "Concatenation Operator");
			lexemesDictionary.Add ("MKAY", "End Delimiter");
			lexemesDictionary.Add ("R", "Assignment Operator");
			lexemesDictionary.Add ("VARIABLE", "Variable Identifier");
			lexemesDictionary.Add ("NUMBR", "Numbr Literal");
			lexemesDictionary.Add ("NUMBAR", "Numbar Literal");
			lexemesDictionary.Add ("YARN", "Yarn Literal");
			lexemesDictionary.Add ("TROOF", "Troof Literal");
			return lexemesDictionary;
		}

		protected String checkKeywordType(String keyword){
			if (HAI_REGEX.Match(keyword).Success){ return "HAI"; }
			else if(KTHXBYE_REGEX.Match(keyword).Success){ return "KTHXBYE"; }
			else if(R_REGEX.Match(keyword).Success){ return "R"; }
			else if(I_HAS_A_REGEX.Match(keyword).Success){ return "I HAS A"; }
			else if(BTW_REGEX.Match(keyword).Success){ return "BTW"; }
			else if(OBTW_REGEX.Match(keyword).Success){ return "OBTW"; }
			else if(TLDR_REGEX.Match(keyword).Success){ return "TLDR"; }
			else if(VISIBLE_REGEX.Match(keyword).Success){ return "VISIBLE"; }
			else if(GIMMEH_REGEX.Match(keyword).Success){ return "GIMMEH"; }
			else if(SUM_OF_REGEX.Match(keyword).Success){ return "SUM OF"; }
			else if(DIFF_OF_REGEX.Match(keyword).Success){ return "DIFF OF"; }
			else if(PRODUKT_OF_REGEX.Match(keyword).Success){ return "PRODUKT OF"; }
			else if(QUOSHUNT_OF_REGEX.Match(keyword).Success){ return "QUOSHUNT OF"; }
			else if(MOD_OF_REGEX.Match(keyword).Success){ return "MOD OF"; }
			else if(BIGGR_OF_REGEX.Match(keyword).Success){ return "BIGGR OF"; }
			else if(SMALLR_OF_REGEX.Match(keyword).Success){ return "SMALLR OF"; }
			else if(BOTH_OF_REGEX.Match(keyword).Success){ return "BOTH OF"; }
			else if(EITHER_OF_REGEX.Match(keyword).Success){ return "EITHER OF"; }
			else if(WON_OF_REGEX.Match(keyword).Success){ return "WON OF"; }
			else if(NOT_REGEX.Match(keyword).Success){ return "NOT"; }
			else if(ALL_OF_REGEX.Match(keyword).Success){ return "ALL OF"; }
			else if(ANY_OF_REGEX.Match(keyword).Success){ return "ANY OF"; }
			else if(BOTH_SAEM_REGEX.Match(keyword).Success){ return "BOTH SAEM"; }
			else if(DIFFRINT_REGEX.Match(keyword).Success){ return "DIFFRINT"; }
			else if(O_RLY_REGEX.Match(keyword).Success){ return "O RLY"; }
			else if(YA_RLY_REGEX.Match(keyword).Success){ return "YA RLY"; }
			else if(NO_WAI_REGEX.Match(keyword).Success){ return "NO WAI"; }
			else if(OIC_REGEX.Match(keyword).Success){ return "OIC"; }
			else if(WTF_REGEX.Match(keyword).Success){ return "WTF"; }
			else if(OMG_REGEX.Match(keyword).Success){ return "OMG"; }
			else if(OMGWTF_REGEX.Match(keyword).Success){ return "OMGWTF"; }
			else if(ITZ_REGEX.Match(keyword).Success){ return "ITZ"; }
			else if(AN_REGEX.Match(keyword).Success){ return "AN"; }
			else if(SMOOSH_REGEX.Match(keyword).Success){ return "SMOOSH"; }
			else if(MKAY_REGEX.Match(keyword).Success){ return "MKAY"; }
			else if(NUMBR_REGEX.Match(keyword).Success) { return "NUMBR"; }
			else if(NUMBAR_REGEX.Match(keyword).Success) { return "NUMBAR"; }
			else if(YARN_REGEX.Match(keyword).Success) { return "YARN"; }
			else if(TROOF_REGEX.Match(keyword).Success) { return "TROOF"; }
			else if(VARIABLE_REGEX.Match(keyword).Success) {return "VARIABLE"; }
			return "Unidentified";
		}
		protected String checkLiteralType(String keyword){
			if(NUMBR_REGEX.Match(keyword).Success) { return "NUMBR"; }
			else if(NUMBAR_REGEX.Match(keyword).Success) { return "NUMBAR"; }
			else if(YARN_REGEX.Match(keyword).Success) { return "YARN"; }
			else if(TROOF_REGEX.Match(keyword).Success) { return "TROOF"; }
			//else if(VARIABLE_REGEX.Match(keyword).Success) {return "VARIABLE"; }
			return "Unidentified";
		}

		public void analyze(){
			MainClass.win.clearTokens();
			Dictionary <String, String> lexemesDictionary = createLexemeDictionary ();
			Stack pairedKeywordsStack = new Stack();
			pairedKeywordsStack.Push ("start");
			String currentWord = "";
			String currentWordType = "";
			bool mustAppend = false;
			bool mustIgnore = false;
			bool multilineMustIgnore = false;
			String lastAppended = "";
			// get each line from the editorTextView
			String[] lines = MainClass.win.getEditorText().Split (new char[]{ '\n' });
			String[] words;
			for (int lineCount = 0; lineCount < lines.Length; lineCount++) {
				if (String.IsNullOrWhiteSpace (lines [lineCount])) continue;
				if (!multilineMustIgnore && !mustIgnore && lastAppended != "TLDR") {
					this.addToken ("\n", "Statement Delimiter", Keyword.DELIMITER, lineCount + 1);
					MainClass.win.appendTokens ("\n", "Statement Delimiter");
				}
				mustAppend = false;
				mustIgnore = false;
				lastAppended = "";
				words = Regex.Matches (lines [lineCount], @"[\""].+?[\""]|[^ ]+").Cast<Match> ().Select (m => m.Value).ToArray ();
				for(int wordCount = 0; wordCount < words.Length; wordCount++){
					if (String.IsNullOrWhiteSpace(words[wordCount])) continue;
					if (mustIgnore) {
						break;
					}
					else if(mustAppend){
						currentWord = currentWord + " " + words[wordCount];	
						currentWord = currentWord.Trim ();
					}
					else{
						currentWord = words[wordCount].Trim();
					}
					if (currentWord == "TLDR") {
						multilineMustIgnore = false;
					} 
					else if (multilineMustIgnore) {
						break;
					}
					currentWordType = checkKeywordType (currentWord);
					Match match = Regex.Match (currentWord, 
						@"^\s*HAI|^\s*KTHXBYE|^\s*BTW|^\s*I HAS A|^\s*ITZ|^\s*OBTW|^\s*TLDR|^\s*BOTH OF|^\s*EITHER OF|^\s*WON OF|^\s*SMOOSH|^\s*ALL OF|^\s*ANY OF|^\s*NOT|^\s*SUM OF|^\s*DIFF OF|^\s*PRODUKT OF|^\s*QUOSHUNT OF|^\s*MOD OF|^\s*BIGGR OF|^\s*SMALLR OF|\s*AN|^\s*MKAY|^\s*BOTH SAEM|^\s*DIFFRINT|^\s*O RLY[?]|^\s*YA RLY|^\s*MEBBE|^\s*NO WAI|^\s*OIC|^\s*WTF[?]|^\s*OMG|^\s*OMGWTF|^\s*GTFO|^\s*VISIBLE|^\s*GIMMEH|^\s*R");				
					if(!match.Success){
						Match separatedKeys = Regex.Match (currentWord,
							@"^\s*I|^\s*I HAS|^\s*EITHER|^\s*WON|^\s*ALL|^\s*ANY|^\s*SUM|^\s*DIFF|^\s*PRODUKT|^\s*QUOSHUNT|^\s*MOD|^\s*BIGGR|^\s*SMALLR|^\s*BOTH|^\s*O|^\s*YA|^\s*NO");
						// If it can match a phrase, append next word to the currentword
						if (separatedKeys.Success) {
							mustAppend = true;
						} 
						else {
							if (currentWordType == "NUMBR") {
								MainClass.win.appendTokens (currentWord, lexemesDictionary ["NUMBR"]);
								this.addToken (currentWord, lexemesDictionary["NUMBR"], Keyword.NUMBR, lineCount + 1);
							}
							else if (currentWordType == "NUMBAR") {
								MainClass.win.appendTokens (currentWord, lexemesDictionary ["NUMBAR"]);
								this.addToken (currentWord, lexemesDictionary["NUMBAR"], Keyword.NUMBAR, lineCount + 1);
							}
							else if (currentWordType == "YARN") {
								MainClass.win.appendTokens (currentWord, lexemesDictionary ["YARN"]);
								this.addToken (currentWord, lexemesDictionary["YARN"], Keyword.YARN, lineCount + 1);
							}
							else if (currentWordType == "TROOF") {
								MainClass.win.appendTokens (currentWord, lexemesDictionary ["TROOF"]);
								this.addToken (currentWord, lexemesDictionary["TROOF"], Keyword.TROOF, lineCount + 1);
							}
							else if (currentWordType == "VARIABLE") {
								MainClass.win.appendTokens (currentWord, lexemesDictionary ["VARIABLE"]);
								this.addToken (currentWord, lexemesDictionary["VARIABLE"], Keyword.VARIABLE, lineCount + 1);
							}
						}
						//If not, check if expectedVar flag is on
					}
					// It is a keyword
					else {
						mustAppend = false;
						if (currentWordType == "BTW") {
							MainClass.win.appendTokens (currentWord, lexemesDictionary ["BTW"]);
							mustIgnore = true;
							break;
						} else if (currentWordType == "OBTW") {
							MainClass.win.appendTokens (currentWord, lexemesDictionary ["OBTW"]);
							multilineMustIgnore = true;
						} else if (currentWordType == "TLDR") {
							MainClass.win.appendTokens (currentWord, lexemesDictionary ["TLDR"]);
							multilineMustIgnore = false;
							lastAppended = "TLDR";
						}
						if (currentWordType == "HAI") {
							MainClass.win.appendTokens (currentWord, lexemesDictionary ["HAI"]);
							this.addToken (currentWord, lexemesDictionary["HAI"], Keyword.HAI, lineCount + 1);
						} 
						else if (currentWordType == "KTHXBYE") {
							MainClass.win.appendTokens (currentWord, lexemesDictionary ["KTHXBYE"]);
							this.addToken (currentWord, lexemesDictionary["KTHXBYE"], Keyword.KTHXBYE, lineCount + 1);
						}
						else if (currentWordType == "I HAS A") {
							MainClass.win.appendTokens (currentWord, lexemesDictionary ["I HAS A"]);
							this.addToken (currentWord, lexemesDictionary["I HAS A"], Keyword.I_HAS_A, lineCount + 1);
						} 
						else if (currentWordType == "GIMMEH") {
							MainClass.win.appendTokens (currentWord, lexemesDictionary ["GIMMEH"]);
							this.addToken (currentWord, lexemesDictionary["GIMMEH"], Keyword.GIMMEH, lineCount + 1);
						} 
						else if (currentWordType == "VISIBLE") {
							MainClass.win.appendTokens (currentWord, lexemesDictionary ["VISIBLE"]);
							this.addToken (currentWord, lexemesDictionary["VISIBLE"], Keyword.VISIBLE, lineCount + 1);
						} 
						else if (currentWordType == "SUM OF") {
							MainClass.win.appendTokens (currentWord, lexemesDictionary ["SUM OF"]);
							this.addToken (currentWord, lexemesDictionary["SUM OF"], Keyword.SUM_OF, lineCount + 1);
						} 
						else if (currentWordType == "DIFF OF") {
							MainClass.win.appendTokens (currentWord, lexemesDictionary ["DIFF OF"]);
							this.addToken (currentWord, lexemesDictionary["DIFF OF"], Keyword.DIFF_OF, lineCount + 1);
						} 
						else if (currentWordType == "PRODUKT OF") {
							MainClass.win.appendTokens (currentWord, lexemesDictionary ["PRODUKT OF"]);
							this.addToken (currentWord, lexemesDictionary["PRODUKT OF"], Keyword.PRODUKT_OF, lineCount + 1);
						} 
						else if (currentWordType == "QUOSHUNT OF") {
							MainClass.win.appendTokens (currentWord, lexemesDictionary ["QUOSHUNT OF"]);
							this.addToken (currentWord, lexemesDictionary["QUOSHUNT OF"], Keyword.QUOSHUNT_OF, lineCount + 1);
						} 
						else if (currentWordType == "MOD OF") {
							MainClass.win.appendTokens (currentWord, lexemesDictionary ["MOD OF"]);
							this.addToken (currentWord, lexemesDictionary["MOD OF"], Keyword.MOD_OF, lineCount + 1);
						}
						else if (currentWordType == "BIGGR OF") {
							MainClass.win.appendTokens (currentWord, lexemesDictionary ["BIGGR OF"]);
							this.addToken (currentWord, lexemesDictionary["BIGGR OF"], Keyword.BIGGR_OF, lineCount + 1);
						} 
						else if (currentWordType == "SMALLR OF") {
							MainClass.win.appendTokens (currentWord, lexemesDictionary ["SMALLR OF"]);
							this.addToken (currentWord, lexemesDictionary["SMALLR OF"], Keyword.SMALLR_OF, lineCount + 1);
						} 
						else if (currentWordType == "BOTH OF") {
							MainClass.win.appendTokens (currentWord, lexemesDictionary ["BOTH OF"]);
							this.addToken (currentWord, lexemesDictionary["BOTH OF"], Keyword.BOTH_OF, lineCount + 1);
						} 
						else if (currentWordType == "EITHER OF") {
							MainClass.win.appendTokens (currentWord, lexemesDictionary ["EITHER OF"]);
							this.addToken (currentWord, lexemesDictionary["EITHER OF"], Keyword.EITHER_OF, lineCount + 1);
						} 
						else if (currentWordType == "WON OF") {
							MainClass.win.appendTokens (currentWord, lexemesDictionary ["WON OF"]);
							this.addToken (currentWord, lexemesDictionary["WON OF"], Keyword.WON_OF, lineCount + 1);
						} 
						else if (currentWordType == "NOT") {
							MainClass.win.appendTokens (currentWord, lexemesDictionary ["NOT"]);
							this.addToken (currentWord, lexemesDictionary["NOT"], Keyword.NOT, lineCount + 1);
						} 
						else if (currentWordType == "ALL OF") {
							MainClass.win.appendTokens (currentWord, lexemesDictionary ["ALL OF"]);
							this.addToken (currentWord, lexemesDictionary["ALL OF"], Keyword.ALL_OF, lineCount + 1);
						} 
						else if (currentWordType == "ANY OF") {
							MainClass.win.appendTokens (currentWord, lexemesDictionary ["ANY OF"]);
							this.addToken (currentWord, lexemesDictionary["ANY OF"], Keyword.ANY_OF, lineCount + 1);
						} 
						else if (currentWordType == "BOTH SAEM") {
							MainClass.win.appendTokens (currentWord, lexemesDictionary ["BOTH SAEM"]);
							this.addToken (currentWord, lexemesDictionary["BOTH SAEM"], Keyword.BOTH_SAEM, lineCount + 1);
						} 
						else if (currentWordType == "DIFFRINT") {
							MainClass.win.appendTokens (currentWord, lexemesDictionary ["DIFFRINT"]);
							this.addToken (currentWord, lexemesDictionary["DIFFRINT"], Keyword.DIFFRINT, lineCount + 1);
						} 
						else if (currentWordType == "O RLY") {
							MainClass.win.appendTokens (currentWord, lexemesDictionary ["O RLY"]);
							this.addToken (currentWord, lexemesDictionary["O RLY"], Keyword.O_RLY, lineCount + 1);
						} 
						else if (currentWordType == "YA RLY") {
							MainClass.win.appendTokens (currentWord, lexemesDictionary ["YA RLY"]);
							this.addToken (currentWord, lexemesDictionary["YA RLY"], Keyword.YA_RLY, lineCount + 1);
						} 
						else if (currentWordType == "NO WAI") {
							MainClass.win.appendTokens (currentWord, lexemesDictionary ["NO WAI"]);
							this.addToken (currentWord, lexemesDictionary["NO WAI"], Keyword.NO_WAI, lineCount + 1);
						} 
						else if (currentWordType == "OIC") {
							MainClass.win.appendTokens (currentWord, lexemesDictionary ["OIC"]);
							this.addToken (currentWord, lexemesDictionary["OIC"], Keyword.OIC, lineCount + 1);
						} 
						else if (currentWordType == "WTF") {
							MainClass.win.appendTokens (currentWord, lexemesDictionary ["WTF"]);
							this.addToken (currentWord, lexemesDictionary["WTF"], Keyword.WTF, lineCount + 1);
						} 
						else if (currentWordType == "OMG") {
							MainClass.win.appendTokens (currentWord, lexemesDictionary ["OMG"]);
							this.addToken (currentWord, lexemesDictionary["OMG"], Keyword.OMG, lineCount + 1);
						} 
						else if (currentWordType == "OMGWTF") {
							MainClass.win.appendTokens (currentWord, lexemesDictionary ["OMGWTF"]);
							this.addToken (currentWord, lexemesDictionary["OMGWTF"], Keyword.OMGWTF, lineCount + 1);
						} 
						else if (currentWordType == "ITZ") {
							MainClass.win.appendTokens (currentWord, lexemesDictionary ["ITZ"]);
							this.addToken (currentWord, lexemesDictionary["ITZ"], Keyword.ITZ, lineCount + 1);
						} 
						else if (currentWordType == "AN") {
							MainClass.win.appendTokens (currentWord, lexemesDictionary ["AN"]);
							this.addToken (currentWord, lexemesDictionary["AN"], Keyword.AN, lineCount + 1);
						} 
						else if (currentWordType == "SMOOSH") {
							MainClass.win.appendTokens (currentWord, lexemesDictionary ["SMOOSH"]);
							this.addToken (currentWord, lexemesDictionary["SMOOSH"], Keyword.SMOOSH, lineCount + 1);
						} 
						else if (currentWordType == "MKAY") {
							MainClass.win.appendTokens (currentWord, lexemesDictionary ["MKAY"]);
							this.addToken (currentWord, lexemesDictionary["MKAY"], Keyword.MKAY, lineCount + 1);
						} 
						else if (currentWordType == "R") {
							MainClass.win.appendTokens (currentWord, lexemesDictionary ["R"]);
							this.addToken (currentWord, lexemesDictionary["R"], Keyword.R, lineCount + 1);
						}

					}
				}
			}

		}
	}
}

