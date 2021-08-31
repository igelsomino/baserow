// Generated from BaserowFormula.g4 by ANTLR 4.8
// jshint ignore: start
var antlr4 = require('antlr4/index');
var BaserowFormulaListener = require('./BaserowFormulaListener').BaserowFormulaListener;
var BaserowFormulaVisitor = require('./BaserowFormulaVisitor').BaserowFormulaVisitor;

var grammarFileName = "BaserowFormula.g4";


var serializedATN = ["\u0003\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964",
    "\u0003Q.\u0004\u0002\t\u0002\u0004\u0003\t\u0003\u0004\u0004\t\u0004",
    "\u0004\u0005\t\u0005\u0003\u0002\u0003\u0002\u0003\u0002\u0003\u0003",
    "\u0003\u0003\u0003\u0003\u0003\u0003\u0003\u0003\u0003\u0003\u0003\u0003",
    "\u0003\u0003\u0003\u0003\u0007\u0003\u0017\n\u0003\f\u0003\u000e\u0003",
    "\u001a\u000b\u0003\u0005\u0003\u001c\n\u0003\u0003\u0003\u0003\u0003",
    "\u0005\u0003 \n\u0003\u0003\u0003\u0003\u0003\u0003\u0003\u0007\u0003",
    "%\n\u0003\f\u0003\u000e\u0003(\u000b\u0003\u0003\u0004\u0003\u0004\u0003",
    "\u0005\u0003\u0005\u0003\u0005\u0002\u0003\u0004\u0006\u0002\u0004\u0006",
    "\b\u0002\u0004\u0004\u0002;;AA\u0003\u0002\u0019\u001a\u0002/\u0002",
    "\n\u0003\u0002\u0002\u0002\u0004\u001f\u0003\u0002\u0002\u0002\u0006",
    ")\u0003\u0002\u0002\u0002\b+\u0003\u0002\u0002\u0002\n\u000b\u0005\u0004",
    "\u0003\u0002\u000b\f\u0007\u0002\u0002\u0003\f\u0003\u0003\u0002\u0002",
    "\u0002\r\u000e\b\u0003\u0001\u0002\u000e \u0007\u0017\u0002\u0002\u000f",
    " \u0007\u0018\u0002\u0002\u0010 \u0007\u0014\u0002\u0002\u0011\u0012",
    "\u0005\u0006\u0004\u0002\u0012\u001b\u0007\r\u0002\u0002\u0013\u0018",
    "\u0005\u0004\u0003\u0002\u0014\u0015\u0007\u0007\u0002\u0002\u0015\u0017",
    "\u0005\u0004\u0003\u0002\u0016\u0014\u0003\u0002\u0002\u0002\u0017\u001a",
    "\u0003\u0002\u0002\u0002\u0018\u0016\u0003\u0002\u0002\u0002\u0018\u0019",
    "\u0003\u0002\u0002\u0002\u0019\u001c\u0003\u0002\u0002\u0002\u001a\u0018",
    "\u0003\u0002\u0002\u0002\u001b\u0013\u0003\u0002\u0002\u0002\u001b\u001c",
    "\u0003\u0002\u0002\u0002\u001c\u001d\u0003\u0002\u0002\u0002\u001d\u001e",
    "\u0007\u000e\u0002\u0002\u001e \u0003\u0002\u0002\u0002\u001f\r\u0003",
    "\u0002\u0002\u0002\u001f\u000f\u0003\u0002\u0002\u0002\u001f\u0010\u0003",
    "\u0002\u0002\u0002\u001f\u0011\u0003\u0002\u0002\u0002 &\u0003\u0002",
    "\u0002\u0002!\"\f\u0004\u0002\u0002\"#\t\u0002\u0002\u0002#%\u0005\u0004",
    "\u0003\u0005$!\u0003\u0002\u0002\u0002%(\u0003\u0002\u0002\u0002&$\u0003",
    "\u0002\u0002\u0002&\'\u0003\u0002\u0002\u0002\'\u0005\u0003\u0002\u0002",
    "\u0002(&\u0003\u0002\u0002\u0002)*\u0005\b\u0005\u0002*\u0007\u0003",
    "\u0002\u0002\u0002+,\t\u0003\u0002\u0002,\t\u0003\u0002\u0002\u0002",
    "\u0006\u0018\u001b\u001f&"].join("");


var atn = new antlr4.atn.ATNDeserializer().deserialize(serializedATN);

var decisionsToDFA = atn.decisionToState.map( function(ds, index) { return new antlr4.dfa.DFA(ds, index); });

var sharedContextCache = new antlr4.PredictionContextCache();

var literalNames = [ null, null, null, null, null, "','", "':'", "'::'", 
                     "'$'", "'$$'", "'*'", "'('", "')'", "'['", "']'", null, 
                     null, null, null, null, "'.'", null, null, null, null, 
                     "'&'", "'&&'", "'&<'", "'@@'", "'@>'", "'@'", "'!'", 
                     "'!!'", "'!='", "'^'", "'='", "'=>'", "'>'", "'>='", 
                     "'>>'", "'#'", "'#='", "'#>'", "'#>>'", "'##'", "'->'", 
                     "'->>'", "'-|-'", "'<'", "'<='", "'<@'", "'<^'", "'<>'", 
                     "'<->'", "'<<'", "'<<='", "'<?>'", "'-'", "'%'", "'|'", 
                     "'||'", "'||/'", "'|/'", "'+'", "'?'", "'?&'", "'?#'", 
                     "'?-'", "'?|'", "'/'", "'~'", "'~='", "'~>=~'", "'~>~'", 
                     "'~<=~'", "'~<~'", "'~*'", "'~~'", "';'" ];

var symbolicNames = [ null, "WHITESPACE", "BLOCK_COMMENT", "LINE_COMMENT", 
                      "IF", "COMMA", "COLON", "COLON_COLON", "DOLLAR", "DOLLAR_DOLLAR", 
                      "STAR", "OPEN_PAREN", "CLOSE_PAREN", "OPEN_BRACKET", 
                      "CLOSE_BRACKET", "BIT_STRING", "REGEX_STRING", "NUMERIC_LITERAL", 
                      "INTEGER_LITERAL", "HEX_INTEGER_LITERAL", "DOT", "SINGLEQ_STRING_LITERAL", 
                      "DOUBLEQ_STRING_LITERAL", "IDENTIFIER", "IDENTIFIER_UNICODE", 
                      "AMP", "AMP_AMP", "AMP_LT", "AT_AT", "AT_GT", "AT_SIGN", 
                      "BANG", "BANG_BANG", "BANG_EQUAL", "CARET", "EQUAL", 
                      "EQUAL_GT", "GT", "GTE", "GT_GT", "HASH", "HASH_EQ", 
                      "HASH_GT", "HASH_GT_GT", "HASH_HASH", "HYPHEN_GT", 
                      "HYPHEN_GT_GT", "HYPHEN_PIPE_HYPHEN", "LT", "LTE", 
                      "LT_AT", "LT_CARET", "LT_GT", "LT_HYPHEN_GT", "LT_LT", 
                      "LT_LT_EQ", "LT_QMARK_GT", "MINUS", "PERCENT", "PIPE", 
                      "PIPE_PIPE", "PIPE_PIPE_SLASH", "PIPE_SLASH", "PLUS", 
                      "QMARK", "QMARK_AMP", "QMARK_HASH", "QMARK_HYPHEN", 
                      "QMARK_PIPE", "SLASH", "TIL", "TIL_EQ", "TIL_GTE_TIL", 
                      "TIL_GT_TIL", "TIL_LTE_TIL", "TIL_LT_TIL", "TIL_STAR", 
                      "TIL_TIL", "SEMI", "ErrorCharacter" ];

var ruleNames =  [ "root", "expr", "func_name", "identifier" ];

function BaserowFormula (input) {
	antlr4.Parser.call(this, input);
    this._interp = new antlr4.atn.ParserATNSimulator(this, atn, decisionsToDFA, sharedContextCache);
    this.ruleNames = ruleNames;
    this.literalNames = literalNames;
    this.symbolicNames = symbolicNames;
    return this;
}

BaserowFormula.prototype = Object.create(antlr4.Parser.prototype);
BaserowFormula.prototype.constructor = BaserowFormula;

Object.defineProperty(BaserowFormula.prototype, "atn", {
	get : function() {
		return atn;
	}
});

BaserowFormula.EOF = antlr4.Token.EOF;
BaserowFormula.WHITESPACE = 1;
BaserowFormula.BLOCK_COMMENT = 2;
BaserowFormula.LINE_COMMENT = 3;
BaserowFormula.IF = 4;
BaserowFormula.COMMA = 5;
BaserowFormula.COLON = 6;
BaserowFormula.COLON_COLON = 7;
BaserowFormula.DOLLAR = 8;
BaserowFormula.DOLLAR_DOLLAR = 9;
BaserowFormula.STAR = 10;
BaserowFormula.OPEN_PAREN = 11;
BaserowFormula.CLOSE_PAREN = 12;
BaserowFormula.OPEN_BRACKET = 13;
BaserowFormula.CLOSE_BRACKET = 14;
BaserowFormula.BIT_STRING = 15;
BaserowFormula.REGEX_STRING = 16;
BaserowFormula.NUMERIC_LITERAL = 17;
BaserowFormula.INTEGER_LITERAL = 18;
BaserowFormula.HEX_INTEGER_LITERAL = 19;
BaserowFormula.DOT = 20;
BaserowFormula.SINGLEQ_STRING_LITERAL = 21;
BaserowFormula.DOUBLEQ_STRING_LITERAL = 22;
BaserowFormula.IDENTIFIER = 23;
BaserowFormula.IDENTIFIER_UNICODE = 24;
BaserowFormula.AMP = 25;
BaserowFormula.AMP_AMP = 26;
BaserowFormula.AMP_LT = 27;
BaserowFormula.AT_AT = 28;
BaserowFormula.AT_GT = 29;
BaserowFormula.AT_SIGN = 30;
BaserowFormula.BANG = 31;
BaserowFormula.BANG_BANG = 32;
BaserowFormula.BANG_EQUAL = 33;
BaserowFormula.CARET = 34;
BaserowFormula.EQUAL = 35;
BaserowFormula.EQUAL_GT = 36;
BaserowFormula.GT = 37;
BaserowFormula.GTE = 38;
BaserowFormula.GT_GT = 39;
BaserowFormula.HASH = 40;
BaserowFormula.HASH_EQ = 41;
BaserowFormula.HASH_GT = 42;
BaserowFormula.HASH_GT_GT = 43;
BaserowFormula.HASH_HASH = 44;
BaserowFormula.HYPHEN_GT = 45;
BaserowFormula.HYPHEN_GT_GT = 46;
BaserowFormula.HYPHEN_PIPE_HYPHEN = 47;
BaserowFormula.LT = 48;
BaserowFormula.LTE = 49;
BaserowFormula.LT_AT = 50;
BaserowFormula.LT_CARET = 51;
BaserowFormula.LT_GT = 52;
BaserowFormula.LT_HYPHEN_GT = 53;
BaserowFormula.LT_LT = 54;
BaserowFormula.LT_LT_EQ = 55;
BaserowFormula.LT_QMARK_GT = 56;
BaserowFormula.MINUS = 57;
BaserowFormula.PERCENT = 58;
BaserowFormula.PIPE = 59;
BaserowFormula.PIPE_PIPE = 60;
BaserowFormula.PIPE_PIPE_SLASH = 61;
BaserowFormula.PIPE_SLASH = 62;
BaserowFormula.PLUS = 63;
BaserowFormula.QMARK = 64;
BaserowFormula.QMARK_AMP = 65;
BaserowFormula.QMARK_HASH = 66;
BaserowFormula.QMARK_HYPHEN = 67;
BaserowFormula.QMARK_PIPE = 68;
BaserowFormula.SLASH = 69;
BaserowFormula.TIL = 70;
BaserowFormula.TIL_EQ = 71;
BaserowFormula.TIL_GTE_TIL = 72;
BaserowFormula.TIL_GT_TIL = 73;
BaserowFormula.TIL_LTE_TIL = 74;
BaserowFormula.TIL_LT_TIL = 75;
BaserowFormula.TIL_STAR = 76;
BaserowFormula.TIL_TIL = 77;
BaserowFormula.SEMI = 78;
BaserowFormula.ErrorCharacter = 79;

BaserowFormula.RULE_root = 0;
BaserowFormula.RULE_expr = 1;
BaserowFormula.RULE_func_name = 2;
BaserowFormula.RULE_identifier = 3;


function RootContext(parser, parent, invokingState) {
	if(parent===undefined) {
	    parent = null;
	}
	if(invokingState===undefined || invokingState===null) {
		invokingState = -1;
	}
	antlr4.ParserRuleContext.call(this, parent, invokingState);
    this.parser = parser;
    this.ruleIndex = BaserowFormula.RULE_root;
    return this;
}

RootContext.prototype = Object.create(antlr4.ParserRuleContext.prototype);
RootContext.prototype.constructor = RootContext;

RootContext.prototype.expr = function() {
    return this.getTypedRuleContext(ExprContext,0);
};

RootContext.prototype.EOF = function() {
    return this.getToken(BaserowFormula.EOF, 0);
};

RootContext.prototype.enterRule = function(listener) {
    if(listener instanceof BaserowFormulaListener ) {
        listener.enterRoot(this);
	}
};

RootContext.prototype.exitRule = function(listener) {
    if(listener instanceof BaserowFormulaListener ) {
        listener.exitRoot(this);
	}
};

RootContext.prototype.accept = function(visitor) {
    if ( visitor instanceof BaserowFormulaVisitor ) {
        return visitor.visitRoot(this);
    } else {
        return visitor.visitChildren(this);
    }
};




BaserowFormula.RootContext = RootContext;

BaserowFormula.prototype.root = function() {

    var localctx = new RootContext(this, this._ctx, this.state);
    this.enterRule(localctx, 0, BaserowFormula.RULE_root);
    try {
        this.enterOuterAlt(localctx, 1);
        this.state = 8;
        this.expr(0);
        this.state = 9;
        this.match(BaserowFormula.EOF);
    } catch (re) {
    	if(re instanceof antlr4.error.RecognitionException) {
	        localctx.exception = re;
	        this._errHandler.reportError(this, re);
	        this._errHandler.recover(this, re);
	    } else {
	    	throw re;
	    }
    } finally {
        this.exitRule();
    }
    return localctx;
};


function ExprContext(parser, parent, invokingState) {
	if(parent===undefined) {
	    parent = null;
	}
	if(invokingState===undefined || invokingState===null) {
		invokingState = -1;
	}
	antlr4.ParserRuleContext.call(this, parent, invokingState);
    this.parser = parser;
    this.ruleIndex = BaserowFormula.RULE_expr;
    return this;
}

ExprContext.prototype = Object.create(antlr4.ParserRuleContext.prototype);
ExprContext.prototype.constructor = ExprContext;


 
ExprContext.prototype.copyFrom = function(ctx) {
    antlr4.ParserRuleContext.prototype.copyFrom.call(this, ctx);
};

function StringLiteralContext(parser, ctx) {
	ExprContext.call(this, parser);
    ExprContext.prototype.copyFrom.call(this, ctx);
    return this;
}

StringLiteralContext.prototype = Object.create(ExprContext.prototype);
StringLiteralContext.prototype.constructor = StringLiteralContext;

BaserowFormula.StringLiteralContext = StringLiteralContext;

StringLiteralContext.prototype.SINGLEQ_STRING_LITERAL = function() {
    return this.getToken(BaserowFormula.SINGLEQ_STRING_LITERAL, 0);
};

StringLiteralContext.prototype.DOUBLEQ_STRING_LITERAL = function() {
    return this.getToken(BaserowFormula.DOUBLEQ_STRING_LITERAL, 0);
};
StringLiteralContext.prototype.enterRule = function(listener) {
    if(listener instanceof BaserowFormulaListener ) {
        listener.enterStringLiteral(this);
	}
};

StringLiteralContext.prototype.exitRule = function(listener) {
    if(listener instanceof BaserowFormulaListener ) {
        listener.exitStringLiteral(this);
	}
};

StringLiteralContext.prototype.accept = function(visitor) {
    if ( visitor instanceof BaserowFormulaVisitor ) {
        return visitor.visitStringLiteral(this);
    } else {
        return visitor.visitChildren(this);
    }
};


function FunctionCallContext(parser, ctx) {
	ExprContext.call(this, parser);
    ExprContext.prototype.copyFrom.call(this, ctx);
    return this;
}

FunctionCallContext.prototype = Object.create(ExprContext.prototype);
FunctionCallContext.prototype.constructor = FunctionCallContext;

BaserowFormula.FunctionCallContext = FunctionCallContext;

FunctionCallContext.prototype.func_name = function() {
    return this.getTypedRuleContext(Func_nameContext,0);
};

FunctionCallContext.prototype.OPEN_PAREN = function() {
    return this.getToken(BaserowFormula.OPEN_PAREN, 0);
};

FunctionCallContext.prototype.CLOSE_PAREN = function() {
    return this.getToken(BaserowFormula.CLOSE_PAREN, 0);
};

FunctionCallContext.prototype.expr = function(i) {
    if(i===undefined) {
        i = null;
    }
    if(i===null) {
        return this.getTypedRuleContexts(ExprContext);
    } else {
        return this.getTypedRuleContext(ExprContext,i);
    }
};

FunctionCallContext.prototype.COMMA = function(i) {
	if(i===undefined) {
		i = null;
	}
    if(i===null) {
        return this.getTokens(BaserowFormula.COMMA);
    } else {
        return this.getToken(BaserowFormula.COMMA, i);
    }
};

FunctionCallContext.prototype.enterRule = function(listener) {
    if(listener instanceof BaserowFormulaListener ) {
        listener.enterFunctionCall(this);
	}
};

FunctionCallContext.prototype.exitRule = function(listener) {
    if(listener instanceof BaserowFormulaListener ) {
        listener.exitFunctionCall(this);
	}
};

FunctionCallContext.prototype.accept = function(visitor) {
    if ( visitor instanceof BaserowFormulaVisitor ) {
        return visitor.visitFunctionCall(this);
    } else {
        return visitor.visitChildren(this);
    }
};


function IntegerLiteralContext(parser, ctx) {
	ExprContext.call(this, parser);
    ExprContext.prototype.copyFrom.call(this, ctx);
    return this;
}

IntegerLiteralContext.prototype = Object.create(ExprContext.prototype);
IntegerLiteralContext.prototype.constructor = IntegerLiteralContext;

BaserowFormula.IntegerLiteralContext = IntegerLiteralContext;

IntegerLiteralContext.prototype.INTEGER_LITERAL = function() {
    return this.getToken(BaserowFormula.INTEGER_LITERAL, 0);
};
IntegerLiteralContext.prototype.enterRule = function(listener) {
    if(listener instanceof BaserowFormulaListener ) {
        listener.enterIntegerLiteral(this);
	}
};

IntegerLiteralContext.prototype.exitRule = function(listener) {
    if(listener instanceof BaserowFormulaListener ) {
        listener.exitIntegerLiteral(this);
	}
};

IntegerLiteralContext.prototype.accept = function(visitor) {
    if ( visitor instanceof BaserowFormulaVisitor ) {
        return visitor.visitIntegerLiteral(this);
    } else {
        return visitor.visitChildren(this);
    }
};


function BinaryOpContext(parser, ctx) {
	ExprContext.call(this, parser);
    this.op = null; // Token;
    ExprContext.prototype.copyFrom.call(this, ctx);
    return this;
}

BinaryOpContext.prototype = Object.create(ExprContext.prototype);
BinaryOpContext.prototype.constructor = BinaryOpContext;

BaserowFormula.BinaryOpContext = BinaryOpContext;

BinaryOpContext.prototype.expr = function(i) {
    if(i===undefined) {
        i = null;
    }
    if(i===null) {
        return this.getTypedRuleContexts(ExprContext);
    } else {
        return this.getTypedRuleContext(ExprContext,i);
    }
};

BinaryOpContext.prototype.PLUS = function() {
    return this.getToken(BaserowFormula.PLUS, 0);
};

BinaryOpContext.prototype.MINUS = function() {
    return this.getToken(BaserowFormula.MINUS, 0);
};
BinaryOpContext.prototype.enterRule = function(listener) {
    if(listener instanceof BaserowFormulaListener ) {
        listener.enterBinaryOp(this);
	}
};

BinaryOpContext.prototype.exitRule = function(listener) {
    if(listener instanceof BaserowFormulaListener ) {
        listener.exitBinaryOp(this);
	}
};

BinaryOpContext.prototype.accept = function(visitor) {
    if ( visitor instanceof BaserowFormulaVisitor ) {
        return visitor.visitBinaryOp(this);
    } else {
        return visitor.visitChildren(this);
    }
};



BaserowFormula.prototype.expr = function(_p) {
	if(_p===undefined) {
	    _p = 0;
	}
    var _parentctx = this._ctx;
    var _parentState = this.state;
    var localctx = new ExprContext(this, this._ctx, _parentState);
    var _prevctx = localctx;
    var _startState = 2;
    this.enterRecursionRule(localctx, 2, BaserowFormula.RULE_expr, _p);
    var _la = 0; // Token type
    try {
        this.enterOuterAlt(localctx, 1);
        this.state = 29;
        this._errHandler.sync(this);
        switch(this._input.LA(1)) {
        case BaserowFormula.SINGLEQ_STRING_LITERAL:
            localctx = new StringLiteralContext(this, localctx);
            this._ctx = localctx;
            _prevctx = localctx;

            this.state = 12;
            this.match(BaserowFormula.SINGLEQ_STRING_LITERAL);
            break;
        case BaserowFormula.DOUBLEQ_STRING_LITERAL:
            localctx = new StringLiteralContext(this, localctx);
            this._ctx = localctx;
            _prevctx = localctx;
            this.state = 13;
            this.match(BaserowFormula.DOUBLEQ_STRING_LITERAL);
            break;
        case BaserowFormula.INTEGER_LITERAL:
            localctx = new IntegerLiteralContext(this, localctx);
            this._ctx = localctx;
            _prevctx = localctx;
            this.state = 14;
            this.match(BaserowFormula.INTEGER_LITERAL);
            break;
        case BaserowFormula.IDENTIFIER:
        case BaserowFormula.IDENTIFIER_UNICODE:
            localctx = new FunctionCallContext(this, localctx);
            this._ctx = localctx;
            _prevctx = localctx;
            this.state = 15;
            this.func_name();
            this.state = 16;
            this.match(BaserowFormula.OPEN_PAREN);
            this.state = 25;
            this._errHandler.sync(this);
            _la = this._input.LA(1);
            if((((_la) & ~0x1f) == 0 && ((1 << _la) & ((1 << BaserowFormula.INTEGER_LITERAL) | (1 << BaserowFormula.SINGLEQ_STRING_LITERAL) | (1 << BaserowFormula.DOUBLEQ_STRING_LITERAL) | (1 << BaserowFormula.IDENTIFIER) | (1 << BaserowFormula.IDENTIFIER_UNICODE))) !== 0)) {
                this.state = 17;
                this.expr(0);
                this.state = 22;
                this._errHandler.sync(this);
                _la = this._input.LA(1);
                while(_la===BaserowFormula.COMMA) {
                    this.state = 18;
                    this.match(BaserowFormula.COMMA);
                    this.state = 19;
                    this.expr(0);
                    this.state = 24;
                    this._errHandler.sync(this);
                    _la = this._input.LA(1);
                }
            }

            this.state = 27;
            this.match(BaserowFormula.CLOSE_PAREN);
            break;
        default:
            throw new antlr4.error.NoViableAltException(this);
        }
        this._ctx.stop = this._input.LT(-1);
        this.state = 36;
        this._errHandler.sync(this);
        var _alt = this._interp.adaptivePredict(this._input,3,this._ctx)
        while(_alt!=2 && _alt!=antlr4.atn.ATN.INVALID_ALT_NUMBER) {
            if(_alt===1) {
                if(this._parseListeners!==null) {
                    this.triggerExitRuleEvent();
                }
                _prevctx = localctx;
                localctx = new BinaryOpContext(this, new ExprContext(this, _parentctx, _parentState));
                this.pushNewRecursionContext(localctx, _startState, BaserowFormula.RULE_expr);
                this.state = 31;
                if (!( this.precpred(this._ctx, 2))) {
                    throw new antlr4.error.FailedPredicateException(this, "this.precpred(this._ctx, 2)");
                }
                this.state = 32;
                localctx.op = this._input.LT(1);
                _la = this._input.LA(1);
                if(!(_la===BaserowFormula.MINUS || _la===BaserowFormula.PLUS)) {
                    localctx.op = this._errHandler.recoverInline(this);
                }
                else {
                	this._errHandler.reportMatch(this);
                    this.consume();
                }
                this.state = 33;
                this.expr(3); 
            }
            this.state = 38;
            this._errHandler.sync(this);
            _alt = this._interp.adaptivePredict(this._input,3,this._ctx);
        }

    } catch( error) {
        if(error instanceof antlr4.error.RecognitionException) {
	        localctx.exception = error;
	        this._errHandler.reportError(this, error);
	        this._errHandler.recover(this, error);
	    } else {
	    	throw error;
	    }
    } finally {
        this.unrollRecursionContexts(_parentctx)
    }
    return localctx;
};


function Func_nameContext(parser, parent, invokingState) {
	if(parent===undefined) {
	    parent = null;
	}
	if(invokingState===undefined || invokingState===null) {
		invokingState = -1;
	}
	antlr4.ParserRuleContext.call(this, parent, invokingState);
    this.parser = parser;
    this.ruleIndex = BaserowFormula.RULE_func_name;
    return this;
}

Func_nameContext.prototype = Object.create(antlr4.ParserRuleContext.prototype);
Func_nameContext.prototype.constructor = Func_nameContext;

Func_nameContext.prototype.identifier = function() {
    return this.getTypedRuleContext(IdentifierContext,0);
};

Func_nameContext.prototype.enterRule = function(listener) {
    if(listener instanceof BaserowFormulaListener ) {
        listener.enterFunc_name(this);
	}
};

Func_nameContext.prototype.exitRule = function(listener) {
    if(listener instanceof BaserowFormulaListener ) {
        listener.exitFunc_name(this);
	}
};

Func_nameContext.prototype.accept = function(visitor) {
    if ( visitor instanceof BaserowFormulaVisitor ) {
        return visitor.visitFunc_name(this);
    } else {
        return visitor.visitChildren(this);
    }
};




BaserowFormula.Func_nameContext = Func_nameContext;

BaserowFormula.prototype.func_name = function() {

    var localctx = new Func_nameContext(this, this._ctx, this.state);
    this.enterRule(localctx, 4, BaserowFormula.RULE_func_name);
    try {
        this.enterOuterAlt(localctx, 1);
        this.state = 39;
        this.identifier();
    } catch (re) {
    	if(re instanceof antlr4.error.RecognitionException) {
	        localctx.exception = re;
	        this._errHandler.reportError(this, re);
	        this._errHandler.recover(this, re);
	    } else {
	    	throw re;
	    }
    } finally {
        this.exitRule();
    }
    return localctx;
};


function IdentifierContext(parser, parent, invokingState) {
	if(parent===undefined) {
	    parent = null;
	}
	if(invokingState===undefined || invokingState===null) {
		invokingState = -1;
	}
	antlr4.ParserRuleContext.call(this, parent, invokingState);
    this.parser = parser;
    this.ruleIndex = BaserowFormula.RULE_identifier;
    return this;
}

IdentifierContext.prototype = Object.create(antlr4.ParserRuleContext.prototype);
IdentifierContext.prototype.constructor = IdentifierContext;

IdentifierContext.prototype.IDENTIFIER = function() {
    return this.getToken(BaserowFormula.IDENTIFIER, 0);
};

IdentifierContext.prototype.IDENTIFIER_UNICODE = function() {
    return this.getToken(BaserowFormula.IDENTIFIER_UNICODE, 0);
};

IdentifierContext.prototype.enterRule = function(listener) {
    if(listener instanceof BaserowFormulaListener ) {
        listener.enterIdentifier(this);
	}
};

IdentifierContext.prototype.exitRule = function(listener) {
    if(listener instanceof BaserowFormulaListener ) {
        listener.exitIdentifier(this);
	}
};

IdentifierContext.prototype.accept = function(visitor) {
    if ( visitor instanceof BaserowFormulaVisitor ) {
        return visitor.visitIdentifier(this);
    } else {
        return visitor.visitChildren(this);
    }
};




BaserowFormula.IdentifierContext = IdentifierContext;

BaserowFormula.prototype.identifier = function() {

    var localctx = new IdentifierContext(this, this._ctx, this.state);
    this.enterRule(localctx, 6, BaserowFormula.RULE_identifier);
    var _la = 0; // Token type
    try {
        this.enterOuterAlt(localctx, 1);
        this.state = 41;
        _la = this._input.LA(1);
        if(!(_la===BaserowFormula.IDENTIFIER || _la===BaserowFormula.IDENTIFIER_UNICODE)) {
        this._errHandler.recoverInline(this);
        }
        else {
        	this._errHandler.reportMatch(this);
            this.consume();
        }
    } catch (re) {
    	if(re instanceof antlr4.error.RecognitionException) {
	        localctx.exception = re;
	        this._errHandler.reportError(this, re);
	        this._errHandler.recover(this, re);
	    } else {
	    	throw re;
	    }
    } finally {
        this.exitRule();
    }
    return localctx;
};


BaserowFormula.prototype.sempred = function(localctx, ruleIndex, predIndex) {
	switch(ruleIndex) {
	case 1:
			return this.expr_sempred(localctx, predIndex);
    default:
        throw "No predicate with index:" + ruleIndex;
   }
};

BaserowFormula.prototype.expr_sempred = function(localctx, predIndex) {
	switch(predIndex) {
		case 0:
			return this.precpred(this._ctx, 2);
		default:
			throw "No predicate with index:" + predIndex;
	}
};


exports.BaserowFormula = BaserowFormula;
