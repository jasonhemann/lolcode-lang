HAI
	WAZZUP
		I HAS A choice
		I HAS A input
	BUHBYE

	BTW if w/o MEBBE, 1 only, everything else is invalid
	VISIBLE "1. Compute something"
	VISIBLE "0. Exit"

	VISIBLE "Choice: "
	GIMMEH choice

	BOTH SAEM choice AN 1
	O RLY?
		YA RLY
			VISIBLE "1. Compute tip"
			VISIBLE "2. Compute square area"
			VISIBLE "Enter num: "
			GIMMEH choice
			choice
			WTF?
				OMG 1
					VISIBLE "Enter bill cost: "
					GIMMEH input
					VISIBLE "Tip: " + PRODUKT OF input AN 0.1
					GTFO
				OMG 2
					VISIBLE "Enter width: "
					GIMMEH input
					VISIBLE "Square Area: " + PRODUKT OF input AN input
					GTFO
				OMG 0
					VISIBLE "Goodbye"
				OMGWTF
					VISIBLE "Invalid Input!"
			OIC
		NO WAI
			VISIBLE "Invalid Input!"

	OIC

KTHXBYE