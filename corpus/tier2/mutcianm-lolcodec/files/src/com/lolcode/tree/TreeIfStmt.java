package com.lolcode.tree;

import com.lolcode.tree.exception.BaseAstException;
import org.objectweb.asm.Label;

import java.util.ArrayList;

/**
 * Created with IntelliJ IDEA.
 * User: miha
 * Date: 7/12/13
 * Time: 2:47 PM
 */

/**
 * Handles lolcode if statement
 */
public class TreeIfStmt extends TreeStatement {
    private TreeExpression condition;
    private final ArrayList<TreeIfStmt> elseIfs;
    private final ArrayList<TreeStatement> trueBranch;
    private final ArrayList<TreeStatement> falseBranch;
    public Label endLabel;


    public TreeIfStmt() {
        condition = null;
        elseIfs = new ArrayList<>();
        trueBranch = new ArrayList<>();
        falseBranch = new ArrayList<>();
    }

    public ArrayList<TreeIfStmt> getElseIf() {
        return elseIfs;
    }

    public void addElseIf(TreeIfStmt elseIf) {
        this.elseIfs.add(elseIf);
    }

    public void setCondition(TreeExpression condition) {
        this.condition = condition;
    }

    public TreeExpression getCondition() {
        return condition;
    }

    public void addTrueStmt(TreeStatement statement) {
        trueBranch.add(statement);
    }

    public void addFalseStmt(TreeStatement statement) {
        falseBranch.add(statement);
    }

    public ArrayList<TreeStatement> getTrueBranch() {
        return trueBranch;
    }

    public ArrayList<TreeStatement> getFalseBranch() {
        return falseBranch;
    }

    public ArrayList<TreeIfStmt> getElseIfs() {
        return elseIfs;
    }

    @Override
    public <T> T accept(BaseASTVisitor<T> v) throws BaseAstException {
        return v.visit(this);
    }
}
