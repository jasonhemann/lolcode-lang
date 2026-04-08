using System.Reflection.Metadata;
using System.Reflection.PortableExecutable;
using Lolcode.CodeAnalysis;
using Lolcode.CodeAnalysis.Syntax;
using Xunit;

namespace Lolcode.CodeAnalysis.Tests;

public class DebuggerSmokeTests
{
    [Fact]
    public void Verify_Pdb_Generation_And_Content()
    {
        // 1. Arrange: Simple LOLCODE program with variables and multiple lines
        var source = @"
HAI 1.2
  I HAS A var ITZ 123
  VISIBLE var
KTHXBYE
";
        var outputDir = Path.Combine(Path.GetTempPath(), "LolcodeDebuggerTest_" + Guid.NewGuid());
        Directory.CreateDirectory(outputDir);

        var sourcePath = Path.Combine(outputDir, "TestProgram.lol");
        File.WriteAllText(sourcePath, source);

        var syntaxTree = SyntaxTree.ParseText(source, sourcePath);
        var compilation = LolcodeCompilation.Create(syntaxTree);
        var dllPath = Path.Combine(outputDir, "TestProgram.dll");
        var pdbPath = Path.ChangeExtension(dllPath, ".pdb");
        
        // Find Lolcode.Runtime.dll by type
        var runtimePath = typeof(Lolcode.Runtime.LolRuntime).Assembly.Location;

        // 2. Act: Emit the assembly
        var result = compilation.Emit(dllPath, runtimePath);

        try 
        {
            // 3. Assert: Compilation succeeded
            Assert.True(result.Success, "Compilation failed: " + string.Join(", ", result.Diagnostics));

            // 4. Assert: PDB File Exists (Smoke Test Level 1)
            Assert.True(File.Exists(pdbPath), "PDB file was not generated.");

            // 5. Assert: PDB Content (Smoke Test Level 2)
            using var fs = File.OpenRead(pdbPath);
            using var provider = MetadataReaderProvider.FromPortablePdbStream(fs);
            var reader = provider.GetMetadataReader();

            // Verify we have LocalScopes (implies local variables are tracked)
            Assert.NotEmpty(reader.LocalScopes);

            // Verify we have SequencePoints (implies line numbers are tracked)
            // Note: Sequence points are stored in MethodDebugInformation
            bool foundSequencePoints = false;
            foreach (var handle in reader.MethodDebugInformation)
            {
                var debugInfo = reader.GetMethodDebugInformation(handle);
                if (!debugInfo.SequencePointsBlob.IsNil)
                {
                    foundSequencePoints = true;
                    break;
                }
            }
            Assert.True(foundSequencePoints, "No sequence points found in PDB.");
        }
        finally
        {
            // Cleanup
            if (Directory.Exists(outputDir))
                Directory.Delete(outputDir, true);
        }
    }
}
