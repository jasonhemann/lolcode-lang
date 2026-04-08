package com.lolcode.tree;

/**
 * Created with IntelliJ IDEA.
 * User: miha
 * Date: 7/11/13
 * Time: 9:45 PM
 */

import com.lolcode.tree.exception.BaseAstException;

/**
 * Implements a value passed to function, it could either be of mutable or immutable type.
 */
public class TreeFunctionParameter extends TreeVariable {

    @Override
    public <T> T accept(BaseASTVisitor<T> v) throws BaseAstException {
        return v.visit(this);
    }
}
