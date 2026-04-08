namespace Lolcode.EndToEnd.Tests;

public class SwitchTests : EndToEndTestBase
{
    [Fact]
    public void BasicSwitch()
    {
        AssertOutput("""
            BTW Test basic WTF? switch with OMG literal cases and GTFO
            BTW Simple switch that matches cases and breaks properly

            HAI 1.2
              BTW test NUMBR matching
              I HAS A day ITZ 3
              day
              WTF?
                OMG 1
                  VISIBLE "MONDAY"
                  GTFO
                OMG 2
                  VISIBLE "TUESDAY"
                  GTFO
                OMG 3
                  VISIBLE "WEDNESDAY"
                  GTFO
                OMG 4
                  VISIBLE "THURSDAY"
                  GTFO
                OMGWTF
                  VISIBLE "OTHER DAY"
              OIC

              BTW test YARN matching
              I HAS A grade ITZ "A"
              grade
              WTF?
                OMG "A"
                  VISIBLE "EXCELLENT"
                  GTFO
                OMG "B"
                  VISIBLE "GOOD"
                  GTFO
                OMG "C"
                  VISIBLE "OKAY"
                  GTFO
                OMGWTF
                  VISIBLE "NEEDS IMPROVEMENT"
              OIC
            KTHXBYE
            """, "WEDNESDAY\nEXCELLENT");
    }

    [Fact]
    public void SwitchDefault()
    {
        AssertOutput("""
            BTW Test OMGWTF default case when no OMG matches
            BTW OMGWTF executes when IT doesn't match any OMG literal

            HAI 1.2
              BTW test default case execution
              I HAS A unknown ITZ 99
              unknown
              WTF?
                OMG 1
                  VISIBLE "ONE"
                  GTFO
                OMG 2
                  VISIBLE "TWO"
                  GTFO
                OMG 3
                  VISIBLE "THREE"
                  GTFO
                OMGWTF
                  VISIBLE "DEFAULT CASE"
              OIC

              BTW test with matching case (default should not execute)
              I HAS A known ITZ 2
              known
              WTF?
                OMG 1
                  VISIBLE "ONE"
                  GTFO
                OMG 2
                  VISIBLE "TWO"
                  GTFO
                OMGWTF
                  VISIBLE "DEFAULT NOT REACHED"
              OIC
            KTHXBYE
            """, "DEFAULT CASE\nTWO");
    }

    [Fact]
    public void SwitchFallthrough()
    {
        AssertOutput("""
            BTW Test switch fallthrough when OMG case has no GTFO
            BTW Without GTFO, execution continues to next OMG case

            HAI 1.2
              I HAS A val ITZ 2
              val
              WTF?
                OMG 1
                  VISIBLE "CASE 1"
                OMG 2
                  VISIBLE "CASE 2"
                  BTW no GTFO here - should fall through
                OMG 3
                  VISIBLE "CASE 3"
                  GTFO
                OMG 4
                  VISIBLE "CASE 4"
              OIC

              VISIBLE "AFTER SWITCH"
            KTHXBYE
            """, "CASE 2\nCASE 3\nAFTER SWITCH");
    }

    [Fact]
    public void SwitchGtfoStopsFallthrough()
    {
        AssertOutput("""
            BTW Test GTFO stops fall-through at precise location
            BTW GTFO should break out immediately, preventing further case execution

            HAI 1.2
              I HAS A test ITZ 2
              test
              WTF?
                OMG 1
                  VISIBLE "CASE 1"
                  BTW no GTFO - would fall through
                OMG 2
                  VISIBLE "CASE 2"
                  BTW no GTFO - would fall through
                OMG 3
                  VISIBLE "CASE 3"
                  GTFO  BTW this stops the fall-through
                OMG 4
                  VISIBLE "CASE 4 - SHOULD NOT EXECUTE"
                OMG 5
                  VISIBLE "CASE 5 - SHOULD NOT EXECUTE"
              OIC

              VISIBLE "AFTER SWITCH"
            KTHXBYE
            """, "CASE 2\nCASE 3\nAFTER SWITCH");
    }

    [Fact]
    public void SwitchMultipleFallthrough()
    {
        AssertOutput("""
            BTW Test cascading fall-through across multiple OMG blocks
            BTW No GTFO causes execution to continue through 3+ cases

            HAI 1.2
              I HAS A cascade ITZ 1
              cascade
              WTF?
                OMG 1
                  VISIBLE "CASE 1"
                  BTW no GTFO - falls through
                OMG 2
                  VISIBLE "CASE 2"
                  BTW no GTFO - falls through
                OMG 3
                  VISIBLE "CASE 3"
                  BTW no GTFO - falls through
                OMG 4
                  VISIBLE "CASE 4"
                  GTFO
                OMG 5
                  VISIBLE "CASE 5"
              OIC

              VISIBLE "DONE"
            KTHXBYE
            """, "CASE 1\nCASE 2\nCASE 3\nCASE 4\nDONE");
    }

    [Fact]
    public void SwitchNoMatch()
    {
        AssertOutput("""
            BTW Test WTF? where no OMG matches and no OMGWTF (does nothing)
            BTW Should execute no cases when no match and no default

            HAI 1.2
              VISIBLE "BEFORE SWITCH"

              I HAS A mystery ITZ 42
              mystery
              WTF?
                OMG 1
                  VISIBLE "NOT THIS ONE"
                  GTFO
                OMG 2
                  VISIBLE "NOT THIS EITHER"
                  GTFO
                OMG 3
                  VISIBLE "NOPE"
                  GTFO
                BTW no OMGWTF default case
              OIC

              VISIBLE "AFTER SWITCH"
            KTHXBYE
            """, "BEFORE SWITCH\nAFTER SWITCH");
    }

    [Fact]
    public void SwitchNumbr()
    {
        AssertOutput("""
            BTW Test WTF? switch with NUMBR integer literals
            BTW Verify integer matching works correctly

            HAI 1.2
              I HAS A score ITZ 85
              score
              WTF?
                OMG 100
                  VISIBLE "PERFECT SCORE"
                  GTFO
                OMG 90
                  VISIBLE "A GRADE"
                  GTFO
                OMG 85
                  VISIBLE "HIGH B GRADE"
                  GTFO
                OMG 80
                  VISIBLE "LOW B GRADE"
                  GTFO
                OMG 70
                  VISIBLE "C GRADE"
                  GTFO
                OMGWTF
                  VISIBLE "OTHER GRADE"
              OIC

              BTW test with negative number
              I HAS A temp ITZ -5
              temp
              WTF?
                OMG 0
                  VISIBLE "FREEZING"
                  GTFO
                OMG -5
                  VISIBLE "VERY COLD"
                  GTFO
                OMG -10
                  VISIBLE "EXTREMELY COLD"
                  GTFO
                OMGWTF
                  VISIBLE "UNKNOWN TEMPERATURE"
              OIC
            KTHXBYE
            """, "HIGH B GRADE\nVERY COLD");
    }

    [Fact]
    public void SwitchString()
    {
        AssertOutput("""
            BTW Test WTF? switch with YARN string literals
            BTW Verify string matching works correctly

            HAI 1.2
              I HAS A color ITZ "red"
              color
              WTF?
                OMG "red"
                  VISIBLE "ROSES"
                  GTFO
                OMG "blue"
                  VISIBLE "VIOLETS"
                  GTFO
                OMG "green"
                  VISIBLE "GRASS"
                  GTFO
                OMG "yellow"
                  VISIBLE "BANANAS"
                  GTFO
                OMGWTF
                  VISIBLE "UNKNOWN COLOR"
              OIC

              BTW test with different string
              I HAS A fruit ITZ "apple"
              fruit
              WTF?
                OMG "banana"
                  VISIBLE "YELLOW FRUIT"
                  GTFO
                OMG "apple"
                  VISIBLE "RED OR GREEN FRUIT"
                  GTFO
                OMG "orange"
                  VISIBLE "ORANGE FRUIT"
                  GTFO
                OMGWTF
                  VISIBLE "UNKNOWN FRUIT"
              OIC
            KTHXBYE
            """, "ROSES\nRED OR GREEN FRUIT");
    }
}
