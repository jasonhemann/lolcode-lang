package com.lolcode.tree;

import com.lolcode.tree.exception.BaseAstException;

import java.util.ArrayList;

/**
 * Created with IntelliJ IDEA.
 * User: miha
 * Date: 7/11/13
 * Time: 9:45 PM
 */

/**
 * Handles lolcode functions. Stores zero or more arguments in TreeFunctionParameter array,
 * and zero or more statements as function body in TreeStatement array.
 */
public class TreeFunction extends PositionedTreeNode implements TreeTypedValue {
    private String name;
    private final ArrayList<TreeFunctionParameter> params;
    private final ArrayList<TreeStatement> body;
    private TYPE returnType;

    public TreeFunction() {
        name = "";
        returnType = TYPE.UNKNOWN;
        params = new ArrayList<>();
        body = new ArrayList<>();
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public void addParam(TreeFunctionParameter param) {
        this.params.add(param);
    }

    public void addStmt(TreeStatement stmt) {
        body.add(stmt);
    }

    public ArrayList<TreeFunctionParameter> getParams() {
        return params;
    }

    public ArrayList<TreeStatement> getBody() {
        return body;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if ((o == null) || (getClass() != o.getClass())) return false;

        TreeFunction that = (TreeFunction) o;

        return !((name != null) ? !name.equals(that.name) : (that.name != null));

    }

    @Override
    public int hashCode() {
        return (name != null) ? name.hashCode() : 0;
    }

    @Override
    public <T> T accept(BaseASTVisitor<T> v) throws BaseAstException {
        return v.visit(this);
    }

    @Override
    public void setType(TYPE type) {
        returnType = type;
    }

    @Override
    public TYPE getType() {
        return returnType;
    }
}
