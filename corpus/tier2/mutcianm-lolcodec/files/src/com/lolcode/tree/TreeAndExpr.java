package com.lolcode.tree;

/**
 * Created with IntelliJ IDEA.
 * User: miha
 * Date: 7/15/13
 * Time: 5:09 PM
 */

import com.lolcode.tree.exception.BaseAstException;

/**
 * Handles lolcode AND expression. <p><pre>{@code
 *  BOTH OF VAR1 AN VAR2
 * }</pre></p>
 */
public class TreeAndExpr extends TreeBinaryExpr {
    @Override
    public <T> T accept(BaseASTVisitor<T> v) throws BaseAstException {
        return v.visit(this);
    }
}
