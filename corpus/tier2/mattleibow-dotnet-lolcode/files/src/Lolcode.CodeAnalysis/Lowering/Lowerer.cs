using System.Collections.Immutable;
using Lolcode.CodeAnalysis.BoundTree;
using Lolcode.CodeAnalysis.Symbols;

namespace Lolcode.CodeAnalysis.Lowering;

/// <summary>
/// Rewrites a bound tree into a simplified form for code generation.
/// Currently an identity pass — returns the tree unchanged.
/// Future: desugar complex constructs into simpler primitives.
/// </summary>
internal sealed class Lowerer
{
    private Lowerer() { }

    /// <summary>Lowers a bound block statement (compilation unit or function body).</summary>
    public static BoundBlockStatement Lower(BoundBlockStatement statement)
    {
        var lowerer = new Lowerer();
        return lowerer.RewriteBlockStatement(statement);
    }

    private BoundBlockStatement RewriteBlockStatement(BoundBlockStatement node)
    {
        var builder = ImmutableArray.CreateBuilder<BoundStatement>(node.Statements.Length);
        var changed = false;

        foreach (var statement in node.Statements)
        {
            var rewritten = RewriteStatement(statement);
            builder.Add(rewritten);
            if (rewritten != statement)
                changed = true;
        }

        if (!changed)
            return node;

        return new BoundBlockStatement(builder.MoveToImmutable(), syntax: node.Syntax);
    }

    private BoundStatement RewriteStatement(BoundStatement node)
    {
        return node switch
        {
            BoundBlockStatement s => RewriteBlockStatement(s),
            BoundVariableDeclaration s => RewriteVariableDeclaration(s),
            BoundAssignment s => RewriteAssignment(s),
            BoundVisibleStatement s => RewriteVisibleStatement(s),
            BoundGimmehStatement s => s,
            BoundExpressionStatement s => RewriteExpressionStatement(s),
            BoundIfStatement s => RewriteIfStatement(s),
            BoundSwitchStatement s => RewriteSwitchStatement(s),
            BoundLoopStatement s => RewriteLoopStatement(s),
            BoundGtfoStatement s => s,
            BoundFunctionDeclaration s => RewriteFunctionDeclaration(s),
            BoundReturnStatement s => RewriteReturnStatement(s),
            BoundCastStatement s => RewriteCastStatement(s),
            _ => node,
        };
    }

    private BoundExpression RewriteExpression(BoundExpression node)
    {
        return node switch
        {
            BoundLiteralExpression => node,
            BoundVariableExpression => node,
            BoundItExpression => node,
            BoundUnaryExpression e => RewriteUnaryExpression(e),
            BoundBinaryExpression e => RewriteBinaryExpression(e),
            BoundSmooshExpression e => RewriteSmooshExpression(e),
            BoundAllOfExpression e => RewriteAllOfExpression(e),
            BoundAnyOfExpression e => RewriteAnyOfExpression(e),
            BoundComparisonExpression e => RewriteComparisonExpression(e),
            BoundCastExpression e => RewriteCastExpression(e),
            BoundFunctionCallExpression e => RewriteFunctionCallExpression(e),
            _ => node,
        };
    }

    private BoundVariableDeclaration RewriteVariableDeclaration(BoundVariableDeclaration node)
    {
        if (node.Initializer is null)
            return node;

        var initializer = RewriteExpression(node.Initializer);
        if (initializer == node.Initializer)
            return node;

        return new BoundVariableDeclaration(node.Variable, initializer, syntax: node.Syntax);
    }

    private BoundAssignment RewriteAssignment(BoundAssignment node)
    {
        var expression = RewriteExpression(node.Expression);
        if (expression == node.Expression)
            return node;

        return new BoundAssignment(node.Variable, expression, syntax: node.Syntax);
    }

    private BoundVisibleStatement RewriteVisibleStatement(BoundVisibleStatement node)
    {
        var builder = ImmutableArray.CreateBuilder<BoundExpression>(node.Arguments.Length);
        var changed = false;

        foreach (var arg in node.Arguments)
        {
            var rewritten = RewriteExpression(arg);
            builder.Add(rewritten);
            if (rewritten != arg)
                changed = true;
        }

        if (!changed)
            return node;

        return new BoundVisibleStatement(builder.MoveToImmutable(), node.SuppressNewline, syntax: node.Syntax);
    }

    private BoundExpressionStatement RewriteExpressionStatement(BoundExpressionStatement node)
    {
        var expression = RewriteExpression(node.Expression);
        if (expression == node.Expression)
            return node;

        return new BoundExpressionStatement(expression, syntax: node.Syntax);
    }

    private BoundIfStatement RewriteIfStatement(BoundIfStatement node)
    {
        var thenBlock = RewriteBlockStatement(node.ThenBlock);

        var mebbeBuilder = ImmutableArray.CreateBuilder<BoundMebbeClause>(node.MebbeClauses.Length);
        var mebbeChanged = false;
        foreach (var clause in node.MebbeClauses)
        {
            var cond = RewriteExpression(clause.Condition);
            var body = RewriteBlockStatement(clause.Body);
            if (cond != clause.Condition || body != clause.Body)
            {
                mebbeBuilder.Add(new BoundMebbeClause(cond, body, syntax: clause.Syntax));
                mebbeChanged = true;
            }
            else
            {
                mebbeBuilder.Add(clause);
            }
        }

        var elseBlock = node.ElseBlock is not null ? RewriteBlockStatement(node.ElseBlock) : null;

        if (thenBlock == node.ThenBlock && !mebbeChanged && elseBlock == node.ElseBlock)
            return node;

        return new BoundIfStatement(thenBlock, mebbeBuilder.MoveToImmutable(), elseBlock, syntax: node.Syntax);
    }

    private BoundSwitchStatement RewriteSwitchStatement(BoundSwitchStatement node)
    {
        var omgBuilder = ImmutableArray.CreateBuilder<BoundOmgClause>(node.OmgClauses.Length);
        var changed = false;
        foreach (var clause in node.OmgClauses)
        {
            var body = RewriteBlockStatement(clause.Body);
            if (body != clause.Body)
            {
                omgBuilder.Add(new BoundOmgClause(clause.LiteralValue, body, syntax: clause.Syntax));
                changed = true;
            }
            else
            {
                omgBuilder.Add(clause);
            }
        }

        var defaultBlock = node.DefaultBlock is not null ? RewriteBlockStatement(node.DefaultBlock) : null;

        if (!changed && defaultBlock == node.DefaultBlock)
            return node;

        return new BoundSwitchStatement(omgBuilder.MoveToImmutable(), defaultBlock, syntax: node.Syntax);
    }

    private BoundLoopStatement RewriteLoopStatement(BoundLoopStatement node)
    {
        var body = RewriteBlockStatement(node.Body);
        var condition = node.Condition is not null ? RewriteExpression(node.Condition) : null;

        if (body == node.Body && condition == node.Condition)
            return node;

        return new BoundLoopStatement(
            node.Label, node.Operation, node.Variable,
            node.IsTil, condition, body, syntax: node.Syntax);
    }

    private BoundFunctionDeclaration RewriteFunctionDeclaration(BoundFunctionDeclaration node)
    {
        var body = RewriteBlockStatement(node.Body);
        if (body == node.Body)
            return node;

        return new BoundFunctionDeclaration(node.Function, body, syntax: node.Syntax);
    }

    private BoundReturnStatement RewriteReturnStatement(BoundReturnStatement node)
    {
        var expression = RewriteExpression(node.Expression);
        if (expression == node.Expression)
            return node;

        return new BoundReturnStatement(expression, syntax: node.Syntax);
    }

    private BoundCastStatement RewriteCastStatement(BoundCastStatement node)
    {
        // CastStatement is in-place cast — no sub-expression to rewrite
        return node;
    }

    private BoundUnaryExpression RewriteUnaryExpression(BoundUnaryExpression node)
    {
        var operand = RewriteExpression(node.Operand);
        if (operand == node.Operand)
            return node;

        return new BoundUnaryExpression(node.OperatorKind, operand, syntax: node.Syntax);
    }

    private BoundBinaryExpression RewriteBinaryExpression(BoundBinaryExpression node)
    {
        var left = RewriteExpression(node.Left);
        var right = RewriteExpression(node.Right);
        if (left == node.Left && right == node.Right)
            return node;

        return new BoundBinaryExpression(node.OperatorKind, left, right, syntax: node.Syntax);
    }

    private BoundSmooshExpression RewriteSmooshExpression(BoundSmooshExpression node)
    {
        var builder = ImmutableArray.CreateBuilder<BoundExpression>(node.Operands.Length);
        var changed = false;
        foreach (var op in node.Operands)
        {
            var rewritten = RewriteExpression(op);
            builder.Add(rewritten);
            if (rewritten != op)
                changed = true;
        }

        if (!changed)
            return node;

        return new BoundSmooshExpression(builder.MoveToImmutable(), syntax: node.Syntax);
    }

    private BoundAllOfExpression RewriteAllOfExpression(BoundAllOfExpression node)
    {
        var builder = ImmutableArray.CreateBuilder<BoundExpression>(node.Operands.Length);
        var changed = false;
        foreach (var op in node.Operands)
        {
            var rewritten = RewriteExpression(op);
            builder.Add(rewritten);
            if (rewritten != op)
                changed = true;
        }

        if (!changed)
            return node;

        return new BoundAllOfExpression(builder.MoveToImmutable(), syntax: node.Syntax);
    }

    private BoundAnyOfExpression RewriteAnyOfExpression(BoundAnyOfExpression node)
    {
        var builder = ImmutableArray.CreateBuilder<BoundExpression>(node.Operands.Length);
        var changed = false;
        foreach (var op in node.Operands)
        {
            var rewritten = RewriteExpression(op);
            builder.Add(rewritten);
            if (rewritten != op)
                changed = true;
        }

        if (!changed)
            return node;

        return new BoundAnyOfExpression(builder.MoveToImmutable(), syntax: node.Syntax);
    }

    private BoundComparisonExpression RewriteComparisonExpression(BoundComparisonExpression node)
    {
        var left = RewriteExpression(node.Left);
        var right = RewriteExpression(node.Right);
        if (left == node.Left && right == node.Right)
            return node;

        return new BoundComparisonExpression(node.IsEquality, left, right, syntax: node.Syntax);
    }

    private BoundExpression RewriteCastExpression(BoundCastExpression node)
    {
        var operand = RewriteExpression(node.Operand);
        if (operand == node.Operand)
            return node;

        return new BoundCastExpression(operand, node.TargetType, syntax: node.Syntax);
    }

    private BoundExpression RewriteFunctionCallExpression(BoundFunctionCallExpression node)
    {
        var builder = ImmutableArray.CreateBuilder<BoundExpression>(node.Arguments.Length);
        var changed = false;
        foreach (var arg in node.Arguments)
        {
            var rewritten = RewriteExpression(arg);
            builder.Add(rewritten);
            if (rewritten != arg)
                changed = true;
        }

        if (!changed)
            return node;

        return new BoundFunctionCallExpression(node.Function, builder.MoveToImmutable(), syntax: node.Syntax);
    }
}
