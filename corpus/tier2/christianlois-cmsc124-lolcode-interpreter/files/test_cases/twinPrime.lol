OBTW
	prints twin
	prime numbers
	from 2 to N
TLDR

HAI
	I HAS A n
	I HAS A i
	I HAS A isPrime
	I HAS A temp ITZ 3
	I HAS A temp1 ITZ temp
	
	VISIBLE "n: "
	GIMMEH n
	
	IM IN YR printPrime UPPIN YR temp WILE BOTH SAEM temp AN SMALLR OF temp AN n
		i R 2
		isPrime R WIN
		IM IN YR checkPrime UPPIN YR i
			BOTH SAEM 0 AN MOD OF temp AN i
			O RLY?
			YA RLY
				isPrime R FAIL
				GTFO
			MEBBE BOTH SAEM SUM OF i AN 1 AN temp
				GTFO
			OIC
		IM OUTTA YR checkPrime

		isPrime
		WTF?
		OMG WIN
			BOTH SAEM 2 AN DIFF OF temp AN temp1
			O RLY?
			YA RLY
				VISIBLE temp1 " " temp
			OIC
			temp1 R temp
		OIC
	IM OUTTA YR printPrime
KTHXBYE
