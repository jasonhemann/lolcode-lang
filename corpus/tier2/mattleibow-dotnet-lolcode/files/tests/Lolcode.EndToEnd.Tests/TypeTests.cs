namespace Lolcode.EndToEnd.Tests;

public class TypeTests : EndToEndTestBase
{
    [Fact]
    public void Noob()
    {
        AssertOutput("""
            BTW Test NOOB (untyped/null) behavior
            BTW Per spec: NOOB only implicit cast to TROOF = FAIL
            BTW Per spec: explicit cast to NUMBR=0, NUMBAR=0.0, YARN=""

            HAI 1.2
              BTW uninitialized is NOOB
              I HAS A noob_var

              BTW NOOB printed is empty string (cast to YARN)
              VISIBLE "BEFORE"
              VISIBLE noob_var
              VISIBLE "AFTER"

              BTW NOOB is falsy
              noob_var
              O RLY?
                YA RLY
                  VISIBLE "NOOB IS TRUTHY"
                NO WAI
                  VISIBLE "NOOB IS FALSY"
              OIC

              BTW explicit cast NOOB to TROOF
              I HAS A noob2
              VISIBLE MAEK noob2 A TROOF

              BTW explicit cast NOOB to NUMBR
              I HAS A noob3
              VISIBLE MAEK noob3 A NUMBR

              BTW explicit cast NOOB to NUMBAR
              I HAS A noob4
              VISIBLE MAEK noob4 A NUMBAR

              BTW explicit cast NOOB to YARN
              I HAS A noob5
              VISIBLE "YARN::"
              VISIBLE MAEK noob5 A YARN
              VISIBLE "::END"

              BTW NOOB in boolean expression (implicitly cast to FAIL)
              I HAS A noob6
              VISIBLE NOT noob6
              VISIBLE EITHER OF noob6 AN WIN
            KTHXBYE
            """, "BEFORE\n\nAFTER\nNOOB IS FALSY\nFAIL\n0\n0.00\nYARN:\n\n:END\nWIN\nWIN");
    }

    [Fact]
    public void Numbar()
    {
        AssertOutput("""
            BTW Test NUMBAR (float) type
            BTW Per spec: digits with exactly one decimal point, optional leading hyphen
            BTW Per spec: NUMBAR cast to YARN truncates to 2 decimal places

            HAI 1.2
              BTW positive floats
              I HAS A zero ITZ 0.0
              I HAS A one ITZ 1.0
              I HAS A pi ITZ 3.14159
              I HAS A small ITZ 0.001

              VISIBLE zero
              VISIBLE one
              VISIBLE pi
              VISIBLE small

              BTW negative floats
              I HAS A neg_one ITZ -1.0
              I HAS A neg_pi ITZ -3.14159

              VISIBLE neg_one
              VISIBLE neg_pi

              BTW floats with many decimals (output truncated to 2)
              I HAS A long_decimal ITZ 1.23456789
              VISIBLE long_decimal

              BTW float arithmetic
              I HAS A a ITZ 10.5
              I HAS A b ITZ 3.2

              VISIBLE SUM OF a AN b
              VISIBLE DIFF OF a AN b
              VISIBLE PRODUKT OF a AN b
              VISIBLE QUOSHUNT OF a AN b

              BTW mixed int/float (result is float)
              VISIBLE SUM OF 5 AN 2.5
              VISIBLE PRODUKT OF 3 AN 1.5

              BTW float min/max
              VISIBLE BIGGR OF 3.14 AN 2.71
              VISIBLE SMALLR OF 3.14 AN 2.71
            KTHXBYE
            """, "0.00\n1.00\n3.14\n0.00\n-1.00\n-3.14\n1.23\n13.70\n7.30\n33.60\n3.28\n7.50\n4.50\n3.14\n2.71");
    }

    [Fact]
    public void Numbr()
    {
        AssertOutput("""
            BTW Test NUMBR (integer) type
            BTW Per spec: contiguous digits without decimal, optional leading hyphen

            HAI 1.2
              BTW positive integers
              I HAS A zero ITZ 0
              I HAS A one ITZ 1
              I HAS A small ITZ 42
              I HAS A big ITZ 999999

              VISIBLE zero
              VISIBLE one
              VISIBLE small
              VISIBLE big

              BTW negative integers
              I HAS A neg_one ITZ -1
              I HAS A neg_big ITZ -12345

              VISIBLE neg_one
              VISIBLE neg_big

              BTW arithmetic with integers
              I HAS A a ITZ 10
              I HAS A b ITZ 3

              VISIBLE SUM OF a AN b
              VISIBLE DIFF OF a AN b
              VISIBLE PRODUKT OF a AN b
              VISIBLE QUOSHUNT OF a AN b
              VISIBLE MOD OF a AN b

              BTW integer division truncates
              VISIBLE QUOSHUNT OF 7 AN 2
              VISIBLE QUOSHUNT OF -7 AN 2

              BTW min/max with integers
              VISIBLE BIGGR OF 5 AN 10
              VISIBLE SMALLR OF 5 AN 10
              VISIBLE BIGGR OF -5 AN -10
              VISIBLE SMALLR OF -5 AN -10
            KTHXBYE
            """, "0\n1\n42\n999999\n-1\n-12345\n13\n7\n30\n3\n1\n3\n-3\n10\n5\n-5\n-10");
    }

    [Fact]
    public void Troof()
    {
        AssertOutput("""
            BTW Test TROOF (boolean) type
            BTW Per spec: WIN (true) and FAIL (false)

            HAI 1.2
              BTW boolean literals
              I HAS A yes ITZ WIN
              I HAS A no ITZ FAIL

              VISIBLE yes
              VISIBLE no

              BTW booleans in conditionals
              yes
              O RLY?
                YA RLY
                  VISIBLE "YES IS TRUTHY"
              OIC

              no
              O RLY?
                YA RLY
                  VISIBLE "NO IS TRUTHY"
                NO WAI
                  VISIBLE "NO IS FALSY"
              OIC

              BTW boolean operators
              VISIBLE BOTH OF WIN AN WIN
              VISIBLE BOTH OF WIN AN FAIL
              VISIBLE EITHER OF WIN AN FAIL
              VISIBLE EITHER OF FAIL AN FAIL
              VISIBLE WON OF WIN AN FAIL
              VISIBLE WON OF WIN AN WIN
              VISIBLE NOT WIN
              VISIBLE NOT FAIL

              BTW truthiness casting
              BTW empty string is FAIL
              ""
              O RLY?
                YA RLY, VISIBLE "EMPTY STRING TRUTHY"
                NO WAI, VISIBLE "EMPTY STRING FALSY"
              OIC

              BTW zero is FAIL
              0
              O RLY?
                YA RLY, VISIBLE "ZERO TRUTHY"
                NO WAI, VISIBLE "ZERO FALSY"
              OIC

              BTW 0.0 is FAIL
              0.0
              O RLY?
                YA RLY, VISIBLE "0.0 TRUTHY"
                NO WAI, VISIBLE "0.0 FALSY"
              OIC

              BTW non-empty string is WIN
              "HAI"
              O RLY?
                YA RLY, VISIBLE "NON-EMPTY STRING TRUTHY"
              OIC

              BTW non-zero is WIN
              42
              O RLY?
                YA RLY, VISIBLE "NON-ZERO TRUTHY"
              OIC

              BTW negative non-zero is WIN
              -1
              O RLY?
                YA RLY, VISIBLE "NEGATIVE TRUTHY"
              OIC
            KTHXBYE
            """, "WIN\nFAIL\nYES IS TRUTHY\nNO IS FALSY\nWIN\nFAIL\nWIN\nFAIL\nWIN\nFAIL\nFAIL\nWIN\nEMPTY STRING FALSY\nZERO FALSY\n0.0 FALSY\nNON-EMPTY STRING TRUTHY\nNON-ZERO TRUTHY\nNEGATIVE TRUTHY");
    }

    [Fact]
    public void Yarn()
    {
        AssertOutput("""
            BTW Test YARN (string) type
            BTW Per spec: demarked with double quotes, escape with colon

            HAI 1.2
              BTW basic strings
              I HAS A empty ITZ ""
              I HAS A hello ITZ "HELLO WORLD"

              VISIBLE "START"
              VISIBLE empty
              VISIBLE "END"
              VISIBLE hello

              BTW escape sequences
              VISIBLE "LINE1:)LINE2"
              VISIBLE "COL1:>COL2"
              VISIBLE "QUOTE:: :"HAI:""
              VISIBLE "COLON:: ::"
              VISIBLE "BELL:::o"

              BTW hex escape :(<hex>)
              VISIBLE "HEX A:: :(41)"
              VISIBLE "HEX NEWLINE:: :(0A)AFTER"

              BTW variable interpolation :{var}
              I HAS A name ITZ "CEILING CAT"
              I HAS A age ITZ 9
              VISIBLE "NAME:: :{name}"
              VISIBLE "AGE:: :{age}"
              VISIBLE ":{name} IS :{age} YEARS OLD"

              BTW string in string context
              I HAS A a ITZ "FIRST"
              I HAS A b ITZ "SECOND"
              VISIBLE SMOOSH a AN " AND " AN b MKAY

              BTW multiline via escape
              VISIBLE "LINE A:)LINE B:)LINE C"
            KTHXBYE
            """, "START\n\nEND\nHELLO WORLD\nLINE1\nLINE2\nCOL1\tCOL2\nQUOTE: \"HAI\"\nCOLON: :\nBELL:\a\nHEX A: A\nHEX NEWLINE: \nAFTER\nNAME: CEILING CAT\nAGE: 9\nCEILING CAT IS 9 YEARS OLD\nFIRST AND SECOND\nLINE A\nLINE B\nLINE C");
    }
}
