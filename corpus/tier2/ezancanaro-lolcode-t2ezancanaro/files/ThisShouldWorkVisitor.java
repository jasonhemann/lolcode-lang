// Generated from C:\Users\Zanca\ThisShouldWork.g4 by ANTLR 4.1
   
import java.util.*;

import org.antlr.v4.runtime.misc.NotNull;
import org.antlr.v4.runtime.tree.ParseTreeVisitor;

/**
 * This interface defines a complete generic visitor for a parse tree produced
 * by {@link ThisShouldWorkParser}.
 *
 * @param <T> The return type of the visit operation. Use {@link Void} for
 * operations with no return type.
 */
public interface ThisShouldWorkVisitor<T> extends ParseTreeVisitor<T> {
	/**
	 * Visit a parse tree produced by {@link ThisShouldWorkParser#sub}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSub(@NotNull ThisShouldWorkParser.SubContext ctx);

	/**
	 * Visit a parse tree produced by {@link ThisShouldWorkParser#mult}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitMult(@NotNull ThisShouldWorkParser.MultContext ctx);

	/**
	 * Visit a parse tree produced by {@link ThisShouldWorkParser#trueBranch}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTrueBranch(@NotNull ThisShouldWorkParser.TrueBranchContext ctx);

	/**
	 * Visit a parse tree produced by {@link ThisShouldWorkParser#lib}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitLib(@NotNull ThisShouldWorkParser.LibContext ctx);

	/**
	 * Visit a parse tree produced by {@link ThisShouldWorkParser#conditional}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitConditional(@NotNull ThisShouldWorkParser.ConditionalContext ctx);

	/**
	 * Visit a parse tree produced by {@link ThisShouldWorkParser#falseBranch}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFalseBranch(@NotNull ThisShouldWorkParser.FalseBranchContext ctx);

	/**
	 * Visit a parse tree produced by {@link ThisShouldWorkParser#scan}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitScan(@NotNull ThisShouldWorkParser.ScanContext ctx);

	/**
	 * Visit a parse tree produced by {@link ThisShouldWorkParser#sum}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSum(@NotNull ThisShouldWorkParser.SumContext ctx);

	/**
	 * Visit a parse tree produced by {@link ThisShouldWorkParser#div}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitDiv(@NotNull ThisShouldWorkParser.DivContext ctx);

	/**
	 * Visit a parse tree produced by {@link ThisShouldWorkParser#argsLeft}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitArgsLeft(@NotNull ThisShouldWorkParser.ArgsLeftContext ctx);

	/**
	 * Visit a parse tree produced by {@link ThisShouldWorkParser#min}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitMin(@NotNull ThisShouldWorkParser.MinContext ctx);

	/**
	 * Visit a parse tree produced by {@link ThisShouldWorkParser#loop}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitLoop(@NotNull ThisShouldWorkParser.LoopContext ctx);

	/**
	 * Visit a parse tree produced by {@link ThisShouldWorkParser#arg}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitArg(@NotNull ThisShouldWorkParser.ArgContext ctx);

	/**
	 * Visit a parse tree produced by {@link ThisShouldWorkParser#exp}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitExp(@NotNull ThisShouldWorkParser.ExpContext ctx);

	/**
	 * Visit a parse tree produced by {@link ThisShouldWorkParser#val}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitVal(@NotNull ThisShouldWorkParser.ValContext ctx);

	/**
	 * Visit a parse tree produced by {@link ThisShouldWorkParser#include}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitInclude(@NotNull ThisShouldWorkParser.IncludeContext ctx);

	/**
	 * Visit a parse tree produced by {@link ThisShouldWorkParser#expression}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitExpression(@NotNull ThisShouldWorkParser.ExpressionContext ctx);

	/**
	 * Visit a parse tree produced by {@link ThisShouldWorkParser#variable_declaration}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitVariable_declaration(@NotNull ThisShouldWorkParser.Variable_declarationContext ctx);

	/**
	 * Visit a parse tree produced by {@link ThisShouldWorkParser#breaks}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitBreaks(@NotNull ThisShouldWorkParser.BreaksContext ctx);

	/**
	 * Visit a parse tree produced by {@link ThisShouldWorkParser#max}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitMax(@NotNull ThisShouldWorkParser.MaxContext ctx);

	/**
	 * Visit a parse tree produced by {@link ThisShouldWorkParser#var}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitVar(@NotNull ThisShouldWorkParser.VarContext ctx);

	/**
	 * Visit a parse tree produced by {@link ThisShouldWorkParser#assignment}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitAssignment(@NotNull ThisShouldWorkParser.AssignmentContext ctx);

	/**
	 * Visit a parse tree produced by {@link ThisShouldWorkParser#module}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitModule(@NotNull ThisShouldWorkParser.ModuleContext ctx);

	/**
	 * Visit a parse tree produced by {@link ThisShouldWorkParser#label}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitLabel(@NotNull ThisShouldWorkParser.LabelContext ctx);

	/**
	 * Visit a parse tree produced by {@link ThisShouldWorkParser#prog}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitProg(@NotNull ThisShouldWorkParser.ProgContext ctx);

	/**
	 * Visit a parse tree produced by {@link ThisShouldWorkParser#differ}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitDiffer(@NotNull ThisShouldWorkParser.DifferContext ctx);

	/**
	 * Visit a parse tree produced by {@link ThisShouldWorkParser#args}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitArgs(@NotNull ThisShouldWorkParser.ArgsContext ctx);

	/**
	 * Visit a parse tree produced by {@link ThisShouldWorkParser#printArgs}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitPrintArgs(@NotNull ThisShouldWorkParser.PrintArgsContext ctx);

	/**
	 * Visit a parse tree produced by {@link ThisShouldWorkParser#print}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitPrint(@NotNull ThisShouldWorkParser.PrintContext ctx);

	/**
	 * Visit a parse tree produced by {@link ThisShouldWorkParser#equals}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEquals(@NotNull ThisShouldWorkParser.EqualsContext ctx);

	/**
	 * Visit a parse tree produced by {@link ThisShouldWorkParser#argsRight}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitArgsRight(@NotNull ThisShouldWorkParser.ArgsRightContext ctx);
}