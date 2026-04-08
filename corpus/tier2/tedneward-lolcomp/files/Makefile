all: antlr test #kotlin csharp java fsharp python ruby cpp

# ======== ANTLR grammar-based source generation
#
antlr: antlrbuild antlrtest jarbuild clrbuild #cppbuild

antlrbuild:
	echo ========== Building ANTLR 
	cd antlr; ./build.sh; cd ..

antlrtest: antlrbuild
	echo ========== Testing ANTLR
	cd antlr; ./test.sh; cd ..

jarbuild:
	echo ========== Building ANTLR JAR
	cd antlr/jar; gradle build; cd ../..
	cp antlr/jar/build/libs/lolcodeparser.jar kotlin/engine/lib
	cp antlr/jar/build/libs/lolcodeparser.jar java/engine/lib

clrbuild:
	echo ========== Building ANTLR CLR
	cd antlr/clr; dotnet build; cd ../..
	cp antlr/clr/bin/Debug/net6.0/LOLCODEParser.dll csharp/lib
	cp antlr/clr/bin/Debug/net6.0/LOLCODEParser.dll fsharp/lib

cppbuild:
	echo ========== Building ANTLR Native/C/C++
	cd antlr/cpp; make; cd ../..
#	cp ...?

# ========== Test everything
#
test: kotlintest csharptest javatest

# ========== Clean everything
#
clean:
	cd antlr; ./clean.sh; cd ..
	rm kotlin/engine/lib/lolcodeparser.jar
	cd kotlin; gradle clean; cd ..
	rm csharp/lib/LOLCODEParser.dll
	cd csharp; dotnet clean; cd ..
	rm java/engine/lib/lolcodeparser.jar
	cd java; gradle clean; cd ..
	rm fsharp/lib/LOLCODEParser.dll
	cd fsharp; dotnet clean; cd ..
	cd python; clean.sh; cd ..
	

# ========== Kotlin Interpreter
#
kotlin: kotlinbuild kotlintest

kotlinbuild: jarbuild
	echo ========== Building Kotlin Engine....
	cd kotlin; gradle build; cd ..

kotlintest: kotlinbuild
	echo ========== Testing Kotlin Engine....
	cd kotlin; gradle test; cd ..

# ========== C# Interpreter
#
csharp: csharpbuild csharptest

csharpbuild: clrbuild
	echo ========== Building CSharp Engine....
	cd csharp; dotnet build; cd ..

csharptest: csharpbuild
	echo ========== Testing CSharp Engine....
	cd csharp; dotnet test; cd ..

# ========== Java Interpreter
#
java: javabuild javatest

javabuild: jarbuild
	cd java; gradle build; cd ..

javatest: javabuild
	cd java; gradle test; cd ..

# ========== F# Interpreter
#
fsharp: fsharpbuild fsharptest

fsharpbuild: clrbuild
	echo ========== Building FSharp Engine....
	cd fsharp; dotnet build; cd ..

fsharptest: fsharpbuild
	echo ========== Testing FSharp Engine....
	cd fsharp; dotnet test; cd ..

# ========== C++ Interpreter
#

# ========== Python (Interpreter, Transpiler, ASTCompiler)
# 
python:
	echo ========== Building Python....
	cd python; build.sh; cd ..

