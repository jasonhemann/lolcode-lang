namespace Lolcode.CodeAnalysis.Syntax;

/// <summary>
/// Static helper methods for analyzing LOLCODE syntax tokens and kinds.
/// Equivalent to Roslyn's SyntaxFacts.
/// </summary>
public static class SyntaxFacts
{
    /// <summary>Gets the SyntaxKind for a keyword text, or IdentifierToken if not a keyword.</summary>
    public static SyntaxKind GetKeywordKind(string text)
    {
        return text switch
        {
            "HAI" => SyntaxKind.HaiKeyword,
            "KTHXBYE" => SyntaxKind.KthxbyeKeyword,
            "I" => SyntaxKind.IKeyword,
            "HAS" => SyntaxKind.HasKeyword,
            "A" => SyntaxKind.AKeyword,
            "ITZ" => SyntaxKind.ItzKeyword,
            "R" => SyntaxKind.RKeyword,
            "AN" => SyntaxKind.AnKeyword,
            "IT" => SyntaxKind.ItKeyword,
            "VISIBLE" => SyntaxKind.VisibleKeyword,
            "GIMMEH" => SyntaxKind.GimmehKeyword,
            "SUM" => SyntaxKind.SumKeyword,
            "DIFF" => SyntaxKind.DiffKeyword,
            "PRODUKT" => SyntaxKind.ProduktKeyword,
            "QUOSHUNT" => SyntaxKind.QuoshuntKeyword,
            "MOD" => SyntaxKind.ModKeyword,
            "BIGGR" => SyntaxKind.BiggrKeyword,
            "SMALLR" => SyntaxKind.SmallrKeyword,
            "OF" => SyntaxKind.OfKeyword,
            "BOTH" => SyntaxKind.BothKeyword,
            "EITHER" => SyntaxKind.EitherKeyword,
            "WON" => SyntaxKind.WonKeyword,
            "NOT" => SyntaxKind.NotKeyword,
            "ALL" => SyntaxKind.AllKeyword,
            "ANY" => SyntaxKind.AnyKeyword,
            "MKAY" => SyntaxKind.MkayKeyword,
            "SAEM" => SyntaxKind.SaemKeyword,
            "DIFFRINT" => SyntaxKind.DiffrintKeyword,
            "SMOOSH" => SyntaxKind.SmooshKeyword,
            "MAEK" => SyntaxKind.MaekKeyword,
            "IS" => SyntaxKind.IsKeyword,
            "NOW" => SyntaxKind.NowKeyword,
            "O" => SyntaxKind.OKeyword,
            "RLY?" => SyntaxKind.RlyKeyword,
            "YA" => SyntaxKind.YaKeyword,
            "NO" => SyntaxKind.NoKeyword,
            "WAI" => SyntaxKind.WaiKeyword,
            "MEBBE" => SyntaxKind.MebbeKeyword,
            "OIC" => SyntaxKind.OicKeyword,
            "WTF?" => SyntaxKind.WtfKeyword,
            "OMG" => SyntaxKind.OmgKeyword,
            "OMGWTF" => SyntaxKind.OmgwtfKeyword,
            "GTFO" => SyntaxKind.GtfoKeyword,
            "IM" => SyntaxKind.ImKeyword,
            "IN" => SyntaxKind.InKeyword,
            "OUTTA" => SyntaxKind.OuttaKeyword,
            "YR" => SyntaxKind.YrKeyword,
            "TIL" => SyntaxKind.TilKeyword,
            "WILE" => SyntaxKind.WileKeyword,
            "UPPIN" => SyntaxKind.UppinKeyword,
            "NERFIN" => SyntaxKind.NerfinKeyword,
            "HOW" => SyntaxKind.HowKeyword,
            "IZ" => SyntaxKind.IzKeyword,
            "FOUND" => SyntaxKind.FoundKeyword,
            "IF" => SyntaxKind.IfKeyword,
            "U" => SyntaxKind.UKeyword,
            "SAY" => SyntaxKind.SayKeyword,
            "SO" => SyntaxKind.SoKeyword,
            "NOOB" => SyntaxKind.NoobKeyword,
            "TROOF" => SyntaxKind.TroofKeyword,
            "NUMBR" => SyntaxKind.NumbrKeyword,
            "NUMBAR" => SyntaxKind.NumbarKeyword,
            "YARN" => SyntaxKind.YarnKeyword,
            "WIN" => SyntaxKind.WinKeyword,
            "FAIL" => SyntaxKind.FailKeyword,
            _ => SyntaxKind.IdentifierToken
        };
    }

    /// <summary>Returns true if the kind represents a keyword.</summary>
    public static bool IsKeyword(SyntaxKind kind) =>
        kind.ToString().EndsWith("Keyword", StringComparison.Ordinal);

    /// <summary>Returns true if the kind represents a literal token.</summary>
    public static bool IsLiteral(SyntaxKind kind) => kind is
        SyntaxKind.NumbrLiteralToken or
        SyntaxKind.NumbarLiteralToken or
        SyntaxKind.YarnLiteralToken;

    /// <summary>Returns true if the kind represents a LOLCODE type keyword.</summary>
    public static bool IsTypeKeyword(SyntaxKind kind) => kind is
        SyntaxKind.NoobKeyword or
        SyntaxKind.TroofKeyword or
        SyntaxKind.NumbrKeyword or
        SyntaxKind.NumbarKeyword or
        SyntaxKind.YarnKeyword;

    /// <summary>Gets the display text for a SyntaxKind, if it has a fixed representation.</summary>
    public static string? GetText(SyntaxKind kind)
    {
        return kind switch
        {
            SyntaxKind.HaiKeyword => "HAI",
            SyntaxKind.KthxbyeKeyword => "KTHXBYE",
            SyntaxKind.IKeyword => "I",
            SyntaxKind.HasKeyword => "HAS",
            SyntaxKind.AKeyword => "A",
            SyntaxKind.ItzKeyword => "ITZ",
            SyntaxKind.RKeyword => "R",
            SyntaxKind.AnKeyword => "AN",
            SyntaxKind.ItKeyword => "IT",
            SyntaxKind.VisibleKeyword => "VISIBLE",
            SyntaxKind.GimmehKeyword => "GIMMEH",
            SyntaxKind.SumKeyword => "SUM",
            SyntaxKind.DiffKeyword => "DIFF",
            SyntaxKind.ProduktKeyword => "PRODUKT",
            SyntaxKind.QuoshuntKeyword => "QUOSHUNT",
            SyntaxKind.ModKeyword => "MOD",
            SyntaxKind.BiggrKeyword => "BIGGR",
            SyntaxKind.SmallrKeyword => "SMALLR",
            SyntaxKind.OfKeyword => "OF",
            SyntaxKind.BothKeyword => "BOTH",
            SyntaxKind.EitherKeyword => "EITHER",
            SyntaxKind.WonKeyword => "WON",
            SyntaxKind.NotKeyword => "NOT",
            SyntaxKind.AllKeyword => "ALL",
            SyntaxKind.AnyKeyword => "ANY",
            SyntaxKind.MkayKeyword => "MKAY",
            SyntaxKind.SaemKeyword => "SAEM",
            SyntaxKind.DiffrintKeyword => "DIFFRINT",
            SyntaxKind.SmooshKeyword => "SMOOSH",
            SyntaxKind.MaekKeyword => "MAEK",
            SyntaxKind.IsKeyword => "IS",
            SyntaxKind.NowKeyword => "NOW",
            SyntaxKind.OKeyword => "O",
            SyntaxKind.RlyKeyword => "RLY?",
            SyntaxKind.YaKeyword => "YA",
            SyntaxKind.NoKeyword => "NO",
            SyntaxKind.WaiKeyword => "WAI",
            SyntaxKind.MebbeKeyword => "MEBBE",
            SyntaxKind.OicKeyword => "OIC",
            SyntaxKind.WtfKeyword => "WTF?",
            SyntaxKind.OmgKeyword => "OMG",
            SyntaxKind.OmgwtfKeyword => "OMGWTF",
            SyntaxKind.GtfoKeyword => "GTFO",
            SyntaxKind.ImKeyword => "IM",
            SyntaxKind.InKeyword => "IN",
            SyntaxKind.OuttaKeyword => "OUTTA",
            SyntaxKind.YrKeyword => "YR",
            SyntaxKind.TilKeyword => "TIL",
            SyntaxKind.WileKeyword => "WILE",
            SyntaxKind.UppinKeyword => "UPPIN",
            SyntaxKind.NerfinKeyword => "NERFIN",
            SyntaxKind.HowKeyword => "HOW",
            SyntaxKind.IzKeyword => "IZ",
            SyntaxKind.FoundKeyword => "FOUND",
            SyntaxKind.IfKeyword => "IF",
            SyntaxKind.UKeyword => "U",
            SyntaxKind.SayKeyword => "SAY",
            SyntaxKind.SoKeyword => "SO",
            SyntaxKind.NoobKeyword => "NOOB",
            SyntaxKind.TroofKeyword => "TROOF",
            SyntaxKind.NumbrKeyword => "NUMBR",
            SyntaxKind.NumbarKeyword => "NUMBAR",
            SyntaxKind.YarnKeyword => "YARN",
            SyntaxKind.WinKeyword => "WIN",
            SyntaxKind.FailKeyword => "FAIL",
            _ => null
        };
    }
}
