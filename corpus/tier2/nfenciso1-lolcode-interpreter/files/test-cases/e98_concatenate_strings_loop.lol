HAI

	I HAS A counter ITZ 0
	I HAS A numStrings
	I HAS A result ITZ ""
	I HAS A input

	VISIBLE "===Concatenate Strings==="
	VISIBLE ">How many strings to concatenate?"
	GIMMEH numStrings
	numStrings IS NOW A NUMBR
	VISIBLE ""

	IM IN YR loop UPPIN YR counter TIL BOTH SAEM counter AN numStrings
		VISIBLE SUM OF counter AN 1 ") Enter string: "
		GIMMEH input
		result R SMOOSH result AN input
	IM OUTTA YR loop

	VISIBLE ""
	VISIBLE "Result: "
	VISIBLE result

KTHXBYE