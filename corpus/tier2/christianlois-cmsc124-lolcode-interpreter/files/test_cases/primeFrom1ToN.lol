HAI	1.2		BTW prime from 2 to N
	I HAS A n
	I HAS A i
	I HAS A j
	I HAS A isPrime

	VISIBLE "n: "
	GIMMEH n
	n IS NOW A NUMBR
	
	i R 2
	
	IM IN YR printPrime UPPIN YR i WILE BOTH SAEM i AN SMALLR OF i AN n
		j R 2
		isPrime R WIN
		IM IN YR checkPrime UPPIN YR j WILE DIFFRINT j AN BIGGR OF j AN i
			BOTH SAEM MOD OF i AN j AN 0
			O RLY?
			YA RLY
				isPrime R FAIL
				GTFO
			OIC
		IM OUTTA YR checkPrime
		IT R isPrime
		O RLY?
		YA RLY
			VISIBLE i
		OIC
	IM OUTTA YR printPrime	

KTHXBYE



