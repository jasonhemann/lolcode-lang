import re

# Patterns to Match With for a lexeme
varIdentifier = r"^[a-zA-Z][a-zA-Z0-9_]*$"
strIdentifier = r"\"[^\"]*\""
numIdentifier = r"^[0-9]+$"
floatIdentifier = r"^-?[0-9]+.[0-9]+$"
troofIdentifier = r"^WIN$|^FAIL$"

# Patterns to match with a line
hai = r"^HAI(.*)(\s*)$"						# Done 
kthxbye = r"^KTHXBYE(\s*)$"
empty = r"^(\s*)$"
ihasa = r"(\s*)(I HAS A) ([a-zA-Z][a-zA-Z0-9_]*)(\s*)"
ihasitz = r"(\s*)(I HAS A) ([a-zA-Z][a-zA-Z0-9_]*) (ITZ) (.+)(\s*)"
gimmeh = r"(\s*)(?P<kw>GIMMEH) (?P<var>[a-zA-Z][a-zA-Z0-9_]*)(\s*)"
r = r"(\s*)(?P<var>[a-zA-Z][a-zA-Z0-9_]*) (?P<kw>R) (?P<val>.+)(\s*)"
visible = r"(\s*)(?P<kw>VISIBLE) (?P<expr>.+)(\s*)"
smoosh = r"(\s*)(?P<kw>SMOOSH) (?P<ops>.+)(\s*)"

sumof = r"(\s*)(?P<kw>SUM OF) (?P<op1>.+) (AN) (?P<op2>.+)(\s*)"					# Arithmetic Expressions 
diffof = r"^(\s*)(?P<kw>DIFF OF) (?P<op1>.+) (AN) (?P<op2>.+)(\s*)"
produktof = r"^(\s*)(?P<kw>PRODUKT OF) (?P<op1>.+) (AN) (?P<op2>.+)(\s*)"
quoshuntof = r"^(\s*)(?P<kw>QUOSHUNT OF) (?P<op1>.+) (AN) (?P<op2>.+)(\s*)"
modof = r"^(\s*)(?P<kw>MOD OF) (?P<op1>.+) (AN) (?P<op2>.+)(\s*)"

# Comparison Expressions
biggrof = r"^(\s*)(?P<kw>BIGGR OF) (?P<op1>.+) (AN) (?P<op2>.+)(\s*)"		# > Operator, returns the bigger number
smallrof = r"^(\s*)(?P<kw>SMALLR OF) (?P<op1>.+) (AN) (?P<op2>.+)(\s*)"		# < Operator, returns the smaller number 
bothsaem = r"^(\s*)(?P<kw>BOTH SAEM) (?P<op1>.+) (AN) (?P<op2>.+)(\s*)"		# == Operator
diffrint = r"^(\s*)(?P<kw>DIFFRINT) (?P<op1>.+) (AN) (?P<op2>.+)(\s*)"		# != Operator 

# Logical Expressions 
notop = r"^(\s*)(?P<kw>NOT) (?P<op1>.+)(\s*)"										# NOT 
bothof = r"^(\s*)(?P<kw>BOTH OF) (?P<op1>.+) (AN) (?P<op2>.+)(\s*)"					# AND
eitherof = r"^(\s*)(?P<kw>EITHER OF) (?P<op1>.+) (AN) (?P<op2>.+)(\s*)" 				# OR
wonof = r"^(\s*)(?P<kw>WON OF) (?P<op1>.+) (AN) (?P<op2>.+)(\s*)"					# XOR
anyof = r"^(\s*)(?P<kw>ANY OF) .+(\s*)"												# Will take infinite arguments and apply AND
allof = r"^(\s*)(?P<kw>ALL OF) .+(\s*)"												# Will take infinite arguments and apply OR

# If statements
orly = r"^(\s*)(?P<kw>O RLY\?)(\s*)$"
yarly = r"^(\s*)(?P<kw>YA RLY)(\s*)$"
nowai = r"^(\s*)(?P<kw>NO WAI)(\s*)$"
oic = r"^(\s*)(?P<kw>OIC)(\s*)$"

# Switch-case
wtf = r'\s*WTF\?\s*$'
omg = r"^(\s*)(?P<kw>OMG) (?P<lit>.+)"
gtfo = r'\s*GTFO\s*$'
omgwtf = r'\s*OMGWTF\s*$'
oicswitch = r'\s*OIC\s*$'

# Lists of Compatible Operands
arithOpsList = ["SUMOF","DIFFOF","PRODUKTOF","QUOSHUNTOF","MODOF","BIGGROF","SMALLROF"]
compOpsList = ["BIGGROF","SMALLROF","BOTHSAEM","DIFFRINT"]
boolOpsList = ["NOT","BOTHOF","EITHEROF","WONOF","ANYOF","ALLOF"]