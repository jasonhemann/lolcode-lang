// Generated from C:\Users\Zanca\ThisShouldWork.g4 by ANTLR 4.1
   
import java.util.*;

import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.misc.*;
import org.antlr.v4.runtime.tree.*;
import java.util.List;
import java.util.Iterator;
import java.util.ArrayList;

@SuppressWarnings({"all", "warnings", "unchecked", "unused", "cast"})
public class ThisShouldWorkParser extends Parser {
	protected static final DFA[] _decisionToDFA;
	protected static final PredictionContextCache _sharedContextCache =
		new PredictionContextCache();
	public static final int
		T__3=1, T__2=2, T__1=3, T__0=4, HAI=5, CANHAS=6, KTHXBYE=7, QUESTIONMARK=8, 
		GIMMEH=9, VISIBLE=10, SUM=11, DIFF=12, PRODUKT=13, QUOSHUNT=14, MOD=15, 
		BIGGR=16, SMALLR=17, EQUALS=18, DIFFRINT=19, AN=20, LOOPIN=21, LOOPOUT=22, 
		IFIN=23, IFOUT=24, THEN=25, ELSE=26, VARI=27, ITZ=28, GTFO=29, BOOLEANS=30, 
		SEPARATOR=31, STRING=32, ID=33, LETTER=34, DIGIT=35, FLOAT=36, COMMENT=37, 
		BLOCKCOMMENT=38, NL=39, WS=40;
	public static final String[] tokenNames = {
		"<INVALID>", "'R'", "'NO WAI'", "'O RLY?'", "'!'", "'HAI'", "'CAN HAS'", 
		"'KTHXBYE'", "'?'", "'GIMMEH'", "'VISIBLE'", "'SUM OF'", "'DIFF OF'", 
		"'PRODUKT OF'", "'QUOSHUNT OF'", "'MOD OF'", "'BIGGR OF'", "'SMALLR OF'", 
		"'BOTH SAEM'", "'DIFFRINT'", "'AN'", "'IM IN YR'", "'IM OUTTA YR'", "'O RLY'", 
		"'OIC'", "'YA RLY'", "'NO WAY'", "'I HAS A'", "'ITZ'", "'GTFO'", "BOOLEANS", 
		"SEPARATOR", "STRING", "ID", "LETTER", "DIGIT", "FLOAT", "COMMENT", "BLOCKCOMMENT", 
		"NL", "WS"
	};
	public static final int
		RULE_prog = 0, RULE_include = 1, RULE_lib = 2, RULE_expression = 3, RULE_breaks = 4, 
		RULE_scan = 5, RULE_print = 6, RULE_printArgs = 7, RULE_arg = 8, RULE_exp = 9, 
		RULE_math = 10, RULE_comparison = 11, RULE_args = 12, RULE_argsLeft = 13, 
		RULE_argsRight = 14, RULE_loop = 15, RULE_conditional = 16, RULE_trueBranch = 17, 
		RULE_falseBranch = 18, RULE_variable_declaration = 19, RULE_var = 20, 
		RULE_label = 21, RULE_val = 22, RULE_assignment = 23;
	public static final String[] ruleNames = {
		"prog", "include", "lib", "expression", "breaks", "scan", "print", "printArgs", 
		"arg", "exp", "math", "comparison", "args", "argsLeft", "argsRight", "loop", 
		"conditional", "trueBranch", "falseBranch", "variable_declaration", "var", 
		"label", "val", "assignment"
	};

	@Override
	public String getGrammarFileName() { return "ThisShouldWork.g4"; }

	@Override
	public String[] getTokenNames() { return tokenNames; }

	@Override
	public String[] getRuleNames() { return ruleNames; }

	@Override
	public ATN getATN() { return _ATN; }


	 

	public ThisShouldWorkParser(TokenStream input) {
		super(input);
		_interp = new ParserATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}
	public static class ProgContext extends ParserRuleContext {
		public TerminalNode SEPARATOR(int i) {
			return getToken(ThisShouldWorkParser.SEPARATOR, i);
		}
		public IncludeContext include() {
			return getRuleContext(IncludeContext.class,0);
		}
		public List<TerminalNode> SEPARATOR() { return getTokens(ThisShouldWorkParser.SEPARATOR); }
		public TerminalNode EOF() { return getToken(ThisShouldWorkParser.EOF, 0); }
		public ExpressionContext expression(int i) {
			return getRuleContext(ExpressionContext.class,i);
		}
		public List<ExpressionContext> expression() {
			return getRuleContexts(ExpressionContext.class);
		}
		public ProgContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_prog; }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof ThisShouldWorkVisitor ) return ((ThisShouldWorkVisitor<? extends T>)visitor).visitProg(this);
			else return visitor.visitChildren(this);
		}
	}

	public final ProgContext prog() throws RecognitionException {
		ProgContext _localctx = new ProgContext(_ctx, getState());
		enterRule(_localctx, 0, RULE_prog);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(48); match(HAI);
			setState(49); match(SEPARATOR);
			setState(53);
			_la = _input.LA(1);
			if (_la==CANHAS) {
				{
				setState(50); include();
				setState(51); match(SEPARATOR);
				}
			}

			setState(61);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while ((((_la) & ~0x3f) == 0 && ((1L << _la) & ((1L << GIMMEH) | (1L << VISIBLE) | (1L << SUM) | (1L << DIFF) | (1L << PRODUKT) | (1L << QUOSHUNT) | (1L << MOD) | (1L << BIGGR) | (1L << SMALLR) | (1L << EQUALS) | (1L << DIFFRINT) | (1L << LOOPIN) | (1L << VARI) | (1L << GTFO) | (1L << SEPARATOR) | (1L << ID))) != 0)) {
				{
				setState(59);
				switch (_input.LA(1)) {
				case GIMMEH:
				case VISIBLE:
				case SUM:
				case DIFF:
				case PRODUKT:
				case QUOSHUNT:
				case MOD:
				case BIGGR:
				case SMALLR:
				case EQUALS:
				case DIFFRINT:
				case LOOPIN:
				case VARI:
				case GTFO:
				case ID:
					{
					setState(55); expression();
					setState(56); match(SEPARATOR);
					}
					break;
				case SEPARATOR:
					{
					setState(58); match(SEPARATOR);
					}
					break;
				default:
					throw new NoViableAltException(this);
				}
				}
				setState(63);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(64); match(KTHXBYE);
			setState(65); match(EOF);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class IncludeContext extends ParserRuleContext {
		public LibContext lib() {
			return getRuleContext(LibContext.class,0);
		}
		public IncludeContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_include; }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof ThisShouldWorkVisitor ) return ((ThisShouldWorkVisitor<? extends T>)visitor).visitInclude(this);
			else return visitor.visitChildren(this);
		}
	}

	public final IncludeContext include() throws RecognitionException {
		IncludeContext _localctx = new IncludeContext(_ctx, getState());
		enterRule(_localctx, 2, RULE_include);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(67); match(CANHAS);
			setState(68); lib();
			setState(69); match(QUESTIONMARK);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class LibContext extends ParserRuleContext {
		public TerminalNode ID() { return getToken(ThisShouldWorkParser.ID, 0); }
		public LibContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_lib; }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof ThisShouldWorkVisitor ) return ((ThisShouldWorkVisitor<? extends T>)visitor).visitLib(this);
			else return visitor.visitChildren(this);
		}
	}

	public final LibContext lib() throws RecognitionException {
		LibContext _localctx = new LibContext(_ctx, getState());
		enterRule(_localctx, 4, RULE_lib);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(71); match(ID);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class ExpressionContext extends ParserRuleContext {
		public ExpContext exp() {
			return getRuleContext(ExpContext.class,0);
		}
		public ScanContext scan() {
			return getRuleContext(ScanContext.class,0);
		}
		public BreaksContext breaks() {
			return getRuleContext(BreaksContext.class,0);
		}
		public LoopContext loop() {
			return getRuleContext(LoopContext.class,0);
		}
		public AssignmentContext assignment() {
			return getRuleContext(AssignmentContext.class,0);
		}
		public TerminalNode SEPARATOR() { return getToken(ThisShouldWorkParser.SEPARATOR, 0); }
		public Variable_declarationContext variable_declaration() {
			return getRuleContext(Variable_declarationContext.class,0);
		}
		public PrintContext print() {
			return getRuleContext(PrintContext.class,0);
		}
		public ConditionalContext conditional() {
			return getRuleContext(ConditionalContext.class,0);
		}
		public ExpressionContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_expression; }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof ThisShouldWorkVisitor ) return ((ThisShouldWorkVisitor<? extends T>)visitor).visitExpression(this);
			else return visitor.visitChildren(this);
		}
	}

	public final ExpressionContext expression() throws RecognitionException {
		ExpressionContext _localctx = new ExpressionContext(_ctx, getState());
		enterRule(_localctx, 6, RULE_expression);
		try {
			setState(84);
			switch ( getInterpreter().adaptivePredict(_input,3,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(73); variable_declaration();
				}
				break;

			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(74); scan();
				}
				break;

			case 3:
				enterOuterAlt(_localctx, 3);
				{
				setState(75); print();
				}
				break;

			case 4:
				enterOuterAlt(_localctx, 4);
				{
				setState(76); exp();
				setState(77); match(SEPARATOR);
				setState(78); conditional();
				}
				break;

			case 5:
				enterOuterAlt(_localctx, 5);
				{
				setState(80); exp();
				}
				break;

			case 6:
				enterOuterAlt(_localctx, 6);
				{
				setState(81); loop();
				}
				break;

			case 7:
				enterOuterAlt(_localctx, 7);
				{
				setState(82); assignment();
				}
				break;

			case 8:
				enterOuterAlt(_localctx, 8);
				{
				setState(83); breaks();
				}
				break;
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class BreaksContext extends ParserRuleContext {
		public TerminalNode GTFO() { return getToken(ThisShouldWorkParser.GTFO, 0); }
		public BreaksContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_breaks; }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof ThisShouldWorkVisitor ) return ((ThisShouldWorkVisitor<? extends T>)visitor).visitBreaks(this);
			else return visitor.visitChildren(this);
		}
	}

	public final BreaksContext breaks() throws RecognitionException {
		BreaksContext _localctx = new BreaksContext(_ctx, getState());
		enterRule(_localctx, 8, RULE_breaks);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(86); match(GTFO);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class ScanContext extends ParserRuleContext {
		public VarContext var() {
			return getRuleContext(VarContext.class,0);
		}
		public ScanContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_scan; }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof ThisShouldWorkVisitor ) return ((ThisShouldWorkVisitor<? extends T>)visitor).visitScan(this);
			else return visitor.visitChildren(this);
		}
	}

	public final ScanContext scan() throws RecognitionException {
		ScanContext _localctx = new ScanContext(_ctx, getState());
		enterRule(_localctx, 10, RULE_scan);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(88); match(GIMMEH);
			setState(89); var();
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class PrintContext extends ParserRuleContext {
		public PrintArgsContext printArgs() {
			return getRuleContext(PrintArgsContext.class,0);
		}
		public PrintContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_print; }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof ThisShouldWorkVisitor ) return ((ThisShouldWorkVisitor<? extends T>)visitor).visitPrint(this);
			else return visitor.visitChildren(this);
		}
	}

	public final PrintContext print() throws RecognitionException {
		PrintContext _localctx = new PrintContext(_ctx, getState());
		enterRule(_localctx, 12, RULE_print);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(91); match(VISIBLE);
			setState(92); printArgs();
			setState(93); match(4);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class PrintArgsContext extends ParserRuleContext {
		public TerminalNode STRING(int i) {
			return getToken(ThisShouldWorkParser.STRING, i);
		}
		public List<VarContext> var() {
			return getRuleContexts(VarContext.class);
		}
		public List<TerminalNode> STRING() { return getTokens(ThisShouldWorkParser.STRING); }
		public VarContext var(int i) {
			return getRuleContext(VarContext.class,i);
		}
		public PrintArgsContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_printArgs; }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof ThisShouldWorkVisitor ) return ((ThisShouldWorkVisitor<? extends T>)visitor).visitPrintArgs(this);
			else return visitor.visitChildren(this);
		}
	}

	public final PrintArgsContext printArgs() throws RecognitionException {
		PrintArgsContext _localctx = new PrintArgsContext(_ctx, getState());
		enterRule(_localctx, 14, RULE_printArgs);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(99);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==STRING || _la==ID) {
				{
				setState(97);
				switch (_input.LA(1)) {
				case STRING:
					{
					setState(95); match(STRING);
					}
					break;
				case ID:
					{
					setState(96); var();
					}
					break;
				default:
					throw new NoViableAltException(this);
				}
				}
				setState(101);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class ArgContext extends ParserRuleContext {
		public VarContext var() {
			return getRuleContext(VarContext.class,0);
		}
		public ValContext val() {
			return getRuleContext(ValContext.class,0);
		}
		public ArgContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_arg; }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof ThisShouldWorkVisitor ) return ((ThisShouldWorkVisitor<? extends T>)visitor).visitArg(this);
			else return visitor.visitChildren(this);
		}
	}

	public final ArgContext arg() throws RecognitionException {
		ArgContext _localctx = new ArgContext(_ctx, getState());
		enterRule(_localctx, 16, RULE_arg);
		try {
			setState(104);
			switch (_input.LA(1)) {
			case BOOLEANS:
			case STRING:
			case DIGIT:
			case FLOAT:
				enterOuterAlt(_localctx, 1);
				{
				setState(102); val();
				}
				break;
			case ID:
				enterOuterAlt(_localctx, 2);
				{
				setState(103); var();
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class ExpContext extends ParserRuleContext {
		public ComparisonContext comparison() {
			return getRuleContext(ComparisonContext.class,0);
		}
		public MathContext math() {
			return getRuleContext(MathContext.class,0);
		}
		public ExpContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_exp; }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof ThisShouldWorkVisitor ) return ((ThisShouldWorkVisitor<? extends T>)visitor).visitExp(this);
			else return visitor.visitChildren(this);
		}
	}

	public final ExpContext exp() throws RecognitionException {
		ExpContext _localctx = new ExpContext(_ctx, getState());
		enterRule(_localctx, 18, RULE_exp);
		try {
			setState(108);
			switch (_input.LA(1)) {
			case SUM:
			case DIFF:
			case PRODUKT:
			case QUOSHUNT:
			case MOD:
			case BIGGR:
			case SMALLR:
				enterOuterAlt(_localctx, 1);
				{
				setState(106); math();
				}
				break;
			case EQUALS:
			case DIFFRINT:
				enterOuterAlt(_localctx, 2);
				{
				setState(107); comparison();
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class MathContext extends ParserRuleContext {
		public MathContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_math; }
	 
		public MathContext() { }
		public void copyFrom(MathContext ctx) {
			super.copyFrom(ctx);
		}
	}
	public static class DivContext extends MathContext {
		public ArgsContext args() {
			return getRuleContext(ArgsContext.class,0);
		}
		public DivContext(MathContext ctx) { copyFrom(ctx); }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof ThisShouldWorkVisitor ) return ((ThisShouldWorkVisitor<? extends T>)visitor).visitDiv(this);
			else return visitor.visitChildren(this);
		}
	}
	public static class SubContext extends MathContext {
		public ArgsContext args() {
			return getRuleContext(ArgsContext.class,0);
		}
		public SubContext(MathContext ctx) { copyFrom(ctx); }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof ThisShouldWorkVisitor ) return ((ThisShouldWorkVisitor<? extends T>)visitor).visitSub(this);
			else return visitor.visitChildren(this);
		}
	}
	public static class MultContext extends MathContext {
		public ArgsContext args() {
			return getRuleContext(ArgsContext.class,0);
		}
		public MultContext(MathContext ctx) { copyFrom(ctx); }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof ThisShouldWorkVisitor ) return ((ThisShouldWorkVisitor<? extends T>)visitor).visitMult(this);
			else return visitor.visitChildren(this);
		}
	}
	public static class MinContext extends MathContext {
		public ArgsContext args() {
			return getRuleContext(ArgsContext.class,0);
		}
		public MinContext(MathContext ctx) { copyFrom(ctx); }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof ThisShouldWorkVisitor ) return ((ThisShouldWorkVisitor<? extends T>)visitor).visitMin(this);
			else return visitor.visitChildren(this);
		}
	}
	public static class MaxContext extends MathContext {
		public ArgsContext args() {
			return getRuleContext(ArgsContext.class,0);
		}
		public MaxContext(MathContext ctx) { copyFrom(ctx); }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof ThisShouldWorkVisitor ) return ((ThisShouldWorkVisitor<? extends T>)visitor).visitMax(this);
			else return visitor.visitChildren(this);
		}
	}
	public static class ModuleContext extends MathContext {
		public ArgsContext args() {
			return getRuleContext(ArgsContext.class,0);
		}
		public ModuleContext(MathContext ctx) { copyFrom(ctx); }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof ThisShouldWorkVisitor ) return ((ThisShouldWorkVisitor<? extends T>)visitor).visitModule(this);
			else return visitor.visitChildren(this);
		}
	}
	public static class SumContext extends MathContext {
		public ArgsContext args() {
			return getRuleContext(ArgsContext.class,0);
		}
		public SumContext(MathContext ctx) { copyFrom(ctx); }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof ThisShouldWorkVisitor ) return ((ThisShouldWorkVisitor<? extends T>)visitor).visitSum(this);
			else return visitor.visitChildren(this);
		}
	}

	public final MathContext math() throws RecognitionException {
		MathContext _localctx = new MathContext(_ctx, getState());
		enterRule(_localctx, 20, RULE_math);
		try {
			setState(124);
			switch (_input.LA(1)) {
			case SUM:
				_localctx = new SumContext(_localctx);
				enterOuterAlt(_localctx, 1);
				{
				setState(110); match(SUM);
				setState(111); args();
				}
				break;
			case DIFF:
				_localctx = new SubContext(_localctx);
				enterOuterAlt(_localctx, 2);
				{
				setState(112); match(DIFF);
				setState(113); args();
				}
				break;
			case PRODUKT:
				_localctx = new MultContext(_localctx);
				enterOuterAlt(_localctx, 3);
				{
				setState(114); match(PRODUKT);
				setState(115); args();
				}
				break;
			case QUOSHUNT:
				_localctx = new DivContext(_localctx);
				enterOuterAlt(_localctx, 4);
				{
				setState(116); match(QUOSHUNT);
				setState(117); args();
				}
				break;
			case MOD:
				_localctx = new ModuleContext(_localctx);
				enterOuterAlt(_localctx, 5);
				{
				setState(118); match(MOD);
				setState(119); args();
				}
				break;
			case BIGGR:
				_localctx = new MaxContext(_localctx);
				enterOuterAlt(_localctx, 6);
				{
				setState(120); match(BIGGR);
				setState(121); args();
				}
				break;
			case SMALLR:
				_localctx = new MinContext(_localctx);
				enterOuterAlt(_localctx, 7);
				{
				setState(122); match(SMALLR);
				setState(123); args();
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class ComparisonContext extends ParserRuleContext {
		public ComparisonContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_comparison; }
	 
		public ComparisonContext() { }
		public void copyFrom(ComparisonContext ctx) {
			super.copyFrom(ctx);
		}
	}
	public static class EqualsContext extends ComparisonContext {
		public ArgsContext args() {
			return getRuleContext(ArgsContext.class,0);
		}
		public EqualsContext(ComparisonContext ctx) { copyFrom(ctx); }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof ThisShouldWorkVisitor ) return ((ThisShouldWorkVisitor<? extends T>)visitor).visitEquals(this);
			else return visitor.visitChildren(this);
		}
	}
	public static class DifferContext extends ComparisonContext {
		public ArgsContext args() {
			return getRuleContext(ArgsContext.class,0);
		}
		public DifferContext(ComparisonContext ctx) { copyFrom(ctx); }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof ThisShouldWorkVisitor ) return ((ThisShouldWorkVisitor<? extends T>)visitor).visitDiffer(this);
			else return visitor.visitChildren(this);
		}
	}

	public final ComparisonContext comparison() throws RecognitionException {
		ComparisonContext _localctx = new ComparisonContext(_ctx, getState());
		enterRule(_localctx, 22, RULE_comparison);
		try {
			setState(130);
			switch (_input.LA(1)) {
			case EQUALS:
				_localctx = new EqualsContext(_localctx);
				enterOuterAlt(_localctx, 1);
				{
				setState(126); match(EQUALS);
				setState(127); args();
				}
				break;
			case DIFFRINT:
				_localctx = new DifferContext(_localctx);
				enterOuterAlt(_localctx, 2);
				{
				setState(128); match(DIFFRINT);
				setState(129); args();
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class ArgsContext extends ParserRuleContext {
		public ArgsRightContext argsRight() {
			return getRuleContext(ArgsRightContext.class,0);
		}
		public ArgsLeftContext argsLeft() {
			return getRuleContext(ArgsLeftContext.class,0);
		}
		public ArgsContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_args; }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof ThisShouldWorkVisitor ) return ((ThisShouldWorkVisitor<? extends T>)visitor).visitArgs(this);
			else return visitor.visitChildren(this);
		}
	}

	public final ArgsContext args() throws RecognitionException {
		ArgsContext _localctx = new ArgsContext(_ctx, getState());
		enterRule(_localctx, 24, RULE_args);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(132); argsLeft();
			setState(133); match(AN);
			setState(134); argsRight();
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class ArgsLeftContext extends ParserRuleContext {
		public ExpContext exp() {
			return getRuleContext(ExpContext.class,0);
		}
		public ArgContext arg() {
			return getRuleContext(ArgContext.class,0);
		}
		public ArgsLeftContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_argsLeft; }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof ThisShouldWorkVisitor ) return ((ThisShouldWorkVisitor<? extends T>)visitor).visitArgsLeft(this);
			else return visitor.visitChildren(this);
		}
	}

	public final ArgsLeftContext argsLeft() throws RecognitionException {
		ArgsLeftContext _localctx = new ArgsLeftContext(_ctx, getState());
		enterRule(_localctx, 26, RULE_argsLeft);
		try {
			setState(138);
			switch (_input.LA(1)) {
			case BOOLEANS:
			case STRING:
			case ID:
			case DIGIT:
			case FLOAT:
				enterOuterAlt(_localctx, 1);
				{
				setState(136); arg();
				}
				break;
			case SUM:
			case DIFF:
			case PRODUKT:
			case QUOSHUNT:
			case MOD:
			case BIGGR:
			case SMALLR:
			case EQUALS:
			case DIFFRINT:
				enterOuterAlt(_localctx, 2);
				{
				setState(137); exp();
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class ArgsRightContext extends ParserRuleContext {
		public ExpContext exp() {
			return getRuleContext(ExpContext.class,0);
		}
		public ArgsRightContext argsRight() {
			return getRuleContext(ArgsRightContext.class,0);
		}
		public ArgsLeftContext argsLeft() {
			return getRuleContext(ArgsLeftContext.class,0);
		}
		public ArgContext arg() {
			return getRuleContext(ArgContext.class,0);
		}
		public ArgsRightContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_argsRight; }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof ThisShouldWorkVisitor ) return ((ThisShouldWorkVisitor<? extends T>)visitor).visitArgsRight(this);
			else return visitor.visitChildren(this);
		}
	}

	public final ArgsRightContext argsRight() throws RecognitionException {
		ArgsRightContext _localctx = new ArgsRightContext(_ctx, getState());
		enterRule(_localctx, 28, RULE_argsRight);
		try {
			setState(146);
			switch ( getInterpreter().adaptivePredict(_input,11,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(140); arg();
				}
				break;

			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(141); exp();
				}
				break;

			case 3:
				enterOuterAlt(_localctx, 3);
				{
				setState(142); argsLeft();
				setState(143); match(AN);
				setState(144); argsRight();
				}
				break;
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class LoopContext extends ParserRuleContext {
		public LabelContext label(int i) {
			return getRuleContext(LabelContext.class,i);
		}
		public TerminalNode SEPARATOR(int i) {
			return getToken(ThisShouldWorkParser.SEPARATOR, i);
		}
		public List<TerminalNode> SEPARATOR() { return getTokens(ThisShouldWorkParser.SEPARATOR); }
		public List<LabelContext> label() {
			return getRuleContexts(LabelContext.class);
		}
		public ExpressionContext expression(int i) {
			return getRuleContext(ExpressionContext.class,i);
		}
		public List<ExpressionContext> expression() {
			return getRuleContexts(ExpressionContext.class);
		}
		public LoopContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_loop; }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof ThisShouldWorkVisitor ) return ((ThisShouldWorkVisitor<? extends T>)visitor).visitLoop(this);
			else return visitor.visitChildren(this);
		}
	}

	public final LoopContext loop() throws RecognitionException {
		LoopContext _localctx = new LoopContext(_ctx, getState());
		enterRule(_localctx, 30, RULE_loop);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(148); match(LOOPIN);
			setState(149); label();
			setState(150); match(SEPARATOR);
			setState(156);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while ((((_la) & ~0x3f) == 0 && ((1L << _la) & ((1L << GIMMEH) | (1L << VISIBLE) | (1L << SUM) | (1L << DIFF) | (1L << PRODUKT) | (1L << QUOSHUNT) | (1L << MOD) | (1L << BIGGR) | (1L << SMALLR) | (1L << EQUALS) | (1L << DIFFRINT) | (1L << LOOPIN) | (1L << VARI) | (1L << GTFO) | (1L << ID))) != 0)) {
				{
				{
				setState(151); expression();
				setState(152); match(SEPARATOR);
				}
				}
				setState(158);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(159); match(LOOPOUT);
			setState(160); label();
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class ConditionalContext extends ParserRuleContext {
		public FalseBranchContext falseBranch() {
			return getRuleContext(FalseBranchContext.class,0);
		}
		public TerminalNode SEPARATOR(int i) {
			return getToken(ThisShouldWorkParser.SEPARATOR, i);
		}
		public BreaksContext breaks() {
			return getRuleContext(BreaksContext.class,0);
		}
		public List<TerminalNode> SEPARATOR() { return getTokens(ThisShouldWorkParser.SEPARATOR); }
		public TrueBranchContext trueBranch() {
			return getRuleContext(TrueBranchContext.class,0);
		}
		public ConditionalContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_conditional; }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof ThisShouldWorkVisitor ) return ((ThisShouldWorkVisitor<? extends T>)visitor).visitConditional(this);
			else return visitor.visitChildren(this);
		}
	}

	public final ConditionalContext conditional() throws RecognitionException {
		ConditionalContext _localctx = new ConditionalContext(_ctx, getState());
		enterRule(_localctx, 32, RULE_conditional);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(162); match(3);
			setState(163); match(SEPARATOR);
			setState(167);
			_la = _input.LA(1);
			if (_la==GTFO) {
				{
				setState(164); breaks();
				setState(165); match(SEPARATOR);
				}
			}

			setState(170);
			_la = _input.LA(1);
			if (_la==THEN) {
				{
				setState(169); trueBranch();
				}
			}

			setState(173);
			_la = _input.LA(1);
			if (_la==2) {
				{
				setState(172); falseBranch();
				}
			}

			setState(175); match(IFOUT);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class TrueBranchContext extends ParserRuleContext {
		public TerminalNode SEPARATOR(int i) {
			return getToken(ThisShouldWorkParser.SEPARATOR, i);
		}
		public List<TerminalNode> SEPARATOR() { return getTokens(ThisShouldWorkParser.SEPARATOR); }
		public ExpressionContext expression(int i) {
			return getRuleContext(ExpressionContext.class,i);
		}
		public List<ExpressionContext> expression() {
			return getRuleContexts(ExpressionContext.class);
		}
		public TrueBranchContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_trueBranch; }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof ThisShouldWorkVisitor ) return ((ThisShouldWorkVisitor<? extends T>)visitor).visitTrueBranch(this);
			else return visitor.visitChildren(this);
		}
	}

	public final TrueBranchContext trueBranch() throws RecognitionException {
		TrueBranchContext _localctx = new TrueBranchContext(_ctx, getState());
		enterRule(_localctx, 34, RULE_trueBranch);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(177); match(THEN);
			setState(178); match(SEPARATOR);
			setState(182); 
			_errHandler.sync(this);
			_la = _input.LA(1);
			do {
				{
				{
				setState(179); expression();
				setState(180); match(SEPARATOR);
				}
				}
				setState(184); 
				_errHandler.sync(this);
				_la = _input.LA(1);
			} while ( (((_la) & ~0x3f) == 0 && ((1L << _la) & ((1L << GIMMEH) | (1L << VISIBLE) | (1L << SUM) | (1L << DIFF) | (1L << PRODUKT) | (1L << QUOSHUNT) | (1L << MOD) | (1L << BIGGR) | (1L << SMALLR) | (1L << EQUALS) | (1L << DIFFRINT) | (1L << LOOPIN) | (1L << VARI) | (1L << GTFO) | (1L << ID))) != 0) );
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class FalseBranchContext extends ParserRuleContext {
		public TerminalNode SEPARATOR(int i) {
			return getToken(ThisShouldWorkParser.SEPARATOR, i);
		}
		public List<TerminalNode> SEPARATOR() { return getTokens(ThisShouldWorkParser.SEPARATOR); }
		public ExpressionContext expression(int i) {
			return getRuleContext(ExpressionContext.class,i);
		}
		public List<ExpressionContext> expression() {
			return getRuleContexts(ExpressionContext.class);
		}
		public FalseBranchContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_falseBranch; }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof ThisShouldWorkVisitor ) return ((ThisShouldWorkVisitor<? extends T>)visitor).visitFalseBranch(this);
			else return visitor.visitChildren(this);
		}
	}

	public final FalseBranchContext falseBranch() throws RecognitionException {
		FalseBranchContext _localctx = new FalseBranchContext(_ctx, getState());
		enterRule(_localctx, 36, RULE_falseBranch);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(186); match(2);
			setState(187); match(SEPARATOR);
			setState(191); 
			_errHandler.sync(this);
			_la = _input.LA(1);
			do {
				{
				{
				setState(188); expression();
				setState(189); match(SEPARATOR);
				}
				}
				setState(193); 
				_errHandler.sync(this);
				_la = _input.LA(1);
			} while ( (((_la) & ~0x3f) == 0 && ((1L << _la) & ((1L << GIMMEH) | (1L << VISIBLE) | (1L << SUM) | (1L << DIFF) | (1L << PRODUKT) | (1L << QUOSHUNT) | (1L << MOD) | (1L << BIGGR) | (1L << SMALLR) | (1L << EQUALS) | (1L << DIFFRINT) | (1L << LOOPIN) | (1L << VARI) | (1L << GTFO) | (1L << ID))) != 0) );
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Variable_declarationContext extends ParserRuleContext {
		public VarContext var() {
			return getRuleContext(VarContext.class,0);
		}
		public TerminalNode ITZ() { return getToken(ThisShouldWorkParser.ITZ, 0); }
		public ValContext val() {
			return getRuleContext(ValContext.class,0);
		}
		public Variable_declarationContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_variable_declaration; }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof ThisShouldWorkVisitor ) return ((ThisShouldWorkVisitor<? extends T>)visitor).visitVariable_declaration(this);
			else return visitor.visitChildren(this);
		}
	}

	public final Variable_declarationContext variable_declaration() throws RecognitionException {
		Variable_declarationContext _localctx = new Variable_declarationContext(_ctx, getState());
		enterRule(_localctx, 38, RULE_variable_declaration);
		try {
			setState(202);
			switch ( getInterpreter().adaptivePredict(_input,18,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(195); match(VARI);
				setState(196); var();
				}
				break;

			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(197); match(VARI);
				setState(198); var();
				setState(199); match(ITZ);
				setState(200); val();
				}
				break;
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class VarContext extends ParserRuleContext {
		public TerminalNode ID() { return getToken(ThisShouldWorkParser.ID, 0); }
		public VarContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_var; }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof ThisShouldWorkVisitor ) return ((ThisShouldWorkVisitor<? extends T>)visitor).visitVar(this);
			else return visitor.visitChildren(this);
		}
	}

	public final VarContext var() throws RecognitionException {
		VarContext _localctx = new VarContext(_ctx, getState());
		enterRule(_localctx, 40, RULE_var);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(204); match(ID);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class LabelContext extends ParserRuleContext {
		public TerminalNode ID() { return getToken(ThisShouldWorkParser.ID, 0); }
		public LabelContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_label; }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof ThisShouldWorkVisitor ) return ((ThisShouldWorkVisitor<? extends T>)visitor).visitLabel(this);
			else return visitor.visitChildren(this);
		}
	}

	public final LabelContext label() throws RecognitionException {
		LabelContext _localctx = new LabelContext(_ctx, getState());
		enterRule(_localctx, 42, RULE_label);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(206); match(ID);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class ValContext extends ParserRuleContext {
		public TerminalNode BOOLEANS() { return getToken(ThisShouldWorkParser.BOOLEANS, 0); }
		public TerminalNode DIGIT() { return getToken(ThisShouldWorkParser.DIGIT, 0); }
		public TerminalNode STRING() { return getToken(ThisShouldWorkParser.STRING, 0); }
		public TerminalNode FLOAT() { return getToken(ThisShouldWorkParser.FLOAT, 0); }
		public ValContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_val; }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof ThisShouldWorkVisitor ) return ((ThisShouldWorkVisitor<? extends T>)visitor).visitVal(this);
			else return visitor.visitChildren(this);
		}
	}

	public final ValContext val() throws RecognitionException {
		ValContext _localctx = new ValContext(_ctx, getState());
		enterRule(_localctx, 44, RULE_val);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(208);
			_la = _input.LA(1);
			if ( !((((_la) & ~0x3f) == 0 && ((1L << _la) & ((1L << BOOLEANS) | (1L << STRING) | (1L << DIGIT) | (1L << FLOAT))) != 0)) ) {
			_errHandler.recoverInline(this);
			}
			consume();
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class AssignmentContext extends ParserRuleContext {
		public ExpContext exp() {
			return getRuleContext(ExpContext.class,0);
		}
		public VarContext var() {
			return getRuleContext(VarContext.class,0);
		}
		public ValContext val() {
			return getRuleContext(ValContext.class,0);
		}
		public AssignmentContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_assignment; }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof ThisShouldWorkVisitor ) return ((ThisShouldWorkVisitor<? extends T>)visitor).visitAssignment(this);
			else return visitor.visitChildren(this);
		}
	}

	public final AssignmentContext assignment() throws RecognitionException {
		AssignmentContext _localctx = new AssignmentContext(_ctx, getState());
		enterRule(_localctx, 46, RULE_assignment);
		try {
			setState(218);
			switch ( getInterpreter().adaptivePredict(_input,19,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(210); var();
				setState(211); match(1);
				setState(212); val();
				}
				break;

			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(214); var();
				setState(215); match(1);
				setState(216); exp();
				}
				break;
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static final String _serializedATN =
		"\3\uacf5\uee8c\u4f5d\u8b0d\u4a45\u78bd\u1b2f\u3378\3*\u00df\4\2\t\2\4"+
		"\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t"+
		"\13\4\f\t\f\4\r\t\r\4\16\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22"+
		"\4\23\t\23\4\24\t\24\4\25\t\25\4\26\t\26\4\27\t\27\4\30\t\30\4\31\t\31"+
		"\3\2\3\2\3\2\3\2\3\2\5\28\n\2\3\2\3\2\3\2\3\2\7\2>\n\2\f\2\16\2A\13\2"+
		"\3\2\3\2\3\2\3\3\3\3\3\3\3\3\3\4\3\4\3\5\3\5\3\5\3\5\3\5\3\5\3\5\3\5\3"+
		"\5\3\5\3\5\5\5W\n\5\3\6\3\6\3\7\3\7\3\7\3\b\3\b\3\b\3\b\3\t\3\t\7\td\n"+
		"\t\f\t\16\tg\13\t\3\n\3\n\5\nk\n\n\3\13\3\13\5\13o\n\13\3\f\3\f\3\f\3"+
		"\f\3\f\3\f\3\f\3\f\3\f\3\f\3\f\3\f\3\f\3\f\5\f\177\n\f\3\r\3\r\3\r\3\r"+
		"\5\r\u0085\n\r\3\16\3\16\3\16\3\16\3\17\3\17\5\17\u008d\n\17\3\20\3\20"+
		"\3\20\3\20\3\20\3\20\5\20\u0095\n\20\3\21\3\21\3\21\3\21\3\21\3\21\7\21"+
		"\u009d\n\21\f\21\16\21\u00a0\13\21\3\21\3\21\3\21\3\22\3\22\3\22\3\22"+
		"\3\22\5\22\u00aa\n\22\3\22\5\22\u00ad\n\22\3\22\5\22\u00b0\n\22\3\22\3"+
		"\22\3\23\3\23\3\23\3\23\3\23\6\23\u00b9\n\23\r\23\16\23\u00ba\3\24\3\24"+
		"\3\24\3\24\3\24\6\24\u00c2\n\24\r\24\16\24\u00c3\3\25\3\25\3\25\3\25\3"+
		"\25\3\25\3\25\5\25\u00cd\n\25\3\26\3\26\3\27\3\27\3\30\3\30\3\31\3\31"+
		"\3\31\3\31\3\31\3\31\3\31\3\31\5\31\u00dd\n\31\3\31\2\32\2\4\6\b\n\f\16"+
		"\20\22\24\26\30\32\34\36 \"$&(*,.\60\2\3\5\2  \"\"%&\u00e6\2\62\3\2\2"+
		"\2\4E\3\2\2\2\6I\3\2\2\2\bV\3\2\2\2\nX\3\2\2\2\fZ\3\2\2\2\16]\3\2\2\2"+
		"\20e\3\2\2\2\22j\3\2\2\2\24n\3\2\2\2\26~\3\2\2\2\30\u0084\3\2\2\2\32\u0086"+
		"\3\2\2\2\34\u008c\3\2\2\2\36\u0094\3\2\2\2 \u0096\3\2\2\2\"\u00a4\3\2"+
		"\2\2$\u00b3\3\2\2\2&\u00bc\3\2\2\2(\u00cc\3\2\2\2*\u00ce\3\2\2\2,\u00d0"+
		"\3\2\2\2.\u00d2\3\2\2\2\60\u00dc\3\2\2\2\62\63\7\7\2\2\63\67\7!\2\2\64"+
		"\65\5\4\3\2\65\66\7!\2\2\668\3\2\2\2\67\64\3\2\2\2\678\3\2\2\28?\3\2\2"+
		"\29:\5\b\5\2:;\7!\2\2;>\3\2\2\2<>\7!\2\2=9\3\2\2\2=<\3\2\2\2>A\3\2\2\2"+
		"?=\3\2\2\2?@\3\2\2\2@B\3\2\2\2A?\3\2\2\2BC\7\t\2\2CD\7\2\2\3D\3\3\2\2"+
		"\2EF\7\b\2\2FG\5\6\4\2GH\7\n\2\2H\5\3\2\2\2IJ\7#\2\2J\7\3\2\2\2KW\5(\25"+
		"\2LW\5\f\7\2MW\5\16\b\2NO\5\24\13\2OP\7!\2\2PQ\5\"\22\2QW\3\2\2\2RW\5"+
		"\24\13\2SW\5 \21\2TW\5\60\31\2UW\5\n\6\2VK\3\2\2\2VL\3\2\2\2VM\3\2\2\2"+
		"VN\3\2\2\2VR\3\2\2\2VS\3\2\2\2VT\3\2\2\2VU\3\2\2\2W\t\3\2\2\2XY\7\37\2"+
		"\2Y\13\3\2\2\2Z[\7\13\2\2[\\\5*\26\2\\\r\3\2\2\2]^\7\f\2\2^_\5\20\t\2"+
		"_`\7\6\2\2`\17\3\2\2\2ad\7\"\2\2bd\5*\26\2ca\3\2\2\2cb\3\2\2\2dg\3\2\2"+
		"\2ec\3\2\2\2ef\3\2\2\2f\21\3\2\2\2ge\3\2\2\2hk\5.\30\2ik\5*\26\2jh\3\2"+
		"\2\2ji\3\2\2\2k\23\3\2\2\2lo\5\26\f\2mo\5\30\r\2nl\3\2\2\2nm\3\2\2\2o"+
		"\25\3\2\2\2pq\7\r\2\2q\177\5\32\16\2rs\7\16\2\2s\177\5\32\16\2tu\7\17"+
		"\2\2u\177\5\32\16\2vw\7\20\2\2w\177\5\32\16\2xy\7\21\2\2y\177\5\32\16"+
		"\2z{\7\22\2\2{\177\5\32\16\2|}\7\23\2\2}\177\5\32\16\2~p\3\2\2\2~r\3\2"+
		"\2\2~t\3\2\2\2~v\3\2\2\2~x\3\2\2\2~z\3\2\2\2~|\3\2\2\2\177\27\3\2\2\2"+
		"\u0080\u0081\7\24\2\2\u0081\u0085\5\32\16\2\u0082\u0083\7\25\2\2\u0083"+
		"\u0085\5\32\16\2\u0084\u0080\3\2\2\2\u0084\u0082\3\2\2\2\u0085\31\3\2"+
		"\2\2\u0086\u0087\5\34\17\2\u0087\u0088\7\26\2\2\u0088\u0089\5\36\20\2"+
		"\u0089\33\3\2\2\2\u008a\u008d\5\22\n\2\u008b\u008d\5\24\13\2\u008c\u008a"+
		"\3\2\2\2\u008c\u008b\3\2\2\2\u008d\35\3\2\2\2\u008e\u0095\5\22\n\2\u008f"+
		"\u0095\5\24\13\2\u0090\u0091\5\34\17\2\u0091\u0092\7\26\2\2\u0092\u0093"+
		"\5\36\20\2\u0093\u0095\3\2\2\2\u0094\u008e\3\2\2\2\u0094\u008f\3\2\2\2"+
		"\u0094\u0090\3\2\2\2\u0095\37\3\2\2\2\u0096\u0097\7\27\2\2\u0097\u0098"+
		"\5,\27\2\u0098\u009e\7!\2\2\u0099\u009a\5\b\5\2\u009a\u009b\7!\2\2\u009b"+
		"\u009d\3\2\2\2\u009c\u0099\3\2\2\2\u009d\u00a0\3\2\2\2\u009e\u009c\3\2"+
		"\2\2\u009e\u009f\3\2\2\2\u009f\u00a1\3\2\2\2\u00a0\u009e\3\2\2\2\u00a1"+
		"\u00a2\7\30\2\2\u00a2\u00a3\5,\27\2\u00a3!\3\2\2\2\u00a4\u00a5\7\5\2\2"+
		"\u00a5\u00a9\7!\2\2\u00a6\u00a7\5\n\6\2\u00a7\u00a8\7!\2\2\u00a8\u00aa"+
		"\3\2\2\2\u00a9\u00a6\3\2\2\2\u00a9\u00aa\3\2\2\2\u00aa\u00ac\3\2\2\2\u00ab"+
		"\u00ad\5$\23\2\u00ac\u00ab\3\2\2\2\u00ac\u00ad\3\2\2\2\u00ad\u00af\3\2"+
		"\2\2\u00ae\u00b0\5&\24\2\u00af\u00ae\3\2\2\2\u00af\u00b0\3\2\2\2\u00b0"+
		"\u00b1\3\2\2\2\u00b1\u00b2\7\32\2\2\u00b2#\3\2\2\2\u00b3\u00b4\7\33\2"+
		"\2\u00b4\u00b8\7!\2\2\u00b5\u00b6\5\b\5\2\u00b6\u00b7\7!\2\2\u00b7\u00b9"+
		"\3\2\2\2\u00b8\u00b5\3\2\2\2\u00b9\u00ba\3\2\2\2\u00ba\u00b8\3\2\2\2\u00ba"+
		"\u00bb\3\2\2\2\u00bb%\3\2\2\2\u00bc\u00bd\7\4\2\2\u00bd\u00c1\7!\2\2\u00be"+
		"\u00bf\5\b\5\2\u00bf\u00c0\7!\2\2\u00c0\u00c2\3\2\2\2\u00c1\u00be\3\2"+
		"\2\2\u00c2\u00c3\3\2\2\2\u00c3\u00c1\3\2\2\2\u00c3\u00c4\3\2\2\2\u00c4"+
		"\'\3\2\2\2\u00c5\u00c6\7\35\2\2\u00c6\u00cd\5*\26\2\u00c7\u00c8\7\35\2"+
		"\2\u00c8\u00c9\5*\26\2\u00c9\u00ca\7\36\2\2\u00ca\u00cb\5.\30\2\u00cb"+
		"\u00cd\3\2\2\2\u00cc\u00c5\3\2\2\2\u00cc\u00c7\3\2\2\2\u00cd)\3\2\2\2"+
		"\u00ce\u00cf\7#\2\2\u00cf+\3\2\2\2\u00d0\u00d1\7#\2\2\u00d1-\3\2\2\2\u00d2"+
		"\u00d3\t\2\2\2\u00d3/\3\2\2\2\u00d4\u00d5\5*\26\2\u00d5\u00d6\7\3\2\2"+
		"\u00d6\u00d7\5.\30\2\u00d7\u00dd\3\2\2\2\u00d8\u00d9\5*\26\2\u00d9\u00da"+
		"\7\3\2\2\u00da\u00db\5\24\13\2\u00db\u00dd\3\2\2\2\u00dc\u00d4\3\2\2\2"+
		"\u00dc\u00d8\3\2\2\2\u00dd\61\3\2\2\2\26\67=?Vcejn~\u0084\u008c\u0094"+
		"\u009e\u00a9\u00ac\u00af\u00ba\u00c3\u00cc\u00dc";
	public static final ATN _ATN =
		ATNSimulator.deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}