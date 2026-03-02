HAI BTW switch and if blocks within loop block

	I HAS A choice
	I HAS A input
	I HAS A var ITZ 0
	I HAS A exit

	IM IN YR loop1 UPPIN YR var
	VISIBLE "1. Compute age"
	VISIBLE "2. Compute tip"
	VISIBLE "3. Compute square area"
	VISIBLE "0. Exit"

	VISIBLE "Choice: "
	GIMMEH choice

	choice
	WTF?
		OMG "1"
			VISIBLE "Enter birth year: "
			GIMMEH input
			VISIBLE DIFF OF 2022 AN input
			GTFO
		OMG "2"
			VISIBLE "Enter bill cost: "
			GIMMEH input
			VISIBLE "Tip: " PRODUKT OF input AN 0.1
			GTFO
		OMG "3"
			VISIBLE "Enter width: "
			GIMMEH input
			VISIBLE "Square Area: " PRODUKT OF input AN input
			GTFO
		OMG "0"
			VISIBLE "Goodbye"
			exit R WIN
		OMGWTF
			VISIBLE "Invalid Input!"
	OIC

	BOTH OF WIN AN exit
	O RLY?
		YA RLY
			GTFO
	OIC

	IM OUTTA YR loop1

KTHXBYE