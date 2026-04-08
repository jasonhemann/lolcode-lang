package com.lolcode.runtime;

public class LolRtUnsupportedOpException extends LolRuntimeException {
    public LolRtUnsupportedOpException(String msg) {
        super(msg);
    }

    public LolRtUnsupportedOpException(String op, LolType type) {
        super("Operation " + op + " is unsupported by " + type);
    }
}
