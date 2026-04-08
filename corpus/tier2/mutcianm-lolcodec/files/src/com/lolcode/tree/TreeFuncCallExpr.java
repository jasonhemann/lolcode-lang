package com.lolcode.tree;

import com.lolcode.tree.exception.BaseAstException;

import java.util.ArrayList;

/**
 * Created with IntelliJ IDEA.
 * User: miha
 * Date: 7/14/13
 * Time: 2:53 PM
 */

/**
 * Implements lolcode function call statement. <p><pre>{@code
 *  I DUNNO HOW TO FUNCTION CALL
 * }</pre></p>
 */
public class TreeFuncCallExpr extends TreeExpression {
    private String funcName; //!< name of function to call
    private final ArrayList<TreeExpression> arguments;
    private TreeFunction boundFunction;

    public TreeFuncCallExpr() {
        funcName = "";
        arguments = new ArrayList<>();
        boundFunction = null;
    }

    public TreeFunction getBoundFunction() {
        return boundFunction;
    }

    public void setBoundFunction(TreeFunction boundFunction) {
        this.boundFunction = boundFunction;
    }

    public String getFuncName() {
        return funcName;
    }

    public void setFuncName(String funcName) {
        this.funcName = funcName;
    }

    public void addArgument(TreeExpression arg) {
        arguments.add(arg);
    }

    public ArrayList<TreeExpression> getArguments() {
        return arguments;
    }

    @Override
    public <T> T accept(BaseASTVisitor<T> v) throws BaseAstException {
        return v.visit(this);
    }
}
