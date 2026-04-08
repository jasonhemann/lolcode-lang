package com.lolcode.tree;

import com.lolcode.Runner;
import org.junit.Before;
import org.junit.Test;

public class ArrayTest {
    private Runner runner;

    @Before
    public void setUp() throws Exception {
        runner = new Runner();
        runner.setInputFile("tests/com/lolcode/tree/arrays.lol");
    }

    @Test
    public void testTest() throws Exception {
        runner.test();
    }
}
