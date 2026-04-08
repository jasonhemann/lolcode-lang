package com.lolcode.generator;

import java.util.ArrayList;


/**
 * Created with IntelliJ IDEA.
 * User: miha
 * Date: 6/29/13
 * Time: 12:28 AM
 */
public class StringTable {
    private static StringTable instance;

    public static synchronized StringTable getInstance() {
        if (instance == null) {
            instance = new StringTable();
        }
        return instance;
    }

    private ArrayList<String> table;

    public int insertString(String str) {
        String index = (!table.isEmpty()) ? String.valueOf(table.size()) : "";
        table.add("@.str" + index + " = private unnamed_addr constant [" + (str.length() + 1) + " x i8] c\"" + str + "\\00\", align 1");
        return table.size();
    }

    public String getIndexRef(int index) {
        return "@.str" + ((index > 0) ? String.valueOf(index) : "");
    }

    public void spewTable() {

    }
}
