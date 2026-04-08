using Lolcode.CodeAnalysis;
using Lolcode.CodeAnalysis.Syntax;
using Lolcode.CodeAnalysis.Text;

namespace Lolcode.CodeAnalysis.Tests;

/// <summary>
/// Tests for the LOLCODE lexer.
/// </summary>
public class LexerTests
{
    private static IReadOnlyList<SyntaxToken> Lex(string input)
    {
        var source = SourceText.From(input);
        var lexer = new Lexer(source);
        return lexer.Tokenize();
    }

    private static IReadOnlyList<SyntaxToken> LexWithDiagnostics(string input, out IReadOnlyList<Diagnostic> diagnostics)
    {
        var source = SourceText.From(input);
        var lexer = new Lexer(source);
        var tokens = lexer.Tokenize();
        diagnostics = lexer.Diagnostics.ToList();
        return tokens;
    }

    [Fact]
    public void Lex_EmptyInput_ReturnsEof()
    {
        var tokens = Lex("");
        tokens.Should().ContainSingle().Which.Kind.Should().Be(SyntaxKind.EndOfFileToken);
    }

    [Fact]
    public void Lex_Integer_ReturnsNumbrToken()
    {
        var tokens = Lex("42");
        tokens.Should().HaveCount(2); // number + EOF
        tokens[0].Kind.Should().Be(SyntaxKind.NumbrLiteralToken);
        tokens[0].Value.Should().Be(42);
        tokens[0].Text.Should().Be("42");
    }

    [Fact]
    public void Lex_NegativeInteger_ReturnsNumbrToken()
    {
        var tokens = Lex("-7");
        tokens[0].Kind.Should().Be(SyntaxKind.NumbrLiteralToken);
        tokens[0].Value.Should().Be(-7);
    }

    [Fact]
    public void Lex_Float_ReturnsNumbarToken()
    {
        var tokens = Lex("3.14");
        tokens[0].Kind.Should().Be(SyntaxKind.NumbarLiteralToken);
        tokens[0].Value.Should().Be(3.14);
    }

    [Fact]
    public void Lex_NegativeFloat_ReturnsNumbarToken()
    {
        var tokens = Lex("-1.5");
        tokens[0].Kind.Should().Be(SyntaxKind.NumbarLiteralToken);
        tokens[0].Value.Should().Be(-1.5);
    }

    [Fact]
    public void Lex_SimpleString_ReturnsYarnToken()
    {
        var tokens = Lex("\"hello\"");
        tokens[0].Kind.Should().Be(SyntaxKind.YarnLiteralToken);
        tokens[0].Value.Should().Be("hello");
    }

    [Fact]
    public void Lex_StringWithNewlineEscape_ProcessesCorrectly()
    {
        var tokens = Lex("\"hello:)world\"");
        tokens[0].Kind.Should().Be(SyntaxKind.YarnLiteralToken);
        tokens[0].Value.Should().Be("hello\nworld");
    }

    [Fact]
    public void Lex_StringWithTabEscape_ProcessesCorrectly()
    {
        var tokens = Lex("\"hello:>world\"");
        tokens[0].Value.Should().Be("hello\tworld");
    }

    [Fact]
    public void Lex_StringWithQuoteEscape_ProcessesCorrectly()
    {
        var tokens = Lex("\"say :\"hi:\"\"");
        tokens[0].Value.Should().Be("say \"hi\"");
    }

    [Fact]
    public void Lex_StringWithColonEscape_ProcessesCorrectly()
    {
        var tokens = Lex("\"a::b\"");
        tokens[0].Value.Should().Be("a:b");
    }

    [Fact]
    public void Lex_StringWithBellEscape_ProcessesCorrectly()
    {
        var tokens = Lex("\"beep:o\"");
        tokens[0].Value.Should().Be("beep\a");
    }

    [Fact]
    public void Lex_StringWithHexEscape_ProcessesCorrectly()
    {
        var tokens = Lex("\":(41)\"");
        tokens[0].Value.Should().Be("A"); // 0x41 = 'A'
    }

    [Fact]
    public void Lex_StringWithNamedUnicode_ProcessesCorrectly()
    {
        var tokens = Lex("\":[SPACE]\"");
        tokens[0].Value.Should().Be(" ");
    }

    [Fact]
    public void Lex_UnterminatedString_ReportsDiagnostic()
    {
        var tokens = LexWithDiagnostics("\"unterminated", out var diagnostics);
        diagnostics.Should().ContainSingle().Which.Id.Should().Be("LOL0002");
    }

    [Fact]
    public void Lex_Keywords_CorrectKinds()
    {
        var tokens = Lex("HAI KTHXBYE VISIBLE GIMMEH");
        tokens[0].Kind.Should().Be(SyntaxKind.HaiKeyword);
        tokens[1].Kind.Should().Be(SyntaxKind.KthxbyeKeyword);
        tokens[2].Kind.Should().Be(SyntaxKind.VisibleKeyword);
        tokens[3].Kind.Should().Be(SyntaxKind.GimmehKeyword);
    }

    [Fact]
    public void Lex_BooleanLiterals_CorrectKinds()
    {
        var tokens = Lex("WIN FAIL");
        tokens[0].Kind.Should().Be(SyntaxKind.WinKeyword);
        tokens[1].Kind.Should().Be(SyntaxKind.FailKeyword);
    }

    [Fact]
    public void Lex_TypeKeywords_CorrectKinds()
    {
        var tokens = Lex("NOOB TROOF NUMBR NUMBAR YARN");
        tokens[0].Kind.Should().Be(SyntaxKind.NoobKeyword);
        tokens[1].Kind.Should().Be(SyntaxKind.TroofKeyword);
        tokens[2].Kind.Should().Be(SyntaxKind.NumbrKeyword);
        tokens[3].Kind.Should().Be(SyntaxKind.NumbarKeyword);
        tokens[4].Kind.Should().Be(SyntaxKind.YarnKeyword);
    }

    [Fact]
    public void Lex_MathKeywords_CorrectKinds()
    {
        var tokens = Lex("SUM DIFF PRODUKT QUOSHUNT MOD BIGGR SMALLR OF");
        tokens[0].Kind.Should().Be(SyntaxKind.SumKeyword);
        tokens[1].Kind.Should().Be(SyntaxKind.DiffKeyword);
        tokens[2].Kind.Should().Be(SyntaxKind.ProduktKeyword);
        tokens[3].Kind.Should().Be(SyntaxKind.QuoshuntKeyword);
        tokens[4].Kind.Should().Be(SyntaxKind.ModKeyword);
        tokens[5].Kind.Should().Be(SyntaxKind.BiggrKeyword);
        tokens[6].Kind.Should().Be(SyntaxKind.SmallrKeyword);
        tokens[7].Kind.Should().Be(SyntaxKind.OfKeyword);
    }

    [Fact]
    public void Lex_QuestionMarkKeywords_CorrectKinds()
    {
        // RLY? and WTF? include the question mark
        var tokens = Lex("RLY? WTF?");
        tokens[0].Kind.Should().Be(SyntaxKind.RlyKeyword);
        tokens[0].Text.Should().Be("RLY?");
        tokens[1].Kind.Should().Be(SyntaxKind.WtfKeyword);
        tokens[1].Text.Should().Be("WTF?");
    }

    [Fact]
    public void Lex_Identifier_ReturnsIdentifier()
    {
        var tokens = Lex("myVar");
        tokens[0].Kind.Should().Be(SyntaxKind.IdentifierToken);
        tokens[0].Text.Should().Be("myVar");
    }

    [Fact]
    public void Lex_Newline_ReturnsEndOfLine()
    {
        var tokens = Lex("HAI\nKTHXBYE");
        tokens[0].Kind.Should().Be(SyntaxKind.HaiKeyword);
        tokens[1].Kind.Should().Be(SyntaxKind.EndOfLineToken);
        tokens[2].Kind.Should().Be(SyntaxKind.KthxbyeKeyword);
    }

    [Fact]
    public void Lex_Comma_ReturnsEndOfLine()
    {
        var tokens = Lex("HAI,KTHXBYE");
        tokens[0].Kind.Should().Be(SyntaxKind.HaiKeyword);
        tokens[1].Kind.Should().Be(SyntaxKind.EndOfLineToken);
        tokens[2].Kind.Should().Be(SyntaxKind.KthxbyeKeyword);
    }

    [Fact]
    public void Lex_Exclamation_ReturnsExclamationToken()
    {
        var tokens = Lex("!");
        tokens[0].Kind.Should().Be(SyntaxKind.ExclamationToken);
    }

    [Fact]
    public void Lex_Comments_AreSkipped()
    {
        var tokens = Lex("BTW this is a comment\nHAI");
        // BTW comment should be skipped, but newline preserved
        tokens[0].Kind.Should().Be(SyntaxKind.EndOfLineToken);
        tokens[1].Kind.Should().Be(SyntaxKind.HaiKeyword);
    }

    [Fact]
    public void Lex_UnexpectedCharacter_ReportsDiagnostic()
    {
        var tokens = LexWithDiagnostics("@", out var diagnostics);
        diagnostics.Should().ContainSingle().Which.Id.Should().Be("LOL0001");
    }

    [Fact]
    public void Lex_AllControlFlowKeywords()
    {
        var tokens = Lex("O YA NO WAI MEBBE OIC OMG OMGWTF GTFO");
        tokens[0].Kind.Should().Be(SyntaxKind.OKeyword);
        tokens[1].Kind.Should().Be(SyntaxKind.YaKeyword);
        tokens[2].Kind.Should().Be(SyntaxKind.NoKeyword);
        tokens[3].Kind.Should().Be(SyntaxKind.WaiKeyword);
        tokens[4].Kind.Should().Be(SyntaxKind.MebbeKeyword);
        tokens[5].Kind.Should().Be(SyntaxKind.OicKeyword);
        tokens[6].Kind.Should().Be(SyntaxKind.OmgKeyword);
        tokens[7].Kind.Should().Be(SyntaxKind.OmgwtfKeyword);
        tokens[8].Kind.Should().Be(SyntaxKind.GtfoKeyword);
    }

    [Fact]
    public void Lex_LoopKeywords()
    {
        var tokens = Lex("IM IN OUTTA YR TIL WILE UPPIN NERFIN");
        tokens[0].Kind.Should().Be(SyntaxKind.ImKeyword);
        tokens[1].Kind.Should().Be(SyntaxKind.InKeyword);
        tokens[2].Kind.Should().Be(SyntaxKind.OuttaKeyword);
        tokens[3].Kind.Should().Be(SyntaxKind.YrKeyword);
        tokens[4].Kind.Should().Be(SyntaxKind.TilKeyword);
        tokens[5].Kind.Should().Be(SyntaxKind.WileKeyword);
        tokens[6].Kind.Should().Be(SyntaxKind.UppinKeyword);
        tokens[7].Kind.Should().Be(SyntaxKind.NerfinKeyword);
    }

    [Fact]
    public void Lex_FunctionKeywords()
    {
        var tokens = Lex("HOW IZ I FOUND IF U SAY SO");
        tokens[0].Kind.Should().Be(SyntaxKind.HowKeyword);
        tokens[1].Kind.Should().Be(SyntaxKind.IzKeyword);
        tokens[2].Kind.Should().Be(SyntaxKind.IKeyword);
        tokens[3].Kind.Should().Be(SyntaxKind.FoundKeyword);
        tokens[4].Kind.Should().Be(SyntaxKind.IfKeyword);
        tokens[5].Kind.Should().Be(SyntaxKind.UKeyword);
        tokens[6].Kind.Should().Be(SyntaxKind.SayKeyword);
        tokens[7].Kind.Should().Be(SyntaxKind.SoKeyword);
    }

    [Fact]
    public void Lex_BooleanOperatorKeywords()
    {
        var tokens = Lex("BOTH EITHER WON NOT ALL ANY MKAY SAEM DIFFRINT");
        tokens[0].Kind.Should().Be(SyntaxKind.BothKeyword);
        tokens[1].Kind.Should().Be(SyntaxKind.EitherKeyword);
        tokens[2].Kind.Should().Be(SyntaxKind.WonKeyword);
        tokens[3].Kind.Should().Be(SyntaxKind.NotKeyword);
        tokens[4].Kind.Should().Be(SyntaxKind.AllKeyword);
        tokens[5].Kind.Should().Be(SyntaxKind.AnyKeyword);
        tokens[6].Kind.Should().Be(SyntaxKind.MkayKeyword);
        tokens[7].Kind.Should().Be(SyntaxKind.SaemKeyword);
        tokens[8].Kind.Should().Be(SyntaxKind.DiffrintKeyword);
    }

    [Fact]
    public void Lex_CastKeywords()
    {
        var tokens = Lex("MAEK IS NOW A SMOOSH");
        tokens[0].Kind.Should().Be(SyntaxKind.MaekKeyword);
        tokens[1].Kind.Should().Be(SyntaxKind.IsKeyword);
        tokens[2].Kind.Should().Be(SyntaxKind.NowKeyword);
        tokens[3].Kind.Should().Be(SyntaxKind.AKeyword);
        tokens[4].Kind.Should().Be(SyntaxKind.SmooshKeyword);
    }

    [Fact]
    public void Lex_VariableDeclarationKeywords()
    {
        var tokens = Lex("I HAS A ITZ R AN IT");
        tokens[0].Kind.Should().Be(SyntaxKind.IKeyword);
        tokens[1].Kind.Should().Be(SyntaxKind.HasKeyword);
        tokens[2].Kind.Should().Be(SyntaxKind.AKeyword);
        tokens[3].Kind.Should().Be(SyntaxKind.ItzKeyword);
        tokens[4].Kind.Should().Be(SyntaxKind.RKeyword);
        tokens[5].Kind.Should().Be(SyntaxKind.AnKeyword);
        tokens[6].Kind.Should().Be(SyntaxKind.ItKeyword);
    }

    [Fact]
    public void Lex_LineContinuation_IsSkipped()
    {
        var tokens = Lex("SUM ...\n  OF");
        // The line continuation + newline should be consumed
        tokens[0].Kind.Should().Be(SyntaxKind.SumKeyword);
        tokens[1].Kind.Should().Be(SyntaxKind.OfKeyword);
    }
}
