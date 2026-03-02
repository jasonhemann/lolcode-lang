module Loco {
	exports SyntaxNodes;
	exports backend;
	exports frontend;


	requires javafx.controls;
	requires javafx.fxml;
	requires org.fxmisc.richtext;
	requires flowless;

	opens frontend to javafx.fxml;

}