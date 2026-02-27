# Implementation and Corpus Candidates (from `implementations.pdf`)

Source document: `/Users/jhemann/Code/lolcode-lang/implementations.pdf`  
Extracted with: `pdftotext -layout implementations.pdf -`  
Extraction date: 2026-02-27

This file converts the PDF survey into an actionable shortlist for:

- differential compatibility oracles (suspect, but still useful)
- additional Tier-2 program corpus sources

Status legend:

- `unverified`: listed in PDF, not yet cloned or profiled in this repo
- `seeded`: already included in `corpus/tier2`
- `archive`: historical/archival reference, may need manual recovery

## Priority shortlist

| Tier | Priority | Candidate | Type | Oracle value | Corpus value | Status | URL |
| --- | --- | --- | --- | --- | --- | --- | --- |
| tier1 | P1 | `justinmeza/lci` | C interpreter | High (baseline behavior oracle, known flaws) | Medium (tests/examples) | unverified | [https://github.com/justinmeza/lci](https://github.com/justinmeza/lci) |
| tier1 | P1 | `jD91mZM2/rust-lci` | Rust interpreter | High (independent parser/runtime) | High (likely tests/examples) | unverified | [https://github.com/jD91mZM2/rust-lci](https://github.com/jD91mZM2/rust-lci) |
| tier1 | P1 | `NullDev/I-HAS-JS` | Node.js interpreter/parser | High (different runtime and parser stack) | High (examples likely) | unverified | [https://github.com/NullDev/I-HAS-JS](https://github.com/NullDev/I-HAS-JS) |
| tier1 | P1 | `JasonBock/LOLCode.net` | C# compiler/interpreter toolchain | High (different frontend/backend assumptions) | Medium | unverified | [https://github.com/JasonBock/LOLCode.net](https://github.com/JasonBock/LOLCode.net) |
| tier2 | P2 | `YS-L/hlci` | Haskell interpreter | Medium-High (very different implementation strategy) | Medium | unverified | [https://github.com/YS-L/hlci](https://github.com/YS-L/hlci) |
| tier2 | P2 | `jpcarreon/loco` | Java interpreter with GUI | Medium | Medium | unverified | [https://github.com/jpcarreon/loco](https://github.com/jpcarreon/loco) |
| tier2 | P2 | `qoobaa/lol` | Ruby interpreter | Medium | Medium | unverified | [https://github.com/qoobaa/lol](https://github.com/qoobaa/lol) |
| tier2 | P2 | `SADAsuncion/LOLCodeInterpreter` | Python interpreter | Medium | Medium | unverified | [https://github.com/SADAsuncion/LOLCodeInterpreter](https://github.com/SADAsuncion/LOLCodeInterpreter) |
| tier2 | P2 | `DvaeFroot/cmsc124-lolcode-interpreter` | Python interpreter (GUI) | Low-Medium | Medium | unverified | [https://github.com/DvaeFroot/cmsc124-lolcode-interpreter](https://github.com/DvaeFroot/cmsc124-lolcode-interpreter) |
| tier3 | P3 | `eggyknap/pllolcode` | PostgreSQL extension | Low (not a full general interpreter) | Low-Medium | unverified | [https://github.com/eggyknap/pllolcode](https://github.com/eggyknap/pllolcode) |
| tier2 | P1 | `justinmeza/httpd.lol` | large LOLCODE app corpus | Low | High | seeded | [https://github.com/justinmeza/httpd.lol](https://github.com/justinmeza/httpd.lol) |
| tier2 | P1 | `LeartS/loleuler` | LOLCODE program corpus | Low | High | seeded | [https://github.com/LeartS/loleuler](https://github.com/LeartS/loleuler) |
| tier2 | P1 | `markjreed/eulol` | LOLCODE program corpus | Low | High | seeded | [https://github.com/markjreed/eulol](https://github.com/markjreed/eulol) |

## Archive and historical references

These are likely useful for historical behavior notes, but may not be easy to automate:

- `lolcode-java` (Google Code archive): [https://code.google.com/archive/p/lolcode-java/](https://code.google.com/archive/p/lolcode-java/)
- `LoLCode1337` (SourceForge): [https://sourceforge.net/projects/lolcode-1337/](https://sourceforge.net/projects/lolcode-1337/)
- YALI (Perl, blog reference): [https://kylewoodward.com/yali-yet-another-lolcode-interpreter/](https://kylewoodward.com/yali-yet-another-lolcode-interpreter/)
- Parrot VM compiler docs: [https://parrot.github.io/parrot-docs0/0.6.1/html/languages/lolcode/lolcode.pir.html](https://parrot.github.io/parrot-docs0/0.6.1/html/languages/lolcode/lolcode.pir.html)
- DLR reference post: [https://winterdom.com/2008/02/04/buildingonthedlr](https://winterdom.com/2008/02/04/buildingonthedlr)
- JavaCC/JJTree post: [https://thomasleecopeland.com/2007/09/29/an-lolcode-interpreter-using-jjtree.html](https://thomasleecopeland.com/2007/09/29/an-lolcode-interpreter-using-jjtree.html)
- Parallel/OpenSHMEM extension paper: [https://arxiv.org/pdf/1703.10242](https://arxiv.org/pdf/1703.10242)

## Additional mixed corpus source

- `justinmeza/lollm`: [https://github.com/justinmeza/lollm](https://github.com/justinmeza/lollm)
  - Contains `lolspeak.txt` training data that mixes real LOLCODE and plain lolspeak prose.
  - Useful for robustness tooling, but not a normative conformance corpus.

## Recommended next harvest order

1. `jD91mZM2/rust-lci`
2. `NullDev/I-HAS-JS`
3. `JasonBock/LOLCode.net`
4. `YS-L/hlci`
5. `jpcarreon/loco`

Rationale: these maximize parser/runtime diversity first, which is best for differential testing against a future spec-matching reference implementation.
