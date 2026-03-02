package frontend;

import java.io.*;
import java.net.URL;
import java.util.ResourceBundle;
import java.util.Scanner;

import backend.Evaluator;
import backend.SymTabEntry;
import backend.Token;
import backend.TokenKind;
import javafx.beans.value.ChangeListener;
import javafx.beans.value.ObservableValue;
import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.control.*;
import javafx.scene.control.Alert.AlertType;
import javafx.scene.control.cell.PropertyValueFactory;
import javafx.scene.input.KeyCode;
import javafx.scene.input.KeyEvent;
import javafx.scene.layout.StackPane;
import javafx.scene.text.Font;
import javafx.scene.text.Text;
import javafx.stage.FileChooser;
import javafx.stage.Stage;
import org.fxmisc.flowless.VirtualizedScrollPane;
import org.fxmisc.richtext.CodeArea;

public class WindowController implements Initializable {
	private Evaluator evaluator;
	
	private boolean isPTreeShow;
	private boolean wrapText;
	private boolean hideHighlight;

	private String codeBackup;
	private String fileName;
	private int loopLimit;

	private CodeHighlighter codeHighlighter;
	private CodeArea codeArea;

	public final static int WINDOW_HEIGHT = 675;
	public final static int WINDOW_WIDTH = 1200;
	
	@FXML private SplitPane verticalSplit;
	@FXML private SplitPane horizontalSplit;

	@FXML private StackPane codeStackPane;

	@FXML private TextArea consoleTextArea;
	@FXML private TextArea parseTreeTextArea;
	
	@FXML private TableView<Token> tokenTable;
	@FXML private TableColumn<Token, String> lexemeColumn;
	@FXML private TableColumn<Token, TokenKind> tokenKindColumn;
	
	@FXML private TableView<SymTabEntry> symbolTable;
	@FXML private TableColumn<SymTabEntry, String> identifierColumn;
	@FXML private TableColumn<SymTabEntry, String> valueColumn;
	
	@FXML private Text symbolTableLabel;
	@FXML private Label programStatus;
	
	@FXML private MenuItem nextLineBtn;
	@FXML private ToggleButton terminalBtn;
	@FXML private ToggleButton lexemeBtn;
	@FXML private ToggleButton symTabBtn;

	
	@Override
	public void initialize(URL arg0, ResourceBundle arg1) {
		codeHighlighter = new CodeHighlighter();

		lexemeColumn.setCellValueFactory(new PropertyValueFactory<Token, String>("value"));
		tokenKindColumn.setCellValueFactory(new PropertyValueFactory<Token, TokenKind>("tokenKind"));
		
		identifierColumn.setCellValueFactory(new PropertyValueFactory<SymTabEntry, String>("identifier"));
		valueColumn.setCellValueFactory(new PropertyValueFactory<SymTabEntry, String>("value"));

		codeArea = codeHighlighter.getCodeArea();
		codeStackPane.getChildren().add(new VirtualizedScrollPane<>(codeArea));

		setDividerListeners();

		programStatus.setText("Idle");

		hideHighlight = isPTreeShow = wrapText = false;
		loopLimit = 999;
	}
	
	@FXML
	void openFile(ActionEvent event) {
		if (!codeArea.isEditable()) return;
		
		FileChooser filechooser = new FileChooser();
		FileChooser.ExtensionFilter extFilter = new FileChooser.ExtensionFilter("Lolcode File", "*.lol");
		
		filechooser.getExtensionFilters().add(extFilter);
		File file = filechooser.showOpenDialog(null);
		
		if (file != null) {
			codeArea.clear();
			fileName = file.getName();
			programStatus.setText(fileName);
			
			try {
				Scanner sc = new Scanner(file);
				
				while(sc.hasNextLine()) {
					codeArea.appendText(sc.nextLine() + "\n");
				}
				
				sc.close();

				codeArea.displaceCaret(0);
				codeArea.requestFollowCaret();
				
			} catch (FileNotFoundException e) {
				e.printStackTrace();
			}
		}
		
	}
	
	@FXML
	void saveFile(ActionEvent event) {
		if (!codeArea.isEditable()) return;
		
		FileChooser filechooser = new FileChooser();
		FileChooser.ExtensionFilter extFilter = new FileChooser.ExtensionFilter("Lolcode File", "*.lol");
		
		filechooser.getExtensionFilters().add(extFilter);
		File file = filechooser.showSaveDialog(null);
		
		if (file != null) {
			fileName = file.getName();
			programStatus.setText(fileName);

			try {
				FileWriter writer = new FileWriter(file);
				writer.write(codeArea.getText());
				writer.close();
				
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
	}

    @FXML
    void runProgram(ActionEvent event) {
		long startTime, totalTime;
    	if (!codeArea.isEditable()) return;
    	
    	startTime = System.nanoTime();

    	try {
    		String fp = codeArea.getText();
        	fp = fp.replaceAll("\t", "");
        	
        	evaluator = new Evaluator(fp, this);
    	} catch (Exception e) {
			programStatus.setText(fileName + " > Java Fatal ERROR");
    		return;
    	}

		programStatus.setText(fileName + " > Program running");
    	evaluator.changeLoopLimit(loopLimit);
    	
    	//	hide console text area
    	verticalSplit.setDividerPosition(0, 1.0);
    	
    	//	update symboltable and tokentable
    	symbolTable.getItems().clear();
    	tokenTable.getItems().clear();
    	for (Token token : evaluator.getTokens()) {
    		tokenTable.getItems().add(token);
    	}
    	
    	//	update parsetree
    	parseTreeTextArea.clear();
    	parseTreeTextArea.appendText(evaluator.getStrParseTree());
    	
    	
    	//	check if there are any parser errors
    	consoleTextArea.clear();
    	for (String string: evaluator.getParserDiagnostics()) {
    		consoleTextArea.appendText(string + "\n");
    		verticalSplit.setDividerPosition(0, 0.8);
    	}
    	
    	//	 repeatedly executes the lines of code
    	while (!evaluator.isPCEmpty()) {
			evaluator.nextInstruction();
			updateSymbolTable();
		}
    	
    	//	check if there are any semantic analyzer errors
    	if (!evaluator.getEvalDiagnostics().isBlank()) {
    		verticalSplit.setDividerPosition(0, 0.8);
    		consoleTextArea.appendText(evaluator.getEvalDiagnostics() + "\n");
    	}

    	totalTime = System.nanoTime() - startTime;
		programStatus.setText(fileName + " > Execution completed in " + totalTime / 1000000.0 + " ms");

    	parseTreeTextArea.positionCaret(0);
    }
    
    //	does almost the same thing as runProgram() except it doesn't run instructions until the file is done
    @FXML
    void runDebug(ActionEvent event) {
    	if (!codeArea.isEditable()) return;
    	
    	try {
    		String fp = codeArea.getText();
        	fp = fp.replaceAll("\t", "");
        	
        	evaluator = new Evaluator(fp, this);
    	} catch (Exception e) {
			programStatus.setText(fileName + " > Java Fatal ERROR");
    		return;
    	}

		programStatus.setText(fileName + " > Program debugging");
    	evaluator.changeLoopLimit(loopLimit);
    	
    	verticalSplit.setDividerPosition(0, 1.0);
    	
    	symbolTable.getItems().clear();
    	tokenTable.getItems().clear();
    	for (Token token : evaluator.getTokens()) {
    		tokenTable.getItems().add(token);
    	}
    	
    	parseTreeTextArea.clear();
    	parseTreeTextArea.appendText(evaluator.getStrParseTree());
    	
    	consoleTextArea.clear();
    	for (String string: evaluator.getParserDiagnostics()) {
    		consoleTextArea.appendText(string + "\n");
    		verticalSplit.setDividerPosition(0, 0.8);
    	}
    	
    	codeBackup = codeArea.getText();
    	codeArea.clear();
    	codeArea.setEditable(false);
    	setDebugText();
    	
    	nextLineBtn.setDisable(false);
    }
    
    //	executes the next line of code
    @FXML
    void runNextLine(ActionEvent event) {
    	if (evaluator.isPCEmpty()) {
			if (!evaluator.getEvalDiagnostics().isBlank()) {
				verticalSplit.setDividerPosition(0, 0.8);
	    		consoleTextArea.appendText(evaluator.getEvalDiagnostics() + "\n");
	    	}
			
			if (!codeArea.isEditable()) {
				codeArea.clear();
				codeArea.appendText(codeBackup);
		    	codeArea.setEditable(true);
			}

			programStatus.setText(fileName + " > Debugging completed");
			nextLineBtn.setDisable(true);
    	} else {
    		evaluator.nextInstruction();
    		updateSymbolTable();
    		
    		codeArea.clear();
    		setDebugText();
    	}
    }
    
    @FXML
    void changeFont(ActionEvent event) {
    	String input = displayInputBox("Change Font Size", "Font Size: ");
    	double fontSize = 20;
    	Alert alert = new Alert(AlertType.ERROR);

    	//	check if input is empty
    	if (input.isEmpty() || input.isBlank()) {
    		alert.setHeaderText("Empty Input!");
    		alert.show();
    		
    		return;
    	}
    	
    	//	check if input is a valid number
    	try {
    		fontSize = Double.parseDouble(input);
    	} catch(Exception e) {
    		alert.setHeaderText("Invalid Input!");
    		alert.show();
    	}
    	
    	//	change font size
		codeArea.setStyle("-fx-font-size: "+fontSize+"px;");
    	consoleTextArea.setFont(Font.font("Consolas", fontSize));
    	parseTreeTextArea.setFont(Font.font("Consolas", fontSize));

    	consoleTextArea.positionCaret(0);
    	parseTreeTextArea.positionCaret(0);
    }

	@FXML
	void setCodeHighlight(ActionEvent event) {
		int pos = codeArea.getCaretPosition();

		codeHighlighter.setHightlight(hideHighlight);
		hideHighlight = !hideHighlight;

		codeBackup = codeArea.getText();
		codeArea.clear();
		codeArea.appendText(codeBackup);

		codeArea.displaceCaret(pos);
	}
    
    @FXML
    void changeLoopLimit(ActionEvent event) {
    	String input = displayInputBox("Change loop limit", "Loop Limit: ");
    	
    	Alert alert = new Alert(AlertType.ERROR);
    	
    	if (input.isEmpty() || input.isBlank()) {
    		alert.setHeaderText("Empty Input!");
    		alert.show();
    		
    		return;
    	}
    	
    	try {
    		loopLimit = Integer.parseInt(input);
    	} catch (Exception e) {
    		alert.setHeaderText("Invalid Input!");
    		alert.show();
    	}
    }
    
    @FXML
    void displayAbout(ActionEvent event) {
    	Alert alert = new Alert(AlertType.INFORMATION);
    	alert.setTitle("About");
    	alert.setHeaderText("A simple Lolcode interpreter. \n" + 
    						"Lolcode is an esoteric programming language based on an internet meme called \"lolcat\"\n" + 
    						"Learn more at: lolcode.org/");
    	alert.setContentText("Github Page:\n" + "https://github.com/jpcarreon/loco");

    	alert.showAndWait();
    }
    
    @FXML
    void showParseTree(ActionEvent event) {
    	//	sends the symboltable to the front if parsetree is showing and vice-versa
    	if (isPTreeShow) {
    		symbolTableLabel.setText("Symbol Table");
    		symbolTable.toFront();
    		parseTreeTextArea.toBack();
    		symbolTable.setVisible(true);
    		
    	} else {
    		symbolTableLabel.setText("Parse Tree");
    		symbolTable.toBack();
    		parseTreeTextArea.toFront();
    		symbolTable.setVisible(false);
    	}
    	
    	isPTreeShow = !isPTreeShow;
    }

	@FXML
	void wrapText(ActionEvent event) {
		wrapText = !wrapText;
		codeArea.setWrapText(wrapText);
	}

    @FXML
    void closeProgram(ActionEvent event) {
    	Stage stage = (Stage) tokenTable.getScene().getWindow();
    	stage.close();
    }

	@FXML
	void sidePanelButtons(ActionEvent event) {
		double dpos1 = horizontalSplit.getDividers().get(1).getPosition();
		double dpos2 = horizontalSplit.getDividers().get(0).getPosition();
		ToggleButton btn = (ToggleButton) event.getSource();
		Stage stage = (Stage) btn.getScene().getWindow();

		//	Get ideal length divider position relative to the width of the window
		double length = 1 - 236 / stage.getWidth();

		if (btn.isSelected()) {
			btn.setSelected(false);
			if (btn.getText().equals("Lexemes")) horizontalSplit.setDividerPosition(0, dpos1 - 236 / stage.getWidth());
			else if (btn.getText().equals("Symbol Table")) {
				if (dpos2 > length) horizontalSplit.setDividerPosition(0, length);
				horizontalSplit.setDividerPosition(1, length);
			}
			else verticalSplit.setDividerPosition(0, length);
		} else {
			btn.setSelected(true);
			if (btn.getText().equals("Lexemes")) horizontalSplit.setDividerPosition(0, dpos1);
			else if (btn.getText().equals("Symbol Table")) {
				horizontalSplit.setDividerPosition(1,1);
				horizontalSplit.layout();

				//	Check if the 2 dividers are close to each other
				if (dpos1 - dpos2 > 0.09) horizontalSplit.setDividerPosition(0, length);
				else horizontalSplit.setDividerPosition(0, 1);
				horizontalSplit.layout();
			}
			else verticalSplit.setDividerPosition(0, 1);
		}
	}

    @FXML
    void setHotKey(KeyEvent event) {
    	if (event.getCode() == KeyCode.F6) runProgram(null);
    	else if (event.getCode() == KeyCode.F7) runDebug(null);
    	else if (event.getCode() == KeyCode.F8 && !codeArea.isEditable()) runNextLine(null);
    	else if (event.getCode() == KeyCode.F12) displayAbout(null);
    }
    
    public void updateConsole(String string) {
    	//	add text to the console text area
    	if (!string.isEmpty()) {
    		verticalSplit.setDividerPosition(0, 0.8);
        	consoleTextArea.appendText(string);
    	}
    }
    
    //	ask for user input
    public String getYarnInput(String varid) {
    	InputWindow popup = new InputWindow("GIMMEH", "Set " + varid + ": ");
    	Alert alert = new Alert(AlertType.ERROR);
    	String string = new String();
    	
    	popup.display();
    	
    	string = popup.getValue();
    	
    	//	input must not be empty
    	if (string.isEmpty() || string.isBlank()) {
    		alert.setHeaderText("Empty Input!");
    		alert.show();
    		
    		return "";
    	}
    	
    	return string;
    }
    
    //	modifies the codeArea to show which line is being executed
    private void setDebugText() {
    	int counter = 0;
    	int currentLine = evaluator.getNextLineNum() - 1;
    	int caretpos = 0;

		codeArea.appendText("==== DEBUGGING MODE ====\n\n");
		for (String i : codeBackup.split("\n")) {
			if (counter++ == currentLine) {
				codeArea.appendText("=>\t" + i + "\n");
				caretpos = codeArea.getLength();
			} else {
				codeArea.appendText("\t" + i + "\n");
			}
		}

		if (currentLine > 0) {
			codeArea.displaceCaret(caretpos - 1);
			codeArea.requestFollowCaret();
		}
    }
    
    public void updateSymbolTable() {
    	symbolTable.getItems().clear();
    	for (SymTabEntry entry : evaluator.getSymbolTable()) {
    		symbolTable.getItems().add(entry);
    	}
    }

	private void setDividerListeners() {
		verticalSplit.getDividers().get(0).positionProperty().addListener(new ChangeListener<Number>() {
			@Override
			public void changed(ObservableValue<? extends Number> observableValue, Number number, Number t1) {
				if ((double) t1 < 0.98) terminalBtn.setSelected(true);
				else terminalBtn.setSelected(false);
			}
		});

		horizontalSplit.getDividers().get(0).positionProperty().addListener(new ChangeListener<Number>() {
			@Override
			public void changed(ObservableValue<? extends Number> observableValue, Number number, Number t1) {
				//	Set css of the button depending on divider positions
				double relativePos = horizontalSplit.getDividers().get(1).getPosition() - (double) t1;
				if ((double) t1 < 0.98 && relativePos > 0.09) lexemeBtn.setSelected(true);
				else lexemeBtn.setSelected(false);
			}
		});

		horizontalSplit.getDividers().get(1).positionProperty().addListener(new ChangeListener<Number>() {
			@Override
			public void changed(ObservableValue<? extends Number> observableValue, Number number, Number t1) {
				double relativePos = (double) t1 - horizontalSplit.getDividers().get(0).getPosition();
				if ((double) t1 < 0.98) symTabBtn.setSelected(true);
				else symTabBtn.setSelected(false);

				//	Update lexemebtn background based on divider positions
				if (relativePos > 0.09) lexemeBtn.setSelected(true);
				else {
					lexemeBtn.setSelected(false);
					horizontalSplit.getDividers().get(0).setPosition((double) t1 - Double.MIN_VALUE);
				}
			}
		});
	}

    private String displayInputBox(String title, String prompt) {
    	InputWindow popup = new InputWindow(title, prompt);
    	popup.display();
    	
    	return popup.getValue();
    }
}
