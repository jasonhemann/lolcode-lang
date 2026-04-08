namespace Lolcode.CodeAnalysis;

/// <summary>
/// Describes a category of diagnostics. Equivalent to Roslyn's DiagnosticDescriptor.
/// Each unique diagnostic in the compiler has one descriptor that defines its
/// ID, title, message format, category, and default severity.
/// </summary>
public sealed class DiagnosticDescriptor
{
    /// <summary>The diagnostic ID (e.g., "LOL0001").</summary>
    public string Id { get; }

    /// <summary>Short title for the diagnostic.</summary>
    public string Title { get; }

    /// <summary>
    /// Format string for the message. Use {0}, {1}, etc. for arguments.
    /// </summary>
    public string MessageFormat { get; }

    /// <summary>The category (e.g., "Lexer", "Parser", "Binder").</summary>
    public string Category { get; }

    /// <summary>The default severity of this diagnostic.</summary>
    public DiagnosticSeverity DefaultSeverity { get; }

    /// <summary>Creates a new diagnostic descriptor.</summary>
    public DiagnosticDescriptor(
        string id, string title, string messageFormat,
        string category, DiagnosticSeverity defaultSeverity = DiagnosticSeverity.Error)
    {
        Id = id;
        Title = title;
        MessageFormat = messageFormat;
        Category = category;
        DefaultSeverity = defaultSeverity;
    }
}
