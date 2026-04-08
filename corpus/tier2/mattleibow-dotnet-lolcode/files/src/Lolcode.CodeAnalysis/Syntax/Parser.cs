using System.Collections.Immutable;
using Lolcode.CodeAnalysis.Text;

namespace Lolcode.CodeAnalysis.Syntax;

/// <summary>
/// Recursive descent parser for LOLCODE 1.2.
/// Produces a <see cref="CompilationUnitSyntax"/> from a list of tokens.
/// </summary>
internal sealed class Parser
{
    private readonly IReadOnlyList<SyntaxToken> _tokens;
    private readonly SourceText _text;
    private readonly DiagnosticBag _diagnostics = new();
    private int _position;

    /// <summary>
    /// Gets the diagnostics produced during parsing.
    /// </summary>
    public IEnumerable<Diagnostic> Diagnostics => _diagnostics;

    /// <summary>
    /// Creates a new parser for the given tokens and source text.
    /// </summary>
    public Parser(IReadOnlyList<SyntaxToken> tokens, SourceText text)
    {
        _tokens = tokens;
        _text = text;
    }

    private SyntaxToken Current => Peek(0);

    private SyntaxToken Peek(int offset)
    {
        int index = _position + offset;
        if (index >= _tokens.Count)
            return _tokens[^1]; // EOF
        return _tokens[index];
    }

    private SyntaxToken Advance()
    {
        var current = Current;
        _position++;
        return current;
    }

    private SyntaxToken Match(SyntaxKind kind)
    {
        if (Current.Kind == kind)
            return Advance();

        var location = GetCurrentLocation();
        _diagnostics.ReportUnexpectedToken(location, Current.Text, kind.ToString());
        return new SyntaxToken(kind, Current.Position, "", null);
    }

    private bool Check(SyntaxKind kind) => Current.Kind == kind;

    private bool CheckText(int offset, string text) => Peek(offset).Text == text;

    private SyntaxToken MatchIdentifier(string expectedText)
    {
        if (Current.Kind == SyntaxKind.IdentifierToken && Current.Text == expectedText)
            return Advance();

        var location = GetCurrentLocation();
        _diagnostics.ReportUnexpectedToken(location, Current.Text, expectedText);
        return new SyntaxToken(SyntaxKind.IdentifierToken, Current.Position, "", null);
    }

    private bool CheckSequence(params SyntaxKind[] kinds)
    {
        for (int i = 0; i < kinds.Length; i++)
        {
            if (Peek(i).Kind != kinds[i])
                return false;
        }
        return true;
    }

    private void SkipNewlines()
    {
        while (Current.Kind == SyntaxKind.EndOfLineToken)
            _position++;
    }

    private void ExpectEndOfLine()
    {
        if (Current.Kind == SyntaxKind.EndOfLineToken || Current.Kind == SyntaxKind.EndOfFileToken)
        {
            if (Current.Kind == SyntaxKind.EndOfLineToken)
                _position++;
        }
        else
        {
            var location = GetCurrentLocation();
            _diagnostics.ReportExpectedToken(location, "end of line");
        }
    }

    private TextLocation GetCurrentLocation()
    {
        return TextLocation.FromSpan(_text, Current.Span);
    }

    /// <summary>
    /// Parses the token stream into a <see cref="CompilationUnitSyntax"/>.
    /// </summary>
    public CompilationUnitSyntax Parse()
    {
        SkipNewlines();
        var program = ParseProgram();
        var eof = Match(SyntaxKind.EndOfFileToken);
        return new CompilationUnitSyntax(program, eof);
    }

    private ProgramStatementSyntax ParseProgram()
    {
        var hai = Match(SyntaxKind.HaiKeyword);

        // Optional version number
        SyntaxToken? version = null;
        if (Current.Kind == SyntaxKind.NumbarLiteralToken || Current.Kind == SyntaxKind.NumbrLiteralToken)
        {
            version = Advance();
        }

        ExpectEndOfLine();
        SkipNewlines();

        var statements = ParseStatements(isTopLevel: true);

        var kthxbye = Match(SyntaxKind.KthxbyeKeyword);
        // Skip any trailing newlines after KTHXBYE
        while (Current.Kind == SyntaxKind.EndOfLineToken)
            _position++;

        return new ProgramStatementSyntax(hai, version, statements, kthxbye);
    }

    private ImmutableArray<StatementSyntax> ParseStatements(
        bool isTopLevel = false,
        bool inYaRly = false,
        bool inNoWai = false,
        bool inMebbe = false,
        bool inOmg = false,
        bool inOmgwtf = false,
        bool inLoop = false,
        bool inFunction = false)
    {
        var statements = ImmutableArray.CreateBuilder<StatementSyntax>();

        while (true)
        {
            SkipNewlines();

            if (Current.Kind == SyntaxKind.EndOfFileToken)
                break;

            // Termination conditions based on context
            if (isTopLevel && Current.Kind == SyntaxKind.KthxbyeKeyword)
                break;

            if ((inYaRly || inMebbe) &&
                (Current.Kind == SyntaxKind.MebbeKeyword ||
                 (Current.Kind == SyntaxKind.NoKeyword && Peek(1).Kind == SyntaxKind.WaiKeyword) ||
                 Current.Kind == SyntaxKind.OicKeyword))
                break;

            if (inNoWai && Current.Kind == SyntaxKind.OicKeyword)
                break;

            if (inOmg &&
                (Current.Kind == SyntaxKind.OmgKeyword ||
                 Current.Kind == SyntaxKind.OmgwtfKeyword ||
                 Current.Kind == SyntaxKind.OicKeyword))
                break;

            if (inOmgwtf && Current.Kind == SyntaxKind.OicKeyword)
                break;

            if (inLoop && CheckSequence(SyntaxKind.ImKeyword, SyntaxKind.OuttaKeyword))
                break;

            if (inFunction && CheckSequence(SyntaxKind.IfKeyword, SyntaxKind.UKeyword))
                break;

            var statement = ParseStatement();
            if (statement != null)
                statements.Add(statement);
        }

        return statements.ToImmutable();
    }

    private StatementSyntax? ParseStatement()
    {
        StatementSyntax? result = Current.Kind switch
        {
            // I HAS A / I IZ (as statement)
            SyntaxKind.IKeyword when Peek(1).Kind == SyntaxKind.HasKeyword => ParseVariableDeclaration(),
            SyntaxKind.IKeyword when Peek(1).Kind == SyntaxKind.IzKeyword => ParseExpressionOrFunctionCallStatement(),

            // Variable assignment: <identifier> R <expr>
            // Variable cast: <identifier> IS NOW A <type>
            SyntaxKind.IdentifierToken when Peek(1).Kind == SyntaxKind.RKeyword => ParseAssignment(),
            SyntaxKind.IdentifierToken when Peek(1).Kind == SyntaxKind.IsKeyword => ParseCastStatement(),

            // IT R <expr> or IT IS NOW A <type>
            SyntaxKind.ItKeyword when Peek(1).Kind == SyntaxKind.RKeyword => ParseAssignment(),
            SyntaxKind.ItKeyword when Peek(1).Kind == SyntaxKind.IsKeyword => ParseCastStatement(),

            SyntaxKind.VisibleKeyword => ParseVisible(),
            SyntaxKind.GimmehKeyword => ParseGimmeh(),

            // O RLY?
            SyntaxKind.OKeyword when Peek(1).Kind == SyntaxKind.RlyKeyword => ParseIf(),

            // WTF?
            SyntaxKind.WtfKeyword => ParseSwitch(),

            // IM IN YR
            SyntaxKind.ImKeyword when Peek(1).Kind == SyntaxKind.InKeyword => ParseLoop(),

            SyntaxKind.GtfoKeyword => ParseGtfo(),

            // HOW IZ I
            SyntaxKind.HowKeyword when Peek(1).Kind == SyntaxKind.IzKeyword => ParseFunctionDeclaration(),

            // FOUND YR
            SyntaxKind.FoundKeyword when Peek(1).Kind == SyntaxKind.YrKeyword => ParseReturn(),

            // BTW comment (should have been filtered by lexer, but handle gracefully)
            _ => ParseExpressionStatement(),
        };

        // Each statement should end with a newline (or EOF)
        if (result != null && Current.Kind != SyntaxKind.EndOfFileToken)
        {
            if (Current.Kind == SyntaxKind.EndOfLineToken)
                _position++;
        }

        return result;
    }

    private VariableDeclarationSyntax ParseVariableDeclaration()
    {
        Match(SyntaxKind.IKeyword);  // I
        Match(SyntaxKind.HasKeyword); // HAS
        Match(SyntaxKind.AKeyword);   // A

        var name = Match(SyntaxKind.IdentifierToken);

        ExpressionSyntax? initializer = null;
        if (Current.Kind == SyntaxKind.ItzKeyword)
        {
            Advance(); // ITZ

            // ITZ A <type> is a special case for typed initialization
            // For now, treat as expression
            initializer = ParseExpression();
        }

        return new VariableDeclarationSyntax(name, initializer);
    }

    private AssignmentStatementSyntax ParseAssignment()
    {
        var name = Advance(); // identifier or IT
        Match(SyntaxKind.RKeyword); // R
        var expr = ParseExpression();
        return new AssignmentStatementSyntax(name, expr);
    }

    private CastStatementSyntax ParseCastStatement()
    {
        var name = Advance(); // identifier or IT
        Match(SyntaxKind.IsKeyword);  // IS
        Match(SyntaxKind.NowKeyword); // NOW
        Match(SyntaxKind.AKeyword);   // A
        var type = ParseTypeKeyword();
        return new CastStatementSyntax(name, type);
    }

    private SyntaxToken ParseTypeKeyword()
    {
        if (Current.Kind is SyntaxKind.TroofKeyword or SyntaxKind.NumbrKeyword
            or SyntaxKind.NumbarKeyword or SyntaxKind.YarnKeyword or SyntaxKind.NoobKeyword)
        {
            return Advance();
        }

        var location = GetCurrentLocation();
        _diagnostics.ReportExpectedToken(location, "type keyword (TROOF, NUMBR, NUMBAR, YARN, or NOOB)");
        return new SyntaxToken(SyntaxKind.BadToken, Current.Position, Current.Text);
    }

    private VisibleStatementSyntax ParseVisible()
    {
        var keyword = Advance(); // VISIBLE
        var args = ImmutableArray.CreateBuilder<ExpressionSyntax>();
        bool suppressNewline = false;

        // Parse arguments until end of line or !
        while (Current.Kind != SyntaxKind.EndOfLineToken &&
               Current.Kind != SyntaxKind.EndOfFileToken)
        {
            if (Current.Kind == SyntaxKind.ExclamationToken)
            {
                suppressNewline = true;
                Advance();
                break;
            }

            // Skip optional AN between arguments
            if (args.Count > 0 && Current.Kind == SyntaxKind.AnKeyword)
                Advance();

            // Check again for end/exclamation after skipping AN
            if (Current.Kind == SyntaxKind.EndOfLineToken ||
                Current.Kind == SyntaxKind.EndOfFileToken)
                break;

            if (Current.Kind == SyntaxKind.ExclamationToken)
            {
                suppressNewline = true;
                Advance();
                break;
            }

            args.Add(ParseExpression());
        }

        return new VisibleStatementSyntax(keyword, args.ToImmutable(), suppressNewline);
    }

    private GimmehStatementSyntax ParseGimmeh()
    {
        var keyword = Advance(); // GIMMEH
        var name = Match(SyntaxKind.IdentifierToken);
        return new GimmehStatementSyntax(keyword, name);
    }

    private IfStatementSyntax ParseIf()
    {
        var o = Advance(); // O
        Match(SyntaxKind.RlyKeyword); // RLY?
        ExpectEndOfLine();
        SkipNewlines();

        // YA RLY (note: RLY here has no ?, so it's an identifier)
        Match(SyntaxKind.YaKeyword);
        MatchIdentifier("RLY"); // RLY without ?
        ExpectEndOfLine();

        var yaRlyStatements = ParseStatements(inYaRly: true);
        var yaRlyBody = new BlockStatementSyntax(yaRlyStatements);

        // MEBBE clauses
        var mebbeClauses = ImmutableArray.CreateBuilder<MebbeClauseSyntax>();
        while (Current.Kind == SyntaxKind.MebbeKeyword)
        {
            var mebbeKeyword = Advance();
            var condition = ParseExpression();
            ExpectEndOfLine();
            var mebbeStatements = ParseStatements(inMebbe: true);
            var mebbeBody = new BlockStatementSyntax(mebbeStatements);
            mebbeClauses.Add(new MebbeClauseSyntax(mebbeKeyword, condition, mebbeBody));
        }

        // NO WAI (optional)
        BlockStatementSyntax? noWaiBody = null;
        if (Current.Kind == SyntaxKind.NoKeyword && Peek(1).Kind == SyntaxKind.WaiKeyword)
        {
            Advance(); // NO
            Advance(); // WAI
            ExpectEndOfLine();
            var noWaiStatements = ParseStatements(inNoWai: true);
            noWaiBody = new BlockStatementSyntax(noWaiStatements);
        }

        var oic = Match(SyntaxKind.OicKeyword);
        return new IfStatementSyntax(o, yaRlyBody, mebbeClauses.ToImmutable(), noWaiBody, oic);
    }

    private SwitchStatementSyntax ParseSwitch()
    {
        var wtf = Advance(); // WTF?
        ExpectEndOfLine();
        SkipNewlines();

        var omgClauses = ImmutableArray.CreateBuilder<OmgClauseSyntax>();

        while (Current.Kind == SyntaxKind.OmgKeyword)
        {
            var omgKeyword = Advance();
            var value = ParseExpression();
            ExpectEndOfLine();
            var omgStatements = ParseStatements(inOmg: true);
            var omgBody = new BlockStatementSyntax(omgStatements);
            omgClauses.Add(new OmgClauseSyntax(omgKeyword, value, omgBody));
        }

        // OMGWTF (optional default)
        BlockStatementSyntax? omgwtfBody = null;
        if (Current.Kind == SyntaxKind.OmgwtfKeyword)
        {
            Advance(); // OMGWTF
            ExpectEndOfLine();
            var omgwtfStatements = ParseStatements(inOmgwtf: true);
            omgwtfBody = new BlockStatementSyntax(omgwtfStatements);
        }

        var oic = Match(SyntaxKind.OicKeyword);
        return new SwitchStatementSyntax(wtf, omgClauses.ToImmutable(), omgwtfBody, oic);
    }

    private LoopStatementSyntax ParseLoop()
    {
        var im = Advance(); // IM
        Match(SyntaxKind.InKeyword); // IN
        Match(SyntaxKind.YrKeyword); // YR
        var label = Match(SyntaxKind.IdentifierToken);

        SyntaxToken? operation = null;
        SyntaxToken? variable = null;
        SyntaxToken? conditionKeyword = null;
        ExpressionSyntax? condition = null;

        // Optional: UPPIN/NERFIN YR <var> [TIL|WILE <expr>]
        if (Current.Kind == SyntaxKind.UppinKeyword || Current.Kind == SyntaxKind.NerfinKeyword ||
            Current.Kind == SyntaxKind.IdentifierToken)
        {
            operation = Advance();
            Match(SyntaxKind.YrKeyword); // YR
            variable = Match(SyntaxKind.IdentifierToken);

            if (Current.Kind == SyntaxKind.TilKeyword || Current.Kind == SyntaxKind.WileKeyword)
            {
                conditionKeyword = Advance();
                condition = ParseExpression();
            }
        }

        ExpectEndOfLine();
        var bodyStatements = ParseStatements(inLoop: true);
        var body = new BlockStatementSyntax(bodyStatements);

        Match(SyntaxKind.ImKeyword);    // IM
        Match(SyntaxKind.OuttaKeyword); // OUTTA
        Match(SyntaxKind.YrKeyword);    // YR
        var endLabel = Match(SyntaxKind.IdentifierToken);

        return new LoopStatementSyntax(
            im, label, operation, variable, conditionKeyword, condition, body, im, endLabel);
    }

    private GtfoStatementSyntax ParseGtfo()
    {
        var keyword = Advance();
        return new GtfoStatementSyntax(keyword);
    }

    private FunctionDeclarationSyntax ParseFunctionDeclaration()
    {
        Match(SyntaxKind.HowKeyword); // HOW
        Match(SyntaxKind.IzKeyword);  // IZ
        Match(SyntaxKind.IKeyword);   // I

        var name = Match(SyntaxKind.IdentifierToken);
        var parameters = ImmutableArray.CreateBuilder<SyntaxToken>();

        // Optional parameters: YR <param> [AN YR <param>]*
        if (Current.Kind == SyntaxKind.YrKeyword)
        {
            Advance(); // YR
            parameters.Add(Match(SyntaxKind.IdentifierToken));

            while (Current.Kind == SyntaxKind.AnKeyword && Peek(1).Kind == SyntaxKind.YrKeyword)
            {
                Advance(); // AN
                Advance(); // YR
                parameters.Add(Match(SyntaxKind.IdentifierToken));
            }
        }

        ExpectEndOfLine();
        var bodyStatements = ParseStatements(inFunction: true);
        var body = new BlockStatementSyntax(bodyStatements);

        Match(SyntaxKind.IfKeyword);  // IF
        Match(SyntaxKind.UKeyword);   // U
        Match(SyntaxKind.SayKeyword); // SAY
        Match(SyntaxKind.SoKeyword);  // SO

        return new FunctionDeclarationSyntax(name, parameters.ToImmutable(), body);
    }

    private ReturnStatementSyntax ParseReturn()
    {
        var found = Advance(); // FOUND
        Match(SyntaxKind.YrKeyword); // YR
        var expr = ParseExpression();
        return new ReturnStatementSyntax(found, expr);
    }

    private StatementSyntax ParseExpressionOrFunctionCallStatement()
    {
        var expr = ParseExpression();
        return new ExpressionStatementSyntax(expr);
    }

    private StatementSyntax ParseExpressionStatement()
    {
        var expr = ParseExpression();
        return new ExpressionStatementSyntax(expr);
    }

    /// <summary>
    /// Parses an expression.
    /// </summary>
    public ExpressionSyntax ParseExpression()
    {
        return Current.Kind switch
        {
            // SUM OF, DIFF OF, PRODUKT OF, QUOSHUNT OF, MOD OF, BIGGR OF, SMALLR OF
            SyntaxKind.SumKeyword or SyntaxKind.DiffKeyword or SyntaxKind.ProduktKeyword or
            SyntaxKind.QuoshuntKeyword or SyntaxKind.ModKeyword or SyntaxKind.BiggrKeyword or
            SyntaxKind.SmallrKeyword => ParseBinaryExpression(),

            // BOTH OF (boolean AND)
            SyntaxKind.BothKeyword when Peek(1).Kind == SyntaxKind.OfKeyword => ParseBinaryExpression(),

            // BOTH SAEM (equality)
            SyntaxKind.BothKeyword when Peek(1).Kind == SyntaxKind.SaemKeyword => ParseComparison(),

            // EITHER OF (boolean OR)
            SyntaxKind.EitherKeyword => ParseBinaryExpression(),

            // WON OF (boolean XOR)
            SyntaxKind.WonKeyword => ParseBinaryExpression(),

            // NOT (unary)
            SyntaxKind.NotKeyword => ParseUnary(),

            // ALL OF (variadic AND)
            SyntaxKind.AllKeyword => ParseAllOf(),

            // ANY OF (variadic OR)
            SyntaxKind.AnyKeyword => ParseAnyOf(),

            // DIFFRINT (inequality)
            SyntaxKind.DiffrintKeyword => ParseDiffrint(),

            // SMOOSH (concatenation)
            SyntaxKind.SmooshKeyword => ParseSmoosh(),

            // MAEK (cast expression)
            SyntaxKind.MaekKeyword => ParseCastExpression(),

            // I IZ (function call)
            SyntaxKind.IKeyword when Peek(1).Kind == SyntaxKind.IzKeyword => ParseFunctionCall(),

            // IT (implicit variable)
            SyntaxKind.ItKeyword => ParseIt(),

            // Literals and variables
            _ => ParsePrimary(),
        };
    }

    private ExpressionSyntax ParseBinaryExpression()
    {
        var op = Advance(); // SUM, DIFF, PRODUKT, QUOSHUNT, MOD, BIGGR, SMALLR, BOTH, EITHER, WON
        Match(SyntaxKind.OfKeyword); // OF
        var left = ParseExpression();

        // Optional AN
        if (Current.Kind == SyntaxKind.AnKeyword)
            Advance();

        var right = ParseExpression();
        return new BinaryExpressionSyntax(op, left, right);
    }

    private ExpressionSyntax ParseComparison()
    {
        var both = Advance(); // BOTH
        Match(SyntaxKind.SaemKeyword); // SAEM
        var left = ParseExpression();

        // Optional AN
        if (Current.Kind == SyntaxKind.AnKeyword)
            Advance();

        var right = ParseExpression();
        return new ComparisonExpressionSyntax(both, left, right);
    }

    private ExpressionSyntax ParseDiffrint()
    {
        var keyword = Advance(); // DIFFRINT
        var left = ParseExpression();

        if (Current.Kind == SyntaxKind.AnKeyword)
            Advance();

        var right = ParseExpression();
        return new DiffrintExpressionSyntax(keyword, left, right);
    }

    private ExpressionSyntax ParseUnary()
    {
        var op = Advance(); // NOT
        var operand = ParseExpression();
        return new UnaryExpressionSyntax(op, operand);
    }

    private ExpressionSyntax ParseAllOf()
    {
        var keyword = Advance(); // ALL
        Match(SyntaxKind.OfKeyword); // OF
        var operands = ParseVariadicArgs();
        return new AllOfExpressionSyntax(keyword, operands);
    }

    private ExpressionSyntax ParseAnyOf()
    {
        var keyword = Advance(); // ANY
        Match(SyntaxKind.OfKeyword); // OF
        var operands = ParseVariadicArgs();
        return new AnyOfExpressionSyntax(keyword, operands);
    }

    private ExpressionSyntax ParseSmoosh()
    {
        var keyword = Advance(); // SMOOSH
        var operands = ParseVariadicArgs();
        return new SmooshExpressionSyntax(keyword, operands);
    }

    private ImmutableArray<ExpressionSyntax> ParseVariadicArgs()
    {
        var args = ImmutableArray.CreateBuilder<ExpressionSyntax>();

        while (Current.Kind != SyntaxKind.MkayKeyword &&
               Current.Kind != SyntaxKind.EndOfLineToken &&
               Current.Kind != SyntaxKind.EndOfFileToken)
        {
            if (args.Count > 0 && Current.Kind == SyntaxKind.AnKeyword)
                Advance();

            if (Current.Kind == SyntaxKind.MkayKeyword ||
                Current.Kind == SyntaxKind.EndOfLineToken ||
                Current.Kind == SyntaxKind.EndOfFileToken)
                break;

            args.Add(ParseExpression());
        }

        // MKAY is optional at end of line
        if (Current.Kind == SyntaxKind.MkayKeyword)
            Advance();

        return args.ToImmutable();
    }

    private ExpressionSyntax ParseCastExpression()
    {
        var keyword = Advance(); // MAEK
        var operand = ParseExpression();

        // Optional A
        if (Current.Kind == SyntaxKind.AKeyword)
            Advance();

        var type = ParseTypeKeyword();
        return new CastExpressionSyntax(keyword, operand, type);
    }

    private ExpressionSyntax ParseFunctionCall()
    {
        Advance(); // I
        Advance(); // IZ

        var name = Match(SyntaxKind.IdentifierToken);
        var args = ImmutableArray.CreateBuilder<ExpressionSyntax>();

        // YR <expr> [AN YR <expr>]*
        if (Current.Kind == SyntaxKind.YrKeyword)
        {
            Advance(); // YR
            args.Add(ParseExpression());

            while (Current.Kind == SyntaxKind.AnKeyword && Peek(1).Kind == SyntaxKind.YrKeyword)
            {
                Advance(); // AN
                Advance(); // YR
                args.Add(ParseExpression());
            }
        }

        // MKAY optional at end of line
        if (Current.Kind == SyntaxKind.MkayKeyword)
            Advance();

        return new FunctionCallExpressionSyntax(name, args.ToImmutable());
    }

    private ExpressionSyntax ParseIt()
    {
        var token = Advance(); // IT
        return new ItExpressionSyntax(token);
    }

    private ExpressionSyntax ParsePrimary()
    {
        switch (Current.Kind)
        {
            case SyntaxKind.NumbrLiteralToken:
            {
                var token = Advance();
                return new LiteralExpressionSyntax(token, token.Value);
            }
            case SyntaxKind.NumbarLiteralToken:
            {
                var token = Advance();
                return new LiteralExpressionSyntax(token, token.Value);
            }
            case SyntaxKind.YarnLiteralToken:
            {
                var token = Advance();
                return new LiteralExpressionSyntax(token, token.Value);
            }
            case SyntaxKind.WinKeyword:
            {
                var token = Advance();
                return new LiteralExpressionSyntax(token, true);
            }
            case SyntaxKind.FailKeyword:
            {
                var token = Advance();
                return new LiteralExpressionSyntax(token, false);
            }
            case SyntaxKind.NoobKeyword:
            {
                var token = Advance();
                return new LiteralExpressionSyntax(token, null);
            }
            case SyntaxKind.IdentifierToken:
            {
                var token = Advance();
                return new VariableExpressionSyntax(token);
            }
            default:
            {
                var location = GetCurrentLocation();
                _diagnostics.ReportExpectedToken(location, "expression");
                var token = Advance();
                return new LiteralExpressionSyntax(token, null);
            }
        }
    }
}
