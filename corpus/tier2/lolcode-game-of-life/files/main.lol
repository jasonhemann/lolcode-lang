HAI "Dear reader"

  BTW *********************************************************************************
  BTW ** classes **********************************************************************
  

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

  BTW *********************************************************************************
  BTW *********************************************************************************

  O HAI IM TehRandomness
    I HAS A multiplier ITZ 16807
    I HAS A prime ITZ 2137    BTW chaotix bhvr dependz much on dis prime
    I HAS A x0 ITZ 1337

    HOW IZ I absolute YR num
      BOTH SAEM 0 AN BIGGR OF 0 AN num, O RLY?
      YA RLY
        FOUND YR PRODUKT OF num AN -1
      NO WAI
        FOUND YR num
      OIC
    IF U SAY SO

    HOW IZ I generating YR min AN YR max
      ME'Z x0 R PRODUKT OF ME'Z multiplier AN ME'Z x0
      ME'Z x0 R MOD OF ME'Z x0 AN ME'Z prime

      FOUND YR SUM OF ...
        MOD OF ...
          ME'Z x0 ...
          AN DIFF OF max AN min ...
        AN min
      
    IF U SAY SO

  KTHX

  BTW *********************************************************************************
  BTW *********************************************************************************

  O HAI IM Graphix

    I HAS A widht ITZ 30
    I HAS A heigth ITZ 30
    I HAS A stylez ITZ TehArrayFactory IZ constructingTehShinyBrandNewArray MKAY  BTW, pixels in conzole arnt really pixls but various unicode chrs
    I HAS A pixelz ITZ A BUKKIT BTW, dis a map of pixelz, they r constant but all diffrnt
    I HAS A screen ITZ A BUKKIT BTW, the actual screen to prnt
    I HAS A clearingOption ITZ WIN

    TehArrayFactory IZ adding YR ":(1F408)" AN YR stylez MKAY
    TehArrayFactory IZ adding YR ":(1F431)" AN YR stylez MKAY
    TehArrayFactory IZ adding YR ":(1F640)" AN YR stylez MKAY
    TehArrayFactory IZ adding YR ":(1F63E)" AN YR stylez MKAY
    TehArrayFactory IZ adding YR ":(1F63F)" AN YR stylez MKAY
    TehArrayFactory IZ adding YR ":(1F63C)" AN YR stylez MKAY
    TehArrayFactory IZ adding YR ":(1F63A)" AN YR stylez MKAY
    TehArrayFactory IZ adding YR ":(1F63D)" AN YR stylez MKAY
    TehArrayFactory IZ adding YR ":(1F63B)" AN YR stylez MKAY
    TehArrayFactory IZ adding YR ":(1F639)" AN YR stylez MKAY
    TehArrayFactory IZ adding YR ":(1F638)" AN YR stylez MKAY
    TehArrayFactory IZ adding YR ":(1F43E)" AN YR stylez MKAY

    HOW IZ I testPrinting
      I HAS A testScreen ITZ A BUKKIT
      IM IN YR colz UPPIN YR x TIL BOTH SAEM x AN ME'Z widht
        I HAS A pixelCol ITZ A BUKKIT
        I HAS A screenCol ITZ A BUKKIT
        IM IN YR rowz UPPIN YR y TIL BOTH SAEM y AN ME'Z heigth
          screenCol HAS A SRS y ITZ 1
        IM OUTTA YR rowz
        testScreen HAS A SRS x ITZ screenCol
      IM OUTTA YR colz
      I HAS A temp ITZ ME'Z screen
      ME'Z screen R testScreen
      ME IZ visible MKAY
      ME'Z screen R temp

    IF U SAY SO

    HOW IZ I visible
      ME'Z clearingOption, O RLY?, YA RLY, VISIBLE ":(001B)[H", OIC
      I HAS A line ITZ ""

      BTW uppre borda
      line R "+"
      IM IN YR row UPPIN YR x TIL BOTH SAEM x AN ME'Z widht
        line R SMOOSH line AN "--" MKAY
      IM OUTTA YR row
      line R SMOOSH line AN "+" MKAY
      VISIBLE line

      
      BTW rowz
      IM IN YR rowz UPPIN YR y TIL BOTH SAEM y AN ME'Z heigth
        I HAS A pixelRow ITZ ME'Z pixelz'Z SRS y
        I HAS A screenRow ITZ ME'Z screen'Z SRS y
        line R "|"
        IM IN YR colz UPPIN YR x TIL BOTH SAEM x AN ME'Z widht
          I HAS A pixel ITZ pixelRow'Z SRS x
          I HAS A screen ITZ screenRow'Z SRS x
          screen, O RLY? 
          YA RLY
            line R SMOOSH line AN pixel MKAY
          NO WAI
            line R SMOOSH line AN "  " MKAY
          OIC
        IM OUTTA YR colz
      line R SMOOSH line AN "|" MKAY
      VISIBLE line
      IM OUTTA YR rowz

      BTW lowr borda
      line R "+"
      IM IN YR row UPPIN YR x TIL BOTH SAEM x AN ME'Z widht
        line R SMOOSH line AN "--" MKAY
      IM OUTTA YR row
      line R SMOOSH line AN "+" MKAY
      VISIBLE line

    IF U SAY SO

    HOW IZ I startingNewScreen
      I HAS A screenRow ITZ A BUKKIT
      IM IN YR rowz UPPIN YR y TIL BOTH SAEM y AN ME'Z heigth
        screenRow R ME'Z screen'Z SRS y
        IM IN YR colz UPPIN YR x TIL BOTH SAEM x AN ME'Z widht
          screenRow'Z SRS x R 0
        IM OUTTA YR colz
      IM OUTTA YR rowz
    IF U SAY SO

    HOW IZ I putinPixel YR x AN YR y
      I HAS A row ITZ ME'Z screen'Z SRS y
      row'Z SRS x R 1
    IF U SAY SO


  KTHX

  HOW IZ I initingGraphix
    BTW, another bugz bunny in lci :(  if has 2 bukkitz in a parent BUTTKIT, then setting ONE inside member funxion does set BOTH of them!
    BTW, that's why I need external init funxion
    BTW, it worx fine for 'stylez' bukkit, bcs not in a funxion
    IM IN YR rowz UPPIN YR y TIL BOTH SAEM y AN Graphix'Z heigth
      I HAS A pixelRou ITZ A BUKKIT
      I HAS A screenRou ITZ A BUKKIT
      IM IN YR colz UPPIN YR x TIL BOTH SAEM x AN Graphix'Z widht
        screenRou HAS A SRS x ITZ 0
        I HAS A styleCount ITZ TehArrayFactory IZ sizing YR Graphix'Z stylez MKAY
        I HAS A random ITZ TehRandomness IZ generating YR 0 AN YR styleCount MKAY
        pixelRou HAS A SRS x ITZ Graphix'Z TehArrayFactory IZ geting YR random AN YR Graphix'Z stylez MKAY
      IM OUTTA YR colz
      Graphix'Z pixelz HAS A SRS y ITZ pixelRou
      Graphix'Z screen HAS A SRS y ITZ screenRou
    IM OUTTA YR rowz
    GTFO
  IF U SAY SO

  BTW *********************************************************************************
  BTW ** compoze bord - important clazz ***********************************************

  O HAI IM TehBoard
  
    I HAS A widht ITZ 30
    I HAS A heigth ITZ 30
    I HAS A contentz ITZ A BUKKIT

    HOW IZ I maekBoard
      IM IN YR rowz UPPIN YR y TIL BOTH SAEM y AN ME'Z heigth
        I HAS A row ITZ A BUKKIT
        IM IN YR colz UPPIN YR x TIL BOTH SAEM x AN ME'Z widht
          row HAS A SRS x ITZ 0
        IM OUTTA YR colz
        ME'Z contentz HAS A SRS y ITZ row
      IM OUTTA YR rowz
      GTFO
    IF U SAY SO

    HOW IZ I cloned
      I HAS A shinyBrandNewMatrix ITZ A BUKKIT
      IM IN YR rowz UPPIN YR y TIL BOTH SAEM y AN ME'Z heigth
        I HAS A row ITZ A BUKKIT
        IM IN YR colz UPPIN YR x TIL BOTH SAEM x AN ME'Z widht
          row HAS A SRS x ITZ ME IZ get YR x AN YR y MKAY
        IM OUTTA YR colz
        shinyBrandNewMatrix HAS A SRS y ITZ row
      IM OUTTA YR rowz
      FOUND YR shinyBrandNewMatrix
    IF U SAY SO

    HOW IZ I lessThan YR numba AN YR othaNumba
      DIFFRINT numba AN BIGGR OF numba AN othaNumba
    IF U SAY SO

    HOW IZ I geq YR numba AN YR othaNumba
      BOTH SAEM numba AN BIGGR OF numba AN othaNumba
    IF U SAY SO

    BTW get a cell with wrapp'd borders
    HOW IZ I get YR x AN YR y
      I HAS A oldX ITZ x
      I HAS A oldY ITZ y
      ME IZ lessThan YR x AN YR 0 MKAY, O RLY?
      YA RLY
        x R SUM OF ME'Z widht AN x
      OIC

      ME IZ geq YR x AN YR ME'Z widht MKAY, O RLY?
      YA RLY
        x R DIFF OF x AN ME'Z widht
      OIC

      ME IZ lessThan YR y AN YR 0 MKAY, O RLY?
      YA RLY
        y R SUM OF ME'Z heigth AN y
      OIC

      ME IZ geq YR y AND YR ME'Z heigth MKAY, O RLY?
      YA RLY
        y R DIFF OF y AN ME'Z heigth
      OIC

      I HAS A row ITZ ME'Z contentz'Z SRS y
      I HAS A cell ITZ row'Z SRS x
      FOUND YR cell
    IF U SAY SO

    HOW IZ I set YR x AN YR y AN YR valz
      I HAS A col ITZ ME'Z contentz'Z SRS y
      col'Z SRS x R valz
      GTFO
    IF U SAY SO

    HOW IZ I calculateNeighbors YR x AN YR y
      SUM OF ME IZ get YR DIFF OF x AN 1 AN YR y              MKAY AN ...
      SUM OF ME IZ get YR DIFF OF x AN 1 AN YR DIFF OF y AN 1 MKAY AN ...
      SUM OF ME IZ get YR DIFF OF x AN 1 AN YR SUM OF y AN 1  MKAY AN ...
      SUM OF ME IZ get YR x              AN YR DIFF OF y AN 1 MKAY AN ...
      SUM OF ME IZ get YR x              AN YR SUM OF y AN 1  MKAY AN ...
      SUM OF ME IZ get YR SUM OF x AN 1  AN YR y              MKAY AN ...
      SUM OF ME IZ get YR SUM OF x AN 1  AN YR DIFF OF y AN 1 MKAY AN ...
             ME IZ get YR SUM OF x AN 1  AN YR SUM OF y AN 1  MKAY
      BTW compilar merges these lines and shows shifted error line afterwards :(
    IF U SAY SO

    HOW IZ I calculaitink YR spawnRules AN YR deadRules
      I HAS A newBoard ITZ ME IZ cloned MKAY
      IM IN YR rowz UPPIN YR y TIL BOTH SAEM y AN ME'Z heigth
        I HAS A row ITZ newBoard'Z SRS y
        IM IN YR colz UPPIN YR x TIL BOTH SAEM x AN ME'Z widht
          I HAS A neighbors ITZ ME IZ calculateNeighbors YR x AN YR y MKAY
          I HAS A current ITZ ME IZ get YR x AN YR y MKAY
          MAEK current A TROOF, O RLY?
          YA RLY
            row'Z SRS x R DIFF OF 1 AN TehArrayFactory IZ having YR neighbors AN YR deadRules MKAY 
            BTW was alive, can only die
          NO WAI
            row'Z SRS x R TehArrayFactory IZ having YR neighbors AN YR spawnRules MKAY
            BTW was dead, can only spawn
          OIC
          BTW VISIBLE "Field: " AN x AN "," AN y AN " has " AN neighbors AN " neighbors, value was: " AN current ...
          BTW   AN " is now: " AN row'Z SRS x AN ", because dead rules: " AN TehArrayFactory IZ having YR neighbors AN YR deadRules MKAY
        IM OUTTA YR colz
      IM OUTTA YR rowz
      ME'Z contentz R newBoard
      GTFO
    IF U SAY SO
  KTHX

  BTW *********************************************************************************
  BTW *********************************************************************************
  BTW moar helpers

  HOW IZ I drawingTehBoardOnTehGraphix
    EITHER OF ...
        DIFFRINT TehBoard'Z heigth AN Graphix'Z heigth AN ...
        DIFFRINT TehBoard'Z widht AN Graphix'Z widht
    O RLY?, YA RLY
      INVISIBLE "I IZ drawingTehBoardOnTehGraphix but has exeption: Board and Graphix dimensions r diffrnt!"
      GTFO
    OIC
    IM IN YR rowz UPPIN YR y TIL BOTH SAEM y AN TehBoard'Z heigth
      IM IN YR colz UPPIN YR x TIL BOTH SAEM x AN TehBoard'Z widht
        TehBoard IZ get YR x AN YR y MKAY, O RLY?
        YA RLY
          Graphix IZ putinPixel YR x AN YR y MKAY
        OIC
      IM OUTTA YR colz
    IM OUTTA YR rowz
  IF U SAY SO

  HOW IZ I sleepy
    IM IN YR nap UPPIN YR nrg TIL BOTH SAEM nrg AN 1000000
      PRODUKT OF nrg AN 1.1
    IM OUTTA YR nap
  IF U SAY SO
  
  BTW *********************************************************************************
  BTW *********************************************************************************
  BTW xript start

  TehBoard IZ maekBoard MKAY
  I IZ initingGraphix MKAY
  I HAS A spawnRulez ITZ TehArrayFactory IZ constructingTehShinyBrandNewArray MKAY
  I HAS A deadRulez  ITZ TehArrayFactory IZ constructingTehShinyBrandNewArray MKAY

  TehArrayFactory IZ adding YR 3 AN YR spawnRulez MKAY

  TehArrayFactory IZ adding YR 0 AN YR deadRulez MKAY
  TehArrayFactory IZ adding YR 1 AN YR deadRulez MKAY
  TehArrayFactory IZ adding YR 4 AN YR deadRulez MKAY
  TehArrayFactory IZ adding YR 5 AN YR deadRulez MKAY
  TehArrayFactory IZ adding YR 6 AN YR deadRulez MKAY
  TehArrayFactory IZ adding YR 7 AN YR deadRulez MKAY
  TehArrayFactory IZ adding YR 8 AN YR deadRulez MKAY

  BTW, test configs

  HOW IZ I settingR_pentomino
    TehBoard IZ set YR 11 AN YR 12 AN YR 1 MKAY
    TehBoard IZ set YR 12 AN YR 11 AN YR 1 MKAY
    TehBoard IZ set YR 12 AN YR 12 AN YR 1 MKAY
    TehBoard IZ set YR 12 AN YR 13 AN YR 1 MKAY
    TehBoard IZ set YR 13 AN YR 11 AN YR 1 MKAY
  IF U SAY SO

  HOW IZ I settingOscillator
    TehBoard IZ set YR 5 AN YR 4 AN YR 1 MKAY
    TehBoard IZ set YR 5 AN YR 5 AN YR 1 MKAY
    TehBoard IZ set YR 5 AN YR 6 AN YR 1 MKAY
  IF U SAY SO

  HOW IZ I settingSpaceshit
    TehBoard IZ set YR 3 AN YR 3 AN YR 1 MKAY
    TehBoard IZ set YR 4 AN YR 4 AN YR 1 MKAY
    TehBoard IZ set YR 4 AN YR 5 AN YR 1 MKAY
    TehBoard IZ set YR 3 AN YR 5 AN YR 1 MKAY
    TehBoard IZ set YR 2 AN YR 5 AN YR 1 MKAY

  IF U SAY SO

  BTW Graphix'Z clearingOption R FAIL
  
  I IZ settingR_pentomino MKAY

  IM IN YR loopie UPPIN YR i TIL BOTH SAEM i AN 200

    Graphix IZ startingNewScreen MKAY
    I IZ drawingTehBoardOnTehGraphix MKAY
    Graphix IZ visible MKAY

    TehBoard IZ calculaitink YR spawnRulez AN YR deadRulez MKAY
    
    I IZ sleepy MKAY    BTW, remove taht fo faster lolgame xperience

  IM OUTTA YR loopie

  
KTHXBYE GG WP
