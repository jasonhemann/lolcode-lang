using System.Collections.Immutable;

namespace Lolcode.CodeAnalysis.Symbols;

/// <summary>
/// Represents a LOLCODE function declared with HOW IZ I.
/// </summary>
public sealed class FunctionSymbol : Symbol
{
    /// <summary>The parameters of this function.</summary>
    public ImmutableArray<ParameterSymbol> Parameters { get; }

    /// <inheritdoc/>
    public override SymbolKind Kind => SymbolKind.Function;

    /// <summary>Creates a new function symbol.</summary>
    public FunctionSymbol(string name, ImmutableArray<ParameterSymbol> parameters)
        : base(name) => Parameters = parameters;
}
