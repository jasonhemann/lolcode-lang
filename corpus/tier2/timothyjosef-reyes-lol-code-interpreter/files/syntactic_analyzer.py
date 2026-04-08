import sys
from lexical_analyzer import lex_analysis as Lexer

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
    
    # get current token using pointer position as index
    def current_token(self):
        return self.tokens[self.position] if self.position < len(self.tokens) else None
    
    # move pointer if token matches type and value
    def match(self, expected_type, expected_value=None):
        token = self.current_token()
        # check if token exists and if type matches
        if token and token["type"] == expected_type:
            # separated value matching, just in case None yung value
            if  expected_value == token["value"] or expected_value is None:   
                self.position += 1 # move the pointer
                return token
        return None
    
    def syntax_error(self, message):
        token = self.current_token()
        line_info = f"Line {token['line']}: " if token else ""
        print(f"Syntax Error: {line_info}{message}")
        sys.exit(1)

    # check if code starts with HAI and ends in KBYE
    def parse_program(self):
        print("gas1")
        # if not tokens[1:] == "HAI"
        if not self.match("PROGRAM_STRUCTURE_DELIMITERS_KEYWORDS", "HAI"):
            self.syntax_error("Program must start with HAI")
            # print("Syntax Error, Program must start with HAI")
            # sys.exit(1)

        print("gas2")
        # call declarations parser
        self.parse_declarations()

        print("gas3")
        # get current token
        current = self.current_token()
        while current and current["value"] != "KTHXBYE":
            self.parse_statement()
            # print("all good")
            current = self.current_token() # reread token for next loop for KTHNXBYE

        print("gas4")
        if not self.match("PROGRAM_STRUCTURE_DELIMITERS_KEYWORDS", "KTHXBYE"):
            self.syntax_error("Program must end with KTHXBYE")
            # print("Syntax Error: Program must end with KTHXBYE")
            sys.exit(1)

        print("Parsing done")
      
    # variable declaration
    def parse_declarations(self):
        # check for wazzup
        current = self.current_token()
        if current and current["value"] == "WAZZUP":
            self.match("PROGRAM_STRUCTURE_DELIMITERS_KEYWORDS", "WAZZUP")

            # parse I HAS A statements
            current = self.current_token()
            while current and current["value"] != "BUHBYE":
                # BTW
                if current["value"] == "BTW":
                    self.parse_singleline()
                    current = self.current_token() # check next token
                    continue
                # OBTW
                if current["value"] == "OBTW":
                    self.parse_multiline()
                    current = self.current_token() # Check next token
                    continue
                # call var declarations for i has a and other logic
                # declaration
                if current["value"] == "I HAS A":
                    self.parse_var_declaration()
                else:
                    self.syntax_error("Unexpected token in WAZZUP block, expected 'I HAS A', 'BTW', 'OBTW', or 'BUHBYE'")

                current = self.current_token() # stupid parenthesis

            if not self.match("PROGRAM_STRUCTURE_DELIMITERS_KEYWORDS", "BUHBYE"):
                # there was WAZZUP but no BUHBYE
                self.syntax_error("Expected BUHBYE to close WAZZUP.")
                # print(f"Syntax Error: Line {current['line']}: Expected BUHBYE to close WAZZUP.")
        print("Parsed WAZZUP and BUHBYE Variable Declaration Statement")

    def parse_var_declaration(self):
        # matches I HAS part
        if self.match("VARIABLE_DECLARATION_AND_ASSIGNMENT_KEYWORDS", "I HAS A"):
            # look out for identifier for variable name
            var_name = self.current_token()["value"]
            if self.match("VARIABLE_DECLARATION", None):                
                # check for ITZ
                if self.current_token() and self.current_token()["value"] == "ITZ": # parenthesis WHYY HUHUHU # tas dito ulet huhu
                    self.match("VARIABLE_DECLARATION_AND_ASSIGNMENT_KEYWORDS", "ITZ")
                    self.parse_expression()

                print(f"Parsed '{var_name}' variable ")
                return
            else:
                self.syntax_error("Expected variable name after I HAS A")
                # print(f"Syntax Error: Line {self.current_token()['line']}: Expected variable name after I HAS A")
                # sys.exit(1)
        

    # parse statements ---------------------------------------------------------------------------------
    # parse statements ---------------------------------------------------------------------------------
    # parse statements ---------------------------------------------------------------------------------
    def parse_statement(self):
        current = self.current_token()
        if not current:
            return
        
        # single line comments
        if current["value"] == "BTW":
            self.parse_singleline()
            return
        
        if current["value"] == "OBTW":
            self.parse_multiline()
            return

        # print("gas6")
        # check for keywords that start statements
        if current["value"] == "VISIBLE":
            self.parse_visible()
        elif current["value"] == "GIMMEH":
            self.parse_gimmeh()
        elif current["value"] == "O RLY?":
            self.parse_conditionals()
        elif current["value"] == "HOW IZ I":
            self.parse_function_definition()
        elif current["value"] == "IM IN YR":
            self.parse_loop()
        elif current["value"] == "GTFO":    # kulang  
            self.parse_gtfo()               # gtfo
        elif current["value"] == "WTF?":    # wtf
            self.parse_switch()
        elif current["value"] in ["SMOOSH", "SUM OF", "DIFF OF", "PRODUKT OF", "QUOSHUNT OF", "MOD OF", "BIGGR OF", "SMALLR OF"]:
            self.parse_expression()
        # naisip ko dito what if yung keyword yung gamitin 
        # like if current["type"] = CONDITIONALS_KEYWORD, tas after sha i breakdwon
        elif current["type"] == "VARIABLE":
            # dito dapat 'var' R 'expression"
            # peek at next token
            # if self.position+1 < len(self.tokens) and self.tokens[self.position + 1]["value"] == "R":
            if self.position+1 < len(self.tokens):
                next_value = self.tokens[self.position + 1]["value"]

                if next_value == " R ":
                    self.parse_assignment()
                
                # diff from MAEK
                elif next_value == "IS NOW A":
                    self.parse_type_cast_statement()
            else:
                # variable pero no assignment, so func call 
                self.parse_expression()
        # functions
        elif current["type"] == "FUNCTIONS" or current["value"] == "I IZ":
            # function is <func> <args>
            self.parse_expression() ## PARENTHESIS
        else:
            self.syntax_error(f"Unrecognized Statement: '{current['value']}'")
            # print(f"Syntax Error: Line {current['line']}: Unrecognized Statement - {current['value']}'")
            # sys.exit[1]

    # parse statements ---------------------------------------------------------------------------------
    # parse statements ---------------------------------------------------------------------------------

    # parse expressions ==================================================
    # parse expressions ==================================================
    # parse expressions ==================================================
    def parse_expression(self):
        current = self.current_token()
        if not current:
            self.syntax_error("Expected expression but found none")
            return False
        
        multi_op_keywords = [
            "SMOOSH", "SUM OF", "DIFF OF", "PRODUKT OF", "QUOSHUNT OF", 
            "MOD OF", "BIGGR OF", "SMALLR OF","BOTH OF", "EITHER OF", "WON OF", 
            "ANY OF", "ALL OF", "BOTH SAEM", "DIFFRINT"
            ]
        if current["value"] in multi_op_keywords:
            op_token = self.match(current["type"], current["value"]) # consume multi arity op SMOOSH)
        
            # get first expr 
            if not self.parse_expression():
                self.syntax_error(f"Expected first argument after {op_token['value']}")
                return False
                
            # to consume ' AN ' and args after
            while self.current_token() and self.current_token()["value"] == " AN ":
                self.match("ARITHMETIC_OPERATIONS_KEYWORDS", " AN ") 
                
                # parse next operand
                if not self.parse_expression():
                    self.syntax_error(f"Expected argument after ' AN ' in {op_token['value']} operation.")
                    return False
        
            print(f"Parsed {op_token['value']} Operation.")
            return True

        # literals (numbr yarn, bool)
        elif current["type"] in ["NUMBER_LITERAL", "STRING_LITERAL", "BOOLEAN_LITERAL", "VARIABLE"]:
            self.position += 1
            print(f"Parsed VISIBLE Expression: {current['value']}")

            # REMOVE FROM HERE
            # string number litrals
            next_token = self.current_token()
            
            # previous token (current) was a STRING or NUMBER literal
            # then next token exists and is a STRING or NUMBER literal
            # last is if equal sila (liek 17)
            if current["type"] in ["STRING_LITERAL", "NUMBER_LITERAL"] and \
            next_token and next_token["type"] in ["STRING_LITERAL", "NUMBER_LITERAL"] and \
            current["value"] == next_token["value"]:
            
                print(f"Consume duplicate literal token: {next_token['value']}")
                self.position += 1 # move pointer 
            
            # REMOVE UNTIL HERE

            # FOR VISIBLE SINCE DITO SIYA BABABALIK AFTER IREAD YUNG x as Variable
            while self.current_token() and self.current_token()['value'] == ' + ':
                # consume + separator for visible
                # print(f"TYPE: {self.current_token()['type']}")
                self.match(self.current_token()['type'], ' + ')
                
                # dapat expr next token after nung + 
                if not self.parse_expression():
                    self.syntax_error("Expected expression after ' + ' separator")

            return True
        
        # variables
        # elif current["type"] == "VARIABLE":
        #     self.position +=1
        #     return
        

        #  # check for artihmetic operations
        # if current["type"] == "ARITHMETIC_OPERATIONS_KEYWORDS" and current["value"] not in [" AN "]:
        #     return self.parse_arithmetic_operation()
        
        # operations (arithmetic, logic, comparisons, strings)
        elif current["type"] in ["ARITHMETIC_OPERATIONS_KEYWORDS", "LOGIC_AND_COMPARISON_KEYWORDS"]:
            operator = self.match(current["type"], current["value"])

            # pattern is <operand> ' AN ' <operand>
            # parse the first operand
            self.parse_expression()

            # handles AN
            while self.current_token() and self.current_token()['value'] == " AN ":
                self.match("ARITHMETIC_OPERATIONS_KEYWORDS", " AN ") # conncetor
                self.parse_expression() # next operand
            # need natin icheck yung number of operands vs operator arity sa semantic after nito

            # self.parse_multi_arity_op()
            # return True
            return True
        
        # funciton call
        elif current["value"] == "I IZ":
            self.parse_function_call()
            return True
        
        # IT (yung implicit var)
        elif current["value"] == "IT":
            self.position += 1
            return True

        elif current["value"] == "MAEK":
            self.parse_typecast()
            return True
        
        # string concat
        elif current["value"] == "SMOOSH":
            return self.parse_smoosh()
        
        else:
            self.syntax_error(f"Expected expression but found '{current['value']}'")
    # parse expressions ==================================================
    # parse expressions ==================================================
    # parse expressions ==================================================
#
### doublecheck if may kulang here pagod na me 
#
    def parse_assignment(self):
        var_token = self.match("VARIABLE", None)
        # <var> R <Expression>
        # if not self.match("VARIABLE", None):
        if not var_token:
            self.syntax_error("Expected variable name for assignment")
            return False

        if not self.match("VARIABLE_DECLARATION_AND_ASSIGNMENT_KEYWORDS", " R "):
            self.syntax_error("Expected ' R ' keyword for assignment")
            return False

        # RHS ng R
        if not self.parse_expression():
            self.syntax_error("Expected an expression after ' R '")
            return False

        print(f"Parsed Assignement Statement: {var_token['value']} R <expression>")
        return True

    def parse_visible(self):
        # VISIBLE <expression>
        self.match("INPUT_OUTPUT_KEYWORDS", "VISIBLE")
        self.parse_expression()

        #  AN <expression>
        while self.current_token() and self.current_token()["value"] == " AN ":
            self.match("ARITHMETIC_OPERATIONS_KEYWORDS", " AN ")
            self.parse_expression()
        
        print("Parsed VISIBLE Statement.")

    def parse_gimmeh(self):
        self.match("INPUT_OUTPUT_KEYWORDS", "GIMMEH")
        if not self.match("VARIABLE"):
            self.syntax_error("Expected variable name after GIMMEH")
        print("Parsed GIMMEH Statement.")

    def parse_conditionals(self):
        #O RLY? blah blah OIC
        self.match("CONDITIONALS_KEYWORDS", "O RLY?")

        # check IT here

        # YA RLY 
        if self.current_token() and self.current_token()["value"] == "YA RLY":
            self.match("CONDITIONALS_KEYWORDS", "YA RLY")
            # statements in YA RLY (true) block
            while self.current_token() and self.current_token()["value"] not in ["MEBBE", "NO WAI", "OIC"]:
                self.parse_statement()

        # MEBBE
        # nag while na ako para lahat ng MEBBE macatch na since pwedeng maraming elif
        while self.current_token() and self.current_token()["value"] == "MEBBE":
            self.match("CONDITIONALS_KEYWORDS", "MEBBE")
            self.parse_expression() # check MEBBE

        # NO WAI
        if self.current_token() and self.current_token()["value"] == "NO WAI":
            self.match("CONDITIONALS_KEYWORDS", "NO WAI")
            # statements in NO WAI (false) block
            while self.current_token() and self.current_token()["value"] != "OIC":
                self.parse_statement()

        # ends with OIC
        if not self.match("CONDITIONALS_KEYWORDS", "OIC"):
            self.syntax_error("Expected OIC to close O RLY?")
        print("Parsed Conditional Statement.")
    
    # function definition
    def parse_function_definition(self):
        # HOW IZ I <funcname> 
        self.match("FUNCTIONS_KEYWORDS", "HOW IZ I")
        if not self.match("FUNCTIONS_DECLARATIONS"):
            self.syntax_error("Expected function name after HOW IZ I")

        # [YR <param> AN YR <param>]
        while self.current_token() and self.current_token()["value"] == "YR":
            self.match("FUNCTIONS_KEYWORDS", "YR")
            if not self.match("FUNCTIONS_PARAMETERS"):
                 self.syntax_error("Expected parameter name after YR")

            # AN connector
            # if self.current_token() and self.current_token()["value"] == " AN ":
            #     self.match("ARITHMETIC_OPERATIONS_KEYWORDS", " AN ")

            # AN YR
            current = self.current_token()
            while current and current["value"] == " AN ":
                self.match("ARITHMETIC_OPERATIONS_KEYWORDS", " AN ")
                self.match("FUNCTIONS_KEYWORDS", "YR")
                if not self.match("FUNCTIONS_PARAMETERS", None):
                    self.syntax_error("Expected parameter name after AN YR")
                current = self.current_token()

        if not self.match("FUNCTIONS_KEYWORDS", "MKAY"):
            self.syntax_error("Expected MKAY after function parameters.")

        # function body statements
        while self.current_token() and self.current_token()["value"] != "IF U SAY SO":
            self.parse_statement()

        # ends in IF U SAY SO
        if not self.match("FUNCTIONS_KEYWORDS", "IF U SAY SO"):
            self.syntax_error("Expected IF U SAY SO to close function definition")
        print("Parsed Function Definition.")
        
    # loops
    def parse_loop(self):
        # IM IN YR <loop> 
        self.match("LOOPS_KEYWORDS", "IM IN YR")
        if not self.match("LOOP_DECLARATION"):
            self.syntax_error("Expected loop name after IM IN YR")

        # operator <UPPIN YR , NERFIN YR>
        if self.current_token() and self.current_token()["value"] in ["UPPIN YR", "NERFIN YR"]:
            self.match("LOOPS_KEYWORDS", self.current_token()["value"])
            # <varbale>
            if not self.match("VARIABLE"):
                self.syntax_error("Expected variable name after UPPIN YR/NERFIN YR")

        # conditional < WILE , TIL >
        if self.current_token() and self.current_token()["value"] in ["WILE", "TIL"]:
            self.match("LOOPS_KEYWORDS", self.current_token()["value"])
            # <expression>
            self.parse_expression()

        # loop body statement
        
        while self.current_token() and self.current_token()["value"] != "IM OUTTA YR":
            self.parse_statement()

        # IM OUTTA YR <loop_name>
        self.match("LOOPS_KEYWORDS", "IM OUTTA YR")
        # if no loop name
        if not self.match("LOOP"):
            self.syntax_error(f"Expected loop name after IM OUTTA YR")

        # loop_name = self.current_token()["value"] 
        print("Parsed Loop Statement.")

    def parse_function_call(self):
        # I IZ <funcname> YR <arg> MKAY
        self.match("FUNCTIONS_KEYWORDS", "I IZ")
        if not self.match("FUNCTION"):
            self.syntax_error("Expected function name after I IZ")

        # YR <args>
        while self.current_token() and self.current_token()["value"] == "YR":
            self.match("FUNCTIONS_KEYWORDS", "YR")
            self.parse_expression()

        # MKAY
        if not self.match("FUNCTIONS_KEYWORDS", "MKAY"):
            self.syntax_error("Expected MKAY to close function call")
        print("Parsed Function Call.")

    def parse_typecast(self):
        # MAEK <expr> A <type>
        self.match("TYPE_CASTING_CONVERSION_KEYWORDS", "MAEK")
        self.parse_expression()
        self.match("TYPE_CASTING_CONVERSION_KEYWORDS", " A ")
        # type
        if not self.match("DATA_TYPES"):
             self.syntax_error("Expected data type after MAEK <expression> A")
        print("Parsed Type Casting Expression.")

    def parse_type_cast_statement(self):
        # consumes the var (i.e 'y')
        var_token = self.match("VARIABLE", None)
        
        # consumes  IS NOW A
        self.match("VARIABLE_DECLARATION_AND_ASSIGNMENT_KEYWORDS", "IS NOW A") 
        
        # consumes type (numbar)
        type_token = self.match("DATA_TYPES", None)
        
        if not type_token:
            self.syntax_error("Expected a data type (NUMBR, YARN, etc.) after 'IS NOW A'.")
            
        print(f"Parsed Type Casting Statement: {var_token['value']} IS NOW A {type_token['value']}")
        return True

    def parse_gtfo(self):
        # exit
        self.match("PROGRAM_EXIT_KEYWORDS", "GTFO")
        print("Parsed GTFO Statement.")

    def parse_switch(self):
        # WTF? OMG <var> blah balh OMGWTF blah balh OIC
        self.match("DEBUGGING_COMMENTS_NONSTANDARD_TOKENS_KEYWORDS", "WTF?")

        # OMG cases
        while self.current_token() and self.current_token()["value"] == "OMG":
            self.match("DEBUGGING_COMMENTS_NONSTANDARD_TOKENS_KEYWORDS", "OMG")
            # <var>
            current_case = self.current_token()
            if current_case["type"] not in ["NUMBER_LITERAL", "STRING_LITERAL", "BOOLEAN_LITERAL", "VARIABLE"]:
                self.syntax_error("Expected a variable after OMG in switch statement")
            self.position += 1 # consume the variable

            # parse statements in case block
            while self.current_token() and self.current_token()["value"] not in ["OMG", "OMGWTF", "OIC"]:
                self.parse_statement()

        # OMGWTF
        if self.current_token() and self.current_token()["value"] == "OMGWTF":
            self.match("DEBUGGING_COMMENTS_NONSTANDARD_TOKENS_KEYWORDS", "OMGWTF")
            
            # parse statements in default block
            while self.current_token() and self.current_token()["value"] != "OIC":
                self.parse_statement()

        # OIC
        if not self.match("CONDITIONALS_KEYWORDS", "OIC"):
            self.syntax_error("Expected OIC to close WTF?")
        
        print("Parsed Switch Statement.")

    # OBTW
    def parse_multiline(self):
        self.match("DEBUGGING_COMMENTS_NONSTANDARD_TOKENS_KEYWORDS", "OBTW")

        # parse all comments 
        while self.current_token() and self.current_token()["value"] != "TLDR":
            self.position += 1 # move the pointer


        # TLDR
        if not self.match("DEBUGGING_COMMENTS_NONSTANDARD_TOKENS_KEYWORDS", "TLDR"):
            self.syntax_error("Expected TLDR to close OBTW comment.")

        print("parsed multiline comment.")
    
    # BTW 
    def parse_singleline(self):
        current = self.current_token()
        if not current:
            return
        
        # get line number of btw, we'll skill everything here 
        start_line = current["line"]

        # BTW
        self.match("DEBUGGING_COMMENTS_NONSTANDARD_TOKENS_KEYWORDS", "BTW")

        # comments
        if self.current_token() and self.current_token()["type"] == "COMMENT":
            print(f"Parsed Single-line comment at line {self.current_token()['line']} with value {self.current_token()['value']}")
            self.match("COMMENT", None) # move the pointer
                  
        # fix for natotokenize yung some parts of the token 
        # i.e x^2 , after nya matokenize as COMMENT: x^2, nagkaka NUMBER: 2
        while self.current_token() and self.current_token()["line"] == start_line:
            # di ko mafigure out pa pano imatch so consume muna (move pointer)
            print(f"Parsed extra token at line {self.current_token()['line']} with value {self.current_token()['value']}")
            self.position += 1

        

    def is_expression_start(self, token):
        if not token:
            return False
        
        # token types that can start an expression
        if token["type"] in ["NUMBER_LITERAL", "STRING_LITERAL", "BOOLEAN_LITERAL", "VARIABLE"]:
            return True
        
        if token["type"] in ["ARITHMETIC_OPERATIONS_KEYWORDS", "LOGIC_AND_COMPARISON_KEYWORDS", "STRING_OPERATIONS_KEYWORDS"]:
            # check specific values to exclude AN/MKAY
            if token["value"] not in [" AN ", " MKAY "]: 
                return True
        return False

    def parse_smoosh(self):
        self.match("STRING_OPERATIONS_KEYWORDS", "SMOOSH")

        # SMOOSH <expr>
        if not self.parse_expression():
            self.syntax_error("Expected first expression after SMOOSH.")

        # other exprs after first, but not ' AN '
        while self.is_expression_start(self.current_token()):
            self.parse_expression() # Consume the next expression
        
        print("Parsed SMOOSH Statement.")
        return True


# get tokens sorted by index per line
def flat_token(tokens):
    flat = []
    for token_line in tokens:
        token_sorted = sorted(token_line, key=lambda x: x['index'])
        for token in token_sorted:
            flat.append(token)
            
    # for token in flat:
    #     print(token)
        
    return flat

def run_tester(verbose=0):
    # list of test cases
    testcases = ['01_variables.lol', '02_gimmeh.lol', '03_arith.lol', 
                 '04_smoosh_assign.lol', '05_bool.lol', '06_comparison.lol',
                 '07_ifelse.lol', '08_switch.lol', '09_loops.lol',
                 '10_functions.lol']

    output_filename = "parser_output.txt"
  
    # get the terminal output
    terminal_output = sys.stdout
    try: 
        with open(output_filename, 'w', encoding='utf-8') as f:
            # redirect stdout to file
            sys.stdout = f
        
            print("running syntactic analyzer test cases")
            print("="*39)

            # iterate thru filenames then call lexical analyzer
            for filename in testcases:
                print("\n")
                print("*"*39)
                print(f"Testing file {filename}")
                print("*"*39)

                # get tokens
                tokens = flat_token(Lexer(filename))

                if verbose == 1:
                    for token in tokens:
                        print(token)

                if tokens is False or not tokens:
                    print(f"Lexical Error: skipping {filename} due to lexical error or no tokens")
                    continue

                print("\nStarting Syntax Analysis")

                # feed tokens to parser
                try:
                    # print("gas0")
                    parser = Parser(tokens)
                    # print("gas5")
                    parser.parse_program()
                    # print("parse done??")
                except SystemExit:
                    # catch sys.exit from syntax error for files that have sys error
                    print(f"Sytax error in file {filename}.")
                except Exception as e:
                    print(f"Unexpected error during the parsing of {filename} Error {e}")
    finally:
        sys.stdout = terminal_output
        print(f"Syntax Analysis complete, Output saved to '{output_filename}")
    
    return None

if __name__ == "__main__":
# Tentative menu for checking
    while(1):
        print('''
            [1] Run Test Cases
            [2] Run Test Cases (with Lex Tokens displayed)  
            [3] Choose file  
            [0] Exit
            ''')
        choice = input("Enter choice: ")

        if (choice == '1'):
            # run test call
            run_tester()
        elif (choice == '2'):
            # verbose toggled
            run_tester(1)
        elif (choice == '3'):
            filename = input("Enter filename: ")
            tokens = flat_token(Lexer(filename)) 
            # verbose default
            for token in tokens:
                        print(token)
            if tokens:
                print("\n Syntax Analysis for file")
                try:
                    parser = Parser(tokens)
                    parser.parse_program()
                except SystemExit:
                    # catch sys.exit from syntax error for files that have sys error
                    print(f"Sytax error in file {filename}.")
                except Exception as e:
                    print(f"Unexpected error during the parsing of {filename}. Error {e}")
                
        elif (choice == '0'):
            print("k thnx bye")
            sys.exit(1)
        else:
            print("Invalid Input")