BTW Conditionals - If/else and truthiness
BTW Demonstrates: O RLY?, YA RLY, NO WAI, MEBBE, OIC, truthiness rules

HAI 1.2
  BTW simple if/else
  I HAS A temp ITZ 75

  BOTH SAEM BIGGR OF temp AN 80 AN temp
  O RLY?
    YA RLY
      VISIBLE "IZ HOT OUTSIDE! " temp " DEGREES"
    NO WAI
      VISIBLE "IZ NICE OUTSIDE! " temp " DEGREES"
  OIC

  BTW if/else-if/else chain
  I HAS A score ITZ 85

  BOTH SAEM BIGGR OF score AN 90 AN score
  O RLY?
    YA RLY
      VISIBLE "GRADE:: A"
    MEBBE BOTH SAEM BIGGR OF score AN 80 AN score
      VISIBLE "GRADE:: B"
    MEBBE BOTH SAEM BIGGR OF score AN 70 AN score
      VISIBLE "GRADE:: C"
    NO WAI
      VISIBLE "GRADE:: F... OH NOES"
  OIC

  BTW truthiness examples
  I HAS A empty_string ITZ ""
  I HAS A zero ITZ 0
  I HAS A positive ITZ 42
  I HAS A full_string ITZ "HAI"

  empty_string
  O RLY?
    YA RLY, VISIBLE "EMPTY STRING IZ TRUTHY"
    NO WAI, VISIBLE "EMPTY STRING IZ FALSY"
  OIC

  zero
  O RLY?
    YA RLY, VISIBLE "ZERO IZ TRUTHY"
    NO WAI, VISIBLE "ZERO IZ FALSY"
  OIC

  positive
  O RLY?
    YA RLY, VISIBLE "POSITIVE NUMBR IZ TRUTHY"
    NO WAI, VISIBLE "POSITIVE NUMBR IZ FALSY"
  OIC
KTHXBYE
