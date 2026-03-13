HAI 1.2

BTW Game introduction and setup
VISIBLE "WELCOM 2 TEH PURPLE VALLEY ADVENTURE! GO EPHS!"
VISIBLE "UR A FRESH FROSH AT WILLIAMS, SURVIVIN UR FIRST WEEK!"
VISIBLE "CAN U BALANCE UR EPIC MEAL PLAN, AVOID TEH DREADED 8AM CLASS, & BECOME A CS LEGEND?"
VISIBLE ""

BTW Real campus locations:
BTW Dining Halls: Paresky Dining Hall, Driscoll Dining Hall, & SNAR Cafe
BTW Dorms: Mission House & FroshQuad House
BTW CS Professors: Professor Jeannine Wood, Professor Mark Harrison, Professor William McCormick, Professor Daniel Frazier, AND Professor Aaron Levine

BTW Initialize variables
I HAS A choice
I HAS A hasMap ITZ FAIL
I HAS A hasFood ITZ FAIL
I HAS A gameOver ITZ FAIL
I HAS A endingMessage

BTW Main game loop
IM IN YR game
    BOTH SAEM gameOver AN FAIL, O RLY?
        YA RLY
            VISIBLE "STANDIN AT TEH CHAPIN STEPS, PURPLE MOUNTAINS MAJESTY ALL AROUND! WHERE 2?"
            VISIBLE "1: SPRINT 2 PARESKY B4 TEH GOOD FOOD IZ GONE!"
            VISIBLE "2: CHILL AT Mission & MAYBE DO SUM HOMEWORK (LOL)"
            VISIBLE "3: BRAVE TEH CS LECTURE & HOPE 4 FREE PIZZA"
            VISIBLE "WHICH EPIC CHOICE? (TYPE 1, 2 OR 3):"
            GIMMEH choice
            
            BOTH SAEM choice AN "1", O RLY?
                YA RLY
                    VISIBLE "OMG! Paresky'S SERVIN THEIR LEGENDARY MAC & CHEESE 2DAY! TEH LINE IZ EPIC!"
                    VISIBLE "1: WAIT IN LINE LIKE A CHAMPION"
                    VISIBLE "2: SWEET TALK TEH STAFF 4 INSIDER FOOD INTEL"
                    GIMMEH choice
                    
                    BOTH SAEM choice AN "1", O RLY?
                        YA RLY
                            VISIBLE "VICTORY! U SCORED TEH LAST SERVING OF MAC & CHEESE! UR OFFICIALLY A Paresky LEGEND!"
                            hasFood R WIN
                        NO WAI
                            VISIBLE "STAFF WHISPERS ABOUT A SECRET STASH OF PURPLE COW ICE CREAM IN TEH BACK!"
                    OIC
                    
                    VISIBLE "WAIT... IZ DAT A VINTAGE WILLIAMS MAP WITH ALL TEH SECRET TUNNELS?!"
                    VISIBLE "1: YOINK TEH MAP LIKE A NINJA"
                    VISIBLE "2: NAH, GPS IZ LIFE (BUT GPS SIGNAL SUX HERE LOL)"
                    GIMMEH choice
                    
                    BOTH SAEM choice AN "1", O RLY?
                        YA RLY
                            VISIBLE "EPIC MAP GET! NOW U CAN FIND ALL TEH SECRET STUDY SPOTS!"
                            hasMap R WIN
                        NO WAI
                            VISIBLE "NO MAP? GOOD LUCK FINDIN TEH BASEMENT VENDING MACHINES!"
                    OIC
                    VISIBLE "BUT PLOT TWIST - U GET LOST IN TEH ENDLESS Paresky CORRIDORS ANYWAY!"
                    endingMessage R "U GOT TEH 'FOREVER LOST IN Paresky' ENDING! NEXT TIME GRAB DAT MAP, N00B!"
                    gameOver R WIN
                NO WAI
            OIC
            
            BOTH SAEM choice AN "2", O RLY?
                YA RLY
                    VISIBLE "Mission HOUSE BE WILDIN! UR ROOMIE STARTED AN IMPROMPTU KARAOKE NIGHT!"
                    VISIBLE "1: UNLEASH UR INNER PURPLE COW & SING UR HEART OUT"
                    VISIBLE "2: ATTEMPT 2 STUDY WHILE PPL BELT 'MOUNTAINS OF WILLIAMS'"
                    GIMMEH choice
                    
                    BOTH SAEM choice AN "1", O RLY?
                        YA RLY
                            VISIBLE "UR RENDITION OF TEH ALMA MATER BRINGS TEARS 2 EVERYONE'S EYES (NOT IN A GOOD WAY)!"
                            endingMessage R "U GOT TEH 'KARAOKE LEGEND' ENDING! SPOTIFY CAREER WHEN?"
                            gameOver R WIN
                        NO WAI
                            VISIBLE "SOMEHOW U MASTER MULTITASKIN - STUDYIN WHILE HUMMIN TEH CHORUS!"
                            endingMessage R "U GOT TEH 'STUDY WIZARD' ENDING! PRODUCTIVITY LEVEL 9000!"
                            gameOver R WIN
                    OIC
                NO WAI
            OIC
            
            BOTH SAEM choice AN "3", O RLY?
                YA RLY
                    VISIBLE "GILMAN HALL AWAITS! RUMOR HAS IT THERE'S FREE ENERGY DRINKS 4 CS STUDENTS!"
                    VISIBLE "U SEE A WILD STUDY GROUP APPEARIN WITH ACTUAL WORKING CODE!"
                    VISIBLE "1: JOIN TEH CODING PARTY"
                    VISIBLE "2: SOLO QUEUE INTO LECTURE"
                    GIMMEH choice
                    
                    BOTH SAEM choice AN "1", O RLY?
                        YA RLY
                            VISIBLE "TEH GROUP SHARES THEIR DEBUGGING SECRETS & ENERGY DRINK STASH!"
                            BOTH SAEM hasFood AN WIN, O RLY?
                                YA RLY
                                    VISIBLE "FUELED BY Paresky'S MAC & CHEESE, U HELP SOLVE A LEGENDARY BUG!"
                                    VISIBLE "TEH PROFESSORS R SHOOK! THEY OFFER U AN INTERNSHIP ON TEH SPOT!"
                                    VISIBLE "UR CODE WILL BE FEATURED IN TEH NEXT CS TEXTBOOK!"
                                    endingMessage R "U GOT TEH 'DEBUG MASTER' ENDING! STACKOVERFLOW FEARS U!"
                                    gameOver R WIN
                                NO WAI
                                    VISIBLE "HUNGRY & TIRED, U MISTAKE A SEMICOLON 4 A COMMA. RIP CODE."
                                    endingMessage R "U GOT TEH 'HANGRY CODER' ENDING. NEXT TIME EAT B4 U CODE!"
                                    gameOver R WIN
                            OIC
                        NO WAI
                            VISIBLE "U DOZE OFF IN CLASS & DREAM OF INFINITE LOOPS! TEH HORROR!"
                            endingMessage R "U GOT TEH 'STACK OVERFLOW' ENDING. COFFEE IS UR FRIEND!"
                            gameOver R WIN
                    OIC
                NO WAI
            OIC
        NO WAI
            GTFO
    OIC
IM OUTTA YR game

VISIBLE "🐮🐮🐮 PURPLE COW PRIDE! 🐮🐮🐮"
VISIBLE endingMessage
VISIBLE "🐮🐮🐮 EPIC ADVENTURE COMPLETE! 🐮🐮🐮"
VISIBLE "KTHXBYE! SEE U AT MOUNTAIN DAY!"

KTHXBYE
