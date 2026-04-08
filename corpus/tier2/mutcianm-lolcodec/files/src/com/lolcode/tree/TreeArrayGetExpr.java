package com.lolcode.tree;

import com.lolcode.tree.exception.BaseAstException;

public class TreeArrayGetExpr extends TreeExpression {

    private TreeVariable array = null;

    private TreeExpression key = null;

    public TreeVariable getArray() {
        return array;
    }

    public void setArray(TreeVariable array) {
        this.array = array;
    }

    public TreeExpression getKey() {
        return key;
    }

    public void setKey(TreeExpression key) {
        this.key = key;
    }

    @Override
    public <T> T accept(BaseASTVisitor<T> v) throws BaseAstException {
        return v.visit(this);
    }
}
