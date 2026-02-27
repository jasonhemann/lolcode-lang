# Availability Evidence

Generated artifacts:

- `availability.json`
- `AVAILABILITY_REPORT.md`

Generator:

- `./scripts/check_implementation_availability.sh`

## Verdict semantics

- `available_live`: URL currently reachable via live probe.
- `live_unavailable_archived`: live probe unavailable, but archived snapshot found.
- `unavailable_archive_unknown`: live probe unavailable, archive checks inconclusive (timeouts/rate-limits/service errors).
- `vanished_candidate`: live probe unavailable and both archive checks returned explicit `no_snapshot`.

Conservative policy:

- Do not claim a target has "vanished from history" unless verdict is `vanished_candidate`.
