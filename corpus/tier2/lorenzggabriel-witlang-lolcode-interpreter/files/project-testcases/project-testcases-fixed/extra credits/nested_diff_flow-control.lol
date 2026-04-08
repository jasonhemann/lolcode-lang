HAI
	WAZZUP
		I HAS A choice
		I HAS A input
                I HAS A yearlevel
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
                                VISIBLE "Enter year level (1, 2, 3, or 4): "
                                GIMMEH yearlevel
                                    yearlevel
                                    WTF?
                                        OMG 1
                                            VISIBLE "Freshman!"
                                        GTFO

                                        OMG 2
                                            VISIBLE "Sophomore!"
                                        GTFO

                                        OMG 3
                                            VISIBLE "Junior!"
                                        GTFO

                                        OMG 4
                                            VISIBLE "Senior!"
                                        GTFO

                                        OMGWTF
                                            VISIBLE "Invalid year level."
                                    OIC

                            NO WAI
                                VISIBLE "You are still not allowed to vote."
                        OIC                           
		NO WAI
			VISIBLE "Invalid Input!"
	OIC

KTHXBYE



