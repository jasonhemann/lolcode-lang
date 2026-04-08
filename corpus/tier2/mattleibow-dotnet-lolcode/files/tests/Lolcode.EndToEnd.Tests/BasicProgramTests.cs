namespace Lolcode.EndToEnd.Tests;

public class BasicProgramTests : EndToEndTestBase
{
    [Fact]
    public void BasicProgram()
    {
        AssertOutput("""
            BTW Test minimal valid LOLCODE program structure
            BTW Per spec: HAI opens, KTHXBYE closes

            HAI 1.2
            KTHXBYE
            """, "");
    }

    [Fact]
    public void VersionNumber()
    {
        AssertOutput("""
            BTW Test HAI with version number
            BTW Per spec: HAI should be followed with LOLCODE version number (1.2)

            HAI 1.2
              VISIBLE "VERSION 1.2 PROGRAM"
            KTHXBYE
            """, "VERSION 1.2 PROGRAM");
    }

    [Fact]
    public void HelloWorld()
    {
        AssertOutput("""
            HAI 1.2
              VISIBLE "HAI WORLD!"
            KTHXBYE
            """, "HAI WORLD!");
    }
}
