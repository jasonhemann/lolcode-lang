namespace Lolcode.EndToEnd.Tests;

public class ExpressionTests : EndToEndTestBase
{
    [Fact]
    public void AssignmentNoIt()
    {
        AssertOutput("""
            HAI 1.2
              BTW Test that assignment does NOT update IT

              SUM OF 5 AN 5
              BTW IT is now 10

              I HAS A x ITZ 100
              BTW IT should still be 10

              VISIBLE IT

              x R 200
              BTW IT should still be 10

              VISIBLE IT
            KTHXBYE
            """, "10\n10");
    }

    [Fact]
    public void ChainedExpressions()
    {
        AssertOutput("""
            HAI 1.2
              BTW Test multiple bare expressions, IT changes each time

              100
              VISIBLE "First:: " IT

              200
              VISIBLE "Second:: " IT

              SUM OF IT AN 50
              VISIBLE "Third:: " IT

              PRODUKT OF IT AN 2
              VISIBLE "Fourth:: " IT
            KTHXBYE
            """, "First: 100\nSecond: 200\nThird: 250\nFourth: 500");
    }

    [Fact]
    public void DeclarationNoIt()
    {
        AssertOutput("""
            HAI 1.2
              BTW Test that declaration with initialization does NOT update IT

              SUM OF 7 AN 8
              BTW IT is now 15

              I HAS A x ITZ SUM OF 100 AN 200
              BTW IT should still be 15

              VISIBLE IT
            KTHXBYE
            """, "15");
    }

    [Fact]
    public void ExpressionSetsIt()
    {
        AssertOutput("""
            HAI 1.2
              BTW Test that bare expressions set IT

              SUM OF 3 AN 5
              VISIBLE IT

              PRODUKT OF 4 AN 10
              VISIBLE IT

              BOTH SAEM 5 AN 5
              VISIBLE IT
            KTHXBYE
            """, "8\n40\nWIN");
    }

    [Fact]
    public void ItInVisible()
    {
        AssertOutput("""
            HAI 1.2
              BTW Test VISIBLE IT prints the current implicit value

              I HAS A x ITZ 42
              x
              VISIBLE "IT is:: " IT

              SUM OF 10 AN 20
              VISIBLE "IT is now:: " IT
            KTHXBYE
            """, "IT is: 42\nIT is now: 30");
    }

    [Fact]
    public void ItPersists()
    {
        AssertOutput("""
            HAI 1.2
              BTW Test that IT persists until next bare expression

              SUM OF 10 AN 20
              VISIBLE IT
              VISIBLE IT
              VISIBLE IT

              DIFF OF 50 AN 10
              VISIBLE IT
              VISIBLE IT
            KTHXBYE
            """, "30\n30\n30\n40\n40");
    }

    [Fact]
    public void ItUsedByOrly()
    {
        AssertOutput("""
            HAI 1.2
              BTW Test that O RLY? reads IT

              SUM OF 2 AN 3
              O RLY?
                YA RLY
                  VISIBLE "5 is truthy"
              OIC

              DIFF OF 1 AN 1
              O RLY?
                YA RLY
                  VISIBLE "0 is truthy"
                NO WAI
                  VISIBLE "0 is falsy"
              OIC
            KTHXBYE
            """, "5 is truthy\n0 is falsy");
    }

    [Fact]
    public void ItUsedByWtf()
    {
        AssertOutput("""
            HAI 1.2
              BTW Test that WTF? reads IT

              "apple"
              WTF?
                OMG "apple"
                  VISIBLE "Got apple"
                  GTFO
                OMG "banana"
                  VISIBLE "Got banana"
                  GTFO
                OMGWTF
                  VISIBLE "Got something else"
              OIC

              42
              WTF?
                OMG 42
                  VISIBLE "The answer"
                  GTFO
                OMGWTF
                  VISIBLE "Not the answer"
              OIC
            KTHXBYE
            """, "Got apple\nThe answer");
    }
}
