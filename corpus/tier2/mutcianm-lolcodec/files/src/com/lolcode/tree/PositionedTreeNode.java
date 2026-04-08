package com.lolcode.tree;

/**
 * Created with IntelliJ IDEA.
 * User: miha
 * Date: 7/22/13
 * Time: 5:30 PM
 */
public abstract class PositionedTreeNode implements TreeNode {
    protected position pos = null;

    @Override
    public position getPos() {
        return pos;
    }

    @Override
    public void setPos(position pos) {
        this.pos = pos;
    }
}
