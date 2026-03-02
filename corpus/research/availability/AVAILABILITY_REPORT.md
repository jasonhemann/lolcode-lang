# Implementation Availability Report

Generated: `2026-03-02T05:49:40Z`

Policy:

- `vanished_candidate` means live probe failed **and** both archive checks were definitively `no_snapshot`.
- If any archive endpoint is rate-limited, timed out, or unavailable, verdict stays conservative (`unavailable_archive_unknown`).

## Catalog Repos

| Tier | Label | Repo | Verdict | GitHub API | Live | Archive.org | Archive.is |
| --- | --- | --- | --- | --- | --- | --- | --- |
| tier1 | lci | justinmeza/lci | available_live | 200 | 200 | error | skipped_live_available |
| tier1 | rust-lci | jD91mZM2/rust-lci | available_live | 200 | 200 | snapshot | skipped_live_available |
| tier1 | i-has-js | NullDev/I-HAS-JS | available_live | 200 | 200 | error | skipped_live_available |
| tier1 | lolcode-net | JasonBock/LOLCode.net | available_live | 200 | 200 | error | skipped_live_available |
| tier2 | hlci | YS-L/hlci | available_live | 200 | 200 | snapshot | skipped_live_available |
| tier2 | loco | jpcarreon/loco | available_live | 200 | 200 | no_snapshot | skipped_live_available |
| tier2 | lol-ruby | qoobaa/lol | available_live | 200 | 200 | snapshot | skipped_live_available |
| tier2 | lolcode-py-sada | SADAsuncion/LOLCodeInterpreter | available_live | 200 | 200 | error | skipped_live_available |
| tier2 | lolcode-py-cmsc124 | DvaeFroot/cmsc124-lolcode-interpreter | available_live | 200 | 200 | no_snapshot | skipped_live_available |
| tier2 | httpd-lol | justinmeza/httpd.lol | available_live | 200 | 200 | error | skipped_live_available |
| tier2 | loleuler | LeartS/loleuler | available_live | 200 | 200 | error | skipped_live_available |
| tier2 | eulol | markjreed/eulol | available_live | 200 | 200 | snapshot | skipped_live_available |
| tier2 | lokalise-lol-post | bodrovis-learning/Lokalise-source | available_live | 200 | 200 | snapshot | skipped_live_available |
| tier2 | lolcode-simple-algorithms | shaunlgs/lolcode-simple-algorithms | available_live | 200 | 200 | error | skipped_live_available |
| tier2 | lolcode-experiments | theDrake/lolcode-experiments | available_live | 200 | 200 | error | skipped_live_available |
| tier2 | lolcode-game-of-life | superkrzysio/lolcode-game-of-life | available_live | 200 | 200 | error | skipped_live_available |
| tier2 | flag-wars-3-lolcode | SomeUnusualGames/Flag-Wars-3-LOLCODE | available_live | 200 | 200 | snapshot | skipped_live_available |
| tier2 | learn-lolcode | seanpm2001/Learn-LOLCODE | available_live | 200 | 200 | snapshot | skipped_live_available |
| tier2 | ai2001-sc-lolcode | seanpm2001/AI2001_Category-Source_Code-SC-LOLCODE | available_live | 200 | 200 | no_snapshot | skipped_live_available |
| tier2 | mkkellogg-lolcode | mkkellogg/lolcode | vanished_candidate | 404 | 404 | no_snapshot | no_snapshot |
| tier2 | wpollock-lolcode | wpollock/lolcode | unavailable_archive_unknown | 404 | 404 | error | no_snapshot |
| tier2 | jasondelponte-lolcode | jasondelponte/lolcode | unavailable_archive_unknown | 404 | 404 | error | no_snapshot |
| tier2 | subcity9000-lolcode | subcity9000/lolcode | vanished_candidate | 404 | 404 | no_snapshot | no_snapshot |
| tier2 | 2ionx-lolcode | 2IONX/LOLCODE | unavailable_archive_unknown | 404 | 404 | error | no_snapshot |
| tier2 | kartiknair-lolcode-interpreter | kartiknair/lolcode-interpreter | vanished_candidate | 404 | 404 | no_snapshot | no_snapshot |
| tier2 | shi2015-lolcode-interpreter | SHI2015/Lolcode-Interpreter | unavailable_archive_unknown | 404 | 404 | error | no_snapshot |
| tier2 | lorenzoperi17-lolcode-interpreter | LorenzoPeri17/lolcode-interpreter | vanished_candidate | 404 | 404 | no_snapshot | no_snapshot |
| tier2 | rileyjshaw-loljs | rileyjshaw/loljs | unavailable_archive_unknown | 404 | 404 | error | no_snapshot |
| tier2 | aurasphere-ftpd-lol | aurasphere/ftpd.lol | available_live | 200 | 200 | error | skipped_live_available |
| tier2 | nicodecastro-lolcode-interpreter | nicodecastro/lolcode-interpreter | available_live | 200 | 200 | no_snapshot | skipped_live_available |
| tier2 | bernardjezua-lolcode-interpreter | bernardjezua/LOLCODE-Interpreter | available_live | 200 | 200 | error | skipped_live_available |
| tier2 | coleenagsao-python-lolcode-interpreter | coleenagsao/python-lolcode-interpreter | available_live | 200 | 200 | no_snapshot | skipped_live_available |
| tier2 | yngve-lci | yngve/lci | unavailable_archive_unknown | 404 | 404 | error | no_snapshot |
| tier3 | pllolcode | eggyknap/pllolcode | available_live | 200 | 200 | snapshot | skipped_live_available |

## PDF Citation Links

| URL | Verdict | Live | Archive.org | Archive.is |
| --- | --- | --- | --- | --- |
| https://arxiv.org/pdf/1703.10242 | available_live | 200 | snapshot | skipped_live_available |
| https://code.google.com/archive/p/lolcode-java/ | available_live | 200 | error | skipped_live_available |
| https://github.com/jpcarreon/loco/blob/master/README.md | available_live | 200 | error | skipped_live_available |
| https://kylewoodward.com/yali-yet-another-lolcode-interpreter/ | available_live | 200 | error | skipped_live_available |
| https://lolcode.org/ | available_live | 200 | error | skipped_live_available |
| https://parrot.github.io/parrot-docs0/0.6.1/html/languages/lolcode/lolcode.pir.html | available_live | 200 | error | skipped_live_available |
| https://raw.githubusercontent.com/YS-L/hlci/master/README.md | available_live | 200 | error | skipped_live_available |
| https://raw.githubusercontent.com/qoobaa/lol/master/README.rdoc | available_live | 200 | error | skipped_live_available |
| https://sourceforge.net/projects/lolcode-1337/ | available_live | 200 | snapshot | skipped_live_available |
| https://thomasleecopeland.com/2007/09/29/an-lolcode-interpreter-using-jjtree.html | available_live | 200 | error | skipped_live_available |
| https://winterdom.com/2008/02/04/buildingonthedlr | available_live | 200 | snapshot | skipped_live_available |
| https://www.dcode.fr/lolcode-language | live_unavailable_archived | 403 | snapshot | no_snapshot |
| https://www.mybackdeck.com/lolcode/ | available_live | 200 | error | skipped_live_available |
| https://www.pmichaud.com/2008/pres/yapc-pct/slides/slide68e.html | available_live | 200 | no_snapshot | skipped_live_available |
| https://ypologistisglossarion.blogspot.com/2012/10/lol.html | available_live | 200 | error | skipped_live_available |

## Vanished Candidates

- catalog: mkkellogg/lolcode (https://github.com/mkkellogg/lolcode)
- catalog: subcity9000/lolcode (https://github.com/subcity9000/lolcode)
- catalog: kartiknair/lolcode-interpreter (https://github.com/kartiknair/lolcode-interpreter)
- catalog: LorenzoPeri17/lolcode-interpreter (https://github.com/LorenzoPeri17/lolcode-interpreter)

## Archive Evidence Notes

- jD91mZM2/rust-lci | archive.org: https://web.archive.org/web/20251022100708/https://github.com/jD91mZM2/rust-lci
- YS-L/hlci | archive.org: https://web.archive.org/web/20201025193017/https://github.com/YS-L/hlci
- qoobaa/lol | archive.org: https://web.archive.org/web/20260227062501/https://github.com/qoobaa/lol
- markjreed/eulol | archive.org: https://web.archive.org/web/20221220134003/https://github.com/markjreed/eulol
- bodrovis-learning/Lokalise-source | archive.org: https://web.archive.org/web/20201023211502/https://github.com/bodrovis-learning/Lokalise-source
- SomeUnusualGames/Flag-Wars-3-LOLCODE | archive.org: https://web.archive.org/web/20231119215703/https://github.com/SomeUnusualGames/Flag-Wars-3-LOLCODE/
- seanpm2001/Learn-LOLCODE | archive.org: https://web.archive.org/web/20240910014922/https://github.com/seanpm2001/Learn-LOLCODE
- eggyknap/pllolcode | archive.org: https://web.archive.org/web/20250126203651/https://github.com/eggyknap/pllolcode
- https://arxiv.org/pdf/1703.10242 | archive.org: https://web.archive.org/web/20240605165310/https://arxiv.org/pdf/1703.10242
- https://sourceforge.net/projects/lolcode-1337/ | archive.org: https://web.archive.org/web/20250428135222/https://sourceforge.net/projects/lolcode-1337/
- https://winterdom.com/2008/02/04/buildingonthedlr | archive.org: https://web.archive.org/web/20240815193131/https://winterdom.com/2008/02/04/buildingonthedlr
- https://www.dcode.fr/lolcode-language | archive.org: https://web.archive.org/web/20260218175634/https://www.dcode.fr/lolcode-language
