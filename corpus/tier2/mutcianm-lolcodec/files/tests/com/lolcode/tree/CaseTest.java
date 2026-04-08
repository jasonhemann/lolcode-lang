package com.lolcode.tree;

import com.lolcode.Runner;
import org.junit.Before;
import org.junit.Test;

/**
 * Created with IntelliJ IDEA.
 * User: miha
 * Date: 7/20/13
 * Time: 10:29 PM
 */
public class CaseTest {

    private Runner runner;

    @Before
    public void setUp() throws Exception {
        runner = new Runner();
        runner.setInputFile("tests/com/lolcode/tree/case.lol");
    }

    @Test
    public void testTest() throws Exception {
        runner.test();
    }
}
