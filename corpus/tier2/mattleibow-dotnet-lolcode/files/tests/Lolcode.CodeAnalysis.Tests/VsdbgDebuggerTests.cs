using System.Diagnostics;
using System.Runtime.InteropServices;
using System.Text.Json;
using Lolcode.CodeAnalysis;
using Lolcode.CodeAnalysis.Syntax;
using Xunit.Abstractions;

namespace Lolcode.CodeAnalysis.Tests;

/// <summary>
/// Integration tests that verify LOLCODE PDB debugging symbols work with a real debugger (vsdbg).
/// Uses a Node.js helper script (vsdbg-driver.js) that handles the proprietary vsda handshake.
///
/// Prerequisites (auto-detected, tests skip gracefully if missing):
/// - VS Code (or VS Code Insiders) with C# extension installed (provides vsdbg + vsda.node)
/// - Node.js available on PATH
///
/// The vsda.node module is a proprietary native addon bundled with Microsoft VS Code builds.
/// It signs a cryptographic challenge from vsdbg — without it, vsdbg refuses to start
/// (error 0x89720009). See: microsoft/vscode src/vs/platform/sign/node/signService.ts
/// </summary>
public sealed class VsdbgDebuggerTests : IDisposable
{
    private readonly string _tempDir;
    private readonly string _runtimeDll;
    private readonly ITestOutputHelper _output;
    private readonly string? _vsdbgPath;
    private readonly string? _vsdaPath;
    private readonly string? _nodePath;
    private readonly string _driverScript;

    public VsdbgDebuggerTests(ITestOutputHelper output)
    {
        _output = output;
        _tempDir = Path.Combine(Path.GetTempPath(), "lolcode-vsdbg-tests", Guid.NewGuid().ToString("N"));
        Directory.CreateDirectory(_tempDir);
        _runtimeDll = Path.Combine(AppContext.BaseDirectory, "Lolcode.Runtime.dll");
        _driverScript = Path.Combine(AppContext.BaseDirectory, "..", "..", "..", "vsdbg-driver.js");
        _vsdbgPath = FindVsdbg();
        _vsdaPath = FindVsda();
        _nodePath = FindNode();
    }

    public void Dispose()
    {
        try { Directory.Delete(_tempDir, recursive: true); } catch { /* best effort */ }
    }

    private bool CanRunDebuggerTests([System.Diagnostics.CodeAnalysis.NotNullWhen(false)] out string? reason)
    {
        if (_vsdbgPath == null) { reason = "vsdbg not found (install VS Code C# extension or set VSDBG_PATH)"; return false; }
        if (_vsdaPath == null) { reason = "vsda.node not found (requires Microsoft VS Code installation)"; return false; }
        if (_nodePath == null) { reason = "node not found on PATH"; return false; }
        if (!File.Exists(_driverScript)) { reason = $"vsdbg-driver.js not found at {_driverScript}"; return false; }
        reason = null;
        return true;
    }

    [Fact]
    public async Task Vsdbg_StopAtEntry_ReportsCorrectSourceFile()
    {
        if (!CanRunDebuggerTests(out var reason)) { _output.WriteLine($"SKIP: {reason}"); return; }

        var source = """
            HAI 1.2
              I HAS A x ITZ 42
              VISIBLE x
            KTHXBYE
            """;

        var (dllPath, pdbPath, sourcePath) = CompileToTempDir(source, "entry_test.lol");
        File.Exists(pdbPath).Should().BeTrue("PDB must exist for debugger test");

        await using var driver = await StartDriverAsync(dllPath);

        // stopAtEntry stops at IL offset 0 (before sequence points), source may be null.
        // Set a breakpoint on the first statement, then continue to it.
        var bpResult = await driver.SendAsync(new { cmd = "setBreakpoints", source = sourcePath, lines = new[] { 2 } });
        bpResult.GetProperty("breakpoints")[0].GetProperty("verified").GetBoolean().Should().BeTrue();

        var stopped = await driver.SendAsync(new { cmd = "continue", threadId = driver.ThreadId });
        var tid = stopped.GetProperty("threadId").GetInt32();

        var stack = await driver.SendAsync(new { cmd = "stackTrace", threadId = tid });
        var frames = stack.GetProperty("frames");
        frames.GetArrayLength().Should().BeGreaterThan(0);

        var topFrame = frames[0];
        var sourceProp = topFrame.GetProperty("source");
        sourceProp.ValueKind.Should().NotBe(JsonValueKind.Null, "source file should be available at breakpoint");
        sourceProp.GetString().Should().Contain("entry_test.lol");

        _output.WriteLine($"Source file: {sourceProp.GetString()}, line: {topFrame.GetProperty("line").GetInt32()}");
    }

    [Fact]
    public async Task Vsdbg_BreakpointHit_StopsAtCorrectLine()
    {
        if (!CanRunDebuggerTests(out var reason)) { _output.WriteLine($"SKIP: {reason}"); return; }

        var source = """
            HAI 1.2
              I HAS A x ITZ 42
              I HAS A y ITZ 7
              VISIBLE x
              VISIBLE y
            KTHXBYE
            """;

        var (dllPath, pdbPath, sourcePath) = CompileToTempDir(source, "bp_test.lol");
        File.Exists(pdbPath).Should().BeTrue("PDB must exist for debugger test");

        await using var driver = await StartDriverAsync(dllPath);

        // Set breakpoint on VISIBLE x (line 4)
        var bpResult = await driver.SendAsync(new { cmd = "setBreakpoints", source = sourcePath, lines = new[] { 4 } });
        var breakpoints = bpResult.GetProperty("breakpoints");
        breakpoints.GetArrayLength().Should().BeGreaterThan(0);
        breakpoints[0].GetProperty("verified").GetBoolean().Should().BeTrue("breakpoint should be verified");

        // Continue from entry to breakpoint
        var stopped = await driver.SendAsync(new { cmd = "continue", threadId = driver.ThreadId });
        stopped.GetProperty("reason").GetString().Should().Be("breakpoint");

        var newThreadId = stopped.GetProperty("threadId").GetInt32();

        // Verify stack frame shows correct source and line
        var stack = await driver.SendAsync(new { cmd = "stackTrace", threadId = newThreadId });
        var topFrame = stack.GetProperty("frames")[0];
        topFrame.GetProperty("source").GetString().Should().Contain("bp_test.lol");
        topFrame.GetProperty("line").GetInt32().Should().Be(4);

        _output.WriteLine($"Breakpoint hit at line {topFrame.GetProperty("line").GetInt32()} ✓");
    }

    [Fact]
    public async Task Vsdbg_LocalVariables_VisibleInDebugger()
    {
        if (!CanRunDebuggerTests(out var reason)) { _output.WriteLine($"SKIP: {reason}"); return; }

        var source = """
            HAI 1.2
              I HAS A x ITZ 42
              I HAS A name ITZ "LOLCODE"
              VISIBLE x
              VISIBLE name
            KTHXBYE
            """;

        var (dllPath, pdbPath, sourcePath) = CompileToTempDir(source, "locals_test.lol");
        File.Exists(pdbPath).Should().BeTrue("PDB must exist for debugger test");

        await using var driver = await StartDriverAsync(dllPath);

        // Set breakpoint on VISIBLE x (line 4) — after both variables are declared
        var bpResult = await driver.SendAsync(new { cmd = "setBreakpoints", source = sourcePath, lines = new[] { 4 } });
        bpResult.GetProperty("breakpoints")[0].GetProperty("verified").GetBoolean().Should().BeTrue();

        // Continue to breakpoint
        var stopped = await driver.SendAsync(new { cmd = "continue", threadId = driver.ThreadId });
        var tid = stopped.GetProperty("threadId").GetInt32();

        // Get stack frame
        var stack = await driver.SendAsync(new { cmd = "stackTrace", threadId = tid });
        var frameId = stack.GetProperty("frames")[0].GetProperty("id").GetInt32();

        // Get scopes
        var scopes = await driver.SendAsync(new { cmd = "scopes", frameId });
        var localsRef = scopes.GetProperty("scopes")[0].GetProperty("ref").GetInt32();

        // Get variables
        var vars = await driver.SendAsync(new { cmd = "variables", @ref = localsRef });
        var varNames = new List<string>();
        foreach (var v in vars.GetProperty("variables").EnumerateArray())
        {
            var name = v.GetProperty("name").GetString()!;
            var value = v.GetProperty("value").GetString() ?? "";
            varNames.Add(name);
            _output.WriteLine($"  Local: {name} = {value}");
        }

        varNames.Should().Contain("x", "local variable 'x' should be visible");
        varNames.Should().Contain("name", "local variable 'name' should be visible");
    }

    [Fact]
    public async Task Vsdbg_StepOver_AdvancesToNextLine()
    {
        if (!CanRunDebuggerTests(out var reason)) { _output.WriteLine($"SKIP: {reason}"); return; }

        var source = """
            HAI 1.2
              I HAS A x ITZ 1
              I HAS A y ITZ 2
              I HAS A z ITZ 3
              VISIBLE x
            KTHXBYE
            """;

        var (dllPath, pdbPath, sourcePath) = CompileToTempDir(source, "step_test.lol");
        File.Exists(pdbPath).Should().BeTrue("PDB must exist for debugger test");

        await using var driver = await StartDriverAsync(dllPath);

        // Set breakpoint on line 2 (I HAS A x)
        await driver.SendAsync(new { cmd = "setBreakpoints", source = sourcePath, lines = new[] { 2 } });
        var stopped = await driver.SendAsync(new { cmd = "continue", threadId = driver.ThreadId });
        var tid = stopped.GetProperty("threadId").GetInt32();

        // Get current line
        var stack1 = await driver.SendAsync(new { cmd = "stackTrace", threadId = tid });
        var line1 = stack1.GetProperty("frames")[0].GetProperty("line").GetInt32();
        _output.WriteLine($"Before step: line {line1}");

        // Step over
        var stepResult = await driver.SendAsync(new { cmd = "next", threadId = tid });
        tid = stepResult.GetProperty("threadId").GetInt32();

        // Get new line
        var stack2 = await driver.SendAsync(new { cmd = "stackTrace", threadId = tid });
        var line2 = stack2.GetProperty("frames")[0].GetProperty("line").GetInt32();
        _output.WriteLine($"After step: line {line2}");

        line2.Should().BeGreaterThan(line1, "stepping should advance to a later line");
    }

    [Fact]
    public async Task Vsdbg_FunctionCall_StepInShowsCorrectSource()
    {
        if (!CanRunDebuggerTests(out var reason)) { _output.WriteLine($"SKIP: {reason}"); return; }

        var source = """
            HAI 1.2
              HOW IZ I greet YR who
                VISIBLE who
              IF U SAY SO
              I IZ greet YR "world" MKAY
            KTHXBYE
            """;

        var (dllPath, pdbPath, sourcePath) = CompileToTempDir(source, "stepin_test.lol");
        File.Exists(pdbPath).Should().BeTrue("PDB must exist for debugger test");

        await using var driver = await StartDriverAsync(dllPath);

        // Set breakpoint on the function call line (line 5)
        await driver.SendAsync(new { cmd = "setBreakpoints", source = sourcePath, lines = new[] { 5 } });
        var stopped = await driver.SendAsync(new { cmd = "continue", threadId = driver.ThreadId });
        var tid = stopped.GetProperty("threadId").GetInt32();

        // Step into the function
        var stepResult = await driver.SendAsync(new { cmd = "stepIn", threadId = tid });
        tid = stepResult.GetProperty("threadId").GetInt32();

        // Verify we're now inside the greet function
        var stack = await driver.SendAsync(new { cmd = "stackTrace", threadId = tid });
        var topFrame = stack.GetProperty("frames")[0];
        var funcName = topFrame.GetProperty("name").GetString();
        var line = topFrame.GetProperty("line").GetInt32();
        _output.WriteLine($"After stepIn: {funcName} at line {line}");

        topFrame.GetProperty("source").GetString().Should().Contain("stepin_test.lol");
        // Should be inside the greet function (lines 2-4)
        line.Should().BeInRange(2, 4);
    }

    // --- Infrastructure ---

    private (string DllPath, string PdbPath, string SourcePath) CompileToTempDir(string source, string lolFileName)
    {
        var sourcePath = Path.Combine(_tempDir, lolFileName);
        File.WriteAllText(sourcePath, source);

        var tree = SyntaxTree.ParseText(source, sourcePath);
        var compilation = LolcodeCompilation.Create(tree);
        var outputPath = Path.Combine(_tempDir, Path.GetFileNameWithoutExtension(lolFileName) + ".dll");
        var result = compilation.Emit(outputPath, _runtimeDll);

        result.Success.Should().BeTrue(string.Join("\n", result.Diagnostics.Select(d => d.ToString())));

        var runtimeDest = Path.Combine(_tempDir, "Lolcode.Runtime.dll");
        if (!File.Exists(runtimeDest))
            File.Copy(_runtimeDll, runtimeDest, overwrite: true);

        var dllPath = result.OutputPath!;
        var pdbPath = Path.ChangeExtension(dllPath, ".pdb");
        return (dllPath, pdbPath, sourcePath);
    }

    private async Task<DebugDriver> StartDriverAsync(string dllPath)
    {
        var driver = new DebugDriver(_nodePath!, _driverScript, _vsdbgPath!, _vsdaPath!, _output);
        await driver.LaunchAsync(dllPath);
        return driver;
    }

    private static string? FindVsdbg()
    {
        var envPath = Environment.GetEnvironmentVariable("VSDBG_PATH");
        if (!string.IsNullOrEmpty(envPath) && File.Exists(envPath))
            return envPath;

        var home = Environment.GetFolderPath(Environment.SpecialFolder.UserProfile);
        var searchDirs = new[]
        {
            Path.Combine(home, ".vscode", "extensions"),
            Path.Combine(home, ".vscode-insiders", "extensions"),
            Path.Combine(home, ".vscode-server", "extensions"),
        };

        var binaryName = OperatingSystem.IsWindows() ? "vsdbg.exe" : "vsdbg";

        // Determine the expected architecture subdirectory
        var arch = RuntimeInformation.OSArchitecture switch
        {
            Architecture.Arm64 => "arm64",
            Architecture.X64 => "x86_64",
            _ => null,
        };

        foreach (var searchDir in searchDirs)
        {
            if (!Directory.Exists(searchDir)) continue;
            try
            {
                var candidates = Directory.GetFiles(searchDir, binaryName, SearchOption.AllDirectories)
                    .Where(p => p.Contains("ms-dotnettools.csharp") && p.Contains(".debugger"))
                    .Where(p => arch == null || p.Contains($".debugger/{arch}/") || p.Contains($".debugger\\{arch}\\"))
                    .OrderDescending()
                    .ToList();
                if (candidates.Count > 0) return candidates[0];
            }
            catch { /* ignore search errors */ }
        }

        return null;
    }

    private static string? FindVsda()
    {
        var envPath = Environment.GetEnvironmentVariable("VSDA_PATH");
        if (!string.IsNullOrEmpty(envPath) && File.Exists(envPath))
            return envPath;

        // Search in VS Code installations for vsda.node
        string[] appDirs;
        if (OperatingSystem.IsMacOS())
        {
            appDirs =
            [
                "/Applications/Visual Studio Code - Insiders.app/Contents/Resources/app",
                "/Applications/Visual Studio Code.app/Contents/Resources/app",
            ];
        }
        else if (OperatingSystem.IsWindows())
        {
            var localAppData = Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData);
            appDirs =
            [
                Path.Combine(localAppData, "Programs", "Microsoft VS Code Insiders", "resources", "app"),
                Path.Combine(localAppData, "Programs", "Microsoft VS Code", "resources", "app"),
            ];
        }
        else // Linux
        {
            appDirs =
            [
                "/usr/share/code-insiders/resources/app",
                "/usr/share/code/resources/app",
            ];
        }

        foreach (var appDir in appDirs)
        {
            // Try the unpacked path first (preferred), then the regular path
            var paths = new[]
            {
                Path.Combine(appDir, "node_modules.asar.unpacked", "vsda", "build", "Release", "vsda.node"),
                Path.Combine(appDir, "node_modules", "vsda", "build", "Release", "vsda.node"),
            };
            foreach (var p in paths)
                if (File.Exists(p)) return p;
        }

        return null;
    }

    private static string? FindNode()
    {
        // Try common node locations directly (more reliable than which/where in test runners)
        string[] candidates = OperatingSystem.IsWindows()
            ? [ @"C:\Program Files\nodejs\node.exe" ]
            : [ "/opt/homebrew/bin/node", "/usr/local/bin/node", "/usr/bin/node" ];

        foreach (var c in candidates)
            if (File.Exists(c)) return c;

        // Fallback to which/where
        try
        {
            var psi = new ProcessStartInfo
            {
                FileName = OperatingSystem.IsWindows() ? "where" : "which",
                Arguments = "node",
                UseShellExecute = false,
                RedirectStandardOutput = true,
                CreateNoWindow = true,
            };
            using var proc = Process.Start(psi)!;
            var result = proc.StandardOutput.ReadLine()?.Trim();
            proc.WaitForExit(5000);
            return !string.IsNullOrEmpty(result) && File.Exists(result) ? result : null;
        }
        catch { return null; }
    }

    /// <summary>
    /// Wraps the Node.js vsdbg-driver.js process, providing typed command/response over JSON lines.
    /// </summary>
    private sealed class DebugDriver : IAsyncDisposable
    {
        private readonly Process _process;
        private readonly ITestOutputHelper _output;
        private readonly List<string> _stderrLines = [];

        public int ThreadId { get; private set; }

        public DebugDriver(string nodePath, string driverScript, string vsdbgPath, string vsdaPath, ITestOutputHelper output)
        {
            _output = output;
            _process = new Process
            {
                StartInfo = new ProcessStartInfo
                {
                    FileName = nodePath,
                    ArgumentList = { driverScript, vsdbgPath, vsdaPath },
                    UseShellExecute = false,
                    RedirectStandardInput = true,
                    RedirectStandardOutput = true,
                    RedirectStandardError = true,
                    CreateNoWindow = true,
                },
            };
        }

        public async Task LaunchAsync(string dllPath)
        {
            _output.WriteLine($"Starting driver: {_process.StartInfo.FileName} {string.Join(" ", _process.StartInfo.ArgumentList)}");
            _output.WriteLine($"DLL: {dllPath}");
            _process.Start();
            _process.ErrorDataReceived += (_, e) => { if (e.Data != null) _stderrLines.Add(e.Data); };
            _process.BeginErrorReadLine();

            var result = await SendAsync(new
            {
                cmd = "launch",
                program = dllPath,
                cwd = Path.GetDirectoryName(dllPath)!,
                stopAtEntry = true,
            });

            if (result.TryGetProperty("error", out var err))
                throw new InvalidOperationException($"vsdbg launch failed: {err.GetString()}");

            ThreadId = result.GetProperty("threadId").GetInt32();
            _output.WriteLine($"Debugger launched (threadId={ThreadId}, reason={result.GetProperty("reason").GetString()})");
        }

        public async Task<JsonElement> SendAsync(object command)
        {
            var json = JsonSerializer.Serialize(command);
            await _process.StandardInput.WriteLineAsync(json);
            await _process.StandardInput.FlushAsync();

            // Read one JSON line of response
            var responseLine = await ReadLineWithTimeoutAsync(TimeSpan.FromSeconds(60));
            if (responseLine == null)
            {
                var stderr = string.Join("\n", _stderrLines);
                _output.WriteLine($"Driver stderr ({_stderrLines.Count} lines):\n{stderr}");
                throw new TimeoutException($"Timeout waiting for vsdbg-driver response. Stderr:\n{stderr}");
            }

            var doc = JsonDocument.Parse(responseLine);
            var root = doc.RootElement.Clone();
            doc.Dispose();

            if (root.TryGetProperty("error", out var err))
            {
                var stderr = string.Join("\n", _stderrLines);
                _output.WriteLine($"Driver error. Stderr ({_stderrLines.Count} lines):\n{stderr}");
                throw new InvalidOperationException($"vsdbg-driver error: {err.GetString()}");
            }

            return root;
        }

        private async Task<string?> ReadLineWithTimeoutAsync(TimeSpan timeout)
        {
            using var cts = new CancellationTokenSource(timeout);
            try
            {
                var line = await _process.StandardOutput.ReadLineAsync(cts.Token);
                return line;
            }
            catch (OperationCanceledException)
            {
                return null;
            }
        }

        public async ValueTask DisposeAsync()
        {
            try
            {
                await _process.StandardInput.WriteLineAsync("""{"cmd":"disconnect"}""");
                await _process.StandardInput.FlushAsync();
                _process.WaitForExit(5000);
            }
            catch { /* best effort */ }

            if (!_process.HasExited)
            {
                try { _process.Kill(entireProcessTree: true); } catch { }
            }

            _process.Dispose();
        }
    }
}
