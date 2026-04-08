package com.tedneward.lolcode

import com.tedneward.lolcode.ast.*

import java.io.File
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertTrue

class ASTTests {
    @Test
    fun simpleCalculations() {
        var interp = Interpreter()
        val outBuffer = java.io.ByteArrayOutputStream()
        interp.ioOut = java.io.PrintStream(outBuffer)

        var program = Program("1.2")

        program.codeBlock = CodeBlock(mutableListOf(
            Declaration("age", Atom("27"))
        ))

        var print = Print(listOf(
            Atom("Ur age is "),
            Label("age")
        ))
        (program.codeBlock.statements as MutableList<Statement>).add(print)

        interp.evaluate(program.codeBlock)

        assertEquals("Ur age is 27\n", outBuffer.toString())
    }
}
