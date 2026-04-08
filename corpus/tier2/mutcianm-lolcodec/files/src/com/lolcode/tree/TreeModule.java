package com.lolcode.tree;

import com.lolcode.tree.exception.BaseAstException;

import java.util.ArrayList;

/**
 * Created with IntelliJ IDEA.
 * User: miha
 * Date: 7/12/13
 * Time: 2:09 PM
 */

/**
 * Represents lolcode primary compilation unit in ast. Consists of 0 or more function declarations
 * and 0 or more body statements, which act as main() in c.
 */
public class TreeModule extends PositionedTreeNode {

    private String moduleName;
    private final ArrayList<TreeFunction> functions;
    private final ArrayList<TreeStatement> body;

    public TreeModule() {
        moduleName = "";
        functions = new ArrayList<>();
        body = new ArrayList<>();
    }

    public String getModuleName() {
        return moduleName;
    }

    public void setModuleName(String moduleName) {
        this.moduleName = moduleName;
    }

    public void addFunction(TreeFunction function) {
        functions.add(function);
    }

    public void addStatement(TreeStatement statement) {
        body.add(statement);
    }

    public ArrayList<TreeFunction> getFunctions() {
        return functions;
    }

    public ArrayList<TreeStatement> getBody() {
        return body;
    }

    @Override
    public <T> T accept(BaseASTVisitor<T> v) throws BaseAstException {
        return v.visit(this);
    }
}
