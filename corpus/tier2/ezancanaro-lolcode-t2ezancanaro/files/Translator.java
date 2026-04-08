import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import org.antlr.v4.runtime.ANTLRInputStream;
import org.antlr.v4.runtime.CommonTokenStream;
import org.antlr.v4.runtime.tree.ParseTree;

/**
 *
 * @author Zanca
 */
public class Translator {

    
    
    /**
     * @param args the command line arguments
     *///"C:\\Users\\Zanca\\DocumentsTestTHIS.txt"
    public static void main(String[] args) throws FileNotFoundException, IOException {
        // TODO code application logic here
        String inputFile = "";
        
        if ( args.length>0 ) inputFile = args[0];
     
        InputStream is = System.in;
   
        if ( inputFile!=null ) {
            is = new FileInputStream(inputFile);
        }
        
        
        ANTLRInputStream input = new ANTLRInputStream(is);
        ThisShouldWorkLexer lexer = new ThisShouldWorkLexer(input);
        CommonTokenStream tokens = new CommonTokenStream(lexer);
        ThisShouldWorkParser parser = new ThisShouldWorkParser(tokens);
        parser.setBuildParseTree(true);      // tell ANTLR to build a parse tree
        ParseTree tree = parser.prog(); // parse
  
        TranslateVisitor evalVisitor = new TranslateVisitor();
        String result = evalVisitor.visit(tree);
       
    }
    
    
}