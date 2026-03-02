HAI
	HOW IZ I factNum YR X
		BOTH SAEM X AN 0
		O RLY?
			YA RLY
				FOUND YR 1
			NO WAI
				BTW return X * factNum(X-1)
				FOUND YR PRODUKT OF X AN I IZ factNum YR DIFF OF X AN 1 MKAY
		OIC
	IF U SAY SO

	HOW IZ I getPascalNum YR row AN YR N
		BTW row! / (N! * (row - N)!)
		FOUND YR QUOSHUNT OF I IZ factNum YR row MKAY AN PRODUKT OF I IZ factNum YR N MKAY AN I IZ factNum YR DIFF OF row AN N MKAY
	IF U SAY SO

	I HAS A var1 
	I HAS A rowCounter ITZ 0
	I HAS A colCounter ITZ 0
	
	GIMMEH var1
	var1 IS NOW A NUMBR

	IM IN YR printPyramid UPPIN YR rowCounter TIL BOTH SAEM rowCounter AN var1

		colCounter R 0

		IM IN YR printCol UPPIN YR colCounter TIL DIFFRINT colCounter AN SMALLR OF colCounter AN rowCounter
			VISIBLE I IZ getPascalNum YR rowCounter AN YR colCounter MKAY " " !
		IM OUTTA YR printCol

		VISIBLE ""

	IM OUTTA YR printPyramid

KTHXBYE
