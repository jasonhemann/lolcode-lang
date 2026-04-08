package com.lolcode.tree;

/**
 * Base class for all binary expressions. Implements two TreeExpression for lhs and rhs
 * as well as getters and setters for them.
 */
public abstract class TreeBinaryExpr extends TreeExpression {
    private TreeExpression lhs;
    private TreeExpression rhs;

    public TreeBinaryExpr() {
        lhs = null;
        rhs = null;
    }

    public TreeExpression getLhs() {
        return lhs;
    }

    public void setLhs(TreeExpression lhs) {
        this.lhs = lhs;
    }

    public TreeExpression getRhs() {
        return rhs;
    }

    public void setRhs(TreeExpression rhs) {
        this.rhs = rhs;
    }
}