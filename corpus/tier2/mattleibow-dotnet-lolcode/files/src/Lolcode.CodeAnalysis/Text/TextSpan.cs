namespace Lolcode.CodeAnalysis.Text;

/// <summary>
/// Represents a span of text in source code.
/// </summary>
/// <param name="Start">The start position (inclusive).</param>
/// <param name="Length">The length of the span.</param>
public readonly record struct TextSpan(int Start, int Length)
{
    /// <summary>
    /// The end position (exclusive).
    /// </summary>
    public int End => Start + Length;

    /// <summary>
    /// Creates a span from start and end positions.
    /// </summary>
    public static TextSpan FromBounds(int start, int end) => new(start, end - start);
}
