namespace Lolcode.EndToEnd.Tests;

public class GtfoTests : EndToEndTestBase
{
    [Fact]
    public void GtfoInLoop()
    {
        AssertOutput("""
            BTW Test GTFO breaks out of loop context
            BTW GTFO in loop should exit the loop, not anything else

            HAI 1.2
              VISIBLE "TESTING GTFO IN LOOP::"
              I HAS A counter ITZ 0
              IM IN YR testloop UPPIN YR i TIL BOTH SAEM i AN 10
                VISIBLE "  iteration " i
                counter R SUM OF counter AN 1
                BOTH SAEM counter AN 3
                O RLY?
                  YA RLY
                    VISIBLE "  breaking at counter = 3"
                    GTFO  BTW should break the loop
                OIC
                VISIBLE "  end of iteration " i
              IM OUTTA YR testloop

              VISIBLE "AFTER LOOP"
            KTHXBYE
            """, "TESTING GTFO IN LOOP:\n  iteration 0\n  end of iteration 0\n  iteration 1\n  end of iteration 1\n  iteration 2\n  breaking at counter = 3\nAFTER LOOP");
    }

    [Fact]
    public void GtfoInSwitch()
    {
        AssertOutput("""
            BTW Test GTFO breaks out of switch case context
            BTW GTFO in switch should break case execution, not anything else

            HAI 1.2
              VISIBLE "TESTING GTFO IN SWITCH::"
              I HAS A test_val ITZ 2
              test_val
              WTF?
                OMG 1
                  VISIBLE "  case 1"
                OMG 2
                  VISIBLE "  case 2 - before GTFO"
                  GTFO  BTW should break switch case execution
                  VISIBLE "  case 2 - after GTFO (should not execute)"
                OMG 3
                  VISIBLE "  case 3 (should not execute due to GTFO)"
              OIC

              VISIBLE "AFTER SWITCH"
            KTHXBYE
            """, "TESTING GTFO IN SWITCH:\n  case 2 - before GTFO\nAFTER SWITCH");
    }

    [Fact]
    public void GtfoNestedLoopSwitch()
    {
        AssertOutput("""
            BTW Test GTFO in nested contexts (switch inside loop)
            BTW GTFO should break innermost context: switch, not the loop

            HAI 1.2
              VISIBLE "NESTED SWITCH INSIDE LOOP::"
              IM IN YR outerloop UPPIN YR i TIL BOTH SAEM i AN 3
                VISIBLE "LOOP iteration " i
                I HAS A switch_val ITZ 2
                switch_val
                WTF?
                  OMG 1
                    VISIBLE "  switch case 1"
                    GTFO  BTW breaks switch only
                  OMG 2
                    VISIBLE "  switch case 2"
                    GTFO  BTW breaks switch only, loop should continue
                  OMG 3
                    VISIBLE "  switch case 3"
                OIC
                VISIBLE "  back in loop after switch"
              IM OUTTA YR outerloop

              VISIBLE "ALL DONE"
            KTHXBYE
            """, "NESTED SWITCH INSIDE LOOP:\nLOOP iteration 0\n  switch case 2\n  back in loop after switch\nLOOP iteration 1\n  switch case 2\n  back in loop after switch\nLOOP iteration 2\n  switch case 2\n  back in loop after switch\nALL DONE");
    }
}
