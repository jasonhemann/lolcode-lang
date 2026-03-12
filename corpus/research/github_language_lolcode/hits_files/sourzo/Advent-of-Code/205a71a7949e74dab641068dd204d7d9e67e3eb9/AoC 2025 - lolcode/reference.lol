HAI 1.3
    OBTW
        There's a decent cheatsheet on the website learnxinyminutes.com/lolcode
        Since I'm using the lci interpreter, on the future branch, the best place for information
        is the lolcode spec v1.3 which you can find in the lci repo.

        At present I don't really want to rewrite everything that's in the above references,
        so this file focuses primarily on details that I don't think are clearly explained elsewhere.
        Although I am throwing a few basics in here as well, for my own reference.
    TLDR

    CAN HAS STDIO? BTW Loads the module. There's only 3 modules.
    CAN HAS STRING?
    CAN HAS STDLIB?
    BTW This is a single-line comment

    OBTW 
    This is a comment block
    Look at it, wheeee
    TLDR


    BTW declare a variable
    I HAS A var ITZ A YARN
    BTW assign a value to an already-existing variable
    var R "2"
    BTW declare and assign
    I HAS A nother_var ITZ "Kitty"
    BTW cast
    var IS NOW A NUMBR
    BTW print
    VISIBLE "Printing things to the terminal...."
    VISIBLE nother_var
    VISIBLE SUM OF var AN 5
    BTW Concatenation
    VISIBLE SMOOSH "The sum of 2 and 8 is " AN 10 MKAY
    BTW VISIBLE doesn't need the SMOOSH
    VISIBLE "The sum of 2 and 8 is " AN 10

    OBTW General syntax notes
    - Whitespace does not matter but it's polite to indent
    - Escape character is colon
    - You can use a comma instead of a new line. Stylistic uses include:
        - <TRUE_OR_FALSE_STATEMENT>, O RLY?
        - YA RLY, <SIMPLE_ACTION>
        - NO WAI, <SIMPLE_ACTION>
    - "IT" is whatever value was last produced but not assigned to anything, e.g.
        SUM OF 5 AN 5
        VISIBLE IT          BTW prints 10
    - "I" refers to the local scope (in the file, inside a function, inside a BUKKIT declaration, inside a loop)
    - "ME" refers to the object calling the function. 
        So a function declaration is
            HOW IZ <obj> <functionName> YR <arg1> etc
        And a function call is
            <obj> IZ <functionName> YR <arg1> etc
        And inside the function, if a BUKKIT called the function, you can say stuff like
            ME'Z name R "sourzo"        BTW to reassign a value
            ME HAS A age ITZ 256        BTW to declare & assign a property
            ME IZ addin YR 12 AN YR 42  BTW to call a function defined for the BUKKIT
    - Generally statements go on one line, but you can use a comma to put more than one statement on a line:
    (Each VISIBLE command prints on a new line)
    - If you see IZ in the code, it's a function call of the form <calling-object> IZ <function>
    TLDR
    VISIBLE "Look here's something:: ", I HAS A x ITZ 23, VISIBLE x

    BTW class definition
    O HAI IM className
        BTW stuff goes here
    KTHX

    BTW function definition
    HOW IZ I FUNCTION_NAME YR arg1 AN YR arg2 
        BTW stuff goes here, eg:
        I HAS A output ITZ SUM OF arg1 AN arg2
        BTW return statement
        FOUND YR output 
    IF U SAY SO

    BTW call function
    I IZ FUNCTION_NAME YR 2 AN YR 3 MKAY

    OBTW - "MKAY"
    Use MKAY at the end of SMOOSH statements and at the end of function calls
    Confusingly (I think so anyway), you don't use MKAY after operators
    TLDR

    BTW use a function from a module or BUKKIT
    BTW The new line character is a smiley :) as shown in lots of print statements below
    VISIBLE ":)Calling the LEN function from the STRING module..."
    VISIBLE I IZ STRING'Z LEN YR nother_var MKAY
    BTW General syntax: I IZ <CLASSNAME>'Z <FUNCTION> YR arg1 YR arg2 YR arg3 MKAY

    BTW input from console
    VISIBLE ":)Getting input from the console..."
    I HAS A kittyName
    VISIBLE "WATS UR NAME"
    GIMMEH kittyName
    
    BTW Control flow: If/Then/Else
    BOTH SAEM kittyName AN "WAFFLES", O RLY?    BTW if
        YA RLY                                  BTW then
            VISIBLE "IZ GREAT NAME"
        MEBBE BOTH SAEM kittyName AN "NEIL"     BTW else if
            VISIBLE "IZ TERRIBLE NAME"
        NO WAI                                  BTW else
            VISIBLE "HAI " AN kittyName
    OIC                                         BTW end if

    VISIBLE ":)Opening a file..."
    BTW Read a file
    I HAS A inputPath ITZ "TREATZ/1"
    I HAS A readFile ITZ I IZ STDIO'Z OPEN YR inputPath AN YR "r" MKAY
    BTW Check it worked
    I IZ STDIO'Z DIAF YR readFile MKAY          BTW DIAF = Die In A Fire. Lovely! Returns WIN/FAIL depending on whether there is an error
    O RLY?                                      BTW WIN/FAIL test on the last unassigned expression (which is the line above this one)
        YA RLY, VISIBLE "WHERE FIEL"                BTW file not found
        NO WAI, VISIBLE "THERE FIEL"                BTW file opened
    OIC

    	I HAS A output ITZ "a,b,c,3:)d,e,f,5:)g,h,i,8"
	I HAS A writeFile ITZ I IZ STDIO'Z OPEN YR "TOYZ/BITZ_OF_YARN/writeOut" AN YR "w" MKAY
                                                            BTW ^^^ Open file for writing
    BTW Writing to a file
	I IZ STDIO'Z DIAF YR writeFile MKAY, O RLY?             BTW Check for errors
        YA RLY, VISIBLE "WHERE FIEL"                        BTW file not found
        NO WAI, VISIBLE "THERE FIEL"                        BTW file opened
	OIC
	I IZ STDIO'Z SCRIBBEL YR writeFile AN YR output MKAY    BTW Write to the file
	I IZ STDIO'Z SCRIBBEL YR writeFile AN YR "More text on same line" MKAY
	I IZ STDIO'Z SCRIBBEL YR writeFile AN YR ":)Write on a new line" MKAY
	I IZ STDIO'Z CLOSE YR writeFile MKAY                    BTW Close the file

    OBTW
    STDIO has the following functions:
        OPEN - open a file
        DIAF - check for error (WIN/FAIL)
        LUK - read a file
        SCRIBBEL - write to a file
        AGEIN - reset the file pointer to the beginning (Calls C's rewind function)
        CLOSE - close a file
    TLDR
    
    BTW An important bit of metaprogramming! SRS turns a value into a var name
    VISIBLE ":)Testing the SRS token to see what it does..."
    I HAS A SRS "fjsnfgosngj" ITZ 123
    VISIBLE "SRS returns " AN fjsnfgosngj

    OBTW 
    The BUKKIT (container object? class?)
    You can assign properties to it
    You can also assign functions to it
    To get the value of a property, the syntax is <bukkitObject>'Z <propertyThing>
    To call a function, it's <bukkitObject>'Z I IZ <functionThing> YR .... MKAY
    TLDR

    VISIBLE ":)Bukkits! How do they work?"
    I HAS A book1 ITZ A BUKKIT
    book1 HAS A pageCount ITZ 300        BTW Remember this is declaration & assignment
    book1 HAS A bookmark ITZ 144         BTW you can only declare a variable that doesn't exist
    book1 HAS A title ITZ "Famous Cats of History"
    
    BTW access an attribute of a BUKKIT
    VISIBLE book1'Z title
    BTW reassign a value
    book1'Z title R "Famous Domestic Cats of History"

    O HAI IM book2
        I HAS A pageCount ITZ 9999
        I HAS A bookmark ITZ 4
        I HAS A title ITZ "Famous Cats of History vol 2"
    KTHX

    BTW you can also define functions in BUKKITz.
    BTW note that "I" in "HOW IZ I" can be substituted for a specific BUKKIT
    HOW IZ book2 TURN_PAGE
        BTW Increases the value for bookmark by 1
        I HAS A page_amount ITZ 1                               BTW "I" here is the local scope
        ME'Z bookmark R SUM OF ME'Z bookmark AN page_amount     BTW 'ME' refers to the calling BUKKIT (book2 in this case)
    IF U SAY SO

    VISIBLE "book2's bookmark:: " book2'Z bookmark
    book2 IZ TURN_PAGE MKAY
    VISIBLE "book2's bookmark:: " book2'Z bookmark
    OBTW use 'book2' instead of 'I' because the function is defined on book2, 
    not the local scope (which in this instance is the whole .lol file)
    TLDR

    OBTW
        Most importantly, you can treat it like an array by creating a variable for each index
        You use SRS to assign values
    TLDR

    VISIBLE ":)Arrays, which are really just BUKKITs"
    I HAS A squareNumbersArray ITZ A BUKKIT
    IM IN YR arrayLoop UPPIN YR idx TIL BOTH SAEM idx AN 5
        squareNumbersArray HAS A SRS idx ITZ PRODUKT OF idx AN idx
        BTW this creates variables inside array called 0, 1, 2, 3, 4 and 5
        BTW which in this example all just have the value "blahblahblah"
    IM OUTTA YR arrayLoop

    VISIBLE "Element 4:: " AN squareNumbersArray'Z SRS 4


    OBTW Inheritance
        You can inherit from BUKKITZ, but (at least for me) it works a bit weirdly.
        Suppose you have the following:
    TLDR
        I HAS A b1 ITZ A BUKKIT
        b1 HAS A greeting ITZ "hello"
        I HAS A b2 ITZ LIEK A b1

        BTW Now b2 sort-of inherits the property 'greeting', except not really.
        BTW To access the property, you have to use 'Z notation:
        VISIBLE ":)b1's greeting is:: " AN b1'Z greeting
        VISIBLE "b2's greeting is:: " AN b2'Z greeting
        OBTW except... b2 doesn't actually have this property.
        Since that property doesn't exist on b2, and b2 inherits from b1, the interpreter
        looks to b1 to find the property and returns the value for b1'Z greeting. When
        you change the value for either BUKKIT, it changes for both BUKKITz. Like so:
        TLDR
        b2'Z greeting R "goodbye"
        VISIBLE ":)b1's greeting is now:: " AN b1'Z greeting
        VISIBLE "b2's greeting is now:: " AN b2'Z greeting

        b1'Z greeting R "no wait I forgot my keys"
        VISIBLE ":)b1's greeting is now:: " AN b1'Z greeting
        VISIBLE "b2's greeting is now:: " AN b2'Z greeting

        BTW If you uncomment the following line, you'll see that you can't re-declare a variable as you get an error:
        BTW b1 HAS A greeting ITZ "bonjour"

        BTW However the following line does work, and assigns a separate value for b2:
        b2 HAS A greeting ITZ "au revoir"
        VISIBLE ":)b1's greeting is now:: " AN b1'Z greeting
        VISIBLE "b2's greeting is now:: " AN b2'Z greeting

        BTW and now if you change either one, it only affects the one you changed:
        b2'Z greeting R "auf wiedersehen"
        VISIBLE ":)b1's greeting is now:: " AN b1'Z greeting
        VISIBLE "b2's greeting is now:: " AN b2'Z greeting

        b1'Z greeting R "guten tag"
        VISIBLE ":)b1's greeting is now:: " AN b1'Z greeting
        VISIBLE "b2's greeting is now:: " AN b2'Z greeting


    OBTW 
    The STRING package only has 2 functions: LEN and AT
    TLDR

    VISIBLE ":)The STRING package"
    VISIBLE "Length: " AN I IZ STRING'Z LEN YR "Whiskas" MKAY
    BTW indexing from zero.
    VISIBLE "Character 1: " AN I IZ STRING'Z AT YR "Whiskas" AN YR 1 MKAY

    OBTW 
    STDLIB: Random numbers (kinda)
    
    The BLOW function generates the next pseudo-random number in a sequence.
    The MIX function sets a seed to change the starting point of the sequence. 
    TLDR
    I IZ STDLIB'Z MIX YR 12 MKAY            BTW Sets a seed for the pseudorandom number (chooses the starting point in the sequence)
    VISIBLE I IZ STDLIB'Z BLOW YR 12 MKAY   BTW Gives a pseudorandom number up to 12 using the new seed

OBTW

Things that are missing from this implementation of LOLCODE
 - System time (without which you can't do a timer, or pseudorandomly seeded pseudorandom numbers)
 - Reflection on primitives (e.g. name of var, type of var, check if something is null, etc) 
 - Error handling. Try/catch would be nice. Exceptions too.
 - Stack trace


Things that are missing but could just about be coded in
 - Square root operator
 - Numbered arrays, basic get/set methods, sorting
 - Reflection on BUKKITz

TLDR

KTHXBYE