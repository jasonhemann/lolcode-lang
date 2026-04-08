HAI
    WAZZUP
    I HAS A var1 ITZ SUM OF 12 AN 4
    I HAS A var2 ITZ QUOSHUNT OF SUM OF PRODUKT OF 4 AN 9 AN SUM OF 3 AN 9 AN SMALLR OF 6 AN var1
    I HAS A var3 ITZ SUM OF var1 AN 4
    I HAS A bool1 ITZ BOTH OF WIN AN FAIL
    I HAS A bool2 ITZ EITHER OF WIN AN 2
    I HAS A bool3 ITZ WON OF WIN AN FAIL
    I HAS A bool4 ITZ NOT WIN
    I HAS A bool5 ITZ ALL OF NOT WIN AN WON OF FAIL AN FAIL MKAY
    I HAS A bool6 ITZ ANY OF NOT WIN AN BOTH OF WIN AN WIN MKAY
    I HAS A bool7 ITZ BOTH SAEM 2 AN 5
    I HAS A bool8 ITZ DIFFRINT 2 AN 4
    I HAS A str1 ITZ "String 1"
    I HAS A str2 ITZ SMOOSH "OKAY" AN "YUPS"
    I HAS A choice ITZ 5
    I HAS A input ITZ 2001
    BUHBYE
    QUOSHUNT OF 1 AN 2
    VISIBLE var1
    2
    WTF?
    OMG 3
        VISIBLE "VALID"
        VISIBLE "VALID"
        VISIBLE "VALID"
    OMG 5
        VISIBLE "VALID_AGAIN"
        VISIBLE "VALID_AGAIN"
        VISIBLE "VALID_AGAIN"
    OMGWTF
        VISIBLE "DEFAULT"
        VISIBLE "DEFAULT"
        VISIBLE "DEFAULT"
    OIC

	choice
	WTF?
		OMG 1
			VISIBLE "Enter birth year: "
			VISIBLE DIFF OF 2022 AN input
		OMG 2
			VISIBLE "Enter bill cost: "
			VISIBLE "Tip: " + PRODUKT OF input AN 0.1
		OMG 3
			VISIBLE "Enter width: "
			VISIBLE "Square Area: " + PRODUKT OF input AN input
		OMG 0
			VISIBLE "Goodbye"
		OMGWTF
			VISIBLE "Invalid Input!"
	OIC

    FAIL
    O RLY?
        YA RLY
            VISIBLE "IF_STATEMENT"
            VISIBLE "IF_STATEMENT"
        NO WAI
            VISIBLE "ELSE_STATEMENT"
            VISIBLE "ELSE_STATEMENT"
    OIC

    DIFFRINT BIGGR OF 3 AN choice AN 3
	O RLY?
		YA RLY
			VISIBLE ">>>>>>> 3."
	OIC
    
KTHXBYE