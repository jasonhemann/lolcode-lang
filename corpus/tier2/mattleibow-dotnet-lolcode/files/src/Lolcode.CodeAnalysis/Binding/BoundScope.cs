using System.Collections.Immutable;
using System.Diagnostics.CodeAnalysis;
using Lolcode.CodeAnalysis.Symbols;

namespace Lolcode.CodeAnalysis.Binding;

/// <summary>
/// Lexical scope for symbol resolution during binding.
/// Supports nested scopes via parent chain (Roslyn's nested binder pattern).
/// </summary>
internal sealed class BoundScope
{
    private readonly Dictionary<string, VariableSymbol> _variables = new(StringComparer.Ordinal);
    private readonly Dictionary<string, FunctionSymbol> _functions = new(StringComparer.Ordinal);

    /// <summary>Parent scope, null for global scope.</summary>
    public BoundScope? Parent { get; }

    /// <summary>The implicit IT variable for this scope.</summary>
    public VariableSymbol ItVariable { get; }

    /// <summary>Creates a new scope, optionally nested under a parent.</summary>
    public BoundScope(BoundScope? parent = null)
    {
        Parent = parent;
        ItVariable = new VariableSymbol("IT", isImplicit: true);
    }

    /// <summary>Declares a variable in this scope. Returns false if already declared.</summary>
    public bool TryDeclareVariable(VariableSymbol variable) =>
        _variables.TryAdd(variable.Name, variable);

    /// <summary>Declares a function in this scope. Returns false if already declared.</summary>
    public bool TryDeclareFunction(FunctionSymbol function) =>
        _functions.TryAdd(function.Name, function);

    /// <summary>Looks up a variable by name, walking the parent chain.</summary>
    public bool TryLookupVariable(string name, [NotNullWhen(true)] out VariableSymbol? variable)
    {
        if (name == "IT") { variable = ItVariable; return true; }
        if (_variables.TryGetValue(name, out variable)) return true;
        // Don't walk parent chain for variables — LOLCODE functions cannot access outer variables
        variable = null;
        return false;
    }

    /// <summary>Looks up a function by name, walking the parent chain.</summary>
    public bool TryLookupFunction(string name, [NotNullWhen(true)] out FunctionSymbol? function)
    {
        if (_functions.TryGetValue(name, out function)) return true;
        if (Parent is not null) return Parent.TryLookupFunction(name, out function);
        function = null;
        return false;
    }

    /// <summary>Gets all variables declared directly in this scope.</summary>
    public ImmutableArray<VariableSymbol> GetDeclaredVariables() =>
        [.. _variables.Values];

    /// <summary>Gets all functions declared directly in this scope.</summary>
    public ImmutableArray<FunctionSymbol> GetDeclaredFunctions() =>
        [.. _functions.Values];
}
