README
________________________________________________________________________________________________________


Introduction -

1. We have created a symbol table in the parser.y file. It checks for symantics helps in giving appropriate errors.
2. Our program successfully generates tokens and stores it in the symantic table aforementioned.
3. It generates parse tree of LOLCODE code provided.


Intructions - 

bison -d parser.y -Wnone
flex ass3.l
gcc parser.tab.c 
 
OR 

you can simply run the script run.sh

./run.sh



BUGS - 

a.out doesn't get generated because there's an error unknown type name 'YYSTYPE', which try as we may, we couldn't remove. It is what resulted in our downfall. Kindly consider the fact that we did all the work ourselves and our code does generate symbol table and TAC supposedly. Our code did run when it was fed simpler statements like declaration, print statement, but when we tried to improve it, we failed miserably.
