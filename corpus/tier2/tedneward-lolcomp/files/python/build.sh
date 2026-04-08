# Build
echo ====== Pip-installing ANTLR4 runtime....
pip install antlr4-python3-runtime

echo ====== Building ANTLR Python code....
mkdir lolcode
java -jar ../antlr/antlr-4.13.1-complete.jar -Dlanguage=Python3 -o lolcode -Xexact-output-dir -visitor ../antlr/lolcode.g4
echo "# This file intentionally left blank" > lolcode/__init__.py
