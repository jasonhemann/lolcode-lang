namespace Lolcode.CodeAnalysis;

/// <summary>
/// Represents the severity of a diagnostic message.
/// </summary>
public enum DiagnosticSeverity
{
    /// <summary>An error that prevents compilation.</summary>
    Error,

    /// <summary>A warning that does not prevent compilation.</summary>
    Warning,

    /// <summary>An informational message.</summary>
    Info
}
