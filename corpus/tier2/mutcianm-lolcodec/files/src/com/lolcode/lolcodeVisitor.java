// Generated from lolcode.g4 by ANTLR 4.1

package com.lolcode;

import org.antlr.v4.runtime.misc.NotNull;
import org.antlr.v4.runtime.tree.ParseTreeVisitor;

/**
 * This interface defines a complete generic visitor for a parse tree produced
 * by {@link lolcodeParser}.
 *
 * @param <T> The return type of the visit operation. Use {@link Void} for
 *            operations with no return type.
 */
public interface lolcodeVisitor<T> extends ParseTreeVisitor<T> {
    /**
     * Visit a parse tree produced by {@link lolcodeParser#formalParameter}.
     *
     * @param ctx the parse tree
     * @return the visitor result
     */
    T visitFormalParameter(@NotNull lolcodeParser.FormalParameterContext ctx);

    /**
     * Visit a parse tree produced by {@link lolcodeParser#caseblock}.
     *
     * @param ctx the parse tree
     * @return the visitor result
     */
    T visitCaseblock(@NotNull lolcodeParser.CaseblockContext ctx);

    /**
     * Visit a parse tree produced by {@link lolcodeParser#varDecl}.
     *
     * @param ctx the parse tree
     * @return the visitor result
     */
    T visitVarDecl(@NotNull lolcodeParser.VarDeclContext ctx);

    /**
     * Visit a parse tree produced by {@link lolcodeParser#block}.
     *
     * @param ctx the parse tree
     * @return the visitor result
     */
    T visitBlock(@NotNull lolcodeParser.BlockContext ctx);

    /**
     * Visit a parse tree produced by {@link lolcodeParser#gimstat}.
     *
     * @param ctx the parse tree
     * @return the visitor result
     */
    T visitGimstat(@NotNull lolcodeParser.GimstatContext ctx);

    /**
     * Visit a parse tree produced by {@link lolcodeParser#expr}.
     *
     * @param ctx the parse tree
     * @return the visitor result
     */
    T visitExpr(@NotNull lolcodeParser.ExprContext ctx);

    /**
     * Visit a parse tree produced by {@link lolcodeParser#dummystmt}.
     *
     * @param ctx the parse tree
     * @return the visitor result
     */
    T visitDummystmt(@NotNull lolcodeParser.DummystmtContext ctx);

    /**
     * Visit a parse tree produced by {@link lolcodeParser#assstat}.
     *
     * @param ctx the parse tree
     * @return the visitor result
     */
    T visitAssstat(@NotNull lolcodeParser.AssstatContext ctx);

    /**
     * Visit a parse tree produced by {@link lolcodeParser#visstat}.
     *
     * @param ctx the parse tree
     * @return the visitor result
     */
    T visitVisstat(@NotNull lolcodeParser.VisstatContext ctx);

    /**
     * Visit a parse tree produced by {@link lolcodeParser#notexpr}.
     *
     * @param ctx the parse tree
     * @return the visitor result
     */
    T visitNotexpr(@NotNull lolcodeParser.NotexprContext ctx);

    /**
     * Visit a parse tree produced by {@link lolcodeParser#arrayDecl}.
     *
     * @param ctx the parse tree
     * @return the visitor result
     */
    T visitArrayDecl(@NotNull lolcodeParser.ArrayDeclContext ctx);

    /**
     * Visit a parse tree produced by {@link lolcodeParser#nequexpr}.
     *
     * @param ctx the parse tree
     * @return the visitor result
     */
    T visitNequexpr(@NotNull lolcodeParser.NequexprContext ctx);

    /**
     * Visit a parse tree produced by {@link lolcodeParser#maxexpr}.
     *
     * @param ctx the parse tree
     * @return the visitor result
     */
    T visitMaxexpr(@NotNull lolcodeParser.MaxexprContext ctx);

    /**
     * Visit a parse tree produced by {@link lolcodeParser#casestat}.
     *
     * @param ctx the parse tree
     * @return the visitor result
     */
    T visitCasestat(@NotNull lolcodeParser.CasestatContext ctx);

    /**
     * Visit a parse tree produced by {@link lolcodeParser#file}.
     *
     * @param ctx the parse tree
     * @return the visitor result
     */
    T visitFile(@NotNull lolcodeParser.FileContext ctx);

    /**
     * Visit a parse tree produced by {@link lolcodeParser#value}.
     *
     * @param ctx the parse tree
     * @return the visitor result
     */
    T visitValue(@NotNull lolcodeParser.ValueContext ctx);

    /**
     * Visit a parse tree produced by {@link lolcodeParser#ifstat}.
     *
     * @param ctx the parse tree
     * @return the visitor result
     */
    T visitIfstat(@NotNull lolcodeParser.IfstatContext ctx);

    /**
     * Visit a parse tree produced by {@link lolcodeParser#exprList}.
     *
     * @param ctx the parse tree
     * @return the visitor result
     */
    T visitExprList(@NotNull lolcodeParser.ExprListContext ctx);

    /**
     * Visit a parse tree produced by {@link lolcodeParser#oneofexpr}.
     *
     * @param ctx the parse tree
     * @return the visitor result
     */
    T visitOneofexpr(@NotNull lolcodeParser.OneofexprContext ctx);

    /**
     * Visit a parse tree produced by {@link lolcodeParser#loopstat}.
     *
     * @param ctx the parse tree
     * @return the visitor result
     */
    T visitLoopstat(@NotNull lolcodeParser.LoopstatContext ctx);

    /**
     * Visit a parse tree produced by {@link lolcodeParser#funexpr}.
     *
     * @param ctx the parse tree
     * @return the visitor result
     */
    T visitFunexpr(@NotNull lolcodeParser.FunexprContext ctx);

    /**
     * Visit a parse tree produced by {@link lolcodeParser#modexpr}.
     *
     * @param ctx the parse tree
     * @return the visitor result
     */
    T visitModexpr(@NotNull lolcodeParser.ModexprContext ctx);

    /**
     * Visit a parse tree produced by {@link lolcodeParser#bothofexpr}.
     *
     * @param ctx the parse tree
     * @return the visitor result
     */
    T visitBothofexpr(@NotNull lolcodeParser.BothofexprContext ctx);

    /**
     * Visit a parse tree produced by {@link lolcodeParser#addexpr}.
     *
     * @param ctx the parse tree
     * @return the visitor result
     */
    T visitAddexpr(@NotNull lolcodeParser.AddexprContext ctx);

    /**
     * Visit a parse tree produced by {@link lolcodeParser#stat}.
     *
     * @param ctx the parse tree
     * @return the visitor result
     */
    T visitStat(@NotNull lolcodeParser.StatContext ctx);

    /**
     * Visit a parse tree produced by {@link lolcodeParser#functionDecl}.
     *
     * @param ctx the parse tree
     * @return the visitor result
     */
    T visitFunctionDecl(@NotNull lolcodeParser.FunctionDeclContext ctx);

    /**
     * Visit a parse tree produced by {@link lolcodeParser#main}.
     *
     * @param ctx the parse tree
     * @return the visitor result
     */
    T visitMain(@NotNull lolcodeParser.MainContext ctx);

    /**
     * Visit a parse tree produced by {@link lolcodeParser#divexpr}.
     *
     * @param ctx the parse tree
     * @return the visitor result
     */
    T visitDivexpr(@NotNull lolcodeParser.DivexprContext ctx);

    /**
     * Visit a parse tree produced by {@link lolcodeParser#minexpr}.
     *
     * @param ctx the parse tree
     * @return the visitor result
     */
    T visitMinexpr(@NotNull lolcodeParser.MinexprContext ctx);

    /**
     * Visit a parse tree produced by {@link lolcodeParser#retpart}.
     *
     * @param ctx the parse tree
     * @return the visitor result
     */
    T visitRetpart(@NotNull lolcodeParser.RetpartContext ctx);

    /**
     * Visit a parse tree produced by {@link lolcodeParser#formalParameters}.
     *
     * @param ctx the parse tree
     * @return the visitor result
     */
    T visitFormalParameters(@NotNull lolcodeParser.FormalParametersContext ctx);

    /**
     * Visit a parse tree produced by {@link lolcodeParser#subexpr}.
     *
     * @param ctx the parse tree
     * @return the visitor result
     */
    T visitSubexpr(@NotNull lolcodeParser.SubexprContext ctx);

    /**
     * Visit a parse tree produced by {@link lolcodeParser#eitherexpr}.
     *
     * @param ctx the parse tree
     * @return the visitor result
     */
    T visitEitherexpr(@NotNull lolcodeParser.EitherexprContext ctx);

    /**
     * Visit a parse tree produced by {@link lolcodeParser#arraygetexpr}.
     *
     * @param ctx the parse tree
     * @return the visitor result
     */
    T visitArraygetexpr(@NotNull lolcodeParser.ArraygetexprContext ctx);

    /**
     * Visit a parse tree produced by {@link lolcodeParser#equexpr}.
     *
     * @param ctx the parse tree
     * @return the visitor result
     */
    T visitEquexpr(@NotNull lolcodeParser.EquexprContext ctx);

    /**
     * Visit a parse tree produced by {@link lolcodeParser#multexpr}.
     *
     * @param ctx the parse tree
     * @return the visitor result
     */
    T visitMultexpr(@NotNull lolcodeParser.MultexprContext ctx);

    /**
     * Visit a parse tree produced by {@link lolcodeParser#arrayputstat}.
     *
     * @param ctx the parse tree
     * @return the visitor result
     */
    T visitArrayputstat(@NotNull lolcodeParser.ArrayputstatContext ctx);
}