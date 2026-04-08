HOW IZ I printName YR person
    VISIBLE "Hello, " + person
    GTFO
IF U SAY SO

HOW IZ I addNum YR x AN YR y
    I IZ printName YR x MKAY
    FOUND YR SUM OF x AN y
IF U SAY SO

HAI
    WAZZUP
    I HAS A num1 ITZ 1
    I HAS A num2 ITZ 3
    I HAS A num3 ITZ 3
    I HAS A choice
    I HAS A input
    I HAS A float1 ITZ 1.25
        BTW special characters in YARN is possible
    I HAS A name ITZ ":>,: hello world"
    BUHBYE



    BTW '!' suppress the newline after a line of output
    VISIBLE "test '!' " !
    VISIBLE name



    BTW Loop nesting
    IM IN YR asc UPPIN YR num1 TIL BOTH SAEM num1 AN num2
        VISIBLE "hi" + num1

        IM IN YR desc NERFIN YR num3 TIL BOTH SAEM num3 AN 0
            VISIBLE "test" + num3
        IM OUTTA YR desc
	IM OUTTA YR asc



    BTW MEBBE 
    VISIBLE "Choice: "
	GIMMEH choice

    BTW convert choice to numerical value
    choice IS NOW A NUMBAR

    BOTH SAEM choice AN 1
	O RLY?
		YA RLY
			VISIBLE "Enter birth year: "
			GIMMEH input
			VISIBLE DIFF OF 2022 AN input

	BTW uncomment this portion if you have MEBBE
	BTW else, this portion should be ignored

		MEBBE BOTH SAEM choice AN 2
			VISIBLE "Enter bill cost: "
			GIMMEH input
			VISIBLE "Tip: " + PRODUKT OF input AN 0.1
		MEBBE BOTH SAEM choice AN 3
			VISIBLE "Enter width: "
			GIMMEH input
			VISIBLE "Square Area: " + PRODUKT OF input AN input
		MEBBE BOTH SAEM choice AN 0
			VISIBLE "Goodbye"

		NO WAI
			VISIBLE "Invalid Input!"
	OIC



    BTW if-else nesting
    VISIBLE "Choice: "
	GIMMEH choice

    BTW convert choice to numerical value
    choice IS NOW A NUMBAR

    BOTH SAEM choice AN 1
    O RLY?
        YA RLY
            VISIBLE 1
            
            BOTH SAEM choice AN 1
            O RLY?
                YA RLY  
                    VISIBLE "Working Nested If-else"
                NO WAI
                    VISIBLE "Hehe"
            OIC
            
        NO WAI
            VISIBLE "Haha"
    OIC



    BTW switch-nesting
    VISIBLE "Choice: "
	GIMMEH choice

    BTW convert choice to numerical value
    choice IS NOW A NUMBAR

    BTW 'WTF?' uses the implicit value of IT
	choice  
	WTF?
		OMG 1
			VISIBLE "Enter number: "
			GIMMEH input
			
            BTW convert to numerical value
            input IS NOW A NUMBAR

            WTF?
                OMG 1
                    VISIBLE "Working nested switch"
                    GTFO
                OMG 2 
                    VISIBLE "Hehe"
                    GTFO
                OMG 0
                    VISIBLE "Goodbye"
                OMGWTF
                    VISIBLE "Invalid Input!"
            OIC
			GTFO
		OMG 2
			VISIBLE "Hehe"
			GTFO
		OMG 0
			VISIBLE "Goodbye"
		OMGWTF
			VISIBLE "Invalid Input!"
	OIC



    BTW switch and if-else nesting
    VISIBLE "Choice: "
	GIMMEH choice

    BTW convert choice to numerical value
    choice IS NOW A NUMBAR

    BTW 'WTF?' uses the implicit value of IT
	choice  
	WTF?
		OMG 1
			BOTH SAEM choice AN 1
            O RLY?
                YA RLY  
                    VISIBLE "Working Nested switch if-else"
                NO WAI
                    VISIBLE "Hehe"
            OIC
			GTFO
		OMG 2
			VISIBLE "Hehe"
			GTFO
		OMG 0
			VISIBLE "Goodbye"
		OMGWTF
			VISIBLE "Invalid Input!"
	OIC



    BTW if-else and switch nesting
    VISIBLE "Choice: "
	GIMMEH choice

    BTW convert choice to numerical value
    choice IS NOW A NUMBAR

    BOTH SAEM choice AN 1
    O RLY?
        YA RLY
            choice  
            WTF?
                OMG 1
                    VISIBLE "Working nested if-else switch"
                    GTFO
                OMG 2
                    VISIBLE "Hehe"
                    GTFO
                OMG 0
                    VISIBLE "Goodbye"
                OMGWTF
                    VISIBLE "Invalid Input!"
            OIC
        NO WAI
            VISIBLE "Haha"
    OIC



    BTW function nesting, function defined at start
    I IZ addNum YR num1 AN YR num2 MKAY

KTHXBYE












