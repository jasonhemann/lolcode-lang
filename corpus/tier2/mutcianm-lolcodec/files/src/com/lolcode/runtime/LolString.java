package com.lolcode.runtime;

public class LolString extends LolObject {
    public LolString(LolType type) {
        super(type);
    }

    @Override
    public LolObject get(LolObject key) {
        if (key.type == LolType.STRING && key.strVal.equals("length"))
            return new LolInt(strVal.length());
        if (key.type != LolType.INT) {
            throw new LolRuntimeException("String index must be an integer");
        }
        return new LolString(String.valueOf(strVal.charAt(key.intVal)));
    }

    @Override
    public void put(LolObject index, LolObject value) {
        if (index.type != LolType.INT) {
            throw new LolRuntimeException("String index must be an integer");
        }
        if (value.type != LolType.STRING) {
            throw new LolRuntimeException("Only a string can be an element of a string");
        }
        if (value.strVal.length() != 1) {
            throw new LolRuntimeException("String element may only be of length 1");
        }
        strVal = strVal.substring(0, index.intVal) + value.strVal + strVal.substring(index.intVal + 1);
    }

    public LolString(String s) {
        type = LolType.STRING;
        strVal = s;
    }
}
