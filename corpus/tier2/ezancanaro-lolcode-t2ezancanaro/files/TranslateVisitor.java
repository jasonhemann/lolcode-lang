
import java.util.ArrayList;
import java.util.List;
import org.antlr.v4.runtime.misc.NotNull;
import org.antlr.v4.runtime.tree.ParseTree;
import org.antlr.v4.runtime.tree.TerminalNode;

/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

/**
 *
 * @author Zanca
 */
public class TranslateVisitor  extends ThisShouldWorkBaseVisitor<String> {
    
    public int nextTemp = 0; //Auxiliar para criação de vars induzidas no LoL
    public String tab = "    ";//Identação.
    public ThisShouldWorkParser.ExpContext helper;
    public int indent = 0;
    
    
    @Override public String visitExpression(@NotNull ThisShouldWorkParser.ExpressionContext ctx) { 
        ThisShouldWorkParser.ConditionalContext cond = ctx.conditional();
        if(cond != null){
            //System.out.println("COND");
            helper = ctx.exp();
            return visitConditional(cond);
        }
        return visitChildren(ctx); }
	
    
    @Override public String visitProg(ThisShouldWorkParser.ProgContext ctx) { 
        String startFile = "# Code start";
        System.out.print(startFile);
        
        int i;
        int size = ctx.children.size();
        int separatorSize = ctx.SEPARATOR().size ();
        String separate;
        // Cada expressao é acompanhada de 1 separador, logo pode pular o filho que é separador.
        for(i = 0; i < size; i+=2){
            visit(ctx.getChild(i));
            if(i/2 < separatorSize ){ 
                separate = (ctx.SEPARATOR().get(i/2).getText()); //Coloca os Separadores , ou \n 
                System.out.print(separate.replaceAll(",", ";"));
            }                                                            // 
        }
        String endFile = "# End Of File";
        System.out.println(endFile);
       // int value = visit(ctx.expr()); // compute value of expression on right
       // memory.put(id, value); // store it in our memory
       // return value;
        return "DONE"; }
    
    @Override public String visitInclude(ThisShouldWorkParser.IncludeContext ctx) { 
        
        String lib = visit(ctx.lib());
        if(lib != null){
            String importText = "import" + " " + lib ;
            System.out.print(importText);
        }
        return "S"; 
    }
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitLib(ThisShouldWorkParser.LibContext ctx) { 
            return ctx.ID().getText().toLowerCase(); }
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	
	@Override public String visitScan(ThisShouldWorkParser.ScanContext ctx) { 
            //a= raw_input()
            String var = visit(ctx.var());
            String scan = var + " = " + "raw_input()";
            System.out.print(scan);
            return visitChildren(ctx); }
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitPrint(ThisShouldWorkParser.PrintContext ctx) { 
           // 'VISIBLE' printArgs '!' ;
           String args = visit(ctx.printArgs());
           String printStr = "print (" + args + ")";
           System.out.print(printStr);
           return visitChildren(ctx); }
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitPrintArgs(ThisShouldWorkParser.PrintArgsContext ctx) { 
            String s = ctx.STRING().toString();
            String myArgs = "";
            
            List<ParseTree> a = ctx.children;
            List<TerminalNode> ds = ctx.STRING();
            int i=0; //Controla se já tem argumento prévio no print
            for(ParseTree t : ctx.children){
                if(i>0) //Se há mais de um argumento, uso o + pra concatenar
                    myArgs = myArgs + "+ ";
                
                myArgs = myArgs + t.getText() + " "; //Cria a String com os argumentos do print
                i++;//Indica que existe um argumento
            }  
            return myArgs; 
        }
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitArg(ThisShouldWorkParser.ArgContext ctx) { 
            return visitChildren(ctx); }
	
	
	@Override public String visitSum(ThisShouldWorkParser.SumContext ctx) { 
            //SUM OF args
            String exp = visit(ctx.args());
            //System.out.println("THIS " + exp);
            String pyExp = exp.replaceAll("AN", "+");
            System.out.print(pyExp);
            return visitChildren(ctx); 
        }
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitSub(ThisShouldWorkParser.SubContext ctx) { 
             String exp = visit(ctx.args());
            //System.out.println("THIS " + exp);
            String pyExp = exp.replaceAll("AN", "-");
            System.out.print(pyExp);
            return visitChildren(ctx); }
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitMult(ThisShouldWorkParser.MultContext ctx) { 
             String exp = visit(ctx.args());
            //System.out.println("THIS " + exp);
            String pyExp = exp.replaceAll("AN", "*");
            System.out.print(pyExp);
            return visitChildren(ctx); }
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitDiv(ThisShouldWorkParser.DivContext ctx) { 
             String exp = visit(ctx.args());
            //System.out.println("THIS " + exp);
            String pyExp = exp.replaceAll("AN", "/");
            System.out.print(pyExp);
            return visitChildren(ctx); }
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitModule(ThisShouldWorkParser.ModuleContext ctx) { 
             String exp = visit(ctx.args());
            //System.out.println("THIS " + exp);
            String pyExp = exp.replaceAll("AN", "%");
            System.out.print(pyExp);
            return visitChildren(ctx); }
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitMax(ThisShouldWorkParser.MaxContext ctx) { 
             String exp = visit(ctx.args());
            //System.out.println("THIS " + exp);
            String pyExp = "max(" + exp.replaceAll(" AN", ",") + ")";
            
            System.out.print(pyExp);
            return visitChildren(ctx); }
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitMin(ThisShouldWorkParser.MinContext ctx) { 
            
            String exp = visit(ctx.args());
            //System.out.println("THIS " + exp);
            String pyExp = "min(" + exp.replaceAll(" AN", ",") + ")";
            
            System.out.print(pyExp);
            
            return visitChildren(ctx); }
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitEquals(ThisShouldWorkParser.EqualsContext ctx) { 
            String exp = visit(ctx.args());
            
//System.out.println("THIS " + exp);
            String pyExp =  exp.replaceAll(" AN", " ==");
            System.out.print(pyExp);
            return visitChildren(ctx); }
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitDiffer(ThisShouldWorkParser.DifferContext ctx) { 
             String exp = visit(ctx.args());
            //System.out.println("THIS " + exp);
            String pyExp = exp.replaceAll(" AN", " !=");
            System.out.print(pyExp);
            return visitChildren(ctx); }
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitArgs(ThisShouldWorkParser.ArgsContext ctx) { 
            // argsLeft 'AN' argsRight;
            String left = visit(ctx.argsLeft());
            String right = visit(ctx.argsRight());
          
            String args = left + " AN " + right;
            
            return args;
        }
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitArgsLeft(ThisShouldWorkParser.ArgsLeftContext ctx) { 
            //argsLeft: arg | exp;
            String args = visit(ctx.arg());
          
            if(args == null)
              args = visit(ctx.exp()); 
            
            
            return args;
            
            //return "S";
        }
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitArgsRight(ThisShouldWorkParser.ArgsRightContext ctx) { 
            //arg | exp | argsLeft 'AN' argsRight;
            String args = visit(ctx.arg());
            if(args != null){
               
                return args;
            }
            args = visit(ctx.exp());
            if(args != null){
  
                return args;
                
            }
            args = visit(ctx.argsLeft()) + " AN " + visit(ctx.argsRight());
           
            return args;
   
        }
        @Override public String visitExp(ThisShouldWorkParser.ExpContext ctx) { 
            return visitChildren(ctx); }    
            
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitLoop(ThisShouldWorkParser.LoopContext ctx) { 
           /* 'IM IN YR' label SEPARATOR 
        (expression SEPARATOR)*
      'IM OUTTA YR' label;*/
            String loopStart = "while True:";
            System.out.print(loopStart);
            int expIterator,sepIterator = 0;
            int size = ctx.expression().size();
            String separate;
           
            separate = ctx.SEPARATOR().get(sepIterator).getText();
            System.out.print(separate.replaceAll(",", ";"));//O próprio while é seguido de um separador.
            sepIterator++;
            indent++;
            String indentat = "";
            for(int i=0; i< indent; i++)
                indentat = indentat + tab;
            
            //Cada expressao é acompanhada de 1 separador, exibe a expressão seguida do Separador.
            for(expIterator = 0; expIterator < size; expIterator++){
                System.out.print(indentat);//
                visit(ctx.expression(expIterator));
                separate = (ctx.SEPARATOR().get(sepIterator).getText()); //Coloca os Separadores , ou \n 
                System.out.print(separate.replaceAll(",", ";"));
            }
            indent--;
            System.out.print("#End Loop");  
        return "YES!"; }
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitConditional(ThisShouldWorkParser.ConditionalContext ctx) { 
            /*//  exp 
            'O RLY?' SEPARATOR //IF
                trueBranch
                falseBranch? 
            'OIC'*/
            String ifText = "if ";
            String elseText = "";
            String indentate = "";
            for(int i=0; i< indent; i++)
                elseText = elseText + tab;
            indentate = elseText + tab;
            
            System.out.print(ifText);
            visitExp(helper);
            System.out.print(" :");
            System.out.print("\n");
            indent++;
            
            
            if(ctx.breaks() != null){ //Como são todos membros opcionais, preciso dos ifs.
                
                System.out.print(indentate + visit(ctx.breaks()));
            }
            if(ctx.trueBranch() != null){
                
                visit(ctx.trueBranch());
                elseText = elseText + "else :";
            }
            
            System.out.print(elseText + "\n");
            if(ctx.falseBranch() != null)
                visit(ctx.falseBranch());
            indent--;
            return "S"; }
        
        @Override public String visitBreaks( ThisShouldWorkParser.BreaksContext ctx) {  
            return "break"; }
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitTrueBranch(ThisShouldWorkParser.TrueBranchContext ctx) { 
            int expIterator;
            int size = ctx.expression().size();
            String separate = "";
            String indentat = "";
            for(int i=0; i< indent; i++)
                indentat = indentat + tab;
            
            for(expIterator = 0; expIterator < size; expIterator++){
                System.out.print(indentat);//
                visit(ctx.expression(expIterator));
                separate = (ctx.SEPARATOR().get(expIterator).getText()); //Coloca os Separadores , ou \n 
                System.out.print(separate.replaceAll(",", ";"));
            }
            return "S"; }
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitFalseBranch(ThisShouldWorkParser.FalseBranchContext ctx) { 
            int expIterator;
            int size = ctx.expression().size();
            String separate = "";
            String indentat = "";
            for(int i=0; i< indent; i++)
                indentat = indentat + tab;
            
            for(expIterator = 0; expIterator < size; expIterator++){
                System.out.print(indentat);//
                visit(ctx.expression(expIterator));
                separate = (ctx.SEPARATOR().get(expIterator).getText()); //Coloca os Separadores , ou \n 
                System.out.print(separate.replaceAll(",", ";"));
            }
            return "S"; }
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitVariable_declaration(ThisShouldWorkParser.Variable_declarationContext ctx) { 
            /* 'I HAS A' var 
                     | 'I HAS A' var 'ITZ' val; */
            String dec = "" + ctx.var().getText() + " = ";
            dec = dec + ((ctx.ITZ() != null) ? ctx.val().getText() : "None");
            System.out.print(dec);
            return "S";}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitVar(ThisShouldWorkParser.VarContext ctx) { 
            return ctx.ID().getText(); }
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitLabel(ThisShouldWorkParser.LabelContext ctx) { 
            return ctx.ID().getText(); }
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitVal(ThisShouldWorkParser.ValContext ctx) { 
            String val = ctx.getChild(0).getText();
            return val; }
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitAssignment(ThisShouldWorkParser.AssignmentContext ctx) { 
            String dec = "";
            //var 'R' val;
            if(ctx.val()!=null){
                dec = ctx.var().getText() + " = " + ctx.val().getText();
                System.out.print(dec);
            }else{
                dec = ctx.var().getText() + " = "; 
                System.out.print(dec);
                visit(ctx.exp());
            }
            //var 'R' exp;
           
            return "S"; }
    
}
