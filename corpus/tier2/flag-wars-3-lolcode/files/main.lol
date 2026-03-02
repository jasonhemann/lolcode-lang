HAI 1.4
CAN HAS RAYLIB?
CAN HAS MATH?

BTW Utils functions

BTW This random number code was yoink'd from LOLTracer:
BTW https://github.com/LoganKelly/LOLTracer
I HAS A prev ITZ 0
I HAS A RAND_MAX ITZ 104729

BTW 0 to RAND_MAX
HOW IZ I randin
    I HAS A a ITZ 33083
    I HAS A c ITZ 67607
    prev R MOD OF SUM OF PRODUKT OF prev AN a AN c AN RAND_MAX
    FOUND YR prev
IF U SAY SO

BTW a to b, b > a
HOW IZ I random YR a AN YR b
    FOUND YR SUM OF a AN MOD OF I IZ randin MKAY AN DIFF OF b AN a
IF U SAY SO

BTW --- Color creator ---
HOW IZ I color YR red AN YR green AN YR blue AN YR alpha
	I HAS A array ITZ A BUKKIT
	array HAS A r ITZ red
	array HAS A g ITZ green
	array HAS A b ITZ blue
	array HAS A a ITZ alpha
	FOUND YR array
IF U SAY SO

I HAS A white ITZ I IZ color YR 255 AN YR 255 AN YR 255 AN YR 255 MKAY
I HAS A yellow ITZ I IZ color YR 252 AN YR 221 AN YR 9 AN YR 255 MKAY
I HAS A red ITZ I IZ color YR 218 AN YR 18 AN YR 26 AN YR 255 MKAY
I HAS A ameriRed ITZ I IZ color YR 178 AN YR 34 AN YR 52 AN YR 255 MKAY
I HAS A ameriBlue ITZ I IZ color YR 60 AN YR 59 AN YR 110 AN YR 255 MKAY
BTW --- End of Color creator ---

BTW --- Vector2 creator ---
HOW IZ I vector2 YR posx AN YR posy
	I HAS A vec2 ITZ A BUKKIT
	vec2 HAS A x ITZ posx
	vec2 HAS A y ITZ posy
	FOUND YR vec2
IF U SAY SO
BTW --- End of Vector2 creator ---

BTW --- Rectangle creator ---
HOW IZ I rectangle YR posx AN YR posy AN YR w AN YR h
	I HAS A rect ITZ A BUKKIT
	rect HAS A x ITZ posx
	rect HAS A y ITZ posy
	rect HAS A width ITZ w
	rect HAS A height ITZ h
	FOUND YR rect	
IF U SAY SO
BTW --- End of Rectangle creator ---

BTW Define some keys
I HAS A KEYRIGHT ITZ 262
I HAS A KEYLEFT ITZ 263
I HAS A KEYDOWN ITZ 264
I HAS A KEYUP ITZ 265
I HAS A KEYW ITZ 87
I HAS A KEYA ITZ 65
I HAS A KEYS ITZ 83
I HAS A KEYD ITZ 68
I HAS A KEYR ITZ 82
I HAS A KEYZ ITZ 90
I HAS A KEYSPACE ITZ 32

BTW DrawTexturePro wrapper
HOW IZ I drawTexturePro YR texture AN YR source AN YR dest AN YR origin AN YR rotation AN YR color	
	I IZ RAYLIB'Z DRAWTEXTUREPRO ...
		YR texture ...
		AN YR source'Z x AN YR source'Z y AN YR source'Z width AN YR source'Z height ...
		AN YR dest'Z x AN YR dest'Z y AN YR dest'Z width AN YR dest'Z height ...
		AN YR origin'Z x AN YR origin'Z y ...
		AN YR PRODUKT OF rotation AN QUOSHUNT OF 180.0 AN 3.141592 ...
		AN YR color'Z r AN YR color'Z g AN YR color'Z b AN YR color'Z a ...
	MKAY
IF U SAY SO

HOW IZ I checkCollisionRecs YR rec1 AN YR rec2
    I HAS A x1 ITZ DIFFRINT rec1'Z x AN BIGGR OF rec1'Z x AN SUM OF rec2'Z x AN rec2'Z width
    I HAS A x2 ITZ DIFFRINT rec2'Z x AN BIGGR OF rec2'Z x AN SUM OF rec1'Z x AN rec1'Z width
    I HAS A y1 ITZ DIFFRINT rec1'Z y AN BIGGR OF rec1'Z y AN SUM OF rec2'Z y AN rec2'Z height
    I HAS A y2 ITZ DIFFRINT rec2'Z y AN BIGGR OF rec2'Z y AN SUM OF rec1'Z y AN rec1'Z height
    FOUND YR ALL OF x1 AN x2 AN y1 AN y2 MKAY
IF U SAY SO

BTW --- End of utils functions ---
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
BTW --- Player object ---
O HAI IM Player
	I HAS A texture
	I HAS A hitbox
	I HAS A position

	I HAS A SOURCE ITZ I IZ rectangle YR 0.0 AN YR 0.0 AN YR 231.0 AN YR 240.0 MKAY
	I HAS A ORIGIN ITZ I IZ vector2 YR 0.0 AN YR 0.0 MKAY

	HOW IZ I initPlayer
		ME'Z texture R I IZ RAYLIB'Z LOADTEXTURE YR "assets/graphics/a_fk_leaf.png" MKAY
		ME'Z position R I IZ rectangle YR 600.0 AN YR 660.0 AN YR 50.0 AN YR 50.0 MKAY
		ME'Z hitbox R I IZ rectangle YR 100.0 AN YR 660.0 AN YR 20.0 AN YR 20.0 MKAY
	IF U SAY SO

    HOW IZ I collision YR bulletRect
        I HAS A col ITZ I IZ checkCollisionRecs YR ME'Z hitbox AN YR bulletRect MKAY
        FOUND YR col
    IF U SAY SO

	HOW IZ I movement
		I HAS A movement ITZ 0.0
		I HAS A possibleNewPos ITZ ME'Z position'Z x

        BTW Check key pressed
		EITHER OF I IZ RAYLIB'Z IZKEYDOWN YR KEYLEFT MKAY AN I IZ RAYLIB'Z IZKEYDOWN YR KEYA MKAY
		O RLY?, YA RLY
			movement R PRODUKT OF -1.0 AN 200.0
		MEBBE EITHER OF I IZ RAYLIB'Z IZKEYDOWN YR KEYRIGHT MKAY AN I IZ RAYLIB'Z IZKEYDOWN YR KEYD MKAY
			movement R 200.0
		OIC

        possibleNewPos R SUM OF ME'Z position'Z x AN PRODUKT OF movement AN I IZ RAYLIB'Z GETFRAMETIME MKAY

		BTW Check the window limits
		I HAS A offsetLeft ITZ DIFF OF possibleNewPos AN -50.0
		I HAS A offsetRight ITZ SUM OF possibleNewPos AN 50.0
		I HAS A leftOnScreen ITZ DIFFRINT offsetLeft AN SMALLR OF offsetLeft AN 60.0
		I HAS A rightOnScreen ITZ DIFFRINT offsetRight AN BIGGR OF offsetRight AN 1250.0

		BOTH OF leftOnScreen AN rightOnScreen
		O RLY?, YA RLY, ME'Z position'Z x R possibleNewPos, OIC
	IF U SAY SO

	HOW IZ I updatePlayer
		ME IZ movement MKAY
		ME'Z hitbox'Z x R SUM OF ME'Z position'Z x AN 15
		ME'Z hitbox'Z y R SUM OF ME'Z position'Z y AN 15
	IF U SAY SO

	HOW IZ I drawPlayer
		I IZ drawTexturePro ...
			YR ME'Z texture AN YR ME'Z SOURCE AN YR ME'Z position ...
			AN YR ME'Z ORIGIN AN YR 0.0 AN YR white ...
		MKAY
        BTW I IZ RAYLIB'Z DRAWRECTANGLEREC YR ME'Z hitbox'Z x AN YR ME'Z hitbox'Z y AN YR ME'Z hitbox'Z width AN YR ME'Z hitbox'Z height AN YR 255 AN YR 255 AN YR 255 AN YR 255 MKAY
	IF U SAY SO
KTHX
BTW --- End of Player object ---

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

HOW IZ I drawBackground
    I HAS A rectStripe ITZ I IZ rectangle YR 0.0 AN YR 0.0 AN YR 1260.0 AN YR 55.0 MKAY
    IM IN YR stripes UPPIN YR n WILE DIFFRINT n AN 13
        BOTH SAEM MOD OF n AN 2 AN 0
        O RLY?, YA RLY
            I IZ RAYLIB'Z DRAWRECTANGLEREC YR ...
                rectStripe'Z x AN YR rectStripe'Z y AN YR ...
                rectStripe'Z width AN YR rectStripe'Z height AN YR ...
                ameriRed'Z r AN YR ameriRed'Z g AN YR ameriRed'Z b AN YR ...
                ameriRed'Z a ...
            MKAY
        NO WAI
            I IZ RAYLIB'Z DRAWRECTANGLEREC YR ...
                rectStripe'Z x AN YR rectStripe'Z y AN YR ...
                rectStripe'Z width AN YR rectStripe'Z height AN YR ...
                white'Z r AN YR white'Z g AN YR white'Z b AN YR white'Z a ...
            MKAY
        OIC
        rectStripe'Z y R SUM OF rectStripe'Z y AN 55
    IM OUTTA YR stripes
    I IZ RAYLIB'Z DRAWRECTANGLEREC YR 0.0 AN YR 0.0 AN YR 500.0 AN YR 385.0 AN YR 60 AN YR 59 AN YR 110 AN YR 255 MKAY
IF U SAY SO

I IZ RAYLIB'Z WINDUS YR 1260 AN YR 720 AN YR "Flag Wars 3: America Invaders" MKAY
I IZ RAYLIB'Z FPS YR 60 MKAY

I HAS A player ITZ LIEK A Player
player IZ initPlayer MKAY

I HAS A playerBullet ITZ LIEK A Bullet
playerBullet IZ initBullet YR ...
    "assets/graphics/a_fk_leaf.png" AN YR ...
    player'Z SOURCE AN YR player'Z ORIGIN AN YR 0.0 AN YR 0.0 AN YR 0.0 ...
MKAY

I HAS A blockList ITZ A BUKKIT
IM IN YR setPosition UPPIN YR n WILE DIFFRINT n AN 6
    blockList HAS A SRS n ITZ LIEK A Block
    I HAS A currentBlock ITZ blockList'Z SRS n
    I HAS A currentRect ITZ I IZ rectangle YR SUM OF 120.0 AN PRODUKT OF 200.0 AN n AN YR 600.0 AN YR 50.0 AN YR 80.0 MKAY
    currentBlock IZ initBlock YR currentRect AN YR 0.0 MKAY
IM OUTTA YR setPosition

I HAS A starList ITZ A BUKKIT
I HAS A starX ITZ 40.0
I HAS A starY ITZ 30.0
I HAS A index ITZ 0
IM IN YR setPosition UPPIN YR n WILE DIFFRINT n AN 99 BTW 9 * 11
    I HAS A row ITZ QUOSHUNT OF n AN 11
    I HAS A col ITZ MOD OF n AN 11
    BOTH SAEM MOD OF SUM OF row AN col AN 2 AN 0
    O RLY?, YA RLY
        starList HAS A SRS index ITZ LIEK A Star
        I HAS A currentStar ITZ starList'Z SRS index
        I HAS A currentRect ITZ I IZ rectangle YR SUM OF starX AN PRODUKT OF col AN 42.0 AN YR SUM OF starY AN PRODUKT OF row AN 40.0 AN YR 39.0 AN YR 37.0 MKAY
        currentStar IZ initStar YR currentRect MKAY
        index R SUM OF index AN 1
    OIC
IM OUTTA YR setPosition

I HAS A enemyBulletSource ITZ I IZ rectangle YR 0.0 AN YR 0.0 AN YR 30.0 AN YR 80.0 MKAY
I HAS A enemyBulletOrigin ITZ I IZ vector2 YR 15.0 AN YR 40.0 MKAY

I HAS A enemyBulletList ITZ A BUKKIT
IM IN YR createEnemyBullet UPPIN YR n WILE DIFFRINT n AN 3
    enemyBulletList HAS A SRS n ITZ LIEK A Bullet
    I HAS A currentEnemyBullet ITZ enemyBulletList'Z SRS n
    I HAS A randTimer ITZ I IZ random YR 8.0 AN YR 15.0 MKAY
    currentEnemyBullet IZ initBullet YR ...
        "assets/graphics/boy.png" AN YR ...
        enemyBulletSource AN YR enemyBulletOrigin ...
        AN YR randTimer AN YR 8.0 AN YR 15.0 ...
    MKAY
IM OUTTA YR createEnemyBullet

I HAS A gameover ITZ FAIL
I HAS A levelComplete ITZ FAIL

I IZ RAYLIB'Z INITAUDIODEVICE MKAY

I HAS A music ITZ I IZ RAYLIB'Z LOADMUSIC YR "assets/music/Boss.wav" MKAY
I IZ RAYLIB'Z PLAYMUSIC YR music MKAY

I HAS A glassCrack ITZ I IZ RAYLIB'Z LOADSOUND YR "assets/sfx/554570__greg_surr__glass-shatter-5.wav" MKAY
I HAS A glassShatter ITZ I IZ RAYLIB'Z LOADSOUND YR "assets/sfx/202093__spookymodem__bottle-shattering.wav" MKAY
I HAS A shoot ITZ I IZ RAYLIB'Z LOADSOUND YR "assets/sfx/shoot.wav" MKAY
I HAS A playerDeath ITZ I IZ RAYLIB'Z LOADSOUND YR "assets/sfx/death.wav" MKAY

I HAS A score ITZ 0

IM IN YR mainLoop
    BOTH OF NOT gameover AN NOT levelComplete, O RLY?, YA RLY
        I IZ RAYLIB'Z UPDATEMUSIC YR music MKAY
        player IZ updatePlayer MKAY
        Star IZ update YR starList MKAY
        gameover R Star IZ starReachedBottom YR starList MKAY
        gameover, O RLY?, YA RLY, I IZ RAYLIB'Z PLAYSOUND YR playerDeath MKAY, OIC

        BOTH SAEM Star'Z aliveCount AN 0
        O RLY?, YA RLY
            levelComplete R WIN
        OIC

        playerBullet'Z alive
        O RLY?, YA RLY
            I HAS A destSize ITZ I IZ vector2 YR 20.0 AN YR 20.0 MKAY
            I HAS A playerBulletRect ITZ I IZ playerBullet'Z getRekt YR destSize MKAY

            playerBullet IZ updateBullet MKAY

            Star IZ collision YR starList AN YR playerBulletRect MKAY
            O RLY?, YA RLY
                playerBullet'Z alive R FAIL
                score R SUM OF score AN 1776
                Star'Z aliveCount R DIFF OF Star'Z aliveCount AN 1
                Star'Z aliveCount, WTF?
                    OMG 25, Star'Z MAXTIMER R 0.4, GTFO
                    OMG 10, Star'Z MAXTIMER R 0.3, GTFO
                    OMG 2, Star'Z MAXTIMER R 0.13, GTFO
                    OMG 1, Star'Z MAXTIMER R 0.08, GTFO
                    OMGWTF, GTFO
                OIC
                BTW Star'Z MAXTIMER R DIFF OF Star'Z timer AN 0.002
            NO WAI
                I HAS A col ITZ Block IZ checkCollisionBlock YR blockList AN YR playerBulletRect MKAY
                BOTH SAEM col AN 1
                O RLY?, YA RLY
                    I IZ RAYLIB'Z PLAYSOUND YR glassCrack MKAY
                    playerBullet'Z alive R FAIL
                MEBBE BOTH SAEM col AN 0
                    I IZ RAYLIB'Z PLAYSOUND YR glassShatter MKAY
                    playerBullet'Z alive R FAIL
                OIC
            OIC
        OIC

        BOTH OF I IZ RAYLIB'Z IZKEYPRESSED YR KEYSPACE MKAY AN NOT playerBullet'Z alive
        O RLY?, YA RLY
            I IZ RAYLIB'Z PLAYSOUND YR shoot MKAY
            playerBullet IZ setBullet YR player'Z position AN YR -265.0 MKAY
        OIC

        IM IN YR enemyShoot UPPIN YR n WILE DIFFRINT n AN 3
            I HAS A currentBullet ITZ enemyBulletList'Z SRS n
            currentBullet'Z alive
            O RLY?, YA RLY,
                I HAS A destSize ITZ I IZ vector2 YR 30.0 AN YR 80.0 MKAY
                I HAS A enemyBulletRect ITZ I IZ currentBullet'Z getRekt YR destSize MKAY
                currentBullet IZ updateBullet MKAY
                BTW Star IZ collision YR starList AN YR playerBulletRect MKAY
                BTW O RLY?, YA RLY, playerBullet'Z alive R FAIL, OIC
                Player IZ collision YR enemyBulletRect MKAY
                O RLY?, YA RLY
                    currentBullet'Z alive R FAIL
                    gameover R WIN
                    GTFO
                NO WAI
                    I HAS A col ITZ Block IZ checkCollisionBlock YR blockList AN YR enemyBulletRect MKAY
                    BOTH SAEM col AN 1
                    O RLY?, YA RLY,
                        I IZ RAYLIB'Z PLAYSOUND YR glassCrack MKAY
                        currentBullet'Z alive R FAIL
                    MEBBE BOTH SAEM col AN 0
                        I IZ RAYLIB'Z PLAYSOUND YR glassShatter MKAY
                        currentBullet'Z alive R FAIL
                    OIC
                OIC
            NO WAI
                currentBullet IZ updateTimer YR starList MKAY
            OIC
        IM OUTTA YR enemyShoot
    MEBBE EITHER OF gameover AN levelComplete
        I IZ RAYLIB'Z IZKEYPRESSED YR KEYR MKAY
        O RLY?, YA RLY
            gameover R FAIL
            Star'Z leftMost R 0
            Star'Z rightMost R 5
            Star'Z MAXTIMER R 0.6
            Star'Z aliveCount R 50
            BTW Reset stars
            index R 0
            IM IN YR setPosition UPPIN YR n WILE DIFFRINT n AN 99 BTW 9 * 11
                I HAS A row ITZ QUOSHUNT OF n AN 11
                I HAS A col ITZ MOD OF n AN 11
                BOTH SAEM MOD OF SUM OF row AN col AN 2 AN 0
                O RLY?, YA RLY
                    I HAS A currentStar ITZ starList'Z SRS index
                    I HAS A currentRect ITZ I IZ rectangle YR SUM OF starX AN PRODUKT OF col AN 42.0 AN YR SUM OF starY AN PRODUKT OF row AN 40.0 AN YR 39.0 AN YR 37.0 MKAY
                    currentStar IZ reset YR currentRect MKAY
                    index R SUM OF index AN 1
                OIC
            IM OUTTA YR setPosition

            BTW Reset blocks
            NOT levelComplete, O RLY?, YA RLY
                score R 0
                IM IN YR setPosition UPPIN YR n WILE DIFFRINT n AN 6
                    I HAS A currentBlock ITZ blockList'Z SRS n
                    I HAS A currentRect ITZ I IZ rectangle YR SUM OF 120.0 AN PRODUKT OF 200.0 AN n AN YR 600.0 AN YR 50.0 AN YR 80.0 MKAY
                    currentBlock IZ reset YR currentRect MKAY
                IM OUTTA YR setPosition
            OIC
            levelComplete R FAIL
        OIC
    OIC

    I IZ RAYLIB'Z BEGINDRAW MKAY
    I IZ RAYLIB'Z BAKGROUND YR 0 AN YR 0 AN YR 0 AN YR 255 MKAY
    I IZ drawBackground MKAY
    
    NOT gameover, O RLY?, YA RLY
        I IZ player'Z drawPlayer MKAY
    OIC

    playerBullet'Z alive
    O RLY?, YA RLY
        I HAS A destSize ITZ I IZ vector2 YR 20.0 AN YR 20.0 MKAY
        playerBullet IZ drawBullet YR destSize AN YR 0.0 MKAY
    OIC

    IM IN YR enemyDraw UPPIN YR n WILE DIFFRINT n AN 3
        I HAS A currentBullet ITZ enemyBulletList'Z SRS n
        currentBullet'Z alive
        O RLY?, YA RLY
            I HAS A destSize ITZ I IZ vector2 YR 30.0 AN YR 80.0 MKAY
            currentBullet IZ drawBullet YR destSize AN YR 0.0 MKAY
        OIC
    IM OUTTA YR enemyDraw

    IM IN YR drawStars UPPIN YR n WILE DIFFRINT n AN 50        
        I HAS A currentStar ITZ starList'Z SRS n
        currentStar IZ draw MKAY
    IM OUTTA YR drawStars

    IM IN YR drawBlocks UPPIN YR n WILE DIFFRINT n AN 6
        I HAS A currentBlock ITZ blockList'Z SRS n
        currentBlock IZ drawBlock MKAY
    IM OUTTA YR drawBlocks

    gameover, O RLY?, YA RLY
        I IZ RAYLIB'Z TEXT YR ...
            "Game over! Press R to restart" AN YR ...
            100 AN YR 300 AN YR 70 AN YR 0 AN YR 0 AN YR 0 AN YR 255 ...
        MKAY
    MEBBE levelComplete
        I IZ RAYLIB'Z TEXT YR ...
            "Level complete! Press R to continue" AN YR ...
            5 AN YR 300 AN YR 50 AN YR 0 AN YR 0 AN YR 0 AN YR 255 ...
        MKAY
    OIC

    I HAS A scoreStr ITZ SMOOSH "SCORE: " score MKAY
    I IZ RAYLIB'Z TEXT YR scoreStr AN YR 10 AN YR 10 AN YR 30 AN YR 0 AN YR 0 AN YR 0 AN YR 255 MKAY

    I IZ RAYLIB'Z STOPDRAW MKAY
    I IZ RAYLIB'Z CLOZE MKAY, O RLY?, YA RLY, GTFO, OIC
IM OUTTA YR mainLoop


I IZ RAYLIB'Z UNLOADTEXTURE YR playerBullet'Z texture MKAY
I IZ RAYLIB'Z UNLOADTEXTURE YR Bullet'Z texture MKAY
I IZ RAYLIB'Z UNLOADTEXTURE YR Player'Z texture MKAY
I IZ RAYLIB'Z UNLOADTEXTURE YR Block'Z texture MKAY
I IZ RAYLIB'Z UNLOADTEXTURE YR Star'Z texture MKAY

I IZ RAYLIB'Z UNLOADMUSIC YR music MKAY
I IZ RAYLIB'Z UNLOADSOUND YR glassCrack MKAY
I IZ RAYLIB'Z UNLOADSOUND YR glassShatter MKAY
I IZ RAYLIB'Z UNLOADSOUND YR shoot MKAY
I IZ RAYLIB'Z CLOSEAUDIODEVICE MKAY
I IZ RAYLIB'Z CLOZEWINDUS MKAY

KTHXBYE