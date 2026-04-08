package com.lolcode.runtime;


public class LolBool extends LolObject {
    public static final LolBool TRUE = new LolBool(true);
    public static final LolBool FALSE = new LolBool(false);

    public LolBool(LolType type) {
        super(type);
    }

    public LolBool(boolean value) {
        type = LolType.BOOL;
        intVal = value ? 1 : 0;
    }

    @Override
    public int toInt() {
        return intVal;
    }

}
