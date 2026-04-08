using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Text;

namespace LOLSharp
{   
    public static class ErrorHelper
    {
        //Oopsie, somebody messed up ze lolz
        public static void throwError(ErrorLevel ErrorLevel, ErrorCodes ErrorCode, List<Error> ErrorList, Int64 line = 0, Int64 pos = 0)
        {
            Error curError = new Error();
            curError.line = line;
            curError.position = pos;
            curError.ErrorCode = ErrorCode;
            curError.ErrorLevel = ErrorLevel;
            ErrorList.Add(curError);
        }

        //Generate standard error message
        public static string generateErrorMessage(Error Err)
        {
            if (Err.line == 0)
            {
                return (Err.ErrorLevel.ToString() + " : " + Err.ErrorCode.ToString());
            }
            return (Err.ErrorLevel.ToString() + " : " + Err.ErrorCode.ToString() + " at line " + Err.line.ToString() + ", character " + Err.position.ToString());
        }

        //Count all unignorable errors
        public static Int64 CountBreakingErrors(List<Error> ErrList)
        {
            Int64 totalerrors = 0;
            if (ErrList.Count == 0) { return totalerrors; }
            foreach (Error Errors in ErrList)
            {
                if (Errors.ErrorLevel == ErrorLevel.Fatal | Errors.ErrorLevel == ErrorLevel.Error)
                {
                    totalerrors += 1;
                }
            }
            return totalerrors;
        }
    }
}
