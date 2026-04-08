using System.Diagnostics;
using System.Reflection.Metadata;
using System.Reflection.PortableExecutable;
using Lolcode.CodeAnalysis;
using Lolcode.CodeAnalysis.Syntax;

namespace Lolcode.CodeAnalysis.Tests;

/// <summary>
/// Portable PDB tests validating LOLCODE source mapping (documents, sequence points, locals, and stack traces).
/// </summary>
public sealed class PortablePdbTests : IDisposable
{
    private const int HiddenSequencePointLine = 0xFEEFEE;

    private const string PdbSampleSource = """
HAI 1.2
  I HAS A x ITZ 42
  I HAS A name ITZ "LOLCODE"
  VISIBLE x
  VISIBLE name
  HOW IZ I add YR a AN YR b
    I HAS A result ITZ SUM OF a AN b
    FOUND YR result
  IF U SAY SO
  VISIBLE I IZ add YR 3 AN YR 4 MKAY
KTHXBYE
""";

    private const string StackTraceSource = """
HAI 1.2
  I HAS A x ITZ NOOB
  VISIBLE SUM OF x AN 1
KTHXBYE
""";

    private readonly string _tempDir;
    private readonly string _runtimeDll;

    public PortablePdbTests()
    {
        _tempDir = Path.Combine(Path.GetTempPath(), "lolcode-pdb-tests", Guid.NewGuid().ToString("N"));
        Directory.CreateDirectory(_tempDir);

        _runtimeDll = Path.Combine(AppContext.BaseDirectory, "Lolcode.Runtime.dll");
        if (!File.Exists(_runtimeDll))
            throw new FileNotFoundException($"Runtime DLL not found at: {_runtimeDll}");
    }

    public void Dispose()
    {
        try { Directory.Delete(_tempDir, recursive: true); } catch { /* best effort */ }
    }


    // (1) Helper that compiles to temp dir and returns (dllPath, pdbPath)
    private (string DllPath, string PdbPath, string SourcePath) CompileToTempDir(string source, string lolFileName)
    {
        // Use a real file path so stack traces point to an actual file.
        var sourcePath = Path.Combine(_tempDir, lolFileName);
        File.WriteAllText(sourcePath, source);

        var tree = SyntaxTree.ParseText(source, sourcePath);
        var compilation = LolcodeCompilation.Create(tree);

        var outputPath = Path.Combine(
            _tempDir,
            $"{Path.GetFileNameWithoutExtension(lolFileName)}_{Guid.NewGuid():N}.dll");

        var result = compilation.Emit(outputPath, _runtimeDll);
        result.Success.Should().BeTrue(string.Join("\n", result.Diagnostics.Select(d => d.ToString())));

        // Ensure runtime DLL is next to the output assembly for execution.
        var runtimeDest = Path.Combine(Path.GetDirectoryName(result.OutputPath!)!, "Lolcode.Runtime.dll");
        if (!File.Exists(runtimeDest))
            File.Copy(_runtimeDll, runtimeDest, overwrite: true);

        var dllPath = result.OutputPath!;
        var pdbPath = Path.ChangeExtension(dllPath, ".pdb");
        return (dllPath, pdbPath, sourcePath);
    }

    private sealed class PeAndPdb : IDisposable
    {
        private readonly FileStream _peStream;
        private readonly FileStream _pdbStream;
        private readonly MetadataReaderProvider _pdbProvider;

        public PEReader PeReader { get; }
        public MetadataReader PeMetadataReader { get; }
        public MetadataReader PdbMetadataReader { get; }

        private PeAndPdb(FileStream peStream, PEReader peReader, FileStream pdbStream, MetadataReaderProvider pdbProvider)
        {
            _peStream = peStream;
            _pdbStream = pdbStream;
            _pdbProvider = pdbProvider;

            PeReader = peReader;
            PeMetadataReader = peReader.GetMetadataReader();
            PdbMetadataReader = pdbProvider.GetMetadataReader();
        }

        public static PeAndPdb Open(string dllPath, string pdbPath)
        {
            // Show the full System.Reflection.Metadata / PE API usage: open PE + PDB as separate readers.
            var peStream = new FileStream(dllPath, FileMode.Open, FileAccess.Read, FileShare.ReadWrite | FileShare.Delete);
            var peReader = new PEReader(peStream);

            var pdbStream = new FileStream(pdbPath, FileMode.Open, FileAccess.Read, FileShare.ReadWrite | FileShare.Delete);
            var pdbProvider = MetadataReaderProvider.FromPortablePdbStream(pdbStream);

            return new PeAndPdb(peStream, peReader, pdbStream, pdbProvider);
        }

        public void Dispose()
        {
            PeReader.Dispose();
            _pdbProvider.Dispose();
            _pdbStream.Dispose();
            _peStream.Dispose();
        }
    }

    private static MethodDefinitionHandle FindMethod(MetadataReader peReader, string methodName)
    {
        foreach (var handle in peReader.MethodDefinitions)
        {
            var def = peReader.GetMethodDefinition(handle);
            var name = peReader.GetString(def.Name);
            if (string.Equals(name, methodName, StringComparison.Ordinal))
                return handle;
        }

        throw new InvalidOperationException($"Method '{methodName}' not found in PE metadata.");
    }

    private static string GetDocumentName(MetadataReader pdbReader, DocumentHandle documentHandle)
    {
        var doc = pdbReader.GetDocument(documentHandle);
        return pdbReader.GetString(doc.Name);
    }

    private static IReadOnlyList<(int StartLine, string DocumentName)> GetSequencePointLines(
        MetadataReader pdbReader,
        MethodDefinitionHandle methodHandle)
    {
        var debugInfo = pdbReader.GetMethodDebugInformation(methodHandle);
        var defaultDocument = debugInfo.Document;

        var points = new List<(int StartLine, string DocumentName)>();
        foreach (var sp in debugInfo.GetSequencePoints())
        {
            if (sp.StartLine == 0 || sp.StartLine == HiddenSequencePointLine)
                continue;

            var docHandle = sp.Document.IsNil ? defaultDocument : sp.Document;
            var docName = GetDocumentName(pdbReader, docHandle);
            points.Add((sp.StartLine, docName));
        }

        return points;
    }

    private static ISet<string> GetNamedLocalVariables(MetadataReader pdbReader, MethodDefinitionHandle methodHandle)
    {
        var names = new HashSet<string>(StringComparer.Ordinal);

        foreach (var scopeHandle in pdbReader.GetLocalScopes(methodHandle))
        {
            var scope = pdbReader.GetLocalScope(scopeHandle);

            foreach (var localHandle in scope.GetLocalVariables())
            {
                var local = pdbReader.GetLocalVariable(localHandle);
                var name = pdbReader.GetString(local.Name);
                if (!string.IsNullOrWhiteSpace(name))
                    names.Add(name);
            }
        }

        return names;
    }

    private static (int ExitCode, string StdErr) RunDotNet(string dllPath)
    {
        var psi = new ProcessStartInfo
        {
            FileName = "dotnet",
            Arguments = dllPath,
            UseShellExecute = false,
            RedirectStandardOutput = true,
            RedirectStandardError = true,
        };

        using var process = Process.Start(psi)!;
        _ = process.StandardOutput.ReadToEnd();
        var stderr = process.StandardError.ReadToEnd();
        process.WaitForExit(10000);

        return (process.ExitCode, stderr);
    }

    // (2) A test that reads the PDB and verifies document presence
    [Fact]
    public void Pdb_ContainsDocument_ForLolSourceFile()
    {
        var (dllPath, pdbPath, sourcePath) = CompileToTempDir(PdbSampleSource, "pdb_sample.lol");

        File.Exists(dllPath).Should().BeTrue();
        File.Exists(pdbPath).Should().BeTrue("Emit should produce a .pdb next to the emitted DLL");

        using var readers = PeAndPdb.Open(dllPath, pdbPath);
        var pdbReader = readers.PdbMetadataReader;

        var documents = pdbReader.Documents.Select(h => GetDocumentName(pdbReader, h)).ToArray();
        documents.Should().Contain(d => d.EndsWith(Path.GetFileName(sourcePath), StringComparison.Ordinal));
    }

    // (3) A test that verifies sequence points exist and have correct 1-based line numbers
    [Fact]
    public void Pdb_ContainsExpectedSequencePointLines_ForMainAndAdd()
    {
        var (dllPath, pdbPath, sourcePath) = CompileToTempDir(PdbSampleSource, "pdb_seqpoints.lol");
        File.Exists(pdbPath).Should().BeTrue();

        using var readers = PeAndPdb.Open(dllPath, pdbPath);
        var peReader = readers.PeMetadataReader;
        var pdbReader = readers.PdbMetadataReader;

        var mainHandle = FindMethod(peReader, "Main");
        var addHandle = FindMethod(peReader, "add");

        var mainPoints = GetSequencePointLines(pdbReader, mainHandle);
        var addPoints = GetSequencePointLines(pdbReader, addHandle);

        var expectedDocSuffix = Path.GetFileName(sourcePath);

        // Main method: sequence points for lines 2,3,4,5,10 (statements)
        var mainLines = mainPoints.Select(p => p.StartLine).Distinct().ToArray();
        mainLines.Should().Contain([2, 3, 4, 5, 10]);
        mainPoints.Where(p => new[] { 2, 3, 4, 5, 10 }.Contains(p.StartLine))
            .Select(p => p.DocumentName)
            .Should().OnlyContain(d => d.EndsWith(expectedDocSuffix, StringComparison.Ordinal));

        // add method: sequence points for lines 7,8
        var addLines = addPoints.Select(p => p.StartLine).Distinct().ToArray();
        addLines.Should().Contain([7, 8]);
        addPoints.Where(p => new[] { 7, 8 }.Contains(p.StartLine))
            .Select(p => p.DocumentName)
            .Should().OnlyContain(d => d.EndsWith(expectedDocSuffix, StringComparison.Ordinal));
    }

    // (4) A test that verifies local variable names per method
    [Fact]
    public void Pdb_ContainsExpectedLocals_ForMainAndAdd()
    {
        var (dllPath, pdbPath, _) = CompileToTempDir(PdbSampleSource, "pdb_locals.lol");
        File.Exists(pdbPath).Should().BeTrue();

        using var readers = PeAndPdb.Open(dllPath, pdbPath);
        var peReader = readers.PeMetadataReader;
        var pdbReader = readers.PdbMetadataReader;

        var mainHandle = FindMethod(peReader, "Main");
        var addHandle = FindMethod(peReader, "add");

        GetNamedLocalVariables(pdbReader, mainHandle)
            .Should().BeEquivalentTo(["IT", "x", "name"]);

        GetNamedLocalVariables(pdbReader, addHandle)
            .Should().BeEquivalentTo(["IT", "a", "b", "result"]);
    }

    // (5) A test that verifies compiler temps are absent
    [Fact]
    public void Pdb_DoesNotExposeCompilerTemps_AsNamedLocals()
    {
        var (dllPath, pdbPath, _) = CompileToTempDir(PdbSampleSource, "pdb_no_temps.lol");
        File.Exists(pdbPath).Should().BeTrue();

        using var readers = PeAndPdb.Open(dllPath, pdbPath);
        var peReader = readers.PeMetadataReader;
        var pdbReader = readers.PdbMetadataReader;

        var allNamedLocals = new HashSet<string>(StringComparer.Ordinal);

        foreach (var methodHandle in peReader.MethodDefinitions)
        {
            foreach (var name in GetNamedLocalVariables(pdbReader, methodHandle))
                allNamedLocals.Add(name);
        }

        allNamedLocals.Should().NotContain("matched");
        allNamedLocals.Should().NotContain("_functionReturnValue");
    }

    // (6) A test that verifies a runtime exception stack trace includes file:line info
    [Fact]
    public void RuntimeException_StackTrace_IncludesLolFileAndLine()
    {
        var (dllPath, pdbPath, sourcePath) = CompileToTempDir(StackTraceSource, "pdb_stacktrace.lol");
        File.Exists(pdbPath).Should().BeTrue("PDB must exist for file:line stack traces");

        var (exitCode, stderr) = RunDotNet(dllPath);
        exitCode.Should().NotBe(0, "Expected an unhandled runtime exception");

        var fileName = Path.GetFileName(sourcePath);
        stderr.Should().Contain($"{fileName}:line 3");
    }
}
