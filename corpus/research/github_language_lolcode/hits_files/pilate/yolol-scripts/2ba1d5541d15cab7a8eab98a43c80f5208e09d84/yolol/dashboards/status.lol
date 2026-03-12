new="\n\nBatt: "+((:storedbatterypower/:maxbatterypower)*100)+"%"
new+="\nFuel: "+((:storedrawfuel/:maxrawfuel)*100)+"%"
prop_pct=(:GasNetworkStoredResource/:GasNetworkMaxResource)*100
new+="\nProp: "+prop_pct+"%"
:status = new goto 1