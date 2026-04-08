BTW Recursion - Recursive functions for classic algorithms
BTW Demonstrates: recursive function calls, base cases, FOUND YR

HAI 1.2
  BTW recursive factorial
  HOW IZ I factorial YR n
    BOTH SAEM n AN 0
    O RLY?
      YA RLY, FOUND YR 1
    OIC
    FOUND YR PRODUKT OF n AN I IZ factorial YR DIFF OF n AN 1 MKAY
  IF U SAY SO

  BTW recursive fibonacci
  HOW IZ I fib YR n
    BOTH SAEM n AN 0
    O RLY?
      YA RLY, FOUND YR 0
    OIC
    BOTH SAEM n AN 1
    O RLY?
      YA RLY, FOUND YR 1
    OIC
    FOUND YR SUM OF I IZ fib YR DIFF OF n AN 1 MKAY AN I IZ fib YR DIFF OF n AN 2 MKAY
  IF U SAY SO

  BTW recursive power
  HOW IZ I power YR base AN YR exp
    BOTH SAEM exp AN 0
    O RLY?
      YA RLY, FOUND YR 1
    OIC
    FOUND YR PRODUKT OF base AN I IZ power YR base AN YR DIFF OF exp AN 1 MKAY
  IF U SAY SO

  BTW test factorial
  VISIBLE "FACTORIALZ::"
  IM IN YR factloop UPPIN YR i TIL BOTH SAEM i AN 11
    I IZ factorial YR i MKAY
    VISIBLE "  " i "! = " IT
  IM OUTTA YR factloop

  BTW test fibonacci
  VISIBLE ""
  VISIBLE "FIBONACCI::"
  IM IN YR fibloop UPPIN YR i TIL BOTH SAEM i AN 12
    I IZ fib YR i MKAY
    VISIBLE "  FIB(" i ") = " IT
  IM OUTTA YR fibloop

  BTW test power
  VISIBLE ""
  VISIBLE "POWERZ::"
  VISIBLE "  2^8 = " I IZ power YR 2 AN YR 8 MKAY
  VISIBLE "  3^4 = " I IZ power YR 3 AN YR 4 MKAY
  VISIBLE "  5^3 = " I IZ power YR 5 AN YR 3 MKAY
KTHXBYE
