using Lolcode.CodeAnalysis;
using Lolcode.CodeAnalysis.Syntax;
using Lolcode.CodeAnalysis.Text;
using Microsoft.Build.Framework;

namespace Lolcode.Build;

/// <summary>
/// MSBuild task that compiles LOLCODE source files (.lol) into a .NET assembly.
/// This is the core integration point between the MSBuild build system and the
/// LOLCODE compiler (<see cref="LolcodeCompilation"/>).
/// </summary>
public sealed class Lolc : Microsoft.Build.Utilities.Task
{
    /// <summary>Source .lol files to compile.</summary>
    [Required]
    public ITaskItem[] Sources { get; set; } = [];

    /// <summary>Path to the output assembly (e.g., obj/Debug/net10.0/MyApp.dll).</summary>
    [Required]
    public ITaskItem OutputAssembly { get; set; } = null!;

    /// <summary>Path to Lolcode.Runtime.dll for the compiler to reference.</summary>
    [Required]
    public string RuntimeAssemblyPath { get; set; } = null!;

    /// <summary>Assembly references (from NuGet, framework, project references).</summary>
    public ITaskItem[] ReferencePath { get; set; } = [];

    /// <summary>The assembly name (defaults to project name).</summary>
    public string AssemblyName { get; set; } = "";

    /// <summary>Output type: Exe or Library.</summary>
    public string OutputType { get; set; } = "Exe";

    /// <summary>
    /// When true, skip actual compilation (design-time builds).
    /// Visual Studio calls this during design-time to gather metadata without compiling.
    /// </summary>
    public bool SkipCompilerExecution { get; set; }

    /// <inheritdoc/>
    public override bool Execute()
    {
        if (SkipCompilerExecution)
        {
            Log.LogMessage(MessageImportance.Low, "Lolc: Skipping compilation (design-time build).");
            return true;
        }

        if (Sources.Length == 0)
        {
            Log.LogMessage(MessageImportance.Normal, "Lolc: No LOLCODE source files to compile.");
            return true;
        }

        var outputPath = OutputAssembly.ItemSpec;

        // Ensure output directory exists
        var outputDir = Path.GetDirectoryName(outputPath);
        if (!string.IsNullOrEmpty(outputDir))
            Directory.CreateDirectory(outputDir);

        Log.LogMessage(MessageImportance.Normal,
            "Lolc: Compiling {0} source file(s) to {1}", Sources.Length, outputPath);

        try
        {
            // Parse all source files
            var trees = new SyntaxTree[Sources.Length];
            for (int i = 0; i < Sources.Length; i++)
            {
                var filePath = Sources[i].ItemSpec;
                if (!File.Exists(filePath))
                {
                    Log.LogError(subcategory: null, errorCode: "LOL9000", helpKeyword: null,
                        file: filePath, lineNumber: 0, columnNumber: 0,
                        endLineNumber: 0, endColumnNumber: 0,
                        message: "Source file not found: {0}", filePath);
                    return false;
                }

                var source = File.ReadAllText(filePath);
                var sourceText = SourceText.From(source, filePath);
                trees[i] = SyntaxTree.ParseText(sourceText, filePath);
            }

            // Compile
            var compilation = LolcodeCompilation.Create(trees);
            var result = compilation.Emit(outputPath, RuntimeAssemblyPath);

            // Report diagnostics in MSBuild format
            foreach (var diagnostic in result.Diagnostics)
            {
                var location = diagnostic.Location;
                var file = location.FileName ?? Sources[0].ItemSpec;
                int line = location.StartLine + 1;
                int col = location.StartCharacter + 1;
                int endLine = location.EndLine + 1;
                int endCol = location.EndCharacter + 1;

                if (diagnostic.Severity == DiagnosticSeverity.Error)
                {
                    Log.LogError(subcategory: null, errorCode: diagnostic.Id, helpKeyword: null,
                        file: file, lineNumber: line, columnNumber: col,
                        endLineNumber: endLine, endColumnNumber: endCol,
                        message: diagnostic.Message);
                }
                else if (diagnostic.Severity == DiagnosticSeverity.Warning)
                {
                    Log.LogWarning(subcategory: null, warningCode: diagnostic.Id, helpKeyword: null,
                        file: file, lineNumber: line, columnNumber: col,
                        endLineNumber: endLine, endColumnNumber: endCol,
                        message: diagnostic.Message);
                }
                else
                {
                    Log.LogMessage(MessageImportance.Normal,
                        "{0}({1},{2}): {3}: {4}", file, line, col, diagnostic.Id, diagnostic.Message);
                }
            }

            if (result.Success)
            {
                Log.LogMessage(MessageImportance.Normal,
                    "Lolc: Successfully compiled to {0}", result.OutputPath);
            }

            return result.Success;
        }
        catch (Exception ex)
        {
            Log.LogError(subcategory: null, errorCode: "LOL9001", helpKeyword: null,
                file: null, lineNumber: 0, columnNumber: 0,
                endLineNumber: 0, endColumnNumber: 0,
                message: "Internal compiler error: {0}", ex.Message);
            return false;
        }
    }
}
