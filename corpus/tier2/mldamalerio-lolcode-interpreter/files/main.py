"""
    CMSC 124 - Project (BTW_BEST_GROUP)
    Authors:
        >>> Damalerio, Mark Lewis
        >>> Sorinio, Nicole Angela
    Description:
        This project simulates a LOLCode Interpreter with a graphical user interface.
"""

# IMPORTS
import re                   # RegEx
from copy import deepcopy   # To copy array without reference
from class_line import *    # For line class

# GUI components
from tkinter import *
from tkinter import ttk
from tkinter import simpledialog
from tkinter import filedialog

# LEXEME DESCRIPTIONS
keyword_description = {
    "HAI": "Start of the program",
    "KTHXBYE": "End of the program", 
    "BTW": "Single-line comment", 
    "OBTW": "Start of multi-line comment", 
    "I HAS A": "Variable declaration", 
    "TLDR": "End of multi-line comment", 
    "ITZ": "Variable initialization",
    "R": "Assignment operation", 
    "SUM OF": "Addition operation", 
    "DIFF OF": "Subtraction operation",
    "PRODUKT OF": "Multiplication operation", 
    "QUOSHUNT OF": "Division operation", 
    "MOD OF": "Modulo operation", 
    "BIGGR OF": "MAX operation", 
    "SMALLR OF": "MIN operation", 
    "BOTH OF": "AND Boolean operation", 
    "EITHER OF": "OR Boolean operation", 
    "WON OF": "XOR Boolean operation", 
    "MAEK": "Explicit typecasting", 
    "IS NOW A": "Re-casting a variable", 
    "VISIBLE": "Print to the terminal", 
    "GIMMEH": "Accept input", 
    "O RLY\?": "Start of IF-THEN statement", 
    "YA RLY": "Start of IF code block", 
    "MEBBE": "", 
    "NO WAI": "Start of ELSE code block", 
    "OIC": "End of IF-THEN/SWITCH-CASE statement", 
    "WTF\?": "Start of SWITCH-CASE statements", 
    "OMG": "Denotes SWITCH-CASE case", 
    "OMGWTF": "SWITCH-CASE default case", 
    "IM IN YR": "Start of loop", 
    "UPPIN": "Increment by 1", 
    "NERFIN": "Decrement by 1", 
    "YR": "Indicates variable to modify in loop", 
    "TIL": "Loop as long as <expression> is FAIL", 
    "WILE": "Loop as long as <expression> is WIN", 
    "IM OUTTA YR": "End of loop", 
    "AN": "Operand separator", 
    "SMOOSH": "String concatenation", 
    "ALL OF": "Infinite arity AND Boolean operation", 
    "ANY OF": "Infinite arity OR Boolean operation", 
    "NOT": "NOT Boolean operation", 
    "BOTH SAEM": "== Comparison operator", 
    "DIFFRINT": "!= Comparison operator", 
    "GTFO": "Break keyword"
}
yarn_description = "String Literal"
numbr_description = "Integer Value"
numbar_description = "Float Value"
troof_description = "Boolean Value"
type_description = "Type Literal"
identifier_description = "Variable Identifier"

INVALID = ["INVALID", "INVALID"]
ZERO = [0, 0]
TYPECAST_ERROR = ["TYPECAST", "TYPECAST"]

# get the token data structure from lines
def get_token_from_lines(lines):
    # original_lines = deepcopy(lines)    # keep a copy of original lines
    length_lines = len(lines)           # take note of the length of the array lines, will be updated once comments are removed

    #Regexes for the classification of lexemes
    obtw_regex = fr"(?<![^\s])(OBTW)\s*((?!TLDR)(.|\s))*\s*(TLDR)(?![^\s])"
    btw_regex = fr"(?<![^\s])(BTW( .*)?(?![^\s]))"
    keyword_regex = fr"(?<![^\s])(HAI|KTHXBYE|BTW|OBTW|I HAS A|A|TLDR|ITZ|R|SUM OF|DIFF OF|PRODUKT OF|QUOSHUNT OF|MOD OF|BIGGR OF|SMALLR OF|BOTH OF|EITHER OF|WON OF|MAEK|IS NOW A|VISIBLE|GIMMEH|O RLY\?|YA RLY|MEBBE|NO WAI|OIC|WTF\?|OMG|OMGWTF|IM IN YR|UPPIN|NERFIN|YR|TIL|WILE|IM OUTTA YR|AN|SMOOSH|ALL OF|ANY OF|NOT|BOTH SAEM|DIFFRINT|GTFO|MKAY)(?![^\s])"
    yarn_regex = fr'(?<![^\s])"[^"]*"(?![^\s])'
    numbr_regex = fr'(?<!\w|\.)-?[0-9]+(?!\w|\.)'
    numbar_regex = fr'(?<!\w|\.)(-?\d*\.\d+)(?!\w|\.)'
    troof_regex = fr'(?<![^\s])(WIN|FAIL)(?![^\s])'
    type_regex = fr'(?<![^\s])(YARN|NUMBR|NUMBAR|TROOF|NOOB)(?![^\s])'
    identifier_regex = fr'(?<![^\s])([a-zA-Z][a-zA-Z0-9_]*)(?![^\s])'
    valid_regex = fr"{keyword_regex}|{yarn_regex}|{numbr_regex}|{numbar_regex}|{troof_regex}|{type_regex}|{identifier_regex}"

    #Pattern for regexes defined above.
    obtw_pattern = re.compile(obtw_regex)
    keyword_pattern = re.compile(keyword_regex)
    yarn_pattern = re.compile(yarn_regex)
    numbr_pattern = re.compile(numbr_regex)
    numbar_pattern = re.compile(numbar_regex)
    troof_pattern = re.compile(troof_regex)
    type_pattern = re.compile(type_regex)
    identifier_pattern = re.compile(identifier_regex)
    valid_pattern = re.compile(valid_regex)

    #Array of valid lexemes
    valid_lexemes = []

    #Array of line objects
    line_objects = []

    #Array of lexemes: grouped
    keywords, yarns, numbrs, numbars, troofs, types, identifiers = [],[],[],[],[],[],[]

    #Lines indexing
    i = 0
    line_num = 0

    #Invalid checking
    invalid = False

    #Go through line per line, check for valid lexemes.
    while(1):

        #Check if we exhausted all of the lines. If true, end checking for lexemes
        if i == length_lines:
            break
        #There's an invalid token detected, end loop, don't continue checking for lexemes
        if invalid == True:
            break

        #Will contain the lexemes in one line, will be appended to valid_lexemes IF there's no invalid token.
        valid_lexemes_oneline = []

        #The while loop will continue searching for lexemes in one line until it does not read a match anymore.
        while(1):

            #From the valid_regex, get one valid lexeme (ANY).
            valid_match = valid_pattern.search(lines[i])

            #The regex caught a match.
            if valid_match:
                match_as_string = str(valid_match.group(0))     #Convert to match object to string

                #Determine the lexeme's classification caught as VALID
                #The lexeme will fall into one of these classifications
                keyword_match = keyword_pattern.search(match_as_string)
                yarn_match = yarn_pattern.search(match_as_string)
                numbr_match = numbr_pattern.search(match_as_string)
                numbar_match = numbar_pattern.search(match_as_string)
                troof_match = troof_pattern.search(match_as_string)
                type_match = type_pattern.search(match_as_string)
                identifier_match = identifier_pattern.search(match_as_string)

                #The detected lexeme is a KEYWORD.
                if keyword_match:
                    
                    valid_lexemes_oneline.append(match_as_string)       #Add the lexeme to valid_lexemes_oneline
                    keywords.append(match_as_string)                    #Add lexeme to its group

                    #We detected a oneline comment, we will remove it from the line since the texts after it can include anything
                    if match_as_string == "BTW":
                        lines[i] = re.sub(btw_regex, "", lines[i], 1)

                    #We detected a multiline comment, we will remove it from the line since the texts after it can include anything
                    elif match_as_string == "OBTW":
                        #Since OBTW is multiline, we need to remove also the lines after it.
                        #Convert the lines array to a string first.
                        #Make a copy of the following lines to lines[i] as string. 
                        lines_as_string = "\n".join(lines)
                        match = obtw_pattern.search(lines_as_string)

                        string_match = str(match.group(0))

                        #Check if OBTW has a corresponding TLDR

                        #HAS corresponding TLDR, valid.
                        if match:
                            valid_lexemes_oneline.append("TLDR")
                            keywords.append("TLDR")
                            lines_as_string = re.sub(obtw_regex, "", lines_as_string, 1)   
                            lines = lines_as_string.split("\n")                         #Convert lines as string to array again
                            length_lines = len(lines)                                   #Change the length of lines since we removed lines
                            line_num += string_match.count("\n")

                        #NO TLDR, invalid
                        else:
                            obtw_invalid = "Keyword OBTW on line " + str(line_num + 1) + " has no corresponding TLDR."
                            print(obtw_invalid)
                            invalid = True
                            break

                    #TLDR has no corresponding OBTW, invalid.
                    elif match_as_string == "TLDR":
                        tldr_invalid = "Keyword TLDR on line " + str(line_num + 1) + " has no corresponding OBTW."
                        invalid = True
                        break

                    #Keyword is neither BTW nor OBTW. Just remove the keyword from line.
                    else:
                        lines[i] = re.sub(fr"(?<![^\s]){keyword_regex}(?![^\s])", "", lines[i], 1)

                #The detected lexeme is a YARN.
                elif yarn_match:
                    valid_lexemes_oneline.append(match_as_string)
                    yarns.append(match_as_string)
                    lines[i] = re.sub(fr"(?<![^\s]){yarn_regex}(?![^\s])", "", lines[i], 1)

                #The detected lexeme is a NUMBR.
                elif numbr_match:
                    valid_lexemes_oneline.append(match_as_string)
                    numbrs.append(match_as_string)
                    lines[i] = re.sub(fr"(?<![^\s]){match_as_string}(?![^\s])", "", lines[i], 1)

                #The detected lexeme is a NUMBAR.
                elif numbar_match:
                    valid_lexemes_oneline.append(match_as_string)
                    numbars.append(match_as_string)
                    lines[i] = re.sub(fr"(?<![^\s]){match_as_string}(?![^\s])", "", lines[i], 1)
                
                #The detected lexeme is a TROOF.
                elif troof_match:
                    valid_lexemes_oneline.append(match_as_string)
                    troofs.append(match_as_string)
                    lines[i] = re.sub(fr"(?<![^\s]){match_as_string}(?![^\s])", "", lines[i], 1)
                
                #The detected lexeme is a TYPE LITERAL.
                elif type_match:
                    valid_lexemes_oneline.append(match_as_string)
                    types.append(match_as_string)
                    lines[i] = re.sub(fr"(?<![^\s]){match_as_string}(?![^\s])", "", lines[i], 1)
                
                #The detected lexeme is n IDENTIFIER.
                elif identifier_match:
                    valid_lexemes_oneline.append(match_as_string)
                    identifiers.append(match_as_string)
                    lines[i] = re.sub(fr"(?<![^\s]){match_as_string}(?![^\s])", "", lines[i], 1)

            #The line does not have a valid lexeme OR the line is already empty.
            else:
                #Check if the line still has content.
                #If it has content, it is invalid.
                if lines[i] != "":
                    split_line = lines[i].split()
                    if len(split_line) != 0:
                        for j in split_line:
                            invalid_message = str(j) + " on line " + str(line_num + 1) + " is invalid."
                            print(invalid_message)
                        invalid = True
                break

        
        #Create a line object
        line = Line(line_num+1, valid_lexemes_oneline)  # args = line_number, line_array
        line_objects.append(line)
        valid_lexemes.append(valid_lexemes_oneline)     #Append the lexemes detected in the line
        i += 1                                          #Increment i (indexing for lines) to go to the next line\
        line_num += 1

    #There are no invalid lexemes. Return:
    #   >>> valid_lexemes_dictionary = dictionary of lexemes classified into groups
    #   >>> valid_lexemes = array of array of lexemes per line
    if invalid == False:
        valid_lexemes_dictionary = {
            "keywords": keywords,
            "yarns": yarns,
            "numbrs": numbrs,
            "numbars": numbars,
            "troofs": troofs,
            "type_literals": types,
            "identifiers": identifiers
        }

        #Pass the values dictionary to every line
        for line_object in line_objects:
            line_object.get_dictionary(valid_lexemes_dictionary)

        #Print results for reference
        # print("\n\nvalid_lexemes_dictionary (dictionary)")
        # for k, v in valid_lexemes_dictionary.items():
        #     print(k, " : ", v)
        # print("\nvalid_lexemes (2d array)")
        # print_2d(valid_lexemes)
        return (valid_lexemes_dictionary, valid_lexemes, line_objects)

    #Code has invalid tokens. Return None.
    else:
        print("Code has invalid tokens.")
        return None

#Open a lol file and put the content in the text box
def open_lol_file():
    # clear the text box
    def clear_text_box():
        code_text_box.delete(1.0, END)

    # get the text of the chosen file
    def get_text_of_current_file():
        code = ""
        with open(f"{CURRENT_FILE}", mode="r") as file:
            for line in file:
                code += line
        
        return code

    try:
        # get the filename of the chosen file (path to filename)
        CURRENT_FILE = filedialog.askopenfilename(initialdir="./", title="Select Input", filetypes=(("input file", "*.lol"), ("all files", "*.*")))
        clear_text_box()                    # clear the text box first
        code = get_text_of_current_file()   # get the code
        code_text_box.insert(END, code)     # insert the code to the text box
        print(f"LOADED = {CURRENT_FILE}")

    except:
        CURRENT_FILE = None
        clear_text_box()
        code_text_box.insert(END, "")
        print("Closed File Dialog")

#Run when execute button is clicked
def execute_code():

    # clear terminal if there are content
    console.clear_terminal()

    # get the lines of code in list
    code_in_string = code_text_box.get("1.0",END)  # get the string of textbox
    code_in_lines = code_in_string.split("\n")  # create a list separated by \n

    # clean the whitespace in lines
    for i in range(len(code_in_lines)):
        code_in_lines[i] = code_in_lines[i].strip()


    #   _               _           _                        _           _     
    #  | |             (_)         | |     /\               | |         (_)    
    #  | |     _____  ___  ___ __ _| |    /  \   _ __   __ _| |_   _ ___ _ ___ 
    #  | |    / _ \ \/ / |/ __/ _` | |   / /\ \ | '_ \ / _` | | | | / __| / __|
    #  | |___|  __/>  <| | (_| (_| | |  / ____ \| | | | (_| | | |_| \__ \ \__ \
    #  |______\___/_/\_\_|\___\__,_|_| /_/    \_\_| |_|\__,_|_|\__, |___/_|___/
    #                                                           __/ |          
    #                                                          |___/           
                 
    # Get code from textbox
    return_result = get_token_from_lines(code_in_lines)
    result = ""     #Temporary value
    lexeme_lines = ""

    # Code has no invalid tokens.
    if return_result != None:
        result = return_result[0]
        lexeme_lines = return_result[1]
        line_objects = return_result[2]

    # Code has invalid tokens.
    else:
        result = return_result
        

    # check if there is an error
    if result == None:
        print("Invalid token!")
    else:
        
        # insert lexeme to table ui
        insert_lexeme_table_to_ui(result)
        print("\nLEXICAL ANALYSIS DONE!\n")
        
        #    _____             _                _____ _                  _             
        #   / ____|           | |              / ____| |                (_)            
        #  | (___  _   _ _ __ | |_ __ ___  __ | |    | | ___  __ _ _ __  _ _ __   __ _ 
        #   \___ \| | | | '_ \| __/ _` \ \/ / | |    | |/ _ \/ _` | '_ \| | '_ \ / _` |
        #   ____) | |_| | | | | || (_| |>  <  | |____| |  __/ (_| | | | | | | | | (_| |
        #  |_____/ \__, |_| |_|\__\__,_/_/\_\  \_____|_|\___|\__,_|_| |_|_|_| |_|\__, |
        #           __/ |                                                         __/ |
        #          |___/                                                         |___/ 
 
        # START OF SYNTAX CLEANING

        # Allowed lines before HAI and after KTHXBYE, and
        # lines that won't intefere with the other lines of code
        #   >> ["BTW"]
        #   >> ["OBTW", "TLDR"]
        #   >> []

        remove_indices= []
        for i in range(len(line_objects)):
            if line_objects[i].line_array == ["BTW"] or line_objects[i].line_array == ["OBTW", "TLDR"] or line_objects[i].line_array == []:
                remove_indices.append(i)
        for i in range(len(remove_indices) - 1, -1, -1):
            line_objects.pop(remove_indices[i])
        
        # Remove trailing BTW comments from line objects
        #   FROM >> ["I HAS A", "identifier", "BTW"]
        #   TO   >> ["I HAS A", "identifier"]

        clean_line_objects = []
        for i in range(len(line_objects)):
            if (line_objects[i].line_array[-1] == 'BTW'):  # if the last element is a BTW comment
                line_objects[i].line_array = line_objects[i].line_array[0:len(line_objects[i].line_array) - 1]  # modify that list
                clean_line_objects.append(line_objects[i])
                continue
            clean_line_objects.append(line_objects[i])

        print("\nSYNTAX CLEANING DONE!\n")
        
        #    _____             _                                    _           _     
        #   / ____|           | |                 /\               | |         (_)    
        #  | (___  _   _ _ __ | |_ __ ___  __    /  \   _ __   __ _| |_   _ ___ _ ___ 
        #   \___ \| | | | '_ \| __/ _` \ \/ /   / /\ \ | '_ \ / _` | | | | / __| / __|
        #   ____) | |_| | | | | || (_| |>  <   / ____ \| | | | (_| | | |_| \__ \ \__ \
        #  |_____/ \__, |_| |_|\__\__,_/_/\_\ /_/    \_\_| |_|\__,_|_|\__, |___/_|___/
        #           __/ |                                              __/ |          
        #          |___/                                              |___/           


        # START OF SYNTAX ANALYSIS
        check_semantics = deepcopy(line_objects)  # create a copy of lines (not normalized) for semantic analysis later
        conditional_stack = []  # stack to check syntax of conditional statements
        loop_stack = []  # stack to check syntax of loop statements
        symbol_table = dict()  # symbol table
        cases_stack = []
        cases_stack_copy = []


        # initialize the IT variable
        IT = "NOOB"
        IT_VALUE = "NOOB"
        there_is_conditional = False    # flag for conditional
        do_not_run_yarly = False        # flag for if
        do_not_run_nowai = False        # flag for else
        case_activated = False          # flag for switch case
        starting_loop_index = None

        LOOP_VARIABLE = None
        LOOP_OPERATION = None
        CONTINUE_LOOP = None

        LOOPED = 0

        # function to check if code should be skipped (used by if else)
        def check_code_skip():
            skip_code = False

            # DO NOT RUN THIS CODE (inside IF)
            if (there_is_conditional and do_not_run_yarly):
                if (conditional_stack[0] == "YA RLY"):
                    print("SKIP YARLY!")
                    skip_code = True

            # DO NOT RUN THIS CODE (inside ELSE)
            if (there_is_conditional and do_not_run_nowai):
                if (conditional_stack[0] == "NO WAI"):
                    print("SKIP NOWAI!")
                    skip_code = True
                    

            return skip_code

        # function to check if code should be skipped (used by case)
        def check_case():
            skip_code = False

            if (there_is_conditional and case_activated):
                # check if current case is the case, if not, skip code

                # default case
                if (IT_VALUE != "NOOB") and (cases_stack[0] == "OMGWTF") and (IT_VALUE not in cases_stack_copy):
                    return False

                # this is the case
                if (cases_stack[0] == IT_VALUE):
                    return False
                
                # not the case
                if (not cases_stack[0] == IT_VALUE):
                    # print(f"SKIP THIS CASE {cases_stack[0]}!")
                    return True

            return skip_code

    
        # normalize the lines
        # print(f"LINE OBJECTS (no comments): ({len(line_objects)} lines)")
        for i in range(len(line_objects)):
            line_objects[i].normalize_line(check_semantics[i], console)

        code_syntax_valid = True

        if (len(line_objects) == 0 or len(line_objects) == 1):
            code_syntax_valid = False
            print("INVALID CODE! HAI KTHXBYE ERROR")
            console.append_terminal(f"INVALID CODE! HAI KTHXBYE ERROR\n")

        
        #   _      _                   _                       
        #  | |    (_)                 | |                      
        #  | |     _ _ __   ___  ___  | |     ___   ___  _ __  
        #  | |    | | '_ \ / _ \/ __| | |    / _ \ / _ \| '_ \ 
        #  | |____| | | | |  __/\__ \ | |___| (_) | (_) | |_) |
        #  |______|_|_| |_|\___||___/ |______\___/ \___/| .__/ 
        #                                               | |    
        #                                               |_|    

        # MAIN LOOP OF CHECKING EVERY LINE
        i = 0
        starting_loop_index = None

        # print error to console
        def print_error(error_text, line_number):
            print(f"line {line_number}: {error_text}")
            console.append_terminal(f"line {line_number}: {error_text}\n")

        # for i in range(len(line_objects)):
        while (i < len(line_objects)):

            # use line to reference the line
            line = line_objects[i]
            complete_line = check_semantics[i]
            line_valid = False

            # DONE
            # Check program start (HAI)
            if (i == 0):
                if line.check_hai():
                    line_valid = True
                    i += 1
                    continue
                else:
                    print_error("INVALID HAI", line.line_number)
                    line_valid = False
                    code_syntax_valid = False
                    break
            
            # DONE
            # Check program end (KTHXBYE)
            if (i == len(line_objects)-1):
                if line.check_kthxbye():
                    line_valid = True
                    i += 1
                    continue
                else:
                    print_error("INVALID KTHXBYE", line.line_number)
                    line_valid = False
                    code_syntax_valid = False
                    break
            
            # Check variable declaration (I HAS A)
            variable_return = line.check_variable_declaration(complete_line, symbol_table)
            # print(f"I HAS A: {variable_return}")
            if (variable_return):
                line_valid = True
                
                if (check_code_skip()):
                    i += 1
                    continue

                if (check_case()):
                    i += 1
                    continue

                # check if invalid
                if variable_return == INVALID:
                    line_valid = False
                    code_syntax_valid = False
                    print_error("IDENTIFIER IS UNDEFINED", line.line_number)
                    break
                if variable_return == TYPECAST_ERROR:
                    line_valid = False
                    code_syntax_valid = False
                    print_error("TYPECAST ERROR", line.line_number)
                    break

                return_type = variable_return[0]
                temp_identifier = variable_return[1]
                temp_value = "NOOB"

                # if initialization (have ITZ keyword)
                if return_type == 1:
                    temp_value = variable_return[2]

                symbol_table[temp_identifier] = temp_value

                i += 1
                continue
     
            # TODO: recast to TROOF (WIN|FAIL)
            # Check variable recasting (IS NOW A)
            recast_return = line.check_variable_recast(complete_line)
            if (recast_return):
                line_valid = True

                if (check_code_skip()):
                    i += 1
                    continue

                if (check_case()):
                    i += 1
                    continue

                # ex. [identifier_to_change, "IS NOW A", new_type]
                identifier_to_change = recast_return[0]
                new_type = recast_return[1]

                # change value of identifier if it exists
                if identifier_to_change in symbol_table.keys():

                    try:
                        if new_type == "NUMBR":
                            stripped = symbol_table[identifier_to_change]
                            if isinstance(symbol_table[identifier_to_change], str):
                                stripped = symbol_table[identifier_to_change].strip('"')
                            symbol_table[identifier_to_change] = int(stripped)
                        elif new_type == "NUMBAR":
                            stripped = symbol_table[identifier_to_change]
                            if isinstance(symbol_table[identifier_to_change], str):
                                stripped = symbol_table[identifier_to_change].strip('"')
                            symbol_table[identifier_to_change] = float(stripped)
                        elif new_type == "TROOF":
                            to_change = symbol_table[identifier_to_change]
                            test = to_boolean(to_change)
                            if test:
                                symbol_table[identifier_to_change] = "WIN"
                            else:
                                symbol_table[identifier_to_change] = "FAIL"
                        elif new_type == "YARN":
                            symbol_table[identifier_to_change] = str(symbol_table[identifier_to_change])
                    except:
                        line_valid = False
                        code_syntax_valid = False
                        print_error("RECASTING ERROR", line.line_number)
                        break
                    
                    i += 1
                    continue
                else:
                    line_valid = False
                    code_syntax_valid = False
                    print_error("IDENTIFIER IS NOT DECLARED BEFORE RECASTING", line.line_number)
                    break

            # TODO: recast to TROOF (WIN|FAIL)
            # Check variable recasting (MAEK)
            typecast_return = line.check_variable_typecast(complete_line)
            if (typecast_return):
                line_valid = True

                if (check_code_skip()):
                    i += 1
                    continue

                if (check_case()):
                    i += 1
                    continue

                # ex. [MAEK, identifier_to_change, "A", new_type]
                # or [MAEK, identifier_to_change, new_type]
                identifier_to_change = typecast_return[0]
                new_type = typecast_return[1]

                # change value of identifier if it exists
                if identifier_to_change in symbol_table.keys():

                    try:
                        if new_type == "NUMBR":
                            if isinstance(symbol_table[identifier_to_change], str):
                                stripped = symbol_table[identifier_to_change].strip('"')
                            symbol_table[identifier_to_change] = int(stripped)
                        elif new_type == "NUMBAR":
                            if isinstance(symbol_table[identifier_to_change], str):
                                stripped = symbol_table[identifier_to_change].strip('"')
                            symbol_table[identifier_to_change] = float(stripped)
                        elif new_type == "TROOF":
                            # TODO:
                            pass
                        elif new_type == "YARN":
                            symbol_table[identifier_to_change] = str(symbol_table[identifier_to_change])
                    except:
                        line_valid = False
                        code_syntax_valid = False
                        print_error("TYPECASTING ERROR", line.line_number)
                        break
                    
                    i += 1
                    continue
                else:
                    line_valid = False
                    code_syntax_valid = False
                    print_error("IDENTIFIER IS NOT DECLARED BEFORE RECASTING", line.line_number)
                    break

            # TODO: maek, boolean
            # Check variable assignment (R)
            assignment_return = line.check_variable_assignment(complete_line, symbol_table)
            if (assignment_return):
                line_valid = True

                if (check_code_skip()):
                    i += 1
                    continue

                if (check_case()):
                    i += 1
                    continue

                if (assignment_return == INVALID):
                    line_valid = False
                    code_syntax_valid = False
                    print_error("UNDEFINED IDENTIFIER", line.line_number)
                    break

                if (assignment_return == TYPECAST_ERROR):
                    line_valid = False
                    code_syntax_valid = False
                    print_error("TYPECAST ERROR", line.line_number)
                    break
                
                return_type = assignment_return[0]
                identifier_to_change = assignment_return[1]
                new_value = assignment_return[2]

                # if 2nd argument is a identifier, check if it exists first
                if (return_type == 0):
                    if (new_value in symbol_table.keys()):
                        symbol_table[identifier_to_change] = symbol_table[new_value]
                        i += 1
                        continue
                    else:
                        line_valid = False
                        code_syntax_valid = False
                        print_error("UNDEFINED IDENTIFIER", line.line_number)
                        break
                
                # case when argument is not an identifier
                # change value of identifier if it exists, add to symbol table if it does not exist
                symbol_table[identifier_to_change] = new_value
                i += 1
                continue

            # Check input (GIMMEH)
            input_return = line.check_input(complete_line, symbol_table)
            if (input_return):
                line_valid = True

                if (check_code_skip()):
                    i += 1
                    continue

                if (check_case()):
                    i += 1
                    continue

                if (input_return == INVALID):
                    line_valid = False
                    code_syntax_valid = False
                    print_error("IDENTIFIER SHOULD BE DECLARED FIRST", line.line_number)
                    break
                
                value = simpledialog.askstring("Input", f"Enter value for {input_return}")
                if value == None or value == "":  # user closed the popup
                    value = "NOOB"
                else:
                    value = '"' + value + '"'
                
                symbol_table[input_return] = value

                i += 1
                continue

            # TODO: expressions
            # Check print (VISIBLE)
            print_return, visible_array = line.check_print(complete_line, symbol_table)
            if (print_return):
                line_valid = True

                if visible_array == INVALID:
                    print_error("INVALID IDENTIFIER!")
                elif visible_array == TYPECAST_ERROR:
                    print_error("TYPECAST ERROR!")

                if (check_code_skip()):
                    i += 1
                    continue

                if (check_case()):
                    i += 1
                    continue

                print("***** VISIBLE ARRAY *****", visible_array)
                # SEMANTICS
                # print("visible_array", visible_array)
                for j in range(len(visible_array)):
                    
                    if j == 0:  # skip VISIBLE keyword
                        continue
                    if visible_array[j] == "AN":
                        continue

                    print("************TO_PRINT***********", visible_array[j])
                    # check if it element to print is identifier
                    to_print = visible_array[j]
                    is_identifier = False
                    if to_print != "WIN" and to_print != "FAIL":
                        identifier_regex = fr'(?<![^\s])([a-zA-Z][a-zA-Z0-9_]*)(?![^\s])'
                        is_identifier = re.match(identifier_regex, to_print)
                    
                    
                    # if valid identifier, display its value instead
                    if (is_identifier and to_print in symbol_table.keys()):
                        to_print = symbol_table[complete_line.line_array[j]]
                        if type(to_print) == type(""):
                            to_print = re.sub("\"", "", to_print)
                        console.append_terminal(f"{to_print} ")
                        continue

                    # case where identifier is undefined
                    elif (is_identifier and not to_print in symbol_table.keys()):
                        line_valid = False
                        code_syntax_valid = False
                        print(f"line {line.line_number}: UNDEFINED IDENTIFIER")
                        console.append_terminal(f"line {line.line_number}: UNDEFINED IDENTIFIER\n")
                        break

                    if type(to_print) == type(""):
                        to_print = re.sub("\"", "", to_print)
                    console.append_terminal(f"{to_print} ")
                console.append_terminal("\n")

                i += 1
                continue

            # Check if then start (O RLY?)
            if (line.check_ifthen_start()):

                # case where IT is not defined
                if (IT == "NOOB"):
                    line_valid = False
                    code_syntax_valid = False
                    print_error("CANNOT START O RLY, IT VARIABLE IS NOT DEFINED", line.line_number)
                    break

                # check if previous O RLY? is not closed by OIC
                if (len(conditional_stack) > 0):
                    if (conditional_stack[-1] == "O RLY?"):  # if there is a O RLY? on stack (not closed by OIC)
                        print_error("PREVIOUS O RLY? IS NOT CLOSED BY OIC!", line.line_number)
                        line_valid = False
                        code_syntax_valid = False
                        break
                    elif (conditional_stack[-1] == "WTF?"):  # if there is a WTF? on stack (not closed by OIC)
                        print_error("PREVIOUS WTF? IS NOT CLOSED BY OIC!", line.line_number)
                        line_valid = False
                        code_syntax_valid = False
                        break

                conditional_stack.insert(0, "O RLY?")  # insert on top of stack array [TOP, MIDDLE, BOTTOM]
                line_valid = True

                there_is_conditional = True
                if (IT):
                    do_not_run_nowai = True
                    do_not_run_yarly = False
                else:
                    do_not_run_yarly = True
                    do_not_run_nowai = False

                
                i += 1
                continue

            # Check if (YA RLY)
            if (line.check_if()):
                if (len(conditional_stack) > 0):
                    # check if there is O RLY? on stack
                    if (conditional_stack[-1] == "O RLY?"):  # if there is O RLY? on bottom of stack
                        if (not conditional_stack[0] == "YA RLY"):  # if top of stack is NOT YA RLY (2 YA RLY = ERROR)
                            conditional_stack.insert(0, "YA RLY")
                            line_valid = True
                            i += 1
                            continue
                        else:
                            line_valid = False
                            code_syntax_valid = False
                            print_error("INVALID YA RLY! MULTIPLE YA RLY FOUND!", line.line_number)
                            break
                    else:
                        line_valid = False
                        code_syntax_valid = False
                        print_error("INVALID YA RLY! NO O RLY FOUND!", line.line_number)
                        break
                else:
                    line_valid = False
                    code_syntax_valid = False
                    print_error("NO O RLY? FOUND! (EMPTY STACK)", line.line_number)
                    break
                
            # Check else (NO WAI)
            if (line.check_else()):
                if (len(conditional_stack) > 0):
                    # required to have one YA RLY
                    if (conditional_stack[0] == "YA RLY"):  # if there is corresponding IF (YA RLY) on top of stack
                        conditional_stack.insert(0, "NO WAI")
                        line_valid = True
                        i += 1
                        continue
                    else:
                        line_valid = False
                        code_syntax_valid = False
                        print_error("INVALID NO WAI! NO YA RLY FOUND!", line.line_number)
                        break
                else:
                    line_valid = False
                    code_syntax_valid = False
                    print_error("INVALID NO WAI! NO YA RLY FOUND!", line.line_number)
                    break

            # Check conditional end (OIC)
            if (line.check_conditional_end()):
                if (len(conditional_stack) > 0):

                    # ENDING O RLY? (IF THEN STATEMENT)
                    # need YA RLY (IF) and NO WAI (THEN), but YA RLY only (without NO WAI) is allowed
                    if (conditional_stack[-1] == "O RLY?"):  # if there is corresponding O RLY? on bottom of stack
                        if (conditional_stack[0] == "YA RLY" or conditional_stack[0] == "NO WAI"):  # if there is YA RLY (IF), NO WAI (THEN), on top of stack
                            conditional_stack.clear()
                            line_valid = True
                            there_is_conditional = False
                            do_not_run_nowai = False
                            do_not_run_yarly = False
                            i += 1
                            continue
                        else:
                            line_valid = False
                            code_syntax_valid = False
                            print_error("INVALID OIC! NO YA RLY (IF) FOUND!", line.line_number)
                            break
                    
                    # ENDING WTF? (CASE STATEMENT)
                    # need atleast one OMG (CASE)
                    elif (conditional_stack[-1] == "WTF?"):  # if there is corresponding WTF? on bottom of stack
                        if (conditional_stack[0] == "OMG"):  # if there is YA RLY (IF), NO WAI (THEN), on top of stack
                            conditional_stack.clear()
                            line_valid = True
                            there_is_conditional = False
                            do_not_run_nowai = False
                            do_not_run_yarly = False
                            case_activated = False
                            i += 1
                            continue
                        else:
                            line_valid = False
                            code_syntax_valid = False
                            print_error("INVALID OIC! PUT ATLEAST ONE OMG (CASE)!", line.line_number)
                            break
                else:
                    line_valid = False
                    code_syntax_valid = False
                    print_error("INVALID OIC! NO O RLY? OR WTF? FOUND!", line.line_number)
                    break

            # Check the implicit IT variable
            return_it = line.check_implicit_it(complete_line, symbol_table)
            if (return_it):
                line_valid = True

                if (check_code_skip()):
                    i += 1
                    continue

                if (check_case()):
                    i += 1
                    continue
                
                # INVALID means IT identifier is undefined
                if return_it == INVALID:
                    line_valid = False
                    code_syntax_valid = False
                    print_error("IT IDENTIFIER IS UNDEFINED", line.line_number)
                    break

                IT = return_it[0]       # BOOLEAN version of IT (True|False)
                IT_VALUE = return_it[1] # VALUE of IT
                i += 1
                continue
            
            # Check case statement (WTF?)
            if (line.check_case_start()):
                if (IT == "NOOB"):
                    line_valid = False
                    code_syntax_valid = False
                    print_error("IT VARIABLE IS NOT DEFINED", line.line_number)
                    break

                if (len(conditional_stack) > 0):
                    if (conditional_stack[-1] == "O RLY?"):  # if there is a O RLY? on stack (not closed by OIC)
                        print_error("PREVIOUS O RLY? IS NOT CLOSED BY OIC!", line.line_number)
                        line_valid = False
                        code_syntax_valid = False
                        break
                    elif (conditional_stack[-1] == "WTF?"):  # if there is a WTF? on stack (not closed by OIC)
                        print_error("PREVIOUS WTF? IS NOT CLOSED BY OIC!", line.line_number)
                        line_valid = False
                        code_syntax_valid = False
                        break

                conditional_stack.insert(0, "WTF?")
                line_valid = True
                there_is_conditional = True

                i += 1
                continue

            # Check cases (OMG <case>)
            case_return = line.check_cases(complete_line)
            if (case_return):
                line_valid = True
            
                conditional_stack.insert(0, "OMG")

                if case_return == ZERO:  # special case
                    cases_stack.insert(0, 0)
                    cases_stack_copy.insert(0, 0)
                else:
                    cases_stack.insert(0, case_return)
                    cases_stack_copy.insert(0, case_return)


                case_activated = True
                print(cases_stack_copy)
                
                i += 1
                continue
            
            # TODO: check break for LOOP (current break is for case only)
            # Check break (GTFO)
            if (line.check_break()):

                if (check_code_skip()):
                    i += 1
                    continue

                if (check_case()):
                    i += 1
                    continue

                if (len(conditional_stack) > 0):
                    if (conditional_stack[0] == "OMG"):

                        # disable the top of case stack to quit running
                        cases_stack.pop(0)
                        conditional_stack.pop(0)
                        cases_stack.insert(0, None)
                        conditional_stack.insert(0, None)

                        line_valid = True
                        i += 1
                        continue
                    else:
                        print_error("INVALID BREAK! NO CASE TO BREAK", line.line_number)
                        line_valid = False
                        code_syntax_valid = False
                        break
                else:
                    print_error("INVALID BREAK!", line.line_number)
                    line_valid = False
                    code_syntax_valid = False
                    break

            # Check case default (OMGWTF)
            if (line.check_case_default()):
                line_valid = True

                # if (check_case()):
                #     i += 1
                #     continue

                cases_stack.insert(0, "OMGWTF")
                cases_stack_copy.insert(0, "OMGWTF")

                i += 1
                continue

            # Check loop start (IM IN YR <label> <operation> YR <variable> [TIL|WILE <expression>])
            return_loop_start = line.check_loop_start(complete_line, symbol_table)
            if (return_loop_start):
                line_valid = True

                # INVALID means an identifier is undefined
                if return_loop_start == INVALID:
                    line_valid = False
                    code_syntax_valid = False
                    print_error("IDENTIFIER IS UNDEFINED", line.line_number)
                    break
                if return_loop_start == TYPECAST_ERROR:
                    line_valid = False
                    code_syntax_valid = False
                    print_error("TYPECAST_ERROR", line.line_number)
                    break
                
                # check if bottom of stack contains another loop (unclosed)
                if (len(loop_stack) > 0):
                    if (loop_stack[-1] == "IM IN YR"):  
                        print_error("PREVIOUS IM IN YR (LOOP) IS NOT CLOSED!", line.line_number)
                        line_valid = False
                        code_syntax_valid = False
                        break

                # this part of code is if VALID
                loop_stack.insert(0, "IM IN YR")

                # set up loop
                CONTINUE_LOOP = return_loop_start[0]
                LOOP_OPERATION = return_loop_start[1]
                LOOP_VARIABLE = return_loop_start[2]

                if (starting_loop_index == None):
                    starting_loop_index = i
                    print(f"SET LOOP {i}")

                i += 1
                continue

            # Check loop end (IM OUTTA YR <label>)
            if (line.check_loop_end()):
                if (len(loop_stack) > 0):
                    if (loop_stack[0] == "IM IN YR"):  # check if top of stack contains a loop starter
                        loop_stack.clear()
                        line_valid = True

                        if (CONTINUE_LOOP):
                            LOOPED += 1

                            
                            i = starting_loop_index
                            print(f"GO BACK TO LOOP {i}")

                            if (LOOP_OPERATION == "UPPIN"):
                                symbol_table[LOOP_VARIABLE] = symbol_table[LOOP_VARIABLE] + 1
                            elif (LOOP_OPERATION == "NERFIN"):
                                symbol_table[LOOP_VARIABLE] = symbol_table[LOOP_VARIABLE] - 1
                            continue

                        # reset loop elements
                        starting_loop_index = None
                        LOOP_VARIABLE = None
                        LOOP_OPERATION = None
                        CONTINUE_LOOP = None

                        i += 1
                        continue
                    else:
                        line_valid = False
                        code_syntax_valid = False
                        print_error("INVALID IM OUTTA YR! NO IM IN YR FOUND!", line.line_number)
                        break
                else:
                    line_valid = False
                    code_syntax_valid = False
                    print_error("INVALID IM OUTTA YR! NO IM IN YR FOUND!", line.line_number)
                    break


            # Check if line is valid/defined
            if (not line_valid):
                code_syntax_valid = False  # If one line is invalid, whole code syntax is invalid
                print(f"SYNTAX ERROR/UNDEFINED: {complete_line.line_number} {complete_line.line_array}")
                print(f"SYNTAX ERROR/UNDEFINED: {line.line_number} {line.line_array}")
                console.append_terminal(f"line {complete_line.line_number}: SYNTAX UNDEFINED/ERROR {complete_line.line_array}\n")
                break


        #   ______           _ 
        #  |  ____|         | |
        #  | |__   _ __   __| |
        #  |  __| | '_ \ / _` |
        #  | |____| | | | (_| |
        #  |______|_| |_|\__,_|
                     
            

        # Check conditional stack, if there is an entry, there is an error in an IF ELSE/CASE statement
        if (len(conditional_stack) > 0):
            code_syntax_valid = False
            print(f"FAULTY O RLY?/WTF? STRUCTURE FOUND! {conditional_stack}")

        # Check loop stack, if there is an entry, there is an error in a LOOP statement
        if (len(loop_stack) > 0):
            code_syntax_valid = False
            print(f"FAULTY LOOP STRUCTURE FOUND! {loop_stack}")

        print(symbol_table)

        # insert symbol table to ui
        insert_symbol_table_to_ui(symbol_table, code_syntax_valid, IT, IT_VALUE)
        print("\nSYNTAX ANALYSIS DONE! ", end="")
        if(code_syntax_valid):
            print("(NO ERRORS FOUND)")
            console.append_terminal("PROGRAM ENDED WITH NO ERRORS")
        else:
            print("(THERE IS AN ERROR)")
            console.append_terminal("PROGRAM TERMINATED BECAUSE OF AN ERROR")


        


"""
   _____ _    _ _____ 
  / ____| |  | |_   _|
 | |  __| |  | | | |  
 | | |_ | |  | | | |  
 | |__| | |__| |_| |_ 
  \_____|\____/|_____|
                                    
"""

# Console class
class LOLConsole(Text):
    # Inherit from Tkinter Textbox
    def __init__(self, root, height, font):
        super().__init__()
        self.root = root
        self.height = height
        self.font = font

    def clear_terminal(self):
        self.delete(1.0, END)

    def append_terminal(self, text):
        self.insert(END, text)

# create a lexeme table
def create_lexeme_table():
    # create a tree view (Lexemes)
    words_tree = ttk.Treeview(root, height=15)

    # set column and format columns (Lexemes)
    words_tree['columns'] = ('Lexeme', 'Type', 'Description')
    words_tree.column("#0", width=0, stretch=NO)
    words_tree.column("Lexeme", anchor=W, width=100)
    words_tree.column("Type", anchor=W, width=100)
    words_tree.column("Description", anchor=W, width=150)

    # set column headings
    words_tree.heading("#0", text="", anchor=W)
    words_tree.heading("Lexeme", text="Lexeme", anchor=W)
    words_tree.heading("Type", text="Type", anchor=W)
    words_tree.heading("Description", text="Description", anchor=W)

    return words_tree

# create the symbol table
def create_symbol_table():
    # create a tree view (Lexemes)
    words_tree = ttk.Treeview(root, height=15)

    # set column and format columns (Lexemes)
    words_tree['columns'] = ('Identifier', 'Value', 'Type')
    words_tree.column("#0", width=0, stretch=NO)
    words_tree.column("Identifier", anchor=W, width=100)
    words_tree.column("Value", anchor=W, width=100)
    words_tree.column("Type", anchor=W, width=100)

    # set column headings
    words_tree.heading("#0", text="", anchor=W)
    words_tree.heading("Identifier", text="Identifier", anchor=W)
    words_tree.heading("Value", text="Value", anchor=W)
    words_tree.heading("Type", text="Type", anchor=W)

    return words_tree

# insert lexeme table to ui
def insert_lexeme_table_to_ui(lexeme_dictionary):
    # clear all data in symbol_table_ui widget (if existing)
    for data in lexemes_table.get_children():
        lexemes_table.delete(data)

    # insert data to table widget
    unique_id = 0
    for key in lexeme_dictionary.keys():
        for value in lexeme_dictionary[f"{key}"]:
            desc = ""
            if value in keyword_description.keys():
                desc += keyword_description.get(value)
            else:
                match key:
                    case "yarns":
                        desc += yarn_description
                    case "numbrs":
                        desc += numbr_description
                    case "numbars":
                        desc += numbar_description
                    case "troofs":
                        desc += troof_description
                    case "type_literals":
                        desc += type_description
                    case "identifiers":
                        desc += identifier_description
                    case _:
                        desc += ""
            lexemes_table.insert(parent='', index='end', iid=unique_id, text="", values=(key, value, desc))
            unique_id += 1

# insert symbol table to ui
def insert_symbol_table_to_ui(symbol_table, code_syntax_valid, IT, IT_VALUE):

    # function to get the description of identifiers in symbol table
    def get_symbol_table_desc(to_classify):
        yarn_regex = fr'(?<![^\s])"[^"]*"(?![^\s])'
        numbr_regex = fr'(?<!\w|\.)-?[0-9]+(?!\w|\.)'
        numbar_regex = fr'(?<!\w|\.)(-?\d*\.\d+)(?!\w|\.)'
        troof_regex = fr'(?<![^\s])(WIN|FAIL)(?![^\s])'

        if (re.search(yarn_regex, to_classify)):
            return "YARN"
        elif (re.search(numbr_regex, to_classify)):
            return "NUMBR"
        elif (re.search(numbar_regex, to_classify)):
            return "NUMBAR"
        elif (re.search(troof_regex, to_classify)):
            return "TROOF"
        else:
            return "NOOB"

    # clear all data in symbol_table_ui widget (if existing)
    for data in symbol_table_ui.get_children():
        symbol_table_ui.delete(data)

    # if there are no errors in the code syntax
    if (code_syntax_valid):
        # insert data to table widget
        unique_id = 0

        # insert IT (VALUE and BOOLEAN type of value)
        desc = get_symbol_table_desc(str(IT_VALUE))
        symbol_table_ui.insert(parent='', index='end', iid=unique_id, text="", values=("IT", IT_VALUE, desc))
        unique_id += 1
        symbol_table_ui.insert(parent='', index='end', iid=unique_id, text="", values=("IT (TROOF)", IT, "TROOF"))
        unique_id += 1

        # insert items from the SYMBOL TABLE
        for identifier, value in symbol_table.items():
            identifier_type = get_symbol_table_desc(str(value))
            symbol_table_ui.insert(parent='', index='end', iid=unique_id, text="", values=(identifier, value, identifier_type))
            unique_id += 1


# configure window (root)
root = Tk()
root.title("LOLCODE INTERPRETER")

# configure choose file button
choose_file_button = Button(root, text="Choose Input", command=open_lol_file)
choose_file_button.grid(row=0, column=0, padx=10, pady=15, sticky=N+S+E+W)

#Labels
lexeme_label = Label(root, text = "LEXEME TABLE")
lexeme_label.grid(row=0, column=1, padx=10, pady=10)

symbol_label = Label(root, text = "SYMBOL TABLE")
symbol_label.grid(row=0, column=2, padx=10, pady=10)

# configure text box
code_text_box = Text(root, width=60, height=18, font=("Consolas", 12))
code_text_box.grid(row=1, column=0, padx=20, pady=20)

# create the lexeme table
lexemes_table = create_lexeme_table()
lexemes_table.grid(row=1, column=1, padx=20, pady=20)

# create the symbol table
symbol_table_ui = create_symbol_table()
symbol_table_ui.grid(row=1, column=2, padx=20, pady=20)

# configure execute file button
execute_button = Button(root, text="Execute", command=execute_code)
execute_button.grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky=N+S+E+W)

# configure console
console = LOLConsole(root, height=7, font=("Consolas", 12))
console.grid(row=5, column=0, columnspan=3, padx=20, pady=20, sticky=N+S+E+W)

# configure clear console output button
clear_button = Button(root, text="Clear Output", command=console.clear_terminal)
clear_button.grid(row=4, column=0, columnspan=3, padx=5, pady=5, sticky=N+S+E+W)

# main root
root.mainloop()