package com.lolcode.runtime;

public class TestStdLib extends LolStdLib {

    public String out = "";

    public String in = "";

    @Override
    protected void putStr(String str) {
        out = str;
    }

    @Override
    protected String readStr() {
        return in;
    }
}
