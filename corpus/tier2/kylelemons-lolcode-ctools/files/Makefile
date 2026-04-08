CC=gcc
CPP=g++

CFLAGS=-Wall -Werror -fPIC -ggdb
CPPFLAGS=${CFLAGS}

CCOMPILE=${CC} ${CFLAGS} -c
CPPCOMPILE=${CPP} ${CPPFLAGS} -c
CASSEMBLE=${CC} ${CFLAGS} -m32 -c
CGENAS=${CC} ${CFLAGS} -m32 -S

LINK=${CPP} ${LFLAGS} -o
LEX=flex
BISON=bison -v -d -k

LEX_PREFIX=lex.yy
BIS_PREFIX=grammar.tab

LEX_SOURCE_OUT=${LEX_PREFIX}.c
LEX_SOURCE_OBJ=${LEX_PREFIX}.o
BIS_SOURCE_OUT=${BIS_PREFIX}.c
BIS_HEADER_OUT=${BIS_PREFIX}.h
BIS_SOURCE_OBJ=${BIS_PREFIX}.o

MY_OBJ=ast.o lcc.o lolcode.o

all : asmutil.s lcc

lcc : ${LEX_SOURCE_OBJ} ${BIS_SOURCE_OBJ} ${MY_OBJ}
	${LINK} $@ ${LEX_SOURCE_OBJ} ${BIS_SOURCE_OBJ} ${MY_OBJ}

${LEX_SOURCE_OBJ} : ${LEX_SOURCE_OUT}

${LEX_SOURCE_OUT} : lexer.l grammar.y ${BIS_HEADER_OUT}
	${LEX} -o ${LEX_SOURCE_OUT} $<

${BIS_SOURCE_OBJ} : ${BIS_SOURCE_OUT}

${BIS_HEADER_OUT} : ${BIS_SOURCE_OUT}

${BIS_SOURCE_OUT} : grammar.y lexer.l
	${BISON} -o ${BIS_SOURCE_OUT} --defines=${BIS_HEADER_OUT} $<

lcc.o : lcc.cpp lolcode.hpp ast.h

lolcode.o : lolcode.cpp lolcode.hpp ast.h asmutil.h

clean :
	@echo "  CLEAN"
	rm *.o *.s lcc
	rm *.yy.* *.tab.* grammar.output 
	rm -rf help/

doc : doxygen.conf
	doxygen doxygen.conf

%.o : %.s
	@echo "  AS      $@"
	${CASSEMBLE} $<

%.o : %.c %.h
	@echo "  CC [h]  $@"
	${CCOMPILE} $<

%.o : %.c
	@echo "  CC      $@"
	${CCOMPILE} $<

%.o : %.cpp %.hpp
	@echo "  CPP [h] $@"
	${CPPCOMPILE} $<

%.o : %.cpp
	@echo "  CPP     $@"
	${CPPCOMPILE} $<

%.s : %.c
	@echo "  C -> S  $@"
	${CGENAS} $<

% : %.o
	@echo "  LINK    $@"
	${LINK} $@ $^

