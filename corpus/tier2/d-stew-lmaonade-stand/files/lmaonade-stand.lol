HAI 1.4

  OBTW

    Lmaonade Stand

    A modern take on the classic game of supply and demand.

    Written in LOLCODE.

  TLDR

  I HAS A name ITZ A YARN
  I HAS A bank ITZ 20.00
  I HAS A cupP ITZ 1.00
  I HAS A lemonP ITZ 1.50
  I HAS A price 
  I HAS A demand
  I HAS A lemons ITZ A NUMBR
  I HAS A cups ITZ A NUMBR
  I HAS A spacing ITZ ":) :) :) :) :) :) :) :) :) :) :)"

  VISIBLE spacing
  
  VISIBLE "*********************************************"
  VISIBLE "*         Welcome to LMAONADE STAND         *"
  VISIBLE "********************************************* :)"

  VISIBLE spacing

  VISIBLE "First things first, young buck... :)"
  VISIBLE "Why don't you tell me your name before we get down to business? :)"

  VISIBLE "Enter name: :)"
  GIMMEH name

  VISIBLE spacing
  VISIBLE "Pleasure to meet you, :{name}! I'm Bucky. Let me tell you how all this works. :)"
  VISIBLE "Type SKIP to go straight to the supply store. :)"
  VISIBLE "Otherwise, press ENTER to keep moving through this short tutorial."

  I HAS A skip
  GIMMEH skip

  BOTH SAEM skip AN "SKIP", O RLY?
    YA RLY 
      VISIBLE "Skip!!!"
  OIC

  VISIBLE spacing

  VISIBLE "To get you started, I deposited $20.00 into your bank account. :)"
  VISIBLE "Before you can sell any lmaonade, you'll need to buy cups and lemons. :)"

  GIMMEH skip
  VISIBLE spacing

  VISIBLE "Cups cost $1.00 for a 10-pack. :)"
  VISIBLE "Lemons cost $1.50 each. Each lemon makes 5 servings of lmaonade. :)"
  VISIBLE "You can keep cups forever, but lemons go bad at the end of each day."

  GIMMEH skip
  VISIBLE spacing

  VISIBLE "CURRENT BANK BALANCE: $:{bank} :)"
  VISIBLE "TOTAL CUPS: :{cups} :)"
  VISIBLE "TOTAL LEMONS: :{lemons} :)"
  VISIBLE "How many 10-packs of cups do you want to buy? ($1.00 each)"


  I HAS A cupQ ITZ A NUMBAR
  GIMMEH cupQ
  VISIBLE spacing

  I HAS A cupCost ITZ PRODUKT OF cupQ AN cupP

  DIFFRINT cupCost AN SMALLR OF cupCost AN bank, O RLY?
    YA RLY
      VISIBLE "Insufficient funds! :{cupQ} cup packs cost $:{cupCost}. You have $:{bank}."
    NO WAI
      cups R SUM OF cups AN PRODUKT OF cupQ AN 10
      bank R DIFF OF bank AN cupCost
      VISIBLE ":{cupQ} 10-cup packs bought. Total cups: :{cups} :)" 
  OIC

  VISIBLE "Press ENTER to continue. Otherwise, type BACK to go back."

  GIMMEH skip
  VISIBLE spacing

  VISIBLE "CURRENT BANK BALANCE: $:{bank} :)"
  VISIBLE "TOTAL CUPS: :{cups} :)"
  VISIBLE "TOTAL LEMONS: :{lemons} :)"
  VISIBLE "How many lemons do you want to buy? ($1.50 each)"

  I HAS A lemonQ ITZ A NUMBAR
  GIMMEH lemonQ
  VISIBLE spacing

  I HAS A lemonCost ITZ PRODUKT OF lemonQ AN lemonP

  DIFFRINT lemonCost AN SMALLR OF lemonCost AN bank, O RLY?
    YA RLY
      VISIBLE "Insufficient funds! :{lemonQ} lemons cost $:{lemonCost}. You have $:{bank}."
    NO WAI
      lemons R SUM OF lemons AN lemonQ
      bank R DIFF OF bank AN lemonCost
      VISIBLE ":{lemonQ} lemons bought. Total lemons: :{lemons} :)" 
  OIC

  VISIBLE "Press ENTER to continue. Otherwise, type BACK to go back."

  GIMMEH skip
  VISIBLE spacing

  VISIBLE "CURRENT BANK BALANCE: $:{bank} :)"
  VISIBLE "TOTAL CUPS: :{cups} :)"
  VISIBLE "TOTAL LEMONS: :{lemons} :)"

  VISIBLE "Type BACK to return to store."
  VISIBLE "Press ENTER to continue."

  GIMMEH skip
  VISIBLE spacing

  VISIBLE "Okay! You're all set. A couple more things... :)"
  VISIBLE "Every day, you'll get a weather report. Hot, sunny days are prime time for lmaonade. :)"
  VISIBLE "After that, you'll be able to set your price. :)"

  GIMMEH skip
  VISIBLE spacing

  VISIBLE "You can set your price to be whatever you want. :)"
  VISIBLE "Lower prices drive up demand and are great for cold or rainy days. :)"
  VISIBLE "Higher prices are perfect for hot, sunny days. :)"

  GIMMEH skip
  VISIBLE spacing

  VISIBLE "Ready? Press ENTER to start Day 1"

  I HAS A weatherScore

  GIMMEH price
  VISIBLE spacing

  VISIBLE "PRICE SET AT $:{price} :)"
  VISIBLE "Press ENTER to continue. :)"
  VISIBLE "Otherwise, type BACK to go back."

  GIMMEH skip
  VISIBLE spacing

KTHXBYE 