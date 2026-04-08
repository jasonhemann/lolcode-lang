package com.lolcode.tree;

/**
 * Created with IntelliJ IDEA.
 * User: miha
 * Date: 7/12/13
 * Time: 4:39 PM
 */

import com.lolcode.tree.exception.BaseAstException;

/**
 * Implements lolcode mutable values, such as local function and module variables, loop variables.
 */
public class TreeVariable extends TreeValue implements Comparable {
    private String name;

    public TreeVariable() {
        name = "";
    }

    public TreeVariable(TreeVariable other) {
        this.name = other.name;
        this.setType(other.getType());
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    @Override
    public <T> T accept(BaseASTVisitor<T> v) throws BaseAstException {
        return v.visit(this);
    }

    @Override
    public int compareTo(Object o) {
        TreeVariable tmp = (TreeVariable) o;
        return name.compareTo(tmp.getName());
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if ((o == null)) return false;

        TreeVariable variable = (TreeVariable) o;

        return !((name != null) ? !name.equals(variable.name) : (variable.name != null));

    }

    @Override
    public int hashCode() {
        return (name != null) ? name.hashCode() : 0;
    }
}
