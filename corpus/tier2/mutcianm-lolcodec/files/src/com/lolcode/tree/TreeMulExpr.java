package com.lolcode.tree;

/**
 * Created with IntelliJ IDEA.
 * User: miha
 * Date: 7/15/13
 * Time: 4:16 PM
 */

import com.lolcode.tree.exception.BaseAstException;

/**
 * Handles lolcode multiplication expression. <p><pre>{@code
 *  PRODUCT OF VAR1 AN VAR2
 * }</pre></p>
 */
public class TreeMulExpr extends TreeBinaryExpr {

    @Override
    public <T> T accept(BaseASTVisitor<T> v) throws BaseAstException {
        return v.visit(this);
    }
}
