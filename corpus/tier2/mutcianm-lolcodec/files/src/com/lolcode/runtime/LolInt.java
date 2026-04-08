package com.lolcode.runtime;

public class LolInt extends LolObject {
    public LolInt(LolType type) {
        super(type);
    }

    public LolInt(int intVal) {
        type = LolType.INT;
        this.intVal = intVal;
    }
}
