if (:BattPow/:MaxBattPow)==1 then goto 3 end
if :active<30 and :need==0 then :GeneratorUnitRateLimit=25 end
if :idle>30 and :lckd==0 then :GeneratorUnitRateLimit=1 end goto 1
