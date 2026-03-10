# Rejected After Auto-Promotion (Strict 1.3)

Date: 2026-03-02

These files were initially auto-promoted (`HAI 1.3` + marker comment) for triage, then reverted to original header form (`HAI`) and marked rejected/non-compliant under strict 1.3 policy.

Reason: non-compliant YARN escaping (uses unescaped `:` in string literals, which triggers string-escape parsing behavior).

## Rejected Files

- `corpus/research/promoted-1_3-programs/bernardjezua-lolcode-interpreter/files/testcases/final/05_bool.lol`
- `corpus/research/promoted-1_3-programs/coleenagsao-python-lolcode-interpreter/files/lolcode-imports/05_bool.lol`
- `corpus/research/promoted-1_3-programs/garthendrich-lolcode-interpreter/files/sample_codes/05_bool.lol`
- `corpus/research/promoted-1_3-programs/lolcode-py-cmsc124/files/project-examples/05_bool.lol`
- `corpus/research/promoted-1_3-programs/lolcode-py-sada/files/CMSC_124_testcases/05_bool.lol`
- `corpus/research/promoted-1_3-programs/nicodecastro-lolcode-interpreter/files/tests/05_bool.lol`
- `corpus/research/promoted-1_3-programs/sallysanban-lolcode-interpreter/files/Project 3/EZR_B-4L/source code/Test Files/05_bool.lol`

## Machine-Readable Source

- `corpus/research/PROMOTED_1_3_REJECTED_NONCOMPLIANT.json`
