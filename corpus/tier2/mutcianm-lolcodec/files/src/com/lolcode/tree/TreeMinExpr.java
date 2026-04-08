package com.lolcode.tree;

/**
 * Created with IntelliJ IDEA.
 * User: miha
 * Date: 7/15/13
 * Time: 5:00 PM
 */

import com.lolcode.tree.exception.BaseAstException;

/**
 * Handles lolcode MIN expression. <p><pre>{@code
 *  SMALLR OF VAR1 AN VAR2
 * }</pre></p>
 */
public class TreeMinExpr extends TreeBinaryExpr {
    @Override
    public <T> T accept(BaseASTVisitor<T> v) throws BaseAstException {
        return v.visit(this);
    }
}
