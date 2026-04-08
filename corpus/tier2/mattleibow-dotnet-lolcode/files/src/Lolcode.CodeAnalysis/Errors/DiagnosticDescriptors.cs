namespace Lolcode.CodeAnalysis.Errors;

/// <summary>
/// Static catalog of all diagnostic descriptors used by the compiler.
/// Each descriptor defines the ID, title, message format, category, and severity
/// for one kind of diagnostic.
/// </summary>
public static class DiagnosticDescriptors
{
    // --- Lexer ---

    /// <summary>Unexpected character in source.</summary>
    public static readonly DiagnosticDescriptor UnexpectedCharacter = new(
        "LOL0001", "Unexpected character",
        "Unexpected character '{0}'.",
        "Lexer");

    /// <summary>Unterminated string literal.</summary>
    public static readonly DiagnosticDescriptor UnterminatedString = new(
        "LOL0002", "Unterminated string",
        "Unterminated string literal.",
        "Lexer");

    /// <summary>Invalid number literal.</summary>
    public static readonly DiagnosticDescriptor InvalidNumber = new(
        "LOL0003", "Invalid number",
        "Invalid number literal '{0}'.",
        "Lexer");

    /// <summary>Invalid escape sequence in string.</summary>
    public static readonly DiagnosticDescriptor InvalidEscapeSequence = new(
        "LOL0004", "Invalid escape sequence",
        "Invalid escape sequence '{0}'.",
        "Lexer");

    // --- Parser ---

    /// <summary>Unexpected token encountered during parsing.</summary>
    public static readonly DiagnosticDescriptor UnexpectedToken = new(
        "LOL1001", "Unexpected token",
        "Unexpected token '{0}', expected {1}.",
        "Parser");

    /// <summary>Expected a specific token that was not found.</summary>
    public static readonly DiagnosticDescriptor ExpectedToken = new(
        "LOL1002", "Expected token",
        "Expected {0}.",
        "Parser");

    /// <summary>Program is missing HAI statement.</summary>
    public static readonly DiagnosticDescriptor MissingHai = new(
        "LOL1003", "Missing HAI",
        "Program must start with 'HAI'.",
        "Parser");

    /// <summary>Program is missing KTHXBYE statement.</summary>
    public static readonly DiagnosticDescriptor MissingKthxbye = new(
        "LOL1004", "Missing KTHXBYE",
        "Program must end with 'KTHXBYE'.",
        "Parser");

    // --- Binder ---

    /// <summary>Variable has not been declared.</summary>
    public static readonly DiagnosticDescriptor UndeclaredVariable = new(
        "LOL2001", "Undeclared variable",
        "Variable '{0}' has not been declared.",
        "Binder");

    /// <summary>Variable has already been declared in this scope.</summary>
    public static readonly DiagnosticDescriptor VariableAlreadyDeclared = new(
        "LOL2002", "Variable already declared",
        "Variable '{0}' has already been declared.",
        "Binder");

    /// <summary>Function is not defined.</summary>
    public static readonly DiagnosticDescriptor UndefinedFunction = new(
        "LOL2003", "Undefined function",
        "Function '{0}' is not defined.",
        "Binder");

    /// <summary>Wrong number of arguments passed to function.</summary>
    public static readonly DiagnosticDescriptor WrongArgumentCount = new(
        "LOL2004", "Wrong argument count",
        "Function '{0}' expects {1} argument(s) but got {2}.",
        "Binder");

    /// <summary>Invalid type cast.</summary>
    public static readonly DiagnosticDescriptor InvalidCast = new(
        "LOL2005", "Invalid cast",
        "Cannot cast '{0}' to '{1}'.",
        "Binder");

    /// <summary>GTFO used outside valid context.</summary>
    public static readonly DiagnosticDescriptor InvalidGtfo = new(
        "LOL2006", "Invalid GTFO",
        "'GTFO' is not valid in this context.",
        "Binder");

    /// <summary>FOUND YR used outside a function.</summary>
    public static readonly DiagnosticDescriptor InvalidFoundYr = new(
        "LOL2007", "Invalid FOUND YR",
        "'FOUND YR' is not valid outside a function.",
        "Binder");

    /// <summary>Duplicate OMG case value in WTF? block.</summary>
    public static readonly DiagnosticDescriptor DuplicateOmgLiteral = new(
        "LOL2008", "Duplicate OMG value",
        "Duplicate OMG case value '{0}'.",
        "Binder");

    /// <summary>OMG case values must be literals.</summary>
    public static readonly DiagnosticDescriptor OmgRequiresLiteral = new(
        "LOL2009", "OMG requires literal",
        "OMG case values must be literals.",
        "Binder");

    /// <summary>Function has already been declared.</summary>
    public static readonly DiagnosticDescriptor FunctionAlreadyDeclared = new(
        "LOL2010", "Function already declared",
        "Function '{0}' has already been declared.",
        "Binder");

    // --- Internal ---

    /// <summary>Internal compiler error.</summary>
    public static readonly DiagnosticDescriptor InternalError = new(
        "LOL9001", "Internal compiler error",
        "Internal compiler error: {0}",
        "Internal");
}
