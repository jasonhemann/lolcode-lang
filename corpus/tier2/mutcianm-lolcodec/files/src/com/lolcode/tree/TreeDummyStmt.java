package com.lolcode.tree;

import com.lolcode.tree.exception.BaseAstException;

/**
 * Created with IntelliJ IDEA.
 * User: miha
 * Date: 7/24/13
 * Time: 1:59 PM
 */
public class TreeDummyStmt extends TreeStatement {
    TreeExpression body;

    public TreeDummyStmt() {
        body = null;
    }

    public TreeExpression getBody() {
        return body;
    }

    public void setBody(TreeExpression body) {
        this.body = body;
    }

    @Override
    public <T> T accept(BaseASTVisitor<T> v) throws BaseAstException {
        return v.visit(this);
    }
}
