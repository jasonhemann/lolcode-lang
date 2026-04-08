namespace Lolcode.CodeAnalysis.Text;

/// <summary>
/// Represents a source text with line tracking capabilities.
/// </summary>
public sealed class SourceText
{
    private readonly string _text;

    /// <summary>
    /// The lines in the source text.
    /// </summary>
    public IReadOnlyList<TextLine> Lines { get; }

    /// <summary>
    /// The file name of the source text, if any.
    /// </summary>
    public string FileName { get; }

    /// <summary>
    /// The length of the source text.
    /// </summary>
    public int Length => _text.Length;

    /// <summary>
    /// Gets the character at the specified index.
    /// </summary>
    public char this[int index] => _text[index];

    private SourceText(string text, string fileName)
    {
        _text = text;
        FileName = fileName;
        Lines = ParseLines(this, text);
    }

    /// <summary>
    /// Creates a <see cref="SourceText"/> from the specified string.
    /// </summary>
    public static SourceText From(string text, string fileName = "")
    {
        return new SourceText(text, fileName);
    }

    /// <summary>
    /// Gets the zero-based line index containing the specified position.
    /// </summary>
    public int GetLineIndex(int position)
    {
        int lower = 0;
        int upper = Lines.Count - 1;

        while (lower <= upper)
        {
            int index = lower + (upper - lower) / 2;
            int start = Lines[index].Start;

            if (position == start)
                return index;

            if (start > position)
                upper = index - 1;
            else
                lower = index + 1;
        }

        return lower - 1;
    }

    /// <summary>
    /// Returns a substring of the source text.
    /// </summary>
    public string ToString(int start, int length) => _text.Substring(start, length);

    /// <summary>
    /// Returns a substring of the source text for the given span.
    /// </summary>
    public string ToString(TextSpan span) => ToString(span.Start, span.Length);

    /// <inheritdoc/>
    public override string ToString() => _text;

    private static IReadOnlyList<TextLine> ParseLines(SourceText sourceText, string text)
    {
        var result = new List<TextLine>();
        int position = 0;
        int lineStart = 0;

        while (position < text.Length)
        {
            int lineBreakWidth = GetLineBreakWidth(text, position);

            if (lineBreakWidth == 0)
            {
                position++;
            }
            else
            {
                AddLine(result, sourceText, lineStart, position, lineBreakWidth);
                position += lineBreakWidth;
                lineStart = position;
            }
        }

        if (position >= lineStart)
            AddLine(result, sourceText, lineStart, position, 0);

        return result;
    }

    private static void AddLine(List<TextLine> result, SourceText sourceText, int lineStart, int position, int lineBreakWidth)
    {
        int lineLength = position - lineStart;
        int lineLengthIncludingLineBreak = lineLength + lineBreakWidth;
        var line = new TextLine(sourceText, lineStart, lineLength, lineLengthIncludingLineBreak);
        result.Add(line);
    }

    private static int GetLineBreakWidth(string text, int position)
    {
        char c = text[position];
        char l = position + 1 >= text.Length ? '\0' : text[position + 1];

        if (c == '\r' && l == '\n')
            return 2;
        if (c == '\r' || c == '\n')
            return 1;

        return 0;
    }
}
