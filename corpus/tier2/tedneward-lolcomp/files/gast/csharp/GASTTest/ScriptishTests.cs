using Xunit;
using GAST;

namespace GASTTest;

public class ScriptishTests
{
    [Fact]
    public void Math()
    {
        // x = 2 + 2
        var varX = new GAST.Variable("x");

        var literal2 = new GAST.Literal("2");
        var twoPlusTwo = new GAST.AdditionOperator(literal2, literal2);

        var xEquals = new GAST.AssignmentOperator(varX, twoPlusTwo);

        Assert.Equal("(assignment-operator (variable x) (addition-operator (literal 2) (literal 2)))", 
            xEquals.SExpr);
    }
    [Fact]
    public void Block()
    {
        // {
        //   var x = 2
        //   var y = 3
        //   var z = 0
        //   z = x + y   
        // }
        var block = new GAST.Block();
        var x = new GAST.Variable("x");
        block.Statements.Add(x);
        var assignX = new GAST.AssignmentOperator(x, new GAST.Literal("2"));
        block.Statements.Add(assignX);

        var y = new GAST.Variable("y");
        block.Statements.Add(y);
        var assignY = new GAST.AssignmentOperator(y, new GAST.Literal("3"));
        block.Statements.Add(assignY);

        var z = new GAST.Variable("z");
        block.Statements.Add(z);
        var assignZ = new GAST.AssignmentOperator(z, new GAST.AdditionOperator(x, y));
        block.Statements.Add(assignZ);
        
        System.Console.WriteLine(block.SExpr);
        Assert.Equal("(block " +
            "(variable x)" + "(assignment-operator (variable x) (literal 2))" +
            "(variable y)" + "(assignment-operator (variable y) (literal 3))" +
            "(variable z)" + "(assignment-operator (variable z) (addition-operator (variable x) (variable y)))" +
        ")", block.SExpr);
    }
}
