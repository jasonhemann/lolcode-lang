namespace Lolcode.EndToEnd.Tests;

public class StringTests : EndToEndTestBase
{
    [Fact]
    public void EmptyString()
    {
        AssertOutput("""
            BTW Test empty string behavior: value, truthiness (FAIL), concatenation
            BTW Per spec: empty YARN is falsy and concatenates as empty text

            HAI 1.2
              I HAS A empty ITZ ""
              I HAS A nonempty ITZ "LOL"

              BTW show empty string in brackets
              VISIBLE "EMPTY::[" empty "]"
              VISIBLE "NONEMPTY::[" nonempty "]"

              BTW empty string is falsy in O RLY?
              empty
              O RLY?
                YA RLY
                  VISIBLE "SHOULD NOT SEE"
                NO WAI
                  VISIBLE "EMPTY IS FAIL"
              OIC

              BTW casting empty and non-empty YARN to TROOF
              VISIBLE "MAEK :":" A TROOF:: " MAEK empty A TROOF
              VISIBLE "MAEK :"LOL:" A TROOF:: " MAEK nonempty A TROOF

              BTW concatenating with empty string
              I HAS A base ITZ ""
              I HAS A joined ITZ SMOOSH base AN "A" MKAY
              VISIBLE joined
            KTHXBYE
            """, "EMPTY:[]\nNONEMPTY:[LOL]\nEMPTY IS FAIL\nMAEK \"\" A TROOF: FAIL\nMAEK \"LOL\" A TROOF: WIN\nA");
    }

    [Fact]
    public void EscapeSequences()
    {
        AssertOutput("""
            BTW Test basic string escape sequences (:), :>, ::, :", :o
            BTW Per spec: colon introduces escape sequences and unicode/interpolation forms

            HAI 1.2
              BTW newline escape :)
              VISIBLE "LINE1:)LINE2"

              BTW tab escape :>
              VISIBLE "COL1:>COL2"

              BTW colon escape ::
              VISIBLE "A::B"

              BTW quote escape :"
              VISIBLE "SHE SED :"OH RLY?:""

              BTW bell escape :o (prints something before and after bell)
              VISIBLE "BELL-START:oBELL-END"
            KTHXBYE
            """, "LINE1\nLINE2\nCOL1\tCOL2\nA:B\nSHE SED \"OH RLY?\"\nBELL-START\aBELL-END");
    }

    [Fact]
    public void Interpolation()
    {
        AssertOutput("""
            BTW Test string interpolation with :{var} for NUMBR, YARN, and TROOF
            BTW Per spec: :{var} inserts the current value of the variable cast to YARN

            HAI 1.2
              I HAS A count ITZ 42
              I HAS A name ITZ "KITTEH"
              I HAS A truth ITZ WIN

              VISIBLE "COUNT:: :{count}"
              VISIBLE "NAME:: :{name}"
              VISIBLE "TROOF:: :{truth}"

              BTW change variable values and ensure interpolation uses updated values
              count R 7
              name R "CEILING CAT"
              truth R FAIL

              VISIBLE "UPDATED COUNT:: :{count}"
              VISIBLE "UPDATED NAME:: :{name}"
              VISIBLE "UPDATED TROOF:: :{truth}"
            KTHXBYE
            """, "COUNT: 42\nNAME: KITTEH\nTROOF: WIN\nUPDATED COUNT: 7\nUPDATED NAME: CEILING CAT\nUPDATED TROOF: FAIL");
    }

    [Fact]
    public void Smoosh()
    {
        AssertOutput("""
            BTW Test SMOOSH concatenation, AN separator, MKAY, implicit YARN casts
            BTW Per spec: SMOOSH has infinite arity, MKAY may be omitted at end of line

            HAI 1.2
              BTW basic SMOOSH with explicit MKAY
              I HAS A result1 ITZ SMOOSH "HAI" AN " " AN "WORLD" MKAY
              VISIBLE result1

              BTW SMOOSH with MKAY omitted at end of line
              I HAS A result2 ITZ SMOOSH "OMITTED" AN " MKAY"
              VISIBLE result2

              BTW SMOOSH with NUMBR, NUMBAR, and TROOF (implicit YARN casts)
              I HAS A num ITZ 42
              I HAS A pi ITZ 3.14159
              I HAS A flag ITZ WIN
              I HAS A result3 ITZ SMOOSH "NUM=" AN num AN ", PI=" AN pi AN ", FLAG=" AN flag MKAY
              VISIBLE result3

              BTW SMOOSH used directly in VISIBLE
              VISIBLE SMOOSH "DIRECT " AN "VISIBLE" MKAY
            KTHXBYE
            """, "HAI WORLD\nOMITTED MKAY\nNUM=42, PI=3.14, FLAG=WIN\nDIRECT VISIBLE");
    }

    [Fact]
    public void SmooshNested()
    {
        AssertOutput("""
            BTW Test nested SMOOSH expressions and SMOOSH with inner expressions
            BTW Per spec: SMOOSH may contain other expressions including nested SMOOSH and math

            HAI 1.2
              BTW nested SMOOSH inside SMOOSH
              I HAS A inner ITZ SMOOSH "INNER" AN " SMOOSH" MKAY
              I HAS A outer ITZ SMOOSH "OUTER(" AN inner AN ")" MKAY
              VISIBLE outer

              BTW SMOOSH containing math expression results
              I HAS A a ITZ 2
              I HAS A b ITZ 3
              VISIBLE SMOOSH "SUM=" AN SUM OF a AN b AN ", PROD=" AN PRODUKT OF a AN b MKAY

              BTW deeply nested SMOOSH calls
              VISIBLE SMOOSH "NEST-" AN SMOOSH "LEVEL-" AN SMOOSH "3" MKAY MKAY MKAY
            KTHXBYE
            """, "OUTER(INNER SMOOSH)\nSUM=5, PROD=6\nNEST-LEVEL-3");
    }

    [Fact]
    public void UnicodeHexEscapeAscii()
    {
        AssertOutput("""
            HAI 1.2
              BTW simple ASCII using :(41)
              VISIBLE "HEX 41:: :(41)"

              BTW multiple escapes in one string
              VISIBLE "MIXED:: :(41):(42):(43)"
            KTHXBYE
            """, "HEX 41: A\nMIXED: ABC");
    }

    [Fact]
    public void UnicodeHexEscapeNonAscii()
    {
        // Non-ASCII Unicode characters may not round-trip through Windows console encoding
        if (OperatingSystem.IsWindows())
            return;

        AssertOutput("""
            HAI 1.2
              BTW non-ASCII BMP character (SMILING FACE)
              VISIBLE "SMILE:: :(263A)"

              BTW higher code point (GRINNING FACE)
              VISIBLE "GRIN:: :(1F600)"
            KTHXBYE
            """, "SMILE: ☺\nGRIN: 😀");
    }

    [Fact]
    public void SmooshConcatenationInAssignment()
    {
        AssertOutput("""
            HAI 1.2
              I HAS A x ITZ SMOOSH "HAI " AN "WORLD" MKAY
              VISIBLE x
            KTHXBYE
            """, "HAI WORLD");
    }
}
