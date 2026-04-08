namespace Lolcode.CodeAnalysis.Symbols;

/// <summary>
/// Represents a variable declared in a LOLCODE program (I HAS A).
/// The implicit IT variable is marked with <see cref="IsImplicit"/>.
/// </summary>
public sealed class VariableSymbol : Symbol
{
    /// <summary>Whether this is the implicit IT variable.</summary>
    public bool IsImplicit { get; }

    /// <inheritdoc/>
    public override SymbolKind Kind => SymbolKind.Variable;

    /// <summary>Creates a new variable symbol.</summary>
    public VariableSymbol(string name, bool isImplicit = false) : base(name)
        => IsImplicit = isImplicit;
}
