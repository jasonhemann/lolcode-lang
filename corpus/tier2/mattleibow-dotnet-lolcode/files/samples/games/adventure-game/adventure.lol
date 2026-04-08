BTW Text Adventure Game - A simple room-based adventure
BTW Demonstrates: functions, loops, switch, I/O, string ops, IT, state via params

HAI 1.2
  BTW game state encoded as a single NUMBR:
  BTW   room = state MOD OF 100
  BTW   has_key = bit in 100s place
  BTW   has_sword = bit in 1000s place
  BTW We use separate variables in main and pass them to functions.

  I HAS A room ITZ 1
  I HAS A has_key ITZ FAIL
  I HAS A has_sword ITZ FAIL
  I HAS A game_over ITZ FAIL

  BTW describe a room by number (pure function, no outer state)
  HOW IZ I describe_room YR r AN YR sword
    r
    WTF?
      OMG 1
        VISIBLE "U R IN A DARK ROOM. THERE IZ A DOOR 2 TEH NORTH."
        VISIBLE "U C A SHINY KEY ON TEH FLOOR."
        GTFO
      OMG 2
        VISIBLE "U R IN A LONG HALLWAY. DOORZ NORTH AN SOUTH."
        VISIBLE "A RUSTY SWORD HANGZ ON TEH WALL."
        GTFO
      OMG 3
        VISIBLE "U R IN A BIG ROOM WIF A SCARY DRAGON!"
        sword
        O RLY?
          YA RLY, VISIBLE "U HAZ A SWORD. MEBBE U CAN FITE?"
          NO WAI, VISIBLE "U HAZ NO WEAPON... DIS IZ BAD."
        OIC
        GTFO
      OMG 4
        VISIBLE "U FOUND TEH TREASURE ROOM! GOLD EVRYWARE!"
        GTFO
      OMGWTF
        VISIBLE "U R IN A VOID. HOW U GET HERE?"
    OIC
    FOUND YR 0
  IF U SAY SO

  BTW main game loop — all state managed here in main scope
  VISIBLE "=== LOLCODE ADVENTURE ==="
  VISIBLE "COMMANDZ:: north, south, take key, take sword, fight, quit"
  VISIBLE ""

  IM IN YR gameloop UPPIN YR turn TIL BOTH SAEM turn AN 1000
    I IZ describe_room YR room AN YR has_sword MKAY
    VISIBLE ""

    game_over
    O RLY?
      YA RLY, GTFO
    OIC

    VISIBLE "WAT DO? "!
    I HAS A cmd
    GIMMEH cmd

    BOTH SAEM cmd AN "quit"
    O RLY?
      YA RLY
        VISIBLE "KTHXBAI! TANKS 4 PLAYIN!"
        GTFO
    OIC

    VISIBLE ""

    BTW process actions inline (state stays in main scope)
    BTW room 1 actions
    BOTH SAEM room AN 1
    O RLY?
      YA RLY
        BOTH SAEM cmd AN "north"
        O RLY?
          YA RLY, room R 2
        OIC
        BOTH SAEM cmd AN "take key"
        O RLY?
          YA RLY
            has_key
            O RLY?
              YA RLY, VISIBLE "U ALREADY HAZ TEH KEY"
              NO WAI
                has_key R WIN
                VISIBLE "U PICKED UP TEH KEY!"
            OIC
        OIC
    OIC

    BTW room 2 actions
    BOTH SAEM room AN 2
    O RLY?
      YA RLY
        BOTH SAEM cmd AN "south"
        O RLY?
          YA RLY, room R 1
        OIC
        BOTH SAEM cmd AN "north"
        O RLY?
          YA RLY
            has_key
            O RLY?
              YA RLY
                VISIBLE "U USE TEH KEY 2 OPEN TEH DOOR..."
                room R 3
              NO WAI
                VISIBLE "TEH DOOR IZ LOCKED. U NEED A KEY."
            OIC
        OIC
        BOTH SAEM cmd AN "take sword"
        O RLY?
          YA RLY
            has_sword
            O RLY?
              YA RLY, VISIBLE "U ALREADY HAZ TEH SWORD"
              NO WAI
                has_sword R WIN
                VISIBLE "U TOOK TEH RUSTY SWORD! IZ DANGEROUS."
            OIC
        OIC
    OIC

    BTW room 3 actions (dragon room)
    BOTH SAEM room AN 3
    O RLY?
      YA RLY
        BOTH SAEM cmd AN "fight"
        O RLY?
          YA RLY
            has_sword
            O RLY?
              YA RLY
                VISIBLE "U SWING TEH SWORD AN DEFEAT TEH DRAGON!"
                VISIBLE "TEH WAI 2 TEH TREASURE IZ OPEN!"
                room R 4
              NO WAI
                VISIBLE "U TRY 2 PUNCH TEH DRAGON..."
                VISIBLE "TEH DRAGON EATZ U. GAME OVER."
                game_over R WIN
            OIC
        OIC
        BOTH SAEM cmd AN "south"
        O RLY?
          YA RLY
            VISIBLE "U RUN AWAY FROM TEH DRAGON!"
            room R 2
        OIC
    OIC

    BTW room 4 (treasure - you win!)
    BOTH SAEM room AN 4
    O RLY?
      YA RLY
        VISIBLE "U ALREADY WON! TEH TREASURE IZ YOURZ!"
        game_over R WIN
    OIC

    VISIBLE ""
  IM OUTTA YR gameloop
KTHXBYE
