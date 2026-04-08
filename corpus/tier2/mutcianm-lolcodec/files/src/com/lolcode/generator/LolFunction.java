package com.lolcode.generator;

import java.util.ArrayList;
import java.util.HashMap;

/**
 * Created with IntelliJ IDEA.
 * User: miha
 * Date: 6/28/13
 * Time: 11:50 PM
 */
public class LolFunction {
    public LolFunction(String name, ArrayList<LolValue> args) {
        body = new StringBuffer();
        body.append("define void @").append(name).append("(");
        if (!args.isEmpty()) {
            body.append(args.get(0).getStrType()).append(" ").append(args.get(0).getStrName());
            addVariable(args.get(0));
        }
        for (LolValue v : args) {
            body.append(", ").append(v.getStrType()).append(" ").append(v.getStrName());
            addVariable(v);
        }
        body.append(") {");
    }

    public void addAddInst(LolValue lhs, LolValue rhsa, LolValue rhsb) {
        addOpCode(symbols.get(lhs) + " = add nsw i32 " + symbols.get(rhsa) + ", " + symbols.get(rhsb));
    }

    public void addSubInst(LolValue lhs, LolValue rhsa, LolValue rhsb) {
        addOpCode(symbols.get(lhs) + " = sub nsw i32 " + symbols.get(rhsa) + ", " + symbols.get(rhsb));
    }

    public void addMulInst(LolValue lhs, LolValue rhsa, LolValue rhsb) {
        addOpCode(symbols.get(lhs) + " = mul nsw i32 " + symbols.get(rhsa) + ", " + symbols.get(rhsb));
    }

    public void addDivInst(LolValue lhs, LolValue rhsa, LolValue rhsb) {
        addOpCode(symbols.get(lhs) + " = sdiv nsw i32 " + symbols.get(rhsa) + ", " + symbols.get(rhsb));
    }

    public void addAssignInst(LolValue lhs, LolValue rhs) {
        addOpCode("store");
    }

    public void addVisibleStmt(LolValue v) {
        String format;
        int tmp;
        switch (v.getVarType()) {
            case INT:
                tmp = StringTable.getInstance().insertString("%d\n");
                break;
            case STRING:
                tmp = StringTable.getInstance().insertString(v.getValue() + "\n");
                break;
            case FLOAT:
                tmp = StringTable.getInstance().insertString("%f\n");
                break;
            case BOOL:
                tmp = StringTable.getInstance().insertString("%d\n");
                break;
        }
//        addOpCode();
    }

    public void endFunction() {
        body.append("}\n\n");
    }

    private void addOpCode(String data) {
        body.append(data).append("\n");
    }

    public boolean addVariable(LolValue var) {
        if (!symbols.containsKey(var)) {
            symbols.put(var, "%" + var.getStrName());
            return true;
        }
        return false;
    }

    public LolValue getVarByName(String name) {
        for (LolValue v : symbols.keySet()) {
            if (v.getStrName().equals(name)) {
                return v;
            }
        }
        return null;
    }

    private StringBuffer body;
    private ArrayList<LolValue> vars;
    public HashMap<LolValue, String> symbols;
}
