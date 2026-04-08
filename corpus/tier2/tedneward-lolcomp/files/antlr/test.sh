if [ -f "../examples/$1" ]; then
    echo Testing ${1}
    java -classpath code:antlr-4.13.1-complete.jar org.antlr.v4.gui.TestRig lolcode program -tree -tokens -gui ../examples/${1}
    exit 0
else
    for TEST in ../examples/*.lol
    do
        echo ============== Testing ${TEST} ============
        java -classpath code:antlr-4.13.1-complete.jar org.antlr.v4.gui.TestRig lolcode program -tree -tokens ${TEST}
    done
fi

