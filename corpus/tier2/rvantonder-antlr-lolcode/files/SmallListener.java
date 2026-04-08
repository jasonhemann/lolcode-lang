// Generated from Small.g4 by ANTLR 4.0
import org.antlr.v4.runtime.tree.*;
import org.antlr.v4.runtime.Token;

public interface SmallListener extends ParseTreeListener {
	void enterUnaryop(SmallParser.UnaryopContext ctx);
	void exitUnaryop(SmallParser.UnaryopContext ctx);

	void enterNaryoptype(SmallParser.NaryoptypeContext ctx);
	void exitNaryoptype(SmallParser.NaryoptypeContext ctx);

	void enterNaryop(SmallParser.NaryopContext ctx);
	void exitNaryop(SmallParser.NaryopContext ctx);

	void enterBlock(SmallParser.BlockContext ctx);
	void exitBlock(SmallParser.BlockContext ctx);

	void enterBinaryoptype(SmallParser.BinaryoptypeContext ctx);
	void exitBinaryoptype(SmallParser.BinaryoptypeContext ctx);

	void enterExpr(SmallParser.ExprContext ctx);
	void exitExpr(SmallParser.ExprContext ctx);

	void enterType(SmallParser.TypeContext ctx);
	void exitType(SmallParser.TypeContext ctx);

	void enterElseifcond(SmallParser.ElseifcondContext ctx);
	void exitElseifcond(SmallParser.ElseifcondContext ctx);

	void enterIfthenelse(SmallParser.IfthenelseContext ctx);
	void exitIfthenelse(SmallParser.IfthenelseContext ctx);

	void enterFile(SmallParser.FileContext ctx);
	void exitFile(SmallParser.FileContext ctx);

	void enterLoopguard(SmallParser.LoopguardContext ctx);
	void exitLoopguard(SmallParser.LoopguardContext ctx);

	void enterLoop(SmallParser.LoopContext ctx);
	void exitLoop(SmallParser.LoopContext ctx);

	void enterExprlist(SmallParser.ExprlistContext ctx);
	void exitExprlist(SmallParser.ExprlistContext ctx);

	void enterEmptyline(SmallParser.EmptylineContext ctx);
	void exitEmptyline(SmallParser.EmptylineContext ctx);

	void enterOpexpr(SmallParser.OpexprContext ctx);
	void exitOpexpr(SmallParser.OpexprContext ctx);

	void enterBinaryop(SmallParser.BinaryopContext ctx);
	void exitBinaryop(SmallParser.BinaryopContext ctx);

	void enterConstant(SmallParser.ConstantContext ctx);
	void exitConstant(SmallParser.ConstantContext ctx);

	void enterDeclaration(SmallParser.DeclarationContext ctx);
	void exitDeclaration(SmallParser.DeclarationContext ctx);

	void enterNaryopargs(SmallParser.NaryopargsContext ctx);
	void exitNaryopargs(SmallParser.NaryopargsContext ctx);

	void enterLoopupdateop(SmallParser.LoopupdateopContext ctx);
	void exitLoopupdateop(SmallParser.LoopupdateopContext ctx);

	void enterInit(SmallParser.InitContext ctx);
	void exitInit(SmallParser.InitContext ctx);

	void enterNaryoparg(SmallParser.NaryopargContext ctx);
	void exitNaryoparg(SmallParser.NaryopargContext ctx);

	void enterPrint(SmallParser.PrintContext ctx);
	void exitPrint(SmallParser.PrintContext ctx);

	void enterStatement(SmallParser.StatementContext ctx);
	void exitStatement(SmallParser.StatementContext ctx);

	void enterElsecond(SmallParser.ElsecondContext ctx);
	void exitElsecond(SmallParser.ElsecondContext ctx);

	void enterAssignment(SmallParser.AssignmentContext ctx);
	void exitAssignment(SmallParser.AssignmentContext ctx);

	void enterInput(SmallParser.InputContext ctx);
	void exitInput(SmallParser.InputContext ctx);

	void enterCast(SmallParser.CastContext ctx);
	void exitCast(SmallParser.CastContext ctx);

	void enterLoopupdate(SmallParser.LoopupdateContext ctx);
	void exitLoopupdate(SmallParser.LoopupdateContext ctx);

	void enterIdentifier(SmallParser.IdentifierContext ctx);
	void exitIdentifier(SmallParser.IdentifierContext ctx);
}