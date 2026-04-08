using System.Collections.Immutable;
using Lolcode.CodeAnalysis.Symbols;
using Lolcode.CodeAnalysis.Syntax;

namespace Lolcode.CodeAnalysis.BoundTree;

/// <summary>
/// Context tracking for GTFO resolution.
/// </summary>
internal enum ControlFlowContext
{
    None,
    Loop,
    Switch,
    Function
}

/// <summary>
/// Base class for all bound nodes (output of semantic analysis).
/// </summary>
internal abstract class BoundNode
{
    /// <summary>The syntax node that produced this bound node, if any. Used for PDB sequence points.</summary>
    public SyntaxNode? Syntax { get; }

    protected BoundNode(SyntaxNode? syntax = null) => Syntax = syntax;

    /// <summary>The kind of bound node.</summary>
    public abstract BoundKind Kind { get; }
}

/// <summary>Enumerates bound node types.</summary>
internal enum BoundKind
{
    // Statements
    BlockStatement,
    VariableDeclaration,
    Assignment,
    VisibleStatement,
    GimmehStatement,
    ExpressionStatement,
    IfStatement,
    SwitchStatement,
    LoopStatement,
    GtfoStatement,
    FunctionDeclaration,
    ReturnStatement,
    CastStatement,

    // Expressions
    LiteralExpression,
    VariableExpression,
    UnaryExpression,
    BinaryExpression,
    SmooshExpression,
    AllOfExpression,
    AnyOfExpression,
    ComparisonExpression,
    CastExpression,
    FunctionCallExpression,
    ItExpression,
}

// ============ Bound Statements ============

/// <summary>Base for bound statements.</summary>
internal abstract class BoundStatement : BoundNode
{
    protected BoundStatement(SyntaxNode? syntax = null) : base(syntax) { }
}

/// <summary>A block of bound statements.</summary>
internal sealed class BoundBlockStatement : BoundStatement
{
    public ImmutableArray<BoundStatement> Statements { get; }
    public BoundBlockStatement(ImmutableArray<BoundStatement> statements, SyntaxNode? syntax = null)
        : base(syntax) => Statements = statements;
    public override BoundKind Kind => BoundKind.BlockStatement;
}

/// <summary>Variable declaration: I HAS A x [ITZ expr]</summary>
internal sealed class BoundVariableDeclaration : BoundStatement
{
    public VariableSymbol Variable { get; }
    public BoundExpression? Initializer { get; }
    public BoundVariableDeclaration(VariableSymbol variable, BoundExpression? initializer, SyntaxNode? syntax = null)
        : base(syntax)
    {
        Variable = variable;
        Initializer = initializer;
    }
    public override BoundKind Kind => BoundKind.VariableDeclaration;
}

/// <summary>Assignment: x R expr</summary>
internal sealed class BoundAssignment : BoundStatement
{
    public VariableSymbol Variable { get; }
    public BoundExpression Expression { get; }
    public BoundAssignment(VariableSymbol variable, BoundExpression expression, SyntaxNode? syntax = null)
        : base(syntax)
    {
        Variable = variable;
        Expression = expression;
    }
    public override BoundKind Kind => BoundKind.Assignment;
}

/// <summary>VISIBLE statement.</summary>
internal sealed class BoundVisibleStatement : BoundStatement
{
    public ImmutableArray<BoundExpression> Arguments { get; }
    public bool SuppressNewline { get; }
    public BoundVisibleStatement(ImmutableArray<BoundExpression> arguments, bool suppressNewline, SyntaxNode? syntax = null)
        : base(syntax)
    {
        Arguments = arguments;
        SuppressNewline = suppressNewline;
    }
    public override BoundKind Kind => BoundKind.VisibleStatement;
}

/// <summary>GIMMEH statement.</summary>
internal sealed class BoundGimmehStatement : BoundStatement
{
    public VariableSymbol Variable { get; }
    public BoundGimmehStatement(VariableSymbol variable, SyntaxNode? syntax = null)
        : base(syntax) => Variable = variable;
    public override BoundKind Kind => BoundKind.GimmehStatement;
}

/// <summary>Expression statement (sets IT).</summary>
internal sealed class BoundExpressionStatement : BoundStatement
{
    public BoundExpression Expression { get; }
    public BoundExpressionStatement(BoundExpression expression, SyntaxNode? syntax = null)
        : base(syntax) => Expression = expression;
    public override BoundKind Kind => BoundKind.ExpressionStatement;
}

/// <summary>O RLY? conditional.</summary>
internal sealed class BoundIfStatement : BoundStatement
{
    public BoundBlockStatement ThenBlock { get; }
    public ImmutableArray<BoundMebbeClause> MebbeClauses { get; }
    public BoundBlockStatement? ElseBlock { get; }
    public BoundIfStatement(BoundBlockStatement thenBlock, ImmutableArray<BoundMebbeClause> mebbeClauses, BoundBlockStatement? elseBlock, SyntaxNode? syntax = null)
        : base(syntax)
    {
        ThenBlock = thenBlock;
        MebbeClauses = mebbeClauses;
        ElseBlock = elseBlock;
    }
    public override BoundKind Kind => BoundKind.IfStatement;
}

/// <summary>Bound MEBBE clause.</summary>
internal sealed class BoundMebbeClause
{
    public BoundExpression Condition { get; }
    public BoundBlockStatement Body { get; }
    public SyntaxNode? Syntax { get; }
    public BoundMebbeClause(BoundExpression condition, BoundBlockStatement body, SyntaxNode? syntax = null)
    {
        Condition = condition;
        Body = body;
        Syntax = syntax;
    }
}

/// <summary>WTF? switch.</summary>
internal sealed class BoundSwitchStatement : BoundStatement
{
    public ImmutableArray<BoundOmgClause> OmgClauses { get; }
    public BoundBlockStatement? DefaultBlock { get; }
    public BoundSwitchStatement(ImmutableArray<BoundOmgClause> omgClauses, BoundBlockStatement? defaultBlock, SyntaxNode? syntax = null)
        : base(syntax)
    {
        OmgClauses = omgClauses;
        DefaultBlock = defaultBlock;
    }
    public override BoundKind Kind => BoundKind.SwitchStatement;
}

/// <summary>Bound OMG clause.</summary>
internal sealed class BoundOmgClause
{
    public object? LiteralValue { get; }
    public BoundBlockStatement Body { get; }
    public SyntaxNode? Syntax { get; }
    public BoundOmgClause(object? literalValue, BoundBlockStatement body, SyntaxNode? syntax = null)
    {
        LiteralValue = literalValue;
        Body = body;
        Syntax = syntax;
    }
}

/// <summary>IM IN YR loop.</summary>
internal sealed class BoundLoopStatement : BoundStatement
{
    public string Label { get; }

    /// <summary>"UPPIN", "NERFIN", or a custom function name. Null for infinite loops.</summary>
    public string? Operation { get; }

    /// <summary>The loop variable. Null for infinite loops.</summary>
    public VariableSymbol? Variable { get; }

    /// <summary>True for TIL, false for WILE. Null if no condition.</summary>
    public bool? IsTil { get; }

    /// <summary>The loop condition. Null for infinite loops.</summary>
    public BoundExpression? Condition { get; }

    public BoundBlockStatement Body { get; }

    public BoundLoopStatement(
        string label, string? operation, VariableSymbol? variable,
        bool? isTil, BoundExpression? condition, BoundBlockStatement body,
        SyntaxNode? syntax = null) : base(syntax)
    {
        Label = label;
        Operation = operation;
        Variable = variable;
        IsTil = isTil;
        Condition = condition;
        Body = body;
    }
    public override BoundKind Kind => BoundKind.LoopStatement;
}

/// <summary>GTFO statement.</summary>
internal sealed class BoundGtfoStatement : BoundStatement
{
    /// <summary>The resolved control flow context.</summary>
    public ControlFlowContext Context { get; }
    public BoundGtfoStatement(ControlFlowContext context, SyntaxNode? syntax = null)
        : base(syntax) => Context = context;
    public override BoundKind Kind => BoundKind.GtfoStatement;
}

/// <summary>HOW IZ I function declaration.</summary>
internal sealed class BoundFunctionDeclaration : BoundStatement
{
    public FunctionSymbol Function { get; }
    public BoundBlockStatement Body { get; }
    public BoundFunctionDeclaration(FunctionSymbol function, BoundBlockStatement body, SyntaxNode? syntax = null)
        : base(syntax)
    {
        Function = function;
        Body = body;
    }
    public override BoundKind Kind => BoundKind.FunctionDeclaration;
}

/// <summary>FOUND YR return.</summary>
internal sealed class BoundReturnStatement : BoundStatement
{
    public BoundExpression Expression { get; }
    public BoundReturnStatement(BoundExpression expression, SyntaxNode? syntax = null)
        : base(syntax) => Expression = expression;
    public override BoundKind Kind => BoundKind.ReturnStatement;
}

/// <summary>IS NOW A cast statement.</summary>
internal sealed class BoundCastStatement : BoundStatement
{
    public VariableSymbol Variable { get; }
    public string TargetType { get; }
    public BoundCastStatement(VariableSymbol variable, string targetType, SyntaxNode? syntax = null)
        : base(syntax)
    {
        Variable = variable;
        TargetType = targetType;
    }
    public override BoundKind Kind => BoundKind.CastStatement;
}

// ============ Bound Expressions ============

/// <summary>Base for bound expressions.</summary>
internal abstract class BoundExpression : BoundNode
{
    protected BoundExpression(SyntaxNode? syntax = null) : base(syntax) { }
}

/// <summary>Literal value (int, double, string, bool, null).</summary>
internal sealed class BoundLiteralExpression : BoundExpression
{
    public object? Value { get; }
    public BoundLiteralExpression(object? value, SyntaxNode? syntax = null)
        : base(syntax) => Value = value;
    public override BoundKind Kind => BoundKind.LiteralExpression;
}

/// <summary>Variable reference.</summary>
internal sealed class BoundVariableExpression : BoundExpression
{
    public VariableSymbol Variable { get; }
    public BoundVariableExpression(VariableSymbol variable, SyntaxNode? syntax = null)
        : base(syntax) => Variable = variable;
    public override BoundKind Kind => BoundKind.VariableExpression;
}

/// <summary>NOT expr.</summary>
internal sealed class BoundUnaryExpression : BoundExpression
{
    public BoundUnaryOperatorKind OperatorKind { get; }
    public BoundExpression Operand { get; }
    public BoundUnaryExpression(BoundUnaryOperatorKind operatorKind, BoundExpression operand, SyntaxNode? syntax = null)
        : base(syntax)
    {
        OperatorKind = operatorKind;
        Operand = operand;
    }
    public override BoundKind Kind => BoundKind.UnaryExpression;
}

/// <summary>Binary arithmetic/boolean operation.</summary>
internal sealed class BoundBinaryExpression : BoundExpression
{
    public BoundBinaryOperatorKind OperatorKind { get; }
    public BoundExpression Left { get; }
    public BoundExpression Right { get; }
    public BoundBinaryExpression(BoundBinaryOperatorKind operatorKind, BoundExpression left, BoundExpression right, SyntaxNode? syntax = null)
        : base(syntax)
    {
        OperatorKind = operatorKind;
        Left = left;
        Right = right;
    }
    public override BoundKind Kind => BoundKind.BinaryExpression;
}

/// <summary>SMOOSH concatenation.</summary>
internal sealed class BoundSmooshExpression : BoundExpression
{
    public ImmutableArray<BoundExpression> Operands { get; }
    public BoundSmooshExpression(ImmutableArray<BoundExpression> operands, SyntaxNode? syntax = null)
        : base(syntax) => Operands = operands;
    public override BoundKind Kind => BoundKind.SmooshExpression;
}

/// <summary>ALL OF variadic AND.</summary>
internal sealed class BoundAllOfExpression : BoundExpression
{
    public ImmutableArray<BoundExpression> Operands { get; }
    public BoundAllOfExpression(ImmutableArray<BoundExpression> operands, SyntaxNode? syntax = null)
        : base(syntax) => Operands = operands;
    public override BoundKind Kind => BoundKind.AllOfExpression;
}

/// <summary>ANY OF variadic OR.</summary>
internal sealed class BoundAnyOfExpression : BoundExpression
{
    public ImmutableArray<BoundExpression> Operands { get; }
    public BoundAnyOfExpression(ImmutableArray<BoundExpression> operands, SyntaxNode? syntax = null)
        : base(syntax) => Operands = operands;
    public override BoundKind Kind => BoundKind.AnyOfExpression;
}

/// <summary>BOTH SAEM or DIFFRINT comparison.</summary>
internal sealed class BoundComparisonExpression : BoundExpression
{
    /// <summary>True for BOTH SAEM (equality), false for DIFFRINT (inequality).</summary>
    public bool IsEquality { get; }
    public BoundExpression Left { get; }
    public BoundExpression Right { get; }
    public BoundComparisonExpression(bool isEquality, BoundExpression left, BoundExpression right, SyntaxNode? syntax = null)
        : base(syntax)
    {
        IsEquality = isEquality;
        Left = left;
        Right = right;
    }
    public override BoundKind Kind => BoundKind.ComparisonExpression;
}

/// <summary>MAEK cast expression.</summary>
internal sealed class BoundCastExpression : BoundExpression
{
    public BoundExpression Operand { get; }
    public string TargetType { get; }
    public BoundCastExpression(BoundExpression operand, string targetType, SyntaxNode? syntax = null)
        : base(syntax)
    {
        Operand = operand;
        TargetType = targetType;
    }
    public override BoundKind Kind => BoundKind.CastExpression;
}

/// <summary>I IZ function call.</summary>
internal sealed class BoundFunctionCallExpression : BoundExpression
{
    public FunctionSymbol Function { get; }
    public ImmutableArray<BoundExpression> Arguments { get; }
    public BoundFunctionCallExpression(FunctionSymbol function, ImmutableArray<BoundExpression> arguments, SyntaxNode? syntax = null)
        : base(syntax)
    {
        Function = function;
        Arguments = arguments;
    }
    public override BoundKind Kind => BoundKind.FunctionCallExpression;
}

/// <summary>IT implicit variable reference.</summary>
internal sealed class BoundItExpression : BoundExpression
{
    public BoundItExpression(SyntaxNode? syntax = null) : base(syntax) { }
    public override BoundKind Kind => BoundKind.ItExpression;
}
