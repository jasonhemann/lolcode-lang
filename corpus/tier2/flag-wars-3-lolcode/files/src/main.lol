HAI 1.4
CAN HAS RAYLIB?
CAN HAS MATH?

BTW INCLUDE "utils.lol" PLS
BTW INCLUDE "bullet.lol" PLS
BTW INCLUDE "player.lol" PLS
BTW INCLUDE "block.lol" PLS
BTW INCLUDE "star.lol" PLS

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