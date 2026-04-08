BTW Loops - Counting, iteration, and break
BTW Demonstrates: IM IN YR, IM OUTTA YR, UPPIN, NERFIN, TIL, WILE, GTFO

HAI 1.2
  BTW count up from 0 to 4
  VISIBLE "COUNTIN UP::"
  IM IN YR countup UPPIN YR i TIL BOTH SAEM i AN 5
    VISIBLE "  " i
  IM OUTTA YR countup

  BTW count down from 5 to 1
  VISIBLE "COUNTIN DOWN::"
  I HAS A j ITZ 5
  IM IN YR countdown NERFIN YR j TIL BOTH SAEM j AN 0
    VISIBLE "  " j
  IM OUTTA YR countdown

  BTW while loop
  VISIBLE "DOUBLIN::"
  I HAS A val ITZ 1
  IM IN YR doubler UPPIN YR n WILE BOTH SAEM SMALLR OF val AN 100 AN val
    VISIBLE "  " val
    val R PRODUKT OF val AN 2
  IM OUTTA YR doubler

  BTW loop with break
  VISIBLE "LOOKIN FOR 7::"
  IM IN YR finder UPPIN YR k TIL BOTH SAEM k AN 100
    BOTH SAEM MOD OF k AN 7 AN 0
    O RLY?
      YA RLY
        BOTH SAEM k AN 0
        O RLY?
          YA RLY, BTW skip zero
          NO WAI
            VISIBLE "  FOUND:: " k
            GTFO
        OIC
    OIC
  IM OUTTA YR finder
KTHXBYE
