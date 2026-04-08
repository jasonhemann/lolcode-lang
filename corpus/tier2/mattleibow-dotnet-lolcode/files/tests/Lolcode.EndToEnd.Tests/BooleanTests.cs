namespace Lolcode.EndToEnd.Tests;

public class BooleanTests : EndToEndTestBase
{
    [Fact]
    public void AllOf()
    {
        AssertOutput("""
            BTW ALL OF: infinite arity AND; MKAY terminator; MKAY may be omitted at EOL
            HAI 1.2
              VISIBLE ALL OF WIN AN WIN AN WIN MKAY
              VISIBLE ALL OF WIN AN WIN AN FAIL MKAY
              VISIBLE ALL OF 1 AN "hai" AN 2 MKAY
              VISIBLE ALL OF WIN AN WIN AN WIN
              VISIBLE ALL OF WIN AN WIN AN FAIL
              VISIBLE ALL OF 1 2 3 MKAY
            KTHXBYE
            """, "WIN\nFAIL\nWIN\nWIN\nFAIL\nWIN");
    }

    [Fact]
    public void AnyOf()
    {
        AssertOutput("""
            BTW ANY OF: infinite arity OR; MKAY terminator; MKAY may be omitted at EOL
            HAI 1.2
              VISIBLE ANY OF FAIL AN FAIL AN WIN MKAY
              VISIBLE ANY OF FAIL AN FAIL AN FAIL MKAY
              VISIBLE ANY OF "" AN 0 AN "x" MKAY
              VISIBLE ANY OF "" AN 0 AN NOOB MKAY
              VISIBLE ANY OF FAIL AN WIN
            KTHXBYE
            """, "WIN\nFAIL\nWIN\nFAIL\nWIN");
    }

    [Fact]
    public void BooleanAutoCast()
    {
        AssertOutput("""
            BTW Boolean auto-cast: 0=FAIL, ""=FAIL, 42=WIN, "hai"=WIN, NOOB=FAIL
            HAI 1.2
              VISIBLE MAEK 0 A TROOF
              VISIBLE MAEK "" A TROOF
              VISIBLE MAEK 42 A TROOF
              VISIBLE MAEK "hai" A TROOF
              I HAS A n
              VISIBLE MAEK n A TROOF
            KTHXBYE
            """, "FAIL\nFAIL\nWIN\nWIN\nFAIL");
    }

    [Fact]
    public void BothOf()
    {
        AssertOutput("""
            BTW BOTH OF (AND): WIN/FAIL and auto-cast to TROOF from other types
            HAI 1.2
              VISIBLE BOTH OF WIN AN WIN
              VISIBLE BOTH OF WIN AN FAIL
              VISIBLE BOTH OF 1 AN "hai"
              VISIBLE BOTH OF 0 AN "hai"
              VISIBLE BOTH OF 42 AN ""
              I HAS A x
              VISIBLE BOTH OF x AN WIN
              VISIBLE BOTH OF 0.0 AN WIN
            KTHXBYE
            """, "WIN\nFAIL\nWIN\nFAIL\nFAIL\nFAIL\nFAIL");
    }

    [Fact]
    public void EitherOf()
    {
        AssertOutput("""
            BTW EITHER OF (OR): truthiness across values
            HAI 1.2
              VISIBLE EITHER OF WIN AN FAIL
              VISIBLE EITHER OF FAIL AN FAIL
              VISIBLE EITHER OF 0 AN "hai"
              VISIBLE EITHER OF "" AN 0
              VISIBLE EITHER OF NOOB AN FAIL
              VISIBLE EITHER OF NOOB AN "x"
            KTHXBYE
            """, "WIN\nFAIL\nWIN\nFAIL\nFAIL\nWIN");
    }

    [Fact]
    public void Not()
    {
        AssertOutput("""
            BTW NOT: unary negation with truthiness auto-cast
            HAI 1.2
              VISIBLE NOT WIN
              VISIBLE NOT FAIL
              VISIBLE NOT 0
              VISIBLE NOT 42
              VISIBLE NOT ""
              VISIBLE NOT "hai"
              VISIBLE NOT NOOB
            KTHXBYE
            """, "FAIL\nWIN\nWIN\nFAIL\nWIN\nFAIL\nWIN");
    }

    [Fact]
    public void WonOf()
    {
        AssertOutput("""
            BTW WON OF (XOR): FAIL if same, WIN if different
            HAI 1.2
              VISIBLE WON OF WIN AN WIN
              VISIBLE WON OF WIN AN FAIL
              VISIBLE WON OF 1 AN "hai"
              VISIBLE WON OF 0 AN ""
              VISIBLE WON OF 42 AN 0
            KTHXBYE
            """, "FAIL\nWIN\nFAIL\nFAIL\nWIN");
    }
}
