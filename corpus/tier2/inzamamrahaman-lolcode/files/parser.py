
import argparse
from arpeggio import *
from arpeggio import RegExMatch as _ 


argument_parser = argparse.ArgumentParser()
argument_parser.add_argument('--input')
argument_parser.add_argument('-debug', action='store_true')


def programme():
    return hai, newlines, code_block, kthnxbye

def hai():
    return _(r'HAI')

def code_block():
    return [ZeroOrMore((statement, newlines)), statement, newlines]

def statement():
    return [comment, declaration, expression]

def expression():
    return [equals, value, not_rule, label]

def equals():
    return "BOTH", "SAEM", expression, "AN", expression

def not_rule():
    return "NOT", expression

def declaration():
    return [(simple_declaration, decl_assignment), simple_declaration]

def simple_declaration():
    return "I", "HAZ", "A", label 

def decl_assignment():
    return "ITZ", value

def comment():
    return [comment1]

def comment1():
    return _(r'BTW'), ZeroOrMore(string_body)


def string_body():
    return _(r'[^\s"]+')

def label():
    return _(r"\w+")



def value():
    return ["WIN", 
    "FAIL", "NOOB", 
    float_literal,
    integer_literal, 
    string_literal]

def atom():
    return value

def integer_literal():
    return _(r'\d+')

def float_literal():
    return _(r'\d*\.\d*')

def string_literal():
    return '"', ZeroOrMore(string_body), '"'

def kthnxbye():
    return _(r'KTHNXBYE')

def nl():
    return _(r'\n')

def newlines():
    return OneOrMore(nl)


def main():
    args = argument_parser.parse_args()
    debug = args.debug
    fp = open(args.input, 'r')
    content = fp.read()
    fp.close()
    #print(content)
    #content = '"pokemon are"'
    if debug:
        parser = ParserPython(programme, ws='\t\r ', autokwd=True)
        parse_tree = parser.parse(content)
        print(parse_tree)
    else:
        try:
            print("YAY!!!!")
        except:
            print(":-(")

    

if __name__ == '__main__':
    main()

