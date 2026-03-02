using System;
using LolcodeInterpreter;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
namespace LolcodeInterpreter
{
	public class Parser
	{
		ArrayList tokensArrayList;
		private int currentPosition;

		public Parser (ArrayList tokensArrayList)
		{
			this.currentPosition = 1;
			this.tokensArrayList = tokensArrayList;
			enumerateReceivedTokens ();
		}

		public void enumerateReceivedTokens(){
			foreach (Token token in tokensArrayList){
				Console.WriteLine (token.getKeyword ());
			}
		}

		private bool checkType(Keyword keyword){
			if (currentPosition == tokensArrayList.Count) return false;
			Token a = (Token)tokensArrayList [currentPosition++];
			if (a.getKeyword () == keyword)
				return true;
			else {
				return false;
			}
		}

		public bool linebreak(){
			if (currentPosition == tokensArrayList.Count) return false;
			Token a = (Token)tokensArrayList [currentPosition++];
			if (a.getKeyword () == Keyword.DELIMITER)
				return true;
			else
				return false;
		}
		public bool program(){
			int save = currentPosition;


			return (currentPosition = save) == save & checkType (Keyword.HAI) && plus_statement() && checkType(Keyword.KTHXBYE);
		}

		public bool plus_statement(){
			int save = currentPosition;
			Console.WriteLine($"plus_init {currentPosition}");
			if ((currentPosition = save) == save & linebreak () && print () && linebreak ())
				return true;
			else if ((currentPosition = save) == save & linebreak ()) {
				Console.WriteLine ($"plus_init after {currentPosition}");
				return true;
				
			}
			else return false;
		}
		public bool print(){
			int save = currentPosition;
			//if ((currentPosition = save) == save & checkType(Keyword.VISIBLE) && variable ()){
			//	return true;
			//}
			if ((currentPosition = save) == save & checkType (Keyword.VISIBLE) && expr()) {
				return true;
			}
			//else if ((currentPosition = save) == save & checkType ("Printing Keyword") && variable ())
			//	return true;
				// TODO: shit
			else
				return false;
		}

		public bool variable(){
			return true;
		}

		public bool expr(){
			int save = currentPosition;
			if ((currentPosition = save) == save & arithmetic ()) {
				return true;
			}
			else if ((currentPosition = save) == save & checkType (Keyword.NUMBR))
				return true;
			else if ((currentPosition = save) == save & checkType (Keyword.NUMBAR))
				return true;
			else
				return false;
		}

		public bool arithmetic(){
			int save = currentPosition;
			if ((currentPosition = save) == save & add ()) {
				return true;
			} 
			else if ((currentPosition = save) == save & subtract ()) {
				return true;
			}
			else if ((currentPosition = save) == save & multiply ()) {
				return true;
			}
			else if ((currentPosition = save) == save & divide ()) {
				return true;
			}
			else if ((currentPosition = save) == save & modulo ()) {
				return true;
			}
			else if ((currentPosition = save) == save & greaterThan ()) {
				return true;
			}
			else if ((currentPosition = save) == save & lessThan ()) {
				return true;
			}
			else{
				return false;
			}

			


			
		}

		public bool add(){
			int save = currentPosition;
			if ((currentPosition = save) == save & checkType (Keyword.SUM_OF) && expr() && checkType(Keyword.AN) && expr())
				return true;
			else
				return false;
			
		}

		public bool subtract(){
			int save = currentPosition;
			if ((currentPosition = save) == save & checkType (Keyword.DIFF_OF) && expr () && checkType (Keyword.AN) && expr ()) {
				return true;
			} 
			else {
				return false;
			}
		}

		public bool multiply(){
			int save = currentPosition;
			if ((currentPosition = save) == save & checkType (Keyword.PRODUKT_OF) && expr () && checkType (Keyword.AN) && expr ()) {
				return true;
			} 
			else {
				return false;
			}
		}

		public bool divide(){
			int save = currentPosition;
			if ((currentPosition = save) == save & checkType (Keyword.QUOSHUNT_OF) && expr () && checkType (Keyword.AN) && expr ()) {
				return true;
			} 
			else {
				return false;
			}
		}

		public bool modulo(){
			int save = currentPosition;
			if ((currentPosition = save) == save & checkType (Keyword.MOD_OF) && expr () && checkType (Keyword.AN) && expr ()) {
				return true;
			} 
			else {
				return false;
			}
		}

		public bool greaterThan(){
			int save = currentPosition;
			if ((currentPosition = save) == save & checkType (Keyword.BIGGR_OF) && expr () && checkType (Keyword.AN) && expr ()) {
				return true;
			} 
			else {
				return false;
			}
		}

		public bool lessThan(){
			int save = currentPosition;
			if ((currentPosition = save) == save & checkType (Keyword.SMALLR_OF) && expr () && checkType (Keyword.AN) && expr ()) {
				return true;
			} 
			else {
				return false;
			}
		}


		public bool or()
		{
			int save = currentPosition;
            if ((currentPosition = save) == save & checkType(Keyword.EITHER_OF) && expr() && checkType(Keyword.AN) && expr())
				return true;
			else
				return false;

		}




	}
}

