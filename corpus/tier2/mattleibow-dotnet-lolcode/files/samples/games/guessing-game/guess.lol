BTW Guessing Game - Interactive number guessing
BTW Demonstrates: GIMMEH input, loops, conditionals, casting, GTFO, comparison

HAI 1.2
  I HAS A secret ITZ 42
  I HAS A guesses ITZ 0
  I HAS A won ITZ FAIL

  VISIBLE "I IZ THINKIN OF A NUMBR BETWEEN 1 AN 100"
  VISIBLE "CAN U GESS IT?"
  VISIBLE ""

  IM IN YR guessing UPPIN YR attempt TIL BOTH SAEM attempt AN 10
    VISIBLE "GESS #" SUM OF attempt AN 1 ":: "!
    I HAS A input
    GIMMEH input
    input IS NOW A NUMBR
    guesses R SUM OF guesses AN 1

    BTW check if correct
    BOTH SAEM input AN secret
    O RLY?
      YA RLY
        VISIBLE "OMG U GOT IT IN " guesses " GESSES!"
        won R WIN
        GTFO
      NO WAI
        BTW give hints
        BOTH SAEM BIGGR OF input AN secret AN input
        O RLY?
          YA RLY, VISIBLE "2 HI! TRY LOER"
          NO WAI, VISIBLE "2 LO! TRY HIER"
        OIC
    OIC
  IM OUTTA YR guessing

  NOT won
  O RLY?
    YA RLY
      VISIBLE "U RAN OUTTA GESSES! TEH NUMBR WUZ " secret
  OIC

  VISIBLE "KTHXBAI!"
KTHXBYE
