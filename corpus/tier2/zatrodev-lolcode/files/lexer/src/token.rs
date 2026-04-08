use std::fmt;
use std::fmt::Formatter;

#[derive(Clone, Debug, PartialOrd, PartialEq)]
pub struct Token {
    pub kind: TokenKind,
    pub span: Span,
}

#[derive(Clone, Debug, Eq, Hash, Ord, PartialOrd, PartialEq)]
pub struct Span {
    pub start: usize,
    pub end: usize,
}

impl fmt::Display for Token {
    fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
        write!(
            f,
            "start: {}, end: {}, kind: {}",
            self.span.start, self.span.end, self.kind
        )
    }
}

#[derive(Clone, Debug, PartialOrd, PartialEq)]
pub enum TokenKind {
    ILLEGAL,
    EOF,

    // Identifiers + literals
    IDENTIFIER { name: String },
    YARN(String),
    NUMBR(i64),
    NUMBAR(f64),
    TROOF(bool),
    TYPENUMBR,
    TYPENUMBAR,
    TYPEYARN,
    TYPETROOF,
    NOOB,
    IT,

    // Operators
    SUM,
    DIFF,
    PRODUKT,
    QUOSHUNT,
    MOD,
    BIGGR,
    SMALLR,
    BothOf,
    EitherOf,
    WonOf,
    NOT,
    AllOf,
    AnyOf,
    BothSaem, // ==
    DIFFRINT, // !=
    SMOOSH,   // String concatenation
    PLUS,     // +
    MAEK,
    IsNowA,

    // Delimiters
    A,
    AN,
    MKAY, // Terminator for variable arguments
    BTW,  // Comment start
    OBTW, // Multi-line comment start
    TLDR, // Multi-line comment end

    // Structure keywords
    HAI,
    KTHXBYE,
    WAZZUP,
    BUHBYE,
    IHasA,
    ITZ,   // Assignment
    R,     // Re-assignment
    ORly,  // If statement start
    YaRly, // Then clause
    Mebbe, // Else-if clause
    NoWai, // Else clause
    OIC,   // End of block
    WTF,   // Switch statement
    OMG,
    OMGWTF,
    Yr,
    ImInYr,
    ImOuttaYr,
    TIL,
    WILE,
    UPPIN,
    NERFIN,
    VISIBLE,
    GIMMEH,
    GTFO,
    FoundYr,
    HowIzI,
    IIz,
    IfUSaySo,
}

impl fmt::Display for TokenKind {
    fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
        match self {
            TokenKind::IDENTIFIER { name } => write!(f, "IDENTIFIER({})", name),
            TokenKind::YARN(s) => write!(f, "\"{}\"", s),
            TokenKind::NUMBR(i) => write!(f, "NUMBR({})", i),
            TokenKind::NUMBAR(d) => write!(f, "NUMBAR({})", d),
            TokenKind::TROOF(true) => write!(f, "WIN"),
            TokenKind::TROOF(false) => write!(f, "FAIL"),
            TokenKind::NOOB => write!(f, "NOOB"),

            // Handle other variants with debug fallback
            _ => write!(f, "{:?}", self),
        }
    }
}

impl TokenKind {
    pub fn classification(&self) -> Classification {
        match self {
            // PROGRAM STRUCTURE
            TokenKind::HAI | TokenKind::KTHXBYE => Classification::CodeDelimiter,

            // DECLARATION BLOCK
            TokenKind::WAZZUP | TokenKind::BUHBYE => Classification::VarDeclarationDelimiter,

            // VARIABLES
            TokenKind::IHasA => Classification::VariableDeclaration,
            TokenKind::ITZ => Classification::VariableAssignment,
            TokenKind::R => Classification::VariableReassignment,
            TokenKind::IDENTIFIER { .. } => Classification::Identifier,
            TokenKind::IT => Classification::ImplicitVariable,

            // LITERALS
            TokenKind::NUMBR(_)
            | TokenKind::NUMBAR(_)
            | TokenKind::YARN(_)
            | TokenKind::TROOF(_)
            | TokenKind::NOOB => Classification::Literal,

            // TYPE SYSTEM
            TokenKind::TYPENUMBR => Classification::IntegerType,
            TokenKind::TYPENUMBAR => Classification::FloatType,
            TokenKind::TYPEYARN => Classification::StringType,
            TokenKind::TYPETROOF => Classification::BooleanType,
            TokenKind::MAEK => Classification::TypeCasting,
            TokenKind::IsNowA => Classification::TypeConversion,

            // OPERATORS
            TokenKind::SUM
            | TokenKind::DIFF
            | TokenKind::PRODUKT
            | TokenKind::QUOSHUNT
            | TokenKind::MOD => Classification::ArithmeticOperator,

            TokenKind::BothSaem | TokenKind::DIFFRINT | TokenKind::BIGGR | TokenKind::SMALLR => {
                Classification::ComparisonOperator
            }

            TokenKind::BothOf
            | TokenKind::EitherOf
            | TokenKind::WonOf
            | TokenKind::NOT
            | TokenKind::AllOf
            | TokenKind::AnyOf => Classification::LogicalOperator,

            TokenKind::SMOOSH | TokenKind::PLUS => Classification::StringConcatenation,

            // INPUT/OUTPUT
            TokenKind::VISIBLE => Classification::OutputKeyword,
            TokenKind::GIMMEH => Classification::InputKeyword,

            // CONDITIONAL STRUCTURE
            TokenKind::ORly => Classification::ConditionalStart,
            TokenKind::YaRly => Classification::ConditionalThen,
            TokenKind::Mebbe => Classification::ConditionalElseIf,
            TokenKind::NoWai => Classification::ConditionalElse,

            // SWITCH STRUCTURE
            TokenKind::WTF => Classification::SwitchStart,
            TokenKind::OMG => Classification::SwitchCase,
            TokenKind::OMGWTF => Classification::SwitchDefault,

            // BLOCK TERMINATOR
            TokenKind::OIC => Classification::BlockEnd,

            // LOOP STRUCTURE
            TokenKind::ImInYr | TokenKind::ImOuttaYr => Classification::LoopDelimiter,
            TokenKind::Yr => Classification::LoopLabel,
            TokenKind::TIL => Classification::LoopUntil,
            TokenKind::WILE => Classification::LoopWhile,
            TokenKind::UPPIN => Classification::LoopIncrement,
            TokenKind::NERFIN => Classification::LoopDecrement,

            // FUNCTION STRUCTURE
            TokenKind::HowIzI => Classification::FunctionDeclaration,
            TokenKind::IIz => Classification::FunctionCall,
            TokenKind::IfUSaySo => Classification::FunctionEnd,
            TokenKind::FoundYr => Classification::FunctionReturn,

            // CONTROL FLOW
            TokenKind::GTFO => Classification::BreakStatement,

            // DELIMITERS
            TokenKind::A | TokenKind::AN => Classification::ArgumentDelimiter,
            TokenKind::MKAY => Classification::ArgumentTerminator,

            // SPECIAL
            TokenKind::ILLEGAL => Classification::IllegalToken,
            TokenKind::EOF => Classification::EndOfFile,

            // Comments
            TokenKind::BTW | TokenKind::OBTW | TokenKind::TLDR => Classification::Comment,
        }
    }
}

#[derive(Clone, Copy, Debug, PartialOrd, PartialEq)]
pub enum Classification {
    // PROGRAM STRUCTURE
    CodeDelimiter, // HAI, KTHXBYE

    // DECLARATION BLOCK
    VarDeclarationDelimiter, // WAZZUP, BUHBYE

    // VARIABLES
    VariableDeclaration,  // I HAS A
    VariableAssignment,   // ITZ
    VariableReassignment, // R
    Identifier,           // Identifier names
    ImplicitVariable,

    // LITERALS
    Literal,

    // TYPE SYSTEM
    IntegerType,    // NUMBR
    FloatType,      // NUMBAR
    StringType,     // YARN
    BooleanType,    // TROOF
    TypeCasting,    // MAEK
    TypeConversion, // IS NOW A

    // OPERATORS
    ArithmeticOperator,  // SUM OF, DIFF OF, PRODUKT OF, QUOSHUNT OF, MOD OF,
    ComparisonOperator,  // BOTH SAEM, DIFFRINT, BIGGR OF, SMALLR OF
    LogicalOperator,     // BOTH OF, EITHER OF, WON OF, ALL OF, ANY OF, NOT
    StringConcatenation, // SMOOSH

    // INPUT/OUTPUT
    OutputKeyword, // VISIBLE
    InputKeyword,  // GIMMEH

    // CONDITIONAL STRUCTURE
    ConditionalStart,  // O RLY?
    ConditionalThen,   // YA RLY
    ConditionalElseIf, // MEBBE
    ConditionalElse,   // NO WAI

    // SWITCH STRUCTURE
    SwitchStart,   // WTF?
    SwitchCase,    // OMG
    SwitchDefault, // OMGWTF

    // BLOCK TERMINATOR
    BlockEnd, // OIC (ends conditionals, switches, etc.)

    // LOOP STRUCTURE
    LoopDelimiter, // IM IN YR, IM OUTTA YR
    LoopLabel,     // YR
    LoopUntil,     // TIL
    LoopWhile,     // WILE
    LoopIncrement, // UPPIN
    LoopDecrement, // NERFIN

    // FUNCTION STRUCTURE
    FunctionDeclaration, // HOW IZ I
    FunctionCall,        // I IZ
    FunctionEnd,         // IF U SAY SO
    FunctionReturn,      // FOUND YR

    // CONTROL FLOW
    BreakStatement, // GTFO

    // DELIMITERS
    ArgumentDelimiter,  // A, AN
    ArgumentTerminator, // MKAY

    // COMMENTS
    Comment, // BTW, OBTW, TLDR

    // SPECIAL
    IllegalToken, // Unrecognized token
    EndOfFile,    // EOF
}

impl fmt::Display for Classification {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            // PROGRAM STRUCTURE
            Classification::CodeDelimiter => write!(f, "Code Delimiter"),

            // DECLARATION BLOCK
            Classification::VarDeclarationDelimiter => write!(f, "Variable Declaration Delimiter"),

            // VARIABLES
            Classification::VariableDeclaration => write!(f, "Variable Declaration"),
            Classification::VariableAssignment => write!(f, "Variable Assignment"),
            Classification::VariableReassignment => write!(f, "Variable Reassignment"),
            Classification::Identifier => write!(f, "Identifier"),
            Classification::ImplicitVariable => write!(f, "Implicit Variable"),

            // LITERALS
            Classification::Literal => write!(f, "Literal"),

            // TYPE SYSTEM
            Classification::IntegerType => write!(f, "Integer Type"),
            Classification::FloatType => write!(f, "Float Type"),
            Classification::StringType => write!(f, "String Type"),
            Classification::BooleanType => write!(f, "Boolean Type"),
            Classification::TypeCasting => write!(f, "Type Casting"),
            Classification::TypeConversion => write!(f, "Type Conversion"),

            // OPERATORS
            Classification::ArithmeticOperator => write!(f, "Arithmetic Operator"),
            Classification::ComparisonOperator => write!(f, "Comparison Operator"),
            Classification::LogicalOperator => write!(f, "Logical Operator"),
            Classification::StringConcatenation => write!(f, "String Concatenation"),

            // INPUT/OUTPUT
            Classification::OutputKeyword => write!(f, "Output Keyword"),
            Classification::InputKeyword => write!(f, "Input Keyword"),

            // CONDITIONAL STRUCTURE
            Classification::ConditionalStart => write!(f, "Conditional Start"),
            Classification::ConditionalThen => write!(f, "Conditional Then"),
            Classification::ConditionalElseIf => write!(f, "Conditional Else-If"),
            Classification::ConditionalElse => write!(f, "Conditional Else"),

            // SWITCH STRUCTURE
            Classification::SwitchStart => write!(f, "Switch Start"),
            Classification::SwitchCase => write!(f, "Switch Case"),
            Classification::SwitchDefault => write!(f, "Switch Default"),

            // BLOCK TERMINATOR
            Classification::BlockEnd => write!(f, "Block End"),

            // LOOP STRUCTURE
            Classification::LoopDelimiter => write!(f, "Loop Delimiter"),
            Classification::LoopLabel => write!(f, "Loop Label"),
            Classification::LoopUntil => write!(f, "Loop Until"),
            Classification::LoopWhile => write!(f, "Loop While"),
            Classification::LoopIncrement => write!(f, "Loop Increment"),
            Classification::LoopDecrement => write!(f, "Loop Decrement"),

            // FUNCTION STRUCTURE
            Classification::FunctionDeclaration => write!(f, "Function Declaration"),
            Classification::FunctionCall => write!(f, "Function Call"),
            Classification::FunctionEnd => write!(f, "Function End"),
            Classification::FunctionReturn => write!(f, "Function Return"),

            // CONTROL FLOW
            Classification::BreakStatement => write!(f, "Break Statement"),

            // DELIMITERS
            Classification::ArgumentDelimiter => write!(f, "Argument Delimiter"),
            Classification::ArgumentTerminator => write!(f, "Argument Terminator"),

            // COMMENTS
            Classification::Comment => write!(f, "Comment"),
            // SPECIAL
            Classification::IllegalToken => write!(f, "Illegal Token"),
            Classification::EndOfFile => write!(f, "End of File"),
        }
    }
}
