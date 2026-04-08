HAI 1.4
    CAN HAS STRING?
    CAN HAS STDIO?

    BTW Constants
    I HAS A MEMORY_CELLS ITZ 3000
    I HAS A DEPTH ITZ 10

    HOW IZ I initArray YR size
        I HAS A indexInit ITZ 0
        I HAS A tempArr ITZ A BUKKIT

        IM IN YR initLoop UPPIN YR indexInit WILE DIFFRINT indexInit AN BIGGR OF indexInit AN size
            tempArr HAS A SRS indexInit ITZ 0
        IM OUTTA YR initLoop

        FOUND YR tempArr
    IF U SAY SO

    BTW global brainfuck elements
    I HAS A memory ITZ I IZ initArray YR MEMORY_CELLS MKAY
    I HAS A pointer ITZ 0

    BTW global index to allow loops to work
    I HAS A index ITZ 0
    I HAS A loopStartsIndex ITZ 0
    I HAS A loopStarts ITZ I IZ initArray YR DEPTH MKAY

    HOW IZ I getSourceCode 
        VISIBLE "Filename: "
        I HAS A filename ITZ A YARN
        GIMMEH filename

        I HAS A openFile ITZ I IZ STDIO'Z OPEN YR filename AN YR "r" MKAY
        I IZ STDIO'Z DIAF YR openFile MKAY
        O RLY?
            YA RLY
                VISIBLE "Could not open file"
                FOUND YR ""
        OIC

        VISIBLE "Length (chars): "
        I HAS A fileLength ITZ A NUMBR
        GIMMEH fileLength
        fileLength R PRODUKT OF fileLength AN 4

        I HAS A source ITZ I IZ STDIO'Z LUK YR openFile AN YR fileLength MKAY
        VISIBLE SMOOSH "Read source: " source MKAY

        I IZ STDIO'Z CLOSE YR openFile MKAY
        FOUND YR source
    IF U SAY SO

    O HAI IM BF_Operators
        HOW IZ I increment
            BOTH SAEM memory'Z SRS pointer AN 127, O RLY?
                YA RLY, memory'Z SRS pointer R -128
                NO WAI, memory'Z SRS pointer R SUM OF memory'Z SRS pointer AN 1
            OIC
        IF U SAY SO

        HOW IZ I decrement
            BOTH SAEM memory'Z SRS pointer AN -128, O RLY?
                YA RLY, memory'Z SRS pointer R 127
                NO WAI, memory'Z SRS pointer R DIFF OF memory'Z SRS pointer AN 1
            OIC
        IF U SAY SO

        HOW IZ I ptrIncrement
            pointer R SUM OF pointer AN 1
        IF U SAY SO

        HOW IZ I ptrDecrement
            pointer R DIFF OF pointer AN 1
        IF U SAY SO

        HOW IZ I print
            I HAS A val ITZ memory'Z SRS pointer
            VISIBLE SMOOSH val " " MKAY !
        IF U SAY SO

        HOW IZ I read
            I HAS A newVal ITZ A NUMBR
            GIMMEH newVal
            
            memory'Z SRS pointer R newVal
        IF U SAY SO

        HOW IZ I loopStart
            loopStartsIndex R SUM OF loopStartsIndex AN 1
            loopStarts'Z SRS loopStartsIndex R index
        IF U SAY SO

        HOW IZ I loopEnd
            BOTH SAEM memory'Z SRS pointer AN 0, O RLY?
                YA RLY
                    loopStartsIndex R DIFF OF loopStartsIndex AN 1
                NO WAI, index R loopStarts'Z SRS loopStartsIndex
            OIC
        IF U SAY SO
    KTHX

    HOW IZ I executeSource YR source
        I HAS A length
        length R I IZ STRING'Z LEN YR source MKAY

        IM IN YR mainLoop UPPIN YR index WILE DIFFRINT index AN BIGGR OF index AN length
            I IZ STRING'Z AT YR source AN YR index MKAY, WTF?
                OMG "+"
                    I IZ BF_Operators'Z increment MKAY
                    GTFO
                OMG "-"
                    I IZ BF_Operators'Z decrement MKAY
                    GTFO
                OMG ">"
                    I IZ BF_Operators'Z ptrIncrement MKAY
                    GTFO
                OMG "<"
                    I IZ BF_Operators'Z ptrDecrement MKAY
                    GTFO
                OMG "."
                    I IZ BF_Operators'Z print MKAY
                    GTFO
                OMG ","
                    I IZ BF_Operators'Z read MKAY
                    GTFO
                OMG "["
                    I IZ BF_Operators'Z loopStart MKAY
                    GTFO
                OMG "]"
                    I IZ BF_Operators'Z loopEnd MKAY
                    GTFO
                OMGWTF
                    BTW Any other chars
            OIC    
        IM OUTTA YR mainLoop
    IF U SAY SO

    BTW get and execute code
    I HAS A source ITZ I IZ getSourceCode MKAY
    VISIBLE "Brainfuck output: "
    I IZ executeSource YR source MKAY
KTHXBYE
