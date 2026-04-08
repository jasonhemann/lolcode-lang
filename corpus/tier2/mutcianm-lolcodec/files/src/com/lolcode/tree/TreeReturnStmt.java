package com.lolcode.tree;

import com.lolcode.tree.exception.BaseAstException;

/**
 * Created with IntelliJ IDEA.
 * User: miha
 * Date: 7/20/13
 * Time: 9:53 PM
 */
public class TreeReturnStmt extends TreeStatement {
    private TreeExpression retValue;

    public TreeReturnStmt() {
        retValue = null;
    }

    public TreeExpression getRetValue() {
        return retValue;
    }

    public void setRetValue(TreeExpression retValue) {
        this.retValue = retValue;
    }

    @Override
    public <T> T accept(BaseASTVisitor<T> v) throws BaseAstException {
        return v.visit(this);
    }
}
