package com.lolcode.tree;

/**
 * Created with IntelliJ IDEA.
 * User: miha
 * Date: 7/12/13
 * Time: 4:36 PM
 */

import com.lolcode.tree.exception.BaseAstException;

/**
 * Handles subtraction expressions. </br>{@code DIFF OF VAR1 an VAR2}</br>
 * Consists of two TreeExpression for lhs and rhs respectively.
 */
public class TreeSubExpr extends TreeBinaryExpr {

    @Override
    public <T> T accept(BaseASTVisitor<T> v) throws BaseAstException {
        return v.visit(this);
    }
}
