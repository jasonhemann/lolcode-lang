# Package Release Checklist

- [ ] `./scripts/test_racket.sh` passes
- [ ] `./scripts/check_spec_traceability.sh` passes
- [ ] CLI smoke runs succeed (`lolcode`, `raco lolcode`)
- [ ] `#lang lolcode` smoke module executes
- [ ] `./scripts/build_cli_exe.sh` succeeds on target host
- [ ] `./scripts/package_cli_dist.sh` produces runnable bundle
- [ ] `info.rkt` metadata reviewed (version, deps, authors)
- [ ] README updated for current release changes
- [ ] Tag and publish workflow reviewed
