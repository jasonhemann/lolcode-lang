HAI

	I HAS A choice
	I HAS A input

	BTW if w/o MEBBE, 1 only, everything else is invalid
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
		OMGWTF
			VISIBLE "Invalid Input!"
	OIC

KTHXBYE

OBTW
	Changes from original file:
		Line 25 - PRODUCKT to PRODUKT
		Line 30 - PRODUCKT to PRODUKT
		Lines 17, 22, 27, 32 - From NUMBRs to YARNs (Alternative: Convert choice to NUMBR)
TLDR