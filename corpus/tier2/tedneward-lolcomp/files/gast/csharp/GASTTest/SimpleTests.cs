using Xunit;
using GAST;

namespace GASTTest;

public class SimpleTests
{
    [Fact]
    public void LiteralTest()
    {
        var lit1 = new GAST.Literal("1");
        Assert.Equal("1", lit1.SourceValue);
        Assert.Equal("(literal 1)", lit1.SExpr);

        var litName = new GAST.Literal("Fred Jones");
        Assert.Equal("Fred Jones", litName.SourceValue);
        Assert.Equal("(literal Fred Jones)", litName.SExpr);
    }
}
