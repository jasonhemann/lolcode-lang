BTW --- Bullet object ---
O HAI IM Bullet
    I HAS A texture ITZ FAIL
    I HAS A position ITZ FAIL
    I HAS A originRect ITZ A BUKKIT
    I HAS A timer ITZ A NUMBAR
    I HAS A timerLower ITZ A NUMBAR
    I HAS A timerUpper ITZ A NUMBAR
    I HAS A origin ITZ A BUKKIT
    I HAS A speed ITZ A NUMBAR
    I HAS A alive ITZ A TROOF

    OBTW Do not fall in the trap of doing this:
            ME'Z texture R I IZ RAYLIB ...
            ME'Z alive R FAIL
        if I'm not mistaken, in this way I'm setting the variables on the
        **parent class** and not the **child class**, which means if the
        parent class inherits more than once, the second object will overwrite
        the first one, which obviously is not want we intend.
        With "HAS A" we are creating a new variable within the child class.
    TLDR
    HOW IZ I initBullet YR texturePath AN YR originRect AN YR origin AN YR timer AN YR lower AN YR upper
        BOTH SAEM ME'Z texture AN FAIL
        O RLY?, YA RLY
            ME HAS A texture ITZ I IZ RAYLIB'Z LOADTEXTURE YR texturePath MKAY
        OIC
        ME HAS A position ITZ I IZ vector2 YR 0.0 AN YR 0.0 MKAY
        ME HAS A speed ITZ 0.0
        ME HAS A alive ITZ FAIL
        ME HAS A originRect ITZ originRect
        ME HAS A origin ITZ origin
        ME HAS A timer ITZ timer
        ME HAS A timerLower ITZ lower
        ME HAS A timerUpper ITZ upper
    IF U SAY SO

    HOW IZ I setBullet YR pos AN YR speed
        ME'Z position'Z x R pos'Z x
        ME'Z position'Z y R pos'Z y
        ME'Z speed R speed
        ME'Z alive R WIN
    IF U SAY SO

    HOW IZ I updateBullet
        ME'Z position'Z y R ...
            SUM OF ME'Z position'Z y AN ...
            PRODUKT OF ME'Z speed AN I IZ RAYLIB'Z GETFRAMETIME ...
        MKAY
        EITHER OF ...
        DIFFRINT ME'Z position'Z y AN BIGGR OF ME'Z position'Z y AN -30 AN ...
        BOTH SAEM ME'Z position'Z y AN BIGGR OF ME'Z position'Z y AN 800.0
        O RLY?, YA RLY
            ME'Z alive R FAIL
            DIFFRINT ME'Z timerLower AN 0
            O RLY?, YA RLY
                ME'Z timer R I IZ random YR ME'Z timerLower AN YR ME'Z timerUpper MKAY
            OIC
        OIC
    IF U SAY SO

    HOW IZ I updateTimer YR starList
        BTW IM IN YR enemyShoot UPPIN YR n WILE DIFFRINT n AN 3
        BTW I HAS A currentBullet ITZ bulletList'Z SRS n
        ME'Z timer R DIFF OF ME'Z timer AN I IZ RAYLIB'Z GETFRAMETIME MKAY
        BOTH SAEM ME'Z timer AN SMALLR OF ME'Z timer AN 0
        O RLY?, YA RLY
            I HAS A randStar ITZ 0
            I HAS A selectedStar ITZ A BUKKIT
            IM IN YR getRandomStar
                randStar R I IZ random YR 0 AN YR 50 MKAY
                selectedStar R starList'Z SRS randStar
                selectedStar'Z alive, O RLY?, YA RLY, GTFO, OIC
            IM OUTTA YR getRandomStar
            I IZ ME'Z setBullet YR selectedStar'Z pos AN YR 185.0 MKAY
        OIC
        BTW IM OUTTA YR enemyShoot
    IF U SAY SO

    HOW IZ I drawBullet YR destSize AN YR angle
        I HAS A destRect ITZ I IZ rectangle YR ...
            ME'Z position'Z x AN YR ME'Z position'Z y AN YR ...
            destSize'Z x AN YR destSize'Z y ...
        MKAY
        I IZ drawTexturePro ...
            YR ME'Z texture AN YR ME'Z originRect AN YR destRect ...
            AN YR ME'Z origin AN YR angle AN YR white ...
        MKAY
    IF U SAY SO

    HOW IZ I getRekt YR destSize
        I HAS A rect ITZ I IZ rectangle YR ...
            ME'Z position'Z x AN YR ME'Z position'Z y AN YR ...
            destSize'Z x AN YR destSize'Z y ...
        MKAY
        FOUND YR rect
    IF U SAY SO
KTHX

BTW --- End of Bullet object ---