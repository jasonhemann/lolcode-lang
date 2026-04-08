using System.Globalization;

namespace Lolcode.Runtime;

/// <summary>
/// Runtime support library for compiled LOLCODE programs.
/// All LOLCODE values are represented as <see cref="object"/> at runtime.
/// Types: <see cref="int"/> (NUMBR), <see cref="double"/> (NUMBAR),
/// <see cref="string"/> (YARN), <see cref="bool"/> (TROOF), or <c>null</c> (NOOB).
/// </summary>
public static class LolRuntime
{
    // ==================== Type Coercion ====================

    /// <summary>
    /// Casts a value to TROOF (boolean).
    /// NOOB → FAIL, 0 → FAIL, 0.0 → FAIL, "" → FAIL, everything else → WIN.
    /// </summary>
    public static bool IsTruthy(object? value)
    {
        return value switch
        {
            null => false,
            bool b => b,
            int i => i != 0,
            double d => d != 0.0,
            string s => s.Length > 0,
            _ => true
        };
    }

    /// <summary>
    /// Casts a value to NUMBR (int).
    /// </summary>
    public static int CastToNumbr(object? value)
    {
        return value switch
        {
            null => 0,
            int i => i,
            double d => (int)d,
            bool b => b ? 1 : 0,
            string s when int.TryParse(s, CultureInfo.InvariantCulture, out int iResult) => iResult,
            string s when double.TryParse(s, CultureInfo.InvariantCulture, out double dResult) => (int)dResult,
            string => 0,
            _ => 0
        };
    }

    /// <summary>
    /// Casts a value to NUMBAR (double).
    /// </summary>
    public static double CastToNumbar(object? value)
    {
        return value switch
        {
            null => 0.0,
            int i => (double)i,
            double d => d,
            bool b => b ? 1.0 : 0.0,
            string s => double.TryParse(s, CultureInfo.InvariantCulture, out double result) ? result : 0.0,
            _ => 0.0
        };
    }

    /// <summary>
    /// Casts a value to YARN (string).
    /// NUMBAR uses 2 decimal places (F2 format).
    /// </summary>
    public static string CastToYarn(object? value)
    {
        return value switch
        {
            null => "",
            bool b => b ? "WIN" : "FAIL",
            int i => i.ToString(CultureInfo.InvariantCulture),
            double d => d.ToString("F2", CultureInfo.InvariantCulture),
            string s => s,
            _ => value.ToString() ?? ""
        };
    }

    /// <summary>
    /// Casts a value to TROOF.
    /// </summary>
    public static bool CastToTroof(object? value) => IsTruthy(value);

    /// <summary>
    /// Performs an explicit MAEK or IS NOW A cast.
    /// </summary>
    public static object? ExplicitCast(object? value, string targetType)
    {
        return targetType switch
        {
            "TROOF" => (object)CastToTroof(value),
            "NUMBR" => (object)CastToNumbr(value),
            "NUMBAR" => (object)CastToNumbar(value),
            "YARN" => (object)CastToYarn(value),
            "NOOB" => null,
            _ => throw new InvalidOperationException($"Unknown type: {targetType}")
        };
    }

    // ==================== Arithmetic ====================

    /// <summary>
    /// Coerces a value to a numeric type for arithmetic.
    /// NOOB → runtime error (per spec: "Any operations on a NOOB that assume another type result in an error").
    /// Non-numeric YARN → runtime error.
    /// bool: WIN→1, FAIL→0.
    /// </summary>
    private static object CoerceToNumeric(object? value)
    {
        return value switch
        {
            int => value,
            double => value,
            bool b => b ? 1 : 0,
            string s when s.Contains('.') => double.TryParse(s, CultureInfo.InvariantCulture, out double d)
                ? (object)d
                : throw new LolRuntimeException("Cannot cast YARN to numeric: " + s),
            string s => int.TryParse(s, CultureInfo.InvariantCulture, out int i)
                ? (object)i
                : throw new LolRuntimeException("Cannot cast YARN to numeric: " + s),
            null => throw new LolRuntimeException("Cannot use NOOB in arithmetic"),
            _ => throw new LolRuntimeException("Cannot use value in arithmetic: " + value)
        };
    }

    /// <summary>
    /// Determines if the result should be NUMBAR (double).
    /// If either operand is double, result is double.
    /// </summary>
    private static bool IsFloatOperation(object a, object b) => a is double || b is double;

    /// <summary>SUM OF a AN b</summary>
    public static object Add(object? a, object? b)
    {
        var ca = CoerceToNumeric(a);
        var cb = CoerceToNumeric(b);
        if (IsFloatOperation(ca, cb))
            return CastToNumbar(ca) + CastToNumbar(cb);
        return CastToNumbr(ca) + CastToNumbr(cb);
    }

    /// <summary>DIFF OF a AN b</summary>
    public static object Subtract(object? a, object? b)
    {
        var ca = CoerceToNumeric(a);
        var cb = CoerceToNumeric(b);
        if (IsFloatOperation(ca, cb))
            return CastToNumbar(ca) - CastToNumbar(cb);
        return CastToNumbr(ca) - CastToNumbr(cb);
    }

    /// <summary>PRODUKT OF a AN b</summary>
    public static object Multiply(object? a, object? b)
    {
        var ca = CoerceToNumeric(a);
        var cb = CoerceToNumeric(b);
        if (IsFloatOperation(ca, cb))
            return CastToNumbar(ca) * CastToNumbar(cb);
        return CastToNumbr(ca) * CastToNumbr(cb);
    }

    /// <summary>QUOSHUNT OF a AN b</summary>
    public static object Divide(object? a, object? b)
    {
        var ca = CoerceToNumeric(a);
        var cb = CoerceToNumeric(b);
        if (IsFloatOperation(ca, cb))
        {
            double divisor = CastToNumbar(cb);
            return divisor == 0.0 ? double.PositiveInfinity : CastToNumbar(ca) / divisor;
        }
        int intDivisor = CastToNumbr(cb);
        return intDivisor == 0 ? 0 : CastToNumbr(ca) / intDivisor;
    }

    /// <summary>MOD OF a AN b</summary>
    public static object Modulo(object? a, object? b)
    {
        var ca = CoerceToNumeric(a);
        var cb = CoerceToNumeric(b);
        if (IsFloatOperation(ca, cb))
        {
            double divisor = CastToNumbar(cb);
            return divisor == 0.0 ? double.NaN : CastToNumbar(ca) % divisor;
        }
        int intDivisor = CastToNumbr(cb);
        return intDivisor == 0 ? 0 : CastToNumbr(ca) % intDivisor;
    }

    /// <summary>BIGGR OF a AN b</summary>
    public static object Greater(object? a, object? b)
    {
        var ca = CoerceToNumeric(a);
        var cb = CoerceToNumeric(b);
        if (IsFloatOperation(ca, cb))
        {
            double da = CastToNumbar(ca), db = CastToNumbar(cb);
            return da >= db ? da : db;
        }
        int ia = CastToNumbr(ca), ib = CastToNumbr(cb);
        return ia >= ib ? ia : ib;
    }

    /// <summary>SMALLR OF a AN b</summary>
    public static object Smaller(object? a, object? b)
    {
        var ca = CoerceToNumeric(a);
        var cb = CoerceToNumeric(b);
        if (IsFloatOperation(ca, cb))
        {
            double da = CastToNumbar(ca), db = CastToNumbar(cb);
            return da <= db ? da : db;
        }
        int ia = CastToNumbr(ca), ib = CastToNumbr(cb);
        return ia <= ib ? ia : ib;
    }

    // ==================== Boolean Operations ====================

    /// <summary>BOTH OF a AN b (AND)</summary>
    public static bool And(object? a, object? b) => IsTruthy(a) && IsTruthy(b);

    /// <summary>EITHER OF a AN b (OR)</summary>
    public static bool Or(object? a, object? b) => IsTruthy(a) || IsTruthy(b);

    /// <summary>WON OF a AN b (XOR)</summary>
    public static bool Xor(object? a, object? b) => IsTruthy(a) ^ IsTruthy(b);

    /// <summary>NOT a</summary>
    public static bool Not(object? a) => !IsTruthy(a);

    // ==================== Comparison ====================

    /// <summary>
    /// BOTH SAEM: equality with NO auto-casting between different type families.
    /// NUMBR/NUMBAR promotes to NUMBAR. All other cross-type comparisons → FAIL.
    /// </summary>
    public static bool BothSaem(object? a, object? b)
    {
        if (a is null && b is null) return true;
        if (a is null || b is null) return false;

        // Same type comparison
        if (a.GetType() == b.GetType())
        {
            return a.Equals(b);
        }

        // NUMBR/NUMBAR cross-promotion
        if ((a is int || a is double) && (b is int || b is double))
        {
            return CastToNumbar(a) == CastToNumbar(b);
        }

        // Different type families → FAIL (no auto-casting)
        return false;
    }

    /// <summary>DIFFRINT: inequality (opposite of BOTH SAEM).</summary>
    public static bool Diffrint(object? a, object? b) => !BothSaem(a, b);

    // ==================== String Operations ====================

    /// <summary>
    /// SMOOSH: concatenate all arguments after casting each to YARN.
    /// </summary>
    public static string Smoosh(params object?[] args)
    {
        var sb = new System.Text.StringBuilder();
        foreach (var arg in args)
            sb.Append(CastToYarn(arg));
        return sb.ToString();
    }

    // ==================== I/O ====================

    /// <summary>
    /// VISIBLE: print arguments concatenated as YARN.
    /// </summary>
    public static void Print(object?[] args, bool suppressNewline)
    {
        var sb = new System.Text.StringBuilder();
        foreach (var arg in args)
            sb.Append(CastToYarn(arg));

        if (suppressNewline)
            Console.Write(sb.ToString());
        else
            Console.WriteLine(sb.ToString());
    }

    /// <summary>
    /// GIMMEH: read a line of input.
    /// </summary>
    public static string ReadLine()
    {
        return Console.ReadLine() ?? "";
    }
}

/// <summary>
/// Exception thrown for runtime errors in LOLCODE programs.
/// </summary>
public class LolRuntimeException : Exception
{
    public LolRuntimeException(string message) : base(message) { }
    public LolRuntimeException(string message, Exception inner) : base(message, inner) { }
}
