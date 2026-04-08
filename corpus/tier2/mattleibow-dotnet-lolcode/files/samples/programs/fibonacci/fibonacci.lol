BTW Fibonacci - Iterative and function-based approaches
BTW Demonstrates: functions, loops, multiple variables, return values

HAI 1.2
  BTW iterative fibonacci
  HOW IZ I fib_iter YR n
    BOTH SAEM n AN 0
    O RLY?
      YA RLY, FOUND YR 0
    OIC
    BOTH SAEM n AN 1
    O RLY?
      YA RLY, FOUND YR 1
    OIC

    I HAS A prev ITZ 0
    I HAS A curr ITZ 1
    I HAS A temp

    IM IN YR fibloop UPPIN YR i TIL BOTH SAEM i AN DIFF OF n AN 1
      temp R curr
      curr R SUM OF prev AN curr
      prev R temp
    IM OUTTA YR fibloop

    FOUND YR curr
  IF U SAY SO

  BTW print first 20 fibonacci numbers
  VISIBLE "FIRST 20 FIBONACCI NUMBRZ::"
  IM IN YR printer UPPIN YR i TIL BOTH SAEM i AN 20
    I IZ fib_iter YR i MKAY
    VISIBLE "  FIB(" i ") = " IT
  IM OUTTA YR printer
KTHXBYE
