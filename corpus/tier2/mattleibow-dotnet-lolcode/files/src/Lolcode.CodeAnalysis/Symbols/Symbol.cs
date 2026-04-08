namespace Lolcode.CodeAnalysis.Symbols;

/// <summary>
/// Kinds of symbols in the LOLCODE compiler.
/// </summary>
public enum SymbolKind
{
    /// <summary>A variable (local or implicit IT).</summary>
    Variable,

    /// <summary>A function (HOW IZ I).</summary>
    Function,

    /// <summary>A function parameter (YR).</summary>
    Parameter,

    /// <summary>A built-in type (NUMBR, NUMBAR, YARN, TROOF, NOOB).</summary>
    Type
}

/// <summary>
/// Base class for all symbols (named entities in a LOLCODE program).
/// </summary>
public abstract class Symbol
{
    /// <summary>The declared name of this symbol.</summary>
    public string Name { get; }

    /// <summary>The kind of symbol.</summary>
    public abstract SymbolKind Kind { get; }

    /// <summary>Creates a new symbol with the given name.</summary>
    protected Symbol(string name) => Name = name;

    /// <inheritdoc/>
    public override string ToString() => $"{Kind}: {Name}";
}
