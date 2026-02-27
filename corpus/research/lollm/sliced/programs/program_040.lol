HAI 1.4
    CAN HAS STRING?

    VISIBLE "TYPE A MESSIJ 2 ENCRYPT:"
    I HAS A msg
    GIMMEH msg
    I HAS A len ITZ I IZ STRING'Z LEN YR msg MKAY
    I HAS A result ITZ ""
    I HAS A i ITZ 0
    IM IN YR loop UPPIN YR i TIL BOTH SAEM i AN len
        I HAS A ch ITZ I IZ STRING'Z AT YR msg AN YR i MKAY
        BTW Simple character shifting would go here
        result R SMOOSH result AN ch MKAY
    IM OUTTA YR loop
    VISIBLE "ENCRYPTED: " AN result
KTHXBYE
