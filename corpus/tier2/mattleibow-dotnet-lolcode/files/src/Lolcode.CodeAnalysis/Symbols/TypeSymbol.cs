namespace Lolcode.CodeAnalysis.Symbols;

/// <summary>
/// Represents one of LOLCODE's five built-in types.
/// Instances are singletons accessed via static properties.
/// </summary>
public sealed class TypeSymbol : Symbol
{
    /// <summary>Integer type (NUMBR).</summary>
    public static readonly TypeSymbol Numbr = new("NUMBR");

    /// <summary>Floating-point type (NUMBAR).</summary>
    public static readonly TypeSymbol Numbar = new("NUMBAR");

    /// <summary>String type (YARN).</summary>
    public static readonly TypeSymbol Yarn = new("YARN");

    /// <summary>Boolean type (TROOF).</summary>
    public static readonly TypeSymbol Troof = new("TROOF");

    /// <summary>Null/uninitialized type (NOOB).</summary>
    public static readonly TypeSymbol Noob = new("NOOB");

    private TypeSymbol(string name) : base(name) { }

    /// <inheritdoc/>
    public override SymbolKind Kind => SymbolKind.Type;
}
