package frontend;

import java.io.File;
import java.io.IOException;

import backend.Evaluator;
import backend.Lexer;
import backend.Parser;
import backend.Token;
import backend.TokenKind;
import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.image.Image;
import javafx.stage.Stage;

public class Main extends Application {

	public static void main(String[] args) {
		//startEvaluator();
		//startLexer();
		launch(args);
	}
	
	static void startLexer() {
		File fp = new File("src/main/java/sample.lol");
		Lexer lexer = new Lexer(fp);
		//lexer.viewLexemes();
		
		Token token;
		do {
			token = lexer.nextToken();
			
			if (token.getTokenKind() != TokenKind.badToken) token.viewToken();
		} while (token.getTokenKind() != TokenKind.eofToken);
		
		System.exit(0);
	}
	
	static void startParser() {
		File fp = new File("src/main/java/sample.lol");
		Parser parser = new Parser(fp);
		parser.parse();
		parser.viewErrors();
		
		System.exit(0);
	}
	
	static void startEvaluator() {
		File fp = new File("src/main/java/sample.lol");
		Evaluator evaluator = new Evaluator(fp);
		
		evaluator.viewParseTree();
		//System.out.println(evaluator.getStrParseTree());
		evaluator.viewParserErrors();
		
		
		while (!evaluator.isPCEmpty()) {
			evaluator.nextInstruction();
		}
		
		
		System.out.println(evaluator.getEvalDiagnostics());
		
		System.exit(0);
	}
	
	@Override
	public void start(Stage primaryStage) throws IOException {
		Scene scene = new Scene(loadFXML("Window"), WindowController.WINDOW_WIDTH, WindowController.WINDOW_HEIGHT);

		scene.getStylesheets().add(getClass().getResource("Window.css").toExternalForm());

		primaryStage.setScene(scene);
		primaryStage.setTitle("Loco - Lolcode Interpreter");
		primaryStage.getIcons().add(new Image(getClass().getResourceAsStream("Loco_48.png")));

		primaryStage.setMinHeight(WindowController.WINDOW_HEIGHT);
		primaryStage.setMinWidth(WindowController.WINDOW_WIDTH);

		primaryStage.show();
	}

	private static Parent loadFXML (String fxml) throws IOException {
		FXMLLoader fxmlLoader = new FXMLLoader(Main.class.getResource(fxml + ".fxml"));
		return fxmlLoader.load();
	}
}
