HAI
	I HAS A curNum ITZ 2
	I HAS A counter ITZ 0
	I HAS A temp ITZ 0
	I HAS A isPrime ITZ WIN


	I HAS A n 
	GIMMEH n
	n IS NOW A NUMBR

	IM IN YR printPrime UPPIN YR curNum TIL BOTH SAEM counter AN n
		temp R 2

		IM IN YR checkPrime UPPIN YR temp WILE DIFFRINT temp AN BIGGR OF temp AN curNum
			BOTH SAEM MOD OF curNum AN temp AN 0
			O RLY?
				YA RLY
					isPrime R FAIL
					GTFO
			OIC
		IM OUTTA YR checkPrime

		BOTH SAEM isPrime AN WIN
		O RLY?
			YA RLY
				VISIBLE curNum " " !
				counter R SUM OF counter AN 1
			NO WAI
				isPrime R WIN
		OIC
		

	IM OUTTA YR printPrime

KTHXBYE
