ANTLR4_RUNTIME_DIR=/opt/homebrew/Cellar/antlr4-cpp-runtime/4.13.1/

all: antlrgen

antlrgen: ../lolcode.g4
	antlr ../lolcode.g4 -Xexact-output-dir -o gen -Dlanguage=Cpp -package LOLCODE -visitor

# Need the ANTLR C++ runtime for this to compile!
# macOS: `brew install antlr4-cpp-runtime`
build: lolcodeLexer.cpp lolcodeParser.cpp lolcodeBaseListener.cpp  lolcodeVisitor.cpp lolcodeBaseVisitor.cpp lolcodeListener.cpp
	g++ *.cpp -I$(ANTLR4_RUNTIME_DIR)/include -L$(ANTLR4_RUNTIME_DIR)/lib

clean:
	rm -r gen
