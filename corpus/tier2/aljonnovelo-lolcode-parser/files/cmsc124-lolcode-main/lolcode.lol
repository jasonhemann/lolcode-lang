OBTW -------------------------------------->

        NOTES:
                    1. OPERATIONS <expr> include Arithmetic, Boolean, and Comparison.
                    2. NOT STATEMENTS: <program>, <func>, <ret>, <main>, <if>, <else>, <acase>, <defcase>, <vardec>, <linebreak>, <varinit>
                    4. Result of an OPERATION or a FUNCTION is stored in an implicit variable called 'IT'. 

<-------------------------------------- TLDR 

BTW _________________________________________________________________________________________________________________________________ MAIN

HOW IZ I yayyparam0                                                          BTW <func>             Function Declaration Start
    VISIBLE "YAY!"                                                           BTW                    Statements
IF U SAY SO                                                                  BTW                    Function Declaration End

HOW IZ I gtfoparam0                                                          BTW                    Function Declaration Start
    VISIBLE "YAY GTFO!"                                                      BTW                    Statements
    GTFO                                                                     BTW <ret>              Return NOOB to IT Variable
IF U SAY SO                                                                  BTW                    Function Declaration End

HOW IZ I plusparam2 YR x AN YR y                                             BTW                    Function Declaration Start
    FOUND YR SUM OF x AN y                                                   BTW <ret>              Return: Value to IT Variable
IF U SAY SO                                                                  BTW                    Function Declaration End


HAI                                                                          BTW <main>             Program Start

    WAZZUP                                                                   BTW <vardec>           Variable Declaration Start
        I HAS A thing                                                        BTW <varinit>          Initialization: Uninitialized Variable
        I HAS A var1 ITZ 12                                                  BTW                    Initialization: Literal
        I HAS A thing2 ITZ thing                                             BTW                    Initialization: Variable
        I HAS A thing3 ITZ SUM OF 5 AN 4                                     BTW                    Initialization: <expression> (Operation)
    BUHBYE                                                                   BTW                    Variable Declaration End

    GIMMEH thing                                                             BTW <input>
    VISIBLE "Input Yarn: " + thing + " " + 124                               BTW <print>  

    GIMMEH thing, VISIBLE "Input Yarn: " + thing + " " + 124!               


    SMOOSH "SUM OF 2 AN 4 is " AN 6 AN " OR " AN 6.0                         BTW <concat>           str1 + str2 + ... + strN
    SUM OF 2 AN 4                                                            BTW <sum>              (result is NUMBR)
    DIFF OF 4 AN 3.14                                                        BTW <difference>       (result is NUMBAR)
    PRODUKT OF "2" AN "7"                                                    BTW <product>          (result is NUMBR)
    QUOSHUNT OF 5 AN "12"                                                    BTW <quotient>         (result is a NUMBR)
    MOD OF 3 AN "3.14"                                                       BTW <modulo>           (result is a NUMBAR)
    BIGGR OF 1.24 AN 1                                                       BTW <min>              Minimum
    SMALLR OF 1.24 AN 1                                                      BTW <max>              Maximum
    SUM OF QUOSHUNT OF PRODUKT OF 3 AN 4 AN 2 AN 1                           BTW                    NESTED -- (((3*4)/2)+1)
    SUM OF SUM OF SUM OF 3 AN 4 AN 2 AN 1                                    BTW                    NESTED -- (((3+4)+2)+1)

    BOTH OF thing2 AN EITHER OF thing2 AN "WIN"                              BTW <and>
    EITHER OF thing2 AN 1                                                    BTW <or>
    WON OF 3.14 AN thing2                                                    BTW <xor>
    NOT WIN                                                                  BTW <not>
    ALL OF thing2 AN thing2 AN thing2 MKAY                                   BTW <infand>           Inf arity AND
    ANY OF thing2 AN thing2 AN thing2 MKAY                                   BTW <infor>            Inf arity OR

    BOTH SAEM 1 AN 1                                                         BTW <equal>            x == y
    DIFFRINT 1.24 AN 1                                                       BTW <notequal>         x != y
    BOTH SAEM 1.24 AN BIGGR OF 1.24 AN 1                                     BTW <greatqual>        x >= y
    BOTH SAEM 1 AN SMALLR OF 1 AN 1                                          BTW <lessequal>        x <= y
    DIFFRINT 1 AN SMALLR OF 1 AN 1                                           BTW <less>             x < y
    DIFFRINT 1 AN BIGGR OF 1 AN 1                                            BTW <great>            x > y

    MAEK var1 A NUMBAR                                                       BTW <typecastit>       Result to   IT
    var1 IS NOW A NUMBAR                                                     BTW <typecastis>       Through     IS NOW A
    number R MAEK number YARN                                                BTW <typecastas>       Through     ASSIGNNMENT

    thing R 124                                                              BTW <varassign>        <variable> R <literal>
    thing R number                                                           BTW                    <variable> R <variable>
    thing R SUM OF 1 AN 123                                                  BTW                    <variable> R <expression>
    thing R BOTH OF WIN AN WIN                                               BTW                    <variable> R <expression>

    O RLY?                                                                   BTW <ifelse>           Flow-Control Start (uses value of IT)
        YA RLY                                                               BTW <if>               If
            VISIBLE "YES"                                                    BTW                    Statements
        NO WAI                                                               BTW <else>             Else
            VISIBLE "NO"                                                     BTW                    Statements
    OIC                                                                      BTW                    Flow-Control End
    
    WTF?                                                                     BTW <case>             Case (uses value of IT)
        OMG 1                                                                BTW <acase>            A Particular Case
            VISIBLE 1                                                        BTW                    Statements
        OMG 2                                                                BTW                    A Particular Case    
            VISIBLE 2                                                        BTW                    Statements
        OMGWTF                                                               BTW <defcase>          Default Case
            VISIBLE "NAH"                                                    BTW                    Statements
    OIC                                                                      BTW                    Case End

    I HAS A temp ITZ 2                                                       BTW                    for(temp=2; UNTIL temp == 10; temp++)
    IM IN YR print_10 UPPIN YR temp TIL BOTH SAEM temp AN 10                 BTW <loop>             Start of A Till Loop
        VISIBLE temp                                                         BTW                    Statements      
    IM OUTTA YR print_10                                                     BTW                    End of A Loop

    temp R 2                                                                 BTW                    for(temp=2; WHILE temp != 10; temp++)      
    IM IN YR print_10 UPPIN YR temp WILE DIFFRINT temp AN 10                 BTW                    Start of A Wile Loop               
        VISIBLE temp                                                         BTW                    Statements                           
    IM OUTTA YR print_10                                                     BTW                    End of A Loop

    I IZ plusparam2 YR SUM OF 1 AN 1 AN YR SUM OF 1 AN 1                     BTW <funccall>         Function Call: 3 Parameters
    I IZ yayyparam0 MKAY                                                     BTW                    Function Call: 0 Parameter

KTHXBYE                                                                      BTW                    Program End