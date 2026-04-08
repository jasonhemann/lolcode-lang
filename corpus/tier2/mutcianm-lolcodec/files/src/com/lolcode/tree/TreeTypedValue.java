package com.lolcode.tree;

/**
 * Created with IntelliJ IDEA.
 * User: miha
 * Date: 7/17/13
 * Time: 2:16 PM
 */

/**
 * Describes interface to access types in AST nodes which support typing.
 */
public interface TreeTypedValue {

    void setType(TYPE type);

    TYPE getType();
}
