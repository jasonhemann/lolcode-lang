# Build
echo ====== Building ANTLR code for immediate testing....
java -jar antlr-4.13.1-complete.jar -o code -Xexact-output-dir lolcode.g4

javac -d code -classpath .:antlr-4.13.1-complete.jar code/lolcode*.java
