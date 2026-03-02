using System;

namespace LolcodeInterpreter
{
	public class Variable
	{
		String variableName;
		String variableType;
		String variableValue;
		public Variable (String varName, String varType, String varValue)
		{
			this.variableName = varName;
			this.variableType = varType;
			this.variableValue = varValue;
		}

		public String getVariableName(){
			return this.variableName;
		}

		public String getVariableType (){
			return this.variableType;

		}

		public String getVariableValue(){
			return this.variableValue;
		}

		public void setVariableValue(String varValue){
			this.variableValue = varValue;
		}

		public void setVariableType(String varType){
			this.variableType = varType;
		}
	}
}
