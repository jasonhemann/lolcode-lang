namespace Lolcode.EndToEnd.Tests;

public class CommentTests : EndToEndTestBase
{
    [Fact]
    public void CommentEdgeCases()
    {
        AssertOutput("""
            BTW Test edge cases: BTW ignores trailing ... and ,
            BTW Per spec: line continuation and soft-command-breaks are ignored after BTW

            HAI 1.2
              BTW this comment has ... at the end but it does NOT continue...
              VISIBLE "LINE ONE"

              BTW this comment has comma, but it is ignored,
              VISIBLE "LINE TWO"

              BTW comment with both ... and ,
              VISIBLE "LINE THREE"

              VISIBLE "CODE" BTW inline comment ignores ... on same line too...
              VISIBLE "NEXT LINE"

              BTW comment with multiple ... in text ... still just one comment...
              VISIBLE "AFTER DOTS"

              BTW ellipsis in comment … should also be ignored…
              VISIBLE "AFTER ELLIPSIS"
            KTHXBYE
            """, "LINE ONE\nLINE TWO\nLINE THREE\nCODE\nNEXT LINE\nAFTER DOTS\nAFTER ELLIPSIS");
    }

    [Fact]
    public void MultiLineComment()
    {
        AssertOutput("""
            BTW Test multi-line comments with OBTW...TLDR
            BTW Per spec: started on own line or after comma

            HAI 1.2
              VISIBLE "BEFORE BLOCK"

              OBTW
                This is a multi-line comment.
                It can span many lines.
                None of this code executes:
                VISIBLE "NOT PRINTED"
              TLDR

              VISIBLE "AFTER BLOCK"

              BTW OBTW on same line as code after comma
              I HAS A x ITZ 5, OBTW
                comment block here
                more comments
              TLDR

              VISIBLE x

              BTW TLDR followed by code after comma
              OBTW another block TLDR, VISIBLE "AFTER TLDR COMMA"

              BTW nested-looking but not really nested
              OBTW
                OBTW this is not a nested comment
                just text inside the outer comment
              TLDR

              VISIBLE "DONE"
            KTHXBYE
            """, "BEFORE BLOCK\nAFTER BLOCK\n5\nAFTER TLDR COMMA\nDONE");
    }

    [Fact]
    public void SingleLineComment()
    {
        AssertOutput("""
            BTW Test single-line comments with BTW
            BTW Per spec: BTW after code, on own line, or after comma

            HAI 1.2
              BTW comment on its own line
              VISIBLE "ONE"

              VISIBLE "TWO" BTW comment after code

              VISIBLE "THREE", BTW comment after comma

              BTW multiple BTW on same line: BTW only first matters
              VISIBLE "FOUR"

              I HAS A x ITZ 10 BTW initialize x
              VISIBLE x
            KTHXBYE
            """, "ONE\nTWO\nTHREE\nFOUR\n10");
    }
}
