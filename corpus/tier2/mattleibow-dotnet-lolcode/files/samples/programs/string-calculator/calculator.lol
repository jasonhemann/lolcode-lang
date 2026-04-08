BTW String Calculator - Parse and evaluate simple math expressions
BTW Demonstrates: string parsing, switch, functions, casting, I/O

HAI 1.2
  BTW evaluate a simple operation
  HOW IZ I calc YR a AN YR op AN YR b
    a IS NOW A NUMBAR
    b IS NOW A NUMBAR

    op
    WTF?
      OMG "+"
        FOUND YR SUM OF a AN b
        GTFO
      OMG "-"
        FOUND YR DIFF OF a AN b
        GTFO
      OMG "*"
        FOUND YR PRODUKT OF a AN b
        GTFO
      OMG "/"
        BOTH SAEM b AN 0
        O RLY?
          YA RLY
            VISIBLE "CANT DIVIDE BY ZERO! OH NOES!"
            FOUND YR 0
          NO WAI
            FOUND YR QUOSHUNT OF a AN b
        OIC
        GTFO
      OMGWTF
        VISIBLE "DUNNO WAT " op " MEANZ"
        FOUND YR 0
    OIC
  IF U SAY SO

  BTW interactive calculator loop
  VISIBLE "WELCOM 2 LOLCODE CALCULATR!"
  VISIBLE "ENTER NUMBR, THEN OPERASHUN (+, -, *, /), THEN NUMBR"
  VISIBLE "TYPE 'quit' 2 EXIT"
  VISIBLE ""

  IM IN YR calcloop UPPIN YR round TIL BOTH SAEM round AN 100
    VISIBLE "FIRST NUMBR:: "!
    I HAS A first
    GIMMEH first

    BOTH SAEM first AN "quit"
    O RLY?
      YA RLY, GTFO
    OIC

    VISIBLE "OPERASHUN:: "!
    I HAS A op
    GIMMEH op

    VISIBLE "SECOND NUMBR:: "!
    I HAS A second
    GIMMEH second

    I IZ calc YR first AN YR op AN YR second MKAY
    VISIBLE first " " op " " second " = " IT
    VISIBLE ""
  IM OUTTA YR calcloop

  VISIBLE "KTHXBAI!"
KTHXBYE
