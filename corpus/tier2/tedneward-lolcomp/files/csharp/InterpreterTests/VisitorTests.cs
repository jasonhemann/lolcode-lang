using Microsoft.VisualStudio.TestTools.UnitTesting;

namespace InterpreterTests;

using System;
using System.Collections.Generic;
using System.IO;
using Antlr4.Runtime;
using Antlr4.Runtime.Tree;
using LOLCODEParser;
using Interpreter;

[TestClass]
public class VisitorTests
{
    [TestMethod]
    public void PrintoutTrees()
    {
        var code = 
            "HAI 1.2\n" +
            "VSIBLE \"Hello world!\" MKAY?\n" +
            "KHTXBYE";
        lolcodeLexer lexer = new lolcodeLexer(CharStreams.fromString(code));
        CommonTokenStream tokens = new CommonTokenStream(lexer);
        lolcodeParser parser = new lolcodeParser(tokens);
        var vinterpreter = new InterpreterVisitor().VisitProgram(parser.program());
    }
}
