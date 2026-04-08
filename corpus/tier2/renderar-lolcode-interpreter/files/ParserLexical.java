// LexicalAnalyzer.java
import java.util.*;
import java.io.*;
import java.util.regex.*;

public class ParserLexical {
    // Contants
    private static final Pattern KEYWORD = Pattern.compile("^(SMOOSH|MAEK|A|IS NOW A|IM IN YR|UPPIN|NERFIN|YR|TIL|WILE|IM OUTTA YR)");
    private static final Pattern CODE_START = Pattern.compile("^(HAI)");
    private static final Pattern CODE_END = Pattern.compile("^(KTHXBYE)");
    private static final Pattern COMMENT = Pattern.compile("^(BTW)");
    private static final Pattern COMMENT_SEPARATE = Pattern.compile("^(OBTW|TLDR)");
    private static final Pattern INPUT = Pattern.compile("^(GIMMEH)");
    private static final Pattern OUTPUT = Pattern.compile("^(VISIBLE)");
    private static final Pattern DECLARATION = Pattern.compile("^(I\\sHAS\\sA)");
    private static final Pattern EXPRESSION = Pattern.compile("^(IT)");
    private static final Pattern INITIALIZE = Pattern.compile("^(ITZ)");
    private static final Pattern ASSIGNMENT = Pattern.compile("^(R)");
    private static final Pattern ARITHMETIC = Pattern.compile("^(SUM\\sOF|DIFF\\sOF|PRODUKT\\sOF|QUOSHUNT\\sOF|MOD\\sOF|BIGGR\\sOF|SMALLR\\sOF)");
    private static final Pattern BOOLEAN = Pattern.compile("^(BOTH\\sOF|EITHER\\sOF|WON\\sOF)");
    private static final Pattern BOOLEAN_INFINITE = Pattern.compile("^(ANY\\sOF|ALL\\sOF)");
    private static final Pattern BOOLEAN_UNARY = Pattern.compile("^(NOT)");
    private static final Pattern COMPARISON = Pattern.compile("^(BOTH\\sSAEM|DIFFRINT)");
    private static final Pattern OPERATION_SEPARATOR = Pattern.compile("^(AN)");
    private static final Pattern CONCATENATE = Pattern.compile("^(SMOOSH)");
    private static final Pattern IFELSE_START = Pattern.compile("^(O\\sRLY?)");
    private static final Pattern SWITCH_START = Pattern.compile("^(WTF?)");
    private static final Pattern CONDITION_END = Pattern.compile("^(OIC)");
    private static final Pattern IF = Pattern.compile("^(YA\\sRLY)");
    private static final Pattern ELSEIF = Pattern.compile("^(MEBBE)");
    private static final Pattern ELSE = Pattern.compile("^(NO\\sWAI)");
    private static final Pattern CASE = Pattern.compile("^(OMG)");
    private static final Pattern DEFAULT = Pattern.compile("^(OMGWTF)");
    private static final Pattern BREAK = Pattern.compile("^(GTFO)");
    private static final Pattern INTEGER = Pattern.compile("^-?\\d+$");
    private static final Pattern FLOAT = Pattern.compile("^-?\\d*\\.\\d+$");
    private static final Pattern STRING = Pattern.compile("^\".*\"$");
    private static final Pattern BOOL = Pattern.compile("^(WIN|FAIL)$");
    private static final Pattern VARIABLE = Pattern.compile("^[a-z]+$");
    private static boolean commentbool = false;

    // Attributes
    private Stack<String> stackOfLines;
    private Stack<Token> tokenStack;

    // Constructor
    public ParserLexical(String path){
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
                    if(letter != '\n' && charRead == -1) toInsert = toInsert + letter;
                    this.stackOfLines.push(toInsert);
                    toInsert = "";
                }else{
                    toInsert = toInsert + letter;
                }
            }while(charRead != -1);
            input.close();
            /* end of Stack of Lines initializer */

            /* Match the Lexemes per line */

            for (String line : this.stackOfLines) {
                this.getAllMatches(line);
            }
            this.tokenStack.pop();
        } catch(Exception e) {
            System.out.println(e.getMessage());
        }
    }

    public void getAllMatches(String line) {
        String lexeme = "";
        Matcher m;
        Matcher whitespace;
        // gets all the keywords

        if (COMMENT_SEPARATE.matcher(line).matches()){
            commentbool = !commentbool;
        }

        for(int i = 0; i < line.length(); i++){            
            if(line.charAt(i) != ' ' && i != line.length()-1){
               lexeme = lexeme + line.charAt(i);
            }else{
                if(COMMENT_SEPARATE.matcher(lexeme).matches()){
                    commentbool = !commentbool;
                    lexeme = "";
                    break;
                }
                if(!commentbool){
                    if(CODE_START.matcher(lexeme).matches()){
                        this.tokenStack.push(new Token(lexeme, "Code Delimiter"));
                        lexeme = "";
                    }else if(CODE_END.matcher(lexeme).matches()){
                        this.tokenStack.push(new Token(lexeme, "Code Delimiter"));
                        lexeme = "";
                    }else if(COMMENT.matcher(lexeme).matches()){
                        lexeme = "";
                        break;
                    }else if(INPUT.matcher(lexeme).matches()){
                        this.tokenStack.push(new Token(lexeme, "Input Keyword"));
                        lexeme = "";
                    }else if(OUTPUT.matcher(lexeme).matches()){
                        this.tokenStack.push(new Token(lexeme, "Output Keyword"));
                        lexeme = "";
                    }else if(DECLARATION.matcher(lexeme).matches()){
                        this.tokenStack.push(new Token(lexeme, "Variable Declaration"));
                        lexeme = "";
                    }else if(EXPRESSION.matcher(lexeme).matches()){
                        this.tokenStack.push(new Token(lexeme, "Variable Expression"));
                        lexeme = "";
                    }else if(INITIALIZE.matcher(lexeme).matches()){
                        this.tokenStack.push(new Token(lexeme, "Variable Initialization"));
                        lexeme = "";
                    }else if(ASSIGNMENT.matcher(lexeme).matches()){
                        this.tokenStack.push(new Token(lexeme, "Variable Assignment"));
                        lexeme = "";
                    }else if(ARITHMETIC.matcher(lexeme).matches()){
                        this.tokenStack.push(new Token(lexeme, "Arithmetic Operation"));
                        lexeme = "";
                    }else if(BOOLEAN.matcher(lexeme).matches() || BOOLEAN_INFINITE.matcher(lexeme).matches() || BOOLEAN_UNARY.matcher(lexeme).matches()){
                        this.tokenStack.push(new Token(lexeme, "Boolean Operation"));
                        lexeme = "";
                    }else if(COMPARISON.matcher(lexeme).matches()){
                        this.tokenStack.push(new Token(lexeme, "Comparison Operation"));
                        lexeme = "";
                    }else if(OPERATION_SEPARATOR.matcher(lexeme).matches() || BOOLEAN_INFINITE.matcher(lexeme).matches() || BOOLEAN_UNARY.matcher(lexeme).matches()){
                        this.tokenStack.push(new Token(lexeme, "Operation Separator"));
                        lexeme = "";
                    }else if(CONCATENATE.matcher(lexeme).matches()){
                        this.tokenStack.push(new Token(lexeme, "String Concatenate"));
                        lexeme = "";
                    }else if(IFELSE_START.matcher(lexeme).matches() || SWITCH_START.matcher(lexeme).matches() || CONDITION_END.matcher(lexeme).matches()){
                        this.tokenStack.push(new Token(lexeme, "Flow-Control Statement Delimiter"));
                        lexeme = "";
                    }else if(IF.matcher(lexeme).matches()){
                        this.tokenStack.push(new Token(lexeme, "If Keyword"));
                        lexeme = "";
                    }else if(ELSEIF.matcher(lexeme).matches()){
                        this.tokenStack.push(new Token(lexeme, "If-else Keyword"));
                        lexeme = "";
                    }else if(ELSE.matcher(lexeme).matches()){
                        this.tokenStack.push(new Token(lexeme, "Else Keyword"));
                        lexeme = "";
                    }else if(CASE.matcher(lexeme).matches()){
                        this.tokenStack.push(new Token(lexeme, "Case Keyword"));
                        lexeme = "";
                    }else if(DEFAULT.matcher(lexeme).matches()){
                        this.tokenStack.push(new Token(lexeme, "Defaut Keyword"));
                        lexeme = "";
                    }else if(BREAK.matcher(lexeme).matches()){
                        this.tokenStack.push(new Token(lexeme, "Break Keyword"));
                        lexeme = "";
                    }else if(VARIABLE.matcher(lexeme).matches()){
                        this.tokenStack.push(new Token(lexeme, "Variable Identifier"));
                        lexeme = "";
                    }else if(INTEGER.matcher(lexeme).matches()){
                        this.tokenStack.push(new Token(lexeme, "Integer Literal"));
                        lexeme = "";
                    }else if(FLOAT.matcher(lexeme).matches()){
                        this.tokenStack.push(new Token(lexeme, "Float Literal"));
                        lexeme = "";
                    }else if(STRING.matcher(lexeme).matches()){
                        this.tokenStack.push(new Token(lexeme, "String Literal"));
                        lexeme = "";
                    }else if(BOOL.matcher(lexeme).matches()){
                        this.tokenStack.push(new Token(lexeme, "Boolean Literal"));
                        lexeme = "";
                    }else if(KEYWORD.matcher(lexeme).matches()){
                        this.tokenStack.push(new Token(lexeme, "Other Keywords"));
                        lexeme = "";
                    }
                }
                lexeme = lexeme + line.charAt(i);
            }
        }

        if (!COMMENT_SEPARATE.matcher(line).matches()){
            this.tokenStack.push(new Token("\\n", "Newline"));
            lexeme = "";
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