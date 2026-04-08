package com.lolcode.runtime;

public class LolRtBinOpWrongTypeException extends LolRuntimeException {
    public LolRtBinOpWrongTypeException(String msg) {
        super(msg);
    }

    public LolRtBinOpWrongTypeException(String op, LolType lhs, LolType rhs) {
        super("Mismatched types in " + op + ": " + lhs + " and " + rhs);
    }
}
