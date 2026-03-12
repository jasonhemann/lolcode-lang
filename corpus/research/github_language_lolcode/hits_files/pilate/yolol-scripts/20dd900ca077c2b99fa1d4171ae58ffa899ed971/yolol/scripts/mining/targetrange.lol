if (:r1 > 50) or (:r1 < 5) then goto 3 end
:mineranglel=-90+:angle1 :minerangler=90-:angle1 goto 1
:mineranglel=0 :minerangler=0 goto 1

// Point left and right mining lasers at rangefinder target
// :r1 = rangefinder distance
// :mineranglel = left laser rotation
// :minerangler = right laser rotation