namespace Lolcode.CodeAnalysis.BoundTree;

/// <summary>
/// Kinds of binary operators in LOLCODE bound trees.
/// </summary>
internal enum BoundBinaryOperatorKind
{
    /// <summary>SUM OF — addition.</summary>
    Addition,

    /// <summary>DIFF OF — subtraction.</summary>
    Subtraction,

    /// <summary>PRODUKT OF — multiplication.</summary>
    Multiplication,

    /// <summary>QUOSHUNT OF — division.</summary>
    Division,

    /// <summary>MOD OF — modulo.</summary>
    Modulo,

    /// <summary>BIGGR OF — maximum.</summary>
    Maximum,

    /// <summary>SMALLR OF — minimum.</summary>
    Minimum,

    /// <summary>BOTH OF — logical AND.</summary>
    LogicalAnd,

    /// <summary>EITHER OF — logical OR.</summary>
    LogicalOr,

    /// <summary>WON OF — logical XOR.</summary>
    LogicalXor,

    /// <summary>BOTH SAEM — equality comparison.</summary>
    Equal,

    /// <summary>DIFFRINT — inequality comparison.</summary>
    NotEqual,
}

/// <summary>
/// Kinds of unary operators in LOLCODE bound trees.
/// </summary>
internal enum BoundUnaryOperatorKind
{
    /// <summary>NOT — logical negation.</summary>
    LogicalNot,
}
