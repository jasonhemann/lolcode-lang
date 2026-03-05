BTW AUTO-NORMALIZE: strict-1.3 triage variant (HAI/version/comment/operator min-fixes)
HAI 1.3

VISIBLE "TEST 1: WIN is truthy"
IT R WIN
O RLY?
  YA RLY
    VISIBLE "CORRECT: WIN is TRUE"
  NO WAI
    VISIBLE "ERROR: WIN not TRUE"
OIC

VISIBLE "TEST 2: FAIL is falsey"
IT R FAIL
O RLY?
  YA RLY
    VISIBLE "ERROR: FAIL treated as TRUE"
  NO WAI
    VISIBLE "CORRECT: FAIL is FALSE"
OIC

KTHXBYE
