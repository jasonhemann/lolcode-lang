# regex for lexemes
keywords = "^(R)$|^(WON OF)$|^(NOT)$|^(ANY OF)$|^(ALL OF)$|^(BOTH SAEM)$|^(DIFFRINT)$|^(SMOOSH)$|^(MAEK)$|^(A)$|^(IS NOW A)$|^(VISIBLE)$|^(GIMMEH)$|^(O RLY\?)$|^(YA RLY)$|^(MEBBE)$|^(NO WAI)$|^(OIC)$|^(WTF\?)$|^(OMG)$|^(OMGWTF)$|^(GTFO)$|^(IM IN YR)$|^(UPPIN)$|^(NERFIN)$|^(YR)$|^(TIL)$|^(WILE)$|^(IM OUTTA YR)$|^(NUMBR)$|^(NUMBAR)$|^(YARN)$|^(TROOF)$"

BTW_flag = 0
OBTW_flag = 0
comm_lit = ""

single_line = "(BTW)"
multiple_start = "(OBTW)"
multiple_end = "(TLDR)"
comment_lit = ".*"

start = "(HAI)"
end = "(KTHXBYE)"

declaration = "(I HAS A)"
assignment_var = "(ITZ)"
assignment_op = "(R)"

and_operator = "(BOTH OF)"
or_operator = "(EITHER OF)"
xor_operator = "(WON OF)"
not_operator = "(NOT)"
arity_and = "(ALL OF)"
arity_or = "(ANY OF)"
operand_sep = "(AN)"

plus = "(SUM OF)"
difference = "(DIFF OF)"
multiply = "(PRODUKT OF)"
divide = "(QUOSHUNT OF)"
modulo = "(MOD OF)"

greater_than = "(BIGGR OF)"
less_than = "(SMALLR OF)"
equal = "(BOTH SAEM)"
not_equal = "(DIFFRINT)"

str_concat = "(SMOOSH)"
typecast = "(MAEK)"
typecast_assign = "(A)"
recast = "(IS NOW A)"

printing = "(VISIBLE)"
inputting = "(GIMMEH)"

if_start = "(O RLY\?)"
if_cond = "(YA RLY)"
elif_cond = "(MEBBE)"
else_cond = "(NO WAI)"
if_end = "(OIC)"

switch_case = "(WTF\?)"
case = "(OMG)"
default = "(OMGWTF)"
break_key = "(GTFO)"

loop_start = "(IM IN YR)"
increment = "(UPPIN)"
decrement = "(NERFIN)"
loop_cond = "(YR)"
til = "(TIL)"
wile = "(WILE)"
loop_end = "(IM OUTTA YR)"

NUMBR = "(-?[0-9]+)"
NUMBAR = "(-?[0-9]+\.?[0-9]+)"
YARN = "(\".*\")"
TROOF = "(WIN)|(FAIL)"
TYPE = "(NUMBR)|(NUMBAR)|(YARN)|(TROOF)"
variable = "([A-Za-z][A-Za-z0-9_]*)"

new_line = "(\n)"
