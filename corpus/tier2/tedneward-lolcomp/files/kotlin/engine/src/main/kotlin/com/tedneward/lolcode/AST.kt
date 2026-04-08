package com.tedneward.lolcode.ast

import java.util.Stack
import java.io.BufferedInputStream

import org.antlr.v4.runtime.*
import org.antlr.v4.runtime.tree.ParseTree
import org.antlr.v4.runtime.tree.ParseTreeWalker

import com.tedneward.lolcode.parser.*

// ====================================
// Abstract Syntax Tree
open class Node() { }

class CodeBlock(val statements: List<Statement> = mutableListOf()) : Node() {
    override fun toString() : String {
        return "(codeBlock statements:${statements.map { it.toString() }})"
    }
}

class Program(var version: String = "", var codeBlock: CodeBlock = CodeBlock()) : Node() { 
    override fun toString() : String {
        return "(program version:${version} codeBlock:${codeBlock})"
    }
}

open class Statement : Node() { }

class Declaration(val name : String, val expr : Expression) : Statement() { 
    override fun toString() : String {
        return "(decl ${name} ${expr})"
    }
}

class Print(val expressions : List<Expression>) : Statement() {
    override fun toString() : String {
        return "(print ${expressions.map { it.toString() }})"
    }
}

class Input(val label : String) : Statement() {
    override fun toString() : String {
        return "(input ${label})"
    }
}

class Assignment(val label : String, val expr : Expression) : Statement() {
    override fun toString() : String {
        return "(assign ${label} ${expr})"
    }
}

class Loop(val label : String, val conditional : Expression, val codeBlock : CodeBlock) : Statement() {
    override fun toString() : String {
        return "(loop ${label} condition:${conditional} ${codeBlock})"
    }
}

// if / if-else
// if-elseif-else ==> Conditional(elseBlock=CodeBlock(Conditional(elseBlock=block)))
class Conditional(val conditional : Expression, val codeBlock : CodeBlock) : Statement() {
    var elseBlock : CodeBlock? = null
    override fun toString() : String {
        return "(if condition:${conditional} ${codeBlock}${if (elseBlock != null) elseBlock.toString() else ""})"
    }
}

class FuncDecl(val name : String, val parameters : List<String>, val body : CodeBlock) : Statement() {
    override fun toString() : String {
        return "(func-decl ${name} ${parameters} ${body})"
    }
}

open class Expression : Statement() { }

class Atom(val value : String) : Expression() {
    override fun toString() : String {
        return "(ATOM '${value}')"
    }
    companion object { val NOOB = Atom("[NOOB]") }
}

class Label(val name : String) : Expression() { 
    override fun toString() : String {
        return "(LABEL ${name})"
    }
}

class BinaryOp(val left : Expression, val op : Operator, val right : Expression) : Expression() {
    enum class Operator { ADD, SUB, MUL, DIV, MOD }
    
    override fun toString() : String {
        return "(binary_op ${left} ${op} ${right})"
    }
}

class Comparison(val left : Expression, val op : Operator, val right : Expression) : Expression() {
    enum class Operator { EQU, NEQ, GT, LT, GTE, LTE }

    override fun toString() : String {
        return "(comparison ${left} ${op} ${right})"
    }
}

class Logical(val op : Operator, val expressions : List<Expression>) : Expression() {
    enum class Operator { ALL, ANY, AND, OR }

    override fun toString() : String {
        return "(logical ${op} ${expressions.map { it.toString() }})"
    }
}

class UnaryOp(val op : Operator, val expression : Expression) : Expression() {
    enum class Operator { NEG }

    override fun toString() : String {
        return "(unary_op ${op} ${expression})"
    }
}

class FuncCall(val name : String, val arguments : List<Expression>) : Expression() {
    override fun toString() : String {
        return "(call ${arguments})"
    }
}

// ====================================
// Visitor: ANTLR parser transformed into Abstract Syntax Tree
//
class ASTVisitor() : lolcodeBaseVisitor<Node>() {

    companion object Utility {
        fun parseToAST(code : String) : Program {
            val lexer = lolcodeLexer(CharStreams.fromString(code))
            val tokens = CommonTokenStream(lexer)
            val parser = lolcodeParser(tokens)
            val syntaxTree : ParseTree = parser.program()
            val programASTNode = ASTVisitor().visit(syntaxTree) as Program
            return programASTNode
        }
    }

    var program = Program()

    override fun visitProgram(ctx: lolcodeParser.ProgramContext) : Node {
        program.version = 
            if (ctx.opening().version() != null) 
                ctx.opening().version().text
            else
                "1.2"

        if (ctx.code_block() != null)
            program.codeBlock = this.visit(ctx.code_block()) as CodeBlock

        return program
    }

	override fun visitCode_block(ctx: lolcodeParser.Code_blockContext) : Node {
        val stmts : MutableList<Statement> = mutableListOf()
        for (stmt in ctx.statement()) {
            stmts.add(visit(stmt) as Statement)
        }
        return CodeBlock(stmts)
    }

	override fun visitDeclaration(ctx: lolcodeParser.DeclarationContext) : Node {
        return Declaration(ctx.LABEL().text, 
            if (ctx.expression() != null)
                this.visit(ctx.expression()) as Expression 
            else 
                Atom.NOOB
        )
    }

    override fun visitLoop(ctx: lolcodeParser.LoopContext) : Node {
        // Labels at top and bottom need to match
        if (ctx.LABEL(0).text != ctx.LABEL(1).text)
            throw Exception("YR LOOP IZ CONFUZED: ${ctx.LABEL(0).text} AN ${ctx.LABEL(1).text}")

        val label = ctx.LABEL(0).text
        val conditional = visitExpression(ctx.expression()) as Expression
        val codeBlock = visitCode_block(ctx.code_block()) as CodeBlock
        return Loop(label, conditional, codeBlock)
    }

    override fun visitIf_block(ctx: lolcodeParser.If_blockContext) : Node {
        val conditional = visitExpression(ctx.expression()) as Expression
        val codeBlock = visitCode_block(ctx.code_block(0)) as CodeBlock

        val node = Conditional(conditional, codeBlock)
        if (ctx.elseBlock != null) {
            node.elseBlock = visitCode_block(ctx.elseBlock) as CodeBlock
        }

        return node
    }

    override fun visitExpression(ctx: lolcodeParser.ExpressionContext) : Node {
        return if (ctx.ATOM() != null)
            Atom(ctx.ATOM().text.replace("\"", ""))
        else if (ctx.LABEL() != null)
            Label(ctx.LABEL().text)
        else if (ctx.maths() != null)
            this.visit(ctx.maths())
        else if (ctx.comparison() != null)
            this.visit(ctx.comparison())
        else if (ctx.logical() != null)
            this.visit(ctx.logical())
        else if (ctx.unary_op() != null)
            this.visit(ctx.unary_op())
        else if (ctx.func_call() != null)
            this.visit(ctx.func_call())
        else
            throw Exception("Somehow expression ${ctx} didn't generate a node")
    }

	override fun visitPrint_block(ctx: lolcodeParser.Print_blockContext) : Node {
        var exprs : MutableList<Expression> = mutableListOf()
        for (expr in ctx.expression()) {
            exprs.add(visit(expr) as Expression)
        }

        return Print(exprs)
    }

	override fun visitInput_block(ctx: lolcodeParser.Input_blockContext) : Node {
        return Input(ctx.LABEL().text)
    }
    
	override fun visitAssignment(ctx: lolcodeParser.AssignmentContext) : Node {
        return Assignment(ctx.LABEL().text, this.visit(ctx.expression()) as Expression)
    }

    override fun visitFunc_decl(ctx: lolcodeParser.Func_declContext) : Node {
        var paramNames : MutableList<String> = mutableListOf()
        for (node in ctx.LABEL()) {
            paramNames.add(node.text)
        }
        return FuncDecl(ctx.name.text, paramNames, this.visit(ctx.code_block()) as CodeBlock)
    }

    override fun visitMaths(ctx: lolcodeParser.MathsContext) : Node {
        val op = 
            if ((ctx.op.text).equals("SUM OF"))
                BinaryOp.Operator.ADD
            else if ((ctx.op.text).equals("DIFF OF"))
                BinaryOp.Operator.SUB
            else if ((ctx.op.text).equals("PRODUKT OF"))
                BinaryOp.Operator.MUL
            else if ((ctx.op.text).equals("QUOSHUNT OF"))
                BinaryOp.Operator.DIV
            else if ((ctx.op.text).equals("MOD OF"))
                BinaryOp.Operator.MOD
            else
                throw Exception("Unrecognized operator: ${ctx.op.text}")

        return BinaryOp(
            this.visit(ctx.left) as Expression, 
            op,
            this.visit(ctx.right) as Expression)
    }

    override fun visitComparison(ctx: lolcodeParser.ComparisonContext) : Node {
        val op = 
            if ((ctx.op.text).equals("BOTH SAEM"))
                Comparison.Operator.EQU
            else if ((ctx.op.text).equals("DIFFRINT"))
                Comparison.Operator.NEQ
            else if ((ctx.op.text).equals("BIGGR OF"))
                Comparison.Operator.GT
            else if ((ctx.op.text).equals("SMALLR OF"))
                Comparison.Operator.LT
            else
                throw Exception("Unrecognized operator: ${ctx.op.text}")

        return Comparison(
            this.visit(ctx.left) as Expression, 
            op,
            this.visit(ctx.right) as Expression)
    }

    override fun visitLogical(ctx: lolcodeParser.LogicalContext) : Node {
        return when (ctx.op.text) {
            "ALL OF" -> {
                val exprs : MutableList<Expression> = mutableListOf()
                for (expr in ctx.expression()) {
                    exprs.add(visit(expr) as Expression)
                }
                return Logical(Logical.Operator.ALL, exprs)
            }
            "ANY OF" -> {
                val exprs : MutableList<Expression> = mutableListOf()
                for (expr in ctx.expression()) {
                    exprs.add(visit(expr) as Expression)
                }
                return Logical(Logical.Operator.ANY, exprs)
            }
            "BOTH OF" -> 
                Logical(Logical.Operator.AND, 
                    listOf(this.visit(ctx.left) as Expression, 
                           this.visit(ctx.right) as Expression)
                )
            "EITHER OF" -> 
                Logical(Logical.Operator.OR, 
                    listOf(this.visit(ctx.left) as Expression, 
                           this.visit(ctx.right) as Expression)
                )
            else ->
                throw Exception("Unrecognized operator: ${ctx.op.text}")
        }
    }

    override fun visitUnary_op(ctx: lolcodeParser.Unary_opContext) : Node {
        // If we ever get a second unary operator, we'll need to make this
        // look like the binary operator code (when ctx.op.text....)
        // but for now, if it's a unary op, it's a NOT

        val expr = visit(ctx.expression()) as Expression
        return UnaryOp(UnaryOp.Operator.NEG, expr)
    }

    override fun visitFunc_call(ctx: lolcodeParser.Func_callContext) : Node {
        val exprs : MutableList<Expression> = mutableListOf()
        for (ex in ctx.expression()) {
            exprs.add(this.visit(ex) as Expression)
        }
        return FuncCall(ctx.name.text, exprs)
    }
}

