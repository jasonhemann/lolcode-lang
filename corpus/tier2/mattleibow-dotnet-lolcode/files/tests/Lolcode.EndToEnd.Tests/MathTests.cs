namespace Lolcode.EndToEnd.Tests;

public class MathTests : EndToEndTestBase
{
    [Fact]
    public void BiggrOf()
    {
        AssertOutput("""
            BTW BIGGR OF tests: equal values, negatives, mixed types; returns the greater operand
            HAI 1.2
              VISIBLE BIGGR OF 5 AN 5
              VISIBLE BIGGR OF -3 AN -7
              VISIBLE BIGGR OF 3 AN 4.0
              VISIBLE BIGGR OF "3" AN 4
              VISIBLE BIGGR OF 3.14 AN "3.99"
            KTHXBYE
            """, "5\n-3\n4.00\n4\n3.99");
    }

    [Fact]
    public void DiffOf()
    {
        AssertOutput("""
            BTW DIFF OF tests: includes negative results and type promotion
            HAI 1.2
              VISIBLE DIFF OF 10 AN 3
              VISIBLE DIFF OF 3 AN 10
              VISIBLE DIFF OF 5.5 AN 2
              VISIBLE DIFF OF 5 AN 2.5
              VISIBLE DIFF OF 2.5 AN 5
            KTHXBYE
            """, "7\n-7\n3.50\n2.50\n-2.50");
    }

    [Fact]
    public void MathTypePromotion()
    {
        AssertOutput("""
            BTW Type promotion: NUMBR+NUMBR=NUMBR; any NUMBAR promotes to NUMBAR
            HAI 1.2
              VISIBLE SUM OF 1 AN 2
              VISIBLE DIFF OF 5 AN 3
              VISIBLE PRODUKT OF 2 AN 2
              VISIBLE QUOSHUNT OF 7 AN 2
              VISIBLE SUM OF 1.0 AN 2
              VISIBLE DIFF OF 5.0 AN 3
              VISIBLE PRODUKT OF 2 AN 2.5
              VISIBLE QUOSHUNT OF 7 AN 2.0
              VISIBLE SUM OF "3" AN "4.0"
            KTHXBYE
            """, "3\n2\n4\n3\n3.00\n2.00\n5.00\n3.50\n7.00");
    }

    [Fact]
    public void MathWithAn()
    {
        AssertOutput("""
            BTW AN keyword optional between operands
            HAI 1.2
              VISIBLE SUM OF 3 AN 4
              VISIBLE SUM OF 3 4
              VISIBLE DIFF OF 10 AN 3
              VISIBLE DIFF OF 10 3
              VISIBLE PRODUKT OF 2 AN 4
              VISIBLE PRODUKT OF 2 4
              VISIBLE QUOSHUNT OF 9 AN 3
              VISIBLE QUOSHUNT OF 9 3
              VISIBLE BIGGR OF 5 AN 5
              VISIBLE BIGGR OF 5 5
            KTHXBYE
            """, "7\n7\n7\n7\n8\n8\n3\n3\n5\n5");
    }

    [Fact]
    public void ModOf()
    {
        AssertOutput("""
            BTW MOD OF tests: edge cases including negatives and YARN casting
            HAI 1.2
              VISIBLE MOD OF 7 AN 2
              VISIBLE MOD OF 7.0 AN 2
              VISIBLE MOD OF -7 AN 2
              VISIBLE MOD OF 7 AN -2
              VISIBLE MOD OF -7 AN -2
              VISIBLE MOD OF 0 AN 3
              VISIBLE MOD OF "10" AN "3"
              VISIBLE MOD OF "3.5" AN "2"
            KTHXBYE
            """, "1\n1.00\n-1\n1\n-1\n0\n1\n1.50");
    }

    [Fact]
    public void NestedMath()
    {
        AssertOutput("""
            BTW Nested math: deeply composed expressions
            HAI 1.2
              VISIBLE SUM OF PRODUKT OF 2 AN DIFF OF 10 AN 5 AN QUOSHUNT OF 9 AN 3
              VISIBLE QUOSHUNT OF PRODUKT OF 2.5 AN SUM OF 1 AN 2 AN 2
              VISIBLE SUM OF SMALLR OF 10 AN 7 AN BIGGR OF 3 AN 4
            KTHXBYE
            """, "13\n3.75\n11");
    }

    [Fact]
    public void ProduktOf()
    {
        AssertOutput("""
            BTW PRODUKT OF tests: zero, negatives, mixed types
            HAI 1.2
              VISIBLE PRODUKT OF 3 AN 4
              VISIBLE PRODUKT OF -3 AN 4
              VISIBLE PRODUKT OF 3 AN 0
              VISIBLE PRODUKT OF 2.5 AN 4
              VISIBLE PRODUKT OF -2.0 AN -3
              VISIBLE PRODUKT OF 2.0 AN 0
            KTHXBYE
            """, "12\n-12\n0\n10.00\n6.00\n0.00");
    }

    [Fact]
    public void QuoshuntOf()
    {
        AssertOutput("""
            BTW QUOSHUNT OF tests: integer vs float division
            HAI 1.2
              VISIBLE QUOSHUNT OF 7 AN 2
              VISIBLE QUOSHUNT OF 7.0 AN 2
              VISIBLE QUOSHUNT OF 7 AN 2.0
              VISIBLE QUOSHUNT OF -7 AN 2
              VISIBLE QUOSHUNT OF 1 AN 2
              VISIBLE QUOSHUNT OF 1.0 AN 2
            KTHXBYE
            """, "3\n3.50\n3.50\n-3\n0\n0.50");
    }

    [Fact]
    public void SmallrOf()
    {
        AssertOutput("""
            BTW SMALLR OF tests: equal values, negatives, mixed types; returns the smaller operand
            HAI 1.2
              VISIBLE SMALLR OF 5 AN 5
              VISIBLE SMALLR OF -3 AN -7
              VISIBLE SMALLR OF 3 AN 4.0
              VISIBLE SMALLR OF "3" AN 4
              VISIBLE SMALLR OF 3.14 AN "3.99"
            KTHXBYE
            """, "5\n-7\n3.00\n3\n3.14");
    }

    [Fact]
    public void SumOf()
    {
        AssertOutput("""
            BTW SUM OF tests: NUMBR, NUMBAR, mixed types, nested expressions
            HAI 1.2
              VISIBLE SUM OF 3 AN 4
              VISIBLE SUM OF 2.5 AN 1.25
              VISIBLE SUM OF 3 AN 4.0
              VISIBLE SUM OF PRODUKT OF 2 AN 3.5 AN DIFF OF 10 AN 4
            KTHXBYE
            """, "7\n3.75\n7.00\n13.00");
    }

    [Fact]
    public void YarnInMath()
    {
        AssertOutput("""
            BTW YARN numeric parsing in math: integer and float strings
            HAI 1.2
              VISIBLE SUM OF "42" AN 8
              VISIBLE SUM OF "3.14" AN 0
              VISIBLE DIFF OF "100" AN "58"
              VISIBLE PRODUKT OF "2.5" AN "4"
              VISIBLE QUOSHUNT OF "7.0" AN "2"
            KTHXBYE
            """, "50\n3.14\n42\n10.00\n3.50");
    }

    [Fact]
    public void LargeNumberArithmetic()
    {
        AssertOutput("""
            HAI 1.2
              VISIBLE PRODUKT OF 100000 AN 100000
            KTHXBYE
            """, "1410065408");
    }

    [Fact]
    public void NegativeNumbers()
    {
        AssertOutput("""
            HAI 1.2
              I HAS A x ITZ -42
              VISIBLE x
              VISIBLE SUM OF x AN 100
            KTHXBYE
            """, "-42\n58");
    }
}
