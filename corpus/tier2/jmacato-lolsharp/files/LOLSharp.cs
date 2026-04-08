using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace LOLSharp
{
    enum ExpressionType
    {
        Logical,
        Numerical,
        None
    }
    public enum ErrorCodes
    {
        COMPILER_ERROR,
        NO_PROG_START,
        NO_PROG_END,
        UNKNOWN_ESCAPE_SEQUENCE,
        UNTERMINATED_STRING_DELIMITER,
        INVALID_MULTILINE_COMMENT,
        STRAY_COMMENT_DELIMITER,
        STRAY_ENDING,
        STRAY_CONDITIONALS,
        SYNTAX_ERROR,
        MULTIPLE_DECLARATION,
        UNKNOWN_OR_UNDECLARED_VARIABLE,
        STACK_OVERFLOW
    }

    public enum ErrorLevel
    {
        Warning,
        Error,
        Fatal    
    }

    public class Error
    {
        public ErrorLevel ErrorLevel { get; set; }
        public ErrorCodes ErrorCode { get; set; }
        public Int64 line { get; set; }
        public Int64 position { get; set; }
    }

    public enum OperandType
    {
        Command,
        Expression,
        Literal,
        Variable,
        Argument,
        Label
    }

    public enum DataTypes
    {
        YARN,
        NUMBR,
        NUMBAR,
        TROOF,
        NOOB
    }

    public class Variable
    {
        public string name { get; set; }
        public DataTypes DataType { get; set; }
        public object value { get; set; }

    }

    public class Token
    {
        public Int64 lineAddress { get; set; }
        public OperandType OperandType { get; set; }
        public string tokenStr { get; set; }
        public DataTypes DataType { get; set; }
    }

}
