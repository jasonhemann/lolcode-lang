BTW --- Star object ---
BTW 39 ticks of movement to move down
O HAI IM Star
    I HAS A texture ITZ FAIL

	I HAS A SOURCE ITZ I IZ rectangle YR 0.0 AN YR 0.0 AN YR 39.0 AN YR 37.0 MKAY
	I HAS A ORIGIN ITZ I IZ vector2 YR 19.5 AN YR 18.5 MKAY

    I HAS A BULLETSOURCE ITZ I IZ rectangle YR 0.0 AN YR 0.0 AN YR 30.0 AN YR 80.0 MKAY
    I HAS A BULLETORIGIN ITZ I IZ vector2 YR 15.0 AN YR 40.0 MKAY

    I HAS A MAXTIMER ITZ 0.6
    I HAS A timer ITZ 0.6
    I HAS A leftMost ITZ 0
    I HAS A rightMost ITZ 5
    I HAS A direction ITZ 20.0
    I HAS A aliveCount ITZ 50

    I HAS A pos
    I HAS A alive
    I HAS A angle

    HOW IZ I initStar YR pos
        BOTH SAEM ME'Z texture AN FAIL
        O RLY?, YA RLY
            ME'Z texture R I IZ RAYLIB'Z LOADTEXTURE YR "assets/graphics/star.png" MKAY
        OIC
        ME HAS A pos ITZ pos
        ME HAS A alive ITZ WIN
        ME HAS A angle ITZ 0.0
    IF U SAY SO

    HOW IZ I reset YR pos
        ME'Z pos R pos
        ME'Z alive R WIN
        ME'Z angle R 0.0
    IF U SAY SO

    HOW IZ I collision YR starList AN YR bulletRect
        IM IN YR checkStars UPPIN YR n WILE DIFFRINT n AN 50
            I HAS A currentStar ITZ starList'Z SRS n
            I HAS A pos ITZ currentStar'Z pos
            I HAS A coll ITZ I IZ checkCollisionRecs YR pos AN YR bulletRect MKAY
            BOTH OF coll AN currentStar'Z alive
            O RLY?, YA RLY
                currentStar'Z alive R FAIL
                BOTH SAEM n AN ME'Z leftMost
                O RLY?, YA RLY
                    IM IN YR getNewLeft UPPIN YR i WILE DIFFRINT i AN 50
                        I HAS A currentIndex ITZ SUM OF i AN n
                        BOTH SAEM currentIndex AN 50
                        O RLY?, YA RLY, ME'Z leftMost R 0, GTFO, OIC
                        I HAS A thisStar ITZ starList'Z SRS currentIndex
                        thisStar'Z alive, O RLY?, YA RLY
                            ME'Z leftMost R MOD OF currentIndex AN 5
                            FOUND YR WIN
                        OIC
                    IM OUTTA YR getNewLeft
                    BTW No new leftMost star found...
                MEBBE BOTH SAEM n AN ME'Z rightMost
                    IM IN YR getNewRight NERFIN YR i WILE DIFFRINT i AN -50
                        I HAS A currentIndex ITZ SUM OF i AN n
                        BOTH SAEM currentIndex AN -1
                        O RLY?, YA RLY, ME'Z rightMost R 5, GTFO, OIC
                        I HAS A thisStar ITZ starList'Z SRS currentIndex
                        thisStar'Z alive, O RLY?, YA RLY
                            ME'Z rightMost R MOD OF currentIndex AN 5
                            FOUND YR WIN
                        OIC
                    IM OUTTA YR getNewRight
                    BTW No new rightMost star found...
                OIC
                FOUND YR WIN
            OIC
        IM OUTTA YR checkStars
        FOUND YR FAIL
    IF U SAY SO

    HOW IZ I starReachedBottom YR starList
        IM IN YR checkBottom NERFIN YR i WILE DIFFRINT i AN -50
            I HAS A index ITZ SUM OF 49 AN i
            I HAS A thisStar ITZ starList'Z SRS index
            thisStar'Z alive, O RLY?, YA RLY
                I HAS A pos ITZ thisStar'Z pos
                FOUND YR BOTH SAEM pos'Z y AN BIGGR OF pos'Z y AN 590
            OIC
        IM OUTTA YR checkBottom
        BTW No stars alive
        FOUND YR FAIL
    IF U SAY SO

    HOW IZ I update YR starList
        I HAS A moveDown ITZ FAIL
        ME'Z timer R DIFF OF ME'Z timer AN I IZ RAYLIB'Z GETFRAMETIME MKAY
        BOTH SAEM ME'Z timer AN SMALLR OF ME'Z timer AN 0
        O RLY?, YA RLY
            ME'Z timer R ME'Z MAXTIMER
            I HAS A posToCheck ITZ A BUKKIT
            DIFFRINT ME'Z direction AN SMALLR OF ME'Z direction AN 0
            O RLY?, YA RLY
                posToCheck R starList'Z SRS ME'Z rightMost  BTW pos'Z SRS ME'Z rightMost
                posToCheck R posToCheck'Z pos
                BTW 1220 - (rightMost-5) * (-20) | rightMost goes from 5 to 0 -> results in 0, 20, 40... 100 -> 1220, 1200...
                I HAS A starLimit ITZ DIFF OF 1220 AN PRODUKT OF DIFF OF ME'Z rightMost AN 5 AN -20
                BOTH SAEM posToCheck'Z x AN BIGGR OF posToCheck'Z x AN starLimit
                O RLY?, YA RLY
                    moveDown R WIN
                    ME'Z direction R PRODUKT OF -1 AN ME'Z direction
                OIC
            NO WAI
                posToCheck R starList'Z SRS ME'Z leftMost BTW pos'Z SRS ME'Z leftMost
                posToCheck R posToCheck'Z pos
                I HAS A starLimit ITZ SUM OF 40 AN PRODUKT OF ME'Z leftMost AN 20
                BOTH SAEM posToCheck'Z x AN SMALLR OF posToCheck'Z x AN starLimit
                O RLY?, YA RLY
                    moveDown R WIN
                    ME'Z direction R PRODUKT OF -1 AN ME'Z direction
                OIC
            OIC
            IM IN YR moveStars UPPIN YR n WILE DIFFRINT n AN 50
                I HAS A currentStar ITZ starList'Z SRS n
                I HAS A pos ITZ currentStar'Z pos
                BTW currentStar'Z alive, O RLY?, YA RLY
                    currentStar'Z angle R SUM OF currentStar'Z angle AN 9.0
                    BOTH SAEM currentStar'Z angle AN BIGGR OF currentStar'Z angle AN 360
                    O RLY?, YA RLY, currentStar'Z angle R 0.0, OIC
                    moveDown, O RLY?, YA RLY
                        pos'Z y R SUM OF pos'Z y AN I IZ MATH'Z ABS YR ME'Z direction MKAY
                    NO WAI
                        pos'Z x R SUM OF pos'Z x AN ME'Z direction
                    OIC
                BTW OIC
            IM OUTTA YR moveStars
        OIC
    IF U SAY SO

    HOW IZ I draw
        ME'Z alive, O RLY?, YA RLY
            BTW ME'Z angle R SUM OF ME'Z angle AN 0.01
            BTW BOTH SAEM ME'Z angle AN BIGGR OF ME'Z angle AN 360
            BTW O RLY?, YA RLY, ME'Z angle R 0.0, OIC
            I IZ drawTexturePro ...
                YR ME'Z texture AN YR ME'Z SOURCE AN YR ME'Z pos ...
                AN YR ME'Z ORIGIN AN YR ME'Z angle AN YR white ...
            MKAY
        OIC
    IF U SAY SO
KTHX

BTW --- End of Star object ---