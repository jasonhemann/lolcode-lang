HAI 1.2
I HAS A EMAIL
GIMMEH EMAIL

I HAS A VALID_EMAIL ITZ A NOOB
VISIBLE "Checking if email is valid..."

BTW Basic email regex for demonstration purposes. Not suitable for production use.
I HAS A REGEX
VISIBLE "^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,4}$"

I HAS A MATCH
I HAS A LOWERCASE_EMAIL

I IZ REGEX "^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,4}$" IN EMAIL
OBTW Check if the email matches the regex pattern.
    BOTH SAEM IT, YR MATCH
    O RLY?
        YA RLY
            SET VALID_EMAIL TO WIN
            VISIBLE "Valid email!"
        NO WAI
            VISIBLE "Invalid email!"
        OIC
    OIC

I HAS A CHAR
I HAS A LENGTH ITZ 0
IM IN YR LOOP UPPIN YR CHAR TIL BOTH SAEM CHAR AN EMAIL
    I HAS A SUBCHAR
    SUBCHAR R MAEK SUBSTRINGS A EMAIL STARTIN CHAR, 1
    I HAS A MATCH ITZ A NOOB
    I IZ REGEX "[A-Z]" IN SUBCHAR
    BTW Check if the character is uppercase.
        BOTH SAEM IT, YR MATCH
        O RLY?
            YA RLY
                I HAS A LOWERCASE_CHAR
                I HAS A LOWERCASE_CHAR ITZ SUM OF SUBCHAR AN "32"
                I HAS A LOWERCASE_CHAR ITZ I HAS A LOWERCASE_CHAR MKAY
                SUBCHAR R MAEK SUBSTRINGS A SUBCHAR, 0
                SUBCHAR R MAEK "CHARACTER" A SUBCHAR
            NO WAI
                I HAS A LOWERCASE_CHAR ITZ SUBCHAR
            OIC
    OIC
    I HAS A LOWERCASE_EMAIL
    I HAS A LOWERCASE_EMAIL ITZ BOTH SAEM LENGTH AN 0, O RLY? YA RLY, SUBCHAR, NO WAI, BOTH SAEM LOWERCASE_CHAR, O RLY? YA RLY, LOWERCASE_CHAR, NO WAI, BOTH SAEM SUBCHAR, "(", O RLY? YA RLY, SUBCHAR, NO WAI, LOWERCASE_EMAIL
    I HAS A LENGTH ITZ BOTH SAEM LENGTH AN 0, O RLY? YA RLY, "1", NO WAI, DIFF OF LENGTH AN "0" BTW Increment the length of the lowercase email.
IM OUTTA YR LOOP

VISIBLE "Lowercase email: ", LOWERCASE_EMAIL
KTHXBYE