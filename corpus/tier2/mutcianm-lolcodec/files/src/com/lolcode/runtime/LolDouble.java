package com.lolcode.runtime;

public class LolDouble extends LolObject {
    public LolDouble(LolType type) {
        super(type);
    }

    public LolDouble(double d) {
        type = LolType.DOUBLE;
        doubleVal = d;
    }
}
