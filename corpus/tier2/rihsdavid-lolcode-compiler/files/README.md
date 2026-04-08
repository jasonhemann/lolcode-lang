# LOLCODE to Python
## Exemple
### LOLCODE
```
BTW This is a single line comment
OBTW This is a multiline comment
    line 2
    line 3
TLDR

BTW variables assignement
I HAS A y ITZ 2
I HAS A x ITZ 10
x R 3

BTW Mathematics operator
SUM OF x AN y
DIFF OF x AN y
PRODUKT OF x AN y
QUOSHUNT OF x AN y
MOD OF x AN y
BIGGR OF x AN y
SMALLR OF x AN y
UPPIN x
NERFIN x

BTW Boolean operator
BOTH OF FAIL AN WIN
EITHER OF FAIL AN WIN
NOT WIN

BTW Comparison
BOTH SAEM x AN y
DIFFRINT x AN y

BTW Conditional
BOTH SAEM x AN y
O RLY?
    YA RLY
    BTW ...
    NO WAI
    BTW ...
OIC

BTW While
IM IN YR LOOP WILE BOTH SAEM x AN y
    BTW ...
    GTFO
IM OUTTA YR LOOP

BTW For
IM IN YR LOOP UPPIN YR x TIL y
    BTW ...
IM OUTTA YR LOOP

IM IN YR LOOP NERFIN YR x TIL y
    BTW ...
IM OUTTA YR LOOP
```

### Python
```
# This is a single line comment
# This is a multiline comment
#    line 2
#    line 3
#

# variables assignement
x = "Three"
y = 2
x = 3

# Mathematics operator
x + y
x - y
x * y 
x / y
x % y
max(x, y)
min(x, y)
x+=1
x-=1

# Boolean operator
False and True
False or True
Not True

# Comparison
x == y
x != y

# Conditional
if x==y:
    # ...
else:
    # ...

# While loop
while x == y :
    # ...
    break

# For loop
for x in range(x, y, 1):
    # ...
    
for x in range(x, y, -1):
    # ...
```
