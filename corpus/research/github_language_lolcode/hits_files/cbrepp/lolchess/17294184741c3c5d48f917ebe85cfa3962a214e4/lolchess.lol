HAI 1.2

OBTW
    Great LOLCODE guide - https://esolangs.org/wiki/LOLCODE
    To run - lci ./lolchess.lol
TLDR

VISIBLE "Welcome to lolchess!"

O HAI IM bored
    I HAS A initflag ITZ 0

	BTW Set a piece on the board
	HOW IZ I settin YR currentsquare AN YR value
        ME'Z initflag, WTF?
            OMG 0
                I HAS A index ITZ SMOOSH "index" AN currentsquare'Z rank AN currentsquare'Z file MKAY
                ME HAS A SRS index ITZ value
                GTFO
            OMG 1
                I HAS A index ITZ SMOOSH "index" AN currentsquare'Z rank AN currentsquare'Z file MKAY
                I HAS A tempval ITZ value
                ME'Z SRS index R tempval
        OIC
	IF U SAY SO

	BTW Get a piece on the board
	HOW IZ I gettin YR currentsquare
        I HAS A index ITZ SMOOSH "index" AN currentsquare'Z rank AN currentsquare'Z file MKAY
        I HAS A tempval ITZ ME'Z SRS index
		FOUND YR tempval
	IF U SAY SO

	BTW Translate piece name to a display value
	HOW IZ I namecallin YR piecename
        I HAS A name ITZ "      "
        piecename, WTF?
            OMG "rook"
                name R "rook  "
                GTFO
            OMG "knight"
                name R "knight"
                GTFO
            OMG "bishop"
                name R "bishop"
                GTFO
            OMG "queen"
                name R "queen "
                GTFO
            OMG "king"
                name R "king  "
                GTFO
            OMG "pawn"
                name R "pawn  "
                GTFO
        OIC
        FOUND YR name
	IF U SAY SO

	BTW Translate piece color to a display value
    HOW IZ I colorcodin YR piececolor
        I HAS A color ITZ "      "
        piececolor, WTF?
            OMG "black"
                color R "black "
                GTFO
            OMG "white"
                color R "white "
                GTFO
        OIC
        FOUND YR color
	IF U SAY SO

	BTW Translate file character to a number
    HOW IZ I filin YR file
        I HAS A filenumber ITZ 0
        file, WTF?
            OMG "a"
                filenumber R "1"
                GTFO
            OMG "b"
                filenumber R "2"
                GTFO
            OMG "c"
                filenumber R "3"
                GTFO
            OMG "d"
                filenumber R "4"
                GTFO
            OMG "e"
                filenumber R "5"
                GTFO
            OMG "f"
                filenumber R "6"
                GTFO
            OMG "g"
                filenumber R "7"
                GTFO
            OMG "h"
                filenumber R "8"
                GTFO
        OIC
        FOUND YR filenumber
	IF U SAY SO

	BTW Show board
	HOW IZ I sigh
        VISIBLE ""
        VISIBLE "  a      b      c      d      e      f      g      h"
        IM IN YR displayranks UPPIN YR i TIL BOTH SAEM i AN 8
            I HAS A currank ITZ DIFF OF 8 AN i
            I HAS A colorline ITZ ""
            I HAS A nameline ITZ ""

            IM IN YR displayfiles UPPIN YR j TIL BOTH SAEM j AN 8
                I HAS A curfile ITZ SUM OF j AN 1
                I HAS A currentdispsquare ITZ A BUKKIT
                currentdispsquare HAS A rank ITZ currank
                currentdispsquare HAS A file ITZ curfile
                I HAS A newpiece ITZ ME IZ gettin YR currentdispsquare MKAY
                I HAS A colorname ITZ ME IZ colorcodin YR newpiece'Z color MKAY
                colorline R SMOOSH colorline AN "|" AN colorname MKAY
                I HAS A piecename ITZ ME IZ namecallin YR newpiece'Z name MKAY
                nameline R SMOOSH nameline AN "|" AN piecename MKAY
            IM OUTTA YR displayfiles

            colorline R SMOOSH currank AN colorline AN "|" AN currank MKAY
            nameline R SMOOSH " " AN nameline AN "|" MKAY
            VISIBLE colorline
            VISIBLE nameline
        IM OUTTA YR displayranks
        VISIBLE "  a      b      c      d      e      f      g      h"
	IF U SAY SO

    BTW Init the game board
    HOW IZ I setbored
        IM IN YR initplaya UPPIN YR i TIL BOTH SAEM i AN 2
            I HAS A currank ITZ 0
            I HAS A curfile ITZ 0
            I HAS A curcolor ITZ ""
            I HAS A curpiece ITZ ""

            i, WTF?
                OMG 0
                    curcolor R "black"
                    currank R 8
                    GTFO
                OMG 1
                    curcolor R "white"
                    currank R 1
                    GTFO
            OIC

            IM IN YR initfirstrank UPPIN YR j TIL BOTH SAEM j AN 8
                curfile R SUM OF j AN 1
                j, WTF?
                    OMG 0
                        curpiece R "rook"
                        GTFO
                    OMG 1
                        curpiece R "knight"
                        GTFO
                    OMG 2
                        curpiece R "bishop"
                        GTFO
                    OMG 3
                        curpiece R "queen"
                        GTFO
                    OMG 4
                        curpiece R "king"
                        GTFO
                    OMG 5
                        curpiece R "bishop"
                        GTFO
                    OMG 6
                        curpiece R "knight"
                        GTFO
                    OMG 7
                        curpiece R "rook"
                        GTFO
                OIC

                I HAS A currentpiece ITZ A BUKKIT
                currentpiece HAS A color ITZ curcolor
                currentpiece HAS A name ITZ curpiece
                BTW VISIBLE SMOOSH "Adding " AN currentpiece'Z color AN " " AN currentpiece'Z name AN " to " AN curfile AN "," AN currank MKAY
                I HAS A currentsquare ITZ A BUKKIT
                currentsquare HAS A rank ITZ currank
                currentsquare HAS A file ITZ curfile
                ME IZ settin YR currentsquare AN YR currentpiece MKAY
            IM OUTTA YR initfirstrank

            i, WTF?
                OMG 0
                    currank R 7
                    GTFO
                OMG 1
                    currank R 2
                    GTFO
            OIC

            IM IN YR initsecondrank UPPIN YR j TIL BOTH SAEM j AN 8
                curfile R SUM OF j AN 1
                curpiece R "pawn"

                I HAS A currentpiece ITZ A BUKKIT
                currentpiece HAS A color ITZ curcolor
                currentpiece HAS A name ITZ curpiece
                BTW VISIBLE SMOOSH "Adding " AN currentpiece'Z color AN " " AN currentpiece'Z name AN " to " AN curfile AN "," AN currank MKAY
                I HAS A currentsquare ITZ A BUKKIT
                currentsquare HAS A rank ITZ currank
                currentsquare HAS A file ITZ curfile
                ME IZ settin YR currentsquare AN YR currentpiece MKAY
            IM OUTTA YR initsecondrank
        IM OUTTA YR initplaya

        IM IN YR initremainingranks UPPIN YR j TIL BOTH SAEM j AN 4
            I HAS A currank ITZ SUM OF j AN 3
            IM IN YR initremainingfiles UPPIN YR k TIL BOTH SAEM k AN 8
                I HAS A curfile ITZ SUM OF k AN 1

                I HAS A currentpiece ITZ A BUKKIT
                currentpiece HAS A color ITZ ""
                currentpiece HAS A name ITZ ""
                I HAS A currentsquare ITZ A BUKKIT
                currentsquare HAS A rank ITZ currank
                currentsquare HAS A file ITZ curfile
                ME IZ settin YR currentsquare AN YR currentpiece MKAY
            IM OUTTA YR initremainingfiles
        IM OUTTA YR initremainingranks

        ME'Z initflag R 1
    IF U SAY SO

    BTW Get a target square from the user
    HOW IZ I getsquare YR description
        I HAS A goawaynow ITZ 0

        BTW Get a valid target file from the user
        I HAS A trashinput ITZ 1
        IM IN YR getvalidinput UPPIN YR x WILE DIFF OF trashinput AN goawaynow
            VISIBLE ""
            VISIBLE SMOOSH "Enter " AN description AN " file (a-h) or 'exit': " MKAY
            GIMMEH targetfile
            trashinput R 0
            targetfile, WTF?
                OMG "exit"
                    trashinput R 1
                    goawaynow R 1
                    GTFO
                OMG "a"
                    GTFO
                OMG "b"
                    GTFO
                OMG "c"
                    GTFO
                OMG "d"
                    GTFO
                OMG "e"
                    GTFO
                OMG "f"
                    GTFO
                OMG "g"
                    GTFO
                OMG "h"
                    GTFO
                OMGWTF
                    trashinput R 1
                    VISIBLE SMOOSH "'" AN targetfile AN "' is not a valid file!  Try again." MKAY
            OIC
        IM OUTTA YR getvalidinput
        targetfile R currentbored IZ filin YR targetfile MKAY

        BTW Get a valid target rank from the user
        trashinput R 1
        IM IN YR getvalidinput UPPIN YR x WILE DIFF OF trashinput AN goawaynow
            VISIBLE ""
            VISIBLE SMOOSH "Enter " AN description AN " rank (1-8) or 'exit': " MKAY
            GIMMEH targetrank
            trashinput R 0
            targetrank, WTF?
                OMG "exit"
                    trashinput R 1
                    goawaynow R 1
                    GTFO
                OMG "1"
                    GTFO
                OMG "2"
                    GTFO
                OMG "3"
                    GTFO
                OMG "4"
                    GTFO
                OMG "5"
                    GTFO
                OMG "6"
                    GTFO
                OMG "7"
                    GTFO
                OMG "8"
                    GTFO
                OMGWTF
                    trashinput R 1
                    VISIBLE SMOOSH "'" AN targetrank AN "' is not a valid rank!  Try again." MKAY
            OIC
        IM OUTTA YR getvalidinput

        goawaynow, O RLY?
            YA RLY
                FOUND YR "goawaynow"
            NO WAI
                I HAS A targetsquare ITZ A BUKKIT
                targetsquare HAS A rank ITZ targetrank
                targetsquare HAS A file ITZ targetfile
                I HAS A targetpiece ITZ currentbored IZ gettin YR targetsquare MKAY
                I HAS A pieceandsquare ITZ A BUKKIT
                pieceandsquare HAS A name ITZ targetpiece'Z name
                pieceandsquare HAS A color ITZ targetpiece'Z color
                pieceandsquare HAS A rank ITZ targetrank
                pieceandsquare HAS A file ITZ targetfile
                FOUND YR pieceandsquare
        OIC
    IF U SAY SO
KTHX

O HAI IM game
    I HAS A gameover ITZ 0
    I HAS A turncount ITZ 0

    BTW Main game loop
    HOW IZ I letsgo YR currentbored
        I HAS A targetfile ITZ ""
        I HAS A targetrank ITZ ""

        IM IN YR gameloop UPPIN YR turncount WILE BOTH SAEM ME'Z gameover AN 0
            IM IN YR playaturn UPPIN YR i TIL BOTH SAEM i AN 2
                I HAS A playacolor ITZ ""

                i, WTF?
                    OMG 0
                        playacolor R "white"
                        GTFO
                    OMG 1
                        playacolor R "black"
                        GTFO
                OIC

                currentbored IZ sigh MKAY
                VISIBLE ""
                VISIBLE SMOOSH "Current turn: " AN playacolor MKAY

                I HAS A targetpiece ITZ A BUKKIT
                I HAS A destsquare ITZ A BUKKIT

                BTW Get the target square for the piece to move
                I HAS A isvalid ITZ 0
                IM IN YR gettargetsquare UPPIN YR x WILE BOTH SAEM isvalid AN 0
                    targetpiece R currentbored IZ getsquare YR "PIECE" MKAY

                    BTW Validate the selected square
                    isvalid R 1
                    targetpiece, WTF?
                        OMG "goawaynow"
                            ME'Z gameover R 1
                            GTFO
                        OMGWTF
                            I HAS A validationmessage ITZ ""
                            BOTH SAEM targetpiece'Z color AN playacolor, O RLY?
                                YA RLY, validationmessage R ""
                                NO WAI, validationmessage R SMOOSH "You need to select a square with a " playacolor " piece!" MKAY
                            OIC
                            BOTH SAEM validationmessage "", O RLY?
                                YA RLY, VISIBLE SMOOSH "You selected " AN targetpiece'Z color AN " " AN targetpiece'Z name MKAY
                                NO WAI, VISIBLE validationmessage
                            OIC
                            BOTH SAEM validationmessage "", O RLY?
                                YA RLY, isvalid R 1
                                NO WAI, isvalid R 0
                            OIC
                    OIC
                IM OUTTA YR gettargetsquare

                BTW Get the destination square for the target piece
                isvalid R ME'Z gameover
                IM IN YR getdestsquare UPPIN YR x WILE BOTH SAEM isvalid AN 0
                    destsquare R currentbored IZ getsquare YR "DESTINATION" MKAY

                    BTW Validate the selected square
                    isvalid R 1
                    destsquare, WTF?
                        OMG "goawaynow"
                            ME'Z gameover R 1
                            GTFO
                        OMGWTF
                            I HAS A validationmessage ITZ ""
                            BOTH SAEM destsquare'Z color AN playacolor, O RLY?
                                YA RLY, validationmessage R SMOOSH "You can NOT select a square with a " playacolor " piece!" MKAY
                                NO WAI, validationmessage R ""
                            OIC
                            BOTH SAEM validationmessage "", O RLY?
                                YA RLY, VISIBLE SMOOSH "You selected square " AN destsquare'Z color AN " " AN destsquare'Z name MKAY
                                NO WAI, VISIBLE validationmessage
                            OIC
                            BOTH SAEM validationmessage "", O RLY?
                                YA RLY, isvalid R 1
                                NO WAI, isvalid R 0
                            OIC
                    OIC

                    BTW TODO - Actually validate the move
                IM OUTTA YR getdestsquare

                ME'Z gameover, WTF?
                    OMG 1
                       isvalid R 0
                       i R 1
                       VISIBLE ""
                       VISIBLE "Game over"
                OIC

                isvalid, WTF?
                    OMG 1
                        BTW Empty the target square
                        I HAS A emptypiece ITZ A BUKKIT
                        emptypiece HAS A color ITZ ""
                        emptypiece HAS A name ITZ ""
                        currentbored IZ settin YR targetpiece AN YR emptypiece MKAY

                        BTW Move the target piece to the destination square
                        currentbored IZ settin YR destsquare AN YR targetpiece MKAY

                        BTW If the other playa's king was removed, game over
                        BOTH SAEM destsquare'Z name AN "king", O RLY?
                            YA RLY, ME'Z gameover R 1
                            NO WAI, ME'Z gameover R 0
                        OIC
                OIC

                SUM OF ME'Z gameover AN isvalid, WTF?
                    OMG 2
                        VISIBLE ""
                        VISIBLE SMOOSH playacolor AN " wins after " AN SUM OF turncount AN 1 AN " turn(s)!!!" MKAY
                        i R 1
                OIC
            IM OUTTA YR playaturn
        IM OUTTA YR gameloop
    IF U SAY SO
KTHX

I HAS A currentbored ITZ LIEK A bored
I HAS A match ITZ LIEK A game
currentbored IZ setbored MKAY
match IZ letsgo YR currentbored MKAY

KTHXBYE
