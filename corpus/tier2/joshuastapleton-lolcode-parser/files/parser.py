
import argparse
from arpeggio import *
from arpeggio import RegExMatch as _ 


argument_parser = argparse.ArgumentParser()
argument_parser.add_argument('--input')
argument_parser.add_argument('--debug', action='store_true')


def programme():
    return hai, newlines, code_block, kthnxbye
def hai():
    return _(r'HAI')
def kthnxbye():
    return _(r'KTHNXBYE')
def code_block():
    return [ZeroOrMore((statement, newlines)), statement, newlines]
def statement():
    return [comment, declaration, expression]
def declaration():
    return [(simple_declaration, decl_assignment), simple_declaration]
def simple_declaration():
    return _(r'I'), _(r'HAZ'),_(r'A'), label
def decl_assignment():
    return _(r'ITZ'), value
def value():
    return [_(r'WIN'), 
    _(r'FAIL'), _(r'NOOB'), 
    float_literal,
    integer_literal, 
    string_literal]
def integer_literal():
    return _(r'\d+')
def float_literal():
    return _(r'\d*\.\d*')
def string_literal():
    return _(r'"'), ZeroOrMore(string_body), _(r'"')
def comment():
    return [comment1]
def comment1():
    return _(r'BTW'), ZeroOrMore(string_body)
def string_body():  
    return _(r'[^\s"]+')        
def print_block():
    return _(r'VISIBLE'), ZeroOrMore(expression), _(r'MKAY?')
def input_block():
    return _(r'GIMMEH'), label
def assignment():
    return label, _(r'R'), expression
def expression():
    return [equals, both, not_equals, greater, less, add, sub, mul, div, mod, either,label, atom]
def equals():
    return _(r'BOTH'), _(r'SAEM'), expression, _(r'AN'), expression
def not_equals():
    return _(r'DIFFRINT'), expression, _(r'AN'), expression
def both():
    return _(r'BOTH'), _(r'OF'), expression, _(r'AN'), expression
def either():
    return _(r'EITHER'), _(r'OF'), expression, _(r'AN'), expression
def greater():
    return _(r'BIGGR'), _(r'OF'), expression,_(r'AN'), expression
def less():
    return _(r'SMALLR'), _(r'OF'), expression,_(r'AN'), expression
def add():
    return _(r'SUM'), _(r'OF'), expression, _(r'AN'), expression
def sub():
    return _(r'DIFF'), _(r'OF'), expression, _(r'AN'), expression
def mul():
    return _(r'PRODUKT'), _(r'OF'), expression, _(r'AN'), expression
def div():
    return _(r'QUOSHUNT'), _(r'OF'), expression, _(r'AN'), expression
def mod():
    return _(r'MOD'), _(r'OF'), expression, _(r'AN'), expression
def not_rule():
    _(r'NOT'),expression
def label():
    return _(r"\w+")
def atom():
    return value
def string():
    return ZeroOrMore(string_body)
def newlines():
    return OneOrMore(nl)
def nl():
    return _(r'\n')


def main():
    args = argument_parser.parse_args()
    debug = args.debug
    fp = open(args.input, 'r')
    content = fp.read()
    fp.close()
    print(content)
    if debug:
        parser = ParserPython(programme, ws='\t\r ', autokwd=True)
        parse_tree = parser.parse(content)
        print(parse_tree)
        print("TRUE")
    else:
        try:
            print("YAY!!!!")
            print("TRUE")
        except:
            print(":-(")
            print("False")

    

if __name__ == '__main__':
    main()


