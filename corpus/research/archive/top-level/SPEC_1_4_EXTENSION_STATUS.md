# LOLCODE "1.4" Ersatz Spec Status

Last updated: 2026-03-05

## Decision

- Treat "1.4" as an implementation-specific extension set, not a normative language spec.
- Do not target 1.4 for current compliance work.
- Current normative target remains strict 1.3 behavior only.
- Extension behavior is not enabled in the main interpreter path.

## Why (from collected evidence)

- No authoritative `v1.4` spec artifact is present in the canonical spec repo (`justinmeza/lolcode-spec`).
- Official language site materials remain centered on `HAI 1.2`.
- Historical discussion indicates 1.4-style features lived in `lci` `future` branch as experimental features pending a new spec.

This supports classifying "1.4" as a de facto label for one implementation lineage, not a ratified standard.

## 1.4-like Feature Surface to Track (Future Work)

The evidence points to a library/module style extension model:

- `CAN HAS <LIB>?` imports (examples seen: `STDIO`, `STRING`, `SOCKS`)
- library-qualified calls (e.g., `LIB'Z FUNC ...`)
- implementation-provided library functions, especially string/network/stdio helpers

These should be treated as extension APIs with unstable naming/semantics across references.

## Current Runtime/Parser Posture

- `CAN HAS ...` is intentionally unsupported in strict core mode.
- `STRING'Z`/`STDIO` extension registration paths were removed from runtime.
- Corpus examples using these features are labeled extension/out-of-scope, not core regressions.

## Non-Goals For Current Phase

- No parser or runtime requirements are derived from 1.4 for baseline milestone acceptance.
- No 1.4 behavior is used as an oracle for core 1.2/1.3 conformance.
- No "LOLCODE 1.4 compliant" claim should be made.

## Future Compatibility Plan (When We Opt In)

- Add an explicit extension mode flag (e.g., `--extensions=lci-1.4`).
- Keep extensions namespaced as implementation-profile behavior, separate from normative semantics.
- Build separate tests for extension mode; do not merge into core conformance suite.
- Prefer differential tests against `lci` `future` branch and preserve expected known divergences.
- If this mode is ever added, keep it behind an explicit opt-in profile and separate AST/runtime hooks.

## Primary Source Pointers

- `lci-general` thread on C/C++ integration (`HAI 1.4`, `CAN HAS STDIO?`):
  - https://groups.google.com/g/lci-general/c/fF9J8iprVSc
- `lci-general` thread on string index/length (`HAI 1.4`, `CAN HAS STRING?`, `future` branch context):
  - https://groups.google.com/g/lci-general/c/u5TRRjdArMk
- Community note stating no official 1.4 document:
  - https://groups.google.com/g/lci-general/c/UHHLk2_5Wzw
- Canonical spec repo (no official 1.4 directory):
  - https://github.com/justinmeza/lolcode-spec
- Official site reference point:
  - https://lolcode.org/

## Project Policy Summary

- Core project scope: spec-matching 1.2/1.3 implementation.
- 1.4: documented, deferred, and intentionally isolated as non-normative extension parity work.
