namespace Lolcode.EndToEnd.Tests;

public class FunctionTests : EndToEndTestBase
{
    [Fact]
    public void BasicFunction()
    {
        AssertOutput("""
            HAI 1.2
              BTW Test basic function definition and calling with no parameters

              HOW IZ I greet
                VISIBLE "Hello from function!"
              IF U SAY SO

              I IZ greet MKAY
            KTHXBYE
            """, "Hello from function!");
    }

    [Fact]
    public void FunctionCallAsExpression()
    {
        AssertOutput("""
            HAI 1.2
              BTW Test function call as bare expression statement (stores result in IT)

              HOW IZ I getNumber
                FOUND YR 99
              IF U SAY SO

              I IZ getNumber MKAY
              BTW Function call result is now in IT
              VISIBLE IT
            KTHXBYE
            """, "99");
    }

    [Fact]
    public void FunctionCallInExpression()
    {
        AssertOutput("""
            HAI 1.2
              BTW Test function call nested inside other expressions

              HOW IZ I getValue
                FOUND YR 10
              IF U SAY SO

              I HAS A result ITZ SUM OF I IZ getValue MKAY AN 5
              VISIBLE result

              VISIBLE "Result:: " I IZ getValue MKAY
            KTHXBYE
            """, "15\nResult: 10");
    }

    [Fact]
    public void FunctionGtfo()
    {
        AssertOutput("""
            HAI 1.2
              BTW Test GTFO in function returns NOOB

              HOW IZ I earlyExit YR x
                BOTH SAEM x AN 5
                O RLY?
                  YA RLY
                    GTFO
                OIC
                FOUND YR "reached end"
              IF U SAY SO

              I HAS A result1 ITZ I IZ earlyExit YR 5 MKAY
              I HAS A result2 ITZ I IZ earlyExit YR 10 MKAY

              BTW NOOB casts to empty string
              VISIBLE "Result1:: " result1
              VISIBLE "Result2:: " result2
            KTHXBYE
            """, "Result1: \nResult2: reached end");
    }

    [Fact]
    public void FunctionImplicitReturn()
    {
        AssertOutput("""
            HAI 1.2
              BTW Test implicit return of IT at end of function

              HOW IZ I implicitReturn YR x
                SUM OF x AN 10
                BTW Above sets IT, which is returned implicitly
              IF U SAY SO

              I HAS A result ITZ I IZ implicitReturn YR 5 MKAY
              VISIBLE result
            KTHXBYE
            """, "15");
    }

    [Fact]
    public void FunctionItIndependent()
    {
        AssertOutput("""
            HAI 1.2
              BTW Test that each function has its own IT, independent of caller's IT

              HOW IZ I modifyIT
                SUM OF 50 AN 50
                BTW Above sets IT to 100 inside function
                VISIBLE "Function IT:: " IT
              IF U SAY SO

              SUM OF 10 AN 10
              BTW IT is now 20 in main scope
              VISIBLE "Before call:: " IT

              I IZ modifyIT MKAY

              VISIBLE "After call:: " IT
              BTW IT in main should still be 20
            KTHXBYE
            """, "Before call: 20\nFunction IT: 100\nAfter call: 100");
    }

    [Fact]
    public void FunctionNoArgs()
    {
        AssertOutput("""
            HAI 1.2
              BTW Test function with no arguments

              HOW IZ I sayHai
                VISIBLE "HAI!"
                FOUND YR 42
              IF U SAY SO

              I HAS A result ITZ I IZ sayHai MKAY
              VISIBLE result
            KTHXBYE
            """, "HAI!\n42");
    }

    [Fact]
    public void FunctionParams()
    {
        AssertOutput("""
            HAI 1.2
              BTW Test functions with 1, 2, and 3 parameters

              HOW IZ I oneParam YR x
                VISIBLE "One:: " x
              IF U SAY SO

              HOW IZ I twoParams YR x AN YR y
                VISIBLE "Two:: " x " and " y
              IF U SAY SO

              HOW IZ I threeParams YR x AN YR y AN YR z
                VISIBLE "Three:: " x ", " y ", " z
              IF U SAY SO

              I IZ oneParam YR "A" MKAY
              I IZ twoParams YR "B" AN YR "C" MKAY
              I IZ threeParams YR "D" AN YR "E" AN YR "F" MKAY
            KTHXBYE
            """, "One: A\nTwo: B and C\nThree: D, E, F");
    }

    [Fact]
    public void FunctionReturn()
    {
        AssertOutput("""
            HAI 1.2
              BTW Test FOUND YR returning different types

              HOW IZ I returnNumber
                FOUND YR 42
              IF U SAY SO

              HOW IZ I returnFloat
                FOUND YR 3.14
              IF U SAY SO

              HOW IZ I returnString
                FOUND YR "YARN"
              IF U SAY SO

              HOW IZ I returnBool
                FOUND YR WIN
              IF U SAY SO

              I HAS A num ITZ I IZ returnNumber MKAY
              I HAS A flt ITZ I IZ returnFloat MKAY
              I HAS A str ITZ I IZ returnString MKAY
              I HAS A bool ITZ I IZ returnBool MKAY

              VISIBLE num
              VISIBLE flt
              VISIBLE str
              VISIBLE bool
            KTHXBYE
            """, "42\n3.14\nYARN\nWIN");
    }

    [Fact]
    public void FunctionScopeIsolation()
    {
        AssertOutput("""
            HAI 1.2
              BTW Test that function variables with same name as outer variables are independent

              I HAS A x ITZ 100

              HOW IZ I testScope
                I HAS A x ITZ 42
                VISIBLE "Inside function:: " x
              IF U SAY SO

              I IZ testScope MKAY
              VISIBLE "Outside function:: " x
            KTHXBYE
            """, "Inside function: 42\nOutside function: 100");
    }

    [Fact]
    public void MultipleFunctions()
    {
        AssertOutput("""
            HAI 1.2
              BTW Test multiple function definitions calling each other

              HOW IZ I add YR a AN YR b
                FOUND YR SUM OF a AN b
              IF U SAY SO

              HOW IZ I multiply YR a AN YR b
                FOUND YR PRODUKT OF a AN b
              IF U SAY SO

              HOW IZ I addAndMultiply YR x AN YR y AN YR z
                I HAS A sum ITZ I IZ add YR x AN YR y MKAY
                FOUND YR I IZ multiply YR sum AN YR z MKAY
              IF U SAY SO

              I HAS A result ITZ I IZ addAndMultiply YR 3 AN YR 4 AN YR 5 MKAY
              VISIBLE result
            KTHXBYE
            """, "35");
    }

    [Fact]
    public void RecursiveFunction()
    {
        AssertOutput("""
            HAI 1.2
              BTW Test recursive function (factorial)

              HOW IZ I factorial YR n
                BOTH SAEM n AN 0
                O RLY?
                  YA RLY
                    FOUND YR 1
                OIC
                FOUND YR PRODUKT OF n AN I IZ factorial YR DIFF OF n AN 1 MKAY
              IF U SAY SO

              I HAS A result ITZ I IZ factorial YR 5 MKAY
              VISIBLE result
            KTHXBYE
            """, "120");
    }
}
