package com.lolcode.tree;

/**
 * Created with IntelliJ IDEA.
 * User: miha
 * Date: 7/12/13
 * Time: 2:48 PM
 */

/**
 * Defines class for lolcode expression.<p>
 * <li>binary math expressions(SUM OF/DIFF OF/PRODUKT OF/etc. )</li>
 * <li>binary logic(BOTH OF/EITHER OF/NOT)</li>
 * <li>comparison(BIGGR OF/SMALLR OF)</li>
 * <li>min/max expressions</li>
 * <li>funexpr - no idea what it is</li>
 * </p>
 */
public abstract class TreeExpression extends PositionedTreeNode implements TreeTypedValue {
    private TYPE type = TYPE.UNKNOWN;

    @Override
    public void setType(TYPE type) {
        this.type = type;
    }

    @Override
    public TYPE getType() {
        return type;
    }
}
