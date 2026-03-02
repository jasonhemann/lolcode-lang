HAI "Dear curious test reader"

  BTW, not a test subject, itz just required
  O HAI IM TehRandomness
    I HAS A multiplier ITZ 16807
    I HAS A prime ITZ 2137
    I HAS A xD ITZ 999

    HOW IZ I absolute YR num
      BOTH SAEM 0 AN BIGGR OF 0 AN num, O RLY?
      YA RLY
        FOUND YR PRODUKT OF num AN -1
      NO WAI
        FOUND YR num
      OIC
    IF U SAY SO

    HOW IZ I generating YR min AN YR max
      ME'Z xD R PRODUKT OF ME'Z multiplier AN ME'Z xD
      ME'Z xD R MOD OF ME'Z xD AN ME'Z prime
      FOUND YR SUM OF MOD OF ME'Z xD AN DIFF OF max AN min  AN min
    IF U SAY SO

  KTHX

  BTW also not a test subject
  O HAI IM TehArrayFactory 

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
    BTW, another bugz bunny :(  if has 2 bukkitz in a parent BUTTKIT, then setting ONE inside member funxion does set BOTH of them!
    BTW, that's why I need external init funxion
    BTW, it worx fine for 'stylez' bukkit, bcs not in a funxion
    IM IN YR colz UPPIN YR x TIL BOTH SAEM x AN Graphix'Z widht
      I HAS A pixelCol ITZ A BUKKIT
      I HAS A screenCol ITZ A BUKKIT
      IM IN YR rowz UPPIN YR y TIL BOTH SAEM y AN Graphix'Z heigth
        screenCol HAS A SRS y ITZ 0
        I HAS A styleCount ITZ TehArrayFactory IZ sizing YR Graphix'Z stylez MKAY
        I HAS A random ITZ TehRandomness IZ generating YR 0 AN YR styleCount MKAY
        pixelCol HAS A SRS y ITZ Graphix'Z TehArrayFactory IZ geting YR random AN YR Graphix'Z stylez MKAY
      IM OUTTA YR rowz
      Graphix'Z pixelz HAS A SRS x ITZ pixelCol
      Graphix'Z screen HAS A SRS x ITZ screenCol
    IM OUTTA YR colz
    GTFO
  IF U SAY SO
  
  I IZ initingGraphix MKAY
  Graphix'Z clearingOption R FAIL
  
  VISIBLE "Test1: display all pixels - check randomnezz and dead pixelz"
  Graphix IZ testPrinting MKAY
  VISIBLE ":)"

  VISIBLE "Test2: display some pixelz"
  Graphix IZ startingNewScreen MKAY
  Graphix IZ putinPixel YR 10 AN YR 10 MKAY
  Graphix IZ putinPixel YR 11 AN YR 10 MKAY
  Graphix IZ putinPixel YR 10 AN YR 11 MKAY
  Graphix IZ putinPixel YR 11 AN YR 11 MKAY
  Graphix IZ putinPixel YR 15 AN YR 0 MKAY
  Graphix IZ putinPixel YR 0 AN YR 0 MKAY
  Graphix IZ putinPixel YR 29 AN YR 29 MKAY
  Graphix IZ visible MKAY
  VISIBLE ":)"

  VISIBLE "Test3: display some other pixelz"
  Graphix IZ startingNewScreen MKAY
  Graphix IZ putinPixel YR 10 AN YR 28 MKAY
  Graphix IZ putinPixel YR 9 AN YR 27 MKAY
  Graphix IZ putinPixel YR 8 AN YR 26 MKAY
  Graphix IZ putinPixel YR 8 AN YR 25 MKAY
  Graphix IZ putinPixel YR 9 AN YR 24 MKAY
  Graphix IZ putinPixel YR 10 AN YR 24 MKAY
  Graphix IZ putinPixel YR 11 AN YR 25 MKAY
  Graphix IZ putinPixel YR 11 AN YR 24 MKAY
  Graphix IZ putinPixel YR 11 AN YR 23 MKAY
  Graphix IZ putinPixel YR 11 AN YR 22 MKAY
  Graphix IZ putinPixel YR 11 AN YR 21 MKAY
  Graphix IZ putinPixel YR 11 AN YR 20 MKAY
  Graphix IZ putinPixel YR 11 AN YR 19 MKAY
  Graphix IZ putinPixel YR 11 AN YR 18 MKAY
  Graphix IZ putinPixel YR 11 AN YR 17 MKAY
  Graphix IZ putinPixel YR 11 AN YR 16 MKAY
  Graphix IZ putinPixel YR 12 AN YR 15 MKAY
  Graphix IZ putinPixel YR 13 AN YR 14 MKAY
  Graphix IZ putinPixel YR 14 AN YR 15 MKAY
  Graphix IZ putinPixel YR 15 AN YR 16 MKAY
  Graphix IZ putinPixel YR 15 AN YR 17 MKAY
  Graphix IZ putinPixel YR 15 AN YR 18 MKAY
  Graphix IZ putinPixel YR 15 AN YR 19 MKAY
  Graphix IZ putinPixel YR 15 AN YR 20 MKAY
  Graphix IZ putinPixel YR 15 AN YR 21 MKAY
  Graphix IZ putinPixel YR 15 AN YR 22 MKAY
  Graphix IZ putinPixel YR 15 AN YR 23 MKAY
  Graphix IZ putinPixel YR 15 AN YR 24 MKAY
  Graphix IZ putinPixel YR 15 AN YR 25 MKAY
  Graphix IZ putinPixel YR 16 AN YR 24 MKAY
  Graphix IZ putinPixel YR 17 AN YR 24 MKAY
  Graphix IZ putinPixel YR 18 AN YR 25 MKAY
  Graphix IZ putinPixel YR 18 AN YR 26 MKAY
  Graphix IZ putinPixel YR 17 AN YR 27 MKAY
  Graphix IZ putinPixel YR 16 AN YR 28 MKAY
  Graphix IZ visible MKAY
  VISIBLE "xD :)"


  BTW prints red: VISIBLE ":(001B)[31m"

OBTW
BLACK	\u001B[30m	BLACK_BACKGROUND	\u001B[40m
RED	\u001B[31m	RED_BACKGROUND	\u001B[41m
GREEN	\u001B[32m	GREEN_BACKGROUND	\u001B[42m
YELLOW	\u001B[33m	YELLOW_BACKGROUND	\u001B[43m
BLUE	\u001B[34m	BLUE_BACKGROUND	\u001B[44m
PURPLE	\u001B[35m	PURPLE_BACKGROUND	\u001B[45m
CYAN	\u001B[36m	CYAN_BACKGROUND	\u001B[46m
WHITE	\u001B[37m	WHITE_BACKGROUND	\u001B[47m
TLDR

OBTW





TLDR

KTHXBYE GL HF

