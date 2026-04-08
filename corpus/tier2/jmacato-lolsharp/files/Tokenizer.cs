using System;
using System.Collections;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.Collections.Specialized;
using System.ComponentModel;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading;

namespace LOLSharp
{
    public class Tokenizer
    {
        public DebugWindow DebugWin;

        #region Declares
        public List<Error> ErrorList;
        //First pass token table
        public Dictionary<Int64, string[]> ProgTokenTableStg1 = new Dictionary<Int64, string[]>();
        //Second table for classified tokens
        public List<Token> ProgTokenTableStg2 = new List<Token>();
        //Lists definitions of each token, to be displayed in debugwin
        public Dictionary<Token, string> TokenDescriptorTable = new Dictionary<Token, string>();
        public Dictionary<string, Variable> VariableMemory = new Dictionary<string, Variable>();

        public Stack<Token> BranchingStack = new Stack<Token>();

        public static Dictionary<string, Variable> BuiltInVariables()
        {
            Dictionary<string, Variable> x = new Dictionary<string, Variable>() {
            {"IT", new Variable() { name="IT", DataType=DataTypes.NOOB, value=null} },
            {"REG_CMP", new Variable() { name="REG_CMP", DataType=DataTypes.NOOB, value=null}},
            {"CON_BUF", new Variable() { name="CON_BUF", DataType=DataTypes.NOOB, value=null}},
            {"TMP_ASN", new Variable() { name="TMP_ASN", DataType=DataTypes.NOOB, value=null}}

            };
            return x;
        }
        
        public Dictionary<string, string> CompressOps = new Dictionary<string, string>
                                    {
                                        {@"I HAS A","I-HAS-A"},
                                        {@"BOTH SAEM","IEQ"},
                                        {@"DIFFRINT","NEQ"},
                                        {@"SUM OF","ADD"},
                                        {@"DIFF OF","SUB"},
                                        {@"PRODUKT OF","PROD"},
                                        {@"QUOSHUNT OF","QUOT"},
                                        {@"MOD OF","MOD"},
                                        {@"BIGGR OF","MAX"},
                                        {@"SMALLR OF","MIN"},
                                        {@"O RLY?","O-RLY?"},
                                        {@"YA RLY","YA-RLY"},
                                        {@"NO WAI","NO-WAI"},
                                        {@"IM IN YR","IM-IN-YR"},
                                        {@"IM OUTTA YR","IM-OUTTA-YR"},
                                        {@"HOW IZ I","HOW-IZ-I"},
                                        {@"IF U SAY SO","IF-U-SAY-SO"},
                                        {@"I IZ","I-IZ"},
                                        {@"BOTH OF","AND"},
                                        {@"NOT","NOT"},
                                        {@"EITHER OF","OR"},
                                        {@"WON OF","XOR"},
                                        {@"ALL OF","AAND"},
                                        {@"ANY OF","ALOR"},
                                        {@"IS NOW A","IS-NOW-A"},
                                        {@"FOUND YR","FOUND-YR"}
                                    };
        public Dictionary<string, string> DTRegex = new Dictionary<string, string>
                        {
                            {@"^(-?[1-9]+\d*)$|^0$","Integer Literal"},
                            {@"^[0-9]*(?:\.[0-9]*)?$","Float Literal"},
                            {@"^[+-][0-9]*(?:\.[0-9]*)?$","Float Literal"},
                            {@"WIN|FAIL","Boolean Literal"},
                            {@"""[^\""]*""","String"},
                            {@"[A-Za-z][A-Za-z0-9_]*","Variable"}
                        };

        public string lolasm = "";
        public List<string> prog_asm = new List<string>();
        public Dictionary<string, Int64> jumplabels = new Dictionary<string, Int64>();


        #endregion

        /// <summary>
        /// Tokenize input from lexer
        /// </summary>
        /// <param name="raw"></param>
        public void Tokenize(string raw)
        {

            ProgTokenTableStg1.Clear();
            ProgTokenTableStg2.Clear();
            TokenDescriptorTable.Clear();
            VariableMemory.Clear();
            VariableMemory = BuiltInVariables();
            prog_asm.Clear();
            BranchingStack.Clear();
            jumplabels.Clear();
            lolasm = "";

            foreach (string x in raw.Split("\r\n".ToCharArray(), StringSplitOptions.RemoveEmptyEntries))
            {
                var curline = x;
                foreach (string s in CompressOps.Keys)
                {
                    curline = Regex.Replace(curline, s, CompressOps[s]);
                }
                var linenum = ProgTokenTableStg1.Count;
                ProgTokenTableStg1.Add(linenum, curline.Split(' '));
            }
            tokenRestruct(ProgTokenTableStg1);
        }

        /// <summary>
        /// Big-ass function to restructure the program
        /// </summary>
        /// <param name="progTokenTableStg1"></param>
        private void tokenRestruct(Dictionary<Int64, string[]> progTokenTableStg1)
        {
            int bLabelCount = 0;

            bool cmpNoExist = false;
            bool cmpYesExist = false;
            int cmpCmdCnt = 0;
            bool swtOWExist = false;
            Dictionary<long, string> cmpElseDict = new Dictionary<long, string>();


            for (Int64 line = 0; line < progTokenTableStg1.Keys.ToArray().Length; line++)
            {
                string[] curline = ProgTokenTableStg1[line];
                Int64 tokenCount = curline.Length;
                for (Int64 indx = 0; indx < tokenCount; indx++)
                {
                    string frame = curline[indx].Trim();
                    switch (frame)
                    {
                        case "HAI": //Program start
                            lolasm += Newline("START");
                            indx = tokenCount;
                            break;
                        case "KTHXBYE": //Program end
                            lolasm += Newline("END");
                            indx = tokenCount;
                            break;
                        case "I-HAS-A": //Variable declare
                            indx++;
                            var varname = curline[indx];
                            indx++;
                            if (tokenCount > 2 && curline[indx] == "ITZ")
                            {
                                indx++;
                                var varvalue = String.Join(" ", curline.Skip(3));
                                VariableMemory.Add(varname, new Variable() { name = varname, DataType = DetermineDataType(varvalue), value = varvalue });

                                if (Interpreter.DetExpressionType(varvalue) != ExpressionType.None)
                                {
                                  lolasm += Newline("ASGN TMP_ASN " + varvalue);
                                    lolasm += Newline("DCLV " + varname + " EQ TMP_ASN");
                                }
                                else
                                {
                                    lolasm += Newline("DCLV " + varname + " EQ " + varvalue);
                                }
                            }
                            else
                            {
                                VariableMemory.Add(varname, new Variable() { name = varname, DataType = DataTypes.NOOB });
                                lolasm += Newline("DCLN " + varname);
                            }
                            indx = tokenCount;
                            break;

                        case "VISIBLE":

                            //Get teh op arguments
                            var vis_Arg = String.Join(" ", curline.Skip(1));

                            if (Interpreter.DetExpressionType(vis_Arg) != ExpressionType.None)
                            {
                                lolasm += Newline("ASGN CON_BUF " + vis_Arg.Replace("!", "").Trim()); //Transform expression into the Assign Operand
                                lolasm += Newline("CPRT CON_BUF"); //Print the result
                            }
                            else
                            {
                                for (Int64 vsargs = 1; vsargs < tokenCount; vsargs++) //Enumerate all arguments and make separate commands
                                {
                                    lolasm += Newline("CPRT " + curline[vsargs]);
                                }
                            }

                            if (!vis_Arg.Contains("!"))
                            {
                                lolasm += Newline("CPLN");
                            }

                            indx = tokenCount;
                            break;

                        case "GIMMEH":
                            lolasm += Newline("INPT" + " " + curline[indx + 1]);
                            indx = tokenCount;
                            break;

                        case "WTF":
                        case "WTF?":
                            BranchingStack.Push(CreateToken(line, OperandType.Command, "SWTC"));
                            lolasm += Newline("SWTC");
                            indx = tokenCount;
                            break;
                        case "OMG":
                            if (BranchingStack.Count == 0) { ErrorHelper.throwError(ErrorLevel.Fatal, ErrorCodes.STRAY_CONDITIONALS, ErrorList, line); break; }
                            var Omg_k = BranchingStack.Peek();
                            if (Omg_k.tokenStr == "SWTC")
                            {
                                if (bLabelCount > 0)
                                {
                                    var omgpLB = "SWTC_" + Omg_k.lineAddress.ToString();
                                    lolasm += Newline("JMP " + omgpLB); //Add jumps from the previous OMG statement to skip the others
                                    var omg_pLB2 = "SWTC" + Omg_k.lineAddress.ToString() + "_" + bLabelCount.ToString();
                                    lolasm += Newline("LABEL " + omg_pLB2);
                                }
                                    indx++;
                                    bLabelCount++;
                                    var omg_lbl = "SWTC" + Omg_k.lineAddress.ToString() + "_" + bLabelCount.ToString();
                                    lolasm += Newline("JNQ " + curline[indx] + " " + omg_lbl);
                            }
                            else
                            {
                                ErrorHelper.throwError(ErrorLevel.Fatal, ErrorCodes.SYNTAX_ERROR, ErrorList, line);
                            }
                            indx = tokenCount;
                            break;
                        case "OMGWTF":
                            if (BranchingStack.Count == 0) { ErrorHelper.throwError(ErrorLevel.Fatal, ErrorCodes.STRAY_CONDITIONALS, ErrorList, line); break; }
                            var Omgw_k = BranchingStack.Peek();
                            if (Omgw_k.tokenStr == "SWTC")
                            {
                                swtOWExist = true;
                                var omgw_lbl = "SWTC" + Omgw_k.lineAddress.ToString() + "_" + bLabelCount.ToString();
                                lolasm += Newline("LABEL " + omgw_lbl);
                                indx++;
                            }
                            else
                            {
                                ErrorHelper.throwError(ErrorLevel.Fatal, ErrorCodes.SYNTAX_ERROR, ErrorList, line);
                            }
                            indx = tokenCount;
                            break;
                        case "OIC":

                            if (BranchingStack.Count == 0) { ErrorHelper.throwError(ErrorLevel.Fatal, ErrorCodes.STRAY_CONDITIONALS, ErrorList, line); break; }
                            var k = BranchingStack.Pop();

                            if (k.tokenStr == "SWTC")
                            {

                                if (!swtOWExist)
                                {
                                    var omgw_lbl = "SWTC" + k.lineAddress.ToString() + "_" + bLabelCount.ToString();
                                    lolasm += Newline("LABEL " + omgw_lbl);
                                    swtOWExist = false;
                                }

                                var OIC_lbl = k.tokenStr +"_" + k.lineAddress.ToString();
                                lolasm += Newline("LABEL " + OIC_lbl);
                            } else if (k.tokenStr == "COMP")
                            {
                                if (cmpCmdCnt > 0) //If not 1st op, add jmp to end
                                {
                                    var yr_lbl_e = "COMP" + k.lineAddress.ToString();
                                    lolasm += Newline("JMP " + yr_lbl_e);
                                }
                                var OIC_lbl = "COMP_"+ k.lineAddress.ToString();
                                lolasm += Newline("LABEL " + OIC_lbl + "_TBL");

                                if (cmpYesExist)
                                {
                                    lolasm += Newline("JT " + OIC_lbl + "_YES");
                                }

                                if (cmpElseDict.Count > 0)
                                {
                                    foreach (int elseKeys in cmpElseDict.Keys)
                                    {
                                        lolasm += Newline("ASGN REG_CMP " + cmpElseDict[elseKeys]);
                                        lolasm += Newline("JTX " + OIC_lbl + "_M" + elseKeys.ToString());
                                    }
                                }
                                if (cmpNoExist)
                                {
                                    lolasm += Newline("JF " + OIC_lbl + "_NO");
                                }
                                lolasm += Newline("LABEL " + k.tokenStr + k.lineAddress.ToString());
                                cmpYesExist = false;
                                cmpNoExist = false;
                                cmpElseDict.Clear();
                                cmpCmdCnt = 0;
                            }
                            bLabelCount = 0;
                            indx = tokenCount;
                            break;
                        case "O-RLY":
                        case "O-RLY?":
                            BranchingStack.Push(CreateToken(line, OperandType.Command, "COMP"));
                            lolasm += Newline("JMP COMP_"+line.ToString()+"_TBL");
                            indx = tokenCount;
                            break;
                        case "YA-RLY":
                        case "YA-RLY?":
                            if (BranchingStack.Count == 0) { ErrorHelper.throwError(ErrorLevel.Fatal, ErrorCodes.STRAY_CONDITIONALS, ErrorList, line); break; }
                            var yr = BranchingStack.Peek();
                            if (yr.tokenStr == "COMP")
                            {
                                if (cmpCmdCnt > 0) //If not 1st op, add jmp to end
                                {
                                    var yr_lbl_e = "COMP" + yr.lineAddress.ToString();
                                    lolasm += Newline("JMP " + yr_lbl_e);
                                }
                                cmpYesExist = true;
                                cmpCmdCnt++;
                                var yr_lbl = "COMP_" + yr.lineAddress.ToString() + "_YES";
                                lolasm += Newline("LABEL " + yr_lbl);
                            }
                            else
                            {
                                ErrorHelper.throwError(ErrorLevel.Fatal, ErrorCodes.SYNTAX_ERROR, ErrorList, line);
                            }
                            indx = tokenCount;
                            break;
                        case "NO-WAI":
                        case "NO-WAI?":
                            if (BranchingStack.Count == 0) { ErrorHelper.throwError(ErrorLevel.Fatal, ErrorCodes.STRAY_CONDITIONALS, ErrorList, line); break; }
                            cmpNoExist = true;
                            var nw = BranchingStack.Peek();
                            if (nw.tokenStr == "COMP")
                            {
                                if (cmpCmdCnt > 0) //If not 1st op, add jmp to end
                                {
                                    var nw_lbl_e = "COMP" + nw.lineAddress.ToString();
                                    lolasm += Newline("JMP " + nw_lbl_e);
                                }
                                cmpNoExist = true;
                                cmpCmdCnt++;
                                var nw_lbl = "COMP_" + nw.lineAddress.ToString() + "_NO";
                                lolasm += Newline("LABEL " + nw_lbl);
                            }
                            else
                            {
                                ErrorHelper.throwError(ErrorLevel.Fatal, ErrorCodes.SYNTAX_ERROR, ErrorList, line);
                            }
                            indx = tokenCount;
                            break;

                        case "MEBBE":
                            if (BranchingStack.Count == 0) { ErrorHelper.throwError(ErrorLevel.Fatal, ErrorCodes.STRAY_CONDITIONALS, ErrorList, line); break; }
                            var mb = BranchingStack.Peek();
                            if (mb.tokenStr == "COMP")
                            {
                                if (cmpCmdCnt > 0) //If not 1st op, add jmp to end
                                {
                                    var nw_lbl_e = "COMP" + mb.lineAddress.ToString();
                                    lolasm += Newline("JMP " + nw_lbl_e);
                                }

                                var yr_lbl = "COMP_" + mb.lineAddress.ToString() + "_M" + line.ToString();
                                lolasm += Newline("LABEL " + yr_lbl);

                                var varvalue = String.Join(" ", curline.Skip(1));
                                cmpElseDict.Add(line, varvalue);

                            }
                            else
                            {
                                ErrorHelper.throwError(ErrorLevel.Fatal, ErrorCodes.SYNTAX_ERROR, ErrorList, line);
                            }
                            indx = tokenCount;
                            break;

                        case "GTFO":

                            if (BranchingStack.Count == 0) { ErrorHelper.throwError(ErrorLevel.Fatal, ErrorCodes.STRAY_CONDITIONALS, ErrorList, line); break; }
                            var gt = BranchingStack.Peek();

                            var labelNameGTFO = gt.tokenStr + "_" + gt.lineAddress.ToString();
                            lolasm += Newline("JMP " + labelNameGTFO);
                            indx = tokenCount;
                            break;

                        case "ADD":
                        case "SUB":
                        case "PROD":
                        case "QUOT":
                        case "MOD":
                        case "MAX":
                        case "MIN":
                        case "AND":
                        case "OR":
                        case "XOR":
                        case "NOT":
                        case "AAND":
                        case "ALOR":
                        case "IEQ":
                        case "NEQ":
                            lolasm += Newline("ASGN IT " + String.Join(" ", curline));
                            indx = tokenCount;
                            break;
                        default:
                            if (VariableMemory.ContainsKey(curline[indx]))
                            {
                                if (tokenCount == 1)
                                {
                                    lolasm += Newline("ASGN IT " + curline[indx]); //IT <-- variable
                                    indx = tokenCount;
                                }
                                else
                                {
                                    if (curline[indx + 1] == "R")
                                    {

                                        var x = String.Join(" ", curline.Skip(2));
                                        lolasm += Newline("ASGN " + curline[indx] + " " + x);
                                        indx = tokenCount;
                                        break;
                                    }
                                }
                                break;
                            }
                            
                            lolasm += Newline(String.Join(" ", curline));
                            ErrorHelper.throwError(ErrorLevel.Error, ErrorCodes.SYNTAX_ERROR, ErrorList, line);
                            indx = tokenCount;
                            break;

                    }
                }
            }


            //Print the processed assembly and remove empty lines
            Int64 lin = 0;
            foreach (string ln in lolasm.Split("\r\n".ToCharArray(), StringSplitOptions.RemoveEmptyEntries))
            {
                prog_asm.Add(ln);
            }

            int lbladd = 0;
            List<string> templabellist = new List<string>();

            //Assign labels with their addresses
            foreach (string prgline in prog_asm)
            {
                var x = prgline.Split(' ');
                if (x[0] == "LABEL")
                {
                    jumplabels.Add(x[1], Convert.ToInt64(lbladd));
                    templabellist.Add("NOP");
                }
                else
                {
                    templabellist.Add(prgline);
                }
                lbladd++;

            }

            List<string> tempproglist = new List<string>();

            //Replace labels with hard-address
            foreach (string prgline in templabellist)
            {
                var x = prgline;
                foreach (string lbl in jumplabels.Keys)
                {
                    x = x.Replace(lbl, "0x" + jumplabels[lbl].ToString("X"));
                }
                tempproglist.Add(x);
            }

            prog_asm = tempproglist;

            lin = 0;
            foreach (string item in prog_asm)
            {
                string algn_tok = "";
                try
                {
                    string[] tok = item.Split(' ').Take(2).ToArray();
                    algn_tok = tok[0].PadRight(6) + tok[1].PadRight(12) + " " + String.Join(" ", item.Split(' ').Skip(2).ToArray());
                    DebugWin.Print(lin.ToString("X").PadRight(8) + algn_tok);
                }
                catch (Exception ex)
                {
                    DebugWin.Print(lin.ToString("X").PadRight(8) + item.PadRight(12));
                    Debug.Print(ex.Message);
                }


                lin++;
            }

            //lolasm = filter;

        }

        public string Newline(string s)
        {
            return s + "\r\n";
        }
        public void Add2ndStgToken(Int64 programAddress, OperandType OperandType, string tokenStr, DataTypes DataType = DataTypes.NOOB)
        {
            ProgTokenTableStg2.Add(new Token() { OperandType = OperandType, tokenStr = tokenStr, DataType = DataType, lineAddress = programAddress });
        }

        public Token CreateToken(Int64 programAddress, OperandType OperandType, string tokenStr, DataTypes DataType = DataTypes.NOOB)
        {
            return (new Token() { OperandType = OperandType, tokenStr = tokenStr, DataType = DataType, lineAddress = programAddress });
        }

        public string atos(object stringIn)
        {
            return stringIn.ToString();
        }

        /// <summary>
        /// Determines the datatypes of literals
        /// </summary>
        /// <param name="expression"></param>
        public DataTypes DetermineDataType(string expression)
        {
            var results = from Arg in DTRegex
                          where Regex.Match(expression, Arg.Key, RegexOptions.Singleline).Success
                          select Arg;

            foreach (var result in results)
            {
                switch (result.Value)
                {
                    case "Float Literal":
                        return DataTypes.NUMBAR;
                    case "Boolean Literal":
                        return DataTypes.TROOF;
                    case "Integer Literal":
                        return DataTypes.NUMBR;
                }
            }

            if (expression.Contains(Lexer.UNICODE_SECTION))
            { return DataTypes.YARN; }
            return DataTypes.NOOB;
        }


    }


}


