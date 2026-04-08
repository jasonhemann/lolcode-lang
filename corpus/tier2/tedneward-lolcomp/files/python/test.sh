if [ -f "../examples/$1" ]; then
    echo ============== ${1}: Parsing ============
    python3 Parser.py ../examples/${1}
    echo ============== ${1}: Interpreting =======
    python3 Interpreter.py ../examples/${1}
    exit 0
else
    for TEST in ../examples/*.lol
    do
        echo ============== ${TEST}: Parsing ============
        python3 Parser.py ../examples/${TEST}
        echo ============== ${TEST}: Interpreting =======
        python3 Interpreter.py ../examples/${TEST}
    done
fi

