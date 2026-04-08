using System.Diagnostics;
using Lolcode.CodeAnalysis;
using Lolcode.CodeAnalysis.Syntax;
using Lolcode.CodeAnalysis.Text;

namespace Lolcode.EndToEnd.Tests;

/// <summary>
/// Base class for end-to-end LOLCODE tests. Provides helpers to compile source,
/// run the resulting DLL, and assert on stdout or diagnostics.
/// </summary>
public abstract class EndToEndTestBase : IDisposable
{
    private readonly string _tempDir;
    private readonly string _runtimeDll;

    protected EndToEndTestBase()
    {
        _tempDir = Path.Combine(Path.GetTempPath(), "lolcode-tests", Guid.NewGuid().ToString("N"));
        Directory.CreateDirectory(_tempDir);

        string testDir = AppContext.BaseDirectory;
        _runtimeDll = Path.Combine(testDir, "Lolcode.Runtime.dll");
        if (!File.Exists(_runtimeDll))
            throw new FileNotFoundException($"Runtime DLL not found at: {_runtimeDll}");
    }

    public void Dispose()
    {
        try { Directory.Delete(_tempDir, recursive: true); } catch { /* best effort */ }
    }

    /// <summary>Compiles and runs LOLCODE source, returns stdout.</summary>
    protected string CompileAndRun(string source, string? stdin = null)
    {
        var tree = SyntaxTree.ParseText(source, "test.lol");
        string outputPath = Path.Combine(_tempDir, $"test_{Guid.NewGuid():N}.dll");
        var compilation = LolcodeCompilation.Create(tree);
        var result = compilation.Emit(outputPath, _runtimeDll);

        if (!result.Success)
        {
            var errors = string.Join("\n", result.Diagnostics.Select(d => d.ToString()));
            throw new InvalidOperationException($"Compilation failed:\n{errors}");
        }

        string runtimeDest = Path.Combine(Path.GetDirectoryName(result.OutputPath!)!, "Lolcode.Runtime.dll");
        if (!File.Exists(runtimeDest))
            File.Copy(_runtimeDll, runtimeDest, overwrite: true);

        var psi = new ProcessStartInfo
        {
            FileName = "dotnet",
            Arguments = result.OutputPath!,
            UseShellExecute = false,
            RedirectStandardOutput = true,
            RedirectStandardError = true,
            RedirectStandardInput = stdin != null,
        };

        using var process = Process.Start(psi)!;

        if (stdin != null)
        {
            process.StandardInput.Write(stdin);
            process.StandardInput.Close();
        }

        string output = process.StandardOutput.ReadToEnd();
        string error = process.StandardError.ReadToEnd();
        process.WaitForExit(10000);

        if (process.ExitCode != 0 && !string.IsNullOrEmpty(error))
            throw new InvalidOperationException($"Runtime error (exit code {process.ExitCode}):\n{error}");

        return output;
    }

    /// <summary>Compiles and runs source, asserts stdout matches expected output.</summary>
    protected void AssertOutput(string source, string expectedOutput, string? stdin = null)
    {
        string actual = CompileAndRun(source, stdin);
        actual = actual.Replace("\r\n", "\n").TrimEnd('\n');
        expectedOutput = expectedOutput.Replace("\r\n", "\n").TrimEnd('\n');
        actual.Should().Be(expectedOutput);
    }

    /// <summary>Asserts that running the source produces a runtime error containing the substring.</summary>
    protected void AssertRuntimeError(string source, string expectedErrorSubstring)
    {
        var tree = SyntaxTree.ParseText(source, "test.lol");
        string outputPath = Path.Combine(_tempDir, $"test_{Guid.NewGuid():N}.dll");
        var compilation = LolcodeCompilation.Create(tree);
        var result = compilation.Emit(outputPath, _runtimeDll);

        if (!result.Success)
        {
            var errors = string.Join("\n", result.Diagnostics.Select(d => d.ToString()));
            throw new InvalidOperationException($"Compilation failed (expected runtime error instead):\n{errors}");
        }

        string runtimeDest = Path.Combine(Path.GetDirectoryName(result.OutputPath!)!, "Lolcode.Runtime.dll");
        if (!File.Exists(runtimeDest))
            File.Copy(_runtimeDll, runtimeDest, overwrite: true);

        var psi = new ProcessStartInfo
        {
            FileName = "dotnet",
            Arguments = result.OutputPath!,
            UseShellExecute = false,
            RedirectStandardOutput = true,
            RedirectStandardError = true,
        };

        using var process = Process.Start(psi)!;
        string output = process.StandardOutput.ReadToEnd();
        string error = process.StandardError.ReadToEnd();
        process.WaitForExit(10000);

        process.ExitCode.Should().NotBe(0, "Expected a runtime error");
        error.Should().Contain(expectedErrorSubstring);
    }

    /// <summary>Asserts that compiling the source produces a diagnostic with the given ID.</summary>
    protected void AssertCompileError(string source, string expectedDiagnosticId)
    {
        var tree = SyntaxTree.ParseText(source, "test.lol");
        var compilation = LolcodeCompilation.Create(tree);
        var diagnostics = compilation.GetDiagnostics();

        diagnostics.Any(d => d.Severity == DiagnosticSeverity.Error).Should().BeTrue("Expected compilation to fail");
        diagnostics.Should().Contain(d => d.Id.Contains(expectedDiagnosticId));
    }
}
