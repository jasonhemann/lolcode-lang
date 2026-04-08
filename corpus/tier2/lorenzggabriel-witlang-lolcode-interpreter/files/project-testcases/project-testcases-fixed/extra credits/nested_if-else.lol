HAI
	WAZZUP
		I HAS A choice
		I HAS A input
	BUHBYE

	BTW if w/o MEBBE, 1 only, everything else is invalid
	VISIBLE "1. Compute age"

	VISIBLE "Choice: "
	GIMMEH choice

	BOTH SAEM choice AN 1
	O RLY?
		YA RLY
			VISIBLE "Enter birth year: "
			GIMMEH input
			VISIBLE "Age: " + DIFF OF 2024 AN input
                        BOTH SAEM DIFF OF 2024 AN input AN BIGGR OF DIFF OF 2024 AN input AN 18
	                O RLY?
                            YA RLY
                                VISIBLE "You can vote! Choose wisely."

                            NO WAI
                                VISIBLE "You are still not allowed to vote."
                        OIC                           
		NO WAI
			VISIBLE "Invalid Input!"
	OIC

KTHXBYE



