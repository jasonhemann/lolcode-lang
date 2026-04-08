using System.Diagnostics;

namespace Lolcode.EndToEnd.Tests;

/// <summary>
/// Integration tests that build sample projects using the LOLCODE SDK.
/// Verifies the MSBuild integration works end-to-end by invoking
/// <c>dotnet build</c> on real <c>.lolproj</c> files.
/// </summary>
public class SdkSampleTests
{
    private static readonly string RepoRoot = FindRepoRoot();

    private static string FindRepoRoot()
    {
        string dir = AppContext.BaseDirectory;
        while (dir != null)
        {
            if (File.Exists(Path.Combine(dir, "dotnet-lolcode.slnx")))
                return dir;
            dir = Path.GetDirectoryName(dir)!;
        }
        throw new InvalidOperationException("Could not find repo root (looked for dotnet-lolcode.slnx)");
    }

    private static (int ExitCode, string StdOut, string StdErr) RunDotnet(string args, string workingDir, int timeoutMs = 30_000)
    {
        var psi = new ProcessStartInfo
        {
            FileName = "dotnet",
            Arguments = args,
            WorkingDirectory = workingDir,
            UseShellExecute = false,
            RedirectStandardOutput = true,
            RedirectStandardError = true,
        };

        using var process = Process.Start(psi)!;
        string stdout = process.StandardOutput.ReadToEnd();
        string stderr = process.StandardError.ReadToEnd();
        process.WaitForExit(timeoutMs);

        return (process.ExitCode, stdout, stderr);
    }

    /// <summary>
    /// Discovers all .lolproj sample projects for parameterized testing.
    /// </summary>
    public static IEnumerable<object[]> GetSampleProjects()
    {
        string samplesDir = Path.Combine(RepoRoot, "samples");
        foreach (string projFile in Directory.EnumerateFiles(samplesDir, "*.lolproj", SearchOption.AllDirectories))
        {
            string relativePath = Path.GetRelativePath(RepoRoot, Path.GetDirectoryName(projFile)!);
            yield return [relativePath];
        }
    }

    [Theory]
    [MemberData(nameof(GetSampleProjects))]
    public void Sample_Builds(string sampleDir)
    {
        var fullPath = Path.Combine(RepoRoot, sampleDir);
        var (exitCode, stdout, stderr) = RunDotnet("build", fullPath);

        exitCode.Should().Be(0, $"dotnet build failed for {sampleDir}:\n{stderr}\n{stdout}");
    }

    [Fact]
    public void HelloWorld_Runs_CorrectOutput()
    {
        var sampleDir = Path.Combine(RepoRoot, "samples", "basics", "hello-world");
        var (exitCode, stdout, stderr) = RunDotnet("run", sampleDir);

        exitCode.Should().Be(0, $"dotnet run failed:\n{stderr}");

        var output = stdout.Replace("\r\n", "\n").TrimEnd('\n');
        output.Should().Be("HAI WORLD!");
    }
}
