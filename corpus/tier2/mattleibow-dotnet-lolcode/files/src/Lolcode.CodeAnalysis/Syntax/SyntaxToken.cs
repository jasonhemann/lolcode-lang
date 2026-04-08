using Lolcode.CodeAnalysis.Text;

namespace Lolcode.CodeAnalysis.Syntax;

/// <summary>
/// Represents a single token produced by the lexer.
/// </summary>
/// <param name="Kind">The kind of token.</param>
/// <param name="Position">The start position in the source text.</param>
/// <param name="Text">The text of the token.</param>
/// <param name="Value">The literal value, if any (int, double, string, bool, or null).</param>
public sealed record SyntaxToken(
    SyntaxKind Kind,
    int Position,
    string Text,
    object? Value = null)
{
    /// <summary>
    /// The span of this token in the source text.
    /// </summary>
    public TextSpan Span => new(Position, Text.Length);

    /// <inheritdoc/>
    public override string ToString() => $"{Kind}: '{Text}'";
}
