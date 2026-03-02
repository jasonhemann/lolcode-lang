HAI
	HOW IZ I addNum YR X AN YR Y
		FOUND YR SUM OF X AN Y
	IF U SAY SO

	HOW IZ I diffNum YR X AN YR Y
		FOUND YR DIFF OF X AN Y
	IF U SAY SO

	HOW IZ I mulNum YR X AN YR Y
		FOUND YR PRODUKT OF X AN Y
	IF U SAY SO

	HOW IZ I divNum YR X AN YR Y
		FOUND YR QUOSHUNT OF X AN Y
	IF U SAY SO

	HOW IZ I powNum YR X AN YR Y
		IM IN YR getPow NERFIN YR Y WILE DIFFRINT Y AN SMALLR OF Y AN 1
			X R PRODUKT OF X AN num1
		IM OUTTA YR getPow

		FOUND YR X
	IF U SAY SO

	I HAS A var1 ITZ 1
	I HAS A num1 
	I HAS A num2
	I HAS A choice

	VISIBLE "=========== MENU ==========="
	VISIBLE "    [1] Addition "
	VISIBLE "    [2] Subtraction "	
	VISIBLE "    [3] Multiplication "
	VISIBLE "    [4] Division "	
	VISIBLE "    [5] Power "
	VISIBLE "    [0] Exit "

        IM IN YR printMenu UPPIN YR var1 

		GIMMEH choice
		choice IS NOW A NUMBR

		DIFFRINT choice AN 0
		O RLY?
			YA RLY
				GIMMEH num1
				GIMMEH num2
				num1 IS NOW A NUMBR
				num2 IS NOW A NUMBR
				
				MAEK choice NUMBR
				WTF? 
				OMG 1
					VISIBLE "> Addition" 
					VISIBLE I IZ addNum YR num1 AN YR num2 MKAY
					GTFO
				OMG 2
					VISIBLE "> Subtraction" 
					VISIBLE I IZ diffNum YR num1 AN YR num2 MKAY
					GTFO
				OMG 3
					VISIBLE "> Multiplication" 
					VISIBLE I IZ mulNum YR num1 AN YR num2 MKAY
					GTFO
				OMG 4
					VISIBLE "> Division" 
					VISIBLE I IZ divNum YR num1 AN YR num2 MKAY
					GTFO
				OMG 5
					VISIBLE "> Power" 
					VISIBLE I IZ powNum YR num1 AN YR num2 MKAY
					GTFO
				OMGWTF
					VISIBLE "Invalid Input!"
				OIC

			NO WAI
				GTFO
		OIC

	IM OUTTA YR printMenu
KTHXBYE
