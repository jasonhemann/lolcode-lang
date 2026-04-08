// Generated from Small.g4 by ANTLR 4.0
import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.misc.*;
import org.antlr.v4.runtime.tree.*;
import java.util.List;
import java.util.Iterator;
import java.util.ArrayList;

@SuppressWarnings({"all", "warnings", "unchecked", "unused", "cast"})
public class SmallParser extends Parser {
	protected static final DFA[] _decisionToDFA;
	protected static final PredictionContextCache _sharedContextCache =
		new PredictionContextCache();
	public static final int
		T__51=1, T__50=2, T__49=3, T__48=4, T__47=5, T__46=6, T__45=7, T__44=8, 
		T__43=9, T__42=10, T__41=11, T__40=12, T__39=13, T__38=14, T__37=15, T__36=16, 
		T__35=17, T__34=18, T__33=19, T__32=20, T__31=21, T__30=22, T__29=23, 
		T__28=24, T__27=25, T__26=26, T__25=27, T__24=28, T__23=29, T__22=30, 
		T__21=31, T__20=32, T__19=33, T__18=34, T__17=35, T__16=36, T__15=37, 
		T__14=38, T__13=39, T__12=40, T__11=41, T__10=42, T__9=43, T__8=44, T__7=45, 
		T__6=46, T__5=47, T__4=48, T__3=49, T__2=50, T__1=51, T__0=52, APOSTROPHE=53, 
		BOOLEAN=54, ID=55, INTEGER=56, WS=57, COMMENT=58, MULTICOMMENT=59, BANG=60, 
		STRING=61, NEWLINE=62;
	public static final String[] tokenNames = {
		"<INVALID>", "'OIC'", "'NUMBAR'", "'UPPIN'", "'WILE'", "'BOTH OF'", "'1.2'", 
		"'MEBBE'", "'BUKKIT'", "'GIMMEH'", "'YARN'", "'NOOB'", "'HAI'", "'QUOSHUNT OF'", 
		"'SRS'", "'BANG'", "'AN'", "'MKAY'", "'PRODUKT OF'", "'VISIBLE'", "'1.1'", 
		"'KTHXBYE'", "'NUMBR'", "'EITHER OF'", "'NOT'", "'NERFIN'", "'ITZ A'", 
		"'IM OUTTA YR'", "'BOTH SAEM'", "','", "'SUM OF'", "'SMALLR OF'", "'BIGGR OF'", 
		"'WON OF'", "'ALL OF'", "'DIFFRINT'", "'1.0'", "'SMOOSH'", "'O RLY?'", 
		"'DIFF OF'", "'ITZ LIEK A'", "'NO WAI'", "'IS NOW A'", "'YA RLY'", "'TIL'", 
		"'ITZ'", "'TROOF'", "'R'", "'MOD OF'", "'YR'", "'ANY OF'", "'IM IN YR'", 
		"'HAS A'", "''Z'", "BOOLEAN", "ID", "INTEGER", "WS", "COMMENT", "MULTICOMMENT", 
		"'!'", "STRING", "NEWLINE"
	};
	public static final int
		RULE_file = 0, RULE_block = 1, RULE_identifier = 2, RULE_statement = 3, 
		RULE_print = 4, RULE_assignment = 5, RULE_declaration = 6, RULE_init = 7, 
		RULE_ifthenelse = 8, RULE_elseifcond = 9, RULE_elsecond = 10, RULE_loop = 11, 
		RULE_loopupdate = 12, RULE_loopupdateop = 13, RULE_loopguard = 14, RULE_input = 15, 
		RULE_cast = 16, RULE_exprlist = 17, RULE_emptyline = 18, RULE_expr = 19, 
		RULE_opexpr = 20, RULE_unaryop = 21, RULE_binaryop = 22, RULE_binaryoptype = 23, 
		RULE_naryop = 24, RULE_naryoptype = 25, RULE_naryopargs = 26, RULE_naryoparg = 27, 
		RULE_constant = 28, RULE_type = 29;
	public static final String[] ruleNames = {
		"file", "block", "identifier", "statement", "print", "assignment", "declaration", 
		"init", "ifthenelse", "elseifcond", "elsecond", "loop", "loopupdate", 
		"loopupdateop", "loopguard", "input", "cast", "exprlist", "emptyline", 
		"expr", "opexpr", "unaryop", "binaryop", "binaryoptype", "naryop", "naryoptype", 
		"naryopargs", "naryoparg", "constant", "type"
	};

	@Override
	public String getGrammarFileName() { return "Small.g4"; }

	@Override
	public String[] getTokenNames() { return tokenNames; }

	@Override
	public String[] getRuleNames() { return ruleNames; }

	@Override
	public ATN getATN() { return _ATN; }

	public SmallParser(TokenStream input) {
		super(input);
		_interp = new ParserATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}
	public static class FileContext extends ParserRuleContext {
		public List<TerminalNode> NEWLINE() { return getTokens(SmallParser.NEWLINE); }
		public TerminalNode EOF() { return getToken(SmallParser.EOF, 0); }
		public BlockContext block() {
			return getRuleContext(BlockContext.class,0);
		}
		public TerminalNode NEWLINE(int i) {
			return getToken(SmallParser.NEWLINE, i);
		}
		public FileContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_file; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SmallListener ) ((SmallListener)listener).enterFile(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SmallListener ) ((SmallListener)listener).exitFile(this);
		}
	}

	public final FileContext file() throws RecognitionException {
		FileContext _localctx = new FileContext(_ctx, getState());
		enterRule(_localctx, 0, RULE_file);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(60); match(12);
			setState(61);
			_la = _input.LA(1);
			if ( !((((_la) & ~0x3f) == 0 && ((1L << _la) & ((1L << 6) | (1L << 20) | (1L << 36))) != 0)) ) {
			_errHandler.recoverInline(this);
			}
			consume();
			setState(62); match(NEWLINE);
			setState(63); block();
			setState(64); match(21);
			setState(65); match(NEWLINE);
			setState(66); match(EOF);
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

	public static class BlockContext extends ParserRuleContext {
		public List<StatementContext> statement() {
			return getRuleContexts(StatementContext.class);
		}
		public StatementContext statement(int i) {
			return getRuleContext(StatementContext.class,i);
		}
		public BlockContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_block; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SmallListener ) ((SmallListener)listener).enterBlock(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SmallListener ) ((SmallListener)listener).exitBlock(this);
		}
	}

	public final BlockContext block() throws RecognitionException {
		BlockContext _localctx = new BlockContext(_ctx, getState());
		enterRule(_localctx, 2, RULE_block);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(71);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while ((((_la) & ~0x3f) == 0 && ((1L << _la) & ((1L << 5) | (1L << 9) | (1L << 13) | (1L << 14) | (1L << 18) | (1L << 19) | (1L << 23) | (1L << 24) | (1L << 28) | (1L << 30) | (1L << 31) | (1L << 32) | (1L << 33) | (1L << 34) | (1L << 35) | (1L << 37) | (1L << 38) | (1L << 39) | (1L << 48) | (1L << 50) | (1L << 51) | (1L << BOOLEAN) | (1L << ID) | (1L << INTEGER) | (1L << STRING) | (1L << NEWLINE))) != 0)) {
				{
				{
				setState(68); statement();
				}
				}
				setState(73);
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

	public static class IdentifierContext extends ParserRuleContext {
		public ConstantContext constant() {
			return getRuleContext(ConstantContext.class,0);
		}
		public TerminalNode APOSTROPHE() { return getToken(SmallParser.APOSTROPHE, 0); }
		public TerminalNode ID() { return getToken(SmallParser.ID, 0); }
		public ExprContext expr() {
			return getRuleContext(ExprContext.class,0);
		}
		public IdentifierContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_identifier; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SmallListener ) ((SmallListener)listener).enterIdentifier(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SmallListener ) ((SmallListener)listener).exitIdentifier(this);
		}
	}

	public final IdentifierContext identifier() throws RecognitionException {
		IdentifierContext _localctx = new IdentifierContext(_ctx, getState());
		enterRule(_localctx, 4, RULE_identifier);
		int _la;
		try {
			setState(84);
			switch ( getInterpreter().adaptivePredict(_input,3,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(74); match(ID);
				}
				break;

			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(80);
				_la = _input.LA(1);
				if ((((_la) & ~0x3f) == 0 && ((1L << _la) & ((1L << BOOLEAN) | (1L << ID) | (1L << INTEGER) | (1L << STRING))) != 0)) {
					{
					setState(77);
					switch (_input.LA(1)) {
					case ID:
						{
						setState(75); match(ID);
						}
						break;
					case BOOLEAN:
					case INTEGER:
					case STRING:
						{
						setState(76); constant();
						}
						break;
					default:
						throw new NoViableAltException(this);
					}
					setState(79); match(APOSTROPHE);
					}
				}

				setState(82); match(14);
				setState(83); expr();
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

	public static class StatementContext extends ParserRuleContext {
		public InputContext input() {
			return getRuleContext(InputContext.class,0);
		}
		public IfthenelseContext ifthenelse() {
			return getRuleContext(IfthenelseContext.class,0);
		}
		public AssignmentContext assignment() {
			return getRuleContext(AssignmentContext.class,0);
		}
		public DeclarationContext declaration() {
			return getRuleContext(DeclarationContext.class,0);
		}
		public CastContext cast() {
			return getRuleContext(CastContext.class,0);
		}
		public TerminalNode NEWLINE() { return getToken(SmallParser.NEWLINE, 0); }
		public LoopContext loop() {
			return getRuleContext(LoopContext.class,0);
		}
		public ExprContext expr() {
			return getRuleContext(ExprContext.class,0);
		}
		public PrintContext print() {
			return getRuleContext(PrintContext.class,0);
		}
		public EmptylineContext emptyline() {
			return getRuleContext(EmptylineContext.class,0);
		}
		public StatementContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_statement; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SmallListener ) ((SmallListener)listener).enterStatement(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SmallListener ) ((SmallListener)listener).exitStatement(this);
		}
	}

	public final StatementContext statement() throws RecognitionException {
		StatementContext _localctx = new StatementContext(_ctx, getState());
		enterRule(_localctx, 6, RULE_statement);
		try {
			setState(97);
			switch ( getInterpreter().adaptivePredict(_input,4,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(86); print();
				}
				break;

			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(87); assignment();
				}
				break;

			case 3:
				enterOuterAlt(_localctx, 3);
				{
				setState(88); declaration();
				}
				break;

			case 4:
				enterOuterAlt(_localctx, 4);
				{
				setState(89); ifthenelse();
				}
				break;

			case 5:
				enterOuterAlt(_localctx, 5);
				{
				setState(90); loop();
				}
				break;

			case 6:
				enterOuterAlt(_localctx, 6);
				{
				setState(91); input();
				}
				break;

			case 7:
				enterOuterAlt(_localctx, 7);
				{
				setState(92); cast();
				}
				break;

			case 8:
				enterOuterAlt(_localctx, 8);
				{
				setState(93); expr();
				setState(94); match(NEWLINE);
				}
				break;

			case 9:
				enterOuterAlt(_localctx, 9);
				{
				setState(96); emptyline();
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

	public static class PrintContext extends ParserRuleContext {
		public TerminalNode NEWLINE() { return getToken(SmallParser.NEWLINE, 0); }
		public ExprlistContext exprlist() {
			return getRuleContext(ExprlistContext.class,0);
		}
		public PrintContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_print; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SmallListener ) ((SmallListener)listener).enterPrint(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SmallListener ) ((SmallListener)listener).exitPrint(this);
		}
	}

	public final PrintContext print() throws RecognitionException {
		PrintContext _localctx = new PrintContext(_ctx, getState());
		enterRule(_localctx, 8, RULE_print);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(99); match(19);
			setState(100); exprlist();
			setState(102);
			_la = _input.LA(1);
			if (_la==15) {
				{
				setState(101); match(15);
				}
			}

			setState(104); match(NEWLINE);
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
		public TerminalNode NEWLINE() { return getToken(SmallParser.NEWLINE, 0); }
		public ExprContext expr() {
			return getRuleContext(ExprContext.class,0);
		}
		public IdentifierContext identifier() {
			return getRuleContext(IdentifierContext.class,0);
		}
		public AssignmentContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_assignment; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SmallListener ) ((SmallListener)listener).enterAssignment(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SmallListener ) ((SmallListener)listener).exitAssignment(this);
		}
	}

	public final AssignmentContext assignment() throws RecognitionException {
		AssignmentContext _localctx = new AssignmentContext(_ctx, getState());
		enterRule(_localctx, 10, RULE_assignment);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(106); identifier();
			setState(107); match(47);
			setState(108); expr();
			setState(109); match(NEWLINE);
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

	public static class DeclarationContext extends ParserRuleContext {
		public IdentifierContext identifier(int i) {
			return getRuleContext(IdentifierContext.class,i);
		}
		public InitContext init() {
			return getRuleContext(InitContext.class,0);
		}
		public List<IdentifierContext> identifier() {
			return getRuleContexts(IdentifierContext.class);
		}
		public DeclarationContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_declaration; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SmallListener ) ((SmallListener)listener).enterDeclaration(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SmallListener ) ((SmallListener)listener).exitDeclaration(this);
		}
	}

	public final DeclarationContext declaration() throws RecognitionException {
		DeclarationContext _localctx = new DeclarationContext(_ctx, getState());
		enterRule(_localctx, 12, RULE_declaration);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(111); identifier();
			setState(112); match(52);
			setState(113); identifier();
			setState(114); init();
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

	public static class InitContext extends ParserRuleContext {
		public TerminalNode NEWLINE() { return getToken(SmallParser.NEWLINE, 0); }
		public ExprContext expr() {
			return getRuleContext(ExprContext.class,0);
		}
		public TypeContext type() {
			return getRuleContext(TypeContext.class,0);
		}
		public IdentifierContext identifier() {
			return getRuleContext(IdentifierContext.class,0);
		}
		public InitContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_init; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SmallListener ) ((SmallListener)listener).enterInit(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SmallListener ) ((SmallListener)listener).exitInit(this);
		}
	}

	public final InitContext init() throws RecognitionException {
		InitContext _localctx = new InitContext(_ctx, getState());
		enterRule(_localctx, 14, RULE_init);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(122);
			switch (_input.LA(1)) {
			case 45:
				{
				setState(116); match(45);
				setState(117); expr();
				}
				break;
			case 26:
				{
				setState(118); match(26);
				setState(119); type();
				}
				break;
			case 40:
				{
				setState(120); match(40);
				setState(121); identifier();
				}
				break;
			case NEWLINE:
				break;
			default:
				throw new NoViableAltException(this);
			}
			setState(124); match(NEWLINE);
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

	public static class IfthenelseContext extends ParserRuleContext {
		public ElsecondContext elsecond() {
			return getRuleContext(ElsecondContext.class,0);
		}
		public List<TerminalNode> NEWLINE() { return getTokens(SmallParser.NEWLINE); }
		public BlockContext block() {
			return getRuleContext(BlockContext.class,0);
		}
		public ElseifcondContext elseifcond(int i) {
			return getRuleContext(ElseifcondContext.class,i);
		}
		public TerminalNode NEWLINE(int i) {
			return getToken(SmallParser.NEWLINE, i);
		}
		public List<ElseifcondContext> elseifcond() {
			return getRuleContexts(ElseifcondContext.class);
		}
		public IfthenelseContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_ifthenelse; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SmallListener ) ((SmallListener)listener).enterIfthenelse(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SmallListener ) ((SmallListener)listener).exitIfthenelse(this);
		}
	}

	public final IfthenelseContext ifthenelse() throws RecognitionException {
		IfthenelseContext _localctx = new IfthenelseContext(_ctx, getState());
		enterRule(_localctx, 16, RULE_ifthenelse);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(126); match(38);
			setState(127); match(NEWLINE);
			setState(128); match(43);
			setState(129); match(NEWLINE);
			setState(130); block();
			setState(134);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==7) {
				{
				{
				setState(131); elseifcond();
				}
				}
				setState(136);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(138);
			_la = _input.LA(1);
			if (_la==41) {
				{
				setState(137); elsecond();
				}
			}

			setState(140); match(1);
			setState(141); match(NEWLINE);
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

	public static class ElseifcondContext extends ParserRuleContext {
		public TerminalNode NEWLINE() { return getToken(SmallParser.NEWLINE, 0); }
		public BlockContext block() {
			return getRuleContext(BlockContext.class,0);
		}
		public ExprContext expr() {
			return getRuleContext(ExprContext.class,0);
		}
		public ElseifcondContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_elseifcond; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SmallListener ) ((SmallListener)listener).enterElseifcond(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SmallListener ) ((SmallListener)listener).exitElseifcond(this);
		}
	}

	public final ElseifcondContext elseifcond() throws RecognitionException {
		ElseifcondContext _localctx = new ElseifcondContext(_ctx, getState());
		enterRule(_localctx, 18, RULE_elseifcond);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(143); match(7);
			setState(144); expr();
			setState(145); match(NEWLINE);
			setState(146); block();
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

	public static class ElsecondContext extends ParserRuleContext {
		public TerminalNode NEWLINE() { return getToken(SmallParser.NEWLINE, 0); }
		public BlockContext block() {
			return getRuleContext(BlockContext.class,0);
		}
		public ElsecondContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_elsecond; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SmallListener ) ((SmallListener)listener).enterElsecond(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SmallListener ) ((SmallListener)listener).exitElsecond(this);
		}
	}

	public final ElsecondContext elsecond() throws RecognitionException {
		ElsecondContext _localctx = new ElsecondContext(_ctx, getState());
		enterRule(_localctx, 20, RULE_elsecond);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(148); match(41);
			setState(149); match(NEWLINE);
			setState(150); block();
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
		public IdentifierContext identifier(int i) {
			return getRuleContext(IdentifierContext.class,i);
		}
		public LoopguardContext loopguard() {
			return getRuleContext(LoopguardContext.class,0);
		}
		public List<TerminalNode> NEWLINE() { return getTokens(SmallParser.NEWLINE); }
		public BlockContext block() {
			return getRuleContext(BlockContext.class,0);
		}
		public TerminalNode NEWLINE(int i) {
			return getToken(SmallParser.NEWLINE, i);
		}
		public LoopupdateContext loopupdate() {
			return getRuleContext(LoopupdateContext.class,0);
		}
		public List<IdentifierContext> identifier() {
			return getRuleContexts(IdentifierContext.class);
		}
		public LoopContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_loop; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SmallListener ) ((SmallListener)listener).enterLoop(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SmallListener ) ((SmallListener)listener).exitLoop(this);
		}
	}

	public final LoopContext loop() throws RecognitionException {
		LoopContext _localctx = new LoopContext(_ctx, getState());
		enterRule(_localctx, 22, RULE_loop);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(152); match(51);
			setState(153); identifier();
			setState(155);
			_la = _input.LA(1);
			if (_la==3 || _la==25) {
				{
				setState(154); loopupdate();
				}
			}

			setState(158);
			_la = _input.LA(1);
			if (_la==4 || _la==44) {
				{
				setState(157); loopguard();
				}
			}

			setState(160); match(NEWLINE);
			setState(161); block();
			setState(162); match(27);
			setState(163); identifier();
			setState(164); match(NEWLINE);
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

	public static class LoopupdateContext extends ParserRuleContext {
		public LoopupdateopContext loopupdateop() {
			return getRuleContext(LoopupdateopContext.class,0);
		}
		public IdentifierContext identifier() {
			return getRuleContext(IdentifierContext.class,0);
		}
		public LoopupdateContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_loopupdate; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SmallListener ) ((SmallListener)listener).enterLoopupdate(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SmallListener ) ((SmallListener)listener).exitLoopupdate(this);
		}
	}

	public final LoopupdateContext loopupdate() throws RecognitionException {
		LoopupdateContext _localctx = new LoopupdateContext(_ctx, getState());
		enterRule(_localctx, 24, RULE_loopupdate);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(166); loopupdateop();
			setState(167); match(49);
			setState(168); identifier();
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

	public static class LoopupdateopContext extends ParserRuleContext {
		public LoopupdateopContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_loopupdateop; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SmallListener ) ((SmallListener)listener).enterLoopupdateop(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SmallListener ) ((SmallListener)listener).exitLoopupdateop(this);
		}
	}

	public final LoopupdateopContext loopupdateop() throws RecognitionException {
		LoopupdateopContext _localctx = new LoopupdateopContext(_ctx, getState());
		enterRule(_localctx, 26, RULE_loopupdateop);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(170);
			_la = _input.LA(1);
			if ( !(_la==3 || _la==25) ) {
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

	public static class LoopguardContext extends ParserRuleContext {
		public ExprContext expr() {
			return getRuleContext(ExprContext.class,0);
		}
		public LoopguardContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_loopguard; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SmallListener ) ((SmallListener)listener).enterLoopguard(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SmallListener ) ((SmallListener)listener).exitLoopguard(this);
		}
	}

	public final LoopguardContext loopguard() throws RecognitionException {
		LoopguardContext _localctx = new LoopguardContext(_ctx, getState());
		enterRule(_localctx, 28, RULE_loopguard);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(172);
			_la = _input.LA(1);
			if ( !(_la==4 || _la==44) ) {
			_errHandler.recoverInline(this);
			}
			consume();
			setState(173); expr();
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

	public static class InputContext extends ParserRuleContext {
		public TerminalNode NEWLINE() { return getToken(SmallParser.NEWLINE, 0); }
		public IdentifierContext identifier() {
			return getRuleContext(IdentifierContext.class,0);
		}
		public InputContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_input; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SmallListener ) ((SmallListener)listener).enterInput(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SmallListener ) ((SmallListener)listener).exitInput(this);
		}
	}

	public final InputContext input() throws RecognitionException {
		InputContext _localctx = new InputContext(_ctx, getState());
		enterRule(_localctx, 30, RULE_input);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(175); match(9);
			setState(176); identifier();
			setState(177); match(NEWLINE);
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

	public static class CastContext extends ParserRuleContext {
		public TerminalNode NEWLINE() { return getToken(SmallParser.NEWLINE, 0); }
		public TypeContext type() {
			return getRuleContext(TypeContext.class,0);
		}
		public IdentifierContext identifier() {
			return getRuleContext(IdentifierContext.class,0);
		}
		public CastContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_cast; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SmallListener ) ((SmallListener)listener).enterCast(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SmallListener ) ((SmallListener)listener).exitCast(this);
		}
	}

	public final CastContext cast() throws RecognitionException {
		CastContext _localctx = new CastContext(_ctx, getState());
		enterRule(_localctx, 32, RULE_cast);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(179); identifier();
			setState(180); match(42);
			setState(181); type();
			setState(182); match(NEWLINE);
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

	public static class ExprlistContext extends ParserRuleContext {
		public ExprContext expr(int i) {
			return getRuleContext(ExprContext.class,i);
		}
		public List<ExprContext> expr() {
			return getRuleContexts(ExprContext.class);
		}
		public ExprlistContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_exprlist; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SmallListener ) ((SmallListener)listener).enterExprlist(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SmallListener ) ((SmallListener)listener).exitExprlist(this);
		}
	}

	public final ExprlistContext exprlist() throws RecognitionException {
		ExprlistContext _localctx = new ExprlistContext(_ctx, getState());
		enterRule(_localctx, 34, RULE_exprlist);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(184); expr();
			setState(189);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==29) {
				{
				{
				setState(185); match(29);
				setState(186); expr();
				}
				}
				setState(191);
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

	public static class EmptylineContext extends ParserRuleContext {
		public TerminalNode NEWLINE() { return getToken(SmallParser.NEWLINE, 0); }
		public EmptylineContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_emptyline; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SmallListener ) ((SmallListener)listener).enterEmptyline(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SmallListener ) ((SmallListener)listener).exitEmptyline(this);
		}
	}

	public final EmptylineContext emptyline() throws RecognitionException {
		EmptylineContext _localctx = new EmptylineContext(_ctx, getState());
		enterRule(_localctx, 36, RULE_emptyline);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(192); match(NEWLINE);
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

	public static class ExprContext extends ParserRuleContext {
		public ConstantContext constant() {
			return getRuleContext(ConstantContext.class,0);
		}
		public IdentifierContext identifier() {
			return getRuleContext(IdentifierContext.class,0);
		}
		public OpexprContext opexpr() {
			return getRuleContext(OpexprContext.class,0);
		}
		public ExprContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_expr; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SmallListener ) ((SmallListener)listener).enterExpr(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SmallListener ) ((SmallListener)listener).exitExpr(this);
		}
	}

	public final ExprContext expr() throws RecognitionException {
		ExprContext _localctx = new ExprContext(_ctx, getState());
		enterRule(_localctx, 38, RULE_expr);
		try {
			setState(197);
			switch ( getInterpreter().adaptivePredict(_input,12,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(194); constant();
				}
				break;

			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(195); identifier();
				}
				break;

			case 3:
				enterOuterAlt(_localctx, 3);
				{
				setState(196); opexpr();
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

	public static class OpexprContext extends ParserRuleContext {
		public UnaryopContext unaryop() {
			return getRuleContext(UnaryopContext.class,0);
		}
		public BinaryopContext binaryop() {
			return getRuleContext(BinaryopContext.class,0);
		}
		public NaryopContext naryop() {
			return getRuleContext(NaryopContext.class,0);
		}
		public OpexprContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_opexpr; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SmallListener ) ((SmallListener)listener).enterOpexpr(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SmallListener ) ((SmallListener)listener).exitOpexpr(this);
		}
	}

	public final OpexprContext opexpr() throws RecognitionException {
		OpexprContext _localctx = new OpexprContext(_ctx, getState());
		enterRule(_localctx, 40, RULE_opexpr);
		try {
			setState(202);
			switch (_input.LA(1)) {
			case 24:
				enterOuterAlt(_localctx, 1);
				{
				setState(199); unaryop();
				}
				break;
			case 5:
			case 13:
			case 18:
			case 23:
			case 28:
			case 30:
			case 31:
			case 32:
			case 33:
			case 35:
			case 39:
			case 48:
				enterOuterAlt(_localctx, 2);
				{
				setState(200); binaryop();
				}
				break;
			case 34:
			case 37:
			case 50:
				enterOuterAlt(_localctx, 3);
				{
				setState(201); naryop();
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

	public static class UnaryopContext extends ParserRuleContext {
		public ExprContext expr() {
			return getRuleContext(ExprContext.class,0);
		}
		public UnaryopContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_unaryop; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SmallListener ) ((SmallListener)listener).enterUnaryop(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SmallListener ) ((SmallListener)listener).exitUnaryop(this);
		}
	}

	public final UnaryopContext unaryop() throws RecognitionException {
		UnaryopContext _localctx = new UnaryopContext(_ctx, getState());
		enterRule(_localctx, 42, RULE_unaryop);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(204); match(24);
			setState(205); expr();
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

	public static class BinaryopContext extends ParserRuleContext {
		public ExprContext expr(int i) {
			return getRuleContext(ExprContext.class,i);
		}
		public BinaryoptypeContext binaryoptype() {
			return getRuleContext(BinaryoptypeContext.class,0);
		}
		public List<ExprContext> expr() {
			return getRuleContexts(ExprContext.class);
		}
		public BinaryopContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_binaryop; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SmallListener ) ((SmallListener)listener).enterBinaryop(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SmallListener ) ((SmallListener)listener).exitBinaryop(this);
		}
	}

	public final BinaryopContext binaryop() throws RecognitionException {
		BinaryopContext _localctx = new BinaryopContext(_ctx, getState());
		enterRule(_localctx, 44, RULE_binaryop);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(207); binaryoptype();
			setState(208); expr();
			setState(210);
			_la = _input.LA(1);
			if (_la==16) {
				{
				setState(209); match(16);
				}
			}

			setState(212); expr();
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

	public static class BinaryoptypeContext extends ParserRuleContext {
		public BinaryoptypeContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_binaryoptype; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SmallListener ) ((SmallListener)listener).enterBinaryoptype(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SmallListener ) ((SmallListener)listener).exitBinaryoptype(this);
		}
	}

	public final BinaryoptypeContext binaryoptype() throws RecognitionException {
		BinaryoptypeContext _localctx = new BinaryoptypeContext(_ctx, getState());
		enterRule(_localctx, 46, RULE_binaryoptype);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(214);
			_la = _input.LA(1);
			if ( !((((_la) & ~0x3f) == 0 && ((1L << _la) & ((1L << 5) | (1L << 13) | (1L << 18) | (1L << 23) | (1L << 28) | (1L << 30) | (1L << 31) | (1L << 32) | (1L << 33) | (1L << 35) | (1L << 39) | (1L << 48))) != 0)) ) {
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

	public static class NaryopContext extends ParserRuleContext {
		public NaryopargsContext naryopargs() {
			return getRuleContext(NaryopargsContext.class,0);
		}
		public NaryoptypeContext naryoptype() {
			return getRuleContext(NaryoptypeContext.class,0);
		}
		public NaryopContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_naryop; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SmallListener ) ((SmallListener)listener).enterNaryop(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SmallListener ) ((SmallListener)listener).exitNaryop(this);
		}
	}

	public final NaryopContext naryop() throws RecognitionException {
		NaryopContext _localctx = new NaryopContext(_ctx, getState());
		enterRule(_localctx, 48, RULE_naryop);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(216); naryoptype();
			setState(217); naryopargs();
			setState(218); match(17);
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

	public static class NaryoptypeContext extends ParserRuleContext {
		public NaryoptypeContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_naryoptype; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SmallListener ) ((SmallListener)listener).enterNaryoptype(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SmallListener ) ((SmallListener)listener).exitNaryoptype(this);
		}
	}

	public final NaryoptypeContext naryoptype() throws RecognitionException {
		NaryoptypeContext _localctx = new NaryoptypeContext(_ctx, getState());
		enterRule(_localctx, 50, RULE_naryoptype);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(220);
			_la = _input.LA(1);
			if ( !((((_la) & ~0x3f) == 0 && ((1L << _la) & ((1L << 34) | (1L << 37) | (1L << 50))) != 0)) ) {
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

	public static class NaryopargsContext extends ParserRuleContext {
		public NaryopargContext naryoparg(int i) {
			return getRuleContext(NaryopargContext.class,i);
		}
		public ExprContext expr() {
			return getRuleContext(ExprContext.class,0);
		}
		public List<NaryopargContext> naryoparg() {
			return getRuleContexts(NaryopargContext.class);
		}
		public NaryopargsContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_naryopargs; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SmallListener ) ((SmallListener)listener).enterNaryopargs(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SmallListener ) ((SmallListener)listener).exitNaryopargs(this);
		}
	}

	public final NaryopargsContext naryopargs() throws RecognitionException {
		NaryopargsContext _localctx = new NaryopargsContext(_ctx, getState());
		enterRule(_localctx, 52, RULE_naryopargs);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(222); expr();
			setState(224); 
			_errHandler.sync(this);
			_la = _input.LA(1);
			do {
				{
				{
				setState(223); naryoparg();
				}
				}
				setState(226); 
				_errHandler.sync(this);
				_la = _input.LA(1);
			} while ( (((_la) & ~0x3f) == 0 && ((1L << _la) & ((1L << 5) | (1L << 13) | (1L << 14) | (1L << 16) | (1L << 18) | (1L << 23) | (1L << 24) | (1L << 28) | (1L << 30) | (1L << 31) | (1L << 32) | (1L << 33) | (1L << 34) | (1L << 35) | (1L << 37) | (1L << 39) | (1L << 48) | (1L << 50) | (1L << BOOLEAN) | (1L << ID) | (1L << INTEGER) | (1L << STRING))) != 0) );
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

	public static class NaryopargContext extends ParserRuleContext {
		public ExprContext expr() {
			return getRuleContext(ExprContext.class,0);
		}
		public NaryopargContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_naryoparg; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SmallListener ) ((SmallListener)listener).enterNaryoparg(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SmallListener ) ((SmallListener)listener).exitNaryoparg(this);
		}
	}

	public final NaryopargContext naryoparg() throws RecognitionException {
		NaryopargContext _localctx = new NaryopargContext(_ctx, getState());
		enterRule(_localctx, 54, RULE_naryoparg);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(229);
			_la = _input.LA(1);
			if (_la==16) {
				{
				setState(228); match(16);
				}
			}

			setState(231); expr();
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

	public static class ConstantContext extends ParserRuleContext {
		public TerminalNode INTEGER() { return getToken(SmallParser.INTEGER, 0); }
		public TerminalNode BOOLEAN() { return getToken(SmallParser.BOOLEAN, 0); }
		public TerminalNode STRING() { return getToken(SmallParser.STRING, 0); }
		public ConstantContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_constant; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SmallListener ) ((SmallListener)listener).enterConstant(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SmallListener ) ((SmallListener)listener).exitConstant(this);
		}
	}

	public final ConstantContext constant() throws RecognitionException {
		ConstantContext _localctx = new ConstantContext(_ctx, getState());
		enterRule(_localctx, 56, RULE_constant);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(233);
			_la = _input.LA(1);
			if ( !((((_la) & ~0x3f) == 0 && ((1L << _la) & ((1L << BOOLEAN) | (1L << INTEGER) | (1L << STRING))) != 0)) ) {
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

	public static class TypeContext extends ParserRuleContext {
		public TypeContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_type; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SmallListener ) ((SmallListener)listener).enterType(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SmallListener ) ((SmallListener)listener).exitType(this);
		}
	}

	public final TypeContext type() throws RecognitionException {
		TypeContext _localctx = new TypeContext(_ctx, getState());
		enterRule(_localctx, 58, RULE_type);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(235);
			_la = _input.LA(1);
			if ( !((((_la) & ~0x3f) == 0 && ((1L << _la) & ((1L << 2) | (1L << 8) | (1L << 10) | (1L << 11) | (1L << 22) | (1L << 46))) != 0)) ) {
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

	public static final String _serializedATN =
		"\2\3@\u00f0\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4\b\t\b\4"+
		"\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r\4\16\t\16\4\17\t\17\4\20\t\20"+
		"\4\21\t\21\4\22\t\22\4\23\t\23\4\24\t\24\4\25\t\25\4\26\t\26\4\27\t\27"+
		"\4\30\t\30\4\31\t\31\4\32\t\32\4\33\t\33\4\34\t\34\4\35\t\35\4\36\t\36"+
		"\4\37\t\37\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\3\7\3H\n\3\f\3\16\3K\13\3"+
		"\3\4\3\4\3\4\5\4P\n\4\3\4\5\4S\n\4\3\4\3\4\5\4W\n\4\3\5\3\5\3\5\3\5\3"+
		"\5\3\5\3\5\3\5\3\5\3\5\3\5\5\5d\n\5\3\6\3\6\3\6\5\6i\n\6\3\6\3\6\3\7\3"+
		"\7\3\7\3\7\3\7\3\b\3\b\3\b\3\b\3\b\3\t\3\t\3\t\3\t\3\t\3\t\5\t}\n\t\3"+
		"\t\3\t\3\n\3\n\3\n\3\n\3\n\3\n\7\n\u0087\n\n\f\n\16\n\u008a\13\n\3\n\5"+
		"\n\u008d\n\n\3\n\3\n\3\n\3\13\3\13\3\13\3\13\3\13\3\f\3\f\3\f\3\f\3\r"+
		"\3\r\3\r\5\r\u009e\n\r\3\r\5\r\u00a1\n\r\3\r\3\r\3\r\3\r\3\r\3\r\3\16"+
		"\3\16\3\16\3\16\3\17\3\17\3\20\3\20\3\20\3\21\3\21\3\21\3\21\3\22\3\22"+
		"\3\22\3\22\3\22\3\23\3\23\3\23\7\23\u00be\n\23\f\23\16\23\u00c1\13\23"+
		"\3\24\3\24\3\25\3\25\3\25\5\25\u00c8\n\25\3\26\3\26\3\26\5\26\u00cd\n"+
		"\26\3\27\3\27\3\27\3\30\3\30\3\30\5\30\u00d5\n\30\3\30\3\30\3\31\3\31"+
		"\3\32\3\32\3\32\3\32\3\33\3\33\3\34\3\34\6\34\u00e3\n\34\r\34\16\34\u00e4"+
		"\3\35\5\35\u00e8\n\35\3\35\3\35\3\36\3\36\3\37\3\37\3\37\2 \2\4\6\b\n"+
		"\f\16\20\22\24\26\30\32\34\36 \"$&(*,.\60\62\64\668:<\2\t\5\b\b\26\26"+
		"&&\4\5\5\33\33\4\6\6..\13\7\7\17\17\24\24\31\31\36\36 #%%))\62\62\5$$"+
		"\'\'\64\64\588::??\7\4\4\n\n\f\r\30\30\60\60\u00ed\2>\3\2\2\2\4I\3\2\2"+
		"\2\6V\3\2\2\2\bc\3\2\2\2\ne\3\2\2\2\fl\3\2\2\2\16q\3\2\2\2\20|\3\2\2\2"+
		"\22\u0080\3\2\2\2\24\u0091\3\2\2\2\26\u0096\3\2\2\2\30\u009a\3\2\2\2\32"+
		"\u00a8\3\2\2\2\34\u00ac\3\2\2\2\36\u00ae\3\2\2\2 \u00b1\3\2\2\2\"\u00b5"+
		"\3\2\2\2$\u00ba\3\2\2\2&\u00c2\3\2\2\2(\u00c7\3\2\2\2*\u00cc\3\2\2\2,"+
		"\u00ce\3\2\2\2.\u00d1\3\2\2\2\60\u00d8\3\2\2\2\62\u00da\3\2\2\2\64\u00de"+
		"\3\2\2\2\66\u00e0\3\2\2\28\u00e7\3\2\2\2:\u00eb\3\2\2\2<\u00ed\3\2\2\2"+
		">?\7\16\2\2?@\t\2\2\2@A\7@\2\2AB\5\4\3\2BC\7\27\2\2CD\7@\2\2DE\7\1\2\2"+
		"E\3\3\2\2\2FH\5\b\5\2GF\3\2\2\2HK\3\2\2\2IG\3\2\2\2IJ\3\2\2\2J\5\3\2\2"+
		"\2KI\3\2\2\2LW\79\2\2MP\79\2\2NP\5:\36\2OM\3\2\2\2ON\3\2\2\2PQ\3\2\2\2"+
		"QS\7\67\2\2RO\3\2\2\2RS\3\2\2\2ST\3\2\2\2TU\7\20\2\2UW\5(\25\2VL\3\2\2"+
		"\2VR\3\2\2\2W\7\3\2\2\2Xd\5\n\6\2Yd\5\f\7\2Zd\5\16\b\2[d\5\22\n\2\\d\5"+
		"\30\r\2]d\5 \21\2^d\5\"\22\2_`\5(\25\2`a\7@\2\2ad\3\2\2\2bd\5&\24\2cX"+
		"\3\2\2\2cY\3\2\2\2cZ\3\2\2\2c[\3\2\2\2c\\\3\2\2\2c]\3\2\2\2c^\3\2\2\2"+
		"c_\3\2\2\2cb\3\2\2\2d\t\3\2\2\2ef\7\25\2\2fh\5$\23\2gi\7\21\2\2hg\3\2"+
		"\2\2hi\3\2\2\2ij\3\2\2\2jk\7@\2\2k\13\3\2\2\2lm\5\6\4\2mn\7\61\2\2no\5"+
		"(\25\2op\7@\2\2p\r\3\2\2\2qr\5\6\4\2rs\7\66\2\2st\5\6\4\2tu\5\20\t\2u"+
		"\17\3\2\2\2vw\7/\2\2w}\5(\25\2xy\7\34\2\2y}\5<\37\2z{\7*\2\2{}\5\6\4\2"+
		"|v\3\2\2\2|x\3\2\2\2|z\3\2\2\2|}\3\2\2\2}~\3\2\2\2~\177\7@\2\2\177\21"+
		"\3\2\2\2\u0080\u0081\7(\2\2\u0081\u0082\7@\2\2\u0082\u0083\7-\2\2\u0083"+
		"\u0084\7@\2\2\u0084\u0088\5\4\3\2\u0085\u0087\5\24\13\2\u0086\u0085\3"+
		"\2\2\2\u0087\u008a\3\2\2\2\u0088\u0086\3\2\2\2\u0088\u0089\3\2\2\2\u0089"+
		"\u008c\3\2\2\2\u008a\u0088\3\2\2\2\u008b\u008d\5\26\f\2\u008c\u008b\3"+
		"\2\2\2\u008c\u008d\3\2\2\2\u008d\u008e\3\2\2\2\u008e\u008f\7\3\2\2\u008f"+
		"\u0090\7@\2\2\u0090\23\3\2\2\2\u0091\u0092\7\t\2\2\u0092\u0093\5(\25\2"+
		"\u0093\u0094\7@\2\2\u0094\u0095\5\4\3\2\u0095\25\3\2\2\2\u0096\u0097\7"+
		"+\2\2\u0097\u0098\7@\2\2\u0098\u0099\5\4\3\2\u0099\27\3\2\2\2\u009a\u009b"+
		"\7\65\2\2\u009b\u009d\5\6\4\2\u009c\u009e\5\32\16\2\u009d\u009c\3\2\2"+
		"\2\u009d\u009e\3\2\2\2\u009e\u00a0\3\2\2\2\u009f\u00a1\5\36\20\2\u00a0"+
		"\u009f\3\2\2\2\u00a0\u00a1\3\2\2\2\u00a1\u00a2\3\2\2\2\u00a2\u00a3\7@"+
		"\2\2\u00a3\u00a4\5\4\3\2\u00a4\u00a5\7\35\2\2\u00a5\u00a6\5\6\4\2\u00a6"+
		"\u00a7\7@\2\2\u00a7\31\3\2\2\2\u00a8\u00a9\5\34\17\2\u00a9\u00aa\7\63"+
		"\2\2\u00aa\u00ab\5\6\4\2\u00ab\33\3\2\2\2\u00ac\u00ad\t\3\2\2\u00ad\35"+
		"\3\2\2\2\u00ae\u00af\t\4\2\2\u00af\u00b0\5(\25\2\u00b0\37\3\2\2\2\u00b1"+
		"\u00b2\7\13\2\2\u00b2\u00b3\5\6\4\2\u00b3\u00b4\7@\2\2\u00b4!\3\2\2\2"+
		"\u00b5\u00b6\5\6\4\2\u00b6\u00b7\7,\2\2\u00b7\u00b8\5<\37\2\u00b8\u00b9"+
		"\7@\2\2\u00b9#\3\2\2\2\u00ba\u00bf\5(\25\2\u00bb\u00bc\7\37\2\2\u00bc"+
		"\u00be\5(\25\2\u00bd\u00bb\3\2\2\2\u00be\u00c1\3\2\2\2\u00bf\u00bd\3\2"+
		"\2\2\u00bf\u00c0\3\2\2\2\u00c0%\3\2\2\2\u00c1\u00bf\3\2\2\2\u00c2\u00c3"+
		"\7@\2\2\u00c3\'\3\2\2\2\u00c4\u00c8\5:\36\2\u00c5\u00c8\5\6\4\2\u00c6"+
		"\u00c8\5*\26\2\u00c7\u00c4\3\2\2\2\u00c7\u00c5\3\2\2\2\u00c7\u00c6\3\2"+
		"\2\2\u00c8)\3\2\2\2\u00c9\u00cd\5,\27\2\u00ca\u00cd\5.\30\2\u00cb\u00cd"+
		"\5\62\32\2\u00cc\u00c9\3\2\2\2\u00cc\u00ca\3\2\2\2\u00cc\u00cb\3\2\2\2"+
		"\u00cd+\3\2\2\2\u00ce\u00cf\7\32\2\2\u00cf\u00d0\5(\25\2\u00d0-\3\2\2"+
		"\2\u00d1\u00d2\5\60\31\2\u00d2\u00d4\5(\25\2\u00d3\u00d5\7\22\2\2\u00d4"+
		"\u00d3\3\2\2\2\u00d4\u00d5\3\2\2\2\u00d5\u00d6\3\2\2\2\u00d6\u00d7\5("+
		"\25\2\u00d7/\3\2\2\2\u00d8\u00d9\t\5\2\2\u00d9\61\3\2\2\2\u00da\u00db"+
		"\5\64\33\2\u00db\u00dc\5\66\34\2\u00dc\u00dd\7\23\2\2\u00dd\63\3\2\2\2"+
		"\u00de\u00df\t\6\2\2\u00df\65\3\2\2\2\u00e0\u00e2\5(\25\2\u00e1\u00e3"+
		"\58\35\2\u00e2\u00e1\3\2\2\2\u00e3\u00e4\3\2\2\2\u00e4\u00e2\3\2\2\2\u00e4"+
		"\u00e5\3\2\2\2\u00e5\67\3\2\2\2\u00e6\u00e8\7\22\2\2\u00e7\u00e6\3\2\2"+
		"\2\u00e7\u00e8\3\2\2\2\u00e8\u00e9\3\2\2\2\u00e9\u00ea\5(\25\2\u00ea9"+
		"\3\2\2\2\u00eb\u00ec\t\7\2\2\u00ec;\3\2\2\2\u00ed\u00ee\t\b\2\2\u00ee"+
		"=\3\2\2\2\23IORVch|\u0088\u008c\u009d\u00a0\u00bf\u00c7\u00cc\u00d4\u00e4"+
		"\u00e7";
	public static final ATN _ATN =
		ATNSimulator.deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
	}
}