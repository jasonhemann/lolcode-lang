package com.lolcode.checker;

import com.lolcode.tree.TYPE;
import com.lolcode.tree.TreeFunction;
import com.lolcode.tree.TreeNode;
import com.lolcode.tree.TreeVariable;

/**
 * Created with IntelliJ IDEA.
 * User: miha
 * Date: 7/22/13
 * Time: 4:53 PM
 */
public class ErrorHandler {
    public static boolean clean = true;
    public static boolean disableWarnings;


    private static void err(TreeNode.position pos, String what) {
        clean = false;
        String tmp = pos.toString() + "\t";
        System.err.println(tmp + what);
    }

    private static void warn(TreeNode.position pos, String what) {
        if (disableWarnings) return;
        String tmp = pos.toString() + " ";
        System.out.println(tmp + what);
    }

    public static void otherError(TreeNode.position pos, String message) {
        err(pos, message);
    }

    public static void warnCaseOverride(TreeNode.position pos, String label) {
        warn(pos, "Label \"" + label + "\" in case statement overrides previous");
    }

    public static void warnAmbiguousReturnType(TreeNode.position pos, TreeFunction func) {
        warn(pos, "Function \"" + func.getName() + "\" has ambiguous return type");
    }

    public static void castError(TreeNode.position pos, String op, TYPE ltype, TYPE rtype) {
        err(pos, "Unexpected types in \"" + op + "\"\t" + ltype + " and " + rtype);
    }

    public static void redeclaredVarible(TreeNode.position pos, TreeVariable var) {
        err(pos, "Variable \"" + var.getName() + "\" is redeclared in current scope");
    }

    public static void undeclaredVariable(TreeNode.position pos, String var) {
        err(pos, "Variable \"" + var + "\" is undeclared in current scope");
    }

    public static void redeclaredFunction(TreeNode.position pos, TreeFunction func) {
        err(pos, "Function \"" + func.getName() + "\" is redeclared");
    }

    public static void undeclaredFunction(TreeNode.position pos, String func) {
        err(pos, "Function \"" + func + "\" is undeclared");
    }

    public static void wrongArguments(TreeNode.position pos, TreeFunction func, int got) {
        err(pos, "Function \"" + func.getName() + "\" expects " + func.getParams().size() + " argument(s), given " + got);
    }
}
