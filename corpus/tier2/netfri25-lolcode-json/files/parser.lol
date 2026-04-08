HAI 1.4

CAN HAS JSON?

CAN HAS STRING?

HOW IZ I parse YR input
    I HAS A parser ITZ LIEK A Parser
    parser HAS A input ITZ input
    parser IZ parse_value MKAY
IF U SAY SO

O HAI IM Parser
    I HAS A input ITZ A YARN

    BTW  parse : -> NOOB | JSON'Z Value
    HOW IZ I parse_value
        ME'Z input R I IZ trim_start YR ME'Z input MKAY
        ME IZ parse_null   MKAY, O RLY?, YA RLY, FOUND YR IT, OIC
        ME IZ parse_bool   MKAY, O RLY?, YA RLY, FOUND YR IT, OIC
        ME IZ parse_num    MKAY, O RLY?, YA RLY, FOUND YR IT, OIC
        ME IZ parse_string MKAY, O RLY?, YA RLY, FOUND YR IT, OIC
        ME IZ parse_array  MKAY, O RLY?, YA RLY, FOUND YR IT, OIC
        ME IZ parse_object MKAY, O RLY?, YA RLY, FOUND YR IT, OIC
    IF U SAY SO

    HOW IZ I consume YR count
        ME'Z input R STRING IZ SLICE YR ME'Z input AN YR count AN YR STRING IZ LEN YR ME'Z input MKAY MKAY
    IF U SAY SO

    HOW IZ I parse_null
        I IZ starts_with YR ME'Z input AN YR "null" MKAY, O RLY?
            YA RLY
                I IZ consume YR 4 MKAY
                FOUND YR JSON'Z Null
            NO WAI
                FOUND YR NOOB
        OIC
    IF U SAY SO

    HOW IZ I parse_bool
        I HAS A result ITZ LIEK A JSON'Z Bool
        I IZ starts_with YR ME'Z input AN YR "true" MKAY, O RLY?
            YA RLY
                ME IZ consume YR 4 MKAY
                result HAS A value ITZ WIN
                FOUND YR result
            MEBBE I IZ starts_with YR ME'Z input AN YR "false" MKAY
                ME IZ consume YR 5 MKAY
                result HAS A value ITZ FAIL
                FOUND YR result
            NO WAI
                FOUND YR NOOB
        OIC
    IF U SAY SO

    BTW TODO: add support for non-integer literals
    HOW IZ I parse_num
        I HAS A count ITZ 0
        IM IN YR loop
            I HAS A cond ITZ I IZ is_digit YR STRING IZ AT YR ME'Z input AN YR count MKAY MKAY
            NOT cond, O RLY?, YA RLY, GTFO, OIC
            count R SUM OF count AN 1
        IM OUTTA YR loop
        BOTH SAEM count AN 0, O RLY?, YA RLY, GTFO, OIC

        I HAS A text ITZ STRING IZ SLICE YR ME'Z input AN YR 0 AN YR count MKAY
        ME IZ consume YR count MKAY
        I HAS A result ITZ LIEK A JSON'Z Number
        result HAS A value ITZ MAEK text A NUMBAR
        FOUND YR result
    IF U SAY SO

    HOW IZ I parse_string
        NOT I IZ starts_with YR ME'Z input AN YR ":"" MKAY, O RLY?, YA RLY, GTFO, OIC
        I HAS A count ITZ 1
        BTW while (count < self.input.len() && self.input[count] != '"')
        IM IN YR loop
            I HAS A cond ITZ BOTH OF DIFFRINT count AN BIGGR OF count AN STRING IZ LEN YR ME'Z input MKAY AN DIFFRINT ":"" AN STRING IZ AT YR ME'Z input AN YR count MKAY
            NOT cond, O RLY?, YA RLY, GTFO, OIC
            BTW TODO: apply escaping
            count R SUM OF count AN 1
        IM OUTTA YR loop

        DIFFRINT ":"" AN STRING IZ AT YR ME'Z input AN YR count MKAY, O RLY?, YA RLY, GTFO, OIC
        I HAS A result ITZ LIEK A JSON'Z String
        result HAS A value ITZ STRING IZ SLICE YR ME'Z input AN YR 1 AN YR count MKAY
        count R SUM OF count AN 1
        ME IZ consume YR count MKAY
        FOUND YR result
    IF U SAY SO

    HOW IZ I parse_array
        NOT I IZ starts_with YR ME'Z input AN YR "[" MKAY, O RLY?, YA RLY, GTFO, OIC

        BTW saving the old input in case of a failure and there's a need to rewind
        I HAS A old_input ITZ ME'Z input
        ME IZ consume YR 1 MKAY

        O HAI IM result IM LIEK JSON'Z Array
            I HAS A len ITZ 0
            I HAS A items ITZ A BUKKIT
        KTHX

        ME'Z input R I IZ trim_start YR ME'Z input MKAY
        I IZ starts_with YR ME'Z input AN YR "]" MKAY, O RLY?
            YA RLY
                ME IZ consume YR 1 MKAY
                FOUND YR result
        OIC

        ME IZ parse_value MKAY, O RLY?
            YA RLY
                result IZ push YR IT MKAY
            NO WAI
                ME'Z input R old_input
                GTFO
        OIC

        ME'Z input R I IZ trim_start YR ME'Z input MKAY
        IM IN YR loop BTW TIL
            I HAS A cond ITZ I IZ starts_with YR ME'Z input AN YR "]" MKAY
            cond, O RLY?, YA RLY, GTFO, OIC
            NOT I IZ starts_with YR ME'Z input AN YR "," MKAY, O RLY?
                YA RLY
                    ME'Z input R old_input
                    FOUND YR NOOB
            OIC
            ME IZ consume YR 1 MKAY

            ME IZ parse_value MKAY, O RLY?
                YA RLY
                    result IZ push YR IT MKAY
                NO WAI
                    ME'Z input R old_input
                    FOUND YR NOOB
            OIC

            ME'Z input R I IZ trim_start YR ME'Z input MKAY
        IM OUTTA YR loop

        ME IZ consume YR 1 MKAY
        FOUND YR result
    IF U SAY SO

    HOW IZ I parse_object
        HOW IZ I parse_pair
            O HAI IM result
                I HAS A key ITZ A YARN
                I HAS A value ITZ LIEK A JSON'Z Value
            KTHX

            ME'Z input R I IZ trim_start YR ME'Z input MKAY
            I HAS A key ITZ ME IZ parse_string MKAY
            BOTH SAEM key AN NOOB, O RLY?, YA RLY, GTFO, OIC
            result'Z key R key'Z value

            ME'Z input R I IZ trim_start YR ME'Z input MKAY
            NOT I IZ starts_with YR ME'Z input AN YR "::" MKAY, O RLY?, YA RLY, GTFO, OIC
            ME IZ consume YR 1 MKAY

            ME'Z input R I IZ trim_start YR ME'Z input MKAY
            I HAS A value ITZ ME IZ parse_value MKAY
            BOTH SAEM value AN NOOB, O RLY?, YA RLY, GTFO, OIC
            result'Z value R value

            FOUND YR result
        IF U SAY SO

        NOT I IZ starts_with YR ME'Z input AN YR "{" MKAY, O RLY?, YA RLY, GTFO, OIC

        BTW saving the old input in case of a failure and there's a need to rewind
        I HAS A old_input ITZ ME'Z input
        ME IZ consume YR 1 MKAY

        O HAI IM result IM LIEK JSON'Z Object
            I HAS A len   ITZ A NUMBR   BTW length of keys
            I HAS A keys  ITZ A BUKKIT  BTW index => key
            I HAS A items ITZ A BUKKIT  BTW key => item
        KTHX

        ME'Z input R I IZ trim_start YR ME'Z input MKAY
        I IZ starts_with YR ME'Z input AN YR "}" MKAY, O RLY?
            YA RLY
                ME IZ consume YR 1 MKAY
                FOUND YR result
        OIC

        I IZ parse_pair MKAY, O RLY?
            YA RLY
                I HAS A pair ITZ IT
                result IZ push YR pair'Z key AN YR pair'Z value MKAY
            NO WAI
                ME'Z input R old_input
                GTFO
        OIC

        IM IN YR loop BTW TIL
            ME'Z input R I IZ trim_start YR ME'Z input MKAY
            I HAS A cond ITZ I IZ starts_with YR ME'Z input AN YR "}" MKAY
            cond, O RLY?, YA RLY, GTFO, OIC
            NOT I IZ starts_with YR ME'Z input AN YR "," MKAY, O RLY?
                YA RLY
                    ME'Z input R old_input
                    FOUND YR NOOB
            OIC
            ME IZ consume YR 1 MKAY

            I IZ parse_pair MKAY, O RLY?
                YA RLY
                    I HAS A pair ITZ IT
                    result IZ push YR pair'Z key AN YR pair'Z value MKAY
                NO WAI
                    ME'Z input R old_input
                    FOUND YR NOOB
            OIC
        IM OUTTA YR loop

        ME IZ consume YR 1 MKAY
        FOUND YR result
    IF U SAY SO
KTHX

HOW IZ I is_whitespace YR text
    FOUND YR ANY OF BOTH SAEM text AN " " AN BOTH SAEM text AN ":>" AN BOTH SAEM text AN ":)" MKAY
IF U SAY SO

HOW IZ I is_digit YR char
    BOTH SAEM SMALLR OF char AN "9" AN BIGGR OF char AN "0"
IF U SAY SO

HOW IZ I trim_start YR text
    I HAS A count ITZ 0
    IM IN YR loop
        I HAS A cond ITZ I IZ is_whitespace YR STRING IZ AT YR text AN YR count MKAY MKAY
        NOT cond, O RLY?, YA RLY, GTFO, OIC
        count R SUM OF count AN 1
    IM OUTTA YR loop
    FOUND YR STRING IZ SLICE YR text AN YR count AN YR STRING IZ LEN YR text MKAY MKAY
IF U SAY SO

HOW IZ I starts_with YR text AN YR prefix
    I HAS A len ITZ STRING IZ LEN YR prefix MKAY
    DIFFRINT len AN SMALLR OF len AN STRING IZ LEN YR text MKAY, O RLY?, YA RLY, FOUND YR FAIL, OIC
    IM IN YR loop UPPIN YR index TIL BOTH SAEM index AN len
        I HAS A c1 ITZ STRING IZ AT YR prefix AN YR index MKAY
        I HAS A c2 ITZ STRING IZ AT YR text   AN YR index MKAY
        DIFFRINT c1 AN c2, O RLY?, YA RLY, FOUND YR FAIL, OIC
    IM OUTTA YR loop
    FOUND YR WIN
IF U SAY SO

KTHXBYE
