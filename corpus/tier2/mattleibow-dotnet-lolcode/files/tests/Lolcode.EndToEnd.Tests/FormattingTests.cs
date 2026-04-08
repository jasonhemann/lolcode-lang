namespace Lolcode.EndToEnd.Tests;

public class FormattingTests : EndToEndTestBase
{
    [Fact]
    public void CommaSeparator()
    {
        AssertOutput("""
            BTW Test comma as statement separator (soft-command-break)
            BTW Per spec: comma acts as virtual newline

            HAI 1.2
              BTW multiple statements on one line
              I HAS A x ITZ 1, I HAS A y ITZ 2, I HAS A z ITZ 3
              VISIBLE x, VISIBLE y, VISIBLE z

              BTW comma after declaration before assignment
              I HAS A a, a R 10, VISIBLE a

              BTW comma in conditional context
              5, O RLY?, YA RLY, VISIBLE "TRUTHY", OIC

              BTW comma before comment
              VISIBLE "BEFORE COMMENT", BTW this is ignored
              VISIBLE "AFTER COMMENT"

              BTW many statements
              I HAS A n ITZ 0, n R SUM OF n AN 1, n R SUM OF n AN 1, n R SUM OF n AN 1, VISIBLE n
            KTHXBYE
            """, "1\n2\n3\n10\nTRUTHY\nBEFORE COMMENT\nAFTER COMMENT\n3");
    }

    [Fact]
    public void Indentation()
    {
        AssertOutput("""
            BTW Test that indentation is irrelevant
            BTW Per spec: indentation is irrelevant

            HAI 1.2
            BTW no indentation
            I HAS A a ITZ 1
            VISIBLE a

              BTW 2 spaces
              I HAS A b ITZ 2
              VISIBLE b

                BTW 4 spaces
                I HAS A c ITZ 3
                VISIBLE c

            				BTW tabs
            				I HAS A d ITZ 4
            				VISIBLE d

              	  	BTW mixed tabs and spaces
              	  	I HAS A e ITZ 5
              	  	VISIBLE e

            BTW back to no indent
            VISIBLE "DONE"
            KTHXBYE
            """, "1\n2\n3\n4\n5\nDONE");
    }

    [Fact]
    public void LineContinuation()
    {
        AssertOutput("""
            BTW Test line continuation with ... and … (ellipsis)
            BTW Per spec: multiple lines combined into single command with ... or …

            HAI 1.2
              BTW basic line continuation with ...
              VISIBLE "LINE" ...
                " CONTINUED"

              BTW line continuation with Unicode ellipsis …
              VISIBLE "UNICODE" …
                " ELLIPSIS"

              BTW multiple continuations chained
              VISIBLE ...
                "MULTI" ...
                " LINE" ...
                " CHAIN"

              BTW continuation in middle of keyword
              I HAS A ...
                longvar ITZ 42
              VISIBLE longvar

              BTW ... on its own line (empty line inclusion)
              VISIBLE "BEFORE" ...
                ...
                " AFTER"

              BTW continuation in expression
              I HAS A result ITZ SUM OF ...
                10 AN ...
                20
              VISIBLE result
            KTHXBYE
            """, "LINE CONTINUED\nUNICODE ELLIPSIS\nMULTI LINE CHAIN\n42\nBEFORE AFTER\n30");
    }

    [Fact]
    public void MultipleSpaces()
    {
        AssertOutput("""
            BTW Test multiple spaces treated as single space
            BTW Per spec: multiple spaces and tabs treated as single spaces

            HAI 1.2
              BTW extra spaces between tokens
              I   HAS   A   var   ITZ   42
              VISIBLE   var

              BTW extra spaces in operators
              I HAS A result ITZ SUM    OF    10    AN    20
              VISIBLE result

              BTW tabs between tokens
              I	HAS	A	tabvar	ITZ	99
              VISIBLE	tabvar

              BTW mixed spaces and tabs
              I 	 HAS 	 A 	 mixed 	 ITZ 	 7
              VISIBLE  	  mixed

              BTW spaces in VISIBLE arguments
              VISIBLE    "HELLO"    " "    "WORLD"
            KTHXBYE
            """, "42\n30\n99\n7\nHELLO WORLD");
    }

    [Fact]
    public void NumbarPrintsTwoDecimals()
    {
        AssertOutput("""
            HAI 1.2
              I HAS A x ITZ 7.0
              VISIBLE x
            KTHXBYE
            """, "7.00");
    }

    [Fact]
    public void NumbarPiTruncatesToTwoDecimals()
    {
        AssertOutput("""
            HAI 1.2
              I HAS A x ITZ 3.14159
              VISIBLE x
            KTHXBYE
            """, "3.14");
    }
}
