echo ====== Emptying ANTLR-test code
rm -r code

echo ====== Cleaning ANTLR-JAR project
cd jar; gradle clean; cd ..

echo ====== Cleaning ANTLR-CLR project
cd clr; dotnet clean; cd ..
