HAI
	WAZZUP
		I HAS A num1
		I HAS A num2
		I HAS A temp ITZ 2
	BUHBYE
	
	VISIBLE "Gimmeh a number: "
	num1 R 2
	VISIBLE num1

	VISIBLE "Gimmeh a number: "
	num2 R 0
	VISIBLE num2
	VISIBLE "─────────────────────────────────────────────────"

	IM IN YR asc UPPIN YR num2 WILE BOTH SAEM num2 AN SMALLR OF num2 AN num1
		VISIBLE num2
	IM OUTTA YR asc

	VISIBLE "─────────────────────────────────────────────────"
	IM IN YR desc NERFIN YR num2 TIL BOTH SAEM num2 AN 0
		VISIBLE num2
	IM OUTTA YR desc

	VISIBLE "─────────────────────────────────────────────────"
	BTW prints 2 to 9 using TIL
	IM IN YR print10 UPPIN YR temp TIL BOTH SAEM temp AN 10
		VISIBLE temp
	IM OUTTA YR print10

	VISIBLE "─────────────────────────────────────────────────"
	BTW at this point, temp’s value is 10, so we must reassign its initial value
	temp R 2
	
	BTW prints 2 to 9 but using WILE
	IM IN YR print10 UPPIN YR temp WILE DIFFRINT temp AN 10
		VISIBLE temp
	IM OUTTA YR print10


KTHXBYE