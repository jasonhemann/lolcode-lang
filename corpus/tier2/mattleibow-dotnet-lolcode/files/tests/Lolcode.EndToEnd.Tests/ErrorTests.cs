namespace Lolcode.EndToEnd.Tests;

public class ErrorTests : EndToEndTestBase
{
    [Fact]
    public void NoobInArithmeticThrowsError()
    {
        AssertRuntimeError("""
            HAI 1.2
              I HAS A x
              VISIBLE SUM OF x AN 1
            KTHXBYE
            """, "NOOB");
    }

    [Fact]
    public void NonNumericYarnInArithmeticThrowsError()
    {
        AssertRuntimeError("""
            HAI 1.2
              VISIBLE SUM OF "hello" AN 1
            KTHXBYE
            """, "Cannot cast YARN to numeric");
    }

    [Fact]
    public void UndeclaredVariableError()
    {
        AssertCompileError("""
            HAI 1.2
              VISIBLE x
            KTHXBYE
            """, "LOL");
    }
}
