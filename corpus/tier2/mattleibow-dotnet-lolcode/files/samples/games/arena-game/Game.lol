BTW ========================================
BTW   LOLCODE ARENA - Turn-Based Battle Game
BTW ========================================
BTW Demonstrates: functions, loops, switch, conditionals, math,
BTW   string ops, I/O, casting, IT, GTFO, BIGGR/SMALLR OF

HAI 1.2

  BTW ---- helper functions ----

  BTW print a separator line
  HOW IZ I separator
    VISIBLE "----------------------------------------"
    FOUND YR 0
  IF U SAY SO

  BTW print a double separator line
  HOW IZ I big_separator
    VISIBLE "========================================"
    FOUND YR 0
  IF U SAY SO

  BTW calculate damage: atk - def, minimum 1
  HOW IZ I calc_damage YR atk AN YR def
    I HAS A dmg ITZ DIFF OF atk AN def
    FOUND YR BIGGR OF dmg AN 1
  IF U SAY SO

  BTW display HP bar: name [####----] hp/max
  HOW IZ I show_hp YR name AN YR hp AN YR max_hp
    I HAS A bar ITZ "["
    I HAS A filled ITZ QUOSHUNT OF PRODUKT OF hp AN 10 AN max_hp
    I HAS A empty ITZ DIFF OF 10 AN filled

    BTW build the filled portion
    IM IN YR fill UPPIN YR f TIL BOTH SAEM f AN filled
      bar R SMOOSH bar AN "#" MKAY
    IM OUTTA YR fill

    BTW build the empty portion
    IM IN YR emp UPPIN YR e TIL BOTH SAEM e AN empty
      bar R SMOOSH bar AN "-" MKAY
    IM OUTTA YR emp

    bar R SMOOSH bar AN "]" MKAY
    VISIBLE "  " name " " bar " " hp "/" max_hp " HP"
    FOUND YR 0
  IF U SAY SO

  BTW get enemy name by round number
  HOW IZ I enemy_name YR round
    round
    WTF?
      OMG 1, FOUND YR "ANGRY KITTEH"
      OMG 2, FOUND YR "TROLLFACE"
      OMG 3, FOUND YR "SPAM BOT"
      OMG 4, FOUND YR "404 DRAGON"
      OMG 5, FOUND YR "CEILIN CAT"
    OIC
    FOUND YR "MYSTERY"
  IF U SAY SO

  BTW get enemy max HP by round number
  HOW IZ I enemy_max_hp YR round
    round
    WTF?
      OMG 1, FOUND YR 30
      OMG 2, FOUND YR 50
      OMG 3, FOUND YR 70
      OMG 4, FOUND YR 100
      OMG 5, FOUND YR 150
    OIC
    FOUND YR 10
  IF U SAY SO

  BTW get enemy attack by round number
  HOW IZ I enemy_atk YR round
    round
    WTF?
      OMG 1, FOUND YR 8
      OMG 2, FOUND YR 12
      OMG 3, FOUND YR 15
      OMG 4, FOUND YR 20
      OMG 5, FOUND YR 25
    OIC
    FOUND YR 5
  IF U SAY SO

  BTW get enemy defense by round number
  HOW IZ I enemy_def YR round
    round
    WTF?
      OMG 1, FOUND YR 2
      OMG 2, FOUND YR 4
      OMG 3, FOUND YR 6
      OMG 4, FOUND YR 8
      OMG 5, FOUND YR 10
    OIC
    FOUND YR 0
  IF U SAY SO

  BTW get enemy taunt for start of battle
  HOW IZ I enemy_taunt YR round
    round
    WTF?
      OMG 1
        VISIBLE "  TEH KITTEH HISSEZ AT U! *HSSSS*"
        GTFO
      OMG 2
        VISIBLE "  TROLLFACE SEZ:: U MAD BRO?"
        GTFO
      OMG 3
        VISIBLE "  SPAM BOT SEZ:: I CAN HAS UR CREDENTIALZ?"
        GTFO
      OMG 4
        VISIBLE "  404 DRAGON SEZ:: UR PAGE NOT FOUND... UR LIFE NOT FOUND!"
        GTFO
      OMG 5
        VISIBLE "  CEILIN CAT SEZ:: I BEEN WATCHIN U... NOW U DIE."
        GTFO
    OIC
    FOUND YR 0
  IF U SAY SO

  BTW ---- main game ----

  I IZ big_separator MKAY
  VISIBLE "       L O L C O D E   A R E N A"
  VISIBLE ""
  VISIBLE "   FITE 5 ENEMYZ 2 BECOME TEH CHAMPION!"
  I IZ big_separator MKAY
  VISIBLE ""

  VISIBLE "WAT IZ UR NAME, WARRIOR? "!
  I HAS A player_name
  GIMMEH player_name
  VISIBLE ""
  VISIBLE "WELCOM 2 TEH ARENA, " player_name "!"
  VISIBLE ""

  BTW player stats
  I HAS A player_hp ITZ 100
  I HAS A player_max_hp ITZ 100
  I HAS A player_atk ITZ 15
  I HAS A player_def ITZ 5
  I HAS A potions ITZ 3
  I HAS A defending ITZ FAIL
  I HAS A arena_over ITZ FAIL
  I HAS A player_won ITZ FAIL

  BTW arena loop: 5 rounds
  I HAS A round ITZ 1
  IM IN YR arena UPPIN YR round_tick TIL BOTH SAEM round AN 6

    arena_over
    O RLY?
      YA RLY, GTFO
    OIC

    BTW get enemy stats for this round
    I HAS A e_name ITZ I IZ enemy_name YR round MKAY
    I HAS A e_hp ITZ I IZ enemy_max_hp YR round MKAY
    I HAS A e_max_hp ITZ e_hp
    I HAS A e_atk ITZ I IZ enemy_atk YR round MKAY
    I HAS A e_def ITZ I IZ enemy_def YR round MKAY

    I IZ big_separator MKAY
    VISIBLE "  ROUND " round " OF 5:: " e_name " APPROCHEZ!"
    I IZ enemy_taunt YR round MKAY
    I IZ big_separator MKAY
    VISIBLE ""

    BTW battle loop
    IM IN YR battle UPPIN YR battle_turn TIL BOTH SAEM battle_turn AN 999

      BTW show status
      I IZ separator MKAY
      I IZ show_hp YR player_name AN YR player_hp AN YR player_max_hp MKAY
      I IZ show_hp YR e_name AN YR e_hp AN YR e_max_hp MKAY
      VISIBLE "  POTIONZ:: " potions
      I IZ separator MKAY

      BTW get player action
      VISIBLE ""
      VISIBLE "  WAT DO? (attack / defend / heal / flee)"
      VISIBLE "  > "!
      I HAS A action
      GIMMEH action
      VISIBLE ""

      BTW reset defending each turn
      defending R FAIL
      I HAS A e_dmg ITZ 0

      BTW handle action
      BOTH SAEM action AN "attack"
      O RLY?
        YA RLY
          BTW player attacks enemy
          I HAS A p_dmg ITZ I IZ calc_damage YR player_atk AN YR e_def MKAY
          e_hp R DIFF OF e_hp AN p_dmg
          e_hp R BIGGR OF e_hp AN 0
          VISIBLE "  " player_name " ATTACKZ " e_name " 4 " p_dmg " DAMAGE!"

          BTW check if enemy defeated
          BOTH SAEM e_hp AN 0
          O RLY?
            YA RLY
              VISIBLE ""
              VISIBLE "  " e_name " HAZ BEEN DEFEATED!"

              BTW heal bonus between rounds
              I HAS A heal_bonus ITZ 10
              player_hp R SUM OF player_hp AN heal_bonus
              player_hp R SMALLR OF player_hp AN player_max_hp
              VISIBLE "  U REST AN RECOVR " heal_bonus " HP."

              round R SUM OF round AN 1
              VISIBLE ""

              BTW check if all enemies beaten
              BOTH SAEM round AN 6
              O RLY?
                YA RLY
                  player_won R WIN
                  arena_over R WIN
              OIC
              GTFO
          OIC

          BTW enemy counter-attacks
          e_dmg R I IZ calc_damage YR e_atk AN YR player_def MKAY
          player_hp R DIFF OF player_hp AN e_dmg
          player_hp R BIGGR OF player_hp AN 0
          VISIBLE "  " e_name " HITZ " player_name " 4 " e_dmg " DAMAGE!"
      OIC

      BOTH SAEM action AN "defend"
      O RLY?
        YA RLY
          defending R WIN
          VISIBLE "  " player_name " RAISEZ SHIELD! DEF UP DIS TURN!"

          BTW enemy attacks at half damage
          e_dmg R I IZ calc_damage YR e_atk AN YR player_def MKAY
          e_dmg R QUOSHUNT OF e_dmg AN 2
          e_dmg R BIGGR OF e_dmg AN 1
          player_hp R DIFF OF player_hp AN e_dmg
          player_hp R BIGGR OF player_hp AN 0
          VISIBLE "  " e_name " HITZ " player_name " 4 ONLY " e_dmg " DAMAGE! (BLOCKED)"
      OIC

      BOTH SAEM action AN "heal"
      O RLY?
        YA RLY
          BOTH SAEM potions AN 0
          O RLY?
            YA RLY
              VISIBLE "  U HAZ NO POTIONZ LEFT! TURN WASTED!"
            NO WAI
              potions R DIFF OF potions AN 1
              I HAS A old_hp ITZ player_hp
              player_hp R SUM OF player_hp AN 30
              player_hp R SMALLR OF player_hp AN player_max_hp
              I HAS A healed ITZ DIFF OF player_hp AN old_hp
              VISIBLE "  " player_name " DRINKZ A POTION! +" healed " HP!"
          OIC

          BTW enemy still attacks while healing
          e_dmg R I IZ calc_damage YR e_atk AN YR player_def MKAY
          player_hp R DIFF OF player_hp AN e_dmg
          player_hp R BIGGR OF player_hp AN 0
          VISIBLE "  " e_name " HITZ " player_name " 4 " e_dmg " DAMAGE!"
      OIC

      BOTH SAEM action AN "flee"
      O RLY?
        YA RLY
          VISIBLE "  " player_name " RUNZ AWAY LIEK A NOOB!"
          arena_over R WIN
          GTFO
      OIC

      BTW check if player died
      BOTH SAEM player_hp AN 0
      O RLY?
        YA RLY
          VISIBLE ""
          VISIBLE "  " player_name " HAZ BEEN DEFEATED BY " e_name "!"
          arena_over R WIN
          GTFO
      OIC

      VISIBLE ""
    IM OUTTA YR battle
  IM OUTTA YR arena

  BTW ---- end game ----
  VISIBLE ""
  I IZ big_separator MKAY

  player_won
  O RLY?
    YA RLY
      VISIBLE "  U DID IT, " player_name "! U R TEH ARENA CHAMPION!"
      VISIBLE ""
      VISIBLE "      *** CHAMPION ***"
      VISIBLE "     *   WINNER!   *"
      VISIBLE "      ***  ***  ***"
      VISIBLE ""
      VISIBLE "  FINAL STATS:: " player_hp "/" player_max_hp " HP, " potions " POTIONZ LEFT"
    NO WAI
      VISIBLE "  GAME OVER, " player_name ". TEH ARENA CLAIMZ ANOTHR VICTIM."
      VISIBLE ""
      VISIBLE "  MEBBE TRY AGAIN? PROTIP:: DEFEND + HEAL = WIN"
  OIC

  I IZ big_separator MKAY
  VISIBLE ""
  VISIBLE "TANKS 4 PLAYIN LOLCODE ARENA!"
  VISIBLE ""

KTHXBYE
