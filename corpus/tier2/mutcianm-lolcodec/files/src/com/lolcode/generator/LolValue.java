package com.lolcode.generator;

/**
 * Created with IntelliJ IDEA.
 * User: miha
 * Date: 6/28/13
 * Time: 11:50 PM
 */

/**
 * Provides interface for language objects storing values, ie. variables, constants, arrays
 */
public interface LolValue {
    type getVarType();

    public enum type {
        INT,
        STRING,
        FLOAT,
        BOOL
    }

    String getStrType();

    String getStrName();

    Object getValue();

    /**
     * Compares by value's name.
     * FIXME must be rewritten to take into account value's scope
     */
    boolean equals(Object other);

    int hashCode();
}
