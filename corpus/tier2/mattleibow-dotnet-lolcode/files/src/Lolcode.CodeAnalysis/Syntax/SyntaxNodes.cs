using System.Collections.Immutable;
using Lolcode.CodeAnalysis.Text;

namespace Lolcode.CodeAnalysis.Syntax;

/// <summary>
/// Base class for all syntax nodes in the AST.
/// </summary>
public abstract class SyntaxNode
{
    /// <summary>The kind of syntax node.</summary>
    public abstract SyntaxKind Kind { get; }

    /// <summary>The text span of this node.</summary>
    public abstract TextSpan Span { get; }
}

// ============ Statements ============

/// <summary>Base class for statement syntax nodes.</summary>
public abstract class StatementSyntax : SyntaxNode { }

/// <summary>Root node of the syntax tree.</summary>
public sealed class CompilationUnitSyntax : SyntaxNode
{
    /// <summary>The program statement (HAI...KTHXBYE).</summary>
    public ProgramStatementSyntax Program { get; }

    /// <summary>The end-of-file token.</summary>
    public SyntaxToken EndOfFileToken { get; }

    public CompilationUnitSyntax(ProgramStatementSyntax program, SyntaxToken endOfFileToken)
    {
        Program = program;
        EndOfFileToken = endOfFileToken;
    }

    public override SyntaxKind Kind => SyntaxKind.CompilationUnit;
    public override TextSpan Span => TextSpan.FromBounds(Program.Span.Start, EndOfFileToken.Span.End);
}

/// <summary>HAI [version] ... KTHXBYE block.</summary>
public sealed class ProgramStatementSyntax : StatementSyntax
{
    public SyntaxToken HaiKeyword { get; }
    public SyntaxToken? VersionToken { get; }
    public ImmutableArray<StatementSyntax> Statements { get; }
    public SyntaxToken KthxbyeKeyword { get; }

    public ProgramStatementSyntax(
        SyntaxToken haiKeyword,
        SyntaxToken? versionToken,
        ImmutableArray<StatementSyntax> statements,
        SyntaxToken kthxbyeKeyword)
    {
        HaiKeyword = haiKeyword;
        VersionToken = versionToken;
        Statements = statements;
        KthxbyeKeyword = kthxbyeKeyword;
    }

    public override SyntaxKind Kind => SyntaxKind.ProgramStatement;
    public override TextSpan Span => TextSpan.FromBounds(HaiKeyword.Position, KthxbyeKeyword.Span.End);
}

/// <summary>I HAS A &lt;name&gt; [ITZ &lt;expr&gt;]</summary>
public sealed class VariableDeclarationSyntax : StatementSyntax
{
    public SyntaxToken NameToken { get; }
    public ExpressionSyntax? Initializer { get; }

    public VariableDeclarationSyntax(SyntaxToken nameToken, ExpressionSyntax? initializer)
    {
        NameToken = nameToken;
        Initializer = initializer;
    }

    public override SyntaxKind Kind => SyntaxKind.VariableDeclarationStatement;
    public override TextSpan Span
    {
        get
        {
            int end = Initializer?.Span.End ?? NameToken.Span.End;
            return TextSpan.FromBounds(NameToken.Position, end);
        }
    }
}

/// <summary>&lt;name&gt; R &lt;expr&gt;</summary>
public sealed class AssignmentStatementSyntax : StatementSyntax
{
    public SyntaxToken NameToken { get; }
    public ExpressionSyntax Expression { get; }

    public AssignmentStatementSyntax(SyntaxToken nameToken, ExpressionSyntax expression)
    {
        NameToken = nameToken;
        Expression = expression;
    }

    public override SyntaxKind Kind => SyntaxKind.AssignmentStatement;
    public override TextSpan Span => TextSpan.FromBounds(NameToken.Position, Expression.Span.End);
}

/// <summary>VISIBLE &lt;expr&gt;+ [!]</summary>
public sealed class VisibleStatementSyntax : StatementSyntax
{
    public SyntaxToken Keyword { get; }
    public ImmutableArray<ExpressionSyntax> Arguments { get; }
    public bool SuppressNewline { get; }

    public VisibleStatementSyntax(
        SyntaxToken keyword,
        ImmutableArray<ExpressionSyntax> arguments,
        bool suppressNewline)
    {
        Keyword = keyword;
        Arguments = arguments;
        SuppressNewline = suppressNewline;
    }

    public override SyntaxKind Kind => SyntaxKind.VisibleStatement;
    public override TextSpan Span
    {
        get
        {
            int end = Arguments.Length > 0 ? Arguments[^1].Span.End : Keyword.Span.End;
            return TextSpan.FromBounds(Keyword.Position, end);
        }
    }
}

/// <summary>GIMMEH &lt;name&gt;</summary>
public sealed class GimmehStatementSyntax : StatementSyntax
{
    public SyntaxToken Keyword { get; }
    public SyntaxToken NameToken { get; }

    public GimmehStatementSyntax(SyntaxToken keyword, SyntaxToken nameToken)
    {
        Keyword = keyword;
        NameToken = nameToken;
    }

    public override SyntaxKind Kind => SyntaxKind.GimmehStatement;
    public override TextSpan Span => TextSpan.FromBounds(Keyword.Position, NameToken.Span.End);
}

/// <summary>A bare expression statement (sets IT).</summary>
public sealed class ExpressionStatementSyntax : StatementSyntax
{
    public ExpressionSyntax Expression { get; }

    public ExpressionStatementSyntax(ExpressionSyntax expression)
    {
        Expression = expression;
    }

    public override SyntaxKind Kind => SyntaxKind.ExpressionStatement;
    public override TextSpan Span => Expression.Span;
}

/// <summary>O RLY? ... OIC conditional block.</summary>
public sealed class IfStatementSyntax : StatementSyntax
{
    public SyntaxToken ORlyKeyword { get; }
    public BlockStatementSyntax YaRlyBody { get; }
    public ImmutableArray<MebbeClauseSyntax> MebbeClauses { get; }
    public BlockStatementSyntax? NoWaiBody { get; }
    public SyntaxToken OicKeyword { get; }

    public IfStatementSyntax(
        SyntaxToken oRlyKeyword,
        BlockStatementSyntax yaRlyBody,
        ImmutableArray<MebbeClauseSyntax> mebbeClauses,
        BlockStatementSyntax? noWaiBody,
        SyntaxToken oicKeyword)
    {
        ORlyKeyword = oRlyKeyword;
        YaRlyBody = yaRlyBody;
        MebbeClauses = mebbeClauses;
        NoWaiBody = noWaiBody;
        OicKeyword = oicKeyword;
    }

    public override SyntaxKind Kind => SyntaxKind.IfStatement;
    public override TextSpan Span => TextSpan.FromBounds(ORlyKeyword.Position, OicKeyword.Span.End);
}

/// <summary>MEBBE &lt;expr&gt; ... clause inside an O RLY? block.</summary>
public sealed class MebbeClauseSyntax : SyntaxNode
{
    public SyntaxToken MebbeKeyword { get; }
    public ExpressionSyntax Condition { get; }
    public BlockStatementSyntax Body { get; }

    public MebbeClauseSyntax(SyntaxToken mebbeKeyword, ExpressionSyntax condition, BlockStatementSyntax body)
    {
        MebbeKeyword = mebbeKeyword;
        Condition = condition;
        Body = body;
    }

    public override SyntaxKind Kind => SyntaxKind.MebbeClause;
    public override TextSpan Span => TextSpan.FromBounds(MebbeKeyword.Position, Body.Span.End);
}

/// <summary>WTF? ... OIC switch block.</summary>
public sealed class SwitchStatementSyntax : StatementSyntax
{
    public SyntaxToken WtfKeyword { get; }
    public ImmutableArray<OmgClauseSyntax> OmgClauses { get; }
    public BlockStatementSyntax? OmgwtfBody { get; }
    public SyntaxToken OicKeyword { get; }

    public SwitchStatementSyntax(
        SyntaxToken wtfKeyword,
        ImmutableArray<OmgClauseSyntax> omgClauses,
        BlockStatementSyntax? omgwtfBody,
        SyntaxToken oicKeyword)
    {
        WtfKeyword = wtfKeyword;
        OmgClauses = omgClauses;
        OmgwtfBody = omgwtfBody;
        OicKeyword = oicKeyword;
    }

    public override SyntaxKind Kind => SyntaxKind.SwitchStatement;
    public override TextSpan Span => TextSpan.FromBounds(WtfKeyword.Position, OicKeyword.Span.End);
}

/// <summary>OMG &lt;literal&gt; ... case clause in WTF? block.</summary>
public sealed class OmgClauseSyntax : SyntaxNode
{
    public SyntaxToken OmgKeyword { get; }
    public ExpressionSyntax Value { get; }
    public BlockStatementSyntax Body { get; }

    public OmgClauseSyntax(SyntaxToken omgKeyword, ExpressionSyntax value, BlockStatementSyntax body)
    {
        OmgKeyword = omgKeyword;
        Value = value;
        Body = body;
    }

    public override SyntaxKind Kind => SyntaxKind.OmgClause;
    public override TextSpan Span => TextSpan.FromBounds(OmgKeyword.Position, Body.Span.End);
}

/// <summary>IM IN YR &lt;label&gt; [&lt;op&gt; YR &lt;var&gt; [TIL|WILE &lt;expr&gt;]] ... IM OUTTA YR &lt;label&gt;</summary>
public sealed class LoopStatementSyntax : StatementSyntax
{
    public SyntaxToken ImInKeyword { get; }
    public SyntaxToken LabelToken { get; }
    public SyntaxToken? OperationToken { get; }
    public SyntaxToken? VariableToken { get; }
    public SyntaxToken? ConditionKeyword { get; }
    public ExpressionSyntax? Condition { get; }
    public BlockStatementSyntax Body { get; }
    public SyntaxToken ImOuttaKeyword { get; }
    public SyntaxToken EndLabelToken { get; }

    public LoopStatementSyntax(
        SyntaxToken imInKeyword,
        SyntaxToken labelToken,
        SyntaxToken? operationToken,
        SyntaxToken? variableToken,
        SyntaxToken? conditionKeyword,
        ExpressionSyntax? condition,
        BlockStatementSyntax body,
        SyntaxToken imOuttaKeyword,
        SyntaxToken endLabelToken)
    {
        ImInKeyword = imInKeyword;
        LabelToken = labelToken;
        OperationToken = operationToken;
        VariableToken = variableToken;
        ConditionKeyword = conditionKeyword;
        Condition = condition;
        Body = body;
        ImOuttaKeyword = imOuttaKeyword;
        EndLabelToken = endLabelToken;
    }

    public override SyntaxKind Kind => SyntaxKind.LoopStatement;
    public override TextSpan Span => TextSpan.FromBounds(ImInKeyword.Position, EndLabelToken.Span.End);
}

/// <summary>GTFO</summary>
public sealed class GtfoStatementSyntax : StatementSyntax
{
    public SyntaxToken Keyword { get; }

    public GtfoStatementSyntax(SyntaxToken keyword) => Keyword = keyword;

    public override SyntaxKind Kind => SyntaxKind.GtfoStatement;
    public override TextSpan Span => Keyword.Span;
}

/// <summary>HOW IZ I &lt;name&gt; [YR &lt;param&gt; [AN YR &lt;param&gt;]*] ... IF U SAY SO</summary>
public sealed class FunctionDeclarationSyntax : StatementSyntax
{
    public SyntaxToken NameToken { get; }
    public ImmutableArray<SyntaxToken> Parameters { get; }
    public BlockStatementSyntax Body { get; }

    public FunctionDeclarationSyntax(
        SyntaxToken nameToken,
        ImmutableArray<SyntaxToken> parameters,
        BlockStatementSyntax body)
    {
        NameToken = nameToken;
        Parameters = parameters;
        Body = body;
    }

    public override SyntaxKind Kind => SyntaxKind.FunctionDeclarationStatement;
    public override TextSpan Span => TextSpan.FromBounds(NameToken.Position, Body.Span.End);
}

/// <summary>FOUND YR &lt;expr&gt;</summary>
public sealed class ReturnStatementSyntax : StatementSyntax
{
    public SyntaxToken Keyword { get; }
    public ExpressionSyntax Expression { get; }

    public ReturnStatementSyntax(SyntaxToken keyword, ExpressionSyntax expression)
    {
        Keyword = keyword;
        Expression = expression;
    }

    public override SyntaxKind Kind => SyntaxKind.ReturnStatement;
    public override TextSpan Span => TextSpan.FromBounds(Keyword.Position, Expression.Span.End);
}

/// <summary>&lt;name&gt; IS NOW A &lt;type&gt;</summary>
public sealed class CastStatementSyntax : StatementSyntax
{
    public SyntaxToken NameToken { get; }
    public SyntaxToken TypeToken { get; }

    public CastStatementSyntax(SyntaxToken nameToken, SyntaxToken typeToken)
    {
        NameToken = nameToken;
        TypeToken = typeToken;
    }

    public override SyntaxKind Kind => SyntaxKind.CastStatement;
    public override TextSpan Span => TextSpan.FromBounds(NameToken.Position, TypeToken.Span.End);
}

/// <summary>A block of statements.</summary>
public sealed class BlockStatementSyntax : StatementSyntax
{
    public ImmutableArray<StatementSyntax> Statements { get; }

    public BlockStatementSyntax(ImmutableArray<StatementSyntax> statements)
    {
        Statements = statements;
    }

    public override SyntaxKind Kind => SyntaxKind.BlockStatement;
    public override TextSpan Span
    {
        get
        {
            if (Statements.Length == 0)
                return new TextSpan(0, 0);
            return TextSpan.FromBounds(Statements[0].Span.Start, Statements[^1].Span.End);
        }
    }
}

// ============ Expressions ============

/// <summary>Base class for expression syntax nodes.</summary>
public abstract class ExpressionSyntax : SyntaxNode { }

/// <summary>A literal value (NUMBR, NUMBAR, YARN, WIN, FAIL, NOOB).</summary>
public sealed class LiteralExpressionSyntax : ExpressionSyntax
{
    public SyntaxToken Token { get; }
    public object? Value { get; }

    public LiteralExpressionSyntax(SyntaxToken token, object? value)
    {
        Token = token;
        Value = value;
    }

    public override SyntaxKind Kind => SyntaxKind.LiteralExpression;
    public override TextSpan Span => Token.Span;
}

/// <summary>A variable reference.</summary>
public sealed class VariableExpressionSyntax : ExpressionSyntax
{
    public SyntaxToken NameToken { get; }

    public VariableExpressionSyntax(SyntaxToken nameToken)
    {
        NameToken = nameToken;
    }

    public override SyntaxKind Kind => SyntaxKind.VariableExpression;
    public override TextSpan Span => NameToken.Span;
}

/// <summary>NOT &lt;expr&gt;</summary>
public sealed class UnaryExpressionSyntax : ExpressionSyntax
{
    public SyntaxToken OperatorToken { get; }
    public ExpressionSyntax Operand { get; }

    public UnaryExpressionSyntax(SyntaxToken operatorToken, ExpressionSyntax operand)
    {
        OperatorToken = operatorToken;
        Operand = operand;
    }

    public override SyntaxKind Kind => SyntaxKind.UnaryExpression;
    public override TextSpan Span => TextSpan.FromBounds(OperatorToken.Position, Operand.Span.End);
}

/// <summary>Binary operator: SUM OF x AN y, etc.</summary>
public sealed class BinaryExpressionSyntax : ExpressionSyntax
{
    public SyntaxToken OperatorToken { get; }
    public ExpressionSyntax Left { get; }
    public ExpressionSyntax Right { get; }

    public BinaryExpressionSyntax(SyntaxToken operatorToken, ExpressionSyntax left, ExpressionSyntax right)
    {
        OperatorToken = operatorToken;
        Left = left;
        Right = right;
    }

    public override SyntaxKind Kind => SyntaxKind.BinaryExpression;
    public override TextSpan Span => TextSpan.FromBounds(OperatorToken.Position, Right.Span.End);
}

/// <summary>SMOOSH &lt;expr&gt;+ [MKAY]</summary>
public sealed class SmooshExpressionSyntax : ExpressionSyntax
{
    public SyntaxToken Keyword { get; }
    public ImmutableArray<ExpressionSyntax> Operands { get; }

    public SmooshExpressionSyntax(SyntaxToken keyword, ImmutableArray<ExpressionSyntax> operands)
    {
        Keyword = keyword;
        Operands = operands;
    }

    public override SyntaxKind Kind => SyntaxKind.SmooshExpression;
    public override TextSpan Span
    {
        get
        {
            int end = Operands.Length > 0 ? Operands[^1].Span.End : Keyword.Span.End;
            return TextSpan.FromBounds(Keyword.Position, end);
        }
    }
}

/// <summary>ALL OF &lt;expr&gt;+ MKAY — variadic AND.</summary>
public sealed class AllOfExpressionSyntax : ExpressionSyntax
{
    public SyntaxToken Keyword { get; }
    public ImmutableArray<ExpressionSyntax> Operands { get; }

    public AllOfExpressionSyntax(SyntaxToken keyword, ImmutableArray<ExpressionSyntax> operands)
    {
        Keyword = keyword;
        Operands = operands;
    }

    public override SyntaxKind Kind => SyntaxKind.AllOfExpression;
    public override TextSpan Span
    {
        get
        {
            int end = Operands.Length > 0 ? Operands[^1].Span.End : Keyword.Span.End;
            return TextSpan.FromBounds(Keyword.Position, end);
        }
    }
}

/// <summary>ANY OF &lt;expr&gt;+ MKAY — variadic OR.</summary>
public sealed class AnyOfExpressionSyntax : ExpressionSyntax
{
    public SyntaxToken Keyword { get; }
    public ImmutableArray<ExpressionSyntax> Operands { get; }

    public AnyOfExpressionSyntax(SyntaxToken keyword, ImmutableArray<ExpressionSyntax> operands)
    {
        Keyword = keyword;
        Operands = operands;
    }

    public override SyntaxKind Kind => SyntaxKind.AnyOfExpression;
    public override TextSpan Span
    {
        get
        {
            int end = Operands.Length > 0 ? Operands[^1].Span.End : Keyword.Span.End;
            return TextSpan.FromBounds(Keyword.Position, end);
        }
    }
}

/// <summary>BOTH SAEM &lt;expr&gt; AN &lt;expr&gt;</summary>
public sealed class ComparisonExpressionSyntax : ExpressionSyntax
{
    public SyntaxToken Keyword { get; }
    public ExpressionSyntax Left { get; }
    public ExpressionSyntax Right { get; }

    public ComparisonExpressionSyntax(SyntaxToken keyword, ExpressionSyntax left, ExpressionSyntax right)
    {
        Keyword = keyword;
        Left = left;
        Right = right;
    }

    public override SyntaxKind Kind => SyntaxKind.ComparisonExpression;
    public override TextSpan Span => TextSpan.FromBounds(Keyword.Position, Right.Span.End);
}

/// <summary>DIFFRINT &lt;expr&gt; AN &lt;expr&gt;</summary>
public sealed class DiffrintExpressionSyntax : ExpressionSyntax
{
    public SyntaxToken Keyword { get; }
    public ExpressionSyntax Left { get; }
    public ExpressionSyntax Right { get; }

    public DiffrintExpressionSyntax(SyntaxToken keyword, ExpressionSyntax left, ExpressionSyntax right)
    {
        Keyword = keyword;
        Left = left;
        Right = right;
    }

    public override SyntaxKind Kind => SyntaxKind.DiffrintExpression;
    public override TextSpan Span => TextSpan.FromBounds(Keyword.Position, Right.Span.End);
}

/// <summary>MAEK &lt;expr&gt; [A] &lt;type&gt;</summary>
public sealed class CastExpressionSyntax : ExpressionSyntax
{
    public SyntaxToken Keyword { get; }
    public ExpressionSyntax Operand { get; }
    public SyntaxToken TypeToken { get; }

    public CastExpressionSyntax(SyntaxToken keyword, ExpressionSyntax operand, SyntaxToken typeToken)
    {
        Keyword = keyword;
        Operand = operand;
        TypeToken = typeToken;
    }

    public override SyntaxKind Kind => SyntaxKind.CastExpression;
    public override TextSpan Span => TextSpan.FromBounds(Keyword.Position, TypeToken.Span.End);
}

/// <summary>I IZ &lt;name&gt; [YR &lt;expr&gt; [AN YR &lt;expr&gt;]*] MKAY</summary>
public sealed class FunctionCallExpressionSyntax : ExpressionSyntax
{
    public SyntaxToken NameToken { get; }
    public ImmutableArray<ExpressionSyntax> Arguments { get; }

    public FunctionCallExpressionSyntax(SyntaxToken nameToken, ImmutableArray<ExpressionSyntax> arguments)
    {
        NameToken = nameToken;
        Arguments = arguments;
    }

    public override SyntaxKind Kind => SyntaxKind.FunctionCallExpression;
    public override TextSpan Span
    {
        get
        {
            int end = Arguments.Length > 0 ? Arguments[^1].Span.End : NameToken.Span.End;
            return TextSpan.FromBounds(NameToken.Position, end);
        }
    }
}

/// <summary>Implicit IT variable reference.</summary>
public sealed class ItExpressionSyntax : ExpressionSyntax
{
    public SyntaxToken Token { get; }

    public ItExpressionSyntax(SyntaxToken token) => Token = token;

    public override SyntaxKind Kind => SyntaxKind.ItExpression;
    public override TextSpan Span => Token.Span;
}
