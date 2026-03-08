The things we resolved after the earlier “still unresolved” list.

The biggest new resolution is the mixin rule. We now have a coherent reading that fits both the formal rule and the `cheeze` example: a mixin contributes its effective visible slot interface, not just a bag of purely syntactic local declarations. The formal rule says that when mixins are used, “all slots defined on the mixin are copied” into the new bukkit in reverse order, and the `ZipFileRiver` example says this means: copy `ZipStuffz`, then `FileStuffz`, then replace the new object’s `parent` slot with `River`. The later `cheeze` example then says “all of cheeze and its parent slots are copied into slice.” The plain-meaning reconciliation is: mixin copying includes inherited-visible slots from the donor’s parent chain, donor-own slots beat donor-parent slots, mixins are applied right-to-left so the leftmost declared mixin wins, and only after that does the explicit declared parent overwrite the recipient’s `parent` slot.

That gives you a concrete test:

```lolcode
O HAI IM A
  I HAS A a ITZ "A"
KTHX

O HAI IM B IM LIEK A
  I HAS A b ITZ "B"
KTHX

I HAS A X ITZ A BUKKIT SMOOSH B

VISIBLE X'Z a
VISIBLE X'Z b
```

Expected output:

```text
A
B
```

Why this is the right test: if mixins copied only B’s own local slots, `X'Z a` would fail. But the `cheeze` comment is hard to read any way except “copy donor plus donor-parent-visible slots.”

The second new resolution is that mixins do copy special slots too. The spec says every bukkit contains special slots `parent`, `omgwtf`, and `izmakin`. The mixin rule says “all slots” on the mixin are copied. The `ZipFileRiver` example then singles out only one post-copy correction: replace the recipient’s `parent` slot with the explicit parent object `River`. Since the text explicitly mentions overwriting `parent` and says nothing analogous about `omgwtf` or `izmakin`, the plain reading is that copied `omgwtf` and `izmakin` survive normally, while copied `parent` is then overwritten by the declared parent. Among multiple mixins, reverse-order copy still decides which special slot wins; there is no extra special-slot exception beyond the later `parent` overwrite.

A good test for copied `omgwtf` is:

```lolcode
HOW IZ I fallback
  FOUND YR "from-mixin"
IF U SAY SO

O HAI IM M
  I HAS A omgwtf ITZ fallback
KTHX

I HAS A X ITZ A BUKKIT SMOOSH M
VISIBLE X'Z missing
```

Expected output:

```text
from-mixin
```

That test checks exactly the new point: the mixin-supplied `omgwtf` should be present on the recipient and should handle a missing slot, because nothing in the text resets `omgwtf` after mixin copy.

A corresponding test for mixin-supplied `izmakin` is:

```lolcode
HOW IZ I boot
  ME HAS A made ITZ WIN
IF U SAY SO

O HAI IM M
  I HAS A izmakin ITZ boot
KTHX

I HAS A X ITZ A BUKKIT SMOOSH M
VISIBLE X'Z made
```

Expected output:

```text
WIN
```

The reason is the same: mixin copy should bring over `izmakin`, and `izmakin` is the hook the spec says runs after a bukkit is fully prototyped. So mixins can inject construction behavior by ordinary slot copying, not by any extra hidden rule.

The third new resolution is that a plain `BUKKIT` starts with `parent = NOOB`. The path is straightforward. The declaration section says `I HAS A <object> ITZ A BUKKIT` creates an empty object with the default behavior of all bukkits. The special-slot section says every bukkit contains a `parent` slot. The inheritance section says parent-chain lookup stops when it reaches an object whose `parent` is `NOOB`. The clean plain meaning is therefore: the default `parent` of a non-inherited bukkit is `NOOB`.

That gives you this test:

```lolcode
I HAS A x ITZ A BUKKIT
VISIBLE BOTH SAEM x'Z parent AN NOOB
```

Expected output:

```text
WIN
```

The fourth new resolution is the slot-operator issue. Under the interpretive rule you are using, we should not discard the prose sentence. The draft literally says “Bukkit slots are accessed using the slot operator `-`,” and then immediately displays `'Z` and `'Z SRS <expression>`. The least-violent harmonization is: support hyphenated slot access as well as the displayed `'Z` spellings, rather than treating the prose as dead text. I would hand this to the implementer as “accept both spellings for slot access.” The displayed forms still tell you the semantics; the prose sentence tells you there is also a hyphenated spelling.

Because the concrete hyphen examples are not shown, the best regression target is simple equivalence:

```lolcode
VISIBLE obj'Z foo
VISIBLE obj-foo    BTW or the parser’s equivalent hyphen spelling
```

These should denote the same slot access.

The fifth new resolution is the interpretation of `I HAS A` inside object syntax. Inside `O HAI IM <object> ... KTHX`, the draft says that anything `I` inside the block actually refers to `<object>`, and identifiers inside the block are looked up by slot access first. So `I HAS A name ITZ "pikachu"` inside that block is not ordinary local-variable declaration; it is slot creation on the current object. Outside that block, `I HAS A` is ordinary declaration syntax. That double duty is not accidental; it is what the alternate syntax is for.

A test:

```lolcode
O HAI IM o
  I HAS A x ITZ 1
KTHX

VISIBLE o'Z x
```

Expected output:

```text
1
```

The sixth new resolution is a clarification of the function-namespace paragraph in the bukkit-function section. The sentence is badly written, but the example makes the intended core plain: in an object-called function, the function namespace consists of the parameters plus locals declared with `I HAS A` inside the function body; the receiver side is separate and is accessed via `ME` or via receiver-sensitive lookup; `ME HAS A` creates a slot on the calling object, and `ME'Z bar R bar` disambiguates receiver slot versus parameter/local. This matters because it sharpens the separation between function locals and object slots even before we solve the larger `IT` problem.

A useful test here is:

```lolcode
HOW IZ I fooin YR bar
  I HAS A bar2 ITZ "local"
  ME HAS A bar3 ITZ "slot"
  FOUND YR SMOOSH bar AN ":" AN bar2 AN ":" AN ME'Z bar3 MKAY
IF U SAY SO

O HAI IM o
  I HAS A fooin ITZ fooin
KTHX

VISIBLE o IZ fooin YR "arg" MKAY
```

Expected output:

```text
arg:local:slot
```

That checks the exact distinction the prose/example is trying to make.

The seventh new resolution is the mixin/`izmakin` interaction. We had left that open before. I would now hand it off this way: mixins interact with `izmakin` only through ordinary slot-copying. There is no separate mixin-specific constructor rule in the text. So whatever `izmakin` slot survives normal slot-copy conflict resolution on the newly constructed object is the one that runs after the object is fully prototyped. That is a direct consequence of “all slots copied,” reverse-order mixin application, and the independent statement that `izmakin` runs after prototyping.

This also gives you a precedence test:

```lolcode
HOW IZ I init1
  ME HAS A who ITZ "m1"
IF U SAY SO

HOW IZ I init2
  ME HAS A who ITZ "m2"
IF U SAY SO

O HAI IM M1
  I HAS A izmakin ITZ init1
KTHX

O HAI IM M2
  I HAS A izmakin ITZ init2
KTHX

I HAS A X ITZ A BUKKIT SMOOSH M1 AN M2
VISIBLE X'Z who
```

Expected output:

```text
m1
```

Why: `M2` is copied first, `M1` second, so the leftmost declared mixin wins and its `izmakin` survives.

What remains genuinely outstanding after these resolutions is much shorter.

The big one is still `IT` and the surrounding “global namespace” language. The bukkit-function section says lookup is function namespace, calling-object namespace, then “global” namespace, and says `IT` is always looked up from global namespace; earlier, the scope section says scope is local to function or main block and there is no global scope. That still needs one coherent rescue reading. Nothing we resolved above makes that disappear.

The other remaining live issue is the exact status of built-in type words like `YARN`, `NUMBR`, `NOOB`, and `TYPE` as identifiers. The spec clearly uses them as special type words and TYPE values, but still never separately says whether they are globally reserved or contextual only. That is still open.

If you want a very short implementer handoff version, it is this:

Mixins copy the donor’s effective visible slot set, including inherited-visible slots; donor-own beats donor-parent; mixins apply right-to-left so leftmost wins; special slots copy too; the explicit declared parent then overwrites only the recipient’s `parent` slot; plain `BUKKIT` starts with `parent = NOOB`; `I HAS A` inside `O HAI IM` creates receiver slots; function namespace in object-called functions means params plus `I HAS A` locals, with receiver slots on the `ME` side; and both hyphen and `'Z` should be accepted as slot-access spellings. The main open issues left are `IT`/“global namespace” and whether built-in type words are reserved or contextual.
