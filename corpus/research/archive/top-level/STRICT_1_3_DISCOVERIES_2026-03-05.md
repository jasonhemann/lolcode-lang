# Strict 1.3 Discoveries and Decisions

Date: 2026-03-05

## Purpose

This note captures high-signal findings from corpus/implementation comparisons that affect strict 1.3 conformance decisions.

## Confirmed Strict Decisions

- Only `HAI 1.3` is accepted by policy.
- `CAN HAS ...` is not part of upstream 1.2/1.3 spec snapshots and is treated as out-of-scope extension syntax.
- `STRING'Z ...`/`STDIO` namespace behaviors are extension APIs, not strict 1.3 semantics.
- Operator spelling remains strict (`DIFF`, `QUOSHUNT`, etc.); permissive aliases are rejected.
- Numeric YARN casting remains strict lexical numeric acceptance; relaxed forms are rejected.

## Unwarranted Extension Patterns Seen In Corpora

- `CAN HAS <LIB>?` (e.g., `STRING`, `STDIO`, `SOCKS`, `STDLIB`).
- Library-qualified namespace call families (`STRING'Z LEN`, `STRING'Z AT`, etc.).
- Dialect-only syntax (`WAZZUP` / `BUHBYE`).
- Header/version drift (`HAI` without version, nonstandard header metadata).

## External Implementation Drift/Bug Patterns

- Some implementations/corpora accept non-spec extensions while labeling programs as "1.3".
- Some implementations accept relaxed numeric casts that violate strict numeric lexical rules.
- Some parser implementations are permissive about misspelled operators.
- Some implementations differ on strict statement delimitation/parsing edge cases.

## What We Changed In Response

- Removed `CAN HAS` parser/runtime path from strict core.
- Removed runtime extension registration path for `STRING'Z`/`STDIO`.
- Removed import statement from strict AST surface.
- Added/updated strict negative tests for extension rejection and non-spec call forms.
- Updated status docs to separate strict conformance findings from extension observations.
- Updated external issue queue generation to label each item with `spec_scope` (`core-1.2-1.3`, `extension`, `unknown`).
- Updated corpus sync progress indexing to track core-vs-extension candidate repro counts per repo/tier.
- Hardened external queue refresh so failed GitHub auth/network uses cached snapshots instead of wiping queue/raw artifacts.

## Newly Confirmed Strict-Core Gaps (2026-03-05)

- `TYPE` literal domain is partial (`spec line 259`):
  - Bare type words (e.g., `NUMBR`) currently parse as identifiers.
  - Traceability status: `partial`.
- Object-function `IT` lookup differs from spec text (`spec line 672`):
  - Current method call frames use method-local `IT`.
  - Spec text indicates lookup from global namespace in object-function context.
  - Traceability status: `known-divergence`.

## Tracking Guidance

- Classify failures first as: strict-core regression vs out-of-scope extension vs invalid input.
- Do not treat extension-heavy corpus failures as core conformance failures.
- Keep a separate extension ledger (this research tree) to preserve ecosystem context without widening strict scope.
