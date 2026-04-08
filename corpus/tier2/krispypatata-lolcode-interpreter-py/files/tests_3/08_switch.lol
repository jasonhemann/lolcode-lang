HAI
	WAZZUP
		I HAS A choice
		I HAS A input
	BUHBYE
	
	BTW if w/o MEBBE, 1 only, everything else is invalid
	VISIBLE "1. Compute age"
	VISIBLE "2. Compute tip"
	VISIBLE "3. Compute square area"
	VISIBLE "0. Exit"

	VISIBLE "Choice: "
	choice R 4
	VISIBLE choice
	VISIBLE "─────────────────────────────────────────────────"

	choice
	WTF?
		OMG 1
			VISIBLE "Enter birth year: "
			input R 2
			VISIBLE input
			VISIBLE DIFF OF 2022 AN input
			GTFO
		OMG 2
			VISIBLE "Enter bill cost: "
			input R 2
			VISIBLE input
			VISIBLE "Tip: " AN PRODUKT OF input AN 0.1
			GTFO
		OMG 3
			VISIBLE "Enter width: "
			input R 2
			VISIBLE input
			VISIBLE "Square Area: " + PRODUKT OF input AN input
			GTFO
		OMG 0
			VISIBLE "Goodbye"
		OMGWTF
			VISIBLE "Invalid Input!"
	OIC

KTHXBYE