# Implementation Availability Report

Generated: `2026-02-27T22:43:22Z`

Policy:

- `vanished_candidate` means live probe failed **and** both archive checks were definitively `no_snapshot`.
- If any archive endpoint is rate-limited, timed out, or unavailable, verdict stays conservative (`unavailable_archive_unknown`).

## Catalog Repos

| Tier | Label | Repo | Verdict | GitHub API | Live | Archive.org | Archive.is |
| --- | --- | --- | --- | --- | --- | --- | --- |
| tier1 | lci | justinmeza/lci | available_live | 200 | 200 | error | skipped_live_available |
| tier1 | rust-lci | jD91mZM2/rust-lci | available_live | 200 | 200 | error | skipped_live_available |
| tier1 | i-has-js | NullDev/I-HAS-JS | available_live | 200 | 200 | snapshot | skipped_live_available |
| tier1 | lolcode-net | JasonBock/LOLCode.net | available_live | 200 | 200 | snapshot | skipped_live_available |
| tier2 | hlci | YS-L/hlci | available_live | 200 | 200 | error | skipped_live_available |
| tier2 | loco | jpcarreon/loco | available_live | 200 | 200 | error | skipped_live_available |
| tier2 | lol-ruby | qoobaa/lol | available_live | 200 | 200 | snapshot | skipped_live_available |
| tier2 | lolcode-py-sada | SADAsuncion/LOLCodeInterpreter | available_live | 200 | 200 | error | skipped_live_available |
| tier2 | lolcode-py-cmsc124 | DvaeFroot/cmsc124-lolcode-interpreter | available_live | 200 | 200 | no_snapshot | skipped_live_available |
| tier2 | httpd-lol | justinmeza/httpd.lol | available_live | 200 | 200 | error | skipped_live_available |
| tier2 | loleuler | LeartS/loleuler | available_live | 200 | 200 | error | skipped_live_available |
| tier2 | eulol | markjreed/eulol | available_live | 200 | 200 | snapshot | skipped_live_available |
| tier3 | pllolcode | eggyknap/pllolcode | available_live | 200 | 200 | snapshot | skipped_live_available |

## PDF Citation Links

| URL | Verdict | Live | Archive.org | Archive.is |
| --- | --- | --- | --- | --- |
| https://arxiv.org/pdf/1703.10242 | available_live | 200 | error | skipped_live_available |
| https://code.google.com/archive/p/lolcode-java/ | available_live | 200 | error | skipped_live_available |
| https://github.com/jpcarreon/loco/blob/master/README.md | available_live | 200 | no_snapshot | skipped_live_available |
| https://kylewoodward.com/yali-yet-another-lolcode-interpreter/ | available_live | 200 | error | skipped_live_available |
| https://lolcode.org/ | available_live | 200 | error | skipped_live_available |
| https://parrot.github.io/parrot-docs0/0.6.1/html/languages/lolcode/lolcode.pir.html | available_live | 200 | no_snapshot | skipped_live_available |
| https://raw.githubusercontent.com/YS-L/hlci/master/README.md | available_live | 200 | no_snapshot | skipped_live_available |
| https://raw.githubusercontent.com/qoobaa/lol/master/README.rdoc | available_live | 200 | no_snapshot | skipped_live_available |
| https://sourceforge.net/projects/lolcode-1337/ | available_live | 200 | snapshot | skipped_live_available |
| https://thomasleecopeland.com/2007/09/29/an-lolcode-interpreter-using-jjtree.html | available_live | 200 | error | skipped_live_available |
| https://winterdom.com/2008/02/04/buildingonthedlr | available_live | 200 | error | skipped_live_available |
| https://www.dcode.fr/lolcode-language | unavailable_archive_unknown | 403 | error | no_snapshot |
| https://www.mybackdeck.com/lolcode/ | available_live | 200 | error | skipped_live_available |
| https://www.pmichaud.com/2008/pres/yapc-pct/slides/slide68e.html | available_live | 200 | no_snapshot | skipped_live_available |
| https://ypologistisglossarion.blogspot.com/2012/10/lol.html | available_live | 200 | snapshot | skipped_live_available |

## Vanished Candidates

- none

## Archive Evidence Notes

- NullDev/I-HAS-JS | archive.org: https://web.archive.org/web/20260210224508/https://github.com/NullDev/I-HAS-JS
- JasonBock/LOLCode.net | archive.org: https://web.archive.org/web/20241228070340/https://github.com/JasonBock/LOLCode.net
- qoobaa/lol | archive.org: https://web.archive.org/web/20260227062501/https://github.com/qoobaa/lol
- markjreed/eulol | archive.org: https://web.archive.org/web/20221220134003/https://github.com/markjreed/eulol
- eggyknap/pllolcode | archive.org: https://web.archive.org/web/20250126203651/https://github.com/eggyknap/pllolcode
- https://sourceforge.net/projects/lolcode-1337/ | archive.org: https://web.archive.org/web/20250428135222/https://sourceforge.net/projects/lolcode-1337/
- https://ypologistisglossarion.blogspot.com/2012/10/lol.html | archive.org: https://web.archive.org/web/20241225094908/http://ypologistisglossarion.blogspot.com/2012/10/lol.html
