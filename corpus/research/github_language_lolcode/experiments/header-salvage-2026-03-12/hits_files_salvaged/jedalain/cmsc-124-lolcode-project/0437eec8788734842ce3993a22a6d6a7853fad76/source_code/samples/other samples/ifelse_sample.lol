HAI 1.3
    WAZZUP
        I HAS A choice
        I HAS A input
    BUHBYE


    BOTH SAEM choice AN 1
    O RLY?
        YA RLY
            VISIBLE "Enter birth year: "
            VISIBLE DIFF OF 2022 AN input

        MEBBE BOTH SAEM choice AN 2
            VISIBLE "Enter bill cost: "
            VISIBLE "Tip: " + PRODUKT OF input AN 0.1

        MEBBE BOTH SAEM choice AN 3
            VISIBLE "Enter width: "
            VISIBLE "Square Area: " + PRODUKT OF input AN input
            
        MEBBE BOTH SAEM choice AN 0
            VISIBLE "Goodbye"


        NO WAI
            VISIBLE "Invalid Input!"
    OIC


    DIFFRINT BIGGR OF 3 AN choice AN 3
    O RLY?
        YA RLY
            VISIBLE "Invalid input is > 3."
    OIC


KTHXBYE