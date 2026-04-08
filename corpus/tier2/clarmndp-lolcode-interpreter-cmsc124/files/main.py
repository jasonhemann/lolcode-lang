"""
# LOLCODE Interpreter written in Python
    
    Authors:
        Diño, John Matthew D.
        Mandap, Clarence P.
        Pore, Richmond Michael B.

    Components/ modules:
        lexer.py - Handles tokenization and lexical analysis
        main.py - Ties all components together and handles program execution
"""

import sys
from lexer import Lexer
import parser
import re

lexeme_table=[]


def interpreter(filename):
    # We first check if the file extension is .lol
    if not filename.endswith('.lol'):
        print("Error: File must have '.lol' extension")
        exit()
        
    try:
        with open(filename, 'r') as file:
            # Read the first line and check for HAI
            starting = file.readline().strip()
            
            if starting != "HAI":
                print ("Error: Invalid Starting Keyword")
                exit()

            # Proceed to the rest of the LOLCODE file
            
            for line in file:
                

                line = line.strip() # Removes the white spaces around the line
                if line:  # Skip empty lines
                    line=line.strip() # Rmoves the white spaces around the line
                    tokenize= Lexer.definer(line)
                    lexeme_table.append(tokenize)
            for index in range(len(lexeme_table)):
                print(index)
                print(lexeme_table[index])
                parse= parser.Parser(lexeme_table[index],lexeme_table,index)
                parse_tree = parse.parse()
               
                    
                print(f"SYMBOL TABLE {parser.symbol_table}")
    except FileNotFoundError:
        print(f"Error: Could not find file '{filename}'")

def main():
    if len(sys.argv) != 2:
        print("Error: Must be of format > python main.py <filename.lol>")
        exit()
    
    program_file = sys.argv[1]
    interpreter(program_file)

if __name__ == "__main__":
    main()
# print(arithmetic_operation("SUM OF SUM OF 3 AN 5 AN 5"))