#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CATALOG_TSV="$REPO_ROOT/corpus/tier2/CANDIDATE_REPOS.tsv"
EVAL_JSON="$REPO_ROOT/corpus/research/tier2-eval-classified.json"
OUT_DIR="$REPO_ROOT/corpus/research/github_repo_search_lolcode"
OUT_TSV="$OUT_DIR/TRANCHE_PARSE_ERROR_BUCKETS.tsv"
OUT_MD="$OUT_DIR/TRANCHE_PARSE_ERROR_BUCKETS.md"
SOURCE_TAG="${SOURCE_TAG:-github-repo-search-lolcode-curated-2026-04-01}"
TMP_DIR="$(mktemp -d "${TMPDIR:-/tmp}/github-tranche-parse-errors.XXXXXX")"

cleanup_tmp() {
  rm -f "$TMP_DIR"/* 2>/dev/null || true
  rmdir "$TMP_DIR" 2>/dev/null || true
}
trap cleanup_tmp EXIT

usage() {
  cat <<'EOF'
Usage:
  ./scripts/analyze_github_repo_search_tranche_parse_errors.sh
  ./scripts/analyze_github_repo_search_tranche_parse_errors.sh --source-tag TAG

Outputs:
  - corpus/research/github_repo_search_lolcode/TRANCHE_PARSE_ERROR_BUCKETS.tsv
  - corpus/research/github_repo_search_lolcode/TRANCHE_PARSE_ERROR_BUCKETS.md
EOF
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --source-tag)
      [ "$#" -lt 2 ] && { echo "Missing value for --source-tag" >&2; exit 2; }
      SOURCE_TAG="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

for cmd in awk date jq mktemp sort; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "Missing required command: $cmd" >&2
    exit 1
  fi
done

[ -f "$CATALOG_TSV" ] || {
  echo "Missing catalog: $CATALOG_TSV" >&2
  exit 1
}

[ -f "$EVAL_JSON" ] || {
  echo "Missing eval report: $EVAL_JSON" >&2
  echo "Run ./scripts/eval_tier2_corpus.sh first." >&2
  exit 1
}

mkdir -p "$OUT_DIR"

labels_tsv="$TMP_DIR/labels.tsv"
rows_tsv="$TMP_DIR/rows.tsv"
stats_tsv="$TMP_DIR/stats.tsv"
repo_counts_tsv="$TMP_DIR/repo-counts.tsv"

awk -F '\t' -v source_tag="$SOURCE_TAG" '
  NR > 1 && $7 == source_tag { print $2 "\t" $4 }
' "$CATALOG_TSV" > "$labels_tsv"

[ -s "$labels_tsv" ] || {
  echo "No candidate rows found for source tag: $SOURCE_TAG" >&2
  exit 1
}

jq -r '
  .rows[]
  | select(.outcome == "parse-error")
  | [.path, (.["first-meaningful-line"] // ""), ((.message // "") | split("\n")[0])]
  | @tsv
' "$EVAL_JSON" > "$rows_tsv"

awk -F '\t' \
  -v bucket_out="$OUT_TSV" \
  -v stats_out="$stats_tsv" \
  -v repo_out="$repo_counts_tsv" '
  function bucket(first, msg) {
    if (msg == "parse-source: program must begin with HAI opener (no leading comments or tokens before HAI)") {
      return "leading-material-before-hai"
    }
    if (msg ~ /^parse-source: unsupported version: 1\.2/) {
      return "unsupported-version-1.2"
    }
    if (msg ~ /^parse-source: unsupported version: 1\.4/) {
      return "unsupported-version-1.4"
    }
    if (((first == "HAI") || (first == "HAI BTW THIS IS A COMMENT")) && msg ~ /unexpected NEWLINE/ && msg ~ /col 4$/) {
      return "split-hai-header"
    }
    if (msg ~ /unexpected ID \(".*\?"\)/ || first ~ /CAN HAS /) {
      return "extension-import-or-question-id"
    }
    if (msg ~ /unexpected STRING \(\(yarn-template/) {
      return "string-literal-at-non-expression-site"
    }
    if (msg ~ /^parse-source: duplicate OMG literal/ || msg ~ /^parse-source: WTF\? case literal must be/) {
      return "strict-switch-negative-fixture"
    }
    if (msg ~ /^parse-source: invalid identifier syntax:/) {
      return "invalid-identifier-syntax"
    }
    if (msg ~ /^parse-source: invalid numeric literal:/) {
      return "invalid-numeric-literal"
    }
    if (msg ~ /^parse-source: no material allowed after KTHXBYE/) {
      return "post-kthxbye-material"
    }
    if (msg ~ /^parse-source: implicit MKAY omission/) {
      return "implicit-mkay-boundary"
    }
    if (msg ~ /^parse-source: syntax error:/) {
      return "other-grammar-drift"
    }
    return "other-parse-error"
  }

  BEGIN {
    order[1] = "split-hai-header"
    order[2] = "leading-material-before-hai"
    order[3] = "unsupported-version-1.2"
    order[4] = "unsupported-version-1.4"
    order[5] = "extension-import-or-question-id"
    order[6] = "string-literal-at-non-expression-site"
    order[7] = "strict-switch-negative-fixture"
    order[8] = "invalid-identifier-syntax"
    order[9] = "invalid-numeric-literal"
    order[10] = "post-kthxbye-material"
    order[11] = "implicit-mkay-boundary"
    order[12] = "other-grammar-drift"
    order[13] = "other-parse-error"
  }

  FNR == NR {
    kind[$1] = $2
    next
  }

  {
    split($1, parts, "/")
    label = parts[3]
    if (!(label in kind)) {
      next
    }

    bucket_name = bucket($2, $3)
    total += 1
    count[bucket_name] += 1
    repo_count[label] += 1

    if (!(bucket_name in example_path)) {
      example_path[bucket_name] = $1
      example_msg[bucket_name] = $3
    }

    if ($1 ~ /\/test\/1\.3-Tests\// || $1 ~ /\/spec\/source\//) {
      imported_overlay += 1
    }
  }

  END {
    print "bucket\tcount\texample_path\texample_message" > bucket_out
    for (i = 1; i <= 13; i += 1) {
      name = order[i]
      if ((name in count) && count[name] > 0) {
        print name "\t" count[name] "\t" example_path[name] "\t" example_msg[name] >> bucket_out
      }
    }

    print "metric\tvalue" > stats_out
    print "total-parse-errors\t" total >> stats_out
    print "imported-negative-fixture-overlay\t" imported_overlay >> stats_out

    print "label\tcount" > repo_out
    for (label in repo_count) {
      print label "\t" repo_count[label] >> repo_out
    }
  }
' "$labels_tsv" "$rows_tsv"

total_parse_errors="$(awk -F '\t' '$1=="total-parse-errors" {print $2}' "$stats_tsv")"
imported_overlay="$(awk -F '\t' '$1=="imported-negative-fixture-overlay" {print $2}' "$stats_tsv")"
generated_at="$(date -u +'%Y-%m-%dT%H:%M:%SZ')"

{
  echo '# Broad-Search Tranche Parse Error Buckets'
  echo
  printf -- '- Generated: %s\n' "$generated_at"
  printf -- '- Source tag: `%s`\n' "$SOURCE_TAG"
  echo '- Eval source: `corpus/research/tier2-eval-classified.json`'
  printf -- '- New-tranche parse errors: `%s`\n' "$total_parse_errors"
  printf -- '- Imported negative-fixture overlay: `%s`\n' "$imported_overlay"
  echo
  echo 'Primary buckets are language-cause buckets, not provenance buckets.'
  echo 'The imported negative-fixture overlay is a separate count of rows whose'
  echo 'paths came from bundled conformance/spec-negative suites.'
  echo
  echo '## Bucket Counts'
  echo
  echo '| Bucket | Count | Example |'
  echo '|---|---:|---|'
  awk -F '\t' '
    NR > 1 {
      printf "| `%s` | `%s` | `%s` |\n", $1, $2, $3
    }
  ' "$OUT_TSV"
  echo
  echo '## Top Parse-Error Repos'
  echo
  echo '| Label | Parse errors |'
  echo '|---|---:|'
  sort -t "$(printf '\t')" -k2,2nr "$repo_counts_tsv" \
    | awk -F '\t' 'NR > 1 { printf "| `%s` | `%s` |\n", $1, $2 }' \
    | sed -n '1,20p'
  echo
  echo '## Notes'
  echo
  echo '- `split-hai-header` is the classic bare-`HAI`/newline-open form that strict `1.3` rejects.'
  echo '- `leading-material-before-hai` captures files with prose, comments, or other tokens before the opener.'
  echo '- `unsupported-version-*` is version mismatch, not general parser confusion.'
  echo '- `extension-import-or-question-id` mostly reflects `CAN HAS ...?` or similar non-strict extension syntax.'
  echo '- `other-grammar-drift` is the remaining long tail of noncanonical operator/keyword/statement forms.'
} > "$OUT_MD"

echo "wrote $OUT_TSV"
echo "wrote $OUT_MD"
