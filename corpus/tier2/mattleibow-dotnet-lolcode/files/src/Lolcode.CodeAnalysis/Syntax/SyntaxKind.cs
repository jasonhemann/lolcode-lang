namespace Lolcode.CodeAnalysis.Syntax;

/// <summary>
/// Enumerates all token and node kinds in the LOLCODE syntax.
/// </summary>
public enum SyntaxKind
{
    // --- Special tokens ---

    /// <summary>Bad/unexpected token.</summary>
    BadToken,

    /// <summary>End of file.</summary>
    EndOfFileToken,

    /// <summary>End of line (newline or comma).</summary>
    EndOfLineToken,

    /// <summary>Whitespace (spaces, tabs — not newlines).</summary>
    WhitespaceToken,

    /// <summary>Single-line comment (BTW ...).</summary>
    SingleLineCommentToken,

    /// <summary>Multi-line comment start (OBTW).</summary>
    MultiLineCommentToken,

    /// <summary>Line continuation (...).</summary>
    LineContinuationToken,

    // --- Literals ---

    /// <summary>Integer literal (NUMBR).</summary>
    NumbrLiteralToken,

    /// <summary>Floating point literal (NUMBAR).</summary>
    NumbarLiteralToken,

    /// <summary>String literal (YARN) delimited by double quotes.</summary>
    YarnLiteralToken,

    /// <summary>Identifier (variable or function name).</summary>
    IdentifierToken,

    // --- Keywords ---

    /// <summary>HAI — program start.</summary>
    HaiKeyword,

    /// <summary>KTHXBYE — program end.</summary>
    KthxbyeKeyword,

    /// <summary>I — used in "I HAS A", "I IZ".</summary>
    IKeyword,

    /// <summary>HAS — used in "I HAS A".</summary>
    HasKeyword,

    /// <summary>A — used in "I HAS A", "IS NOW A".</summary>
    AKeyword,

    /// <summary>ITZ — used in "I HAS A x ITZ value".</summary>
    ItzKeyword,

    /// <summary>R — assignment operator.</summary>
    RKeyword,

    /// <summary>AN — optional separator between arguments.</summary>
    AnKeyword,

    /// <summary>IT — implicit variable.</summary>
    ItKeyword,

    /// <summary>VISIBLE — print statement.</summary>
    VisibleKeyword,

    /// <summary>GIMMEH — input statement.</summary>
    GimmehKeyword,

    /// <summary>SUM — addition (SUM OF).</summary>
    SumKeyword,

    /// <summary>DIFF — subtraction (DIFF OF).</summary>
    DiffKeyword,

    /// <summary>PRODUKT — multiplication (PRODUKT OF).</summary>
    ProduktKeyword,

    /// <summary>QUOSHUNT — division (QUOSHUNT OF).</summary>
    QuoshuntKeyword,

    /// <summary>MOD — modulo (MOD OF).</summary>
    ModKeyword,

    /// <summary>BIGGR — maximum (BIGGR OF).</summary>
    BiggrKeyword,

    /// <summary>SMALLR — minimum (SMALLR OF).</summary>
    SmallrKeyword,

    /// <summary>OF — used in binary/variadic ops (SUM OF, ALL OF, etc.).</summary>
    OfKeyword,

    /// <summary>BOTH — used in "BOTH OF", "BOTH SAEM".</summary>
    BothKeyword,

    /// <summary>EITHER — used in "EITHER OF" (OR).</summary>
    EitherKeyword,

    /// <summary>WON — used in "WON OF" (XOR).</summary>
    WonKeyword,

    /// <summary>NOT — boolean NOT.</summary>
    NotKeyword,

    /// <summary>ALL — used in "ALL OF" (variadic AND).</summary>
    AllKeyword,

    /// <summary>ANY — used in "ANY OF" (variadic OR).</summary>
    AnyKeyword,

    /// <summary>MKAY — ends variadic operator.</summary>
    MkayKeyword,

    /// <summary>SAEM — used in "BOTH SAEM" (equality).</summary>
    SaemKeyword,

    /// <summary>DIFFRINT — inequality comparison.</summary>
    DiffrintKeyword,

    /// <summary>SMOOSH — string concatenation.</summary>
    SmooshKeyword,

    /// <summary>MAEK — explicit cast (MAEK x A type).</summary>
    MaekKeyword,

    /// <summary>IS — used in "IS NOW A" (in-place cast).</summary>
    IsKeyword,

    /// <summary>NOW — used in "IS NOW A".</summary>
    NowKeyword,

    /// <summary>O — used in "O RLY?".</summary>
    OKeyword,

    /// <summary>RLY? — used in "O RLY?".</summary>
    RlyKeyword,

    /// <summary>YA — used in "YA RLY".</summary>
    YaKeyword,

    /// <summary>NO — used in "NO WAI".</summary>
    NoKeyword,

    /// <summary>WAI — used in "NO WAI".</summary>
    WaiKeyword,

    /// <summary>MEBBE — else-if clause.</summary>
    MebbeKeyword,

    /// <summary>OIC — ends conditional or switch block.</summary>
    OicKeyword,

    /// <summary>WTF? — switch statement.</summary>
    WtfKeyword,

    /// <summary>OMG — switch case label.</summary>
    OmgKeyword,

    /// <summary>OMGWTF — default case in switch.</summary>
    OmgwtfKeyword,

    /// <summary>GTFO — break (loop/switch) or return NOOB (function).</summary>
    GtfoKeyword,

    /// <summary>IM — used in "IM IN YR" and "IM OUTTA YR".</summary>
    ImKeyword,

    /// <summary>IN — used in "IM IN YR".</summary>
    InKeyword,

    /// <summary>OUTTA — used in "IM OUTTA YR".</summary>
    OuttaKeyword,

    /// <summary>YR — used in function parameters, loop variable, etc.</summary>
    YrKeyword,

    /// <summary>TIL — loop until condition is true.</summary>
    TilKeyword,

    /// <summary>WILE — loop while condition is true.</summary>
    WileKeyword,

    /// <summary>UPPIN — increment loop operation.</summary>
    UppinKeyword,

    /// <summary>NERFIN — decrement loop operation.</summary>
    NerfinKeyword,

    /// <summary>HOW — used in "HOW IZ I" (function definition).</summary>
    HowKeyword,

    /// <summary>IZ — used in "HOW IZ I", "I IZ" (function call).</summary>
    IzKeyword,

    /// <summary>FOUND — used in "FOUND YR" (return value).</summary>
    FoundKeyword,

    /// <summary>IF — used in "IF U SAY SO".</summary>
    IfKeyword,

    /// <summary>U — used in "IF U SAY SO".</summary>
    UKeyword,

    /// <summary>SAY — used in "IF U SAY SO".</summary>
    SayKeyword,

    /// <summary>SO — used in "IF U SAY SO".</summary>
    SoKeyword,

    // --- Type keywords ---

    /// <summary>NOOB — untyped/null value.</summary>
    NoobKeyword,

    /// <summary>TROOF — boolean type.</summary>
    TroofKeyword,

    /// <summary>NUMBR — integer type.</summary>
    NumbrKeyword,

    /// <summary>NUMBAR — float type.</summary>
    NumbarKeyword,

    /// <summary>YARN — string type.</summary>
    YarnKeyword,

    // --- Boolean literals ---

    /// <summary>WIN — true.</summary>
    WinKeyword,

    /// <summary>FAIL — false.</summary>
    FailKeyword,

    // --- Punctuation ---

    /// <summary>Exclamation mark — used in VISIBLE to suppress newline.</summary>
    ExclamationToken,

    /// <summary>Question mark — part of RLY?, WTF?.</summary>
    QuestionToken,

    // --- Syntax node kinds ---

    /// <summary>Compilation unit (root).</summary>
    CompilationUnit,

    /// <summary>HAI ... KTHXBYE block.</summary>
    ProgramStatement,

    /// <summary>Variable declaration (I HAS A ...).</summary>
    VariableDeclarationStatement,

    /// <summary>Assignment statement (x R value).</summary>
    AssignmentStatement,

    /// <summary>VISIBLE statement.</summary>
    VisibleStatement,

    /// <summary>GIMMEH statement.</summary>
    GimmehStatement,

    /// <summary>Expression statement (bare expression, sets IT).</summary>
    ExpressionStatement,

    /// <summary>O RLY? conditional block.</summary>
    IfStatement,

    /// <summary>YA RLY clause.</summary>
    YaRlyClause,

    /// <summary>MEBBE clause.</summary>
    MebbeClause,

    /// <summary>NO WAI clause.</summary>
    NoWaiClause,

    /// <summary>WTF? switch block.</summary>
    SwitchStatement,

    /// <summary>OMG case clause.</summary>
    OmgClause,

    /// <summary>OMGWTF default clause.</summary>
    OmgwtfClause,

    /// <summary>IM IN YR loop.</summary>
    LoopStatement,

    /// <summary>GTFO statement.</summary>
    GtfoStatement,

    /// <summary>HOW IZ I function definition.</summary>
    FunctionDeclarationStatement,

    /// <summary>FOUND YR return statement.</summary>
    ReturnStatement,

    /// <summary>IS NOW A (in-place cast) statement.</summary>
    CastStatement,

    /// <summary>Block of statements.</summary>
    BlockStatement,

    // --- Expression node kinds ---

    /// <summary>Literal expression (NUMBR, NUMBAR, YARN, WIN, FAIL, NOOB).</summary>
    LiteralExpression,

    /// <summary>Variable reference expression.</summary>
    VariableExpression,

    /// <summary>Unary expression (NOT).</summary>
    UnaryExpression,

    /// <summary>Binary expression (SUM OF, DIFF OF, etc.).</summary>
    BinaryExpression,

    /// <summary>SMOOSH string concatenation expression.</summary>
    SmooshExpression,

    /// <summary>ALL OF variadic AND expression.</summary>
    AllOfExpression,

    /// <summary>ANY OF variadic OR expression.</summary>
    AnyOfExpression,

    /// <summary>BOTH SAEM comparison expression.</summary>
    ComparisonExpression,

    /// <summary>DIFFRINT comparison expression.</summary>
    DiffrintExpression,

    /// <summary>MAEK cast expression.</summary>
    CastExpression,

    /// <summary>I IZ function call expression.</summary>
    FunctionCallExpression,

    /// <summary>IT implicit variable expression.</summary>
    ItExpression,

    /// <summary>Interpolated string expression (YARN with :<var>).</summary>
    InterpolatedStringExpression,
}
