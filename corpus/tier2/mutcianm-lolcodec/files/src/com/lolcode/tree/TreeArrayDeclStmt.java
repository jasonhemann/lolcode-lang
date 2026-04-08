package com.lolcode.tree;

import com.lolcode.tree.exception.BaseAstException;

public class TreeArrayDeclStmt extends TreeStatement {
    private TreeVariable array;

    public TreeVariable getArray() {
        return array;
    }

    public void setArray(TreeVariable array) {
        this.array = array;
    }

    @Override
    public <T> T accept(BaseASTVisitor<T> v) throws BaseAstException {
        return v.visit(this);
    }
}
