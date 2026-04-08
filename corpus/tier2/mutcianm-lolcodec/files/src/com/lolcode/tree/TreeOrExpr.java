package com.lolcode.tree;

/**
 * Created with IntelliJ IDEA.
 * User: miha
 * Date: 7/15/13
 * Time: 5:11 PM
 */

import com.lolcode.tree.exception.BaseAstException;

/**
 * Handles lolcode OR expression. <p><pre>{@code
 *  WTF AM I SUPPOSED TO WRITE HERE
 * }</pre></p>
 */
public class TreeOrExpr extends TreeBinaryExpr {
    @Override
    public <T> T accept(BaseASTVisitor<T> v) throws BaseAstException {
        return v.visit(this);
    }
}
