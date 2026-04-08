using Lolcode.CodeAnalysis.Text;

namespace Lolcode.CodeAnalysis.Syntax;

/// <summary>
/// Tokenizes LOLCODE 1.2 source text into a sequence of <see cref="SyntaxToken"/>s.
/// </summary>
internal sealed class Lexer
{
    private readonly SourceText _text;
    private readonly DiagnosticBag _diagnostics = new();
    private int _position;

    /// <summary>
    /// Gets the diagnostics produced during lexing.
    /// </summary>
    public IEnumerable<Diagnostic> Diagnostics => _diagnostics;

    /// <summary>
    /// Creates a new lexer for the given source text.
    /// </summary>
    public Lexer(SourceText text)
    {
        _text = text;
    }

    private char Current => Peek(0);
    private char Lookahead => Peek(1);

    private char Peek(int offset)
    {
        int index = _position + offset;
        if (index >= _text.Length)
            return '\0';
        return _text[index];
    }

    /// <summary>
    /// Tokenizes the entire source text.
    /// </summary>
    public IReadOnlyList<SyntaxToken> Tokenize()
    {
        var tokens = new List<SyntaxToken>();

        while (true)
        {
            var token = NextToken();
            if (token.Kind == SyntaxKind.WhitespaceToken ||
                token.Kind == SyntaxKind.SingleLineCommentToken ||
                token.Kind == SyntaxKind.MultiLineCommentToken ||
                token.Kind == SyntaxKind.LineContinuationToken)
            {
                // Skip trivia tokens
                continue;
            }

            tokens.Add(token);

            if (token.Kind == SyntaxKind.EndOfFileToken)
                break;
        }

        return tokens;
    }

    private SyntaxToken NextToken()
    {
        if (_position >= _text.Length)
            return new SyntaxToken(SyntaxKind.EndOfFileToken, _position, "\0");

        // Newline => EndOfLineToken
        if (Current == '\n')
        {
            int start = _position;
            _position++;
            return new SyntaxToken(SyntaxKind.EndOfLineToken, start, "\n");
        }

        if (Current == '\r')
        {
            int start = _position;
            if (Lookahead == '\n')
            {
                _position += 2;
                return new SyntaxToken(SyntaxKind.EndOfLineToken, start, "\r\n");
            }
            _position++;
            return new SyntaxToken(SyntaxKind.EndOfLineToken, start, "\r");
        }

        // Comma => line separator (equivalent to newline)
        if (Current == ',')
        {
            int start = _position;
            _position++;
            return new SyntaxToken(SyntaxKind.EndOfLineToken, start, ",");
        }

        // Whitespace (not newlines)
        if (Current == ' ' || Current == '\t')
        {
            return ReadWhitespace();
        }

        // Line continuation (three dots or Unicode ellipsis)
        if ((Current == '.' && Lookahead == '.' && Peek(2) == '.') || Current == '\u2026')
        {
            return ReadLineContinuation();
        }

        // Exclamation mark
        if (Current == '!')
        {
            int start = _position;
            _position++;
            return new SyntaxToken(SyntaxKind.ExclamationToken, start, "!");
        }

        // File-based app directives (#:sdk, #:package, etc.) and shebang (#!)
        // These appear at the top of .lol files for dotnet run --file support.
        // Skip the entire line as trivia.
        if (Current == '#' && (Lookahead == ':' || Lookahead == '!'))
        {
            return ReadHashDirective();
        }

        // String literal
        if (Current == '"')
        {
            return ReadString();
        }

        // Number literal (digits, or negative sign followed by digit)
        if (char.IsDigit(Current))
        {
            return ReadNumber();
        }

        if (Current == '-' && char.IsDigit(Lookahead))
        {
            return ReadNumber();
        }

        // Identifier or keyword
        if (char.IsLetter(Current) || Current == '_')
        {
            return ReadIdentifierOrKeyword();
        }

        // Unknown character
        var span = new TextSpan(_position, 1);
        var location = TextLocation.FromSpan(_text, span);
        _diagnostics.ReportUnexpectedCharacter(location, Current);
        var badToken = new SyntaxToken(SyntaxKind.BadToken, _position, Current.ToString());
        _position++;
        return badToken;
    }

    private SyntaxToken ReadWhitespace()
    {
        int start = _position;
        while (_position < _text.Length && (Current == ' ' || Current == '\t'))
            _position++;

        string text = _text.ToString(start, _position - start);
        return new SyntaxToken(SyntaxKind.WhitespaceToken, start, text);
    }

    private SyntaxToken ReadLineContinuation()
    {
        int start = _position;

        // Skip ... or … (Unicode ellipsis is 1 char, ASCII is 3)
        if (_text[_position] == '\u2026')
            _position += 1;
        else
            _position += 3;

        // Consume the rest of the line (it's part of the continuation)
        while (_position < _text.Length && Current != '\n' && Current != '\r')
            _position++;

        // Consume the newline itself
        if (_position < _text.Length)
        {
            if (Current == '\r' && Lookahead == '\n')
                _position += 2;
            else if (Current == '\n' || Current == '\r')
                _position++;
        }

        string text = _text.ToString(start, _position - start);
        return new SyntaxToken(SyntaxKind.LineContinuationToken, start, text);
    }

    private SyntaxToken ReadHashDirective()
    {
        // Reads #: directives (e.g., #:sdk Lolcode.NET.Sdk) and #! shebang lines.
        // Skips the entire line, returning a SingleLineCommentToken (trivia).
        int start = _position;
        while (_position < _text.Length && Current != '\n' && Current != '\r')
            _position++;

        string text = _text.ToString(start, _position - start);
        return new SyntaxToken(SyntaxKind.SingleLineCommentToken, start, text);
    }

    private SyntaxToken ReadString()
    {
        // Opening quote
        int start = _position;
        _position++; // skip "

        var sb = new System.Text.StringBuilder();
        bool terminated = false;

        while (_position < _text.Length)
        {
            if (Current == '"')
            {
                _position++;
                terminated = true;
                break;
            }

            if (Current == '\n' || Current == '\r')
            {
                // Strings do not span lines
                break;
            }

            if (Current == ':')
            {
                // Escape sequence
                _position++;
                if (_position >= _text.Length)
                {
                    var escSpan = new TextSpan(_position - 1, 1);
                    var escLoc = TextLocation.FromSpan(_text, escSpan);
                    _diagnostics.ReportInvalidEscapeSequence(escLoc, ":");
                    break;
                }

                switch (Current)
                {
                    case ')': sb.Append('\n'); _position++; break;
                    case '>': sb.Append('\t'); _position++; break;
                    case 'o': sb.Append('\a'); _position++; break; // bell
                    case '"': sb.Append('"'); _position++; break;
                    case ':': sb.Append(':'); _position++; break;
                    case '(':
                        // Hex escape :(<hex>)
                        _position++; // skip (
                        int hexStart = _position;
                        while (_position < _text.Length && Current != ')')
                            _position++;
                        if (_position < _text.Length)
                        {
                            string hex = _text.ToString(hexStart, _position - hexStart);
                            _position++; // skip )
                            if (int.TryParse(hex, System.Globalization.NumberStyles.HexNumber, null, out int codePoint))
                            {
                                sb.Append(char.ConvertFromUtf32(codePoint));
                            }
                            else
                            {
                                var hexSpan = new TextSpan(hexStart - 2, _position - hexStart + 2);
                                var hexLoc = TextLocation.FromSpan(_text, hexSpan);
                                _diagnostics.ReportInvalidEscapeSequence(hexLoc, $":({hex})");
                            }
                        }
                        break;
                    case '[':
                        // Unicode named escape :[<name>]
                        _position++; // skip [
                        int nameStart = _position;
                        while (_position < _text.Length && Current != ']')
                            _position++;
                        if (_position < _text.Length)
                        {
                            string name = _text.ToString(nameStart, _position - nameStart);
                            _position++; // skip ]
                            char? named = ResolveUnicodeName(name);
                            if (named.HasValue)
                            {
                                sb.Append(named.Value);
                            }
                            else
                            {
                                var nameSpan = new TextSpan(nameStart - 2, _position - nameStart + 2);
                                var nameLoc = TextLocation.FromSpan(_text, nameSpan);
                                _diagnostics.ReportInvalidEscapeSequence(nameLoc, $":[{name}]");
                            }
                        }
                        break;
                    case '{':
                        // Variable interpolation :{<var>}
                        // For now, we include the raw text in the string value.
                        // The parser will handle interpolation.
                        _position--; // back to ':'
                        sb.Append(Current);
                        _position++;
                        sb.Append(Current); // '{'
                        _position++;
                        while (_position < _text.Length && Current != '}')
                        {
                            sb.Append(Current);
                            _position++;
                        }
                        if (_position < _text.Length)
                        {
                            sb.Append(Current); // '}'
                            _position++;
                        }
                        break;
                    default:
                        var defSpan = new TextSpan(_position - 1, 2);
                        var defLoc = TextLocation.FromSpan(_text, defSpan);
                        _diagnostics.ReportInvalidEscapeSequence(defLoc, $":{Current}");
                        sb.Append(Current);
                        _position++;
                        break;
                }
            }
            else
            {
                sb.Append(Current);
                _position++;
            }
        }

        if (!terminated)
        {
            var untermSpan = new TextSpan(start, _position - start);
            var untermLoc = TextLocation.FromSpan(_text, untermSpan);
            _diagnostics.ReportUnterminatedString(untermLoc);
        }

        string tokenText = _text.ToString(start, _position - start);
        string value = sb.ToString();

        // Check if the string contains interpolation markers
        if (value.Contains(":{"))
        {
            return new SyntaxToken(SyntaxKind.YarnLiteralToken, start, tokenText, value);
        }

        return new SyntaxToken(SyntaxKind.YarnLiteralToken, start, tokenText, value);
    }

    private static char? ResolveUnicodeName(string name)
    {
        // Curated subset of Unicode named characters
        return name.ToUpperInvariant() switch
        {
            "SPACE" => ' ',
            "TAB" or "CHARACTER TABULATION" => '\t',
            "NEWLINE" or "LINE FEED" or "LINE FEED (LF)" => '\n',
            "CARRIAGE RETURN" or "CARRIAGE RETURN (CR)" => '\r',
            "NULL" => '\0',
            "BELL" => '\a',
            "BACKSPACE" => '\b',
            "FORM FEED" or "FORM FEED (FF)" => '\f',
            "VERTICAL TAB" or "LINE TABULATION" => '\v',
            "QUOTATION MARK" => '"',
            "COLON" => ':',
            "EXCLAMATION MARK" => '!',
            "QUESTION MARK" => '?',
            "NUMBER SIGN" => '#',
            "DOLLAR SIGN" => '$',
            "PERCENT SIGN" => '%',
            "AMPERSAND" => '&',
            "APOSTROPHE" => '\'',
            "LEFT PARENTHESIS" => '(',
            "RIGHT PARENTHESIS" => ')',
            "ASTERISK" => '*',
            "PLUS SIGN" => '+',
            "COMMA" => ',',
            "HYPHEN-MINUS" => '-',
            "FULL STOP" => '.',
            "SOLIDUS" => '/',
            _ => null
        };
    }

    private SyntaxToken ReadNumber()
    {
        int start = _position;
        bool isFloat = false;

        if (Current == '-')
            _position++;

        while (_position < _text.Length && char.IsDigit(Current))
            _position++;

        if (_position < _text.Length && Current == '.' && char.IsDigit(Lookahead))
        {
            isFloat = true;
            _position++; // skip .
            while (_position < _text.Length && char.IsDigit(Current))
                _position++;
        }

        string text = _text.ToString(start, _position - start);

        if (isFloat)
        {
            if (double.TryParse(text, System.Globalization.CultureInfo.InvariantCulture, out double doubleValue))
            {
                return new SyntaxToken(SyntaxKind.NumbarLiteralToken, start, text, doubleValue);
            }
        }
        else
        {
            if (int.TryParse(text, System.Globalization.CultureInfo.InvariantCulture, out int intValue))
            {
                return new SyntaxToken(SyntaxKind.NumbrLiteralToken, start, text, intValue);
            }
        }

        var span = new TextSpan(start, text.Length);
        var location = TextLocation.FromSpan(_text, span);
        _diagnostics.ReportInvalidNumber(location, text);
        return new SyntaxToken(SyntaxKind.BadToken, start, text);
    }

    private SyntaxToken ReadIdentifierOrKeyword()
    {
        int start = _position;

        while (_position < _text.Length && (char.IsLetterOrDigit(Current) || Current == '_'))
            _position++;

        string text = _text.ToString(start, _position - start);

        // Handle BTW single-line comment
        if (text == "BTW")
        {
            while (_position < _text.Length && Current != '\n' && Current != '\r')
                _position++;
            string commentText = _text.ToString(start, _position - start);
            return new SyntaxToken(SyntaxKind.SingleLineCommentToken, start, commentText);
        }

        // Handle OBTW multi-line comment
        if (text == "OBTW")
        {
            // Read until TLDR
            while (_position < _text.Length)
            {
                if (_position + 3 < _text.Length &&
                    _text[_position] == 'T' && _text[_position + 1] == 'L' &&
                    _text[_position + 2] == 'D' && _text[_position + 3] == 'R')
                {
                    _position += 4;
                    break;
                }
                _position++;
            }
            string commentText = _text.ToString(start, _position - start);
            return new SyntaxToken(SyntaxKind.MultiLineCommentToken, start, commentText);
        }

        // Check for question mark suffix (RLY?, WTF?)
        bool hasQuestion = _position < _text.Length && Current == '?';

        string textWithQuestion = hasQuestion ? text + "?" : text;

        // Try to match with question mark first
        if (hasQuestion)
        {
            var kindWithQ = GetKeywordKind(textWithQuestion);
            if (kindWithQ != SyntaxKind.IdentifierToken)
            {
                _position++; // consume ?
                return new SyntaxToken(kindWithQ, start, textWithQuestion);
            }
        }

        var kind = GetKeywordKind(text);
        return new SyntaxToken(kind, start, text, kind == SyntaxKind.IdentifierToken ? text : null);
    }

    /// <summary>
    /// Maps a keyword string to its <see cref="SyntaxKind"/>.
    /// </summary>
    internal static SyntaxKind GetKeywordKind(string text) =>
        SyntaxFacts.GetKeywordKind(text);
}
