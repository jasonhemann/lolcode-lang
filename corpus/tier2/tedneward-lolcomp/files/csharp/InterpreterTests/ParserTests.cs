using Microsoft.VisualStudio.TestTools.UnitTesting;

namespace InterpreterTests;

using System;
using System.Collections.Generic;
using Antlr4.Runtime;
using Antlr4.Runtime.Misc;
using Antlr4.Runtime.Tree;
using LOLCODEParser;
using Interpreter;

/*
 * Run with console verbose output on:
 * `dotnet test -l "console;verbosity=detailed"`
 */
[TestClass]
public class ParserTests
{
    public IParseTree Parse(string code)
    {
        lolcodeLexer lexer = new lolcodeLexer(CharStreams.fromString(code));
        CommonTokenStream tokens = new CommonTokenStream(lexer);
        lolcodeParser parser = new lolcodeParser(tokens);
        //parser.BuildParseTree = true;
        return parser.program();
    }

    class OpeningInterpreter : lolcodeBaseListener 
    {
        public OpeningInterpreter() { Version = ""; }
        public string Version { get; set; }

        public override void ExitProgram(lolcodeParser.ProgramContext ctx)
        {
            var opening = ctx.opening().GetText();
            var version = ctx.opening().version().GetText();
            Version = version;
        }
    }
    [TestMethod]
    public void TestOpening()
    {
        var parseTree = Parse("HAI 1.2\nKTHXBYE");
        var interp = new OpeningInterpreter();
        ParseTreeWalker.Default.Walk(interp, parseTree);
        Assert.AreEqual(interp.Version, "1.2");
    }

    class DeclarationInterpreter : lolcodeBaseListener 
    {
        public DeclarationInterpreter() { Name = ""; Value = ""; }
        public string Name { get; set; }
        public string Value { get; set; }

        public override void ExitCode_block(lolcodeParser.Code_blockContext ctx)
        {
            lolcodeParser.StatementContext[] sts = ctx.statement();
        }
        public override void ExitDeclaration(lolcodeParser.DeclarationContext ctx)
        {
            Name = ctx.LABEL().GetText();
            Value = ctx.expression().GetText();
        }
    }
    [TestMethod]
    public void TestDeclaration()
    {
        var parseTree = Parse("HAI 1.2\n" +
            "I HAS A var ITZ 0" +
            "KTHXBYE");
        var interp = new DeclarationInterpreter();
        ParseTreeWalker.Default.Walk(interp, parseTree);
        Assert.AreEqual(interp.Name, "var");
        Assert.AreEqual(interp.Value, "0");
    }
}
