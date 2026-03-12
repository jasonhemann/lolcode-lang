HAI 1.4
CAN HAS STDIO?
CAN HAS STRING?

OBTW
 This is how we do the turn calculations. If this language was sane, it would have 
 increment and decrement. Instead, we've got this...
TLDR
HOW IZ I turnin YR turn AND YR direction
    direction R SUM OF direction AN 4
    turn, WTF?
      OMG "R"
        direction R SUM OF direction AN 1
        GTFO
      OMG "L"
        direction R SUM OF direction AN -1
        GTFO
    OIC
    FOUND YR MOD OF direction AN 4
IF U SAY SO

OBTW
  Arrays are really sketchy so instead of matrix selection, we end up doing stupid
  case statements. 
TLDR
HOW IZ I northAdjustin YR direction AN YR distance
    direction, WTF?
      OMG 0
        FOUND YR distance
        GTFO
      OMG 2
        FOUND YR PRODUKT OF distance AN -1
        GTFO
      OMGWTF
        FOUND YR 0
        GTFO
    OIC
IF U SAY SO

OBTW
  And here's another copy of nearly the same function, just because its easier to
  duplicate code than return complex objects (because they don't exist). 
TLDR
HOW IZ I eastAdjustin YR direction AN YR distance
    direction, WTF?
      OMG 1
        FOUND YR distance
        GTFO
      OMG 3
        FOUND YR PRODUKT OF distance AN -1
        GTFO
      OMGWTF
        FOUND YR 0
        GTFO
    OIC
IF U SAY SO

OBTW
  Seriously. There isn't even an absolute value function.
TLDR
HOW IZ I denegatifying YR number
    FOUND YR BIGGR OF number AN PRODUKT OF number AN -1
IF U SAY SO

BTW Can has announcement?
VISIBLE "=============================================="
VISIBLE "I CAN HAZ TAXI JEOMETRY?"
VISIBLE  "============================================="

BTW The same bounded directional index that everyone is using.
I HAS A direction ITZ 0

OBTW
  Grabbing the input. Gotta come from STDIN because there's no way to 
  grab command line arguments. Of course.
TLDR
I HAS A inputz
GIMMEH inputz

OBTW
   Read teh inputz and parsin the yarn
TLDR
I HAS A inputzbignes
inputzbignes R I IZ STRING'Z LEN YR inputz MKAY

OBTW
   Since we're parsing with stone-age code functionality, not only do we
   have to increment the loop boundary, but we've got to force the loop 
   boundary to an extra index past the actual boundary, and then do some 
   stupid loop-state-injection to mimic what the end of a loop might look
   like if the input ended in a terminator or if our code had any chance in
   hell of detecting the end-of-input inside the loop.
TLDR
BTW That probably actually is TL;DR
I HAS A inputztail ITZ SUM OF inputzbignes AN 1
BTW This hurts so much
I HAS A loopzstopper ITZ SUM OF inputztail AN 1

BTW These store the geometric location at each step.
I HAS A northSpot ITZ 0
I HAS A eastSpot ITZ 0

OBTW
    Scoped storage for the currently parsed turn and distance. I just ... 
    Yeah. So you have to parse letter by letter and build up the parsed results
    here. They have to exist outside the loop because the loop generates a new
    context with each run.
TLDR
I HAS A turn ITZ ""
I HAS A distance ITZ ""

BTW This is a for-loop, of sorts.
I HAS A luper ITZ 0
IM IN YR inputsnomnom UPPIN YR luper TIL BOTH SAEM luper AN loopzstopper

    I HAS A blep
    BOTH SAEM luper AN inputztail, O RLY?
      YA RLY
        blep R ","
      NO WAI
        blep R I IZ STRING'Z AT YR inputz AN YR luper MKAY
    OIC

    blep, WTF?
      OMG "R"
      OMG "L"
         turn R blep
         BTW VISIBLE SMOOSH "Turn: " blep MKAY
         GTFO
      OMG "0"
      OMG "1"
      OMG "2"
      OMG "3"
      OMG "4"
      OMG "5"
      OMG "6"
      OMG "7"
      OMG "8"
      OMG "9"
          distance R SMOOSH distance blep MKAY
          GTFO
      OMG ","
          MAEK distance A NUMBR
          VISIBLE SMOOSH "Turn=" turn ", Distance=" distance MKAY

          OBTW
              The comma is the trigger for resolving a move. It's gotta all happen here. If you
              do it in a function, the function won't see any scope but itself.
              LOLCODE has no global scope. You don't know how troubling that truly is until you
              try to work with it.
          TLDR

          BTW Select the adjustment. Keep the old one so I've got a hope to debug this monster.
          I HAS A newDirection
          newDirection R I IZ turnin YR turn AND YR direction MKAY
          direction R newDirection

          BTW Calculate these for later adjustment of the location.
          I HAS A northMove ITZ I IZ northAdjustin YR direction AN YR distance MKAY
          I HAS A eastMove ITZ I IZ eastAdjustin YR direction AN YR distance MKAY

          BTW Apply the translations to the location
          northSpot R SUM OF northSpot AN northMove
          eastSpot R SUM OF eastSpot AN eastMove

          VISIBLE SMOOSH "Location: North=" northSpot " East=" eastSpot MKAY

          BTW Reset stuff
          turn R ""
          distance R ""
          GTFO
      OMGWTF
         BTW Who cares?
    OIC

IM OUTTA YR inputsnomnom

VISIBLE SMOOSH "Location: North=" northSpot " East=" eastSpot MKAY

I HAS A northDistance ITZ I IZ denegatifying YR northSpot MKAY
I HAS A eastDistance ITZ I IZ denegatifying YR eastSpot MKAY

I HAS A taxiDistance ITZ SUM OF northDistance AN eastDistance
VISIBLE SMOOSH "Best Distance: " taxiDistance MKAY

VISIBLE "Done"
KTHXBYE
