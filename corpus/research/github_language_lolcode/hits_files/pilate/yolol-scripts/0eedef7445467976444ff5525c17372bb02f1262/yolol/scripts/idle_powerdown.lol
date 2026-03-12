if (:Battery_1/:MaxBatteryPower)==1 then goto 3 end
if :active<60 then :GeneratorUnitRateLimit=50 end
if :idle>60 then :GeneratorUnitRateLimit=1 end goto 1

// Power down when idle for too long while