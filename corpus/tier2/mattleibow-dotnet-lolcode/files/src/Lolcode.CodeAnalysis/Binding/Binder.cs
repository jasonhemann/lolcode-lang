using System.Collections.Immutable;
using Lolcode.CodeAnalysis.BoundTree;
using Lolcode.CodeAnalysis.Symbols;
using Lolcode.CodeAnalysis.Syntax;
using Lolcode.CodeAnalysis.Text;

namespace Lolcode.CodeAnalysis.Binding;

/// <summary>
/// Performs semantic analysis on a parsed syntax tree, producing a bound tree.
/// Resolves variable references, validates control flow, and checks types.
/// </summary>
internal sealed class Binder
{
    private readonly DiagnosticBag _diagnostics = new();
    private readonly SourceText _text;
    private BoundScope _scope;
    private readonly Stack<ControlFlowContext> _contextStack = new();

    /// <summary>
    /// Gets the diagnostics produced during binding.
    /// </summary>
    public IEnumerable<Diagnostic> Diagnostics => _diagnostics;

    /// <summary>
    /// Creates a new binder for the given source text.
    /// </summary>
    public Binder(SourceText text)
    {
        _text = text;
        _scope = new BoundScope();
    }

    /// <summary>
    /// Binds a compilation unit to a <see cref="BoundBlockStatement"/>.
    /// </summary>
    public BoundBlockStatement BindCompilationUnit(CompilationUnitSyntax compilationUnit)
    {
        // First pass: collect all function declarations
        CollectFunctions(compilationUnit.Program.Statements);

        // Second pass: bind all statements
        return BindBlock(compilationUnit.Program.Statements);
    }

    private void CollectFunctions(ImmutableArray<StatementSyntax> statements)
    {
        foreach (var statement in statements)
        {
            if (statement is FunctionDeclarationSyntax funcDecl)
            {
                string name = funcDecl.NameToken.Text;
                var parameters = funcDecl.Parameters.Select((p, i) =>
                    new ParameterSymbol(p.Text, i)).ToImmutableArray();

                var function = new FunctionSymbol(name, parameters);

                if (!_scope.TryDeclareFunction(function))
                {
                    var location = TextLocation.FromSpan(_text, funcDecl.NameToken.Span);
                    _diagnostics.ReportFunctionAlreadyDeclared(location, name);
                }
            }
        }
    }

    private BoundBlockStatement BindBlock(ImmutableArray<StatementSyntax> statements)
    {
        var boundStatements = ImmutableArray.CreateBuilder<BoundStatement>();

        foreach (var statement in statements)
        {
            var bound = BindStatement(statement);
            if (bound != null)
                boundStatements.Add(bound);
        }

        return new BoundBlockStatement(boundStatements.ToImmutable());
    }

    private BoundStatement? BindStatement(StatementSyntax statement)
    {
        return statement switch
        {
            VariableDeclarationSyntax s => BindVariableDeclaration(s),
            AssignmentStatementSyntax s => BindAssignment(s),
            VisibleStatementSyntax s => BindVisible(s),
            GimmehStatementSyntax s => BindGimmeh(s),
            ExpressionStatementSyntax s => BindExpressionStatement(s),
            IfStatementSyntax s => BindIf(s),
            SwitchStatementSyntax s => BindSwitch(s),
            LoopStatementSyntax s => BindLoop(s),
            GtfoStatementSyntax s => BindGtfo(s),
            FunctionDeclarationSyntax s => BindFunctionDeclaration(s),
            ReturnStatementSyntax s => BindReturn(s),
            CastStatementSyntax s => BindCastStatement(s),
            _ => null,
        };
    }

    private BoundVariableDeclaration BindVariableDeclaration(VariableDeclarationSyntax syntax)
    {
        string name = syntax.NameToken.Text;
        var variable = new VariableSymbol(name);

        if (!_scope.TryDeclareVariable(variable))
        {
            var location = TextLocation.FromSpan(_text, syntax.NameToken.Span);
            _diagnostics.ReportVariableAlreadyDeclared(location, name);
        }

        BoundExpression? initializer = null;
        if (syntax.Initializer != null)
            initializer = BindExpression(syntax.Initializer);

        return new BoundVariableDeclaration(variable, initializer, syntax: syntax);
    }

    private BoundAssignment BindAssignment(AssignmentStatementSyntax syntax)
    {
        string name = syntax.NameToken.Text;

        if (!_scope.TryLookupVariable(name, out var variable))
        {
            var location = TextLocation.FromSpan(_text, syntax.NameToken.Span);
            _diagnostics.ReportUndeclaredVariable(location, name);
            variable = new VariableSymbol(name);
        }

        var expression = BindExpression(syntax.Expression);
        return new BoundAssignment(variable, expression, syntax: syntax);
    }

    private BoundVisibleStatement BindVisible(VisibleStatementSyntax syntax)
    {
        var args = syntax.Arguments.Select(BindExpression).ToImmutableArray();
        return new BoundVisibleStatement(args, syntax.SuppressNewline, syntax: syntax);
    }

    private BoundGimmehStatement BindGimmeh(GimmehStatementSyntax syntax)
    {
        string name = syntax.NameToken.Text;
        if (!_scope.TryLookupVariable(name, out var variable))
        {
            var location = TextLocation.FromSpan(_text, syntax.NameToken.Span);
            _diagnostics.ReportUndeclaredVariable(location, name);
            variable = new VariableSymbol(name);
        }
        return new BoundGimmehStatement(variable, syntax: syntax);
    }

    private BoundExpressionStatement BindExpressionStatement(ExpressionStatementSyntax syntax)
    {
        var expression = BindExpression(syntax.Expression);
        return new BoundExpressionStatement(expression, syntax: syntax);
    }

    private BoundIfStatement BindIf(IfStatementSyntax syntax)
    {
        var thenBlock = BindBlock(syntax.YaRlyBody.Statements);

        var mebbeClauses = syntax.MebbeClauses.Select(m =>
        {
            var condition = BindExpression(m.Condition);
            var body = BindBlock(m.Body.Statements);
            return new BoundMebbeClause(condition, body, syntax: m);
        }).ToImmutableArray();

        BoundBlockStatement? elseBlock = null;
        if (syntax.NoWaiBody != null)
            elseBlock = BindBlock(syntax.NoWaiBody.Statements);

        return new BoundIfStatement(thenBlock, mebbeClauses, elseBlock, syntax: syntax);
    }

    private BoundSwitchStatement BindSwitch(SwitchStatementSyntax syntax)
    {
        var seenValues = new HashSet<string>();
        var omgClauses = ImmutableArray.CreateBuilder<BoundOmgClause>();

        _contextStack.Push(ControlFlowContext.Switch);

        foreach (var clause in syntax.OmgClauses)
        {
            var value = BindExpression(clause.Value);

            // Validate literal-only and uniqueness
            if (value is BoundLiteralExpression lit)
            {
                string key = lit.Value?.ToString() ?? "NOOB";
                if (!seenValues.Add(key))
                {
                    var location = TextLocation.FromSpan(_text, clause.Value.Span);
                    _diagnostics.ReportDuplicateOmgLiteral(location, key);
                }
            }
            else
            {
                var location = TextLocation.FromSpan(_text, clause.Value.Span);
                _diagnostics.ReportOmgRequiresLiteral(location);
            }

            var body = BindBlock(clause.Body.Statements);
            object? literalValue = value is BoundLiteralExpression l ? l.Value : null;
            omgClauses.Add(new BoundOmgClause(literalValue, body, syntax: clause));
        }

        BoundBlockStatement? defaultBlock = null;
        if (syntax.OmgwtfBody != null)
            defaultBlock = BindBlock(syntax.OmgwtfBody.Statements);

        _contextStack.Pop();

        return new BoundSwitchStatement(omgClauses.ToImmutable(), defaultBlock, syntax: syntax);
    }

    private BoundLoopStatement BindLoop(LoopStatementSyntax syntax)
    {
        string label = syntax.LabelToken.Text;
        string? operation = syntax.OperationToken?.Text;
        string? variableName = syntax.VariableToken?.Text;
        bool? isTil = null;
        BoundExpression? condition = null;
        VariableSymbol? loopVariable = null;

        // Loop variable is local to the loop — declare in scope
        if (variableName != null)
        {
            loopVariable = new VariableSymbol(variableName);
            _scope.TryDeclareVariable(loopVariable);
        }

        if (syntax.ConditionKeyword != null)
        {
            isTil = syntax.ConditionKeyword.Kind == SyntaxKind.TilKeyword;
            condition = BindExpression(syntax.Condition!);
        }

        _contextStack.Push(ControlFlowContext.Loop);
        var body = BindBlock(syntax.Body.Statements);
        _contextStack.Pop();

        return new BoundLoopStatement(label, operation, loopVariable, isTil, condition, body, syntax: syntax);
    }

    private BoundGtfoStatement BindGtfo(GtfoStatementSyntax syntax)
    {
        ControlFlowContext context;
        if (_contextStack.Count == 0)
        {
            var location = TextLocation.FromSpan(_text, syntax.Keyword.Span);
            _diagnostics.ReportInvalidGtfo(location);
            context = ControlFlowContext.None;
        }
        else
        {
            context = _contextStack.Peek();
        }

        return new BoundGtfoStatement(context, syntax: syntax);
    }

    private BoundFunctionDeclaration BindFunctionDeclaration(FunctionDeclarationSyntax syntax)
    {
        string name = syntax.NameToken.Text;

        if (!_scope.TryLookupFunction(name, out var function))
        {
            // Should have been collected in first pass; create a placeholder
            var parameters = syntax.Parameters.Select((p, i) =>
                new ParameterSymbol(p.Text, i)).ToImmutableArray();
            function = new FunctionSymbol(name, parameters);
        }

        // Create a new scope for the function (chained to global for function visibility)
        var outerScope = _scope;
        _scope = new BoundScope(outerScope);

        foreach (var param in function.Parameters)
            _scope.TryDeclareVariable(new VariableSymbol(param.Name));

        _contextStack.Push(ControlFlowContext.Function);
        var body = BindBlock(syntax.Body.Statements);
        _contextStack.Pop();

        // Restore outer scope
        _scope = outerScope;

        return new BoundFunctionDeclaration(function, body, syntax: syntax);
    }

    private BoundReturnStatement BindReturn(ReturnStatementSyntax syntax)
    {
        if (!_contextStack.Contains(ControlFlowContext.Function))
        {
            var location = TextLocation.FromSpan(_text, syntax.Keyword.Span);
            _diagnostics.ReportInvalidFoundYr(location);
        }

        var expression = BindExpression(syntax.Expression);
        return new BoundReturnStatement(expression, syntax: syntax);
    }

    private BoundCastStatement BindCastStatement(CastStatementSyntax syntax)
    {
        string name = syntax.NameToken.Text;
        if (!_scope.TryLookupVariable(name, out var variable))
        {
            var location = TextLocation.FromSpan(_text, syntax.NameToken.Span);
            _diagnostics.ReportUndeclaredVariable(location, name);
            variable = new VariableSymbol(name);
        }

        string targetType = syntax.TypeToken.Text;
        return new BoundCastStatement(variable, targetType, syntax: syntax);
    }

    private BoundExpression BindExpression(ExpressionSyntax syntax)
    {
        return syntax switch
        {
            LiteralExpressionSyntax s => BindLiteral(s),
            VariableExpressionSyntax s => BindVariableExpression(s),
            UnaryExpressionSyntax s => BindUnary(s),
            BinaryExpressionSyntax s => BindBinary(s),
            SmooshExpressionSyntax s => BindSmoosh(s),
            AllOfExpressionSyntax s => BindAllOf(s),
            AnyOfExpressionSyntax s => BindAnyOf(s),
            ComparisonExpressionSyntax s => new BoundComparisonExpression(true, BindExpression(s.Left), BindExpression(s.Right), syntax: s),
            DiffrintExpressionSyntax s => new BoundComparisonExpression(false, BindExpression(s.Left), BindExpression(s.Right), syntax: s),
            CastExpressionSyntax s => new BoundCastExpression(BindExpression(s.Operand), s.TypeToken.Text, syntax: s),
            FunctionCallExpressionSyntax s => BindFunctionCall(s),
            ItExpressionSyntax s => new BoundItExpression(syntax: s),
            _ => new BoundLiteralExpression(null),
        };
    }

    private BoundExpression BindLiteral(LiteralExpressionSyntax syntax)
    {
        // Check for string interpolation :{varname}
        if (syntax.Value is string strValue && strValue.Contains(":{"))
        {
            return BindInterpolatedString(strValue);
        }
        return new BoundLiteralExpression(syntax.Value, syntax: syntax);
    }

    private BoundExpression BindInterpolatedString(string template)
    {
        var parts = new List<BoundExpression>();
        int pos = 0;

        while (pos < template.Length)
        {
            int nextInterp = template.IndexOf(":{", pos, StringComparison.Ordinal);
            if (nextInterp < 0)
            {
                parts.Add(new BoundLiteralExpression(template[pos..]));
                break;
            }

            if (nextInterp > pos)
            {
                parts.Add(new BoundLiteralExpression(template[pos..nextInterp]));
            }

            int closingBrace = template.IndexOf('}', nextInterp + 2);
            if (closingBrace < 0)
            {
                parts.Add(new BoundLiteralExpression(template[nextInterp..]));
                break;
            }

            string varName = template[(nextInterp + 2)..closingBrace];

            if (!_scope.TryLookupVariable(varName, out var variable))
            {
                parts.Add(new BoundLiteralExpression($":{{{varName}}}"));
            }
            else
            {
                parts.Add(new BoundVariableExpression(variable));
            }

            pos = closingBrace + 1;
        }

        if (parts.Count == 1)
            return parts[0];

        return new BoundSmooshExpression(parts.ToImmutableArray());
    }

    private BoundExpression BindVariableExpression(VariableExpressionSyntax syntax)
    {
        string name = syntax.NameToken.Text;
        if (!_scope.TryLookupVariable(name, out var variable))
        {
            var location = TextLocation.FromSpan(_text, syntax.NameToken.Span);
            _diagnostics.ReportUndeclaredVariable(location, name);
            variable = new VariableSymbol(name);
        }
        return new BoundVariableExpression(variable, syntax: syntax);
    }

    private BoundUnaryExpression BindUnary(UnaryExpressionSyntax syntax)
    {
        var operand = BindExpression(syntax.Operand);
        return new BoundUnaryExpression(BoundUnaryOperatorKind.LogicalNot, operand, syntax: syntax);
    }

    private BoundBinaryExpression BindBinary(BinaryExpressionSyntax syntax)
    {
        string op = syntax.OperatorToken.Text;
        var left = BindExpression(syntax.Left);
        var right = BindExpression(syntax.Right);

        var kind = op switch
        {
            "SUM" => BoundBinaryOperatorKind.Addition,
            "DIFF" => BoundBinaryOperatorKind.Subtraction,
            "PRODUKT" => BoundBinaryOperatorKind.Multiplication,
            "QUOSHUNT" => BoundBinaryOperatorKind.Division,
            "MOD" => BoundBinaryOperatorKind.Modulo,
            "BIGGR" => BoundBinaryOperatorKind.Maximum,
            "SMALLR" => BoundBinaryOperatorKind.Minimum,
            "BOTH" => BoundBinaryOperatorKind.LogicalAnd,
            "EITHER" => BoundBinaryOperatorKind.LogicalOr,
            "WON" => BoundBinaryOperatorKind.LogicalXor,
            _ => throw new InvalidOperationException($"Unknown operator: {op}")
        };

        return new BoundBinaryExpression(kind, left, right, syntax: syntax);
    }

    private BoundSmooshExpression BindSmoosh(SmooshExpressionSyntax syntax)
    {
        var operands = syntax.Operands.Select(BindExpression).ToImmutableArray();
        return new BoundSmooshExpression(operands, syntax: syntax);
    }

    private BoundAllOfExpression BindAllOf(AllOfExpressionSyntax syntax)
    {
        var operands = syntax.Operands.Select(BindExpression).ToImmutableArray();
        return new BoundAllOfExpression(operands, syntax: syntax);
    }

    private BoundAnyOfExpression BindAnyOf(AnyOfExpressionSyntax syntax)
    {
        var operands = syntax.Operands.Select(BindExpression).ToImmutableArray();
        return new BoundAnyOfExpression(operands, syntax: syntax);
    }

    private BoundFunctionCallExpression BindFunctionCall(FunctionCallExpressionSyntax syntax)
    {
        string name = syntax.NameToken.Text;

        if (!_scope.TryLookupFunction(name, out var function))
        {
            var location = TextLocation.FromSpan(_text, syntax.NameToken.Span);
            _diagnostics.ReportUndefinedFunction(location, name);
            function = new FunctionSymbol(name, ImmutableArray<ParameterSymbol>.Empty);
        }
        else
        {
            if (syntax.Arguments.Length != function.Parameters.Length)
            {
                var location = TextLocation.FromSpan(_text, syntax.NameToken.Span);
                _diagnostics.ReportWrongArgumentCount(location, name, function.Parameters.Length, syntax.Arguments.Length);
            }
        }

        var args = syntax.Arguments.Select(BindExpression).ToImmutableArray();
        return new BoundFunctionCallExpression(function, args, syntax: syntax);
    }
}
