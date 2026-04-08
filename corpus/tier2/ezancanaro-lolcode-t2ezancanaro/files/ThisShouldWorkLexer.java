// Generated from C:\Users\Zanca\ThisShouldWork.g4 by ANTLR 4.1
   
import java.util.*;

import org.antlr.v4.runtime.Lexer;
import org.antlr.v4.runtime.CharStream;
import org.antlr.v4.runtime.Token;
import org.antlr.v4.runtime.TokenStream;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;
import org.antlr.v4.runtime.misc.*;

@SuppressWarnings({"all", "warnings", "unchecked", "unused", "cast"})
public class ThisShouldWorkLexer extends Lexer {
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
	public static String[] modeNames = {
		"DEFAULT_MODE"
	};

	public static final String[] tokenNames = {
		"<INVALID>",
		"'R'", "'NO WAI'", "'O RLY?'", "'!'", "'HAI'", "'CAN HAS'", "'KTHXBYE'", 
		"'?'", "'GIMMEH'", "'VISIBLE'", "'SUM OF'", "'DIFF OF'", "'PRODUKT OF'", 
		"'QUOSHUNT OF'", "'MOD OF'", "'BIGGR OF'", "'SMALLR OF'", "'BOTH SAEM'", 
		"'DIFFRINT'", "'AN'", "'IM IN YR'", "'IM OUTTA YR'", "'O RLY'", "'OIC'", 
		"'YA RLY'", "'NO WAY'", "'I HAS A'", "'ITZ'", "'GTFO'", "BOOLEANS", "SEPARATOR", 
		"STRING", "ID", "LETTER", "DIGIT", "FLOAT", "COMMENT", "BLOCKCOMMENT", 
		"NL", "WS"
	};
	public static final String[] ruleNames = {
		"T__3", "T__2", "T__1", "T__0", "HAI", "CANHAS", "KTHXBYE", "QUESTIONMARK", 
		"GIMMEH", "VISIBLE", "SUM", "DIFF", "PRODUKT", "QUOSHUNT", "MOD", "BIGGR", 
		"SMALLR", "EQUALS", "DIFFRINT", "AN", "LOOPIN", "LOOPOUT", "IFIN", "IFOUT", 
		"THEN", "ELSE", "VARI", "ITZ", "GTFO", "BOOLEANS", "SEPARATOR", "STRING", 
		"STR_TEXT", "ESC_SEQ", "ID", "LETTER", "DIGIT", "FLOAT", "COMMENT", "BLOCKCOMMENT", 
		"NL", "WS"
	};


	 


	public ThisShouldWorkLexer(CharStream input) {
		super(input);
		_interp = new LexerATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}

	@Override
	public String getGrammarFileName() { return "ThisShouldWork.g4"; }

	@Override
	public String[] getTokenNames() { return tokenNames; }

	@Override
	public String[] getRuleNames() { return ruleNames; }

	@Override
	public String[] getModeNames() { return modeNames; }

	@Override
	public ATN getATN() { return _ATN; }

	@Override
	public void action(RuleContext _localctx, int ruleIndex, int actionIndex) {
		switch (ruleIndex) {
		case 38: COMMENT_action((RuleContext)_localctx, actionIndex); break;

		case 39: BLOCKCOMMENT_action((RuleContext)_localctx, actionIndex); break;

		case 41: WS_action((RuleContext)_localctx, actionIndex); break;
		}
	}
	private void BLOCKCOMMENT_action(RuleContext _localctx, int actionIndex) {
		switch (actionIndex) {
		case 2: skip();  break;
		}
	}
	private void WS_action(RuleContext _localctx, int actionIndex) {
		switch (actionIndex) {
		case 0: skip(); break;
		}
	}
	private void COMMENT_action(RuleContext _localctx, int actionIndex) {
		switch (actionIndex) {
		case 1: skip();  break;
		}
	}

	public static final String _serializedATN =
		"\3\uacf5\uee8c\u4f5d\u8b0d\u4a45\u78bd\u1b2f\u3378\2*\u0187\b\1\4\2\t"+
		"\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13"+
		"\t\13\4\f\t\f\4\r\t\r\4\16\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22"+
		"\4\23\t\23\4\24\t\24\4\25\t\25\4\26\t\26\4\27\t\27\4\30\t\30\4\31\t\31"+
		"\4\32\t\32\4\33\t\33\4\34\t\34\4\35\t\35\4\36\t\36\4\37\t\37\4 \t \4!"+
		"\t!\4\"\t\"\4#\t#\4$\t$\4%\t%\4&\t&\4\'\t\'\4(\t(\4)\t)\4*\t*\4+\t+\3"+
		"\2\3\2\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\5\3\5"+
		"\3\6\3\6\3\6\3\6\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\b\3\b\3\b\3\b\3\b\3"+
		"\b\3\b\3\b\3\t\3\t\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\13\3\13\3\13\3\13\3\13"+
		"\3\13\3\13\3\13\3\f\3\f\3\f\3\f\3\f\3\f\3\f\3\r\3\r\3\r\3\r\3\r\3\r\3"+
		"\r\3\r\3\16\3\16\3\16\3\16\3\16\3\16\3\16\3\16\3\16\3\16\3\16\3\17\3\17"+
		"\3\17\3\17\3\17\3\17\3\17\3\17\3\17\3\17\3\17\3\17\3\20\3\20\3\20\3\20"+
		"\3\20\3\20\3\20\3\21\3\21\3\21\3\21\3\21\3\21\3\21\3\21\3\21\3\22\3\22"+
		"\3\22\3\22\3\22\3\22\3\22\3\22\3\22\3\22\3\23\3\23\3\23\3\23\3\23\3\23"+
		"\3\23\3\23\3\23\3\23\3\24\3\24\3\24\3\24\3\24\3\24\3\24\3\24\3\24\3\25"+
		"\3\25\3\25\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\27\3\27\3\27"+
		"\3\27\3\27\3\27\3\27\3\27\3\27\3\27\3\27\3\27\3\30\3\30\3\30\3\30\3\30"+
		"\3\30\3\31\3\31\3\31\3\31\3\32\3\32\3\32\3\32\3\32\3\32\3\32\3\33\3\33"+
		"\3\33\3\33\3\33\3\33\3\33\3\34\3\34\3\34\3\34\3\34\3\34\3\34\3\34\3\35"+
		"\3\35\3\35\3\35\3\36\3\36\3\36\3\36\3\36\3\37\3\37\3\37\3\37\3\37\3\37"+
		"\3\37\5\37\u012a\n\37\3 \3 \5 \u012e\n \3!\3!\3!\7!\u0133\n!\f!\16!\u0136"+
		"\13!\3!\3!\3\"\3\"\6\"\u013c\n\"\r\"\16\"\u013d\3#\3#\5#\u0142\n#\3$\3"+
		"$\3$\3$\7$\u0148\n$\f$\16$\u014b\13$\3%\6%\u014e\n%\r%\16%\u014f\3&\6"+
		"&\u0153\n&\r&\16&\u0154\3\'\3\'\3\'\5\'\u015a\n\'\3(\3(\3(\3(\3(\7(\u0161"+
		"\n(\f(\16(\u0164\13(\3(\3(\3(\3(\3)\3)\3)\3)\3)\3)\7)\u0170\n)\f)\16)"+
		"\u0173\13)\3)\3)\3)\3)\3)\3)\3)\3*\5*\u017d\n*\3*\3*\3+\6+\u0182\n+\r"+
		"+\16+\u0183\3+\3+\4\u0162\u0171,\3\3\1\5\4\1\7\5\1\t\6\1\13\7\1\r\b\1"+
		"\17\t\1\21\n\1\23\13\1\25\f\1\27\r\1\31\16\1\33\17\1\35\20\1\37\21\1!"+
		"\22\1#\23\1%\24\1\'\25\1)\26\1+\27\1-\30\1/\31\1\61\32\1\63\33\1\65\34"+
		"\1\67\35\19\36\1;\37\1= \1?!\1A\"\1C\2\1E\2\1G#\1I$\1K%\1M&\1O\'\3Q(\4"+
		"S)\1U*\2\3\2\7\6\2\f\f\17\17$$^^\7\3$$^^ddhhvv\4\2C\\c|\3\2\62;\6\2\13"+
		"\13\"\"))..\u0194\2\3\3\2\2\2\2\5\3\2\2\2\2\7\3\2\2\2\2\t\3\2\2\2\2\13"+
		"\3\2\2\2\2\r\3\2\2\2\2\17\3\2\2\2\2\21\3\2\2\2\2\23\3\2\2\2\2\25\3\2\2"+
		"\2\2\27\3\2\2\2\2\31\3\2\2\2\2\33\3\2\2\2\2\35\3\2\2\2\2\37\3\2\2\2\2"+
		"!\3\2\2\2\2#\3\2\2\2\2%\3\2\2\2\2\'\3\2\2\2\2)\3\2\2\2\2+\3\2\2\2\2-\3"+
		"\2\2\2\2/\3\2\2\2\2\61\3\2\2\2\2\63\3\2\2\2\2\65\3\2\2\2\2\67\3\2\2\2"+
		"\29\3\2\2\2\2;\3\2\2\2\2=\3\2\2\2\2?\3\2\2\2\2A\3\2\2\2\2G\3\2\2\2\2I"+
		"\3\2\2\2\2K\3\2\2\2\2M\3\2\2\2\2O\3\2\2\2\2Q\3\2\2\2\2S\3\2\2\2\2U\3\2"+
		"\2\2\3W\3\2\2\2\5Y\3\2\2\2\7`\3\2\2\2\tg\3\2\2\2\13i\3\2\2\2\rm\3\2\2"+
		"\2\17u\3\2\2\2\21}\3\2\2\2\23\177\3\2\2\2\25\u0086\3\2\2\2\27\u008e\3"+
		"\2\2\2\31\u0095\3\2\2\2\33\u009d\3\2\2\2\35\u00a8\3\2\2\2\37\u00b4\3\2"+
		"\2\2!\u00bb\3\2\2\2#\u00c4\3\2\2\2%\u00ce\3\2\2\2\'\u00d8\3\2\2\2)\u00e1"+
		"\3\2\2\2+\u00e4\3\2\2\2-\u00ed\3\2\2\2/\u00f9\3\2\2\2\61\u00ff\3\2\2\2"+
		"\63\u0103\3\2\2\2\65\u010a\3\2\2\2\67\u0111\3\2\2\29\u0119\3\2\2\2;\u011d"+
		"\3\2\2\2=\u0129\3\2\2\2?\u012d\3\2\2\2A\u012f\3\2\2\2C\u013b\3\2\2\2E"+
		"\u013f\3\2\2\2G\u0143\3\2\2\2I\u014d\3\2\2\2K\u0152\3\2\2\2M\u0156\3\2"+
		"\2\2O\u015b\3\2\2\2Q\u0169\3\2\2\2S\u017c\3\2\2\2U\u0181\3\2\2\2WX\7T"+
		"\2\2X\4\3\2\2\2YZ\7P\2\2Z[\7Q\2\2[\\\7\"\2\2\\]\7Y\2\2]^\7C\2\2^_\7K\2"+
		"\2_\6\3\2\2\2`a\7Q\2\2ab\7\"\2\2bc\7T\2\2cd\7N\2\2de\7[\2\2ef\7A\2\2f"+
		"\b\3\2\2\2gh\7#\2\2h\n\3\2\2\2ij\7J\2\2jk\7C\2\2kl\7K\2\2l\f\3\2\2\2m"+
		"n\7E\2\2no\7C\2\2op\7P\2\2pq\7\"\2\2qr\7J\2\2rs\7C\2\2st\7U\2\2t\16\3"+
		"\2\2\2uv\7M\2\2vw\7V\2\2wx\7J\2\2xy\7Z\2\2yz\7D\2\2z{\7[\2\2{|\7G\2\2"+
		"|\20\3\2\2\2}~\7A\2\2~\22\3\2\2\2\177\u0080\7I\2\2\u0080\u0081\7K\2\2"+
		"\u0081\u0082\7O\2\2\u0082\u0083\7O\2\2\u0083\u0084\7G\2\2\u0084\u0085"+
		"\7J\2\2\u0085\24\3\2\2\2\u0086\u0087\7X\2\2\u0087\u0088\7K\2\2\u0088\u0089"+
		"\7U\2\2\u0089\u008a\7K\2\2\u008a\u008b\7D\2\2\u008b\u008c\7N\2\2\u008c"+
		"\u008d\7G\2\2\u008d\26\3\2\2\2\u008e\u008f\7U\2\2\u008f\u0090\7W\2\2\u0090"+
		"\u0091\7O\2\2\u0091\u0092\7\"\2\2\u0092\u0093\7Q\2\2\u0093\u0094\7H\2"+
		"\2\u0094\30\3\2\2\2\u0095\u0096\7F\2\2\u0096\u0097\7K\2\2\u0097\u0098"+
		"\7H\2\2\u0098\u0099\7H\2\2\u0099\u009a\7\"\2\2\u009a\u009b\7Q\2\2\u009b"+
		"\u009c\7H\2\2\u009c\32\3\2\2\2\u009d\u009e\7R\2\2\u009e\u009f\7T\2\2\u009f"+
		"\u00a0\7Q\2\2\u00a0\u00a1\7F\2\2\u00a1\u00a2\7W\2\2\u00a2\u00a3\7M\2\2"+
		"\u00a3\u00a4\7V\2\2\u00a4\u00a5\7\"\2\2\u00a5\u00a6\7Q\2\2\u00a6\u00a7"+
		"\7H\2\2\u00a7\34\3\2\2\2\u00a8\u00a9\7S\2\2\u00a9\u00aa\7W\2\2\u00aa\u00ab"+
		"\7Q\2\2\u00ab\u00ac\7U\2\2\u00ac\u00ad\7J\2\2\u00ad\u00ae\7W\2\2\u00ae"+
		"\u00af\7P\2\2\u00af\u00b0\7V\2\2\u00b0\u00b1\7\"\2\2\u00b1\u00b2\7Q\2"+
		"\2\u00b2\u00b3\7H\2\2\u00b3\36\3\2\2\2\u00b4\u00b5\7O\2\2\u00b5\u00b6"+
		"\7Q\2\2\u00b6\u00b7\7F\2\2\u00b7\u00b8\7\"\2\2\u00b8\u00b9\7Q\2\2\u00b9"+
		"\u00ba\7H\2\2\u00ba \3\2\2\2\u00bb\u00bc\7D\2\2\u00bc\u00bd\7K\2\2\u00bd"+
		"\u00be\7I\2\2\u00be\u00bf\7I\2\2\u00bf\u00c0\7T\2\2\u00c0\u00c1\7\"\2"+
		"\2\u00c1\u00c2\7Q\2\2\u00c2\u00c3\7H\2\2\u00c3\"\3\2\2\2\u00c4\u00c5\7"+
		"U\2\2\u00c5\u00c6\7O\2\2\u00c6\u00c7\7C\2\2\u00c7\u00c8\7N\2\2\u00c8\u00c9"+
		"\7N\2\2\u00c9\u00ca\7T\2\2\u00ca\u00cb\7\"\2\2\u00cb\u00cc\7Q\2\2\u00cc"+
		"\u00cd\7H\2\2\u00cd$\3\2\2\2\u00ce\u00cf\7D\2\2\u00cf\u00d0\7Q\2\2\u00d0"+
		"\u00d1\7V\2\2\u00d1\u00d2\7J\2\2\u00d2\u00d3\7\"\2\2\u00d3\u00d4\7U\2"+
		"\2\u00d4\u00d5\7C\2\2\u00d5\u00d6\7G\2\2\u00d6\u00d7\7O\2\2\u00d7&\3\2"+
		"\2\2\u00d8\u00d9\7F\2\2\u00d9\u00da\7K\2\2\u00da\u00db\7H\2\2\u00db\u00dc"+
		"\7H\2\2\u00dc\u00dd\7T\2\2\u00dd\u00de\7K\2\2\u00de\u00df\7P\2\2\u00df"+
		"\u00e0\7V\2\2\u00e0(\3\2\2\2\u00e1\u00e2\7C\2\2\u00e2\u00e3\7P\2\2\u00e3"+
		"*\3\2\2\2\u00e4\u00e5\7K\2\2\u00e5\u00e6\7O\2\2\u00e6\u00e7\7\"\2\2\u00e7"+
		"\u00e8\7K\2\2\u00e8\u00e9\7P\2\2\u00e9\u00ea\7\"\2\2\u00ea\u00eb\7[\2"+
		"\2\u00eb\u00ec\7T\2\2\u00ec,\3\2\2\2\u00ed\u00ee\7K\2\2\u00ee\u00ef\7"+
		"O\2\2\u00ef\u00f0\7\"\2\2\u00f0\u00f1\7Q\2\2\u00f1\u00f2\7W\2\2\u00f2"+
		"\u00f3\7V\2\2\u00f3\u00f4\7V\2\2\u00f4\u00f5\7C\2\2\u00f5\u00f6\7\"\2"+
		"\2\u00f6\u00f7\7[\2\2\u00f7\u00f8\7T\2\2\u00f8.\3\2\2\2\u00f9\u00fa\7"+
		"Q\2\2\u00fa\u00fb\7\"\2\2\u00fb\u00fc\7T\2\2\u00fc\u00fd\7N\2\2\u00fd"+
		"\u00fe\7[\2\2\u00fe\60\3\2\2\2\u00ff\u0100\7Q\2\2\u0100\u0101\7K\2\2\u0101"+
		"\u0102\7E\2\2\u0102\62\3\2\2\2\u0103\u0104\7[\2\2\u0104\u0105\7C\2\2\u0105"+
		"\u0106\7\"\2\2\u0106\u0107\7T\2\2\u0107\u0108\7N\2\2\u0108\u0109\7[\2"+
		"\2\u0109\64\3\2\2\2\u010a\u010b\7P\2\2\u010b\u010c\7Q\2\2\u010c\u010d"+
		"\7\"\2\2\u010d\u010e\7Y\2\2\u010e\u010f\7C\2\2\u010f\u0110\7[\2\2\u0110"+
		"\66\3\2\2\2\u0111\u0112\7K\2\2\u0112\u0113\7\"\2\2\u0113\u0114\7J\2\2"+
		"\u0114\u0115\7C\2\2\u0115\u0116\7U\2\2\u0116\u0117\7\"\2\2\u0117\u0118"+
		"\7C\2\2\u01188\3\2\2\2\u0119\u011a\7K\2\2\u011a\u011b\7V\2\2\u011b\u011c"+
		"\7\\\2\2\u011c:\3\2\2\2\u011d\u011e\7I\2\2\u011e\u011f\7V\2\2\u011f\u0120"+
		"\7H\2\2\u0120\u0121\7Q\2\2\u0121<\3\2\2\2\u0122\u0123\7Y\2\2\u0123\u0124"+
		"\7K\2\2\u0124\u012a\7P\2\2\u0125\u0126\7N\2\2\u0126\u0127\7Q\2\2\u0127"+
		"\u0128\7U\2\2\u0128\u012a\7G\2\2\u0129\u0122\3\2\2\2\u0129\u0125\3\2\2"+
		"\2\u012a>\3\2\2\2\u012b\u012e\7.\2\2\u012c\u012e\5S*\2\u012d\u012b\3\2"+
		"\2\2\u012d\u012c\3\2\2\2\u012e@\3\2\2\2\u012f\u0134\7$\2\2\u0130\u0133"+
		"\5C\"\2\u0131\u0133\5S*\2\u0132\u0130\3\2\2\2\u0132\u0131\3\2\2\2\u0133"+
		"\u0136\3\2\2\2\u0134\u0132\3\2\2\2\u0134\u0135\3\2\2\2\u0135\u0137\3\2"+
		"\2\2\u0136\u0134\3\2\2\2\u0137\u0138\7$\2\2\u0138B\3\2\2\2\u0139\u013c"+
		"\n\2\2\2\u013a\u013c\5E#\2\u013b\u0139\3\2\2\2\u013b\u013a\3\2\2\2\u013c"+
		"\u013d\3\2\2\2\u013d\u013b\3\2\2\2\u013d\u013e\3\2\2\2\u013eD\3\2\2\2"+
		"\u013f\u0141\7^\2\2\u0140\u0142\t\3\2\2\u0141\u0140\3\2\2\2\u0142F\3\2"+
		"\2\2\u0143\u0149\5I%\2\u0144\u0148\5I%\2\u0145\u0148\5K&\2\u0146\u0148"+
		"\7a\2\2\u0147\u0144\3\2\2\2\u0147\u0145\3\2\2\2\u0147\u0146\3\2\2\2\u0148"+
		"\u014b\3\2\2\2\u0149\u0147\3\2\2\2\u0149\u014a\3\2\2\2\u014aH\3\2\2\2"+
		"\u014b\u0149\3\2\2\2\u014c\u014e\t\4\2\2\u014d\u014c\3\2\2\2\u014e\u014f"+
		"\3\2\2\2\u014f\u014d\3\2\2\2\u014f\u0150\3\2\2\2\u0150J\3\2\2\2\u0151"+
		"\u0153\t\5\2\2\u0152\u0151\3\2\2\2\u0153\u0154\3\2\2\2\u0154\u0152\3\2"+
		"\2\2\u0154\u0155\3\2\2\2\u0155L\3\2\2\2\u0156\u0159\5K&\2\u0157\u0158"+
		"\7.\2\2\u0158\u015a\5K&\2\u0159\u0157\3\2\2\2\u0159\u015a\3\2\2\2\u015a"+
		"N\3\2\2\2\u015b\u015c\7D\2\2\u015c\u015d\7V\2\2\u015d\u015e\7Y\2\2\u015e"+
		"\u0162\3\2\2\2\u015f\u0161\13\2\2\2\u0160\u015f\3\2\2\2\u0161\u0164\3"+
		"\2\2\2\u0162\u0163\3\2\2\2\u0162\u0160\3\2\2\2\u0163\u0165\3\2\2\2\u0164"+
		"\u0162\3\2\2\2\u0165\u0166\5S*\2\u0166\u0167\3\2\2\2\u0167\u0168\b(\3"+
		"\2\u0168P\3\2\2\2\u0169\u016a\7Q\2\2\u016a\u016b\7D\2\2\u016b\u016c\7"+
		"V\2\2\u016c\u016d\7Y\2\2\u016d\u0171\3\2\2\2\u016e\u0170\13\2\2\2\u016f"+
		"\u016e\3\2\2\2\u0170\u0173\3\2\2\2\u0171\u0172\3\2\2\2\u0171\u016f\3\2"+
		"\2\2\u0172\u0174\3\2\2\2\u0173\u0171\3\2\2\2\u0174\u0175\7V\2\2\u0175"+
		"\u0176\7N\2\2\u0176\u0177\7F\2\2\u0177\u0178\7T\2\2\u0178\u0179\3\2\2"+
		"\2\u0179\u017a\b)\4\2\u017aR\3\2\2\2\u017b\u017d\7\17\2\2\u017c\u017b"+
		"\3\2\2\2\u017c\u017d\3\2\2\2\u017d\u017e\3\2\2\2\u017e\u017f\7\f\2\2\u017f"+
		"T\3\2\2\2\u0180\u0182\t\6\2\2\u0181\u0180\3\2\2\2\u0182\u0183\3\2\2\2"+
		"\u0183\u0181\3\2\2\2\u0183\u0184\3\2\2\2\u0184\u0185\3\2\2\2\u0185\u0186"+
		"\b+\2\2\u0186V\3\2\2\2\23\2\u0129\u012d\u0132\u0134\u013b\u013d\u0141"+
		"\u0147\u0149\u014f\u0154\u0159\u0162\u0171\u017c\u0183";
	public static final ATN _ATN =
		ATNSimulator.deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}