
O HAI IM Block
    I HAS A texture ITZ FAIL

    I HAS A source ITZ I IZ rectangle YR 0.0 AN YR 0.0 AN YR 50.0 AN YR 80.0 MKAY
    I HAS A ORIGIN ITZ I IZ vector2 YR 25.0 AN YR 40.0 MKAY

    I HAS A pos
    I HAS A startX
    I HAS A alive

    HOW IZ I initBlock YR pos AN YR startX
        BOTH SAEM ME'Z texture AN FAIL
        O RLY?, YA RLY
            ME HAS A texture ITZ I IZ RAYLIB'Z LOADTEXTURE YR "assets/graphics/syrup.png" MKAY
        OIC
        ME HAS A pos ITZ pos
        ME HAS A startX ITZ startX
        ME HAS A alive ITZ WIN
    IF U SAY SO

    HOW IZ I reset YR pos
        ME'Z pos R pos
        ME'Z startX R 0.0
        ME'Z alive R WIN
    IF U SAY SO

    HOW IZ I checkCollisionBlock YR blockList AN YR bulletRect
        IM IN YR checkBlocks UPPIN YR i WILE DIFFRINT i AN 6
            I HAS A currentBlock ITZ blockList'Z SRS i
            BTW Switch width and height since the block is rotated 90 degrees
            I HAS A hitbox ITZ I IZ rectangle YR ...
                DIFF OF currentBlock'Z pos'Z x AN QUOSHUNT OF currentBlock'Z pos'Z height AN 2 AN YR ...
                DIFF OF currentBlock'Z pos'Z y AN QUOSHUNT OF currentBlock'Z pos'Z width AN 2 AN YR ...
                currentBlock'Z pos'Z height AN YR currentBlock'Z pos'Z width ...
            MKAY
            I HAS A collision ITZ I IZ checkCollisionRecs YR hitbox AN YR bulletRect MKAY
            BOTH OF collision AN currentBlock'Z alive
            O RLY?, YA RLY
                BOTH SAEM currentBlock'Z startX AN 100
                O RLY?, YA RLY
                    currentBlock'Z alive R FAIL
                    FOUND YR 0
                NO WAI
                    currentBlock'Z startX R SUM OF currentBlock'Z startX AN 50.0
                    FOUND YR 1
                OIC
            OIC
        IM OUTTA YR checkBlocks
        FOUND YR -1
    IF U SAY SO

    HOW IZ I drawBlock
        ME'Z alive
        O RLY?, YA RLY
            I HAS A sourceRect ITZ I IZ rectangle YR ME'Z startX AN YR ME'Z source'Z y AN YR ME'Z source'Z width AN YR ME'Z source'Z height MKAY
            BTW I IZ RAYLIB'Z DRAWRECTANGLEREC YR DIFF OF ME'Z pos'Z x AN 40.0 AN YR DIFF OF ME'Z pos'Z y AN 25.0 AN YR ME'Z pos'Z height AN YR ME'Z pos'Z width AN YR white'Z r AN YR white'Z g AN YR white'Z b AN YR white'Z a MKAY
            I IZ drawTexturePro ...
                YR ME'Z texture AN YR sourceRect AN YR ME'Z pos ...
                AN YR ME'Z ORIGIN AN YR -1.570796 AN YR white ...
            MKAY
        OIC
    IF U SAY SO
KTHX