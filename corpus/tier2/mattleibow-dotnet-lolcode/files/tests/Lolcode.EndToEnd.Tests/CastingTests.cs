namespace Lolcode.EndToEnd.Tests;

public class CastingTests : EndToEndTestBase
{
    [Fact]
    public void CastingRulesMatrix()
    {
        AssertOutput("""
            BTW Comprehensive casting matrix tests for LANGUAGE_SPEC Casting Rules Summary
            BTW Per spec: verify each From -> To case with representative values

            HAI 1.2
              BTW NUMBR -> YARN
              VISIBLE "NUMBR->YARN:: " MAEK 42 A YARN

              BTW NUMBAR -> YARN (2 decimal places)
              I HAS A numbar ITZ 3.14159
              VISIBLE "NUMBAR->YARN:: " MAEK numbar A YARN

              BTW TROOF -> YARN
              VISIBLE "TROOF WIN->YARN:: " MAEK WIN A YARN
              VISIBLE "TROOF FAIL->YARN:: " MAEK FAIL A YARN

              BTW YARN -> NUMBR
              VISIBLE "YARN :"123:"->NUMBR:: " MAEK "123" A NUMBR
              VISIBLE "YARN :"4.56:"->NUMBR:: " MAEK "4.56" A NUMBR

              BTW YARN -> NUMBAR
              VISIBLE "YARN :"4.56:"->NUMBAR:: " MAEK "4.56" A NUMBAR

              BTW YARN -> TROOF
              VISIBLE "YARN :":"->TROOF:: " MAEK "" A TROOF
              VISIBLE "YARN :"LOL:"->TROOF:: " MAEK "LOL" A TROOF

              BTW NUMBR -> TROOF
              VISIBLE "NUMBR 0->TROOF:: " MAEK 0 A TROOF
              VISIBLE "NUMBR 5->TROOF:: " MAEK 5 A TROOF

              BTW NUMBAR -> TROOF
              I HAS A zeroNumbar ITZ 0.0
              I HAS A nonzeroNumbar ITZ -1.5
              VISIBLE "NUMBAR 0.0->TROOF:: " MAEK zeroNumbar A TROOF
              VISIBLE "NUMBAR -1.5->TROOF:: " MAEK nonzeroNumbar A TROOF

              BTW TROOF -> NUMBR
              VISIBLE "TROOF WIN->NUMBR:: " MAEK WIN A NUMBR
              VISIBLE "TROOF FAIL->NUMBR:: " MAEK FAIL A NUMBR

              BTW TROOF -> NUMBAR
              VISIBLE "TROOF WIN->NUMBAR:: " MAEK WIN A NUMBAR
              VISIBLE "TROOF FAIL->NUMBAR:: " MAEK FAIL A NUMBAR

              BTW NOOB -> TROOF (implicit and explicit)
              I HAS A nothing ITZ NOOB
              VISIBLE "NOOB->TROOF (explicit):: " MAEK nothing A TROOF
              nothing
              O RLY?
                YA RLY
                  VISIBLE "NOOB->TROOF (implicit in O RLY?):: WIN BRANCH"
                NO WAI
                  VISIBLE "NOOB->TROOF (implicit in O RLY?):: FAIL BRANCH"
              OIC

              BTW NOOB -> other (explicit)
              VISIBLE "NOOB->NUMBR:: " MAEK nothing A NUMBR
              VISIBLE "NOOB->NUMBAR:: " MAEK nothing A NUMBAR
              VISIBLE "NOOB->YARN:: [" MAEK nothing A YARN "]"
            KTHXBYE
            """, "NUMBR->YARN: 42\nNUMBAR->YARN: 3.14\nTROOF WIN->YARN: WIN\nTROOF FAIL->YARN: FAIL\nYARN \"123\"->NUMBR: 123\nYARN \"4.56\"->NUMBR: 4\nYARN \"4.56\"->NUMBAR: 4.56\nYARN \"\"->TROOF: FAIL\nYARN \"LOL\"->TROOF: WIN\nNUMBR 0->TROOF: FAIL\nNUMBR 5->TROOF: WIN\nNUMBAR 0.0->TROOF: FAIL\nNUMBAR -1.5->TROOF: WIN\nTROOF WIN->NUMBR: 1\nTROOF FAIL->NUMBR: 0\nTROOF WIN->NUMBAR: 1.00\nTROOF FAIL->NUMBAR: 0.00\nNOOB->TROOF (explicit): FAIL\nNOOB->TROOF (implicit in O RLY?): FAIL BRANCH\nNOOB->NUMBR: 0\nNOOB->NUMBAR: 0.00\nNOOB->YARN: []");
    }

    [Fact]
    public void IsNowA()
    {
        AssertOutput("""
            BTW Test in-place casting with IS NOW A
            BTW Per spec: IS NOW A mutates the variable's runtime type

            HAI 1.2
              I HAS A val ITZ "42"
              VISIBLE "START YARN:: " val

              val IS NOW A NUMBR
              VISIBLE "AFTER IS NOW A NUMBR:: " val

              val IS NOW A NUMBAR
              VISIBLE "AFTER IS NOW A NUMBAR:: " val

              val IS NOW A YARN
              VISIBLE "AFTER IS NOW A YARN:: " val

              I HAS A flag ITZ 0
              flag IS NOW A TROOF
              VISIBLE "0 IS NOW A TROOF:: " flag
            KTHXBYE
            """, "START YARN: 42\nAFTER IS NOW A NUMBR: 42\nAFTER IS NOW A NUMBAR: 42.00\nAFTER IS NOW A YARN: 42.00\n0 IS NOW A TROOF: FAIL");
    }

    [Fact]
    public void MaekNumbar()
    {
        AssertOutput("""
            BTW Test MAEK <expression> A NUMBAR from YARN, NUMBR, and TROOF
            BTW Per spec: results print with two decimal places when cast to YARN

            HAI 1.2
              BTW YARN to NUMBAR (integer)
              VISIBLE "YARN :"42:" AS NUMBAR:: " MAEK "42" A NUMBAR

              BTW YARN with decimal to NUMBAR
              VISIBLE "YARN :"3.14:" AS NUMBAR:: " MAEK "3.14" A NUMBAR

              BTW NUMBR to NUMBAR
              VISIBLE "NUMBR 7 AS NUMBAR:: " MAEK 7 A NUMBAR

              BTW TROOF to NUMBAR
              VISIBLE "WIN AS NUMBAR:: " MAEK WIN A NUMBAR
              VISIBLE "FAIL AS NUMBAR:: " MAEK FAIL A NUMBAR
            KTHXBYE
            """, "YARN \"42\" AS NUMBAR: 42.00\nYARN \"3.14\" AS NUMBAR: 3.14\nNUMBR 7 AS NUMBAR: 7.00\nWIN AS NUMBAR: 1.00\nFAIL AS NUMBAR: 0.00");
    }

    [Fact]
    public void MaekNumbr()
    {
        AssertOutput("""
            BTW Test MAEK <expression> A NUMBR from YARN, NUMBAR, and TROOF
            BTW Per spec: YARN parses to integer, NUMBAR truncates, TROOF WIN/FAIL become 1/0

            HAI 1.2
              BTW YARN to NUMBR (integer)
              VISIBLE "YARN :"42:" AS NUMBR:: " MAEK "42" A NUMBR

              BTW YARN with decimal truncates toward zero
              VISIBLE "YARN :"3.14:" AS NUMBR:: " MAEK "3.14" A NUMBR

              BTW NUMBAR to NUMBR truncates decimal part
              I HAS A pi ITZ 3.14159
              VISIBLE "NUMBAR 3.14159 AS NUMBR:: " MAEK pi A NUMBR

              BTW TROOF to NUMBR
              VISIBLE "WIN AS NUMBR:: " MAEK WIN A NUMBR
              VISIBLE "FAIL AS NUMBR:: " MAEK FAIL A NUMBR
            KTHXBYE
            """, "YARN \"42\" AS NUMBR: 42\nYARN \"3.14\" AS NUMBR: 3\nNUMBAR 3.14159 AS NUMBR: 3\nWIN AS NUMBR: 1\nFAIL AS NUMBR: 0");
    }

    [Fact]
    public void MaekTroof()
    {
        AssertOutput("""
            BTW Test MAEK <expression> A TROOF for numbers, strings, and NOOB
            BTW Per spec: 0 and empty string are FAIL, non-zero/non-empty are WIN, NOOB is FAIL

            HAI 1.2
              BTW numeric zero is FAIL
              VISIBLE "0 AS TROOF:: " MAEK 0 A TROOF

              BTW empty string is FAIL
              VISIBLE ":":" AS TROOF:: " MAEK "" A TROOF

              BTW non-zero number is WIN
              VISIBLE "42 AS TROOF:: " MAEK 42 A TROOF

              BTW non-empty string is WIN
              VISIBLE ":"hai:" AS TROOF:: " MAEK "hai" A TROOF

              BTW NOOB casts to FAIL
              I HAS A nothing ITZ NOOB
              VISIBLE "NOOB AS TROOF:: " MAEK nothing A TROOF
            KTHXBYE
            """, "0 AS TROOF: FAIL\n\"\" AS TROOF: FAIL\n42 AS TROOF: WIN\n\"hai\" AS TROOF: WIN\nNOOB AS TROOF: FAIL");
    }

    [Fact]
    public void MaekYarn()
    {
        AssertOutput("""
            BTW Test MAEK <expression> A YARN from NUMBR, NUMBAR, and TROOF
            BTW Per spec: NUMBAR is truncated to 2 decimal places, TROOF prints WIN/FAIL

            HAI 1.2
              BTW NUMBR to YARN
              VISIBLE "NUMBR 42 AS YARN:: " MAEK 42 A YARN

              BTW NUMBAR to YARN with 2 decimal digits
              VISIBLE "NUMBAR 3.14159 AS YARN:: " MAEK 3.14159 A YARN

              BTW TROOF to YARN
              VISIBLE "WIN AS YARN:: " MAEK WIN A YARN
              VISIBLE "FAIL AS YARN:: " MAEK FAIL A YARN
            KTHXBYE
            """, "NUMBR 42 AS YARN: 42\nNUMBAR 3.14159 AS YARN: 3.14\nWIN AS YARN: WIN\nFAIL AS YARN: FAIL");
    }

    [Fact]
    public void NoobExplicitCast()
    {
        AssertOutput("""
            BTW Test explicit casts from NOOB to TROOF, NUMBR, NUMBAR, and YARN
            BTW Per spec: NOOB casts to FAIL/0/0.0/"" depending on target type

            HAI 1.2
              I HAS A nothing ITZ NOOB

              VISIBLE "NOOB AS TROOF:: " MAEK nothing A TROOF
              VISIBLE "NOOB AS NUMBR:: " MAEK nothing A NUMBR
              VISIBLE "NOOB AS NUMBAR:: " MAEK nothing A NUMBAR
              VISIBLE "NOOB AS YARN:: [" MAEK nothing A YARN "]"
            KTHXBYE
            """, "NOOB AS TROOF: FAIL\nNOOB AS NUMBR: 0\nNOOB AS NUMBAR: 0.00\nNOOB AS YARN: []");
    }

    [Fact]
    public void NumbarToYarnTruncation()
    {
        AssertOutput("""
            BTW Test NUMBAR to YARN truncation to two decimal places
            BTW Per spec: NUMBAR prints with two decimal digits when cast to YARN

            HAI 1.2
              I HAS A pi ITZ 3.14159
              VISIBLE "PI AS YARN:: " MAEK pi A YARN

              I HAS A half ITZ 0.5
              VISIBLE "0.5 AS YARN:: " MAEK half A YARN

              I HAS A neg ITZ -1.234
              VISIBLE "-1.234 AS YARN:: " MAEK neg A YARN
            KTHXBYE
            """, "PI AS YARN: 3.14\n0.5 AS YARN: 0.50\n-1.234 AS YARN: -1.23");
    }

    [Fact]
    public void YarnToNumbrParsing()
    {
        AssertOutput("""
            BTW Test parsing YARN to NUMBR and error on non-numeric
            BTW Per spec: integer parses directly, decimal truncates, non-numeric causes runtime error

            HAI 1.2
              BTW integer string
              VISIBLE ":"42:" AS NUMBR:: " MAEK "42" A NUMBR

              BTW decimal string truncates toward zero
              VISIBLE ":"3.14:" AS NUMBR:: " MAEK "3.14" A NUMBR

              BTW non-numeric string should cause runtime error (no further output)
              MAEK "LOL" A NUMBR
            KTHXBYE
            """, "\"42\" AS NUMBR: 42\n\"3.14\" AS NUMBR: 3");
    }
}
