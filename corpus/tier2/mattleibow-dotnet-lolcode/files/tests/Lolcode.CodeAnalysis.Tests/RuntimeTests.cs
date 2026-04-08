using Lolcode.Runtime;

namespace Lolcode.CodeAnalysis.Tests;

/// <summary>
/// Tests for the LolRuntime helper methods.
/// </summary>
public class RuntimeTests
{
    // ==================== IsTruthy ====================

    [Fact]
    public void IsTruthy_Null_ReturnsFalse() =>
        LolRuntime.IsTruthy(null).Should().BeFalse();

    [Fact]
    public void IsTruthy_True_ReturnsTrue() =>
        LolRuntime.IsTruthy(true).Should().BeTrue();

    [Fact]
    public void IsTruthy_False_ReturnsFalse() =>
        LolRuntime.IsTruthy(false).Should().BeFalse();

    [Fact]
    public void IsTruthy_Zero_ReturnsFalse() =>
        LolRuntime.IsTruthy(0).Should().BeFalse();

    [Fact]
    public void IsTruthy_NonZero_ReturnsTrue() =>
        LolRuntime.IsTruthy(42).Should().BeTrue();

    [Fact]
    public void IsTruthy_ZeroDouble_ReturnsFalse() =>
        LolRuntime.IsTruthy(0.0).Should().BeFalse();

    [Fact]
    public void IsTruthy_NonZeroDouble_ReturnsTrue() =>
        LolRuntime.IsTruthy(3.14).Should().BeTrue();

    [Fact]
    public void IsTruthy_EmptyString_ReturnsFalse() =>
        LolRuntime.IsTruthy("").Should().BeFalse();

    [Fact]
    public void IsTruthy_NonEmptyString_ReturnsTrue() =>
        LolRuntime.IsTruthy("hello").Should().BeTrue();

    // ==================== CastToNumbr ====================

    [Fact]
    public void CastToNumbr_Null_ReturnsZero() =>
        LolRuntime.CastToNumbr(null).Should().Be(0);

    [Fact]
    public void CastToNumbr_Int_ReturnsSame() =>
        LolRuntime.CastToNumbr(42).Should().Be(42);

    [Fact]
    public void CastToNumbr_Double_Truncates() =>
        LolRuntime.CastToNumbr(3.7).Should().Be(3);

    [Fact]
    public void CastToNumbr_True_ReturnsOne() =>
        LolRuntime.CastToNumbr(true).Should().Be(1);

    [Fact]
    public void CastToNumbr_False_ReturnsZero() =>
        LolRuntime.CastToNumbr(false).Should().Be(0);

    [Fact]
    public void CastToNumbr_NumericString_Parses() =>
        LolRuntime.CastToNumbr("42").Should().Be(42);

    [Fact]
    public void CastToNumbr_NonNumericString_ReturnsZero() =>
        LolRuntime.CastToNumbr("hello").Should().Be(0);

    // ==================== CastToNumbar ====================

    [Fact]
    public void CastToNumbar_Null_ReturnsZero() =>
        LolRuntime.CastToNumbar(null).Should().Be(0.0);

    [Fact]
    public void CastToNumbar_Int_Converts() =>
        LolRuntime.CastToNumbar(42).Should().Be(42.0);

    [Fact]
    public void CastToNumbar_Double_ReturnsSame() =>
        LolRuntime.CastToNumbar(3.14).Should().Be(3.14);

    [Fact]
    public void CastToNumbar_True_ReturnsOne() =>
        LolRuntime.CastToNumbar(true).Should().Be(1.0);

    [Fact]
    public void CastToNumbar_NumericString_Parses() =>
        LolRuntime.CastToNumbar("3.14").Should().Be(3.14);

    // ==================== CastToYarn ====================

    [Fact]
    public void CastToYarn_Null_ReturnsEmpty() =>
        LolRuntime.CastToYarn(null).Should().Be("");

    [Fact]
    public void CastToYarn_Int_ReturnsString() =>
        LolRuntime.CastToYarn(42).Should().Be("42");

    [Fact]
    public void CastToYarn_Double_ReturnsTwoDecimals() =>
        LolRuntime.CastToYarn(3.14159).Should().Be("3.14");

    [Fact]
    public void CastToYarn_DoubleWhole_ReturnsTwoDecimals() =>
        LolRuntime.CastToYarn(7.0).Should().Be("7.00");

    [Fact]
    public void CastToYarn_True_ReturnsWIN() =>
        LolRuntime.CastToYarn(true).Should().Be("WIN");

    [Fact]
    public void CastToYarn_False_ReturnsFAIL() =>
        LolRuntime.CastToYarn(false).Should().Be("FAIL");

    [Fact]
    public void CastToYarn_String_ReturnsSame() =>
        LolRuntime.CastToYarn("hello").Should().Be("hello");

    // ==================== Arithmetic ====================

    [Fact]
    public void Add_TwoInts_ReturnsInt() =>
        LolRuntime.Add(3, 4).Should().Be(7);

    [Fact]
    public void Add_IntAndDouble_ReturnsDouble()
    {
        var result = LolRuntime.Add(3, 1.5);
        result.Should().BeOfType<double>();
        result.Should().Be(4.5);
    }

    [Fact]
    public void Add_TwoDoubles_ReturnsDouble() =>
        LolRuntime.Add(1.5, 2.5).Should().Be(4.0);

    [Fact]
    public void Add_StringContainingNumber_Parses() =>
        LolRuntime.Add("3", 4).Should().Be(7);

    [Fact]
    public void Subtract_TwoInts_ReturnsInt() =>
        LolRuntime.Subtract(10, 3).Should().Be(7);

    [Fact]
    public void Multiply_TwoInts_ReturnsInt() =>
        LolRuntime.Multiply(3, 4).Should().Be(12);

    [Fact]
    public void Divide_TwoInts_TruncatesInt() =>
        LolRuntime.Divide(7, 2).Should().Be(3);

    [Fact]
    public void Divide_IntAndDouble_ReturnsDouble() =>
        LolRuntime.Divide(7, 2.0).Should().Be(3.5);

    [Fact]
    public void Modulo_TwoInts_ReturnsRemainder() =>
        LolRuntime.Modulo(7, 3).Should().Be(1);

    [Fact]
    public void Greater_ReturnsLarger() =>
        LolRuntime.Greater(3, 7).Should().Be(7);

    [Fact]
    public void Smaller_ReturnsSmaller() =>
        LolRuntime.Smaller(3, 7).Should().Be(3);

    // ==================== Boolean Operations ====================

    [Fact]
    public void And_TrueTrue_ReturnsTrue() =>
        LolRuntime.And(true, true).Should().BeTrue();

    [Fact]
    public void And_TrueFalse_ReturnsFalse() =>
        LolRuntime.And(true, false).Should().BeFalse();

    [Fact]
    public void Or_FalseTrue_ReturnsTrue() =>
        LolRuntime.Or(false, true).Should().BeTrue();

    [Fact]
    public void Xor_TrueTrue_ReturnsFalse() =>
        LolRuntime.Xor(true, true).Should().BeFalse();

    [Fact]
    public void Xor_TrueFalse_ReturnsTrue() =>
        LolRuntime.Xor(true, false).Should().BeTrue();

    [Fact]
    public void Not_True_ReturnsFalse() =>
        LolRuntime.Not(true).Should().BeFalse();

    [Fact]
    public void Not_False_ReturnsTrue() =>
        LolRuntime.Not(false).Should().BeTrue();

    // ==================== Comparison ====================

    [Fact]
    public void BothSaem_SameInts_ReturnsTrue() =>
        LolRuntime.BothSaem(42, 42).Should().BeTrue();

    [Fact]
    public void BothSaem_DifferentInts_ReturnsFalse() =>
        LolRuntime.BothSaem(42, 43).Should().BeFalse();

    [Fact]
    public void BothSaem_IntAndDouble_PromotesToDouble() =>
        LolRuntime.BothSaem(3, 3.0).Should().BeTrue();

    [Fact]
    public void BothSaem_StringAndInt_ReturnsFalse_NoCrossCast() =>
        LolRuntime.BothSaem("3", 3).Should().BeFalse();

    [Fact]
    public void BothSaem_NullNull_ReturnsTrue() =>
        LolRuntime.BothSaem(null, null).Should().BeTrue();

    [Fact]
    public void BothSaem_NullInt_ReturnsFalse() =>
        LolRuntime.BothSaem(null, 0).Should().BeFalse();

    [Fact]
    public void Diffrint_SameInts_ReturnsFalse() =>
        LolRuntime.Diffrint(42, 42).Should().BeFalse();

    [Fact]
    public void Diffrint_DifferentInts_ReturnsTrue() =>
        LolRuntime.Diffrint(42, 43).Should().BeTrue();

    // ==================== Smoosh ====================

    [Fact]
    public void Smoosh_Strings_Concatenates() =>
        LolRuntime.Smoosh("hello", " ", "world").Should().Be("hello world");

    [Fact]
    public void Smoosh_MixedTypes_CastsToYarn() =>
        LolRuntime.Smoosh("value: ", 42).Should().Be("value: 42");

    [Fact]
    public void Smoosh_WithDouble_UsesTwoDecimals() =>
        LolRuntime.Smoosh("pi=", 3.14159).Should().Be("pi=3.14");

    // ==================== ExplicitCast ====================

    [Fact]
    public void ExplicitCast_ToNOOB_ReturnsNull() =>
        LolRuntime.ExplicitCast(42, "NOOB").Should().BeNull();

    [Fact]
    public void ExplicitCast_ToTROOF_ReturnsBool()
    {
        LolRuntime.ExplicitCast(1, "TROOF").Should().Be(true);
        LolRuntime.ExplicitCast(0, "TROOF").Should().Be(false);
    }

    [Fact]
    public void ExplicitCast_ToNUMBR_ReturnsInt() =>
        LolRuntime.ExplicitCast("42", "NUMBR").Should().Be(42);

    [Fact]
    public void ExplicitCast_ToNUMBAR_ReturnsDouble() =>
        LolRuntime.ExplicitCast("3.14", "NUMBAR").Should().Be(3.14);

    [Fact]
    public void ExplicitCast_ToYARN_ReturnsString() =>
        LolRuntime.ExplicitCast(42, "YARN").Should().Be("42");

    // ==================== NOOB Arithmetic Errors ====================

    [Fact]
    public void Add_NoobThrows() =>
        FluentActions.Invoking(() => LolRuntime.Add(null, 1))
            .Should().Throw<LolRuntimeException>()
            .WithMessage("*NOOB*");

    [Fact]
    public void Subtract_NoobThrows() =>
        FluentActions.Invoking(() => LolRuntime.Subtract(1, null))
            .Should().Throw<LolRuntimeException>()
            .WithMessage("*NOOB*");

    [Fact]
    public void Multiply_NoobThrows() =>
        FluentActions.Invoking(() => LolRuntime.Multiply(null, null))
            .Should().Throw<LolRuntimeException>()
            .WithMessage("*NOOB*");

    [Fact]
    public void Divide_NoobThrows() =>
        FluentActions.Invoking(() => LolRuntime.Divide(null, 1))
            .Should().Throw<LolRuntimeException>()
            .WithMessage("*NOOB*");

    [Fact]
    public void Add_NonNumericYarnThrows() =>
        FluentActions.Invoking(() => LolRuntime.Add("hello", 1))
            .Should().Throw<LolRuntimeException>()
            .WithMessage("*Cannot cast YARN*");

    [Fact]
    public void Modulo_NonNumericYarnThrows() =>
        FluentActions.Invoking(() => LolRuntime.Modulo("abc", 2))
            .Should().Throw<LolRuntimeException>()
            .WithMessage("*Cannot cast YARN*");

    // ==================== Numeric YARN Coercion ====================

    [Fact]
    public void Add_NumericYarn_ParsesCorrectly() =>
        LolRuntime.Add("3", 2).Should().Be(5);

    [Fact]
    public void Add_FloatYarn_ParsesCorrectly() =>
        LolRuntime.Add("3.5", 2).Should().Be(5.5);

    // ==================== Division Edge Cases ====================

    [Fact]
    public void Divide_IntByZero_ReturnsZero() =>
        LolRuntime.Divide(10, 0).Should().Be(0);

    [Fact]
    public void Divide_FloatByZero_ReturnsInfinity() =>
        LolRuntime.Divide(10.0, 0.0).Should().Be(double.PositiveInfinity);

    [Fact]
    public void Modulo_IntByZero_ReturnsZero() =>
        LolRuntime.Modulo(10, 0).Should().Be(0);

    // ==================== SMOOSH Additional ====================

    [Fact]
    public void Smoosh_EmptyArgs_ReturnsEmpty() =>
        LolRuntime.Smoosh().Should().Be("");

    [Fact]
    public void Smoosh_WithNull_CastsToEmpty() =>
        LolRuntime.Smoosh("a", null, "b").Should().Be("ab");

    // ==================== BothSaem Edge Cases ====================

    [Fact]
    public void BothSaem_BothNull_ReturnsTrue() =>
        LolRuntime.BothSaem(null, null).Should().BeTrue();

    [Fact]
    public void BothSaem_IntDouble_Promotion() =>
        LolRuntime.BothSaem(3, 3.0).Should().BeTrue();

    [Fact]
    public void BothSaem_IntDouble_NotEqual() =>
        LolRuntime.BothSaem(3, 3.1).Should().BeFalse();

    [Fact]
    public void BothSaem_StringInt_NoAutocast() =>
        LolRuntime.BothSaem("42", 42).Should().BeFalse();

    [Fact]
    public void BothSaem_BoolInt_NoAutocast() =>
        LolRuntime.BothSaem(true, 1).Should().BeFalse();

    // ==================== CastToYarn Formatting ====================

    [Fact]
    public void CastToYarn_Numbar_TwoDecimals() =>
        LolRuntime.CastToYarn(7.0).Should().Be("7.00");

    [Fact]
    public void CastToYarn_NumbarPi_TwoDecimals() =>
        LolRuntime.CastToYarn(3.14159).Should().Be("3.14");

    [Fact]
    public void CastToYarn_Null_EmptyString() =>
        LolRuntime.CastToYarn(null).Should().Be("");

    [Fact]
    public void CastToYarn_Bool_WinFail() =>
        LolRuntime.CastToYarn(true).Should().Be("WIN");

    [Fact]
    public void Greater_Equal_ReturnsFirst() =>
        LolRuntime.Greater(5, 5).Should().Be(5);

    [Fact]
    public void Greater_FloatPromotion() =>
        LolRuntime.Greater(3, 3.5).Should().Be(3.5);
}
