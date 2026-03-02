package frontend;

import javafx.event.EventHandler;
import javafx.geometry.Pos;
import javafx.scene.Group;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.TextField;
import javafx.scene.input.KeyCode;
import javafx.scene.input.KeyEvent;
import javafx.scene.layout.VBox;
import javafx.scene.text.Font;
import javafx.scene.text.FontWeight;
import javafx.scene.text.Text;
import javafx.stage.Modality;
import javafx.stage.Stage;

public class InputWindow {
	private Scene scene;
	private Stage stage;
	private Group root;
	private VBox vbox;
	
	static private String value = "";
	
	public InputWindow (String title, String message) {
		this.stage = new Stage();
		this.root = new Group();
		this.scene = new Scene(this.root, 300, 200);
		this.vbox = new VBox();
		
		stage.initModality(Modality.APPLICATION_MODAL);
		
		this.setStage(title, message);
	}
	
	public void setStage(String title, String message) {
		Text text = new Text(message);
		TextField textField = new TextField();
		Button btn = new Button("Submit");
		
		btn.setOnAction(e -> {
			InputWindow.value = textField.getText();
			stage.close();
		});
		
		vbox.setOnKeyPressed(new EventHandler<KeyEvent>() {
			@Override
			public void handle(KeyEvent event) {
				if (event.getCode() == KeyCode.ENTER) btn.fire();
			}

		});
		
		text.setFont(Font.font("Segoe UI", FontWeight.BOLD, 15));
		
		vbox.setAlignment(Pos.CENTER);
		vbox.setLayoutX(300/4);
		vbox.setLayoutY(200/6);
		vbox.setSpacing(10);
		
		
		vbox.getChildren().addAll(text, textField, btn);
		root.getChildren().add(vbox);
		stage.setTitle(title);
		stage.setScene(scene);
	}
	
	public void display() {
		stage.showAndWait();
	}
	
	public String getValue() {
		return value;
	}
}
