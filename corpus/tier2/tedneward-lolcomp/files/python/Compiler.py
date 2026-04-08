import sys
from antlr4 import *
from lolcode.lolcodeLexer import lolcodeLexer
from lolcode.lolcodeParser import lolcodeParser
from lolcode.lolcodeVisitor import lolcodeVisitor

class Compiler():
    pass

def main(argv):
    incoming = FileStream(sys.argv[1])
    lexer = lolcodeLexer(incoming)
    tokens = CommonTokenStream(lexer)
    parser = lolcodeParser(tokens)
    tree = parser.program()
    print(tree.toStringTree(recog=parser))

    ast = ASTParser().parse_file(sys.argv[1])
    print(ast)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Specify an incoming file to transpile!")
        return

    main(sys.argv)
