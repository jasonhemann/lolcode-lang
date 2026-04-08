package com.lolcode.tree;

import com.lolcode.tree.exception.BaseAstException;

import java.util.*;

/**
 * Created with IntelliJ IDEA.q
 * User: miha
 * Date: 7/14/13
 * Time: 2:00 PM
 */

/**
 * Implements lolcode switch statement. <p>
 * Implemented with a Map : Constant(label) -> array of TreeStatement
 * <pre>{@code
 *  VAR1 WTF?
 *      OMG 256
 *          VISIBLE "256"
 *          GTFO
 *      OMGWTF
 *          VISIBLE "NOT 256 LOL"
 *   OIC}</pre></p>
 */
public class TreeCaseStmt extends TreeStatement {
    private TreeExpression val;
    private final LinkedHashMap<TreeConstant, List<TreeStatement>> body;
    private final List<TreeStatement> defaultBranch;

    public TreeCaseStmt() {
        val = null;
        body = new LinkedHashMap<>();
        defaultBranch = new ArrayList<>();
    }

    public TreeExpression getVal() {
        return val;
    }

    public void setVal(TreeExpression val) {
        this.val = val;
    }

    public void addStatement(TreeConstant label, TreeStatement statement) {
        //might as well check if value is set prior to adding statements
        List<TreeStatement> statements = body.get(label);
        if (statements != null) {
            statements.add(statement);
        } else {
            statements = new ArrayList<>();
            statements.add(statement);
            body.put(label, statements);
        }
    }

    public void addDefaultStmt(TreeStatement statement) {
        defaultBranch.add(statement);
    }

    public boolean addStatement(TreeConstant label, List<TreeStatement> stmts) {
        return body.put(label, stmts) == null;          // returns true if there was no value for label
    }

    public Map<TreeConstant, List<TreeStatement>> getBody() {
        return body;
    }

    public List<TreeStatement> getDefaultBranch() {
        return defaultBranch;
    }

    @Override
    public <T> T accept(BaseASTVisitor<T> v) throws BaseAstException {
        return v.visit(this);
    }
}
