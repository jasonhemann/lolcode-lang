package com.lolcode.tree;

/**
 * Created with IntelliJ IDEA.
 * User: miha
 * Date: 7/15/13
 * Time: 4:58 PM
 */

import com.lolcode.tree.exception.BaseAstException;

/**
 * Handles lolcode MAX expressions. <p><pre>{@code
 *  BIGGR OF VAR1 AN VAR2
 * }</pre></p>
 */
public class TreeMaxExpr extends TreeBinaryExpr {
    @Override
    public <T> T accept(BaseASTVisitor<T> v) throws BaseAstException {
        return v.visit(this);
    }
}
