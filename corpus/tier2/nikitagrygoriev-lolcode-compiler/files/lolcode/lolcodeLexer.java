// Generated from lolcode.g4 by ANTLR 4.7.2
import org.antlr.v4.runtime.Lexer;
import org.antlr.v4.runtime.CharStream;
import org.antlr.v4.runtime.Token;
import org.antlr.v4.runtime.TokenStream;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;
import org.antlr.v4.runtime.misc.*;

@SuppressWarnings({"all", "warnings", "unchecked", "unused", "cast"})
public class lolcodeLexer extends Lexer {
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
	public static String[] channelNames = {
		"DEFAULT_TOKEN_CHANNEL", "HIDDEN"
	};

	public static String[] modeNames = {
		"DEFAULT_MODE"
	};

	private static String[] makeRuleNames() {
		return new String[] {
			"T__0", "T__1", "T__2", "T__3", "T__4", "T__5", "T__6", "T__7", "T__8", 
			"T__9", "T__10", "T__11", "T__12", "T__13", "T__14", "T__15", "T__16", 
			"T__17", "T__18", "T__19", "T__20", "T__21", "T__22", "T__23", "T__24", 
			"T__25", "T__26", "T__27", "T__28", "T__29", "T__30", "T__31", "ATOM", 
			"LABEL", "BOOLEAN", "STRING", "WHITESPACE", "NEWLINE"
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


	public lolcodeLexer(CharStream input) {
		super(input);
		_interp = new LexerATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}

	@Override
	public String getGrammarFileName() { return "lolcode.g4"; }

	@Override
	public String[] getRuleNames() { return ruleNames; }

	@Override
	public String getSerializedATN() { return _serializedATN; }

	@Override
	public String[] getChannelNames() { return channelNames; }

	@Override
	public String[] getModeNames() { return modeNames; }

	@Override
	public ATN getATN() { return _ATN; }

	public static final String _serializedATN =
		"\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2(\u0167\b\1\4\2\t"+
		"\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13"+
		"\t\13\4\f\t\f\4\r\t\r\4\16\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22"+
		"\4\23\t\23\4\24\t\24\4\25\t\25\4\26\t\26\4\27\t\27\4\30\t\30\4\31\t\31"+
		"\4\32\t\32\4\33\t\33\4\34\t\34\4\35\t\35\4\36\t\36\4\37\t\37\4 \t \4!"+
		"\t!\4\"\t\"\4#\t#\4$\t$\4%\t%\4&\t&\4\'\t\'\3\2\3\2\3\2\3\2\3\3\3\3\3"+
		"\3\3\3\3\3\3\3\3\3\3\3\3\4\3\4\3\4\3\4\3\5\3\5\3\5\3\5\3\6\3\6\3\6\3\6"+
		"\3\6\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\b\3\b\3\b\3\b\3\t\3\t\3\t\3\t\3"+
		"\n\3\n\3\n\3\n\3\n\3\13\3\13\3\13\3\13\3\13\3\f\3\f\3\f\3\f\3\f\3\f\3"+
		"\f\3\f\3\r\3\r\3\r\3\r\3\r\3\r\3\16\3\16\3\16\3\16\3\16\3\16\3\16\3\17"+
		"\3\17\3\17\3\17\3\17\3\17\3\17\3\20\3\20\3\20\3\20\3\21\3\21\3\21\3\21"+
		"\3\21\3\21\3\22\3\22\3\22\3\22\3\22\3\22\3\22\3\23\3\23\3\23\3\23\3\23"+
		"\3\23\3\23\3\24\3\24\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25"+
		"\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\27\3\27\3\27\3\27\3\27"+
		"\3\27\3\27\3\27\3\30\3\30\3\30\3\30\3\30\3\30\3\30\3\30\3\30\3\30\3\31"+
		"\3\31\3\31\3\31\3\31\3\31\3\31\3\31\3\31\3\32\3\32\3\32\3\32\3\32\3\32"+
		"\3\32\3\32\3\32\3\32\3\33\3\33\3\33\3\33\3\33\3\33\3\33\3\34\3\34\3\34"+
		"\3\34\3\34\3\34\3\34\3\34\3\35\3\35\3\35\3\35\3\35\3\35\3\35\3\35\3\35"+
		"\3\35\3\35\3\36\3\36\3\36\3\36\3\36\3\36\3\36\3\36\3\36\3\36\3\36\3\36"+
		"\3\37\3\37\3\37\3\37\3\37\3\37\3\37\3 \3 \3 \3 \3!\3!\3!\3\"\3\"\3\"\3"+
		"\"\3\"\3\"\6\"\u012b\n\"\r\"\16\"\u012c\3\"\7\"\u0130\n\"\f\"\16\"\u0133"+
		"\13\"\3\"\3\"\7\"\u0137\n\"\f\"\16\"\u013a\13\"\3\"\5\"\u013d\n\"\3#\6"+
		"#\u0140\n#\r#\16#\u0141\3$\3$\3$\3$\3$\3$\3$\5$\u014b\n$\3%\3%\3%\3%\7"+
		"%\u0151\n%\f%\16%\u0154\13%\3%\3%\3&\3&\3&\3&\3\'\5\'\u015d\n\'\3\'\3"+
		"\'\6\'\u0161\n\'\r\'\16\'\u0162\3\'\5\'\u0166\n\'\2\2(\3\3\5\4\7\5\t\6"+
		"\13\7\r\b\17\t\21\n\23\13\25\f\27\r\31\16\33\17\35\20\37\21!\22#\23%\24"+
		"\'\25)\26+\27-\30/\31\61\32\63\33\65\34\67\359\36;\37= ?!A\"C#E$G%I&K"+
		"\'M(\3\2\4\6\2\62;C\\aac|\3\2$$\2\u0175\2\3\3\2\2\2\2\5\3\2\2\2\2\7\3"+
		"\2\2\2\2\t\3\2\2\2\2\13\3\2\2\2\2\r\3\2\2\2\2\17\3\2\2\2\2\21\3\2\2\2"+
		"\2\23\3\2\2\2\2\25\3\2\2\2\2\27\3\2\2\2\2\31\3\2\2\2\2\33\3\2\2\2\2\35"+
		"\3\2\2\2\2\37\3\2\2\2\2!\3\2\2\2\2#\3\2\2\2\2%\3\2\2\2\2\'\3\2\2\2\2)"+
		"\3\2\2\2\2+\3\2\2\2\2-\3\2\2\2\2/\3\2\2\2\2\61\3\2\2\2\2\63\3\2\2\2\2"+
		"\65\3\2\2\2\2\67\3\2\2\2\29\3\2\2\2\2;\3\2\2\2\2=\3\2\2\2\2?\3\2\2\2\2"+
		"A\3\2\2\2\2C\3\2\2\2\2E\3\2\2\2\2G\3\2\2\2\2I\3\2\2\2\2K\3\2\2\2\2M\3"+
		"\2\2\2\3O\3\2\2\2\5S\3\2\2\2\7[\3\2\2\2\t_\3\2\2\2\13c\3\2\2\2\rh\3\2"+
		"\2\2\17p\3\2\2\2\21t\3\2\2\2\23x\3\2\2\2\25}\3\2\2\2\27\u0082\3\2\2\2"+
		"\31\u008a\3\2\2\2\33\u0090\3\2\2\2\35\u0097\3\2\2\2\37\u009e\3\2\2\2!"+
		"\u00a2\3\2\2\2#\u00a8\3\2\2\2%\u00af\3\2\2\2\'\u00b6\3\2\2\2)\u00b8\3"+
		"\2\2\2+\u00c2\3\2\2\2-\u00cb\3\2\2\2/\u00d3\3\2\2\2\61\u00dd\3\2\2\2\63"+
		"\u00e6\3\2\2\2\65\u00f0\3\2\2\2\67\u00f7\3\2\2\29\u00ff\3\2\2\2;\u010a"+
		"\3\2\2\2=\u0116\3\2\2\2?\u011d\3\2\2\2A\u0121\3\2\2\2C\u013c\3\2\2\2E"+
		"\u013f\3\2\2\2G\u014a\3\2\2\2I\u014c\3\2\2\2K\u0157\3\2\2\2M\u0165\3\2"+
		"\2\2OP\7J\2\2PQ\7C\2\2QR\7K\2\2R\4\3\2\2\2ST\7M\2\2TU\7V\2\2UV\7J\2\2"+
		"VW\7Z\2\2WX\7D\2\2XY\7[\2\2YZ\7G\2\2Z\6\3\2\2\2[\\\7N\2\2\\]\7Q\2\2]^"+
		"\7N\2\2^\b\3\2\2\2_`\7I\2\2`a\7Q\2\2ab\7V\2\2b\n\3\2\2\2cd\7I\2\2de\7"+
		"G\2\2ef\7G\2\2fg\7M\2\2g\f\3\2\2\2hi\7K\2\2ij\7\"\2\2jk\7J\2\2kl\7C\2"+
		"\2lm\7U\2\2mn\7\"\2\2no\7C\2\2o\16\3\2\2\2pq\7K\2\2qr\7V\2\2rs\7\\\2\2"+
		"s\20\3\2\2\2tu\7D\2\2uv\7V\2\2vw\7Y\2\2w\22\3\2\2\2xy\7Q\2\2yz\7D\2\2"+
		"z{\7V\2\2{|\7Y\2\2|\24\3\2\2\2}~\7V\2\2~\177\7N\2\2\177\u0080\7F\2\2\u0080"+
		"\u0081\7T\2\2\u0081\26\3\2\2\2\u0082\u0083\7X\2\2\u0083\u0084\7K\2\2\u0084"+
		"\u0085\7U\2\2\u0085\u0086\7K\2\2\u0086\u0087\7D\2\2\u0087\u0088\7N\2\2"+
		"\u0088\u0089\7G\2\2\u0089\30\3\2\2\2\u008a\u008b\7O\2\2\u008b\u008c\7"+
		"M\2\2\u008c\u008d\7C\2\2\u008d\u008e\7[\2\2\u008e\u008f\7A\2\2\u008f\32"+
		"\3\2\2\2\u0090\u0091\7Q\2\2\u0091\u0092\7\"\2\2\u0092\u0093\7T\2\2\u0093"+
		"\u0094\7N\2\2\u0094\u0095\7[\2\2\u0095\u0096\7A\2\2\u0096\34\3\2\2\2\u0097"+
		"\u0098\7[\2\2\u0098\u0099\7C\2\2\u0099\u009a\7\"\2\2\u009a\u009b\7T\2"+
		"\2\u009b\u009c\7N\2\2\u009c\u009d\7[\2\2\u009d\36\3\2\2\2\u009e\u009f"+
		"\7Q\2\2\u009f\u00a0\7K\2\2\u00a0\u00a1\7E\2\2\u00a1 \3\2\2\2\u00a2\u00a3"+
		"\7O\2\2\u00a3\u00a4\7G\2\2\u00a4\u00a5\7D\2\2\u00a5\u00a6\7D\2\2\u00a6"+
		"\u00a7\7G\2\2\u00a7\"\3\2\2\2\u00a8\u00a9\7P\2\2\u00a9\u00aa\7Q\2\2\u00aa"+
		"\u00ab\7\"\2\2\u00ab\u00ac\7Y\2\2\u00ac\u00ad\7C\2\2\u00ad\u00ae\7K\2"+
		"\2\u00ae$\3\2\2\2\u00af\u00b0\7I\2\2\u00b0\u00b1\7K\2\2\u00b1\u00b2\7"+
		"O\2\2\u00b2\u00b3\7O\2\2\u00b3\u00b4\7G\2\2\u00b4\u00b5\7J\2\2\u00b5&"+
		"\3\2\2\2\u00b6\u00b7\7T\2\2\u00b7(\3\2\2\2\u00b8\u00b9\7D\2\2\u00b9\u00ba"+
		"\7Q\2\2\u00ba\u00bb\7V\2\2\u00bb\u00bc\7J\2\2\u00bc\u00bd\7\"\2\2\u00bd"+
		"\u00be\7U\2\2\u00be\u00bf\7C\2\2\u00bf\u00c0\7G\2\2\u00c0\u00c1\7O\2\2"+
		"\u00c1*\3\2\2\2\u00c2\u00c3\7F\2\2\u00c3\u00c4\7K\2\2\u00c4\u00c5\7H\2"+
		"\2\u00c5\u00c6\7H\2\2\u00c6\u00c7\7T\2\2\u00c7\u00c8\7K\2\2\u00c8\u00c9"+
		"\7P\2\2\u00c9\u00ca\7V\2\2\u00ca,\3\2\2\2\u00cb\u00cc\7D\2\2\u00cc\u00cd"+
		"\7Q\2\2\u00cd\u00ce\7V\2\2\u00ce\u00cf\7J\2\2\u00cf\u00d0\7\"\2\2\u00d0"+
		"\u00d1\7Q\2\2\u00d1\u00d2\7H\2\2\u00d2.\3\2\2\2\u00d3\u00d4\7G\2\2\u00d4"+
		"\u00d5\7K\2\2\u00d5\u00d6\7V\2\2\u00d6\u00d7\7J\2\2\u00d7\u00d8\7G\2\2"+
		"\u00d8\u00d9\7T\2\2\u00d9\u00da\7\"\2\2\u00da\u00db\7Q\2\2\u00db\u00dc"+
		"\7H\2\2\u00dc\60\3\2\2\2\u00dd\u00de\7D\2\2\u00de\u00df\7K\2\2\u00df\u00e0"+
		"\7I\2\2\u00e0\u00e1\7I\2\2\u00e1\u00e2\7T\2\2\u00e2\u00e3\7\"\2\2\u00e3"+
		"\u00e4\7Q\2\2\u00e4\u00e5\7H\2\2\u00e5\62\3\2\2\2\u00e6\u00e7\7U\2\2\u00e7"+
		"\u00e8\7O\2\2\u00e8\u00e9\7C\2\2\u00e9\u00ea\7N\2\2\u00ea\u00eb\7N\2\2"+
		"\u00eb\u00ec\7T\2\2\u00ec\u00ed\7\"\2\2\u00ed\u00ee\7Q\2\2\u00ee\u00ef"+
		"\7H\2\2\u00ef\64\3\2\2\2\u00f0\u00f1\7U\2\2\u00f1\u00f2\7W\2\2\u00f2\u00f3"+
		"\7O\2\2\u00f3\u00f4\7\"\2\2\u00f4\u00f5\7Q\2\2\u00f5\u00f6\7H\2\2\u00f6"+
		"\66\3\2\2\2\u00f7\u00f8\7F\2\2\u00f8\u00f9\7K\2\2\u00f9\u00fa\7H\2\2\u00fa"+
		"\u00fb\7H\2\2\u00fb\u00fc\7\"\2\2\u00fc\u00fd\7Q\2\2\u00fd\u00fe\7H\2"+
		"\2\u00fe8\3\2\2\2\u00ff\u0100\7R\2\2\u0100\u0101\7T\2\2\u0101\u0102\7"+
		"Q\2\2\u0102\u0103\7F\2\2\u0103\u0104\7W\2\2\u0104\u0105\7M\2\2\u0105\u0106"+
		"\7V\2\2\u0106\u0107\7\"\2\2\u0107\u0108\7Q\2\2\u0108\u0109\7H\2\2\u0109"+
		":\3\2\2\2\u010a\u010b\7S\2\2\u010b\u010c\7W\2\2\u010c\u010d\7Q\2\2\u010d"+
		"\u010e\7U\2\2\u010e\u010f\7J\2\2\u010f\u0110\7W\2\2\u0110\u0111\7P\2\2"+
		"\u0111\u0112\7V\2\2\u0112\u0113\7\"\2\2\u0113\u0114\7Q\2\2\u0114\u0115"+
		"\7H\2\2\u0115<\3\2\2\2\u0116\u0117\7O\2\2\u0117\u0118\7Q\2\2\u0118\u0119"+
		"\7F\2\2\u0119\u011a\7\"\2\2\u011a\u011b\7Q\2\2\u011b\u011c\7H\2\2\u011c"+
		">\3\2\2\2\u011d\u011e\7P\2\2\u011e\u011f\7Q\2\2\u011f\u0120\7V\2\2\u0120"+
		"@\3\2\2\2\u0121\u0122\7C\2\2\u0122\u0123\7P\2\2\u0123B\3\2\2\2\u0124\u013d"+
		"\5G$\2\u0125\u0126\7P\2\2\u0126\u0127\7Q\2\2\u0127\u0128\7Q\2\2\u0128"+
		"\u013d\7D\2\2\u0129\u012b\4\62;\2\u012a\u0129\3\2\2\2\u012b\u012c\3\2"+
		"\2\2\u012c\u012a\3\2\2\2\u012c\u012d\3\2\2\2\u012d\u013d\3\2\2\2\u012e"+
		"\u0130\4\62;\2\u012f\u012e\3\2\2\2\u0130\u0133\3\2\2\2\u0131\u012f\3\2"+
		"\2\2\u0131\u0132\3\2\2\2\u0132\u0134\3\2\2\2\u0133\u0131\3\2\2\2\u0134"+
		"\u0138\7\60\2\2\u0135\u0137\4\62;\2\u0136\u0135\3\2\2\2\u0137\u013a\3"+
		"\2\2\2\u0138\u0136\3\2\2\2\u0138\u0139\3\2\2\2\u0139\u013d\3\2\2\2\u013a"+
		"\u0138\3\2\2\2\u013b\u013d\5I%\2\u013c\u0124\3\2\2\2\u013c\u0125\3\2\2"+
		"\2\u013c\u012a\3\2\2\2\u013c\u0131\3\2\2\2\u013c\u013b\3\2\2\2\u013dD"+
		"\3\2\2\2\u013e\u0140\t\2\2\2\u013f\u013e\3\2\2\2\u0140\u0141\3\2\2\2\u0141"+
		"\u013f\3\2\2\2\u0141\u0142\3\2\2\2\u0142F\3\2\2\2\u0143\u0144\7Y\2\2\u0144"+
		"\u0145\7K\2\2\u0145\u014b\7P\2\2\u0146\u0147\7H\2\2\u0147\u0148\7C\2\2"+
		"\u0148\u0149\7K\2\2\u0149\u014b\7N\2\2\u014a\u0143\3\2\2\2\u014a\u0146"+
		"\3\2\2\2\u014bH\3\2\2\2\u014c\u0152\7$\2\2\u014d\u014e\7)\2\2\u014e\u0151"+
		"\7$\2\2\u014f\u0151\n\3\2\2\u0150\u014d\3\2\2\2\u0150\u014f\3\2\2\2\u0151"+
		"\u0154\3\2\2\2\u0152\u0150\3\2\2\2\u0152\u0153\3\2\2\2\u0153\u0155\3\2"+
		"\2\2\u0154\u0152\3\2\2\2\u0155\u0156\7$\2\2\u0156J\3\2\2\2\u0157\u0158"+
		"\7\"\2\2\u0158\u0159\3\2\2\2\u0159\u015a\b&\2\2\u015aL\3\2\2\2\u015b\u015d"+
		"\7\17\2\2\u015c\u015b\3\2\2\2\u015c\u015d\3\2\2\2\u015d\u015e\3\2\2\2"+
		"\u015e\u0161\7\f\2\2\u015f\u0161\7\17\2\2\u0160\u015c\3\2\2\2\u0160\u015f"+
		"\3\2\2\2\u0161\u0162\3\2\2\2\u0162\u0160\3\2\2\2\u0162\u0163\3\2\2\2\u0163"+
		"\u0166\3\2\2\2\u0164\u0166\7.\2\2\u0165\u0160\3\2\2\2\u0165\u0164\3\2"+
		"\2\2\u0166N\3\2\2\2\17\2\u012c\u0131\u0138\u013c\u0141\u014a\u0150\u0152"+
		"\u015c\u0160\u0162\u0165\3\b\2\2";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}