HAI
	WAZZUP
		I HAS A choice
		I HAS A numA
		I HAS A numB
	BUHBYE
	
	BTW if w/o MEBBE, 1 only, everything else is invalid
	VISIBLE "1. Divide"
	VISIBLE "2. Multiply"
	VISIBLE "0. Exit"

	VISIBLE "Choice: "
	GIMMEH choice

	WTF?
		OMG 1
			VISIBLE "Enter numA: "
			GIMMEH numA
			
            VISIBLE "Enter numB: "
			GIMMEH numB

            DIFFRINT numB AN 0
            O RLY?
                YA RLY
                    VISIBLE "Quotient: " + QUOSHUNT OF numA AN numB
                MEBBE BOTH SAEM numB AN 0
                    VISIBLE "Division by ZERO is not allowed!"
                NO WAI
                    VISIBLE "Invalid Input!"
            OIC

            GTFO
		OMG 2
            VISIBLE "Enter numA: "
			GIMMEH numA
			
            VISIBLE "Enter numB: "
			GIMMEH numB

			VISIBLE "Product: " + PRODUKT OF numA AN numB
			GTFO
		OMG 0
			VISIBLE "Goodbye"
			GTFO
		OMGWTF
			VISIBLE "Invalid Input!"
	OIC

KTHXBYE