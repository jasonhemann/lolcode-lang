The spec defines identifier syntax, but never separately reserves keywords, literals, or special names. So collisions like user identifiers versus WIN, FAIL, IT, ME, or control keywords are left to the implementation.

It never gives a longest-match rule for multiword keywords. Since spaces are token separators but many constructs are themselves space-containing phrases, lexer/parser coordination is underspecified.

The preprocessing order among comma-as-newline, ellipsis continuation, comment stripping, and string shielding is not specified. Different orders produce different token streams.

OBTW/TLDR placement is phrased with “should,” not “must,” so mid-command block comments are not actually ruled out normatively.

TLDR, code is explicitly valid, so block-comment termination is not statement termination. The handoff back into normal parsing needs a precise rule and does not get one.

HAI version handling is explicitly left without a standard behavior. Whether to require, ignore, warn on, or reject version mismatches is open.

The line-continuation rule recognizes ... or Unicode ellipsis “at the end of the line,” but never says whether trailing spaces or trailing comments after them are tolerated.

Bare literals like WIN, FAIL, NOOB, and TYPE words like YARN are given value status, but the identifier section never reserves them. Literal-vs-identifier tokenization is therefore partly inferred, not stated.

Truthiness mentions “empty array” while the earlier type section still says BUKKIT is reserved for future expansion, and later sections fully define BUKKITs. Truthiness of empty BUKKITs is therefore muddy rather than nailed down.

NUMBR and NUMBAR are host-defined. That leaves overflow, underflow, infinities, NaNs, and division-by-zero behavior non-portable unless the implementation adds policy the spec never gives.

Numeric literal syntax still leaves edge forms like .5, 2., -.5, and -0. unsettled. “Containing exactly one decimal point” is not a full lexical grammar.

String-to-number casting bans bad characters, but not bad placement or multiplicity of - and .. A permissive implementation could accept junk strings the prose clearly did not think through.

String-escape failure modes are absent: malformed hex, unknown Unicode name, out-of-range code point, malformed interpolation delimiters, and so on.

TYPE is admitted as a value type and then immediately marked “under current review,” with type comparisons explicitly unresolved. That forces implementers to invent policy in a load-bearing area.

Variadic closure lacks an explicit stack-discipline rule when explicit MKAY and implicit end-of-statement closure mix. The prose implies nesting behavior, but does not define it.

VISIBLE is not just another variadic operator: it closes on the statement delimiter rather than MKAY. Combined with line splicing, “line end” is really “logical statement end,” but the spec never says that outright.

The trailing ! on VISIBLE is special suffix punctuation with one local meaning, but the spec never says whether it is lexed as its own token or attached to the final expression token.

The spec never says what value VISIBLE produces. That matters because bare expressions write IT, and functions without FOUND YR return the final IT.

GIMMEH has the same hole. It is described operationally as input, not as an expression, but default function return and IT semantics make its result matter if it is the last executed form in a function.

Neither x R expr nor I HAS A x ITZ expr says whether the left-hand binding exists before the right side is evaluated. That is observable when expr reads or mutates x.

There is no closed list of which statement classes preserve IT. Since O RLY?, WTF?, and implicit function return all depend on IT, that omission is semantically expensive.

Default function return via IT means the value status of the last executed statement matters, yet many statement forms are specified only operationally, not as value-producing or value-less constructs.

GTFO has specified roles inside WTF?, loops, and functions, but the spec never gives a failure mode for top-level or otherwise out-of-context GTFO.

“Variables are only accessible after declaration” plus “functions behave the same as variables” strongly suggests forward function calls might be illegal, but the call section never says one way or the other.

Duplicate parameter names in a function definition are never forbidden or resolved, even though the spec is explicit elsewhere that names inhabit a shared namespace model.

The ordinary function section says functions do not see outer/calling variables, but the bukkit-function section reintroduces global fallback and receiver-sensitive lookup. Those are two different function semantics, not one.

Argument evaluation order is only “obtained before the function is called,” not left-to-right. With mutation or I/O in argument expressions, different evaluators can disagree on results.

The spec never says whether function definitions are declarations only, executable statements, or expressions. That affects whether they can appear conditionally, in loops, or inside other functions, and whether they affect IT.

O HAI IM says anything I inside the block refers to the object, but never formalizes whether HOW IZ I name there is method-slot definition sugar or just an ordinary function definition textually nested in an object block. The example implies one thing; the grammar never states it.

ME HAS A slot is shown as receiver-slot declaration, but the spec does not say whether it always creates/shadows on the current receiver or may overwrite an inherited slot in place.

ME'Z slot R expr lacks a sequencing rule. That matters if expr itself touches the same slot, or if writing the slot creates a new shadow binding before expr is finished.

Mixins say slots are “copied,” but never say whether copied mutable BUKKIT values are deep-cloned or shallow aliases. With mutation, that is immediately observable behavior.

More generally, the memory model says variables are references, so function arguments and slot assignments appear to be call-by-sharing for mutable BUKKITs, but the spec never states that policy explicitly.

The spec allows mutating the special parent slot, but never says what happens if parent is set to NOOB, a primitive, or some non-BUKKIT value. Parent-chain lookup then has no defined domain.

omgwtf installs whatever it returns into the missing slot, but the call path is silent: if obj IZ missing MKAY triggers omgwtf and the synthesized value is not a function, do you retry the call or fail immediately?

izmakin timing is described relative to “fully prototyped” and “before the prototyping method returns,” but not relative to mixin-copy order, object-body execution order, or visibility of partially initialized state.

If izmakin throws, the spec does not say whether the target variable remains bound to a partial object or whether construction is atomic and the binding never happens.

The parent-chain access rule includes cycle stopping, but the assignment rule also does an ancestor search before creating a local shadow slot. The prose never explicitly says that this second search must use the same visited-set discipline, even though it obviously must.

LIEK A inheritance, static SMOOSH mixins, and receiver-rebinding slot-call semantics are three different object models composed in one section. The spec never states a single composition order for them.

Slots are said to be keyed by NUMBR or YARN, but direct slot syntax only gives identifier or SRS <expression> names. Numeric-literal slot access is therefore only implicit, not actually defined as surface syntax.
