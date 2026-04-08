using Microsoft.VisualStudio.TestTools.UnitTesting;

namespace InterpreterTests;

using System;
using System.Collections.Generic;
using System.IO;
using LOLCODEParser;
using Interpreter;

[TestClass]
public class SourceInterpreterTests
{
    public static (Interpreter, String) RunExample(string filename, string input = "")
    {
        var interp = new Interpreter();

        interp.In = new StringReader(input);
        interp.Out = new StringWriter();

        var filepath = String.Format(@"../../../../../examples/{0}", filename);
        interp.Execute(File.ReadAllText(filepath));

        var outString = ((StringWriter)interp.Out).ToString();
        return (interp, outString);
    }
    [TestMethod]
    public void hai()
    {
        var (_, result) = RunExample("hai.lol");

        Assert.AreEqual("", result);
    }
    [TestMethod]
    public void hai12()
    {
        var (_, result) = RunExample("hai12.lol");

        Assert.AreEqual("", result);
    }
    [TestMethod]
    public void hello()
    {
        var (_, result) = RunExample("hello.lol");

        Assert.AreEqual("Hello world\n", result);
    }

    [TestMethod]
    public void justvar()
    {
        var (_, result) = RunExample("justvar.lol");

        Assert.AreEqual("", result);
    }
    [TestMethod]
    public void var()
    {
        var (_, result) = RunExample("var.lol");

        Assert.AreEqual("The var is 0\n", result);
    }
    [TestMethod]
    public void inputage()
    {
        var (_, result) = RunExample("inputage.lol", "27\n");

        Assert.AreEqual("What is your age?\nYour age is 27\n", result);
    }
    [TestMethod]
    public void assign()
    {
        var (_, result) = RunExample("assign.lol", "27\n");

        Assert.AreEqual(
            "What is your age?\n" +
            "Your age is 27\n" +
            "Your age is now 50\n" +
            "UR OLD!\n", 
            result);
    }
}
