namespace Lolcode.EndToEnd.Tests;

public class ComparisonTests : EndToEndTestBase
{
    [Fact]
    public void BothSaem()
    {
        AssertOutput("""
            BTW BOTH SAEM: equality for same type same value vs diff value
            HAI 1.2
              VISIBLE BOTH SAEM 3 AN 3
              VISIBLE BOTH SAEM 3 AN 4
              VISIBLE BOTH SAEM "hai" AN "hai"
              VISIBLE BOTH SAEM "hai" AN "hai!"
              VISIBLE BOTH SAEM WIN AN WIN
              VISIBLE BOTH SAEM FAIL AN WIN
            KTHXBYE
            """, "WIN\nFAIL\nWIN\nFAIL\nWIN\nFAIL");
    }

    [Fact]
    public void Diffrint()
    {
        AssertOutput("""
            BTW DIFFRINT: inequality
            HAI 1.2
              VISIBLE DIFFRINT 3 AN 4
              VISIBLE DIFFRINT 3 AN 3
              VISIBLE DIFFRINT "hai" AN "hai"
              VISIBLE DIFFRINT WIN AN FAIL
            KTHXBYE
            """, "WIN\nFAIL\nFAIL\nWIN");
    }

    [Fact]
    public void GreaterThanIdiom()
    {
        AssertOutput("""
            BTW Greater-than-or-equal idiom: BOTH SAEM x AN BIGGR OF x AN y
            HAI 1.2
              I HAS A x ITZ 5
              I HAS A y ITZ 3
              VISIBLE BOTH SAEM x AN BIGGR OF x AN y
              x R 3
              y R 5
              VISIBLE BOTH SAEM x AN BIGGR OF x AN y
              x R 5
              y R 5
              VISIBLE BOTH SAEM x AN BIGGR OF x AN y
              x R 3.0
              y R 3
              VISIBLE BOTH SAEM x AN BIGGR OF x AN y
              x R 2
              y R 2.5
              VISIBLE BOTH SAEM x AN BIGGR OF x AN y
            KTHXBYE
            """, "WIN\nFAIL\nWIN\nWIN\nFAIL");
    }

    [Fact]
    public void LessThanIdiom()
    {
        AssertOutput("""
            BTW Greater-than idiom: DIFFRINT x AN SMALLR OF x AN y (x > y)
            HAI 1.2
              I HAS A x ITZ 5
              I HAS A y ITZ 3
              VISIBLE DIFFRINT x AN SMALLR OF x AN y
              x R 3
              y R 5
              VISIBLE DIFFRINT x AN SMALLR OF x AN y
              x R 5
              y R 5
              VISIBLE DIFFRINT x AN SMALLR OF x AN y
              x R 3.0
              y R 2
              VISIBLE DIFFRINT x AN SMALLR OF x AN y
              x R 3.0
              y R 3
              VISIBLE DIFFRINT x AN SMALLR OF x AN y
            KTHXBYE
            """, "WIN\nFAIL\nFAIL\nWIN\nFAIL");
    }

    [Fact]
    public void NoAutoCastEquality()
    {
        AssertOutput("""
            BTW BOTH SAEM has NO automatic casting: YARN "3" vs NUMBR 3
            HAI 1.2
              VISIBLE BOTH SAEM "3" AN 3
              VISIBLE BOTH SAEM "3.0" AN 3
              VISIBLE DIFFRINT "3" AN 3
            KTHXBYE
            """, "FAIL\nFAIL\nWIN");
    }

    [Fact]
    public void NumbarComparison()
    {
        AssertOutput("""
            BTW NUMBAR comparison and NUMBR vs NUMBAR promotion
            HAI 1.2
              VISIBLE BOTH SAEM 3 AN 3.0
              VISIBLE BOTH SAEM 3.14 AN 3.140
              VISIBLE DIFFRINT 3 AN 3.1
              VISIBLE DIFFRINT 3.14 AN 3.13
            KTHXBYE
            """, "WIN\nWIN\nWIN\nWIN");
    }
}
