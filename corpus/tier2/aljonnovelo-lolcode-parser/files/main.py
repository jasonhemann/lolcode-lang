from lolcode_parser import identify_statement
from lolcode_token_identifier import identify_tokens

def read_file(filename):
    try:
        openfile = open(filename)
        lines = openfile.read().split("\n")
        identify_tokens(lines)

        # i = 0
        # while i < len(lines):
        #     line = lines[i].strip()

        #     # skip empty lines
        #     if not line:
        #         i += 1
        #         continue

        #     # identify the statement type
        #     statement_type, i = identify_statement(lines, i)

        #     # print the identified statement type
        #     if statement_type:
        #         print(f"Line {i + 1}: {statement_type}")
        #     else:
        #         print(f"Line {i + 1}: Unrecognized statement")
        # i += 1

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

read_file('sample1.lol')