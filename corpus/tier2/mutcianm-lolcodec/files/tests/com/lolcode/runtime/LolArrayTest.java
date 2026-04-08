package com.lolcode.runtime;

import org.junit.Assert;
import org.junit.Test;

public class LolArrayTest {

    @Test(expected = LolRtNoSuchKeyException.class)
    public void testInvalidKey() throws Exception {
        LolArray array = new LolArray(new LolInt(23), new LolDouble(21));
        array.get(new LolString("InVALD KEY"));
    }


    @Test
    public void testGet() throws Exception {
        LolArray array = new LolArray(new LolInt(23), new LolDouble(21));
        array.put(new LolString("ASASSS"), new LolString("MEH"));
        Assert.assertTrue(array.get(new LolInt(0)).eq(new LolInt(23)).toBool());
        Assert.assertTrue(array.get(new LolString("1")).eq(new LolDouble(21)).toBool());
        Assert.assertTrue(array.get(new LolString("ASASSS")).eq(new LolString("MEH")).toBool());
    }


    @Test
    public void testPut() throws Exception {
        LolArray array = new LolArray(new LolInt(23), new LolDouble(21));
        array.put(new LolString("ASASSS"), new LolString("MEH"));
        Assert.assertTrue(array.get(new LolString("length")).eq(new LolInt(3)).toBool());
    }
}
