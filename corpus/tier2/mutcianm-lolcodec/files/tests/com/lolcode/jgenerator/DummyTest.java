package com.lolcode.jgenerator;

import com.lolcode.Runner;
import org.junit.Before;
import org.junit.Test;

public class DummyTest {
    private Runner runner;

    @Before
    public void setUp() throws Exception {
        runner = new Runner();
        runner.setInputFile("tests/com/lolcode/jgenerator/dummy.lol");
    }

    @Test
    public void testTest() throws Exception {
        runner.test();
    }
}
