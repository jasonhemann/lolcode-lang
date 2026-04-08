namespace Lolcode.CodeAnalysis.Symbols;

/// <summary>
/// Represents a parameter of a LOLCODE function (YR).
/// </summary>
public sealed class ParameterSymbol : Symbol
{
    /// <summary>The zero-based ordinal position of this parameter.</summary>
    public int Ordinal { get; }

    /// <inheritdoc/>
    public override SymbolKind Kind => SymbolKind.Parameter;

    /// <summary>Creates a new parameter symbol.</summary>
    public ParameterSymbol(string name, int ordinal) : base(name)
        => Ordinal = ordinal;
}
