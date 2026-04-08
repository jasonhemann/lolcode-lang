using System.Collections;
using Lolcode.CodeAnalysis.Errors;
using Lolcode.CodeAnalysis.Text;

namespace Lolcode.CodeAnalysis;

/// <summary>
/// A mutable bag for collecting diagnostics during compilation.
/// </summary>
internal sealed class DiagnosticBag : IEnumerable<Diagnostic>
{
    private readonly List<Diagnostic> _diagnostics = [];

    /// <summary>
    /// Gets the number of diagnostics in the bag.
    /// </summary>
    public int Count => _diagnostics.Count;

    /// <summary>
    /// Returns true if the bag contains any errors.
    /// </summary>
    public bool HasErrors => _diagnostics.Any(d => d.Severity == DiagnosticSeverity.Error);

    /// <summary>
    /// Adds all diagnostics from another source.
    /// </summary>
    public void AddRange(IEnumerable<Diagnostic> diagnostics)
    {
        _diagnostics.AddRange(diagnostics);
    }

    /// <summary>
    /// Reports a diagnostic from a descriptor and format arguments.
    /// </summary>
    public void Report(DiagnosticDescriptor descriptor, TextLocation location, params object[] args)
    {
        _diagnostics.Add(Diagnostic.Create(descriptor, location, args));
    }

    /// <summary>
    /// Reports an error diagnostic with a raw ID and message (for internal errors).
    /// </summary>
    public void ReportError(string id, TextLocation location, string message)
    {
        _diagnostics.Add(new Diagnostic(id, location, message, DiagnosticSeverity.Error));
    }

    // --- Lexer Diagnostics ---

    /// <summary>Reports an unexpected character.</summary>
    public void ReportUnexpectedCharacter(TextLocation location, char character)
        => Report(DiagnosticDescriptors.UnexpectedCharacter, location, character);

    /// <summary>Reports an unterminated string literal.</summary>
    public void ReportUnterminatedString(TextLocation location)
        => Report(DiagnosticDescriptors.UnterminatedString, location);

    /// <summary>Reports an invalid number literal.</summary>
    public void ReportInvalidNumber(TextLocation location, string text)
        => Report(DiagnosticDescriptors.InvalidNumber, location, text);

    /// <summary>Reports an invalid escape sequence.</summary>
    public void ReportInvalidEscapeSequence(TextLocation location, string sequence)
        => Report(DiagnosticDescriptors.InvalidEscapeSequence, location, sequence);

    // --- Parser Diagnostics ---

    /// <summary>Reports an unexpected token.</summary>
    public void ReportUnexpectedToken(TextLocation location, string actual, string expected)
        => Report(DiagnosticDescriptors.UnexpectedToken, location, actual, expected);

    /// <summary>Reports a missing expected token.</summary>
    public void ReportExpectedToken(TextLocation location, string expected)
        => Report(DiagnosticDescriptors.ExpectedToken, location, expected);

    /// <summary>Reports a missing HAI statement.</summary>
    public void ReportMissingHai(TextLocation location)
        => Report(DiagnosticDescriptors.MissingHai, location);

    /// <summary>Reports a missing KTHXBYE statement.</summary>
    public void ReportMissingKthxbye(TextLocation location)
        => Report(DiagnosticDescriptors.MissingKthxbye, location);

    // --- Binder Diagnostics ---

    /// <summary>Reports an undeclared variable.</summary>
    public void ReportUndeclaredVariable(TextLocation location, string name)
        => Report(DiagnosticDescriptors.UndeclaredVariable, location, name);

    /// <summary>Reports a variable that has already been declared.</summary>
    public void ReportVariableAlreadyDeclared(TextLocation location, string name)
        => Report(DiagnosticDescriptors.VariableAlreadyDeclared, location, name);

    /// <summary>Reports a function that has already been declared.</summary>
    public void ReportFunctionAlreadyDeclared(TextLocation location, string name)
        => Report(DiagnosticDescriptors.FunctionAlreadyDeclared, location, name);

    /// <summary>Reports an undefined function.</summary>
    public void ReportUndefinedFunction(TextLocation location, string name)
        => Report(DiagnosticDescriptors.UndefinedFunction, location, name);

    /// <summary>Reports wrong argument count for a function call.</summary>
    public void ReportWrongArgumentCount(TextLocation location, string name, int expected, int actual)
        => Report(DiagnosticDescriptors.WrongArgumentCount, location, name, expected, actual);

    /// <summary>Reports an invalid cast.</summary>
    public void ReportInvalidCast(TextLocation location, string fromType, string toType)
        => Report(DiagnosticDescriptors.InvalidCast, location, fromType, toType);

    /// <summary>Reports GTFO used outside of loop, switch, or function.</summary>
    public void ReportInvalidGtfo(TextLocation location)
        => Report(DiagnosticDescriptors.InvalidGtfo, location);

    /// <summary>Reports FOUND YR used outside of a function.</summary>
    public void ReportInvalidFoundYr(TextLocation location)
        => Report(DiagnosticDescriptors.InvalidFoundYr, location);

    /// <summary>Reports duplicate OMG literal in WTF? block.</summary>
    public void ReportDuplicateOmgLiteral(TextLocation location, string value)
        => Report(DiagnosticDescriptors.DuplicateOmgLiteral, location, value);

    /// <summary>Reports non-literal in OMG case.</summary>
    public void ReportOmgRequiresLiteral(TextLocation location)
        => Report(DiagnosticDescriptors.OmgRequiresLiteral, location);

    /// <inheritdoc/>
    public IEnumerator<Diagnostic> GetEnumerator() => _diagnostics.GetEnumerator();

    /// <inheritdoc/>
    IEnumerator IEnumerable.GetEnumerator() => GetEnumerator();
}
