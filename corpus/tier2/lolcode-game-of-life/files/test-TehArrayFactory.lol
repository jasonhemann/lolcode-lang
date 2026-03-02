HAI "Dear curious test reader"
BTW, this clazz once tested must be copied to ur main file, loading filez in lolcode r borked :(

  O HAI IM TehArrayFactory BTW, java style xD
    
    BTW, "I HAS A foo ITZ LIEK TehArray" don't worx, bugz? :(  BUKKIT fieldz are not cloned but referenced, so dis fucktory iz teh workaround"

    HOW IZ I constructingTehShinyBrandNewArray
      I HAS A arr ITZ A BUKKIT
      arr HAS A size ITZ A NOOB
      arr HAS A maxSize ITZ A NOOB
      FOUND YR arr
    IF U SAY SO    

    HOW IZ I adding YR new AN YR array
      NOT array'Z size, O RLY?, YA RLY, array'Z size R 0, array'Z maxSize R 0, OIC
      BOTH SAEM array'Z size AN array'Z maxSize, O RLY?
      YA RLY
        array HAS A SRS array'Z size ITZ new
      NO WAI
        array'Z SRS array'Z size R new
      OIC
      array'Z size R SUM OF array'Z size AN 1
      array'Z maxSize R BIGGR OF array'Z maxSize AN array'Z size
    IF U SAY SO

    HOW IZ I geting YR index AN YR array
      BOTH SAEM index AN BIGGR OF index AN array'Z size, O RLY?, YA RLY, INVISIBLE "HOW I geting YR index: OutOfBoundzExeption: index " AN index " BUT HAZ ONLY " AN array'Z size, GTFO, OIC
      FOUND YR array'Z SRS index
    IF U SAY SO

    HOW IZ I removing YR index AN YR array
      BOTH SAEM index AN BIGGR OF index AN array'Z size, O RLY?, YA RLY, INVISIBLE "HOW I removing YR index: OutOfBoundzExeption: index " AN index " BUT HAZ ONLY " AN array'Z size, GTFO, OIC
      BTW, has to rewrite elements
      I HAS A removedElement ITZ A NOOB
      IM IN YR loopie UPPIN YR x TIL BOTH SAEM x AN DIFF OF array'Z size AN 1
        BOTH SAEM x AN 0, O RLY?,
        YA RLY
          x R index   BTW, offset the loop
          removedElement R array'Z SRS x
          BOTH SAEM x AN DIFF OF array'Z size AN 1, O RLY?, YA RLY, GTFO, OIC
          BTW, it was a granny's debugger: VISIBLE "SEtting removed element: " AN removedElement
        OIC
        array'Z SRS x R array'Z SRS SUM OF x AN 1
      IM OUTTA YR loopie
      array'Z SRS DIFF OF array'Z size AN 1 R NOOB
      array'Z size R DIFF OF array'Z size AN 1
      FOUND YR removedElement
    IF U SAY SO

    HOW IZ I having YR item AN YR array
      I HAS A rezult ITZ 0  BTW, numbas are somehow easier to handle than TROOFs
      IM IN YR loopie UPPIN YR x TIL BOTH SAEM x AN array'Z size
        I HAS A testedItem ITZ array'Z SRS x
        BOTH SAEM item AN testedItem
        O RLY?, YA RLY, rezult R 1, OIC
      IM OUTTA YR loopie
      FOUND YR rezult
    IF U SAY SO

    HOW IZ I yarnizing YR array
      BTW, will fail on BUKKIT items
      I HAS A yarn ITZ "[empty]"
      I HAS A noob ITZ A NOOB
      DIFFRINT array'Z size AN noob, O RLY?
      YA RLY
        BTW VISIBLE "Current size: " AN array'Z size
        IM IN YR loopie UPPIN YR x TIL BOTH SAEM x AN array'Z size
          BOTH SAEM x AN 0, O RLY?
          YA RLY
            yarn R ""  
          NO WAI
            yarn R SMOOSH yarn AN ", " MKAY
          OIC
          yarn R SMOOSH yarn AN array'Z SRS x MKAY
        IM OUTTA YR loopie
      OIC
      FOUND YR yarn
    IF U SAY SO

    HOW IZ I sizing YR array
      array'Z size
    IF U SAY SO

    HOW IZ I checkingEmpty YR array
      BOTH SAEM array'Z size AN 0
    IF U SAY SO

  KTHX

  BTW, testing xD

  I HAS A arr1 ITZ TehArrayFactory IZ constructingTehShinyBrandNewArray MKAY

  VISIBLE "Test 1: Adding items to aray"
  TehArrayFactory IZ adding YR "item1" AN YR arr1 MKAY
  TehArrayFactory IZ adding YR "item2" AN YR arr1 MKAY
  TehArrayFactory IZ adding YR "item3" AN YR arr1 MKAY

  VISIBLE "After test: " AN TehArrayFactory IZ yarnizing YR arr1 MKAY AN ", expected: item1, item2, item3 :)" BTW xD


  VISIBLE "Test 2: Removing middel item from arr"
  I HAS A removed ITZ TehArrayFactory IZ removing YR 1 AN YR arr1 MKAY
  VISIBLE "Removed item2: " AN removed
  VISIBLE "After test: " AN TehArrayFactory IZ yarnizing YR arr1 MKAY AN ", expected: itme1, imte3 :)"

  VISIBLE "Test 3: Adding a item again"
  TehArrayFactory IZ adding YR "item4" AN YR arr1  MKAY
  VISIBLE "After test: " AN TehArrayFactory IZ yarnizing YR arr1 MKAY AN ", expected: item1, item3, item4 :)"
  
  VISIBLE "Test 4: Removing again"
  BTW VISIBLE "Before: " AN arr1 IZ yarnizing MKAY
  removed R TehArrayFactory IZ removing YR 0 AN YR arr1 MKAY
  VISIBLE "Removed item1: " AN removed
  VISIBLE "After test of mixing twixing: " AN TehArrayFactory IZ yarnizing YR arr1 MKAY AN ", expected: item3, item4 xD :)"

  I HAS A arr2 ITZ TehArrayFactory IZ constructingTehShinyBrandNewArray MKAY

  VISIBLE "Test 5: created a new empty arrayz"
  VISIBLE "After test: " AN TehArrayFactory IZ yarnizing YR arr2 MKAY AN ", expecting: empty :)"

  VISIBLE "Test 6: remove first element"
  TehArrayFactory IZ adding YR "item1" AN YR arr2 MKAY
  TehArrayFactory IZ adding YR "item2" AN YR arr2 MKAY
  TehArrayFactory IZ adding YR "item3" AN YR arr2 MKAY
  TehArrayFactory IZ removing YR 0 AN YR arr2 MKAY
  VISIBLE "After test: " AN TehArrayFactory IZ yarnizing YR arr2 MKAY AN ", expecting: item2, item3 :)"


  VISIBLE "Test 7: remove last element"
  I HAS A arr3 ITZ TehArrayFactory IZ constructingTehShinyBrandNewArray MKAY
  TehArrayFactory IZ adding YR "item1" AN YR arr3 MKAY
  TehArrayFactory IZ adding YR "item2" AN YR arr3 MKAY
  TehArrayFactory IZ adding YR "item3" AN YR arr3 MKAY
  removed R TehArrayFactory IZ removing YR 2 AN YR arr3 MKAY
  VISIBLE "Removed item3: " AN removed
  VISIBLE "After test: " AN TehArrayFactory IZ yarnizing YR arr3 MKAY AN ", expecting: item1, item2 :)"

  VISIBLE "Test 8: remove last and add last"
  I HAS A arr4 ITZ TehArrayFactory IZ constructingTehShinyBrandNewArray MKAY
  TehArrayFactory IZ adding YR "item1" AN YR arr4 MKAY
  TehArrayFactory IZ adding YR "item2" AN YR arr4 MKAY
  TehArrayFactory IZ adding YR "item3" AN YR arr4 MKAY
  TehArrayFactory IZ removing YR 2 AN YR arr4 MKAY
  TehArrayFactory IZ adding YR "item4" AN YR arr4 MKAY
  VISIBLE "After test: " AN TehArrayFactory IZ yarnizing YR arr4 MKAY AN ", expecting: item1, item2, item4 :)"

  VISIBLE "Test 8: remove last and add 2 (beyond maxLimit)"
  I HAS A arr5 ITZ TehArrayFactory IZ constructingTehShinyBrandNewArray MKAY
  TehArrayFactory IZ adding YR "item1" AN YR arr5 MKAY
  TehArrayFactory IZ adding YR "item2" AN YR arr5 MKAY
  TehArrayFactory IZ adding YR "item3" AN YR arr5 MKAY
  TehArrayFactory IZ removing YR 2 AN YR arr5 MKAY
  TehArrayFactory IZ adding YR "item4" AN YR arr5 MKAY
  TehArrayFactory IZ adding YR "item5" AN YR arr5 MKAY
  VISIBLE "After test: " AN TehArrayFactory IZ yarnizing YR arr5 MKAY AN ", expecting: item1, item2, item4, item5 :)"

  VISIBLE "Test 9: remove all from the beginning"
  I HAS A arr6 ITZ TehArrayFactory IZ constructingTehShinyBrandNewArray MKAY
  TehArrayFactory IZ adding YR "item1" AN YR arr6 MKAY
  TehArrayFactory IZ adding YR "item2" AN YR arr6 MKAY
  TehArrayFactory IZ removing YR 0 AN YR arr6 MKAY
  TehArrayFactory IZ removing YR 0 AN YR arr6 MKAY
  VISIBLE "After test: " AN TehArrayFactory IZ yarnizing YR arr6 MKAY AN ", expecting: empty :)"

  VISIBLE "Test 10: remove all from the end"
  I HAS A arr7 ITZ TehArrayFactory IZ constructingTehShinyBrandNewArray MKAY
  TehArrayFactory IZ adding YR "item1" AN YR arr7 MKAY
  TehArrayFactory IZ adding YR "item2" AN YR arr7 MKAY
  TehArrayFactory IZ removing YR 1 AN YR arr7 MKAY
  TehArrayFactory IZ removing YR 0 AN YR arr7 MKAY
  VISIBLE "After test: " AN TehArrayFactory IZ yarnizing YR arr7 MKAY AN ", expecting: empty :)"

  VISIBLE "Test 11: remove beyond size"
  I HAS A arr8 ITZ TehArrayFactory IZ constructingTehShinyBrandNewArray MKAY
  TehArrayFactory IZ adding YR "item1" AN YR arr8 MKAY
  TehArrayFactory IZ adding YR "item2" AN YR arr8 MKAY
  TehArrayFactory IZ removing YR 2 AN YR arr8 MKAY
  VISIBLE "After test: expected errorz :)"

  VISIBLE "Test 12: gettin"
  I HAS A arr10 ITZ TehArrayFactory IZ constructingTehShinyBrandNewArray MKAY
  TehArrayFactory IZ adding YR "item1" AN YR arr10 MKAY
  TehArrayFactory IZ adding YR "item2" AN YR arr10 MKAY
  I HAS A value ITZ TehArrayFactory IZ geting YR 1 AN YR arr10 MKAY
  VISIBLE "After test: " AN value AN ", expecting item2 :)"

  VISIBLE "Test 13: get moar than has"
  I HAS A arr9 ITZ TehArrayFactory IZ constructingTehShinyBrandNewArray MKAY
  TehArrayFactory IZ adding YR "item1" AN YR arr9 MKAY
  TehArrayFactory IZ geting YR 1 AN YR arr9 MKAY
  VISIBLE "After test: expecin errz :)))) u noob ofc it worx xD :(D)                                "

  VISIBLE "Test 14: having"
  I HAS A arr11 ITZ TehArrayFactory IZ constructingTehShinyBrandNewArray MKAY
  TehArrayFactory IZ adding YR "item1" AN YR arr11 MKAY
  TehArrayFactory IZ adding YR "item2" AN YR arr11 MKAY
  TehArrayFactory IZ adding YR "item3" AN YR arr11 MKAY
  VISIBLE "Shood has first - item1  : " AN TehArrayFactory IZ having YR "item1" AN YR arr11 MKAY
  VISIBLE "Shood has middle - item2 : " AN TehArrayFactory IZ having YR "item2" AN YR arr11 MKAY
  VISIBLE "Shood has last - item3   : " AN TehArrayFactory IZ having YR "item3" AN YR arr11 MKAY
  VISIBLE "Shood not has item4      : " AN TehArrayFactory IZ having YR "item4" AN YR arr11 MKAY
  VISIBLE "After test :)"

KTHXBYE GL HF
