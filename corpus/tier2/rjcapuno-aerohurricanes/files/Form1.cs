using System;
using System.Collections.Generic;
using System.Collections.Specialized;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;
using System.Text.RegularExpressions;
using System.IO;

namespace safeprojectname
{
    public partial class Form1 : Form
    {
        LinkedList<String> lexemes; // AddLast()
        public Dictionary<String, String> symbolTable;
        String[] arr = new String[100];
        Stack<string> st;
        String[] content; 
        Stack<String> st1;
        int arithStat = 0;
        int booleanStat = 0;
        int comparisonStat = 0;
        int yarlycnt, nowaicnt = 0;
        bool hasErr;

        public Form1()
        {
            InitializeComponent();
            lexemes = new LinkedList<String>();
            symbolTable = new Dictionary<String, String>();
            st = new Stack<string>();
            st1 = new Stack<String>();
            
           
        }

        private void run_Click(object sender, EventArgs e)
        {
            this.table1.Rows.Clear(); this.table2.Rows.Clear(); output.Clear(); symbolTable.Clear(); lexemes.Clear();
            symbolTable.Add("IT", "");
            String code = editor.Text;
            if (code.Length == 0)
            {// no code written
                output.AppendText("\nError: No code");
            }
            else this.checkSyntax(code);
        }

        // check REGEX of line
        private void checkSyntax(string s)
        {
            // REGEX here
            content = s.Split('\n');
            string pattern = @"\bHAI\s+((.*\s*)*)?KTHXBYE\b";
            Match m = Regex.Match(s, pattern);
            if (m.Success)
            {
                table1.Rows.Add("HAI", "CODE DELIMITER");
                using (StringReader strRead = new StringReader(m.Groups[1].Value))
                {
                    string strGetLineVal;
                    while ((strGetLineVal = strRead.ReadLine()) != null) this.checkString(strGetLineVal);
                }
                table1.Rows.Add("KTHXBYE", "CODE DELIMITER");
            }
            else
            {
                if (output.TextLength != 0) output.AppendText("\n\n");
                output.AppendText("\nError: Missing / wrong code delimiter");
            }
        }

        private void checkString(String line) {
            string str;
            if (line.Contains(' ')) str = line.Substring(0, line.IndexOf(" "));
            else str = line;
            switch (str)
            {
                case "I": this.VarDeclaration(line);
                    break;
                case "GIMMEH": this.InputStatement(line);
                    break;
                case "VISIBLE": this.OutputStatement(line);
                    break;
                case "MAEK": this.TypeCastMaek(line);
                    break;
                case "SUM": case "DIFF": case "PRODUKT": case "QUOSHUNT": case "MOD": case "BIGGR": case "SMALLR":
                    this.ArithmeticOp(line, "");
                    break;
                case "BOTH": case "EITHER": case "WON": case "NOT": case "ANY": case "ALL":
                    this.BoolOp(line, "");
                    this.ComparisonOp(line, "");
                    break;
                case "DIFFRINT":
                    this.ComparisonOp(line, "");
                    break;
                case "SMOOSH": this.ConcatStatement(line);
                    break;
                case "IM": //this.LoopStatement(line);
                    /*Match m = Regex.Match(line, "(?<loop>IM\\s+IN\\s+YR|IM\\s+OUTTA\\s+YR)\\s+(?<value>[a-zA-Z]\\w*)");
                     if (m.Success)
                    {
                        table1.Rows.Add(m.Groups["loop"].Value, "LOOP DELIMITER");
                        lexemes.AddLast(m.Groups["loop"].Value);
                        table1.Rows.Add(m.Groups["value"].Value, "LOOP DELIMITER");
                        lexemes.AddLast(m.Groups["value"].Value);
                    }*/
                    Match m4 = Regex.Match(line, "IM\\s+IN\\s+YR\\s+(?<label1>[a-zA-Z]+)\\s+(?<opr1>UPPIN|NERFIN)\\s+YR\\s+(?<var>[a-zA-Z]\\w*)(\\s+)?((?<opr2>TIL|WILE)\\s+(?<expr>.+)\\s+)?");
                     Match m = Regex.Match(line, "(?<loop>IM\\s+OUTTA\\s+YR)\\s+(?<value>[a-zA-Z]\\w*)");
                     if (m4.Success) {
                         table1.Rows.Add("IM IN YR", "LOOP STATEMENT");
                         lexemes.AddLast("IM IN YR");
                         table1.Rows.Add(m4.Groups["label1"].Value, "LOOP LABEL");
                         lexemes.AddLast(m4.Groups["label1"].Value);
                         table1.Rows.Add(m4.Groups["opr1"].Value, "OPERATION");
                         lexemes.AddLast(m4.Groups["opr1"].Value);
                         table1.Rows.Add("YR", "KEYWORD");
                         lexemes.AddLast("YR");
                         table1.Rows.Add(m4.Groups["var"].Value, "VARIABLE IDENTIFIER");
                         lexemes.AddLast(m4.Groups["var"].Value);
                         this.output.AppendText(m4.Groups["opr2"].Value);
                         if (!string.IsNullOrEmpty(m4.Groups["opr2"].Value))
                         {
                             table1.Rows.Add(m4.Groups["opr2"].Value, "OPERATION");
                             lexemes.AddLast(m4.Groups["opr2"].Value);
                         }
                         if (!string.IsNullOrEmpty(m4.Groups["expr"].Value))
                         {
                             this.checkExpr(m4.Groups["expr"].Value, "");
                         }
                     }
                     if (m.Success)
                     {
                         table1.Rows.Add(m.Groups["loop"].Value, "LOOP DELIMITER");
                         lexemes.AddLast(m.Groups["loop"].Value);
                         table1.Rows.Add(m.Groups["value"].Value, "LOOP LABEL");
                         lexemes.AddLast(m.Groups["value"].Value);
                     }
                    break;
                case "O": this.IfThenStatement(line);
                    if (Regex.IsMatch(line, "\\s*O\\s+RLY?"))
                    {
                        table1.Rows.Add("O RLY?", "CONDITIONAL DELIMITER");
                        lexemes.AddLast("O RLY?");
                    }
                    break;
                case "YA":
                    if (Regex.IsMatch(line, "YA\\s+RLY"))
                    {
                        table1.Rows.Add("YA RLY", "IF DELIMITER");
                        lexemes.AddLast("YA RLY");
                    }
                    break;
                case "NO":
                    if (Regex.IsMatch(line, "NO\\s+WAI"))
                    {
                        table1.Rows.Add("NO WAI", "IF DELIMITER");
                        lexemes.AddLast("NO WAI");
                    }
                    break;
                case "OIC":
                    if (Regex.IsMatch(line, "OIC"))
                    {
                        table1.Rows.Add("OIC", "CONDITIONAL DELIMITER");
                        lexemes.AddLast("OIC");
                    }
                    break;
                case "MEBBE":
                    Match m2 = Regex.Match(line, "MEBBE\\s+(?<expr>.+)");
                    if (m2.Success)
                    {
                        table1.Rows.Add("MEBBE", "ELSE-IF DELIMITER");
                        lexemes.AddLast("MEBBE");
                        this.checkExpr(m2.Groups["expr"].Value, "");
                    }
                    break;
                case "OMG":
                    Match m3 = Regex.Match(line, "OMG\\s+(?<value>.+)");
                    if (m3.Success)
                    {
                        table1.Rows.Add("OMG", "CASE DELIMITER");
                        lexemes.AddLast("OMG");
                        this.checkValue(m3.Groups["value"].Value);
                    }
                    break;
                case "HOW": this.FunctionStatement(line);
                    break;
                case "IF":
                    if (Regex.IsMatch(line, "IF\\s+U\\s+SAY\\s+SO"))
                    {
                        table1.Rows.Add("IF U SAY SO", "FUNCTION DELIMITER");
                        lexemes.AddLast("IF U SAY SO");
                    }
                    break;
                default:
                    Match m1 = Regex.Match(str, "[a-zA-Z]\\w*");
                    if (m1.Success) this.VarsFirst(line);
                    break;
            }
        }

        private void checkExpr(String line, String var){
            string str;
            if (line.Contains(' ')) str = line.Substring(0, line.IndexOf(" "));
            else str = line;
            switch (str)
            {
                case "SUM": case "DIFF": case "PRODUKT": case "QUOSHUNT": case "MOD": case "BIGGR": case "SMALLR":
                    this.ArithmeticOp(line, var);
                    break;
                case "BOTH": case "EITHER": case "WON": case "NOT": case "ANY": case "ALL":
                    this.BoolOp(line, var);
                    this.ComparisonOp(line, var);
                    break;
                case "DIFFRINT":
                    this.ComparisonOp(line, var);
                    break;
                default: this.checkValue(line);
                    break;
            }
        }
			
        private void VarDeclaration(String line) {
            // VARIABLE DECLARATION AND INITIALIZATION
            Match m = Regex.Match(line, "I\\s+HAS\\s+A\\s+(?<vardec>[a-zA-Z]\\w*)(\\s+(?<initVar>ITZ)\\s+(?<value>[a-zA-Z]\\w*|\\\"(.*?)\\\"|(\\-|\\+)?[0-9]+(\\.[0-9]*)?|WIN|FAIL))?");
            if (m.Success)
            {
                string value = "";
                if (!symbolTable.TryGetValue(m.Groups["vardec"].Value, out value))
                {
                    symbolTable.Add(m.Groups["vardec"].Value, m.Groups["value"].Value);
                }
                else
                {
                    this.output.AppendText("\nERROR: Variable identifier {" + m.Groups["vardec"].Value + "} already exists.");
                    return;
                }//If variable is declared twice

                if (!string.IsNullOrEmpty(m.Groups["value"].Value) && m.Groups["value"].Value == m.Groups["vardec"].Value) {
                    this.output.AppendText("\nERROR: Variable initialized to same variable {" + m.Groups["vardec"].Value+"}.");
                    return;
                }//If variable is initialized to same variable

                table1.Rows.Add("I HAS A", "VARIABLE DECLARATION");
                lexemes.AddLast("I HAS A");
                table1.Rows.Add(m.Groups["vardec"].Value, "VARIABLE IDENTIFIER");
                lexemes.AddLast(m.Groups["vardec"].Value);
                if (!string.IsNullOrEmpty(m.Groups["initVar"].Value))
                {
                    table1.Rows.Add(m.Groups["initVar"].Value, "INITIALIZE IDENTIFIER");
                    lexemes.AddLast(m.Groups["initVar"].Value);
                }
                if (!string.IsNullOrEmpty(m.Groups["value"].Value))
                {
                    Match m2 = Regex.Match(m.Groups["value"].Value, "I\\s+HAS\\s+A\\s+(?<vardec>[a-zA-Z]\\w*)(\\s+(?<initVar>ITZ)\\s+(?<value>[a-zA-Z]\\w*|\\\"(.*?)\\\"|(\\-|\\+)?[0-9]+(\\.[0-9]*)?|WIN|FAIL))?");
                    if (m.Groups["value"].Value == "WIN" || m.Groups["value"].Value == "FAIL")
                    {
                        table2.Rows.Add(m.Groups["vardec"].Value, this.checkInput(m.Groups["value"].Value), m.Groups["value"].Value);
                        symbolTable[m.Groups["vardec"].Value] = m.Groups["value"].Value;
                    }
                    else if (Regex.IsMatch(m.Groups["value"].Value, "^[a-zA-Z]\\w*$"))// I HAS A VAR ITZ VAR2
                    {
                        String value1 = "";
                        if (!symbolTable.TryGetValue(m.Groups["value"].Value, out value1))
                        {
                            this.output.AppendText("\nERROR: Variable identifier {" + m.Groups["value"].Value + "} does not exist.");
                            return;
                        }
                        else
                        {
                            if (!string.IsNullOrEmpty(value1))
                                table2.Rows.Add(m.Groups["vardec"].Value, this.checkValue(value1), value1);
                            else table2.Rows.Add(m.Groups["vardec"].Value, "NOOB", value1);
                            symbolTable[m.Groups["vardec"].Value] = value1;
                        }
                    }
                    else
                    {
                      
                        table2.Rows.Add(m.Groups["vardec"].Value, this.checkInput(m.Groups["value"].Value), m.Groups["value"].Value);
                        symbolTable[m.Groups["vardec"].Value] = m.Groups["value"].Value;
                    }
                }
                else
                {

                    table2.Rows.Add(m.Groups["vardec"].Value, "NOOB", m.Groups["value"].Value);
                    symbolTable[m.Groups["vardec"].Value] = m.Groups["value"].Value;
                }
            }
        }
			
        private bool VarsFirst(String line) {
            String value = "";
            if ((Regex.IsMatch(line, "^\\s*([a-zA-Z][a-zA-Z0-9_]*)\\s+R\\s+.+$")))
            {
                Regex r = new Regex("^\\s*(?<varident>([a-zA-Z][a-zA-Z0-9_]*))\\s+(?<assign>R)(?<rhs>\\s+.+)$");
                Match m = r.Match(line);

                if (symbolTable.TryGetValue(m.Groups["varident"].Value, out value))
                {

                    table1.Rows.Add(m.Groups["varident"].ToString(), "variable identifier");
                    table1.Rows.Add(m.Groups["assign"].ToString(), "variable assignment");

                    if ((Regex.IsMatch(line, "^\\s*(?<varident>([a-zA-Z][a-zA-Z0-9_]*))\\s+(?<assign>R)\\s+((BOTH\\s+SAEM|DIFFRINT))!?")))
                    {

                        String compexpr = m.Groups["rhs"].ToString().Trim();
                        symbolTable[m.Groups["varident"].ToString()] = this.ComparisonOp(compexpr, "");
                        return false;

                    }
                    else if ((Regex.IsMatch(line, "^\\s*(?<varident>([a-zA-Z][a-zA-Z0-9_]*))\\s+(?<assign>R)\\s+((SUM\\s+OF)|(DIFF\\s+OF)|(PRODUKT\\s+OF)|(QUOSHUNT\\s+OF)|(MOD\\s+OF)|(BIGGR\\s+OF)|(SMALLR\\s+OF))!?")))
                    {


                        String mathexpr = m.Groups["rhs"].ToString().Trim();
                        symbolTable[m.Groups["varident"].ToString()] = this.ArithmeticOp(mathexpr, "");
                        return false;

                    }
                    else if ((Regex.IsMatch(line, "^\\s*(?<varident>([a-zA-Z][a-zA-Z0-9_]*))\\s+(?<assign>R)\\s+((WON\\s+OF)|(EITHER\\s+OF)|(BOTH\\s+OF))!?")))
                    {

                        String boolexpr = m.Groups["rhs"].ToString().Trim();
                        symbolTable[m.Groups["varident"].ToString()] = this.BoolOp(boolexpr, "");
                        table2.Rows[GetRowIndexByValue(table2, m.Groups["varident"].ToString())].Cells[1].Value = symbolTable[m.Groups["varident"].ToString()];
                        return false;
                    }

                    else
                    {
                        symbolTable[m.Groups["varident"].ToString()] = m.Groups["rhs"].ToString();
                        return false;
                    }
                }
                else
                {
                    return true;
                }
            }
            else
            {
                return true;
            }
        }

        private int GetRowIndexByValue(DataGridView dgv, string value)
        {
            int row;
            for (row = 0; row < dgv.Rows.Count; row++)
            {
                if (dgv.Rows[row].Cells[0].Value!=null && dgv.Rows[row].Cells[0].Value.Equals(value))
                {
                    return row;
                }
            }
            return -1;
        }

        private bool InputStatement(String line)
        {
            // INPUT
            Match m = Regex.Match(line, "GIMMEH\\s+(?<vardec>[a-zA-Z]\\w*)");
            if (m.Success)
            {
                int row;
                // VAR
                string value = "";
                if (!symbolTable.TryGetValue(m.Groups["vardec"].Value, out value))
                {
                    this.output.AppendText("\nERROR: Variable identifier {" + m.Groups["vardec"].Value + "} does not exist.");
                    return true;
                }
                else
                { // store value in this index
                    row = this.GetRowIndexByValue(table2, m.Groups["vardec"].Value);
                }
                table1.Rows.Add("GIMMEH", "INPUT DECLARATION");
                lexemes.AddLast("GIMMEH");
                table1.Rows.Add(m.Groups["vardec"].Value, "VARIABLE IDENTIFIER");
                lexemes.AddLast(m.Groups["vardec"].Value);

                //call symbol table
                Form2 inputForm = new Form2(row);
                inputForm.ShowDialog(this);
                return false;
            }
            else
            {
                output.AppendText("Syntax Error: Check input statement\n");
                return true;
            }
        }
			
        private bool OutputStatement(String line) {
            // OUTPUT
            
            if (Regex.IsMatch(line, "^\\s*VISIBLE\\s+.+!?$"))
            {
                if ((Regex.IsMatch(line, "^\\s*VISIBLE\\s+((BOTH\\s+SAEM|DIFFRINT))")))
                {
                    String mathexpr = line.Replace("VISIBLE", " ");
                    mathexpr = mathexpr.Trim();

                    if (mathexpr[mathexpr.Length - 1].CompareTo('!') == 0)
                    {
                        mathexpr = mathexpr.Replace("!", " ");
                        mathexpr = mathexpr.Trim();



                        output.AppendText(this.ComparisonOp(mathexpr, ""));
                    }
                    else
                    {
                        output.AppendText(this.ComparisonOp(mathexpr, ""));
                    }
                }
                else if ((Regex.IsMatch(line, "^\\s*VISIBLE\\s+((SUM\\s+OF)|(DIFF\\s+OF)|(PRODUKT\\s+OF)|(QUOSHUNT\\s+OF)|(MOD\\s+OF)|(BIGGR\\s+OF)|(SMALLR\\s+OF))!?")))
                {
                    Console.WriteLine("EXPR");
                    String mathexpr = line.Replace("VISIBLE", " ");
                    mathexpr = mathexpr.Trim();
                    
                    if (mathexpr[mathexpr.Length - 1].CompareTo('!') == 0)
                    {
                        mathexpr = mathexpr.Replace("!", " ");
                        mathexpr = mathexpr.Trim();

                        

                        output.AppendText(this.ArithmeticOp(mathexpr, ""));
                    }
                    else
                    {
                        output.AppendText(this.ArithmeticOp(mathexpr, ""));
                    }

             
                }else if ((Regex.IsMatch(line, "^\\s*VISIBLE\\s+((BOTH\\s+SAEM|DIFFRINT|BOTH\\s+OF|WON\\s+OF|EITHER\\s+OF))"))){
                    String mathexpr = line.Replace("VISIBLE", " ");
                    mathexpr = mathexpr.Trim();

                    if (mathexpr[mathexpr.Length - 1].CompareTo('!') == 0)
                    {
                        mathexpr = mathexpr.Replace("!", " ");
                        mathexpr = mathexpr.Trim();



                        output.AppendText(this.BoolOp(mathexpr, ""));
                    }
                    else
                    {
                        output.AppendText(this.BoolOp(mathexpr, ""));
                    }
                }
                //PRINT VAR
                else if ((Regex.IsMatch(line, "^\\s*VISIBLE\\s+[a-zA-Z][a-zA-Z0-9_]*!?$")))
                {

                    Regex r = new Regex("^\\s*(?<output>VISIBLE)\\s+(?<varident>[a-zA-Z][a-zA-Z0-9_]*)(?<bang>!)?$");
                    Match m = r.Match(line);
                    
                    table1.Rows.Add(m.Groups["output"].ToString(), "STANDARD OUTPUT\n");
                    String value = "";
                    if (symbolTable.TryGetValue(m.Groups["varident"].Value, out value))
                    {
                        //*
                        if (String.IsNullOrWhiteSpace(m.Groups["bang"].ToString()))
                        {
                            if (!String.IsNullOrWhiteSpace(symbolTable[m.Groups["varident"].ToString()]))
                            {
                                output.AppendText(symbolTable[m.Groups["varident"].ToString()]);
                            }
                            else
                            {
                                output.AppendText("Cannot implicitly cast nil\n");
                            }
                        }
                        else
                        {
                            if (!String.IsNullOrWhiteSpace(symbolTable[m.Groups["varident"].ToString()]))
                            {
                                output.AppendText(symbolTable[m.Groups["varident"].ToString()]);
                            }
                            else
                            {
                                output.AppendText("Cannot implicitly cast nil\n");
                            }
                        }
                        
                        table1.Rows.Add(m.Groups["varident"].ToString(), "VARIABLE INDENTIFIER");
                    }
                    else
                    {
                        output.AppendText(m.Groups["varident"].ToString() + " undeclared.\n" );
                    }
                }
                //PRINT LITERAL
                else
                {

                    Regex r = new Regex("^\\s*(?<output>VISIBLE)\\s+(?<literal>(" + @"(?<yarn>\""[^\""]+\"")" + "|" + "(?<numbar>-?[0-9]+\\.[0-9]*)" + "|" + "(?<numbr>-?[0-9]+)" + "))(?<bang>!)?$");
                    Match m = r.Match(line.Trim());
                    String y = "";
                    
                    table1.Rows.Add(m.Groups["output"].ToString(), "STANDARD OUTPUT");
                    if (!String.IsNullOrWhiteSpace(m.Groups["literal"].ToString()))
                    {

                        String[] literal = {    @"(?<yarn>\""[^\""]+\"")",
                                    "(?<numbar>-?[0-9]+\\.[0-9]*)",
                                    "(?<numbr>-?[0-9]+)"
                               };

                        foreach (String lit in literal)
                        {
                            Regex s = new Regex(lit);
                            Match n = s.Match(m.Groups["literal"].ToString());
                            if (n.Success)
                            {
                                if (!String.IsNullOrWhiteSpace(n.Groups["numbr"].ToString()))
                                {
                                    
                                   table1.Rows.Add(n.Groups["numbr"].ToString(), "NUMBR literal");
                                }

                                else if (!String.IsNullOrWhiteSpace(n.Groups["numbar"].ToString()))
                                {
                                    
                                    table1.Rows.Add(n.Groups["numbar"].ToString(), "NUMBAR literal");
                                }

                                else if (!String.IsNullOrWhiteSpace(n.Groups["yarn"].ToString()))
                                {
                                    String[] yarn = n.Groups["yarn"].ToString().Split('"');
                                    y = yarn[1];
                                    
                                    table1.Rows.Add("\"", "YARN delimiter");
                                    
                                    table1.Rows.Add(yarn[1], "YARN literal");
                                    
                                    table1.Rows.Add("\"", "YARN delimiter");
                                }
                                break;
                            }
                        }

                        if (String.IsNullOrWhiteSpace(m.Groups["bang"].ToString()))
                        {

                            if (String.IsNullOrWhiteSpace(y))
                            {
                                output.AppendText(m.Groups["literal"].ToString() + "\n");
                            }
                            else
                            {
                                output.AppendText(y + "\n");
                            }

                        }
                        else
                        {
                            if (String.IsNullOrWhiteSpace(y))
                            {
                                output.AppendText(m.Groups["literal"].ToString()); 
                            }
                            else
                            {
                                output.AppendText(y);
                            }
                        }
                    }
                    else
                    {
                        output.AppendText(line);
                        output.AppendText(" Missing expression\n");
                    }
                }
                return false;
            }
            else
            {
                output.AppendText("Error: Check output statement\n");
                return true;
            }
        }

        private void TypeCastMaek(String line) {
            // TYPECASTING
            Match num;
            Match m = Regex.Match(line, "MAEK\\s+(?<value>[a-zA-Z]\\w*|\\\"(.*?)\\\"|(\\-|\\+)?[0-9]+(\\.[0-9]*)?|WIN|FAIL)\\s+A\\s+(?<type>TROOF|NUMBR|NUMBAR|YARN|NOOB)");
            if (m.Success)
            {
                // VAR
                int row;
                string value = "";
                if (!symbolTable.TryGetValue(m.Groups["value"].Value, out value))
                {
                    this.output.AppendText("\nERROR: Variable identifier {" + m.Groups["value"].Value + "} does not exist.");
                    return;
                }
                else
                { // store value in this index
                    row = this.GetRowIndexByValue(table2, m.Groups["value"].Value);
                }
                if (symbolTable[m.Groups["value"].Value] != "WIN" && symbolTable[m.Groups["value"].Value] != "FAIL" && Regex.IsMatch(symbolTable[m.Groups["value"].Value], "[^\\d\\.\\+-]") && (m.Groups["type"].Value == "NUMBR" || m.Groups["type"].Value == "NUMBAR")) //if casting as a numerical type
                {
                    this.output.AppendText("\nERROR: Variable identifier {" + m.Groups["value"].Value + "} contains invalid characters.");
                    return;
                }
                else{
                    table1.Rows.Add("MAEK", "TYPE CAST");
                    lexemes.AddLast("MAEK");
                    // variable identifier
                    this.checkValue(m.Groups["value"].Value);
                    if (m.Groups["type"].Value == "NUMBR" && Regex.IsMatch(symbolTable[m.Groups["value"].Value], "(?<wholeNum>[-\\+]?\\d+)\\.\\d+"))
                    { //if cast from numbar to numbr, get only the whole number part
                        num = Regex.Match(symbolTable[m.Groups["value"].Value], "(?<wholeNum>[-\\+]?\\d+)\\.\\d+");
                        table2.Rows[row].Cells[2].Value = num.Groups["wholeNum"].Value;
                        symbolTable[m.Groups["value"].Value] = num.Groups["wholeNum"].Value; ;
                    }
                    else if (m.Groups["type"].Value == "NUMBAR" && Regex.IsMatch(symbolTable[m.Groups["value"].Value], "^[-\\+]?\\d+$"))
                    { //if cast from numbr to numbar, append ".0"
                        table2.Rows[row].Cells[2].Value = symbolTable[m.Groups["value"].Value] + ".0";
                        symbolTable[m.Groups["value"].Value] = symbolTable[m.Groups["value"].Value] + ".0"; ;
                    }
                    else if (m.Groups["type"].Value == "NUMBAR" && symbolTable[m.Groups["value"].Value] == "WIN")
                    {
                        table2.Rows[row].Cells[2].Value = "1.0";
                        symbolTable[m.Groups["value"].Value] = "1.0";
                    }
                    else if (m.Groups["type"].Value == "NUMBAR" && symbolTable[m.Groups["value"].Value] == "FAIL")
                    {
                        table2.Rows[row].Cells[2].Value = "0.0";
                        symbolTable[m.Groups["value"].Value] = "0.0";
                    }
                    else if (m.Groups["type"].Value == "NUMBR" && symbolTable[m.Groups["value"].Value] == "WIN")
                    {
                        table2.Rows[row].Cells[2].Value = "1";
                        symbolTable[m.Groups["value"].Value] = "1";
                    }
                    else if (m.Groups["type"].Value == "NUMBR" && symbolTable[m.Groups["value"].Value] == "FAIL")
                    {
                        table2.Rows[row].Cells[2].Value = "0";
                        symbolTable[m.Groups["value"].Value] = "0";
                    }
                    else if (m.Groups["type"].Value == "TROOF")
                    {
                        if (symbolTable[m.Groups["value"].Value] == "0") // IF VALUE IS 0, TROOF VALUE IS FAIL
                        {
                            table2.Rows[row].Cells[2].Value = "FAIL";
                            symbolTable[m.Groups["value"].Value] = "FAIL";
                        }
                        else if (!String.IsNullOrEmpty(symbolTable[m.Groups["value"].Value])) // IF VARIABLE HAS A VALUE THAT IS NOT 0, TROOF VALUE IS WIN
                        {
                            table2.Rows[row].Cells[2].Value = "WIN";
                            symbolTable[m.Groups["value"].Value] = "WIN";
                        }
                        else // VARIABLE CONTAINS NO VALUE
                        {
                            table2.Rows[row].Cells[2].Value = "FAIL";
                            symbolTable[m.Groups["value"].Value] = "FAIL";
                        }
                    }
                    else if (m.Groups["type"].Value == "NOOB") // IF CAST AS NOOB, REMOVE VALUES, NULL
                    {
                        table2.Rows[row].Cells[2].Value = "";
                        symbolTable[m.Groups["value"].Value] = "";
                    }
                    lexemes.AddLast(m.Groups["value"].Value);
                    table1.Rows.Add("A", "OPERATOR");
                    lexemes.AddLast("A");
                    table1.Rows.Add(m.Groups["type"].Value, "DATA TYPE");
                    lexemes.AddLast(m.Groups["type"].Value);
                    //////////////////// change data type
                    table2.Rows[row].Cells[1].Value = m.Groups["type"].Value;
// CHANGE VALUE
                }
            }
        }
			
        private String ArithmeticOp(String line, String var) {
            
            Regex r = new Regex("(?<op>(SUM OF|DIFF OF|PRODUKT OF|QUOSHUNT OF|MOD OF|BIGGR OF|SMALLR OF))");
            int cnt = 0, opCounter=0, anCounter=0;
            //opCounter -> SUM OF, DIFF OF, etc.
            //anCounter -> AN
            //cnt -> total count of tokens

            foreach (Match ItemMatch in r.Matches(line))
            {
                opCounter++;
                cnt++;
            }
            //add code here to match variable and number literals 
            //put in lexemes table
            r = new Regex("(?<op>AN)");

            foreach (Match ItemMatch in r.Matches(line))
            {
                anCounter++;
            }


            if (opCounter!=anCounter)
            {
                arithStat = 1;
                st.Push("Syntax Error: Check number of operator\n");
                return st.Pop();
            }
            else
            {  //If no error is detected, proceed here
               
                String[] result = line.Split(' ');
                String[] temp = new String[result.Length];

                int counter = 0;
                int litCtr = 0; //LITERAL/VAR COUNTER
                for (int i = 0; i < result.Length; i++)
                {
                    if (result[i] == "SUM" || result[i] == "DIFF" || result[i] == "PRODUKT" || result[i] == "QUOSHUNT" || result[i] == "MOD" || result[i] == "BIGGR" || result[i] == "SMALLR")
                    {
                        temp[counter] = result[i] + " " + result[i + 1];
                        i++;
                        //Console.WriteLine("temp1=" + temp[counter]);
                    }
                    else
                    {
                        temp[counter] = result[i];
                        if (temp[counter].CompareTo("AN") != 0 && !String.IsNullOrWhiteSpace(temp[counter])) { litCtr++; }
                        //Console.WriteLine("temp2=" + temp[counter]);
                    }
                    counter++;
                }

                //
                String[] combined = new String[counter];
                for (int i = 0; i < counter; i++)
                {
                    combined[i] = temp[i];
                    Regex a = new Regex("(?<op>(SUM OF|DIFF OF|PRODUKT OF|QUOSHUNT OF|MOD OF|BIGGR OF|SMALLR OF))");
                    Match k = a.Match(combined[i]);
                    Regex c = new Regex("(?<num>[0-9]+)");
                    Match l = c.Match(combined[i]);
                    Regex d = new Regex("(?<var>[a-zA-Z][a-zA-Z_0-9]*)");
                    Match m = d.Match(combined[i]);
                    if (combined[i] == "AN")
                    {
                        table1.Rows.Add(combined[i], "CONJUNCTOR");
                        lexemes.AddLast(combined[i]);
                    }
                    else if (combined[i].Contains("."))
                    {
                        table1.Rows.Add(combined[i], "NUMBAR Literal");
                        lexemes.AddLast(combined[i]);
                    }
                    else if (!String.IsNullOrEmpty(k.Groups["op"].ToString()))
                    {
                        table1.Rows.Add(combined[i], "MATH OPERATION");
                        lexemes.AddLast(combined[i]);
                    }
                    else if (!String.IsNullOrEmpty(l.Groups["num"].ToString()))
                    {
                        table1.Rows.Add(combined[i], "NUMBR Literal");
                        lexemes.AddLast(combined[i]);
                    }
                    else if (!String.IsNullOrEmpty(m.Groups["var"].ToString()))
                    {
                        table1.Rows.Add(combined[i], "Variable Identifier");
                        lexemes.AddLast(combined[i]);
                    }
                    else
                    {

                        Console.WriteLine("Not inside the shit");
                    }
                }//"combined" array contains the whole expression


                for (int i = counter - 1; i >= 0; i--)
                {
                    if (combined[i] == "SUM OF")
                    {
                        
                        String n1 = st.Pop(), n2 = st.Pop();
                        int cont1 = 0, cont2 = 0;
                        float cont3 = 0, cont4 = 0;
                        bool isFloat = false;

                        if (n1 == "WIN")
                        {
                            n1 = "1";
                        }
                        else if (n1 == "FAIL")
                        {
                            n1 = "0";
                        }

                        if (n2 == "WIN")
                        {
                            n2 = "1";
                        }
                        else if (n2 == "FAIL")
                        {
                            n2 = "0";
                        }

                        if (n1.Contains(".")) { cont3 = float.Parse(n1); isFloat = true; }
                        else { cont1 = int.Parse(n1); }

                        if (n2.Contains(".")) { cont4 = float.Parse(n2); isFloat = true; }
                        else { cont2 = int.Parse(n2); }

                        

                        if (!isFloat)
                        {
                            st.Push((cont1 + cont2).ToString());
                            
                        }
                        else if (isFloat)
                        {
                            if (cont3.CompareTo(0) != 0 && cont4.CompareTo(0) != 0) //si cont 3 ay string at equal siya kay zero
                            {
                                st.Push((cont3 + cont4).ToString());
                                //Console.WriteLine("yung sa cont 3 - cont 4");
                            }
                            else if (cont3.CompareTo(0) == 0)
                            {
                                //int val1 = cont1;
                                float val = (float)cont1 + cont4;
                                
                                st.Push(val.ToString());
                                //Console.WriteLine("yung sa cont 1 - cont 4");
                            }

                            else
                            {
                                //Console.WriteLine("yung sa cont 3 - cont 2");
                                st.Push((cont3 + cont2).ToString());
                            }
                        }
                    }
                    else if (combined[i] == "DIFF OF")
                    {
                        //st.Push(st.Pop() - st.Pop());
                        String n1 = st.Pop(), n2 = st.Pop();
                        int cont1 = 0, cont2 = 0;
                        float cont3 = 0, cont4 = 0;
                        bool isFloat = false;
                        if (n1 == "WIN")
                        {
                            n1 = "1";
                        }
                        else if (n1 == "FAIL")
                        {
                            n1 = "0";
                        }

                        if (n2 == "WIN")
                        {
                            n2 = "1";
                        }
                        else if (n2 == "FAIL")
                        {
                            n2 = "0";
                        }
                        if (n1.Contains(".")) { cont3 = float.Parse(n1); isFloat = true; }
                        else { cont1 = int.Parse(n1); }

                        if (n2.Contains(".")) { cont4 = float.Parse(n2); isFloat = true; }
                        else { cont2 = int.Parse(n2); }

                        if (!isFloat)
                        {
                            st.Push((cont1 - cont2).ToString());
                            //Console.WriteLine("int lahat");
                        }
                        else if (isFloat)
                        {
                            if (cont3.CompareTo(0) != 0 && cont4.CompareTo(0) != 0) //si cont 3 ay string at equal siya kay zero
                            {
                                st.Push((cont3 - cont4).ToString());
                                Console.WriteLine("yung sa cont 3 - cont 4");
                            }
                            else if (cont3.CompareTo(0) == 0)
                            {

                                //int val1 = cont1;
                                float val = (float)cont1 - cont4;
                                //Console.WriteLine(val2);
                                //Console.WriteLine(cont4);

                                st.Push(val.ToString());
                                Console.WriteLine("yung sa cont 1 - cont 4");

                            }
                            else
                            {
                                Console.WriteLine("yung sa cont 3 - cont 2");
                                st.Push((cont3 - cont2).ToString());
                            }
                        }
                    }
                    else if (combined[i] == "PRODUKT OF")
                    {
                        //st.Push(st.Pop() * st.Pop());
                        String n1 = st.Pop(), n2 = st.Pop();
                        int cont1 = 0, cont2 = 0;
                        float cont3 = 0, cont4 = 0;
                        bool isFloat = false;
                        if (n1 == "WIN")
                        {
                            n1 = "1";
                        }
                        else if (n1 == "FAIL")
                        {
                            n1 = "0";
                        }

                        if (n2 == "WIN")
                        {
                            n2 = "1";
                        }
                        else if (n2 == "FAIL")
                        {
                            n2 = "0";
                        }
                        if (n1.Contains(".")) { cont3 = float.Parse(n1); isFloat = true; }
                        else { cont1 = int.Parse(n1); }

                        if (n2.Contains(".")) { cont4 = float.Parse(n2); isFloat = true; }
                        else { cont2 = int.Parse(n2); }

                        if (!isFloat)
                        {
                            st.Push((cont1 * cont2).ToString());
                            //Console.WriteLine("int lahat");
                        }
                        else if (isFloat)
                        {
                            if (cont3.CompareTo(0) != 0 && cont4.CompareTo(0) != 0) //si cont 3 ay string at equal siya kay zero
                            {
                                st.Push((cont3 * cont4).ToString());
                                Console.WriteLine("yung sa cont 3 - cont 4");
                            }
                            else if (cont3.CompareTo(0) == 0)
                            {
                                //int val1 = cont1;
                                float val = (float)cont1 * cont4;
                                //Console.WriteLine(val2);
                                //Console.WriteLine(cont4);
                                st.Push(val.ToString());
                                Console.WriteLine("yung sa cont 1 - cont 4");
                            }
                            else
                            {
                                Console.WriteLine("yung sa cont 3 - cont 2");

                                st.Push((cont3 * cont2).ToString());
                            }
                        }
                    }

                    else if (combined[i] == "QUOSHUNT OF")
                    {
                        //st.Push(st.Pop() / st.Pop());
                        String n1 = st.Pop(), n2 = st.Pop();
                        int cont1 = 0, cont2 = 0;
                        float cont3 = 0, cont4 = 0;
                        bool isFloat = false;
                        if (n1 == "WIN")
                        {
                            n1 = "1";
                        }
                        else if (n1 == "FAIL")
                        {
                            n1 = "0";
                        }

                        if (n2 == "WIN")
                        {
                            n2 = "1";
                        }
                        else if (n2 == "FAIL")
                        {
                            n2 = "0";
                        }
                        if (n1.Contains(".")) { cont3 = float.Parse(n1); isFloat = true; }
                        else { cont1 = int.Parse(n1); }

                        if (n2.Contains(".")) { cont4 = float.Parse(n2); isFloat = true; }
                        else { cont2 = int.Parse(n2); }

                        if (!isFloat)
                        {
                            if (cont2 == 0)
                            {
                                st.Push(" Division by zero error");
                                break;
                            }
                            st.Push((cont1 / cont2).ToString());
                            //Console.WriteLine("int lahat");
                        }
                        else if (isFloat)
                        {
                            if (cont3.CompareTo(0) != 0 && cont4.CompareTo(0) != 0) //si cont 3 ay string at equal siya kay zero
                            {
                                st.Push((cont3 / cont4).ToString());
                                //Console.WriteLine("yung sa cont 3 - cont 4");
                            }
                            else if (cont3.CompareTo(0) == 0)
                            {
                                //int val1 = cont1;
                                float val = (float)cont1 / cont4;
                                //Console.WriteLine(val2);
                                //Console.WriteLine(cont4);

                                st.Push(val.ToString());
                                //Console.WriteLine("yung sa cont 1 - cont 4");
                            }
                            else
                            {
                                //Console.WriteLine("yung sa cont 3 - cont 2");
                                st.Push((cont3 / cont2).ToString());
                            }
                        }
                    }

                    else if (combined[i] == "MOD OF")
                    {
                        //st.Push(st.Pop() % st.Pop());
                        String n1 = st.Pop(), n2 = st.Pop();
                        int cont1 = 0, cont2 = 0;
                        float cont3 = 0, cont4 = 0;
                        bool isFloat = false;
                        if (n1 == "WIN")
                        {
                            n1 = "1";
                        }
                        else if (n1 == "FAIL")
                        {
                            n1 = "0";
                        }

                        if (n2 == "WIN")
                        {
                            n2 = "1";
                        }
                        else if (n2 == "FAIL")
                        {
                            n2 = "0";
                        }
                        if (n1.Contains(".")) { cont3 = float.Parse(n1); isFloat = true; }
                        else { cont1 = int.Parse(n1); }

                        if (n2.Contains(".")) { cont4 = float.Parse(n2); isFloat = true; }
                        else { cont2 = int.Parse(n2); }

                        if (!isFloat)
                        {
                            st.Push((cont1 % cont2).ToString());
                            //Console.WriteLine("int lahat");
                        }
                        else if (isFloat)
                        {
                            if (cont3.CompareTo(0) != 0 && cont4.CompareTo(0) != 0) //si cont 3 ay string at equal siya kay zero
                            {
                                st.Push((cont3 % cont4).ToString());
                                //Console.WriteLine("yung sa cont 3 - cont 4");
                            }
                            else if (cont3.CompareTo(0) == 0)
                            {

                                float val = (float)cont1 % cont4;

                                st.Push(val.ToString());

                            }
                            else
                            {

                                st.Push((cont3 % cont2).ToString());
                            }
                        }
                    }
                    else if (combined[i] == "BIGGR OF")
                    {
                        
                        String n1 = st.Pop(), n2 = st.Pop();
                        int cont1 = 0, cont2 = 0;
                        float cont3 = 0, cont4 = 0;
                        bool isFloat = false;
                        if (n1 == "WIN")
                        {
                            n1 = "1";
                        }
                        else if (n1 == "FAIL")
                        {
                            n1 = "0";
                        }

                        if (n2 == "WIN")
                        {
                            n2 = "1";
                        }
                        else if (n2 == "FAIL")
                        {
                            n2 = "0";
                        }
                        if (n1.Contains(".")) { cont3 = float.Parse(n1); isFloat = true; }
                        else { cont1 = int.Parse(n1); }

                        if (n2.Contains(".")) { cont4 = float.Parse(n2); isFloat = true; }
                        else { cont2 = int.Parse(n2); }

                        if (!isFloat)
                        {

                            if (cont1 <= cont2)
                            {
                                st.Push(cont2.ToString());
                            }
                            else
                            {
                                st.Push(cont1.ToString());
                            }
                        }
                        else if (isFloat)
                        {
                            if (cont3.CompareTo(0) != 0 && cont4.CompareTo(0) != 0) //si cont 3 ay string at equal siya kay zero
                            {

                                if (cont3 <= cont4)
                                {
                                    st.Push(cont4.ToString());
                                }
                                else
                                {
                                    st.Push(cont3.ToString());
                                }
                            }
                            else if (cont3.CompareTo(0) == 0)
                            {

                                if (cont4 <= cont1)
                                {
                                    st.Push(cont1.ToString());
                                }
                                else
                                {
                                    st.Push(cont4.ToString());
                                }

                            }
                            else
                            {

                                if (cont3 <= cont2)
                                {
                                    st.Push(cont2.ToString());
                                }
                                else
                                {
                                    st.Push(cont3.ToString());
                                }
                            }
                        }

                    }
                    else if (combined[i] == "SMALLR OF")
                    {
                        
                        String n1 = st.Pop(), n2 = st.Pop();
                        int cont1 = 0, cont2 = 0;
                        float cont3 = 0, cont4 = 0;
                        bool isFloat = false;
                        if (n1 == "WIN")
                        {
                            n1 = "1";
                        }
                        else if (n1 == "FAIL")
                        {
                            n1 = "0";
                        }

                        if (n2 == "WIN")
                        {
                            n2 = "1";
                        }
                        else if (n2 == "FAIL")
                        {
                            n2 = "0";
                        }
                        if (n1.Contains(".")) { cont3 = float.Parse(n1); isFloat = true; }
                        else { cont1 = int.Parse(n1); }

                        if (n2.Contains(".")) { cont4 = float.Parse(n2); isFloat = true; }
                        else { cont2 = int.Parse(n2); }

                        if (!isFloat)
                        {
                            //st.Push((cont1 * cont2).ToString());
                            //Console.WriteLine("int lahat");
                            if (cont1 >= cont2)
                            {
                                st.Push(cont2.ToString());
                            }
                            else
                            {
                                st.Push(cont1.ToString());
                            }
                        }
                        else if (isFloat)
                        {
                            if (cont3.CompareTo(0) != 0 && cont4.CompareTo(0) != 0) //si cont 3 ay string at equal siya kay zero
                            {
                                //st.Push((cont3 * cont4).ToString());
                                //Console.WriteLine("yung sa cont 3 - cont 4");
                                if (cont3 >= cont4)
                                {
                                    st.Push(cont4.ToString());
                                }
                                else
                                {
                                    st.Push(cont3.ToString());
                                }

                            }

                            else if (cont3.CompareTo(0) == 0)
                            {
                                //int val1 = cont1;
                                //float val = (float)cont1 * cont4;
                                //Console.WriteLine(val2);
                                //Console.WriteLine(cont4);

                                //st.Push(val.ToString());
                                //Console.WriteLine("yung sa cont 1 - cont 4");
                                if (cont4 >= cont1)
                                {
                                    st.Push(cont1.ToString());
                                }
                                else
                                {
                                    st.Push(cont4.ToString());
                                }

                            }
                            else
                            {
                                //Console.WriteLine("yung sa cont 3 - cont 2");
                                //st.Push((cont3 * cont2).ToString());
                                if (cont3 >= cont2)
                                {
                                    st.Push(cont2.ToString());
                                }
                                else
                                {
                                    st.Push(cont3.ToString());
                                }
                            }
                        }
                    }
                    else if (combined[i] == "AN")
                    {
                        continue;
                    }else if (combined[i]=="WIN" || combined[i] == "FAIL"){
                        st.Push(combined[i]);
                    }
                    else
                    {
                        Match m1 = Regex.Match(combined[i], "^(?![A-Za-z]+)(-?[0-­9]+|-?[0-­9]+\\.[0-9]*)$");
                        if ((anCounter + 1) != litCtr)
                        {
                            st.Push("Missing operand");
                            //Console.WriteLine("KULANG");
                            break;
                        }
                        if (m1.Success)
                        {//if combined[i] is a number
                         //st.Push(int.Parse(combined[i]));
                            st.Push(combined[i]);
                            //Console.WriteLine(combined[i]);
                        }
                        else
                        {
                            String nigga = "";
                            if (!symbolTable.TryGetValue(combined[i], out nigga))
                            {
                                this.output.AppendText("Variable not found");
                            }
                            else
                            {
                                symbolTable.TryGetValue(combined[i], out nigga);
                                
                                st.Push(nigga);
                            }
                        }
                    }
                }
                
                cnt = 0;
                opCounter = 0;
                anCounter = 0;
                counter = 0;

            }
            return (st.Pop());

            

        }//end of ArithmeticOp

        private String BoolOp(String line, String var) {
            // boolean operations
            int cnt = 0, opCounter = 0, anCounter = 0;
            String temp1, temp2 = "";

            Match m1 = Regex.Match(line, "(?<boolOp>BOTH\\s+OF|EITHER\\s+OF|WON\\s+OF)\\s+(?<value1>[a-zA-Z]\\w*|\\\"(.*?)\\\"|(\\-|\\+)?[0-9]+(\\.[0-9]*)?|WIN|FAIL)\\s+AN\\s+(?<value2>[a-zA-Z]\\w*|\\\"(.*?)\\\"|(\\-|\\+)?[0-9]+(\\.[0-9]*)?|WIN|FAIL)");
            Match m2 = Regex.Match(line, "NOT\\s+(?<value1>[a-zA-Z]\\w*|\\\"(.*?)\\\"|(\\-|\\+)?[0-9]+(\\.[0-9]*)?|WIN|FAIL)");
            Match m3 = Regex.Match(line, "(?<boolOp>ANY|ALL)\\s+(?<values>.+)\\s+(?<delim>MKAY)");
            Match m0 = Regex.Match(line, "(BOTH OF|EITHER OF|WON OF)");
            if (m0.Success)
            {
                if (m1.Success)
                {
                    table1.Rows.Add(m1.Groups["boolOp"].Value, "BOOLEAN OPERATION");
                    lexemes.AddLast(m1.Groups["boolOp"].Value);
                    this.checkValue(m1.Groups["value1"].Value);
                    lexemes.AddLast(m1.Groups["value1"].Value);
                    table1.Rows.Add("AN", "OPERATOR");
                    lexemes.AddLast("AN");
                    this.checkValue(m1.Groups["value2"].Value);
                    lexemes.AddLast(m1.Groups["value2"].Value);
                    Regex r = new Regex("(?<op>(BOTH OF|EITHER OF|WON OF))");

                    foreach (Match ItemMatch in r.Matches(line))
                    {
                        opCounter++;
                        cnt++;
                    }

                    r = new Regex("(?<op>AN)");

                    foreach (Match ItemMatch in r.Matches(line))
                    {
                        anCounter++;
                    }

                    if (opCounter != anCounter)
                    {
                        booleanStat = 1;
                        st1.Push("Syntax Error: Check number of operator\n");
                        return st1.Pop();
                    }
                    else
                    {

                        String[] result = line.Split(' ');
                        String[] temp = new String[result.Length];

                        int counter = 0;
                        for (int i = 0; i < result.Length; i++)
                        {
                            if (result[i] == "BOTH" || result[i] == "EITHER" || result[i] == "WON")
                            {
                                temp[counter] = result[i] + " " + result[i + 1];
                                i++;
                            }
                            else
                            {
                                temp[counter] = result[i];

                            }
                            counter++;
                        }


                        String[] combined = new String[counter];
                        for (int i = 0; i < counter; i++)
                        {
                            combined[i] = temp[i];

                        }//"combined" array contains the whole expression

                        for (int i = counter - 1; i >= 0; i--)
                        {

                            if (combined[i] == "BOTH OF")
                            {

                                temp1 = st1.Pop();
                                temp2 = st1.Pop();

                                if (temp1 == "WIN" && temp2 == "WIN")
                                {
                                    st1.Push("WIN");
                                }
                                else
                                {
                                    st1.Push("FAIL");
                                }



                            }
                            else if (combined[i] == "EITHER OF")
                            {
                                temp1 = st1.Pop();
                                temp2 = st1.Pop();

                                if (temp1 == "FAIL" && temp2 == "FAIL")
                                {
                                    st1.Push("FAIL");
                                }
                                else
                                {
                                    st1.Push("WIN");
                                }
                            }
                            else if (combined[i] == "WON OF")
                            {
                                temp1 = st1.Pop();
                                temp2 = st1.Pop();

                                if (temp1 != temp2)
                                {
                                    st1.Push("WIN");
                                }
                                else
                                {
                                    st1.Push("FAIL");
                                }
                            }
                            else if (combined[i] == "NOT")
                            {
                                temp1 = st1.Pop();
                                if (temp1 == "WIN")
                                {
                                    st1.Push("FAIL");
                                }
                                else
                                {
                                    st1.Push("WIN");
                                }
                            }
                            else if (combined[i] == "AN")
                            {

                                continue;

                            }
                            else
                            {
                                Match m4 = Regex.Match(combined[i], "^(?!-?[0-9]+)(WIN|FAIL)$");

                                if (m4.Success)//if combined[i] is WIN or FAIL
                                {
                                    st1.Push(combined[i]);
                                }
                                else
                                {
                                    Match m5 = Regex.Match(combined[i], "^(?![WIN|FAIL])([A-Za-z0-9_]+)$");

                                    if (m5.Success)
                                    {//if combined[i] is a variable

                                        String nigga = "";
                                        if (!symbolTable.TryGetValue(combined[i], out nigga))
                                        {
                                            output.AppendText("Error: Variable not found\n");
                                        }
                                        else
                                        {
                                            symbolTable.TryGetValue(combined[i], out nigga);
                                            st1.Push(nigga);
                                        }

                                    }
                                    else
                                    {

                                        output.AppendText("Error: Variable not found\n");


                                    }
                                }
                                //match if variable, WIN or FAIL
                            }

                        }//end of for

                        cnt = 0;
                        opCounter = 0;
                        anCounter = 0;
                        counter = 0;

                    }


                }
                else if (m2.Success)
                {
                    table1.Rows.Add("NOT", "BOOL OPERATION");
                    lexemes.AddLast("NOT");
                    this.checkValue(m2.Groups["value1"].Value);
                    lexemes.AddLast(m2.Groups["value1"].Value);

                }
                else if (m3.Success)
                {
                    table1.Rows.Add(m3.Groups["boolOp"].Value, "BOOLEAN OPERATION");
                    lexemes.AddLast(m3.Groups["boolOp"].Value);
                    String str = m3.Groups["values"].Value;
                    string[] values = Regex.Split(str, "AN");
                    int i;
                    for (i = 0; i < values.Length; i++)
                    {
                        Match m4 = Regex.Match(values[i], "(?<value>[a-zA-Z]\\w*|\\\"(.*?)\\\"|(\\-|\\+)?[0-9]+(\\.[0-9]*)?|WIN|FAIL)");
                        if (m4.Success)
                        {
                            this.checkValue(m4.Groups["value"].Value);
                            lexemes.AddLast(m4.Groups["value"].Value);
                        }
                        if (i != values.Length - 1)
                        {
                            table1.Rows.Add("AN", "OPERATOR");
                            lexemes.AddLast("AN");
                        }
                    }
                    table1.Rows.Add("MKAY", "DELIMITER");
                    lexemes.AddLast("MKAY");

                }
                String temporary = st1.Pop();

                symbolTable["IT"] = temporary;
                return (temporary);
            }
            else
            {
                return ("Syntax Error.\n");
            }
            

        }
			
        private void ConcatStatement(String line) {
            // Concatenation statement
            Match yarnLit;
            Match m = Regex.Match(line, "SMOOSH\\s+(?<values>.+)");
            if (m.Success)
            {
                table1.Rows.Add("SMOOSH", "CONCATENATION");
                lexemes.AddLast("SMOOSH");
                String str = m.Groups["values"].Value;
                string[] values = Regex.Split(str, "AN");
                symbolTable["IT"] = "\"";
                int i;
                for (i = 0; i < values.Length; i++)
                {
                    values[i] = values[i].Trim();
                    Match m1 = Regex.Match(values[i], "^(?<value>[a-zA-Z]\\w*|\\\"(.*?)\\\"|(\\-|\\+)?[0-9]+(\\.[0-9]*)?|WIN|FAIL)$");
                    if (!values[i].Contains("MKAY"))
                    {
                        if (m1.Success)
                        {
                            this.checkValue(m1.Groups["value"].Value);
                            lexemes.AddLast(m1.Groups["value"].Value);
                        }
                        if (i != values.Length - 1)
                        {
                            table1.Rows.Add("AN", "OPERATOR");
                            lexemes.AddLast("AN");
                        }
                        if (Regex.IsMatch(values[i], "^[a-zA-Z]\\w*$"))
                        {
                            string value1 = "";
                            if (!symbolTable.TryGetValue(values[i], out value1))
                            {
                                this.output.AppendText("\nERROR: Variable identifier {" + m1.Groups["value"].Value + "} does not exist.");
                                return;
                            }
                            else
                            {
                                values[i] = symbolTable[m1.Groups["value"].Value];
                            }
                        }

                        yarnLit = Regex.Match(values[i], "\"(?<yarnLiteral>.*)\"");
                        if (yarnLit.Success) values[i] = yarnLit.Groups["yarnLiteral"].Value;
                        if (values[i].Trim() == "MKAY") break;
                        values[i] = values[i].Replace(":)", "\n"); //escape characters
                        values[i] = values[i].Replace(":>", "\t"); //escape characters
                        values[i] = values[i].Replace("::", ":"); //escape characters
                        symbolTable["IT"] = symbolTable["IT"] + values[i]; //appending
                    }
                    else {
                        String[] str1 = values[i].Split(' ');
                        foreach (String s in str1) {
                            if (s.Length != 0)
                            {
                                m1 = Regex.Match(s, "^(?<value>[a-zA-Z]\\w*|\\\"(.*?)\\\"|(\\-|\\+)?[0-9]+(\\.[0-9]*)?|WIN|FAIL)$");
                                if (m1.Success && s.Trim() != "MKAY")
                                {
                                    this.checkValue(m1.Groups["value"].Value);
                                    lexemes.AddLast(m1.Groups["value"].Value);
                                    if (Regex.IsMatch(s, "^[a-zA-Z]\\w*$") && !Regex.IsMatch(s, "(WIN|FAIL)"))
                                    {
                                        string value1 = "";
                                        if (!symbolTable.TryGetValue(s, out value1))
                                        {
                                            this.output.AppendText("\nERROR: Variable identifier {" + s + "} does not exist.");
                                            return;
                                        }
                                        else
                                        {
                                            symbolTable["IT"] = symbolTable["IT"] + symbolTable[s];
                                        }
                                    }
                                    else
                                    {
                                        yarnLit = Regex.Match(s, "\"(?<yarnLiteral>.*)\"");
                                        if (yarnLit.Success) symbolTable["IT"] = symbolTable["IT"] + yarnLit.Groups["yarnLiteral"].Value;
                                    }
                                }
                                else
                                {
                                    table1.Rows.Add("MKAY", "DELIMITER");
                                    lexemes.AddLast("MKAY");
                                    return;
                                }
                            }
                        }//end of foreach
                    }
                }// end of for loop
            }
            symbolTable["IT"] = symbolTable["IT"] + "\""; 
        }

        private String ComparisonOp(String line, String var) {
            Match m0 = Regex.Match(line, "(BOTH SAEM|DIFFIRINT)");
            Match m1 = Regex.Match(line, "(?<compOp0>BOTH\\s+SAEM|DIFFRINT)\\s+(?<value1>[a-zA-Z]\\w*|\\\"(.*?)\\\"|(\\-|\\+)?[0-9]+(\\.[0-9]*)?|WIN|FAIL)\\s+AN\\s+(?<value2>[a-zA-Z]\\w*|\\\"(.*?)\\\"|(\\-|\\+)?[0-9]+(\\.[0-9]*)?|WIN|FAIL)");
            Match m2 = Regex.Match(line, "(?<compOp1>BOTH\\s+SAEM|DIFFRINT)\\s+(?<value1>[a-zA-Z]\\w*|\\\"(.*?)\\\"|(\\-|\\+)?[0-9]+(\\.[0-9]*)?|WIN|FAIL)\\s+AN\\s+(?<compOp2>BIGGR|SMALLR)\\s+OF\\s+(?<value2>[a-zA-Z]\\w*|\\\"(.*?)\\\"|(\\-|\\+)?[0-9]+(\\.[0-9]*)?|WIN|FAIL)\\s+AN\\s+(?<value3>[a-zA-Z]\\w*|\\\"(.*?)\\\"|(\\-|\\+)?[0-9]+(\\.[0-9]*)?|WIN|FAIL)");
            if (m0.Success)
            {
                if (m2.Success)
                {
                    table1.Rows.Add(m2.Groups["compOp1"].Value, "COMPARISON OPERATION");
                    lexemes.AddLast(m2.Groups["compOp1"].Value);
                    this.checkValue(m2.Groups["value1"].Value);
                    lexemes.AddLast(m2.Groups["value1"].Value);
                    table1.Rows.Add("AN", "OPERATOR");
                    lexemes.AddLast("AN");
                    table1.Rows.Add(m2.Groups["compOp2"].Value, "COMPARISON OPERATION");
                    lexemes.AddLast(m2.Groups["compOp2"].Value);
                    table1.Rows.Add("OF", "OPERATOR");
                    lexemes.AddLast("OF");
                    this.checkValue(m2.Groups["value2"].Value);
                    lexemes.AddLast(m2.Groups["value2"].Value);
                    table1.Rows.Add("AN", "OPERATOR");
                    lexemes.AddLast("AN");
                    this.checkValue(m2.Groups["value3"].Value);
                    lexemes.AddLast(m2.Groups["value3"].Value);

                    String[] result = line.Split(' ', '"');

                    String[] temp = new String[result.Length];

                    int counter = 0;
                    for (int i = 0; i < result.Length; i++)
                    {
                        if (result[i] == "BOTH" || result[i] == "BIGGR" || result[i] == "SMALLR")
                        {
                            temp[counter] = result[i] + " " + result[i + 1];
                            i++;
                        }
                        else
                        {
                            temp[counter] = result[i];

                        }
                        counter++;
                    }//put in array and update counters

                    String[] combined = new String[counter];
                    for (int i = 0; i < counter; i++)
                    {
                        combined[i] = temp[i];

                    }//"combined" array contains the whole expression

                    for (int i = counter - 1; i >= 0; i--)
                    {

                        if (combined[i] == "BOTH SAEM")
                        {

                            String temp1, temp2 = "";
                            temp1 = st.Pop();
                            temp2 = st.Pop();

                            if (temp1.Equals(temp2))
                            {
                                st.Push("WIN");
                            }
                            else
                            {
                                st.Push("FAIL");
                            }
                        }
                        else if (combined[i] == "DIFFRINT")
                        {
                            String temp1, temp2 = "";
                            temp1 = st.Pop();
                            temp2 = st.Pop();

                            if (!temp1.Equals(temp2))
                            {
                                st.Push("WIN");
                            }
                            else
                            {
                                st.Push("FAIL");
                            }
                        }
                        else if (combined[i] == "BIGGR OF")
                        {

                            String n1 = st.Pop(), n2 = st.Pop();
                            int cont1 = 0, cont2 = 0;
                            float cont3 = 0, cont4 = 0;
                            bool isFloat = false;

                            if (n1.Contains(".")) { cont3 = float.Parse(n1); isFloat = true; }
                            else { cont1 = int.Parse(n1); }

                            if (n2.Contains(".")) { cont4 = float.Parse(n2); isFloat = true; }
                            else { cont2 = int.Parse(n2); }

                            if (!isFloat)
                            {

                                if (cont1 <= cont2)
                                {
                                    st.Push(cont2.ToString());
                                }
                                else
                                {
                                    st.Push(cont1.ToString());
                                }
                            }
                            else if (isFloat)
                            {
                                if (cont3.CompareTo(0) != 0 && cont4.CompareTo(0) != 0) //si cont 3 ay string at equal siya kay zero
                                {

                                    if (cont3 <= cont4)
                                    {
                                        st.Push(cont4.ToString());
                                    }
                                    else
                                    {
                                        st.Push(cont3.ToString());
                                    }
                                }
                                else if (cont3.CompareTo(0) == 0)
                                {

                                    if (cont4 <= cont1)
                                    {
                                        st.Push(cont1.ToString());
                                    }
                                    else
                                    {
                                        st.Push(cont4.ToString());
                                    }

                                }
                                else
                                {

                                    if (cont3 <= cont2)
                                    {
                                        st.Push(cont2.ToString());
                                    }
                                    else
                                    {
                                        st.Push(cont3.ToString());
                                    }
                                }
                            }

                        }
                        else if (combined[i] == "SMALLR OF")
                        {

                            String n1 = st.Pop(), n2 = st.Pop();
                            int cont1 = 0, cont2 = 0;
                            float cont3 = 0, cont4 = 0;
                            bool isFloat = false;

                            if (n1.Contains(".")) { cont3 = float.Parse(n1); isFloat = true; }
                            else { cont1 = int.Parse(n1); }

                            if (n2.Contains(".")) { cont4 = float.Parse(n2); isFloat = true; }
                            else { cont2 = int.Parse(n2); }

                            if (!isFloat)
                            {
                                //st.Push((cont1 * cont2).ToString());
                                //Console.WriteLine("int lahat");
                                if (cont1 >= cont2)
                                {
                                    st.Push(cont2.ToString());
                                }
                                else
                                {
                                    st.Push(cont1.ToString());
                                }
                            }
                            else if (isFloat)
                            {
                                if (cont3.CompareTo(0) != 0 && cont4.CompareTo(0) != 0) //si cont 3 ay string at equal siya kay zero
                                {
                                    //st.Push((cont3 * cont4).ToString());
                                    //Console.WriteLine("yung sa cont 3 - cont 4");
                                    if (cont3 >= cont4)
                                    {
                                        st.Push(cont4.ToString());
                                    }
                                    else
                                    {
                                        st.Push(cont3.ToString());
                                    }

                                }

                                else if (cont3.CompareTo(0) == 0)
                                {
                                    //int val1 = cont1;
                                    //float val = (float)cont1 * cont4;
                                    //Console.WriteLine(val2);
                                    //Console.WriteLine(cont4);

                                    //st.Push(val.ToString());
                                    //Console.WriteLine("yung sa cont 1 - cont 4");
                                    if (cont4 >= cont1)
                                    {
                                        st.Push(cont1.ToString());
                                    }
                                    else
                                    {
                                        st.Push(cont4.ToString());
                                    }

                                }
                                else
                                {
                                    //Console.WriteLine("yung sa cont 3 - cont 2");
                                    //st.Push((cont3 * cont2).ToString());
                                    if (cont3 >= cont2)
                                    {
                                        st.Push(cont2.ToString());
                                    }
                                    else
                                    {
                                        st.Push(cont3.ToString());
                                    }
                                }
                            }
                        }

                        else if (combined[i] == "AN")
                        {

                            continue;

                        }
                        else
                        {

                            st.Push(combined[i]);

                        }

                    }//end of for

                }
                else if (m1.Success)
                {
                    table1.Rows.Add(m1.Groups["compOp0"].Value, "COMPARISON OPERATION");
                    lexemes.AddLast(m1.Groups["compOp0"].Value);
                    this.checkValue(m1.Groups["value1"].Value);
                    lexemes.AddLast(m1.Groups["value1"].Value);
                    table1.Rows.Add("AN", "OPERATOR");
                    lexemes.AddLast("AN");
                    this.checkValue(m1.Groups["value2"].Value);
                    lexemes.AddLast(m1.Groups["value2"].Value);

                    String[] result = line.Split(' ', '"');
                    String[] temp = new String[result.Length];

                    int counter = 0;
                    for (int i = 0; i < result.Length; i++)
                    {
                        if (result[i] == "BOTH")
                        {
                            temp[counter] = result[i] + " " + result[i + 1];
                            i++;
                        }
                        else
                        {
                            temp[counter] = result[i];

                        }
                        counter++;
                    }//put in array and update counters

                    String[] combined = new String[counter];
                    for (int i = 0; i < counter; i++)
                    {
                        combined[i] = temp[i];
                    }//"combined" array contains the whole expression

                    for (int i = counter - 1; i >= 0; i--)
                    {

                        if (combined[i] == "BOTH SAEM")
                        {

                            String temp1, temp2 = "";
                            temp1 = st.Pop();
                            temp2 = st.Pop();

                            if (temp1 == temp2)
                            {
                                st.Push("WIN");
                            }
                            else
                            {
                                st.Push("FAIL");
                            }
                        }
                        else if (combined[i] == "DIFFRINT")
                        {
                            String temp1, temp2 = "";
                            temp1 = st.Pop();
                            temp2 = st.Pop();

                            if (temp1 != temp2)
                            {
                                st.Push("WIN");
                            }
                            else
                            {
                                st.Push("FAIL");
                            }
                        }

                        else if (combined[i] == "AN")
                        {

                            continue;

                        }
                        else
                        {

                            st.Push(combined[i]);

                        }

                    }//end of for

                }
                else
                {
                    output.AppendText("Error\n");
                    comparisonStat = 1;
                }
                
                String temporary = st.Pop();
                symbolTable["IT"] = temporary;
                return (temporary);
            }
            else
            {
                return ("Syntax Error.\n");
            }
            
        }

        private void LoopStatement(String line) {
            Match m = Regex.Match(line, "IM\\s+IN\\s+YR\\s+(?<label1>[a-zA-Z]+)\\s+(?<opr1>UPPIN|NERFIN)\\s+YR\\s+(?<var>[a-zA-Z]\\w*)\\s+((?<opr2>TIL|WILE)\\s+(?<expr>.+)\\s+)?(?<code>.+)\\s+IM\\s+OUTTA\\s+YR\\s+(?<label2>[a-zA-Z]+)");
            if (m.Success)
            {
                table1.Rows.Add("IM IN YR", "LOOP STATEMENT");
                lexemes.AddLast("IM IN YR");
                table1.Rows.Add(m.Groups["label1"].Value, "LOOP LABEL");
                lexemes.AddLast(m.Groups["label1"].Value);
                table1.Rows.Add(m.Groups["opr1"].Value, "OPERATION");
                lexemes.AddLast(m.Groups["opr1"].Value);
                table1.Rows.Add("YR", "KEYWORD");
                lexemes.AddLast("YR");
                table1.Rows.Add(m.Groups["var"].Value, "VARIABLE IDENTIFIER");
                lexemes.AddLast(m.Groups["var"].Value);
                if (!string.IsNullOrEmpty(m.Groups["opr2"].Value))
                {
                    table1.Rows.Add(m.Groups["opr2"].Value, "OPERATION");
                    lexemes.AddLast(m.Groups["opr2"].Value);
                }
                if (!string.IsNullOrEmpty(m.Groups["expr"].Value))
                {
                    this.checkExpr(m.Groups["expr"].Value, "");
                }
                this.checkString(m.Groups["code"].Value);
                table1.Rows.Add("IM OUTTA YR", "LOOP STATEMENT");
                lexemes.AddLast("IM OUTTA YR");
                table1.Rows.Add(m.Groups["label2"].Value, "LOOP LABEL");
                lexemes.AddLast(m.Groups["label2"].Value);
            }
        }

        private bool IfThenStatement(String line) {
            int line2 = 0;
            Dictionary<String, Regex> patterns = new Dictionary<String, Regex>
    {
        {"HAI", new Regex("^\\s*(?<start>HAI)(\\s+(?<version>\\d+(\\.\\d*)?))?(\\s+(?<comm>(.*)))?\\s*$")},
        {"KTHXBYE", new Regex("^\\s*(?<end>KTHXBYE)\\s*$")},

        {"BTW", new Regex("\\s*(?<scomm>BTW)(?<comm>\\s+(.*))?\\s*$")},
        {"OBTW", new Regex("^\\s*(?<commstart>OBTW)(\\s+(.*))?\\s*")},
        {"TLDR", new Regex("^\\s*(?<comm>(.*))?(?<commend>TLDR)\\s*$")},

        {"I HAS A VAR", new Regex("^\\s*(?<vardec>I\\s+HAS\\s+A)\\s+(?<varident>[a-zA-Z][a-zA-Z0-9_]*)(\\s+(?<comm>(.*)))?\\s*$")},
        {"I HAS A VAR ITZ", new Regex("^\\s*(?<vardec>I\\s+HAS\\s+A)\\s+(?<varident>[a-zA-Z][a-zA-Z0-9_]*)\\s+(?<init>ITZ)\\s+(?<rhs>(.+))\\s*$")},
        {"VAR R", new Regex("^\\s*(?<varident>[a-zA-Z][a-zA-Z0-9_]*)\\s+(?<assign>R)\\s+(?<rhs>(.+))\\s*$")},

        {"SUM OF", new Regex("^\\s*(?<sum>SUM\\s+OF)\\s+(?<rhs>(.+))\\s*")},
        {"DIFF OF", new Regex("^\\s*(?<diff>DIFF\\s+OF)\\s+(?<rhs>(.+))\\s*")},
        {"PRODUKT OF", new Regex("^\\s*(?<prod>PRODUKT\\s+OF)\\s+(?<rhs>(.+))\\s*")},
        {"QUOSHUNT OF", new Regex("^\\s*(?<quo>QUOSHUNT\\s+OF)\\s+(?<rhs>(.+))\\s*")},
        {"MOD OF", new Regex("^\\s*(?<mod>MOD\\s+OF)\\s+(?<rhs>(.+))\\s*")},
        {"BIGGR OF", new Regex("^\\s*(?<max>BIGGR\\s+OF)\\s+(?<rhs>(.+))\\s*")},
        {"SMALLR OF", new Regex("^\\s*(?<min>SMALLR\\s+OF)\\s+(?<rhs>(.+))\\s*")},

        {"BOTH OF", new Regex("^\\s*(?<and>BOTH\\s+OF)\\s+(?<rhs>(.+))\\s*")},
        {"EITHER OF", new Regex("^\\s*(?<or>EITHER\\s+OF)\\s+(?<rhs>(.+))\\s*")},
        {"WON OF", new Regex("^\\s*(?<xor>WON\\s+OF)\\s+(?<rhs>(.+))\\s*")},
        {"NOT", new Regex("^\\s*(?<not>NOT)\\s+(?<rhs>(.+))\\s*")},
        {"ALL OF", new Regex("^\\s*(?<infand>ALL\\s+OF)\\s+(?<rhs>(.+))\\s*$")}, //MKAY REQUIRED
	    {"ANY OF", new Regex("^\\s*(?<infor>ANY\\s+OF)\\s+(?<rhs>(.+))\\s*$")}, //MKAY REQUIRED
	
	    {"BOTH SAEM", new Regex("^\\s*(?<eq>BOTH\\s+SAEM)\\s+(?<rhs>(.+))\\s*")},
        {"DIFFRINT", new Regex("^\\s*(?<ne>DIFFRINT)\\s+(?<rhs>(.+))\\s*")},

        {"SMOOSH", new Regex("^\\s*(?<concat>SMOOSH)\\s+(?<rhs>(.+))\\s*$")}, //similar to visible
	
	    {"VISIBLE", new Regex("^\\s*(?<output>VISIBLE)\\s+(?<rhs>(.+))\\s*$")}, //prints space separated shit
	    {"GIMMEH", new Regex("^\\s*(?<input>GIMMEH)\\s+(?<varident>[a-zA-Z][a-zA-Z0-9_]*)(\\s+(?<comm>(.*)))?\\s*$")},
    };

            Dictionary<String, Regex> IFSTUFF = new Dictionary<String, Regex>
    {
	    //{"O RLY?", new Regex("^\\s*(?<ifstart>O\\s+RLY\\?)(\\s+(?<comm>(.*)))?\\s*$")},
	    {"YA RLY", new Regex("^\\s*(?<if>YA\\s+RLY)(\\s+(?<comm>(.*)))?\\s*$")},
        {"NO WAI", new Regex("^\\s*(?<else>NO\\s+WAI)(\\s+(?<comm>(.*)))?\\s*$")},
        {"OIC", new Regex("^\\s*(?<end>OIC)(\\s+(?<comm>(.*)))?\\s*$")},
    };

            Dictionary<String, Regex> doable = new Dictionary<String, Regex>
    {
        {"VAR R", new Regex("^\\s*(?<varident>[a-zA-Z][a-zA-Z0-9_]*)\\s+(?<assign>R)\\s+(?<rhs>(.+))\\s*$")},

        {"SUM OF", new Regex("^\\s*(?<sum>SUM\\s+OF)\\s+(?<rhs>(.+))\\s*")},
        {"DIFF OF", new Regex("^\\s*(?<diff>DIFF\\s+OF)\\s+(?<rhs>(.+))\\s*")},
        {"PRODUKT OF", new Regex("^\\s*(?<prod>PRODUKT\\s+OF)\\s+(?<rhs>(.+))\\s*")},
        {"QUOSHUNT OF", new Regex("^\\s*(?<quo>QUOSHUNT\\s+OF)\\s+(?<rhs>(.+))\\s*")},
        {"MOD OF", new Regex("^\\s*(?<mod>MOD\\s+OF)\\s+(?<rhs>(.+))\\s*")},
        {"BIGGR OF", new Regex("^\\s*(?<max>BIGGR\\s+OF)\\s+(?<rhs>(.+))\\s*")},
        {"SMALLR OF", new Regex("^\\s*(?<min>SMALLR\\s+OF)\\s+(?<rhs>(.+))\\s*")},

        {"BOTH OF", new Regex("^\\s*(?<and>BOTH\\s+OF)\\s+(?<rhs>(.+))\\s*")},
        {"EITHER OF", new Regex("^\\s*(?<or>EITHER\\s+OF)\\s+(?<rhs>(.+))\\s*")},
        {"WON OF", new Regex("^\\s*(?<xor>WON\\s+OF)\\s+(?<rhs>(.+))\\s*")},
        {"NOT", new Regex("^\\s*(?<not>NOT)\\s+(?<rhs>(.+))\\s*")},
        {"ALL OF", new Regex("^\\s*(?<infand>ALL\\s+OF)\\s+(?<rhs>(.+))\\s*$")}, //MKAY REQUIRED
	    {"ANY OF", new Regex("^\\s*(?<infor>ANY\\s+OF)\\s+(?<rhs>(.+))\\s*$")}, //MKAY REQUIRED
	
	    {"BOTH SAEM", new Regex("^\\s*(?<eq>BOTH\\s+SAEM)\\s+(?<rhs>(.+))\\s*")},
        {"DIFFRINT", new Regex("^\\s*(?<ne>DIFFRINT)\\s+(?<rhs>(.+))\\s*")},

        {"SMOOSH", new Regex("^\\s*(?<concat>SMOOSH)\\s+(?<rhs>(.+))\\s*$")}, //similar to visible
	
	    {"VISIBLE", new Regex("^\\s*(?<output>VISIBLE)\\s+(?<rhs>(.+))\\s*$")}, //prints space separated shit
	    {"GIMMEH", new Regex("^\\s*(?<input>GIMMEH)\\s+(?<varident>[a-zA-Z][a-zA-Z0-9_]*)(\\s+(?<comm>(.*)))?\\s*$")},
    };
            Dictionary<String, Regex> doable2 = new Dictionary<String, Regex> { 
            { "WTF?", new Regex("^\\s*(?<switchstart>WTF\\?)\\s*$")},
        { "OMG", new Regex("^\\s*(?<case>OMG\\s+(.+))\\s*$")},
	    { "OMGWTF", new Regex("^\\s*(?<default>OMGWTF)\\s*$")},
	    { "GTFO", new Regex("^\\s*(?<break>GTFO)\\s*$")},
            };
            int temp=0;
            bool hasIf = false;
            //bool complete = false;
            for (int i=0;i<content.GetLength(0);i++)
            {
                if (content[i]==line)
                {
                    temp = i;
                }
                
            }
            
            line2 = temp;

            //if-else
            int oicLA = 0;      //closing lookahead -> OIC
            int orlyLA = 0;     //if-block lookahead -> O RLY?
            int yarlyLA = 0;    //if true lookahead -> YA RLY
            int nowaiLA = 0;    //else lookahead -> NO WAI
                                //int counter = 0;
            int loc = content.GetLength(0);
            int tagahanap = line2 + 1;

           
            while (tagahanap < loc)
            {
                Console.WriteLine("HANAP O RLY");
                if (Regex.IsMatch(content[tagahanap], "^\\s*O\\s+RLY\\?\\s*(.*)?"))
                {
                    orlyLA = tagahanap;
                    hasIf = true;
                    tagahanap++;

                    Console.WriteLine("ORAYT MAY IF. HANAPIN ANG IBANG INGREDIENTS.");
                    break;
                }
                else if (String.IsNullOrWhiteSpace(content[tagahanap]) ||
                         Regex.IsMatch(content[tagahanap], "^\\s*BTW\\s*(.*)") ||
                         Regex.IsMatch(content[tagahanap], "^\\s*OBTW\\s*(.*)"))
                {

                    if (String.IsNullOrWhiteSpace(content[tagahanap]) ||
                        Regex.IsMatch(content[tagahanap], "^\\s*BTW\\s*(.*)") ||
                        Regex.IsMatch(content[tagahanap], "^\\s*OBTW\\s*(.*)"))
                    {
                        //IF OBTW IGNORE
                        if (Regex.IsMatch(content[tagahanap], "^\\s*OBTW\\s*(.*)$"))
                        {
                            if (ignoreMultiline(content, tagahanap, out tagahanap, loc)) { break; }
                            //Console.WriteLine("AFTER IGNORING MULTILINE->"+content[tagahanap]);
                        }
                        //Console.WriteLine("IGNORING SHIT");
                    }
                }
                else
                {
                    //Console.WriteLine("NO ROOM FOR IF-ELSE. MAY IBA NA E->"+content[tagahanap]);
                    //console.Buffer.Text += "At line " + (tagahanap + 1) + " expected O RLY?, got something else";
                    //hasErr = true;

                    foreach (KeyValuePair<String, Regex> kv in patterns)
                    {
                        if (Regex.IsMatch(content[tagahanap], kv.Value.ToString()))
                        {
                            Console.WriteLine("found->" + kv.Key);

                            if (kv.Key.CompareTo("HAI") == 0)
                            {
                                output.AppendText("At line " + (tagahanap + 1) + " you can't do that.");
                                return true;
                            }

                            Console.WriteLine("NO ROOM FOR IF-ELSE. MAY IBA NA E->" + content[tagahanap]);

                            return false;
                        }
                    }

                    foreach (KeyValuePair<String, Regex> kv in IFSTUFF)
                    {
                        if (Regex.IsMatch(content[tagahanap], kv.Value.ToString()))
                        {
                            output.AppendText("At line " + (tagahanap + 1) + " found '" + kv.Key + "' for an IF-block but missing 'O RLY?'");

                            Console.WriteLine("NAKALIMUTAN MO SI O RLY" + content[tagahanap]);

                            return true;
                        }
                    }

                    output.AppendText("At line " + (tagahanap + 1) + " unexpected something.");
                    return true;

                }

                tagahanap++;
            }

            if (hasIf)
            {
                while (tagahanap < loc)
                {
                    Console.WriteLine("HANAP YA RLY NAMAN");

                    //*
                    if (Regex.IsMatch(content[tagahanap], "^\\s*O\\s+RLY\\?\\s*(.*)?"))
                    {
                        output.AppendText("At line " + (tagahanap + 1) + " expected 'YA RLY', got 'O RLY?'");
                        return true;
                    }
                    else if (Regex.IsMatch(content[tagahanap], "^\\s*YA\\s+RLY\\s*(.*)?"))
                    {
                        yarlyLA = tagahanap;
                        tagahanap++;

                        Console.WriteLine("ORAYT MAY IF-BLOCK. HANAPIN ANG ELSE OR END AGAD.");

                        while (tagahanap < loc)
                        {
                            if (Regex.IsMatch(content[tagahanap], "^\\s*NO\\s+WAI\\s*(.*)?")) { break; }
                            else if (Regex.IsMatch(content[tagahanap], "^\\s*OIC\\s*(.*)?")) { break; }
                            else
                            {

                                if (String.IsNullOrWhiteSpace(content[tagahanap]) ||
                                    Regex.IsMatch(content[tagahanap], "^\\s*BTW\\s*(.*)") ||
                                    Regex.IsMatch(content[tagahanap], "^\\s*OBTW\\s*(.*)"))
                                {

                                    if (String.IsNullOrWhiteSpace(content[tagahanap]) ||
                                        Regex.IsMatch(content[tagahanap], "^\\s*BTW\\s*(.*)") ||
                                        Regex.IsMatch(content[tagahanap], "^\\s*OBTW\\s*(.*)"))
                                    {
                                        //IF OBTW IGNORE
                                        if (Regex.IsMatch(content[tagahanap], "^\\s*OBTW\\s*(.*)$"))
                                        {
                                            if (ignoreMultiline(content, tagahanap, out tagahanap, loc)) { break; }
                                            //Console.WriteLine("AFTER IGNORING MULTILINE->"+content[tagahanap]);
                                        }
                                        //Console.WriteLine("IGNORING SHIT");
                                    }
                                }
                                else
                                {
                                  
                                    hasErr = true;

                                    foreach (KeyValuePair<String, Regex> kv in doable)
                                    {
                                        if (Regex.IsMatch(content[tagahanap], kv.Value.ToString()))
                                        {
                                            hasErr = false;
                                            break;
                                        }
                                    }
                                    if (hasErr)
                                    {
                                        output.AppendText("At line " + (tagahanap + 1) + " unexpected something.");
                                        return true;
                                    }
                                }
                                tagahanap++;
                            }
                        }
                        break;
                    }
                    else if (String.IsNullOrWhiteSpace(content[tagahanap]) ||
                         Regex.IsMatch(content[tagahanap], "^\\s*BTW\\s*(.*)") ||
                         Regex.IsMatch(content[tagahanap], "^\\s*OBTW\\s*(.*)"))
                    {

                        if (String.IsNullOrWhiteSpace(content[tagahanap]) ||
                            Regex.IsMatch(content[tagahanap], "^\\s*BTW\\s*(.*)") ||
                            Regex.IsMatch(content[tagahanap], "^\\s*OBTW\\s*(.*)"))
                        {
                            //IF OBTW IGNORE
                            if (Regex.IsMatch(content[tagahanap], "^\\s*OBTW\\s*(.*)$"))
                            {
                                if (ignoreMultiline(content, tagahanap, out tagahanap, loc)) { break; }
                                //Console.WriteLine("AFTER IGNORING MULTILINE->"+content[tagahanap]);
                            }
                            //Console.WriteLine("IGNORING SHIT");
                        }
                    }
                    else
                    {
                    

                        foreach (KeyValuePair<String, Regex> kv in patterns)
                        {
                            if (Regex.IsMatch(content[tagahanap], kv.Value.ToString()))
                            {
                                Console.WriteLine("found->" + kv.Key);

                                if (kv.Key.CompareTo("HAI") == 0)
                                {
                                    output.AppendText("At line " + (tagahanap + 1) + " you can't do that.");
                                    return true;
                                }
                                if (kv.Key.CompareTo("KTHXBYE") == 0)
                                {
                                    output.AppendText("Unexpected EOF; unterminated if-else block");
                                    return true;
                                }

                                output.AppendText("At line " + (tagahanap + 1) + " expected 'YA RLY', got '" + kv.Key + "'");

                                return true;
                            }
                        }

                        output.AppendText("At line " + (tagahanap + 1) + " unexpected something.");
                        return true;

                    }
                    tagahanap++;
                }

                while (tagahanap < loc)
                {
                    Console.WriteLine("HANAP OPTIONAL NO WAI");

                    //*
                    if (Regex.IsMatch(content[tagahanap], "^\\s*O\\s+RLY\\?\\s*(.*)?"))
                    {
                        output.AppendText("At line " + (tagahanap + 1) + " expected 'NO WAI' or 'OIC', got 'O RLY?'");
                        return true;
                    }
                    else if (Regex.IsMatch(content[tagahanap], "^\\s*YA\\s+RLY\\s*(.*)?"))
                    {
                        output.AppendText( "At line " + (tagahanap + 1) + " expected 'NO WAI' or 'OIC', got 'YA RLY'");
                        return true;
                    }
                    else if (Regex.IsMatch(content[tagahanap], "^\\s*NO\\s+WAI\\s*(.*)?"))
                    {
                        nowaiLA = tagahanap;
                        tagahanap++;

                        Console.WriteLine("ORAYT MAY ELSE-BLOCK. HANAPIN ANG END.");

                        while (tagahanap < loc)
                        {
                            if (Regex.IsMatch(content[tagahanap], "^\\s*OIC\\s*(.*)?")) { break; }
                            else
                            {
                                if (String.IsNullOrWhiteSpace(content[tagahanap]) ||
                                    Regex.IsMatch(content[tagahanap], "^\\s*BTW\\s*(.*)") ||
                                    Regex.IsMatch(content[tagahanap], "^\\s*OBTW\\s*(.*)"))
                                {

                                    if (String.IsNullOrWhiteSpace(content[tagahanap]) ||
                                        Regex.IsMatch(content[tagahanap], "^\\s*BTW\\s*(.*)") ||
                                        Regex.IsMatch(content[tagahanap], "^\\s*OBTW\\s*(.*)"))
                                    {
                                        //IF OBTW IGNORE
                                        if (Regex.IsMatch(content[tagahanap], "^\\s*OBTW\\s*(.*)$"))
                                        {
                                            if (ignoreMultiline(content, tagahanap, out tagahanap, loc)) { break; }
                                            //Console.WriteLine("AFTER IGNORING MULTILINE->"+content[tagahanap]);
                                        }
                                        //Console.WriteLine("IGNORING SHIT");
                                    }
                                }
                                else
                                {
                                
                                    hasErr = true;

                                    foreach (KeyValuePair<String, Regex> kv in doable)
                                    {
                                        if (Regex.IsMatch(content[tagahanap], kv.Value.ToString()))
                                        {
                                            hasErr = false;
                                            break;
                                        }
                                    }


                                    if (hasErr)
                                    {
                                        output.AppendText("At line " + (tagahanap + 1) + " unexpected something.");
                                        return true;
                                    }

                                }
                                tagahanap++;
                            }
                        }

                        break;

                    }
                    else if (String.IsNullOrWhiteSpace(content[tagahanap]) ||
                         Regex.IsMatch(content[tagahanap], "^\\s*BTW\\s*(.*)") ||
                         Regex.IsMatch(content[tagahanap], "^\\s*OBTW\\s*(.*)"))
                    {

                        if (String.IsNullOrWhiteSpace(content[tagahanap]) ||
                            Regex.IsMatch(content[tagahanap], "^\\s*BTW\\s*(.*)") ||
                            Regex.IsMatch(content[tagahanap], "^\\s*OBTW\\s*(.*)"))
                        {
                            //IF OBTW IGNORE
                            if (Regex.IsMatch(content[tagahanap], "^\\s*OBTW\\s*(.*)$"))
                            {
                                if (ignoreMultiline(content, tagahanap, out tagahanap, loc)) { break; }
                                //Console.WriteLine("AFTER IGNORING MULTILINE->"+content[tagahanap]);
                            }
                            //Console.WriteLine("IGNORING SHIT");
                        }
                    }
                    else if (Regex.IsMatch(content[tagahanap], "^\\s*OIC\\s*(.*)?"))
                    {
                        break;
                    }
                    else
                    {
                        //Console.WriteLine("NO ROOM FOR IF-ELSE. MAY IBA NA E->"+content[tagahanap]);
                        //console.Buffer.Text += "At line " + (tagahanap + 1) + " expected O RLY?, got something else";
                        //hasErr = true;

                        foreach (KeyValuePair<String, Regex> kv in patterns)
                        {
                            if (Regex.IsMatch(content[tagahanap], kv.Value.ToString()))
                            {
                                Console.WriteLine("found->" + kv.Key);

                                if (kv.Key.CompareTo("HAI") == 0)
                                {
                                    output.AppendText("At line " + (tagahanap + 1) + " you can't do that.");
                                    return true;
                                }
                                if (kv.Key.CompareTo("KTHXBYE") == 0)
                                {
                                    output.AppendText("Unexpected EOF; unterminated if-else block");
                                    return true;
                                }
                                output.AppendText("At line " + (tagahanap + 1) + " expected 'NO WAI' or 'OIC', got " + kv.Key + "'");

                                return true;
                            }
                        }

                        output.AppendText("At line " + (tagahanap + 1) + " unexpected something.");
                        return true;

                    }
                    tagahanap++;
                }

                while (tagahanap < loc)
                {
                    Console.WriteLine("HANAP OIC");

                    //*
                    if (Regex.IsMatch(content[tagahanap], "^\\s*O\\s+RLY\\?\\s*(.*)?"))
                    {
                        output.AppendText("At line " + (tagahanap + 1) + " expected 'OIC', got 'O RLY?'");
                        return true;
                    }
                    else if (Regex.IsMatch(content[tagahanap], "^\\s*YA\\s+RLY\\s*(.*)?"))
                    {
                        output.AppendText("At line " + (tagahanap + 1) + " expected 'OIC', got 'YA RLY'");
                        return true;
                    }
                    else if (Regex.IsMatch(content[tagahanap], "^\\s*OIC\\s*(.*)?"))
                    {
                        oicLA = tagahanap;
                        tagahanap++;

                        Console.WriteLine("ORAYT MAY NAKITA KO NA UNG END-IF.");
                        break;

                    }
                    else if (String.IsNullOrWhiteSpace(content[tagahanap]) ||
                         Regex.IsMatch(content[tagahanap], "^\\s*BTW\\s*(.*)") ||
                         Regex.IsMatch(content[tagahanap], "^\\s*OBTW\\s*(.*)"))
                    {

                        if (String.IsNullOrWhiteSpace(content[tagahanap]) ||
                            Regex.IsMatch(content[tagahanap], "^\\s*BTW\\s*(.*)") ||
                            Regex.IsMatch(content[tagahanap], "^\\s*OBTW\\s*(.*)"))
                        {
                            //IF OBTW IGNORE
                            if (Regex.IsMatch(content[tagahanap], "^\\s*OBTW\\s*(.*)$"))
                            {
                                if (ignoreMultiline(content, tagahanap, out tagahanap, loc)) { break; }
                                //Console.WriteLine("AFTER IGNORING MULTILINE->"+content[tagahanap]);
                            }
                            //Console.WriteLine("IGNORING SHIT");
                        }
                    }
                    else
                    {
                        //Console.WriteLine("NO ROOM FOR IF-ELSE. MAY IBA NA E->"+content[tagahanap]);
                        //console.Buffer.Text += "At line " + (tagahanap + 1) + " expected O RLY?, got something else";
                        //hasErr = true;

                        foreach (KeyValuePair<String, Regex> kv in patterns)
                        {
                            if (Regex.IsMatch(content[tagahanap], kv.Value.ToString()))
                            {
                                Console.WriteLine("found->" + kv.Key);

                                if (kv.Key.CompareTo("HAI") == 0)
                                {
                                    output.AppendText("At line " + (tagahanap + 1) + " you can't do that.");
                                    return true;
                                }
                                if (kv.Key.CompareTo("KTHXBYE") == 0)
                                {
                                    output.AppendText("Unexpected EOF; unterminated if-else block");
                                    return true;
                                }
                                output.AppendText("At line " + (tagahanap + 1) + " expected 'OIC', got " + kv.Key + "'");

                                return true;
                            }
                        }

                        output.AppendText("At line " + (tagahanap + 1) + " unexpected something.");
                        return true;

                    }
                    tagahanap++;
                }

            }


            
            while (tagahanap < loc) //MATCH ON FIRST OCCURRENCE
            {
                if (Regex.IsMatch(content[tagahanap], "^\\s*O\\s+RLY\\?") && orlyLA == 0) 
                {
                    orlyLA = tagahanap; 
                    hasIf = true; 
                }
                else if (Regex.IsMatch(content[tagahanap], "^\\s*YA\\s+RLY") && yarlyLA == 0) 
                {
                    yarlyLA = tagahanap;
                    yarlycnt++;
                    if (yarlycnt > 1) 
                    {
                        output.AppendText( "At line " + (tagahanap + 1) + " multiple if-blocks");
                        hasErr = true;
                        return hasErr;
                    }
                }
                else if (Regex.IsMatch(content[tagahanap], "^\\s*NO\\s+WAI") && nowaiLA == 0) 
                { 
                    nowaiLA = tagahanap;
                    nowaicnt++;
                    if (yarlycnt > 1)
                    {
                        output.AppendText("At line " + (tagahanap + 1) + " multiple else-blocks");
                        hasErr = true;
                        return hasErr;
                    }
                }
                else if (Regex.IsMatch(content[tagahanap], "^\\s*OIC") && oicLA == 0)
                {
                    oicLA = tagahanap; 
                }
                tagahanap++;

                if (oicLA != 0) { break; }  //kumpleto na sana yung mga kailangan sa if-else
            }
            

            if (oicLA == 0)
            {
                if (hasIf)
                {
                    output.AppendText("Unexpected EOF; unterminated IF-ELSE block.");
                    hasErr = true;
                    //break;
                    return hasErr;
                }

            }
            else
            {

                if (yarlyLA > nowaiLA && nowaiLA != 0)
                {
                    output.AppendText("Unexpected NO WAI ; expected YA RLY");
                    hasErr = true;
                    //break;
                    return hasErr;
                }

                if (orlyLA != 0) //may if block
                {
                    output.AppendText("orlyLA\n");
                    if (symbolTable["IT"].CompareTo("WIN") == 0) //gawin mo yung yarly+1 until nowai-1||oic-1
                    {
                        //Console.WriteLine("TARA KAY WIN");
                        
                        if (yarlyLA == 0)
                        {
                            output.AppendText("After line " + (orlyLA + 1) + " missing if statement");
                            line2 = oicLA;
                            hasErr = true;
                            //break;
                            return hasErr;
                        }
                        else //may if-block
                        {
                            //Console.WriteLine("GAWIN SI WIN");
                            for (int i = yarlyLA + 1; i < oicLA + 1; i++)
                            {
                                if (Regex.IsMatch(content[i], "^\\s*NO\\s+WAI\\s*") ||
                                    Regex.IsMatch(content[i], "^\\s*OIC\\s*"))
                                {
                                    //OKAY, MAY NO WAI or OIC
                                    //SET I TO NO WAI or BREAK
                                    //Console.WriteLine("DI KITA KELANGAN NO WAI");
                                    /****/
                                    table1.Rows.Add("NO WAI", "ELSE BLOCK");
                                    i = oicLA;
                                    line2 = oicLA;
                                    break;
                                }
                                else if ((Regex.IsMatch(line, "^\\s*VISIBLE\\s+.+!?$")))
                                {
                                    //printDaw(content[i], i);
                                    if (OutputStatement(line)) { break; }
                                }
                                else if ((Regex.IsMatch(line, "^\\s*GIMMEH\\s+[a-zA-Z][a-zA-Z0-9_]*$")))
                                {
                                    //scanDaw(content[i], i);
                                    if (InputStatement(line)) { break; }
                                }
                                else if ((Regex.IsMatch(line, "^\\s*(SUM\\s+OF|DIFF\\s+OF|QUOSHUNT\\s+OF|PRODUKT\\s+OF|MOD\\s+OF|BIGGR\\s+OF|SMALLR\\s+OF)")))
                                {
                                    //arithmeticDaw(content[i], i);
                                    this.ArithmeticOp(line, "");
                                }
                                else if ((Regex.IsMatch(line, "^\\s*(BOTH\\s+SAEM|DIFFRINT)")))
                                {
                                    //comparisonDaw(content[i], i);
                                    this.ComparisonOp(line, "");
                                }
                                else if ((Regex.IsMatch(line, "^\\s*(BOTH\\s+OF|EITHER\\s+OF|WON\\s+OF)")))
                                {
                                    //booleanDaw(content[i], i);
                                    this.BoolOp(line, "");
                                }
                                else if ((Regex.IsMatch(content[i], "^\\s*(I\\s+HAS\\s+A|HAI|KTHXBYE)")))
                                {
                                    output.AppendText("At line" + (i + 1) + " you can't do that in an if-block");
                                    hasErr = true;
                                    break;
                                }
                                else if ((Regex.IsMatch(content[i], "^\\s*([a-zA-Z][a-zA-Z0-9_]*)\\s+R\\s+.+$")))
                                {
                                    Regex p = new Regex("^\\s*(?<varident>[a-zA-Z][a-zA-Z0-9_]*)\\s+R\\s+.+$");
                                    Match n = p.Match(content[i]);

                                    hasErr = VarsFirst(line);
                                    if (hasErr)
                                    {
                                        output.AppendText(" At line " + (i + 1) + " " + n.Groups["varident"].ToString() + " undeclared ");
                                        break;
                                    }
                                }
                                //DO PRINTING, SCANNING, ARITHMETIC, COMPARISON, BOOLEAN HERE                                   
                                //Console.WriteLine("DOING WIN SHIT");
                            }
                        }
                    }
                    else if (symbolTable["IT"].CompareTo("FAIL") == 0) //gawin mo yung nowai-1 until oic-1
                    {
                        if (yarlyLA == 0)
                        {
                            output.AppendText("After line " + (orlyLA + 1) + " missing if statement");

                            //Console.WriteLine(content[line]);
                            line2 = oicLA;
                            hasErr = true;
                            //Console.WriteLine(content[line]);
                            //break;
                            return hasErr;
                        }
                        else if (nowaiLA != 0) //kung may else block, else kebs ka lang
                        {
                            for (int i = nowaiLA + 1; i < oicLA + 1; i++)
                            {
                                if (Regex.IsMatch(content[i], "^\\s*OIC\\s*(.*)?"))
                                {
                                    //OKAY, end IF-ELSE
                                    //SET I TO NO WAI or BREAK
                                    //Console.WriteLine("DI KITA KELANGAN NO WAI");
                                    /****/
                                    table1.Rows.Add("NO WAI", "ELSE BLOCK");
                                    i = oicLA;
                                    line2 = oicLA;
                                    break;
                                }
                                else if ((Regex.IsMatch(line, "^\\s*VISIBLE\\s+.+!?$")))
                                {
                                    //printDaw(content[i], i);
                                    if (OutputStatement(line)) { break; }
                                }
                                else if ((Regex.IsMatch(line, "^\\s*GIMMEH\\s+[a-zA-Z][a-zA-Z0-9_]*$")))
                                {
                                    //scanDaw(content[i], i);
                                    if (InputStatement(line)) { break; }
                                }
                                else if ((Regex.IsMatch(line, "^\\s*(SUM\\s+OF|DIFF\\s+OF|QUOSHUNT\\s+OF|PRODUKT\\s+OF|MOD\\s+OF|BIGGR\\s+OF|SMALLR\\s+OF)")))
                                {
                                    //arithmeticDaw(content[i], i);
                                    this.ArithmeticOp(line, "");
                                }
                                else if ((Regex.IsMatch(line, "^\\s*(BOTH\\s+SAEM|DIFFRINT)")))
                                {
                                    //comparisonDaw(content[i], i);
                                    this.ComparisonOp(line, "");
                                }
                                else if ((Regex.IsMatch(line, "^\\s*(BOTH\\s+OF|EITHER\\s+OF|WON\\s+OF)")))
                                {
                                    //booleanDaw(content[i], i);
                                    this.BoolOp(line, "");
                                }
                                else if ((Regex.IsMatch(content[i], "^\\s*(I\\s+HAS\\s+A|HAI|KTHXBYE)")))
                                {
                                    output.AppendText("At line" + (i + 1) + " you can't do that in an if-block");
                                    hasErr = true;
                                    break;
                                }
                                else if ((Regex.IsMatch(content[i], "^\\s*([a-zA-Z][a-zA-Z0-9_]*)\\s+R\\s+.+$")))
                                {
                                    Regex p = new Regex("^\\s*(?<varident>[a-zA-Z][a-zA-Z0-9_]*)\\s+R\\s+.+$");
                                    Match n = p.Match(content[i]);

                                    hasErr = VarsFirst(line);
                                    if (hasErr)
                                    {
                                        output.AppendText(" At line " + (i + 1) + " " + n.Groups["varident"].ToString() + " undeclared ");
                                        hasErr = true;
                                        break;
                                    }
                                }
                                //DO PRINTING, SCANNING, ARITHMETIC, COMPARISON, BOOLEAN HERE                                   
                                //Console.WriteLine("DOING FAIL SHIT");
                            }
                        }
                    }
                    else
                    {
                        output.AppendText("At line " + (temp + 1) + " cannot implicitly cast value of IT to TROOF");
                        return true;
                    }
                    Console.WriteLine("AFTER IF-ELSE" + content[line2]);
                }
            }
            return hasErr;
        }

        private bool ignoreMultiline(String[] content, int i, out int line, int loc)
        {
            bool multiline = false;
            line = i;

            Console.WriteLine("MAY OBTW BA?->" + content[line]);

            Dictionary<String, Regex> patterns = new Dictionary<String, Regex>
            {
                {"OBTW", new Regex("^\\s*(?<commstart>OBTW)(\\s+(.*))?\\s*")},
                {"TLDR", new Regex("^\\s*(?<comm>(.*))?(?<commend>TLDR)\\s*$")},
            };

            if (Regex.IsMatch(content[line], patterns["OBTW"].ToString()))
            {
                Console.WriteLine("MAY MULTILINE");
                Match m = patterns["OBTW"].Match(content[line]);

                String comment = m.Groups["comm"].ToString();

                table1.Rows.Add(m.Groups["commstart"].ToString(), "multiline comment start");
                multiline = true;
                i++;

                while (multiline && i < loc)
                {
                    if (Regex.IsMatch(content[line], patterns["TLDR"].ToString()))
                    {
                        Match n = patterns["TLDR"].Match(content[line]);
                        comment = comment + " " + n.Groups["comm"].ToString();

                        if (!String.IsNullOrWhiteSpace(comment))
                        {
                            table1.Rows.Add(comment, "COMMENT");
                        }
                        table1.Rows.Add(n.Groups["commend"].ToString(), "multiline comment end");
                        multiline = false;
                        
                        Console.WriteLine("ITO IBABALIK KO->" + content[line]);
                        return false;
                    }
                    else
                    {
                        comment = comment + " " + content[line];
                    }
                    line++;
                }

            }

            if (line == loc)
            {
                output.AppendText("Unexpected EOF; unterminated comment.");
                return true;
            }

            return false;

        }

        private void CaseStatement(String line) {
            Match m = Regex.Match(line, "(?<value>[a-zA-Z]\\w*|\\\"(.*?)\\\"|(\\-|\\+)?[0-9]+(\\.[0-9]*)?|WIN|FAIL),\\s+WTF\\?\\s+(?<case>.+)\\s+OIC");
            if (m.Success)
            {
                this.checkValue(m.Groups["value"].Value);
                table1.Rows.Add("WTF?", "DELIMITER");
                lexemes.AddLast("WTF?");
                string cases = m.Groups["case"].Value;
                string[] codes = Regex.Split(cases, "OMG");
                foreach (string code in codes) {
                    if (!string.IsNullOrEmpty(code))
                    {
                        Match m1 = Regex.Match(code, "(\\s+)(?<value>[a-zA-Z]\\w*|\\\"(.*?)\\\"|(\\-|\\+)?[0-9]+(\\.[0-9]*)?|WIN|FAIL)(\\s+)?(?<case0>.+)?(?<gtfo>\\s+GTFO)");
                        Match m2 = Regex.Match(code, "(\\s+)(?<value>[a-zA-Z]\\w*|\\\"(.*?)\\\"|(\\-|\\+)?[0-9]+(\\.[0-9]*)?|WIN|FAIL)(\\s+)?(?<case1>.+)?");
                        Match m3 = Regex.Match(code, "(?<wtf>(WTF))(\\s+)?(?<case2>.+)?(\\s+)?(?<gtfo>GTFO)?");
                        if (m3.Success)
                        {
                            table1.Rows.Add("OMGWTF", "DELIMITER");
                            if (!string.IsNullOrEmpty(m3.Groups["case2"].Value)) {
                                this.checkString(m3.Groups["case2"].Value);
                            }
                            table1.Rows.Add("GTFO", "DELIMITER");
                            lexemes.AddLast("GTFO");
                        }
                        else if (m1.Success)
                        {
                            table1.Rows.Add("OMG", "DELIMITER");
                            lexemes.AddLast("OMG");
                            this.checkValue(m1.Groups["value"].Value);
                            if (!string.IsNullOrEmpty(m1.Groups["case0"].Value))
                            {
                                this.checkString(m1.Groups["case0"].Value);
                            }
                            table1.Rows.Add(m1.Groups["gtfo"].Value, "DELIMITER");
                            lexemes.AddLast(m1.Groups["gtfo"].Value);
                        }
                        else if (m2.Success)
                        {
                            table1.Rows.Add("OMG", "DELIMITER");
                            lexemes.AddLast("OMG");
                            this.checkValue(m2.Groups["value"].Value);
                            if (!string.IsNullOrEmpty(m2.Groups["case1"].Value)) this.checkString(m2.Groups["case1"].Value);
                        }
                    }
                }
                
                table1.Rows.Add("OIC","DELIMITER");
                lexemes.AddLast("OIC");
            }
        }

        public String checkValue(string s1)
        { // check value type
            String type = "";
            if (Regex.IsMatch(s1, @"^(WIN|FAIL)$")) type = "BOOLEAN LITERAL";
            else if (Regex.IsMatch(s1, @"^\b(\-|\+)?[0-9]+\.[0-9]*\b$")) type = "NUMBAR LITERAL";
            else if (Regex.IsMatch(s1, @"^\b(\-|\+)?[0-9]+\b$")) type = "NUMBR LITERAL";
            else if (Regex.IsMatch(s1, "^\\\"(.*?)\\\"$")) type = "YARN LITERAL";
            else if (Regex.IsMatch(s1, "^[a-zA-Z]\\w*$")) type = "VARIABLE IDENTIFIER";
            table1.Rows.Add(s1, type);
            lexemes.AddLast(s1);
            return type;
        }

     
        public String checkInput(string s1)
        { // check value type
            String type = "";
            if (Regex.IsMatch(s1, @"^\b(WIN|FAIL)\b$")) type = "BOOLEAN LITERAL";
            else if (Regex.IsMatch(s1, @"^\b(\-|\+)?[0-9]+\.[0-9]*\b$")) type = "NUMBAR LITERAL";
            else if (Regex.IsMatch(s1, @"^\b(\-|\+)?[0-9]+\b$")) type = "NUMBR LITERAL";
            else if (Regex.IsMatch(s1, ".*")) type = "YARN LITERAL";
            table1.Rows.Add(s1, type);
            lexemes.AddLast(s1);
            return type;
        }

        private void FunctionStatement(String line) {
            Match m = Regex.Match(line, "HOW\\s+DUZ\\s+I\\s+(?<value>[a-zA-Z]\\w*)(\\s+)?(<?here>.+)?");
            if (m.Success) {
                table1.Rows.Add("HOW DUZ I", "FUNCTION DELIMITER");
                lexemes.AddLast("HOW DUZ I");
                this.checkValue(m.Groups["value"].Value);
                String str = m.Groups["here"].Value;
                this.output.AppendText(str);
                string[] values = Regex.Split(str, "AN");
                string pattern1 = "YR\\s+(?<arg>.+)";
                int i;
                for (i = 0; i < values.Length; i++)
                {
                    Match m1 = Regex.Match(m.Groups["here"].Value, pattern1);
                    if (m1.Success) {
                        table1.Rows.Add("YR", "OPERATOR");
                        lexemes.AddLast("YR");
                        table1.Rows.Add(m1.Groups["arg"].Value, "FUNCTION ARGUMENT");
                        lexemes.AddLast(m1.Groups["arg"].Value);
                    }
                }
            }
        }

        private void button1_Click(object sender, EventArgs e)
        {
            this.table1.Rows.Clear(); this.table2.Rows.Clear(); editor.Clear(); output.Clear();
        }

        private void button2_Click(object sender, EventArgs e)
        {
            OpenFileDialog fDialog = new OpenFileDialog();
            fDialog.Title = "Open LOLCode File"; //title
            fDialog.Filter = "LOLCode Files|*.lol"; //filters only .lol files
            fDialog.InitialDirectory = @"C:\"; //initial directory at C:\


            if (fDialog.ShowDialog() == DialogResult.OK)
            {
                //  MessageBox.Show(fDialog.FileName.ToString());

                int counter = 0;
                string line;

                // Read the file and display it line by line.
                System.IO.StreamReader file = new System.IO.StreamReader(fDialog.FileName.ToString());
                while ((line = file.ReadLine()) != null)
                {
                    editor.AppendText(line);
                    editor.AppendText("\n");
                    counter++;
                }

                file.Close();
            }
        }//Open Button
    }
}
//---------------------------------------------------------------------------------------------
