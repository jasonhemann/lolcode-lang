Can these two pieces combine together to cause trouble:

"
* Multiple commands can be put on a single line if they are separated by a comma (,). In this case, the comma acts as a virtual newline or a soft-command-break.

* Multiple lines can be combined into a single command by including three periods (...) or the unicode ellipsis character (u2026) at the end of the line. This causes the contents of the next line to be evaluated as if it were on the same line.
"

"
* Lines with line continuation can be strung together, many in a row, to allow a single command to stretch over more than one or two lines. As long as each line is ended with three periods, the next line is included, until a line without three periods is reached, at which point, the entire command may be processed.
" 

This means we do not begin calculating until we have the entire statement. Right. That's true for our lexing parsing eval. right?

"* A line with line continuation may not be followed by an empty line.
Three periods may be by themselves on a single line, in which case, the empty line is "included" in the command (doing nothing), and the next line is included as well.
"
What if we do ... on the first or second line. What if the only thing we have in the file is HAI 1.3 KTHXBYE ... ? 

How do comments interact with the dot-dot-dot ? If we have dot-dot-dot before the end of the line what happens. What happens if we have a dot-dot-dot in a comment?

A LOLCODE file is closed by the keyword `KTHXBYE` which closes the `HAI` code-block. --- have we ensured that this works in a single otherwise-empty one-line file, HAI 1.3, KTHXBYE ? 

"
### Scope

*(to be revisited and refined)*

All variable scope, as of this version, is local to the enclosing function or to the main program block. Variables are only accessible after declaration, and there is no global scope.

" 

What do we do about this. does that mean that there is no object-level scope? 

"
```
HOW DUZ I var YR stuff
	BTW implement
IF U SAY SO

I HAS A var ITZ 0  BTW Throws an error AS var is already taken

var R 0 BTW FUNIKSHUN var no longer exists, it's now NUMBR-0
```
"

We do something to ensure that no duplicate variables are created, and that that's an error? 

I see from 

"

Function types are declared/initialized using the HOW DUZ I / IF U SAY SO blocks, however they behave the same as variables. For example:

```
HOW DUZ I var YR stuff
	BTW implement
IF U SAY SO

I HAS A var ITZ 0  BTW Throws an error AS var is already taken

var R 0 BTW FUNIKSHUN var no longer exists, it's now NUMBR-0
" that vars and functions share the same namespace. But also this seems contradictory, because we throw an error but the program proceeds because we appear to have nonetheless executed the assignment, because later it says now var is NUMBR-0 

Is "AS" a keyword? It seems like it? 

We need to ensure also that once a value's last reference has been mutated to NOOB, that it will be GC'd:


```
<variable> R NOOB
 ```

This above code ensures that a variable no longer references anything. The reference still exists on the current scope and still requires a small amount of memory. If this was the last reference to an object, it will be garbage collected in the future.

Do we do that? 

Spec says that "All primitive types are considered Immutable. All built in operations return new objects instead of references to old objects." So what are those operations? Does that count for numbers? I could imagine it for strings, but does the loose typing and coercions mean that we need to worry about different boxes for each number? 

Spec says said "The A becomes optional in variable declaration" is that the only place that "A" comes up as an article in code? Are there other places spec says it's used?

What happens if you try and assign to a variable that hasn't been declared? What does the spec say wil/should happen?

It says we're reserving arrays "(Arrays (BUKKIT) are reserved for future expansion.)"---but that doesn't show up here? Do we currently implement BUKKIT? Should we? 

I'm confused here by what spec says:

 ~~Casting operations operate on TYPE types, as well.~~

### Untyped

The untyped type (NOOB) cannot be implicitly cast into any type except a TROOF. 

We are casting not the untyped type's only _value_, but we're saying that we can implictly cast the untyped _type_, types are apparently values, so NOOB :: Type, into  FAIL :: TROOF. Is that what that's saying. 

In my IDE  ~~Casting operations operate on TYPE types, as well.~~ looks like it's struck out, but I think that's really supposed to be outlining or underlining or highlighting the importance because it says casting of types in the immediately following section.


"The two boolean (TROOF) values are WIN (true) and FAIL (false). The empty string (""), an empty array, and numerical zero are all cast to FAIL. All other values evaluate to WIN." Strictly speaking, that seems in tension at least with what we've said before right? So we are saying that the _type_ NOOB :: TYPE, interpreted as a boolean, is FAIL, but the *value* NOOB :: NOOB, must be interpreted as a boolean as WIN. Is that right? 

Also, we said that we're deferring BUKKITs, but the spec mentions an empty array. I guess if we can't build them, then we vacuously implement the behavior of translating them to FAIL booleans. but I *swore* that there was some kind of objects in the most up to date spec, and that was critical to our intended use case.

"Any contiguous sequence of digits outside of a quoted YARN and not containing a decimal point (.) is considered a NUMBR. A NUMBR may have a leading hyphen (-) to signify a negative number." So we presumably mean contiguous non-empty sequence of digits outside fo a quoted YARN. 

"It is represented as a contiguous string of digits containing exactly one decimal point. " when we say "containing" does that seem to mean that we cannot write "2." as a NUMBAR, because the decimal isn't "contained" and we need to have "2.0" if we want a whole number. 

" Casting a NUMBAR to a NUMBR truncates the decimal portion of the floating point number. Casting a NUMBAR to a YARN (by printing it, for example), truncates the output to a default of two decimal places." it doesn't say how the decimal portion of the floating point number is truncated. Truncate I assume means drop the post decimal part. So negative numbers get closer to zero, positive numebers get closer to zero. Do we make sure that we get -0.567 goes to 0? 

Have we ensured we got the hex coding correct?

"* :(`<hex>`) resolves the hex number into the corresponding Unicode code point."

We are going to proceed with this part of the spec as written:

"
The TYPE type only has the values of TROOF, NOOB, NUMBR, NUMBAR, YARN, and TYPE, as bare words. They may be legally cast to TROOF (all true except for NOOB) or YARN.
"

"In cases where operators have variable arity, the operation is closed with `MKAY`. An `MKAY` may be omitted if it coincides with the end of the line/statement, in which case the EOL stands in for as many `MKAYs` as there are open variadic functions."

This seems to indicate variatic operators---are these only primitives or are they user-defined in spec. How does the "coincides with the end of the line/statement," adjudicate when the EOL isn't the end of the statement (b/c dot-dot-dots?).

When we have an MKAY and two open variadic, the MKAY presumably closes the most *recently* opened variadic? 

Prove to me that we have the right behavior for two open variadics on one line, nested, and that we do in fact get the right closure property from EOL, and also that we get the right behavior when we use a comma and have multiple open variadics even though that's not the end of the line.

Make sure that we have the parsing accept AN in operators as "optional" <operator> <expression1> [AN] <expression2>.

How do we do string comparisons? The spec says:

"

```
BOTH SAEM <x> [AN] <y>   BTW WIN iff x == y
DIFFRINT <x> [AN] <y>    BTW WIN iff x != y
```

Comparisons are performed as integer math in the presence of two NUMBRs, but if either of the expressions are NUMBARs, then floating point math takes over. Otherwise, there is no automatic casting in the equality, so `BOTH SAEM "3" AN 3` is FAIL.
"

but we also said that all types are immutable, and I think that all things are by-value, no reference. 

Let's cofirm this part:

"
```
MAEK <expression> [A] <type>
```

Where `<type>` is one of TROOF, YARN, NUMBR, NUMBAR, or NOOB. This is only for local casting: only the resultant value is cast, not the underlying variable(s), if any."

If indeed we have a variable of a given type, and we have a MAEK, where the expression is the name of that variable, let's ensure that the underlying type of that variable hasn't been changed. So we'll be sure that, for instance 

I HAZ A foo ITZ A  BTW 2.0

I HAZ A bar ITZ MAEK foo A NUMBR. 

VISIBLE FOO (make sure we get 2.0 back out of here)


And another question, how do we know what type to give a variable when we create it? I HAZ A foo ITZ 2 . values get implicitly coerced? So it seems like it would be to spec to make it a YARN "2", a NUMBR 2, a TROOF WIN, or a NUMBAR 2.0, and like that would be up to the implementation? Is that right??

And how about this:

"The print (to STDOUT or the terminal) operator is `VISIBLE`. It has infinite arity and implicitly concatenates all of its arguments after casting them to YARNs. It is terminated by the statement delimiter (line end or comma). The output is automatically terminated with a carriage return (:)), unless the final token is terminated with an exclamation point (!), in which case the carriage return is suppressed."

How deos that "end of line" interact with the dot-dot-dot operator signalling the line continues? 

How does the "IT is always global" we discussed square with 
"`IT`'s value remains in local scope " 

in 

"
A bare expression (e.g. a function call or math operation), without any assignment, is a legal statement in LOLCODE. Aside from any side-effects from the expression when evaluated, the final value is placed in the temporary variable `IT`. `IT`'s value remains in local scope and exists until the next time it is replaced with a bare expression.

Our choice seems inconsistent with spec. Right? No? 

They write about assignment: "<variable> <assignment operator> <expression>" --- but what *is* the assignment operator? Is that written?

Can we ensure that the function calls are affecting the same IT that's being implicitly manipulated by our loops? Like it says here:

"
The traditional if/then construct is a very simple construct operating on the implicit `IT` variable. In the base form, there are four keywords: `O RLY?`, `YA RLY`, `NO WAI`, and `OIC`.

`O RLY?` branches to the block begun with `YA RLY` if `IT` can be cast to WIN, and branches to the `NO WAI` block if `IT` is FAIL. The code block introduced with `YA RLY` is implicitly closed when `NO WAI` is reached. The `NO WAI` block is closed with `OIC`. The general form is then as follows:"

Here's another q: "
The elseif construction adds a little bit of complexity. Optional `MEBBE <expression>` blocks may appear between the YA RLY and NO WAI blocks. If the `<expression>` following `MEBBE` is WIN, then that block is performed; if not, the block is skipped until the following `MEBBE`, `NO WAI`, or `OIC`. The full expression syntax is then as follows:
" --- do we ensure that there must be a NO WAI block at the end of the case block? 

Do we make sure we distinguish between YARN variables and teh format-string like things?

(A literal, in this case, excludes any YARN containing variable interpolation (`:{var}`).)

Do we get an error if we use a YARN with a variable interpolation? What about if we have a double-colon in there escaping the literal colon so it looks superficially *like* a variable interpolation but it isn't because of the escape. Do we get that right?

Do we check that in the WTF? that the literals are unique? It says in spec we must: " Each literal must be unique. "
I want to see the test that we do something about that. I guess it doesn't say in spec what happens if you violate that, but I don't know what I'd want to do *except* throw an error. I guess you could also let the program proceed until you *reach* the second duplicate one, at which point you might signal an error? 

And I have another question:

"which breaks to the end of the the `WTF` statement. If an `OMG` block is not terminated by a `GTFO`, then the next `OMG` block is executed as is the next until a `GTFO` or the end of the `WTF` block is reached. The optional default case, if none of the literals evaluate as true, is signified by `OMGWTF`." If one of them signals an error, then that should *stop*? or should they continue to execute until the end of the OMGWTF? 

Let's also confirm that we allow blank blocks in WTF?, like they show in spec (e.g.   OMG "G").

Let's also have a test to ensure that when we create a new loop-local variable that's shadowing, and doesn't affect outrer scope. It says in spec that we must: "Where <operation> may be UPPIN (increment by one), NERFIN (decrement by one), or any unary function. That operation/function is applied to the <variable>, which is temporary, and local to the loop."

When it says here "The `<argument>`s are single-word identifiers that act as variables within the scope of the function's code. " --- does that imply that there are multiple-word identifiers that can act as variables within the scope of the functions code? 

Let's mkae sure we have tests for both of these behaviors for the function call:

* `GTFO` returns with no value (NOOB).
* in the absence of any explicit break, when the end of the code block is reached (`IF U SAY SO`), the value in `IT` is returned.

The right behavior of the implicit IT is important to get right. 

Also this says something about the "I" parameter. Is that another actual implicit parameter? Or what does that imply:

"The I parameter is used to distingish a function call on the current namespace vs. a function call on a bukkit (defined below)."

Let's make sure we have a test demonstrating we follow "
A slot may be declared/initialized more than once, however doing so only changes the value the slot references." correctly.

Also let's make sure that this is an expression position: "This places the value returned from expression (could be another object) into the slot identified by slotname. The slot name may be any identifier (or SRS BIZNUS cast). Note: This identifier may be a function." for the bukkit. 

This statement: " Note: This identifier may be a function." in the spec seems like its a mistake. I think they mean to say that the expression could evaluate to a procedure. Because functions aren't ordinary expressions, right? Like I can't do an application of a dynamically created procedure on a value, right?) The equivalen of a racket syntax for something like: ((begin (define (f x) (add1 x)) f) 5)  ; that doesn't actually work I bet.

Let's also make sure that we have a slotname figured out by a srs business cast, like it mentions in spec: "The slot name may be any identifier (or SRS BIZNUS cast)". I want to see that we have an example of that.

Let's make sure that this function-in-bukkit syntax is covered and works:

HOW IZ <object> <slot> (YR <argument>)*
( <statements> )*
IF U SAY SO

Can we have functions creating functions in this context? Does it work what would happen?

Let's make sure that we have checked all of these in order. We didn't give the full rules up top about scope, which made me confused. But I now understand I think what the general case is:

"
Functions operate differently in the context of bukkits. When a function is called from an object, some scope rules and variable resolution change.

When an identifier is used in a function, the variable is looked up in the following manner:

* The function namespace
* The calling object's namespace (if called from object)
* The “global” namespace
"

I don't think that we talked about all of those; let's make sure that we do. 

What does this mean: *IT is always looked up from global namespace*" in that context. Because I thought we said "IT was local scope", when we talked about functions? 

Have we put ME in the language parser and checked this behavior:

"
ME is an identifier used to access the calling object of a function. If there is no calling object, access to ME throws an exception.

Declaring a variable on the calling objects namespace is done as follows:

```
HOW IZ I fooin YR bar
    ME HAS A bar2
    BTW bar2 is now a slot on calling object
IF U SAY SO
```

ME can also be used to explicitly use a slot variable vs. a function namespace variable.
"

So we also need to use that to access object variables instead of object method parameters.

What does the optional IM LIEK mean?

"O HAI IM <object> [IM LIEK <parent>]
  <code-block>
KTHX"

Is that syntax for describing inheritance? How do you call the equivalent of "super" or parent object. Are we sure we get lookup correctly? And how does mutation of a parents field from a child affect the parent. Do we have a test for that? 

Our version of the spec says the slot operator is that dash. But that seems odd. is that correct or an artifact of our download?

"Bukkit slots are accessed using the slot operator ”-”.

```
<object> 'Z <slotname>
 ```

 or indirectly using the Srs operator

```
<object> 'Z SRS <expression>
```

Slot access is very important to function calls.  To call a function on an object:

```
<object> IZ <slotname> (YR <variable> (AN YR <variable)*)? MKAY
```

combined with the Srs operator allows the following:"

What happens if the slotname isn't a function. Do we have a check for that? 

This is a really great example, and we need to make sure we have it in our tests:

"HOW IZ I getin YR object AN YR varName
	I HAS A funcName ITZ SMOOSH "get" AN varName MKAY
	FOUND YR object IZ SRS funcName MKAY
IF U SAY SO
" Honestly, probably all the program snippets that could easily be transformed into full programs should be, and added to our test suite as those full programs. 

Let's check what the default behavior we have for omgwtf is, and also an eaxmple where we override that behavior, and get a missing field to override. 

And detail question:
"`omgwtf` refers to a method that is called when slot access fails. This method should return a variable (that will be placed in the unknown slot) or throw an exception. The default implementation of canhas is to always throw an exception."

What do we mean by "slot access fails". If the slot exists, but the value isn't a function, should omgwtf get called? Or no?

Let's make sure we have an example of objects mutating their parent slot, as described: "that a Bukkit may change its “parent”/“prototype” by changing its parent slot. More on this later."

This points to an object who is its own parent, or objects who are aech other's parent: 

"Accessing a variable from within the current object looks for that variable within the current object. If it is not found, it searches for the variable within the parent object (using the parent slot), and on up the chain of parents until it reaches an object where the parent slot is NOOB or it reaches a parent object is has already searched before."

Let's make sure we check for cycles in our implementation, and we fix it. 

Also, when we discuss the omgwtf "slot lookup failure", and this parent lookup behavior and they coincide, what does that mean? Do we do the omgwtf behavior for each object slot lookup, and only if the error happens do we catch the error, and proceed with the parent? Or do we not do the omgwtf if there _is_ a parent? When none of the ancestors or have the field name, do we call the original object's omgwtf, or the most distant ancestor's omgwtf? And what happens if the slot lookup fails, but we *do* have that variable in global environment? Do we not omgwtf if there's a global with that name? Or am I confusing something about slot lookup? 

This seems like an example of something that we need to have a test for:

"
Assigning a variable within the object first searches for it within the current object. If it has been declared within the current object, then it is set. If that fails, it attempts to access it within the parent object. Search continues in up the chain of parents. If the variable name is found up the inheritance chain, then that variable is declared and created within the current object (where the search started), and the value is set. If the variable search fails and the variable was never previously assigned, then it's a declaration error." Specifically the "if it's in the hierarchy but not us, we declare it here", and it makes me worry about cycles, because determining the variable name existence isn't the same as a lookup, but it seems like we're implicitly saying that, if this isn't nonsense, the "does the variable name exist" lookup has to also have that "have we been here before?" cycle check too.

Also, we need a test that signals that declaration error.

The term " a Slot-Access Function call" seems like a term of art something we should be able to separately represent in the AST, because aren't they fundamentally different semantically knids of things? 

I just literally can't understand the English that this is saying "the Function obtains variables from the object it was accessed from."

Oh, I get it now. We need this example in our tests:

"
```
HOW IZ I funkin YR shun ?
	VISIBLE SMOOSH prefix AN shun MKAY
IF U SAY SO

O HAI IM parentClass
	I HAS A prefix ITZ "parentClass-"
	I HAS A funkin ITZ funkin    BTW Pulls funk from global scope
KTHX


O HAI IM testClass IM LIEK parentClass
	I HAS A prefix ITZ "testClass-"
KTHX

parentClass IZ funkin YR "HAI" MKAY        BTW parentClass-HAI
testClass IZ funkin YR "HAI" MKAY            BTW testClass-HAI
```"

Let's also make sure we test the mixin inheritance and that we check all the nasty cases:

"
This copies all slots from ZipStuffz into ZipFileRiver, then all slots from FileStuffz into ZipFileRiver, then replaces the parent slot with a reference to River.

Mixin-Inheritance is static. It can only pull in slots that are defined when the mixin takes place. If the FileStuffz or ZipStuffz objects change after the ZipFileRiver object is defined, the ZipFileRiver class does not see the change.
"

What if we try and mixin from a parent and its child, or vica versa? Do we get all that right? Show me with the test.

