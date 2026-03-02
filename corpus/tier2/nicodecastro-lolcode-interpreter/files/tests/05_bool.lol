HAI
    WAZZUP
        BTW variable dec
        I HAS A x
        I HAS A y
    BUHBYE

    VISIBLE "x:" + WIN + ", y:" + WIN
    x R WIN
    y R WIN

    VISIBLE BOTH OF x AN y        BTW WIN
    VISIBLE EITHER OF x AN y        BTW WIN
    VISIBLE WON OF x AN y        BTW FAIL
    VISIBLE NOT x        BTW FAIL
    VISIBLE ALL OF x AN x AN x AN y MKAY        BTW WIN
    VISIBLE ANY OF y AN y AN y AN 0 MKAY        BTW WIN
    VISIBLE ANY OF BOTH OF x AN EITHER OF NOT x AN y AN y AN NOT y MKAY        BTW WIN
    VISIBLE BOTH OF x AN EITHER OF NOT x AN y        BTW WIN

    VISIBLE "x: " + FAIL + ", y: " + WIN
    x R FAIL

    VISIBLE BOTH OF x AN y        BTW FAIL
    VISIBLE EITHER OF x AN y        BTW WIN
    VISIBLE WON OF x AN y        BTW WIN
    VISIBLE NOT x        BTW WIN
    VISIBLE ALL OF x AN x AN x AN y MKAY        BTW FAIL
    VISIBLE ANY OF y AN y AN y AN 0 MKAY        BTW WIN
    VISIBLE ANY OF BOTH OF x AN EITHER OF NOT x AN y AN y AN NOT y MKAY        BTW WIN
    VISIBLE BOTH OF x AN EITHER OF NOT x AN y        BTW FAIL

    VISIBLE "x:" + FAIL + ", y:" + FAIL
    y R FAIL

    VISIBLE BOTH OF x AN y        BTW FAIL
    VISIBLE EITHER OF x AN y        BTW FAIL
    VISIBLE WON OF x AN y        BTW FAIL
    VISIBLE NOT x        BTW WIN
    VISIBLE ALL OF x AN x AN x AN y MKAY        BTW FAIL
    VISIBLE ANY OF y AN y AN y AN 0 MKAY        BTW FAIL
    VISIBLE ANY OF BOTH OF x AN EITHER OF NOT x AN y AN y AN NOT y MKAY        BTW WIN
    VISIBLE BOTH OF x AN EITHER OF NOT x AN y        BTW FAIL
KTHXBYE