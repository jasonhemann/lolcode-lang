import com.opencsv.CSVReader;
import com.opencsv.exceptions.CsvValidationException;
import org.antlr.v4.runtime.ANTLRInputStream;
import org.antlr.v4.runtime.CommonTokenStream;

import java.io.FileInputStream;
import java.io.FileReader;
import java.io.IOException;
import java.util.*;

public class lolcodeCustomListener extends lolcodeBaseListener {

    private Map<String, String> variables; //map in which we store our variables
    private Stack<String> stack1; // stack on which current value of expression is stored (we manipulate on it all the time)
    private String mode; // LOL, GOT, GEEK
    private final String info = "Geek info: ";
    private int loopState=0; //0 not if,else 1-yes but already satisfied 2-yes but still waiting
    private boolean isTrue = false;

    public lolcodeCustomListener() {
        variables = new HashMap<>();
        stack1 = new Stack<>();
    }

    @Override
    public void enterProgram(lolcodeParser.ProgramContext ctx) {
        // Printing entering message to program
        super.enterProgram(ctx);
        System.out.print("Welcome to LOLv2.0 programme! You can now laugh to your heart's content! ");
    }

    @Override
    public void exitProgram(lolcodeParser.ProgramContext ctx) {
        // Printing exiting message to program
        super.exitProgram(ctx);
        System.out.println("LOL has ended! Don't laugh it's not a joke! Bye!");
    }

    @Override
    public void enterProg_type(lolcodeParser.Prog_typeContext ctx) {
        // Nothing special, I needed that to get LOl, GOT, GEEK mode
        // TODO: Information for GEEK mode
        super.enterProg_type(ctx);
    }

    @Override
    public void exitProg_type(lolcodeParser.Prog_typeContext ctx) {
        // Setting up program mode and printing for everyone
        super.exitProg_type(ctx);
        mode = ctx.getText();
        System.out.println("MODE: "+mode);
    }

    @Override
    public void enterDeclaration(lolcodeParser.DeclarationContext ctx) {
        // Entering declaration and printing for GEEK mode
        super.enterDeclaration(ctx);
        if(mode.equals("GEEK")){System.out.println(info+"You're entering declaration!");}
    }

    @Override
    public void exitDeclaration(lolcodeParser.DeclarationContext ctx) {
        // We can declare empty label which is NOOB or label with values. Printing what's going on...
        // Storing values and variables (labels) names in map
        // TODO: Enhancements for GEEK mode

        super.exitDeclaration(ctx);
        if(loopState==1 || (loopState==2 && !isTrue)){}
        else{
            if(ctx.ATOM()==null){
                System.out.println("You've just declared empty variable!");
                variables.put(ctx.getChild(1).getText(), "NOOB");
            }
            else{
                variables.put(ctx.getChild(1).getText(), ctx.ATOM().getText());
                System.out.println("You've decalred: "+ctx.getChild(1).toString()+" with value: "+variables.get(ctx.getChild(1).toString()));
            }
            if(mode.equals("GEEK")){System.out.println(info+"You're exiting declaration!");}
        }
    }

    @Override
    public void enterInput_block(lolcodeParser.Input_blockContext ctx) {
        // Just enering input block, GEEK info
        super.enterInput_block(ctx);
        if(mode.equals("GEEK")){System.out.println(info+"You're entering input block!");}
    }

    @Override
    public void exitInput_block(lolcodeParser.Input_blockContext ctx) {
        // On exit input block, we get value from user and validate with regexp
        // We can either add new value to existing label or assign to empty (NOOB)
        // TODO: Move printing to GEEK mode accordingly as well as add some
        super.exitInput_block(ctx);
        if(loopState==1 || (loopState==2 && !isTrue)){}
        else{
            System.out.println(ctx.LABEL());
            String newlabel;
            Scanner sc = new Scanner(System.in);
            while(true){
                System.out.println("Gimme "+ctx.LABEL().getText()+" label value: ");
                newlabel = sc.nextLine();
                System.out.println("You gimmed: "+newlabel);
                if(newlabel.matches("WIN|FAIL|[0-9]*|[0-9]*\\.[0-9]*|[a-zA-Z]*|(^\\\"(\"|[^\"])*\"$)")){
                    if(variables.get(ctx.LABEL().getText())!=null){
                        variables.replace(ctx.LABEL().getText(), newlabel);
                    }
                    else{
                        variables.put(ctx.LABEL().getText(), newlabel);
                    }
                    break;
                }
                else {
                    System.out.println("Wait you cheater! Gimme ATOM!!!");
                }
            }

            if(variables.get(ctx.LABEL().getText())!=null){
                System.out.println("new label");
            }
            else{

            }
            if(mode.equals("GEEK")){System.out.println(info+"You're exiting input block!");}
        }

    }

    @Override
    public void enterPrint_block(lolcodeParser.Print_blockContext ctx) {
        // Enterig print block, GEEK mode may be updated
        super.enterPrint_block(ctx);
        if(mode.equals("GEEK")){System.out.println(info+"You're entering print block!");}
    }


    @Override
    public void exitPrint_block(lolcodeParser.Print_blockContext ctx) {
        // On exiting: we pop from stack, add to array and print values reversed
        // TODO: Update GEEK mode
        super.exitPrint_block(ctx);
        if(loopState==1 || (loopState==2 && !isTrue)){}
        else{
            if(isTrue){loopState=1;}
            ArrayList<String> elements = new ArrayList<>();
            for(int n=ctx.getChildCount()-2; n>0; n--) {
                elements.add(stack1.pop());
            }
            for(int j=elements.size()-1; j>=0; j--) {
                System.out.print(elements.get(j));
                System.out.print(" ");
            }
            System.out.print("\n");
            if(mode.equals("GEEK")){System.out.println(info+"You're exiting print block!");}
        }
    }

    @Override
    public void enterExpression(lolcodeParser.ExpressionContext ctx) {
        // On entering expression, Geek mode may needs updates
        super.enterExpression(ctx);
        if(mode.equals("GEEK")){System.out.println(info+"You're entering expression!");}
    }

    @Override
    public void exitExpression(lolcodeParser.ExpressionContext ctx) {
        // Super important! If expression call ends with ATOM we push on stack its value to pop it later on
        // If we have label at the end, then we search for its value in variables map and push to stack its value
        // TODO: As it is super important we need to cover that more in GEEK mode. Print as much info as we can.
        super.exitExpression(ctx);
        if(ctx.ATOM()!=null){
            //System.out.println(ctx.ATOM().getText());
            stack1.push(ctx.ATOM().getText());
        }
        else if(ctx.LABEL()!=null){
            stack1.push(variables.get(ctx.LABEL().getText()));
            //System.out.println(variables.get(ctx.LABEL().getText()));
        }
        if(mode.equals("GEEK")){System.out.println(info+"You're exiting expression!");}

    }

    @Override
    public void enterEquals(lolcodeParser.EqualsContext ctx) {
        // On entering equals, GEEK mode may needs updates
        super.enterEquals(ctx);
        if(mode.equals("GEEK")){System.out.println(info+"You're entering equals!");}
    }

    @Override
    public void exitEquals(lolcodeParser.EqualsContext ctx) {
        // Exiting equals, using equals in here
        // TODO: GEEK mode enhancements
        super.exitEquals(ctx);
        String two = stack1.pop();
        String one = stack1.pop();
        if(one.equals(two)){
            stack1.push("WIN");
        }
        else{
            stack1.push("FAIL");
        }
        if(loopState!=0){
            String score = stack1.pop();
            if(parseToDoubleEveything(score)==1.0){isTrue=true;}
            else{isTrue=false;}
        }
        if(mode.equals("GEEK")){System.out.println(info+"You're exiting equals!");}
    }

    @Override
    public void enterNot_equals(lolcodeParser.Not_equalsContext ctx) {
        // Not much difference with equals see above
        super.enterNot_equals(ctx);
        if(mode.equals("GEEK")){System.out.println(info+"You're entering not equals!");}
    }

    @Override
    public void exitNot_equals(lolcodeParser.Not_equalsContext ctx) {
        // Not much difference with equals see above
        super.exitNot_equals(ctx);
        String two = stack1.pop();
        String one = stack1.pop();
        if(!one.equals(two)){
            stack1.push("WIN");
        }
        else{
            stack1.push("FAIL");
        }
        if(loopState!=0){
            String score = stack1.pop();
            if(parseToDoubleEveything(score)==1.0){isTrue=true;}
            else{isTrue=false;}
        }
        if(mode.equals("GEEK")){System.out.println(info+"You're exiting not equals!");}
    }

    @Override
    public void enterBoth(lolcodeParser.BothContext ctx) {
        // Entering both, GEEK mode needs more
        super.enterBoth(ctx);
        if(mode.equals("GEEK")){System.out.println(info+"You're entering both!");}
    }

    @Override
    public void exitBoth(lolcodeParser.BothContext ctx) {
        // When on of them NOOB then NOOB
        // Both cannot be FAIL, 0, 0.0
        // TODO: Check if it makes sense, must be consistent with other expressions, GEEK mode needs updating
        super.exitBoth(ctx);
        String two = stack1.pop();
        String one = stack1.pop();
        if(one.equals("NOOB") || two.equals("NOOB")){
            stack1.push("NOOB");

        }
        else if(one.equals("FAIL") || one.equals("0") || one.equals("0.0") || two.equals("FAIL") || two.equals("0") || two.equals("0.0")){
            stack1.push("FAIL");
        }
        else{
            stack1.push("WIN");
        }
        if(loopState!=0){
            String score = stack1.pop();
            if(parseToDoubleEveything(score)==1.0){isTrue=true;}
            else{isTrue=false;}
        }
        if(mode.equals("GEEK")){System.out.println(info+"You're exiting both!");}
    }

    @Override
    public void enterEither(lolcodeParser.EitherContext ctx) {
        // Entering either, GEEK mode check
        super.enterEither(ctx);
        if(mode.equals("GEEK")){System.out.println(info+"You're entering either!");}
    }

    @Override
    public void exitEither(lolcodeParser.EitherContext ctx) {
        // When on of them NOOB then NOOB
        // Both cannot be FAIL, 0, 0.0
        // TODO: Check if it makes sense, must be consistent with other expressions, GEEK mode needs updating
        super.exitEither(ctx);
        String two = stack1.pop();
        String one = stack1.pop();
        if(one.equals("NOOB") || two.equals("NOOB")){
            stack1.push("NOOB");
        }
        else if((one.equals("FAIL") || one.equals("0") || one.equals("0.0") )&& !two.equals("FAIL") && !two.equals("0") && !two.equals("0.0")){
            stack1.push("WIN");
        }
        else if((two.equals("FAIL") || two.equals("0") || two.equals("0.0") )&& !one.equals("FAIL") && !one.equals("0") && !one.equals("0.0")){
            stack1.push("WIN");
        }
        else{
            stack1.push("FAIL");
        }
        if(mode.equals("GEEK")){System.out.println(info+"You're exiting either!");}

    }

    @Override
    public void enterGreater(lolcodeParser.GreaterContext ctx) {
        super.enterGreater(ctx);
        if(mode.equals("GEEK")){System.out.println(info+"You're entering greater!");}
    }

    @Override
    public void exitGreater(lolcodeParser.GreaterContext ctx) {
        super.exitGreater(ctx);
        String two = stack1.pop();
        String one = stack1.pop();
        if(one.equals("NOOB") || two.equals("NOOB")){
            stack1.push("NOOB");
            return;
        }
        double d1 = parseToDoubleEveything(one);
        double d2 = parseToDoubleEveything(two);

        if(d1>d2){stack1.push(Double.toString(d1));}
        else{stack1.push(Double.toString(d2));}
        if(mode.equals("GEEK")){System.out.println(info+"You're exiting greater!");}
    }

    @Override
    public void enterLess(lolcodeParser.LessContext ctx) {
        super.enterLess(ctx);
        if(mode.equals("GEEK")){System.out.println(info+"You're entering less!");}
    }

    @Override
    public void exitLess(lolcodeParser.LessContext ctx) {
        super.exitLess(ctx);
        String two = stack1.pop();
        String one = stack1.pop();
        if(one.equals("NOOB") || two.equals("NOOB")){
            stack1.push("NOOB");
            return;
        }
        double d1 = parseToDoubleEveything(one);
        double d2 = parseToDoubleEveything(two);

        if(d1<d2){stack1.push(Double.toString(d1));}
        else{stack1.push(Double.toString(d2));}
        if(mode.equals("GEEK")){System.out.println(info+"You're exiting less!");}
    }

    @Override
    public void enterAdd(lolcodeParser.AddContext ctx) {
        super.enterAdd(ctx);
        if(mode.equals("GEEK")){System.out.println(info+"You're entering add!");}
    }

    @Override
    public void exitAdd(lolcodeParser.AddContext ctx) {
        super.exitAdd(ctx);
        String two = stack1.pop();
        String one = stack1.pop();
        if(one.equals("NOOB") || two.equals("NOOB")){
            stack1.push("NOOB");
            return;
        }
        double d1 = parseToDoubleEveything(one);
        double d2 = parseToDoubleEveything(two);

        stack1.push(Double.toString(d1+d2));
        if(mode.equals("GEEK")){System.out.println(info+"You're exiting add!");}
    }

    @Override
    public void enterSub(lolcodeParser.SubContext ctx) {
        super.enterSub(ctx);
        if(mode.equals("GEEK")){System.out.println(info+"You're entering sub!");}
    }

    @Override
    public void exitSub(lolcodeParser.SubContext ctx) {
        super.exitSub(ctx);
        String two = stack1.pop();
        String one = stack1.pop();
        if(one.equals("NOOB") || two.equals("NOOB")){
            stack1.push("NOOB");
            return;
        }
        double d1 = parseToDoubleEveything(one);
        double d2 = parseToDoubleEveything(two);

        stack1.push(Double.toString(d1-d2));
        if(mode.equals("GEEK")){System.out.println(info+"You're exiting sub!");}
    }

    @Override
    public void enterMul(lolcodeParser.MulContext ctx) {
        super.enterMul(ctx);
        if(mode.equals("GEEK")){System.out.println(info+"You're entering mul!");}
    }

    @Override
    public void exitMul(lolcodeParser.MulContext ctx) {
        super.exitMul(ctx);
        String two = stack1.pop();
        String one = stack1.pop();
        if(one.equals("NOOB") || two.equals("NOOB")){
            stack1.push("NOOB");
            return;
        }
        double d1 = parseToDoubleEveything(one);
        double d2 = parseToDoubleEveything(two);

        stack1.push(Double.toString(d1*d2));
        if(mode.equals("GEEK")){System.out.println(info+"You're exiting mul!");}
    }

    @Override
    public void enterDiv(lolcodeParser.DivContext ctx) {
        super.enterDiv(ctx);
        if(mode.equals("GEEK")){System.out.println(info+"You're entering div!");}
    }

    @Override
    public void exitDiv(lolcodeParser.DivContext ctx) {
        super.exitDiv(ctx);
        String two = stack1.pop();
        String one = stack1.pop();
        if(one.equals("NOOB") || two.equals("NOOB")){
            stack1.push("NOOB");
            return;
        }
        double d1 = parseToDoubleEveything(one);
        double d2 = parseToDoubleEveything(two);

        if(d2==0.0){stack1.push("NOOB");}
        else{stack1.push(Double.toString(d1/d2));}
        if(mode.equals("GEEK")){System.out.println(info+"You're exiting div!");}
    }

    @Override
    public void enterNope(lolcodeParser.NopeContext ctx) {
        super.enterNope(ctx);
        if(mode.equals("GEEK")){System.out.println(info+"You're entering nope!");}
    }

    @Override
    public void exitNope(lolcodeParser.NopeContext ctx) {
        super.exitNope(ctx);
        String one = stack1.pop();
        if(one.equals("NOOB")){
            stack1.push("NOOB");
        }
        else if (one.equals("WIN")){stack1.push("FAIL");}
        else if (one.equals("FAIL")){stack1.push("WIN");}
        else if(one.matches("^([0-9]*)$")){stack1.push("-"+one);}
        else if(one.matches("^([0-9]*\\.([0-9])*)$")){stack1.push("-"+one);}
        else{stack1.push(new StringBuilder(one).reverse().toString());}
        if(mode.equals("GEEK")){System.out.println(info+"You're exiting nope!");}
    }

    private double parseToDoubleEveything(String one){
        double d1;
        if(one.equals("WIN")){d1=1.0;}
        else if(one.equals("FAIL")){d1=0.0;}
        else if(one.matches("^([0-9]*|([0-9]*\\.([0-9])*))$")){d1=Double.parseDouble(one);}
        else{d1=(double)one.length()-2;}
        return d1;
    }

    @Override
    public void enterMod(lolcodeParser.ModContext ctx) {
        super.enterMod(ctx);
        if(mode.equals("GEEK")){System.out.println(info+"You're entering mod!");}
    }

    @Override
    public void exitMod(lolcodeParser.ModContext ctx) {
        super.exitMod(ctx);
        String two = stack1.pop();
        String one = stack1.pop();
        if(one.equals("NOOB") || two.equals("NOOB")){
            stack1.push("NOOB");
            return;
        }
        double d1 = parseToDoubleEveything(one);
        double d2 = parseToDoubleEveything(two);

        int i1 = (int) d1;
        int i2 = (int) d2;
        if(d2==0){stack1.push("NOOB");}
        else{stack1.push(Double.toString(d1%d2));}
        if(mode.equals("GEEK")){System.out.println(info+"You're exiting mod!");}
    }

    @Override
    public void enterAssignment(lolcodeParser.AssignmentContext ctx) {
        super.enterAssignment(ctx);
        if(mode.equals("GEEK")){System.out.println(info+"You're entering assignment!");}
    }

    @Override
    public void exitAssignment(lolcodeParser.AssignmentContext ctx) {
        super.exitAssignment(ctx);
        if(loopState==1 || (loopState==2 && !isTrue)){}
        else {
            if (variables.get(ctx.getChild(0).getText()) != null) {
                variables.replace(ctx.getChild(0).getText(), stack1.pop());
            } else {
                System.out.println("No such LABEL you liar! Declare first!");
            }
            if (mode.equals("GEEK")) {
                System.out.println(info + "You're exiting assignment!");
            }
        }
    }

    @Override
    public void enterStatement(lolcodeParser.StatementContext ctx) {
        super.enterStatement(ctx);
        if(mode.equals("LOL")){System.out.println("JOKE TIME: "+tellMeAJoke());}
        if(mode.equals("GEEK")){System.out.println(info+"You're entering statement!");}
    }

    private String tellMeAJoke(){
        Random rand = new Random();
        int n = rand.nextInt(1622)+1;

            String csvFile = "res/cleanjokes.csv";

            CSVReader reader = null;
            try {
                reader = new CSVReader(new FileReader(csvFile));
                String[] line;
                while ((line = reader.readNext()) != null) {
                    if(line[0].equals(Integer.toString(n))){return line[1];}
                }
            } catch (IOException | CsvValidationException e) {
                e.printStackTrace();
            }
            return "No joke today";
    }

    @Override
    public void exitStatement(lolcodeParser.StatementContext ctx) {
        super.exitStatement(ctx);
        if(mode.equals("GEEK")){System.out.println(info+"You're exiting statement!");}
    }

    @Override
    public void enterComment(lolcodeParser.CommentContext ctx) {
        super.enterComment(ctx);
        if(mode.equals("GEEK")){System.out.println(info+"You're entering comment!");}
        System.out.println("ICYMI: there is comment! IDC but IMO you should read it. ");
    }

    @Override
    public void exitComment(lolcodeParser.CommentContext ctx) {
        super.exitComment(ctx);
        if(mode.equals("GEEK")){System.out.println(info+"You're exiting comment!");}
    }

    @Override
    public void enterIf_block(lolcodeParser.If_blockContext ctx) {
        super.enterIf_block(ctx);
        loopState = 2;
        if(mode.equals("GEEK")){System.out.println(info+"You're entering if block!");}
    }

    @Override
    public void exitIf_block(lolcodeParser.If_blockContext ctx) {
        super.exitIf_block(ctx);
        loopState = 0;
        if(mode.equals("GEEK")){System.out.println(info+"You're exiting if block!");}
    }

    @Override
    public void enterElse_if_block(lolcodeParser.Else_if_blockContext ctx) {
        super.enterElse_if_block(ctx);
        if(ctx.getStart().getText().equals("NO WAI")){isTrue=true;}
        if(mode.equals("GEEK")){System.out.println(info+"You're exiting else if block!");}
    }

    @Override
    public void exitElse_if_block(lolcodeParser.Else_if_blockContext ctx) {
        super.exitElse_if_block(ctx);
        if(mode.equals("GEEK")){System.out.println(info+"You're exiting else if block!");}
    }


    public static void main(String[] args) {
        // Take program argument as lol file to parse
        try {
            ANTLRInputStream input = new ANTLRInputStream(
                    new FileInputStream(args[0]));

            lolcodeLexer lexer = new lolcodeLexer(input);
            lolcodeParser parser = new lolcodeParser(new CommonTokenStream(lexer));
            parser.addParseListener(new lolcodeCustomListener());

            // Start parsing
            parser.program();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
