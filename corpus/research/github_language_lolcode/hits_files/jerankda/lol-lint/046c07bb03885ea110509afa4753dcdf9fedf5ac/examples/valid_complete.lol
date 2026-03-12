HAI 1.2

BTW Valid LOLCODE program with all features

I HAS A x ITZ 5
I HAS A y ITZ 10
I HAS A msg ITZ "Hello, World!"
I HAS A result

result R SUM OF x AN y
VISIBLE "x + y =" result

I HAS A diff
diff R DIFF OF y AN x
VISIBLE "y - x =" diff

I HAS A product
product R PRODUKT OF x AN y
VISIBLE "x * y =" product

I HAS A quotient
quotient R QUOSHUNT OF y AN x
VISIBLE "y / x =" quotient

I HAS A modulo
modulo R MOD OF y AN x
VISIBLE "y % x =" modulo

result R BOTH SAEM x AN 5
O RLY?
    YA RLY
        VISIBLE "x equals 5"
    NO WAI
        VISIBLE "x does not equal 5"
OIC

result R DIFFRINT x AN y
O RLY?
    YA RLY
        VISIBLE "x and y are different"
    NO WAI
        VISIBLE "x and y are same"
OIC

I HAS A counter ITZ 0
IM IN YR LOOP
    VISIBLE "Loop iteration:" counter
    counter R SUM OF counter AN 1
IM OUTTA YR LOOP

VISIBLE msg

KTHXBYE
