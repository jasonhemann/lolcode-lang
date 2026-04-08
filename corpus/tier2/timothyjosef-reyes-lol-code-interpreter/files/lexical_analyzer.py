import re
import sys

# lists of keywords and their specific types
lolcode_keywords = [
    ["PROGRAM_STRUCTURE_DELIMITERS_KEYWORDS",
        "KTHXBYE",
        "WAZZUP",
        "BUHBYE",
        "HAI"
    ],

    ["DATA_TYPES",
        "NUMBAR",
        "TROOF",
        "NUMBR",
        "NOOB",
        "YARN"
    ],

    ["VARIABLE_DECLARATION_AND_ASSIGNMENT_KEYWORDS",
        "IS NOW A",
        "I HAS A",
        "ITZ",
        " R "
    ],

    ["ARITHMETIC_OPERATIONS_KEYWORDS",
        "QUOSHUNT OF",
        "PRODUKT OF",
        "SMALLR OF",
        "BIGGR OF",
        "DIFF OF",
        "SUM OF",
        "MOD OF",
        " AN "
    ],

    ["LOGIC_AND_COMPARISON_KEYWORDS",
        "BOTH SAEM",
        "EITHER OF",
        "DIFFRINT",
        "BOTH OF",
        "WON OF",
        "ANY OF",
        "ALL OF",
        "NOT"
    ],

    ["STRING_OPERATIONS_KEYWORDS",
        "SMOOSH"
    ],

    ["INPUT_OUTPUT_KEYWORDS",
        "VISIBLE",
        "GIMMEH",
        "IT"
    ],

    ["CONDITIONALS_KEYWORDS",
        "O RLY?",
        "YA RLY",
        "NO WAI",
        "MEBBE",
        "OIC"
    ],

    ["LOOPS_KEYWORDS",
        "IM OUTTA YR",
        "NERFIN YR",
        "IM IN YR",
        "UPPIN YR",
        "WILE",
        "TIL",
    ],
    
    ["FUNCTIONS_KEYWORDS",
        "IF U SAY SO",
        "HOW IZ I",
        "FOUND YR",
        "MKAY",
        "I IZ",
        "YR"
    ],

    ["PROGRAM_EXIT_KEYWORDS",
        "GTFO"
    ],

    ["DEBUGGING_COMMENTS_NONSTANDARD_TOKENS_KEYWORDS",
        "OMGWTF",
        "WTF?",
        "OMG"
    ],
    
    # remove "A" for easier lexcode analysis, just check for it in the syntax analyzer
    ["TYPE_CASTING_CONVERSION_KEYWORDS",
        "MAEK",
        " A "
    ]
]

def remove_nested_tokens(tokens):
    cleaned = []

    for token in tokens:
        start, end = token["index"], token["end"]
        length = end - start
        nested = False

        for other in tokens:
            if token is other:
                continue

            o_start, o_end = other["index"], other["end"]
            o_length = o_end - o_start

            # If other token is larger
            if o_length > length:
                # Check overlap: [start,end) intersects [o_start,o_end)
                if not (end <= o_start or start >= o_end):
                    nested = True
                    break

        if not nested:
            cleaned.append(token)

    return cleaned


# Main lexical analyzer function
def lex_analysis(source_code):
    tokens = []
    
    # Containers for the different classifications
    keywords = []
    variables = []
    functions = []
    loops = []
    parameters = []
    string_literals = []
    number_literals = []
    boolean_literals = []

    # for error printing
    errors = []
    
    # Regex patterns for the different classifications
    # keywords_pattern = r"\b[A-Z](?:[ ]|[A-Z])*\b"
    string_pattern = r'"([^"]*)"'
    number_pattern = r"\b-?[0-9]+(?:\.[0-9]+)?\b"
    boolean_pattern = r"\b(WIN|FAIL)\b"
    
    lines = source_code.split("\n")  # break into lines
            
    obtw = False

    # Iterate over each line
    for line_num, line in enumerate(lines, start=1):
        
        tokens_line = []
        
        line = line.strip()
        # will be continuously be replaced with nothing
        lexeme_check = line
        
        if line == "OBTW":
            lexeme_check = lexeme_check.replace(line, "")
            obtw = True
            continue
        
        if line == "TLDR":
            lexeme_check = lexeme_check.replace(line, "")
            obtw = False
            continue

        if obtw:
            lexeme_check = lexeme_check.replace(line, "")
            
        if "BTW" in line:
            index = line.find("BTW")
            lexeme_check = lexeme_check.replace(line[index:len(line)], "")
            line = line.replace(line[index:len(line)], "")

        if line in variables:
            index = line.find(line)
            add_token(tokens_line, "VARIABLE_USAGE", line, line_num, index, index+len(line))
            lexeme_check = lexeme_check.replace(line, "")
        
        # Find all matches for each pattern
        # keyword_matches = re.findall(keywords_pattern, line)
        string_matches = re.findall(string_pattern, line)
        string_indices = [match.start() for match in re.finditer(string_pattern, line)]
        number_matches = re.findall(number_pattern, line)
        number_indices = [match.start() for match in re.finditer(number_pattern, line)]
        boolean_matches = re.findall(boolean_pattern, line)
        boolean_indices = [match.start() for match in re.finditer(boolean_pattern, line)]
        concat_matches = re.findall(r"\s\+\s", line)
        concat_indices = [match.start() for match in re.finditer(r"\s\+\s", line)]
        
        # Add matches to respective lists
        for keyword_type in lolcode_keywords: # changed to use LOL_Keyword set
            for keyword in keyword_type:
                if keyword in line:
                    keywords.append(keyword)
                    matches = re.findall(keyword, line)
                    indices = [match.start() for match in re.finditer(keyword, line)]
                    for i, match in enumerate(matches):
                        add_token(tokens_line, keyword_type[0], match, line_num, indices[i], indices[i]+len(match)) # add to token list for parser
                        lexeme_check = lexeme_check.replace(keyword, "")
        
        for i, match in enumerate(concat_matches):
            keywords.append(match)
            index = concat_indices[i]
            add_token(tokens_line, "CONCATENATION", match, line_num, index, index+len(match))
            lexeme_check = lexeme_check.replace(" + ", "")
        for i, match in enumerate(string_matches):
            string_literals.append(match)
            index = string_indices[i]
            add_token(tokens_line, "STRING_LITERAL", match, line_num, index, index+len(match)) #####
            lexeme_check = lexeme_check.replace("\""+match+"\"", "")
        for i, match in enumerate(number_matches):
            number_literals.append(match)
            index = number_indices[i]
            add_token(tokens_line, "NUMBER_LITERAL", match, line_num, index, index+len(match)) #####
            lexeme_check = lexeme_check.replace(match, "")
        for i, match in enumerate(boolean_matches):
            boolean_literals.append(match)
            index = boolean_indices[i]
            add_token(tokens_line, "BOOLEAN_LITERAL", match, line_num, index, index+len(match)) #####
            lexeme_check = lexeme_check.replace(match, "")
        
        # variable declarations
        if "I HAS A" in line:
            declaration = line.strip().split()
            if len(declaration) > 3:
                variables.append(declaration[3])
                index = line.find(declaration[3])
                add_token(tokens_line, "VARIABLE_DECLARATION", declaration[3], line_num, index, index+len(declaration[3]))
                lexeme_check = lexeme_check.replace(declaration[3], "")

        # function declarations
        if "HOW IZ I" in line:
            declaration = line.strip().split()
            if len(declaration) > 3:
                functions.append(declaration[3])
                index = line.find(declaration[3])
                add_token(tokens_line, "FUNCTIONS_DECLARATIONS", declaration[3], line_num, index, index+len(declaration[3]))
                lexeme_check = lexeme_check.replace(declaration[3], "")
                for i in range(4, len(declaration)):
                    if declaration[i] == "YR":
                        parameters.append(declaration[i+1])
                        index = line.find(declaration[i])
                        add_token(tokens_line, "FUNCTIONS_KEYWORDS", declaration[i], line_num, index, index+len(declaration[i]))
                        lexeme_check = lexeme_check.replace(declaration[i], "")
                        index = line.find(declaration[i+1])
                        add_token(tokens_line, "FUNCTIONS_PARAMETERS", declaration[i+1], line_num, index, index+len(declaration[i+1]))
                        lexeme_check = lexeme_check.replace(declaration[i+1], "")

        # loop declarations
        if "IM IN YR" in line:
            declaration = line.strip().split()
            if len(declaration) > 3:
                loops.append(declaration[3])
                index = line.find(declaration[3])
                add_token(tokens_line, "LOOP_DECLARATION", declaration[3], line_num, index, index+len(declaration[3]))
                lexeme_check = lexeme_check.replace(declaration[3], "")
        
        for variable in sorted(variables, key=len, reverse=True):
            if variable in lexeme_check:
                matches = re.findall(variable, line)
                indices = [match.start() for match in re.finditer(variable, line)]
                for i, match in enumerate(matches):
                    add_token(tokens_line, "VARIABLE", match, line_num, indices[i], indices[i]+len(match))
                    lexeme_check = lexeme_check.replace(variable, "")
            
        for function in sorted(functions, key=len, reverse=True):
            if function in lexeme_check:
                matches = re.findall(function, line)
                indices = [match.start() for match in re.finditer(function, line)]
                for i, match in enumerate(matches):
                    add_token(tokens_line, "FUNCTION", match, line_num, indices[i], indices[i]+len(match))
                    lexeme_check = lexeme_check.replace(function, "")
            
        for parameter in sorted(parameters, key=len, reverse=True):
            if parameter in lexeme_check:
                matches = re.findall(parameter, line)
                indices = [match.start() for match in re.finditer(parameter, line)]
                for i, match in enumerate(matches):
                    add_token(tokens_line, "PARAMETER", match, line_num, indices[i], indices[i]+len(match))
                    lexeme_check = lexeme_check.replace(parameter, "")
            
        for loop in sorted(loops, key=len, reverse=True):
            if loop in lexeme_check:
                matches = re.findall(loop, line)
                indices = [match.start() for match in re.finditer(loop, line)]
                for i, match in enumerate(matches):
                    add_token(tokens_line, "LOOP", match, line_num, indices[i], indices[i]+len(match))
                    lexeme_check = lexeme_check.replace(loop, "")
        
        tokens.append(tokens_line)
        
        lexeme_check = lexeme_check.replace(" ", "")
        if lexeme_check:
            print(lexeme_check)
        # if non empty line but no tokes found, append error emssage
        if line and lexeme_check:
            errors.append(f"Lexical error at line {line_num}: {line}")

    # prints errors and exits if there are any
    if errors:
        print("Lexical Errors Found: ")
        for err in errors:
            print(err)
    
    # Print the results
    # print("Keywords:", keywords)
    # print("variable Identifiers:", variables)
    # print("Function Identifiers:", functions)
    # print("Loop Identifiers:", loops)
    # print("Parameters", parameters)
    # print("String Literals:", string_literals)
    # print("Number Literals:", number_literals)
    # print("Boolean Literals:", boolean_literals)
    for i in range(len(tokens)):
        if tokens[i]:
            tokens[i] = remove_nested_tokens(tokens[i])

    # feed tokens to parser
    return tokens, errors

def run_tester():
    # list of test cases
    testcases = ['01_variables.lol', '02_gimmeh.lol', '03_arith.lol', 
                 '04_smoosh_assign.lol', '05_bool.lol', '06_comparison.lol',
                 '07_ifelse.lol', '08_switch.lol', '09_loops.lol',
                 '10_functions.lol']
    
    print("Running lexical analyzer test cases")
    # iterate thru filenames then call lexical analyzer
    for filename in testcases:
        print("\n")
        print("*"*39)
        print(f"Testing file {filename}")
        print("*"*39)
        result = lex_analysis(filename)

        if result is False:
            print(f"Skipping {filename} due to error\n")

    return None

# def
def add_token(tokens_line, token_type, value, line_num, index, end):
    tokens_line.append({"type": token_type, "value": value, "line": line_num, "index": index, "end":end})


# if __name__ == "__main__":
# # Tentative menu for checking
#     while(1):
#         print('''
#             [1] Run Test Cases
#             [2] Choose File
#             [0] Exit
#             ''')
#         choice = input("Enter choice: ")
#         if (choice == '1'):
#             # run test call
#             run_tester()
#         elif (choice == '2'):
#             # Get user input of file name
#             file = input("Enter filename: ")
#             # Call lexical analyzer
#             lex_analysis(file)
#         elif (choice == '0'):
#             print("k thnx bye")
#             sys.exit(1)
#         else:
#             print("Invalid Input")


