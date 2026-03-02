BTW if block within loop block
HAI

	I HAS A result ITZ 0
	I HAS A input
	I HAS A counter ITZ 0

	VISIBLE "===Continuous Addition==="
	VISIBLE "Initial value is 0."

	IM IN YR loop UPPIN YR counter
		VISIBLE ""
		VISIBLE SUM OF counter AN 1 ">Add what to [" result "]?"
		GIMMEH input
		result R SUM OF input AN result
		VISIBLE "New sum: " result

		VISIBLE ""
		VISIBLE "End operation? (Enter 1 to confirm)"
		GIMMEH input
		
		BOTH SAEM input AN "1"
		O RLY?
			YA RLY
				GTFO
		OIC

	IM OUTTA YR loop

	VISIBLE "END"

KTHXBYE
