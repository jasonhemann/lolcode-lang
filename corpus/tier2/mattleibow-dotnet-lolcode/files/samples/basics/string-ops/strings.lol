BTW String Operations - Concatenation, escapes, and interpolation
BTW Demonstrates: SMOOSH, string escapes (:) :> :: :"), :{var} interpolation, VISIBLE

HAI 1.2
  BTW basic string concatenation with SMOOSH
  I HAS A first ITZ "CEILING"
  I HAS A last ITZ "CAT"
  I HAS A fullname ITZ SMOOSH first AN " " AN last MKAY
  VISIBLE fullname

  BTW escape sequences
  VISIBLE "LINE 1:)LINE 2"
  VISIBLE "COL1:>COL2:>COL3"
  VISIBLE "HE SED ::HAI::!"
  VISIBLE "SHE SED :"OH RLY?:""

  BTW string interpolation with :{var}
  I HAS A animal ITZ "KITTEH"
  I HAS A count ITZ 3
  VISIBLE "I HAZ :{count} :{animal}Z"

  BTW building strings in a loop
  I HAS A stars ITZ ""
  IM IN YR starmaker UPPIN YR i TIL BOTH SAEM i AN 10
    stars R SMOOSH stars AN "*" MKAY
    VISIBLE stars
  IM OUTTA YR starmaker

  BTW VISIBLE with multiple arguments (auto-concatenation)
  VISIBLE "OH HAI " first " " last "!"
KTHXBYE
