namespace Lolcode.CodeAnalysis.Text;

/// <summary>
/// Represents a location in source code with file, line, and column information.
/// </summary>
/// <param name="FileName">The file name.</param>
/// <param name="Span">The text span.</param>
/// <param name="StartLine">Zero-based start line.</param>
/// <param name="StartCharacter">Zero-based start character in the line.</param>
/// <param name="EndLine">Zero-based end line.</param>
/// <param name="EndCharacter">Zero-based end character in the line.</param>
public readonly record struct TextLocation(
    string FileName,
    TextSpan Span,
    int StartLine,
    int StartCharacter,
    int EndLine,
    int EndCharacter)
{
    /// <summary>
    /// Creates a <see cref="TextLocation"/> from a <see cref="SourceText"/> and <see cref="TextSpan"/>.
    /// </summary>
    public static TextLocation FromSpan(SourceText text, TextSpan span)
    {
        int startLineIndex = text.GetLineIndex(span.Start);
        int endLineIndex = text.GetLineIndex(span.End == 0 ? 0 : span.End - 1);

        int startCharacter = span.Start - text.Lines[startLineIndex].Start;
        int endCharacter = (span.End == 0 ? 0 : span.End - 1) - text.Lines[endLineIndex].Start + 1;

        return new TextLocation(text.FileName, span, startLineIndex, startCharacter, endLineIndex, endCharacter);
    }

    /// <summary>
    /// Returns a human-readable string like "file.lol(1,5)".
    /// </summary>
    public override string ToString()
    {
        string file = string.IsNullOrEmpty(FileName) ? "" : $"{FileName}";
        return $"{file}({StartLine + 1},{StartCharacter + 1})";
    }
}
