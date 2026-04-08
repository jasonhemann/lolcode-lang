package com.tedneward.lolcode

import com.tedneward.lolcode.ast.*

import java.io.File
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertTrue

class ScriptTests {
    fun executeExampleFile(testname : String) : Interpreter {
        val code = File("../../examples/${testname}.lol").readText()
        val input = if (File("../../examples/${testname}.in").isFile)
                File("../../examples/${testname}.in").readText()
            else
                ""
        val output = if (File("../../examples/${testname}.out").isFile)
                File("../../examples/${testname}.out").readText()
            else
                ""

        val interp = Interpreter()
        val outBuffer = java.io.ByteArrayOutputStream()
        interp.ioOut = java.io.PrintStream(outBuffer)
        interp.ioIn = input.byteInputStream()

        interp.execute(code)
        assertEquals(output, outBuffer.toString())

        return interp
    }

    @Test fun haiExample() {
        val interp = executeExampleFile("hai")

        assertEquals(interp.program.version, "1.2")
    }
    @Test fun hai12Example() {
        val interp = executeExampleFile("hai12")

        assertEquals(interp.program.version, "1.2")
    }
    @Test fun justvarExample() {
        val interp = executeExampleFile("justvar")

        assertEquals(interp.program.version, "1.2")
        assertEquals(interp.program.codeBlock.statements.size, 1)
        val decl = interp.program.codeBlock.statements.get(0) as Declaration
        assertEquals(decl.name, "var")
        assertTrue(decl.expr is Atom)
        assertEquals((decl.expr as Atom).value, "0")
    }
    @Test fun varExample() {
        val interp = executeExampleFile("var")

        assertEquals(interp.program.codeBlock.statements.size, 2)

        val decl = interp.program.codeBlock.statements.get(0) as Declaration
        assertEquals(decl.name, "var")
        assertTrue(decl.expr is Atom)
        assertEquals((decl.expr as Atom).value, "0")

        assertTrue(interp.program.codeBlock.statements.get(1) is Print)
    }

    @Test fun assignExample() { executeExampleFile("assign") }
    @Test fun commentExample() { executeExampleFile("comment") }
    @Test fun comparisonsExample() { executeExampleFile("comparisons") }
    @Test fun helloExample() { executeExampleFile("hello") }
    @Test fun ifExample() { executeExampleFile("if") }
    @Test fun ifElseExample() { executeExampleFile("ifelse") }
    @Test fun inputageExample() { executeExampleFile("inputage") }
    @Test fun logicalsExample() { executeExampleFile("logicals") }
    @Test fun loopingExample() { executeExampleFile("looping") }
    @Test fun mathsExample() { executeExampleFile("maths") }
    @Test fun moremathsExample() { executeExampleFile("moremaths") }
    @Test fun negnumbrsExample() { executeExampleFile("negnumbrs") }
    @Test fun simplefun() { executeExampleFile("simplefun") }
}
