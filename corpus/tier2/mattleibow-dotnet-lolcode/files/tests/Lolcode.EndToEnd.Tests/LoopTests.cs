namespace Lolcode.EndToEnd.Tests;

public class LoopTests : EndToEndTestBase
{
    [Fact]
    public void InfiniteLoopGtfo()
    {
        AssertOutput("""
            BTW Test infinite loop with GTFO break
            BTW Loop with no operation/condition that uses GTFO to exit

            HAI 1.2
              VISIBLE "ENTERING INFINITE LOOP::"
              I HAS A count ITZ 0
              IM IN YR infiniteloop
                VISIBLE "  iteration " count
                count R SUM OF count AN 1
                BOTH SAEM count AN 3
                O RLY?
                  YA RLY
                    VISIBLE "  breaking at count = 3"
                    GTFO
                OIC
              IM OUTTA YR infiniteloop

              VISIBLE "LOOP EXITED"
            KTHXBYE
            """, "ENTERING INFINITE LOOP:\n  iteration 0\n  iteration 1\n  iteration 2\n  breaking at count = 3\nLOOP EXITED");
    }

    [Fact]
    public void LoopCounterZeroStart()
    {
        AssertOutput("""
            BTW Test UPPIN loop counter starts at 0 by default
            BTW Loop variable for UPPIN should start at 0, not 1

            HAI 1.2
              VISIBLE "UPPIN COUNTER STARTING VALUE::"
              IM IN YR starttest UPPIN YR counter TIL BOTH SAEM counter AN 3
                VISIBLE "  counter = " counter
              IM OUTTA YR starttest

              VISIBLE "FIRST VALUE WAS 0, NOT 1"
            KTHXBYE
            """, "UPPIN COUNTER STARTING VALUE:\n  counter = 0\n  counter = 1\n  counter = 2\nFIRST VALUE WAS 0, NOT 1");
    }

    [Fact]
    public void LoopGtfoBreak()
    {
        AssertOutput("""
            BTW Test GTFO breaks innermost loop only
            BTW GTFO should exit only the immediately enclosing loop

            HAI 1.2
              VISIBLE "TESTING GTFO IN NESTED LOOPS::"
              IM IN YR outerloop UPPIN YR i TIL BOTH SAEM i AN 4
                VISIBLE "OUTER:: i = " i
                IM IN YR innerloop UPPIN YR j TIL BOTH SAEM j AN 10
                  VISIBLE "  INNER:: j = " j
                  BOTH SAEM j AN 2
                  O RLY?
                    YA RLY
                      VISIBLE "  BREAKING INNER LOOP AT j = 2"
                      GTFO  BTW this should only break inner loop
                  OIC
                IM OUTTA YR innerloop
                VISIBLE "  BACK IN OUTER LOOP"
              IM OUTTA YR outerloop

              VISIBLE "ALL LOOPS DONE"
            KTHXBYE
            """, "TESTING GTFO IN NESTED LOOPS:\nOUTER: i = 0\n  INNER: j = 0\n  INNER: j = 1\n  INNER: j = 2\n  BREAKING INNER LOOP AT j = 2\n  BACK IN OUTER LOOP\nOUTER: i = 1\n  INNER: j = 0\n  INNER: j = 1\n  INNER: j = 2\n  BREAKING INNER LOOP AT j = 2\n  BACK IN OUTER LOOP\nOUTER: i = 2\n  INNER: j = 0\n  INNER: j = 1\n  INNER: j = 2\n  BREAKING INNER LOOP AT j = 2\n  BACK IN OUTER LOOP\nOUTER: i = 3\n  INNER: j = 0\n  INNER: j = 1\n  INNER: j = 2\n  BREAKING INNER LOOP AT j = 2\n  BACK IN OUTER LOOP\nALL LOOPS DONE");
    }

    [Fact]
    public void LoopVariableLocal()
    {
        AssertOutput("""
            BTW Test loop variable is local to loop, doesn't affect outer scope
            BTW Loop variable should not interfere with variables of same name outside

            HAI 1.2
              I HAS A i ITZ 99
              VISIBLE "BEFORE LOOP:: i = " i

              IM IN YR testloop UPPIN YR i TIL BOTH SAEM i AN 3
                VISIBLE "  IN LOOP:: i = " i
              IM OUTTA YR testloop

              VISIBLE "AFTER LOOP:: i = " i

              BTW test with different variable name
              I HAS A counter ITZ 42
              VISIBLE "BEFORE SECOND LOOP:: counter = " counter

              IM IN YR testloop2 UPPIN YR counter TIL BOTH SAEM counter AN 2
                VISIBLE "  IN LOOP2:: counter = " counter
              IM OUTTA YR testloop2

              VISIBLE "AFTER SECOND LOOP:: counter = " counter
            KTHXBYE
            """, "BEFORE LOOP: i = 99\n  IN LOOP: i = 0\n  IN LOOP: i = 1\n  IN LOOP: i = 2\nAFTER LOOP: i = 99\nBEFORE SECOND LOOP: counter = 42\n  IN LOOP2: counter = 0\n  IN LOOP2: counter = 1\nAFTER SECOND LOOP: counter = 42");
    }

    [Fact]
    public void LoopWithExpressions()
    {
        AssertOutput("""
            BTW Test complex expressions in TIL and WILE conditions
            BTW Loop conditions can use arithmetic and comparison expressions

            HAI 1.2
              BTW complex TIL condition with math
              VISIBLE "COMPLEX TIL CONDITION::"
              I HAS A limit ITZ 10
              IM IN YR complexloop UPPIN YR x TIL BOTH SAEM BIGGR OF x AN limit AN x
                VISIBLE "  x = " x ", limit = " limit
              IM OUTTA YR complexloop

              BTW complex WILE condition with multiple comparisons
              VISIBLE "COMPLEX WILE CONDITION::"
              I HAS A a ITZ 1
              I HAS A b ITZ 20
              IM IN YR wilecomplex UPPIN YR y WILE BOTH SAEM SMALLR OF a AN b AN a
                VISIBLE "  y = " y ", a = " a ", b = " b
                a R PRODUKT OF a AN 2
              IM OUTTA YR wilecomplex

              VISIBLE "DONE"
            KTHXBYE
            """, "COMPLEX TIL CONDITION:\n  x = 0, limit = 10\n  x = 1, limit = 10\n  x = 2, limit = 10\n  x = 3, limit = 10\n  x = 4, limit = 10\n  x = 5, limit = 10\n  x = 6, limit = 10\n  x = 7, limit = 10\n  x = 8, limit = 10\n  x = 9, limit = 10\nCOMPLEX WILE CONDITION:\n  y = 0, a = 1, b = 20\n  y = 1, a = 2, b = 20\n  y = 2, a = 4, b = 20\n  y = 3, a = 8, b = 20\n  y = 4, a = 16, b = 20\nDONE");
    }

    [Fact]
    public void NerfinLoop()
    {
        AssertOutput("""
            BTW Test NERFIN YR loop with TIL condition
            BTW NERFIN decrements loop variable from 0 downwards

            HAI 1.2
              VISIBLE "COUNTING DOWN FROM 0 TO -4::"
              IM IN YR nerfloop NERFIN YR j TIL BOTH SAEM j AN -5
                VISIBLE "  j = " j
              IM OUTTA YR nerfloop

              VISIBLE "DONE"
            KTHXBYE
            """, "COUNTING DOWN FROM 0 TO -4:\n  j = 0\n  j = -1\n  j = -2\n  j = -3\n  j = -4\nDONE");
    }

    [Fact]
    public void NestedLoops()
    {
        AssertOutput("""
            BTW Test nested loops with different labels
            BTW Verify inner and outer loops maintain separate counters

            HAI 1.2
              VISIBLE "NESTED LOOP TEST::"
              IM IN YR outerloop UPPIN YR i TIL BOTH SAEM i AN 3
                VISIBLE "OUTER i = " i
                IM IN YR innerloop UPPIN YR j TIL BOTH SAEM j AN 2
                  VISIBLE "  INNER j = " j
                IM OUTTA YR innerloop
              IM OUTTA YR outerloop

              VISIBLE "DONE"
            KTHXBYE
            """, "NESTED LOOP TEST:\nOUTER i = 0\n  INNER j = 0\n  INNER j = 1\nOUTER i = 1\n  INNER j = 0\n  INNER j = 1\nOUTER i = 2\n  INNER j = 0\n  INNER j = 1\nDONE");
    }

    [Fact]
    public void UppinLoop()
    {
        AssertOutput("""
            BTW Test UPPIN YR loop with TIL condition
            BTW UPPIN increments loop variable until condition is true

            HAI 1.2
              VISIBLE "COUNTING UP FROM 0 TO 4::"
              IM IN YR uploop UPPIN YR i TIL BOTH SAEM i AN 5
                VISIBLE "  i = " i
              IM OUTTA YR uploop

              VISIBLE "DONE"
            KTHXBYE
            """, "COUNTING UP FROM 0 TO 4:\n  i = 0\n  i = 1\n  i = 2\n  i = 3\n  i = 4\nDONE");
    }

    [Fact]
    public void WileLoop()
    {
        AssertOutput("""
            BTW Test WILE condition loop (loop while true)
            BTW WILE continues while expression evaluates to WIN

            HAI 1.2
              VISIBLE "DOUBLING UNTIL >= 100::"
              I HAS A val ITZ 1
              IM IN YR wileloop UPPIN YR n WILE BOTH SAEM SMALLR OF val AN 100 AN val
                VISIBLE "  val = " val
                val R PRODUKT OF val AN 2
              IM OUTTA YR wileloop

              VISIBLE "FINAL VAL:: " val
            KTHXBYE
            """, "DOUBLING UNTIL >= 100:\n  val = 1\n  val = 2\n  val = 4\n  val = 8\n  val = 16\n  val = 32\n  val = 64\nFINAL VAL: 128");
    }
}
