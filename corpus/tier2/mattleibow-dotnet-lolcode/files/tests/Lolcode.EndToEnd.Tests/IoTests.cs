namespace Lolcode.EndToEnd.Tests;

public class IoTests : EndToEndTestBase
{
    [Fact]
    public void VisibleBasic()
    {
        AssertOutput("""
            BTW Test basic VISIBLE with string, number, and expression
            BTW Per spec: VISIBLE prints each argument cast to YARN and adds a newline by default

            HAI 1.2
              VISIBLE "HELLO"
              VISIBLE 123
              VISIBLE SUM OF 2 AN 3
            KTHXBYE
            """, "HELLO\n123\n5");
    }

    [Fact]
    public void VisibleExpression()
    {
        AssertOutput("""
            BTW Test VISIBLE with inline expressions (math, SMOOSH, casting)
            BTW Per spec: expressions are evaluated then cast to YARN for output

            HAI 1.2
              I HAS A a ITZ 2
              I HAS A b ITZ 5

              VISIBLE SUM OF a AN b
              VISIBLE SMOOSH "A+B=" AN SUM OF a AN b MKAY

              I HAS A pi ITZ 3.14159
              VISIBLE SMOOSH "PI=" AN pi MKAY

              VISIBLE MAEK "42" A NUMBR

              VISIBLE SMOOSH "BOOL " AN MAEK 0 A TROOF AN " / " AN MAEK 1 A TROOF MKAY
            KTHXBYE
            """, "7\nA+B=7\nPI=3.14\n42\nBOOL FAIL / WIN");
    }

    [Fact]
    public void VisibleMultipleArgs()
    {
        AssertOutput("""
            BTW Test VISIBLE with multiple arguments and auto-concatenation
            BTW Per spec: VISIBLE concatenates all arguments after casting to YARN

            HAI 1.2
              I HAS A x ITZ 10
              I HAS A y ITZ 20

              VISIBLE "X=" x ", Y=" y
              VISIBLE "SUM=" SUM OF x AN y "!"
              VISIBLE "MIXED " x " AND " "STRING"
            KTHXBYE
            """, "X=10, Y=20\nSUM=30!\nMIXED 10 AND STRING");
    }

    [Fact]
    public void VisibleNewlineDefault()
    {
        AssertOutput("""
            BTW Test that VISIBLE adds newline by default
            BTW Per spec: every VISIBLE without ! ends with a newline

            HAI 1.2
              VISIBLE "LINE ONE"
              VISIBLE "LINE TWO"
              VISIBLE "LINE THREE"
            KTHXBYE
            """, "LINE ONE\nLINE TWO\nLINE THREE");
    }

    [Fact]
    public void VisibleNoNewline()
    {
        AssertOutput("""
            BTW Test VISIBLE newline suppression with !
            BTW Per spec: final ! suppresses the automatic newline

            HAI 1.2
              VISIBLE "NO NEWLINE"!
              VISIBLE " AFTER"
              VISIBLE "SECOND LINE"
            KTHXBYE
            """, "NO NEWLINE AFTER\nSECOND LINE");
    }

    [Fact]
    public void GimmehInput()
    {
        AssertOutput("""
            HAI 1.2
              I HAS A line
              GIMMEH line
              VISIBLE line
            KTHXBYE
            """, "hello world", stdin: "hello world\n");
    }

    [Fact]
    public void VisibleMultipleArgsWithAn()
    {
        AssertOutput("""
            HAI 1.2
              VISIBLE "A" AN "B" AN "C"
            KTHXBYE
            """, "ABC");
    }
}
