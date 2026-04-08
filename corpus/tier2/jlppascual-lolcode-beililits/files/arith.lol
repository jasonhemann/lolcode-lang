HAI 1.2
	I HAS A x
	I HAS A y
	I HAS A answer

	VISIBLE "x: "
	GIMMEH x

	VISIBLE "y: "
	GIMMEH y

	answer R SUM OF x AN y
	VISIBLE x "+" y " is " answer

	answer R DIFF OF x AN y
	VISIBLE x "-" y " is " answer

	answer R PRODUKT OF x AN y
	VISIBLE x "*" y " is " answer

	answer R QUOSHUNT OF x AN y
	VISIBLE x "/" y " is " answer

	answer R MOD OF x AN y
	VISIBLE x "%" y " is " answer

	answer R BIGGR OF x AN y
	VISIBLE "max(" x "," y ") is " answer

	answer R SMALLR OF x AN y
	VISIBLE "min(" x "," y ") is " answer


	BTW answer R SUM OF 2 AN SUM OF 3 AN SUM OF 4 AN 1

	BTW VISIBLE answer

KTHXBYE
