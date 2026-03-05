Keyword case handling is unspecified. Variables are explicitly case-sensitive, but the spec never separately says whether keywords are case-sensitive too. 

lolcode-spec-v1.3

You need a fixed preprocessing order for CR/LF normalization, comma-as-newline, ellipsis continuation, comment stripping, and string shielding; the prose gives all the pieces but not the order.

Unicode ellipsis and ... have to normalize to the same continuation token, but only at logical line end; the spec never says how trailing spaces interact with that.

OBTW/TLDR placement uses “should,” not “must,” so inline block comments in the middle of a command are grammatically ambiguous.

TLDR, <next code> is explicitly valid, so block-comment termination has to hand control back to normal lexing immediately, not only at newline.

HAI version handling is explicitly nonstandard. Decide whether the parser accepts only 1.3, any number, or ignores the version token.

The empty one-line file case HAI 1.3, KTHXBYE only works if comma normalization happens before block parsing.

The slot-operator typo - is lexically dangerous because - already belongs to negative-number syntax. Honoring both would tokenize garbage.

NUMBAR lexical form leaves .5, 2., -.5, and -0. undefined. “Containing exactly one decimal point” is not a full grammar.

String-to-number casting only bans bad characters, not bad placements or multiplicities of - and .. A whitelist parser could accept nonsense like 1-2 or 1.2.3.

Escape syntax never specifies failure mode for malformed hex escapes, unknown Unicode names, surrogates, or out-of-range code points.

Interpolation scanning has to give :: precedence over :{...} or escaped colons will be misread as interpolation starts. 

lolcode-spec-v1.3

Multiword and punctuated keywords require longest-match parsing, not token-by-token ad hoc parsing: O RLY?, IF U SAY SO, IM OUTTA YR, O HAI IM, and so on. 

lolcode-spec-v1.3

The SRS declaration extension is contextual. I HAS A SRS name / I HAS SRS name is special syntax, so “optional A” cannot be generalized safely across the grammar.

The generic assignment grammar is incomplete: one section says <variable> <assignment operator> <expression>, another gives the concrete operator R. That matters if you are deriving an actual grammar from the prose. 

lolcode-spec-v1.3

O RLY? is context-sensitive because it consumes the IT produced by the immediately preceding expression, and the spec allows both newline-separated and comma-separated forms. 

lolcode-spec-v1.3

MEBBE is worded differently from O RLY?: it says “if the expression is WIN,” not “cast the expression to TROOF and test it.” That is either a real semantic distinction or a wording bug. 

lolcode-spec-v1.3

lolcode-spec-v1.3

NO WAI is optional, but YA RLY is not; the grammar needs an explicit rejection story for orphan MEBBE or NO WAI. 

lolcode-spec-v1.3

lolcode-spec-v1.3

WTF? has the same predecessor-binding problem: it operates on IT, and the example shows COLOR, WTF?, so the parser has to define exactly what expression produced the controlling IT. 

lolcode-spec-v1.3

lolcode-spec-v1.3

WTF’s “each literal must be unique” rule is not operationalized. You need to choose parse-time error, load-time error, or runtime trap. 

lolcode-spec-v1.3

Empty OMG blocks are intentional, not accidental; the example has OMG "G" immediately followed by OMG "B". Your AST needs explicit empty-case bodies. 

lolcode-spec-v1.3

Loop labels are required but declared semantically unused. You still need rules for matching, mismatch, duplication, and case sensitivity. 

lolcode-spec-v1.3

Iteration-loop headers mix parse-time and runtime validation. UPPIN/NERFIN are syntax; “any unary function” cannot be fully validated until evaluation time. 

lolcode-spec-v1.3

HOW DUZ I and HOW IZ I are both used in the spec corpus. If you do not declare one canonical and the other editorial debris, your grammar has two competing function-definition forms.

SRS BIZNUS cast is undefined terminology. The spec uses it as if it were established, but never defines what it actually constrains.

O HAI IM’s “Anything I inside the codeblock actually refers to <object>” is not a parser rule; it is a contextual rewrite step. That is exactly the sort of thing that needs formalization or implementations drift.

IT is local in the expression-statement section but “always looked up from global namespace” in bukkit-function scope. Those cannot both be true without a more elaborate environment model than the spec states.

Because O RLY?, WTF?, and comparison idioms all consume IT, you need a closed list of which syntactic forms update IT; the spec explicitly grants that only to bare expressions. 

lolcode-spec-v1.3

VISIBLE is not just another variadic prefix operator. General variadics close with MKAY or implicit end-of-statement closure, while VISIBLE closes on the statement delimiter and has its own suffix !. It needs its own rule.

The trailing ! on VISIBLE is suffix punctuation with one very local meaning. Letting the parser treat it as general punctuation will create nonsense elsewhere.

GIMMEH says it stores into “the given variable,” but never states whether undeclared targets are errors, implicit declarations, or assignments to existing bindings only.

TYPE names like NOOB, YARN, NUMBR, etc. are both bare values of the TYPE type and type designators in cast syntax. They need distinct AST/value categories.

MAEK <expr> [A] <type> and <var> IS NOW A <type> reuse the same type words in different roles, so the parser must treat “type designator” as context-sensitive, not as ordinary identifier/literal parsing.

The comparison section only specifies numeric coercion and then says otherwise there is no automatic casting. That leaves equality for BUKKIT, FUNKSHUN, and TYPE values effectively unspecified.

The “all built in operations return new objects” rule is semantically thin because the spec never says whether object identity is observable, beyond special singleton treatment for WIN/FAIL/NOOB.

The GC/deallocation prose is not really normative semantics. It is not something a conformance suite can test portably.

ME must parse as a valid special expression form anywhere a receiver/object reference can appear, and only fail at runtime when no calling object exists. Static rejection would not match the prose.

ME HAS A and ME'Z ... R ... prove that slot declaration and slot assignment are distinct statement forms, not mere sugar for local-variable assignment to a magic identifier.

HOW IZ <object> <slot> presumes that <object> already exists and is a BUKKIT, but the spec never says whether that is checked when the definition executes, when the slot is called, or at parse time.

Mixin inheritance is static slot-copying, while slot-access function calls are receiver-sensitive and pull variables from the access object. Those two rules only coexist cleanly if you explicitly specify that copied function values remain late-bound to the eventual receiver rather than the source mixin object.
