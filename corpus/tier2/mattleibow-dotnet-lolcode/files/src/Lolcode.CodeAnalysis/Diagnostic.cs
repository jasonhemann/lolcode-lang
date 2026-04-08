using Lolcode.CodeAnalysis.Text;

namespace Lolcode.CodeAnalysis;

/// <summary>
/// Represents a compiler diagnostic (error, warning, or info).
/// </summary>
/// <param name="Id">The diagnostic ID (e.g., LOL0001).</param>
/// <param name="Location">The source location of the diagnostic.</param>
/// <param name="Message">The human-readable diagnostic message.</param>
/// <param name="Severity">The severity of the diagnostic.</param>
public sealed record Diagnostic(
    string Id,
    TextLocation Location,
    string Message,
    DiagnosticSeverity Severity = DiagnosticSeverity.Error)
{
    /// <summary>The descriptor that produced this diagnostic, if any.</summary>
    public DiagnosticDescriptor? Descriptor { get; init; }

    /// <summary>
    /// Creates a diagnostic from a descriptor, location, and format arguments.
    /// </summary>
    public static Diagnostic Create(DiagnosticDescriptor descriptor, TextLocation location, params object[] args)
    {
        var message = args.Length > 0
            ? string.Format(descriptor.MessageFormat, args)
            : descriptor.MessageFormat;

        return new Diagnostic(descriptor.Id, location, message, descriptor.DefaultSeverity)
        {
            Descriptor = descriptor
        };
    }

    /// <inheritdoc/>
    public override string ToString()
    {
        return $"{Location}: {Severity.ToString().ToLowerInvariant()} {Id}: {Message}";
    }
}
