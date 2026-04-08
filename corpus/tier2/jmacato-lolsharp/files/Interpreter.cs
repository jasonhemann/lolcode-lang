using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;

namespace LOLSharp
{
    class Interpreter
    {
        public Console Console;
        public Tokenizer Tokenizer;
        public MainWindow MainWindow;
        public Lexer Lexer;


        public Dictionary<string, string> StringTable { get; set; }
        public Dictionary<string, Variable> WorkingMem = new Dictionary<string, Variable>();

        BackgroundWorker ExecutionThread = new BackgroundWorker();
        public string[] prog;

        public Interpreter()
        {
            Console = new Console();
            Tokenizer = new Tokenizer();
            ExecutionThread = new BackgroundWorker();
            ExecutionThread.WorkerSupportsCancellation = true;
            ExecutionThread.DoWork += ExecutionThread_DoWork;
            ExecutionThread.RunWorkerCompleted += ExecutionThread_RunWorkerCompleted; ;
        }

        private void ExecutionThread_RunWorkerCompleted(object sender, RunWorkerCompletedEventArgs e)
        {
            Console.WriteLine("\r\n\r\n[PROGRAM TERMINATED]");
        }
        
        private void ExecutionThread_DoWork(object sender, DoWorkEventArgs e)
        {
            for (Int64 l = 0; l < prog.Length - 1; l++){
                if (Console.HaltExec) {
                    StopExec();
                    return; }

                string[] lex;
                lex = prog[l].Split(' ');
                var head = lex[0];

                for (Int64 i = 0; i < lex.Length +1; i++)
                {
                    switch (head)
                    {
                        case "START":
                            Console.Clear();
                            i = lex.Length;
                            break;

                        case "END":
                            i = lex.Length;
                            break;

                        case "CPRT": //Write to console
                            if (CheckIfVar(lex[i + 1]) == true)
                            {
                                i++;
                                string tmp = GetVar(lex[i]).ToString();
                                if (tmp.Contains(Lexer.UNICODE_SECTION)){
                                    tmp = StringTable[tmp];
                                }
                                Console.Write(tmp);
                                i = lex.Length;
                                break;
                            }
                            else if (StringTable.ContainsKey(lex[i + 1]))
                            {
                                i++;
                                Console.Write(StringTable[lex[i]].ToString());
                                i = lex.Length;
                                break;
                            }
                            i = lex.Length;
                            break;
                        case "CPLN"://Write newline
                            Console.Write("\r\n");
                            i = lex.Length;
                            break;
                        case "NOP": //No operation
                            i = lex.Length;
                            break;
                        case "SWTC": //Switch WTF
                        case "COMP": //Comp ORLY
                            i = lex.Length;
                            break;
                        case "INPT":
                            var inputvar = lex[i + 1];
                            if (!CheckIfVar(inputvar)) {StopExec(); return; }
                            Console.StartIn();
                            while (Console.awaitinput) {
                                System.Threading.Thread.Sleep(2);
                                if (Console.HaltExec) { StopExec(); return; }
                            }
                            SetVar(inputvar, Console.ReadBuffer());
                            i = lex.Length;
                            break;
                        case "ASGN": //Assign variable with value/expression
                            i++;
                            var ASGNvar = lex[i];

                            var ASGN_ExprArray = lex.Skip(2).Take(lex.Length - 2).ToArray();
                            var ASGN_ExprString = String.Join(" ", ASGN_ExprArray);
                            var ASGN_ExpType = DetExpressionType(ASGN_ExprString);
                            SetVar(ASGNvar, ProcessExpression(ASGN_ExprArray));
                            i = lex.Length;
                            break;

                        case "DCLV": //Declare variable with initializer
                            var varname = lex[i+1];
                            object value = lex[i+3];

                            //Check if variable already exists
                            if (WorkingMem.ContainsKey(varname))
                            {
                                ErrorHelper.throwError(ErrorLevel.Error, ErrorCodes.MULTIPLE_DECLARATION, Tokenizer.ErrorList, l);
                                l = prog.Length;
                                StopExec();
                                return;
                            }

                            var dt_dclv = Tokenizer.DetermineDataType(value.ToString());
                            if (CheckIfVar(value.ToString()))
                            {
                                WorkingMem.Add(varname, new Variable() { name = varname, DataType = dt_dclv, value = GetVar(value.ToString()) });
                            }
                            else
                            {
                                WorkingMem.Add(varname, new Variable() { name = varname, DataType = dt_dclv, value = value });
                            }

                            i = lex.Length;
                            break;

                        case "DCLN": //Declare variable without initializer
                            var varname_n = lex[i+1];

                            if (WorkingMem.ContainsKey(varname_n)) {
                                ErrorHelper.throwError(ErrorLevel.Error, ErrorCodes.MULTIPLE_DECLARATION, Tokenizer.ErrorList, l);
                                l = prog.Length;
                                break;
                            }

                            WorkingMem.Add(varname_n, new Variable() { name = varname_n, DataType = DataTypes.NOOB, value = ""});

                            i = lex.Length;
                            break;
                        case "JMP": //Assign variable with value/expression
                            i++;
                            l = Convert.ToInt64(lex[i],16); 
                            i = lex.Length;
                            break;
                        case "JT": //Jump if true
                            i++;
                            var JT_IT = CBl(WorkingMem["IT"]);
                            var JT_LB = Convert.ToInt64(lex[i], 16);
                            if (JT_IT == true)
                            {
                                l = JT_LB;
                            }
                            i = lex.Length;
                            break;
                        case "JTX": //Jump if true, use REG_CMP as comparison
                            i++;
                            var JTX_IT = CBl(WorkingMem["REG_CMP"]);
                            var JTX_LB = Convert.ToInt64(lex[i], 16);
                            if (JTX_IT == true)
                            {
                                l = JTX_LB;
                            }
                            i = lex.Length;
                            break;
                        case "JF": //Jump if false
                            i++;
                            var JF_IT = CBl(WorkingMem["IT"]);
                            var JF_LB = Convert.ToInt64(lex[i], 16);
                            if (JF_IT == false)
                            {
                                l = JF_LB;
                            }
                            i = lex.Length;
                            break;
                        case "JNQ": //Continue if equal, Jump if not
                            i++;
                            string JNQ_IT = WorkingMem["IT"].value.ToString();
                            object JNQ_VL = lex[i];
                            var JNQ_LB = Convert.ToInt64(lex[i+1], 16);

                            if (JNQ_VL.ToString().Contains(Lexer.UNICODE_SECTION))
                            {
                                if (JNQ_IT != StringTable[JNQ_VL.ToString()])
                                {
                                    l = JNQ_LB;
                                }
                            } else 
                            {
                                if (JNQ_IT != JNQ_VL.ToString())
                                {
                                    l = JNQ_LB;
                                }
                            }
                            i = lex.Length;
                            break;
                        default:
                            Console.WriteLine("[" + head + "] Illegal/Unimplemented Instruction");
                            break;
                    }
                    //  System.Threading.Thread.Sleep(60);
                    var lni = String.Join(" ", lex);

                    MainWindow.Dispatcher.BeginInvoke((Action)(() =>
                    {
                        Lexer.DebugWin.setSymbols(WorkingMem.Values.ToList());
                    }));
                }
            }
        }

        public void StopExec()
        {
            MainWindow.Dispatcher.BeginInvoke((Action)(() =>
            {
                Console.HaltExec = false;
                Tokenizer.DebugWin.Activate();
            }));
        }

        public void Run(string[] progin)
        {

            Console = new Console();
            ExecutionThread = new BackgroundWorker();
            ExecutionThread.WorkerSupportsCancellation = true;
            ExecutionThread.DoWork += ExecutionThread_DoWork;
            ExecutionThread.RunWorkerCompleted += ExecutionThread_RunWorkerCompleted; ;

            MainWindow.Dispatcher.BeginInvoke((Action)(() =>
            {
                Console.Visibility = Visibility.Visible;
                Console.Activate();
            }));

            WorkingMem.Clear();
            WorkingMem = Tokenizer.BuiltInVariables();

            prog = progin;
            ExecutionThread.RunWorkerAsync();
        }

        public Stack<object> LiteralsStack = new Stack<object>();

        public double CDb(object x)
        {
            return Convert.ToDouble(x);
        }
        public bool CBl(object x)
        {

            var isString = x is string;
            var isInt = x is int | x is double;
            var isVariable = x is Variable;


            if (isVariable)
            {
                x = (((Variable)x).value);
                isString = x is string;
                isInt = x is int | x is double;
            }

            if (isString)
            {
                var cmp = x.ToString().ToUpper();
                if (cmp.Contains("WIN"))
                {
                    return true;
                }
                else if (cmp.Contains("FAIL"))
                {
                    return false;
                } else if (cmp==""||cmp=="0")
                {
                    return false;
                } else
                {
                    return true;
                }
            }

            if (isInt)
            {
                var cmp = Convert.ToDouble(x);
                if (cmp>0)
                {
                    return true;
                }
                else if (cmp==0)
                {
                    return false;
                }
            }

            
            return Convert.ToBoolean(x);
        }

        /// <summary>
        /// Parse a math expression to final result
        /// </summary>
        /// <param name="Ops"></param>
        /// <returns></returns>
        public object ProcessExpression(string[] Ops)
        {
            object x = 0, y = 0, r = 0;
            foreach (string op in Ops.Reverse())
            {
                switch (op)
                {
                    case "ADD":
                        y = LiteralsStack.Pop();
                        x = LiteralsStack.Pop();
                        r = CDb(x) + CDb(y);
                        LiteralsStack.Push(r);
                        break;
                    case "SUB":
                        y = LiteralsStack.Pop();
                        x = LiteralsStack.Pop();
                        r = CDb(y) - CDb(x);
                        LiteralsStack.Push(r);
                        break;
                    case "PROD":
                        y = LiteralsStack.Pop();
                        x = LiteralsStack.Pop();
                        r = CDb(x) * CDb(y);
                        LiteralsStack.Push(r);
                        break;
                    case "QUOT":
                        y = LiteralsStack.Pop();
                        x = LiteralsStack.Pop();
                        r = CDb(y) / CDb(x);
                        LiteralsStack.Push(r);
                        break;
                    case "MOD":
                        y = LiteralsStack.Pop();
                        x = LiteralsStack.Pop();
                        r = CDb(y) % CDb(x);
                        LiteralsStack.Push(r);
                        break;
                    case "MAX":
                        y = LiteralsStack.Pop();
                        x = LiteralsStack.Pop();
                        r = Math.Max(CDb(x), CDb(y));
                        LiteralsStack.Push(r);
                        break;
                    case "MIN":
                        y = LiteralsStack.Pop();
                        x = LiteralsStack.Pop();
                        r = Math.Min(CDb(x), CDb(y));
                        LiteralsStack.Push(r);
                        break;
                    case "AND":
                        y = LiteralsStack.Pop();
                        x = LiteralsStack.Pop();
                        r = CBl(x) & CBl(y);
                        LiteralsStack.Push(r);
                        break;
                    case "OR":
                        y = LiteralsStack.Pop();
                        x = LiteralsStack.Pop();
                        r = CBl(x) | CBl(y);
                        LiteralsStack.Push(r);
                        break;
                    case "XOR":
                        y = LiteralsStack.Pop();
                        x = LiteralsStack.Pop();
                        r = CBl(x) ^ CBl(y);
                        LiteralsStack.Push(r);
                        break;
                    case "NOT":
                        x = LiteralsStack.Pop();
                        r = !CBl(x);
                        LiteralsStack.Push(r);
                        break;
                    case "AAND":
                        r = CBl(LiteralsStack.Pop());
                        do
                        {
                            r = CBl(r) & CBl(LiteralsStack.Pop());
                        } while (LiteralsStack.Count != 0);
                        LiteralsStack.Push(r);
                        break;
                    case "ALOR":
                        r = CBl(LiteralsStack.Pop());
                        do
                        {
                            r = CBl(r) | CBl(LiteralsStack.Pop());
                        } while (LiteralsStack.Count != 0);
                        LiteralsStack.Push(r);
                        break;
                    case "IEQ":
                        y = LiteralsStack.Pop();
                        x = LiteralsStack.Pop();
                        r = (x.ToString() == y.ToString());
                        LiteralsStack.Push(r);
                        break;
                    case "NEQ":
                        y = LiteralsStack.Pop();
                        x = LiteralsStack.Pop();
                        r = (x.ToString() != y.ToString());
                        LiteralsStack.Push(r);
                        break;
                    case "MKAY":
                        break;
                    case "SMOOSH":
                        if (LiteralsStack.Peek().ToString().Contains(Lexer.UNICODE_SECTION))
                        {
                            r = StringTable[LiteralsStack.Pop().ToString()];
                        } else
                        {
                            r = LiteralsStack.Pop().ToString();
                        }
                        do
                        {
                            if (LiteralsStack.Peek().ToString().Contains(Lexer.UNICODE_SECTION))
                            {
                                r += StringTable[LiteralsStack.Pop().ToString()];
                            }
                            else
                            {
                                r += LiteralsStack.Pop().ToString();
                            }
                        } while (LiteralsStack.Count != 0);
                        LiteralsStack.Push(r);
                        break;
                    default:
                        if (CheckIfVar(op))
                        {
                            var u = GetVar(op);
                            LiteralsStack.Push(u);
                        } else
                        {

                            if (op.ToString().Contains("WIN"))
                            {
                                LiteralsStack.Push(true);
                            }
                            else if (op.ToString().Contains("FAIL"))
                            {
                                LiteralsStack.Push(false);
                            } else
                            {
                                LiteralsStack.Push(op);
                            }
                        }
                        break;
                }
            }

            if(LiteralsStack.Count > 1) {
                ErrorHelper.throwError(ErrorLevel.Fatal, ErrorCodes.STACK_OVERFLOW, Tokenizer.ErrorList);
                return null; }
            return LiteralsStack.Pop();
        }
        


        /// <summary>
        /// 
        /// </summary>
        /// <param name="key"></param>
        /// <returns></returns>
        public object GetVar(string key)
        {
            if (!WorkingMem.ContainsKey(key))
            {
                ErrorHelper.throwError(ErrorLevel.Error, ErrorCodes.UNKNOWN_OR_UNDECLARED_VARIABLE, Tokenizer.ErrorList);
                return null;
            }
            return WorkingMem[key].value;
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="key"></param>
        /// <param name="value"></param>
        /// <returns></returns>
        public bool SetVar(string key,object value)
        {
            if (!WorkingMem.ContainsKey(key))
            {
                ErrorHelper.throwError(ErrorLevel.Error, ErrorCodes.UNKNOWN_OR_UNDECLARED_VARIABLE, Tokenizer.ErrorList);
                return false;
            }

            WorkingMem[key].value = value;
            WorkingMem[key].DataType = Tokenizer.DetermineDataType(value.ToString());

            return true;
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="key"></param>
        /// <returns></returns>
        public bool CheckIfVar(string key)
        {
            return WorkingMem.ContainsKey(key);
        }


        /// <summary>
        /// 
        /// </summary>
        /// <param name="exp"></param>
        /// <returns></returns>
        public static ExpressionType DetExpressionType(string exp)
        {
            string[] BoolOps = {"AND",
                                "XOR",
                                "OR",
                                "AAND",
                                "ALOR",
                                "NOT"};

            string[] NumOps = {"ADD",
                                "SUB",
                                "PROD",
                                "QUOT",
                                "MOD",
                                "MAX",
                                "MIN"};

            foreach(string x in BoolOps)
            {
                if (exp.Contains(x)) { return ExpressionType.Logical; }
            }

            foreach (string x in NumOps)
            {
                if (exp.Contains(x)) { return ExpressionType.Numerical; }
            }

            return ExpressionType.None;
        }


    }
}
