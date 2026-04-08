HAI
	WAZZUP
		I HAS A numA
		I HAS A numB
		I HAS A numC
	BUHBYE
	
	VISIBLE "Gimmeh a number: "
	GIMMEH numA

	numB R 0
	numC R 0

	IM IN YR asc UPPIN YR numB WILE SMALLR OF numB AN numA
		VISIBLE numB
		
		BTW print "yellow" numA - 1 times for every numB
		IM IN YR dsc UPPIN YR numC WILE SMALLR OF numC AN DIFF OF numA AN 1
			VISIBLE "yellow"
		IM OUTTA YR dsc
		
		numC R 0	BTW reset numC
	IM OUTTA YR asc

	VISIBLE "***"
KTHXBYE