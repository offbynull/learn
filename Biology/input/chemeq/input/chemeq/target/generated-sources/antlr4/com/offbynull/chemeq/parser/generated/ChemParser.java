// Generated from com/offbynull/chemeq/parser/generated/Chem.g4 by ANTLR 4.7.2
package com.offbynull.chemeq.parser.generated;
import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.misc.*;
import org.antlr.v4.runtime.tree.*;
import java.util.List;
import java.util.Iterator;
import java.util.ArrayList;

@SuppressWarnings({"all", "warnings", "unchecked", "unused", "cast"})
public class ChemParser extends Parser {
	static { RuntimeMetaData.checkVersion("4.7.2", RuntimeMetaData.VERSION); }

	protected static final DFA[] _decisionToDFA;
	protected static final PredictionContextCache _sharedContextCache =
		new PredictionContextCache();
	public static final int
		T__0=1, T__1=2, UNIDIRECTIONAL=3, BIDIRECTIONAL=4, PLUS=5, COUNT=6, SYMBOL=7, 
		WS=8;
	public static final int
		RULE_chemEq = 0, RULE_chemEqSet = 1, RULE_chemEqUnit = 2, RULE_bond = 3, 
		RULE_bondUnit = 4;
	private static String[] makeRuleNames() {
		return new String[] {
			"chemEq", "chemEqSet", "chemEqUnit", "bond", "bondUnit"
		};
	}
	public static final String[] ruleNames = makeRuleNames();

	private static String[] makeLiteralNames() {
		return new String[] {
			null, "'('", "')'", "'->'", "'<->'", "'+'"
		};
	}
	private static final String[] _LITERAL_NAMES = makeLiteralNames();
	private static String[] makeSymbolicNames() {
		return new String[] {
			null, null, null, "UNIDIRECTIONAL", "BIDIRECTIONAL", "PLUS", "COUNT", 
			"SYMBOL", "WS"
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
	public String getGrammarFileName() { return "Chem.g4"; }

	@Override
	public String[] getRuleNames() { return ruleNames; }

	@Override
	public String getSerializedATN() { return _serializedATN; }

	@Override
	public ATN getATN() { return _ATN; }

	public ChemParser(TokenStream input) {
		super(input);
		_interp = new ParserATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}

	public static class ChemEqContext extends ParserRuleContext {
		public ChemEqContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_chemEq; }
	 
		public ChemEqContext() { }
		public void copyFrom(ChemEqContext ctx) {
			super.copyFrom(ctx);
		}
	}
	public static class UnidirChemEqContext extends ChemEqContext {
		public List<ChemEqSetContext> chemEqSet() {
			return getRuleContexts(ChemEqSetContext.class);
		}
		public ChemEqSetContext chemEqSet(int i) {
			return getRuleContext(ChemEqSetContext.class,i);
		}
		public TerminalNode UNIDIRECTIONAL() { return getToken(ChemParser.UNIDIRECTIONAL, 0); }
		public UnidirChemEqContext(ChemEqContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof ChemListener ) ((ChemListener)listener).enterUnidirChemEq(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof ChemListener ) ((ChemListener)listener).exitUnidirChemEq(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof ChemVisitor ) return ((ChemVisitor<? extends T>)visitor).visitUnidirChemEq(this);
			else return visitor.visitChildren(this);
		}
	}
	public static class BidirChemEqContext extends ChemEqContext {
		public List<ChemEqSetContext> chemEqSet() {
			return getRuleContexts(ChemEqSetContext.class);
		}
		public ChemEqSetContext chemEqSet(int i) {
			return getRuleContext(ChemEqSetContext.class,i);
		}
		public TerminalNode BIDIRECTIONAL() { return getToken(ChemParser.BIDIRECTIONAL, 0); }
		public BidirChemEqContext(ChemEqContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof ChemListener ) ((ChemListener)listener).enterBidirChemEq(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof ChemListener ) ((ChemListener)listener).exitBidirChemEq(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof ChemVisitor ) return ((ChemVisitor<? extends T>)visitor).visitBidirChemEq(this);
			else return visitor.visitChildren(this);
		}
	}

	public final ChemEqContext chemEq() throws RecognitionException {
		ChemEqContext _localctx = new ChemEqContext(_ctx, getState());
		enterRule(_localctx, 0, RULE_chemEq);
		try {
			setState(18);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,0,_ctx) ) {
			case 1:
				_localctx = new UnidirChemEqContext(_localctx);
				enterOuterAlt(_localctx, 1);
				{
				setState(10);
				chemEqSet();
				setState(11);
				match(UNIDIRECTIONAL);
				setState(12);
				chemEqSet();
				}
				break;
			case 2:
				_localctx = new BidirChemEqContext(_localctx);
				enterOuterAlt(_localctx, 2);
				{
				setState(14);
				chemEqSet();
				setState(15);
				match(BIDIRECTIONAL);
				setState(16);
				chemEqSet();
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

	public static class ChemEqSetContext extends ParserRuleContext {
		public List<ChemEqUnitContext> chemEqUnit() {
			return getRuleContexts(ChemEqUnitContext.class);
		}
		public ChemEqUnitContext chemEqUnit(int i) {
			return getRuleContext(ChemEqUnitContext.class,i);
		}
		public List<TerminalNode> PLUS() { return getTokens(ChemParser.PLUS); }
		public TerminalNode PLUS(int i) {
			return getToken(ChemParser.PLUS, i);
		}
		public ChemEqSetContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_chemEqSet; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof ChemListener ) ((ChemListener)listener).enterChemEqSet(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof ChemListener ) ((ChemListener)listener).exitChemEqSet(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof ChemVisitor ) return ((ChemVisitor<? extends T>)visitor).visitChemEqSet(this);
			else return visitor.visitChildren(this);
		}
	}

	public final ChemEqSetContext chemEqSet() throws RecognitionException {
		ChemEqSetContext _localctx = new ChemEqSetContext(_ctx, getState());
		enterRule(_localctx, 2, RULE_chemEqSet);
		try {
			int _alt;
			enterOuterAlt(_localctx, 1);
			{
			setState(25);
			_errHandler.sync(this);
			_alt = getInterpreter().adaptivePredict(_input,1,_ctx);
			while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER ) {
				if ( _alt==1 ) {
					{
					{
					setState(20);
					chemEqUnit();
					setState(21);
					match(PLUS);
					}
					} 
				}
				setState(27);
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,1,_ctx);
			}
			setState(28);
			chemEqUnit();
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

	public static class ChemEqUnitContext extends ParserRuleContext {
		public BondContext bond() {
			return getRuleContext(BondContext.class,0);
		}
		public TerminalNode COUNT() { return getToken(ChemParser.COUNT, 0); }
		public ChemEqUnitContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_chemEqUnit; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof ChemListener ) ((ChemListener)listener).enterChemEqUnit(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof ChemListener ) ((ChemListener)listener).exitChemEqUnit(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof ChemVisitor ) return ((ChemVisitor<? extends T>)visitor).visitChemEqUnit(this);
			else return visitor.visitChildren(this);
		}
	}

	public final ChemEqUnitContext chemEqUnit() throws RecognitionException {
		ChemEqUnitContext _localctx = new ChemEqUnitContext(_ctx, getState());
		enterRule(_localctx, 4, RULE_chemEqUnit);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(31);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==COUNT) {
				{
				setState(30);
				match(COUNT);
				}
			}

			setState(33);
			bond();
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

	public static class BondContext extends ParserRuleContext {
		public List<BondUnitContext> bondUnit() {
			return getRuleContexts(BondUnitContext.class);
		}
		public BondUnitContext bondUnit(int i) {
			return getRuleContext(BondUnitContext.class,i);
		}
		public BondContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_bond; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof ChemListener ) ((ChemListener)listener).enterBond(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof ChemListener ) ((ChemListener)listener).exitBond(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof ChemVisitor ) return ((ChemVisitor<? extends T>)visitor).visitBond(this);
			else return visitor.visitChildren(this);
		}
	}

	public final BondContext bond() throws RecognitionException {
		BondContext _localctx = new BondContext(_ctx, getState());
		enterRule(_localctx, 6, RULE_bond);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(36); 
			_errHandler.sync(this);
			_la = _input.LA(1);
			do {
				{
				{
				setState(35);
				bondUnit();
				}
				}
				setState(38); 
				_errHandler.sync(this);
				_la = _input.LA(1);
			} while ( _la==T__0 || _la==SYMBOL );
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

	public static class BondUnitContext extends ParserRuleContext {
		public BondUnitContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_bondUnit; }
	 
		public BondUnitContext() { }
		public void copyFrom(BondUnitContext ctx) {
			super.copyFrom(ctx);
		}
	}
	public static class GroupedBondUnitContext extends BondUnitContext {
		public List<BondUnitContext> bondUnit() {
			return getRuleContexts(BondUnitContext.class);
		}
		public BondUnitContext bondUnit(int i) {
			return getRuleContext(BondUnitContext.class,i);
		}
		public TerminalNode COUNT() { return getToken(ChemParser.COUNT, 0); }
		public GroupedBondUnitContext(BondUnitContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof ChemListener ) ((ChemListener)listener).enterGroupedBondUnit(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof ChemListener ) ((ChemListener)listener).exitGroupedBondUnit(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof ChemVisitor ) return ((ChemVisitor<? extends T>)visitor).visitGroupedBondUnit(this);
			else return visitor.visitChildren(this);
		}
	}
	public static class SingleBondUnitContext extends BondUnitContext {
		public TerminalNode SYMBOL() { return getToken(ChemParser.SYMBOL, 0); }
		public TerminalNode COUNT() { return getToken(ChemParser.COUNT, 0); }
		public SingleBondUnitContext(BondUnitContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof ChemListener ) ((ChemListener)listener).enterSingleBondUnit(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof ChemListener ) ((ChemListener)listener).exitSingleBondUnit(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof ChemVisitor ) return ((ChemVisitor<? extends T>)visitor).visitSingleBondUnit(this);
			else return visitor.visitChildren(this);
		}
	}

	public final BondUnitContext bondUnit() throws RecognitionException {
		BondUnitContext _localctx = new BondUnitContext(_ctx, getState());
		enterRule(_localctx, 8, RULE_bondUnit);
		int _la;
		try {
			setState(54);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case SYMBOL:
				_localctx = new SingleBondUnitContext(_localctx);
				enterOuterAlt(_localctx, 1);
				{
				setState(40);
				match(SYMBOL);
				setState(42);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==COUNT) {
					{
					setState(41);
					match(COUNT);
					}
				}

				}
				break;
			case T__0:
				_localctx = new GroupedBondUnitContext(_localctx);
				enterOuterAlt(_localctx, 2);
				{
				setState(44);
				match(T__0);
				setState(46); 
				_errHandler.sync(this);
				_la = _input.LA(1);
				do {
					{
					{
					setState(45);
					bondUnit();
					}
					}
					setState(48); 
					_errHandler.sync(this);
					_la = _input.LA(1);
				} while ( _la==T__0 || _la==SYMBOL );
				setState(50);
				match(T__1);
				setState(52);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==COUNT) {
					{
					setState(51);
					match(COUNT);
					}
				}

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

	public static final String _serializedATN =
		"\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\n;\4\2\t\2\4\3\t"+
		"\3\4\4\t\4\4\5\t\5\4\6\t\6\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\5\2\25\n\2"+
		"\3\3\3\3\3\3\7\3\32\n\3\f\3\16\3\35\13\3\3\3\3\3\3\4\5\4\"\n\4\3\4\3\4"+
		"\3\5\6\5\'\n\5\r\5\16\5(\3\6\3\6\5\6-\n\6\3\6\3\6\6\6\61\n\6\r\6\16\6"+
		"\62\3\6\3\6\5\6\67\n\6\5\69\n\6\3\6\2\2\7\2\4\6\b\n\2\2\2=\2\24\3\2\2"+
		"\2\4\33\3\2\2\2\6!\3\2\2\2\b&\3\2\2\2\n8\3\2\2\2\f\r\5\4\3\2\r\16\7\5"+
		"\2\2\16\17\5\4\3\2\17\25\3\2\2\2\20\21\5\4\3\2\21\22\7\6\2\2\22\23\5\4"+
		"\3\2\23\25\3\2\2\2\24\f\3\2\2\2\24\20\3\2\2\2\25\3\3\2\2\2\26\27\5\6\4"+
		"\2\27\30\7\7\2\2\30\32\3\2\2\2\31\26\3\2\2\2\32\35\3\2\2\2\33\31\3\2\2"+
		"\2\33\34\3\2\2\2\34\36\3\2\2\2\35\33\3\2\2\2\36\37\5\6\4\2\37\5\3\2\2"+
		"\2 \"\7\b\2\2! \3\2\2\2!\"\3\2\2\2\"#\3\2\2\2#$\5\b\5\2$\7\3\2\2\2%\'"+
		"\5\n\6\2&%\3\2\2\2\'(\3\2\2\2(&\3\2\2\2()\3\2\2\2)\t\3\2\2\2*,\7\t\2\2"+
		"+-\7\b\2\2,+\3\2\2\2,-\3\2\2\2-9\3\2\2\2.\60\7\3\2\2/\61\5\n\6\2\60/\3"+
		"\2\2\2\61\62\3\2\2\2\62\60\3\2\2\2\62\63\3\2\2\2\63\64\3\2\2\2\64\66\7"+
		"\4\2\2\65\67\7\b\2\2\66\65\3\2\2\2\66\67\3\2\2\2\679\3\2\2\28*\3\2\2\2"+
		"8.\3\2\2\29\13\3\2\2\2\n\24\33!(,\62\668";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}