package com.lolcode.runtime;

public class LolRtNoSuchKeyException extends LolRuntimeException {
    public LolRtNoSuchKeyException(String msg) {
        super(msg);
    }

    public LolRtNoSuchKeyException(LolObject key) {
        super("No such key: " + key.toLolString().strVal);
    }
}
