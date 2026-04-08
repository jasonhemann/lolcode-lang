// LexicalAnalyzer.java
import java.util.*;
import java.io.*;
import javax.swing.*;
import java.util.regex.*;

public class LexicalAnalyzer {
    // Contants
    private static final Pattern CODE_DELIMITER = Pattern.compile("^(HAI|KTHXBYE)");
    private static final Pattern OUTPUT = Pattern.compile("^(VISIBLE)");
    private static final Pattern INPUT = Pattern.compile("^(GIMMEH)");
    private static final Pattern INCOMPLETE_KEYWORD = Pattern.compile("^(I|IS|HAS|NOW|A|IM|IN|YR|ANY|EITHER|WON|ALL|OF|OUTTA|SUM|OF|DIFF|PRODUKT|QUOSHUNT|MOD|BIGGR|SMALLR|BOTH|SAEM|YA|RLY|O|RLY\\?|NO|WAI)");
    private static final Pattern INCREMENT = Pattern.compile("^(UPPIN)"); // added
    private static final Pattern RANGE_INDICATOR = Pattern.compile("^(TIL|WILE)"); // added
    private static final Pattern DECREMENT = Pattern.compile("^(NERFIN)"); // added
    private static final Pattern HARD_TYPECAST = Pattern.compile("^(MAEK)"); // added
    private static final Pattern COMMENT = Pattern.compile("^(BTW)");
    private static final Pattern COMMENT_DELIMITER = Pattern.compile("^(OBTW|TLDR)"); // changed
    private static final Pattern EXPRESSION = Pattern.compile("^(IT)");
    private static final Pattern INITIALIZE = Pattern.compile("^(ITZ)");
    private static final Pattern ASSIGNMENT = Pattern.compile("^(R)");
    private static final Pattern BOOLEAN_UNARY = Pattern.compile("^(NOT)");
    private static final Pattern BOOLEAN_END = Pattern.compile("^(MKAY)"); // added
    private static final Pattern DIFFERENT = Pattern.compile("^(DIFFRINT)"); // added
    private static final Pattern OPERATION_SEPARATOR = Pattern.compile("^(AN)");
    private static final Pattern CONCATENATE = Pattern.compile("^(SMOOSH)");
    private static final Pattern SWITCH_START = Pattern.compile("^(WTF\\?)");
    private static final Pattern CONDITION_END = Pattern.compile("^(OIC)");
    private static final Pattern ELSEIF = Pattern.compile("^(MEBBE)");
    private static final Pattern CASE = Pattern.compile("^(OMG)");
    private static final Pattern DEFAULT = Pattern.compile("^(OMGWTF)");
    private static final Pattern BREAK = Pattern.compile("^(GTFO)");
    private static final Pattern VARIABLE = Pattern.compile("^[_a-zA-Z]+[_a-zA-Z0-9]*$"); //changed
    private static final Pattern INTEGER = Pattern.compile("^-?\\d+$");
    private static final Pattern FLOAT = Pattern.compile("^-?\\d*\\.\\d+$");
    private static final Pattern STRING_DELIMITER = Pattern.compile("^\".*|.*\"$");
    private static final Pattern STRING = Pattern.compile("^\".*\"$");
    private static final Pattern BOOL = Pattern.compile("^(WIN|FAIL)$");
    private static final Pattern NEWLINE = Pattern.compile("(?s).*[\n\r].*");

    /* multi-word patterns */
    private static final Pattern IS_NOW = Pattern.compile("^(IS NOW A)"); // added
    private static final Pattern IM_IN = Pattern.compile("^(IM IN YR)"); // added
    private static final Pattern IM_OUT = Pattern.compile("^(IM OUTTA YR)"); // added
    private static final Pattern IF_ELSE_START = Pattern.compile("^(O\\sRLY\\?)"); // changed
    private static final Pattern IF = Pattern.compile("^(YA\\sRLY)");
    private static final Pattern ELSE = Pattern.compile("^(NO\\sWAI)");
    private static final Pattern COMPARISON = Pattern.compile("^(BOTH\\sSAEM)");
    private static final Pattern BOOLEAN_OR = Pattern.compile("^(ANY\\sOF)");
    private static final Pattern BOOLEAN_AND = Pattern.compile("^(ALL\\sOF)");
    private static final Pattern BOOLEAN = Pattern.compile("^(BOTH\\sOF|EITHER\\sOF|WON\\sOF)");
    private static final Pattern ARITHMETIC = Pattern.compile("^(SUM\\sOF|DIFF\\sOF|PRODUKT\\sOF|BIGGR\\sOF|SMALLR\\sOF)"); //changed
    private static final Pattern DIVISION = Pattern.compile("^(QUOSHUNT\\sOF|MOD\\sOF)"); //added
    private static final Pattern DECLARATION = Pattern.compile("^(I\\sHAS\\sA)");
    
    // Attributes
    private static boolean isComment = false; // is the file pointer pointing to a comment
    private static boolean isMiddle = false; // is the file pointer in the middle of the source code
    private static boolean isString = false;
    private Stack<String> stackOfLines;
    private Stack<Token> tokenStack;

    // Constructor
    public LexicalAnalyzer(String path){
        try {
            FileInputStream input = new FileInputStream(path);
            this.tokenStack = new Stack<Token>();
            /* Initializes the stack of lines */
            this.stackOfLines = new Stack<String>();  
            String toInsert = "";
            char letter;
            int charRead;
            do{
                charRead = input.read();
                letter = (char)charRead;
                if(letter == '\n' || charRead == -1){
                    // if(letter != '\n' && charRead == -1) toInsert = toInsert;
                    // System.out.println(toInsert);
                    this.stackOfLines.push(toInsert + " \n");
                    toInsert = "";
                }else{
                    toInsert = toInsert + letter;
                }
            }while(charRead != -1);
            input.close();
            /* end of Stack of Lines initializer */

            /* Match the Lexemes per line */

            // this.getAllMatches(stackOfLines.get(3));
            int i = 0;
            for(String line : this.stackOfLines) {
                if(line == null)continue;
                this.getAllMatches(line);
                // System.out.println(line);
            }

            // this.tokenStack.pop();
        } catch(Exception e) {
            System.out.println(e.getMessage());;
        }
    }

    public String getMatchingType(String s){
        if(CODE_DELIMITER.matcher(s).matches()){
            return "Source Code Delimiter";
        }else if(OUTPUT.matcher(s).matches()){
            return "Visible Keyword";
        }else if(INPUT.matcher(s).matches()){
            return "Gimmeh Keyword";
        }else if(INCOMPLETE_KEYWORD.matcher(s).matches()){
            return "Incomplete Keyword";
        }else if(INCREMENT.matcher(s).matches()){
            return "Increment";
        }else if(DECREMENT.matcher(s).matches()){
            return "Decrement";
        }else if(HARD_TYPECAST.matcher(s).matches()){
            return "Hard Typecast";
        }else if(COMMENT.matcher(s).matches()){
            return "Comment Unary";
        }else if(COMMENT_DELIMITER.matcher(s).matches()){
            return "Comment Delimiter";
        }else if(EXPRESSION.matcher(s).matches()){
            return "Variable Expression";
        }else if(INITIALIZE.matcher(s).matches()){
            return "Variable Initialization";
        }else if(ASSIGNMENT.matcher(s).matches()){
            return "Variable Assignment";
        }else if(BOOLEAN_UNARY.matcher(s).matches()){ 
            return "Boolean Unary"; // changed
        }else if(BOOLEAN_END.matcher(s).matches()){
            return "Boolean End"; //changed
        }else if(DIFFERENT.matcher(s).matches()){
            return "Different";
        }else if(OPERATION_SEPARATOR.matcher(s).matches()){
            return "Operation Separator";
        }else if(CONCATENATE.matcher(s).matches()){
            return "String Concatenate";
        }else if(SWITCH_START.matcher(s).matches()){
            return "Switch Start"; // added
        }else if(CONDITION_END.matcher(s).matches()){
            return "Condition End";
        }else if(ELSEIF.matcher(s).matches()){
            return "Else-If Keyword";
        }else if(CASE.matcher(s).matches()){
            return "Case Keyword";
        }else if(DEFAULT.matcher(s).matches()){
            return "Default Keyword";
        }else if(BREAK.matcher(s).matches()){
            return "Break Keyword";
        }else if(INTEGER.matcher(s).matches()){
            return "Integer Literal";
        }else if(FLOAT.matcher(s).matches()){
            return "Float Literal";
        }else if(STRING.matcher(s).matches()){
            return "String Literal";
        }else if(STRING_DELIMITER.matcher(s).matches()){
            return "String Delimiter";
        }else if(BOOL.matcher(s).matches()){
            return "Boolean Literal";
        }else if(VARIABLE.matcher(s).matches()){
            return "Variable Identifier";
        }else if(s.equals("\n")){
            return "Newline";
        }else if(s.equals(",")){
            return "Command Break";
        }
        
        return "No Match";
    }

    public String getMultiWordMatchingType(String s){
        if(IM_IN.matcher(s).matches()){
            return "Loop Start";
        }else if(IS_NOW.matcher(s).matches()){
            return "Soft Typecast";
        }else if(IM_OUT.matcher(s).matches()){
            return "Loop End";
        }else if(IF_ELSE_START.matcher(s).matches()){
            return "If-else Start";
        }else if(IF.matcher(s).matches()){
            return "If Keyword";
        }else if(ELSE.matcher(s).matches()){
            return "Else Keyword";
        }else if(COMPARISON.matcher(s).matches()){
            return "And";
        }else if(BOOLEAN_AND.matcher(s).matches()){
            return "Infinite And";
        }else if(BOOLEAN_OR.matcher(s).matches()){
            return "Infinite Or";
        }else if(BOOLEAN.matcher(s).matches()){
            return "Boolean Binary";
        }else if(ARITHMETIC.matcher(s).matches()){
            return "Arithmetic";
        }else if(DIVISION.matcher(s).matches()){
            return "Division";
        }else if(DECLARATION.matcher(s).matches()){
            return "Variable Declaration";
        }

        return "No Match";
    }

    private boolean isWhitespace(char c){
        return (c == ' ' || c == '\t' || c == '\n')? true : false;
    }

    private Stack<Token> KeyWordCleaner(Stack<Token> tokenStack){
        
        Stack<Token> newTokenStack = new Stack<Token>();
        String lexeme = "";
        String type = "";
        for(Token t : tokenStack){
            type = t.getType();
            if(type.equals("Incomplete Keyword")){
                lexeme += t.getContent() + " ";
                if(!(type = this.getMultiWordMatchingType(lexeme.substring(0, lexeme.length() - 1))).equals("No Match")){
                    newTokenStack.push(new Token(lexeme,type));
                    lexeme = "";
                }
            }else{
                newTokenStack.push(t);
            }
        }

        return newTokenStack;
    }

    private Stack<Token> StringCleaner(Stack<Token> tokenStack){

        int delimiter_counter = 0;
        Stack<Token> newTokenStack = new Stack<Token>();
        String lexeme = "";


        for(Token t : tokenStack){
            if(t.getType().equals("String Delimiter"))delimiter_counter += 1;
            if(delimiter_counter > 0){
                lexeme += t.getContent() + " ";
                if(delimiter_counter == 2){
                    newTokenStack.push(new Token(lexeme.substring(0, lexeme.length() - 1), "String Literal"));
                    delimiter_counter = 0;
                    lexeme = "";
                }
            }else{
                newTokenStack.push(t);
            }
        }

        return newTokenStack;
    }

    public void getAllMatches(String line) {
        Stack<String> stackOfLexemes = new Stack<String>();
        String lexeme = "";
        String type;
        Matcher m;
        // gets all the keywords

        if(line.equals(""))return;

        char[] character_array = line.toCharArray();
        int i = 0;
        char c = character_array[i];


        // System.out.println("STARTS");

        // System.out.println(character_array);
        for(; i < character_array.length; i++){ // fills up the lexeme stack with words
            c = character_array[i];
            if(isWhitespace(c) || i == (character_array.length - 1)){
                if(i == (character_array.length - 1)){
                    lexeme += c; // if eol is reached               
                }
                if(lexeme.equals(""))continue; // if lexeme is still empty, you will not push

                // preliminary type checking for stack errors
                type = getMatchingType(lexeme);

                if(type.equals("Source Code Delimiter"))isMiddle = !isMiddle; // having encountered a source code delimiter means the program has already started/ended
                if(lexeme.equals("KTHXBYE"))stackOfLexemes.push(lexeme);
                if(!isMiddle)break;

                // checks if is a comment
                if(type.equals("Comment Delimiter")){
                    isComment = !isComment;
                    break;
                }if(isComment)break;

                if(type.equals("Comment Unary")){ // if a comment starts
                    lexeme = "\n";
                    stackOfLexemes.push(lexeme);
                    lexeme ="";
                    break;
                }

                stackOfLexemes.push(lexeme);
                lexeme = "";

            }else{
                lexeme += c;
            }
        }

        // identifies the datatypes of the words and stores them to tokenStack
        lexeme = "";
        for(String currString : stackOfLexemes){
            type = getMatchingType(currString);

            this.tokenStack.push(new Token(currString, type));
        }

        // appends all incomplete keyword types
        this.tokenStack = KeyWordCleaner(this.tokenStack);

        // appends all incomplete string types
        this.tokenStack = StringCleaner(this.tokenStack);

    }

    public void showCode(JTextArea jarea){
        for(String line: this.stackOfLines){
            jarea.append(line);
        }
    }

    public void showStack(JTextArea jarea1, JTextArea jarea2){
        int counter = 0;
        for(Token t: this.tokenStack){
            t.show(++counter, jarea1, jarea2);
        }
    }

    public void showStack(){
        for (Token t : this.tokenStack) {
            t.show();
        }
    }

    public Stack<Token> getStack(){
        return this.tokenStack;
    }

}