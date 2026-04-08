package com.lolcode.tree;

/**
 * Created with IntelliJ IDEA.
 * User: miha
 * Date: 7/15/13
 * Time: 4:12 PM
 */

import com.lolcode.tree.exception.BaseAstException;

/**
 * Handles lolcode NOT expression. <p><pre>{@code
 * NOT BOTH SAEM VAR1 AN VAR2
 * }</pre></p>
 */
public class TreeNotExpr extends TreeExpression {
    private TreeExpression expr;

    public TreeNotExpr() {
        expr = null;
    }

    public TreeExpression getExpr() {
        return expr;
    }

    public void setExpr(TreeExpression expr) {
        this.expr = expr;
    }

    @Override
    public <T> T accept(BaseASTVisitor<T> v) throws BaseAstException {
        return v.visit(this);
    }
}
