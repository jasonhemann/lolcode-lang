namespace Lolcode.EndToEnd.Tests;

public class ConditionalTests : EndToEndTestBase
{
    [Fact]
    public void BasicIfElse()
    {
        AssertOutput("""
            BTW Test basic O RLY? / YA RLY / NO WAI / OIC structure
            BTW Simple if-else with both branches

            HAI 1.2
              BTW test true condition
              WIN
              O RLY?
                YA RLY
                  VISIBLE "TRUE BRANCH"
                NO WAI
                  VISIBLE "FALSE BRANCH"
              OIC

              BTW test false condition
              FAIL
              O RLY?
                YA RLY
                  VISIBLE "TRUE BRANCH"
                NO WAI
                  VISIBLE "FALSE BRANCH"
              OIC
            KTHXBYE
            """, "TRUE BRANCH\nFALSE BRANCH");
    }

    [Fact]
    public void CommaOnConditional()
    {
        AssertOutput("""
            BTW Test comma on same line with O RLY? (soft-command-break)
            BTW Expression can set IT, then comma, then O RLY? on same line

            HAI 1.2
              I HAS A x ITZ 7
              I HAS A y ITZ 7

              BOTH SAEM x AN y, O RLY?
                YA RLY, VISIBLE "X EQUALS Y"
                NO WAI, VISIBLE "X NOT EQUALS Y"
              OIC

              DIFFRINT x AN 42, O RLY?
                YA RLY, VISIBLE "X IS NOT 42"
                NO WAI, VISIBLE "X IS 42"
              OIC

              BTW multiple statements on same line
              I HAS A flag ITZ WIN
              flag, O RLY?, YA RLY, VISIBLE "FLAG IS TRUE", NO WAI, VISIBLE "FLAG IS FALSE", OIC
            KTHXBYE
            """, "X EQUALS Y\nX IS NOT 42\nFLAG IS TRUE");
    }

    [Fact]
    public void ExpressionBeforeOrly()
    {
        AssertOutput("""
            BTW Test expression before O RLY? sets IT, then conditional reads it
            BTW Verify IT persists across statements and O RLY? uses current value

            HAI 1.2
              BTW expression sets IT, next statement reads it
              SUM OF 3 AN 7
              O RLY?
                YA RLY
                  VISIBLE "10 IS TRUTHY"
                NO WAI
                  VISIBLE "10 IS FALSY"
              OIC

              BTW another expression overwrites IT
              DIFF OF 5 AN 5
              O RLY?
                YA RLY
                  VISIBLE "0 IS TRUTHY"
                NO WAI
                  VISIBLE "0 IS FALSY"
              OIC

              BTW assignment doesn't affect IT
              I HAS A x ITZ 99
              x R 100
              BTW IT should still be 0 from above
              O RLY?
                YA RLY
                  VISIBLE "STILL TRUTHY"
                NO WAI
                  VISIBLE "STILL FALSY"
              OIC

              BTW new expression sets IT again
              BOTH SAEM 1 AN 1
              O RLY?
                YA RLY
                  VISIBLE "TRUE IS TRUTHY"
                NO WAI
                  VISIBLE "TRUE IS FALSY"
              OIC
            KTHXBYE
            """, "10 IS TRUTHY\n0 IS FALSY\nSTILL FALSY\nTRUE IS TRUTHY");
    }

    [Fact]
    public void IfOnly()
    {
        AssertOutput("""
            BTW Test O RLY? with only YA RLY branch (no NO WAI)
            BTW Should execute YA RLY when true, do nothing when false

            HAI 1.2
              BTW test true condition - should execute
              WIN
              O RLY?
                YA RLY
                  VISIBLE "EXECUTED"
              OIC

              BTW test false condition - should do nothing
              FAIL
              O RLY?
                YA RLY
                  VISIBLE "NOT EXECUTED"
              OIC

              VISIBLE "DONE"
            KTHXBYE
            """, "EXECUTED\nDONE");
    }

    [Fact]
    public void ItTruthiness()
    {
        AssertOutput("""
            BTW Test O RLY? truthiness evaluation of IT
            BTW Per spec: 0=FAIL, ""=FAIL, NOOB=FAIL, 1=WIN, "a"=WIN

            HAI 1.2
              BTW test NUMBR 0 (should be FAIL)
              0
              O RLY?
                YA RLY
                  VISIBLE "0 IS TRUTHY"
                NO WAI
                  VISIBLE "0 IS FALSY"
              OIC

              BTW test empty string (should be FAIL)
              ""
              O RLY?
                YA RLY
                  VISIBLE "EMPTY STRING IS TRUTHY"
                NO WAI
                  VISIBLE "EMPTY STRING IS FALSY"
              OIC

              BTW test NOOB (should be FAIL)
              I HAS A null_var
              null_var
              O RLY?
                YA RLY
                  VISIBLE "NOOB IS TRUTHY"
                NO WAI
                  VISIBLE "NOOB IS FALSY"
              OIC

              BTW test positive NUMBR (should be WIN)
              1
              O RLY?
                YA RLY
                  VISIBLE "1 IS TRUTHY"
                NO WAI
                  VISIBLE "1 IS FALSY"
              OIC

              BTW test non-empty string (should be WIN)
              "a"
              O RLY?
                YA RLY
                  VISIBLE "NON-EMPTY STRING IS TRUTHY"
                NO WAI
                  VISIBLE "NON-EMPTY STRING IS FALSY"
              OIC
            KTHXBYE
            """, "0 IS FALSY\nEMPTY STRING IS FALSY\nNOOB IS FALSY\n1 IS TRUTHY\nNON-EMPTY STRING IS TRUTHY");
    }

    [Fact]
    public void Mebbe()
    {
        AssertOutput("""
            BTW Test multiple MEBBE (else-if) chains
            BTW MEBBE expressions are evaluated in order until one is WIN

            HAI 1.2
              BTW test first MEBBE case
              I HAS A val ITZ 1
              val
              O RLY?
                YA RLY
                  VISIBLE "FIRST"
                MEBBE BOTH SAEM val AN 1
                  VISIBLE "MEBBE 1"
                MEBBE BOTH SAEM val AN 2
                  VISIBLE "MEBBE 2"
                NO WAI
                  VISIBLE "NONE"
              OIC

              BTW test second MEBBE case
              I HAS A val2 ITZ 2
              FAIL
              O RLY?
                YA RLY
                  VISIBLE "FIRST"
                MEBBE BOTH SAEM val2 AN 1
                  VISIBLE "MEBBE 1"
                MEBBE BOTH SAEM val2 AN 2
                  VISIBLE "MEBBE 2"
                NO WAI
                  VISIBLE "NONE"
              OIC

              BTW test NO WAI fallback
              I HAS A val3 ITZ 99
              FAIL
              O RLY?
                YA RLY
                  VISIBLE "FIRST"
                MEBBE BOTH SAEM val3 AN 1
                  VISIBLE "MEBBE 1"
                MEBBE BOTH SAEM val3 AN 2
                  VISIBLE "MEBBE 2"
                NO WAI
                  VISIBLE "NONE"
              OIC
            KTHXBYE
            """, "FIRST\nMEBBE 2\nNONE");
    }

    [Fact]
    public void NestedConditionals()
    {
        AssertOutput("""
            BTW Test nested O RLY? conditionals
            BTW Verify inner conditionals work correctly within outer ones

            HAI 1.2
              I HAS A x ITZ 5
              I HAS A y ITZ 10

              BOTH SAEM BIGGR OF x AN 3 AN x
              O RLY?
                YA RLY
                  VISIBLE "OUTER:: X >= 3"
                  BOTH SAEM SMALLR OF y AN 15 AN y
                  O RLY?
                    YA RLY
                      VISIBLE "  INNER:: Y <= 15"
                      BOTH SAEM x AN 5
                      O RLY?
                        YA RLY
                          VISIBLE "    INNERMOST:: X == 5"
                        NO WAI
                          VISIBLE "    INNERMOST:: X != 5"
                      OIC
                    NO WAI
                      VISIBLE "  INNER:: Y > 15"
                  OIC
                NO WAI
                  VISIBLE "OUTER:: X < 3"
              OIC
            KTHXBYE
            """, "OUTER: X >= 3\n  INNER: Y <= 15\n    INNERMOST: X == 5");
    }
}
