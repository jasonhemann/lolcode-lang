package com.lolcode.tree;

/**
 * Created with IntelliJ IDEA.
 * User: miha
 * Date: 7/11/13
 * Time: 9:24 PM
 */

import com.lolcode.tree.exception.BaseAstException;

/**
 * Basic node type. Mainly used as a root of ASTBuilder resulting tree.
 */
public interface TreeNode {

    class position {
        public int line;
        public int symbol;

        public position(int line, int symbol) {
            this.line = line;
            this.symbol = symbol;
        }

        @Override
        public String toString() {
            return "[" + line + ":" + symbol + ']';
        }
    }

    position getPos();

    void setPos(position pos);

    <T> T accept(BaseASTVisitor<T> v) throws BaseAstException;
}
