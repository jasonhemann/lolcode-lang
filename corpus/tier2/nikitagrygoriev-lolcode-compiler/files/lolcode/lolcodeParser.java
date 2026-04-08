// Generated from lolcode.g4 by ANTLR 4.7.2
import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.misc.*;
import org.antlr.v4.runtime.tree.*;
import java.util.List;
import java.util.Iterator;
import java.util.ArrayList;

@SuppressWarnings({"all", "warnings", "unchecked", "unused", "cast"})
public class lolcodeParser extends Parser {
	static { RuntimeMetaData.checkVersion("4.7.2", RuntimeMetaData.VERSION); }

	protected static final DFA[] _decisionToDFA;
	protected static final PredictionContextCache _sharedContextCache =
		new PredictionContextCache();
	public static final int
		T__0=1, T__1=2, T__2=3, T__3=4, T__4=5, T__5=6, T__6=7, T__7=8, T__8=9, 
		T__9=10, T__10=11, T__11=12, T__12=13, T__13=14, T__14=15, T__15=16, T__16=17, 
		T__17=18, T__18=19, T__19=20, T__20=21, T__21=22, T__22=23, T__23=24, 
		T__24=25, T__25=26, T__26=27, T__27=28, T__28=29, T__29=30, T__30=31, 
		T__31=32, ATOM=33, LABEL=34, BOOLEAN=35, STRING=36, WHITESPACE=37, NEWLINE=38;
	public static final int
		RULE_program = 0, RULE_prog_type = 1, RULE_code_block = 2, RULE_statement = 3, 
		RULE_declaration = 4, RULE_comment = 5, RULE_print_block = 6, RULE_if_block = 7, 
		RULE_else_if_block = 8, RULE_input_block = 9, RULE_assignment = 10, RULE_full_expression = 11, 
		RULE_expression = 12, RULE_equals = 13, RULE_not_equals = 14, RULE_both = 15, 
		RULE_either = 16, RULE_greater = 17, RULE_less = 18, RULE_add = 19, RULE_sub = 20, 
		RULE_mul = 21, RULE_div = 22, RULE_mod = 23, RULE_nope = 24, RULE_r_an = 25;
	private static String[] makeRuleNames() {
		return new String[] {
			"program", "prog_type", "code_block", "statement", "declaration", "comment", 
			"print_block", "if_block", "else_if_block", "input_block", "assignment", 
			"full_expression", "expression", "equals", "not_equals", "both", "either", 
			"greater", "less", "add", "sub", "mul", "div", "mod", "nope", "r_an"
		};
	}
	public static final String[] ruleNames = makeRuleNames();

	private static String[] makeLiteralNames() {
		return new String[] {
			null, "'HAI'", "'KTHXBYE'", "'LOL'", "'GOT'", "'GEEK'", "'I HAS A'", 
			"'ITZ'", "'BTW'", "'OBTW'", "'TLDR'", "'VISIBLE'", "'MKAY?'", "'O RLY?'", 
			"'YA RLY'", "'OIC'", "'MEBBE'", "'NO WAI'", "'GIMMEH'", "'R'", "'BOTH SAEM'", 
			"'DIFFRINT'", "'BOTH OF'", "'EITHER OF'", "'BIGGR OF'", "'SMALLR OF'", 
			"'SUM OF'", "'DIFF OF'", "'PRODUKT OF'", "'QUOSHUNT OF'", "'MOD OF'", 
			"'NOT'", "'AN'", null, null, null, null, "' '"
		};
	}
	private static final String[] _LITERAL_NAMES = makeLiteralNames();
	private static String[] makeSymbolicNames() {
		return new String[] {
			null, null, null, null, null, null, null, null, null, null, null, null, 
			null, null, null, null, null, null, null, null, null, null, null, null, 
			null, null, null, null, null, null, null, null, null, "ATOM", "LABEL", 
			"BOOLEAN", "STRING", "WHITESPACE", "NEWLINE"
		};
	}
	private static final String[] _SYMBOLIC_NAMES = makeSymbolicNames();
	public static final Vocabulary VOCABULARY = new VocabularyImpl(_LITERAL_NAMES, _SYMBOLIC_NAMES);

	/**
	 * @deprecated Use {@link #VOCABULARY} instead.
	 */
	@Deprecated
	public static final String[] tokenNames;
	static {
		tokenNames = new String[_SYMBOLIC_NAMES.length];
		for (int i = 0; i < tokenNames.length; i++) {
			tokenNames[i] = VOCABULARY.getLiteralName(i);
			if (tokenNames[i] == null) {
				tokenNames[i] = VOCABULARY.getSymbolicName(i);
			}

			if (tokenNames[i] == null) {
				tokenNames[i] = "<INVALID>";
			}
		}
	}

	@Override
	@Deprecated
	public String[] getTokenNames() {
		return tokenNames;
	}

	@Override

	public Vocabulary getVocabulary() {
		return VOCABULARY;
	}

	@Override
	public String getGrammarFileName() { return "lolcode.g4"; }

	@Override
	public String[] getRuleNames() { return ruleNames; }

	@Override
	public String getSerializedATN() { return _serializedATN; }

	@Override
	public ATN getATN() { return _ATN; }

	public lolcodeParser(TokenStream input) {
		super(input);
		_interp = new ParserATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}
	public static class ProgramContext extends ParserRuleContext {
		public Prog_typeContext prog_type() {
			return getRuleContext(Prog_typeContext.class,0);
		}
		public TerminalNode NEWLINE() { return getToken(lolcodeParser.NEWLINE, 0); }
		public Code_blockContext code_block() {
			return getRuleContext(Code_blockContext.class,0);
		}
		public ProgramContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_program; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof lolcodeListener ) ((lolcodeListener)listener).enterProgram(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof lolcodeListener ) ((lolcodeListener)listener).exitProgram(this);
		}
	}

	public final ProgramContext program() throws RecognitionException {
		ProgramContext _localctx = new ProgramContext(_ctx, getState());
		enterRule(_localctx, 0, RULE_program);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(52);
			match(T__0);
			setState(53);
			prog_type();
			setState(54);
			match(NEWLINE);
			setState(55);
			code_block();
			setState(57);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==T__1) {
				{
				setState(56);
				match(T__1);
				}
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

	public static class Prog_typeContext extends ParserRuleContext {
		public Prog_typeContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_prog_type; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof lolcodeListener ) ((lolcodeListener)listener).enterProg_type(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof lolcodeListener ) ((lolcodeListener)listener).exitProg_type(this);
		}
	}

	public final Prog_typeContext prog_type() throws RecognitionException {
		Prog_typeContext _localctx = new Prog_typeContext(_ctx, getState());
		enterRule(_localctx, 2, RULE_prog_type);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(59);
			_la = _input.LA(1);
			if ( !((((_la) & ~0x3f) == 0 && ((1L << _la) & ((1L << T__2) | (1L << T__3) | (1L << T__4))) != 0)) ) {
			_errHandler.recoverInline(this);
			}
			else {
				if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
				_errHandler.reportMatch(this);
				consume();
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

	public static class Code_blockContext extends ParserRuleContext {
		public List<StatementContext> statement() {
			return getRuleContexts(StatementContext.class);
		}
		public StatementContext statement(int i) {
			return getRuleContext(StatementContext.class,i);
		}
		public Code_blockContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_code_block; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof lolcodeListener ) ((lolcodeListener)listener).enterCode_block(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof lolcodeListener ) ((lolcodeListener)listener).exitCode_block(this);
		}
	}

	public final Code_blockContext code_block() throws RecognitionException {
		Code_blockContext _localctx = new Code_blockContext(_ctx, getState());
		enterRule(_localctx, 4, RULE_code_block);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(62); 
			_errHandler.sync(this);
			_la = _input.LA(1);
			do {
				{
				{
				setState(61);
				statement();
				}
				}
				setState(64); 
				_errHandler.sync(this);
				_la = _input.LA(1);
			} while ( (((_la) & ~0x3f) == 0 && ((1L << _la) & ((1L << T__5) | (1L << T__7) | (1L << T__8) | (1L << T__10) | (1L << T__12) | (1L << T__17) | (1L << T__19) | (1L << T__20) | (1L << T__21) | (1L << T__22) | (1L << T__23) | (1L << T__24) | (1L << T__25) | (1L << T__26) | (1L << T__27) | (1L << T__28) | (1L << T__29) | (1L << T__30) | (1L << ATOM) | (1L << LABEL))) != 0) );
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
		public DeclarationContext declaration() {
			return getRuleContext(DeclarationContext.class,0);
		}
		public TerminalNode NEWLINE() { return getToken(lolcodeParser.NEWLINE, 0); }
		public CommentContext comment() {
			return getRuleContext(CommentContext.class,0);
		}
		public Print_blockContext print_block() {
			return getRuleContext(Print_blockContext.class,0);
		}
		public If_blockContext if_block() {
			return getRuleContext(If_blockContext.class,0);
		}
		public Input_blockContext input_block() {
			return getRuleContext(Input_blockContext.class,0);
		}
		public AssignmentContext assignment() {
			return getRuleContext(AssignmentContext.class,0);
		}
		public Full_expressionContext full_expression() {
			return getRuleContext(Full_expressionContext.class,0);
		}
		public StatementContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_statement; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof lolcodeListener ) ((lolcodeListener)listener).enterStatement(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof lolcodeListener ) ((lolcodeListener)listener).exitStatement(this);
		}
	}

	public final StatementContext statement() throws RecognitionException {
		StatementContext _localctx = new StatementContext(_ctx, getState());
		enterRule(_localctx, 6, RULE_statement);
		try {
			setState(85);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,2,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(66);
				declaration();
				setState(67);
				match(NEWLINE);
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(69);
				comment();
				setState(70);
				match(NEWLINE);
				}
				break;
			case 3:
				enterOuterAlt(_localctx, 3);
				{
				setState(72);
				print_block();
				setState(73);
				match(NEWLINE);
				}
				break;
			case 4:
				enterOuterAlt(_localctx, 4);
				{
				setState(75);
				if_block();
				setState(76);
				match(NEWLINE);
				}
				break;
			case 5:
				enterOuterAlt(_localctx, 5);
				{
				setState(78);
				input_block();
				setState(79);
				match(NEWLINE);
				}
				break;
			case 6:
				enterOuterAlt(_localctx, 6);
				{
				setState(81);
				assignment();
				setState(82);
				match(NEWLINE);
				}
				break;
			case 7:
				enterOuterAlt(_localctx, 7);
				{
				setState(84);
				full_expression();
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

	public static class DeclarationContext extends ParserRuleContext {
		public TerminalNode LABEL() { return getToken(lolcodeParser.LABEL, 0); }
		public TerminalNode ATOM() { return getToken(lolcodeParser.ATOM, 0); }
		public DeclarationContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_declaration; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof lolcodeListener ) ((lolcodeListener)listener).enterDeclaration(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof lolcodeListener ) ((lolcodeListener)listener).exitDeclaration(this);
		}
	}

	public final DeclarationContext declaration() throws RecognitionException {
		DeclarationContext _localctx = new DeclarationContext(_ctx, getState());
		enterRule(_localctx, 8, RULE_declaration);
		try {
			setState(93);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,3,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(87);
				match(T__5);
				setState(88);
				match(LABEL);
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(89);
				match(T__5);
				setState(90);
				match(LABEL);
				setState(91);
				match(T__6);
				setState(92);
				match(ATOM);
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

	public static class CommentContext extends ParserRuleContext {
		public ExpressionContext expression() {
			return getRuleContext(ExpressionContext.class,0);
		}
		public List<TerminalNode> NEWLINE() { return getTokens(lolcodeParser.NEWLINE); }
		public TerminalNode NEWLINE(int i) {
			return getToken(lolcodeParser.NEWLINE, i);
		}
		public List<Full_expressionContext> full_expression() {
			return getRuleContexts(Full_expressionContext.class);
		}
		public Full_expressionContext full_expression(int i) {
			return getRuleContext(Full_expressionContext.class,i);
		}
		public TerminalNode STRING() { return getToken(lolcodeParser.STRING, 0); }
		public CommentContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_comment; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof lolcodeListener ) ((lolcodeListener)listener).enterComment(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof lolcodeListener ) ((lolcodeListener)listener).exitComment(this);
		}
	}

	public final CommentContext comment() throws RecognitionException {
		CommentContext _localctx = new CommentContext(_ctx, getState());
		enterRule(_localctx, 10, RULE_comment);
		int _la;
		try {
			setState(113);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,5,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(95);
				match(T__7);
				setState(96);
				expression();
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(97);
				match(T__8);
				setState(98);
				match(NEWLINE);
				setState(102);
				_errHandler.sync(this);
				_la = _input.LA(1);
				while ((((_la) & ~0x3f) == 0 && ((1L << _la) & ((1L << T__19) | (1L << T__20) | (1L << T__21) | (1L << T__22) | (1L << T__23) | (1L << T__24) | (1L << T__25) | (1L << T__26) | (1L << T__27) | (1L << T__28) | (1L << T__29) | (1L << T__30) | (1L << ATOM) | (1L << LABEL))) != 0)) {
					{
					{
					setState(99);
					full_expression();
					}
					}
					setState(104);
					_errHandler.sync(this);
					_la = _input.LA(1);
				}
				setState(105);
				match(T__9);
				}
				break;
			case 3:
				enterOuterAlt(_localctx, 3);
				{
				setState(106);
				match(T__7);
				setState(107);
				match(STRING);
				}
				break;
			case 4:
				enterOuterAlt(_localctx, 4);
				{
				setState(108);
				match(T__8);
				setState(109);
				match(NEWLINE);
				setState(110);
				match(STRING);
				setState(111);
				match(NEWLINE);
				setState(112);
				match(T__9);
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

	public static class Print_blockContext extends ParserRuleContext {
		public List<ExpressionContext> expression() {
			return getRuleContexts(ExpressionContext.class);
		}
		public ExpressionContext expression(int i) {
			return getRuleContext(ExpressionContext.class,i);
		}
		public Print_blockContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_print_block; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof lolcodeListener ) ((lolcodeListener)listener).enterPrint_block(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof lolcodeListener ) ((lolcodeListener)listener).exitPrint_block(this);
		}
	}

	public final Print_blockContext print_block() throws RecognitionException {
		Print_blockContext _localctx = new Print_blockContext(_ctx, getState());
		enterRule(_localctx, 12, RULE_print_block);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(115);
			match(T__10);
			setState(119);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while ((((_la) & ~0x3f) == 0 && ((1L << _la) & ((1L << T__19) | (1L << T__20) | (1L << T__21) | (1L << T__22) | (1L << T__23) | (1L << T__24) | (1L << T__25) | (1L << T__26) | (1L << T__27) | (1L << T__28) | (1L << T__29) | (1L << T__30) | (1L << ATOM) | (1L << LABEL))) != 0)) {
				{
				{
				setState(116);
				expression();
				}
				}
				setState(121);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(123);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==T__11) {
				{
				setState(122);
				match(T__11);
				}
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

	public static class If_blockContext extends ParserRuleContext {
		public List<TerminalNode> NEWLINE() { return getTokens(lolcodeParser.NEWLINE); }
		public TerminalNode NEWLINE(int i) {
			return getToken(lolcodeParser.NEWLINE, i);
		}
		public Code_blockContext code_block() {
			return getRuleContext(Code_blockContext.class,0);
		}
		public EqualsContext equals() {
			return getRuleContext(EqualsContext.class,0);
		}
		public Not_equalsContext not_equals() {
			return getRuleContext(Not_equalsContext.class,0);
		}
		public BothContext both() {
			return getRuleContext(BothContext.class,0);
		}
		public EitherContext either() {
			return getRuleContext(EitherContext.class,0);
		}
		public GreaterContext greater() {
			return getRuleContext(GreaterContext.class,0);
		}
		public LessContext less() {
			return getRuleContext(LessContext.class,0);
		}
		public Else_if_blockContext else_if_block() {
			return getRuleContext(Else_if_blockContext.class,0);
		}
		public If_blockContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_if_block; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof lolcodeListener ) ((lolcodeListener)listener).enterIf_block(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof lolcodeListener ) ((lolcodeListener)listener).exitIf_block(this);
		}
	}

	public final If_blockContext if_block() throws RecognitionException {
		If_blockContext _localctx = new If_blockContext(_ctx, getState());
		enterRule(_localctx, 14, RULE_if_block);
		try {
			setState(158);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,10,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(125);
				match(T__12);
				setState(126);
				match(NEWLINE);
				setState(127);
				match(T__13);
				setState(128);
				match(NEWLINE);
				setState(135);
				_errHandler.sync(this);
				switch (_input.LA(1)) {
				case T__19:
					{
					setState(129);
					equals();
					}
					break;
				case T__20:
					{
					setState(130);
					not_equals();
					}
					break;
				case T__21:
					{
					setState(131);
					both();
					}
					break;
				case T__22:
					{
					setState(132);
					either();
					}
					break;
				case T__23:
					{
					setState(133);
					greater();
					}
					break;
				case T__24:
					{
					setState(134);
					less();
					}
					break;
				default:
					throw new NoViableAltException(this);
				}
				setState(137);
				match(NEWLINE);
				setState(138);
				code_block();
				setState(139);
				match(T__14);
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(141);
				match(T__12);
				setState(142);
				match(NEWLINE);
				setState(143);
				match(T__13);
				setState(144);
				match(NEWLINE);
				setState(151);
				_errHandler.sync(this);
				switch (_input.LA(1)) {
				case T__19:
					{
					setState(145);
					equals();
					}
					break;
				case T__20:
					{
					setState(146);
					not_equals();
					}
					break;
				case T__21:
					{
					setState(147);
					both();
					}
					break;
				case T__22:
					{
					setState(148);
					either();
					}
					break;
				case T__23:
					{
					setState(149);
					greater();
					}
					break;
				case T__24:
					{
					setState(150);
					less();
					}
					break;
				default:
					throw new NoViableAltException(this);
				}
				setState(153);
				match(NEWLINE);
				setState(154);
				code_block();
				setState(155);
				else_if_block();
				setState(156);
				match(T__14);
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

	public static class Else_if_blockContext extends ParserRuleContext {
		public TerminalNode NEWLINE() { return getToken(lolcodeParser.NEWLINE, 0); }
		public Code_blockContext code_block() {
			return getRuleContext(Code_blockContext.class,0);
		}
		public Else_if_blockContext else_if_block() {
			return getRuleContext(Else_if_blockContext.class,0);
		}
		public EqualsContext equals() {
			return getRuleContext(EqualsContext.class,0);
		}
		public Not_equalsContext not_equals() {
			return getRuleContext(Not_equalsContext.class,0);
		}
		public BothContext both() {
			return getRuleContext(BothContext.class,0);
		}
		public EitherContext either() {
			return getRuleContext(EitherContext.class,0);
		}
		public GreaterContext greater() {
			return getRuleContext(GreaterContext.class,0);
		}
		public LessContext less() {
			return getRuleContext(LessContext.class,0);
		}
		public Else_if_blockContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_else_if_block; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof lolcodeListener ) ((lolcodeListener)listener).enterElse_if_block(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof lolcodeListener ) ((lolcodeListener)listener).exitElse_if_block(this);
		}
	}

	public final Else_if_blockContext else_if_block() throws RecognitionException {
		Else_if_blockContext _localctx = new Else_if_blockContext(_ctx, getState());
		enterRule(_localctx, 16, RULE_else_if_block);
		try {
			setState(188);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,13,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(160);
				match(T__15);
				setState(167);
				_errHandler.sync(this);
				switch (_input.LA(1)) {
				case T__19:
					{
					setState(161);
					equals();
					}
					break;
				case T__20:
					{
					setState(162);
					not_equals();
					}
					break;
				case T__21:
					{
					setState(163);
					both();
					}
					break;
				case T__22:
					{
					setState(164);
					either();
					}
					break;
				case T__23:
					{
					setState(165);
					greater();
					}
					break;
				case T__24:
					{
					setState(166);
					less();
					}
					break;
				default:
					throw new NoViableAltException(this);
				}
				setState(169);
				match(NEWLINE);
				setState(170);
				code_block();
				setState(171);
				else_if_block();
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(173);
				match(T__16);
				setState(174);
				match(NEWLINE);
				setState(175);
				code_block();
				}
				break;
			case 3:
				enterOuterAlt(_localctx, 3);
				{
				setState(176);
				match(T__15);
				setState(183);
				_errHandler.sync(this);
				switch (_input.LA(1)) {
				case T__19:
					{
					setState(177);
					equals();
					}
					break;
				case T__20:
					{
					setState(178);
					not_equals();
					}
					break;
				case T__21:
					{
					setState(179);
					both();
					}
					break;
				case T__22:
					{
					setState(180);
					either();
					}
					break;
				case T__23:
					{
					setState(181);
					greater();
					}
					break;
				case T__24:
					{
					setState(182);
					less();
					}
					break;
				default:
					throw new NoViableAltException(this);
				}
				setState(185);
				match(NEWLINE);
				setState(186);
				code_block();
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

	public static class Input_blockContext extends ParserRuleContext {
		public TerminalNode LABEL() { return getToken(lolcodeParser.LABEL, 0); }
		public Input_blockContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_input_block; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof lolcodeListener ) ((lolcodeListener)listener).enterInput_block(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof lolcodeListener ) ((lolcodeListener)listener).exitInput_block(this);
		}
	}

	public final Input_blockContext input_block() throws RecognitionException {
		Input_blockContext _localctx = new Input_blockContext(_ctx, getState());
		enterRule(_localctx, 18, RULE_input_block);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(190);
			match(T__17);
			setState(191);
			match(LABEL);
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
		public TerminalNode LABEL() { return getToken(lolcodeParser.LABEL, 0); }
		public ExpressionContext expression() {
			return getRuleContext(ExpressionContext.class,0);
		}
		public AssignmentContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_assignment; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof lolcodeListener ) ((lolcodeListener)listener).enterAssignment(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof lolcodeListener ) ((lolcodeListener)listener).exitAssignment(this);
		}
	}

	public final AssignmentContext assignment() throws RecognitionException {
		AssignmentContext _localctx = new AssignmentContext(_ctx, getState());
		enterRule(_localctx, 20, RULE_assignment);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(193);
			match(LABEL);
			setState(194);
			match(T__18);
			setState(195);
			expression();
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

	public static class Full_expressionContext extends ParserRuleContext {
		public ExpressionContext expression() {
			return getRuleContext(ExpressionContext.class,0);
		}
		public TerminalNode NEWLINE() { return getToken(lolcodeParser.NEWLINE, 0); }
		public Full_expressionContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_full_expression; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof lolcodeListener ) ((lolcodeListener)listener).enterFull_expression(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof lolcodeListener ) ((lolcodeListener)listener).exitFull_expression(this);
		}
	}

	public final Full_expressionContext full_expression() throws RecognitionException {
		Full_expressionContext _localctx = new Full_expressionContext(_ctx, getState());
		enterRule(_localctx, 22, RULE_full_expression);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(197);
			expression();
			setState(198);
			match(NEWLINE);
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
		public EqualsContext equals() {
			return getRuleContext(EqualsContext.class,0);
		}
		public BothContext both() {
			return getRuleContext(BothContext.class,0);
		}
		public Not_equalsContext not_equals() {
			return getRuleContext(Not_equalsContext.class,0);
		}
		public GreaterContext greater() {
			return getRuleContext(GreaterContext.class,0);
		}
		public LessContext less() {
			return getRuleContext(LessContext.class,0);
		}
		public AddContext add() {
			return getRuleContext(AddContext.class,0);
		}
		public SubContext sub() {
			return getRuleContext(SubContext.class,0);
		}
		public MulContext mul() {
			return getRuleContext(MulContext.class,0);
		}
		public DivContext div() {
			return getRuleContext(DivContext.class,0);
		}
		public ModContext mod() {
			return getRuleContext(ModContext.class,0);
		}
		public EitherContext either() {
			return getRuleContext(EitherContext.class,0);
		}
		public NopeContext nope() {
			return getRuleContext(NopeContext.class,0);
		}
		public TerminalNode LABEL() { return getToken(lolcodeParser.LABEL, 0); }
		public TerminalNode ATOM() { return getToken(lolcodeParser.ATOM, 0); }
		public ExpressionContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_expression; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof lolcodeListener ) ((lolcodeListener)listener).enterExpression(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof lolcodeListener ) ((lolcodeListener)listener).exitExpression(this);
		}
	}

	public final ExpressionContext expression() throws RecognitionException {
		ExpressionContext _localctx = new ExpressionContext(_ctx, getState());
		enterRule(_localctx, 24, RULE_expression);
		try {
			setState(214);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case T__19:
				enterOuterAlt(_localctx, 1);
				{
				setState(200);
				equals();
				}
				break;
			case T__21:
				enterOuterAlt(_localctx, 2);
				{
				setState(201);
				both();
				}
				break;
			case T__20:
				enterOuterAlt(_localctx, 3);
				{
				setState(202);
				not_equals();
				}
				break;
			case T__23:
				enterOuterAlt(_localctx, 4);
				{
				setState(203);
				greater();
				}
				break;
			case T__24:
				enterOuterAlt(_localctx, 5);
				{
				setState(204);
				less();
				}
				break;
			case T__25:
				enterOuterAlt(_localctx, 6);
				{
				setState(205);
				add();
				}
				break;
			case T__26:
				enterOuterAlt(_localctx, 7);
				{
				setState(206);
				sub();
				}
				break;
			case T__27:
				enterOuterAlt(_localctx, 8);
				{
				setState(207);
				mul();
				}
				break;
			case T__28:
				enterOuterAlt(_localctx, 9);
				{
				setState(208);
				div();
				}
				break;
			case T__29:
				enterOuterAlt(_localctx, 10);
				{
				setState(209);
				mod();
				}
				break;
			case T__22:
				enterOuterAlt(_localctx, 11);
				{
				setState(210);
				either();
				}
				break;
			case T__30:
				enterOuterAlt(_localctx, 12);
				{
				setState(211);
				nope();
				}
				break;
			case LABEL:
				enterOuterAlt(_localctx, 13);
				{
				setState(212);
				match(LABEL);
				}
				break;
			case ATOM:
				enterOuterAlt(_localctx, 14);
				{
				setState(213);
				match(ATOM);
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

	public static class EqualsContext extends ParserRuleContext {
		public ExpressionContext expression() {
			return getRuleContext(ExpressionContext.class,0);
		}
		public R_anContext r_an() {
			return getRuleContext(R_anContext.class,0);
		}
		public EqualsContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_equals; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof lolcodeListener ) ((lolcodeListener)listener).enterEquals(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof lolcodeListener ) ((lolcodeListener)listener).exitEquals(this);
		}
	}

	public final EqualsContext equals() throws RecognitionException {
		EqualsContext _localctx = new EqualsContext(_ctx, getState());
		enterRule(_localctx, 26, RULE_equals);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(216);
			match(T__19);
			setState(217);
			expression();
			setState(218);
			r_an();
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

	public static class Not_equalsContext extends ParserRuleContext {
		public ExpressionContext expression() {
			return getRuleContext(ExpressionContext.class,0);
		}
		public R_anContext r_an() {
			return getRuleContext(R_anContext.class,0);
		}
		public Not_equalsContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_not_equals; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof lolcodeListener ) ((lolcodeListener)listener).enterNot_equals(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof lolcodeListener ) ((lolcodeListener)listener).exitNot_equals(this);
		}
	}

	public final Not_equalsContext not_equals() throws RecognitionException {
		Not_equalsContext _localctx = new Not_equalsContext(_ctx, getState());
		enterRule(_localctx, 28, RULE_not_equals);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(220);
			match(T__20);
			setState(221);
			expression();
			setState(222);
			r_an();
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

	public static class BothContext extends ParserRuleContext {
		public ExpressionContext expression() {
			return getRuleContext(ExpressionContext.class,0);
		}
		public R_anContext r_an() {
			return getRuleContext(R_anContext.class,0);
		}
		public BothContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_both; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof lolcodeListener ) ((lolcodeListener)listener).enterBoth(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof lolcodeListener ) ((lolcodeListener)listener).exitBoth(this);
		}
	}

	public final BothContext both() throws RecognitionException {
		BothContext _localctx = new BothContext(_ctx, getState());
		enterRule(_localctx, 30, RULE_both);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(224);
			match(T__21);
			setState(225);
			expression();
			setState(226);
			r_an();
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

	public static class EitherContext extends ParserRuleContext {
		public ExpressionContext expression() {
			return getRuleContext(ExpressionContext.class,0);
		}
		public R_anContext r_an() {
			return getRuleContext(R_anContext.class,0);
		}
		public EitherContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_either; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof lolcodeListener ) ((lolcodeListener)listener).enterEither(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof lolcodeListener ) ((lolcodeListener)listener).exitEither(this);
		}
	}

	public final EitherContext either() throws RecognitionException {
		EitherContext _localctx = new EitherContext(_ctx, getState());
		enterRule(_localctx, 32, RULE_either);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(228);
			match(T__22);
			setState(229);
			expression();
			setState(230);
			r_an();
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

	public static class GreaterContext extends ParserRuleContext {
		public ExpressionContext expression() {
			return getRuleContext(ExpressionContext.class,0);
		}
		public R_anContext r_an() {
			return getRuleContext(R_anContext.class,0);
		}
		public GreaterContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_greater; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof lolcodeListener ) ((lolcodeListener)listener).enterGreater(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof lolcodeListener ) ((lolcodeListener)listener).exitGreater(this);
		}
	}

	public final GreaterContext greater() throws RecognitionException {
		GreaterContext _localctx = new GreaterContext(_ctx, getState());
		enterRule(_localctx, 34, RULE_greater);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(232);
			match(T__23);
			setState(233);
			expression();
			setState(234);
			r_an();
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

	public static class LessContext extends ParserRuleContext {
		public ExpressionContext expression() {
			return getRuleContext(ExpressionContext.class,0);
		}
		public R_anContext r_an() {
			return getRuleContext(R_anContext.class,0);
		}
		public LessContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_less; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof lolcodeListener ) ((lolcodeListener)listener).enterLess(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof lolcodeListener ) ((lolcodeListener)listener).exitLess(this);
		}
	}

	public final LessContext less() throws RecognitionException {
		LessContext _localctx = new LessContext(_ctx, getState());
		enterRule(_localctx, 36, RULE_less);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(236);
			match(T__24);
			setState(237);
			expression();
			setState(238);
			r_an();
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

	public static class AddContext extends ParserRuleContext {
		public ExpressionContext expression() {
			return getRuleContext(ExpressionContext.class,0);
		}
		public R_anContext r_an() {
			return getRuleContext(R_anContext.class,0);
		}
		public AddContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_add; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof lolcodeListener ) ((lolcodeListener)listener).enterAdd(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof lolcodeListener ) ((lolcodeListener)listener).exitAdd(this);
		}
	}

	public final AddContext add() throws RecognitionException {
		AddContext _localctx = new AddContext(_ctx, getState());
		enterRule(_localctx, 38, RULE_add);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(240);
			match(T__25);
			setState(241);
			expression();
			setState(242);
			r_an();
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

	public static class SubContext extends ParserRuleContext {
		public ExpressionContext expression() {
			return getRuleContext(ExpressionContext.class,0);
		}
		public R_anContext r_an() {
			return getRuleContext(R_anContext.class,0);
		}
		public SubContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_sub; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof lolcodeListener ) ((lolcodeListener)listener).enterSub(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof lolcodeListener ) ((lolcodeListener)listener).exitSub(this);
		}
	}

	public final SubContext sub() throws RecognitionException {
		SubContext _localctx = new SubContext(_ctx, getState());
		enterRule(_localctx, 40, RULE_sub);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(244);
			match(T__26);
			setState(245);
			expression();
			setState(246);
			r_an();
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

	public static class MulContext extends ParserRuleContext {
		public ExpressionContext expression() {
			return getRuleContext(ExpressionContext.class,0);
		}
		public R_anContext r_an() {
			return getRuleContext(R_anContext.class,0);
		}
		public MulContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_mul; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof lolcodeListener ) ((lolcodeListener)listener).enterMul(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof lolcodeListener ) ((lolcodeListener)listener).exitMul(this);
		}
	}

	public final MulContext mul() throws RecognitionException {
		MulContext _localctx = new MulContext(_ctx, getState());
		enterRule(_localctx, 42, RULE_mul);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(248);
			match(T__27);
			setState(249);
			expression();
			setState(250);
			r_an();
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

	public static class DivContext extends ParserRuleContext {
		public ExpressionContext expression() {
			return getRuleContext(ExpressionContext.class,0);
		}
		public R_anContext r_an() {
			return getRuleContext(R_anContext.class,0);
		}
		public DivContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_div; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof lolcodeListener ) ((lolcodeListener)listener).enterDiv(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof lolcodeListener ) ((lolcodeListener)listener).exitDiv(this);
		}
	}

	public final DivContext div() throws RecognitionException {
		DivContext _localctx = new DivContext(_ctx, getState());
		enterRule(_localctx, 44, RULE_div);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(252);
			match(T__28);
			setState(253);
			expression();
			setState(254);
			r_an();
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

	public static class ModContext extends ParserRuleContext {
		public ExpressionContext expression() {
			return getRuleContext(ExpressionContext.class,0);
		}
		public R_anContext r_an() {
			return getRuleContext(R_anContext.class,0);
		}
		public ModContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_mod; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof lolcodeListener ) ((lolcodeListener)listener).enterMod(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof lolcodeListener ) ((lolcodeListener)listener).exitMod(this);
		}
	}

	public final ModContext mod() throws RecognitionException {
		ModContext _localctx = new ModContext(_ctx, getState());
		enterRule(_localctx, 46, RULE_mod);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(256);
			match(T__29);
			setState(257);
			expression();
			setState(258);
			r_an();
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

	public static class NopeContext extends ParserRuleContext {
		public ExpressionContext expression() {
			return getRuleContext(ExpressionContext.class,0);
		}
		public NopeContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_nope; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof lolcodeListener ) ((lolcodeListener)listener).enterNope(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof lolcodeListener ) ((lolcodeListener)listener).exitNope(this);
		}
	}

	public final NopeContext nope() throws RecognitionException {
		NopeContext _localctx = new NopeContext(_ctx, getState());
		enterRule(_localctx, 48, RULE_nope);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(260);
			match(T__30);
			setState(261);
			expression();
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

	public static class R_anContext extends ParserRuleContext {
		public ExpressionContext expression() {
			return getRuleContext(ExpressionContext.class,0);
		}
		public R_anContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_r_an; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof lolcodeListener ) ((lolcodeListener)listener).enterR_an(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof lolcodeListener ) ((lolcodeListener)listener).exitR_an(this);
		}
	}

	public final R_anContext r_an() throws RecognitionException {
		R_anContext _localctx = new R_anContext(_ctx, getState());
		enterRule(_localctx, 50, RULE_r_an);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(263);
			match(T__31);
			setState(264);
			expression();
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
		"\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3(\u010d\4\2\t\2\4"+
		"\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t"+
		"\13\4\f\t\f\4\r\t\r\4\16\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22"+
		"\4\23\t\23\4\24\t\24\4\25\t\25\4\26\t\26\4\27\t\27\4\30\t\30\4\31\t\31"+
		"\4\32\t\32\4\33\t\33\3\2\3\2\3\2\3\2\3\2\5\2<\n\2\3\3\3\3\3\4\6\4A\n\4"+
		"\r\4\16\4B\3\5\3\5\3\5\3\5\3\5\3\5\3\5\3\5\3\5\3\5\3\5\3\5\3\5\3\5\3\5"+
		"\3\5\3\5\3\5\3\5\5\5X\n\5\3\6\3\6\3\6\3\6\3\6\3\6\5\6`\n\6\3\7\3\7\3\7"+
		"\3\7\3\7\7\7g\n\7\f\7\16\7j\13\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\5\7t"+
		"\n\7\3\b\3\b\7\bx\n\b\f\b\16\b{\13\b\3\b\5\b~\n\b\3\t\3\t\3\t\3\t\3\t"+
		"\3\t\3\t\3\t\3\t\3\t\5\t\u008a\n\t\3\t\3\t\3\t\3\t\3\t\3\t\3\t\3\t\3\t"+
		"\3\t\3\t\3\t\3\t\3\t\5\t\u009a\n\t\3\t\3\t\3\t\3\t\3\t\5\t\u00a1\n\t\3"+
		"\n\3\n\3\n\3\n\3\n\3\n\3\n\5\n\u00aa\n\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3"+
		"\n\3\n\3\n\3\n\3\n\3\n\3\n\5\n\u00ba\n\n\3\n\3\n\3\n\5\n\u00bf\n\n\3\13"+
		"\3\13\3\13\3\f\3\f\3\f\3\f\3\r\3\r\3\r\3\16\3\16\3\16\3\16\3\16\3\16\3"+
		"\16\3\16\3\16\3\16\3\16\3\16\3\16\3\16\5\16\u00d9\n\16\3\17\3\17\3\17"+
		"\3\17\3\20\3\20\3\20\3\20\3\21\3\21\3\21\3\21\3\22\3\22\3\22\3\22\3\23"+
		"\3\23\3\23\3\23\3\24\3\24\3\24\3\24\3\25\3\25\3\25\3\25\3\26\3\26\3\26"+
		"\3\26\3\27\3\27\3\27\3\27\3\30\3\30\3\30\3\30\3\31\3\31\3\31\3\31\3\32"+
		"\3\32\3\32\3\33\3\33\3\33\3\33\2\2\34\2\4\6\b\n\f\16\20\22\24\26\30\32"+
		"\34\36 \"$&(*,.\60\62\64\2\3\3\2\5\7\2\u0125\2\66\3\2\2\2\4=\3\2\2\2\6"+
		"@\3\2\2\2\bW\3\2\2\2\n_\3\2\2\2\fs\3\2\2\2\16u\3\2\2\2\20\u00a0\3\2\2"+
		"\2\22\u00be\3\2\2\2\24\u00c0\3\2\2\2\26\u00c3\3\2\2\2\30\u00c7\3\2\2\2"+
		"\32\u00d8\3\2\2\2\34\u00da\3\2\2\2\36\u00de\3\2\2\2 \u00e2\3\2\2\2\"\u00e6"+
		"\3\2\2\2$\u00ea\3\2\2\2&\u00ee\3\2\2\2(\u00f2\3\2\2\2*\u00f6\3\2\2\2,"+
		"\u00fa\3\2\2\2.\u00fe\3\2\2\2\60\u0102\3\2\2\2\62\u0106\3\2\2\2\64\u0109"+
		"\3\2\2\2\66\67\7\3\2\2\678\5\4\3\289\7(\2\29;\5\6\4\2:<\7\4\2\2;:\3\2"+
		"\2\2;<\3\2\2\2<\3\3\2\2\2=>\t\2\2\2>\5\3\2\2\2?A\5\b\5\2@?\3\2\2\2AB\3"+
		"\2\2\2B@\3\2\2\2BC\3\2\2\2C\7\3\2\2\2DE\5\n\6\2EF\7(\2\2FX\3\2\2\2GH\5"+
		"\f\7\2HI\7(\2\2IX\3\2\2\2JK\5\16\b\2KL\7(\2\2LX\3\2\2\2MN\5\20\t\2NO\7"+
		"(\2\2OX\3\2\2\2PQ\5\24\13\2QR\7(\2\2RX\3\2\2\2ST\5\26\f\2TU\7(\2\2UX\3"+
		"\2\2\2VX\5\30\r\2WD\3\2\2\2WG\3\2\2\2WJ\3\2\2\2WM\3\2\2\2WP\3\2\2\2WS"+
		"\3\2\2\2WV\3\2\2\2X\t\3\2\2\2YZ\7\b\2\2Z`\7$\2\2[\\\7\b\2\2\\]\7$\2\2"+
		"]^\7\t\2\2^`\7#\2\2_Y\3\2\2\2_[\3\2\2\2`\13\3\2\2\2ab\7\n\2\2bt\5\32\16"+
		"\2cd\7\13\2\2dh\7(\2\2eg\5\30\r\2fe\3\2\2\2gj\3\2\2\2hf\3\2\2\2hi\3\2"+
		"\2\2ik\3\2\2\2jh\3\2\2\2kt\7\f\2\2lm\7\n\2\2mt\7&\2\2no\7\13\2\2op\7("+
		"\2\2pq\7&\2\2qr\7(\2\2rt\7\f\2\2sa\3\2\2\2sc\3\2\2\2sl\3\2\2\2sn\3\2\2"+
		"\2t\r\3\2\2\2uy\7\r\2\2vx\5\32\16\2wv\3\2\2\2x{\3\2\2\2yw\3\2\2\2yz\3"+
		"\2\2\2z}\3\2\2\2{y\3\2\2\2|~\7\16\2\2}|\3\2\2\2}~\3\2\2\2~\17\3\2\2\2"+
		"\177\u0080\7\17\2\2\u0080\u0081\7(\2\2\u0081\u0082\7\20\2\2\u0082\u0089"+
		"\7(\2\2\u0083\u008a\5\34\17\2\u0084\u008a\5\36\20\2\u0085\u008a\5 \21"+
		"\2\u0086\u008a\5\"\22\2\u0087\u008a\5$\23\2\u0088\u008a\5&\24\2\u0089"+
		"\u0083\3\2\2\2\u0089\u0084\3\2\2\2\u0089\u0085\3\2\2\2\u0089\u0086\3\2"+
		"\2\2\u0089\u0087\3\2\2\2\u0089\u0088\3\2\2\2\u008a\u008b\3\2\2\2\u008b"+
		"\u008c\7(\2\2\u008c\u008d\5\6\4\2\u008d\u008e\7\21\2\2\u008e\u00a1\3\2"+
		"\2\2\u008f\u0090\7\17\2\2\u0090\u0091\7(\2\2\u0091\u0092\7\20\2\2\u0092"+
		"\u0099\7(\2\2\u0093\u009a\5\34\17\2\u0094\u009a\5\36\20\2\u0095\u009a"+
		"\5 \21\2\u0096\u009a\5\"\22\2\u0097\u009a\5$\23\2\u0098\u009a\5&\24\2"+
		"\u0099\u0093\3\2\2\2\u0099\u0094\3\2\2\2\u0099\u0095\3\2\2\2\u0099\u0096"+
		"\3\2\2\2\u0099\u0097\3\2\2\2\u0099\u0098\3\2\2\2\u009a\u009b\3\2\2\2\u009b"+
		"\u009c\7(\2\2\u009c\u009d\5\6\4\2\u009d\u009e\5\22\n\2\u009e\u009f\7\21"+
		"\2\2\u009f\u00a1\3\2\2\2\u00a0\177\3\2\2\2\u00a0\u008f\3\2\2\2\u00a1\21"+
		"\3\2\2\2\u00a2\u00a9\7\22\2\2\u00a3\u00aa\5\34\17\2\u00a4\u00aa\5\36\20"+
		"\2\u00a5\u00aa\5 \21\2\u00a6\u00aa\5\"\22\2\u00a7\u00aa\5$\23\2\u00a8"+
		"\u00aa\5&\24\2\u00a9\u00a3\3\2\2\2\u00a9\u00a4\3\2\2\2\u00a9\u00a5\3\2"+
		"\2\2\u00a9\u00a6\3\2\2\2\u00a9\u00a7\3\2\2\2\u00a9\u00a8\3\2\2\2\u00aa"+
		"\u00ab\3\2\2\2\u00ab\u00ac\7(\2\2\u00ac\u00ad\5\6\4\2\u00ad\u00ae\5\22"+
		"\n\2\u00ae\u00bf\3\2\2\2\u00af\u00b0\7\23\2\2\u00b0\u00b1\7(\2\2\u00b1"+
		"\u00bf\5\6\4\2\u00b2\u00b9\7\22\2\2\u00b3\u00ba\5\34\17\2\u00b4\u00ba"+
		"\5\36\20\2\u00b5\u00ba\5 \21\2\u00b6\u00ba\5\"\22\2\u00b7\u00ba\5$\23"+
		"\2\u00b8\u00ba\5&\24\2\u00b9\u00b3\3\2\2\2\u00b9\u00b4\3\2\2\2\u00b9\u00b5"+
		"\3\2\2\2\u00b9\u00b6\3\2\2\2\u00b9\u00b7\3\2\2\2\u00b9\u00b8\3\2\2\2\u00ba"+
		"\u00bb\3\2\2\2\u00bb\u00bc\7(\2\2\u00bc\u00bd\5\6\4\2\u00bd\u00bf\3\2"+
		"\2\2\u00be\u00a2\3\2\2\2\u00be\u00af\3\2\2\2\u00be\u00b2\3\2\2\2\u00bf"+
		"\23\3\2\2\2\u00c0\u00c1\7\24\2\2\u00c1\u00c2\7$\2\2\u00c2\25\3\2\2\2\u00c3"+
		"\u00c4\7$\2\2\u00c4\u00c5\7\25\2\2\u00c5\u00c6\5\32\16\2\u00c6\27\3\2"+
		"\2\2\u00c7\u00c8\5\32\16\2\u00c8\u00c9\7(\2\2\u00c9\31\3\2\2\2\u00ca\u00d9"+
		"\5\34\17\2\u00cb\u00d9\5 \21\2\u00cc\u00d9\5\36\20\2\u00cd\u00d9\5$\23"+
		"\2\u00ce\u00d9\5&\24\2\u00cf\u00d9\5(\25\2\u00d0\u00d9\5*\26\2\u00d1\u00d9"+
		"\5,\27\2\u00d2\u00d9\5.\30\2\u00d3\u00d9\5\60\31\2\u00d4\u00d9\5\"\22"+
		"\2\u00d5\u00d9\5\62\32\2\u00d6\u00d9\7$\2\2\u00d7\u00d9\7#\2\2\u00d8\u00ca"+
		"\3\2\2\2\u00d8\u00cb\3\2\2\2\u00d8\u00cc\3\2\2\2\u00d8\u00cd\3\2\2\2\u00d8"+
		"\u00ce\3\2\2\2\u00d8\u00cf\3\2\2\2\u00d8\u00d0\3\2\2\2\u00d8\u00d1\3\2"+
		"\2\2\u00d8\u00d2\3\2\2\2\u00d8\u00d3\3\2\2\2\u00d8\u00d4\3\2\2\2\u00d8"+
		"\u00d5\3\2\2\2\u00d8\u00d6\3\2\2\2\u00d8\u00d7\3\2\2\2\u00d9\33\3\2\2"+
		"\2\u00da\u00db\7\26\2\2\u00db\u00dc\5\32\16\2\u00dc\u00dd\5\64\33\2\u00dd"+
		"\35\3\2\2\2\u00de\u00df\7\27\2\2\u00df\u00e0\5\32\16\2\u00e0\u00e1\5\64"+
		"\33\2\u00e1\37\3\2\2\2\u00e2\u00e3\7\30\2\2\u00e3\u00e4\5\32\16\2\u00e4"+
		"\u00e5\5\64\33\2\u00e5!\3\2\2\2\u00e6\u00e7\7\31\2\2\u00e7\u00e8\5\32"+
		"\16\2\u00e8\u00e9\5\64\33\2\u00e9#\3\2\2\2\u00ea\u00eb\7\32\2\2\u00eb"+
		"\u00ec\5\32\16\2\u00ec\u00ed\5\64\33\2\u00ed%\3\2\2\2\u00ee\u00ef\7\33"+
		"\2\2\u00ef\u00f0\5\32\16\2\u00f0\u00f1\5\64\33\2\u00f1\'\3\2\2\2\u00f2"+
		"\u00f3\7\34\2\2\u00f3\u00f4\5\32\16\2\u00f4\u00f5\5\64\33\2\u00f5)\3\2"+
		"\2\2\u00f6\u00f7\7\35\2\2\u00f7\u00f8\5\32\16\2\u00f8\u00f9\5\64\33\2"+
		"\u00f9+\3\2\2\2\u00fa\u00fb\7\36\2\2\u00fb\u00fc\5\32\16\2\u00fc\u00fd"+
		"\5\64\33\2\u00fd-\3\2\2\2\u00fe\u00ff\7\37\2\2\u00ff\u0100\5\32\16\2\u0100"+
		"\u0101\5\64\33\2\u0101/\3\2\2\2\u0102\u0103\7 \2\2\u0103\u0104\5\32\16"+
		"\2\u0104\u0105\5\64\33\2\u0105\61\3\2\2\2\u0106\u0107\7!\2\2\u0107\u0108"+
		"\5\32\16\2\u0108\63\3\2\2\2\u0109\u010a\7\"\2\2\u010a\u010b\5\32\16\2"+
		"\u010b\65\3\2\2\2\21;BW_hsy}\u0089\u0099\u00a0\u00a9\u00b9\u00be\u00d8";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}