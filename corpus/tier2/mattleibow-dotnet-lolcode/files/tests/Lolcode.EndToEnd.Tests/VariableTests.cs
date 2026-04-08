namespace Lolcode.EndToEnd.Tests;

public class VariableTests : EndToEndTestBase
{
    [Fact]
    public void Assignment()
    {
        AssertOutput("""
            BTW Test assignment with R operator
            BTW Per spec: <variable> R <expression> for assignment

            HAI 1.2
              BTW basic assignment after declaration
              I HAS A x
              x R 10
              VISIBLE x

              BTW reassignment
              x R 20
              VISIBLE x

              BTW assignment with expression
              x R SUM OF x AN 5
              VISIBLE x

              BTW type change via assignment
              I HAS A var ITZ 42
              VISIBLE var
              var R "NOW A STRING"
              VISIBLE var
              var R 3.14
              VISIBLE var
              var R WIN
              VISIBLE var

              BTW assignment using another variable
              I HAS A a ITZ 100
              I HAS A b
              b R a
              VISIBLE b

              BTW self-referential assignment
              I HAS A n ITZ 5
              n R PRODUKT OF n AN n
              VISIBLE n
            KTHXBYE
            """, "10\n20\n25\n42\nNOW A STRING\n3.14\nWIN\n100\n25");
    }

    [Fact]
    public void CaseSensitivity()
    {
        AssertOutput("""
            BTW Test variable names are case-sensitive
            BTW Per spec: cheezburger, CheezBurger, CHEEZBURGER are different variables

            HAI 1.2
              BTW declare variables with same name different case
              I HAS A cat ITZ "lowercase"
              I HAS A Cat ITZ "mixed"
              I HAS A CAT ITZ "uppercase"

              VISIBLE cat
              VISIBLE Cat
              VISIBLE CAT

              BTW modify one, others unchanged
              cat R "modified lowercase"
              VISIBLE cat
              VISIBLE Cat
              VISIBLE CAT

              BTW more complex names
              I HAS A myVar ITZ 1
              I HAS A MyVar ITZ 2
              I HAS A MYVAR ITZ 3
              I HAS A myvar ITZ 4

              VISIBLE myVar
              VISIBLE MyVar
              VISIBLE MYVAR
              VISIBLE myvar

              BTW underscores and numbers
              I HAS A var_1 ITZ "one"
              I HAS A VAR_1 ITZ "ONE"
              I HAS A Var_1 ITZ "One"

              VISIBLE var_1
              VISIBLE VAR_1
              VISIBLE Var_1
            KTHXBYE
            """, "lowercase\nmixed\nuppercase\nmodified lowercase\nmixed\nuppercase\n1\n2\n3\n4\none\nONE\nOne");
    }

    [Fact]
    public void Declaration()
    {
        AssertOutput("""
            BTW Test variable declaration with I HAS A, with and without ITZ
            BTW Per spec: I HAS A declares, ITZ initializes in same statement

            HAI 1.2
              BTW declaration without initialization (becomes NOOB)
              I HAS A uninit

              BTW declaration with initialization - various types
              I HAS A num ITZ 42
              I HAS A float_num ITZ 3.14
              I HAS A str ITZ "HELLO"
              I HAS A truth ITZ WIN
              I HAS A lie ITZ FAIL

              BTW print initialized variables
              VISIBLE num
              VISIBLE float_num
              VISIBLE str
              VISIBLE truth
              VISIBLE lie

              BTW declare and init with expression
              I HAS A sum ITZ SUM OF 10 AN 20
              VISIBLE sum

              BTW declare with variable reference
              I HAS A copy ITZ num
              VISIBLE copy

              BTW multiple declarations
              I HAS A a ITZ 1
              I HAS A b ITZ 2
              I HAS A c ITZ 3
              VISIBLE a
              VISIBLE b
              VISIBLE c
            KTHXBYE
            """, "42\n3.14\nHELLO\nWIN\nFAIL\n30\n42\n1\n2\n3");
    }

    [Fact]
    public void ItNotSetByAssignment()
    {
        AssertOutput("""
            BTW Test that assignment and declaration do NOT update IT
            BTW Per spec: assignment statements have no side effects with IT

            HAI 1.2
              BTW set IT to a known value
              42
              VISIBLE IT

              BTW declaration does not change IT
              I HAS A x ITZ 100
              VISIBLE IT

              BTW assignment does not change IT
              x R 200
              VISIBLE IT

              BTW another assignment
              I HAS A y
              y R 999
              VISIBLE IT

              BTW expression statement DOES change IT
              SUM OF 1 AN 1
              VISIBLE IT

              BTW but declaration right after does NOT change IT
              I HAS A z ITZ 777
              VISIBLE IT

              BTW assignment with expression does NOT change IT
              BTW (the expression is evaluated, but IT is not updated)
              x R SUM OF 10 AN 20
              VISIBLE IT
            KTHXBYE
            """, "42\n42\n42\n42\n2\n2\n2");
    }

    [Fact]
    public void ItVariable()
    {
        AssertOutput("""
            BTW Test IT variable - set by expression statements
            BTW Per spec: bare expression sets IT; O RLY? and WTF? test IT

            HAI 1.2
              BTW expression statement sets IT
              SUM OF 3 AN 5
              VISIBLE IT

              BTW another expression updates IT
              PRODUKT OF 4 AN 7
              VISIBLE IT

              BTW IT used in O RLY?
              10
              O RLY?
                YA RLY
                  VISIBLE "10 IS TRUTHY"
              OIC

              BTW 0 is falsy
              0
              O RLY?
                YA RLY
                  VISIBLE "0 IS TRUTHY"
                NO WAI
                  VISIBLE "0 IS FALSY"
              OIC

              BTW IT used in WTF?
              "B"
              WTF?
                OMG "A"
                  VISIBLE "IT WAS A"
                  GTFO
                OMG "B"
                  VISIBLE "IT WAS B"
                  GTFO
                OMG "C"
                  VISIBLE "IT WAS C"
                  GTFO
              OIC

              BTW function call as expression sets IT
              HOW IZ I double YR n
                FOUND YR PRODUKT OF n AN 2
              IF U SAY SO

              I IZ double YR 21 MKAY
              VISIBLE IT

              BTW comparison expression sets IT
              BOTH SAEM 5 AN 5
              VISIBLE IT

              DIFFRINT 5 AN 10
              VISIBLE IT
            KTHXBYE
            """, "8\n28\n10 IS TRUTHY\n0 IS FALSY\nIT WAS B\n42\nWIN\nWIN");
    }

    [Fact]
    public void NoobVariable()
    {
        AssertOutput("""
            BTW Test uninitialized variables are NOOB
            BTW Per spec: until given initial value, variable is untyped (NOOB)

            HAI 1.2
              BTW declare without initialization
              I HAS A noob_var

              BTW NOOB printed via VISIBLE casts to YARN which is ""
              VISIBLE "START"
              VISIBLE noob_var
              VISIBLE "END"

              BTW NOOB is falsy (only implicit cast from NOOB is to TROOF = FAIL)
              noob_var
              O RLY?
                YA RLY
                  VISIBLE "NOOB IS TRUTHY"
                NO WAI
                  VISIBLE "NOOB IS FALSY"
              OIC

              BTW after assignment, no longer NOOB
              noob_var R "NOW DEFINED"
              VISIBLE noob_var

              BTW another uninitialized variable
              I HAS A another
              another
              O RLY?
                YA RLY
                  VISIBLE "ANOTHER IS TRUTHY"
                NO WAI
                  VISIBLE "ANOTHER IS FALSY"
              OIC
            KTHXBYE
            """, "START\n\nEND\nNOOB IS FALSY\nNOW DEFINED\nANOTHER IS FALSY");
    }
}
