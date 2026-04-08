namespace GAST;

/*
 * Base class for all GAST classes.
 */
public abstract class Node
{
    public Node() { }

    // Source file relationship
    //
    public string File { get; set; } = "";
    public int Line { get; set; } = 0;
    public int ColStart { get; set; } = 0;
    public int ColEnd { get; set; } = 0;

    public abstract string SExpr { get; }
}

/*
 * Module represents a compilation unit
 */
public class Module : Node
{
    public Module() { }

    public List<Statement> Statements { get; } = new List<Statement>();

    public override string SExpr 
    { 
        get { return Statements.Aggregate("(", (acc, stmt) => acc + stmt.SExpr ) + ")"; } 
    }
}

/*
 * Statement 
 */
public abstract class Statement : Node
{
    public Statement() { }
}

/*
 * Expr is an expression type--it yields a value.
 */
public abstract class Expression : Statement
{
    public Expression() { }
}

public class Variable : Expression
{
    public Variable(string name) { Name = name; }

    public string Name { get; }
    public override string SExpr { get { return "(variable " + Name + ")"; } }
}

public class Block : Expression
{
    public Block() { }

    public List<Statement> Statements { get; } = new List<Statement>();

    public override string SExpr 
    { 
        get { return Statements.Aggregate("(block ", (acc, x) => acc += x.SExpr) + ")"; }
    }
}

public class Condition : Expression
{
    public Condition(Expression cond, Block block) { Test = cond; Block = block; }

    public Expression Test { get; }
    public Block Block { get; }

    public override string SExpr { get { return "(condition)"; } }
}

/*
 * Literal represents a source-present literal, like "4" or "'Fred Jones'"
 * in the source code.
 */
public class Literal : Expression
{
    public Literal(string literal) { SourceValue = literal; }

    // The literal as written in the source
    public string SourceValue { get; } = "";

    public override string SExpr { get { return "(literal " + SourceValue + ")"; } }
}
// Could/would have subclasses of Literal that correspond
// to the core primitive types of the language: CharLiteral, 
// StringLiteral, IntLiteral, FloatLiteral, BoolLiteral
// NullLiteral?

/*
 * Operators that take two operands to perform their operation.
 */
public class BinaryOperator : Expression
{
    public BinaryOperator(Expression l, Expression r) { Left = l; Right = r; }

    public Expression Left { get; set; }
    public Expression Right { get; set; }

    public override string SExpr { get { return "(binary-operator)"; } }
}
public class AdditionOperator : BinaryOperator
{
    public AdditionOperator(Expression left, Expression right) : base(left, right) { } 

    public override string SExpr { get { return "(addition-operator " + Left.SExpr + " " + Right.SExpr + ")"; } }
}
public class SubtractionOperator : BinaryOperator
{
    public SubtractionOperator(Expression left, Expression right) : base(left, right) { } 

    public override string SExpr { get { return "(subtraction-operator " + Left.SExpr + " " + Right.SExpr + ")"; } }
}
public class MultiplicationOperator : BinaryOperator
{
    public MultiplicationOperator(Expression left, Expression right) : base(left, right) { } 

    public override string SExpr { get { return "(multiplication-operator " + Left.SExpr + " " + Right.SExpr + ")"; } }
}
public class DivisionOperator : BinaryOperator
{
    public DivisionOperator(Expression left, Expression right) : base(left, right) { } 

    public override string SExpr { get { return "(division-operator " + Left.SExpr + " " + Right.SExpr + ")"; } }
}
public class ModuloOperator : BinaryOperator
{
    public ModuloOperator(Expression left, Expression right) : base(left, right) { } 

    public override string SExpr { get { return "(modulo-operator " + Left.SExpr + " " + Right.SExpr + ")"; } }
}
// Comparisons: GTOp, GTEOp, LTOp, LTEOp, EqualsOp, NotEqualsOp
public class AssignmentOperator : BinaryOperator
{
    public AssignmentOperator(Variable l, Expression r) : base(l, r) { }

    public override string SExpr { get { return "(assignment-operator " + Left.SExpr + " " + Right.SExpr + ")"; } }
}

public class UnaryOperator : Expression
{
    public UnaryOperator(Expression e) { Unary = e; }

    public Expression Unary { get; set; }

    public override string SExpr { get { return "(unary-operator)"; } }
}
// NegationOp (-5), NotOp (!x)



