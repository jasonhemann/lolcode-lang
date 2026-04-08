HAI 1.2
    I HAS A N ITZ 100
    I HAS A array ITZ A BUKKIT
    IM IN YR loop UPPIN YR index TIL BOTH SAEM index AN N
        array HAS A SRS index ITZ WIN
    IM OUTTA YR loop
    array'Z SRS 0 R FAIL
    array'Z SRS 1 R FAIL

    VISIBLE "READY TO SURCH 4 YR PRIMES"

    IM IN YR loop UPPIN YR step TIL BOTH SAEM step AN N
        array'Z SRS step
        O RLY?
            YA RLY
                VISIBLE step " IZ PRIME"

                I HAS A cumpound ITZ PRODUKT OF step AN step
                IM IN YR inner_loop
                    BOTH SAEM cumpound AN BIGGR OF cumpound AN N
                    O RLY?
                        YA RLY
                            ENUF
                    OIC
                    array'Z SRS cumpound R FAIL
                    cumpound R SUM OF cumpound AN step
                IM OUTTA YR inner_loop
        OIC
    IM OUTTA YR loop

    VISIBLE "FOUND ALL YR PRIMES SMALLR THAN " N
KTHXBYE
