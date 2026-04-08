package com.lolcode.tree;

/**
 * Created with IntelliJ IDEA.
 * User: miha
 * Date: 7/14/13
 * Time: 2:41 PM
 */

import com.lolcode.tree.exception.BaseAstException;

import java.util.ArrayList;

/**
 * Implements lolcode loop statement. <p><pre>{@code
 * IM IN YR LOOP1 UPPIN YR VAR1 TIL BOTH SAEM VAR1 AN 256
 *      VISIBLE "VAR1 IS NAO " VAR1
 *      GTFO
 * IM OUTTA YR POOP1
 * }</pre></p>
 */
public class TreeLoopStmt extends TreeStatement {
    private String label;
    private TreeVariable variable;
    public TreeVariable weakref;
    private TreeExpression exitCondition;
    private final ArrayList<TreeStatement> body;

    public static enum loopType {TIL, WHILE, EMPTY}

    public static enum opType {UPPIN, NERFIN, EMPTY}

    private loopType lType;
    private opType oType;

    public TreeLoopStmt() {
        label = "";
        variable = null;
        weakref = null;
        exitCondition = null;
        lType = loopType.EMPTY;
        oType = opType.EMPTY;
        body = new ArrayList<>();

    }

    public String getLabel() {
        return label;
    }

    public void setLabel(String label) {
        this.label = label;
    }

    public loopType getlType() {
        return lType;
    }

    public void setlType(loopType lType) {
        this.lType = lType;
    }

    public opType getoType() {
        return oType;
    }

    public void setoType(opType oType) {
        this.oType = oType;
    }

    public TreeVariable getVariable() {
        return variable;
    }

    public void setVariable(TreeVariable variable) {
        this.variable = variable;
    }

    public TreeExpression getExitCondition() {
        return exitCondition;
    }

    public void setExitCondition(TreeExpression exitCondition) {
        this.exitCondition = exitCondition;
    }

    public void addStatement(TreeStatement statement) {
        body.add(statement);
    }

    public ArrayList<TreeStatement> getBody() {
        return body;
    }

    @Override
    public <T> T accept(BaseASTVisitor<T> v) throws BaseAstException {
        return v.visit(this);
    }
}
