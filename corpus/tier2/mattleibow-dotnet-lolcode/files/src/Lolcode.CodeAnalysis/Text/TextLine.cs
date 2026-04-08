namespace Lolcode.CodeAnalysis.Text;

/// <summary>
/// Represents a line in a <see cref="SourceText"/>.
/// </summary>
public sealed class TextLine
{
    /// <summary>
    /// The source text containing this line.
    /// </summary>
    public SourceText Text { get; }

    /// <summary>
    /// The start position of the line in the source text.
    /// </summary>
    public int Start { get; }

    /// <summary>
    /// The length of the line excluding line break characters.
    /// </summary>
    public int Length { get; }

    /// <summary>
    /// The length of the line including line break characters.
    /// </summary>
    public int LengthIncludingLineBreak { get; }

    /// <summary>
    /// The end position of the line excluding line break characters.
    /// </summary>
    public int End => Start + Length;

    /// <summary>
    /// The span of the line excluding line break characters.
    /// </summary>
    public TextSpan Span => new(Start, Length);

    /// <summary>
    /// The span of the line including line break characters.
    /// </summary>
    public TextSpan SpanIncludingLineBreak => new(Start, LengthIncludingLineBreak);

    internal TextLine(SourceText text, int start, int length, int lengthIncludingLineBreak)
    {
        Text = text;
        Start = start;
        Length = length;
        LengthIncludingLineBreak = lengthIncludingLineBreak;
    }

    /// <inheritdoc/>
    public override string ToString() => Text.ToString(Span);
}
