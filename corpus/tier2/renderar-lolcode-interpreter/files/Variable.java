//Variable.java
import javax.swing.*;

public class Variable{
	private String varname;
	private String type;
	private String value;

	public Variable(String varname, String type, String value){
		this.varname = varname;
		this.type = type;
		this.value = value;

		this.show();
	}

	//methods
	public void show(){
		System.out.println(this.varname + " " + this.type + " " + this.value);
	}

	public void show(JTextArea idHolder, JTextArea valHolder){
		idHolder.append(this.varname + "\n");
		valHolder.append(this.value + "\n");
	}
}