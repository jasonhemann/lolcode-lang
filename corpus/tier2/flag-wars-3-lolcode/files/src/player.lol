BTW --- Player object ---
O HAI IM Player
	I HAS A texture
	I HAS A hitbox
	I HAS A position

	I HAS A SOURCE ITZ I IZ rectangle YR 0.0 AN YR 0.0 AN YR 231.0 AN YR 240.0 MKAY
	I HAS A ORIGIN ITZ I IZ vector2 YR 0.0 AN YR 0.0 MKAY

	HOW IZ I initPlayer
		ME'Z texture R I IZ RAYLIB'Z LOADTEXTURE YR "assets/graphics/a_fk_leaf.png" MKAY
		ME'Z position R I IZ rectangle YR 600.0 AN YR 660.0 AN YR 50.0 AN YR 50.0 MKAY
		ME'Z hitbox R I IZ rectangle YR 100.0 AN YR 660.0 AN YR 20.0 AN YR 20.0 MKAY
	IF U SAY SO

    HOW IZ I collision YR bulletRect
        I HAS A col ITZ I IZ checkCollisionRecs YR ME'Z hitbox AN YR bulletRect MKAY
        FOUND YR col
    IF U SAY SO

	HOW IZ I movement
		I HAS A movement ITZ 0.0
		I HAS A possibleNewPos ITZ ME'Z position'Z x

        BTW Check key pressed
		EITHER OF I IZ RAYLIB'Z IZKEYDOWN YR KEYLEFT MKAY AN I IZ RAYLIB'Z IZKEYDOWN YR KEYA MKAY
		O RLY?, YA RLY
			movement R PRODUKT OF -1.0 AN 200.0
		MEBBE EITHER OF I IZ RAYLIB'Z IZKEYDOWN YR KEYRIGHT MKAY AN I IZ RAYLIB'Z IZKEYDOWN YR KEYD MKAY
			movement R 200.0
		OIC

        possibleNewPos R SUM OF ME'Z position'Z x AN PRODUKT OF movement AN I IZ RAYLIB'Z GETFRAMETIME MKAY

		BTW Check the window limits
		I HAS A offsetLeft ITZ DIFF OF possibleNewPos AN -50.0
		I HAS A offsetRight ITZ SUM OF possibleNewPos AN 50.0
		I HAS A leftOnScreen ITZ DIFFRINT offsetLeft AN SMALLR OF offsetLeft AN 60.0
		I HAS A rightOnScreen ITZ DIFFRINT offsetRight AN BIGGR OF offsetRight AN 1250.0

		BOTH OF leftOnScreen AN rightOnScreen
		O RLY?, YA RLY, ME'Z position'Z x R possibleNewPos, OIC
	IF U SAY SO

	HOW IZ I updatePlayer
		ME IZ movement MKAY
		ME'Z hitbox'Z x R SUM OF ME'Z position'Z x AN 15
		ME'Z hitbox'Z y R SUM OF ME'Z position'Z y AN 15
	IF U SAY SO

	HOW IZ I drawPlayer
		I IZ drawTexturePro ...
			YR ME'Z texture AN YR ME'Z SOURCE AN YR ME'Z position ...
			AN YR ME'Z ORIGIN AN YR 0.0 AN YR white ...
		MKAY
        BTW I IZ RAYLIB'Z DRAWRECTANGLEREC YR ME'Z hitbox'Z x AN YR ME'Z hitbox'Z y AN YR ME'Z hitbox'Z width AN YR ME'Z hitbox'Z height AN YR 255 AN YR 255 AN YR 255 AN YR 255 MKAY
	IF U SAY SO
KTHX
BTW --- End of Player object ---