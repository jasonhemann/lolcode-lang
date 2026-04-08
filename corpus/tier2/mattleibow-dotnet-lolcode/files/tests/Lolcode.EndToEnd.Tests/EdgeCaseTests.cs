namespace Lolcode.EndToEnd.Tests;

public class EdgeCaseTests : EndToEndTestBase
{
    [Fact]
    public void AllFeatures()
    {
        AssertOutput("""
            HAI 1.2
              BTW Comprehensive test using all major LOLCODE features

              BTW Variables and types
              I HAS A num ITZ 42
              I HAS A str ITZ "CEILING CAT"
              I HAS A truth ITZ WIN

              BTW Functions
              HOW IZ I add YR a AN YR b
                FOUND YR SUM OF a AN b
              IF U SAY SO

              HOW IZ I greet YR name
                VISIBLE "OH HAI " name
              IF U SAY SO

              BTW Function calls
              I IZ greet YR str MKAY
              I HAS A sum ITZ I IZ add YR 10 AN YR 20 MKAY
              VISIBLE "Sum:: " sum

              BTW Math operations
              I HAS A result ITZ SUM OF num AN 8
              VISIBLE "42 + 8 = " result

              BTW Boolean logic
              I HAS A logic ITZ BOTH OF WIN AN truth
              VISIBLE "Both WIN:: " logic

              BTW Comparison
              BOTH SAEM result AN 50
              O RLY?
                YA RLY
                  VISIBLE "Result is 50!"
                NO WAI
                  VISIBLE "Result is not 50"
              OIC

              BTW Switch statement
              "red"
              WTF?
                OMG "red"
                  VISIBLE "Color is red"
                  GTFO
                OMG "blue"
                  VISIBLE "Color is blue"
                  GTFO
                OMGWTF
                  VISIBLE "Unknown color"
              OIC

              BTW Loop
              IM IN YR loop UPPIN YR i TIL BOTH SAEM i AN 3
                VISIBLE "Loop:: " i
              IM OUTTA YR loop

              BTW Casting
              I HAS A numStr ITZ "123"
              numStr IS NOW A NUMBR
              I HAS A doubled ITZ PRODUKT OF numStr AN 2
              VISIBLE "Doubled:: " doubled

              BTW Expression statement and IT
              DIFF OF 100 AN 50
              VISIBLE "IT is:: " IT

              VISIBLE "ALL DONE!"
            KTHXBYE
            """, "OH HAI CEILING CAT\nSum: 30\n42 + 8 = 50\nBoth WIN: WIN\nResult is 50!\nColor is red\nLoop: 0\nLoop: 1\nLoop: 2\nDoubled: 246\nIT is: 50\nALL DONE!");
    }

    [Fact]
    public void DeeplyNested()
    {
        AssertOutput("""
            HAI 1.2
              BTW Test deeply nested conditionals and loops

              I HAS A x ITZ 5

              BOTH SAEM x AN 5
              O RLY?
                YA RLY
                  VISIBLE "Outer:: x is 5"

                  IM IN YR outer UPPIN YR i TIL BOTH SAEM i AN 2
                    VISIBLE "Outer loop:: " i

                    BOTH SAEM i AN 1
                    O RLY?
                      YA RLY
                        VISIBLE "Inner:: i is 1"

                        IM IN YR inner UPPIN YR j TIL BOTH SAEM j AN 2
                          VISIBLE "Inner loop:: " j

                          BOTH SAEM j AN 1
                          O RLY?
                            YA RLY
                              VISIBLE "Deepest:: j is 1"
                          OIC
                        IM OUTTA YR inner
                    OIC
                  IM OUTTA YR outer
              OIC

              VISIBLE "Done!"
            KTHXBYE
            """, "Outer: x is 5\nOuter loop: 0\nOuter loop: 1\nInner: i is 1\nInner loop: 0\nInner loop: 1\nDeepest: j is 1\nDone!");
    }

    [Fact]
    public void EmptyProgram()
    {
        AssertOutput("""
            HAI 1.2
            KTHXBYE
            """, "");
    }

    [Fact]
    public void FunctionAndLoop()
    {
        AssertOutput("""
            HAI 1.2
              BTW Test function called from within a loop

              HOW IZ I square YR n
                FOUND YR PRODUKT OF n AN n
              IF U SAY SO

              IM IN YR loop UPPIN YR i TIL BOTH SAEM i AN 5
                I HAS A squared ITZ I IZ square YR i MKAY
                VISIBLE i " squared is " squared
              IM OUTTA YR loop
            KTHXBYE
            """, "0 squared is 0\n1 squared is 1\n2 squared is 4\n3 squared is 9\n4 squared is 16");
    }

    [Fact]
    public void ItAcrossControlFlow()
    {
        AssertOutput("""
            HAI 1.2
              BTW Test IT behavior across control flow structures

              100
              VISIBLE "Initial IT:: " IT

              BTW IT in if/else
              BOTH SAEM 5 AN 5
              O RLY?
                YA RLY
                  200
                  VISIBLE "IT in YA RLY:: " IT
                NO WAI
                  300
                  VISIBLE "IT in NO WAI:: " IT
              OIC

              VISIBLE "IT after O RLY?:: " IT

              BTW IT in loop
              IM IN YR loop UPPIN YR i TIL BOTH SAEM i AN 2
                SUM OF i AN 1000
                VISIBLE "IT in loop:: " IT
              IM OUTTA YR loop

              VISIBLE "IT after loop:: " IT

              BTW IT in switch
              "apple"
              WTF?
                OMG "apple"
                  777
                  VISIBLE "IT in OMG:: " IT
                  GTFO
                OMGWTF
                  888
                  VISIBLE "IT in OMGWTF:: " IT
              OIC

              VISIBLE "Final IT:: " IT
            KTHXBYE
            """, "Initial IT: 100\nIT in YA RLY: 200\nIT after O RLY?: 200\nIT in loop: 1000\nIT in loop: 1001\nIT after loop: 1001\nIT in OMG: 777\nFinal IT: 777");
    }

    [Fact]
    public void VariableNameLikeKeyword()
    {
        AssertOutput("""
            HAI 1.2
              BTW Test variables with names similar to keywords

              I HAS A SUMMER ITZ 100
              I HAS A NOTIFY ITZ "message"
              I HAS A TRUFFLE ITZ WIN
              I HAS A WINNER ITZ "you"
              I HAS A YARN_VALUE ITZ "string"

              VISIBLE SUMMER
              VISIBLE NOTIFY
              VISIBLE TRUFFLE
              VISIBLE WINNER
              VISIBLE YARN_VALUE

              I HAS A result ITZ SUM OF SUMMER AN 50
              VISIBLE result
            KTHXBYE
            """, "100\nmessage\nWIN\nyou\nstring\n150");
    }

    [Fact]
    public void MultipleVisibleOnSameLine()
    {
        AssertOutput("""
            HAI 1.2
              VISIBLE "A", VISIBLE "B"
            KTHXBYE
            """, "A\nB");
    }
}
