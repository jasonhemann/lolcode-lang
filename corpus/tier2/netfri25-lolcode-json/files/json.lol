O HAI IM Value
    I HAS A kind ITZ A NUMBR BTW kind is the ID of the type

    BTW possible kinds
    I HAS A null   ITZ 1
    I HAS A bool   ITZ 2
    I HAS A num    ITZ 3
    I HAS A string ITZ 4
    I HAS A array  ITZ 5
    I HAS A object ITZ 6
    I HAS A to_string ITZ A FUNKSHUN
KTHX

O HAI IM Null IM LIEK Value
    I HAS A kind ITZ Value'Z null

    HOW IZ I to_string
        FOUND YR "null"
    IF U SAY SO
KTHX

O HAI IM Bool IM LIEK Value
    I HAS A kind ITZ Value'Z bool
    I HAS A value ITZ A TROOF

    HOW IZ I to_string
        ME'Z value, O RLY?
            YA RLY
                FOUND YR "true"
            NO WAI
                FOUND YR "false"
        OIC
    IF U SAY SO
KTHX

O HAI IM Number IM LIEK Value
    I HAS A kind ITZ Value'Z num
    I HAS A value ITZ A NUMBAR

    HOW IZ I to_string
        FOUND YR MAEK ME'Z value A YARN
    IF U SAY SO
KTHX

O HAI IM String IM LIEK Value
    I HAS A kind ITZ Value'Z string
    I HAS A value ITZ A YARN

    HOW IZ I to_string
        FOUND YR SMOOSH ":"" AN ME'Z value AN ":"" MKAY
    IF U SAY SO
KTHX

O HAI IM Array IM LIEK Value
    I HAS A kind ITZ Value'Z array

    I HAS A len   ITZ A NUMBR  BTW length of items
    I HAS A items ITZ A BUKKIT BTW index => item

    HOW IZ I push YR item
        ME'Z items HAS A SRS ME'Z len ITZ item
        ME'Z len R SUM OF ME'Z len AN 1
    IF U SAY SO

    HOW IZ I to_string
        BOTH SAEM ME'Z len AN 0, O RLY?, YA RLY, FOUND YR "[]", OIC
        I HAS A output ITZ "["

        IM IN YR loop UPPIN YR index TIL BOTH SAEM index AN ME'Z len
            DIFFRINT index AN 0, O RLY?
                YA RLY
                    output R SMOOSH output AN ", " MKAY
            OIC

            I HAS A item ITZ ME'Z items'Z SRS index
            I HAS A item_string ITZ item IZ to_string MKAY
            output R SMOOSH output AN item_string MKAY
        IM OUTTA YR loop

        output R SMOOSH output AN "]" MKAY
        FOUND YR output
    IF U SAY SO
KTHX

O HAI IM Object IM LIEK Value
    I HAS A kind ITZ Value'Z object

    I HAS A len   ITZ A NUMBR   BTW length of keys
    I HAS A keys  ITZ A BUKKIT  BTW index => key
    I HAS A items ITZ A BUKKIT  BTW key => item

    HOW IZ I push YR key AN YR value
        ME'Z keys HAS A SRS ME'Z len ITZ key
        ME'Z items HAS A SRS key ITZ value
        ME'Z len R SUM OF ME'Z len AN 1
    IF U SAY SO

    HOW IZ I to_string
        BOTH SAEM ME'Z len AN 0, O RLY?, YA RLY, FOUND YR "{}", OIC
        I HAS A output ITZ "{"

        IM IN YR loop UPPIN YR index TIL BOTH SAEM index AN ME'Z len
            DIFFRINT index AN 0, O RLY?
                YA RLY
                    output R SMOOSH output AN ", " MKAY
            OIC

            I HAS A key ITZ ME'Z keys'Z SRS index
            I HAS A item ITZ ME'Z items'Z SRS key
            I HAS A item_string ITZ item IZ to_string MKAY
            output R SMOOSH output AN ":"" AN key AN ":":: " AN item_string MKAY
        IM OUTTA YR loop

        output R SMOOSH output AN "}" MKAY
        FOUND YR output
    IF U SAY SO
KTHX
