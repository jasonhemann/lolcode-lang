package com.lolcode.runtime;

import org.junit.Assert;
import org.junit.Test;

public class LolObjectTest {

    @Test
    public void testToBool() throws Exception {
        Assert.assertTrue(new LolBool(true).toBool());
        Assert.assertFalse(new LolBool(false).toBool());
    }

    @Test
    public void testGet() throws Exception {
        LolObject o = new LolObject();
        try {
            o.get(o);
            Assert.fail("LolRuntimeException not thrown");
        } catch (LolRuntimeException e) {
        }
    }

    @Test
    public void testPut() throws Exception {
        LolObject o = new LolObject();
        try {
            o.put(o, o);
            Assert.fail("LolRuntimeException not thrown");
        } catch (LolRuntimeException e) {
        }
    }


    private void testCompareException(LolObject lhs, LolObject rhs) {
        try {
            lhs.compare(rhs);
            Assert.fail("LolRtUnsupportedOpException not thrown");
        } catch (LolRtBadCompareException e) {
        }
    }

    @Test
    public void testCompare() throws Exception {
        Assert.assertEquals(new LolBool(true).compare(new LolBool(true)).intVal, 0);
        Assert.assertEquals(new LolBool(true).compare(new LolBool(false)).intVal, 1);
        Assert.assertEquals(new LolBool(false).compare(new LolBool(true)).intVal, -1);
        Assert.assertEquals(new LolInt(100).compare(new LolInt(100)).intVal, 0);
        Assert.assertEquals(new LolInt(100).compare(new LolInt(0)).intVal, 1);
        Assert.assertEquals(new LolInt(1).compare(new LolInt(2)).intVal, -1);
        Assert.assertEquals(new LolInt(-100).compare(new LolInt(-2)).intVal, -1);
        Assert.assertEquals(new LolDouble(3.14159265359).compare(new LolDouble(3.14159265359)).intVal, 0);
        Assert.assertEquals(new LolDouble(3.14159265359).compare(new LolDouble(-3.14159265359)).intVal, 1);
        Assert.assertEquals(new LolDouble(3.1).compare(new LolDouble(3.14159265359)).intVal, -1);
        Assert.assertEquals(new LolString("testCompare").compare(new LolString("testCompare")).intVal, 0);
        Assert.assertEquals(new LolString("aaac").compare(new LolString("aaaa")).intVal, 2);
        Assert.assertEquals(new LolString("aaa").compare(new LolString("aaaaaa")).intVal, -3);

        testCompareException(new LolBool(true), new LolDouble(1.3));
        testCompareException(new LolBool(true), new LolInt(1));
        testCompareException(new LolBool(true), new LolString(""));
        testCompareException(new LolInt(1), new LolDouble(1.4));
        testCompareException(new LolInt(1), new LolString(""));
        testCompareException(new LolDouble(1.3), new LolString(""));
    }

    private void doTestToLolBool(LolObject o, boolean result) {
        Assert.assertEquals(o.toLolBool().toBool(), result);
    }

    @Test
    public void testToLolBool() throws Exception {
        doTestToLolBool(new LolDouble(1.234234), true);
        doTestToLolBool(new LolDouble(0), false);
        doTestToLolBool(new LolString("str"), true);
        doTestToLolBool(new LolString(""), false);
        doTestToLolBool(new LolInt(123), true);
        doTestToLolBool(new LolInt(0), false);
        try {
            doTestToLolBool(new LolObject(), true);
            Assert.fail("LolRtUnsupportedOpException not thrown");
        } catch (LolRtUnsupportedOpException e) {
        }
    }

    private void doTestToLolInt(LolObject o, int result) {
        Assert.assertEquals(o.toLolInt().intVal, result);
    }

    @Test
    public void testToLolInt() throws Exception {
        doTestToLolInt(new LolBool(true), 1);
        doTestToLolInt(new LolBool(false), 0);
        doTestToLolInt(new LolDouble(3.14159265359), 3);
        doTestToLolInt(new LolString("314"), 314);
        try {
            doTestToLolInt(new LolObject(), 1);
            Assert.fail("LolRtUnsupportedOpException not thrown");
        } catch (LolRtUnsupportedOpException e) {
        }
    }

    private void doTestToLolDouble(LolObject o, double result) {
        Assert.assertEquals(o.toLolDouble().doubleVal, result, 0);
    }

    @Test
    public void testToLolDouble() throws Exception {
        doTestToLolDouble(new LolBool(true), 1.0);
        doTestToLolDouble(new LolBool(false), 0.0);
        doTestToLolDouble(new LolInt(39), 39.0);
        doTestToLolDouble(new LolString("3.14159265359"), 3.14159265359);
        try {
            doTestToLolDouble(new LolObject(), 1);
            Assert.fail("LolRtUnsupportedOpException not thrown");
        } catch (LolRtUnsupportedOpException e) {
        }
    }

    private void doTestToLolString(LolObject o, String result) {
        Assert.assertEquals(o.toLolString().strVal, result);
    }

    @Test
    public void testToLolString() throws Exception {
        doTestToLolString(new LolBool(true), "true");
        doTestToLolString(new LolBool(false), "false");
        doTestToLolString(new LolInt(39), "39");
        doTestToLolString(new LolDouble(3.14159265359), "3.14159265359");
        try {
            doTestToLolString(new LolObject(), "");
            Assert.fail("LolRtUnsupportedOpException not thrown");
        } catch (LolRtUnsupportedOpException e) {
        }
    }

    private void testAddExceptions(LolObject lhs, LolObject rhs) {
        try {
            lhs.add(rhs);
            Assert.fail("Exception not thrown");
        } catch (LolRtBinOpWrongTypeException | LolRtUnsupportedOpException e) {
        }
    }

    @Test
    public void testAdd() throws Exception {
        Assert.assertEquals(new LolInt(123).add(new LolInt(321)).intVal, 444);
        Assert.assertEquals(new LolDouble(3.14159265359).add(new LolDouble(2.71828182846)).doubleVal, 5.8598744820499995, 0);
        Assert.assertEquals(new LolString("aaaa").add(new LolString("0000")).strVal, "aaaa0000");
        Assert.assertEquals(new LolInt(123).add(new LolDouble(3.21)).doubleVal, 126.21, 0.001);
        Assert.assertEquals(new LolDouble(3.21).add(new LolInt(3)).doubleVal, 6.21, 0.001);

        testAddExceptions(new LolBool(true), new LolDouble(123));
        testAddExceptions(new LolBool(true), new LolInt(123));
        testAddExceptions(new LolBool(true), new LolString(""));
        testAddExceptions(new LolDouble(123), new LolString(""));
        testAddExceptions(new LolString(""), new LolInt(1));
        testAddExceptions(new LolBool(true), new LolBool(true));
        try {
            new LolObject().add(new LolObject());
            Assert.fail("LolRtUnsupportedOpException not thrown");
        } catch (LolRtUnsupportedOpException e) {
        }
    }

    private void testSubExceptions(LolObject lhs, LolObject rhs) {
        try {
            lhs.sub(rhs);
            Assert.fail("Exception not thrown");
        } catch (LolRtBinOpWrongTypeException | LolRtUnsupportedOpException e) {
        }
    }

    @Test
    public void testSub() throws Exception {
        Assert.assertEquals(new LolInt(444).sub(new LolInt(321)).intVal, 123);
        Assert.assertEquals(new LolDouble(5.8598744820499995).sub(new LolDouble(2.71828182846)).doubleVal, 3.1415926535899996, 0);
        Assert.assertEquals(new LolInt(123).sub(new LolDouble(3.21)).doubleVal, 119.79, 0.001);
        Assert.assertEquals(new LolDouble(3.21).sub(new LolInt(3)).doubleVal, 0.21, 0.001);

        testSubExceptions(new LolBool(true), new LolDouble(123));
        testSubExceptions(new LolBool(true), new LolInt(123));
        testSubExceptions(new LolBool(true), new LolString(""));
        testSubExceptions(new LolDouble(123), new LolString(""));
        testSubExceptions(new LolString(""), new LolInt(1));
        testSubExceptions(new LolBool(true), new LolBool(true));
        testSubExceptions(new LolString(""), new LolString(""));
        try {
            new LolObject().sub(new LolObject());
            Assert.fail("LolRtUnsupportedOpException not thrown");
        } catch (LolRtUnsupportedOpException e) {
        }
    }

    private void testMulExceptions(LolObject lhs, LolObject rhs) {
        try {
            lhs.mul(rhs);
            Assert.fail("Exception not thrown");
        } catch (LolRtBinOpWrongTypeException | LolRtUnsupportedOpException e) {
        }
    }

    @Test
    public void testMul() throws Exception {
        Assert.assertEquals(new LolInt(123).mul(new LolInt(321)).intVal, 39483);
        Assert.assertEquals(new LolDouble(1.23).mul(new LolDouble(3.21)).doubleVal, 3.9483, 0.00000001);
        Assert.assertEquals(new LolInt(123).mul(new LolDouble(3.21)).doubleVal, 394.83, 0.001);
        Assert.assertEquals(new LolDouble(1.23).mul(new LolInt(321)).doubleVal, 394.83, 0.001);

        testMulExceptions(new LolBool(true), new LolDouble(123));
        testMulExceptions(new LolBool(true), new LolInt(123));
        testMulExceptions(new LolBool(true), new LolString(""));
        testMulExceptions(new LolDouble(123), new LolString(""));
        testMulExceptions(new LolString(""), new LolInt(1));
        testMulExceptions(new LolBool(true), new LolBool(true));
        testMulExceptions(new LolString(""), new LolString(""));
        try {
            new LolObject().mul(new LolObject());
            Assert.fail("LolRtUnsupportedOpException not thrown");
        } catch (LolRtUnsupportedOpException e) {
        }
    }

    private void testDivExceptions(LolObject lhs, LolObject rhs) {
        try {
            lhs.div(rhs);
            Assert.fail("Exception not thrown");
        } catch (LolRtBinOpWrongTypeException | LolRtUnsupportedOpException e) {
        }
    }

    @Test
    public void testDiv() throws Exception {
        Assert.assertEquals(new LolInt(321).div(new LolInt(123)).intVal, 2);
        Assert.assertEquals(new LolDouble(1.23).div(new LolDouble(3.21)).doubleVal, 0.38317, 0.00001);
        Assert.assertEquals(new LolInt(123).div(new LolDouble(3.21)).doubleVal, 38.3177, 0.001);
        Assert.assertEquals(new LolDouble(1.23).div(new LolInt(321)).doubleVal, 0.00383177, 0.00001);

        testDivExceptions(new LolBool(true), new LolDouble(123));
        testDivExceptions(new LolBool(true), new LolInt(123));
        testDivExceptions(new LolBool(true), new LolString(""));
        testDivExceptions(new LolDouble(123), new LolString(""));
        testDivExceptions(new LolString(""), new LolInt(1));
        testDivExceptions(new LolBool(true), new LolBool(true));
        testDivExceptions(new LolString(""), new LolString(""));
        try {
            new LolObject().div(new LolObject());
            Assert.fail("LolRtUnsupportedOpException not thrown");
        } catch (LolRtUnsupportedOpException e) {
        }
    }

    private void testModExceptions(LolObject lhs, LolObject rhs) {
        try {
            lhs.mod(rhs);
            Assert.fail("Exception not thrown");
        } catch (LolRtBinOpWrongTypeException | LolRtUnsupportedOpException e) {
        }
    }

    @Test
    public void testMod() throws Exception {
        Assert.assertEquals(new LolInt(321).mod(new LolInt(123)).intVal, 75);
        Assert.assertEquals(new LolDouble(3.21).mod(new LolDouble(1.23)).doubleVal, 0.75, 0.00001);
        //fixme: should this even work?
        Assert.assertEquals(new LolInt(321).mod(new LolDouble(1.23)).doubleVal, 1.2, 0.001);
        Assert.assertEquals(new LolDouble(321.0).mod(new LolInt(123)).doubleVal, 75.0, 0.00001);

        testModExceptions(new LolBool(true), new LolDouble(123));
        testModExceptions(new LolBool(true), new LolInt(123));
        testModExceptions(new LolBool(true), new LolString(""));
        testModExceptions(new LolDouble(123), new LolString(""));
        testModExceptions(new LolString(""), new LolInt(1));
        testModExceptions(new LolBool(true), new LolBool(true));
        testModExceptions(new LolString(""), new LolString(""));
        try {
            new LolObject().mod(new LolObject());
            Assert.fail("LolRtUnsupportedOpException not thrown");
        } catch (LolRtUnsupportedOpException e) {
        }
    }

    private void testAndExceptions(LolObject lhs, LolObject rhs) {
        try {
            lhs.and(rhs);
            Assert.fail("Exception not thrown");
        } catch (LolRtBinOpWrongTypeException | LolRtUnsupportedOpException e) {
        }
    }

    @Test
    public void testAnd() throws Exception {
        Assert.assertEquals(new LolBool(true).and(new LolBool(true)).toBool(), true);
        Assert.assertEquals(new LolBool(true).and(new LolBool(false)).toBool(), false);
        Assert.assertEquals(new LolBool(false).and(new LolBool(true)).toBool(), false);
        Assert.assertEquals(new LolBool(false).and(new LolBool(false)).toBool(), false);

        testAndExceptions(new LolInt(123), new LolDouble(123));
        testAndExceptions(new LolInt(123), new LolInt(123));
        testAndExceptions(new LolBool(true), new LolString(""));
        testAndExceptions(new LolDouble(123), new LolString(""));
        testAndExceptions(new LolString(""), new LolInt(1));
        testAndExceptions(new LolString(""), new LolString(""));
        try {
            new LolObject().and(new LolObject());
            Assert.fail("LolRtUnsupportedOpException not thrown");
        } catch (LolRtUnsupportedOpException e) {
        }
    }

    private void testOrExceptions(LolObject lhs, LolObject rhs) {
        try {
            lhs.or(rhs);
            Assert.fail("Exception not thrown");
        } catch (LolRtBinOpWrongTypeException | LolRtUnsupportedOpException e) {
        }
    }

    @Test
    public void testOr() throws Exception {
        Assert.assertEquals(new LolBool(true).or(new LolBool(true)).toBool(), true);
        Assert.assertEquals(new LolBool(true).or(new LolBool(false)).toBool(), true);
        Assert.assertEquals(new LolBool(false).or(new LolBool(true)).toBool(), true);
        Assert.assertEquals(new LolBool(false).or(new LolBool(false)).toBool(), false);

        testOrExceptions(new LolInt(123), new LolDouble(123));
        testOrExceptions(new LolInt(123), new LolInt(123));
        testOrExceptions(new LolBool(true), new LolString(""));
        testOrExceptions(new LolDouble(123), new LolString(""));
        testOrExceptions(new LolString(""), new LolInt(1));
        testOrExceptions(new LolString(""), new LolString(""));
        try {
            new LolObject().or(new LolObject());
            Assert.fail("LolRtUnsupportedOpException not thrown");
        } catch (LolRtUnsupportedOpException e) {
        }
    }

    private void testNotExceptions(LolObject lhs) {
        try {
            lhs.not();
            Assert.fail("Exception not thrown");
        } catch (LolRtBinOpWrongTypeException | LolRtUnsupportedOpException e) {
        }
    }

    @Test
    public void testNot() throws Exception {
        Assert.assertEquals(new LolBool(true).not().toBool(), false);
        Assert.assertEquals(new LolBool(false).not().toBool(), true);

        testNotExceptions(new LolInt(123));
        testNotExceptions(new LolDouble(123));
        testNotExceptions(new LolString(""));
        try {
            new LolObject().not();
            Assert.fail("LolRtUnsupportedOpException not thrown");
        } catch (LolRtUnsupportedOpException e) {
        }
    }

    private void testEqExceptions(LolObject lhs, LolObject rhs) {
        try {
            lhs.eq(rhs);
            Assert.fail("Exception not thrown");
        } catch (LolRtBadCompareException e) {
        }
    }

    @Test
    public void testEq() throws Exception {
        Assert.assertEquals(new LolBool(true).eq(new LolBool(true)).toBool(), true);
        Assert.assertEquals(new LolBool(true).eq(new LolBool(false)).toBool(), false);
        Assert.assertEquals(new LolBool(false).eq(new LolBool(true)).toBool(), false);
        Assert.assertEquals(new LolInt(100).eq(new LolInt(100)).toBool(), true);
        Assert.assertEquals(new LolInt(100).eq(new LolInt(0)).toBool(), false);
        Assert.assertEquals(new LolInt(1).eq(new LolInt(2)).toBool(), false);
        Assert.assertEquals(new LolInt(-100).eq(new LolInt(-2)).toBool(), false);
        Assert.assertEquals(new LolDouble(3.14159265359).eq(new LolDouble(3.14159265359)).toBool(), true);
        Assert.assertEquals(new LolDouble(3.14159265359).eq(new LolDouble(-3.14159265359)).toBool(), false);
        Assert.assertEquals(new LolDouble(3.1).eq(new LolDouble(3.14159265359)).toBool(), false);
        Assert.assertEquals(new LolString("testCompare").eq(new LolString("testCompare")).toBool(), true);
        Assert.assertEquals(new LolString("aaac").eq(new LolString("aaaa")).toBool(), false);

        testEqExceptions(new LolBool(true), new LolDouble(1.3));
        testEqExceptions(new LolBool(true), new LolInt(1));
        testEqExceptions(new LolBool(true), new LolString(""));
        testEqExceptions(new LolInt(1), new LolDouble(1.4));
        testEqExceptions(new LolInt(1), new LolString(""));
        testEqExceptions(new LolDouble(1.3), new LolString(""));
    }

    private void testNeqExceptions(LolObject lhs, LolObject rhs) {
        try {
            lhs.neq(rhs);
            Assert.fail("Exception not thrown");
        } catch (LolRtBadCompareException e) {
        }
    }

    @Test
    public void testNeq() throws Exception {
        Assert.assertEquals(new LolBool(true).neq(new LolBool(true)).toBool(), false);
        Assert.assertEquals(new LolBool(true).neq(new LolBool(false)).toBool(), true);
        Assert.assertEquals(new LolBool(false).neq(new LolBool(true)).toBool(), true);
        Assert.assertEquals(new LolInt(100).neq(new LolInt(100)).toBool(), false);
        Assert.assertEquals(new LolInt(100).neq(new LolInt(0)).toBool(), true);
        Assert.assertEquals(new LolInt(1).neq(new LolInt(2)).toBool(), true);
        Assert.assertEquals(new LolInt(-100).neq(new LolInt(-2)).toBool(), true);
        Assert.assertEquals(new LolDouble(3.14159265359).neq(new LolDouble(3.14159265359)).toBool(), false);
        Assert.assertEquals(new LolDouble(3.14159265359).neq(new LolDouble(-3.14159265359)).toBool(), true);
        Assert.assertEquals(new LolDouble(3.1).neq(new LolDouble(3.14159265359)).toBool(), true);
        Assert.assertEquals(new LolString("testCompare").neq(new LolString("testCompare")).toBool(), false);
        Assert.assertEquals(new LolString("aaac").neq(new LolString("aaaa")).toBool(), true);

        testNeqExceptions(new LolBool(true), new LolDouble(1.3));
        testNeqExceptions(new LolBool(true), new LolInt(1));
        testNeqExceptions(new LolBool(true), new LolString(""));
        testNeqExceptions(new LolInt(1), new LolDouble(1.4));
        testNeqExceptions(new LolInt(1), new LolString(""));
        testNeqExceptions(new LolDouble(1.3), new LolString(""));
    }
}
