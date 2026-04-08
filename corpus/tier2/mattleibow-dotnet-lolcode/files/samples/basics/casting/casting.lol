BTW Type Casting - Converting between types
BTW Demonstrates: MAEK, IS NOW A, implicit casting, type names

HAI 1.2
  BTW string to number
  I HAS A numstr ITZ "42"
  VISIBLE "BEFORE CAST:: " numstr
  numstr IS NOW A NUMBR
  VISIBLE "AFTER CAST TO NUMBR:: " numstr
  VISIBLE "PLUS 8 = " SUM OF numstr AN 8

  BTW number to string
  I HAS A num ITZ 100
  I HAS A str ITZ MAEK num A YARN
  VISIBLE "NUMBR 100 AS YARN:: " str

  BTW number to float
  I HAS A whole ITZ 7
  whole IS NOW A NUMBAR
  VISIBLE "7 AS NUMBAR:: " whole          BTW prints 7.00 (NUMBAR → YARN = 2 decimal places)

  BTW float to integer (truncates)
  I HAS A pi ITZ 3.14159
  I HAS A rounded ITZ MAEK pi A NUMBR
  VISIBLE "3.14159 AS NUMBR:: " rounded

  BTW boolean to number
  I HAS A truth ITZ WIN
  I HAS A lie ITZ FAIL
  VISIBLE "WIN AS NUMBR:: " MAEK truth A NUMBR
  VISIBLE "FAIL AS NUMBR:: " MAEK lie A NUMBR

  BTW number to boolean (truthiness)
  I HAS A zero ITZ 0
  I HAS A nonzero ITZ 42
  VISIBLE "0 AS TROOF:: " MAEK zero A TROOF
  VISIBLE "42 AS TROOF:: " MAEK nonzero A TROOF

  BTW string to boolean
  I HAS A empty ITZ ""
  I HAS A notempty ITZ "HAI"
  VISIBLE "EMPTY YARN AS TROOF:: " MAEK empty A TROOF
  VISIBLE "NON-EMPTY YARN AS TROOF:: " MAEK notempty A TROOF
KTHXBYE
