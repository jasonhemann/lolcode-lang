// Generated from lolcode.g4 by ANTLR 4.7.2
import org.antlr.v4.runtime.tree.ParseTreeListener;

/**
 * This interface defines a complete listener for a parse tree produced by
 * {@link lolcodeParser}.
 */
public interface lolcodeListener extends ParseTreeListener {
	/**
	 * Enter a parse tree produced by {@link lolcodeParser#program}.
	 * @param ctx the parse tree
	 */
	void enterProgram(lolcodeParser.ProgramContext ctx);
	/**
	 * Exit a parse tree produced by {@link lolcodeParser#program}.
	 * @param ctx the parse tree
	 */
	void exitProgram(lolcodeParser.ProgramContext ctx);
	/**
	 * Enter a parse tree produced by {@link lolcodeParser#prog_type}.
	 * @param ctx the parse tree
	 */
	void enterProg_type(lolcodeParser.Prog_typeContext ctx);
	/**
	 * Exit a parse tree produced by {@link lolcodeParser#prog_type}.
	 * @param ctx the parse tree
	 */
	void exitProg_type(lolcodeParser.Prog_typeContext ctx);
	/**
	 * Enter a parse tree produced by {@link lolcodeParser#code_block}.
	 * @param ctx the parse tree
	 */
	void enterCode_block(lolcodeParser.Code_blockContext ctx);
	/**
	 * Exit a parse tree produced by {@link lolcodeParser#code_block}.
	 * @param ctx the parse tree
	 */
	void exitCode_block(lolcodeParser.Code_blockContext ctx);
	/**
	 * Enter a parse tree produced by {@link lolcodeParser#statement}.
	 * @param ctx the parse tree
	 */
	void enterStatement(lolcodeParser.StatementContext ctx);
	/**
	 * Exit a parse tree produced by {@link lolcodeParser#statement}.
	 * @param ctx the parse tree
	 */
	void exitStatement(lolcodeParser.StatementContext ctx);
	/**
	 * Enter a parse tree produced by {@link lolcodeParser#declaration}.
	 * @param ctx the parse tree
	 */
	void enterDeclaration(lolcodeParser.DeclarationContext ctx);
	/**
	 * Exit a parse tree produced by {@link lolcodeParser#declaration}.
	 * @param ctx the parse tree
	 */
	void exitDeclaration(lolcodeParser.DeclarationContext ctx);
	/**
	 * Enter a parse tree produced by {@link lolcodeParser#comment}.
	 * @param ctx the parse tree
	 */
	void enterComment(lolcodeParser.CommentContext ctx);
	/**
	 * Exit a parse tree produced by {@link lolcodeParser#comment}.
	 * @param ctx the parse tree
	 */
	void exitComment(lolcodeParser.CommentContext ctx);
	/**
	 * Enter a parse tree produced by {@link lolcodeParser#print_block}.
	 * @param ctx the parse tree
	 */
	void enterPrint_block(lolcodeParser.Print_blockContext ctx);
	/**
	 * Exit a parse tree produced by {@link lolcodeParser#print_block}.
	 * @param ctx the parse tree
	 */
	void exitPrint_block(lolcodeParser.Print_blockContext ctx);
	/**
	 * Enter a parse tree produced by {@link lolcodeParser#if_block}.
	 * @param ctx the parse tree
	 */
	void enterIf_block(lolcodeParser.If_blockContext ctx);
	/**
	 * Exit a parse tree produced by {@link lolcodeParser#if_block}.
	 * @param ctx the parse tree
	 */
	void exitIf_block(lolcodeParser.If_blockContext ctx);
	/**
	 * Enter a parse tree produced by {@link lolcodeParser#else_if_block}.
	 * @param ctx the parse tree
	 */
	void enterElse_if_block(lolcodeParser.Else_if_blockContext ctx);
	/**
	 * Exit a parse tree produced by {@link lolcodeParser#else_if_block}.
	 * @param ctx the parse tree
	 */
	void exitElse_if_block(lolcodeParser.Else_if_blockContext ctx);
	/**
	 * Enter a parse tree produced by {@link lolcodeParser#input_block}.
	 * @param ctx the parse tree
	 */
	void enterInput_block(lolcodeParser.Input_blockContext ctx);
	/**
	 * Exit a parse tree produced by {@link lolcodeParser#input_block}.
	 * @param ctx the parse tree
	 */
	void exitInput_block(lolcodeParser.Input_blockContext ctx);
	/**
	 * Enter a parse tree produced by {@link lolcodeParser#assignment}.
	 * @param ctx the parse tree
	 */
	void enterAssignment(lolcodeParser.AssignmentContext ctx);
	/**
	 * Exit a parse tree produced by {@link lolcodeParser#assignment}.
	 * @param ctx the parse tree
	 */
	void exitAssignment(lolcodeParser.AssignmentContext ctx);
	/**
	 * Enter a parse tree produced by {@link lolcodeParser#full_expression}.
	 * @param ctx the parse tree
	 */
	void enterFull_expression(lolcodeParser.Full_expressionContext ctx);
	/**
	 * Exit a parse tree produced by {@link lolcodeParser#full_expression}.
	 * @param ctx the parse tree
	 */
	void exitFull_expression(lolcodeParser.Full_expressionContext ctx);
	/**
	 * Enter a parse tree produced by {@link lolcodeParser#expression}.
	 * @param ctx the parse tree
	 */
	void enterExpression(lolcodeParser.ExpressionContext ctx);
	/**
	 * Exit a parse tree produced by {@link lolcodeParser#expression}.
	 * @param ctx the parse tree
	 */
	void exitExpression(lolcodeParser.ExpressionContext ctx);
	/**
	 * Enter a parse tree produced by {@link lolcodeParser#equals}.
	 * @param ctx the parse tree
	 */
	void enterEquals(lolcodeParser.EqualsContext ctx);
	/**
	 * Exit a parse tree produced by {@link lolcodeParser#equals}.
	 * @param ctx the parse tree
	 */
	void exitEquals(lolcodeParser.EqualsContext ctx);
	/**
	 * Enter a parse tree produced by {@link lolcodeParser#not_equals}.
	 * @param ctx the parse tree
	 */
	void enterNot_equals(lolcodeParser.Not_equalsContext ctx);
	/**
	 * Exit a parse tree produced by {@link lolcodeParser#not_equals}.
	 * @param ctx the parse tree
	 */
	void exitNot_equals(lolcodeParser.Not_equalsContext ctx);
	/**
	 * Enter a parse tree produced by {@link lolcodeParser#both}.
	 * @param ctx the parse tree
	 */
	void enterBoth(lolcodeParser.BothContext ctx);
	/**
	 * Exit a parse tree produced by {@link lolcodeParser#both}.
	 * @param ctx the parse tree
	 */
	void exitBoth(lolcodeParser.BothContext ctx);
	/**
	 * Enter a parse tree produced by {@link lolcodeParser#either}.
	 * @param ctx the parse tree
	 */
	void enterEither(lolcodeParser.EitherContext ctx);
	/**
	 * Exit a parse tree produced by {@link lolcodeParser#either}.
	 * @param ctx the parse tree
	 */
	void exitEither(lolcodeParser.EitherContext ctx);
	/**
	 * Enter a parse tree produced by {@link lolcodeParser#greater}.
	 * @param ctx the parse tree
	 */
	void enterGreater(lolcodeParser.GreaterContext ctx);
	/**
	 * Exit a parse tree produced by {@link lolcodeParser#greater}.
	 * @param ctx the parse tree
	 */
	void exitGreater(lolcodeParser.GreaterContext ctx);
	/**
	 * Enter a parse tree produced by {@link lolcodeParser#less}.
	 * @param ctx the parse tree
	 */
	void enterLess(lolcodeParser.LessContext ctx);
	/**
	 * Exit a parse tree produced by {@link lolcodeParser#less}.
	 * @param ctx the parse tree
	 */
	void exitLess(lolcodeParser.LessContext ctx);
	/**
	 * Enter a parse tree produced by {@link lolcodeParser#add}.
	 * @param ctx the parse tree
	 */
	void enterAdd(lolcodeParser.AddContext ctx);
	/**
	 * Exit a parse tree produced by {@link lolcodeParser#add}.
	 * @param ctx the parse tree
	 */
	void exitAdd(lolcodeParser.AddContext ctx);
	/**
	 * Enter a parse tree produced by {@link lolcodeParser#sub}.
	 * @param ctx the parse tree
	 */
	void enterSub(lolcodeParser.SubContext ctx);
	/**
	 * Exit a parse tree produced by {@link lolcodeParser#sub}.
	 * @param ctx the parse tree
	 */
	void exitSub(lolcodeParser.SubContext ctx);
	/**
	 * Enter a parse tree produced by {@link lolcodeParser#mul}.
	 * @param ctx the parse tree
	 */
	void enterMul(lolcodeParser.MulContext ctx);
	/**
	 * Exit a parse tree produced by {@link lolcodeParser#mul}.
	 * @param ctx the parse tree
	 */
	void exitMul(lolcodeParser.MulContext ctx);
	/**
	 * Enter a parse tree produced by {@link lolcodeParser#div}.
	 * @param ctx the parse tree
	 */
	void enterDiv(lolcodeParser.DivContext ctx);
	/**
	 * Exit a parse tree produced by {@link lolcodeParser#div}.
	 * @param ctx the parse tree
	 */
	void exitDiv(lolcodeParser.DivContext ctx);
	/**
	 * Enter a parse tree produced by {@link lolcodeParser#mod}.
	 * @param ctx the parse tree
	 */
	void enterMod(lolcodeParser.ModContext ctx);
	/**
	 * Exit a parse tree produced by {@link lolcodeParser#mod}.
	 * @param ctx the parse tree
	 */
	void exitMod(lolcodeParser.ModContext ctx);
	/**
	 * Enter a parse tree produced by {@link lolcodeParser#nope}.
	 * @param ctx the parse tree
	 */
	void enterNope(lolcodeParser.NopeContext ctx);
	/**
	 * Exit a parse tree produced by {@link lolcodeParser#nope}.
	 * @param ctx the parse tree
	 */
	void exitNope(lolcodeParser.NopeContext ctx);
	/**
	 * Enter a parse tree produced by {@link lolcodeParser#r_an}.
	 * @param ctx the parse tree
	 */
	void enterR_an(lolcodeParser.R_anContext ctx);
	/**
	 * Exit a parse tree produced by {@link lolcodeParser#r_an}.
	 * @param ctx the parse tree
	 */
	void exitR_an(lolcodeParser.R_anContext ctx);
}