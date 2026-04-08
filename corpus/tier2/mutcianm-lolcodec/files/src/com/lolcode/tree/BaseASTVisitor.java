package com.lolcode.tree;

/**
 * Created with IntelliJ IDEA.
 * User: miha
 * Date: 7/12/13
 * Time: 2:31 PM
 */

import com.lolcode.tree.exception.BaseAstException;

/**
 * Declares a base visitor with all kinds of visitable nodes. AST visitors must implement this interface.
 */
public interface BaseASTVisitor<T> {
    T visit(TreeFunction func) throws BaseAstException;

    T visit(TreeModule module) throws BaseAstException;

    T visit(TreeFunctionParameter param) throws BaseAstException;

    T visit(TreeIfStmt ifStmt) throws BaseAstException;

    T visit(TreeLoopStmt loopStmt) throws BaseAstException;

    T visit(TreeAssignStmt assignStmt) throws BaseAstException;

    T visit(TreeCaseStmt caseStmt) throws BaseAstException;

    T visit(TreeVarDeclStmt varDeclStmt) throws BaseAstException;

    T visit(TreeArrayDeclStmt arrayDeclStmt) throws BaseAstException;

    T visit(TreeVisibleStmt visibleStmt) throws BaseAstException;

    T visit(TreeGimmehStmt gimmehStmt) throws BaseAstException;

    T visit(TreeFuncCallExpr funcCallStmt) throws BaseAstException;

    T visit(TreeDummyStmt dummyStmt) throws BaseAstException;

    T visit(TreeBreakStmt breakStmt) throws BaseAstException;

    T visit(TreeReturnStmt returnStmt) throws BaseAstException;

    //Expressions:
    T visit(TreeVariable variable) throws BaseAstException;

    T visit(TreeConstant constant) throws BaseAstException;

    T visit(TreeSumExpr sumExpr) throws BaseAstException;

    T visit(TreeSubExpr subExpr) throws BaseAstException;

    T visit(TreeMulExpr mulExpr) throws BaseAstException;

    T visit(TreeDivExpr divExpr) throws BaseAstException;

    T visit(TreeModExpr modExpr) throws BaseAstException;

    T visit(TreeArrayPutStmt arrayPutExpr) throws BaseAstException;

    T visit(TreeArrayGetExpr arrayGetExpr) throws BaseAstException;

    //logic expressions
    T visit(TreeMaxExpr maxExpr) throws BaseAstException;

    T visit(TreeMinExpr minExpr) throws BaseAstException;

    T visit(TreeAndExpr andExpr) throws BaseAstException;

    T visit(TreeOrExpr orExpr) throws BaseAstException;

    T visit(TreeXorExpr xorExpr) throws BaseAstException;

    T visit(TreeNotExpr notExpr) throws BaseAstException;

    T visit(TreeEqualExpr equalExpr) throws BaseAstException;

    T visit(TreeNequalExpr nequalExpr) throws BaseAstException;
}
