HAI 1.2
    HOW IZ I get_left YR index
        BTW I HAS A base ITZ 18446744073709551616
        I HAS A base ITZ 1000
        I HAS A left ITZ 1
        IM IN YR loop NERFIN YR index WILE DIFFRINT index AN 0
            left R PRODUKT left AN base
        IM OUTTA YR loop
        FOUND YR left
    IF U SAY SO

    HOW IZ I store YR memory AN YR index AN YR val
        BTW I HAS A base ITZ 18446744073709551616
        I HAS A base ITZ 1000
        I HAS A left ITZ I IZ get_left YR index
        I HAS A right ITZ PRODUKT left AN base
        memory R SUM OF MOD OF memory AN left AN PRODUKT QUOSHUNT memory AN right AN right
        memory R SUM OF memory AN PRODUKT val AN left
        FOUND YR memory
    IF U SAY SO
    
    HOW IZ I load YR memory AN YR index
        BTW I HAS A base ITZ 18446744073709551616
        I HAS A base ITZ 1000
        I HAS A left ITZ I IZ get_left YR index
        FOUND YR MOD OF QUOSHUNT memory AN left AN base
    IF U SAY SO
    
    I HAS A PRIMES ITZ 0
    I HAS A PRIMES_LEN ITZ 0
    I HAS A TARGET
    VISIBLE "Enter positive number"
    GIMMEH TARGET
    TARGET IS NOW A NUMBR
    I HAS A CURRENT_PRIME ITZ 2
    IM IN YR LOOP UPPIN YR CURRENT_PRIME TIL BOTH SAEM PRIMES_LEN AN TARGET
        I HAS A IS_PRIME ITZ WIN
        I HAS A PRIME_INDEX ITZ 0
        IM IN YR LOOP UPPIN YR PRIME_INDEX TIL BOTH SAEM PRIME_INDEX PRIMES_LEN
            I HAS A PRIME ITZ I IZ load YR PRIMES AN YR PRIME_INDEX
            BOTH SAEM MOD OF CURRENT_PRIME AN PRIME AN 0, O RLY?
            YA RLY
                IS_PRIME R FAIL
            OIC
        IM OUTTA YR LOOP
        IS_PRIME, O RLY?
        YA RLY
            PRIMES R I IZ store YR PRIMES AN YR PRIMES_LEN AN YR CURRENT_PRIME
            UPPIN PRIMES_LEN
        OIC
    IM OUTTA YR LOOP
    VISIBLE "The first :{TARGET} primes are::"
    IM IN YR LOOP NERFIN YR PRIMES_LEN TIL BOTH SAEM PRIMES_LEN 0
        DIFFRINT TARGET AN PRIMES_LEN, O RLY?
        YA RLY
            NERFIN PRIMES_LEN
            VISIBLE " " I IZ load YR PRIMES AN YR PRIMES_LEN !
            UPPIN PRIMES_LEN
        NO WAI
            NERFIN PRIMES_LEN
            VISIBLE I IZ load YR PRIMES AN YR PRIMES_LEN !
            UPPIN PRIMES_LEN
        OIC
    IM OUTTA YR LOOP
    VISIBLE
KTHXBYE
