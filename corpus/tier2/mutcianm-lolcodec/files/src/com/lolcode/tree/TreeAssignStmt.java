package com.lolcode.tree;

/**
 * Created with IntelliJ IDEA.
 * User: miha
 * Date: 7/12/13
 * Time: 3:50 PM
 */

import com.lolcode.tree.exception.BaseAstException;

/**
 * Stores assign statement. <p>For example:<pre> {@code VAR1 = VAR2 + 256}</pre> where VAR1 is lhs and VAR2 + 256 is rhs.
 * lhs must be of TreeValue type only, to avoid thing like `VAR1 + VAR2 = 256`, this should be checked in semantic check pass.</p>
 */
public class TreeAssignStmt extends TreeStatement {
    private TreeVariable lhs;
    private TreeExpression rhs;

    public TreeAssignStmt() {
        lhs = null;
        rhs = null;
    }

    public TreeVariable getLhs() {
        return lhs;
    }

    public TreeExpression getRhs() {
        return rhs;
    }

    public void setRhs(TreeExpression rhs) {
        this.rhs = rhs;
    }

    public void setLhs(TreeVariable lhs) {
        this.lhs = lhs;
    }

    @Override
    public <T> T accept(BaseASTVisitor<T> v) throws BaseAstException {
        return v.visit(this);
    }
}
