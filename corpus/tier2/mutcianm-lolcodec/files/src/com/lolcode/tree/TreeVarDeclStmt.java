package com.lolcode.tree;

/**
 * Created with IntelliJ IDEA.
 * User: miha
 * Date: 7/12/13
 * Time: 4:39 PM
 */

import com.lolcode.tree.exception.BaseAstException;

/**
 * Implements lolcode variable declaration and optional initialisation. Example: `I HAZ A VAR1 ITZ 256`
 */
public class TreeVarDeclStmt extends TreeStatement {
    private TreeVariable var;
    private TreeExpression initialValue;

    public TreeVarDeclStmt() {
        var = null;
        initialValue = null;
    }

    public TreeVariable getVar() {
        return var;
    }

    public void setVar(TreeVariable var) {
        this.var = var;
    }

    public TreeExpression getInitialValue() {
        return initialValue;
    }

    public void setInitialValue(TreeExpression initialValue) {
        this.initialValue = initialValue;
    }

    @Override
    public <T> T accept(BaseASTVisitor<T> v) throws BaseAstException {
        return v.visit(this);
    }
}
